import streamlit as st
import os
import requests

# Définir la configuration de la page
st.set_page_config(
    page_title="Gestion des Scripts NSE - TRHACKNON",  # Titre du navigateur
    page_icon="https://miro.medium.com/v2/resize:fit:828/format:webp/1*areV8qZKYjT0dzxuL8Nifg.png",  # Icône personnalisée
    layout="centered",  # Centrer le contenu
    initial_sidebar_state="expanded"  # Développer la barre latérale par défaut
)

st.markdown("""
    <head>
        <meta property="og:title" content="Gestion des Scripts NSE - by TRHACKNON" />
        <meta property="og:description" content="Une application pour gérer les scripts NSE pour Nmap, conçu par TRHACKNON." />
        <meta property="og:image" content="https://miro.medium.com/v2/resize:fit:828/format:webp/1*areV8qZKYjT0dzxuL8Nifg.png" />
        <meta property="og:url" content="https://trkn-nse.streamlit.app/" />
        <meta name="twitter:card" content="summary_large_image">
    </head>
""", unsafe_allow_html=True)

# Définir les styles personnalisés (fond sombre, texte fluo, éléments interactifs)
st.markdown("""
    <style>
        body {
            background-color: #1e1e1e;
            color: #00ff00;
            font-family: "Courier New", monospace;
            margin: 0;
        }
        .stButton button {
            background-color: #00ff00;
            color: #1e1e1e;
            border: 2px solid #00ff00;
            padding: 12px 25px;
            font-size: 18px;
            font-family: "Courier New", monospace;
            border-radius: 8px;
            box-shadow: 0px 0px 10px #00ff00;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            background-color: #00cc00;
            transform: translateY(-2px);
            box-shadow: 0px 4px 20px #00ff00;
        }
        .stTextArea textarea {
            background-color: #1e1e1e;
            color: #00ff00;
            border: 2px solid #00ff00;
            font-family: "Courier New", monospace;
            border-radius: 8px;
            box-shadow: 0px 0px 10px #00ff00;
            padding: 15px;
        }
        .stSelectbox select {
            background-color: #1e1e1e;
            color: #00ff00;
            border: 2px solid #00ff00;
            font-family: "Courier New", monospace;
            border-radius: 8px;
            padding: 10px;
        }
        h1, h2, h3 {
            color: #00ff00;
            text-shadow: 0px 0px 15px rgba(0,255,0,0.7);
        }
        .stText {
            color: #00ff00;
        }
        .stMarkdown {
            margin-top: 10px;
        }
        .stTitle {
            font-size: 3em;
            font-weight: bold;
            letter-spacing: 2px;
            text-align: center;
            text-shadow: 0px 0px 20px rgba(0,255,0,0.8);
            margin-bottom: 20px;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }
        .logo-container img {
            width: 150px;
            height: auto;
            transition: transform 0.3s ease;
        }
        .logo-container img:hover {
            transform: scale(1.1);
        }
        .stSidebar .stMarkdown {
            color: #00ff00;
            font-family: "Courier New", monospace;
        }
    </style>
""", unsafe_allow_html=True)

# Fonction About personnalisée dans le menu Streamlit
def about_section():
    st.markdown("<h2>À propos</h2>", unsafe_allow_html=True)
    st.markdown("""
        <p>
            Bienvenue dans la gestion des scripts NSE! Cette application vous permet de télécharger et de gérer des scripts NSE pour Nmap, créés pour améliorer vos tests de sécurité.
        </p>
        <p>
            Conçu par <strong>TRHACKNON</strong>, un passionné de cybersécurité, cet outil facilite l'intégration de scripts pour tester vos systèmes et applications. 
        </p>
        <p>
            Vous pouvez explorer les scripts, les mettre à jour, et voir leur contenu directement ici. Un outil simple et efficace pour les professionnels de la sécurité.
        </p>
        <p>
            <a href="https://www.facebook.com/share/18SFLvkBT2/" style="color: #00ff00;">Rejoignez-moi sur Facebook!</a>
        </p>
    """, unsafe_allow_html=True)

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
st.markdown("<h1 class='stTitle'>Gestion des Scripts NSE - by TRHACKNON</h1>", unsafe_allow_html=True)

# Option de mise à jour des scripts
col1, col2 = st.columns([2, 1])
with col1:
    if st.button("Mettre à jour les scripts", use_container_width=True):
        download_scripts()
        st.success("Scripts mis à jour avec succès!")
with col2:
    st.markdown('<div class="logo-container"><img src="https://miro.medium.com/v2/resize:fit:828/format:webp/1*areV8qZKYjT0dzxuL8Nifg.png" alt="Logo" /></div>', unsafe_allow_html=True)

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

# Ajouter la section About dans le menu sidebar
with st.sidebar:
    about_section()
