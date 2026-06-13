# from backend.cli import app as cli_app
# from backend.main import app


# def get_testgame_config():
#     return {
#         "name": "test game",
#         "size": 2,
#         "creator": "player 1"
#     }


# def test_create_game(client, runner):
#     client.post("/lobbies", json=get_testgame_config())
#     result = runner.invoke(cli_app, ['list'])
#     assert "test game" in result.output
#     # assert client.get("/lobbies").json() == []


# def test_game_public_after_first_player_connects(client):
#     lobby = client.post("/lobbies", json=get_testgame_config()).json()
#     with client.websocket_connect(f"/lobbies/{lobby['id']}/connect") as conn:
#         assert client.get("/lobbies").json() == [lobby]

def test_server_responding_properply_on_wrong_code(client):
    response = client.post("/lobbies/WRONG/join")
    assert response.status_code == 404, response.json()

def test_join_twice(client):
    ...

def test_user_in_game_after_joining(client):
    ...