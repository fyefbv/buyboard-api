import uuid
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9a0e4ac94306'
down_revision: Union[str, Sequence[str], None] = '44d1a2f4a817'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('categories',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4),
        sa.Column('name_translations', JSONB, nullable=False, unique=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('categories')
