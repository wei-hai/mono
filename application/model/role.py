"""
Role
"""
import sqlalchemy as sa

from application.model import Base
from application.model.base import TimestampMixin


class Role(Base, TimestampMixin):
    """
    Role model
    """
    __tablename__ = "role"
    id = sa.Column(sa.BigInteger, primary_key=True)
    name = sa.Column(sa.String(255), nullable=False)
    description = sa.Column(sa.TEXT, nullable=True)
