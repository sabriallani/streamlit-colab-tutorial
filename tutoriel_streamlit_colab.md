# Tutoriel : Trois Applications Streamlit pour Google Colab

Ce tutoriel explique comment construire et exécuter trois mini-applications Streamlit directement dans Google Colab, sans avoir besoin d'un environnement de développement local.

## 🚀 Configuration Initiale dans Google Colab

### Cellule 1 : Installation des Dépendances

```python
# Installation des packages nécessaires
!pip install streamlit pyngrok pandas matplotlib seaborn plotly

# Import des modules
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime
import random
import subprocess
import threading
import time
from pyngrok import ngrok
```

### Cellule 2 : Configuration de l'Authentification ngrok

```python
# Configuration de ngrok (remplacez par votre token)
# Obtenez un token gratuit sur https://ngrok.com/
ngrok.set_auth_token("VOTRE_TOKEN_NGROK_ICI")  # Remplacez par votre token
```

## 📝 Application 1 : Formulaire d'Achat de Véhicule

### Cellule 3 : Code du Formulaire

```python
%%writefile app_vehicle_form.py
import streamlit as st
import pandas as pd
from datetime import datetime

def init_vehicle_data():
    """Initialise les données de véhicules dans la session."""
    if "vehicle_data" not in st.session_state:
        st.session_state["vehicle_data"] = pd.DataFrame(columns=[
            "Nom", "Contact", "Type", "Prix", "Mode_Paiement", "Date_Achat"
        ])

def main():
    st.set_page_config(
        page_title="Formulaire Véhicule",
        page_icon="🚗",
        layout="wide"
    )
    
    st.title("🚗 Formulaire d'Achat de Véhicule")
    st.markdown("---")
    
    init_vehicle_data()
    
    # Création du formulaire
    with st.form(key="vehicle_form", clear_on_submit=True):
        st.subheader("Informations d'Achat")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom complet *", placeholder="Ex: Jean Dupont")
            contact = st.text_input("Contact *", placeholder="Email ou téléphone")
            
        with col2:
            type_vehicule = st.selectbox(
                "Type de véhicule *",
                ["Voiture", "Moto", "Camion", "SUV", "Autre"]
            )
            prix = st.number_input(
                "Prix (€) *", 
                min_value=0.0, 
                step=100.0,
                format="%.2f"
            )
        
        mode_paiement = st.selectbox(
            "Mode de paiement *",
            ["Comptant", "Crédit", "Leasing", "Autre"]
        )
        
        date_achat = st.date_input(
            "Date d'achat *",
            value=datetime.now().date()
        )
        
        # Bouton de soumission
        submitted = st.form_submit_button("💾 Enregistrer l'Achat", type="primary")
        
        if submitted:
            # Validation des champs obligatoires
            if not nom or not contact or prix <= 0:
                st.error("⚠️ Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Ajout des données
                nouvelle_ligne = pd.DataFrame({
                    "Nom": [nom],
                    "Contact": [contact],
                    "Type": [type_vehicule],
                    "Prix": [prix],
                    "Mode_Paiement": [mode_paiement],
                    "Date_Achat": [date_achat]
                })
                
                st.session_state["vehicle_data"] = pd.concat([
                    st.session_state["vehicle_data"], 
                    nouvelle_ligne
                ], ignore_index=True)
                
                st.success(f"✅ Achat de {nom} enregistré avec succès !")
    
    # Affichage de l'historique
    st.markdown("---")
    st.subheader("📊 Historique des Achats")
    
    if not st.session_state["vehicle_data"].empty:
        st.dataframe(
            st.session_state["vehicle_data"],
            use_container_width=True,
            hide_index=True
        )
        st.info(f"📈 Total : {len(st.session_state['vehicle_data'])} achat(s) enregistré(s)")
    else:
        st.info("🔍 Aucun achat enregistré pour le moment.")

if __name__ == "__main__":
    main()
```

### Cellule 4 : Lancement du Formulaire

```python
# Fonction pour lancer Streamlit en arrière-plan
def run_streamlit_form():
    subprocess.run(["streamlit", "run", "app_vehicle_form.py", "--server.port", "8501", "--server.headless", "true"])

# Arrêter les processus existants
!pkill -f streamlit

# Lancer l'application en arrière-plan
thread = threading.Thread(target=run_streamlit_form)
thread.daemon = True
thread.start()

# Attendre que le serveur démarre
time.sleep(10)

# Créer le tunnel public
public_url = ngrok.connect(8501)
print(f"🌐 Application Formulaire accessible à : {public_url}")
```

## 🤖 Application 2 : Chatbot Simple

### Cellule 5 : Code du Chatbot

```python
%%writefile app_chatbot.py
import streamlit as st
import random
from datetime import datetime

def init_chat_history():
    """Initialise l'historique du chat."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "👋 Bonjour ! Je suis votre assistant virtuel. Comment puis-je vous aider aujourd'hui ?",
                "timestamp": datetime.now()
            }
        ]

def get_bot_response(user_message):
    """Génère une réponse basée sur le message utilisateur."""
    message_lower = user_message.lower()
    
    # Réponses contextuelles
    responses = {
        "bonjour": [
            "Bonjour ! Comment allez-vous ?",
            "Salut ! Que puis-je faire pour vous ?",
            "Hello ! Ravi de vous parler !"
        ],
        "voiture": [
            "🚗 Les voitures sont fascinantes ! Quel type vous intéresse ?",
            "🔧 Avez-vous des questions sur l'entretien automobile ?",
            "🚙 Électrique, essence ou hybride ?"
        ],
        "prix": [
            "💰 Les prix varient selon le modèle et l'année.",
            "💵 Quel est votre budget approximatif ?",
            "📊 Souhaitez-vous comparer des prix ?"
        ],
        "aide": [
            "🤝 Je suis là pour vous aider ! Posez-moi vos questions.",
            "📞 N'hésitez pas à me demander ce dont vous avez besoin.",
            "💡 Je peux vous renseigner sur les véhicules et leurs caractéristiques."
        ],
        "merci": [
            "De rien ! 😊",
            "Avec plaisir !",
            "C'est un plaisir de vous aider !"
        ]
    }
    
    # Recherche de mots-clés
    for keyword, possible_responses in responses.items():
        if keyword in message_lower:
            return random.choice(possible_responses)
    
    # Réponse par défaut
    default_responses = [
        "🤔 Intéressant ! Pouvez-vous me donner plus de détails ?",
        "📝 Je prends note. Que souhaitez-vous savoir d'autre ?",
        "💭 C'est une bonne question ! Laissez-moi y réfléchir...",
        "🎯 Je comprends votre point de vue. Comment puis-je vous aider davantage ?"
    ]
    
    return random.choice(default_responses)

def main():
    st.set_page_config(
        page_title="Chatbot Assistant",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Assistant Virtuel")
    st.markdown("*Votre compagnon conversationnel intelligent*")
    st.markdown("---")
    
    init_chat_history()
    
    # Affichage de l'historique des messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if "timestamp" in message:
                    st.caption(f"📅 {message['timestamp'].strftime('%H:%M:%S')}")
    
    # Interface de saisie
    if prompt := st.chat_input("💬 Tapez votre message ici..."):
        # Ajout du message utilisateur
        user_message = {
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now()
        }
        st.session_state["messages"].append(user_message)
        
        # Affichage du message utilisateur
        with st.chat_message("user"):
            st.write(prompt)
            st.caption(f"📅 {user_message['timestamp'].strftime('%H:%M:%S')}")
        
        # Génération et affichage de la réponse
        bot_response = get_bot_response(prompt)
        assistant_message = {
            "role": "assistant",
            "content": bot_response,
            "timestamp": datetime.now()
        }
        st.session_state["messages"].append(assistant_message)
        
        with st.chat_message("assistant"):
            st.write(bot_response)
            st.caption(f"📅 {assistant_message['timestamp'].strftime('%H:%M:%S')}")
    
    # Sidebar avec options
    with st.sidebar:
        st.header("🛠️ Options")
        
        if st.button("🗑️ Effacer l'historique", type="secondary"):
            st.session_state["messages"] = []
            init_chat_history()
            st.rerun()
        
        st.markdown("---")
        st.subheader("📊 Statistiques")
        nb_messages = len(st.session_state["messages"])
        st.metric("Messages échangés", nb_messages)

if __name__ == "__main__":
    main()
```

### Cellule 6 : Lancement du Chatbot

```python
# Arrêter les processus précédents
!pkill -f streamlit
time.sleep(3)

# Fonction pour lancer le chatbot
def run_streamlit_chat():
    subprocess.run(["streamlit", "run", "app_chatbot.py", "--server.port", "8502", "--server.headless", "true"])

# Lancer l'application
thread = threading.Thread(target=run_streamlit_chat)
thread.daemon = True
thread.start()

# Attendre que le serveur démarre
time.sleep(10)

# Créer le tunnel public
public_url = ngrok.connect(8502)
print(f"🤖 Application Chatbot accessible à : {public_url}")
```

## 📊 Application 3 : Visualisation des Achats

### Cellule 7 : Code de Visualisation

```python
%%writefile app_data_visualization.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def load_vehicle_data():
    """Charge les données de véhicules depuis la session."""
    if "vehicle_data" not in st.session_state:
        # Créer des données d'exemple pour la démonstration
        sample_data = pd.DataFrame({
            "Nom": ["Jean Dupont", "Marie Martin", "Pierre Durand", "Sophie Leblanc", "Paul Rousseau"],
            "Contact": ["jean@email.com", "marie@email.com", "pierre@email.com", "sophie@email.com", "paul@email.com"],
            "Type": ["Voiture", "SUV", "Moto", "Voiture", "Camion"],
            "Prix": [25000, 45000, 8000, 30000, 55000],
            "Mode_Paiement": ["Crédit", "Comptant", "Comptant", "Crédit", "Leasing"],
            "Date_Achat": pd.to_datetime(["2024-01-15", "2024-02-20", "2024-03-10", "2024-04-05", "2024-05-12"])
        })
        st.session_state["vehicle_data"] = sample_data
    
    return st.session_state["vehicle_data"]

def create_summary_stats(df):
    """Crée des statistiques résumées."""
    if df.empty:
        return None
    
    stats = {
        "Total des achats": len(df),
        "Prix moyen": f"{df['Prix'].mean():.2f} €",
        "Prix médian": f"{df['Prix'].median():.2f} €",
        "Prix total": f"{df['Prix'].sum():.2f} €",
        "Type le plus populaire": df['Type'].mode().iloc[0] if not df['Type'].mode().empty else "N/A"
    }
    return stats

def main():
    st.set_page_config(
        page_title="Visualisation des Achats",
        page_icon="📊",
        layout="wide"
    )
    
    st.title("📊 Visualisation des Achats de Véhicules")
    st.markdown("*Analyse et visualisation des données d'achat*")
    st.markdown("---")
    
    # Chargement des données
    df = load_vehicle_data()
    
    if df.empty:
        st.warning("⚠️ Aucune donnée disponible.")
        st.info("💡 Utilisez d'abord l'application de formulaire pour enregistrer des achats.")
        st.stop()
    
    # Sidebar pour les filtres
    st.sidebar.header("🔧 Filtres")
    
    # Filtre par type de véhicule
    types_disponibles = df['Type'].unique().tolist()
    types_selectionnes = st.sidebar.multiselect(
        "Sélectionner les types de véhicules",
        options=types_disponibles,
        default=types_disponibles,
        help="Choisissez un ou plusieurs types pour filtrer les données"
    )
    
    # Filtre par gamme de prix
    if not df['Prix'].empty:
        prix_min, prix_max = st.sidebar.slider(
            "Gamme de prix (€)",
            min_value=float(df['Prix'].min()),
            max_value=float(df['Prix'].max()),
            value=(float(df['Prix'].min()), float(df['Prix'].max())),
            step=100.0
        )
    else:
        prix_min, prix_max = 0.0, 100000.0
    
    # Application des filtres
    df_filtre = df[
        (df['Type'].isin(types_selectionnes)) &
        (df['Prix'] >= prix_min) &
        (df['Prix'] <= prix_max)
    ]
    
    # Affichage des statistiques
    st.subheader("📈 Statistiques Générales")
    stats = create_summary_stats(df_filtre)
    
    if stats:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Total achats", stats["Total des achats"])
        with col2:
            st.metric("Prix moyen", stats["Prix moyen"])
        with col3:
            st.metric("Prix médian", stats["Prix médian"])
        with col4:
            st.metric("Prix total", stats["Prix total"])
        with col5:
            st.metric("Type populaire", stats["Type le plus populaire"])
    
    st.markdown("---")
    
    # Tableau des données filtrées
    st.subheader("📋 Données Filtrées")
    if not df_filtre.empty:
        st.dataframe(
            df_filtre,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("🔍 Aucune donnée ne correspond aux filtres sélectionnés.")
    
    st.markdown("---")
    
    # Visualisations
    if not df_filtre.empty:
        st.subheader("📊 Visualisations")
        
        # Ligne 1 : Graphiques en barres
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Nombre d'achats par type**")
            type_counts = df_filtre['Type'].value_counts()
            fig1 = px.bar(
                x=type_counts.index, 
                y=type_counts.values,
                labels={'x': 'Type de véhicule', 'y': 'Nombre d\'achats'},
                title="Distribution par type"
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.write("**Prix moyen par type**")
            prix_moyen = df_filtre.groupby('Type')['Prix'].mean()
            fig2 = px.bar(
                x=prix_moyen.index,
                y=prix_moyen.values,
                labels={'x': 'Type de véhicule', 'y': 'Prix moyen (€)'},
                title="Prix moyen par type"
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Ligne 2 : Graphiques avancés
        col3, col4 = st.columns(2)
        
        with col3:
            st.write("**Distribution des prix**")
            fig3 = px.histogram(
                df_filtre, 
                x='Prix', 
                nbins=10,
                title="Distribution des prix",
                labels={'Prix': 'Prix (€)', 'count': 'Fréquence'}
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col4:
            st.write("**Répartition par mode de paiement**")
            paiement_counts = df_filtre['Mode_Paiement'].value_counts()
            fig4 = px.pie(
                values=paiement_counts.values,
                names=paiement_counts.index,
                title="Modes de paiement"
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        # Graphique temporel
        if 'Date_Achat' in df_filtre.columns:
            st.write("**Évolution des achats dans le temps**")
            df_filtre['Date_Achat'] = pd.to_datetime(df_filtre['Date_Achat'])
            achats_par_date = df_filtre.groupby(df_filtre['Date_Achat'].dt.date).size().reset_index()
            achats_par_date.columns = ['Date', 'Nombre_Achats']
            
            fig5 = px.line(
                achats_par_date,
                x='Date',
                y='Nombre_Achats',
                title="Évolution temporelle des achats",
                markers=True
            )
            st.plotly_chart(fig5, use_container_width=True)
    
    # Section d'export
    st.markdown("---")
    st.subheader("💾 Export des Données")
    
    if st.button("📥 Télécharger les données (CSV)", type="primary"):
        csv = df_filtre.to_csv(index=False)
        st.download_button(
            label="Cliquez ici pour télécharger",
            data=csv,
            file_name=f"achats_vehicules_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
```

### Cellule 8 : Lancement de la Visualisation

```python
# Arrêter les processus précédents
!pkill -f streamlit
time.sleep(3)

# Fonction pour lancer la visualisation
def run_streamlit_viz():
    subprocess.run(["streamlit", "run", "app_data_visualization.py", "--server.port", "8503", "--server.headless", "true"])

# Lancer l'application
thread = threading.Thread(target=run_streamlit_viz)
thread.daemon = True
thread.start()

# Attendre que le serveur démarre
time.sleep(10)

# Créer le tunnel public
public_url = ngrok.connect(8503)
print(f"📊 Application Visualisation accessible à : {public_url}")
```

## 🎯 Application Complète Multi-Pages

### Cellule 9 : Application Intégrée (Optionnel)

```python
%%writefile app_complete.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

# Configuration de la page
st.set_page_config(
    page_title="Gestion de Véhicules",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_data():
    """Initialise les données de base."""
    if "vehicle_data" not in st.session_state:
        st.session_state["vehicle_data"] = pd.DataFrame(columns=[
            "Nom", "Contact", "Type", "Prix", "Mode_Paiement", "Date_Achat"
        ])
    
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "👋 Bonjour ! Je suis votre assistant virtuel. Comment puis-je vous aider ?",
                "timestamp": datetime.now()
            }
        ]

def page_formulaire():
    """Page du formulaire d'achat."""
    st.title("🚗 Formulaire d'Achat de Véhicule")
    
    with st.form(key="vehicle_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom complet *")
            contact = st.text_input("Contact *")
            
        with col2:
            type_vehicule = st.selectbox("Type de véhicule *", ["Voiture", "Moto", "Camion", "SUV"])
            prix = st.number_input("Prix (€) *", min_value=0.0, step=100.0)
        
        mode_paiement = st.selectbox("Mode de paiement *", ["Comptant", "Crédit", "Leasing"])
        date_achat = st.date_input("Date d'achat *", value=datetime.now().date())
        
        if st.form_submit_button("💾 Enregistrer", type="primary"):
            if nom and contact and prix > 0:
                nouvelle_ligne = pd.DataFrame({
                    "Nom": [nom], "Contact": [contact], "Type": [type_vehicule],
                    "Prix": [prix], "Mode_Paiement": [mode_paiement], "Date_Achat": [date_achat]
                })
                st.session_state["vehicle_data"] = pd.concat([
                    st.session_state["vehicle_data"], nouvelle_ligne
                ], ignore_index=True)
                st.success("✅ Achat enregistré !")
            else:
                st.error("⚠️ Veuillez remplir tous les champs obligatoires")
    
    # Affichage des données
    if not st.session_state["vehicle_data"].empty:
        st.subheader("📊 Historique")
        st.dataframe(st.session_state["vehicle_data"], use_container_width=True, hide_index=True)

def page_chatbot():
    """Page du chatbot."""
    st.title("🤖 Assistant Virtuel")
    
    # Affichage des messages
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Interface de chat
    if prompt := st.chat_input("💬 Votre message..."):
        # Message utilisateur
        st.session_state["messages"].append({
            "role": "user", "content": prompt, "timestamp": datetime.now()
        })
        
        with st.chat_message("user"):
            st.write(prompt)
        
        # Réponse du bot
        responses = [
            "C'est intéressant ! Pouvez-vous me donner plus de détails ?",
            "Je comprends votre question. Comment puis-je vous aider davantage ?",
            "Merci pour votre message ! Que souhaitez-vous savoir d'autre ?"
        ]
        bot_response = random.choice(responses)
        
        st.session_state["messages"].append({
            "role": "assistant", "content": bot_response, "timestamp": datetime.now()
        })
        
        with st.chat_message("assistant"):
            st.write(bot_response)

def page_visualisation():
    """Page de visualisation."""
    st.title("📊 Visualisation des Données")
    
    df = st.session_state["vehicle_data"]
    
    if df.empty:
        st.info("🔍 Aucune donnée à afficher. Utilisez le formulaire pour ajouter des données.")
        return
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total achats", len(df))
    with col2:
        st.metric("Prix moyen", f"{df['Prix'].mean():.0f} €")
    with col3:
        st.metric("Prix total", f"{df['Prix'].sum():.0f} €")
    with col4:
        st.metric("Types uniques", df['Type'].nunique())
    
    # Graphiques
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Répartition par type")
        type_counts = df['Type'].value_counts()
        fig1 = px.pie(values=type_counts.values, names=type_counts.index)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Prix par type")
        fig2 = px.bar(df, x='Type', y='Prix', title="Prix par type de véhicule")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Tableau détaillé
    st.subheader("📋 Données Détaillées")
    st.dataframe(df, use_container_width=True, hide_index=True)

def main():
    """Fonction principale avec navigation."""
    init_data()
    
    # Sidebar pour la navigation
    st.sidebar.title("🚗 Navigation")
    page = st.sidebar.selectbox(
        "Choisir une page",
        ["📝 Formulaire", "🤖 Chatbot", "📊 Visualisation"]
    )
    
    # Affichage de la page sélectionnée
    if page == "📝 Formulaire":
        page_formulaire()
    elif page == "🤖 Chatbot":
        page_chatbot()
    elif page == "📊 Visualisation":
        page_visualisation()
    
    # Informations dans la sidebar
    st.sidebar.markdown("---")
    st.sidebar.info(f"📊 Données enregistrées : {len(st.session_state['vehicle_data'])}")
    st.sidebar.info(f"💬 Messages échangés : {len(st.session_state['messages'])}")

if __name__ == "__main__":
    main()
```

### Cellule 10 : Lancement de l'Application Complète

```python
# Arrêter tous les processus
!pkill -f streamlit
time.sleep(3)

# Fonction pour lancer l'application complète
def run_complete_app():
    subprocess.run(["streamlit", "run", "app_complete.py", "--server.port", "8504", "--server.headless", "true"])

# Lancer l'application
thread = threading.Thread(target=run_complete_app)
thread.daemon = True
thread.start()

# Attendre que le serveur démarre
time.sleep(10)

# Créer le tunnel public
public_url = ngrok.connect(8504)
print(f"🎯 Application Complète accessible à : {public_url}")
print(f"🚀 Utilisez cette URL pour accéder à toutes les fonctionnalités !")
```

## 🛠️ Gestion des Applications

### Cellule 11 : Utilitaires de Gestion

```python
# Fonction pour arrêter toutes les applications
def stop_all_apps():
    !pkill -f streamlit
    print("🛑 Toutes les applications Streamlit ont été arrêtées")

# Fonction pour voir les processus actifs
def show_active_processes():
    !ps aux | grep streamlit

# Fonction pour nettoyer les tunnels ngrok
def clean_ngrok():
    ngrok.kill()
    print("🧹 Tous les tunnels ngrok ont été fermés")

# Utilisation :
# stop_all_apps()
# show_active_processes()
# clean_ngrok()

print("🎛️ Fonctions de gestion disponibles :")
print("- stop_all_apps() : Arrête toutes les applications")
print("- show_active_processes() : Affiche les processus actifs")
print("- clean_ngrok() : Ferme tous les tunnels ngrok")
```

## 📋 Instructions d'Utilisation

### Étapes à Suivre dans Google Colab

1. **Exécuter les cellules 1-2** : Installation et configuration
2. **Choisir une application** :
   - Cellules 3-4 : Formulaire de véhicule
   - Cellules 5-6 : Chatbot
   - Cellules 7-8 : Visualisation
   - Cellules 9-10 : Application complète (recommandé)
3. **Accéder à l'application** via l'URL ngrok fournie
4. **Utiliser la cellule 11** pour gérer les applications

### Conseils Important

- ⚠️ **Token ngrok** : Obtenez un token gratuit sur [ngrok.com](https://ngrok.com/)
- 🔄 **Redémarrage** : Si une application plante, utilisez `stop_all_apps()` puis relancez
- 💾 **Données** : Les données sont perdues si vous fermez Colab
- 🌐 **URLs** : Les URLs ngrok changent à chaque redémarrage

### Dépannage

```python
# Si les applications ne démarrent pas :
!pip install --upgrade streamlit

# Pour voir les logs d'erreur :
!tail -f /root/.streamlit/logs/streamlit.log

# Pour libérer les ports :
!lsof -ti:8501,8502,8503,8504 | xargs kill -9
```

## 🎉 Conclusion

Ce tutoriel vous permet de créer et exécuter des applications Streamlit directement dans Google Colab. L'application complète (cellules 9-10) est recommandée car elle combine toutes les fonctionnalités en une seule interface avec navigation par onglets.

Les applications sont maintenant **entièrement fonctionnelles dans Google Colab** ! 🚀