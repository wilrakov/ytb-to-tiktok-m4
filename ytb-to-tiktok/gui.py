#!/usr/bin/env python3
"""
Interface graphique pour ytb-to-tiktok
Interface moderne et responsive pour convertir des vidéos YouTube en segments TikTok
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
from pathlib import Path
from typing import Optional
import sys

# Ajouter le répertoire parent au path pour importer ytb_to_tiktok
sys.path.insert(0, str(Path(__file__).parent))
from ytb_to_tiktok.cli import main as cli_main, parse_args


class ModernTkinterApp:
    """Application Tkinter moderne avec design professionnel"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube to TikTok - Convertisseur de Vidéos")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)
        
        # Configuration du style
        self.setup_styles()
        
        # Variables
        self.output_dir = tk.StringVar(value=str(Path.cwd() / "outputs"))
        self.segments_dir = tk.StringVar()
        self.segment_seconds = tk.IntVar(value=60)
        self.limit_segments = tk.IntVar()
        self.cookies_file = tk.StringVar()
        self.cookies_browser = tk.StringVar()
        self.user_agent = tk.StringVar()
        self.proxy = tk.StringVar()
        
        # Options de label
        self.add_label = tk.BooleanVar(value=False)
        self.label_template = tk.StringVar(value="Partie {i}")
        self.label_fontsize = tk.IntVar(value=54)
        self.label_color = tk.StringVar(value="black")
        self.label_position = tk.StringVar(value="tc")
        self.label_boxcolor = tk.StringVar(value="white")
        self.label_boxborderw = tk.IntVar(value=14)
        self.label_rounded = tk.BooleanVar(value=False)
        self.label_radius = tk.IntVar(value=24)
        self.label_padding = tk.IntVar(value=18)
        self.label_box = tk.BooleanVar(value=True)
        
        # Initialiser le dossier des segments automatiquement
        self.auto_segments_dir()
        
        # Queue pour la communication entre threads
        self.log_queue = queue.Queue()
        
        # État de l'application
        self.is_processing = False
        
        self.setup_ui()
        self.setup_bindings()
        
        # Démarrer la surveillance de la queue de logs
        self.check_log_queue()
    
    def setup_styles(self):
        """Configure les styles de l'interface"""
        style = ttk.Style()
        
        # Thème moderne
        try:
            style.theme_use('clam')
        except:
            pass
        
        # Couleurs personnalisées
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Segoe UI', 12, 'bold'))
        style.configure('Success.TLabel', foreground='#28a745')
        style.configure('Error.TLabel', foreground='#dc3545')
        style.configure('Warning.TLabel', foreground='#ffc107')
        
        # Boutons
        style.configure('Primary.TButton', 
                       background='#007bff', 
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        style.configure('Success.TButton',
                       background='#28a745',
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
        style.configure('Danger.TButton',
                       background='#dc3545',
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'))
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        # Configuration des colonnes et lignes pour la responsivité
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        
        # Titre principal
        title_frame = ttk.Frame(self.root)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.columnconfigure(0, weight=1)
        
        title_label = ttk.Label(title_frame, 
                               text="YouTube to TikTok", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, sticky="w")
        
        subtitle_label = ttk.Label(title_frame, 
                                  text="Convertisseur de vidéos YouTube en segments TikTok", 
                                  font=('Segoe UI', 10))
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        # Notebook principal pour organiser les sections
        notebook = ttk.Notebook(self.root)
        notebook.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        
        # Onglet principal
        main_frame = ttk.Frame(notebook)
        notebook.add(main_frame, text="Configuration")
        self.setup_main_tab(main_frame)
        
        # Onglet avancé
        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="Options avancées")
        self.setup_advanced_tab(advanced_frame)
        
        # Onglet logs
        logs_frame = ttk.Frame(notebook)
        notebook.add(logs_frame, text="Logs")
        self.setup_logs_tab(logs_frame)
        
        # Barre de statut
        self.status_var = tk.StringVar(value="Prêt")
        status_bar = ttk.Label(self.root, 
                              textvariable=self.status_var, 
                              relief="sunken", 
                              anchor="w")
        status_bar.grid(row=2, column=0, sticky="ew", padx=20)
    
    def setup_main_tab(self, parent):
        """Configure l'onglet principal"""
        # Configuration des colonnes
        parent.columnconfigure(1, weight=1)
        
        row = 0
        
        # URL YouTube
        ttk.Label(parent, text="URL YouTube:", style='Heading.TLabel').grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=10)
        
        self.url_entry = ttk.Entry(parent, font=('Segoe UI', 10))
        self.url_entry.grid(row=row, column=1, sticky="ew", padx=(0, 10), pady=10)
        
        row += 1
        
        # Dossier de sortie
        ttk.Label(parent, text="Dossier de sortie:", style='Heading.TLabel').grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=10)
        
        output_frame = ttk.Frame(parent)
        output_frame.grid(row=row, column=1, sticky="ew", padx=(0, 10), pady=10)
        output_frame.columnconfigure(0, weight=1)
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir, font=('Segoe UI', 10))
        output_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        browse_btn = ttk.Button(output_frame, text="Parcourir", 
                               command=self.browse_output_dir)
        browse_btn.grid(row=0, column=1)
        
        row += 1
        
        # Dossier des segments
        ttk.Label(parent, text="Dossier des segments:", style='Heading.TLabel').grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=10)
        
        segments_frame = ttk.Frame(parent)
        segments_frame.grid(row=row, column=1, sticky="ew", padx=(0, 10), pady=10)
        segments_frame.columnconfigure(0, weight=1)
        
        segments_entry = ttk.Entry(segments_frame, textvariable=self.segments_dir, font=('Segoe UI', 10))
        segments_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        auto_btn = ttk.Button(segments_frame, text="Auto", 
                              command=self.auto_segments_dir)
        auto_btn.grid(row=0, column=1)
        
        row += 1
        
        # Paramètres de découpage
        ttk.Label(parent, text="Durée des segments (secondes):", style='Heading.TLabel').grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=10)
        
        segment_spin = ttk.Spinbox(parent, from_=10, to=300, textvariable=self.segment_seconds, 
                                  width=10, font=('Segoe UI', 10))
        segment_spin.grid(row=row, column=1, sticky="w", padx=(0, 10), pady=10)
        
        row += 1
        
        # Limite de segments
        ttk.Label(parent, text="Limite de segments:", style='Heading.TLabel').grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=10)
        
        limit_spin = ttk.Spinbox(parent, from_=1, to=100, textvariable=self.limit_segments, 
                                width=10, font=('Segoe UI', 10))
        limit_spin.grid(row=row, column=1, sticky="w", padx=(0, 10), pady=10)
        
        # Décocher la valeur par défaut
        self.limit_segments.set("")
        
        row += 1
        
        # Options de label
        label_frame = ttk.LabelFrame(parent, text="Options de surimpression", padding=10)
        label_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=20)
        label_frame.columnconfigure(1, weight=1)
        
        # Activer les labels
        label_check = ttk.Checkbutton(label_frame, text="Ajouter des labels 'Partie X'", 
                                     variable=self.add_label)
        label_check.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        # Template
        ttk.Label(label_frame, text="Template:").grid(row=1, column=0, sticky="w", padx=(0, 10))
        template_entry = ttk.Entry(label_frame, textvariable=self.label_template, font=('Segoe UI', 10))
        template_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10))
        
        # Taille de police
        ttk.Label(label_frame, text="Taille de police:").grid(row=2, column=0, sticky="w", padx=(0, 10))
        fontsize_spin = ttk.Spinbox(label_frame, from_=20, to=100, textvariable=self.label_fontsize, 
                                   width=10, font=('Segoe UI', 10))
        fontsize_spin.grid(row=2, column=1, sticky="w", padx=(0, 10))
        
        # Position
        ttk.Label(label_frame, text="Position:").grid(row=3, column=0, sticky="w", padx=(0, 10))
        position_combo = ttk.Combobox(label_frame, textvariable=self.label_position, 
                                     values=["tc", "tl", "tr", "bl", "br", "center"], 
                                     state="readonly", width=10, font=('Segoe UI', 10))
        position_combo.grid(row=3, column=1, sticky="w", padx=(0, 10))
        
        # Style arrondi
        rounded_check = ttk.Checkbutton(label_frame, text="Style arrondi (nécessite Pillow)", 
                                       variable=self.label_rounded)
        rounded_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))
        
        row += 1
        
        # Bouton de traitement
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        
        self.process_btn = ttk.Button(button_frame, text="Démarrer la conversion", 
                                     style='Success.TButton', 
                                     command=self.start_processing)
        self.process_btn.pack(side="left", padx=(0, 10))
        
        self.stop_btn = ttk.Button(button_frame, text="Arrêter", 
                                   style='Danger.TButton', 
                                   command=self.stop_processing, 
                                   state="disabled")
        self.stop_btn.pack(side="left")
    
    def setup_advanced_tab(self, parent):
        """Configure l'onglet des options avancées"""
        # Configuration des colonnes
        parent.columnconfigure(1, weight=1)
        
        row = 0
        
        # Fichier cookies
        ttk.Label(parent, text="Fichier cookies:", style='Heading.TLabel').grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=10)
        
        cookies_frame = ttk.Frame(parent)
        cookies_frame.grid(row=row, column=1, sticky="ew", padx=(0, 10), pady=10)
        cookies_frame.columnconfigure(0, weight=1)
        
        cookies_entry = ttk.Entry(cookies_frame, textvariable=self.cookies_file, font=('Segoe UI', 10))
        cookies_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        cookies_btn = ttk.Button(cookies_frame, text="Parcourir", 
                                command=self.browse_cookies_file)
        cookies_btn.grid(row=0, column=1)
        
        row += 1
        
        # Cookies depuis navigateur
        ttk.Label(parent, text="Cookies depuis navigateur:", style='Heading.TLabel').grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=10)
        
        browser_combo = ttk.Combobox(parent, textvariable=self.cookies_browser, 
                                    values=["chrome", "edge", "firefox", "brave", "chromium", "opera", "vivaldi"], 
                                    state="readonly", font=('Segoe UI', 10))
        browser_combo.grid(row=row, column=1, sticky="w", padx=(0, 10), pady=10)
        
        row += 1
        
        # User-Agent
        ttk.Label(parent, text="User-Agent:", style='Heading.TLabel').grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=10)
        
        ua_entry = ttk.Entry(parent, textvariable=self.user_agent, font=('Segoe UI', 10))
        ua_entry.grid(row=row, column=1, sticky="ew", padx=(0, 10), pady=10)
        
        row += 1
        
        # Proxy
        ttk.Label(parent, text="Proxy:", style='Heading.TLabel').grid(
            row=row, column=0, sticky="w", padx=(0, 10), pady=10)
        
        proxy_entry = ttk.Entry(parent, textvariable=self.proxy, font=('Segoe UI', 10))
        proxy_entry.grid(row=row, column=1, sticky="ew", padx=(0, 10), pady=10)
        
        row += 1
        
        # Options de label avancées
        label_frame = ttk.LabelFrame(parent, text="Options de label avancées", padding=10)
        label_frame.grid(row=row, column=0, columnspan=2, sticky="ew", pady=20)
        label_frame.columnconfigure(1, weight=1)
        
        # Couleur du texte
        ttk.Label(label_frame, text="Couleur du texte:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        color_entry = ttk.Entry(label_frame, textvariable=self.label_color, font=('Segoe UI', 10))
        color_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        
        # Couleur de fond
        ttk.Label(label_frame, text="Couleur de fond:").grid(row=1, column=0, sticky="w", padx=(0, 10))
        bgcolor_entry = ttk.Entry(label_frame, textvariable=self.label_boxcolor, font=('Segoe UI', 10))
        bgcolor_entry.grid(row=1, column=1, sticky="ew", padx=(0, 10))
        
        # Épaisseur de la bordure
        ttk.Label(label_frame, text="Épaisseur bordure:").grid(row=2, column=0, sticky="w", padx=(0, 10))
        border_spin = ttk.Spinbox(label_frame, from_=0, to=50, textvariable=self.label_boxborderw, 
                                 width=10, font=('Segoe UI', 10))
        border_spin.grid(row=2, column=1, sticky="w", padx=(0, 10))
        
        # Rayon d'arrondi
        ttk.Label(label_frame, text="Rayon d'arrondi:").grid(row=3, column=0, sticky="w", padx=(0, 10))
        radius_spin = ttk.Spinbox(label_frame, from_=0, to=100, textvariable=self.label_radius, 
                                 width=10, font=('Segoe UI', 10))
        radius_spin.grid(row=3, column=1, sticky="w", padx=(0, 10))
        
        # Padding
        ttk.Label(label_frame, text="Padding:").grid(row=4, column=0, sticky="w", padx=(0, 10))
        padding_spin = ttk.Spinbox(label_frame, from_=5, to=50, textvariable=self.label_padding, 
                                  width=10, font=('Segoe UI', 10))
        padding_spin.grid(row=4, column=1, sticky="w", padx=(0, 10))
        
        # Afficher la boîte
        box_check = ttk.Checkbutton(label_frame, text="Afficher la boîte de fond", 
                                   variable=self.label_box)
        box_check.grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))
    
    def setup_logs_tab(self, parent):
        """Configure l'onglet des logs"""
        # Zone de logs
        log_frame = ttk.Frame(parent)
        log_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barre d'outils
        toolbar = ttk.Frame(log_frame)
        toolbar.pack(fill="x", pady=(0, 10))
        
        clear_btn = ttk.Button(toolbar, text="Effacer les logs", command=self.clear_logs)
        clear_btn.pack(side="left")
        
        save_btn = ttk.Button(toolbar, text="Sauvegarder les logs", command=self.save_logs)
        save_btn.pack(side="left", padx=(10, 0))
        
        # Zone de texte pour les logs
        self.log_text = scrolledtext.ScrolledText(log_frame, 
                                                 wrap=tk.WORD, 
                                                 font=('Consolas', 9),
                                                 height=20)
        self.log_text.pack(fill="both", expand=True)
        
        # Configuration des tags de couleur
        self.log_text.tag_configure("info", foreground="black")
        self.log_text.tag_configure("success", foreground="green")
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("error", foreground="red")
    
    def setup_bindings(self):
        """Configure les raccourcis clavier et événements"""
        # Raccourci Ctrl+Enter pour démarrer
        self.root.bind('<Control-Return>', lambda e: self.start_processing())
        
        # Raccourci Ctrl+Q pour quitter
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        
        # Mise à jour automatique du dossier des segments
        self.output_dir.trace('w', lambda *args: self.auto_segments_dir())
    
    def browse_output_dir(self):
        """Ouvre le dialogue pour choisir le dossier de sortie"""
        directory = filedialog.askdirectory(initialdir=self.output_dir.get())
        if directory:
            self.output_dir.set(directory)
    
    def browse_cookies_file(self):
        """Ouvre le dialogue pour choisir le fichier cookies"""
        filename = filedialog.askopenfilename(
            title="Sélectionner le fichier cookies",
            filetypes=[("Fichiers cookies", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        if filename:
            self.cookies_file.set(filename)
    
    def auto_segments_dir(self):
        """Met à jour automatiquement le dossier des segments"""
        output_dir = self.output_dir.get().strip()
        if output_dir:
            try:
                segments_path = Path(output_dir) / "segments"
                self.segments_dir.set(str(segments_path))
            except Exception:
                # En cas d'erreur, utiliser le dossier par défaut
                self.segments_dir.set(str(Path.cwd() / "outputs" / "segments"))
        else:
            # Si le dossier de sortie est vide, utiliser le dossier par défaut
            self.segments_dir.set(str(Path.cwd() / "outputs" / "segments"))
    
    def get_safe_int_value(self, int_var, default_value=0):
        """Récupère la valeur d'une variable IntVar de manière sécurisée"""
        try:
            value = int_var.get()
            if value is None or value == "":
                return default_value
            return int(value)
        except (ValueError, tk.TclError):
            return default_value
    
    def start_processing(self):
        """Démarre le traitement de la vidéo"""
        # Validation des champs obligatoires
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Erreur", "Veuillez saisir une URL YouTube")
            self.url_entry.focus()
            return
        
        output_dir = self.output_dir.get().strip()
        if not output_dir:
            messagebox.showerror("Erreur", "Veuillez spécifier un dossier de sortie")
            self.output_dir.focus()
            return
        
        # Validation de l'URL YouTube
        if not url.startswith(('http://', 'https://')) or 'youtube.com' not in url and 'youtu.be' not in url:
            messagebox.showerror("Erreur", "Veuillez saisir une URL YouTube valide")
            self.url_entry.focus()
            return
        
        # Validation du dossier de sortie
        try:
            output_path = Path(output_dir)
            if not output_path.exists():
                # Créer le dossier s'il n'existe pas
                output_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le dossier de sortie : {str(e)}")
            return
        
        # Désactiver l'interface
        self.is_processing = True
        self.process_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_var.set("Traitement en cours...")
        
        # Construire les arguments CLI
        try:
            args = self.build_cli_args()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la construction des arguments : {str(e)}")
            self.processing_finished()
            return
        
        # Démarrer le traitement dans un thread séparé
        self.processing_thread = threading.Thread(target=self.run_cli, args=(args,))
        self.processing_thread.daemon = True
        self.processing_thread.start()
    
    def stop_processing(self):
        """Arrête le traitement en cours"""
        # Arrêt immédiat
        self.is_processing = False
        self.status_var.set("Arrêt en cours...")
        
        # Réactiver immédiatement l'interface
        self.process_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        
        # Envoyer un message de log
        self.log_queue.put(("warning", "Arrêt demandé par l'utilisateur"))
        
        # Essayer d'interrompre le thread de traitement
        if hasattr(self, 'processing_thread') and self.processing_thread.is_alive():
            try:
                # Marquer le thread comme non-daemon pour permettre l'arrêt
                self.processing_thread.daemon = False
                
                # Essayer d'interrompre le processus CLI si possible
                self.force_stop_cli()
                
                self.log_queue.put(("info", "Thread de traitement marqué pour arrêt"))
            except Exception as e:
                self.log_queue.put(("error", f"Erreur lors de l'arrêt: {str(e)}"))
        
        # Mettre à jour le statut final
        self.root.after(100, lambda: self.status_var.set("Arrêt effectué"))
    
    def force_stop_cli(self):
        """Essaie de forcer l'arrêt du processus CLI"""
        try:
            # Importer os pour la gestion des processus
            import os
            import signal
            
            # Sur Windows, on ne peut pas envoyer de signal SIGTERM
            # mais on peut essayer d'interrompre le processus principal
            if os.name == 'nt':  # Windows
                # Essayer d'interrompre le processus Python en cours
                try:
                    # Envoyer un signal d'interruption (Ctrl+C équivalent)
                    os.kill(os.getpid(), signal.CTRL_C_EVENT)
                    self.log_queue.put(("info", "Signal d'interruption envoyé au processus"))
                except:
                    # Si ça ne marche pas, on note juste
                    self.log_queue.put(("info", "Arrêt demandé (Windows - arrêt progressif)"))
            else:
                # Sur Unix/Linux, on peut envoyer SIGTERM
                try:
                    os.kill(os.getpid(), signal.SIGTERM)
                    self.log_queue.put(("info", "Signal SIGTERM envoyé au processus"))
                except:
                    self.log_queue.put(("info", "Arrêt demandé (Unix - arrêt progressif)"))
                    
        except Exception as e:
            self.log_queue.put(("warning", f"Impossible de forcer l'arrêt: {str(e)}"))
            self.log_queue.put(("info", "L'arrêt se fera progressivement"))
    
    def build_cli_args(self):
        """Construit la liste d'arguments pour la CLI"""
        args = [self.url_entry.get().strip()]
        
        # Dossier de sortie
        if self.output_dir.get():
            args.extend(["--output", self.output_dir.get()])
        
        # Dossier des segments
        if self.segments_dir.get():
            args.extend(["--segments-dir", self.segments_dir.get()])
        
        # Limite de segments - vérifier que la valeur n'est pas vide
        limit_value = self.get_safe_int_value(self.limit_segments, 0)
        if limit_value > 0:
            args.extend(["--limit", str(limit_value)])
        
        # Durée des segments
        segment_seconds = self.get_safe_int_value(self.segment_seconds, 60)
        args.extend(["--segment-seconds", str(segment_seconds)])
        
        # Cookies
        if self.cookies_file.get():
            args.extend(["--cookies", self.cookies_file.get()])
        
        if self.cookies_browser.get():
            args.extend(["--cookies-from-browser", self.cookies_browser.get()])
        
        # User-Agent
        if self.user_agent.get():
            args.extend(["--user-agent", self.user_agent.get()])
        
        # Proxy
        if self.proxy.get():
            args.extend(["--proxy", self.proxy.get()])
        
        # Options de label
        if self.add_label.get():
            args.append("--label")
            
            if self.label_template.get() != "Partie {i}":
                args.extend(["--label-template", self.label_template.get()])
            
            label_fontsize = self.get_safe_int_value(self.label_fontsize, 54)
            if label_fontsize != 54:
                args.extend(["--label-fontsize", str(label_fontsize)])
            
            if self.label_color.get() != "black":
                args.extend(["--label-color", self.label_color.get()])
            
            if self.label_position.get() != "tc":
                args.extend(["--label-position", self.label_position.get()])
            
            if self.label_boxcolor.get() != "white":
                args.extend(["--label-boxcolor", self.label_boxcolor.get()])
            
            label_boxborderw = self.get_safe_int_value(self.label_boxborderw, 14)
            if label_boxborderw != 14:
                args.extend(["--label-boxborderw", str(label_boxborderw)])
            
            if self.label_rounded.get():
                args.append("--label-rounded")
                
                label_radius = self.get_safe_int_value(self.label_radius, 24)
                if label_radius != 24:
                    args.extend(["--label-radius", str(label_radius)])
                
                label_padding = self.get_safe_int_value(self.label_padding, 18)
                if label_padding != 18:
                    args.extend(["--label-padding", str(label_padding)])
            
            if not self.label_box.get():
                args.append("--no-label-box")
        
        return args
    
    def run_cli(self, args):
        """Exécute la CLI dans un thread séparé"""
        try:
            # Envoyer un message de début
            self.log_queue.put(("info", f"Démarrage du traitement avec les arguments: {' '.join(args)}"))
            
            # Vérifier si l'arrêt a été demandé avant de commencer
            if not self.is_processing:
                self.log_queue.put(("warning", "Traitement annulé avant démarrage"))
                return
            
            # Rediriger stdout/stderr pour capturer les logs
            import io
            import contextlib
            
            # Capturer la sortie
            output = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                # Parser les arguments et exécuter
                parsed_args = parse_args(args)
                
                # Vérifier à nouveau si l'arrêt a été demandé
                if not self.is_processing:
                    self.log_queue.put(("warning", "Traitement annulé après parsing des arguments"))
                    return
                
                result = cli_main(args)
            
            # Vérifier si l'arrêt a été demandé pendant le traitement
            if not self.is_processing:
                self.log_queue.put(("warning", "Traitement interrompu par l'utilisateur"))
                return
            
            # Récupérer la sortie capturée
            output_text = output.getvalue()
            if output_text.strip():
                # Envoyer les logs capturés ligne par ligne
                for line in output_text.strip().split('\n'):
                    if line.strip():
                        if 'error' in line.lower() or 'erreur' in line.lower():
                            self.log_queue.put(("error", line.strip()))
                        elif 'warning' in line.lower() or 'attention' in line.lower():
                            self.log_queue.put(("warning", line.strip()))
                        else:
                            self.log_queue.put(("info", line.strip()))
            
            # Envoyer le message de succès seulement si pas d'arrêt
            if self.is_processing:
                self.log_queue.put(("success", f"Traitement terminé avec succès (code: {result})"))
            
        except Exception as e:
            # Vérifier si l'arrêt a été demandé
            if not self.is_processing:
                self.log_queue.put(("warning", "Traitement interrompu par l'utilisateur"))
                return
                
            error_msg = f"Erreur lors du traitement: {str(e)}"
            self.log_queue.put(("error", error_msg))
            
            # Log détaillé de l'erreur pour le débogage
            import traceback
            traceback_text = traceback.format_exc()
            for line in traceback_text.strip().split('\n'):
                if line.strip():
                    self.log_queue.put(("error", line.strip()))
        
        finally:
            # Réactiver l'interface
            self.root.after(0, self.processing_finished)
    
    def processing_finished(self):
        """Appelé quand le traitement est terminé"""
        self.is_processing = False
        self.process_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        
        # Déterminer le statut final
        if hasattr(self, 'processing_thread') and self.processing_thread.is_alive():
            # Le thread est encore en cours, c'est probablement un arrêt
            self.status_var.set("Arrêt effectué")
            # Marquer le thread comme terminé
            self.processing_thread = None
        else:
            # Traitement normal terminé
            self.status_var.set("Prêt")
    
    def check_log_queue(self):
        """Vérifie la queue de logs et met à jour l'interface"""
        try:
            while True:
                log_type, message = self.log_queue.get_nowait()
                
                # Ajouter le log à l'interface
                self.log_text.insert(tk.END, f"{message}\n", log_type)
                self.log_text.see(tk.END)
                
                # Mettre à jour le statut
                if log_type == "success":
                    self.status_var.set("Traitement terminé avec succès")
                elif log_type == "error":
                    self.status_var.set("Erreur lors du traitement")
                elif log_type == "warning" and "interrompu" in message.lower():
                    self.status_var.set("Traitement interrompu")
                
        except queue.Empty:
            pass
        
        # Vérifier si l'arrêt a été demandé et mettre à jour l'interface
        if not self.is_processing and self.process_btn.cget("state") == "disabled":
            # Réactiver l'interface si elle n'est pas déjà réactivée
            self.root.after(0, self.processing_finished)
        
        # Vérifier à nouveau dans 50ms (plus rapide pour une meilleure réactivité)
        self.root.after(50, self.check_log_queue)
    
    def clear_logs(self):
        """Efface tous les logs"""
        self.log_text.delete(1.0, tk.END)
    
    def save_logs(self):
        """Sauvegarde les logs dans un fichier"""
        filename = filedialog.asksaveasfilename(
            title="Sauvegarder les logs",
            defaultextension=".txt",
            filetypes=[("Fichiers texte", "*.txt"), ("Tous les fichiers", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, tk.END))
                messagebox.showinfo("Succès", "Logs sauvegardés avec succès")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de sauvegarder les logs: {str(e)}")


def main():
    """Point d'entrée principal de l'application"""
    root = tk.Tk()
    
    # Configuration de l'icône (si disponible)
    try:
        # Essayer de charger une icône
        root.iconbitmap(default="icon.ico")
    except:
        pass
    
    app = ModernTkinterApp(root)
    
    # Centrer la fenêtre
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Démarrer la boucle principale
    root.mainloop()


if __name__ == "__main__":
    main()
