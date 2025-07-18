"""Add repository_id to rework_data

Revision ID: 5d6d20511cca
Revises: 85edbd09eeb8
Create Date: 2025-07-15 12:48:07.827255

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mssql

# revision identifiers, used by Alembic.
revision: str = '5d6d20511cca'
down_revision: Union[str, Sequence[str], None] = '85edbd09eeb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rework_data', sa.Column('repository_id', mssql.UNIQUEIDENTIFIER(), nullable=True))
    op.create_foreign_key(None, 'rework_data', 'repositories', ['repository_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rework_data', type_='foreignkey')
    op.drop_column('rework_data', 'repository_id')
    # ### end Alembic commands ###
