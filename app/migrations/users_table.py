from sqlalchemy import Table, Column, Integer, String, ARRAY, TEXT
from app.models import metadata_obj

users_table = Table(
    "users",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), nullable=False),
)