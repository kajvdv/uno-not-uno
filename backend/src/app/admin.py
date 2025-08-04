import pickle

from fastapi import FastAPI, Depends, HTTPException, APIRouter, Form, File, Request
from fastapi.responses import Response

from app.auth import get_current_user, get_token
from app.lobby.dependencies import Lobbies
from app.lobby.routes import get_lobbies_create_parameters
from app.lobby.schemas import LobbyCreate
from pesten.lobby import AIConnection


def get_current_admin(user = Depends(get_current_user)):
    if user != 'admin':
        raise HTTPException(401, "Not an admin")
    return user


router = APIRouter(dependencies=[Depends(get_current_admin)])


@router.get("/logs/{lobby_name}")
def get_game_logs(lobby_name, request: Request):
    lobbies = request.state['lobbies']
    lobby = lobbies.get(lobby_name, None)
    if not lobby:
        raise HTTPException(404, "Lobby does not exists")
    return [[lobby.players[chair].name, message] for chair, message in lobby.game.logs]

@router.get("/game/{lobby_name}")
def get_game_pickle(
    lobby_name,
    request: Request,
    # lobbies: dict[str, Lobby] = Depends(get_lobbies),
    # lobbies_create_parameters = Depends(get_lobbies_create_parameters)
):
    lobbies = request.state.lobbies
    lobbies_create_parameters = request.state.lobbies_create_parameters
    lobby = lobbies.get(lobby_name, None)
    game = lobby.game
    creator = lobby.creator
    chooses = lobby.chooses
    player_names = [p.name for p in lobby.players]
    lobby_create = lobbies_create_parameters[lobby_name]
    ai_count = len([player.connection for player in lobby.players if type(player.connection) == AIConnection])
    data = pickle.dumps([game, creator, player_names, chooses, ai_count, lobby_create])
    return Response(data)
    

@router.post("/game")
async def add_game(
    request: Request,
    lobby_name = Form(),
    ai_count = Form(0),
    file = File(),
    lobbies_crud: Lobbies = Depends(),
):
    lobbies_create_parameters = request.state.lobbies_create_parameters
    user = 'admin'
    game = pickle.loads(await file.read())
    aiCount = int(ai_count)
    await lobbies_crud.create_lobby(lobby_name, aiCount, game)
    lobbies_create_parameters[lobby_name] = LobbyCreate(name=lobby_name, size=game.player_count, aiCount=ai_count)
    return {
        'id': lobby_name,
        'size': 1 + aiCount,
        'capacity': game.player_count,
        'creator': user,
        'players': [user],
    }

@router.post('/game/connect-ai')
def connect_ai_to_game():
    #TODO implement. Connect an ai to a game at any moment if there is capacity.
    ...

# @router.delete('/game/reset')
# def reset_games(
#     lobbies: dict[str, Lobby] = Depends(get_lobbies)
# ):
#     while lobbies:
#         lobbies.popitem()
