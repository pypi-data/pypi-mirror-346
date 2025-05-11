"""
Component combination logic for AI-on-Rails templates.
"""

import os
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from ruamel.yaml import YAML
import traceback

from aor.templates.utils.template_manager import TemplateManager
from aor.templates.utils.dependency_manager import DependencyManager
from aor.templates.utils.file_generator import FileGenerator
from aor.templates.utils.template_renderer import TemplateRenderer
from aor.templates.utils.validators.compatibility import CompatibilityValidator


class ComponentCombiner:
    """
    Combines different components (core, protocols, deployments)
    # Note: Framework functionality is currently disabled
    into a complete working agent.
    """

    def __init__(self, templates_dir: Path, ui):
        """
        Initialize the component combiner.

        Args:
            templates_dir: Root directory containing all templates
            ui: UI instance for displaying messages
        """
        self.templates_dir = templates_dir
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.indent = 2
        self.ui = ui

        self.template_manager = TemplateManager(templates_dir, ui=ui)
        self.dependency_manager = DependencyManager(ui=ui)
        self.file_generator = FileGenerator(ui=ui)
        self.compatibility_validator = CompatibilityValidator()

        self.ui.debug(
            f"Initialized ComponentCombiner with templates_dir: {templates_dir}"
        )

    def validate_compatibility(self, components: List[str]) -> Dict[str, Any]:
        """
        Validate if the given components are compatible with each other.

        Args:
            components: List of component paths

        Returns:
            Validation result with details
        """
        self.ui.debug(f"Validating compatibility for components: {components}")

        # Load metadata for all components
        metadata_list = []
        for component_path in components:
            category, component_name = component_path.split("/")
            metadata = self.template_manager.get_template_metadata(
                category, component_name
            )
            if metadata:
                metadata["path"] = component_path
                metadata_list.append(metadata)
            else:
                self.ui.warning(f"Could not load metadata for {component_path}")

        self.ui.debug(f"Loaded metadata for {len(metadata_list)} components")

        result = self.compatibility_validator.validate_components(metadata_list)
        self.ui.debug(f"Validation result: {result}")

        return result

    def combine_components(
        self, components: List[str], agent_name: str, output_dir: Path, **kwargs
    ) -> bool:
        """
        Combine multiple components into a working agent.

        Args:
            components: List of component paths (e.g., ["core/langgraph", "protocols/a2a"])
            agent_name: Name of the agent
            output_dir: Where to generate the agent
            **kwargs: Additional parameters for components

        Returns:
            True if successful, False otherwise
        """
        self.ui.debug(
            f"Starting to combine {len(components)} components for agent '{agent_name}'"
        )
        self.ui.debug(f"Components: {components}")
        self.ui.debug(f"Output directory: {output_dir}")
        self.ui.debug(f"Additional parameters: {kwargs}")

        # Validate compatibility first
        validation_result = self.validate_compatibility(components)
        if not validation_result["compatible"]:
            self.ui.error(f"Incompatible components: {validation_result['errors']}")
            return False

        # Sort components by type (core should be first)
        sorted_components = self._sort_components(components)
        self.ui.debug(f"Sorted components: {sorted_components}")

        # Create output directory
        try:
            os.makedirs(output_dir, exist_ok=True)
            self.ui.debug(f"Created output directory: {output_dir}")
        except Exception as e:
            self.ui.error(f"Failed to create output directory {output_dir}: {str(e)}")
            return False

        # Process components in order
        combined_metadata = {}
        combined_dependencies = set()
        # Extract inputs and outputs from kwargs if available
        inputs = kwargs.get("inputs", [])
        outputs = kwargs.get("outputs", [])

        # Create parameters dictionary with agent name, inputs, and outputs
        parameters = {
            "agent_name": agent_name,
            "endpoint": {"name": agent_name, "inputs": inputs, "outputs": outputs},
            **kwargs,
        }

        # First, copy base files for all specified components
        try:
            self._copy_base_files(output_dir, agent_name, sorted_components, parameters)
        except Exception as e:
            self.ui.error(f"Failed to copy base files: {str(e)}")
            self.ui.error(traceback.format_exc())
            return False

        for component_path in sorted_components:
            self.ui.debug(f"Processing component: {component_path}")
            category, component_name = component_path.split("/")

            # Get component metadata
            metadata = self.template_manager.get_template_metadata(
                category, component_name
            )
            if not metadata:
                self.ui.error(f"Failed to get metadata for {component_path}")
                return False

            self.ui.debug(f"Got metadata for {component_path}: {metadata}")

            # Merge metadata
            combined_metadata = self._merge_metadata(combined_metadata, metadata)

            # Collect dependencies
            if "dependencies" in metadata:
                combined_dependencies.update(metadata["dependencies"])
                self.ui.debug(
                    f"Added dependencies from {component_path}: {metadata['dependencies']}"
                )

            # Apply component
            component_dir = self.templates_dir / category / component_name
            self.ui.debug(f"Component directory: {component_dir}")

            try:
                renderer = TemplateRenderer(component_dir, ui=self.ui)
                self.ui.debug(f"Created renderer for {component_dir}")
            except Exception as e:
                self.ui.error(f"Failed to create renderer for {component_dir}: {str(e)}")
                self.ui.error(traceback.format_exc())
                return False

            try:
                success = self.file_generator.generate_files(
                    component_dir, metadata, parameters, renderer, output_dir
                )
                if not success:
                    self.ui.error(
                        f"Failed to generate files for component {component_path}"
                    )
                    return False

                # Display created files as a group
                if self.file_generator.created_files:
                    # Group files by directory for better organization
                    files_by_dir = {}
                    for file_path in self.file_generator.created_files:
                        dir_name = os.path.dirname(file_path)
                        if not dir_name:
                            dir_name = "."
                        if dir_name not in files_by_dir:
                            files_by_dir[dir_name] = []
                        files_by_dir[dir_name].append(file_path)
                    
                    # Display each directory group separately
                    for dir_name, files in files_by_dir.items():
                        self.ui.group_file_operations(
                            f"Created Files in {dir_name}", files
                        )

                self.ui.debug(f"Successfully applied component {component_path}")
            except Exception as e:
                self.ui.error(
                    f"Exception generating files for {component_path}: {str(e)}"
                )
                self.ui.error(traceback.format_exc())
                return False

        # Handle dependencies
        if combined_dependencies:
            self.ui.debug(f"Handling combined dependencies: {combined_dependencies}")
            project_root = Path.cwd()
            self.dependency_manager.update_requirements(
                combined_dependencies, project_root / "requirements.txt"
            )

        self.ui.debug("Successfully combined all components")
        return True

    def _copy_base_files(
        self,
        output_dir: Path,
        agent_name: str,
        components: List[str],
        parameters: Dict[str, Any],
    ) -> None:
        """
        Copy base files for all specified components using TemplateRenderer and metadata.

        Args:
            output_dir: Project output directory
            agent_name: Name of the agent
            components: List of component paths to process
            parameters: Parameters for template rendering
        """
        self.ui.debug(
            "Copying base files for specified components using TemplateRenderer"
        )

        # Extract unique categories from component paths
        categories = set()
        for component_path in components:
            category = component_path.split("/")[0]
            categories.add(category)

        self.ui.debug(f"Categories to process: {categories}")

        # Process each category found in components
        for category in categories:
            self.ui.debug(f"Processing base files for category: {category}")

            # Check if base component exists
            base_dir = self.templates_dir / category / "base"
            if not base_dir.exists():
                self.ui.debug(f"No base directory found for category: {category}")
                continue

            # Get base component metadata
            base_metadata = self.template_manager.get_template_metadata(
                category, "base"
            )
            if not base_metadata:
                self.ui.debug(f"No base metadata found for category: {category}")
                continue

            self.ui.debug(
                f"Found base metadata for category {category}: {base_metadata}"
            )

            try:
                # Create renderer for base component
                renderer = TemplateRenderer(base_dir, ui=self.ui)
                self.ui.debug(f"Created renderer for {base_dir}")

                # Use FileGenerator to generate files from the base component
                success = self.file_generator.generate_files(
                    base_dir, base_metadata, parameters, renderer, output_dir
                )

                if success:
                    self.ui.debug(f"Successfully copied base files for {category}")
                else:
                    self.ui.warning(f"Failed to copy some base files for {category}")
            except Exception as e:
                self.ui.error(f"Error while copying base files for {category}: {str(e)}")
                self.ui.error(traceback.format_exc())
                raise

    def get_component_dependencies(self, components: List[str]) -> Dict[str, List[str]]:
        """
        Get all dependencies for the given components.

        Args:
            components: List of component paths

        Returns:
            Dictionary mapping component names to their dependencies
        """
        self.ui.debug(f"Getting dependencies for components: {components}")
        dependencies = {}

        for component_path in components:
            category, component_name = component_path.split("/")
            metadata = self.template_manager.get_template_metadata(
                category, component_name
            )

            if metadata and "dependencies" in metadata:
                dependencies[component_path] = metadata["dependencies"]
                self.ui.debug(
                    f"Dependencies for {component_path}: {metadata['dependencies']}"
                )

        return dependencies

    def _sort_components(self, components: List[str]) -> List[str]:
        """Sort components by type priority (core -> protocols -> deployments)."""
        # Note: Framework functionality is currently disabled
        type_order = {"core": 0, "protocols": 1, "deployments": 2}

        sorted_components = sorted(
            components, key=lambda x: type_order.get(x.split("/")[0], 999)
        )
        self.ui.debug(f"Sorted components: {sorted_components}")

        return sorted_components

    def _merge_metadata(
        self, base: Dict[str, Any], new: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Merge metadata from multiple components."""
        if not base:
            return new.copy()

        merged = base.copy()

        # Merge specific fields intelligently
        if "provides" in new:
            merged.setdefault("provides", []).extend(new["provides"])

        if "requires" in new:
            merged.setdefault("requires", []).extend(new["requires"])

        if "parameters" in new:
            merged.setdefault("parameters", {}).update(new["parameters"])

        self.ui.debug("Merged metadata")
        return merged
