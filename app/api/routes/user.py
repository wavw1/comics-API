from fastapi import APIRouter, HTTPException, Depends
from app.models import UserCreate, UserUpdate, UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.db import get_db

from app.crud import create_user, get_user_by_id, delete_user_by_id, update_user_by_id

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", status_code=201, response_model=UserRead)
async def create(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db)
    ):
    return await create_user(session=session, user_in=user_in)

@router.get("/{user_id}")
async def get(user_id: int,
    session: AsyncSession = Depends(get_db)
    ):
    try:
        user = await get_user_by_id(
            session=session,
            user_id=user_id,
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'failed to get user: {e}')
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.delete("/{user_id}", status_code=204)
async def delete(
    user_id: int,
    session: AsyncSession = Depends(get_db)
    ):
    try:
        user = await get_user_by_id(session=session, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'failed to get user: {e}')
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    repo_user_id = user.id

    try:
        await delete_user_by_id(session=session, user_id=repo_user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed deleting: {e}")

    return 

@router.patch("/{user_id}")
async def patch(
    user_id: int, 
    updated_user: UserUpdate,
    session: AsyncSession = Depends(get_db)
    ):
    try:
        user = await get_user_by_id(
            session=session, 
            user_id=user_id,
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'failed to get user: {e}')
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    repo_user_id = user.id

    try:
        user = await update_user_by_id(
            session=session, 
            user_id=repo_user_id, 
            updated_user=updated_user,
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"failed to update: {e}")
    
    return user