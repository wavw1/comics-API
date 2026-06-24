from app.crud import create_user, get_user_by_username, get_user_by_id, update_user_by_id
from app.models import UserUpdate
from app.utils.utils import random_username, random_user
import pytest

@pytest.mark.asyncio(loop_scope="session")
async def test_get_non_existing_user(db_session, client) -> None:
    user_in = random_user()
    await create_user(session=db_session, user_in=user_in)

    user = await get_user_by_username(
         session=db_session,
         username=user_in.username,
         )
    non_existing_id = user.id + 1

    login_data = {
        "username": user_in.username,
        "password": user_in.password,
    }
    r = await client.post("/auth/login/", json=login_data)
    tokens = r.json()
    a_token = tokens["token"]["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    
    r = await client.get(
        f"/user/{non_existing_id}",
        headers=headers
    )

    assert r.status_code == 404
    assert r.json() == {"detail": "User not found"}

@pytest.mark.asyncio(loop_scope="session")
async def test_get_existing_user(db_session, client) -> None:
    user_in = random_user()
    user = await create_user(
        session=db_session, 
        user_in=user_in,
        )
    user_id = user.id

    login_data = {
        "username": user_in.username,
        "password": user_in.password,
    }
    r = await client.post("/auth/login/", json=login_data)
    tokens = r.json()
    a_token = tokens["token"]["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = await client.get(
        f"/user/{user_id}",
        headers=headers,
    )

    assert 200 <= r.status_code < 300

    api_user = r.json()
    existing_user = await get_user_by_username(
        session=db_session, 
        username=user.username,
        )

    assert existing_user
    assert existing_user.username == api_user["username"]

@pytest.mark.asyncio(loop_scope="session")
async def test_update_user(db_session, client) -> None:
    user_in = random_user()
    user = await create_user(
        session=db_session,
        user_in=user_in,
        )
    user_id = user.id
    user_username = user.username

    new_username = random_username(1)
    user_in_update = UserUpdate(username=new_username)
    
    user_2 = await update_user_by_id(
        session=db_session,
        user_id=user_id, 
        updated_user=user_in_update,
        )
    user_2_id = user_2.id
    user_2_username = user_2.username

    assert user_2
    assert user_id == user_2_id
    assert user_username != user_2_username

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user(db_session, client) -> None:
    user_in = random_user()
    user = await create_user(
        session=db_session,
        user_in=user_in,
    )
    user_id = user.id

    login_data = {
        "username": user_in.username,
        "password": user_in.password,
    }
    r = await client.post("/auth/login/", json=login_data)
    tokens = r.json()
    a_token = tokens["token"]["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    
    r = await client.delete(
        f"/user/{user_id}",
        headers=headers
    )
    assert r.status_code == 204

    repo_user = await get_user_by_id(
        session=db_session,
        user_id=user_id
    )
    assert repo_user == None

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_non_existing_user(db_session, client) -> None:
    user_in = random_user()
    user = await create_user(
        session=db_session,
        user_in=user_in,
    )
    non_existing_id = user.id + 1

    login_data = {
        "username": user_in.username,
        "password": user_in.password,
    }
    r = await client.post("/auth/login/", json=login_data)
    tokens = r.json()
    a_token = tokens["token"]["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    
    r = await client.delete(
        f"/user/{non_existing_id}",
        headers=headers
    )
    assert r.status_code == 404
    assert r.json() == {"detail": "User not found"}