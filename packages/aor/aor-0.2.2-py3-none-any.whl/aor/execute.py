#
# AI-on-Rails: All rights reserved.
#
"""Execute requests through the AI-on-Rails proxy API."""

import json
import sys
from typing import Dict, Any, List, Optional

import rich_click as click

from .common.config import Config
from .system.token import get_token
from .backend.config import configure
from .backend.execute import ExecuteRequest, ProtocolType, detect_protocol
from .backend.resolve import Resolve
from .utils.ui import UI


@click.command()
@click.option("--token", type=str, help="Token for the AI-on-Rails API", required=False)
@click.option("--app", type=str, help="Application UUID", required=False)
@click.option("--endpoint", type=str, help="Endpoint UUID", required=False)
@click.option(
    "--name", type=str, help="Agent name (alternative to endpoint UUID)", required=False
)
@click.option(
    "--input", type=(str, str), multiple=True, help="Input name and value pairs"
)
@click.option(
    "--protocol",
    type=click.Choice(["a2a", "rest", "basic"]),
    help="Protocol to use (auto-detect if not specified)",
)
@click.pass_context
def execute(
    ctx,
    token: str | None,
    app: str | None,
    endpoint: str | None,
    name: str | None,
    input: List[tuple[str, str]],
    protocol: str | None,
):
    """Call the AI Agent through the platform proxy (use public UUIDs from `aor resolve`).

    Supports multiple protocols:
    - A2A (Agent-to-Agent): For compatibility
    - REST: For standard REST API calls
    - Basic: For multipart/form-data requests

    You can specify either --endpoint with the endpoint UUID or --name with the agent name.
    If neither is provided, an interactive selection will be shown.
    """

    # Get no_ansi from context if available
    no_ansi = ctx.obj.get("NO_ANSI", False) if ctx.obj else False

    # Get debug mode from context
    debug = ctx.obj.get("DEBUG", False) if ctx.obj else False

    # Configure backend
    configure(debug=debug)

    # Initialize UI
    ui = UI(debug_mode=debug, no_ansi=no_ansi)
    ui.header("Executing AI-on-Rails Request")

    # Get token if not provided
    if token is None:
        token = get_token()

    # Check if token exists
    if token is None:
        ui.error("No authentication token found.")
        ui.info("Please login first with 'aor login' to authenticate.")
        return

    # Try to load configuration
    config = None
    try:
        ui.debug("Loading configuration...")
        config = Config(readiness=Config.READY_TO_EXECUTE)
    except FileNotFoundError:
        if app is None or (endpoint is None and name is None):
            ui.error(
                "Configuration file not found and app or endpoint/name not provided."
            )
            return
        # If app and either endpoint or name are provided, we can continue without config
        ui.debug("Configuration file not found, but app and endpoint/name provided.")

    # Get app UUID
    app_uuid = app
    if app_uuid is None:
        if config is not None:
            app_uuid = config.get("uuid")
        if not app_uuid:
            ui.error("Application UUID not provided and not found in configuration.")
            return

        def resolve_endpoints():
            """Resolve endpoint UUIDs to public identifiers."""
            resolve_request = Resolve(token, config)
            return resolve_request.send()

        try:
            # Send the resolve request
            response = ui.process_spinner("Resolving endpoints", resolve_endpoints)

            # Format the response as pretty-printed JSON for better readability in debug mode

            # Check if the response contains a 'body' field with a JSON string
            body_json = {}
            formatted_response = response.copy()
            if isinstance(response.get("body"), str):
                try:
                    # Parse the nested JSON in the body field
                    body_json = json.loads(response["body"])
                    formatted_response["body"] = body_json
                except json.JSONDecodeError:
                    # If parsing fails, keep the original body
                    pass

            ui.debug(f"Server response: {json.dumps(formatted_response, indent=2)}")
            app_uuid = body_json.get("uuid")
            resolved_endpoints = body_json.get("endpoints", {})
            if resolved_endpoints:
                ui.section("Resolved Endpoints")
                for key, value in resolved_endpoints.items():
                    ui.value(key, value)
            else:
                ui.warning("No endpoints were resolved.")
        except Exception as e:
            ui.error(f"Failed to resolve endpoints: {str(e)}")
            ui.debug("Check your API token and network connection.")
            if ui.debug_mode:
                raise e
            return

    def select_agent_interactively(endpoints):
        """Display a list of available agents and let the user select one.

        Args:
            endpoints: List of endpoint dictionaries

        Returns:
            Tuple of (endpoint_uuid, endpoint_data) or (None, None) if canceled
        """
        if not endpoints:
            return None, None

        ui.section("Available Agents")

        # Display the list of agents with numbers
        for i, e in enumerate(endpoints, 1):
            name = e.get("name", "Unnamed")
            desc = e.get("desc", "No description")
            ui.info(f"{i}. {name} - {desc}")

        # Prompt for selection
        try:
            selection = ui.prompt("Select an agent (number) or press Ctrl+C to cancel")

            # Convert to integer and validate
            try:
                idx = int(selection) - 1
                if 0 <= idx < len(endpoints):
                    selected = endpoints[idx]
                    ui.success(f"Selected agent: {selected.get('name')}")
                    return selected.get("uuid"), selected
                else:
                    ui.error(f"Invalid selection: {selection}")
                    return None, None
            except ValueError:
                ui.error(f"Invalid input: {selection}")
                return None, None

        except KeyboardInterrupt:
            ui.info("Agent selection canceled")
            return None, None

    # Get endpoint UUID and data
    endpoint_uuid = endpoint
    endpoint_data = None

    # If name is provided but endpoint is not, look up the endpoint by name
    if endpoint_uuid is None and name is not None:
        if config is not None:
            endpoints = config.get("endpoints", [])
            for e in endpoints:
                if e.get("name") == name:
                    endpoint_uuid = e.get("uuid")
                    endpoint_data = e
                    ui.info(
                        f"Found endpoint with name '{name}' (UUID: {endpoint_uuid})"
                    )
                    if (
                        "resolved_endpoints" in locals()
                        and endpoint_uuid in resolved_endpoints
                    ):
                        endpoint_uuid = resolved_endpoints[endpoint_uuid]
                        ui.info(
                            f"Using the public endpoint '{name}' (UUID: {endpoint_uuid})"
                        )
                    break

            if endpoint_uuid is None:
                ui.error(f"No endpoint found with name: {name}")
                return
        else:
            ui.error("Cannot resolve agent name without configuration file.")
            return
    elif endpoint_uuid is None:
        # No endpoint or name provided, try interactive selection
        if config is not None:
            endpoints = config.get("endpoints", [])
            if endpoints:
                selected_uuid, selected_data = select_agent_interactively(endpoints)
                if selected_uuid:
                    endpoint_uuid = selected_uuid
                    endpoint_data = selected_data
                    if (
                        "resolved_endpoints" in locals()
                        and endpoint_uuid in resolved_endpoints
                    ):
                        endpoint_uuid = resolved_endpoints[endpoint_uuid]
                        ui.info(
                            f"Using the public endpoint '{selected_data.get('name')}' (UUID: {endpoint_uuid})"
                        )
                else:
                    ui.info("Agent selection canceled")
                    return
            else:
                ui.error("No endpoints found in configuration.")
                return
        else:
            ui.error("Configuration file not found and no endpoint or name provided.")
            return

        if not endpoint_uuid:
            ui.error(
                "No endpoint selected. Use --endpoint, --name, or select interactively."
            )
            return
    else:
        # Try to find the endpoint data for the provided UUID
        if config is not None:
            endpoints = config.get("endpoints", [])
            for e in endpoints:
                if e.get("uuid") == endpoint_uuid:
                    endpoint_data = e
                    break

    # Convert input tuples to dictionary
    inputs = {}
    for name, value in input:
        inputs[name] = value

    # If no inputs provided, try to read from stdin
    if not inputs:
        ui.info("No inputs provided. Reading from stdin...")
        try:
            stdin_data = sys.stdin.read().strip()
            if stdin_data:
                try:
                    # Try to parse as JSON
                    json_data = json.loads(stdin_data)
                    if isinstance(json_data, dict):
                        inputs = json_data
                    else:
                        inputs = {"input": stdin_data}
                except json.JSONDecodeError:
                    # Use as raw text input
                    inputs = {"input": stdin_data}
        except Exception as e:
            ui.warning(f"Failed to read from stdin: {str(e)}")

    # Check if we have any inputs
    if not inputs:
        ui.error("No inputs provided. Use --input option or pipe data to stdin.")
        return

    ui.debug(f"Using app UUID: {app_uuid}")
    ui.debug(f"Using endpoint UUID: {endpoint_uuid}")
    ui.debug(f"Inputs: {json.dumps(inputs, indent=2)}")

    # Determine protocol to use
    protocol_type = None
    if protocol:
        # Use specified protocol
        protocol_type = ProtocolType(protocol)
        ui.debug(f"Using specified protocol: {protocol}")
    elif endpoint_data and "protocol" in endpoint_data:
        # No matter the endpoint protocol type, the proxy can speak any protocol.
        # Defaulting to A2A as the protocol to speak to the proxy.
        protocol_type = ProtocolType.A2A
        ui.debug(f"Using the default proxy protocol: {protocol_type.value}")

    # TODO(clairbee): If an explicit URL is given,
    #                 then assume that it's the URL of the agent itself (not through proxy),
    #                 and, thus, use the endpoint protocol type.
    # # Detect protocol from endpoint data
    # protocol_type = detect_protocol(endpoint_data)
    # ui.debug(f"Detected protocol from endpoint: {protocol_type.value}")

    # Create execute request
    execute_request = ExecuteRequest(
        token, app_uuid, endpoint_uuid, inputs, protocol_type, debug
    )

    def send_request():
        """Send the request."""
        return execute_request.send()

    try:
        # Send the request
        protocol_name = protocol_type.value if protocol_type else "auto-detected"
        response = ui.process_spinner(f"Sending {protocol_name} request", send_request)

        ui.debug(f"Raw response: {json.dumps(response, indent=2)}")

        # Extract text from response
        text_responses = execute_request.extract_response_text(response)

        # Display results
        ui.section("Response")

        if not text_responses:
            ui.warning("No text found in response.")
        else:
            for i, text in enumerate(text_responses):
                if i > 0:
                    ui.divider()
                ui.text(text)

    except Exception as e:
        error_message = str(e)

        # In debug mode, we'll show detailed error information
        if ui.debug_mode:
            ui.debug(f"Error details: {str(e)}")
            ui.debug(f"Error type: {type(e).__name__}")
            if hasattr(e, "details"):
                ui.debug(f"Additional details: {e.details}")

        # Extract the core error message without the detailed explanation
        core_error = (
            error_message.split("\n")[0] if "\n" in error_message else error_message
        )
        ui.error(f"Failed to execute request: {core_error}")

        # Add more specific guidance for common errors
        if "Invalid resource" in error_message:
            ui.error("The app or endpoint UUID could not be found on the server.")
            ui.info("Possible solutions:")
            ui.info("1. Verify you're logged in with 'aor login'")
            ui.info("2. Check that the app and endpoint UUIDs are correct")
            ui.info(
                "3. If using --name, ensure the agent name exists in your configuration"
            )
            ui.info(
                "4. Try running without --endpoint or --name to use interactive selection"
            )
            ui.info("5. Make sure the app and endpoint exist on the server")
            ui.info("6. Try resolving endpoints with 'aor resolve'")
            ui.info(
                "7. Run with --debug flag for more detailed information: 'aor --debug execute ...'"
            )
        elif "502" in error_message and "Internal server error" in error_message:
            ui.error("The server encountered an internal error (502 Bad Gateway).")
            ui.info("Possible solutions:")
            ui.info("1. Verify your API token is valid with 'aor login'")
            ui.info("2. Check your network connection")
            ui.info(
                "3. The backend service might be temporarily unavailable - try again later"
            )
            ui.info("4. Verify the input format is correct")
            ui.info(
                "5. Try with a simpler input to see if the complexity is causing issues"
            )
            ui.info("6. Contact support if the issue persists")
        else:
            ui.debug("Check your API token, UUIDs, and network connection.")

        return
