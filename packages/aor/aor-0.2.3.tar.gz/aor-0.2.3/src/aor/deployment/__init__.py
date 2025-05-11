"""
Deployment module for AI-on-Rails.

This module provides client interfaces for deploying agents to various platforms.
"""

from typing import Dict, Type, Optional

from .base import DeploymentClient
from .models import DeploymentOptions, DeploymentResult, DeploymentStatus
from .exceptions import DeploymentError, ClientInitializationError, ValidationError

# Import clients
from .clients.aws import LambdaClient, SAMClient

# Client registry
_CLIENT_REGISTRY: Dict[str, Type[DeploymentClient]] = {
    "aws-lambda": LambdaClient,
    "aws-sam": SAMClient,
}


def get_client(provider: str, **kwargs) -> DeploymentClient:
    """
    Get a deployment client for the specified provider.

    Args:
        provider: Name of the provider (e.g., "aws-lambda")
        **kwargs: Additional options for client initialization

    Returns:
        Initialized deployment client

    Raises:
        ClientInitializationError: If client initialization fails
    """
    client_class = _CLIENT_REGISTRY.get(provider)
    if not client_class:
        raise ClientInitializationError(f"Unknown provider: {provider}")

    try:
        return client_class(**kwargs)
    except Exception as e:
        raise ClientInitializationError(
            f"Failed to initialize {provider} client: {str(e)}"
        )


__all__ = [
    "DeploymentClient",
    "DeploymentOptions",
    "DeploymentResult",
    "DeploymentStatus",
    "DeploymentError",
    "ValidationError",
    "ClientInitializationError",
    "get_client",
    "LambdaClient",
    "SAMClient",
]
