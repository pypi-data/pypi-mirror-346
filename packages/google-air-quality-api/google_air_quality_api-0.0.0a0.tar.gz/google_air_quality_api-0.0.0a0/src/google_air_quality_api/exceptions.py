"""Exceptions for Google Photos API calls."""


class GooglePhotosApiError(Exception):
    """Error talking to the Google Photos API."""


class ApiException(GooglePhotosApiError):
    """Raised during problems talking to the API."""


class AuthException(GooglePhotosApiError):
    """Raised due to auth problems talking to API."""


class ApiForbiddenException(GooglePhotosApiError):
    """Raised due to permission errors talking to API."""


class NoDataForLocationError(GooglePhotosApiError):
    """Raised due to permission errors talking to API."""
