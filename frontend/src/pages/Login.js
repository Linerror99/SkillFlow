import React, { useState } from "react";
import axios from "../services/api";
import { useNavigate } from "react-router-dom";
import "../styles/Login.css";

const Login = () => {
  const [formData, setFormData] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true); // 🔥 Activation du mode "chargement"

    console.log("🔍 Données envoyées :", JSON.stringify(formData)); // Vérification avant l'envoi

    try {
      const response = await axios.post("/token", formData);
      localStorage.setItem("token", response.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Nom d'utilisateur, email ou mot de passe incorrect");
    }

    setLoading(false); // 🔥 Désactivation du mode "chargement"
  };

  return (
    <div className="login-container">
      <h2>Se connecter</h2>
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
        <button type="submit" disabled={loading}>
          {loading ? "Connexion en cours..." : "Connexion"}
        </button>
      </form>

      {/* 🔥 Bouton d'inscription ajouté ici */}
      <p>Pas encore de compte ? <a href="/signup">Créer un compte</a></p>
    </div>
  );
};

export default Login;
