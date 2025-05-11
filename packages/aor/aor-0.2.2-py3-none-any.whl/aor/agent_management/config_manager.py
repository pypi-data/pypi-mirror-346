"""
Configuration management for agent creation.

This module provides functionality for managing configuration operations
during agent creation.
"""
from typing import Any, Dict, List, Optional, Tuple

from aor.common.agent import Agent
from aor.common.config import Config
from aor.utils.ui import UI

from .types import AgentType
from .validation_utils import sanitize_name



class AgentConfigManager:
    """Manages configuration operations for agent creation."""

    def __init__(self, ui: UI):
        """Initialize the config manager.

        Args:
            ui: UI instance for logging and user interaction
        """
        self.ui = ui

    def load_configuration(self) -> Optional[Config]:
        """Load application configuration.

        Returns:
            Config object if successful, None otherwise
        """
        try:
            self.ui.step("Loading application configuration")
            config = Config()
            self.ui.success("Application configuration loaded successfully")
            return config
        except Exception as e:
            self.ui.error(f"Failed to load configuration: {e}")
            return None

    def sanitize_agent_name(self, name: str) -> str:
        """Sanitize agent name for folder naming.
        
        Replaces spaces, hyphens, and other special characters with underscores.
        Ensures the name is valid for use as a folder name.
        Converts the name to lowercase for normalization.
        Handles Python reserved keywords by appending an underscore.

        Args:
            name: Original agent name

        Returns:
            Sanitized agent name suitable for folder naming
        """
        original_name = name
        
        # Use the common sanitize_name utility
        sanitized_name, was_modified, modification_message = sanitize_name(name, prefix="endpoint")
        
        # Convert to lowercase for normalization (specific to agent names)
        sanitized_name = sanitized_name.lower()
            
        if was_modified:
            message = modification_message or "Name contained invalid characters or format"
            self.ui.info(
                f"Sanitized agent name from '{original_name}' to '{sanitized_name}': {message}"
            )
        return sanitized_name

    def validate_agent_inputs_outputs(self, agent: Agent) -> Tuple[bool, Optional[str]]:
        """Validate agent inputs and outputs for duplicates, reserved names, and minimum requirements.
        
        Args:
            agent: Agent object to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        from .validation_utils import check_for_duplicates, validate_name
        
        # Check for minimum requirements - at least one input and one output
        if not agent.inputs:
            return False, "At least one input field is required"
            
        if not agent.outputs:
            return False, "At least one output field is required"
            
        # Check that the first input is required
        if not agent.inputs[0].get("required", False):
            return False, "The first input field must be required"
        
        # Check for duplicate input names
        input_names = [input_def["name"] for input_def in agent.inputs]
        has_duplicates, error_message = check_for_duplicates(input_names)
        if has_duplicates:
            return False, f"Duplicate input names found: {error_message}"
            
        # Check for duplicate output names
        output_names = [output_def["name"] for output_def in agent.outputs]
        has_duplicates, error_message = check_for_duplicates(output_names)
        if has_duplicates:
            return False, f"Duplicate output names found: {error_message}"
            
        # Check for reserved keywords in input names
        for input_def in agent.inputs:
            name = input_def["name"]
            is_valid, error_message = validate_name(name)
            if not is_valid:
                return False, f"Invalid input name '{name}': {error_message}"
            
            # Ensure only text type is used
            if input_def.get("type") != "text":
                return False, f"Input '{name}' has unsupported type '{input_def.get('type')}'. Only 'text' type is supported."
                
        # Check for reserved keywords in output names
        for output_def in agent.outputs:
            name = output_def["name"]
            is_valid, error_message = validate_name(name)
            if not is_valid:
                return False, f"Invalid output name '{name}': {error_message}"
            
            # Ensure only text type is used
            if output_def.get("type") != "text":
                return False, f"Output '{name}' has unsupported type '{output_def.get('type')}'. Only 'text' type is supported."
        
        return True, None
        
    def create_agent_object(
        self,
        name: str,
        desc: Optional[str],
        type_name: str,
        show_graph: bool,
        path: str,
        protocol: str,
        framework: str,
        deploy: str,
        manual: bool = False,
        input_output_manager=None,
    ) -> Agent:
        """Create and configure an agent object.

        Args:
            name: Agent name
            desc: Agent description
            type_name: Agent type
            show_graph: Whether to show graph
            path: Agent path
            protocol: Communication protocol
            framework: Web framework
            deploy: Deployment target
            manual: Whether this is a manual agent creation
            input_output_manager: Optional InputOutputManager instance

        Returns:
            Configured Agent object
        """
        self.ui.step("Creating agent object")
        agent = Agent(
            name=name,
            desc=desc or f"A {type_name} agent",
            type=type_name,
            show_graph=show_graph,
            path=path,
        )

        # Set additional configuration options
        agent.protocol = protocol
        # Framework functionality is disabled
        # agent.framework = framework
        # Set deployment as a dictionary with type
        agent.deployment = {"type": deploy}
        # Initialize URL at the endpoint level
        agent.url = ""

        # Prompt for inputs and outputs if this is a langgraph agent and not in manual mode
        # In manual mode, we'll add example inputs/outputs later in update_configuration
        if (
            type_name == AgentType.LANGGRAPH.value
            and not manual
            and input_output_manager
        ):
            # Add inputs and outputs through interactive prompts
            input_output_manager.prompt_for_inputs_outputs(agent)

        self.ui.debug(f"Agent object created with path: {path}")

        return agent

    def find_agent_in_config(self, config: Config, name: str) -> Optional[Agent]:
        """Find an agent in the configuration by name.

        Args:
            config: Config object
            name: Name of the agent to find

        Returns:
            Agent object if found, None otherwise
        """
        self.ui.step(f"Looking for agent '{name}' in configuration")
        try:
            agents = config.get("endpoints", [])
            for agent_dict in agents:
                if agent_dict.get("name") == name:
                    self.ui.success(f"Found agent '{name}' in configuration")
                    # Create Agent object from dict using the class method
                    agent = Agent.from_dict(agent_dict)
                    
                    # Only validate if this is a langgraph agent
                    if agent.type == AgentType.LANGGRAPH.value:
                        # Validate inputs and outputs
                        is_valid, error_message = self.validate_agent_inputs_outputs(agent)
                        if not is_valid:
                            self.ui.error(f"Agent inputs/outputs validation error: {error_message}")
                            self.ui.error("Agent validation failed: requirements not met.")
                            return None
                    
                    return agent

            self.ui.warning(f"Agent '{name}' not found in configuration")
            return None
        except Exception as e:
            self.ui.error(f"Error finding agent in configuration: {e}")
            return None

    def update_configuration(
        self, config: Config, agent: Agent, manual: bool = False
    ) -> bool:
        """Update configuration with the new agent.

        Args:
            config: Config object
            agent: Agent object
            manual: Whether this is a manual agent creation

        Returns:
            True if successful, False otherwise
        """
        self.ui.step("Updating configuration")
        try:
            agents = config.get("endpoints", [])

            # Check if agent already exists
            existing_agent_index = None
            for i, existing_agent in enumerate(agents):
                if existing_agent.get("name") == agent.name:
                    existing_agent_index = i
                    break

            # Create agent dict and sort fields in the desired order
            agent_dict = agent.to_dict()
            agent_dict = self._sort_agent_fields(agent_dict)

            # If manual mode, set the flag but don't add examples yet
            if manual:
                # Set the manual_mode flag on the agent object
                agent.manual_mode = True

            # Update or add the agent
            if existing_agent_index is not None:
                agents[existing_agent_index] = agent_dict
                self.ui.info(f"Updated existing agent '{agent.name}' in configuration")
            else:
                agents.append(agent_dict)
                self.ui.info(f"Added new agent '{agent.name}' to configuration")

            config.set("endpoints", agents)

            # Validate inputs and outputs before saving
            is_valid, error_message = self.validate_agent_inputs_outputs(agent)
            if not is_valid:
                self.ui.error(f"Agent inputs/outputs validation error: {error_message}")
                self.ui.error("Agent creation failed: validation requirements not met.")
                return False
            
            # Save the configuration - this might raise an exception if validation fails
            try:
                progress, task_id = self.ui.start_progress("Saving configuration", 1)
                config.save()
                
                # If in manual mode, add commented examples to the YAML file
                if manual and agent.type == AgentType.LANGGRAPH.value:
                    self.ui.info("Adding commented examples to the configuration file")
                    self._add_commented_examples_to_yaml(config.path, agent.name)
                
                self.ui.stop_progress(message="Configuration saved successfully")
                self.ui.success("Agent configuration saved")
                return True
            except Exception as e:
                self.ui.stop_progress(message="Failed to save configuration")
                self.ui.error(f"Failed to save configuration: {e}")
                
                # Even though saving failed, the agent files were created
                self.ui.warning("Agent files were created but configuration could not be saved.")
                self.ui.warning("You may need to manually fix the configuration file.")
                return False
                
        except Exception as e:
            self.ui.error(f"Failed to update configuration: {e}")
            return False

    def _sort_agent_fields(
        self, agent_dict: Dict[str, Any], field_order: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Sort agent fields according to the specified order.

        Args:
            agent_dict: Dictionary containing agent fields
            field_order: List of field names in the desired order. Fields not in the list will be placed at the end.
                        If None, a default order will be used.

        Returns:
            Sorted agent dictionary
        """
        self.ui.debug("Sorting agent fields")

        # Default field order if not specified
        if field_order is None:
            field_order = [
                "name",
                "internal_id",
                "desc",
                "path",
                "type",
                "protocol",
                "deployment",
                "inputs",
                "outputs",
                # Framework functionality is disabled
                # "framework",
                "show_graph",
            ]

        # Create a new dictionary with fields in the specified order
        sorted_dict = {}

        # First add fields in the specified order
        for field in field_order:
            if field in agent_dict:
                sorted_dict[field] = agent_dict[field]

        # Then add any remaining fields not in the order list
        for field, value in agent_dict.items():
            if field not in sorted_dict:
                sorted_dict[field] = value

        self.ui.debug("Agent fields sorted successfully")
        return sorted_dict

    def _add_commented_examples_to_yaml(
        self, config_path: str, agent_name: str
    ) -> None:
        """Add commented examples for inputs and outputs to the YAML file.

        Args:
            config_path: Path to the configuration file
            agent_name: Name of the agent to add examples for
        """
        self.ui.step(f"Adding commented examples to {config_path}")

        try:
            # Read the file content
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Find the agent in the file
            lines = content.split("\n")
            agent_line_idx = -1
            indent = ""

            # Find the agent with the specified name
            for i, line in enumerate(lines):
                if (
                    line.strip().startswith("-")
                    and "name:" in line
                    and agent_name in line
                ):
                    agent_line_idx = i
                    indent = " " * (line.index("-"))  # Get the indentation level
                    break

            if agent_line_idx == -1:
                self.ui.warning(
                    f"Could not find agent '{agent_name}' in the configuration file"
                )
                return

            # Find where to insert the examples (after the protocol field)
            insert_idx = -1
            for i in range(agent_line_idx, len(lines)):
                if "protocol:" in lines[i]:
                    insert_idx = i + 1
                    break

            if insert_idx == -1:
                self.ui.warning("Could not find where to insert examples")
                return

            # Prepare the examples
            examples = self._generate_example_comments(indent, agent_name)

            # Insert the examples (one by one to maintain proper line structure)
            for i, example in enumerate(examples):
                lines.insert(insert_idx + i, example)

            # Write the file back
            with open(config_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))

            self.ui.success("Added commented examples to the configuration file")
        except Exception as e:
            self.ui.error(f"Error adding commented examples: {e}")

    def _generate_example_comments(self, indent: str, agent_name: str) -> List[str]:
        """Generate example comments for the YAML file.

        Args:
            indent: Indentation string
            agent_name: Name of the agent

        Returns:
            List of example comment lines
        """
        examples = []
        # Add instructions at the top for better visibility
        examples.append(f"{indent}    # INSTRUCTIONS:")
        examples.append(
            f"{indent}    # Uncomment and edit the examples below to define your inputs and outputs"
        )
        examples.append(
            f"{indent}    # Remove the EXAMPLE_ prefix from names you want to keep"
        )
        examples.append(f"{indent}    # Then run: aor add {agent_name} --continue")
        examples.append(f"{indent}    # ===========================================")
        examples.append(f"{indent}    #")
        examples.append(f"{indent}    # inputs:")
        examples.append(f"{indent}    # -   name: EXAMPLE_text_input")
        examples.append(f"{indent}    #     type: text")
        examples.append(f"{indent}    #     required: true")
        examples.append(
            f"{indent}    #     desc: Example text input - first input must be required"
        )
        examples.append(f"{indent}    # -   name: EXAMPLE_second_input")
        examples.append(f"{indent}    #     type: text")
        examples.append(f"{indent}    #     required: false")
        examples.append(
            f"{indent}    #     desc: Another example text input - additional inputs can be optional"
        )
        examples.append(f"{indent}    # outputs:")
        examples.append(f"{indent}    # -   name: EXAMPLE_text_output")
        examples.append(f"{indent}    #     type: text")
        examples.append(
            f"{indent}    #     desc: Example text output - replace with your own output name and description"
        )
        examples.append(f"{indent}    # -   name: EXAMPLE_second_output")
        examples.append(f"{indent}    #     type: text")
        examples.append(
            f"{indent}    #     desc: Another example text output - you must define at least one output"
        )
        examples.append(f"{indent}    # ")

        return examples
