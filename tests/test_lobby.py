import pytest

from sqlalchemy.orm import Session

from app.client import Client


@pytest.mark.anyio
class TestLobby:
    # Every test starts with creating a lobby
    #TODO parameterize creating lobbies
    async def test_crud_lobby(self, client: Client, user: str):
        name = 'test_lobby'
        size = 2
        ai_count = 0
        response = await client.create_lobby(
            name=name,
            size=size,
            aiCount=ai_count,
        )
        assert response.status_code == 200, response.json()
        response = await client.get_lobbies()
        data = response.json()
        assert len(data) == 1, data
        assert len([l for l in data if l['creator'] == user]) == 1

        response = await client.delete_lobby(name)
        response = await client.get_lobbies()
        data = response.json()
        assert len(data) == 0, data


    async def test_lobby_already_exists(self, client, user):
        name = 'test_lobby'
        size = 2
        ai_count = 0
        response = await client.create_lobby(
            name=name,
            size=size,
            aiCount=ai_count,
        )
        assert response.status_code == 200
        response = await client.create_lobby(
            name=name,
            size=size,
            aiCount=ai_count,
        )
        assert response.status_code == 400
        assert response.json()['detail'] == "Lobby name already exists"

        
    async def test_cant_delete_other_user_lobby(self, client, user):
        name = 'test_lobby'
        size = 2
        ai_count = 0
        response = await client.create_lobby(
            name=name,
            size=size,
            aiCount=ai_count,
        )
        assert response.status_code == 200
        # Create other user
        await client.register('other', 'password')
        await client.login('other', 'password')
        response = await client.delete_lobby(name)
        assert response.status_code == 403
        assert response.json()['detail'] == "This lobby does not belong to you"


    async def test_get_rules_lobby(self, client, user):
        name = 'test_lobby'
        size = 2
        ai_count = 0
        response = await client.create_lobby(
            name=name,
            size=size,
            aiCount=ai_count,
            two='test_rule',
        )
        assert response.status_code == 200
        response = await client.get_lobby_rules(name)
        assert response.json()['2'] == 'test_rule'