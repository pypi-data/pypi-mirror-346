"""API for Google Photos bound to Home Assistant OAuth.

Callers subclass this to provide an asyncio implementation that handles
refreshing authentication tokens. You then pass in the auth object to the
GooglePhotosLibraryApi object to make authenticated calls to the Google Photos
Library API.

Example usage:
```python
from aiohttp import ClientSession
from google_air_quality_api import api
from google_air_quality_api import auth

class GooglePhotosAuth(auth.AbstractAuth):
    '''Provide OAuth for Google Photos.'''

    async def async_get_access_token(self) -> str:
        # Your auth implementation details are here

# Create a client library
auth = GooglePhotosAuth()
api = api.GooglePhotosLibraryApi(auth)

# Upload content
with open("image.jpg", "rb") as fd:
    upload_result = await api.upload_content(fd.read(), "image/jpeg")

# Create a media item
await api.create_media_items([
    NewMediaItem(SimpleMediaItem(upload_token=upload_result.upload_token))
])

# List all media items created by this application
result = await api.list_media_items()
for item in result.media_items:
    print(item.id)
```

"""

import logging
from typing import Any

from aiohttp.client_exceptions import ClientError

from .auth import AbstractAuth
from .exceptions import GooglePhotosApiError
from .model import UserInfoResult, AirQualityData

__all__ = [
    "GooglePhotosLibraryApi",
]


_LOGGER = logging.getLogger(__name__)

DEFAULT_PAGE_SIZE = 20

# Only included necessary fields to limit response sizes
GET_MEDIA_ITEM_FIELDS = (
    "id,baseUrl,mimeType,filename,mediaMetadata(width,height,photo,video)"
)
LIST_MEDIA_ITEM_FIELDS = f"nextPageToken,mediaItems({GET_MEDIA_ITEM_FIELDS})"
GET_ALBUM_FIELDS = "id,title,coverPhotoBaseUrl,coverPhotoMediaItemId"
LIST_ALBUMS_FIELDS = f"nextPageToken,albums({GET_ALBUM_FIELDS})"
USERINFO_API = "https://www.googleapis.com/oauth2/v1/userinfo"


class GooglePhotosLibraryApi:
    """The Google Photos library api client."""

    def __init__(self, auth: AbstractAuth) -> None:
        """Initialize GooglePhotosLibraryApi."""
        self._auth = auth

    async def get_media_item(self, lat, long) -> AirQualityData:
        """Get all MediaItem resources."""
        _LOGGER.debug("get_media_item")
        payload = {
            "location": {"latitude": lat, "longitude": long},
            "extraComputations": [
                "LOCAL_AQI",
                "POLLUTANT_CONCENTRATION",
            ],
            "customLocalAqis": [
                {"regionCode": "DE", "aqi": "USA_EPA_NOWCAST"},
            ],
            "universalAqi": True,
        }
        return await self._auth.post_json(
            "https://airquality.googleapis.com/v1/currentConditions:lookup",
            json=payload,
            data_cls=AirQualityData,
        )

    async def get_user_info(self) -> UserInfoResult:
        """Get the user profile info.

        This call requires the userinfo.email scope.
        """
        return await self._auth.get_json(USERINFO_API, data_cls=UserInfoResult)
