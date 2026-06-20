from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.db import get_db
from app.models import User
from app.models import TokenData
from app.core.security import decode_token
from sqlalchemy import select

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_db)
) -> User:
    """
    Зависимость, которая извлекает текущего пользователя из токена.
    Используется для защиты эндпоинтов.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    token_data = TokenData(user_id=int(user_id))

    statement = select(User).where(User.id == token_data.user_id)
    result = await session.scalars(statement)
    user = result.first()
    
    if user is None:
        raise credentials_exception
    
    return user