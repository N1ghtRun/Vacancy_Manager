"""empty message

Revision ID: 378ad6fade1d
Revises: 5748bdaec489
Create Date: 2023-02-26 19:23:22.176021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '378ad6fade1d'
down_revision = '5748bdaec489'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('contacts', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=0)
    op.alter_column('documents', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=0)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('documents', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('contacts', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###