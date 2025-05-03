import pygame
from constants import *

class Button:
    def __init__(self, x, y, largeur, hauteur, texte):
        self.rect = pygame.Rect(x, y, largeur, hauteur)
        self.text=texte
        self.couleur=BLANC
        self.couleur_texte = NOIR
        self.font = pygame.font.Font(None, 36)
        
        self.hover = False
        self.clicked = False
        
    def draw(self, surface):
        # Dessiner le fond du bouton
        pygame.draw.rect(surface, self.couleur, self.rect, 0, 10)
        
        # Dessiner le contour du bouton
        pygame.draw.rect(surface, NOIR, self.rect, 2, 10)
        
        # Rendre le texte
        text_surface = self.font.render(self.text, True, self.couleur_texte)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def update(self, mouse_pos, mouse_click):
        # Vérifier si la souris est sur le bouton
        self.hover = self.rect.collidepoint(mouse_pos)
        
        # Changer la couleur si la souris survole le bouton
        if self.hover:
            self.couleur = GRIS_CLAIR
            if mouse_click:
                self.clicked = True
            else:
                self.clicked = False
        else:
            self.couleur = BLANC
            self.clicked = False
    
    def is_clicked(self):
        return self.clicked
        