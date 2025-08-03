import os

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.reload import Reloader
from app.testclient import Client





@pytest.fixture()
def add_lobbies(client, lobbies):
    with client:
        for lobby in lobbies:
            name, size, ai_count = lobby
            client.create_lobby(
                name=name,
                size=size,
                aiCount=ai_count
            )

TEST_LOBBIES_PARAMS = [
    (
        ('test_lobby', 2, 0),
    ),
]



class TestReload:

    @pytest.mark.usefixtures('add_lobbies')
    @pytest.mark.parametrize('lobbies', TEST_LOBBIES_PARAMS)
    def test_reload(self, client):
        print("Start test_reload")
        with client:
            lobbies = client.get_lobbies()
        assert len(lobbies.json()) == 1



    @pytest.mark.usefixtures('add_lobbies')
    @pytest.mark.parametrize('lobbies', [
        [('test_lobby', 2, 1)],
    ])
    def test_reconnect_ai(self, client):
        # # with client:
        # #     lobbies = client.get_lobbies()
        # #     assert len(lobbies.json()) == 0
        # #     client.create_lobby(
        # #         name='test_lobby',
        # #         size=3,
        # #         aiCount=1
        # #     )

        # with client:
        #     lobbies = client.get_lobbies()
        # assert len(lobbies.json()) == 1
        with client:
            connection = client.connect_game('test_lobby')
            with connection:
                connection.play_turn(-1)
                print(connection.connection.receive_json())
        
        with client:
            connection = client.connect_game('test_lobby')
            with connection:
                connection.play_turn(-1)
                print(connection.connection.receive_json())
        


def test_game_against_ai(client, username):
    from pesten.pesten import Pesten, card
    name = 'play_ai'
    with client:
        # client.create_lobby(name=name, size=2, aiCount=1)
        response = client.add_game(game, name, 1)
        if username != 'admin':
            assert response.status_code == 403
            return 
        with client.connect_game(name) as connection:
            while not game.has_won:
                print(connection.play_turn(-1))
                print(connection.connection.receive_json())
                game = client.get_game(name)
    # assert 0