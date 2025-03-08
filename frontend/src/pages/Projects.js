import React, { useEffect, useState } from "react";
import axios from "../services/api";
import "../styles/Projects.css";

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [newProject, setNewProject] = useState({ name: "", description: "" });

  useEffect(() => {
    fetchProjects();
  }, []);

  const fetchProjects = async () => {
    try {
      const response = await axios.get("/projects/");
      setProjects(response.data);
    } catch (error) {
      console.error("❌ Erreur lors du chargement des projets :", error);
    }
  };

  const handleAddProject = async () => {
    if (!newProject.name.trim()) {
      alert("Le nom du projet est obligatoire !");
      return;
    }
    try {
      const response = await axios.post("/projects/", newProject);
      setProjects([...projects, response.data]);
      setNewProject({ name: "", description: "" });
    } catch (error) {
      console.error("❌ Erreur lors de l'ajout du projet :", error);
    }
  };

  const handleDeleteProject = async (id) => {
    try {
      await axios.delete(`/projects/${id}`);
      setProjects(projects.filter(project => project.id !== id));
    } catch (error) {
      console.error("❌ Erreur lors de la suppression du projet", error);
    }
  };

  return (
    <div className="projects-container">
      <h2>📁 Gestion des Projets</h2>

      <div className="project-form">
        <input
          type="text"
          placeholder="Nom du projet"
          value={newProject.name}
          onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
        />
        <input
          type="text"
          placeholder="Description"
          value={newProject.description}
          onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
        />
        <button className="add-btn" onClick={handleAddProject}>➕ Ajouter</button>
      </div>

      <ul className="projects-list">
        {projects.map((project) => (
          <li key={project.id} className="project-item">
            <strong>{project.name}</strong> - {project.description}
            <button onClick={() => handleDeleteProject(project.id)}>🗑️ Supprimer</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Projects;
