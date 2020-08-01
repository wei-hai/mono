"""
Mixins
"""
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.sql import func

Base: DeclarativeMeta = declarative_base()


def generate_random_uuid():
    """
    Generate random uuid
    :return:
    """
    return uuid4().hex


class TimestampMixin:
    """
    The TimestampMixin model.
    """

    created_at = sa.Column(sa.DateTime, server_default=func.now(), nullable=False)
    modified_at = sa.Column(
        sa.DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class UUIDMixin:
    """
    The UUIDMixin
    """

    id = sa.Column(sa.String(32), primary_key=True, default=generate_random_uuid)


class SoftDeleteMixin:
    """
    SoftDeleteMixin
    """

    is_deleted = sa.Column(sa.Boolean, server_default="f", nullable=False)
