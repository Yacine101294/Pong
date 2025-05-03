# Script de test pour la fenêtre de logs
import logging
import time
from log_window import start_log_window

def test_log_window():
    # Configurer le logger pour ne pas afficher dans la console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[]  # Pas de handler par défaut
    )
    logger = logging.getLogger("TestLogger")
    
    print("Démarrage de la fenêtre de logs (test)...")
    log_window = start_log_window()
    
    if log_window:
        # Ajouter notre handler de fenêtre au logger
        logger.addHandler(log_window.get_handler())
        print("Fenêtre de logs initialisée. Les logs apparaîtront uniquement dans la fenêtre, pas dans ce terminal.")
        
        # Envoyer divers types de logs pour tester
        logger.info("INFO: Ceci est un message d'information standard")
        time.sleep(0.5)
        
        logger.info("JOUEUR: Le joueur a déplacé sa raquette")
        time.sleep(0.5)
        
        logger.info("IA: L'IA a décidé de monter")
        time.sleep(0.5)
        
        logger.info("COLLISION: La balle a rebondi sur un mur à la position (150, 300)")
        time.sleep(0.5)
        
        logger.info("POINT: Joueur marque un point! Score: 1-0")
        time.sleep(0.5)
        
        logger.info("INPUT: Joueur appuie sur la touche HAUT")
        time.sleep(0.5)
        
        logger.debug("Ceci est un message de débogage (peut ne pas être visible)")
        time.sleep(0.5)
        
        logger.warning("ATTENTION: Ceci est un avertissement")
        time.sleep(0.5)
        
        logger.error("ERREUR: Ceci est un message d'erreur")
        time.sleep(0.5)
        
        logger.critical("CRITIQUE: Ceci est un message critique")
        
        print("Test terminé! Vous devriez voir tous ces messages dans la fenêtre de logs (fond noir).")
        print("La fenêtre restera ouverte jusqu'à ce que vous la fermiez ou arrêtiez ce script.")
        
        # Maintenir le script en vie pour que la fenêtre reste ouverte
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Script arrêté par l'utilisateur.")
    else:
        print("Erreur: Impossible d'initialiser la fenêtre de logs.")

if __name__ == "__main__":
    test_log_window() 