"""v1

Revision ID: 8206dd168650
Revises: 
Create Date: 2025-03-16 17:45:45.484538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8206dd168650'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vin', sa.String(), nullable=False),
    sa.Column('mark', sa.String(), nullable=False),
    sa.Column('model', sa.String(), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('vin')
    )
    op.create_table('mechanic',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('driver',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('phone', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('run', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('mechanic_id', sa.Integer(), nullable=False),
    sa.Column('car_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['car_id'], ['car.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['mechanic_id'], ['mechanic.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bid',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('state', sa.Enum('procces', 'done', name='state'), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('mechanic_id', sa.Integer(), nullable=False),
    sa.Column('driver_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['driver_id'], ['driver.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['mechanic_id'], ['mechanic.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bid')
    op.drop_table('history')
    op.drop_table('driver')
    op.drop_table('mechanic')
    op.drop_table('car')

    # Если нужно удалить тип Enum, созданный для этого столбца
    op.execute("DROP TYPE IF EXISTS state")

    # ### end Alembic commands ###
