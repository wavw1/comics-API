from fastapi import APIRouter, HTTPException
from app.models import UserCreate
import json

from app.crud import create_user, get_user_by_id, get_user_by_username

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", status_code=201)
def create(user_in: UserCreate):
    user = get_user_by_username(user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )

    try:
        create_user(json.loads(user_in.model_dump_json()))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'failed to create user: {e}')

    return {"message": "user has been created"}

@router.get("/{user_id}")
def get(user_id: int):
    try:
        user = get_user_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'failed to get user: {e}')
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user