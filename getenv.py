from pathlib import Path
from dotenv import load_dotenv
import os

dossier_actuel = Path(__file__).parent
load_dotenv(dossier_actuel / "settings.env")

MODE_TEST = os.getenv('MODE_TEST', 'False') == 'True'
TELEGRAM = os.getenv('TELEGRAM', 'False') == 'True'
MODELE = os.getenv('MODELE')
HISTORIQUE = os.getenv('HISTORIQUE', 'False') == 'True'