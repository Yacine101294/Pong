import tkinter as tk
from tkinter import scrolledtext
import queue
import threading
import logging
import time
import sys

class QueueHandler(logging.Handler):
    """Gestionnaire de logging qui place les logs dans une queue pour l'interface Tkinter"""
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)

class LogWindow:
    """Fenêtre d'affichage des logs en temps réel"""
    def __init__(self, title="Logs Pong"):
        # Flag pour indiquer si la fenêtre est active
        self.running = True
        
        # Créer la fenêtre principale
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configurer la fenêtre pour qu'elle apparaisse derrière les autres
        self.root.attributes('-topmost', False)
        self.root.lower()  # Mettre la fenêtre en arrière-plan
        
        # Configurer les couleurs de fond et de texte
        bg_color = "black"
        fg_color = "white"
        self.root.configure(bg=bg_color)
        
        # Créer une zone de texte défilante pour les logs
        self.log_area = scrolledtext.ScrolledText(self.root, width=95, height=35, bg=bg_color, fg=fg_color)
        self.log_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Configurer les styles de texte pour différents niveaux de log
        self.log_area.tag_config("INFO", foreground="white")
        self.log_area.tag_config("DEBUG", foreground="gray")
        self.log_area.tag_config("WARNING", foreground="orange")
        self.log_area.tag_config("ERROR", foreground="red")
        self.log_area.tag_config("CRITICAL", foreground="red", background="yellow")
        
        # Configurer les styles pour différents types d'événements
        self.log_area.tag_config("JOUEUR", foreground="cyan")
        self.log_area.tag_config("IA", foreground="green")
        self.log_area.tag_config("COLLISION", foreground="magenta")
        self.log_area.tag_config("POINT", foreground="yellow")
        self.log_area.tag_config("INPUT", foreground="orange")
        
        # File d'attente pour recevoir les logs
        self.log_queue = queue.Queue()
        
        # Configurer le gestionnaire de logs pour notre queue
        self.queue_handler = QueueHandler(self.log_queue)
        self.queue_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.queue_handler.setFormatter(formatter)
        
        # Désactiver l'édition du widget
        self.log_area.config(state='disabled')
        
        # Message initial
        self.add_message("Fenêtre de logs Pong initialisée. Les logs en temps réel apparaîtront ici.", ["INFO"])
        
        # Démarrer la vérification périodique des nouveaux logs
        self.check_queue()
    
    def add_message(self, message, tags):
        """Ajoute un message directement dans la zone de texte"""
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"{message}\n", tags)
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')
        
    def check_queue(self):
        """Vérifie périodiquement s'il y a de nouveaux logs dans la queue"""
        if not self.running:
            return
            
        while True:
            try:
                # Récupérer un record sans bloquer
                record = self.log_queue.get_nowait()
                
                # Activer l'édition temporairement
                self.log_area.config(state='normal')
                
                # Déterminer le tag à utiliser
                tags = [record.levelname]  # Tag de base pour le niveau de log
                
                # Ajouter des tags spécifiques basés sur le contenu du message
                message = record.getMessage()
                if "JOUEUR:" in message:
                    tags.append("JOUEUR")
                elif "IA:" in message:
                    tags.append("IA")
                elif "COLLISION:" in message:
                    tags.append("COLLISION")
                elif "POINT:" in message:
                    tags.append("POINT")
                elif "INPUT:" in message:
                    tags.append("INPUT")
                
                # Ajouter le message formaté avec les tags appropriés
                formatted_message = self.queue_handler.format(record) + "\n"
                self.log_area.insert(tk.END, formatted_message, tags)
                
                # Faire défiler automatiquement vers le bas
                self.log_area.see(tk.END)
                
                # Désactiver l'édition
                self.log_area.config(state='disabled')
                
                # Marquer comme traité
                self.log_queue.task_done()
            except queue.Empty:
                break
        
        # Vérifier à nouveau après 100ms
        self.root.after(100, self.check_queue)
    
    def on_closing(self):
        """Gestionnaire pour la fermeture de la fenêtre"""
        self.running = False
        self.root.destroy()
    
    def run(self):
        """Démarre la boucle principale de la fenêtre"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"Erreur dans la boucle principale de la fenêtre de logs: {e}")
            sys.stderr.write(f"Erreur dans la fenêtre de logs: {e}\n")
    
    def get_handler(self):
        """Renvoie le gestionnaire de logs pour l'intégration avec le système de logging"""
        return self.queue_handler

# Variable globale pour la fenêtre de logs
_log_window = None

def start_log_window():
    """Démarre la fenêtre de logs dans un thread séparé"""
    global _log_window
    
    if _log_window is not None:
        return _log_window
    
    # Créer une queue pour communiquer entre les threads
    log_queue = queue.Queue()
    
    def run_log_window():
        global _log_window
        try:
            _log_window = LogWindow()
            _log_window.run()
        except Exception as e:
            print(f"Erreur lors du démarrage de la fenêtre de logs: {e}")
            sys.stderr.write(f"Erreur de la fenêtre de logs: {e}\n")
    
    # Démarrer la fenêtre dans un thread séparé
    log_thread = threading.Thread(target=run_log_window)
    log_thread.daemon = True
    log_thread.start()
    
    # Attendre un peu pour que la fenêtre soit créée
    time.sleep(0.5)
    
    # S'assurer que la fenêtre a été créée
    attempts = 0
    while _log_window is None and attempts < 10:
        time.sleep(0.2)
        attempts += 1
    
    return _log_window 