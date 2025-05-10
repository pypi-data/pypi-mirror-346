"""
Reusable components for AI-on-Rails.

This package contains shared components used across the framework.
"""

# Media handling
from .media import (
    MediaType,
    MediaFormat,
    MediaItem,
    TextItem,
    ImageItem,
    AudioItem,
    VideoItem,
    Model3DItem,
    DocumentItem,
    BinaryItem,
    MediaItemUnion,
    MediaHandler,
    TextHandler,
    ImageHandler,
    AudioHandler,
    MediaHandlerRegistry,
    media_registry
)

# Authentication
from .auth import (
    # JWT
    JWTConfig,
    JWTHandler,
    JWTError,
    TokenExpiredError,
    InvalidTokenError,
    jwt_required,
    create_jwt_token,
    validate_jwt_token,
    
    # API Key
    APIKeyConfig,
    APIKeyManager,
    APIKeyError,
    InvalidAPIKeyError,
    ExpiredAPIKeyError,
    RateLimitExceededError,
    api_key_required,
    generate_api_key,
    validate_api_key
)

# Monitoring
from .monitoring import (
    # Metrics
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
    timer_metric,
    
    # Logging
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
    # Media
    "MediaType",
    "MediaFormat",
    "MediaItem",
    "TextItem",
    "ImageItem",
    "AudioItem",
    "VideoItem",
    "Model3DItem",
    "DocumentItem",
    "BinaryItem",
    "MediaItemUnion",
    "MediaHandler",
    "TextHandler",
    "ImageHandler",
    "AudioHandler",
    "MediaHandlerRegistry",
    "media_registry",
    
    # Auth - JWT
    "JWTConfig",
    "JWTHandler",
    "JWTError",
    "TokenExpiredError",
    "InvalidTokenError",
    "jwt_required",
    "create_jwt_token",
    "validate_jwt_token",
    
    # Auth - API Key
    "APIKeyConfig",
    "APIKeyManager",
    "APIKeyError",
    "InvalidAPIKeyError",
    "ExpiredAPIKeyError",
    "RateLimitExceededError",
    "api_key_required",
    "generate_api_key",
    "validate_api_key",
    
    # Monitoring - Metrics
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
    
    # Monitoring - Logging
    "LogConfig",
    "StructuredLogger",
    "JSONFormatter",
    "RequestLogger",
    "log_context",
    "log_operation",
    "get_logger",
    "configure_logging"
]