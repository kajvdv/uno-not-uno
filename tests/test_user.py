import pickle
from pathlib import Path
import sys
import time
import subprocess
from io import BytesIO
import pytest
import urllib.parse

from dotenv import load_dotenv
load_dotenv()

import requests
from requests import Session
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from bot.bot import Bot
from pesten.pesten import Pesten, card
from pesten.agent import Agent
from app.auth import generate_access_token



class Client(requests.Session):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    #     engine = create_db_engine()
    #     Base.metadata.create_all(engine)
    #     self.engine = engine
    #     app.dependency_overrides[get_db] = self.get_db

    def get_db(self):
        with Session(self.engine) as db:
            yield db

    def __enter__(self):
        return super().__enter__()
    
    def __exit__(self, *args):
        return super().__exit__(*args)

    def reset(self):
        ...
        # for db in get_db_override():
        #     yield db
    
    # def drop_tables(self):
    #     Base.metadata.drop_all(self.engine)

    def register(self, username, password):
        response = self.post('/register', data={
            "username": username,
            "password": password
        })
        return response
    
    def login(self, username, password):
        response = self.post('http://localhost:5173/api/token', data={
            "username": username,
            "password": password
        })
        data = response.json()
        self.headers['Authorization'] = f"Bearer {data['access_token']}"
        return response
    
    def get_lobbies(self):
        response = self.get('/lobbies')
        return response

    def create_lobby(self, **kwars):
        response = self.post('/lobbies', data=kwars)
        return response


    # def connect_game(self, lobby_name, token):
    #     connection = self.websocket_connect(f'/lobbies/connect?lobby_name={lobby_name}&token={token}')
    #     return TestConnection(connection)

    def add_game(self, game, lobby_name):
        file = BytesIO()
        pickle.dump(game, file)
        data = {
            'lobby_name': lobby_name,
            'size': game.player_count
        }
        file.seek(0)
        response = self.post('http://localhost:5173/api/admin/game', data=data, files={
            'file': file.read()
        })
        return response

    def get_game(self, lobby_name):
        response = self.get(f'/admin/game/{lobby_name}')
        return response
    
    def reset_lobbies(self):
        response = self.delete(f'http://localhost:5173/api/admin/game/reset')
        return response



@pytest.fixture
def browser(ports):
    sys.path.append(str(Path("C:/Program Files/Google/Chrome/Application")))
    
    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    user_data_dir = r"C:\Selenium\ChromeProfile"
    
    # Start Chrome using Popen
    processes = [
        subprocess.Popen([
            chrome_path,
            f"--remote-debugging-port={port}",
            f'--user-data-dir={user_data_dir}-{i}'
        ])
        for i, port in enumerate(ports)
    ]
    yield
    for p in processes:
        p.terminate()
        p.wait()

@pytest.fixture
def game():
    cards = [card(suit, value) for suit in range(4) for value in range(13)]
    game = Pesten(2, 8, cards)
    client = Client()
    name = 'auto test lobby'
    with client:
        client.login('admin', 'admin')
        client.reset_lobbies()
        resposnse = client.add_game(game, name)
    return name


@pytest.mark.parametrize('ports', [(9222, 9223,),])
def test_open_chrome(browser, ports, game):
    # print(zip(*ports, [
    #     ('admin', 'admin'),
    #     ('kaj', 'kaj'),
    # ]))
    # assert 0
    bots = []
    user_pws = [
        ('admin', 'admin'),
        ('kaj', 'kaj'),
    ]
    for i, port in enumerate(ports):
        user_pw = user_pws[i]
        options = Options()
        options.debugger_address = f"127.0.0.1:{port}"
        options.add_argument('--disable-search-engine-choice-screen')
        options.add_argument('--hide-crash-restore-bubble')
        options.add_argument('--disable-session-crashed-bubble')
        options.add_argument('--credentials_enable_service')
        options.add_argument('--incognito')
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)
        
        bots.append(Bot(options=options))

    for i, bot in enumerate(bots):
        # bot.get('http://localhost:5173/')
        bot.get(f'http://localhost:5173/game?lobby_id={urllib.parse.quote(game)}')
        user = user_pws[i][0]
        print(user)
        value = generate_access_token(user)
        bot.execute_script(f"window.sessionStorage.setItem('accessToken', '{value}');")
        bot.get(f'http://localhost:5173/game?lobby_id={urllib.parse.quote(game)}')
    #     bot.join_lobby(game)


    while not bot.check_won():
        for bot in bots:
            bot.wait_until_turn()
            bot.play_card()

    bot.go_back_to_lobbies()
        
    time.sleep(10)  