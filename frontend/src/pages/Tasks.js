import React, { useEffect, useState } from "react";
import axios from "../services/api";
import "../styles/Tasks.css";

const Tasks = () => {
  const [tasks, setTasks] = useState([]);
  const [projects, setProjects] = useState([]);
  const [newTask, setNewTask] = useState({
    title: "",
    description: "",
    due_date: "",
    status: "À faire",
    project_id: "",
  });

  useEffect(() => {
    fetchTasks();
    fetchProjects();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await axios.get("/tasks/");
      setTasks(response.data);
    } catch (error) {
      console.error("❌ Erreur lors de la récupération des tâches :", error);
    }
  };

  const fetchProjects = async () => {
    try {
      const response = await axios.get("/projects/");
      setProjects(response.data);
    } catch (error) {
      console.error("❌ Erreur lors de la récupération des projets :", error);
    }
  };

  const handleAddTask = async () => {
    if (!newTask.title || !newTask.project_id) {
      alert("⚠️ Le titre et le projet sont obligatoires !");
      return;
    }
    try {
      const response = await axios.post("/tasks/", newTask);
      setTasks([...tasks, response.data]);
      setNewTask({ title: "", description: "", due_date: "", status: "À faire", project_id: "" });
    } catch (error) {
      console.error("❌ Erreur lors de l'ajout de la tâche :", error);
    }
  };

  const handleDeleteTask = async (id) => {
    try {
      await axios.delete(`/tasks/${id}`);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (error) {
      console.error("❌ Erreur lors de la suppression de la tâche", error);
    }
  };

  const handleStatusUpdate = async (task) => {
    try {
        await axios.put(`${process.env.REACT_APP_API_URL}/tasks/${task.id}`, { status: task.status });
        fetchTasks();  // Rafraîchir la liste après modification
    } catch (error) {
        console.error("Erreur lors de la mise à jour du statut de la tâche", error);
    }
};


  return (
    <div className="tasks-container">
      <h2>✅ Gestion des Tâches</h2>

      <div className="task-form">
        <label>Titre de la tâche :</label>
        <input
          type="text"
          placeholder="Titre de la tâche"
          value={newTask.title}
          onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
        />

        <label>Description :</label>
        <input
          type="text"
          placeholder="Description"
          value={newTask.description}
          onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
        />

        <label>Date d'échéance :</label>
        <input
          type="date"
          value={newTask.due_date}
          onChange={(e) => setNewTask({ ...newTask, due_date: e.target.value })}
        />

        <label>Projet :</label>
        <select
          value={newTask.project_id}
          onChange={(e) => setNewTask({ ...newTask, project_id: e.target.value })}
        >
          <option value="">Sélectionner un projet</option>
          {projects.map((project) => (
            <option key={project.id} value={project.id}>
              {project.name}
            </option>
          ))}
        </select>

        <button className="add-btn" onClick={handleAddTask}>➕ Ajouter</button>
      </div>

      <ul className="tasks-list">
        {tasks.map((task) => (
          <li key={task.id} className="task-item">
            <div>
              <strong>{task.title}</strong> - {task.description} (📅 {task.due_date})
              <select value={task.status} onChange={(e) => setTasks(tasks.map(t => t.id === task.id ? { ...t, status: e.target.value } : t))}>
                <option value="À faire">À faire</option>
                <option value="En cours">En cours</option>
                <option value="Terminé">Terminé</option>
              </select>
              <button onClick={() => handleStatusUpdate(task)}>✔ Mettre à jour</button>
              <button onClick={() => handleDeleteTask(task.id)}>🗑️ Supprimer</button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Tasks;
