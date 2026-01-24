---
name: API Documentation
description: Creating comprehensive, interactive API documentation that enables developers to effectively integrate with your services using OpenAPI/Swagger, code examples, and best practices.
---

# API Documentation

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** Documentation / Developer Experience

---

## Overview

API documentation is critical for enabling developers to effectively integrate with your services. Well-documented APIs reduce integration time, minimize support requests, increase adoption, and improve developer satisfaction through clear examples, interactive tools, and comprehensive reference materials.

---

## 1. Executive Summary & Strategic Necessity

* **Context:** ในปี 2025-2026 API Documentation ด้วย OpenAPI/Swagger ช่วย Developer Experience ที่มีอัตโนมาติการทำงานอัตโนมาติ (API Documentation) ใน Enterprise Scale

* **Business Impact:** API Documentation ช่วยลด Downtime ของระบบ Customer Support ผ่านการตอบคำถามอัตโนมาติการเขียนเอกสาร (Reduce support burden), ลดต้นทุนการจัดการทีม (Increase developer adoption), เพิ่มอัตรากำไร Gross Margin ผ่านการทำงานอัตโนมาติ (Faster integration), และปรับประสบทการทำงาน (Consistent quality)

* **Product Thinking:** API Documentation ช่วยแก้ปัญหา (Pain Point) ความต้องการมีเอกสาร API ที่ชัดเจน (Developers need clear documentation) ผ่านการทำงานอัตโนมาติ (Interactive documentation)

---

## 2. Technical Deep Dive (The "How-to")

* **Core Logic:** API Documentation ใช้ OpenAPI/Swagger ช่วย Developer Experience ทำงานอัตโนมาติ:
  1. **OpenAPI Specification**: สร้าง OpenAPI spec จาก code หรือ manual (OpenAPI 3.0, Swagger 2.0)
  2. **Documentation Generation**: สร้าง Interactive docs จาก OpenAPI spec (Swagger UI, Redoc)
  3. **Code Examples**: เพิ่ม Code examples หลายภาษา (JavaScript, Python, Go, etc.)
  4. **Version Management**: จัดการ API versions (URL versioning, Header versioning)
  5. **Changelog**: เก็บ changelog สำหรับ API changes (Breaking changes, New features)

* **Architecture Diagram Requirements:** แผนผังระบบ API Documentation ต้องมีองค์ประกอบ:
  1. **OpenAPI Spec**: OpenAPI specification สำหรับการจัดเก็บ API definitions (openapi.yaml, openapi.json)
  2. **Documentation Generator**: Tool สำหรับสร้าง Interactive docs (Swagger UI, Redoc, Docusaurus)
  3. **Code Examples**: Code examples สำหรับหลายภาษา (JavaScript, Python, Go, Java, etc.)
  4. **Version Management**: System สำหรับการจัดการ API versions (Git branches, API versioning)
  5. **Changelog System**: System สำหรับการจัดการ changelog (Keep a Changelog, Conventional Commits)
  6. **Hosting Platform**: Platform สำหรับ hosting docs (GitHub Pages, Vercel, Netlify)
  7. **Observability**: Logging, Monitoring, Tracing สำหรับการ debug และปรับสิทท

* **Implementation Workflow:** ขั้นตอนการนำ API Documentation ไปใช้งานจริง:
  1. **Planning Phase**: กำหนด Requirement และเลือก Documentation tool ที่เหมาะสม
  2. **OpenAPI Design**: ออกแบบ OpenAPI spec สำหรับ API definitions
  3. **Documentation Generation**: สร้าง Interactive docs จาก OpenAPI spec
  4. **Code Examples**: เพิ่ม Code examples หลายภาษา
  5. **Version Management**: จัดการ API versions
  6. **Changelog**: เก็บ changelog สำหรับ API changes
  7. **Testing Phase**: Unit test, Integration test, E2E test ด้วยจริง Scenario
  8. **Deployment**: Deploy ด้วย Hosting platform, Set up CI/CD, Configure Monitoring
  9. **Optimization**: Optimize documentation performance, Add search functionality, Improve UX
  10. **Maintenance**: Monitor documentation usage, Update docs with API changes, Handle edge cases

---

## 3. Tooling & Tech Stack

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้สำหรับ API Documentation ใน Enterprise Scale:
  1. **OpenAPI/Swagger**: OpenAPI specification สำหรับ API definitions (OpenAPI 3.0, Swagger 2.0)
  2. **Swagger UI**: Interactive documentation UI สำหรับ testing APIs
  3. **Redoc**: Beautiful documentation UI สำหรับ production docs
  4. **Docusaurus**: Static site generator สำหรับ custom documentation
  5. **Postman**: API testing และ documentation platform
  6. **Stoplight**: API design, mock, และ documentation platform
  7. **GitHub**: Version control สำหรับ documentation source
  8. **GitHub Pages**: Free hosting สำหรับ static documentation
  9. **Vercel**: Hosting platform สำหรับ documentation sites
  10. **Google Analytics**: Analytics สำหรับ tracking documentation usage

* **Configuration Essentials:** การตั้งค่าสำคัญสำหรับให้ระบบเสถียร API Documentation:
  1. **OpenAPI Version**: เลือก OpenAPI version ตาม requirement (OpenAPI 3.0, Swagger 2.0)
  2. **Documentation Theme**: เลือก theme ตาม brand colors และ design guidelines
  3. **Code Examples Languages**: เลือก languages ตาม target audience (JavaScript, Python, Go, Java, etc.)
  4. **Versioning Strategy**: เลือก versioning strategy ตาม API lifecycle (URL versioning, Header versioning)
  5. **Rate Limiting**: Set rate limits สำหรับ documentation access (100-1000 requests/hour)
  6. **Cache Configuration**: Set cache headers สำหรับ documentation pages (1-24 hours)
  7. **Search Configuration**: Configure search indexing สำหรับ documentation
  8. **Analytics Configuration**: Set up analytics สำหรับ tracking documentation usage
  9. **CDN Configuration**: Set up CDN สำหรับ faster documentation delivery
  10. **SSL/TLS**: Enable HTTPS สำหรับ secure documentation access

---

## 4. Standards, Compliance & Security

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  1. **ISO/IEC 27001**: Information Security Management - สำหรับการจัดการ Secrets และ Access Control
  2. **ISO/IEC 27017**: Code of Practice for Information Security Controls - สำหรับ Secure Development
  3. **GDPR**: General Data Protection Regulation - สำหรับการจัดการ Personal Data และ User Consent
  4. **SOC 2 Type II**: Security Controls - สำหรับการ Audit และ Compliance
  5. **WCAG 2.1 AA**: Web Content Accessibility Guidelines - สำหรับ accessibility

* **Security Protocol:** กลไกการป้องกัน API Documentation:
  1. **Input Validation**: Validate และ Sanitize ทุก Input ก่อน processing (Prevent XSS, SQL injection)
  2. **Output Sanitization**: Filter sensitive information จาก documentation (API keys, Secrets)
  3. **Access Control**: RBAC (Role-Based Access Control) สำหรับ documentation access - บาง docs internal only
  4. **Audit Trail**: Log ทุก documentation access ด้วย Timestamp, User ID, และ Page accessed (สำหรับ Forensics และ Compliance)
  5. **Rate Limiting**: Per-user และ Per-IP rate limits สำหรับป้องกัน Abuse (100-1000 requests/hour)
  6. **Secure Communication**: TLS 1.3 สำหรับ HTTPS access
  7. **Secret Management**: Use Environment variables หรือ Secret Manager (AWS Secrets Manager, HashiCorp Vault)
  8. **Content Security**: CSP headers สำหรับ preventing XSS attacks
  9. **Authentication**: Implement authentication สำหรับ internal documentation (SSO, OAuth)
  10. **Data Encryption**: Encrypt sensitive data ที่ rest ใน Database (AES-256 หรือ Customer-managed keys)

* **Explainability:** (สำหรับ Documentation) ความสามารถในการอธิบายผลลัพธ์ผ่านเทคนิค:
  1. **Clear Structure**: เก็บ documentation structure สำหรับ easy navigation
  2. **Detailed Examples**: Provide detailed examples สำหรับ common use cases
  3. **Error Documentation**: Document all error responses ด้วย clear explanations
  4. **Changelog Tracking**: Track all changes ด้วย clear versioning
  5. **Search Functionality**: Enable search สำหรับ finding relevant information quickly

---

## 5. Unit Economics & Performance Metrics (KPIs)

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย API Documentation:
  1. **Hosting Cost** = Bandwidth × Cost per GB + Storage × Cost per GB/month
     - GitHub Pages: Free
     - Vercel: Free tier + $20/month for Pro
     - Netlify: Free tier + $19/month for Pro
  2. **Domain Cost** = Domain registration ($10-15/year)
  3. **SSL Certificate Cost** = $0 (Let's Encrypt) or $50-100/year (paid)
  4. **CDN Cost** = Bandwidth × Cost per GB ($0.01-0.08/GB)
  5. **Analytics Cost** = Free (Google Analytics) or $10-50/month (paid)
  6. **Total Monthly Cost** = Hosting + Domain + SSL + CDN + Analytics
  7. **Infrastructure Costs** = Compute ($0/month for static sites) + Storage ($0/month for static sites) + Monitoring ($0/month for static sites)

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  1. **Documentation Usage**: จำนวย visitors ต่อเดือน (Target: >1,000 visitors/month)
  2. **Page Load Time**: เวลาการโหลดหน้า (Target: <2 seconds p95)
  3. **Search Success Rate**: อัตราการค้นหาสำเร็จ (Target: >80%)
  4. **User Satisfaction Score**: 1-5 rating จาก User feedback (Target: >4.0)
  5. **Error Rate**: อัตราการ Error (Target: <1%)
  6. **Documentation Coverage**: เปอร์เซ็นต์ของ endpoints ที่มี documentation (Target: >95%)
  7. **Code Example Accuracy**: เปอร์เซ็นต์ของ code examples ที่ทำงานได้ (Target: >98%)
  8. **API Integration Rate**: อัตราการ integration จาก documentation (Target: >10 integrations/month)
  9. **Support Ticket Reduction**: อัตราการลด support tickets (Target: >30% reduction)
  10. **Developer Satisfaction**: NPS score จาก developer survey (Target: >50)

---

## 6. Strategic Recommendations (CTO Insights)

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน API Documentation เพื่อลดความเสี่ยง:
  1. **Phase 1: MVP (1-2 เดือน)**: Deploy Simple API Documentation ด้วย OpenAPI spec และ Swagger UI สำหรับ Internal team ก่อนเปิดให้ Public
     - **Goal**: Validate API Documentation architecture และ gather feedback
     - **Success Criteria**: >80% documentation coverage, <5s page load time
     - **Risk Mitigation**: Internal-only access, Manual review ก่อน Public
  2. **Phase 2: Beta (2-3 เดือน)**: Expand ด้วย Code examples, Version management, และ Changelog สำหรับ Selected customers
     - **Goal**: Test scalability และ Documentation reliability
     - **Success Criteria**: >90% documentation coverage, <3s page load time
     - **Risk Mitigation**: Canary deployment, Feature flags, Gradual rollout
  3. **Phase 3: GA (3-6 เดือน)**: Full rollout ด้วย Advanced features (Search, Analytics, Custom theme)
     - **Goal**: Enterprise-grade documentation และ Performance
     - **Success Criteria**: >95% documentation coverage, <2s page load time, 99.9% uptime
     - **Risk Mitigation**: Load testing, Disaster recovery, Blue-green deployment

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาดในระดับ Enterprise Scale:
  1. **Over-engineering**: สร้าง Documentation ที่ซ้อนเกินไป (Too many features, Complex navigation) → เริ่มจาก Simple และ iterate
  2. **No Rate Limiting**: ไม่มี Rate limits ทำให้ Cost blowout และ API abuse → Implement per-IP และ per-user limits
  3. **Outdated Documentation**: Documentation ไม่ sync กับ API changes → Implement automated documentation generation จาก code
  4. **Missing Code Examples**: ไม่มี Code examples ทำให้ developers ยากในการ integrate → Provide examples หลายภาษา
  5. **No Version Management**: ไม่มี Version management ทำให้ developers สับสนใจ → Implement clear versioning strategy
  6. **No Changelog**: ไม่มี Changelog ทำให้ developers ไม่รู้ changes → Maintain changelog สำหรับ all changes
  7. **No Search**: ไม่มี Search functionality ทำให้ developers ยากในการ find information → Implement search สำหรับ documentation
  8. **Poor Accessibility**: ไม่ support accessibility ทำให้ developers พิการัดใช้งาน → Follow WCAG 2.1 AA guidelines
  9. **No Analytics**: ไม่มี Analytics ทำให้ไม่รู้ documentation usage → Set up analytics สำหรับ tracking usage
  10. **Single Point of Failure**: ไม่มี Redundancy หรือ Fallback → Deploy multiple instances ด้วย CDN

---

## Core Concepts

### 1. API Documentation Importance

### Why API Documentation Matters

```markdown
# API Documentation Importance

## Benefits

### 1. Developer Experience
- Reduces integration time
- Minimizes support requests
- Increases adoption
- Improves developer satisfaction

### 2. Product Quality
- Ensures correct usage
- Reduces bugs
- Improves reliability
- Enables testing

### 3. Business Impact
- Faster time to market
- Lower support costs
- Higher partner satisfaction
- Better ecosystem growth

### 4. Team Efficiency
- Onboards new developers faster
- Reduces knowledge silos
- Provides reference for changes
- Supports collaboration

## Consequences of Poor Documentation

### 1. Integration Issues
- Misunderstanding of parameters
- Incorrect usage patterns
- Security vulnerabilities
- Performance problems

### 2. Support Burden
- Increased support tickets
- Longer resolution times
- Frustrated developers
- Lost opportunities

### 3. Maintenance Costs
- More bug reports
- Frequent clarifications
- Repeated explanations
- Knowledge loss

### 4. Brand Damage
- Poor developer perception
- Negative reviews
- Reduced adoption
- Competitive disadvantage
```

---

## 2. OpenAPI/Swagger

### OpenAPI Specification

```yaml
# OpenAPI 3.0 Specification Example
openapi: 3.0.3
info:
  title: User Management API
  description: API for managing users in system
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server
  - url: http://localhost:3000/v1
    description: Development server

tags:
  - name: Users
    description: User management operations
  - name: Authentication
    description: Authentication operations

paths:
  /users:
    get:
      tags:
        - Users
      summary: List all users
      description: Retrieve a paginated list of users
      operationId: listUsers
      parameters:
        - name: page
          in: query
          description: Page number
          required: false
          schema:
            type: integer
            default: 1
            minimum: 1
        - name: limit
          in: query
          description: Number of items per page
          required: false
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
        - name: search
          in: query
          description: Search query
          required: false
          schema:
            type: string
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserListResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'
      security:
        - BearerAuth: []

    post:
      tags:
        - Users
      summary: Create a new user
      description: Create a new user account
      operationId: createUser
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '409':
          $ref: '#/components/responses/Conflict'
        '500':
          $ref: '#/components/responses/InternalError'
      security:
        - BearerAuth: []

  /users/{userId}:
    get:
      tags:
        - Users
      summary: Get user by ID
      description: Retrieve a specific user by ID
      operationId: getUser
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'
      security:
        - BearerAuth: []

    put:
      tags:
        - Users
      summary: Update user
      description: Update an existing user
      operationId: updateUser
      parameters:
        - $ref: '#/components/parameters/UserId'
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: User updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'
      security:
        - BearerAuth: []

    delete:
      tags:
        - Users
      summary: Delete user
      description: Delete a user account
      operationId: deleteUser
      parameters:
        - $ref: '#/components/parameters/UserId'
      responses:
        '204':
          description: User deleted successfully
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '404':
          $ref: '#/components/responses/NotFound'
        '500':
          $ref: '#/components/responses/InternalError'
      security:
        - BearerAuth: []

  /auth/login:
    post:
      tags:
        - Authentication
      summary: Login
      description: Authenticate and receive access token
      operationId: login
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/LoginRequest'
      responses:
        '200':
          description: Login successful
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/LoginResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'
        '500':
          $ref: '#/components/responses/InternalError'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
      description: JWT token for authentication

  parameters:
    UserId:
      name: userId
      in: path
      description: User ID
      required: true
      schema:
        type: string
        format: uuid
      example: "550e8400-e29b-41d4-a716-446655440000"

  schemas:
    UserResponse:
      type: object
      properties:
        id:
          type: string
          format: uuid
          description: User ID
        name:
          type: string
          description: User's full name
        email:
          type: string
          format: email
          description: User's email address
        age:
          type: integer
          nullable: true
          description: User's age
        createdAt:
          type: string
          format: date-time
          description: Creation timestamp
        updatedAt:
          type: string
          format: date-time
          description: Last update timestamp
      required:
        - id
        - name
        - email
        - createdAt
        - updatedAt

    UserListResponse:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/UserResponse'
        pagination:
          type: object
          properties:
            page:
              type: integer
              description: Current page number
            limit:
              type: integer
              description: Items per page
            total:
              type: integer
              description: Total number of items
            totalPages:
              type: integer
              description: Total number of pages
      required:
        - data
        - pagination

    CreateUserRequest:
      type: object
      properties:
        name:
          type: string
          minLength: 2
          maxLength: 100
          description: User's full name
        email:
          type: string
          format: email
          description: User's email address
        password:
          type: string
          minLength: 8
          format: password
          description: User's password
        age:
          type: integer
          minimum: 0
          maximum: 150
          nullable: true
          description: User's age
      required:
        - name
        - email
        - password

    UpdateUserRequest:
      type: object
      properties:
        name:
          type: string
          minLength: 2
          maxLength: 100
          description: User's full name
        email:
          type: string
          format: email
          description: User's email address
        age:
          type: integer
          minimum: 0
          maximum: 150
          nullable: true
          description: User's age

    LoginRequest:
      type: object
      properties:
        email:
          type: string
          format: email
          description: User's email address
        password:
          type: string
          format: password
          description: User's password
      required:
        - email
        - password

    LoginResponse:
      type: object
      properties:
        accessToken:
          type: string
          description: JWT access token
        refreshToken:
          type: string
          description: JWT refresh token
        expiresIn:
          type: integer
          description: Token expiration time in seconds
        tokenType:
          type: string
          enum: [Bearer]
          description: Token type
      required:
        - accessToken
        - refreshToken
        - expiresIn
        - tokenType

    ErrorResponse:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
              description: Error code
            message:
              type: string
              description: Error message
            details:
              type: object
              description: Additional error details
          required:
            - code
            - message
      required:
        - error

  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            error:
              code: "BAD_REQUEST"
              message: "Invalid request parameters"
              details:
                field: "email"
                issue: "Invalid email format"

    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            error:
              code: "UNAUTHORIZED"
              message: "Authentication required"

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            error:
              code: "NOT_FOUND"
              message: "User not found"

    Conflict:
      description: Resource conflict
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            error:
              code: "CONFLICT"
              message: "User with this email already exists"

    InternalError:
      description: Internal server error
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'
          example:
            error:
              code: "INTERNAL_ERROR"
              message: "An unexpected error occurred"
```

---

## 3. Documentation Structure

### Standard API Documentation Structure

```markdown
# API Documentation Structure

## 1. Overview
- Introduction
- API purpose
- Key features
- Use cases

## 2. Authentication
- Authentication methods
- API keys
- OAuth flows
- Token management
- Security considerations

## 3. Quick Start
- Getting started guide
- First API call
- Common use cases
- Example code

## 4. Endpoints
- Endpoint listing
- Detailed endpoint documentation
- Request/response examples
- Error handling

## 5. Reference
- Data models
- Enumerations
- Common parameters
- Response formats

## 6. Guides
- Integration guides
- Best practices
- Troubleshooting
- FAQ

## 7. Changelog
- Version history
- Breaking changes
- New features
- Deprecations

## 8. Support
- Contact information
- Support channels
- Community resources
- Feedback
```

### Endpoint Documentation Template

```markdown
# Endpoint: [Endpoint Name]

## Description
[Brief description of what this endpoint does]

## HTTP Method
`[GET | POST | PUT | PATCH | DELETE]`

## URL
```
[Full URL path]
```

## Authentication
[Required authentication method]

## Parameters

### Query Parameters
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `param1` | string | Yes | Description | `"value"` |
| `param2` | integer | No | Description | `123` |

### Path Parameters
| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | string | Yes | Resource ID | `"abc123"` |

### Request Body
```json
{
  "field1": "value1",
  "field2": 123
}
```

## Request Headers
| Header | Value | Required | Description |
|--------|-------|----------|-------------|
| `Authorization` | `Bearer {token}` | Yes | Authentication token |
| `Content-Type` | `application/json` | Yes | Content type |

## Response

### Success Response (200 OK)
```json
{
  "data": {
    "id": "abc123",
    "name": "Example"
  }
}
```

### Error Response (400 Bad Request)
```json
{
  "error": {
    "code": "BAD_REQUEST",
    "message": "Invalid request"
  }
}
```

## Status Codes
- `200 OK` - Success
- `400 Bad Request` - Invalid request
- `401 Unauthorized` - Authentication required
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

## Rate Limiting
[Rate limit information]

## Examples

### cURL
```bash
curl -X GET https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### JavaScript (fetch)
```javascript
const response = await fetch('https://api.example.com/v1/users', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
console.log(data);
```

### Python (requests)
```python
import requests

response = requests.get(
    'https://api.example.com/v1/users',
    headers={
        'Authorization': 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    }
)

data = response.json()
print(data)
```

## See Also
- [Related Endpoint 1](link)
- [Related Endpoint 2](link)
- [Data Model](link)
```

---

## 4. Interactive Documentation

### Swagger UI

```yaml
# swagger-ui configuration
swagger: "2.0"
info:
  title: API Documentation
  version: "1.0.0"
host: api.example.com
basePath: /v1
schemes:
  - https
  - http

# Enable "Try it out" functionality
securityDefinitions:
  Bearer:
    type: apiKey
    name: Authorization
    in: header
    description: "JWT token in format: Bearer {token}"

# Add examples for each endpoint
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          type: integer
          default: 20
          description: Number of results
      responses:
        200:
          description: Success
          schema:
            $ref: '#/definitions/UserList'
          examples:
            application/json:
              data: []
              pagination:
                page: 1
                limit: 20
                total: 0
```

### Redoc Configuration

```yaml
# redoc configuration
specUrl: /openapi.json
theme:
  colors:
    primary:
      main: "#326ce5"
    text:
      primary: "#333333"
    rightPanel:
      backgroundColor: "#f7f9fc"
  typography:
    fontFamily: "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
  sidebar:
    width: "300px"
  rightPanel:
    width: "40%"
```

---

## 5. Code Examples (Multiple Languages)

### Code Example Template

```markdown
# Code Examples

## cURL
```bash
curl -X GET https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

## JavaScript (fetch)
```javascript
const response = await fetch('https://api.example.com/v1/users', {
  method: 'GET',
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  }
});

const data = await response.json();
console.log(data);
```

## JavaScript (axios)
```javascript
import axios from 'axios';

const response = await axios.get('https://api.example.com/v1/users', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN',
    'Content-Type': 'application/json'
  }
});

console.log(response.data);
```

## Python (requests)
```python
import requests

response = requests.get(
    'https://api.example.com/v1/users',
    headers={
        'Authorization': 'Bearer YOUR_TOKEN',
        'Content-Type': 'application/json'
    }
)

data = response.json()
print(data)
```

## Python (httpx)
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get(
        'https://api.example.com/v1/users',
        headers={
            'Authorization': 'Bearer YOUR_TOKEN',
            'Content-Type': 'application/json'
        }
    )
    
    data = response.json()
    print(data)
```

## Ruby
```ruby
require 'net/http'
require 'json'

uri = URI('https://api.example.com/v1/users')
request = Net::HTTP::Get.new(uri)
request['Authorization'] = 'Bearer YOUR_TOKEN'
request['Content-Type'] = 'application/json'

response = Net::HTTP.start(uri.hostname, uri.port, use_ssl: true) do |http|
  http.request(request)
end

data = JSON.parse(response.body)
puts data
```

## Go
```go
package main

import (
    "encoding/json"
    "fmt"
    "net/http"
)

func main() {
    req, err := http.NewRequest("GET", "https://api.example.com/v1/users", nil)
    if err != nil {
        panic(err)
    }
    
    req.Header.Set("Authorization", "Bearer YOUR_TOKEN")
    req.Header.Set("Content-Type", "application/json")
    
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()
    
    var data interface{}
    json.NewDecoder(resp.Body).Decode(&data)
    fmt.Println(data)
}
```

## Java (OkHttp)
```java
import okhttp3.*;

public class Main {
    public static void main(String[] args) throws IOException {
        OkHttpClient client = new OkHttpClient();
        
        Request request = new Request.Builder()
            .url("https://api.example.com/v1/users")
            .get()
            .addHeader("Authorization", "Bearer YOUR_TOKEN")
            .addHeader("Content-Type", "application/json")
            .build();
        
        Response response = client.newCall(request).execute();
        System.out.println(response.body().string());
    }
}
```

## C# (HttpClient)
```csharp
using System;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;

class Program
{
    static async Task Main()
    {
        using var client = new HttpClient();
        client.DefaultRequestHeaders.Add("Authorization", "Bearer YOUR_TOKEN");
        client.DefaultRequestHeaders.Add("Content-Type", "application/json");
        
        var response = await client.GetAsync("https://api.example.com/v1/users");
        var content = await response.Content.ReadAsStringAsync();
        
        Console.WriteLine(content);
    }
}
```

## PHP (cURL)
```php
<?php

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, "https://api.example.com/v1/users");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Authorization: Bearer YOUR_TOKEN",
    "Content-Type: application/json"
]);

$response = curl_exec($ch);
curl_close($ch);

$data = json_decode($response, true);
print_r($data);
```
```

---

## 6. Postman Collections

### Postman Collection Template

```json
{
  "info": {
    "name": "User Management API",
    "description": "Collection for User Management API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "variable": [
    {
      "key": "baseUrl",
      "value": "https://api.example.com/v1",
      "type": "string"
    },
    {
      "key": "token",
      "value": "",
      "type": "string"
    }
  ],
  "auth": {
    "type": "bearer",
    "bearer": [
      {
        "key": "token",
        "value": "{{token}}",
        "type": "string"
      }
    ]
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"email\": \"user@example.com\",\n  \"password\": \"password123\"\n}"
            },
            "url": {
              "raw": "{{baseUrl}}/auth/login",
              "host": ["{{baseUrl}}"],
              "path": ["auth", "login"]
            }
          },
          "response": []
        }
      ]
    },
    {
      "name": "Users",
      "item": [
        {
          "name": "List Users",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{baseUrl}}/users?page=1&limit=20",
              "host": ["{{baseUrl}}"],
              "path": ["users"],
              "query": [
                {
                  "key": "page",
                  "value": "1"
                },
                {
                  "key": "limit",
                  "value": "20"
                }
              ]
            }
          },
          "response": []
        },
        {
          "name": "Get User",
          "request": {
            "method": "GET",
            "header": [],
            "url": {
              "raw": "{{baseUrl}}/users/:userId",
              "host": ["{{baseUrl}}"],
              "path": ["users", ":userId"],
              "variable": [
                {
                  "key": "userId",
                  "value": "550e8400-e29b-41d4-a716-446655440000"
                }
              ]
            }
          },
          "response": []
        },
        {
          "name": "Create User",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"John Doe\",\n  \"email\": \"john@example.com\",\n  \"password\": \"password123\",\n  \"age\": 30\n}"
            },
            "url": {
              "raw": "{{baseUrl}}/users",
              "host": ["{{baseUrl}}"],
              "path": ["users"]
            }
          },
          "response": []
        },
        {
          "name": "Update User",
          "request": {
            "method": "PUT",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"Jane Doe\",\n  \"email\": \"jane@example.com\",\n  \"age\": 25\n}"
            },
            "url": {
              "raw": "{{baseUrl}}/users/:userId",
              "host": ["{{baseUrl}}"],
              "path": ["users", ":userId"],
              "variable": [
                {
                  "key": "userId",
                  "value": "550e8400-e29b-41d4-a716-446655440000"
                }
              ]
            }
          },
          "response": []
        },
        {
          "name": "Delete User",
          "request": {
            "method": "DELETE",
            "header": [],
            "url": {
              "raw": "{{baseUrl}}/users/:userId",
              "host": ["{{baseUrl}}"],
              "path": ["users", ":userId"],
              "variable": [
                {
                  "key": "userId",
                  "value": "550e8400-e29b-41d4-a716-446655440000"
                }
              ]
            }
          },
          "response": []
        }
      ]
    }
  ]
}
```

---

## 7. Versioning

### API Versioning Strategies

```markdown
# API Versioning

## 1. URL Versioning
```
https://api.example.com/v1/users
https://api.example.com/v2/users
```

**Pros:**
- Clear and explicit
- Easy to understand
- Works with caching

**Cons:**
- Requires URL changes
- Multiple endpoints to maintain

## 2. Header Versioning
```
GET /users
Accept: application/vnd.api.v1+json
```

**Pros:**
- Clean URLs
- Version in request metadata
- Supports content negotiation

**Cons:**
- Less visible
- Harder to debug
- Requires header support

## 3. Query Parameter Versioning
```
GET /users?version=1
```

**Pros:**
- Simple to implement
- Easy to test

**Cons:**
- Not RESTful
- Caching issues
- Less explicit

## 4. Semantic Versioning
```
1.0.0 - Initial release
1.1.0 - New feature (backward compatible)
2.0.0 - Breaking changes
```

**Pros:**
- Clear communication
- Industry standard
- Predictable changes

**Cons:**
- Requires planning
- Multiple versions to maintain

## Best Practices

### 1. Version from Start
- Always include version in first release
- Plan for versioning early
- Document versioning strategy

### 2. Support Multiple Versions
- Maintain at least 2 versions
- Provide migration guides
- Deprecate old versions gracefully

### 3. Communicate Changes
- Document breaking changes
- Provide advance notice
- Support migration

### 4. Deprecation Policy
- Set deprecation timeline
- Communicate deprecation
- Remove after grace period
```

---

## 8. Changelog

### Changelog Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-01-15

### Added
- New endpoint: `/users/{id}/avatar` for user avatar management
- New field: `avatarUrl` in User response
- Support for multiple authentication methods

### Changed
- **BREAKING**: `/users` endpoint now requires `Authorization` header
- **BREAKING**: User ID format changed from integer to UUID
- Updated rate limits: 1000 requests per hour (was 500)
- Improved error response format with additional details

### Deprecated
- `/users/{id}/profile` endpoint (use `/users/{id}` instead)
- Basic authentication (use OAuth instead)

### Removed
- **BREAKING**: `/legacy/users` endpoint removed
- **BREAKING**: `username` field removed from User model

### Fixed
- Fixed pagination bug in `/users` endpoint
- Fixed authentication token expiration handling
- Fixed rate limit response headers

### Security
- Added rate limiting to prevent abuse
- Improved input validation
- Added CORS configuration

## [1.1.0] - 2023-12-01

### Added
- New endpoint: `/users/{id}/settings` for user preferences
- New field: `createdAt` and `updatedAt` in User response
- Support for filtering users by date range

### Changed
- Improved performance of `/users` endpoint
- Updated documentation with new examples

### Fixed
- Fixed bug with user search case sensitivity
- Fixed error handling for invalid user IDs

## [1.0.0] - 2023-11-01

### Added
- Initial release
- User management endpoints
- Authentication endpoints
- Documentation
```

---

## 9. Getting Started Guides

### Quick Start Template

```markdown
# Getting Started

## Prerequisites
- API key or authentication token
- HTTP client (curl, Postman, etc.)
- Basic knowledge of REST APIs

## 1. Authentication

### Get Your API Key
1. Sign up at [dashboard.example.com](https://dashboard.example.com)
2. Navigate to API Keys section
3. Generate a new API key
4. Copy your API key

### Make Your First Request
```bash
curl -X GET https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 2. Create a User

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securePassword123"
  }'
```

## 3. List Users

```bash
curl -X GET "https://api.example.com/v1/users?page=1&limit=10" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## 4. Get a Specific User

```bash
curl -X GET https://api.example.com/v1/users/USER_ID \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Next Steps
- Read [full API documentation](#)
- Check out [code examples](#)
- Explore [integration guides](#)
- Join our [community](#)
```

---

## 10. Tools

### Documentation Tools Comparison

```markdown
# Documentation Tools

## 1. Swagger UI
- **Type**: Open-source
- **Features**: Interactive docs, try it out
- **Best For**: REST APIs
- **Cost**: Free

## 2. Redoc
- **Type**: Open-source
- **Features**: Beautiful UI, responsive
- **Best For**: Production docs
- **Cost**: Free

## 3. Stoplight
- **Type**: Commercial
- **Features**: Design, mock, test
- **Best For**: API lifecycle
- **Cost**: Freemium

## 4. Postman
- **Type**: Commercial
- **Features**: Testing, documentation
- **Best For**: Development
- **Cost**: Freemium

## 5. ReadMe
- **Type**: Commercial
- **Features**: Hosting, customization
- **Best For**: Public APIs
- **Cost**: Paid

## 6. Docusaurus
- **Type**: Open-source
- **Features**: Static site, customizable
- **Best For**: Custom docs
- **Cost**: Free
```

---

## 11. Best Practices

### API Documentation Best Practices

```markdown
# Best Practices

## 1. Start Early
- Document as you build
- Keep docs in sync with code
- Use API-first design

## 2. Be Complete
- Document all endpoints
- Include all parameters
- Provide examples
- Cover error cases

## 3. Be Clear
- Use simple language
- Avoid jargon
- Provide context
- Explain concepts

## 4. Be Consistent
- Use consistent terminology
- Follow style guide
- Maintain formatting
- Use standard patterns

## 5. Be Interactive
- Provide try it out
- Include code examples
- Use live demos
- Enable testing

## 6. Be Accessible
- Support screen readers
- Use semantic HTML
- Provide alt text
- Ensure color contrast

## 7. Be Searchable
- Use good titles
- Include keywords
- Add tags
- Optimize for SEO

## 8. Be Maintained
- Update regularly
- Track changes
- Review periodically
- Archive old versions

## 9. Be Tested
- Test all examples
- Verify links
- Check for errors
- Get feedback

## 10. Be Helpful
- Include troubleshooting
- Provide FAQ
- Offer support
- Gather feedback
```

---

## Quick Start

### 1. Generate OpenAPI Spec from Code

```python
# FastAPI automatically generates OpenAPI spec
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Get user by ID"""
    return {"id": user_id, "name": "John"}

# Access OpenAPI JSON
# GET /openapi.json
```

### 2. Set Up Swagger UI

```python
# FastAPI includes Swagger UI automatically
# Access at: http://localhost:8000/docs

# Or use Swagger UI standalone
from fastapi.openapi.docs import get_swagger_ui_html

@app.get("/docs")
async def swagger_ui():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API Documentation"
    )
```

### 3. Add Examples to OpenAPI

```python
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    name: str = Field(..., example="John Doe", description="User's full name")
    email: str = Field(..., example="john@example.com", description="User's email")
    age: int = Field(..., example=30, description="User's age", ge=0, le=120)

@app.post("/users", response_model=UserCreate)
async def create_user(user: UserCreate):
    """Create a new user"""
    return user
```

### 4. Document with Markdown

```markdown
# API Documentation

## Authentication

All requests require an API key in the header:

```
Authorization: Bearer YOUR_API_KEY
```

## Endpoints

### GET /users/{id}

Get user by ID.

**Parameters:**
- `id` (path, required): User ID

**Response:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com"
}
```
```

---

## Production Checklist

- [ ] **OpenAPI Spec**: Generate and maintain OpenAPI/Swagger specification
- [ ] **Interactive Docs**: Set up Swagger UI or Redoc for interactive testing
- [ ] **Code Examples**: Include working code examples in multiple languages
- [ ] **Authentication**: Document authentication methods clearly
- [ ] **Error Responses**: Document all possible error responses with status codes
- [ ] **Rate Limits**: Document rate limits and quota information
- [ ] **Versioning**: Document API versioning strategy
- [ ] **Changelog**: Maintain changelog for API changes
- [ ] **SDKs**: Provide or link to SDKs if available
- [ ] **Postman Collection**: Provide Postman/Insomnia collection
- [ ] **Testing**: Test all examples in documentation
- [ ] **Search**: Make documentation searchable
- [ ] **Feedback**: Provide way for users to give feedback
- [ ] **Updates**: Keep documentation in sync with API changes

---

## Anti-patterns

### ❌ Don't: Outdated Examples

```python
# ❌ Bad - Old API version
@app.get("/v1/users")  # API is now v2!
async def get_users():
    return {"users": []}
```

```python
# ✅ Good - Current version
@app.get("/v2/users")
async def get_users():
    """Get all users (API v2)"""
    return {"users": []}

# Document version clearly
```

### ❌ Don't: Missing Error Documentation

```python
# ❌ Bad - No error documentation
@app.get("/users/{id}")
async def get_user(id: int):
    if not user_exists(id):
        raise HTTPException(status_code=404)  # Not documented!
    return user
```

```python
# ✅ Good - Document all errors
@app.get(
    "/users/{id}",
    responses={
        200: {"description": "User found"},
        404: {"description": "User not found"},
        500: {"description": "Internal server error"}
    }
)
async def get_user(id: int):
    if not user_exists(id):
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### ❌ Don't: No Code Examples

```markdown
# ❌ Bad - Only description
## GET /users
Returns a list of users.
```

```markdown
# ✅ Good - Include examples
## GET /users

Returns a list of users.

**Example Request:**
```bash
curl -X GET https://api.example.com/v1/users \
  -H "Authorization: Bearer YOUR_API_KEY"
```

**Example Response:**
```json
{
  "users": [
    {"id": 1, "name": "John"},
    {"id": 2, "name": "Jane"}
  ]
}
```
```

### ❌ Don't: Incomplete Authentication Docs

```markdown
# ❌ Bad - Vague
## Authentication
Use API key for authentication.
```

```markdown
# ✅ Good - Detailed
## Authentication

All API requests require authentication using a Bearer token.

1. Get your API key from the dashboard
2. Include it in the Authorization header:
   ```
   Authorization: Bearer YOUR_API_KEY
   ```
3. API keys expire after 90 days
4. Regenerate keys from the dashboard
```

### ❌ Don't: No Interactive Testing

```markdown
# ❌ Bad - Static documentation only
# API Documentation
## Endpoints
...
```

```python
# ✅ Good - Interactive Swagger UI
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    description="Comprehensive API documentation",
    version="1.0.0"
)

# Automatically available at /docs
```

---

## Integration Points

- **API Design** (`01-foundations/api-design/`) - RESTful API principles
- **Technical Writing** (`21-documentation/technical-writing/`) - Writing clear docs
- **OpenAPI/Swagger** (`03-backend-api/express-rest/`) - OpenAPI generation
- **Error Handling** (`03-backend-api/error-handling/`) - Error documentation

---

## Further Reading

- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [API Documentation Best Practices](https://www.postman.com/api-platform/api-documentation/)
- [Redoc](https://github.com/Redocly/redoc)
