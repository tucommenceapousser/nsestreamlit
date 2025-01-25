import streamlit as st
import os
import requests

# Définition du répertoire pour stocker les scripts
SCRIPTS_DIR = "scripts/nse"
GITHUB_URL = "https://raw.githubusercontent.com/tucommenceapousser/nmap-nse-scripts/master/scripts/"

def download_scripts():
    """Télécharge les scripts NSE depuis GitHub."""
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    scripts_url = "https://api.github.com/repos/tucommenceapousser/nmap-nse-scripts/contents/scripts"
    response = requests.get(scripts_url)
    if response.status_code == 200:
        scripts = response.json()
        for script in scripts:
            if script["name"].endswith(".nse"):
                script_path = os.path.join(SCRIPTS_DIR, script["name"])
                if not os.path.exists(script_path):
                    content = requests.get(script["download_url"]).text
                    with open(script_path, "w") as file:
                        file.write(content)

def get_scripts():
    """Récupère la liste des scripts NSE disponibles localement."""
    if not os.path.exists(SCRIPTS_DIR):
        download_scripts()
    return [{"name": script, "path": f"{SCRIPTS_DIR}/{script}"} for script in os.listdir(SCRIPTS_DIR) if script.endswith(".nse")]

# Streamlit UI
st.title("Gestion des Scripts NSE")

# Option de mise à jour des scripts
if st.button("Mettre à jour les scripts"):
    download_scripts()
    st.success("Scripts mis à jour avec succès!")

# Récupérer et afficher la liste des scripts
scripts = get_scripts()
script_names = [script["name"] for script in scripts]

# Sélectionner un script
selected_script = st.selectbox("Sélectionnez un script", script_names)

# Affichage des détails du script sélectionné
if selected_script:
    script_path = next(script["path"] for script in scripts if script["name"] == selected_script)
    if os.path.exists(script_path):
        with open(script_path, "r") as file:
            content = file.read()
        
        st.subheader(f"Détails du script: {selected_script}")
        st.text_area("Contenu du script", content, height=400)
