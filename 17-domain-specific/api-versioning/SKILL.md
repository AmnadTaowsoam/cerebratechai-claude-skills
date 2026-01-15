# API Versioning

A comprehensive guide to API versioning strategies.

## Table of Contents

1. [Versioning Approaches](#versioning-approaches)
2. [Implementation Patterns](#implementation-patterns)
3. [Version Negotiation](#version-negotiation)
4. [Deprecation Strategy](#deprecation-strategy)
5. [Migration Guides](#migration-guides)
6. [Backward Compatibility](#backward-compatibility)
7. [Documentation](#documentation)
8. [Testing Multiple Versions](#testing-multiple-versions)
9. [Sunset Headers](#sunset-headers)
10. [Best Practices](#best-practices)

---

## Versioning Approaches

### URL Path Versioning

```
Version in URL path:
- https://api.example.com/v1/users
- https://api.example.com/v2/users
- https://api.example.com/v3/users

Pros:
- Clear version in URL
- Easy to cache by version
- Simple to implement

Cons:
- URL changes when versioning
- Breaks existing clients
```

```typescript
// Express - URL path versioning
import express from 'express';

const v1Router = express.Router();
v1Router.get('/users', (req, res) => {
  res.json({ version: 'v1', users: [] });
});

const v2Router = express.Router();
v2Router.get('/users', (req, res) => {
  res.json({ version: 'v2', users: [], meta: { total: 0 } });
});

const app = express();
app.use('/v1', v1Router);
app.use('/v2', v2Router);
```

```python
# FastAPI - URL path versioning
from fastapi import FastAPI

app = FastAPI()

@app.get("/v1/users")
async def get_users_v1():
    return {"version": "v1", "users": []}

@app.get("/v2/users")
async def get_users_v2():
    return {"version": "v2", "users": [], "meta": {"total": 0}}
```

### Header Versioning

```
Version in HTTP header:
- GET /users HTTP/1.1
  Host: api.example.com
  Accept: application/json
  API-Version: v2

Pros:
- URL doesn't change
- Backward compatible
- Clean URLs

Cons:
- Less discoverable
- Requires header handling
```

```typescript
// Express - Header versioning
import express from 'express';

const app = express();

app.get('/users', (req, res) => {
  const version = req.headers['api-version'] || 'v1';

  if (version === 'v2') {
    return res.json({ version: 'v2', users: [], meta: { total: 0 } });
  }

  return res.json({ version: 'v1', users: [] });
});
```

```python
# FastAPI - Header versioning
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/users")
async def get_users(api_version: str = Header("API-Version", "v1")):
    if api_version == "v2":
        return {"version": "v2", "users": [], "meta": {"total": 0}}
    return {"version": "v1", "users": []}
```

### Query Parameter Versioning

```
Version in query parameter:
- https://api.example.com/users?version=v2
- https://api.example.com/users?version=v1

Pros:
- Simple to implement
- Backward compatible
- Easy to test

Cons:
- Pollutes URL
- Not standard
```

```typescript
// Express - Query parameter versioning
import express from 'express';

const app = express();

app.get('/users', (req, res) => {
  const version = req.query.version || 'v1';

  if (version === 'v2') {
    return res.json({ version: 'v2', users: [], meta: { total: 0 } });
  }

  return res.json({ version: 'v1', users: [] });
});
```

```python
# FastAPI - Query parameter versioning
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/users")
async def get_users(version: str = Query("v1")):
    if version == "v2":
        return {"version": "v2", "users": [], "meta": {"total": 0}}
    return {"version": "v1", "users": []}
```

---

## Implementation Patterns

### Versioned Router

```typescript
// routers/v1/users.ts
import express, { Request, Response } from 'express';

const router = express.Router();

router.get('/', (req: Request, res: Response) => {
  res.json({
    version: 'v1',
    users: [
      { id: 1, name: 'John Doe', email: 'john@example.com' },
    ],
  });
});

router.get('/:id', (req: Request, res: Response) => {
  const { id } = req.params;
  res.json({
    version: 'v1',
    user: { id, name: 'John Doe', email: 'john@example.com' },
  });
});

router.post('/', (req: Request, res: Response) => {
  const { name, email } = req.body;
  res.json({
    version: 'v1',
    user: { id: 1, name, email },
  });
});

export default router;
```

```typescript
// routers/v2/users.ts
import express, { Request, Response } from 'express';

const router = express.Router();

router.get('/', (req: Request, res: Response) => {
  res.json({
    version: 'v2',
    users: [
      { id: 1, name: 'John Doe', email: 'john@example.com', createdAt: '2024-01-01T00:00:00Z' },
    ],
    meta: {
      total: 1,
      page: 1,
      pageSize: 10,
    },
  });
});

router.get('/:id', (req: Request, res: Response) => {
  const { id } = req.params;
  res.json({
    version: 'v2',
    user: { id, name: 'John Doe', email: 'john@example.com', createdAt: '2024-01-01T00:00:00Z' },
  });
});

router.post('/', (req: Request, res: Response) => {
  const { name, email } = req.body;
  res.json({
    version: 'v2',
    user: { id: 1, name, email, createdAt: new Date().toISOString() },
  });
});

export default router;
```

```typescript
// app.ts
import express from 'express';
import v1UsersRouter from './routers/v1/users';
import v2UsersRouter from './routers/v2/users';

const app = express();

app.use('/v1/users', v1UsersRouter);
app.use('/v2/users', v2UsersRouter);

export default app;
```

### Versioned Controller

```python
# controllers/v1/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/v1/users")

@router.get("")
async def get_users():
    return {
        "version": "v1",
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"}
        ]
    }

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {
        "version": "v1",
        "user": {"id": user_id, "name": "John Doe", "email": "john@example.com"}
    }

@router.post("")
async def create_user(user: dict):
    return {
        "version": "v1",
        "user": {"id": 1, **user}
    }
```

```python
# controllers/v2/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/v2/users")

@router.get("")
async def get_users():
    return {
        "version": "v2",
        "users": [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "created_at": "2024-01-01T00:00:00Z"}
        ],
        "meta": {"total": 1, "page": 1, "page_size": 10}
    }

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {
        "version": "v2",
        "user": {"id": user_id, "name": "John Doe", "email": "john@example.com", "created_at": "2024-01-01T00:00:00Z"}
    }

@router.post("")
async def create_user(user: dict):
    return {
        "version": "v2",
        "user": {"id": 1, **user, "created_at": "2024-01-01T00:00:00Z"}
    }
```

```python
# app.py
from fastapi import FastAPI
from controllers.v1 import users as v1_users
from controllers.v2 import users as v2_users

app = FastAPI()

app.include_router(v1_users.router)
app.include_router(v2_users.router)
```

---

## Version Negotiation

### Content Negotiation

```typescript
// Express - Content negotiation
import express from 'express';

const app = express();

app.get('/users', (req, res) => {
  const accept = req.headers['accept'];

  if (accept?.includes('application/vnd.api.v2+json')) {
    return res.json({ version: 'v2', users: [], meta: { total: 0 } });
  }

  return res.json({ version: 'v1', users: [] });
});
```

```python
# FastAPI - Content negotiation
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/users")
async def get_users(accept: str = Header("Accept", "application/json")):
    if "application/vnd.api.v2+json" in accept:
        return {"version": "v2", "users": [], "meta": {"total": 0}}
    return {"version": "v1", "users": []}
```

### Version Selection Logic

```typescript
// Version selection based on header
function getApiVersion(headers: any, defaultVersion = 'v1'): string {
  const apiVersion = headers['api-version'];
  const accept = headers['accept'];

  // Priority: API-Version header > Accept header > default
  if (apiVersion) {
    return apiVersion;
  }

  if (accept?.includes('application/vnd.api.v2+json')) {
    return 'v2';
  }

  if (accept?.includes('application/vnd.api.v3+json')) {
    return 'v3';
  }

  return defaultVersion;
}

// Express middleware
import express from 'express';

const app = express();

app.use((req, res, next) => {
  req.apiVersion = getApiVersion(req.headers);
  next();
});

app.get('/users', (req, res) => {
  const version = req.apiVersion;
  res.json({ version, users: [] });
});
```

```python
# Version selection based on header
def get_api_version(headers: dict, default_version: str = "v1") -> str:
    api_version = headers.get("api-version")
    accept = headers.get("accept", "")

    # Priority: API-Version header > Accept header > default
    if api_version:
        return api_version

    if "application/vnd.api.v2+json" in accept:
        return "v2"

    if "application/vnd.api.v3+json" in accept:
        return "v3"

    return default_version

# FastAPI dependency
from fastapi import FastAPI, Header, Depends

def get_version(headers: dict = Header()) -> str:
    return get_api_version(headers)

app = FastAPI(dependencies=[get_version])

@app.get("/users")
async def get_users(version: str = Depends(get_version)):
    return {"version": version, "users": []}
```

---

## Deprecation Strategy

### Sunset Headers

```typescript
// Express - Sunset headers
import express from 'express';

const app = express();

app.get('/v1/users', (req, res) => {
  res.setHeader('Sunset', 'Wed, 01 Jan 2025 00:00:00 GMT');
  res.setHeader('Link', '<https://api.example.com/docs/migration>; rel="deprecation"; type="text/html"');
  res.setHeader('Deprecation', 'true');
  res.setHeader('Warning', '299 - "Deprecated API"');

  res.json({
    version: 'v1',
    users: [],
    deprecation: {
      message: 'This API is deprecated. Please use v2.',
      sunsetDate: '2025-01-01',
      migrationGuide: 'https://api.example.com/docs/migration',
    },
  });
});
```

```python
# FastAPI - Sunset headers
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/v1/users")
async def get_users():
    return JSONResponse(
        {
            "version": "v1",
            "users": [],
            "deprecation": {
                "message": "This API is deprecated. Please use v2.",
                "sunset_date": "2025-01-01T00:00:00Z",
                "migration_guide": "https://api.example.com/docs/migration"
            }
        },
        headers={
            "Sunset": "Wed, 01 Jan 2025 00:00:00 GMT",
            "Link": '<https://api.example.com/docs/migration>; rel="deprecation"; type="text/html"',
            "Deprecation": "true",
            "Warning": '299 - "Deprecated API"'
        }
    )
```

### Deprecation Warning

```typescript
// Add deprecation warning to response
interface ApiResponse<T> {
  version: string;
  data: T;
  deprecation?: {
    message: string;
    sunsetDate: string;
    migrationGuide: string;
  };
}

function createResponse<T>(
  version: string,
  data: T,
  deprecation?: ApiResponse<T>['deprecation']
): ApiResponse<T> {
  const response: ApiResponse<T> = { version, data };

  if (deprecation) {
    response.deprecation = deprecation;
  }

  return response;
}

// Usage
app.get('/v1/users', (req, res) => {
  const users = [];
  const response = createResponse('v1', users, {
    message: 'This API is deprecated. Please use v2.',
    sunsetDate: '2025-01-01T00:00:00Z',
    migrationGuide: 'https://api.example.com/docs/migration',
  });

  res.json(response);
});
```

---

## Migration Guides

### Migration Documentation

```markdown
# Migration Guide: v1 to v2

## What Changed?

### Breaking Changes
- `email` field renamed to `email_address`
- `name` field now includes first and last name
- Response format changed to include `meta` object

### New Features
- Pagination support
- Filtering support
- Sorting support

## Migration Steps

### Step 1: Update Request Format
**Old Format (v1):**
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**New Format (v2):**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email_address": "john@example.com"
}
```

### Step 2: Update Response Handling
**Old Response (v1):**
```json
{
  "users": [...]
}
```

**New Response (v2):**
```json
{
  "version": "v2",
  "users": [...],
  "meta": {
    "total": 100,
    "page": 1,
    "page_size": 10
  }
}
```

### Step 3: Update API Endpoint
- Change from `/v1/users` to `/v2/users`
- Update request body format
- Update response handling

### Step 4: Test
- Test new endpoint with new format
- Test backward compatibility

## Timeline
- **2024-01-01**: v2 released
- **2024-06-01**: v1 deprecated
- **2025-01-01**: v1 sunset
```

---

## Backward Compatibility

### Adapter Pattern

```typescript
// Adapter for v1 to v2
interface V1User {
  id: number;
  name: string;
  email: string;
}

interface V2User {
  id: number;
  firstName: string;
  lastName: string;
  emailAddress: string;
}

function v1ToV2Adapter(v1User: V1User): V2User {
  const [firstName, lastName] = v1User.name.split(' ');
  return {
    id: v1User.id,
    firstName,
    lastName,
    emailAddress: v1User.email,
  };
}

// Usage
app.get('/v1/users', (req, res) => {
  const v1Users: V1User[] = await getV1Users();
  const v2Users = v1Users.map(v1ToV2Adapter);

  res.json({ version: 'v2', users: v2Users });
});
```

```python
# Adapter for v1 to v2
from pydantic import BaseModel

class V1User(BaseModel):
    id: int
    name: str
    email: str

class V2User(BaseModel):
    id: int
    first_name: str
    last_name: str
    email_address: str

def v1_to_v2_adapter(v1_user: V1User) -> V2User:
    first_name, last_name = v1_user.name.split(' ', 1)
    return V2User(
        id=v1_user.id,
        first_name=first_name,
        last_name=last_name,
        email_address=v1_user.email
    )

# Usage
@app.get("/v1/users")
async def get_users():
    v1_users = await get_v1_users()
    v2_users = [v1_to_v2_adapter(user) for user in v1_users]
    return {"version": "v2", "users": v2_users}
```

### Version-Specific Controllers

```typescript
// Keep v1 controller for backward compatibility
import express, { Request, Response } from 'express';

const v1Router = express.Router();

v1Router.get('/users', (req: Request, res: Response) => {
  // v1 implementation
  res.json({ version: 'v1', users: [] });
});

v1Router.post('/users', (req: Request, res: Response) => {
  const { name, email } = req.body;
  // v1 implementation
  res.json({ version: 'v1', user: { id: 1, name, email } });
});

export default v1Router;
```

---

## Documentation

### OpenAPI Specification

```yaml
# openapi.yaml
openapi: 3.0.0
info:
  title: My API
  version: 2.0.0
  description: API with versioning support

servers:
  - url: https://api.example.com/v2
    description: v2 API (current)
  - url: https://api.example.com/v1
    description: v1 API (deprecated)

paths:
  /users:
    get:
      summary: Get users
      description: Retrieve list of users
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UsersResponse'
  /users/{userId}:
    get:
      summary: Get user by ID
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'

components:
  schemas:
    UserResponse:
      type: object
      properties:
        id:
          type: integer
        first_name:
          type: string
        last_name:
          type: string
        email_address:
          type: string
    UsersResponse:
      type: object
      properties:
        version:
          type: string
        users:
          type: array
          items:
            $ref: '#/components/schemas/UserResponse'
        meta:
          type: object
          properties:
            total:
              type: integer
            page:
              type: integer
            page_size:
              type: integer
```

---

## Testing Multiple Versions

### Version-Specific Tests

```typescript
// tests/v1/users.test.ts
import request from 'supertest';
import { app } from '../../app';

describe('V1 Users API', () => {
  it('should get users', async () => {
    const response = await request(app)
      .get('/v1/users')
      .expect(200)
      .expect('Content-Type', /json/);

    expect(response.body.version).toBe('v1');
    expect(Array.isArray(response.body.users)).toBe(true);
  });

  it('should create user', async () => {
    const response = await request(app)
      .post('/v1/users')
      .send({ name: 'John Doe', email: 'john@example.com' })
      .expect(201)
      .expect('Content-Type', /json/);

    expect(response.body.version).toBe('v1');
    expect(response.body.user.name).toBe('John Doe');
  });
});
```

```typescript
// tests/v2/users.test.ts
import request from 'supertest';
import { app } from '../../app';

describe('V2 Users API', () => {
  it('should get users with pagination', async () => {
    const response = await request(app)
      .get('/v2/users?page=1&pageSize=10')
      .expect(200)
      .expect('Content-Type', /json/);

    expect(response.body.version).toBe('v2');
    expect(response.body.meta).toEqual({
      total: expect.any(Number),
      page: 1,
      pageSize: 10,
    });
  });

  it('should create user with new format', async () => {
    const response = await request(app)
      .post('/v2/users')
      .send({ firstName: 'John', lastName: 'Doe', emailAddress: 'john@example.com' })
      .expect(201)
      .expect('Content-Type', /json/);

    expect(response.body.version).toBe('v2');
    expect(response.body.user.firstName).toBe('John');
  });
});
```

---

## Sunset Headers

### Sunset Header Format

```typescript
// Sunset header format
function setSunsetHeaders(
  res: any,
  sunsetDate: Date,
  link: string,
  deprecation: boolean = true
): void {
  res.setHeader('Sunset', sunsetDate.toUTCString());
  res.setHeader('Link', `<${link}>; rel="deprecation"; type="text/html"`);
  res.setHeader('Deprecation', deprecation.toString());
  res.setHeader('Warning', '299 - "Deprecated API"');
}

// Usage
app.get('/v1/users', (req, res) => {
  setSunsetHeaders(
    res,
    new Date('2025-01-01'),
    'https://api.example.com/docs/migration',
    true
  );

  res.json({ version: 'v1', users: [] });
});
```

```python
# Sunset header format
from fastapi import Response
from datetime import datetime

def set_sunset_headers(
    response: Response,
    sunset_date: datetime,
    link: str,
    deprecation: bool = True
):
    response.headers["Sunset"] = sunset_date.strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.headers["Link"] = f'<{link}>; rel="deprecation"; type="text/html"'
    response.headers["Deprecation"] = str(deprecation)
    response.headers["Warning"] = '299 - "Deprecated API"'

# Usage
@app.get("/v1/users")
async def get_users():
    response = Response(
        content={"version": "v1", "users": []},
        media_type="application/json"
    )
    set_sunset_headers(
        response,
        datetime(2025, 1, 1),
        "https://api.example.com/docs/migration"
    )
    return response
```

---

## Best Practices

### 1. Use Semantic Versioning

```typescript
// Use semantic versioning
const API_VERSION = '2.0.0'; // MAJOR.MINOR.PATCH
```

### 2. Document Changes

```markdown
# Changelog

## [2.0.0] - 2024-01-01
### Added
- Pagination support
- Filtering support
- Sorting support

### Changed
- `email` field renamed to `email_address`
- `name` field split into `first_name` and `last_name`

### Deprecated
- `/v1/users` endpoint
- Old request format

### Removed
- None

### Fixed
- Bug in user creation
```

### 3. Use Sunset Headers

```typescript
// Always set sunset headers for deprecated versions
res.setHeader('Sunset', '2025-01-01T00:00:00Z');
res.setHeader('Deprecation', 'true');
```

### 4. Provide Migration Guides

```typescript
// Link to migration guide
res.setHeader('Link', '<https://api.example.com/docs/migration>; rel="deprecation"; type="text/html"');
```

### 5. Test Multiple Versions

```typescript
// Test both v1 and v2
describe('API Versioning', () => {
  describe('V1', () => {
    // v1 tests
  });

  describe('V2', () => {
    // v2 tests
  });
});
```

### 6. Use Version in Response

```typescript
// Always include version in response
res.json({
  version: 'v2',
  data: {},
});
```

### 7. Support Multiple Versions

```typescript
// Keep old versions for backward compatibility
app.use('/v1', v1Router);
app.use('/v2', v2Router);
app.use('/v3', v3Router);
```

### 8. Monitor Version Usage

```typescript
// Track which versions are being used
app.use((req, res, next) => {
  const version = req.apiVersion;
  metrics.record('api_version_usage', 1, { version });
  next();
});
```

### 9. Communicate Changes Early

```typescript
// Communicate changes early
res.setHeader('Deprecation', 'true');
res.setHeader('Warning', '299 - "This API will be deprecated on 2025-01-01"');
```

### 10. Use Version-Specific Errors

```typescript
// Version-specific error codes
class ApiVersionError extends Error {
  constructor(
    public version: string,
    public code: string,
    public message: string
  ) {
    super(message);
    this.name = 'ApiVersionError';
  }
}

// Usage
throw new ApiVersionError('v1', 'DEPRECATED', 'This API is deprecated');
```

---

## Resources

- [API Versioning Best Practices](https://restfulapi.net/versioning/)
- [HTTP API Versioning](https://www.vinaysahni.com/api-versioning/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [REST API Design](https://restfulapi.net/)
