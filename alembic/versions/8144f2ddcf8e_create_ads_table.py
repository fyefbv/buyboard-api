import uuid
from datetime import datetime, timezone
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8144f2ddcf8e'
down_revision: Union[str, Sequence[str], None] = '20a16e9adbbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'ads',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False, primary_key=True, default=uuid.uuid4),
        sa.Column('user_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('category_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('location_id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('price > 0', name='check_price_positive')
    )
    
    op.create_index(op.f('ix_ads_price'), 'ads', ['price'], unique=False)
    op.create_index(op.f('ix_ads_title'), 'ads', ['title'], unique=False)
    
    op.create_index(op.f('ix_ads_user_id'), 'ads', ['user_id'], unique=False)
    op.create_index(op.f('ix_ads_category_id'), 'ads', ['category_id'], unique=False)
    op.create_index(op.f('ix_ads_location_id'), 'ads', ['location_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_ads_location_id'), table_name='ads')
    op.drop_index(op.f('ix_ads_category_id'), table_name='ads')
    op.drop_index(op.f('ix_ads_user_id'), table_name='ads')
    op.drop_index(op.f('ix_ads_title'), table_name='ads')
    op.drop_index(op.f('ix_ads_price'), table_name='ads')
    
    op.drop_table('ads')
