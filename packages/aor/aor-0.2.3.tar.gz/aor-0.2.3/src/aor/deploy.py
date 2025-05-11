#
# AI-on-Rails: All rights reserved.
#

import os
import shutil
from pathlib import Path
import logging
import rich_click as click

from .utils.ui import UI
from .common.config import Config
from .deployment.models import DeploymentOptions, ResourceRequirements
from .deployment.exceptions import (
    DeploymentError,
    ClientInitializationError,
    ValidationError,
)
from .deployment.agent import get_agents_to_deploy
from .deployment.clients.aws.lambda_deployment import deploy_to_aws_lambda

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("deploy")


@click.command()
@click.option(
    "--target",
    type=click.Choice(["aws-lambda", "aws-ec2", "azure", "gcp"]),
    default="aws-lambda",
    help="Deployment target platform",
)
@click.option(
    "--endpoint",
    type=str,
    help="Name of specific agent to deploy (deploys all if not specified)",
)
@click.option(
    "--stage",
    type=click.Choice(["dev", "staging", "prod"]),
    default="dev",
    help="Deployment stage",
)
@click.option("--region", type=str, help="AWS region (overrides default from config)")
@click.option("--memory", type=int, help="Memory size in MB for Lambda function")
@click.option("--timeout", type=int, help="Timeout in seconds for Lambda function")
@click.option("--profile", type=str, help="AWS CLI profile to use")
@click.option("--guided", is_flag=True, help="Guide through deployment options")
@click.option(
    "--update-only",
    "-u",
    is_flag=True,
    help="Deploy only if changes are detected, otherwise succeed without error",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    help="Force deployment even if SAM detects no changes",
)
@click.option(
    "--recreate",
    "-r",
    is_flag=True,
    help="Delete and recreate the stack instead of updating it",
)
@click.option(
    "--recover-failed",
    is_flag=True,
    help="Attempt to recover stacks in UPDATE_ROLLBACK_FAILED state",
)
@click.option("--verbose", "-v", is_flag=True, help="Show verbose output")
@click.pass_context
def deploy(
    ctx,
    target: str,
    endpoint: str,
    stage: str,
    region: str,
    memory: int,
    timeout: int,
    profile: str,
    guided: bool,
    update_only: bool,
    force: bool,
    recreate: bool,
    recover_failed: bool,
    verbose: bool,
):
    """Deploy the current application to Cloud services."""
    # Get no_ansi from context if available
    no_ansi = ctx.obj.get("NO_ANSI", False) if ctx.obj else False

    # Get debug mode from context
    debug = ctx.obj.get("DEBUG", False) if ctx.obj else False

    # Initialize UI
    ui = UI(debug_mode=debug or verbose, no_ansi=no_ansi)

    # Set logging level based on verbosity/debug
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    elif verbose:
        logging.getLogger().setLevel(logging.INFO)

    ui.header(f"Deploying to {target.upper()}", f"Stage: {stage}")

    config = Config(readiness=Config.READY_TO_DEPLOY)

    # Get application name
    app_name = config.get("name") or "aor-app"
    ui.info(f"Application: {app_name}")

    # Get agents to deploy
    ui.section("Finding Agents")
    agents_to_deploy = get_agents_to_deploy(ui, config, endpoint)
    if not agents_to_deploy:
        ui.error("No agents found to deploy.")
        return

    # Display agents that will be deployed
    agent_list = [
        [a["name"], a.get("type", "unknown"), a.get("path", "unknown")]
        for a in agents_to_deploy
    ]
    ui.display_table(
        f"Agents to Deploy ({len(agents_to_deploy)})",
        ["Name", "Type", "Path"],
        agent_list,
    )

    # Create deployment options
    resources = ResourceRequirements(memory_mb=memory, timeout_seconds=timeout)

    options = DeploymentOptions(
        name=app_name,
        environment=stage,
        region=region,
        profile=profile,
        resources=resources,
        force=force,
    )

    # Set additional options
    options.guided = guided
    options.update_only = update_only
    options.recreate = recreate
    options.recover_failed = recover_failed
    options.verbose = verbose

    # Display deployment configuration
    ui.section("Deployment Configuration")
    options_table = []
    options_table.append(["Target", target])
    options_table.append(["Environment", stage])
    if region:
        options_table.append(["Region", region])
    if profile:
        options_table.append(["AWS Profile", profile])
    if memory:
        options_table.append(["Memory", f"{memory} MB"])
    if timeout:
        options_table.append(["Timeout", f"{timeout} seconds"])
    options_table.append(["Force", "Yes" if force else "No"])
    options_table.append(["Recreate", "Yes" if recreate else "No"])
    options_table.append(["Update Only", "Yes" if update_only else "No"])
    options_table.append(["Recover Failed Stacks", "Yes" if recover_failed else "No"])

    # Check if ANTHROPIC_API_KEY is set
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if anthropic_api_key:
        options_table.append(
            ["ANTHROPIC_API_KEY", "Set (will be used during deployment)"]
        )
    else:
        options_table.append(
            ["ANTHROPIC_API_KEY", "Not set (agent may not work properly)"]
        )

    ui.display_table("Options", ["Setting", "Value"], options_table)

    # Create temporary deployment directory
    deploy_dir = Path(".aor-deploy")
    if deploy_dir.exists():
        with ui.console.status("Cleaning up previous deployment files..."):
            shutil.rmtree(deploy_dir)

    ui.debug(f"Creating deployment directory: {deploy_dir}")
    deploy_dir.mkdir()

    # Note: A2A layer creation is now handled in the deployment process
    # No need to pre-create it here

    try:
        # Deploy based on target
        if target == "aws-lambda":
            deploy_to_aws_lambda(ui, config, agents_to_deploy, options, deploy_dir)
        elif target == "aws-ec2":
            ui.error("AWS EC2 deployment is not yet implemented.")
        elif target == "azure":
            ui.error("Azure deployment is not yet implemented.")
        elif target == "gcp":
            ui.error("GCP deployment is not yet implemented.")
        else:
            ui.error(f"Unknown target platform: {target}")
            
        ui.info("Are you ready to publish it with `aor publish`?")
    finally:
        # Clean up deployment directory
        if deploy_dir.exists():
            ui.info("Cleaning up deployment files...")
            shutil.rmtree(deploy_dir)
            ui.debug("Deployment directory removed")


if __name__ == "__main__":
    deploy()
