"""empty message

Revision ID: deb735447bee
Revises: b1ed4422fde3
Create Date: 2023-05-06 22:20:26.027512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'deb735447bee'
down_revision = 'b1ed4422fde3'
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
    op.create_table('post_comment_vote',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('comment_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['comment_id'], ['post_comment.id'], name=op.f('fk_post_comment_vote_comment_id_post_comment')),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name=op.f('fk_post_comment_vote_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_post_comment_vote'))
    )
    with op.batch_alter_table('post_comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('vote_count', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('comment_count', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade_pyduck():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post_comment', schema=None) as batch_op:
        batch_op.drop_column('comment_count')
        batch_op.drop_column('vote_count')

    op.drop_table('post_comment_vote')
    # ### end Alembic commands ###


def upgrade_faduck():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_faduck():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
