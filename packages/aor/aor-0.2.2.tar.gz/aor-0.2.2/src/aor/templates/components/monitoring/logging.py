"""
Logging configuration and utilities for AI-on-Rails.

Provides structured logging with support for various outputs and formats.
"""

import logging
import json
import sys
import os
import time
import traceback
from typing import Dict, Any, Optional, Union, List
from datetime import datetime
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from dataclasses import dataclass, asdict
import uuid
from contextlib import contextmanager


@dataclass
class LogConfig:
    """Configuration for logging."""
    log_level: str = "INFO"
    log_format: str = "json"  # json, text
    log_file: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    enable_console: bool = True
    enable_file: bool = False
    enable_rotation: bool = True
    rotation_when: str = "midnight"  # For TimedRotatingFileHandler
    include_stack_trace: bool = True
    json_indent: Optional[int] = None


class StructuredLogger:
    """
    Logger that supports structured logging with context.
    """
    
    def __init__(self, name: str, config: LogConfig):
        """
        Initialize structured logger.
        
        Args:
            name: Logger name
            config: Logging configuration
        """
        self.config = config
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, config.log_level.upper()))
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Configure formatters
        if config.log_format == "json":
            formatter = JSONFormatter(include_stack_trace=config.include_stack_trace)
        else:
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
        
        # Add console handler
        if config.enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        
        # Add file handler
        if config.enable_file and config.log_file:
            os.makedirs(os.path.dirname(config.log_file), exist_ok=True)
            
            if config.enable_rotation:
                if config.rotation_when:
                    file_handler = TimedRotatingFileHandler(
                        config.log_file,
                        when=config.rotation_when,
                        backupCount=config.backup_count
                    )
                else:
                    file_handler = RotatingFileHandler(
                        config.log_file,
                        maxBytes=config.max_file_size,
                        backupCount=config.backup_count
                    )
            else:
                file_handler = logging.FileHandler(config.log_file)
            
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        
        # Context data
        self._context: Dict[str, Any] = {}
    
    def with_context(self, **kwargs) -> 'StructuredLogger':
        """
        Create a new logger with additional context.
        
        Args:
            **kwargs: Context key-value pairs
            
        Returns:
            New logger instance with added context
        """
        new_logger = StructuredLogger(self.logger.name, self.config)
        new_logger._context = {**self._context, **kwargs}
        new_logger.logger = self.logger
        return new_logger
    
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log(logging.DEBUG, message, **kwargs)
    
    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log(logging.INFO, message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log(logging.WARNING, message, **kwargs)
    
    def error(self, message: str, **kwargs):
        """Log error message."""
        self._log(logging.ERROR, message, **kwargs)
    
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._log(logging.CRITICAL, message, **kwargs)
    
    def exception(self, message: str, **kwargs):
        """Log exception with stack trace."""
        kwargs["exc_info"] = sys.exc_info()
        self._log(logging.ERROR, message, **kwargs)
    
    def _log(self, level: int, message: str, **kwargs):
        """Internal log method."""
        # Merge context
        extra = {**self._context, **kwargs}
        
        # Handle exc_info separately
        exc_info = extra.pop("exc_info", None)
        
        # Create log record
        self.logger.log(level, message, extra={"structured_data": extra}, exc_info=exc_info)


class JSONFormatter(logging.Formatter):
    """
    JSON formatter for structured logging.
    """
    
    def __init__(self, include_stack_trace: bool = True):
        super().__init__()
        self.include_stack_trace = include_stack_trace
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "thread": record.thread,
            "thread_name": record.threadName,
            "process": record.process,
        }
        
        # Add structured data
        if hasattr(record, "structured_data"):
            log_data.update(record.structured_data)
        
        # Add exception info
        if record.exc_info and self.include_stack_trace:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "stacktrace": traceback.format_exception(*record.exc_info)
            }
        
        return json.dumps(log_data)


class RequestLogger:
    """
    Logger for HTTP requests with timing and tracing.
    """
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
    
    def log_request(self, request_id: str, method: str, path: str, 
                   headers: Dict[str, str], body: Optional[Any] = None):
        """Log incoming request."""
        self.logger.info(
            "Request received",
            request_id=request_id,
            method=method,
            path=path,
            headers=self._sanitize_headers(headers),
            body_size=len(str(body)) if body else 0
        )
    
    def log_response(self, request_id: str, status_code: int, 
                    response_time_ms: float, body_size: int):
        """Log outgoing response."""
        self.logger.info(
            "Response sent",
            request_id=request_id,
            status_code=status_code,
            response_time_ms=response_time_ms,
            body_size=body_size
        )
    
    def log_error(self, request_id: str, error: Exception):
        """Log request error."""
        self.logger.exception(
            "Request failed",
            request_id=request_id,
            error_type=type(error).__name__,
            error_message=str(error)
        )
    
    def _sanitize_headers(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Remove sensitive information from headers."""
        sensitive_headers = ["authorization", "x-api-key", "cookie"]
        sanitized = {}
        
        for key, value in headers.items():
            if key.lower() in sensitive_headers:
                sanitized[key] = "[REDACTED]"
            else:
                sanitized[key] = value
        
        return sanitized


@contextmanager
def log_context(**kwargs):
    """
    Context manager for adding temporary logging context.
    
    Example:
        with log_context(user_id="123", operation="process"):
            logger.info("Processing started")
    """
    current_context = getattr(log_context, "_context", {})
    new_context = {**current_context, **kwargs}
    
    setattr(log_context, "_context", new_context)
    try:
        yield
    finally:
        setattr(log_context, "_context", current_context)


@contextmanager
def log_operation(logger: StructuredLogger, operation: str, **kwargs):
    """
    Context manager for logging operation with timing.
    
    Example:
        with log_operation(logger, "data_processing", user_id="123"):
            # Process data
    """
    operation_id = str(uuid.uuid4())
    start_time = time.time()
    
    logger.info(
        f"Starting {operation}",
        operation=operation,
        operation_id=operation_id,
        **kwargs
    )
    
    try:
        yield operation_id
        
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            f"Completed {operation}",
            operation=operation,
            operation_id=operation_id,
            duration_ms=duration_ms,
            status="success",
            **kwargs
        )
        
    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000
        logger.exception(
            f"Failed {operation}",
            operation=operation,
            operation_id=operation_id,
            duration_ms=duration_ms,
            status="error",
            error_type=type(e).__name__,
            **kwargs
        )
        raise


# Global logger registry
_loggers: Dict[str, StructuredLogger] = {}


def get_logger(name: str, config: Optional[LogConfig] = None) -> StructuredLogger:
    """
    Get or create a logger.
    
    Args:
        name: Logger name
        config: Optional logging configuration
        
    Returns:
        StructuredLogger instance
    """
    if name not in _loggers:
        _loggers[name] = StructuredLogger(name, config or LogConfig())
    
    return _loggers[name]


def configure_logging(config: LogConfig):
    """
    Configure global logging settings.
    
    Args:
        config: Logging configuration
    """
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers = []
    
    # Add handlers based on config
    if config.log_format == "json":
        formatter = JSONFormatter(include_stack_trace=config.include_stack_trace)
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    if config.enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    if config.enable_file and config.log_file:
        os.makedirs(os.path.dirname(config.log_file), exist_ok=True)
        file_handler = RotatingFileHandler(
            config.log_file,
            maxBytes=config.max_file_size,
            backupCount=config.backup_count
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)