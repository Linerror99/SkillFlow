import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Projects from "./pages/Projects";
import Tasks from "./pages/Tasks";
import Calendar from "./components/Calendar";
import "./styles/App.css";

const App = () => {
    const token = localStorage.getItem("token"); // 🔥 Vérifie si l'utilisateur est connecté

    return (
        <Router>
            {token && <Navbar />} {/* 🔥 Afficher la Navbar uniquement si connecté */}
            <Routes>
                <Route path="/" element={token ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/dashboard" element={token ? <Dashboard /> : <Navigate to="/login" />} />
                <Route path="/projects" element={token ? <Projects /> : <Navigate to="/login" />} />
                <Route path="/tasks" element={token ? <Tasks /> : <Navigate to="/login" />} />
                <Route path="/calendar" element={token ? <Calendar /> : <Navigate to="/login" />} /> {/* 📌 Route pour le calendrier */}
            </Routes>
        </Router>
    );
};

export default App;
