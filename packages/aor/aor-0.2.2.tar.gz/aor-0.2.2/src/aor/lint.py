#
# AI-on-Rails: All rights reserved.
#

import rich_click as click
import os

from .common.config import Config
from .utils.ui import UI


@click.command()
@click.pass_context
def lint(ctx):
    """Lint the current application."""

    # Get no_ansi from context if available
    no_ansi = ctx.obj.get("NO_ANSI", False) if ctx.obj else False

    # Get debug mode from context
    debug = ctx.obj.get("DEBUG", False) if ctx.obj else False

    # Initialize UI
    ui = UI(debug_mode=debug, no_ansi=no_ansi)
    ui.header("Linting Application")

    readiness = -1
    try:
        # Load the config to get the syntax checked implicitly
        ui.info("Checking configuration syntax")
        config = Config()
        ui.success("Basic syntax...", end="")
        config = Config()
        ui.success("OK")

        # Display basic config info
        ui.section("Configuration Details")
        app_name = config.get("name", "Unknown")
        ui.value("Application", app_name)
        ui.value("Version", config.get("version", "Unknown"))

        # Count endpoints
        endpoints = config.get("endpoints", [])
        ui.value("Endpoints", len(endpoints))

        readiness = Config.NOT_READY
        ui.text("Ready to be deployed... ", end="")
        config = Config(readiness=Config.READY_TO_DEPLOY)
        ui.success("")

        readiness = Config.READY_TO_DEPLOY
        ui.text("Ready to be published... ", end="")
        config = Config(readiness=Config.READY_TO_PUBLISH)
        ui.success("")

        readiness = Config.READY_TO_PUBLISH
        ui.text("Ready to be executed... ", end="")
        config = Config(readiness=Config.READY_TO_EXECUTE)
        ui.success("")

        readiness = Config.READY_TO_EXECUTE
        ui.text("Ready to be advertised... ", end="")
        config = Config(readiness=Config.READY_TO_ADVERTISE)
        ui.success("")

        readiness = Config.READY_TO_ADVERTISE
        ui.text("Fully configured... ", end="")
        config = Config(readiness=Config.FULLY_CONFIGURED)
        ui.success("")

        readiness = Config.FULLY_CONFIGURED
        ui.success("Lint completed successfully")
    except Exception as e:
        ui.error(f"Failed")
        ui.error(f"Error: {str(e)}")
        if readiness == -1:
            ui.info("Basic configuration file sytax is broken.")
        elif readiness == Config.NOT_READY:
            ui.info(
                "Basic syntax is OK but the application is not ready to be deployed."
            )
        elif readiness == Config.READY_TO_DEPLOY:
            ui.info(
                "Application is ready to be deployed, but not yet ready to be published to AI-on-Rails."
            )
            ui.info("Please, consider running `aor deploy` to deploy the application.")
        elif readiness == Config.READY_TO_PUBLISH:
            ui.info(
                "Application is deployed, ready to be published to become available through the API, but not yet ready to be advertised to the public."
            )
            ui.info(
                "Please, consider running `aor publish` to publish the application."
            )
        elif readiness == Config.READY_TO_EXECUTE:
            ui.info(
                "Application is deployed, published, ready to be executed through the API, but not yet ready to be advertised to the public."
            )
            ui.info(
                "Please, complement the application description in the configuration file."
            )
        elif readiness == Config.READY_TO_ADVERTISE:
            ui.info(
                "Application is deployed, published, and ready to be advertised to the public."
            )
            ui.info(
                "Please, consider re-running `aor publish` to publish the application description updates and to queue it for review."
            )
        elif readiness == Config.FULLY_CONFIGURED:
            ui.info(
                "Application is fully configured, deployed, published, reviewed and advertised to the public."
            )

        if debug:
            raise
