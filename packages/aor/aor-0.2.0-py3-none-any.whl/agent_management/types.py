"""
Type definitions for agent management.

This module defines enums and type definitions used throughout the agent management package.
"""

from enum import Enum
from typing import List, TypedDict


class AgentType(str, Enum):
    """Supported agent types."""

    PYDANTIC = "pydantic"
    LANGCHAIN = "langchain"
    LANGGRAPH = "langgraph"


class ProtocolType(str, Enum):
    """Supported communication protocols."""

    A2A = "a2a"
    RAW = "raw"
    CUSTOM = "custom"


class FrameworkType(str, Enum):
    """Supported web frameworks."""

    FASTAPI = "fastapi"
    FLASK = "flask"


class DeploymentType(str, Enum):
    """Supported deployment targets."""

    AWS_LAMBDA = "aws-lambda"
    EC2 = "ec2"
    LOCAL = "local"


class InputType(str, Enum):
    """Supported input types."""

    TEXT = "text"
    # FILE = "file"
    # NUMBER = "number"
    # BOOLEAN = "boolean"
    # OBJECT = "object"
    # ARRAY = "array"


class OutputType(str, Enum):
    """Supported output types."""

    TEXT = "text"
    # FILE = "file"
    # NUMBER = "number"
    # BOOLEAN = "boolean"
    # OBJECT = "object"
    # ARRAY = "array"
    # ENUM = "enum"


class InputDefinition(TypedDict, total=False):
    """Type definition for agent input."""

    name: str
    type: str
    required: bool
    desc: str
    formats: List[str]


class OutputDefinition(TypedDict, total=False):
    """Type definition for agent output."""

    name: str
    type: str
    desc: str
    values: List[str]
