# Script to create the env file with the vars.

import os
from pathlib import Path
import secrets


email = input("Choose email for database: ")

ENV_FILE = ".env"
DEFAULTS = {
    "DB_CONN_STRING": "postgresql://username:password@db:5432/master",
    "LOBBIES_DIR": "data/lobbies",
    "ACCESS_TOKEN_SECRET": None,  # To be generated
    "REFRESH_TOKEN_SECRET": None,  # To be generated
    "BACKEND_URL": "http://backend:8000",
    "WEBSOCKET_URL": "ws://backend:8000",
    "POSTGRES_USER": "username",
    "POSTGRES_PASSWORD": "password",
    "PGADMIN_DEFAULT_EMAIL": email,
    "PGADMIN_DEFAULT_PASSWORD": "password",
}

def generate_secret():
    return secrets.token_hex(32)

def create_env_file(path=ENV_FILE):
    env_path = Path(path)
    if env_path.exists():
        print(f"{ENV_FILE} already exists. Skipping creation.")
        return

    DEFAULTS["ACCESS_TOKEN_SECRET"] = generate_secret()
    DEFAULTS["REFRESH_TOKEN_SECRET"] = generate_secret()

    with env_path.open("w") as f:
        for key, value in DEFAULTS.items():
            f.write(f"{key}={value}\n")

    print(f"✅ {ENV_FILE} created successfully.")

if __name__ == "__main__":
    create_env_file()
