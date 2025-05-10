"""
Utilities for the AI-on-Rails template system.
"""

from .template_manager import TemplateManager
from .component_combiner import ComponentCombiner
from .dependency_manager import DependencyManager
from .file_generator import FileGenerator
from .template_renderer import TemplateRenderer
from .text_case_converter import TextCaseConverter
from .validators.compatibility import CompatibilityValidator
from .validators.dependency import DependencyValidator
from .validators.metadata import MetadataValidator

__all__ = [
    "TemplateManager",
    "ComponentCombiner",
    "DependencyManager",
    "FileGenerator",
    "TemplateRenderer",
    "TextCaseConverter",
    "CompatibilityValidator",
    "DependencyValidator",
    "MetadataValidator",
]
