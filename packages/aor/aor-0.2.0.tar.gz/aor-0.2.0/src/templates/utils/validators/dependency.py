"""
Dependency validation for template components.
"""

import re
from typing import List, Dict, Any, Set, Optional
from packaging import version


class DependencyValidator:
    """
    Validates and manages dependencies for template components.
    """

    def validate_dependencies(self, dependencies: List[str]) -> Dict[str, Any]:
        """
        Validate a list of dependencies.

        Args:
            dependencies: List of dependency strings (e.g., ["package>=1.0.0", "other-package"])

        Returns:
            Validation result with details
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "parsed_dependencies": {},
        }

        for dep in dependencies:
            parsed = self._parse_dependency(dep)

            if not parsed:
                result["valid"] = False
                result["errors"].append(f"Invalid dependency format: {dep}")
                continue

            # Check for version conflicts
            package_name = parsed["name"]
            if package_name in result["parsed_dependencies"]:
                existing = result["parsed_dependencies"][package_name]
                if not self._are_versions_compatible(existing, parsed):
                    result["valid"] = False
                    result["errors"].append(
                        f"Version conflict for {package_name}: {existing['original']} vs {parsed['original']}"
                    )
            else:
                result["parsed_dependencies"][package_name] = parsed

        return result

    def check_dependency_conflicts(
        self, component_dependencies: Dict[str, List[str]]
    ) -> Dict[str, Any]:
        """
        Check for conflicts between dependencies from different components.

        Args:
            component_dependencies: Map of component paths to their dependencies

        Returns:
            Conflict analysis result
        """
        result = {
            "has_conflicts": False,
            "conflicts": [],
            "warnings": [],
            "combined_dependencies": {},
        }

        # Parse all dependencies
        parsed_deps = {}
        for component, deps in component_dependencies.items():
            parsed_deps[component] = []
            for dep in deps:
                parsed = self._parse_dependency(dep)
                if parsed:
                    parsed_deps[component].append(parsed)

        # Check for conflicts
        package_versions = {}
        for component, deps in parsed_deps.items():
            for dep in deps:
                package_name = dep["name"]

                if package_name not in package_versions:
                    package_versions[package_name] = []

                package_versions[package_name].append(
                    {"component": component, "version": dep}
                )

        # Analyze conflicts
        for package_name, versions in package_versions.items():
            if len(versions) > 1:
                # Check if versions are compatible
                if not self._check_version_compatibility(versions):
                    result["has_conflicts"] = True
                    result["conflicts"].append(
                        {
                            "package": package_name,
                            "components": [v["component"] for v in versions],
                            "versions": [v["version"]["original"] for v in versions],
                        }
                    )
                else:
                    # Get the most restrictive version
                    most_restrictive = self._get_most_restrictive_version(versions)
                    result["combined_dependencies"][package_name] = most_restrictive

        return result

    def _parse_dependency(self, dep: str) -> Optional[Dict[str, Any]]:
        """Parse a dependency string into its components."""
        # Pattern for package name and version specifier
        pattern = r"^([a-zA-Z0-9\-_\.]+)(?:(>=|<=|==|>|<|~=|!=)([0-9\.\*]+))?$"
        match = re.match(pattern, dep.strip())

        if not match:
            return None

        package_name, operator, version_str = match.groups()

        return {
            "name": package_name,
            "operator": operator,
            "version": version_str,
            "original": dep.strip(),
        }

    def _are_versions_compatible(
        self, dep1: Dict[str, Any], dep2: Dict[str, Any]
    ) -> bool:
        """Check if two dependency specifications are compatible."""
        if not dep1["operator"] or not dep2["operator"]:
            return True  # One has no version constraint

        # For simplicity, we'll just check if they're exactly the same
        # In a real implementation, you'd want more sophisticated version compatibility checking
        return (
            dep1["operator"] == dep2["operator"] and dep1["version"] == dep2["version"]
        )

    def _check_version_compatibility(self, versions: List[Dict[str, Any]]) -> bool:
        """Check if a list of version specifications are compatible."""
        # This is a simplified check
        # In reality, you'd want to use a proper version constraint solver
        operators = set()
        version_strs = set()

        for v in versions:
            if v["version"]["operator"]:
                operators.add(v["version"]["operator"])
                version_strs.add(v["version"]["version"])

        # If all have the same operator and version, they're compatible
        if len(operators) <= 1 and len(version_strs) <= 1:
            return True

        # For now, we'll say they're incompatible if they're different
        return False

    def _get_most_restrictive_version(self, versions: List[Dict[str, Any]]) -> str:
        """Get the most restrictive version from a list of compatible versions."""
        # This is a simplified implementation
        # In reality, you'd want to properly calculate the intersection of version constraints

        # For now, just return the first one with a version constraint
        for v in versions:
            if v["version"]["operator"]:
                return v["version"]["original"]

        # If none have version constraints, return the first one
        return versions[0]["version"]["original"]
