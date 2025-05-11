"""
Authentication components for AI-on-Rails.

This package provides JWT and API key authentication mechanisms.
"""

from .jwt import (
    JWTConfig,
    JWTHandler,
    JWTError,
    TokenExpiredError,
    InvalidTokenError,
    jwt_required,
    create_jwt_token,
    validate_jwt_token
)

from .api_key import (
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

__all__ = [
    # JWT
    "JWTConfig",
    "JWTHandler",
    "JWTError",
    "TokenExpiredError",
    "InvalidTokenError",
    "jwt_required",
    "create_jwt_token",
    "validate_jwt_token",
    
    # API Key
    "APIKeyConfig",
    "APIKeyManager",
    "APIKeyError",
    "InvalidAPIKeyError",
    "ExpiredAPIKeyError",
    "RateLimitExceededError",
    "api_key_required",
    "generate_api_key",
    "validate_api_key"
]