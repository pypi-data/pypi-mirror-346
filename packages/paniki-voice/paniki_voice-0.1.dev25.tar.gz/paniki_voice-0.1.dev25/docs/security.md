# Security Guide

## Overview

This guide covers security best practices for deploying and using Paniki in production environments.

## Authentication and Authorization

### API Key Management

```python
from paniki.utils.security import APIKeyManager

class SecureAPIKeyManager(APIKeyManager):
    def __init__(self, key_rotation_days=30):
        self.key_rotation_days = key_rotation_days
        
    def rotate_keys(self):
        """Implement key rotation logic."""
        pass
        
    def validate_key(self, api_key):
        """Validate API key."""
        pass
```

### JWT Authentication

```python
from paniki.utils.security import JWTAuthenticator
import jwt

class TokenAuthenticator:
    def __init__(self, secret_key):
        self.secret_key = secret_key
        
    def create_token(self, user_id, expiry=3600):
        """Create JWT token."""
        return jwt.encode(
            {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=expiry)
            },
            self.secret_key,
            algorithm='HS256'
        )
        
    def validate_token(self, token):
        """Validate JWT token."""
        try:
            return jwt.decode(
                token,
                self.secret_key,
                algorithms=['HS256']
            )
        except jwt.InvalidTokenError:
            return None
```

## Secure Communication

### SSL/TLS Configuration

```python
import ssl
from aiohttp import web

def create_ssl_context():
    """Create SSL context for secure communication."""
    ssl_context = ssl.create_default_context(
        purpose=ssl.Purpose.CLIENT_AUTH
    )
    ssl_context.load_cert_chain(
        certfile='path/to/cert.pem',
        keyfile='path/to/key.pem'
    )
    return ssl_context

app = web.Application()
web.run_app(
    app,
    ssl_context=create_ssl_context(),
    host='0.0.0.0',
    port=443
)
```

### WebSocket Security

```python
from paniki.transports.network.websocket_server import SecureWebSocketServer

class SecureWebSocketServer(WebSocketServer):
    def __init__(self, ssl_context, **kwargs):
        super().__init__(**kwargs)
        self.ssl_context = ssl_context
        
    async def authenticate_client(self, request):
        """Authenticate WebSocket client."""
        token = request.headers.get('Authorization')
        if not token:
            raise web.HTTPUnauthorized()
        # Validate token
        return await self.validate_token(token)
```

## Data Protection

### Encryption at Rest

```python
from cryptography.fernet import Fernet
from paniki.utils.security import DataEncryptor

class SecureDataHandler:
    def __init__(self, encryption_key):
        self.fernet = Fernet(encryption_key)
        
    def encrypt_data(self, data):
        """Encrypt sensitive data."""
        return self.fernet.encrypt(data.encode())
        
    def decrypt_data(self, encrypted_data):
        """Decrypt sensitive data."""
        return self.fernet.decrypt(encrypted_data).decode()
```

### Secure Frame Handling

```python
from paniki.frames import SecureFrame
from typing import Optional

class SecureAudioFrame(SecureFrame):
    def __init__(self, data: bytes, encryption_key: bytes):
        self.encryption_key = encryption_key
        self.encrypted_data = self.encrypt_data(data)
        
    def encrypt_data(self, data: bytes) -> bytes:
        """Encrypt frame data."""
        pass
        
    def decrypt_data(self) -> bytes:
        """Decrypt frame data."""
        pass
```

## Access Control

### Role-Based Access Control

```python
from enum import Enum
from typing import List

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class AccessControl:
    def __init__(self):
        self.role_permissions = {
            Role.ADMIN: ["read", "write", "delete"],
            Role.USER: ["read", "write"],
            Role.GUEST: ["read"]
        }
        
    def check_permission(self, role: Role, action: str) -> bool:
        """Check if role has permission for action."""
        return action in self.role_permissions.get(role, [])
```

### Resource Access Control

```python
class ResourceAccessManager:
    def __init__(self):
        self.resource_permissions = {}
        
    def grant_access(self, user_id: str, resource_id: str):
        """Grant access to resource."""
        if user_id not in self.resource_permissions:
            self.resource_permissions[user_id] = set()
        self.resource_permissions[user_id].add(resource_id)
        
    def check_access(self, user_id: str, resource_id: str) -> bool:
        """Check if user has access to resource."""
        return resource_id in self.resource_permissions.get(user_id, set())
```

## Audit Logging

### Security Event Logging

```python
from loguru import logger
import json

class SecurityAuditor:
    def __init__(self, log_file="security.log"):
        self.logger = logger
        self.logger.add(log_file, rotation="1 day")
        
    def log_security_event(self, event_type: str, details: dict):
        """Log security event."""
        self.logger.info(json.dumps({
            "type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details
        }))
```

### Access Logging

```python
class AccessLogger:
    def __init__(self):
        self.logger = logger
        
    async def log_access(self, request, response):
        """Log access attempt."""
        self.logger.info({
            "timestamp": datetime.utcnow().isoformat(),
            "ip": request.remote,
            "method": request.method,
            "path": request.path,
            "status": response.status
        })
```

## Security Best Practices

### Input Validation

```python
from pydantic import BaseModel, validator
from typing import Optional

class UserInput(BaseModel):
    text: str
    language: Optional[str] = "en"
    
    @validator('text')
    def validate_text(cls, v):
        """Validate text input."""
        if len(v) > 1000:
            raise ValueError("Text too long")
        if not v.isprintable():
            raise ValueError("Invalid characters in text")
        return v
```

### Rate Limiting

```python
from paniki.utils.security import RateLimiter

class APIRateLimiter:
    def __init__(self, requests_per_minute=60):
        self.rate_limiter = RateLimiter(
            max_requests=requests_per_minute,
            time_window=60
        )
        
    async def check_rate_limit(self, client_id: str) -> bool:
        """Check if client has exceeded rate limit."""
        return await self.rate_limiter.check_limit(client_id)
```

### Error Handling

```python
class SecurityError(Exception):
    """Base class for security errors."""
    pass

class AuthenticationError(SecurityError):
    """Authentication related errors."""
    pass

class AuthorizationError(SecurityError):
    """Authorization related errors."""
    pass

def handle_security_error(error: SecurityError):
    """Handle security errors."""
    if isinstance(error, AuthenticationError):
        # Handle authentication error
        pass
    elif isinstance(error, AuthorizationError):
        # Handle authorization error
        pass
```

## Deployment Security

### Container Security

```dockerfile
# Use specific version
FROM python:3.10-slim

# Run as non-root user
RUN useradd -m -s /bin/bash paniki
USER paniki

# Set secure permissions
RUN chmod 600 /app/config/secrets.json

# Use secure base image
FROM gcr.io/distroless/python3
```

### Environment Variables

```python
from paniki.utils.security import SecretManager

class EnvironmentSecrets:
    def __init__(self):
        self.secret_manager = SecretManager()
        
    def load_secrets(self):
        """Load secrets from environment."""
        return {
            'api_key': self.secret_manager.get_secret('API_KEY'),
            'jwt_secret': self.secret_manager.get_secret('JWT_SECRET'),
            'db_password': self.secret_manager.get_secret('DB_PASSWORD')
        }
```

### Network Security

```python
from paniki.utils.security import FirewallRules

class NetworkSecurity:
    def __init__(self):
        self.firewall = FirewallRules()
        
    def configure_firewall(self):
        """Configure network security rules."""
        self.firewall.allow_port(443)  # HTTPS
        self.firewall.allow_port(8080)  # WebSocket
        self.firewall.deny_all_other_ports()
```