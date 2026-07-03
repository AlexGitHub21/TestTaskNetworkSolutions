"""Create ticket table4

Revision ID: 9ff63642d17a
Revises: 87242c671dae
Create Date: 2026-06-30 23:39:53.502509

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9ff63642d17a'
down_revision: Union[str, Sequence[str], None] = '87242c671dae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
