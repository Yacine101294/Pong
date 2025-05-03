# Classe pour la balle du jeu Pong
import pygame
import random
from constants import *

class Ball:
    def __init__(self, x, y, taille=BALLE_TAILLE, vitesse_initiale=BALLE_VITESSE_INITIALE, acceleration=BALLE_ACCELERATION, couleur=BALLE_COULEUR):
        self.x = x
        self.y = y
        self.taille = pygame.Rect(x, y, taille, taille)
        self.vitesse_x = vitesse_initiale
        self.vitesse_y = vitesse_initiale
        self.vitesse_initiale = vitesse_initiale
        self.acceleration = acceleration
        self.couleur = couleur
    
    def deplacer(self):
        """Déplace la balle selon sa vitesse actuelle"""
        self.taille.x += self.vitesse_x
        self.taille.y += self.vitesse_y
    
    def detecter_collision_murs(self):
        """Détecte les collisions avec les murs haut et bas et inverse la direction"""
        if self.taille.top <= 0 or self.taille.bottom >= WINDOW_HEIGHT:
            self.vitesse_y *= -1
            return True
        return False
    
    def detecter_collision_raquettes(self, raquette_gauche, raquette_droite):
        """Détecte les collisions avec les raquettes et inverse la direction"""
        if self.taille.colliderect(raquette_gauche.rect) or self.taille.colliderect(raquette_droite.rect):
            self.vitesse_x *= -1
            self.vitesse_x *= self.acceleration  # Accélération après rebond
            
            # Limiter la vitesse maximale
            if abs(self.vitesse_x) > BALLE_VITESSE_MAX:
                self.vitesse_x = BALLE_VITESSE_MAX * (1 if self.vitesse_x > 0 else -1)
                
            return True
        return False
    
    def detecter_point(self):
        """Détecte si la balle est sortie des limites horizontales (point marqué)"""
        if self.taille.left <= 0:
            return "droite"  # Point pour le joueur de droite
        elif self.taille.right >= WINDOW_WIDTH:
            return "gauche"  # Point pour le joueur de gauche
        return None
    
    def reinitialiser(self, x, y):
        """Réinitialise la position et la vitesse de la balle après un point"""
        self.taille.x = x
        self.taille.y = y
        # Réinitialise la vitesse avec une direction aléatoire
        self.vitesse_x = self.vitesse_initiale * (1 if random.random() > 0.5 else -1)
        self.vitesse_y = self.vitesse_initiale * (1 if random.random() > 0.5 else -1)
    
    def dessiner_balle(self, screen):
        """Dessine la balle sur l'écran"""
        pygame.draw.rect(screen, self.couleur, self.taille)
    
    def get_vitesse_actuelle(self):
        """Retourne la vitesse horizontale absolue actuelle de la balle"""
        return abs(self.vitesse_x)
        
    
