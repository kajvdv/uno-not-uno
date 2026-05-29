

def get_testgame_config():
    return {
        "name": "test game",
        "size": 2,
        "creator": "player 1"
    }


def test_game_not_public_after_creation(client):
    client.post("/lobbies", json=get_testgame_config())
    assert client.get("/lobbies").json() == []


def test_game_public_after_first_player_connects(client):
    lobby = client.post("/lobbies", json=get_testgame_config()).json()
    with client.websocket_connect(f"/lobbies/{lobby['id']}/connect") as conn:
        assert client.get("/lobbies").json() == [lobby]