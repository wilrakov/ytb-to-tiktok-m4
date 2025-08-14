# ytb-to-tiktok

Python CLI application to:
- Download a YouTube video
- Split it into 60-second segments (or a custom duration)

## Prerequisites
- Python 3.10+ (Windows compatible)
- Internet connection

No manual ffmpeg installation required: it is provided via `imageio-ffmpeg` and automatically added to PATH at runtime.

## Installation
```powershell
# From the project directory
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Usage
Two options:

1) As a module (recommended):
```powershell
python -m ytb_to_tiktok "https://www.youtube.com/watch?v=XXXXXXXXXXX" -o outputs --segment-seconds 60
```

2) By calling the script directly:
```powershell
python ytb-to-tiktok/ytb_to_tiktok/cli.py "https://www.youtube.com/watch?v=XXXXXXXXXXX" -o outputs --segment-seconds 60
```

Main arguments:
- url (positional): YouTube video URL
- --output / -o: output directory (default: outputs)
- --segments-dir: directory for segments (default: outputs/segments)
- --segment-seconds: segment duration in seconds (default: 60)
- --limit: limit the number of generated segments
- --cookies: path to a cookies file (Netscape format)
- --cookies-from-browser: auto-import cookies from a browser (chrome, edge, firefox, brave, chromium, opera, vivaldi)
- --user-agent: custom HTTP User-Agent
- --proxy: HTTP/HTTPS proxy, e.g. `http://127.0.0.1:8080`

Examples:
```powershell
# Standard 60s split
python -m ytb_to_tiktok "https://youtu.be/XXXXXXXXXXX" -o outputs

# Split into 45s and keep only the first 5 segments
python -m ytb_to_tiktok "https://youtu.be/XXXXXXXXXXX" -o outputs --segment-seconds 45 --limit 5

# Use cookies (YouTube may require verification)
# 1) From Chrome (default profile):
python -m ytb_to_tiktok "https://youtu.be/XXXXXXXXXXX" -o outputs --cookies-from-browser chrome

# 2) From an exported Netscape cookies file
python -m ytb_to_tiktok "https://youtu.be/XXXXXXXXXXX" -o outputs --cookies .\cookies.txt
```

## Outputs
- The downloaded video is saved to: outputs/downloads
- Segments are generated in: outputs/segments
- Segment naming: <title>_0001.mp4, <title>_0002.mp4, ...

## Technical notes
- Downloading uses yt-dlp with mp4 format when possible.
- Splitting first attempts a fast "stream copy". If ffmpeg fails, it falls back to re-encoding in h264/aac, forcing keyframes to guarantee exact segment durations.

## Option: "Part X" overlay
Add a label on each segment via `ffmpeg drawtext`.

Example:
```powershell
python -m ytb_to_tiktok "https://youtu.be/XXXXXXXXXXX" -o outputs --segment-seconds 60 --label --label-template "Part {i}" --label-position br --label-fontsize 54 --label-color white
```

Available options:
- `--label`: enable the overlay
- `--label-template`: text template. Variables: `{i}` (index 1..N), `{n}` (alias), `{total}` (N)
- `--label-fontsize`: size in pixels (default: 54)
- `--label-color`: color (e.g., white, black, yellow, `#RRGGBB`)
- `--label-position`: `tl` | `tr` | `bl` | `br` | `center` (default: `br`)
- `--label-box` / `--no-label-box`: enable/disable a box behind the text (default: enabled)

## Legal
Respect YouTube's Terms of Service and copyrights. This application is provided for educational purposes.