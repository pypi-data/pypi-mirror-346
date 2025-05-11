"""
Base deployment adapter for AI-on-Rails deployments.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pathlib import Path


class DeploymentAdapter(ABC):
    """
    Base class for all deployment adapters.
    Defines the interface that all deployment targets must implement.
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the deployment adapter.
        
        Args:
            config: Configuration dictionary containing deployment-specific settings
        """
        self.config = config
        self.name = self.__class__.__name__.replace('Adapter', '').lower()
        
    @abstractmethod
    def validate_config(self) -> bool:
        """
        Validate the deployment configuration.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        pass
    
    @abstractmethod
    def prepare_package(self, agent_dir: Path, output_dir: Path) -> bool:
        """
        Prepare the deployment package.
        
        Args:
            agent_dir: Directory containing the agent code
            output_dir: Directory where the deployment package should be created
            
        Returns:
            bool: True if package preparation was successful
        """
        pass
    
    @abstractmethod
    def deploy(self, package_dir: Path, **kwargs) -> Dict[str, Any]:
        """
        Deploy the agent to the target platform.
        
        Args:
            package_dir: Directory containing the prepared deployment package
            **kwargs: Additional deployment parameters
            
        Returns:
            Dict containing deployment results (endpoint URL, status, etc.)
        """
        pass
    
    @abstractmethod
    def get_runtime_config(self) -> Dict[str, Any]:
        """
        Get runtime configuration for the deployed agent.
        
        Returns:
            Dict with runtime settings specific to this deployment type
        """
        pass
    
    @abstractmethod
    def get_required_environment_vars(self) -> List[str]:
        """
        Get list of required environment variables.
        
        Returns:
            List of environment variable names that must be set
        """
        pass
    
    def get_deployment_commands(self) -> List[str]:
        """
        Get list of commands needed to deploy.
        
        Returns:
            List of commands that will be executed during deployment
        """
        return []
    
    def validate_prerequisites(self) -> bool:
        """
        Validate that all prerequisites for deployment are met.
        
        Returns:
            bool: True if all prerequisites are met
        """
        return True
    
    def get_deployment_info(self) -> Dict[str, Any]:
        """
        Get information about the deployment adapter.
        
        Returns:
            Dict with adapter information
        """
        return {
            "name": self.name,
            "type": self.__class__.__name__,
            "supported_features": self.get_supported_features(),
            "required_env_vars": self.get_required_environment_vars()
        }
    
    def get_supported_features(self) -> List[str]:
        """
        Get list of supported features by this deployment adapter.
        
        Returns:
            List of supported feature names
        """
        return []