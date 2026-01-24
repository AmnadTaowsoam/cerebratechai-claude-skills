---
name: Caching Strategies
description: Multi-layer caching patterns: in-memory (Redis/Memcached), CDN, HTTP caching, cache invalidation, cache warming, and cache stampede prevention
---

# Caching Strategies

## Overview

Multi-layer caching ใช้เพื่อลด load บน database/external services และปรับปรุง performance ครอบคลุม in-memory cache, CDN, HTTP caching, cache invalidation, และ cache stampede prevention

## Why This Matters

- **Performance**: ลด latency อย่างมีนัยสำคัญ
- **Scalability**: ลด load บน backend services
- **Cost reduction**: ลด database queries และ external API calls
- **User experience**: Response เร็วขึ้น = UX ดีขึ้น

---

## Core Concepts

### 1. Cache Layers

```typescript
// Multi-layer cache architecture
interface CacheLayer {
  get<T>(key: string): Promise<T | null>
  set<T>(key: string, value: T, ttl?: number): Promise<void>
  del(key: string): Promise<void>
}

class MultiLayerCache {
  private layers: CacheLayer[]

  constructor(layers: CacheLayer[]) {
    this.layers = layers // [memory, redis, cdn]
  }

  async get<T>(key: string): Promise<T | null> {
    // Check each layer from fastest to slowest
    for (const layer of this.layers) {
      const value = await layer.get<T>(key)
      if (value !== null) {
        // Promote to faster layers
        await this.promote(key, value, layer)
        return value
      }
    }
    return null
  }

  async set<T>(key: string, value: T, ttl?: number): Promise<void> {
    // Set in all layers
    await Promise.all(
      this.layers.map(layer => layer.set(key, value, ttl))
    )
  }

  private async promote<T>(
    key: string,
    value: T,
    sourceLayer: CacheLayer
  ): Promise<void> {
    // Promote to faster layers
    for (const layer of this.layers) {
      if (layer === sourceLayer) break
      await layer.set(key, value)
    }
  }
}

// Usage
const cache = new MultiLayerCache([
  new MemoryCache(),
  new RedisCache(),
  new CDNCache()
])
```

### 2. Redis Caching

```typescript
import { Redis } from 'ioredis'

class RedisCache implements CacheLayer {
  private client: Redis

  constructor() {
    this.client = new Redis({
      host: process.env.REDIS_HOST,
      port: parseInt(process.env.REDIS_PORT || '6379'),
      password: process.env.REDIS_PASSWORD,
    })
  }

  async get<T>(key: string): Promise<T | null> {
    const value = await this.client.get(key)
    return value ? JSON.parse(value) : null
  }

  async set<T>(key: string, value: T, ttl = 3600): Promise<void> {
    await this.client.setex(
      key,
      ttl,
      JSON.stringify(value)
    )
  }

  async del(key: string): Promise<void> {
    await this.client.del(key)
  }

  // Get multiple keys at once (mget)
  async mget<T>(keys: string[]): Promise<(T | null)[]> {
    const values = await this.client.mget(keys)
    return values.map(v => v ? JSON.parse(v) : null)
  }

  // Set multiple keys at once (mset)
  async mset<T>(items: Record<string, T>, ttl = 3600): Promise<void> {
    const pipeline = this.client.pipeline()
    for (const [key, value] of Object.entries(items)) {
      pipeline.setex(key, ttl, JSON.stringify(value))
    }
    await pipeline.exec()
  }
}
```

### 3. HTTP Caching

```typescript
// Server-side HTTP caching headers
function setCacheHeaders(res: Response, options: {
  maxAge?: number
  staleWhileRevalidate?: number
  staleIfError?: number
  mustRevalidate?: boolean
  private?: boolean
}) {
  const directives: string[] = []

  if (options.private) {
    directives.push('private')
  } else {
    directives.push('public')
  }

  if (options.maxAge !== undefined) {
    directives.push(`max-age=${options.maxAge}`)
  }

  if (options.staleWhileRevalidate) {
    directives.push(`stale-while-revalidate=${options.staleWhileRevalidate}`)
  }

  if (options.staleIfError) {
    directives.push(`stale-if-error=${options.staleIfError}`)
  }

  if (options.mustRevalidate) {
    directives.push('must-revalidate')
  }

  res.setHeader('Cache-Control', directives.join(', '))

  // Add ETag for conditional requests
  const etag = generateETag(res.body)
  res.setHeader('ETag', etag)
}

// Usage in Express
app.get('/api/users/:id', async (req, res) => {
  const user = await getUser(req.params.id)

  // Cache for 5 minutes, allow stale for 1 hour
  setCacheHeaders(res, {
    maxAge: 300,
    staleWhileRevalidate: 3600,
    public: true,
  })

  res.json(user)
})

// Client-side caching with Service Worker
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      if (response) {
        // Return cached response
        return response
      }

      // Fetch from network and cache
      return fetch(event.request).then((response) => {
        const clonedResponse = response.clone()
        caches.open('api-cache').then((cache) => {
          cache.put(event.request, clonedResponse)
        })
        return response
      })
    })
  )
})
```

### 4. Cache Invalidation

```typescript
// Cache invalidation strategies
class CacheInvalidator {
  private cache: CacheLayer
  private invalidationQueue: Queue

  constructor(cache: CacheLayer) {
    this.cache = cache
    this.invalidationQueue = new Queue()
  }

  // Time-based expiration (TTL)
  async invalidateByTTL(key: string): Promise<void> {
    // Auto-expires after TTL
    // No manual invalidation needed
  }

  // Event-based invalidation
  async invalidateOnEvent(event: string, data: any): Promise<void> {
    switch (event) {
      case 'user.updated':
        await this.cache.del(`user:${data.userId}`)
        await this.cache.del(`user:${data.userId}:profile`)
        break
      case 'user.deleted':
        await this.cache.del(`user:${data.userId}`)
        await this.cache.delPattern(`user:${data.userId}:*`)
        break
    }
  }

  // Pattern-based invalidation
  async invalidatePattern(pattern: string): Promise<void> {
    const keys = await this.scanKeys(pattern)
    await Promise.all(keys.map(key => this.cache.del(key)))
  }

  // Write-through cache
  async writeThrough(key: string, value: any): Promise<void> {
    // Write to cache first
    await this.cache.set(key, value)
    // Then write to database
    await this.saveToDatabase(key, value)
  }

  // Write-back cache (write-behind)
  async writeBack(key: string, value: any): Promise<void> {
    // Write to cache only
    await this.cache.set(key, value)
    // Queue for async write to database
    await this.invalidationQueue.add({ key, value })
  }

  // Cache aside (lazy loading)
  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttl = 3600
  ): Promise<T> {
    // Try to get from cache
    const cached = await this.cache.get<T>(key)
    if (cached !== null) {
      return cached
    }

    // Cache miss - fetch from source
    const value = await fetcher()
    await this.cache.set(key, value, ttl)
    return value
  }
}

// Usage
const invalidator = new CacheInvalidator(redisCache)

// Cache aside pattern
const user = await invalidator.getOrSet(
  `user:${userId}`,
  () => getUserFromDB(userId),
  3600
)

// Event-based invalidation
eventBus.on('user.updated', async (data) => {
  await invalidator.invalidateOnEvent('user.updated', data)
})
```

### 5. Cache Warming

```typescript
class CacheWarmer {
  private cache: CacheLayer

  constructor(cache: CacheLayer) {
    this.cache = cache
  }

  // Warm cache on startup
  async warmOnStartup(): Promise<void> {
    const keys = await this.getFrequentKeys()

    for (const key of keys) {
      const value = await this.fetchValue(key)
      await this.cache.set(key, value)
    }
  }

  // Warm cache on schedule
  async warmOnSchedule(): Promise<void> {
    setInterval(async () => {
      const keys = await this.getStaleKeys()
      for (const key of keys) {
        const value = await this.fetchValue(key)
        await this.cache.set(key, value)
      }
    }, 60000) // Every minute
  }

  // Warm cache on demand
  async warmOnDemand(keys: string[]): Promise<void> {
    for (const key of keys) {
      const value = await this.fetchValue(key)
      await this.cache.set(key, value)
    }
  }

  private async getFrequentKeys(): Promise<string[]> {
    // Get keys that are accessed frequently
    return ['user:1', 'user:2', 'product:100']
  }

  private async getStaleKeys(): Promise<string[]> {
    // Get keys that are about to expire
    return ['user:3', 'product:200']
  }

  private async fetchValue(key: string): Promise<any> {
    // Fetch from database or API
    return {}
  }
}
```

### 6. Cache Stampede Prevention

```typescript
import { Mutex } from 'async-mutex'

class CacheStampedePreventer {
  private cache: CacheLayer
  private locks: Map<string, Mutex> = new Map()

  constructor(cache: CacheLayer) {
    this.cache = cache
  }

  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttl = 3600
  ): Promise<T> {
    // Try to get from cache
    const cached = await this.cache.get<T>(key)
    if (cached !== null) {
      return cached
    }

    // Get or create lock for this key
    let lock = this.locks.get(key)
    if (!lock) {
      lock = new Mutex()
      this.locks.set(key, lock)
    }

    // Acquire lock
    const release = await lock.acquire()

    try {
      // Double-check cache after acquiring lock
      const doubleCheck = await this.cache.get<T>(key)
      if (doubleCheck !== null) {
        return doubleCheck
      }

      // Fetch from source
      const value = await fetcher()
      await this.cache.set(key, value, ttl)
      return value
    } finally {
      release()
      // Clean up lock after a delay
      setTimeout(() => {
        this.locks.delete(key)
      }, 10000)
    }
  }
}

// Alternative: Use Redis distributed lock
class RedisCacheStampedePreventer {
  private redis: Redis
  private cache: CacheLayer

  constructor(redis: Redis, cache: CacheLayer) {
    this.redis = redis
    this.cache = cache
  }

  async getOrSet<T>(
    key: string,
    fetcher: () => Promise<T>,
    ttl = 3600,
    lockTimeout = 10
  ): Promise<T> {
    // Try to get from cache
    const cached = await this.cache.get<T>(key)
    if (cached !== null) {
      return cached
    }

    // Try to acquire lock
    const lockKey = `lock:${key}`
    const lockValue = Date.now().toString()
    const acquired = await this.redis.set(
      lockKey,
      lockValue,
      'PX',
      lockTimeout * 1000,
      'NX'
    )

    if (acquired) {
      // We have the lock - fetch and cache
      try {
        const value = await fetcher()
        await this.cache.set(key, value, ttl)
        return value
      } finally {
        // Release lock
        const script = `
          if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
          else
            return 0
          end
        `
        await this.redis.eval(script, 1, lockKey, lockValue)
      }
    } else {
      // Wait and retry
      await new Promise(resolve => setTimeout(resolve, 100))
      return this.getOrSet(key, fetcher, ttl, lockTimeout)
    }
  }
}
```

### 7. CDN Caching

```typescript
// CDN cache configuration
interface CDNConfig {
  cacheRules: CacheRule[]
  purgeAPI: string
  apiKey: string
}

interface CacheRule {
  path: string
  ttl: number
  queryStrings?: boolean
  headers?: string[]
}

class CDNCache {
  private config: CDNConfig

  constructor(config: CDNConfig) {
    this.config = config
  }

  // Set cache headers for CDN
  setCacheHeaders(res: Response, path: string): void {
    const rule = this.config.cacheRules.find(r =>
      path.startsWith(r.path)
    )

    if (rule) {
      const directives: string[] = [`max-age=${rule.ttl}`]

      if (rule.queryStrings) {
        directives.push('public')
      } else {
        directives.push('public, no-cache="set-cookie"')
      }

      res.setHeader('Cache-Control', directives.join(', '))
    }
  }

  // Purge CDN cache
  async purge(paths: string[]): Promise<void> {
    const response = await fetch(this.config.purgeAPI, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
      },
      body: JSON.stringify({ paths }),
    })

    if (!response.ok) {
      throw new Error('CDN purge failed')
    }
  }

  // Purge by pattern
  async purgePattern(pattern: string): Promise<void> {
    const response = await fetch(`${this.config.purgeAPI}/pattern`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.config.apiKey}`,
      },
      body: JSON.stringify({ pattern }),
    })

    if (!response.ok) {
      throw new Error('CDN pattern purge failed')
    }
  }
}
```

## Quick Start

```typescript
// 1. Set up Redis cache
const redisCache = new RedisCache()

// 2. Create multi-layer cache
const cache = new MultiLayerCache([
  new MemoryCache(),
  redisCache,
])

// 3. Use cache aside pattern
const user = await cache.getOrSet(
  `user:${userId}`,
  () => getUserFromDB(userId),
  3600
)

// 4. Set HTTP cache headers
setCacheHeaders(res, {
  maxAge: 300,
  staleWhileRevalidate: 3600,
  public: true,
})
```

## Production Checklist

- [ ] Cache layer strategy defined
- [ ] Redis/Memcached configured
- [ ] HTTP cache headers set correctly
- [ ] Cache invalidation strategy implemented
- [ ] Cache stampede prevention in place
- [ ] Cache warming configured
- [ ] CDN caching configured
- [ ] Cache monitoring in place
- [ ] Cache size limits set
- [ ] Cache hit ratio monitored

## Anti-patterns

1. **No cache invalidation**: Cache เก่าเสมอ ทำให้ข้อมูลผิด
2. **Cache everything**: Cache data ที่ไม่ควร cache (sensitive, real-time)
3. **Long TTL**: Cache เก่านานเกินไป
4. **No cache stampede prevention**: Multiple requests hit backend simultaneously
5. **Ignoring cache size**: Memory overflow จาก cache ใหญ่เกินไป

## Integration Points

- Database queries
- External API calls
- CDN providers
- Monitoring systems
- Event buses

## Further Reading

- [Redis Caching Best Practices](https://redis.io/docs/manual/patterns/caching/)
- [HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- [Cache Stampede](https://en.wikipedia.org/wiki/Cache_stampede)
- [CDN Caching Strategies](https://www.cloudflare.com/learning/cdn/what-is-a-cdn/)
