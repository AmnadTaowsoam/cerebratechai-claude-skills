---
name: Redis Caching Patterns
description: Comprehensive guide to Redis caching including setup, data structures, caching strategies, and best practices.
---

# Redis Caching Patterns

## Overview

Redis is an in-memory data structure store that can be used as a database, cache, message broker, and queue. This skill covers Redis setup, data structures, caching strategies, key naming conventions, TTL management, cache invalidation, distributed caching, pub/sub patterns, session storage, and rate limiting.

## Prerequisites

- Understanding of caching concepts
- Knowledge of data structures (strings, hashes, lists, sets, sorted sets)
- Familiarity with Node.js or Python
- Understanding of TTL (Time To Live) concepts
- Knowledge of distributed systems basics

## Key Concepts

### Redis Data Structures

- **Strings**: Binary-safe strings with up to 512MB size
- **Hashes**: Maps between string fields and string values
- **Lists**: Collections of string elements sorted by insertion order
- **Sets**: Unordered collections of unique strings
- **Sorted Sets**: Collections of unique strings ordered by an associated score

### Caching Strategies

- **Cache-Aside (Lazy Loading)**: Cache is populated on demand
- **Write-Through**: Cache is updated synchronously with database
- **Write-Behind**: Cache is updated asynchronously with database
- **Read-Through**: Cache is populated by the cache provider

### Key Design Patterns

- **Key Naming**: Hierarchical, environment-based, and pattern-based naming
- **TTL Management**: Absolute TTL, sliding TTL, dynamic TTL
- **Cache Invalidation**: Simple, pattern-based, tag-based, hash-based
- **Distributed Caching**: Redis clusters, client-side sharding

## Implementation Guide

### Redis Setup

#### Basic Connection

```typescript
// config/redis.ts
import { createClient } from 'redis'

const redisClient = createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379',
  socket: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
  },
  password: process.env.REDIS_PASSWORD,
  database: process.env.REDIS_DB || '0',
})

export { redisClient }
```

```python
# config/redis.py
import redis
from typing import Optional

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    password=Optional[str] = None,
    decode_responses=True
)
```

#### Connection Pooling

```typescript
// config/redis-pool.ts
import { createClient } from 'redis'

const pool = createClient({
  url: process.env.REDIS_URL || 'redis://localhost:6379',
  socket: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
  },
  maxRetriesPerRequest: 3,
  retryDelayOnFailover: 100,
  lazyConnect: true,
})

export { pool }
```

```python
# config/redis-pool.py
import redis
from redis.connection import ConnectionPool

pool = ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=50,
    decode_responses=True
)

def get_redis_client():
    return pool.get_connection()
```

### Data Structures

#### Strings

```typescript
// Basic string operations
import { redisClient } from '../config/redis'

// Set a key
await redisClient.set('user:123', JSON.stringify({ name: 'John', email: 'john@example.com' }))

// Get a key
const user = await redisClient.get('user:123')
if (user) {
  console.log(JSON.parse(user))
}

// Set with expiration (TTL in seconds)
await redisClient.set('session:abc', JSON.stringify({ userId: 123 }), {
  EX: 3600 // 1 hour
})

// Set with expiration using milliseconds
await redisClient.set('temp:data', 'value', {
  PX: 60000 // 60 seconds
})

// Get remaining TTL
const ttl = await redisClient.ttl('session:abc')
console.log(`Session expires in ${ttl} seconds`)

// Delete a key
await redisClient.del('user:123')
```

```python
# Basic string operations
import redis_client

# Set a key
await redis_client.set('user:123', '{"name": "John", "email": "john@example.com"}')

# Get a key
user_data = await redis_client.get('user:123')
if user_data:
    import json
    print(json.loads(user_data))

# Set with expiration (TTL in seconds)
await redis_client.setex('session:abc', json.dumps({"user_id": 123}), 3600)

# Get remaining TTL
ttl = await redis_client.ttl('session:abc')
print(f'Session expires in {ttl} seconds')

# Delete a key
await redis_client.delete('user:123')
```

#### Hashes

```typescript
// Hash operations
import { redisClient } from '../config/redis'

// Set hash fields
await redisClient.hSet('user:123', {
  name: 'John Doe',
  email: 'john@example.com',
  age: '30'
})

// Get specific hash field
const name = await redisClient.hGet('user:123', 'name')

// Get all hash fields
const user = await redisClient.hGetAll('user:123')

// Get multiple hash fields
const fields = await redisClient.hMGet('user:123', ['name', 'email'])

// Set multiple hash fields
await redisClient.hMSet('user:123', {
  name: 'Jane Smith',
  email: 'jane@example.com'
})

// Increment hash field
const newAge = await redisClient.hIncrBy('user:123', 'age', 1)

// Check if hash field exists
const hasName = await redisClient.hExists('user:123', 'name')

// Delete hash field
await redisClient.hDel('user:123', 'age')

// Get hash length
const hashLength = await redisClient.hLen('user:123')

// Get all hash keys
const allUsers = await redisClient.keys('user:*')
```

```python
# Hash operations
import redis_client

# Set hash fields
await redis_client.hset('user:123', mapping={
    'name': 'John Doe',
    'email': 'john@example.com',
    'age': '30'
})

# Get specific hash field
name = await redis_client.hget('user:123', 'name')

# Get all hash fields
user = await redis_client.hgetall('user:123')

# Get multiple hash fields
fields = await redis_client.hmget('user:123', ['name', 'email'])

# Set multiple hash fields
await redis_client.hmset('user:123', {
    'name': 'Jane Smith',
    'email': 'jane@example.com'
})

# Increment hash field
new_age = await redis_client.hincrby('user:123', 'age', 1)

# Check if hash field exists
has_name = await redis_client.hexists('user:123', 'name')

# Delete hash field
await redis_client.hdel('user:123', 'age')

# Get hash length
hash_length = await redis_client.hlen('user:123')

# Get all hash keys
all_users = await redis_client.keys('user:*')
```

#### Lists

```typescript
// List operations
import { redisClient } from '../config/redis'

// Add to list (left push)
await redisClient.lPush('recent:items', JSON.stringify({ id: 1, name: 'Item 1' }))

// Add to list (right push)
await redisClient.rPush('recent:items', JSON.stringify({ id: 2, name: 'Item 2' }))

// Get list range (0 to -1 means all)
const items = await redisClient.lRange('recent:items', 0, -1)

// Get list range with pagination
const page1 = await redisClient.lRange('recent:items', 0, 9)
const page2 = await redisClient.lRange('recent:items', 10, 19)

// Get list length
const length = await redisClient.lLen('recent:items')

// Trim list to N items
await redisClient.lTrim('recent:items', 0, 99)

// Remove from list
await redisClient.lRem('recent:items', 0)

// Get element at index
const firstItem = await redisClient.lIndex('recent:items', 0)
```

```python
# List operations
import redis_client

# Add to list (left push)
await redis_client.lpush('recent:items', json.dumps({"id": 1, "name": "Item 1"}))

# Add to list (right push)
await redis_client.rpush('recent:items', json.dumps({"id": 2, "name": "Item 2"}))

# Get list range (0 to -1 means all)
items = await redis_client.lrange('recent:items', 0, -1)

# Get list range with pagination
page1 = await redis_client.lrange('recent:items', 0, 9)
page2 = await redis_client.lrange('recent:items', 10, 19)

# Get list length
length = await redis_client.llen('recent:items')

# Trim list to N items
await redis_client.ltrim('recent:items', 0, 99)

# Remove from list
await redis_client.lrem('recent:items', 0, 1)

# Get element at index
first_item = await redis_client.lindex('recent:items', 0)
```

#### Sets

```typescript
// Set operations
import { redisClient } from '../config/redis'

// Add to set
await redisClient.sAdd('user:123:followers', 'user456')

// Add multiple to set
await redisClient.sAdd('user:123:followers', ['user456', 'user789', 'user012'])

// Check if member exists
const isFollower = await redisClient.sIsMember('user:123:followers', 'user456')

// Get all members
const followers = await redisClient.sMembers('user:123:followers')

// Get random member
const randomFollower = await redisClient.sRandMember('user:123:followers')

// Remove from set
await redisClient.sRem('user:123:followers', 'user456')

// Get set size
const followerCount = await redisClient.sCard('user:123:followers')

// Get union of multiple sets
const allUsers = await redisClient.sUnion('user:123:followers', 'user:456:following')
```

```python
# Set operations
import redis_client

# Add to set
await redis_client.sadd('user:123:followers', 'user456')

# Add multiple to set
await redis_client.sadd('user:123:followers', ['user456', 'user789', 'user012'])

# Check if member exists
is_follower = await redis_client.sismember('user:123:followers', 'user456')

# Get all members
followers = await redis_client.smembers('user:123:followers')

# Get random member
random_follower = await redis_client.srandmember('user:123:followers')

# Remove from set
await redis_client.srem('user:123:followers', 'user456')

# Get set size
follower_count = await redis_client.scard('user:123:followers')

# Get union of multiple sets
all_users = await redis_client.sunion('user:123:followers', 'user:456:following')
```

#### Sorted Sets

```typescript
// Sorted set operations
import { redisClient } from '../config/redis'

// Add to sorted set
await redisClient.zAdd('leaderboard:scores', JSON.stringify({ userId: 1, score: 100 }))

// Add multiple with scores
await redisClient.zAdd('leaderboard:scores', [
  JSON.stringify({ userId: 1, score: 100 }),
  JSON.stringify({ userId: 2, score: 95 }),
  JSON.stringify({ userId: 3, score: 90 })
])

// Get range by score (ascending)
const top10 = await redisClient.zRangeWithScores('leaderboard:scores', 0, 9, 'WITHSCORES')

// Get range by score (descending)
const top10 = await redisClient.zRevRangeWithScores('leaderboard:scores', 0, 9, 'WITHSCORES')

// Get rank of member
const rank = await redis.zRevRank('leaderboard:scores', JSON.stringify({ userId: 1 }))

// Get score of member
const score = await redis.zScore('leaderboard:scores', JSON.stringify({ userId: 1 }))

// Remove member
await redis.zRem('leaderboard:scores', JSON.stringify({ userId: 1 }))
```

```python
# Sorted set operations
import redis_client

# Add to sorted set
await redis_client.zadd('leaderboard:scores', json.dumps({"user_id": 1, "score": 100}))

# Add multiple with scores
await redis_client.zadd('leaderboard:scores', [
    json.dumps({"user_id": 1, "score": 100}),
    json.dumps({"user_id": 2, "score": 95}),
    json.dumps({"user_id": 3, "score": 90})
])

# Get range by score (ascending)
top_10 = await redis_client.zrange('leaderboard:scores', 0, 9, withscores=True)

# Get range by score (descending)
top_10 = await redis_client.zrevrange('leaderboard:scores', 0, 9, withscores=True)

# Get rank of member
rank = await redis_client.zrevrank('leaderboard:scores', json.dumps({"user_id": 1}))

# Get score of member
score = await redis_client.zscore('leaderboard:scores', json.dumps({"user_id": 1}))

# Remove member
await redis_client.zrem('leaderboard:scores', json.dumps({"user_id": 1}))
```

### Caching Strategies

#### Cache-Aside (Lazy Loading)

```typescript
// services/cache.service.ts
import { redisClient } from '../config/redis'

interface CacheOptions {
  ttl?: number
}

export async function getFromCache<T>(
  key: string,
  options?: CacheOptions
): Promise<T | null> {
  const cached = await redisClient.get(key)
  
  if (cached) {
    return JSON.parse(cached)
  }
  
  return null
}

export async function setCache<T>(
  key: string,
  data: T,
  options?: CacheOptions
): Promise<void> {
  const value = JSON.stringify(data)
  
  if (options?.ttl) {
    await redisClient.set(key, value, {
      EX: options.ttl
    })
  } else {
    await redisClient.set(key, value)
  }
}

// Usage
async function getUser(userId: string) {
  const cacheKey = `user:${userId}`
  
  // Try to get from cache
  const cached = await getFromCache<User>(cacheKey)
  if (cached) {
    return cached
  }
  
  // Fetch from database
  const user = await db.user.findUnique({ where: { id: userId } })
  
  // Set in cache with 1 hour TTL
  await setCache(cacheKey, user, { ttl: 3600 })
  
  return user
}
```

```python
# services/cache.service.py
import redis_client
import json

async def get_from_cache(key: str, ttl: int = None) -> dict | None:
    cached = await redis_client.get(key)
    
    if cached:
        return json.loads(cached)
    
    return None


async def set_cache(key: str, data: any, ttl: int = None) -> None:
    value = json.dumps(data)
    
    if ttl:
        await redis_client.setex(key, value, ttl)
    else:
        await redis_client.set(key, value)


async def get_user(user_id: str):
    cache_key = f"user:{user_id}"
    
    # Try to get from cache
    cached = await get_from_cache(cache_key)
    if cached:
        return cached
    
    # Fetch from database
    user = await db.user.find_unique({"id": user_id})
    
    # Set in cache with 1 hour TTL
    await set_cache(cache_key, user, ttl=3600)
    
    return user
```

#### Write-Through

```typescript
// services/cache.service.ts
export async function updateWithCache<T>(
  key: string,
  updater: () => Promise<T>
): Promise<T> {
  // Update cache and database atomically
  const data = await updater()
  
  // Set in cache
  await redisClient.set(key, JSON.stringify(data), {
    EX: 3600
  })
  
  return data
}

// Usage
async function updateUser(userId: string, updates: Partial<User>) {
  const cacheKey = `user:${userId}`
  
  const updatedUser = await updateWithCache(cacheKey, async () => {
    return await db.user.update({
      where: { id: userId },
      data: updates
    })
  })
  
  return updatedUser
}
```

```python
async def update_with_cache(key: str, updater: callable) -> dict:
    # Update cache and database atomically
    data = await updater()
    
    # Set in cache
    await redis_client.set(key, json.dumps(data), ex=3600)
    
    return data


async def update_user(user_id: str, updates: dict):
    cache_key = f"user:{user_id}"
    
    updated_user = await update_with_cache(cache_key, lambda: db.user.update(
        {"id": user_id},
        updates=updates
    ))
    
    return updated_user
```

#### Write-Behind (Asynchronous)

```typescript
// services/cache.service.ts
import { redisClient } from '../config/redis'

export async function setCacheAsync<T>(
  key: string,
  data: T,
  ttl?: number
): Promise<void> {
  const value = JSON.stringify(data)
  
  // Set in Redis
  await redisClient.set(key, value, {
    EX: ttl || 3600
  })
  
  // Update in background
  await db.user.update({
    where: { id: data.id },
    data: updates
  })
}

// Usage
async function createUser(userData: User) {
  // Create in database first
  const user = await db.user.create({ data: userData })
  
  // Set in cache asynchronously
  await setCacheAsync(`user:${user.id}`, user)
}
```

```python
async def set_cache_async(key: str, data: dict, ttl: int = None) -> None:
    value = json.dumps(data)
    
    # Set in Redis
    await redis_client.set(key, value, ex=ttl or 3600)
    
    # Update in background
    await db.user.create(data=data)


async def create_user(user_data: dict):
    # Create in database first
    user = await db.user.create(data=user_data)
    
    # Set in cache asynchronously
    await set_cache_async(f"user:{user['id']}", user)
```

#### Write-Behind (Synchronous)

```typescript
// services/cache.service.ts
export async function setCacheSync<T>(
  key: string,
  data: T,
  ttl?: number
): Promise<void> {
  const value = JSON.stringify(data)
  
  // Update in database
  await db.user.create({ data })
  
  // Set in Redis synchronously
  await redisClient.set(key, value, {
    EX: ttl || 3600
  })
}

// Usage
async function createAndCacheUser(userData: User) {
  // Create in database
  const user = await db.user.create({ data: userData })
  
  // Set in cache
  await setCacheSync(`user:${user.id}`, user)
}
```

```python
async def set_cache_sync(key: str, data: dict, ttl: int = None) -> None:
    value = json.dumps(data)
    
    # Set in Redis synchronously
    await redis_client.set(key, value, ex=ttl or 3600)
```

### Key Naming Conventions

#### Naming Patterns

```typescript
// Good naming conventions
const keys = {
  user: 'user:{userId}',              // User data
  userSession: 'session:{sessionId}',      // User session
  userList: 'users:page:{page}',       // User list pagination
  userCache: 'cache:user:{userId}',       // User cache
  product: 'product:{productId}',         // Product data
  productCache: 'cache:product:{productId}', // Product cache
  searchResults: 'search:{query}:page:{page}', // Search results pagination
  leaderboard: 'leaderboard:category:{category}', // Leaderboard by category
  rateLimit: 'ratelimit:{ip}', // Rate limit per IP
  session: 'session:{sessionId}:user:{userId}', // User session data
}

// Usage
const userKey = keys.user('123')
const sessionKey = keys.userSession('abc-123', '123')
```

#### Key Hierarchies

```typescript
// Hierarchical key structure
const keys = {
  user: {
    base: 'user',
    profile: (userId: string) => `user:${userId}:profile`,
    settings: (userId: string) => `user:${userId}:settings`,
    posts: (userId: string, page: number) => `user:${userId}:posts:${page}`,
  },
  product: {
    base: 'product',
    details: (productId: string) => `product:${productId}:details`,
    reviews: (productId: string) => `product:${productId}:reviews`,
    cache: (productId: string) => `cache:product:${productId}`,
  },
  session: {
    base: 'session',
    user: (sessionId: string, userId: string) => `session:${sessionId}:user:${userId}`,
  },
}

// Usage
const userProfileKey = keys.user.profile('123')
const productDetailsKey = keys.product.details('abc-456')
```

#### Environment-based Keys

```typescript
const keys = {
  development: {
    user: (userId: string) => `dev:user:${userId}`,
    session: (sessionId: string) => `dev:session:${sessionId}`,
  },
  production: {
    user: (userId: string) => `prod:user:${userId}`,
    session: (sessionId: string) => `prod:session:${sessionId}`,
  },
}

const envPrefix = process.env.NODE_ENV === 'production' ? 'prod' : 'dev'

const userKey = keys[envPrefix].user('123')
```

```python
# Hierarchical key structure
keys = {
    'user': {
        'base': 'user',
        'profile': lambda user_id: f'user:{user_id}:profile',
        'settings': lambda user_id: f'user:{user_id}:settings',
        'posts': lambda user_id, page: f'user:{user_id}:posts:{page}',
    },
    'product': {
        'base': 'product',
        'details': lambda product_id: f'product:{product_id}:details',
        'reviews': lambda product_id: f'product:{product_id}:reviews',
        'cache': lambda product_id: f'cache:product:{product_id}',
    },
    'session': {
        'base': 'session',
        'user': lambda session_id, user_id: f'session:{session_id}:user:{user_id}',
    },
}

# Usage
user_profile_key = keys['user']['profile']('123')
product_details_key = keys['product']['details']('abc-456')
```

### TTL Management

#### Absolute TTL

```typescript
// services/cache.service.ts
export async function setWithTTL(
  key: string,
  data: any,
  ttlSeconds: number
): Promise<void> {
  await redisClient.set(key, JSON.stringify(data), {
    EX: ttlSeconds
  })
}

// Usage
await setWithTTL('user:123', userData, 3600) // 1 hour
await setWithTTL('session:abc', sessionData, 1800) // 30 minutes
await setWithTTL('temp:data', tempData, 60) // 1 minute
```

#### Sliding TTL (Refresh on Access)

```typescript
// services/cache.service.ts
export async function getWithRefresh(
  key: string,
  ttlSeconds: number
): Promise<any> {
  const cached = await redisClient.get(key)
  
  if (cached) {
    // Refresh TTL on access
    await redisClient.expire(key, ttlSeconds)
    return JSON.parse(cached)
  }
  
  return null
}

// Usage
async function getUserWithRefresh(userId: string) {
  const key = `user:${userId}`
  
  const user = await getWithRefresh(key, 3600)
  
  if (user) {
    return user
  }
  
  // Fetch from database
  const dbUser = await db.user.findUnique({ where: { id: userId } })
  
  await setWithTTL(key, dbUser, 3600)
  
  return dbUser
}
```

```python
async def get_with_refresh(key: str, ttl_seconds: int) -> dict | None:
    cached = await redis_client.get(key)
    
    if cached:
        # Refresh TTL on access
        await redis_client.expire(key, ttl_seconds)
        return json.loads(cached)
    
    return None


async def get_user_with_refresh(user_id: str):
    key = f"user:{user_id}"
    
    user = await get_with_refresh(key, 3600)
    if user:
        return user
    
    # Fetch from database
    db_user = await db.user.find_unique({"id": user_id})
    await set_with_ttl(key, db_user, 3600)
    
    return db_user
```

#### Dynamic TTL Based on Data

```typescript
// services/cache.service.ts
export async function setDynamicTTL(
  key: string,
  data: any
): Promise<void> {
  let ttl: number
  
  // Calculate TTL based on data type
  if (data.type === 'user') {
    ttl = 3600 // 1 hour
  } else if (data.type === 'session') {
    ttl = 1800 // 30 minutes
  } else if (data.type === 'temp') {
    ttl = 60 // 1 minute
  } else {
    ttl = 600 // 10 minutes
  }
  
  await redisClient.set(key, JSON.stringify(data), {
    EX: ttl
  })
}
```

### Cache Invalidation

#### Simple Invalidation

```typescript
// services/cache.service.ts
export async function invalidateUser(userId: string): Promise<void> {
  // Delete user cache
  await redisClient.del(`user:${userId}`)
  
  // Delete user-related caches
  const keys = await redisClient.keys(`user:${userId}:*`)
  if (keys.length > 0) {
    await redisClient.del(keys)
  }
}

// Usage
async function updateUser(userId: string, updates: Partial<User>) {
  // Update in database
  const user = await db.user.update({
    where: { id: userId },
    data: updates
  })
  
  // Invalidate cache
  await invalidateUser(userId)
  
  return user
}
```

#### Pattern-based Invalidation

```typescript
// services/cache.service.ts
export async function invalidatePattern(pattern: string): Promise<number> {
  const keys = await redisClient.keys(pattern)
  
  if (keys.length > 0) {
    await redisClient.del(keys)
  }
  
  return keys.length
}

// Usage
async function invalidateAllUserCaches() {
  await invalidatePattern('user:*')
}

async function invalidateAllProductCaches(productId: string) {
  await invalidatePattern(`product:${productId}:*`)
}
```

#### Tag-based Invalidation

```typescript
// services/cache.service.ts
export async function invalidateTag(tag: string): Promise<number> {
  // Invalidate all keys with the tag
  const keys = await redisClient.keys(`*:${tag}`)
  
  if (keys.length > 0) {
    await redisClient.del(keys)
  }
  
  return keys.length
}

// Usage
async function invalidateByTags(tags: string[]) {
  for (const tag of tags) {
    await invalidateTag(tag)
  }
}
```

#### Hash-based Invalidation

```typescript
// services/cache.service.ts
export async function invalidateUserHash(userId: string): Promise<void> {
  // Delete user hash
  await redisClient.del(`user:${userId}`)
  
  // Delete user sessions
  const sessionKeys = await redisClient.keys(`session:*:user:${userId}`)
  if (sessionKeys.length > 0) {
    await redisClient.del(sessionKeys)
  }
}
```

```python
# Hash-based invalidation
async def invalidate_user_hash(user_id: str) -> None:
    # Delete user hash
    await redis_client.delete(f"user:{user_id}")
    
    # Delete user sessions
    session_keys = await redis_client.keys(f"session:*:user:{user_id}")
    if session_keys:
        await redis_client.delete(*session_keys)
```

### Distributed Caching

#### Redis Cluster

```typescript
// config/redis-cluster.ts
import { createCluster } from 'redis'

const cluster = createCluster({
  rootNodes: [
    { host: 'redis-1.example.com', port: 6379 },
    { host: 'redis-2.example.com', port: 6379 },
    { host: 'redis-3.example.com', port: 6379 },
  ],
  readonlyMode: 'slave',
})

export { cluster }
```

#### Client-side Sharding

```typescript
// services/cache.service.ts
export function getShardKey(key: string, userId?: string): string {
  // Shard by user ID for user-specific data
  if (userId) {
    return `${userId}:${key}`
  }
  
  // Shard by key prefix
  const shard = Math.abs(key.split(':')[0].charCodeAt(0) % 4)
  return `shard:${shard}:${key}`
}

// Usage
const userKey = getShardKey('user:123', '456')
const sessionKey = getShardKey('session:abc', '123')
```

### Pub/Sub Patterns

#### Simple Publisher

```typescript
// services/pubsub.service.ts
import { redisClient } from '../config/redis'

export async function publish(channel: string, message: any): Promise<number> {
  return await redisClient.publish(channel, JSON.stringify(message))
}

// Usage
await publish('notifications', { type: 'user.created', userId: '123' })
```

#### Simple Subscriber

```typescript
// services/pubsub.service.ts
import { redisClient } from '../config/redis'

export async function subscribe(
  channel: string,
  callback: (message: any) => void
): Promise<void> {
  const subscriber = redisClient.duplicate()
  
  await subscriber.subscribe(channel, (message) => {
    const data = JSON.parse(message)
    callback(data)
  })
}

// Usage
await subscribe('notifications', (data) => {
  console.log('Received notification:', data)
})
```

#### Pattern-based Subscriptions

```typescript
// services/pubsub.service.ts
export async function subscribeToUserNotifications(
  userId: string,
  callback: (message: any) => void
): Promise<void> {
  const channel = `notifications:user:${userId}`
  await subscribe(channel, callback)
}

export async function subscribeToGlobalNotifications(
  callback: (message: any) => void
): Promise<void> {
  const channel = 'notifications:global'
  await subscribe(channel, callback)
}
```

#### Message Queues (Pub/Sub)

```typescript
// services/queue.service.ts
export async function addToQueue(
  queueName: string,
  item: any
): Promise<number> {
  return await redisClient.lPush(queueName, JSON.stringify(item))
}

export async function processQueue(
  queueName: string,
  processor: (item: any) => Promise<void>
): Promise<void> {
  while (true) {
    const result = await redisClient.brPop(queueName)
    
    if (!result) {
      break
    }
    
    const item = JSON.parse(result)
    await processor(item)
  }
}

// Usage
await addToQueue('email:queue', { to: 'user@example.com', subject: 'Hello', body: 'Message' })
```

### Session Storage

#### Session Management

```typescript
// services/session.service.ts
import { redisClient } from '../config/redis'

export async function createSession(
  userId: string,
  userData: any,
  ttlSeconds: number = 3600
): Promise<string> {
  const sessionId = generateSessionId()
  const sessionKey = `session:${sessionId}`
  
  const sessionData = {
    userId,
    userData,
    createdAt: new Date().toISOString(),
    lastActivity: new Date().toISOString(),
  }
  
  // Store session data in hash
  await redisClient.hSet(sessionKey, sessionData)
  
  // Set TTL
  await redisClient.expire(sessionKey, ttlSeconds)
  
  return sessionId
}

export async function getSession(sessionId: string): Promise<any | null> {
  const sessionKey = `session:${sessionId}`
  
  const sessionData = await redisClient.hGetAll(sessionKey)
  
  if (!sessionData) {
    return null
  }
  
  return sessionData
}

export async function updateSessionActivity(sessionId: string): Promise<void> {
  const sessionKey = `session:${sessionId}`
  
  await redisClient.hSet(sessionKey, {
    lastActivity: new Date().toISOString()
  })
}

export async function deleteSession(sessionId: string): Promise<void> {
  const sessionKey = `session:${sessionId}`
  await redisClient.del(sessionKey)
}

function generateSessionId(): string {
  return Date.now().toString(36) + Math.random().toString(36).slice(2)
}
```

```python
# services/session.service.py
import redis_client
import json
from datetime import datetime, timedelta
import uuid

def create_session(user_id: str, user_data: dict, ttl_seconds: int = 3600) -> str:
    session_id = str(uuid.uuid4())
    session_key = f"session:{session_id}"
    
    session_data = {
        "user_id": user_id,
        "user_data": user_data,
        "created_at": datetime.utcnow().isoformat(),
        "last_activity": datetime.utcnow().isoformat(),
    }
    
    # Store session data in hash
    await redis_client.hset(session_key, session_data)
    
    # Set TTL
    await redis_client.expire(session_key, ttl_seconds)
    
    return session_id


async def get_session(session_id: str) -> dict | None:
    session_key = f"session:{session_id}"
    session_data = await redis_client.hgetall(session_key)
    
    if not session_data:
        return None
    
    return session_data


async def update_session_activity(session_id: str) -> None:
    session_key = f"session:{session_id}"
    
    await redis_client.hset(session_key, {
        "last_activity": datetime.utcnow().isoformat()
    })


async def delete_session(session_id: str) -> None:
    session_key = f"session:{session_id}"
    await redis_client.delete(session_key)
```

#### Session with Multiple Devices

```typescript
// services/session.service.ts
export async function createSessionForDevice(
  userId: string,
  deviceId: string,
  userData: any
): Promise<string> {
  const sessionId = generateSessionId()
  const sessionKey = `session:${sessionId}:device:${deviceId}`
  
  const sessionData = {
    userId,
    deviceId,
    userData,
    createdAt: new Date().toISOString(),
    lastActivity: new Date().toISOString(),
  }
  
  await redisClient.hSet(sessionKey, sessionData)
  await redisClient.expire(sessionKey, 3600)
  
  return sessionId
}

export async function getUserSessions(userId: string): Promise<string[]> {
  const pattern = `session:*:user:${userId}`
  const keys = await redisClient.keys(pattern)
  
  return keys
}
```

### Rate Limiting with Redis

#### Fixed Window Rate Limiter

```typescript
// services/ratelimit.service.ts
import { redisClient } from '../config/redis'

export async function checkRateLimit(
  identifier: string,
  limit: number,
  windowMs: number
): Promise<boolean> {
  const key = `ratelimit:${identifier}`
  const current = await redisClient.incr(key)
  
  if (current > limit) {
    return false
  }
  
  // Set expiration for the window
  await redisClient.expire(key, windowMs / 1000)
  
  return true
}

export async function resetRateLimit(identifier: string): Promise<void> {
  await redisClient.del(`ratelimit:${identifier}`)
}

// Usage
async function rateLimiter(
  identifier: string,
  limit: number = 10,
  windowMs: number = 60000 // 1 minute
): Promise<void> {
  const allowed = await checkRateLimit(identifier, limit, windowMs)
  
  if (!allowed) {
    throw new Error('Rate limit exceeded')
  }
  
  // Proceed with operation
}
```

```python
# services/ratelimit.service.py
import redis_client

async def check_rate_limit(identifier: str, limit: int, window_ms: int = 60000) -> bool:
    key = f"ratelimit:{identifier}"
    current = await redis_client.incr(key)
    
    if current > limit:
        return False
    
    # Set expiration for the window
    await redis_client.expire(key, window_ms / 1000)
    
    return True


async def reset_rate_limit(identifier: str) -> None:
    await redis_client.delete(f"ratelimit:{identifier}")


async def rate_limiter(identifier: str, limit: int = 10, window_ms: int = 60000):
    allowed = await check_rate_limit(identifier, limit, window_ms)
    
    if not allowed:
        raise Exception('Rate limit exceeded')
    
    # Proceed with operation
```

#### Sliding Window Rate Limiter

```typescript
// services/ratelimit.service.ts
export async function slidingWindowRateLimit(
  identifier: string,
  limit: number,
  windowMs: number
): Promise<void> {
  const key = `ratelimit:${identifier}`
  
  // Get current count
  const current = await redisClient.incr(key)
  
  if (current > limit) {
    throw new Error('Rate limit exceeded')
  }
  
  // Remove old entries outside window
  const now = Date.now()
  const oldest = await redisClient.zRangeByScore(
    key,
    0,
    Date.now() - windowMs,
    Date.now(),
    'WITHSCORES'
  )
  
  if (oldest.length > 0) {
    await redisClient.zRemRangeByScore(
      key,
      oldest[0].score,
      oldest[oldest.length - 1].score,
      oldest[oldest.length - 1].member
    )
  }
}

// Usage
async function apiRateLimiter(
  identifier: string,
  limit: number = 100,
  windowMs: number = 60000
): Promise<void> {
  await slidingWindowRateLimit(identifier, limit, windowMs)
  
  // Proceed with API call
}
```

```python
async def sliding_window_rate_limit(
    identifier: str,
    limit: int = 100,
    window_ms: int = 60000
) -> None:
    key = f"ratelimit:{identifier}"
    
    # Get current count
    current = await redis_client.incr(key)
    
    if current > limit:
        raise Exception('Rate limit exceeded')
    
    # Remove old entries outside window
    now = int(time.time() * 1000)
    oldest = await redis_client.zrangebyscore(
        key,
        0,
        now - window_ms,
        now,
        withscores=True
    )
    
    if oldest:
        await redis_client.zremrangebyscore(
            key,
            oldest[0].score,
            oldest[oldest.length - 1].score,
            oldest[oldest.length - 1].member
        )
```

## Best Practices

1. **Use Appropriate Data Structures**
   - Use hashes for related fields
   - Use sets for unique collections
   - Use sorted sets for ranked data
   - Use lists for ordered sequences

2. **Always Set TTL**
   - Cache data should always have expiration
   - Use appropriate TTL based on data volatility
   - Consider sliding TTL for frequently accessed data

3. **Use Compression**
   - Compress large data before caching
   - Use efficient serialization formats
   - Consider binary formats for performance

4. **Handle Connection Errors**
   - Implement proper error handling
   - Use connection pooling
   - Set appropriate retry strategies
   - Monitor connection health

5. **Monitor Redis Performance**
   - Track memory usage
   - Monitor hit/miss ratios
   - Watch for slow operations
   - Set up alerts for critical metrics

6. **Use Pipeline for Multiple Operations**
   - Batch multiple operations together
   - Reduce network round trips
   - Improve overall performance

7. **Use Appropriate Serialization**
   - Use JSON for complex objects
   - Consider protocol buffers for high performance
   - Avoid string concatenation for structured data

8. **Key Naming**
   - Use hierarchical naming conventions
   - Include environment prefixes
   - Use consistent patterns
   - Avoid overly long keys

9. **Cache Invalidation**
   - Implement proper invalidation strategies
   - Use pattern-based invalidation carefully
   - Consider tag-based invalidation for complex scenarios

10. **Security**
    - Use authentication in production
    - Encrypt sensitive data
    - Use TLS for network connections
    - Follow principle of least privilege

## Related Skills

- [`04-database/cache-invalidation`](04-database/cache-invalidation/SKILL.md)
- [`04-database/connection-pooling`](04-database/connection-pooling/SKILL.md)
- [`04-database/database-optimization`](04-database/database-optimization/SKILL.md)
- [`04-database/database-transactions`](04-database/database-transactions/SKILL.md)
