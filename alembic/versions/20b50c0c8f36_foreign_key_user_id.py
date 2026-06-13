"""foreign key user_id

Revision ID: 20b50c0c8f36
Revises: 7d1b5620fecf
Create Date: 2026-06-13 09:46:19.625371

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20b50c0c8f36'
down_revision: Union[str, Sequence[str], None] = '7d1b5620fecf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_user_id",
        "characters",
        "users",
        ["user_id"],
        ["id"],
    )
    pass


def downgrade() -> None:
    op.drop_constraint('fk_user_id', 'characters', type_='foreignkey')
    pass
