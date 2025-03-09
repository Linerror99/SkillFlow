import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar"; // Assure-toi que le chemin est correct
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";

const App = () => {
    const token = localStorage.getItem("token"); // 🔥 Vérifie si l'utilisateur est connecté

    return (
        <Router>
            <Navbar /> {/* 🔥 La navbar doit être affichée en permanence */}
            <Routes>
                <Route path="/" element={token ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} />
                <Route path="/login" element={<Login />} />
                <Route path="/signup" element={<Signup />} />
                <Route path="/dashboard" element={token ? <Dashboard /> : <Navigate to="/login" />} />
            </Routes>
        </Router>
    );
};

export default App;
