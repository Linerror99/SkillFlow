import axios from "axios";

const API_BASE_URL = process.env.REACT_APP_API_URL?.trim() || "http://backend:8000";

console.log("📌 API Base URL :", API_BASE_URL); // Vérifier dans la console si l'URL est correcte

const api = axios.create({
  baseURL: API_BASE_URL, 
});

export default api;
