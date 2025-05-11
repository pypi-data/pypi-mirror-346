"""
AWS EC2 deployment adapter for AI-on-Rails.
"""

from typing import Dict, Any, List
from pathlib import Path
import subprocess
import shutil
import json
import os
import tarfile

from ..base.deployment_adapter import DeploymentAdapter


class EC2DeploymentAdapter(DeploymentAdapter):
    """
    AWS EC2 deployment adapter.
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.agent_name = config.get("agent_name")
        self.stage = config.get("stage", "dev")
        self.instance_type = config.get("instance_type", "t3.medium")
        self.port = config.get("port", 8000)
        self.key_name = config.get("key_name")
        self.vpc_id = config.get("vpc_id")
        self.subnet_id = config.get("subnet_id")
        self.profile = config.get("aws_profile")
        self.region = config.get("region", "us-east-1")
    
    def validate_config(self) -> bool:
        """Validate EC2 deployment configuration."""
        required_fields = ["agent_name", "key_name", "vpc_id", "subnet_id"]
        for field in required_fields:
            if field not in self.config:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate instance type
        valid_instance_types = [
            "t3.micro", "t3.small", "t3.medium", "t3.large",
            "m5.large", "m5.xlarge", "m5.2xlarge"
        ]
        if self.instance_type not in valid_instance_types:
            print(f"Warning: Instance type {self.instance_type} may not be ideal for this workload")
        
        return True
    
    def prepare_package(self, agent_dir: Path, output_dir: Path) -> bool:
        """Prepare EC2 deployment package."""
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create tar.gz archive of agent files
        archive_path = output_dir / f"{self.agent_name}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as tar:
            if agent_dir.is_file():
                tar.add(agent_dir, arcname=agent_dir.name)
            else:
                tar.add(agent_dir, arcname=self.agent_name)
        
        # TODO: Generate EC2-specific files from templates
        
        return True
    
    def deploy(self, package_dir: Path, **kwargs) -> Dict[str, Any]:
        """Deploy to AWS EC2 using CloudFormation."""
        # Deploy CloudFormation stack
        stack_name = f"{self.agent_name}-{self.stage}"
        template_file = package_dir / "cloudformation.yaml"
        
        cmd = [
            "aws", "cloudformation", "deploy",
            "--template-file", str(template_file),
            "--stack-name", stack_name,
            "--capabilities", "CAPABILITY_IAM",
            "--parameter-overrides",
            f"InstanceType={self.instance_type}",
            f"KeyName={self.key_name}",
            f"VpcId={self.vpc_id}",
            f"SubnetId={self.subnet_id}",
            f"Stage={self.stage}",
            f"AgentPort={self.port}",
            f"AgentName={self.agent_name}"
        ]
        
        if self.profile:
            cmd.extend(["--profile", self.profile])
        
        if self.region:
            cmd.extend(["--region", self.region])
        
        subprocess.run(cmd, check=True)
        
        # Get deployment outputs
        return self._get_deployment_info()
    
    def get_runtime_config(self) -> Dict[str, Any]:
        """Get EC2 runtime configuration."""
        return {
            "instance_type": self.instance_type,
            "port": self.port,
            "key_name": self.key_name,
            "vpc_id": self.vpc_id,
            "subnet_id": self.subnet_id
        }
    
    def get_required_environment_vars(self) -> List[str]:
        """Get required environment variables."""
        return ["ANTHROPIC_API_KEY"]
    
    def validate_prerequisites(self) -> bool:
        """Validate AWS CLI is installed."""
        try:
            subprocess.run(["aws", "--version"], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def get_supported_features(self) -> List[str]:
        """Get supported features."""
        return [
            "full-control",
            "customizable",
            "persistent-storage",
            "ssh-access",
            "https-endpoint",
            "ssl-certificates"
        ]
    
    def _get_deployment_info(self) -> Dict[str, Any]:
        """Get deployment information from CloudFormation stack."""
        stack_name = f"{self.agent_name}-{self.stage}"
        
        cmd = [
            "aws", "cloudformation", "describe-stacks",
            "--stack-name", stack_name,
            "--query", "Stacks[0].Outputs",
            "--output", "json"
        ]
        
        if self.profile:
            cmd.extend(["--profile", self.profile])
        
        if self.region:
            cmd.extend(["--region", self.region])
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        outputs = json.loads(result.stdout)
        
        deployment_info = {}
        for output in outputs:
            key = output["OutputKey"]
            value = output["OutputValue"]
            deployment_info[key] = value
        
        return deployment_info


__all__ = ["EC2DeploymentAdapter"]