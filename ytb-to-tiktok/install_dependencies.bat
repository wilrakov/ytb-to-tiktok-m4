@echo off
chcp 65001 >nul
echo === Installation des dépendances YouTube to TikTok ===
echo.

REM Vérifier si Python est installé
echo Vérification de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé
    echo.
    echo Veuillez installer Python depuis https://python.org
    echo Assurez-vous de cocher "Add Python to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)

echo ✓ Python est installé
python --version

echo.
echo Installation des dépendances...
echo.

REM Mettre à jour pip
echo Mise à jour de pip...
python -m pip install --upgrade pip

REM Installer les dépendances
echo.
echo Installation des packages requis...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERREUR: Échec de l'installation des dépendances
    echo.
    echo Solutions possibles:
    echo 1. Vérifiez votre connexion Internet
    echo 2. Essayez: pip install --user -r requirements.txt
    echo 3. Vérifiez que vous avez les droits administrateur
    echo.
    pause
    exit /b 1
)

echo.
echo ✓ Toutes les dépendances ont été installées avec succès!
echo.

REM Vérifier l'installation
echo Vérification de l'installation...
python -c "import yt_dlp, rich, PIL; print('✓ Toutes les dépendances sont disponibles')" 2>nul
if errorlevel 1 (
    echo.
    echo ⚠ ATTENTION: Certaines dépendances ne sont pas disponibles
    echo Lancez 'python test_gui.py' pour diagnostiquer le problème
    echo.
) else (
    echo.
    echo 🎉 Installation terminée avec succès!
    echo.
    echo Vous pouvez maintenant lancer l'interface graphique avec:
    echo - Double-clic sur 'lancer_interface.bat'
    echo - Ou: python launch_gui.py
    echo.
)

pause
