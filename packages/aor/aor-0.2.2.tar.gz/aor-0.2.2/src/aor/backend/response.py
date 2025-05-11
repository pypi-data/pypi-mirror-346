#
# AI-on-Rails: All rights reserved.
#
"""Response handling utilities for the backend module."""

from typing import Dict, Any, List, Optional, Union, Callable
import json
from aor.utils.ui import ui


class ResponseParser:
    """Base class for parsing API responses."""

    def parse(self, response_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the response data.

        Args:
            response_data: The response data to parse

        Returns:
            The parsed response data
        """
        return response_data


class TextResponseParser:
    """Parser for extracting text from various response formats."""

    def __init__(self, debug: bool = False):
        """Initialize the text response parser.

        Args:
            debug: Whether to enable debug logging
        """
        self.debug = debug

    def extract_text(self, response_data: Dict[str, Any]) -> List[str]:
        """Extract text from the response.

        Args:
            response_data: The response data

        Returns:
            List of text responses
        """
        ui.debug(f"Extracting text from response")

        result = []

        # Try different response formats in order of preference
        if result := self._extract_a2a_format(response_data):
            return result

        if result := self._extract_outputs_format(response_data):
            return result

        if result := self._extract_direct_response(response_data):
            return result

        # If no structured format is found, try to extract any text field
        if not result:
            result = self._extract_text_fields(response_data)

        # If still no result, just convert the whole response to a string
        if not result:
            result.append(json.dumps(response_data, indent=2))

        return result

    def _extract_a2a_format(self, data: Dict[str, Any]) -> List[str]:
        """Extract text from A2A format response.

        Args:
            data: The response data

        Returns:
            List of extracted text
        """
        result = []

        # Format: A2A format with result.message.parts
        if "result" in data and "message" in data["result"]:
            message = data["result"]["message"]
            if "parts" in message:
                for part in message["parts"]:
                    if part.get("type") == "text":
                        result.append(part.get("text", ""))

        return result

    def _extract_outputs_format(self, data: Dict[str, Any]) -> List[str]:
        """Extract text from outputs format response.

        Args:
            data: The response data

        Returns:
            List of extracted text
        """
        result = []

        # Format: Simple response with outputs
        if "outputs" in data:
            outputs = data["outputs"]
            if isinstance(outputs, dict):
                for key, value in outputs.items():
                    result.append(f"{key}: {value}")
            elif isinstance(outputs, list):
                for item in outputs:
                    if isinstance(item, str):
                        result.append(item)
                    elif isinstance(item, dict) and "text" in item:
                        result.append(item["text"])

        return result

    def _extract_direct_response(self, data: Dict[str, Any]) -> List[str]:
        """Extract text from direct response field.

        Args:
            data: The response data

        Returns:
            List of extracted text
        """
        result = []

        # Format: Direct response field (check for default output first)
        if "default" in data:
            response = data["default"]
            if isinstance(response, str):
                result.append(response)
            elif isinstance(response, dict) and "text" in response:
                result.append(response["text"])
        # For backward compatibility, also check for legacy response field
        elif "response" in data:
            response = data["response"]
            if isinstance(response, str):
                result.append(response)
            elif isinstance(response, dict) and "text" in response:
                result.append(response["text"])

        return result

    def _extract_text_fields(self, data: Dict[str, Any], prefix: str = "") -> List[str]:
        """Recursively extract text fields from the response.

        Args:
            data: The response data
            prefix: The current path prefix for nested fields

        Returns:
            List of extracted text
        """
        result = []

        def extract_recursive(data, prefix=""):
            if isinstance(data, dict):
                for key, value in data.items():
                    if key in ["text", "content", "message"] and isinstance(value, str):
                        result.append(value)
                    elif isinstance(value, (dict, list)):
                        extract_recursive(value, f"{prefix}.{key}" if prefix else key)
            elif isinstance(data, list):
                for i, item in enumerate(data):
                    extract_recursive(item, f"{prefix}[{i}]")

        extract_recursive(data, prefix)
        return result


class ResponseValidator:
    """Validate API responses."""

    @staticmethod
    def validate_status(
        response: Dict[str, Any], valid_statuses: List[str] = None
    ) -> bool:
        """Validate the status of a response.

        Args:
            response: The response to validate
            valid_statuses: List of valid status values (default: ["success"])

        Returns:
            True if the status is valid, False otherwise
        """
        if valid_statuses is None:
            valid_statuses = ["success"]

        status = response.get("status")
        return status in valid_statuses

    @staticmethod
    def get_error_message(response: Dict[str, Any]) -> str:
        """Get the error message from a response.

        Args:
            response: The response to extract the error message from

        Returns:
            The error message
        """
        if "message" in response:
            return response["message"]
        elif "error" in response and isinstance(response["error"], str):
            return response["error"]
        elif "details" in response and isinstance(response["details"], str):
            return response["details"]
        else:
            return "Unknown error"
