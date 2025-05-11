"""
Agent creation module for adding new agents to the application.

This module provides functionality to create and configure different types of agents
(pydantic, langchain, langgraph) with various protocols and deployment options.
# Note: Framework functionality is currently disabled
"""

import os
from typing import Optional

import rich_click as click

from .utils.ui import UI
from .common.agent import Agent
from .common.config import Config
from .agent_management import (
    AgentType,
    ProtocolType,
    # FrameworkType,  # Framework functionality is disabled
    DeploymentType,
    AgentCreationContext,
    AgentPathManager,
    AgentConfigManager,
    InputOutputManager,
    AgentCodeGenerator,
)
from .agent_management.validation_utils import validate_name


@click.command()
@click.argument("name")
@click.option("--desc", default=None, help="Description of the agent")
@click.option(
    "--type",
    type=click.Choice(["pydantic", "langchain", "langgraph"]),
    help="Type of the agent",
    default="langgraph",
)
# @click.option("--show-graph", is_flag=True, help="Publish the graph of the agent")
@click.option("--path", type=str, help="Path to the agent implementation file")
@click.option(
    "--protocol",
    type=click.Choice(["a2a", "raw", "custom"]),
    default="a2a",
    help="Communication protocol to use",
)
# Framework functionality is disabled
# @click.option(
#     "--framework",
#     type=click.Choice(["fastapi", "flask"]),
#     default=None,
#     help="Web framework to use",
# )
@click.option(
    "--deploy",
    type=click.Choice(["aws-lambda", "ec2", "local"]),
    default="aws-lambda",
    help="Deployment target",
)
@click.option(
    "--manual",
    is_flag=True,
    help="Create a template config file for manual editing without generating code",
)
@click.option(
    "--continue",
    "continue_flag",
    is_flag=True,
    help="Continue agent creation process after manual config editing",
)
@click.pass_context
def add(
    ctx,
    name: str,
    desc: Optional[str],
    type: str,
    # show_graph: bool,
    path: Optional[str],
    protocol: str,
    # framework: str,  # Framework functionality is disabled
    deploy: str,
    manual: bool = False,
    continue_flag: bool = False,
) -> None:
    """Add a new agent to the current application."""

    # Get no_ansi from context if available
    no_ansi = ctx.obj.get("NO_ANSI", False) if ctx.obj else False

    # Get debug mode from context
    debug = ctx.obj.get("DEBUG", False) if ctx.obj else False

    # Initialize UI with debug mode and no_ansi flag
    ui = UI(debug_mode=debug, no_ansi=no_ansi)

    # Create context object to store all parameters
    context = AgentCreationContext(
        ui=ui,
        name=name,
        desc=desc,
        agent_type=type,
        # show_graph=show_graph,
        path=path or "",
        protocol=protocol,
        framework=None,  # Framework functionality is disabled
        deploy=deploy,
        manual=manual,
        continue_flag=continue_flag,
    )

    # Initialize managers
    path_manager = AgentPathManager(ui)
    config_manager = AgentConfigManager(ui)
    input_output_manager = InputOutputManager(ui)
    code_generator = AgentCodeGenerator(ui)

    # Start a logical group for the agent creation process
    if continue_flag:
        ui.header(
            f"Continuing Agent Creation: {name}",
            "Reading configuration and generating code",
        )
    else:
        ui.header(
            f"Adding Agent: {name}",
            f"Type: {type} | Protocol: {protocol} | Deploy: {deploy}{' | Manual Mode' if manual else ''}",
            # Note: Framework functionality is disabled
        )

    # Load configuration
    context.config = config_manager.load_configuration()
    if not context.config:
        ui.group_end(f"Adding Agent: {name}", success=False)
        return
    # Validate agent name
    is_valid, error_message = validate_name(name)
    if not is_valid:
        ui.error(f"Invalid agent name: {error_message}")
        ui.info(
            "Agent names must start with a letter and contain only letters, numbers, underscores, and spaces."
        )
        ui.group_end(f"Adding Agent: {name}", success=False)
        return

    # Set validated agent name
    context.name = name

    # Handle continue flag - find existing agent in config
    if continue_flag:
        ui.info(f"Continuing agent creation for: {context.name}")
        context.agent = config_manager.find_agent_in_config(
            context.config, context.name
        )
        if not context.agent:
            ui.error(
                f"Agent '{context.name}' not found in configuration. Create it first with 'aor add {context.name} --manual'"
            )
            ui.group_end(f"Continuing Agent Creation: {context.name}", success=False)
            return

        # Extract agent properties from the loaded config
        context.agent_type = context.agent.type
        context.protocol = getattr(context.agent, "protocol", ProtocolType.A2A.value)
        # Framework functionality is disabled
        # context.framework = getattr(context.agent, "framework", None)
        context.framework = None
        deployment = getattr(
            context.agent,
            "deployment",
            {"type": DeploymentType.AWS_LAMBDA.value},
        )
        # Handle both string and dictionary deployment values
        if isinstance(deployment, dict):
            context.deploy = deployment.get("type", DeploymentType.AWS_LAMBDA.value)
        else:
            context.deploy = deployment
        context.show_graph = getattr(context.agent, "show_graph", False)
        context.desc = context.agent.desc
        context.path = context.agent.path

        ui.info(
            f"Loaded agent configuration: Type: {context.agent_type}, Protocol: {context.protocol}, "
            f"Deploy: {context.deploy}"
        )
        # Note: Framework functionality is disabled
    else:
        ui.info(f"Adding agent: {context.name}")
        ui.debug(
            f"Agent parameters - Type: {context.agent_type}, Protocol: {context.protocol}, "
            f"Deploy: {context.deploy}"
        )
        # Note: Framework functionality is disabled

        # Set default path if not provided
        if not context.path:
            # Create agent object to generate internal_id
            from .agent_management.validation_utils import generate_stable_internal_id

            internal_id = generate_stable_internal_id(context.name)

            # For langgraph agents, use folder-based path
            if context.agent_type == AgentType.LANGGRAPH.value:
                context.path = f"src/{internal_id}"
            else:
                context.path = f"src/{internal_id}/agent.py"
            ui.info(f"Using default path: {context.path} (based on stable ID)")

        # Create and configure agent object
        context.agent = config_manager.create_agent_object(
            context.name,
            context.desc,
            context.agent_type,
            context.show_graph,
            context.path,
            context.protocol,
            context.framework,
            context.deploy,
            context.manual,
            input_output_manager,
        )

        # Handle existing agent path
        ui.step(f"Preparing agent path: {context.path}")
        if not path_manager.prepare_agent_path(context.path):
            ui.error(f"Failed to prepare agent path: {context.path}")
            ui.group_end(f"Adding Agent: {context.name}", success=False)
            return

        # Add agent to config
        if not config_manager.update_configuration(
            context.config, context.agent, context.manual
        ):
            ui.warning(f"Failed to add agent '{context.name}' to configuration")
            ui.group_end(f"Adding Agent: {context.name}", success=False)
            return

        # If manual mode, skip code generation
        if context.manual:
            ui.section("Manual Agent Creation")
            ui.info("Code generation has been skipped.")
            ui.info("A template configuration has been created for you to edit.")
            ui.info(
                "The configuration includes example inputs and outputs with instructions."
            )
            ui.info("Edit the inputs and outputs to match your requirements.")
            ui.info("Remove the 'EXAMPLE_' prefix from names you want to keep.")
            ui.info("To continue the agent creation process after editing, run:")
            ui.command(
                f"aor add {context.name} --continue", "Continue agent creation process"
            )
            # Success message for manual mode
            ui.success(f"Agent '{context.name}' added to the current application")
        else:
            # Apply components based on agent type and options
            ui.section("Generating Agent Code")
            ui.step(
                f"Generating code for {context.agent_type} agent with {context.protocol} protocol"
            )
            try:
                code_generator.generate_agent_code(
                    context.agent,
                    context.name,
                    context.desc,
                    context.protocol,
                    None,  # Framework functionality is disabled
                    context.deploy,
                )

                # Run formatters on the generated code
                code_generator.run_linters_on_generated_files(context.agent)

                # Only show success message after code generation is complete
                ui.success(f"Agent '{context.name}' added to the current application")
            except Exception as e:
                ui.error(f"Failed to generate code for agent '{context.name}': {e}")
                ui.warning(
                    "Agent was added to configuration but code generation failed."
                )
                ui.warning("You may need to manually fix the issues or try again.")

    # Display agent information
    ui.section("Agent Details")
    ui.agent_info(context.agent.to_dict())
    # End the logical group
    ui.group_end(f"Adding Agent: {context.name}", success=True)

    ui.info("Use `aor deploy` to deploy the application.")
    ui.info("Use `aor lint` to check the application readiness.")
