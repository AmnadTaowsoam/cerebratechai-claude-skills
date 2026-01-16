---
name: Caching Strategies
description: Comprehensive guide to caching strategies, cache layers, invalidation patterns, and implementation for improving application performance
---

# Caching Strategies

## Why Caching Matters

Caching is one of the most effective performance optimizations. A well-designed cache can reduce latency by 10-100x.

### Key Benefits
- **Reduce Database Load**: Serve frequent queries from memory instead of disk
- **Improve Response Time**: Memory access is 1000x faster than disk
- **Reduce Costs**: Fewer database queries = lower compute costs
- **Scale to More Users**: Handle 10x more traffic with same infrastructure
- **Improve Availability**: Serve cached data even if database is down

### The Two Hard Problems in Computer Science
> "There are only two hard things in Computer Science: cache invalidation and naming things." - Phil Karlton

Cache invalidation is notoriously difficult. This guide will help you get it right.

---

## Types of Caches

### 1. In-Memory Cache (Application-Level)

**Characteristics:**
- Stored in application process memory
- Fastest (no network latency)
- Lost on restart
- Not shared across instances

**Use Cases:**
- Configuration data
- Computed values
- Small datasets

**Tools:**
- Node.js: `node-cache`, `lru-cache`
- Python: `functools.lru_cache`, `cachetools`

### 2. Distributed Cache (Redis, Memcached)

**Characteristics:**
- Shared across all application instances
- Persists across restarts (Redis)
- Network latency (1-5ms)
- Scalable (can add more cache nodes)

**Use Cases:**
- User sessions
- API responses
- Database query results
- Rate limiting

**Tools:**
- Redis (persistent, feature-rich)
- Memcached (simple, fast)

### 3. Database Query Cache

**Characteristics:**
- Built into database
- Automatic (no code changes)
- Limited control

**Use Cases:**
- Frequent identical queries
- Read-heavy workloads

**Tools:**
- MySQL Query Cache (deprecated in 8.0)
- PostgreSQL: No built-in query cache (use application-level)

### 4. CDN Cache (Edge Caching)

**Characteristics:**
- Cached at edge locations (close to users)
- Global distribution
- Lowest latency for static assets

**Use Cases:**
- Static files (images, CSS, JS)
- API responses (with proper headers)
- HTML pages

**Tools:**
- Cloudflare
- AWS CloudFront
- Fastly
- Akamai

---

## Cache Layers

### Multi-Tier Caching Architecture

```
User Request
    ↓
┌─────────────────────────────────────┐
│ L1: Application Memory (fastest)    │ ← 1-10ms
├─────────────────────────────────────┤
│ L2: Redis (fast)                    │ ← 1-5ms
├─────────────────────────────────────┤
│ L3: Database (slower)               │ ← 10-100ms
├─────────────────────────────────────┤
│ Edge: CDN (geographic distribution) │ ← 10-50ms
└─────────────────────────────────────┘
```

### Example: Multi-Tier Cache Lookup

```javascript
async function getUser(id) {
  // L1: Check application memory
  if (memoryCache.has(id)) {
    return memoryCache.get(id);
  }
  
  // L2: Check Redis
  const cached = await redis.get(`user:${id}`);
  if (cached) {
    const user = JSON.parse(cached);
    memoryCache.set(id, user); // Populate L1
    return user;
  }
  
  // L3: Query database
  const user = await db.users.findUnique({ where: { id } });
  
  // Populate caches
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user)); // L2
  memoryCache.set(id, user); // L1
  
  return user;
}
```

---

## What to Cache

### ✅ Good Candidates for Caching

1. **Frequent Reads, Infrequent Writes**
   - User profiles
   - Product catalogs
   - Configuration data

2. **Expensive Computations**
   - Complex aggregations
   - ML model predictions
   - Report generation

3. **Database Query Results**
   - Slow queries
   - Frequently accessed data
   - JOIN-heavy queries

4. **API Responses**
   - Third-party API calls
   - Internal microservice calls
   - Public API endpoints

5. **Static Assets**
   - Images, CSS, JavaScript
   - Fonts, icons
   - PDFs, documents

### ❌ Bad Candidates for Caching

1. **User-Specific Data** (unless keyed properly)
   - Shopping cart (changes frequently)
   - Real-time notifications
   - Live dashboards

2. **Frequently Changing Data**
   - Stock prices
   - Live scores
   - Real-time analytics

3. **Large Datasets**
   - Cache memory is limited
   - Better to cache aggregates or summaries

4. **Security-Sensitive Data**
   - Passwords (never cache!)
   - Credit card numbers
   - Personal health information

---

## Caching Strategies

### 1. Cache-Aside (Lazy Loading)

**How it Works:**
1. Application checks cache
2. If miss, query database
3. Store result in cache
4. Return result

**Pros:**
- Only cache what's needed
- Simple to implement
- Cache failures don't break app

**Cons:**
- First request is slow (cache miss)
- Cache and database can get out of sync

**Implementation:**
```javascript
async function getUser(id) {
  // Check cache
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);
  
  // Cache miss: Query database
  const user = await db.users.findUnique({ where: { id } });
  
  // Store in cache
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  
  return user;
}
```

### 2. Read-Through Cache

**How it Works:**
1. Application always queries cache
2. Cache automatically fetches from database on miss
3. Cache returns result

**Pros:**
- Simpler application code
- Cache handles database interaction

**Cons:**
- Requires cache library support
- Less control over caching logic

**Implementation:**
```javascript
// Using cache library with read-through
const cache = new CacheManager({
  loader: async (key) => {
    const id = key.split(':')[1];
    return await db.users.findUnique({ where: { id: parseInt(id) } });
  }
});

// Usage (cache handles database query automatically)
const user = await cache.get(`user:${id}`);
```

### 3. Write-Through Cache

**How it Works:**
1. Application writes to cache
2. Cache synchronously writes to database
3. Return success

**Pros:**
- Cache and database always in sync
- No stale data

**Cons:**
- Slower writes (synchronous)
- Write latency increased

**Implementation:**
```javascript
async function updateUser(id, data) {
  // Update database
  const user = await db.users.update({
    where: { id },
    data
  });
  
  // Update cache
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  
  return user;
}
```

### 4. Write-Behind (Write-Back) Cache

**How it Works:**
1. Application writes to cache
2. Cache asynchronously writes to database
3. Return success immediately

**Pros:**
- Fastest writes
- Batching possible

**Cons:**
- Risk of data loss (if cache fails before DB write)
- Complex to implement

**Implementation:**
```javascript
async function updateUser(id, data) {
  // Update cache immediately
  const user = { id, ...data };
  await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
  
  // Queue database write (asynchronous)
  await queue.add('update-user', { id, data });
  
  return user;
}

// Worker processes queue
queue.process('update-user', async (job) => {
  const { id, data } = job.data;
  await db.users.update({ where: { id }, data });
});
```

### 5. Refresh-Ahead

**How it Works:**
1. Cache automatically refreshes data before expiration
2. Predictive: Refresh popular keys proactively

**Pros:**
- No cache misses for popular data
- Always fresh data

**Cons:**
- Wasted refreshes for unpopular data
- Complex to implement

**Implementation:**
```javascript
// Refresh popular keys before expiration
setInterval(async () => {
  const popularKeys = await redis.zrange('popular:keys', 0, 100);
  
  for (const key of popularKeys) {
    const ttl = await redis.ttl(key);
    
    // Refresh if TTL < 10% of original
    if (ttl < 360) { // 10% of 3600s
      const id = key.split(':')[1];
      const user = await db.users.findUnique({ where: { id: parseInt(id) } });
      await redis.setex(key, 3600, JSON.stringify(user));
    }
  }
}, 60000); // Check every minute
```

---

## Cache Invalidation (Hardest Problem)

### 1. Time-Based Expiration (TTL)

**How it Works:**
- Set expiration time when caching
- Cache automatically deletes after TTL

**Pros:**
- Simple
- Automatic cleanup

**Cons:**
- Stale data until expiration
- Hard to choose right TTL

**Implementation:**
```javascript
// Cache for 1 hour
await redis.setex(`user:${id}`, 3600, JSON.stringify(user));
```

**TTL Guidelines:**
- Frequently changing data: 1-60 seconds
- Moderate changes: 5-60 minutes
- Rarely changing data: 1-24 hours
- Static data: 7-30 days

### 2. Event-Based Invalidation (On Update/Delete)

**How it Works:**
- Invalidate cache when data changes
- Triggered by database writes

**Pros:**
- No stale data
- Cache always fresh

**Cons:**
- Requires code changes
- Can miss invalidations

**Implementation:**
```javascript
async function updateUser(id, data) {
  // Update database
  const user = await db.users.update({ where: { id }, data });
  
  // Invalidate cache
  await redis.del(`user:${id}`);
  
  return user;
}
```

### 3. Tag-Based Invalidation (Invalidate Related Keys)

**How it Works:**
- Tag cache entries with categories
- Invalidate all entries with a tag

**Pros:**
- Invalidate related data easily
- Flexible

**Cons:**
- Requires tracking tags
- More complex

**Implementation:**
```javascript
// Cache with tags
async function cacheUserPosts(userId) {
  const posts = await db.posts.findMany({ where: { userId } });
  
  // Cache posts
  await redis.setex(`user:${userId}:posts`, 3600, JSON.stringify(posts));
  
  // Track tag
  await redis.sadd(`tag:user:${userId}`, `user:${userId}:posts`);
}

// Invalidate all user-related caches
async function invalidateUserCache(userId) {
  const keys = await redis.smembers(`tag:user:${userId}`);
  
  if (keys.length > 0) {
    await redis.del(...keys);
  }
  
  await redis.del(`tag:user:${userId}`);
}
```

### 4. Cache Stampede Prevention (Locking)

**Problem:**
- Cache expires
- 1000 requests hit at once
- All query database simultaneously
- Database overload

**Solution: Lock Pattern**
```javascript
async function getUser(id) {
  const cacheKey = `user:${id}`;
  const lockKey = `lock:${cacheKey}`;
  
  // Check cache
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // Try to acquire lock
  const locked = await redis.set(lockKey, '1', 'EX', 10, 'NX');
  
  if (locked) {
    // This request won the lock, query database
    const user = await db.users.findUnique({ where: { id } });
    await redis.setex(cacheKey, 3600, JSON.stringify(user));
    await redis.del(lockKey);
    return user;
  } else {
    // Another request is fetching, wait and retry
    await new Promise(resolve => setTimeout(resolve, 100));
    return getUser(id); // Retry
  }
}
```

---

## Cache Keys Design

### Best Practices

1. **Unique and Descriptive**
   ```javascript
   // BAD
   cache.set('123', user);
   
   // GOOD
   cache.set('user:123', user);
   ```

2. **Include Version (for Schema Changes)**
   ```javascript
   // Version 1
   cache.set('user:123:v1', { id: 123, name: 'John' });
   
   // Version 2 (added email field)
   cache.set('user:123:v2', { id: 123, name: 'John', email: 'john@example.com' });
   ```

3. **Namespace by Feature**
   ```javascript
   cache.set('api:users:123', user);
   cache.set('api:posts:456', post);
   cache.set('session:abc123', sessionData);
   ```

4. **Consistent Naming Convention**
   ```
   Format: <namespace>:<entity>:<id>:<version>
   
   Examples:
   - user:profile:123:v2
   - product:details:456:v1
   - api:search:query123:v1
   ```

---

## TTL Strategies

### 1. Short TTL for Changing Data

**Use Case:** Data that changes frequently
```javascript
// Cache for 30 seconds
await redis.setex('stock:AAPL:price', 30, JSON.stringify(price));
```

### 2. Long TTL for Static Data

**Use Case:** Data that rarely changes
```javascript
// Cache for 24 hours
await redis.setex('product:123:details', 86400, JSON.stringify(product));
```

### 3. No TTL for Immutable Data

**Use Case:** Data that never changes
```javascript
// No expiration
await redis.set('user:123:signup_date', '2024-01-15');
```

### 4. Stale-While-Revalidate Pattern

**How it Works:**
- Serve stale data immediately
- Refresh cache in background

**Implementation:**
```javascript
async function getUser(id) {
  const cacheKey = `user:${id}`;
  const cached = await redis.get(cacheKey);
  
  if (cached) {
    const { data, cachedAt } = JSON.parse(cached);
    const age = Date.now() - cachedAt;
    
    // If older than 5 minutes, refresh in background
    if (age > 300000) {
      // Don't await (background refresh)
      refreshUser(id);
    }
    
    // Return stale data immediately
    return data;
  }
  
  // Cache miss: Fetch and cache
  return await refreshUser(id);
}

async function refreshUser(id) {
  const user = await db.users.findUnique({ where: { id } });
  await redis.setex(
    `user:${id}`,
    3600,
    JSON.stringify({ data: user, cachedAt: Date.now() })
  );
  return user;
}
```

---

## Cache Warming

### 1. Pre-Populate Cache on Startup

**Use Case:** Critical data needed immediately

```javascript
async function warmCache() {
  console.log('Warming cache...');
  
  // Cache popular users
  const popularUsers = await db.users.findMany({
    where: { follower_count: { gte: 1000 } }
  });
  
  for (const user of popularUsers) {
    await redis.setex(`user:${user.id}`, 3600, JSON.stringify(user));
  }
  
  console.log(`Cached ${popularUsers.length} popular users`);
}

// Run on startup
warmCache();
```

### 2. Background Refresh of Popular Keys

**Use Case:** Keep popular data always fresh

```javascript
setInterval(async () => {
  // Get popular keys from analytics
  const popularKeys = await redis.zrange('analytics:popular', 0, 100);
  
  for (const key of popularKeys) {
    const id = key.split(':')[1];
    const user = await db.users.findUnique({ where: { id: parseInt(id) } });
    await redis.setex(key, 3600, JSON.stringify(user));
  }
}, 300000); // Every 5 minutes
```

### 3. Predictive Caching (What Users Will Request Next)

**Use Case:** Cache related data proactively

```javascript
async function getProduct(id) {
  const product = await getCachedProduct(id);
  
  // Predictive: Cache related products in background
  if (product.related_ids) {
    for (const relatedId of product.related_ids.slice(0, 5)) {
      getCachedProduct(relatedId); // Don't await
    }
  }
  
  return product;
}
```

---

## Cache Performance

### Key Metrics

1. **Hit Rate**
   - Formula: `hits / (hits + misses)`
   - Goal: >80%
   - Low hit rate = cache not effective

2. **Miss Rate**
   - Formula: `misses / (hits + misses)`
   - Goal: <20%

3. **Eviction Rate**
   - How often cache evicts entries
   - High eviction = cache too small

4. **Memory Usage**
   - Current memory / max memory
   - Goal: <80% (leave headroom)

### Monitoring Cache Performance

**Redis:**
```bash
# Get cache stats
redis-cli INFO stats

# Key metrics:
# - keyspace_hits
# - keyspace_misses
# - evicted_keys
# - used_memory
```

**Calculate Hit Rate:**
```javascript
const info = await redis.info('stats');
const hits = parseInt(info.match(/keyspace_hits:(\d+)/)[1]);
const misses = parseInt(info.match(/keyspace_misses:(\d+)/)[1]);
const hitRate = hits / (hits + misses);

console.log(`Cache hit rate: ${(hitRate * 100).toFixed(2)}%`);
```

---

## Eviction Policies

### Redis Eviction Policies

1. **LRU (Least Recently Used)** - Most Common
   ```
   maxmemory-policy allkeys-lru
   ```
   - Evicts least recently accessed keys
   - Good for general caching

2. **LFU (Least Frequently Used)**
   ```
   maxmemory-policy allkeys-lfu
   ```
   - Evicts least frequently accessed keys
   - Good for long-running caches

3. **FIFO (First In First Out)**
   - Evicts oldest keys first
   - Rarely used

4. **Random**
   ```
   maxmemory-policy allkeys-random
   ```
   - Evicts random keys
   - Fast but unpredictable

5. **No Eviction**
   ```
   maxmemory-policy noeviction
   ```
   - Returns error when memory full
   - Use for critical data

### Configuration

**redis.conf:**
```
maxmemory 2gb
maxmemory-policy allkeys-lru
```

---

## Distributed Caching

### 1. Redis Cluster

**Features:**
- Automatic sharding
- High availability
- Horizontal scaling

**Setup:**
```bash
# Create cluster with 3 masters, 3 replicas
redis-cli --cluster create \
  127.0.0.1:7000 127.0.0.1:7001 127.0.0.1:7002 \
  127.0.0.1:7003 127.0.0.1:7004 127.0.0.1:7005 \
  --cluster-replicas 1
```

### 2. Consistent Hashing

**How it Works:**
- Keys distributed across nodes using hash function
- Adding/removing nodes only affects adjacent keys

**Implementation:**
```javascript
const HashRing = require('hashring');

const ring = new HashRing([
  'redis1:6379',
  'redis2:6379',
  'redis3:6379'
]);

// Get node for key
const node = ring.get('user:123');
console.log(`Key "user:123" stored on ${node}`);
```

### 3. Cache Replication

**Master-Replica Setup:**
```bash
# On replica
redis-cli REPLICAOF redis-master 6379
```

**Benefits:**
- Read scaling (read from replicas)
- High availability (failover to replica)

### 4. Cache Failover

**Redis Sentinel:**
```bash
# sentinel.conf
sentinel monitor mymaster 127.0.0.1 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 10000
```

---

## Application-Level Caching

### Node.js

#### 1. node-cache

```javascript
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 600 }); // 10 minutes

// Set
cache.set('user:123', user);

// Get
const user = cache.get('user:123');

// Delete
cache.del('user:123');
```

#### 2. lru-cache

```javascript
const LRU = require('lru-cache');
const cache = new LRU({
  max: 500, // Max 500 items
  maxAge: 1000 * 60 * 60 // 1 hour
});

cache.set('user:123', user);
const user = cache.get('user:123');
```

### Python

#### 1. functools.lru_cache

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_user(user_id):
    return db.query(User).filter(User.id == user_id).first()

# Usage
user = get_user(123)  # Cached automatically
```

#### 2. cachetools

```python
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=300)  # 5 minutes

# Set
cache['user:123'] = user

# Get
user = cache.get('user:123')
```

---

## HTTP Caching Headers

### 1. Cache-Control

**Directives:**
```http
Cache-Control: max-age=3600              # Cache for 1 hour
Cache-Control: no-cache                  # Revalidate before use
Cache-Control: no-store                  # Don't cache at all
Cache-Control: public                    # Can be cached by CDN
Cache-Control: private                   # Only cache in browser
Cache-Control: must-revalidate           # Revalidate when stale
```

**Example:**
```javascript
app.get('/api/products', (req, res) => {
  res.set('Cache-Control', 'public, max-age=3600');
  res.json(products);
});
```

### 2. ETag (Validation)

**How it Works:**
1. Server sends ETag header (hash of content)
2. Client caches response with ETag
3. Client sends If-None-Match header with ETag
4. Server returns 304 Not Modified if unchanged

**Implementation:**
```javascript
const etag = require('etag');

app.get('/api/products', (req, res) => {
  const products = getProducts();
  const etagValue = etag(JSON.stringify(products));
  
  // Check if client has current version
  if (req.headers['if-none-match'] === etagValue) {
    return res.status(304).end();
  }
  
  res.set('ETag', etagValue);
  res.json(products);
});
```

### 3. Last-Modified

**How it Works:**
1. Server sends Last-Modified header
2. Client sends If-Modified-Since header
3. Server returns 304 if not modified

**Implementation:**
```javascript
app.get('/api/products', (req, res) => {
  const products = getProducts();
  const lastModified = new Date(products.updatedAt);
  
  // Check if modified since last request
  const ifModifiedSince = req.headers['if-modified-since'];
  if (ifModifiedSince && new Date(ifModifiedSince) >= lastModified) {
    return res.status(304).end();
  }
  
  res.set('Last-Modified', lastModified.toUTCString());
  res.json(products);
});
```

### 4. Expires (Legacy)

**Usage:**
```javascript
app.get('/api/products', (req, res) => {
  const expires = new Date(Date.now() + 3600000); // 1 hour
  res.set('Expires', expires.toUTCString());
  res.json(products);
});
```

**Note:** Use `Cache-Control: max-age` instead (more flexible)

---

## Common Caching Mistakes

### 1. Cache Stampede (Thundering Herd)

**Problem:** See "Cache Invalidation" section above

### 2. Stale Data Issues

**Problem:**
```javascript
// User updates profile
await db.users.update({ where: { id: 123 }, data: { name: 'Jane' } });

// Cache not invalidated, still returns old name
const user = await cache.get('user:123'); // { name: 'John' }
```

**Solution:**
```javascript
// Invalidate cache on update
await db.users.update({ where: { id: 123 }, data: { name: 'Jane' } });
await cache.del('user:123');
```

### 3. Cache Key Collisions

**Problem:**
```javascript
// BAD: Keys collide
cache.set('123', user);
cache.set('123', product); // Overwrites user!
```

**Solution:**
```javascript
// GOOD: Namespaced keys
cache.set('user:123', user);
cache.set('product:123', product);
```

### 4. Memory Leaks (Unbounded Caches)

**Problem:**
```javascript
// BAD: No size limit, grows forever
const cache = new Map();
cache.set(key, value); // Never evicts
```

**Solution:**
```javascript
// GOOD: LRU cache with size limit
const cache = new LRU({ max: 1000 });
```

---

## Real Caching Scenarios

### Scenario 1: API Response Caching

**Use Case:** Cache expensive API responses

```javascript
async function getWeather(city) {
  const cacheKey = `weather:${city}`;
  
  // Check cache
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // Call external API
  const response = await fetch(`https://api.weather.com/v1/${city}`);
  const weather = await response.json();
  
  // Cache for 10 minutes
  await redis.setex(cacheKey, 600, JSON.stringify(weather));
  
  return weather;
}
```

### Scenario 2: Database Query Caching

**Use Case:** Cache slow database queries

```javascript
async function getPopularPosts() {
  const cacheKey = 'posts:popular';
  
  // Check cache
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // Expensive query
  const posts = await db.posts.findMany({
    where: { views: { gte: 1000 } },
    orderBy: { views: 'desc' },
    take: 10,
    include: { author: true, comments: true }
  });
  
  // Cache for 1 hour
  await redis.setex(cacheKey, 3600, JSON.stringify(posts));
  
  return posts;
}
```

### Scenario 3: User Session Caching

**Use Case:** Store user sessions in Redis

```javascript
async function createSession(userId) {
  const sessionId = crypto.randomUUID();
  const session = {
    userId,
    createdAt: Date.now(),
    expiresAt: Date.now() + 86400000 // 24 hours
  };
  
  // Store in Redis with 24h TTL
  await redis.setex(`session:${sessionId}`, 86400, JSON.stringify(session));
  
  return sessionId;
}

async function getSession(sessionId) {
  const cached = await redis.get(`session:${sessionId}`);
  return cached ? JSON.parse(cached) : null;
}
```

### Scenario 4: Product Catalog Caching

**Use Case:** Cache product catalog with tag-based invalidation

```javascript
async function getProduct(id) {
  const cacheKey = `product:${id}`;
  
  // Check cache
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);
  
  // Query database
  const product = await db.products.findUnique({
    where: { id },
    include: { category: true, reviews: true }
  });
  
  // Cache for 1 hour
  await redis.setex(cacheKey, 3600, JSON.stringify(product));
  
  // Track tag for invalidation
  await redis.sadd(`tag:category:${product.categoryId}`, cacheKey);
  
  return product;
}

// Invalidate all products in a category
async function invalidateCategory(categoryId) {
  const keys = await redis.smembers(`tag:category:${categoryId}`);
  if (keys.length > 0) {
    await redis.del(...keys);
  }
  await redis.del(`tag:category:${categoryId}`);
}
```

---

## Implementation Examples

### Redis Caching in Node.js

```javascript
const redis = require('redis');
const client = redis.createClient();

class CacheService {
  async get(key) {
    const value = await client.get(key);
    return value ? JSON.parse(value) : null;
  }
  
  async set(key, value, ttl = 3600) {
    await client.setex(key, ttl, JSON.stringify(value));
  }
  
  async del(key) {
    await client.del(key);
  }
  
  async invalidatePattern(pattern) {
    const keys = await client.keys(pattern);
    if (keys.length > 0) {
      await client.del(...keys);
    }
  }
}

module.exports = new CacheService();
```

### Redis Caching in Python

```python
import redis
import json

class CacheService:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)
    
    def get(self, key):
        value = self.client.get(key)
        return json.loads(value) if value else None
    
    def set(self, key, value, ttl=3600):
        self.client.setex(key, ttl, json.dumps(value))
    
    def delete(self, key):
        self.client.delete(key)
    
    def invalidate_pattern(self, pattern):
        keys = self.client.keys(pattern)
        if keys:
            self.client.delete(*keys)

cache = CacheService()
```

### Cache-Aside Pattern

```javascript
class Repository {
  constructor(db, cache) {
    this.db = db;
    this.cache = cache;
  }
  
  async findById(id) {
    const cacheKey = `user:${id}`;
    
    // Check cache
    const cached = await this.cache.get(cacheKey);
    if (cached) return cached;
    
    // Query database
    const user = await this.db.users.findUnique({ where: { id } });
    
    // Cache result
    if (user) {
      await this.cache.set(cacheKey, user, 3600);
    }
    
    return user;
  }
  
  async update(id, data) {
    // Update database
    const user = await this.db.users.update({ where: { id }, data });
    
    // Invalidate cache
    await this.cache.del(`user:${id}`);
    
    return user;
  }
}
```

### Write-Through Pattern

```javascript
class Repository {
  async update(id, data) {
    // Update database
    const user = await this.db.users.update({ where: { id }, data });
    
    // Update cache (write-through)
    await this.cache.set(`user:${id}`, user, 3600);
    
    return user;
  }
}
```

---

## Summary

### Quick Reference

**Cache Types:**
- In-memory: Fastest, not shared
- Redis: Shared, persistent
- CDN: Edge caching, global

**Caching Strategies:**
- Cache-Aside: Most common, lazy loading
- Read-Through: Cache handles DB queries
- Write-Through: Sync cache and DB
- Write-Behind: Async DB writes
- Refresh-Ahead: Proactive refresh

**Invalidation:**
- TTL: Time-based expiration
- Event-based: Invalidate on update
- Tag-based: Invalidate related keys
- Lock pattern: Prevent stampede

**Best Practices:**
1. Cache frequently read, rarely written data
2. Use namespaced keys (`user:123:v2`)
3. Set appropriate TTLs
4. Monitor hit rate (goal: >80%)
5. Invalidate on updates
6. Prevent cache stampede with locks
7. Use multi-tier caching (L1, L2, L3)

**Common Mistakes:**
- Cache stampede
- Stale data
- Key collisions
- Unbounded caches

**Tools:**
- Redis (distributed cache)
- node-cache, lru-cache (Node.js)
- functools.lru_cache (Python)
- Cloudflare, CloudFront (CDN)
