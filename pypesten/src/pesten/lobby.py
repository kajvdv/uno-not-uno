import asyncio
import logging
from typing import Protocol
import json

from pesten.pesten import Pesten, CannotDraw, EndWithSpecialCard, card_object
from pesten.agent import Agent, AgentError

logger = logging.getLogger(__name__)


class ConnectionDisconnect(Exception):
    ...


class ClosingConnection(Exception):
    """This exception will prevent a NullConnection to get stuck in its gameloop inside Lobby.connect"""
    ...


class Connection(Protocol):
    async def accept(self): ...
    async def close(self): ...
    async def send_json(self, data): ...
    async def receive_text(self) -> str: ...


class NullConnection:
    async def accept(self): ...

    async def close(self): ...

    async def send_json(self, data): ...

    async def receive_text(self) -> str:
        raise ClosingConnection("Null connection closing")
        

class AIConnection():
    def __init__(self, game: Pesten, player_index, delay = 1): # Resolve player_index automatically
        self.game = game
        self.agent = Agent(player_index)
        self.event = asyncio.Event()
        self.delay = delay
        self.messages = []
        self.exit = False

    async def accept(self):
        ...
    
    async def close(self):
        self.event.set() # makes it raise exception in receive_text method to stop loop
        self.exit = True
    
    async def send_json(self, data: dict):
        # This function can trigger the event when it detects that its this AI its turn
        # logger.debug(f"Received for {self.agent.player_index} : \n{json.dumps(data, indent=2)}")
        if 'error' in data:
            return
        if self.game.current_player == self.agent.player_index or self.game.has_won:
            # if len(self.messages) < 3:
            #     self.messages.append(data)
            # else:
            #     if all([msg["current_player"] == data["current_player"] for msg in self.messages]):
            #         raise Exception("AI is getting stuck")
            #     self.messages = []
            self.event.set()

    
    async def receive_text(self) -> str:
        await self.event.wait() # Would be nice to get rid of this for not using create_tasks
        self.event.clear()
        if self.exit:
            raise ClosingConnection("Closing AI after exit")
        choose = self.agent.generate_choose(self.game)
        await asyncio.sleep(self.delay)
        return choose


class Player:
    # Structure holding player information 
    def __init__(self, name, connection: Connection):
        self.name = name
        self.connection = connection


class Lobby:
    def __init__(self, game: Pesten, creator) -> None:
        self.game = game
        self.creator = creator
        self.started = False
        self.capacity = game.player_count
        self.players: list[Player] = [] # List corresponds with players in pesten game
        self.chooses = []
        self.run = True

    async def connect(self, new_player: Player):
        name = new_player.name
        # Creates a gameloop for a connection
        if player := self.get_player_by_name(name):
            index = self.players.index(player)
            self.players[index] = new_player # Replacing the player object
        elif self.started:
            raise Exception("Lobby is full")
        else:
            self.players.append(new_player)
        if len(self.players) == self.capacity:
            self.started = True
        await new_player.connection.accept() # Accept as late as possible
        connection = new_player.connection
        await self.update_boards(message=f"{name} joined the game")
        # break-statements only make sure that the current connection stops
        while self.run:
            try:
                logger.info(f"Waiting for choose of {name}")
                choose = await connection.receive_text()
                logger.info(f"Choose received from {name}. Choose: {choose}")
                await self.play_choose(new_player, choose)
                self.run = not self.game.has_won # Stop all connections if game was won
            except CannotDraw as e:
                await new_player.connection.send_json({"error": "Cannot draw, you have to play a card"})
            except EndWithSpecialCard as e:
                logger.error("Player tried to end with special card")
                await new_player.connection.send_json({"error": "Cannot end with special card"})
            except ClosingConnection as e:
                logger.info("Closing connection")
                break
            except ConnectionDisconnect as e:
                logger.info("Connection disconnected")
                break

    async def update_boards(self, message=""):
        for player_id, player in enumerate(self.players):
            try:
                send_coro = player.connection.send_json({
                    "topcard": card_object(self.game.play_stack[-1]),
                    "previous_topcard": card_object(self.game.play_stack[-2]) if len(self.game.play_stack) > 1 else None,
                    "can_draw": bool(self.game.draw_stack),
                    "choose_suit": self.game.asking_suit,
                    "draw_count": self.game.draw_count,
                    "current_player": self.players[self.game.current_player].name,
                    "otherPlayers": {
                        self.players[i].name
                        if i < len(self.players)else "": 
                        len(self.game.hands[i])
                        if i < len(self.players) else 0
                        for i in range(self.capacity)
                    },
                    "hand": [card_object(card) for card in self.game.hands[player_id]],
                    "message": message
                })
                logger.debug(f"Updating {self.players[self.game.current_player].name}'s board")
                await send_coro
            except IndexError:
                # the amount of players should be at least the same as the current player index
                # Fix by having a NullConnection for every inital player
                continue

    def get_player_by_name(self, name: str) -> Player:
        try:
            player = next(filter(lambda p: p.name == name, self.players))
        except StopIteration as e:
            return None
        return player
        
    async def play_choose(self, player: Player, choose):
        # player = self.get_player_by_name(name)
        logger.info("Playing choose")
        name = player.name
        if not self.started:
            logger.info("Game not started")
            await player.connection.send_json({"error": "Game not started"})
            return
        player_index = [p.name for p in self.players].index(name)
        if self.game.current_player != player_index:
            logger.info("Not your turn")
            await player.connection.send_json({"error": "Not your turn"})
            return
        try:
            choose = int(choose)
        except ValueError:
            logger.info("Invalid choose")
            await player.connection.send_json({"error": "Invalid choose"})
            return
        log_count_before = len(self.game.logs)
        self.chooses.append(choose)
        self.game.play_turn(choose)
        if len(self.game.logs) != log_count_before:
            message = self.game.logs[-1][1]
        else:
            message = ""
        if self.game.has_won:
            await self.update_boards(f"{name} has won the game!")
        else:
            await self.update_boards(message=message)