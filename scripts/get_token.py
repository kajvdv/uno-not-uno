import os
from datetime import datetime, timedelta, timezone
from jose import  jwt


access_token = jwt.encode(
    {"sub": "admin", 'exp': datetime.now(timezone.utc) + timedelta(days=7)},
    key=os.environ["ACCESS_TOKEN_SECRET"],
    algorithm="HS256"
)

print(access_token)