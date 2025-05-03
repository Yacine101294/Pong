# Logique principale du jeu Pong
import pygame
from constants import *
from paddle import Paddle
from ball import Ball
import logging
import os
import datetime
from log_window import start_log_window


pygame.init()

# Configuration du logging
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(log_dir, f"pong_game_{timestamp}.log")

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # Affiche également dans la console
    ]
)
logger = logging.getLogger("PongGame")

# Démarrer la fenêtre de logs
log_window = start_log_window()
logger.addHandler(log_window.get_handler())

class Game:
    """Classe qui gère la logique du jeu Pong"""
    def __init__(self):
        # Création de la fenêtre de jeu
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Pong")
        
        # Horloge pour contrôler le FPS
        self.clock = pygame.time.Clock()
        
        # État du jeu
        self.running = True
        
        # Score des joueurs
        self.score_left = 0
        self.score_right = 0
        
        # Police pour l'affichage du score
        self.font = pygame.font.Font(None, 74)  # Taille 74 pour un grand score visible
        
        # Initialisation des raquettes
        self.paddle_left = Paddle(
            RAQUETTE_MARGE,                                 # Position X de la raquette gauche
            WINDOW_HEIGHT // 2 - RAQUETTE_HAUTEUR // 2      # Position Y centrée verticalement
        )
        
        self.paddle_right = Paddle(
            WINDOW_WIDTH - RAQUETTE_LARGEUR - RAQUETTE_MARGE,   # Position X de la raquette droite
            WINDOW_HEIGHT // 2 - RAQUETTE_HAUTEUR // 2,         # Position Y centrée verticalement
            is_ai=True                                          # Raquette contrôlée par l'IA
        )
        
        # Initialisation de la balle
        self.ball = Ball(
            WINDOW_WIDTH // 2 - BALLE_TAILLE // 2,       # Position X centrée horizontalement
            WINDOW_HEIGHT // 2 - BALLE_TAILLE // 2       # Position Y centrée verticalement
        )
        
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
        
        # Mettre à jour l'affichage
        pygame.display.flip()
    
    def update(self):
        """Met à jour l'état du jeu"""
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
        
        # Détecter si un point a été marqué
        point = self.ball.detecter_point()
        if point == "gauche":
            self.score_left += 1
            logger.info(f"POINT: Joueur gauche marque un point! Score: {self.score_left}-{self.score_right}")
            self.ball.reinitialiser(WINDOW_WIDTH // 2 - BALLE_TAILLE // 2, WINDOW_HEIGHT // 2 - BALLE_TAILLE // 2)
        elif point == "droite":
            self.score_right += 1
            logger.info(f"POINT: Joueur droite (IA) marque un point! Score: {self.score_left}-{self.score_right}")
            self.ball.reinitialiser(WINDOW_WIDTH // 2 - BALLE_TAILLE // 2, WINDOW_HEIGHT // 2 - BALLE_TAILLE // 2)
        
    def handle_input(self):
        """Gestion des entrées"""
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
        
        # L'IA contrôle la raquette droite
        # self.paddle_right.ai_move(self.ball) # À implémenter si nécessaire
    
    
    