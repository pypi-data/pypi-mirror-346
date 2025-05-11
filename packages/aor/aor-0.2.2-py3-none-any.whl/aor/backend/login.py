#
# AI-on-Rails: All rights reserved.
#
"""Login functionality for AI-on-Rails."""

from typing import Dict, Any, Optional

from aor.backend.request import Request
from aor.backend.exceptions import AuthenticationError
from aor.utils.ui import ui


class Login(Request):
    """Represents a request to login."""

    def __init__(self, email: str, password: str):
        """Initialize a login request.

        Args:
            email: User email
            password: User password
        """
        ui.debug(f"Attempting login for user: {email}")

        super().__init__("", "login", {"email": email, "password": password})

    def send(self) -> str:
        """Send the login request and return the token.

        Returns:
            Authentication token

        Raises:
            AuthenticationError: If login fails
        """
        response = super().send()

        if response.get("status") != "success":
            error_message = response.get("message", "Authentication failed")
            raise AuthenticationError(error_message)

        return response.get("token")

    def send_with_error_handling(self) -> Dict[str, Any]:
        """Send the login request and handle errors.

        Returns:
            Dictionary with token or error information
        """
        try:
            token = self.send()
            return {"status": "success", "token": token}
        except AuthenticationError as e:
            return {"status": "error", "message": str(e)}
