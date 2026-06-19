from app.crud import get_user_by_username
from app.models import UserCreate
from app.utils.utils import random_username, random_password, random_email
import pytest

@pytest.mark.asyncio(loop_scope="session")
async def test_register_user(db_session, client) -> None:
    username = random_username(1)
    email = random_email()
    password = random_password()
    user_in = UserCreate(
        username=username,
        email=email,
        password=password,
        )

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