---
name: CQRS Pattern
description: Implementing Command Query Responsibility Segregation for separating read and write operations in distributed systems.
---

# CQRS Pattern (Command Query Responsibility Segregation)

## Overview

CQRS separates write operations (commands) from read operations (queries) so each
can scale and evolve independently. It is often paired with event sourcing but
can be used with traditional persistence as well.

## Table of Contents

1. [What is CQRS](#what-is-cqrs)
2. [Commands vs Queries](#commands-vs-queries)
3. [Separate Read and Write Models](#separate-read-and-write-models)
4. [CQRS Without Event Sourcing](#cqrs-without-event-sourcing)
5. [CQRS With Event Sourcing](#cqrs-with-event-sourcing)
6. [Eventual Consistency](#eventual-consistency)
7. [Read Model Projections](#read-model-projections)
8. [Sync vs Async Projections](#sync-vs-async-projections)
9. [Command Handlers](#command-handlers)
10. [Query Handlers](#query-handlers)
11. [Database per Model](#database-per-model)
12. [Materialized Views](#materialized-views)
13. [Implementation Patterns](#implementation-patterns)
14. [When to Use CQRS](#when-to-use-cqrs)
15. [Anti-Patterns](#anti-patterns)

---

## What is CQRS

CQRS splits the write model (commands) from the read model (queries). This allows
different data shapes, storage, and scaling strategies for each side.

## Commands vs Queries

- **Command**: Intent to change state (CreateOrder).
- **Query**: Read-only data request (GetOrderSummary).

Commands should be validated and enforce invariants; queries should be optimized
for fast reads.

## Separate Read and Write Models

Write model:
- Validates business rules
- Produces state changes
- Often normalized

Read model:
- Denormalized for fast queries
- Can join data across aggregates

## CQRS Without Event Sourcing

Use traditional DB for writes and a separate read replica or view:
- Write: transactional DB
- Read: read-optimized replica or cache

## CQRS With Event Sourcing

Command side writes events. Read models are projections built from events:
- Clear audit log
- Rebuildable views
- Eventual consistency by design

## Eventual Consistency

Reads may lag behind writes:
- Communicate staleness to clients
- Use read-your-write when required
- Provide consistent "status" endpoints

## Read Model Projections

Projection handler example:
```typescript
interface OrderCreated {
  orderId: string;
  customerId: string;
  total: number;
}

function projectOrderCreated(event: OrderCreated) {
  // Upsert into read model
}
```

## Sync vs Async Projections

- **Synchronous**: Lower staleness, higher latency.
- **Asynchronous**: Higher throughput, eventual consistency.

Pick based on SLA and complexity.

## Command Handlers

Command handlers should:
- Validate input
- Enforce invariants
- Persist changes atomically
- Emit events if needed

## Query Handlers

Query handlers should:
- Use read-optimized storage
- Avoid heavy joins if possible
- Paginate and cache aggressively

## Database per Model

Common patterns:
- Write DB: PostgreSQL/MySQL
- Read DB: Elastic, Redis, or denormalized tables

## Materialized Views

Materialized views provide fast reads and can be refreshed by projections or ETL.

## Implementation Patterns

Node.js example structure:
```
src/
  commands/
  command-handlers/
  queries/
  query-handlers/
  read-models/
```

Python example:
```
app/
  commands/
  handlers/
  read_models/
```

## When to Use CQRS

Use when:
- Read/write workloads differ significantly.
- Read models require different shapes.
- Complex business rules on write side.

Avoid when:
- Simple CRUD is enough.
- Team cannot manage added complexity.

## Anti-Patterns

- Sharing the same ORM model for reads and writes.
- Over-separating models without need.
- Ignoring consistency requirements.

## Related Skills
- `09-microservices/event-sourcing`
- `04-database/database-optimization`
