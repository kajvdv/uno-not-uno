import asyncio
import logging
import pytest

from app.client import Client

logger = logging.getLogger(__name__)

@pytest.fixture
def anyio_backend():
    return 'asyncio'

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
            async with conn.start_receiving() as task:
                await conn.play_turn(-1)
                await conn.play_turn(-1)
                await conn.play_turn(-1)
                await conn.play_turn(-1)
                await asyncio.sleep(5)
            logger.info("Exiting receive loop") # This line is not reached
        logger.info("Disconnecting websocket")
