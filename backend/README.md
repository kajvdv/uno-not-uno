# pesten-fastapi
Fastapi app that hosts pesten games.

# Installation
Backend depends on the following env variables.
```
DB_CONN_STRING=<connection string for sqlalchemy>
LOBBIES_DIR=<directory to save existing lobbies when app stops>
ACCESS_TOKEN_SECRET=<see how to generate below>
REFRESH_TOKEN_SECRET=<see how to generate below>
```

Initialize the database with `python -m app.init_db`.

Load env variables in the terminal using `export $(xargs < .env)` (linux).

Start the app with `fastapi dev` for development and `fastapi run` for production.

You can also use `uvicorn app.main:app --env-file=.env` to use .env without loading it in the terminal beforehand 

Navigate to `localhost:8000/docs` to see if the app runs

Pypesten should be manually installed with a seperate pip install. 

## Building the Docker image
Run `docker build -t pesten-fastapi .` to build the docker image. The tag is important since it gets referenced by the deploy repo.

## Generate secrets
Use this command: `openssl rand -hex 32` to generate secrets. Use git bash to run this command on Windows.