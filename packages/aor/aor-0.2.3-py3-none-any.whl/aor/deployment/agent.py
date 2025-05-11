"""
Agent discovery and validation utilities for deployment.
"""

from pathlib import Path
from typing import Dict, List, Optional, Any

from aor.utils.ui import UI
from aor.common.config import Config


def get_agents_to_deploy(
    ui: UI, config: Config, endpoint_name: Optional[str]
) -> List[Dict[str, Any]]:
    """
    Get the list of agents to deploy.

    Args:
        ui: UI instance for displaying messages
        config: Configuration object
        endpoint_name: Optional name of a specific endpoint to deploy

    Returns:
        List of agent configurations to deploy
    """
    agents_list = config.get("endpoints") or []
    ui.debug(f"Found {len(agents_list)} agents in configuration")

    # Process all agents if no specific endpoint is specified
    if not endpoint_name:
        ui.info(
            f"No specific endpoint specified, will deploy all {len(agents_list)} agents"
        )
        # Validate and fix paths for all agents
        for agent in agents_list:
            validate_and_fix_agent_path(ui, agent)
        return agents_list

    # Find specific agent
    ui.info(f"Looking for endpoint: {endpoint_name}")
    for agent in agents_list:
        if agent["name"] == endpoint_name:
            # Validate and fix the path
            validate_and_fix_agent_path(ui, agent)
            ui.success(f"Found endpoint: {endpoint_name}")
            return [agent]

    ui.error(f"Endpoint '{endpoint_name}' not found in configuration.")
    return []


def validate_and_fix_agent_path(ui: UI, agent: Dict[str, Any]) -> None:
    """
    Validate and fix the agent path to handle both file and directory paths.

    Args:
        ui: UI instance for displaying messages
        agent: Agent configuration dictionary
    """
    if "path" not in agent:
        ui.warning(f"Agent {agent['name']} has no path specified")
        return

    # Convert path separators to platform-specific format
    agent["path"] = str(Path(agent["path"]))
    path = Path(agent["path"])

    # Check if path exists
    if path.exists():
        # Path exists, check if it's a file or directory
        if path.is_file():
            ui.debug(f"Agent path is a file: {path}")
        elif path.is_dir():
            ui.debug(f"Agent path is a directory: {path}")
        else:
            ui.warning(
                f"Agent path exists but is neither a file nor a directory: {path}"
            )
    else:
        ui.warning(f"Agent path does not exist: {path}")

        # Try to find a matching file or directory
        if path.suffix == ".py":
            # If it's a .py file that doesn't exist, check if there's a directory with the same name
            potential_dir = Path(str(path).replace(".py", ""))
            if potential_dir.exists() and potential_dir.is_dir():
                agent["path"] = str(potential_dir)
                ui.debug(f"Updated agent path to directory: {agent['path']}")
        else:
            # If it's a directory that doesn't exist, check if there's a .py file with the same name
            potential_file = Path(f"{path}.py")
            if potential_file.exists() and potential_file.is_file():
                agent["path"] = str(potential_file)
                ui.debug(f"Updated agent path to file: {agent['path']}")
