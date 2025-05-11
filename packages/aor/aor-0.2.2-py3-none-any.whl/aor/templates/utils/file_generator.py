"""
File generation utilities for template system.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from aor.templates.utils.template_renderer import TemplateRenderer
import traceback


class FileGenerator:
    """
    Handles file generation from templates.
    """

    def __init__(self, ui):
        """
        Initialize the file generator.

        Args:
            ui: UI instance for displaying messages
        """
        self.ui = ui
        self.created_files = []

    def generate_files(
        self,
        template_dir: Path,
        metadata: Dict[str, Any],
        params: Dict[str, Any],
        renderer: TemplateRenderer,
        output_dir: Optional[Path] = None,
    ) -> bool:
        """
        Generate files based on template metadata.

        Args:
            template_dir: Directory containing template files
            metadata: Template metadata
            params: Parameters for template rendering
            renderer: Template renderer instance
            output_dir: Optional output directory (defaults to current directory)

        Returns:
            True if successful, False otherwise
        """
        output_dir = output_dir or Path.cwd()
        self.ui.debug(f"Generating files from {template_dir} to {output_dir}")
        self.ui.debug(f"Metadata: {metadata}")
        self.ui.debug(f"Parameters: {params}")

        # Clear the list of created files
        self.created_files = []

        # Process each file in metadata
        if "files" not in metadata:
            self.ui.warning(f"No files defined in metadata for {template_dir}")
            return False

        # Group files by destination for priority handling
        files_by_destination = {}

        for file_info in metadata["files"]:
            self.ui.debug(f"Processing file info: {file_info}")

            # Check condition if present
            if "condition" in file_info:
                if not self._evaluate_condition(file_info["condition"], params):
                    self.ui.debug(f"Skipping file due to condition: {file_info}")
                    continue

            # Group by destination
            dest_path_str = file_info["destination"]
            if dest_path_str not in files_by_destination:
                files_by_destination[dest_path_str] = []
            files_by_destination[dest_path_str].append(file_info)

        self.ui.debug(f"Files grouped by destination: {files_by_destination}")

        # Process files, handling priority for same destinations
        for dest_path_str, file_list in files_by_destination.items():
            # If multiple files for same destination, choose highest priority
            if len(file_list) > 1:
                file_list.sort(key=lambda x: x.get("priority", 0), reverse=True)
                file_info = file_list[0]  # Highest priority
                self.ui.debug(f"Multiple files for {dest_path_str}, chose: {file_info}")
            else:
                file_info = file_list[0]

            if not self._process_file(
                template_dir, file_info, params, renderer, output_dir
            ):
                self.ui.error(f"Failed to process file: {file_info}")
                return False

        self.ui.debug("Successfully generated all files")
        return True

    def _evaluate_condition(self, condition: str, params: Dict[str, Any]) -> bool:
        """Evaluate a condition string against parameters."""
        self.ui.debug(f"Evaluating condition: {condition} with params: {params}")

        try:
            # Simple and safe evaluation of conditions
            # Replace parameter names with their values
            condition_eval = condition
            for key, value in params.items():
                if key in condition:
                    value_str = f"'{value}'" if isinstance(value, str) else str(value)
                    condition_eval = condition_eval.replace(key, value_str)
            
            # Replace JavaScript-style boolean literals with Python equivalents
            condition_eval = condition_eval.replace(" true", " True").replace(" false", " False")
            condition_eval = condition_eval.replace("(true", "(True").replace("(false", "(False")
            condition_eval = condition_eval.replace("==true", "==True").replace("==false", "==False")

            # Safely evaluate boolean expressions
            # This is a simplified approach - in production you'd want a proper expression evaluator
            result = eval(condition_eval, {"__builtins__": {}}, {})
            self.ui.debug(f"Condition '{condition}' evaluated to: {result}")
            return result
        except Exception as e:
            self.ui.error(f"Error evaluating condition '{condition}': {e}")
            self.ui.error(traceback.format_exc())
            return False

    def _process_file(
        self,
        template_dir: Path,
        file_info: Dict[str, Any],
        params: Dict[str, Any],
        renderer: TemplateRenderer,
        output_dir: Path,
    ) -> bool:
        """Process a single file from template."""
        source_path = file_info["source"]

        # Check if source file exists
        source_file = template_dir / source_path
        if not source_file.exists():
            source_file = template_dir / f"{source_path}.j2"
            if not source_file.exists():
                return True  # Continue with other files

        # Remove .j2 from destination if present
        dest_path_str = file_info["destination"]
        if dest_path_str.endswith(".j2"):
            dest_path_str = dest_path_str[:-3]

        # Render destination path
        rendered_dest_path_str = renderer.render_string(dest_path_str, params)

        # Special handling for agent templates to prevent duplication
        # If the destination path starts with "src/{agent_name}/" and the output_dir is already "src/{something}"
        # This specifically targets the pattern that causes duplication in agent creation

        # Normalize paths for comparison
        output_dir_str = str(output_dir).replace("\\", "/")
        if output_dir_str.endswith("/"):
            output_dir_str = output_dir_str[:-1]

        # Check if output_dir follows the pattern "src/{something}"
        if "/" in output_dir_str:
            parts = output_dir_str.split("/")
            if len(parts) >= 2 and parts[0] == "src":
                # Check if destination starts with "src/" followed by the agent name from params
                agent_name = params.get("agent_name", "")
                if agent_name and rendered_dest_path_str.startswith(f"src/{agent_name}/"):
                    # Remove the duplicated "src/{agent_name}/" prefix
                    rendered_dest_path_str = rendered_dest_path_str[
                        len(f"src/{agent_name}/") :
                    ]
                    self.ui.debug(
                        f"Removed duplicated agent path prefix. New path: {rendered_dest_path_str}"
                    )

        dest_path = output_dir / rendered_dest_path_str

        # Create destination directory if needed
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Process file based on type
        return self._process_text_file(
            source_file, dest_path, params, renderer, file_info
        )

    def _process_text_file(
        self,
        source_file: Path,
        dest_path: Path,
        params: Dict[str, Any],
        renderer: TemplateRenderer,
        file_info: Dict[str, Any],
    ) -> bool:
        """Process a text file with template rendering."""
        self.ui.debug(f"Processing text file: {source_file} -> {dest_path}")

        try:
            # Check if file already exists
            if dest_path.exists() and not file_info.get("overwrite", False):
                self.ui.debug(f"Skipping existing file: {dest_path}")
                return True

            # Render content - use forward slashes and relative path
            try:
                # Get relative path from template directory
                relative_path = source_file.relative_to(renderer.template_dir)
                # Convert to forward slashes for jinja2
                relative_path_str = str(relative_path).replace("\\", "/")
                self.ui.debug(f"Rendering template: {relative_path_str}")
                content = renderer.render_template(relative_path_str, params)
                self.ui.debug(
                    f"Successfully rendered content, length: {len(content)} chars"
                )
            except Exception as e:
                self.ui.error(f"Failed to render template {relative_path}: {str(e)}")
                self.ui.error(traceback.format_exc())
                # Try reading the file directly if rendering fails
                self.ui.debug(f"Fallback: trying to read file directly")
                try:
                    with open(source_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    # Still try to process as template if possible
                    content = renderer.render_string(content, params)
                except Exception as e2:
                    self.ui.error(f"Failed to read file directly: {str(e2)}")
                    return False

            # Write rendered content
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(content)

            self.ui.debug(f"Successfully wrote file: {dest_path}")
            # Add to the list of created files
            self.created_files.append(str(dest_path))
            
            # Don't report individual files here as they'll be grouped later
            # This prevents duplicate file creation messages in the output
            return True

        except Exception as e:
            self.ui.error(f"Error processing file {source_file}: {str(e)}")
            self.ui.error(traceback.format_exc())
            return False
