"""
Custom exceptions for the deployment module.
"""


class DeploymentError(Exception):
    """Base exception for all deployment-related errors."""

    pass


class ClientInitializationError(DeploymentError):
    """Error initializing a deployment client."""

    pass


class ValidationError(DeploymentError):
    """Validation error for deployment parameters."""

    pass


class ConnectionError(DeploymentError):
    """Error connecting to deployment provider."""

    pass


class PackagingError(DeploymentError):
    """Error packaging an agent for deployment."""

    pass


class DeploymentTimeoutError(DeploymentError):
    """Deployment operation timed out."""

    pass


class ResourceLimitError(DeploymentError):
    """Resource limit exceeded during deployment."""

    pass


class PermissionError(DeploymentError):
    """Insufficient permissions for deployment operation."""

    pass


class ConfigurationError(DeploymentError):
    """Invalid configuration for deployment."""

    pass


class ResourceNotFoundError(DeploymentError):
    """Resource not found during deployment operation."""

    pass
