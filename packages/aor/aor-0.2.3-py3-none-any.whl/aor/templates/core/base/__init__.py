"""
Base interfaces for all AI-on-Rails agents.
"""

from .agent_interface import BaseAgent, AgentMetadata
from .state_interface import BaseState

__all__ = [
    'BaseAgent',
    'BaseState',
    "AgentMetadata",
]