#!/usr/bin/env python3
"""
Lanceur simple pour l'interface graphique de ytb-to-tiktok
"""

import sys
import os
from pathlib import Path

# Ajouter le répertoire courant au path Python
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
    from gui import main
    print("Lancement de l'interface graphique...")
    main()
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assurez-vous que tous les fichiers sont présents dans le répertoire.")
    input("Appuyez sur Entrée pour fermer...")
except Exception as e:
    print(f"Erreur lors du lancement: {e}")
    input("Appuyez sur Entrée pour fermer...")
