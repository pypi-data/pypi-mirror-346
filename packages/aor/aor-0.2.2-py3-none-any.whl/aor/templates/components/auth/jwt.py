"""
JWT authentication for AI-on-Rails.

Provides JWT token generation, validation, and middleware for API authentication.
"""

import jwt
import time
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from functools import wraps
import os
import json


@dataclass
class JWTConfig:
    """JWT configuration settings."""
    secret_key: str
    algorithm: str = "HS256"
    token_expiry_minutes: int = 60
    issuer: str = "ai-on-rails"
    audience: Optional[str] = None


class JWTError(Exception):
    """Base exception for JWT errors."""
    pass


class TokenExpiredError(JWTError):
    """Token has expired."""
    pass


class InvalidTokenError(JWTError):
    """Token is invalid."""
    pass


class JWTHandler:
    """
    Handles JWT operations including token creation and validation.
    """
    
    def __init__(self, config: JWTConfig):
        """
        Initialize JWT handler with configuration.
        
        Args:
            config: JWT configuration
        """
        self.config = config
        
        if not config.secret_key:
            raise ValueError("JWT secret key must be provided")
    
    def create_token(self, payload: Dict[str, Any], 
                    custom_claims: Optional[Dict[str, Any]] = None,
                    expiry_minutes: Optional[int] = None) -> str:
        """
        Create a JWT token.
        
        Args:
            payload: Token payload (user data)
            custom_claims: Additional claims to include
            expiry_minutes: Custom expiry time (overrides config)
            
        Returns:
            JWT token string
        """
        now = datetime.utcnow()
        expiry = now + timedelta(minutes=expiry_minutes or self.config.token_expiry_minutes)
        
        # Standard claims
        claims = {
            "iat": int(now.timestamp()),
            "exp": int(expiry.timestamp()),
            "iss": self.config.issuer,
            "nbf": int(now.timestamp()),
            "jti": self._generate_jti()
        }
        
        if self.config.audience:
            claims["aud"] = self.config.audience
        
        # Add payload data
        claims.update(payload)
        
        # Add custom claims
        if custom_claims:
            claims.update(custom_claims)
        
        # Create token
        token = jwt.encode(
            claims,
            self.config.secret_key,
            algorithm=self.config.algorithm
        )
        
        return token
    
    def validate_token(self, token: str) -> Dict[str, Any]:
        """
        Validate a JWT token and return the payload.
        
        Args:
            token: JWT token string
            
        Returns:
            Token payload
            
        Raises:
            TokenExpiredError: If token has expired
            InvalidTokenError: If token is invalid
        """
        try:
            # Decode and validate token
            payload = jwt.decode(
                token,
                self.config.secret_key,
                algorithms=[self.config.algorithm],
                issuer=self.config.issuer,
                audience=self.config.audience
            )
            
            return payload
            
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError(f"Invalid token: {str(e)}")
    
    def refresh_token(self, token: str) -> str:
        """
        Refresh a token by creating a new one with the same payload.
        
        Args:
            token: Existing JWT token
            
        Returns:
            New JWT token
        """
        try:
            # Decode existing token (without validating expiry)
            payload = jwt.decode(
                token,
                self.config.secret_key,
                algorithms=[self.config.algorithm],
                options={"verify_exp": False}
            )
            
            # Remove standard claims
            for claim in ["iat", "exp", "nbf", "jti"]:
                payload.pop(claim, None)
            
            # Create new token
            return self.create_token(payload)
            
        except jwt.InvalidTokenError as e:
            raise InvalidTokenError(f"Cannot refresh invalid token: {str(e)}")
    
    def _generate_jti(self) -> str:
        """Generate a unique JWT ID."""
        import uuid
        return str(uuid.uuid4())


def jwt_required(secret_key: str = None, algorithm: str = "HS256"):
    """
    Decorator for protecting routes with JWT authentication.
    
    Args:
        secret_key: JWT secret key (if not provided, uses environment variable)
        algorithm: JWT algorithm
    """
    def decorator(f):
        @wraps(f)
        async def decorated_function(*args, **kwargs):
            # Framework-specific implementation needed
            request = kwargs.get("request")
            if not request:
                raise ValueError("Request object not found")
            
            # Extract token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return {"error": "Missing or invalid authorization header"}, 401
            
            token = auth_header.split(" ")[1]
            
            # Validate token
            try:
                key = secret_key or os.environ.get("JWT_SECRET_KEY")
                if not key:
                    raise ValueError("JWT secret key not configured")
                
                config = JWTConfig(secret_key=key, algorithm=algorithm)
                handler = JWTHandler(config)
                payload = handler.validate_token(token)
                
                # Add user data to request
                request.user = payload
                
                return await f(*args, **kwargs)
                
            except TokenExpiredError:
                return {"error": "Token has expired"}, 401
            except InvalidTokenError as e:
                return {"error": str(e)}, 401
            except Exception as e:
                return {"error": "Authentication failed"}, 500
        
        return decorated_function
    
    return decorator


# Convenience functions
def create_jwt_token(payload: Dict[str, Any], 
                    secret_key: Optional[str] = None,
                    expiry_minutes: int = 60) -> str:
    """
    Convenience function to create a JWT token.
    
    Args:
        payload: Token payload
        secret_key: JWT secret key (if not provided, uses environment variable)
        expiry_minutes: Token expiry time in minutes
        
    Returns:
        JWT token string
    """
    key = secret_key or os.environ.get("JWT_SECRET_KEY")
    if not key:
        raise ValueError("JWT secret key not configured")
    
    config = JWTConfig(secret_key=key, token_expiry_minutes=expiry_minutes)
    handler = JWTHandler(config)
    return handler.create_token(payload)


def validate_jwt_token(token: str, 
                      secret_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to validate a JWT token.
    
    Args:
        token: JWT token string
        secret_key: JWT secret key (if not provided, uses environment variable)
        
    Returns:
        Token payload
    """
    key = secret_key or os.environ.get("JWT_SECRET_KEY")
    if not key:
        raise ValueError("JWT secret key not configured")
    
    config = JWTConfig(secret_key=key)
    handler = JWTHandler(config)
    return handler.validate_token(token)