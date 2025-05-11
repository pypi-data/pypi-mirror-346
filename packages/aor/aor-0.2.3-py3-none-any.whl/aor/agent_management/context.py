"""
Context for agent creation process.

This module defines the AgentCreationContext class which holds all the state
needed during the agent creation process.
"""

from dataclasses import dataclass
from typing import Optional

from aor.common.agent import Agent
from aor.common.config import Config
from aor.utils.ui import UI


@dataclass
class AgentCreationContext:
    """Context for agent creation process.

    This class holds all the parameters and state needed during the agent creation process,
    making it easier to pass around between different components.
    """

    ui: UI

    name: str
    desc: Optional[str]
    agent_type: str
    path: str
    protocol: str
    framework: Optional[str]
    deploy: str
    manual: bool = False
    continue_flag: bool = False
    show_graph: bool = False
    config: Optional[Config] = None
    agent: Optional[Agent] = None
