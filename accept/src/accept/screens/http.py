from time import sleep

from httpx import Client

from backend.lobby.schemas import LobbyResponse
from accept.drivers.http import HttpDriver, WebsocketConnection


class HttpHomeScreen:
    def __init__(self, driver: HttpDriver):
        # Each home screen gets its own isolated session (separate cookie jar)
        self._driver = HttpDriver(Client(base_url=str(driver.client.base_url)))

    def create_game(self, size: int, username: str) -> 'HttpLobbyScreen':
        response = self._driver.client.post("/lobbies", json={
            "name": "test game",
            "size": size,
            "creator": username,
        })
        assert response.status_code == 200, response.text
        data = response.json()
        lobby = LobbyResponse(
            id=data['id'],
            size=data['size'],
            capacity=data['capacity'],
            creator=data['creator'],
            players=data['players'],
        )
        connection = self._driver.join_lobby(lobby, username)
        connection.__enter__()
        return HttpLobbyScreen(self, connection, lobby)

    def join_game(self, code: str, username: str) -> 'HttpLobbyScreen':
        lobbies = self._driver.get_lobbies()
        lobby = next(l for l in lobbies if l.id == code)
        connection = self._driver.join_lobby(lobby, username)
        connection.__enter__()
        return HttpLobbyScreen(self, connection, lobby)

    def __eq__(self, other):
        return self is other


class HttpLobbyScreen:
    def __init__(self, home: HttpHomeScreen, connection: WebsocketConnection, lobby: LobbyResponse):
        self._home = home
        self._connection = connection
        self._lobby = lobby

    @property
    def code(self) -> str:
        return self._lobby.id

    def wait_for_game(self) -> 'HttpGameScreen':
        while True:
            board = self._connection._last_board
            if board is not None and len(board['otherPlayers']) == self._lobby.capacity - 1:
                return HttpGameScreen(self._home, self._connection)
            sleep(0.1)


class HttpGameScreen:
    def __init__(self, home: HttpHomeScreen, connection: WebsocketConnection):
        self._home = home
        self._connection = connection

    @property
    def current_player(self) -> str:
        return self._connection._last_board['current_player']

    @property
    def winner(self) -> str | None:
        board = self._connection._last_board
        if board is None:
            return None
        msg = board.get('message', '')
        if ' has won' in msg:
            return msg.split(' has won')[0]
        return None

    def play_card(self, i: int):
        self._connection.play_card(i)

    def exit(self) -> HttpHomeScreen:
        self._connection.__exit__(None, None, None)
        return self._home

    def __eq__(self, other):
        return self is other
