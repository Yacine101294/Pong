# Logique principale du jeu Pong
import pygame
from constants import *
from paddle import Paddle
from ball import Ball
import logging
import os
import datetime
import time
from log_window import start_log_window
from buttons import Button


pygame.init()

# Configuration du logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_dir, f"pong_game_{timestamp}.log")

# Configuration du logger pour qu'il écrive uniquement dans un fichier (pas dans la console)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file)
        # Suppression du StreamHandler pour ne plus afficher les logs dans le terminal
    ]
)
logger = logging.getLogger("PongGame")

# Démarrer la fenêtre de logs
print("Démarrage du jeu Pong avec système de logs...")
log_window = start_log_window()

# S'assurer que la fenêtre de logs est initialisée avant de continuer
if log_window:
    logger.addHandler(log_window.get_handler())
    # Pas de message dans la console
else:
    print("Attention: La fenêtre de logs n'a pas pu être initialisée correctement.")

class Game:
    """Classe qui gère la logique du jeu Pong"""
    def __init__(self, niveau_ia=NIVEAU_IA_DEFAUT):
        # Création de la fenêtre de jeu
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        
        # Horloge pour contrôler le FPS
        self.clock = pygame.time.Clock()
        
        # État du jeu
        self.running = True
        self.paused = False
        
        # Score des joueurs
        self.score_left = 0
        self.score_right = 0
        
        # Police pour l'affichage du score
        self.font = pygame.font.Font(None, 74)  # Taille 74 pour un grand score visible
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        
        # Initialisation des raquettes
        self.paddle_left = Paddle(
            RAQUETTE_MARGE,                                 # Position X de la raquette gauche
            WINDOW_HEIGHT // 2 - RAQUETTE_HAUTEUR // 2      # Position Y centrée verticalement
        )
        
        self.paddle_right = Paddle(
            WINDOW_WIDTH - RAQUETTE_LARGEUR - RAQUETTE_MARGE,   # Position X de la raquette droite
            WINDOW_HEIGHT // 2 - RAQUETTE_HAUTEUR // 2,         # Position Y centrée verticalement
            is_ai=True,                                         # Raquette contrôlée par l'IA
            niveau_ia=niveau_ia                                 # Niveau de difficulté
        )
        
        # Initialisation de la balle
        self.ball = Ball(
            WINDOW_WIDTH // 2 - BALLE_TAILLE // 2,       # Position X centrée horizontalement
            WINDOW_HEIGHT // 2 - BALLE_TAILLE // 2       # Position Y centrée verticalement
        )
        
        # Initialiser la vitesse des raquettes en fonction de la vitesse de la balle
        vitesse_balle = self.ball.get_vitesse_actuelle()
        self.paddle_left.ajuster_vitesse(vitesse_balle)
        self.paddle_right.ajuster_vitesse(vitesse_balle)
        logger.info(f"INIT: Vitesse initiale de la balle: {vitesse_balle:.1f}, vitesses des raquettes ajustées")
        
        # Boutons pour le menu pause
        self.btn_continuer = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 40, 200, 50, "CONTINUER")
        self.btn_quitter = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 40, 200, 50, "QUITTER")
        
        logger.info("Jeu initialisé avec succès")
        logger.info(f"Taille de l'écran: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        logger.info(f"Position initiale raquette gauche: {self.paddle_left.rect}")
        logger.info(f"Position initiale raquette droite: {self.paddle_right.rect}")
        logger.info(f"Position initiale balle: {self.ball.taille}")
    
    def draw_score(self):
        """Dessine le score sur l'écran, dans le camp respectif de chaque joueur"""
        # Score du joueur gauche
        score_left_text = self.font.render(str(self.score_left), True, BLANC)
        score_left_rect = score_left_text.get_rect()
        score_left_rect.centerx = WINDOW_WIDTH // 4  # À 1/4 de l'écran (camp gauche)
        score_left_rect.top = 20  # 20 pixels du haut de l'écran
        
        # Score du joueur droit
        score_right_text = self.font.render(str(self.score_right), True, BLANC)
        score_right_rect = score_right_text.get_rect()
        score_right_rect.centerx = WINDOW_WIDTH * 3 // 4  # À 3/4 de l'écran (camp droit)
        score_right_rect.top = 20  # 20 pixels du haut de l'écran
        
        # Dessiner les scores sur l'écran
        self.screen.blit(score_left_text, score_left_rect)
        self.screen.blit(score_right_text, score_right_rect)
    
    def draw(self):
        """Dessine tous les éléments du jeu sur l'écran"""
        # Effacer l'écran
        self.screen.fill(NOIR)
        
        # Dessiner la ligne centrale (séparation des camps)
        pygame.draw.aaline(self.screen, GRIS, 
                          (WINDOW_WIDTH // 2, 0), 
                          (WINDOW_WIDTH // 2, WINDOW_HEIGHT))
        
        # Dessiner le score
        self.draw_score()
        
        # Dessiner les raquettes
        self.paddle_left.draw(self.screen)
        self.paddle_right.draw(self.screen)
        
        # Dessiner la balle
        self.ball.dessiner_balle(self.screen)
        
        # Si le jeu est en pause, afficher le menu pause
        if self.paused:
            self.draw_pause_menu()
        
        # Mettre à jour l'affichage
        pygame.display.flip()
    
    def draw_pause_menu(self):
        """Dessine le menu pause"""
        # Fond semi-transparent
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Noir avec 70% d'opacité
        self.screen.blit(overlay, (0, 0))
        
        # Titre du menu pause
        pause_text = self.font_medium.render("PAUSE", True, BLANC)
        pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
        self.screen.blit(pause_text, pause_rect)
        
        # Instructions
        instr_text = self.font_small.render("Appuyez sur ÉCHAP pour reprendre", True, GRIS)
        instr_rect = instr_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4 + 50))
        self.screen.blit(instr_text, instr_rect)
        
        # Dessiner les boutons
        self.btn_continuer.draw(self.screen)
        self.btn_quitter.draw(self.screen)
    
    def update(self):
        """Met à jour l'état du jeu"""
        # Si le jeu est en pause, ne pas mettre à jour la logique
        if self.paused:
            return
            
        # Position avant mise à jour
        prev_paddle_left_pos = self.paddle_left.rect.y
        prev_paddle_right_pos = self.paddle_right.rect.y
        prev_ball_pos = (self.ball.taille.x, self.ball.taille.y)
        
        # Mettre à jour la position des raquettes
        self.paddle_left.update()
        
        # Mettre à jour la position de la raquette IA
        if self.paddle_right.is_ai:
            self.paddle_right.ai_move(self.ball)
        self.paddle_right.update()
        
        # Mettre à jour la position de la balle
        self.ball.deplacer()
        
        # Journaliser les déplacements
        if prev_paddle_left_pos != self.paddle_left.rect.y:
            logger.info(f"JOUEUR: Raquette gauche déplacée de {prev_paddle_left_pos} à {self.paddle_left.rect.y}")
        
        if prev_paddle_right_pos != self.paddle_right.rect.y:
            logger.info(f"IA: Raquette droite déplacée de {prev_paddle_right_pos} à {self.paddle_right.rect.y}")
        
        if prev_ball_pos != (self.ball.taille.x, self.ball.taille.y):
            logger.debug(f"BALLE: Déplacée de {prev_ball_pos} à ({self.ball.taille.x}, {self.ball.taille.y})")
        
        # Détecter les collisions avec les murs
        if self.ball.detecter_collision_murs():
            logger.info(f"COLLISION: Balle a rebondi sur un mur à la position ({self.ball.taille.x}, {self.ball.taille.y})")
        
        # Détecter les collisions avec les raquettes
        if self.ball.detecter_collision_raquettes(self.paddle_left, self.paddle_right):
            logger.info(f"COLLISION: Balle a rebondi sur une raquette à la position ({self.ball.taille.x}, {self.ball.taille.y})")
            
            # Ajuster la vitesse des raquettes en fonction de la vitesse de la balle
            vitesse_balle = self.ball.get_vitesse_actuelle()
            self.paddle_left.ajuster_vitesse(vitesse_balle)
            self.paddle_right.ajuster_vitesse(vitesse_balle)
            logger.info(f"VITESSE: Balle accélérée à {vitesse_balle:.1f}, vitesses raquettes ajustées")
        
        # Détecter si un point a été marqué
        point = self.ball.detecter_point()
        if point == "gauche":
            self.score_left += 1
            logger.info(f"POINT: Joueur gauche marque un point! Score: {self.score_left}-{self.score_right}")
            self.ball.reinitialiser(WINDOW_WIDTH // 2 - BALLE_TAILLE // 2, WINDOW_HEIGHT // 2 - BALLE_TAILLE // 2)
            
            # Réinitialiser la vitesse des raquettes car la balle est réinitialisée
            self.paddle_left.ajuster_vitesse(self.ball.get_vitesse_actuelle())
            self.paddle_right.ajuster_vitesse(self.ball.get_vitesse_actuelle())
            
        elif point == "droite":
            self.score_right += 1
            logger.info(f"POINT: Joueur droite (IA) marque un point! Score: {self.score_left}-{self.score_right}")
            self.ball.reinitialiser(WINDOW_WIDTH // 2 - BALLE_TAILLE // 2, WINDOW_HEIGHT // 2 - BALLE_TAILLE // 2)
            
            # Réinitialiser la vitesse des raquettes car la balle est réinitialisée
            self.paddle_left.ajuster_vitesse(self.ball.get_vitesse_actuelle())
            self.paddle_right.ajuster_vitesse(self.ball.get_vitesse_actuelle())
    
    def handle_input(self):
        """Gestion des entrées"""
        # Récupérer tous les événements
        events = pygame.event.get()
        
        # Traiter les événements
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                    if self.paused:
                        logger.info("PAUSE: Jeu mis en pause")
                    else:
                        logger.info("PAUSE: Jeu repris")
            
            # Si le jeu est en pause, vérifier les clics sur les boutons
            if self.paused and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Mise à jour de l'état des boutons
                self.btn_continuer.update(mouse_pos, True)
                self.btn_quitter.update(mouse_pos, True)
                
                # Vérifier si le bouton Continuer est cliqué
                if self.btn_continuer.is_clicked():
                    self.paused = False
                    logger.info("PAUSE: Jeu repris (via bouton)")
                
                # Vérifier si le bouton Quitter est cliqué
                if self.btn_quitter.is_clicked():
                    self.running = False
                    logger.info("PAUSE: Jeu quitté (via bouton)")
        
        # Si le jeu est en pause, ne pas traiter les autres entrées
        if self.paused:
            return
        
        # Lire l'état actuel du clavier
        keys = pygame.key.get_pressed()
        old_direction = self.paddle_left.direction
        
        # Contrôle du joueur 1 (raquette gauche)
        if keys[pygame.K_UP]:
            self.paddle_left.move_up()
            if old_direction != -1:
                logger.info("INPUT: Joueur appuie sur la touche HAUT")
        elif keys[pygame.K_DOWN]:
            self.paddle_left.move_down()
            if old_direction != 1:
                logger.info("INPUT: Joueur appuie sur la touche BAS")
        else:
            self.paddle_left.stop()
            if old_direction != 0:
                logger.info("INPUT: Joueur relâche les touches directionnelles")
    
    def set_niveau_ia(self, niveau_ia):
        """Change le niveau de difficulté de l'IA"""
        return self.paddle_right.set_niveau_ia(niveau_ia)
    
    
    