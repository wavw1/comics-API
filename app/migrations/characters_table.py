from sqlalchemy import Table, Column, Integer, String, ForeignKey, ARRAY, TEXT
from models import metadata_obj

characters_table = Table(
    "characters",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30), nullable=False),
    Column("user_id", ForeignKey("users.id"), nullable=False)
)