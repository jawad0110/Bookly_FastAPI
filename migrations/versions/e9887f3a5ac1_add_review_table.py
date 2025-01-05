"""add review table

Revision ID: e9887f3a5ac1
Revises: 261152aa0abd
Create Date: 2024-12-25 19:14:38.192122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e9887f3a5ac1'
down_revision: Union[str, None] = '261152aa0abd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
   op.create_table(
        'Reviews',
        sa.Column('uid', sa.UUID(), nullable=False),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('review_text', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('user_uid', sa.UUID(), nullable=True),  # Keep as UUID if you might add the table later
        sa.Column('book_uid', sa.UUID(), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(), nullable=True),
        sa.Column('update_at', postgresql.TIMESTAMP(), nullable=True),
        sa.ForeignKeyConstraint(['book_uid'], ['books.uid'], ),
        sa.PrimaryKeyConstraint('uid')
    )

    
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Reviews')
    # ### end Alembic commands ###
