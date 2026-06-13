from pydantic import BaseModel

class Db(BaseModel):
    characters: dict[str, int]

class User(BaseModel):
    id: int
    username: str

class UserCreate(BaseModel):
    username: str