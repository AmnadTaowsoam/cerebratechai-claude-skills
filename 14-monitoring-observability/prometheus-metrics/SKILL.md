# Prometheus Metrics

## Overview

Prometheus is an open-source monitoring and alerting toolkit that collects and stores metrics as time series data. This skill covers Prometheus concepts, metric types, client libraries, and best practices.

## Table of Contents

1. [Prometheus Concepts](#prometheus-concepts)
2. [Metric Types](#metric-types)
3. [Client Libraries](#client-libraries)
4. [Custom Metrics](#custom-metrics)
5. [Labels Best Practices](#labels-best-practices)
6. [Instrumentation Patterns](#instrumentation-patterns)
7. [Service Discovery](#service-discovery)
8. [Scrape Configuration](#scrape-configuration)
9. [Recording Rules](#recording-rules)
10. [Alerting Rules](#alerting-rules)
11. [Best Practices](#best-practices)

---

## Prometheus Concepts

### Architecture

```
┌─────────────┐
│   Targets   │
│  (Services) │
└──────┬──────┘
       │ Scrape
       ↓
┌─────────────┐
│  Prometheus │
│   Server    │
└──────┬──────┘
       │ Query
       ↓
┌─────────────┐
│   Grafana   │
│ Dashboard   │
└─────────────┘
```

### Key Components

| Component | Description |
|-----------|-------------|
| **Prometheus Server** | Scrapes and stores metrics |
| **Targets** | Services exposing metrics endpoints |
| **Exporters** | Programs that expose metrics for non-native services |
| **Alertmanager** | Handles alert routing and notifications |
| **Pushgateway** | For short-lived jobs |

### Time Series Data

```
metric_name{label_name="label_value"} timestamp value
```

Example:
```
http_requests_total{method="GET",path="/api/users",status="200"} 1234567890 42
```

---

## Metric Types

### Counter

A counter is a cumulative metric that represents a single monotonically increasing counter.

```typescript
// counter.ts
import { Counter } from 'prom-client';

const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'path', 'status_code'],
});

// Increment counter
httpRequestsTotal.inc({ method: 'GET', path: '/api/users', status_code: '200' });

// Increment by specific value
httpRequestsTotal.inc({ method: 'POST', path: '/api/users', status_code: '201' }, 1);
```

```python
# counter.py
from prometheus_client import Counter

http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'path', 'status_code']
)

# Increment counter
http_requests_total.labels(method='GET', path='/api/users', status_code='200').inc()

# Increment by specific value
http_requests_total.labels(method='POST', path='/api/users', status_code='201').inc(1)
```

### Gauge

A gauge is a metric that represents a single numerical value that can arbitrarily go up and down.

```typescript
// gauge.ts
import { Gauge } from 'prom-client';

const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Number of active connections',
});

const memoryUsage = new Gauge({
  name: 'memory_usage_bytes',
  help: 'Memory usage in bytes',
  labelNames: ['type'], // e.g., heap, external, array_buffers
});

// Set gauge value
activeConnections.set(42);

// Increment/decrement
activeConnections.inc();
activeConnections.dec();

// Set with labels
memoryUsage.set({ type: 'heap' }, 1024000);
```

```python
# gauge.py
from prometheus_client import Gauge

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

memory_usage = Gauge(
    'memory_usage_bytes',
    'Memory usage in bytes',
    ['type']
)

# Set gauge value
active_connections.set(42)

# Increment/decrement
active_connections.inc()
active_connections.dec()

# Set with labels
memory_usage.labels(type='heap').set(1024000)
```

### Histogram

A histogram samples observations and counts them in configurable buckets.

```typescript
// histogram.ts
import { Histogram } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'path', 'status_code'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
});

// Observe duration
httpRequestDuration.observe({ method: 'GET', path: '/api/users', status_code: '200' }, 0.123);

// Observe with timer
const end = httpRequestDuration.startTimer({ method: 'POST', path: '/api/users' });
// ... do work ...
end({ status_code: '201' });
```

```python
# histogram.py
from prometheus_client import Histogram

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'path', 'status_code'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
)

# Observe duration
http_request_duration.labels(
    method='GET', path='/api/users', status_code='200'
).observe(0.123)

# Observe with timer
with http_request_duration.labels(method='POST', path='/api/users').time():
    # ... do work ...
    http_request_duration.labels(status_code='201').observe()
```

### Summary

A summary samples observations and provides a count and sum of observations plus configurable quantiles.

```typescript
// summary.ts
import { Summary } from 'prom-client';

const httpRequestDuration = new Summary({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'path'],
  percentiles: [0.5, 0.9, 0.95, 0.99],
});

// Observe duration
httpRequestDuration.observe({ method: 'GET', path: '/api/users' }, 0.123);
```

```python
# summary.py
from prometheus_client import Summary

http_request_duration = Summary(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'path']
)

# Observe duration
http_request_duration.labels(method='GET', path='/api/users').observe(0.123)
```

---

## Client Libraries

### Node.js (prom-client)

```typescript
// prom-client-setup.ts
import express from 'express';
import { register, Counter, Gauge, Histogram, collectDefaultMetrics } from 'prom-client';

// Collect default metrics (CPU, memory, etc.)
collectDefaultMetrics({ register });

// Define metrics
const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'path', 'status_code'],
  registers: [register],
});

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'path', 'status_code'],
  registers: [register],
});

// Express middleware
const app = express();

app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const { method, path } = req;
    const status_code = res.statusCode.toString();

    httpRequestsTotal.inc({ method, path, status_code });
    httpRequestDuration.observe({ method, path, status_code }, duration);
  });

  next();
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.listen(3000);
```

### Python (prometheus_client)

```python
# prometheus_client_setup.py
from flask import Flask, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

app = Flask(__name__)

# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'path', 'status_code']
)

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'path', 'status_code']
)

# Middleware
@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    
    http_requests_total.labels(
        method=request.method,
        path=request.path,
        status_code=str(response.status_code)
    ).inc()
    
    http_request_duration.labels(
        method=request.method,
        path=request.path,
        status_code=str(response.status_code)
    ).observe(duration)
    
    return response

# Metrics endpoint
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == '__main__':
    app.run(port=3000)
```

---

## Custom Metrics

### Business Metrics

```typescript
// business-metrics.ts
import { Counter, Gauge, Histogram } from 'prom-client';

// User registrations
const userRegistrationsTotal = new Counter({
  name: 'user_registrations_total',
  help: 'Total number of user registrations',
  labelNames: ['plan', 'source'],
});

// Active users
const activeUsers = new Gauge({
  name: 'active_users',
  help: 'Number of active users',
  labelNames: ['plan'],
});

// Order value
const orderValue = new Histogram({
  name: 'order_value_usd',
  help: 'Order value in USD',
  labelNames: ['currency'],
  buckets: [10, 25, 50, 100, 250, 500, 1000, 2500, 5000],
});

// Usage
userRegistrationsTotal.inc({ plan: 'pro', source: 'organic' });
activeUsers.set({ plan: 'pro' }, 150);
orderValue.observe({ currency: 'USD' }, 99.99);
```

```python
# business_metrics.py
from prometheus_client import Counter, Gauge, Histogram

# User registrations
user_registrations_total = Counter(
    'user_registrations_total',
    'Total number of user registrations',
    ['plan', 'source']
)

# Active users
active_users = Gauge(
    'active_users',
    'Number of active users',
    ['plan']
)

# Order value
order_value = Histogram(
    'order_value_usd',
    'Order value in USD',
    ['currency'],
    buckets=[10, 25, 50, 100, 250, 500, 1000, 2500, 5000]
)

# Usage
user_registrations_total.labels(plan='pro', source='organic').inc()
active_users.labels(plan='pro').set(150)
order_value.labels(currency='USD').observe(99.99)
```

### Database Metrics

```typescript
// database-metrics.ts
import { Counter, Histogram, Gauge } from 'prom-client';

const dbQueryDuration = new Histogram({
  name: 'db_query_duration_seconds',
  help: 'Database query duration in seconds',
  labelNames: ['operation', 'table', 'status'],
  buckets: [0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1],
});

const dbConnectionsActive = new Gauge({
  name: 'db_connections_active',
  help: 'Number of active database connections',
  labelNames: ['pool'],
});

const dbQueryTotal = new Counter({
  name: 'db_query_total',
  help: 'Total number of database queries',
  labelNames: ['operation', 'table', 'status'],
});

// Prisma middleware
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

prisma.$use(async (params, next) => {
  const start = Date.now();
  let status = 'success';

  try {
    const result = await next(params);
    return result;
  } catch (error) {
    status = 'error';
    throw error;
  } finally {
    const duration = (Date.now() - start) / 1000;
    const operation = params.action;
    const table = params.model;

    dbQueryDuration.observe({ operation, table, status }, duration);
    dbQueryTotal.inc({ operation, table, status });
  }
});
```

---

## Labels Best Practices

### Label Naming Conventions

```typescript
// labels.ts
// Good labels
const goodLabels = {
  method: 'GET',        // Lowercase, snake_case
  path: '/api/users',    // Clear, meaningful
  status_code: '200',    // Descriptive
  environment: 'production',
  region: 'us-east-1',
};

// Bad labels
const badLabels = {
  Method: 'GET',         // Mixed case
  p: '/api/users',      // Abbreviated
  sc: '200',           // Unclear
  env: 'prod',         // Abbreviated
  r: 'us-east-1',      // Abbreviated
};
```

### Cardinality Management

```typescript
// cardinality.ts
// High cardinality (avoid)
const badCounter = new Counter({
  name: 'requests_total',
  labelNames: ['user_id', 'request_id'], // Too many unique values
});

// Low cardinality (good)
const goodCounter = new Counter({
  name: 'requests_total',
  labelNames: ['method', 'path', 'status'], // Limited values
});

// Use buckets for high cardinality data
const requestDuration = new Histogram({
  name: 'request_duration_seconds',
  labelNames: ['method', 'path'], // Low cardinality labels
  buckets: [0.1, 0.5, 1, 2, 5, 10], // Buckets for ranges
});
```

### Label Value Guidelines

```typescript
// label-values.ts
// Use consistent values
const statusValues = ['success', 'error', 'timeout'];
const methodValues = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'];
const environmentValues = ['development', 'staging', 'production'];

// Normalize label values
function normalizeStatus(status: number): string {
  if (status >= 200 && status < 300) return 'success';
  if (status >= 400 && status < 500) return 'client_error';
  if (status >= 500) return 'server_error';
  return 'unknown';
}

// Usage
httpRequestsTotal.inc({
  method: 'GET',
  path: '/api/users',
  status_code: normalizeStatus(200),
});
```

---

## Instrumentation Patterns

### HTTP Server Instrumentation

```typescript
// http-instrumentation.ts
import express from 'express';
import { Counter, Histogram, Gauge } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'path', 'status_code'],
});

const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'path', 'status_code'],
});

const httpRequestsInProgress = new Gauge({
  name: 'http_requests_in_progress',
  help: 'Number of HTTP requests in progress',
  labelNames: ['method', 'path'],
});

function createInstrumentedMiddleware() {
  return (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const start = Date.now();
    const { method, path } = req;

    httpRequestsInProgress.inc({ method, path });

    res.on('finish', () => {
      const duration = (Date.now() - start) / 1000;
      const status_code = res.statusCode.toString();

      httpRequestDuration.observe({ method, path, status_code }, duration);
      httpRequestsTotal.inc({ method, path, status_code });
      httpRequestsInProgress.dec({ method, path });
    });

    next();
  };
}

// Usage
const app = express();
app.use(createInstrumentedMiddleware());
```

### Database Instrumentation

```typescript
// database-instrumentation.ts
import { Histogram, Counter, Gauge } from 'prom-client';

const dbQueryDuration = new Histogram({
  name: 'db_query_duration_seconds',
  help: 'Database query duration in seconds',
  labelNames: ['operation', 'table', 'status'],
});

const dbConnectionsActive = new Gauge({
  name: 'db_connections_active',
  help: 'Number of active database connections',
  labelNames: ['pool'],
});

const dbQueryTotal = new Counter({
  name: 'db_query_total',
  help: 'Total number of database queries',
  labelNames: ['operation', 'table', 'status'],
});

async function instrumentedQuery<T>(
  operation: string,
  table: string,
  query: () => Promise<T>
): Promise<T> {
  const start = Date.now();
  let status = 'success';

  try {
    const result = await query();
    return result;
  } catch (error) {
    status = 'error';
    throw error;
  } finally {
    const duration = (Date.now() - start) / 1000;
    dbQueryDuration.observe({ operation, table, status }, duration);
    dbQueryTotal.inc({ operation, table, status });
  }
}

// Usage
const users = await instrumentedQuery('select', 'users', () =>
  prisma.user.findMany()
);
```

### External Service Instrumentation

```typescript
// external-service-instrumentation.ts
import { Histogram, Counter } from 'prom-client';

const externalRequestDuration = new Histogram({
  name: 'external_request_duration_seconds',
  help: 'External API request duration in seconds',
  labelNames: ['service', 'endpoint', 'status'],
});

const externalRequestTotal = new Counter({
  name: 'external_request_total',
  help: 'Total number of external API requests',
  labelNames: ['service', 'endpoint', 'status'],
});

async function instrumentedExternalRequest<T>(
  service: string,
  endpoint: string,
  request: () => Promise<T>
): Promise<T> {
  const start = Date.now();
  let status = 'success';

  try {
    const result = await request();
    return result;
  } catch (error) {
    status = 'error';
    throw error;
  } finally {
    const duration = (Date.now() - start) / 1000;
    externalRequestDuration.observe({ service, endpoint, status }, duration);
    externalRequestTotal.inc({ service, endpoint, status });
  }
}

// Usage
const data = await instrumentedExternalRequest(
  'stripe',
  '/v1/charges',
  () => stripe.charges.create({ amount: 1000, currency: 'usd' })
);
```

---

## Service Discovery

### Static Configuration

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'nodejs-app'
    static_configs:
      - targets:
          - 'localhost:3000'
          - 'localhost:3001'
          - 'localhost:3002'
    metrics_path: '/metrics'
```

### File-Based Discovery

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'nodejs-app'
    file_sd_configs:
      - files:
          - '/etc/prometheus/targets/*.yml'
        refresh_interval: 5s
```

```yaml
# /etc/prometheus/targets/nodejs-app.yml
- targets:
    - 'app1.example.com:3000'
    - 'app2.example.com:3000'
  labels:
    environment: 'production'
```

### Kubernetes Service Discovery

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
```

### Consul Service Discovery

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'consul-services'
    consul_sd_configs:
      - server: 'consul.example.com:8500'
        services: ['nodejs-app', 'python-app']
```

---

## Scrape Configuration

### Basic Scrape Config

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'nodejs-app'
    scrape_interval: 10s
    scrape_timeout: 5s
    metrics_path: '/metrics'
    static_configs:
      - targets: ['localhost:3000']
        labels:
          environment: 'production'
```

### Relabeling

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      # Only scrape pods with prometheus.io/scrape annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true

      # Use custom metrics path from annotation
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)

      # Use custom port from annotation
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__

      # Add namespace label
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace

      # Add pod label
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name
```

### TLS Configuration

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'secure-app'
    scheme: https
    tls_config:
      ca_file: /etc/prometheus/ca.crt
      cert_file: /etc/prometheus/client.crt
      key_file: /etc/prometheus/client.key
      insecure_skip_verify: false
    static_configs:
      - targets: ['secure.example.com:443']
```

---

## Recording Rules

### Basic Recording Rules

```yaml
# recording-rules.yml
groups:
  - name: api
    interval: 30s
    rules:
      # Calculate request rate
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))

      # Calculate error rate
      - record: job:http_requests:errors:rate5m
        expr: sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))

      # Calculate error percentage
      - record: job:http_requests:error_percentage5m
        expr: |
          (
            sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum by (job) (rate(http_requests_total[5m]))
          ) * 100

  - name: database
    interval: 30s
    rules:
      # Calculate query rate
      - record: job:db_query:rate5m
        expr: sum by (job) (rate(db_query_total[5m]))

      # Calculate average query duration
      - record: job:db_query:duration:avg5m
        expr: |
          sum by (job) (rate(db_query_duration_seconds_sum[5m]))
          /
          sum by (job) (rate(db_query_duration_seconds_count[5m]))
```

### Advanced Recording Rules

```yaml
# advanced-recording-rules.yml
groups:
  - name: sla
    interval: 1m
    rules:
      # Calculate 95th percentile latency
      - record: job:http_request:duration:p95
        expr: |
          histogram_quantile(0.95,
            sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
          )

      # Calculate 99th percentile latency
      - record: job:http_request:duration:p99
        expr: |
          histogram_quantile(0.99,
            sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
          )

      # Calculate SLA compliance (requests under 500ms)
      - record: job:http_request:sla:compliance
        expr: |
          (
            sum by (job) (rate(http_request_duration_seconds_bucket{le="0.5"}[5m]))
            /
            sum by (job) (rate(http_request_duration_seconds_count[5m]))
          ) * 100

  - name: availability
    interval: 1m
    rules:
      # Calculate uptime percentage
      - record: job:up:percentage
        expr: |
          avg_over_time(up[5m]) * 100

      # Calculate downtime duration
      - record: job:down:duration_seconds
        expr: |
          sum_over_time((1 - up)[5m]) * 300
```

---

## Alerting Rules

### Basic Alerting Rules

```yaml
# alerting-rules.yml
groups:
  - name: api_alerts
    interval: 30s
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))
            /
            sum by (job) (rate(http_requests_total[5m]))
          ) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} for job {{ $labels.job }}"

      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))
          ) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }}s for job {{ $labels.job }}"

      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service is down"
          description: "Service {{ $labels.job }} has been down for more than 1 minute"
```

### Advanced Alerting Rules

```yaml
# advanced-alerting-rules.yml
groups:
  - name: database_alerts
    interval: 30s
    rules:
      - alert: DatabaseConnectionPoolExhausted
        expr: |
          (
            db_connections_active / db_connections_max
          ) > 0.9
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Database connection pool nearly exhausted"
          description: "{{ $value | humanizePercentage }} of connections are in use"

      - alert: DatabaseSlowQueries
        expr: |
          histogram_quantile(0.99,
            sum by (database, le) (rate(db_query_duration_seconds_bucket[5m]))
          ) > 5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Database slow queries detected"
          description: "99th percentile query latency is {{ $value }}s"

  - name: business_alerts
    interval: 1m
    rules:
      - alert: LowUserRegistrations
        expr: |
          rate(user_registrations_total[1h]) < 0.5
        for: 2h
        labels:
          severity: warning
        annotations:
          summary: "Low user registration rate"
          description: "Registration rate is {{ $value }}/s, below threshold"

      - alert: HighOrderValue
        expr: |
          histogram_quantile(0.99,
            sum by (le) (rate(order_value_usd_bucket[1h]))
          ) > 10000
        for: 30m
        labels:
          severity: info
        annotations:
          summary: "High order value detected"
          description: "99th percentile order value is ${{ $value }}"
```

---

## Best Practices

### 1. Use Meaningful Metric Names

```typescript
// naming.ts
// Good
const goodMetrics = {
  http_requests_total: 'Total HTTP requests',
  http_request_duration_seconds: 'HTTP request duration',
  db_query_duration_seconds: 'Database query duration',
};

// Bad
const badMetrics = {
  reqs: 'Requests', // Abbreviated
  hrd: 'HTTP request duration', // Unclear
  dbq: 'Database query duration', // Abbreviated
};
```

### 2. Label Consistency

```typescript
// consistency.ts
// Use consistent label names across metrics
const commonLabels = {
  method: 'GET',
  path: '/api/users',
  status_code: '200',
  environment: 'production',
  region: 'us-east-1',
};

// Apply to all metrics
httpRequestsTotal.inc(commonLabels);
httpRequestDuration.observe(commonLabels, 0.123);
```

### 3. Avoid High Cardinality

```typescript
// cardinality.ts
// Bad: High cardinality
const badCounter = new Counter({
  name: 'requests_total',
  labelNames: ['user_id', 'request_id', 'timestamp'], // Too many unique values
});

// Good: Low cardinality
const goodCounter = new Counter({
  name: 'requests_total',
  labelNames: ['method', 'path', 'status_code'], // Limited values
});
```

### 4. Use Appropriate Metric Types

```typescript
// metric-types.ts
// Counter: Monotonically increasing values
const requestCount = new Counter({
  name: 'requests_total',
  help: 'Total requests',
});

// Gauge: Values that go up and down
const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Active connections',
});

// Histogram: Distributions
const requestDuration = new Histogram({
  name: 'request_duration_seconds',
  help: 'Request duration',
});
```

### 5. Set Meaningful Buckets

```typescript
// buckets.ts
// Good: Buckets tailored to expected latency
const latencyBuckets = [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10];

const requestDuration = new Histogram({
  name: 'request_duration_seconds',
  help: 'Request duration',
  buckets: latencyBuckets,
});

// Good: Buckets tailored to order values
const orderValueBuckets = [10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000];

const orderValue = new Histogram({
  name: 'order_value_usd',
  help: 'Order value',
  buckets: orderValueBuckets,
});
```

---

## Summary

This skill covers comprehensive Prometheus metrics implementation including:

- **Prometheus Concepts**: Architecture and key components
- **Metric Types**: Counter, Gauge, Histogram, Summary
- **Client Libraries**: Node.js (prom-client) and Python (prometheus_client)
- **Custom Metrics**: Business and database metrics
- **Labels Best Practices**: Naming conventions, cardinality management, value guidelines
- **Instrumentation Patterns**: HTTP server, database, external service instrumentation
- **Service Discovery**: Static, file-based, Kubernetes, Consul
- **Scrape Configuration**: Basic config, relabeling, TLS
- **Recording Rules**: Basic and advanced recording rules
- **Alerting Rules**: Basic and advanced alerting rules
- **Best Practices**: Naming, consistency, cardinality, metric types, buckets
