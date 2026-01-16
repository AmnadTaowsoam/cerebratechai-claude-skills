---
name: Logging, Metrics & Tracing Standard
description: Observability standards for services: structured logging schema, metrics naming and label rules, trace context propagation, correlation IDs, sensitive-data handling, and cardinality controls
---

# Logging, Metrics & Tracing Standard

## Overview

มาตรฐาน observability สำหรับทุก service: log format, metric naming, trace propagation ที่ทำให้ correlate ข้อมูลข้าม services ได้ และ query/alert ได้ง่าย

## Why This Matters

- **Correlation**: ติดตาม request ข้าม services ได้
- **Query efficiency**: Log/metric format เดียวกัน query ง่าย
- **Alert accuracy**: Metric naming consistent = accurate alerts
- **Debug speed**: หา root cause เร็ว

---

## Core Concepts

### 1. Structured Logging Format

- logs ต้องเป็น JSON เท่านั้น (machine-readable)
- fields ที่ควรมีทุกบรรทัด: `timestamp`, `level`, `service`, `message`, `requestId`
- ถ้ามี tracing ให้ใส่ `traceId`, `spanId`
- context เพิ่มเติมให้ใส่เป็น object ใน `context` (ไม่กระจาย keys แบบสุ่ม)

### 2. Metric Naming Convention

- ชื่อ metric เป็น `snake_case` และสื่อ unit เช่น `_seconds`, `_bytes`, `_total`
- หลีกเลี่ยงชื่อที่ซ้ำ semantics (เช่น `latency` โดยไม่บอก unit)
- labels ต้องจำกัด cardinality (ดูข้อ 7)

### 3. Trace Context Propagation

- ใช้ W3C Trace Context (`traceparent`, `tracestate`) เป็น baseline
- propagate context ผ่าน HTTP/gRPC และ messaging (ถ้าเป็นไปได้) เพื่อให้ trace ต่อเนื่อง
- baggage ใช้เฉพาะข้อมูลที่ปลอดภัยและจำเป็น (ห้าม PII/secret)

### 4. Correlation IDs

- `requestId` ต้องถูกสร้างที่ edge (gateway) หรือ service แรก และส่งต่อไปทุก downstream
- map: `requestId` (app-level) ⟷ `traceId` (distributed tracing) เพื่อ debug ได้ทั้งสองโลก
- ตอบกลับ client ด้วย `X-Request-Id` เพื่อให้ support team อ้างอิงได้

### 5. Log Levels Guidelines

- `DEBUG`: รายละเอียดเฉพาะ dev/staging (ต้องปิดใน prod หรือ sampling)
- `INFO`: business-relevant events (start/stop, state transitions, major actions)
- `WARN`: ความผิดปกติที่ระบบยังทำงานต่อได้ (retrying, degraded mode)
- `ERROR`: request/job ล้มเหลวหรือมี data loss risk (ต้องมี alert routing)

### 6. Sensitive Data Handling

- ห้าม log: passwords, access tokens, refresh tokens, API keys, raw credit cards
- PII ให้ทำ masking/redaction (email/phone) และหลีกเลี่ยง logging payload เต็มของ request
- ให้มี “denylist keys” (เช่น `password`, `authorization`, `cookie`) และ scrub อัตโนมัติ

### 7. Cardinality Management

- ห้ามใช้ `userId`, `email`, `orderId` เป็น metric label
- ใช้ labels ที่มีจำนวนค่าจำกัด: `route`, `method`, `status`, `tenantTier` (ถ้าจำกัดจริง)
- logs สามารถมี identifiers ได้ แต่ต้องคุม PII และทำ sampling ถ้าปริมาณสูง

### 8. Sampling Strategies

- tracing: head-based (เช่น 1–10%) + tail-based สำหรับ errors/slow requests
- logs: sampling สำหรับ noisy endpoints และ DEBUG logs
- ต้องมั่นใจว่า error logs ไม่ถูก sampling จนหายไปจาก incident

## Quick Start

```typescript
import pino from "pino";

export function createLogger(service: string) {
  return pino({
    level: process.env.LOG_LEVEL ?? "info",
    base: { service },
    redact: {
      paths: ["req.headers.authorization", "req.headers.cookie", "*.password", "*.token", "*.apiKey"],
      remove: true,
    },
  });
}
```

## Production Checklist

- [ ] All logs are structured JSON
- [ ] Trace context propagated across services
- [ ] Metrics follow naming convention
- [ ] PII masked in logs
- [ ] Request ID in all log entries
- [ ] Cardinality checked for metrics

## Log Format Standard

```json
{
  "timestamp": "2024-01-15T10:30:00.000Z",
  "level": "INFO",
  "service": "user-service",
  "traceId": "abc123",
  "spanId": "def456",
  "requestId": "req-789",
  "message": "User created successfully",
  "context": {
    "userId": "usr_123",
    "action": "create_user"
  }
}
```

## Metric Naming Convention

```
# Format: <namespace>_<subsystem>_<name>_<unit>

# Examples:
http_requests_total
http_request_duration_seconds
db_connections_active
queue_messages_pending_count
```

## Recommended Metrics (เริ่มต้น)

- `http_requests_total{route,method,status}`
- `http_request_duration_seconds{route,method}` (histogram)
- `db_query_duration_seconds{operation}` (histogram)
- `process_uptime_seconds` / `process_resident_memory_bytes`

## Anti-patterns

1. **Unstructured logs**: Plain text logs
2. **Missing trace context**: Can't correlate
3. **High cardinality labels**: userId as label
4. **Sensitive data in logs**: Passwords, tokens
5. **Free-form labels**: ใส่ค่าที่ไม่จำกัดลง labels จนระบบล่ม

## Integration Points

- Log aggregation (ELK, Loki)
- Metrics (Prometheus, Datadog)
- Tracing (Jaeger, Tempo)
- APM tools

## Further Reading

- [OpenTelemetry Specification](https://opentelemetry.io/docs/specs/)
- [Prometheus Naming Best Practices](https://prometheus.io/docs/practices/naming/)
- [W3C Trace Context](https://www.w3.org/TR/trace-context/)
