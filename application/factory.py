"""
This module provides function to create Sanic application
"""
import sentry_sdk
from redis import asyncio as aioredis
from sanic import Sanic
from sanic.exceptions import SanicException
from sanic_compress import Compress
from sanic_openapi import swagger_blueprint
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.sanic import SanicIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

from application.api.error_handler import error_handler
from application.api.register import register_blueprints
from application.service.common.db_client import DatabaseClient, DatabaseEngineManager
from application.service.common.thrift_client import ThriftClientFactory
from application.thrifts.services.user import UserService


async def before_server_start(app: Sanic):
    """
    Before server start
    @param app:
    @return:
    """
    DatabaseEngineManager.create_engines(
        primary_db_urls=[app.config["PRIMARY_DB_URL"]],
        replica_db_urls=[app.config["REPLICA_DB_URL"]],
    )

    app.ctx.db_client = DatabaseClient()
    app.ctx.redis_client = aioredis.ConnectionPool(app.config["REDIS_URL"])
    sentry_sdk.init(
        dsn=app.config["SENTRY_DSN"],
        environment=app.config["ENV"],
        integrations=[
            SanicIntegration(),
            AioHttpIntegration(),
            SqlalchemyIntegration(),
        ],
    )
    # Thrift services
    app.ctx.transports = []
    user_service_transport, user_service_client = ThriftClientFactory.createUserServiceClient("localhost", 9090)
    app.ctx.transports.append(user_service_transport)
    app.ctx.user_service_client = user_service_client
    for transport in app.ctx.transports:
        transport.open()


async def after_server_stop(app: Sanic):
    """
    After server stop
    @param app:
    @return:
    """
    await app.ctx.redis_client.disconnect()
    for transport in app.ctx.transports:
        if transport.isOpen():
            transport.close()


def create_app(default_settings: str = "application/setting/env.py") -> Sanic:
    """
    Create instance
    @param default_settings:
    @return:
    """
    app = Sanic("Mono")
    Compress(app)
    app.update_config(default_settings)
    # app.blueprint(swagger_blueprint)
    register_blueprints(app)
    app.error_handler.add(SanicException, error_handler)

    @app.listener('before_server_start')
    async def _before_server_start(_app, loop):
        await before_server_start(_app)

    @app.listener('after_server_stop')
    async def _after_server_stop(_app, loop):
        await after_server_stop(_app)

    return app
