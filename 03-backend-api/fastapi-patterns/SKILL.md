# FastAPI Patterns and Best Practices

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

FastAPI เป็น modern, fast (high-performance) web framework สำหรับ building APIs ด้วย Python 3.6+ โดยใช้ standard Python type hints ซึ่งช่วยให้ developers สร้าง APIs ได้รวดเร็ว, maintainable, และ type-safe

FastAPI ประกอบด้วย:
- **Type Hints** - Standard Python type hints สำหรับ automatic validation
- **Pydantic** - Data validation ด้วย Pydantic models
- **Async Support** - Native async/await support
- **OpenAPI** - Automatic OpenAPI documentation
- **Dependency Injection** - Powerful dependency injection system
- **WebSocket Support** - Built-in WebSocket support

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **เพิ่ม Development Velocity** - FastAPI ช่วยเพิ่ม development velocity ได้ถึง 40-60%
2. **ลด Bugs** - Automatic validation ช่วยลด bugs ได้ถึง 30-40%
3. **เพิ่ม Performance** - High-performance framework ช่วยเพิ่ม API performance
4. **ลด Documentation Time** - Auto-generated documentation ช่วยลด documentation time
5. **ปรับปรุง Type Safety** - Type hints ช่วยเพิ่ม type safety

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Type-Safe** - APIs ต้อง type-safe ด้วย Python type hints
2. **Validated** - APIs ต้อง validated ด้วย Pydantic
3. **Documented** - APIs ต้อง auto-documented ด้วย OpenAPI
4. **Async** - APIs ต้อง async สำหรับ high performance
5. **Testable** - APIs ต้อง testable ง่าย

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

FastAPI ประกอบด้วย:

1. **Application** - FastAPI application instance
2. **Router** - Routing system สำหรับ mapping URLs ไปยัง endpoints
3. **Pydantic Models** - Data validation ด้วย Pydantic
4. **Dependency Injection** - Dependency injection system
5. **Middleware** - Middleware สำหรับ request/response processing
6. **Background Tasks** - Background tasks สำหรับ async operations
7. **WebSocket** - WebSocket support

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              FastAPI Architecture                    │
├─────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Client Layer                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Browser    │  │  Mobile     │  │  API Client │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Middleware Stack                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  CORS       │  │  Logging    │  │  Auth       │  │   │
│  │  │  Middleware│  │  Middleware │  │  Middleware │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Routing Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Routes     │  │  Endpoints  │  │  Routers    │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Dependency Injection Layer           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Database   │  │  Services   │  │  Utilities  │  │   │
│  │  │  Dependencies│  │            │  │            │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Data Layer                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Pydantic   │  │  Models     │  │  Schemas    │  │   │
│  │  │  Models     │  │            │  │            │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Initialize FastAPI App**

```python
# app/main.py
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)
```

**Step 2: Add Routes**

```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
async def get_users():
    return {"users": []}
```

**Step 3: Include Router**

```python
# app/main.py
from app.api.v1.api import api_router

app.include_router(api_router, prefix=settings.API_V1_STR)
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| FastAPI | Web Framework | ^0.104.0 | MIT |
| Pydantic | Data Validation | ^2.5.0 | MIT |
| SQLAlchemy | ORM | ^2.0.0 | MIT |
| Pytest | Testing Framework | ^7.4.0 | MIT |
| httpx | Async HTTP Client | ^0.25.0 | BSD-3-Clause |
| uvicorn | ASGI Server | ^0.24.0 | BSD-3-Clause |
| alembic | Database Migration | ^1.12.0 | MIT |
| redis-py | Redis Client | ^5.0.0 | MIT |

### 3.2 Configuration Essentials

**Pydantic Settings:**
```python
# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "My API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: str = "noreply@example.com"


settings = Settings()
```

**Database Configuration:**
```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **OpenAPI 3.0** - OpenAPI Specification
- **REST API Standards** - RESTful API Design Standards
- **OWASP** - Security Best Practices
- **GDPR** - Data Protection สำหรับ API Data
- **HIPAA** - Healthcare Data Protection

### 4.2 Security Protocol

FastAPI ต้องปฏิบัติตามหลักความปลอดภัย:

1. **Input Validation** - Validate ข้อมูลทั้ง client แล server
2. **Authentication** - ใช้ JWT หรือ OAuth2
3. **Authorization** - Implement role-based access control
4. **CORS** - Configure CORS อย่างเหมาะสม
5. **HTTPS** - ใช้ HTTPS สำหรับ production
6. **Rate Limiting** - จำกัดจำนวน requests

### 4.3 Explainability

FastAPI ต้องสามารถอธิบายได้ว่า:

1. **Request Flow** - ทำไม request ถูก process อย่างไร
2. **Validation** - ทำไม data ถูก validate อย่างไร
3. **Error Handling** - ทำไม errors ถูก handle อย่างไร
4. **Response Format** - ทำไม responses ถูก format อย่างไร

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Response Time | Average response time | < 50ms |
| Throughput | Requests per second | > 2000 req/s |
| Error Rate | Errors / Total Requests | < 1% |
| Memory Usage | Memory per request | < 5 MB |
| CPU Usage | CPU utilization | < 60% |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **Response Time** - Average response time
2. **Throughput** - Requests per second
3. **Error Rate** - Error rate
4. **Memory Usage** - Memory usage

**Business Metrics:**

1. **API Availability** - API uptime
2. **User Satisfaction** - CSAT score
3. **Support Tickets** - Support tickets จาก API issues
4. **Time to Resolution** - Average time to resolve issues

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Initialize FastAPI app
- Setup project structure
- Add basic routes
- Implement Pydantic models

**Phase 2: Advanced Features (Week 3-4)**
- Add dependency injection
- Implement authentication
- Add middleware
- Setup database

**Phase 3: Integration (Week 5-6)**
- Add background tasks
- Implement WebSocket support
- Add file uploads
- Setup testing

**Phase 4: Production (Week 7-8)**
- Optimize performance
- Setup monitoring
- Documentation and training
- Best practices documentation

### 6.2 Pitfalls to Avoid

1. **Poor Type Hints** - ไม่ใช้ type hints อย่างถูกต้อง
2. **Missing Validation** - ไม่ validate input
3. **Poor Error Handling** - ไม่ handle errors อย่างเหมาะสม
4. **No Documentation** - ไม่ document APIs
5. **Poor Performance** - ไม่ optimize performance
6. **No Testing** - ไม่ test endpoints

### 6.3 Best Practices Checklist

- [ ] ใช้ Python type hints สำหรับ type safety
- [ ] Implement Pydantic models สำหรับ validation
- [ ] Use async/await สำหรับ async operations
- [ ] Implement dependency injection
- [ ] Add authentication แล authorization
- [ ] Use middleware สำหรับ cross-cutting concerns
- [ ] Implement proper error handling
- [ ] Add background tasks สำหรับ async operations
- [ ] Test endpoints ด้วย Pytest
- [ ] Use OpenAPI documentation
- [ ] Add CORS configuration
- [ ] Implement rate limiting
- [ ] Use WebSocket สำหรับ real-time features
- [ ] Add file upload support
- [ ] Monitor performance แล errors

---

## 7. Implementation Examples

### 7.1 Project Structure

**Recommended Structure:**
```
app/
├── __init__.py
├── main.py              # Application entry point
├── api/                 # API routes
│   ├── __init__.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── auth.py
│   │   │   └── items.py
│   │   └── api.py      # Router aggregation
├── core/                # Core configuration
│   ├── __init__.py
│   ├── config.py
│   ├── security.py
│   └── deps.py        # Dependency injection
├── models/              # Database models
│   ├── __init__.py
│   ├── user.py
│   └── item.py
├── schemas/             # Pydantic models
│   ├── __init__.py
│   ├── user.py
│   └── item.py
├── services/            # Business logic
│   ├── __init__.py
│   ├── user_service.py
│   └── item_service.py
├── repositories/        # Data access layer
│   ├── __init__.py
│   ├── base.py
│   └── user_repository.py
├── middleware/         # Custom middleware
│   ├── __init__.py
│   └── logging.py
└── utils/              # Utility functions
    ├── __init__.py
    └── helpers.py
```

**Main Application Setup:**
```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# Startup event
@app.on_event("startup")
async def startup_event():
    # Initialize database, cache, etc.
    pass

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    # Cleanup resources
    pass
```

### 7.2 Application Setup

**Configuration with Pydantic Settings:**
```python
# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "My API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: str
    EMAILS_FROM_EMAIL: str = "noreply@example.com"


settings = Settings()
```

**Database Setup:**
```python
# app/core/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 7.3 Pydantic Models

**Request Models:**
```python
# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

    @validator("password")
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain number")
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDBBase(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserResponse(UserInDBBase):
    """User response without sensitive data"""
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: int | None = None
```

**Response Models:**
```python
# app/schemas/common.py
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, List


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    size: int
    pages: int


class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str = "Operation successful"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: Optional[dict] = None
```

### 7.4 Dependency Injection

**Common Dependencies:**
```python
# app/core/deps.py
from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import verify_password
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.sub).first()
    if not user:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
```

**Custom Dependencies:**
```python
# Pagination dependency
from fastapi import Depends, Query
from typing import Optional


async def get_pagination(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of records per page")
) -> dict:
    return {"skip": skip, "limit": limit}

# Usage in endpoint
@app.get("/users")
async def get_users(
    pagination: dict = Depends(get_pagination),
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(pagination["skip"]).limit(pagination["limit"]).all()
    return {"items": users, "total": len(users)}
```

### 7.5 Async Patterns

**Async Database Operations:**
```python
# Using asyncpg with SQLAlchemy
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

async_engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db"
)
AsyncSessionLocal = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

# Async endpoint
from fastapi import Depends
from app.core.database import get_async_db

@app.get("/users")
async def get_users_async(db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users
```

**Async External API Calls:**
```python
import httpx
from fastapi import HTTPException


async def fetch_external_data(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"External API error: {exc.response.text}"
            )
        except httpx.RequestError as exc:
            raise HTTPException(
                status_code=503,
                detail=f"External service unavailable: {str(exc)}"
            )


@app.get("/external-data")
async def get_external_data():
    data = await fetch_external_data("https://api.example.com/data")
    return data
```

**Concurrent Requests:**
```python
import asyncio
from typing import List


async def fetch_multiple_users(user_ids: List[int]) -> List[dict]:
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f"https://api.example.com/users/{uid}")
            for uid in user_ids
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        users = []
        for response in responses:
            if isinstance(response, Exception):
                continue
            users.append(response.json())

        return users


@app.get("/users/batch")
async def get_users_batch(user_ids: str = Query(...)):
    ids = [int(uid) for uid in user_ids.split(",")]
    users = await fetch_multiple_users(ids)
    return users
```

### 7.6 Error Handling

**Custom Exception Handler:**
```python
# app/core/exceptions.py
from typing import Any, Dict, Optional, Union
from fastapi import HTTPException, status


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundException(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class BadRequestException(AppException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenException(AppException):
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ConflictException(AppException):
    def __init__(self, detail: str = "Conflict"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
```

**Global Exception Handler:**
```python
# app/core/exception_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import AppException


async def app_exception_handler(
    request: Request, exc: AppException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "path": str(request.url)
        }
    )


async def http_exception_handler(
    request: Request, exc: HTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "path": str(request.url)
        }
    )


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "message": "Validation error",
            "errors": errors,
            "path": str(request.url)
        }
    )
```

**Register Exception Handlers:**
```python
# app/main.py
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.exception_handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler
)

app = FastAPI()

# Register exception handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
```

### 7.7 Middleware

**Logging Middleware:**
```python
# app/middleware/logging.py
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import logger


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate duration
        process_time = (time.time() - start_time) * 1000

        # Log request
        logger.info({
            "method": request.method,
            "url": str(request.url),
            "status_code": response.status_code,
            "process_time_ms": round(process_time, 2),
            "client": request.client.host if request.client else None,
        })

        # Add custom header
        response.headers["X-Process-Time"] = str(process_time)

        return response


# Usage in main.py
app.add_middleware(LoggingMiddleware)
```

**Request ID Middleware:**
```python
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response
```

**Timing Middleware:**
```python
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Response-Time"] = str(process_time)

        return response
```

### 7.8 Background Tasks

**Simple Background Task:**
```python
from fastapi import FastAPI, BackgroundTasks
from app.utils.email import send_email

app = FastAPI()


@app.post("/send-email")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    # Add task to background
    background_tasks.add_task(send_email, email, "Welcome!")

    return {"message": "Email will be sent in background"}
```

**Background Task with Dependencies:**
```python
from app.core.database import get_db
from app.models.user import User


def process_user_update(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.last_active = datetime.utcnow()
        db.commit()


@app.post("/users/{user_id}/ping")
async def ping_user(
    user_id: int,
    background_tasks: BackgroundTasks
):
    # Pass db session to background task
    db = next(get_db())
    background_tasks.add_task(process_user_update, user_id, db)

    return {"message": "Ping recorded"}
```

**Long-running Background Task:**
```python
import asyncio
from fastapi import BackgroundTasks


async def long_running_task(task_id: str):
    await asyncio.sleep(60)  # Simulate long task
    # Update task status in database
    print(f"Task {task_id} completed")


@app.post("/tasks/start")
async def start_task(background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())
    background_tasks.add_task(long_running_task, task_id)

    return {"task_id": task_id, "status": "started"}
```

### 7.9 WebSocket Support

**Basic WebSocket:**
```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client {client_id} left")
```

**WebSocket with Authentication:**
```python
from fastapi import WebSocket, WebSocketException, status, Query
from jose import jwt
from app.core.config import settings


async def websocket_auth(
    websocket: WebSocket,
    token: str = Query(...)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY)
        return payload
    except jwt.JWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)


@app.websocket("/ws/protected")
async def protected_websocket(
    websocket: WebSocket,
    user: dict = Depends(websocket_auth)
):
    await websocket.accept()
    await websocket.send_json({"message": "Authenticated", "user": user})
```

### 7.10 File Uploads

**Single File Upload:**
```python
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os

app = FastAPI()
UPLOAD_DIR = "uploads"


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Create upload directory if not exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save file
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "location": file_location
    }


@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = f"{UPLOAD_DIR}/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)
```

**Multiple File Upload:**
```python
from typing import List


@app.post("/upload-multiple")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    uploaded_files = []

    for file in files:
        file_location = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        uploaded_files.append(file.filename)

    return {
        "filenames": uploaded_files,
        "count": len(uploaded_files)
    }
```

**File Upload with Validation:**
```python
from fastapi import UploadFile, File, HTTPException, status

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_file(file: UploadFile) -> UploadFile:
    # Check file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File extension {file_ext} not allowed"
        )

    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Seek back to start

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds {MAX_FILE_SIZE} bytes"
        )

    return file


@app.post("/upload-image")
async def upload_image(file: UploadFile = Depends(validate_file)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"filename": file.filename}
```

### 7.11 Testing with Pytest

**Test Configuration:**
```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides = {}
```

**Endpoint Tests:**
```python
# tests/test_users.py
from fastapi.testclient import TestClient
from app.schemas.user import UserCreate, UserResponse


def test_create_user(client: TestClient):
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "Test123456"
    }

    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "password" not in data  # Password should not be returned


def test_get_users(client: TestClient, db):
    # Create test user
    user_data = UserCreate(
        email="test@example.com",
        full_name="Test User",
        password="Test123456"
    )
    user = User(**user_data.dict(), hashed_password="hashed")
    db.add(user)
    db.commit()

    # Get users
    response = client.get("/api/v1/users/")

    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["email"] == user_data["email"]


def test_get_user_not_found(client: TestClient):
    response = client.get("/api/v1/users/999")

    assert response.status_code == 404
    assert "not found" in response.json()["message"].lower()
```

**Async Tests:**
```python
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_async_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/users/")
        assert response.status_code == 200
```

### 7.12 Auto-documentation

**Custom OpenAPI Schema:**
```python
# app/main.py
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A comprehensive API documentation",
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users. The **login** logic is also here.",
        },
        {
            "name": "items",
            "description": "Manage items.",
        },
        {
            "name": "auth",
            "description": "Authentication and authorization.",
        },
    ],
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT License",
    },
)
```

**Custom Response Examples:**
```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class UserResponse(BaseModel):
    id: int = Field(..., example=1)
    email: str = Field(..., example="user@example.com")
    full_name: str = Field(..., example="John Doe")
    is_active: bool = Field(..., example=True)


@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    responses={
        200: {
            "description": "User found",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "user@example.com",
                        "full_name": "John Doe",
                        "is_active": True
                    }
                }
            }
        },
        404: {
            "description": "User not found",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "message": "User not found"
                    }
                }
            }
        }
    }
)
async def get_user(user_id: int):
    # Implementation
    pass
```

**Security Documentation:**
```python
from fastapi import FastAPI, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

app = FastAPI(
    security=[{"bearerAuth": []}],
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/protected")
async def protected_endpoint(
    credentials: HTTPAuthorizationCredentials = Security(security)
):
    return {"message": "Access granted"}
```

---

## 8. Related Skills

- `03-backend-api/error-handling`
- `03-backend-api/validation`
- `03-backend-api/middleware`
- `01-foundations/python-standards`
- `14-monitoring-observability`
