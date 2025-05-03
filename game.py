# Logique principale du jeu Pong
import pygame
from constants import *
from paddle import Paddle
from ball import Ball


pygame.init()

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
        self.paddle_left = pygame.Rect(
            RAQUETTE_MARGE,                                 # Position X de la raquette gauche
            WINDOW_HEIGHT // 2 - RAQUETTE_HAUTEUR // 2,     # Position Y centrée verticalement
            RAQUETTE_LARGEUR,                               # Largeur de la raquette
            RAQUETTE_HAUTEUR                                # Hauteur de la raquette
        )
        
        self.paddle_right = pygame.Rect(
            WINDOW_WIDTH - RAQUETTE_LARGEUR - RAQUETTE_MARGE,   # Position X de la raquette droite
            WINDOW_HEIGHT // 2 - RAQUETTE_HAUTEUR // 2,         # Position Y centrée verticalement
            RAQUETTE_LARGEUR,                                   # Largeur de la raquette
            RAQUETTE_HAUTEUR                                    # Hauteur de la raquette
        )
        
        # Initialisation de la balle
        self.ball = pygame.Rect(
            WINDOW_WIDTH // 2 - BALLE_TAILLE // 2,       # Position X centrée horizontalement
            WINDOW_HEIGHT // 2 - BALLE_TAILLE // 2,      # Position Y centrée verticalement
            BALLE_TAILLE,                                # Largeur de la balle
            BALLE_TAILLE                                 # Hauteur de la balle (carrée)
        )
        
        # Vitesse initiale de la balle
        self.ball_speed_x = BALLE_VITESSE_INITIALE        # Vitesse horizontale initiale
        self.ball_speed_y = BALLE_VITESSE_INITIALE        # Vitesse verticale initiale
    
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
        pygame.draw.rect(self.screen, BLANC, self.paddle_left)
        pygame.draw.rect(self.screen, BLANC, self.paddle_right)
        
        # Dessiner la balle
        pygame.draw.rect(self.screen, BLANC, self.ball)
        
        # Mettre à jour l'affichage
        pygame.display.flip()
        
    
    def handle_input(self):
        """Gestion des entrées"""
        keys = pygame.key.get_pressed()
        
        #Contole du joueur 1
        if keys[pygame.K_UP]:
            self.paddle_left.move_up()
        elif keys[pygame.K_DOWN]:
            self.paddle_right.move_down()
        else:
            self.paddle_left.stop()
            
        
        
    
    
    