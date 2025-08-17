#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration de construction
YouTube to TikTok
"""

import sys
import subprocess
from pathlib import Path
import importlib.util

def test_python_version():
    """Teste la version de Python"""
    print("🐍 Test de la version Python...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"✗ Python {version.major}.{version.minor}.{version.micro} - Version 3.8+ requise")
        return False

def test_dependencies():
    """Teste les dépendances principales"""
    print("\n📦 Test des dépendances principales...")
    
    dependencies = [
        "ytb_to_tiktok.cli",
        "ytb_to_tiktok.__main__",
        "PIL",
        "tkinter",
        "yt_dlp",
        "rich",
        "imageio_ffmpeg"
    ]
    
    all_ok = True
    for dep in dependencies:
        try:
            if dep == "tkinter":
                import tkinter
                print(f"✓ {dep} - OK")
            elif dep == "PIL":
                import PIL
                print(f"✓ {dep} - OK")
            else:
                importlib.import_module(dep)
                print(f"✓ {dep} - OK")
        except ImportError as e:
            print(f"✗ {dep} - Manquant: {e}")
            all_ok = False
    
    return all_ok

def test_build_tools():
    """Teste les outils de construction"""
    print("\n🔨 Test des outils de construction...")
    
    build_tools = [
        ("PyInstaller", "pyinstaller"),
        ("auto-py-to-exe", "auto_py_to_exe"),
        ("Pillow", "PIL"),
    ]
    
    all_ok = True
    for name, module in build_tools:
        try:
            if module == "pyinstaller":
                import PyInstaller
                print(f"✓ {name} {PyInstaller.__version__} - OK")
            elif module == "auto_py_to_exe":
                import auto_py_to_exe
                print(f"✓ {name} - OK")
            elif module == "PIL":
                import PIL
                print(f"✓ {name} {PIL.__version__} - OK")
        except ImportError:
            print(f"✗ {name} - Manquant")
            all_ok = False
    
    return all_ok

def test_files():
    """Teste l'existence des fichiers nécessaires"""
    print("\n📁 Test des fichiers nécessaires...")
    
    required_files = [
        "gui.py",
        "ytb_to_tiktok/__init__.py",
        "ytb_to_tiktok/cli.py",
        "requirements.txt",
        "setup.py",
    ]
    
    all_ok = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✓ {file_path} - OK")
        else:
            print(f"✗ {file_path} - Manquant")
            all_ok = False
    
    return all_ok

def test_gui():
    """Teste que l'interface graphique peut être importée"""
    print("\n🖥️ Test de l'interface graphique...")
    
    try:
        # Test d'import sans lancer l'interface
        spec = importlib.util.spec_from_file_location("gui", "gui.py")
        gui_module = importlib.util.module_from_spec(spec)
        
        # Vérifier que la classe principale existe
        if hasattr(gui_module, 'ModernTkinterApp'):
            print("✓ Classe ModernTkinterApp - OK")
        else:
            print("✗ Classe ModernTkinterApp manquante")
            return False
        
        # Vérifier que la fonction main existe
        if hasattr(gui_module, 'main'):
            print("✓ Fonction main - OK")
        else:
            print("✗ Fonction main manquante")
            return False
        
        print("✓ Interface graphique - OK")
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors du test de l'interface: {e}")
        return False

def test_cli():
    """Teste que la CLI peut être importée"""
    print("\n💻 Test de l'interface en ligne de commande...")
    
    try:
        from ytb_to_tiktok.cli import main, parse_args
        print("✓ Fonctions CLI - OK")
        return True
    except Exception as e:
        print(f"✗ Erreur lors du test de la CLI: {e}")
        return False

def test_build_config():
    """Teste la configuration de construction"""
    print("\n⚙️ Test de la configuration de construction...")
    
    try:
        from build_config import (
            APP_NAME, APP_VERSION, PYINSTALLER_CONFIG,
            INCLUDED_FILES, HIDDEN_IMPORTS
        )
        
        print(f"✓ Configuration chargée - {APP_NAME} v{APP_VERSION}")
        print(f"✓ Options PyInstaller: {len(PYINSTALLER_CONFIG)}")
        print(f"✓ Fichiers inclus: {len(INCLUDED_FILES)}")
        print(f"✓ Imports cachés: {len(HIDDEN_IMPORTS)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Erreur lors du test de la configuration: {e}")
        return False

def test_pyinstaller_command():
    """Teste que PyInstaller peut être exécuté"""
    print("\n🚀 Test de la commande PyInstaller...")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ PyInstaller {version} - OK")
            return True
        else:
            print(f"✗ PyInstaller - Erreur: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ PyInstaller - Timeout")
        return False
    except Exception as e:
        print(f"✗ PyInstaller - Erreur: {e}")
        return False

def run_all_tests():
    """Exécute tous les tests"""
    print("🧪 Tests de construction YouTube to TikTok")
    print("=" * 50)
    
    tests = [
        ("Version Python", test_python_version),
        ("Dépendances", test_dependencies),
        ("Outils de construction", test_build_tools),
        ("Fichiers", test_files),
        ("Interface graphique", test_gui),
        ("Interface CLI", test_cli),
        ("Configuration", test_build_config),
        ("Commande PyInstaller", test_pyinstaller_command),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} - Erreur: {e}")
            results.append((test_name, False))
    
    # Résumé
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\nRésultat: {passed}/{total} tests réussis")
    
    if passed == total:
        print("🎉 Tous les tests sont réussis! L'application est prête pour la construction.")
        return True
    else:
        print("⚠️ Certains tests ont échoué. Vérifiez les erreurs ci-dessus.")
        return False

def main():
    """Fonction principale"""
    success = run_all_tests()
    
    if success:
        print("\n🚀 Prochaines étapes:")
        print("1. Installer les dépendances: install_dependencies_build.bat")
        print("2. Construire l'exécutable: build_exe.bat")
        print("3. Ou utiliser PowerShell: .\\build_exe.ps1 -Clean")
        print("4. Ou Python direct: python build_exe.py --clean")
    else:
        print("\n❌ Problèmes détectés:")
        print("1. Vérifiez que Python 3.8+ est installé")
        print("2. Installez les dépendances: pip install -r requirements-build.txt")
        print("3. Vérifiez que tous les fichiers sont présents")
        print("4. Relancez les tests: python test_build.py")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
