import pickle
import logging
import pytest
from contextlib import ExitStack

from app.client import Client

@pytest.fixture
def token(username, client):
    return client.headers['Authorization'].split()[1]

def test_register_and_login(client, username):
    assert client.client.headers['Authorization']


def test_admin_add_game(client, username):
    from pesten.pesten import Pesten, card
    cards = [card(suit, value) for suit in range(4) for value in range(13)]
    game = Pesten(2, 8, cards)
    response = client.add_game(game, "direct", 0)
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


class TestLobbyEndpoint:
    def test_create_lobby(self):
        ...

    def test_get_rules(self):
        ...

    def test_delete_lobby(self):
        ...

# @pytest.mark.usefixtures('with_lobbies')
@pytest.mark.parametrize('lobbies', [
    [('play_game', 2, 0)]
])
def test_play_game(client: Client, lobbies):
    from app.auth import generate_access_token
    from pesten.agent import Agent
    from pesten.pesten import Pesten, card
    name, size, ais = lobbies[0]
    cards = [card(suit, value) for suit in range(4) for value in range(13)]
    game = Pesten(size, 8, cards)
    # agents = [Agent(1), Agent(2)]
    agents = [Agent(i) for i in range(size-ais)]
    lobby_name = name
    with client:
        client.add_game(game, lobby_name, ais, generate_access_token('admin'))
        # connections = (
        #     client.connect_game(lobby_name, generate_access_token('admin')),
        #     client.connect_game(lobby_name, generate_access_token('user')),
        # )
        connections = [
            client.connect_game(lobby_name, generate_access_token(f'testuser-{i}'))
            for i in range(size-ais)
        ]

        # connections.start()
        # with connections[0], connections[1]:
        #     ...
        # # i = 0
        with ExitStack() as stack:
            # conns = [stack.enter_context(c) for c in connections]
            # conns = [stack.enter_context(c) for c in connections]
            for c in connections:
                conn = stack.enter_context(c)
                conn.start_receiving()
                raise Exception("excep")
                assert 0
        #     # connections[i].connection.receive_json()
            while not game.has_won:
                game = client.get_game(lobby_name)
                print(game.players)
        #         # choose = agents[i].generate_choose(game)
        #         # logging.info(f'Agent plays {choose}')
        #         # connections[i].play_turn(choose)
        #         # i += 1
        #         # i %= 2
        #         # response = client.get_game(lobby_name)
        #         # game, *_ = pickle.loads(response.content)
    
