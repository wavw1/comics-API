from app.main import app
from app.crud import create_user, get_user_by_username, get_user_by_id, update_user_by_id
from app.models import UserCreate, UserUpdate
from app.utils.utils import random_username
import pytest
from httpx import AsyncClient, ASGITransport
import json

@pytest.mark.asyncio
async def test_create_user(db_session, client) -> None:
    username = random_username(1)
    user_in = UserCreate(username=username)

    r = await client.post(
        "/user/",
        json=user_in.model_dump()
    )

    user_in_db = await get_user_by_username(
         session=db_session, 
         username=user_in.username,
         )

    assert r.status_code == 201
    assert user_in_db is not None
    assert user_in.username == user_in_db.username

@pytest.mark.asyncio
async def test_get_non_existing_user(db_session, client) -> None:
    username=random_username(1)
    user_in = UserCreate(username=username)
    await create_user(session=db_session, user_in=user_in)

    user = await get_user_by_username(
         session=db_session,
         username=user_in.username,
         )
    non_existing_id = user.id + 1
    
    r = await client.get(
        f"/user/{non_existing_id}",
    )
    print(f"response: {r.json()}")

    assert r.status_code == 404
    assert r.json() == {"detail": "User not found"}

@pytest.mark.asyncio
async def test_get_existing_user() -> None:
    user_in = UserCreate(username=random_username(1))
    await create_user(json.loads(user_in.model_dump_json()))
    
    user = await get_user_by_username(user_in.username)
    user_id = user.id

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
        ) as ac:
            r = await ac.get(
        f"/user/{user_id}",
    )

    assert 200 <= r.status_code < 300

    api_user = r.json()
    existing_user = await get_user_by_username(user.username)

    assert existing_user
    assert existing_user.username == api_user["username"]

@pytest.mark.asyncio
async def test_update_user() -> None:
    username = random_username(1)
    user_in = UserCreate(username=username)
    
    await create_user(json.loads(user_in.model_dump_json()))
    
    user = await get_user_by_username(user_in.username)

    new_username = random_username(1)
    user_in_update = UserUpdate(username=new_username)
    
    if user.id is not None:
        await update_user_by_id(user.id, user_in_update)
    
    user_2 = await get_user_by_id(user.id)
    assert user_2
    assert user.id == user_2.id
    assert user.username != user_2.username