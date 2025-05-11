#
# AI-on-Rails: All rights reserved.
#
"""Endpoint management for AI-on-Rails applications."""

from typing import Dict, Any, List, Optional

from aor.common.agent import Agent
from aor.backend.request import Request
from aor.utils.ui import ui


class CreateEndpoint(Request):
    """Represents a request to create an endpoint."""

    def __init__(self, token: str, app_id: str, endpoint: Agent):
        """Initialize a create endpoint request.

        Args:
            token: Authentication token
            app_id: The application ID
            endpoint: The endpoint configuration
        """
        body = {
            "app_id": app_id,
            **endpoint.to_dict(),
        }

        ui.debug(f"Creating endpoint: {endpoint.get('name', 'unnamed')}")

        super().__init__(token, "publish/create-endpoint", body)


class UpdateEndpoint(Request):
    """Represents a request to update an endpoint."""

    def __init__(self, token: str, app_id: str, endpoint: Agent):
        """Initialize an update endpoint request.

        Args:
            token: Authentication token
            app_id: The application ID
            endpoint: The endpoint configuration
        """
        body = {
            "app_id": app_id,
            **endpoint.to_dict(),
        }

        ui.debug(f"Updating endpoint: {endpoint.get('name', 'unnamed')}")

        super().__init__(token, "publish/update-endpoint", body)


class DeleteEndpoint(Request):
    """Represents a request to delete an endpoint."""

    def __init__(self, token: str, app_id: str, endpoint_uuid: str):
        """Initialize a delete endpoint request.

        Args:
            token: Authentication token
            app_id: The application ID
            endpoint_uuid: The endpoint UUID
        """
        body = {"app_id": app_id, "endpoint_uuid": endpoint_uuid}

        ui.debug(f"Deleting endpoint: {endpoint_uuid}")

        super().__init__(token, "publish/delete-endpoint", body)


# Legacy aliases for backward compatibility
CreateAgent = CreateEndpoint
UpdateAgent = UpdateEndpoint
DeleteAgent = DeleteEndpoint


class EndpointManager:
    """Manage endpoints for an application."""

    def __init__(self, token: str, app_id: str):
        """Initialize the endpoint manager.

        Args:
            token: Authentication token
            app_id: The application ID
        """
        self.token = token
        self.app_id = app_id

    def create_endpoint(self, endpoint: Agent) -> Dict[str, Any]:
        """Create a new endpoint.

        Args:
            endpoint: The endpoint configuration

        Returns:
            The response from the API
        """
        request = CreateEndpoint(self.token, self.app_id, endpoint)
        return request.send()

    def update_endpoint(self, endpoint: Agent) -> Dict[str, Any]:
        """Update an existing endpoint.

        Args:
            endpoint: The endpoint configuration

        Returns:
            The response from the API
        """
        request = UpdateEndpoint(self.token, self.app_id, endpoint)
        return request.send()

    def delete_endpoint(self, endpoint_uuid: str) -> Dict[str, Any]:
        """Delete an endpoint.

        Args:
            endpoint_uuid: The endpoint UUID

        Returns:
            The response from the API
        """
        request = DeleteEndpoint(self.token, self.app_id, endpoint_uuid)
        return request.send()

    def sync_endpoints(
        self, local_endpoints: List[Agent], remote_endpoints: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Synchronize local endpoints with remote endpoints.

        Args:
            local_endpoints: List of local endpoint configurations
            remote_endpoints: List of remote endpoint configurations

        Returns:
            Dictionary with lists of created, updated, and deleted endpoints
        """
        result = {"created": [], "updated": [], "deleted": []}

        # Build a map of remote endpoint UUIDs to endpoints
        remote_endpoint_map = {
            endpoint["uuid"]: endpoint
            for endpoint in remote_endpoints
            if endpoint.get("uuid")
        }

        # Track which remote endpoints we've processed
        processed_remote_uuids = set()

        # Process local endpoints
        for local_endpoint in local_endpoints:
            local_uuid = local_endpoint.get("uuid")

            if local_uuid and local_uuid in remote_endpoint_map:
                # Endpoint exists remotely, update it
                ui.info(f"Updating endpoint: {local_endpoint.get('name', 'unnamed')}")
                response = self.update_endpoint(local_endpoint)
                result["updated"].append(response)
                processed_remote_uuids.add(local_uuid)
            else:
                # Endpoint doesn't exist remotely, create it
                ui.info(f"Creating endpoint: {local_endpoint.get('name', 'unnamed')}")
                response = self.create_endpoint(local_endpoint)
                result["created"].append(response)

                # Update the local endpoint with the UUID from the response
                if response.get("uuid"):
                    local_endpoint["uuid"] = response["uuid"]

        # Delete remote endpoints that don't exist locally
        for remote_uuid in remote_endpoint_map:
            if remote_uuid not in processed_remote_uuids:
                ui.info(f"Deleting endpoint: {remote_uuid}")
                response = self.delete_endpoint(remote_uuid)
                result["deleted"].append(response)

        return result
