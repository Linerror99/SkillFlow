# Utiliser l'image Python officielle
FROM python:3.12

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers du projet
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000 (FastAPI)
EXPOSE 8000

# Commande pour lancer l'API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
