from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg://postgres:123@localhost:5432/postgres?sslmode=disable", echo=True)