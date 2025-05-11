"""
Input/output management for agent creation.

This module provides functionality for managing input and output definitions
during agent creation.
"""

from typing import List, Optional, Tuple, Set

from aor.common.agent import Agent
from aor.utils.ui import UI

from .types import InputDefinition, InputType, OutputDefinition, OutputType
from .validation_utils import validate_name, check_for_duplicates


class InputOutputManager:
    """Manages input and output definitions for agents."""

    def __init__(self, ui: UI):
        """Initialize the input/output manager.

        Args:
            ui: UI instance for logging and user interaction
        """
        self.ui = ui

    def _validate_name(self, name: str) -> Tuple[bool, Optional[str]]:
        """Validate an input or output name.

        Names must:
        - Start with a letter
        - Contain only letters, numbers, and underscores
        - Be at least 3 characters long
        - Not exceed 50 characters
        - Not be a Python reserved keyword or common built-in name

        Args:
            name: The name to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        return validate_name(name)

    def prompt_for_inputs_outputs(self, agent: Agent) -> None:
        """Interactively prompt the user for inputs and outputs.

        Args:
            agent: Agent object to update
        """
        self.ui.section("Agent Inputs and Outputs")
        self.ui.info("Define the inputs and outputs for your agent.")
        self.ui.info("These will be used to generate the input and output models.")
        self.ui.info("You must define at least one input and one output field.")
        self.ui.info("Only text type is currently supported.")

        # Initialize inputs and outputs lists
        inputs = []
        outputs = []

        # Prompt for inputs
        self._prompt_for_inputs(inputs)

        # Prompt for outputs
        self._prompt_for_outputs(outputs)

        # Validate that at least one input and one output is provided
        if not inputs:
            self.ui.error("At least one input field is required.")
            # Prompt again for inputs
            self._prompt_for_inputs(inputs)
            
        if not outputs:
            self.ui.error("At least one output field is required.")
            # Prompt again for outputs
            self._prompt_for_outputs(outputs)
            
        # Final validation check
        if not inputs or not outputs:
            self.ui.error("Agent creation failed: At least one input and one output field is required.")
            raise ValueError("Agent creation requires at least one input and one output field.")
            
        # Set the inputs and outputs on the agent
        agent.inputs = inputs
        agent.outputs = outputs

    def _prompt_for_inputs(self, inputs: List[InputDefinition]) -> None:
        """Prompt for input definitions.

        Args:
            inputs: List to append input definitions to
        """
        self.ui.section("Inputs")
        self.ui.info("Define the inputs your agent will accept.")
        self.ui.info("Available types: text")

        # Keep track of input names to check for duplicates
        input_names: Set[str] = set()

        while True:
            # Get input name
            if len(inputs) > 0:
                name = self.ui.prompt(
                    "Input name (or leave empty to finish inputs)"
                )
            else:
                name = self.ui.prompt("First input name (will be used as the primary input field)")
            if not name and len(inputs) > 0:
                break
            elif not name:
                self.ui.error("You must provide at least one input field name.")
                continue

            # Validate input name
            is_valid, error_message = self._validate_name(name)

            # Check for duplicate names (case-insensitive)
            if is_valid and name.lower() in input_names:
                is_valid = False
                error_message = (
                    f"Input name '{name}' is already used. Names must be unique."
                )

            while not is_valid:
                self.ui.warning(f"Invalid input name: {error_message}")
                name = self.ui.prompt("Input name (must be valid identifier)")
                if not name:
                    break
                is_valid, error_message = self._validate_name(name)
                # Check for duplicate names again
                if is_valid and name.lower() in input_names:
                    is_valid = False
                    error_message = (
                        f"Input name '{name}' is already used. Names must be unique."
                    )

            if not name:  # User decided to skip after validation errors
                continue

            # Add name to the set of used names
            input_names.add(name.lower())

            # Only text type is supported
            input_type = "text"
            self.ui.info("Using input type: text")

            # First input must be required and is used as primary input
            if len(inputs) == 0:
                required = True
                self.ui.info("First input is required by default")
                self.ui.info("First input will be used as the primary input field for your agent")
            else:
                required = self.ui.confirm("Is this input required?")

            # Get description (required)
            desc = self.ui.prompt("Input description (visible to the user)")
            
            # Ensure description is not empty
            while not desc:
                self.ui.warning("Input description is required")
                desc = self.ui.prompt("Input description (visible to the user)")

            # Create input definition
            input_def: InputDefinition = {
                "name": name,
                "type": input_type,
                "required": required,
                "desc": desc,
            }

            inputs.append(input_def)
            self.ui.info(f"Added input: {name} ({input_type})")

    def _prompt_for_outputs(self, outputs: List[OutputDefinition]) -> None:
        """Prompt for output definitions.

        Args:
            outputs: List to append output definitions to
        """
        self.ui.section("Outputs")
        self.ui.info("Define the outputs your agent will produce.")
        self.ui.info("Available types: text")

        # Keep track of output names to check for duplicates
        output_names: Set[str] = set()

        while True:
            # Get output name
            if len(outputs) > 0:
                name = self.ui.prompt("Output name (or leave empty to finish outputs)")
            else:
                name = self.ui.prompt("Output name")
            if not name and len(outputs) > 0:
                break
            elif not name:
                self.ui.error("You must provide at least one output field name.")
                continue

            # Validate output name
            is_valid, error_message = self._validate_name(name)

            # Check for duplicate names (case-insensitive)
            if is_valid and name.lower() in output_names:
                is_valid = False
                error_message = (
                    f"Output name '{name}' is already used. Names must be unique."
                )

            while not is_valid:
                self.ui.warning(f"Invalid output name: {error_message}")
                name = self.ui.prompt("Output name (must be valid identifier)")
                if not name:
                    break
                is_valid, error_message = self._validate_name(name)
                # Check for duplicate names again
                if is_valid and name.lower() in output_names:
                    is_valid = False
                    error_message = (
                        f"Output name '{name}' is already used. Names must be unique."
                    )

            if not name:  # User decided to skip after validation errors
                continue

            # Add name to the set of used names
            output_names.add(name.lower())

            # Only text type is supported
            output_type = "text"
            self.ui.info("Using output type: text")

            # Get description (required)
            desc = self.ui.prompt("Output description")
            
            # Ensure description is not empty
            while not desc:
                self.ui.warning("Output description is required")
                desc = self.ui.prompt("Output description")

            # Create output definition
            output_def: OutputDefinition = {
                "name": name,
                "type": output_type,
                "desc": desc,
            }

            outputs.append(output_def)
            self.ui.info(f"Added output: {name} ({output_type})")

    def _get_type_selection(self, type_options: List[str], type_label: str) -> str:
        """Get type selection from user input.

        Args:
            type_options: List of available type options
            type_label: Label for the type (input or output)

        Returns:
            Selected type
        """
        # Only text type is supported, so we always return "text"
        return "text"

    def _get_file_formats(self) -> List[str]:
        """Get file formats from user input.

        Note: This method is currently unused as file type is disabled.

        Returns:
            List of file formats
        """
        # This functionality is disabled as file type is not supported
        return []

    def _get_enum_values(self) -> List[str]:
        """Get enum values from user input.
        
        Note: This method is currently unused as enum type is disabled.

        Returns:
            List of enum values
        """
        # This functionality is disabled as enum type is not supported
        return []
