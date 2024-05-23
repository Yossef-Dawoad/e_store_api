"""user email as unique

Revision ID: c2e5b0e9c171
Revises: 13e887697e69
Create Date: 2024-05-23 02:10:10.302237

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel # NEW


# revision identifiers, used by Alembic.
revision: str = 'c2e5b0e9c171'
down_revision: Union[str, None] = '13e887697e69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    # ### end Alembic commands ###
