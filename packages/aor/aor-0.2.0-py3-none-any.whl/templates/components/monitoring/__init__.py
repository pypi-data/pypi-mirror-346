"""
Monitoring and logging components for AI-on-Rails.

This package provides metrics collection and structured logging.
"""

from .metrics import (
    MetricType,
    MetricConfig,
    Metric,
    MetricsCollector,
    Timer,
    PrometheusExporter,
    get_metrics_collector,
    increment_counter,
    set_gauge,
    record_histogram,
    timer_metric
)

from .logging import (
    LogConfig,
    StructuredLogger,
    JSONFormatter,
    RequestLogger,
    log_context,
    log_operation,
    get_logger,
    configure_logging
)

__all__ = [
    # Metrics
    "MetricType",
    "MetricConfig",
    "Metric",
    "MetricsCollector",
    "Timer",
    "PrometheusExporter",
    "get_metrics_collector",
    "increment_counter",
    "set_gauge",
    "record_histogram",
    "timer_metric",
    
    # Logging
    "LogConfig",
    "StructuredLogger",
    "JSONFormatter",
    "RequestLogger",
    "log_context",
    "log_operation",
    "get_logger",
    "configure_logging"
]