"""Add title and verified_purchase columns

Revision ID: 003_add_title_verified_purchase
Revises: 002_add_product_attributes
Create Date: 2026-05-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_add_title_verified_purchase'
down_revision = '002_add_product_attributes'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('reviews', sa.Column('title', sa.String(), nullable=False, server_default=''))
    op.add_column('reviews', sa.Column('verified_purchase', sa.Boolean(), nullable=False, server_default='0'))


def downgrade() -> None:
    op.drop_column('reviews', 'verified_purchase')
    op.drop_column('reviews', 'title')
