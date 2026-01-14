# Queue Monitoring

## Overview

Comprehensive guide to monitoring message queues including RabbitMQ, Redis, and Kafka for production systems.

## Table of Contents

1. [Key Metrics](#key-metrics)
2. [RabbitMQ Monitoring](#rabbitmq-monitoring)
3. [Redis Queue Monitoring](#redis-queue-monitoring)
4. [Health Checks](#health-checks)
5. [Alerting Strategies](#alerting-strategies)
6. [Grafana Dashboards](#grafana-dashboards)
7. [Dead Letter Queue Monitoring](#dead-letter-queue-monitoring)
8. [Performance Troubleshooting](#performance-troubleshooting)
9. [Capacity Planning](#capacity-planning)
10. [Best Practices](#best-practices)

---

## Key Metrics

### Core Metrics

```yaml
# Key Queue Metrics
queue_depth:
  description: Number of messages waiting in queue
  unit: count
  alert_threshold: > 1000

message_rate:
  description: Messages per second
  unit: messages/sec
  alert_threshold: < 1 or > 10000

processing_time:
  description: Time to process a message
  unit: milliseconds
  alert_threshold: > 5000

error_rate:
  description: Failed messages per second
  unit: errors/sec
  alert_threshold: > 10

consumer_lag:
  description: Messages behind producer
  unit: count
  alert_threshold: > 10000

queue_size_bytes:
  description: Total queue size in bytes
  unit: bytes
  alert_threshold: > 1GB
```

### Metrics Collection

```typescript
// metrics-collector.ts
import promClient from 'prom-client';

// Create metrics registry
const register = new promClient.Registry();

// Queue depth gauge
export const queueDepthGauge = new promClient.Gauge({
  name: 'queue_depth',
  help: 'Number of messages in queue',
  labelNames: ['queue_name', 'queue_type'],
  registers: [register],
});

// Message rate gauge
export const messageRateGauge = new promClient.Gauge({
  name: 'message_rate',
  help: 'Messages per second',
  labelNames: ['queue_name', 'direction'],  // direction: in/out
  registers: [register],
});

// Processing time histogram
export const processingTimeHistogram = new promClient.Histogram({
  name: 'processing_time_ms',
  help: 'Time to process messages',
  labelNames: ['queue_name'],
  buckets: [10, 50, 100, 500, 1000, 5000, 10000],
  registers: [register],
});

// Error rate gauge
export const errorRateGauge = new promClient.Gauge({
  name: 'error_rate',
  help: 'Error messages per second',
  labelNames: ['queue_name', 'error_type'],
  registers: [register],
});

// Consumer lag gauge
export const consumerLagGauge = new promClient.Gauge({
  name: 'consumer_lag',
  help: 'Messages behind producer',
  labelNames: ['queue_name', 'consumer_group'],
  registers: [register],
});

// Export metrics endpoint
export const getMetrics = () => register.metrics();
```

---

## RabbitMQ Monitoring

### Management Plugin

```typescript
// rabbitmq-monitor.ts
import axios from 'axios';

export class RabbitMQMonitor {
  private baseUrl: string;
  private auth: { username: string; password: string };

  constructor(
    host: string = 'localhost',
    port: number = 15672,
    username: string = 'guest',
    password: string = 'guest'
  ) {
    this.baseUrl = `http://${host}:${port}/api`;
    this.auth = { username, password };
  }

  async getQueues(): Promise<any[]> {
    const response = await axios.get(`${this.baseUrl}/queues`, {
      auth: this.auth,
    });
    return response.data;
  }

  async getQueueMetrics(queueName: string, vhost: string = '/'): Promise<any> {
    const response = await axios.get(
      `${this.baseUrl}/queues/${encodeURIComponent(vhost)}/${encodeURIComponent(queueName)}`,
      { auth: this.auth }
    );
    return response.data;
  }

  async getOverview(): Promise<any> {
    const response = await axios.get(`${this.baseUrl}/overview`, {
      auth: this.auth,
    });
    return response.data;
  }

  async getConnections(): Promise<any[]> {
    const response = await axios.get(`${this.baseUrl}/connections`, {
      auth: this.auth,
    });
    return response.data;
  }

  async getChannels(): Promise<any[]> {
    const response = await axios.get(`${this.baseUrl}/channels`, {
      auth: this.auth,
    });
    return response.data;
  }

  async getConsumers(): Promise<any[]> {
    const response = await axios.get(`${this.baseUrl}/consumers`, {
      auth: this.auth,
    });
    return response.data;
  }

  async getNodeStats(): Promise<any> {
    const response = await axios.get(`${this.baseUrl}/nodes`, {
      auth: this.auth,
    });
    return response.data;
  }
}

// Usage
const monitor = new RabbitMQMonitor('localhost', 15672, 'admin', 'password');
const queues = await monitor.getQueues();
const overview = await monitor.getOverview();
```

### Prometheus Exporter

```yaml
# prometheus-rabbitmq-exporter.yml
version: '3.8'

services:
  rabbitmq:
    image: rabbitmq:3-management
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin123

  prometheus-rabbitmq-exporter:
    image: kbudde/rabbitmq-exporter
    ports:
      - "9090:9090"
    environment:
      RABBIT_URL: http://admin:admin123@rabbitmq:15672
      PUBLISH_PORT: 9090
      OUTPUT_FORMAT: JSON
      LOG_LEVEL: info
      RABBIT_CAPABILITIES: bert,no_sort
```

### RabbitMQ Metrics Dashboard

```json
{
  "dashboard": {
    "title": "RabbitMQ Monitoring",
    "panels": [
      {
        "title": "Queue Depth",
        "targets": [
          {
            "expr": "rabbitmq_queue_messages{queue=~\".*\"}",
            "legendFormat": "{{queue}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Message Rate",
        "targets": [
          {
            "expr": "rate(rabbitmq_queue_messages_published_total[5m])",
            "legendFormat": "{{queue}} (publish)"
          },
          {
            "expr": "rate(rabbitmq_queue_messages_delivered_total[5m])",
            "legendFormat": "{{queue}} (deliver)"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Consumer Lag",
        "targets": [
          {
            "expr": "rabbitmq_queue_messages_unacknowledged",
            "legendFormat": "{{queue}}"
          }
        ],
        "type": "graph"
      },
      {
        "title": "Error Rate",
        "targets": [
          {
            "expr": "rate(rabbitmq_channel_messages_unroutable_total[5m])",
            "legendFormat": "unroutable"
          }
        ],
        "type": "graph"
      }
    ]
  }
}
```

---

## Redis Queue Monitoring

### Redis Metrics

```typescript
// redis-monitor.ts
import { createClient } from 'redis';
import { queueDepthGauge, messageRateGauge } from './metrics-collector';

export class RedisQueueMonitor {
  private client: ReturnType<typeof createClient>;

  constructor(redisUrl: string = 'redis://localhost:6379') {
    this.client = createClient({ url: redisUrl });
  }

  async connect(): Promise<void> {
    await this.client.connect();
  }

  async getQueueInfo(queueName: string): Promise<any> {
    const length = await this.client.lLen(queueName);
    const memory = await this.client.memoryUsage(queueName);
    
    return {
      name: queueName,
      length,
      memoryBytes: memory,
    };
  }

  async getAllQueues(pattern: string = 'bull:*'): Promise<any[]> {
    const keys = await this.client.keys(pattern);
    const queues = [];
    
    for (const key of keys) {
      const info = await this.getQueueInfo(key);
      queues.push(info);
    }
    
    return queues;
  }

  async getBullQueueMetrics(queueName: string): Promise<any> {
    const waiting = await this.client.lLen(`${queueName}:waiting`);
    const active = await this.client.lLen(`${queueName}:active`);
    const completed = await this.client.lLen(`${queueName}:completed`);
    const failed = await this.client.lLen(`${queueName}:failed`);
    const delayed = await this.client.zCard(`${queueName}:delayed`);
    
    return {
      queueName,
      waiting,
      active,
      completed,
      failed,
      delayed,
    };
  }

  async collectMetrics(queueNames: string[]): Promise<void> {
    for (const queueName of queueNames) {
      const metrics = await this.getBullQueueMetrics(queueName);
      
      queueDepthGauge.set(
        { queue_name: queueName, queue_type: 'waiting' },
        metrics.waiting
      );
      queueDepthGauge.set(
        { queue_name: queueName, queue_type: 'active' },
        metrics.active
      );
      queueDepthGauge.set(
        { queue_name: queueName, queue_type: 'failed' },
        metrics.failed
      );
    }
  }

  async close(): Promise<void> {
    await this.client.quit();
  }
}

// Usage
const monitor = new RedisQueueMonitor('redis://localhost:6379');
await monitor.connect();
const metrics = await monitor.getBullQueueMetrics('emails');
await monitor.collectMetrics(['emails', 'notifications']);
```

### Redis Exporter

```yaml
# prometheus-redis-exporter.yml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  redis-exporter:
    image: oliver006/redis_exporter
    ports:
      - "9121:9121"
    environment:
      REDIS_ADDR: redis://redis:6379
      REDIS_EXPORTER_LOG_FORMAT: txt
```

---

## Health Checks

### Queue Health Check

```typescript
// health-check.ts
import { RabbitMQMonitor } from './rabbitmq-monitor';
import { RedisQueueMonitor } from './redis-monitor';

export interface HealthCheckResult {
  healthy: boolean;
  checks: Record<string, boolean>;
  metrics: any;
}

export class QueueHealthChecker {
  private rabbitMQMonitor?: RabbitMQMonitor;
  private redisMonitor?: RedisQueueMonitor;

  constructor(config: {
    rabbitmq?: { host: string; port: number };
    redis?: { url: string };
  }) {
    if (config.rabbitmq) {
      this.rabbitMQMonitor = new RabbitMQMonitor(
        config.rabbitmq.host,
        config.rabbitmq.port
      );
    }
    if (config.redis) {
      this.redisMonitor = new RedisQueueMonitor(config.redis.url);
    }
  }

  async checkHealth(): Promise<HealthCheckResult> {
    const checks: Record<string, boolean> = {};
    const metrics: any = {};

    // Check RabbitMQ
    if (this.rabbitMQMonitor) {
      try {
        const overview = await this.rabbitMQMonitor.getOverview();
        checks['rabbitmq'] = true;
        metrics.rabbitmq = overview;
      } catch (error) {
        checks['rabbitmq'] = false;
        metrics.rabbitmq = { error: (error as Error).message };
      }
    }

    // Check Redis
    if (this.redisMonitor) {
      try {
        await this.redisMonitor.connect();
        const queues = await this.redisMonitor.getAllQueues();
        checks['redis'] = true;
        metrics.redis = { queueCount: queues.length };
        await this.redisMonitor.close();
      } catch (error) {
        checks['redis'] = false;
        metrics.redis = { error: (error as Error).message };
      }
    }

    const healthy = Object.values(checks).every((v) => v === true);

    return { healthy, checks, metrics };
  }
}

// Usage in Express
import express from 'express';

const app = express();
const healthChecker = new QueueHealthChecker({
  rabbitmq: { host: 'localhost', port: 15672 },
  redis: { url: 'redis://localhost:6379' },
});

app.get('/health', async (req, res) => {
  const health = await healthChecker.checkHealth();
  res.status(health.healthy ? 200 : 503).json(health);
});
```

---

## Alerting Strategies

### Prometheus Alert Rules

```yaml
# alert-rules.yml
groups:
  - name: queue_alerts
    interval: 30s
    rules:
      # High queue depth
      - alert: HighQueueDepth
        expr: rabbitmq_queue_messages > 1000
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High queue depth detected"
          description: "Queue {{ $labels.queue }} has {{ $value }} messages"

      # Queue growing rapidly
      - alert: QueueGrowingRapidly
        expr: rate(rabbitmq_queue_messages[5m]) > 100
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "Queue growing rapidly"
          description: "Queue {{ $labels.queue }} growing at {{ $value }} msgs/sec"

      # High error rate
      - alert: HighErrorRate
        expr: rate(rabbitmq_channel_messages_unroutable_total[5m]) > 10
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors/sec"

      # Consumer lag
      - alert: HighConsumerLag
        expr: rabbitmq_queue_messages_unacknowledged > 5000
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High consumer lag"
          description: "Consumer lag is {{ $value }} messages"

      # No consumers
      - alert: NoConsumers
        expr: rabbitmq_queue_consumers == 0
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "No consumers detected"
          description: "Queue {{ $labels.queue }} has no consumers"

      # Redis memory usage
      - alert: HighRedisMemory
        expr: redis_memory_used_bytes / redis_memory_max_bytes > 0.9
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Redis memory usage high"
          description: "Redis using {{ $value | humanizePercentage }} of memory"
```

### Custom Alerting

```typescript
// alert-manager.ts
import axios from 'axios';

export interface AlertConfig {
  webhookUrl: string;
  channels: string[];
  severity: 'info' | 'warning' | 'critical';
}

export class AlertManager {
  private alertHistory: Map<string, number> = new Map();
  private cooldownMs: number = 300000; // 5 minutes

  constructor(private config: AlertConfig) {}

  async sendAlert(
    alertName: string,
    message: string,
    severity: string = this.config.severity
  ): Promise<void> {
    // Check cooldown
    const lastAlert = this.alertHistory.get(alertName);
    if (lastAlert && Date.now() - lastAlert < this.cooldownMs) {
      return; // Skip due to cooldown
    }

    const payload = {
      text: `[${severity.toUpperCase()}] ${alertName}`,
      attachments: [
        {
          color: this.getColorForSeverity(severity),
          text: message,
          ts: Math.floor(Date.now() / 1000),
        },
      ],
    };

    try {
      await axios.post(this.config.webhookUrl, payload);
      this.alertHistory.set(alertName, Date.now());
    } catch (error) {
      console.error('Failed to send alert:', error);
    }
  }

  private getColorForSeverity(severity: string): string {
    const colors: Record<string, string> = {
      info: '#36a64f',
      warning: '#ff9900',
      critical: '#ff0000',
    };
    return colors[severity] || '#36a64f';
  }

  async sendQueueAlert(
    queueName: string,
    metric: string,
    value: number,
    threshold: number
  ): Promise<void> {
    const message = `Queue ${queueName} ${metric} is ${value}, threshold is ${threshold}`;
    await this.sendAlert(
      `QueueAlert_${queueName}_${metric}`,
      message,
      value > threshold * 2 ? 'critical' : 'warning'
    );
  }
}

// Usage
const alertManager = new AlertManager({
  webhookUrl: process.env.SLACK_WEBHOOK_URL!,
  channels: ['#alerts'],
  severity: 'warning',
});

await alertManager.sendQueueAlert('emails', 'depth', 1500, 1000);
```

---

## Grafana Dashboards

### Queue Monitoring Dashboard

```json
{
  "dashboard": {
    "title": "Queue Monitoring Dashboard",
    "panels": [
      {
        "title": "Queue Depth",
        "type": "graph",
        "targets": [
          {
            "expr": "rabbitmq_queue_messages",
            "legendFormat": "{{queue}}"
          }
        ]
      },
      {
        "title": "Message Rate (Publish)",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(rabbitmq_queue_messages_published_total[5m])",
            "legendFormat": "{{queue}}"
          }
        ]
      },
      {
        "title": "Message Rate (Deliver)",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(rabbitmq_queue_messages_delivered_total[5m])",
            "legendFormat": "{{queue}}"
          }
        ]
      },
      {
        "title": "Consumer Lag",
        "type": "graph",
        "targets": [
          {
            "expr": "rabbitmq_queue_messages_unacknowledged",
            "legendFormat": "{{queue}}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(rabbitmq_channel_messages_unroutable_total[5m])",
            "legendFormat": "unroutable"
          }
        ]
      },
      {
        "title": "Queue Memory",
        "type": "graph",
        "targets": [
          {
            "expr": "rabbitmq_queue_memory_bytes",
            "legendFormat": "{{queue}}"
          }
        ]
      }
    ]
  }
}
```

---

## Dead Letter Queue Monitoring

### DLQ Monitoring

```typescript
// dlq-monitor.ts
import { RabbitMQMonitor } from './rabbitmq-monitor';
import { AlertManager } from './alert-manager';

export class DLQMonitor {
  constructor(
    private rabbitMQMonitor: RabbitMQMonitor,
    private alertManager: AlertManager
  ) {}

  async monitorDLQ(dlqName: string, threshold: number = 100): Promise<void> {
    const metrics = await this.rabbitMQMonitor.getQueueMetrics(dlqName);
    
    if (metrics.messages > threshold) {
      await this.alertManager.sendAlert(
        `DLQAlert_${dlqName}`,
        `Dead letter queue ${dlqName} has ${metrics.messages} messages`,
        metrics.messages > threshold * 5 ? 'critical' : 'warning'
      );
    }
  }

  async getDLQMessages(dlqName: string, limit: number = 10): Promise<any[]> {
    const messages = await this.rabbitMQMonitor.getMessages(dlqName, limit);
    return messages;
  }

  async analyzeDLQ(dlqName: string): Promise<any> {
    const messages = await this.getDLQMessages(dlqName, 100);
    
    const analysis = {
      total: messages.length,
      byReason: {} as Record<string, number>,
      byQueue: {} as Record<string, number>,
    };
    
    for (const message of messages) {
      const reason = message.payload?.properties?.headers?.['x-death']?.[0]?.reason || 'unknown';
      const originalQueue = message.payload?.properties?.headers?.['x-death']?.[0]?.queue || 'unknown';
      
      analysis.byReason[reason] = (analysis.byReason[reason] || 0) + 1;
      analysis.byQueue[originalQueue] = (analysis.byQueue[originalQueue] || 0) + 1;
    }
    
    return analysis;
  }
}
```

---

## Performance Troubleshooting

### Common Issues

```typescript
// troubleshooting.ts
export class QueueTroubleshooter {
  static async diagnoseSlowConsumers(queueName: string): Promise<string[]> {
    const issues: string[] = [];
    
    // Check consumer count
    const consumers = await this.getConsumerCount(queueName);
    if (consumers === 0) {
      issues.push('No consumers attached to queue');
    }
    
    // Check prefetch settings
    const prefetch = await this.getPrefetchCount(queueName);
    if (prefetch > 100) {
      issues.push(`High prefetch count (${prefetch}) may cause memory issues`);
    }
    
    // Check processing time
    const avgProcessingTime = await this.getAvgProcessingTime(queueName);
    if (avgProcessingTime > 5000) {
      issues.push(`High average processing time (${avgProcessingTime}ms)`);
    }
    
    return issues;
  }

  static async diagnoseBacklog(queueName: string): Promise<string[]> {
    const issues: string[] = [];
    
    // Check queue depth
    const depth = await this.getQueueDepth(queueName);
    if (depth > 10000) {
      issues.push(`Large queue backlog (${depth} messages)`);
    }
    
    // Check message rate
    const publishRate = await this.getPublishRate(queueName);
    const consumeRate = await this.getConsumeRate(queueName);
    
    if (publishRate > consumeRate * 1.5) {
      issues.push('Publish rate significantly higher than consume rate');
    }
    
    return issues;
  }

  static async diagnoseMemoryIssues(queueName: string): Promise<string[]> {
    const issues: string[] = [];
    
    // Check queue memory
    const memory = await this.getQueueMemory(queueName);
    if (memory > 1073741824) { // 1GB
      issues.push(`High queue memory usage (${memory / 1024 / 1024}MB)`);
    }
    
    // Check message size
    const avgMessageSize = await this.getAvgMessageSize(queueName);
    if (avgMessageSize > 1048576) { // 1MB
      issues.push(`Large average message size (${avgMessageSize / 1024}KB)`);
    }
    
    return issues;
  }

  private static async getConsumerCount(queueName: string): Promise<number> {
    // Implementation
    return 0;
  }

  private static async getPrefetchCount(queueName: string): Promise<number> {
    // Implementation
    return 0;
  }

  private static async getAvgProcessingTime(queueName: string): Promise<number> {
    // Implementation
    return 0;
  }

  private static async getQueueDepth(queueName: string): Promise<number> {
    // Implementation
    return 0;
  }

  private static async getPublishRate(queueName: string): Promise<number> {
    // Implementation
    return 0;
  }

  private static async getConsumeRate(queueName: string): Promise<number> {
    // Implementation
    return 0;
  }

  private static async getQueueMemory(queueName: string): Promise<number> {
    // Implementation
    return 0;
  }

  private static async getAvgMessageSize(queueName: string): Promise<number> {
    // Implementation
    return 0;
  }
}
```

---

## Capacity Planning

### Capacity Calculator

```typescript
// capacity-planning.ts
export interface QueueCapacity {
  queueName: string;
  currentDepth: number;
  peakDepth: number;
  avgMessageSize: number;
  avgProcessingTime: number;
  consumers: number;
}

export class CapacityPlanner {
  static calculateRequiredConsumers(capacity: QueueCapacity): number {
    const messagesPerSecond = capacity.peakDepth / 86400; // Peak over 24 hours
    const processingPerConsumer = 1000 / capacity.avgProcessingTime;
    
    const required = Math.ceil(messagesPerSecond / processingPerConsumer);
    
    // Add 20% buffer
    return Math.ceil(required * 1.2);
  }

  static estimateQueueMemory(capacity: QueueCapacity): number {
    return capacity.peakDepth * capacity.avgMessageSize;
  }

  static calculateThroughput(capacity: QueueCapacity): number {
    return capacity.consumers * (1000 / capacity.avgProcessingTime);
  }

  static recommendConfiguration(capacity: QueueCapacity): any {
    const requiredConsumers = this.calculateRequiredConsumers(capacity);
    const estimatedMemory = this.estimateQueueMemory(capacity);
    const throughput = this.calculateThroughput(capacity);
    
    return {
      recommendedConsumers: requiredConsumers,
      estimatedMemoryBytes: estimatedMemory,
      estimatedMemoryMB: estimatedMemory / 1024 / 1024,
      estimatedThroughput: throughput,
      currentConsumers: capacity.consumers,
      needsScaling: requiredConsumers > capacity.consumers,
    };
  }
}

// Usage
const capacity: QueueCapacity = {
  queueName: 'emails',
  currentDepth: 5000,
  peakDepth: 20000,
  avgMessageSize: 1024,
  avgProcessingTime: 100,
  consumers: 5,
};

const recommendation = CapacityPlanner.recommendConfiguration(capacity);
console.log(recommendation);
```

---

## Best Practices

### Monitoring Checklist

```markdown
## Queue Monitoring Checklist

### Basic Metrics
- [ ] Queue depth (waiting messages)
- [ ] Message rate (publish/deliver)
- [ ] Processing time
- [ ] Error rate
- [ ] Consumer lag

### Advanced Metrics
- [ ] Queue memory usage
- [ ] Consumer count
- [ ] Prefetch settings
- [ ] Connection count
- [ ] Channel count

### Alerts
- [ ] High queue depth
- [ ] Growing queue
- [ ] High error rate
- [ ] No consumers
- [ ] DLQ messages

### Dashboards
- [ ] Real-time queue metrics
- [ ] Historical trends
- [ ] Consumer performance
- [ ] Error analysis
- [ ] Capacity planning
```

---

## Additional Resources

- [RabbitMQ Management Plugin](https://www.rabbitmq.com/management.html)
- [Prometheus RabbitMQ Exporter](https://github.com/kbudde/rabbitmq_exporter)
- [Prometheus Redis Exporter](https://github.com/oliver006/redis_exporter)
- [Grafana Dashboards](https://grafana.com/grafana/dashboards/)
- [BullMQ Monitoring](https://docs.bullmq.io/guide/monitoring)
