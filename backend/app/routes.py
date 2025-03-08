from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Project, Task
from app.schemas import ProjectCreate, ProjectResponse, TaskCreate, TaskResponse
from typing import List

router = APIRouter()

# Dépendance pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### 📌 Routes pour les projets ###
@router.post("/projects/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/projects/", response_model=List[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")

    db.delete(project)
    db.commit()
    return {"message": "Projet supprimé"}

### 📌 Routes pour les tâches ###
@router.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    if not db.query(Project).filter(Project.id == task.project_id).first():
        raise HTTPException(status_code=404, detail="Projet non trouvé")

    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskCreate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    db_task.title = task_update.title
    db_task.description = task_update.description
    db_task.due_date = task_update.due_date
    db_task.status = task_update.status
    db_task.project_id = task_update.project_id

    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    db.delete(db_task)
    db.commit()
    return {"message": "Tâche supprimée"}

### 📌 Route pour le tableau de bord ###
@router.get("/dashboard/")
def get_dashboard(db: Session = Depends(get_db)):
    total_projects = db.query(Project).count()
    total_tasks = db.query(Task).count()
    
    tasks_todo = db.query(Task).filter(Task.status == "À faire").count()
    tasks_in_progress = db.query(Task).filter(Task.status == "En cours").count()
    tasks_done = db.query(Task).filter(Task.status == "Terminé").count()

    return {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "tasks_status": {
            "todo": tasks_todo,
            "in_progress": tasks_in_progress,
            "done": tasks_done
        }
    }
