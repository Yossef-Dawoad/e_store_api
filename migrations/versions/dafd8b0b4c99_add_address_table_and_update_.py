"""add address table and update relationships

Revision ID: dafd8b0b4c99
Revises: b8d893efab08
Create Date: 2024-05-27 15:59:14.346390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel # NEW


# revision identifiers, used by Alembic.
revision: str = 'dafd8b0b4c99'
down_revision: Union[str, None] = 'b8d893efab08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('street_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('street_number', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('city', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('state', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('country', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('postal_code', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('address')
    # ### end Alembic commands ###
