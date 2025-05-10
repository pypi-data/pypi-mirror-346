#
# AI-on-Rails: All rights reserved.
#
"""Configuration for the backend module."""

import os
from typing import Dict, Any, Optional

# Default configuration
DEFAULT_CONFIG = {
    "api_url": "https://j64up4hf4i.execute-api.us-west-2.amazonaws.com/production",
    "request_timeout": 30,  # Default timeout for regular requests
    "a2a_timeout": 60,  # Longer timeout for AI processing
    "debug": False,
    # Logging configuration
    "log_level": "INFO",
    "log_format": "text",  # json, text
    "log_file": None,
    "log_to_file": False,
    "log_dir": "logs",
    "log_max_size": 10 * 1024 * 1024,  # 10MB
    "log_backup_count": 5,
    "log_rotation": True,
}


class BackendConfig:
    """Configuration for the backend module."""

    _instance = None

    def __new__(cls):
        """Singleton pattern to ensure only one config instance exists."""
        if cls._instance is None:
            cls._instance = super(BackendConfig, cls).__new__(cls)
            cls._instance._config = DEFAULT_CONFIG.copy()
            cls._instance._load_from_env()
        return cls._instance

    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # API URL
        if api_url := os.environ.get("AIONRAILS_API_URL"):
            self._config["api_url"] = api_url

        # Timeouts
        if request_timeout := os.environ.get("AIONRAILS_REQUEST_TIMEOUT"):
            try:
                self._config["request_timeout"] = int(request_timeout)
            except ValueError:
                pass

        if a2a_timeout := os.environ.get("AIONRAILS_A2A_TIMEOUT"):
            try:
                self._config["a2a_timeout"] = int(a2a_timeout)
            except ValueError:
                pass

        # Debug mode
        if debug := os.environ.get("AIONRAILS_DEBUG"):
            self._config["debug"] = debug.lower() in ("true", "1", "yes")

        # Logging configuration
        if log_level := os.environ.get("AIONRAILS_LOG_LEVEL"):
            self._config["log_level"] = log_level

        if log_format := os.environ.get("AIONRAILS_LOG_FORMAT"):
            self._config["log_format"] = log_format

        if log_file := os.environ.get("AIONRAILS_LOG_FILE"):
            self._config["log_file"] = log_file

        if log_to_file := os.environ.get("AIONRAILS_LOG_TO_FILE"):
            self._config["log_to_file"] = log_to_file.lower() in ("true", "1", "yes")

        if log_dir := os.environ.get("AIONRAILS_LOG_DIR"):
            self._config["log_dir"] = log_dir

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value.

        Args:
            key: The configuration key
            default: The default value if the key is not found

        Returns:
            The configuration value
        """
        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value.

        Args:
            key: The configuration key
            value: The configuration value
        """
        self._config[key] = value

    def update(self, config: Dict[str, Any]) -> None:
        """Update multiple configuration values.

        Args:
            config: Dictionary of configuration values to update
        """
        self._config.update(config)

    def as_dict(self) -> Dict[str, Any]:
        """Get the configuration as a dictionary.

        Returns:
            The configuration as a dictionary
        """
        return self._config.copy()


# Global configuration instance
config = BackendConfig()


def get_api_url() -> str:
    """Get the API URL.

    Returns:
        The API URL
    """
    return config.get("api_url")


def get_request_timeout() -> int:
    """Get the request timeout.

    Returns:
        The request timeout in seconds
    """
    return config.get("request_timeout")


def get_a2a_timeout() -> int:
    """Get the A2A request timeout.

    Returns:
        The A2A request timeout in seconds
    """
    return config.get("a2a_timeout")


def is_debug_enabled(ctx=None) -> bool:
    """Check if debug mode is enabled from any source.

    Debug mode can be enabled through:
    1. The --debug flag in the main CLI command (stored in context)
    2. The AOR_DEBUG environment variable
    3. The backend configuration

    Args:
        ctx: Optional Click context object that may contain debug flag

    Returns:
        True if debug mode is enabled, False otherwise
    """
    # Check context object first (from CLI --debug flag)
    if ctx and ctx.obj and ctx.obj.get("DEBUG", False):
        return True

    # Check environment variable
    if os.environ.get("AOR_DEBUG", "0") == "1":
        return True

    # Check configuration
    return config.get("debug", False)


def get_log_level() -> str:
    """Get the log level.

    Returns:
        The log level
    """
    return config.get("log_level", "INFO")


def get_log_format() -> str:
    """Get the log format.

    Returns:
        The log format (text or json)
    """
    return config.get("log_format", "text")


def get_log_file() -> Optional[str]:
    """Get the log file path.

    Returns:
        The log file path or None if not set
    """
    if config.get("log_to_file", False):
        log_file = config.get("log_file")
        if log_file:
            return log_file

        # If log_file is not set but log_to_file is True,
        # use the default log directory and filename
        log_dir = config.get("log_dir", "logs")
        return os.path.join(log_dir, "aor.log")

    return None


def is_log_to_file_enabled() -> bool:
    """Check if logging to file is enabled.

    Returns:
        True if logging to file is enabled, False otherwise
    """
    return config.get("log_to_file", False)


def configure(
    api_url: Optional[str] = None,
    request_timeout: Optional[int] = None,
    a2a_timeout: Optional[int] = None,
    debug: Optional[bool] = None,
    log_level: Optional[str] = None,
    log_format: Optional[str] = None,
    log_file: Optional[str] = None,
    log_to_file: Optional[bool] = None,
    log_dir: Optional[str] = None,
) -> None:
    """Configure the backend module.

    Args:
        api_url: The API URL
        request_timeout: The request timeout in seconds
        a2a_timeout: The A2A request timeout in seconds
        debug: Whether to enable debug mode
        log_level: The log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: The log format (text, json)
        log_file: The log file path
        log_to_file: Whether to log to a file
        log_dir: The directory for log files
    """
    update_dict = {}

    if api_url is not None:
        update_dict["api_url"] = api_url

    if request_timeout is not None:
        update_dict["request_timeout"] = request_timeout

    if a2a_timeout is not None:
        update_dict["a2a_timeout"] = a2a_timeout

    if debug is not None:
        update_dict["debug"] = debug

    if log_level is not None:
        update_dict["log_level"] = log_level

    if log_format is not None:
        update_dict["log_format"] = log_format

    if log_file is not None:
        update_dict["log_file"] = log_file

    if log_to_file is not None:
        update_dict["log_to_file"] = log_to_file

    if log_dir is not None:
        update_dict["log_dir"] = log_dir

    config.update(update_dict)
