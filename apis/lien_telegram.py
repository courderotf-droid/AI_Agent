import os, sys, asyncio
from pathlib import Path
from dotenv import load_dotenv
from telegram.ext import Application, filters, CommandHandler, MessageHandler
from ai_agent.display import style_print as sp
from ai_agent.logging import logger as log

try:
    dossier_actuel = Path(__file__).parent
    load_dotenv(dossier_actuel / "settings.env")

    TOKEN = os.getenv("TOKEN")
    CHAT_ID = int(os.getenv("CHAT_ID"))

    if not TOKEN:
        raise RuntimeError("TOKEN introuvable")
    if not CHAT_ID:
        raise RuntimeError("CHAT_ID introuvable")

    callbacks_texte = []

    app = Application.builder().token(TOKEN).build()

    séparateur = f"\n\n{'='*30}\n{'='*8} séparateur {'='*8}\n{'='*30}\n\n"

    stop_event = asyncio.Event()
    animation_task = None

    async def animation():
        frames = ["|", "/", "-", "\\"]
        i = 0

        try:
            while not stop_event.is_set():
                sys.stdout.write(
                    f"\rEn attente de messages {frames[i % len(frames)]}"
                )
                sys.stdout.flush()

                i += 1
                await asyncio.sleep(0.4)

        except asyncio.CancelledError:
            pass

        finally:
            sys.stdout.write("\r" + " " * 50 + "\r")
            sys.stdout.flush()

    async def démarrer_animation():
        global animation_task

        if animation_task is None or animation_task.done():
            animation_task = asyncio.create_task(animation())

    async def arrêter_animation():
        global animation_task

        stop_event.set()

        if animation_task:
            animation_task.cancel()

            try:
                await animation_task
            except asyncio.CancelledError:
                pass

    def fix_print():
        sys.stdout.write("\r" + " " * 80 + "\r")
        sys.stdout.flush()

    def obtenir_infos_entrée(update):
        message = update.message

        return (
            message.chat.id,
            message.from_user.id,
            message.from_user.username,
            message.date
        )

    async def start(update, context):
        if update.message:
            chat_id, user_id, user_name, date = obtenir_infos_entrée(update)

            réponse = (
                f"Chat_ID: {chat_id}\n"
                f"User_ID: {user_id}\n"
                f"Username: {user_name}\n"
                f"Date: {date}"
            )

            fix_print()
            print(réponse, séparateur)

            await update.message.reply_text(réponse)

    async def test(update, context):
        reponse = f"{"" * 20}pong!"

        if update.message:
            fix_print()
            print(reponse.upper(), séparateur)
            await update.message.reply_text(reponse)

    async def entrée_texte(update, context):

        message = update.message

        if not message or not message.text:
            return

        if message.chat.id != CHAT_ID:
            fix_print()
            print(
                "Envoi non-autorisé identifié",
                séparateur
            )
            return

        chat_id, user_id, user_name, date = obtenir_infos_entrée(update)

        réponse = {
            "Texte": message.text,
            "Chat_ID": chat_id,
            "User_ID": user_id,
            "Username": user_name,
            "Date": date
        }

        for cb in callbacks_texte:
            résultat = cb(réponse, context)

            if asyncio.iscoroutine(résultat):
                await résultat

    def réception_texte(handle_texte):
        callbacks_texte.append(handle_texte)

    async def entrée_image(update, context):
        if update.message:
            await update.message.reply_text("Image reçue!")

    async def sortie_texte(texte_envoyé):

        global CHAT_ID

        print("AVANT TELEGRAM :", texte_envoyé)
        print("REPR :", repr(texte_envoyé))
        await app.bot.send_message(
            chat_id=CHAT_ID,
            text=texte_envoyé,
        )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "ping",
            test
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            entrée_texte
        )
    )

    app.add_handler(
        MessageHandler(
            filters.PHOTO,
            entrée_image
        )
    )

    async def main():

        await app.initialize()
        await app.start()
        await app.updater.start_polling()

        await démarrer_animation()

        try:
            await asyncio.Event().wait()

        except KeyboardInterrupt:
            print("\nArrêt en cours...")

        finally:
            await arrêter_animation()

            await app.updater.stop()
            await app.stop()
            await app.shutdown()

            print("Bot arrêté proprement.")

    def start_bot():
        asyncio.run(main())

except Exception as e:
    message = f"Erreur: {e}"

    sp.print_erreur(message)
    log.erreur_critique(message)