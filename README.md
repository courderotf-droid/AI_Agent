# AI Agent

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Agent** est un projet encore non abouti pour un assistant conversationnel intelligent et modulaire écrit en Python. Il intègre des capacités de communication avec des modèles locaux via Ollama ainsi qu'une passerelle de messagerie Telegram.

---

## 📂 Structure du Projet
```
ai_agent/
├── apis/                              # Modules d'intégration avec les API externes
│   ├── lien_telegram.py               # Gestion des interactions avec le bot Telegram
│   └── ollama_api.py                  # Interface de communication avec l'API Ollama
├── data/                              # Fichiers de données, de configuration et journaux de stockage
│   ├── chat_history.json              # Stockage de l'historique des conversations
│   └── prompts.json                   # Configuration et personnalisation des prompts
├── display/                           # Modules d'affichage et gestion des retours console/erreurs
│   ├── gestion_erreurs.py             # Gestion centralisée des exceptions et erreurs
│   └── style_print.py                 # Mise en forme et styles des affichages console
├── logs/                              # Logique de gestion des logs et de l'historique
│   ├── history_logs.py                # Gestion et persistance de l'historique des conversations
│   ├── logger.py                      # Système de journalisation (logs)
│   └── logs.log                       # Fichier de journalisation des événements
├── getenv.py                          # Chargement sécurisé des variables d'environnement
├── licence.txt                        # Fichier de licence du projet
├── main.py                            # Point d'entrée principal de l'agent
├── README.md                          # Documentation principale du projet
├── requierements.txt                  # Dépendances et bibliothèques requises
├── récupérer_texte_telegram.py        # Récupération et traitement des messages entrants Telegram
└── settings.env                       # Fichier de configuration des variables d'environnement
```
---

## ✨ Fonctionnalités

- **Intégration Ollama** : Utilisation de modèles de langage exécutés localement pour des réponses rapides et sécurisées.
- **Passerelle Telegram** : Possibilité d'interagir avec l'agent directement via l'application de messagerie Telegram.
- **Historique Persistant** : Sauvegarde automatique des échanges dans `chat_history.json` pour conserver le contexte des conversations.
- **Gestion des Erreurs et Logs** : Suivi rigoureux des événements et de la stabilité de l'application grâce au module de journalisation.
- **Configuration Flexible** : Personnalisation facile des comportements de l'agent via des fichiers de configuration (`settings.env` et `prompts.json`).

---

## ⚙️ Installation & Configuration

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/votre-nom-d-utilisateur/ai_agent.git
   cd ai_agent
   ```

2. **Créer et activer un environnement virtuel :**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate
   ```

3. **Installer les dépendances :**
   ```bash
   pip install -r requierements.txt
   ```

4. **Configurer les variables d'environnement :**
   Remplissez les informations requises dans le fichier `settings.env` (tokens Telegram, URL Ollama, etc.).

---

## 🚀 Utilisation

Pour lancer l'agent IA :
```
bash
python main.py
```
---

## 📄 Licence

Ce projet est sous licence [MIT](LICENSE).
