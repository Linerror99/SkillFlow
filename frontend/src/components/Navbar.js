import React from "react";
import { Link } from "react-router-dom";
import "../styles/Navbar.css";

const Navbar = () => {
  return (
    <nav className="navbar">
      <h1>SkillFlow</h1>
      <ul>
        <li><Link to="/">Accueil</Link></li>
        <li><Link to="/dashboard">Dashboard</Link></li>
        <li><Link to="/projects">Projets</Link></li>
        <li><Link to="/tasks">Tâches</Link></li>
        <li><Link to="/login">Connexion</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
