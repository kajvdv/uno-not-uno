from pathlib import Path
import os
import pickle

from fastapi import Request

from pesten.lobby import AIConnection

from app.lobby.dependencies import Lobbies, Player, NullConnection
from app.lobby.routes import create_lobby_route


# lobbies_dir = Path.cwd() / os.environ.get('LOBBIES_DIR', 'data/lobbies')

def save_lobbies(lobbies_dir, lobbies, lobbies_create_parameters, delete_old=False):
    lobbies_dir.mkdir(parents=True, exist_ok=True)
    if delete_old:
        for file in lobbies_dir.iterdir():
            file.unlink()
    for name, lobby in lobbies.items():
        path = lobbies_dir / f'{name}.pickle'
        game = lobby.game
        creator = lobby.creator
        chooses = lobby.chooses
        player_names = [p.name for p in lobby.players]
        lobby_create = lobbies_create_parameters[name]
        ai_count = len([player.connection for player in lobby.players if type(player.connection) == AIConnection])
        with open(path, 'wb') as file:
            pickle.dump([game, creator, player_names, chooses, ai_count, lobby_create], file)

async def load_lobbies(lobbies_dir, lobbies, lobbies_create_parameters):
    if not lobbies_dir.exists():
        return
    for lobby_path in lobbies_dir.iterdir():
        with open(lobby_path, 'rb') as file:
            game, creator, player_names, chooses, ai_count, lobby_create = pickle.load(file)
        # await lobbies_crud.create_lobby(lobby_path.stem, ai_count, game)
        request = Request({
            'type': 'http',
            'state': {
                'lobbies': lobbies,
                'lobbies_create_parameters': lobbies_create_parameters,
            }
        })
        lobbies_crud = Lobbies(request, creator)
        await create_lobby_route(
            request,
            lobby_create,
            creator,
            lobbies_crud,
            game,
        )
        lobby = lobbies[lobby_create.name]
        lobby.chooses = chooses
        for name in player_names:
            # This might seem that these NullConnections will override the AIConnections established in create_lobby_route.
            # However, the connect function of the AIConnection created in create_lobby_route will execute AFTER this coroutine is finished.
            # These AIConnections will then override these NullConnections and thus putting things back to normal
            await lobby.connect(Player(name, NullConnection()))



class Reloader:
    def __init__(self, dir: Path, create_params):
        dir = Path(dir)
        if not dir.exists():
            dir.mkdir(parents=True)
        self.dir = dir
        self.create_params = create_params
    
    async def load_lobbies(self, lobbies):
        await load_lobbies(self.dir, lobbies, self.create_params)

    def save_lobbies(self, lobbies):
        save_lobbies(self.dir, lobbies, self.create_params)
