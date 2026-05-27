from time import sleep
from pathlib import Path

import pytest
from httpx import Client

from app.exceptions import NameAlreadyTakenError, GameNotStartedError
from app.lobby.schemas import LobbyCreate

from accept.generate import generate_chooses
from accept.driver import Driver
from accept.drivers.http import HttpDriver
from accept.drivers.selenium import SeleniumDriver


def get_testgame_config():
    return {
        "name": "test game",
        "size": 2,
        "creator": "player 1"
    }
    

@pytest.fixture
def client():
    return Client(base_url="http://localhost:8000")


@pytest.fixture(autouse=True)
def reload_server():
    import app
    yield
    Path(app.__file__).touch()
    sleep(1)


@pytest.fixture(params=[
    pytest.param("http", marks=[pytest.mark.http]),
    pytest.param("selenium", marks=[pytest.mark.selenium])
])
def driver(request):
    driver_name = request.param
    if driver_name == "http":
        return HttpDriver(Client(base_url="http://localhost:8000")) 
    elif driver_name == "selenium":
        return SeleniumDriver()
    else:
        raise Exception(f"No driver for {driver_name}")


@pytest.fixture(params=[
    pytest.param("http", marks=[pytest.mark.http]),
    pytest.param("selenium", marks=[pytest.mark.selenium])
])
def drivers(request):
    driver_name = request.param
    if driver_name == "http":
        return [
            HttpDriver(Client(base_url="http://localhost:8000")),
            HttpDriver(Client(base_url="http://localhost:8000")),
        ]
    elif driver_name == "selenium":
        return [
            SeleniumDriver(),
            SeleniumDriver(),
        ]
    else:
        raise Exception(f"No driver for {driver_name}")
    

def test_main_happy_path(driver, chooses):
    p1_homescreen = driver.home()
    p2_homescreen = driver.home()

    p1_lobby_screen = p1_homescreen.create_game(size=2, username="player 1")
    p2_lobby_screen = p2_homescreen.join_game(p1_lobby_screen.code, username="player 2")

    p1_game_screen = p1_lobby_screen.wait_for_game()
    p2_game_screen = p2_lobby_screen.wait_for_game()

    game_screens = {
        "player 1": p1_game_screen,
        "player 2": p2_game_screen,
    }

    for i in chooses:
        game_screens[p1_game_screen.current_player].play_card(i)

    assert p1_game_screen.winner == "player 2"
    assert p2_game_screen.winner == "player 2"
    assert p1_homescreen == p1_game_screen.exit()
    assert p2_homescreen == p2_game_screen.exit()
