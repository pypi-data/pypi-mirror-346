"""
Deployment adapters for AI-on-Rails.

This package contains deployment configurations for various platforms.
"""

# Import deployment adapters
from .base.deployment_adapter import DeploymentAdapter

# Registry for all available deployment adapters
deployment_registry = {}

def register_deployment(key: str, adapter_class: type):
    """
    Register a deployment adapter.
    
    Args:
        key: Deployment type key (e.g., 'aws-lambda', 'ec2')
        adapter_class: Deployment adapter class
    """
    deployment_registry[key] = adapter_class

def get_deployment_adapter(key: str, config: dict) -> DeploymentAdapter:
    """
    Get deployment adapter by key.
    
    Args:
        key: Deployment type key
        config: Configuration for the deployment
        
    Returns:
        Initialized deployment adapter
        
    Raises:
        KeyError: If deployment type not found
    """
    if key not in deployment_registry:
        raise KeyError(f"Deployment adapter '{key}' not found")
    
    adapter_class = deployment_registry[key]
    return adapter_class(config)

def list_deployments() -> list:
    """
    List all registered deployment types.
    
    Returns:
        List of deployment type keys
    """
    return list(deployment_registry.keys())

# Import all deployment adapters to register them
try:
    from .aws_lambda import LambdaDeploymentAdapter
    register_deployment("aws-lambda", LambdaDeploymentAdapter)
except ImportError:
    pass

try:
    from .ec2 import EC2DeploymentAdapter
    register_deployment("ec2", EC2DeploymentAdapter)
except ImportError:
    pass

# Add more deployments as they are implemented...

__all__ = [
    "DeploymentAdapter",
    "register_deployment",
    "get_deployment_adapter",
    "list_deployments"
]