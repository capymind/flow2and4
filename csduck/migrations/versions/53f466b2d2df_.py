"""empty message

Revision ID: 53f466b2d2df
Revises: 491019b4ed51
Create Date: 2023-05-01 23:25:20.911486

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53f466b2d2df'
down_revision = '491019b4ed51'
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_pyduck():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question_reaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(), nullable=False),
    sa.Column('created_at', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], name=op.f('fk_question_reaction_question_id_question')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_question_reaction_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_question_reaction')),
    sa.UniqueConstraint('user_id', 'question_id', 'code', name=op.f('uq_question_reaction_user_id_question_id_code'))
    )
    # ### end Alembic commands ###


def downgrade_pyduck():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('question_reaction')
    # ### end Alembic commands ###


def upgrade_faduck():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_faduck():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###

