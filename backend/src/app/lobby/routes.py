# TODO: Have a player be replaced by an AI if they don't join back on time
import logging

from fastapi import APIRouter, Depends, Form, Request, WebSocket


from app.auth import get_current_user
from pesten.lobby import Player
from .schemas import LobbyCreate, LobbyResponse, Card
from .dependencies import Lobbies, HumanConnection, create_game


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('', response_model=list[LobbyResponse])
async def get_lobbies(lobbies_crud: Lobbies = Depends()):
    lobbies = lobbies_crud.get_lobbies()
    return sorted([{
        'id': id,
        'size': len(lobby.players),
        'capacity': lobby.capacity,
        'creator': lobby.creator,
        'players': list(map(lambda p: p.name, lobby.players)),
    } for id, lobby in lobbies.items() if not lobby.game.has_won], key=lambda lobby: lobby['creator'] != lobbies_crud.user)


lobbies_create_parameters: dict[str, LobbyCreate] = {}
def get_lobbies_create_parameters():
    return lobbies_create_parameters

@router.post('', response_model=LobbyResponse)
async def create_lobby_route(
        request: Request,
        lobby_create: LobbyCreate = Form(),
        user: str = Depends(get_current_user),
        lobbies_crud: Lobbies = Depends(),
        game = Depends(create_game),
        # lobbies_create_parameters = Depends(get_lobbies_create_parameters)
):
    await lobbies_crud.create_lobby(lobby_create.name, lobby_create.aiCount, game)
    # Save config to restore lobby on startup
    request.state.lobbies_create_parameters[lobby_create.name] = lobby_create
    return {
        'id': lobby_create.name,
        'size': 1 + lobby_create.aiCount,
        'capacity': lobby_create.size,
        'creator': user,
        'players': [user],
    }


@router.delete('/{id}', response_model=LobbyResponse)
async def delete_lobby(
        id: str,
        lobbies_crud: Lobbies = Depends(),
):
    lobby = await lobbies_crud.delete_lobby(id)
    return {
        'id': id,
        'size': len(lobby.players),
        'capacity': lobby.capacity,
        'creator': lobbies_crud.user,
        'players': [p.name for p in lobby.players],
    }


@router.get('/{lobby_id}/rules')
def get_lobby_rules(lobby_id, request: Request):
    lobbies = request.state.lobbies
    lobby = lobbies[lobby_id]
    assert lobby
    return {Card.from_int(value).value: rule for value, rule in lobby.game.rules.items()}


@router.websocket("/connect")
async def connect_to_lobby(
        lobby_name: str,
        websocket: WebSocket,
        connection: HumanConnection = Depends(),
):
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
