# Rate Limiting

A comprehensive guide to rate limiting implementation patterns.

## Table of Contents

1. [Rate Limiting Algorithms](#rate-limiting-algorithms)
2. [Implementation](#implementation)
3. [Per-User Limits](#per-user-limits)
4. [Per-Endpoint Limits](#per-endpoint-limits)
5. [Quota Management](#quota-management)
6. [Response Headers](#response-headers)
7. [Error Handling](#error-handling)
8. [Distributed Rate Limiting](#distributed-rate-limiting)
9. [Testing](#testing)
10. [Best Practices](#best-practices)

---

## Rate Limiting Algorithms

### Token Bucket

```
┌─────────────────────────────────────────────────────┐
│              Token Bucket Algorithm               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Bucket Size: 100 tokens                           │
│  Refill Rate: 10 tokens/second                   │
│                                                     │
│  Request ─>  Check bucket ─>  Consume token │
│  ─>  If enough tokens ─>  Allow                │
│  ─>  If not enough ─>  Rate limit              │
│                                                     │
│  Tokens refill over time at constant rate           │
└─────────────────────────────────────────────────────┘
```

```typescript
class TokenBucket {
  private tokens: number;
  private readonly capacity: number;
  private readonly refillRate: number;
  private lastRefill: number;

  constructor(capacity: number, refillRate: number) {
    this.capacity = capacity;
    this.refillRate = refillRate;
    this.tokens = capacity;
    this.lastRefill = Date.now();
  }

  refill(): void {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000; // seconds
    const tokensToAdd = elapsed * this.refillRate;

    this.tokens = Math.min(this.capacity, this.tokens + tokensToAdd);
    this.lastRefill = now;
  }

  tryConsume(tokens: number = 1): boolean {
    this.refill();
    if (this.tokens >= tokens) {
      this.tokens -= tokens;
      return true;
    }
    return false;
  }

  getAvailableTokens(): number {
    this.refill();
    return this.tokens;
  }
}
```

### Leaky Bucket

```
┌─────────────────────────────────────────────────────┐
│             Leaky Bucket Algorithm               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Bucket Size: 100 requests                         │
│  Leak Rate: 10 requests/second                    │
│                                                     │
│  Request ─>  Add to bucket                       │
│  ─> Bucket leaks at constant rate                   │
│  ─> If bucket full ─>  Rate limit                  │
│                                                     │
│  Requests leak out over time                          │
└─────────────────────────────────────────────────────┘
```

```typescript
class LeakyBucket {
  private queue: number[];
  private readonly capacity: number;
  private readonly leakRate: number;
  private lastLeak: number;

  constructor(capacity: number, leakRate: number) {
    this.capacity = capacity;
    this.leakRate = leakRate;
    this.queue = [];
    this.lastLeak = Date.now();
  }

  leak(): void {
    const now = Date.now();
    const elapsed = (now - this.lastLeak) / 1000; // seconds
    const leakCount = Math.floor(elapsed * this.leakRate);

    for (let i = 0; i < leakCount && this.queue.length > 0; i++) {
      this.queue.shift();
    }

    this.lastLeak = now;
  }

  tryAdd(): boolean {
    this.leak();
    if (this.queue.length < this.capacity) {
      this.queue.push(Date.now());
      return true;
    }
    return false;
  }

  getQueueSize(): number {
    this.leak();
    return this.queue.length;
  }
}
```

### Fixed Window

```
┌─────────────────────────────────────────────────────┐
│            Fixed Window Algorithm                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Window Size: 1 minute                              │
│  Max Requests: 100                                 │
│                                                     │
│  ┌──────────────────────────────────────┐           │
│  │  00:00 - 00:59: Count requests │           │
│  └──────────────────────────────────────┘           │
│                                                     │
│  If count > max ─>  Rate limit                    │
│  Reset at window boundary                            │
└─────────────────────────────────────────────────────┘
```

```typescript
class FixedWindow {
  private requests: Map<string, number[]>;
  private readonly windowSize: number;
  private readonly maxRequests: number;

  constructor(windowSize: number, maxRequests: number) {
    this.windowSize = windowSize;
    this.maxRequests = maxRequests;
    this.requests = new Map();
  }

  tryAdd(key: string): boolean {
    const now = Date.now();
    const windowStart = Math.floor(now / (this.windowSize * 1000)) * (this.windowSize * 1000);

    if (!this.requests.has(key)) {
      this.requests.set(key, []);
    }

    const requests = this.requests.get(key)!;
    const validRequests = requests.filter(timestamp => timestamp >= windowStart);

    if (validRequests.length < this.maxRequests) {
      validRequests.push(now);
      this.requests.set(key, validRequests);
      return true;
    }

    return false;
  }

  getRemaining(key: string): number {
    const now = Date.now();
    const windowStart = Math.floor(now / (this.windowSize * 1000)) * (this.windowSize * 1000);

    if (!this.requests.has(key)) {
      return this.maxRequests;
    }

    const requests = this.requests.get(key)!;
    const validRequests = requests.filter(timestamp => timestamp >= windowStart);

    return this.maxRequests - validRequests.length;
  }
}
```

### Sliding Window

```
┌─────────────────────────────────────────────────────┐
│           Sliding Window Algorithm                │
├─────────────────────────────────────────────────────┤
│                                                     │
│  Window Size: 1 minute                              │
│  Max Requests: 100                                 │
│                                                     │
│  ┌──────────────────────────────────────┐           │
│  │  Count requests in sliding window  │           │
│  │  [now - 1min, now]                        │           │
│  └──────────────────────────────────────┘           │
│                                                     │
│  If count > max ─>  Rate limit                    │
│  More accurate than fixed window                       │
└─────────────────────────────────────────────────────┘
```

```typescript
class SlidingWindow {
  private requests: Map<string, number[]>;
  private readonly windowSize: number;
  private readonly maxRequests: number;

  constructor(windowSize: number, maxRequests: number) {
    this.windowSize = windowSize;
    this.maxRequests = maxRequests;
    this.requests = new Map();
  }

  tryAdd(key: string): boolean {
    const now = Date.now();
    const windowStart = now - (this.windowSize * 1000);

    if (!this.requests.has(key)) {
      this.requests.set(key, []);
    }

    const requests = this.requests.get(key)!;
    const validRequests = requests.filter(timestamp => timestamp >= windowStart);

    if (validRequests.length < this.maxRequests) {
      validRequests.push(now);
      this.requests.set(key, validRequests);
      return true;
    }

    return false;
  }

  getRemaining(key: string): number {
    const now = Date.now();
    const windowStart = now - (this.windowSize * 1000);

    if (!this.requests.has(key)) {
      return this.maxRequests;
    }

    const requests = this.requests.get(key)!;
    const validRequests = requests.filter(timestamp => timestamp >= windowStart);

    return this.maxRequests - validRequests.length;
  }
}
```

---

## Implementation

### Express Rate Limiting

```typescript
import express from 'express';
import rateLimit from 'express-rate-limit';

const app = express();

// Basic rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: 'Too many requests from this IP, please try again after 15 minutes',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api', limiter);

app.get('/api/users', (req, res) => {
  res.json({ users: [] });
});
```

### Express Rate Limiting with Custom Key

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  keyGenerator: (req) => {
    // Rate limit by user ID if authenticated
    return req.user?.id || req.ip;
  },
  skip: (req) => {
    // Skip rate limiting for certain routes
    return req.path.startsWith('/api/public');
  },
});

app.use('/api', limiter);
```

### FastAPI Rate Limiting

```python
from fastapi import FastAPI, Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

app = FastAPI()

# Rate limiter
limiter = Limiter(key_func=get_remote_address, rate="100/15minute")

@app.get("/api/users")
@limiter.limit("100/15minute")
async def get_users(request: Request):
    return {"users": []}

# Custom rate limit exceeded handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": "Too many requests"}
    )
```

### Django Rate Limiting

```python
from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from functools import wraps

def rate_limit(key_func, rate, period):
    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            key = key_func(request)
            cache_key = f"rate_limit:{key}"
            
            count = cache.get_or_set(cache_key, 0, timeout=period)
            
            if count >= rate:
                return HttpResponse(
                    "Rate limit exceeded",
                    status_code=429
                )
            
            cache.incr(cache_key)
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator

# Usage
@require_http_methods(["GET"])
@rate_limit(
    key_func=lambda r: r.META.get('REMOTE_ADDR'),
    rate=100,
    period=60
)
def api_view(request):
    return JsonResponse({"users": []})
```

---

## Per-User Limits

### Express Per-User Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

const userLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  keyGenerator: (req) => {
    // Rate limit by user ID
    return `user:${req.user?.id}` || `ip:${req.ip}`;
  },
  skip: (req) => {
    // Skip if not authenticated
    return !req.user;
  },
});

app.use('/api', userLimiter);
```

### FastAPI Per-User Rate Limiting

```python
from fastapi import FastAPI, Request, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler

app = FastAPI()

# Rate limiter for authenticated users
user_limiter = Limiter(key_func=lambda r: r.state.user.id, rate="100/15minute")

@app.get("/api/users")
@user_limiter.limit("100/15minute")
async def get_users(request: Request):
    return {"users": []}
```

### Redis-Based Per-User Rate Limiting

```typescript
import { createClient } from 'redis';
import rateLimit from 'express-rate-limit-redis';

const redisClient = createClient({ url: process.env.REDIS_URL });

const userLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'ratelimit:',
  }),
  windowMs: 15 * 60 * 1000,
  max: 100,
  keyGenerator: (req) => {
    return `user:${req.user?.id}` || `ip:${req.ip}`;
  },
});

app.use('/api', userLimiter);
```

---

## Per-Endpoint Limits

### Express Per-Endpoint Rate Limiting

```typescript
import rateLimit from 'express-rate-limit';

// Different limits for different endpoints
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  keyGenerator: (req) => `${req.ip}:${req.path}`,
});

const uploadLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,
  max: 10,
  keyGenerator: (req) => `${req.ip}:${req.path}`,
});

app.use('/api', apiLimiter);
app.use('/upload', uploadLimiter);
```

### FastAPI Per-Endpoint Rate Limiting

```python
from fastapi import FastAPI
from slowapi import Limiter

app = FastAPI()

# Different limits for different endpoints
api_limiter = Limiter(key_func=lambda r: r.client.host, rate="100/15minute")
upload_limiter = Limiter(key_func=lambda r: r.client.host, rate="10/1hour")

@app.get("/api/users")
@api_limiter.limit("100/15minute")
async def get_users():
    return {"users": []}

@app.post("/upload")
@upload_limiter.limit("10/1hour")
async def upload_file():
    return {"status": "uploaded"}
```

---

## Quota Management

### Daily Quota

```typescript
interface UserQuota {
  userId: string;
  dailyLimit: number;
  used: number;
  resetAt: Date;
}

const quotas = new Map<string, UserQuota>();

function checkQuota(userId: string, cost: number = 1): boolean {
  const quota = quotas.get(userId);

  if (!quota || new Date() > quota.resetAt) {
    quotas.set(userId, {
      userId,
      dailyLimit: 1000,
      used: 0,
      resetAt: new Date(new Date().setHours(24, 0, 0, 0)),
    });
    return true;
  }

  if (quota.used + cost > quota.dailyLimit) {
    return false;
  }

  quota.used += cost;
  return true;
}

// Express middleware
function quotaMiddleware(req: any, res: any, next: any) {
  const userId = req.user?.id;
  const cost = getQuotaCost(req.path);

  if (!checkQuota(userId, cost)) {
    return res.status(429).json({
      error: 'Quota exceeded',
      remaining: quotas.get(userId)?.dailyLimit - quotas.get(userId)?.used,
    });
  }

  next();
}
```

### Monthly Quota

```typescript
function checkMonthlyQuota(userId: string, cost: number = 1): boolean {
  const now = new Date();
  const monthStart = new Date(now.getFullYear(), now.getMonth(), 1);
  const monthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 0);

  const quota = quotas.get(userId);

  if (!quota || now > quota.resetAt) {
    quotas.set(userId, {
      userId,
      monthlyLimit: 10000,
      used: 0,
      resetAt: monthEnd,
    });
    return true;
  }

  if (quota.used + cost > quota.monthlyLimit) {
    return false;
  }

  quota.used += cost;
  return true;
}
```

---

## Response Headers

### Standard Rate Limit Headers

```typescript
function setRateLimitHeaders(res: any, remaining: number, reset: number) {
  res.setHeader('X-RateLimit-Limit', '100');
  res.setHeader('X-RateLimit-Remaining', remaining.toString());
  res.setHeader('X-RateLimit-Reset', new Date(reset * 1000).toUTCString());
}

// Express middleware
function rateLimitMiddleware(req: any, res: any, next: any) {
  const key = req.ip;
  const { allowed, remaining, reset } = checkRateLimit(key);

  setRateLimitHeaders(res, remaining, reset);

  if (!allowed) {
    return res.status(429).json({
      error: 'Too many requests',
    });
  }

  next();
}
```

### Retry-After Header

```typescript
function setRetryAfter(res: any, retryAfter: number) {
  res.setHeader('Retry-After', retryAfter.toString());
}

// Express middleware
function rateLimitMiddleware(req: any, res: any, next: any) {
  const key = req.ip;
  const { allowed, retryAfter } = checkRateLimit(key);

  if (!allowed) {
    setRetryAfter(res, retryAfter);
    return res.status(429).json({
      error: 'Too many requests',
    });
  }

  next();
}
```

---

## Error Handling

### Rate Limit Error Response

```typescript
class RateLimitError extends Error {
  constructor(
    public retryAfter: number,
    public limit: number,
    public remaining: number,
    public reset: number
  ) {
    super('Rate limit exceeded');
    this.name = 'RateLimitError';
  }
}

function handleRateLimitError(error: Error, req: any, res: any, next: any) {
  if (error instanceof RateLimitError) {
    return res.status(429).json({
      error: 'Rate limit exceeded',
      retryAfter: error.retryAfter,
      limit: error.limit,
      remaining: error.remaining,
      reset: error.reset,
    });
  }

  next(error);
}
```

### FastAPI Rate Limit Error

```python
from fastapi import FastAPI, HTTPException
from slowapi import Limiter, _rate_limit_exceeded_handler

app = FastAPI()

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "detail": exc.detail,
            "retry_after": exc.retry_after
        }
    )
```

---

## Distributed Rate Limiting

### Redis-Based Rate Limiting

```typescript
import { createClient } from 'redis';
import rateLimit from 'express-rate-limit-redis';

const redisClient = createClient({ url: process.env.REDIS_URL });

const limiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'ratelimit:',
  }),
  windowMs: 15 * 60 * 1000,
  max: 100,
});

app.use(limiter);
```

### Memcached-Based Rate Limiting

```typescript
import Memcached from 'memcached';
import rateLimit from 'express-rate-limit-memcached';

const memcached = new Memcached('localhost:11211');

const limiter = rateLimit({
  store: new MemcachedStore(memcached),
  windowMs: 15 * 60 * 1000,
  max: 100,
});

app.use(limiter);
```

---

## Testing

### Unit Testing Rate Limiting

```typescript
import { TokenBucket } from './rateLimiter';

describe('TokenBucket', () => {
  it('should allow requests within capacity', () => {
    const bucket = new TokenBucket(100, 10);

    for (let i = 0; i < 100; i++) {
      expect(bucket.tryConsume()).toBe(true);
    }
  });

  it('should reject requests over capacity', () => {
    const bucket = new TokenBucket(100, 10);

    for (let i = 0; i < 100; i++) {
      bucket.tryConsume();
    }

    expect(bucket.tryConsume()).toBe(false);
  });

  it('should refill tokens over time', async () => {
    const bucket = new TokenBucket(100, 10);

    // Consume all tokens
    for (let i = 0; i < 100; i++) {
      bucket.tryConsume();
    }

    expect(bucket.tryConsume()).toBe(false);

    // Wait for refill
    await new Promise(resolve => setTimeout(resolve, 2000));

    expect(bucket.tryConsume()).toBe(true);
  });
});
```

### Integration Testing Rate Limiting

```typescript
import request from 'supertest';
import { app } from '../app';

describe('Rate Limiting', () => {
  it('should allow requests under limit', async () => {
    const response = await request(app).get('/api/users');
    expect(response.status).toBe(200);
  });

  it('should reject requests over limit', async () => {
    // Send 101 requests
    for (let i = 0; i < 101; i++) {
      await request(app).get('/api/users');
    }

    const response = await request(app).get('/api/users');
    expect(response.status).toBe(429);
    expect(response.body.error).toBe('Too many requests');
  });
});
```

---

## Best Practices

### 1. Use Appropriate Rate Limits

```typescript
// Set appropriate limits based on endpoint
const apiLimiter = rateLimit({ max: 100, windowMs: 60000 }); // 100 req/min
const uploadLimiter = rateLimit({ max: 10, windowMs: 3600000 }); // 10 req/hour
const authLimiter = rateLimit({ max: 5, windowMs: 60000 }); // 5 req/min
```

### 2. Use Consistent Key Generation

```typescript
// Use consistent keys for rate limiting
const keyGenerator = (req) => {
  return `${req.ip}:${req.path}`;
};
```

### 3. Set Appropriate Headers

```typescript
// Set standard rate limit headers
res.setHeader('X-RateLimit-Limit', limit.toString());
res.setHeader('X-RateLimit-Remaining', remaining.toString());
res.setHeader('X-RateLimit-Reset', reset.toString());
res.setHeader('Retry-After', retryAfter.toString());
```

### 4. Use Distributed Storage

```typescript
// Use Redis for distributed rate limiting
const limiter = rateLimit({
  store: new RedisStore({ client: redisClient }),
});
```

### 5. Handle Rate Limit Errors Gracefully

```typescript
// Return helpful error messages
res.status(429).json({
  error: 'Too many requests',
  message: 'Please try again later',
  retryAfter: 60,
});
```

### 6. Monitor Rate Limiting

```typescript
// Track rate limit violations
metrics.record('rate_limit_violations', 1, {
  ip: req.ip,
  endpoint: req.path,
});
```

### 7. Test Rate Limiting

```typescript
// Write tests for rate limiting
describe('Rate Limiting', () => {
  it('should enforce limits', async () => {
    // Test implementation
  });
});
```

### 8. Document Rate Limits

```markdown
# Rate Limits

## API Endpoints

| Endpoint | Limit | Window |
|----------|-------|---------|
| GET /api/users | 100 | 15 minutes |
| POST /api/users | 10 | 15 minutes |
| POST /upload | 5 | 1 hour |
```

### 9. Use Different Limits for Different Tiers

```typescript
// Different limits for different user tiers
const getRateLimit = (user: any) => {
  if (user.tier === 'premium') {
    return { max: 1000, windowMs: 60000 };
  } else if (user.tier === 'standard') {
    return { max: 100, windowMs: 60000 };
  } else {
    return { max: 10, windowMs: 60000 };
  }
};
```

### 10. Consider Burst Traffic

```typescript
// Allow bursts within reason
const limiter = rateLimit({
  max: 100, // Allow bursts up to 100
  windowMs: 60000, // Over 1 minute
  skipFailedRequests: true, // Don't count failed requests
});
```

---

## Resources

- [express-rate-limit](https://github.com/nfriedly/express-rate-limit)
- [slowapi](https://slowapi.readthedocs.io/)
- [Redis Rate Limiting](https://redis.io/docs/manual/patterns/distributed-rate-limiting-pattern/)
- [Rate Limiting Algorithms](https://en.wikipedia.org/wiki/Rate_limiting)
