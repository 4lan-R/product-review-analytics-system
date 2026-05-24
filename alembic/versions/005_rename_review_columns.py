"""Rename review columns - title to review_title and text to review_text

Revision ID: 005_rename_review_columns
Revises: 004_create_products_and_review_fk
Create Date: 2026-05-24 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '005_rename_review_columns'
down_revision = '004_create_products_and_review_fk'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('reviews', recreate='always') as batch_op:
        batch_op.alter_column('title', new_column_name='review_title')
        batch_op.alter_column('text', new_column_name='review_text')


def downgrade() -> None:
    with op.batch_alter_table('reviews', recreate='always') as batch_op:
        batch_op.alter_column('review_title', new_column_name='title')
        batch_op.alter_column('review_text', new_column_name='text')
