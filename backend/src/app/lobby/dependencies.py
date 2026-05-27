from typing import Protocol
import asyncio
import logging
import json
import random
from random import Random

from fastapi import Depends, BackgroundTasks, status, Form, Request
from fastapi.exceptions import HTTPException
from fastapi.websockets import WebSocket, WebSocketDisconnect
from pesten.pesten import Pesten, card
from pesten.lobby import Lobby, NullConnection, AIConnection, Player, ConnectionDisconnect

from .schemas import LobbyCreate


logger = logging.getLogger('uvicorn.error')


def construct_rules(lobby_create: LobbyCreate = Form()):
    rules = {}
    if lobby_create.two:
        rules[0] = lobby_create.two

    if lobby_create.three:
        rules[1] = lobby_create.three

    if lobby_create.four:
        rules[2] = lobby_create.four

    if lobby_create.five:
        rules[3] = lobby_create.five

    if lobby_create.six:
        rules[4] = lobby_create.six

    if lobby_create.seven:
        rules[5] = lobby_create.seven

    if lobby_create.eight:
        rules[6] = lobby_create.eight

    if lobby_create.nine:
        rules[7] = lobby_create.nine

    if lobby_create.ten:
        rules[8] = lobby_create.ten

    if lobby_create.jack:
        rules[9] = lobby_create.jack

    if lobby_create.queen:
        rules[10] = lobby_create.queen

    if lobby_create.king:
        rules[11] = lobby_create.king

    if lobby_create.ace:
        rules[12] = lobby_create.ace
    
    if lobby_create.joker:
        rules[77] = lobby_create.joker
        rules[78] = lobby_create.joker

    return rules


class HumanConnection:
    def __init__(self, websocket: WebSocket, username):
        self.username = username
        self.websocket = websocket

    async def accept(self):
        await self.websocket.accept()

    async def close(self):
        try:
            logger.info("Closing websocket")
            await self.websocket.close()
        except RuntimeError:
            logger.error("Some runtime error")

    async def send_json(self, data):
        try:
            await self.websocket.send_json(data)
            logger.info("Sended data to client")
        except WebSocketDisconnect as e:
            raise ConnectionDisconnect(e)
        # except RuntimeError:
        #     pass

    async def receive_text(self) -> str:
        try:
            return await self.websocket.receive_text()
        except WebSocketDisconnect as e:
            raise ConnectionDisconnect from e


def get_randomizer(request: Request):
    return request.app.state.rng


def create_game(
        lobby_create: LobbyCreate = Form(),
        rules = Depends(construct_rules),
        rng: Random = Depends(get_randomizer)
):
    cards = [card(suit, value) for suit in range(4) for value in range(13)]
    jokers = [77, 78]
    for i in range(lobby_create.jokerCount):
        cards.append(jokers[i%2])
    rng.shuffle(cards)
    game = Pesten(lobby_create.size, 8, cards, rules)
    return game

tasks = set()
class Lobbies:
    def __init__(
            self,
            request: Request,
            # lobby_create: LobbyCreate,
            # user: str = Depends(get_current_user),
    ):
        self.lobbies = request.state.lobbies
        # self.user = lobby_create.creator

    def get_lobbies(self):
        return self.lobbies

    def get_lobby(self, lobby_name):
        return self.lobbies[lobby_name]

    async def create_lobby(self, lobby_create: LobbyCreate, game: Pesten):
        user = lobby_create.creator
        lobby_name = lobby_create.name
        ai_count = lobby_create.aiCount
        if lobby_name in self.lobbies:
            raise HTTPException(status_code=400, detail="Lobby name already exists")        
        lobby = Lobby(game, user)
        await lobby.connect(Player(user, NullConnection()))
        self.lobbies[lobby_name] = lobby
        for i in range(ai_count):
            connection = AIConnection(lobby.game, i+1)
            task = asyncio.create_task(lobby.connect(Player(f'AI{i+1}', connection)), name=f"{lobby_name}-AI-{i+1}")
            tasks.add(task) # Make sure task is not garbage collected
            task.add_done_callback(tasks.discard)
        logger.info(f"New game created: {lobby_name}")
        return lobby

    async def delete_lobby(self, lobby_create: LobbyCreate):
        user = lobby_create.creator
        
        try:
            lobby_to_be_deleted = self.lobbies.pop(lobby_name)
        except KeyError as e:
            logger.error(f'Lobby with name of {e} does not exist')
            raise HTTPException(status.HTTP_404_NOT_FOUND, "This lobby does not exists")
        if lobby_to_be_deleted.players[0].name != user:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "This lobby does not belong to you")

        for player in lobby_to_be_deleted.players:
            await player.connection.close()

        return lobby_to_be_deleted
        