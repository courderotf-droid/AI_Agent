import ollama
from ollama import chat, ChatResponse

from ai_agent.getenv import OLLAMA_MODELE
from ai_agent.display import gestion_erreurs as erreurs

try:

    if not OLLAMA_MODELE:
        erreurs.gerer_avertissement(
            "Veuillez configurer le modèle dans le fichier '.env'"
        )

    def inferer(contexte):

        try:
            response: ChatResponse = chat(
                model=OLLAMA_MODELE,
                messages=contexte
            )

            return response.message.content

        except ollama.ResponseError as e:
            erreurs.gerer_erreur("Erreur Ollama :", e.error)
            raise

        except Exception as e:
            erreurs.gerer_erreur(e)
            raise


    def inferer_streaming(contexte, callback):

        try:
            stream = chat(
                model=OLLAMA_MODELE,
                messages=contexte,
                stream=True
            )

            for chunk in stream:

                contenu = chunk.message.content

                if contenu:
                    callback(contenu)

        except ollama.ResponseError as e:
            erreurs.gerer_erreur("Erreur Ollama :", e.error)
            raise

        except Exception as e:
            erreurs.gerer_erreur(e)
            raise


    def liste_modeles():

        try:
            return ollama.list()

        except ollama.ResponseError as e:
            erreurs.gerer_erreur("Erreur Ollama :", e.error)
            raise

        except Exception as e:
            erreurs.gerer_erreur(e)
            raise


    def info_modele(modele):

        try:
            return ollama.show(modele)

        except ollama.ResponseError as e:
            erreurs.gerer_erreur("Erreur Ollama :", e.error)
            raise

        except Exception as e:
            erreurs.gerer_erreur(e)
            raise


except Exception as e:
    erreurs.gerer_erreur(e)
    raise