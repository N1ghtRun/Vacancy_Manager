"""empty message

Revision ID: adad3b4e4768
Revises: 87ac99d86b62
Create Date: 2023-02-26 20:20:56.004274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adad3b4e4768'
down_revision = '87ac99d86b62'
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
               existing_type=sa.VARCHAR(length=24),
               type_=sa.String(length=240),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('vacancy', 'contacts_ids',
               existing_type=sa.String(length=240),
               type_=sa.VARCHAR(length=24),
               existing_nullable=True)
    op.alter_column('documents', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    op.alter_column('contacts', 'name',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
    # ### end Alembic commands ###
