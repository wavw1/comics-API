from app.crud import get_user_by_username
from app.crud import create_user
from app.utils.utils import random_user
import pytest

@pytest.mark.asyncio(loop_scope="session")
async def test_register_user(db_session, client) -> None:
    user_in = random_user()

    r = await client.post(
        "/auth/register/",
        json=user_in.model_dump()
    )

    user_in_db = await get_user_by_username(
         session=db_session, 
         username=user_in.username,
         )

    assert r.status_code == 201
    assert user_in_db is not None
    assert user_in.username == user_in_db.username

@pytest.mark.asyncio(loop_scope="session")
async def test_register_incorrect_password_user(db_session, client) -> None:
    user_in = random_user()
    user_in.password = "short"
    
    r = await client.post(
        "/auth/register/",
        json=user_in.model_dump()
    )

    assert r.status_code == 400
    assert r.json() == {"detail": "Password must be at least 8 characters long"}

@pytest.mark.asyncio(loop_scope="session")
async def test_register_incorrect_email_user(db_session, client) -> None:
    user_in = random_user()
    user_in.email = "incorrect@"
    
    r = await client.post(
        "/auth/register/",
        json=user_in.model_dump()
    )

    assert r.status_code == 400
    assert r.json() == {"detail": "Invalid user data"}

@pytest.mark.asyncio(loop_scope="session")
async def test_login_user(db_session, client) -> None:
    user_in = random_user()
    await create_user(session=db_session, user_in=user_in)
    
    login_data = {"username": user_in.username, "password": user_in.password}
    r = await client.post(
        "/auth/login/",
        json=login_data
    )

    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens["token"]