# API Versioning

## Overview

API versioning allows you to evolve your API while maintaining backward compatibility. This skill covers versioning approaches (URL path, header, query parameter), implementation patterns, version negotiation, deprecation strategy, migration guides, backward compatibility, documentation, testing multiple versions, sunset headers, and best practices.

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

```typescript
// src/routes/v1/user.routes.ts
import express from 'express';

const router = express.Router();

router.get('/users', async (req, res) => {
  const users = await User.findAll();
  res.json(users);
});

router.get('/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user);
});

router.post('/users', async (req, res) => {
  const user = await User.create(req.body);
  res.status(201).json(user);
});

export default router;
```

```typescript
// src/routes/v2/user.routes.ts
import express from 'express';

const router = express.Router();

router.get('/users', async (req, res) => {
  const users = await User.findAll();
  res.json(users);
});

router.get('/users/:id', async (req, res) => {
  const user = await User.findById(req.params.id);
  res.json(user);
});

router.post('/users', async (req, res) => {
  const user = await User.create(req.body);
  res.status(201).json(user);
});

export default router;
```

```typescript
// src/app.ts
import express from 'express';
import v1Routes from './routes/v1/user.routes';
import v2Routes from './routes/v2/user.routes';

const app = express();

// Mount v1 routes
app.use('/api/v1', v1Routes);

// Mount v2 routes
app.use('/api/v2', v2Routes);

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### Header Versioning

```typescript
// src/middleware/version.middleware.ts
import { Request, Response, NextFunction } from 'express';

export function versionMiddleware(req: Request, res: Response, next: NextFunction) {
  const version = req.headers['api-version'] as string || 'v1';
  
  if (!['v1', 'v2'].includes(version)) {
    return res.status(400).json({
      error: 'Invalid API version',
      supported: ['v1', 'v2'],
    });
  }
  
  req.apiVersion = version;
  next();
}
```

```typescript
// src/controllers/user.controller.ts
import { Request, Response } from 'express';

export class UserController {
  async getUsers(req: Request, res: Response) {
    const version = req.apiVersion || 'v1';
    
    let users;
    if (version === 'v1') {
      users = await User.findAll();
    } else if (version === 'v2') {
      users = await User.findAllWithRelations();
    }
    
    res.json(users);
  }

  async getUser(req: Request, res: Response) {
    const version = req.apiVersion || 'v1';
    
    let user;
    if (version === 'v1') {
      user = await User.findById(req.params.id);
    } else if (version === 'v2') {
      user = await User.findByIdWithRelations(req.params.id);
    }
    
    res.json(user);
  }
}
```

```typescript
// src/app.ts
import express from 'express';
import { versionMiddleware } from './middleware/version.middleware';
import { UserController } from './controllers/user.controller';

const app = express();
const userController = new UserController();

app.use(versionMiddleware);

app.get('/users', userController.getUsers.bind(userController));
app.get('/users/:id', userController.getUser.bind(userController));

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### Query Parameter Versioning

```typescript
// src/middleware/query-version.middleware.ts
import { Request, Response, NextFunction } from 'express';

export function queryVersionMiddleware(req: Request, res: Response, next: NextFunction) {
  const version = req.query.version as string || 'v1';
  
  if (!['v1', 'v2'].includes(version)) {
    return res.status(400).json({
      error: 'Invalid API version',
      supported: ['v1', 'v2'],
    });
  }
  
  req.apiVersion = version;
  next();
}
```

```typescript
// src/app.ts
import express from 'express';
import { queryVersionMiddleware } from './middleware/query-version.middleware';
import { UserController } from './controllers/user.controller';

const app = express();
const userController = new UserController();

app.use(queryVersionMiddleware);

app.get('/users', userController.getUsers.bind(userController));
app.get('/users/:id', userController.getUser.bind(userController));

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

---

## Implementation Patterns

### Versioned Controllers

```typescript
// src/controllers/v1/user.controller.ts
import { Request, Response } from 'express';

export class V1UserController {
  async getUsers(req: Request, res: Response) {
    const users = await User.findAll();
    res.json(users);
  }

  async getUser(req: Request, res: Response) {
    const user = await User.findById(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  }

  async createUser(req: Request, res: Response) {
    const user = await User.create(req.body);
    res.status(201).json(user);
  }

  async updateUser(req: Request, res: Response) {
    const user = await User.update(req.params.id, req.body);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  }

  async deleteUser(req: Request, res: Response) {
    await User.delete(req.params.id);
    res.status(204).send();
  }
}
```

```typescript
// src/controllers/v2/user.controller.ts
import { Request, Response } from 'express';

export class V2UserController {
  async getUsers(req: Request, res: Response) {
    const users = await User.findAllWithRelations();
    res.json(users);
  }

  async getUser(req: Request, res: Response) {
    const user = await User.findByIdWithRelations(req.params.id);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  }

  async createUser(req: Request, res: Response) {
    const user = await User.createWithRelations(req.body);
    res.status(201).json(user);
  }

  async updateUser(req: Request, res: Response) {
    const user = await User.updateWithRelations(req.params.id, req.body);
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }
    res.json(user);
  }

  async deleteUser(req: Request, res: Response) {
    await User.deleteWithRelations(req.params.id);
    res.status(204).send();
  }
}
```

### Versioned Services

```typescript
// src/services/v1/user.service.ts
export class V1UserService {
  async findAll(): Promise<User[]> {
    return User.findAll();
  }

  async findById(id: string): Promise<User | null> {
    return User.findById(id);
  }

  async create(data: CreateUserData): Promise<User> {
    return User.create(data);
  }

  async update(id: string, data: UpdateUserData): Promise<User | null> {
    return User.update(id, data);
  }

  async delete(id: string): Promise<void> {
    return User.delete(id);
  }
}
```

```typescript
// src/services/v2/user.service.ts
export class V2UserService {
  async findAll(): Promise<UserWithRelations[]> {
    return User.findAllWithRelations();
  }

  async findById(id: string): Promise<UserWithRelations | null> {
    return User.findByIdWithRelations(id);
  }

  async create(data: CreateUserData): Promise<UserWithRelations> {
    return User.createWithRelations(data);
  }

  async update(id: string, data: UpdateUserData): Promise<UserWithRelations | null> {
    return User.updateWithRelations(id, data);
  }

  async delete(id: string): Promise<void> {
    return User.deleteWithRelations(id);
  }
}
```

---

## Version Negotiation

### Content Negotiation

```typescript
// src/middleware/content-negotiation.middleware.ts
import { Request, Response, NextFunction } from 'express';

export function contentNegotiationMiddleware(req: Request, res: Response, next: NextFunction) {
  const accept = req.headers.accept || 'application/json';
  const version = req.headers['api-version'] as string || 'v1';
  
  // Check if requested version is supported
  if (!['v1', 'v2'].includes(version)) {
    return res.status(400).json({
      error: 'Unsupported API version',
      supported: ['v1', 'v2'],
    });
  }
  
  // Check if requested content type is supported
  if (!accept.includes('application/json')) {
    return res.status(406).json({
      error: 'Unsupported content type',
      supported: ['application/json'],
    });
  }
  
  req.apiVersion = version;
  req.contentType = accept;
  next();
}
```

### Version Routing

```typescript
// src/middleware/version-routing.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { V1UserController } from '../controllers/v1/user.controller';
import { V2UserController } from '../controllers/v2/user.controller';

const v1Controller = new V1UserController();
const v2Controller = new V2UserController();

export function versionRoutingMiddleware(req: Request, res: Response, next: NextFunction) {
  const version = req.apiVersion || 'v1';
  
  // Route to appropriate controller based on version
  if (version === 'v1') {
    req.userController = v1Controller;
  } else if (version === 'v2') {
    req.userController = v2Controller;
  }
  
  next();
}
```

---

## Deprecation Strategy

### Deprecation Middleware

```typescript
// src/middleware/deprecation.middleware.ts
import { Request, Response, NextFunction } from 'express';

interface DeprecationConfig {
  version: string;
  deprecationDate: Date;
  sunsetDate: Date;
  recommendedVersion: string;
  migrationGuide: string;
}

const deprecationConfigs: Map<string, DeprecationConfig> = new Map([
  ['v1', {
    version: 'v1',
    deprecationDate: new Date('2024-01-01'),
    sunsetDate: new Date('2024-06-01'),
    recommendedVersion: 'v2',
    migrationGuide: 'https://docs.example.com/migration/v1-to-v2',
  }],
]);

export function deprecationMiddleware(req: Request, res: Response, next: NextFunction) {
  const version = req.apiVersion || 'v1';
  const config = deprecationConfigs.get(version);
  
  if (config) {
    const now = new Date();
    
    // Add deprecation headers
    res.setHeader('Deprecation', `true; version="${config.version}"; date="${config.deprecationDate.toISOString()}"`);
    res.setHeader('Sunset', config.sunsetDate.toISOString());
    res.setHeader('Link', `<${config.migrationGuide}>; rel="deprecation"; type="text/html"`);
    
    // Check if version is sunset
    if (now >= config.sunsetDate) {
      return res.status(410).json({
        error: 'API version sunset',
        message: `Version ${config.version} is no longer supported`,
        recommendedVersion: config.recommendedVersion,
        migrationGuide: config.migrationGuide,
      });
    }
    
    // Add warning header if deprecated
    if (now >= config.deprecationDate) {
      res.setHeader('Warning', `299 - "Deprecated API version ${config.version}, use ${config.recommendedVersion} instead"`);
    }
  }
  
  next();
}
```

### Deprecation Response

```typescript
// src/middleware/deprecation-response.middleware.ts
import { Request, Response, NextFunction } from 'express';

export function deprecationResponseMiddleware(req: Request, res: Response, next: NextFunction) {
  const version = req.apiVersion || 'v1';
  
  // Add deprecation info to response body
  const originalJson = res.json.bind(res);
  
  res.json = function(data: any) {
    if (version === 'v1') {
      return originalJson({
        ...data,
        _meta: {
          version,
          deprecated: true,
          sunsetDate: '2024-06-01',
          recommendedVersion: 'v2',
          migrationGuide: 'https://docs.example.com/migration/v1-to-v2',
        },
      });
    }
    
    return originalJson(data);
  };
  
  next();
}
```

---

## Migration Guides

### Migration Documentation

```markdown
# API Migration Guide: v1 to v2

## Overview

API v1 will be deprecated on January 1, 2024 and sunset on June 1, 2024. This guide helps you migrate to v2.

## Breaking Changes

### 1. Response Format

**v1 Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

**v2 Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z"
}
```

### 2. Endpoint Changes

| v1 Endpoint | v2 Endpoint | Notes |
|-------------|-------------|--------|
| GET /api/v1/users | GET /api/v2/users | Added pagination |
| GET /api/v1/users/:id | GET /api/v2/users/:id | Added relationships |
| POST /api/v1/users | POST /api/v2/users | Changed request body |

### 3. Request Body Changes

**v1 Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**v2 Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zipCode": "10001"
  }
}
```

## Migration Steps

1. **Update your API version header:**
   ```javascript
   headers: {
     'API-Version': 'v2'
   }
   ```

2. **Update request bodies:**
   - Add new required fields
   - Update field names if changed

3. **Update response handling:**
   - Handle new response fields
   - Update data transformation logic

4. **Test your integration:**
   - Use our staging environment
   - Test all endpoints
   - Verify data integrity

## Support

If you need help with migration, contact us at:
- Email: support@example.com
- Documentation: https://docs.example.com
- Migration Guide: https://docs.example.com/migration/v1-to-v2
```

---

## Backward Compatibility

### Adapter Pattern

```typescript
// src/adapters/v1-to-v2.adapter.ts
export class V1ToV2Adapter {
  static adaptUser(user: V1User): V2User {
    return {
      id: user.id,
      name: user.name,
      email: user.email,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
  }

  static adaptUsers(users: V1User[]): V2User[] {
    return users.map(user => this.adaptUser(user));
  }
}

export class V2ToV1Adapter {
  static adaptUser(user: V2User): V1User {
    return {
      id: user.id,
      name: user.name,
      email: user.email,
    };
  }

  static adaptUsers(users: V2User[]): V1User[] {
    return users.map(user => this.adaptUser(user));
  }
}
```

### Compatibility Layer

```typescript
// src/middleware/compatibility.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { V1ToV2Adapter } from '../adapters/v1-to-v2.adapter';

export function compatibilityMiddleware(req: Request, res: Response, next: NextFunction) {
  const version = req.apiVersion || 'v1';
  
  // Transform request body if needed
  if (version === 'v1' && req.body) {
    req.body = this.transformRequestBody(req.body);
  }
  
  // Transform response if needed
  const originalJson = res.json.bind(res);
  
  res.json = function(data: any) {
    if (version === 'v1' && data) {
      data = this.transformResponseBody(data);
    }
    return originalJson(data);
  };
  
  next();
}

private transformRequestBody(body: any): any {
  // Transform v1 request to v2 format
  return body;
}

private transformResponseBody(body: any): any {
  // Transform v2 response to v1 format
  if (Array.isArray(body)) {
    return V1ToV2Adapter.adaptUsers(body);
  }
  return V1ToV2Adapter.adaptUser(body);
}
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
  description: API documentation with versioning
servers:
  - url: https://api.example.com/v1
    description: API v1 (Deprecated)
  - url: https://api.example.com/v2
    description: API v2 (Current)

paths:
  /users:
    get:
      summary: Get all users
      description: Retrieve a list of users
      tags:
        - Users
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    post:
      summary: Create a user
      description: Create a new user
      tags:
        - Users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
          format: email
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    CreateUser:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
        email:
          type: string
          format: email
```

---

## Testing Multiple Versions

### Version-Aware Tests

```typescript
// test/api/versioning.test.ts
import { describe, it, expect } from '@jest/globals';
import request from 'supertest';
import app from '../src/app';

describe('API Versioning', () => {
  describe('v1 API', () => {
    it('should return v1 response format', async () => {
      const response = await request(app)
        .get('/api/v1/users')
        .expect(200);

      expect(response.body[0]).toHaveProperty('id');
      expect(response.body[0]).toHaveProperty('name');
      expect(response.body[0]).toHaveProperty('email');
      expect(response.body[0]).not.toHaveProperty('createdAt');
    });

    it('should accept v1 request format', async () => {
      const response = await request(app)
        .post('/api/v1/users')
        .send({
          name: 'John Doe',
          email: 'john@example.com',
        })
        .expect(201);

      expect(response.body).toHaveProperty('id');
      expect(response.body.name).toBe('John Doe');
    });
  });

  describe('v2 API', () => {
    it('should return v2 response format', async () => {
      const response = await request(app)
        .get('/api/v2/users')
        .expect(200);

      expect(response.body[0]).toHaveProperty('id');
      expect(response.body[0]).toHaveProperty('name');
      expect(response.body[0]).toHaveProperty('email');
      expect(response.body[0]).toHaveProperty('createdAt');
      expect(response.body[0]).toHaveProperty('updatedAt');
    });

    it('should accept v2 request format', async () => {
      const response = await request(app)
        .post('/api/v2/users')
        .send({
          name: 'John Doe',
          email: 'john@example.com',
          phone: '+1234567890',
        })
        .expect(201);

      expect(response.body).toHaveProperty('id');
      expect(response.body.name).toBe('John Doe');
    });
  });
});
```

---

## Sunset Headers

### Sunset Header Implementation

```typescript
// src/middleware/sunset.middleware.ts
import { Request, Response, NextFunction } from 'express';

interface SunsetConfig {
  version: string;
  sunsetDate: Date;
  recommendedVersion: string;
  migrationGuide: string;
}

const sunsetConfigs: Map<string, SunsetConfig> = new Map([
  ['v1', {
    version: 'v1',
    sunsetDate: new Date('2024-06-01'),
    recommendedVersion: 'v2',
    migrationGuide: 'https://docs.example.com/migration/v1-to-v2',
  }],
]);

export function sunsetMiddleware(req: Request, res: Response, next: NextFunction) {
  const version = req.apiVersion || 'v1';
  const config = sunsetConfigs.get(version);
  
  if (config) {
    const now = new Date();
    const daysUntilSunset = Math.ceil((config.sunsetDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    
    // Add sunset header
    res.setHeader('Sunset', config.sunsetDate.toISOString());
    
    // Add link header
    res.setHeader('Link', `<${config.migrationGuide}>; rel="sunset"; type="text/html"`);
    
    // Add warning header if close to sunset
    if (daysUntilSunset <= 30) {
      res.setHeader('Warning', `299 - "API version ${config.version} will be sunset on ${config.sunsetDate.toISOString()}, migrate to ${config.recommendedVersion}"`);
    }
    
    // Reject requests after sunset
    if (now >= config.sunsetDate) {
      return res.status(410).json({
        error: 'API version sunset',
        message: `Version ${config.version} is no longer supported`,
        recommendedVersion: config.recommendedVersion,
        migrationGuide: config.migrationGuide,
      });
    }
  }
  
  next();
}
```

---

## Best Practices

### 1. Use Semantic Versioning

```typescript
// Good: Semantic versioning
const API_VERSION = '2.1.0'; // MAJOR.MINOR.PATCH

// MAJOR: Incompatible API changes
// MINOR: Backwards-compatible functionality
// PATCH: Backwards-compatible bug fixes

// Bad: Arbitrary versioning
const API_VERSION = 'v2'; // No semantic meaning
```

### 2. Document Changes Clearly

```markdown
# Good: Clear documentation

## Breaking Changes

### User Endpoint

**Before (v1):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```

**After (v2):**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2024-01-01T00:00:00Z",
  "updatedAt": "2024-01-01T00:00:00Z"
}
```

**Migration:** Update your code to handle the new `createdAt` and `updatedAt` fields.

# Bad: No documentation
```

### 3. Provide Deprecation Warnings

```typescript
// Good: Deprecation warnings
res.setHeader('Deprecation', 'true; version="v1"; date="2024-01-01"');
res.setHeader('Sunset', '2024-06-01');
res.setHeader('Warning', '299 - "Deprecated API version v1, use v2 instead"');

// Bad: No warnings
// No headers
```

### 4. Maintain Backward Compatibility

```typescript
// Good: Backward compatibility
if (version === 'v1') {
  return v1Response;
} else if (version === 'v2') {
  return v2Response;
}

// Bad: Breaking changes without notice
// Only v2 response, v1 clients break
```

### 5. Test All Versions

```typescript
// Good: Test all versions
describe('API Versioning', () => {
  describe('v1 API', () => {
    it('should work correctly', async () => {
      // Test v1
    });
  });

  describe('v2 API', () => {
    it('should work correctly', async () => {
      // Test v2
    });
  });
});

// Bad: Only test latest version
describe('API', () => {
  it('should work correctly', async () => {
    // Only test v2
  });
});
```

---

## Summary

This skill covers comprehensive API versioning patterns including:

- **Versioning Approaches**: URL path, header, query parameter versioning
- **Implementation Patterns**: Versioned controllers, versioned services
- **Version Negotiation**: Content negotiation, version routing
- **Deprecation Strategy**: Deprecation middleware, deprecation responses
- **Migration Guides**: Documentation, breaking changes, migration steps
- **Backward Compatibility**: Adapter pattern, compatibility layer
- **Documentation**: OpenAPI specification
- **Testing Multiple Versions**: Version-aware tests
- **Sunset Headers**: Sunset header implementation
- **Best Practices**: Semantic versioning, clear documentation, deprecation warnings, backward compatibility, testing
