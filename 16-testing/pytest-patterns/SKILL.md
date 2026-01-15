# Pytest Patterns

## Overview

Pytest is a powerful testing framework for Python that makes it easy to write simple yet scalable test cases. This skill covers pytest basics, fixtures, mocking, and best practices.

## Table of Contents

1. [Pytest Basics](#pytest-basics)
2. [Test Structure](#test-structure)
3. [Fixtures](#fixtures)
4. [Parametrization](#parametrization)
5. [Markers](#markers)
6. [Mocking](#mocking)
7. [Async Tests](#async-tests)
8. [Coverage](#coverage)
9. [Testing FastAPI](#testing-fastapi)
10. [Testing Database Code](#testing-database-code)
11. [Best Practices](#best-practices)

---

## Pytest Basics

### Installation

```bash
pip install pytest pytest-cov pytest-asyncio pytest-mock
```

### Basic Test

```python
# test_basic.py
def test_addition():
    """Test basic addition."""
    assert 1 + 1 == 2

def test_string_equality():
    """Test string equality."""
    assert "hello" == "hello"

def test_list_contains():
    """Test list contains."""
    assert 3 in [1, 2, 3]
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific file
pytest tests/test_user.py

# Run specific test
pytest tests/test_user.py::test_get_user

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html
```

---

## Test Structure

### Basic Structure

```python
# test_user.py
import pytest

from src.user import User

class TestUser:
    """Test User class."""

    def test_init(self):
        """Test User initialization."""
        user = User("John", "john@example.com")
        assert user.name == "John"
        assert user.email == "john@example.com"

    def test_full_name(self):
        """Test full name property."""
        user = User("John", "john@example.com")
        assert user.full_name == "John (john@example.com)"

    def test_validate_email(self):
        """Test email validation."""
        user = User("John", "invalid-email")
        assert not user.is_valid_email()
```

### Test Modules

```python
# test_user.py
import pytest

from src import user

def test_create_user():
    """Test user creation."""
    user = user.create("John", "john@example.com")
    assert user.id is not None
    assert user.name == "John"

def test_get_user():
    """Test getting user."""
    user = user.get(1)
    assert user is not None
    assert user.id == 1

def test_update_user():
    """Test user update."""
    user = user.update(1, name="Jane")
    assert user.name == "Jane"

def test_delete_user():
    """Test user deletion."""
    user = user.delete(1)
    assert user is None
```

---

## Fixtures

### Basic Fixture

```python
# conftest.py
import pytest
from src.database import Database

@pytest.fixture
def db():
    """Database fixture."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

# test_user.py
def test_create_user(db):
    """Test user creation with database."""
    user = db.create_user("John", "john@example.com")
    assert user.id is not None
```

### Fixture with Parameters

```python
# conftest.py
import pytest

@pytest.fixture(params=["John", "Jane", "Alice"])
def user(request):
    """User fixture with parameters."""
    return {"name": request.param, "email": f"{request.param.lower()}@example.com"}

# test_user.py
def test_user_creation(user):
    """Test user creation."""
    assert user["name"] is not None
    assert "@" in user["email"]
```

### Fixture with Scope

```python
# conftest.py
import pytest

@pytest.fixture(scope="session")
def session_db():
    """Session-scoped database fixture."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture(scope="function")
def function_db():
    """Function-scoped database fixture."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()
```

### Fixture with Autouse

```python
# conftest.py
import pytest

@pytest.fixture(autouse=True)
def setup_database():
    """Setup database before each test."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()
```

---

## Parametrization

### Basic Parametrization

```python
# test_math.py
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (2, 3, 5),
    (3, 4, 7),
])
def test_addition(a, b, expected):
    """Test addition with parametrization."""
    assert a + b == expected
```

### Multiple Parameters

```python
# test_string.py
import pytest

@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("world", "WORLD"),
    ("test", "TEST"),
])
def test_uppercase(input, expected):
    """Test uppercase function."""
    assert input.upper() == expected
```

### Parametrize with IDs

```python
# test_numbers.py
import pytest

@pytest.mark.parametrize("input,expected", [
    pytest.param(1, 2, id="1+1=2"),
    pytest.param(2, 3, id="2+1=3"),
    pytest.param(3, 4, id="3+1=4"),
])
def test_addition(input, expected):
    """Test addition with parametrization IDs."""
    assert input + 1 == expected
```

---

## Markers

### Basic Markers

```python
# test_api.py
import pytest

@pytest.mark.unit
def test_user_creation():
    """Unit test for user creation."""
    assert True

@pytest.mark.integration
def test_api_user_creation():
    """Integration test for API user creation."""
    assert True
```

### Marker Configuration

```python
# pytest.ini
[pytest]
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests
```

### Running Marked Tests

```bash
# Run only unit tests
pytest -m unit

# Skip slow tests
pytest -m "not slow"

# Run integration tests
pytest -m integration
```

### Skip Marker

```python
# test_slow.py
import pytest

@pytest.mark.slow
def test_slow_operation():
    """Slow operation test."""
    import time
    time.sleep(10)
    assert True

@pytest.mark.skip(reason="Feature not implemented")
def test_unimplemented_feature():
    """Test for unimplemented feature."""
    assert True
```

---

## Mocking

### Mocking Functions

```python
# test_utils.py
import pytest
from src.utils import send_email
from unittest.mock import patch

def test_send_email(mocker):
    """Test email sending with mock."""
    mocker.patch('src.utils.smtp.sendmail')
    mock_sendmail = mocker.Mock()
    
    send_email("test@example.com", "Test subject", "Test body")
    
    mock_sendmail.assert_called_once()
    mock_sendmail.assert_called_with(
        "test@example.com",
        "Test subject",
        "Test body"
    )
```

### Mocking Classes

```python
# test_service.py
import pytest
from src.service import UserService
from unittest.mock import Mock

@pytest.fixture
def mock_user_service():
    """Mock user service."""
    return Mock(spec=UserService)

def test_get_user(mock_user_service):
    """Test getting user with mock service."""
    mock_user_service.get_user.return_value = {
        "id": 1,
        "name": "John",
        "email": "john@example.com"
    }
    
    service = UserService(mock_user_service)
    user = service.get_user(1)
    
    assert user["id"] == 1
    assert user["name"] == "John"
    mock_user_service.get_user.assert_called_once_with(1)
```

### Mocking External APIs

```python
# test_external_api.py
import pytest
import requests
from unittest.mock import patch

def test_external_api(mocker):
    """Test external API call with mock."""
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"data": "test"}
    mocker.patch('requests.get', return_value=mock_response)
    
    response = requests.get("https://api.example.com/data")
    
    assert response.json()["data"] == "test"
    mock_response.json.assert_called_once()
```

---

## Async Tests

### Async Test

```python
# test_async.py
import pytest

@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""
    result = await async_function()
    assert result == "success"

async def async_function():
    """Async function to test."""
    return "success"
```

### Async Fixture

```python
# conftest.py
import pytest
import asyncio

@pytest.fixture
async def async_db():
    """Async database fixture."""
    db = AsyncDatabase()
    await db.connect()
    yield db
    await db.disconnect()

# test_async_user.py
@pytest.mark.asyncio
async def test_async_create_user(async_db):
    """Test async user creation."""
    user = await async_db.create_user("John", "john@example.com")
    assert user.id is not None
```

---

## Coverage

### Coverage Configuration

```ini
# pytest.ini
[pytest]
addopts = --cov=src --cov-report=html --cov-report=term
```

### Running Coverage

```bash
# Run tests with coverage
pytest --cov=src --cov-report=html

# Generate coverage report
pytest --cov=src --cov-report=xml
```

### Coverage Exclusions

```ini
# pytest.ini
[pytest]
addopts = --cov=src --cov-report=html --cov-report=term
[coverage:run]
omit =
    */tests/*
    */conftest.py
    */__init__.py
```

---

## Testing FastAPI

### Basic API Test

```python
# test_main.py
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_read_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_user():
    """Test user creation endpoint."""
    response = client.post(
        "/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    assert response.status_code == 201
    assert response.json()["name"] == "John"
```

### Test with Database

```python
# test_users.py
from fastapi.testclient import TestClient
from src.main import app
from src.database import Database

client = TestClient(app)

@pytest.fixture
def db():
    """Database fixture."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

def test_create_user(db):
    """Test user creation with database."""
    response = client.post(
        "/users/",
        json={"name": "John", "email": "john@example.com"}
    )
    assert response.status_code == 201
    
    user = db.get_user(response.json()["id"])
    assert user is not None
    assert user["name"] == "John"
```

### Test Authentication

```python
# test_auth.py
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_protected_endpoint():
    """Test protected endpoint without auth."""
    response = client.get("/users/me")
    assert response.status_code == 401

def test_protected_endpoint_with_auth():
    """Test protected endpoint with auth."""
    headers = {"Authorization": "Bearer test-token"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
```

---

## Testing Database Code

### Model Tests

```python
# test_models.py
import pytest
from src.models import User

def test_user_creation():
    """Test user model creation."""
    user = User(name="John", email="john@example.com")
    assert user.id is None
    assert user.name == "John"
    assert user.email == "john@example.com"

def test_user_validation():
    """Test user email validation."""
    user = User(name="John", email="invalid-email")
    assert not user.is_valid_email()
```

### Repository Tests

```python
# test_repositories.py
import pytest
from src.repositories import UserRepository
from src.models import User

@pytest.fixture
def db():
    """Database fixture."""
    from src.database import Database
    db = Database()
    db.connect()
    yield db
    db.disconnect()

def test_create_user(db):
    """Test user repository create."""
    repo = UserRepository(db)
    user = repo.create("John", "john@example.com")
    assert user.id is not None
    assert user.name == "John"

def test_get_user(db):
    """Test user repository get."""
    repo = UserRepository(db)
    user = repo.create("Jane", "jane@example.com")
    retrieved_user = repo.get(user.id)
    assert retrieved_user.id == user.id
    assert retrieved_user.name == "Jane"
```

### Transaction Tests

```python
# test_transactions.py
import pytest
from src.repositories import UserRepository
from src.models import User

@pytest.fixture
def db():
    """Database fixture."""
    from src.database import Database
    db = Database()
    db.connect()
    yield db
    db.disconnect()

def test_transaction(db):
    """Test database transaction."""
    repo = UserRepository(db)
    
    with db.transaction():
        user1 = repo.create("John", "john@example.com")
        user2 = repo.create("Jane", "jane@example.com")
        user1.name = "Updated"
        user2.name = "Updated"
        db.commit()
    
    assert repo.get(user1.id).name == "Updated"
    assert repo.get(user2.id).name == "Updated"
```

---

## Best Practices

### 1. Use Descriptive Test Names

```python
# Good
def test_create_user_with_valid_email():
    """Test user creation with valid email."""
    pass

def test_create_user_with_invalid_email():
    """Test user creation with invalid email."""
    pass

# Bad
def test_1():
    """Test user creation."""
    pass
```

### 2. Use Fixtures Effectively

```python
# Good
@pytest.fixture
def user():
    """User fixture."""
    return User("John", "john@example.com")

def test_user_name(user):
    """Test user name."""
    assert user.name == "John"

# Bad
def test_user_name():
    """Test user name."""
    user = User("John", "john@example.com")
    assert user.name == "John"
```

### 3. Use Parametrization

```python
# Good
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 3),
    (3, 4),
])
def test_addition(input, expected):
    """Test addition."""
    assert input + 1 == expected

# Bad
def test_addition_1():
    assert 1 + 1 == 2

def test_addition_2():
    assert 2 + 1 == 3

def test_addition_3():
    assert 3 + 1 == 4
```

### 4. Use Markers

```python
# Good
@pytest.mark.unit
def test_user_creation():
    """Unit test for user creation."""
    pass

@pytest.mark.integration
def test_api_user_creation():
    """Integration test for API user creation."""
    pass

# Bad
def test_user_creation_unit():
    """Unit test for user creation."""
    pass

def test_api_user_creation_integration():
    """Integration test for API user creation."""
    pass
```

### 5. Test One Thing Per Test

```python
# Good
def test_user_name():
    """Test user name."""
    user = User("John", "john@example.com")
    assert user.name == "John"

def test_user_email():
    """Test user email."""
    user = User("John", "john@example.com")
    assert user.email == "john@example.com"

# Bad
def test_user():
    """Test user."""
    user = User("John", "john@example.com")
    assert user.name == "John"
    assert user.email == "john@example.com"
```

---

## Summary

This skill covers comprehensive pytest testing patterns including:

- **Pytest Basics**: Installation, basic tests, running tests
- **Test Structure**: Basic structure, test modules
- **Fixtures**: Basic fixtures, parameters, scope, autouse
- **Parametrization**: Basic, multiple parameters, IDs
- **Markers**: Basic markers, configuration, running, skip
- **Mocking**: Functions, classes, external APIs
- **Async Tests**: Async functions and fixtures
- **Coverage**: Configuration, running, exclusions
- **Testing FastAPI**: Basic API tests, database tests, authentication
- **Testing Database Code**: Models, repositories, transactions
- **Best Practices**: Descriptive names, fixtures, parametrization, markers, one thing per test
