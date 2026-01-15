# Pytest Patterns

A comprehensive guide to pytest testing patterns for Python applications.

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
# Install pytest
pip install pytest

# Install with plugins
pip install pytest pytest-asyncio pytest-cov pytest-mock

# Install for async testing
pip install pytest-asyncio

# Install for coverage
pip install pytest-cov
```

### Configuration

```ini
# pytest.ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_user.py

# Run specific test function
pytest tests/test_user.py::test_create_user

# Run tests matching pattern
pytest -k "test_create"

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=src --cov-report=html

# Run tests with markers
pytest -m unit
pytest -m "not slow"

# Stop on first failure
pytest -x

# Show local variables on failure
pytest -l

# Run failed tests only
pytest --lf
```

---

## Test Structure

### Basic Test Function

```python
# tests/test_calculator.py
def test_add():
    result = add(2, 3)
    assert result == 5

def test_subtract():
    result = subtract(5, 3)
    assert result == 2
```

### Test Class

```python
# tests/test_calculator.py
class TestCalculator:
    def test_add(self):
        result = add(2, 3)
        assert result == 5

    def test_subtract(self):
        result = subtract(5, 3)
        assert result == 2
```

### Test Organization

```
tests/
├── unit/
│   ├── test_user.py
│   ├── test_calculator.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   └── test_database.py
└── conftest.py
```

---

## Fixtures

### Basic Fixture

```python
import pytest

@pytest.fixture
def user():
    return {
        'id': 1,
        'name': 'John Doe',
        'email': 'john@example.com'
    }

def test_user_name(user):
    assert user['name'] == 'John Doe'
```

### Fixture with Setup and Teardown

```python
@pytest.fixture
def database():
    # Setup
    db = Database()
    db.connect()

    yield db

    # Teardown
    db.disconnect()
    db.cleanup()

def test_database_query(database):
    result = database.query('SELECT * FROM users')
    assert len(result) > 0
```

### Fixture Scope

```python
# Function scope (default)
@pytest.fixture(scope='function')
def temp_file():
    with open('temp.txt', 'w') as f:
        f.write('test')
    yield 'temp.txt'
    os.remove('temp.txt')

# Module scope
@pytest.fixture(scope='module')
def module_resource():
    resource = Resource()
    resource.initialize()
    yield resource
    resource.cleanup()

# Session scope
@pytest.fixture(scope='session')
def session_resource():
    resource = SessionResource()
    resource.initialize()
    yield resource
    resource.cleanup()
```

### Fixture with Parameters

```python
@pytest.fixture(params=['postgres', 'mysql', 'sqlite'])
def database(request):
    return Database(request.param)

def test_database_connection(database):
    assert database.connect() is True
```

### Fixture Dependencies

```python
@pytest.fixture
def user():
    return User(id=1, name='John Doe')

@pytest.fixture
def post(user):
    return Post(id=1, title='Test Post', author=user)

def test_post_author(post):
    assert post.author.name == 'John Doe'
```

### Using Fixtures in Classes

```python
@pytest.mark.usefixtures('database')
class TestDatabase:
    def test_query(self, database):
        result = database.query('SELECT * FROM users')
        assert len(result) > 0

    def test_insert(self, database):
        database.insert('INSERT INTO users VALUES (1, "John")')
        assert database.count() == 1
```

---

## Parametrization

### Basic Parametrization

```python
import pytest

@pytest.mark.parametrize('a, b, expected', [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Parametrize with IDs

```python
@pytest.mark.parametrize('a, b, expected', [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
], ids=['positive', 'zero', 'mixed'])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Parametrize with Fixtures

```python
@pytest.fixture(params=['postgres', 'mysql'])
def database(request):
    return Database(request.param)

@pytest.mark.parametrize('user_id', [1, 2, 3])
def test_get_user(database, user_id):
    user = database.get_user(user_id)
    assert user is not None
```

### Parametrize from File

```python
import json
import pytest

# Load test data from JSON file
with open('test_data.json') as f:
    test_data = json.load(f)

@pytest.mark.parametrize('data', test_data)
def test_with_data(data):
    assert validate(data['input']) == data['expected']
```

---

## Markers

### Defining Markers

```python
# pytest.ini
[pytest]
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### Using Markers

```python
import pytest

@pytest.mark.unit
def test_unit_function():
    assert add(2, 3) == 5

@pytest.mark.integration
def test_integration():
    response = requests.get('https://api.example.com')
    assert response.status_code == 200

@pytest.mark.slow
def test_slow_operation():
    result = slow_operation()
    assert result is not None
```

### Multiple Markers

```python
@pytest.mark.unit
@pytest.mark.slow
def test_slow_unit():
    assert slow_calculation() is not None
```

### Running Tests with Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Run tests not marked as slow
pytest -m "not slow"

# Run tests with multiple markers
pytest -m "unit and not slow"
```

### Skip and Xfail Markers

```python
@pytest.mark.skip(reason="Not implemented yet")
def test_not_implemented():
    pass

@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
def test_python38_feature():
    pass

@pytest.mark.xfail(reason="Known issue")
def test_known_failure():
    assert False

@pytest.mark.xfail(raises=ValueError)
def test_expected_failure():
    raise ValueError("Expected error")
```

---

## Mocking

### Basic Mocking

```python
from unittest.mock import Mock, patch

def test_with_mock():
    mock_func = Mock(return_value=42)
    result = mock_func()
    assert result == 42
    mock_func.assert_called_once()
```

### Patching

```python
from unittest.mock import patch

def test_external_api():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        response = external_api_call()
        assert response == 200
        mock_get.assert_called_once()
```

### Patching with Side Effects

```python
def test_with_side_effect():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = [200, 404, 500]

        assert external_api_call() == 200
        assert external_api_call() == 404
        assert external_api_call() == 500
```

### Mocking Classes

```python
def test_class_mock():
    with patch('myapp.Database') as MockDatabase:
        mock_db = MockDatabase.return_value
        mock_db.query.return_value = [{'id': 1}]

        result = get_users()
        assert result == [{'id': 1}]
```

### Mocking Async Functions

```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_async_mock():
    with patch('myapp.async_function', new_callable=AsyncMock()) as mock_func:
        mock_func.return_value = 42
        result = await async_function()
        assert result == 42
```

### Pytest Mock Fixture

```python
@pytest.fixture
def mock_database():
    with patch('myapp.Database') as MockDatabase:
        mock_db = MockDatabase.return_value
        mock_db.connect.return_value = True
        mock_db.query.return_value = [{'id': 1}]
        yield mock_db

def test_with_mock_database(mock_database):
    result = get_users()
    assert result == [{'id': 1}]
```

---

## Async Tests

### Basic Async Test

```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result is not None
```

### Async Fixture

```python
@pytest.fixture
async def async_resource():
    resource = await AsyncResource.create()
    yield resource
    await resource.close()

@pytest.mark.asyncio
async def test_with_async_resource(async_resource):
    result = await async_resource.get_data()
    assert result is not None
```

### Async Tests with Database

```python
@pytest.fixture
async def async_db():
    db = AsyncDatabase()
    await db.connect()
    yield db
    await db.disconnect()

@pytest.mark.asyncio
async def test_async_database_query(async_db):
    result = await async_db.query('SELECT * FROM users')
    assert len(result) > 0
```

---

## Coverage

### Running Coverage

```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# Generate coverage for specific module
pytest --cov=src.user --cov-report=term-missing

# Generate coverage with minimum threshold
pytest --cov=src --cov-fail-under=80
```

### Coverage Configuration

```ini
# .coveragerc
[run]
source = src
omit =
    */tests/*
    */__pycache__/*
    */migrations/*
    */venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
```

### Coverage Thresholds

```bash
# Fail if coverage is below 80%
pytest --cov=src --cov-fail-under=80

# Fail if specific module coverage is below 90%
pytest --cov=src.user --cov-fail-under=90
```

---

## Testing FastAPI

### Basic FastAPI Test

```python
from fastapi.testclient import TestClient
from myapp.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

### Testing Endpoints

```python
def test_create_user():
    response = client.post(
        "/users/",
        json={"name": "John Doe", "email": "john@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert "id" in data
```

### Testing with Authentication

```python
def test_protected_endpoint():
    # Test without authentication
    response = client.get("/protected")
    assert response.status_code == 401

    # Test with authentication
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer token123"}
    )
    assert response.status_code == 200
```

### Testing with Database

```python
@pytest.fixture
async def test_db():
    # Use test database
    async with TestDatabase() as db:
        yield db

@pytest.mark.asyncio
async def test_create_user(test_db):
    response = client.post(
        "/users/",
        json={"name": "John Doe", "email": "john@example.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
```

---

## Testing Database Code

### Testing with SQLite In-Memory

```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture
def db_session():
    engine = create_engine('sqlite:///:memory:')
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    session = Session()
    yield session

    session.close()
    engine.dispose()

def test_create_user(db_session):
    user = User(name='John Doe', email='john@example.com')
    db_session.add(user)
    db_session.commit()

    retrieved = db_session.query(User).first()
    assert retrieved.name == 'John Doe'
```

### Testing with Mock Database

```python
from unittest.mock import Mock, patch

@pytest.fixture
def mock_db():
    with patch('myapp.Database') as MockDatabase:
        mock_db = MockDatabase.return_value
        mock_db.session.return_value = Mock()
        yield mock_db

def test_user_service(mock_db):
    user = UserService.create('John Doe', 'john@example.com')
    assert user.name == 'John Doe'
    mock_db.session.add.assert_called_once()
```

### Testing Database Queries

```python
def test_user_query(db_session):
    user1 = User(name='John Doe', email='john@example.com')
    user2 = User(name='Jane Doe', email='jane@example.com')
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()

    users = db_session.query(User).all()
    assert len(users) == 2
    assert users[0].name == 'John Doe'
```

---

## Best Practices

### 1. Use Descriptive Test Names

```python
# ❌ BAD: Vague test name
def test_user():
    pass

# ✅ GOOD: Descriptive test name
def test_create_user_with_valid_data():
    pass

def test_create_user_with_duplicate_email():
    pass
```

### 2. Use Fixtures for Setup

```python
# ❌ BAD: Setup in test
def test_database():
    db = Database()
    db.connect()
    result = db.query('SELECT * FROM users')
    assert len(result) > 0
    db.disconnect()

# ✅ GOOD: Use fixture
@pytest.fixture
def database():
    db = Database()
    db.connect()
    yield db
    db.disconnect()

def test_database(database):
    result = database.query('SELECT * FROM users')
    assert len(result) > 0
```

### 3. Use Parametrization

```python
# ❌ BAD: Multiple similar tests
def test_add_positive():
    assert add(2, 3) == 5

def test_add_zero():
    assert add(0, 0) == 0

def test_add_negative():
    assert add(-1, 1) == 0

# ✅ GOOD: Use parametrization
@pytest.mark.parametrize('a, b, expected', [
    (2, 3, 5),
    (0, 0, 0),
    (-1, 1, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### 4. Use Markers

```python
@pytest.mark.unit
def test_unit_function():
    pass

@pytest.mark.integration
def test_integration():
    pass
```

### 5. Mock External Dependencies

```python
from unittest.mock import patch

def test_external_api():
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        response = external_api_call()
        assert response == 200
```

### 6. Use Coverage

```bash
pytest --cov=src --cov-report=html
```

### 7. Test Edge Cases

```python
def test_empty_input():
    with pytest.raises(ValueError):
        validate_user({})

def test_null_input():
    with pytest.raises(ValueError):
        validate_user(None)
```

### 8. Keep Tests Independent

```python
# Each test should be able to run independently
def test_1():
    pass

def test_2():
    pass
```

### 9. Use Conftest for Shared Fixtures

```python
# conftest.py
@pytest.fixture
def app():
    return create_app()

@pytest.fixture
def client(app):
    return app.test_client()
```

### 10. Run Tests in CI

```yaml
# .github/workflows/test.yml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: pytest --cov=src --cov-report=xml
```

---

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Fixtures](https://docs.pytest.org/en/stable/fixture.html)
- [Pytest Asyncio](https://pytest-asyncio.readthedocs.io/)
- [Pytest Coverage](https://pytest-cov.readthedocs.io/)
- [Pytest Mock](https://pytest-mock.readthedocs.io/)
