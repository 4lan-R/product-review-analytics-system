"""Create products table and add foreign key to reviews

Revision ID: 004_create_products_and_review_fk
Revises: 003_add_title_verified_purchase
Create Date: 2026-05-23 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004_create_products_and_review_fk'
down_revision = '003_add_title_verified_purchase'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'products',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    with op.batch_alter_table('reviews', recreate='always') as batch_op:
        batch_op.alter_column('product_id', existing_type=sa.String(), nullable=False)
        batch_op.create_foreign_key(
            'fk_reviews_product_id_products',
            'products',
            ['product_id'],
            ['id']
        )


def downgrade() -> None:
    with op.batch_alter_table('reviews', recreate='always') as batch_op:
        batch_op.drop_constraint('fk_reviews_product_id_products', type_='foreignkey')

    op.drop_table('products')
