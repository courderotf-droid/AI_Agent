import history_logs
from time import sleep

history_logs.vider_historique()

n = 0

try:
    while True:
        history_logs.logger_message("Hello World!", "user")
        sleep(0.3)
        print("Message enregistré avec succès")
        print(history_logs.lire())
        n += 1

except KeyboardInterrupt:
    print("Nombre de messages: ", n)