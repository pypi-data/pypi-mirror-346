"""
Utilities for packaging deployments.
"""

import os
import shutil
import tempfile
import zipfile
import tarfile
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Set

from .fs import copy_files, get_file_checksum, get_directory_size
from ..models import PackageInfo
from ..exceptions import PackagingError


def create_deployment_package(
    source_dir: Path,
    output_file: Optional[Path] = None,
    format: str = "zip",
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    excluded_dirs: Optional[Set[str]] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> PackageInfo:
    """
    Create a deployment package from source directory.

    Args:
        source_dir: Source directory to package
        output_file: Optional output file path (auto-generated if not provided)
        format: Package format ('zip' or 'tar')
        include_patterns: Optional list of glob patterns to include
        exclude_patterns: Optional list of glob patterns to exclude
        excluded_dirs: Optional set of directory names to exclude
        metadata: Optional metadata to include in the package

    Returns:
        PackageInfo object with package details

    Raises:
        PackagingError: If packaging fails
    """
    if not source_dir.exists() or not source_dir.is_dir():
        raise PackagingError(f"Source directory {source_dir} does not exist")

    # Create temporary directory for staging
    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = Path(temp_dir_str)

        try:
            # Copy files to staging directory
            copied_files = copy_files(
                source_dir, temp_dir, include_patterns, exclude_patterns, excluded_dirs
            )

            # Generate metadata file if provided
            if metadata:
                metadata_file = temp_dir / ".package-metadata.json"
                with open(metadata_file, "w") as f:
                    json.dump(metadata, f, indent=2)

            # Determine output file if not provided
            if not output_file:
                output_file = Path(f"{source_dir.name}_package.{format}")

            # Create package based on format
            if format == "zip":
                _create_zip_package(temp_dir, output_file)
            elif format == "tar":
                _create_tar_package(temp_dir, output_file)
            else:
                raise PackagingError(f"Unsupported package format: {format}")

            # Create package info
            return PackageInfo(
                path=output_file,
                size_bytes=output_file.stat().st_size,
                files_count=len(copied_files),
                checksum=get_file_checksum(output_file),
                metadata=metadata or {},
            )

        except Exception as e:
            if output_file and output_file.exists():
                output_file.unlink()
            raise PackagingError(f"Failed to create deployment package: {str(e)}")


def extract_package(package_path: Path, output_dir: Path) -> Path:
    """
    Extract a deployment package.

    Args:
        package_path: Path to the package file
        output_dir: Directory to extract to

    Returns:
        Path to the extracted directory

    Raises:
        PackagingError: If extraction fails
    """
    if not package_path.exists():
        raise PackagingError(f"Package file {package_path} does not exist")

    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        if package_path.suffix == ".zip":
            with zipfile.ZipFile(package_path, "r") as zip_file:
                zip_file.extractall(output_dir)
        elif package_path.suffix in (".tar", ".gz", ".tgz"):
            with tarfile.open(package_path, "r:*") as tar_file:
                tar_file.extractall(output_dir)
        else:
            raise PackagingError(f"Unsupported package format: {package_path.suffix}")

        return output_dir
    except Exception as e:
        raise PackagingError(f"Failed to extract package: {str(e)}")


def _create_zip_package(source_dir: Path, output_file: Path) -> None:
    """Create a ZIP package from a directory."""
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                zipf.write(file_path, file_path.relative_to(source_dir))


def _create_tar_package(source_dir: Path, output_file: Path) -> None:
    """Create a TAR package from a directory."""
    with tarfile.open(output_file, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))
