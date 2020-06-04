"""
Health check
"""
from sanic.request import Request
from sanic.response import text


async def health_check(request: Request):
    """
    Health check
    @param request:
    @return:
    """
    return text("everything is ok!")
