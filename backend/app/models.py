from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Enum, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base  # Import relatif pour éviter les erreurs
import enum

# Définition du statut des tâches
class TaskStatus(str, enum.Enum):
    TODO = "À faire"
    IN_PROGRESS = "En cours"
    DONE = "Terminé"

# Modèle de projet
class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)

    # Relation avec les tâches
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")

# Modèle de tâche
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    
    created_at = Column(DateTime, server_default=func.now())  # 📌 Ajout de la date de création
    updated_at = Column(DateTime, onupdate=func.now())  # Ajout du suivi de la mise à jour

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="tasks")
