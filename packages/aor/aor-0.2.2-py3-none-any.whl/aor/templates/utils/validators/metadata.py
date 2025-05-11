"""
Metadata validation for template components.
"""
from typing import Dict, Any, List, Optional, Set


class MetadataValidator:
    """
    Validates metadata for template components using unified format.
    """
    
    def __init__(self, ui=None):
        """
        Initialize the metadata validator.
        
        Args:
            ui: Optional UI instance for displaying messages
        """
        self.ui = ui
    
    # Required fields for all components
    REQUIRED_FIELDS = [
        "componentType", 
        "displayName", 
        "description",
        "version",
        "files"
    ]
    
    # Valid component types
    VALID_COMPONENT_TYPES = [
        "core",
        "protocol",
        # "framework",  # Framework functionality is disabled
        "deployment",
        "utility",
    ]
    
    # Valid values for certain fields
    VALID_AGENT_TYPES = ["langgraph", "langchain", "pydantic"]
    VALID_PROTOCOLS = ["a2a", "raw", "custom"]
    # Framework functionality is disabled
    # VALID_FRAMEWORKS = ["fastapi", "flask", "aiohttp"]
    VALID_DEPLOYMENTS = ["aws-lambda", "ec2", "docker", "kubernetes", "local"]
    
    def validate(self, metadata: Dict[str, Any]) -> bool:
        """
        Validate metadata for a component.
        
        Args:
            metadata: Component metadata to validate
        
        Returns:
            True if valid, False otherwise
        """
        if self.ui:
            self.ui.debug(f"Validating metadata: {metadata}")
        
        if not metadata:
            if self.ui:
                self.ui.error("Empty metadata provided")
            return False
        
        # Check required fields
        missing_fields = []
        for field in self.REQUIRED_FIELDS:
            if field not in metadata:
                missing_fields.append(field)
        
        if missing_fields:
            if self.ui:
                self.ui.error(f"Missing required fields: {', '.join(missing_fields)}")
                self.ui.error(f"in metadata for component")
            return False
        
        # Check component type
        component_type = metadata.get("componentType")
        if component_type not in self.VALID_COMPONENT_TYPES:
            if self.ui:
                self.ui.error(f"Invalid componentType: {component_type}")
            return False
        
        if self.ui:
            self.ui.debug(f"Component type: {component_type}")
        
        # Validate files section
        if not self._validate_files(metadata.get("files", [])):
            if self.ui:
                self.ui.error("Files validation failed")
            return False
        
        # Validate parameters if present
        if "parameters" in metadata:
            if not self._validate_parameters(metadata["parameters"]):
                if self.ui:
                    self.ui.error("Parameters validation failed")
                return False
        
        # Validate compatibility if present
        if "compatibleWith" in metadata:
            if not self._validate_compatibility(metadata["compatibleWith"]):
                if self.ui:
                    self.ui.error("Compatibility validation failed")
                return False
        
        if self.ui:
            self.ui.debug("Metadata validation successful")
        return True
    
    def validate_comprehensive(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive validation with detailed results.
        
        Args:
            metadata: Component metadata to validate
        
        Returns:
            Validation result with details
        """
        if self.ui:
            self.ui.debug(f"Comprehensive validation for metadata: {metadata}")
        
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        if not metadata:
            result["valid"] = False
            result["errors"].append("Empty metadata")
            return result
        
        # Check component type
        component_type = metadata.get("componentType")
        if not component_type:
            result["valid"] = False
            result["errors"].append("Missing componentType")
            return result
        
        if component_type not in self.VALID_COMPONENT_TYPES:
            result["valid"] = False
            result["errors"].append(f"Invalid componentType: {component_type}")
            return result
        
        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field not in metadata:
                result["valid"] = False
                result["errors"].append(f"Missing required field: {field}")
        
        # Validate specific fields based on component type
        if component_type == "core":
            self._validate_core_metadata_comprehensive(metadata, result)
        elif component_type == "protocol":
            self._validate_protocol_metadata_comprehensive(metadata, result)
        # Framework functionality is disabled
        # elif component_type == "framework":
        #     self._validate_framework_metadata_comprehensive(metadata, result)
        elif component_type == "deployment":
            self._validate_deployment_metadata_comprehensive(metadata, result)
        
        # Validate common fields
        self._validate_common_fields(metadata, result)
        
        if self.ui:
            self.ui.debug(f"Comprehensive validation result: {result}")
        
        return result
    
    def _validate_files(self, files: List[Dict[str, Any]]) -> bool:
        """Validate files section of metadata."""
        if self.ui:
            self.ui.debug(f"Validating files: {files}")
        
        if not isinstance(files, list):
            if self.ui:
                self.ui.error("files must be a list")
            return False
        
        for i, file_info in enumerate(files):
            if not isinstance(file_info, dict):
                if self.ui:
                    self.ui.error(f"files[{i}] must be a dictionary")
                return False
            
            if "source" not in file_info or "destination" not in file_info:
                if self.ui:
                    self.ui.error(f"files[{i}] missing source or destination")
                return False
        
        if self.ui:
            self.ui.debug("Files validation successful")
        return True
    
    def _validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate parameters section."""
        if self.ui:
            self.ui.debug(f"Validating parameters: {parameters}")
        
        if not isinstance(parameters, dict):
            if self.ui:
                self.ui.error("parameters must be a dictionary")
            return False
        
        for name, param in parameters.items():
            if not isinstance(param, dict):
                if self.ui:
                    self.ui.error(f"parameter '{name}' must be a dictionary")
                return False
            
            if "description" not in param:
                if self.ui:
                    self.ui.error(f"parameter '{name}' missing description")
                return False
        
        if self.ui:
            self.ui.debug("Parameters validation successful")
        return True
    
    def _validate_compatibility(self, compatibility: Dict[str, Any]) -> bool:
        """Validate compatibility section."""
        if self.ui:
            self.ui.debug(f"Validating compatibility: {compatibility}")
        
        if not isinstance(compatibility, dict):
            if self.ui:
                self.ui.error("compatibleWith must be a dictionary")
            return False
        
        for key, values in compatibility.items():
            if not isinstance(values, list):
                if self.ui:
                    self.ui.error(f"compatibleWith.{key} must be a list")
                return False
        
        if self.ui:
            self.ui.debug("Compatibility validation successful")
        return True
    
    def _validate_core_metadata_comprehensive(self, metadata: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Comprehensive validation for core metadata."""
        agent_type = metadata.get("agentType")
        if agent_type and agent_type not in self.VALID_AGENT_TYPES:
            result["errors"].append(f"Invalid agentType: {agent_type}")
            result["valid"] = False
        
        compatible_with = metadata.get("compatibleWith", {})
        if not isinstance(compatible_with, dict):
            result["errors"].append("compatibleWith must be a dictionary")
            result["valid"] = False
        else:
            # Validate compatibility lists
            for key, values in compatible_with.items():
                if not isinstance(values, list):
                    result["errors"].append(f"compatibleWith.{key} must be a list")
                    result["valid"] = False
    
    def _validate_protocol_metadata_comprehensive(self, metadata: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Comprehensive validation for protocol metadata."""
        protocol_name = metadata.get("protocolName")
        if protocol_name and protocol_name not in self.VALID_PROTOCOLS:
            result["warnings"].append(f"Unknown protocolName: {protocol_name}")
    
    # Framework functionality is disabled
    # def _validate_framework_metadata_comprehensive(self, metadata: Dict[str, Any], result: Dict[str, Any]) -> None:
    #     """Comprehensive validation for framework metadata."""
    #     framework_name = metadata.get("frameworkName")
    #     if framework_name and framework_name not in self.VALID_FRAMEWORKS:
    #         result["warnings"].append(f"Unknown frameworkName: {framework_name}")
    
    def _validate_deployment_metadata_comprehensive(self, metadata: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Comprehensive validation for deployment metadata."""
        deployment_name = metadata.get("deploymentName")
        if deployment_name and deployment_name not in self.VALID_DEPLOYMENTS:
            result["warnings"].append(f"Unknown deploymentName: {deployment_name}")
    
    def _validate_common_fields(self, metadata: Dict[str, Any], result: Dict[str, Any]) -> None:
        """Validate common fields across all component types."""
        # Validate version format
        version = metadata.get("version")
        if version and not self._is_valid_version(version):
            result["warnings"].append(f"Invalid version format: {version}")
        
        # Validate dependencies
        dependencies = metadata.get("dependencies", [])
        if not isinstance(dependencies, list):
            result["errors"].append("dependencies must be a list")
            result["valid"] = False
        
        # Validate files
        files = metadata.get("files", [])
        if not isinstance(files, list):
            result["errors"].append("files must be a list")
            result["valid"] = False
        else:
            for i, file_info in enumerate(files):
                if not isinstance(file_info, dict):
                    result["errors"].append(f"files[{i}] must be a dictionary")
                    result["valid"] = False
                elif "source" not in file_info or "destination" not in file_info:
                    result["errors"].append(f"files[{i}] missing source or destination")
                    result["valid"] = False
    
    def _is_valid_version(self, version: str) -> bool:
        """Check if version format is valid (simple check)."""
        import re
        valid = bool(re.match(r'^\d+\.\d+\.\d+$', version))
        if self.ui:
            self.ui.debug(f"Version '{version}' valid: {valid}")
        return valid