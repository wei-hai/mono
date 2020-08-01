"""
Customized exception
"""
from sanic.exceptions import SanicException


class ApiServerError(SanicException):
    """
    ApiServerError
    """
