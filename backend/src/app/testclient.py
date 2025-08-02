from contextlib import contextmanager
import pickle
from io import BytesIO

from fastapi import testclient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session
from app.main import app 
from app.database import Base, get_db
from starlette import testclient


def create_db_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={
            'check_same_thread': False
        },
        poolclass=StaticPool
    )
    return engine


class TestConnection:
    def __init__(self, connection):
        self.connection = connection
        self.board = None

    def __enter__(self):
        c = self.connection.__enter__()
        self.board = self.connection
        return c

    def __exit__(self, *args, **kwargs):
        c = self.connection.__exit__(*args, **kwargs)
        return c

    def play_turn(self, choose):
        self.connection.send_text(str(choose))
        return self.connection.receive_json()


class TestClient(testclient.TestClient):
    def __init__(self, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        engine = create_db_engine()
        Base.metadata.create_all(engine)
        self.engine = engine
        app.dependency_overrides[get_db] = self.get_db

    def get_db(self):
        with Session(self.engine) as db:
            yield db

    def reset(self):
        ...
        # for db in get_db_override():
        #     yield db
    
    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

    def register(self, username, password):
        response = self.post('/register', data={
            "username": username,
            "password": password
        })
        return response
    
    def login(self, username, password):
        response = self.post('/token', data={
            "username": username,
            "password": password
        })
        data = response.json()
        self.headers['Authorization'] = f"Bearer {data['access_token']}"
        return response
    
    def get_lobbies(self):
        response = self.get('/lobbies')
        return response

    def create_lobby(self, **kwars):
        response = self.post('/lobbies', data=kwars)
        return response


    def connect_game(self, lobby_name, token):
        connection = self.websocket_connect(f'/lobbies/connect?lobby_name={lobby_name}&token={token}')
        return TestConnection(connection)

    def add_game(self, game, lobby_name):
        file = BytesIO()
        pickle.dump(game, file)
        data = {
            'lobby_name': lobby_name,
            'size': game.player_count
        }
        response = self.post('/admin/game', data=data, files={
            'file': file
        })
        return response

    def get_game(self, lobby_name):
        response = self.get(f'/admin/game/{lobby_name}')
        return response
