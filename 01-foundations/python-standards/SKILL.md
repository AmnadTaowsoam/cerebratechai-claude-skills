# Python Coding Standards

## Overview
มาตรฐานการเขียน Python สำหรับ Backend และ AI/ML Projects
รองรับ Python 3.11+

## Core Principles
- PEP 8 Compliance
- Type Hints Always
- Explicit is Better Than Implicit
- Fail Fast with Clear Error Messages

## Python Version & Setup

### pyproject.toml (Modern Python)
```toml
[project]
name = "your-project"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "black>=23.0.0",
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]

[tool.black]
line-length = 88
target-version = ['py311']

[tool.ruff]
line-length = 88
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
```

## Naming Conventions

### Variables & Functions
```python
# ❌ Bad
UserData = {}
def Get_User(): pass
def getUserData(): pass  # camelCase is not Pythonic

# ✅ Good
user_data = {}
def get_user(): pass
def get_user_data(): pass
```

### Classes
```python
# ❌ Bad
class user_service: pass
class userService: pass

# ✅ Good
class UserService: pass
class HTTPRequestHandler: pass
```

### Constants
```python
# ❌ Bad
apiKey = "..."
max_retries = 3

# ✅ Good
API_KEY = "..."
MAX_RETRIES = 3
DATABASE_URL = "postgresql://..."
```

### Private vs Public
```python
class UserService:
    # Public attribute
    name: str
    
    # Protected (internal use, subclasses OK)
    _cache: dict[str, Any]
    
    # Private (name mangling)
    __secret_key: str
    
    def public_method(self) -> None:
        pass
    
    def _internal_helper(self) -> None:
        """Used internally, but subclasses can override."""
        pass
    
    def __private_method(self) -> None:
        """Truly private, name mangled."""
        pass
```

## Type Hints

### Basic Types
```python
from typing import Any

# ❌ Bad - no type hints
def process_data(data):
    return data

# ✅ Good
def process_data(data: str | int) -> str:
    return str(data)

# ✅ Generic types
from typing import TypeVar

T = TypeVar("T")

def get_first(items: list[T]) -> T | None:
    return items[0] if items else None
```

### Modern Python 3.10+ Syntax
```python
# ❌ Old style (Python 3.9)
from typing import Optional, Union, List, Dict

def get_user(user_id: str) -> Optional[Dict[str, Union[str, int]]]:
    pass

# ✅ New style (Python 3.10+)
def get_user(user_id: str) -> dict[str, str | int] | None:
    pass

# ✅ List, Dict, Set, Tuple
def process_users(
    user_ids: list[str],
    metadata: dict[str, Any],
    tags: set[str],
    coords: tuple[float, float],
) -> list[dict[str, Any]]:
    pass
```

### Pydantic Models (Recommended)
```python
from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime

class User(BaseModel):
    """User model with validation."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        frozen=False,  # Set to True for immutable
    )
    
    id: str
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    tags: list[str] = Field(default_factory=list)
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v.endswith(("@company.com", "@example.com")):
            raise ValueError("Must be company email")
        return v.lower()

# Usage
user = User(
    id="123",
    email="John.Doe@Company.COM",
    name="John Doe",
    age=30,
)
print(user.email)  # john.doe@company.com (validated & normalized)
```

## Error Handling

### Custom Exceptions
```python
class AppException(Exception):
    """Base exception for application errors."""
    
    def __init__(
        self,
        message: str,
        code: str,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class ValidationException(AppException):
    """Raised when validation fails."""
    
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
            details=details,
        )


class NotFoundException(AppException):
    """Raised when resource not found."""
    
    def __init__(self, resource: str, resource_id: str) -> None:
        super().__init__(
            message=f"{resource} with id {resource_id} not found",
            code="NOT_FOUND",
            status_code=404,
        )
```

### Try-Except Patterns
```python
# ❌ Bad - bare except
try:
    result = risky_operation()
except:
    print("Error occurred")

# ❌ Bad - catching too broad
try:
    result = risky_operation()
except Exception as e:
    print(e)

# ✅ Good - specific exceptions
try:
    result = risky_operation()
except ValueError as e:
    logger.error(f"Invalid value: {e}")
    raise ValidationException(str(e)) from e
except FileNotFoundError as e:
    logger.error(f"File not found: {e}")
    raise NotFoundException("File", str(e)) from e
except Exception as e:
    logger.exception("Unexpected error in risky_operation")
    raise AppException("Internal error", "INTERNAL_ERROR") from e

# ✅ Good - using else and finally
try:
    result = risky_operation()
except ValueError as e:
    handle_error(e)
else:
    # Runs only if no exception
    process_success(result)
finally:
    # Always runs
    cleanup()
```

### Context Managers
```python
from contextlib import contextmanager
from typing import Generator

# ✅ Custom context manager
@contextmanager
def database_transaction() -> Generator[None, None, None]:
    """Context manager for database transactions."""
    try:
        db.begin()
        yield
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Transaction failed: {e}")
        raise
    finally:
        db.close()

# Usage
with database_transaction():
    db.insert_user(user)
    db.insert_profile(profile)
```

## Async/Await Best Practices
```python
import asyncio
from typing import Coroutine

# ❌ Bad - not actually async
async def fetch_user(user_id: str) -> User:
    return db.get_user(user_id)  # Blocking call!

# ✅ Good - properly async
async def fetch_user(user_id: str) -> User:
    return await db_async.get_user(user_id)

# ✅ Parallel execution
async def fetch_multiple_users(user_ids: list[str]) -> list[User]:
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)

# ✅ With error handling
async def safe_fetch_user(user_id: str) -> User | None:
    try:
        return await fetch_user(user_id)
    except NotFoundException:
        logger.warning(f"User {user_id} not found")
        return None
    except Exception as e:
        logger.error(f"Error fetching user {user_id}: {e}")
        raise
```

## Logging
```python
import logging
from typing import Any

# Setup logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# ❌ Bad - using print
def process_order(order_id: str) -> None:
    print(f"Processing order {order_id}")
    try:
        result = process(order_id)
        print(f"Order processed: {result}")
    except Exception as e:
        print(f"Error: {e}")

# ✅ Good - using logger with context
def process_order(order_id: str) -> None:
    logger.info("Processing order", extra={"order_id": order_id})
    try:
        result = process(order_id)
        logger.info(
            "Order processed successfully",
            extra={"order_id": order_id, "result": result},
        )
    except Exception as e:
        logger.exception(
            "Failed to process order",
            extra={"order_id": order_id},
        )
        raise

# ✅ Structured logging helper
def log_with_context(
    level: str,
    message: str,
    **context: Any,
) -> None:
    """Log with structured context."""
    log_func = getattr(logger, level.lower())
    log_func(message, extra=context)

# Usage
log_with_context("info", "User logged in", user_id="123", ip="1.2.3.4")
```

## Function Patterns

### Dependency Injection
```python
from typing import Protocol

# ❌ Bad - tight coupling
class UserService:
    def __init__(self) -> None:
        self.db = Database()  # Hard-coded dependency
    
    def get_user(self, user_id: str) -> User:
        return self.db.users.find_one(user_id)

# ✅ Good - dependency injection with Protocol
class DatabaseProtocol(Protocol):
    """Database interface."""
    
    def find_user(self, user_id: str) -> User | None:
        ...

class UserService:
    def __init__(self, db: DatabaseProtocol) -> None:
        self._db = db
    
    def get_user(self, user_id: str) -> User:
        user = self._db.find_user(user_id)
        if user is None:
            raise NotFoundException("User", user_id)
        return user

# Usage
db = Database()
service = UserService(db)
```

### Dataclasses vs Pydantic
```python
from dataclasses import dataclass, field
from datetime import datetime

# ✅ Use dataclass for internal data structures (no validation needed)
@dataclass(frozen=True)  # immutable
class Point:
    x: float
    y: float
    
    def distance_from_origin(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

# ✅ Use Pydantic for API models (with validation)
from pydantic import BaseModel, Field

class CreateUserRequest(BaseModel):
    """API request model."""
    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    name: str = Field(..., min_length=1)
    age: int = Field(..., ge=0)
```

## File Organization
```
src/
├── core/
│   ├── __init__.py
│   ├── config.py          # Configuration
│   ├── exceptions.py      # Custom exceptions
│   └── logging.py         # Logging setup
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── base.py
├── services/
│   ├── __init__.py
│   └── user_service.py
├── api/
│   ├── __init__.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── users.py
│   └── dependencies.py
└── utils/
    ├── __init__.py
    └── helpers.py
```

## Import Organization
```python
"""Module docstring."""

# 1. Standard library
import logging
import os
from datetime import datetime
from typing import Any

# 2. Third-party packages
import fastapi
from pydantic import BaseModel
from sqlalchemy import select

# 3. Local imports (absolute)
from app.core.config import settings
from app.core.exceptions import AppException
from app.models.user import User
from app.services.user_service import UserService

# 4. Relative imports (if needed)
from .dependencies import get_db
from .schemas import UserResponse
```

## Environment Variables
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn

class Settings(BaseSettings):
    """Application settings with validation."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )
    
    # App
    app_name: str = "My App"
    debug: bool = False
    environment: str = Field(default="development", pattern="^(development|staging|production)$")
    
    # Database
    database_url: PostgresDsn
    db_pool_size: int = Field(default=10, ge=1, le=100)
    
    # API
    api_key: str = Field(..., min_length=32)
    api_rate_limit: int = Field(default=100, ge=1)
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"

# Singleton instance
settings = Settings()

# Usage
print(settings.database_url)  # Fully validated PostgreSQL URL
print(settings.is_production)  # False
```

## Testing Patterns
```python
import pytest
from unittest.mock import Mock, patch, AsyncMock

# ✅ Fixture
@pytest.fixture
def sample_user() -> User:
    """Create a sample user for testing."""
    return User(
        id="test-123",
        email="test@example.com",
        name="Test User",
        age=30,
    )

# ✅ Parametrize
@pytest.mark.parametrize(
    "age,expected",
    [
        (17, False),
        (18, True),
        (100, True),
    ],
)
def test_is_adult(age: int, expected: bool) -> None:
    assert is_adult(age) == expected

# ✅ Async test
@pytest.mark.asyncio
async def test_fetch_user() -> None:
    user = await fetch_user("123")
    assert user.id == "123"

# ✅ Mocking
def test_user_service_with_mock() -> None:
    # Mock database
    mock_db = Mock()
    mock_db.find_user.return_value = User(
        id="123",
        email="test@example.com",
        name="Test",
        age=25,
    )
    
    # Test service
    service = UserService(mock_db)
    user = service.get_user("123")
    
    assert user.id == "123"
    mock_db.find_user.assert_called_once_with("123")
```

## Code Quality Tools

### Black (Formatter)
```bash
black src/
black --check src/  # CI/CD
```

### Ruff (Linter - Fast)
```bash
ruff check src/
ruff check --fix src/
```

### Mypy (Type Checker)
```bash
mypy src/
```

### Pre-commit Configuration
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies: [pydantic>=2.0.0]
```

## Common Patterns Checklist

When writing Python code, ensure:
- [ ] All functions have type hints (args + return)
- [ ] Using Python 3.10+ syntax (`list[str]` not `List[str]`)
- [ ] Pydantic models for API/external data
- [ ] Dataclasses for internal structures
- [ ] Custom exceptions for error handling
- [ ] Proper logging (not print statements)
- [ ] Environment variables validated with Pydantic
- [ ] Async/await where appropriate
- [ ] Code formatted with Black
- [ ] Type-checked with Mypy
- [ ] No bare `except:` clauses