from app.models import metadata_obj
from app.core.db.sql_alchemy.sql_alchemy import engine

from app.migrations.users_table import users_table
from app.migrations.characters_table import characters_table

metadata_obj.create_all(engine)