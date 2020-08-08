"""
Initiate Base
"""
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

from application.model.role import Role  # noqa pylint: disable=wrong-import-position
from application.model.user import User  # noqa pylint: disable=wrong-import-position

Base: DeclarativeMeta = declarative_base()
