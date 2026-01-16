---
name: Observability Packaging
description: Standardize and package logs, metrics, and traces into services by default using a lightweight stack and shared instrumentation with dashboards and alerting
---

# Observability Packaging

## Overview

มาตรฐานการ package observability (logs, metrics, traces) เข้ากับ applications ให้ทุก service มี observability พร้อมใช้ตั้งแต่ day one

## Why This Matters

- **Day-one visibility**: ไม่ต้อง add observability ทีหลัง
- **Consistency**: ทุก service มี dashboards เหมือนกัน
- **Fast debugging**: มีข้อมูลพร้อมเมื่อเกิดปัญหา
- **SLO tracking**: วัด performance ได้ทันที

---

## Core Concepts

### 1. Default Instrumentation (paved road)

- ทุก service ต้องได้: structured logs, request metrics, trace propagation โดยไม่ต้อง “ติดตั้งทีหลัง”
- ใช้ shared library/boilerplate เพื่อให้ fields และ naming consistent
- อ้างอิงมาตรฐาน: `64-meta-standards/logging-metrics-tracing-standard/SKILL.md`

### 2. Golden Signals

- **Latency**, **Traffic**, **Errors**, **Saturation**
- dashboards ต้องมองเห็น 4 อย่างนี้ในหน้าเดียวของ service

### 3. Cardinality & Cost Control

- ห้าม tenantId/userId เป็น metric labels ถ้าทำให้ cardinality ระเบิด
- traces/logs อนุญาตให้ filter ด้วย identifiers ได้ แต่ต้องมี redaction/PII policy

## Observability Stack (Lightweight)

```
Application
    ├── Logs → Loki / CloudWatch
    ├── Metrics → Prometheus / CloudWatch
    └── Traces → Jaeger / X-Ray

Dashboard: Grafana
Alerting: Grafana / PagerDuty
```

## Standard Instrumentation

```typescript
// Packaged in shared library
import { initObservability } from '@company/observability';

initObservability({
  serviceName: 'user-service',
  environment: process.env.NODE_ENV,
  logging: {
    level: 'info',
    format: 'json',
  },
  metrics: {
    enabled: true,
    endpoint: '/metrics',
  },
  tracing: {
    enabled: true,
    sampler: 0.1, // 10% sampling
  },
});
```

## Pre-built Dashboards

```
Dashboard Templates:
├── service-overview.json     # Request rate, errors, latency
├── infrastructure.json       # CPU, memory, disk
├── database.json            # Query time, connections
└── alerts.json              # Alert rules
```

## Metrics to Expose

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total HTTP requests |
| `http_request_duration_seconds` | Histogram | Request latency |
| `http_requests_in_flight` | Gauge | Current requests |
| `app_errors_total` | Counter | Application errors |

## Quick Start

1. ติดตั้ง shared observability package (logger + metrics + tracing) เป็น dependency มาตรฐาน
2. บังคับ fields ที่ต้องมีใน logs และ trace context propagation (W3C)
3. expose `/metrics` และ health endpoints และผูก dashboards ที่เตรียมไว้
4. ตั้ง alert rules ขั้นต่ำ: high error rate, latency regression, saturation, crashloop

## Production Checklist

- [ ] Logs เป็น JSON + redaction ของ secrets/PII
- [ ] Metrics naming/labels ตามมาตรฐาน และคุม cardinality
- [ ] Traces propagate ข้าม services และมี sampling policy
- [ ] Dashboard “service overview” พร้อมใช้งานทุก service
- [ ] Alerts ผูกกับ SLOs และมี runbook link

## Anti-patterns

1. **Instrument later**: รอ incident แล้วค่อยเพิ่ม logs/metrics
2. **High cardinality labels**: ทำให้ monitoring ล่ม/แพง
3. **No correlation IDs**: debug ข้าม service ยากมาก
4. **Leaking secrets**: log tokens/passwords โดยไม่ตั้งใจ

## Integration Points

- OpenTelemetry SDKs / collectors
- Prometheus scraping / managed monitoring (Datadog, CloudWatch)
- Central logging (Loki/ELK/Cloud logs)
- Incident management (PagerDuty/Opsgenie) + runbooks

## Further Reading

- [OpenTelemetry](https://opentelemetry.io/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
