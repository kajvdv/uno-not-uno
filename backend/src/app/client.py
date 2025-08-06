from contextlib import asynccontextmanager
import logging
import pickle
from io import BytesIO
import asyncio
from anyio import ClosedResourceError
import json

from httpx import AsyncClient
from httpx_ws import aconnect_ws, AsyncWebSocketSession


logger = logging.getLogger(__name__)


class GameConnection:
    def __init__(self, connection: AsyncWebSocketSession):
        self.connection = connection
        self.websocket = None
        self.board = None
        self.run = False

    async def receive(self):
        logger.debug("Start receiving messages")
        while self.run:
            logger.info("Waiting on message")
            data = await self.ws.receive_json()
        logger.debug("Stop receiving messages")


    async def __aenter__(self):
        logger.debug("Enter GameConnection")
        self.websocket = await self.connection.__aenter__()
        self.receive_task = asyncio.create_task(self.receive())
        # self.board = self.connection
        return self

    async def __aexit__(self, *args, **kwargs):
        logger.debug("Exit GameConnection")
        self.run = False
        self.receive_task.cancel()
        await self.connection.__aexit__(*args, **kwargs)

    async def play_turn(self, choose):
        await self.websocket.send_text(str(choose))
    

class Client(AsyncClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __enter__(self):
        return self.client.__enter__()
    
    def __exit__(self, *args, **kwargs):
        return self.client.__exit__(*args, **kwargs)

    async def register(self, username, password):
        response = await self.post('/register', data={
            "username": username,
            "password": password
        })
        return response
    
    async def login(self, username, password):
        response = await self.post('/token', data={
            "username": username,
            "password": password
        })
        data = response.json()
        self.token = data['access_token']
        self.headers['Authorization'] = f"Bearer {self.token}"
        return response
    
    async def get_lobbies(self):
        response = await self.get('/lobbies')
        return response

    async def create_lobby(self, **kwars):
        response = await self.post('/lobbies', data=kwars)
        return response

    async def delete_lobby(self, name):
        response = await self.delete(f'/lobbies/{name}')
        return response

    async def get_lobby_rules(self, name):
        response = await self.get(f'/lobbies/{name}/rules')
        return response


    def connect_game(self, lobby_name, token=None):
        if not token:
            token = self.token
        endpoint = f'/lobbies/connect?lobby_name={lobby_name}&token={token}'
        url = str(self.base_url) + endpoint
        # url = "ws://test/lobbies/connect"
        logger.info(f"Websocket connect to {url}")
        connection = aconnect_ws(url, self)
        return GameConnection(connection)

    def add_game(self, game, lobby_name, ai_count, token=None):
        file = BytesIO()
        pickle.dump(game, file)
        data = {
            'lobby_name': lobby_name,
            'size': game.player_count,
            'ai_count': ai_count,
        }
        prev_value = self.client.headers.get('Authorization')
        if token:
            self.client.headers['Authorization'] = f"Bearer {token}"
        response = self.client.post('/admin/game', data=data, files={
            'file': file
        })
        if response.status_code != 200:
            logger.warning(f"Failed to add game: {response.json()}")
        if prev_value:
            self.client.headers['Authorization'] = prev_value
        return response

    def get_game(self, lobby_name):
        response = self.get(f'/admin/game/{lobby_name}')
        return response
    