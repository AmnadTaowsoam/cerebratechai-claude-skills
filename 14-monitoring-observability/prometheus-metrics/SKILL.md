# Prometheus Metrics

A comprehensive guide to implementing Prometheus metrics for application monitoring and observability.

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

Prometheus is a time-series database and monitoring system that scrapes metrics from configured targets at given intervals.

### Key Concepts

- **Metric**: A named measurement with a set of labeled dimensions
- **Label**: Key-value pairs that add dimensions to metrics
- **Scrape**: The process of collecting metrics from targets
- **Time Series**: A sequence of data points over time
- **PromQL**: Prometheus Query Language for querying metrics

### Architecture

```
┌─────────────┐    Scrape    ┌──────────────┐
│   Targets   │─────────────>│   Prometheus │
│ (Services)  │              │   Server     │
└─────────────┘              └──────┬───────┘
                                     │
                                     │ Query
                                     ▼
                              ┌──────────────┐
                              │   Grafana    │
                              │  Dashboard   │
                              └──────────────┘
```

---

## Metric Types

### Counter

A counter is a cumulative metric that represents a single monotonically increasing counter.

**Use Cases**: Request counts, errors processed, tasks completed

```typescript
import { Counter } from 'prom-client';

const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
});

// Increment counter
httpRequestsTotal.inc({ method: 'GET', route: '/api/users', status_code: 200 });
```

```python
from prometheus_client import Counter

http_requests_total = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'route', 'status_code']
)

# Increment counter
http_requests_total.labels(method='GET', route='/api/users', status_code=200).inc()
```

### Gauge

A gauge is a metric that represents a single numerical value that can arbitrarily go up and down.

**Use Cases**: Memory usage, active connections, temperature

```typescript
import { Gauge } from 'prom-client';

const memoryUsageBytes = new Gauge({
  name: 'memory_usage_bytes',
  help: 'Current memory usage in bytes',
});

// Set gauge value
memoryUsageBytes.set(process.memoryUsage().heapUsed);

// Increment/decrement
memoryUsageBytes.inc(100);
memoryUsageBytes.dec(50);
```

```python
from prometheus_client import Gauge
import psutil

memory_usage_bytes = Gauge(
    'memory_usage_bytes',
    'Current memory usage in bytes'
)

# Set gauge value
memory_usage_bytes.set(psutil.virtual_memory().used)

# Increment/decrement
memory_usage_bytes.inc(100)
memory_usage_bytes.dec(50)
```

### Histogram

A histogram samples observations and counts them in configurable buckets.

**Use Cases**: Request latency, response sizes

```typescript
import { Histogram } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'route'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
});

// Start timer
const end = httpRequestDuration.startTimer();
// ... do work ...
end({ method: 'GET', route: '/api/users' });
```

```python
from prometheus_client import Histogram

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'route'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10)
)

# Start timer
with http_request_duration.labels(method='GET', route='/api/users').time():
    # ... do work ...
    pass
```

### Summary

A summary samples observations and provides a count and sum of observations plus configurable quantiles.

**Use Cases**: Request latency with configurable quantiles

```typescript
import { Summary } from 'prom-client';

const requestDuration = new Summary({
  name: 'request_duration_seconds',
  help: 'Request duration in seconds',
  labelNames: ['endpoint'],
  percentiles: [0.5, 0.9, 0.95, 0.99],
});

// Start timer
const end = requestDuration.startTimer();
// ... do work ...
end({ endpoint: '/api/users' });
```

```python
from prometheus_client import Summary

request_duration = Summary(
    'request_duration_seconds',
    'Request duration in seconds',
    ['endpoint'],
    registry=registry
)

# Start timer
with request_duration.labels(endpoint='/api/users').time():
    # ... do work ...
    pass
```

---

## Client Libraries

### Node.js (prom-client)

```typescript
import express from 'express';
import { register, Counter, Histogram, Gauge } from 'prom-client';
import promBundle from 'express-prom-bundle';

const app = express();

// Auto-instrument express
const metricsMiddleware = promBundle({
  includeMethod: true,
  includePath: true,
  includeStatusCode: true,
  promClient: {
    collectDefaultMetrics: {
      timeout: 5000,
    },
  },
});

app.use(metricsMiddleware);

// Custom metrics
const activeConnections = new Gauge({
  name: 'active_connections',
  help: 'Number of active connections',
});

// Expose metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});

app.listen(3000);
```

### Python (prometheus_client)

```python
from flask import Flask, Response
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client.flask_exposer import FlaskExposer

app = Flask(__name__)

# Expose metrics endpoint
FlaskExposer(app)

# Custom metrics
request_count = Counter(
    'request_count',
    'Total request count',
    ['method', 'endpoint']
)

request_duration = Histogram(
    'request_duration_seconds',
    'Request duration',
    ['method', 'endpoint']
)

@app.route('/')
def hello():
    request_count.labels(method='GET', endpoint='/').inc()
    return 'Hello World'

if __name__ == '__main__':
    app.run(port=3000)
```

---

## Custom Metrics

### Business Metrics

```typescript
import { Counter, Gauge } from 'prom-client';

// Track user registrations
const userRegistrations = new Counter({
  name: 'user_registrations_total',
  help: 'Total number of user registrations',
  labelNames: ['plan_type', 'source'],
});

// Track active subscriptions
const activeSubscriptions = new Gauge({
  name: 'active_subscriptions',
  help: 'Number of active subscriptions',
  labelNames: ['plan_type'],
});

// Track revenue
const revenue = new Gauge({
  name: 'revenue_usd',
  help: 'Total revenue in USD',
  labelNames: ['plan_type'],
});

// Usage examples
userRegistrations.inc({ plan_type: 'pro', source: 'organic' });
activeSubscriptions.set({ plan_type: 'pro' }, 150);
revenue.inc({ plan_type: 'pro' }, 99.99);
```

```python
from prometheus_client import Counter, Gauge

# Track user registrations
user_registrations = Counter(
    'user_registrations_total',
    'Total number of user registrations',
    ['plan_type', 'source']
)

# Track active subscriptions
active_subscriptions = Gauge(
    'active_subscriptions',
    'Number of active subscriptions',
    ['plan_type']
)

# Track revenue
revenue = Gauge(
    'revenue_usd',
    'Total revenue in USD',
    ['plan_type']
)

# Usage examples
user_registrations.labels(plan_type='pro', source='organic').inc()
active_subscriptions.labels(plan_type='pro').set(150)
revenue.labels(plan_type='pro').inc(99.99)
```

### Database Metrics

```typescript
import { Counter, Histogram, Gauge } from 'prom-client';

const dbQueryDuration = new Histogram({
  name: 'db_query_duration_seconds',
  help: 'Database query duration',
  labelNames: ['operation', 'table'],
});

const dbConnections = new Gauge({
  name: 'db_connections_active',
  help: 'Active database connections',
  labelNames: ['pool'],
});

const dbQueryErrors = new Counter({
  name: 'db_query_errors_total',
  help: 'Total database query errors',
  labelNames: ['operation', 'table', 'error_type'],
});

// Usage
async function queryDatabase(operation: string, table: string, query: string) {
  const end = dbQueryDuration.startTimer({ operation, table });
  try {
    const result = await db.query(query);
    end();
    return result;
  } catch (error) {
    dbQueryErrors.inc({ operation, table, error_type: error.name });
    end();
    throw error;
  }
}
```

---

## Labels Best Practices

### Cardinality Management

High cardinality labels can cause performance issues.

```typescript
// ❌ BAD - High cardinality
const requestsByUser = new Counter({
  name: 'requests_by_user_total',
  help: 'Requests per user',
  labelNames: ['user_id'], // Can have millions of values
});

// ✅ GOOD - Low cardinality
const requestsByStatus = new Counter({
  name: 'requests_by_status_total',
  help: 'Requests by status',
  labelNames: ['status'], // Limited values (200, 400, 500)
});

// ✅ GOOD - Medium cardinality (use with caution)
const requestsByRegion = new Counter({
  name: 'requests_by_region_total',
  help: 'Requests by region',
  labelNames: ['region'], // Limited regions (us-east-1, eu-west-1, etc.)
});
```

### Label Naming Conventions

```typescript
// Use snake_case for label names
const metric = new Counter({
  name: 'api_requests_total',
  help: 'API requests',
  labelNames: [
    'method',        // HTTP method
    'route',         // API route
    'status_code',   // HTTP status code
    'version',       // API version
  ],
});

// Use consistent values
metric.inc({ method: 'GET', route: '/api/users', status_code: '200', version: 'v1' });
```

---

## Instrumentation Patterns

### Middleware Instrumentation

```typescript
import { Request, Response, NextFunction } from 'express';
import { Histogram, Counter } from 'prom-client';

const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'HTTP request duration',
  labelNames: ['method', 'route', 'status_code'],
});

const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
});

export function metricsMiddleware(req: Request, res: Response, next: NextFunction) {
  const start = Date.now();

  // Capture response
  const originalSend = res.send;
  res.send = function(...args) {
    const duration = (Date.now() - start) / 1000;
    const route = req.route?.path || req.path;
    const statusCode = res.statusCode.toString();

    httpRequestDuration.observe({ method: req.method, route, status_code: statusCode }, duration);
    httpRequestsTotal.inc({ method: req.method, route, status_code: statusCode });

    return originalSend.apply(this, args);
  };

  next();
}
```

### Database Instrumentation

```typescript
import { Histogram } from 'prom-client';

const dbQueryDuration = new Histogram({
  name: 'db_query_duration_seconds',
  help: 'Database query duration',
  labelNames: ['operation', 'table', 'index_used'],
});

export function instrumentQuery<T>(
  operation: string,
  table: string,
  queryFn: () => Promise<T>
): Promise<T> {
  const end = dbQueryDuration.startTimer({ operation, table });
  return queryFn()
    .then(result => {
      end({ index_used: 'yes' });
      return result;
    })
    .catch(error => {
      end({ index_used: 'no' });
      throw error;
    });
}
```

---

## Service Discovery

### Static Configuration

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'api-server'
    static_configs:
      - targets: ['localhost:3000', 'localhost:3001', 'localhost:3002']
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
```

### Consul Service Discovery

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'consul-services'
    consul_sd_configs:
      - server: 'localhost:8500'
        services: ['api', 'worker', 'web']
```

---

## Scrape Configuration

### Basic Scrape Config

```yaml
# prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    replica: '1'

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'node-exporter'
    static_configs:
      - targets: ['localhost:9100']

  - job_name: 'api-server'
    scrape_interval: 10s
    scrape_timeout: 5s
    static_configs:
      - targets:
          - 'api-server-1:3000'
          - 'api-server-2:3000'
          - 'api-server-3:3000'
```

### Advanced Scrape Config

```yaml
scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
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

---

## Recording Rules

Recording rules allow you to precompute frequently needed or computationally expensive expressions.

```yaml
# rules/recording.yml
groups:
  - name: api
    interval: 30s
    rules:
      # Calculate request rate per route
      - record: job:http_requests:rate5m
        expr: sum by (job, route) (rate(http_requests_total[5m]))

      # Calculate error rate
      - record: job:http_requests:error_rate5m
        expr: |
          sum by (job, route) (rate(http_requests_total{status_code=~"5.."}[5m]))
          /
          sum by (job, route) (rate(http_requests_total[5m]))

      # Calculate 95th percentile latency
      - record: job:http_request_duration:p95
        expr: histogram_quantile(0.95, sum by (job, le) (rate(http_request_duration_seconds_bucket[5m])))

  - name: database
    interval: 1m
    rules:
      # Calculate query rate
      - record: job:db_queries:rate1m
        expr: sum by (job) (rate(db_query_duration_seconds_count[1m]))

      # Calculate average query duration
      - record: job:db_query_duration:avg1m
        expr: |
          sum by (job) (rate(db_query_duration_seconds_sum[1m]))
          /
          sum by (job) (rate(db_query_duration_seconds_count[1m]))
```

---

## Alerting Rules

Alerting rules define conditions that trigger alerts.

```yaml
# rules/alerting.yml
groups:
  - name: api_alerts
    rules:
      # High error rate
      - alert: HighErrorRate
        expr: |
          sum by (job) (rate(http_requests_total{status_code=~"5.."}[5m]))
          /
          sum by (job) (rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High error rate on {{ $labels.job }}"
          description: "Error rate is {{ $value | humanizePercentage }} for the last 5 minutes"

      # High latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, sum by (job, le) (rate(http_request_duration_seconds_bucket[5m]))) > 1
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "High latency on {{ $labels.job }}"
          description: "95th percentile latency is {{ $value }}s"

      # Service down
      - alert: ServiceDown
        expr: up{job="api-server"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.job }} is down"
          description: "{{ $labels.instance }} has been down for more than 1 minute"

  - name: database_alerts
    rules:
      # High connection usage
      - alert: HighConnectionUsage
        expr: |
          db_connections_active / db_connections_max > 0.8
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High database connection usage"
          description: "{{ $value | humanizePercentage }} of connections are in use"

      # Slow queries
      - alert: SlowQueries
        expr: |
          histogram_quantile(0.99, sum by (le) (rate(db_query_duration_seconds_bucket[5m]))) > 5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow database queries detected"
          description: "99th percentile query duration is {{ $value }}s"
```

---

## Best Practices

### 1. Choose the Right Metric Type

| Scenario | Metric Type | Why |
|----------|-------------|-----|
| Request counts | Counter | Monotonically increasing |
| Memory usage | Gauge | Goes up and down |
| Request latency | Histogram | Provides buckets for quantiles |
| Response size | Summary | Configurable quantiles |

### 2. Use Meaningful Labels

```typescript
// ✅ Good - Descriptive labels
const metric = new Counter({
  name: 'api_requests_total',
  labelNames: ['method', 'route', 'status_code', 'version'],
});

// ❌ Bad - Too many labels, high cardinality
const metric = new Counter({
  name: 'api_requests_total',
  labelNames: ['method', 'route', 'status_code', 'version', 'user_id', 'request_id', 'timestamp'],
});
```

### 3. Monitor Your Monitoring

```typescript
import { Gauge, Histogram } from 'prom-client';

// Monitor scrape duration
const scrapeDuration = new Histogram({
  name: 'prometheus_scrape_duration_seconds',
  help: 'Duration of Prometheus scrape',
  labelNames: ['job'],
});

// Monitor metric cardinality
const metricCardinality = new Gauge({
  name: 'metric_cardinality',
  help: 'Number of unique label combinations',
  labelNames: ['metric_name'],
});
```

### 4. Use Consistent Naming

```typescript
// Naming convention: <target>_<metric>_<unit>
const api_requests_total = new Counter({
  name: 'api_requests_total',
  help: 'Total API requests',
});

const api_request_duration_seconds = new Histogram({
  name: 'api_request_duration_seconds',
  help: 'API request duration in seconds',
});

const api_response_size_bytes = new Histogram({
  name: 'api_response_size_bytes',
  help: 'API response size in bytes',
});
```

### 5. Set Appropriate Bucket Sizes

```typescript
// For latency metrics, choose buckets based on your SLA
const requestDuration = new Histogram({
  name: 'request_duration_seconds',
  help: 'Request duration',
  buckets: [
    0.001,   // 1ms
    0.005,   // 5ms
    0.01,    // 10ms
    0.025,   // 25ms
    0.05,    // 50ms
    0.1,     // 100ms
    0.25,    // 250ms
    0.5,     // 500ms
    1,       // 1s
    2.5,     // 2.5s
    5,       // 5s
    10,      // 10s
  ],
});
```

### 6. Instrument Early

```typescript
// Instrument from the start of development
import { Counter } from 'prom-client';

const userActions = new Counter({
  name: 'user_actions_total',
  help: 'Total user actions',
  labelNames: ['action_type'],
});

function handleUserAction(action: string) {
  userActions.inc({ action_type: action });
  // ... rest of logic
}
```

### 7. Use Default Metrics

```typescript
import { collectDefaultMetrics } from 'prom-client';

// Collect default metrics (CPU, memory, etc.)
collectDefaultMetrics({
  timeout: 5000,
  gcDurationBuckets: [0.001, 0.01, 0.1, 1, 2, 5],
});
```

### 8. Test Your Metrics

```typescript
import { register } from 'prom-client';

describe('Metrics', () => {
  beforeEach(() => {
    register.clear();
  });

  it('should increment request counter', () => {
    const counter = new Counter({
      name: 'test_counter',
      help: 'Test counter',
    });

    counter.inc();
    counter.inc();

    const metrics = register.getSingleMetric('test_counter')?.get() as any;
    expect(metrics.values[0].value).toBe(2);
  });
});
```

---

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)
- [PromQL Cheat Sheet](https://promlabs.com/promql-cheat-sheet/)
- [prom-client Documentation](https://github.com/siimon/prom-client)
- [prometheus_client Documentation](https://github.com/prometheus/client_python)
