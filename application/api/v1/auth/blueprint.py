"""
Auth blueprint
"""
from marshmallow import ValidationError
from sanic import Blueprint
from sanic.exceptions import InvalidUsage
from sanic.request import Request
from sanic.response import json
from sanic_openapi import doc

from application.api.util.auth import generate_jwt, auth
from application.api.v1.auth.schema import SignUpPostSchema, SignInPostSchema
from application.model.user import User
from application.repository.user import UserRepository

bp = Blueprint(name="/v1/auth", url_prefix="/v1/auth")


@bp.post("/sign_up")
@doc.summary("User sign up")
@doc.description("User sign up")
@doc.consumes(doc.JsonBody({
    "email": str,
    "password": str
}), content_type="application/json", location="body")
@doc.consumes({'Authorization': str}, location="header")
@doc.produces(User,
              description="user object",
              content_type="application/json")
async def sign_up(request: Request):
    """
    Sign up
    @param request:
    @return:
    """
    try:
        params = SignUpPostSchema().load(request.json)
    except ValidationError as ex:
        raise InvalidUsage(ex.messages)
    user_repo = UserRepository(request.app.db_client)
    user = user_repo.find_by_email(params["email"])
    if user:
        raise InvalidUsage("User already exists", 422)
    user = user_repo.create(params["email"], params["password"])
    return json(user)


@bp.post("/sign_in")
@doc.summary("User sign in")
@doc.description("User sign in")
@doc.consumes(doc.JsonBody({
    "email": str,
    "password": str
}), content_type="application/json", location="body")
@doc.produces({"token": str, "refresh_token": str},
              description="Token",
              content_type="application/json")
async def sign_in(request: Request):
    """
    Sign in
    @param request:
    @return:
    """
    try:
        params = SignInPostSchema().load(request.json)
    except ValidationError as ex:
        raise InvalidUsage(ex.messages)
    user_repo = UserRepository(request.app.db_client)
    user = user_repo.find_by_email_password(params["email"], params["password"])
    if not user:
        raise InvalidUsage("Email or password incorrect")
    jwt_secret = request.app.config["JWT_SECRET"]
    jwt_refresh_secret = request.app.config["JWT_REFRESH_SECRET"]
    token = generate_jwt(request.app.config["SERVICE_NAME"], user["id"], jwt_secret,
                         request.app.config["JWT_EXPIRATION"])
    refresh_token = generate_jwt(request.app.config["SERVICE_NAME"], user["id"], jwt_refresh_secret,
                                 request.app.config["JWT_REFRESH_EXPIRATION"])
    return json({
        "access_token": token,
        "refresh_token": refresh_token
    })


@bp.get("/refresh_access_token")
@doc.summary("Refresh access token")
@doc.description("Use refresh_token in the header to pass authentication")
@doc.consumes({'Authorization': str}, location="header")
@doc.produces({"token": str},
              description="Token",
              content_type="application/json")
@auth(secret_key="JWT_REFRESH_SECRET")
async def refresh_access_token(request: Request):
    """
    Refresh access token
    @param request:
    @return:
    """
    jwt_secret = request.app.config["JWT_SECRET"]
    token = generate_jwt(request.app.config["SERVICE_NAME"], request.ctx.user_id, jwt_secret,
                         request.app.config["JWT_EXPIRATION"])
    return json({
        "access_token": token
    })