"""API for Google Photos OAuth.

Callers subclass this to provide an asyncio implementation that refreshes
authentication tokens.
"""

import logging
from abc import ABC, abstractmethod
from http import HTTPStatus
from typing import Any, TypeVar

import aiohttp
from aiohttp.client_exceptions import ClientError
from mashumaro.mixins.json import DataClassJSONMixin

from .const import LIBRARY_API_URL
from .exceptions import (
    ApiException,
    ApiForbiddenException,
    AuthException,
    NoDataForLocationError,
)
from .model import Error, ErrorResponse

__all__ = ["AbstractAuth"]

_LOGGER = logging.getLogger(__name__)


AUTHORIZATION_HEADER = "Authorization"
CONTENT_TYPE = "Content-Type"
ERROR = "error"
STATUS = "status"
MESSAGE = "message"

_T = TypeVar("_T", bound=DataClassJSONMixin)


class AbstractAuth(ABC):
    """Base class for Google Photos authentication library.

    Provides an asyncio interface around the blocking client library.
    """

    def __init__(self, websession: aiohttp.ClientSession, host: str | None = None):
        """Initialize the auth."""
        self._websession = websession
        self._host = host or LIBRARY_API_URL

    @abstractmethod
    async def async_get_access_token(self) -> str:
        """Return a valid access token."""

    async def request(
        self,
        method: str,
        url: str,
        headers: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> aiohttp.ClientResponse:
        """Make a request."""
        _LOGGER.debug("2")
        try:
            access_token = await self.async_get_access_token()
        except ClientError as err:
            raise AuthException(f"Access token failure: {err}") from err
        _LOGGER.debug("3")
        if headers is None:
            headers = {}
        if AUTHORIZATION_HEADER not in headers:
            headers[AUTHORIZATION_HEADER] = f"Bearer {access_token}"
            headers[CONTENT_TYPE] = "application/json"
        if not (url.startswith("http://") or url.startswith("https://")):
            url = f"{self._host}/{url}"
        _LOGGER.debug("request[%s]=%s %s", method, url, kwargs)
        if method != "get" and "json" in kwargs:
            _LOGGER.debug("request[post json]=%s", kwargs["json"])
        _LOGGER.debug("4")
        test = await self._websession.request(method, url, **kwargs, headers=headers)
        _LOGGER.debug("test: %s", test)
        _LOGGER.debug("headers: %s", headers)
        return await self._websession.request(method, url, **kwargs, headers=headers)

    async def get(self, url: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Make a get request."""
        try:
            resp = await self.request("get", url, **kwargs)
        except ClientError as err:
            raise ApiException(f"Error connecting to API: {err}") from err
        return await AbstractAuth._raise_for_status(resp)

    async def get_json(
        self,
        url: str,
        data_cls: type[_T],
        **kwargs: Any,
    ) -> _T:
        """Make a get request and return json response."""
        resp = await self.get(url, **kwargs)
        try:
            result = await resp.text()
        except ClientError as err:
            raise ApiException("Server returned malformed response") from err
        _LOGGER.debug("response=%s", result)
        try:
            return data_cls.from_json(result)
        except (LookupError, ValueError) as err:
            raise ApiException(f"Server return malformed response: {result}") from err

    async def post(self, url: str, **kwargs: Any) -> aiohttp.ClientResponse:
        """Make a post request."""
        try:
            resp = await self.request("post", url, **kwargs)
        except ClientError as err:
            raise ApiException(f"Error connecting to API: {err}") from err
        return await AbstractAuth._raise_for_status(resp)

    async def post_json(self, url: str, data_cls: type[_T], **kwargs: Any) -> _T:
        """Make a post request and return a json response."""
        resp = await self.post(url, **kwargs)
        try:
            result = await resp.text()
        except ClientError as err:
            raise ApiException("Server returned malformed response") from err
        _LOGGER.debug("response=%s", result)
        return data_cls.from_json(result)
        try:
            return data_cls.from_json(result)
        except (LookupError, ValueError) as err:
            raise ApiException(f"Server return malformed response: {result}") from err

    @classmethod
    async def _raise_for_status(
        cls, resp: aiohttp.ClientResponse
    ) -> aiohttp.ClientResponse:
        """Raise exceptions on failure methods."""
        error_detail = await cls._error_detail(resp)
        try:
            resp.raise_for_status()
        except aiohttp.ClientResponseError as err:
            error_message = f"{err.message} response from API ({resp.status})"
            if error_detail:
                error_message += f": {error_detail}"
                if "Information is unavailable for this location" in error_message:
                    raise NoDataForLocationError(error_message)
            if err.status == HTTPStatus.FORBIDDEN:
                raise ApiForbiddenException(error_message)
            if err.status == HTTPStatus.UNAUTHORIZED:
                raise AuthException(error_message)
            raise ApiException(error_message) from err
        except aiohttp.ClientError as err:
            raise ApiException(f"Error from API: {err}") from err
        return resp

    @classmethod
    async def _error_detail(cls, resp: aiohttp.ClientResponse) -> Error | None:
        """Returns an error message string from the API response."""
        if resp.status < 400:
            return None
        try:
            result = await resp.text()
        except ClientError:
            return None
        try:
            error_response = ErrorResponse.from_json(result)
        except (LookupError, ValueError):
            return None
        return error_response.error
