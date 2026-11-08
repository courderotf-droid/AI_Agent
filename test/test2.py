import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'mon_sous_dossier')))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# ---

# Récupérer le dossier où se trouve le script principal
dossier_principal = os.path.dirname(os.path.abspath(__file__))

# Parcourir récursivement tous les sous-dossiers
for racine, sous_dossiers, fichiers in os.walk(dossier_principal):
    # Optionnel : ignorer certains dossiers (comme .git, __pycache__, venv, etc.)
    if '__pycache__' in racine or '.git' in racine:
        continue

    # Ajouter le sous-dossier courant à sys.path s'il n'y est pas déjà
    if racine not in sys.path:
        sys.path.append(racine)