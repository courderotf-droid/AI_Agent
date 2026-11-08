import ollama
from ollama import chat
from ollama import ChatResponse
from ai_agent.getenv import MODELE
from ai_agent.display import gestion_erreurs as erreurs
import ai_agent.apis.lien_telegram as tg

try:
    tg.callbacks_texte = []

    if not MODELE:
        erreurs.gerer_avertissement("Veuillez configurer le modèle dans le fichier '.env'")


    def inferer(contexte):

        response: ChatResponse = chat(model=MODELE, messages=contexte)
        return response.message.content

    def inferer_streaming(contexte):

        stream = chat(
            model=MODELE,
            messages=contexte,
            stream=True,
        )

        for chunk in stream:
            for cb in tg.callbacks_texte:
                cb(chunk['message']['content'])

        return None

    #A utiliser avec 'inferer_streaming()'
    def reception_texte(handle_texte):
        tg.callbacks_texte.append(handle_texte)

    def liste_modeles():
        return ollama.list()

    def info_modele(modele):
        return ollama.show(modele)

except ollama.ResponseError as e:
  erreurs.gerer_erreur('Erreur Ollama:', e.error)
  #if e.status_code == 404:
    #ollama.pull(MODELE)

except Exception as e:
    erreurs.gerer_erreur(e)