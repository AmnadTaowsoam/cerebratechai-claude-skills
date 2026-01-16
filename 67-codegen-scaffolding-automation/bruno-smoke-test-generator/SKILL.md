---
name: Bruno Smoke Test Generator
description: Generator สำหรับสร้าง Bruno API test collections อัตโนมัติจาก OpenAPI specs หรือ endpoint definitions
---

# Bruno Smoke Test Generator

## Overview

สร้าง Bruno (API testing tool) test collections อัตโนมัติจาก OpenAPI specs เพื่อ smoke test APIs

## Why This Matters

- **Fast testing**: Smoke tests ใน 1 นาที
- **Auto-generated**: จาก OpenAPI spec
- **Version control**: Bruno files เป็น text
- **CI-ready**: Run ใน pipeline ได้

---

## Quick Start

```bash
# Generate from OpenAPI
npx generate-bruno-tests --from-openapi api-spec.yaml

# Output:
bruno/
├── users/
│   ├── create-user.bru
│   ├── get-users.bru
│   └── get-user.bru
└── bruno.json
```

---

## Generated Test

```
# create-user.bru
meta {
  name: Create User
  type: http
  seq: 1
}

post {
  url: {{baseUrl}}/users
  body: json
  auth: bearer
}

auth:bearer {
  token: {{authToken}}
}

body:json {
  {
    "email": "test@example.com",
    "name": "Test User",
    "password": "password123"
  }
}

assert {
  res.status: eq 201
  res.body.data.email: eq test@example.com
}

tests {
  test("should create user", function() {
    expect(res.status).to.equal(201);
    expect(res.body.data).to.have.property('id');
  });
}
```

---

## Environment Variables

```
# bruno/environments/local.bru
vars {
  baseUrl: http://localhost:3000
  authToken: {{process.env.AUTH_TOKEN}}
}
```

---

## Run Tests

```bash
# Run all tests
bruno run bruno/

# Run specific collection
bruno run bruno/users/

# In CI
bruno run bruno/ --env production
```

---

## Summary

**Bruno Test Generator:** สร้าง API smoke tests อัตโนมัติ

**From:**
- OpenAPI specs
- Endpoint definitions
- Existing APIs

**Features:**
- Auto-assertions
- Environment vars
- Auth handling
- CI-ready

**Usage:**
```bash
npx generate-bruno-tests --from-openapi api.yaml
bruno run bruno/
```
