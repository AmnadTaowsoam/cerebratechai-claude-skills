# Performance Monitoring

## Overview

Application Performance Monitoring (APM) helps you understand how your application performs from the user's perspective. This skill covers APM concepts, key metrics, tools, and best practices.

## Table of Contents

1. [APM Concepts](#apm-concepts)
2. [Key Metrics](#key-metrics)
3. [Tools](#tools)
4. [Database Query Monitoring](#database-query-monitoring)
5. [N+1 Query Detection](#n1-query-detection)
6. [Memory Profiling](#memory-profiling)
7. [CPU Profiling](#cpu-profiling)
8. [Bottleneck Identification](#bottleneck-identification)
9. [Performance Budgets](#performance-budgets)
10. [Best Practices](#best-practices)

---

## APM Concepts

### What is APM?

APM (Application Performance Monitoring) is the practice of monitoring software applications to ensure they perform as expected and meet user expectations.

### APM Architecture

```
┌─────────────┐
│  End Users  │
└──────┬──────┘
       │ Requests
       ↓
┌─────────────┐
│  Your App   │
└──────┬──────┘
       │ Metrics
       ↓
┌─────────────┐
│   APM Agent │
└──────┬──────┘
       │ Data
       ↓
┌─────────────┐
│ APM Backend │
└──────┬──────┘
       │
       ↓
┌─────────────┐
│  Dashboard  │
└─────────────┘
```

### APM Components

| Component | Description |
|-----------|-------------|
| **Agent** | Software installed on your app that collects metrics |
| **Backend** | Central server that receives and stores metrics |
| **Dashboard** | UI for visualizing metrics and traces |
| **Alerting** | System for notifying about performance issues |

---

## Key Metrics

### Response Time

The time it takes for a request to complete.

```typescript
// response-time.ts
import express from 'express';

const app = express();

app.use((req, res, next) => {
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`${req.method} ${req.path} - ${duration}ms`);
  });

  next();
});
```

```python
# response_time.py
from flask import Flask, request, g
import time

app = Flask(__name__)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    duration = (time.time() - g.start_time) * 1000
    print(f"{request.method} {request.path} - {duration}ms")
    return response
```

### Throughput

The number of requests processed per unit of time.

```typescript
// throughput.ts
let requestCount = 0;

setInterval(() => {
  console.log(`Throughput: ${requestCount} requests/sec`);
  requestCount = 0;
}, 1000);

app.use((req, res, next) => {
  requestCount++;
  next();
});
```

```python
# throughput.py
import time
from collections import defaultdict

request_counts = defaultdict(int)

@app.before_request
def before_request():
    request_counts[request.path] += 1

def print_throughput():
    while True:
        time.sleep(1)
        print(f"Throughput: {sum(request_counts.values())} requests/sec")

import threading
thread = threading.Thread(target=print_throughput, daemon=True)
thread.start()
```

### Error Rate

The percentage of requests that result in errors.

```typescript
// error-rate.ts
let totalRequests = 0;
let errorRequests = 0;

app.use((req, res, next) => {
  totalRequests++;

  res.on('finish', () => {
    if (res.statusCode >= 400) {
      errorRequests++;
    }
  });

  next();
});

setInterval(() => {
  const errorRate = (errorRequests / totalRequests) * 100;
  console.log(`Error rate: ${errorRate.toFixed(2)}%`);
}, 10000);
```

```python
# error_rate.py
from flask import Flask, request, g
import time

app = Flask(__name__)

total_requests = 0
error_requests = 0

@app.before_request
def before_request():
    global total_requests
    total_requests += 1

@app.after_request
def after_request(response):
    global error_requests
    if response.status_code >= 400:
        error_requests += 1
    return response

def print_error_rate():
    while True:
        time.sleep(10)
        error_rate = (error_requests / total_requests) * 100
        print(f"Error rate: {error_rate:.2f}%")

import threading
thread = threading.Thread(target=print_error_rate, daemon=True)
thread.start()
```

### Apdex Score

Application Performance Index measures user satisfaction based on response times.

```typescript
// apdex.ts
interface ApdexConfig {
  threshold: number; // Response time threshold (seconds)
  samples: number[];
}

function calculateApdex(config: ApdexConfig): number {
  const { threshold, samples } = config;

  let satisfied = 0;
  let tolerating = 0;
  let frustrated = 0;

  for (const sample of samples) {
    if (sample <= threshold) {
      satisfied++;
    } else if (sample <= threshold * 4) {
      tolerating++;
    } else {
      frustrated++;
    }
  }

  const total = samples.length;
  return (satisfied + tolerating / 2) / total;
}

// Usage
const responseTimes = [0.1, 0.2, 0.15, 0.8, 0.3, 2.5, 0.4];
const apdex = calculateApdex({ threshold: 0.5, samples: responseTimes });

console.log(`Apdex: ${apdex.toFixed(3)}`); // 0.714
// 0.714 = 71.4% user satisfaction
```

```python
# apdex.py
from typing import List

def calculate_apdex(threshold: float, samples: List[float]) -> float:
    """Calculate Apdex score."""
    satisfied = 0
    tolerating = 0
    frustrated = 0
    
    for sample in samples:
        if sample <= threshold:
            satisfied += 1
        elif sample <= threshold * 4:
            tolerating += 1
        else:
            frustrated += 1
    
    total = len(samples)
    return (satisfied + tolerating / 2) / total

# Usage
response_times = [0.1, 0.2, 0.15, 0.8, 0.3, 2.5, 0.4]
apdex = calculate_apdex(0.5, response_times)

print(f"Apdex: {apdex:.3f}")  # 0.714
```

---

## Tools

### New Relic

```bash
npm install newrelic
```

```typescript
// newrelic.ts
import newrelic from 'newrelic';

// Automatic instrumentation
// No code changes needed for HTTP, database, etc.

// Custom instrumentation
newrelic.startSegment('customOperation', () => {
  // Your code here
});

// Record custom metrics
newrelic.recordMetric('Custom/Metric', 42);

// Record custom events
newrelic.recordCustomEvent('CustomEvent', {
  attribute1: 'value1',
  attribute2: 'value2',
});
```

```python
# newrelic.py
import newrelic.agent

# Automatic instrumentation
# No code changes needed for Flask, Django, etc.

# Custom instrumentation
@newrelic.agent.function_trace()
def custom_operation():
    # Your code here
    pass

# Record custom metrics
newrelic.agent.record_custom_metric('Custom/Metric', 42)

# Record custom events
newrelic.agent.record_custom_event('CustomEvent', {
    'attribute1': 'value1',
    'attribute2': 'value2'
})
```

### DataDog APM

```bash
npm install dd-trace
```

```typescript
// datadog.ts
import tracer from 'dd-trace';

tracer.init({
  service: 'my-service',
  env: 'production',
  logInjection: true,
});

// Custom span
const span = tracer.startSpan('customOperation');
try {
  // Your code here
} finally {
  span.finish();
}

// Record custom metrics
tracer.recordMetric('custom.metric', 42);

// Record custom events
tracer.recordEvent('CustomEvent', {
  attribute1: 'value1',
  attribute2: 'value2',
});
```

```python
# datadog.py
from ddtrace import tracer, patch_all

# Patch all supported libraries
patch_all()

# Custom span
@tracer.wrap('custom', 'operation')
def custom_operation():
    # Your code here
    pass

# Record custom metrics
tracer.metric('custom.metric', 42)

# Record custom events
tracer.event('CustomEvent', {
    'attribute1': 'value1',
    'attribute2': 'value2'
})
```

### Elastic APM

```bash
npm install elastic-apm-node
```

```typescript
// elastic-apm.ts
import apm from 'elastic-apm-node';

apm.start({
  serviceName: 'my-service',
  serverUrl: 'http://apm-server:8200',
  environment: 'production',
});

// Custom span
const span = apm.startSpan('customOperation');
try {
  // Your code here
} finally {
  span.end();
}

// Record custom metrics
apm.setCustomContext({
  customMetric: 42,
});

// Record custom events
apm.captureError(new Error('Custom error'));
```

```python
# elastic_apm.py
from elasticapm import Client

apm = Client(
    service_name='my-service',
    server_url='http://apm-server:8200',
    environment='production'
)

# Custom span
with apm.capture_span('custom_operation'):
    # Your code here
    pass

# Record custom metrics
apm.set_custom_context({
    'custom_metric': 42
})

# Record custom events
apm.capture_exception(Exception('Custom error'))
```

---

## Database Query Monitoring

### Query Duration Tracking

```typescript
// db-monitoring.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

prisma.$use(async (params, next) => {
  const start = Date.now();
  let result;

  try {
    result = await next(params);
  } catch (error) {
    const duration = Date.now() - start;
    console.log(`DB Query: ${params.action} on ${params.model} - ${duration}ms`);
    throw error;
  }

  const duration = Date.now() - start;
  console.log(`DB Query: ${params.action} on ${params.model} - ${duration}ms`);

  return result;
});
```

```python
# db_monitoring.py
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time

@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    print(f"DB Query: {statement} - {total * 1000:.2f}ms")
```

### Slow Query Detection

```typescript
// slow-query.ts
const SLOW_QUERY_THRESHOLD = 1000; // 1 second

prisma.$use(async (params, next) => {
  const start = Date.now();

  try {
    return await next(params);
  } finally {
    const duration = Date.now() - start;

    if (duration > SLOW_QUERY_THRESHOLD) {
      console.warn(`SLOW QUERY: ${params.action} on ${params.model} - ${duration}ms`);
    }
  }
});
```

```python
# slow_query.py
SLOW_QUERY_THRESHOLD = 1.0  # 1 second

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    
    if total > SLOW_QUERY_THRESHOLD:
        print(f"SLOW QUERY: {statement} - {total:.2f}s")
```

---

## N+1 Query Detection

### Detect N+1 Queries

```typescript
// n-plus-one.ts
const queryCounts = new Map<string, number>();

prisma.$use(async (params, next) => {
  const key = `${params.action}:${params.model}`;
  const count = queryCounts.get(key) || 0;
  queryCounts.set(key, count + 1);

  const result = await next(params);

  // Check for N+1 queries
  if (count > 10) {
    console.warn(`Potential N+1 query detected: ${key} - ${count + 1} queries`);
  }

  // Reset counter after request
  setTimeout(() => {
    queryCounts.set(key, 0);
  }, 0);

  return result;
});
```

```python
# n_plus_one.py
from collections import defaultdict

query_counts = defaultdict(int)

def check_n_plus_one(action: str, model: str):
    """Check for N+1 queries."""
    key = f"{action}:{model}"
    query_counts[key] += 1
    
    if query_counts[key] > 10:
        print(f"Potential N+1 query detected: {key} - {query_counts[key]} queries")
    
    # Reset counter after request
    import threading
    timer = threading.Timer(0, lambda: query_counts.__setitem__(key, 0))
    timer.start()
```

### Fix N+1 Queries

```typescript
// fix-n-plus-one.ts
// Bad: N+1 queries
async function getUsersWithPostsBad() {
  const users = await prisma.user.findMany();

  for (const user of users) {
    const posts = await prisma.post.findMany({
      where: { userId: user.id },
    });
    user.posts = posts;
  }

  return users;
}

// Good: Single query with includes
async function getUsersWithPostsGood() {
  return prisma.user.findMany({
    include: {
      posts: true,
    },
  });
}
```

```python
# fix_n_plus_one.py
# Bad: N+1 queries
async def get_users_with_posts_bad():
    users = await prisma.user.find_many()
    
    for user in users:
        posts = await prisma.post.find_many(
            where={'user_id': user.id}
        )
        user.posts = posts
    
    return users

# Good: Single query with includes
async def get_users_with_posts_good():
    return await prisma.user.find_many(
        include={
            'posts': True
        }
    )
```

---

## Memory Profiling

### Node.js Memory Profiling

```typescript
// memory-profiling.ts
import v8 from 'v8';

// Get heap statistics
function getHeapStats() {
  const stats = v8.getHeapStatistics();

  console.log('Heap Statistics:');
  console.log(`  Total heap size: ${(stats.total_heap_size / 1024 / 1024).toFixed(2)} MB`);
  console.log(`  Used heap size: ${(stats.used_heap_size / 1024 / 1024).toFixed(2)} MB`);
  console.log(`  Heap size limit: ${(stats.heap_size_limit / 1024 / 1024).toFixed(2)} MB`);
  console.log(`  Malloced memory: ${(stats.malloced_memory / 1024 / 1024).toFixed(2)} MB`);
}

// Get heap snapshot
function getHeapSnapshot() {
  const snapshot = v8.getHeapSnapshot();
  return snapshot;
}

// Monitor memory usage
setInterval(() => {
  const used = process.memoryUsage();
  console.log(`Memory Usage:`);
  console.log(`  RSS: ${(used.rss / 1024 / 1024).toFixed(2)} MB`);
  console.log(`  Heap Total: ${(used.heapTotal / 1024 / 1024).toFixed(2)} MB`);
  console.log(`  Heap Used: ${(used.heapUsed / 1024 / 1024).toFixed(2)} MB`);
  console.log(`  External: ${(used.external / 1024 / 1024).toFixed(2)} MB`);
}, 60000); // Every minute
```

### Python Memory Profiling

```python
# memory_profiling.py
import psutil
import gc
import time

def get_memory_stats():
    """Get memory statistics."""
    process = psutil.Process()
    mem_info = process.memory_info()
    
    print('Memory Usage:')
    print(f'  RSS: {mem_info.rss / 1024 / 1024:.2f} MB')
    print(f'  VMS: {mem_info.vms / 1024 / 1024:.2f} MB')
    print(f'  Heap: {process.memory_info().rss / 1024 / 1024:.2f} MB')

def get_object_stats():
    """Get Python object statistics."""
    gc.collect()
    
    print('Object Statistics:')
    print(f'  Total objects: {len(gc.get_objects())}')
    print(f'  Unreachable objects: {len(gc.garbage)}')

def monitor_memory():
    """Monitor memory usage."""
    while True:
        get_memory_stats()
        get_object_stats()
        time.sleep(60)  # Every minute

import threading
thread = threading.Thread(target=monitor_memory, daemon=True)
thread.start()
```

---

## CPU Profiling

### Node.js CPU Profiling

```typescript
// cpu-profiling.ts
import { Profiler } from 'v8';

const profiler = new Profiler();

// Start profiling
profiler.startProfiling('cpu-profile', 1, 1000);

// Run your code
// ...

// Stop profiling
const profile = profiler.stopProfiling('cpu-profile');

// Save profile
const fs = require('fs');
fs.writeFileSync('cpu-profile.cpuprofile', JSON.stringify(profile));
```

### Python CPU Profiling

```python
# cpu_profiling.py
import cProfile
import pstats
import io

def profile_function(func):
    """Decorator to profile a function."""
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        
        # Print stats
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats()
        print(s.getvalue())
        
        return result
    
    return wrapper

# Usage
@profile_function
def my_function():
    # Your code here
    pass
```

---

## Bottleneck Identification

### Identify Slow Endpoints

```typescript
// slow-endpoints.ts
import express from 'express';

const app = express();
const endpointStats = new Map<string, { count: number; totalTime: number }>();

app.use((req, res, next) => {
  const start = Date.now();
  const endpoint = `${req.method} ${req.path}`;

  res.on('finish', () => {
    const duration = Date.now() - start;
    const stats = endpointStats.get(endpoint) || { count: 0, totalTime: 0 };
    stats.count++;
    stats.totalTime += duration;
    endpointStats.set(endpoint, stats);

    const avgTime = stats.totalTime / stats.count;
    console.log(`${endpoint} - ${duration}ms (avg: ${avgTime.toFixed(0)}ms)`);
  });

  next();
});

// Print slow endpoints
setInterval(() => {
  console.log('\nSlow Endpoints:');
  const sorted = Array.from(endpointStats.entries())
    .sort((a, b) => b[1].totalTime / b[1].count - a[1].totalTime / a[1].count);

  for (const [endpoint, stats] of sorted.slice(0, 10)) {
    const avgTime = stats.totalTime / stats.count;
    console.log(`  ${endpoint} - ${avgTime.toFixed(0)}ms (${stats.count} requests)`);
  }
}, 60000);
```

### Identify Memory Leaks

```typescript
// memory-leaks.ts
import v8 from 'v8';

const heapSnapshots: any[] = [];

function takeHeapSnapshot() {
  const snapshot = v8.getHeapSnapshot();
  heapSnapshots.push({
    timestamp: Date.now(),
    snapshot,
  });

  // Keep only last 10 snapshots
  if (heapSnapshots.length > 10) {
    heapSnapshots.shift();
  }

  // Check for memory leak
  if (heapSnapshots.length >= 2) {
    const current = heapSnapshots[heapSnapshots.length - 1];
    const previous = heapSnapshots[heapSnapshots.length - 2];

    const currentSize = current.snapshot.getHeapStatistics().used_heap_size;
    const previousSize = previous.snapshot.getHeapStatistics().used_heap_size;
    const growth = currentSize - previousSize;

    if (growth > 10 * 1024 * 1024) { // 10MB growth
      console.warn(`Memory leak detected: ${(growth / 1024 / 1024).toFixed(2)} MB growth`);
    }
  }
}

// Take snapshot every minute
setInterval(takeHeapSnapshot, 60000);
```

---

## Performance Budgets

### Define Performance Budgets

```typescript
// performance-budgets.ts
interface PerformanceBudget {
  name: string;
  budget: number;
  actual: number;
  threshold: number; // Percentage of budget
}

const budgets: PerformanceBudget[] = [
  {
    name: 'First Contentful Paint (FCP)',
    budget: 1800, // 1.8 seconds
    actual: 0,
    threshold: 0.8, // 80% of budget
  },
  {
    name: 'Largest Contentful Paint (LCP)',
    budget: 2500, // 2.5 seconds
    actual: 0,
    threshold: 0.75, // 75% of budget
  },
  {
    name: 'Time to Interactive (TTI)',
    budget: 3800, // 3.8 seconds
    actual: 0,
    threshold: 0.8, // 80% of budget
  },
  {
    name: 'Total Blocking Time (TBT)',
    budget: 300, // 300ms
    actual: 0,
    threshold: 0.8, // 80% of budget
  },
];

function checkBudgets(): void {
  let failed = false;

  for (const budget of budgets) {
    const threshold = budget.budget * budget.threshold;

    if (budget.actual > threshold) {
      console.error(`Budget exceeded: ${budget.name}`);
      console.error(`  Budget: ${budget.budget}ms`);
      console.error(`  Actual: ${budget.actual}ms`);
      console.error(`  Threshold: ${threshold}ms`);
      failed = true;
    }
  }

  if (!failed) {
    console.log('All budgets within threshold');
  }
}
```

### Web Vitals Monitoring

```tsx
// web-vitals.tsx
import { onCLS, onFID, onFCP, onLCP, onTTFB } from 'web-vitals';

function sendToAnalytics(metric: any) {
  // Send to your analytics service
  console.log(metric);
}

onCLS(sendToAnalytics);
onFID(sendToAnalytics);
onFCP(sendToAnalytics);
onLCP(sendToAnalytics);
onTTFB(sendToAnalytics);
```

---

## Best Practices

### 1. Monitor Key Metrics

```typescript
// key-metrics.ts
// Monitor these metrics:
// - Response time
// - Throughput
// - Error rate
// - Apdex score
// - Memory usage
// - CPU usage
// - Database query time
```

### 2. Set Alerts

```typescript
// alerts.ts
// Alert when:
// - Response time > threshold
// - Error rate > threshold
// - Memory usage > threshold
// - CPU usage > threshold
// - Database query time > threshold
```

### 3. Profile Regularly

```typescript
// profiling.ts
// Profile your application:
// - Before major releases
// - When performance issues are reported
// - Regularly (e.g., weekly)
```

### 4. Use Sampling

```typescript
// sampling.ts
// Sample expensive operations to reduce overhead
const shouldSample = Math.random() < 0.1; // 10% sampling

if (shouldSample) {
  // Profile or trace this operation
}
```

### 5. Correlate Metrics

```typescript
// correlate.ts
// Correlate metrics to find patterns:
// - High response time with high CPU usage
// - High error rate with database issues
// - Memory leaks with specific operations
```

---

## Summary

This skill covers comprehensive performance monitoring implementation including:

- **APM Concepts**: What is APM and architecture
- **Key Metrics**: Response time, throughput, error rate, Apdex score
- **Tools**: New Relic, DataDog APM, Elastic APM
- **Database Query Monitoring**: Query duration tracking and slow query detection
- **N+1 Query Detection**: Detecting and fixing N+1 queries
- **Memory Profiling**: Node.js and Python memory profiling
- **CPU Profiling**: Node.js and Python CPU profiling
- **Bottleneck Identification**: Slow endpoints and memory leaks
- **Performance Budgets**: Defining and checking budgets
- **Best Practices**: Monitoring, alerts, profiling, sampling, correlation
