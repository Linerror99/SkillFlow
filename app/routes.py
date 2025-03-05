from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Task, Project
from app.schemas import ProjectCreate, ProjectResponse, TaskCreate, TaskResponse, TaskStatus
from sqlalchemy.sql import func
from datetime import date

router = APIRouter()

# Fonction pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Créer une tâche
@router.post("/tasks/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# Lister les tâches d’un projet
@router.get("/projects/{project_id}/tasks/", response_model=list[TaskResponse])
def get_tasks_by_project(project_id: int, db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.project_id == project_id).all()

# Récupérer les tâches par date (Vue calendrier)
@router.get("/tasks/date/{date}/", response_model=list[TaskResponse])
def get_tasks_by_date(date: str, db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.due_date == date).all()

@router.post("/projects/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(name=project.name, description=project.description)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project



# Mettre à jour une tâche
@router.put("/tasks/{task_id}/", response_model=TaskResponse)
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


# Supprimer une tâche
@router.delete("/tasks/{task_id}/", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = db.query(Task).filter(Task.id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")

    db.delete(db_task)
    db.commit()
    
    return {"message": "Tâche supprimée avec succès"}

# Mettre à jour un projet
@router.put("/projects/{project_id}/", response_model=ProjectResponse)
def update_project(project_id: int, project_update: ProjectCreate, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()
    
    if not db_project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")

    db_project.name = project_update.name
    db_project.description = project_update.description
    
    db.commit()
    db.refresh(db_project)
    
    return db_project


# Supprimer un projet
@router.delete("/projects/{project_id}/", response_model=dict)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(Project).filter(Project.id == project_id).first()

    if not db_project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")

    # Vérifier s'il y a des tâches associées
    tasks_count = db.query(Task).filter(Task.project_id == project_id).count()
    if tasks_count > 0:
        raise HTTPException(status_code=400, detail="Impossible de supprimer un projet contenant des tâches")

    db.delete(db_project)
    db.commit()
    
    return {"message": "Projet supprimé avec succès"}



@router.get("/dashboard/", response_model=dict)
def get_dashboard(db: Session = Depends(get_db)):
    # Nombre total de projets et tâches
    total_projects = db.query(Project).count()
    total_tasks = db.query(Task).count()

    # Compter les tâches par statut
    tasks_todo = db.query(Task).filter(Task.status == TaskStatus.TODO).count()
    tasks_in_progress = db.query(Task).filter(Task.status == TaskStatus.IN_PROGRESS).count()
    tasks_done = db.query(Task).filter(Task.status == TaskStatus.DONE).count()

    # Tâches en retard
    today = date.today()
    overdue_tasks = db.query(Task).filter(Task.due_date < today, Task.status != TaskStatus.DONE).count()

    # Calcul de l'avancement des projets
    projects_progress = []
    projects = db.query(Project).all()
    for project in projects:
        project_tasks = db.query(Task).filter(Task.project_id == project.id).count()
        completed_tasks = db.query(Task).filter(Task.project_id == project.id, Task.status == TaskStatus.DONE).count()
        progress = (completed_tasks / project_tasks * 100) if project_tasks > 0 else 0
        projects_progress.append({
            "project_id": project.id,
            "name": project.name,
            "progress": round(progress, 2)
        })

    return {
        "total_projects": total_projects,
        "total_tasks": total_tasks,
        "tasks_status": {
            "todo": tasks_todo,
            "in_progress": tasks_in_progress,
            "done": tasks_done
        },
        "overdue_tasks": overdue_tasks,
        "projects_progress": projects_progress
    }
