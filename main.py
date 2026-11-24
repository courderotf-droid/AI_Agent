import json, asyncio
import apis.ollama_api as api
import display.style_print as sp
import ai_agent.logging.logger as log
import display.gestion_erreurs as erreurs
import context as ctx
import commands as cmd
import vars

# Variables d'environnement
from getenv import MODE_TEST, HISTORIQUE, dossier_actuel

taille_du_contexte = ctx.taille_du_contexte

try:
    ## Extraction des variables d'environnement et importation des bibliothèques utiles
    if vars.TELEGRAM:
        import apis.lien_telegram as tele

    if HISTORIQUE:
        import ai_agent.logging.history_logs as hist
    #

    sp.print_message_lancement(
        f"Chat avec Ollama (Interface: {"Telegram" if vars.TELEGRAM else "Terminal"}, Mode test: {'activé' if MODE_TEST else 'désactivé'})"
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

    def hist_wrapper(texte, role):
        if HISTORIQUE:
            hist.logger_message(texte, role)

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
                cmd.traiter_message,
                entree
            )

            if retour:

                traiter_retour(retour)
                reponse = retour[0]
                
            else:
                
                ctx.add_context({'role': 'user', 'content': entree})
                ctx.add_question()
                hist_wrapper(entree, 'user')
                reponse = api.inferer(ctx.get_context())
                ctx.add_reponse()
                hist_wrapper(reponse, 'assistant')

            await tele.sortie_texte(reponse)

        tele.fix_print()
        sp.print_role("\nAssistant Telegram: ")
        tele.fix_print()
        print(f"{reponse}\n")

    if vars.TELEGRAM:

        tele.réception_texte(handle_texte)
        tele.start_bot()

    else:

        while True:

            entree = sp.input_role("\nUser: ")

            if entree.lower() in ['exit', 'quit', 'q']:

                sp.print_message_arret("\nBye!")
                break

            # Indique si le message a été intercepté
            retour = cmd.traiter_message(entree)

            if retour:
                
                traiter_retour(retour)
                sp.print_c(retour[0])
                continue

            ctx.add_question()
            hist_wrapper(entree, 'user')

            ctx.add_context({'role': 'user', 'content': entree})
            log.info("requete utilisateur", 'user')

            sp.print_role("\nOllama: ")

            #Traitement de la réponse de l'IA
            if vars.streaming:

                reponse_assistant = []

                def handle_texte_api(texte):
                    print(texte, end='', flush=True)
                    reponse_assistant.append(texte)

                api.reception_texte(handle_texte_api)
                api.inferer_streaming(ctx.get_context())

                reponse_assistant = ''.join(reponse_assistant)

            else:

                reponse_assistant = api.inferer(ctx.get_context())
                print(reponse_assistant)

            print()

            ctx.add_context({'role': 'assistant', 'content': reponse_assistant})
            log.info("réponse de Ollama", 'assistant')
            ctx.add_reponse()

            hist_wrapper(reponse_assistant, 'assistant')


except KeyboardInterrupt:

    sp.print_message_arret("\nBye!")

except Exception as e:

    erreurs.gerer_erreur(e)

    contexte = ctx.get_context()
    if contexte and contexte[-1]['role'] == 'user':
        ctx.define_context(contexte.pop())