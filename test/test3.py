import os, sys

dossier_principal = os.path.join(os.path.dirname(__file__), "..")

dossiers_exclus = ['__pycache__', '.git']

for racine, sous_dossiers, fichiers in os.walk(dossier_principal):

    for dossier in dossiers_exclus:
        if dossier in racine:
            continue

        print(racine + "  " + str(sous_dossiers) + "  " + str(fichiers))

    if racine not in sys.path:
        sys.path.append(racine)