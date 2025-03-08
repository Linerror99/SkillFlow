from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, Enum
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

# Modèle de tâche
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", back_populates="tasks")

# Relation entre projets et tâches
Project.tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
