"""
This module provides function to create Sanic application
"""

import aioredis
import sentry_sdk
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
    app.db_client = DatabaseClient()
    app.redis_client = await aioredis.create_redis_pool(app.config["REDIS_URL"])
    sentry_sdk.init(
        dsn=app.config["SENTRY_DSN"],
        environment=app.config["ENV"],
        integrations=[
            SanicIntegration(),
            AioHttpIntegration(),
            SqlalchemyIntegration(),
        ],
    )


async def after_server_stop(app: Sanic):
    """
    After server stop
    @param app:
    @return:
    """
    app.redis_client.close()
    await app.redis_client.wait_closed()


def create_app(default_settings: str = "application/setting/env.py") -> Sanic:
    """
    Create instance
    @param default_settings:
    @return:
    """
    app = Sanic(__name__)
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
