# Workshop Streamlit : Création d’Applications Web Interactives

Ce workshop vous guide dans l’apprentissage de Streamlit, une bibliothèque Python pour créer des applications web interactives. Vous développerez deux applications principales : une pour gérer une connexion à une base de données SQLite (créée automatiquement avec des données par défaut) et une autre pour visualiser des données CSV sous forme de graphiques. Chaque section comprend des instructions, du code à compléter et des tâches pour approfondir vos compétences. Testez vos codes souvent pour une expérience interactive !

**Prérequis :**
- Python 3.8+ installé.
- Un éditeur de code (ex. : VS Code, PyCharm).
- Connaissances de base en Python (variables, fonctions, pandas, matplotlib).
- Installez les dépendances nécessaires dans un terminal :
  ```
  pip install streamlit pandas matplotlib sqlite3
  ```

**Durée estimée :** 4 à 6 heures.

**Instructions générales :**
- Créez un dossier pour vos fichiers (ex. : `Streamlit_Workshop`).
- Testez vos applications avec la commande :
  ```
  streamlit run nom_du_fichier.py
  ```
- Ouvrez l’application dans votre navigateur (généralement http://localhost:8501).
- Ajoutez des commentaires clairs dans votre code.
- À la fin, préparez un court résumé (PDF ou Word) de vos apprentissages, des défis rencontrés et des solutions trouvées.

---

## Section 1 : Découverte de Streamlit

**Objectif :** Créer une première application simple avec Streamlit.

1. Créez un fichier `app_basique.py` avec le code suivant :

```python
import streamlit as st

st.title("Ma Première Application Streamlit")
st.write("Bonjour, monde !")

nom = st.text_input("Entrez votre nom :")
if st.button("Saluer"):
    st.write(f"Bonjour, {nom} !")
```

2. Lancez l’application avec :
   ```
   streamlit run app_basique.py
   ```

3. **Tâche :** Ajoutez un slider pour sélectionner un âge (entre 0 et 100). Affichez un message personnalisé : "Bonjour, [nom], vous êtes majeur !" si l’âge est supérieur à 18, sinon "Bonjour, [nom], vous êtes mineur !".

**Résultat attendu :** Testez et partagez votre application modifiée avec le groupe.

---

## Section 2 : Application de Connexion à une Base de Données SQLite

**Objectif :** Créer une interface pour se connecter à une base de données SQLite, qui est automatiquement créée avec des données par défaut.

**Instructions :**

1. Créez un fichier `app_config_bdd.py` avec le code suivant :

```python
import streamlit as st
import sqlite3

# Fonction pour initialiser la base de données avec des données par défaut
def init_db():
    conn = sqlite3.connect('ma_bdd.db')
    c = conn.cursor()
    # Créer la table utilisateurs si elle n'existe pas
    c.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (id INTEGER PRIMARY KEY, nom TEXT, age INTEGER)''')
    # Insérer des données par défaut si la table est vide
    c.execute("SELECT COUNT(*) FROM utilisateurs")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO utilisateurs (nom, age) VALUES ('Alice', 25), ('Bob', 30), ('Charlie', 28)")
    conn.commit()
    conn.close()

# Initialiser la base au démarrage
init_db()

# Initialisation de l'état de session
if 'connexion_etablie' not in st.session_state:
    st.session_state.connexion_etablie = False
if 'conn' not in st.session_state:
    st.session_state.conn = None

st.title("Connexion à une Base de Données SQLite")

# Inputs pour configuration
db_name = st.text_input("Nom de la base de données :", value="ma_bdd.db", disabled=True)

if st.button("Se Connecter"):
    try:
        conn = sqlite3.connect(db_name)
        st.session_state.conn = conn
        st.session_state.connexion_etablie = True
        st.success("Connexion établie avec succès !")
    except Exception as e:
        st.error(f"Erreur de connexion : {e}")

# Afficher les données si connecté
if st.session_state.connexion_etablie:
    st.subheader("Données de la table 'utilisateurs'")
    cursor = st.session_state.conn.cursor()
    cursor.execute("SELECT * FROM utilisateurs")
    rows = cursor.fetchall()
    for row in rows:
        st.write(row)
    
    # Ajouter un nouvel utilisateur
    st.subheader("Ajouter un utilisateur")
    new_nom = st.text_input("Nom du nouvel utilisateur :")
    new_age = st.number_input("Âge du nouvel utilisateur :", min_value=0, max_value=150, value=18)
    if st.button("Ajouter Utilisateur"):
        if new_nom:
            try:
                cursor.execute("INSERT INTO utilisateurs (nom, age) VALUES (?, ?)", (new_nom, new_age))
                st.session_state.conn.commit()
                st.success("Utilisateur ajouté !")
            except Exception as e:
                st.error(f"Erreur lors de l'ajout : {e}")
        else:
            st.error("Le nom ne peut pas être vide.")
    
    if st.button("Déconnecter"):
        st.session_state.conn.close()
        st.session_state.connexion_etablie = False
        st.info("Déconnecté.")
```

2. **Notes :**
   - La base de données `ma_bdd.db` est créée automatiquement avec des données par défaut (trois utilisateurs : Alice, Bob, Charlie).
   - Le champ `db_name` est désactivé (`disabled=True`) pour éviter des modifications inutiles, car la base est prédéfinie.
   - La validation du mot de passe est supprimée, car SQLite ne nécessite pas de paramètres complexes comme host/port/user/password.

3. **Tâches :**
   - Testez l’application et vérifiez que les données par défaut s’affichent.
   - Ajoutez une validation pour empêcher l’ajout d’un âge négatif ou supérieur à 150.
   - Modifiez l’affichage des données pour utiliser `st.dataframe` au lieu de `st.write` pour un rendu tabulaire.

4. **Défi facultatif :** Ajoutez un bouton pour supprimer un utilisateur par son ID.

**Résultat attendu :** Montrez votre application au groupe et expliquez vos modifications.

---

## Section 3 : Visualisation de Données CSV

**Objectif :** Créer une application pour uploader un fichier CSV et visualiser ses données sous forme de graphique.

**Préparation :** Créez un fichier CSV nommé `donnees.csv` avec ce contenu :

```
x,y
1,10
2,20
3,15
4,30
5,25
```

**Instructions :**

1. Créez un fichier `app_csv_courbe.py` avec le code suivant :

```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.title("Visualisation de Données CSV")

# Uploader le fichier
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        st.subheader("Aperçu des Données")
        st.dataframe(df.head())
        
        # Sélection des colonnes
        col_x = st.selectbox("Colonne X :", df.columns)
        col_y = st.selectbox("Colonne Y :", df.columns)
        
        # Filtrage des données
        min_x, max_x = float(df[col_x].min()), float(df[col_x].max())
        x_range = st.slider("Plage de X :", min_x, max_x, (min_x, max_x))
        df_filtered = df[(df[col_x] >= x_range[0]) & (df[col_x] <= x_range[1])]
        
        # Options de personnalisation
        titre = st.text_input("Titre du Graphique :", value="Ma Courbe")
        couleur = st.color_picker("Couleur de la Courbe :", "#FF0000")
        type_courbe = st.selectbox("Type de Courbe :", ["Line", "Scatter", "Bar"])
        
        if st.button("Afficher la Courbe"):
            fig, ax = plt.subplots()
            if type_courbe == "Line":
                ax.plot(df_filtered[col_x], df_filtered[col_y], color=couleur)
            elif type_courbe == "Scatter":
                ax.scatter(df_filtered[col_x], df_filtered[col_y], color=couleur)
            elif type_courbe == "Bar":
                ax.bar(df_filtered[col_x], df_filtered[col_y], color=couleur)
            
            ax.set_title(titre)
            ax.set_xlabel(col_x)
            ax.set_ylabel(col_y)
            st.pyplot(fig)
            
            # Télécharger le graphique
            buffer = io.BytesIO()
            fig.savefig(buffer, format="png")
            st.download_button(
                label="Télécharger le Graphique",
                data=buffer.getvalue(),
                file_name="graphique.png",
                mime="image/png"
            )
    except Exception as e:
        st.error(f"Erreur lors du chargement du CSV : {e}")
```

2. **Tâches :**
   - Testez avec `donnees.csv` et essayez le filtrage via le slider.
   - Ajoutez une option pour sélectionner plusieurs colonnes Y (via `st.multiselect`) et affichez plusieurs courbes superposées.
   - Validez que le CSV contient au moins deux colonnes numériques avant de générer le graphique.

3. **Défi facultatif :** Remplacez matplotlib par Altair (installez via `pip install altair`) pour un graphique interactif.

**Résultat attendu :** Présentez votre application et discutez des personnalisations ajoutées.

---

## Section 4 : Projet Final – Application Hybride

**Objectif :** Combiner les deux applications dans une application unique avec un menu de navigation, utilisant une base SQLite créée automatiquement.

**Instructions :**

1. Créez un fichier `app_hybride.py` avec le code suivant :

```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import io

# Fonction pour initialiser la base de données avec des données par défaut
def init_db():
    conn = sqlite3.connect('ma_bdd.db')
    c = conn.cursor()
    # Créer la table utilisateurs
    c.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (id INTEGER PRIMARY KEY, nom TEXT, age INTEGER)''')
    # Créer la table donnees_csv
    c.execute('''CREATE TABLE IF NOT EXISTS donnees_csv (x REAL, y REAL)''')
    # Insérer des données par défaut dans utilisateurs si vide
    c.execute("SELECT COUNT(*) FROM utilisateurs")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO utilisateurs (nom, age) VALUES ('Alice', 25), ('Bob', 30), ('Charlie', 28)")
    # Insérer des données par défaut dans donnees_csv si vide
    c.execute("SELECT COUNT(*) FROM donnees_csv")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO donnees_csv (x, y) VALUES (1, 10), (2, 20), (3, 15), (4, 30), (5, 25)")
    conn.commit()
    conn.close()

# Initialiser la base au démarrage
init_db()

# Initialisation de l'état de session
if 'connexion_etablie' not in st.session_state:
    st.session_state.connexion_etablie = False
if 'conn' not in st.session_state:
    st.session_state.conn = None

st.title("Application Hybride Streamlit")

# Menu de navigation
page = st.sidebar.selectbox("Choisissez une page :", ["Configuration BDD", "Visualisation CSV", "Requêtes SQL"])

if page == "Configuration BDD":
    st.subheader("Connexion à la Base de Données")
    db_name = st.text_input("Nom de la base de données :", value="ma_bdd.db", disabled=True)
    
    if st.button("Se Connecter"):
        try:
            conn = sqlite3.connect(db_name)
            st.session_state.conn = conn
            st.session_state.connexion_etablie = True
            st.success("Connexion établie !")
        except Exception as e:
            st.error(f"Erreur : {e}")
    
    if st.session_state.connexion_etablie:
        st.subheader("Données de la table 'utilisateurs'")
        cursor = st.session_state.conn.cursor()
        cursor.execute("SELECT * FROM utilisateurs")
        rows = cursor.fetchall()
        st.dataframe(rows, column_config={"0": "ID", "1": "Nom", "2": "Âge"})
        
        # Ajouter un utilisateur
        st.subheader("Ajouter un utilisateur")
        new_nom = st.text_input("Nom du nouvel utilisateur :")
        new_age = st.number_input("Âge du nouvel utilisateur :", min_value=0, max_value=150, value=18)
        if st.button("Ajouter Utilisateur"):
            if new_nom:
                try:
                    cursor.execute("INSERT INTO utilisateurs (nom, age) VALUES (?, ?)", (new_nom, new_age))
                    st.session_state.conn.commit()
                    st.success("Utilisateur ajouté !")
                except Exception as e:
                    st.error(f"Erreur lors de l'ajout : {e}")
            else:
                st.error("Le nom ne peut pas être vide.")

elif page == "Visualisation CSV":
    st.subheader("Visualisation de Données CSV")
    uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        
        col_x = st.selectbox("Colonne X :", df.columns)
        col_y = st.selectbox("Colonne Y :", df.columns)
        
        # Filtrage
        min_x, max_x = float(df[col_x].min()), float(df[col_x].max())
        x_range = st.slider("Plage de X :", min_x, max_x, (min_x, max_x))
        df_filtered = df[(df[col_x] >= x_range[0]) & (df[col_x] <= x_range[1])]
        
        if st.button("Afficher la Courbe"):
            fig, ax = plt.subplots()
            ax.plot(df_filtered[col_x], df_filtered[col_y])
            ax.set_title("Graphique CSV")
            ax.set_xlabel(col_x)
            ax.set_ylabel(col_y)
            st.pyplot(fig)
            
            # Télécharger le graphique
            buffer = io.BytesIO()
            fig.savefig(buffer, format="png")
            st.download_button(
                label="Télécharger le Graphique",
                data=buffer.getvalue(),
                file_name="graphique.png",
                mime="image/png"
            )
        
        if st.session_state.connexion_etablie and st.button("Insérer dans BDD"):
            try:
                cursor = st.session_state.conn.cursor()
                for index, row in df.iterrows():
                    cursor.execute("INSERT INTO donnees_csv (x, y) VALUES (?, ?)", (row[col_x], row[col_y]))
                st.session_state.conn.commit()
                st.success("Données insérées dans la BDD !")
            except Exception as e:
                st.error(f"Erreur lors de l'insertion : {e}")

elif page == "Requêtes SQL":
    st.subheader("Exécuter une Requête SQL")
    requete = st.text_area("Entrez votre requête SQL :", value="SELECT * FROM donnees_csv")
    if st.button("Exécuter"):
        if st.session_state.connexion_etablie:
            try:
                cursor = st.session_state.conn.cursor()
                cursor.execute(requete)
                rows = cursor.fetchall()
                st.write("Résultat de la requête :")
                st.dataframe(rows)
            except Exception as e:
                st.error(f"Erreur dans la requête : {e}")
        else:
            st.error("Veuillez vous connecter à la base de données d'abord.")
```

2. **Tâches :**
   - Testez avec `donnees.csv` et vérifiez que la base SQLite contient les données par défaut.
   - Ajoutez la possibilité de visualiser les données de la table `donnees_csv` (via une requête SQL automatique) dans la page "Visualisation CSV".
   - Implémentez les fonctionnalités des sections précédentes (ex. : superposition de courbes, validation des données).

3. **Défi facultatif :** Ajoutez une option dans "Requêtes SQL" pour sauvegarder les résultats d’une requête dans un fichier CSV téléchargeable.

**Résultat attendu :** Présentez votre application hybride au groupe et partagez vos améliorations.

---

## Résumé et Partage

- À la fin du workshop, soumettez un dossier ZIP contenant :
  - Les fichiers Python : `app_basique.py`, `app_config_bdd.py`, `app_csv_courbe.py`, `app_hybride.py`.
  - Le fichier CSV de test (`donnees.csv`).
  - Un court résumé (PDF ou Word) décrivant :
    - Ce que vous avez appris sur Streamlit.
    - Les fonctionnalités implémentées et les défis rencontrés.
    - Une explication de votre code pour l’application hybride.
- Présentez vos applications au groupe et discutez de vos choix techniques.

**Ressources utiles :**
- Documentation officielle Streamlit : https://docs.streamlit.io/
- Documentation pandas : https://pandas.pydata.org/docs/
- Documentation matplotlib : https://matplotlib.org/stable/contents.html
- Pour Altair (facultatif) : https://altair-viz.github.io/

Amusez-vous à coder vos applications web et partagez vos créations !
