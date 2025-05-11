#
# AI-on-Rails: All rights reserved.
#
"""Application management for AI-on-Rails."""

import base64
import locale
import copy
import os
from typing import Dict, Any, List, Optional, Union

from aor.common.config import Config
from aor.backend.request import Request
from aor.backend.endpoint import EndpointManager
from aor.backend.exceptions import BackendError, ValidationError
from aor.utils.ui import ui


class CreateApp(Request):
    """Represents a request to create an app."""

    def __init__(self, token: str, app: Config):
        """Initialize a create app request.

        Args:
            token: Authentication token
            app: The application configuration
        """
        # Get the original config as a dictionary
        orig_config = app.to_dict()

        # Add language if not present
        self._add_language_if_missing(orig_config)

        # Create a deep copy to avoid modifying the original
        body = copy.deepcopy(orig_config)

        # Process endpoints to ensure URL is at the top level
        self._process_endpoints(body)

        # Process cover image
        self._process_cover_image(body)

        ui.debug(f"Processing cover image in app configuration")

        super().__init__(token, "publish/create-app", body)

    def _add_language_if_missing(self, config: Dict[str, Any]) -> None:
        """Add language to the configuration if missing.

        Args:
            config: The configuration dictionary to modify
        """
        if "lang" not in config:
            try:
                # Get the language from the system locale
                lc = locale.getdefaultlocale()[0].split("_")
                config["lang"] = lc[0]
                ui.debug(f"Adding language '{config['lang']}' from system locale")
            except (TypeError, IndexError, AttributeError):
                # Default to English if locale detection fails
                config["lang"] = "en"
                ui.debug(f"Using default language 'en' as locale detection failed")

    def _process_endpoints(self, config: Dict[str, Any]) -> None:
        """Process endpoints to ensure URL is at the top level.

        Args:
            config: The configuration dictionary to modify
        """
        if "endpoints" in config:
            for endpoint in config["endpoints"]:
                # If URL is not at the top level but exists in deployment section, copy it to the top level
                if (
                    "url" not in endpoint
                    and "deployment" in endpoint
                    and "url" in endpoint["deployment"]
                ):
                    endpoint["url"] = endpoint["deployment"]["url"]
                    ui.debug(
                        f"Copying URL from deployment to top level for endpoint: {endpoint.get('name', 'unnamed')}"
                    )

    def _process_cover_image(self, config: Dict[str, Any]) -> None:
        """Process cover image in the configuration.

        Args:
            config: The configuration dictionary to modify
        """
        if "cover" in config:
            if config["cover"]:  # Check if cover exists and is not empty
                if "image" not in config:
                    # Check if the cover is a valid file path
                    cover_path = config["cover"]
                    if os.path.isfile(cover_path):
                        try:
                            # The cover is not yet uploaded, turn it into a base64 content
                            with open(cover_path, "rb") as f:
                                config["cover"] = base64.b64encode(f.read()).decode(
                                    "utf-8"
                                )
                            ui.debug(f"Converting cover image to base64: {cover_path}")
                        except (IOError, OSError) as e:
                            ui.error(f"Failed to read cover image: {str(e)}")
                            del config["cover"]
                    else:
                        ui.warning(f"Cover path does not exist: {cover_path}")
                        del config["cover"]
                else:
                    # Image already exists, no need to upload cover again
                    ui.debug(f"Image already exists, skipping cover upload")
                    del config["cover"]
            else:
                # Remove empty cover field to avoid file not found errors
                ui.debug(f"Removing empty cover field")
                del config["cover"]

    def send(self) -> Dict[str, Any]:
        """Send the request and process the response.

        Returns:
            The processed response
        """
        response = super().send()

        # Remove cover from response to avoid large data transfer
        if "cover" in response:
            del response["cover"]

        return response


class UpdateApp(Request):
    """Represents a request to update an app."""

    def __init__(self, token: str, config: Config):
        """Initialize an update app request.

        Args:
            token: Authentication token
            config: The application configuration
        """
        app_dict = config.to_dict()

        # Ensure the app has a UUID
        if not app_dict.get("uuid"):
            raise ValidationError("Cannot update app without UUID")

        ui.debug(f"Preparing to update app with UUID: {app_dict.get('uuid')}")

        # Process endpoints to ensure URL is at the top level
        self._process_endpoints(app_dict)

        # Log detailed app configuration in debug mode
        from aor.backend.config import is_debug_enabled

        if is_debug_enabled():
            import json

            # Create a copy to avoid modifying the original
            debug_dict = app_dict.copy()
            # Mask sensitive information if present
            if "token" in debug_dict:
                debug_dict["token"] = "***MASKED***"
            # Log key configuration elements
            ui.debug(f"App configuration for update:")
            ui.debug(f"  Name: {debug_dict.get('name', 'unnamed')}")
            ui.debug(f"  UUID: {debug_dict.get('uuid', 'missing')}")
            ui.debug(f"  Version: {debug_dict.get('version', 'not specified')}")
            ui.debug(f"  Endpoints count: {len(debug_dict.get('endpoints', []))}")

            # Check for potentially problematic fields
            if not debug_dict.get("name"):
                ui.debug("WARNING: App name is missing")
            if not debug_dict.get("version"):
                ui.debug("WARNING: App version is not specified")
            if not debug_dict.get("endpoints"):
                ui.debug("WARNING: No endpoints defined")

            # Log full configuration for detailed debugging
            ui.debug(f"Full app configuration: {json.dumps(debug_dict, indent=2)}")

        ui.info(f"Updating app: {app_dict.get('name', 'unnamed')}")

        super().__init__(token, "publish/create-app", app_dict)

    def _process_endpoints(self, config: Dict[str, Any]) -> None:
        """Process endpoints to ensure URL is at the top level.

        Args:
            config: The configuration dictionary to modify
        """
        if "endpoints" in config:
            for endpoint in config["endpoints"]:
                # If URL is not at the top level but exists in deployment section, copy it to the top level
                if (
                    "url" not in endpoint
                    and "deployment" in endpoint
                    and "url" in endpoint["deployment"]
                ):
                    endpoint["url"] = endpoint["deployment"]["url"]
                    ui.debug(
                        f"Copying URL from deployment to top level for endpoint: {endpoint.get('name', 'unnamed')}"
                    )


class DeleteApp(Request):
    """Represents a request to delete an app."""

    def __init__(self, token: str, app_id: str):
        """Initialize a delete app request.

        Args:
            token: Authentication token
            app_id: The application ID
        """
        ui.info(f"Deleting app: {app_id}")

        super().__init__(token, "publish/delete-app", {"app_id": app_id})


class ApplicationManager:
    """Manage AI-on-Rails applications."""

    def __init__(self, token: str):
        """Initialize the application manager.

        Args:
            token: Authentication token
        """
        self.token = token

    def create_app(self, config: Config) -> Dict[str, Any]:
        """Create a new application.

        Args:
            config: The application configuration

        Returns:
            The response from the API
        """
        request = CreateApp(self.token, config)
        return request.send()

    def update_app(self, config: Config) -> Dict[str, Any]:
        """Update an existing application.

        Args:
            config: The application configuration

        Returns:
            The response from the API
        """
        request = UpdateApp(self.token, config)
        return request.send()

    def delete_app(self, app_id: str) -> Dict[str, Any]:
        """Delete an application.

        Args:
            app_id: The application ID

        Returns:
            The response from the API
        """
        request = DeleteApp(self.token, app_id)
        return request.send()

    def publish_app(self, config: Config) -> Dict[str, Any]:
        """Publish an application (create or update).

        This method will create a new application if it doesn't exist,
        or update an existing application if it does.

        Args:
            config: The application configuration

        Returns:
            The response from the API
        """
        from aor.backend.config import is_debug_enabled

        app_uuid = config.get("uuid")
        app_name = config.get("name", "unnamed")

        if is_debug_enabled():
            ui.debug(f"Publishing application: {app_name}")
            ui.debug(f"Application UUID: {app_uuid or 'Not set (will create new)'}")

            # Log key configuration elements
            ui.debug(f"Application configuration summary:")
            ui.debug(f"  Name: {app_name}")
            ui.debug(f"  Version: {config.get('version', 'not specified')}")

            # Log endpoints information
            endpoints = config.get("endpoints", [])
            ui.debug(f"  Endpoints: {len(endpoints)}")
            for i, endpoint in enumerate(endpoints):
                ui.debug(f"    Endpoint {i+1}: {endpoint.get('name', 'unnamed')}")
                ui.debug(f"      Type: {endpoint.get('type', 'unknown')}")
                ui.debug(f"      UUID: {endpoint.get('uuid', 'not set')}")
                if "url" in endpoint:
                    ui.debug(f"      URL: {endpoint['url']}")
                elif endpoint.get("deployment", {}).get("url"):
                    ui.debug(
                        f"      URL (from deployment): {endpoint['deployment']['url']}"
                    )
                else:
                    ui.debug(f"      URL: Not set")

        if app_uuid:
            ui.info(f"Updating existing app: {app_uuid}")
            try:
                response = self.update_app(config)
                if is_debug_enabled():
                    ui.debug(f"Update successful for app: {app_uuid}")
            except Exception as e:
                if is_debug_enabled():
                    ui.debug(f"Update failed for app {app_uuid}: {str(e)}")
                raise
        else:
            ui.info(f"Creating new app: {app_name}")
            try:
                response = self.create_app(config)
                if is_debug_enabled():
                    ui.debug(f"Creation successful for app: {app_name}")
            except Exception as e:
                if is_debug_enabled():
                    ui.debug(f"Creation failed for app {app_name}: {str(e)}")
                raise

            # Update the config with the new UUID
            if response.get("uuid"):
                new_uuid = response["uuid"]
                config.set("uuid", new_uuid)
                if is_debug_enabled():
                    ui.debug(f"Updated config with new UUID: {new_uuid}")

        # Update the config with the image if provided
        if response.get("image"):
            image_url = response["image"]
            config.set("image", image_url)
            if is_debug_enabled():
                ui.debug(f"Updated config with image URL: {image_url}")

        if is_debug_enabled():
            import json

            ui.debug(f"Publish response: {json.dumps(response, indent=2)}")

        return response

    def sync_endpoints(self, config: Config, app_response: Dict[str, Any]) -> None:
        """Synchronize endpoints for an application.

        Args:
            config: The application configuration
            app_response: The response from the create/update app request

        Raises:
            ValidationError: If the app response is invalid
        """
        if not app_response.get("uuid"):
            raise ValidationError("App response missing UUID")

        app_uuid = app_response["uuid"]
        remote_endpoints = app_response.get("endpoints", [])
        local_endpoints = config.get("endpoints", [])

        # Validate that the number of endpoints matches
        if len(remote_endpoints) != len(local_endpoints):
            ui.warning(
                f"Endpoint count mismatch: remote={len(remote_endpoints)}, local={len(local_endpoints)}"
            )
            pass

        # Update local endpoint UUIDs from remote
        for i, remote_endpoint in enumerate(remote_endpoints):
            if i >= len(local_endpoints):
                ui.warning(
                    f"Skipping endpoint sync for index {i}: no matching local endpoint"
                )
                continue

            local_endpoint = local_endpoints[i]

            # Validate endpoint names match
            if remote_endpoint.get("name") != local_endpoint.get("name"):
                ui.warning(
                    f"Endpoint name mismatch: remote={remote_endpoint.get('name')}, local={local_endpoint.get('name')}"
                )
                pass

            # Validate endpoint UUIDs match if both exist
            if (
                local_endpoint.get("uuid")
                and remote_endpoint.get("uuid")
                and local_endpoint["uuid"] != remote_endpoint["uuid"]
            ):
                ui.warning(
                    f"Endpoint UUID mismatch: remote={remote_endpoint.get('uuid')}, local={local_endpoint.get('uuid')}"
                )
                pass

            # Update local UUID
            if remote_endpoint.get("uuid"):
                local_endpoint["uuid"] = remote_endpoint["uuid"]
                ui.debug(f"Updated local endpoint UUID: {remote_endpoint.get('uuid')}")

        # Save the updated configuration
        config.save()
