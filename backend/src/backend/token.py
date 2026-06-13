import os
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt, ExpiredSignatureError


TOKEN_SECRET = os.environ["TOKEN_SECRET"]
ALGORITHM = "HS256"


def generate_token(username: str, lobby_code: str):
    access_token = jwt.encode(
        {"sub": username, "lobby": lobby_code, 'exp': datetime.now(timezone.utc) + timedelta(minutes=15)},
        key=TOKEN_SECRET,
        algorithm="HS256"
    )
    return access_token


def decode_token(token):
    return jwt.decode(token, TOKEN_SECRET, algorithms=[ALGORITHM])