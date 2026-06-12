from app.core.db.sql_alchemy.sql_alchemy import Session
from sqlalchemy import text, select
from app.models import UserCreate, User

def create_user(user_create: UserCreate):
    stmt = text("INSERT INTO users (username) VALUES (:username)")

    try:
        with Session.begin() as session:
            session.execute(
                stmt,
                [user_create],
        )
            session.commit()
    except Exception:
        raise

def get_user_by_id(user_id: int) -> User | None:
    stmt = text("SELECT id, username FROM users WHERE id=:id")
    
    try:
        with Session.begin() as session:
            result = session.execute(
                stmt,
                [{"id": user_id}],
        )
            
            for row in result:
                user = {
                    "id": row.id,
                    "username": row.username,
                }
                return user
    except Exception:
        raise

def get_user_by_username(username: str) -> User | None:
    stmt = text("SELECT id, username FROM users WHERE username=:username")
    
    try:
        with Session.begin() as session:
            result = session.execute(
                stmt,
                [{"username": username}],
        )
            
            for row in result:
                user = User(
                    id=row.id,
                    username=row.username,
                )
                return user
    except Exception:
        raise