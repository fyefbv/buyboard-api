from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '98d418bede77'
down_revision: Union[str, Sequence[str], None] = '8144f2ddcf8e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('favorites',
        sa.Column('user_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('ad_id', sa.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['ad_id'], ['ads.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'ad_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('favorites')
