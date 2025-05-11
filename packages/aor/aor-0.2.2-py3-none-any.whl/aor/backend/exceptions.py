#
# AI-on-Rails: All rights reserved.
#
"""Custom exceptions for the backend module."""

from typing import Optional, Dict, Any


class BackendError(Exception):
    """Base exception for all backend errors."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        self.message = message
        self.details = details or {}
        super().__init__(message)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the exception to a dictionary for API responses."""
        return {"error": True, "message": self.message, "details": self.details}


class RequestError(BackendError):
    """Exception raised when a request to the backend fails."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_text: Optional[str] = None,
    ):
        details = {}
        if status_code is not None:
            details["status_code"] = status_code
        if response_text is not None:
            details["response_text"] = response_text
        super().__init__(message, details)


class ResponseParsingError(BackendError):
    """Exception raised when parsing a response from the backend fails."""

    def __init__(self, message: str, response_text: Optional[str] = None):
        details = {}
        if response_text is not None:
            details["response_text"] = response_text
        super().__init__(message, details)


class ValidationError(BackendError):
    """Exception raised when validation of request or response data fails."""

    def __init__(
        self, message: str, validation_errors: Optional[Dict[str, Any]] = None
    ):
        details = {}
        if validation_errors is not None:
            details["validation_errors"] = validation_errors
        super().__init__(message, details)


class AuthenticationError(BackendError):
    """Exception raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message)
