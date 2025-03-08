import React from "react";
import { Link } from "react-router-dom";

function Header() {
  return (
    <header style={{ background: "#eee", padding: "10px" }}>
      <h1>SkillFlow</h1>
      <nav>
        <Link to="/">Accueil</Link> | 
        <Link to="/dashboard">Dashboard</Link> | 
        <Link to="/projects">Projets</Link>
      </nav>
    </header>
  );
}

export default Header;
