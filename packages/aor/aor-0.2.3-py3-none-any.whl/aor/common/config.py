#
# AI-on-Rails: All rights reserved.
#

import rich_click as click
import json
import os

import os
from ruamel.yaml import YAML
import fastjsonschema

DEFAULT_CONFIG_PATH = "aionrails.yaml"


def recursive_merge(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            dict1[key] = recursive_merge(dict1[key], value)
        else:
            # Merge non-dictionary values
            dict1[key] = value
    return dict1


class Config:
    """Configuration for the AI-on-Rails application."""

    path: str
    yaml_config: YAML
    config: dict

    NOT_READY = 0
    READY_TO_DEPLOY = 1
    READY_TO_PUBLISH = 2
    READY_TO_EXECUTE = 3
    READY_TO_ADVERTISE = 4
    FULLY_CONFIGURED = 5

    schema_suffix: dict[int, str] = {
        NOT_READY: "",
        READY_TO_DEPLOY: ".deploy",
        READY_TO_PUBLISH: ".publish",
        READY_TO_EXECUTE: ".execute",
        READY_TO_ADVERTISE: ".advertise",
        FULLY_CONFIGURED: ".full",
    }

    def __init__(self, path: str = DEFAULT_CONFIG_PATH, readiness: int = NOT_READY):
        self.path = path
        self.yaml_config = YAML()
        self.yaml_config.preserve_quotes = True
        self.yaml_config.indent = 4

        # Check if file exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"Configuration file not found: {path}")

        # Load the configuration
        with open(self.path, "r", encoding="utf-8") as f:
            self.config = self.yaml_config.load(f)

        # Check the config schema
        try:
            schema_obj = self.get_schema(readiness)
            self.schema = fastjsonschema.compile(schema_obj)
            self.schema(self.config)
        except fastjsonschema.JsonSchemaException as e:
            raise click.ClickException(f"Syntax error: {e}") from None
        except Exception as e:
            raise click.ClickException(
                f"Unknown error while checking syntax: {e}"
            ) from None

    def get_schema(self, readiness: int):
        # Get the schema for the given readiness
        try:
            schema_path = os.path.join(
                os.path.dirname(__file__),
                f"../schema/aionrails{self.schema_suffix[readiness]}.json",
            )
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_obj = json.load(f)
        except FileNotFoundError:
            raise click.ClickException(
                f"Schema file not found: {schema_path}"
            ) from None

        # Merge the schema with the schemas for the previous readiness levels
        if readiness > Config.NOT_READY:
            schema_previous = self.get_schema(readiness - 1)
            schema_obj = recursive_merge(schema_previous, schema_obj)

        return schema_obj

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value

    def to_dict(self) -> dict:
        return self.config

    def save(self):
        from aor.utils.ui import ui

        ui.info(f"Saving configuration to: {self.path}")
        try:
            with open(self.path, "w", encoding="utf-8") as f:
                self.yaml_config.dump(self.config, f)
            ui.success(f"Configuration saved successfully to: {self.path}")
        except Exception as e:
            ui.error(f"Error saving configuration to {self.path}: {str(e)}")
            import traceback

            ui.debug(f"Stack trace: {traceback.format_exc()}")
            raise
