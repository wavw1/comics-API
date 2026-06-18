"""create characters_glossary table

Revision ID: 02b192d1325f
Revises: 20b50c0c8f36
Create Date: 2026-06-18 09:17:30.883978

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02b192d1325f'
down_revision: Union[str, Sequence[str], None] = '20b50c0c8f36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'characters_glossary',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(30), nullable=False),
        sa.Column('biography', sa.TEXT, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table('characters_glossary')
    pass
