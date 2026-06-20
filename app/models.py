from pydantic import BaseModel
from typing import Optional
from sqlalchemy import String, TEXT
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class Db(BaseModel):
    characters: dict[str, int]

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(TEXT, nullable=False)

class Characters_Glossary(Base):
    __tablename__ = 'characters_glossary'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    biography: Mapped[str] = mapped_column(TEXT)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class AuthorizedUser(BaseModel):
    id: int
    email: str
    username: str

class UserRead(BaseModel):
    id: int
    username: str
    email: str

    model_config = {"from_attributes": True} 

class UserUpdate(BaseModel):
    username: Optional[str] = None

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int