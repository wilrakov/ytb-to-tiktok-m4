#!/usr/bin/env python3
"""
Configuration centralisée pour la construction de l'exécutable
YouTube to TikTok
"""

import os
from pathlib import Path

# Configuration de l'application
APP_NAME = "YouTube-to-TikTok"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Convertisseur de vidéos YouTube en segments TikTok"
APP_AUTHOR = "Votre Nom"
APP_AUTHOR_EMAIL = "votre.email@example.com"
APP_URL = "https://github.com/votre-username/ytb-to-tiktok"
APP_LICENSE = "MIT"

# Configuration PyInstaller
PYINSTALLER_CONFIG = {
    "script": "gui.py",
    "name": APP_NAME,
    "onefile": True,
    "console": False,
    "icon": "icon.ico",
    "version_file": "version.txt",
    "distpath": "dist",
    "workpath": "build",
    "specpath": ".",
    "clean": True,
    "noconfirm": True,
    "upx": True,
    "upx_exclude": [],
    "debug": False,
    "strip": False,
    "noupx": False,
    "uac_admin": False,
    "uac_uiaccess": False,
    "win_private_assemblies": False,
    "win_no_prefer_redirects": False,
    "bootloader_ignore_signals": False,
    "disable_windowed_traceback": False,
    "argv_emulation": False,
    "target_arch": None,
    "codesign_identity": None,
    "entitlements_file": None,
}

# Fichiers à inclure dans l'exécutable
INCLUDED_FILES = [
    ("config.example.ini", "."),
    ("README.md", "."),
    ("LICENSE", "."),
    ("README_BUILD.md", "."),
]

# Modules cachés à inclure
HIDDEN_IMPORTS = [
    "ytb_to_tiktok.cli",
    "ytb_to_tiktok.__main__",
    "PIL",
    "PIL._tkinter_finder",
    "tkinter",
    "tkinter.ttk",
    "tkinter.filedialog",
    "tkinter.messagebox",
    "tkinter.scrolledtext",
    "yt_dlp",
    "rich",
    "imageio_ffmpeg",
    "imageio",
    "numpy",
    "requests",
    "urllib3",
    "certifi",
    "charset_normalizer",
    "idna",
    "websockets",
    "brotli",
    "certifi",
    "cryptography",
    "mutagen",
    "pycryptodome",
]

# Modules à exclure (optionnel)
EXCLUDED_MODULES = [
    "matplotlib",
    "scipy",
    "pandas",
    "jupyter",
    "IPython",
    "notebook",
    "pytest",
    "unittest",
    "doctest",
    "test",
    "tests",
]

# Configuration Inno Setup
INNO_SETUP_CONFIG = {
    "app_name": "YouTube to TikTok",
    "app_version": APP_VERSION,
    "app_publisher": "Votre Entreprise",
    "app_publisher_url": APP_URL,
    "app_support_url": f"{APP_URL}/issues",
    "app_updates_url": f"{APP_URL}/releases",
    "default_dir_name": "{autopf}\\YouTube to TikTok",
    "default_group_name": "YouTube to TikTok",
    "allow_no_icons": True,
    "license_file": "LICENSE",
    "output_dir": "installer",
    "output_base_filename": f"{APP_NAME}-Setup",
    "setup_icon_file": "icon.ico",
    "compression": "lzma",
    "solid_compression": True,
    "wizard_style": "modern",
    "privileges_required": "lowest",
    "languages": ["french"],
    "tasks": ["desktopicon"],
    "run_postinstall": True,
}

# Configuration de l'icône
ICON_CONFIG = {
    "size": (256, 256),
    "background_color": (0, 0, 0, 0),  # Transparent
    "youtube_color": (255, 0, 0, 255),  # Rouge YouTube
    "tiktok_color": (0, 0, 0, 255),     # Noir TikTok
    "accent_color": (255, 255, 255, 255), # Blanc
}

# Configuration de version Windows
VERSION_CONFIG = {
    "file_version": (1, 0, 0, 0),
    "product_version": (1, 0, 0, 0),
    "company_name": "Votre Entreprise",
    "file_description": "Convertisseur YouTube vers TikTok",
    "internal_name": "ytb-to-tiktok",
    "legal_copyright": f"Copyright © 2024 {APP_AUTHOR}",
    "original_filename": f"{APP_NAME}.exe",
    "product_name": "YouTube to TikTok",
    "product_version_str": APP_VERSION,
}

# Chemins des dossiers
PATHS = {
    "dist": Path("dist"),
    "build": Path("build"),
    "installer": Path("installer"),
    "outputs": Path("outputs"),
    "temp": Path("temp"),
}

# Configuration de nettoyage
CLEANUP_PATTERNS = [
    "build",
    "dist",
    "__pycache__",
    "*.spec",
    "*.log",
    "temp",
]

# Configuration de test
TEST_CONFIG = {
    "test_exe": True,
    "test_installer": True,
    "cleanup_after_test": True,
    "timeout_seconds": 30,
}

# Configuration de distribution
DISTRIBUTION_CONFIG = {
    "create_zip": True,
    "zip_name": f"{APP_NAME}-{APP_VERSION}-Windows.zip",
    "include_installer": True,
    "include_portable": True,
    "create_checksums": True,
    "checksum_algorithms": ["md5", "sha256"],
}

def get_pyinstaller_args():
    """Retourne les arguments PyInstaller formatés"""
    args = [
        "--onefile" if PYINSTALLER_CONFIG["onefile"] else "--onedir",
        "--windowed" if not PYINSTALLER_CONFIG["console"] else "--console",
        "--name", PYINSTALLER_CONFIG["name"],
        "--distpath", str(PYINSTALLER_CONFIG["distpath"]),
        "--workpath", str(PYINSTALLER_CONFIG["workpath"]),
        "--specpath", str(PYINSTALLER_CONFIG["specpath"]),
    ]
    
    if PYINSTALLER_CONFIG["icon"]:
        args.extend(["--icon", PYINSTALLER_CONFIG["icon"]])
    
    if PYINSTALLER_CONFIG["version_file"]:
        args.extend(["--version-file", PYINSTALLER_CONFIG["version_file"]])
    
    if PYINSTALLER_CONFIG["clean"]:
        args.append("--clean")
    
    if PYINSTALLER_CONFIG["noconfirm"]:
        args.append("--noconfirm")
    
    if PYINSTALLER_CONFIG["upx"]:
        args.append("--upx-dir")
    
    # Ajouter les fichiers inclus
    for src, dst in INCLUDED_FILES:
        args.extend(["--add-data", f"{src}{os.pathsep}{dst}"])
    
    # Ajouter les imports cachés
    for module in HIDDEN_IMPORTS:
        args.extend(["--hidden-import", module])
    
    # Ajouter les modules exclus
    for module in EXCLUDED_MODULES:
        args.extend(["--exclude-module", module])
    
    return args

def create_directories():
    """Crée les dossiers nécessaires"""
    for path in PATHS.values():
        path.mkdir(exist_ok=True)

def cleanup_build_files():
    """Nettoie les fichiers de construction"""
    import shutil
    
    for pattern in CLEANUP_PATTERNS:
        if Path(pattern).exists():
            if Path(pattern).is_dir():
                shutil.rmtree(pattern)
            else:
                Path(pattern).unlink()

if __name__ == "__main__":
    # Test de la configuration
    print(f"Configuration pour {APP_NAME} v{APP_VERSION}")
    print(f"Arguments PyInstaller: {' '.join(get_pyinstaller_args())}")
    
    # Créer les dossiers
    create_directories()
    print("✓ Dossiers créés")
    
    # Afficher la configuration
    print(f"\nConfiguration PyInstaller:")
    for key, value in PYINSTALLER_CONFIG.items():
        print(f"  {key}: {value}")
    
    print(f"\nFichiers inclus: {len(INCLUDED_FILES)}")
    print(f"Imports cachés: {len(HIDDEN_IMPORTS)}")
    print(f"Modules exclus: {len(EXCLUDED_MODULES)}")
