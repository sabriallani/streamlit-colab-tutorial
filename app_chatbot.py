"""Application 2 : Chatbot simple.

Cette application démontre comment utiliser les nouveaux éléments de
conversation de Streamlit (`st.chat_input` et `st.chat_message`) pour
créer une interface de chat. Les messages de l'utilisateur et de
l'assistant sont stockés dans `st.session_state` afin de conserver
l'historique. Un exemple de logique de réponse basique est fourni pour
illustrer comment traiter les requêtes de l'utilisateur. Dans un cas
réél, on intégrerait un modèle de langage externe, mais cet exemple
reste autonome.
"""

import streamlit as st

# Initialisation de l'historique des messages
if "messages" not in st.session_state:
    st.session_state["messages"] = []  # liste de dicts {'role': 'user'/'assistant', 'content': str}

st.title("Chatbot – exemple minimal")

# Afficher les messages enregistrés. Pour chaque message, on choisit un
# rôle ("user" ou "assistant") pour appliquer le style adapté. `st.chat_message`
# insère un conteneur de message dans l'application【266638346480461†L188-L223】.
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Zone de saisie de chat. `st.chat_input` affiche un champ de
# conversation avec un texte indicatif et peut limiter le nombre de
# caractères【911194705357470†L188-L223】.
prompt = st.chat_input("Votre message…")

if prompt:
    # Ajouter le message de l'utilisateur à l'historique
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Logique de réponse simple. On analyse des mots-clés pour retourner
    # une phrase pré-définie. Cette partie peut être remplacée par une
    # intégration avec un modèle de langage ou une API externe.
    lower_prompt = prompt.lower()
    if "prix" in lower_prompt:
        response = "Les informations de prix sont disponibles dans l'application du formulaire."
    elif "bonjour" in lower_prompt or "salut" in lower_prompt:
        response = "Bonjour ! Comment puis-je vous aider aujourd'hui ?"
    elif "merci" in lower_prompt:
        response = "Avec plaisir !"
    else:
        response = "Je suis un simple robot d'exemple et je ne comprends pas encore cette requête."

    # Afficher la réponse et l'ajouter à l'historique
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state["messages"].append({"role": "assistant", "content": response})
