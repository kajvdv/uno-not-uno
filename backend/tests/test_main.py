from urllib.parse import urlsplit

import pytest
from fastapi.testclient import TestClient

from backend.auth import decode_token


TESTGAME = {
    "size": 2,
    "creator": "player 1"
}


@pytest.fixture
def clients(app):
    with TestClient(app) as client_1:
        client_2 = TestClient(app)
        yield client_1, client_2


def test_create_and_join_game(clients):
    user_1, user_2 = clients

    # Player 1 creates a game
    frontend_url = user_1.post("/lobbies", json=TESTGAME).json()['url']

    # Player 2 receives the url pastes it into the browser.
    # App modifies url to join game by getting cookie.
    backend_url = urlsplit(frontend_url).path + "/join"
    user_2.post(backend_url, json={"username": "player 2"})

    assert decode_token(user_1.cookies['sessionToken']).items() >= {"sub": "player 1"}.items()
    assert decode_token(user_2.cookies['sessionToken']).items() >= {"sub": "player 2"}.items()


def test_get_url_after_creation(clients):
    client, _ = clients
    frontend_url = client.post("/lobbies", json=TESTGAME).json()["url"]
    assert client.get("/lobbies/current").json()['url'] == frontend_url


def test_users_should_receive_same_websocket_url(clients):
    user1, user2 = clients
    lobby = user1.post("/lobbies", json=TESTGAME).json()
    backend_url = urlsplit(lobby['url']).path + "/join"
    user2.post(backend_url, json={"username": "player 2"})
    
    ws_url_1, url_1 = user1.get("/lobbies/current").json().values()
    ws_url_2, url_2 = user2.get("/lobbies/current").json().values()
    assert lobby['url'] == url_1
    assert lobby['url'] == url_2
    assert ws_url_1 == ws_url_2


def test_main_happy_path(clients):
    user1, user2 = clients
    lobby = user1.post("/lobbies", json=TESTGAME).json()
    # print(lobby)
    backend_url = urlsplit(lobby['url']).path + "/join"
    user2.post(backend_url, json={"username": "player 2"})

    ws_url, _ = user1.get("/lobbies/current").json().values()
    
    with (
        user1.websocket_connect(ws_url) as user1_ws,
        user2.websocket_connect(ws_url) as user2_ws,
    ):
        print(user1_ws.receive_json())
        print(user2_ws.receive_json())
        user1_ws.send_text("0")
        print(user1_ws.receive_json())
        print(user2_ws.receive_json())

    assert 0
