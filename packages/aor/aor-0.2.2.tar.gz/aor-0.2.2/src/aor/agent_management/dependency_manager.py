"""
Dependency management for agent creation.

This module provides functionality for managing dependencies during agent creation.
"""

import os
from typing import List

from aor.common.agent import Agent
from aor.utils.ui import UI

from .types import AgentType, FrameworkType, ProtocolType


class AgentDependencyManager:
    """Manages dependencies for agents."""

    def __init__(self, ui: UI):
        """Initialize the dependency manager.

        Args:
            ui: UI instance for logging and user interaction
        """
        self.ui = ui

    def add_dependencies(self, agent: Agent) -> None:
        """Add dependencies based on agent type and options.

        Args:
            agent: The agent object
        """
        dependencies = self._get_agent_dependencies(agent)

        # Install main dependencies (dedup them first)
        if dependencies:
            unique_deps = list(set(dependencies))
            self.ui.step(f"Installing {len(unique_deps)} dependencies")
            self.ui.display_table(
                "Dependencies", ["Package"], [[dep] for dep in unique_deps]
            )

            with self.ui.console.status("Installing dependencies...") as status:
                # Execute and capture the result of dependency installation
                command = f"poetry add {' '.join(unique_deps)}"
                self.ui.debug(f"Running command: {command}")
                result = os.system(command)
                if result == 0:
                    status.update("Dependencies installed successfully")
                    self.ui.success("Dependencies installed successfully")
                else:
                    status.update(
                        "Some dependencies may not have been installed properly"
                    )
                    self.ui.warning(
                        "Some dependencies may not have been installed properly"
                    )

        # Add dev dependencies for Python agents
        if agent.is_python_agent():
            self._add_dev_dependencies()

    def _get_agent_dependencies(self, agent: Agent) -> List[str]:
        """Get the dependencies required for a specific agent.

        Args:
            agent: The agent object

        Returns:
            List of dependencies
        """
        dependencies: List[str] = []

        # Add type-specific dependencies
        if agent.type == AgentType.LANGCHAIN.value:
            dependencies.extend(["langchain", "langchain_anthropic"])
        elif agent.type == AgentType.PYDANTIC.value:
            dependencies.append("pydantic")
        elif agent.type == AgentType.LANGGRAPH.value:
            dependencies.extend(["langgraph", "anthropic"])

        # Add protocol-specific dependencies
        if agent.protocol == ProtocolType.A2A.value:
            dependencies.extend(["fastapi", "uvicorn", "pydantic"])

        # Add framework-specific dependencies
        if agent.framework == FrameworkType.FASTAPI.value:
            dependencies.extend(["fastapi", "uvicorn"])
        elif agent.framework == FrameworkType.FLASK.value:
            dependencies.append("flask")

        return dependencies

    def _add_dev_dependencies(self) -> None:
        """Add development dependencies for Python agents."""
        dev_dependencies = ["pytest", "black", "isort", "ruff", "pytest-cov"]
        self.ui.step(f"Installing {len(dev_dependencies)} development dependencies")
        self.ui.display_table(
            "Dev Dependencies", ["Package"], [[dep] for dep in dev_dependencies]
        )

        with self.ui.console.status("Installing dev dependencies...") as status:
            # Execute and capture the result of dev dependency installation
            command = f"poetry add --dev {' '.join(dev_dependencies)}"
            self.ui.debug(f"Running command: {command}")
            result = os.system(command)
            if result == 0:
                status.update("Dev dependencies installed successfully")
                self.ui.success("Dev dependencies installed successfully")
            else:
                status.update(
                    "Some dev dependencies may not have been installed properly"
                )
                self.ui.warning(
                    "Some dev dependencies may not have been installed properly"
                )
