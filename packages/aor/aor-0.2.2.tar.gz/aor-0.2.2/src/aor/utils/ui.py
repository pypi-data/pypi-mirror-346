#
# AI-on-Rails: All rights reserved.
#

from datetime import datetime
import os
from typing import Dict, Any, List, Optional, Tuple, Callable
import time
import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
    TaskID,
)
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.markdown import Markdown
from rich.syntax import Syntax
from rich.tree import Tree
from rich.style import Style
from rich.live import Live
from rich.layout import Layout
from rich.align import Align
from rich.padding import Padding


class UI:
    """Modern UI toolkit for AI-on-Rails CLI applications.

    This class provides a rich console interface for displaying information to users.
    It implements a unified console output solution with consistent formatting and
    different verbosity levels.

    Key features:
    - Consistent formatting for different message types
    - Support for different verbosity levels
    - Rich text formatting and styling
    - Progress indicators and spinners
    - Structured data display (tables, trees, etc.)

    Usage:
        # Initialize UI
        ui = UI(debug_mode=True)

        # Display information
        ui.header("Application Title")
        ui.info("Processing started")

        # Display information to console
        ui.info("Processing file")
        ui.debug("Detailed information")  # Only shown in debug mode

        # Display operations
        ui.file_operation("Created", "path/to/file.txt")
    """

    # Predefined styles
    STYLES = {
        "header": "bold blue",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "info": "cyan",
        "dim": "dim",
        "highlight": "bold yellow on black",
        "command": "bold cyan",
        "path": "italic yellow",
        "value": "bold magenta",
        "file_op": "bold cyan",
        "step": "bold blue",
        "operation": "bold white",
        "timestamp": "dim cyan",
    }

    # Log level icons
    LOG_ICONS = {
        "success": "✓",
        "warning": "!",
        "error": "✗",
        "info": "ℹ",
        "debug": "▸",
        "file": "📄",
        "step": "→",
        "operation": "⚙",
    }

    def __init__(self, debug_mode: bool = False, no_ansi: bool = None):
        """Initialize the UI toolkit.

        Args:
            debug_mode: Enable debug mode for more verbose output
            no_ansi: Disable ANSI color codes and interactive elements
                     If None, will check for --no-ansi in sys.argv
        """
        # Check for --no-ansi in command line if not explicitly provided
        if no_ansi is None:
            import sys

            no_ansi = "--no-ansi" in sys.argv

        self.console = Console(
            highlight=True,
            color_system=None if no_ansi else "auto",
            markup=not no_ansi,
            emoji=not no_ansi,
        )
        self.debug_mode = debug_mode
        self.no_ansi = no_ansi

        # No longer using external logging module

        # Current progress instance
        self._current_progress = None
        self._current_task_id = None

    def header(self, title: str, subtitle: str = None) -> None:
        """Display a header with optional subtitle."""
        if self.no_ansi:
            # Plain text header for no-ansi mode
            self.console.print(f"=== {title} ===")
            if subtitle:
                self.console.print(subtitle)
        else:
            # Rich formatted header
            panel_content = (
                f"[{self.STYLES['header']}]{title}[/{self.STYLES['header']}]"
            )
            if subtitle:
                panel_content += (
                    f"\n[{self.STYLES['info']}]{subtitle}[/{self.STYLES['info']}]"
                )

            self.console.print(
                Panel(
                    Align.center(panel_content),
                    border_style=self.STYLES["header"],
                    expand=False,
                )
            )

    def section(self, title: str) -> None:
        """Display a section header.

        Args:
            title: Section title
        """
        if self.no_ansi:
            # Plain text section header for no-ansi mode
            self.console.print(f"\n--- {title} ---")
        else:
            # Rich formatted section header
            self.console.print(
                f"\n[{self.STYLES['header']}]── {title} ──[/{self.STYLES['header']}]"
            )

    def divider(self) -> None:
        """Display a divider line."""
        self.console.print(
            "───────────────────────────────────────────────────────────────"
        )

    def text(self, message: str, end: str = os.linesep) -> None:
        """Display success message."""
        self.console.print(f"{message}", end=end)

    def success(self, message: str, end: str = os.linesep) -> None:
        """Display success message."""
        if self.no_ansi:
            self.console.print(f"SUCCESS: {message}", end=end)
        else:
            self.console.print(
                f"[{self.STYLES['success']}]{self.LOG_ICONS['success']}[/{self.STYLES['success']}] {message}",
                end=end,
            )

    def warning(self, message: str) -> None:
        """Display warning message."""
        if self.no_ansi:
            self.console.print(f"WARNING: {message}")
        else:
            self.console.print(
                f"[{self.STYLES['warning']}]{self.LOG_ICONS['warning']}[/{self.STYLES['warning']}] {message}"
            )

    def error(self, message: str) -> None:
        """Display error message."""
        if self.no_ansi:
            self.console.print(f"ERROR: {message}")
        else:
            self.console.print(
                f"[{self.STYLES['error']}]{self.LOG_ICONS['error']}[/{self.STYLES['error']}] {message}"
            )

    def info(self, message: str) -> None:
        """Display info message."""
        if self.no_ansi:
            self.console.print(f"INFO: {message}")
        else:
            self.console.print(
                f"[{self.STYLES['info']}]{self.LOG_ICONS['info']}[/{self.STYLES['info']}] {message}"
            )

    def debug(self, message: str) -> None:
        """Display debug message (only in debug mode)."""
        if self.debug_mode:
            if self.no_ansi:
                self.console.print(f"DEBUG: {message}")
            else:
                self.console.print(
                    f"[{self.STYLES['dim']}]{self.LOG_ICONS['debug']} {message}[/{self.STYLES['dim']}]"
                )

    def step(self, message: str) -> None:
        """Display a step in a process."""
        if self.no_ansi:
            self.console.print(f"STEP: {message}")
        else:
            self.console.print(
                f"[{self.STYLES['step']}]{self.LOG_ICONS['step']}[/{self.STYLES['step']}] {message}"
            )

    def operation(self, message: str) -> None:
        """Display an operation message."""
        if self.no_ansi:
            self.console.print(f"OPERATION: {message}")
        else:
            self.console.print(
                f"[{self.STYLES['operation']}]{self.LOG_ICONS['operation']}[/{self.STYLES['operation']}] {message}"
            )

    def file_operation(self, operation: str, path: str) -> None:
        """Display a file operation message.

        Args:
            operation: The file operation (e.g., "Created", "Modified", "Deleted")
            path: The file path
        """
        if self.no_ansi:
            self.console.print(f"FILE: {operation} {path}")
        else:
            self.console.print(
                f"[{self.STYLES['file_op']}]{self.LOG_ICONS['file']}[/{self.STYLES['file_op']}] "
                f"{operation} [{self.STYLES['path']}]{path}[/{self.STYLES['path']}]"
            )

    def group_file_operations(self, title: str, files: List[str]) -> None:
        """Display a group of file operations in a panel.

        Args:
            title: Title for the panel
            files: List of file paths
        """
        if not files:
            return

        # Sort files for consistent display
        sorted_files = sorted(files)

        if self.no_ansi:
            # Plain text file operations for no-ansi mode
            self.console.print(f"{title}:")
            for f in sorted_files:
                self.console.print(f"  • {f}")
        else:
            # Rich formatted file operations
            # Limit the number of files displayed to prevent overwhelming output
            max_files_to_display = 25
            if len(sorted_files) > max_files_to_display:
                displayed_files = sorted_files[:max_files_to_display]
                file_list = "\n".join(
                    [
                        f"• [{self.STYLES['path']}]{f}[/{self.STYLES['path']}]"
                        for f in displayed_files
                    ]
                )
                file_list += f"\n\n[dim]...and {len(sorted_files) - max_files_to_display} more files[/dim]"
            else:
                file_list = "\n".join(
                    [
                        f"• [{self.STYLES['path']}]{f}[/{self.STYLES['path']}]"
                        for f in sorted_files
                    ]
                )

            self.console.print(
                Panel(
                    file_list,
                    title=f"[{self.STYLES['file_op']}]{title}[/{self.STYLES['file_op']}]",
                    border_style=self.STYLES["file_op"],
                    expand=False,
                )
            )

    def command(self, cmd: str, description: str = None) -> None:
        """Display a command with optional description.

        Args:
            cmd: Command to display
            description: Optional description
        """
        if self.no_ansi:
            # Plain text command for no-ansi mode
            if description:
                self.console.print(f"  {cmd}  {description}")
            else:
                self.console.print(f"  {cmd}")
        else:
            # Rich formatted command
            cmd_text = f"[{self.STYLES['command']}]{cmd}[/{self.STYLES['command']}]"
            if description:
                self.console.print(f"  {cmd_text}  {description}")
            else:
                self.console.print(f"  {cmd_text}")

    def path(self, path: str) -> None:
        """Display a file path.

        Args:
            path: File path to display
        """
        if self.no_ansi:
            # Plain text path for no-ansi mode
            self.console.print(f"{path}")
        else:
            # Rich formatted path
            self.console.print(f"[{self.STYLES['path']}]{path}[/{self.STYLES['path']}]")

    def value(self, label: str, value: Any) -> None:
        """Display a labeled value.

        Args:
            label: Label for the value
            value: Value to display
        """
        if self.no_ansi:
            # Plain text value for no-ansi mode
            self.console.print(f"{label}: {value}")
        else:
            # Rich formatted value
            self.console.print(
                f"{label}: [{self.STYLES['value']}]{value}[/{self.STYLES['value']}]"
            )

    def prompt(self, message: str, default: str = None, password: bool = False) -> str:
        """Prompt for user input.

        Args:
            message: Prompt message
            default: Default value
            password: Whether input should be masked

        Returns:
            User input string
        """
        return Prompt.ask(
            message, default=default, password=password, console=self.console
        )

    def confirm(self, message: str, default: bool = True) -> bool:
        """Prompt for confirmation.

        Args:
            message: Confirmation message
            default: Default value

        Returns:
            True if confirmed, False otherwise
        """
        return Confirm.ask(message, default=default, console=self.console)

    def start_progress(
        self, message: str, total: Optional[int] = None
    ) -> Tuple[Progress, TaskID]:
        """Start a progress indicator with spinner.

        Args:
            message: Progress message
            total: Optional total steps (None for indeterminate)

        Returns:
            Tuple of (Progress, TaskID)
        """
        if self.no_ansi:
            # In non-ANSI mode, just print a message and return a dummy progress
            self.console.print(f"PROGRESS: Started - {message}")
            # Create a simple progress object without visual elements
            progress = Progress(
                TextColumn("{task.description}"),
                console=self.console,
                disable=True,  # Disable visual progress updates
            )
        else:
            # Create different progress objects based on whether total is provided
            if total is not None:
                # Determinate progress with bar and percentage
                progress = Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]{task.description}"),
                    BarColumn(),
                    TextColumn("[progress.percentage]{task.completed}/{task.total}"),
                    TimeElapsedColumn(),
                    console=self.console,
                )
            else:
                # Indeterminate progress with just spinner and elapsed time
                progress = Progress(
                    SpinnerColumn(),
                    TextColumn("[bold blue]{task.description}"),
                    TimeElapsedColumn(),
                    console=self.console,
                )

        task_id = progress.add_task(message, total=total)

        # Store current progress for later updates
        self._current_progress = progress
        self._current_task_id = task_id

        # Start progress display if not in no_ansi mode
        if not self.no_ansi:
            progress.start()
        return progress, task_id

    def update_progress(self, advance: int = 1, message: Optional[str] = None) -> None:
        """Update current progress.

        Args:
            advance: Steps to advance
            message: Optional new message
        """
        if not self._current_progress or not self._current_task_id:
            return

        if self.no_ansi and message:
            # In non-ANSI mode, print progress updates as messages
            self.console.print(f"PROGRESS: Update - {message}")

        if message:
            self._current_progress.update(self._current_task_id, description=message)

        self._current_progress.update(self._current_task_id, advance=advance)

    def stop_progress(self, message: Optional[str] = None) -> None:
        """Stop current progress.

        Args:
            message: Optional completion message
        """
        if not self._current_progress:
            return

        if self.no_ansi:
            # In non-ANSI mode, print completion message
            completion_text = f"PROGRESS: Completed"
            if message:
                completion_text += f" - {message}"
            self.console.print(completion_text)

        if message:
            self._current_progress.update(self._current_task_id, description=message)

        if not self.no_ansi:
            self._current_progress.stop()

        self._current_progress = None
        self._current_task_id = None

    def display_table(
        self, title: str, columns: List[str], rows: List[List[Any]]
    ) -> None:
        """Display data in a table.

        Args:
            title: Table title
            columns: Column headers
            rows: Table data rows
        """
        table = Table(title=title)

        # Add columns
        for column in columns:
            table.add_column(column)

        # Add rows
        for row in rows:
            table.add_row(*[str(cell) for cell in row])

        self.console.print(table)

    def display_tree(self, title: str, data: Dict[str, Any]) -> None:
        """Display hierarchical data as a tree.

        Args:
            title: Tree title
            data: Hierarchical data to display
        """
        tree = Tree(f"[bold]{title}[/bold]")

        def _add_items(parent, items):
            for key, value in items.items():
                if isinstance(value, dict):
                    branch = parent.add(f"[bold]{key}[/bold]")
                    _add_items(branch, value)
                else:
                    parent.add(f"[bold]{key}[/bold]: {value}")

        _add_items(tree, data)
        self.console.print(tree)

    def display_code(self, code: str, language: str = "python") -> None:
        """Display syntax-highlighted code.

        Args:
            code: Code to display
            language: Programming language
        """
        syntax = Syntax(code, language, theme="monokai", line_numbers=True)
        self.console.print(syntax)

    def display_markdown(self, markdown: str) -> None:
        """Display markdown content.

        Args:
            markdown: Markdown content to display
        """
        md = Markdown(markdown)
        self.console.print(md)

    def task_list(self, tasks: List[Tuple[str, bool]], title: str = "Tasks") -> None:
        """Display a list of tasks with completion status.

        Args:
            tasks: List of (task_description, is_completed) tuples
            title: Task list title
        """
        self.console.print(f"\n[bold]{title}[/bold]")
        for task, completed in tasks:
            status = (
                f"[{self.STYLES['success']}]✓[/{self.STYLES['success']}]"
                if completed
                else f"[{self.STYLES['dim']}]○[/{self.STYLES['dim']}]"
            )
            self.console.print(f"  {status} {task}")

    def banner(self, title: str, version: str = None) -> None:
        """Display an application banner.

        Args:
            title: Application title
            version: Optional version string
        """
        version_text = f" v{version}" if version else ""

        # Calculate the box width based on the title length
        title_length = len(title) + len(version_text)
        min_width = 39  # Minimum width
        content_width = max(min_width, title_length + 10)  # Add padding

        # Create the box borders with dynamic width
        top_border = "╭" + "─" * (content_width + 2) + "╮"
        middle_border = "│" + " " * (content_width + 2) + "│"
        bottom_border = "╰" + "─" * (content_width + 2) + "╯"

        # Calculate padding for centering the title
        title_padding = (content_width - title_length) // 2

        # Create the title line with proper centering
        title_line = (
            "│"
            + " " * (title_padding + 1)
            + f"[bold blue]{title}[/bold blue]{version_text}"
            + " " * (content_width - title_length - title_padding + 1)
            + "│"
        )

        # Assemble the banner
        banner_text = f"\n{top_border}\n{middle_border}\n{title_line}\n{middle_border}\n{bottom_border}\n"

        self.console.print(banner_text)

    def process_spinner(self, message: str, func: Callable, *args, **kwargs) -> Any:
        """Execute a function with a spinner indicator.

        Args:
            message: Message to display during execution
            func: Function to execute
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function

        Returns:
            Function return value
        """
        # In debug mode or no_ansi mode, don't use the spinner
        if self.debug_mode or self.no_ansi:
            self.info(f"{message}...")
            try:
                result = func(*args, **kwargs)
                self.success(f"{message} - Completed")
                return result
            except Exception as e:
                # Log the error with detailed information in debug mode
                self.error(f"{message} - Failed: {str(e)}")
                
                # Add more detailed debug information for RequestError
                if self.debug_mode and hasattr(e, "status_code") and hasattr(e, "response_text"):
                    self.debug(f"HTTP Status Code: {e.status_code}")
                    
                    # Display the response body in debug mode
                    self.debug(f"Response body: {e.response_text}")
                    
                    # Try to parse and display formatted JSON if possible
                    try:
                        import json
                        response_json = json.loads(e.response_text)
                        self.debug(f"Response JSON: {json.dumps(response_json, indent=2)}")
                    except Exception as json_error:
                        self.debug(f"Could not parse response as JSON: {str(json_error)}")
                
                # Re-raise the exception for the caller to handle
                raise
        else:
            # Use spinner in normal mode
            with self.console.status(
                f"[bold blue]{message}[/bold blue]", spinner="dots"
            ) as status:
                try:
                    result = func(*args, **kwargs)
                    status.update(f"[bold green]✓ {message} - Completed[/bold green]")
                    return result
                except Exception as e:
                    status.update(
                        f"[bold red]✗ {message} - Failed: {str(e)}[/bold red]"
                    )
                    
                    # Add more detailed debug information for RequestError in debug mode
                    if self.debug_mode and hasattr(e, "status_code") and hasattr(e, "response_text"):
                        self.debug(f"HTTP Status Code: {e.status_code}")
                        self.debug(f"Response body: {e.response_text}")
                        
                        # Try to parse and display formatted JSON if possible
                        try:
                            import json
                            response_json = json.loads(e.response_text)
                            self.debug(f"Response JSON: {json.dumps(response_json, indent=2)}")
                        except Exception as json_error:
                            self.debug(f"Could not parse response as JSON: {str(json_error)}")
                    
                    # Re-raise the exception for the caller to handle
                    raise

    def agent_info(self, agent_data: Dict[str, Any]) -> None:
        """Display agent information in a structured format.

        Args:
            agent_data: Agent data dictionary
        """
        agent_name = agent_data.get("name", "Unknown")
        agent_type = agent_data.get("type", "Unknown")

        table = Table(show_header=False, box=None, padding=(0, 1, 0, 1))
        table.add_column("Property")
        table.add_column("Value")

        table.add_row("Name", f"[bold]{agent_name}[/bold]")
        table.add_row("Type", f"[cyan]{agent_type}[/cyan]")

        if "desc" in agent_data and agent_data["desc"]:
            table.add_row("Description", agent_data["desc"])

        if "path" in agent_data and agent_data["path"]:
            path_obj = Path(agent_data["path"])
            table.add_row(
                "Path", f"[{self.STYLES['path']}]{path_obj}[/{self.STYLES['path']}]"
            )

        if "protocol" in agent_data and agent_data["protocol"]:
            table.add_row("Protocol", agent_data["protocol"])

        if "framework" in agent_data and agent_data["framework"]:
            table.add_row("Framework", agent_data["framework"])

        if "deployment" in agent_data and agent_data["deployment"]:
            # Handle both string and dictionary deployment values
            deployment = agent_data["deployment"]
            if isinstance(deployment, dict):
                deployment_type = deployment.get("type", "unknown")
                table.add_row("Deployment", f"{deployment_type}")
            else:
                table.add_row("Deployment", deployment)

        self.console.print(
            Panel(
                table, title=f"[bold blue]Agent: {agent_name}[/bold blue]", expand=False
            )
        )

    def group_start(self, title: str) -> None:
        """Start a logical group of related operations.

        Args:
            title: The group title
        """
        separator = "=" * (len(title) + 4)
        self.console.print(
            f"\n[{self.STYLES['header']}]{separator}[/{self.STYLES['header']}]"
        )
        self.console.print(
            f"[{self.STYLES['header']}]  {title}  [/{self.STYLES['header']}]"
        )
        self.console.print(
            f"[{self.STYLES['header']}]{separator}[/{self.STYLES['header']}]"
        )

    def group_end(self, title: str, success: bool = True) -> None:
        """End a logical group of related operations.

        Args:
            title: The group title (should match the one used in group_start)
            success: Whether the operation was successful (affects the completion message)
        """
        separator = "-" * (len(title) + 4)
        self.console.print(
            f"[{self.STYLES['header']}]{separator}[/{self.STYLES['header']}]"
        )
        
        # Change the message based on success status
        status_style = self.STYLES["success"] if success else self.STYLES["error"]
        status_text = "completed" if success else "failed"
        
        self.console.print(
            f"[{status_style}]  {title} {status_text}  [/{status_style}]"
        )
        self.console.print(
            f"[{self.STYLES['header']}]{separator}[/{self.STYLES['header']}]\n"
        )

    def command_result(self, command: str, success: bool, output: str = None) -> None:
        """Display the result of a command execution.

        Args:
            command: The command that was executed
            success: Whether the command was successful
            output: Optional command output to display
        """
        status_icon = self.LOG_ICONS["success"] if success else self.LOG_ICONS["error"]
        status_style = self.STYLES["success"] if success else self.STYLES["error"]
        status_text = "succeeded" if success else "failed"

        self.console.print(
            f"[{status_style}]{status_icon}[/{status_style}] Command [{self.STYLES['command']}]{command}[/{self.STYLES['command']}] {status_text}"
        )

        if output:
            self.console.print(
                Panel(output, title="Command Output", border_style="dim")
            )


# Create a default UI instance for direct import
# Check if --no-ansi flag is in command line arguments
import sys

no_ansi = "--no-ansi" in sys.argv
ui = UI(no_ansi=no_ansi)
