---
name: Config Distribution
description: Patterns for distributing configuration and secrets to services safely and consistently across environments (env vars, config files, secret managers, K8s External Secrets, and change process)
---

# Config Distribution

## Overview

วิธีการ distribute configuration ไปยัง services ต่างๆ อย่างปลอดภัยและ consistent: environment variables, config files, secrets management

## Why This Matters

- **Centralized management**: Config อยู่ที่เดียว
- **Security**: Secrets แยกจาก code
- **Flexibility**: เปลี่ยน config โดยไม่ต้อง redeploy
- **Audit**: Track config changes

---

## Core Concepts

### 1. Config vs Secrets (แบ่งให้ชัด)

- **Config**: timeouts, hosts, feature toggles (บางแบบ), limits
- **Secrets**: passwords, API keys, signing keys, tokens → ต้องมาจาก secret manager และห้ามลง repo/logs
- อ้างอิงมาตรฐาน: `64-meta-standards/config-env-conventions/SKILL.md`

### 2. Precedence / Hierarchy

```
Priority (highest to lowest):
1. Runtime secrets (Vault, AWS SM)
2. Environment variables
3. Environment-specific config files
4. Default config files
5. Code defaults
```

### 3. Distribution Methods

### Environment Variables (Simple)
```yaml
# docker-compose.yml
services:
  app:
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://...
    env_file:
      - .env.production
```

### Config Service (Advanced)
```typescript
// Fetch from central config service
const config = await configService.get({
  service: 'user-service',
  environment: 'production',
});
```

### External Secrets (K8s)
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: app-secrets
spec:
  secretStoreRef:
    name: aws-secrets-manager
  target:
    name: app-secrets
  data:
    - secretKey: DATABASE_URL
      remoteRef:
        key: prod/database
        property: url
```

### 4. Validation & Fail-Fast

- validate config ที่ startup (type/format/range) ก่อนรับ traffic
- ป้องกันการ log ค่า secret ด้วย redaction/denylist
- ทุก key ต้อง document ใน `.env.example` (ค่า secret ให้เว้นว่าง + comment แหล่งที่มา)

## Quick Start

1. กำหนด source-of-truth: secret manager (secrets) + env vars/config file (non-secrets)
2. ใช้ schema validation ที่ startup (เช่น Zod/JSON schema)
3. ทำ reload strategy ที่ปลอดภัย (ถ้าต้อง reload runtime)
4. ทำ change process ที่มี audit + rollback

## Config Change Process

1. Update config in source (Git/Vault)
2. CI validates config
3. Deploy/reload applications
4. Verify via health checks

## Production Checklist

- [ ] Secrets อยู่ใน secret manager เท่านั้น (ไม่อยู่ใน repo, image, logs)
- [ ] Config precedence ถูกกำหนดและ document ชัดเจน
- [ ] Config validated at startup (fail fast)
- [ ] `.env.example` ครบ keys และระบุ required/optional
- [ ] มี audit trail และ rollback ของ config changes

## Anti-patterns

1. **Secrets in env files**: เผลอ commit หรือรั่วจาก log/backup
2. **No validation**: config ผิดแล้วพังตอน runtime
3. **Snowflake configs**: แต่ละ service ตั้งชื่อ/ความหมายไม่เหมือนกัน
4. **Uncontrolled reload**: reload config กลางทางจน behavior เปลี่ยนโดยไม่มี guardrails

## Integration Points

- Secret managers (Vault, AWS/GCP/Azure Secret Manager)
- Kubernetes (External Secrets Operator)
- CI/CD (config linting, policy checks)
- Observability (log redaction, config change audit events)

## Further Reading

- [12-Factor Config](https://12factor.net/config)
- [External Secrets Operator](https://external-secrets.io/)
