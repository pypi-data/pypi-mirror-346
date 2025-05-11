"""
Command execution utilities for deployment operations.
"""

import os
import subprocess
import time
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Union, Tuple


@dataclass
class CommandResult:
    """Result of command execution."""

    returncode: int
    stdout: str
    stderr: str
    duration: float
    command: str

    @property
    def success(self) -> bool:
        """Check if command was successful."""
        return self.returncode == 0

    def __str__(self) -> str:
        status = "SUCCESS" if self.success else f"FAILED ({self.returncode})"
        return f"{status}: {self.command} ({self.duration:.2f}s)"


def run_command(
    cmd: Union[List[str], str],
    shell: bool = False,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    timeout: Optional[float] = None,
    check: bool = False,
    capture_output: bool = True,
) -> CommandResult:
    """
    Run a shell command with improved error handling and timing.

    Args:
        cmd: Command string or list of arguments
        shell: Whether to use shell execution
        cwd: Working directory for the command
        env: Environment variables
        timeout: Command timeout in seconds
        check: Whether to raise an exception on non-zero return code
        capture_output: Whether to capture stdout/stderr

    Returns:
        CommandResult with execution details

    Raises:
        subprocess.TimeoutExpired: If command times out
        subprocess.CalledProcessError: If check=True and command returns non-zero
    """
    # Create final environment
    full_env = os.environ.copy()
    if env:
        full_env.update(env)

    # Record command for result
    cmd_str = cmd if isinstance(cmd, str) else " ".join(cmd)

    # Setup stdout/stderr capture
    stdout_opt = subprocess.PIPE if capture_output else None
    stderr_opt = subprocess.PIPE if capture_output else None

    # Run command with timing
    start_time = time.time()

    try:
        process = subprocess.run(
            cmd,
            shell=shell,
            cwd=cwd,
            env=full_env,
            stdout=stdout_opt,
            stderr=stderr_opt,
            timeout=timeout,
            check=check,
            text=True,
        )

        duration = time.time() - start_time

        # Create result
        result = CommandResult(
            returncode=process.returncode,
            stdout=process.stdout if capture_output else "",
            stderr=process.stderr if capture_output else "",
            duration=duration,
            command=cmd_str,
        )

        return result

    except subprocess.TimeoutExpired as e:
        duration = time.time() - start_time
        result = CommandResult(
            returncode=-1,
            stdout=e.stdout.decode("utf-8") if e.stdout else "",
            stderr=(
                e.stderr.decode("utf-8")
                if e.stderr
                else f"Command timed out after {timeout} seconds"
            ),
            duration=duration,
            command=cmd_str,
        )
        if check:
            raise
        return result

    except subprocess.CalledProcessError as e:
        duration = time.time() - start_time
        result = CommandResult(
            returncode=e.returncode,
            stdout=e.stdout if capture_output else "",
            stderr=e.stderr if capture_output else "",
            duration=duration,
            command=cmd_str,
        )
        if check:
            raise
        return result


def run_commands_in_sequence(
    commands: List[Union[List[str], str]],
    shell: bool = False,
    cwd: Optional[str] = None,
    env: Optional[Dict[str, str]] = None,
    stop_on_error: bool = True,
) -> List[CommandResult]:
    """
    Run multiple commands in sequence.

    Args:
        commands: List of commands to run
        shell: Whether to use shell execution
        cwd: Working directory for the commands
        env: Environment variables
        stop_on_error: Whether to stop execution on first error

    Returns:
        List of CommandResult objects
    """
    results = []

    for cmd in commands:
        result = run_command(cmd, shell=shell, cwd=cwd, env=env, capture_output=True)
        results.append(result)

        if stop_on_error and not result.success:
            break

    return results
