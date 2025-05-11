"""
Condition evaluation for template file inclusion.
"""

from typing import Dict, Any, Optional


class FileConditionEvaluator:
    """
    Evaluates conditions for file inclusion in templates.

    This class provides functionality to determine whether specific files
    from templates should be included based on conditions specified in
    the template metadata.
    """

    def evaluate(self, condition: Optional[str], context: Dict[str, Any]) -> bool:
        """
        Evaluate a condition for file inclusion.

        Args:
            condition: Condition string from metadata
            context: Context dictionary with evaluation variables

        Returns:
            True if condition is met or no condition specified, False otherwise
        """
        if not condition:
            return True

        # Template type condition
        if "templateType ==" in condition:
            expected_type = condition.split("==")[1].strip().strip("\"'")
            return context.get("template_type", "") == expected_type

        # Existence condition
        if "exists" in condition:
            var_name = (
                condition.split("exists")[1].strip().strip("(").strip(")").strip()
            )
            return var_name in context and context[var_name] is not None

        # Negation condition
        if condition.startswith("not "):
            negated_condition = condition[4:]  # Remove "not " prefix
            return not self.evaluate(negated_condition, context)

        # Default to True for unknown conditions
        return True
