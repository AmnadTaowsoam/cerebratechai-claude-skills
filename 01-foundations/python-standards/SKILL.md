### **04: Python Coding Standards**

> 
> **Current Level:** Expert (Enterprise Scale) 
> 
> 
> **Domain:** Foundations / Python Development 
> 

---

### **1. Executive Summary & Strategic Necessity**

* **Context:** ในโลกปี 2025-2026 การพัฒนาซอฟต์แวร์ด้วย Python มีความซับซ้อนเพิ่มขึ้นอย่างมาก การใช้ Python Standards ที่เป็นมาตรฐานช่วยให้ทีมพัฒนาสามารถเขียนโค้ดที่สะอดความ มีประสิทธิภาพ และสามารถบำรุงรักษาได้ง่าย
* **Business Impact:** การใช้ Python Standards ที่มีประสิทธิภาพช่วย:
  - เพิ่มความโค้ดที่สะอดความและเป็นมาตรฐาน
  - ลดความ Bug ที่เกิดขึ้นใน Production
  - เพิ่มประสิทธิภาพในการพัฒนา
  - ลดเวลาในการ Code Review
  - เพิ่มความสามารถในการทำงานร่วมกัน
  - ลด Technical Debt ที่สะสมในระยะว
  - เพิ่มความโปร่งใสในการพัฒนา
* **Product Thinking:** ทักษะนี้ช่วยแก้ปัญหา (Pain Point) ให้กับ:
  - ทีมพัฒนาที่ต้องการ Python Standards ที่เป็นระบบ
  - ผู้ทำงานผิดพลาดที่ต้องการ Standards ที่เข้าใจ
  - ทีมพัฒนาที่ต้องการ Code Quality ที่สูง
  - ลูกค้าที่ต้องการความเสถียรของระบบ
  - ทีม Support ที่ต้องการ Debug ของ Code

### **2. Technical Deep Dive (The "How-to")**

* **Core Logic:** Python Standards ประกอบด้วย:
  - **PEP 8 Compliance:** การปฏิบัติตามมาตรฐาน Python (Naming Conventions, Code Style, Import Organization)
  - **Type Hints:** การระบุ Type ทุกที่ (Basic Types, TypeVar, Callable, TypedDict, Literal, Self)
  - **Pydantic Models:** การใช้ Pydantic สำหรับ Validation (Basic Models, Nested Models, Request/Response Models, Custom Types)
  - **Error Handling:** การจัดการ Error ที่เป็นระบบ (Custom Exception Hierarchy, Try-Except Patterns, Context Managers)
  - **Async/Await Patterns:** การใช้ Async/Await อย่างถูกต้อง (Basic Async Functions, Parallel Execution, TaskGroup, Semaphore, Timeout Handling)
  - **Logging Best Practices:** การใช้ Logging ที่เป็นระบบ (Structured Logging, Log Levels, Logging Decorator)
  - **Dependency Injection:** การใช้ Dependency Injection ด้วย Protocol (Protocol-Based Interfaces, Service with DI, Concrete Implementations)
  - **Testing Patterns:** การเขียน Tests ที่มีประสิทธิภาพ (Pytest Configuration, Unit Tests, Integration Tests, Mocking)

* **Architecture Diagram Requirements:** แผนผังสถาปัตยกรรมที่ต้องมี:
  - **Python Project Structure Diagram:** แผนผังแสดงโครงสร้างโปรเจกต์ Python
  - **Type System Diagram:** แผนผังแสดง Type System ของ Python
  - **Error Handling Flow Diagram:** แผนผังแสดงกระบวนการ Error Handling
  - **Async Execution Flow Diagram:** แผนผังแสดงกระบวนการ Async Execution
  - **Dependency Injection Diagram:** แผนผังแสดง Dependency Injection Pattern

* **Implementation Workflow:**
  1. **Setup Python Environment:** ตั้งค่า Python Environment และ Dependencies
  2. **Configure Code Quality Tools:** ตั้งค่า Black, Ruff, Mypy, Pre-commit
  3. **Define Type Hints Standards:** กำหนด Type Hints Standards สำหรับโปรเจกต์
  4. **Implement Pydantic Models:** สร้าง Pydantic Models สำหรับ Validation
  5. **Setup Error Handling:** ตั้งค่า Error Handling ที่เป็นระบบ
  6. **Configure Logging:** ตั้งค่า Structured Logging
  7. **Write Tests:** เขียน Tests สำหรับโค้ด

### **3. Tooling & Tech Stack**

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้:
  - **Code Formatting:** Black, Ruff Format
  - **Linting:** Ruff, Pylint, Flake8, Bandit
  - **Type Checking:** Mypy, Pyright
  - **Testing:** Pytest, Pytest-asyncio, Faker, Coverage.py
  - **Validation:** Pydantic, Pydantic-Settings
  - **Logging:** Structlog, Loguru
  - **Pre-commit:** Pre-commit, Husky
  - **CI/CD:** GitHub Actions, GitLab CI, Azure Pipelines

* **Configuration Essentials:** ส่วนประกอบสำคัญในการตั้งค่า:
  - **pyproject.toml:** การตั้งค่า Python Project ที่ทันสมัย
  - **Black Configuration:** การตั้งค่า Black สำหรับ Formatting
  - **Ruff Configuration:** การตั้งค่า Ruff สำหรับ Linting
  - **Mypy Configuration:** การตั้งค่า Mypy สำหรับ Type Checking
  - **Pytest Configuration:** การตั้งค่า Pytest สำหรับ Testing
  - **Pre-commit Configuration:** การตั้งค่า Pre-commit Hooks

### **4. Standards, Compliance & Security**

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  - **PEP 8:** Python Enhancement Proposal 8 - Style Guide for Python Code
  - **PEP 484:** Type Hints for Python
  - **PEP 585:** Type Hinting Generics In Standard Collections
  - **PEP 613:** Explicit Type Aliases
  - **PEP 673:** Self Type
  - **PEP 695:** Type Parameter Syntax

* **Security Protocol:** กลไกการป้องกัน:
  - **Input Validation:** การตรวจสอบ Input ด้วย Pydantic
  - **Secret Management:** การจัดการ Secrets ด้วย Pydantic-Settings
  - **SQL Injection Prevention:** การป้องกัน SQL Injection ด้วย Parameterized Queries
  - **XSS Prevention:** การป้องกัน XSS ด้วย Input Sanitization
  - **Dependency Scanning:** การสแกน Dependencies ด้วย Bandit
  - **Secret Detection:** การตรวจสอบ Secrets ด้วย detect-secrets

* **Explainability:** ความสามารถในการอธิบาย:
  - **Type Annotations Documentation:** การบันทึก Type Annotations ที่ชัดเจน
  - **Error Messages Documentation:** การบันทึก Error Messages ที่ชัดเจน
  - **Logging Documentation:** การบันทึก Logging ที่ชัดเจน
  - **Code Comments:** การบันทึก Code Comments ที่ชัดเจน

### **5. Unit Economics & Performance Metrics (KPIs)**

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย (COGS):
  ```
  Total Cost = (Development Time × Hourly Rate) + 
               (Code Review Time × Hourly Rate) + 
               (Bug Fix Time × Hourly Rate) + 
               (Tooling Cost)
  
  ROI = (Productivity Gain - Total Cost) / Total Cost × 100%
  
  Productivity Gain = (Time Saved on Code Reviews) + 
                      (Time Saved on Bug Fixes) + 
                      (Time Saved on Onboarding)
  ```

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  - **Type Coverage:** % ของ Code ที่มี Type Hints (Target: > 90%)
  - **Code Quality Score:** คะแนนคุณภาพของโค้ด (Target: > A)
  - **Test Coverage:** % ของ Code ที่มี Tests (Target: > 80%)
  - **Bug Detection Rate:** % ของ Bugs ที่ค้นพบก่อน Production (Target: > 80%)
  - **Code Review Time:** เวลาเฉลี่ยในการ Code Review (Target: < 30 min)
  - **Team Productivity:** จำนวน Commits ต่อวัน (Target: > 10/day)

### **6. Strategic Recommendations (CTO Insights)**

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน:
  1. **Phase 1 (Months 1-2):** สร้าง Python Standards และ Guidelines, ฝึกอบรมทีม
  2. **Phase 2 (Months 3-4):** ตั้งค่า Code Quality Tools และ Pre-commit Hooks
  3. **Phase 3 (Months 5-6):** ฝึกอบรมทีมเกี่ยวกับ Python Standards และ Best Practices
  4. **Phase 4 (Year 2+):** ขยายไปยังทุกทีม, สร้าง Culture ของ Python Best Practices

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาด:
  - **Over-Engineering:** หลีกเลี่ยงการสร้าง Standards ที่ซับซ้อนเกินไป
  - **Not Following Standards:** ต้องทบทวนตามหลักการ Python Standards
  - **Skipping Type Hints:** หลีกเลี่ยงการไม่ใช้ Type Hints
  - **Not Using Pydantic:** หลีกเลี่ยงการไม่ใช้ Pydantic สำหรับ Validation
  - **Not Writing Tests:** หลีกเลี่ยงการไม่เขียน Tests
  - **Not Using Logging:** หลีกเลี่ยงการไม่ใช้ Logging ที่เป็นระบบ
  - **Not Using Pre-commit:** หลีกเลี่ยงการไม่ใช้ Pre-commit Hooks

---

## Overview

Python coding standards for Backend and AI/ML projects. Supports Python 3.11+.

## Core Principles

- **PEP 8 Compliance**: ปฏิบัติตามมาตรฐาน Python
- **Type Hints Always**: ระบุ type ทุกที่
- **Explicit is Better Than Implicit**: ชัดเจนดีกว่าคลุมเครือ
- **Fail Fast with Clear Error Messages**: ล้มเหลวเร็ว พร้อม error ที่ชัดเจน

## Python Version and Setup

### pyproject.toml (Modern Python)

```toml
[project]
name = "your-project"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.11"
license = { text = "MIT" }
authors = [
    { name = "Your Name", email = "your@email.com" }
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "fastapi>=0.109.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "uvicorn[standard]>=0.25.0",
    "httpx>=0.26.0",
    "sqlalchemy>=2.0.0",
    "alembic>=1.13.0",
    "asyncpg>=0.29.0",
    "redis>=5.0.0",
    "structlog>=24.1.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "black>=24.1.0",
    "ruff>=0.1.14",
    "mypy>=1.8.0",
    "pre-commit>=3.6.0",
    "faker>=22.0.0",
    "httpx>=0.26.0",
]
ml = [
    "torch>=2.1.0",
    "numpy>=1.26.0",
    "pandas>=2.1.0",
    "scikit-learn>=1.4.0",
]

[project.scripts]
app = "app.main:main"
migrate = "app.db.migrate:run_migrations"

[build-system]
requires = ["setuptools>=69.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 88
target-version = ['py311', 'py312']
include = '\.pyi?$'
extend-exclude = '''
/(
    \.git
    | \.venv
    | build
    | dist
    | migrations
)/
'''

[tool.ruff]
line-length = 88
target-version = "py311"
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "N",      # pep8-naming
    "UP",     # pyupgrade
    "ANN",    # flake8-annotations
    "ASYNC",  # flake8-async
    "S",      # flake8-bandit (security)
    "B",      # flake8-bugbear
    "A",      # flake8-builtins
    "C4",     # flake8-comprehensions
    "DTZ",    # flake8-datetimez
    "T10",    # flake8-debugger
    "EXE",    # flake8-executable
    "ISC",    # flake8-implicit-str-concat
    "ICN",    # flake8-import-conventions
    "LOG",    # flake8-logging
    "G",      # flake8-logging-format
    "PIE",    # flake8-pie
    "PYI",    # flake8-pyi
    "PT",     # flake8-pytest-style
    "Q",      # flake8-quotes
    "RSE",    # flake8-raise
    "RET",    # flake8-return
    "SLF",    # flake8-self
    "SIM",    # flake8-simplify
    "TID",    # flake8-tidy-imports
    "TCH",    # flake8-type-checking
    "ARG",    # flake8-unused-arguments
    "PTH",    # flake8-use-pathlib
    "ERA",    # eradicate
    "PL",     # Pylint
    "TRY",    # tryceratops
    "PERF",   # Perflint
    "RUF",    # Ruff-specific rules
]
ignore = [
    "E501",   # line too long (handled by black)
    "ANN101", # missing type for self
    "ANN102", # missing type for cls
    "ANN401", # Dynamically typed expressions (Any)
    "S101",   # assert usage (needed for tests)
    "TRY003", # Avoid long messages in exceptions
]

[tool.ruff.per-file-ignores]
"tests/**/*.py" = [
    "S101",   # asserts allowed in tests
    "ARG",    # unused arguments allowed in fixtures
    "ANN",    # type annotations not required in tests
    "PLR2004", # magic values allowed in tests
]

[tool.ruff.isort]
known-first-party = ["app"]
force-single-line = false
lines-after-imports = 2

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
warn_redundant_casts = true
warn_unused_ignores = true
show_error_codes = true
show_column_numbers = true
pretty = true
plugins = ["pydantic.mypy"]

[[tool.mypy.overrides]]
module = [
    "redis.*",
    "uvicorn.*",
]
ignore_missing_imports = true

[tool.pydantic-mypy]
init_forbid_extra = true
init_typed = true
warn_required_dynamic_aliases = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "-ra",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]
filterwarnings = [
    "ignore::DeprecationWarning",
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/migrations/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
]
```

## Naming Conventions (PEP 8)

### Variables & Functions (snake_case)

```python
# ❌ Bad
UserData = {}
def Get_User(): pass
def getUserData(): pass  # camelCase is not Pythonic
myVariable = 42

# ✅ Good
user_data = {}
def get_user(): pass
def get_user_data(): pass
my_variable = 42
```

### Classes (PascalCase)

```python
# ❌ Bad
class user_service: pass
class userService: pass
class USER_SERVICE: pass

# ✅ Good
class UserService: pass
class HTTPRequestHandler: pass
class XMLParser: pass
class OAuth2Client: pass
```

### Constants (SCREAMING_SNAKE_CASE)

```python
# ❌ Bad
apiKey = "..."
max_retries = 3
MaxConnections = 100

# ✅ Good
API_KEY = "..."
MAX_RETRIES = 3
MAX_CONNECTIONS = 100
DATABASE_URL = "postgresql://..."
DEFAULT_TIMEOUT_SECONDS = 30
```

### Private vs Protected vs Public

```python
class UserService:
    """Demonstrates naming conventions for visibility."""

    # Public attribute - accessible everywhere
    name: str = "UserService"

    # Protected attribute - internal use, subclasses OK
    # Single underscore is a convention, not enforced
    _cache: dict[str, Any]

    # Private attribute - name mangling applied
    # Becomes _UserService__secret_key
    __secret_key: str

    def __init__(self) -> None:
        self._cache = {}
        self.__secret_key = "secret"

    def public_method(self) -> str:
        """Public method - part of API."""
        return self._internal_helper()

    def _internal_helper(self) -> str:
        """Protected method - used internally, subclasses can override."""
        return "helper"

    def __private_method(self) -> str:
        """Private method - name mangled, truly private."""
        return self.__secret_key
```

### Boolean Variables (use is/has/can/should/was prefix)

```python
# ❌ Bad
active = True
admin = False
valid = True

# ✅ Good
is_active = True
is_admin = False
is_valid = True
has_permission = True
can_edit = False
should_retry = True
was_processed = False
```

### Module and Package Names

```python
# ❌ Bad
UserService.py
My-Module.py
myModule.py

# ✅ Good (lowercase, underscores if needed)
user_service.py
my_module.py
utils.py
helpers.py
```

## Type Hints (Modern Python 3.10+ Syntax)

### Basic Types

```python
# ❌ Bad - no type hints
def process_data(data):
    return data

# ❌ Bad - old style (Python 3.9)
from typing import Optional, Union, List, Dict, Tuple, Set

def get_user(user_id: str) -> Optional[Dict[str, Union[str, int]]]:
    pass

# ✅ Good - modern Python 3.10+ syntax
def process_data(data: str | int) -> str:
    return str(data)

def get_user(user_id: str) -> dict[str, str | int] | None:
    pass

# ✅ Good - built-in generic types
def process_users(
    user_ids: list[str],
    metadata: dict[str, Any],
    tags: set[str],
    coords: tuple[float, float],
    matrix: list[list[int]],
) -> list[dict[str, Any]]:
    pass
```

### TypeVar and Generic Types

```python
from typing import TypeVar, Generic

# Simple TypeVar
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

def get_first(items: list[T]) -> T | None:
    """Return first item or None if empty."""
    return items[0] if items else None

# Bounded TypeVar
from typing import TypeVar
from collections.abc import Hashable

THashable = TypeVar("THashable", bound=Hashable)

def deduplicate(items: list[THashable]) -> list[THashable]:
    """Remove duplicates while preserving order."""
    seen: set[THashable] = set()
    result: list[THashable] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

# Generic class
class Repository(Generic[T]):
    """Generic repository pattern."""

    def __init__(self) -> None:
        self._items: dict[str, T] = {}

    def get(self, id: str) -> T | None:
        return self._items.get(id)

    def save(self, id: str, item: T) -> None:
        self._items[id] = item

    def all(self) -> list[T]:
        return list(self._items.values())

# Usage
user_repo: Repository[User] = Repository()
user_repo.save("123", User(id="123", name="John"))
```

### Callable Types

```python
from collections.abc import Callable, Awaitable, Coroutine
from typing import ParamSpec, TypeVar, Concatenate

P = ParamSpec("P")
R = TypeVar("R")

# Simple callable
Handler = Callable[[str, int], bool]

def register_handler(handler: Handler) -> None:
    pass

# Callable with keyword arguments
def apply_function(
    func: Callable[..., R],
    *args: Any,
    **kwargs: Any,
) -> R:
    return func(*args, **kwargs)

# Async callable
AsyncHandler = Callable[[str], Awaitable[dict[str, Any]]]

async def process_with_handler(
    data: str,
    handler: AsyncHandler,
) -> dict[str, Any]:
    return await handler(data)

# Decorator with ParamSpec (preserves signature)
def log_calls(func: Callable[P, R]) -> Callable[P, R]:
    """Decorator that logs function calls."""
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

### TypedDict for Structured Dictionaries

```python
from typing import TypedDict, Required, NotRequired

# ❌ Bad - untyped dict
def process_config(config: dict[str, Any]) -> None:
    host = config["host"]  # No type safety
    port = config["port"]

# ✅ Good - TypedDict
class DatabaseConfig(TypedDict):
    host: str
    port: int
    database: str
    user: str
    password: str
    pool_size: NotRequired[int]  # Optional key
    ssl: NotRequired[bool]

def process_config(config: DatabaseConfig) -> None:
    host = config["host"]  # Type: str
    port = config["port"]  # Type: int
    pool_size = config.get("pool_size", 10)  # Type: int

# Total=False makes all keys optional
class PartialConfig(TypedDict, total=False):
    host: str
    port: int
```

### Literal Types

```python
from typing import Literal

# Restrict to specific values
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
HttpMethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
Environment = Literal["development", "staging", "production"]

def configure_logging(level: LogLevel) -> None:
    pass

def make_request(method: HttpMethod, url: str) -> None:
    pass

# Overloads with Literal
from typing import overload

@overload
def fetch_data(format: Literal["json"]) -> dict[str, Any]: ...
@overload
def fetch_data(format: Literal["text"]) -> str: ...
@overload
def fetch_data(format: Literal["bytes"]) -> bytes: ...

def fetch_data(format: Literal["json", "text", "bytes"]) -> dict[str, Any] | str | bytes:
    if format == "json":
        return {"data": "value"}
    elif format == "text":
        return "text data"
    else:
        return b"bytes data"
```

### Self Type (Python 3.11+)

```python
from typing import Self

class Builder:
    """Builder pattern with proper Self type."""

    def __init__(self) -> None:
        self._name: str = ""
        self._value: int = 0

    def with_name(self, name: str) -> Self:
        self._name = name
        return self

    def with_value(self, value: int) -> Self:
        self._value = value
        return self

class ExtendedBuilder(Builder):
    def __init__(self) -> None:
        super().__init__()
        self._extra: str = ""

    def with_extra(self, extra: str) -> Self:
        self._extra = extra
        return self

# Self correctly types return
builder = ExtendedBuilder().with_name("test").with_extra("data")  # Type: ExtendedBuilder
```

## Pydantic Models for Validation

### Basic Model Definition

```python
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from typing import Annotated


class User(BaseModel):
    """User model with comprehensive validation."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        frozen=False,
        extra="forbid",
        populate_by_name=True,
        use_enum_values=True,
    )

    id: str = Field(..., min_length=1, max_length=50, description="Unique identifier")
    email: str = Field(
        ...,
        pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$",
        description="User email address",
    )
    name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(default=None)
    tags: list[str] = Field(default_factory=list, max_length=10)
    metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Normalize email to lowercase."""
        return v.lower()

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Capitalize name properly."""
        return v.strip().title()

    @field_validator("tags", mode="before")
    @classmethod
    def validate_tags(cls, v: list[str] | str) -> list[str]:
        """Accept comma-separated string or list."""
        if isinstance(v, str):
            return [tag.strip() for tag in v.split(",") if tag.strip()]
        return v

    @model_validator(mode="after")
    def validate_model(self) -> Self:
        """Cross-field validation."""
        if self.age < 18 and "admin" in self.tags:
            raise ValueError("Users under 18 cannot be admins")
        return self
```

### Nested Models and Relationships

```python
from pydantic import BaseModel, Field
from enum import Enum


class AddressType(str, Enum):
    HOME = "home"
    WORK = "work"
    OTHER = "other"


class Address(BaseModel):
    """Address model."""
    street: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    country: str = Field(..., min_length=2, max_length=2)  # ISO code
    postal_code: str = Field(..., pattern=r"^\d{5}(-\d{4})?$")
    type: AddressType = Field(default=AddressType.HOME)


class UserProfile(BaseModel):
    """User profile with nested models."""
    user: User
    addresses: list[Address] = Field(default_factory=list, max_length=5)
    primary_address: Address | None = Field(default=None)

    @model_validator(mode="after")
    def validate_primary_address(self) -> Self:
        """Ensure primary address is in addresses list."""
        if self.primary_address and self.addresses:
            if self.primary_address not in self.addresses:
                raise ValueError("Primary address must be in addresses list")
        return self
```

### Request/Response Models

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Generic, TypeVar

T = TypeVar("T")


# Request models (input validation)
class CreateUserRequest(BaseModel):
    """Request model for creating a user."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    email: str = Field(..., pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")
    name: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=128)
    age: int = Field(..., ge=0, le=150)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password complexity."""
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain digit")
        return v


class UpdateUserRequest(BaseModel):
    """Request model for updating a user (partial)."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: str | None = Field(default=None, min_length=1, max_length=100)
    age: int | None = Field(default=None, ge=0, le=150)
    is_active: bool | None = Field(default=None)


# Response models (output serialization)
class UserResponse(BaseModel):
    """Response model for user data."""

    model_config = ConfigDict(
        from_attributes=True,  # Allow ORM model conversion
    )

    id: str
    email: str
    name: str
    age: int
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None


# Generic API response wrapper
class ApiResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool = True
    data: T | None = None
    error: str | None = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model."""
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1
```

### Custom Types with Annotated

```python
from typing import Annotated
from pydantic import Field, AfterValidator, BeforeValidator
from pydantic.functional_validators import AfterValidator
import re


def validate_slug(v: str) -> str:
    """Validate and normalize slug."""
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", v):
        raise ValueError("Invalid slug format")
    return v


def normalize_phone(v: str) -> str:
    """Normalize phone number."""
    # Remove all non-digits
    digits = re.sub(r"\D", "", v)
    if len(digits) != 10:
        raise ValueError("Phone must have 10 digits")
    return f"+1-{digits[:3]}-{digits[3:6]}-{digits[6:]}"


# Reusable annotated types
Slug = Annotated[str, AfterValidator(validate_slug)]
PhoneNumber = Annotated[str, BeforeValidator(normalize_phone)]
PositiveInt = Annotated[int, Field(gt=0)]
NonEmptyStr = Annotated[str, Field(min_length=1)]
EmailStr = Annotated[str, Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")]


class Article(BaseModel):
    """Article with custom types."""
    title: NonEmptyStr
    slug: Slug
    author_phone: PhoneNumber
    view_count: PositiveInt = 1
```

## Error Handling

### Custom Exception Hierarchy

```python
from typing import Any
from datetime import datetime


class AppException(Exception):
    """Base exception for all application errors."""

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
        self.timestamp = datetime.utcnow()

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for API response."""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
                "timestamp": self.timestamp.isoformat(),
            }
        }


# Client Errors (4xx)
class BadRequestException(AppException):
    """Raised for malformed requests."""

    def __init__(
        self,
        message: str = "Bad request",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code="BAD_REQUEST",
            status_code=400,
            details=details,
        )


class ValidationException(AppException):
    """Raised when validation fails."""

    def __init__(
        self,
        message: str,
        errors: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=400,
            details={"errors": errors or []},
        )


class UnauthorizedException(AppException):
    """Raised when authentication is required."""

    def __init__(self, message: str = "Authentication required") -> None:
        super().__init__(
            message=message,
            code="UNAUTHORIZED",
            status_code=401,
        )


class ForbiddenException(AppException):
    """Raised when access is denied."""

    def __init__(self, message: str = "Access denied") -> None:
        super().__init__(
            message=message,
            code="FORBIDDEN",
            status_code=403,
        )


class NotFoundException(AppException):
    """Raised when resource is not found."""

    def __init__(self, resource: str, resource_id: str | None = None) -> None:
        message = f"{resource} not found"
        if resource_id:
            message = f"{resource} with id '{resource_id}' not found"
        super().__init__(
            message=message,
            code="NOT_FOUND",
            status_code=404,
            details={"resource": resource, "id": resource_id},
        )


class ConflictException(AppException):
    """Raised for resource conflicts."""

    def __init__(
        self,
        message: str,
        resource: str | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code="CONFLICT",
            status_code=409,
            details={"resource": resource} if resource else {},
        )


class RateLimitException(AppException):
    """Raised when rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details={"retry_after": retry_after} if retry_after else {},
        )


# Server Errors (5xx)
class InternalException(AppException):
    """Raised for internal server errors."""

    def __init__(
        self,
        message: str = "Internal server error",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message=message,
            code="INTERNAL_ERROR",
            status_code=500,
            details=details,
        )


class ServiceUnavailableException(AppException):
    """Raised when a service is unavailable."""

    def __init__(self, service: str) -> None:
        super().__init__(
            message=f"{service} is currently unavailable",
            code="SERVICE_UNAVAILABLE",
            status_code=503,
            details={"service": service},
        )


class ExternalServiceException(AppException):
    """Raised when an external service fails."""

    def __init__(
        self,
        service: str,
        message: str | None = None,
        original_error: Exception | None = None,
    ) -> None:
        super().__init__(
            message=message or f"External service '{service}' failed",
            code="EXTERNAL_SERVICE_ERROR",
            status_code=502,
            details={
                "service": service,
                "original_error": str(original_error) if original_error else None,
            },
        )
```

### Try-Except Patterns

```python
import logging
from typing import TypeVar

logger = logging.getLogger(__name__)
T = TypeVar("T")


# ❌ Bad - bare except
def process_data_bad1(data: str) -> dict[str, Any]:
    try:
        return json.loads(data)
    except:  # Catches everything, including KeyboardInterrupt!
        return {}


# ❌ Bad - catching too broad, swallowing errors
def process_data_bad2(data: str) -> dict[str, Any]:
    try:
        return json.loads(data)
    except Exception as e:
        print(e)  # Just printing, not handling
        return {}


# ❌ Bad - re-raising without context
def process_data_bad3(data: str) -> dict[str, Any]:
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        raise  # Loses context of where error occurred


# ✅ Good - specific exceptions with proper handling
def process_data(data: str) -> dict[str, Any]:
    """Parse JSON data with proper error handling."""
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        logger.error(
            "Failed to parse JSON",
            extra={"data_preview": data[:100], "error": str(e)},
        )
        raise ValidationException(
            message="Invalid JSON format",
            errors=[{"field": "data", "message": str(e)}],
        ) from e


# ✅ Good - multiple exception types
async def fetch_user(user_id: str) -> User:
    """Fetch user with comprehensive error handling."""
    try:
        user = await db.users.find_one({"id": user_id})

        if user is None:
            raise NotFoundException("User", user_id)

        return User.model_validate(user)

    except NotFoundException:
        # Re-raise our custom exceptions as-is
        raise
    except ValidationError as e:
        # Data corruption in database
        logger.error(
            "Invalid user data in database",
            extra={"user_id": user_id, "error": str(e)},
        )
        raise InternalException(
            "User data is corrupted",
            details={"user_id": user_id},
        ) from e
    except Exception as e:
        # Unexpected errors
        logger.exception(
            "Unexpected error fetching user",
            extra={"user_id": user_id},
        )
        raise InternalException("Failed to fetch user") from e


# ✅ Good - using else and finally
def process_file(path: str) -> list[str]:
    """Process file with proper cleanup."""
    file_handle = None
    try:
        file_handle = open(path)
        lines = file_handle.readlines()
    except FileNotFoundError as e:
        logger.error(f"File not found: {path}")
        raise NotFoundException("File", path) from e
    except PermissionError as e:
        logger.error(f"Permission denied: {path}")
        raise ForbiddenException(f"Cannot access file: {path}") from e
    except IOError as e:
        logger.error(f"IO error reading file: {path}")
        raise InternalException(f"Failed to read file: {path}") from e
    else:
        # Only runs if no exception
        logger.info(f"Successfully read {len(lines)} lines from {path}")
        return lines
    finally:
        # Always runs
        if file_handle:
            file_handle.close()
```

### Context Managers

```python
from contextlib import contextmanager, asynccontextmanager
from typing import Generator, AsyncGenerator
from datetime import datetime


# ✅ Synchronous context manager
@contextmanager
def database_transaction(
    db: Database,
    *,
    readonly: bool = False,
) -> Generator[Connection, None, None]:
    """Context manager for database transactions."""
    connection = db.get_connection()
    try:
        if not readonly:
            connection.begin()
        yield connection
        if not readonly:
            connection.commit()
    except Exception as e:
        if not readonly:
            connection.rollback()
        logger.error(f"Transaction failed: {e}")
        raise
    finally:
        connection.close()


# Usage
with database_transaction(db) as conn:
    conn.execute("INSERT INTO users ...")
    conn.execute("INSERT INTO profiles ...")


# ✅ Async context manager
@asynccontextmanager
async def async_database_transaction(
    db: AsyncDatabase,
) -> AsyncGenerator[AsyncConnection, None]:
    """Async context manager for database transactions."""
    connection = await db.acquire()
    transaction = connection.transaction()
    try:
        await transaction.start()
        yield connection
        await transaction.commit()
    except Exception as e:
        await transaction.rollback()
        logger.error(f"Async transaction failed: {e}")
        raise
    finally:
        await db.release(connection)


# Usage
async with async_database_transaction(db) as conn:
    await conn.execute("INSERT INTO users ...")


# ✅ Timing context manager
@contextmanager
def timer(operation: str) -> Generator[None, None, None]:
    """Context manager to time operations."""
    start = datetime.utcnow()
    try:
        yield
    finally:
        elapsed = (datetime.utcnow() - start).total_seconds()
        logger.info(f"{operation} completed in {elapsed:.3f}s")


# Usage
with timer("User creation"):
    create_user(data)


# ✅ Resource cleanup context manager
@contextmanager
def temp_directory() -> Generator[Path, None, None]:
    """Create and cleanup temporary directory."""
    import tempfile
    import shutil
    from pathlib import Path

    temp_dir = Path(tempfile.mkdtemp())
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


# Usage
with temp_directory() as tmp:
    file_path = tmp / "data.json"
    file_path.write_text('{"key": "value"}')
    process_file(file_path)
# Directory automatically cleaned up
```

## Async/Await Patterns

### Basic Async Functions

```python
import asyncio
from typing import Any


# ❌ Bad - blocking call in async function
async def fetch_user_bad(user_id: str) -> User:
    # This blocks the event loop!
    return db.get_user(user_id)


# ❌ Bad - unnecessary async
async def calculate_sum(numbers: list[int]) -> int:
    # No I/O, no need for async
    return sum(numbers)


# ✅ Good - properly async with await
async def fetch_user(user_id: str) -> User:
    """Fetch user asynchronously."""
    return await db_async.get_user(user_id)


# ✅ Good - running blocking code in executor
async def fetch_user_from_sync_db(user_id: str) -> User:
    """Run sync code without blocking event loop."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,  # Default executor (ThreadPoolExecutor)
        lambda: sync_db.get_user(user_id),
    )
```

### Parallel Execution

```python
import asyncio


# ❌ Bad - sequential when parallel is possible
async def fetch_all_data_bad() -> tuple[list[User], list[Product], list[Order]]:
    users = await fetch_users()
    products = await fetch_products()
    orders = await fetch_orders()
    return users, products, orders


# ✅ Good - parallel execution with gather
async def fetch_all_data() -> tuple[list[User], list[Product], list[Order]]:
    """Fetch all data in parallel."""
    users, products, orders = await asyncio.gather(
        fetch_users(),
        fetch_products(),
        fetch_orders(),
    )
    return users, products, orders


# ✅ Good - parallel with error handling
async def fetch_all_data_safe() -> tuple[
    list[User] | None,
    list[Product] | None,
    list[Order] | None,
]:
    """Fetch all data, returning None for failed requests."""
    results = await asyncio.gather(
        fetch_users(),
        fetch_products(),
        fetch_orders(),
        return_exceptions=True,
    )

    processed: list[Any] = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Request {i} failed: {result}")
            processed.append(None)
        else:
            processed.append(result)

    return tuple(processed)
```

### TaskGroup (Python 3.11+)

```python
import asyncio


async def process_users(user_ids: list[str]) -> list[User]:
    """Process users using TaskGroup for better error handling."""
    results: list[User] = []

    async with asyncio.TaskGroup() as tg:
        tasks = [
            tg.create_task(fetch_user(uid))
            for uid in user_ids
        ]

    # All tasks completed successfully
    results = [task.result() for task in tasks]
    return results


# With exception handling
async def process_users_safe(user_ids: list[str]) -> dict[str, User | Exception]:
    """Process users, capturing individual failures."""
    results: dict[str, User | Exception] = {}

    async def fetch_and_store(uid: str) -> None:
        try:
            results[uid] = await fetch_user(uid)
        except Exception as e:
            results[uid] = e

    async with asyncio.TaskGroup() as tg:
        for uid in user_ids:
            tg.create_task(fetch_and_store(uid))

    return results
```

### Semaphore for Concurrency Control

```python
import asyncio


async def fetch_urls(urls: list[str], max_concurrent: int = 10) -> list[str]:
    """Fetch URLs with limited concurrency."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_with_limit(url: str) -> str:
        async with semaphore:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.text

    return await asyncio.gather(*[fetch_with_limit(url) for url in urls])


# Using asyncio.Queue for producer-consumer pattern
async def process_queue(
    items: list[str],
    num_workers: int = 5,
) -> list[str]:
    """Process items using worker queue pattern."""
    queue: asyncio.Queue[str | None] = asyncio.Queue()
    results: list[str] = []
    results_lock = asyncio.Lock()

    async def worker() -> None:
        while True:
            item = await queue.get()
            if item is None:  # Poison pill
                queue.task_done()
                break
            try:
                result = await process_item(item)
                async with results_lock:
                    results.append(result)
            finally:
                queue.task_done()

    # Start workers
    workers = [asyncio.create_task(worker()) for _ in range(num_workers)]

    # Add items to queue
    for item in items:
        await queue.put(item)

    # Add poison pills to stop workers
    for _ in range(num_workers):
        await queue.put(None)

    # Wait for all items to be processed
    await queue.join()
    await asyncio.gather(*workers)

    return results
```

### Timeout Handling

```python
import asyncio


async def fetch_with_timeout(
    url: str,
    timeout_seconds: float = 30.0,
) -> str:
    """Fetch URL with timeout."""
    try:
        async with asyncio.timeout(timeout_seconds):
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                return response.text
    except asyncio.TimeoutError:
        logger.error(f"Request to {url} timed out after {timeout_seconds}s")
        raise ServiceUnavailableException(f"Request to {url} timed out")


# Retry with exponential backoff
async def fetch_with_retry(
    url: str,
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> str:
    """Fetch URL with retry and exponential backoff."""
    last_exception: Exception | None = None

    for attempt in range(max_retries):
        try:
            return await fetch_with_timeout(url)
        except (httpx.HTTPError, asyncio.TimeoutError) as e:
            last_exception = e
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)
                logger.warning(
                    f"Attempt {attempt + 1} failed, retrying in {delay}s",
                    extra={"url": url, "error": str(e)},
                )
                await asyncio.sleep(delay)

    raise ExternalServiceException(
        service=url,
        message=f"Failed after {max_retries} attempts",
        original_error=last_exception,
    )
```

## Logging Best Practices

### Structured Logging Setup

```python
import logging
import sys
from typing import Any
import structlog
from datetime import datetime


def setup_logging(
    level: str = "INFO",
    json_format: bool = True,
) -> None:
    """Configure structured logging."""

    # Configure structlog
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if json_format:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


# Get logger instance
logger = structlog.get_logger()
```

### Using Structured Logging

```python
# ❌ Bad - using print
def process_order_bad(order_id: str) -> None:
    print(f"Processing order {order_id}")
    try:
        result = process(order_id)
        print(f"Order processed: {result}")
    except Exception as e:
        print(f"Error: {e}")


# ❌ Bad - f-string in log message
def process_order_bad2(order_id: str) -> None:
    logger.info(f"Processing order {order_id}")  # Interpolated before sent


# ✅ Good - structured logging with context
def process_order(order_id: str) -> None:
    """Process order with proper logging."""
    log = logger.bind(order_id=order_id)

    log.info("processing_order_started")

    try:
        result = process(order_id)
        log.info(
            "processing_order_completed",
            result=result,
            duration_ms=calculate_duration(),
        )
    except ValidationException as e:
        log.warning(
            "processing_order_validation_failed",
            error=str(e),
            error_code=e.code,
        )
        raise
    except Exception as e:
        log.exception(
            "processing_order_failed",
            error=str(e),
        )
        raise


# ✅ Context binding for request tracing
async def handle_request(request_id: str, user_id: str) -> None:
    """Handle request with context bound to logger."""
    # Bind context for all subsequent log calls
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        request_id=request_id,
        user_id=user_id,
    )

    logger.info("request_started")

    # All log calls from here will include request_id and user_id
    await process_request()

    logger.info("request_completed")
```

### Log Levels Usage

```python
# DEBUG - Detailed information for debugging
logger.debug(
    "cache_lookup",
    key=cache_key,
    hit=True,
)

# INFO - General operational events
logger.info(
    "user_created",
    user_id=user.id,
    email=user.email,
)

# WARNING - Something unexpected but handled
logger.warning(
    "rate_limit_approaching",
    current_rate=current,
    limit=limit,
    percentage=current / limit * 100,
)

# ERROR - Error that affected a specific operation
logger.error(
    "payment_failed",
    user_id=user_id,
    amount=amount,
    error=str(e),
)

# CRITICAL - System-wide critical failure
logger.critical(
    "database_connection_lost",
    host=db_host,
    retry_count=retry_count,
)

# EXCEPTION - Error with stack trace
try:
    process()
except Exception:
    logger.exception(
        "unexpected_error",
        operation="process",
    )
```

### Logging Decorator

```python
from functools import wraps
from typing import Callable, ParamSpec, TypeVar
import time

P = ParamSpec("P")
R = TypeVar("R")


def log_function_call(
    logger: structlog.BoundLogger,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Decorator to log function calls with timing."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter()
            log = logger.bind(function=func.__name__)

            log.debug("function_call_started")

            try:
                result = func(*args, **kwargs)
                elapsed = (time.perf_counter() - start) * 1000
                log.info(
                    "function_call_completed",
                    duration_ms=round(elapsed, 2),
                )
                return result
            except Exception as e:
                elapsed = (time.perf_counter() - start) * 1000
                log.error(
                    "function_call_failed",
                    duration_ms=round(elapsed, 2),
                    error=str(e),
                    error_type=type(e).__name__,
                )
                raise

        return wrapper

    return decorator


# Async version
def log_async_function_call(
    logger: structlog.BoundLogger,
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """Decorator to log async function calls with timing."""

    def decorator(func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            start = time.perf_counter()
            log = logger.bind(function=func.__name__)

            log.debug("async_function_call_started")

            try:
                result = await func(*args, **kwargs)
                elapsed = (time.perf_counter() - start) * 1000
                log.info(
                    "async_function_call_completed",
                    duration_ms=round(elapsed, 2),
                )
                return result
            except Exception as e:
                elapsed = (time.perf_counter() - start) * 1000
                log.error(
                    "async_function_call_failed",
                    duration_ms=round(elapsed, 2),
                    error=str(e),
                )
                raise

        return wrapper

    return decorator


# Usage
@log_function_call(logger)
def process_data(data: str) -> dict[str, Any]:
    return {"processed": data}

@log_async_function_call(logger)
async def fetch_data(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.text
```

## Function Patterns (Dependency Injection with Protocol)

### Protocol-Based Interfaces

```python
from typing import Protocol, runtime_checkable


# Define protocols (interfaces)
@runtime_checkable
class UserRepository(Protocol):
    """Protocol for user repository operations."""

    async def get_by_id(self, user_id: str) -> User | None:
        """Get user by ID."""
        ...

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        ...

    async def create(self, user: User) -> User:
        """Create a new user."""
        ...

    async def update(self, user: User) -> User:
        """Update existing user."""
        ...

    async def delete(self, user_id: str) -> bool:
        """Delete user by ID."""
        ...


@runtime_checkable
class EmailService(Protocol):
    """Protocol for email service."""

    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
    ) -> bool:
        """Send an email."""
        ...

    async def send_template_email(
        self,
        to: str,
        template: str,
        context: dict[str, Any],
    ) -> bool:
        """Send templated email."""
        ...


@runtime_checkable
class CacheService(Protocol):
    """Protocol for cache operations."""

    async def get(self, key: str) -> Any | None:
        ...

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        ...

    async def delete(self, key: str) -> bool:
        ...
```

### Service with Dependency Injection

```python
class UserService:
    """User service with injected dependencies."""

    def __init__(
        self,
        user_repo: UserRepository,
        email_service: EmailService,
        cache: CacheService,
        logger: structlog.BoundLogger,
    ) -> None:
        self._user_repo = user_repo
        self._email_service = email_service
        self._cache = cache
        self._logger = logger

    async def get_user(self, user_id: str) -> User:
        """Get user by ID with caching."""
        cache_key = f"user:{user_id}"

        # Try cache first
        cached = await self._cache.get(cache_key)
        if cached:
            self._logger.debug("cache_hit", user_id=user_id)
            return User.model_validate(cached)

        # Fetch from repository
        user = await self._user_repo.get_by_id(user_id)
        if user is None:
            raise NotFoundException("User", user_id)

        # Cache result
        await self._cache.set(cache_key, user.model_dump(), ttl=3600)

        return user

    async def create_user(self, request: CreateUserRequest) -> User:
        """Create a new user."""
        # Check for existing user
        existing = await self._user_repo.get_by_email(request.email)
        if existing:
            raise ConflictException(
                f"User with email {request.email} already exists",
                resource="User",
            )

        # Create user
        user = User(
            id=generate_id(),
            email=request.email,
            name=request.name,
            age=request.age,
        )

        created = await self._user_repo.create(user)

        # Send welcome email
        await self._email_service.send_template_email(
            to=user.email,
            template="welcome",
            context={"name": user.name},
        )

        self._logger.info("user_created", user_id=created.id)

        return created
```

### Concrete Implementations

```python
from sqlalchemy.ext.asyncio import AsyncSession

class SQLAlchemyUserRepository:
    """SQLAlchemy implementation of UserRepository."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        row = result.scalar_one_or_none()
        return User.model_validate(row) if row else None

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        row = result.scalar_one_or_none()
        return User.model_validate(row) if row else None

    async def create(self, user: User) -> User:
        model = UserModel(**user.model_dump())
        self._session.add(model)
        await self._session.commit()
        await self._session.refresh(model)
        return User.model_validate(model)

    # ... other methods


class RedisCache:
    """Redis implementation of CacheService."""

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def get(self, key: str) -> Any | None:
        value = await self._redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        await self._redis.set(
            key,
            json.dumps(value),
            ex=ttl,
        )

    async def delete(self, key: str) -> bool:
        return await self._redis.delete(key) > 0
```

### Dependency Container / Factory

```python
from dataclasses import dataclass
from functools import lru_cache

@dataclass
class Container:
    """Dependency injection container."""

    db_session: AsyncSession
    redis: Redis
    logger: structlog.BoundLogger

    @property
    def user_repository(self) -> UserRepository:
        return SQLAlchemyUserRepository(self.db_session)

    @property
    def cache(self) -> CacheService:
        return RedisCache(self.redis)

    @property
    def email_service(self) -> EmailService:
        return SendGridEmailService(settings.sendgrid_api_key)

    @property
    def user_service(self) -> UserService:
        return UserService(
            user_repo=self.user_repository,
            email_service=self.email_service,
            cache=self.cache,
            logger=self.logger.bind(service="UserService"),
        )


# FastAPI dependency injection
async def get_container(
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis),
) -> Container:
    return Container(
        db_session=db,
        redis=redis,
        logger=structlog.get_logger(),
    )


async def get_user_service(
    container: Container = Depends(get_container),
) -> UserService:
    return container.user_service


# Usage in route
@router.get("/users/{user_id}")
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await user_service.get_user(user_id)
    return UserResponse.model_validate(user)
```

## Dataclasses vs Pydantic

### When to Use Dataclasses

```python
from dataclasses import dataclass, field, asdict, astuple
from typing import ClassVar

# ✅ Use dataclass for internal data structures (no validation needed)
@dataclass
class Point:
    """Simple data container - no validation needed."""
    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

# ✅ Use frozen dataclass for immutable value objects
@dataclass(frozen=True)
class Coordinate:
    """Immutable coordinate - can be used as dict key."""
    latitude: float
    longitude: float

    def __post_init__(self) -> None:
        # Validation in __post_init__ for dataclasses
        if not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")

# ✅ Dataclass with default factory and class variables
@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    key: str
    value: Any
    created_at: datetime = field(default_factory=datetime.utcnow)
    ttl_seconds: int = 3600
    hits: int = field(default=0, repr=False)

    # Class variable (not included in __init__)
    DEFAULT_TTL: ClassVar[int] = 3600

    @property
    def is_expired(self) -> bool:
        age = (datetime.utcnow() - self.created_at).total_seconds()
        return age > self.ttl_seconds

# ✅ Dataclass with slots for memory efficiency
@dataclass(slots=True)
class LogEntry:
    """Memory-efficient log entry."""
    timestamp: datetime
    level: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)

# ✅ Dataclass for internal DTOs
@dataclass
class UserCreationResult:
    """Internal result of user creation."""
    user: User
    verification_token: str
    email_sent: bool
```

### When to Use Pydantic

```python
from pydantic import BaseModel, Field, field_validator

# ✅ Use Pydantic for API request/response models
class CreateOrderRequest(BaseModel):
    """API request - needs validation."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    product_id: str = Field(..., min_length=1)
    quantity: int = Field(..., ge=1, le=100)
    shipping_address: str = Field(..., min_length=10)

    @field_validator("product_id")
    @classmethod
    def validate_product_id(cls, v: str) -> str:
        if not v.startswith("PROD-"):
            raise ValueError("Product ID must start with PROD-")
        return v


# ✅ Use Pydantic for configuration
class DatabaseConfig(BaseModel):
    """Database configuration with validation."""
    host: str
    port: int = Field(ge=1, le=65535)
    database: str
    user: str
    password: str
    pool_size: int = Field(default=10, ge=1, le=100)

    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


# ✅ Use Pydantic for external data parsing
class ExternalApiResponse(BaseModel):
    """Parse external API response with validation."""

    model_config = ConfigDict(
        extra="ignore",  # Ignore unknown fields from API
    )

    id: str
    status: Literal["success", "error", "pending"]
    data: dict[str, Any] | None = None
    error_message: str | None = None


# ✅ Use Pydantic for ORM model serialization
class UserFromDB(BaseModel):
    """User model from database."""

    model_config = ConfigDict(
        from_attributes=True,  # Allow ORM object conversion
    )

    id: str
    email: str
    name: str
    created_at: datetime
```

### Comparison Summary

```python
# Summary: Dataclass vs Pydantic

# Use DATACLASS when:
# - Internal data structures
# - No validation needed
# - Performance critical (slightly faster)
# - Simple DTOs between internal layers
# - Value objects (frozen=True)
# - Need slots for memory efficiency

# Use PYDANTIC when:
# - API request/response models
# - Configuration with validation
# - External data parsing (JSON, API responses)
# - ORM model serialization
# - Complex validation rules
# - Need schema export (OpenAPI)
```

## File Organization and Imports

### Project Structure

```
project/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py              # Application entry point
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py        # Settings and configuration
│       │   ├── exceptions.py    # Custom exceptions
│       │   ├── logging.py       # Logging setup
│       │   └── security.py      # Security utilities
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py          # Base model classes
│       │   ├── user.py          # User models
│       │   └── order.py         # Order models
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── user.py          # Pydantic schemas for users
│       │   └── order.py         # Pydantic schemas for orders
│       ├── repositories/
│       │   ├── __init__.py
│       │   ├── base.py          # Base repository
│       │   └── user.py          # User repository
│       ├── services/
│       │   ├── __init__.py
│       │   ├── user.py          # User service
│       │   └── order.py         # Order service
│       ├── api/
│       │   ├── __init__.py
│       │   ├── dependencies.py  # FastAPI dependencies
│       │   ├── middleware.py    # API middleware
│       │   └── routes/
│       │       ├── __init__.py
│       │       ├── users.py     # User routes
│       │       └── orders.py    # Order routes
│       ├── db/
│       │   ├── __init__.py
│       │   ├── session.py       # Database session
│       │   └── migrations/      # Alembic migrations
│       └── utils/
│           ├── __init__.py
│           └── helpers.py       # Utility functions
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Shared fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_user_service.py
│   └── integration/
│       ├── __init__.py
│       └── test_user_api.py
├── pyproject.toml
├── .pre-commit-config.yaml
└── .env.example
```

### Import Organization

```python
"""Module docstring describing module's purpose.

This module handles user-related operations.
"""

# 1. Future imports (if needed for compatibility)
