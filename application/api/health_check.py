"""
Health check
"""
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from sanic_openapi import doc

bp = Blueprint(name="Health_check", url_prefix="/health_check")


@bp.get("/")
@doc.summary("Health check")
@doc.description("Health check")
@doc.response(200, {"status": str}, description="health check")
async def health_check(request: Request):
    """
    Health Check
    :param request:
    :return:
    """
    return json({"status": "everything is good!"})
