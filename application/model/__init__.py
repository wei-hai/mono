"""
Initiate Base
"""
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

Base: DeclarativeMeta = declarative_base()

from application.model.user import User  # noqa pylint: disable=wrong-import-position
from application.model.role import Role  # noqa pylint: disable=wrong-import-position
