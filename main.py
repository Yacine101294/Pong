# Point d'entrée principal du jeu Pong
import pygame
from constants import *
from game import Game

def main():
    # Initialisation de Pygame
    pygame.init()
    
    # Création d'une instance de Game qui contient toute la logique
    game = Game()
    
    # Boucle principale du jeu
    while game.running:
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
        
        # Gestion des entrées clavier pour le joueur
        game.handle_input()
        
        # Mise à jour de l'état du jeu
        game.update()
        
        # Affichage de tous les éléments
        game.draw()
        
        # Limiter le taux de rafraîchissement
        pygame.time.Clock().tick(60)  # 60 FPS
    
    # Quitter Pygame
    pygame.quit()

# Lancement du jeu si ce fichier est exécuté directement
if __name__ == "__main__":
    main()