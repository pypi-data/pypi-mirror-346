#
# AI-on-Rails: All rights reserved.
#
"""Resolve internal AI Agent identifiers into the publicly visible ones."""

import rich_click as click

from .common.config import Config
from .system.token import get_token
from .backend.config import configure
from .backend.resolve import Resolve
from .utils.ui import UI


@click.command()
@click.option("--token", type=str, help="Token for the AI-on-Rails API", required=False)
@click.pass_context
def resolve(ctx, token: str | None):
    """Resolve internal identifiers into the publicly visible ones."""

    # Get no_ansi from context if available
    no_ansi = ctx.obj.get("NO_ANSI", False) if ctx.obj else False

    # Get debug mode from context
    debug = ctx.obj.get("DEBUG", False) if ctx.obj else False

    # Configure backend
    configure(debug=debug)

    # Initialize UI
    ui = UI(debug_mode=debug, no_ansi=no_ansi)
    ui.header("Resolving Endpoints")

    # Load configuration
    ui.debug("Loading configuration...")
    config = Config(readiness=Config.READY_TO_EXECUTE)

    # Get token if not provided
    if token is None:
        token = get_token()

    # Check if app has UUID
    app_uuid = config.get("uuid")
    if not app_uuid:
        ui.error("Application has no UUID. Please publish it first.")
        return

    # Check if app has endpoints
    endpoints = config.get("endpoints", [])
    if not endpoints:
        ui.warning("Application has no endpoints to resolve.")
        return

    # Count endpoints with UUIDs
    endpoints_with_uuid = [e for e in endpoints if e.get("uuid")]
    if not endpoints_with_uuid:
        ui.error("No endpoints have UUIDs. Please publish the application first.")
        return

    ui.info(
        f"Resolving {len(endpoints_with_uuid)} endpoints for application '{config.get('name')}'"
    )

    # Create resolve request
    def resolve_endpoints():
        """Resolve endpoint UUIDs to public identifiers."""
        resolve_request = Resolve(token, config)
        return resolve_request.send()

    try:
        # Send the resolve request
        response = ui.process_spinner("Resolving endpoints", resolve_endpoints)

        # Format the response as pretty-printed JSON for better readability in debug mode
        import json

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

        # Check for errors
        if response.get("error"):
            ui.error(
                f"Failed to resolve endpoints: {response.get('message', 'Unknown error')}"
            )
            return

        # Display results
        ui.section("Resolution Results")

        # Display app information
        app_info = body_json.get("uuid", "N/A")
        if app_info:
            name = config.get("name")
            private_uuid = config.get("uuid")
            ui.value(
                f"Application: {name}",
                f"{private_uuid} (private) -> {app_info} (public)",
            )

        # Display endpoint information
        resolved_endpoints = body_json.get("endpoints", {})
        if resolved_endpoints:
            ui.section("Resolved Endpoints")
            for key, value in resolved_endpoints.items():
                for endpoint in config.get("endpoints", []):
                    if endpoint.get("uuid") == key:
                        name = endpoint.get("name")
                        private_uuid = endpoint.get("uuid")
                        ui.value(
                            f"Endpoint: {name}",
                            f"{private_uuid} (private) -> {value} (public)",
                        )
                        break
                else:
                    ui.warning(f"Endpoint with UUID {key} not found in configuration.")
        else:
            ui.warning("No endpoints were resolved.")

        ui.info(
            "Use `aor execute` to call the AI Agents using the public application and endpoint UUIDs, or let `aor execute` auto-detect them."
        )

    except Exception as e:
        ui.error(f"Failed to resolve endpoints: {str(e)}")
        ui.debug("Check your API token and network connection.")
        if ui.debug_mode:
            raise e
        return
