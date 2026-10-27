# DevOps Docker Lab: Step-by-Step Runbook

This runbook guides students through all 11 modules of the Docker syllabus, including **Lab A** (Three-Tier Stack) and **Lab B** (Hardened Nginx Reverse Proxy Architecture).

Every command block starts from the **repository root directory** (`docker-flask-react-lab`), in exact chronological order. You can copy and paste each code block directly into your terminal.

---

## Part 0: Prerequisites & Repository Setup

Check that required tools are installed on your machine and clone the repository.

```bash
# Verify Docker engine is installed and running
docker --version

# Verify Docker Compose plugin is available
docker compose version

# Verify Git is installed
git --version
```

### Clone and Enter the Repository

```bash
git clone https://github.com/<your-username>/docker-flask-react-lab.git
cd docker-flask-react-lab
```

---

## Module 1: Introduction to Containers

**Goal:** Run your first lightweight container from Docker Hub to verify the Docker daemon is responding.

### Execution

```bash
# Run the official hello-world container
docker run --rm hello-world
```

### Expected Output
```text
Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### Cleanup
The `--rm` flag automatically cleans up and deletes the container when execution finishes.

---

## Module 2: Essential Docker CLI Commands

**Goal:** Practice creating, inspecting, accessing, and stopping background (detached) containers.

### Execution

```bash
# Start an Nginx web server in detached mode mapped to port 8080
docker run -d --name demo-web -p 8080:80 nginx:alpine

# List active containers
docker ps

# Check container standard output logs
docker logs demo-web

# Execute a command inside the running container to inspect its version
docker exec demo-web nginx -v

# Test container response from host
curl -I http://localhost:8080
```

### Expected Output
`docker ps` displays `demo-web` with status `Up`. The `curl` command returns `HTTP/1.1 200 OK`.

### Cleanup

```bash
# Stop and delete the container
docker stop demo-web
docker rm demo-web
```

---

## Module 3: Docker Images & Registry Basics

**Goal:** Pull, list, tag, and inspect image layers from Docker Hub.

### Execution

```bash
# Pull the base Python image used in our labs
docker pull python:3.12-slim

# List local images matching python
docker images python:3.12-slim

# Create a local development tag for this image
docker tag python:3.12-slim my-python:local

# Inspect image history to see individual layers
docker history my-python:local
```

### Expected Output
Both `python:3.12-slim` and `my-python:local` appear in `docker images` with the same Image ID.

### Cleanup

```bash
# Remove the custom tag
docker rmi my-python:local
```

---

## Module 4: Building Single-Stage Images (`01-flask-basic`)

**Goal:** Package and run a minimal Python Flask API using a single-stage Dockerfile.

### Execution

```bash
# Navigate to the 01-flask-basic directory
cd 01-flask-basic

# Build the Docker image
docker build -t flask-basic:1.0 .

# Run the container in detached mode mapping host port 5000 to container port 5000
docker run -d --name flask-basic-app -p 5000:5000 flask-basic:1.0

# Verify the container is running
docker ps

# Test the root endpoint
curl -i http://localhost:5000/

# Test the health check endpoint
curl -i http://localhost:5000/health

# Inspect container output logs
docker logs flask-basic-app
```

### Expected Output
- `GET /` returns `{"message": "Welcome to Flask Docker Lab!", "status": "running"}`.
- `GET /health` returns `{"status": "healthy"}`.

### Cleanup

```bash
# Stop and remove the container, then return to repository root
docker stop flask-basic-app
docker rm flask-basic-app
cd ..
```

---

## Module 5: Multi-Stage Builds & Optimization (`02-flask-multistage`)

**Goal:** Build a secure, lightweight container using a multi-stage Dockerfile with a virtual environment and a non-root user.

### Execution

```bash
# Navigate to 02-flask-multistage
cd 02-flask-multistage

# Build the multi-stage image
docker build -t flask-multistage:1.0 .

# Run the container with Gunicorn
docker run -d --name flask-multi-app -p 5000:5000 flask-multistage:1.0

# Verify the container is running
docker ps

# Test endpoints
curl -i http://localhost:5000/
curl -i http://localhost:5000/health

# Verify that the container is running as the non-root user (appuser)
docker exec flask-multi-app whoami

# Compare image sizes between single-stage and multi-stage
docker images | grep flask
```

### Expected Output
`docker exec flask-multi-app whoami` outputs `appuser`. The application returns JSON with `"server": "gunicorn"`.

### Cleanup

```bash
# Stop and remove the container, then return to repository root
docker stop flask-multi-app
docker rm flask-multi-app
cd ..
```

---

## Module 6: Containerizing the React Frontend

**Goal:** Compile a React single-page application into static assets using Node.js and serve it through Nginx.

### Execution

```bash
# Navigate to 03-three-tier/frontend
cd 03-three-tier/frontend

# Build the frontend Docker image
docker build -t react-frontend:1.0 .

# Run the frontend container independently on port 3000
docker run -d --name frontend-standalone -p 3000:80 react-frontend:1.0

# Verify HTTP response
curl -I http://localhost:3000
```

### Expected Output
Returns `HTTP/1.1 200 OK` from Nginx, serving the compiled `index.html`.

### Cleanup

```bash
# Stop and remove standalone test container, then return to repository root
docker stop frontend-standalone
docker rm frontend-standalone
cd ../..
```

---

## Module 7: Introduction to Docker Compose

**Goal:** Understand declarative multi-container orchestration using `compose.yaml`.

### Execution

```bash
# Navigate to 03-three-tier
cd 03-three-tier

# Validate and preview the compose specification
docker compose config

# Start only the database service in detached mode
docker compose up -d database

# Verify database container status
docker compose ps

# Inspect PostgreSQL initialization logs
docker compose logs database
```

### Expected Output
The `database` container status is `Up`, and logs confirm PostgreSQL is ready to accept connections on port 5432.

### Cleanup

```bash
# Tear down the single service
docker compose down -v
cd ..
```

---

## Module 8: Lab A - Full Three-Tier Stack (`03-three-tier`)

**Goal:** Deploy and test the complete three-tier application (PostgreSQL 17, Flask 3.12 with Gunicorn, and React on Nginx) with volume persistence.

### Execution

```bash
# Navigate to 03-three-tier
cd 03-three-tier

# Build images and start all three services in detached mode
docker compose up -d --build

# Verify all services are running
docker compose ps

# Check backend logs to verify database connection and table creation
docker compose logs backend

# 1. Test backend health check
curl -i http://localhost:5000/api/health

# 2. Save a message to the database via POST
curl -i -X POST http://localhost:5000/api/message \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello DevOps from Lab A!"}'

# 3. Retrieve the latest message via GET
curl -i http://localhost:5000/api/message

# 4. Open the frontend in your browser or test with curl
curl -I http://localhost:3000
```

You can open `http://localhost:3000` in your web browser, type a message, and click **Save**.

### Persistence Test (Crucial Step)

```bash
# Stop and remove containers (DO NOT PASS -v FLAG!)
docker compose down

# Check that containers are stopped
docker compose ps

# Restart the stack using existing volume
docker compose up -d

# Verify that our previous message survived container removal
curl -i http://localhost:5000/api/message
```

> [!WARNING]
> **Warning:** Running `docker compose down -v` permanently deletes the named volume `postgres-data` and all database records. Only use `-v` when you intend to erase all data during complete cleanup.

### Cleanup

```bash
# Remove containers and the persistent volume
docker compose down -v
cd ..
```

---

## Module 9: Docker Networking in Practice

**Goal:** Understand container DNS resolution on custom networks, port publishing, and network isolation.

### Execution

```bash
# 1. Create a custom user-defined bridge network
docker network create lab-net

# 2. Run an Nginx container attached to lab-net (no published ports to host)
docker run -d --name web-internal --network lab-net nginx:alpine

# 3. Resolve and reach web-internal by its container name from another container
docker run --rm --network lab-net curlimages/curl:8.10.1 http://web-internal

# 4. Notice that web-internal cannot be reached directly from host localhost
curl http://localhost:80
```

### Expected Output
The curl container inside `lab-net` successfully retrieves Nginx's welcome page by resolving `http://web-internal`. The host `curl http://localhost:80` fails because no host port was published.

### Cleanup

```bash
# Stop and remove container, then remove the network
docker stop web-internal
docker rm web-internal
docker network rm lab-net
```

---

## Module 10: Docker Storage & Data Persistence

**Goal:** Compare bind mounts and named volumes, and verify data survives container destruction.

### Scenario 1: Bind Mount (Host-to-Container Sharing)

```bash
# Mount current directory into an Alpine container to inspect files
docker run --rm -v "$(pwd)/01-flask-basic:/workspace:ro" alpine ls -la /workspace
```

### Scenario 2: Named Volume Data Survival

```bash
# 1. Create a named volume
docker volume create storage-demo

# 2. Write data to the named volume from container A
docker run --rm -v storage-demo:/data alpine sh -c "echo 'DevOps volume data' > /data/info.txt"

# 3. Read the data from a brand-new container B
docker run --rm -v storage-demo:/data alpine cat /data/info.txt
```

### Expected Output
Container B reads and outputs `'DevOps volume data'` proving data persisted across container lifecycles.

### Cleanup

```bash
# Delete the demo volume
docker volume rm storage-demo
```

---

## Module 11: Lab B - Reverse Proxy Architecture (`04-three-tier-nginx`)

**Goal:** Deploy a hardened production architecture where only Nginx publishes host port 8080, isolating frontend and internal database networks.

### Execution

```bash
# Navigate to 04-three-tier-nginx
cd 04-three-tier-nginx

# Build images and start all 4 services
docker compose up -d --build

# Verify all services are running
docker compose ps

# Validate Nginx configuration inside the proxy container
docker compose exec nginx nginx -t

# 1. Test backend health check through Nginx reverse proxy
curl -i http://localhost:8080/api/health

# 2. Save a message through Nginx reverse proxy
curl -i -X POST http://localhost:8080/api/message \
  -H "Content-Type: application/json" \
  -d '{"text": "Production architecture works perfectly!"}'

# 3. Fetch latest message through Nginx reverse proxy
curl -i http://localhost:8080/api/message

# 4. Fetch frontend UI through Nginx reverse proxy
curl -I http://localhost:8080/
```

Open `http://localhost:8080` in your web browser to interact with the full stack.

### Network Isolation Verification

```bash
# Database is on database-network (internal: true)
# Verify database has NO direct internet access or public port mapping
docker compose exec database ping -c 1 8.8.8.8 || echo "Database has no public egress (as expected)"
```

### Persistence Test

```bash
# Stop containers without removing volume
docker compose down

# Bring stack back up
docker compose up -d

# Verify persisted data
curl -i http://localhost:8080/api/message
```

### Cleanup

```bash
# Remove containers and the persistent database volume
docker compose down -v
cd ..
```

---

## Part 12: Publishing to GitHub and Docker Hub

### 1. Initialize Git Repository and Commit per Lab Folder

```bash
# Initialize git in repository root
git init

# Commit 1: Project setup and documentation
git add .gitignore .env.example README.md docs/
git commit -m "docs: initial repository setup and documentation"

# Commit 2: Basic Flask container
git add 01-flask-basic/
git commit -m "feat(01): basic single-stage Flask container"

# Commit 3: Multi-stage Flask container
git add 02-flask-multistage/
git commit -m "feat(02): multi-stage Flask container with gunicorn and non-root user"

# Commit 4: Three-tier compose application
git add 03-three-tier/
git commit -m "feat(03): three-tier compose stack with React, Flask, and PostgreSQL"

# Commit 5: Hardened Nginx reverse proxy stack
git add 04-three-tier-nginx/
git commit -m "feat(04): production compose stack with Nginx proxy and network isolation"
```

### 2. Push to GitHub

```bash
# Set primary branch to main
git branch -M main

# Link your remote GitHub repository
git remote add origin https://github.com/<your-username>/docker-flask-react-lab.git

# Push all commits to GitHub
git push -u origin main
```

### 3. Tag and Push Flask Image to Docker Hub

```bash
# Authenticate with Docker Hub
docker login

# Tag the multi-stage Flask image with your Docker Hub username
docker tag flask-multistage:1.0 <your-dockerhub-username>/flask-multistage:1.0

# Push the image to Docker Hub
docker push <your-dockerhub-username>/flask-multistage:1.0
```
