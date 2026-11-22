import json, asyncio
import apis.ollama_api as api
import display.style_print as sp
import ai_agent.logging.logger as log
import display.gestion_erreurs as erreurs
import context as ctx

# Variables d'environnement
from getenv import MODE_TEST, TELEGRAM, HISTORIQUE, dossier_actuel

taille_du_contexte = ctx.taille_du_contexte
streaming = False  # (False if TELEGRAM else True)

try:
    ## Gestion contexte
    def get_context():
        return ctx.contexte

    def get_n_questions():
        return int(ctx.n_de_questions)

    def get_n_reponses():
        return int(ctx.n_de_reponses)

    def add_question():
        ctx.define_n_questions(get_n_questions() + 1)

    def add_reponse():
        ctx.define_n_reponses(get_n_reponses() + 1)
    # (Cet emplacement évite une erreur de nettoyage du contexte en cas d'erreur entérieure)

    ## Extraction des variables d'environnement et importation des bibliothèques utiles
    if TELEGRAM:
        import apis.lien_telegram as tele

    if HISTORIQUE:
        import ai_agent.logging.history_logs as hist
    #

    sp.print_message_lancement(
        f"Chat avec Ollama (Interface: {"Telegram" if TELEGRAM else "Terminal"}, Mode test: {'activé' if MODE_TEST else 'désactivé'})"
    )

    ## Création du prompt système
    with open(dossier_actuel / "data/prompts.json", 'r', encoding='utf-8') as f:
        prompts = json.load(f)

    prompt_systeme_agent = prompts['prompt_système_agent']
    prompt_agent_compression = prompts['prompt_agent_compression']

    if not MODE_TEST:

        reponse = api.liste_modeles()

        # A revoir/vérifier
        if not reponse in ['error', 'Error', 'ERROR']:

            print("API Ollama connectée avec succès!")

            log.info(
                "Accès à l'API vérifié avec succès!",
                "system"
            )

    def traiter_message(entree):

        global streaming

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

                    streaming = True
                    return ["Streaming activé", False]

                elif entree == 'no':

                    streaming = False
                    return ["Streaming désactivé", False]

                else:

                    # Marqué comme erreur
                    return ["Commande incorrecte", True]

        else:

            # Ajout fonction test de compression
            if get_n_reponses() > taille_du_contexte - 1 or entree == "test":

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
                return [str(get_context()), True]

            if entree == "count":

                logger_cmd(entree)
                return [f"Le contexte contient {get_n_questions()} questions et {get_n_reponses()} réponses.", False]

        return False

    def traiter_retour(retour):

        # Récupère les variables
        contenu = retour[0]
        mention_erreur = retour[1]

        if mention_erreur:

            log.erreur(contenu)

        else:

            log.info("réponse système", "system", contenu)

    async def handle_texte(data, context):

        entree = data["Texte"]

        tele.fix_print()
        sp.print_role("\nUser Telegram: ")
        tele.fix_print()
        print(entree)

        # Commande d'arret du programme
        if entree.lower() in ['exit', 'quit', 'q']:

            sp.print_message_arret("\nBye!")
            exit()

        else:

            boucle = asyncio.get_event_loop()

            retour = await boucle.run_in_executor(
                None,
                traiter_message,
                entree
            )

            if retour:

                traiter_retour(retour)
                reponse = retour[0]
                
            else:
                
                ctx.add_context({'role': 'user', 'content': entree})
                add_question()
                hist.logger_message(entree, 'user')
                reponse = api.inferer(get_context())
                add_reponse()
                hist.logger_message(reponse, 'assistant')

            await tele.sortie_texte(reponse)

        tele.fix_print()
        sp.print_role("\nAssistant Telegram: ")
        tele.fix_print()
        print(f"{reponse}\n")

    if TELEGRAM:

        tele.réception_texte(handle_texte)
        tele.start_bot()

    else:

        while True:

            entree = sp.input_role("\nUser: ")

            if entree.lower() in ['exit', 'quit', 'q']:

                sp.print_message_arret("\nBye!")
                break

            # Indique si le message a été intercepté
            retour = traiter_message(entree)

            if retour:
                
                traiter_retour(retour)
                sp.print_c(retour[0])
                continue

            add_question()
            hist.logger_message(entree, 'user')

            ctx.add_context({'role': 'user', 'content': entree})
            log.info("requete utilisateur", 'user')

            sp.print_role("\nOllama: ")

            #Traitement de la réponse de l'IA
            if streaming:

                reponse_assistant = []

                def handle_texte_api(texte):
                    print(texte, end='', flush=True)
                    reponse_assistant.append(texte)

                api.reception_texte(handle_texte_api)
                api.inferer_streaming(get_context())

                reponse_assistant = ''.join(reponse_assistant)

            else:

                reponse_assistant = api.inferer(get_context())
                print(reponse_assistant)

            print()

            ctx.add_context({'role': 'assistant', 'content': reponse_assistant})
            log.info("réponse de Ollama", 'assistant')
            add_reponse()

            hist.logger_message(reponse_assistant, 'assistant')


except KeyboardInterrupt:

    sp.print_message_arret("\nBye!")

except Exception as e:

    erreurs.gerer_erreur(e)

    contexte = get_context()
    if contexte and contexte[-1]['role'] == 'user':
        ctx.define_context(contexte.pop())
