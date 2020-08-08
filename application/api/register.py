"""
This module registers all api endpoints
"""

from sanic import Blueprint, Sanic

from application.api.health_check import bp as health_check
from application.api.v1.auth.blueprint import bp as auth


def register_blueprints(app: Sanic):
    """
    Register api endpoints
    @param app:
    @return:
    """
    v1 = Blueprint.group(auth, health_check)
    app.blueprint(v1)
