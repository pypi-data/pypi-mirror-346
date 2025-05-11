#
# AI-on-Rails: All rights reserved.
#

import rich_click as click
import os
import re
from ruamel.yaml import YAML

from .common.config import Config, DEFAULT_CONFIG_PATH
from .utils.ui import UI


@click.command()
@click.argument("name")
@click.option("--desc", default="A new AI-on-Rails application")
@click.option("--tag", type=str, help="Tag of the agent", multiple=True, default=[])
@click.option(
    "--lang",
    type=str,
    help="Language of the application",
    default="en",
    show_default=True,
)
@click.option(
    "--currency",
    type=str,
    help="Currency used for pricing",
    default="USD",
    show_default=True,
)
@click.option(
    "--buy-price",
    type=float,
    help="The price to purchase the application indefinitely (until it is unpublished)",
    required=False,
)
@click.option(
    "--rent-price",
    type=float,
    help="The price to rent the application for a period of time",
    required=False,
)
@click.option(
    "--rent-period",
    type=int,
    help="The period of time to rent the application (in days)",
    required=False,
)
@click.option("--query-price", type=float, help="The price per query", required=False)
@click.pass_context
def new(
    ctx,
    name: str,
    desc: str,
    tag: list[str],
    lang: str,
    currency: str,
    buy_price: float | None,
    rent_price: float | None,
    rent_period: str | None,
    query_price: float | None,
):
    """Create a new AI-on-Rails application."""

    # Get no_ansi from context if available
    no_ansi = ctx.obj.get("NO_ANSI", False) if ctx.obj else False

    # Get debug mode from context
    debug = ctx.obj.get("DEBUG", False) if ctx.obj else False

    # Initialize UI with debug mode and no_ansi flag
    ui = UI(debug_mode=debug, no_ansi=no_ansi)

    if tag and len(tag) > 5:
        ui.error("Each application can have at most 5 tags.")
        return

    if buy_price is not None:
        if buy_price < 0.01:
            ui.error("Buy price must be greater or equal to 0.01.")
            return

    if rent_price is not None:
        if rent_period is None:
            raise click.UsageError(
                "Rent period is required when rent price is provided."
            )
        if rent_price < 0.01:
            ui.error("Rent period must be greater or equal to 0.01.")
            return

    if rent_period is not None:
        if rent_price is None:
            raise click.UsageError(
                "Rent price is required when rent period is provided."
            )
        if rent_period <= 0:
            ui.error("Rent period must be greater than 0.")
            return

    if query_price is not None:
        if query_price < 0.01:
            ui.error("Query price must be greater or equal to 0.01.")
            return

    ui.header(f"Creating new application", f"Name: {name}")

    # Create the application
    def create_application():
        # Convert name to a Python-friendly directory name
        # Replace spaces with underscores, convert to lowercase, and remove non-alphanumeric characters
        import re
        dir_name = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower().replace(' ', '_'))
        # Remove consecutive underscores
        dir_name = re.sub(r'_+', '_', dir_name)
        # Remove leading/trailing underscores
        dir_name = dir_name.strip('_')
        # Ensure it's not empty
        if not dir_name:
            dir_name = "aor_application"
        
        # Create directory
        os.makedirs(dir_name, exist_ok=True)

        # Create config file path
        config_path = f"{dir_name}/{DEFAULT_CONFIG_PATH}"

        # Prepare config data
        config_data = {
            "name": name,
            "desc": desc,
            "cover": "",
            "version": "0.1.0",
            "lang": lang,
            "currency": currency,
            # "agents": []
            "endpoints": [],
        }

        if buy_price is not None:
            config_data["buy_price"] = buy_price
        if rent_price is not None:
            config_data["rent_price"] = rent_price
            if rent_period is not None:
                config_data["rent_period"] = rent_period
        if query_price is not None:
            config_data["query_price"] = query_price
        if tag and len(tag) > 0:
            config_data["tags"] = list(tag)

        # Create the config file
        yaml = YAML()
        yaml.indent = 2
        yaml.preserve_quotes = True

        # Create the config file with initial data
        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(config_data, f)

        return config_path

    config_path = ui.process_spinner(
        "Creating application structure", create_application
    )

    # Show application details
    ui.section("Application Details")
    ui.value("Name", name)
    ui.value("Description", desc)
    ui.value("Version", "0.1.0")
    ui.value("Language", lang)
    ui.value("Currency", currency)

    if tag and len(tag) > 0:
        ui.value("Tags", ", ".join(tag))

    if buy_price is not None:
        ui.value("Buy Price", f"{buy_price} {currency}")
    if rent_price is not None:
        ui.value("Rent Price", f"{rent_price} {currency} for {rent_period} days")
    if query_price is not None:
        ui.value("Query Price", f"{query_price} {currency}")

    ui.path(config_path)
    ui.success(f"Application {name} created successfully.")

    # Suggest next steps
    ui.section("Next Steps")
    # Use sanitized directory name for cd command
    import re
    dir_name = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower().replace(' ', '_'))
    dir_name = re.sub(r'_+', '_', dir_name)
    dir_name = dir_name.strip('_')
    if not dir_name:
        dir_name = "aor_application"
    ui.command("cd " + dir_name, "Navigate to your new application directory")
    ui.command("aor add <NAME>", "Add an agent to your application")
