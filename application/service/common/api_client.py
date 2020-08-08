"""
This module includes the BaseApiClient
"""
from typing import Any, Dict, Optional

import aiohttp
from aiohttp import ServerConnectionError, ServerDisconnectedError, ServerTimeoutError
from sanic.exceptions import SanicException
from tenacity import retry, retry_if_exception_type, stop_after_attempt

from application.util.exception import ApiServerError


class BaseApiClient:
    """Base API Client
    """

    @retry(
        stop=stop_after_attempt(3),
        retry=(
            retry_if_exception_type(ServerConnectionError)
            | retry_if_exception_type(ServerDisconnectedError)
            | retry_if_exception_type(ServerTimeoutError)
            | retry_if_exception_type(ApiServerError)
        ),
    )
    async def _request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[Any, Any]] = None,
        headers: Optional[Dict[Any, Any]] = None,
        json: Optional[Dict[Any, Any]] = None,
        timeout: int = 30,
    ) -> Any:
        """
        Make request and return response in json format
        :param method:
        :param url:
        :param params:
        :param headers:
        :param json:
        :param timeout:
        :return:
        """
        aio_timeout = aiohttp.ClientTimeout(total=timeout)
        async with aiohttp.ClientSession(timeout=aio_timeout) as session:
            async with session.request(
                method=method, url=url, params=params, headers=headers, json=json
            ) as response:
                status = response.status
                if response.content_type == "application/json":
                    response_text = await response.json()
                else:
                    response_text = await response.text()
                if status >= 400:
                    if status in (500, 502, 503, 504, 509):
                        raise ApiServerError(response_text, status)
                    raise SanicException(response_text, status)
                return response_text

    async def get_json(
        self,
        url: str,
        params: Optional[Dict[Any, Any]] = None,
        headers: Optional[Dict[Any, Any]] = None,
        timeout: int = 30,
    ) -> Any:
        """
        Make get request and return response in json format
        :param url:
        :param params:
        :param headers:
        :param timeout:
        :return:
        """
        return await self._request(
            method="get", url=url, params=params, headers=headers, timeout=timeout
        )

    async def post_json(
        self,
        url: str,
        json: Optional[Dict[Any, Any]] = None,
        headers: Optional[Dict[Any, Any]] = None,
        timeout: int = 30,
    ) -> Any:
        """
        Make post request and return response in json format
        :param url:
        :param json:
        :param headers:
        :param timeout:
        :return:
        """
        return await self._request(
            method="post", url=url, json=json, headers=headers, timeout=timeout
        )
