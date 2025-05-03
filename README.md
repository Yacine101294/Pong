# Jeu Pong en Python avec Pygame

Un jeu Pong classique développé en Python avec la bibliothèque Pygame, offrant une interface graphique moderne et des fonctionnalités avancées.

![Pong Game](https://raw.githubusercontent.com/username/pong/main/screenshot.png)

## Fonctionnalités

- **Interface graphique moderne** avec menus interactifs
- **IA adaptative** avec trois niveaux de difficulté (Facile, Normal, Difficile)
- **Système de score** en temps réel
- **Menu pause** activable avec la touche Échap
- **Système de logs** avec fenêtre dédiée pour suivre les événements du jeu
- **Vitesse dynamique** : les raquettes s'adaptent à la vitesse de la balle

## Commandes

- **Flèche Haut/Bas** : Déplacer la raquette du joueur
- **Échap** : Mettre le jeu en pause
- **Souris** : Naviguer dans les menus

## Architecture du projet

Le jeu est structuré de manière modulaire avec les composants suivants :

- `main.py` : Point d'entrée et gestion des écrans
- `game.py` : Logique principale du jeu
- `ball.py` : Gestion de la balle (mouvements, collisions)
- `paddle.py` : Gestion des raquettes (joueur et IA)
- `constants.py` : Constantes et paramètres
- `buttons.py` : Composants d'interface utilisateur
- `log_window.py` : Système de journalisation

## Fonctionnalités techniques

### Système d'IA

L'IA comporte trois niveaux de difficulté avec des paramètres configurables :
- **Vitesse** : Rapidité de déplacement de la raquette
- **Précision** : Marge d'erreur pour suivre la balle
- **Réaction** : Probabilité de réagir aux mouvements de la balle

### Système de journalisation

Un système complet de logs avec une fenêtre dédiée qui s'affiche en arrière-plan :
- Logs colorés par type d'événement
- Enregistrement dans des fichiers datés
- Suivi en temps réel des actions du jeu

### Vitesse dynamique des raquettes

Les raquettes ajustent automatiquement leur vitesse proportionnellement à celle de la balle :
- Plus la balle va vite, plus les raquettes deviennent rapides
- Permet au joueur de continuer à suivre la balle lors des accélérations
- Facteur d'accélération configurable

## Installation

1. Assurez-vous d'avoir Python 3.7+ installé
2. Installez Pygame en exécutant :
   ```
   pip install pygame==2.1.2
   ```
3. Clonez ce dépôt ou téléchargez-le
4. Lancez le jeu :
   ```
   python main.py
   ```

## Personnalisation

Vous pouvez personnaliser divers aspects du jeu en modifiant le fichier `constants.py` :
- Taille de la fenêtre
- Couleurs
- Dimensions des raquettes
- Vitesse et accélération de la balle
- Comportement de l'IA

## Développement

Ce projet a été développé en Python avec la bibliothèque Pygame. Il utilise une architecture orientée objet pour faciliter la maintenance et l'extension. 