"""
This module includes functions to do authentication.
"""

import logging
import time
from functools import wraps
from typing import Callable, List, Optional

import jwt
from aioredis import Redis
from sanic.exceptions import Unauthorized
from sanic.request import Request

from application.repository.role import RoleRepository
from application.service.db_client.client import DatabaseClient
from application.util.constant import ACTIVE_ROLES, CacheKey

logger = logging.getLogger(__name__)


def generate_jwt(issuer: str, subject: str, secret: str, expiration: int) -> bytes:
    """
    Generate JWT
    @param issuer:
    @param subject:
    @param secret:
    @param expiration:
    @return:
    """
    now: int = int(time.time())
    payload: dict = {
        "iss": issuer,
        "sub": subject,
        "exp": now + expiration,
        "iat": now,
        "nbf": now,
    }
    return jwt.encode(payload, secret)


def authenticate(request: Request, secret: str):
    """
    Authenticate jwt against secret
    @param request:
    @param secret:
    @return:
    """
    token = request.headers.get("Authorization")
    if token is None:
        raise Unauthorized('Missing JWT')
    try:
        payload = jwt.decode(
            token, secret, algorithms=["HS256"], options=dict(require_exp=True)
        )
    except (
        jwt.ExpiredSignatureError,
        jwt.DecodeError,
        jwt.MissingRequiredClaimError,
    ) as ex:
        raise Unauthorized(str(ex))
    request.ctx.token = token
    request.ctx.user_id = int(payload["sub"])


async def authorize(request: Request, roles: Optional[List[str]]):
    """
    Authorize user role against roles
    @param request:
    @param roles:
    @return:
    """
    if not roles:
        roles = ACTIVE_ROLES
    redis_client: Redis = request.app.redis_client
    db_client: DatabaseClient = request.app.db_client
    user_id: int = request.ctx.user_id
    cached_role: str = await redis_client.get(
        CacheKey.user_role(user_id), encoding="utf-8"
    )
    if cached_role:
        if cached_role not in roles:
            raise Unauthorized("Unauthorized")
        return
    role_repo: RoleRepository = RoleRepository(db_client)
    role = role_repo.find_by_user_id(user_id)
    if not role or role["name"] not in roles:
        raise Unauthorized("Unauthorized")
    await redis_client.set(CacheKey.user_role(user_id), role["name"], expire=3600)


def auth(secret_key: str = "JWT_SECRET", roles: Optional[List[str]] = None) -> Callable:
    """
    Decorator to do authentication against secret and authorization against roles.
    @param secret_key:
    @param roles:
    @return:
    """
    if not roles:
        roles = ACTIVE_ROLES

    def real_auth_decorator(endpoint):
        @wraps(endpoint)
        async def wrapper(request: Request, *args, **kwargs):
            authenticate(request, request.app.config[secret_key])
            await authorize(request, roles)
            return await endpoint(request, *args, **kwargs)

        return wrapper

    return real_auth_decorator
