from core.db.sql_alchemy.sql_alchemy import engine
from sqlalchemy.orm import Session
from sqlalchemy import text

def create_user(user):
    stmt = text("INSERT INTO users (username) VALUES (:username)")
    
    try:
        with Session(engine) as session:
            session.execute(
                stmt,
                [user],
        )
            session.commit()
    except Exception:
        raise

def get_user_by_id(user_id: int):
    stmt = text("SELECT id, username FROM users WHERE id=:id")
    
    try:
        with Session(engine) as session:
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