"""create characters table

Revision ID: 7d1b5620fecf
Revises: 8001100563aa
Create Date: 2026-06-13 09:31:05.704256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d1b5620fecf'
down_revision: Union[str, Sequence[str], None] = '8001100563aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'characters',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(30), nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table('characters')
    pass
