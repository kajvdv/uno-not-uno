from importlib import reload
import pickle

import logging

from dotenv import load_dotenv
load_dotenv()

import pytest
from app.testclient import TestClient
from app.database import Base
import app
from pesten.pesten import Pesten, card


@pytest.fixture()
def client():
    client = TestClient()
    yield client
    client.drop_tables()
    reload(app.lobby.dependencies)

users = [
    ('admin', 'password'),
    ('user', 'password')
]

@pytest.fixture(params=users, ids=[u[0] for u in users])
def username(request, client):
    client.register(*request.param)
    client.login(*request.param)
    return request.param[0]

@pytest.fixture
def token(username, client):
    return client.headers['Authorization'].split()[1]

def test_register_and_login(client):
    response = client.register('admin', 'admin')
    assert response.status_code == 204, response.text
    response = client.login('admin', 'admin')
    assert response.status_code == 200, response.text


def test_admin_add_game(client, username):
    cards = [card(suit, value) for suit in range(4) for value in range(13)]
    game = Pesten(2, 8, cards)
    response = client.add_game(game, "direct")
    if username != 'admin':
        assert response.status_code == 401
        return
    assert response.status_code == 200, response.text
    response = client.get_lobbies()
    data = response.json()
    assert len(data) == 1
    response = client.get_game('direct')
    assert response.status_code == 200
    loaded_game, *_ = pickle.loads(response.content)
    assert loaded_game.draw_stack == game.draw_stack
    

@pytest.mark.parametrize('size, ai_count', [
    (0, 0),
    (7, 0),
    (1, 0),
    (2, 0),
    (2, 1),
    (2, 2),
])
def test_create_lobby(client, username, size, ai_count):
    response = client.create_lobby(
        name='test_lobby', 
        size=size,
        aiCount=ai_count,
    )
    if size < 2:
        assert response.status_code == 422, (response.status_code, response.text)
    elif size > 6:
        assert response.status_code == 422, (response.status_code, response.text)
    elif ai_count >= size:
        assert response.status_code == 422, (response.status_code, response.text)
    else:
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['creator'] == username
        response = client.get_lobbies()
        data = response.json()
        assert len(data) == 1


def test_connect_to_game(client):
    from app.auth import generate_access_token
    from pesten.agent import Agent
    cards = [card(suit, value) for suit in range(4) for value in range(13)]
    game = Pesten(2, 8, cards)
    agents = [Agent(1), Agent(2)]
    lobby_name = 'test_lobby'
    client.register('admin', 'admin')
    client.login('admin', 'admin')
    client.add_game(game, lobby_name)
    connections = (
        client.connect_game(lobby_name, generate_access_token('admin')),
        client.connect_game(lobby_name, generate_access_token('user')),
    )
    i = 0
    with connections[0], connections[1]:
        # connections[i].connection.receive_json()
        while not game.has_won:
            choose = agents[i].generate_choose(game)
            logging.info(f'Agent plays {choose}')
            connections[i].play_turn(choose)
            i += 1
            i %= 2
            response = client.get_game(lobby_name)
            game, *_ = pickle.loads(response.content)
    