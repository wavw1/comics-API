from fastapi import APIRouter, HTTPException, Depends
from app.models import UserCreate, UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.db import get_db
from app.crud import create_user
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register/", status_code=201, response_model=UserRead)
async def register(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db)
    ):
    try:
        user = await create_user(session=session, user_in=user_in)
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=400, detail="invalid user data")
    
    return user