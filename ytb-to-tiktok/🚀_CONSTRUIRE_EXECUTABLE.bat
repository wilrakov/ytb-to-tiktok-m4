@echo off
chcp 65001 >nul
title Construction Exécutable YouTube to TikTok
color 0A

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 CONSTRUCTION EXÉCUTABLE 🚀            ║
echo ║                   YouTube to TikTok v1.0.0                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Ce script va construire un exécutable Windows autonome de votre
echo application YouTube to TikTok.
echo.

echo 📋 Vérification de l'environnement...
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo 🔧 SOLUTIONS:
    echo   1. Installez Python 3.8+ depuis https://python.org
    echo   2. Cochez "Add Python to PATH" lors de l'installation
    echo   3. Redémarrez ce script après installation
    echo.
    pause
    exit /b 1
)

echo ✓ Python trouvé
python --version

echo.
echo 🔧 Installation des dépendances de construction...
echo.

REM Installer les dépendances si nécessaire
if not exist "requirements-build.txt" (
    echo ❌ Fichier requirements-build.txt manquant
    pause
    exit /b 1
)

echo Installation des outils de construction...
pip install -r requirements-build.txt

if errorlevel 1 (
    echo ❌ Erreur lors de l'installation des dépendances
    echo.
    echo 🔧 SOLUTIONS:
    echo   1. Vérifiez votre connexion internet
    echo   2. Essayez: pip install --upgrade pip
    echo   3. Relancez ce script
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Dépendances installées avec succès!
echo.

echo 🚀 Démarrage de la construction...
echo.

REM Lancer la construction
python build_exe.py --clean

if errorlevel 1 (
    echo.
    echo ❌ Échec de la construction
    echo.
    echo 🔧 SOLUTIONS:
    echo   1. Vérifiez les erreurs ci-dessus
    echo   2. Lancez: python test_build.py
    echo   3. Consultez README_BUILD.md
    echo.
    pause
    exit /b 1
)

echo.
echo 🎉 CONSTRUCTION RÉUSSIE!
echo.

REM Vérifier que l'exécutable a été créé
if exist "dist\YouTube-to-Tiktok.exe" (
    echo ✅ Exécutable créé: dist\YouTube-to-Tiktok.exe
    
    REM Afficher la taille
    for %%A in ("dist\YouTube-to-Tiktok.exe") do (
        set size=%%~zA
        set /a sizeMB=!size!/1024/1024
        echo 📏 Taille: !sizeMB! MB
    )
    
    echo.
    echo 🎯 PROCHAINES ÉTAPES:
    echo   1. Testez l'exécutable: double-cliquez sur dist\YouTube-to-Tiktok.exe
    echo   2. Créez un raccourci sur le bureau
    echo   3. Partagez l'exécutable avec d'autres utilisateurs
    echo.
    echo 💡 Pour créer un installateur complet:
    echo   1. Installez Inno Setup depuis https://jrsoftware.org/isdl.php
    echo   2. Lancez: build_installer.bat
    echo.
    
) else (
    echo ❌ Exécutable non trouvé dans le dossier dist/
    echo.
    echo 🔧 Vérifiez:
    echo   1. Les logs de construction ci-dessus
    echo   2. Le dossier dist/ a-t-il été créé?
    echo   3. Y a-t-il des erreurs dans build/
    echo.
)

echo.
echo 📚 Documentation complète: README_BUILD.md
echo 🧪 Tests: python test_build.py
echo 🔧 Configuration: build_config.py
echo.

echo Appuyez sur une touche pour fermer...
pause >nul
