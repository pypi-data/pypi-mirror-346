"""
AWS SAM deployment client.
"""

import logging
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

from aor.deployment.base import DeploymentClient
from aor.deployment.models import DeploymentOptions, DeploymentResult, DeploymentStatus
from aor.deployment.exceptions import DeploymentError, ValidationError
from aor.deployment.utils.command import run_command, CommandResult


logger = logging.getLogger(__name__)


class SAMClient(DeploymentClient):
    """Client for AWS SAM deployments."""

    def __init__(self, profile: Optional[str] = None, region: Optional[str] = None):
        """
        Initialize the SAM client.

        Args:
            profile: Optional AWS profile name
            region: Optional AWS region
        """
        self.profile = profile
        self.region = region

    def validate_connection(self) -> bool:
        """Verify SAM CLI is installed and accessible."""
        try:
            if os.name == "nt":
                result = run_command("sam --version", shell=True)
            else:
                result = run_command(["sam", "--version"])

            return result.success
        except Exception as e:
            logger.error(f"SAM CLI validation error: {str(e)}")
            return False

    def deploy(
        self, package_path: Path, options: DeploymentOptions
    ) -> DeploymentResult:
        """
        Deploy a package using SAM CLI.

        Args:
            package_path: Path to the deployment package
            options: Deployment options

        Returns:
            Deployment result
        """
        # Initialize result
        result = DeploymentResult(
            status=DeploymentStatus.IN_PROGRESS, start_time=datetime.now()
        )

        # Validate package path
        if not package_path.exists():
            result.status = DeploymentStatus.FAILED
            result.error = f"Package path {package_path} does not exist"
            result.end_time = datetime.now()
            return result

        try:
            # Build first
            build_result = self._build_package(package_path, options)
            if not build_result.success:
                result.status = DeploymentStatus.FAILED
                result.error = f"SAM build failed: {build_result.stderr}"
                result.logs.append(f"Build command: {build_result.command}")
                result.logs.append(f"Build stdout: {build_result.stdout}")
                result.logs.append(f"Build stderr: {build_result.stderr}")
                result.end_time = datetime.now()
                return result

            # Then deploy
            result.logs.append(f"Build successful: {build_result.command}")
            deploy_result = self._deploy_package(package_path, options)

            # Check if this is a "no changes to deploy" case with update_only flag
            no_changes_message_in_stderr = (
                "No changes to deploy. Stack" in deploy_result.stderr
            )
            no_changes_message_in_stdout = (
                "No changes to deploy" in deploy_result.stdout
            )
            file_exists_message = (
                "File with same data already exists" in deploy_result.stderr
            )
            update_only_enabled = (
                hasattr(options, "update_only") and options.update_only
            )

            # Determine if this is a "no changes" scenario
            is_no_changes_case = update_only_enabled and (
                no_changes_message_in_stderr
                or no_changes_message_in_stdout
                or file_exists_message
            )

            if deploy_result.success or is_no_changes_case:
                result.status = DeploymentStatus.SUCCESSFUL
                result.logs.append(f"Deploy command: {deploy_result.command}")
                result.logs.append(f"Deploy stdout: {deploy_result.stdout}")

                if is_no_changes_case:
                    # This is a successful case with no changes when update_only is enabled
                    result.logs.append(f"No changes detected, stack is up to date")

                    # Get existing stack information to populate the result
                    from aor.deployment.utils.config import format_agent_name_for_cloud
                    stack_name = (
                        f"{format_agent_name_for_cloud(options.name, for_cloudformation=True)}-{options.environment}"
                    )
                    result.stack_name = stack_name
                    result.deployment_id = stack_name

                    # Try to get existing stack outputs
                    try:
                        cf_outputs = self._get_stack_outputs(stack_name)
                        if cf_outputs:
                            result.resources = cf_outputs
                            if cf_outputs.get("FunctionUrl"):
                                result.url = cf_outputs["FunctionUrl"]
                    except Exception as e:
                        # If we can't get outputs, just continue without them
                        result.logs.append(
                            f"Could not retrieve existing stack outputs: {str(e)}"
                        )
                else:
                    # Parse CloudFormation outputs for normal successful deployment
                    cf_outputs = self._parse_outputs(deploy_result.stdout)
                    if cf_outputs.get("FunctionUrl"):
                        result.url = cf_outputs["FunctionUrl"]

                    # Use the stack name provided in options
                    # This ensures we're updating the same stack each time
                    from aor.deployment.utils.config import format_agent_name_for_cloud
                    stack_name = (
                        f"{format_agent_name_for_cloud(options.name, for_cloudformation=True)}-{options.environment}"
                    )
                    result.stack_name = stack_name
                    result.deployment_id = stack_name

                    # Add resources to result
                    result.resources = cf_outputs
            else:
                result.status = DeploymentStatus.FAILED
                result.error = f"SAM deploy failed: {deploy_result.stderr}"
                result.logs.append(f"Deploy command: {deploy_result.command}")
                result.logs.append(f"Deploy stdout: {deploy_result.stdout}")
                result.logs.append(f"Deploy stderr: {deploy_result.stderr}")

            result.end_time = datetime.now()
            return result

        except Exception as e:
            logger.error(f"SAM deployment error: {str(e)}")
            result.status = DeploymentStatus.FAILED
            result.error = str(e)
            result.end_time = datetime.now()
            return result

    def get_deployment_status(self, deployment_id: str) -> DeploymentStatus:
        """
        Get the status of a CloudFormation stack.

        Args:
            deployment_id: CloudFormation stack name

        Returns:
            Current deployment status
        """
        cmd = [
            "aws",
            "cloudformation",
            "describe-stacks",
            "--stack-name",
            deployment_id,
            "--query",
            "Stacks[0].StackStatus",
            "--output",
            "text",
        ]

        if self.profile:
            cmd.extend(["--profile", self.profile])

        if self.region:
            cmd.extend(["--region", self.region])

        try:
            result = run_command(cmd)
            if not result.success:
                return DeploymentStatus.UNKNOWN

            status = result.stdout.strip()

            # Map CloudFormation status to DeploymentStatus
            status_map = {
                "CREATE_IN_PROGRESS": DeploymentStatus.IN_PROGRESS,
                "CREATE_COMPLETE": DeploymentStatus.SUCCESSFUL,
                "CREATE_FAILED": DeploymentStatus.FAILED,
                "DELETE_IN_PROGRESS": DeploymentStatus.IN_PROGRESS,
                "DELETE_COMPLETE": DeploymentStatus.SUCCESSFUL,
                "DELETE_FAILED": DeploymentStatus.FAILED,
                "UPDATE_IN_PROGRESS": DeploymentStatus.IN_PROGRESS,
                "UPDATE_COMPLETE": DeploymentStatus.SUCCESSFUL,
                "UPDATE_FAILED": DeploymentStatus.FAILED,
                "ROLLBACK_IN_PROGRESS": DeploymentStatus.ROLLBACK_IN_PROGRESS,
                "ROLLBACK_COMPLETE": DeploymentStatus.ROLLBACK_COMPLETE,
            }

            return status_map.get(status, DeploymentStatus.UNKNOWN)
        except Exception as e:
            logger.error(f"Error getting deployment status: {str(e)}")
            return DeploymentStatus.UNKNOWN

    def remove_deployment(self, deployment_id: str) -> bool:
        """
        Remove a deployment (CloudFormation stack).

        Args:
            deployment_id: CloudFormation stack name

        Returns:
            True if removal was successful
        """
        cmd = ["aws", "cloudformation", "delete-stack", "--stack-name", deployment_id]

        if self.profile:
            cmd.extend(["--profile", self.profile])

        if self.region:
            cmd.extend(["--region", self.region])

        try:
            result = run_command(cmd)
            if not result.success:
                logger.error(f"Failed to delete stack: {result.stderr}")
                return False

            # Wait for deletion to complete
            wait_cmd = [
                "aws",
                "cloudformation",
                "wait",
                "stack-delete-complete",
                "--stack-name",
                deployment_id,
            ]

            if self.profile:
                wait_cmd.extend(["--profile", self.profile])

            if self.region:
                wait_cmd.extend(["--region", self.region])

            wait_result = run_command(wait_cmd)
            return wait_result.success
        except Exception as e:
            logger.error(f"Error removing deployment: {str(e)}")
            return False

    def list_deployments(
        self, filter_options: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        List CloudFormation stacks with optional filtering.

        Args:
            filter_options: Options to filter deployments

        Returns:
            List of deployment information
        """
        cmd = [
            "aws",
            "cloudformation",
            "list-stacks",
            "--query",
            "StackSummaries[*].{StackName:StackName,StackStatus:StackStatus,CreationTime:CreationTime}",
            "--output",
            "json",
        ]

        if self.profile:
            cmd.extend(["--profile", self.profile])

        if self.region:
            cmd.extend(["--region", self.region])

        if filter_options and filter_options.get("status"):
            cmd.extend(["--stack-status-filter", filter_options["status"]])

        try:
            result = run_command(cmd)
            if not result.success:
                logger.error(f"Failed to list deployments: {result.stderr}")
                return []

            import json

            deployments = json.loads(result.stdout)

            # Apply client-side filtering
            if filter_options and filter_options.get("name_prefix"):
                prefix = filter_options["name_prefix"]
                deployments = [
                    d for d in deployments if d["StackName"].startswith(prefix)
                ]

            return deployments
        except Exception as e:
            logger.error(f"Error listing deployments: {str(e)}")
            return []

    def get_logs(
        self,
        deployment_id: str,
        start_time: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[str]:
        """
        Get logs for a deployment using SAM CLI.

        Args:
            deployment_id: Stack name
            start_time: Optional start time for logs
            limit: Optional maximum number of log entries

        Returns:
            List of log entries
        """
        cmd = ["sam", "logs", "--stack-name", deployment_id, "--include-traces"]

        if self.profile:
            cmd.extend(["--profile", self.profile])

        if self.region:
            cmd.extend(["--region", self.region])

        if start_time:
            cmd.extend(["--start-time", start_time])

        if limit:
            cmd.extend(["--limit", str(limit)])

        try:
            result = run_command(cmd)
            if not result.success:
                logger.error(f"Failed to get logs: {result.stderr}")
                return [f"Error getting logs: {result.stderr}"]

            # Split log entries
            return result.stdout.strip().split("\n")
        except Exception as e:
            logger.error(f"Error getting logs: {str(e)}")
            return [f"Error retrieving logs: {str(e)}"]

    def _build_package(
        self, package_path: Path, options: DeploymentOptions
    ) -> CommandResult:
        """Run SAM build command."""
        cmd = ["sam", "build"]

        if self.profile:
            cmd.extend(["--profile", self.profile])

        # Memory parameter for building
        if options.resources and options.resources.memory_mb:
            cmd.extend(["--build-memory", str(options.resources.memory_mb)])

        # Run command
        if os.name == "nt":
            cmd_str = " ".join(cmd)
            return run_command(cmd_str, shell=True, cwd=str(package_path))
        else:
            return run_command(cmd, cwd=str(package_path))

    def _deploy_package(
        self, package_path: Path, options: DeploymentOptions
    ) -> CommandResult:
        """Run SAM deploy command."""
        # Safe stack name using proper formatting for CloudFormation compatibility
        from aor.deployment.utils.config import format_agent_name_for_cloud
        stack_name = f"{format_agent_name_for_cloud(options.name, for_cloudformation=True)}-{options.environment}"

        # Check if stack exists
        stack_exists = self._check_stack_exists(stack_name)
        
        # Check if stack is in UPDATE_ROLLBACK_FAILED state
        if stack_exists:
            stack_status = self._get_stack_status(stack_name)
            if stack_status == "UPDATE_ROLLBACK_FAILED":
                logger.warning(f"Stack {stack_name} is in UPDATE_ROLLBACK_FAILED state")
                
                # Try to recover the stack if recover_failed is enabled
                if options.recover_failed:
                    logger.info(f"Attempting to recover stack {stack_name} from UPDATE_ROLLBACK_FAILED state")
                    recovery_success = self._recover_failed_stack(stack_name)
                    
                    if recovery_success:
                        # If recovery was successful, check the current stack status
                        stack_status = self._get_stack_status(stack_name)
                        logger.info(f"Stack recovery completed. Current status: {stack_status}")
                        
                        # If the stack is still not in a stable state, return error
                        if stack_status not in ["UPDATE_ROLLBACK_COMPLETE", "CREATE_COMPLETE", "UPDATE_COMPLETE"]:
                            return CommandResult(
                                returncode=1,
                                command="sam deploy",
                                stdout="",
                                stderr=f"Stack {stack_name} was recovered but is in {stack_status} state. Use --recreate flag to delete and recreate the stack.",
                                duration=0.0
                            )
                    else:
                        # If recovery fails and recreate is enabled, delete and recreate
                        if options.recreate:
                            logger.info(f"Stack recovery failed, recreating stack: {stack_name}")
                            self.remove_deployment(stack_name)
                        else:
                            # If we can't recover and recreate is not enabled, return error
                            return CommandResult(
                                returncode=1,
                                command="sam deploy",
                                stdout="",
                                stderr=f"Stack {stack_name} is in UPDATE_ROLLBACK_FAILED state and could not be recovered. Use --recreate flag to delete and recreate the stack.",
                                duration=0.0
                            )
                else:
                    # If recover_failed is not enabled, return error with instructions
                    return CommandResult(
                        returncode=1,
                        command="sam deploy",
                        stdout="",
                        stderr=f"Stack {stack_name} is in UPDATE_ROLLBACK_FAILED state. Use --recover-failed flag to attempt recovery or --recreate flag to delete and recreate the stack.",
                        duration=0.0
                    )

        # If recreate flag is set and stack exists, delete it first
        if options.recreate and stack_exists:
            logger.info(f"Recreate flag set, deleting existing stack: {stack_name}")
            self.remove_deployment(stack_name)

        cmd = [
            "sam",
            "deploy",
            "--stack-name",
            stack_name,
            "--capabilities",
            "CAPABILITY_IAM",
            "--resolve-s3",
        ]

        # Add profile and region if specified
        if self.profile:
            cmd.extend(["--profile", self.profile])

        if self.region or options.region:
            cmd.extend(["--region", options.region or self.region])

        # Add options
        if options.force:
            cmd.append("--force-upload")

        if not options.variables.get("GUIDED", False):
            cmd.append("--no-confirm-changeset")

        # When update_only is set, we want to deploy only if there are changes
        # But we should NOT use --no-execute-changeset as that prevents any updates
        # Instead, we'll use --fail-on-empty-changeset=false to allow the deployment
        # to succeed even if there are no changes
        if hasattr(options, "update_only") and options.update_only:
            cmd.append("--fail-on-empty-changeset=false")

        # Add parameter overrides
        parameters = []
        if options.resources:
            if options.resources.memory_mb:
                parameters.append(f"MemorySize={options.resources.memory_mb}")
            if options.resources.timeout_seconds:
                parameters.append(f"Timeout={options.resources.timeout_seconds}")

        # Add Anthropic API key from environment if available
        anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
        if anthropic_api_key:
            parameters.append(f"AnthropicApiKey={anthropic_api_key}")

        if parameters:
            cmd.extend(["--parameter-overrides", " ".join(parameters)])

        # Run command
        if os.name == "nt":
            cmd_str = " ".join(cmd)
            return run_command(cmd_str, shell=True, cwd=str(package_path))
        else:
            return run_command(cmd, cwd=str(package_path))

    def _parse_outputs(self, output_text: str) -> Dict[str, str]:
        """Parse outputs from SAM deploy output text."""
        import logging
        logger = logging.getLogger("sam_client")
        
        outputs = {}
        logger.debug(f"Parsing outputs from SAM deploy output text")
        logger.debug(f"Output text: {output_text}")

        # Simple regex-free parsing approach
        output_section = False
        for line in output_text.split("\n"):
            line = line.strip()

            if "Outputs" in line and "----------" in line:
                output_section = True
                logger.debug("Found outputs section")
                continue

            if output_section and "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip()
                outputs[key] = value
                logger.debug(f"Found output: {key} = {value}")

        # Also try to parse JSON format if available
        import json
        import re
        try:
            # Look for JSON-like output in the text
            json_match = re.search(r'{\s*"Outputs"\s*:\s*{.*?}}', output_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                logger.debug(f"Found JSON output: {json_str}")
                json_data = json.loads(json_str)
                if "Outputs" in json_data and isinstance(json_data["Outputs"], dict):
                    for key, value_obj in json_data["Outputs"].items():
                        if isinstance(value_obj, dict) and "Value" in value_obj:
                            outputs[key] = value_obj["Value"]
                            logger.debug(f"Found output from JSON: {key} = {value_obj['Value']}")
        except Exception as e:
            logger.debug(f"Error parsing JSON outputs: {str(e)}")

        logger.debug(f"Parsed outputs: {outputs}")
        return outputs

    def _check_stack_exists(self, stack_name: str) -> bool:
        """Check if a CloudFormation stack exists."""
        cmd = ["aws", "cloudformation", "describe-stacks", "--stack-name", stack_name]

        if self.profile:
            cmd.extend(["--profile", self.profile])

        if self.region:
            cmd.extend(["--region", self.region])

        try:
            result = run_command(cmd)
            return result.success
        except Exception as e:
            logger.debug(f"Stack check error (likely doesn't exist): {str(e)}")
            return False
            
    def _get_stack_status(self, stack_name: str) -> str:
        """Get the current status of a CloudFormation stack."""
        cmd = [
            "aws",
            "cloudformation",
            "describe-stacks",
            "--stack-name",
            stack_name,
            "--query",
            "Stacks[0].StackStatus",
            "--output",
            "text"
        ]

        if self.profile:
            cmd.extend(["--profile", self.profile])

        if self.region:
            cmd.extend(["--region", self.region])

        try:
            result = run_command(cmd)
            if not result.success:
                logger.warning(f"Failed to get stack status: {result.stderr}")
                return "UNKNOWN"
            
            return result.stdout.strip()
        except Exception as e:
            logger.warning(f"Error getting stack status: {str(e)}")
            return "UNKNOWN"
            
    def _recover_failed_stack(self, stack_name: str, max_retries: int = 3) -> bool:
        """
        Attempt to recover a stack in UPDATE_ROLLBACK_FAILED state.
        
        This method tries to continue the rollback operation to get the stack
        back to a stable state.
        
        Args:
            stack_name: The name of the stack to recover
            max_retries: Maximum number of retry attempts
            
        Returns:
            True if recovery was successful, False otherwise
        """
        logger.info(f"Attempting to recover stack {stack_name} from UPDATE_ROLLBACK_FAILED state")
        
        # Try multiple times in case of transient issues
        for attempt in range(1, max_retries + 1):
            if attempt > 1:
                logger.info(f"Retry attempt {attempt}/{max_retries} to recover stack {stack_name}")
                # Wait a bit before retrying
                time.sleep(5)
            
            cmd = [
                "aws",
                "cloudformation",
                "continue-update-rollback",
                "--stack-name",
                stack_name
            ]
            
            if self.profile:
                cmd.extend(["--profile", self.profile])
                
            if self.region:
                cmd.extend(["--region", self.region])
                
            try:
                result = run_command(cmd)
                if not result.success:
                    logger.warning(f"Failed to continue update rollback (attempt {attempt}/{max_retries}): {result.stderr}")
                    if attempt == max_retries:
                        return False
                    continue
                    
                # Wait for the rollback to complete
                wait_cmd = [
                    "aws",
                    "cloudformation",
                    "wait",
                    "stack-rollback-complete",
                    "--stack-name",
                    stack_name
                ]
                
                if self.profile:
                    wait_cmd.extend(["--profile", self.profile])
                    
                if self.region:
                    wait_cmd.extend(["--region", self.region])
                    
                logger.info(f"Waiting for rollback to complete for stack {stack_name}...")
                wait_result = run_command(wait_cmd)
                if not wait_result.success:
                    logger.warning(f"Failed to wait for rollback completion (attempt {attempt}/{max_retries}): {wait_result.stderr}")
                    if attempt == max_retries:
                        return False
                    continue
                    
                # Check if the stack is now in a stable state
                status = self._get_stack_status(stack_name)
                if status in ["UPDATE_ROLLBACK_COMPLETE", "CREATE_COMPLETE", "UPDATE_COMPLETE"]:
                    logger.info(f"Successfully recovered stack {stack_name} to {status} state")
                    return True
                else:
                    logger.warning(f"Stack recovery completed but stack is in {status} state (attempt {attempt}/{max_retries})")
                    if attempt == max_retries:
                        return False
                    continue
                    
            except Exception as e:
                logger.warning(f"Error recovering stack (attempt {attempt}/{max_retries}): {str(e)}")
                if attempt == max_retries:
                    return False
                continue
                
        return False

    def _get_stack_outputs(self, stack_name: str) -> Dict[str, str]:
        """Get outputs from an existing CloudFormation stack."""
        cmd = [
            "aws",
            "cloudformation",
            "describe-stacks",
            "--stack-name",
            stack_name,
            "--query",
            "Stacks[0].Outputs",
        ]

        if self.profile:
            cmd.extend(["--profile", self.profile])

        if self.region:
            cmd.extend(["--region", self.region])

        try:
            result = run_command(cmd)
            if not result.success:
                logger.warning(f"Failed to get stack outputs: {result.stderr}")
                return {}

            # Parse the JSON output
            import json

            outputs_list = json.loads(result.stdout)

            # Convert the list of outputs to a dictionary
            outputs = {}
            for output in outputs_list:
                if "OutputKey" in output and "OutputValue" in output:
                    outputs[output["OutputKey"]] = output["OutputValue"]

            return outputs
        except Exception as e:
            logger.warning(f"Error getting stack outputs: {str(e)}")
            return {}
