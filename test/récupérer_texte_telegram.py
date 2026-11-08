import apis.lien_telegram as tg

def handle_texte(texte):
    print("Reçu :", texte)

tg.réception_texte(handle_texte)

tg.start_bot()