from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# URL de connexion à PostgreSQL (change localhost par ton serveur distant si nécessaire)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@db:5432/skillflow_db")

# Création du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Création de la session pour interagir avec la base de données
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclaration de la base des modèles
Base = declarative_base()

# Dépendance pour obtenir une session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
