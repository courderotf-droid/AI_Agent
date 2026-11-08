from colorama import init, Fore, Style
import ai_agent.display.gestion_erreurs as erreurs

#Définitions
formatage_message_lancement = Style.BRIGHT + Fore.CYAN
formatage_message_arret = Fore.LIGHTBLUE_EX
formatage_message_auto = Style.BRIGHT + Fore.LIGHTBLUE_EX
formatage_roles = Style.DIM
formatage_commandes = Fore.WHITE
formatage_erreurs = Style.DIM + Fore.LIGHTMAGENTA_EX
formatage_avertissements = Style.DIM + Fore.YELLOW

try:
    init(autoreset=True)

    def print_message_lancement(message):
        print(formatage_message_lancement + str(message))

    def print_message_arret(message):
        print(formatage_message_arret + str(message))

    #Messages automatiques
    def print_message_auto(message):
        print(formatage_message_auto + str(message))

    ##

    def print_role(role):
        print(formatage_roles + str(role))

    def input_role(role):
        entrée = input(formatage_roles + role)
        return entrée

    #Commandes
    def print_c(message):
        print(formatage_commandes + str(message))

    def input_c(question):
        réponse = input(formatage_commandes + question)
        return réponse

    ##

    def print_erreur(erreur):
        print(formatage_erreurs + str(erreur))

    def print_avertissement(avertissement):
        print(formatage_avertissements + str(avertissement))

except Exception as e:

    erreurs.gerer_erreur(e)