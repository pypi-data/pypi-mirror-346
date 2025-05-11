#
# AI-on-Rails: All rights reserved.
#

import getpass
import os

import click

from .backend.login import Login
from .system.token import save_token
from .system.credentials import get_credentials, save_credentials
from .utils.ui import UI


@click.command()
@click.option("--email", type=str, help="Email")
@click.option("--password", type=str, help="Password")
@click.option(
    "--persist",
    is_flag=True,
    help="Persist the login credentials for future use",
)
@click.pass_context
def login(ctx, email: str | None, password: str | None, persist: bool):
    """Login to AI-on-Rails to persist a token to be used by other commands."""

    # Get no_ansi from context if available
    no_ansi = ctx.obj.get("NO_ANSI", False) if ctx.obj else False

    # Get debug mode from context
    debug = ctx.obj.get("DEBUG", False) if ctx.obj else False

    # Initialize UI
    ui = UI(debug_mode=debug, no_ansi=no_ansi)
    ui.header("Login to AI-on-Rails")

    if email is None and password is None:
        ui.info("No credentials provided, checking for saved credentials")
        email, password = get_credentials()

    if email is None:
        email = ui.prompt("Email")
    if password is None:
        password = getpass.getpass("Password: ")

    ui.debug(f"Logging in with email: {email}")

    try:
        login_client = Login(email, password)
        token = ui.process_spinner("Authenticating", login_client.send)

        save_token(token)
        ui.success("Logged in successfully")

        if persist:
            ui.info("Saving credentials for future use")
            save_credentials(email, password)
            ui.success("Credentials saved")
    except Exception as e:
        ui.error(f"Login failed: {str(e)}")
        if ui.debug_mode:
            raise
