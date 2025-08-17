@echo off
chcp 65001 >nul
echo ========================================
echo Construction de l'exécutable YouTube to TikTok
echo ========================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

echo ✓ Python trouvé
python --version

echo.
echo 🔨 Construction de l'exécutable...
python build_exe.py --clean

if errorlevel 1 (
    echo.
    echo ❌ Échec de la construction
    pause
    exit /b 1
)

echo.
echo 🎉 Construction terminée avec succès!
echo.
echo L'exécutable se trouve dans: dist\YouTube-to-TikTok.exe
echo.
pause
