import ai_agent.logging.logger as log
import display.style_print as sp
import context as ctx
from getenv import TELEGRAM
import vars

def traiter_message(entree):

    def logger_cmd(entree):
        log.info("commande utilisateur", "user", entree)

    # Evite les fautes de frappe
    entree = entree.lower()

    if entree == 'stream':

        logger_cmd(entree)

        if TELEGRAM:

            return ["La fonction streaming n'est pas disponible dans Telegram.", False]

        else:

            entree = sp.input_c("System (choisir entre 'yes' et 'no'): ").lower()

            if entree == 'yes':

                vars.streaming = True
                return ["Streaming activé", False]

            elif entree == 'no':

                vars.streaming = False
                return ["Streaming désactivé", False]

            else:

                # Marqué comme erreur
                return ["Commande incorrecte", True]

    else:

        # Ajout fonction test de compression
        if ctx.get_n_reponses() > ctx.taille_du_contexte - 1 or entree == "test":

            ctx.compression_contexte()
            if entree == 'test':
                logger_cmd(entree)
            return ["Contexte nettoyé", False]

        if entree == "reset":
            ctx.define_context([])
            ctx.add_system_prompt()
            logger_cmd(entree)
            return ["Contexte réinitialisé.", False]

        if entree == "context":
            logger_cmd(entree)
            return [str(ctx.get_context()), True]

        if entree == "count":
            logger_cmd(entree)
            return [f"Le contexte contient {ctx.get_n_questions()} questions et {ctx.get_n_reponses()} réponses.", False]

    return False