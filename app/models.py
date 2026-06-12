from pydantic import BaseModel

from sqlalchemy import MetaData
metadata_obj = MetaData()

class Db(BaseModel):
    characters: dict[str, int]

class User(BaseModel):
    id: int
    username: str

class UserCreate(BaseModel):
    username: str