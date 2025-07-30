# uno-not-uno
Portfolio project that demostrates my knowledge about full-stack web development. This includes:
- backend development with Fastapi
- frontend development with React
- deployment with Docker
- code organization
- other DevOps practices

## Run with Docker
`docker compose up`

## Run local
Run the app locally for easy debugging.
It is easier to attach a debugger to it.
Local app uses the same data as the docker dev one.
Stop the backend container before debugging.
Before installation, set environment variables.
### Backend
1. `python3 -m venv .venv`
2. `pip install -e ./pypesten`
2. `pip install -e ./backend`
3. `uvicorn app.main:app` to run the backend.

### Frontend
1. `cd frontend`
2. `npm install`
3. `npm run dev`

# Deployment