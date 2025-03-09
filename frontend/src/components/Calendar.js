import React, { useState, useEffect } from "react";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import axios from "../services/api";

const Calendar = () => {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const response = await axios.get("/tasks/");
      const formattedTasks = response.data.map((task) => ({
        id: task.id,
        title: task.title,
        start: task.due_date, // 📌 Date d'échéance de la tâche
        backgroundColor: getStatusColor(task.status), // 📌 Couleur selon le statut
      }));
      setEvents(formattedTasks);
    } catch (error) {
      console.error("Erreur lors du chargement des tâches", error);
    }
  };

  // 📌 Fonction pour attribuer une couleur selon le statut de la tâche
  const getStatusColor = (status) => {
    switch (status) {
      case "À faire":
        return "red";
      case "En cours":
        return "orange";
      case "Terminé":
        return "green";
      default:
        return "blue";
    }
  };

  return (
    <div>
      <h2>📅 Calendrier des Tâches</h2>
      <FullCalendar
        plugins={[dayGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        events={events}
        eventClick={(info) => alert(`Tâche: ${info.event.title}`)} // 📌 Afficher le titre lors du clic
      />
    </div>
  );
};

export default Calendar;
