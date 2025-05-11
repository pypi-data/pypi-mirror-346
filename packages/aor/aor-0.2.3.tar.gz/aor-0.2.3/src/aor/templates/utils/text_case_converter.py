"""
Text case conversion utilities for template variables.
"""

import re
import keyword
from typing import Optional, Tuple


class TextCaseConverter:
    """
    Provides static methods for converting between different text cases.

    This class provides conversion utilities for:
    - snake_case
    - PascalCase
    - camelCase
    - Title Case

    These are primarily used as filters in Jinja2 templates.
    """

    @staticmethod
    def _remove_agent_suffix(text: str) -> str:
        # Remove 'agent' suffix from name for template processing only
        if text.lower().endswith("agent"):
            text = text[:-5]  # Remove "agent" suffix

        return text

    @staticmethod
    def snake_case(text: str) -> str:
        """
        Convert a string to snake_case.

        Examples:
        - 'UserProfile' -> 'user_profile'
        - 'courseSelector' -> 'course_selector'
        - 'Course Selector' -> 'course_selector'
        """
        if not text:
            return text

        # Handle spaces first (for Title Case input)
        s0 = text.replace(" ", "_")

        # Handle camelCase and PascalCase
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s0)
        s2 = re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1)

        # Handle other separators like hyphens
        s3 = re.sub(r"[^a-zA-Z0-9_]", "_", s2)

        s3 = TextCaseConverter._remove_agent_suffix(s3)

        return s3.lower()

    @staticmethod
    def is_valid_python_identifier(text: str) -> Tuple[bool, Optional[str]]:
        """
        Check if a string is a valid Python identifier.
        
        Args:
            text: The string to check
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not text:
            return False, "Identifier cannot be empty"
            
        # Check if it's a valid identifier
        if not text.isidentifier():
            if text[0].isdigit():
                return False, "Identifier cannot start with a digit"
            else:
                return False, "Identifier contains invalid characters"
                
        # Check if it's a reserved keyword
        if keyword.iskeyword(text):
            return False, f"'{text}' is a Python reserved keyword"
            
        # Check if it's a built-in name
        builtins = [
            "abs", "all", "any", "ascii", "bin", "bool", "breakpoint", "bytearray",
            "bytes", "callable", "chr", "classmethod", "compile", "complex", "delattr",
            "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter", "float",
            "format", "frozenset", "getattr", "globals", "hasattr", "hash", "help",
            "hex", "id", "input", "int", "isinstance", "issubclass", "iter", "len",
            "list", "locals", "map", "max", "memoryview", "min", "next", "object",
            "oct", "open", "ord", "pow", "print", "property", "range", "repr",
            "reversed", "round", "set", "setattr", "slice", "sorted", "staticmethod",
            "str", "sum", "super", "tuple", "type", "vars", "zip", "__import__"
        ]
        
        if text in builtins:
            return False, f"'{text}' is a Python built-in function and should be avoided"
            
        return True, None
    
    @staticmethod
    def safe_pascal_case(text: str) -> Tuple[str, bool, Optional[str]]:
        """
        Convert a string to PascalCase, ensuring it's a valid Python class name.
        
        Args:
            text: The string to convert
            
        Returns:
            Tuple of (converted_text, was_modified, modification_message)
        """
        if not text:
            return "Class", True, "Empty string converted to 'Class'"
            
        original = text
        
        # First convert to snake_case to normalize
        snake = TextCaseConverter.snake_case(text)
        
        # Split by underscores and capitalize each word
        words = snake.split("_")
        words = [w.capitalize() for w in words if w]
        
        # Join words
        result = "".join(words)
        
        # Ensure it starts with a letter
        if not result or not result[0].isalpha():
            result = "C" + result
            
        # Check if it's a reserved keyword
        if keyword.iskeyword(result):
            result = result + "Class"
            
        was_modified = original != result
        modification_message = None
        
        if was_modified:
            modification_message = "Modified to ensure valid Python class name"
            
        return result, was_modified, modification_message
    
    @staticmethod
    def pascal_case(text: str) -> str:
        """
        Convert a string to PascalCase.

        Examples:
        - 'user_profile' -> 'UserProfile'
        - 'course_selector' -> 'CourseSelector'
        - 'Course Selector' -> 'CourseSelector'
        """
        if not text:
            return text

        # Use the safe version but discard the additional information
        result, _, _ = TextCaseConverter.safe_pascal_case(text)
        return result

    @staticmethod
    def camel_case(text: str) -> str:
        """
        Convert a string to camelCase.

        Examples:
        - 'user_profile' -> 'userProfile'
        - 'course_selector' -> 'courseSelector'
        - 'CourseSelector' -> 'courseSelector'
        """
        if not text:
            return text

        # Get the PascalCase version
        pascal = TextCaseConverter.pascal_case(text)

        # Make the first character lowercase
        if pascal:
            return pascal[0].lower() + pascal[1:]
        return pascal

    @staticmethod
    def title_case(text: str) -> str:
        """
        Convert a string to Title Case, handling different input formats.

        Examples:
        - 'course_selector' -> 'Course Selector'
        - 'userProfile' -> 'User Profile'
        - 'course-selector' -> 'Course Selector'
        """
        if not text:
            return text

        # First, convert to snake_case to normalize
        snake = TextCaseConverter.snake_case(text)

        # Replace underscores with spaces and capitalize each word
        words = snake.split("_")
        words = [w.capitalize() for w in words if w]

        return " ".join(words)
