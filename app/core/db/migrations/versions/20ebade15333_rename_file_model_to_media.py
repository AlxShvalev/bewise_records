"""rename File model to Media

Revision ID: 20ebade15333
Revises: 1c5485ac681d
Create Date: 2023-05-31 13:52:44.619327

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20ebade15333'
down_revision = '1c5485ac681d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media',
    sa.Column('title', sa.String(length=1024), nullable=False),
    sa.Column('file_url', sa.String(length=255), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('file')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file',
    sa.Column('file_url', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['user.id'], name='file_owner_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='file_pkey')
    )
    op.drop_table('media')
    # ### end Alembic commands ###