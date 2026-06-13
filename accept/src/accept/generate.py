from random import Random

from backend.lobby.dependencies import create_game
from backend.lobby.schemas import LobbyCreate

from pesten.agent import Agent


def generate_chooses(lobby_create: LobbyCreate, seed: int):
    game = create_game(lobby_create, {}, Random(seed))
    agents = [
        Agent(0),
        Agent(1),
    ]
    i = 0
    chooses = []
    while not game.has_won:
        agent = agents[i]
        choose = agent.generate_choose(game)
        agent.play_turn(game)
        chooses.append(choose)
        i += 1
        i %= len(agents)
    return chooses
    