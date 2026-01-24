---
name: Database Optimization Techniques
description: Query optimization, indexing strategies, and performance tuning for database systems.
---

# Database Optimization Techniques

## Overview

Database optimization involves improving query performance, reducing resource consumption, and ensuring efficient data access patterns. This skill covers query analysis, indexing strategies, caching, and maintenance practices.

## Prerequisites

- Understanding of SQL and database operations
- Knowledge of database schema design principles
- Familiarity with database management tools
- Basic understanding of performance monitoring

## Key Concepts

### Performance Optimization Areas

1. **Query Optimization**: Writing efficient SQL queries
2. **Indexing Strategies**: Creating and maintaining indexes
3. **Connection Management**: Efficient connection pooling
4. **Caching**: Reducing database load
5. **Schema Design**: Proper normalization and denormalization
6. **Maintenance**: Regular database maintenance tasks

### Performance Metrics

- **Query Response Time**: Time to execute queries
- **Throughput**: Queries per second
- **Resource Usage**: CPU, memory, I/O
- **Lock Contention**: Time spent waiting for locks
- **Cache Hit Ratio**: Percentage of queries served from cache

## Implementation Guide

### Query Optimization

#### EXPLAIN Analysis

```sql
-- Basic EXPLAIN
EXPLAIN
SELECT * FROM users WHERE email = 'user@example.com';

-- EXPLAIN with actual execution (PostgreSQL)
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'user@example.com';

-- EXPLAIN with buffers (PostgreSQL)
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT * FROM users WHERE email = 'user@example.com';

-- EXPLAIN in MySQL
EXPLAIN
SELECT * FROM users WHERE email = 'user@example.com';

-- EXPLAIN in MongoDB
db.users.find({ email: 'user@example.com' }).explain('executionStats');
```

#### Query Planning

```sql
-- Understanding query plans
-- Key metrics to analyze:
-- - Sequential Scan vs Index Scan
-- - Filter conditions
-- - Join types (Nested Loop, Hash Join, Merge Join)
-- - Sort operations
-- - Aggregate operations

-- Example: Analyze a complex query
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name
ORDER BY order_count DESC
LIMIT 10;

-- Look for:
-- 1. Sequential scans on large tables (should use index)
-- 2. High cost estimates
-- 3. Large result sets being materialized
-- 4. Inefficient join strategies
```

#### Join Optimization

```sql
-- Good: Use indexed columns for joins
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Good: Join on indexed columns
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';

-- Bad: Join on non-indexed columns
SELECT u.name, o.total
FROM users u
INNER JOIN orders o ON u.email = o.user_email
WHERE o.status = 'completed';

-- Good: Use appropriate join type
-- INNER JOIN: Only matching rows
-- LEFT JOIN: All from left, matching from right
-- RIGHT JOIN: All from right, matching from left
-- FULL JOIN: All from both tables

-- Good: Filter before joining
SELECT u.name, o.total
FROM users u
INNER JOIN (
    SELECT user_id, total
    FROM orders
    WHERE status = 'completed'
) o ON u.id = o.user_id;
```

### Indexing Strategies

#### B-Tree Indexes

```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Multi-column (composite) index
CREATE INDEX idx_users_name_email ON users(name, email);

-- Index with order
CREATE INDEX idx_orders_status_created ON orders(status, created_at DESC);

-- Unique index
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);

-- Partial index (index only subset of rows)
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- Expression index (index computed values)
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Covering index (include non-indexed columns)
-- PostgreSQL
CREATE INDEX idx_orders_covering ON orders(user_id, status) INCLUDE (total, created_at);
```

#### Composite Indexes

```sql
-- Good: Order columns by selectivity
-- Most selective column first
CREATE INDEX idx_users_status_created ON users(status, created_at);

-- Good: Match query order to index order
-- This query uses the index:
SELECT * FROM users WHERE status = 'active' AND created_at > '2024-01-01';

-- This query doesn't use the index effectively:
SELECT * FROM users WHERE created_at > '2024-01-01' AND status = 'active';

-- Good: Create multiple indexes for different query patterns
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_users_status_created ON users(status, created_at);

-- Bad: Too many columns in composite index
CREATE INDEX idx_users_all ON users(name, email, status, created_at, updated_at);
-- Only the first few columns are used effectively
```

#### Partial Indexes

```sql
-- Index only active users
CREATE INDEX idx_active_users_email ON users(email) WHERE active = true;

-- Index only recent orders
CREATE INDEX idx_recent_orders ON orders(user_id) WHERE created_at > NOW() - INTERVAL '30 days';

-- Index only high-value orders
CREATE INDEX idx_high_value_orders ON orders(user_id) WHERE total > 1000;

-- Benefits:
-- - Smaller index size
-- - Faster index scans
-- - Less maintenance overhead
-- - Better for filtered queries
```

#### Index Maintenance

```sql
-- Rebuild index (PostgreSQL)
REINDEX INDEX idx_users_email;

-- Rebuild all indexes on table (PostgreSQL)
REINDEX TABLE users;

-- Analyze table statistics (PostgreSQL)
ANALYZE users;

-- Analyze table (MySQL)
ANALYZE TABLE users;

-- Optimize table (MySQL)
OPTIMIZE TABLE users;

-- Check index usage (PostgreSQL)
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Find unused indexes (PostgreSQL)
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
AND indexname NOT LIKE '%_pkey';
```

### Connection Pooling

#### Connection Pool Configuration

```typescript
// Prisma connection pool
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  // Connection pool settings
  connection_limit = 10  // Max connections
  pool_timeout = 20      // Seconds to wait for connection
}

// PostgreSQL pool configuration
const pool = new Pool({
  host: 'localhost',
  port: 5432,
  database: 'mydb',
  user: 'postgres',
  password: 'password',
  max: 20,              // Maximum pool size
  min: 2,               // Minimum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```

#### Connection Pool Best Practices

```typescript
// Good: Use connection pool
const pool = new Pool({
  max: 20,
  min: 2,
  idleTimeoutMillis: 30000,
});

// Bad: Create new connection for each query
async function getUser(id: string) {
  const client = new Client({ /* config */ });
  await client.connect();
  const result = await client.query('SELECT * FROM users WHERE id = $1', [id]);
  await client.end();
  return result.rows[0];
}

// Good: Use pool for queries
async function getUser(id: string) {
  const result = await pool.query('SELECT * FROM users WHERE id = $1', [id]);
  return result.rows[0];
}
```

### N+1 Query Problem

#### Identifying N+1 Problem

```typescript
// Bad: N+1 query problem
async function getUsersWithOrders() {
  const users = await db.user.findMany(); // 1 query

  const usersWithOrders = [];
  for (const user of users) {
    const orders = await db.order.findMany({ // N queries
      where: { userId: user.id }
    });
    usersWithOrders.push({ ...user, orders });
  }

  return usersWithOrders;
}

// Total queries: 1 + N (where N is number of users)
```

#### Solving N+1 with Joins

```typescript
// Good: Use JOIN
async function getUsersWithOrders() {
  const result = await db.$queryRaw`
    SELECT
      u.id, u.name, u.email,
      o.id as order_id, o.total, o.status
    FROM users u
    LEFT JOIN orders o ON u.id = o.user_id
  `;

  // Transform result to nested structure
  const usersMap = new Map();
  for (const row of result) {
    if (!usersMap.has(row.id)) {
      usersMap.set(row.id, {
        id: row.id,
        name: row.name,
        email: row.email,
        orders: []
      });
    }
    if (row.order_id) {
      usersMap.get(row.id).orders.push({
        id: row.order_id,
        total: row.total,
        status: row.status
      });
    }
  }

  return Array.from(usersMap.values());
}

// Total queries: 1
```

#### Solving N+1 with Include

```typescript
// Good: Prisma include
async function getUsersWithOrders() {
  return await db.user.findMany({
    include: {
      orders: true
    }
  });
}

// Good: Mongoose populate
async function getUsersWithOrders() {
  return await User.find().populate('orders');
}
```

#### Solving N+1 with Batch Loading

```typescript
// Good: Batch loading
async function getUsersWithOrders() {
  const users = await db.user.findMany();
  const userIds = users.map(u => u.id);

  const orders = await db.order.findMany({
    where: { userId: { in: userIds } }
  });

  const ordersMap = new Map();
  orders.forEach(order => {
    if (!ordersMap.has(order.userId)) {
      ordersMap.set(order.userId, []);
    }
    ordersMap.get(order.userId).push(order);
  });

  return users.map(user => ({
    ...user,
    orders: ordersMap.get(user.id) || []
  }));
}

// Total queries: 2
```

### Caching Strategies

#### Query Result Caching

```typescript
// Cache query results with Redis
import { redisClient } from './redis';

async function getCachedUser(userId: string) {
  const cacheKey = `user:${userId}`;

  // Try cache first
  const cached = await redisClient.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Cache miss - query database
  const user = await db.user.findUnique({ where: { id: userId } });

  // Store in cache with 1 hour TTL
  await redisClient.set(cacheKey, JSON.stringify(user), {
    EX: 3600
  });

  return user;
}
```

#### Cache Invalidation

```typescript
// Invalidate cache on update
async function updateUser(userId: string, data: any) {
  const user = await db.user.update({
    where: { id: userId },
    data
  });

  // Invalidate cache
  await redisClient.del(`user:${userId}`);

  return user;
}

// Invalidate multiple caches
async function invalidateUserCaches(userId: string) {
  await redisClient.del(`user:${userId}`);
  await redisClient.del(`user:${userId}:profile`);
  await redisClient.del(`user:${userId}:orders`);
}
```

#### Cache-Aside Pattern

```typescript
// Cache-aside implementation
class CacheAside {
  async get(key: string) {
    // 1. Try cache
    const cached = await redisClient.get(key);
    if (cached) {
      return JSON.parse(cached);
    }

    // 2. Cache miss - load from database
    const data = await this.loadFromDatabase(key);

    // 3. Populate cache
    await redisClient.set(key, JSON.stringify(data), { EX: 3600 });

    return data;
  }

  async set(key: string, data: any) {
    // Update database
    await this.saveToDatabase(key, data);

    // Update cache
    await redisClient.set(key, JSON.stringify(data), { EX: 3600 });
  }

  async delete(key: string) {
    // Delete from database
    await this.deleteFromDatabase(key);

    // Invalidate cache
    await redisClient.del(key);
  }
}
```

### Denormalization When Needed

#### When to Denormalize

```sql
-- Good: Denormalize for read-heavy workloads
-- Add redundant data to avoid joins

-- Normalized schema
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255)
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP
);

-- Denormalized schema for fast reads
CREATE TABLE orders_denormalized (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    user_name VARCHAR(255),  -- Denormalized
    user_email VARCHAR(255),   -- Denormalized
    total DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP
);

-- Good: Use materialized views for complex aggregations
CREATE MATERIALIZED VIEW user_order_summary AS
SELECT
    u.id,
    u.name,
    u.email,
    COUNT(o.id) as order_count,
    SUM(o.total) as total_spent,
    MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name, u.email;

-- Refresh materialized view
REFRESH MATERIALIZED VIEW user_order_summary;
```

#### Trade-offs

```sql
-- Benefits of denormalization:
-- - Faster read queries (no joins)
-- - Simpler queries
-- - Better for reporting

-- Drawbacks of denormalization:
-- - Data redundancy
-- - Update anomalies
-- - Increased storage
-- - Complex data synchronization
```

### Partitioning

#### Table Partitioning (PostgreSQL)

```sql
-- Range partitioning by date
CREATE TABLE orders (
    id SERIAL,
    user_id INTEGER,
    total DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create partitions
CREATE TABLE orders_2024_q1 PARTITION OF orders
    FOR VALUES FROM ('2024-01-01') TO ('2024-04-01');

CREATE TABLE orders_2024_q2 PARTITION OF orders
    FOR VALUES FROM ('2024-04-01') TO ('2024-07-01');

CREATE TABLE orders_2024_q3 PARTITION OF orders
    FOR VALUES FROM ('2024-07-01') TO ('2024-10-01');

CREATE TABLE orders_2024_q4 PARTITION OF orders
    FOR VALUES FROM ('2024-10-01') TO ('2025-01-01');

-- List partitioning
CREATE TABLE orders_by_status (
    id SERIAL,
    user_id INTEGER,
    total DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP
) PARTITION BY LIST (status);

CREATE TABLE orders_active PARTITION OF orders_by_status
    FOR VALUES IN ('pending', 'processing');

CREATE TABLE orders_completed PARTITION OF orders_by_status
    FOR VALUES IN ('completed');

CREATE TABLE orders_cancelled PARTITION OF orders_by_status
    FOR VALUES IN ('cancelled', 'refunded');

-- Hash partitioning
CREATE TABLE orders_hash (
    id SERIAL,
    user_id INTEGER,
    total DECIMAL(10, 2),
    status VARCHAR(50),
    created_at TIMESTAMP
) PARTITION BY HASH (user_id);

CREATE TABLE orders_hash_0 PARTITION OF orders_hash
    FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE orders_hash_1 PARTITION OF orders_hash
    FOR VALUES WITH (MODULUS 4, REMAINDER 1);

CREATE TABLE orders_hash_2 PARTITION OF orders_hash
    FOR VALUES WITH (MODULUS 4, REMAINDER 2);

CREATE TABLE orders_hash_3 PARTITION OF orders_hash
    FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

#### Partition Pruning

```sql
-- Query benefits from partition pruning
-- Only relevant partitions are scanned

-- Good: Query with partition key
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE created_at >= '2024-01-01' AND created_at < '2024-04-01';
-- Only scans orders_2024_q1 partition

-- Bad: Query without partition key
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE total > 1000;
-- Scans all partitions
```

### Database Maintenance

#### Vacuum and Analyze

```sql
-- Vacuum (PostgreSQL)
-- Reclaims storage and updates statistics
VACUUM users;

-- Vacuum with analyze
VACUUM ANALYZE users;

-- Vacuum all tables
VACUUM ANALYZE;

-- Vacuum specific table with full option
VACUUM FULL users;  -- Reclaims more space but locks table

-- Auto-vacuum configuration (PostgreSQL)
ALTER SYSTEM SET autovacuum = on;
ALTER SYSTEM SET autovacuum_vacuum_threshold = 50;
ALTER SYSTEM SET autovacuum_analyze_threshold = 50;
SELECT pg_reload_conf();
```

#### Reindexing

```sql
-- Reindex single index (PostgreSQL)
REINDEX INDEX idx_users_email;

-- Reindex all indexes on table (PostgreSQL)
REINDEX TABLE users;

-- Reindex concurrently (PostgreSQL)
-- Doesn't lock table but takes longer
REINDEX INDEX CONCURRENTLY idx_users_email;
```

#### Table Optimization

```sql
-- Optimize table (MySQL)
OPTIMIZE TABLE users;

-- Optimize table (SQLite)
VACUUM;

-- Analyze table (MySQL)
ANALYZE TABLE users;

-- Check table integrity (MySQL)
CHECK TABLE users;
```

## Monitoring Queries

### Slow Query Logging

```sql
-- Enable slow query logging (PostgreSQL)
ALTER SYSTEM SET log_min_duration_statement = 1000; -- Log queries > 1 second
SELECT pg_reload_conf();

-- View slow queries
SELECT
    query,
    calls,
    total_time,
    mean_time,
    max_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Enable slow query log (MySQL)
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1; -- Log queries > 1 second
SET GLOBAL slow_query_log_file = '/var/log/mysql/slow-query.log';
```

### Query Performance Monitoring

```sql
-- Find most time-consuming queries (PostgreSQL)
SELECT
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Find most frequent queries (PostgreSQL)
SELECT
    query,
    calls,
    total_exec_time
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 20;

-- Monitor query execution (MySQL)
SHOW PROFILE;
SHOW PROFILE FOR QUERY 1;
```

### Database Metrics

```sql
-- Connection usage (PostgreSQL)
SELECT
    state,
    COUNT(*) as count
FROM pg_stat_activity
GROUP BY state;

-- Table sizes (PostgreSQL)
SELECT
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Index sizes (PostgreSQL)
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 20;
```

## Common Anti-Patterns

### SELECT *

```sql
-- Bad: SELECT * retrieves all columns
SELECT * FROM users WHERE id = 1;

-- Good: Select only needed columns
SELECT id, name, email FROM users WHERE id = 1;

-- Benefits:
-- - Less data transferred
-- - Less memory used
-- - Can use covering indexes
```

### Wildcard Prefix Matching

```sql
-- Bad: Leading wildcard prevents index usage
SELECT * FROM users WHERE name LIKE '%Smith%';

-- Good: Use full-text search
SELECT * FROM users WHERE to_tsvector('english', name) @@ to_tsquery('english', 'Smith');

-- Good: Use trigram extension (PostgreSQL)
CREATE EXTENSION pg_trgm;
CREATE INDEX idx_users_name_trgm ON users USING gin (name gin_trgm_ops);
SELECT * FROM users WHERE name LIKE '%Smith%';
```

### OR Conditions

```sql
-- Bad: OR conditions can prevent index usage
SELECT * FROM users WHERE email = 'user@example.com' OR name = 'John';

-- Good: Use UNION
SELECT * FROM users WHERE email = 'user@example.com'
UNION
SELECT * FROM users WHERE name = 'John';

-- Good: Use IN clause
SELECT * FROM users WHERE email IN ('user@example.com', 'user2@example.com');
```

### Subqueries

```sql
-- Bad: Subquery can be inefficient
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders WHERE total > 1000);

-- Good: Use JOIN
SELECT DISTINCT u.*
FROM users u
INNER JOIN orders o ON u.id = o.user_id
WHERE o.total > 1000;

-- Good: Use EXISTS
SELECT u.*
FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id AND o.total > 1000
);
```

### Functions on Indexed Columns

```sql
-- Bad: Function on indexed column prevents index usage
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Good: Store data in normalized form
SELECT * FROM users WHERE email = 'user@example.com';

-- Good: Use expression index
CREATE INDEX idx_users_lower_email ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';
```

### Large Transactions

```typescript
// Bad: Large transaction holds locks too long
async function processLargeBatch() {
  const transaction = await db.$transaction([
    db.user.create({ data: user1 }),
    db.user.create({ data: user2 }),
    db.user.create({ data: user3 }),
    // ... 1000 more operations
  ]);
}

// Good: Process in smaller batches
async function processInBatches(users: any[]) {
  const batchSize = 100;
  for (let i = 0; i < users.length; i += batchSize) {
    const batch = users.slice(i, i + batchSize);
    await db.$transaction(
      batch.map(user => db.user.create({ data: user }))
    );
  }
}
```

### Missing Indexes

```sql
-- Bad: No index on frequently queried column
SELECT * FROM orders WHERE user_id = 123;

-- Good: Create index
CREATE INDEX idx_orders_user_id ON orders(user_id);

-- Bad: No index on foreign keys
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),  -- No index
    total DECIMAL(10, 2)
);

-- Good: Always index foreign keys
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    total DECIMAL(10, 2)
);
CREATE INDEX idx_orders_user_id ON orders(user_id);
```

### Over-Indexing

```sql
-- Bad: Too many indexes slow down writes
CREATE INDEX idx_users_name ON users(name);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status ON users(status);
CREATE INDEX idx_users_created ON users(created_at);
CREATE INDEX idx_users_updated ON users(updated_at);
CREATE INDEX idx_users_name_email ON users(name, email);
CREATE INDEX idx_users_email_name ON users(email, name);
-- ... more indexes

-- Good: Create only necessary indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_status_created ON users(status, created_at);
```

## Best Practices

1. **Query Optimization**
   - Use EXPLAIN to analyze query plans
   - Select only needed columns
   - Use appropriate join types
   - Avoid functions on indexed columns

2. **Indexing Strategy**
   - Create indexes on frequently queried columns
   - Use composite indexes for multi-column queries
   - Consider partial indexes for filtered queries
   - Monitor and remove unused indexes

3. **Connection Management**
   - Use connection pooling
   - Configure appropriate pool size
   - Set connection timeouts
   - Monitor connection usage

4. **Caching**
   - Cache frequently accessed data
   - Implement proper cache invalidation
   - Use appropriate TTL values
   - Monitor cache hit rates

5. **Maintenance**
   - Regular vacuum and analyze operations
   - Monitor slow queries
   - Rebuild indexes periodically
   - Keep statistics up to date

## Related Skills

- [`04-database/connection-pooling`](04-database/connection-pooling/SKILL.md)
- [`04-database/cache-invalidation`](04-database/cache-invalidation/SKILL.md)
- [`47-performance-engineering/caching-strategies`](47-performance-engineering/caching-strategies/SKILL.md)
- [`14-monitoring-observability/prometheus-metrics`](14-monitoring-observability/prometheus-metrics/SKILL.md)
