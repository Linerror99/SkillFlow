import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
import plotly.express as px
import requests
import pandas as pd
import os

# 📌 URL de l'API FastAPI (Docker-friendly)
API_URL = os.getenv("API_URL", "http://backend:8000/stats/")

# 🔄 Fonction pour récupérer les données depuis l'API
def fetch_data():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur API : {e}")
        return None

# Initialisation de l'application Dash avec Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# 📊 Mise en page initiale (sans données)
app.layout = dbc.Container([
    html.H1("📊 SkillFlow Dashboard", className="text-center my-4"),
    
    # 📌 Statistiques globales
    dbc.Row([
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Total Projets"), html.H2(id="total-projects")])]), width=4),
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Total Tâches"), html.H2(id="total-tasks")])]), width=4),
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Tâches en retard"), html.H2(id="overdue-tasks")])]), width=4),
    ], className="mb-4"),

    # 📈 Graphiques
    dbc.Row([
        dbc.Col(dcc.Graph(id="tasks-status-chart"), width=6),
        dbc.Col(dcc.Graph(id="tasks-evolution-chart"), width=6),
    ]),

    # 🔄 Rafraîchir les données toutes les 30 secondes
    dcc.Interval(id="interval-update", interval=30000, n_intervals=0),
], fluid=True)

# 🔄 Callback pour mettre à jour les données dynamiquement
@app.callback(
    [Output("total-projects", "children"),
     Output("total-tasks", "children"),
     Output("overdue-tasks", "children"),
     Output("tasks-status-chart", "figure"),
     Output("tasks-evolution-chart", "figure")],
    Input("interval-update", "n_intervals")
)
def update_dashboard(n_intervals):
    data = fetch_data()
    if not data:
        return "Erreur", "Erreur", "Erreur", px.pie(title="Erreur API"), px.line(title="Erreur API")

    # 📌 Mettre à jour les valeurs globales
    total_projects = data["total_projects"]
    total_tasks = data["total_tasks"]
    overdue_tasks = data["overdue_tasks"]

    # 📊 Répartition des tâches par statut (Pie Chart)
    tasks_status = pd.DataFrame([
        {"Statut": "À faire", "Nombre": data["tasks_status"]["todo"]},
        {"Statut": "En cours", "Nombre": data["tasks_status"]["in_progress"]},
        {"Statut": "Terminé", "Nombre": data["tasks_status"]["done"]}
    ])
    fig_status = px.pie(
        tasks_status, names="Statut", values="Nombre", title="Répartition des tâches",
        color_discrete_sequence=["#FF5733", "#F1C40F", "#28B463"]
    )

    # 📈 Evolution des tâches créées et terminées (Line Chart)
    task_progress = pd.DataFrame([
        {"Date": key, "Créées": data["tasks_created_per_day"].get(key, 0), "Terminées": data["tasks_completed_per_day"].get(key, 0)}
        for key in data["tasks_created_per_day"].keys()
    ])
    fig_progress = px.line(
        task_progress, x="Date", y=["Créées", "Terminées"], title="Évolution des tâches",
        markers=True, labels={"value": "Nombre de tâches", "variable": "Statut"}
    )

    return total_projects, total_tasks, overdue_tasks, fig_status, fig_progress

# Lancer l'application Dash
if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
