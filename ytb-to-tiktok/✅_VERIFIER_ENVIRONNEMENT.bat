@echo off
chcp 65001 >nul
title Vérification Environnement - YouTube to TikTok
color 0E

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                ✅ VÉRIFICATION ENVIRONNEMENT ✅              ║
echo ║              YouTube to TikTok - Construction               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Ce script vérifie que votre environnement est prêt pour
echo la construction de l'exécutable YouTube to TikTok.
echo.

REM Initialiser la variable de contrôle des fichiers
set all_files_ok=True

echo 🐍 Vérification Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python non trouvé
    echo.
    echo 🔧 INSTALLATION REQUISE:
    echo   1. Téléchargez Python 3.8+ depuis https://python.org
    echo   2. Cochez "Add Python to PATH" lors de l'installation
    echo   3. Redémarrez ce script après installation
    echo.
    pause
    exit /b 1
)

echo ✓ Python trouvé
python --version

echo.
echo 📦 Vérification pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip non trouvé
    echo.
    echo 🔧 SOLUTIONS:
    echo   1. Réinstallez Python en cochant "Add pip to PATH"
    echo   2. Ou exécutez: python -m ensurepip --upgrade
    echo.
    pause
    exit /b 1
)

echo ✓ pip trouvé
pip --version

echo.
echo 🔧 Vérification des outils de construction...
echo.

REM Vérifier PyInstaller
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo ❌ PyInstaller non installé
    echo.
    echo 🔧 INSTALLATION AUTOMATIQUE:
    echo   pip install pyinstaller
    echo.
    pip install pyinstaller
    if errorlevel 1 (
        echo ❌ Échec de l'installation
        pause
        exit /b 1
    )
    echo ✓ PyInstaller installé
) else (
    echo ✓ PyInstaller déjà installé
)

REM Vérifier Pillow
python -c "import PIL" 2>nul
if errorlevel 1 (
    echo ❌ Pillow non installé
    echo.
    echo 🔧 INSTALLATION AUTOMATIQUE:
    echo   pip install Pillow
    echo.
    pip install Pillow
    if errorlevel 1 (
        echo ❌ Échec de l'installation
        pause
        exit /b 1
    )
    echo ✓ Pillow installé
) else (
    echo ✓ Pillow déjà installé
)

REM Vérifier auto-py-to-exe
python -c "import auto_py_to_exe" 2>nul
if errorlevel 1 (
    echo ❌ auto-py-to-exe non installé
    echo.
    echo 🔧 INSTALLATION AUTOMATIQUE:
    echo   pip install auto-py-to-exe
    echo.
    pip install auto-py-to-exe
    if errorlevel 1 (
        echo ❌ Échec de l'installation
        pause
        exit /b 1
    )
    echo ✓ auto-py-to-exe installé
) else (
    echo ✓ auto-py-to-exe déjà installé
)

echo.
echo 📁 Vérification des fichiers du projet...
echo.

REM Vérifier les fichiers essentiels
echo Vérification des fichiers essentiels...

if exist "gui.py" (
    echo ✓ gui.py
) else (
    echo ❌ gui.py - MANQUANT
    set all_files_ok=False
)

if exist "ytb_to_tiktok\__init__.py" (
    echo ✓ ytb_to_tiktok\__init__.py
) else (
    echo ❌ ytb_to_tiktok\__init__.py - MANQUANT
    set all_files_ok=False
)

if exist "ytb_to_tiktok\cli.py" (
    echo ✓ ytb_to_tiktok\cli.py
) else (
    echo ❌ ytb_to_tiktok\cli.py - MANQUANT
    set all_files_ok=False
)

if exist "requirements.txt" (
    echo ✓ requirements.txt
) else (
    echo ❌ requirements.txt - MANQUANT
    set all_files_ok=False
)

if exist "setup.py" (
    echo ✓ setup.py
) else (
    echo ❌ setup.py - MANQUANT
    set all_files_ok=False
)

if "%all_files_ok%"=="False" (
    echo.
    echo ❌ Certains fichiers essentiels sont manquants
    echo.
    echo 🔧 VÉRIFIEZ:
    echo   1. Êtes-vous dans le bon dossier?
    echo   2. Le projet est-il complet?
    echo   3. Y a-t-il des erreurs de téléchargement?
    echo.
    pause
    exit /b 1
)

echo.
echo 🧪 Lancement des tests de validation...
echo.

REM Lancer les tests Python
python test_build.py

if errorlevel 1 (
    echo.
    echo ❌ Certains tests ont échoué
    echo.
    echo 🔧 SOLUTIONS:
    echo   1. Vérifiez les erreurs ci-dessus
    echo   2. Installez les dépendances manquantes
    echo   3. Relancez: python test_build.py
    echo.
    pause
    exit /b 1
)

echo.
echo 🎉 ENVIRONNEMENT VALIDÉ AVEC SUCCÈS!
echo.
echo ✅ Python: OK
echo ✅ pip: OK
echo ✅ PyInstaller: OK
echo ✅ Pillow: OK
echo ✅ auto-py-to-exe: OK
echo ✅ Fichiers projet: OK
echo ✅ Tests: OK
echo.
echo 🚀 Votre environnement est prêt pour la construction!
echo.
echo 🎯 PROCHAINES ÉTAPES:
echo   1. Construction simple: 🚀_CONSTRUIRE_EXECUTABLE.bat
echo   2. Interface graphique: 🎨_INTERFACE_GRAPHIQUE.bat
echo   3. Construction complète: build_installer.bat
echo.
echo 📚 Documentation complète: README_BUILD.md
echo 📋 Résumé: 📋_RESUME_CONSTRUCTION.md
echo.

echo Appuyez sur une touche pour continuer...
pause >nul

echo.
echo 🚀 Lancement de la construction automatique...
echo.

REM Lancer la construction
🚀_CONSTRUIRE_EXECUTABLE.bat
