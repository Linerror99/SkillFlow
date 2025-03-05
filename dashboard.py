import dash
from dash import dcc, html
import plotly.express as px
import requests
import pandas as pd

# Récupérer les statistiques depuis l'API SkillFlow
API_URL = "http://127.0.0.1:8000/dashboard/"


def fetch_data():
    try:
        print(f"📌 Récupération des données depuis : {API_URL}")  # 🔍 Ajout debug
        response = requests.get(API_URL)
        print(f"📌 Code de réponse : {response.status_code}")  # 🔍 Vérifier la réponse HTTP
        print(f"📌 Contenu brut : {response.text}")  # 🔍 Voir la réponse complète
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération des données : {e}")
        return None


# Lancer la récupération des stats
data = fetch_data()
print("📌 Données récupérées depuis l'API :", data)

if data:
    # Création des datasets
    tasks_status = pd.DataFrame([
        {"Statut": "À faire", "Nombre": data["tasks_status"]["todo"]},
        {"Statut": "En cours", "Nombre": data["tasks_status"]["in_progress"]},
        {"Statut": "Terminé", "Nombre": data["tasks_status"]["done"]}
    ])

    projects_progress = pd.DataFrame(data["projects_progress"])

    # Création des graphiques interactifs
    fig_status = px.pie(tasks_status, names="Statut", values="Nombre", title="Répartition des tâches")
    fig_progress = px.bar(projects_progress, x="name", y="progress", text="progress",
                          labels={"name": "Projet", "progress": "Progression (%)"},
                          title="Progression des projets")

    # Initialiser Dash
    app = dash.Dash(__name__)

    # Layout du Dashboard
    app.layout = html.Div(children=[
        html.H1("Tableau de Bord SkillFlow", style={"textAlign": "center"}),

        html.Div(children=[
            html.Div(children=[
                html.H3(f"Total Projets : {data['total_projects']}"),
                html.H3(f"Total Tâches : {data['total_tasks']}"),
                html.H3(f"Tâches en retard : {data['overdue_tasks']}"),
            ], style={"textAlign": "center", "marginBottom": "20px"})
        ]),

        html.Div(children=[
            dcc.Graph(figure=fig_status),
            dcc.Graph(figure=fig_progress),
        ])
    ])

    # Lancer l'application Dash
    if __name__ == "__main__":
        app.run_server(debug=True, host="0.0.0.0", port=8050)
