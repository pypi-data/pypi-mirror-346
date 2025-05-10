#
# AI-on-Rails: All rights reserved.
#
"""Backend module for AI-on-Rails."""

from backend.config import (
    configure,
    get_api_url,
    get_request_timeout,
    get_a2a_timeout,
    is_debug_enabled,
)
from backend.exceptions import (
    BackendError,
    RequestError,
    ResponseParsingError,
    ValidationError,
    AuthenticationError,
)
from backend.request import Request
from backend.response import ResponseParser, TextResponseParser, ResponseValidator
from backend.resolve import Resolve
from backend.execute import ExecuteRequest
from backend.application import ApplicationManager, CreateApp, UpdateApp, DeleteApp
from ui import ui
from backend.endpoint import (
    EndpointManager,
    CreateEndpoint,
    UpdateEndpoint,
    DeleteEndpoint,
    # Legacy aliases for backward compatibility
    CreateAgent,
    UpdateAgent,
    DeleteAgent,
)

__all__ = [
    # Config
    "configure",
    "get_api_url",
    "get_request_timeout",
    "get_a2a_timeout",
    "is_debug_enabled",
    # UI
    "ui",
    # Exceptions
    "BackendError",
    "RequestError",
    "ResponseParsingError",
    "ValidationError",
    "AuthenticationError",
    # Request/Response
    "Request",
    "ResponseParser",
    "TextResponseParser",
    "ResponseValidator",
    # Core functionality
    "Resolve",
    "ExecuteRequest",
    # Application management
    "ApplicationManager",
    "CreateApp",
    "UpdateApp",
    "DeleteApp",
    # Endpoint management
    "EndpointManager",
    "CreateEndpoint",
    "UpdateEndpoint",
    "DeleteEndpoint",
    # Legacy aliases
    "CreateAgent",
    "UpdateAgent",
    "DeleteAgent",
]
