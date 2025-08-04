"""The player connects to a game using websockets. 
Every websockets represents a player, so every game has multiple websocket connections.
Players can create new games using the post endpoint, to which they can connect using a websocket.

"""
import os
from pathlib import Path
import logging
import asyncio
import pickle
import random
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, Depends
from fastapi.responses import RedirectResponse, PlainTextResponse

from app.lobby.routes import router as router_lobby, lobbies_create_parameters
from app.auth import router as router_auth, ExpiredSignatureError
from app.admin import router as router_admin
from app.reload import Reloader


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("startup")
    lobbies_dir = os.environ['LOBBIES_DIR']
    lobbies = {}
    lobbies_create_parameters = {}
    reloader = Reloader(lobbies_dir, lobbies_create_parameters)
    logger.info('Loading lobbies from previous server process')
    await reloader.load_lobbies(lobbies)
    yield {
        'lobbies': lobbies,
        'lobbies_create_parameters': lobbies_create_parameters
    }
    print("shutdown")
    logger.info('Saving lobbies for next server process')
    reloader.save_lobbies(lobbies)

    # Save the lobbies on exit. Load them back via the admin endpoints whenever after the server startsup.
    # The owner of the lobby can connect AI's they want.
    # save_lobbies(lobbies, lobbies_create_parameters)


app = FastAPI(lifespan=lifespan)
# Secure endpoints with Depends(get_current_user)
app.include_router(router_auth)
app.include_router(
    router_lobby,
    prefix='/lobbies',
)
app.include_router(router_admin, prefix='/admin')

@app.exception_handler(ExpiredSignatureError)
def handle_expired_auth(request, exc):
    return PlainTextResponse("Unauthorized", status_code=401)


@app.get('/tasks')
async def get_tasks():
    tasks = asyncio.all_tasks()
    for task in tasks:
        print(task.get_name(), task.get_coro())


from pesten.lobby import Player
from app.lobby.dependencies import Lobbies, HumanConnection
@app.websocket("/ws")
async def connect_to_lobby(
        lobby_name: str,
        websocket: WebSocket,
        connection: HumanConnection = Depends(),
):
    print("connected with websocket route")
    lobbies = websocket.state.lobbies
    try:
        lobby = lobbies[lobby_name]
    except KeyError as e:
        logger.error(f"Could not find {lobby_name} in lobbies")
        logger.error(f"Current lobbies: {lobbies}")
        return
    player = Player(connection.username, connection)
    logger.info(f"Connecting {connection.username} to {lobby_name}")
    await lobby.connect(player)

@app.websocket('/other')
async def other_connection(ws: WebSocket):
    print("connected to websocket")