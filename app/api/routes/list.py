from fastapi import APIRouter

from core.db import all_characters, characters

router = APIRouter(prefix="/list", tags=["list"])

@router.get("/")
def list():
    list = all_characters(characters)

    return {"list of all characters": list}