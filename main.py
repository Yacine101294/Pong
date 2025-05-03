# Point d'entrée principal du jeu Pong
import pygame
from constants import *
from game import Game
from buttons import Button

def afficher_ecran_accueil():
    """Affiche l'écran d'accueil et retourne l'action choisie (start, reglages, quit)"""
    # Création de la fenêtre
    fenetre = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pong Game")
    
    # Création des boutons
    bouton_start = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 30, 200, 50, "JOUER")
    bouton_reglages = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 40, 200, 50, "RÉGLAGES")
    
    # Création du fond
    background = pygame.Surface(fenetre.get_size())
    background = background.convert()
    background.fill(NOIR)
    
    # Création du titre
    font_title = pygame.font.Font(None, 72)
    text_title = font_title.render("PONG", True, BLANC)
    title_pos = text_title.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4))
    
    # Création du sous-titre
    font = pygame.font.Font(None, 36)
    text = font.render("Bienvenue dans le jeu Pong", True, BLANC)
    textpos = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4 + 50))
    
    # Horloge pour contrôler le FPS
    clock = pygame.time.Clock()
    
    # Boucle de l'écran d'accueil
    running = True
    while running:
        # Récupération des événements
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_click = True
        
        # Mise à jour des boutons
        bouton_start.update(mouse_pos, mouse_click)
        bouton_reglages.update(mouse_pos, mouse_click)
        
        # Vérifier si un bouton a été cliqué
        if bouton_start.is_clicked():
            return "start"
        if bouton_reglages.is_clicked():
            return "reglages"
        
        # Dessin de l'écran
        fenetre.blit(background, (0, 0))
        fenetre.blit(text_title, title_pos)
        fenetre.blit(text, textpos)
        
        # Dessin des boutons
        bouton_start.draw(fenetre)
        bouton_reglages.draw(fenetre)
        
        # Mise à jour de l'écran
        pygame.display.flip()
        
        # Limiter le taux de rafraîchissement
        clock.tick(60)
    
    return "quit"

def afficher_ecran_reglages():
    """Affiche l'écran des réglages et retourne le niveau de difficulté choisi"""
    # Création de la fenêtre
    fenetre = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pong - Réglages")
    
    # Création des boutons
    bouton_facile = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 80, 200, 50, "FACILE")
    bouton_normal = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, 200, 50, "NORMAL")
    bouton_difficile = Button(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 80, 200, 50, "DIFFICILE")
    bouton_retour = Button(30, WINDOW_HEIGHT - 70, 120, 40, "RETOUR")
    
    # Création du fond
    background = pygame.Surface(fenetre.get_size())
    background = background.convert()
    background.fill(NOIR)
    
    # Création du titre
    font_title = pygame.font.Font(None, 48)
    text_title = font_title.render("RÉGLAGES", True, BLANC)
    title_pos = text_title.get_rect(center=(WINDOW_WIDTH // 2, 50))
    
    # Création du sous-titre
    font = pygame.font.Font(None, 36)
    text = font.render("Sélectionnez le niveau de difficulté de l'IA", True, BLANC)
    textpos = text.get_rect(center=(WINDOW_WIDTH // 2, 100))
    
    # Horloge pour contrôler le FPS
    clock = pygame.time.Clock()
    
    # Niveau actuellement sélectionné (par défaut: intermédiaire)
    niveau_selectionne = "intermediaire"
    
    # Couleur des boutons selon la sélection
    def mettre_a_jour_couleurs():
        bouton_facile.couleur = VERT if niveau_selectionne == "facile" else BLANC
        bouton_normal.couleur = JAUNE if niveau_selectionne == "intermediaire" else BLANC
        bouton_difficile.couleur = ROUGE if niveau_selectionne == "difficile" else BLANC
    
    # Initialisation des couleurs
    mettre_a_jour_couleurs()
    
    # Boucle de l'écran des réglages
    running = True
    while running:
        # Récupération des événements
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    mouse_click = True
        
        # Mise à jour des boutons
        bouton_facile.update(mouse_pos, mouse_click)
        bouton_normal.update(mouse_pos, mouse_click)
        bouton_difficile.update(mouse_pos, mouse_click)
        bouton_retour.update(mouse_pos, mouse_click)
        
        # Vérifier si un bouton a été cliqué
        if bouton_facile.is_clicked():
            niveau_selectionne = "facile"
            mettre_a_jour_couleurs()
        if bouton_normal.is_clicked():
            niveau_selectionne = "intermediaire"
            mettre_a_jour_couleurs()
        if bouton_difficile.is_clicked():
            niveau_selectionne = "difficile"
            mettre_a_jour_couleurs()
        if bouton_retour.is_clicked():
            # Retourner le niveau de difficulté choisi
            if niveau_selectionne == "facile":
                return IA_FACILE
            elif niveau_selectionne == "intermediaire":
                return IA_INTERMEDIAIRE
            else:
                return IA_DIFFICILE
        
        # Dessin de l'écran
        fenetre.blit(background, (0, 0))
        fenetre.blit(text_title, title_pos)
        fenetre.blit(text, textpos)
        
        # Dessin des boutons
        bouton_facile.draw(fenetre)
        bouton_normal.draw(fenetre)
        bouton_difficile.draw(fenetre)
        bouton_retour.draw(fenetre)
        
        # Afficher les caractéristiques du niveau sélectionné
        niveau_info = IA_FACILE
        if niveau_selectionne == "intermediaire":
            niveau_info = IA_INTERMEDIAIRE
        elif niveau_selectionne == "difficile":
            niveau_info = IA_DIFFICILE
        
        # Textes d'information
        info_vitesse = font.render(f"Vitesse: {niveau_info['VITESSE']}", True, BLANC)
        info_precision = font.render(f"Précision: {100 - niveau_info['PRECISION']}%", True, BLANC)
        info_reaction = font.render(f"Réaction: {int(niveau_info['REACTION'] * 100)}%", True, BLANC)
        
        # Positions des textes
        vitesse_pos = info_vitesse.get_rect(topleft=(WINDOW_WIDTH // 2 + 120, WINDOW_HEIGHT // 2 - 80))
        precision_pos = info_precision.get_rect(topleft=(WINDOW_WIDTH // 2 + 120, WINDOW_HEIGHT // 2))
        reaction_pos = info_reaction.get_rect(topleft=(WINDOW_WIDTH // 2 + 120, WINDOW_HEIGHT // 2 + 80))
        
        # Affichage des informations
        fenetre.blit(info_vitesse, vitesse_pos)
        fenetre.blit(info_precision, precision_pos)
        fenetre.blit(info_reaction, reaction_pos)
        
        # Mise à jour de l'écran
        pygame.display.flip()
        
        # Limiter le taux de rafraîchissement
        clock.tick(60)
    
    return IA_INTERMEDIAIRE  # Niveau par défaut si l'écran est fermé

def lancer_jeu(niveau_ia=NIVEAU_IA_DEFAUT):
    """Lance le jeu principal"""
    game = Game(niveau_ia)
    
    # Horloge pour contrôler le FPS
    clock = pygame.time.Clock()
    
    # Boucle principale du jeu
    while game.running:
        # Gestion des entrées clavier pour le joueur
        game.handle_input()
        
        # Mise à jour de l'état du jeu
        game.update()
        
        # Affichage de tous les éléments
        game.draw()
        
        # Limiter le taux de rafraîchissement
        clock.tick(60)  # 60 FPS

def main():
    # Initialisation de Pygame
    pygame.init()
    
    niveau_ia = NIVEAU_IA_DEFAUT
    
    while True:
        # Afficher l'écran d'accueil
        action = afficher_ecran_accueil()
        
        # Traiter l'action choisie
        if action == "start":
            lancer_jeu(niveau_ia)
        elif action == "reglages":
            nouveau_niveau = afficher_ecran_reglages()
            if nouveau_niveau:
                niveau_ia = nouveau_niveau
        else:  # action == "quit"
            break
    
    # Quitter Pygame
    pygame.quit()

# Lancement du jeu si ce fichier est exécuté directement
if __name__ == "__main__":
    main()