"""
Path management for agent creation.

This module provides functionality for managing file and directory operations
during agent creation.
"""

import os
import shutil
from pathlib import Path

from aor.utils.ui import UI


class AgentPathManager:
    """Manages file and directory operations for agent creation."""

    def __init__(self, ui: UI):
        """Initialize the path manager.

        Args:
            ui: UI instance for logging and user interaction
        """
        self.ui = ui

    def prepare_agent_path(self, path: str) -> bool:
        """Prepare the agent path by removing existing files/directories and creating necessary directories.

        Args:
            path: The path to prepare

        Returns:
            True if preparation was successful, False otherwise
        """
        agent_path = Path(path)
        self.ui.debug(f"Checking if agent path exists: {agent_path}")

        # Remove existing path if it exists
        if agent_path.exists():
            self.ui.info(f"Path {agent_path} exists")
            if not self._remove_existing_path(agent_path):
                return False

        # Create directory structure
        if not self._create_directory_structure(path):
            return False

        return True

    def _remove_existing_path(self, path: Path) -> bool:
        """Remove an existing file or directory.

        Args:
            path: Path to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            if path.is_dir():
                self.ui.warning(f"Directory '{path}' already exists. Removing it...")
                shutil.rmtree(path)
                self.ui.file_operation("Removed directory", str(path))
            else:
                self.ui.warning(f"File '{path}' already exists. Removing it...")
                path.unlink()
                self.ui.file_operation("Removed file", str(path))
            return True
        except Exception as e:
            self.ui.error(f"Error removing existing path: {str(e)}")
            return False

    def _create_directory_structure(self, path: str) -> bool:
        """Create the directory structure for an agent.

        Args:
            path: Path to create

        Returns:
            True if successful, False otherwise
        """
        try:
            self.ui.step("Preparing directory structure for agent")
            parent_dir = os.path.dirname(path)
            if parent_dir:  # Only create parent dir if it's not empty
                self.ui.debug(f"Creating parent directory: {parent_dir}")
                os.makedirs(parent_dir, exist_ok=True)
                self.ui.file_operation("Created directory", parent_dir)
            self.ui.success("Directory structure prepared")
            return True
        except Exception as e:
            self.ui.error(f"Error creating directory structure: {str(e)}")
            return False
