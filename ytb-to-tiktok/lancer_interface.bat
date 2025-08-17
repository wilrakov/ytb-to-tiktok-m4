@echo off
chcp 65001 >nul
echo Lancement de l'interface graphique YouTube to TikTok...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python depuis https://python.org
    pause
    exit /b 1
)

REM Vérifier si les dépendances sont installées
echo Vérification des dépendances...
python -c "import tkinter" >nul 2>&1
if errorlevel 1 (
    echo ERREUR: tkinter n'est pas disponible
    echo Veuillez réinstaller Python avec tkinter
    pause
    exit /b 1
)

REM Lancer l'interface graphique
echo Lancement de l'interface...
python launch_gui.py

REM En cas d'erreur, attendre que l'utilisateur lise le message
if errorlevel 1 (
    echo.
    echo Une erreur s'est produite. Vérifiez les messages ci-dessus.
    pause
)
