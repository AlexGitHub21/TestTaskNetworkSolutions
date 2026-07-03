"""Create ticket table

Revision ID: 87242c671dae
Revises: 9e556c78df85
Create Date: 2026-06-30 23:35:54.661964

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87242c671dae'
down_revision: Union[str, Sequence[str], None] = '9e556c78df85'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
