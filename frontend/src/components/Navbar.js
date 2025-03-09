import React from "react";
import { Link, useNavigate } from "react-router-dom"; // ✅ Ajout de `useNavigate`
import "../styles/Navbar.css";

const Navbar = () => {
  const navigate = useNavigate();
  const token = localStorage.getItem("token"); // ✅ Vérifie si l'utilisateur est connecté

  console.log("🔍 Navbar chargée - Token :", token); // 🔥 Vérifie si la Navbar se charge

  const handleLogout = () => {
    localStorage.removeItem("token"); // Supprime le token JWT
    navigate("/login"); // Redirige vers la page de connexion
  };

  return (
    <nav className="navbar">
      <ul>
        {token ? ( // 🔥 Si l'utilisateur est connecté
          <>
            <li><Link to="/dashboard">Dashboard</Link></li>
            <li><Link to="/projects">Projets</Link></li>
            <li><Link to="/tasks">Tâches</Link></li>
            <li><Link to="/calendar">📅 Calendrier</Link></li> {/* 📌 Ajout du lien */}
            <li className="logout-btn" onClick={handleLogout}>🚪 Déconnexion</li>
          </>
        ) : ( // 🔥 Si l'utilisateur n'est PAS connecté
          <>
            <li><Link to="/login">Connexion</Link></li>
            <li><Link to="/signup">Inscription</Link></li>
          </>
        )}
      </ul>
    </nav>
  );
};

export default Navbar;
