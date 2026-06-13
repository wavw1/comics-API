from fastapi.testclient import TestClient
from app.main import app
from app.crud import create_user, get_user_by_username
from app.models import UserCreate
import json
from app.utils.utils import random_username

client = TestClient(app)

def test_create_user() -> None:
    username = random_username(1)
    data = {"username": username}
    r = client.post(
        f"/user/",
        json=data
    )
    assert r.status_code == 201

def test_get_non_existing_user() -> None:
    user_in = UserCreate(username=random_username(1))
    create_user(json.loads(user_in.model_dump_json()))
    
    user = get_user_by_username(user_in.username)
    non_existing_id = user.id + 1
    
    r = client.get(
        f"/user/{non_existing_id}",
    )
    assert r.status_code == 404
    assert r.json() == {"detail": "User not found"}

def test_get_existing_user() -> None:
    user_in = UserCreate(username=random_username(1))
    create_user(json.loads(user_in.model_dump_json()))
    
    user = get_user_by_username(user_in.username)
    user_id = user.id

    r = client.get(
        f"/user/{user_id}",
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = get_user_by_username(user.username)
    assert existing_user
    assert existing_user.username == api_user["username"]