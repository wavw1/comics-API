from fastapi import APIRouter, HTTPException, Depends
from app.models import UserCreate, UserRead, UserLogin, Token, User, AuthorizedUser
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.db import get_db
from app.crud import create_user, get_user_by_username
from datetime import timedelta
from app.core.security import verify_password, create_access_token, create_refresh_token, decode_token
from sqlalchemy import select

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register/", status_code=201, response_model=UserRead)
async def register(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db)
    ):
    if len(user_in.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    try:
        user = await create_user(session=session, user_in=user_in)
    except Exception:
        await session.rollback()
        raise HTTPException(status_code=400, detail="Invalid user data")
    
    return user

@router.post("/login/")
async def login(
    user_in: UserLogin,
    session: AsyncSession = Depends(get_db)
    ):
    repo_user = await get_user_by_username(session=session, username=user_in.username)
    
    if not repo_user:
        raise HTTPException(
        status_code=401,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

    verify = verify_password(user_in.password, repo_user.password_hash)

    if not verify[0]:
        raise HTTPException(
        status_code=401,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
        
    access_token = create_access_token(
        subject=repo_user.id,
        expires_delta=timedelta(minutes=30)
        )
    refresh_token = create_refresh_token(data={"sub": str(repo_user.id)})
    
    authorized_user = AuthorizedUser(
        id=repo_user.id,
        email=repo_user.email,
        username=repo_user.username,
    )

    token = Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )

    return {"user": authorized_user, "token": token}

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    session: AsyncSession = Depends(get_db)
):
    payload = decode_token(refresh_token)
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
    
    user_id = int(payload.get("sub"))
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
    
    statement = select(User).where(User.id == user_id)
    
    result = await session.scalars(statement)
    user = result.first()
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    
    new_access_token = create_access_token(
        subject=user.id, 
        expires_delta=timedelta(minutes=30),
        )
    
    return {
        "access_token": new_access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }