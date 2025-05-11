#
# AI-on-Rails: All rights reserved.
#
"""Backend module for AI-on-Rails."""

from aor.backend.config import (
    configure,
    get_api_url,
    get_request_timeout,
    get_a2a_timeout,
    is_debug_enabled,
)
from aor.backend.exceptions import (
    BackendError,
    RequestError,
    ResponseParsingError,
    ValidationError,
    AuthenticationError,
)
from aor.backend.request import Request
from aor.backend.response import ResponseParser, TextResponseParser, ResponseValidator
from aor.backend.resolve import Resolve
from aor.backend.execute import ExecuteRequest
from aor.backend.application import ApplicationManager, CreateApp, UpdateApp, DeleteApp
from aor.utils.ui import ui
from aor.backend.endpoint import (
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
