import httpx
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Characters_Glossary
import json

async def load_characters_glossary(session: AsyncSession):
    statement = select(Characters_Glossary).where(Characters_Glossary.id == 1)
    
    result = await session.scalars(statement)
    id = result.first()

    if id == None:

        async with httpx.AsyncClient() as client:
            r = await client.get('https://cdn.jsdelivr.net/gh/akabab/superhero-api@0.3.0/api/all.json')
        
        data = r.json()

        data_to_insert = []
    
        for i in range(0, len(data)):
            character = {"id": data[i]["id"], "name": data[i]["name"], "biography": json.dumps(data[i]["biography"])}
            data_to_insert.append(character)

        await session.execute(
            insert(Characters_Glossary),
            data_to_insert
            )
        await session.commit()
    else:
        raise Exception('glossary already initialized')