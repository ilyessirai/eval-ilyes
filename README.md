# 🛡️ TechSecure - Application Flask Conteneurisée et Sécurisée

Projet réalisé dans le cadre de l'évaluation Greta. Cette application est un portail web sécurisé pour l'entreprise **TechSecure**, permettant notamment la gestion et la visualisation de ses filiales.

L'objectif principal de ce projet était de reprendre une application existante comportant des vulnérabilités critiques, de corriger son code, de sécuriser ses accès et de la conteneuriser entièrement à l'aide de Docker.

## 🚀 Guide d'Installation Rapide

Suivez ces étapes pour installer et lancer le projet sur votre machine en quelques secondes grâce à Docker.

### 1. Prérequis
- **Git** installé.
- **Docker Desktop** démarré.

### 2. Cloner le projet
### 2. Cloner le projet
Ouvrez un terminal et récupérez le dépôt GitHub :
```bash
git clone https://github.com/ilyessirai/eval-ilyes
cd eval-ilyes

3. Configurer l'environnement (.env)

FLASK_SECRET_KEY=9a8b7c6d5e4f3g2h1i0j_greta_secure_key_2026
FLASK_DEBUG=True

DB_HOST=db
DB_USER=root
DB_PASSWORD=techsecure_docker_password123
DB_NAME=techsecure_db

Lancer l'application avec Docker
Pas besoin d'installer Python ou MySQL sur votre machine locale. Lancez simplement la commande suivante à la racine du projet :

docker-compose up --build

Accéder au site web
Une fois le déploiement terminé dans le terminal, ouvrez votre navigateur et rendez-vous sur :
👉 http://localhost:5000