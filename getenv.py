from pathlib import Path
from dotenv import load_dotenv
import os

dossier_actuel = Path(__file__).parent
load_dotenv(dossier_actuel / "settings.env")

MODE_TEST = os.getenv('MODE_TEST', 'False') == 'True'
TELEGRAM = os.getenv('TELEGRAM', 'False') == 'True'
HISTORIQUE = os.getenv('HISTORIQUE', 'False') == 'True'
LLM_ENGINE = os.getenv('LLM_ENGINE')

if LLM_ENGINE == 'ollama':
    OLLAMA_MODELE = os.getenv('OLLAMA_MODELE')