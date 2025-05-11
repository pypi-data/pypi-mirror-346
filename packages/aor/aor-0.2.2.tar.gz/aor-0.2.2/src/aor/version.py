#
# AI-on-Rails: All rights reserved.
#

import rich_click as click
from .common.config import Config
from .utils.ui import UI


@click.command(name="version-bump")
@click.option("--major", is_flag=True, help="Bump the major version (x.0.0)")
@click.option("--minor", is_flag=True, help="Bump the minor version (0.x.0)")
@click.option("--patch", is_flag=True, help="Bump the patch version (0.0.x)")
@click.pass_context
def version_bump(ctx, major: bool, minor: bool, patch: bool):
    """Bump the version of the current application."""

    # Get no_ansi from context if available
    no_ansi = ctx.obj.get("NO_ANSI", False) if ctx.obj else False

    # Get debug mode from context
    debug = ctx.obj.get("DEBUG", False) if ctx.obj else False

    # Initialize UI
    ui = UI(debug_mode=debug, no_ansi=no_ansi)
    ui.banner("AI-on-Rails")
    ui.header("Version Management")

    # Load configuration
    try:
        config = Config()
    except Exception as e:
        ui.error(f"Failed to load configuration: {str(e)}")
        return

    current_version = config.get("version")
    ui.value("Current version", current_version)

    # Verify version format
    try:
        version_parts = current_version.split(".")
        if len(version_parts) != 3:
            ui.error(
                f"Invalid version format: {current_version}. Expected format: x.y.z"
            )
            return

        # Convert to integers to verify they're valid numbers
        major_num, minor_num, patch_num = (
            int(version_parts[0]),
            int(version_parts[1]),
            int(version_parts[2]),
        )
    except ValueError:
        ui.error(
            f"Invalid version format: {current_version}. Version components must be numbers."
        )
        return

    # Determine bump type
    bump_type = "patch"  # Default
    if major:
        bump_type = "major"
    elif minor:
        bump_type = "minor"
    elif patch:
        bump_type = "patch"

    ui.info(f"Performing a {bump_type} version bump")

    # Bump the version
    def bump_version():
        version_parts = current_version.split(".")
        if bump_type == "major":
            version_parts[0] = str(int(version_parts[0]) + 1)
            version_parts[1] = "0"
            version_parts[2] = "0"
        elif bump_type == "minor":
            version_parts[1] = str(int(version_parts[1]) + 1)
            version_parts[2] = "0"
        else:  # patch
            version_parts[2] = str(int(version_parts[2]) + 1)

        # Update version in config
        new_version = ".".join(version_parts)
        config.set("version", new_version)
        config.save()

        return new_version

    try:
        new_version = ui.process_spinner("Updating version", bump_version)
        ui.success(f"Version bumped successfully")

        # Show version change details
        ui.section("Version Change")
        ui.value("Previous version", current_version)
        ui.value("New version", new_version)

        # Additional information based on bump type
        if bump_type == "major":
            ui.info("Major version bumps indicate breaking changes")
        elif bump_type == "minor":
            ui.info(
                "Minor version bumps indicate new features with backward compatibility"
            )
        else:
            ui.info("Patch version bumps indicate bug fixes and small changes")

    except Exception as e:
        ui.error(f"Failed to bump version: {str(e)}")
