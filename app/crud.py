from app.core.db.db import async_session
from sqlalchemy import text, select, update, delete
from app.models import UserCreate, User, UserUpdate, UserRead
from sqlalchemy.ext.asyncio import AsyncSession

async def create_user(session: AsyncSession, user_in: UserCreate):
    user = User(username=user_in.username)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user

async def get_user_by_id(session: AsyncSession, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    result = await session.scalars(statement)
    user = result.first()
    return user

async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    statement = select(User).where(User.username == username)
    result = await session.scalars(statement)
    user = result.first()
    return user

async def delete_user_by_id(session: AsyncSession, user_id: int) -> None:
    statement = delete(User).where(User.id == user_id)
    await session.execute(statement)
    await session.commit()

async def update_user_by_id(session: AsyncSession, user_id: int, updated_user: UserUpdate) -> User | None:
    if updated_user.username == None or updated_user.username == "":
        updated_user.username = f"user_{user_id}"
    
    statement = update(User).where(User.id == user_id).values(username=updated_user.username).returning(User)

    result = await session.scalars(statement)
    await session.commit()
    user = result.first()
    return user