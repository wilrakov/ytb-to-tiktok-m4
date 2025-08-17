# Guide de Construction - YouTube to TikTok

Ce guide explique comment construire un exécutable Windows autonome et un installateur pour l'application YouTube to TikTok.

## 🚀 Démarrage Rapide

### Option 1: Scripts automatiques (Recommandé)

#### Construction de l'exécutable uniquement
```batch
# Double-cliquez sur ce fichier
build_exe.bat
```

#### Construction complète avec installateur
```batch
# Double-cliquez sur ce fichier
build_installer.bat
```

### Option 2: Scripts PowerShell
```powershell
# Construction simple
.\build_exe.ps1

# Construction avec nettoyage
.\build_exe.ps1 -Clean

# Construction avec installateur
.\build_exe.ps1 -Installer

# Afficher l'aide
.\build_exe.ps1 -Help
```

### Option 3: Script Python direct
```bash
# Construction simple
python build_exe.py

# Construction avec nettoyage
python build_exe.py --clean

# Construction avec installateur
python build_exe.py --clean --installer
```

## 📋 Prérequis

### 1. Python 3.8+
- Téléchargez depuis [python.org](https://python.org)
- Assurez-vous que Python est dans le PATH système
- Vérifiez avec: `python --version`

### 2. Dépendances Python
```bash
# Installer les dépendances de construction
pip install -r requirements-build.txt

# Ou installer manuellement
pip install pyinstaller auto-py-to-exe
```

### 3. Inno Setup (pour l'installateur)
- Téléchargez depuis [jrsoftware.org](https://jrsoftware.org/isdl.php)
- Installez avec les options par défaut
- Assurez-vous que `iscc` est dans le PATH

## 🔧 Configuration

### Fichiers de configuration créés automatiquement

- **`YouTube-to-TikTok.spec`** - Configuration PyInstaller
- **`version.txt`** - Informations de version Windows
- **`icon.ico`** - Icône de l'application (créée automatiquement)
- **`installer.iss`** - Script Inno Setup

### Personnalisation

#### Modifier l'icône
Remplacez `icon.ico` par votre propre icône au format ICO (256x256 recommandé).

#### Modifier les informations de version
Éditez `version.txt` pour changer:
- Nom de l'entreprise
- Description du fichier
- Copyright
- Version

#### Modifier l'installateur
Éditez `installer.iss` pour personnaliser:
- Nom de l'application
- Informations de l'éditeur
- Options d'installation
- Raccourcis créés

## 🏗️ Processus de Construction

### 1. Vérification des dépendances
- Python et pip
- PyInstaller
- Pillow (pour l'icône)
- Inno Setup (optionnel)

### 2. Création des fichiers de configuration
- Fichier .spec PyInstaller
- Fichier de version Windows
- Icône de l'application
- Script Inno Setup

### 3. Construction de l'exécutable
- Analyse des dépendances
- Empaquetage avec PyInstaller
- Optimisation et compression
- Création du fichier .exe

### 4. Construction de l'installateur (optionnel)
- Compilation avec Inno Setup
- Création du fichier .exe d'installation
- Configuration des raccourcis et désinstallation

## 📁 Structure des fichiers de sortie

```
dist/
├── YouTube-to-TikTok.exe          # Exécutable principal
└── _internal/                     # Bibliothèques empaquetées

installer/
└── YouTube-to-TikTok-Setup.exe    # Installateur Windows

# Fichiers de configuration
YouTube-to-TikTok.spec             # Configuration PyInstaller
version.txt                        # Informations de version
icon.ico                          # Icône de l'application
installer.iss                     # Script Inno Setup
```

## 🎯 Options de Construction

### PyInstaller
- **Mode one-file**: Un seul fichier .exe (recommandé pour la distribution)
- **Mode one-directory**: Dossier avec tous les fichiers (plus rapide, plus volumineux)
- **Console cachée**: Application GUI sans fenêtre de console
- **Icône personnalisée**: Icône Windows native
- **Informations de version**: Métadonnées Windows complètes

### Inno Setup
- **Installation silencieuse**: Support des paramètres en ligne de commande
- **Raccourcis**: Menu Démarrer et bureau
- **Désinstallation**: Suppression complète
- **Compression LZMA**: Taille d'installateur optimisée
- **Interface moderne**: Assistant d'installation Windows 10/11

## 🐛 Résolution des Problèmes

### Erreur: "Python n'est pas dans le PATH"
- Réinstallez Python en cochant "Add Python to PATH"
- Ou ajoutez manuellement Python au PATH système

### Erreur: "PyInstaller non trouvé"
```bash
pip install pyinstaller
```

### Erreur: "Inno Setup non trouvé"
- Installez Inno Setup depuis [jrsoftware.org](https://jrsoftware.org/isdl.php)
- Assurez-vous que `iscc` est dans le PATH

### L'exécutable ne démarre pas
- Vérifiez que toutes les dépendances sont installées
- Testez d'abord l'application Python: `python gui.py`
- Consultez les logs dans le dossier `build/`

### L'exécutable est trop volumineux
- Utilisez `--exclude-module` pour exclure des modules inutiles
- Activez UPX pour la compression (déjà activé par défaut)
- Utilisez le mode one-directory au lieu de one-file

## 🔍 Débogage

### Mode debug PyInstaller
```bash
python build_exe.py --debug
```

### Logs détaillés
Les logs de construction sont affichés dans la console. En cas d'erreur, vérifiez:
- Les modules manquants dans `hiddenimports`
- Les fichiers manquants dans `datas`
- Les conflits de dépendances

### Test de l'exécutable
1. Lancez l'exécutable depuis `dist/`
2. Vérifiez que l'interface se charge
3. Testez les fonctionnalités principales
4. Vérifiez les logs d'erreur

## 📦 Distribution

### Fichiers à distribuer
- **Exécutable seul**: `dist/YouTube-to-TikTok.exe`
- **Installateur complet**: `installer/YouTube-to-TikTok-Setup.exe`

### Recommandations
- Testez sur une machine Windows propre
- Vérifiez la compatibilité Windows 10/11
- Incluez un fichier README avec les instructions
- Fournissez un support pour les utilisateurs

## 🆘 Support

### Problèmes courants
- **Antivirus**: Certains antivirus peuvent bloquer PyInstaller
- **Permissions**: Exécutez en tant qu'administrateur si nécessaire
- **Espace disque**: Assurez-vous d'avoir au moins 2 GB d'espace libre

### Ressources utiles
- [Documentation PyInstaller](https://pyinstaller.readthedocs.io/)
- [Documentation Inno Setup](https://jrsoftware.org/ishelp/)
- [Forum PyInstaller](https://github.com/pyinstaller/pyinstaller/discussions)

---

**Note**: Ce guide est optimisé pour Windows. Pour d'autres plateformes, adaptez les commandes et outils de construction.
