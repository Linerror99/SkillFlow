import React, { useState } from "react";
import axios from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";

const Signup = () => {
  const [formData, setFormData] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    console.log("🔍 Données envoyées :", JSON.stringify(formData)); // Vérification avant l'envoi
    
    try {
      await axios.post("/signup", formData);
      alert("Compte créé avec succès ! Connectez-vous maintenant.");
      navigate("/login");
    } catch (err) {
      setError(err.response?.data?.detail || "Erreur lors de l'inscription");
    }
  };

  return (
    <div className="login-container">
      <h2>Créer un compte</h2>
      {error && <p className="error">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Nom d'utilisateur"
          value={formData.username}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Mot de passe"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <button type="submit">S'inscrire</button>
      </form>
      <p>Déjà un compte ? <a href="/login">Se connecter</a></p>
    </div>
  );
};

export default Signup;
