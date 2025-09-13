# ytb-to-tiktok (ENGLISH)

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

- vidéo exemple = https://www.youtube.com/watch?v=A1MY_8EUois&pp=ygUVd2FyIHRodW5kZXIgc3Bvb2tzdG9u

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


# ytb-to-tiktok (FRENCH)

Un outil Python pour télécharger des vidéos YouTube et les découper automatiquement en segments de durée configurable, optimisé pour TikTok et autres plateformes de réseaux sociaux.

## 🚀 Fonctionnalités

- **Téléchargement YouTube** : Télécharge des vidéos YouTube avec support des cookies pour accéder au contenu restreint
- **Découpage automatique** : Découpe automatiquement les vidéos en segments de durée configurable
- **Support des cookies** : Import automatique depuis les navigateurs ou utilisation de fichiers cookies
- **Surimpression de texte** : Ajout optionnel de labels "Partie X" sur chaque segment
- **Format optimisé** : Export en MP4 avec codec H.264 pour une compatibilité maximale
- **Interface riche** : Interface console moderne avec barres de progression
- **Interface graphique** : Interface graphique moderne et intuitive (nouveau !)

## 📋 Prérequis

- Python 3.8+
- Connexion Internet
- Fichier cookies YouTube (optionnel, pour le contenu restreint)

## 🛠️ Installation

1. **Cloner le repository** :
```bash
git clone <votre-repo>
cd ytb-to-tiktok
```

2. **Installer les dépendances** :
```bash
pip install -r requirements.txt
```

## 📖 Utilisation

### 🖥️ Interface graphique (Recommandé)

Pour une utilisation facile et intuitive, lancez l'interface graphique :

**Ligne de commande** :
```bash
python launch_gui.py
```

L'interface graphique offre :
- Configuration visuelle de tous les paramètres
- Sélecteurs de dossiers intégrés
- Suivi en temps réel du processus
- Logs détaillés et colorés
- Gestion des erreurs intuitive

### 💻 Interface en ligne de commande

#### Commande de base

```bash
python -m ytb_to_tiktok "URL_YOUTUBE" [options]
```

### Exemples d'utilisation

**Découpage simple en segments de 60 secondes** :
```bash
python -m ytb_to_tiktok "https://www.youtube.com/watch?v=VIDEO_ID" -o outputs
```

**Découpage en segments de 90 secondes** :
```bash
python -m ytb_to_tiktok "https://www.youtube.com/watch?v=VIDEO_ID" -o outputs --segment-seconds 90
```

**Avec fichier cookies pour contenu restreint** :
```bash
python -m ytb_to_tiktok "https://www.youtube.com/watch?v=VIDEO_ID" -o outputs --cookies cookies.txt
```

**Avec surimpression de texte "Partie X"** :
```bash
python -m ytb_to_tiktok "https://www.youtube.com/watch?v=VIDEO_ID" -o outputs --label
```

**Limiter le nombre de segments** :
```bash
python -m ytb_to_tiktok "https://www.youtube.com/watch?v=VIDEO_ID" -o outputs --limit 5
```

### Options disponibles

| Option | Description | Défaut |
|--------|-------------|---------|
| `--output, -o` | Dossier de sortie | `outputs` |
| `--segment-seconds` | Durée d'un segment en secondes | `60` |
| `--cookies` | Fichier cookies Netscape | Aucun |
| `--cookies-from-browser` | Importer depuis un navigateur | Aucun |
| `--limit` | Limiter le nombre de segments | Aucune limite |
| `--label` | Ajouter surimpression "Partie X" | Désactivé |
| `--label-template` | Modèle de texte | `"Partie {i}"` |
| `--label-position` | Position du texte | `tc` (top-center) |
| `--user-agent` | User-Agent personnalisé | Défaut |
| `--proxy` | Proxy HTTP/HTTPS | Aucun |

### Positions de texte disponibles

- `tl` : Top-left (haut-gauche)
- `tc` : Top-center (haut-centre) 
- `tr` : Top-right (haut-droite)
- `bl` : Bottom-left (bas-gauche)
- `br` : Bottom-right (bas-droite)
- `center` : Centre de la vidéo

## 📁 Structure des fichiers de sortie

```
outputs/
├── downloads/           # Vidéos téléchargées
│   └── video.mp4
└── segments/            # Segments découpés
    ├── video_0000.mp4
    ├── video_0001.mp4
    ├── video_0002.mp4
    └── ...
```

## 🆕 Interface graphique

Une interface graphique moderne est maintenant disponible ! Elle offre une expérience utilisateur intuitive avec :

- **3 onglets organisés** : Configuration, Options avancées, Logs
- **Validation automatique** : Vérification des paramètres en temps réel
- **Gestion des erreurs** : Messages clairs et suggestions de résolution
- **Interface responsive** : Adaptation automatique à toutes les résolutions
- **Raccourcis clavier** : Ctrl+Enter pour démarrer, Ctrl+Q pour quitter

### 📋 Documentation complète

Consultez `README_GUI.md` pour une documentation détaillée de l'interface graphique. \
Consultez `README_BUILD.md` pour une explication complète sur les étapes nécessaires à la création d'un exécutable Windows autonome pour l'application **YouTube to TikTok**. 

## 🔧 Configuration des cookies

### Méthode 1 : Fichier cookies

1. Installez l'extension "Get cookies.txt" dans votre navigateur
2. Allez sur YouTube et connectez-vous
3. Utilisez l'extension pour exporter les cookies
4. Utilisez le fichier avec l'option `--cookies`

### Méthode 2 : Import automatique

```bash
python -m ytb_to_tiktok "URL" --cookies-from-browser chrome
```

Navigateurs supportés : `chrome`, `edge`, `firefox`, `brave`, `chromium`, `opera`, `vivaldi`

## 🎯 Cas d'usage

- **TikTok** : Segments de 15-60 secondes
- **Instagram Reels** : Segments de 15-90 secondes  
- **YouTube Shorts** : Segments de 15-60 secondes
- **Twitter/X** : Segments de 2-3 minutes
- **LinkedIn** : Segments de 1-10 minutes

## 🐛 Résolution des problèmes

### Erreur "ffmpeg not found"
- Le script utilise automatiquement `imageio-ffmpeg` inclus
- Si le problème persiste, installez ffmpeg manuellement

### Erreur "No module named 'rich'"
- Installez les dépendances : `pip install -r requirements.txt`

### Vidéo non téléchargée
- Vérifiez que l'URL est valide
- Utilisez l'option `--cookies` pour le contenu restreint
- Vérifiez votre connexion Internet

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## 📞 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.
