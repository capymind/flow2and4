"""empty message

Revision ID: 598485880e7d
Revises: 369373b507cc
Create Date: 2023-04-29 21:23:21.854622

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '598485880e7d'
down_revision = '369373b507cc'
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
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.Integer(), nullable=False),
    sa.Column('password', sa.Integer(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('verified', sa.Boolean(), nullable=False),
    sa.Column('role', sa.String(), nullable=False),
    sa.Column('created_at', sa.String(), nullable=False),
    sa.Column('deleted_at', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user')),
    sa.UniqueConstraint('nickname', name=op.f('uq_user_nickname')),
    sa.UniqueConstraint('username', name=op.f('uq_user_username')),
    schema='pyduck_schema'
    )
    op.create_table('user_avatar',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.Column('original_filename', sa.String(), nullable=False),
    sa.Column('mimetype', sa.String(), nullable=True),
    sa.Column('filesize', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['pyduck_schema.user.id'], name=op.f('fk_user_avatar_user_id_user')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_user_avatar')),
    schema='pyduck_schema'
    )
    op.drop_table('user_avatar')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade_pyduck():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.INTEGER(), nullable=False),
    sa.Column('nickname', sa.INTEGER(), nullable=False),
    sa.Column('password', sa.INTEGER(), nullable=False),
    sa.Column('active', sa.BOOLEAN(), nullable=False),
    sa.Column('verified', sa.BOOLEAN(), nullable=False),
    sa.Column('role', sa.VARCHAR(), nullable=False),
    sa.Column('created_at', sa.VARCHAR(), nullable=False),
    sa.Column('deleted_at', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id', name='pk_user'),
    sa.UniqueConstraint('nickname', name='uq_user_nickname'),
    sa.UniqueConstraint('username', name='uq_user_username')
    )
    op.create_table('user_avatar',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('created_at', sa.VARCHAR(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('url', sa.VARCHAR(), nullable=False),
    sa.Column('filename', sa.VARCHAR(), nullable=False),
    sa.Column('original_filename', sa.VARCHAR(), nullable=False),
    sa.Column('mimetype', sa.VARCHAR(), nullable=True),
    sa.Column('filesize', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='fk_user_avatar_user_id_user'),
    sa.PrimaryKeyConstraint('id', name='pk_user_avatar')
    )
    op.drop_table('user_avatar', schema='pyduck_schema')
    op.drop_table('user', schema='pyduck_schema')
    # ### end Alembic commands ###


def upgrade_faduck():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_faduck():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
