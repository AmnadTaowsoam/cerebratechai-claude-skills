---
name: API Design Contracts
description: API contract-first design using OpenAPI/Swagger, AsyncAPI for events, versioning strategies, backward compatibility, and contract testing
---

# API Design Contracts

## Overview

API contract-first design ใช้ OpenAPI/Swagger สำหรับ REST และ AsyncAPI สำหรับ events เพื่อสร้าง contract ที่ชัดเจน สนับสนุน backward compatibility และ enable contract testing ระหว่าง services

## Why This Matters

- **Contract-first**: Design API ก่อน implement ลด rework
- **Type safety**: Auto-generate clients จาก contract
- **Backward compatibility**: Versioning strategy ที่ชัดเจน
- **Contract testing**: Detect breaking changes early

---

## Core Concepts

### 1. OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: Example API
  version: 1.0.0
  description: API contract example
servers:
  - url: https://api.example.com/v1
    description: Production server

paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      tags:
        - users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
        - name: cursor
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
    post:
      summary: Create user
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        createdAt:
          type: string
          format: date-time
        updatedAt:
          type: string
          format: date-time

    CreateUserRequest:
      type: object
      required:
        - email
        - name
      properties:
        email:
          type: string
          format: email
        name:
          type: string
          minLength: 1
          maxLength: 100

    Pagination:
      type: object
      properties:
        cursor:
          type: string
        hasMore:
          type: boolean
```

### 2. AsyncAPI Specification

```yaml
asyncapi: '2.6.0'
info:
  title: User Events API
  version: '1.0.0'
  description: Events for user lifecycle

servers:
  production:
    url: broker.example.com
    protocol: kafka
    description: Production Kafka broker

channels:
  user.created:
    publish:
      summary: User created event
      message:
        name: UserCreated
        payload:
          type: object
          required:
            - userId
            - email
            - name
            - timestamp
          properties:
            userId:
              type: string
              format: uuid
            email:
              type: string
              format: email
            name:
              type: string
            timestamp:
              type: string
              format: date-time

  user.updated:
    publish:
      summary: User updated event
      message:
        name: UserUpdated
        payload:
          type: object
          required:
            - userId
            - timestamp
          properties:
            userId:
              type: string
              format: uuid
            changes:
              type: object
              additionalProperties: true
            timestamp:
              type: string
              format: date-time

components:
  schemas:
    UserCreated:
      type: object
      required:
        - userId
        - email
        - name
        - timestamp
      properties:
        userId:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        timestamp:
          type: string
          format: date-time
```

### 3. Versioning Strategy

**URL Versioning (Recommended):**
```yaml
servers:
  - url: https://api.example.com/v1
    description: Version 1 (current)
  - url: https://api.example.com/v2
    description: Version 2 (new features)
```

**Header Versioning:**
```yaml
paths:
  /users:
    get:
      parameters:
        - name: API-Version
          in: header
          schema:
            type: string
            enum: ['1.0', '2.0']
            default: '1.0'
```

**Versioning Rules:**
- Breaking changes = new major version
- Additive changes = same version
- Deprecation period = minimum 6 months
- Sunset policy = documented and communicated

### 4. Backward Compatibility

**Additive Changes (Safe):**
```yaml
# Add new optional field
properties:
  email:
    type: string
  phone:  # New optional field
    type: string
```

**Breaking Changes (New Version):**
```yaml
# Change field type
properties:
  userId:
    type: string  # Changed from integer
```

**Deprecation Pattern:**
```yaml
paths:
  /users:
    get:
      deprecated: true
      x-deprecation-date: '2026-06-01'
      x-sunset-date: '2026-12-01'
      x-migration-guide: 'https://docs.example.com/migration/v1-to-v2'
```

### 5. Contract Testing

**Pact (Consumer-Driven Contracts):**
```typescript
// Consumer test
import { Pact } from '@pact-foundation/pact'
import { expect } from 'chai'

describe('User API Consumer', () => {
  const provider = new Pact({
    consumer: 'frontend-app',
    provider: 'user-service',
    port: 1234,
  })

  before(() => provider.setup())
  after(() => provider.finalize())

  it('should get user list', async () => {
    await provider.addInteraction({
      state: 'users exist',
      uponReceiving: 'a request for users',
      withRequest: {
        method: 'GET',
        path: '/api/v1/users',
        query: { limit: '20' },
      },
      willRespondWith: {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: {
          data: eachLike({
            id: like('123e4567-e89b-12d3-a456-426614174000'),
            email: like('user@example.com'),
            name: like('John Doe'),
          }),
          pagination: {
            cursor: like('abc123'),
            hasMore: false,
          },
        },
      },
    })

    const response = await fetch('http://localhost:1234/api/v1/users?limit=20')
    const data = await response.json()

    expect(data.data).to.be.an('array')
  })
})
```

**Provider Verification:**
```typescript
// Provider verification
import { Verifier } from '@pact-foundation/pact'

describe('User API Provider', () => {
  it('should validate consumer contracts', async () => {
    const verifier = new Verifier({
      providerBaseUrl: 'http://localhost:3000',
      pactUrls: ['./pacts/frontend-app-user-service.json'],
    })

    await verifier.verify()
  })
})
```

### 6. Schema Validation

**Request Validation:**
```typescript
import Ajv from 'ajv'

const ajv = new Ajv()

// Validate request against OpenAPI schema
function validateRequest(schema: any, data: any) {
  const validate = ajv.compile(schema)
  const valid = validate(data)

  if (!valid) {
    throw new Error(`Validation failed: ${JSON.stringify(validate.errors)}`)
  }

  return data
}

// Usage
const createUserSchema = {
  type: 'object',
  required: ['email', 'name'],
  properties: {
    email: { type: 'string', format: 'email' },
    name: { type: 'string', minLength: 1, maxLength: 100 },
  },
}

validateRequest(createUserSchema, requestBody)
```

### 7. Code Generation

**Generate TypeScript Types:**
```bash
# Using openapi-typescript-codegen
npx openapi-typescript-codegen -i openapi.yaml -o ./src/api
```

**Generated Types:**
```typescript
// Auto-generated from OpenAPI
export interface User {
  id: string
  email: string
  name: string
  createdAt: string
  updatedAt: string
}

export interface CreateUserRequest {
  email: string
  name: string
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    cursor: string
    hasMore: boolean
  }
}
```

## Quick Start

1. **Create OpenAPI spec:**
```bash
npm install -g @apidevtools/swagger-cli
swagger-cli validate openapi.yaml
```

2. **Generate types:**
```bash
npx openapi-typescript openapi.yaml -o src/api/types.ts
```

3. **Set up contract testing:**
```bash
npm install --save-dev @pact-foundation/pact
```

4. **Generate API client:**
```bash
npx openapi-typescript-codegen -i openapi.yaml -o ./src/api
```

## Production Checklist

- [ ] OpenAPI/AsyncAPI spec exists and is valid
- [ ] Versioning strategy documented
- [ ] Backward compatibility guidelines defined
- [ ] Contract tests implemented
- [ ] Schema validation in place
- [ ] Type generation automated
- [ ] Deprecation policy documented
- [ ] Breaking change detection in CI

## Anti-patterns

1. **Code-first without contract**: Implement API ก่อน สร้าง contract ทีหลัง
2. **No versioning**: Breaking changes ทำให้ clients พัง
3. **Ignoring deprecation**: ลบ old version โดยไม่แจ้งล่วงหน้า
4. **Loose contracts**: Schema ไม่ชัดเจน ทำให้ type safety หายไป
5. **No contract testing**: Breaking changes รั่วไป production

## Integration Points

- API gateways
- Client SDK generators
- Contract testing frameworks
- CI/CD pipelines
- Documentation tools

## Further Reading

- [OpenAPI Specification](https://swagger.io/specification/)
- [AsyncAPI Specification](https://www.asyncapi.com/docs/specifications/latest)
- [Pact Contract Testing](https://docs.pact.io/)
- [API Versioning Best Practices](https://restfulapi.net/versioning/)
