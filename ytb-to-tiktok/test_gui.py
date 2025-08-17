#!/usr/bin/env python3
"""
Test simple de l'interface graphique
Vérifie que tous les composants se chargent correctement
"""

import sys
import tkinter as tk
from pathlib import Path

def test_tkinter():
    """Test que tkinter fonctionne"""
    try:
        root = tk.Tk()
        root.withdraw()  # Cacher la fenêtre
        
        # Test des composants de base
        label = tk.Label(root, text="Test")
        button = tk.Button(root, text="Test")
        entry = tk.Entry(root)
        
        # Test des composants ttk
        from tkinter import ttk
        ttk_label = ttk.Label(root, text="Test")
        ttk_button = ttk.Button(root, text="Test")
        ttk_entry = ttk.Entry(root)
        
        root.destroy()
        return True
    except Exception as e:
        print(f"Erreur tkinter: {e}")
        return False

def test_imports():
    """Test que tous les modules nécessaires peuvent être importés"""
    try:
        # Test des imports de base
        import threading
        import queue
        import os
        from pathlib import Path
        from typing import Optional
        
        # Test des imports de l'interface
        sys.path.insert(0, str(Path(__file__).parent))
        from gui import ModernTkinterApp
        
        return True
    except ImportError as e:
        print(f"Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        return False

def test_cli_import():
    """Test que le module CLI peut être importé"""
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from ytb_to_tiktok.cli import parse_args, main
        
        # Test de parse_args avec des arguments simples
        args = parse_args(["https://example.com"])
        print(f"Arguments parsés avec succès: {args}")
        
        return True
    except Exception as e:
        print(f"Erreur CLI: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("=== Test de l'interface graphique ===\n")
    
    # Test 1: Tkinter
    print("1. Test de tkinter...")
    if test_tkinter():
        print("   ✓ Tkinter fonctionne correctement")
    else:
        print("   ✗ Erreur avec tkinter")
        return False
    
    # Test 2: Imports
    print("2. Test des imports...")
    if test_imports():
        print("   ✓ Tous les imports fonctionnent")
    else:
        print("   ✗ Erreur avec les imports")
        return False
    
    # Test 3: Module CLI
    print("3. Test du module CLI...")
    if test_cli_import():
        print("   ✓ Module CLI accessible")
    else:
        print("   ✗ Erreur avec le module CLI")
        return False
    
    print("\n=== Résumé ===")
    print("✓ Tous les tests sont passés avec succès!")
    print("L'interface graphique devrait fonctionner correctement.")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Certains tests ont échoué.")
        print("Vérifiez l'installation et les dépendances.")
    
    input("\nAppuyez sur Entrée pour fermer...")
