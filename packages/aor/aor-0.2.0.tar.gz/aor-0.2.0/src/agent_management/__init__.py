"""
Agent management module for creating and configuring agents.

This package provides classes for managing different aspects of agent creation:
- Path management
- Configuration management
- Input/output management
- Dependency management
- Code generation
"""

from .types import (
    AgentType,
    ProtocolType,
    FrameworkType,
    DeploymentType,
    InputType,
    OutputType,
    InputDefinition,
    OutputDefinition,
)
from .context import AgentCreationContext
from .path_manager import AgentPathManager
from .config_manager import AgentConfigManager
from .input_output_manager import InputOutputManager
from .dependency_manager import AgentDependencyManager
from .code_generator import AgentCodeGenerator

__all__ = [
    "AgentType",
    "ProtocolType",
    "FrameworkType",
    "DeploymentType",
    "InputType",
    "OutputType",
    "InputDefinition",
    "OutputDefinition",
    "AgentCreationContext",
    "AgentPathManager",
    "AgentConfigManager",
    "InputOutputManager",
    "AgentDependencyManager",
    "AgentCodeGenerator",
]