"""
Validation utilities for agent management.

This module provides common validation functions for agent names, input names,
and output names.
"""

import re
import keyword
import uuid
from typing import Tuple, Optional, List, Dict


# List of Python reserved keywords
PYTHON_KEYWORDS = set(keyword.kwlist)

# Add additional reserved names that shouldn't be used
ADDITIONAL_RESERVED = {
    "None", "True", "False", "print", "input", "output", "type", "id", "format",
    "min", "max", "sum", "len", "str", "int", "float", "bool", "list", "dict",
    "set", "tuple", "object", "file", "open", "close", "read", "write", "append",
    "self", "cls", "super", "init", "new", "del", "repr", "str", "bytes",
    "format", "hash", "bool", "dir", "help", "globals", "locals", "vars",
    "getattr", "setattr", "delattr", "hasattr", "isinstance", "issubclass",
    "callable", "classmethod", "staticmethod", "property", "enumerate", "zip",
    "map", "filter", "reduce", "sorted", "reversed", "all", "any", "abs", "round"
}

# Combine all reserved names
RESERVED_NAMES = PYTHON_KEYWORDS.union(ADDITIONAL_RESERVED)


def validate_name(name: str, min_length: int = 3, max_length: int = 50) -> Tuple[bool, Optional[str]]:
    """Validate a name for use as an agent, input, or output name.
    
    Names must:
    - Start with a letter
    - Contain only letters, numbers, underscores, and spaces
    - Be at least min_length characters long (default: 3)
    - Not exceed max_length characters (default: 50)
    - Not be a Python reserved keyword or common built-in name
    
    Args:
        name: The name to validate
        min_length: Minimum length for the name
        max_length: Maximum length for the name
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Check if name is too short
    if len(name) < min_length:
        return False, f"Name must be at least {min_length} characters long"
        
    # Check if name is too long
    if len(name) > max_length:
        return False, f"Name must not exceed {max_length} characters"
        
    # Check if name starts with a letter
    if not name[0].isalpha():
        return False, "Name must start with a letter"
        
    # Check if name contains only valid characters (now including spaces)
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_ ]*$', name):
        return False, "Name must contain only letters, numbers, underscores, and spaces"
    
    # Check if name is a reserved keyword or common built-in name
    if name.lower() in RESERVED_NAMES:
        return False, f"Name '{name}' is a reserved Python keyword or built-in name and cannot be used"
    
    # Skip Python identifier check if name contains spaces
    if ' ' not in name and not name.isidentifier():
        return False, f"Name '{name}' is not a valid Python identifier"
        
    return True, None


def sanitize_name(name: str, prefix: str = "item") -> Tuple[str, bool, Optional[str]]:
    """Sanitize a name for use as an agent, input, or output name.
    
    This function will:
    - Replace spaces and special characters with underscores
    - Ensure the name starts with a letter (adding a prefix if needed)
    - Remove consecutive underscores
    - Remove leading/trailing underscores
    - Ensure the name is not empty (using the provided prefix as default)
    - Check if the name is a reserved keyword and add a trailing underscore if it is
    
    Args:
        name: Original name to sanitize
        prefix: Prefix to use if the name starts with a number or is empty
        
    Returns:
        Tuple of (sanitized_name, was_modified, modification_message)
    """
    original_name = name
    was_modified = False
    modification_message = None
    
    # Replace spaces and special characters with underscores
    sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '_', name)
    
    # Ensure the name doesn't start with a number
    if sanitized_name and sanitized_name[0].isdigit():
        sanitized_name = f"{prefix}_{sanitized_name}"
        was_modified = True
        modification_message = f"Name started with a number, prefixed with '{prefix}_'"
    
    # Remove consecutive underscores
    sanitized_name = re.sub(r'_+', '_', sanitized_name)
    
    # Remove leading/trailing underscores
    sanitized_name = sanitized_name.strip('_')
    
    # Ensure the name is not empty
    if not sanitized_name:
        sanitized_name = prefix
        was_modified = True
        modification_message = f"Name was empty or contained only special characters, using '{prefix}' as default"
    
    # Check if the name is a reserved keyword
    if sanitized_name.lower() in RESERVED_NAMES:
        sanitized_name = f"{sanitized_name}_"
        was_modified = True
        modification_message = f"Name was a reserved keyword, appended underscore"
    
    # Check if the name was modified
    if original_name != sanitized_name and not modification_message:
        was_modified = True
        modification_message = "Name contained invalid characters or format"
    
    return sanitized_name, was_modified, modification_message


def check_for_duplicates(names: List[str]) -> Tuple[bool, Optional[str]]:
    """Check for duplicate names in a list.
    
    Args:
        names: List of names to check
        
    Returns:
        Tuple of (has_duplicates, error_message)
    """
    seen = set()
    duplicates = []
    
    for name in names:
        name_lower = name.lower()  # Case-insensitive comparison
        if name_lower in seen:
            duplicates.append(name)
        else:
            seen.add(name_lower)
    
    if duplicates:
        return True, f"Duplicate names found: {', '.join(duplicates)}"
    
    return False, None


# Dictionary to store generated internal IDs for agents
# This ensures IDs are generated only once per agent name
_AGENT_INTERNAL_IDS: Dict[str, str] = {}


def generate_stable_internal_id(agent_name: str) -> str:
    """Generate a stable internal identifier for an agent.
    
    This function:
    1. Uses the agent_name as the base
    2. If the name contains non-English characters, uses "endpoint" as the base instead
    3. Normalizes the name into lowercase alphanumeric characters (replaces non-alphanumerics with _)
    4. Generates a deterministic hash based on the normalized name
    5. Ensures IDs are generated only once per agent name (case-insensitive)
    
    Args:
        agent_name: The user-provided agent name
        
    Returns:
        A stable internal identifier that won't change even if user-visible configuration changes
    """
    # Normalize the agent name to lowercase for case-insensitive lookup
    normalized_lookup = agent_name.lower()
    
    # Check if we already generated an ID for this agent name (case-insensitive)
    for name, id_value in _AGENT_INTERNAL_IDS.items():
        if name.lower() == normalized_lookup:
            return id_value
    
    # Check if the name contains any non-English characters
    if any(ord(c) > 127 for c in agent_name):
        # Use "endpoint" as the base name if non-English characters are detected
        base_name = "endpoint"
        sanitized_name, _, _ = sanitize_name(base_name)
    else:
        # Replace spaces with underscores before sanitizing
        agent_name_no_spaces = agent_name.replace(" ", "_")
        # Normalize the name (replace special chars with underscore and convert to lowercase)
        sanitized_name, _, _ = sanitize_name(agent_name_no_spaces, prefix="endpoint")
    
    normalized_name = sanitized_name.lower()
    
    # Generate a deterministic hash based on the normalized name
    # Use the first 8 characters of the UUID5 with the normalized name as namespace
    # UUID5 is deterministic based on the input, unlike UUID4 which is random
    import hashlib
    name_hash = hashlib.md5(normalized_name.encode()).hexdigest()[:8]
    
    # Combine the normalized name with the hash
    internal_id = f"{normalized_name}_{name_hash}"
    
    # Store the generated ID to ensure it's used consistently
    _AGENT_INTERNAL_IDS[agent_name] = internal_id
    
    return internal_id