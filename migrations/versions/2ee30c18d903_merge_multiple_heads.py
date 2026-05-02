"""merge multiple heads

Revision ID: 2ee30c18d903
Revises: 7f7051746b0e, a5da181bdee1
Create Date: 2026-05-01 20:31:44.768104

"""
from typing import Sequence, Union
import sqlmodel
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ee30c18d903'
down_revision: Union[str, Sequence[str], None] = ('7f7051746b0e', 'a5da181bdee1')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
