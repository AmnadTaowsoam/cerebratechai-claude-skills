---
name: Schema Management
description: Strategies for managing data structures, versioning, and evolutions across databases and event streams.
---

# Schema Management

## Overview

Schema Management is the discipline of defining, versioning, and evolving the structure of data. In a distributed system, a change in one service's schema can have a cascading "breaking" effect on dozens of downstream consumers.

**Core Principle**: "Structure your data so it can change without breaking the world."

---

## 1. Schema Evolution Models

When you change a schema (e.g., adding a field), you must consider compatibility with old and new data.

| Compatibility | Description | Use Case |
| :--- | :--- | :--- |
| **Backwards** | New code can read old data. | Adding an optional field. |
| **Forwards** | Old code can read new data. | Removing a field (if old code ignores it). |
| **Full** | New can read old AND old can read new. | Safest for rolling deployments. |
| **Breaking** | Neither works with the other. | Renaming or deleting a mandatory field. |

---

## 2. Schema Standards

### A. Protocol Buffers (Protobuf)
Strongly typed, binary format. Best for gRPC and internal services.
```protobuf
message User {
  string user_id = 1;      // Tag numbers (1, 2) allow versioning
  string email = 2;
  optional int32 age = 3;  // Optional allows backwards compatibility
}
```

### B. Apache Avro
Binary format with schema stored *with* the data. Best for Big Data (Kafka, Hadoop).
```json
{
  "type": "record",
  "name": "User",
  "fields": [
    {"name": "user_id", "type": "string"},
    {"name": "email", "type": "string"}
  ]
}
```

### C. JSON Schema
Human-readable, best for public APIs.
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "user_id": { "type": "string" },
    "age": { "type": "integer", "minimum": 18 }
  }
}
```

---

## 3. Database Migrations

For Relational DBs (Postgres, MySQL), schema changes must be versioned and reversible.

### Migration Best Practices
1.  **Never Use `SELECT *`**: Explicitly name columns to avoid breaks when new columns are added.
2.  **Add First, Delete Later**: When renaming a field: 
    - Create the new column.
    - Double-write to both.
    - Migrate old data.
    - Delete the old column.
3.  **Idempotency**: Migrations should check if a change has already been applied.

### Example: Liquibase (YAML)
```yaml
databaseChangeLog:
  - changeSet:
      id: 1
      author: team-alpha
      changes:
        - addColumn:
            tableName: users
            columns:
              - column:
                  name: phone_number
                  type: varchar(20)
```

---

## 4. Confluent Schema Registry

A centralized service that stores schemas for Kafka and enforces compatibility rules during the "Producer" phase.

**Workflow**:
1. Producer sends a message to Kafka.
2. Producer checks if the message schema is registered.
3. If new, the Registry checks for **compatibility violations**.
4. If valid, the message is sent with a **Schema ID**.
5. Consumer looks up the ID to decode the message.

---

## 5. Managed Breaking Changes: The "Tombstoning" Strategy

When you must delete a field:
1.  **Phase 1 (Warning)**: Mark the field as `@deprecated` in code and documentation.
2.  **Phase 2 (Shadowing)**: Create the new field and start populating it.
3.  **Phase 3 (Enforce)**: Make the new field mandatory, old field optional.
4.  **Phase 4 (Tombstone)**: Remove the data from the old field but keep the column (to prevent "missing column" errors in old readers).
5.  **Phase 5 (Cleanup)**: Finally drop the column after 6-12 months.

---

## 6. Schema-on-Read vs. Schema-on-Write

*   **Schema-on-Write (RDBMs)**: Data is validated against a schema before being stored. High reliability, slower iteration.
*   **Schema-on-Read (NoSQL/Data Lake)**: Data is stored as raw (JSON/Parquet). Logic for interpreting the structure is in the application. High flexibility, high risk of "Data Swamp".

---

## 7. Breaking Change Detection in CI/CD

Integrate tools like **OpenAPI-diff** or **Tufin** to detect breaking changes in Pull Requests.

```bash
# Example check
npx @redocly/cli lint openapi.yaml
npx openapi-diff old-spec.yaml new-spec.yaml --fail-on-breaking
```

---

## 8. Real-World Scenario: The "Null" Catastrophe
*   **Problem**: A developer changed an optional `middle_name` field to a mandatory `last_name` in a MongoDB collection.
*   **Impact**: Old records didn't have `last_name`, causing the mobile app to crash when attempting to render user profiles (JSON parsing error).
*   **Remediation**: Reverted the code change, created a script to backfill `last_name` with a default string `"N/A"`, and then reapplied the mandatory constraint.

---

## 9. Schema Management Checklist

- [ ] **Documentation**: Does every column have a human-readable description?
- [ ] **Validation**: Are we using a Registry to prevent breaking Kafka changes?
- [ ] **Compatibility**: Is this change Backwards-Compatible?
- [ ] **Migrations**: Can our DB migrations be rolled back automatically?
- [ ] **Naming**: Are we using a consistent naming convention (e.g., `snake_case`)?
- [ ] **Data Types**: Are we using the most efficient type (e.g., `UUID` instead of `TEXT`)?

---

## Related Skills
- `43-data-reliability/data-contracts`
- `43-data-reliability/data-quality-monitoring`
- `41-incident-management/oncall-playbooks`
