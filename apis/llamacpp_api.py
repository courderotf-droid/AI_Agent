from openai import OpenAI
from openai import OpenAIError

from ai_agent.display import gestion_erreurs as erreurs

try:

    client = OpenAI(
        base_url="http://localhost:8080/v1",
        api_key="sk-no-key-required"
    )


    def liste_modeles():

        try:
            return client.models.list()

        except OpenAIError as e:
            erreurs.gerer_erreur("Erreur llama.cpp :", e)
            raise

        except Exception as e:
            erreurs.gerer_erreur(e)
            raise


    def info_modele(modele):

        try:
            return client.models.retrieve(modele)

        except OpenAIError as e:
            erreurs.gerer_erreur("Erreur llama.cpp :", e)
            raise

        except Exception as e:
            erreurs.gerer_erreur(e)
            raise


    def modele_actif():

        modeles = liste_modeles()

        if not modeles.data:
            raise RuntimeError(
                "Aucun modèle disponible sur llama.cpp."
            )

        return modeles.data[0].id


    def inferer(contexte):

        try:
            response = client.chat.completions.create(
                model=modele_actif(),
                messages=contexte
            )

            return response.choices[0].message.content

        except OpenAIError as e:
            erreurs.gerer_erreur("Erreur llama.cpp :", e)
            raise

        except Exception as e:
            erreurs.gerer_erreur(e)
            raise


    def inferer_streaming(contexte, callback):

        try:
            stream = client.chat.completions.create(
                model=modele_actif(),
                messages=contexte,
                stream=True
            )

            for chunk in stream:

                if not chunk.choices:
                    continue

                contenu = chunk.choices[0].delta.content

                if contenu:
                    callback(contenu)

        except OpenAIError as e:
            erreurs.gerer_erreur("Erreur llama.cpp :", e)
            raise

        except Exception as e:
            erreurs.gerer_erreur(e)
            raise


except Exception as e:
    erreurs.gerer_erreur(e)
    raise