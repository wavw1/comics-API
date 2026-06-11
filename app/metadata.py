from models import metadata_obj
from core.db.sql_alchemy.sql_alchemy import engine

from migrations.users_table import users_table
from migrations.characters_table import characters_table

metadata_obj.create_all(engine)