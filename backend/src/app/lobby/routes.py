# TODO: Have a player be replaced by an AI if they don't join back on time
import logging

from fastapi import APIRouter, Depends, Form, Request, WebSocket, Response, Body, Path, HTTPException


from app.auth import get_current_user, generate_access_token, decode_token
from pesten.lobby import Player, NullConnection
from .schemas import LobbyCreate, LobbyResponse, Card, Registration
from .dependencies import Lobbies, HumanConnection, create_game

from app.game.schemas import GamePublic


logger = logging.getLogger(__name__)
router = APIRouter()



def decode_cookie(cookies):
    content = decode_token(cookies.get("sessionToken"))
    username = content['sub']
    return username, content['lobby']


@router.get('', response_model=list[LobbyResponse])
async def get_lobbies(lobbies_crud: Lobbies = Depends()):
    lobbies = lobbies_crud.get_lobbies()
    return [{
        'id': id,
        'size': len(lobby.players),
        'capacity': lobby.capacity,
        'creator': lobby.creator,
        'players': list(map(lambda p: p.name, lobby.players)),
    }
        for id, lobby in lobbies.items()
        if not lobby.game.has_won
        and len([p for p in lobby.players
            if not isinstance(p.connection, NullConnection)
        ]) > 0
    ]


lobbies_create_parameters: dict[str, LobbyCreate] = {}
def get_lobbies_create_parameters():
    return lobbies_create_parameters


@router.get("/{lobby_id}")
def get_lobby_route(lobby_id: str, lobbies_crud: Lobbies = Depends()):
    lobby = lobbies_crud.get_lobby(lobby_id)
    return lobby



@router.post('', response_model=GamePublic)
async def create_lobby_route(
        request: Request,
        response: Response,
        lobby_create: LobbyCreate,
        # user: str = Depends(get_current_user),
        lobbies_crud: Lobbies = Depends(),
        game = Depends(create_game),
        # lobbies_create_parameters = Depends(get_lobbies_create_parameters)
):
    await lobbies_crud.create_lobby(lobby_create, game)
    # Save config to restore lobby on startup
    request.state.lobbies_create_parameters[lobby_create.name] = lobby_create
    response.set_cookie("sessionToken", generate_access_token(lobby_create.creator, lobby_create.name))
    return {
        "url": f"{request.url_for("get_lobby_route", lobby_id=lobby_create.name)}",
        'id': lobby_create.name,
        'size': 1 + lobby_create.aiCount,
        'capacity': lobby_create.size,
        'creator': lobby_create.creator,
        'players': [lobby_create.creator],
    }


@router.post("/{lobby_id}/join", response_model=Registration)
def register_user_router(
    request: Request,
    response: Response,
    lobby_id: str,
    body: dict,
    lobbies_crud: Lobbies = Depends(),
):
    username = body['username']
    lobby = lobbies_crud.get_lobby(lobby_id)
    usernames = [p.name for p in lobby.players]
    if request.cookies.get("sessionToken"):
        username_cookie, lobby_name = decode_cookie(request.cookies)
        assert lobby_name == lobby_id
        assert username_cookie == username
    elif username in usernames:
        raise HTTPException(status_code=409)
    response.set_cookie("sessionToken", generate_access_token(username, lobby_id))
    return {
        "url": str(request.url_for("connect_to_lobby", lobby_name=lobby_id))
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


@router.websocket("/{lobby_name}/connect")
async def connect_to_lobby(
        lobby_name: str,
        websocket: WebSocket,
        # connection: HumanConnection = Depends(),
):
    username, lobby_id = decode_cookie(websocket.cookies)
    # await websocket.accept()
    lobbies = websocket.state.lobbies
    try:
        lobby = lobbies[lobby_name]
    except KeyError as e:
        logger.error(f"Could not find {lobby_name} in lobbies")
        logger.error(f"Current lobbies: {lobbies}")
        return
    connection = HumanConnection(websocket, username)
    player = Player(connection.username, connection)
    logger.info(f"Connecting {connection.username} to {lobby_name}")
    await lobby.connect(player)

