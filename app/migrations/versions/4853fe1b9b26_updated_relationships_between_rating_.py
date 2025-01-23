"""Updated relationships between Rating and Review models

Revision ID: 4853fe1b9b26
Revises: 4c4190c590d9
Create Date: 2025-01-22 12:20:57.430052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4853fe1b9b26'
down_revision: Union[str, None] = '4c4190c590d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ratings', sa.Column('review_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'ratings', 'reviews', ['review_id'], ['id'])
    op.drop_constraint('reviews_rating_id_fkey', 'reviews', type_='foreignkey')
    op.drop_column('reviews', 'rating_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('rating_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('reviews_rating_id_fkey', 'reviews', 'ratings', ['rating_id'], ['id'])
    op.drop_constraint(None, 'ratings', type_='foreignkey')
    op.drop_column('ratings', 'review_id')
    # ### end Alembic commands ###
