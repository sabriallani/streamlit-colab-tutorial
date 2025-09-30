# Tutoriel : Trois Applications Streamlit pour Google Colab

Ce tutoriel explique comment construire trois mini-applications Streamlit en Python, optimisées pour fonctionner dans l'environnement Google Colab :

1. **Formulaire d'achat de véhicule** – collecte des informations via un formulaire structuré et les enregistre dans la session
2. **Chatbot simple** – illustre l'utilisation des éléments de chat pour créer une conversation interactive sans dépendance externe
3. **Visualisation des achats** – regroupe et affiche les données collectées sous forme de tableau et de diagramme en barres

Le tutoriel est rédigé en français et chaque étape est commentée pour aider à la compréhension.

## Structure du Projet

```
streamlit-colab-tutorial/
├── app_vehicle_form.py          # Application du formulaire
├── app_chatbot.py               # Application du chatbot
├── app_data_visualization.py    # Application de visualisation
└── README.md                    # Ce fichier
```

## 1. Préparation de l'Environnement

### Installation des Dépendances

Dans un nouveau notebook Google Colab, exécutez la cellule suivante :

```python
!pip install streamlit pandas matplotlib seaborn pyngrok
```

**Description des packages :**
- `streamlit` : Framework pour créer des applications web interactives
- `pandas` : Manipulation de données et DataFrames
- `matplotlib` & `seaborn` : Visualisation de données
- `pyngrok` : Exposition d'un port local sur Internet (pour Colab)

### Configuration de l'Environnement Colab

```python
# Télécharger les fichiers du projet (optionnel si vous les créez manuellement)
import os
import wget

# Créer le répertoire de travail
os.makedirs('streamlit_apps', exist_ok=True)
os.chdir('streamlit_apps')
```

### Création des Fichiers d'Application

Utilisez la commande magique `%%writefile` pour créer chaque fichier :

```python
%%writefile app_vehicle_form.py
# Le contenu du fichier sera collé ici
```

## 2. Application 1 : Formulaire d'Achat de Véhicule

### Fonctionnalités Principales

- **Formulaire structuré** avec validation des données
- **Persistance des données** dans `st.session_state`
- **Interface utilisateur intuitive** avec différents types de widgets

### Code Principal

```python
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

### Points Clés

1. **Gestion de l'état** : Utilisation de `st.session_state` pour persister les données
2. **Validation** : Vérification des champs obligatoires avant l'enregistrement
3. **Interface responsive** : Utilisation de colonnes pour optimiser l'espace
4. **Feedback utilisateur** : Messages de succès et d'erreur appropriés

## 3. Application 2 : Chatbot Simple

### Fonctionnalités

- **Interface de chat moderne** avec `st.chat_message` et `st.chat_input`
- **Historique de conversation** persistant
- **Réponses contextuelles** basées sur des mots-clés

### Code Principal

```python
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
    
    # Bouton pour effacer l'historique
    st.markdown("---")
    if st.button("🗑️ Effacer l'historique", type="secondary"):
        st.session_state["messages"] = []
        init_chat_history()
        st.rerun()

if __name__ == "__main__":
    main()
```

### Améliorations Possibles

- **Intégration d'API** : Connexion à des services comme OpenAI GPT
- **Base de connaissances** : Réponses basées sur une FAQ
- **Analyse de sentiment** : Adaptation du ton selon l'humeur de l'utilisateur

## 4. Application 3 : Visualisation des Achats

### Fonctionnalités

- **Tableau filtrable** par type de véhicule
- **Graphiques interactifs** avec Streamlit
- **Statistiques descriptives** des données

### Code Principal

```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_vehicle_data():
    """Charge les données de véhicules depuis la session."""
    if "vehicle_data" not in st.session_state:
        st.session_state["vehicle_data"] = pd.DataFrame()
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
        
        # Graphique en barres par type
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Nombre d'achats par type**")
            type_counts = df_filtre['Type'].value_counts()
            st.bar_chart(type_counts)
        
        with col2:
            st.write("**Prix moyen par type**")
            prix_moyen = df_filtre.groupby('Type')['Prix'].mean()
            st.bar_chart(prix_moyen)
        
        # Graphique de distribution des prix
        st.write("**Distribution des prix**")
        fig, ax = plt.subplots(figsize=(10, 6))
        
        sns.histplot(data=df_filtre, x='Prix', bins=10, kde=True, ax=ax)
        ax.set_title('Distribution des Prix des Véhicules')
        ax.set_xlabel('Prix (€)')
        ax.set_ylabel('Fréquence')
        
        st.pyplot(fig)
        
        # Graphique temporel
        if 'Date_Achat' in df_filtre.columns:
            st.write("**Évolution des achats dans le temps**")
            df_filtre['Date_Achat'] = pd.to_datetime(df_filtre['Date_Achat'])
            achats_par_date = df_filtre.groupby('Date_Achat').size()
            st.line_chart(achats_par_date)

if __name__ == "__main__":
    main()
```

## 5. Déploiement sur Google Colab

### Méthode 1 : Utilisation de pyngrok

```python
# Installation et configuration de ngrok
from pyngrok import ngrok
import subprocess
import threading

def run_streamlit():
    subprocess.run(["streamlit", "run", "app_vehicle_form.py", "--server.port", "8501"])

# Lancer Streamlit en arrière-plan
thread = threading.Thread(target=run_streamlit)
thread.daemon = True
thread.start()

# Exposer le port avec ngrok
public_url = ngrok.connect(8501)
print(f"🌐 Application accessible à : {public_url}")
```

### Méthode 2 : Utilisation de LocalTunnel

```python
import subprocess
import time

# Lancer Streamlit
subprocess.Popen(["streamlit", "run", "app_vehicle_form.py", "--server.port", "8501"])

# Attendre que le serveur démarre
time.sleep(5)

# Installer et utiliser localtunnel
subprocess.run(["npm", "install", "-g", "localtunnel"])
subprocess.run(["lt", "--port", "8501"])
```

## 6. Conseils d'Optimisation

### Performance

- **Mise en cache** : Utilisez `@st.cache_data` pour les opérations coûteuses
- **Session State** : Minimisez les données stockées en session
- **Composants** : Séparez la logique en fonctions réutilisables

### Interface Utilisateur

- **Responsive Design** : Utilisez `st.columns()` pour l'adaptabilité
- **Feedback Visuel** : Implémentez des messages de statut clairs
- **Navigation** : Créez une barre latérale pour les options avancées

### Sécurité

- **Validation des entrées** : Vérifiez toujours les données utilisateur
- **Gestion d'erreurs** : Implémentez une gestion robuste des exceptions
- **Limites** : Définissez des limites sur les tailles de données

## 7. Extensions Possibles

### Fonctionnalités Avancées

1. **Base de données** : Intégration avec SQLite ou PostgreSQL
2. **Authentification** : Système de connexion utilisateur
3. **Export de données** : Téléchargement en CSV, Excel, PDF
4. **Notifications** : Alertes email ou SMS
5. **API REST** : Intégration avec des services externes

### Améliorations Techniques

1. **Tests unitaires** : Framework pytest pour la validation
2. **Documentation** : Génération automatique avec Sphinx
3. **CI/CD** : Intégration continue avec GitHub Actions
4. **Containerisation** : Déploiement avec Docker

## Conclusion

Ce tutoriel présente les bases pour créer des applications Streamlit interactives dans Google Colab. Les trois exemples couvrent les aspects essentiels :

- **Collecte de données** avec des formulaires structurés
- **Interaction utilisateur** via un système de chat
- **Visualisation** et analyse de données

Le code est modulaire et extensible, permettant d'ajouter facilement de nouvelles fonctionnalités selon vos besoins.

## Ressources Utiles

- [Documentation officielle Streamlit](https://docs.streamlit.io/)
- [Galerie d'applications Streamlit](https://streamlit.io/gallery)
- [Forum communautaire](https://discuss.streamlit.io/)
- [GitHub - Exemples Streamlit](https://github.com/streamlit/streamlit-example)

## Licence

Ce projet est distribué sous licence MIT. Vous êtes libre de l'utiliser, le modifier et le distribuer selon les termes de cette licence.

---

*Créé avec ❤️ pour la communauté francophone de développeurs Python*
