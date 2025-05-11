"""
Code generation for agent creation.

This module provides functionality for generating code during agent creation.
"""

import os
import traceback
from pathlib import Path
from typing import Dict, List, Optional

from aor import templates
from aor.common.agent import Agent
from aor.utils.ui import UI

from .dependency_manager import AgentDependencyManager
from .types import AgentType, DeploymentType, FrameworkType, ProtocolType


class AgentCodeGenerator:
    """Generates code for agents."""

    def __init__(self, ui: UI):
        """Initialize the code generator.

        Args:
            ui: UI instance for logging and user interaction
        """
        self.ui = ui
        self.dependency_manager = AgentDependencyManager(ui)

    def generate_agent_code(
        self,
        agent: Agent,
        name: str,
        desc: Optional[str],
        protocol: str,
        framework: str,
        deploy: str,
    ) -> None:
        """Generate code for the agent based on its type and options.

        Args:
            agent: Agent object
            name: Agent name
            desc: Agent description
            protocol: Communication protocol
            framework: Web framework
            deploy: Deployment target
        """
        try:
            if not self._apply_components(
                agent, name, desc, protocol, framework, deploy
            ):
                self.ui.warning(
                    "Component application failed, using default implementation"
                )
                self._create_default_implementation(agent)
        except Exception as e:
            error_msg = f"Failed to generate agent code: {e}"
            self.ui.error(error_msg)
            self.ui.warning("Using default implementation instead")
            self._create_default_implementation(agent)

    def _apply_components(
        self,
        agent: Agent,
        name: str,
        desc: Optional[str],
        protocol: str,
        framework: str,
        deploy: str,
    ) -> bool:
        """Apply components to create agent implementation.

        Args:
            agent: The agent object
            name: The agent name
            desc: The agent description
            protocol: The communication protocol
            framework: The web framework
            deploy: The deployment target

        Returns:
            bool: True if components were applied successfully, False otherwise
        """
        try:
            # Get components to combine
            components = self._get_components_to_combine(
                agent, protocol, framework, deploy
            )

            if len(components) > 1:
                self.ui.step(f"Combining {len(components)} components for the agent")
                self.ui.display_table(
                    "Components", ["Component Type"], [[c] for c in components]
                )

            # Determine output directory
            agent_path = Path(agent.path)
            if agent_path.suffix == ".py":
                # If path is a file, use its parent directory
                output_dir = str(agent_path.parent)
            else:
                # If path is already a directory, use it directly
                output_dir = str(agent_path)
            self.ui.debug(f"Output directory: {output_dir}")

            # Validate component compatibility before combining
            self.ui.step("Validating component compatibility")

            # Combine components

            # Start a progress indicator for code generation
            progress, task_id = self.ui.start_progress(
                "Generating agent code", len(components)
            )

            success = templates.combine_components(
                components=components,
                agent_name=name,
                output_dir=output_dir,
                agent_desc=desc,
                protocol=protocol,
                framework=framework,
                deployment=deploy,
                inputs=agent.inputs,
                outputs=agent.outputs,
                internal_id=agent.internal_id,
                enable_async=True,  # Add the enable_async parameter with default value True
            )

            # Update progress after component combination
            self.ui.update_progress(len(components), "Components combined")

            self.ui.stop_progress(message="Code generation completed")
            self.ui.info(
                f"Component application result: {'success' if success else 'failed'}"
            )

            if success:
                self.ui.success("Agent code generated successfully")
                self._show_post_creation_instructions(name, protocol, framework, deploy)
                return True
            else:
                self.ui.error(
                    "Failed to apply components - see previous logs for details"
                )
                return False

        except Exception as e:
            self.ui.error(f"Error applying components: {str(e)}")
            self.ui.debug(traceback.format_exc())
            return False

    def _get_components_to_combine(
        self, agent: Agent, protocol: str, framework: str, deploy: str
    ) -> List[str]:
        """Get the list of components to combine based on agent type and options.

        Args:
            agent: Agent object
            protocol: Communication protocol
            framework: Web framework
            deploy: Deployment target

        Returns:
            List of component paths to combine
        """
        # Create list of components to combine based on the directory structure
        type_template_map: Dict[str, str] = {
            AgentType.LANGCHAIN.value: "core/langchain",
            AgentType.LANGGRAPH.value: "core/langgraph",
            AgentType.PYDANTIC.value: "core/pydantic",
            ProtocolType.A2A.value: "protocols/a2a",
        }

        core_component = type_template_map.get(agent.type, "core/langgraph")
        components: List[str] = [core_component]

        # Add additional components based on options
        if protocol != ProtocolType.RAW.value:
            components.append(f"protocols/{protocol}")
        # Framework functionality is disabled
        # if framework is not None:
        #     components.append(f"frameworks/{framework}")
        if deploy is not None:
            components.append(f"deployments/{deploy}")

        self.ui.info(f"Components to combine: {components}")
        return components

    def _show_post_creation_instructions(
        self, name: str, protocol: str, framework: str, deploy: str
    ) -> None:
        """Show instructions after successful agent creation.

        Args:
            name: The agent name
            protocol: The communication protocol
            framework: The web framework
            deploy: The deployment target
        """
        if protocol == ProtocolType.RAW.value and framework is None and deploy is None:
            return

        self.ui.section("Next Steps")
        self.ui.step(f"Showing post-creation instructions for {name}")

        # Provide additional instructions based on options
        # Framework functionality is disabled
        # if (
        #     protocol == ProtocolType.A2A.value
        #     and framework == FrameworkType.FASTAPI.value
        # ):
        #     self.ui.info("Providing FastAPI server startup instructions")
        #     self.ui.info("To run your A2A agent with FastAPI:")
        #     self.ui.command(
        #         f"uvicorn src.{name}.server:app --reload", "Start the server"
        #     )
        if deploy == DeploymentType.AWS_LAMBDA.value:
            self.ui.info("Providing AWS Lambda deployment instructions")
            self.ui.info("To deploy to AWS Lambda:")
            self.ui.command(
                f"aor deploy --endpoint {name}", "Deploy agent to AWS Lambda"
            )

    def _create_default_implementation(self, agent: Agent) -> None:
        """Create a default implementation for the agent.

        Args:
            agent: The agent object
        """
        self.ui.step(f"Creating default implementation for agent: {agent.name}")

        # Add dependencies
        self.dependency_manager.add_dependencies(agent)

        # Create agent implementation
        agent_path = Path(agent.path)

        # Write the default implementation
        try:
            progress, task_id = self.ui.start_progress("Creating agent files", 1)

            self._write_default_implementation(agent_path, agent)
            self.ui.update_progress(1, "Agent file created")

            self.ui.stop_progress(message="Agent files created successfully")
            self.ui.success(f"Created default implementation at {agent.path}")
            self.ui.file_operation("Created file", str(agent_path))

        except Exception as e:
            self.ui.error(f"Error writing files: {str(e)}")

    def _write_default_implementation(self, main_file: Path, agent: Agent) -> None:
        """Write the default implementation to the main file or directory.

        Args:
            main_file: The main file path or directory path
            agent: The agent object
        """
        # For langgraph agents with folder-based path, create multiple files
        if agent.type == AgentType.LANGGRAPH.value and main_file.suffix != ".py":
            self.ui.step(f"Creating folder-based langgraph agent in: {main_file}")

            # Create directory if needed
            if not main_file.exists():
                os.makedirs(main_file, exist_ok=True)
                self.ui.file_operation("Created directory", str(main_file))

            try:
                # Create __init__.py
                init_file = main_file / "__init__.py"
                with open(init_file, "w", encoding="utf-8") as f:
                    f.write(f"# {agent.name} agent package\n")
                self.ui.file_operation("Created file", str(init_file))

                # Create agent.py
                agent_file = main_file / "agent.py"
                with open(agent_file, "w", encoding="utf-8") as f:
                    # Write header comments
                    f.write(f"# {agent.name} agent implementation\n")
                    f.write(f"# {agent.desc}\n")
                    f.write(f"# {agent.type} agent\n")
                    f.write(f"# Internal ID: {agent.internal_id}\n")
                    f.write(f"# Protocol: {agent.protocol}\n")
                    f.write(f"# Framework: {agent.framework}\n")
                    # Format deployment info nicely if it's a dictionary
                    if isinstance(agent.deployment, dict):
                        deployment_type = agent.deployment.get("type", "unknown")
                        f.write(f"# Deployment: {deployment_type}\n\n")
                    else:
                        f.write(f"# Deployment: {agent.deployment}\n\n")

                    # Write langgraph implementation
                    self._write_langgraph_implementation(f)
                self.ui.file_operation("Created file", str(agent_file))

                # Create nodes.py
                nodes_file = main_file / "nodes.py"
                with open(nodes_file, "w", encoding="utf-8") as f:
                    f.write(f"# {agent.name} agent nodes\n\n")
                    f.write("from typing import Dict, Any\n\n")
                    f.write("def process_node(state):\n")
                    f.write('    """Process the input and return an output."""\n')
                    f.write('    return {"output": f"Processed: {state[\'input\']}"}\n')
                self.ui.file_operation("Created file", str(nodes_file))

                # Create graph.py
                graph_file = main_file / "graph.py"
                with open(graph_file, "w", encoding="utf-8") as f:
                    f.write(f"# {agent.name} agent graph definition\n\n")
                    f.write("from langgraph.graph import StateGraph\n")
                    f.write("from .nodes import process_node\n")
                    f.write("from .state import State\n\n")
                    f.write("# Define the graph\n")
                    f.write("def create_graph():\n")
                    f.write("    builder = StateGraph(State)\n")
                    f.write('    builder.add_node("process", process_node)\n')
                    f.write('    builder.set_entry_point("process")\n')
                    f.write("    return builder.compile()\n\n")
                    f.write("graph = create_graph()\n")
                self.ui.file_operation("Created file", str(graph_file))

                # Create state.py
                state_file = main_file / "state.py"
                with open(state_file, "w", encoding="utf-8") as f:
                    f.write(f"# {agent.name} agent state definition\n\n")
                    f.write("from typing import TypedDict, Optional\n\n")
                    f.write("class State(TypedDict):\n")
                    f.write("    input: str\n")
                    f.write("    output: Optional[str]\n")
                self.ui.file_operation("Created file", str(state_file))

                # Create __main__.py
                main_py_file = main_file / "__main__.py"
                with open(main_py_file, "w", encoding="utf-8") as f:
                    f.write(f"# {agent.name} agent entry point\n\n")
                    f.write("from .agent import graph\n\n")
                    f.write('if __name__ == "__main__":\n')
                    f.write('    result = graph.invoke({"input": "Hello, world!"})\n')
                    f.write('    print(f"Result: {result}")\n')
                self.ui.file_operation("Created file", str(main_py_file))

                self.ui.success(
                    f"Successfully created folder-based langgraph agent in {main_file}"
                )

            except Exception as e:
                error_msg = f"Error creating langgraph agent files: {str(e)}"
                self.ui.error(error_msg)
                raise
        else:
            # For file-based agents, write to a single file
            self.ui.step(f"Writing default implementation to: {main_file}")

            # Create parent directory if needed
            parent_dir = main_file.parent
            if parent_dir != Path(".") and not parent_dir.exists():
                os.makedirs(parent_dir, exist_ok=True)
                self.ui.file_operation("Created directory", str(parent_dir))

            try:
                self.ui.debug(f"Writing agent implementation file: {main_file}")
                with open(main_file, "w", encoding="utf-8") as f:
                    # Write header comments
                    f.write(f"# {agent.name} agent implementation\n")
                    f.write(f"# {agent.desc}\n")
                    f.write(f"# {agent.type} agent\n")
                    f.write(f"# Internal ID: {agent.internal_id}\n")
                    f.write(f"# Protocol: {agent.protocol}\n")
                    f.write(f"# Framework: {agent.framework}\n")
                    # Format deployment info nicely if it's a dictionary
                    if isinstance(agent.deployment, dict):
                        deployment_type = agent.deployment.get("type", "unknown")
                        f.write(f"# Deployment: {deployment_type}\n\n")
                    else:
                        f.write(f"# Deployment: {agent.deployment}\n\n")

                    # Write type-specific implementation
                    if agent.type == AgentType.LANGCHAIN.value:
                        self._write_langchain_implementation(f)
                    elif agent.type == AgentType.LANGGRAPH.value:
                        self._write_langgraph_implementation(f)
                    elif agent.type == AgentType.PYDANTIC.value:
                        self._write_pydantic_implementation(f)

                self.ui.success(
                    f"Successfully wrote default implementation to {main_file}"
                )
                self.ui.file_operation("Created file", str(main_file))
            except Exception as e:
                error_msg = f"Error writing default implementation: {str(e)}"
                self.ui.error(error_msg)
                raise

    def _write_langchain_implementation(self, f) -> None:
        """Write a default LangChain implementation.

        Args:
            f: File object to write to
        """
        f.write("from langchain.llms import OpenAI\n")
        f.write("from langchain.chains import LLMChain\n")
        f.write("from langchain.prompts import PromptTemplate\n\n")

        f.write("# Define your chain\n")
        f.write('template = """You are an AI assistant. {input}"""\n')
        f.write(
            'prompt = PromptTemplate(template=template, input_variables=["input"])\n'
        )
        f.write("llm = OpenAI()\n")
        f.write("chain = LLMChain(llm=llm, prompt=prompt)\n")

    def _write_langgraph_implementation(self, f) -> None:
        """Write a default LangGraph implementation.

        Args:
            f: File object to write to
        """
        f.write("from langgraph.graph import StateGraph\n")
        f.write("from typing import TypedDict, Annotated, Dict, Any\n\n")

        f.write("# State definition\n")
        f.write("class State(TypedDict):\n")
        f.write("    input: str\n")
        f.write("    output: str\n\n")

        f.write("# Node function\n")
        f.write("def process(state: State) -> Dict[str, Any]:\n")
        f.write('    """Process the input and return an output."""\n')
        f.write('    return {"output": f"Processed: {state[\'input\']}"}\n\n')

        f.write("# Define the graph\n")
        f.write("builder = StateGraph(State)\n")
        f.write('builder.add_node("process", process)\n')
        f.write('builder.set_entry_point("process")\n')
        f.write("graph = builder.compile()\n")

    def _write_pydantic_implementation(self, f) -> None:
        """Write a default Pydantic implementation.

        Args:
            f: File object to write to
        """
        f.write("from pydantic import BaseModel, Field\n")
        f.write("from typing import Optional, List, Dict, Any\n\n")

        f.write("class Request(BaseModel):\n")
        f.write("    input: str\n")
        f.write("    metadata: Optional[Dict[str, Any]] = None\n\n")

        f.write("class Response(BaseModel):\n")
        f.write("    output: str\n")
        f.write("    error: Optional[str] = None\n\n")

        f.write("def process(request: Request) -> Response:\n")
        f.write('    """Process the request and return a response."""\n')
        f.write('    return Response(output=f"Processed: {request.input}")\n')

    def run_linters_on_generated_files(self, agent: Agent) -> None:
        """Run linters on generated files to clean up formatting.

        Args:
            agent: The agent object
        """
        self.ui.section("Formatting Generated Files")
        self.ui.step("Running linters to clean up generated files")

        # Get the base directory for the agent
        agent_dir = os.path.dirname(agent.path)

        # Check if formatters are installed
        black_installed = self._check_tool_installed("black")
        isort_installed = self._check_tool_installed("isort")

        if not black_installed and not isort_installed:
            self.ui.warning("Formatters (black, isort) are not installed")
            self.ui.info("To install formatters, run: pip install black isort")
            self.ui.info("Skipping formatting step")
            return

        try:
            # Run Black formatter if installed
            if black_installed:
                self.ui.info("Running Black formatter to remove excessive blank lines")
                with self.ui.console.status("Running Black formatter...") as status:
                    command = f"black {agent_dir} --quiet"
                    self.ui.debug(f"Running command: {command}")
                    result = os.system(command)
                    if result == 0:
                        status.update("Black formatter completed successfully")
                        self.ui.success("Black formatter completed successfully")
                    else:
                        status.update("Black formatter encountered issues")
                        self.ui.warning("Black formatter encountered issues")
            else:
                self.ui.warning("Black formatter not installed. Skipping.")
                self.ui.info("To install Black, run: pip install black")

            # Run isort to organize imports if installed
            if isort_installed:
                self.ui.info("Running isort to organize imports")
                with self.ui.console.status("Running isort...") as status:
                    command = f"isort {agent_dir} --quiet"
                    self.ui.debug(f"Running command: {command}")
                    result = os.system(command)
                    if result == 0:
                        status.update("isort completed successfully")
                        self.ui.success("isort completed successfully")
                    else:
                        status.update("isort encountered issues")
                        self.ui.warning("isort encountered issues")
            else:
                self.ui.warning("isort not installed. Skipping.")
                self.ui.info("To install isort, run: pip install isort")

            if black_installed or isort_installed:
                self.ui.success("Generated files have been formatted")
            else:
                self.ui.info("No formatters were run")
        except Exception as e:
            self.ui.error(f"Error running linters: {str(e)}")
            self.ui.warning(
                "Skipping linting step, files may contain excessive blank lines"
            )

    def _check_tool_installed(self, tool_name: str) -> bool:
        """Check if a command-line tool is installed and available.

        Args:
            tool_name: Name of the tool to check

        Returns:
            bool: True if the tool is installed, False otherwise
        """
        # Use 'where' on Windows and 'which' on Unix-like systems
        if os.name == "nt":  # Windows
            check_cmd = f"where {tool_name}"
        else:  # Unix-like
            check_cmd = f"which {tool_name}"

        # Run the command and check the return code
        # Return code 0 means the tool was found
        return (
            os.system(
                f"{check_cmd} > nul 2>&1"
                if os.name == "nt"
                else f"{check_cmd} > /dev/null 2>&1"
            )
            == 0
        )
