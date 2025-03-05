from app.database import Base, engine
from app.models import Project, Task  # Importer les modèles

def init_db():
    print("📌 Création des tables en cours...")
    Base.metadata.drop_all(bind=engine)  # Supprime les tables existantes
    Base.metadata.create_all(bind=engine)  # Recrée les tables
    print("✅ Base de données initialisée avec succès !")

if __name__ == "__main__":
    init_db()
