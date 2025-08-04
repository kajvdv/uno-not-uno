import asyncio
import pickle
import logging
import pytest

from app.client import Client

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.anyio

@pytest.fixture(name='lobby_name')
async def lobby_fixture(client, ai_count, user):
    name = 'test_lobby'
    size = 2
    # ai_count = 0
    response = await client.create_lobby(
        name=name,
        size=size,
        aiCount=ai_count,
    )
    assert response.status_code == 200, response.json()
    return name
    

@pytest.mark.parametrize('ai_count', [0])
async def test_connect_to_game(client: Client, lobby_name, user: str):
    async with client.connect_game(lobby_name) as conn:
        async with conn.start_receiving() as task:
            # Just sending a bunch of messages.
            await conn.play_turn(-1)
            await conn.play_turn(-1)
            await conn.play_turn(-1)
            await conn.play_turn(-1)
        logger.info("Exiting receive loop") # This line is not reached
    logger.info("Disconnecting websocket")


@pytest.mark.parametrize('ai_count', [1])
async def test_play_against_ai(client, lobby_name, user):
    from pesten.agent import Agent
    player = Agent(0)
    response = await client.get_game(lobby_name)
    game, *_ = pickle.loads(response.content)
    game_conn = client.connect_game(lobby_name)
    async with game_conn as ws_client:
        while not game.has_won:
            response = await client.get_game(lobby_name)
            game, *_ = pickle.loads(response.content)
            choose = player.generate_choose(game)
            await ws_client.play_turn(choose)
            await asyncio.sleep(1.2)

        # async with conn.start_receiving() as receiver:
        #     logger.debug(f"I'm inside! {receiver}")
        #     # assert 0

        #     print(game.has_won)
        #         logger.debug("Entering while loop")
        #         await asyncio.sleep(1.2)
        # logger.info("Exiting receive loop") # This line is not reached
    logger.info("Disconnecting websocket")


async def test_two_players_play(client, lobby_name, user):
    ...
