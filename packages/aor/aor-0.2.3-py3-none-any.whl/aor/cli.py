#
# AI-on-Rails: All rights reserved.
#

import platform
import sys
import logging
from typing import Optional, List, Dict, Any

from click import Context
import rich_click as click
from rich.console import Console

# Import commands
from .login import login
from .new import new
from .add import add
from .lint import lint
from .deploy import deploy
from .publish import publish
from .resolve import resolve
from .version import version_bump
from .rm import rm
from .execute import execute

from .utils.ui import UI

# Create UI instance
ui = UI()

# ASCII Art logo for AOR
AOR_LOGO = r"""
[bold blue]
    _     ___               ____         _  _
   / \   |_ _| ___   _ __  |  _ \  __ _ (_)| | ___     ___  ___   _ __ ___
  / _ \   | | / _ \ | '_ \ | |_) |/ _` || || |/ __|   / __|/ _ \ | '_ ` _ \
 / ___ \  | || (_) || | | ||  _ <| (_| || || |\__ \ _| (__| (_) || | | | | |
/_/   \_\|___|\___/ |_| |_||_| \_\\__,_||_||_||___/(_)\___|\___/ |_| |_| |_|

[/bold blue][bold cyan]Welcome to `AI on Rails`![/bold cyan]
"""

# Plain text logo for non-ANSI mode
PLAIN_LOGO = """
Welcome to `AI on Rails`!
"""

# Configure rich_click settings
click.rich_click.USE_RICH_MARKUP = True


# def format_beautiful_help(ctx: Context) -> None:
#     """
#     Display a beautiful help message for AOR CLI.

#     Args:
#         ctx: Click context object containing command information
#     """
#     # Extract command information
#     cmd = ctx.command
#     # Display logo
#     ui.console.print(AOR_LOGO)
#     # Display help text
#     ui.info("Rapid prototyping and publishing AI applications with guardrails.")

#     # Display usage
#     ui.section("Usage")
#     ui.command("aor [OPTIONS] COMMAND [ARGS]...")

#     # Display options
#     ui.section("Options")
#     options = [
#         ["--version", "Show the version and exit."],
#         ["--debug", "Enable debug mode"],
#         ["--help", "Show this message and exit."],
#     ]
#     ui.display_table("", ["Option", "Description"], options)

#     # Display commands
#     ui.section("Commands")

#     commands = [
#         ["add", "Add a new agent to the current application."],
#         ["deploy", "Deploy `AI on Rails` application to cloud services."],
#         ["execute", "Execute an A2A request through the proxy API."],
#         ["new", "Create a new `AI on Rails` application."],
#         ["publish", "Publish an `AI on Rails` application."],
#         ["rm", "Remove an agent from the current application."],
#         ["version-bump", "Bump the version of the `AI on Rails` application."],
#     ]

#     ui.display_table("", ["Command", "Description"], commands)

#     # Display footer
#     ui.console.print(
#         "\n[dim]Run 'aor COMMAND --help' for more information on a command.[/dim]"
#     )


# # Override the Click help formatting behavior
# original_format_help = click.core.Command.format_help


# def custom_format_help(self, ctx, formatter):
#     """Custom help formatter that intercepts the main help display."""
#     # If this is the main CLI command with no arguments, use our custom formatter
#     if self.name == "cli" and (
#         len(sys.argv) == 1 or "--help" in sys.argv or "-h" in sys.argv
#     ):
#         format_beautiful_help(ctx)
#         return

#     # Otherwise, use the original formatter
#     original_format_help(self, ctx, formatter)


# # Apply the monkey patch
# click.core.Command.format_help = custom_format_help


# Check if --no-ansi flag is in command line arguments
import sys

no_ansi_cli = "--no-ansi" in sys.argv

help_config = click.RichHelpConfiguration(
    color_system=(
        None
        if no_ansi_cli
        else ("windows" if platform.system() == "Windows" else "auto")
    ),
    force_terminal=False if no_ansi_cli else (platform.system() != "Windows"),
    show_arguments=True,
    text_markup=None if no_ansi_cli else "rich",
    use_markdown_emoji=False,
)
help_config.dump_to_globals()

command_groups = [
    {
        "name": "User commands",
        "commands": ["login"],
    },
    {
        "name": "Application commands",
        "commands": ["new", "lint", "deploy", "publish", "resolve", "version-bump"],
    },
    {
        "name": "AI Agent commands",
        "commands": ["add", "rm", "execute"],
    },
]

# Set the command groups for main CLI and all subcommands
click.rich_click.COMMAND_GROUPS = {
    "cli": command_groups,
    "add": [],  # Empty list means no grouping for add command options
    "new": [],
    "deploy": [],
    "publish": [],
    "login": [],
    "lint": [],
    "rm": [],
    "resolve": [],
    "version-bump": [],
    "execute": [],
}

# Create console for logo printing
console = Console(
    color_system=None if no_ansi_cli else "auto",
    markup=not no_ansi_cli,
    emoji=not no_ansi_cli,
)


# Custom command class to show logo for all commands
class LogoCommand(click.RichCommand):
    def get_help(self, ctx):
        # Show appropriate logo based on ANSI mode
        if no_ansi_cli:
            console.print(PLAIN_LOGO)
        else:
            console.print(AOR_LOGO)
        return super().get_help(ctx)


# Custom group class to show logo and handle subcommands
class LogoGroup(click.RichGroup):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all commands use LogoCommand
        self.command_class = LogoCommand

    def get_help(self, ctx):
        # Show appropriate logo based on ANSI mode
        if no_ansi_cli:
            console.print(PLAIN_LOGO)
        else:
            console.print(AOR_LOGO)
        return super().get_help(ctx)

    def add_command(self, cmd, name=None):
        # If command is a standard Click Command, convert it to LogoCommand
        if isinstance(cmd, click.Command) and not isinstance(cmd, LogoCommand):
            cmd.__class__ = LogoCommand
        return super().add_command(cmd, name)


@click.group(cls=LogoGroup)
@click.version_option(package_name="aor")
@click.option("--debug", is_flag=True, help="Enable debug mode")
@click.option(
    "--no-ansi", is_flag=True, help="Disable ANSI color codes and interactive elements"
)
@click.pass_context
def cli(ctx, debug, no_ansi):
    """AIonRails.com: A framework for rapid prototyping and publishing AI Agents, with guardrails and guiding rails."""

    # Store no_ansi and debug in the context for subcommands
    ctx.ensure_object(dict)
    ctx.obj["NO_ANSI"] = no_ansi
    ctx.obj["DEBUG"] = debug

    # Set debug mode if requested
    if debug:
        ui.debug_mode = True
        ui.debug("Debug mode enabled")

    # Set no-ansi mode if requested (already handled in ui.py, but we set it here for consistency)
    if no_ansi:
        ui.no_ansi = True


cli.context_settings = {
    "show_default": True,
}

# Register commands
cli.add_command(login)
cli.add_command(new)
cli.add_command(add)
cli.add_command(lint)
cli.add_command(deploy)
cli.add_command(publish)
cli.add_command(version_bump)
cli.add_command(rm)
cli.add_command(resolve)
cli.add_command(execute)
