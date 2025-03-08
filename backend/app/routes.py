from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Project, Task
from app.schemas import ProjectCreate, ProjectResponse, TaskCreate, TaskResponse,TaskUpdate
from typing import List
from datetime import datetime, timedelta
from collections import defaultdict

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

@router.get("/stats/")
def get_statistics(db: Session = Depends(get_db)):
    total_projects = db.query(Project).count()
    total_tasks = db.query(Task).count()

    # Répartition des statuts des tâches
    tasks_status = {
        "todo": db.query(Task).filter(Task.status == "À faire").count(),
        "in_progress": db.query(Task).filter(Task.status == "En cours").count(),
        "done": db.query(Task).filter(Task.status == "Terminé").count(),
    }

    projects_completion = {}
    for project in db.query(Project).all():
        total_tasks_project = db.query(Task).filter(Task.project_id == project.id).count()
        done_tasks_project = db.query(Task).filter(Task.project_id == project.id, Task.status == "Terminé").count()
        completion_rate = (done_tasks_project / total_tasks_project * 100) if total_tasks_project > 0 else 0
        projects_completion[project.name] = completion_rate

    now = datetime.now()
    tasks_created_per_day = defaultdict(int)
    tasks_completed_per_day = defaultdict(int)

    for task in db.query(Task).all():
        if hasattr(task, "created_at") and task.created_at:
            created_date = task.created_at.strftime("%Y-%m-%d")
            tasks_created_per_day[created_date] += 1

        if hasattr(task, "completed_at") and task.completed_at:
            completed_date = task.completed_at.strftime("%Y-%m-%d")
            tasks_completed_per_day[completed_date] += 1

    projects_activity = {}
    for project in db.query(Project).all():
        projects_activity[project.name] = db.query(Task).filter(Task.project_id == project.id).count()

    overdue_tasks = db.query(Task).filter(Task.due_date < now, Task.status != "Terminé").count()

    return {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "tasks_status": tasks_status,
        "projects_completion": projects_completion,
        "tasks_created_per_day": dict(tasks_created_per_day),
        "tasks_completed_per_day": dict(tasks_completed_per_day),
        "projects_activity": projects_activity,
        "overdue_tasks": overdue_tasks,
    }

### 📌 Modifier un projet
@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_update: ProjectCreate, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")

    db_project.name = project_update.name
    db_project.description = project_update.description

    db.commit()
    db.refresh(db_project)
    return db_project


### 📌 Supprimer un projet
@router.delete("/projects/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")

    db.delete(project)
    db.commit()
    return {"message": "Projet supprimé"}

### 📌 Modifier une tâche (Titre, Description, Date d’échéance, Statut)
@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    # Mise à jour uniquement des champs fournis
    for field, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


### 📌 Supprimer une tâche
@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    db.delete(db_task)
    db.commit()
    return {"message": "Tâche supprimée"}
