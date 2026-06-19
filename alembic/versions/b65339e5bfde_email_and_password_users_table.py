"""email and password users table

Revision ID: b65339e5bfde
Revises: 02b192d1325f
Create Date: 2026-06-19 08:33:05.393530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b65339e5bfde'
down_revision: Union[str, Sequence[str], None] = '02b192d1325f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('email', sa.String(255), unique=True, nullable=False))
    op.add_column('users', sa.Column('password_hash', sa.TEXT, nullable=False))
    op.create_check_constraint(
        "check_email_format",
        table_name="users",
        condition="email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'"
    )
    pass


def downgrade() -> None:
    op.drop_constraint("check_email_format", table_name="users", type_="check")
    op.drop_column('users', 'email')
    op.drop_column('users', 'password_hash')
    pass
