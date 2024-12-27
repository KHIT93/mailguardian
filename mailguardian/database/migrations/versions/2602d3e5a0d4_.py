"""empty message

Revision ID: 2602d3e5a0d4
Revises: 902e96660a66
Create Date: 2024-09-21 21:58:50.439626

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision: str = '2602d3e5a0d4'
down_revision: Union[str, None] = '902e96660a66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('audit_log', sa.Column('allowed', sa.Boolean(), nullable=True))
    # Adjust all existing values
    op.execute("UPDATE audit_log SET allowed = false WHERE message ilike 'Denied%'")
    op.execute("UPDATE audit_log SET allowed = true WHERE allowed IS NULL")
    # Then mark it as not nullable
    op.alter_column('audit_log', 'allowed', nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('audit_log', 'allowed')
    # ### end Alembic commands ###