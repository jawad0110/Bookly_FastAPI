"""add roles to users

Revision ID: 6782e7ea6c88
Revises: 3c0ee1ef38b2
Create Date: 2024-12-25 01:19:17.004197

"""
import datetime
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
import sqlalchemy.dialects.postgresql as pg
import uuid

# revision identifiers, used by Alembic.
revision: str = '6782e7ea6c88'
down_revision: Union[str, None] = '3c0ee1ef38b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the user_uid column to the books table
    op.add_column('books', sa.Column('user_uid', sa.UUID(), nullable=True))

    # Now, create the foreign key
    op.create_foreign_key('fk_books_user_uid', 'books', 'users', ['user_uid'], ['uid'])


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_books_user_uid', 'books', type_='foreignkey')
    # ### end Alembic commands ###