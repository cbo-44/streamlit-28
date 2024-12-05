import streamlit as st
from streamlit_authenticator import Authenticate
from streamlit_option_menu import option_menu
import pandas as pd 

# Nos données utilisateurs doivent respecter ce format

#Fonction pour charger les données des comptes depuis un fichier CSV

def charger_comptes(csv_path):
    try:
        # Lecture du fichier CSV
        data = pd.read_csv(csv_path)
        # Transformation des données en un dictionnaire au format attendu
        comptes = {
            "usernames": {
                row["name"]: {
                    "name": row["name"],
                    "password": row["password"],
                    "email": row["email"],
                    "failed_login_attemps": int(row["failed_login_attempts"]),
                    "logged_in": bool(row["logged_in"]),
                    "role": row["role"]
                } for _, row in data.iterrows()
            }
        }
        return comptes
    except Exception as e:
        st.error(f"Erreur lors du chargement des comptes depuis le fichier CSV : {e}")
        return None
# Chemin vers le fichier CSV contenant les comptes
csv_path = "comptes_utilisateurs.csv"
# Charger les comptes
lesDonneesDesComptes = charger_comptes(csv_path)
if not lesDonneesDesComptes:
    st.stop()  # Arrêter l'exécution si les données ne peuvent pas être chargées

authenticator = Authenticate(
    lesDonneesDesComptes, # Les données des comptes
    "cookie name", # Le nom du cookie, un str quelconque
    "cookie key", # La clé du cookie, un str quelconque
    30, # Le nombre de jours avant que le cookie expire 
)

authenticator.login()

def accueil():
    st.title("Bienvenu sur le contenu réservé aux utilisateurs connectés")
    
    add_selectbox = st.sidebar.selectbox(
            "Bienvenue",
            ("Acceuil", "Photos")       
        )
        # On indique au programme quoi faire en fonction du choix
    if add_selectbox == "Acceuil":
            st.write("Bienvenue sur la page d'accueil !")
            st.image("https://t4.ftcdn.net/jpg/01/36/05/99/360_F_136059986_AxO3eLvDIZeDjc2UK77ci7WsZ22sap6b.jpg")

    elif add_selectbox == "Photos":
            st.write("Bienvenue sur mon album photo")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.header("A cat")
                st.image("https://static.streamlit.io/examples/cat.jpg")

            with col2:
                st.header("A dog")
                st.image("https://static.streamlit.io/examples/dog.jpg")

            with col3:
                st.header("An owl")
                st.image("https://static.streamlit.io/examples/owl.jpg")

if st.session_state["authentication_status"]:
  accueil()
  # Le bouton de déconnexion
  authenticator.logout("Déconnexion")

elif st.session_state["authentication_status"] is False:
    st.error("L'username ou le password est/sont incorrect")
elif st.session_state["authentication_status"] is None:
    st.warning('Les champs username et mot de passe doivent être remplie')

