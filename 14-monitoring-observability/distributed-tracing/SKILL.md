# Distributed Tracing

A comprehensive guide to distributed tracing with OpenTelemetry and Jaeger for observability in microservices.

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

### Core Concepts

```
┌─────────────────────────────────────────────────────────────────┐
│                         Trace                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Span 1     │  │   Span 2     │  │   Span 3     │          │
│  │  (Client)    │──>│  (API)      │──>│  (Database) │          │
│  │              │  │              │  │              │          │
│  │ Start: 0ms   │  │ Start: 10ms  │  │ Start: 25ms  │          │
│  │ End: 50ms    │  │ End: 40ms    │  │ End: 35ms    │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Key Terms

| Term | Description |
|------|-------------|
| **Trace** | A collection of spans representing a single request across services |
| **Span** | A single unit of work within a trace |
| **Trace ID** | Unique identifier for the entire trace |
| **Span ID** | Unique identifier for a span |
| **Parent Span ID** | ID of the parent span (for nested spans) |
| **Context** | Contains trace ID, span ID, and propagation data |
| **Baggage** | Key-value pairs propagated across spans |

### Span Attributes

```typescript
interface Span {
  traceId: string;
  spanId: string;
  parentSpanId?: string;
  name: string;
  kind: 'CLIENT' | 'SERVER' | 'PRODUCER' | 'CONSUMER';
  startTime: number;
  endTime: number;
  status: 'OK' | 'ERROR';
  attributes: Record<string, string | number | boolean>;
  events: SpanEvent[];
  links: SpanLink[];
}
```

---

## OpenTelemetry Setup

### Installation

```bash
# Node.js
npm install @opentelemetry/api @opentelemetry/sdk-node
npm install @opentelemetry/auto-instrumentations

# Python
pip install opentelemetry-api
pip install opentelemetry-sdk
pip install opentelemetry-instrumentation
```

### Node.js Setup

```typescript
// tracing.ts
import { NodeSDK } from '@opentelemetry/sdk-node';
import { ConsoleSpanExporter } from '@opentelemetry/sdk-trace-node';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { JaegerExporter } from '@opentelemetry/exporter-trace-jaeger';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations';

const resource = Resource.default().merge(
  new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'api-server',
    [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
    [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: 'production',
  })
);

const sdk = new NodeSDK({
  resource,
  traceExporter: new JaegerExporter({
    endpoint: 'http://jaeger:14268/api/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

### Python Setup

```python
# tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.auto_instrumentation import AutoInstrumentation

resource = Resource.create({
    SERVICE_NAME: "api-server",
    "service.version": "1.0.0",
    "deployment.environment": "production"
})

trace.set_tracer_provider(TracerProvider(resource=resource))

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(jaeger_exporter)
)

# Auto-instrumentation
auto_instrumentation = AutoInstrumentation()
auto_instrumentation.instrument()
```

---

## Instrumentation

### Automatic Instrumentation

```typescript
// Node.js - Auto-instrumentation covers:
// - HTTP/HTTPS
// - Express
// - PostgreSQL
// - MongoDB
// - Redis
// - GraphQL
// - gRPC

import { NodeSDK } from '@opentelemetry/sdk-node';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations';

const sdk = new NodeSDK({
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

```python
# Python - Auto-instrumentation covers:
# - Flask, Django, FastAPI
# - Requests, httpx
# - SQLAlchemy
# - Redis
# - Celery
# - psycopg2

from opentelemetry.instrumentation.auto_instrumentation import AutoInstrumentation

auto_instrumentation = AutoInstrumentation()
auto_instrumentation.instrument()
```

### Manual Instrumentation (Node.js)

```typescript
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('my-service');

async function processOrder(orderId: string) {
  // Create a span
  const span = tracer.startSpan('processOrder', {
    attributes: {
      'order.id': orderId,
      'order.type': 'purchase',
    },
  });

  try {
    // Add event
    span.addEvent('Order received');

    // Do work
    const result = await validateOrder(orderId);
    span.setAttribute('order.valid', true);

    // Create child span
    const childSpan = tracer.startSpan('validateOrder', {
      parent: span,
    });

    try {
      await chargePayment(orderId);
    } finally {
      childSpan.end();
    }

    span.setStatus({ code: SpanStatusCode.OK });
    return result;
  } catch (error) {
    span.recordException(error);
    span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
    throw error;
  } finally {
    span.end();
  }
}
```

### Manual Instrumentation (Python)

```python
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer(__name__)

async def process_order(order_id: str):
    # Create a span
    with tracer.start_as_current_span(
        "processOrder",
        attributes={
            "order.id": order_id,
            "order.type": "purchase"
        }
    ) as span:
        # Add event
        span.add_event("Order received")

        try:
            # Do work
            result = await validate_order(order_id)
            span.set_attribute("order.valid", True)

            # Create child span
            with tracer.start_as_current_span("validateOrder") as child_span:
                await charge_payment(order_id)

            span.set_status(Status(StatusCode.OK))
            return result
        except Exception as error:
            span.record_exception(error)
            span.set_status(Status(StatusCode.ERROR, str(error)))
            raise
```

### HTTP Client Instrumentation (Node.js)

```typescript
import { trace } from '@opentelemetry/api';
import { SemanticAttributes } from '@opentelemetry/semantic-conventions';

async function fetchUserData(userId: string) {
  const tracer = trace.getTracer('user-service');

  return tracer.startActiveSpan('fetchUserData', async (span) => {
    span.setAttribute('user.id', userId);

    try {
      const response = await fetch(`https://api.example.com/users/${userId}`);
      span.setAttribute(SemanticAttributes.HTTP_STATUS_CODE, response.status);

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      return response.json();
    } catch (error) {
      span.recordException(error);
      throw error;
    }
  });
}
```

### Database Instrumentation (Python)

```python
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.semconv.trace import SpanAttributes

tracer = trace.get_tracer(__name__)

def get_user(user_id: str):
    with tracer.start_as_current_span(
        "database.query",
        kind=SpanKind.CLIENT
    ) as span:
        span.set_attribute(SpanAttributes.DB_SYSTEM, "postgresql")
        span.set_attribute(SpanAttributes.DB_NAME, "production")
        span.set_attribute(SpanAttributes.DB_OPERATION, "SELECT")
        span.set_attribute(SpanAttributes.DB_STATEMENT, f"SELECT * FROM users WHERE id = {user_id}")

        try:
            result = db.execute(f"SELECT * FROM users WHERE id = {user_id}")
            span.set_attribute(SpanAttributes.DB_ROW_COUNT, len(result))
            return result
        except Exception as error:
            span.record_exception(error)
            raise
```

---

## Jaeger Backend

### Docker Compose Setup

```yaml
version: '3.8'
services:
  jaeger:
    image: jaegertracing/all-in-one:1.50
    container_name: jaeger
    ports:
      - "5775:5775/udp"   # accept zipkin.thrift over compact thrift protocol
      - "6831:6831/udp"   # accept jaeger.thrift over compact thrift protocol
      - "6832:6832/udp"   # accept jaeger.thrift over binary thrift protocol
      - "5778:5778"       # serve configs
      - "16686:16686"     # serve frontend
      - "14268:14268"     # accept jaeger.thrift directly from clients
      - "14250:14250"     # accept model.proto
      - "9411:9411"       # Zipkin compatible endpoint
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411
      - COLLECTOR_OTLP_ENABLED=true
    networks:
      - tracing

networks:
  tracing:
    driver: bridge
```

### Kubernetes Deployment

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: tracing

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger
  namespace: tracing
spec:
  replicas: 1
  selector:
    matchLabels:
      app: jaeger
  template:
    metadata:
      labels:
        app: jaeger
    spec:
      containers:
      - name: jaeger
        image: jaegertracing/all-in-one:1.50
        ports:
        - containerPort: 16686
        - containerPort: 14268
        env:
        - name: COLLECTOR_ZIPKIN_HOST_PORT
          value: ":9411"

---
apiVersion: v1
kind: Service
metadata:
  name: jaeger
  namespace: tracing
spec:
  selector:
    app: jaeger
  ports:
  - name: ui
    port: 16686
    targetPort: 16686
  - name: collector
    port: 14268
    targetPort: 14268
  type: LoadBalancer
```

### Jaeger Configuration

```yaml
# jaeger-config.yml
collector:
  zipkin:
    host-port: :9411
  otlp:
    enabled: true

storage:
  type: elasticsearch
  elasticsearch:
    server-urls: http://elasticsearch:9200
    index-prefix: jaeger
    tags-as-fields:
      all: true

query:
  base-path: /
```

---

## Trace Correlation

### Correlating Logs with Traces

```typescript
import { trace } from '@opentelemetry/api';

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.printf(({ message, ...meta }) => {
      const spanContext = trace.getSpanContext(trace.getActiveSpan());
      return JSON.stringify({
        message,
        traceId: spanContext?.traceId,
        spanId: spanContext?.spanId,
        ...meta,
      });
    })
  ),
});

// Usage
logger.info('User logged in', { userId: '123' });
// Output: {"message":"User logged in","traceId":"abc123","spanId":"def456","userId":"123"}
```

```python
import logging
from opentelemetry import trace

class TraceContextFilter(logging.Filter):
    def filter(self, record):
        span = trace.get_current_span()
        context = span.get_span_context()
        record.trace_id = f"{context.trace_id:032x}"
        record.span_id = f"{context.span_id:016x}"
        return True

logger = logging.getLogger(__name__)
logger.addFilter(TraceContextFilter())

# Usage
logger.info("User logged in", extra={"user_id": "123"})
# Output: User logged in trace_id=abc123 span_id=def456 user_id=123
```

### Correlating Metrics with Traces

```typescript
import { trace, metrics } from '@opentelemetry/api';

const meter = metrics.getMeter('my-service');
const requestCounter = meter.createCounter('requests_total', {
  description: 'Total requests',
});

function handleRequest(req, res) {
  const span = trace.getActiveSpan();
  const traceId = span?.spanContext().traceId;

  requestCounter.add(1, {
    'trace.id': traceId,
    'route': req.path,
  });
}
```

---

## Context Propagation

### HTTP Headers Propagation

```typescript
import { propagation, trace } from '@opentelemetry/api';

// Server-side - Extract context from incoming request
function handleRequest(req, res) {
  const carrier = propagation.extract(trace.getSpanContext(), propagation.defaultTextMapGetter, req.headers);
  const span = trace.getTracer('server').startSpan('handleRequest', {
    root: carrier === undefined,
  });

  trace.setActiveSpan(span);
  // ... handle request ...
  span.end();
}

// Client-side - Inject context into outgoing request
async function makeRequest(url: string) {
  const headers = {};
  propagation.inject(trace.getActiveSpan(), propagation.defaultTextMapSetter, headers);

  return fetch(url, { headers });
}
```

```python
from opentelemetry import trace, propagate
from flask import request, make_response

# Server-side - Extract context from incoming request
@app.route('/api/endpoint')
def handle_request():
    carrier = {}
    for key, value in request.headers:
        carrier[key] = value

    ctx = propagate.extract(carrier)
    token = context.attach(ctx)

    try:
        # ... handle request ...
        return make_response("OK")
    finally:
        context.detach(token)

# Client-side - Inject context into outgoing request
import requests

def make_request(url: str):
    headers = {}
    propagate.inject(headers)

    return requests.get(url, headers=headers)
```

### gRPC Propagation

```typescript
import { propagation, trace } from '@opentelemetry/api';
import * as grpc from '@grpc/grpc-js';

// Server middleware
function traceInterceptor(options, nextCall) {
  return new grpc.InterceptingCall(nextCall(options), {
    start: (metadata, listener, next) => {
      const carrier = propagation.extract(trace.getSpanContext(), propagation.defaultTextMapGetter, metadata);
      const span = trace.getTracer('grpc').startSpan('grpc.server', {
        root: carrier === undefined,
      });

      next(metadata, {
        ...listener,
        onReceiveMetadata: (metadata, next) => {
          span.setAttributes({
            'rpc.method': metadata.get('method'),
            'rpc.service': metadata.get('service'),
          });
          next(metadata);
        },
      });
    },
  });
}
```

### Message Queue Propagation

```typescript
import { propagation, trace } from '@opentelemetry/api';

// Producer - Inject context into message
async function publishMessage(queue: string, message: any) {
  const headers = {};
  propagation.inject(trace.getActiveSpan(), propagation.defaultTextMapSetter, headers);

  await channel.sendToQueue(queue, Buffer.from(JSON.stringify({
    ...message,
    _traceHeaders: headers,
  })));
}

// Consumer - Extract context from message
channel.consume(queue, async (msg) => {
  const { _traceHeaders, ...message } = JSON.parse(msg.content.toString());
  const ctx = propagation.extract(trace.getSpanContext(), propagation.defaultTextMapGetter, _traceHeaders);
  const token = context.with(ctx, () => trace.startSpan('processMessage'));

  try {
    await processMessage(message);
  } finally {
    token.end();
  }
});
```

---

## Sampling Strategies

### Always Sample

```typescript
import { TraceIdRatioBased } from '@opentelemetry/sdk-trace-base';

const sdk = new NodeSDK({
  traceExporter: new JaegerExporter({ endpoint: 'http://jaeger:14268/api/traces' }),
  sampler: new TraceIdRatioBased(1.0), // 100% sampling
});
```

### Probability Sampling

```typescript
// Sample 10% of traces
const sdk = new NodeSDK({
  sampler: new TraceIdRatioBased(0.1),
});
```

### Parent-Based Sampling

```typescript
import { ParentBasedSampler } from '@opentelemetry/sdk-trace-base';

const sdk = new NodeSDK({
  sampler: new ParentBasedSampler({
    root: new TraceIdRatioBased(0.1), // 10% for root spans
    remoteParentSampled: new AlwaysOnSampler(),
    remoteParentNotSampled: new AlwaysOffSampler(),
    localParentSampled: new AlwaysOnSampler(),
    localParentNotSampled: new AlwaysOffSampler(),
  }),
});
```

### Custom Sampling

```typescript
import { Sampler, SamplingResult } from '@opentelemetry/sdk-trace-base';

class CustomSampler implements Sampler {
  shouldSample(context, traceId, name, kind, attributes, links) {
    // Sample all error spans
    if (attributes['error'] === true) {
      return {
        decision: SamplingDecision.RECORD_AND_SAMPLED,
      };
    }

    // Sample 10% of health check spans
    if (name === 'health-check') {
      return {
        decision: Math.random() < 0.1 ? SamplingDecision.RECORD_AND_SAMPLED : SamplingDecision.NOT_RECORD,
      };
    }

    // Sample 5% of all other spans
    return {
      decision: Math.random() < 0.05 ? SamplingDecision.RECORD_AND_SAMPLED : SamplingDecision.NOT_RECORD,
    };
  }

  toString() {
    return 'CustomSampler';
  }
}

const sdk = new NodeSDK({
  sampler: new CustomSampler(),
});
```

---

## Performance Impact

### Reducing Overhead

```typescript
// Use async span processors
import { BatchSpanProcessor } from '@opentelemetry/sdk-trace-node';

const sdk = new NodeSDK({
  spanProcessor: new BatchSpanProcessor(new JaegerExporter({
    endpoint: 'http://jaeger:14268/api/traces',
  })),
  // Configure batch size and timeout
  traceExporter: new JaegerExporter({
    maxQueueSize: 2048,
    scheduledDelayMillis: 5000,
    exportTimeoutMillis: 30000,
  }),
});
```

### Selective Instrumentation

```typescript
// Only instrument critical paths
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('critical-service');

async function criticalOperation() {
  const span = tracer.startSpan('criticalOperation');
  try {
    // ... critical work ...
  } finally {
    span.end();
  }
}

// Skip instrumentation for non-critical paths
async function backgroundTask() {
  // No tracing for background tasks
  // ... background work ...
}
```

---

## Common Patterns

### Database Query Tracing

```typescript
import { trace } from '@opentelemetry/api';
import { SemanticAttributes } from '@opentelemetry/semantic-conventions';

async function queryDatabase(sql: string, params: any[]) {
  const tracer = trace.getTracer('database');
  const span = tracer.startSpan('database.query', {
    attributes: {
      [SemanticAttributes.DB_SYSTEM]: 'postgresql',
      [SemanticAttributes.DB_NAME]: 'production',
      [SemanticAttributes.DB_STATEMENT]: sql,
      [SemanticAttributes.DB_OPERATION]: sql.split(' ')[0].toUpperCase(),
    },
  });

  try {
    const start = Date.now();
    const result = await db.query(sql, params);
    const duration = Date.now() - start;

    span.setAttribute(SemanticAttributes.DB_ROW_COUNT, result.rowCount);
    span.setAttribute('db.duration_ms', duration);

    return result;
  } catch (error) {
    span.recordException(error);
    throw error;
  } finally {
    span.end();
  }
}
```

### External API Call Tracing

```typescript
import { trace } from '@opentelemetry/api';
import { SemanticAttributes } from '@opentelemetry/semantic-conventions';

async function callExternalAPI(url: string, options: RequestInit) {
  const tracer = trace.getTracer('http-client');
  const span = tracer.startSpan('http.request', {
    kind: SpanKind.CLIENT,
    attributes: {
      [SemanticAttributes.HTTP_URL]: url,
      [SemanticAttributes.HTTP_METHOD]: options.method || 'GET',
    },
  });

  try {
    const response = await fetch(url, options);
    span.setAttribute(SemanticAttributes.HTTP_STATUS_CODE, response.status);

    if (!response.ok) {
      span.setStatus({
        code: SpanStatusCode.ERROR,
        message: `HTTP ${response.status}`,
      });
    }

    return response;
  } catch (error) {
    span.recordException(error);
    span.setStatus({
      code: SpanStatusCode.ERROR,
      message: error.message,
    });
    throw error;
  } finally {
    span.end();
  }
}
```

### Cache Tracing

```typescript
import { trace } from '@opentelemetry/api';
import { SemanticAttributes } from '@opentelemetry/semantic-conventions';

async function getFromCache<T>(key: string): Promise<T | null> {
  const tracer = trace.getTracer('cache');
  const span = tracer.startSpan('cache.get', {
    attributes: {
      'cache.key': key,
      'cache.hit': false,
    },
  });

  try {
    const value = await redis.get(key);

    if (value) {
      span.setAttribute('cache.hit', true);
      return JSON.parse(value);
    }

    return null;
  } finally {
    span.end();
  }
}

async function setCache<T>(key: string, value: T, ttl: number): Promise<void> {
  const tracer = trace.getTracer('cache');
  const span = tracer.startSpan('cache.set', {
    attributes: {
      'cache.key': key,
      'cache.ttl': ttl,
    },
  });

  try {
    await redis.setex(key, ttl, JSON.stringify(value));
  } finally {
    span.end();
  }
}
```

---

## Debugging with Traces

### Finding Slow Requests

```typescript
// Jaeger UI Search
1. Go to http://jaeger:16686
2. Select service
3. Filter by operation
4. Sort by duration
5. Click on trace to view details
```

### Identifying Bottlenecks

```
Trace Timeline:
┌─────────────────────────────────────────────────────────────┐
│ Service A          ┌──────────────────────┐                 │
│                    │     200ms            │                 │
│                    └──────────────────────┘                 │
├─────────────────────────────────────────────────────────────┤
│ Service B          ┌──────────────────────────────────────┐ │
│                    │           180ms                      │ │
│                    └──────────────────────────────────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Database           ┌──────────────────────┐                 │
│                    │     150ms            │                 │
│                    └──────────────────────┘                 │
└─────────────────────────────────────────────────────────────┘

Bottleneck: Database query (150ms / 200ms = 75% of total time)
```

### Error Analysis

```typescript
// Search for error traces
const errorTraces = await jaegerClient.search({
  service: 'api-server',
  operation: 'processOrder',
  tags: [{ key: 'error', value: 'true' }],
});

// Analyze common error patterns
const errorPatterns = errorTraces.reduce((acc, trace) => {
  const errorMessage = trace.spans.find(s => s.tags.find(t => t.key === 'error'))?.tags.find(t => t.key === 'error.message')?.value;
  acc[errorMessage] = (acc[errorMessage] || 0) + 1;
  return acc;
}, {});
```

---

## Production Setup

### Elasticsearch Storage

```yaml
# docker-compose.yml
services:
  jaeger:
    image: jaegertracing/all-in-one:1.50
    environment:
      - SPAN_STORAGE_TYPE=elasticsearch
      - ES_SERVER_URLS=http://elasticsearch:9200
      - ES_TAGS_AS_FIELDS_ALL=true
    depends_on:
      - elasticsearch

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
    volumes:
      - es-data:/usr/share/elasticsearch/data

volumes:
  es-data:
```

### Sampling in Production

```typescript
// Production: Sample 1% of traces
const sampler = process.env.NODE_ENV === 'production'
  ? new TraceIdRatioBased(0.01)
  : new TraceIdRatioBased(1.0);

const sdk = new NodeSDK({ sampler });
```

### Retention Policy

```yaml
# Elasticsearch Index Lifecycle Management
PUT _ilm/policy/jaeger-policy
{
  "policy": {
    "phases": {
      "hot": {
        "actions": {
          "rollover": {
            "max_size": "50GB",
            "max_age": "7d"
          }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": {
            "number_of_shards": 1
          }
        }
      },
      "delete": {
        "min_age": "30d",
        "actions": {
          "delete": {}
        }
      }
    }
  }
}
```

---

## Resources

- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [OpenTelemetry JavaScript](https://github.com/open-telemetry/opentelemetry-js)
- [OpenTelemetry Python](https://github.com/open-telemetry/opentelemetry-python)
- [Trace Context Specification](https://www.w3.org/TR/trace-context/)
