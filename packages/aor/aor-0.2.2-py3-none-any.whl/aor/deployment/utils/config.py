"""
Configuration management utilities for deployment.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import boto3
from botocore.exceptions import ClientError

from aor.utils.ui import UI
from aor.common.config import Config


def update_agent_config(
    ui: UI, config: Config, agent: Dict[str, Any], result: Any, options: Optional[Any] = None
) -> bool:
    """
    Update agent configuration with deployment info.

    Args:
        ui: UI instance for displaying messages
        config: Configuration object
        agent: Agent configuration dictionary
        result: Deployment result object
        options: Deployment options object (optional)

    Returns:
        True if update was successful, False otherwise
    """
    try:
        # Find the agent in the config
        agent_name = agent["name"]
        agent_config = None

        # Look in endpoints (previously agents)
        for a in config.get("endpoints", []):
            if a["name"] == agent_name:
                agent_config = a
                break

        # If not found in endpoints, try the legacy agents section
        if agent_config is None:
            for a in config.get("agents", []):
                if a["name"] == agent_name:
                    agent_config = a
                    break

        if agent_config is None:
            ui.warning(f"Agent {agent_name} not found in configuration, cannot update")
            return False

        # Check if deployment section exists
        if "deployment" not in agent_config:
            agent_config["deployment"] = {}

        # Get the current URL if it exists (first check at endpoint level, then in deployment for backward compatibility)
        current_url = agent_config.get("url") or agent_config["deployment"].get("url")

        # Get the new URL from the result
        new_url = result.url if hasattr(result, "url") and result.url else None
        ui.debug(f"URL from deployment result: {new_url}")

        # If we don't have a new URL from the result, try to get it from AWS
        if not new_url and hasattr(result, "stack_name") and result.stack_name:
            ui.info(
                f"No URL in result, retrieving from AWS for stack: {result.stack_name}"
            )
            new_url = get_function_url_from_aws(
                result.stack_name,
                result.region if hasattr(result, "region") else None,
                ui,
            )
            if new_url:
                ui.info(f"Retrieved URL from AWS: {new_url}")
            else:
                ui.warning(f"Failed to retrieve URL from AWS for stack: {result.stack_name}")

        # If we have a new URL from the result or AWS, use it
        # If not, keep the existing URL if it exists
        url_to_use = new_url if new_url else current_url

        # Update URL in the agent body (not in deployment section)
        agent_config["url"] = url_to_use

        # Update deployment section (without URL)
        # Determine region - first try options, then extract from URL, then use default
        region = None
        if options and options.region:
            region = options.region
        elif url_to_use and "lambda-url." in url_to_use and ".on.aws" in url_to_use:
            # Extract region from Lambda URL format: https://xxx.lambda-url.{region}.on.aws/
            try:
                region = url_to_use.split("lambda-url.")[1].split(".on.aws")[0]
                ui.debug(f"Extracted region from URL: {region}")
            except Exception as e:
                ui.debug(f"Failed to extract region from URL: {str(e)}")
        
        if not region:
            region = "us-east-1"  # Default to us-east-1 if no region is found
            ui.debug(f"Using default region: {region}")
            
        deployment_info = {
            "type": "aws-lambda",
            "stack_name": result.stack_name,
            "deployment_id": result.deployment_id,
            "stage": options.environment if options else None,
            "region": region,
            "last_deployed": (
                result.end_time.isoformat() if result.end_time else None
            ),
        }
        
        ui.debug(f"Updating deployment section with: {deployment_info}")
        agent_config["deployment"].update(deployment_info)

        # Log URL status
        if url_to_use:
            if new_url:
                ui.info(f"Updated URL for agent {agent_name}: {url_to_use}")
            else:
                ui.debug(f"Preserved existing URL for agent {agent_name}: {url_to_use}")
        else:
            ui.warning(
                f"No URL available for agent {agent_name}. The agent may not be accessible."
            )

        # Save updated config
        config.save()
        ui.debug(f"Updated configuration for agent {agent_name}")
        return True
    except Exception as e:
        ui.error(f"Error updating agent configuration: {str(e)}")
        import traceback

        ui.debug(f"Stack trace: {traceback.format_exc()}")
        return False


def get_deployment_info(config: Config, agent_name: str) -> Optional[Dict[str, Any]]:
    """
    Get deployment information for an agent from the configuration.

    Args:
        config: Configuration object
        agent_name: Name of the agent

    Returns:
        Dictionary with deployment information or None if not found
    """
    # Look in endpoints (previously agents)
    for agent in config.get("endpoints", []):
        if agent["name"] == agent_name and "deployment" in agent:
            return agent["deployment"]

    # If not found in endpoints, try the legacy agents section
    for agent in config.get("agents", []):
        if agent["name"] == agent_name and "deployment" in agent:
            return agent["deployment"]

    return None


def format_agent_name_for_cloud(agent_name: str, for_cloudformation: bool = False) -> str:
    """
    Format agent name to be compatible with cloud service naming conventions.
    
    Args:
        agent_name: Original agent name
        for_cloudformation: If True, ensures compatibility with CloudFormation stack names
                           (replaces spaces with hyphens and removes underscores)
                           If False, preserves underscores for Python module import compatibility

    Returns:
        Formatted agent name
    """
    import re
    
    if for_cloudformation:
        # For CloudFormation, replace spaces with hyphens and underscores with hyphens
        # CloudFormation stack names must match pattern: [-a-zA-Z0-9]*
        formatted_name = agent_name.replace(" ", "-").replace("_", "-")
        
        # Remove any characters that aren't alphanumeric or hyphens
        formatted_name = re.sub(r'[^a-zA-Z0-9\-]', '', formatted_name)
    else:
        # For Python module compatibility, replace spaces with underscores
        formatted_name = agent_name.replace(" ", "_")
        
        # Remove any characters that aren't alphanumeric, underscores, or hyphens
        formatted_name = re.sub(r'[^a-zA-Z0-9\_\-]', '', formatted_name)
    
    # Ensure name doesn't start or end with a hyphen
    formatted_name = formatted_name.strip('-')
    
    # If name is empty after sanitization, use a default
    if not formatted_name:
        formatted_name = "aor-app"
        
    return formatted_name


def get_function_url_from_aws(
    stack_name: str, region: Optional[str] = None, ui: Optional[UI] = None
) -> Optional[str]:
    """
    Get the function URL directly from AWS CloudFormation stack outputs.

    Args:
        stack_name: The name of the CloudFormation stack
        region: AWS region (optional)
        ui: UI instance for displaying messages (optional)

    Returns:
        Function URL if found, None otherwise
    """
    try:
        # Create CloudFormation client
        if region:
            cf_client = boto3.client("cloudformation", region_name=region)
        else:
            cf_client = boto3.client("cloudformation")

        if ui:
            ui.debug(f"Getting stack outputs for: {stack_name}")

        # Get stack outputs
        response = cf_client.describe_stacks(StackName=stack_name)
        outputs = response["Stacks"][0].get("Outputs", [])

        if ui:
            ui.debug(f"Stack outputs: {outputs}")

        # Look for FunctionUrl in outputs
        for output in outputs:
            if output["OutputKey"] == "FunctionUrl":
                url = output["OutputValue"]
                if ui:
                    ui.info(f"Found FunctionUrl in stack outputs: {url}")
                return url

        # Also check for ApiEndpoint if FunctionUrl is not found
        for output in outputs:
            if output["OutputKey"] == "ApiEndpoint":
                url = output["OutputValue"]
                if ui:
                    ui.info(f"Found ApiEndpoint in stack outputs: {url}")
                return url

        if ui:
            ui.warning(f"No FunctionUrl or ApiEndpoint found in stack outputs for {stack_name}")
        return None
    except ClientError as e:
        if ui:
            ui.debug(f"Error retrieving function URL from AWS: {str(e)}")
        return None
    except Exception as e:
        if ui:
            ui.debug(f"Unexpected error retrieving function URL: {str(e)}")
        return None
