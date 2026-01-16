---
name: Service Standards Blueprint
description: SSOT blueprint for creating consistent services: folder structure, required endpoints, dependency conventions, interface contracts, docs/testing/security/observability requirements
---

# Service Standards Blueprint

## Overview

Single Source of Truth (SSOT) สำหรับมาตรฐานการสร้าง service ทั้งหมด ให้ AI และคนทำตามได้เหมือนกันทุก service ครอบคลุม structure, naming, dependencies, และ patterns ที่ต้องใช้

## Why This Matters

- **Consistency**: ทุก service หน้าตาเหมือนกัน เข้าใจง่าย
- **Onboarding**: คนใหม่/AI เข้าใจ codebase เร็ว
- **Maintainability**: แก้ที่เดียว apply ทุก service
- **Quality**: มาตรฐานเดียวกัน = คุณภาพเท่ากัน

---

## Core Concepts

### 1. Service Structure Template

หลักการ: โครงเหมือนกันทุก service, แยก concerns ชัดเจน และหา “สิ่งที่สำคัญ” ได้เร็ว

- `src/config/` โหลด config + validation (จาก `64-meta-standards/config-env-conventions/SKILL.md`)
- `src/interfaces/` HTTP handlers / consumers / presenters (boundary)
- `src/domain/` business logic (pure-ish), types, use-cases
- `src/infrastructure/` DB clients, queues, external adapters
- `src/lib/` cross-cutting: logger, tracing, errors
- `tests/` แยก unit/integration ตามความเหมาะสม

### 2. Required Components

ขั้นต่ำที่ทุก service ต้องมี:

- `GET /healthz` (liveness): ตอบ `200` ถ้า process ยังทำงาน
- `GET /readyz` (readiness): เช็ค dependencies ที่จำเป็น (DB/queue) แบบเบา ๆ
- `GET /metrics` (ถ้าใช้ Prometheus): ต้องมี auth หรือจำกัด network ตาม policy
- logging/tracing instrumentation (ดู `64-meta-standards/logging-metrics-tracing-standard/SKILL.md`)

### 3. Dependency Standards

- ใช้ libraries มาตรฐานองค์กรสำหรับ: logging, config validation, error shape, tracing
- pin versions และหลีกเลี่ยง drift ระหว่าง services
- dependency ที่ critical ต้องมี owner และ upgrade cadence

### 4. Interface Contracts

- HTTP APIs ต้องทำตาม `64-meta-standards/api-style-guide/SKILL.md`
- Error responses ต้องทำตาม `64-meta-standards/error-shape-taxonomy/SKILL.md`
- Events ต้องทำตาม `64-meta-standards/event-style-guide/SKILL.md`
- สำหรับ DB: กำหนด conventions ของ primary keys, timestamps, soft delete, tenant scoping (ถ้ามี)

### 5. Documentation Requirements

- มี README ที่ตอบ 5 คำถาม: ทำอะไร / รันยังไง / config อะไรบ้าง / deploy ยังไง / troubleshooting
- มี runbook (สั้น ๆ) สำหรับ alarms หลัก และขั้นตอน rollback
- มี OpenAPI/GraphQL schema หรือ contract ที่ generate ได้

### 6. Testing Standards

- unit tests สำหรับ domain logic และ edge cases สำคัญ
- integration tests สำหรับ DB/queue/external adapters ที่ critical
- contract tests สำหรับ public APIs/events ถ้าทีมมี infra รองรับ
- smoke tests สำหรับ readiness ของ endpoints หลัง deploy

### 7. Security Baseline

- ทำตาม `64-meta-standards/security-baseline-controls/SKILL.md`
- secrets จาก secret manager; ห้าม hardcode; ห้าม log
- input validation ที่ boundary และกำหนด limits ชัดเจน

### 8. Observability Requirements

- logs เป็น JSON และมี `requestId` ทุก request/job
- metrics ขั้นต่ำ: request rate/errors/latency และ saturation (CPU/mem)
- traces propagate ผ่าน downstream calls และมี sampling strategy

## Quick Start

```yaml
service:
  name: example-service
  owner: team-platform
  runtime: nodejs

interfaces:
  http:
    basePath: /api/v1
    health: /healthz
    ready: /readyz
    metrics: /metrics

standards:
  apiStyle: 64-meta-standards/api-style-guide/SKILL.md
  errors: 64-meta-standards/error-shape-taxonomy/SKILL.md
  events: 64-meta-standards/event-style-guide/SKILL.md
  config: 64-meta-standards/config-env-conventions/SKILL.md
  observability: 64-meta-standards/logging-metrics-tracing-standard/SKILL.md
  security: 64-meta-standards/security-baseline-controls/SKILL.md
```

## Production Checklist

- [ ] Service follows folder structure standard
- [ ] All required endpoints implemented (health, ready, metrics)
- [ ] Config follows convention
- [ ] Logging format matches standard
- [ ] Tests meet coverage threshold
- [ ] Documentation complete
- [ ] Error shape + codes documented (catalog)
- [ ] Dashboards/alerts exist for SLOs
- [ ] Runbook exists for top alerts

## Template Structure

```
service-name/
├── src/
│   ├── config/
│   ├── domain/
│   ├── infrastructure/
│   ├── interfaces/
│   └── index.ts
├── tests/
├── docs/
├── .env.example
├── Dockerfile
└── README.md
```

## Minimum Files (แนะนำ)

- `src/config/env.ts` (load + validate config)
- `src/lib/logger.ts` (structured logger + redaction)
- `src/lib/errors.ts` (error helpers + mapping)
- `src/routes/health.ts` (healthz/readyz)
- `src/index.ts` (bootstrap: config → observability → server)

## Anti-patterns

1. **Snowflake services**: ทุก service ต่างกันหมด
2. **Copy-paste drift**: Copy แล้วแก้จน diverge
3. **Undocumented exceptions**: ทำต่างแต่ไม่บอกทำไม
4. **Version sprawl**: Dependencies คนละ version
5. **No ownership**: ไม่มี owner ของ service/alerts/runbooks

## Integration Points

- Scaffolding generators
- CI/CD pipelines
- Code review checklists
- Architecture decision records (ADR)

## Further Reading

- [12-Factor App](https://12factor.net/)
- [Microservices Patterns](https://microservices.io/patterns/)
