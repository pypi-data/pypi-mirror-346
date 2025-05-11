"""
File preparation utilities for deployment.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any

from aor.utils.ui import UI


def prepare_agent_files(
    ui: UI, agent: Dict[str, Any], agent_dir: Path, folder_name: Optional[str] = None
) -> Optional[Path]:
    """
    Copy agent files to deployment directory.

    Args:
        ui: UI instance for displaying messages
        agent: Agent configuration dictionary
        agent_dir: Target directory for agent files
        folder_name: Optional name to use for the agent folder (defaults to agent["name"])

    Returns:
        Path to the prepared agent directory or None if preparation failed
    """
    try:
        if "path" not in agent:
            ui.error(f"Agent {agent['name']} has no path specified")
            return None

        agent_path = Path(agent["path"])
        if not agent_path.exists():
            ui.error(f"Agent path does not exist: {agent_path}")
            return None

        ui.debug(
            f"Processing agent path: {agent_path} (is_dir={agent_path.is_dir()}, is_file={agent_path.is_file()})"
        )

        # First, copy deployment templates to the root directory
        deployment_templates_copied = False

        # Try agent-specific deployment templates first
        agent_deploy_templates = (
            agent_path / "deployments" / "lambda"
            if agent_path.is_dir()
            else agent_path.parent / "deployments" / "lambda"
        )

        if agent_deploy_templates.exists():
            ui.debug(f"Found agent deployment templates at: {agent_deploy_templates}")
            # Copy template files
            for item in agent_deploy_templates.glob("*"):
                if item.is_file() and item.name not in ["__init__.py", "__pycache__"]:
                    dest_path = agent_dir / item.name
                    shutil.copy2(item, dest_path)
                    ui.debug(f"Copied agent template: {item.name}")

            # Also copy the scripts directory if it exists
            scripts_dir = agent_deploy_templates / "scripts"
            if scripts_dir.exists() and scripts_dir.is_dir():
                dest_scripts_dir = agent_dir / "scripts"
                dest_scripts_dir.mkdir(exist_ok=True)
                for script in scripts_dir.glob("*"):
                    if script.is_file() and script.name not in [
                        "__init__.py",
                        "__pycache__",
                    ]:
                        dest_script = dest_scripts_dir / script.name
                        shutil.copy2(script, dest_script)
                        # Make script executable on Unix-like systems
                        if os.name != "nt" and script.name.endswith(".sh"):
                            os.chmod(dest_script, 0o755)
                        ui.debug(f"Copied script: {script.name}")

            deployment_templates_copied = True

        # If no agent-specific templates, try common locations
        if not deployment_templates_copied:
            ui.debug(f"No deployment templates found at {agent_deploy_templates}")
            template_locations = [
                Path("deployments") / "lambda",
                Path("src") / "deployments" / "lambda",
                Path(__file__).parent.parent.parent.parent / "deployments" / "lambda",
            ]

            for location in template_locations:
                if location.exists():
                    ui.debug(f"Found deployment templates at: {location}")
                    for item in location.glob("*"):
                        if item.is_file() and item.name not in [
                            "__init__.py",
                            "__pycache__",
                        ]:
                            dest_path = agent_dir / item.name
                            shutil.copy2(item, dest_path)
                            ui.debug(f"Copied deployment template: {item.name}")
                    deployment_templates_copied = True
                    break

        if not deployment_templates_copied:
            ui.warning("Deployment templates not found in any known location")

        # Now copy the agent code files, preserving package structure
        # Find the project root (to preserve absolute imports)
        project_root = find_project_root(agent_path)
        ui.debug(f"Using project root: {project_root}")

        progress, task_id = ui.start_progress("Copying agent files")

        # Create agent folder inside agent_dir
        # Use provided folder_name if available, otherwise fall back to agent name
        agent_name = agent["name"]
        folder_to_use = folder_name if folder_name else agent_name
        agent_name_dir = agent_dir / folder_to_use
        agent_name_dir.mkdir(exist_ok=True)
        ui.debug(f"Created agent directory: {agent_name_dir} using folder name: {folder_to_use}")

        if agent_path.is_file():
            # Copy single file
            dest_file = agent_name_dir / agent_path.name
            shutil.copy2(agent_path, dest_file)
            ui.update_progress(1, f"Copied {agent_path.name}")
        elif agent_path.is_dir():
            # If it's a directory, copy while preserving package structure
            # 1. First determine if we need to create a package structure or just copy the directory
            ui.update_progress(0, "Analyzing imports")
            has_imports = check_for_absolute_imports(agent_path)

            if has_imports:
                ui.update_progress(0, "Preserving package structure")
                # Copy preserving package structure relative to project root
                files_copied = 0
                for item in agent_path.glob("**/*"):
                    if item.is_file():
                        # Skip __pycache__ and .aor-deploy directories using path-based check
                        if "__pycache__" in item.parts or ".aor-deploy" in item.parts:
                            ui.debug(f"Skipping file in excluded directory: {item}")
                            continue

                        try:
                            # Check if this file is from a previous deployment directory
                            if any(part == ".aor-deploy" for part in item.parts):
                                ui.debug(
                                    f"Skipping file from previous deployment: {item}"
                                )
                                continue

                            # Get path relative to project root to maintain import structure
                            if project_root and project_root in item.parents:
                                rel_path = item.relative_to(project_root)
                            else:
                                # Fallback to direct copy if can't determine project structure
                                rel_path = item.relative_to(agent_path.parent)

                            dest_path = agent_name_dir / rel_path
                            dest_path.parent.mkdir(parents=True, exist_ok=True)
                            ui.debug(f"Copying file from {item} to {dest_path}")
                            shutil.copy2(item, dest_path)
                            files_copied += 1
                            if files_copied % 5 == 0:  # Update progress every 5 files
                                ui.update_progress(0, f"Copied {files_copied} files")
                        except ValueError:
                            # If we can't determine the relative path, use a direct copy
                            # But avoid creating nested directories with the agent name
                            rel_path = item.relative_to(agent_path)
                            dest_path = agent_name_dir / rel_path
                            dest_path.parent.mkdir(parents=True, exist_ok=True)
                            ui.debug(
                                f"Copying file (direct) from {item} to {dest_path}"
                            )
                            shutil.copy2(item, dest_path)
                            files_copied += 1

                ui.update_progress(1, f"Copied {files_copied} files")
            else:
                ui.update_progress(0, "Simple directory copy")
                # Simple copy directly to agent directory (avoid nested subdirectory)
                files_copied = 0
                for item in agent_path.glob("**/*"):
                    if item.is_file():
                        # Skip __pycache__ and .aor-deploy directories using path-based check
                        if (
                            "__pycache__" in item.parts
                            or ".aor-deploy" in item.parts
                            or any(part == ".aor-deploy" for part in item.parts)
                        ):
                            ui.debug(f"Skipping file in excluded directory: {item}")
                            continue

                        rel_path = item.relative_to(agent_path)
                        dest_path = agent_name_dir / rel_path
                        dest_path.parent.mkdir(parents=True, exist_ok=True)
                        ui.debug(f"Copying file (simple) from {item} to {dest_path}")
                        shutil.copy2(item, dest_path)
                        files_copied += 1
                        if files_copied % 5 == 0:  # Update progress every 5 files
                            ui.update_progress(0, f"Copied {files_copied} files")

                ui.update_progress(1, f"Copied {files_copied} files")

        # Add __init__.py files to ensure proper Python package structure
        ui.update_progress(0, "Adding __init__.py files")
        ensure_init_files(agent_name_dir)

        # Create a symlink to the agent_name directory in the agent_dir for SAM deployment
        ui.update_progress(0, "Setting up deployment structure")

        # Copy template files to the agent_dir root for SAM deployment
        for item in agent_dir.glob("*"):
            if item.is_file() and item != agent_name_dir:
                # Keep template files at the root level
                ui.debug(f"Keeping template file at root: {item.name}")

        ui.stop_progress("File preparation complete")

        return agent_dir
    except Exception as e:
        ui.error(f"Error preparing agent files: {str(e)}")
        import traceback

        ui.debug(f"Stack trace: {traceback.format_exc()}")
        ui.stop_progress("File preparation failed")
        return None


def find_project_root(agent_path: Path) -> Optional[Path]:
    """
    Find the project root directory to preserve absolute imports.

    Args:
        agent_path: Path to the agent file or directory

    Returns:
        Path to the project root or None if not found
    """
    current = agent_path if agent_path.is_dir() else agent_path.parent

    # Look for typical project markers
    for _ in range(8):  # Don't go up too many levels
        # Check for setup.py, pyproject.toml, or .git directory
        for marker in ["setup.py", "pyproject.toml", ".git"]:
            if (current / marker).exists():
                return current

        # Move up one directory
        parent = current.parent
        if parent == current:  # We've reached the root
            break
        current = parent

    return None


def check_for_absolute_imports(directory: Path) -> bool:
    """
    Check if the directory contains Python files with absolute imports.

    Args:
        directory: Directory to check for absolute imports

    Returns:
        True if absolute imports are found, False otherwise
    """
    import re

    absolute_import_pattern = re.compile(
        r"^\s*from\s+[a-zA-Z_][a-zA-Z0-9_]*\s+import|^\s*import\s+[a-zA-Z_][a-zA-Z0-9_]*\s*$"
    )

    for py_file in directory.glob("**/*.py"):
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                content = f.read()
                if absolute_import_pattern.search(content, re.MULTILINE):
                    return True
        except Exception:
            continue

    return False


def ensure_init_files(directory: Path) -> None:
    """
    Ensure all directories have __init__.py files for proper Python package structure.

    Args:
        directory: Directory to ensure __init__.py files in
    """
    for dir_path in directory.glob("**/"):
        init_file = dir_path / "__init__.py"
        if not init_file.exists() and any(
            f.name.endswith(".py") for f in dir_path.glob("*.py")
        ):
            with open(init_file, "w") as f:
                f.write("# Auto-generated __init__.py file\n")


def modify_template_yaml(ui: UI, template_file: Path) -> bool:
    """
    Modify template.yaml to remove A2A layer dependency.

    Args:
        ui: UI instance for displaying messages
        template_file: Path to the template.yaml file

    Returns:
        True if modification was successful, False otherwise
    """
    try:
        if not template_file.exists():
            ui.warning(f"Template file does not exist: {template_file}")
            return False

        ui.info("Modifying template.yaml to remove A2A layer dependency...")
        with open(template_file, "r") as f:
            template_content = f.read()

        # Parse the YAML content
        import yaml

        try:
            # Try to parse with PyYAML
            template_data = yaml.safe_load(template_content)

            # Remove the A2A layer resource
            if (
                "Resources" in template_data
                and "A2ALayer" in template_data["Resources"]
            ):
                del template_data["Resources"]["A2ALayer"]

            # Remove references to the A2A layer in the AgentFunction
            if (
                "Resources" in template_data
                and "AgentFunction" in template_data["Resources"]
                and "Properties" in template_data["Resources"]["AgentFunction"]
                and "Layers"
                in template_data["Resources"]["AgentFunction"]["Properties"]
            ):
                # Filter out any references to A2ALayer
                layers = template_data["Resources"]["AgentFunction"]["Properties"][
                    "Layers"
                ]
                filtered_layers = [
                    layer
                    for layer in layers
                    if not (isinstance(layer, str) and "A2ALayer" in layer)
                ]
                if filtered_layers:
                    template_data["Resources"]["AgentFunction"]["Properties"][
                        "Layers"
                    ] = filtered_layers
                else:
                    # If no layers left, remove the Layers property
                    del template_data["Resources"]["AgentFunction"]["Properties"][
                        "Layers"
                    ]

            # Write the modified template back
            with open(template_file, "w") as f:
                yaml.dump(template_data, f, default_flow_style=False)

            ui.success(
                "Modified template.yaml to remove A2A layer dependency using YAML parser"
            )
            return True
        except Exception as yaml_error:
            ui.warning(f"YAML parsing failed: {str(yaml_error)}")

            # Fallback to regex-based approach
            ui.info("Falling back to regex-based template modification...")

            # Remove the A2A layer resource and references
            modified_content = []
            skip_section = False
            layer_ref_pattern = r"!Ref\s+A2ALayer"

            for line in template_content.splitlines():
                # Skip the A2A layer resource section
                if line.strip().startswith("A2ALayer:"):
                    skip_section = True
                    continue

                if skip_section:
                    if line.strip().startswith("RetentionPolicy:"):
                        skip_section = False
                        continue
                    else:
                        continue

                # Remove references to the A2A layer
                if re.search(layer_ref_pattern, line):
                    continue

                modified_content.append(line)

            # Write the modified template back
            with open(template_file, "w") as f:
                f.write("\n".join(modified_content))

            ui.success(
                "Modified template.yaml to remove A2A layer dependency using regex"
            )
            return True
    except Exception as e:
        ui.warning(f"Failed to modify template.yaml: {str(e)}")
        return False
