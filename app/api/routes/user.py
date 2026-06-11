from fastapi import APIRouter, HTTPException
from models import User
import json

from crud import create_user, get_user_by_id

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/", status_code=201)
def create(request: User):
    try:
        create_user(json.loads(request.model_dump_json()))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'failed to create user: {e}')

    return {"message": "user has been created"}

@router.get("/{user_id}")
def get(user_id: int):
    try:
        user = get_user_by_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'failed to get user: {e}')

    return user