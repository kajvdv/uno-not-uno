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
from random import Random
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, Depends
from fastapi.responses import RedirectResponse, PlainTextResponse

from backend.lobby.routes import router as router_lobby, lobbies_create_parameters
from backend.auth import router as router_auth, ExpiredSignatureError
from backend.admin import router as router_admin
from backend.reload import Reloader


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    lobbies_dir = os.environ['LOBBIES_DIR']
    lobbies = {}
    lobbies_create_parameters = {}
    reloader = Reloader(lobbies_dir, lobbies_create_parameters)
    logger.info('Loading lobbies from previous server process')
    # await reloader.load_lobbies(lobbies)
    seed = int(os.environ["GAME_SEED"])
    app.state.rng = Random(seed)
    app.state.lobbies = lobbies
    yield {
        'lobbies': lobbies,
        'lobbies_create_parameters': lobbies_create_parameters
    }
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

