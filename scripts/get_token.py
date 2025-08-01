# Get a development token for a few days

from dotenv import load_dotenv
load_dotenv()

import os
from datetime import datetime, timedelta, timezone
from jose import  jwt

from app.auth import generate_access_token

def generate_token(name, days):
    access_token = jwt.encode(
        {"sub": name, 'exp': datetime.now(timezone.utc) + timedelta(days=days)},
        key=os.environ["ACCESS_TOKEN_SECRET"],
        algorithm="HS256"
    )
    return access_token

if __name__ == "__main__":
    print(generate_access_token("admin", days=7))