"""
Logging utilities for the AI-on-Rails framework.

This module provides standardized logging functions for different parts of the agent lifecycle,
making logs more consistent, structured, and useful for debugging.
"""

import json
import logging
import time
import asyncio
from typing import Any, Dict, Optional, Union
from functools import wraps

logger = logging.getLogger(__name__)

# Constants for log categories
LOG_CATEGORY_INPUT = "INPUT"
LOG_CATEGORY_PROCESSING = "PROCESSING"
LOG_CATEGORY_OUTPUT = "OUTPUT"
LOG_CATEGORY_ERROR = "ERROR"
LOG_CATEGORY_VALIDATION = "VALIDATION"
LOG_CATEGORY_PERFORMANCE = "PERFORMANCE"


def safe_serialize(obj: Any) -> str:
    """
    Safely serialize an object to JSON string, handling common serialization issues.
    
    Args:
        obj: The object to serialize
        
    Returns:
        JSON string representation of the object
    """
    try:
        if hasattr(obj, "model_dump"):
            # Pydantic v2
            obj_dict = obj.model_dump()
        elif hasattr(obj, "dict"):
            # Pydantic v1
            obj_dict = obj.dict()
        elif isinstance(obj, dict):
            obj_dict = obj
        else:
            obj_dict = {"value": str(obj)}
            
        # Filter out sensitive fields
        if isinstance(obj_dict, dict):
            filtered_dict = {k: v for k, v in obj_dict.items() if k not in ["api_key", "password", "token"]}
        else:
            filtered_dict = obj_dict
            
        return json.dumps(filtered_dict, default=str, indent=2)
    except Exception as e:
        return f"<Could not serialize: {type(obj).__name__} - {str(e)}>"


def log_input(input_data: Any, source: str = "agent") -> None:
    """
    Log input data with standardized format.
    
    Args:
        input_data: The input data to log
        source: The source of the input (e.g., "agent", "protocol", "handler")
    """
    logger.info(f"[{LOG_CATEGORY_INPUT}] [{source.upper()}] Received input: {safe_serialize(input_data)}")


def log_output(output_data: Any, source: str = "agent") -> None:
    """
    Log output data with standardized format.
    
    Args:
        output_data: The output data to log
        source: The source of the output (e.g., "agent", "protocol", "handler")
    """
    logger.info(f"[{LOG_CATEGORY_OUTPUT}] [{source.upper()}] Generated output: {safe_serialize(output_data)}")


def log_processing(message: str, data: Optional[Any] = None, source: str = "agent") -> None:
    """
    Log processing information with standardized format.
    
    Args:
        message: The processing message
        data: Optional data to include
        source: The source of the processing (e.g., "agent", "protocol", "handler")
    """
    if data:
        logger.info(f"[{LOG_CATEGORY_PROCESSING}] [{source.upper()}] {message}: {safe_serialize(data)}")
    else:
        logger.info(f"[{LOG_CATEGORY_PROCESSING}] [{source.upper()}] {message}")


def log_error(error: Union[str, Exception], context: Optional[Dict[str, Any]] = None, source: str = "agent") -> None:
    """
    Log error information with standardized format.
    
    Args:
        error: The error message or exception
        context: Optional context information
        source: The source of the error (e.g., "agent", "protocol", "handler")
    """
    error_msg = str(error)
    error_type = error.__class__.__name__ if isinstance(error, Exception) else "Error"
    
    if context:
        logger.error(f"[{LOG_CATEGORY_ERROR}] [{source.upper()}] {error_type}: {error_msg} - Context: {safe_serialize(context)}")
    else:
        logger.error(f"[{LOG_CATEGORY_ERROR}] [{source.upper()}] {error_type}: {error_msg}")


def log_validation(is_valid: bool, entity_type: str, details: Optional[Dict[str, Any]] = None, source: str = "agent") -> None:
    """
    Log validation results with standardized format.
    
    Args:
        is_valid: Whether validation passed
        entity_type: The type of entity being validated (e.g., "input", "output")
        details: Optional validation details
        source: The source of the validation (e.g., "agent", "protocol", "handler")
    """
    result = "PASSED" if is_valid else "FAILED"
    
    if details:
        logger.info(f"[{LOG_CATEGORY_VALIDATION}] [{source.upper()}] {entity_type.upper()} validation {result}: {safe_serialize(details)}")
    else:
        logger.info(f"[{LOG_CATEGORY_VALIDATION}] [{source.upper()}] {entity_type.upper()} validation {result}")


def log_performance(operation: str, duration: float, metrics: Optional[Dict[str, Any]] = None, source: str = "agent") -> None:
    """
    Log performance metrics with standardized format.
    
    Args:
        operation: The operation being measured
        duration: The duration in seconds
        metrics: Optional additional metrics
        source: The source of the performance measurement (e.g., "agent", "protocol", "handler")
    """
    if metrics:
        logger.info(f"[{LOG_CATEGORY_PERFORMANCE}] [{source.upper()}] {operation} completed in {duration:.4f}s - Metrics: {safe_serialize(metrics)}")
    else:
        logger.info(f"[{LOG_CATEGORY_PERFORMANCE}] [{source.upper()}] {operation} completed in {duration:.4f}s")


def timed_operation(operation_name: str, source: str = "agent"):
    """
    Decorator to time an operation and log its performance.
    
    Args:
        operation_name: Name of the operation being timed
        source: The source of the operation (e.g., "agent", "protocol", "handler")
        
    Returns:
        Decorated function
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                duration = time.time() - start_time
                log_performance(operation_name, duration, source=source)
                return result
            except Exception as e:
                duration = time.time() - start_time
                log_performance(f"{operation_name} (failed)", duration, source=source)
                log_error(e, {"operation": operation_name, "duration": duration}, source=source)
                raise
                
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                duration = time.time() - start_time
                log_performance(operation_name, duration, source=source)
                return result
            except Exception as e:
                duration = time.time() - start_time
                log_performance(f"{operation_name} (failed)", duration, source=source)
                log_error(e, {"operation": operation_name, "duration": duration}, source=source)
                raise
                
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
            
    return decorator