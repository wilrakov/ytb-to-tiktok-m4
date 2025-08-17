@echo off
chcp 65001 >nul
echo ========================================
echo Installation des dépendances de construction
echo YouTube to TikTok
echo ========================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo Veuillez installer Python 3.8+ depuis https://python.org
    echo Assurez-vous de cocher "Add Python to PATH" lors de l'installation
    echo.
    pause
    exit /b 1
)

echo ✓ Python trouvé
python --version

REM Vérifier que pip est installé
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: pip n'est pas installé
    echo.
    echo Réinstallez Python en cochant "Add pip to PATH"
    pause
    exit /b 1
)

echo ✓ pip trouvé
pip --version

echo.
echo 🔧 Mise à jour de pip...
python -m pip install --upgrade pip

echo.
echo 📦 Installation des dépendances principales...
pip install -r requirements.txt

echo.
echo 🔨 Installation des outils de construction...
pip install -r requirements-build.txt

echo.
echo ✅ Vérification des installations...

REM Vérifier PyInstaller
python -c "import PyInstaller; print(f'✓ PyInstaller {PyInstaller.__version__}')" 2>nul
if errorlevel 1 (
    echo ✗ PyInstaller non installé
    pip install pyinstaller
) else (
    echo ✓ PyInstaller installé
)

REM Vérifier Pillow
python -c "import PIL; print(f'✓ Pillow {PIL.__version__}')" 2>nul
if errorlevel 1 (
    echo ✗ Pillow non installé
    pip install Pillow
) else (
    echo ✓ Pillow installé
)

REM Vérifier auto-py-to-exe
python -c "import auto_py_to_exe; print(f'✓ auto-py-to-exe installé')" 2>nul
if errorlevel 1 (
    echo ✗ auto-py-to-exe non installé
    pip install auto-py-to-exe
) else (
    echo ✓ auto-py-to-exe installé
)

echo.
echo 🎯 Vérification des outils de construction...

REM Vérifier PyInstaller
pyinstaller --version >nul 2>&1
if errorlevel 1 (
    echo ⚠ PyInstaller n'est pas dans le PATH
    echo   Utilisez: python -m PyInstaller
) else (
    echo ✓ PyInstaller accessible via: pyinstaller
)

REM Vérifier auto-py-to-exe
auto-py-to-exe --version >nul 2>&1
if errorlevel 1 (
    echo ⚠ auto-py-to-exe n'est pas dans le PATH
    echo   Utilisez: python -m auto_py_to_exe
) else (
    echo ✓ auto-py-to-exe accessible via: auto-py-to-exe
)

echo.
echo 📋 Outils disponibles:

echo.
echo 1. Construction via script Python:
echo    python build_exe.py --help

echo.
echo 2. Construction via script batch:
echo    build_exe.bat

echo.
echo 3. Construction via PowerShell:
echo    .\build_exe.ps1 -Help

echo.
echo 4. Interface graphique auto-py-to-exe:
echo    auto-py-to-exe

echo.
echo 5. Construction manuelle PyInstaller:
echo    python -m PyInstaller --onefile --windowed --icon=icon.ico gui.py

echo.
echo 🚀 Pour commencer la construction:
echo   1. Double-cliquez sur build_exe.bat
echo   2. Ou lancez: python build_exe.py --clean
echo.

echo ✅ Installation terminée!
echo.
echo Prochaine étape: Construire l'exécutable
echo.
pause
