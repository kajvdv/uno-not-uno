FROM python:3.12-slim AS prod
WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .

CMD ["fastapi", "run", "src/backend/main.py", "--host", "0.0.0.0", "--port", "8000"]
