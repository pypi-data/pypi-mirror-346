#
# AI-on-Rails: All rights reserved.
#
"""Execute requests through the AI-on-Rails proxy API."""

import json
import time
import uuid
from enum import Enum
from typing import Dict, Any, List, Optional, Union
from requests_toolbelt.multipart import encoder

import requests

from aor.backend.config import (
    get_api_url,
    get_a2a_timeout,
    get_request_timeout,
    is_debug_enabled,
)
from aor.backend.exceptions import RequestError, ResponseParsingError
from aor.backend.response import TextResponseParser
from aor.utils.ui import ui


class ProtocolType(Enum):
    """Protocol types supported by the API."""

    A2A = "a2a"
    REST = "rest"
    BASIC = "basic"  # multipart/form-data


class ExecuteRequest:
    """Execute a request through the AI-on-Rails proxy API."""

    def __init__(
        self,
        token: str,
        app_uuid: str,
        endpoint_uuid: str,
        inputs: Dict[str, str],
        protocol: Optional[ProtocolType] = None,
        debug: Optional[bool] = None,
    ):
        """Initialize the execute request.

        Args:
            token: Authentication token
            app_uuid: Public UUID of the app
            endpoint_uuid: Public UUID of the endpoint
            inputs: Dictionary of input name to input value
            protocol: Protocol type to use (auto-detected if not specified)
            debug: Whether to enable debug mode (overrides global setting)
        """
        self.token = token.strip() if token else ""
        self.app_uuid = app_uuid
        self.endpoint_uuid = endpoint_uuid
        self.inputs = inputs
        self.protocol = protocol
        self.debug = debug if debug is not None else is_debug_enabled()

        # Generate unique IDs for the request
        self.request_id = str(uuid.uuid4())
        self.params_id = str(uuid.uuid4())
        self.session_id = str(uuid.uuid4())

        # Create response parser
        self.response_parser = TextResponseParser(self.debug)

    def build_a2a_request(self) -> Dict[str, Any]:
        """Build an A2A protocol request.

        Returns:
            The A2A request as a dictionary
        """
        # Create parts for each input
        parts = []
        for name, value in self.inputs.items():
            parts.append({"type": "text", "text": value, "metadata": {"name": name}})

        # Build the A2A request
        return {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tasks/send",
            "params": {
                "id": self.params_id,
                "sessionId": self.session_id,
                "message": {"role": "user", "parts": parts, "metadata": None},
                "acceptedOutputModes": ["text"],
                "pushNotification": None,
                "historyLength": None,
                "metadata": None,
            },
        }

    def build_rest_request(self) -> Dict[str, Any]:
        """Build a REST protocol request.

        Returns:
            The REST request as a dictionary
        """
        # For REST, we just send the inputs directly
        return {"inputs": self.inputs}

    def build_multipart_request(self) -> bytes:
        """Build a multipart/form-data request.

        Returns:
            The multipart request as bytes
        """
        # For multipart/form-data, we encode the inputs as form fields
        return encoder.MultipartEncoder(self.inputs).to_string()

    def get_url(self) -> str:
        """Get the URL for the request.

        Returns:
            The URL for the request
        """
        protocol_path = self.protocol.value if self.protocol else "a2a"
        return f"{get_api_url()}/{protocol_path}/{self.app_uuid}/{self.endpoint_uuid}"

    def get_headers(self) -> Dict[str, str]:
        """Get the headers for the request.

        Returns:
            The headers for the request
        """
        headers = {}

        # Set content type based on protocol
        if not self.protocol or self.protocol in [ProtocolType.A2A, ProtocolType.REST]:
            headers["Content-Type"] = "application/json"
        elif self.protocol == ProtocolType.BASIC:
            # For multipart/form-data, the content type is set by the encoder
            multipart_data = encoder.MultipartEncoder(self.inputs)
            headers["Content-Type"] = multipart_data.content_type

        # Add authorization if token is provided
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    def get_request_data(self) -> Union[Dict[str, Any], bytes]:
        """Get the request data based on the protocol.

        Returns:
            The request data
        """
        if not self.protocol or self.protocol == ProtocolType.A2A:
            return self.build_a2a_request()
        elif self.protocol == ProtocolType.REST:
            return self.build_rest_request()
        elif self.protocol == ProtocolType.BASIC:
            return self.build_multipart_request()
        else:
            raise ValueError(f"Unsupported protocol: {self.protocol}")

    def send(self) -> Dict[str, Any]:
        """Send the request to the API.

        Returns:
            The response from the API

        Raises:
            RequestError: If the request fails
            ResponseParsingError: If parsing the response fails
        """
        # Build the request
        url = self.get_url()
        headers = self.get_headers()
        request_data = self.get_request_data()

        ui.debug(f"Executing request to {url}")
        
        try:
            # Send the request
            if isinstance(request_data, dict):
                # JSON request
                response = requests.post(
                    url,
                    json=request_data,
                    headers=headers,
                    timeout=(
                        get_a2a_timeout()
                        if self.protocol == ProtocolType.A2A
                        else get_request_timeout()
                    ),
                )
            else:
                # Multipart request
                response = requests.post(
                    url,
                    data=request_data,
                    headers=headers,
                    timeout=get_request_timeout(),
                )
            
            ui.debug(f"Received response with status code {response.status_code}")

            # Check for errors
            if response.status_code != 200:
                error_message = f"Request failed with status code {response.status_code}: {response.text}"

                # Add more context for specific error types
                try:
                    error_data = json.loads(response.text)
                    if isinstance(error_data, dict) and "error" in error_data:
                        if error_data["error"] == "Invalid resource":
                            error_message = (
                                f"Request failed with status code {response.status_code}: {response.text}\n"
                                f"The app UUID '{self.app_uuid}' or endpoint UUID '{self.endpoint_uuid}' "
                                f"could not be found on the server."
                            )
                except (json.JSONDecodeError, KeyError):
                    pass
                
                # Add specific handling for 502 errors
                if response.status_code == 502:
                    error_message = (
                        f"Request failed with status code 502: {response.text}\n"
                        f"The server encountered an internal error while processing your request.\n"
                        f"This could be due to temporary server issues, network problems, "
                        f"or an issue with the request format."
                    )
                    
                    # Log additional debug information
                    ui.debug(f"Request URL: {url}")
                    ui.debug(f"Request headers: {headers}")
                    ui.debug(f"Request data: {request_data}")

                raise RequestError(error_message, response.status_code, response.text)

            # Parse the response
            try:
                response_json = response.json()
                return response_json
            except json.JSONDecodeError:
                error_message = f"Failed to parse response as JSON: {response.text}"
                raise ResponseParsingError(error_message, response.text)
                
        except requests.exceptions.RequestException as e:
            # Raise the error
            error_message = f"Request error: {str(e)}"
            raise RequestError(error_message)

    def send_with_error_handling(self) -> Dict[str, Any]:
        """Send the request and handle errors by returning an error dictionary.

        Returns:
            The parsed response or an error dictionary
        """
        try:
            return self.send()
        except (RequestError, ResponseParsingError) as e:
            return {
                "error": True,
                "message": str(e),
                "details": getattr(e, "details", {}),
            }

    def extract_response_text(self, response_data: Dict[str, Any]) -> List[str]:
        """Extract text from the response.

        Args:
            response_data: The response data

        Returns:
            List of text responses
        """
        return self.response_parser.extract_text(response_data)


def detect_protocol(endpoint_data: Dict[str, Any]) -> ProtocolType:
    """Detect the protocol type from endpoint data.

    Args:
        endpoint_data: The endpoint data

    Returns:
        The detected protocol type
    """
    protocol_str = endpoint_data.get("protocol", "").lower()

    if protocol_str == "a2a":
        return ProtocolType.A2A
    elif protocol_str == "rest":
        return ProtocolType.REST
    elif protocol_str == "basic":
        return ProtocolType.BASIC
    else:
        # Default to A2A if unknown
        return ProtocolType.A2A