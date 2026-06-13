Start the server with test settings:

`uv run uvicorn backend.main:app --reload --reload-dir ../backend --env-file .env`