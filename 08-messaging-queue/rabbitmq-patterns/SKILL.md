# RabbitMQ Patterns

## Overview

Comprehensive guide to RabbitMQ messaging patterns and best practices for distributed systems.

## Table of Contents

1. [RabbitMQ Concepts](#rabbitmq-concepts)
2. [Exchange Types](#exchange-types)
3. [Message Patterns](#message-patterns)
4. [Producer Patterns](#producer-patterns)
5. [Consumer Patterns](#consumer-patterns)
6. [Dead Letter Queues](#dead-letter-queues)
7. [Message Acknowledgment](#message-acknowledgment)
8. [Persistence](#persistence)
9. [Error Handling](#error-handling)
10. [Performance Optimization](#performance-optimization)
11. [Monitoring](#monitoring)
12. [Production Setup](#production-setup)

---

## RabbitMQ Concepts

### Core Components

```python
# RabbitMQ Core Concepts
"""
- Producer: Application that sends messages
- Consumer: Application that receives messages
- Queue: Buffer that stores messages
- Exchange: Receives messages from producers and routes them to queues
- Binding: Link between exchange and queue
- Routing Key: Key used by exchange to route messages
- Connection: TCP connection between application and RabbitMQ
- Channel: Virtual connection within a TCP connection
"""
```

### Basic Connection (Node.js)

```typescript
// rabbitmq-connection.ts
import amqp from 'amqplib';

export class RabbitMQConnection {
  private connection: amqp.Connection | null = null;
  private channel: amqp.Channel | null = null;

  async connect(url: string = 'amqp://localhost'): Promise<void> {
    try {
      this.connection = await amqp.connect(url);
      this.channel = await this.connection.createChannel();
      console.log('Connected to RabbitMQ');
    } catch (error) {
      console.error('Failed to connect to RabbitMQ:', error);
      throw error;
    }
  }

  getChannel(): amqp.Channel {
    if (!this.channel) {
      throw new Error('Channel not initialized');
    }
    return this.channel;
  }

  async close(): Promise<void> {
    if (this.channel) {
      await this.channel.close();
    }
    if (this.connection) {
      await this.connection.close();
    }
  }
}

// Usage
const connection = new RabbitMQConnection();
await connection.connect('amqp://user:password@localhost:5672');
const channel = connection.getChannel();
```

### Basic Connection (Python)

```python
# rabbitmq_connection.py
import pika
import logging

class RabbitMQConnection:
    def __init__(self, url: str = 'amqp://localhost'):
        self.url = url
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Establish connection to RabbitMQ"""
        try:
            parameters = pika.URLParameters(self.url)
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            logging.info("Connected to RabbitMQ")
            return self.channel
        except Exception as e:
            logging.error(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    def close(self):
        """Close connection"""
        if self.channel:
            self.channel.close()
        if self.connection:
            self.connection.close()
        logging.info("RabbitMQ connection closed")

# Usage
connection = RabbitMQConnection('amqp://user:password@localhost:5672')
channel = connection.connect()
```

---

## Exchange Types

### Direct Exchange

```typescript
// direct-exchange.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class DirectExchange {
  constructor(private connection: RabbitMQConnection) {}

  async setup(exchangeName: string, queueNames: string[], routingKeys: string[]) {
    const channel = this.connection.getChannel();

    // Declare direct exchange
    await channel.assertExchange(exchangeName, 'direct', { durable: true });

    // Declare and bind queues
    for (let i = 0; i < queueNames.length; i++) {
      await channel.assertQueue(queueNames[i], { durable: true });
      await channel.bindQueue(queueNames[i], exchangeName, routingKeys[i]);
    }
  }

  async publish(exchangeName: string, routingKey: string, message: any) {
    const channel = this.connection.getChannel();
    channel.publish(
      exchangeName,
      routingKey,
      Buffer.from(JSON.stringify(message)),
      { persistent: true }
    );
  }
}

// Usage
const direct = new DirectExchange(connection);
await direct.setup('orders', ['order-processing', 'order-shipping'], ['process', 'ship']);
await direct.publish('orders', 'process', { orderId: 123 });
```

### Topic Exchange

```typescript
// topic-exchange.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class TopicExchange {
  constructor(private connection: RabbitMQConnection) {}

  async setup(exchangeName: string, bindings: Array<{ queue: string; pattern: string }>) {
    const channel = this.connection.getChannel();

    // Declare topic exchange
    await channel.assertExchange(exchangeName, 'topic', { durable: true });

    // Declare and bind queues with patterns
    for (const binding of bindings) {
      await channel.assertQueue(binding.queue, { durable: true });
      await channel.bindQueue(binding.queue, exchangeName, binding.pattern);
    }
  }

  async publish(exchangeName: string, routingKey: string, message: any) {
    const channel = this.connection.getChannel();
    channel.publish(
      exchangeName,
      routingKey,
      Buffer.from(JSON.stringify(message)),
      { persistent: true }
    );
  }
}

// Usage
const topic = new TopicExchange(connection);
await topic.setup('logs', [
  { queue: 'error-logs', pattern: '*.error' },
  { queue: 'all-logs', pattern: '#' }
]);

// Publish with routing keys
await topic.publish('logs', 'app.error', { message: 'Error occurred' });
await topic.publish('logs', 'app.info', { message: 'Info message' });
```

### Fanout Exchange

```typescript
// fanout-exchange.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class FanoutExchange {
  constructor(private connection: RabbitMQConnection) {}

  async setup(exchangeName: string, queueNames: string[]) {
    const channel = this.connection.getChannel();

    // Declare fanout exchange
    await channel.assertExchange(exchangeName, 'fanout', { durable: true });

    // Declare and bind queues (no routing key needed)
    for (const queueName of queueNames) {
      await channel.assertQueue(queueName, { durable: true });
      await channel.bindQueue(queueName, exchangeName, '');
    }
  }

  async publish(exchangeName: string, message: any) {
    const channel = this.connection.getChannel();
    channel.publish(
      exchangeName,
      '',  // Fanout ignores routing key
      Buffer.from(JSON.stringify(message)),
      { persistent: true }
    );
  }
}

// Usage
const fanout = new FanoutExchange(connection);
await fanout.setup('notifications', ['email-queue', 'sms-queue', 'push-queue']);
await fanout.publish('notifications', { userId: 123, message: 'Hello!' });
```

### Headers Exchange

```typescript
// headers-exchange.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class HeadersExchange {
  constructor(private connection: RabbitMQConnection) {}

  async setup(exchangeName: string, bindings: Array<{ queue: string; headers: any }>) {
    const channel = this.connection.getChannel();

    // Declare headers exchange
    await channel.assertExchange(exchangeName, 'headers', { durable: true });

    // Declare and bind queues with headers
    for (const binding of bindings) {
      await channel.assertQueue(binding.queue, { durable: true });
      await channel.bindQueue(binding.queue, exchangeName, '', binding.headers);
    }
  }

  async publish(exchangeName: string, message: any, headers: any) {
    const channel = this.connection.getChannel();
    channel.publish(
      exchangeName,
      '',
      Buffer.from(JSON.stringify(message)),
      { persistent: true, headers }
    );
  }
}

// Usage
const headers = new HeadersExchange(connection);
await headers.setup('priority', [
  { queue: 'high-priority', headers: { 'x-match': 'all', priority: 'high' } },
  { queue: 'low-priority', headers: { 'x-match': 'all', priority: 'low' } }
]);

await headers.publish('priority', { data: 'test' }, { priority: 'high' });
```

---

## Message Patterns

### Work Queue (Competing Consumers)

```typescript
// work-queue.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class WorkQueue {
  constructor(private connection: RabbitMQConnection) {}

  async setup(queueName: string) {
    const channel = this.connection.getChannel();
    await channel.assertQueue(queueName, { durable: true });
    await channel.prefetch(1);  // Fair dispatch
  }

  async publish(queueName: string, task: any) {
    const channel = this.connection.getChannel();
    channel.sendToQueue(
      queueName,
      Buffer.from(JSON.stringify(task)),
      { persistent: true }
    );
  }

  async consume(queueName: string, handler: (task: any) => Promise<void>) {
    const channel = this.connection.getChannel();
    await channel.consume(
      queueName,
      async (msg) => {
        if (msg) {
          try {
            const task = JSON.parse(msg.content.toString());
            await handler(task);
            channel.ack(msg);
          } catch (error) {
            console.error('Error processing task:', error);
            channel.nack(msg, false, true);  // Requeue
          }
        }
      },
      { noAck: false }
    );
  }
}

// Usage
const workQueue = new WorkQueue(connection);
await workQueue.setup('tasks');

// Producer
await workQueue.publish('tasks', { id: 1, data: 'Process me' });

// Consumer
await workQueue.consume('tasks', async (task) => {
  console.log('Processing task:', task.id);
  await processTask(task);
});
```

### Publish/Subscribe

```typescript
// pub-sub.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class PubSub {
  constructor(private connection: RabbitMQConnection) {}

  async setup(exchangeName: string, queueNames: string[]) {
    const channel = this.connection.getChannel();
    await channel.assertExchange(exchangeName, 'fanout', { durable: true });

    for (const queueName of queueNames) {
      await channel.assertQueue(queueName, { durable: false });  // Non-durable for temp queues
      await channel.bindQueue(queueName, exchangeName, '');
    }
  }

  async publish(exchangeName: string, message: any) {
    const channel = this.connection.getChannel();
    channel.publish(exchangeName, '', Buffer.from(JSON.stringify(message)));
  }

  async subscribe(queueName: string, handler: (message: any) => Promise<void>) {
    const channel = this.connection.getChannel();
    await channel.consume(queueName, async (msg) => {
      if (msg) {
        const message = JSON.parse(msg.content.toString());
        await handler(message);
        channel.ack(msg);
      }
    });
  }
}

// Usage
const pubsub = new PubSub(connection);
await pubsub.setup('news', ['sports-queue', 'tech-queue', 'weather-queue']);

// Publisher
await pubsub.publish('news', { category: 'tech', title: 'New AI breakthrough' });

// Subscribers
await pubsub.subscribe('tech-queue', async (msg) => {
  console.log('Tech news:', msg.title);
});
```

### Routing Pattern

```typescript
// routing-pattern.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class RoutingPattern {
  constructor(private connection: RabbitMQConnection) {}

  async setup(exchangeName: string, bindings: Array<{ queue: string; routingKey: string }>) {
    const channel = this.connection.getChannel();
    await channel.assertExchange(exchangeName, 'direct', { durable: true });

    for (const binding of bindings) {
      await channel.assertQueue(binding.queue, { durable: true });
      await channel.bindQueue(binding.queue, exchangeName, binding.routingKey);
    }
  }

  async publish(exchangeName: string, routingKey: string, message: any) {
    const channel = this.connection.getChannel();
    channel.publish(
      exchangeName,
      routingKey,
      Buffer.from(JSON.stringify(message))
    );
  }

  async consume(queueName: string, handler: (message: any) => Promise<void>) {
    const channel = this.connection.getChannel();
    await channel.consume(queueName, async (msg) => {
      if (msg) {
        const message = JSON.parse(msg.content.toString());
        await handler(message);
        channel.ack(msg);
      }
    });
  }
}

// Usage
const routing = new RoutingPattern(connection);
await routing.setup('logs', [
  { queue: 'error-queue', routingKey: 'error' },
  { queue: 'info-queue', routingKey: 'info' },
  { queue: 'warning-queue', routingKey: 'warning' }
]);

// Publisher
await routing.publish('logs', 'error', { message: 'Critical error' });
await routing.publish('logs', 'info', { message: 'Info message' });
```

### RPC (Remote Procedure Call)

```typescript
// rpc-pattern.ts
import { RabbitMQConnection } from './rabbitmq-connection';
import { v4 as uuidv4 } from 'uuid';

export class RPCServer {
  constructor(private connection: RabbitMQConnection) {}

  async setup(queueName: string, handler: (request: any) => Promise<any>) {
    const channel = this.connection.getChannel();
    await channel.assertQueue(queueName, { durable: false });
    await channel.prefetch(1);

    await channel.consume(queueName, async (msg) => {
      if (msg) {
        const request = JSON.parse(msg.content.toString());
        const correlationId = msg.properties.correlationId;
        const replyTo = msg.properties.replyTo;

        try {
          const response = await handler(request);
          channel.sendToQueue(
            replyTo,
            Buffer.from(JSON.stringify(response)),
            { correlationId }
          );
          channel.ack(msg);
        } catch (error) {
          channel.nack(msg, false, false);
        }
      }
    });
  }
}

export class RPCClient {
  private correlationMap = new Map<string, { resolve: any; reject: any }>();
  private replyQueue: string;

  constructor(private connection: RabbitMQConnection) {}

  async initialize() {
    const channel = this.connection.getChannel();
    const replyQueue = await channel.assertQueue('', { exclusive: true });
    this.replyQueue = replyQueue.queue;

    await channel.consume(this.replyQueue, (msg) => {
      if (msg) {
        const correlationId = msg.properties.correlationId;
        const callback = this.correlationMap.get(correlationId);
        if (callback) {
          callback.resolve(JSON.parse(msg.content.toString()));
          this.correlationMap.delete(correlationId);
        }
        channel.ack(msg);
      }
    });
  }

  async call(queueName: string, request: any, timeout: number = 5000): Promise<any> {
    const channel = this.connection.getChannel();
    const correlationId = uuidv4();

    return new Promise((resolve, reject) => {
      this.correlationMap.set(correlationId, { resolve, reject });

      const timer = setTimeout(() => {
        this.correlationMap.delete(correlationId);
        reject(new Error('RPC timeout'));
      }, timeout);

      channel.sendToQueue(
        queueName,
        Buffer.from(JSON.stringify(request)),
        {
          correlationId,
          replyTo: this.replyQueue
        }
      );
    });
  }
}

// Usage
// Server
const server = new RPCServer(connection);
await server.setup('rpc_queue', async (request) => {
  return { result: `Processed: ${request.data}` };
});

// Client
const client = new RPCClient(connection);
await client.initialize();
const response = await client.call('rpc_queue', { data: 'test' });
console.log(response);
```

---

## Producer Patterns

### Reliable Publisher

```typescript
// reliable-publisher.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class ReliablePublisher {
  private confirmChannel: amqp.ConfirmChannel;

  constructor(private connection: RabbitMQConnection) {}

  async setup() {
    const channel = this.connection.getChannel();
    this.confirmChannel = channel as amqp.ConfirmChannel;
    await this.confirmChannel.confirmChannel();
  }

  async publishWithConfirm(
    exchangeName: string,
    routingKey: string,
    message: any
  ): Promise<boolean> {
    return new Promise((resolve, reject) => {
      this.confirmChannel.publish(
        exchangeName,
        routingKey,
        Buffer.from(JSON.stringify(message)),
        { persistent: true },
        (err) => {
          if (err) {
            reject(err);
          } else {
            resolve(true);
          }
        }
      );
    });
  }

  async publishWithRetry(
    exchangeName: string,
    routingKey: string,
    message: any,
    maxRetries: number = 3
  ): Promise<void> {
    let lastError: Error | null = null;

    for (let i = 0; i < maxRetries; i++) {
      try {
        await this.publishWithConfirm(exchangeName, routingKey, message);
        return;
      } catch (error) {
        lastError = error as Error;
        console.error(`Publish attempt ${i + 1} failed:`, error);
        await this.delay(1000 * (i + 1));  // Exponential backoff
      }
    }

    throw lastError;
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

### Transactional Publisher

```typescript
// transactional-publisher.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class TransactionalPublisher {
  constructor(private connection: RabbitMQConnection) {}

  async publishInTransaction(
    exchangeName: string,
    routingKey: string,
    messages: any[]
  ): Promise<void> {
    const channel = this.connection.getChannel();

    try {
      await channel.selectMode();  // Start transaction

      // Publish all messages
      for (const message of messages) {
        channel.publish(
          exchangeName,
          routingKey,
          Buffer.from(JSON.stringify(message))
        );
      }

      await channel.commitTx();  // Commit transaction
    } catch (error) {
      await channel.rollbackTx();  // Rollback on error
      throw error;
    }
  }
}
```

---

## Consumer Patterns

### Batch Consumer

```typescript
// batch-consumer.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class BatchConsumer {
  private batch: any[] = [];
  private timer: NodeJS.Timeout | null = null;

  constructor(
    private connection: RabbitMQConnection,
    private batchSize: number = 10,
    private batchTimeout: number = 5000
  ) {}

  async consume(queueName: string, handler: (batch: any[]) => Promise<void>) {
    const channel = this.connection.getChannel();
    await channel.prefetch(this.batchSize);

    await channel.consume(queueName, async (msg) => {
      if (msg) {
        this.batch.push(JSON.parse(msg.content.toString()));

        if (this.batch.length >= this.batchSize) {
          await this.processBatch(handler);
        } else if (!this.timer) {
          this.timer = setTimeout(() => this.processBatch(handler), this.batchTimeout);
        }
      }
    });
  }

  private async processBatch(handler: (batch: any[]) => Promise<void>) {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }

    if (this.batch.length === 0) return;

    const batch = [...this.batch];
    this.batch = [];

    try {
      await handler(batch);
    } catch (error) {
      console.error('Error processing batch:', error);
      // Handle batch failure
    }
  }
}
```

### Rate-Limited Consumer

```typescript
// rate-limited-consumer.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class RateLimitedConsumer {
  private lastProcessTime = 0;

  constructor(
    private connection: RabbitMQConnection,
    private rateLimit: number  // Messages per second
  ) {}

  async consume(queueName: string, handler: (message: any) => Promise<void>) {
    const channel = this.connection.getChannel();
    const interval = 1000 / this.rateLimit;

    await channel.consume(queueName, async (msg) => {
      if (msg) {
        const now = Date.now();
        const elapsed = now - this.lastProcessTime;

        if (elapsed < interval) {
          await this.delay(interval - elapsed);
        }

        try {
          const message = JSON.parse(msg.content.toString());
          await handler(message);
          channel.ack(msg);
          this.lastProcessTime = Date.now();
        } catch (error) {
          console.error('Error processing message:', error);
          channel.nack(msg, false, true);
        }
      }
    });
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

---

## Dead Letter Queues

### DLX Setup

```typescript
// dead-letter-queue.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class DeadLetterQueue {
  constructor(private connection: RabbitMQConnection) {}

  async setup(
    queueName: string,
    dlxName: string,
    dlqName: string,
    maxRetries: number = 3
  ) {
    const channel = this.connection.getChannel();

    // Declare dead letter exchange
    await channel.assertExchange(dlxName, 'direct', { durable: true });

    // Declare dead letter queue
    await channel.assertQueue(dlqName, { durable: true });
    await channel.bindQueue(dlqName, dlxName, '');

    // Declare main queue with DLX arguments
    await channel.assertQueue(queueName, {
      durable: true,
      arguments: {
        'x-dead-letter-exchange': dlxName,
        'x-dead-letter-routing-key': '',
        'x-max-retries': maxRetries
      }
    });
  }

  async publish(queueName: string, message: any) {
    const channel = this.connection.getChannel();
    channel.publish(
      '',
      queueName,
      Buffer.from(JSON.stringify(message)),
      {
        persistent: true,
        headers: {
          'x-retry-count': 0
        }
      }
    );
  }

  async consumeDLQ(dlqName: string, handler: (message: any) => Promise<void>) {
    const channel = this.connection.getChannel();
    await channel.consume(dlqName, async (msg) => {
      if (msg) {
        const message = JSON.parse(msg.content.toString());
        const retryCount = msg.properties.headers?.['x-retry-count'] || 0;

        await handler({ ...message, retryCount });
        channel.ack(msg);
      }
    });
  }
}

// Usage
const dlq = new DeadLetterQueue(connection);
await dlq.setup('tasks', 'tasks-dlx', 'tasks-dlq', 3);
```

---

## Message Acknowledgment

### Manual Acknowledgment

```typescript
// manual-ack.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class ManualAckConsumer {
  constructor(private connection: RabbitMQConnection) {}

  async consume(queueName: string, handler: (message: any) => Promise<boolean>) {
    const channel = this.connection.getChannel();
    await channel.prefetch(10);  // Limit unacknowledged messages

    await channel.consume(queueName, async (msg) => {
      if (msg) {
        try {
          const message = JSON.parse(msg.content.toString());
          const success = await handler(message);

          if (success) {
            channel.ack(msg);  // Acknowledge successful processing
          } else {
            channel.nack(msg, false, true);  // Requeue message
          }
        } catch (error) {
          console.error('Error processing message:', error);
          channel.nack(msg, false, false);  // Don't requeue, send to DLQ
        }
      }
    });
  }
}
```

---

## Persistence

### Durable Queues and Messages

```typescript
// persistence.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class PersistentMessaging {
  constructor(private connection: RabbitMQConnection) {}

  async setupDurableQueue(queueName: string) {
    const channel = this.connection.getChannel();
    await channel.assertQueue(queueName, { durable: true });
  }

  async publishPersistent(queueName: string, message: any) {
    const channel = this.connection.getChannel();
    channel.sendToQueue(
      queueName,
      Buffer.from(JSON.stringify(message)),
      {
        persistent: true,  // Message survives broker restart
        deliveryMode: 2   // Persistent delivery mode
      }
    );
  }
}
```

---

## Error Handling

### Error Handling Strategies

```typescript
// error-handling.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class ErrorHandler {
  private errorCount = 0;
  private maxErrors = 5;
  private backoffTime = 1000;

  async consumeWithRetry(
    queueName: string,
    handler: (message: any) => Promise<void>
  ) {
    const channel = this.connection.getChannel();

    await channel.consume(queueName, async (msg) => {
      if (msg) {
        try {
          const message = JSON.parse(msg.content.toString());
          await handler(message);
          channel.ack(msg);
          this.errorCount = 0;  // Reset on success
        } catch (error) {
          this.errorCount++;
          console.error(`Error ${this.errorCount}:`, error);

          if (this.errorCount >= this.maxErrors) {
            // Max retries reached, send to DLQ
            channel.nack(msg, false, false);
            this.errorCount = 0;
          } else {
            // Requeue with backoff
            await this.delay(this.backoffTime * this.errorCount);
            channel.nack(msg, false, true);
          }
        }
      }
    });
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

---

## Performance Optimization

### Connection Pooling

```typescript
// connection-pool.ts
import amqp from 'amqplib';

export class ConnectionPool {
  private pool: amqp.Channel[] = [];
  private maxSize: number;

  constructor(maxSize: number = 10) {
    this.maxSize = maxSize;
  }

  async getChannel(url: string): Promise<amqp.Channel> {
    if (this.pool.length > 0) {
      return this.pool.pop()!;
    }

    const connection = await amqp.connect(url);
    return await connection.createChannel();
  }

  releaseChannel(channel: amqp.Channel) {
    if (this.pool.length < this.maxSize) {
      this.pool.push(channel);
    } else {
      channel.close();
    }
  }
}
```

---

## Monitoring

### Health Check

```typescript
// health-check.ts
import { RabbitMQConnection } from './rabbitmq-connection';

export class HealthCheck {
  constructor(private connection: RabbitMQConnection) {}

  async check(): Promise<boolean> {
    try {
      const channel = this.connection.getChannel();
      await channel.checkExchange('amq.direct');  // Built-in exchange
      return true;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  async getQueueInfo(queueName: string): Promise<any> {
    const channel = this.connection.getChannel();
    return await channel.checkQueue(queueName);
  }
}
```

---

## Production Setup

### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  rabbitmq:
    image: rabbitmq:3-management
    container_name: rabbitmq
    ports:
      - "5672:5672"   # AMQP port
      - "15672:15672" # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: admin123
      RABBITMQ_DEFAULT_VHOST: /
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  rabbitmq_data:
```

### Configuration Best Practices

```typescript
// config.ts
export interface RabbitMQConfig {
  url: string;
  prefetch: number;
  reconnectDelay: number;
  maxRetries: number;
  heartbeat: number;
}

export const defaultConfig: RabbitMQConfig = {
  url: process.env.RABBITMQ_URL || 'amqp://localhost',
  prefetch: 10,
  reconnectDelay: 5000,
  maxRetries: 10,
  heartbeat: 60
};
```

---

## Additional Resources

- [RabbitMQ Official Documentation](https://www.rabbitmq.com/docs/)
- [amqplib Documentation](https://www.squaremo.com/amqp.node/)
- [Pika Documentation](https://pika.readthedocs.io/)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/tutorials/)

## Best Practices

### Exchange Selection

- **Use Direct Exchange**: For point-to-point routing with specific routing keys
- **Use Topic Exchange**: For flexible routing with pattern matching
- **Use Fanout Exchange**: For broadcast to multiple consumers
- **Use Headers Exchange**: For complex routing based on message headers
- **Document exchange purpose**: Clear documentation for each exchange

### Queue Configuration

- **Use durable queues**: For critical data that must survive broker restart
- **Set appropriate TTL**: Configure message and queue TTL for cleanup
- **Use exclusive queues**: For temporary, single-consumer queues
- **Configure auto-delete**: For queues that should be deleted when unused
- **Set queue length limits**: Prevent memory exhaustion

### Message Design

- **Keep messages small**: Prefer messages under 1MB for optimal performance
- **Include message metadata**: Add headers for routing and tracing
- **Use consistent schemas**: Define message formats and versions
- **Design for idempotency**: Messages may be delivered multiple times
- **Add correlation IDs**: For request/response patterns

### Consumer Configuration

- **Use manual acknowledgments**: Enable manual ack for better control
- **Set appropriate prefetch**: Limit unacknowledged messages per consumer
- **Handle acknowledgments properly**: Always ack or nack messages
- **Implement graceful shutdown**: Stop consuming and close connections properly
- **Monitor consumer health**: Track message processing rates

### Producer Configuration

- **Use publisher confirms**: Ensure messages are received by broker
- **Set persistent delivery**: For critical messages that must survive restart
- **Implement retry logic**: Handle transient failures
- **Use connection pooling**: Reuse connections for better performance
- **Batch messages when possible**: Reduce network overhead

### Dead Letter Handling

- **Always use DLX**: Route failed messages to dead letter queue
- **Configure retry policies**: Set max retry counts and backoff
- **Monitor DLQ size**: Alert on growing dead letter queues
- **Process DLQ messages**: Analyze and reprocess failed messages
- **Document DLQ handling**: Clear procedures for handling failed messages

### Performance Optimization

- **Use multiple queues**: Distribute load across queues
- **Configure appropriate prefetch**: Balance between throughput and fairness
- **Use connection pooling**: Limit number of TCP connections
- **Enable compression**: For large message payloads
- **Monitor resource usage**: Track memory, CPU, and disk I/O

### Security

- **Enable authentication**: Use username/password or certificates
- **Configure TLS encryption**: Encrypt connections in production
- **Use virtual hosts**: Isolate different applications
- **Set up user permissions**: Restrict access to specific resources
- **Audit access logs**: Monitor who is accessing what

### Monitoring and Observability

- **Track queue depths**: Monitor message counts in queues
- **Monitor consumer lag**: Track unprocessed messages
- **Collect broker metrics**: Use management API or plugins
- **Set up alerts**: Alert on queue depth, consumer failures, or broker issues
- **Use distributed tracing**: Correlate messages across services

### High Availability

- **Use clustering**: Set up RabbitMQ cluster for high availability
- **Configure queue mirroring**: Replicate queues across cluster nodes
- **Use load balancers**: Distribute connections across cluster nodes
- **Test failover scenarios**: Verify automatic recovery works
- **Monitor cluster health**: Track node status and synchronization

## Checklist

### Setup and Configuration
- [ ] Install and configure RabbitMQ broker
- [ ] Enable management plugin for monitoring
- [ ] Configure authentication and authorization
- [ ] Set up TLS encryption for secure connections
- [ ] Configure clustering for high availability

### Exchange Setup
- [ ] Choose appropriate exchange type for each use case
- [ ] Document exchange purpose and routing rules
- [ ] Configure durable exchanges for critical data
- [ ] Set up exchange-to-exchange bindings if needed
- [ ] Test exchange routing behavior

### Queue Setup
- [ ] Configure durable queues for critical data
- [ ] Set appropriate TTL for messages and queues
- [ ] Configure dead letter exchange for failed messages
- [ ] Set queue length limits to prevent memory issues
- [ ] Document queue purpose and usage

### Producer Configuration
- [ ] Enable publisher confirms
- [ ] Set persistent delivery for critical messages
- [ ] Implement retry logic with backoff
- [ ] Use connection pooling
- [ ] Add message metadata and correlation IDs

### Consumer Configuration
- [ ] Use manual acknowledgments
- [ ] Set appropriate prefetch count
- [ ] Implement graceful shutdown handling
- [ ] Configure error handling and DLQ routing
- [ ] Monitor consumer health and processing rates

### Dead Letter Queue Setup
- [ ] Configure dead letter exchange
- [ ] Set up dead letter queues
- [ ] Configure retry policies (max retries, backoff)
- [ ] Set up DLQ monitoring and alerts
- [ ] Document DLQ processing procedures

### Security Setup
- [ ] Enable authentication (username/password or certificates)
- [ ] Configure TLS/SSL encryption
- [ ] Set up virtual hosts for isolation
- [ ] Configure user permissions and ACLs
- [ ] Enable audit logging

### Performance Tuning
- [ ] Tune prefetch settings for consumers
- [ ] Configure connection pooling
- [ ] Enable compression for large messages
- [ ] Monitor resource usage (memory, CPU, disk)
- [ ] Optimize queue and exchange configurations

### High Availability
- [ ] Set up RabbitMQ cluster
- [ ] Configure queue mirroring
- [ ] Set up load balancer for connections
- [ ] Test failover scenarios
- [ ] Monitor cluster health and synchronization

### Monitoring and Alerting
- [ ] Enable management plugin
- [ ] Set up metrics collection (Prometheus/Grafana)
- [ ] Configure alerts for queue depth
- [ ] Monitor consumer lag and processing rates
- [ ] Track broker health metrics

### Testing
- [ ] Test message publishing and consuming
- [ ] Verify exchange routing behavior
- [ ] Test dead letter queue routing
- [ ] Validate acknowledgment behavior
- [ ] Test failover and recovery

### Documentation
- [ ] Document exchange and queue structure
- [ ] Document message schemas and formats
- [ ] Create runbooks for common issues
- [ ] Document security configuration
- [ ] Maintain API documentation
