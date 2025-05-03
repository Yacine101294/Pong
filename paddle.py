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
    def __init__(self, x, y, largeur=RAQUETTE_LARGEUR, hauteur=RAQUETTE_HAUTEUR, vitesse=RAQUETTE_VITESSE, is_ai=False, niveau_ia=NIVEAU_IA_DEFAUT):  # Initialisation de la raquette avec position et dimensions
        self.rect = pygame.Rect(x, y, largeur, hauteur)  # Création du rectangle de la raquette
        self.couleur = RAQUETTE_COULEUR  # Définition de la couleur
        self.vitesse_base = vitesse  # Vitesse de base de déplacement
        self.vitesse = vitesse  # Vitesse actuelle de déplacement
        self.direction = 0  # 0: immobile, -1: vers le haut, 1: vers le bas
        self.is_ai = is_ai  # Indique si la raquette est contrôlée par l'IA
        
        # Paramètres de l'IA
        self.niveau_ia = niveau_ia
        
        if is_ai:
            logger.info(f"IA: Raquette IA initialisée à la position ({x}, {y})")
            logger.info(f"IA: Niveau défini - Vitesse: {niveau_ia['VITESSE']}, Précision: {niveau_ia['PRECISION']}, Réaction: {niveau_ia['REACTION']}")
            # La vitesse de l'IA remplace la vitesse par défaut
            self.vitesse_base = niveau_ia['VITESSE']
            self.vitesse = self.vitesse_base
    
    def move_up(self):  # Méthode pour monter
        """Déplace la raquette vers le haut"""
        self.direction = -1  # Change la direction vers le haut
    
    def move_down(self):  # Méthode pour descendre
        """Déplace la raquette vers le bas"""
        self.direction = 1  # Change la direction vers le bas
    
    def stop(self):  # Méthode pour arrêter
        """Arrête le mouvement de la raquette"""
        self.direction = 0  # Arrête le mouvement
    
    def ajuster_vitesse(self, vitesse_balle):
        """Ajuste la vitesse de la raquette en fonction de la vitesse de la balle"""
        # Calculer un facteur d'ajustement basé sur la vitesse de la balle
        # Plus la balle va vite, plus les raquettes sont rapides
        facteur = vitesse_balle / BALLE_VITESSE_INITIALE
        facteur = max(1.0, min(facteur, FACTEUR_VITESSE_MAX))  # Limiter le facteur
        
        # Mettre à jour la vitesse
        vitesse_ajustee = self.vitesse_base * facteur
        
        # Appliquer la nouvelle vitesse
        if self.is_ai:
            # Pour l'IA, ajuster proportionnellement au niveau de difficulté
            self.vitesse = self.niveau_ia['VITESSE'] * facteur
            logger.debug(f"IA: Vitesse raquette ajustée à {self.vitesse:.1f} (facteur: {facteur:.2f})")
        else:
            # Pour le joueur humain
            self.vitesse = self.vitesse_base * facteur
            logger.debug(f"JOUEUR: Vitesse raquette ajustée à {self.vitesse:.1f} (facteur: {facteur:.2f})")
    
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
        # Probabilité de réaction basée sur le niveau
        if random.random() > self.niveau_ia['REACTION']:
            # L'IA ne réagit pas cette frame
            return
            
        # Position cible avec erreur basée sur le niveau
        target_y = ball.taille.centery
        
        # Ajouter une erreur aléatoire pour rendre l'IA plus humaine
        error = random.randint(-self.niveau_ia['PRECISION'], self.niveau_ia['PRECISION'])
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
    
    def set_niveau_ia(self, niveau_ia):
        """Change le niveau de difficulté de l'IA"""
        if self.is_ai:
            self.niveau_ia = niveau_ia
            self.vitesse_base = niveau_ia['VITESSE']
            self.vitesse = self.vitesse_base
            logger.info(f"IA: Niveau modifié - Vitesse: {niveau_ia['VITESSE']}, Précision: {niveau_ia['PRECISION']}, Réaction: {niveau_ia['REACTION']}")
            return True
        return False
    
    def draw(self, screen):  # Méthode de dessin
        """Dessine la raquette sur l'écran"""
        pygame.draw.rect(screen, self.couleur, self.rect)  # Dessine le rectangle
        
