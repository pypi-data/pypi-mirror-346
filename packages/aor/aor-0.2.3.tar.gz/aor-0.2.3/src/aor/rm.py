#
# AI-on-Rails: All rights reserved.
#

import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Set, Optional, Tuple

import rich_click as click

from .common.config import Config
from .backend.endpoint import DeleteAgent
from .common.agent import PYTHON_AGENT_TYPES

from .utils.ui import UI


@click.command()
@click.option("--token", type=str, help="Token for the AI-on-Rails API")
@click.option("--name", type=str, help="Name of the agent to remove")
@click.option("--uuid", type=str, help="UUID of the agent to remove")
@click.option(
    "--keep-dependencies",
    is_flag=True,
    help="Keep all dependencies even if not used by other agents",
)
@click.option(
    "-d",
    "--delete-files",
    is_flag=True,
    help="Delete the agent's source files from disk",
)
@click.option(
    "-s",
    "--skip-uninstall",
    is_flag=True,
    help="Skip uninstalling dependencies from the system (still updates requirements.txt)",
)
@click.pass_context
def rm(
    ctx,
    name: Optional[str],
    uuid: Optional[str],
    token: Optional[str],
    keep_dependencies: bool = False,
    delete_files: bool = False,
    skip_uninstall: bool = False,
):
    """
    Remove an agent from the current application.

    Args:
        name: Name of the agent to remove
        uuid: UUID of the agent to remove
        token: Token for the AI-on-Rails API
        keep_dependencies: Keep all dependencies even if not used by other agents
        delete_files: Delete the agent's source files from disk
        skip_uninstall: Skip uninstalling dependencies from the system
        debug: Enable debug mode for more verbose output
    """
    # Get no_ansi from context if available
    no_ansi = ctx.obj.get("NO_ANSI", False) if ctx.obj else False

    # Get debug mode from context
    debug = ctx.obj.get("DEBUG", False) if ctx.obj else False

    # Initialize UI
    ui = UI(debug_mode=debug, no_ansi=no_ansi)
    ui.header("Remove Agent")

    # Validate parameters
    if not _validate_parameters(ui, name, uuid):
        return

    # Load configuration
    config = _load_configuration(ui)
    if not config:
        return

    # Get the agents list from config
    agents = config.get("endpoints")

    # Find the agent to remove
    agent, agent_index = _find_agent_to_remove(ui, agents, name, uuid)
    if agent_index is None:
        return

    # Display agent details
    _display_agent_details(ui, agent)

    # Confirm removal
    if not ui.confirm("Are you sure you want to remove this agent?"):
        ui.info("Operation cancelled.")
        return

    # Get the dependencies for the agent being removed
    agent_type = agent.get("type", "")
    removed_agent_dependencies = get_dependencies_for_type(agent_type)

    # Process agent removal
    if not _remove_agent(ui, config, agents, agent, agent_index, delete_files, token):
        return

    ui.success(f"Agent '{agent.get('name')}' removed from the current application.")

    # Clean up dependencies if needed
    if not keep_dependencies and agent_type in PYTHON_AGENT_TYPES:
        cleanup_dependencies(agents, removed_agent_dependencies, skip_uninstall, ui)


def _validate_parameters(ui: UI, name: Optional[str], uuid: Optional[str]) -> bool:
    """
    Validate command parameters.

    Args:
        ui: UI instance
        name: Agent name
        uuid: Agent UUID

    Returns:
        True if parameters are valid, False otherwise
    """
    if name is None and uuid is None:
        ui.error("Either --name or --uuid must be provided.")
        return False

    if name is not None and uuid is not None:
        ui.error("Only one of --name or --uuid can be provided.")
        return False

    return True


def _load_configuration(ui: UI) -> Optional[Config]:
    """
    Load application configuration.

    Args:
        ui: UI instance

    Returns:
        Config object if successful, None otherwise
    """
    try:
        config = Config()
        return config
    except Exception as e:
        ui.error(f"Failed to load configuration: {str(e)}")
        return None


def _find_agent_to_remove(
    ui: UI, agents: List[Dict[str, Any]], name: Optional[str], uuid: Optional[str]
) -> Tuple[Optional[Dict[str, Any]], Optional[int]]:
    """
    Find the agent to remove by name or UUID.

    Args:
        ui: UI instance
        agents: List of agents
        name: Agent name to find
        uuid: Agent UUID to find

    Returns:
        Tuple of (agent, index) if found, (None, None) otherwise
    """
    agent = None
    agent_index = None

    identifier_type = "name" if name is not None else "UUID"
    identifier_value = name if name is not None else uuid

    ui.info(f"Searching for agent with {identifier_type}: {identifier_value}")

    if name is not None:
        # Find the agent with the matching name
        for i, e in enumerate(agents):
            if e["name"] == name:
                agent = e
                agent_index = i
                break

        if agent_index is None:
            ui.error(f"Agent '{name}' not found in the current application.")
            return None, None

    elif uuid is not None:
        # Find the agent with the matching UUID
        for i, e in enumerate(agents):
            if e.get("uuid") == uuid:
                agent = e
                agent_index = i
                break

        if agent_index is None:
            ui.error(f"Agent with UUID '{uuid}' not found in the current application.")
            return None, None

    return agent, agent_index


def _display_agent_details(ui: UI, agent: Dict[str, Any]) -> None:
    """
    Display agent details in the UI.

    Args:
        ui: UI instance
        agent: Agent dictionary
    """
    ui.section("Agent Details")
    ui.value("Name", agent.get("name", "Unknown"))
    ui.value("Type", agent.get("type", "Unknown"))
    if "path" in agent:
        ui.path(agent["path"])
    if "uuid" in agent:
        ui.value("UUID", agent["uuid"])


def _remove_agent(
    ui: UI,
    config: Config,
    agents: List[Dict[str, Any]],
    agent: Dict[str, Any],
    agent_index: int,
    delete_files: bool,
    token: Optional[str],
) -> bool:
    """
    Remove the agent from configuration and optionally delete files.

    Args:
        ui: UI instance
        config: Config object
        agents: List of agents
        agent: Agent to remove
        agent_index: Index of agent in the list
        delete_files: Whether to delete agent files
        token: API token

    Returns:
        True if successful, False otherwise
    """
    try:

        def remove_agent_operation():
            # Remove the agent's files if requested
            if delete_files and "path" in agent:
                # Set delete_files to True by default if not explicitly specified
                ui.debug(f"Deleting agent files for {agent.get('name')}")
                delete_agent_files(agent, ui)

            # Remove the agent from the list
            agents.pop(agent_index)

            # Update the agents in the config
            config.set("endpoints", agents)

            # Save the updated config
            config.save()

            # If the agent was found and has a UUID, delete it from the database
            if agent and agent.get("uuid") is not None and token:
                ui.debug(f"Deleting agent from the AI-on-Rails database...")
                delete_agent = DeleteAgent(
                    token, app_id=config.get("uuid"), agent_uuid=agent["uuid"]
                )
                result = delete_agent.send()
                if result["status"] != "success":
                    raise Exception(result["message"])

            return True

        ui.process_spinner(
            f"Removing agent '{agent.get('name')}'", remove_agent_operation
        )
        return True
    except Exception as e:
        ui.error(f"Failed to remove agent: {str(e)}")
        return False


def delete_agent_files(agent: Dict[str, Any], ui: UI) -> None:
    """
    Delete the agent's source files from disk.

    Args:
        agent: Agent dictionary
        ui: UI instance
    """
    # Get the file path from the agent
    file_path = agent.get("path")
    if not file_path:
        ui.warning("No file path specified for this agent. Nothing to delete.")
        return

    ui.section("Deleting Files")

    try:
        # Get the full path to the file
        path = Path(file_path)
        agent_name = agent.get("name")  # Use agent name from dict instead of path.stem

        ui.debug(f"Agent path: {path}")
        ui.debug(f"Agent name: {agent_name}")

        # Prioritize deleting full agent directory
        found_any_files = False

        # First, try to find and delete the agent directory directly
        # Common patterns for agent directories
        possible_agent_dirs = [
            path.parent / agent_name,  # src/agent_name/
            path.parent / path.stem,  # src/agent_module/
            path,  # If path itself is a directory
        ]

        # Also check parent directories that might contain the agent
        if path.parent.name == agent_name:
            possible_agent_dirs.append(path.parent)  # The parent directory is the agent

        # Find and delete the first matching directory
        for agent_dir in possible_agent_dirs:
            if agent_dir.exists() and agent_dir.is_dir():
                ui.debug(f"Found agent directory: {agent_dir}")
                ui.path(str(agent_dir))
                ui.debug(f"Deleting agent directory: {agent_dir}")

                shutil.rmtree(agent_dir)
                ui.success(f"Deleted agent directory: {agent_dir}")
                found_any_files = True
                break

        # If we couldn't find a main agent directory, try to find individual files
        if not found_any_files:
            ui.debug("No agent directories found, trying individual files")

            # Build patterns for agent files
            patterns = [
                f"{agent_name}.py",
                f"{agent_name}_*.py",
                f"*_{agent_name}.py",
                f"{path.stem}.py",
                f"{path.stem}_*.py",
                f"*_{path.stem}.py",
            ]

            # Look for files in the parent directory
            for pattern in patterns:
                for file in path.parent.glob(pattern):
                    if file.exists():
                        ui.debug(f"Deleting file: {file}")
                        file.unlink()
                        ui.path(str(file))
                        found_any_files = True

            # If specified file exists but wasn't caught by patterns, delete it too
            if path.exists() and path.is_file():
                ui.debug(f"Deleting specified file: {path}")
                path.unlink()
                ui.path(str(path))
                found_any_files = True

        if found_any_files:
            ui.success("Agent files deleted successfully.")
        else:
            ui.warning(f"Could not find any files related to {file_path}.")

    except Exception as e:
        ui.error(f"Error deleting agent files: {str(e)}")


def _get_files_to_check(path: Path) -> List[Path]:
    """
    Get a list of files and directories to check for deletion.

    Args:
        path: Base path

    Returns:
        List of paths to check
    """
    files_to_check = []

    # Get the agent name from the path
    agent_name = path.stem

    # Check for the main file patterns
    name_patterns = [
        path,  # Original path (e.g., src/agent_name.py)
        path.parent / agent_name,  # Module directory (e.g., src/agent_name/)
    ]

    # Add potential file patterns based on naming conventions
    for pattern in [f"{agent_name}_*.py", f"*_{agent_name}.py"]:
        files_to_check.extend(list(path.parent.glob(pattern)))

    # Add the primary patterns
    files_to_check.extend(name_patterns)

    return files_to_check


def _delete_item(item: Path, ui: UI) -> None:
    """
    Delete a file or directory.

    Args:
        item: Path to delete
        ui: UI instance
    """
    try:
        if item.is_dir():
            ui.debug(f"Deleting directory: {item}")
            # Delete the entire directory tree
            shutil.rmtree(item)
            ui.path(str(item))

            # Also check for nested duplicated structure
            agent_name = item.name
            nested_path = item / "src" / agent_name
            if nested_path.exists():
                ui.debug(f"Deleting nested directory: {nested_path}")
                shutil.rmtree(nested_path)
                ui.path(str(nested_path))
        else:
            ui.debug(f"Deleting file: {item}")
            item.unlink()
            ui.path(str(item))
    except Exception as e:
        ui.warning(f"Error deleting {item}: {str(e)}")


def get_dependencies_for_type(agent_type: str) -> Set[str]:
    """
    Get the dependencies required for a specific agent type.

    Args:
        agent_type: Type of agent

    Returns:
        Set of dependency names
    """
    dependencies = set()

    # Add type-specific dependencies
    if agent_type == "langchain":
        dependencies.update(["langchain", "langchain_anthropic"])
    elif agent_type == "pydantic":
        dependencies.add("pydantic")
    elif agent_type == "langgraph":
        dependencies.update(["langgraph", "anthropic"])
    elif agent_type == "a2a":
        dependencies.update(["fastapi", "uvicorn", "pydantic"])

    # Always include development dependencies
    if agent_type in PYTHON_AGENT_TYPES:
        dependencies.update(["pytest", "black", "isort", "ruff", "pytest-cov"])

    return dependencies


def cleanup_dependencies(
    remaining_agents: List[Dict[str, Any]],
    dependencies_to_check: Set[str],
    skip_uninstall: bool = False,
    ui: Optional[UI] = None,
) -> None:
    """
    Remove dependencies that are no longer needed by any agent.
    Only removes dependencies if they're not used by remaining agents.

    Args:
        remaining_agents: List of agents still in the application
        dependencies_to_check: Set of dependencies to check for removal
        skip_uninstall: If True, only update requirements.txt without uninstalling packages
        ui: UI instance for displaying output
    """
    if ui is None:
        ui = UI()

    ui.section("Dependency Cleanup")

    # Find dependencies still in use and those that can be removed
    needed_dependencies, dependencies_to_remove = _identify_dependencies_to_remove(
        remaining_agents, dependencies_to_check
    )

    if not dependencies_to_remove:
        ui.info("No dependencies to remove.")
        return

    ui.info(f"Found unused dependencies:")
    for dep in dependencies_to_remove:
        ui.value("Package", dep)

    # Update the requirements.txt file if it exists
    _update_requirements_file(ui, dependencies_to_remove)

    # Skip the physical uninstallation if requested
    if skip_uninstall:
        ui.info("Skipping dependency uninstallation as requested.")
        return

    # Check if we have Poetry and remove dependencies
    _uninstall_dependencies_with_poetry(ui, dependencies_to_remove)


def _identify_dependencies_to_remove(
    remaining_agents: List[Dict[str, Any]], dependencies_to_check: Set[str]
) -> Tuple[Set[str], Set[str]]:
    """
    Identify which dependencies are still needed and which can be removed.

    Args:
        remaining_agents: List of agents still in the application
        dependencies_to_check: Set of dependencies to check for removal

    Returns:
        Tuple of (needed_dependencies, dependencies_to_remove)
    """
    # Find the dependencies still in use by other agents
    needed_dependencies = set()
    for agent in remaining_agents:
        agent_type = agent.get("type", "")
        needed_dependencies.update(get_dependencies_for_type(agent_type))

    # Find dependencies that can be safely removed
    dependencies_to_remove = dependencies_to_check - needed_dependencies

    return needed_dependencies, dependencies_to_remove


def _update_requirements_file(ui: UI, dependencies_to_remove: Set[str]) -> None:
    """
    Update the requirements.txt file to remove unused dependencies.

    Args:
        ui: UI instance
        dependencies_to_remove: Set of dependencies to remove
    """
    requirements_path = Path("requirements.txt")
    if not requirements_path.exists():
        return

    try:

        def update_requirements():
            # Read the current requirements
            with open(requirements_path, "r", encoding="utf-8") as f:
                requirements = f.readlines()

            # Filter out the dependencies to remove
            updated_requirements = []
            removed_any = False
            removed_packages = []

            for req in requirements:
                req_name = req.strip().split("==")[0].split(">=")[0].strip()
                if req_name in dependencies_to_remove:
                    removed_packages.append(req_name)
                    removed_any = True
                else:
                    updated_requirements.append(req)

            # Write the updated requirements
            if removed_any:
                with open(requirements_path, "w", encoding="utf-8") as f:
                    f.writelines(updated_requirements)

            return removed_packages

        removed_packages = ui.process_spinner(
            "Updating requirements.txt", update_requirements
        )

        if removed_packages:
            ui.success(
                f"Removed {len(removed_packages)} packages from requirements.txt"
            )
            for pkg in removed_packages:
                ui.value("Removed", pkg)
        else:
            ui.info("No changes made to requirements.txt")

    except Exception as e:
        ui.error(f"Error updating requirements.txt: {str(e)}")


def _uninstall_dependencies_with_poetry(
    ui: UI, dependencies_to_remove: Set[str]
) -> None:
    """
    Uninstall dependencies using Poetry.

    Args:
        ui: UI instance
        dependencies_to_remove: Set of dependencies to remove
    """
    try:
        # Check if Poetry is available
        def check_poetry():
            subprocess.run(
                ["poetry", "--version"], check=True, capture_output=True, text=True
            )
            return True

        try:
            ui.process_spinner("Checking for Poetry", check_poetry)
        except Exception:
            ui.warning("Poetry is not available or not working correctly.")
            return

        # Check which dependencies are actually installed and remove them
        for dep in dependencies_to_remove:
            _uninstall_dependency(ui, dep)

    except Exception as e:
        ui.error(f"Error during dependency cleanup: {str(e)}")


def _uninstall_dependency(ui: UI, dep: str) -> None:
    """
    Uninstall a single dependency using Poetry.

    Args:
        ui: UI instance
        dep: Dependency name to uninstall
    """
    try:
        # First check if the dependency is installed
        def check_dependency():
            check_cmd = ["poetry", "show", dep]
            subprocess.run(check_cmd, check=True, capture_output=True, text=True)
            return True

        try:
            is_installed = ui.process_spinner(
                f"Checking if {dep} is installed", check_dependency
            )
        except Exception:
            ui.debug(f"Dependency {dep} is not installed, skipping")
            return

        # If we get here, the dependency is installed - try to remove it
        # Check if it's a dev dependency
        is_dev = dep in ["pytest", "black", "isort", "ruff", "pytest-cov"]

        def remove_dependency():
            cmd = ["poetry", "remove"]
            if is_dev:
                cmd.append("--dev")
            cmd.append(dep)

            subprocess.run(cmd, check=True, capture_output=True, text=True)
            return True

        ui.process_spinner(f"Removing dependency {dep}", remove_dependency)
        ui.success(f"Removed {dep}")

    except Exception as e:
        ui.error(f"Failed to remove {dep}: {str(e)}")
