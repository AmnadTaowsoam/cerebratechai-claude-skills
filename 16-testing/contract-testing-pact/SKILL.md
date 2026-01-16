---
name: Contract Testing with Pact
description: Implementing consumer-driven contract testing for microservices using Pact.
---

# Contract Testing with Pact

## Overview

Contract testing validates that service consumers and providers agree on
request/response expectations. Pact implements consumer-driven contracts (CDC)
with shareable pact files and provider verification.

## Table of Contents

1. [What is Contract Testing](#what-is-contract-testing)
2. [Consumer-Driven Contracts](#consumer-driven-contracts)
3. [Pact Fundamentals](#pact-fundamentals)
4. [Pact vs Integration Testing](#pact-vs-integration-testing)
5. [Writing Consumer Tests](#writing-consumer-tests)
6. [Provider Verification](#provider-verification)
7. [Pact Broker](#pact-broker)
8. [CI/CD Integration](#cicd-integration)
9. [Bi-Directional Contracts](#bi-directional-contracts)
10. [Async Messaging](#async-messaging)
11. [GraphQL](#graphql)
12. [Language Support](#language-support)
13. [Patterns and Anti-Patterns](#patterns-and-anti-patterns)
14. [Breaking Change Strategy](#breaking-change-strategy)
15. [Monitoring Compliance](#monitoring-compliance)

---

## What is Contract Testing

Contract tests validate API interactions without full end-to-end setups.
They prevent breaking changes by verifying expectations explicitly.

## Consumer-Driven Contracts

Consumers define expectations; providers must satisfy them:
- Faster feedback for consumers
- Clear API expectations
- Reduced integration surprises

## Pact Fundamentals

- **Consumer tests**: Generate pact files.
- **Provider verification**: Validate pact files.
- **Pact files**: JSON contracts.
- **Pact Broker**: Store and manage contracts.

## Pact vs Integration Testing

- **Pact**: Validates interface compatibility.
- **Integration**: Validates full system behavior.

Use both for comprehensive coverage.

## Writing Consumer Tests

Define interactions with matchers:
- Exact value
- Type-based matcher
- Regex matcher

Example (TypeScript):
```typescript
await provider.addInteraction({
  state: 'user exists',
  uponReceiving: 'get user',
  withRequest: { method: 'GET', path: '/users/123' },
  willRespondWith: {
    status: 200,
    body: { id: like(123), name: like('Alice') }
  }
});
```

## Provider Verification

Provider verifies against published contracts:
- Implement state handlers
- Validate response headers/body/status
- Support pending and WIP pacts for safe changes

## Pact Broker

Key features:
- Publish and version contracts
- Webhooks on new contracts
- Can-I-Deploy checks for promotion
- Visibility into compatibility

## CI/CD Integration

Recommended flow:
1. Consumer tests generate pact
2. Publish pact to broker
3. Provider verifies in CI
4. Use Can-I-Deploy before release

## Bi-Directional Contracts

Support for provider-defined expectations plus consumer constraints:
- Useful for GraphQL or schema-first APIs
- Prevents provider drift

## Async Messaging

Pact supports message-based contracts:
- Define message payload expectations
- Verify consumer and provider handlers

## GraphQL

Contract test schema and query responses:
- Use schema as a contract baseline
- Validate query response shapes

## Language Support

SDKs available for:
- JavaScript/TypeScript
- Python
- Java
- Go

## Patterns and Anti-Patterns

Good:
- Use flexible matchers
- Keep interactions focused

Avoid:
- Over-specifying exact values
- One contract covering multiple unrelated cases

## Breaking Change Strategy

- Use pending pacts for backward-compatible changes.
- Version APIs when breaking changes are required.
- Maintain old contract until consumers migrate.

## Monitoring Compliance

Track contract verification in CI and alert on failed verification runs.

## Related Skills
- `16-testing/integration-testing`
- `09-microservices/service-design`
- `03-backend-api/express-rest`
