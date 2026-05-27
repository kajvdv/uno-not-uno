import pytest

from sqlalchemy.orm import Session

from app.client import Client


@pytest.mark.anyio
async def test_registering_user(client: Client, db: Session):
    from app.auth import User
    response = await client.register('user', 'password')
    assert response.status_code == 204
    user = db.get(User, 'user')
    assert user


@pytest.mark.anyio
async def test_login_user(client: Client, db: Session):
    from app.auth import User, hash_password
    db.add(User(
        username='user',
        password=hash_password('password'),
    ))
    response = await client.login('user', 'password')
    assert response.status_code == 200
    assert response.json()['access_token']