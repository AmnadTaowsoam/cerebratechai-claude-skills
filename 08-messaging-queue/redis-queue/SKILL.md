# Redis Queue

## Overview

Comprehensive guide to Redis as a message queue using Bull and BullMQ for Node.js applications.

## Table of Contents

1. [Redis Queue Concepts](#redis-queue-concepts)
2. [Bull/BullMQ Setup](#bullbullmq-setup)
3. [Job Creation](#job-creation)
4. [Job Processing](#job-processing)
5. [Job Priorities](#job-priorities)
6. [Delayed Jobs](#delayed-jobs)
7. [Repeatable Jobs](#repeatable-jobs)
8. [Job Lifecycle](#job-lifecycle)
9. [Error Handling](#error-handling)
10. [Retries](#retries)
11. [Queue Monitoring](#queue-monitoring)
12. [Scaling Workers](#scaling-workers)
13. [Production Patterns](#production-patterns)

---

## Redis Queue Concepts

### Core Concepts

```typescript
// Redis Queue Core Concepts
/**
 * Queue: A named list of jobs waiting to be processed
 * Job: A unit of work to be processed
 * Worker: A process that processes jobs from a queue
 * Priority: Importance level of a job (higher = processed first)
 * Delay: Time to wait before processing a job
 * Repeat: Schedule jobs to run periodically
 * Retry: Automatic retry of failed jobs
 * Backoff: Delay between retry attempts
 */
```

### Basic Setup

```typescript
// redis-connection.ts
import { Queue, Worker, Job, QueueOptions } from 'bullmq';
import { Redis } from 'ioredis';

// Redis connection configuration
export const redisConfig = {
  host: process.env.REDIS_HOST || 'localhost',
  port: parseInt(process.env.REDIS_PORT || '6379'),
  password: process.env.REDIS_PASSWORD,
  db: parseInt(process.env.REDIS_DB || '0'),
  maxRetriesPerRequest: 3,
  retryStrategy: (times: number) => {
    const delay = Math.min(times * 50, 2000);
    return delay;
  }
};

// Create Redis connection
export const createRedisConnection = () => {
  return new Redis(redisConfig);
};

// Default queue options
export const defaultQueueOptions: QueueOptions = {
  connection: createRedisConnection(),
  defaultJobOptions: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
    removeOnComplete: 100,
    removeOnFail: 50,
  },
};
```

---

## Bull/BullMQ Setup

### BullMQ Queue Setup

```typescript
// queue-setup.ts
import { Queue, QueueOptions } from 'bullmq';
import { defaultQueueOptions } from './redis-connection';

export class JobQueue {
  private queue: Queue;

  constructor(name: string, options?: QueueOptions) {
    this.queue = new Queue(name, {
      ...defaultQueueOptions,
      ...options,
    });
  }

  getQueue(): Queue {
    return this.queue;
  }

  async close(): Promise<void> {
    await this.queue.close();
  }

  async getQueueStats(): Promise<any> {
    const counts = await this.queue.getJobCounts();
    const workers = await this.queue.getWorkers();
    
    return {
      waiting: counts.waiting,
      active: counts.active,
      completed: counts.completed,
      failed: counts.failed,
      delayed: counts.delayed,
      paused: counts.paused,
      workerCount: workers.length,
    };
  }
}

// Usage
const emailQueue = new JobQueue('emails');
const stats = await emailQueue.getQueueStats();
console.log(stats);
```

### Worker Setup

```typescript
// worker-setup.ts
import { Worker, WorkerOptions, Job } from 'bullmq';
import { createRedisConnection } from './redis-connection';

export class JobWorker {
  private worker: Worker;

  constructor(
    queueName: string,
    processor: (job: Job) => Promise<void>,
    options?: WorkerOptions
  ) {
    this.worker = new Worker(
      queueName,
      processor,
      {
        connection: createRedisConnection(),
        concurrency: 5,
        ...options,
      }
    );

    this.setupEventListeners();
  }

  private setupEventListeners(): void {
    this.worker.on('completed', (job: Job) => {
      console.log(`Job ${job.id} completed`);
    });

    this.worker.on('failed', (job: Job | undefined, error: Error) => {
      console.error(`Job ${job?.id} failed:`, error.message);
    });

    this.worker.on('error', (error: Error) => {
      console.error('Worker error:', error);
    });

    this.worker.on('stalled', (job: Job) => {
      console.warn(`Job ${job.id} stalled`);
    });
  }

  async close(): Promise<void> {
    await this.worker.close();
  }
}

// Usage
const worker = new JobWorker('emails', async (job) => {
  console.log('Processing job:', job.data);
  await sendEmail(job.data);
});
```

---

## Job Creation

### Basic Job Creation

```typescript
// job-creation.ts
import { JobQueue } from './queue-setup';

export class JobManager {
  constructor(private queue: JobQueue) {}

  async addJob(name: string, data: any, options?: any): Promise<Job> {
    const job = await this.queue.getQueue().add(name, data, options);
    console.log(`Job ${job.id} added to queue`);
    return job;
  }

  async addBulkJobs(jobs: Array<{ name: string; data: any; opts?: any }>): Promise<Job[]> {
    const addedJobs = await this.queue.getQueue().addBulk(jobs);
    console.log(`Added ${addedJobs.length} jobs to queue`);
    return addedJobs;
  }
}

// Usage
const jobManager = new JobManager(emailQueue);

// Add single job
await jobManager.addJob('send-email', {
  to: 'user@example.com',
  subject: 'Welcome',
  body: 'Hello!'
});

// Add bulk jobs
await jobManager.addBulkJobs([
  { name: 'send-email', data: { to: 'user1@example.com' } },
  { name: 'send-email', data: { to: 'user2@example.com' } },
  { name: 'send-email', data: { to: 'user3@example.com' } },
]);
```

### Job with Options

```typescript
// job-options.ts
import { Job } from 'bullmq';

export interface JobOptions {
  // Retry options
  attempts?: number;
  backoff?: {
    type: 'exponential' | 'fixed';
    delay: number;
  };
  
  // Priority
  priority?: number;
  
  // Delay
  delay?: number;
  
  // Lifecycle
  removeOnComplete?: number | boolean;
  removeOnFail?: number | boolean;
  
  // Timeout
  timeout?: number;
  
  // Custom data
  jobId?: string;
  repeat?: any;
}

export class AdvancedJobManager extends JobManager {
  async addJobWithOptions(
    name: string,
    data: any,
    options: JobOptions
  ): Promise<Job> {
    return await this.addJob(name, data, options);
  }
}

// Usage
const advancedManager = new AdvancedJobManager(emailQueue);

// High priority job
await advancedManager.addJobWithOptions('send-email', emailData, {
  priority: 10,
  attempts: 5,
  backoff: {
    type: 'exponential',
    delay: 1000,
  },
});

// Low priority job
await advancedManager.addJobWithOptions('send-email', emailData, {
  priority: 1,
  attempts: 3,
});
```

---

## Job Processing

### Basic Processor

```typescript
// processor.ts
import { Job } from 'bullmq';

export interface EmailData {
  to: string;
  subject: string;
  body: string;
}

export async function emailProcessor(job: Job<EmailData>): Promise<void> {
  const { to, subject, body } = job.data;

  console.log(`Sending email to ${to}`);
  
  // Simulate email sending
  await new Promise(resolve => setTimeout(resolve, 1000));
  
  console.log(`Email sent to ${to}`);
  
  // Update progress
  job.updateProgress(100);
}

// Usage in worker
const worker = new JobWorker('emails', emailProcessor);
```

### Progress Tracking

```typescript
// progress-tracking.ts
import { Job } from 'bullmq';

export async function longRunningProcessor(job: Job): Promise<void> {
  const totalSteps = 100;
  
  for (let i = 0; i < totalSteps; i++) {
    // Process step
    await processStep(i);
    
    // Update progress
    await job.updateProgress(Math.round((i / totalSteps) * 100));
    
    // Log progress
    job.log(`Completed step ${i + 1} of ${totalSteps}`);
  }
}

async function processStep(step: number): Promise<void> {
  // Simulate work
  await new Promise(resolve => setTimeout(resolve, 50));
}

// Usage
const worker = new JobWorker('long-tasks', longRunningProcessor);
```

### Job Dependencies

```typescript
// job-dependencies.ts
import { JobQueue } from './queue-setup';

export class JobDependencyManager {
  constructor(private queue: JobQueue) {}

  async addChainedJobs(jobs: Array<{ name: string; data: any }>): Promise<Job> {
    const queue = this.queue.getQueue();
    
    // Create job chain
    const chain = jobs.map(job => ({ name: job.name, data: job.data }));
    
    const job = await queue.addBulk(chain);
    
    // Add dependencies
    for (let i = 1; i < job.length; i++) {
      await job[i].addDependency(job[i - 1]);
    }
    
    return job[job.length - 1];
  }

  async addParallelJobs(
    parentJobId: string,
    jobs: Array<{ name: string; data: any }>
  ): Promise<Job[]> {
    const queue = this.queue.getQueue();
    const parentJob = await queue.getJob(parentJobId);
    
    if (!parentJob) {
      throw new Error('Parent job not found');
    }
    
    const addedJobs = await queue.addBulk(jobs);
    
    // Add parent dependency to all jobs
    for (const job of addedJobs) {
      await job.addDependency(parentJob);
    }
    
    return addedJobs;
  }
}

// Usage
const dependencyManager = new JobDependencyManager(emailQueue);

// Chained jobs
await dependencyManager.addChainedJobs([
  { name: 'validate-email', data: { email: 'user@example.com' } },
  { name: 'send-email', data: { to: 'user@example.com' } },
  { name: 'log-email', data: { email: 'user@example.com' } },
]);

// Parallel jobs after parent
const parentJob = await jobManager.addJob('prepare-data', {});
await dependencyManager.addParallelJobs(parentJob.id!, [
  { name: 'process-a', data: {} },
  { name: 'process-b', data: {} },
  { name: 'process-c', data: {} },
]);
```

---

## Job Priorities

### Priority Queue

```typescript
// priority-queue.ts
import { JobQueue } from './queue-setup';

export class PriorityJobManager extends JobManager {
  async addHighPriorityJob(name: string, data: any): Promise<Job> {
    return await this.addJob(name, data, { priority: 10 });
  }

  async addMediumPriorityJob(name: string, data: any): Promise<Job> {
    return await this.addJob(name, data, { priority: 5 });
  }

  async addLowPriorityJob(name: string, data: any): Promise<Job> {
    return await this.addJob(name, data, { priority: 1 });
  }

  async addPriorityJob(
    name: string,
    data: any,
    priority: number
  ): Promise<Job> {
    return await this.addJob(name, data, { priority });
  }
}

// Usage
const priorityManager = new PriorityJobManager(emailQueue);

// Add jobs with different priorities
await priorityManager.addHighPriorityJob('urgent-email', urgentEmailData);
await priorityManager.addMediumPriorityJob('normal-email', normalEmailData);
await priorityManager.addLowPriorityJob('newsletter-email', newsletterData);

// Custom priority
await priorityManager.addPriorityJob('custom-priority', data, 7);
```

---

## Delayed Jobs

### Delayed Job Creation

```typescript
// delayed-jobs.ts
import { JobQueue } from './queue-setup';

export class DelayedJobManager extends JobManager {
  async addDelayedJob(
    name: string,
    data: any,
    delayMs: number
  ): Promise<Job> {
    return await this.addJob(name, data, { delay: delayMs });
  }

  async addDelayedJobByDate(
    name: string,
    data: any,
    executeAt: Date
  ): Promise<Job> {
    const delay = executeAt.getTime() - Date.now();
    if (delay < 0) {
      throw new Error('Execution time must be in the future');
    }
    return await this.addJob(name, data, { delay });
  }
}

// Usage
const delayedManager = new DelayedJobManager(emailQueue);

// Delay by milliseconds
await delayedManager.addDelayedJob('send-reminder', reminderData, 60000); // 1 minute

// Delay to specific time
const executeAt = new Date('2024-01-01T10:00:00Z');
await delayedManager.addDelayedJobByDate('send-scheduled-email', emailData, executeAt);
```

---

## Repeatable Jobs

### Cron Jobs

```typescript
// repeatable-jobs.ts
import { JobQueue } from './queue-setup';

export class RepeatableJobManager extends JobManager {
  async addCronJob(
    name: string,
    data: any,
    cronPattern: string
  ): Promise<Job> {
    return await this.addJob(name, data, {
      repeat: {
        pattern: cronPattern,
      },
    });
  }

  async addRepeatJob(
    name: string,
    data: any,
    options: {
      every?: number;  // milliseconds
      cron?: string;
      startDate?: Date;
      endDate?: Date;
      tz?: string;
    }
  ): Promise<Job> {
    return await this.addJob(name, data, {
      repeat: options,
    });
  }

  async removeRepeatableJob(name: string, repeat: any): Promise<void> {
    await this.queue.getQueue().removeRepeatable(name, repeat);
  }
}

// Usage
const repeatableManager = new RepeatableJobManager(emailQueue);

// Run every minute
await repeatableManager.addRepeatJob('cleanup', {}, {
  every: 60000, // 1 minute
});

// Run daily at midnight
await repeatableManager.addCronJob('daily-report', {}, '0 0 * * *');

// Run every Monday at 9 AM
await repeatableManager.addRepeatJob('weekly-summary', {}, {
  cron: '0 9 * * 1',
  tz: 'America/New_York',
});

// Run with start and end date
await repeatableManager.addRepeatJob('campaign', {}, {
  every: 86400000, // 1 day
  startDate: new Date('2024-01-01'),
  endDate: new Date('2024-12-31'),
});

// Remove repeatable job
await repeatableManager.removeRepeatableJob('cleanup', { every: 60000 });
```

---

## Job Lifecycle

### Job States

```typescript
// job-lifecycle.ts
import { JobQueue } from './queue-setup';

export class JobLifecycleManager {
  constructor(private queue: JobQueue) {}

  async getJob(jobId: string): Promise<Job | undefined> {
    return await this.queue.getQueue().getJob(jobId);
  }

  async getJobState(jobId: string): Promise<string> {
    const job = await this.getJob(jobId);
    if (!job) {
      return 'unknown';
    }
    return await job.getState();
  }

  async getJobsByState(state: string, start: number = 0, end: number = 10): Promise<Job[]> {
    return await this.queue.getQueue().getJobs([state], start, end);
  }

  async retryJob(jobId: string): Promise<Job> {
    const job = await this.getJob(jobId);
    if (!job) {
      throw new Error('Job not found');
    }
    return await job.retry();
  }

  async promoteJob(jobId: string): Promise<Job> {
    const job = await this.getJob(jobId);
    if (!job) {
      throw new Error('Job not found');
    }
    return await job.promote();
  }

  async removeJob(jobId: string): Promise<void> {
    const job = await this.getJob(jobId);
    if (!job) {
      throw new Error('Job not found');
    }
    await job.remove();
  }
}

// Usage
const lifecycleManager = new JobLifecycleManager(emailQueue);

// Get job state
const state = await lifecycleManager.getJobState('job-id');
console.log('Job state:', state);

// Get failed jobs
const failedJobs = await lifecycleManager.getJobsByState('failed');

// Retry failed job
await lifecycleManager.retryJob('failed-job-id');

// Promote delayed job
await lifecycleManager.promoteJob('delayed-job-id');
```

---

## Error Handling

### Error Handling in Processor

```typescript
// error-handling.ts
import { Job } from 'bullmq';

export class ErrorHandler {
  static async safeProcessor<T>(
    job: Job<T>,
    handler: (job: Job<T>) => Promise<void>
  ): Promise<void> {
    try {
      await handler(job);
    } catch (error) {
      console.error('Processor error:', error);
      
      // Add error metadata
      job.data.error = {
        message: (error as Error).message,
        stack: (error as Error).stack,
        timestamp: new Date().toISOString(),
      };
      
      // Re-throw to let BullMQ handle retries
      throw error;
    }
  }
}

// Usage
const worker = new JobWorker('emails', async (job) => {
  await ErrorHandler.safeProcessor(job, async (j) => {
    await emailProcessor(j);
  });
});
```

### Custom Error Types

```typescript
// custom-errors.ts
export class RetryableError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'RetryableError';
  }
}

export class NonRetryableError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NonRetryableError';
  }
}

// Usage in processor
export async function smartProcessor(job: Job): Promise<void> {
  try {
    await processJob(job);
  } catch (error) {
    if (error instanceof RetryableError) {
      // Let BullMQ handle retry
      throw error;
    } else if (error instanceof NonRetryableError) {
      // Don't retry, mark as failed
      throw error;
    } else {
      // Default to retryable
      throw new RetryableError(error.message);
    }
  }
}
```

---

## Retries

### Retry Configuration

```typescript
// retry-config.ts
export interface RetryConfig {
  attempts: number;
  backoff: {
    type: 'exponential' | 'fixed';
    delay: number;
  };
}

export const retryConfigs: Record<string, RetryConfig> = {
  default: {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
  },
  aggressive: {
    attempts: 10,
    backoff: {
      type: 'exponential',
      delay: 1000,
    },
  },
  conservative: {
    attempts: 2,
    backoff: {
      type: 'fixed',
      delay: 5000,
    },
  },
};

// Usage
await jobManager.addJob('send-email', data, retryConfigs.aggressive);
```

### Custom Retry Logic

```typescript
// custom-retry.ts
import { Job } from 'bullmq';

export class CustomRetryHandler {
  static async shouldRetry(job: Job, error: Error): Promise<boolean> {
    const attemptsMade = job.attemptsMade;
    const maxAttempts = job.opts.attempts || 3;
    
    // Don't retry if max attempts reached
    if (attemptsMade >= maxAttempts) {
      return false;
    }
    
    // Don't retry certain errors
    if (error.message.includes('invalid')) {
      return false;
    }
    
    // Retry on network errors
    if (error.message.includes('timeout') || error.message.includes('network')) {
      return true;
    }
    
    // Default to retry
    return true;
  }

  static async getRetryDelay(job: Job): Promise<number> {
    const attemptsMade = job.attemptsMade;
    
    // Exponential backoff
    return Math.pow(2, attemptsMade) * 1000;
  }
}

// Usage in worker
const worker = new JobWorker('emails', async (job) => {
  try {
    await processJob(job);
  } catch (error) {
    if (await CustomRetryHandler.shouldRetry(job, error as Error)) {
      const delay = await CustomRetryHandler.getRetryDelay(job);
      await job.moveToDelayed(Date.now() + delay);
      throw error;
    } else {
      throw error;
    }
  }
});
```

---

## Queue Monitoring

### Queue Statistics

```typescript
// queue-monitoring.ts
import { JobQueue } from './queue-setup';

export class QueueMonitor {
  constructor(private queue: JobQueue) {}

  async getQueueMetrics(): Promise<any> {
    const queue = this.queue.getQueue();
    
    const [
      waiting,
      active,
      completed,
      failed,
      delayed,
      paused,
    ] = await Promise.all([
        queue.getWaiting(),
        queue.getActive(),
        queue.getCompleted(),
        queue.getFailed(),
        queue.getDelayed(),
        queue.isPaused(),
      ]);
    
    return {
      waiting: waiting.length,
      active: active.length,
      completed: completed.length,
      failed: failed.length,
      delayed: delayed.length,
      paused,
    };
  }

  async getJobCounts(): Promise<any> {
    return await this.queue.getQueue().getJobCounts();
  }

  async getWorkers(): Promise<any[]> {
    const workers = await this.queue.getQueue().getWorkers();
    return workers.map(worker => ({
      name: worker.name,
      pid: worker.process.pid,
      ready: worker.isReady(),
    }));
  }

  async getJobHistory(jobId: string): Promise<any> {
    const job = await this.queue.getQueue().getJob(jobId);
    if (!job) {
      return null;
    }
    
    return {
      id: job.id,
      name: job.name,
      data: job.data,
      progress: job.progress,
      attemptsMade: job.attemptsMade,
      failedReason: job.failedReason,
      processedOn: job.processedOn,
      finishedOn: job.finishedOn,
      stacktrace: job.stacktrace,
    };
  }
}

// Usage
const monitor = new QueueMonitor(emailQueue);
const metrics = await monitor.getQueueMetrics();
console.log('Queue metrics:', metrics);
```

---

## Scaling Workers

### Horizontal Scaling

```typescript
// worker-scaling.ts
import { JobWorker } from './worker-setup';

export class WorkerPool {
  private workers: JobWorker[] = [];
  private concurrency: number;

  constructor(
    queueName: string,
    processor: (job: any) => Promise<void>,
    concurrency: number = 5,
    workerCount: number = 1
  ) {
    this.concurrency = concurrency;
    
    // Create multiple workers
    for (let i = 0; i < workerCount; i++) {
      const worker = new JobWorker(
        queueName,
        processor,
        { concurrency: this.concurrency }
      );
      this.workers.push(worker);
    }
  }

  async scaleUp(additionalWorkers: number): Promise<void> {
    for (let i = 0; i < additionalWorkers; i++) {
      const worker = new JobWorker(
        this.workers[0].name,
        this.workers[0].processor,
        { concurrency: this.concurrency }
      );
      this.workers.push(worker);
    }
  }

  async scaleDown(removeWorkers: number): Promise<void> {
    const workersToRemove = this.workers.splice(0, removeWorkers);
    for (const worker of workersToRemove) {
      await worker.close();
    }
  }

  async closeAll(): Promise<void> {
    for (const worker of this.workers) {
      await worker.close();
    }
    this.workers = [];
  }
}

// Usage
const workerPool = new WorkerPool('emails', emailProcessor, 5, 3);

// Scale up during peak hours
await workerPool.scaleUp(2);

// Scale down during off-peak hours
await workerPool.scaleDown(1);
```

---

## Production Patterns

### Graceful Shutdown

```typescript
// graceful-shutdown.ts
import { JobWorker } from './worker-setup';

export class GracefulWorker extends JobWorker {
  private isShuttingDown = false;

  constructor(
    queueName: string,
    processor: (job: any) => Promise<void>,
    options?: any
  ) {
    super(queueName, processor, options);
    this.setupShutdownHandlers();
  }

  private setupShutdownHandlers(): void {
    process.on('SIGTERM', () => this.shutdown('SIGTERM'));
    process.on('SIGINT', () => this.shutdown('SIGINT'));
  }

  private async shutdown(signal: string): Promise<void> {
    console.log(`Received ${signal}, shutting down gracefully...`);
    this.isShuttingDown = true;
    
    // Stop accepting new jobs
    await this.worker.pause();
    
    // Wait for active jobs to complete
    await this.worker.waitUntilReady();
    
    // Close worker
    await this.close();
    
    console.log('Worker shut down gracefully');
    process.exit(0);
  }
}

// Usage
const worker = new GracefulWorker('emails', emailProcessor);
```

### Health Check

```typescript
// health-check.ts
import { JobQueue } from './queue-setup';

export class HealthChecker {
  constructor(private queue: JobQueue) {}

  async checkHealth(): Promise<{
    healthy: boolean;
    metrics: any;
  }> {
    try {
      const metrics = await this.queue.getQueueStats();
      
      // Check if queue is healthy
      const healthy = (
        metrics.active < 100 &&  // Not too many active jobs
        metrics.failed < 1000    // Not too many failed jobs
      );
      
      return { healthy, metrics };
    } catch (error) {
      return {
        healthy: false,
        metrics: null,
        error: (error as Error).message,
      };
    }
  }
}

// Usage in Express
import express from 'express';

const app = express();
const healthChecker = new HealthChecker(emailQueue);

app.get('/health', async (req, res) => {
  const health = await healthChecker.checkHealth();
  res.status(health.healthy ? 200 : 503).json(health);
});
```

---

## Additional Resources

- [BullMQ Documentation](https://docs.bullmq.io/)
- [Bull Documentation](https://github.com/OptimalBits/bull)
- [Redis Documentation](https://redis.io/documentation)
- [ioredis Documentation](https://github.com/luin/ioredis)

## Best Practices

### Queue Configuration

- **Use separate queues for different job types**: This allows for independent scaling and prioritization
- **Set appropriate `removeOnComplete` and `removeOnFail` values**: Keep enough history for debugging but avoid memory bloat
- **Configure `attempts` and `backoff` appropriately**: Balance between reliability and processing time
- **Use `prefetch` for fair distribution**: Prevent one worker from hogging all jobs
- **Set reasonable `timeout` values**: Prevent stuck jobs from blocking workers

### Worker Configuration

- **Set appropriate `concurrency`**: Too high can overwhelm resources, too low wastes capacity
- **Implement graceful shutdown**: Handle SIGTERM/SIGINT to complete in-flight jobs
- **Monitor worker health**: Track active jobs, failed jobs, and queue depth
- **Use separate worker processes**: Isolate failures and improve reliability
- **Implement proper error handling**: Distinguish between retryable and non-retryable errors

### Job Design

- **Keep jobs idempotent**: Jobs should be safe to retry without side effects
- **Use job dependencies**: Ensure proper ordering when required
- **Implement progress tracking**: Provide visibility into long-running jobs
- **Add job metadata**: Include context for debugging and monitoring
- **Design for eventual consistency**: Jobs may not execute immediately

### Production Considerations

- **Use Redis Cluster for high availability**: Distribute load across multiple nodes
- **Enable persistence**: Configure Redis AOF or RDB for durability
- **Monitor Redis metrics**: Track memory usage, connections, and command stats
- **Implement rate limiting**: Prevent queue flooding from overwhelming workers
- **Use job priorities**: Ensure critical jobs are processed first

### Security

- **Use Redis AUTH**: Protect your Redis instance with password authentication
- **Enable TLS**: Encrypt connections between workers and Redis
- **Use connection pooling**: Limit the number of connections to Redis
- **Sanitize job data**: Prevent injection attacks through job payloads
- **Implement job size limits**: Prevent memory exhaustion from large jobs

## Checklist

### Setup and Configuration
- [ ] Configure Redis connection with appropriate settings
- [ ] Set up separate queues for different job types
- [ ] Configure default job options (attempts, backoff, timeout)
- [ ] Set up Redis persistence (AOF/RDB)
- [ ] Configure Redis authentication and TLS

### Queue Management
- [ ] Implement queue monitoring and metrics collection
- [ ] Set up alerts for queue depth and failure rates
- [ ] Configure job cleanup policies (removeOnComplete/removeOnFail)
- [ ] Implement queue pausing and draining procedures
- [ ] Set up queue backup and recovery procedures

### Worker Setup
- [ ] Configure appropriate concurrency per worker
- [ ] Implement graceful shutdown handling
- [ ] Set up worker health checks
- [ ] Configure worker logging and error tracking
- [ ] Implement worker restart policies

### Job Processing
- [ ] Implement idempotent job handlers
- [ ] Add progress tracking for long-running jobs
- [ ] Configure appropriate retry strategies
- [ ] Implement dead letter queue for failed jobs
- [ ] Add job metadata for debugging

### Monitoring and Alerting
- [ ] Set up dashboard for queue metrics
- [ ] Configure alerts for queue depth thresholds
- [ ] Monitor worker health and restart failures
- [ ] Track job completion rates and latency
- [ ] Set up logs aggregation and search

### Security and Compliance
- [ ] Enable Redis authentication
- [ ] Configure TLS for Redis connections
- [ ] Implement job data sanitization
- [ ] Set up access controls for queue operations
- [ ] Audit queue access and job modifications

### Testing and Validation
- [ ] Test job processing under load
- [ ] Verify retry and backoff behavior
- [ ] Test graceful shutdown scenarios
- [ ] Validate error handling and DLQ routing
- [ ] Test Redis failover scenarios

### Documentation
- [ ] Document queue naming conventions
- [ ] Document job schemas and data formats
- [ ] Create runbooks for common issues
- [ ] Document scaling procedures
- [ ] Maintain API documentation for queue operations
