"""
Health check
"""
from typing import List
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from sanic_openapi import doc
from application.thrifts.services.user import UserService
from application.thrifts.services.user.ttypes import User

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
    user_service_client: UserService.Client = request.app.ctx.user_service_client
    req: UserService.GetUserByIdRequest = UserService.GetUserByIdRequest(ids=["user_id_1", "user_id_2"])
    res: UserService.GetUserByIdResponse = await request.app.loop.run_in_executor(None, user_service_client.get_user_by_id, req)
    users: List[User] = res.users
    if users:
        for user in users:
            print(user.id)
            print(user.info.first_name)
            print(user.info.last_name)
    return json({"status": "everything is good!"})
