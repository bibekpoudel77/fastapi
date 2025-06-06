"""TEST

Revision ID: 04a3f946db01
Revises: 747f50c16722
Create Date: 2025-06-05 09:53:43.445699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04a3f946db01'
down_revision: Union[str, None] = '747f50c16722'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
