import pytest

from app.client import Client


@pytest.mark.anyio
class TestGame:
    async def test_create_connect_to_game(self, client: Client, user: str):
        name = 'test_lobby'
        size = 2
        ai_count = 0
        response = await client.create_lobby(
            name=name,
            size=size,
            aiCount=ai_count,
        )
        assert response.status_code == 200, response.json()
        async with client.connect_game(name) as conn:
            await conn.play_turn(-1)
