"""
This is the module for defining database.
"""

from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# https://alembic.sqlalchemy.org/en/latest/naming.html#the-importance-of-naming-constraints
naming_convention = {
    "ix": "ix_%(column_0_N_label)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_N_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=naming_convention)
db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
