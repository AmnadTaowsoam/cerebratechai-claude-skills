# Performance Monitoring

A comprehensive guide to Application Performance Monitoring (APM) for production applications.

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

Application Performance Monitoring (APM) is the practice of monitoring software applications to ensure they perform well and meet user expectations.

```
┌─────────────────────────────────────────────────────────────┐
│                    APM Architecture                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   Client    │  │   Server    │  │  Database   │       │
│  │   Browser   │  │   Node.js   │  │  PostgreSQL │       │
│  │             │  │             │  │             │       │
│  │  [Metrics]  │  │  [Metrics]  │  │  [Metrics]  │       │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘       │
│         │                │                │               │
│         └────────────────┼────────────────┘               │
│                          ▼                                │
│                   ┌─────────────┐                         │
│                   │   APM Tool  │                         │
│                   │ (New Relic) │                         │
│                   │ (DataDog)   │                         │
│                   │ (Elastic)   │                         │
│                   └─────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

### APM Benefits

| Benefit | Description |
|---------|-------------|
| **Proactive Detection** | Identify issues before users report them |
| **Root Cause Analysis** | Quickly find what's causing performance problems |
| **Capacity Planning** | Understand resource usage for scaling decisions |
| **SLA Compliance** | Monitor and report on service level agreements |
| **User Experience** | Ensure fast, responsive applications |

---

## Key Metrics

### Response Time

The time it takes for a request to complete.

```typescript
// Measure response time
import { performance } from 'perf_hooks';

async function handleRequest(req, res) {
  const start = performance.now();

  try {
    // ... process request ...
    const result = await processOrder(req.body);
    res.json(result);
  } finally {
    const duration = performance.now() - start;
    metrics.record('response_time', duration, {
      route: req.path,
      method: req.method,
    });
  }
}
```

```python
import time
import prometheus_client

response_time = prometheus_client.Histogram(
    'response_time_seconds',
    'Response time',
    ['route', 'method']
)

def handle_request(request):
    start = time.time()
    try:
        # ... process request ...
        result = process_order(request.data)
        return jsonify(result)
    finally:
        duration = time.time() - start
        response_time.labels(
            route=request.path,
            method=request.method
        ).observe(duration)
```

### Throughput

The number of requests processed per unit of time.

```typescript
// Track throughput
const requestCounter = new Counter({
  name: 'requests_total',
  help: 'Total requests',
  labelNames: ['route', 'method'],
});

app.use((req, res, next) => {
  requestCounter.inc({ route: req.path, method: req.method });
  next();
});
```

### Error Rate

The percentage of requests that result in errors.

```typescript
// Calculate error rate
const errorRate = new Gauge({
  name: 'error_rate',
  help: 'Error rate',
  labelNames: ['route'],
});

setInterval(() => {
  const errors = errorCounter.getValue();
  const total = requestCounter.getValue();
  const rate = errors / total;
  errorRate.set({ route: 'api' }, rate);
}, 60000);
```

### Apdex Score

Application Performance Index - a measure of user satisfaction.

```
Apdex = (Satisfied + (Tolerating / 2)) / Total

Where:
- Satisfied: Response time ≤ T (threshold)
- Tolerating: T < Response time ≤ 4T
- Frustrated: Response time > 4T

Example:
- T = 500ms
- 100 requests: 80 satisfied, 15 tolerating, 5 frustrated
- Apdex = (80 + 15/2) / 100 = 0.875 (87.5%)
```

```typescript
function calculateApdex(responses: number[], threshold: number): number {
  const satisfied = responses.filter(r => r <= threshold).length;
  const tolerating = responses.filter(r => r > threshold && r <= threshold * 4).length;
  const total = responses.length;

  return (satisfied + tolerating / 2) / total;
}
```

---

## Tools

### New Relic

```typescript
// Installation
npm install newrelic

// newrelic.js
exports.config = {
  app_name: ['My Application'],
  license_key: process.env.NEW_RELIC_LICENSE_KEY,
  logging: {
    level: 'info',
  },
  application_logging: {
    enabled: true,
  },
  distributed_tracing: {
    enabled: true,
  },
};

// main.ts
import newrelic from 'newrelic';

// Automatic instrumentation
// No code changes required for Express, MongoDB, etc.
```

### DataDog APM

```typescript
// Installation
npm install dd-trace

// Initialize
import tracer from 'dd-trace';

tracer.init({
  service: 'api-server',
  env: process.env.NODE_ENV,
  logInjection: true,
  analytics: true,
});

// Manual instrumentation
import tracer from 'dd-trace';

async function processOrder(orderId: string) {
  const span = tracer.startSpan('processOrder', {
    tags: {
      'order.id': orderId,
    },
  });

  try {
    const result = await validateOrder(orderId);
    span.setTag('order.valid', true);
    return result;
  } catch (error) {
    span.setTag('error', error.message);
    throw error;
  } finally {
    span.finish();
  }
}
```

### Elastic APM

```typescript
// Installation
npm install elastic-apm-node

// Initialize
import apm from 'elastic-apm-node';

apm.start({
  serviceName: 'api-server',
  serverUrl: process.env.ELASTIC_APM_SERVER_URL,
  secretToken: process.env.ELASTIC_APM_SECRET_TOKEN,
  environment: process.env.NODE_ENV,
});

// Manual transaction
async function handleRequest(req, res) {
  const transaction = apm.startTransaction('handleRequest', 'request');

  try {
    const result = await processOrder(req.body);
    res.json(result);
    transaction.end('success');
  } catch (error) {
    transaction.end('error');
    throw error;
  }
}
```

---

## Database Query Monitoring

### Query Duration Tracking

```typescript
import { performance } from 'perf_hooks';

async function queryDatabase<T>(sql: string, params: any[]): Promise<T> {
  const start = performance.now();

  try {
    const result = await db.query(sql, params);
    const duration = performance.now() - start;

    metrics.record('db_query_duration', duration, {
      operation: sql.split(' ')[0].toUpperCase(),
      table: extractTable(sql),
    });

    return result;
  } catch (error) {
    metrics.increment('db_query_errors', {
      operation: sql.split(' ')[0].toUpperCase(),
    });
    throw error;
  }
}
```

```python
import time
import prometheus_client

db_query_duration = prometheus_client.Histogram(
    'db_query_duration_seconds',
    'Database query duration',
    ['operation', 'table']
)

async def query_database(sql: str, params: list):
    start = time.time()
    try:
        result = await db.execute(sql, params)
        duration = time.time() - start

        operation = sql.split()[0].upper()
        table = extract_table(sql)

        db_query_duration.labels(
            operation=operation,
            table=table
        ).observe(duration)

        return result
    except Exception as error:
        # Track errors
        pass
        raise
```

### Slow Query Logging

```typescript
const SLOW_QUERY_THRESHOLD = 1000; // 1 second

async function queryDatabase<T>(sql: string, params: any[]): Promise<T> {
  const start = performance.now();

  try {
    const result = await db.query(sql, params);
    const duration = performance.now() - start;

    if (duration > SLOW_QUERY_THRESHOLD) {
      logger.warn('Slow query detected', {
        sql,
        params: sanitizeParams(params),
        duration,
      });
    }

    return result;
  } catch (error) {
    throw error;
  }
}
```

### Query Frequency Tracking

```typescript
const queryFrequency = new Map<string, number>();

function trackQuery(sql: string) {
  const normalized = normalizeSQL(sql);
  queryFrequency.set(normalized, (queryFrequency.get(normalized) || 0) + 1);

  if (queryFrequency.get(normalized) > 100) {
    logger.warn('High frequency query detected', {
      sql: normalized,
      frequency: queryFrequency.get(normalized),
    });
  }
}
```

---

## N+1 Query Detection

### What is N+1 Query Problem?

```
N+1 Query Problem:
- 1 query to fetch N records
- N queries to fetch related data for each record

Example:
1. SELECT * FROM users (N=10 users)
2. SELECT * FROM posts WHERE user_id = 1
3. SELECT * FROM posts WHERE user_id = 2
...
11. SELECT * FROM posts WHERE user_id = 10

Total: 11 queries (1 + N)
```

### Detection with APM

```typescript
// Detect N+1 queries
const queryCount = new Map<string, number>();

async function detectNPlusOne() {
  queryCount.clear();

  // Run operation
  await fetchUsersWithPosts();

  // Check for patterns
  for (const [query, count] of queryCount.entries()) {
    if (count > 10) {
      logger.warn('Potential N+1 query detected', {
        query,
        count,
      });
    }
  }
}

// Wrap database client
const originalQuery = db.query.bind(db);
db.query = function(sql: string, params: any[]) {
  const key = normalizeSQL(sql);
  queryCount.set(key, (queryCount.get(key) || 0) + 1);
  return originalQuery(sql, params);
};
```

### Prevention with Eager Loading

```typescript
// ❌ BAD - N+1 queries
async function getUsersWithPosts() {
  const users = await db.query('SELECT * FROM users');

  for (const user of users) {
    user.posts = await db.query(
      'SELECT * FROM posts WHERE user_id = ?',
      [user.id]
    );
  }

  return users;
}

// ✅ GOOD - Single query with JOIN
async function getUsersWithPosts() {
  return await db.query(`
    SELECT
      users.*,
      posts.id as post_id,
      posts.title as post_title
    FROM users
    LEFT JOIN posts ON users.id = posts.user_id
  `);
}

// ✅ GOOD - Using ORM eager loading
async function getUsersWithPosts() {
  return await User.findAll({
    include: [Post],
  });
}
```

### Prevention with DataLoader

```typescript
import DataLoader from 'dataloader';

const postsLoader = new DataLoader(async (userIds: readonly string[]) => {
  const posts = await db.query(
    'SELECT * FROM posts WHERE user_id IN (?)',
    [userIds]
  );

  return userIds.map(id =>
    posts.filter(post => post.user_id === id)
  );
});

async function getUserPosts(userId: string) {
  return await postsLoader.load(userId);
}
```

---

## Memory Profiling

### Node.js Memory Profiling

```typescript
// Get memory usage
function getMemoryUsage() {
  const usage = process.memoryUsage();
  return {
    rss: usage.rss / 1024 / 1024, // MB
    heapTotal: usage.heapTotal / 1024 / 1024,
    heapUsed: usage.heapUsed / 1024 / 1024,
    external: usage.external / 1024 / 1024,
  };
}

// Track memory over time
setInterval(() => {
  const usage = getMemoryUsage();
  metrics.record('memory_usage', usage.heapUsed, {
    type: 'heap_used',
  });
}, 60000);

// Detect memory leaks
let previousUsage = getMemoryUsage();
setInterval(() => {
  const currentUsage = getMemoryUsage();
  const increase = currentUsage.heapUsed - previousUsage.heapUsed;

  if (increase > 100) { // 100 MB increase
    logger.warn('Potential memory leak detected', {
      increase: `${increase} MB`,
      current: currentUsage,
    });
  }

  previousUsage = currentUsage;
}, 300000); // Check every 5 minutes
```

### Heap Snapshot Analysis

```typescript
import { writeHeapSnapshot } from 'v8';

// Take heap snapshot
function takeHeapSnapshot() {
  const filename = `heap-${Date.now()}.heapsnapshot`;
  writeHeapSnapshot(filename);
  logger.info(`Heap snapshot saved: ${filename}`);
}

// Schedule snapshots
setInterval(takeHeapSnapshot, 3600000); // Every hour
```

### Python Memory Profiling

```python
import psutil
import prometheus_client

memory_usage = prometheus_client.Gauge(
    'memory_usage_bytes',
    'Memory usage',
    ['type']
)

def track_memory():
    process = psutil.Process()
    memory_info = process.memory_info()

    memory_usage.labels(type='rss').set(memory_info.rss)
    memory_usage.labels(type='vms').set(memory_info.vms)

# Track memory over time
import threading
def memory_tracker():
    while True:
        track_memory()
        time.sleep(60)

threading.Thread(target=memory_tracker, daemon=True).start()
```

---

## CPU Profiling

### Node.js CPU Profiling

```typescript
import { Profiler } from 'v8';

// Start CPU profiler
const profiler = new Profiler();
profiler.startProfiling('cpu-profile', true);

// ... run application for some time ...

// Stop and save profile
const profile = profiler.stopProfiling('cpu-profile');
profile.export((error, result) => {
  if (!error) {
    fs.writeFileSync('cpu-profile.cpuprofile', result);
  }
});

// Load in Chrome DevTools
// chrome://inspect -> Profiler -> Load
```

### Python CPU Profiling

```python
import cProfile
import pstats
from io import StringIO

def profile_function(func, *args, **kwargs):
    pr = cProfile.Profile()
    pr.enable()

    result = func(*args, **kwargs)

    pr.disable()

    # Print stats
    s = StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
    ps.print_stats()
    print(s.getvalue())

    return result

# Usage
def my_function():
    # ... code ...
    pass

profile_function(my_function)
```

### Flame Graphs

```bash
# Install flamegraph
npm install -g 0x

# Run with flamegraph
0x --output-dir profiles node server.js

# View flamegraph
# Open profiles/flamegraph.html in browser
```

---

## Bottleneck Identification

### Response Time Breakdown

```typescript
// Track each step of request processing
async function handleRequest(req, res) {
  const steps: Record<string, number> = {};

  const start = Date.now();

  // Authentication
  const authStart = Date.now();
  await authenticate(req);
  steps.authentication = Date.now() - authStart;

  // Authorization
  const authzStart = Date.now();
  await authorize(req);
  steps.authorization = Date.now() - authzStart;

  // Business logic
  const logicStart = Date.now();
  const result = await processRequest(req);
  steps.business_logic = Date.now() - logicStart;

  // Response
  steps.total = Date.now() - start;

  // Log breakdown
  logger.info('Request breakdown', steps);

  // Identify bottleneck
  const bottleneck = Object.entries(steps)
    .filter(([key]) => key !== 'total')
    .sort(([, a], [, b]) => b - a)[0];

  if (bottleneck[1] > steps.total * 0.5) {
    logger.warn('Bottleneck detected', {
      step: bottleneck[0],
      duration: bottleneck[1],
      percentage: (bottleneck[1] / steps.total * 100).toFixed(2),
    });
  }

  res.json(result);
}
```

### Database Bottleneck Detection

```typescript
// Track database time vs total time
async function handleRequest(req, res) {
  const totalStart = Date.now();
  let dbTime = 0;

  const dbQuery = async (sql: string, params: any[]) => {
    const start = Date.now();
    const result = await db.query(sql, params);
    dbTime += Date.now() - start;
    return result;
  };

  // Use dbQuery instead of db.query
  const users = await dbQuery('SELECT * FROM users', []);
  const posts = await dbQuery('SELECT * FROM posts', []);

  const totalTime = Date.now() - totalStart;
  const dbPercentage = (dbTime / totalTime) * 100;

  if (dbPercentage > 50) {
    logger.warn('Database bottleneck detected', {
      dbTime,
      totalTime,
      percentage: dbPercentage.toFixed(2),
    });
  }

  res.json({ users, posts });
}
```

### External API Bottleneck Detection

```typescript
async function callExternalAPI(url: string) {
  const start = Date.now();
  const response = await fetch(url);
  const duration = Date.now() - start;

  metrics.record('external_api_duration', duration, {
    url,
    status: response.status,
  });

  if (duration > 5000) {
    logger.warn('Slow external API call', {
      url,
      duration,
    });
  }

  return response;
}
```

---

## Performance Budgets

### Setting Performance Budgets

```typescript
interface PerformanceBudget {
  responseTime: number; // ms
  databaseTime: number; // ms
  externalAPICall: number; // ms
  memoryUsage: number; // MB
  cpuUsage: number; // percentage
}

const budgets: Record<string, PerformanceBudget> = {
  api: {
    responseTime: 200,
    databaseTime: 50,
    externalAPICall: 100,
    memoryUsage: 512,
    cpuUsage: 50,
  },
  worker: {
    responseTime: 5000,
    databaseTime: 1000,
    externalAPICall: 2000,
    memoryUsage: 1024,
    cpuUsage: 80,
  },
};

function checkBudget(operation: string, metric: keyof PerformanceBudget, value: number) {
  const budget = budgets[operation];
  if (!budget) return;

  if (value > budget[metric]) {
    logger.warn('Performance budget exceeded', {
      operation,
      metric,
      value,
      budget: budget[metric],
      exceedBy: value - budget[metric],
    });
  }
}

// Usage
async function handleAPIRequest(req, res) {
  const start = Date.now();

  try {
    const result = await processRequest(req);
    const duration = Date.now() - start;

    checkBudget('api', 'responseTime', duration);

    res.json(result);
  } catch (error) {
    const duration = Date.now() - start;
    checkBudget('api', 'responseTime', duration);
    throw error;
  }
}
```

### Web Vitals Budgets

```typescript
// Core Web Vitals
const webVitalsBudgets = {
  LCP: 2500, // Largest Contentful Paint
  FID: 100, // First Input Delay
  CLS: 0.1, // Cumulative Layout Shift
  FCP: 1800, // First Contentful Paint
  TTI: 3800, // Time to Interactive
};

function checkWebVitals(name: string, value: number) {
  const budget = webVitalsBudgets[name as keyof typeof webVitalsBudgets];
  if (!budget) return;

  if (value > budget) {
    logger.warn('Web vital budget exceeded', {
      metric: name,
      value,
      budget,
      exceedBy: value - budget,
    });
  }
}

// Usage with web-vitals library
import { getCLS, getFID, getFCP, getLCP, getTTI } from 'web-vitals';

getCLS((metric) => checkWebVitals('CLS', metric.value));
getFID((metric) => checkWebVitals('FID', metric.value));
getFCP((metric) => checkWebVitals('FCP', metric.value));
getLCP((metric) => checkWebVitals('LCP', metric.value));
getTTI((metric) => checkWebVitals('TTI', metric.value));
```

---

## Best Practices

### 1. Monitor Early and Often

```typescript
// Start monitoring from development
if (process.env.NODE_ENV === 'development') {
  const profiler = new Profiler();
  profiler.startProfiling();
}
```

### 2. Set Meaningful Alerts

```typescript
// Alert on degraded performance
if (averageResponseTime > 500) {
  alert('High response time detected');
}

if (errorRate > 0.01) {
  alert('High error rate detected');
}

if (memoryUsage > 90) {
  alert('High memory usage detected');
}
```

### 3. Track User Experience

```typescript
// Track user-facing metrics
import { onCLS, onFID, onLCP } from 'web-vitals';

onCLS((metric) => {
  metrics.record('web_vital', metric.value, {
    name: 'CLS',
    rating: metric.rating,
  });
});

onFID((metric) => {
  metrics.record('web_vital', metric.value, {
    name: 'FID',
    rating: metric.rating,
  });
});

onLCP((metric) => {
  metrics.record('web_vital', metric.value, {
    name: 'LCP',
    rating: metric.rating,
  });
});
```

### 4. Profile Regularly

```typescript
// Schedule regular profiling
setInterval(() => {
  takeHeapSnapshot();
}, 3600000); // Every hour

setInterval(() => {
  takeCPUProfile();
}, 86400000); // Every day
```

### 5. Analyze Trends

```typescript
// Track performance over time
const performanceHistory: Array<{ timestamp: number; metrics: any }> = [];

function recordPerformance(metrics: any) {
  performanceHistory.push({
    timestamp: Date.now(),
    metrics,
  });

  // Keep last 30 days
  const thirtyDaysAgo = Date.now() - 30 * 24 * 60 * 60 * 1000;
  while (performanceHistory[0]?.timestamp < thirtyDaysAgo) {
    performanceHistory.shift();
  }
}

// Analyze trends
function analyzeTrends() {
  const recent = performanceHistory.slice(-100);
  const older = performanceHistory.slice(-200, -100);

  const recentAvg = calculateAverage(recent.map(r => r.metrics.responseTime));
  const olderAvg = calculateAverage(older.map(o => o.metrics.responseTime));

  const trend = ((recentAvg - olderAvg) / olderAvg) * 100;

  logger.info('Performance trend', {
    recentAvg,
    olderAvg,
    trend: `${trend.toFixed(2)}%`,
  });

  if (trend > 10) {
    logger.warn('Performance degrading', { trend });
  }
}
```

### 6. Use Sampling in Production

```typescript
// Sample transactions to reduce overhead
const SAMPLE_RATE = 0.1; // 10%

async function handleRequest(req, res) {
  const shouldSample = Math.random() < SAMPLE_RATE;

  if (shouldSample) {
    const transaction = startTransaction('handleRequest');
    // ... process request ...
    transaction.finish();
  } else {
    // ... process request without tracing ...
  }
}
```

### 7. Correlate Metrics

```typescript
// Correlate errors with performance
const errorsByPerformance = {
  fast: 0,
  medium: 0,
  slow: 0,
};

function recordError(duration: number) {
  if (duration < 100) {
    errorsByPerformance.fast++;
  } else if (duration < 500) {
    errorsByPerformance.medium++;
  } else {
    errorsByPerformance.slow++;
  }
}

// Analyze correlation
function analyzeErrorCorrelation() {
  const total = errorsByPerformance.fast +
                errorsByPerformance.medium +
                errorsByPerformance.slow;

  logger.info('Error correlation', {
    fast: (errorsByPerformance.fast / total * 100).toFixed(2) + '%',
    medium: (errorsByPerformance.medium / total * 100).toFixed(2) + '%',
    slow: (errorsByPerformance.slow / total * 100).toFixed(2) + '%',
  });
}
```

---

## Resources

- [New Relic Documentation](https://docs.newrelic.com/)
- [DataDog APM Documentation](https://docs.datadoghq.com/tracing/)
- [Elastic APM Documentation](https://www.elastic.co/guide/en/apm/index.html)
- [Web Vitals](https://web.dev/vitals/)
- [Node.js Performance](https://nodejs.org/en/docs/guides/simple-profiling/)
