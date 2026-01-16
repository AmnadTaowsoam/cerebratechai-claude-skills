---
name: API Style Guide
description: Organization-wide REST/GraphQL API conventions: URL and naming rules, versioning, pagination/filtering, status codes, authentication headers, and compatibility guidance
---

# API Style Guide

## Overview

มาตรฐานการออกแบบ API (REST/GraphQL) ทั้งองค์กร: URL patterns, naming, versioning, pagination, filtering ที่ทำให้ทุก API ใช้งานได้เหมือนกัน

## Why This Matters

- **Consistency**: Clients รู้วิธีใช้ API โดยไม่ต้องอ่าน docs ทุกครั้ง
- **Predictability**: Guess ได้ว่า endpoint หน้าตาเป็นยังไง
- **Tooling**: Auto-generate clients ได้
- **Maintainability**: เปลี่ยนคนดูแลได้ง่าย

---

## Core Concepts

### 1. URL Structure & Naming

- ใช้ **nouns แบบพหูพจน์** สำหรับ resources: `/users`, `/orders`
- ใช้ **kebab-case** ใน path: `/payment-methods` (ไม่ใช้ camelCase)
- nesting ไม่ลึกเกิน 2 ชั้น: `/users/{id}/orders` (หลีกเลี่ยง `/a/{id}/b/{id}/c`)
- หลีกเลี่ยง verbs ใน URL; ใช้ HTTP method แทน (ยกเว้น actions ที่ไม่ใช่ CRUD)
- actions ที่จำเป็นให้ใช้ subresource แบบ verb: `POST /orders/{id}/cancel`

### 2. HTTP Methods

- `GET` อ่านอย่างเดียว, ต้อง **idempotent**
- `POST` สร้าง resource หรือ trigger action ที่มี side effect
- `PUT` replace ทั้ง resource (ควร idempotent)
- `PATCH` update บางส่วน (ควรเป็น merge patch / JSON patch ตามที่ทีมเลือก)
- `DELETE` ลบ (soft-delete เป็น default ถ้าต้อง audit/restore)

สถานะตอบกลับที่แนะนำ:
- `200` สำเร็จ (มี body), `204` สำเร็จ (ไม่มี body)
- `201` สร้างสำเร็จ (+ `Location` header ถ้าเหมาะสม)
- `400/401/403/404/409/422/429` สำหรับ client errors ตามเหตุผล
- `500/502/503` สำหรับ server/upstream errors

### 3. Versioning Strategy

- ใช้ **URL versioning** เป็นค่าเริ่มต้น: `/api/v1/...`
- การเปลี่ยนแบบ breaking ต้อง bump version (`v1` → `v2`) และมีช่วง deprecate
- ภายใน version เดียว ให้ใช้ schema evolution แบบ additive (เพิ่ม field optional)
- หลีกเลี่ยง “date-based versions” ถ้าทีมไม่มีระบบ deprecation ที่เข้มแข็ง

### 4. Request/Response Format

- JSON fields ใช้ **camelCase** (`createdAt`, `userId`) ให้สม่ำเสมอทั้งองค์กร
- Response ใช้ envelope เดียวกันทุก endpoint (ดูตัวอย่างด้านล่าง)
- Errors ต้องใช้ shape มาตรฐานเดียวกัน (แนะนำให้สอดคล้องกับ `64-meta-standards/error-shape-taxonomy/SKILL.md`)
- ระบุ `Content-Type: application/json; charset=utf-8`
- สำหรับ list ให้มี `pagination` (cursor) หรือ `page` (offset) ที่ชัดเจน และไม่ผสมกัน

### 5. Pagination

- ค่าเริ่มต้นใช้ **cursor pagination** สำหรับ data ที่โตเร็ว/มีการเปลี่ยนแปลงตลอด
- offset pagination ใช้ได้กับ dataset เล็ก/รายงานที่ order คงที่
- กำหนดเพดาน `limit` (เช่น 100) และกำหนด default (เช่น 20)
- ต้องระบุ ordering ที่ deterministic (เช่น `(createdAt,id)`)

### 6. Filtering & Sorting

- Filtering: `?status=active&createdAtGte=...&createdAtLt=...`
- Sorting: `?sort=-createdAt` (prefix `-` = desc) หรือ `?sort=createdAt:desc`
- Fields ที่อนุญาตให้ filter/sort ต้อง document ชัดเจน
- หลีกเลี่ยง free-form query ที่ทำให้เกิด SQL injection หรือ query plan แย่

### 7. Authentication & Authorization

- ใช้ `Authorization: Bearer <token>` สำหรับ client-facing APIs
- Service-to-service ให้ใช้ mTLS หรือ signed JWT/OIDC ตาม platform ที่ใช้
- Authorization ต้องชัดเจนว่าเป็น **resource-level** (เช็ค owner/tenant) ไม่ใช่แค่ role
- `401` = ไม่ได้ auth, `403` = auth แล้วแต่ไม่อนุญาต

### 8. GraphQL Conventions (if applicable)

- Query/Mutation ชื่อเป็น verbs ที่สื่อความหมาย (`createOrder`, `cancelOrder`)
- Input types แยกชัดเจน (`CreateOrderInput`), output มี `errors`/`userErrors` ตามมาตรฐานทีม
- หลีกเลี่ยง breaking changes ด้วยการเพิ่ม field ใหม่แทนการเปลี่ยน type เดิม
- ใช้ pagination แบบ Relay (connections) ถ้า ecosystem ใช้อยู่

## Quick Start

```yaml
openapi: 3.0.3
info:
  title: Example API
  version: 1.0.0
paths:
  /api/v1/users:
    get:
      summary: List users
      parameters:
        - in: query
          name: limit
          schema: { type: integer, minimum: 1, maximum: 100, default: 20 }
        - in: query
          name: cursor
          schema: { type: string }
        - in: query
          name: sort
          schema: { type: string, example: "-createdAt" }
      responses:
        "200":
          description: OK
```

## Production Checklist

- [ ] URLs follow naming convention
- [ ] Versioning strategy documented
- [ ] Pagination implemented consistently
- [ ] Error responses follow standard shape
- [ ] OpenAPI spec maintained
- [ ] Rate limiting documented

## REST URL Conventions

```
# Resources (plural nouns)
GET    /api/v1/users           # List users
POST   /api/v1/users           # Create user
GET    /api/v1/users/{id}      # Get user
PUT    /api/v1/users/{id}      # Replace user
PATCH  /api/v1/users/{id}      # Update user
DELETE /api/v1/users/{id}      # Delete user

# Nested resources
GET    /api/v1/users/{id}/orders    # User's orders

# Actions (verbs for non-CRUD)
POST   /api/v1/users/{id}/activate
POST   /api/v1/orders/{id}/cancel

# Filtering & Pagination
GET    /api/v1/users?status=active&limit=20&cursor=abc123
```

## Response Envelope

```typescript
// Success
{
  "data": { ... },
  "meta": {
    "requestId": "req-123",
    "timestamp": "2024-01-15T10:00:00Z"
  }
}

// List with pagination
{
  "data": [...],
  "pagination": {
    "cursor": "next_cursor",
    "hasMore": true
  },
  "meta": { ... }
}
```

## Idempotency (แนะนำสำหรับ POST ที่สำคัญ)

- รองรับ `Idempotency-Key` header สำหรับ create ที่ client อาจ retry (เช่น payment/order)
- เก็บผลลัพธ์ตาม `(clientId, idempotencyKey, endpoint)` ด้วย TTL เพื่อกันการสร้างซ้ำ

## Anti-patterns

1. **Verbs in URLs**: `/api/getUsers` instead of `/api/users`
2. **Inconsistent casing**: `userId` vs `user_id`
3. **No versioning**: Breaking changes break clients
4. **Different pagination**: Cursor here, offset there

## Integration Points

- API gateways
- Client SDK generators
- Documentation tools (Swagger UI)
- Contract testing

## Further Reading

- [Google API Design Guide](https://cloud.google.com/apis/design)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [JSON:API Specification](https://jsonapi.org/)
