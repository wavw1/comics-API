from fastapi import APIRouter
import httpx

router = APIRouter(prefix="/characters", tags=["characters"])

@router.get("/search/{character_name}")
def search(character_name: str, biography: bool = False):
    if biography:
        r = httpx.get(f'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/biography/{character_name}.json')
        return {f"{character_name}'s biography": r.json()}

    r = httpx.get(f'https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/id/{character_name}.json')
    
    return {"character": r.json()}