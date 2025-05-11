#
# AI-on-Rails: All rights reserved.
#
"""Publish an AI-on-Rails application."""

import json
import logging
import os
import sys
import traceback
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable, Union, Tuple

import rich_click as click

from .common.config import Config
from .system.token import get_token
from .backend.config import configure, is_debug_enabled
from .backend.application import ApplicationManager
from .backend.exceptions import BackendError, ValidationError, RequestError
from .utils.ui import UI

# Set up logger for this module
logger = logging.getLogger(__name__)


class PublishManager:
    """Manages the publication process for AI-on-Rails applications.
    
    This class encapsulates the logic for publishing an application to the
    AI-on-Rails platform, including configuration validation, endpoint validation,
    and interaction with the backend API.
    """

    def __init__(self, ui: UI, token: Optional[str] = None, debug: bool = False):
        """Initialize the publish manager.
        
        Args:
            ui: The UI instance for displaying information
            token: Optional API token for authentication
            debug: Whether to enable debug mode
        """
        self.ui = ui
        self.token = token
        self.debug = debug
        self.config: Optional[Config] = None
        self.app_manager: Optional[ApplicationManager] = None

    def load_configuration(self) -> bool:
        """Load and validate the application configuration.
        
        Returns:
            bool: True if configuration was loaded successfully, False otherwise
        """
        self.ui.debug("Loading configuration...")
        try:
            self.config = Config(readiness=Config.READY_TO_PUBLISH)
            return True
        except FileNotFoundError:
            self.ui.error("Configuration file not found: aionrails.yaml")
            self.ui.info("Make sure you are in the correct directory with an AI-on-Rails project.")
            self.ui.info("You can create a new project with: aor new <project-name>")
            return False
        except Exception as e:
            self.ui.error(f"Failed to load configuration: {str(e)}")
            self.ui.debug(f"Exception details: {type(e).__name__}: {str(e)}")
            return False

    def validate_cover_image(self) -> bool:
        """Validate and process the cover image.
        
        Returns:
            bool: True if cover image is valid or was set to default, False otherwise
        """
        if not self.config or not isinstance(self.config, Config):
            self.ui.error("Configuration not loaded")
            return False

        # Check if cover image is specified in the config
        if self.config.get("cover"):
            return True

        self.ui.warning("No cover image specified in the configuration.")

        # Find the package root directory (where the default cover image is located)
        package_root = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        default_cover_path = package_root / "src" / "common" / "logo.png"

        # Check if the default cover image exists
        if default_cover_path.exists():
            use_default = self.ui.confirm("Do you want to use the default cover image?")
            if use_default:
                self.config.set("cover", str(default_cover_path))
                self.ui.info("Using default cover image.")
                return True
            else:
                self.ui.error(
                    "Cannot publish without a cover image. Please add a cover image to your configuration."
                )
                return False
        else:
            self.ui.error(
                "No cover image found. Cannot publish without a cover image. "
                "Please add a cover image to your configuration."
            )
            return False

    def validate_endpoints(self) -> bool:
        """Validate that endpoints have URLs if they have deployment info.
        
        Returns:
            bool: True if endpoints are valid, False otherwise
        """
        if not self.config:
            self.ui.error("Configuration not loaded")
            return False

        missing_urls = []
        for endpoint in self.config.get("endpoints", []):
            if endpoint.get("deployment") and not endpoint.get("url"):
                missing_urls.append(endpoint["name"])
                self.ui.warning(
                    f"Endpoint '{endpoint['name']}' has no URL. It may not be accessible."
                )

        if missing_urls:
            self.ui.warning(
                f"Found {len(missing_urls)} endpoint(s) without URLs. Consider deploying them first."
            )
        
        return True

    def get_token(self) -> Optional[str]:
        """Get the API token, either from the provided token or from the system.
        
        Returns:
            Optional[str]: The API token, or None if not available
        """
        if self.token:
            self.ui.debug("Using provided API token")
            return self.token
        
        self.ui.debug("No token provided, attempting to retrieve from system")
        token = get_token()
        
        if not token:
            self.ui.error("No API token found")
            self.ui.info("Please login first with: aor login")
            return None
        
        if len(token.strip()) < 10:  # Basic validation for token format
            self.ui.warning("API token appears to be invalid or malformed")
            self.ui.info("Please login again with: aor login")
            return None
            
        self.ui.debug("Successfully retrieved API token from system")
        return token

    def publish_application(self) -> Optional[Dict[str, Any]]:
        """Publish the application to the AI-on-Rails platform.
        
        Returns:
            Optional[Dict[str, Any]]: The server response if successful, None otherwise
        """
        if not self.config:
            self.ui.error("Configuration not loaded")
            return None

        token = self.get_token()
        if not token:
            return None

        # Create application manager
        self.app_manager = ApplicationManager(token)

        try:
            # Add debug log before process_spinner to track execution flow
            self.ui.debug("About to publish application...")
            
            # Publish the application
            app_response = self.ui.process_spinner(
                "Publishing to AI-on-Rails platform", 
                self.app_manager.publish_app,
                self.config
            )

            self.ui.debug(f"Server response: {app_response}")

            # Process the response
            if not self._process_publish_response(app_response):
                return None

            return app_response
            
        except RequestError as e:
            # Handle request-specific errors
            status_code = e.details.get("status_code", "unknown")
            response_text = e.details.get("response_text", "no response")
            self.ui.debug(f"Request error details: Status code: {status_code}, Response: {response_text}")
            
            # Check for invalid token error
            if status_code == 400 and "invalid token" in str(response_text).lower():
                self.ui.error("Authentication failed: Invalid API token")
                self.ui.info("Please login again using: aor login")
            else:
                self.ui.error(f"API request failed: {str(e)}")
                
            return None
        except Exception as e:
            # Handle general exceptions
            self.ui.debug(f"Exception caught in publish_application: {type(e).__name__}: {str(e)}")
            self.ui.debug(f"Stack trace: {traceback.format_exc()}")
            self.ui.error(f"Failed to publish application: {str(e)}")
            return None

    def _process_publish_response(self, response: Dict[str, Any]) -> bool:
        """Process the response from the publish API call.
        
        Args:
            response: The server response
            
        Returns:
            bool: True if the response was processed successfully, False otherwise
        """
        # Check for errors
        if response.get("error"):
            error_msg = response.get("message", "Unknown error")
            self.ui.debug(f"Error in response: {error_msg}")
            self.ui.debug(f"Full error response: {response}")
            self.ui.error(f"Publication failed: {error_msg}")
            return False

        # Check for incomplete status
        elif response.get("status") == "incomplete":
            if response.get("messages", None):
                for message in response.get("messages", []):
                    self.ui.error(f"Not ready for review: {message}")
            else:
                self.ui.error(
                    "Not ready for review: {}".format(
                        response.get("message", "unknown reason")
                    )
                )
            self.ui.warning(
                "Application is not yet queued for review and not ready to be queried."
            )
            self.ui.info(
                "Use `aor lint` to see what might be missing in the configuration file"
            )
            return False

        # Check for unexpected status
        elif response.get("status") != "success":
            error_msg = response.get("message", "Unknown error")
            self.ui.debug(f"Unexpected status: {response.get('status')}")
            self.ui.debug(f"Full response: {response}")
            self.ui.error(f"Publication failed with status '{response.get('status')}': {error_msg}")
            return False
            
        return True

    def sync_endpoints(self, app_response: Dict[str, Any]) -> bool:
        """Synchronize endpoints between the local configuration and the server.
        
        Args:
            app_response: The server response
            
        Returns:
            bool: True if endpoints were synchronized successfully, False otherwise
        """
        if not self.config or not self.app_manager:
            self.ui.error("Configuration or application manager not initialized")
            return False

        try:
            self.app_manager.sync_endpoints(self.config, app_response)
            return True
        except Exception as e:
            self.ui.debug(f"Failed to sync endpoints: {str(e)}")
            self.ui.warning("Failed to synchronize endpoints with the server")
            return False

    def display_summary(self, app_response: Dict[str, Any]) -> None:
        """Display a summary of the published application.
        
        Args:
            app_response: The server response
        """
        if not self.config:
            return

        # Display summary
        self.ui.section("Publication Summary")
        self.ui.value("Application", self.config.get("name"))
        self.ui.value("UUID", app_response["uuid"])
        if "image" in app_response:
            self.ui.value("Image", app_response["image"])

        # Display endpoints
        if app_response.get("endpoints"):
            self.ui.section("Published Endpoints")
            for endpoint in app_response["endpoints"]:
                self.ui.success(f"{endpoint['name']} (UUID: {endpoint['uuid']})")

        self.ui.success("The application is published successfully!")
        self.ui.info("Use `aor execute` to test AI Agents")
        self.ui.info("Use `aor lint` to test the application readiness")
        self.ui.info("Re-run `aor publish` to update the application")


@click.command()
@click.option("--token", type=str, help="Token for the AI-on-Rails API", required=False)
@click.pass_context
def publish(ctx, token: Optional[str] = None) -> None:
    """Publish the current application to AI-on-Rails."""
    # Get context parameters
    no_ansi = ctx.obj.get("NO_ANSI", False) if ctx.obj else False
    debug = ctx.obj.get("DEBUG", False) if ctx.obj else False

    # Configure backend
    configure(debug=debug)

    # Initialize UI
    ui = UI(debug_mode=debug, no_ansi=no_ansi)
    ui.header("Publishing Application")

    # Create publish manager
    manager = PublishManager(ui, token, debug)

    # Load configuration
    if not manager.load_configuration():
        return

    # Validate cover image
    if not manager.validate_cover_image():
        return

    # Validate endpoints
    try:
        ui.process_spinner("Validating endpoints", manager.validate_endpoints)
    except Exception as e:
        ui.error(f"Failed to validate endpoints: {str(e)}")
        return

    # Determine if updating or creating new application
    if manager.config.get("uuid") is not None:
        ui.info(f"Updating existing application: {manager.config.get('name')}")
        ui.debug(f"Application UUID: {manager.config.get('uuid')}")
    else:
        ui.info(f"Creating new application: {manager.config.get('name')}")

    # Publish application
    app_response = manager.publish_application()
    if not app_response:
        return

    # Synchronize endpoints
    manager.sync_endpoints(app_response)

    # Display summary
    manager.display_summary(app_response)
