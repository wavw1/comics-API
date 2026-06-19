from fastapi import APIRouter

from app.api.routes import user, characters, auth

api_router = APIRouter()
api_router.include_router(characters.router)
api_router.include_router(user.router)
api_router.include_router(auth.router)