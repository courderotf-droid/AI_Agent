import json
from datetime import datetime
from display import style_print as sp
from . import logger as log

nom_fichier = "chat_history.json"

def erreur(message):
    sp.print_erreur(f"Erreur: {message}")
    log.erreur(message)

try:
    def ecrire(contenu):
        try:
            with open(nom_fichier, "w", encoding="utf-8") as fichier:
                json.dump(contenu, fichier, indent=4, ensure_ascii=False)

        except OSError as e:
            erreur(f"Impossible d'écrire l'historique : {e}")

    def lire():
        try:
            with open(nom_fichier, "r", encoding="utf-8") as fichier:
                return json.load(fichier)

        except FileNotFoundError:
            erreur("Le fichier d'historique n'existe pas.")
            return []

        except json.JSONDecodeError:
            log.avertissement("Le fichier d'historique contient un JSON invalide.")
            return []

        except OSError as e:
            erreur(f"Erreur lors de la lecture du fichier : {e}")
            return []

    # Ecraser le contenu par une structure json minimale (évite les erreurs de parser)
    def vider_historique():

        with open("chat_history.json", 'w') as fichier:
            fichier.write("[]")


    def logger_message(texte, role):
        try:
            chat_history = lire()

            if not isinstance(chat_history, list):
                raise ValueError("Le fichier JSON ne contient pas une liste.")

            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

            chat_history.append({
                "heure": timestamp,
                "message": texte,
                "role": role
            })

            ecrire(chat_history)

        except ValueError as e:
            erreur(f"Format d'historique invalide : {e}")

        except Exception as e:
            erreur(f"Erreur inattendue : {e}")

except Exception as e:

    erreur(f"Erreur: {e}")