# Docker Flask + React Beginner Lab (`docker-flask-react-lab`)

Welcome to the hands-on Docker lab repository! This repository is designed for beginners and DevOps students to learn Docker containerization, multi-stage builds, multi-container orchestration with Docker Compose, networking, volume persistence, and reverse proxy architectures.

Everything is kept minimal, practical, and heavily commented in plain language.

---

## 🚀 Getting Started

Start with our comprehensive, step-by-step runbook:
👉 **[docs/step-by-step.md](docs/step-by-step.md)**

Every single command can be copied and pasted directly into your terminal.

---

## 📁 Repository Structure

```text
docker-flask-react-lab/
├── README.md               # Repository documentation and guide
├── .gitignore              # Ignores secrets, caches, and node_modules
├── .env.example            # Sample environment variables file
├── 01-flask-basic/         # Single-stage Dockerfile with Flask (Python 3.12-slim)
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── 02-flask-multistage/    # Multi-stage Dockerfile (venv, non-root user, Gunicorn)
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
├── 03-three-tier/          # Three-tier stack: React + Flask + PostgreSQL
│   ├── compose.yaml
│   ├── backend/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── .dockerignore
│   └── frontend/
│       ├── package.json
│       ├── vite.config.js
│       ├── index.html
│       ├── src/
│       ├── nginx.conf      # Serves React and proxies /api/ to backend:5000
│       ├── Dockerfile
│       └── .dockerignore
├── 04-three-tier-nginx/    # Production architecture with dedicated Nginx proxy
│   ├── compose.yaml
│   ├── nginx/
│   │   └── default.conf    # Routes / to frontend:80 and /api/ to backend:5000
│   ├── backend/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   └── .dockerignore
│   └── frontend/
│       ├── package.json
│       ├── vite.config.js
│       ├── index.html
│       ├── src/
│       ├── nginx.conf      # Serves static React files only
│       ├── Dockerfile
│       └── .dockerignore
└── docs/
    ├── step-by-step.md     # Full runbook covering Modules 1 to 11
    └── devops-code.pdf     # Visual reference document of all Docker code
```

---

## 🛠️ Troubleshooting Guide

| Issue | Typical Cause | Solution / Fix |
| :--- | :--- | :--- |
| **Port Already in Use**<br>`Bind for 0.0.0.0:5000 failed: port is already allocated` | Another application or previous Docker container is using host port 5000, 3000, or 8080. | 1. Find running containers: `docker ps`<br>2. Stop old containers: `docker stop <container_id>`<br>3. Or change host port in `compose.yaml` (e.g., `"5001:5000"`). |
| **502 Bad Gateway from Nginx** | Nginx cannot establish a connection to the backend service. | 1. Check if backend is running: `docker compose ps`<br>2. Inspect backend logs: `docker compose logs backend`<br>3. Verify backend listens on `0.0.0.0:5000` and shares a common network with Nginx. |
| **Backend Cannot Reach Database**<br>`psycopg2.OperationalError` | PostgreSQL is still starting up or credentials / network names mismatch. | 1. Verify database is running: `docker compose ps database`<br>2. Check database logs: `docker compose logs database`<br>3. Verify `DB_HOST=database` and matching credentials in `compose.yaml`. |

---

## 💡 Better Practice: Use a `.env` File

Hardcoding database credentials directly in `compose.yaml` is acceptable for a beginner lab, but in real-world DevOps environments, credentials should be managed via environment variables.

Follow these 6 simple steps to transition to a `.env` file:

1. **Create your `.env` file** in the project directory:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to define your secret values:
   ```env
   DB_NAME=appdb
   DB_USER=appuser
   DB_PASSWORD=apppass123
   ```

2. **Replace the hardcoded values in `compose.yaml`** with variable references:
   ```yaml
   database:
     image: postgres:17
     environment:
       POSTGRES_DB: ${DB_NAME}
       POSTGRES_USER: ${DB_USER}
       POSTGRES_PASSWORD: ${DB_PASSWORD}
     volumes:
       - postgres-data:/var/lib/postgresql/data

   backend:
     build: ./backend
     environment:
       DB_HOST: database
       DB_PORT: 5432
       DB_NAME: ${DB_NAME}
       DB_USER: ${DB_USER}
       DB_PASSWORD: ${DB_PASSWORD}
   ```

3. **Verify that `.env` is listed in `.gitignore`**:
   Ensure `.gitignore` contains `.env` so secrets are never pushed to GitHub.

4. **Commit `.env.example` with fake values**:
   Keep `.env.example` in Git as a template for other developers:
   ```bash
   git add .env.example .gitignore
   git commit -m "docs: add environment variable template"
   ```

5. **Rebuild and launch your stack**:
   ```bash
   docker compose up -d --build
   ```

6. **Verify the resolved configuration**:
   Run `docker compose config` to inspect how Docker Compose substituted your environment variables without starting the containers:
   ```bash
   docker compose config
   ```
