from ai_agent.logging import logger as log
from . import style_print as sp
from ai_agent.apis import lien_telegram as tele
import asyncio

# Variable 'TELEGRAM'
from ai_agent.getenv import TELEGRAM

# Traitement de l'erreur en mode Terminal
def log_sh(message_erreur):
    sp.print_erreur(message_erreur)
    log.erreur(message_erreur)

def envoie_telegram(message_erreur):

        asyncio.run(
            tele.envoi_texte(message_erreur)
        )
        log.erreur(message_erreur)

def gerer_erreur(message_erreur):

    if TELEGRAM:
        envoie_telegram(message_erreur)

    else:
        log_sh(message_erreur)

def gerer_avertissement(avertissement):
    sp.print_avertissement(avertissement)
    log.avertissement(avertissement)