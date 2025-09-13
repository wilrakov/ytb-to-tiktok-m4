# 🚀 Installation Rapide - Interface Graphique

## 📋 Prérequis

- **Windows 10/11** (testé et optimisé)
- **Python 3.8+** avec tkinter
- **Connexion Internet** pour télécharger les dépendances

## ⚡ Installation en 3 étapes

### 1️⃣ Installer Python
- Téléchargez Python depuis [python.org](https://python.org)
- **IMPORTANT** : Cochez "Add Python to PATH" lors de l'installation
- Redémarrez votre terminal après l'installation

### 2️⃣ Installer les dépendances
Double-cliquez sur `install_dependencies.bat` et suivez les instructions.

**Ou manuellement :**
```bash
pip install -r requirements.txt
```

### 3️⃣ Lancer l'interface
Double-cliquez sur `lancer_interface.bat` et c'est parti !

## 🎯 Fichiers de lancement

| Fichier | Description | Utilisation |
|---------|-------------|-------------|
| `lancer_interface.bat` | Lanceur Windows simple | Double-clic |
| `lancer_interface.ps1` | Script PowerShell avancé | PowerShell |
| `launch_gui.py` | Lanceur Python direct | Terminal |
| `gui.py` | Interface principale | Développement |

## 🔧 Vérification de l'installation

Lancez `test_gui.py` pour vérifier que tout fonctionne :
```bash
python test_gui.py
```

## 🆘 Dépannage rapide

### L'interface ne se lance pas
1. Vérifiez Python : `python --version`
2. Vérifiez tkinter : `python -c "import tkinter"`
3. Relancez `install_dependencies.bat`

### Erreur de dépendances
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Problème de permissions
Exécutez PowerShell en tant qu'administrateur et lancez :
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## 📚 Documentation complète

- **README_GUI.md** : Guide complet de l'interface
- **README.md** : Documentation du projet principal

## 🎉 C'est parti !

Une fois l'installation terminée, vous pouvez :
- Convertir des vidéos YouTube en segments TikTok
- Personnaliser l'apparence des labels
- Suivre le processus en temps réel
- Gérer tous les paramètres via une interface intuitive

**Bonnes conversions ! 🎬✨**
