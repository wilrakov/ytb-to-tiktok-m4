@echo off
chcp 65001 >nul
title Interface Graphique de Construction - YouTube to TikTok
color 0B

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🎨 INTERFACE GRAPHIQUE 🎨                    ║
echo ║              Construction Exécutable YouTube to TikTok      ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Ce script lance l'interface graphique auto-py-to-exe pour
echo configurer et construire votre exécutable de manière visuelle.
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
echo 🔧 Vérification d'auto-py-to-exe...
echo.

REM Vérifier auto-py-to-exe
python -c "import auto_py_to_exe" 2>nul
if errorlevel 1 (
    echo ⚠ auto-py-to-exe non installé. Installation en cours...
    echo.
    pip install auto-py-to-exe
    
    if errorlevel 1 (
        echo ❌ Échec de l'installation d'auto-py-to-exe
        echo.
        echo 🔧 SOLUTIONS:
        echo   1. Vérifiez votre connexion internet
        echo   2. Essayez: pip install --upgrade pip
        echo   3. Relancez ce script
        echo.
        pause
        exit /b 1
    )
    
    echo ✓ auto-py-to-exe installé avec succès
) else (
    echo ✓ auto-py-to-exe déjà installé
)

echo.
echo 🎨 Lancement de l'interface graphique...
echo.
echo L'interface va s'ouvrir dans votre navigateur web.
echo.
echo 💡 CONFIGURATION RECOMMANDÉE:
echo   1. Script Location: gui.py
echo   2. Onefile: ✓ (recommandé)
echo   3. Console Window: Window Based (pas de console)
echo   4. Icon: icon.ico (sera créé automatiquement)
echo   5. Additional Files: config.example.ini, README.md, LICENSE
echo   6. Advanced: Utilisez le fichier auto_py_to_exe_config.json
echo.
echo ⏳ Ouverture de l'interface...

REM Lancer auto-py-to-exe
start "" "http://127.0.0.1:5000"
python -m auto_py_to_exe

echo.
echo ✅ Interface fermée
echo.
echo 🎯 Prochaines étapes:
echo   1. L'exécutable sera créé dans le dossier dist/
echo   2. Testez-le en double-cliquant dessus
echo   3. Pour un installateur: utilisez build_installer.bat
echo.
echo 📚 Documentation: README_BUILD.md
echo 🧪 Tests: python test_build.py
echo.

pause
