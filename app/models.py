from pydantic import BaseModel
from typing import Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class Db(BaseModel):
    characters: dict[str, int]

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))

class UserCreate(BaseModel):
    username: str

class UserRead(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True} 

class UserUpdate(BaseModel):
    username: Optional[str] = None