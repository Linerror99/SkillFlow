import dash
from dash import dcc, html
import plotly.express as px
import requests
import pandas as pd

# 📌 URL de l'API FastAPI
API_URL = "http://localhost:8000/dashboard/"

# 🔄 Récupérer les statistiques depuis l'API
def fetch_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur API : {e}")
        return None

# Initialisation de l'application Dash
app = dash.Dash(__name__)

# Récupération des données API
data = fetch_data()

if data:
    # 📊 Création des datasets pour les graphiques
    tasks_status = pd.DataFrame([
        {"Statut": "À faire", "Nombre": data["tasks_status"]["todo"]},
        {"Statut": "En cours", "Nombre": data["tasks_status"]["in_progress"]},
        {"Statut": "Terminé", "Nombre": data["tasks_status"]["done"]}
    ])

    # 📈 Graphique des tâches par statut
    fig_status = px.pie(
        tasks_status, names="Statut", values="Nombre", title="Répartition des tâches",
        color_discrete_sequence=["#FF5733", "#F1C40F", "#28B463"]
    )

    # 🔹 Interface du dashboard
    app.layout = html.Div([
        html.H1("📊 SkillFlow Dashboard", style={"textAlign": "center"}),
        dcc.Graph(figure=fig_status)
    ])

if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
