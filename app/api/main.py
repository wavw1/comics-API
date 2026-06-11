from fastapi import APIRouter

from api.routes import search, list
from api.routes import user

api_router = APIRouter()
api_router.include_router(search.router)
api_router.include_router(list.router)
api_router.include_router(user.router)