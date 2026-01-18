# Event-Driven Testing

## Overview

Testing strategies and patterns for event-driven architectures, including event flow testing, saga testing, message queue testing, event replay, and integration testing with asynchronous messaging systems.

---

## 1. Event-Driven Testing Architecture

### Testing Pyramid for Event-Driven Systems

```markdown
# Event-Driven Testing Pyramid

## Test Levels

### Unit Tests (60-70%)
- Event handlers
- Event publishers
- Business logic
- Data transformations

### Integration Tests (20-30%)
- Event flow between services
- Message queue integration
- Database transactions
- External API calls

### End-to-End Tests (5-10%)
- Complete user journeys
- Multi-service workflows
- Saga orchestration
- System behavior

## Test Types

### Functional Tests
- Event processing correctness
- State transitions
- Data validation
- Business rules

### Non-Functional Tests
- Performance (throughput, latency)
- Reliability (retries, DLQ)
- Scalability (load testing)
- Resilience (failure scenarios)
```

---

## 2. Event Handler Testing

### Unit Testing Event Handlers

```typescript
// Event Handler
interface OrderCreatedEvent {
  orderId: string
  userId: string
  items: Array<{ productId: string; quantity: number; price: number }>
  totalAmount: number
  createdAt: Date
}

class OrderEventHandler {
  constructor(
    private orderRepository: OrderRepository,
    private notificationService: NotificationService,
    private eventPublisher: EventPublisher
  ) {}

  async handleOrderCreated(event: OrderCreatedEvent): Promise<void> {
    // Save order to database
    await this.orderRepository.create({
      id: event.orderId,
      userId: event.userId,
      items: event.items,
      totalAmount: event.totalAmount,
      status: 'pending',
      createdAt: event.createdAt,
    })

    // Send notification
    await this.notificationService.sendOrderConfirmation(
      event.userId,
      event.orderId
    )

    // Publish follow-up event
    await this.eventPublisher.publish('order.confirmed', {
      orderId: event.orderId,
      userId: event.userId,
    })
  }
}

// Unit Tests
import { describe, it, expect, vi, beforeEach } from 'vitest'

describe('OrderEventHandler', () => {
  let handler: OrderEventHandler
  let mockOrderRepository: any
  let mockNotificationService: any
  let mockEventPublisher: any

  beforeEach(() => {
    mockOrderRepository = {
      create: vi.fn(),
    }

    mockNotificationService = {
      sendOrderConfirmation: vi.fn(),
    }

    mockEventPublisher = {
      publish: vi.fn(),
    }

    handler = new OrderEventHandler(
      mockOrderRepository,
      mockNotificationService,
      mockEventPublisher
    )
  })

  it('should save order to database', async () => {
    const event: OrderCreatedEvent = {
      orderId: 'ORDER-001',
      userId: 'USER-001',
      items: [{ productId: 'PROD-001', quantity: 2, price: 100 }],
      totalAmount: 200,
      createdAt: new Date(),
    }

    await handler.handleOrderCreated(event)

    expect(mockOrderRepository.create).toHaveBeenCalledWith({
      id: event.orderId,
      userId: event.userId,
      items: event.items,
      totalAmount: event.totalAmount,
      status: 'pending',
      createdAt: event.createdAt,
    })
  })

  it('should send notification', async () => {
    const event: OrderCreatedEvent = {
      orderId: 'ORDER-001',
      userId: 'USER-001',
      items: [],
      totalAmount: 200,
      createdAt: new Date(),
    }

    await handler.handleOrderCreated(event)

    expect(mockNotificationService.sendOrderConfirmation).toHaveBeenCalledWith(
      'USER-001',
      'ORDER-001'
    )
  })

  it('should publish follow-up event', async () => {
    const event: OrderCreatedEvent = {
      orderId: 'ORDER-001',
      userId: 'USER-001',
      items: [],
      totalAmount: 200,
      createdAt: new Date(),
    }

    await handler.handleOrderCreated(event)

    expect(mockEventPublisher.publish).toHaveBeenCalledWith('order.confirmed', {
      orderId: 'ORDER-001',
      userId: 'USER-001',
    })
  })

  it('should handle errors gracefully', async () => {
    const event: OrderCreatedEvent = {
      orderId: 'ORDER-001',
      userId: 'USER-001',
      items: [],
      totalAmount: 200,
      createdAt: new Date(),
    }

    mockOrderRepository.create.mockRejectedValue(new Error('Database error'))

    await expect(handler.handleOrderCreated(event)).rejects.toThrow(
      'Database error'
    )
  })
})
```

---

## 3. Event Flow Testing

### Integration Testing Event Flows

```typescript
// Event Flow Test
import { describe, it, expect, beforeAll, afterAll } from 'vitest'
import { RabbitMQTestContainer } from './test-containers'
import { EventBus } from './event-bus'

describe('Order Event Flow', () => {
  let rabbitMQ: RabbitMQTestContainer
  let eventBus: EventBus

  beforeAll(async () => {
    // Start RabbitMQ test container
    rabbitMQ = await RabbitMQTestContainer.start()
    eventBus = new EventBus(rabbitMQ.getConnectionString())
    await eventBus.connect()
  })

  afterAll(async () => {
    await eventBus.disconnect()
    await rabbitMQ.stop()
  })

  it('should process complete order flow', async () => {
    const events: any[] = []

    // Subscribe to all events
    await eventBus.subscribe('order.*', (event) => {
      events.push(event)
    })

    // Publish initial event
    await eventBus.publish('order.created', {
      orderId: 'ORDER-001',
      userId: 'USER-001',
      totalAmount: 200,
    })

    // Wait for event processing
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Verify event flow
    expect(events).toHaveLength(3)
    expect(events[0].type).toBe('order.created')
    expect(events[1].type).toBe('order.confirmed')
    expect(events[2].type).toBe('payment.initiated')
  })

  it('should handle event ordering', async () => {
    const receivedEvents: string[] = []

    await eventBus.subscribe('order.created', () => {
      receivedEvents.push('created')
    })

    await eventBus.subscribe('order.confirmed', () => {
      receivedEvents.push('confirmed')
    })

    // Publish events
    await eventBus.publish('order.created', { orderId: 'ORDER-001' })
    await eventBus.publish('order.confirmed', { orderId: 'ORDER-001' })

    await new Promise((resolve) => setTimeout(resolve, 500))

    expect(receivedEvents).toEqual(['created', 'confirmed'])
  })
})
```

### Event Flow Assertions

```typescript
// Event Flow Assertion Helper
class EventFlowAssertion {
  private events: any[] = []
  private timeout: number

  constructor(timeout: number = 5000) {
    this.timeout = timeout
  }

  recordEvent(event: any): void {
    this.events.push({
      ...event,
      timestamp: Date.now(),
    })
  }

  async waitForEvent(
    eventType: string,
    predicate?: (event: any) => boolean
  ): Promise<any> {
    const startTime = Date.now()

    while (Date.now() - startTime < this.timeout) {
      const event = this.events.find(
        (e) => e.type === eventType && (!predicate || predicate(e))
      )

      if (event) {
        return event
      }

      await new Promise((resolve) => setTimeout(resolve, 100))
    }

    throw new Error(`Event ${eventType} not received within ${this.timeout}ms`)
  }

  async waitForEventSequence(eventTypes: string[]): Promise<void> {
    for (const eventType of eventTypes) {
      await this.waitForEvent(eventType)
    }
  }

  assertEventOrder(expectedOrder: string[]): void {
    const actualOrder = this.events.map((e) => e.type)
    expect(actualOrder).toEqual(expectedOrder)
  }

  assertEventCount(eventType: string, expectedCount: number): void {
    const count = this.events.filter((e) => e.type === eventType).length
    expect(count).toBe(expectedCount)
  }

  getEvents(): any[] {
    return this.events
  }

  reset(): void {
    this.events = []
  }
}

// Usage in tests
describe('Event Flow with Assertions', () => {
  let flowAssertion: EventFlowAssertion

  beforeEach(() => {
    flowAssertion = new EventFlowAssertion()
  })

  it('should process events in correct order', async () => {
    // Setup event recording
    eventBus.subscribe('*', (event) => {
      flowAssertion.recordEvent(event)
    })

    // Trigger workflow
    await eventBus.publish('order.created', { orderId: 'ORDER-001' })

    // Wait for event sequence
    await flowAssertion.waitForEventSequence([
      'order.created',
      'order.confirmed',
      'payment.initiated',
    ])

    // Assert order
    flowAssertion.assertEventOrder([
      'order.created',
      'order.confirmed',
      'payment.initiated',
    ])
  })
})
```

---

## 4. Saga Testing

### Saga Pattern Testing

```typescript
// Saga Implementation
class OrderSaga {
  constructor(
    private eventBus: EventBus,
    private orderService: OrderService,
    private paymentService: PaymentService,
    private inventoryService: InventoryService
  ) {}

  async execute(orderId: string): Promise<void> {
    try {
      // Step 1: Create order
      await this.orderService.createOrder(orderId)
      await this.eventBus.publish('saga.order.created', { orderId })

      // Step 2: Reserve inventory
      await this.inventoryService.reserveItems(orderId)
      await this.eventBus.publish('saga.inventory.reserved', { orderId })

      // Step 3: Process payment
      await this.paymentService.processPayment(orderId)
      await this.eventBus.publish('saga.payment.completed', { orderId })

      // Saga completed
      await this.eventBus.publish('saga.completed', { orderId })
    } catch (error) {
      // Compensate on failure
      await this.compensate(orderId)
      throw error
    }
  }

  private async compensate(orderId: string): Promise<void> {
    // Rollback in reverse order
    await this.paymentService.refundPayment(orderId)
    await this.inventoryService.releaseItems(orderId)
    await this.orderService.cancelOrder(orderId)
    await this.eventBus.publish('saga.compensated', { orderId })
  }
}

// Saga Tests
describe('OrderSaga', () => {
  let saga: OrderSaga
  let mockEventBus: any
  let mockOrderService: any
  let mockPaymentService: any
  let mockInventoryService: any

  beforeEach(() => {
    mockEventBus = { publish: vi.fn() }
    mockOrderService = {
      createOrder: vi.fn(),
      cancelOrder: vi.fn(),
    }
    mockPaymentService = {
      processPayment: vi.fn(),
      refundPayment: vi.fn(),
    }
    mockInventoryService = {
      reserveItems: vi.fn(),
      releaseItems: vi.fn(),
    }

    saga = new OrderSaga(
      mockEventBus,
      mockOrderService,
      mockPaymentService,
      mockInventoryService
    )
  })

  it('should complete saga successfully', async () => {
    await saga.execute('ORDER-001')

    expect(mockOrderService.createOrder).toHaveBeenCalledWith('ORDER-001')
    expect(mockInventoryService.reserveItems).toHaveBeenCalledWith('ORDER-001')
    expect(mockPaymentService.processPayment).toHaveBeenCalledWith('ORDER-001')
    expect(mockEventBus.publish).toHaveBeenCalledWith('saga.completed', {
      orderId: 'ORDER-001',
    })
  })

  it('should compensate on payment failure', async () => {
    mockPaymentService.processPayment.mockRejectedValue(
      new Error('Payment failed')
    )

    await expect(saga.execute('ORDER-001')).rejects.toThrow('Payment failed')

    // Verify compensation
    expect(mockPaymentService.refundPayment).toHaveBeenCalledWith('ORDER-001')
    expect(mockInventoryService.releaseItems).toHaveBeenCalledWith('ORDER-001')
    expect(mockOrderService.cancelOrder).toHaveBeenCalledWith('ORDER-001')
    expect(mockEventBus.publish).toHaveBeenCalledWith('saga.compensated', {
      orderId: 'ORDER-001',
    })
  })

  it('should publish events at each step', async () => {
    await saga.execute('ORDER-001')

    expect(mockEventBus.publish).toHaveBeenCalledWith('saga.order.created', {
      orderId: 'ORDER-001',
    })
    expect(mockEventBus.publish).toHaveBeenCalledWith(
      'saga.inventory.reserved',
      { orderId: 'ORDER-001' }
    )
    expect(mockEventBus.publish).toHaveBeenCalledWith(
      'saga.payment.completed',
      { orderId: 'ORDER-001' }
    )
  })
})
```

---

## 5. Message Queue Testing

### RabbitMQ Testing

```typescript
// RabbitMQ Test Helper
import amqp from 'amqplib'

class RabbitMQTestHelper {
  private connection: amqp.Connection | null = null
  private channel: amqp.Channel | null = null

  async connect(url: string): Promise<void> {
    this.connection = await amqp.connect(url)
    this.channel = await this.connection.createChannel()
  }

  async disconnect(): Promise<void> {
    await this.channel?.close()
    await this.connection?.close()
  }

  async purgeQueue(queueName: string): Promise<void> {
    if (!this.channel) throw new Error('Not connected')
    await this.channel.purgeQueue(queueName)
  }

  async getQueueMessageCount(queueName: string): Promise<number> {
    if (!this.channel) throw new Error('Not connected')
    const queue = await this.channel.checkQueue(queueName)
    return queue.messageCount
  }

  async publishMessage(
    exchange: string,
    routingKey: string,
    message: any
  ): Promise<void> {
    if (!this.channel) throw new Error('Not connected')

    this.channel.publish(
      exchange,
      routingKey,
      Buffer.from(JSON.stringify(message)),
      { persistent: true }
    )
  }

  async consumeMessages(
    queueName: string,
    count: number,
    timeout: number = 5000
  ): Promise<any[]> {
    if (!this.channel) throw new Error('Not connected')

    const messages: any[] = []

    return new Promise((resolve, reject) => {
      const timeoutId = setTimeout(() => {
        reject(new Error(`Timeout waiting for ${count} messages`))
      }, timeout)

      this.channel!.consume(queueName, (msg) => {
        if (msg) {
          messages.push(JSON.parse(msg.content.toString()))
          this.channel!.ack(msg)

          if (messages.length >= count) {
            clearTimeout(timeoutId)
            resolve(messages)
          }
        }
      })
    })
  }
}

// Usage in tests
describe('RabbitMQ Integration', () => {
  let rabbitMQ: RabbitMQTestHelper

  beforeAll(async () => {
    rabbitMQ = new RabbitMQTestHelper()
    await rabbitMQ.connect('amqp://localhost')
  })

  afterAll(async () => {
    await rabbitMQ.disconnect()
  })

  beforeEach(async () => {
    await rabbitMQ.purgeQueue('test-queue')
  })

  it('should publish and consume messages', async () => {
    const message = { orderId: 'ORDER-001', amount: 100 }

    await rabbitMQ.publishMessage('test-exchange', 'test-key', message)

    const messages = await rabbitMQ.consumeMessages('test-queue', 1)

    expect(messages).toHaveLength(1)
    expect(messages[0]).toEqual(message)
  })

  it('should handle message ordering', async () => {
    const messages = [
      { id: 1, data: 'first' },
      { id: 2, data: 'second' },
      { id: 3, data: 'third' },
    ]

    for (const msg of messages) {
      await rabbitMQ.publishMessage('test-exchange', 'test-key', msg)
    }

    const received = await rabbitMQ.consumeMessages('test-queue', 3)

    expect(received).toEqual(messages)
  })
})
```

---

## 6. Event Replay Testing

### Event Replay Implementation

```typescript
// Event Store for Replay
interface StoredEvent {
  id: string
  type: string
  data: any
  timestamp: Date
  metadata?: any
}

class EventStore {
  private events: StoredEvent[] = []

  async store(event: StoredEvent): Promise<void> {
    this.events.push(event)
  }

  async getEvents(
    fromTimestamp?: Date,
    toTimestamp?: Date
  ): Promise<StoredEvent[]> {
    return this.events.filter((event) => {
      if (fromTimestamp && event.timestamp < fromTimestamp) return false
      if (toTimestamp && event.timestamp > toTimestamp) return false
      return true
    })
  }

  async replay(
    handler: (event: StoredEvent) => Promise<void>,
    fromTimestamp?: Date
  ): Promise<void> {
    const events = await this.getEvents(fromTimestamp)

    for (const event of events) {
      await handler(event)
    }
  }
}

// Replay Tests
describe('Event Replay', () => {
  let eventStore: EventStore
  let processedEvents: StoredEvent[]

  beforeEach(() => {
    eventStore = new EventStore()
    processedEvents = []
  })

  it('should replay all events', async () => {
    // Store events
    const events = [
      {
        id: '1',
        type: 'order.created',
        data: { orderId: 'ORDER-001' },
        timestamp: new Date('2026-01-01'),
      },
      {
        id: '2',
        type: 'order.confirmed',
        data: { orderId: 'ORDER-001' },
        timestamp: new Date('2026-01-02'),
      },
    ]

    for (const event of events) {
      await eventStore.store(event)
    }

    // Replay events
    await eventStore.replay(async (event) => {
      processedEvents.push(event)
    })

    expect(processedEvents).toHaveLength(2)
    expect(processedEvents).toEqual(events)
  })

  it('should replay events from specific timestamp', async () => {
    const events = [
      {
        id: '1',
        type: 'order.created',
        data: {},
        timestamp: new Date('2026-01-01'),
      },
      {
        id: '2',
        type: 'order.confirmed',
        data: {},
        timestamp: new Date('2026-01-05'),
      },
      {
        id: '3',
        type: 'order.shipped',
        data: {},
        timestamp: new Date('2026-01-10'),
      },
    ]

    for (const event of events) {
      await eventStore.store(event)
    }

    // Replay from Jan 5
    await eventStore.replay(
      async (event) => {
        processedEvents.push(event)
      },
      new Date('2026-01-05')
    )

    expect(processedEvents).toHaveLength(2)
    expect(processedEvents[0].id).toBe('2')
    expect(processedEvents[1].id).toBe('3')
  })
})
```

---

## 7. Performance Testing

### Load Testing Event System

```typescript
// Event Load Test
import { describe, it } from 'vitest'

describe('Event System Load Test', () => {
  it('should handle high throughput', async () => {
    const eventCount = 10000
    const startTime = Date.now()
    const publishedEvents: Promise<void>[] = []

    // Publish events concurrently
    for (let i = 0; i < eventCount; i++) {
      publishedEvents.push(
        eventBus.publish('load.test', {
          id: i,
          timestamp: Date.now(),
        })
      )
    }

    await Promise.all(publishedEvents)

    const duration = Date.now() - startTime
    const throughput = (eventCount / duration) * 1000 // events per second

    console.log(`Published ${eventCount} events in ${duration}ms`)
    console.log(`Throughput: ${throughput.toFixed(2)} events/sec`)

    expect(throughput).toBeGreaterThan(1000) // Expect > 1000 events/sec
  })

  it('should handle concurrent consumers', async () => {
    const consumerCount = 10
    const messagesPerConsumer = 100
    const receivedMessages: number[] = []

    // Start consumers
    const consumers = Array.from({ length: consumerCount }, (_, i) =>
      eventBus.subscribe('concurrent.test', async (event) => {
        receivedMessages.push(event.data.id)
      })
    )

    // Publish messages
    for (let i = 0; i < messagesPerConsumer * consumerCount; i++) {
      await eventBus.publish('concurrent.test', { id: i })
    }

    // Wait for processing
    await new Promise((resolve) => setTimeout(resolve, 2000))

    expect(receivedMessages.length).toBe(messagesPerConsumer * consumerCount)
  })
})
```

---

## Best Practices

1. **Test Isolation**
   - Use test containers for dependencies
   - Clean up queues between tests
   - Reset event stores
   - Avoid test interdependencies

2. **Event Assertions**
   - Verify event content
   - Check event ordering
   - Validate timestamps
   - Assert event counts

3. **Async Testing**
   - Use proper timeouts
   - Wait for event processing
   - Handle race conditions
   - Test eventual consistency

4. **Error Scenarios**
   - Test retry mechanisms
   - Verify DLQ handling
   - Test compensation logic
   - Validate error events

5. **Performance**
   - Load test event throughput
   - Test concurrent consumers
   - Measure latency
   - Monitor resource usage

---

## Common Pitfalls

1. **Timing Issues**: Not waiting for async event processing
2. **Test Pollution**: Events from previous tests affecting current test
3. **Missing Cleanup**: Not purging queues or resetting state
4. **Flaky Tests**: Race conditions in event ordering
5. **Insufficient Timeout**: Tests failing due to short timeouts

---

## Production Checklist

- [ ] Unit tests for all event handlers
- [ ] Integration tests for event flows
- [ ] Saga compensation tested
- [ ] Message queue integration tested
- [ ] Event replay tested
- [ ] Load tests performed
- [ ] Error scenarios covered
- [ ] Monitoring configured
- [ ] DLQ handling verified
- [ ] Performance benchmarks met

---

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| Vitest | Test framework |
| Testcontainers | Docker containers for testing |
| amqplib | RabbitMQ client |
| @testcontainers/rabbitmq | RabbitMQ test container |
| Artillery | Load testing |

---

## Further Reading

- [Testing Event-Driven Systems](https://martinfowler.com/articles/201701-event-driven.html)
- [Saga Pattern Testing](https://microservices.io/patterns/data/saga.html)
- [Message Queue Testing](https://www.rabbitmq.com/tutorials/tutorial-one-javascript.html)
- [Event Sourcing Testing](https://eventstore.com/blog/testing-event-sourced-applications/)
