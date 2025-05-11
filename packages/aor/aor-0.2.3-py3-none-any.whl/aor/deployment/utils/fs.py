"""
File system utilities for deployment operations.
"""

import hashlib
import os
import shutil
from pathlib import Path
from typing import List, Optional, Set, Callable, Dict, Any


def ensure_directory(directory: Path) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        directory: Directory path

    Returns:
        Path to the directory
    """
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def safe_delete(path: Path) -> bool:
    """
    Safely delete a file or directory.

    Args:
        path: Path to delete

    Returns:
        True if deletion was successful
    """
    try:
        if path.is_file():
            path.unlink()
        elif path.is_dir():
            shutil.rmtree(path)
        return True
    except Exception:
        return False


def copy_files(
    source_dir: Path,
    target_dir: Path,
    include_patterns: Optional[List[str]] = None,
    exclude_patterns: Optional[List[str]] = None,
    excluded_dirs: Optional[Set[str]] = None,
) -> List[Path]:
    """
    Copy files from source to target directory with filtering.

    Args:
        source_dir: Source directory
        target_dir: Target directory
        include_patterns: Optional list of glob patterns to include
        exclude_patterns: Optional list of glob patterns to exclude
        excluded_dirs: Optional set of directory names to exclude

    Returns:
        List of copied file paths
    """
    if not excluded_dirs:
        excluded_dirs = {"__pycache__", ".git", ".vscode", ".idea", "node_modules"}

    copied_files = []
    target_dir.mkdir(parents=True, exist_ok=True)

    # Collect all files based on include/exclude patterns
    files_to_copy = []
    if include_patterns:
        for pattern in include_patterns:
            files_to_copy.extend(source_dir.glob(pattern))
    else:
        files_to_copy = list(source_dir.rglob("*"))

    # Apply exclusions
    if exclude_patterns:
        for pattern in exclude_patterns:
            for excluded in source_dir.glob(pattern):
                if excluded in files_to_copy:
                    files_to_copy.remove(excluded)

    # Copy files
    for src_path in files_to_copy:
        # Skip excluded directories
        if any(excl_dir in src_path.parts for excl_dir in excluded_dirs):
            continue

        # Skip directories in the list
        if src_path.is_dir():
            continue

        # Create relative path and destination
        rel_path = src_path.relative_to(source_dir)
        dest_path = target_dir / rel_path

        # Create parent directories
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy the file
        shutil.copy2(src_path, dest_path)
        copied_files.append(dest_path)

    return copied_files


def get_file_checksum(
    file_path: Path, algorithm: str = "sha256", buffer_size: int = 65536
) -> str:
    """
    Calculate checksum for a file.

    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use
        buffer_size: Read buffer size

    Returns:
        Hexadecimal checksum string
    """
    hash_algo = hashlib.new(algorithm)

    with open(file_path, "rb") as f:
        buffer = f.read(buffer_size)
        while buffer:
            hash_algo.update(buffer)
            buffer = f.read(buffer_size)

    return hash_algo.hexdigest()


def find_files_by_extension(
    directory: Path, extensions: List[str], recursive: bool = True
) -> List[Path]:
    """
    Find files with specific extensions.

    Args:
        directory: Directory to search
        extensions: List of file extensions (without the dot)
        recursive: Whether to search recursively

    Returns:
        List of matching file paths
    """
    files = []
    search_func = directory.rglob if recursive else directory.glob

    for ext in extensions:
        files.extend(search_func(f"*.{ext}"))

    return files


def get_directory_size(directory: Path) -> int:
    """
    Calculate total size of a directory in bytes.

    Args:
        directory: Directory path

    Returns:
        Size in bytes
    """
    total_size = 0
    for path in directory.rglob("*"):
        if path.is_file():
            total_size += path.stat().st_size
    return total_size
