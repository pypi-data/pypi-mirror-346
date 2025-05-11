#
# AI-on-Rails: All rights reserved.
#
"""Resolve internal AI Agent identifiers into the publicly visible ones."""

from typing import Dict, Any, List

from aor.common.config import Config
from aor.backend.request import Request
from aor.utils.ui import ui


class Resolve(Request):
    """Resolve internal AI Agent identifiers into the publicly visible ones."""

    def __init__(self, token: str, app: Config):
        """Initialize a resolve request.

        Args:
            token: Authentication token
            app: The application configuration
        """
        # Extract the necessary information from the app configuration
        app_uuid = app.get("uuid")
        endpoint_uuids = self._extract_endpoint_uuids(app)

        # Build the request body
        request_body = {
            "uuid": app_uuid,
            "endpoints": endpoint_uuids,
        }

        ui.debug(f"Resolving app: {app_uuid}")

        super().__init__(token, "publish/resolve", request_body)

    def _extract_endpoint_uuids(self, app: Config) -> List[str]:
        """Extract endpoint UUIDs from the app configuration.

        Args:
            app: The application configuration

        Returns:
            List of endpoint UUIDs
        """
        endpoints = app.get("endpoints", [])
        return [
            endpoint.get("uuid")
            for endpoint in endpoints
            if endpoint.get("uuid") is not None
        ]

    def send(self) -> Dict[str, Any]:
        """Send the request and handle error responses.

        Returns:
            The parsed response or an error dictionary
        """
        try:
            # Call the parent class's send method directly to avoid recursion
            return super().send()
        except Exception as e:
            if hasattr(e, "to_dict"):
                return e.to_dict()
            return {"error": str(e)}
