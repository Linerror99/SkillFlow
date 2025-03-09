# Utilisation de Python 3.12
FROM python:3.12

# Définir le répertoire de travail
WORKDIR /app
ENV PYTHONPATH="/app"

# Copier uniquement requirements.txt d'abord pour optimiser le cache Docker
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application après l'installation des dépendances
COPY . .

# Exposer le port de l'API
EXPOSE 8000

# Commande pour démarrer l'API avec une attente pour la base de données
CMD ["sh", "-c", "sleep 10 && python init_db.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
