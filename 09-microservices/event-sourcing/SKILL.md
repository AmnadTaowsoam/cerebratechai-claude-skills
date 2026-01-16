---
name: Event Sourcing
description: Implementing event sourcing pattern for maintaining application state as a sequence of immutable events.
---

# Event Sourcing

## Overview

Event Sourcing stores state changes as an immutable sequence of events. Current
state is derived by replaying events, enabling auditability, time travel, and
rebuildable read models.

## Table of Contents

1. [What is Event Sourcing](#what-is-event-sourcing)
2. [Event Sourcing vs CRUD](#event-sourcing-vs-crud)
3. [Event Store Design](#event-store-design)
4. [Event Types and Schema](#event-types-and-schema)
5. [Versioning and Upcasting](#versioning-and-upcasting)
6. [Snapshots](#snapshots)
7. [Projections and Read Models](#projections-and-read-models)
8. [Event Replay](#event-replay)
9. [Consistency Guarantees](#consistency-guarantees)
10. [Event Sourcing with CQRS](#event-sourcing-with-cqrs)
11. [Aggregate Design](#aggregate-design)
12. [Event Store Implementations](#event-store-implementations)
13. [Schema Evolution](#schema-evolution)
14. [Testing](#testing)
15. [When to Use](#when-to-use)

---

## What is Event Sourcing

Instead of storing only the latest state, store each state change as an event:
```
OrderCreated -> PaymentAuthorized -> OrderShipped
```

The current state is a fold of all events for an aggregate.

## Event Sourcing vs CRUD

- **CRUD**: Overwrites state, limited audit history.
- **Event Sourcing**: Immutable history, full traceability, replayable.

Trade-off: higher complexity and operational overhead.

## Event Store Design

Key characteristics:
- Append-only log
- Strong ordering per aggregate
- Optimistic concurrency via version checks

Minimum fields:
```json
{
  "eventId": "uuid",
  "aggregateId": "order-123",
  "type": "PaymentAuthorized",
  "version": 3,
  "timestamp": "2026-01-01T12:00:00Z",
  "data": {}
}
```

## Event Types and Schema

Guidelines:
- Use explicit domain events.
- Validate event payloads.
- Avoid generic "update" events.

## Versioning and Upcasting

Events evolve. Use upcasters to map old versions to new schemas:
- Add defaults for new fields
- Convert deprecated fields
- Preserve backward compatibility

## Snapshots

Snapshots reduce replay time:
- Snapshot every N events or time interval
- Store snapshot version and payload
- Replay events after the snapshot

## Projections and Read Models

Build query-optimized views by projecting events:
- Materialized views per feature
- Denormalized read models
- Rebuildable from event log

## Event Replay

Rebuild state by replaying events:
- For new projections
- For recovery from corruption
- For audits and simulations

Use replay safeguards:
- Throttle rebuilds
- Run in isolated environments

## Consistency Guarantees

- Strong ordering per aggregate
- Eventual consistency across aggregates
- Read models may be stale until projections catch up

## Event Sourcing with CQRS

Command side writes events; query side reads projections:
- Separate write model from read model
- Scale reads independently
- Clear separation of responsibilities

## Aggregate Design

Aggregates enforce invariants:
- Small, cohesive boundaries
- Single source of truth for rules
- Avoid cross-aggregate transactions

## Event Store Implementations

- **EventStoreDB**: Purpose-built event store.
- **PostgreSQL**: Append-only table + indexes.

For relational DBs, enforce:
- Append-only writes
- Unique (aggregateId, version)

## Schema Evolution

Guidelines:
- Keep events immutable.
- Deprecate old event types gradually.
- Maintain versioned schemas and upcasters.

## Testing

- Unit test aggregates with given-when-then.
- Integration test projections and rebuilds.
- Verify idempotency of projection handlers.

## When to Use

Use when:
- Auditability and replay are required.
- Complex workflows need traceability.

Avoid when:
- CRUD is sufficient.
- Team lacks ops maturity for event-driven systems.

## Related Skills
- `09-microservices/cqrs-pattern`
- `09-microservices/saga-pattern`
- `09-microservices/event-driven`
