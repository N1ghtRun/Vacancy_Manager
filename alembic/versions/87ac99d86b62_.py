"""empty message

Revision ID: 87ac99d86b62
Revises: 378ad6fade1d
Create Date: 2023-02-26 19:36:56.778615

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '87ac99d86b62'
down_revision = '378ad6fade1d'
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
    op.alter_column('vacancy', 'contacts_ids',
               existing_type=sa.VARCHAR(length=16),
               type_=sa.String(length=24),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vacancy', 'contacts_ids',
               existing_type=sa.String(length=24),
               type_=sa.VARCHAR(length=16),
               existing_nullable=True)
    op.alter_column('documents', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('contacts', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###
