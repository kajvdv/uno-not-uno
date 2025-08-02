from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import Session

engine = create_engine(
    "sqlite://",
    connect_args={
        'check_same_thread': False
    },
    poolclass=StaticPool
)

def get_db_override():
    with Session(engine) as db:
        yield db


app.dependency_overrides[get_db] = get_db_override
# app.debug = True
client = TestClient(app)

def test_app():
    response = client.get("/lobbies")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 0
    
    lobby_name = "test_lobby"
    response = client.post('/lobbies', data={
        'name': lobby_name,
        "size": 2,
    })
    assert response.status_code == 200, response.text

    response = client.get("/lobbies")
    assert response.status_code == 200, response.text
    assert len(response.json()) == 1

    connections = [
        client.websocket_connect(f'/lobbies/connect?lobby_name={lobby_name}&player_id=testplayer1'),
        client.websocket_connect(f'/lobbies/connect?lobby_name={lobby_name}&player_id=testplayer2')
    ]
    with connections[0], connections[1]:
        # Messages first join
        board = connections[0].receive_json()
        # Message second join
        board = connections[0].receive_json()
        board = connections[1].receive_json()
        connections[0].send_text('0')

    