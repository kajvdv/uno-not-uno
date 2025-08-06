# uno-not-uno
Portfolio project that demostrates my knowledge about full-stack web development. This includes:
- backend development with Fastapi
- frontend development with React
- deployment with Docker
- code organization
- other DevOps practices


## Testing
First party modules are imported in the tests.
This gives more control over setting up the environment before importing them.
An example is setting environment variables that are needed at import time.

## Scripts folder
This contains usefull code for development. The same .env file should be used locally as in Docker to make sure that these scripts will work.

## Local development
1. `python -m venv .venv`
1. enter virtual environment
2. `pip install -r requirements.txt`

## Bot developement
cd to chrome.exe: `cd "C:\Program Files\Google\Chrome\Application"`
`./chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Selenium\ChromeProfile"`
This will open a debug session make it easy for to develop the bot.

## Run
`docker compose up`

# Deployment