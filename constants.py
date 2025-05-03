# Constantes pour le jeu Pong
import pygame

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 480

SCORE = 0

# Couleurs
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)
GRIS = (200, 200, 200)
VERT = (0, 255, 0)
ROUGE = (255, 0, 0)
BLEU = (0, 0, 255)
JAUNE = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

#Paramètres des raquettes
RAQUETTE_LARGEUR = 15
RAQUETTE_HAUTEUR = 90
RAQUETTE_VITESSE = 7
RAQUETTE_MARGE = 20  # Distance du bord de l'écran
RAQUETTE_COULEUR = BLANC

#Paramètre de la balle
BALLE_TAILLE = 15  # Taille du carré de la balle
BALLE_VITESSE_INITIALE = 5  # Vitesse initiale de la balle
BALLE_ACCELERATION = 1.1  # Facteur d'accélération après chaque rebond
BALLE_VITESSE_MAX = 15  # Vitesse maximale de la balle
BALLE_COULEUR = BLANC  # Couleur de la balle

fps = pygame.time.Clock().tick(30)
