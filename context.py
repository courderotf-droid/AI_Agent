from getenv import dossier_actuel
import json
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
    #

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

    def get_context():
        return contexte

    def get_n_questions():
        return int(n_de_questions)

    def get_n_reponses():
        return int(n_de_reponses)

    def add_question():
        define_n_questions(get_n_questions() + 1)

    def add_reponse():
        define_n_reponses(get_n_reponses() + 1)

    def add_system_prompt():
        global contexte

        contexte.append({'role': 'system', 'content': prompt_systeme_agent})

    add_system_prompt()

except Exception as e:
    erreurs.gerer_erreur(e)