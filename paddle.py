# Classe pour les raquettes du jeu Pong
import pygame
from constants import *
"""window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Pong game")


go = True
while go:
    for event in pygame.event.get():
        pygame.display.flip()"""

class Paddle:
    def __init__(self, x, y, largeur=RAQUETTE_LARGEUR, hauteur=RAQUETTE_HAUTEUR, vitesse=RAQUETTE_VITESSE):  # Initialisation de la raquette avec position et dimensions
        self.rect = pygame.Rect(x, y, largeur, hauteur)  # Création du rectangle de la raquette
        self.couleur = RAQUETTE_COULEUR  # Définition de la couleur
        self.vitesse = vitesse  # Vitesse de déplacement
        self.direction = 0  # 0: immobile, -1: vers le haut, 1: vers le bas
    
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
        self.rect.y += self.direction * self.vitesse  # Calcul du nouveau déplacement
        
        # Empêche la raquette de sortir de l'écran
        if self.rect.top < 0:  # Collision avec le haut
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:  # Collision avec le bas
            self.rect.bottom = WINDOW_HEIGHT
        
    def ai_move(self, ball):
        # IA simple: suivre la balle
        # Ajout d'un petit délai/imprécision pour que l'IA ne soit pas parfaite
        target_y = ball.rect.centery
        
        # Ajouter une petite erreur aléatoire pour rendre l'IA plus humaine
        # (optionnel, commentez si vous voulez une IA parfaite)
        import random
        target_y += random.randint(-30, 30)
        
        #Décider si on mon ou descent
        if self.rect.centery < target_y:
            self.rect.y += self.speed
        elif self.rect.centery > target_y:
            self.rect.y -= self.speed
    
    def draw(self, screen):  # Méthode de dessin La variable screen est un paramètre de la méthode draw de la classe Paddle. Elle représente la surface Pygame sur laquelle la raquette sera dessinée. Cette variable n'est pas définie à l'intérieur de la classe, mais elle est passée comme argument lorsque la méthode draw est appelée depuis l'extérieur.Pour utiliser cette méthode, vous devez passer la surface d'affichage principale (généralement créée avec pygame.display.set_mode()) comme paramètre. Dans votre code, vous pourriez l'utiliser comme
        """Dessine la raquette sur l'écran"""
        pygame.draw.rect(screen, self.couleur, self.rect)  # Dessine le rectangle
        
