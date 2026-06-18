from fastapi import APIRouter

from app.api.routes import user
from app.api.routes import characters

api_router = APIRouter()
api_router.include_router(characters.router)
api_router.include_router(user.router)