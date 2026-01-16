---
name: Event Contract Generator
description: Generator สำหรับสร้าง event schemas, types, validators และ documentation สำหรับ event-driven architecture
---

# Event Contract Generator

## Overview

สร้าง event contracts (schemas, types, validators) อัตโนมัติเพื่อให้ producer และ consumer ใช้ event format เดียวกัน

## Why This Matters

- **Type safety**: TypeScript types จาก schema
- **Validation**: Auto-validate events
- **Documentation**: Event catalog อัตโนมัติ
- **Versioning**: Track schema changes

---

## Quick Start

```bash
# Generate event contract
npx generate-event-contract user.created

# Output:
events/user.created/
├── schema.json          # JSON Schema
├── types.ts             # TypeScript types
├── validator.ts         # Validation functions
└── examples.json        # Example events
```

---

## Generated Files

### Schema (JSON Schema)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "UserCreated",
  "type": "object",
  "required": ["eventId", "eventType", "timestamp", "data"],
  "properties": {
    "eventId": { "type": "string", "format": "uuid" },
    "eventType": { "const": "user.created" },
    "timestamp": { "type": "string", "format": "date-time" },
    "data": {
      "type": "object",
      "required": ["userId", "email"],
      "properties": {
        "userId": { "type": "string" },
        "email": { "type": "string", "format": "email" },
        "name": { "type": "string" }
      }
    }
  }
}
```

### TypeScript Types
```typescript
// types.ts (auto-generated)
export interface UserCreatedEvent {
  eventId: string;
  eventType: 'user.created';
  timestamp: string;
  data: {
    userId: string;
    email: string;
    name?: string;
  };
}
```

### Validator
```typescript
// validator.ts (auto-generated)
import Ajv from 'ajv';
import schema from './schema.json';

const ajv = new Ajv();
const validate = ajv.compile(schema);

export function validateUserCreatedEvent(event: unknown): event is UserCreatedEvent {
  return validate(event) as boolean;
}
```

---

## Event Catalog

### Auto-generated Documentation
```markdown
# Event Catalog

## user.created
**Version:** 1.0.0
**Producer:** user-service
**Consumers:** email-service, analytics-service

### Schema
- eventId: UUID (required)
- eventType: "user.created" (required)
- timestamp: ISO 8601 (required)
- data.userId: string (required)
- data.email: email format (required)
- data.name: string (optional)

### Example
```json
{
  "eventId": "123e4567-e89b-12d3-a456-426614174000",
  "eventType": "user.created",
  "timestamp": "2024-01-16T12:00:00Z",
  "data": {
    "userId": "user_123",
    "email": "test@example.com",
    "name": "Test User"
  }
}
```
```

---

## Versioning

```bash
# Create new version
npx generate-event-contract user.created --version 2.0.0

# Output:
events/user.created/
├── v1/
│   ├── schema.json
│   └── types.ts
└── v2/
    ├── schema.json      # New version
    └── types.ts
```

---

## Summary

**Event Contract Generator:** สร้าง event schemas อัตโนมัติ

**Generated:**
- JSON Schema
- TypeScript types
- Validators
- Documentation
- Examples

**Benefits:**
- Type safety
- Auto-validation
- Version control
- Event catalog
