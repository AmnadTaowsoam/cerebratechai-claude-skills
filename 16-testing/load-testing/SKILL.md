# Load Testing

## Overview

Load testing evaluates system performance under expected and peak load conditions. This skill covers load testing concepts, tools, test scenarios, metrics, ramp-up strategies, and best practices.

## Table of Contents

1. [Load Testing Concepts](#load-testing-concepts)
2. [Tools](#tools)
   - [k6](#k6)
   - [Artillery](#artillery)
   - [Locust](#locust)
   - [JMeter](#jmeter)
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

### Why Load Testing?

1. **Verify system capacity**
2. **Identify performance bottlenecks**
3. **Ensure scalability**
4. **Validate SLA compliance**
5. **Prevent production failures**

### Load Testing Types

| Type | Purpose | Duration |
|------|---------|----------|
| **Smoke Test** | Basic functionality | Short (5-10 min) |
| **Load Test** | Normal traffic patterns | Medium (30-60 min) |
| **Stress Test** | Find breaking point | Variable |
| **Spike Test** | Sudden traffic surge | Short (5-10 min) |
| **Endurance Test** | Long-term stability | Long (several hours/days) |

### Key Concepts

- **Virtual Users (VUs)**: Simulated users
- **Requests Per Second (RPS)**: Request rate
- **Throughput**: Successful requests per time unit
- **Response Time**: Time to receive response
- **Latency**: Network delay
- **Error Rate**: Percentage of failed requests

---

## Tools

### k6

#### Installation

```bash
# macOS
brew install k6

# Linux
sudo gpg -k
sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
sudo apt-get update
sudo apt-get install k6

# Windows
choco install k6

# Or via npm
npm install -g k6
```

#### Basic Test Script

```javascript
// load-tests/basic.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 100 },  // Ramp up to 100 users
    { duration: '1m', target: 100 },   // Stay at 100 users
    { duration: '20s', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests must be under 500ms
    http_req_failed: ['rate<0.01'],   // Error rate must be less than 1%
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1); // Pause between iterations
}
```

#### Advanced Test Script

```javascript
// load-tests/advanced.js
import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { Rate, Trend } from 'k6/metrics';

const errorRate = new Rate('errors');
const responseTime = new Trend('response_time');

export const options = {
  stages: [
    { duration: '2m', target: 100 },   // Ramp up to 100 users
    { duration: '5m', target: 100 },    // Stay at 100 users
    { duration: '2m', target: 200 },   // Ramp up to 200 users
    { duration: '5m', target: 200 },   // Stay at 200 users
    { duration: '2m', target: 0 },     // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
    errors: ['rate<0.01'],
  },
};

export function setup() {
  // Setup: Create test data
  const loginRes = http.post('https://api.example.com/auth/login', JSON.stringify({
    email: 'test@example.com',
    password: 'password123',
  }), {
    headers: { 'Content-Type': 'application/json' },
  });
  
  return { token: loginRes.json('token') };
}

export default function (data) {
  group('User Flow', () => {
    // Get users
    const usersRes = http.get('https://api.example.com/users', {
      headers: { Authorization: `Bearer ${data.token}` },
    });
    
    const usersOk = check(usersRes, {
      'users status is 200': (r) => r.status === 200,
      'users has data': (r) => r.json().length > 0,
    });
    
    errorRate.add(!usersOk);
    responseTime.add(usersRes.timings.duration);
    
    sleep(1);
    
    // Get user details
    if (usersRes.json().length > 0) {
      const userId = usersRes.json()[0].id;
      const userRes = http.get(`https://api.example.com/users/${userId}`, {
        headers: { Authorization: `Bearer ${data.token}` },
      });
      
      const userOk = check(userRes, {
        'user status is 200': (r) => r.status === 200,
        'user has correct id': (r) => r.json().id === userId,
      });
      
      errorRate.add(!userOk);
      responseTime.add(userRes.timings.duration);
    }
  });
}

export function teardown(data) {
  // Teardown: Clean up test data
  console.log('Cleaning up test data...');
}
```

#### Running k6 Tests

```bash
# Run basic test
k6 run load-tests/basic.js

# Run with output
k6 run --out json=results.json load-tests/basic.js

# Run with custom options
k6 run --vus 50 --duration 30s load-tests/basic.js

# Run with environment variables
k6 run -e BASE_URL=https://api.example.com load-tests/basic.js
```

---

### Artillery

#### Installation

```bash
npm install -g artillery
```

#### Basic Configuration

```yaml
# load-tests/basic.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 120
      arrivalRate: 50
      name: "Ramp up to 50 users"
    - duration: 60
      arrivalRate: 100
      name: "Spike to 100 users"
    - duration: 60
      arrivalRate: 10
      name: "Cool down"
  defaults:
    headers:
      Content-Type: "application/json"
  processor: "./load-tests/functions.js"

scenarios:
  - name: "User Flow"
    flow:
      - get:
          url: "/users"
          name: "Get Users"
      - think: 1
      - post:
          url: "/users"
          name: "Create User"
          json:
            name: "Test User"
            email: "test@example.com"
      - think: 1
```

#### Advanced Configuration

```yaml
# load-tests/advanced.yml
config:
  target: "https://api.example.com"
  phases:
    - duration: 60
      arrivalRate: 10
      name: "Warm up"
    - duration: 300
      arrivalRate: 50
      name: "Sustained load"
    - duration: 60
      arrivalRate: 100
      name: "Spike test"
    - duration: 60
      arrivalRate: 10
      name: "Cool down"
  defaults:
    headers:
      Content-Type: "application/json"
      Authorization: "Bearer {{ $processEnvironment.TOKEN }}"
  processor: "./load-tests/functions.js"
  ensure:
    p95: 500
    maxErrorRate: 1

scenarios:
  - name: "User Flow"
    weight: 70
    flow:
      - get:
          url: "/users"
          name: "Get Users"
          capture:
            - json: "$[0].id"
              as: "userId"
      - think: 1
      - get:
          url: "/users/{{ userId }}"
          name: "Get User Details"
      - think: 1
      - post:
          url: "/orders"
          name: "Create Order"
          json:
            userId: "{{ userId }}"
            items:
              - productId: 1
                quantity: 2
      - think: 1

  - name: "Search Flow"
    weight: 30
    flow:
      - get:
          url: "/products/search?q={{ $randomString() }}"
          name: "Search Products"
      - think: 1
```

#### Processor Functions

```javascript
// load-tests/functions.js
module.exports = {
  // Generate random email
  randomEmail() {
    const domains = ['gmail.com', 'yahoo.com', 'outlook.com'];
    const domain = domains[Math.floor(Math.random() * domains.length)];
    const random = Math.floor(Math.random() * 10000);
    return `user${random}@${domain}`;
  },

  // Generate random string
  randomString(length = 10) {
    const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let result = '';
    for (let i = 0; i < length; i++) {
      result += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    return result;
  },

  // Generate random number
  randomNumber(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  },

  // Setup function
  setup(config, events, done) {
    console.log('Setting up load test...');
    done();
  },

  // Teardown function
  teardown(context, events, done) {
    console.log('Tearing down load test...');
    done();
  },
};
```

#### Running Artillery Tests

```bash
# Run basic test
artillery run load-tests/basic.yml

# Run with output
artillery run --output results.json load-tests/basic.yml

# Run with environment variables
TOKEN=your_token artillery run load-tests/advanced.yml

# Run with custom config
artillery run --config custom.yml load-tests/basic.yml
```

---

### Locust

#### Installation

```bash
pip install locust
```

#### Basic Test Script

```python
# load-tests/basic.py
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def get_users(self):
        self.client.get("/users")
    
    @task(3)
    def get_products(self):
        self.client.get("/products")
```

#### Advanced Test Script

```python
# load-tests/advanced.py
from locust import HttpUser, task, between, events
from locust.runners import MasterRunner
import random

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        """Login on start."""
        response = self.client.post("/auth/login", json={
            "email": "test@example.com",
            "password": "password123"
        })
        self.token = response.json()["token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(2)
    def get_users(self):
        """Get users list."""
        self.client.get("/users", headers=self.headers)
    
    @task
    def get_user_details(self):
        """Get user details."""
        users = self.client.get("/users", headers=self.headers).json()
        if users:
            user_id = random.choice(users)["id"]
            self.client.get(f"/users/{user_id}", headers=self.headers)
    
    @task(3)
    def search_products(self):
        """Search products."""
        query = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=5))
        self.client.get(f"/products/search?q={query}")
    
    @task
    def create_order(self):
        """Create order."""
        users = self.client.get("/users", headers=self.headers).json()
        if users:
            user_id = random.choice(users)["id"]
            self.client.post("/orders", headers=self.headers, json={
                "userId": user_id,
                "items": [
                    {"productId": 1, "quantity": 2},
                    {"productId": 2, "quantity": 1}
                ]
            })

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when test starts."""
    print("Starting load test...")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when test stops."""
    print("Load test completed.")
    if isinstance(environment.runner, MasterRunner):
        print(f"Total requests: {environment.runner.stats.total.num_requests}")
        print(f"Failures: {environment.runner.stats.total.num_failures}")
```

#### Running Locust Tests

```bash
# Run Locust web UI
locust -f load-tests/basic.py

# Run Locust headless
locust -f load-tests/basic.py --headless -u 100 -r 10 -t 1m

# Run with custom host
locust -f load-tests/basic.py --host https://api.example.com

# Run with environment variables
API_URL=https://api.example.com locust -f load-tests/basic.py
```

---

### JMeter

#### Installation

```bash
# Download from https://jmeter.apache.org/download_jmeter.cgi
# Or use Homebrew
brew install jmeter

# Or use Chocolatey
choco install jmeter
```

#### Basic Test Plan

```xml
<?xml version="1.0" encoding="UTF-8"?>
<jmeterTestPlan version="1.2" properties="5.0">
  <hashTree>
    <TestPlan guiclass="TestPlanGui" testclass="TestPlan">
      <stringProp name="TestPlan.comments">Basic Load Test</stringProp>
      <stringProp name="TestPlan.user_define_classpath"></stringProp>
      <boolProp name="TestPlan.functional_mode">false</boolProp>
      <boolProp name="TestPlan.serialize_threadgroups">false</boolProp>
      <elementProp name="TestPlan.user_defined_variables" elementType="Arguments">
        <collectionProp name="Arguments.arguments">
          <elementProp name="BASE_URL" elementType="Argument">
            <stringProp name="Argument.name">BASE_URL</stringProp>
            <stringProp name="Argument.value">https://api.example.com</stringProp>
          </elementProp>
        </collectionProp>
      </elementProp>
    </TestPlan>
    <hashTree>
      <ThreadGroup guiclass="ThreadGroupGui" testclass="ThreadGroup">
        <stringProp name="ThreadGroup.num_threads">100</stringProp>
        <stringProp name="ThreadGroup.ramp_time">10</stringProp>
        <stringProp name="ThreadGroup.duration">60</stringProp>
        <boolProp name="ThreadGroup.scheduler">true</boolProp>
      </ThreadGroup>
      <hashTree>
        <HTTPSamplerProxy guiclass="HttpTestSampleGui" testclass="HTTPSamplerProxy">
          <stringProp name="HTTPSampler.domain">${BASE_URL}</stringProp>
          <stringProp name="HTTPSampler.path">/users</stringProp>
          <stringProp name="HTTPSampler.method">GET</stringProp>
        </HTTPSamplerProxy>
        <hashTree/>
      </hashTree>
    </hashTree>
  </hashTree>
</jmeterTestPlan>
```

#### Running JMeter Tests

```bash
# Run JMeter GUI
jmeter

# Run JMeter in non-GUI mode
jmeter -n -t load-tests/basic.jmx -l results.jtl

# Run with output file
jmeter -n -t load-tests/basic.jmx -l results.jtl -e -o report

# Run with properties
jmeter -n -t load-tests/basic.jmx -Jusers=100 -Jduration=60
```

---

## Test Scenarios

### Smoke Test

```javascript
// k6 smoke test
export const options = {
  stages: [
    { duration: '30s', target: 10 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.05'],
  },
};
```

### Load Test

```javascript
// k6 load test
export const options = {
  stages: [
    { duration: '2m', target: 50 },
    { duration: '5m', target: 50 },
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};
```

### Stress Test

```javascript
// k6 stress test
export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '2m', target: 200 },
    { duration: '5m', target: 200 },
    { duration: '2m', target: 400 },
    { duration: '5m', target: 400 },
    { duration: '2m', target: 800 },
    { duration: '5m', target: 800 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<1000'],
    http_req_failed: ['rate<0.05'],
  },
};
```

### Spike Test

```javascript
// k6 spike test
export const options = {
  stages: [
    { duration: '2m', target: 100 },
    { duration: '5m', target: 100 },
    { duration: '1m', target: 1000 }, // Spike
    { duration: '5m', target: 1000 },
    { duration: '1m', target: 100 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<2000'],
    http_req_failed: ['rate<0.1'],
  },
};
```

### Endurance Test

```javascript
// k6 endurance test
export const options = {
  stages: [
    { duration: '10m', target: 100 },
    { duration: '4h', target: 100 },
    { duration: '10m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};
```

---

## Metrics to Track

### Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| **Response Time** | Time to complete request | < 500ms (p95) |
| **Throughput** | Requests per second | > 100 RPS |
| **Error Rate** | Percentage of failed requests | < 1% |
| **Latency** | Network delay | < 100ms |
| **CPU Usage** | Server CPU utilization | < 70% |
| **Memory Usage** | Server memory utilization | < 80% |
| **Database Connections** | Active database connections | < 80% of pool |

### Custom Metrics (k6)

```javascript
import { Counter, Rate, Trend } from 'k6/metrics';

export const metrics = {
  // Counter: Count occurrences
  requests: new Counter('requests'),
  
  // Rate: Percentage of values
  errors: new Rate('errors'),
  
  // Trend: Statistical distribution
  responseTime: new Trend('response_time'),
};

export default function () {
  const res = http.get('https://api.example.com/users');
  
  metrics.requests.add(1);
  metrics.errors.add(res.status !== 200);
  metrics.responseTime.add(res.timings.duration);
}
```

---

## Ramp-up Strategies

### Linear Ramp-up

```javascript
// Linear ramp-up
export const options = {
  stages: [
    { duration: '10m', target: 100 }, // 10 users per minute
  ],
};
```

### Step Ramp-up

```javascript
// Step ramp-up
export const options = {
  stages: [
    { duration: '5m', target: 25 },
    { duration: '5m', target: 50 },
    { duration: '5m', target: 75 },
    { duration: '5m', target: 100 },
  ],
};
```

### Exponential Ramp-up

```javascript
// Exponential ramp-up
export const options = {
  stages: [
    { duration: '2m', target: 10 },
    { duration: '2m', target: 20 },
    { duration: '2m', target: 40 },
    { duration: '2m', target: 80 },
    { duration: '2m', target: 160 },
  ],
};
```

### Spike Ramp-up

```javascript
// Spike ramp-up
export const options = {
  stages: [
    { duration: '5m', target: 100 },
    { duration: '1m', target: 1000 }, // Spike
    { duration: '5m', target: 1000 },
    { duration: '1m', target: 100 },
  ],
};
```

---

## Analyzing Results

### k6 Results

```bash
# Run with JSON output
k6 run --out json=results.json load-tests/basic.js

# Analyze results
# Check response time percentiles
# Check error rates
# Check throughput
```

### Artillery Results

```bash
# Run with output
artillery run --output results.json load-tests/basic.yml

# Generate HTML report
artillery report results.json

# Analyze results
# Check p95, p99 response times
# Check error rates
# Check RPS
```

### Locust Results

```bash
# Run Locust with output
locust -f load-tests/basic.py --headless -u 100 -r 10 -t 1m --csv results

# Analyze results
# Check response times
# Check failure rates
# Check RPS
```

---

## Bottleneck Identification

### Database Bottlenecks

```javascript
// Identify slow database queries
export default function () {
  const start = Date.now();
  
  const res = http.get('https://api.example.com/users');
  
  const duration = Date.now() - start;
  
  if (duration > 1000) {
    console.log(`Slow request: ${duration}ms`);
  }
}
```

### API Bottlenecks

```javascript
// Identify slow API endpoints
export default function () {
  const endpoints = [
    '/users',
    '/products',
    '/orders',
  ];
  
  endpoints.forEach(endpoint => {
    const res = http.get(`https://api.example.com${endpoint}`);
    
    if (res.timings.duration > 500) {
      console.log(`Slow endpoint: ${endpoint} - ${res.timings.duration}ms`);
    }
  });
}
```

### Network Bottlenecks

```javascript
// Identify network latency
export default function () {
  const res = http.get('https://api.example.com/users');
  
  const latency = res.timings.waiting;
  const processing = res.timings.duration - latency;
  
  console.log(`Latency: ${latency}ms, Processing: ${processing}ms`);
}
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/load-test.yml
name: Load Tests

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 * * 0' # Weekly

jobs:
  load-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install k6
        run: |
          sudo gpg -k
          sudo gpg --no-default-keyring --keyring /usr/share/keyrings/k6-archive-keyring.gpg --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
          echo "deb [signed-by=/usr/share/keyrings/k6-archive-keyring.gpg] https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update
          sudo apt-get install k6

      - name: Run load tests
        run: k6 run load-tests/basic.js

      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: load-test-results
          path: results.json
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  - load-test

load-test:
  stage: load-test
  image:
    name: loadimpact/k6:latest
    entrypoint: ['']
  script:
    - k6 run load-tests/basic.js
  artifacts:
    when: always
    paths:
      - results.json
    expire_in: 1 week
  only:
    - main
    - merge_requests
```

---

## Production Testing

### Canary Testing

```javascript
// Test canary deployment
export const options = {
  stages: [
    { duration: '5m', target: 10 }, // Small load on canary
  ],
  scenarios: {
    canary: {
      executor: 'constant-vus',
      vus: 10,
      duration: '5m',
      exec: 'canary',
    },
  },
};

export function canary() {
  const res = http.get('https://canary.example.com/api/users');
  check(res, { 'status is 200': (r) => r.status === 200 });
}
```

### Blue-Green Testing

```javascript
// Test blue-green deployment
export const options = {
  scenarios: {
    blue: {
      executor: 'constant-vus',
      vus: 50,
      duration: '5m',
      exec: 'blue',
    },
    green: {
      executor: 'constant-vus',
      vus: 50,
      duration: '5m',
      exec: 'green',
    },
  },
};

export function blue() {
  const res = http.get('https://blue.example.com/api/users');
  check(res, { 'status is 200': (r) => r.status === 200 });
}

export function green() {
  const res = http.get('https://green.example.com/api/users');
  check(res, { 'status is 200': (r) => r.status === 200 });
}
```

---

## Best Practices

### 1. Start Small

```javascript
// Good: Start with small load
export const options = {
  stages: [
    { duration: '30s', target: 10 },
  ],
};

// Bad: Start with maximum load
export const options = {
  stages: [
    { duration: '1m', target: 1000 },
  ],
};
```

### 2. Use Realistic Scenarios

```javascript
// Good: Realistic user flow
export default function () {
  group('User Flow', () => {
    const res = http.get('/users');
    const userId = res.json()[0].id;
    http.get(`/users/${userId}`);
  });
}

// Bad: Unrelated requests
export default function () {
  http.get('/users');
  http.get('/products');
  http.get('/orders');
}
```

### 3. Monitor System Resources

```javascript
// Good: Monitor resources
export default function () {
  const res = http.get('/users');
  
  // Log response time
  console.log(`Response time: ${res.timings.duration}ms`);
  
  // Check for errors
  if (res.status !== 200) {
    console.log(`Error: ${res.status}`);
  }
}

// Bad: No monitoring
export default function () {
  http.get('/users');
}
```

### 4. Use Thresholds

```javascript
// Good: Define thresholds
export const options = {
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

// Bad: No thresholds
export const options = {
  stages: [
    { duration: '5m', target: 100 },
  ],
};
```

### 5. Test in Staging First

```javascript
// Good: Test in staging
const BASE_URL = __ENV.BASE_URL || 'https://staging.example.com';

export default function () {
  http.get(`${BASE_URL}/users`);
}

// Bad: Test in production directly
export default function () {
  http.get('https://production.example.com/users');
}
```

---

## Summary

This skill covers comprehensive load testing patterns including:

- **Load Testing Concepts**: Why load testing, types, key concepts
- **Tools**: k6, Artillery, Locust, JMeter with installation and usage
- **Test Scenarios**: Smoke, load, stress, spike, endurance tests
- **Metrics to Track**: Response time, throughput, error rate, latency, CPU, memory
- **Ramp-up Strategies**: Linear, step, exponential, spike ramp-up
- **Analyzing Results**: k6, Artillery, Locust result analysis
- **Bottleneck Identification**: Database, API, network bottlenecks
- **CI/CD Integration**: GitHub Actions, GitLab CI configurations
- **Production Testing**: Canary, blue-green testing
- **Best Practices**: Start small, realistic scenarios, monitoring, thresholds, staging first
