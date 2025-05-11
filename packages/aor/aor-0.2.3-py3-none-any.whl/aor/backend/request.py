#
# AI-on-Rails: All rights reserved.
#
"""Base request handling for the AI-on-Rails backend."""

import json
from typing import Dict, Any, Optional, Union

import requests

from aor.backend.config import get_api_url, get_request_timeout, is_debug_enabled
from aor.backend.exceptions import RequestError, ResponseParsingError
from aor.utils.ui import ui


class Request:
    """Base class for all requests to the AI-on-Rails backend."""

    def __init__(self, token: str, uri: str, body: Dict[str, Any]):
        """Initialize a request.

        Args:
            token: Authentication token
            uri: The URI path for the request
            body: The request body
        """
        self.token = token.strip() if token else ""
        self.uri = uri
        self.body = {**body}

        # Add token to body if provided
        if self.token:
            self.body["token"] = self.token

    def get_url(self) -> str:
        """Get the full URL for the request.

        Returns:
            The full URL
        """
        return f"{get_api_url()}/{self.uri}"

    def get_headers(self) -> Dict[str, str]:
        """Get the headers for the request.

        Returns:
            The request headers
        """
        return {
            "Content-Type": "application/json",
        }

    def handle_error_response(self, response: requests.Response) -> None:
        """Handle an error response.

        Args:
            response: The response object

        Raises:
            RequestError: If the request failed
        """
        error_message = f"Request failed with status code {response.status_code}"

        try:
            response_text = response.text
            # Try to parse as JSON for more detailed error
            error_data = json.loads(response_text)
            if isinstance(error_data, dict):
                if "message" in error_data:
                    error_message = error_data["message"]

                # Log additional error details in debug mode
                if is_debug_enabled():
                    ui.debug(
                        f"Error response details: {json.dumps(error_data, indent=2)}"
                    )

                    # Extract validation errors if present
                    if "errors" in error_data:
                        ui.debug(
                            f"Validation errors: {json.dumps(error_data['errors'], indent=2)}"
                        )
                    elif "error" in error_data and isinstance(
                        error_data["error"], dict
                    ):
                        ui.debug(
                            f"Error details: {json.dumps(error_data['error'], indent=2)}"
                        )
        except (json.JSONDecodeError, KeyError):
            # If parsing fails, use the raw response text
            response_text = response.text
            if is_debug_enabled():
                ui.debug(f"Could not parse error response as JSON: {response_text}")

        raise RequestError(error_message, response.status_code, response_text)

    def parse_response(self, response: requests.Response) -> Dict[str, Any]:
        """Parse the response.

        Args:
            response: The response object

        Returns:
            The parsed response

        Raises:
            ResponseParsingError: If parsing the response fails
        """
        try:
            if response.headers.get("content-type") != "application/json":
                raise ResponseParsingError(
                    f"Unexpected content type: {response.headers.get('content-type')}",
                    response.text,
                )

            return response.json()
        except json.JSONDecodeError:
            raise ResponseParsingError(
                "Failed to parse response as JSON", response.text
            )

    def send(self) -> Dict[str, Any]:
        """Send the request and return the response.

        Returns:
            The parsed response

        Raises:
            RequestError: If the request fails
            ResponseParsingError: If parsing the response fails
        """
        url = self.get_url()
        headers = self.get_headers()

        ui.debug(f"Sending request to {url}")

        # Log detailed request information in debug mode
        if is_debug_enabled():
            ui.debug(f"Request headers: {headers}")
            # Create a copy of the body to avoid modifying the original
            body_copy = self.body.copy()
            # Mask token if present for security
            if "token" in body_copy:
                body_copy["token"] = "***MASKED***"
            ui.debug(f"Request body: {json.dumps(body_copy, indent=2)}")

        try:
            response = requests.post(
                url,
                json=self.body,
                headers=headers,  # TODO(clairbee): add this some day: timeout=get_request_timeout()
            )

            ui.debug(f"Received response with status code {response.status_code}")

            # Log detailed response information in debug mode
            if is_debug_enabled():
                ui.debug(f"Response headers: {dict(response.headers)}")
                try:
                    # Try to parse and pretty-print JSON response
                    response_body = response.json()
                    ui.debug(f"Response body: {json.dumps(response_body, indent=2)}")
                except json.JSONDecodeError:
                    # If not JSON, log the raw text
                    ui.debug(f"Response body (raw): {response.text}")

            # Check for errors
            if response.status_code != 200:
                self.handle_error_response(response)

            # Parse the response
            return self.parse_response(response)

        except requests.exceptions.RequestException as e:
            ui.error(f"Request error: {str(e)}")
            raise RequestError(f"Request error: {str(e)}")

    def send_with_error_handling(self) -> Dict[str, Any]:
        """Send the request and handle errors by returning an error dictionary.

        This is useful for UI-facing requests where we want to display errors
        rather than raising exceptions.

        Returns:
            The parsed response or an error dictionary
        """
        try:
            return self.send()
        except (RequestError, ResponseParsingError) as e:
            ui.error(f"Request failed: {str(e)}")
            return e.to_dict()
