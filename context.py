from getenv import dossier_actuel
import json
import display.style_print as sp
import apis.ollama_api as api
import display.gestion_erreurs as erreurs


try:
    ## Initialisation de variables
    contexte = []
    taille_du_contexte = 6
    n_de_questions = 0
    n_de_reponses = 0
    #

    ## Création du prompt système
    with open(dossier_actuel / "data/prompts.json", 'r', encoding='utf-8') as f:
        prompts = json.load(f)

    prompt_systeme_agent = prompts['prompt_système_agent']
    prompt_agent_compression = prompts['prompt_agent_compression']

    def define_context(list : list):
        global contexte
        contexte = list
        return True

    def define_n_questions(n : int):
        global n_de_questions
        n_de_questions = n

    def define_n_reponses(n : int):
        global n_de_reponses
        n_de_reponses = n

    def add_context(dict : dict):
        global contexte
        contexte.append(dict)
        return True

    def add_system_prompt():
        global contexte

        contexte.append({'role': 'system', 'content': prompt_systeme_agent})

    add_system_prompt()
    #

    def compression_contexte():
        global contexte
        global taille_du_contexte
        global prompt_agent_compression

        moitie_limite_contexte = taille_du_contexte // 2

        a_resumer = contexte[1:moitie_limite_contexte + 1]

        texte_a_resumer = "\n".join(
            [
                f"{m['role']}: {m['content']}"
                for m in a_resumer
            ]
        )

        requete = prompt_agent_compression.format(texte_a_resumer=texte_a_resumer)

        sp.print_message_auto("Contexte plein! Nettoyage en cours...")

        resume = api.inferer_streaming(requete)

        resume_formate = {
            'role': 'system',
            'content':
                f"[Ceci est le résumé du contexte précédent.] {resume}"
        }

        contexte = (
                [contexte[0], resume_formate]
                +
                contexte[-moitie_limite_contexte:]
        )

except Exception as e:
    erreurs.gerer_erreur(e)