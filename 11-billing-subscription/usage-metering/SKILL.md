# Usage Metering

## Overview

Comprehensive guide to API usage metering, tracking, and quota enforcement for billing purposes.

## Table of Contents

1. [Metering Concepts](#metering-concepts)
2. [Tracking Mechanisms](#tracking-mechanisms)
3. [Storage Strategies](#storage-strategies)
4. [Quota Enforcement](#quota-enforcement)
5. [Rate Limiting Integration](#rate-limiting-integration)
6. [Usage Reports](#usage-reports)
7. [Billing Integration](#billing-integration)
8. [Anomaly Detection](#anomaly-detection)
9. [Usage Alerts](#usage-alerts)
10. [Performance Optimization](#performance-optimization)
11. [Data Retention](#data-retention)
12. [Production Patterns](#production-patterns)

---

## Metering Concepts

### Core Concepts

```typescript
// metering-concepts.ts

/**
 * Usage Metering Core Concepts
 * 
 * 1. Metrics: What to measure (API calls, storage, bandwidth, etc.)
 * 2. Dimensions: How to group (by user, by endpoint, by time period)
 * 3. Granularity: How often to record (real-time, hourly, daily)
 * 4. Aggregation: How to summarize (sum, average, max, count)
 * 5. Retention: How long to keep data
 * 6. Billing: How usage maps to charges
 */

export interface UsageMetric {
  userId: string;
  metric: string;
  quantity: number;
  timestamp: Date;
  metadata?: Record<string, any>;
}

export interface UsageQuota {
  userId: string;
  metric: string;
  limit: number;
  period: 'hourly' | 'daily' | 'monthly';
  current: number;
  resetAt: Date;
}

export interface UsageReport {
  userId: string;
  period: {
    start: Date;
    end: Date;
  };
  metrics: Record<string, {
    total: number;
    breakdown: Record<string, number>;
  }>;
  cost: number;
}

export interface UsageAlert {
  id: string;
  userId: string;
  metric: string;
  threshold: number;
  current: number;
  severity: 'warning' | 'critical';
  triggeredAt: Date;
  acknowledged: boolean;
}
```

---

## Tracking Mechanisms

### Middleware-Based Tracking

```typescript
// middleware-tracking.ts
import { Request, Response, NextFunction } from 'express';
import { Redis } from 'ioredis';

export class UsageTrackingMiddleware {
  constructor(private redis: Redis) {}
  
  middleware = async (req: Request, res: Response, next: NextFunction) => {
    const startTime = Date.now();
    const userId = req.user?.id || 'anonymous';
    
    // Track API call
    await this.trackApiCall(userId, req.method, req.path);
    
    // Track on response
    res.on('finish', async () => {
      const duration = Date.now() - startTime;
      const statusCode = res.statusCode;
      
      await this.trackApiCallComplete(
        userId,
        req.method,
        req.path,
        statusCode,
        duration
      );
    });
    
    next();
  };
  
  private async trackApiCall(
    userId: string,
    method: string,
    path: string
  ): Promise<void> {
    const metric = 'api_calls';
    const key = `usage:${userId}:${metric}:${this.getPeriodKey('daily')}`;
    
    await this.redis.incr(key);
    await this.redis.expire(key, 86400); // 24 hours
    
    // Track by endpoint
    const endpointKey = `usage:${userId}:${metric}:${method}:${path}:${this.getPeriodKey('daily')}`;
    await this.redis.incr(endpointKey);
    await this.redis.expire(endpointKey, 86400);
  }
  
  private async trackApiCallComplete(
    userId: string,
    method: string,
    path: string,
    statusCode: number,
    duration: number
  ): Promise<void> {
    // Track response time
    const latencyMetric = 'api_latency_ms';
    const latencyKey = `usage:${userId}:${latencyMetric}:${this.getPeriodKey('daily')}`;
    await this.redis.incrbyfloat(latencyKey, duration);
    await this.redis.expire(latencyKey, 86400);
    
    // Track errors
    if (statusCode >= 400) {
      const errorMetric = 'api_errors';
      const errorKey = `usage:${userId}:${errorMetric}:${this.getPeriodKey('daily')}`;
      await this.redis.incr(errorKey);
      await this.redis.expire(errorKey, 86400);
    }
  }
  
  private getPeriodKey(period: 'hourly' | 'daily' | 'monthly'): string {
    const now = new Date();
    if (period === 'hourly') {
      return `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}-${now.getHours()}`;
    } else if (period === 'daily') {
      return `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}`;
    } else {
      return `${now.getFullYear()}-${now.getMonth() + 1}`;
    }
  }
}

// Express integration
import express from 'express';

const app = express();
const redis = new Redis();
const usageTracking = new UsageTrackingMiddleware(redis);

app.use(usageTracking.middleware);
```

### Event-Based Tracking

```typescript
// event-tracking.ts
import { EventEmitter } from 'events';

export class UsageEventTracker extends EventEmitter {
  private eventQueue: Array<UsageMetric> = [];
  private flushInterval: NodeJS.Timeout | null = null;
  
  constructor(
    private flushIntervalMs: number = 5000,
    private batchSize: number = 100
  ) {
    super();
    this.startFlushTimer();
  }
  
  track(metric: UsageMetric): void {
    this.eventQueue.push(metric);
    
    if (this.eventQueue.length >= this.batchSize) {
      this.flush();
    }
  }
  
  trackApiCall(userId: string, endpoint: string, metadata?: Record<string, any>): void {
    this.track({
      userId,
      metric: 'api_calls',
      quantity: 1,
      timestamp: new Date(),
      metadata: { endpoint, ...metadata }
    });
  }
  
  trackStorageUsage(userId: string, bytes: number, metadata?: Record<string, any>): void {
    this.track({
      userId,
      metric: 'storage_bytes',
      quantity: bytes,
      timestamp: new Date(),
      metadata
    });
  }
  
  trackBandwidthUsage(userId: string, bytes: number, metadata?: Record<string, any>): void {
    this.track({
      userId,
      metric: 'bandwidth_bytes',
      quantity: bytes,
      timestamp: new Date(),
      metadata
    });
  }
  
  trackTokenUsage(userId: string, tokens: number, metadata?: Record<string, any>): void {
    this.track({
      userId,
      metric: 'llm_tokens',
      quantity: tokens,
      timestamp: new Date(),
      metadata
    });
  }
  
  private async flush(): Promise<void> {
    if (this.eventQueue.length === 0) return;
    
    const batch = [...this.eventQueue];
    this.eventQueue = [];
    
    this.emit('flush', batch);
    
    // Process batch
    await this.processBatch(batch);
  }
  
  private async processBatch(batch: UsageMetric[]): Promise<void> {
    // Implement batch processing (e.g., write to database, send to analytics)
    console.log(`Processing ${batch.length} usage metrics`);
  }
  
  private startFlushTimer(): void {
    this.flushInterval = setInterval(() => {
      this.flush();
    }, this.flushIntervalMs);
  }
  
  stop(): void {
    if (this.flushInterval) {
      clearInterval(this.flushInterval);
      this.flushInterval = null;
    }
    this.flush();
  }
}

// Usage example
const tracker = new UsageEventTracker();

tracker.on('flush', (batch) => {
  console.log(`Flushing ${batch.length} metrics`);
});

// Track events
tracker.trackApiCall('user_123', '/api/v1/users', { method: 'GET' });
tracker.trackTokenUsage('user_123', 1500, { model: 'gpt-4' });
```

---

## Storage Strategies

### Real-Time Counters (Redis)

```typescript
// redis-storage.ts
import { Redis } from 'ioredis';

export class RedisUsageStorage {
  constructor(private redis: Redis) {}
  
  async increment(
    userId: string,
    metric: string,
    quantity: number = 1,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<number> {
    const key = this.getKey(userId, metric, period);
    const newValue = await this.redis.incrby(key, quantity);
    await this.redis.expire(key, this.getTTL(period));
    return newValue;
  }
  
  async get(
    userId: string,
    metric: string,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<number> {
    const key = this.getKey(userId, metric, period);
    const value = await this.redis.get(key);
    return value ? parseInt(value, 10) : 0;
  }
  
  async getRange(
    userId: string,
    metric: string,
    start: Date,
    end: Date,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<number> {
    const keys = this.getKeysInRange(userId, metric, start, end, period);
    if (keys.length === 0) return 0;
    
    const values = await this.redis.mget(keys);
    return values.reduce((sum, val) => sum + (val ? parseInt(val, 10) : 0), 0);
  }
  
  async reset(
    userId: string,
    metric: string,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<void> {
    const key = this.getKey(userId, metric, period);
    await this.redis.del(key);
  }
  
  private getKey(userId: string, metric: string, period: string): string {
    const periodKey = this.getPeriodKey(period);
    return `usage:${userId}:${metric}:${periodKey}`;
  }
  
  private getKeysInRange(
    userId: string,
    metric: string,
    start: Date,
    end: Date,
    period: string
  ): string[] {
    const keys: string[] = [];
    const current = new Date(start);
    
    while (current <= end) {
      const periodKey = this.getPeriodKeyForDate(current, period);
      keys.push(`usage:${userId}:${metric}:${periodKey}`);
      
      if (period === 'hourly') {
        current.setHours(current.getHours() + 1);
      } else if (period === 'daily') {
        current.setDate(current.getDate() + 1);
      } else {
        current.setMonth(current.getMonth() + 1);
      }
    }
    
    return keys;
  }
  
  private getPeriodKey(period: string): string {
    return this.getPeriodKeyForDate(new Date(), period);
  }
  
  private getPeriodKeyForDate(date: Date, period: string): string {
    if (period === 'hourly') {
      return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}-${date.getHours()}`;
    } else if (period === 'daily') {
      return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`;
    } else {
      return `${date.getFullYear()}-${date.getMonth() + 1}`;
    }
  }
  
  private getTTL(period: string): number {
    if (period === 'hourly') return 3600; // 1 hour
    if (period === 'daily') return 86400; // 24 hours
    return 2592000; // 30 days
  }
}
```

### Aggregated Data (TimescaleDB)

```sql
-- timescale-schema.sql

-- Create hypertable for time-series data
CREATE TABLE usage_metrics (
  time TIMESTAMPTZ NOT NULL,
  user_id UUID NOT NULL,
  metric VARCHAR(255) NOT NULL,
  quantity INTEGER NOT NULL,
  metadata JSONB DEFAULT '{}'
);

SELECT create_hypertable('usage_metrics', 'time');

-- Create indexes
CREATE INDEX idx_usage_metrics_user_id ON usage_metrics(user_id);
CREATE INDEX idx_usage_metrics_metric ON usage_metrics(metric);
CREATE INDEX idx_usage_metrics_time ON usage_metrics(time DESC);

-- Create continuous aggregates for hourly data
CREATE MATERIALIZED VIEW usage_metrics_hourly
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 hour', time) AS bucket,
  user_id,
  metric,
  SUM(quantity) AS total_quantity,
  COUNT(*) AS count
FROM usage_metrics
GROUP BY bucket, user_id, metric;

-- Create continuous aggregates for daily data
CREATE MATERIALIZED VIEW usage_metrics_daily
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 day', time) AS bucket,
  user_id,
  metric,
  SUM(quantity) AS total_quantity,
  COUNT(*) AS count
FROM usage_metrics
GROUP BY bucket, user_id, metric;

-- Create refresh policy
SELECT add_continuous_aggregate_policy('usage_metrics_hourly',
  start_offset => INTERVAL '3 hours',
  end_offset => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour'
);

SELECT add_continuous_aggregate_policy('usage_metrics_daily',
  start_offset => INTERVAL '3 days',
  end_offset => INTERVAL '1 day',
  schedule_interval => INTERVAL '1 day'
);
```

```typescript
// timescale-storage.ts
import { Pool } from 'pg';

export class TimescaleUsageStorage {
  constructor(private pool: Pool) {}
  
  async insertMetric(metric: UsageMetric): Promise<void> {
    await this.pool.query(
      `INSERT INTO usage_metrics (time, user_id, metric, quantity, metadata)
       VALUES ($1, $2, $3, $4, $5)`,
      [metric.timestamp, metric.userId, metric.metric, metric.quantity, metric.metadata || {}]
    );
  }
  
  async insertBatch(metrics: UsageMetric[]): Promise<void> {
    const client = await this.pool.connect();
    try {
      await client.query('BEGIN');
      
      for (const metric of metrics) {
        await client.query(
          `INSERT INTO usage_metrics (time, user_id, metric, quantity, metadata)
           VALUES ($1, $2, $3, $4, $5)`,
          [metric.timestamp, metric.userId, metric.metric, metric.quantity, metric.metadata || {}]
        );
      }
      
      await client.query('COMMIT');
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }
  
  async getUsage(
    userId: string,
    metric: string,
    start: Date,
    end: Date
  ): Promise<number> {
    const result = await this.pool.query(
      `SELECT SUM(quantity) as total
       FROM usage_metrics
       WHERE user_id = $1 AND metric = $2 AND time >= $3 AND time <= $4`,
      [userId, metric, start, end]
    );
    
    return result.rows[0].total || 0;
  }
  
  async getUsageByHour(
    userId: string,
    metric: string,
    start: Date,
    end: Date
  ): Promise<Array<{ bucket: Date; total: number }>> {
    const result = await this.pool.query(
      `SELECT bucket, SUM(total_quantity) as total
       FROM usage_metrics_hourly
       WHERE user_id = $1 AND metric = $2 AND bucket >= $3 AND bucket <= $4
       GROUP BY bucket
       ORDER BY bucket`,
      [userId, metric, start, end]
    );
    
    return result.rows;
  }
  
  async getUsageByDay(
    userId: string,
    metric: string,
    start: Date,
    end: Date
  ): Promise<Array<{ bucket: Date; total: number }>> {
    const result = await this.pool.query(
      `SELECT bucket, SUM(total_quantity) as total
       FROM usage_metrics_daily
       WHERE user_id = $1 AND metric = $2 AND bucket >= $3 AND bucket <= $4
       GROUP BY bucket
       ORDER BY bucket`,
      [userId, metric, start, end]
    );
    
    return result.rows;
  }
  
  async getAllMetrics(
    userId: string,
    start: Date,
    end: Date
  ): Promise<Record<string, number>> {
    const result = await this.pool.query(
      `SELECT metric, SUM(quantity) as total
       FROM usage_metrics
       WHERE user_id = $1 AND time >= $2 AND time <= $3
       GROUP BY metric`,
      [userId, start, end]
    );
    
    const metrics: Record<string, number> = {};
    for (const row of result.rows) {
      metrics[row.metric] = row.total;
    }
    
    return metrics;
  }
}
```

---

## Quota Enforcement

### Quota Service

```typescript
// quota-service.ts
import { Redis } from 'ioredis';

export class QuotaService {
  constructor(private redis: Redis) {}
  
  async checkQuota(
    userId: string,
    metric: string,
    quantity: number = 1,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<{ allowed: boolean; remaining: number; resetAt: Date }> {
    const quota = await this.getQuota(userId, metric, period);
    const current = await this.getCurrentUsage(userId, metric, period);
    const remaining = quota.limit - current;
    
    const allowed = remaining >= quantity;
    const resetAt = this.getResetAt(period);
    
    return { allowed, remaining, resetAt };
  }
  
  async checkAndConsume(
    userId: string,
    metric: string,
    quantity: number = 1,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<{ allowed: boolean; remaining: number; resetAt: Date }> {
    const result = await this.checkQuota(userId, metric, quantity, period);
    
    if (result.allowed) {
      await this.incrementUsage(userId, metric, quantity, period);
    }
    
    return result;
  }
  
  async setQuota(
    userId: string,
    metric: string,
    limit: number,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<void> {
    const key = `quota:${userId}:${metric}:${period}`;
    await this.redis.set(key, limit);
    await this.redis.expire(key, this.getTTL(period));
  }
  
  async getQuota(
    userId: string,
    metric: string,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<{ limit: number; period: string }> {
    const key = `quota:${userId}:${metric}:${period}`;
    const value = await this.redis.get(key);
    
    // Default quota if not set
    const limit = value ? parseInt(value, 10) : this.getDefaultQuota(metric, period);
    
    return { limit, period };
  }
  
  async resetQuota(
    userId: string,
    metric: string,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<void> {
    const usageKey = `usage:${userId}:${metric}:${this.getPeriodKey(period)}`;
    await this.redis.del(usageKey);
  }
  
  private async getCurrentUsage(
    userId: string,
    metric: string,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<number> {
    const key = `usage:${userId}:${metric}:${this.getPeriodKey(period)}`;
    const value = await this.redis.get(key);
    return value ? parseInt(value, 10) : 0;
  }
  
  private async incrementUsage(
    userId: string,
    metric: string,
    quantity: number,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<number> {
    const key = `usage:${userId}:${metric}:${this.getPeriodKey(period)}`;
    const newValue = await this.redis.incrby(key, quantity);
    await this.redis.expire(key, this.getTTL(period));
    return newValue;
  }
  
  private getPeriodKey(period: 'hourly' | 'daily' | 'monthly'): string {
    const now = new Date();
    if (period === 'hourly') {
      return `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}-${now.getHours()}`;
    } else if (period === 'daily') {
      return `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}`;
    } else {
      return `${now.getFullYear()}-${now.getMonth() + 1}`;
    }
  }
  
  private getResetAt(period: 'hourly' | 'daily' | 'monthly'): Date {
    const now = new Date();
    if (period === 'hourly') {
      return new Date(now.setHours(now.getHours() + 1, 0, 0, 0));
    } else if (period === 'daily') {
      return new Date(now.setHours(24, 0, 0, 0));
    } else {
      return new Date(now.getFullYear(), now.getMonth() + 1, 1);
    }
  }
  
  private getTTL(period: 'hourly' | 'daily' | 'monthly'): number {
    if (period === 'hourly') return 3600;
    if (period === 'daily') return 86400;
    return 2592000;
  }
  
  private getDefaultQuota(metric: string, period: string): number {
    // Define default quotas per metric
    const defaults: Record<string, Record<string, number>> = {
      api_calls: { hourly: 1000, daily: 10000, monthly: 300000 },
      storage_bytes: { daily: 10 * 1024 * 1024 * 1024, monthly: 100 * 1024 * 1024 * 1024 },
      bandwidth_bytes: { daily: 100 * 1024 * 1024 * 1024, monthly: 3 * 1024 * 1024 * 1024 * 1024 },
      llm_tokens: { daily: 100000, monthly: 3000000 }
    };
    
    return defaults[metric]?.[period] || 1000;
  }
}
```

---

## Rate Limiting Integration

### Rate Limiting with Quota

```typescript
// rate-limiting-quota.ts
import { Request, Response, NextFunction } from 'express';
import { QuotaService } from './quota-service';

export class RateLimitingMiddleware {
  constructor(private quotaService: QuotaService) {}
  
  middleware = (metric: string, period: 'hourly' | 'daily' | 'monthly' = 'daily') => {
    return async (req: Request, res: Response, next: NextFunction) => {
      const userId = req.user?.id;
      
      if (!userId) {
        return next();
      }
      
      const result = await this.quotaService.checkAndConsume(
        userId,
        metric,
        1,
        period
      );
      
      // Add rate limit headers
      res.setHeader('X-RateLimit-Limit', await this.getQuotaLimit(userId, metric, period));
      res.setHeader('X-RateLimit-Remaining', result.remaining);
      res.setHeader('X-RateLimit-Reset', result.resetAt.getTime() / 1000);
      
      if (!result.allowed) {
        return res.status(429).json({
          error: 'Rate limit exceeded',
          retryAfter: Math.ceil((result.resetAt.getTime() - Date.now()) / 1000)
        });
      }
      
      next();
    };
  };
  
  private async getQuotaLimit(
    userId: string,
    metric: string,
    period: 'hourly' | 'daily' | 'monthly'
  ): Promise<number> {
    const quota = await this.quotaService.getQuota(userId, metric, period);
    return quota.limit;
  }
}

// Express integration
import express from 'express';

const app = express();
const quotaService = new QuotaService(redis);
const rateLimiting = new RateLimitingMiddleware(quotaService);

// Apply rate limiting to specific routes
app.use('/api/v1', rateLimiting.middleware('api_calls', 'daily'));
```

---

## Usage Reports

### Report Generation

```typescript
// usage-reports.ts
import { Pool } from 'pg';

export class UsageReportService {
  constructor(private pool: Pool) {}
  
  async generateDailyReport(userId: string, date: Date): Promise<UsageReport> {
    const start = new Date(date);
    start.setHours(0, 0, 0, 0);
    const end = new Date(date);
    end.setHours(23, 59, 59, 999);
    
    const metrics = await this.getAllMetrics(userId, start, end);
    const cost = await this.calculateCost(userId, start, end);
    
    return {
      userId,
      period: { start, end },
      metrics,
      cost
    };
  }
  
  async generateMonthlyReport(userId: string, year: number, month: number): Promise<UsageReport> {
    const start = new Date(year, month - 1, 1);
    const end = new Date(year, month, 0, 23, 59, 59, 999);
    
    const metrics = await this.getAllMetrics(userId, start, end);
    const cost = await this.calculateCost(userId, start, end);
    
    return {
      userId,
      period: { start, end },
      metrics,
      cost
    };
  }
  
  async generateUsageBreakdown(
    userId: string,
    start: Date,
    end: Date
  ): Promise<Array<{ metric: string; total: number; details: any[] }>> {
    const result = await this.pool.query(
      `SELECT metric, SUM(quantity) as total
       FROM usage_metrics
       WHERE user_id = $1 AND time >= $2 AND time <= $3
       GROUP BY metric
       ORDER BY total DESC`,
      [userId, start, end]
    );
    
    const breakdown = [];
    
    for (const row of result.rows) {
      const details = await this.pool.query(
        `SELECT time, quantity, metadata
         FROM usage_metrics
         WHERE user_id = $1 AND metric = $2 AND time >= $3 AND time <= $4
         ORDER BY time DESC
         LIMIT 100`,
        [userId, row.metric, start, end]
      );
      
      breakdown.push({
        metric: row.metric,
        total: row.total,
        details: details.rows
      });
    }
    
    return breakdown;
  }
  
  async getTopUsersByMetric(
    metric: string,
    start: Date,
    end: Date,
    limit: number = 10
  ): Promise<Array<{ userId: string; total: number }>> {
    const result = await this.pool.query(
      `SELECT user_id, SUM(quantity) as total
       FROM usage_metrics
       WHERE metric = $1 AND time >= $2 AND time <= $3
       GROUP BY user_id
       ORDER BY total DESC
       LIMIT $4`,
      [metric, start, end, limit]
    );
    
    return result.rows;
  }
  
  async getUsageTrends(
    userId: string,
    metric: string,
    days: number = 30
  ): Promise<Array<{ date: Date; total: number }>> {
    const result = await this.pool.query(
      `SELECT bucket, SUM(total_quantity) as total
       FROM usage_metrics_daily
       WHERE user_id = $1 AND metric = $2 AND bucket >= NOW() - INTERVAL '${days} days'
       GROUP BY bucket
       ORDER BY bucket`,
      [userId, metric]
    );
    
    return result.rows;
  }
  
  private async getAllMetrics(
    userId: string,
    start: Date,
    end: Date
  ): Promise<Record<string, { total: number; breakdown: Record<string, number> }>> {
    const metrics = await this.pool.query(
      `SELECT metric, SUM(quantity) as total
       FROM usage_metrics
       WHERE user_id = $1 AND time >= $2 AND time <= $3
       GROUP BY metric`,
      [userId, start, end]
    );
    
    const result: Record<string, { total: number; breakdown: Record<string, number> }> = {};
    
    for (const row of metrics.rows) {
      // Get breakdown by metadata
      const breakdown = await this.getBreakdown(userId, row.metric, start, end);
      result[row.metric] = {
        total: row.total,
        breakdown
      };
    }
    
    return result;
  }
  
  private async getBreakdown(
    userId: string,
    metric: string,
    start: Date,
    end: Date
  ): Promise<Record<string, number>> {
    const result = await this.pool.query(
      `SELECT metadata, SUM(quantity) as total
       FROM usage_metrics
       WHERE user_id = $1 AND metric = $2 AND time >= $3 AND time <= $4
       GROUP BY metadata
       LIMIT 10`,
      [userId, metric, start, end]
    );
    
    const breakdown: Record<string, number> = {};
    for (const row of result.rows) {
      const key = JSON.stringify(row.metadata);
      breakdown[key] = row.total;
    }
    
    return breakdown;
  }
  
  private async calculateCost(
    userId: string,
    start: Date,
    end: Date
  ): Promise<number> {
    // Implement cost calculation based on pricing tiers
    const metrics = await this.getAllMetrics(userId, start, end);
    let totalCost = 0;
    
    // Example: API calls cost $0.001 per call after 10,000 free calls
    const apiCalls = metrics['api_calls']?.total || 0;
    const freeCalls = 10000;
    const paidCalls = Math.max(0, apiCalls - freeCalls);
    totalCost += paidCalls * 0.001;
    
    // Example: Storage costs $0.10 per GB after 10 GB free
    const storageBytes = metrics['storage_bytes']?.total || 0;
    const freeStorage = 10 * 1024 * 1024 * 1024;
    const paidStorage = Math.max(0, storageBytes - freeStorage);
    const paidStorageGB = paidStorage / (1024 * 1024 * 1024);
    totalCost += paidStorageGB * 0.10;
    
    return totalCost;
  }
}
```

---

## Billing Integration

### Stripe Integration

```typescript
// billing-integration.ts
import Stripe from 'stripe';

export class UsageBasedBilling {
  constructor(private stripe: Stripe) {}
  
  async recordUsage(
    subscriptionItemId: string,
    quantity: number,
    timestamp?: Date
  ): Promise<Stripe.UsageRecord> {
    const usageRecord = await this.stripe.usageRecords.create({
      subscription_item: subscriptionItemId,
      quantity,
      timestamp: timestamp ? Math.floor(timestamp.getTime() / 1000) : undefined,
      action: 'increment'
    });
    
    return usageRecord;
  }
  
  async createUsageBasedSubscription(
    customerId: string,
    priceId: string
  ): Promise<Stripe.Subscription> {
    const subscription = await this.stripe.subscriptions.create({
      customer: customerId,
      items: [{
        price: priceId
      }],
      payment_behavior: 'default_incomplete',
      metadata: {
        billing_type: 'usage_based'
      }
    });
    
    return subscription;
  }
  
  async getUsageSummary(
    subscriptionItemId: string,
    start: Date,
    end: Date
  ): Promise<Stripe.UsageRecordSummary> {
    const summary = await this.stripe.usageRecordSummaries.list({
      subscription_item: subscriptionItemId,
      start: Math.floor(start.getTime() / 1000),
      end: Math.floor(end.getTime() / 1000)
    });
    
    return summary.data[0];
  }
}
```

---

## Anomaly Detection

### Anomaly Detection Service

```typescript
// anomaly-detection.ts
import { Pool } from 'pg';

export class AnomalyDetectionService {
  constructor(private pool: Pool) {}
  
  async detectAnomalies(
    userId: string,
    metric: string,
    threshold: number = 3 // Standard deviations
  ): Promise<Array<{ timestamp: Date; value: number; zscore: number }>> {
    const result = await this.pool.query(
      `SELECT time, quantity
       FROM usage_metrics
       WHERE user_id = $1 AND metric = $2
       ORDER BY time DESC
       LIMIT 100`,
      [userId, metric]
    );
    
    const values = result.rows.map(r => r.quantity);
    const mean = this.calculateMean(values);
    const stdDev = this.calculateStdDev(values, mean);
    
    const anomalies = [];
    
    for (const row of result.rows) {
      const zscore = Math.abs((row.quantity - mean) / stdDev);
      
      if (zscore > threshold) {
        anomalies.push({
          timestamp: row.time,
          value: row.quantity,
          zscore
        });
      }
    }
    
    return anomalies;
  }
  
  async detectSpikes(
    userId: string,
    metric: string,
    multiplier: number = 5
  ): Promise<Array<{ timestamp: Date; value: number; expected: number }>> {
    const result = await this.pool.query(
      `SELECT time, quantity
       FROM usage_metrics
       WHERE user_id = $1 AND metric = $2
       ORDER BY time DESC
       LIMIT 100`,
      [userId, metric]
    );
    
    const values = result.rows.map(r => r.quantity);
    const median = this.calculateMedian(values);
    
    const spikes = [];
    
    for (const row of result.rows) {
      if (row.quantity > median * multiplier) {
        spikes.push({
          timestamp: row.time,
          value: row.quantity,
          expected: median
        });
      }
    }
    
    return spikes;
  }
  
  private calculateMean(values: number[]): number {
    return values.reduce((sum, val) => sum + val, 0) / values.length;
  }
  
  private calculateStdDev(values: number[], mean: number): number {
    const squaredDiffs = values.map(val => Math.pow(val - mean, 2));
    const avgSquaredDiff = squaredDiffs.reduce((sum, val) => sum + val, 0) / values.length;
    return Math.sqrt(avgSquaredDiff);
  }
  
  private calculateMedian(values: number[]): number {
    const sorted = [...values].sort((a, b) => a - b);
    const mid = Math.floor(sorted.length / 2);
    return sorted.length % 2 !== 0 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
  }
}
```

---

## Usage Alerts

### Alert Service

```typescript
// usage-alerts.ts
import { Pool } from 'pg';
import { EventEmitter } from 'events';

export class UsageAlertService extends EventEmitter {
  constructor(private pool: Pool) {
    super();
  }
  
  async checkAlerts(): Promise<void> {
    const users = await this.getActiveUsers();
    
    for (const userId of users) {
      await this.checkUserAlerts(userId);
    }
  }
  
  async checkUserAlerts(userId: string): Promise<void> {
    const alerts = await this.getUserAlerts(userId);
    
    for (const alert of alerts) {
      const current = await this.getCurrentUsage(userId, alert.metric);
      
      if (current >= alert.threshold && !alert.acknowledged) {
        await this.triggerAlert(alert, current);
      }
    }
  }
  
  async createAlert(
    userId: string,
    metric: string,
    threshold: number,
    severity: 'warning' | 'critical' = 'warning'
  ): Promise<void> {
    await this.pool.query(
      `INSERT INTO usage_alerts (user_id, metric, threshold, severity, created_at)
       VALUES ($1, $2, $3, $4, NOW())`,
      [userId, metric, threshold, severity]
    );
  }
  
  async acknowledgeAlert(alertId: string): Promise<void> {
    await this.pool.query(
      `UPDATE usage_alerts SET acknowledged = true WHERE id = $1`,
      [alertId]
    );
  }
  
  private async getActiveUsers(): Promise<string[]> {
    const result = await this.pool.query(
      `SELECT DISTINCT user_id FROM usage_metrics WHERE time >= NOW() - INTERVAL '24 hours'`
    );
    return result.rows.map(r => r.user_id);
  }
  
  private async getUserAlerts(userId: string): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM usage_alerts WHERE user_id = $1 AND acknowledged = false`,
      [userId]
    );
    return result.rows;
  }
  
  private async getCurrentUsage(userId: string, metric: string): Promise<number> {
    // Implement usage retrieval
    return 0;
  }
  
  private async triggerAlert(alert: any, current: number): Promise<void> {
    const alertData: UsageAlert = {
      id: alert.id,
      userId: alert.user_id,
      metric: alert.metric,
      threshold: alert.threshold,
      current,
      severity: alert.severity,
      triggeredAt: new Date(),
      acknowledged: false
    };
    
    this.emit('alert', alertData);
    
    // Send notification
    await this.sendNotification(alertData);
  }
  
  private async sendNotification(alert: UsageAlert): Promise<void> {
    // Implement notification sending (email, Slack, etc.)
    console.log(`Alert triggered for user ${alert.userId}: ${alert.metric} = ${alert.current}/${alert.threshold}`);
  }
}

// SQL for alerts table
/*
CREATE TABLE usage_alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL,
  metric VARCHAR(255) NOT NULL,
  threshold INTEGER NOT NULL,
  severity VARCHAR(20) NOT NULL CHECK (severity IN ('warning', 'critical')),
  acknowledged BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT NOW()
);
*/
```

---

## Performance Optimization

### Optimization Strategies

```typescript
// optimization.ts
import { Redis } from 'ioredis';

export class UsageOptimization {
  constructor(private redis: Redis) {}
  
  async batchIncrement(
    operations: Array<{ userId: string; metric: string; quantity: number }>
  ): Promise<void> {
    const pipeline = this.redis.pipeline();
    
    for (const op of operations) {
      const key = `usage:${op.userId}:${op.metric}:${this.getPeriodKey()}`;
      pipeline.incrby(key, op.quantity);
      pipeline.expire(key, 86400);
    }
    
    await pipeline.exec();
  }
  
  async getBatchUsage(
    userIds: string[],
    metric: string,
    period: 'hourly' | 'daily' | 'monthly' = 'daily'
  ): Promise<Record<string, number>> {
    const keys = userIds.map(userId => `usage:${userId}:${metric}:${this.getPeriodKey(period)}`);
    const values = await this.redis.mget(keys);
    
    const result: Record<string, number> = {};
    userIds.forEach((userId, index) => {
      result[userId] = values[index] ? parseInt(values[index]!, 10) : 0;
    });
    
    return result;
  }
  
  async cacheQuota(userId: string, metric: string, limit: number): Promise<void> {
    const key = `quota:${userId}:${metric}`;
    await this.redis.setex(key, 3600, limit);
  }
  
  async getCachedQuota(userId: string, metric: string): Promise<number | null> {
    const key = `quota:${userId}:${metric}`;
    const value = await this.redis.get(key);
    return value ? parseInt(value, 10) : null;
  }
  
  private getPeriodKey(period: 'hourly' | 'daily' | 'monthly' = 'daily'): string {
    const now = new Date();
    if (period === 'hourly') {
      return `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}-${now.getHours()}`;
    } else if (period === 'daily') {
      return `${now.getFullYear()}-${now.getMonth() + 1}-${now.getDate()}`;
    } else {
      return `${now.getFullYear()}-${now.getMonth() + 1}`;
    }
  }
}
```

---

## Data Retention

### Retention Policy

```typescript
// data-retention.ts
import { Pool } from 'pg';

export class DataRetentionService {
  constructor(private pool: Pool) {}
  
  async retainRealtimeData(days: number = 7): Promise<void> {
    await this.pool.query(
      `DELETE FROM usage_metrics 
       WHERE time < NOW() - INTERVAL '${days} days'`
    );
  }
  
  async aggregateToHourly(days: number = 30): Promise<void> {
    await this.pool.query(
      `INSERT INTO usage_metrics_hourly (bucket, user_id, metric, total_quantity, count)
       SELECT
         time_bucket('1 hour', time) as bucket,
         user_id,
         metric,
         SUM(quantity) as total_quantity,
         COUNT(*) as count
       FROM usage_metrics
       WHERE time >= NOW() - INTERVAL '${days} days'
       GROUP BY bucket, user_id, metric
       ON CONFLICT (bucket, user_id, metric) DO UPDATE
       SET total_quantity = EXCLUDED.total_quantity + usage_metrics_hourly.total_quantity,
           count = EXCLUDED.count + usage_metrics_hourly.count`
    );
  }
  
  async aggregateToDaily(months: number = 12): Promise<void> {
    await this.pool.query(
      `INSERT INTO usage_metrics_daily (bucket, user_id, metric, total_quantity, count)
       SELECT
         time_bucket('1 day', time) as bucket,
         user_id,
         metric,
         SUM(quantity) as total_quantity,
         COUNT(*) as count
       FROM usage_metrics_hourly
       WHERE bucket >= NOW() - INTERVAL '${months} months'
       GROUP BY bucket, user_id, metric
       ON CONFLICT (bucket, user_id, metric) DO UPDATE
       SET total_quantity = EXCLUDED.total_quantity + usage_metrics_daily.total_quantity,
           count = EXCLUDED.count + usage_metrics_daily.count`
    );
  }
  
  async deleteOldHourlyData(months: number = 3): Promise<void> {
    await this.pool.query(
      `DELETE FROM usage_metrics_hourly 
       WHERE bucket < NOW() - INTERVAL '${months} months'`
    );
  }
  
  async deleteOldDailyData(years: number = 2): Promise<void> {
    await this.pool.query(
      `DELETE FROM usage_metrics_daily 
       WHERE bucket < NOW() - INTERVAL '${years} years'`
    );
  }
}
```

---

## Production Patterns

```markdown
## Usage Metering Production Patterns

### Architecture
- [ ] Use Redis for real-time counters
- [ ] Use TimescaleDB for historical data
- [ ] Implement async event processing
- [ ] Use message queues for batching
- [ ] Separate tracking from enforcement

### Performance
- [ ] Batch Redis operations
- [ ] Use pipeline for multiple operations
- [ ] Cache quota limits
- [ ] Implement connection pooling
- [ ] Monitor Redis memory usage

### Reliability
- [ ] Implement retry logic
- [ ] Handle Redis failures gracefully
- [ ] Use circuit breakers
- [ ] Implement fallback storage
- [ ] Monitor system health

### Monitoring
- [ ] Track usage metrics
- [ ] Monitor quota violations
- [ ] Alert on anomalies
- [ ] Track performance metrics
- [ ] Monitor system resources

### Security
- [ ] Validate user IDs
- [ ] Sanitize metric names
- [ ] Implement rate limiting
- [ ] Use secure connections
- [ ] Audit log access

### Testing
- [ ] Unit test tracking logic
- [ ] Integration test quota enforcement
- [ ] Load test system performance
- [ ] Test failure scenarios
- [ ] Validate data accuracy

### Documentation
- [ ] Document API endpoints
- [ ] Document quota limits
- [ ] Document metrics tracked
- [ ] Document alert thresholds
- [ ] Document retention policies
```

---

## Additional Resources

- [Stripe Usage-Based Billing](https://stripe.com/docs/billing/subscriptions/usage-based)
- [Redis Best Practices](https://redis.io/topics/best-practices)
- [TimescaleDB Documentation](https://docs.timescale.com/)
- [Rate Limiting Patterns](https://cloud.google.com/architecture/rate-limiting-strategies-techniques)
