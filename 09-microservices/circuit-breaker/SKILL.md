# Circuit Breaker Pattern

## Overview

Comprehensive guide to circuit breaker pattern implementation for microservices resilience.

## Table of Contents

1. [Circuit Breaker Concept](#circuit-breaker-concept)
2. [States (Closed, Open, Half-Open)](#states-closed-open-half-open)
3. [Implementation](#implementation)
4. [Configuration](#configuration)
5. [Bulkhead Pattern](#bulkhead-pattern)
6. [Retry Strategies](#retry-strategies)
7. [Timeout Patterns](#timeout-patterns)
8. [Monitoring](#monitoring)
9. [Testing](#testing)
10. [Production Patterns](#production-patterns)

---

## Circuit Breaker Concept

### Core Concept

```markdown
## Circuit Breaker Pattern

### What is a Circuit Breaker?
- Prevents cascading failures in distributed systems
- Detects failures and stops calling failing services
- Allows recovery by testing if service is healthy again

### States
1. **Closed** - Normal operation, requests pass through
2. **Open** - Circuit is tripped, requests fail immediately
3. **Half-Open** - Testing if service has recovered

### Benefits
- Prevents system overload
- Fast failure when service is down
- Automatic recovery
- Improved user experience
```

### Circuit Breaker Diagram

```typescript
// circuit-breaker-types.ts
export enum CircuitState {
  CLOSED = 'closed',
  OPEN = 'open',
  HALF_OPEN = 'half_open'
}

export interface CircuitBreakerConfig {
  failureThreshold: number;
  successThreshold: number;
  timeout: number; // Time to wait before trying again
  monitoringPeriod: number;
}

export interface CircuitBreakerStats {
  state: CircuitState;
  failureCount: number;
  successCount: number;
  lastFailureTime: Date | null;
  lastSuccessTime: Date | null;
}
```

---

## States (Closed, Open, Half-Open)

### State Transitions

```typescript
// circuit-breaker-states.ts
export enum CircuitState {
  CLOSED = 'closed',
  OPEN = 'open',
  HALF_OPEN = 'half_open'
}

export class CircuitBreakerStateMachine {
  private state: CircuitState = CircuitState.CLOSED;
  private failureCount = 0;
  private successCount = 0;
  private lastFailureTime: Date | null = null;
  private lastStateChange: Date = new Date();
  
  constructor(
    private config: {
      failureThreshold: number;
      successThreshold: number;
      timeout: number;
    }
  ) {}
  
  recordFailure(): void {
    this.failureCount++;
    this.successCount = 0;
    this.lastFailureTime = new Date();
    
    if (this.state === CircuitState.CLOSED && 
        this.failureCount >= this.config.failureThreshold) {
      this.transitionTo(CircuitState.OPEN);
    } else if (this.state === CircuitState.HALF_OPEN) {
      this.transitionTo(CircuitState.OPEN);
    }
  }
  
  recordSuccess(): void {
    this.successCount++;
    this.failureCount = 0;
    
    if (this.state === CircuitState.HALF_OPEN && 
        this.successCount >= this.config.successThreshold) {
      this.transitionTo(CircuitState.CLOSED);
    }
  }
  
  canAttempt(): boolean {
    if (this.state === CircuitState.CLOSED) {
      return true;
    }
    
    if (this.state === CircuitState.OPEN) {
      const timeSinceFailure = Date.now() - this.lastFailureTime!.getTime();
      return timeSinceFailure >= this.config.timeout;
    }
    
    // HALF_OPEN allows one attempt
    return true;
  }
  
  private transitionTo(newState: CircuitState): void {
    console.log(`Circuit breaker transition: ${this.state} -> ${newState}`);
    this.state = newState;
    this.lastStateChange = new Date();
    
    if (newState === CircuitState.CLOSED) {
      this.failureCount = 0;
      this.successCount = 0;
    } else if (newState === CircuitState.HALF_OPEN) {
      this.successCount = 0;
    }
  }
  
  getState(): CircuitState {
    return this.state;
  }
  
  getStats(): any {
    return {
      state: this.state,
      failureCount: this.failureCount,
      successCount: this.successCount,
      lastFailureTime: this.lastFailureTime,
      lastStateChange: this.lastStateChange
    };
  }
}
```

---

## Implementation

### Node.js (opossum)

```typescript
// circuit-breaker-opossum.ts
import CircuitBreaker from 'opossum';
import { CircuitBreakerOptions } from 'opossum';

export class OpossumCircuitBreaker {
  private breaker: CircuitBreaker;
  
  constructor(
    private action: (...args: any[]) => Promise<any>,
    options: CircuitBreakerOptions
  ) {
    const defaultOptions: CircuitBreakerOptions = {
      timeout: 10000, // 10 seconds
      errorThresholdPercentage: 50,
      resetTimeout: 30000, // 30 seconds
      rollingCountTimeout: 10000,
      rollingCountBuckets: 10,
      cache: false,
      fallback: this.defaultFallback.bind(this),
      ...options
    };
    
    this.breaker = new CircuitBreaker(this.action, defaultOptions);
    this.setupEventListeners();
  }
  
  private setupEventListeners(): void {
    this.breaker.on('open', () => {
      console.log('Circuit breaker OPEN');
    });
    
    this.breaker.on('halfOpen', () => {
      console.log('Circuit breaker HALF_OPEN');
    });
    
    this.breaker.on('close', () => {
      console.log('Circuit breaker CLOSED');
    });
    
    this.breaker.on('fallback', (result) => {
      console.log('Fallback executed:', result);
    });
    
    this.breaker.on('reject', () => {
      console.log('Request rejected - circuit is OPEN');
    });
  }
  
  async execute(...args: any[]): Promise<any> {
    return this.breaker.fire(...args);
  }
  
  private defaultFallback(...args: any[]): any {
    throw new Error('Circuit breaker is OPEN');
  }
  
  getState(): string {
    return this.breaker.opened ? 'OPEN' : 'CLOSED';
  }
  
  getStats(): any {
    return {
      state: this.getState(),
      stats: this.breaker.stats,
      status: this.breaker.status
    };
  }
}

// Usage
const breaker = new OpossumCircuitBreaker(
  async (userId: string) => {
    const response = await fetch(`https://api.example.com/users/${userId}`);
    return response.json();
  },
  {
    timeout: 5000,
    errorThresholdPercentage: 50,
    resetTimeout: 30000,
    rollingCountTimeout: 10000
  }
);

try {
  const user = await breaker.execute('123');
  console.log(user);
} catch (error) {
  console.error('Error:', error);
}
```

### Python (pybreaker)

```python
# circuit-breaker-pybreaker.py
from pybreaker import CircuitBreaker, CircuitBreakerError
import time
import logging

class PyBreakerCircuitBreaker:
    def __init__(
        self,
        action: callable,
        failure_threshold: int = 5,
        recovery_timeout: int = 30,
        expected_exception: Exception = Exception
    ):
        self.breaker = CircuitBreaker(
            fail_max=failure_threshold,
            timeout_duration=recovery_timeout,
            expected_exception=expected_exception
        )
        self.action = action
        self.setup_listeners()
    
    def setup_listeners(self):
        self.breaker.add_listener('open', self.on_open)
        self.breaker.add_listener('half_open', self.on_half_open)
        self.breaker.add_listener('close', self.on_close)
    
    def on_open(self, breaker):
        logging.info('Circuit breaker OPEN')
    
    def on_half_open(self, breaker):
        logging.info('Circuit breaker HALF_OPEN')
    
    def on_close(self, breaker):
        logging.info('Circuit breaker CLOSED')
    
    async def execute(self, *args, **kwargs):
        try:
            result = await self.breaker.call(self.action, *args, **kwargs)
            return result
        except CircuitBreakerError:
            raise Exception('Circuit breaker is OPEN')
    
    def get_state(self) -> str:
        if self.breaker.current_state == 'open':
            return 'OPEN'
        elif self.breaker.current_state == 'half_open':
            return 'HALF_OPEN'
        else:
            return 'CLOSED'
    
    def get_stats(self) -> dict:
        return {
            'state': self.get_state(),
            'failure_count': self.breaker.fail_counter,
            'success_count': self.breaker.success_counter,
            'last_failure': self.breaker.last_failure
        }

# Usage
import aiohttp

async def fetch_user(user_id: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.example.com/users/{user_id}') as response:
            return await response.json()

breaker = PyBreakerCircuitBreaker(
    fetch_user,
    failure_threshold=5,
    recovery_timeout=30
)

try:
    user = await breaker.execute('123')
    print(user)
except Exception as e:
    print(f'Error: {e}')
```

---

## Configuration

### Threshold Configuration

```typescript
// circuit-breaker-config.ts
export interface CircuitBreakerConfig {
  // Failure thresholds
  failureThreshold: number;
  failureThresholdPercentage: number;
  successThreshold: number;
  
  // Timeouts
  timeout: number; // Request timeout
  resetTimeout: number; // Time to wait before trying again
  monitoringPeriod: number;
  
  // Rolling window
  rollingCountTimeout: number;
  rollingCountBuckets: number;
  
  // Fallback
  fallback?: (...args: any[]) => any;
  
  // Cache
  cache?: boolean;
  cacheTimeout?: number;
  
  // Sliding window
  slidingWindowType?: 'count' | 'time';
  slidingWindowSize?: number;
}

export const defaultConfig: CircuitBreakerConfig = {
  failureThreshold: 5,
  failureThresholdPercentage: 50,
  successThreshold: 2,
  timeout: 10000,
  resetTimeout: 30000,
  monitoringPeriod: 60000,
  rollingCountTimeout: 10000,
  rollingCountBuckets: 10,
  cache: false,
  slidingWindowType: 'count',
  slidingWindowSize: 10
};

export const aggressiveConfig: CircuitBreakerConfig = {
  ...defaultConfig,
  failureThreshold: 3,
  failureThresholdPercentage: 30,
  resetTimeout: 10000
};

export const conservativeConfig: CircuitBreakerConfig = {
  ...defaultConfig,
  failureThreshold: 10,
  failureThresholdPercentage: 70,
  resetTimeout: 60000
};
```

---

## Bulkhead Pattern

### Bulkhead Implementation

```typescript
// bulkhead.ts
export class Bulkhead {
  private semaphore: number;
  private queue: Array<() => void> = [];
  
  constructor(concurrency: number) {
    this.semaphore = concurrency;
  }
  
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    return new Promise((resolve, reject) => {
      const task = async () => {
        try {
          const result = await fn();
          resolve(result);
        } catch (error) {
          reject(error);
        } finally {
          this.release();
        }
      };
      
      if (this.semaphore > 0) {
        this.semaphore--;
        task();
      } else {
        this.queue.push(task);
      }
    });
  }
  
  private release(): void {
    if (this.queue.length > 0) {
      const task = this.queue.shift()!;
      task();
    } else {
      this.semaphore++;
    }
  }
  
  getAvailableSlots(): number {
    return this.semaphore;
  }
  
  getQueueLength(): number {
    return this.queue.length;
  }
}

// Usage
const bulkhead = new Bulkhead(5); // Max 5 concurrent requests

async function makeRequest(url: string) {
  return await bulkhead.execute(async () => {
    const response = await fetch(url);
    return response.json();
  });
}

// Make multiple requests
const promises = [
  makeRequest('https://api.example.com/users/1'),
  makeRequest('https://api.example.com/users/2'),
  makeRequest('https://api.example.com/users/3')
];

const results = await Promise.all(promises);
```

---

## Retry Strategies

### Exponential Backoff

```typescript
// retry-strategies.ts
export interface RetryConfig {
  maxAttempts: number;
  initialDelay: number;
  maxDelay: number;
  backoffMultiplier: number;
  jitter: boolean;
}

export class RetryStrategy {
  constructor(private config: RetryConfig) {}
  
  async execute<T>(fn: () => Promise<T>): Promise<T> {
    let lastError: Error;
    
    for (let attempt = 1; attempt <= this.config.maxAttempts; attempt++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error as Error;
        
        if (attempt < this.config.maxAttempts) {
          const delay = this.calculateDelay(attempt);
          await this.sleep(delay);
        }
      }
    }
    
    throw lastError;
  }
  
  private calculateDelay(attempt: number): number {
    let delay = this.config.initialDelay * Math.pow(this.config.backoffMultiplier, attempt - 1);
    delay = Math.min(delay, this.config.maxDelay);
    
    if (this.config.jitter) {
      delay = delay * (0.5 + Math.random() * 0.5);
    }
    
    return delay;
  }
  
  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Usage
const retry = new RetryStrategy({
  maxAttempts: 3,
  initialDelay: 1000,
  maxDelay: 10000,
  backoffMultiplier: 2,
  jitter: true
});

try {
  const result = await retry.execute(async () => {
    const response = await fetch('https://api.example.com/data');
    return response.json();
  });
  console.log(result);
} catch (error) {
  console.error('All retries failed:', error);
}
```

---

## Timeout Patterns

### Timeout Implementation

```typescript
// timeout.ts
export class Timeout {
  static async execute<T>(fn: () => Promise<T>, timeoutMs: number): Promise<T> {
    return Promise.race([
      fn(),
      new Promise<T>((_, reject) => 
        setTimeout(() => reject(new Error('Timeout')), timeoutMs)
      )
    ]);
  }
  
  static async executeWithFallback<T>(
    fn: () => Promise<T>,
    timeoutMs: number,
    fallback: () => T
  ): Promise<T> {
    try {
      return await this.execute(fn, timeoutMs);
    } catch (error) {
      if ((error as Error).message === 'Timeout') {
        return fallback();
      }
      throw error;
    }
  }
}

// Usage
try {
  const result = await Timeout.execute(
    async () => {
      const response = await fetch('https://api.example.com/data');
      return response.json();
    },
    5000 // 5 second timeout
  );
  console.log(result);
} catch (error) {
  console.error('Request failed:', error);
}

// With fallback
const result = await Timeout.executeWithFallback(
  async () => {
    const response = await fetch('https://api.example.com/data');
    return response.json();
  },
  5000,
  () => ({ cached: true, data: [] })
);
```

---

## Monitoring

### Circuit Breaker Metrics

```typescript
// circuit-breaker-metrics.ts
import promClient from 'prom-client';

export class CircuitBreakerMetrics {
  private stateGauge: promClient.Gauge;
  private failureCounter: promClient.Counter;
  private successCounter: promClient.Counter;
  private rejectCounter: promClient.Counter;
  private fallbackCounter: promClient.Counter;
  
  constructor(name: string) {
    const labels = { circuit_breaker: name };
    
    this.stateGauge = new promClient.Gauge({
      name: 'circuit_breaker_state',
      help: 'Circuit breaker state (0=closed, 1=open, 2=half_open)',
      labelNames: ['circuit_breaker'],
      registers: [promClient.register]
    });
    
    this.failureCounter = new promClient.Counter({
      name: 'circuit_breaker_failures_total',
      help: 'Total number of failures',
      labelNames: ['circuit_breaker'],
      registers: [promClient.register]
    });
    
    this.successCounter = new promClient.Counter({
      name: 'circuit_breaker_successes_total',
      help: 'Total number of successes',
      labelNames: ['circuit_breaker'],
      registers: [promClient.register]
    });
    
    this.rejectCounter = new promClient.Counter({
      name: 'circuit_breaker_rejects_total',
      help: 'Total number of rejected requests',
      labelNames: ['circuit_breaker'],
      registers: [promClient.register]
    });
    
    this.fallbackCounter = new promClient.Counter({
      name: 'circuit_breaker_fallbacks_total',
      help: 'Total number of fallback executions',
      labelNames: ['circuit_breaker'],
      registers: [promClient.register]
    });
  }
  
  recordState(state: string): void {
    const stateValue = state === 'OPEN' ? 1 : state === 'HALF_OPEN' ? 2 : 0;
    this.stateGauge.set({ circuit_breaker: this.name }, stateValue);
  }
  
  recordFailure(): void {
    this.failureCounter.inc({ circuit_breaker: this.name });
  }
  
  recordSuccess(): void {
    this.successCounter.inc({ circuit_breaker: this.name });
  }
  
  recordReject(): void {
    this.rejectCounter.inc({ circuit_breaker: this.name });
  }
  
  recordFallback(): void {
    this.fallbackCounter.inc({ circuit_breaker: this.name });
  }
  
  getMetrics(): string {
    return promClient.register.metrics();
  }
}
```

---

## Testing

### Circuit Breaker Tests

```typescript
// circuit-breaker.test.ts
import { describe, it, expect, beforeEach } from '@jest/globals';
import { CircuitBreakerStateMachine } from './circuit-breaker-states';

describe('CircuitBreakerStateMachine', () => {
  let breaker: CircuitBreakerStateMachine;
  
  beforeEach(() => {
    breaker = new CircuitBreakerStateMachine({
      failureThreshold: 3,
      successThreshold: 2,
      timeout: 30000
    });
  });
  
  describe('initial state', () => {
    it('should start in CLOSED state', () => {
      expect(breaker.getState()).toBe(CircuitState.CLOSED);
    });
    
    it('should allow attempts when CLOSED', () => {
      expect(breaker.canAttempt()).toBe(true);
    });
  });
  
  describe('failure handling', () => {
    it('should transition to OPEN after threshold failures', () => {
      breaker.recordFailure();
      breaker.recordFailure();
      breaker.recordFailure();
      
      expect(breaker.getState()).toBe(CircuitState.OPEN);
    });
    
    it('should reject attempts when OPEN', () => {
      breaker.recordFailure();
      breaker.recordFailure();
      breaker.recordFailure();
      
      expect(breaker.canAttempt()).toBe(false);
    });
  });
  
  describe('recovery', () => {
    it('should transition to HALF_OPEN after timeout', () => {
      breaker.recordFailure();
      breaker.recordFailure();
      breaker.recordFailure();
      
      // Wait for timeout
      jest.useFakeTimers();
      jest.advanceTimersByTime(31000);
      
      expect(breaker.canAttempt()).toBe(true);
      expect(breaker.getState()).toBe(CircuitState.HALF_OPEN);
    });
    
    it('should transition to CLOSED after success threshold', () => {
      breaker.recordFailure();
      breaker.recordFailure();
      breaker.recordFailure();
      
      // Simulate timeout
      jest.useFakeTimers();
      jest.advanceTimersByTime(31000);
      
      // Record successes
      breaker.recordSuccess();
      breaker.recordSuccess();
      
      expect(breaker.getState()).toBe(CircuitState.CLOSED);
    });
  });
});
```

---

## Production Patterns

### Circuit Breaker with Fallback

```typescript
// production-circuit-breaker.ts
export class ProductionCircuitBreaker {
  constructor(
    private action: (...args: any[]) => Promise<any>,
    private fallback: (...args: any[]) => Promise<any>,
    config: CircuitBreakerConfig
  ) {
    this.breaker = new OpossumCircuitBreaker(action, {
      ...config,
      fallback: this.executeFallback.bind(this)
    });
  }
  
  private async executeFallback(...args: any[]): Promise<any> {
    console.log('Executing fallback');
    return this.fallback(...args);
  }
  
  async execute(...args: any[]): Promise<any> {
    try {
      return await this.breaker.execute(...args);
    } catch (error) {
      console.error('Circuit breaker error:', error);
      throw error;
    }
  }
}

// Usage with cache fallback
const cache = new Map();

const breaker = new ProductionCircuitBreaker(
  async (userId: string) => {
    const response = await fetch(`https://api.example.com/users/${userId}`);
    return response.json();
  },
  async (userId: string) => {
    console.log('Using cached data for user:', userId);
    return cache.get(userId) || { error: 'User not found' };
  },
  {
    timeout: 5000,
    errorThresholdPercentage: 50,
    resetTimeout: 30000
  }
);
```

---

## Additional Resources

- [Opossum Documentation](https://nodeshift.dev/opossum/)
- [PyBreaker Documentation](https://pypi.org/project/pybreaker/)
- [Circuit Breaker Pattern](https://martinfowler.com/bliki/CircuitBreaker.html)
- [Resilience4j Documentation](https://resilience4j.readme.io/)

## Best Practices

### Circuit Breaker Configuration

- **Set appropriate thresholds**: Don't set too sensitive or too lenient
- **Use rolling windows**: Track failures over time, not just count
- **Configure timeout appropriately**: Balance between responsiveness and recovery
- **Set reset timeout**: Allow circuit to close after recovery time
- **Monitor circuit state**: Track how often circuits open

### Failure Detection

- **Classify error types**: Distinguish between retryable and non-retryable errors
- **Use appropriate thresholds**: Different thresholds for different services
- **Consider seasonal patterns**: Adjust for expected traffic patterns
- **Handle timeouts separately**: Timeouts may not indicate service failure
- **Monitor false positives**: Track circuits opening incorrectly

### State Management

- **Persist circuit state**: Store state across restarts
- **Use distributed coordination**: For multiple instances of same service
- **Implement graceful degradation**: Use fallbacks when circuit is open
- **Communicate state**: Notify users when services are degraded
- **Monitor state transitions**: Track circuit behavior over time

### Fallback Strategies

- **Provide meaningful fallbacks**: Return cached data or default values
- **Make fallbacks fast**: Don't add latency when circuit is open
- **Log fallback usage**: Track when and how often fallbacks are used
- **Consider partial degradation**: Provide reduced functionality instead of complete failure
- **Test fallback paths**: Ensure fallbacks work correctly

### Retry Integration

- **Use exponential backoff**: Retry with increasing delays
- **Add jitter**: Randomize retry delays to avoid thundering herd
- **Limit retry attempts**: Don't retry indefinitely
- **Combine with circuit breaker**: Stop retries when circuit is open
- **Monitor retry success rates**: Track if retries are effective

### Monitoring

- **Track circuit state**: Monitor open/closed/half-open transitions
- **Monitor failure rates**: Track service health over time
- **Alert on circuit opens**: Notify when circuits trip
- **Monitor fallback usage**: Track how often fallbacks are used
- **Visualize metrics**: Create dashboards for circuit breaker health

### Performance

- **Keep circuit checks fast**: Don't add significant latency
- **Use appropriate data structures**: Efficient tracking of failures
- **Minimize memory usage**: Don't store excessive history
- **Consider circuit breaker overhead**: Weigh benefits against cost
- **Profile under load**: Ensure circuit breaker performs at scale

### Testing

- **Test circuit behavior**: Verify circuits open and close as expected
- **Test failure scenarios**: Simulate service failures
- **Test recovery scenarios**: Verify circuits close after service recovers
- **Test with concurrent requests**: Ensure thread safety
- **Load test**: Verify circuit breaker handles high traffic

### Production Considerations

- **Start in monitoring mode**: Log actions without affecting requests
- **Gradually enable enforcement**: Ramp up circuit breaker impact
- **Monitor closely**: Watch for unexpected behavior after deployment
- **Have rollback plan**: Be ready to disable if issues arise
- **Document procedures**: Clear runbooks for circuit breaker issues

## Checklist

### Design
- [ ] Identify services that need circuit breakers
- [ ] Define failure thresholds
- [ ] Configure timeout values
- [ ] Design fallback strategies
- [ ] Plan monitoring and alerting

### Configuration
- [ ] Set failure thresholds
- [ ] Configure success thresholds
- [ ] Set timeout values
- [ ] Configure reset timeout
- [ ] Choose appropriate rolling window

### State Management
- [ ] Implement circuit state tracking
- [ ] Configure state persistence
- [ ] Set up distributed coordination
- [ ] Implement graceful degradation
- [ ] Configure state change notifications

### Fallback Implementation
- [ ] Design fallback responses
- [ ] Implement cached data fallbacks
- [ ] Implement default value fallbacks
- [ ] Add fallback logging
- [ ] Test fallback paths

### Retry Integration
- [ ] Configure retry policies
- [ ] Set up exponential backoff
- [ ] Add jitter to retries
- [ ] Limit retry attempts
- [ ] Combine with circuit breaker

### Monitoring Setup
- [ ] Configure metrics collection
- [ ] Set up state tracking
- [ ] Configure failure rate monitoring
- [ ] Set up alerts
- [ ] Create dashboards

### Testing
- [ ] Write circuit state tests
- [ ] Test failure scenarios
- [ ] Test recovery scenarios
- [ ] Load test circuit breaker
- [ ] Test concurrent requests

### Deployment
- [ ] Plan deployment strategy
- [ ] Configure monitoring mode
- [ ] Set up rollback plan
- [ ] Document deployment procedures
- [ ] Train team on runbooks

### Documentation
- [ ] Document circuit breaker configuration
- [ ] Document fallback strategies
- [ ] Create runbooks for issues
- [ ] Document monitoring setup
- [ ] Maintain API documentation
