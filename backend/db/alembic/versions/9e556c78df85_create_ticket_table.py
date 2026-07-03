"""Create ticket table

Revision ID: 9e556c78df85
Revises: 85da9f43d504
Create Date: 2026-06-30 23:35:27.397327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e556c78df85'
down_revision: Union[str, Sequence[str], None] = '85da9f43d504'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
