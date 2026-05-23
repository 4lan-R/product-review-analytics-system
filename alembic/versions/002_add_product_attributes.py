"""Add color, storage_size, and rating columns

Revision ID: 002_add_product_attributes
Revises: 001_initial
Create Date: 2026-05-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_product_attributes'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('reviews', sa.Column('color', sa.String(), nullable=True))
    op.add_column('reviews', sa.Column('storage_size', sa.String(), nullable=True))
    op.add_column('reviews', sa.Column('rating', sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column('reviews', 'rating')
    op.drop_column('reviews', 'storage_size')
    op.drop_column('reviews', 'color')
