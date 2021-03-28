"""
User and Role
"""
import sqlalchemy as sa

from application.model.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """
    User model
    """

    __tablename__ = "user"
    id = sa.Column(sa.BigInteger, primary_key=True)
    email = sa.Column(sa.String(255), nullable=False)
    password = sa.Column(sa.String(32), nullable=False)
    salt = sa.Column(sa.String(32), nullable=False)
    role_id = sa.Column(sa.BigInteger, nullable=False)
