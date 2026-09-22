# eClipseBord

A full-stack Python dashboard built on a NASA solar eclipse dataset, containerized with Docker and deployed to Azure.

## Overview

eClipseBord serves and visualizes solar eclipse data through a small two-service application:

* **Backend** — FastAPI service that reads the dataset and exposes it via a REST API
* **Frontend** — Streamlit dashboard that consumes the backend API and renders tables and charts

The two services are built as separate Python packages in a shared `uv` workspace, containerized independently, and deployed to two different Azure compute services.

## Tech stack

* **Python** — FastAPI, Streamlit, httpx, pandas
* **uv** — workspace and dependency management
* **Docker** — containerization (one image per service)
* **Azure Container Registry** — stores the built images
* **Azure Container App** — runs the backend
* **Azure App Service (Web App)** — runs the frontend

## Architecture

```
Browser
   │
   ▼
Frontend (Azure Web App, Streamlit, port 8501)
   │  httpx.get(BACKEND_URL + "/solar/stats")
   ▼
Backend (Azure Container App, FastAPI, port 8000)
   │  reads solar.csv
   ▼
JSON response → rendered as table/chart in the dashboard
```

The frontend and backend are connected purely through the `BACKEND_URL` environment variable — no code changes are needed to point the same image at a different backend URL across environments (local, Docker Compose, Azure).

## Repository structure

```
.
├── backend/
│   ├── data/solar.csv
│   ├── src/backend/        # FastAPI app (api.py, data_processing.py, constants.py)
│   └── pyproject.toml
├── frontend/
│   ├── src/frontend/       # Streamlit app (dashboard.py)
│   └── pyproject.toml
├── dockerfiles/
│   ├── backend.dockerfile
│   └── frontend.dockerfile
├── docker-compose.yaml
├── eda.ipynb
└── pyproject.toml          # uv workspace root
```

## Running locally

```bash
uv sync
cd backend && uv run uvicorn api:app --reload   # in one terminal
cd frontend && uv run streamlit run dashboard.py # in another
```

## Running with Docker

```bash
docker compose build
docker compose up
```

Builds must target `linux/amd64` for Azure deployment (set via `platform: linux/amd64` in `docker-compose.yaml`) even when building on Apple Silicon.

## Azure deployment

* **Container Registry:** `eclipseregistry`
* **Backend:** Azure Container App (`eclipse-container-app`, resource group `eclipseproject`, Germany West Central)
* **Frontend:** Azure Web App (`eclipse-fullstack`), configured with `WEBSITES_PORT=8501` and `BACKEND_URL` pointing to the backend's public URL

Images are built, tagged, and pushed to the registry, then the respective Azure resource is pointed at the new tag to deploy.
