from app.core.db.db import async_session
from sqlalchemy import text, select
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
    statement = select(User).where(User.id == user_id)
    await session.delete(statement)


async def update_user_by_id(user_id: int, updated_user: UserUpdate) -> User | None:
    stmt = text("""
                UPDATE users 
                SET username=:username 
                WHERE id=:id
                RETURNING id, username
                """)

    if updated_user.username == None or updated_user.username == "":
        updated_user.username = f"user_{user_id}"

    try:
        async with async_session.begin() as session:
            result = await session.execute(
                stmt,
                [{"username": updated_user.username, "id": user_id}]
            )

            for row in result:
                return User(
                    id=row.id,
                    username=row.username
                    )
    except Exception:
        raise