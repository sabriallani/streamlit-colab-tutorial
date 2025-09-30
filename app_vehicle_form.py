"""Application 1 : formulaire d'achat de véhicule.

Cette application Streamlit illustre comment regrouper plusieurs widgets
dans un formulaire (`st.form`) afin de collecter des informations sur
l'achat d'un véhicule. Les données saisies sont stockées dans
`st.session_state` sous forme de DataFrame et peuvent être réutilisées
par d'autres pages (par exemple pour la visualisation). Chaque section
du formulaire est commentée en français pour faciliter la compréhension.
"""

import streamlit as st
import pandas as pd
from datetime import date

# Initialisation de l'état de session pour stocker les achats.
# La variable `vehicle_data` est une table (DataFrame) avec des colonnes
# correspondant aux champs du formulaire. Si elle n'existe pas encore
# dans `st.session_state`, on la crée vide au démarrage de l'application.
if "vehicle_data" not in st.session_state:
    st.session_state["vehicle_data"] = pd.DataFrame(
        columns=[
            "Nom", "Contact", "Type", "Modèle", "Prix", "Date",
            "Paiement", "Commentaires",
        ]
    )

# Titre de la page
st.title("Formulaire d'achat de véhicule")

# Construction du formulaire. Tous les widgets définis à l'intérieur du
# bloc `with st.form()` seront envoyés en une seule fois lorsque
# l'utilisateur cliquera sur le bouton de soumission. Cela permet de
# contrôler précisément quand les valeurs sont envoyées au serveur【472898386844030†L193-L204】.
with st.form(key="vehicle_form"):
    # Champs textuels pour le nom et le contact
    nom = st.text_input("Nom et prénom du client")
    contact = st.text_input("Contact (email ou téléphone)")

    # Liste déroulante pour le type de véhicule
    type_vehicule = st.selectbox(
        "Type de véhicule",
        [
            "SUV", "Citadine", "Berline", "Pickup", "Fourgon", "Autre",
        ],
    )

    # Saisie du modèle ou de la marque
    modele = st.text_input("Modèle / Marque")

    # Saisie du prix avec un champ numérique (acceptant des décimales)
    prix = st.number_input(
        "Prix (€)", min_value=0.0, step=500.0, format="%.2f"
    )

    # Date d'achat. `st.date_input` affiche un sélecteur de date
    # configurable et retourne un objet date【648397162177243†L249-L259】.
    date_achat = st.date_input(
        "Date d'achat", value=date.today(), format="DD/MM/YYYY"
    )

    # Choix du mode de paiement
    mode_paiement = st.selectbox(
        "Mode de paiement", ["Comptant", "Financement", "Location longue durée"]
    )

    # Zone de texte pour des commentaires supplémentaires
    commentaires = st.text_area(
        "Commentaires supplémentaires", height=100, placeholder="Notes sur la transaction…"
    )

    # Bouton de soumission. Selon la documentation, chaque formulaire
    # doit contenir au moins un `st.form_submit_button`【472898386844030†L193-L204】.
    submitted = st.form_submit_button("Envoyer")

    # Lorsque l'utilisateur clique sur le bouton, on ajoute la ligne au
    # DataFrame stocké dans la session. Pandas concatène la nouvelle
    # ligne au tableau existant et met à jour l'état de session.
    if submitted:
        new_record = pd.DataFrame(
            [[
                nom,
                contact,
                type_vehicule,
                modele,
                prix,
                date_achat,
                mode_paiement,
                commentaires,
            ]],
            columns=st.session_state["vehicle_data"].columns,
        )
        st.session_state["vehicle_data"] = pd.concat(
            [st.session_state["vehicle_data"], new_record], ignore_index=True
        )
        # Message de confirmation
        st.success("Données enregistrées avec succès.")

# Affichage de la table courante
if not st.session_state["vehicle_data"].empty:
    st.subheader("Historique des achats")
    st.dataframe(st.session_state["vehicle_data"], use_container_width=True)
