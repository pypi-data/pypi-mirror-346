"""
Template discovery and management for AI-on-Rails.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from ruamel.yaml import YAML
import traceback

from aor.templates.utils.template_renderer import TemplateRenderer
from aor.templates.utils.dependency_manager import DependencyManager
from aor.templates.utils.file_generator import FileGenerator
from aor.templates.utils.validators.metadata import MetadataValidator
from aor.utils.ui import UI

class TemplateManager:
    """
    Manages template discovery, metadata reading, and template application.
    """

    def __init__(self, templates_dir: Path, ui: UI = None):
        """
        Initialize the template manager.

        Args:
            templates_dir: Root directory containing all templates
            ui: UI instance for output and logging
        """
        self.templates_dir = templates_dir
        self.ui = ui or UI()  # Use provided UI or create a new one
        self.yaml = YAML()
        self.yaml.preserve_quotes = True
        self.yaml.indent = 2

        self.dependency_manager = DependencyManager(ui=self.ui)
        self.file_generator = FileGenerator(ui=self.ui)
        self.metadata_validator = MetadataValidator()

        self.ui.debug(
            f"Initialized TemplateManager with templates_dir: {templates_dir}"
        )

    def list_templates(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        List all available templates grouped by category.

        Returns:
            Dictionary of templates grouped by categories
        """
        self.ui.debug("Listing templates...")
        templates = {}

        # Scan all category directories
        for category_dir in self.templates_dir.iterdir():
            if category_dir.is_dir() and not category_dir.name.startswith("__"):
                category = category_dir.name
                templates[category] = []
                self.ui.debug(f"Scanning category: {category}")

                # Find templates with metadata.yaml
                for template_dir in category_dir.iterdir():
                    if (
                        template_dir.is_dir()
                        and (template_dir / "metadata.yaml").exists()
                    ):
                        metadata = self.get_template_metadata(
                            category, template_dir.name
                        )
                        if metadata:
                            template_info = {
                                "name": template_dir.name,
                                "displayName": metadata.get(
                                    "displayName", template_dir.name
                                ),
                                "description": metadata.get("description", ""),
                                "type": metadata.get("type", category),
                                "version": metadata.get("version", "1.0.0"),
                                "componentType": metadata.get(
                                    "componentType", category
                                ),
                            }
                            templates[category].append(template_info)
                            self.ui.debug(
                                f"Found template: {category}/{template_dir.name}"
                            )

        self.ui.debug(
            f"Listed {sum(len(t) for t in templates.values())} templates in {len(templates)} categories"
        )
        return templates

    def get_template_path(self, category: str, template_name: str) -> Path:
        """
        Get the path to a template directory.

        Args:
            category: Template category
            template_name: Template name

        Returns:
            Path to template directory
        """
        path = self.templates_dir / category / template_name
        self.ui.debug(f"Template path for {category}/{template_name}: {path}")
        return path

    def get_template_metadata(
        self, category: str, template_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get metadata for a specific template.

        Args:
            category: Template category
            template_name: Template name

        Returns:
            Template metadata or None if not found
        """
        self.ui.debug(f"Getting metadata for {category}/{template_name}")

        metadata_path = self.templates_dir / category / template_name / "metadata.yaml"
        self.ui.debug(f"Metadata path: {metadata_path}")

        if not metadata_path.exists():
            self.ui.warning(f"Metadata file not found: {metadata_path}")
            return None

        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = self.yaml.load(f)
            self.ui.debug(f"Loaded metadata for {category}/{template_name}")
            self.ui.debug(f"Metadata content: {metadata}")
        except Exception as e:
            self.ui.error(f"Error loading metadata from {metadata_path}: {str(e)}")
            return None

        # Validate metadata
        if not self.metadata_validator.validate(metadata):
            self.ui.warning(f"Invalid metadata for {category}/{template_name}")
            self.ui.warning(f"Metadata validation failed for: {metadata}")
            return None

        return metadata

    def apply_template(
        self,
        category: str,
        template_name: str,
        agent_name: str,
        agent_desc: Optional[str] = None,
        **kwargs,
    ) -> bool:
        """
        Apply a template to create files for an agent.

        Args:
            category: Template category
            template_name: Template name
            agent_name: Name of the agent to create
            agent_desc: Description of the agent
            **kwargs: Additional parameters for the template

        Returns:
            True if successful, False otherwise
        """
        self.ui.debug(
            f"Applying template {category}/{template_name} for agent {agent_name}"
        )
        self.ui.debug(f"Description: {agent_desc}")
        self.ui.debug(f"Additional parameters: {kwargs}")

        template_dir = self.templates_dir / category / template_name
        self.ui.debug(f"Template directory: {template_dir}")

        # Check if template exists
        if not template_dir.exists() or not template_dir.is_dir():
            self.ui.error(
                f"Template {category}/{template_name} not found at {template_dir}"
            )
            self.ui.error(f"Template {category}/{template_name} not found.")
            return False

        # Get template metadata
        metadata = self.get_template_metadata(category, template_name)
        if not metadata:
            self.ui.error(
                f"Invalid template: metadata.yaml not found for {category}/{template_name}."
            )
            self.ui.error(
                f"Invalid template: metadata.yaml not found for {category}/{template_name}."
            )
            return False

        # Initialize renderer with template directory
        try:
            renderer = TemplateRenderer(template_dir, self.ui)
            self.ui.debug(f"Initialized renderer for {template_dir}")
        except Exception as e:
            self.ui.error(f"Failed to initialize renderer: {str(e)}")
            return False

        # Prepare parameters
        params = {
            "agent_name": agent_name,
            "agent_desc": agent_desc
            or metadata.get("parameters", {})
            .get("agent_desc", {})
            .get("default", "An AI agent"),
        }

        # Add additional parameters
        params.update(kwargs)
        self.ui.debug(f"Final parameters: {params}")

        # Validate parameters against metadata
        if not self._validate_parameters(metadata, params):
            self.ui.error("Parameter validation failed")
            return False

        # Generate files
        try:
            success = self.file_generator.generate_files(
                template_dir, metadata, params, renderer
            )
            self.ui.debug(f"File generation result: {success}")
        except Exception as e:
            self.ui.error(f"Error generating files: {str(e)}")
            return False

        # Handle dependencies if successful
        if success and "dependencies" in metadata and metadata["dependencies"]:
            self.ui.debug(f"Handling dependencies: {metadata['dependencies']}")
            self._handle_dependencies(metadata["dependencies"])

        return success

    def _validate_parameters(
        self, metadata: Dict[str, Any], params: Dict[str, Any]
    ) -> bool:
        """Validate parameters against template metadata."""
        self.ui.debug(f"Validating parameters: {params}")
        self.ui.debug(f"Against metadata: {metadata}")

        required_params = {}
        for param_name, param_info in metadata.get("parameters", {}).items():
            if param_info.get("required", False):
                required_params[param_name] = param_info

        self.ui.debug(f"Required parameters: {required_params}")

        # Check if all required parameters are provided
        for param_name, param_info in required_params.items():
            if param_name not in params:
                self.ui.error(f"Missing required parameter: {param_name}")
                self.ui.error(f"Missing required parameter: {param_name}")
                self.ui.info(
                    f"Description: {param_info.get('description', 'No description')}"
                )
                return False

        self.ui.debug("Parameter validation successful")
        return True

    def _handle_dependencies(self, dependencies: List[str]) -> None:
        """Handle template dependencies."""
        self.ui.debug(f"Handling dependencies: {dependencies}")
        dependency_set = set(dependencies)

        # Update requirements.txt
        try:
            new_deps = self.dependency_manager.update_requirements(dependency_set)
            self.ui.debug(f"New dependencies to add: {new_deps}")

            if new_deps:
                self.ui.info(
                    f"Added {len(new_deps)} new dependencies to requirements.txt"
                )

                # Install new dependencies
                self.ui.info("Installing dependencies...")
                progress, task_id = self.ui.start_progress(
                    "Installing dependencies", total=len(new_deps)
                )

                results = self.dependency_manager.install_dependencies(new_deps)

                # Stop the progress indicator
                self.ui.stop_progress("Dependencies installation completed")

                if results["installed"]:
                    self.ui.debug(f"Successfully installed: {results['installed']}")
                    self.ui.success(
                        f"Installed dependencies: {', '.join(results['installed'])}"
                    )

                if results["failed"]:
                    self.ui.error(f"Failed to install: {results['failed']}")
                    self.ui.error(
                        f"Failed to install: {', '.join([item['dependency'] for item in results['failed']])}"
                    )
        except Exception as e:
            self.ui.error(f"Error handling dependencies: {str(e)}")
            self.ui.error(f"Error handling dependencies: {str(e)}")
