from contextlib import contextmanager
import logging
import pickle
from io import BytesIO
from threading import Thread

from sqlalchemy import create_engine, StaticPool
from httpx import AsyncClient, ASGITransport
from httpx_ws import aconnect_ws, AsyncWebSocketSession


logger = logging.getLogger(__name__)

def create_db_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={
            'check_same_thread': False
        },
        poolclass=StaticPool
    )
    return engine


class GameConnection:
    def __init__(self, endpoint, base_url):
        self.connection = None
        self.board = None
        self.thread: Thread = None
        self.run = False
        self.endpoint = endpoint
        self.base_url = base_url

    async def __aenter__(self):
        import httpx
        from httpx_ws.transport import ASGIWebSocketTransport
        from app.main import app
        # async with  as ws_client:
        self.ws_client = httpx.AsyncClient(transport=ASGIWebSocketTransport(app), base_url="http://testserver")
        c = await self.ws_client.__aenter__()
        self.connection = aconnect_ws(self.endpoint, c)
        self.connection = await self.connection.__aenter__()
        # self.board = self.connection
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.connection.__aexit__()
        c = await self.ws_client.__aexit__(*args, **kwargs)
        return self

    def play_turn(self, choose):
        self.connection.send_text(str(choose))
        return self.connection.receive_json()
    
    # def start_receiving(self):
    #     def receive():
    #         print("Start receiving messages")
    #         while self.run: #TODO make wait on game won message
    #             data = self.connection.receive_json()
    #             print(data)
    #     self.thread = Thread(target=receive)
    #     self.run = True
    #     self.thread.start()
    #     print("Thread started")
    #     assert 0
        

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
        endpoint = f'/ws?lobby_name={lobby_name}&token={token}'
        url = str(self.base_url) + endpoint
        url = '/other'
        # url = "ws://test/lobbies/connect"
        logger.info(f"Websocket connect to {url}")
        # connection = aconnect_ws(url.replace('http', 'ws'), self)
        return GameConnection(endpoint)

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
        response = self.client.get(f'/admin/game/{lobby_name}')
        return response
    
    # async def register_user(self, username, password):
    #     from app.main import app
    #     async with AsyncClient(
    #         transport=ASGITransport(app=app), base_url="http://test"
    #     ) as client:
    #         response = await client.post('/register', data={
    #             "username": username,
    #             "password": password
    #         })
    #         return response

    # def reset_lobbies(self):
    #     response = self.client.delete(f'/admin/game/reset')
    #     return response
