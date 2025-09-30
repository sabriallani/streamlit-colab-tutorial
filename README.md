# Tutoriel : trois applications Streamlit pour Colab

Ce tutoriel explique comment construire trois mini‑applications Streamlit
en Python :

1. **Formulaire d'achat de véhicule** – collecte des informations via un
   formulaire structuré et les enregistre dans la session.
2. **Chatbot simple** – illustre l'utilisation des éléments de chat pour
   créer une conversation interactive sans dépendance externe.
3. **Visualisation des achats** – regroupe et affiche les données
   collectées sous forme de tableau et de diagramme en barres.

Le tutoriel est rédigé en français et chaque étape est commentée pour
aider à la compréhension. Les fichiers sources se trouvent dans ce
dépôt :

* `app_vehicle_form.py` – application du formulaire.
* `app_chatbot.py` – application du chatbot.
* `app_data_visualization.py` – application de visualisation.

## 1. Préparation de l'environnement

Dans un nouveau notebook Colab :

1. Installer Streamlit et les dépendances nécessaires :

   ```python
   !pip install streamlit pandas pyngrok
   ```

   * `streamlit` : framework pour créer des apps web interactives.
   * `pandas` : manipulation de tables et de DataFrames.
   * `pyngrok` : publication d'un port local sur Internet (optionnel pour Colab).

2. Télécharger ou créer les fichiers Python dans votre environnement. Par
   exemple :

   ```python
   # enregistrez le code du formulaire dans un fichier
   %%writefile app_vehicle_form.py
   # (coller ici le contenu du fichier app_vehicle_form.py)
   ```

   Répétez l'opération pour `app_chatbot.py` et
   `app_data_visualization.py` ou utilisez les fichiers fournis.

3. Exécuter une application : la commande suivante lance un script
   Streamlit et renvoie l'adresse locale du serveur :

   ```python
   !streamlit run app_vehicle_form.py --server.port 8501 &> logs.txt &
   ```

   Sur Google Colab, les pages Web ne sont pas accessibles
   directement. Vous pouvez utiliser `pyngrok` ou [LocalTunnel](https://theboroer.github.io/localtunnel-www/) pour exposer le port 8501.
   Par exemple :

   ```python
   from pyngrok import ngrok
   public_url = ngrok.connect(8501)
   public_url
   ```

   Ouvrez l'URL retournée pour accéder à votre application.

## 2. Application 1 : Formulaire d'achat de véhicule

Ce module montre comment regrouper plusieurs champs dans un
`st.form` pour contrôler la soumission. L'utilisation d'un formulaire
permet d'envoyer toutes les données en une seule fois au clic sur
`Envoyer`. Les données sont ensuite stockées dans la variable
`st.session_state["vehicle_data"]` pour être réutilisées.

### Étapes principales

1. **Initialiser l'état** : vérifier si `vehicle_data` existe dans
   `st.session_state` ; sinon créer un DataFrame vide avec les colonnes
   nécessaires.
2. **Créer le formulaire** :
   * Définir le conteneur `with st.form(key="vehicle_form"):`.
   * Ajouter des widgets comme `st.text_input` pour le nom et le
     contact, `st.selectbox` pour le type de véhicule et le mode de
     paiement, `st.number_input` pour le prix et `st.date_input` pour
     la date d'achat. La fonction `st.date_input` affiche un
     sélecteur de date configurable【648397162177243†L249-L259】.
   * Terminer par un `st.form_submit_button("Envoyer")`. Chaque
     formulaire doit comporter au moins un bouton de soumission【472898386844030†L193-L204】.
3. **Traiter la soumission** : lorsque l'utilisateur clique sur le
   bouton, concaténer la nouvelle ligne au DataFrame stocké dans la
   session et afficher un message de réussite.
4. **Afficher l'historique** : en dehors du formulaire, utiliser
   `st.dataframe` pour présenter les données enregistrées.

## 3. Application 2 : Chatbot simple

Cette application utilise les nouveaux widgets de chat :

* `st.chat_message` insère un conteneur pour un message et applique
  automatiquement un style en fonction de l'auteur (utilisateur ou
  assistant). Il prend un paramètre `name` et peut afficher une icône【266638346480461†L188-L223】.
* `st.chat_input` crée un champ de saisie optimisé pour la
  conversation, avec un texte indicatif et un nombre maximal de
  caractères【911194705357470†L188-L223】.

### Logique de base

1. **Initialiser l'historique** : créer `st.session_state["messages"]` si
   nécessaire pour stocker des dicts `{role: ..., content: ...}`.
2. **Afficher l'historique** : parcourir la liste et appeler
   `st.chat_message(role)` pour chaque message.
3. **Saisir un nouveau message** : récupérer la chaîne saisie via
   `st.chat_input`. Si elle n'est pas vide, l'ajouter à l'historique
   avec le rôle `user` et l'afficher.
4. **Générer une réponse** : dans cet exemple, on vérifie quelques
   mots‑clés dans le message et on renvoie une réponse fixe. Dans un
   projet réel, cette partie pourrait appeler un modèle de langage ou
   un service externe.
5. **Afficher la réponse** : utiliser `st.chat_message("assistant")` pour
   montrer la réponse et l'ajouter à l'historique.

## 4. Application 3 : Visualisation des achats

La troisième application exploite les données enregistrées par le
formulaire pour fournir un tableau filtrable et un graphique. On
utilise `st.multiselect` pour choisir les types de véhicules à
afficher, puis on agrège les données et on utilise `st.bar_chart` pour
dessiner un diagramme :

1. **Accéder aux données** : récupérer `st.session_state["vehicle_data"]`.
   Si la table est vide, afficher un message informatif.
2. **Filtrer** : les valeurs uniques de la colonne « Type » sont
   proposées dans un `st.multiselect` afin que l'utilisateur puisse
   sélectionner un ou plusieurs types.
3. **Afficher le tableau filtré** : `st.dataframe` permet de voir les
   enregistrements correspondant à la sélection.
4. **Créer le graphique** : grouper par type et compter le nombre
   d'achats. `st.bar_chart` prend en entrée un DataFrame indexé par
   « Type » et dessine automatiquement un diagramme en barres en
   utilisant les colonnes pour définir l'axe des ordonnées【54672515633451†L209-L214】. La
   fonction est un raccourci vers `st.altair_chart` et déduit la
   spécification Altair à partir des données【54672515633451†L218-L239】.

## 5. Conseils de déploiement

* **Ordre d'exécution** : si vous souhaitez utiliser la visualisation
  après avoir saisi des données, lancez d'abord `app_vehicle_form.py`
  pour créer quelques enregistrements. Ensuite, ouvrez
  `app_data_visualization.py` ; l'historique des achats sera déjà
  présent en mémoire tant que vous exécutez les applications dans la
  même session Python.
* **Édition** : n'hésitez pas à adapter les listes (types de véhicules,
  modes de paiement) à vos besoins. Vous pouvez également enrichir le
  chatbot en ajoutant une logique plus sophistiquée ou en le connectant
  à un modèle externe.
* **Licence** : ce code est fourni à titre éducatif et peut être
  utilisé et modifié librement.
