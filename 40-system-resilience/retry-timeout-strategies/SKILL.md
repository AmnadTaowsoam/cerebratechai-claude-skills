---
name: Retry, Timeout & Backoff Strategies
description: Comprehensive guide to implementing robust retry logic, timeout handling, and backoff algorithms for resilient distributed systems
---

# Retry, Timeout & Backoff Strategies

## Overview

In distributed systems, transient failures are inevitable. Proper retry, timeout, and backoff strategies are essential for building resilient applications that gracefully handle temporary failures without overwhelming downstream services.

## 1. Why Retries and Timeouts Matter

### The Problem

```
Without retries:
User Request → Service A → [Network Glitch] → X Failed
Result: User sees error for a transient issue

Without timeouts:
User Request → Service A → Service B (hung) → ∞ Waiting forever
Result: Resources exhausted, cascading failures
```

### The Solution

```
With retries + timeouts:
User Request → Service A → [Timeout 5s] → Retry → Success
Result: User doesn't notice transient failure

With circuit breaker:
User Request → Service A → [Circuit Open] → Fallback
Result: Fast failure, no resource exhaustion
```

### Key Principles

1. **Fail Fast**: Don't wait indefinitely
2. **Retry Smart**: Not all failures should be retried
3. **Back Off**: Give systems time to recover
4. **Limit Retries**: Prevent retry storms
5. **Be Idempotent**: Retries shouldn't cause duplicate side effects

## 2. Timeout Strategies

### 2.1 Connection Timeouts

**Definition**: Maximum time to establish a connection.

```typescript
// Node.js with axios
import axios from 'axios';

const client = axios.create({
  timeout: 5000, // Total request timeout
  // For more control:
  httpAgent: new http.Agent({
    timeout: 3000, // Connection timeout
  })
});

// Fetch API
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 3000);

try {
  const response = await fetch('https://api.example.com/data', {
    signal: controller.signal
  });
} catch (error) {
  if (error.name === 'AbortError') {
    console.error('Connection timeout');
  }
} finally {
  clearTimeout(timeoutId);
}
```

```python
# Python with requests
import requests

try:
    response = requests.get(
        'https://api.example.com/data',
        timeout=(3, 10)  # (connect timeout, read timeout)
    )
except requests.exceptions.ConnectTimeout:
    print("Connection timeout")
except requests.exceptions.ReadTimeout:
    print("Read timeout")
```

```go
// Go
package main

import (
    "context"
    "net/http"
    "time"
)

func makeRequest() error {
    client := &http.Client{
        Timeout: 5 * time.Second,
        Transport: &http.Transport{
            DialContext: (&net.Dialer{
                Timeout: 3 * time.Second, // Connection timeout
            }).DialContext,
            ResponseHeaderTimeout: 5 * time.Second,
        },
    }

    resp, err := client.Get("https://api.example.com/data")
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    return nil
}
```

### 2.2 Read/Write Timeouts

**Definition**: Maximum time to read response or write request.

```typescript
// Node.js with socket timeouts
import * as http from 'http';

const options = {
  hostname: 'api.example.com',
  port: 80,
  path: '/data',
  method: 'GET',
  timeout: 10000 // Socket timeout
};

const req = http.request(options, (res) => {
  res.setTimeout(10000); // Read timeout
  res.on('data', (chunk) => {
    // Process data
  });
});

req.on('timeout', () => {
  req.destroy();
  console.error('Request timeout');
});
```

### 2.3 Idle Timeouts

**Definition**: Maximum time a connection can be idle.

```typescript
// Express.js server with idle timeout
import express from 'express';

const app = express();
const server = app.listen(3000);

// Set idle timeout to 60 seconds
server.keepAliveTimeout = 60000;
server.headersTimeout = 65000; // Should be > keepAliveTimeout
```

### 2.4 Request Timeouts

**Definition**: Maximum total time for entire request/response cycle.

```typescript
// End-to-end request timeout
async function makeRequestWithTimeout<T>(
  fn: () => Promise<T>,
  timeoutMs: number
): Promise<T> {
  return Promise.race([
    fn(),
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error('Request timeout')), timeoutMs)
    )
  ]);
}

// Usage
try {
  const data = await makeRequestWithTimeout(
    () => fetch('https://api.example.com/data').then(r => r.json()),
    5000
  );
} catch (error) {
  console.error('Request timed out after 5 seconds');
}
```

### 2.5 Timeout Calculation (p99 Latency + Buffer)

```typescript
// Calculate appropriate timeout based on latency percentiles
interface LatencyStats {
  p50: number;
  p95: number;
  p99: number;
  p999: number;
}

function calculateTimeout(stats: LatencyStats, bufferMultiplier: number = 1.5): number {
  // Use p99 latency + 50% buffer
  return Math.ceil(stats.p99 * bufferMultiplier);
}

// Example
const apiLatency: LatencyStats = {
  p50: 100,   // 100ms
  p95: 250,   // 250ms
  p99: 500,   // 500ms
  p999: 1000  // 1000ms
};

const timeout = calculateTimeout(apiLatency); // 750ms
```

### Timeout Best Practices

```
1. Connection timeout: 3-5 seconds
   (Enough for DNS + TCP handshake)

2. Read timeout: Based on p99 latency + buffer
   (Example: p99=200ms → timeout=300ms)

3. Total timeout: Sum of all operations + buffer
   (Example: DB query + API call + processing)

4. Idle timeout: 60-120 seconds
   (Balance between connection reuse and resource usage)

5. Always set timeouts
   (Never rely on defaults or infinite timeouts)
```

## 3. Retry Strategies

### 3.1 When to Retry (Idempotent Operations)

```typescript
// Safe to retry (idempotent)
✓ GET requests
✓ PUT requests (with same data)
✓ DELETE requests (with idempotency key)
✓ Read operations
✓ Queries with same parameters

// Unsafe to retry (non-idempotent)
✗ POST requests (without idempotency key)
✗ Payment processing
✗ Email sending
✗ Incrementing counters
✗ Appending to logs
```

### 3.2 When NOT to Retry

```typescript
// HTTP status codes that should NOT be retried
const NON_RETRYABLE_STATUS_CODES = [
  400, // Bad Request - client error, won't succeed on retry
  401, // Unauthorized - need new credentials
  403, // Forbidden - permission issue
  404, // Not Found - resource doesn't exist
  405, // Method Not Allowed
  409, // Conflict - business logic error
  422, // Unprocessable Entity - validation error
];

// Retryable status codes
const RETRYABLE_STATUS_CODES = [
  408, // Request Timeout
  429, // Too Many Requests
  500, // Internal Server Error
  502, // Bad Gateway
  503, // Service Unavailable
  504, // Gateway Timeout
];

function shouldRetry(statusCode: number): boolean {
  return RETRYABLE_STATUS_CODES.includes(statusCode);
}
```

```typescript
// Error-based retry logic
function shouldRetryError(error: Error): boolean {
  // Network errors - retry
  if (error.code === 'ECONNREFUSED') return true;
  if (error.code === 'ETIMEDOUT') return true;
  if (error.code === 'ENOTFOUND') return false; // DNS error - don't retry

  // HTTP errors - check status code
  if (error.response) {
    return shouldRetry(error.response.status);
  }

  // Unknown errors - don't retry
  return false;
}
```

### 3.3 Max Retry Attempts

```typescript
// Simple retry with max attempts
async function retryWithMaxAttempts<T>(
  fn: () => Promise<T>,
  maxAttempts: number = 3
): Promise<T> {
  let lastError: Error;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      console.log(`Attempt ${attempt}/${maxAttempts} failed:`, error.message);

      if (attempt === maxAttempts) {
        throw lastError;
      }

      if (!shouldRetryError(error)) {
        throw error; // Don't retry non-retryable errors
      }
    }
  }

  throw lastError!;
}

// Usage
const data = await retryWithMaxAttempts(
  () => fetch('https://api.example.com/data').then(r => r.json()),
  3
);
```

### 3.4 Retry Budget (SRE Concept)

```typescript
// Retry budget: Limit retries to prevent amplification
class RetryBudget {
  private requests = 0;
  private retries = 0;
  private windowMs = 60000; // 1 minute
  private maxRetryRatio = 0.1; // 10% retry budget

  canRetry(): boolean {
    const retryRatio = this.retries / Math.max(this.requests, 1);
    return retryRatio < this.maxRetryRatio;
  }

  recordRequest() {
    this.requests++;
  }

  recordRetry() {
    this.retries++;
  }

  // Reset counters periodically
  reset() {
    this.requests = 0;
    this.retries = 0;
  }
}

// Usage
const budget = new RetryBudget();
setInterval(() => budget.reset(), 60000);

async function makeRequestWithBudget<T>(fn: () => Promise<T>): Promise<T> {
  budget.recordRequest();

  try {
    return await fn();
  } catch (error) {
    if (shouldRetryError(error) && budget.canRetry()) {
      budget.recordRetry();
      return await fn(); // Retry
    }
    throw error;
  }
}
```

## 4. Backoff Algorithms

### 4.1 Linear Backoff

```typescript
// Linear backoff: delay = attempt * baseDelay
function linearBackoff(attempt: number, baseDelay: number = 1000): number {
  return attempt * baseDelay;
}

// Example: 1s, 2s, 3s, 4s, 5s
for (let i = 1; i <= 5; i++) {
  console.log(`Attempt ${i}: ${linearBackoff(i)}ms`);
}
```

### 4.2 Exponential Backoff

```typescript
// Exponential backoff: delay = baseDelay * 2^attempt
function exponentialBackoff(
  attempt: number,
  baseDelay: number = 1000,
  maxDelay: number = 60000
): number {
  const delay = baseDelay * Math.pow(2, attempt - 1);
  return Math.min(delay, maxDelay);
}

// Example: 1s, 2s, 4s, 8s, 16s, 32s, 60s (capped)
for (let i = 1; i <= 7; i++) {
  console.log(`Attempt ${i}: ${exponentialBackoff(i)}ms`);
}
```

### 4.3 Exponential Backoff with Jitter (AWS Recommendation)

```typescript
// Full jitter: delay = random(0, exponentialDelay)
function exponentialBackoffWithFullJitter(
  attempt: number,
  baseDelay: number = 1000,
  maxDelay: number = 60000
): number {
  const exponentialDelay = baseDelay * Math.pow(2, attempt - 1);
  const cappedDelay = Math.min(exponentialDelay, maxDelay);
  return Math.random() * cappedDelay;
}

// Decorrelated jitter: delay = random(baseDelay, previousDelay * 3)
function exponentialBackoffWithDecorrelatedJitter(
  attempt: number,
  previousDelay: number,
  baseDelay: number = 1000,
  maxDelay: number = 60000
): number {
  const delay = Math.random() * (previousDelay * 3 - baseDelay) + baseDelay;
  return Math.min(delay, maxDelay);
}

// Equal jitter: delay = exponentialDelay/2 + random(0, exponentialDelay/2)
function exponentialBackoffWithEqualJitter(
  attempt: number,
  baseDelay: number = 1000,
  maxDelay: number = 60000
): number {
  const exponentialDelay = baseDelay * Math.pow(2, attempt - 1);
  const cappedDelay = Math.min(exponentialDelay, maxDelay);
  const half = cappedDelay / 2;
  return half + Math.random() * half;
}
```

**Why Jitter?**
```
Without jitter (thundering herd):
Service fails → 1000 clients retry at same time → Service overwhelmed

With jitter:
Service fails → 1000 clients retry at different times → Gradual recovery
```

### 4.4 Fibonacci Backoff

```typescript
// Fibonacci backoff: delay = fibonacci(attempt) * baseDelay
function fibonacciBackoff(
  attempt: number,
  baseDelay: number = 1000,
  maxDelay: number = 60000
): number {
  const fib = (n: number): number => {
    if (n <= 1) return n;
    return fib(n - 1) + fib(n - 2);
  };

  const delay = fib(attempt) * baseDelay;
  return Math.min(delay, maxDelay);
}

// Example: 1s, 1s, 2s, 3s, 5s, 8s, 13s, 21s
for (let i = 1; i <= 8; i++) {
  console.log(`Attempt ${i}: ${fibonacciBackoff(i)}ms`);
}
```

### Backoff Comparison

```
Attempt | Linear | Exponential | Exp+Jitter | Fibonacci
--------|--------|-------------|------------|----------
1       | 1s     | 1s          | 0-1s       | 1s
2       | 2s     | 2s          | 0-2s       | 1s
3       | 3s     | 4s          | 0-4s       | 2s
4       | 4s     | 8s          | 0-8s       | 3s
5       | 5s     | 16s         | 0-16s      | 5s
6       | 6s     | 32s         | 0-32s      | 8s

Recommendation: Exponential with jitter (AWS best practice)
```

## 5. Circuit Breaker Pattern

### 5.1 States

```
CLOSED (Normal operation)
  ↓ (Failure threshold exceeded)
OPEN (Fail fast)
  ↓ (After timeout period)
HALF_OPEN (Test if service recovered)
  ↓ (Success) → CLOSED
  ↓ (Failure) → OPEN
```

### 5.2 Implementation

```typescript
class CircuitBreaker {
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  private failureCount = 0;
  private successCount = 0;
  private lastFailureTime?: number;
  private nextAttemptTime?: number;

  constructor(
    private failureThreshold: number = 5,
    private successThreshold: number = 2,
    private timeout: number = 60000 // Time before trying again
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttemptTime!) {
        throw new Error('Circuit breaker is OPEN');
      }
      this.state = 'HALF_OPEN';
      this.successCount = 0;
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failureCount = 0;

    if (this.state === 'HALF_OPEN') {
      this.successCount++;
      if (this.successCount >= this.successThreshold) {
        this.state = 'CLOSED';
        console.log('Circuit breaker closed');
      }
    }
  }

  private onFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();

    if (this.state === 'HALF_OPEN') {
      this.state = 'OPEN';
      this.nextAttemptTime = Date.now() + this.timeout;
      console.log('Circuit breaker opened (from half-open)');
    } else if (this.failureCount >= this.failureThreshold) {
      this.state = 'OPEN';
      this.nextAttemptTime = Date.now() + this.timeout;
      console.log('Circuit breaker opened');
    }
  }

  getState() {
    return {
      state: this.state,
      failureCount: this.failureCount,
      successCount: this.successCount
    };
  }
}

// Usage
const breaker = new CircuitBreaker(5, 2, 60000);

async function callExternalAPI() {
  return breaker.execute(async () => {
    const response = await fetch('https://api.example.com/data');
    if (!response.ok) throw new Error('API error');
    return response.json();
  });
}
```

### 5.3 Circuit Breaker with Fallback

```typescript
class CircuitBreakerWithFallback<T> extends CircuitBreaker {
  constructor(
    private fallback: () => Promise<T>,
    failureThreshold?: number,
    successThreshold?: number,
    timeout?: number
  ) {
    super(failureThreshold, successThreshold, timeout);
  }

  async executeWithFallback(fn: () => Promise<T>): Promise<T> {
    try {
      return await this.execute(fn);
    } catch (error) {
      console.log('Using fallback due to:', error.message);
      return await this.fallback();
    }
  }
}

// Usage with cache fallback
const breaker = new CircuitBreakerWithFallback(
  async () => {
    // Fallback to cached data
    return await cache.get('user-data');
  },
  5, 2, 60000
);

const userData = await breaker.executeWithFallback(async () => {
  return await fetch('https://api.example.com/user').then(r => r.json());
});
```

## 6. Idempotency Keys and Tokens

### 6.1 Idempotency Keys

```typescript
// Generate idempotency key
import { v4 as uuidv4 } from 'uuid';

function generateIdempotencyKey(): string {
  return uuidv4();
}

// Client-side: Include idempotency key in request
async function createPayment(amount: number) {
  const idempotencyKey = generateIdempotencyKey();

  const response = await fetch('https://api.example.com/payments', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Idempotency-Key': idempotencyKey
    },
    body: JSON.stringify({ amount })
  });

  return response.json();
}

// Server-side: Check idempotency key
const processedRequests = new Map<string, any>();

app.post('/payments', async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key'];

  if (!idempotencyKey) {
    return res.status(400).json({ error: 'Idempotency-Key required' });
  }

  // Check if already processed
  if (processedRequests.has(idempotencyKey)) {
    return res.json(processedRequests.get(idempotencyKey));
  }

  // Process payment
  const result = await processPayment(req.body.amount);

  // Store result
  processedRequests.set(idempotencyKey, result);

  res.json(result);
});
```

### 6.2 Database-Backed Idempotency

```typescript
// Store idempotency keys in database
interface IdempotencyRecord {
  key: string;
  response: any;
  createdAt: Date;
}

async function handleIdempotentRequest(
  idempotencyKey: string,
  handler: () => Promise<any>
): Promise<any> {
  // Check if already processed
  const existing = await db.idempotency.findOne({ key: idempotencyKey });

  if (existing) {
    console.log('Request already processed, returning cached response');
    return existing.response;
  }

  // Process request
  const response = await handler();

  // Store result
  await db.idempotency.create({
    key: idempotencyKey,
    response,
    createdAt: new Date()
  });

  return response;
}

// Cleanup old idempotency records (run periodically)
async function cleanupIdempotencyRecords() {
  const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
  await db.idempotency.deleteMany({
    createdAt: { $lt: oneDayAgo }
  });
}
```

## 7. Retry Amplification (Cascading Retries)

### The Problem

```
Client → Service A → Service B → Service C

Service C fails:
- Service B retries 3 times
- Service A retries 3 times
- Client retries 3 times

Total requests to C: 1 × 3 × 3 × 3 = 27x amplification!
```

### Solutions

```typescript
// Solution 1: Retry budget (limit total retries)
class RetryBudget {
  private budget = 100; // Allow 100 retries per minute
  private used = 0;

  canRetry(): boolean {
    return this.used < this.budget;
  }

  useRetry() {
    this.used++;
  }

  reset() {
    this.used = 0;
  }
}

// Solution 2: Deadline propagation
interface RequestContext {
  deadline: number; // Timestamp when request must complete
  retriesRemaining: number;
}

async function makeRequestWithDeadline(
  url: string,
  context: RequestContext
): Promise<any> {
  if (Date.now() > context.deadline) {
    throw new Error('Request deadline exceeded');
  }

  if (context.retriesRemaining <= 0) {
    throw new Error('No retries remaining');
  }

  try {
    return await fetch(url, {
      headers: {
        'X-Deadline': context.deadline.toString(),
        'X-Retries-Remaining': context.retriesRemaining.toString()
      }
    });
  } catch (error) {
    context.retriesRemaining--;
    return makeRequestWithDeadline(url, context);
  }
}

// Solution 3: Only retry at the edge
const RETRY_AT_EDGE_ONLY = true;

async function makeRequest(url: string, isEdge: boolean) {
  if (!isEdge && RETRY_AT_EDGE_ONLY) {
    // Internal services don't retry
    return await fetch(url);
  }

  // Only edge (client-facing) services retry
  return await retryWithBackoff(() => fetch(url));
}
```

## 8. Client-Side vs Server-Side Retries

### Client-Side Retries

```typescript
// Client controls retry logic
async function clientSideRetry() {
  let attempt = 0;
  const maxAttempts = 3;

  while (attempt < maxAttempts) {
    try {
      const response = await fetch('https://api.example.com/data');
      if (response.ok) return await response.json();

      // Retry on 5xx errors
      if (response.status >= 500) {
        attempt++;
        await sleep(exponentialBackoff(attempt));
        continue;
      }

      throw new Error(`HTTP ${response.status}`);
    } catch (error) {
      attempt++;
      if (attempt >= maxAttempts) throw error;
      await sleep(exponentialBackoff(attempt));
    }
  }
}
```

**Pros**:
- Client controls retry behavior
- Can retry across multiple servers
- No server-side state needed

**Cons**:
- Inconsistent retry logic across clients
- Can cause retry amplification
- Client may not know best retry strategy

### Server-Side Retries

```typescript
// Server handles retries internally
app.get('/data', async (req, res) => {
  const data = await retryWithBackoff(async () => {
    return await database.query('SELECT * FROM data');
  });

  res.json(data);
});
```

**Pros**:
- Consistent retry logic
- Server knows best retry strategy
- Can implement retry budgets

**Cons**:
- Longer request times
- Holds server resources during retries
- Client doesn't know retries are happening

### Hybrid Approach

```typescript
// Server retries transient failures, client retries server failures
// Server
app.get('/data', async (req, res) => {
  try {
    // Server retries database failures
    const data = await retryWithBackoff(
      () => database.query('SELECT * FROM data'),
      { maxAttempts: 2, backoff: 'exponential' }
    );
    res.json(data);
  } catch (error) {
    // Return 503 to signal client should retry
    res.status(503).json({ error: 'Service temporarily unavailable' });
  }
});

// Client
async function getData() {
  // Client retries 503 errors
  return await retryWithBackoff(
    async () => {
      const response = await fetch('https://api.example.com/data');
      if (response.status === 503) throw new Error('Service unavailable');
      return response.json();
    },
    { maxAttempts: 3, backoff: 'exponential' }
  );
}
```

## 9. Retry Headers (Retry-After)

```typescript
// Server sends Retry-After header
app.get('/data', async (req, res) => {
  if (isOverloaded()) {
    res.set('Retry-After', '60'); // Retry after 60 seconds
    return res.status(503).json({ error: 'Service overloaded' });
  }

  const data = await getData();
  res.json(data);
});

// Client respects Retry-After header
async function makeRequestWithRetryAfter(url: string) {
  const response = await fetch(url);

  if (response.status === 503) {
    const retryAfter = response.headers.get('Retry-After');
    if (retryAfter) {
      const delaySeconds = parseInt(retryAfter, 10);
      console.log(`Server requested retry after ${delaySeconds} seconds`);
      await sleep(delaySeconds * 1000);
      return makeRequestWithRetryAfter(url); // Retry
    }
  }

  return response;
}
```

## 10. Libraries and Implementations

### 10.1 TypeScript/JavaScript

#### axios-retry

```typescript
import axios from 'axios';
import axiosRetry from 'axios-retry';

const client = axios.create();

axiosRetry(client, {
  retries: 3,
  retryDelay: axiosRetry.exponentialDelay,
  retryCondition: (error) => {
    return axiosRetry.isNetworkOrIdempotentRequestError(error) ||
           error.response?.status === 503;
  },
  shouldResetTimeout: true
});

// Usage
const response = await client.get('https://api.example.com/data');
```

#### p-retry

```typescript
import pRetry from 'p-retry';

const result = await pRetry(
  async () => {
    const response = await fetch('https://api.example.com/data');
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  },
  {
    retries: 3,
    factor: 2,
    minTimeout: 1000,
    maxTimeout: 60000,
    randomize: true, // Add jitter
    onFailedAttempt: (error) => {
      console.log(`Attempt ${error.attemptNumber} failed. ${error.retriesLeft} retries left.`);
    }
  }
);
```

### 10.2 Python

#### tenacity

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
import requests

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    retry=retry_if_exception_type(requests.exceptions.RequestException)
)
def fetch_data():
    response = requests.get('https://api.example.com/data')
    response.raise_for_status()
    return response.json()

# Usage
data = fetch_data()
```

#### backoff

```python
import backoff
import requests

@backoff.on_exception(
    backoff.expo,
    requests.exceptions.RequestException,
    max_tries=3,
    max_time=60,
    jitter=backoff.full_jitter
)
def fetch_data():
    response = requests.get('https://api.example.com/data')
    response.raise_for_status()
    return response.json()

# Usage
data = fetch_data()
```

### 10.3 Go

#### retry-go

```go
package main

import (
    "github.com/avast/retry-go"
    "net/http"
    "time"
)

func fetchData() ([]byte, error) {
    var body []byte

    err := retry.Do(
        func() error {
            resp, err := http.Get("https://api.example.com/data")
            if err != nil {
                return err
            }
            defer resp.Body.Close()

            if resp.StatusCode >= 500 {
                return fmt.Errorf("server error: %d", resp.StatusCode)
            }

            body, err = ioutil.ReadAll(resp.Body)
            return err
        },
        retry.Attempts(3),
        retry.Delay(1*time.Second),
        retry.DelayType(retry.BackOffDelay),
        retry.OnRetry(func(n uint, err error) {
            log.Printf("Attempt %d failed: %v", n+1, err)
        }),
    )

    return body, err
}
```

## 11. Testing Retry Logic

```typescript
// Mock server with controlled failures
class MockServer {
  private failureCount = 0;
  private failuresBeforeSuccess: number;

  constructor(failuresBeforeSuccess: number) {
    this.failuresBeforeSuccess = failuresBeforeSuccess;
  }

  async request(): Promise<string> {
    if (this.failureCount < this.failuresBeforeSuccess) {
      this.failureCount++;
      throw new Error('Service unavailable');
    }
    return 'Success';
  }

  reset() {
    this.failureCount = 0;
  }
}

// Test retry logic
describe('Retry logic', () => {
  it('should succeed after 2 failures', async () => {
    const server = new MockServer(2);
    const result = await retryWithBackoff(() => server.request(), {
      maxAttempts: 3
    });
    expect(result).toBe('Success');
  });

  it('should fail after max attempts', async () => {
    const server = new MockServer(5);
    await expect(
      retryWithBackoff(() => server.request(), { maxAttempts: 3 })
    ).rejects.toThrow('Service unavailable');
  });

  it('should use exponential backoff', async () => {
    const delays: number[] = [];
    const server = new MockServer(3);

    await retryWithBackoff(
      () => server.request(),
      {
        maxAttempts: 3,
        onRetry: (attempt, delay) => delays.push(delay)
      }
    );

    expect(delays).toEqual([1000, 2000, 4000]); // Exponential
  });
});
```

## 12. Monitoring Retry Rates

```typescript
// Metrics collection
class RetryMetrics {
  private attempts = 0;
  private successes = 0;
  private failures = 0;
  private retries = 0;

  recordAttempt() {
    this.attempts++;
  }

  recordSuccess(retriesUsed: number) {
    this.successes++;
    this.retries += retriesUsed;
  }

  recordFailure(retriesUsed: number) {
    this.failures++;
    this.retries += retriesUsed;
  }

  getMetrics() {
    return {
      attempts: this.attempts,
      successes: this.successes,
      failures: this.failures,
      retries: this.retries,
      successRate: this.successes / this.attempts,
      retryRate: this.retries / this.attempts,
      avgRetriesPerRequest: this.retries / this.attempts
    };
  }
}

// Instrumented retry function
const metrics = new RetryMetrics();

async function retryWithMetrics<T>(fn: () => Promise<T>): Promise<T> {
  metrics.recordAttempt();
  let retriesUsed = 0;

  try {
    const result = await retryWithBackoff(fn, {
      onRetry: () => retriesUsed++
    });
    metrics.recordSuccess(retriesUsed);
    return result;
  } catch (error) {
    metrics.recordFailure(retriesUsed);
    throw error;
  }
}

// Export metrics to monitoring system
setInterval(() => {
  const m = metrics.getMetrics();
  console.log('Retry metrics:', m);
  // Send to Prometheus, Datadog, etc.
}, 60000);
```

## 13. Real-World Examples

### AWS SDK Retry Logic

```typescript
// AWS SDK uses exponential backoff with jitter
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';

const client = new DynamoDBClient({
  maxAttempts: 3,
  retryMode: 'adaptive', // Adaptive retry mode
});

// AWS retry strategy:
// - Retries throttling errors (429)
// - Retries transient errors (500, 503)
// - Uses exponential backoff with jitter
// - Adaptive mode adjusts retry rate based on success/failure
```

### Stripe API Retry Logic

```typescript
// Stripe recommends exponential backoff with jitter
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  maxNetworkRetries: 2,
  timeout: 80000,
});

// Stripe retry behavior:
// - Retries network errors
// - Retries 409 Conflict (idempotent requests)
// - Retries 429 Too Many Requests (respects Retry-After)
// - Retries 500, 503 errors
// - Uses exponential backoff
```

## 14. Antipatterns

### Antipattern 1: Retry Storms

```typescript
// BAD: All clients retry at same time
❌ async function badRetry() {
  for (let i = 0; i < 3; i++) {
    try {
      return await fetch('https://api.example.com/data');
    } catch (error) {
      await sleep(1000); // Fixed delay - everyone retries together!
    }
  }
}

// GOOD: Add jitter to spread retries
✓ async function goodRetry() {
  for (let i = 0; i < 3; i++) {
    try {
      return await fetch('https://api.example.com/data');
    } catch (error) {
      await sleep(exponentialBackoffWithJitter(i));
    }
  }
}
```

### Antipattern 2: Infinite Retries

```typescript
// BAD: Retry forever
❌ async function infiniteRetry() {
  while (true) {
    try {
      return await fetch('https://api.example.com/data');
    } catch (error) {
      await sleep(1000);
      // Never gives up!
    }
  }
}

// GOOD: Limit retries
✓ async function limitedRetry() {
  const maxAttempts = 3;
  for (let i = 0; i < maxAttempts; i++) {
    try {
      return await fetch('https://api.example.com/data');
    } catch (error) {
      if (i === maxAttempts - 1) throw error;
      await sleep(exponentialBackoff(i));
    }
  }
}
```

### Antipattern 3: Retrying Non-Idempotent Operations

```typescript
// BAD: Retry payment without idempotency key
❌ async function badPayment() {
  return await retryWithBackoff(() =>
    fetch('https://api.example.com/payments', {
      method: 'POST',
      body: JSON.stringify({ amount: 100 })
    })
  );
  // Could charge customer multiple times!
}

// GOOD: Use idempotency key
✓ async function goodPayment() {
  const idempotencyKey = generateIdempotencyKey();
  return await retryWithBackoff(() =>
    fetch('https://api.example.com/payments', {
      method: 'POST',
      headers: { 'Idempotency-Key': idempotencyKey },
      body: JSON.stringify({ amount: 100 })
    })
  );
}
```

### Antipattern 4: No Timeout

```typescript
// BAD: No timeout
❌ async function noTimeout() {
  return await retryWithBackoff(() => fetch('https://api.example.com/data'));
  // Could wait forever!
}

// GOOD: Always set timeout
✓ async function withTimeout() {
  return await retryWithBackoff(
    () => fetchWithTimeout('https://api.example.com/data', 5000),
    { maxAttempts: 3 }
  );
}
```

## Summary

Key takeaways for retry, timeout, and backoff strategies:

1. **Always set timeouts** - Never wait indefinitely
2. **Use exponential backoff with jitter** - Prevents thundering herd
3. **Limit retry attempts** - Use retry budgets to prevent amplification
4. **Only retry idempotent operations** - Use idempotency keys for non-idempotent operations
5. **Implement circuit breakers** - Fail fast when service is down
6. **Respect Retry-After headers** - Server knows best when to retry
7. **Monitor retry rates** - High retry rates indicate problems
8. **Test retry logic** - Ensure it works as expected
9. **Don't retry 4xx errors** - Client errors won't succeed on retry
10. **Use appropriate timeout values** - Based on p99 latency + buffer

---

## Quick Start

### Basic Retry with Exponential Backoff

```python
import time
import random
from typing import Callable, Any

def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0
) -> Any:
    """Retry function with exponential backoff"""
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            # Calculate delay with jitter
            jitter = random.uniform(0, delay * 0.1)
            sleep_time = min(delay + jitter, max_delay)
            
            time.sleep(sleep_time)
            delay *= exponential_base
    
    raise Exception("Max retries exceeded")
```

### Usage

```python
# Retry API call
result = retry_with_backoff(
    lambda: api_client.get_data(),
    max_retries=3,
    initial_delay=1.0
)
```

---

## Production Checklist

- [ ] **Retry Strategy**: Choose appropriate retry strategy (exponential, linear, fixed)
- [ ] **Max Retries**: Set reasonable max retry limits (typically 3-5)
- [ ] **Backoff**: Implement exponential backoff with jitter
- [ ] **Timeout**: Set connection and read timeouts
- [ ] **Idempotency**: Ensure operations are idempotent
- [ ] **Error Classification**: Only retry retryable errors (5xx, network errors)
- [ ] **Circuit Breaker**: Implement circuit breaker to prevent retry storms
- [ ] **Monitoring**: Track retry rates, success rates, latency
- [ ] **Logging**: Log retry attempts with context
- [ ] **Deadline**: Set overall deadline for entire operation
- [ ] **Resource Limits**: Prevent resource exhaustion from too many retries

---

## Anti-patterns

### ❌ Don't: Retry Everything

```python
# ❌ Bad - Retries non-retryable errors
def retry_all(func):
    for i in range(5):
        try:
            return func()
        except Exception:  # Catches everything!
            time.sleep(1)
    raise
```

```python
# ✅ Good - Only retry retryable errors
RETRYABLE_ERRORS = (ConnectionError, TimeoutError, HTTPException)

def retry_smart(func):
    for i in range(5):
        try:
            return func()
        except RETRYABLE_ERRORS:
            if i < 4:
                time.sleep(2 ** i)
                continue
            raise
        except Exception as e:
            # Don't retry client errors (4xx)
            raise
```

### ❌ Don't: No Backoff (Thundering Herd)

```python
# ❌ Bad - All retries happen immediately
def retry_no_backoff(func):
    for i in range(5):
        try:
            return func()
        except Exception:
            pass  # No delay!
    raise
```

```python
# ✅ Good - Exponential backoff with jitter
import random

def retry_with_backoff(func):
    for i in range(5):
        try:
            return func()
        except Exception:
            if i < 4:
                delay = (2 ** i) + random.uniform(0, 1)  # Jitter
                time.sleep(delay)
                continue
            raise
```

### ❌ Don't: Infinite Retries

```python
# ❌ Bad - Never gives up
def retry_forever(func):
    while True:
        try:
            return func()
        except Exception:
            time.sleep(1)  # Retries forever!
```

```python
# ✅ Good - Bounded retries
def retry_bounded(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
                continue
            raise
```

### ❌ Don't: No Timeout

```python
# ❌ Bad - Waits forever
response = requests.get(url)  # No timeout!
```

```python
# ✅ Good - Set timeouts
response = requests.get(
    url,
    timeout=(5, 30)  # (connect timeout, read timeout)
)
```

### ❌ Don't: Retry Non-Idempotent Operations

```python
# ❌ Bad - Retries can cause duplicates
def create_order(data):
    return retry_with_backoff(
        lambda: api.post('/orders', data)  # Creates order multiple times!
    )
```

```python
# ✅ Good - Make idempotent or don't retry
def create_order(data, idempotency_key):
    return retry_with_backoff(
        lambda: api.post('/orders', data, headers={
            'Idempotency-Key': idempotency_key  # Prevents duplicates
        })
    )
```

---

## Integration Points

- **Failure Modes** (`40-system-resilience/failure-modes/`) - Understanding what failures to retry
- **Chaos Engineering** (`40-system-resilience/chaos-engineering/`) - Testing retry behavior
- **Bulkhead Patterns** (`40-system-resilience/bulkhead-patterns/`) - Isolating failures
- **Circuit Breaker** (`40-system-resilience/graceful-degradation/`) - Preventing retry storms
- **Error Handling** (`03-backend-api/error-handling/`) - Error classification

---

## Further Reading

- [Exponential Backoff and Jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)
- [Retry Pattern (Microsoft)](https://docs.microsoft.com/en-us/azure/architecture/patterns/retry)
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
- `40-system-resilience/graceful-degradation` - Fallback strategies
