"""
Helper functions
"""
import math
from typing import Dict

from sanic_openapi import doc


class Pagination:
    """
    Pagination
    """

    total = doc.Integer("total count")
    page = doc.Integer("current page number")
    last_page = doc.Integer("last page number")
    per_page = doc.Integer("number of results per page")


def extract_class_fields(cls):
    """
    Extract class fields
    :param cls:
    :return:
    """
    return tuple([k for k in vars(cls).keys() if not k.startswith("__")])


def build_pagination_info(count: int, page: int, per_page: int) -> Dict[str, int]:
    """
    Build pagination information
    :param count:
    :param page:
    :param per_page:
    :return:
    """
    last_page = int(math.ceil(1.0 * count / per_page) - 1)
    return {"total": count, "page": page, "last_page": last_page, "per_page": per_page}
