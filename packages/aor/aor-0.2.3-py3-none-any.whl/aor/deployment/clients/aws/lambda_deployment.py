"""
AWS Lambda deployment utilities.
"""

import os
import time
import uuid
import boto3
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

from botocore.exceptions import ClientError
from aor.utils.ui import UI
from aor.common.config import Config
from aor.deployment.base import DeploymentClient
from aor.deployment.models import DeploymentOptions, DeploymentResult, DeploymentStatus
from aor.deployment.exceptions import (
    DeploymentError,
    ClientInitializationError,
    ValidationError,
)
from aor.deployment.utils.config import update_agent_config, format_agent_name_for_cloud
from aor.deployment.utils.file_preparation import prepare_agent_files


def deploy_to_aws_lambda(
    ui: UI,
    config: Config,
    agents: List[Dict[str, Any]],
    options: DeploymentOptions,
    deploy_dir: Path,
) -> Tuple[int, int]:
    """
    Deploy agents to AWS Lambda.

    Args:
        ui: UI instance for displaying messages
        config: Configuration object
        agents: List of agent configurations to deploy
        options: Deployment options
        deploy_dir: Temporary deployment directory

    Returns:
        Tuple of (successful_deployments, failed_deployments)
    """
    ui.section("AWS Lambda Deployment")
    ui.info(f"Preparing to deploy {len(agents)} agent(s) to AWS Lambda")

    try:
        # Initialize deployment client
        ui.info("Initializing AWS Lambda deployment client")
        with ui.console.status("[bold blue]Connecting to AWS...") as status:
            client: DeploymentClient = get_lambda_client(
                profile=options.profile, region=options.region
            )
            status.update("[bold green]Connected to AWS successfully")

        # Validate connection
        with ui.console.status("[bold blue]Validating AWS credentials...") as status:
            if not client.validate_connection():
                ui.error(
                    "Failed to connect to AWS. Please check your credentials and network connection."
                )
                return 0, len(agents)
            status.update("[bold green]AWS credentials validated successfully")

        # Setup progress tracking for deployment
        successful_deployments = 0
        failed_deployments = 0

        # Deploy each agent
        for i, agent in enumerate(agents, 1):
            agent_name = agent["name"]
            ui.section(f"Deploying Agent {i}/{len(agents)}: {agent_name}")

            # Determine folder name using internal_id if available
            if "internal_id" in agent:
                # internal_id is already sanitized, but ensure it's CloudFormation compatible
                folder_name = format_agent_name_for_cloud(agent["internal_id"])
                ui.debug(f"Using internal_id for deployment folder: {agent['internal_id']}")
            else:
                # Fallback to agent name if internal_id is not available
                folder_name = format_agent_name_for_cloud(agent_name)
                ui.debug(f"No internal_id found, using formatted agent name for folder: {folder_name}")

            # Create agent deployment directory
            agent_dir = deploy_dir / folder_name
            agent_dir.mkdir(exist_ok=True)
            ui.debug(f"Created agent deployment directory: {agent_dir}")

            # Copy agent files
            ui.info(f"Preparing files for {agent_name}...")
            agent_path = prepare_agent_files(ui, agent, agent_dir, folder_name)
            if not agent_path:
                ui.error(f"Failed to prepare files for agent: {agent_name}")
                failed_deployments += 1
                continue

            status.update(f"[bold green]Files prepared successfully for {agent_name}")

            # Check if template file exists in expected locations
            template_file = agent_dir / "template.yaml"
            if not template_file.exists():
                template_file = agent_dir / "template.yml"

            ui.debug(f"Looking for template file at: {template_file}")

            if not template_file.exists():
                ui.error(f"Template file not found for agent {agent_name}")
                ui.info("Please ensure deployments/lambda/template.yaml exists")
                failed_deployments += 1
                continue

            ui.debug(f"Found template file: {template_file}")

            # Use internal_id if available, otherwise format agent name for CloudFormation compatibility
            if "internal_id" in agent:
                # internal_id is already sanitized, but ensure it's CloudFormation compatible
                base_name = format_agent_name_for_cloud(agent["internal_id"], for_cloudformation=True)
                ui.debug(f"Using internal_id for stack name: {agent['internal_id']}")
            else:
                # Fallback to agent name if internal_id is not available
                base_name = format_agent_name_for_cloud(agent_name, for_cloudformation=True)
                ui.debug(f"No internal_id found, using formatted agent name: {base_name}")
                
            stack_name = f"{base_name}-{options.environment}"
            ui.info(f"Using CloudFormation stack name: {stack_name}")

            # Set agent-specific options with the correctly formatted name
            agent_options = DeploymentOptions(
                name=base_name,  # Use the base_name (from internal_id or formatted agent name)
                environment=options.environment,
                region=options.region,
                profile=options.profile,
                resources=options.resources,
                force=options.force,
            )

            # Copy additional options
            agent_options.guided = options.guided
            agent_options.update_only = options.update_only
            agent_options.recreate = options.recreate
            agent_options.recover_failed = options.recover_failed
            agent_options.verbose = options.verbose

            try:
                # We already set the stack_name above based on internal_id or formatted agent name
                # No need to redefine it here, just use the existing value
                ui.debug(f"Using consistent stack name: {stack_name}")

                # Set the name in the agent_options to match what we used for the stack name
                agent_options.name = base_name

                # Create a temporary script to run SAM directly for better debugging
                debug_script = deploy_dir / f"debug_deploy_{agent_name}.sh"
                with open(debug_script, "w") as f:
                    f.write("#!/bin/bash\n")
                    f.write(f"cd {agent_dir}\n")
                    f.write("sam validate\n")
                    f.write(
                        f"sam deploy --stack-name {stack_name} --no-confirm-changeset --capabilities CAPABILITY_IAM --fail-on-empty-changeset=false\n"
                    )

                # Make script executable (Linux/Mac only)
                if os.name != "nt":
                    os.chmod(debug_script, 0o755)

                ui.debug(f"Created debug script at {debug_script}")
                ui.debug("You can run this script manually for more detailed debugging")

                # Deploy using client
                ui.info(f"Starting deployment for {agent_name}")
                progress, task_id = ui.start_progress("Deploying to AWS Lambda")

                start_time = time.time()
                result = client.deploy(agent_dir, agent_options)
                elapsed_time = time.time() - start_time

                # Stop the progress display after getting the result
                ui.stop_progress(f"Deployment completed for {agent_name}")

                if result.is_successful:
                    # Check if this was a "no changes" success with update_only flag
                    no_changes_detected = any(
                        "No changes detected, stack is up to date" in log
                        for log in result.logs
                    )

                    if options.update_only and no_changes_detected:
                        ui.success(
                            f"No changes detected for agent: {agent_name} - stack is up to date ({elapsed_time:.1f}s)"
                        )

                        # Still display the function URL if available
                        if result.url:
                            ui.value("Function URL", result.url)
                            ui.command(
                                f"curl -X POST {result.url}/invoke -H 'Content-Type: application/json' -d '{{\"input\":\"Hello from AI-on-Rails\"}}'",
                                "Test the deployed function",
                            )
                    else:
                        ui.success(
                            f"Successfully deployed agent: {agent_name} ({elapsed_time:.1f}s)"
                        )
                        if result.url:
                            ui.value("Function URL", result.url)
                            ui.command(
                                f"curl -X POST {result.url}/invoke -H 'Content-Type: application/json' -d '{{\"input\":\"Hello from AI-on-Rails\"}}'",
                                "Test the deployed function",
                            )

                    # Update agent configuration with deployment info
                    # Always update config if deployment was successful, even if no resources were retrieved
                    ui.info("Updating agent configuration...")
                    # Debug log to help diagnose issues
                    ui.debug(f"Deployment result URL: {result.url}")
                    ui.debug(f"Deployment result resources: {result.resources}")
                    update_agent_config(ui, config, agent, result, agent_options)

                    successful_deployments += 1
                else:
                    ui.error(f"Failed to deploy agent {agent_name}: {result.error}")

                    # Try to get CloudFormation events for more details
                    try:
                        # Create CloudFormation client without status display
                        cf_client = get_cloudformation_client(
                            profile=options.profile,
                            region=options.region or "us-east-1",  # TODO: is it needed?
                        )

                        try:
                            # First check if the stack exists
                            try:
                                cf_client.describe_stacks(StackName=stack_name)
                                # If we get here, the stack exists
                                events = cf_client.describe_stack_events(
                                    StackName=stack_name
                                )
                                ui.section("CloudFormation Errors")
                            except ClientError as stack_error:
                                if "does not exist" in str(stack_error):
                                    ui.warning(
                                        f"Stack '{stack_name}' does not exist yet. No CloudFormation events available."
                                    )
                                    continue
                                else:
                                    # Re-raise if it's a different error
                                    raise stack_error

                            error_rows = []
                            for event in events.get("StackEvents", [])[
                                :10
                            ]:  # Get last 10 events
                                if (
                                    "ResourceStatus" in event
                                    and "ResourceStatusReason" in event
                                ):
                                    status = event["ResourceStatus"]
                                    reason = event.get("ResourceStatusReason", "")
                                    resource = event.get("LogicalResourceId", "")
                                    if "_FAILED" in status:
                                        error_rows.append([resource, status, reason])

                            if error_rows:
                                ui.display_table(
                                    "Failed Resources",
                                    ["Resource", "Status", "Reason"],
                                    error_rows,
                                )
                            else:
                                ui.info(
                                    "No specific error details found in CloudFormation events"
                                )
                        except Exception as e:
                            ui.error(f"Could not get stack events: {str(e)}")
                            if ui.debug:
                                raise e from e
                    except Exception as e:
                        ui.error(f"Error getting CloudFormation events: {str(e)}")
                        if ui.debug:
                            raise e from e

                    ui.info(
                        "For more details, check CloudWatch Logs and CloudFormation console"
                    )
                    failed_deployments += 1
            except Exception as e:
                ui.error(f"Unexpected error: {str(e)}")
                import traceback

                ui.debug(f"Stack trace: {traceback.format_exc()}")
                failed_deployments += 1

        # Summary
        ui.section("Deployment Summary")
        summary_rows = [
            ["Total Agents", len(agents)],
            ["Successfully Deployed", successful_deployments],
            ["Failed", failed_deployments],
        ]
        ui.display_table("Results", ["Metric", "Count"], summary_rows)

        if successful_deployments == len(agents):
            ui.success("All agents were deployed successfully!")
        elif successful_deployments > 0:
            ui.warning(
                f"Deployment partially successful ({successful_deployments}/{len(agents)} agents deployed)"
            )
        else:
            ui.error("Deployment failed for all agents")

        return successful_deployments, failed_deployments

    except ClientInitializationError as e:
        ui.error(f"Failed to initialize deployment client: {str(e)}")
        return 0, len(agents)
    except Exception as e:
        ui.error(f"Unexpected error during deployment: {str(e)}")
        import traceback

        ui.debug(f"Stack trace: {traceback.format_exc()}")
        return 0, len(agents)


def get_lambda_client(
    profile: Optional[str] = None, region: Optional[str] = None
) -> DeploymentClient:
    """
    Get a Lambda deployment client.

    Args:
        profile: AWS profile name
        region: AWS region

    Returns:
        Initialized Lambda deployment client
    """
    from aor.deployment import get_client

    return get_client("aws-lambda", profile=profile, region=region)


def get_cloudformation_client(profile: Optional[str] = None, region: str = "us-east-1"):
    """
    Get a CloudFormation client.

    Args:
        profile: AWS profile name
        region: AWS region

    Returns:
        Initialized CloudFormation client
    """
    if profile:
        session = boto3.Session(profile_name=profile)
        return session.client("cloudformation", region_name=region)
    else:
        return boto3.client("cloudformation", region_name=region)


def create_lambda_test_event(
    ui: UI, client: DeploymentClient, agent: Dict[str, Any], result: Any
) -> bool:
    """
    Create a test event for the Lambda function.

    Args:
        ui: UI instance for displaying messages
        client: Deployment client
        agent: Agent configuration
        result: Deployment result

    Returns:
        True if test event creation was successful, False otherwise
    """
    try:
        # Try to extract function name from the available resources
        function_arn = None
        function_name = None

        # Debug available resources
        ui.debug(f"Available resources: {result.resources}")

        # Check for FunctionArn in resources
        if "FunctionArn" in result.resources:
            function_arn = result.resources.get("FunctionArn")
            function_name = function_arn.split(":")[-1]
        # Check for stack name which might contain the function name
        elif result.stack_name:
            # Function name is usually stack_name + "-function"
            function_name = f"{result.stack_name}-function"
            ui.debug(f"Using derived function name from stack: {function_name}")
        # Try to get function name from URL
        elif result.url:
            # Extract function name from URL if possible
            ui.debug(f"Trying to extract function name from URL: {result.url}")
            function_name = result.stack_name

        if not function_name:
            ui.warning(
                "Function name could not be determined, cannot create test event"
            )
            return False

        ui.debug(f"Creating test event for function: {function_name}")

        # Create test event JSON based on agent inputs
        test_event = {"input": "Hello from AI-on-Rails test event"}

        # Add agent-specific inputs if available
        if "inputs" in agent:
            for input_field in agent.get("inputs", []):
                field_name = input_field.get("name")
                if field_name and field_name != "input":
                    # Add sample values based on input type
                    if input_field.get("type") == "text":
                        test_event[field_name] = f"Sample {field_name}"
                    elif input_field.get("type") == "number":
                        test_event[field_name] = 42
                    elif input_field.get("type") == "boolean":
                        test_event[field_name] = True
                    elif input_field.get("type") == "array":
                        test_event[field_name] = ["sample", "array", "values"]
                    else:
                        test_event[field_name] = f"Sample {field_name}"

        # Format test event JSON
        import json

        test_event_json = json.dumps(test_event, indent=2)

        # Create a temporary file with the test event
        test_event_path = Path(f".lambda-test-event-{agent['name']}.json")
        with open(test_event_path, "w") as f:
            f.write(test_event_json)

        ui.debug(f"Test event JSON created at: {test_event_path}")

        # Use AWS CLI to create the test event
        try:
            # Create test event name
            test_event_name = f"{agent['name']}-test-event"

            # AWS CLI command to create test event
            aws_cmd = [
                "aws",
                "lambda",
                "update-function-event-invoke-config",
                "--function-name",
                function_name,
                "--maximum-event-age-in-seconds",
                "3600",
                "--maximum-retry-attempts",
                "0",
            ]

            # Add profile if available
            if hasattr(client, "profile") and client.profile:
                aws_cmd.extend(["--profile", client.profile])

            # Add region if available
            if hasattr(client, "region") and client.region:
                aws_cmd.extend(["--region", client.region])

            # Execute command
            ui.debug(f"Executing AWS CLI command: {' '.join(aws_cmd)}")
            result = subprocess.run(aws_cmd, capture_output=True, text=True)

            if result.returncode == 0:
                ui.success(f"Lambda test configuration updated for {function_name}")

                # Display instructions for testing on Lambda console
                ui.info("To test the function on AWS Lambda console:")
                ui.command(
                    f"1. Go to https://console.aws.amazon.com/lambda/home?region={client.region or 'us-east-1'}#/functions/{function_name}"
                )
                ui.command(f"2. Click on 'Test' tab")
                ui.command(f"3. Create a new test event with the following JSON:")
                ui.command(test_event_json)
                return True
            else:
                ui.warning(
                    f"Failed to update Lambda test configuration: {result.stderr}"
                )
                return False

        except Exception as e:
            ui.warning(f"Failed to create Lambda test event via AWS CLI: {str(e)}")
            ui.info(
                "You can still test the function manually on the AWS Lambda console"
            )
            ui.command(f"Test event JSON: {test_event_json}")
            return False

        # Clean up temporary file
        if test_event_path.exists():
            test_event_path.unlink()

    except Exception as e:
        ui.warning(f"Error creating Lambda test event: {str(e)}")
        import traceback

        ui.debug(f"Stack trace: {traceback.format_exc()}")
        return False
