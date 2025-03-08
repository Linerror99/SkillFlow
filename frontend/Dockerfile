# Utilisation de Node.js 18
FROM node:18

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement package.json (ignorer package-lock.json si inexistant)
COPY package.json ./

# Installer les dépendances (sans cache)
RUN npm install

# Copier tout le projet après l’installation
COPY . .

# Exposer le port du frontend
EXPOSE 3000

# Commande pour démarrer React
CMD ["npm", "start"]
