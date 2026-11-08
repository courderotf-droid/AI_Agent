from pathlib import Path
import logging
from ai_agent.display import style_print as sp

try:
    #Initialisation
    dossier_actuel = Path(__file__).parent

    #Restrictions
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)

    #Configuration du logging
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%d/%m/%Y %I:%M:%S %p',
    filename= dossier_actuel / 'logs.log',
    level=logging.INFO)

    source_erreur = 'system'

    def avertissement(avertissement):
        logging.warning(f"{avertissement} | source: '{source_erreur}'")

    def erreur(erreur, *action):
        if action:
            logging.error(f"{erreur} | action: [{action}] | source: '{source_erreur}'")
        else:
            logging.error(f"{erreur} | source: '{source_erreur}'")

    def erreur_critique(erreur, *action):
        if action:
            logging.critical(f"{erreur} | action: [{action}] | source: '{source_erreur}'")
        else:
            logging.critical(f"{erreur} | source: '{source_erreur}'")

    def info(action, source, *contenu):
        if contenu:
            logging.info(f"""action: [{action}] | contenu: "{contenu}" | source: '{source}'""")
        else:
            logging.info(f"action: [{action}] | source: '{source}'")

except Exception as e:
    message_arret = "Arret du programme!"
    sp.formatage_erreurs(f"Erreur de logging (CRITIQUE): {e}")
    sp.print_erreur(message_arret)
    erreur_critique(e, message_arret)
    exit()