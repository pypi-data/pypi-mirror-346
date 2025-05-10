"""
API Key authentication for AI-on-Rails.

Provides API key generation, validation, and middleware for API authentication.
"""

import hashlib
import hmac
import secrets
import time
from typing import Dict, Any, Optional, Tuple, Callable, List
from datetime import datetime, timedelta
from dataclasses import dataclass
from functools import wraps
import os
import json
import re


@dataclass
class APIKeyConfig:
    """API key configuration settings."""
    key_prefix: str = "aor_"
    key_length: int = 32
    hash_algorithm: str = "sha256"
    allow_multiple_keys: bool = True
    key_rotation_days: int = 90
    rate_limit_requests: int = 1000
    rate_limit_window_seconds: int = 3600


class APIKeyError(Exception):
    """Base exception for API key errors."""
    pass


class InvalidAPIKeyError(APIKeyError):
    """API key is invalid."""
    pass


class ExpiredAPIKeyError(APIKeyError):
    """API key has expired."""
    pass


class RateLimitExceededError(APIKeyError):
    """Rate limit exceeded for API key."""
    pass


class APIKeyManager:
    """
    Manages API key operations including generation, validation, and storage.
    """
    
    def __init__(self, config: APIKeyConfig, 
                 storage_backend: Optional[Callable] = None):
        """
        Initialize API key manager.
        
        Args:
            config: API key configuration
            storage_backend: Optional storage backend for API keys
        """
        self.config = config
        self.storage = storage_backend or self._default_storage
        self._rate_limits = {}
    
    def generate_key(self, user_id: str, 
                    metadata: Optional[Dict[str, Any]] = None,
                    expires_in_days: Optional[int] = None) -> str:
        """
        Generate a new API key.
        
        Args:
            user_id: User ID associated with the key
            metadata: Additional metadata for the key
            expires_in_days: Custom expiration time
            
        Returns:
            API key string
        """
        # Generate secure random key
        raw_key = secrets.token_hex(self.config.key_length // 2)
        api_key = f"{self.config.key_prefix}{raw_key}"
        
        # Hash the key for storage
        key_hash = self._hash_key(api_key)
        
        # Set expiration
        expiry_days = expires_in_days or self.config.key_rotation_days
        expires_at = datetime.utcnow() + timedelta(days=expiry_days)
        
        # Create key record
        key_record = {
            "key_hash": key_hash,
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": expires_at.isoformat(),
            "metadata": metadata or {},
            "active": True,
            "last_used": None,
            "usage_count": 0
        }
        
        # Store the key
        self.storage("store", user_id, key_hash, key_record)
        
        return api_key
    
    def validate_key(self, api_key: str) -> Tuple[bool, Optional[Dict[str, Any]]]:
        """
        Validate an API key.
        
        Args:
            api_key: API key to validate
            
        Returns:
            Tuple of (is_valid, key_record)
        """
        # Check key format
        if not api_key.startswith(self.config.key_prefix):
            return False, None
        
        # Hash the key for lookup
        key_hash = self._hash_key(api_key)
        
        # Retrieve key record
        key_record = self.storage("get", key_hash=key_hash)
        if not key_record:
            return False, None
        
        # Check if key is active
        if not key_record.get("active", False):
            return False, key_record
        
        # Check expiration
        expires_at = datetime.fromisoformat(key_record["expires_at"])
        if datetime.utcnow() > expires_at:
            return False, key_record
        
        # Check rate limit
        if not self._check_rate_limit(api_key):
            raise RateLimitExceededError("Rate limit exceeded")
        
        # Update usage statistics
        key_record["last_used"] = datetime.utcnow().isoformat()
        key_record["usage_count"] = key_record.get("usage_count", 0) + 1
        self.storage("update", key_hash, key_record)
        
        return True, key_record
    
    def revoke_key(self, api_key: str) -> bool:
        """
        Revoke an API key.
        
        Args:
            api_key: API key to revoke
            
        Returns:
            True if revoked successfully
        """
        key_hash = self._hash_key(api_key)
        key_record = self.storage("get", key_hash=key_hash)
        
        if key_record:
            key_record["active"] = False
            key_record["revoked_at"] = datetime.utcnow().isoformat()
            self.storage("update", key_hash, key_record)
            return True
        
        return False
    
    def rotate_key(self, old_api_key: str) -> Optional[str]:
        """
        Rotate an API key by revoking the old one and generating a new one.
        
        Args:
            old_api_key: API key to rotate
            
        Returns:
            New API key or None if rotation failed
        """
        key_hash = self._hash_key(old_api_key)
        key_record = self.storage("get", key_hash=key_hash)
        
        if key_record:
            # Revoke old key
            self.revoke_key(old_api_key)
            
            # Generate new key with same user_id and metadata
            return self.generate_key(
                key_record["user_id"],
                key_record.get("metadata", {})
            )
        
        return None
    
    def _hash_key(self, api_key: str) -> str:
        """Hash an API key for secure storage."""
        return hashlib.sha256(api_key.encode()).hexdigest()
    
    def _check_rate_limit(self, api_key: str) -> bool:
        """Check rate limit for an API key."""
        if not self.config.rate_limit_requests:
            return True
        
        now = time.time()
        key_hash = self._hash_key(api_key)
        
        if key_hash not in self._rate_limits:
            self._rate_limits[key_hash] = []
        
        # Remove old requests outside the window
        window_start = now - self.config.rate_limit_window_seconds
        self._rate_limits[key_hash] = [
            t for t in self._rate_limits[key_hash] if t > window_start
        ]
        
        # Check if under limit
        if len(self._rate_limits[key_hash]) >= self.config.rate_limit_requests:
            return False
        
        # Add current request
        self._rate_limits[key_hash].append(now)
        return True
    
    def _default_storage(self, operation: str, *args, **kwargs):
        """Default in-memory storage implementation."""
        if not hasattr(self, "_storage_dict"):
            self._storage_dict = {}
        
        if operation == "store":
            user_id, key_hash, key_record = args
            self._storage_dict[key_hash] = key_record
        
        elif operation == "get":
            key_hash = kwargs.get("key_hash")
            return self._storage_dict.get(key_hash)
        
        elif operation == "update":
            key_hash, key_record = args
            self._storage_dict[key_hash] = key_record
        
        elif operation == "delete":
            key_hash = args[0]
            if key_hash in self._storage_dict:
                del self._storage_dict[key_hash]


def api_key_required(config: Optional[APIKeyConfig] = None,
                    storage_backend: Optional[Callable] = None):
    """
    Decorator for protecting routes with API key authentication.
    
    Args:
        config: API key configuration
        storage_backend: Storage backend for API keys
    """
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            # Framework-specific implementation needed
            request = kwargs.get("request")
            if not request:
                raise ValueError("Request object not found")
            
            # Extract API key from headers
            api_key = None
            
            # Check Authorization header
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                api_key = auth_header.split(" ")[1]
            
            # Check X-API-Key header
            if not api_key:
                api_key = request.headers.get("X-API-Key")
            
            # Check query parameter
            if not api_key:
                api_key = request.args.get("api_key")
            
            if not api_key:
                return {"error": "API key is required"}, 401
            
            # Validate API key
            try:
                manager = APIKeyManager(config or APIKeyConfig(), storage_backend)
                is_valid, key_record = manager.validate_key(api_key)
                
                if not is_valid:
                    return {"error": "Invalid or expired API key"}, 401
                
                # Add key info to request
                request.api_key = key_record
                
                return await f(*args, **kwargs)
                
            except RateLimitExceededError:
                return {"error": "Rate limit exceeded"}, 429
            except Exception as e:
                return {"error": "Authentication failed"}, 500
        
        return decorated_function
    
    return decorator


# Convenience functions
def generate_api_key(user_id: str, 
                    metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Convenience function to generate an API key.
    
    Args:
        user_id: User ID associated with the key
        metadata: Additional metadata
        
    Returns:
        API key string
    """
    manager = APIKeyManager(APIKeyConfig())
    return manager.generate_key(user_id, metadata)


def validate_api_key(api_key: str) -> bool:
    """
    Convenience function to validate an API key.
    
    Args:
        api_key: API key to validate
        
    Returns:
        True if valid
    """
    manager = APIKeyManager(APIKeyConfig())
    is_valid, _ = manager.validate_key(api_key)
    return is_valid