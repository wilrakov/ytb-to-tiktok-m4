from __future__ import annotations

import argparse
import os
import sys
import subprocess
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from uuid import uuid4

from rich.console import Console
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TextColumn

console = Console()


@dataclass
class DownloadResult:
    video_path: Path
    title: str


def ensure_ffmpeg_in_path() -> tuple[str, str]:
    """Ensure ffmpeg is available. imageio-ffmpeg provides a binary path we can expose.

    Returns tuple of (ffmpeg_path, ffprobe_path) for direct use in subprocess calls.
    """
    try:
        import imageio_ffmpeg

        ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_dir = Path(ffmpeg_path).parent
        
        # Construire le chemin vers ffprobe (même répertoire que ffmpeg)
        ffprobe_path = ffmpeg_dir / "ffprobe-win-x86_64-v7.1.exe"
        if not ffprobe_path.exists():
            # Essayer d'autres noms possibles
            for name in ["ffprobe.exe", "ffprobe"]:
                candidate = ffmpeg_dir / name
                if candidate.exists():
                    ffprobe_path = candidate
                    break
            else:
                # Si ffprobe n'est pas trouvé, utiliser ffmpeg avec -i pour obtenir la durée
                ffprobe_path = None
        
        return str(ffmpeg_path), str(ffprobe_path) if ffprobe_path else None
    except Exception as exc:  # pragma: no cover - defensive
        console.print(f"[yellow]Attention:[/] ffmpeg introuvable automatiquement ({exc}). Assurez-vous qu'il est installé et dans PATH.")
        return "ffmpeg", "ffprobe"  # Fallback aux commandes système


def download_youtube(
    url: str,
    out_dir: Path,
    cookies_file: Optional[Path] = None,
    cookies_from_browser: Optional[str] = None,
    user_agent: Optional[str] = None,
    proxy: Optional[str] = None,
) -> DownloadResult:
    from yt_dlp import YoutubeDL

    out_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
        "format": "mp4/bestvideo+bestaudio/best",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        # Améliore la compat YouTube en utilisant le client Android par défaut
        "extractor_args": {"youtube": {"player_client": ["android"]}},
    }

    if cookies_file is not None:
        ydl_opts["cookiefile"] = str(cookies_file)
    if cookies_from_browser is not None:
        # Format attendu: (browser, profile, keyring, browser_dir)
        ydl_opts["cookiesfrombrowser"] = (cookies_from_browser, None, None, None)
    if user_agent is not None:
        ydl_opts["http_headers"] = {"User-Agent": user_agent}
    if proxy is not None:
        ydl_opts["proxy"] = proxy

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title") or "video"
        # Compute actual output path. yt-dlp may choose ext.
        # Prefer mp4; fall back to first matching file by title.
        candidate_mp4 = out_dir / f"{title}.mp4"
        if candidate_mp4.exists():
            video_path = candidate_mp4
        else:
            # Search any file with the exact title prefix
            matches = list(out_dir.glob(f"{title}.*"))
            if not matches:
                raise FileNotFoundError("Fichier vidéo téléchargé introuvable")
            video_path = matches[0]

    return DownloadResult(video_path=video_path, title=title)


def split_video_ffmpeg(input_path: Path, out_dir: Path, segment_seconds: int = 60, limit: Optional[int] = None) -> list[Path]:
    ffmpeg_path, ffprobe_path = ensure_ffmpeg_in_path()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build segment pattern: basename_0001.mp4
    base = input_path.stem
    output_pattern = str(out_dir / f"{base}_%04d.mp4")

    # Probe duration
    duration = probe_duration_seconds(input_path)
    if duration is None:
        raise RuntimeError("Impossible d'obtenir la durée de la vidéo (ffprobe)")

    # Si vidéo plus courte que la durée de segment demandée: produire un seul clip
    if duration <= float(segment_seconds):
        console.print("[yellow]La vidéo est plus courte que la durée de segment demandée; un seul clip sera produit.[/]")
        single_out = str(out_dir / f"{base}_0000.mp4")
        cmd_single = [
            ffmpeg_path,
            "-y",
            "-i",
            str(input_path),
            "-c",
            "copy",
            single_out,
        ]
        proc_single = subprocess.run(cmd_single, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc_single.returncode != 0:
            raise RuntimeError(f"ffmpeg a échoué:\n{proc_single.stderr}")
        return [Path(single_out)]

    # Calculer des points de coupe garantissant un dernier segment >= segment_seconds
    # Exemple: pour 12m30s et 60s -> coupes à 60,120,..., (N-1)*60 ; le dernier sera >=60s
    total_seconds = float(duration)
    n_full = int(total_seconds // float(segment_seconds))
    remainder = total_seconds - (n_full * float(segment_seconds))

    # Générer les temps de segment uniquement jusqu'à (n_full - 1) * S si remainder > 0
    cut_count = max(n_full - 1, 0) if remainder > 0 else max(n_full - 1, 0)
    cut_times = [float(segment_seconds) * i for i in range(1, cut_count + 1)]

    if not cut_times:
        # Il n'y a qu'un seul segment (>= segment_seconds), copier tel quel
        single_out = str(out_dir / f"{base}_0000.mp4")
        cmd_single = [
            ffmpeg_path,
            "-y",
            "-i",
            str(input_path),
            "-c",
            "copy",
            single_out,
        ]
        proc_single = subprocess.run(cmd_single, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc_single.returncode != 0:
            raise RuntimeError(f"ffmpeg a échoué:\n{proc_single.stderr}")
        return [Path(single_out)]

    # Re-encodage avec -segment_times pour garantir des coupes exactes et dernier segment >= S
    segment_times_arg = ",".join(f"{t:.3f}" for t in cut_times)
    cmd_segment = [
        ffmpeg_path,
        "-y",
        "-i",
        str(input_path),
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-b:a",
        "128k",
        "-f",
        "segment",
        "-segment_times",
        segment_times_arg,
        "-reset_timestamps",
        "1",
        output_pattern,
    ]
    proc_segment = subprocess.run(cmd_segment, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc_segment.returncode != 0:
        raise RuntimeError(f"ffmpeg a échoué:\n{proc_segment.stderr}")

    parts = sorted(out_dir.glob(f"{base}_*.mp4"))
    if limit is not None:
        parts = parts[:limit]
    return parts


def probe_duration_seconds(input_path: Path) -> Optional[float]:
    ffmpeg_path, ffprobe_path = ensure_ffmpeg_in_path()
    
    # Si ffprobe n'est pas disponible, utiliser ffmpeg avec -i pour obtenir la durée
    if ffprobe_path is None:
        return _get_duration_with_ffmpeg(input_path, ffmpeg_path)
    
    cmd = [
        ffprobe_path,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(input_path),
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        return None
    try:
        return float(proc.stdout.strip())
    except ValueError:
        return None


def _get_duration_with_ffmpeg(input_path: Path, ffmpeg_path: str) -> Optional[float]:
    """Obtenir la durée d'une vidéo en utilisant ffmpeg -i (fallback si ffprobe n'est pas disponible)."""
    cmd = [
        ffmpeg_path,
        "-i",
        str(input_path),
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        # ffmpeg -i retourne toujours un code d'erreur, mais la durée est dans stderr
        stderr_output = proc.stderr
        
        # Chercher la ligne "Duration: HH:MM:SS.xx"
        import re
        duration_match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2})\.(\d{2})", stderr_output)
        if duration_match:
            hours = int(duration_match.group(1))
            minutes = int(duration_match.group(2))
            seconds = int(duration_match.group(3))
            centiseconds = int(duration_match.group(4))
            
            total_seconds = hours * 3600 + minutes * 60 + seconds + centiseconds / 100.0
            return total_seconds
    
    return None


def _escape_drawtext_text(text: str) -> str:
    """Échapper les caractères spéciaux pour ffmpeg drawtext."""
    escaped = text.replace('\\', '\\\\')
    escaped = escaped.replace(':', '\\:')
    escaped = escaped.replace("'", "\\'")
    return escaped


def _find_default_fontfile() -> Optional[str]:
    """Essaye de trouver une police par défaut sur Windows; renvoie un chemin POSIX pour ffmpeg."""
    candidates = [
        Path("C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/ARIAL.TTF"),
        Path("C:/Windows/Fonts/segoeui.ttf"),
        Path("C:/Windows/Fonts/SegoeUI.ttf"),
    ]
    for path in candidates:
        if path.exists():
            # drawtext utilise ':' comme séparateur d'options -> échapper le ':' du lecteur Windows
            posix_path = path.as_posix().replace(":", "\\:")
            return posix_path
    return None


def _position_expressions(position: str) -> tuple[str, str]:
    """Renvoie les expressions x,y drawtext pour une position donnée."""
    if position == "tl":
        return ("20", "20")
    if position == "tr":
        return ("w-text_w-20", "20")
    if position == "tc":
        return ("(w-text_w)/2", "20")
    if position == "bl":
        return ("20", "h-text_h-20")
    if position == "br":
        return ("w-text_w-20", "h-text_h-20")
    return ("(w-text_w)/2", "(h-text_h)/2")


def overlay_text_on_video(
    input_path: Path,
    output_path: Path,
    text: str,
    *,
    fontsize: int = 54,
    fontcolor: str = "black",
    box: bool = True,
    boxcolor: str = "white@0.8",
    boxborderw: int = 14,
    position: str = "tc",
) -> None:
    """Ajoute une surimpression de texte via ffmpeg drawtext."""
    ffmpeg_path, _ = ensure_ffmpeg_in_path()

    text_escaped = _escape_drawtext_text(text)
    fontfile = _find_default_fontfile()
    x_expr, y_expr = _position_expressions(position)

    drawtext_kvs: list[str] = []
    if fontfile is not None:
        drawtext_kvs.append(f"fontfile='{fontfile}'")
    else:
        # Fallback via fontconfig; la build Windows utilisée l'active généralement
        drawtext_kvs.append("font=Arial")
    drawtext_kvs.append(f"text='{text_escaped}'")
    drawtext_kvs.append(f"fontcolor={fontcolor}")
    drawtext_kvs.append(f"fontsize={fontsize}")
    drawtext_kvs.append(f"box={'1' if box else '0'}")
    if box:
        drawtext_kvs.append(f"boxcolor={boxcolor}")
        drawtext_kvs.append(f"boxborderw={boxborderw}")
    drawtext_kvs.append(f"x={x_expr}")
    drawtext_kvs.append(f"y={y_expr}")

    filter_arg = "drawtext=" + ":".join(drawtext_kvs)

    cmd = [
        ffmpeg_path,
        "-y",
        "-i",
        str(input_path),
        "-vf",
        filter_arg,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-c:a",
        "copy",
        str(output_path),
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"ffmpeg drawtext a échoué:\n{proc.stderr}")


def _overlay_position_exprs(position: str) -> tuple[str, str]:
    """Expressions x,y pour le filtre overlay (utilise main_w/main_h et overlay_w/overlay_h)."""
    if position == "tl":
        return ("20", "20")
    if position == "tr":
        return ("main_w-overlay_w-20", "20")
    if position == "tc":
        return ("(main_w-overlay_w)/2", "20")
    if position == "bl":
        return ("20", "main_h-overlay_h-20")
    if position == "br":
        return ("main_w-overlay_w-20", "main_h-overlay_h-20")
    return ("(main_w-overlay_w)/2", "(main_h-overlay_h)/2")


def overlay_label_with_pillow(
    input_path: Path,
    output_path: Path,
    text: str,
    *,
    fontsize: int = 54,
    fontcolor: str = "black",
    bg_color: str = "white@0.8",
    padding: int = 18,
    radius: int = 24,
    position: str = "tc",
) -> None:
    """Rend un label (texte + fond arrondi) avec Pillow et l'overlay sur la vidéo via ffmpeg."""
    ffmpeg_path, _ = ensure_ffmpeg_in_path()

    try:
        from PIL import Image, ImageDraw, ImageFont
    except Exception as exc:  # pragma: no cover - pillow manquant
        raise RuntimeError("Pillow n'est pas installé. Veuillez installer 'Pillow' ou désactiver --label-rounded.") from exc

    # Chargement de la police
    font_path = _find_default_fontfile()
    try:
        if font_path is not None:
            font = ImageFont.truetype(font_path.replace("\\:", ":"), fontsize)
        else:
            font = ImageFont.load_default()
    except Exception:
        font = ImageFont.load_default()

    # Mesurer le texte
    dummy = Image.new("RGBA", (10, 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(dummy)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = max(1, bbox[2] - bbox[0])
    text_h = max(1, bbox[3] - bbox[1])
    box_w = text_w + padding * 2
    box_h = text_h + padding * 2

    # Créer l'overlay RGBA
    overlay_img = Image.new("RGBA", (box_w, box_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay_img)

    # Convertir couleurs CSS simples/#hex vers RGBA
    def _parse_color(col: str) -> tuple[int, int, int, int]:
        base = col
        alpha = None
        try:
            if '@' in col:
                base, a_str = col.split('@', 1)
                try:
                    a_float = max(0.0, min(1.0, float(a_str)))
                    alpha = int(round(a_float * 255))
                except Exception:
                    alpha = None
            if base.startswith('#') and len(base) in (4, 7, 9):
                # #RGB, #RRGGBB, #RRGGBBAA
                if len(base) == 4:
                    r = int(base[1] * 2, 16)
                    g = int(base[2] * 2, 16)
                    b = int(base[3] * 2, 16)
                    a = alpha if alpha is not None else 255
                    return (r, g, b, a)
                if len(base) == 7:
                    r = int(base[1:3], 16)
                    g = int(base[3:5], 16)
                    b = int(base[5:7], 16)
                    a = alpha if alpha is not None else 255
                    return (r, g, b, a)
                if len(base) == 9:
                    r = int(base[1:3], 16)
                    g = int(base[3:5], 16)
                    b = int(base[5:7], 16)
                    a = int(base[7:9], 16)
                    if alpha is not None:
                        a = alpha
                    return (r, g, b, a)
        except Exception:
            pass
        named = {
            "white": (255, 255, 255, 255),
            "black": (0, 0, 0, 255),
            "yellow": (255, 255, 0, 255),
            "red": (255, 0, 0, 255),
            "green": (0, 128, 0, 255),
            "blue": (0, 0, 255, 255),
        }
        rgba = named.get(base.lower(), (255, 255, 255, 255))
        if alpha is not None:
            rgba = (rgba[0], rgba[1], rgba[2], alpha)
        return rgba

    bg_rgba = _parse_color(bg_color)
    fg_rgba = _parse_color(fontcolor)

    # Arrondis
    rad = max(0, min(radius, min(box_w, box_h) // 2))
    draw.rounded_rectangle((0, 0, box_w, box_h), radius=rad, fill=bg_rgba)

    # Texte centré
    try:
        # Centrage exact via ancre (Pillow >= 8.0)
        draw.text((box_w / 2, box_h / 2), text, font=font, fill=fg_rgba, anchor="mm")
    except Exception:
        # Fallback: centrage via bbox
        text_x = (box_w - text_w) // 2
        text_y = (box_h - text_h) // 2
        draw.text((text_x, text_y), text, font=font, fill=fg_rgba)

    # Sauvegarder l'overlay temporaire
    overlay_path = output_path.with_name(f"label_{uuid4().hex}.png")
    overlay_img.save(overlay_path.as_posix())

    # Position overlay
    x_expr, y_expr = _overlay_position_exprs(position)
    filter_arg = f"overlay=x={x_expr}:y={y_expr}"

    cmd = [
        ffmpeg_path,
        "-y",
        "-i",
        str(input_path),
        "-i",
        str(overlay_path),
        "-filter_complex",
        filter_arg,
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "20",
        "-c:a",
        "copy",
        str(output_path),
    ]
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"ffmpeg overlay a échoué:\n{proc.stderr}")
    finally:
        try:
            if overlay_path.exists():
                overlay_path.unlink()
        except Exception:
            pass


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="ytb-to-tiktok",
        description="Télécharger une vidéo YouTube et la découper en segments de 60 secondes.",
    )
    parser.add_argument("url", help="URL de la vidéo YouTube")
    parser.add_argument("--output", "-o", type=Path, default=Path("outputs"), help="Dossier de sortie pour la vidéo et les segments")
    parser.add_argument("--segments-dir", type=Path, default=None, help="Dossier des segments (défaut: <output>/segments)")
    parser.add_argument("--limit", type=int, default=None, help="Limiter le nombre de segments produits")
    parser.add_argument("--segment-seconds", type=int, default=60, help="Durée d'un segment en secondes (défaut: 60)")
    parser.add_argument("--cookies", type=Path, default=None, help="Fichier cookies (format Netscape)")
    parser.add_argument(
        "--cookies-from-browser",
        choices=["chrome", "edge", "firefox", "brave", "chromium", "opera", "vivaldi"],
        default=None,
        help="Importer automatiquement les cookies depuis un navigateur",
    )
    parser.add_argument("--user-agent", default=None, help="User-Agent HTTP personnalisé")
    parser.add_argument("--proxy", default=None, help="Proxy HTTP/HTTPS, ex: http://127.0.0.1:8080")

    # Options de surimpression "Partie X" (drawtext)
    parser.add_argument("--label", action="store_true", help="Ajouter une surimpression de texte 'Partie X' (fond rectangulaire)")
    parser.add_argument("--label-template", default="Partie {i}", help="Modèle de texte. Variables: {i} (index 1..N), {n} (alias), {total} (N)")
    parser.add_argument("--label-fontsize", type=int, default=54, help="Taille de police (px)")
    parser.add_argument("--label-color", default="black", help="Couleur du texte (ex: white, black, yellow, #RRGGBB)")
    parser.add_argument("--label-position", choices=["tl", "tr", "tc", "bl", "br", "center"], default="tc", help="Position du texte")
    parser.add_argument("--label-boxcolor", default="white", help="Couleur de fond de la boîte (rectangulaire)")
    parser.add_argument("--label-boxborderw", type=int, default=14, help="Épaisseur de la boîte autour du texte")

    # Variante arrondie (génère une image RGBA via Pillow puis overlay)
    parser.add_argument("--label-rounded", action="store_true", help="Utiliser un fond aux coins arrondis (nécessite Pillow)")
    parser.add_argument("--label-radius", type=int, default=24, help="Rayon d'arrondi (pixels) pour --label-rounded")
    parser.add_argument("--label-padding", type=int, default=18, help="Padding interne (pixels) pour --label-rounded")
    parser.add_argument("--label-box", dest="label_box", action="store_true", help="Afficher une boîte semi-transparente derrière le texte")
    parser.add_argument("--no-label-box", dest="label_box", action="store_false", help="Ne pas afficher de boîte derrière le texte")
    parser.set_defaults(label_box=True)
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)

    output_dir: Path = args.output
    segments_root: Path = args.segments_dir or (output_dir / "segments")
    downloads_dir: Path = output_dir / "downloads"

    console.rule("ytb-to-tiktok")
    console.print("[bold]1) Téléchargement de la vidéo YouTube[/]")
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TimeElapsedColumn(),
        transient=True,
        console=console,
    ) as progress:
        task = progress.add_task("Téléchargement en cours...", total=None)
        result = download_youtube(
            args.url,
            downloads_dir,
            cookies_file=args.cookies,
            cookies_from_browser=args.cookies_from_browser,
            user_agent=args.user_agent,
            proxy=args.proxy,
        )
        progress.update(task, completed=1)

    console.print(f"[green]OK[/] Téléchargé: [italic]{result.video_path.name}[/]")

    console.print("[bold]2) Découpage en segments[/]")
    parts = split_video_ffmpeg(result.video_path, segments_root, segment_seconds=args.segment_seconds, limit=args.limit)
    console.print(f"[green]OK[/] {len(parts)} segment(s) créé(s) dans {segments_root}")

    if args.label and parts:
        console.print("[bold]3) Ajout de la surimpression 'Partie X'[/]")
        total = len(parts)
        for index, part in enumerate(parts, start=1):
            label_text = args.label_template.format(i=index, n=index, total=total)
            tmp_out = part.with_name(part.stem + "_labeled" + part.suffix)
            if args.label_rounded:
                overlay_label_with_pillow(
                    part,
                    tmp_out,
                    label_text,
                    fontsize=args.label_fontsize,
                    fontcolor=args.label_color,
                    bg_color=args.label_boxcolor,
                    padding=args.label_padding,
                    radius=args.label_radius,
                    position=args.label_position,
                )
            else:
                overlay_text_on_video(
                    part,
                    tmp_out,
                    label_text,
                    fontsize=args.label_fontsize,
                    fontcolor=args.label_color,
                    box=args.label_box,
                    boxcolor=args.label_boxcolor,
                    boxborderw=args.label_boxborderw,
                    position=args.label_position,
                )
            try:
                os.replace(tmp_out, part)
            except Exception:
                try:
                    if part.exists():
                        part.unlink()
                finally:
                    os.replace(tmp_out, part)
        console.print(f"[green]OK[/] Surimpression ajoutée sur {total} segment(s)")

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())


