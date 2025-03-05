from pydantic import BaseModel
from datetime import date
from typing import List, Optional
import enum

class TaskStatus(str, enum.Enum):
    TODO = "À faire"
    IN_PROGRESS = "En cours"
    DONE = "Terminé"

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    status: TaskStatus
    project_id: int

class TaskResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectResponse(ProjectCreate):
    id: int

    class Config:
        orm_mode = True
