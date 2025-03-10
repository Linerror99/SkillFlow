from pydantic import BaseModel
from datetime import date
from typing import List, Optional
import enum

# Enum pour le statut des tâches
class TaskStatus(str, enum.Enum):
    TODO = "À faire"
    IN_PROGRESS = "En cours"
    DONE = "Terminé"

# Schéma pour créer une tâche
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    status: TaskStatus
    project_id: int

# Schéma pour renvoyer une tâche
class TaskResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True

# Schéma pour créer un projet
class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

# Schéma pour renvoyer un projet
class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        orm_mode = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    status: Optional[str] = None  # Permet de ne mettre à jour que le statut
    project_id: Optional[int] = None