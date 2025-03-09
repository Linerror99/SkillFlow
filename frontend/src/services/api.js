import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL?.trim() || "http://localhost:8000";

console.log("📌 API Base URL :", API_BASE_URL); // Vérifier dans la console si l'URL est correcte

const api = axios.create({
  baseURL: API_BASE_URL, 
});

// Ajouter le token à toutes les requêtes
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");  // 🔥 Vérifie bien le nom de la clé
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;