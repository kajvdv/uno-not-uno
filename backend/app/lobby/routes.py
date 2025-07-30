# TODO: Structure file with all routes together and all models together and so on.
# TODO: Have a player be replaced by an AI if they don't join back on time
import logging

from fastapi import APIRouter, Depends, Form


from app.auth import get_current_user
from .schemas import LobbyCreate, LobbyResponse, Card
from .dependencies import Lobbies, Connector, HumanConnection, get_lobbies as fetch_lobbies, create_game


logger = logging.getLogger(__name__)
router = APIRouter()


@router.get('', response_model=list[LobbyResponse])
async def get_lobbies(lobbies_crud: Lobbies = Depends()):
    lobbies = lobbies_crud.get_lobbies()
    return [{
        'id': id,
        'size': len(lobby.players),
        'capacity': lobby.capacity,
        # 'creator': lobby.creator,
        'players': list(map(lambda p: p.name, lobby.players)),
    } for id, lobby in lobbies.items() if not lobby.game.has_won]


lobbies_create_parameters: dict[str, LobbyCreate] = {}
def get_lobbies_create_parameters():
    return lobbies_create_parameters

@router.post('', response_model=LobbyResponse)
async def create_lobby_route(
        lobby_create: LobbyCreate = Form(),
        lobbies_crud: Lobbies = Depends(),
        game = Depends(create_game),
        # user: str = Depends(get_current_user),
        lobbies_create_parameters = Depends(get_lobbies_create_parameters)
):
    new_lobby = await lobbies_crud.create_lobby(lobby_create.name, lobby_create.aiCount, game)
    lobbies_create_parameters[lobby_create.name] = lobby_create
    return {
        'id': lobby_create.name,
        'size': 1 + lobby_create.aiCount,
        'capacity': lobby_create.size,
        # 'creator': user,
        'players': [],
    }


# @router.delete('/{id}', response_model=LobbyResponse)
# async def delete_lobby(
#         id: str,
#         lobbies_crud: Lobbies = Depends(),
# ):
#     lobby = await lobbies_crud.delete_lobby(id)
#     return {
#         'id': id,
#         'size': len(lobby.players),
#         'capacity': lobby.capacity,
#         # 'creator': lobbies_crud.user,
#         'players': [p.name for p in lobby.players],
#     }


@router.get('/{lobby_id}/rules')
def get_lobby_rules(lobby_id, lobbies = Depends(fetch_lobbies)):
    lobby = lobbies[lobby_id]
    assert lobby
    return {Card.from_int(value).value: rule for value, rule in lobby.game.rules.items()}


@router.websocket("/connect")
async def connect_to_lobby(
        lobby_name: str,
        connection: HumanConnection = Depends(),
        connector: Connector = Depends(),
):
    await connector.connect_to_lobby(lobby_name, connection)
