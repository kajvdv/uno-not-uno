
from dotenv import load_dotenv
load_dotenv()

import pickle

import requests as re

from app.auth import generate_access_token

token = generate_access_token('admin', 1)
with re.Session() as session:
    session.headers['Authorization'] = f"Bearer {token}"
    response = session.get('http://localhost:5173/api/lobbies')
    lobbies = response.json()
    first = lobbies[0]['id']
    response = session.get(f'http://localhost:5173/api/admin/game/{first}')
    assert response.status_code == 200
    data = response.content
    

game, creator, player_names, chooses, ai_count, lobby_create = pickle.loads(data)

print(game.play_stack)