# Load Testing

A comprehensive guide to load testing patterns for applications.

## Table of Contents

1. [Load Testing Concepts](#load-testing-concepts)
2. [Tools](#tools)
3. [Test Scenarios](#test-scenarios)
4. [Metrics to Track](#metrics-to-track)
5. [Ramp-up Strategies](#ramp-up-strategies)
6. [Analyzing Results](#analyzing-results)
7. [Bottleneck Identification](#bottleneck-identification)
8. [CI/CD Integration](#cicd-integration)
9. [Production Testing](#production-testing)
10. [Best Practices](#best-practices)

---

## Load Testing Concepts

### What is Load Testing?

Load testing simulates real-world load on your application to identify performance bottlenecks.

```
┌─────────────────────────────────────────────────────────────┐
│                   Load Testing Flow                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│  │  Load    │──>│ System   │──>│  Metrics │              │
│  │ Generator│  │ Under    │  │  &      │              │
│  │          │  │  Test    │  │ Analysis │              │
│  └─────────┘  └─────────┘  └─────────┘              │
│                                                             │
│  Load Types:                                                │
│  - Load: Normal expected traffic                            │
│  - Stress: Beyond normal capacity                            │
│  - Spike: Sudden traffic surge                              │
│  - Endurance: Sustained load over time                        │
└─────────────────────────────────────────────────────────────┘
```

### Key Metrics

| Metric | Description |
|--------|-------------|
| **Requests Per Second (RPS)** | Number of requests handled per second |
| **Response Time** | Time to process a request |
| **Throughput** | Data transferred per second |
| **Error Rate** | Percentage of failed requests |
| **Concurrent Users** | Number of simultaneous users |
| **CPU Usage** | Server CPU utilization |
| **Memory Usage** | Server memory utilization |

---

## Tools

### K6

```bash
# Install K6
brew install k6  # macOS
# or
curl https://github.com/grafana/k6/releases/download/v0.47.0/k6-v0.47.0-linux-amd64.tar.gz -L | tar xvz
```

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },   // Ramp up to 10 users
    { duration: '1m', target: 10 },    // Stay at 10 users
    { duration: '20s', target: 0 },    // Ramp down to 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'], // < 1% error rate
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

```bash
# Run K6 test
k6 run load-test.js

# Run with output
k6 run load-test.js --out json=results.json

# Run with specific VUs
k6 run load-test.js --vus 100
```

### Artillery

```bash
# Install Artillery
npm install -g artillery
```

```yaml
# config.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 120
      arrivalRate: 50
      name: "Ramp up load"
    - duration: 60
      arrivalRate: 50
      name: "Sustained load"
    - duration: 60
      arrivalRate: 0
      name: "Ramp down"
  processor:
    - function: "randomString.js"

scenarios:
  - name: "Get Users"
    flow:
      - get:
          url: "/users"
          capture:
            - json: "$.id"
      - think: 1
```

```javascript
// randomString.js
module.exports = function(userContext, events, done) {
  const randomString = Math.random().toString(36).substring(7);
  userContext.vars.randomString = randomString;
  return done();
};
```

```bash
# Run Artillery test
artillery run config.yml

# Run with report
artillery run config.yml --output results.json
```

### Locust

```bash
# Install Locust
pip install locust
```

```python
# locustfile.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def index(self):
        self.client.get("/")

    @task(1)
    def about(self):
        self.client.get("/about")
```

```bash
# Run Locust
locust -f locustfile.py --host=https://example.com

# Run headless
locust -f locustfile.py --headless --users 100 --spawn-rate 10
```

### JMeter

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2">
  <hashTree>
    <TestPlan guiclass="TestPlan">
      <elementProp name="TestPlan.user_defined_variables">
        <collectionProp name="BASE_URL">
          <stringProp name="BASE_URL">https://api.example.com</stringProp>
        </collectionProp>
      </elementProp>
      <ThreadGroup guiclass="ThreadGroup">
        <stringProp name="ThreadGroup.num_threads">10</stringProp>
        <stringProp name="ThreadGroup.ramp_time">10</stringProp>
        <LoopController guiclass="LoopController">
          <stringProp name="LoopController.loops">100</stringProp>
        </LoopController>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui">
          <stringProp name="HTTPSampler.domain">${BASE_URL}</stringProp>
          <stringProp name="HTTPSampler.path">/users</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
        </HTTPSamplerProxy>
      </ThreadGroup>
    </TestPlan>
  </hashTree>
</jmeterTestPlan>
```

---

## Test Scenarios

### User Journey Scenario

```javascript
// k6
import http from 'k6/http';
import { check, sleep } from 'k6';

export default function () {
  // Login
  const loginRes = http.post('https://api.example.com/auth/login', JSON.stringify({
    email: 'user@example.com',
    password: 'password',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });

  check(loginRes, {
    'login successful': (r) => r.status === 200,
  });

  const token = loginRes.json('token');

  // Get users
  const usersRes = http.get('https://api.example.com/users', {
    headers: { 'Authorization': `Bearer ${token}` },
  });

  check(usersRes, {
    'users fetched': (r) => r.status === 200,
  });

  sleep(1);
}
```

### API Endpoint Scenario

```javascript
// k6
import http from 'k6/http';
import { check, group } from 'k6';

export default function () {
  group('Get Users', function () {
    const res = http.get('https://api.example.com/users');
    check(res, {
      'status is 200': (r) => r.status === 200,
      'has users': (r) => r.json('users.length') > 0,
    });
  });

  group('Create User', function () {
    const res = http.post('https://api.example.com/users', JSON.stringify({
      name: 'Test User',
      email: 'test@example.com',
    }), {
      headers: { 'Content-Type': 'application/json' },
    });
    check(res, {
      'user created': (r) => r.status === 201,
    });
  });
}
```

### Mixed Traffic Scenario

```javascript
// k6
import http from 'k6/http';
import { check, sleep, randomIntBetween } from 'k6';

export const options = {
  scenarios: {
    read_requests: {
      executor: 'constant-arrival-rate',
      rate: 100,
      timeUnit: '1s',
      duration: '5m',
      exec: 'readRequest',
    },
    write_requests: {
      executor: 'constant-arrival-rate',
      rate: 10,
      timeUnit: '1s',
      duration: '5m',
      exec: 'writeRequest',
    },
  },
};

export function readRequest() {
  const res = http.get('https://api.example.com/users');
  check(res, { 'status is 200': (r) => r.status === 200 });
}

export function writeRequest() {
  const res = http.post('https://api.example.com/users', JSON.stringify({
    name: `User ${randomIntBetween(1, 1000)}`,
    email: `user${randomIntBetween(1, 1000)}@example.com`,
  }), {
    headers: { 'Content-Type': 'application/json' },
  });
  check(res, { 'status is 201': (r) => r.status === 201 });
}
```

---

## Metrics to Track

### Response Time Metrics

```javascript
// k6
import http from 'k6/http';
import { check, Trend } from 'k6';

const responseTime = new Trend('response_time', true);

export default function () {
  const res = http.get('https://api.example.com/users');
  responseTime.add(res.timings.duration);

  check(res, {
    'p(95) < 500ms': (r) => r.timings.duration < 500,
    'p(99) < 1000ms': (r) => r.timings.duration < 1000,
  });
}
```

### Error Rate Metrics

```javascript
// k6
import http from 'k6/http';
import { Rate } from 'k6';

const errorRate = new Rate('errors');

export default function () {
  const res = http.get('https://api.example.com/users');
  errorRate.add(res.status !== 200);

  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}
```

### Throughput Metrics

```javascript
// k6
import http from 'k6/http';
import { Counter } from 'k6';

const requestCount = new Counter('requests');

export default function () {
  const res = http.get('https://api.example.com/users');
  requestCount.add(1);
}
```

---

## Ramp-up Strategies

### Linear Ramp-up

```javascript
// k6
export const options = {
  stages: [
    { duration: '5m', target: 100 },  // Ramp up to 100 users over 5 minutes
    { duration: '10m', target: 100 }, // Stay at 100 users for 10 minutes
    { duration: '5m', target: 0 },    // Ramp down to 0 over 5 minutes
  ],
};
```

### Step Ramp-up

```javascript
// k6
export const options = {
  stages: [
    { duration: '2m', target: 10 },
    { duration: '2m', target: 20 },
    { duration: '2m', target: 30 },
    { duration: '2m', target: 40 },
    { duration: '2m', target: 50 },
    { duration: '5m', target: 50 },
    { duration: '5m', target: 0 },
  ],
};
```

### Spike Test

```javascript
// k6
export const options = {
  stages: [
    { duration: '1m', target: 10 },
    { duration: '30s', target: 100 }, // Spike to 100 users
    { duration: '1m', target: 10 },  // Back to 10 users
    { duration: '2m', target: 0 },
  ],
};
```

### Stress Test

```javascript
// k6
export const options = {
  stages: [
    { duration: '5m', target: 100 },
    { duration: '10m', target: 200 }, // Beyond normal capacity
    { duration: '5m', target: 300 },
    { duration: '5m', target: 0 },
  ],
};
```

---

## Analyzing Results

### K6 Results

```bash
# Run K6 with output
k6 run load-test.js --out json=results.json

# Analyze results
k6 run load-test.js --out influxdb=http://localhost:8086/k6
```

```javascript
// Custom metrics
import { Trend, Rate, Counter, Gauge } from 'k6';

export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

const responseTime = new Trend('response_time', true);
const errorRate = new Rate('errors', true);
const requestCount = new Counter('requests', true);
const activeUsers = new Gauge('active_users', true);

export default function () {
  activeUsers.add(__VUS);
  const res = http.get('https://api.example.com/users');
  responseTime.add(res.timings.duration);
  errorRate.add(res.status !== 200);
  requestCount.add(1);
}
```

### Artillery Results

```yaml
# config.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 10
  plugins:
    ensure: {}
    metrics-by-endpoint:
      use: true
```

```bash
# Run with report
artillery run config.yml --output results.json

# Generate HTML report
artillery report results.json
```

### Locust Results

```python
# locustfile.py
from locust import events

def on_request(request_type, name, response_time, response_length, exception, **kwargs):
    events.request.fire(
        request_type=request_type,
        name=name,
        response_time=response_time,
        response_length=response_length,
        exception=exception
    )

events.request += on_request
```

```bash
# Run with HTML report
locust -f locustfile.py --host=https://example.com --html report.html
```

---

## Bottleneck Identification

### Database Bottleneck

```javascript
// k6
import http from 'k6/http';
import { Trend } from 'k6';

const dbQueryTime = new Trend('db_query_time', true);

export default function () {
  const start = new Date();
  const res = http.get('https://api.example.com/users');
  const duration = new Date() - start;

  dbQueryTime.add(duration);

  if (duration > 1000) {
    console.log(`Slow query: ${duration}ms`);
  }
}
```

### API Bottleneck

```javascript
// k6
import http from 'k6/http';
import { check } from 'k6';

export default function () {
  const res = http.get('https://api.example.com/users');

  check(res, {
    'response time < 500ms': (r) => r.timings.duration < 500,
    'response time < 1000ms': (r) => r.timings.duration < 1000,
    'response time < 2000ms': (r) => r.timings.duration < 2000,
  });

  if (res.timings.duration > 2000) {
    console.log(`Slow endpoint: ${res.url} - ${res.timings.duration}ms`);
  }
}
```

### Memory Bottleneck

```javascript
// k6
import { Gauge } from 'k6';

const memoryUsage = new Gauge('memory_usage', true);

export default function () {
  const res = http.get('https://api.example.com/metrics');
  const metrics = res.json();

  memoryUsage.add(metrics.memory.used);
}
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Load Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18

      - name: Install K6
        run: |
          curl https://github.com/grafana/k6/releases/download/v0.47.0/k6-v0.47.0-linux-amd64.tar.gz -L | tar xvz
          sudo mv k6 /usr/local/bin/

      - name: Run Load Tests
        run: k6 run load-test.js

      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: load-test-results
          path: results.json
```

### GitLab CI

```yaml
load-test:
  stage: test
  image:
    name: grafana/k6:latest
    entrypoint: [""]
  script:
    - k6 run load-test.js --out json=results.json
  artifacts:
    paths:
      - results.json
```

---

## Production Testing

### Safe Production Testing

```javascript
// k6 - Production safe
export const options = {
  stages: [
    { duration: '5m', target: 10 },   // Low load
    { duration: '10m', target: 20 }, // Medium load
    { duration: '5m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_failed: ['rate<0.01'], // Strict error rate
    http_req_duration: ['p(95)<1000'], // Strict response time
  },
};

export default function () {
  const res = http.get('https://api.example.com/health');
  check(res, {
    'status is 200': (r) => r.status === 200,
  });
}
```

### Canary Testing

```javascript
// k6 - Canary testing
export const options = {
  scenarios: {
    production: {
      executor: 'constant-arrival-rate',
      rate: 5,
      timeUnit: '1s',
      duration: '10m',
      exec: 'productionRequest',
    },
    canary: {
      executor: 'constant-arrival-rate',
      rate: 5,
      timeUnit: '1s',
      duration: '10m',
      exec: 'canaryRequest',
    },
  },
};

export function productionRequest() {
  http.get('https://api.example.com/users');
}

export function canaryRequest() {
  http.get('https://canary-api.example.com/users');
}
```

---

## Best Practices

### 1. Start Small

```javascript
// Start with low load
export const options = {
  stages: [
    { duration: '5m', target: 10 },
  ],
};
```

### 2. Gradually Increase Load

```javascript
// Gradual ramp-up
export const options = {
  stages: [
    { duration: '5m', target: 10 },
    { duration: '5m', target: 20 },
    { duration: '5m', target: 30 },
  ],
};
```

### 3. Monitor System Resources

```javascript
// Track CPU and memory
const cpuUsage = new Trend('cpu_usage', true);
const memoryUsage = new Trend('memory_usage', true);
```

### 4. Use Realistic Scenarios

```javascript
// Simulate real user behavior
export default function () {
  group('Login', () => {
    // Login logic
  });

  group('Browse', () => {
    // Browse logic
  });

  group('Checkout', () => {
    // Checkout logic
  });
}
```

### 5. Test During Off-Peak Hours

```bash
# Schedule tests during off-peak hours
# Use cron jobs or CI schedulers
```

### 6. Use Thresholds

```javascript
// Set performance thresholds
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};
```

### 7. Analyze Results

```bash
# Generate reports
k6 run load-test.js --out json=results.json
artillery run config.yml --output results.json
locust -f locustfile.py --html report.html
```

### 8. Test Error Handling

```javascript
// Test error scenarios
export default function () {
  const res = http.get('https://api.example.com/users/999');
  check(res, {
    'handles 404': (r) => r.status === 404,
  });
}
```

### 9. Test Caching

```javascript
// Test cache effectiveness
export default function () {
  const res1 = http.get('https://api.example.com/users');
  const res2 = http.get('https://api.example.com/users');

  check(res2, {
    'cached response': (r) => r.timings.duration < res1.timings.duration,
  });
}
```

### 10. Document Results

```javascript
// Document findings
console.log('Test completed');
console.log('Average response time: ${getAverageResponseTime()}');
console.log('Error rate: ${getErrorRate()}');
console.log('Bottlenecks: ${identifyBottlenecks()}');
```

---

## Resources

- [K6 Documentation](https://k6.io/docs/)
- [Artillery Documentation](https://artillery.io/docs/)
- [Locust Documentation](https://docs.locust.io/)
- [JMeter Documentation](https://jmeter.apache.org/usermanual/index.html)
