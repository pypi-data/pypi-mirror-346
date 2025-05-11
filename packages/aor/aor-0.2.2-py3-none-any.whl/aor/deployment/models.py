"""
Data models for deployment configurations and results.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pathlib import Path


class DeploymentStatus(str, Enum):
    """Deployment status values."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESSFUL = "successful"
    FAILED = "failed"
    ROLLBACK_IN_PROGRESS = "rollback_in_progress"
    ROLLBACK_COMPLETE = "rollback_complete"
    UNKNOWN = "unknown"


@dataclass
class ResourceRequirements:
    """Resource requirements for deployments."""

    memory_mb: Optional[int] = None
    cpu: Optional[int] = None
    timeout_seconds: Optional[int] = None
    storage_gb: Optional[int] = None


@dataclass
class DeploymentOptions:
    """Configuration options for deployment."""

    name: str
    environment: str = "dev"
    region: Optional[str] = None
    profile: Optional[str] = None
    resources: ResourceRequirements = field(default_factory=ResourceRequirements)
    variables: Dict[str, str] = field(default_factory=dict)
    tags: Dict[str, str] = field(default_factory=dict)
    force: bool = False
    package_path: Optional[Path] = None
    include_files: List[str] = field(default_factory=list)
    exclude_files: List[str] = field(default_factory=list)

    stage: str = field(default="dev", init=False, repr=False)
    guided: bool = field(default=False, init=False, repr=False)
    update_only: bool = field(default=False, init=False, repr=False)
    recreate: bool = field(default=False, init=False, repr=False)
    recover_failed: bool = field(default=False, init=False, repr=False)
    verbose: bool = field(default=False, init=False, repr=False)
    memory: Optional[int] = field(default=None, init=False, repr=False)
    timeout: Optional[int] = field(default=None, init=False, repr=False)

    def __post_init__(self):
        """Set derived fields after initialization."""
        # Map environment to stage for backward compatibility
        self.stage = self.environment

        # Set memory and timeout from resources for backward compatibility
        if self.resources.memory_mb:
            self.memory = self.resources.memory_mb
        if self.resources.timeout_seconds:
            self.timeout = self.resources.timeout_seconds


@dataclass
class DeploymentResult:
    """Result of a deployment operation."""

    status: DeploymentStatus
    deployment_id: Optional[str] = None
    stack_name: Optional[str] = None
    url: Optional[str] = None
    resources: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    error: Optional[str] = None
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

    @property
    def is_successful(self) -> bool:
        """Check if deployment was successful."""
        return self.status == DeploymentStatus.SUCCESSFUL

    @property
    def duration_seconds(self) -> Optional[float]:
        """Get deployment duration in seconds."""
        if self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def complete(self, success: bool, error: Optional[str] = None) -> None:
        """Mark deployment as complete."""
        self.end_time = datetime.now()
        self.status = (
            DeploymentStatus.SUCCESSFUL if success else DeploymentStatus.FAILED
        )
        if error:
            self.error = error


@dataclass
class PackageInfo:
    """Information about a deployment package."""

    path: Path
    size_bytes: int
    files_count: int
    checksum: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
