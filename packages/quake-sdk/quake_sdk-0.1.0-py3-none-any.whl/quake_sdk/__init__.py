"""
Quake API Python SDK
"""
from .client import QuakeClient
from .exceptions import (
    QuakeAPIException,
    QuakeAuthException,
    QuakeRateLimitException,
    QuakeInvalidRequestException,
    QuakeServerException
)
from .models import (
    # Request Models
    RealtimeSearchQuery,
    ScrollSearchQuery,
    AggregationQuery,
    FaviconSimilarityQuery,
    # Response Data Models (core data part of responses)
    UserInfoData,
    QuakeService,
    QuakeHost,
    AggregationBucket,
    SimilarIconData,
    Location,
    Component,
    ServiceData,
    # Specific Service Info Models (examples)
    HttpServiceInfo,
    FtpServiceInfo,
    SshServiceInfo,
    # Full Response Wrappers
    UserInfoResponse,
    FilterableFieldsResponse,
    ServiceSearchResponse,
    ServiceScrollResponse,
    ServiceAggregationResponse,
    HostSearchResponse,
    HostScrollResponse,
    HostAggregationResponse,
    SimilarIconResponse
)

__version__ = "0.2.0" # Bump version due to significant changes

__all__ = [
    "QuakeClient",
    # Exceptions
    "QuakeAPIException",
    "QuakeAuthException",
    "QuakeRateLimitException",
    "QuakeInvalidRequestException",
    "QuakeServerException",
    # Request Models
    "RealtimeSearchQuery",
    "ScrollSearchQuery",
    "AggregationQuery",
    "FaviconSimilarityQuery",
    # Response Data Models
    "UserInfoData",
    "QuakeService",
    "QuakeHost",
    "AggregationBucket",
    "SimilarIconData",
    "Location",
    "Component",
    "ServiceData",
    "HttpServiceInfo",
    "FtpServiceInfo",
    "SshServiceInfo",
    # Full Response Wrappers
    "UserInfoResponse",
    "FilterableFieldsResponse",
    "ServiceSearchResponse",
    "ServiceScrollResponse",
    "ServiceAggregationResponse",
    "HostSearchResponse",
    "HostScrollResponse",
    "HostAggregationResponse",
    "SimilarIconResponse",
]
