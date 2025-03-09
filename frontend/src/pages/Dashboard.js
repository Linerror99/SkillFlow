import React, { useEffect, useState } from "react";
import axios from "../services/api";
import { useNavigate } from "react-router-dom";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ResponsiveContainer
} from "recharts";
import "../styles/Dashboard.css";

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token"); // Récupérer le token JWT

    if (!token) {
      navigate("/login"); // Rediriger si l'utilisateur n'est pas connecté
      return;
    }

    axios
      .get("/stats/", {
        headers: { Authorization: `Bearer ${token}` }, // Ajouter le token dans la requête API
      })
      .then((response) => {
        setStats(response.data);
      })
      .catch((error) => {
        console.error("❌ Erreur lors de la récupération des stats :", error);
        if (error.response && error.response.status === 401) {
          navigate("/login"); // Rediriger si l'authentification échoue
        }
      });
  }, [navigate]);

  if (!stats) return <p>Chargement des statistiques...</p>;

  // 📌 Données pour le PieChart - Répartition des statuts des tâches
  const taskStatusData = [
    { name: "À faire", value: stats.tasks_status.todo, fill: "#FF6384" },
    { name: "En cours", value: stats.tasks_status.in_progress, fill: "#36A2EB" },
    { name: "Terminé", value: stats.tasks_status.done, fill: "#4CAF50" },
  ];

  // 📌 Données pour le BarChart - Activité des projets
  const projectActivityData = Object.keys(stats.projects_activity).map((key) => ({
    name: key,
    tasks: stats.projects_activity[key],
  }));

  // 📌 Données pour le LineChart - Nombre de tâches créées par jour
  const taskProgressData = Object.keys(stats.tasks_created_per_day).map((key) => ({
    date: key,
    created: stats.tasks_created_per_day[key] || 0,
    completed: stats.tasks_completed_per_day[key] || 0,
  }));

  return (
    <div className="dashboard-container">
      <h2>📊 Tableau de Bord</h2>
      <p>Bienvenue, {stats.user} 👋</p>

      <div className="stats-container">
        <div className="stat-box">
          <h3>Total Projets</h3>
          <p>{stats.total_projects}</p>
        </div>
        <div className="stat-box">
          <h3>Total Tâches</h3>
          <p>{stats.total_tasks}</p>
        </div>
        <div className="stat-box overdue">
          <h3>Tâches en retard</h3>
          <p>{stats.overdue_tasks}</p>
        </div>
      </div>

      <div className="charts-container">
        {/* PieChart - Répartition des tâches */}
        <div className="chart">
          <h3>Répartition des tâches</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={taskStatusData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label />
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* BarChart - Activité des projets */}
        <div className="chart">
          <h3>Activité des projets</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={projectActivityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="tasks" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* LineChart - Progression des tâches */}
        <div className="chart">
          <h3>Évolution des tâches</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={taskProgressData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="created" stroke="#FF6384" name="Créées" />
              <Line type="monotone" dataKey="completed" stroke="#36A2EB" name="Terminées" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
