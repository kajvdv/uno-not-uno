# uno-not-uno
Portfolio project that demostrates my knowledge about full-stack web development. This includes:
- backend development with Fastapi
- frontend development with React
- deployment with Docker
- code organization
- other DevOps practices


## Scripts folder
This contains usefull code for development. The same .env file should be used locally as in Docker to make sure that these scripts will work.

## Local development
1. `python -m venv .venv`
1. enter virtual environment
2. `pip install -r requirements.txt`


## Testing
In /frontend
```
npm run dev
```
In /accept:
```
uv run uvicorn app.main:app --reload --reload-dir ../backend --env-file .env
accept startbrowser 5001 user1
accept startbrowser 5002 user2
pytest
```

## Run
`docker compose up`

# Deployment