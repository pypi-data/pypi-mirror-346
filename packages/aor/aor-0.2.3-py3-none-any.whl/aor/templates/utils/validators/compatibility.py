"""
Component compatibility validation.
"""

from typing import List, Dict, Any, Optional, Set


class CompatibilityValidator:
    """
    Validates compatibility between different components.
    """

    def validate_components(
        self, metadata_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Validate if the given components are compatible with each other.

        Args:
            metadata_list: List of component metadata with paths

        Returns:
            Validation result with compatibility details
        """
        result = {
            "compatible": True,
            "errors": [],
            "warnings": [],
            "dependencies": self._collect_dependencies(metadata_list),
        }

        # Skip validation if metadata is invalid
        invalid_metadata = [m for m in metadata_list if not m]
        if invalid_metadata:
            result["compatible"] = False
            result["errors"].append("Some components have invalid metadata")
            return result

        # Find core component
        core_component = self._find_component_by_type(metadata_list, "core")
        if not core_component:
            result["compatible"] = False
            result["errors"].append(
                "No core component found. At least one core component is required."
            )
            return result

        # For now, skip strict compatibility checking - just log warnings
        # This allows the system to be more flexible during development
        for metadata in metadata_list:
            if metadata["componentType"] == "core":
                continue

            # Add warnings instead of errors for now
            component_type = metadata["componentType"]
            if component_type == "protocol":
                result["warnings"].append(
                    f"Protocol '{metadata['path']}' compatibility check skipped"
                )
            # Framework functionality is disabled
            # elif component_type == "framework":
            #     result["warnings"].append(
            #         f"Framework '{metadata['path']}' compatibility check skipped"
            #     )
            elif component_type == "deployment":
                result["warnings"].append(
                    f"Deployment '{metadata['path']}' compatibility check skipped"
                )

        # Check dependency requirements - convert to warnings
        dependency_result = self._check_dependency_requirements(metadata_list)
        if not dependency_result["valid"]:
            result["warnings"].extend(dependency_result["errors"])
            # Don't mark as incompatible - let the system try anyway

        # Check for duplicate component types
        duplicate_result = self._check_duplicate_components(metadata_list)
        if duplicate_result["errors"]:
            result["errors"].extend(duplicate_result["errors"])
        if duplicate_result["warnings"]:
            result["warnings"].extend(duplicate_result["warnings"])

        return result

    def _find_component_by_type(
        self, metadata_list: List[Dict[str, Any]], component_type: str
    ) -> Optional[Dict[str, Any]]:
        """Find a component by its type."""
        for metadata in metadata_list:
            if metadata.get("componentType") == component_type:
                return metadata
        return None

    def _check_component_compatibility(
        self,
        component: Dict[str, Any],
        core_component: Dict[str, Any],
        all_components: List[Dict[str, Any]],
    ) -> bool:
        """Check if a component is compatible with the core component."""
        component_type = component["componentType"]

        # Check if core supports this component type
        if component_type == "protocol":
            supported_protocols = core_component.get("compatibleWith", {}).get(
                "protocols", []
            )
            protocol_name = (
                component.get("protocolName") or component["path"].split("/")[-1]
            )
            return protocol_name in supported_protocols

        # Framework functionality is disabled
        # elif component_type == "framework":
        #     supported_frameworks = core_component.get("compatibleWith", {}).get(
        #         "frameworks", []
        #     )
        #     framework_name = (
        #         component.get("frameworkName") or component["path"].split("/")[-1]
        #     )
        #     return framework_name in supported_frameworks

        elif component_type == "deployment":
            supported_deployments = core_component.get("compatibleWith", {}).get(
                "deployments", []
            )
            deployment_name = (
                component.get("deploymentName") or component["path"].split("/")[-1]
            )
            return deployment_name in supported_deployments

        return True

    def _check_dependency_requirements(
        self, metadata_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Check if all component requirements are met."""
        result = {"valid": True, "errors": []}

        # Collect all provided features
        provided_features = set()
        for metadata in metadata_list:
            if "provides" in metadata:
                provided_features.update(metadata["provides"])

        # Check requirements
        for metadata in metadata_list:
            if "requires" in metadata:
                for requirement in metadata["requires"]:
                    if requirement not in provided_features:
                        result["valid"] = False
                        result["errors"].append(
                            f"Component {metadata['path']} requires '{requirement}' which is not provided by any component"
                        )

        return result

    def _check_duplicate_components(
        self, metadata_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Check for duplicate component types."""
        result = {"errors": [], "warnings": []}
        type_counts = {}

        for metadata in metadata_list:
            component_type = metadata["componentType"]
            type_counts[component_type] = type_counts.get(component_type, 0) + 1

        # Check for duplicates
        if type_counts.get("core", 0) > 1:
            result["errors"].append(
                "Multiple core components found. Only one core component is allowed."
            )

        if type_counts.get("protocol", 0) > 1:
            result["warnings"].append(
                "Multiple protocol components found. This may cause conflicts."
            )

        # Framework functionality is disabled
        # if type_counts.get("framework", 0) > 1:
        #     result["warnings"].append(
        #         "Multiple framework components found. This may cause conflicts."
        #     )

        return result

    def _collect_dependencies(
        self, metadata_list: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Collect all dependencies from components."""
        dependencies = {}

        for metadata in metadata_list:
            if "dependencies" in metadata:
                dependencies[metadata["path"]] = metadata["dependencies"]

        return dependencies
