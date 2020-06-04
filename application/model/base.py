"""
Mixin
"""
import sqlalchemy as sa
from sqlalchemy.sql import func


class TimestampMixin:
    """
    The TimestampMixin model.
    """
    created_at = sa.Column(sa.DateTime, server_default=func.now(), nullable=False)
    modified_at = sa.Column(sa.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
