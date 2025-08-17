#!/usr/bin/env python3
"""
Script de construction d'exécutable avec PyInstaller
Crée un exécutable Windows autonome de l'application GUI
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import argparse

def check_dependencies():
    """Vérifie que toutes les dépendances sont installées"""
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} trouvé")
    except ImportError:
        print("✗ PyInstaller non trouvé. Installation...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    try:
        import PIL
        print(f"✓ Pillow {PIL.__version__} trouvé")
    except ImportError:
        print("✗ Pillow non trouvé. Installation...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])

def create_spec_file():
    """Crée le fichier .spec pour PyInstaller"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Fichiers et dossiers à inclure
added_files = [
    ('config.example.ini', '.'),
    ('README.md', '.'),
    ('LICENSE', '.'),
]

# Configuration de l'exécutable
a = Analysis(
    ['gui.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'ytb_to_tiktok.cli',
        'ytb_to_tiktok.__main__',
        'PIL',
        'PIL._tkinter_finder',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.scrolledtext',
        'yt_dlp',
        'rich',
        'imageio_ffmpeg',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Configuration de l'exécutable
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='YouTube-to-TikTok',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Application GUI sans console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',  # Icône de l'application
    version='version.txt',  # Informations de version
    uac_admin=False,
    uac_uiaccess=False,
)
'''
    
    with open('YouTube-to-TikTok.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✓ Fichier .spec créé")

def create_version_file():
    """Crée le fichier de version pour Windows"""
    version_content = '''# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
    # Set not needed items to 0 0.
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    # Contains a bitmask that specifies the valid bits 'flags'r
    mask=0x3f,
    # Contains a bitmask that specifies the Boolean attributes of the file.
    flags=0x0,
    # The operating system for which this file was designed.
    # 0x4 - NT and there is no need to change it.
    OS=0x40004,
    # The general type of file.
    # 0x1 - the file is an application.
    fileType=0x1,
    # The function of the file.
    # 0x0 - the function is not defined for this fileType
    subtype=0x0,
    # Creation date and time stamp.
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Votre Entreprise'),
        StringStruct(u'FileDescription', u'Convertisseur YouTube vers TikTok'),
        StringStruct(u'FileVersion', u'1.0.0'),
        StringStruct(u'InternalName', u'ytb-to-tiktok'),
        StringStruct(u'LegalCopyright', u'Copyright © 2024 Votre Nom'),
        StringStruct(u'OriginalFilename', u'YouTube-to-TikTok.exe'),
        StringStruct(u'ProductName', u'YouTube to TikTok'),
        StringStruct(u'ProductVersion', u'1.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
    
    with open('version.txt', 'w', encoding='utf-8') as f:
        f.write(version_content)
    
    print("✓ Fichier de version créé")

def create_icon():
    """Crée une icône simple si elle n'existe pas"""
    if not Path('icon.ico').exists():
        try:
            from PIL import Image, ImageDraw
            
            # Créer une image 256x256
            img = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # Dessiner un cercle avec les couleurs YouTube/TikTok
            draw.ellipse([20, 20, 236, 236], fill=(255, 0, 0, 255))  # Rouge YouTube
            draw.ellipse([60, 60, 196, 196], fill=(0, 0, 0, 255))    # Noir TikTok
            draw.ellipse([80, 80, 176, 176], fill=(255, 0, 0, 255))  # Rouge YouTube
            
            # Sauvegarder en ICO
            img.save('icon.ico', format='ICO')
            print("✓ Icône créée")
        except Exception as e:
            print(f"⚠ Impossible de créer l'icône: {e}")
            print("  Vous pouvez ajouter manuellement un fichier icon.ico")

def build_executable():
    """Construit l'exécutable avec PyInstaller"""
    print("🔨 Construction de l'exécutable...")
    
    # Nettoyer les anciens builds
    for dir_name in ['build', 'dist', '__pycache__']:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"✓ Dossier {dir_name} nettoyé")
    
    # Construire avec PyInstaller
    try:
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            "YouTube-to-TikTok.spec"
        ]
        
        print(f"Commande: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✓ Construction réussie!")
        print(f"Sortie: {result.stdout}")
        
        # Vérifier que l'exécutable a été créé
        exe_path = Path("dist/YouTube-to-TikTok.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"✓ Exécutable créé: {exe_path}")
            print(f"  Taille: {size_mb:.1f} MB")
        else:
            print("✗ Exécutable non trouvé!")
            
    except subprocess.CalledProcessError as e:
        print(f"✗ Erreur lors de la construction: {e}")
        print(f"Sortie d'erreur: {e.stderr}")
        return False
    
    return True

def create_installer_script():
    """Crée un script pour Inno Setup"""
    inno_content = '''[Setup]
AppName=YouTube to TikTok
AppVersion=1.0.0
AppPublisher=Votre Entreprise
AppPublisherURL=https://github.com/votre-username/ytb-to-tiktok
AppSupportURL=https://github.com/votre-username/ytb-to-tiktok/issues
AppUpdatesURL=https://github.com/votre-username/ytb-to-tiktok/releases
DefaultDirName={autopf}\\YouTube to TikTok
DefaultGroupName=YouTube to TikTok
AllowNoIcons=yes
LicenseFile=LICENSE
OutputDir=installer
OutputBaseFilename=YouTube-to-TikTok-Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest

[Languages]
Name: "french"; MessagesFile: "compiler:Languages\\French.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "dist\\YouTube-to-TikTok.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.example.ini"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\YouTube to TikTok"; Filename: "{app}\\YouTube-to-TikTok.exe"
Name: "{group}\\{cm:UninstallProgram,YouTube to TikTok}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\\YouTube to TikTok"; Filename: "{app}\\YouTube-to-TikTok.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\\YouTube-to-TikTok.exe"; Description: "{cm:LaunchProgram,YouTube to TikTok}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
end;
'''
    
    with open('installer.iss', 'w', encoding='utf-8') as f:
        f.write(inno_content)
    
    print("✓ Script Inno Setup créé")

def main():
    """Fonction principale"""
    parser = argparse.ArgumentParser(description="Construction de l'exécutable YouTube to TikTok")
    parser.add_argument("--clean", action="store_true", help="Nettoyer avant construction")
    parser.add_argument("--installer", action="store_true", help="Créer aussi le script d'installateur")
    parser.add_argument("--no-icon", action="store_true", help="Ne pas créer d'icône")
    
    args = parser.parse_args()
    
    print("🚀 Démarrage de la construction de l'exécutable YouTube to TikTok")
    print("=" * 60)
    
    # Vérifier les dépendances
    check_dependencies()
    
    # Nettoyer si demandé
    if args.clean:
        for dir_name in ['build', 'dist', '__pycache__']:
            if Path(dir_name).exists():
                shutil.rmtree(dir_name)
                print(f"✓ Dossier {dir_name} nettoyé")
    
    # Créer les fichiers nécessaires
    create_spec_file()
    create_version_file()
    
    if not args.no_icon:
        create_icon()
    
    if args.installer:
        create_installer_script()
    
    # Construire l'exécutable
    if build_executable():
        print("\n🎉 Construction terminée avec succès!")
        print("\nFichiers créés:")
        print("  - dist/YouTube-to-TikTok.exe (exécutable principal)")
        print("  - YouTube-to-TikTok.spec (configuration PyInstaller)")
        print("  - version.txt (informations de version)")
        
        if not args.no_icon:
            print("  - icon.ico (icône de l'application)")
        
        if args.installer:
            print("  - installer.iss (script Inno Setup)")
            print("\nPour créer l'installateur, installez Inno Setup et exécutez:")
            print("  iscc installer.iss")
        
        print("\nL'application est prête à être distribuée!")
    else:
        print("\n❌ Échec de la construction")
        sys.exit(1)

if __name__ == "__main__":
    main()
