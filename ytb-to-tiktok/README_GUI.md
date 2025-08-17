# Interface Graphique YouTube to TikTok

## 🎯 Vue d'ensemble

Cette interface graphique moderne et intuitive permet d'utiliser facilement le logiciel `ytb-to-tiktok` sans avoir à taper de commandes dans le terminal. Elle offre une expérience utilisateur professionnelle avec toutes les fonctionnalités du logiciel en ligne de commande.

## 🚀 Lancement rapide

### Option 1 : Double-clic sur le fichier batch (Windows)
1. Double-cliquez sur `lancer_interface.bat`
2. L'interface se lance automatiquement

### Option 2 : Ligne de commande
```bash
python launch_gui.py
```

### Option 3 : Directement
```bash
python gui.py
```

## 🖥️ Interface utilisateur

### Onglet "Configuration" (Principal)
- **URL YouTube** : Collez l'URL de la vidéo à convertir
- **Dossier de sortie** : Choisissez où sauvegarder les fichiers
- **Dossier des segments** : Dossier pour les segments découpés (auto-configuré)
- **Durée des segments** : Durée en secondes de chaque segment (défaut: 60s)
- **Limite de segments** : Nombre maximum de segments à créer (optionnel)

#### Options de surimpression
- **Ajouter des labels** : Active l'ajout de texte "Partie X" sur les vidéos
- **Template** : Modèle de texte (variables: `{i}`, `{n}`, `{total}`)
- **Taille de police** : Taille du texte en pixels
- **Position** : Position du texte sur la vidéo
  - `tc` : Top Center (haut centre)
  - `tl` : Top Left (haut gauche)
  - `tr` : Top Right (haut droite)
  - `bl` : Bottom Left (bas gauche)
  - `br` : Bottom Right (bas droite)
  - `center` : Centre de la vidéo
- **Style arrondi** : Utilise des coins arrondis (nécessite Pillow)

### Onglet "Options avancées"
- **Fichier cookies** : Fichier de cookies pour accéder aux vidéos privées
- **Cookies depuis navigateur** : Import automatique depuis Chrome, Firefox, etc.
- **User-Agent** : Agent utilisateur personnalisé
- **Proxy** : Configuration de proxy HTTP/HTTPS

#### Options de label avancées
- **Couleur du texte** : Couleur du texte (nom ou code hex)
- **Couleur de fond** : Couleur de la boîte de fond
- **Épaisseur de bordure** : Épaisseur de la bordure autour du texte
- **Rayon d'arrondi** : Rayon des coins arrondis (style arrondi)
- **Padding** : Espacement interne autour du texte
- **Afficher la boîte** : Active/désactive la boîte de fond

### Onglet "Logs"
- **Affichage en temps réel** : Suivi du processus de conversion
- **Couleurs** : Logs colorés selon le type (succès, erreur, avertissement)
- **Actions** : Effacer et sauvegarder les logs

## ⌨️ Raccourcis clavier

- **Ctrl+Enter** : Démarrer la conversion
- **Ctrl+Q** : Quitter l'application

## 🔧 Fonctionnalités

### Gestion des erreurs
- Validation des champs obligatoires
- Messages d'erreur clairs et informatifs
- Gestion gracieuse des exceptions

### Interface responsive
- Redimensionnement automatique des fenêtres
- Adaptation aux différentes résolutions d'écran
- Design moderne et professionnel

### Suivi en temps réel
- Barre de statut informative
- Logs en temps réel
- Indicateurs visuels de progression

### Gestion des fichiers
- Sélecteurs de dossiers intégrés
- Validation des chemins
- Configuration automatique des dossiers

## 📋 Prérequis

### Python
- Python 3.7 ou supérieur
- Module `tkinter` (inclus avec Python)

### Dépendances
```bash
pip install -r requirements.txt
```

### FFmpeg
- FFmpeg doit être installé et accessible dans le PATH
- Ou utilisez `imageio-ffmpeg` (installé automatiquement)

## 🐛 Dépannage

### L'interface ne se lance pas
1. Vérifiez que Python est installé : `python --version`
2. Vérifiez que tkinter est disponible : `python -c "import tkinter"`
3. Vérifiez que toutes les dépendances sont installées

### Erreur lors de la conversion
1. Vérifiez que FFmpeg est installé
2. Vérifiez que l'URL YouTube est valide
3. Consultez l'onglet "Logs" pour plus de détails

### Problèmes de performance
1. Fermez les autres applications
2. Vérifiez l'espace disque disponible
3. Utilisez des paramètres de qualité appropriés

## 🔄 Mise à jour

Pour mettre à jour l'interface graphique :
1. Remplacez le fichier `gui.py` par la nouvelle version
2. Redémarrez l'application

## 📝 Personnalisation

L'interface peut être personnalisée en modifiant :
- Les couleurs et styles dans `setup_styles()`
- La disposition des éléments dans `setup_ui()`
- Les raccourcis clavier dans `setup_bindings()`

## 🤝 Support

Pour toute question ou problème :
1. Consultez d'abord ce README
2. Vérifiez les logs dans l'onglet "Logs"
3. Consultez la documentation du projet principal

## 📄 Licence

Cette interface graphique suit la même licence que le projet principal `ytb-to-tiktok`.
