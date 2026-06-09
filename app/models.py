from pydantic import BaseModel

class Db(BaseModel):
    characters: dict[str, int]