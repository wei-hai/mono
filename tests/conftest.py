"""
Config for test cases
"""
import pytest
from pytest_sanic.utils import TestClient
from sanic import Sanic

from application.factory import create_app


@pytest.yield_fixture
def app():
    """
    application fixture
    :return:
    """
    application = create_app()
    yield application


@pytest.fixture
def test_cli(
    loop, app: Sanic, sanic_client: TestClient
):  # pylint: disable=redefined-outer-name
    """
    Test client
    :param loop:
    :param app:
    :param sanic_client:
    :return:
    """
    return loop.run_until_complete(sanic_client(app))
