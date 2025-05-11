"""
AWS Lambda deployment client.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

import boto3
from botocore.exceptions import ClientError

from aor.deployment.base import DeploymentClient
from aor.deployment.models import DeploymentOptions, DeploymentResult, DeploymentStatus
from aor.deployment.exceptions import (
    DeploymentError,
    ConnectionError,
    ValidationError,
    ResourceNotFoundError,
    PermissionError,
)
from aor.deployment.utils.command import run_command
from aor.deployment.clients.aws.sam_client import SAMClient


logger = logging.getLogger(__name__)


class LambdaClient(DeploymentClient):
    """Client for AWS Lambda deployments."""

    def __init__(self, profile: Optional[str] = None, region: Optional[str] = None):
        """
        Initialize the Lambda client.

        Args:
            profile: Optional AWS profile name
            region: Optional AWS region
        """
        self.profile = profile
        self.region = region
        self._sam_client = SAMClient(profile, region)

        # Initialize boto3 session and clients
        session_kwargs = {}
        if profile:
            session_kwargs["profile_name"] = profile
        if region:
            session_kwargs["region_name"] = region

        self.session = boto3.Session(**session_kwargs)
        self.lambda_client = self.session.client("lambda")
        self.cloudformation = self.session.client("cloudformation")

    def validate_connection(self) -> bool:
        """Verify connectivity and credentials to AWS."""
        try:
            # Test API access to Lambda
            self.lambda_client.list_functions(MaxItems=1)
            return True
        except ClientError as e:
            logger.error(f"AWS connection error: {str(e)}")
            return False

    def deploy(
        self, package_path: Path, options: DeploymentOptions
    ) -> DeploymentResult:
        """
        Deploy a package to AWS Lambda using SAM.

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
            # Get safe stack name using proper formatting for CloudFormation compatibility
            from aor.deployment.utils.config import format_agent_name_for_cloud
            stack_name = f"{format_agent_name_for_cloud(options.name, for_cloudformation=True)}-{options.environment}"
            result.stack_name = stack_name

            # Check if stack exists and delete if needed
            if options.force or (hasattr(options, "recreate") and options.recreate):
                self._delete_stack_if_exists(stack_name)

            # Build and deploy using SAM client
            sam_options = DeploymentOptions(
                name=options.name,
                environment=options.environment,
                region=options.region or self.region,
                profile=options.profile or self.profile,
                resources=options.resources,
                force=options.force,
            )

            sam_result = self._sam_client.deploy(package_path, sam_options)

            # Get function URL if deployment succeeded
            if sam_result.is_successful:
                function_url = self._get_function_url(stack_name)

                # Update result with success information
                result.status = DeploymentStatus.SUCCESSFUL
                result.url = function_url
                result.deployment_id = stack_name
                result.resources = sam_result.resources
                result.logs = sam_result.logs
            else:
                # Update result with failure information
                result.status = DeploymentStatus.FAILED
                result.error = sam_result.error

            result.end_time = datetime.now()
            return result

        except Exception as e:
            logger.error(f"Deployment error: {str(e)}")
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

        try:
            response = self.cloudformation.describe_stacks(StackName=deployment_id)
            cf_status = response["Stacks"][0]["StackStatus"]
            return status_map.get(cf_status, DeploymentStatus.UNKNOWN)
        except ClientError as e:
            logger.error(f"Error getting stack status: {str(e)}")
            return DeploymentStatus.UNKNOWN

    def remove_deployment(self, deployment_id: str) -> bool:
        """
        Remove a deployment (CloudFormation stack).

        Args:
            deployment_id: CloudFormation stack name

        Returns:
            True if removal was successful
        """
        try:
            self.cloudformation.delete_stack(StackName=deployment_id)

            # Wait for stack deletion to complete
            waiter = self.cloudformation.get_waiter("stack_delete_complete")
            waiter.wait(
                StackName=deployment_id, WaiterConfig={"Delay": 5, "MaxAttempts": 30}
            )

            return True
        except ClientError as e:
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
        deployments = []

        try:
            paginator = self.cloudformation.get_paginator("list_stacks")

            for page in paginator.paginate():
                for stack in page["StackSummaries"]:
                    # Skip deleted stacks unless specifically requested
                    if stack[
                        "StackStatus"
                    ] == "DELETE_COMPLETE" and not filter_options.get(
                        "include_deleted"
                    ):
                        continue

                    # Apply filters if provided
                    if filter_options and "name_prefix" in filter_options:
                        if not stack["StackName"].startswith(
                            filter_options["name_prefix"]
                        ):
                            continue

                    deployments.append(
                        {
                            "id": stack["StackId"],
                            "name": stack["StackName"],
                            "status": stack["StackStatus"],
                            "creation_time": stack["CreationTime"],
                            "last_updated": stack.get("LastUpdatedTime"),
                        }
                    )

            return deployments
        except ClientError as e:
            logger.error(f"Error listing deployments: {str(e)}")
            return []

    def get_logs(
        self,
        deployment_id: str,
        start_time: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[str]:
        """
        Get CloudWatch logs for a Lambda function.

        Args:
            deployment_id: Stack name or function name
            start_time: Optional start time for logs
            limit: Optional maximum number of log entries

        Returns:
            List of log entries
        """
        log_entries = []

        try:
            # Get the function name from the stack outputs
            function_name = self._get_function_name_from_stack(deployment_id)
            if not function_name:
                raise ResourceNotFoundError(
                    f"Function not found in stack {deployment_id}"
                )

            logs_client = self.session.client("logs")
            log_group_name = f"/aws/lambda/{function_name}"

            # Get log streams for the function
            response = logs_client.describe_log_streams(
                logGroupName=log_group_name,
                orderBy="LastEventTime",
                descending=True,
                limit=5,  # Get the most recent streams
            )

            # Get events from each stream
            for stream in response["logStreams"]:
                events_params = {
                    "logGroupName": log_group_name,
                    "logStreamName": stream["logStreamName"],
                    "limit": limit or 100,
                    "startFromHead": False,
                }

                if start_time:
                    # Convert to timestamp if provided as string
                    if isinstance(start_time, str):
                        start_dt = datetime.fromisoformat(
                            start_time.replace("Z", "+00:00")
                        )
                        events_params["startTime"] = int(start_dt.timestamp() * 1000)

                events_response = logs_client.get_log_events(**events_params)

                for event in events_response["events"]:
                    log_entries.append(event["message"])

            return log_entries
        except ClientError as e:
            logger.error(f"Error getting logs: {str(e)}")
            return [f"Error retrieving logs: {str(e)}"]

    def _delete_stack_if_exists(self, stack_name: str) -> bool:
        """Delete a CloudFormation stack if it exists."""
        try:
            self.cloudformation.describe_stacks(StackName=stack_name)

            # Stack exists, delete it
            logger.info(f"Deleting existing stack: {stack_name}")
            self.cloudformation.delete_stack(StackName=stack_name)

            # Wait for deletion to complete
            waiter = self.cloudformation.get_waiter("stack_delete_complete")
            waiter.wait(
                StackName=stack_name, WaiterConfig={"Delay": 5, "MaxAttempts": 30}
            )

            return True
        except ClientError as e:
            if "does not exist" in str(e):
                logger.info(f"Stack {stack_name} does not exist, nothing to delete")
                return True
            else:
                logger.warning(f"Error checking/deleting stack: {str(e)}")
                return False

    def _get_function_url(self, stack_name: str) -> Optional[str]:
        """Get function URL from CloudFormation outputs."""
        try:
            response = self.cloudformation.describe_stacks(StackName=stack_name)
            outputs = response["Stacks"][0].get("Outputs", [])

            for output in outputs:
                if output["OutputKey"] == "FunctionUrl":
                    return output["OutputValue"]

            return None
        except ClientError as e:
            logger.warning(f"Error getting function URL: {str(e)}")
            return None

    def _get_function_name_from_stack(self, stack_name: str) -> Optional[str]:
        """Get Lambda function name from CloudFormation stack."""
        try:
            response = self.cloudformation.describe_stacks(StackName=stack_name)
            outputs = response["Stacks"][0].get("Outputs", [])

            for output in outputs:
                if output["OutputKey"] == "FunctionName":
                    return output["OutputValue"]

            # Try to find by resource
            resources = self.cloudformation.list_stack_resources(StackName=stack_name)
            for resource in resources["StackResourceSummaries"]:
                if resource["ResourceType"] == "AWS::Lambda::Function":
                    return resource["PhysicalResourceId"]

            return None
        except ClientError as e:
            logger.warning(f"Error getting function name: {str(e)}")
            return None
