from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.db import get_db
from app.crud import search_character
from app.scripts.seed_characters import load_characters_glossary

router = APIRouter(prefix="/characters", tags=["characters"])

@router.get("/search/{character_name}")
async def search(
    character_name: str,
    session: AsyncSession = Depends(get_db), 
    ):
    character = await search_character(session=session, name=character_name)
    
    return {"character": character}

@router.post("/glossary/")
async def glossary(
    session: AsyncSession = Depends(get_db)
):
    try:
        await load_characters_glossary(session=session)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e}')

    return {"message": "glossary was initialized"}