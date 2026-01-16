# API Design & Contracts

## Overview

API design contracts define the interface between services using specifications like OpenAPI/Swagger. Contract-first development ensures API compatibility, enables parallel development, and provides automatic documentation and client generation.

## Why This Matters

- **Breaking change prevention**: Detect incompatibilities before deployment
- **Parallel development**: Frontend/backend work simultaneously
- **Auto-generated clients**: Type-safe SDKs in multiple languages
- **Living documentation**: Always up-to-date API docs

## Core Concepts

### 1. OpenAPI/Swagger Specification
<!-- TODO: Spec structure, components, paths -->

### 2. Contract-First Development
<!-- TODO: Design spec → Generate code -->

### 3. API Versioning Strategies
<!-- TODO: URL, header, query param versioning -->

### 4. Breaking vs Non-Breaking Changes
<!-- TODO: Compatibility rules, deprecation -->

### 5. Schema Validation
<!-- TODO: Request/response validation -->

### 6. Error Response Standards
<!-- TODO: RFC 7807, error codes -->

### 7. API Evolution
<!-- TODO: Deprecation, sunset headers -->

### 8. Contract Testing
<!-- TODO: Consumer-driven contracts -->

## Quick Start

```yaml
# TODO: Basic OpenAPI spec
```

## Production Checklist

- [ ] OpenAPI spec for all endpoints
- [ ] Automated spec validation in CI
- [ ] Breaking change detection
- [ ] Deprecation policy documented
- [ ] Client SDKs auto-generated
- [ ] API documentation published

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| OpenAPI Generator | Client/server generation |
| Swagger UI | Interactive documentation |
| Spectral | API linting |
| Prism | Mock server |
| Pact | Contract testing |

## Anti-patterns

1. **Code-first without spec**: Inconsistent API contracts
2. **No versioning**: Breaking changes break clients
3. **Ignoring deprecation**: Sudden removal of endpoints
4. **Undocumented errors**: Clients can't handle failures

## Real-World Examples

### Example 1: OpenAPI Specification
<!-- TODO: Complete API spec example -->

### Example 2: Breaking Change Detection
<!-- TODO: CI pipeline for compatibility -->

### Example 3: Client Generation
<!-- TODO: TypeScript SDK generation -->

## Common Mistakes

1. Changing response structure without version bump
2. Not validating requests against spec
3. Missing error response schemas
4. Inconsistent naming conventions

## Integration Points

- API gateways
- Documentation platforms
- CI/CD pipelines
- Client applications

## Further Reading

- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)
- [API Design Patterns (Google)](https://cloud.google.com/apis/design)
- [REST API Design Best Practices](https://restfulapi.net/)
