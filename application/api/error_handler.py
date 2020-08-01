"""
This module includes error handler
"""
from typing import Any

from sanic.log import logger
from sanic.request import Request
from sanic.response import json


async def error_handler(request: Request, exception: Any):
    """
    Handle client and server errors
    @param request:
    @param exception:
    @return:
    """
    logger.error(exception)
    response = json({"message": exception.args[0]})
    response.status = exception.status_code
    return response
