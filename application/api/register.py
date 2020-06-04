"""
This module registers all api endpoints
"""

from sanic import Blueprint
from sanic import Sanic

from application.api.v1.auth.blueprint import bp


def register_blueprints(app: Sanic):
    """
    Register api endpoints
    @param app:
    @return:
    """
    v1 = Blueprint.group(bp, url_prefix="/api/mono")
    app.blueprint(v1)
