app_data_visualization.py"""Application 3 : Visualisation des données d'achat.

Cette application lit les données stockées par le formulaire d'achat de
véhicule (voir `app_vehicle_form.py`) et propose un filtrage par type
de véhicule. Une fois filtrées, les données sont affichées puis
agrégées pour produire un graphique. La fonction `st.bar_chart` est
utilisée pour afficher un diagramme en barres de manière simple :
elle construit automatiquement la spécification Altair en se basant
sur les colonnes du DataFrame【54672515633451†L209-L214】, ce qui
simplifie la création du graphique【54672515633451†L218-L239】.
"""

import streamlit as st
import pandas as pd

st.title("Visualisation des données d'achat")

# Vérifier la présence de données. Si la table est vide, on informe
# l'utilisateur qu'aucune donnée n'est disponible.
data = st.session_state.get("vehicle_data")
if data is None or data.empty:
    st.info(
        "Aucune donnée disponible. Veuillez d'abord saisir des achats via l'application du formulaire."
    )
else:
    # Choisir les types à afficher. `st.multiselect` permet de
    # sélectionner plusieurs options à partir des valeurs uniques de la
    # colonne 'Type'. Par défaut, toutes les catégories sont cochées.
    types_disponibles = sorted(data["Type"].unique())
    selection_types = st.multiselect(
        "Filtrer par type de véhicule",
        options=types_disponibles,
        default=types_disponibles,
    )

    # Filtrer le DataFrame selon la sélection
    df_filtre = data[data["Type"].isin(selection_types)]

    st.subheader("Données filtrées")
    st.dataframe(df_filtre, use_container_width=True)

    # Agréger les données pour obtenir le nombre d'achats par type
    counts = (
        df_filtre.groupby("Type")["Nom"]
        .count()
        .reset_index()
        .rename(columns={"Nom": "Nombre d'achats"})
    )

    st.subheader("Graphique du nombre d'achats par type")
    # Le paramètre `set_index` est utilisé pour que la colonne 'Type'
    # devienne l'axe des x et que la colonne de comptage soit tracée en y.
    st.bar_chart(counts.set_index("Type"))
