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

## Best Practices

### Event Design

- **Use explicit domain events**: Name events based on business language
- **Make events immutable**: Never modify events after creation
- **Include event metadata**: Add timestamps, correlation IDs, and causation IDs
- **Keep events small**: Prefer focused events over large payloads
- **Validate event schemas**: Ensure events conform to defined schemas

### Event Store Design

- **Use append-only storage**: Never update or delete events
- **Enforce ordering per aggregate**: Ensure events are ordered by version
- **Implement optimistic concurrency**: Use version checks to prevent conflicts
- **Choose appropriate storage**: EventStoreDB, PostgreSQL, or other options
- **Plan for scalability**: Design for high write throughput

### Snapshots

- **Snapshot periodically**: After N events or time interval
- **Store snapshot version**: Include event version for consistency
- **Use snapshots for replay**: Start replay from last snapshot
- **Keep snapshots consistent**: Ensure snapshots match event history
- **Monitor snapshot performance**: Track snapshot creation time

### Projections

- **Design for queries**: Build projections optimized for read patterns
- **Make projections rebuildable**: Allow complete rebuild from event log
- **Use idempotent handlers**: Handle duplicate events safely
- **Handle event ordering**: Process events in correct order
- **Monitor projection lag**: Track how far behind projections are

### Event Replay

- **Test replay procedures**: Verify replay works correctly
- **Use throttling**: Limit replay impact on production
- **Plan replay time**: Estimate how long replay will take
- **Use isolated environments**: Test replay in staging first
- **Monitor replay progress**: Track replay completion

### CQRS Integration

- **Separate read and write models**: Use different schemas for each
- **Scale independently**: Scale read and write sides separately
- **Handle eventual consistency**: Communicate staleness to users
- **Use read-your-writes**: When strong consistency is needed
- **Design for async updates**: Accept temporary inconsistency

### Schema Evolution

- **Never modify existing events**: Create new event types instead
- **Use upcasters**: Convert old event versions to new schemas
- **Deprecate gradually**: Mark old event types before removal
- **Maintain backward compatibility**: Support multiple event versions
- **Document schema changes**: Keep clear records of all changes

### Performance

- **Batch event writes**: Write multiple events together when possible
- **Use appropriate indexes**: Index for read patterns, not write patterns
- **Monitor event throughput**: Track events per second
- **Optimize replay**: Use snapshots to reduce replay time
- **Choose appropriate storage**: Match storage to workload

### Monitoring

- **Track event counts**: Monitor events per aggregate and type
- **Monitor projection lag**: Alert on large delays
- **Track replay performance**: Measure replay time and resource usage
- **Monitor event store health**: Track storage metrics
- **Set up alerts**: Notify on anomalies or failures

## Checklist

### Event Design
- [ ] Define event schemas
- [ ] Use explicit domain event names
- [ ] Include event metadata (timestamps, correlation IDs)
- [ ] Validate event payloads
- [ ] Document event types

### Event Store Setup
- [ ] Choose appropriate event store
- [ ] Configure append-only writes
- [ ] Implement optimistic concurrency
- [ ] Set up indexes for queries
- [ ] Configure replication for high availability

### Aggregate Design
- [ ] Define aggregate boundaries
- [ ] Implement business invariants
- [ ] Design event sequence
- [ ] Implement version checking
- [ ] Test aggregate behavior

### Snapshot Strategy
- [ ] Define snapshot frequency
- [ ] Implement snapshot creation
- [ ] Store snapshot versions
- [ ] Test replay from snapshots
- [ ] Monitor snapshot performance

### Projection Design
- [ ] Identify read patterns
- [ ] Design projection schemas
- [ ] Implement projection handlers
- [ ] Make projections idempotent
- [ ] Test projection rebuilds

### CQRS Setup
- [ ] Separate read and write models
- [ ] Configure separate databases if needed
- [ ] Implement command handlers
- [ ] Implement query handlers
- [ ] Handle eventual consistency

### Event Replay
- [ ] Design replay procedures
- [ ] Implement replay throttling
- [ ] Test replay in staging
- [ ] Plan replay windows
- [ ] Monitor replay progress

### Schema Evolution
- [ ] Define event versioning strategy
- [ ] Implement upcasters
- [ ] Plan deprecation process
- [ ] Maintain backward compatibility
- [ ] Document schema changes

### Monitoring
- [ ] Set up event metrics
- [ ] Monitor projection lag
- [ ] Track event throughput
- [ ] Configure alerts
- [ ] Create dashboards

### Testing
- [ ] Test aggregate behavior
- [ ] Test projection handlers
- [ ] Test event replay
- [ ] Test schema evolution
- [ ] Performance test event store

### Documentation
- [ ] Document event schemas
- [ ] Document aggregate design
- [ ] Document projection logic
- [ ] Create replay runbooks
- [ ] Maintain API documentation
