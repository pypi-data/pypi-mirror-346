"""
Template module for AI-on-Rails.
Provides a modular template system for creating AI agents with various
protocols, frameworks, and deployment options.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional
import traceback

# Import UI
from aor.utils.ui import UI

# Import components from utilities
from .utils.template_manager import TemplateManager
from .utils.component_combiner import ComponentCombiner
from .utils.dependency_manager import DependencyManager
from .utils.template_renderer import TemplateRenderer
from .utils.file_condition_evaluator import FileConditionEvaluator

# Get the templates directory
TEMPLATES_DIR = Path(__file__).parent

# Create UI instance
_ui = UI(debug_mode=False)

# Create singleton instances
_template_manager = TemplateManager(TEMPLATES_DIR, ui=_ui)
_component_combiner = ComponentCombiner(TEMPLATES_DIR, ui=_ui)
_dependency_manager = DependencyManager(ui=_ui)
_condition_evaluator = FileConditionEvaluator()

# Public API functions


def list_templates() -> Dict[str, List[Dict[str, Any]]]:
    """
    List all available templates grouped by category.

    Returns:
        Dictionary with categories as keys and lists of templates as values
    """
    _ui.debug("Listing templates...")
    return _template_manager.list_templates()


def get_template_metadata(
    category: str, template_name: str
) -> Optional[Dict[str, Any]]:
    """
    Get metadata for a specific template.

    Args:
        category: Template category (e.g., 'core', 'protocols', 'frameworks')
        template_name: Name of the template

    Returns:
        Template metadata or None if not found
    """
    _ui.debug(f"Getting metadata for {category}/{template_name}")
    return _template_manager.get_template_metadata(category, template_name)


def apply_template(
    category: str,
    template_name: str,
    agent_name: str,
    agent_desc: Optional[str] = None,
    output_dir: str = None,
    **kwargs,
) -> bool:
    """
    Apply a template to create files for an agent.

    Args:
        category: Template category
        template_name: Template name
        agent_name: Name of the agent to create
        agent_desc: Description of the agent
        output_dir: Optional output directory path
        **kwargs: Additional parameters for the template

    Returns:
        True if successful, False otherwise
    """
    _ui.debug(f"Applying template {category}/{template_name} for agent {agent_name}")
    _ui.debug(f"Output directory: {output_dir}")
    _ui.debug(f"Additional parameters: {kwargs}")

    template_dir = _template_manager.get_template_path(category, template_name)
    _ui.debug(f"Template directory: {template_dir}")

    # Check if template exists
    if not template_dir.exists() or not template_dir.is_dir():
        _ui.error(f"Template {category}/{template_name} not found at {template_dir}")
        return False

    # Get template metadata
    metadata = _template_manager.get_template_metadata(category, template_name)
    if not metadata:
        _ui.error(
            f"Invalid template: metadata.yaml not found for {category}/{template_name}."
        )
        return False

    _ui.debug(f"Template metadata: {metadata}")

    # Initialize renderer
    renderer = TemplateRenderer(template_dir, ui=_ui)

    # Process template
    success = _process_template_files(
        renderer=renderer,
        metadata=metadata,
        agent_name=agent_name,
        agent_desc=agent_desc,
        output_dir=output_dir,
        **kwargs,
    )

    # Handle dependencies if template was successfully applied
    if success and "dependencies" in metadata and metadata["dependencies"]:
        _ui.debug(f"Handling dependencies: {metadata['dependencies']}")
        _handle_dependencies(metadata["dependencies"])

    return success


def _process_template_files(
    renderer: TemplateRenderer,
    metadata: Dict[str, Any],
    agent_name: str,
    agent_desc: Optional[str] = None,
    output_dir: Optional[str] = None,
    **kwargs,
) -> bool:
    """
    Process all files in the template.

    Args:
        renderer: Template renderer instance
        metadata: Template metadata
        agent_name: Name of the agent
        agent_desc: Description of the agent
        output_dir: Optional output directory path
        **kwargs: Additional parameters for the template

    Returns:
        True if successful, False otherwise
    """
    _ui.debug(f"Processing template files for {agent_name}")
    _ui.debug(f"Using output directory: {output_dir}")

    # Get template type
    template_type = metadata.get("templateType", "agent")
    _ui.debug(f"Template type: {template_type}")

    # Prepare parameters
    params = {
        "agent_name": agent_name,
        "agent_desc": agent_desc
        or metadata.get("parameters", {})
        .get("agent_desc", {})
        .get("default", f"A {template_type} agent"),
    }

    # Add additional parameters
    params.update(kwargs)
    _ui.debug(f"Template parameters: {params}")

    # Process each file in the template
    if "files" in metadata:
        _ui.debug(f"Processing {len(metadata['files'])} files")
        for file_info in metadata.get("files", []):
            _ui.debug(f"Processing file: {file_info}")

            # Check condition for file inclusion
            condition_context = {"template_type": template_type}
            condition_context.update(
                params
            )  # Include all parameters for condition evaluation

            if "condition" in file_info and not _condition_evaluator.evaluate(
                file_info["condition"], condition_context
            ):
                _ui.debug(
                    f"Skipping file due to condition: {file_info.get('source', 'unknown')}"
                )
                continue

            try:
                # Process the file
                success = _process_single_file(renderer, file_info, params, output_dir)
                if not success:
                    _ui.error(
                        f"Failed to process file: {file_info.get('source', 'unknown')}"
                    )
                    continue
            except Exception as e:
                _ui.error(
                    f"Error processing file {file_info.get('source', 'unknown')}: {str(e)}"
                )
                _ui.error(traceback.format_exc())
                continue
    else:
        _ui.warning("No files defined in template metadata")

    return True


def _process_single_file(
    renderer: TemplateRenderer,
    file_info: Dict[str, Any],
    params: Dict[str, Any],
    output_dir: Optional[str] = None,
) -> bool:
    """
    Process a single file from the template.

    Args:
        renderer: Template renderer
        file_info: File information from metadata
        params: Parameters for template rendering
        output_dir: Optional output directory path

    Returns:
        True if successful, False otherwise
    """
    source_path = file_info["source"]
    _ui.debug(f"Processing single file: {source_path}")

    # Check if source is a template file
    template_file = renderer.template_dir / source_path
    if not template_file.exists():
        # Try with .j2 extension
        template_file = renderer.template_dir / f"{source_path}.j2"
        if not template_file.exists():
            _ui.warning(
                f"Source file {source_path} not found in template at {renderer.template_dir}"
            )
            return False

    _ui.debug(f"Template file found: {template_file}")

    # Get relative path from template directory
    relative_source = template_file.relative_to(renderer.template_dir)
    _ui.debug(f"Relative source: {relative_source}")

    # Process the destination path with Jinja2
    dest_path_str = renderer.render_string(file_info["destination"], params)
    _ui.debug(f"Destination path after rendering: {dest_path_str}")

    # Fix path duplication issue: if output_dir is "src" and dest_path starts with "src/", remove the duplicate
    if (
        output_dir
        and str(output_dir).rstrip("/\\") == "src"
        and dest_path_str.startswith("src/")
    ):
        dest_path_str = dest_path_str[4:]  # Remove leading "src/"
        _ui.debug(f"Fixed duplicate path, new destination: {dest_path_str}")

    # Create full destination path
    dest_path = Path(output_dir) / dest_path_str if output_dir else Path(dest_path_str)
    _ui.debug(f"Full destination path: {dest_path}")

    # Create destination directory if needed
    _ui.debug(f"Creating parent directory: {dest_path.parent}")
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if the file already exists before rendering content
    if dest_path.exists() and not file_info.get("overwrite", False):
        # Special handling for README.md files
        if dest_path.name == "README.md":
            # Render template content for README files
            content = renderer.render_template(str(relative_source), params)
            _ui.debug(f"Updating existing README: {dest_path}")
            _update_readme(dest_path, content, params["agent_name"])
            return True
        else:
            _ui.debug(
                f"Skipping existing file: {dest_path} (use 'overwrite: true' in metadata to force)"
            )
            return True

    # Render template content using Jinja2
    try:
        _ui.debug(f"Rendering template: {relative_source}")
        content = renderer.render_template(str(relative_source), params)
    except Exception as e:
        _ui.error(f"Error rendering template {relative_source}: {str(e)}")
        _ui.error(traceback.format_exc())
        return False

    # Write the processed content
    try:
        _ui.debug(f"Writing content to: {dest_path}")
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(content)
        _ui.debug(f"Successfully created file: {dest_path}")
    except Exception as e:
        _ui.error(f"Error writing file {dest_path}: {str(e)}")
        _ui.error(traceback.format_exc())
        return False

    return True


def _update_readme(readme_path: Path, content: str, agent_name: str) -> None:
    """
    Update an existing README.md file with agent-specific content.

    Args:
        readme_path: Path to the README file
        content: New content to add
        agent_name: Name of the agent for section header
    """
    _ui.debug(f"Updating README at {readme_path} for agent {agent_name}")
    # Read existing README
    with open(readme_path, "r", encoding="utf-8") as f:
        existing_content = f.read()

    # Add or update agent section
    agent_header = f"## {agent_name}"
    if agent_header in existing_content:
        # Replace existing section
        parts = existing_content.split(agent_header)
        pre_content = parts[0]

        # Find the beginning of the next section (if any)
        post_content = ""
        if len(parts) > 1:
            next_section_pos = parts[1].find("## ")
            if next_section_pos != -1:
                post_content = parts[1][next_section_pos:]

        # Write updated content
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"{pre_content}{agent_header}\n\n{content}\n\n{post_content}")
    else:
        # Add new section
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"{existing_content}\n\n{agent_header}\n\n{content}")


def _handle_dependencies(dependencies: List[str]) -> None:
    """
    Handle dependencies specified in the template.

    Args:
        dependencies: List of dependencies to manage
    """
    _ui.debug(f"Handling dependencies: {dependencies}")
    dependency_set = set(dependencies)

    # Update requirements.txt
    new_deps = _dependency_manager.update_requirements(dependency_set)

    if new_deps:
        _ui.debug(f"Added {len(new_deps)} new dependencies to requirements.txt")

        # Install new dependencies
        results = _dependency_manager.install_dependencies(new_deps)

        if results["installed"]:
            _ui.debug(f"Installed dependencies: {', '.join(results['installed'])}")

        if results["failed"]:
            _ui.error(
                f"Failed to install: {', '.join([item['dependency'] for item in results['failed']])}"
            )


def combine_components(
    components: List[str], agent_name: str, output_dir: str, **kwargs
) -> bool:
    """
    Combine multiple components to create a complete agent.

    Args:
        components: List of component paths (e.g., ["core/langgraph", "protocols/a2a"])
        agent_name: Name of the agent
        output_dir: Output directory for the agent
        **kwargs: Additional parameters for components

    Returns:
        True if successful, False otherwise
    """
    _ui.debug(f"Attempting to combine components for '{agent_name}':")
    for comp in components:
        _ui.debug(f"  - {comp}")
    _ui.debug(f"Output directory: {output_dir}")
    _ui.debug(f"Additional parameters: {kwargs}")

    # Ensure output directory exists
    try:
        if not os.path.exists(output_dir):
            _ui.debug(f"Creating output directory: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)
        else:
            _ui.debug(f"Output directory already exists: {output_dir}")
    except Exception as e:
        _ui.error(f"Failed to create output directory: {str(e)}")
        return False

    # Use component_combiner for actual combination - make sure path duplication prevention is handled
    kwargs["_prevent_path_duplication"] = True
    return _component_combiner.combine_components(
        components, agent_name, Path(output_dir), **kwargs
    )


def validate_component_compatibility(components: List[str]) -> Dict[str, Any]:
    """
    Validate if the given components are compatible with each other.

    Args:
        components: List of component paths

    Returns:
        Validation result with details
    """
    _ui.debug(f"Validating compatibility for components: {components}")
    return _component_combiner.validate_compatibility(components)


def get_component_dependencies(components: List[str]) -> Dict[str, List[str]]:
    """
    Get all dependencies for the given components.

    Args:
        components: List of component paths

    Returns:
        Dictionary mapping component names to their dependencies
    """
    _ui.debug(f"Getting dependencies for components: {components}")
    return _component_combiner.get_component_dependencies(components)


# Export main classes and functions
__all__ = [
    "list_templates",
    "get_template_metadata",
    "apply_template",
    "combine_components",
    "validate_component_compatibility",
    "get_component_dependencies",
    "TemplateManager",
    "ComponentCombiner",
    "DependencyManager",
    "TemplateRenderer",
    "FileConditionEvaluator",
]
