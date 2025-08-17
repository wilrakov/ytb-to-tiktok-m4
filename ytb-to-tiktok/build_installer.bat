@echo off
chcp 65001 >nul
echo ========================================
echo Construction de l'installateur YouTube to TikTok
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

REM Vérifier que Inno Setup est installé
iscc --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ATTENTION: Inno Setup n'est pas installé
    echo Téléchargez-le depuis: https://jrsoftware.org/isdl.php
    echo.
    echo Construction de l'exécutable uniquement...
    echo.
    python build_exe.py --clean
    if errorlevel 1 (
        echo ERREUR: Échec de la construction de l'exécutable
        pause
        exit /b 1
    )
    echo.
    echo Exécutable construit avec succès!
    echo Pour créer l'installateur, installez Inno Setup et relancez ce script
    pause
    exit /b 0
)

echo ✓ Inno Setup trouvé
iscc --version

echo.
echo 🔨 Construction de l'exécutable...
python build_exe.py --clean --installer
if errorlevel 1 (
    echo ERREUR: Échec de la construction de l'exécutable
    pause
    exit /b 1
)

echo.
echo 🔨 Construction de l'installateur...
if not exist "dist\YouTube-to-TikTok.exe" (
    echo ERREUR: L'exécutable n'a pas été créé
    pause
    exit /b 1
)

REM Créer le dossier installer s'il n'existe pas
if not exist "installer" mkdir installer

REM Compiler l'installateur avec Inno Setup
iscc installer.iss
if errorlevel 1 (
    echo ERREUR: Échec de la construction de l'installateur
    pause
    exit /b 1
)

echo.
echo 🎉 Construction terminée avec succès!
echo.
echo Fichiers créés:
echo   - dist\YouTube-to-TikTok.exe (exécutable)
echo   - installer\YouTube-to-TikTok-Setup.exe (installateur)
echo.
echo L'application est prête à être distribuée!
echo.
pause
