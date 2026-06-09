from fastapi import APIRouter
import httpx

from core.db import find_character

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/{character_name}")
def character(character_name: str, biography: bool = False):
    character_id = find_character(character_name)
    
    if biography:
        r = httpx.get(f'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/biography/{character_id}.json')
        return {f"{character_name}'s biography": r.json()}

    r = httpx.get(f'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/id/{character_id}.json')
    
    return {"character": r.json()}