### **01: RESTful API Design Principles**

> 
> **Current Level:** Expert (Enterprise Scale) 
> 
> 
> **Domain:** Foundations / Backend Development 
> 

---

### **1. Executive Summary & Strategic Necessity**

* **Context:** ในโลกปี 2025-2026 การออกแบบ RESTful API เป็นทักษะสำคัญที่มีผลกระทบต่อความสามารถในการขยายระบบและประสิทธิภาพของทีมพัฒนา API ที่ดีจะช่วยลด Technical Debt ที่เกิดจากการออกแบบ API ที่ไม่ดี และช่วยให้ผู้ใช้งาน (Developers, Partners, Customers) ได้สร้าง Integration ได้อย่างรวดเร็วและเสถียร
* **Business Impact:** การออกแบบ RESTful API ที่มีประสิทธิภาพช่วย:
  - ลดเวลาในการพัฒนา Integration ใหม่
  - เพิ่มความพึงพอใจของผู้ใช้งาน (Developers)
  - ลดความเสี่ยงที่อาจเกิดจากการเรียก API ที่ไม่ถูกต้อง
  - เพิ่มความเสถียรและ Performance ของระบบ
  - ลดต้นทุนในการบำรุงและการแก้ไข
  - เพิ่มประสิทธิภาพในการวางแผน Roadmap และการจัดการ Version
* **Product Thinking:** ทักษะนี้ช่วยแก้ปัญหา (Pain Point) ให้กับ:
  - ทีมพัฒนาที่ต้องการ API ที่เอกสารอย่างชัดเจนและใช้งานได้ง่าย
  - ผู้ใช้งาน (Partners) ที่ต้องการ API ที่เสถียรและมีการรองรับที่ดี
  - ลูกค้าที่ต้องการ API ที่ตอบสนองรวดเร็ว
  - ทีม Support ที่ต้องการ API ที่มี Error Messages ที่ชัดเจน
  - ผู้บริหารที่ต้องการ API ที่สามารถวัดและวิเคราะห์การใช้งานได้

### **2. Technical Deep Dive (The "How-to")**

* **Core Logic:** RESTful API Design เป็นกระบวนการที่ช่วยให้:
  - **Resource-First Thinking:** การออกแบบ API รอบ Resources (Nouns) ไม่ใช่ Actions (Verbs)
  - **Consistency:** การใช้ Naming Conventions, Response Formats, Error Handling ที่สอดคล้องกัน
  - **HTTP Semantics:** การใช้ HTTP Methods และ Status Codes ตามความหมายของแต่ละ Method
  - **Statelessness:** แต่ละ Request ต้องมีข้อมูลครบถ้วน ไม่ต้องพึ่พึง Session บน Server
  - **Versioning:** การวางแผนการเปลี่ยนแปลง API ตั้งแต่เริ่ม
  - **Security:** การใช้ Authentication, Authorization, Rate Limiting, Input Validation

* **Architecture Diagram Requirements:** แผนผังสถาปัตยกรรมที่ต้องมี:
  - **API Resource Hierarchy:** แผนผังแสดงความสัมพันธ์ระหว่าง Resources
  - **Request/Response Flow:** แผนผังแสดงการไหลของ Request และ Response
  - **Authentication Flow:** แผนผังแสดงการ Authentication และ Authorization
  - **Error Handling Flow:** แผนผังแสดงการจัดการ Error
  - **Versioning Strategy:** แผนผังแสดงการจัดการ Version ของ API

* **Implementation Workflow:**
  1. **Define Resources:** ระบุ Resources ทั้งหมดที่ API จะให้บริการ
  2. **Design Endpoints:** ออกแบบ Endpoints ตาม RESTful Principles
  3. **Define Request/Response Formats:** กำหนด Format ของ Request และ Response
  4. **Define Error Handling:** กำหนด Error Response Format และ Error Codes
  5. **Implement Authentication/Authorization:** สร้างระบบ Authentication และ Authorization
  6. **Implement Rate Limiting:** สร้างระบบ Rate Limiting เพื่อป้องกันการใช้งานเกิน
  7. **Write Documentation:** สร้าง API Documentation (OpenAPI/Swagger)
  8. **Test API:** ทดสอบ API ด้วย Integration Tests และ Load Tests
  9. **Deploy and Monitor:** Deploy API และติดตาม Performance และ Errors

### **3. Tooling & Tech Stack**

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้:
  - **API Documentation:** OpenAPI/Swagger, Postman, Insomnia, Redoc
  - **API Testing:** Postman, Insomnia, REST Client, JMeter
  - **API Gateway:** Kong, AWS API Gateway, Azure API Management
  - **Monitoring:** Datadog, New Relic, Prometheus, Grafana
  - **Documentation Platforms:** Confluence, Notion, GitHub Wiki

* **Configuration Essentials:** ส่วนประกอบสำคัญในการตั้งค่า:
  - **API Gateway Configuration:** การตั้งค่า API Gateway (Rate Limiting, Caching, Authentication)
  - **CORS Configuration:** การตั้งค่า CORS สำหรับ Cross-Origin Requests
  - **Security Headers:** การตั้งค่า Security Headers (CSP, X-Frame-Options, etc.)
  - **Rate Limiting Rules:** การตั้งค่า Rate Limiting ตาม User Plan หรือ Endpoint
  - **Monitoring Alerts:** การตั้งค่า Alerts สำหรับ Performance และ Errors

### **4. Standards, Compliance & Security**

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  - **RFC 7231-7235:** HTTP/1.1
  - **RFC 8288:** The OAuth 2.0 Authorization Framework
  - **OpenAPI Specification:** OpenAPI 3.0 Specification
  - **OWASP API Security:** OWASP API Security Top 10

* **Security Protocol:** กลไกการป้องกัน:
  - **Authentication:** การใช้ JWT, OAuth 2.0, API Keys
  - **Authorization:** การใช้ Role-Based Access Control (RBAC)
  - **Input Validation:** การตรวจสอบและ Validate ข้อมูลที่รับมา
  - **Output Encoding:** การ Encode Output เพื่อป้องกัน XSS
  - **Rate Limiting:** การจำกัด Request ต่อวินาที
  - **HTTPS Only:** การบังคับให้ใช้ HTTPS เท่านั้น

* **Explainability:** ความสามารถในการอธิบาย:
  - **API Documentation:** การบันทึก API Documentation อย่างละเอียด
  - **Error Messages:** การใช้ Error Messages ที่ชัดเจนและ Actionable
  - **Request/Response Examples:** การให้ตัวอย่างของ Request และ Response
  - **Use Cases:** การอธิบาย Use Cases และ Workflows
  - **Changelog:** การบันทึกการเปลี่ยนแปลง API

### **5. Unit Economics & Performance Metrics (KPIs)**

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย (COGS):
  ```
  Total Cost = (Development Cost) + (Infrastructure Cost) + (Monitoring Cost)
  
  ROI = (Developer Productivity Gain - Total Cost) / Total Cost × 100%
  
  Developer Productivity Gain = (Time Saved × Hourly Rate × Number of Developers)
  ```

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  - **API Response Time:** เวลาเฉลี่ยในการตอบสนอง (Target: < 100ms P95)
  - **API Availability:** % ของเวลาที่ API พร้อมใช้งาน (Target: > 99.9%)
  - **Error Rate:** % ของ Request ที่ล้มเหลว (Target: < 0.1%)
  - **Developer Satisfaction:** ความพึงพอใจของผู้ใช้งาน (Target: > 4/5)
  - **Integration Success Rate:** % ของ Integration ที่สำเร็จในครั้งแรก (Target: > 95%)

### **6. Strategic Recommendations (CTO Insights)**

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน:
  1. **Phase 1 (Months 1-2):** สร้าง API Design Guidelines และ Template, ฝึกอบรมทีม
  2. **Phase 2 (Months 3-4):** ออกแบบ API ใหม่ตาม RESTful Principles
  3. **Phase 3 (Months 5-6):** สร้าง API Gateway และ Monitoring
  4. **Phase 4 (Year 2+):** ขยายไปยังทุกทีม, สร้าง Culture ของการออกแบบ API ที่ดี

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาด:
  - **Over-engineering:** หลีกเลี่ยงการออกแบบ API ที่ซับซ้อนเกินไป
  - **Inconsistent Naming:** ต้องใช้ Naming Conventions ที่สอดคล้องกัน
  - **Poor Error Handling:** ต้องใช้ Error Response Format ที่สอดคล้องกัน
  - **No Versioning:** ต้องวางแผนการเปลี่ยนแปลง API ตั้งแต่เริ่ม
  - **Missing Documentation:** ต้องมี API Documentation ที่ครบถ้วน
  - **No Rate Limiting:** ต้องมี Rate Limiting เพื่อป้องกันการใช้งานเกิน
  - **Ignoring Security:** ต้องพิจารณา Security ตั้งแต่เริ่ม

---

## Overview

This skill covers RESTful API design principles, best practices, and patterns for building consistent, scalable, and developer-friendly APIs.

## Core Principles

### REST Architectural Constraints

REST (Representational State Transfer) is an architectural style based on six key constraints that guide API design:

1. **Client-Server Separation** - Client and server are independent; client handles UI/UX while server handles data storage and business logic
2. **Statelessness** - Each request contains all information needed to process it; server doesn't store client session state
3. **Cacheability** - Responses must define themselves as cacheable or non-cacheable to reduce client-server interactions
4. **Uniform Interface** - Consistent way to interact with resources using URIs, self-descriptive messages, and HATEOAS
5. **Layered System** - Client cannot tell if connected directly to server; enables load balancing, caching, and security layers
6. **Code on Demand (Optional)** - Server can extend client functionality by transferring executable code

### API Design Fundamentals

- **Resource-First Thinking**: Design APIs around resources (nouns), not actions (verbs)
- **Consistency is King**: Maintain consistent naming conventions, response formats, and error handling
- **Pragmatic REST**: Balance RESTful purity with practical developer experience
- **Version from Day One**: Plan for evolution by including versioning from the start
- **Security by Default**: Use HTTPS, validate inputs, implement proper authentication/authorization
- **Performance Matters**: Implement caching, pagination, and efficient data structures
- **Developer Experience**: Provide clear documentation, meaningful error messages, and intuitive URLs

### HTTP Semantics

Use HTTP methods and status codes according to their intended semantic meaning:
- **GET**: Retrieve resources (idempotent, safe)
- **POST**: Create resources (non-idempotent, unsafe)
- **PUT**: Replace entire resource (idempotent, unsafe)
- **PATCH**: Partial update (non-idempotent, unsafe)
- **DELETE**: Remove resource (idempotent, unsafe)

## Table of Contents

1. [REST Principles](#rest-principles)
2. [HTTP Methods](#http-methods)
3. [URL Structure and Naming](#url-structure-and-naming)
4. [Status Codes](#status-codes)
5. [Request/Response Format](#requestresponse-format)
6. [Versioning Strategies](#versioning-strategies)
7. [Authentication Patterns](#authentication-patterns)
8. [Rate Limiting](#rate-limiting)
9. [CORS Configuration](#cors-configuration)
10. [API Documentation](#api-documentation)
11. [Common Patterns Checklist](#common-api-patterns-checklist)

---

## REST Principles

REST (Representational State Transfer) is an architectural style based on six key constraints:

### 1. Client-Server Separation
- Client and server are independent
- Client handles UI/UX, server handles data storage and business logic
- Changes to one don't affect the other

### 2. Statelessness
- Each request contains all information needed to process it
- Server doesn't store client session state
- Improves scalability and reliability

### 3. Cacheability
- Responses must define themselves as cacheable or non-cacheable
- Reduces client-server interactions
- Improves performance and scalability

### 4. Uniform Interface
- Consistent way to interact with resources
- Resources identified by URIs
- Self-descriptive messages
- HATEOAS (Hypermedia as the Engine of Application State)

### 5. Layered System
- Client cannot tell if connected directly to server
- Enables load balancing, caching, and security layers

### 6. Code on Demand (Optional)
- Server can extend client functionality by transferring executable code

## HTTP Methods

### Method Summary

| Method | Purpose | Idempotent | Safe | Request Body | Response Body |
|--------|---------|------------|------|--------------|---------------|
| GET | Retrieve resource(s) | Yes | Yes | No | Yes |
| POST | Create resource | No | No | Yes | Yes |
| PUT | Replace resource | Yes | No | Yes | Yes |
| PATCH | Partial update | No | No | Yes | Yes |
| DELETE | Remove resource | Yes | No | No | Optional |
| HEAD | Get headers only | Yes | Yes | No | No |
| OPTIONS | Get allowed methods | Yes | Yes | No | Yes |

### GET - Retrieve Resources

```http
# Get all users (with pagination)
GET /api/v1/users?page=1&limit=20

# Get single user
GET /api/v1/users/123

# Get nested resource
GET /api/v1/users/123/orders
```

**Best Practices:**
- Never modify data on GET requests
- Support filtering, sorting, and pagination
- Return 200 OK with data or 404 Not Found

### POST - Create Resources

```http
POST /api/v1/users
Content-Type: application/json

{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "member"
}
```

**Response:**
```http
HTTP/1.1 201 Created
Location: /api/v1/users/124

{
  "id": 124,
  "email": "user@example.com",
  "name": "John Doe",
  "role": "member",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

**Best Practices:**
- Return 201 Created with Location header
- Include created resource in response body
- Validate all input data

### PUT - Replace Resources

```http
PUT /api/v1/users/123
Content-Type: application/json

{
  "email": "updated@example.com",
  "name": "John Updated",
  "role": "admin"
}
```

**Best Practices:**
- Replace entire resource (all fields required)
- Return 200 OK with updated resource
- Return 404 if resource doesn't exist
- Idempotent: multiple identical requests have same effect

### PATCH - Partial Update

```http
PATCH /api/v1/users/123
Content-Type: application/json

{
  "name": "John Patched"
}
```

**Best Practices:**
- Update only specified fields
- Return 200 OK with updated resource
- Consider using JSON Patch (RFC 6902) for complex updates

### DELETE - Remove Resources

```http
DELETE /api/v1/users/123
```

**Response Options:**
```http
# Option 1: No content
HTTP/1.1 204 No Content

# Option 2: Return deleted resource
HTTP/1.1 200 OK
{
  "id": 123,
  "deleted": true
}
```

**Best Practices:**
- Return 204 No Content or 200 OK
- Return 404 if resource doesn't exist
- Consider soft delete for audit trails

## URL Structure and Naming

### Resource Naming Conventions

```
# Good - Nouns, plural, lowercase, kebab-case
GET /api/v1/users
GET /api/v1/order-items
GET /api/v1/product-categories

# Bad - Verbs, singular, camelCase
GET /api/v1/getUser
GET /api/v1/user
GET /api/v1/orderItems
GET /api/v1/productCategories
```

### Resource Hierarchy

```
# Collection
GET /api/v1/users                    # All users

# Single Resource
GET /api/v1/users/123                # User 123

# Nested Resources (belongs-to relationship)
GET /api/v1/users/123/orders         # Orders for user 123
GET /api/v1/users/123/orders/456     # Order 456 for user 123

# Avoid deep nesting (max 2-3 levels)
# Bad
GET /api/v1/users/123/orders/456/items/789/details

# Better - Use query params or separate endpoint
GET /api/v1/order-items/789
GET /api/v1/orders/456/items?include=details
```

### Query Parameters

```
# Pagination
GET /api/v1/users?page=2&limit=20
GET /api/v1/users?offset=40&limit=20
GET /api/v1/users?cursor=eyJpZCI6MTAwfQ==
GET /api/v1/users?search=john
GET /api/v1/products?q=laptop
```

### URL Structure Examples

```
# Base URL structure
https://api.example.com/v1/resources

# Environment-based
https://api.example.com          # Production
https://api.staging.example.com  # Staging
https://api.dev.example.com      # Development

# Action endpoints (when needed)
POST /api/v1/users/123/activate
POST /api/v1/orders/456/cancel
POST /api/v1/payments/789/refund
```

## Status Codes

### 2xx Success

| Code | Name | Usage |
|------|------|-------|
| 200 | OK | Successful GET, PUT, PATCH, or DELETE |
| 201 | Created | Successful POST creating a resource |
| 202 | Accepted | Request accepted for async processing |
| 204 | No Content | Successful request with no response body |

### 4xx Client Errors

| Code | Name | Usage |
|------|------|-------|
| 400 | Bad Request | Invalid request syntax or parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Valid auth but insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 405 | Method Not Allowed | HTTP method not supported |
| 409 | Conflict | Request conflicts with current state |
| 410 | Gone | Resource permanently deleted |
| 415 | Unsupported Media Type | Content-Type not supported |
| 422 | Unprocessable Entity | Validation errors |
| 429 | Too Many Requests | Rate limit exceeded |

### 5xx Server Errors

| Code | Name | Usage |
|------|------|-------|
| 500 | Internal Server Error | Unexpected server error |
| 502 | Bad Gateway | Invalid response from upstream server |
| 503 | Service Unavailable | Server temporarily unavailable |
| 504 | Gateway Timeout | Upstream server timeout |

## Request/Response Format

### JSON Structure Standards

#### Successful Response

```typescript
// Single resource
{
  "data": {
    "id": 123,
    "type": "user",
    "attributes": {
      "email": "user@example.com",
      "name": "John Doe",
      "createdAt": "2024-01-15T10:30:00Z",
      "updatedAt": "2024-01-15T10:30:00Z"
    }
  }
}

// Simplified format (also acceptable)
{
  "id": 123,
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2024-01-15T10:30:00Z",
  "updatedAt": "2024-01-15T10:30:00Z"
}
```

#### Collection Response

```typescript
{
  "data": [
    { "id": 1, "name": "User 1" },
    { "id": 2, "name": "User 2" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20,
    "totalPages": 5
  }
}
```

### Error Response Format

```typescript
// Standard error structure
interface ErrorResponse {
  error: {
    code: string;           // Machine-readable error code
    message: string;        // Human-readable message
    details?: ErrorDetail[];// Field-level errors
    requestId?: string;     // For debugging/support
    timestamp?: string;     // When error occurred
    path?: string;          // Request path
  };
}

interface ErrorDetail {
  field: string;
  message: string;
  code?: string;
}

// Example implementation
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address",
        "code": "INVALID_FORMAT"
      },
      {
        "field": "age",
        "message": "Must be between 18 and 120",
        "code": "OUT_OF_RANGE"
      }
    ],
    "requestId": "req-abc-123",
    "timestamp": "2024-01-15T10:30:00Z",
    "path": "/api/v1/users"
  }
}
```

### Pagination

#### Offset-Based Pagination

```typescript
// Request
GET /api/v1/users?page=2&limit=20

// Response
{
  "data": [...],
  "meta": {
    "pagination": {
      "total": 100,
      "count": 20,
      "perPage": 20,
      "currentPage": 2,
      "totalPages": 5
    }
  },
  "links": {
    "self": "/api/v1/users?page=2&limit=20",
    "first": "/api/v1/users?page=1&limit=20",
    "prev": "/api/v1/users?page=1&limit=20",
    "next": "/api/v1/users?page=3&limit=20",
    "last": "/api/v1/users?page=5&limit=20"
  }
}
```

#### Cursor-Based Pagination (Recommended for large datasets)

```typescript
// Request
GET /api/v1/users?cursor=eyJpZCI6MTAwfQ==&limit=20

// Response
{
  "data": [...],
  "meta": {
    "hasMore": true,
    "count": 20
  },
  "links": {
    "self": "/api/v1/users?cursor=eyJpZCI6MTAwfQ==&limit=20",
    "next": "/api/v1/users?cursor=eyJpZCI6MTIwfQ==&limit=20"
  }
}
```

### Filtering and Sorting

```typescript
// Filtering request
GET /api/v1/products?category=electronics&price_min=100&price_max=1000&in_stock=true

// Sorting request
GET /api/v1/products?sort=-price,name  // Descending price, ascending name

// Combined with pagination
GET /api/v1/products?category=electronics&sort=-created_at&page=1&limit=20

// Response with applied filters
{
  "data": [...],
  "meta": {
    "filters": {
      "category": "electronics",
      "price_min": 100,
      "price_max": 1000,
      "in_stock": true
    },
    "sort": ["-price", "name"],
    "pagination": {
      "total": 45,
      "page": 1,
      "limit": 20
    }
  }
}
```

### Date/Time Format

Always use ISO 8601 format:

```typescript
{
  "createdAt": "2024-01-15T10:30:00Z",        // UTC
  "updatedAt": "2024-01-15T10:30:00+07:00",   // With timezone
  "date": "2024-01-15"                         // Date only
}
```

## Versioning Strategies

### URL Path Versioning (Recommended)

```
GET /api/v1/users
GET /api/v2/users
```

**Pros:** Clear, easy to implement, cache-friendly
**Cons:** URL changes between versions

### Header Versioning

```http
GET /api/users
Accept: application/vnd.api+json; version=1
# or
X-API-Version: 1
```

**Pros:** Clean URLs
**Cons:** Less discoverable, harder to test

### Query Parameter Versioning

```
GET /api/users?version=1
```

**Pros:** Easy to implement
**Cons:** Can be cached incorrectly, less RESTful

### Version Implementation Example

```typescript
// Express.js with URL versioning
import express from 'express';
import v1Routes from './routes/v1';
import v2Routes from './routes/v2';

const app = express();

app.use('/api/v1', v1Routes);
app.use('/api/v2', v2Routes);

// Version deprecation headers
app.use('/api/v1', (req, res, next) => {
  res.set('Deprecation', 'true');
  res.set('Sunset', 'Sat, 01 Jun 2025 00:00:00 GMT');
  res.set('Link', '</api/v2>; rel="successor-version"');
  next();
});
```

### Versioning Best Practices

1. Start with v1 from day one
2. Maintain at least one previous version
3. Announce deprecation with sunset headers
4. Provide migration guides
5. Use semantic versioning for breaking changes

## Authentication Patterns

### Bearer Token (JWT)

```http
GET /api/v1/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

```typescript
// Middleware implementation
import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';

interface AuthRequest extends Request {
  user?: { id: string; role: string };
}

export const authenticate = (
  req: AuthRequest,
  res: Response,
  next: NextFunction
) => {
  const authHeader = req.headers.authorization;

  if (!authHeader?.startsWith('Bearer ')) {
    return res.status(401).json({
      error: {
        code: 'MISSING_TOKEN',
        message: 'Authorization header required'
      }
    });
  }

  const token = authHeader.split(' ')[1];

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!);
    req.user = decoded as { id: string; role: string };
    next();
  } catch (error) {
    return res.status(401).json({
      error: {
        code: 'INVALID_TOKEN',
        message: 'Invalid or expired token'
      }
    });
  }
};
```

### API Key Authentication

```http
GET /api/v1/users
X-API-Key: your-api-key-here
```

```typescript
export const apiKeyAuth = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const apiKey = req.headers['x-api-key'] as string;

  if (!apiKey) {
    return res.status(401).json({
      error: {
        code: 'MISSING_API_KEY',
        message: 'X-API-Key header required'
      }
    });
  }

  // Validate API key against database
  const validKey = await validateApiKey(apiKey);

  if (!validKey) {
    return res.status(401).json({
      error: {
        code: 'INVALID_API_KEY',
        message: 'Invalid API key'
      }
    });
  }

  req.apiClient = validKey.client;
  next();
};
```

### OAuth 2.0 Flow

```typescript
// Authorization endpoint
GET /oauth/authorize?
  response_type=code&
  client_id=CLIENT_ID&
  redirect_uri=https://app.example.com/callback&
  scope=read write&
  state=RANDOM_STATE

// Token endpoint
POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code=AUTHORIZATION_CODE&
client_id=CLIENT_ID&
client_secret=CLIENT_SECRET&
redirect_uri=https://app.example.com/callback

// Token response
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "dGhpcyBpcyBhIHJlZnJlc2gu",
  "scope": "read write"
}
```

## Rate Limiting

### Rate Limit Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1705312800
X-RateLimit-Window: 3600
```

### Rate Limit Exceeded Response

```http
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1705312800
Retry-After: 3600

{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please retry after 3600 seconds.",
    "retryAfter": 3600
  }
}
```

### Rate Limiting Implementation

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { createClient } from 'redis';

const redisClient = createClient({ url: process.env.REDIS_URL });

// Standard rate limiter
export const standardLimiter = rateLimit({
  store: new RedisStore({
    sendCommand: (...args: string[]) => redisClient.sendCommand(args),
  }),
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 1000,                 // 1000 requests per hour
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Too many requests, please try again later.'
    }
  }
});

// Tiered rate limits
export const rateLimitByPlan = (req: Request) => {
  const plan = req.user?.plan || 'free';
  const limits: Record<string, number> = {
    free: 100,
    basic: 1000,
    pro: 10000,
    enterprise: 100000
  };
  return limits[plan];
};
```

## CORS Configuration

### CORS Headers

```http
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://app.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization, X-API-Key
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400
Access-Control-Expose-Headers: X-RateLimit-Limit, X-RateLimit-Remaining
```

### Express CORS Configuration

```typescript
import cors from 'cors';

const corsOptions: cors.CorsOptions = {
  origin: (origin, callback) => {
    const allowedOrigins = [
      'https://app.example.com',
      'https://admin.example.com'
    ];

    // Allow requests with no origin (mobile apps, Postman)
    if (!origin) return callback(null, true);

    if (allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
  allowedHeaders: [
    'Content-Type',
    'Authorization',
    'X-API-Key',
    'X-Request-ID'
  ],
  exposedHeaders: [
    'X-RateLimit-Limit',
    'X-RateLimit-Remaining',
    'X-RateLimit-Reset'
  ],
  credentials: true,
  maxAge: 86400 // 24 hours
};

app.use(cors(corsOptions));
```

### Preflight Request Handling

```typescript
// Handle OPTIONS preflight requests
app.options('*', cors(corsOptions));

// Or manually
app.options('/api/*', (req, res) => {
  res.header('Access-Control-Allow-Origin', req.headers.origin);
  res.header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type,Authorization');
  res.header('Access-Control-Max-Age', '86400');
  res.sendStatus(204);
});
```

## API Documentation

### OpenAPI/Swagger Specification

```yaml
openapi: 3.0.3
info:
  title: Example API
  description: RESTful API for Example Application
  version: 1.0.0
  contact:
    email: api@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://api.staging.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List all users
      description: Retrieve a paginated list of users
      tags:
        - Users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '422':
          $ref: '#/components/responses/ValidationError'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
          example: 123
        email:
          type: string
          format: email
          example: user@example.com
        name:
          type: string
          example: John Doe
        createdAt:
          type: string
          format: date-time

    responses:
      Unauthorized:
        description: Authentication required
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

security:
  - bearerAuth: []
```

### Documentation Requirements Checklist

- [ ] API overview and getting started guide
- [ ] Authentication instructions with examples
- [ ] Complete endpoint reference
- [ ] Request/response examples for each endpoint
- [ ] Error codes and handling guide
- [ ] Rate limiting documentation
- [ ] Changelog and versioning policy
- [ ] SDK/client library examples
- [ ] Webhook documentation (if applicable)
- [ ] Testing/sandbox environment details

## Common API Patterns Checklist

### Design Phase

- [ ] Use nouns for resources, not verbs
- [ ] Use plural resource names (`/users` not `/user`)
- [ ] Use kebab-case for multi-word resources
- [ ] Limit URL nesting to 2-3 levels maximum
- [ ] Design consistent response envelopes
- [ ] Plan versioning strategy from start
- [ ] Define standard error response format

### Implementation Phase

- [ ] Implement proper HTTP status codes
- [ ] Validate all input data
- [ ] Implement pagination for list endpoints
- [ ] Support filtering and sorting
- [ ] Add rate limiting
- [ ] Configure CORS properly
- [ ] Implement authentication/authorization
- [ ] Add request ID to all responses
- [ ] Log all requests for debugging

### Security

- [ ] Use HTTPS only
- [ ] Validate and sanitize all inputs
- [ ] Implement proper authentication
- [ ] Use parameterized queries (prevent SQL injection)
- [ ] Rate limit authentication endpoints
- [ ] Don't expose sensitive data in URLs
- [ ] Implement proper CORS
- [ ] Add security headers (CSP, X-Frame-Options, etc.)

### Performance

- [ ] Implement caching with proper headers
- [ ] Use cursor-based pagination for large datasets
- [ ] Support field selection (sparse fieldsets)
- [ ] Compress responses (gzip/brotli)
- [ ] Optimize database queries
- [ ] Consider async processing for long operations

### Documentation

- [ ] Provide OpenAPI/Swagger specification
- [ ] Include request/response examples
- [ ] Document all error codes
- [ ] Provide authentication guide
- [ ] Include rate limiting information
- [ ] Maintain changelog
- [ ] Provide SDK/client libraries

### Monitoring

- [ ] Log all API requests
- [ ] Track response times
- [ ] Monitor error rates
- [ ] Set up alerting for anomalies
- [ ] Track rate limit violations
- [ ] Monitor authentication failures

## Quick Reference

### HTTP Methods Cheat Sheet

```
GET    /resources       → List resources (200)
GET    /resources/:id   → Get single resource (200, 404)
POST   /resources       → Create resource (201, 422)
PUT    /resources/:id   → Replace resource (200, 404)
PATCH  /resources/:id   → Update resource (200, 404)
DELETE /resources/:id   → Delete resource (204, 404)
```

### Common Status Codes

```
200 OK                    → Successful request
201 Created               → Resource created
204 No Content            → Successful, no body
400 Bad Request           → Invalid syntax
401 Unauthorized          → Authentication required
403 Forbidden             → Permission denied
404 Not Found             → Resource not found
409 Conflict              → Resource conflict
422 Unprocessable Entity  → Validation failed
429 Too Many Requests     → Rate limit exceeded
500 Internal Server Error → Server error
503 Service Unavailable   → Maintenance/overload
```

### Response Headers Checklist

```http
Content-Type: application/json
X-Request-ID: req-abc-123
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1705312800
Cache-Control: no-cache, private
```

## Common Pitfalls

### Anti-Patterns to Avoid

#### 1. Using Verbs in URLs

```http
# Bad - Actions in URL
GET /api/v1/getUsers
POST /api/v1/createUser
DELETE /api/v1/deleteUser/123

# Good - Resources with HTTP methods
GET /api/v1/users
POST /api/v1/users
DELETE /api/v1/users/123
```

#### 2. Inconsistent Naming Conventions

```http
# Bad - Mixed conventions
GET /api/v1/users
GET /api/v1/UserProfile
GET /api/v1/order_items
GET /api/v1/productCategories

# Good - Consistent kebab-case, plural
GET /api/v1/users
GET /api/v1/user-profiles
GET /api/v1/order-items
GET /api/v1/product-categories
```

#### 3. Deep URL Nesting

```http
# Bad - Too many levels
GET /api/v1/users/123/orders/456/items/789/details

# Good - Flatten with query params or separate endpoints
GET /api/v1/order-items/789
GET /api/v1/orders/456/items?include=details
```

#### 4. Returning Wrong Status Codes

```typescript
// Bad - Using 200 for errors
res.status(200).json({ error: "User not found" });

// Bad - Using 500 for client errors
res.status(500).json({ error: "Invalid email format" });

// Good - Use appropriate status codes
res.status(404).json({ error: { code: "USER_NOT_FOUND", message: "User not found" } });
res.status(422).json({ error: { code: "VALIDATION_ERROR", message: "Invalid email format" } });
```

#### 5. Missing Pagination on List Endpoints

```typescript
// Bad - Returns all records (performance issue)
GET /api/v1/users
// Returns 100,000+ users in one response

// Good - Paginated response
GET /api/v1/users?page=1&limit=20
{
  "data": [...],
  "meta": { "total": 100000, "page": 1, "limit": 20, "totalPages": 5000 }
}
```

#### 6. Over-Using POST for Everything

```http
# Bad - POST for retrieval
POST /api/v1/getUser
{ "userId": 123 }

# Good - GET for retrieval
GET /api/v1/users/123
```

#### 7. Inconsistent Error Responses

```typescript
// Bad - Different error formats
{ "error": "User not found" }
{ "message": "Invalid email" }
{ "status": "error", "details": "..." }

// Good - Consistent error envelope
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User not found",
    "requestId": "req-abc-123"
  }
}
```

#### 8. Ignoring Idempotency

```typescript
// Bad - POST for updates (non-idempotent)
POST /api/v1/users/123/update
{ "name": "New Name" }

// Good - PUT or PATCH (idempotent)
PUT /api/v1/users/123
{ "name": "New Name" }
```

#### 9. Exposing Internal Implementation

```http
# Bad - Database structure exposed
GET /api/v1/user_profiles
GET /api/v1/user_roles_map

# Good - Domain-focused resources
GET /api/v1/users
GET /api/v1/roles
```

#### 10. No Versioning Strategy

```http
# Bad - Breaking changes without version
GET /api/users  // Changes break all clients

# Good - Versioned from start
GET /api/v1/users
GET /api/v2/users  // New version, v1 still works
```

### Security Pitfalls

#### 1. Missing HTTPS Enforcement

```typescript
// Bad - Accepts HTTP
app.listen(80);

// Good - Redirect HTTP to HTTPS
app.use((req, res, next) => {
  if (req.protocol !== 'https') {
    return res.redirect(301, `https://${req.headers.host}${req.url}`);
  }
  next();
});
```

#### 2. Exposing Sensitive Data in URLs

```http
# Bad - Sensitive data in URL (logged, cached)
GET /api/v1/users?api_key=SECRET_KEY
GET /api/v1/users?password=secret123

# Good - Sensitive data in headers/body
GET /api/v1/users
Authorization: Bearer SECRET_KEY
```

#### 3. Not Validating Input

```typescript
// Bad - No validation
app.post('/users', (req, res) => {
  db.insert(req.body);  // SQL injection risk
});

// Good - Validate input
app.post('/users', validateUserSchema, (req, res) => {
  db.insert(req.body);  // Safe, validated data
});
```

#### 4. Weak Rate Limiting

```typescript
// Bad - No rate limiting or per-IP only
app.use(rateLimit({ windowMs: 60000, max: 1000 }));

// Good - Per-user rate limiting with authentication
app.use((req, res, next) => {
  const userId = req.user?.id || req.ip;
  const limit = req.user?.plan === 'enterprise' ? 10000 : 1000;
  checkRateLimit(userId, limit).then(next);
});
```

### Performance Pitfalls

#### 1. N+1 Query Problem

```typescript
// Bad - N+1 queries
const users = await db.users.findMany();
for (const user of users) {
  user.orders = await db.orders.findMany({ where: { userId: user.id } });
}

// Good - Eager loading
const users = await db.users.findMany({
  include: { orders: true }
});
```

#### 2. Returning Too Much Data

```typescript
// Bad - Returns all fields
GET /api/v1/users
// Returns: id, name, email, phone, address, ssn, ...

// Good - Field selection
GET /api/v1/users?fields=id,name,email
// Returns only requested fields
```

#### 3. No Caching Strategy

```typescript
// Bad - No cache headers
res.json({ data: users });

// Good - Cache headers for GET requests
res.set('Cache-Control', 'public, max-age=300');
res.json({ data: users });
```

## Additional Resources

### Official Documentation

- [REST API Tutorial](https://restfulapi.net/) - Comprehensive REST API tutorial and best practices
- [MDN Web Docs - HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP) - Complete HTTP reference
- [OpenAPI Specification](https://swagger.io/specification/) - OpenAPI 3.0 specification
- [RFC 7231 - HTTP Semantics](https://tools.ietf.org/html/rfc7231) - Official HTTP semantics RFC

### Design Guides

- [API Design Guide (Google)](https://cloud.google.com/apis/design) - Google's API design principles
- [Microsoft REST API Guidelines](https://github.com/Microsoft/api-guidelines) - Microsoft's REST API guidelines
- [Zalando RESTful API Guidelines](https://github.com/zalando/restful-api-guidelines) - Comprehensive REST guidelines
- [Heroku Platform API Style Guide](https://github.com/heroku/platform-api-style-guide) - Heroku's API style guide

### Tools and Libraries

- [Swagger/OpenAPI Tools](https://swagger.io/tools/) - API documentation and testing tools
- [Postman](https://www.postman.com/) - API development and testing platform
- [Insomnia](https://insomnia.rest/) - REST client for API testing
- [HTTPie](https://httpie.io/) - User-friendly command-line HTTP client

### Related Skills

- [`express-rest`](03-backend-api/express-rest/SKILL.md) - Express.js REST API patterns
- [`error-handling`](03-backend-api/error-handling/SKILL.md) - Backend error handling patterns
- [`validation`](03-backend-api/validation/SKILL.md) - API request validation patterns
- [`jwt-authentication`](10-authentication-authorization/jwt-authentication/SKILL.md) - JWT authentication implementation
- [`api-style-guide`](64-meta-standards/api-style-guide/SKILL.md) - Organization-wide API conventions
- [`error-shape-taxonomy`](64-meta-standards/error-shape-taxonomy/SKILL.md) - Standard error response taxonomy
