# ytb-to-tiktok

Application CLI Python pour:
- Télécharger une vidéo YouTube
- La découper en segments de 60 secondes (ou durée personnalisée)

## Prérequis
- Python 3.10+ (Windows compatible)
- Connexion Internet

Aucun ffmpeg à installer manuellement: il est fourni via `imageio-ffmpeg` et ajouté automatiquement au PATH au runtime.

## Installation
```powershell
# Dans le répertoire du projet
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Utilisation
Deux options:

1) En tant que module (recommandé):
```powershell
python -m ytb_to_tiktok "https://www.youtube.com/watch?v=XXXXXXXXXXX" -o outputs --segment-seconds 60
```

2) En appelant le script directement:
```powershell
python ytb-to-tiktok/ytb_to_tiktok/cli.py "https://www.youtube.com/watch?v=XXXXXXXXXXX" -o outputs --segment-seconds 60
```

Arguments principaux:
- url (positionnel): URL de la vidéo YouTube
- --output / -o: dossier de sortie (défaut: outputs)
- --segments-dir: dossier des segments (défaut: outputs/segments)
- --segment-seconds: durée d’un segment en secondes (défaut: 60)
- --limit: limite le nombre de segments générés
 - --limit: limite le nombre de segments générés
 - --cookies: chemin vers un fichier cookies (format Netscape)
 - --cookies-from-browser: import auto des cookies depuis un navigateur (chrome, edge, firefox, brave, chromium, opera, vivaldi)
 - --user-agent: User-Agent HTTP personnalisé
 - --proxy: proxy HTTP/HTTPS, ex `http://127.0.0.1:8080`

Exemples:
```powershell
# Découpe standard 60s
python -m ytb_to_tiktok "https://youtu.be/XXXXXXXXXXX" -o outputs

# Découpe en 45s et ne garder que les 5 premiers segments
python -m ytb_to_tiktok "https://youtu.be/XXXXXXXXXXX" -o outputs --segment-seconds 45 --limit 5

# Utiliser les cookies (YouTube peut demander de confirmer que vous n'êtes pas un robot)
# 1) Depuis Chrome (profil par défaut):
python -m ytb_to_tiktok "https://youtu.be/XXXXXXXXXXX" -o outputs --cookies-from-browser chrome

# 2) Depuis un fichier cookies Netscape exporté
python -m ytb_to_tiktok "https://youtu.be/XXXXXXXXXXX" -o outputs --cookies .\cookies.txt
```

## Sorties
- La vidéo téléchargée est placée dans: outputs/downloads
- Les segments sont générés dans: outputs/segments
- Nom des segments: <titre>_0001.mp4, <titre>_0002.mp4, ...

## Notes techniques
- Le téléchargement utilise yt-dlp au format mp4 quand possible.
- Le découpage tente d’abord un « stream copy » (rapide). Si ffmpeg échoue, re-encodage en h264/aac avec forçage de keyframes pour garantir la durée exacte des segments.

## Option: Surimpression "Partie X"
Ajoutez un libellé sur chaque segment via `ffmpeg drawtext`.

Exemple:
```powershell
python -m ytb_to_tiktok "https://youtu.be/XXXXXXXXXXX" -o outputs --segment-seconds 60 --label --label-template "Partie {i}" --label-position br --label-fontsize 54 --label-color white
```

Options disponibles:
- `--label`: active la surimpression
- `--label-template`: modèle de texte. Variables: `{i}` (index 1..N), `{n}` (alias), `{total}` (N)
- `--label-fontsize`: taille en pixels (défaut: 54)
- `--label-color`: couleur (ex: white, black, yellow, `#RRGGBB`)
- `--label-position`: `tl` | `tr` | `bl` | `br` | `center` (défaut: `br`)
- `--label-box` / `--no-label-box`: activer/désactiver la boîte derrière le texte (défaut: activée)

## Légal
Respectez les conditions d’utilisation de YouTube et les droits d’auteur. Cette application est fournie à des fins éducatives.
