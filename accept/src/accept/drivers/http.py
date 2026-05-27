import json
from urllib.parse import quote
from time import sleep
from threading import Thread

from websockets.sync.client import connect, ClientConnection
from websockets.exceptions import ConnectionClosed
from httpx import Client

from app.exceptions import NameAlreadyTakenError, GameNotStartedError
from app.lobby.schemas import LobbyResponse

from accept.driver import Connection, Driver


class WebsocketConnection(Connection):
    def __init__(self, ws: ClientConnection, username: str, lobby: LobbyResponse) -> None:
        self._ws = ws
        self.t = Thread(target=self._listen)
        self._is_listening = False
        self._exception = None
        self._username = username
        self.lobby = lobby
        self._last_board: dict | None = None

    def _listen(self):
        try:
            while self._is_listening:
                data = json.loads(self._ws.recv())
                if 'topcard' in data:
                    self._last_board = data
                if "error" in data:
                    if data['error'] == "Game not started":
                        self._exception = GameNotStartedError()
        except ConnectionClosed:
            pass


    def __enter__(self) -> Connection:
        self._ws.__enter__()
        self._is_listening = True
        self.t.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self._is_listening = False
        self.t.join(0.5)
        self._ws.__exit__(exc_type, exc, tb)
    
    def play_card(self, i: int):
        self._ws.send(str(i))
        sleep(0.1)
        if self._exception:
            try:
                raise self._exception
            except Exception as e:
                raise e
            finally:
                self._exception = None



class HttpDriver(Driver):
    def __init__(self, client: Client) -> None:
        self.client = client

    def home(self):
        from accept.screens.http import HttpHomeScreen
        return HttpHomeScreen(self)
    
    def create_and_join_lobby(self, config: dict) -> LobbyResponse:
        response = self.client.post("/lobbies", json=config)
        lobby = LobbyResponse.model_validate(response.json())
        self.join_lobby(lobby, config['creator'])
        assert response.status_code == 200, response.text
        return lobby
    
    def get_lobbies(self) -> list[LobbyResponse]:
        response = self.client.get("/lobbies")
        assert response.status_code == 200, response.text
        return [LobbyResponse.model_validate(l) for l in response.json()]

    def join_lobby(self, lobby: LobbyResponse, username) -> Connection:
        response = self.client.post(f"/lobbies/{lobby.id}/join", json={
            "username": username
        })
        if response.status_code == 409:
            raise NameAlreadyTakenError()
        assert response.status_code == 200, response.text
        # Token is set in cookies
        token = self.client.cookies.get("sessionToken")
        ws = connect(
            f"ws://localhost:8000/lobbies/{quote(lobby.id)}/connect",
            additional_headers={"Cookie": f"sessionToken={token}"}
        )

        return WebsocketConnection(ws, username, lobby)
