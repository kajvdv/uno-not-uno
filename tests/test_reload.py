import pytest

from fastapi import FastAPI

from app.client import Client


@pytest.fixture(name='app')
async def app_fixture(app_setup):
    return app_setup

@pytest.mark.anyio
class TestReload:
    async def test_lobbies_reload_after_restart(self, client: Client, app: FastAPI, user: str):
        from asgi_lifespan import LifespanManager
        async with LifespanManager(app) as manager:
            client._transport.app = manager.app
            count = 5
            for i in range(count):
                name = f'test_lobby-{i}'
                size = 2
                ai_count = 0
                response = await client.create_lobby(
                    name=name,
                    size=size,
                    aiCount=ai_count,
                )
                assert response.status_code == 200
            response = await client.get_lobbies()
            assert len(response.json()) == count

        async with LifespanManager(app) as manager:
            client._transport.app = manager.app
            response = await client.get_lobbies()
            assert len(response.json()) == count











































# TEST_LOBBIES_PARAMS = [
#     (
#         ('test_lobby', 2, 1),
#         ('test_lobby-2', 2, 1),
#     ),
#     (
#         ('test_lobby', 2, 1),
#     ),
# ]
# @pytest.mark.usefixtures(
#     'username', # Loggin in should be top
#     'with_lobbies',
# )
# class TestReload:

#     @pytest.mark.parametrize('lobbies', TEST_LOBBIES_PARAMS)
#     def test_reload(self, client, lobbies):
#         with client:
#             response = client.get_lobbies()
#         assert len(response.json()) == len(lobbies)
        

#     @pytest.mark.parametrize('lobbies', [
#         [("test_lobby", 2, 1,),],
#         [("test_lobby", 3, 2,),],
#     ])
#     def test_reconnect_ai(self, client: Client, lobbies, username):
#         name, *_ = lobbies[0]
#         for _ in range(2): # Disconnect two times
#             with client:
#                 connection = client.connect_game(name)
#                 with connection:
#                     connection.play_turn(-1)
#                     connection.connection.receive_json()['current_player'] == 'AI1'
#         with client:
#             connection = client.connect_game(name)
#             with connection:
#                 assert connection.connection.receive_json()['current_player'] == 'AI1'
#                 assert connection.connection.receive_json()['current_player'] == username # AI played card
