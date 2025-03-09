from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database import SessionLocal, get_db
from app.models import Project, Task, User
from app.schemas import ProjectCreate, ProjectResponse, TaskCreate, TaskResponse,TaskUpdate, UserCreate, UserRead, UserResponse, LoginRequest
from app.auth import authenticate_user, create_access_token, get_password_hash, hash_password, get_current_user
from typing import List
from datetime import datetime, timedelta
from collections import defaultdict

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/register", response_model=UserRead)
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/signup", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Vérifier si l'utilisateur existe déjà
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Cet utilisateur existe déjà")

    # Hasher le mot de passe
    hashed_password = hash_password(user.password)

    # Créer un nouvel utilisateur avec username, email et mot de passe
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/token")
def login(user: LoginRequest, db: Session = Depends(get_db)):
    user_db = authenticate_user(db, user.email, user.password)
    if not user_db:
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


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
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Vérifie l'utilisateur connecté
):
    total_projects = db.query(Project).count()
    total_tasks = db.query(Task).count()

    tasks_todo = db.query(Task).filter(Task.status == "À faire").count()
    tasks_in_progress = db.query(Task).filter(Task.status == "En cours").count()
    tasks_done = db.query(Task).filter(Task.status == "Terminé").count()

    return {
        "user": current_user["email"],  # Affiche l'email de l'utilisateur connecté
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
