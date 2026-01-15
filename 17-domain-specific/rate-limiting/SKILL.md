# Rate Limiting

## Overview

Rate limiting controls the rate of incoming requests to protect your API from abuse and ensure fair usage. This skill covers rate limiting algorithms, implementation with Express rate-limit, Redis-based rate limiting, NGINX rate limiting, per-user limits, per-endpoint limits, quota management, response headers, error handling, distributed rate limiting, testing, and best practices.

## Table of Contents

1. [Rate Limiting Algorithms](#rate-limiting-algorithms)
2. [Implementation](#implementation)
   - [Express Rate-Limit](#express-rate-limit)
   - [Redis-Based](#redis-based)
   - [NGINX](#nginx)
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

### Token Bucket Algorithm

```typescript
// src/rate-limiting/token-bucket.ts
interface TokenBucketConfig {
  capacity: number;  // Maximum tokens
  refillRate: number;  // Tokens per second
}

class TokenBucket {
  private tokens: number;
  private lastRefill: number;

  constructor(private config: TokenBucketConfig) {
    this.tokens = config.capacity;
    this.lastRefill = Date.now();
  }

  consume(tokens: number = 1): boolean {
    this.refill();

    if (this.tokens >= tokens) {
      this.tokens -= tokens;
      return true;
    }

    return false;
  }

  private refill(): void {
    const now = Date.now();
    const elapsed = (now - this.lastRefill) / 1000;  // Convert to seconds
    const tokensToAdd = elapsed * this.config.refillRate;

    this.tokens = Math.min(this.config.capacity, this.tokens + tokensToAdd);
    this.lastRefill = now;
  }

  getAvailableTokens(): number {
    this.refill();
    return this.tokens;
  }
}

// Usage
const bucket = new TokenBucket({ capacity: 10, refillRate: 5 });

if (bucket.consume()) {
  // Request allowed
} else {
  // Rate limit exceeded
}
```

### Leaky Bucket Algorithm

```typescript
// src/rate-limiting/leaky-bucket.ts
interface LeakyBucketConfig {
  capacity: number;  // Maximum requests in bucket
  leakRate: number;  // Requests per second
}

class LeakyBucket {
  private queue: number[] = [];
  private lastLeak: number = Date.now();

  constructor(private config: LeakyBucketConfig) {}

  tryAdd(): boolean {
    this.leak();

    if (this.queue.length < this.config.capacity) {
      this.queue.push(Date.now());
      return true;
    }

    return false;
  }

  private leak(): void {
    const now = Date.now();
    const elapsed = (now - this.lastLeak) / 1000;  // Convert to seconds
    const toLeak = Math.floor(elapsed * this.config.leakRate);

    this.queue = this.queue.slice(toLeak);
    this.lastLeak = now;
  }

  getQueueSize(): number {
    this.leak();
    return this.queue.length;
  }
}

// Usage
const bucket = new LeakyBucket({ capacity: 10, leakRate: 5 });

if (bucket.tryAdd()) {
  // Request allowed
} else {
  // Rate limit exceeded
}
```

### Fixed Window Algorithm

```typescript
// src/rate-limiting/fixed-window.ts
interface FixedWindowConfig {
  maxRequests: number;
  windowMs: number;
}

class FixedWindowRateLimiter {
  private requests: Map<string, number[]> = new Map();

  constructor(private config: FixedWindowConfig) {}

  isAllowed(identifier: string): boolean {
    const now = Date.now();
    const windowStart = now - this.config.windowMs;

    // Get existing requests for this identifier
    let requests = this.requests.get(identifier) || [];

    // Remove requests outside the current window
    requests = requests.filter(timestamp => timestamp > windowStart);

    // Check if under limit
    if (requests.length < this.config.maxRequests) {
      requests.push(now);
      this.requests.set(identifier, requests);
      return true;
    }

    return false;
  }

  reset(identifier: string): void {
    this.requests.delete(identifier);
  }

  resetAll(): void {
    this.requests.clear();
  }
}

// Usage
const limiter = new FixedWindowRateLimiter({
  maxRequests: 100,
  windowMs: 60000,  // 1 minute
});

if (limiter.isAllowed('user123')) {
  // Request allowed
} else {
  // Rate limit exceeded
}
```

### Sliding Window Algorithm

```typescript
// src/rate-limiting/sliding-window.ts
interface SlidingWindowConfig {
  maxRequests: number;
  windowMs: number;
}

class SlidingWindowRateLimiter {
  private requests: Map<string, number[]> = new Map();

  constructor(private config: SlidingWindowConfig) {}

  isAllowed(identifier: string): boolean {
    const now = Date.now();
    const windowStart = now - this.config.windowMs;

    // Get existing requests for this identifier
    let requests = this.requests.get(identifier) || [];

    // Remove requests outside the current window
    requests = requests.filter(timestamp => timestamp > windowStart);

    // Check if under limit
    if (requests.length < this.config.maxRequests) {
      requests.push(now);
      this.requests.set(identifier, requests);
      return true;
    }

    return false;
  }

  getRemainingRequests(identifier: string): number {
    const now = Date.now();
    const windowStart = now - this.config.windowMs;

    let requests = this.requests.get(identifier) || [];
    requests = requests.filter(timestamp => timestamp > windowStart);

    return Math.max(0, this.config.maxRequests - requests.length);
  }

  getResetTime(identifier: string): number {
    const requests = this.requests.get(identifier) || [];
    
    if (requests.length === 0) {
      return Date.now();
    }

    const oldestRequest = requests[0];
    return oldestRequest + this.config.windowMs;
  }
}

// Usage
const limiter = new SlidingWindowRateLimiter({
  maxRequests: 100,
  windowMs: 60000,  // 1 minute
});

if (limiter.isAllowed('user123')) {
  // Request allowed
} else {
  // Rate limit exceeded
  console.log(`Reset at: ${new Date(limiter.getResetTime('user123'))}`);
}
```

---

## Implementation

### Express Rate-Limit

#### Installation

```bash
npm install express-rate-limit
```

#### Basic Usage

```typescript
// src/middleware/rate-limit.middleware.ts
import rateLimit from 'express-rate-limit';
import { Request, Response } from 'express';

export const apiRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,  // Limit each IP to 100 requests per windowMs
  message: {
    error: 'Too many requests from this IP, please try again later.',
  },
  standardHeaders: true,  // Return rate limit info in the `RateLimit-*` headers
  legacyHeaders: false,  // Disable the `X-RateLimit-*` headers
  handler: (req: Request, res: Response) => {
    res.status(429).json({
      error: 'Too many requests',
      retryAfter: Math.ceil(15 * 60),  // 15 minutes in seconds
    });
  },
});

export const authRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5,  // Limit each IP to 5 requests per windowMs
  message: {
    error: 'Too many authentication attempts, please try again later.',
  },
  skipSuccessfulRequests: true,  // Don't count successful requests
});
```

#### Using in Express

```typescript
// src/app.ts
import express from 'express';
import { apiRateLimiter, authRateLimiter } from './middleware/rate-limit.middleware';

const app = express();

// Apply rate limiter to all routes
app.use('/api', apiRateLimiter);

// Apply stricter rate limiter to auth routes
app.use('/api/auth', authRateLimiter);

app.post('/api/auth/login', (req, res) => {
  res.json({ token: 'example-token' });
});

app.get('/api/users', (req, res) => {
  res.json({ users: [] });
});
```

### Redis-Based

#### Installation

```bash
npm install ioredis
npm install @types/ioredis
```

#### Redis Rate Limiter

```typescript
// src/rate-limiting/redis-rate-limiter.ts
import Redis from 'ioredis';

interface RedisRateLimiterConfig {
  maxRequests: number;
  windowMs: number;
  prefix?: string;
}

class RedisRateLimiter {
  constructor(
    private redis: Redis,
    private config: RedisRateLimiterConfig
  ) {}

  async isAllowed(identifier: string): Promise<{ allowed: boolean; remaining: number; reset: number }> {
    const key = this.config.prefix ? `${this.config.prefix}:${identifier}` : identifier;
    const now = Date.now();
    const windowStart = now - this.config.windowMs;

    const pipeline = this.redis.pipeline();

    // Remove expired entries
    pipeline.zremrangebyscore(key, 0, windowStart);

    // Count current requests
    pipeline.zcard(key);

    // Add current request
    pipeline.zadd(key, now, `${now}-${Math.random()}`);

    // Set expiry
    pipeline.expire(key, Math.ceil(this.config.windowMs / 1000));

    const results = await pipeline.exec();

    if (!results) {
      throw new Error('Redis pipeline failed');
    }

    const count = results[1][1] as number;
    const allowed = count <= this.config.maxRequests;
    const remaining = Math.max(0, this.config.maxRequests - count);
    const reset = now + this.config.windowMs;

    return { allowed, remaining, reset };
  }

  async reset(identifier: string): Promise<void> {
    const key = this.config.prefix ? `${this.config.prefix}:${identifier}` : identifier;
    await this.redis.del(key);
  }
}

// Usage
const redis = new Redis();
const limiter = new RedisRateLimiter(redis, {
  maxRequests: 100,
  windowMs: 60000,  // 1 minute
  prefix: 'rate-limit',
});

// Middleware
export const redisRateLimiter = async (req: any, res: any, next: any) => {
  const identifier = req.ip || req.user?.id || 'anonymous';
  const result = await limiter.isAllowed(identifier);

  res.setHeader('X-RateLimit-Limit', limiter['config'].maxRequests);
  res.setHeader('X-RateLimit-Remaining', result.remaining);
  res.setHeader('X-RateLimit-Reset', new Date(result.reset).toISOString());

  if (!result.allowed) {
    return res.status(429).json({
      error: 'Too many requests',
      retryAfter: Math.ceil((result.reset - Date.now()) / 1000),
    });
  }

  next();
};
```

### NGINX

#### Basic Rate Limiting

```nginx
# /etc/nginx/nginx.conf

http {
    # Define rate limit zone
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=1r/s;

    server {
        listen 80;
        server_name api.example.com;

        # Apply rate limiting to all API routes
        location /api/ {
            limit_req zone=api_limit burst=20 nodelay;
            
            proxy_pass http://backend;
        }

        # Apply stricter rate limiting to auth routes
        location /api/auth/ {
            limit_req zone=auth_limit burst=5 nodelay;
            
            proxy_pass http://backend;
        }
    }
}
```

#### Advanced Rate Limiting

```nginx
# /etc/nginx/nginx.conf

http {
    # Multiple rate limit zones
    limit_req_zone $binary_remote_addr zone=general_limit:10m rate=100r/m;
    limit_req_zone $binary_remote_addr zone=auth_limit:10m rate=5r/m;
    limit_req_zone $binary_remote_addr zone=upload_limit:10m rate=10r/m;

    # Connection limit
    limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

    server {
        listen 80;
        server_name api.example.com;

        # General API rate limiting
        location /api/ {
            limit_req zone=general_limit burst=20 nodelay;
            limit_conn conn_limit 10;
            
            proxy_pass http://backend;
        }

        # Auth rate limiting
        location /api/auth/ {
            limit_req zone=auth_limit burst=2 nodelay;
            
            proxy_pass http://backend;
        }

        # Upload rate limiting
        location /api/upload {
            limit_req zone=upload_limit burst=5 nodelay;
            client_max_body_size 10M;
            
            proxy_pass http://backend;
        }
    }
}
```

---

## Per-User Limits

```typescript
// src/middleware/user-rate-limit.middleware.ts
import rateLimit from 'express-rate-limit';
import { Request } from 'express';

// Create a rate limiter that uses user ID instead of IP
export const userRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,  // Limit each user to 100 requests per windowMs
  keyGenerator: (req: Request) => {
    // Use user ID if authenticated, otherwise use IP
    return (req as any).user?.id || req.ip;
  },
  message: {
    error: 'Too many requests, please try again later.',
  },
});

// Different limits for different user tiers
export const tieredRateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: (req: Request) => {
    const user = (req as any).user;
    
    switch (user?.tier) {
      case 'premium':
        return 1000;
      case 'standard':
        return 100;
      case 'basic':
      default:
        return 50;
    }
  },
  keyGenerator: (req: Request) => {
    return (req as any).user?.id || req.ip;
  },
});
```

---

## Per-Endpoint Limits

```typescript
// src/middleware/endpoint-rate-limit.middleware.ts
import rateLimit from 'express-rate-limit';

// Different rate limits for different endpoints
export const createEndpointLimiter = (maxRequests: number, windowMs: number) => {
  return rateLimit({
    windowMs,
    max: maxRequests,
    message: {
      error: `Too many requests for this endpoint, limit is ${maxRequests} per ${windowMs / 1000} seconds.`,
    },
  });
};

// Usage in routes
import express from 'express';
import { createEndpointLimiter } from './middleware/endpoint-rate-limit.middleware';

const router = express.Router();

// Strict rate limit for auth endpoints
router.post('/login', createEndpointLimiter(5, 15 * 60 * 1000), (req, res) => {
  res.json({ token: 'example-token' });
});

// Moderate rate limit for user endpoints
router.get('/users', createEndpointLimiter(100, 15 * 60 * 1000), (req, res) => {
  res.json({ users: [] });
});

// Lenient rate limit for public endpoints
router.get('/public', createEndpointLimiter(1000, 15 * 60 * 1000), (req, res) => {
  res.json({ message: 'Hello' });
});
```

---

## Quota Management

```typescript
// src/rate-limiting/quota-manager.ts
import Redis from 'ioredis';

interface QuotaConfig {
  dailyLimit: number;
  monthlyLimit: number;
}

class QuotaManager {
  constructor(
    private redis: Redis,
    private config: QuotaConfig
  ) {}

  async checkDailyQuota(userId: string): Promise<{ allowed: boolean; remaining: number; reset: number }> {
    const today = new Date().toISOString().split('T')[0];
    const key = `quota:daily:${userId}:${today}`;
    
    const current = await this.redis.incr(key);
    await this.redis.expire(key, 86400);  // 24 hours

    const remaining = Math.max(0, this.config.dailyLimit - current);
    const reset = new Date();
    reset.setDate(reset.getDate() + 1);
    reset.setHours(0, 0, 0, 0);

    return {
      allowed: current <= this.config.dailyLimit,
      remaining,
      reset: reset.getTime(),
    };
  }

  async checkMonthlyQuota(userId: string): Promise<{ allowed: boolean; remaining: number; reset: number }> {
    const now = new Date();
    const month = now.toISOString().slice(0, 7);  // YYYY-MM
    const key = `quota:monthly:${userId}:${month}`;
    
    const current = await this.redis.incr(key);
    
    // Set expiry to end of month
    const endOfMonth = new Date(now.getFullYear(), now.getMonth() + 1, 0);
    const ttl = Math.floor((endOfMonth.getTime() - now.getTime()) / 1000);
    await this.redis.expire(key, ttl);

    const remaining = Math.max(0, this.config.monthlyLimit - current);
    const reset = endOfMonth.getTime();

    return {
      allowed: current <= this.config.monthlyLimit,
      remaining,
      reset,
    };
  }

  async resetDailyQuota(userId: string): Promise<void> {
    const today = new Date().toISOString().split('T')[0];
    const key = `quota:daily:${userId}:${today}`;
    await this.redis.del(key);
  }

  async resetMonthlyQuota(userId: string): Promise<void> {
    const now = new Date();
    const month = now.toISOString().slice(0, 7);
    const key = `quota:monthly:${userId}:${month}`;
    await this.redis.del(key);
  }
}

// Usage
const redis = new Redis();
const quotaManager = new QuotaManager(redis, {
  dailyLimit: 1000,
  monthlyLimit: 30000,
});

// Middleware
export const quotaMiddleware = async (req: any, res: any, next: any) => {
  const userId = (req as any).user?.id;
  
  if (!userId) {
    return next();
  }

  const dailyQuota = await quotaManager.checkDailyQuota(userId);
  const monthlyQuota = await quotaManager.checkMonthlyQuota(userId);

  res.setHeader('X-Quota-Daily-Limit', 1000);
  res.setHeader('X-Quota-Daily-Remaining', dailyQuota.remaining);
  res.setHeader('X-Quota-Daily-Reset', new Date(dailyQuota.reset).toISOString());
  res.setHeader('X-Quota-Monthly-Limit', 30000);
  res.setHeader('X-Quota-Monthly-Remaining', monthlyQuota.remaining);
  res.setHeader('X-Quota-Monthly-Reset', new Date(monthlyQuota.reset).toISOString());

  if (!dailyQuota.allowed) {
    return res.status(429).json({
      error: 'Daily quota exceeded',
      retryAfter: Math.ceil((dailyQuota.reset - Date.now()) / 1000),
    });
  }

  if (!monthlyQuota.allowed) {
    return res.status(429).json({
      error: 'Monthly quota exceeded',
      retryAfter: Math.ceil((monthlyQuota.reset - Date.now()) / 1000),
    });
  }

  next();
};
```

---

## Response Headers

```typescript
// src/middleware/rate-limit-headers.middleware.ts
import { Request, Response, NextFunction } from 'express';

export function addRateLimitHeaders(
  limit: number,
  remaining: number,
  reset: number
) {
  return (req: Request, res: Response, next: NextFunction) => {
    res.setHeader('X-RateLimit-Limit', limit);
    res.setHeader('X-RateLimit-Remaining', remaining);
    res.setHeader('X-RateLimit-Reset', new Date(reset).toISOString());
    res.setHeader('Retry-After', Math.ceil((reset - Date.now()) / 1000));
    next();
  };
}

// Usage with express-rate-limit
import rateLimit from 'express-rate-limit';

export const rateLimiterWithHeaders = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,  // Automatically adds RateLimit-* headers
  legacyHeaders: false,
});
```

---

## Error Handling

```typescript
// src/middleware/rate-limit-error.middleware.ts
import { Request, Response, NextFunction } from 'express';

export class RateLimitError extends Error {
  constructor(
    message: string,
    public retryAfter: number
  ) {
    super(message);
    this.name = 'RateLimitError';
  }
}

export function handleRateLimitError(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  if (err instanceof RateLimitError) {
    return res.status(429).json({
      error: err.message,
      retryAfter: err.retryAfter,
    });
  }

  next(err);
}

// Custom rate limiter with error handling
import rateLimit from 'express-rate-limit';

export const rateLimiterWithErrorHandling = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  handler: (req: Request, res: Response) => {
    const retryAfter = 15 * 60;  // 15 minutes
    throw new RateLimitError('Too many requests', retryAfter);
  },
});
```

---

## Distributed Rate Limiting

```typescript
// src/rate-limiting/distributed-rate-limiter.ts
import Redis from 'ioredis';
import { Cluster } from 'ioredis';

interface DistributedRateLimiterConfig {
  maxRequests: number;
  windowMs: number;
  prefix?: string;
  keyPrefix?: string;
}

class DistributedRateLimiter {
  constructor(
    private redis: Redis | Cluster,
    private config: DistributedRateLimiterConfig
  ) {}

  async isAllowed(identifier: string): Promise<{ allowed: boolean; remaining: number; reset: number }> {
    const key = this.buildKey(identifier);
    const now = Date.now();
    const windowStart = now - this.config.windowMs;

    // Use Redis Lua script for atomic operations
    const script = `
      local key = KEYS[1]
      local now = tonumber(ARGV[1])
      local windowStart = tonumber(ARGV[2])
      local maxRequests = tonumber(ARGV[3])
      local windowMs = tonumber(ARGV[4])
      
      -- Remove expired entries
      redis.call('ZREMRANGEBYSCORE', key, 0, windowStart)
      
      -- Count current requests
      local count = redis.call('ZCARD', key)
      
      -- Check if under limit
      if count < maxRequests then
        -- Add current request
        redis.call('ZADD', key, now, now .. '-' .. math.random())
        
        -- Set expiry
        redis.call('EXPIRE', key, math.ceil(windowMs / 1000))
        
        return {1, maxRequests - count - 1, now + windowMs}
      else
        return {0, 0, now + windowMs}
      end
    `;

    const results = await this.redis.eval(
      script,
      1,
      key,
      now,
      windowStart,
      this.config.maxRequests,
      this.config.windowMs
    ) as [number, number, number];

    return {
      allowed: results[0] === 1,
      remaining: results[1],
      reset: results[2],
    };
  }

  private buildKey(identifier: string): string {
    const parts = [];
    
    if (this.config.keyPrefix) {
      parts.push(this.config.keyPrefix);
    }
    
    if (this.config.prefix) {
      parts.push(this.config.prefix);
    }
    
    parts.push(identifier);
    
    return parts.join(':');
  }
}

// Usage with Redis Cluster
const redisCluster = new Cluster([
  { host: 'redis1.example.com', port: 6379 },
  { host: 'redis2.example.com', port: 6379 },
  { host: 'redis3.example.com', port: 6379 },
]);

const distributedLimiter = new DistributedRateLimiter(redisCluster, {
  maxRequests: 100,
  windowMs: 60000,
  prefix: 'rate-limit',
  keyPrefix: 'api',
});
```

---

## Testing

```typescript
// test/rate-limit.test.ts
import { describe, it, beforeEach, afterEach } from '@jest/globals';
import request from 'supertest';
import app from '../src/app';

describe('Rate Limiting', () => {
  beforeEach(() => {
    // Reset rate limiter before each test
  });

  afterEach(() => {
    // Clean up after each test
  });

  it('should allow requests under the limit', async () => {
    const response = await request(app)
      .get('/api/users')
      .expect(200);

    expect(response.headers['x-ratelimit-limit']).toBeDefined();
    expect(response.headers['x-ratelimit-remaining']).toBeDefined();
  });

  it('should block requests over the limit', async () => {
    // Make requests up to the limit
    for (let i = 0; i < 100; i++) {
      await request(app).get('/api/users');
    }

    // Next request should be blocked
    const response = await request(app)
      .get('/api/users')
      .expect(429);

    expect(response.body.error).toContain('Too many requests');
    expect(response.headers['retry-after']).toBeDefined();
  });

  it('should use different limits for different endpoints', async () => {
    // Login endpoint has stricter limit
    for (let i = 0; i < 5; i++) {
      await request(app).post('/api/auth/login');
    }

    // Next login request should be blocked
    await request(app)
      .post('/api/auth/login')
      .expect(429);

    // Other endpoints should still work
    await request(app)
      .get('/api/users')
      .expect(200);
  });

  it('should respect per-user limits', async () => {
    const user1Token = 'token1';
    const user2Token = 'token2';

    // User 1 makes requests up to limit
    for (let i = 0; i < 100; i++) {
      await request(app)
        .get('/api/users')
        .set('Authorization', `Bearer ${user1Token}`);
    }

    // User 1 should be blocked
    await request(app)
      .get('/api/users')
      .set('Authorization', `Bearer ${user1Token}`)
      .expect(429);

    // User 2 should still be allowed
    await request(app)
      .get('/api/users')
      .set('Authorization', `Bearer ${user2Token}`)
      .expect(200);
  });
});
```

---

## Best Practices

### 1. Use Appropriate Limits

```typescript
// Good: Appropriate limits for different endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,  // Stricter for auth
});

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,  // Moderate for API
});

const publicLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 1000,  // Lenient for public
});

// Bad: Same limit for all endpoints
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
});
```

### 2. Use Redis for Distributed Systems

```typescript
// Good: Use Redis for distributed rate limiting
const redisLimiter = new RedisRateLimiter(redis, {
  maxRequests: 100,
  windowMs: 60000,
});

// Bad: Use in-memory limiter for distributed systems
const memoryLimiter = new FixedWindowRateLimiter({
  maxRequests: 100,
  windowMs: 60000,
});
```

### 3. Provide Clear Error Messages

```typescript
// Good: Clear error messages with retry information
export const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  handler: (req: Request, res: Response) => {
    res.status(429).json({
      error: 'Too many requests from this IP, please try again later.',
      retryAfter: 15 * 60,  // 15 minutes
    });
  },
});

// Bad: Generic error message
export const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  handler: (req: Request, res: Response) => {
    res.status(429).json({ error: 'Too many requests' });
  },
});
```

### 4. Include Rate Limit Headers

```typescript
// Good: Include rate limit headers
export const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: true,
  legacyHeaders: false,
});

// Bad: No rate limit headers
export const rateLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  standardHeaders: false,
});
```

### 5. Test Rate Limiting

```typescript
// Good: Test rate limiting
describe('Rate Limiting', () => {
  it('should block requests over the limit', async () => {
    for (let i = 0; i < 100; i++) {
      await request(app).get('/api/users');
    }

    await request(app)
      .get('/api/users')
      .expect(429);
  });
});

// Bad: No tests for rate limiting
```

---

## Summary

This skill covers comprehensive rate limiting implementation patterns including:

- **Rate Limiting Algorithms**: Token bucket, leaky bucket, fixed window, sliding window
- **Implementation**: Express rate-limit, Redis-based, NGINX
- **Per-User Limits**: User-based rate limiting, tiered limits
- **Per-Endpoint Limits**: Different limits for different endpoints
- **Quota Management**: Daily and monthly quota tracking
- **Response Headers**: Rate limit headers, retry information
- **Error Handling**: Custom error handling, error responses
- **Distributed Rate Limiting**: Redis cluster, Lua scripts
- **Testing**: Testing rate limiting behavior
- **Best Practices**: Appropriate limits, Redis for distributed systems, clear messages, headers, testing
