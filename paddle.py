# Classe pour les raquettes du jeu Pong
import pygame
from constants import *
"""window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Pong game")


go = True
while go:
    for event in pygame.event.get():
        pygame.display.flip()"""

import random
import logging

# Récupérer le logger
logger = logging.getLogger("PongGame")

class Paddle:
    def __init__(self, x, y, largeur=RAQUETTE_LARGEUR, hauteur=RAQUETTE_HAUTEUR, vitesse=RAQUETTE_VITESSE, is_ai=False):  # Initialisation de la raquette avec position et dimensions
        self.rect = pygame.Rect(x, y, largeur, hauteur)  # Création du rectangle de la raquette
        self.couleur = RAQUETTE_COULEUR  # Définition de la couleur
        self.vitesse = vitesse  # Vitesse de déplacement
        self.direction = 0  # 0: immobile, -1: vers le haut, 1: vers le bas
        self.is_ai = is_ai  # Indique si la raquette est contrôlée par l'IA
        if is_ai:
            logger.info(f"IA: Raquette IA initialisée à la position ({x}, {y})")
    
    def move_up(self):  # Méthode pour monter
        """Déplace la raquette vers le haut"""
        self.direction = -1  # Change la direction vers le haut
    
    def move_down(self):  # Méthode pour descendre
        """Déplace la raquette vers le bas"""
        self.direction = 1  # Change la direction vers le bas
    
    def stop(self):  # Méthode pour arrêter
        """Arrête le mouvement de la raquette"""
        self.direction = 0  # Arrête le mouvement
    
    def update(self):  # Mise à jour de la position
        """Met à jour la position de la raquette"""
        old_y = self.rect.y
        self.rect.y += self.direction * self.vitesse  # Calcul du nouveau déplacement
        
        # Empêche la raquette de sortir de l'écran
        if self.rect.top < 0:  # Collision avec le haut
            self.rect.top = 0
            if self.is_ai:
                logger.debug("IA: Raquette IA bloquée par le bord supérieur")
        if self.rect.bottom > WINDOW_HEIGHT:  # Collision avec le bas
            self.rect.bottom = WINDOW_HEIGHT
            if self.is_ai:
                logger.debug("IA: Raquette IA bloquée par le bord inférieur")
        
    def ai_move(self, ball):
        """Déplace la raquette IA pour suivre la balle"""
        # IA simple: suivre la balle
        # Ajout d'un petit délai/imprécision pour que l'IA ne soit pas parfaite
        target_y = ball.taille.centery
        
        # Ajouter une petite erreur aléatoire pour rendre l'IA plus humaine
        error = random.randint(-30, 30)
        target_y += error
        
        # Décider si on monte ou descend
        old_direction = self.direction
        
        if self.rect.centery < target_y:
            self.move_down()
            if old_direction != 1:
                logger.debug(f"IA: Décision de descendre, cible: {target_y}, position: {self.rect.centery}, erreur: {error}")
        elif self.rect.centery > target_y:
            self.move_up()
            if old_direction != -1:
                logger.debug(f"IA: Décision de monter, cible: {target_y}, position: {self.rect.centery}, erreur: {error}")
        else:
            self.stop()
            if old_direction != 0:
                logger.debug(f"IA: Décision de s'arrêter, cible: {target_y}, position: {self.rect.centery}")
    
    def draw(self, screen):  # Méthode de dessin
        """Dessine la raquette sur l'écran"""
        pygame.draw.rect(screen, self.couleur, self.rect)  # Dessine le rectangle
        
