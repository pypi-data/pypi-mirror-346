"""
Template rendering system for AI-on-Rails templates using Jinja2.
"""

from pathlib import Path
from typing import Dict, Any
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from aor.templates.utils.text_case_converter import TextCaseConverter


class TemplateRenderer:
    """
    Renders templates using Jinja2 with custom filters.

    This class is responsible for rendering template files and strings using
    Jinja2 with custom filters for text case conversion.
    """

    def __init__(self, template_dir: Path, ui):
        """
        Initialize the template renderer.

        Args:
            template_dir: Root directory for the template
            ui: UI instance for output and logging
        """
        self.template_dir = template_dir
        self.ui = ui
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(["html", "xml"]),
            keep_trailing_newline=True,
        )
        self._register_filters()

    def _register_filters(self) -> None:
        """Register custom filters for the Jinja2 environment."""
        self.env.filters["snake_case"] = TextCaseConverter.snake_case
        self.env.filters["pascal_case"] = TextCaseConverter.pascal_case
        self.env.filters["title_case"] = TextCaseConverter.title_case
        self.env.filters["camel_case"] = TextCaseConverter.camel_case
        
        # Register new safe filters
        self.env.filters["safe_pascal_case"] = lambda text: TextCaseConverter.safe_pascal_case(text)[0]
        
        # Register validation filters
        self.env.filters["is_valid_python_identifier"] = lambda text: TextCaseConverter.is_valid_python_identifier(text)[0]

    def render_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """
        Render a template string with the given context.

        Args:
            template_string: Jinja2 template string
            context: Variables for template rendering

        Returns:
            Rendered string
        """
        template = self.env.from_string(template_string)
        return template.render(**context)

    def render_template(self, template_path: str, context: Dict[str, Any]) -> str:
        """
        Render a template file with the given context.

        Args:
            template_path: Path to the template file relative to template_dir
            context: Variables for template rendering

        Returns:
            Rendered content
        """
        try:
            # Ensure template path uses forward slashes (required by jinja2)
            template_path = template_path.replace("\\", "/")
            self.ui.debug(f"Loading template: {template_path}")
            template = self.env.get_template(template_path)
            return template.render(**context)
        except TemplateNotFound as e:
            self.ui.error(f"Template not found: {template_path}")
            self.ui.error(f"Available templates: {self.env.list_templates()}")
            raise e
        except Exception as e:
            self.ui.error(f"Error rendering template {template_path}: {str(e)}")
            raise e
