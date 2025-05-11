"""
Abstract base classes for deployment clients.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, Optional, List

from .models import DeploymentOptions, DeploymentResult, DeploymentStatus


class DeploymentClient(ABC):
    """Base abstract client for all deployment providers."""

    @abstractmethod
    def validate_connection(self) -> bool:
        """
        Verify connectivity and credentials.

        Returns:
            True if connected successfully, False otherwise
        """
        pass

    @abstractmethod
    def deploy(
        self, package_path: Path, options: DeploymentOptions
    ) -> DeploymentResult:
        """
        Deploy a prepared package to the target environment.

        Args:
            package_path: Path to the deployment package
            options: Deployment options

        Returns:
            Deployment result
        """
        pass

    @abstractmethod
    def get_deployment_status(self, deployment_id: str) -> DeploymentStatus:
        """
        Get the current status of a deployment.

        Args:
            deployment_id: ID of the deployment

        Returns:
            Current deployment status
        """
        pass

    @abstractmethod
    def remove_deployment(self, deployment_id: str) -> bool:
        """
        Remove a deployment from the target environment.

        Args:
            deployment_id: ID of the deployment to remove

        Returns:
            True if removal was successful, False otherwise
        """
        pass

    @abstractmethod
    def list_deployments(
        self, filter_options: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        List deployments with optional filtering.

        Args:
            filter_options: Options to filter deployments

        Returns:
            List of deployment information
        """
        pass

    @abstractmethod
    def get_logs(
        self,
        deployment_id: str,
        start_time: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[str]:
        """
        Get logs for a deployment.

        Args:
            deployment_id: ID of the deployment
            start_time: Optional start time for logs
            limit: Optional maximum number of log entries

        Returns:
            List of log entries
        """
        pass
