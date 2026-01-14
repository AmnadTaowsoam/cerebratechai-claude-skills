# Event-Driven Architecture

## Overview

Comprehensive guide to event-driven microservices patterns for building scalable distributed systems.

## Table of Contents

1. [Event-Driven Concepts](#event-driven-concepts)
2. [Event Types](#event-types)
3. [Event Sourcing](#event-sourcing)
4. [CQRS Pattern](#cqrs-pattern)
5. [Saga Pattern](#saga-pattern)
6. [Event Schemas](#event-schemas)
7. [Idempotency](#idempotency)
8. [Event Versioning](#event-versioning)
9. [Dead Letter Handling](#dead-letter-handling)
10. [Eventual Consistency](#eventual-consistency)
11. [Testing Strategies](#testing-strategies)
12. [Best Practices](#best-practices)

---

## Event-Driven Concepts

### Core Concepts

```markdown
## Event-Driven Architecture Core Concepts

### What is Event-Driven Architecture?
- Services communicate via events
- Decoupled producers and consumers
- Asynchronous communication pattern

### Key Concepts
- **Event**: A fact that happened in the past
- **Event Bus**: Infrastructure for event distribution
- **Event Store**: Persistent storage for events
- **Event Handler**: Processes events
- **Event Stream**: Sequence of related events

### Benefits
- Loose coupling between services
- Scalability through async processing
- Better resilience
- Audit trail of all changes
- Real-time processing
```

### Event Architecture

```typescript
// event-types.ts
export interface DomainEvent {
  id: string;
  type: string;
  aggregateId: string;
  aggregateType: string;
  version: number;
  occurredAt: Date;
  data: any;
  metadata?: Record<string, any>;
}

export interface IntegrationEvent {
  id: string;
  type: string;
  source: string;
  timestamp: Date;
  data: any;
  correlationId?: string;
  causationId?: string;
}

export enum EventType {
  // User events
  USER_CREATED = 'user.created',
  USER_UPDATED = 'user.updated',
  USER_DELETED = 'user.deleted',
  
  // Order events
  ORDER_CREATED = 'order.created',
  ORDER_UPDATED = 'order.updated',
  ORDER_CANCELLED = 'order.cancelled',
  ORDER_COMPLETED = 'order.completed',
  
  // Payment events
  PAYMENT_INITIATED = 'payment.initiated',
  PAYMENT_COMPLETED = 'payment.completed',
  PAYMENT_FAILED = 'payment.failed',
  PAYMENT_REFUNDED = 'payment.refunded'
}
```

---

## Event Types

### Domain Events

```typescript
// domain-events.ts
export class UserCreatedEvent implements DomainEvent {
  id: string;
  type = EventType.USER_CREATED;
  aggregateId: string;
  aggregateType = 'User';
  version: number;
  occurredAt: Date;
  data: any;
  metadata?: Record<string, any>;
  
  constructor(userId: string, email: string, metadata?: Record<string, any>) {
    this.id = generateUUID();
    this.aggregateId = userId;
    this.version = 1;
    this.occurredAt = new Date();
    this.data = {
      userId,
      email
    };
    this.metadata = metadata;
  }
}

export class OrderCreatedEvent implements DomainEvent {
  id: string;
  type = EventType.ORDER_CREATED;
  aggregateId: string;
  aggregateType = 'Order';
  version: number;
  occurredAt: Date;
  data: any;
  metadata?: Record<string, any>;
  
  constructor(
    orderId: string,
    userId: string,
    items: any[],
    total: number,
    metadata?: Record<string, any>
  ) {
    this.id = generateUUID();
    this.aggregateId = orderId;
    this.version = 1;
    this.occurredAt = new Date();
    this.data = {
      orderId,
      userId,
      items,
      total
    };
    this.metadata = metadata;
  }
}

function generateUUID(): string {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}
```

### Integration Events

```typescript
// integration-events.ts
export class OrderCreatedIntegrationEvent implements IntegrationEvent {
  id: string;
  type = 'order.created.v1';
  source = 'order-service';
  timestamp: Date;
  data: any;
  correlationId?: string;
  causationId?: string;
  
  constructor(
    orderId: string,
    userId: string,
    items: any[],
    total: number,
    correlationId?: string
  ) {
    this.id = generateUUID();
    this.timestamp = new Date();
    this.correlationId = correlationId;
    this.data = {
      orderId,
      userId,
      items,
      total,
      currency: 'USD'
    };
  }
}

export class PaymentCompletedIntegrationEvent implements IntegrationEvent {
  id: string;
  type = 'payment.completed.v1';
  source = 'payment-service';
  timestamp: Date;
  data: any;
  correlationId?: string;
  causationId?: string;
  
  constructor(
    paymentId: string,
    orderId: string,
    amount: number,
    correlationId?: string
  ) {
    this.id = generateUUID();
    this.timestamp = new Date();
    this.correlationId = correlationId;
    this.data = {
      paymentId,
      orderId,
      amount,
      currency: 'USD',
      status: 'completed'
    };
  }
}
```

---

## Event Sourcing

### Event Store

```typescript
// event-store.ts
export interface EventStore {
  saveEvents(aggregateId: string, events: DomainEvent[]): Promise<void>;
  getEvents(aggregateId: string): Promise<DomainEvent[]>;
  getEventsFromVersion(aggregateId: string, version: number): Promise<DomainEvent[]>;
  getAllEvents(): Promise<DomainEvent[]>;
}

export class InMemoryEventStore implements EventStore {
  private events: Map<string, DomainEvent[]> = new Map();
  
  async saveEvents(aggregateId: string, events: DomainEvent[]): Promise<void> {
    if (!this.events.has(aggregateId)) {
      this.events.set(aggregateId, []);
    }
    
    const existingEvents = this.events.get(aggregateId)!;
    existingEvents.push(...events);
  }
  
  async getEvents(aggregateId: string): Promise<DomainEvent[]> {
    return this.events.get(aggregateId) || [];
  }
  
  async getEventsFromVersion(aggregateId: string, version: number): Promise<DomainEvent[]> {
    const events = this.events.get(aggregateId) || [];
    return events.filter(e => e.version >= version);
  }
  
  async getAllEvents(): Promise<DomainEvent[]> {
    const allEvents: DomainEvent[] = [];
    for (const events of this.events.values()) {
      allEvents.push(...events);
    }
    return allEvents.sort((a, b) => a.occurredAt.getTime() - b.occurredAt.getTime());
  }
}

export class PostgresEventStore implements EventStore {
  constructor(private pool: any) {}
  
  async saveEvents(aggregateId: string, events: DomainEvent[]): Promise<void> {
    const client = await this.pool.connect();
    
    try {
      await client.query('BEGIN');
      
      for (const event of events) {
        await client.query(
          'INSERT INTO events (id, type, aggregate_id, aggregate_type, version, occurred_at, data, metadata) VALUES ($1, $2, $3, $4, $5, $6, $7, $8)',
          [
            event.id,
            event.type,
            event.aggregateId,
            event.aggregateType,
            event.version,
            event.occurredAt,
            JSON.stringify(event.data),
            JSON.stringify(event.metadata || {})
          ]
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
  
  async getEvents(aggregateId: string): Promise<DomainEvent[]> {
    const result = await this.pool.query(
      'SELECT * FROM events WHERE aggregate_id = $1 ORDER BY version ASC',
      [aggregateId]
    );
    
    return result.rows.map((row: any) => ({
      id: row.id,
      type: row.type,
      aggregateId: row.aggregate_id,
      aggregateType: row.aggregate_type,
      version: row.version,
      occurredAt: row.occurred_at,
      data: JSON.parse(row.data),
      metadata: JSON.parse(row.metadata)
    }));
  }
  
  async getEventsFromVersion(aggregateId: string, version: number): Promise<DomainEvent[]> {
    const result = await this.pool.query(
      'SELECT * FROM events WHERE aggregate_id = $1 AND version >= $2 ORDER BY version ASC',
      [aggregateId, version]
    );
    
    return result.rows.map((row: any) => ({
      id: row.id,
      type: row.type,
      aggregateId: row.aggregate_id,
      aggregateType: row.aggregate_type,
      version: row.version,
      occurredAt: row.occurred_at,
      data: JSON.parse(row.data),
      metadata: JSON.parse(row.metadata)
    }));
  }
  
  async getAllEvents(): Promise<DomainEvent[]> {
    const result = await this.pool.query(
      'SELECT * FROM events ORDER BY occurred_at ASC'
    );
    
    return result.rows.map((row: any) => ({
      id: row.id,
      type: row.type,
      aggregateId: row.aggregate_id,
      aggregateType: row.aggregate_type,
      version: row.version,
      occurredAt: row.occurred_at,
      data: JSON.parse(row.data),
      metadata: JSON.parse(row.metadata)
    }));
  }
}
```

### Aggregate Rebuilding

```typescript
// aggregate-rebuilder.ts
export class AggregateRebuilder {
  constructor(private eventStore: EventStore) {}
  
  async rebuildAggregate<T>(
    aggregateId: string,
    aggregateType: string,
    initialState: T
  ): Promise<T> {
    const events = await this.eventStore.getEvents(aggregateId);
    let state = initialState;
    
    for (const event of events) {
      state = this.applyEvent(state, event);
    }
    
    return state;
  }
  
  private applyEvent<T>(state: T, event: DomainEvent): T {
    switch (event.type) {
      case EventType.USER_CREATED:
        return this.handleUserCreated(state, event);
      case EventType.USER_UPDATED:
        return this.handleUserUpdated(state, event);
      case EventType.ORDER_CREATED:
        return this.handleOrderCreated(state, event);
      default:
        return state;
    }
  }
  
  private handleUserCreated<T>(state: T, event: DomainEvent): T {
    return {
      ...state,
      ...event.data,
      version: event.version
    };
  }
  
  private handleUserUpdated<T>(state: T, event: DomainEvent): T {
    return {
      ...state,
      ...event.data,
      version: event.version
    };
  }
  
  private handleOrderCreated<T>(state: T, event: DomainEvent): T {
    return {
      ...state,
      ...event.data,
      version: event.version
    };
  }
}
```

---

## CQRS Pattern

### Command Query Separation

```typescript
// cqrs-pattern.ts
export interface Command {
  type: string;
  aggregateId: string;
  data: any;
}

export interface Query {
  type: string;
  params: any;
}

export class CQRSService {
  constructor(
    private eventStore: EventStore,
    private commandHandlers: Map<string, Function>,
    private queryHandlers: Map<string, Function>
  ) {}
  
  async executeCommand(command: Command): Promise<void> {
    const handler = this.commandHandlers.get(command.type);
    
    if (!handler) {
      throw new Error(`No handler for command: ${command.type}`);
    }
    
    // Execute command
    const events = await handler(command);
    
    // Save events
    await this.eventStore.saveEvents(command.aggregateId, events);
    
    // Publish events
    for (const event of events) {
      await this.publishEvent(event);
    }
  }
  
  async executeQuery<T>(query: Query): Promise<T> {
    const handler = this.queryHandlers.get(query.type);
    
    if (!handler) {
      throw new Error(`No handler for query: ${query.type}`);
    }
    
    return handler(query.params);
  }
  
  private async publishEvent(event: DomainEvent): Promise<void> {
    // Publish to event bus
    // Implementation depends on event bus (Kafka, RabbitMQ, etc.)
  }
}

// Example command handler
export class UserCommandHandler {
  constructor(private eventStore: EventStore) {}
  
  async handleCreateUser(command: Command): Promise<DomainEvent[]> {
    const { userId, email, password } = command.data;
    
    // Validate
    if (!email || !password) {
      throw new Error('Email and password are required');
    }
    
    // Create event
    const event = new UserCreatedEvent(userId, email);
    
    return [event];
  }
  
  async handleUpdateEmail(command: Command): Promise<DomainEvent[]> {
    const { userId, newEmail } = command.data;
    
    // Get current state
    const events = await this.eventStore.getEvents(userId);
    const user = events[events.length - 1].data;
    
    // Validate
    if (!this.isValidEmail(newEmail)) {
      throw new Error('Invalid email format');
    }
    
    // Create event
    const event = new UserUpdatedEvent(userId, { email: newEmail });
    
    return [event];
  }
  
  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}

// Example query handler
export class UserQueryHandler {
  constructor(private readModel: any) {}
  
  async handleGetUser(params: { userId: string }): Promise<any> {
    return this.readModel.getUserById(params.userId);
  }
  
  async handleListUsers(params: { page: number; limit: number }): Promise<any[]> {
    return this.readModel.listUsers(params.page, params.limit);
  }
  
  async handleSearchUsers(params: { query: string }): Promise<any[]> {
    return this.readModel.searchUsers(params.query);
  }
}
```

---

## Saga Pattern

### Orchestration-Based Saga

```typescript
// saga-orchestrator.ts
export interface SagaStep {
  name: string;
  execute: () => Promise<any>;
  compensate: (result: any) => Promise<void>;
}

export class SagaOrchestrator {
  private steps: SagaStep[] = [];
  private completedSteps: Map<string, any> = new Map();
  private compensating = false;
  
  addStep(step: SagaStep): void {
    this.steps.push(step);
  }
  
  async execute(): Promise<void> {
    try {
      // Execute all steps
      for (const step of this.steps) {
        if (this.compensating) break;
        
        console.log(`Executing step: ${step.name}`);
        const result = await step.execute();
        this.completedSteps.set(step.name, result);
      }
      
      console.log('Saga completed successfully');
    } catch (error) {
      console.error('Saga failed, starting compensation:', error);
      await this.compensate();
      throw error;
    }
  }
  
  private async compensate(): Promise<void> {
    this.compensating = true;
    
    // Compensate in reverse order
    for (let i = this.steps.length - 1; i >= 0; i--) {
      const step = this.steps[i];
      const result = this.completedSteps.get(step.name);
      
      if (result) {
        console.log(`Compensating step: ${step.name}`);
        try {
          await step.compensate(result);
        } catch (error) {
          console.error(`Failed to compensate ${step.name}:`, error);
          // Continue compensating other steps
        }
      }
    }
    
    this.compensating = false;
  }
}

// Example: Order Saga
export class OrderSaga {
  private orchestrator: SagaOrchestrator;
  
  constructor(
    private orderService: any,
    private paymentService: any,
    private inventoryService: any,
    private notificationService: any
  ) {
    this.orchestrator = new SagaOrchestrator();
    this.setupSteps();
  }
  
  private setupSteps(): void {
    // Step 1: Create order
    this.orchestrator.addStep({
      name: 'create-order',
      execute: async () => {
        return await this.orderService.createOrder(this.orderData);
      },
      compensate: async (result) => {
        await this.orderService.cancelOrder(result.orderId);
      }
    });
    
    // Step 2: Process payment
    this.orchestrator.addStep({
      name: 'process-payment',
      execute: async () => {
        const order = this.orchestrator['completedSteps'].get('create-order');
        return await this.paymentService.processPayment(order);
      },
      compensate: async (result) => {
        await this.paymentService.refundPayment(result.paymentId);
      }
    });
    
    // Step 3: Reserve inventory
    this.orchestrator.addStep({
      name: 'reserve-inventory',
      execute: async () => {
        const order = this.orchestrator['completedSteps'].get('create-order');
        return await this.inventoryService.reserveItems(order.items);
      },
      compensate: async (result) => {
        await this.inventoryService.releaseItems(result.reservationId);
      }
    });
    
    // Step 4: Send confirmation
    this.orchestrator.addStep({
      name: 'send-confirmation',
      execute: async () => {
        const order = this.orchestrator['completedSteps'].get('create-order');
        return await this.notificationService.sendOrderConfirmation(order);
      },
      compensate: async () => {
        // No compensation needed for notification
      }
    });
  }
  
  async execute(orderData: any): Promise<void> {
    this.orderData = orderData;
    await this.orchestrator.execute();
  }
}
```

### Choreography-Based Saga

```typescript
// saga-choreographer.ts
export class SagaChoreographer {
  private eventHandlers: Map<string, Function> = new Map();
  private sagaState: Map<string, any> = new Map();
  
  registerHandler(eventType: string, handler: Function): void {
    this.eventHandlers.set(eventType, handler);
  }
  
  async handleEvent(event: IntegrationEvent): Promise<void> {
    const handler = this.eventHandlers.get(event.type);
    
    if (!handler) {
      return;
    }
    
    try {
      await handler(event);
    } catch (error) {
      console.error(`Error handling event ${event.type}:`, error);
      await this.handleSagaFailure(event, error as Error);
    }
  }
  
  private async handleSagaFailure(event: IntegrationEvent, error: Error): Promise<void> {
    // Determine which saga failed
    const sagaId = event.correlationId;
    const state = this.sagaState.get(sagaId);
    
    if (!state) {
      return;
    }
    
    // Compensate completed steps
    for (const step of state.completedSteps.reverse()) {
      try {
        await this.compensateStep(step);
      } catch (compensateError) {
        console.error(`Failed to compensate ${step.name}:`, compensateError);
      }
    }
  }
  
  private async compensateStep(step: any): Promise<void> {
    // Implement step-specific compensation
  }
}

// Example: Order Choreography
export class OrderChoreography extends SagaChoreographer {
  constructor(
    private orderService: any,
    private paymentService: any,
    private inventoryService: any
  ) {
    super();
    this.setupHandlers();
  }
  
  private setupHandlers(): void {
    // Order created
    this.registerHandler('order.created.v1', async (event) => {
      const { orderId, userId, total } = event.data;
      
      // Initiate payment
      await this.paymentService.initiatePayment({
        orderId,
        userId,
        amount: total
      });
    });
    
    // Payment completed
    this.registerHandler('payment.completed.v1', async (event) => {
      const { orderId, items } = event.data;
      
      // Reserve inventory
      await this.inventoryService.reserveItems({
        orderId,
        items
      });
    });
    
    // Payment failed
    this.registerHandler('payment.failed.v1', async (event) => {
      const { orderId } = event.data;
      
      // Cancel order
      await this.orderService.cancelOrder(orderId);
    });
  }
}
```

---

## Event Schemas

### Schema Definition

```typescript
// event-schemas.ts
import { z } from 'zod';

export const UserCreatedSchema = z.object({
  userId: z.string().uuid(),
  email: z.string().email(),
  createdAt: z.date()
});

export const OrderCreatedSchema = z.object({
  orderId: z.string().uuid(),
  userId: z.string().uuid(),
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number().int().positive(),
    price: z.number().positive()
  })),
  total: z.number().positive(),
  currency: z.enum(['USD', 'EUR', 'GBP']),
  createdAt: z.date()
});

export const PaymentCompletedSchema = z.object({
  paymentId: z.string().uuid(),
  orderId: z.string().uuid(),
  amount: z.number().positive(),
  currency: z.enum(['USD', 'EUR', 'GBP']),
  status: z.enum(['completed', 'pending', 'failed']),
  completedAt: z.date()
});

export class EventValidator {
  static validateEvent(event: DomainEvent): boolean {
    switch (event.type) {
      case EventType.USER_CREATED:
        return UserCreatedSchema.safeParse(event.data).success;
      case EventType.ORDER_CREATED:
        return OrderCreatedSchema.safeParse(event.data).success;
      case EventType.PAYMENT_COMPLETED:
        return PaymentCompletedSchema.safeParse(event.data).success;
      default:
        return false;
    }
  }
  
  static validateIntegrationEvent(event: IntegrationEvent): boolean {
    switch (event.type) {
      case 'order.created.v1':
        return OrderCreatedSchema.safeParse(event.data).success;
      case 'payment.completed.v1':
        return PaymentCompletedSchema.safeParse(event.data).success;
      default:
        return false;
    }
  }
}
```

---

## Idempotency

### Idempotent Event Processing

```typescript
// idempotency.ts
export interface IdempotencyStore {
  hasProcessed(eventId: string): Promise<boolean>;
  markProcessed(eventId: string, result: any): Promise<void>;
  getProcessedResult(eventId: string): Promise<any>;
}

export class RedisIdempotencyStore implements IdempotencyStore {
  constructor(private redis: any) {}
  
  async hasProcessed(eventId: string): Promise<boolean> {
    const key = `processed:${eventId}`;
    return await this.redis.exists(key) === 1;
  }
  
  async markProcessed(eventId: string, result: any): Promise<void> {
    const key = `processed:${eventId}`;
    await this.redis.setex(key, 86400, JSON.stringify(result)); // 24 hours TTL
  }
  
  async getProcessedResult(eventId: string): Promise<any> {
    const key = `processed:${eventId}`;
    const result = await this.redis.get(key);
    return result ? JSON.parse(result) : null;
  }
}

export class IdempotentEventHandler {
  constructor(
    private idempotencyStore: IdempotencyStore,
    private handler: (event: DomainEvent) => Promise<any>
  ) {}
  
  async handle(event: DomainEvent): Promise<any> {
    // Check if already processed
    if (await this.idempotencyStore.hasProcessed(event.id)) {
      console.log(`Event ${event.id} already processed, returning cached result`);
      return await this.idempotencyStore.getProcessedResult(event.id);
    }
    
    // Process event
    const result = await this.handler(event);
    
    // Mark as processed
    await this.idempotencyStore.markProcessed(event.id, result);
    
    return result;
  }
}

// Usage
const idempotentHandler = new IdempotentEventHandler(
  new RedisIdempotencyStore(redis),
  async (event) => {
    // Handle event
    console.log('Processing event:', event.type);
    return { processed: true };
  }
);

await idempotentHandler.handle(userCreatedEvent);
```

---

## Event Versioning

### Version Handling

```typescript
// event-versioning.ts
export interface EventVersionHandler {
  handle(event: IntegrationEvent): Promise<void>;
}

export class EventVersionRouter {
  private versionHandlers: Map<string, Map<string, EventVersionHandler>> = new Map();
  
  registerHandler(eventType: string, version: string, handler: EventVersionHandler): void {
    if (!this.versionHandlers.has(eventType)) {
      this.versionHandlers.set(eventType, new Map());
    }
    this.versionHandlers.get(eventType)!.set(version, handler);
  }
  
  async handle(event: IntegrationEvent): Promise<void> {
    const [eventType, version] = event.type.split('.v');
    const handlers = this.versionHandlers.get(eventType);
    
    if (!handlers) {
      console.warn(`No handlers registered for event type: ${eventType}`);
      return;
    }
    
    const handler = handlers.get(version);
    
    if (!handler) {
      console.warn(`No handler for version: ${version}`);
      // Try to use latest version handler
      const latestVersion = this.getLatestVersion(handlers);
      const latestHandler = handlers.get(latestVersion);
      
      if (latestHandler) {
        console.log(`Using latest version ${latestVersion} for event ${event.type}`);
        await this.transformAndHandle(event, latestVersion, latestHandler);
      }
      return;
    }
    
    await handler.handle(event);
  }
  
  private async transformAndHandle(
    event: IntegrationEvent,
    targetVersion: string,
    handler: EventVersionHandler
  ): Promise<void> {
    // Transform event data to target version
    const transformedEvent = this.transformEvent(event, targetVersion);
    await handler.handle(transformedEvent);
  }
  
  private transformEvent(event: IntegrationEvent, targetVersion: string): IntegrationEvent {
    // Implement event transformation logic
    return event;
  }
  
  private getLatestVersion(handlers: Map<string, EventVersionHandler>): string {
    const versions = Array.from(handlers.keys()).map(v => parseInt(v));
    return Math.max(...versions).toString();
  }
}

// Example version handlers
export class OrderCreatedV1Handler implements EventVersionHandler {
  async handle(event: IntegrationEvent): Promise<void> {
    console.log('Handling order.created.v1:', event.data);
    // V1 specific logic
  }
}

export class OrderCreatedV2Handler implements EventVersionHandler {
  async handle(event: IntegrationEvent): Promise<void> {
    console.log('Handling order.created.v2:', event.data);
    // V2 specific logic with additional fields
  }
}
```

---

## Dead Letter Handling

### Dead Letter Queue

```typescript
// dead-letter-handler.ts
export class DeadLetterHandler {
  constructor(
    private dlqPublisher: any,
    private maxRetries: number = 3
  ) {}
  
  async handleFailedEvent(
    event: DomainEvent,
    error: Error,
    retryCount: number = 0
  ): Promise<void> {
    if (retryCount < this.maxRetries) {
      // Retry the event
      console.log(`Retrying event ${event.id}, attempt ${retryCount + 1}`);
      await this.retryEvent(event, retryCount + 1);
    } else {
      // Send to dead letter queue
      console.log(`Max retries reached, sending event ${event.id} to DLQ`);
      await this.sendToDLQ(event, error);
    }
  }
  
  private async retryEvent(event: DomainEvent, retryCount: number): Promise<void> {
    // Add retry metadata
    const retryEvent = {
      ...event,
      metadata: {
        ...event.metadata,
        retryCount,
        lastError: 'Will be set on failure'
      }
    };
    
    // Republish event
    await this.dlqPublisher.publish(retryEvent);
  }
  
  private async sendToDLQ(event: DomainEvent, error: Error): Promise<void> {
    const dlqEvent = {
      originalEvent: event,
      error: {
        message: error.message,
        stack: error.stack,
        timestamp: new Date().toISOString()
      },
      failedAt: new Date().toISOString()
    };
    
    await this.dlqPublisher.publish('dead-letter-queue', dlqEvent);
  }
}
```

---

## Eventual Consistency

### Consistency Monitoring

```typescript
// consistency-monitor.ts
export class ConsistencyMonitor {
  private consistencyChecks: Map<string, Function> = new Map();
  
  registerCheck(name: string, check: Function): void {
    this.consistencyChecks.set(name, check);
  }
  
  async runChecks(): Promise<Map<string, boolean>> {
    const results = new Map<string, boolean>();
    
    for (const [name, check] of this.consistencyChecks) {
      try {
        const result = await check();
        results.set(name, result);
        
        if (!result) {
          console.warn(`Consistency check failed: ${name}`);
          await this.handleInconsistency(name);
        }
      } catch (error) {
        console.error(`Error running check ${name}:`, error);
        results.set(name, false);
      }
    }
    
    return results;
  }
  
  private async handleInconsistency(checkName: string): Promise<void> {
    // Handle inconsistency (alert, repair, etc.)
    console.log(`Handling inconsistency for: ${checkName}`);
  }
}

// Example consistency checks
export class OrderConsistencyChecks {
  constructor(
    private orderService: any,
    private paymentService: any,
    private inventoryService: any
  ) {}
  
  async checkOrderPaymentConsistency(orderId: string): Promise<boolean> {
    const order = await this.orderService.getOrder(orderId);
    const payment = await this.paymentService.getPaymentByOrderId(orderId);
    
    if (order.status === 'paid' && !payment) {
      return false;
    }
    
    if (order.status === 'paid' && payment.status !== 'completed') {
      return false;
    }
    
    return true;
  }
  
  async checkOrderInventoryConsistency(orderId: string): Promise<boolean> {
    const order = await this.orderService.getOrder(orderId);
    const reservation = await this.inventoryService.getReservation(orderId);
    
    if (order.status === 'confirmed' && !reservation) {
      return false;
    }
    
    return true;
  }
}
```

---

## Testing Strategies

### Event Testing

```typescript
// event-testing.ts
import { describe, it, expect, beforeEach } from '@jest/globals';

describe('Event-Driven Architecture', () => {
  let eventStore: EventStore;
  let saga: OrderSaga;
  
  beforeEach(() => {
    eventStore = new InMemoryEventStore();
    saga = new OrderSaga(
      mockOrderService,
      mockPaymentService,
      mockInventoryService,
      mockNotificationService
    );
  });
  
  describe('Event Sourcing', () => {
    it('should save and retrieve events', async () => {
      const event = new UserCreatedEvent('user-1', 'test@example.com');
      
      await eventStore.saveEvents('user-1', [event]);
      const events = await eventStore.getEvents('user-1');
      
      expect(events).toHaveLength(1);
      expect(events[0]).toEqual(event);
    });
    
    it('should rebuild aggregate from events', async () => {
      const events = [
        new UserCreatedEvent('user-1', 'test@example.com'),
        new UserUpdatedEvent('user-1', { email: 'updated@example.com' })
      ];
      
      await eventStore.saveEvents('user-1', events);
      
      const rebuilder = new AggregateRebuilder(eventStore);
      const user = await rebuilder.rebuildAggregate('user-1', 'User', {});
      
      expect(user.email).toBe('updated@example.com');
    });
  });
  
  describe('Saga Pattern', () => {
    it('should execute all steps successfully', async () => {
      const orderData = {
        userId: 'user-1',
        items: [{ productId: 'product-1', quantity: 2, price: 10 }],
        total: 20
      };
      
      await saga.execute(orderData);
      
      expect(mockOrderService.createOrder).toHaveBeenCalled();
      expect(mockPaymentService.processPayment).toHaveBeenCalled();
      expect(mockInventoryService.reserveItems).toHaveBeenCalled();
      expect(mockNotificationService.sendOrderConfirmation).toHaveBeenCalled();
    });
    
    it('should compensate on failure', async () => {
      mockPaymentService.processPayment.mockRejectedValue(new Error('Payment failed'));
      
      const orderData = {
        userId: 'user-1',
        items: [{ productId: 'product-1', quantity: 2, price: 10 }],
        total: 20
      };
      
      await expect(saga.execute(orderData)).rejects.toThrow();
      
      expect(mockOrderService.cancelOrder).toHaveBeenCalled();
      expect(mockPaymentService.refundPayment).not.toHaveBeenCalled();
    });
  });
});
```

---

## Best Practices

### Event-Driven Checklist

```markdown
## Event-Driven Architecture Best Practices

### Event Design
- [ ] Use immutable events
- [ ] Include event metadata (timestamp, correlation ID)
- [ ] Version events explicitly
- [ ] Keep events small and focused
- [ ] Use descriptive event names

### Event Sourcing
- [ ] Store all events immutably
- [ ] Use event versioning
- [ ] Implement snapshot strategy
- [ ] Validate event schemas
- [ ] Handle event replay

### CQRS
- [ ] Separate command and query models
- [ ] Keep read models eventually consistent
- [ ] Optimize read models for queries
- [ ] Use materialized views
- [ ] Implement read model rebuild

### Saga Pattern
- [ ] Define compensation actions
- [ ] Handle saga timeout
- [ ] Log saga state changes
- [ ] Implement saga monitoring
- [ ] Test compensation logic

### Idempotency
- [ ] Make event handlers idempotent
- [ ] Use unique event IDs
- [ ] Track processed events
- [ ] Handle duplicate events gracefully
- [ ] Implement idempotency store

### Monitoring
- [ ] Track event processing latency
- [ ] Monitor event backlog
- [ ] Alert on processing failures
- [ ] Track saga execution
- [ ] Monitor consistency checks
```

---

## Additional Resources

- [Event Sourcing Pattern](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)
- [Saga Pattern](https://microservices.io/patterns/data/saga.html)
- [Apache Kafka](https://kafka.apache.org/documentation/)
- [RabbitMQ](https://www.rabbitmq.com/getting-started.html)
