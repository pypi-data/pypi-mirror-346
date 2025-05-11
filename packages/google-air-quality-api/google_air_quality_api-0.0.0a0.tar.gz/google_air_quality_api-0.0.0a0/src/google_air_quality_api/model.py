"""Google Photos Library API Data Model."""

from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Any, Self
from datetime import datetime
from mashumaro import DataClassDictMixin, field_options
from mashumaro.mixins.json import DataClassJSONMixin

__all__ = [
    "ListMediaItemResult",
    "MediaItem",
    "MediaMetadata",
    "Photo",
    "Video",
    "ContributorInfo",
    "UploadResult",
    "NewMediaItem",
    "SimpleMediaItem",
    "CreateMediaItemsResult",
    "NewMediaItemResult",
    "Status",
    "UserInfoResult",
]


@dataclass
class Concentration(DataClassDictMixin):
    value: float
    units: str


@dataclass
class Pollutant(DataClassDictMixin):
    code: str
    display_name: str = field(metadata={"alias": "displayName"})
    full_name: str = field(metadata={"alias": "fullName"})
    concentration: Concentration


class PollutantList(list[Pollutant]):
    """Ermöglicht Zugriff auf Einträge per Attribut .<code>"""

    def __getattr__(self, name: str) -> Pollutant:
        name = name.lower()
        for pollutant in self:
            if pollutant.code.lower() == name:
                return pollutant
        raise AttributeError(f"No pollutant named {name!r}")


@dataclass
class Color(DataClassDictMixin):
    red: float | None = None
    green: float | None = None
    blue: float | None = None


@dataclass
class Index(DataClassDictMixin):
    code: str
    display_name: str = field(metadata={"alias": "displayName"})
    color: Color
    category: str
    dominant_pollutant: str = field(metadata={"alias": "dominantPollutant"})
    aqi: int | None = None
    aqi_display: str | None = field(default=None, metadata={"alias": "aqiDisplay"})


class IndexList(list[Index]):
    """Ermöglicht Zugriff auf Einträge per Attribut .<code>"""

    def __getattr__(self, name: str) -> Index:
        name = name.lower()
        for idx in self:
            if idx.code.lower() == name:
                return idx
        raise AttributeError(f"No index named {name!r}")


@dataclass
class AirQualityData(DataClassJSONMixin):
    date_time: datetime = field(metadata={"alias": "dateTime"})
    region_code: str = field(metadata={"alias": "regionCode"})
    _indexes: list[Index] = field(metadata={"alias": "indexes"})
    _pollutants: list[Pollutant] = field(metadata={"alias": "pollutants"})

    @property
    def indexes(self) -> IndexList:
        """Gibt bei jedem Zugriff eine IndexList zurück."""
        return IndexList(self._indexes)

    @property
    def pollutants(self) -> PollutantList:
        return PollutantList(self._pollutants)


@dataclass
class UserInfoResult(DataClassJSONMixin):
    """Response from getting user info."""

    id: str
    """User ID."""

    name: str
    """User name."""


@dataclass
class Error:
    """Error details from the API response."""

    status: str | None = None
    code: int | None = None
    message: str | None = None
    details: list[dict[str, Any]] | None = field(default_factory=list)

    def __str__(self) -> str:
        """Return a string representation of the error details."""
        error_message = ""
        if self.status:
            error_message += self.status
        if self.code:
            if error_message:
                error_message += f" ({self.code})"
            else:
                error_message += str(self.code)
        if self.message:
            if error_message:
                error_message += ": "
            error_message += self.message
        if self.details:
            error_message += f"\nError details: ({self.details})"
        return error_message


@dataclass
class ErrorResponse(DataClassJSONMixin):
    """A response message that contains an error message."""

    error: Error | None = None
