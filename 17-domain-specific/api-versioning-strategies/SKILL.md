---
name: API Versioning Strategies
description: Comprehensive guide to API versioning approaches for maintaining backward compatibility.
---

# API Versioning Strategies

## Overview

API versioning protects clients from breaking changes while allowing
servers to evolve. This guide covers strategies, lifecycle management,
and migration practices.

## Table of Contents

1. [Why Version APIs](#why-version-apis)
2. [Versioning Strategies](#versioning-strategies)
3. [Semantic Versioning](#semantic-versioning)
4. [Breaking vs Non-Breaking Changes](#breaking-vs-non-breaking-changes)
5. [Deprecation Strategies](#deprecation-strategies)
6. [Version Lifecycle Management](#version-lifecycle-management)
7. [Multi-Version Support](#multi-version-support)
8. [API Evolution Patterns](#api-evolution-patterns)
9. [GraphQL Versioning](#graphql-versioning)
10. [OpenAPI Versioning](#openapi-versioning)
11. [SDK Versioning](#sdk-versioning)
12. [Client Migration](#client-migration)
13. [Monitoring Version Usage](#monitoring-version-usage)
14. [Best Practices](#best-practices)
15. [Anti-Patterns](#anti-patterns)

---

## Why Version APIs

- Preserve backward compatibility
- Enable safe migrations
- Support long-lived clients

## Versioning Strategies

Common approaches:
- **URI**: `/v1/users`
- **Query**: `?version=1`
- **Header**: `Accept-Version: 1`
- **Content negotiation**: `Accept: application/vnd.api+json;version=1`

Prefer URI or header for clarity and tooling support.

## Semantic Versioning

Use semantic versioning to communicate changes:
- **Major**: breaking changes
- **Minor**: backward-compatible additions
- **Patch**: backward-compatible fixes

## Breaking vs Non-Breaking Changes

Breaking:
- Removing fields or endpoints
- Changing field types
- Altering error semantics

Non-breaking:
- Adding optional fields
- Adding new endpoints
- Adding enum values (if tolerant readers)

## Deprecation Strategies

Use:
- `Sunset` header for planned retirement
- Deprecation notices in docs
- Grace periods for migration

## Version Lifecycle Management

- Define support timelines per version
- Maintain a changelog and migration guide
- Automate deprecation notices

## Multi-Version Support

Techniques:
- Separate routing per version
- Versioned controllers or handlers
- Versioned API docs

Example routing:
```
/v1/users -> v1 handlers
/v2/users -> v2 handlers
```

## API Evolution Patterns

- **Additive changes**: Add new fields/endpoints.
- **Expand and contract**: Introduce new API, migrate, then remove old.
- **Tolerant reader**: Ignore unknown fields.

## GraphQL Versioning

GraphQL prefers:
- Deprecate fields with `@deprecated`
- Add new fields instead of breaking schema

## OpenAPI Versioning

Maintain versioned OpenAPI specs and publish per version.

## SDK Versioning

Align SDK versions with API versions and document compatibility.

## Client Migration

- Provide migration guides
- Use feature flags for gradual rollout
- Offer dual-write or response shaping during transition

## Monitoring Version Usage

- Track usage per version
- Alert on deprecated version activity
- Report adoption progress

## Best Practices

- Minimize number of active versions
- Provide long-enough deprecation windows
- Avoid breaking changes when possible

## Anti-Patterns

- Silent breaking changes
- Too many parallel versions
- Unclear version headers or routing rules

## Related Skills
- `01-foundations/api-design`
- `03-backend-api/express-rest`
- `51-contracts-governance/openapi-governance`
