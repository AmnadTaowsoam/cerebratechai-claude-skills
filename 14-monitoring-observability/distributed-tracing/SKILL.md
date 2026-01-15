# Distributed Tracing

## Overview

Distributed tracing helps you understand how requests flow through your distributed system by tracking the journey of a request across multiple services. This skill covers OpenTelemetry, Jaeger, and tracing best practices.

## Table of Contents

1. [Tracing Concepts](#tracing-concepts)
2. [OpenTelemetry Setup](#opentelemetry-setup)
3. [Instrumentation](#instrumentation)
4. [Jaeger Backend](#jaeger-backend)
5. [Trace Correlation](#trace-correlation)
6. [Context Propagation](#context-propagation)
7. [Sampling Strategies](#sampling-strategies)
8. [Performance Impact](#performance-impact)
9. [Common Patterns](#common-patterns)
10. [Debugging with Traces](#debugging-with-traces)
11. [Production Setup](#production-setup)

---

## Tracing Concepts

### Trace, Span, Context

```
Trace: The complete journey of a request
  ├─ Span A: Service 1 (HTTP Handler)
  │   └─ Span B: Service 1 (Database Query)
  ├─ Span C: Service 2 (HTTP Handler)
  │   ├─ Span D: Service 2 (Cache Lookup)
  │   └─ Span E: Service 2 (External API Call)
  └─ Span F: Service 3 (HTTP Handler)
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Trace** | A tree of spans representing the full journey of a request |
| **Span** | A single operation within a trace |
| **Trace ID** | Unique identifier for the entire trace |
| **Span ID** | Unique identifier for a specific span |
| **Parent Span ID** | ID of the parent span (for nested spans) |
| **Context** | Container for trace and span IDs |
| **Baggage** | Key-value pairs that propagate across services |

### Span Attributes

| Attribute | Description | Example |
|------------|-------------|---------|
| `http.method` | HTTP method | `GET`, `POST` |
| `http.url` | Request URL | `/api/users` |
| `http.status_code` | Response status | `200`, `404`, `500` |
| `db.system` | Database type | `postgresql`, `mysql` |
| `db.statement` | SQL query | `SELECT * FROM users` |
| `net.peer.name` | Remote host | `api.example.com` |
| `error` | Error flag | `true` |

---

## OpenTelemetry Setup

### Node.js Setup

```bash
npm install @opentelemetry/api @opentelemetry/sdk-node @opentelemetry/auto-instrumentations-node @opentelemetry/exporter-trace-otlp-grpc
```

```typescript
// tracing.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';

const sdk = new NodeSDK({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'my-service',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: 'production',
  }),
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT || 'http://localhost:4317',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();

console.log('OpenTelemetry tracing initialized');
```

### Python Setup

```bash
pip install opentelemetry-api opentelemetry-sdk opentelemetry-auto-instrumentation opentelemetry-exporter-otlp
```

```python
# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.instrumentation.auto_instrumentation import AutoInstrumentation

# Configure resource
resource = Resource.create({
    SERVICE_NAME: "my-service",
    "service.version": "1.0.0",
    "deployment.environment": "production"
})

# Configure exporter
exporter = OTLPSpanExporter(
    endpoint="localhost:4317",
    insecure=True
)

# Configure tracer provider
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

# Auto-instrumentation
auto_instrumentation = AutoInstrumentation()
auto_instrumentation.instrument()

print("OpenTelemetry tracing initialized")
```

---

## Instrumentation

### Automatic Instrumentation

```typescript
// Node.js - Automatic instrumentation is enabled by default
// No code changes needed for HTTP, database, etc.

// Express example - automatically traced
import express from 'express';

const app = express();

app.get('/api/users', async (req, res) => {
  // This request is automatically traced
  const users = await db.query('SELECT * FROM users');
  res.json(users);
});
```

```python
# Python - Automatic instrumentation
# No code changes needed for Flask, FastAPI, etc.

from fastapi import FastAPI

app = FastAPI()

@app.get("/api/users")
async def get_users():
    # This request is automatically traced
    users = await db.query("SELECT * FROM users")
    return users
```

### Manual Instrumentation

```typescript
// manual-tracing.ts
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('my-service', '1.0.0');

async function processOrder(orderId: string) {
  const span = tracer.startSpan('processOrder', {
    attributes: {
      'order.id': orderId,
    },
  });

  try {
    // Validate order
    const validateSpan = tracer.startSpan('validateOrder', {
      parent: span,
    });
    await validateOrder(orderId);
    validateSpan.end();

    // Process payment
    const paymentSpan = tracer.startSpan('processPayment', {
      parent: span,
    });
    await processPayment(orderId);
    paymentSpan.end();

    // Send confirmation
    const confirmSpan = tracer.startSpan('sendConfirmation', {
      parent: span,
    });
    await sendConfirmation(orderId);
    confirmSpan.end();

    span.setStatus({ code: 1, message: 'OK' });
  } catch (error) {
    span.recordException(error as Error);
    span.setStatus({ code: 2, message: 'ERROR' });
    throw error;
  } finally {
    span.end();
  }
}
```

```python
# manual_tracing.py
from opentelemetry import trace

tracer = trace.get_tracer("my-service", "1.0.0")

async def process_order(order_id: str):
    with tracer.start_as_current_span("processOrder") as span:
        span.set_attribute("order.id", order_id)
        
        try:
            # Validate order
            with tracer.start_as_current_span("validateOrder") as validate_span:
                await validate_order(order_id)
            
            # Process payment
            with tracer.start_as_current_span("processPayment") as payment_span:
                await process_payment(order_id)
            
            # Send confirmation
            with tracer.start_as_current_span("sendConfirmation") as confirm_span:
                await send_confirmation(order_id)
            
            span.set_status(trace.Status(trace.StatusCode.OK))
        except Exception as error:
            span.record_exception(error)
            span.set_status(trace.Status(trace.StatusCode.ERROR, str(error)))
            raise
```

### Database Instrumentation

```typescript
// db-tracing.ts
import { trace, SpanKind } from '@opentelemetry/api';
import { SemanticAttributes } from '@opentelemetry/semantic-conventions';

const tracer = trace.getTracer('database', '1.0.0');

async function queryDatabase(sql: string, params: any[]) {
  const span = tracer.startSpan('database.query', {
    kind: SpanKind.CLIENT,
    attributes: {
      [SemanticAttributes.DB_SYSTEM]: 'postgresql',
      [SemanticAttributes.DB_STATEMENT]: sql,
      [SemanticAttributes.DB_NAME]: 'mydb',
    },
  });

  try {
    const result = await pool.query(sql, params);
    span.setAttribute('db.rows', result.rows.length);
    return result;
  } catch (error) {
    span.recordException(error as Error);
    throw error;
  } finally {
    span.end();
  }
}
```

```python
# db_tracing.py
from opentelemetry import trace, SpanKind
from opentelemetry.semconv.trace import SpanAttributes

tracer = trace.get_tracer("database", "1.0.0")

async def query_database(sql: str, params: list):
    with tracer.start_as_current_span(
        "database.query",
        kind=SpanKind.CLIENT
    ) as span:
        span.set_attribute(SpanAttributes.DB_SYSTEM, "postgresql")
        span.set_attribute(SpanAttributes.DB_STATEMENT, sql)
        span.set_attribute(SpanAttributes.DB_NAME, "mydb")
        
        try:
            result = await pool.query(sql, params)
            span.set_attribute("db.rows", len(result))
            return result
        except Exception as error:
            span.record_exception(error)
            raise
```

### HTTP Client Instrumentation

```typescript
// http-client-tracing.ts
import { trace, SpanKind, propagation } from '@opentelemetry/api';
import { SemanticAttributes } from '@opentelemetry/semantic-conventions';

const tracer = trace.getTracer('http-client', '1.0.0');

async function makeRequest(url: string, options: RequestInit = {}) {
  const span = tracer.startSpan('http.request', {
    kind: SpanKind.CLIENT,
    attributes: {
      [SemanticAttributes.HTTP_METHOD]: options.method || 'GET',
      [SemanticAttributes.HTTP_URL]: url,
    },
  });

  try {
    // Inject trace context into headers
    const headers: Record<string, string> = {};
    propagation.inject(trace.setSpanContext(span.context()), headers);

    const response = await fetch(url, {
      ...options,
      headers: {
        ...headers,
        ...options.headers,
      },
    });

    span.setAttribute(SemanticAttributes.HTTP_STATUS_CODE, response.status);

    return response;
  } catch (error) {
    span.recordException(error as Error);
    throw error;
  } finally {
    span.end();
  }
}
```

```python
# http_client_tracing.py
from opentelemetry import trace, SpanKind, propagation
from opentelemetry.semconv.trace import SpanAttributes
import httpx

tracer = trace.get_tracer("http-client", "1.0.0")

async def make_request(url: str, **kwargs):
    with tracer.start_as_current_span(
        "http.request",
        kind=SpanKind.CLIENT
    ) as span:
        method = kwargs.get("method", "GET")
        span.set_attribute(SpanAttributes.HTTP_METHOD, method)
        span.set_attribute(SpanAttributes.HTTP_URL, url)
        
        # Inject trace context into headers
        headers = kwargs.get("headers", {})
        ctx = trace.get_current()
        propagation.inject(ctx, headers)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    **{k: v for k, v in kwargs.items() if k != "headers"}
                )
            
            span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, response.status_code)
            return response
        except Exception as error:
            span.record_exception(error)
            raise
```

---

## Jaeger Backend

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  jaeger:
    image: jaegertracing/all-in-one:latest
    container_name: jaeger
    ports:
      - "5775:5775/udp"
      - "6831:6831/udp"
      - "6832:6832/udp"
      - "5778:5778"
      - "16686:16686"
      - "14268:14268"
      - "14250:14250"
      - "9411:9411"
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    networks:
      - tracing

  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    container_name: otel-collector
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4317:4317"
      - "4318:4318"
    depends_on:
      - jaeger
    networks:
      - tracing

networks:
  tracing:
    driver: bridge
```

### Collector Configuration

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger]
```

---

## Trace Correlation

### Correlate with Logs

```typescript
// log-correlation.ts
import pino from 'pino';
import { trace } from '@opentelemetry/api';

const logger = pino({
  level: 'info',
  formatters: {
    level: (label) => ({ level: label }),
  },
  base: {
    trace_id: () => trace.getSpanContext()?.traceId,
    span_id: () => trace.getSpanContext()?.spanId,
  },
});

// Usage
logger.info({ userId: '123' }, 'User logged in');
```

```python
# log_correlation.py
import logging
from opentelemetry import trace

class TraceContextFilter(logging.Filter):
    def filter(self, record):
        span_context = trace.get_current_span().get_span_context()
        record.trace_id = span_context.trace_id if span_context else None
        record.span_id = span_context.span_id if span_context else None
        return True

# Configure logging
logger = logging.getLogger(__name__)
logger.addFilter(TraceContextFilter())

# Usage
logger.info("User logged in", extra={"user_id": "123"})
```

### Correlate with Metrics

```typescript
// metric-correlation.ts
import { Counter } from 'prom-client';
import { trace } from '@opentelemetry/api';

const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'path', 'status_code', 'trace_id'],
});

// Usage
const spanContext = trace.getSpanContext();
httpRequestsTotal.inc({
  method: 'GET',
  path: '/api/users',
  status_code: '200',
  trace_id: spanContext?.traceId,
});
```

---

## Context Propagation

### HTTP Headers

```typescript
// context-propagation.ts
import { propagation } from '@opentelemetry/api';

// Extract context from incoming request
function extractContext(headers: Headers) {
  const carrier: Record<string, string> = {};
  headers.forEach((value, key) => {
    carrier[key] = value;
  });

  return propagation.extract(carrier);
}

// Inject context into outgoing request
function injectContext(headers: Headers) {
  const carrier: Record<string, string> = {};
  propagation.inject(trace.setSpanContext(trace.getSpanContext()), carrier);

  for (const [key, value] of Object.entries(carrier)) {
    headers.set(key, value);
  }
}
```

```python
# context_propagation.py
from opentelemetry import trace, propagation

def extract_context(headers: dict):
    """Extract trace context from incoming headers."""
    ctx = propagation.extract(headers)
    return ctx

def inject_context(headers: dict):
    """Inject trace context into outgoing headers."""
    ctx = trace.get_current()
    propagation.inject(ctx, headers)
```

### Express Middleware

```typescript
// express-middleware.ts
import express from 'express';
import { propagation, context } from '@opentelemetry/api';

function tracingMiddleware() {
  return (req: express.Request, res: express.Response, next: express.NextFunction) => {
    // Extract context from incoming headers
    const extractedContext = propagation.extract(req.headers);

    // Set as current context
    context.with(extractedContext, () => {
      next();
    });
  };
}

// Usage
const app = express();
app.use(tracingMiddleware());
```

---

## Sampling Strategies

### Fixed Rate Sampling

```typescript
// sampling.ts
import { Sampler, SamplingResult, TraceIdRatioBased } from '@opentelemetry/sdk-trace-base';

// Sample 10% of traces
const sampler = new TraceIdRatioBased(0.1);

// Or custom sampler
class CustomSampler implements Sampler {
  shouldSample(
    context: any,
    traceId: string,
    spanName: string,
    spanKind: any,
    attributes: any
  ): SamplingResult {
    // Sample all error traces
    if (attributes['error'] === true) {
      return {
        decision: 1, // RECORD_AND_SAMPLED
      };
    }

    // Sample 1% of other traces
    const shouldSample = Math.random() < 0.01;
    return {
      decision: shouldSample ? 1 : 0,
    };
  }
}
```

```python
# sampling.py
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased

# Sample 10% of traces
sampler = TraceIdRatioBased(0.1)

# Or custom sampler
from opentelemetry.sdk.trace.sampling import Sampler, SamplingResult, Decision

class CustomSampler(Sampler):
    def should_sample(
        self,
        parent_context,
        trace_id,
        name,
        kind,
        attributes,
        links,
    ):
        # Sample all error traces
        if attributes.get("error"):
            return SamplingResult(Decision.RECORD_AND_SAMPLED)
        
        # Sample 1% of other traces
        import random
        should_sample = random.random() < 0.01
        return SamplingResult(
            Decision.RECORD_AND_SAMPLED if should_sample else Decision.DROP
        )
```

### Dynamic Sampling

```typescript
// dynamic-sampling.ts
import { Sampler, SamplingResult } from '@opentelemetry/sdk-trace-base';

class DynamicSampler implements Sampler {
  private sampleRates: Map<string, number> = new Map();

  constructor(
    private baseRate: number = 0.01,
    private maxRate: number = 1.0
  ) {}

  shouldSample(
    context: any,
    traceId: string,
    spanName: string,
    spanKind: any,
    attributes: any
  ): SamplingResult {
    // Get service name
    const serviceName = attributes['service.name'] || 'unknown';

    // Get sample rate for this service
    let rate = this.sampleRates.get(serviceName) || this.baseRate;

    // Increase rate for high-traffic services
    if (serviceName === 'api' && rate < this.maxRate) {
      rate = Math.min(rate * 1.1, this.maxRate);
      this.sampleRates.set(serviceName, rate);
    }

    const shouldSample = Math.random() < rate;
    return {
      decision: shouldSample ? 1 : 0,
      attributes: {
        'sampling.rate': rate,
      },
    };
  }
}
```

---

## Performance Impact

### Async Span Processing

```typescript
// async-spans.ts
import { trace, SpanProcessor } from '@opentelemetry/sdk-trace-base';

class AsyncSpanProcessor implements SpanProcessor {
  async forceFlush(): Promise<void> {
    // Flush pending spans
  }

  onStart(span: any, parentContext: any): void {
    // Called when span starts
  }

  onEnd(span: any): void {
    // Called when span ends
    // Process asynchronously
    setImmediate(() => {
      // Export span
    });
  }

  shutdown(): Promise<void> {
    return Promise.resolve();
  }
}
```

### Batch Processing

```typescript
// batch-processor.ts
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-base';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-grpc';

const exporter = new OTLPTraceExporter({
  url: 'http://localhost:4317',
});

// Batch spans for better performance
const batchProcessor = new BatchSpanProcessor(exporter, {
  maxQueueSize: 2048,
  maxExportBatchSize: 512,
  scheduledDelayMillis: 5000,
});

tracerProvider.addSpanProcessor(batchProcessor);
```

---

## Common Patterns

### Request-Response Pattern

```typescript
// request-response.ts
async function handleRequest(req: express.Request, res: express.Response) {
  const tracer = trace.getTracer('http-server');
  const span = tracer.startSpan('http.request', {
    attributes: {
      'http.method': req.method,
      'http.url': req.path,
    },
  });

  try {
    // Process request
    const result = await processRequest(req);

    span.setAttribute('http.status_code', res.statusCode);
    res.json(result);
  } catch (error) {
    span.recordException(error as Error);
    span.setAttribute('http.status_code', 500);
    res.status(500).json({ error: 'Internal server error' });
  } finally {
    span.end();
  }
}
```

### Database Operation Pattern

```typescript
// db-operation.ts
async function executeQuery(sql: string, params: any[]) {
  const tracer = trace.getTracer('database');
  const span = tracer.startSpan('db.query', {
    attributes: {
      'db.system': 'postgresql',
      'db.statement': sql,
    },
  });

  try {
    const start = Date.now();
    const result = await pool.query(sql, params);
    const duration = Date.now() - start;

    span.setAttribute('db.duration_ms', duration);
    span.setAttribute('db.rows', result.rows.length);

    return result;
  } catch (error) {
    span.recordException(error as Error);
    throw error;
  } finally {
    span.end();
  }
}
```

### External Service Pattern

```typescript
// external-service.ts
async function callExternalService(url: string) {
  const tracer = trace.getTracer('http-client');
  const span = tracer.startSpan('http.request', {
    attributes: {
      'http.method': 'GET',
      'http.url': url,
    },
  });

  try {
    const response = await fetch(url);
    span.setAttribute('http.status_code', response.status);
    return response.json();
  } catch (error) {
    span.recordException(error as Error);
    throw error;
  } finally {
    span.end();
  }
}
```

---

## Debugging with Traces

### Find Slow Requests

```typescript
// debug-slow.ts
// In Jaeger UI:
// 1. Search by service name
// 2. Sort by duration (descending)
// 3. Click on trace to see span details
// 4. Identify slow spans
// 5. Check span attributes and logs
```

### Find Error Traces

```typescript
// debug-errors.ts
// In Jaeger UI:
// 1. Search by service name
// 2. Filter by tags: error=true
// 3. Click on trace to see error details
// 4. Check span exceptions
// 5. Correlate with logs
```

### Trace Waterfall Analysis

```typescript
// waterfall-analysis.ts
// In Jaeger UI:
// 1. Select a trace
// 2. View waterfall visualization
// 3. Identify parallel vs sequential operations
// 4. Find bottlenecks (long spans)
// 5. Check for unnecessary synchronous operations
```

---

## Production Setup

### High Availability

```yaml
# docker-compose-ha.yml
version: '3.8'

services:
  jaeger-collector:
    image: jaegertracing/all-in-one:latest
    container_name: jaeger-collector
    ports:
      - "14269:14269"
      - "14268:14268"
      - "14267:14267"
      - "9411:9411"
      - "4317:4317"
      - "4318:4318"
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411
      - COLLECTOR_OTLP_ENABLED=true
    networks:
      - tracing

  jaeger-query:
    image: jaegertracing/all-in-one:latest
    container_name: jaeger-query
    ports:
      - "16686:16686"
      - "16687:16687"
    environment:
      - SPAN_STORAGE_TYPE=elasticsearch
      - ES_SERVER_URLS=http://elasticsearch:9200
    depends_on:
      - elasticsearch
    networks:
      - tracing

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    networks:
      - tracing

networks:
  tracing:
    driver: bridge
```

---

## Summary

This skill covers comprehensive distributed tracing implementation including:

- **Tracing Concepts**: Trace, span, context, and attributes
- **OpenTelemetry Setup**: Node.js and Python setup
- **Instrumentation**: Automatic and manual instrumentation
- **Jaeger Backend**: Docker Compose and collector configuration
- **Trace Correlation**: Correlating with logs and metrics
- **Context Propagation**: HTTP headers and Express middleware
- **Sampling Strategies**: Fixed rate and dynamic sampling
- **Performance Impact**: Async span processing and batch processing
- **Common Patterns**: Request-response, database operation, external service
- **Debugging with Traces**: Finding slow requests, error traces, waterfall analysis
- **Production Setup**: High availability configuration
