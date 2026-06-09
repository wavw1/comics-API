from fastapi import APIRouter

from api.routes import search, list

api_router = APIRouter()
api_router.include_router(search.router)
api_router.include_router(list.router)