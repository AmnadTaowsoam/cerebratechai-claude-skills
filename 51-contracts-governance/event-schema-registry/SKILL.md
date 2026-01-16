---
name: Event Schema Registry
description: Comprehensive guide to event schema registries, schema evolution, compatibility checking, and governance for event-driven architectures
---

# Event Schema Registry

## What is Event Schema Registry?

**Definition:** Centralized repository of event schemas with versioning, validation, and compatibility checking.

### Purpose
```
Producer publishes event → Schema Registry validates schema
Consumer receives event → Schema Registry provides schema
→ Contract between producer and consumer
```

### Example
```
Event: user.created
Schema v1: { id, email, name }
Schema v2: { id, email, name, avatar }  (backward compatible)

Consumer using v1 schema can still read v2 events
```

---

## Why Schema Registry Matters

### 1. Prevents Breaking Changes in Event Streams

**Without Registry:**
```
Producer changes event format:
- name: string (removed)
+ firstName: string
+ lastName: string

Consumer breaks (expects 'name' field)
```

**With Registry:**
```
Producer tries to register breaking change
→ Registry rejects (not backward compatible)
→ Producer must use new event type or major version
```

### 2. Self-Documenting Events

**Registry as Documentation:**
- What events exist?
- What fields do they have?
- What are the types?
- Who produces/consumes them?

### 3. Type Safety Across Producers/Consumers

**Generated Types:**
```typescript
// Auto-generated from schema
interface UserCreatedEvent {
  id: string;
  email: string;
  name: string;
  createdAt: string;
}

// Type-safe producer
producer.send<UserCreatedEvent>({
  id: '123',
  email: 'user@example.com',
  name: 'John Doe',
  createdAt: '2024-01-15T10:00:00Z'
});
```

### 4. Contract Between Services

**Agreement:**
- Producer promises to send events matching schema
- Consumer expects events matching schema
- Registry enforces contract

---

## Schema Formats

### JSON Schema (Flexible, Widely Supported)

**Example:**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "UserCreatedEvent",
  "type": "object",
  "required": ["id", "email", "name", "createdAt"],
  "properties": {
    "id": {
      "type": "string",
      "format": "uuid"
    },
    "email": {
      "type": "string",
      "format": "email"
    },
    "name": {
      "type": "string"
    },
    "createdAt": {
      "type": "string",
      "format": "date-time"
    }
  }
}
```

**Pros:**
- Human-readable
- Widely supported
- Flexible

**Cons:**
- Verbose
- No built-in schema evolution

### Avro (Compact, Schema Evolution)

**Example:**
```json
{
  "type": "record",
  "name": "UserCreatedEvent",
  "namespace": "com.example.events",
  "fields": [
    {"name": "id", "type": "string"},
    {"name": "email", "type": "string"},
    {"name": "name", "type": "string"},
    {"name": "createdAt", "type": "long", "logicalType": "timestamp-millis"}
  ]
}
```

**Pros:**
- Compact binary format
- Built-in schema evolution
- Fast serialization

**Cons:**
- Not human-readable (binary)
- Requires schema to deserialize

### Protobuf (Efficient, Strongly Typed)

**Example:**
```protobuf
syntax = "proto3";

message UserCreatedEvent {
  string id = 1;
  string email = 2;
  string name = 3;
  int64 created_at = 4;
}
```

**Pros:**
- Very efficient
- Strongly typed
- Code generation

**Cons:**
- Requires compilation
- Less flexible than JSON

### Comparison: When to Use Each

| Format | Use Case | Pros | Cons |
|--------|----------|------|------|
| **JSON Schema** | REST APIs, webhooks, simple events | Human-readable, flexible | Verbose, no built-in evolution |
| **Avro** | Kafka, high-volume streams | Compact, schema evolution | Binary, requires schema |
| **Protobuf** | gRPC, microservices | Efficient, strongly typed | Requires compilation |

**Recommendation:**
- **Kafka:** Avro (with Confluent Schema Registry)
- **Webhooks:** JSON Schema
- **gRPC:** Protobuf

---

## Schema Registry Implementations

### Confluent Schema Registry (for Kafka)

**Features:**
- Avro, JSON Schema, Protobuf support
- Compatibility checking
- REST API
- Integration with Kafka

**Setup:**
```bash
docker run -d \
  --name schema-registry \
  -p 8081:8081 \
  -e SCHEMA_REGISTRY_HOST_NAME=schema-registry \
  -e SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS=kafka:9092 \
  confluentinc/cp-schema-registry
```

**Pricing:** Free (open source), or Confluent Cloud ($0.13/hour)

### AWS Glue Schema Registry

**Features:**
- Avro, JSON Schema, Protobuf
- Integration with Kinesis, MSK, Lambda
- Compatibility checking
- Free tier

**Setup:**
```python
import boto3

glue = boto3.client('glue')

glue.create_schema(
    RegistryId={'RegistryName': 'my-registry'},
    SchemaName='user-created',
    DataFormat='AVRO',
    Compatibility='BACKWARD',
    SchemaDefinition=avro_schema
)
```

### Azure Schema Registry

**Features:**
- Avro support
- Integration with Event Hubs
- Compatibility checking

**Setup:**
```csharp
var client = new SchemaRegistryClient(
    endpoint: "https://my-namespace.servicebus.windows.net",
    credential: new DefaultAzureCredential()
);

var schema = await client.RegisterSchemaAsync(
    groupName: "my-group",
    schemaName: "user-created",
    schemaDefinition: avroSchema,
    format: SchemaFormat.Avro
);
```

### Custom Registry (Database + API)

**Database Schema:**
```sql
CREATE TABLE schemas (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  version INT NOT NULL,
  format VARCHAR(50) NOT NULL,  -- 'json-schema', 'avro', 'protobuf'
  definition TEXT NOT NULL,
  compatibility VARCHAR(50),     -- 'BACKWARD', 'FORWARD', 'FULL'
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(name, version)
);

CREATE TABLE schema_compatibility_checks (
  id UUID PRIMARY KEY,
  schema_id UUID REFERENCES schemas(id),
  previous_version INT,
  is_compatible BOOLEAN,
  errors TEXT,
  checked_at TIMESTAMP DEFAULT NOW()
);
```

**API:**
```
POST   /schemas                    Register new schema
GET    /schemas/{name}             Get latest schema
GET    /schemas/{name}/versions    List all versions
GET    /schemas/{name}/v/{version} Get specific version
POST   /schemas/{name}/compatibility Check compatibility
```

---

## Schema Structure

### Event Metadata

**Standard Fields:**
```json
{
  "id": "evt_123",
  "type": "user.created",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:00:00Z",
  "source": "user-service",
  "data": { ... }
}
```

### Event Type (domain.entity.action)

**Format:** `domain.entity.action`

**Examples:**
- `user.account.created`
- `order.payment.processed`
- `inventory.item.updated`
- `notification.email.sent`

### Event Payload (Actual Data)

**Example:**
```json
{
  "id": "evt_123",
  "type": "user.account.created",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:00:00Z",
  "data": {
    "userId": "123",
    "email": "user@example.com",
    "name": "John Doe",
    "plan": "pro"
  }
}
```

### Schema Version

**Semantic Versioning:**
```
1.0.0 → 1.1.0  (backward compatible: add optional field)
1.1.0 → 2.0.0  (breaking: remove field)
```

---

## Schema Evolution Rules

### Forward Compatibility (New Consumer, Old Producer)

**Definition:** New consumer can read old events

**Example:**
```
Old event (v1): { id, email }
New consumer expects (v2): { id, email, name? }

Consumer handles missing 'name' field → Compatible ✅
```

**Rule:** Can add optional fields

### Backward Compatibility (Old Consumer, New Producer)

**Definition:** Old consumer can read new events

**Example:**
```
Old consumer expects (v1): { id, email }
New event (v2): { id, email, name }

Consumer ignores 'name' field → Compatible ✅
```

**Rule:** Can add fields (old consumers ignore them)

### Full Compatibility (Both Directions)

**Definition:** New consumer reads old events AND old consumer reads new events

**Example:**
```
v1: { id, email }
v2: { id, email, name? }  (optional field)

Old consumer + new events: Ignores 'name' ✅
New consumer + old events: Handles missing 'name' ✅
```

**Rule:** Only add optional fields

### Breaking Changes (Require Major Version)

**Examples:**
- Remove required field
- Change field type
- Rename field
- Change field semantics

**Solution:** Create new event type or major version

---

## Compatible Changes

### Add Optional Field

**Before (v1):**
```json
{
  "type": "object",
  "required": ["id", "email"],
  "properties": {
    "id": {"type": "string"},
    "email": {"type": "string"}
  }
}
```

**After (v2):**
```json
{
  "type": "object",
  "required": ["id", "email"],
  "properties": {
    "id": {"type": "string"},
    "email": {"type": "string"},
    "name": {"type": "string"}  // Optional (not in required)
  }
}
```

**Compatible:** ✅ Backward compatible

### Remove Optional Field

**Before (v1):**
```json
{
  "required": ["id", "email"],
  "properties": {
    "id": {"type": "string"},
    "email": {"type": "string"},
    "phone": {"type": "string"}  // Optional
  }
}
```

**After (v2):**
```json
{
  "required": ["id", "email"],
  "properties": {
    "id": {"type": "string"},
    "email": {"type": "string"}
    // 'phone' removed
  }
}
```

**Compatible:** ✅ Forward compatible (old consumers ignore missing field)

### Add New Event Type

**New Event:**
```
user.account.deleted  (new event type)
```

**Compatible:** ✅ Doesn't affect existing events

### Add Enum Value (at End)

**Before:**
```json
{
  "status": {
    "type": "string",
    "enum": ["ACTIVE", "INACTIVE"]
  }
}
```

**After:**
```json
{
  "status": {
    "type": "string",
    "enum": ["ACTIVE", "INACTIVE", "PENDING"]
  }
}
```

**Compatible:** ✅ Backward compatible (old consumers may not handle new value, but schema is valid)

---

## Breaking Changes

### Remove Required Field

**Before:**
```json
{
  "required": ["id", "email", "name"],
  "properties": {
    "id": {"type": "string"},
    "email": {"type": "string"},
    "name": {"type": "string"}
  }
}
```

**After:**
```json
{
  "required": ["id", "email"],  // 'name' removed
  "properties": {
    "id": {"type": "string"},
    "email": {"type": "string"}
  }
}
```

**Breaking:** ❌ Old consumers expect 'name' field

### Change Field Type

**Before:**
```json
{
  "age": {"type": "integer"}
}
```

**After:**
```json
{
  "age": {"type": "string"}  // Changed type
}
```

**Breaking:** ❌ Old consumers expect integer

### Rename Field

**Before:**
```json
{
  "name": {"type": "string"}
}
```

**After:**
```json
{
  "fullName": {"type": "string"}  // Renamed
}
```

**Breaking:** ❌ Old consumers expect 'name' field

### Change Field Semantics

**Before:**
```json
{
  "amount": {"type": "integer"}  // Amount in dollars
}
```

**After:**
```json
{
  "amount": {"type": "integer"}  // Amount in cents (changed meaning!)
}
```

**Breaking:** ❌ Same field, different meaning

---

## Schema Versioning

### Semantic Versioning (MAJOR.MINOR.PATCH)

**Format:** `MAJOR.MINOR.PATCH`

**Rules:**
- **MAJOR:** Breaking changes (remove field, change type)
- **MINOR:** Backward-compatible additions (add optional field)
- **PATCH:** Bug fixes (no schema change, just documentation)

**Example:**
```
1.0.0: Initial schema
1.1.0: Add optional 'avatar' field (backward compatible)
1.1.1: Fix typo in description (no schema change)
2.0.0: Remove 'name' field, add 'firstName' and 'lastName' (breaking)
```

---

## Event Naming Conventions

### Format: domain.entity.action

**Structure:**
```
{domain}.{entity}.{action}

Examples:
user.account.created
order.payment.processed
inventory.item.updated
```

### Past Tense (Event Already Happened)

```
✅ Good:
user.created
order.placed
payment.processed

❌ Bad:
user.create (present tense)
order.place (imperative)
```

### Specific (Not Too Generic)

```
✅ Good:
user.account.created
user.profile.updated
user.password.reset

❌ Bad:
user.changed (too generic)
user.event (meaningless)
```

---

## Schema Validation

### Producer-Side Validation (Before Publish)

**Example (JavaScript):**
```javascript
const Ajv = require('ajv');
const ajv = new Ajv();

// Get schema from registry
const schema = await schemaRegistry.getSchema('user.created', 'latest');

// Validate event
const validate = ajv.compile(schema);
const event = {
  id: '123',
  email: 'user@example.com',
  name: 'John Doe',
  createdAt: '2024-01-15T10:00:00Z'
};

if (!validate(event)) {
  throw new Error(`Invalid event: ${JSON.stringify(validate.errors)}`);
}

// Publish event
await producer.send({
  topic: 'user-events',
  value: event
});
```

### Consumer-Side Validation (After Receive)

**Example:**
```javascript
consumer.on('message', async (message) => {
  const event = JSON.parse(message.value);
  
  // Get schema from registry
  const schema = await schemaRegistry.getSchema('user.created', event.version);
  
  // Validate event
  const validate = ajv.compile(schema);
  if (!validate(event)) {
    console.error('Invalid event:', validate.errors);
    // Send to Dead Letter Queue
    await dlq.send(message);
    return;
  }
  
  // Process event
  await handleUserCreated(event);
});
```

### Schema Registry Enforcement

**Confluent Schema Registry:**
```javascript
const { SchemaRegistry } = require('@kafkajs/confluent-schema-registry');

const registry = new SchemaRegistry({ host: 'http://localhost:8081' });

// Producer
const encodedMessage = await registry.encode(schemaId, event);
await producer.send({
  topic: 'user-events',
  value: encodedMessage
});

// Consumer
const decodedMessage = await registry.decode(message.value);
```

---

## Schema Discovery

### Searchable Registry UI

**Features:**
- Search schemas by name
- Browse by domain/entity
- View schema details
- See version history

**Example (Confluent Control Center):**
```
Schemas:
- user.account.created (v1.2.0)
- user.profile.updated (v1.0.0)
- order.payment.processed (v2.1.0)

Click schema → View details:
- Fields
- Examples
- Producers
- Consumers
```

### Documentation Generation

**Auto-Generated Docs:**
```markdown
# user.account.created

**Version:** 1.2.0
**Compatibility:** BACKWARD

## Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | string (uuid) | Yes | User ID |
| email | string (email) | Yes | User email |
| name | string | Yes | User name |
| avatar | string (url) | No | Avatar URL (added in v1.2.0) |

## Example

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "name": "John Doe",
  "avatar": "https://example.com/avatar.jpg"
}
```

## Producers
- user-service (v2.1.0)

## Consumers
- email-service (v1.5.0)
- analytics-service (v3.0.0)
```

### Example Events

**Registry Stores Examples:**
```json
{
  "schemaName": "user.created",
  "version": "1.0.0",
  "examples": [
    {
      "name": "Basic user",
      "value": {
        "id": "123",
        "email": "user@example.com",
        "name": "John Doe"
      }
    },
    {
      "name": "User with avatar",
      "value": {
        "id": "456",
        "email": "jane@example.com",
        "name": "Jane Smith",
        "avatar": "https://example.com/avatar.jpg"
      }
    }
  ]
}
```

### Consumer/Producer Tracking

**Who Uses What:**
```
Schema: user.account.created

Producers:
- user-service (v2.1.0)
  - Last published: 2024-01-15 10:00:00
  - Events/day: 1,000

Consumers:
- email-service (v1.5.0)
  - Last consumed: 2024-01-15 10:05:00
  - Events/day: 1,000
- analytics-service (v3.0.0)
  - Last consumed: 2024-01-15 10:03:00
  - Events/day: 1,000
```

---

## Multi-Environment Schemas

### Dev, Staging, Prod Registries

**Separate Registries:**
```
Dev:     http://schema-registry-dev:8081
Staging: http://schema-registry-staging:8081
Prod:    http://schema-registry-prod:8081
```

**Why Separate:**
- Test schema changes in dev/staging
- Prevent accidental prod changes
- Different schemas in different environments

### Schema Promotion Workflow

**Process:**
```
1. Register schema in dev
2. Test with dev events
3. Promote to staging
4. Test with staging events
5. Promote to prod
6. Deploy producer/consumer code
```

**Automation:**
```bash
# Promote schema from dev to staging
./promote-schema.sh user.created 1.2.0 dev staging

# Promote schema from staging to prod
./promote-schema.sh user.created 1.2.0 staging prod
```

### Testing Schema Changes

**Process:**
```
1. Create new schema version in dev
2. Deploy producer to dev (publishes new events)
3. Deploy consumer to dev (reads new events)
4. Verify compatibility
5. Promote to staging
6. Repeat testing
7. Promote to prod
```

---

## Schema Governance Workflow

### Step 1: Developer Proposes Schema (PR)

**Process:**
```
1. Create feature branch
2. Add/update schema file (schemas/user-created.json)
3. Commit and push
4. Create PR
```

### Step 2: Automated Compatibility Check (CI)

**GitHub Actions:**
```yaml
- name: Check schema compatibility
  run: |
    # Get previous version
    PREV_VERSION=$(curl http://schema-registry:8081/subjects/user.created/versions/latest | jq -r '.version')
    
    # Check compatibility
    curl -X POST http://schema-registry:8081/compatibility/subjects/user.created/versions/$PREV_VERSION \
      -H "Content-Type: application/json" \
      -d @schemas/user-created.json
    
    # Exit if not compatible
    if [ $? -ne 0 ]; then
      echo "Schema is not backward compatible"
      exit 1
    fi
```

### Step 3: Review by Data Team

**Review Checklist:**
- [ ] Follows naming conventions
- [ ] Has description and examples
- [ ] Backward compatible (or justified breaking change)
- [ ] No PII in event name
- [ ] Appropriate data types

### Step 4: Register Schema in Registry

**After Approval:**
```bash
curl -X POST http://schema-registry:8081/subjects/user.created/versions \
  -H "Content-Type: application/json" \
  -d @schemas/user-created.json
```

### Step 5: Deploy Producer/Consumer Code

**Process:**
```
1. Update producer to use new schema
2. Deploy producer
3. Update consumer to handle new schema
4. Deploy consumer
```

---

## Dead Letter Queue (DLQ)

### Invalid Events Go to DLQ

**Example:**
```javascript
consumer.on('message', async (message) => {
  try {
    const event = JSON.parse(message.value);
    
    // Validate against schema
    if (!validate(event)) {
      throw new Error('Invalid schema');
    }
    
    await handleEvent(event);
  } catch (err) {
    // Send to DLQ
    await dlq.send({
      topic: 'user-events-dlq',
      value: message.value,
      headers: {
        'error': err.message,
        'original-topic': 'user-events'
      }
    });
  }
});
```

### Monitor DLQ for Schema Violations

**Alerts:**
```
Alert: High DLQ rate
Topic: user-events-dlq
Error: Invalid schema (field 'name' is required)
Count: 100 events in last hour

Action: Investigate producer
```

### Fix and Replay

**Process:**
```
1. Identify issue (producer sending invalid events)
2. Fix producer
3. Deploy fix
4. Replay DLQ events
```

**Replay:**
```javascript
// Read from DLQ
const dlqEvents = await dlq.read('user-events-dlq');

// Replay to original topic
for (const event of dlqEvents) {
  await producer.send({
    topic: event.headers['original-topic'],
    value: event.value
  });
}
```

---

## Schema Migration

### Dual Publishing (Old + New Schema)

**Process:**
```
1. Publish events in both old and new format
2. Consumers migrate to new format
3. Stop publishing old format
4. Remove old schema
```

**Example:**
```javascript
// Publish both formats
await producer.send({
  topic: 'user-events-v1',
  value: { id, name }  // Old format
});

await producer.send({
  topic: 'user-events-v2',
  value: { id, firstName, lastName }  // New format
});
```

### Consumer Migration

**Process:**
```
1. Deploy consumer that reads both v1 and v2
2. Gradually migrate consumers to v2
3. Once all consumers on v2, stop publishing v1
```

### Deprecate Old Schema

**Timeline:**
```
Month 0: Announce deprecation
Month 3: Stop publishing old format
Month 6: Remove old schema
```

---

## Tools and Libraries

### Confluent Schema Registry

See "Schema Registry Implementations" section

### JSON Schema Validators

**JavaScript:**
```bash
npm install ajv
```

**Python:**
```bash
pip install jsonschema
```

### Avro/Protobuf Libraries

**Avro (JavaScript):**
```bash
npm install avsc
```

**Protobuf (JavaScript):**
```bash
npm install protobufjs
```

### Schema Registry Clients

**JavaScript:**
```bash
npm install @kafkajs/confluent-schema-registry
```

**Python:**
```bash
pip install confluent-kafka[avro]
```

---

## Real-World Event Schemas

### Kafka Event Schemas

See examples throughout this document

### Webhook Payloads

**GitHub Webhook:**
```json
{
  "action": "created",
  "issue": {
    "id": 1,
    "number": 1,
    "title": "Bug report",
    "body": "Description"
  },
  "repository": {
    "id": 123,
    "name": "my-repo"
  }
}
```

### CloudEvents Standard

**Format:**
```json
{
  "specversion": "1.0",
  "type": "com.example.user.created",
  "source": "https://example.com/users",
  "id": "A234-1234-1234",
  "time": "2024-01-15T10:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "userId": "123",
    "email": "user@example.com"
  }
}
```

---

## Summary

### Quick Reference

**Schema Registry:** Centralized repository of event schemas with versioning and validation

**Why:**
- Prevent breaking changes
- Self-documenting events
- Type safety
- Contract between services

**Schema Formats:**
- JSON Schema (flexible, human-readable)
- Avro (compact, schema evolution)
- Protobuf (efficient, strongly typed)

**Implementations:**
- Confluent Schema Registry (Kafka)
- AWS Glue Schema Registry
- Azure Schema Registry
- Custom (database + API)

**Evolution Rules:**
- Backward compatible: Old consumer + new events
- Forward compatible: New consumer + old events
- Full compatible: Both directions

**Compatible Changes:**
- Add optional field
- Remove optional field
- Add new event type

**Breaking Changes:**
- Remove required field
- Change field type
- Rename field

**Versioning:** Semantic (MAJOR.MINOR.PATCH)

**Naming:** `domain.entity.action` (past tense)

**Validation:**
- Producer-side (before publish)
- Consumer-side (after receive)
- Registry enforcement

**Workflow:**
1. Propose schema (PR)
2. Compatibility check (CI)
3. Data team review
4. Register in registry
5. Deploy code

## Overview

Event Schema Registry is a centralized repository of event schemas with versioning, validation, and compatibility checking for event-driven architectures.

### Purpose

```
Producer publishes event → Schema Registry validates schema
Consumer receives event → Schema Registry provides schema
→ Contract between producer and consumer
```

### Example

```
Event: user.created
Schema v1: { id, email, name }
Schema v2: { id, email, name, avatar }  (backward compatible)

Consumer using v1 schema can still read v2 events
```

---

## Why Schema Registry Matters

### 1. Prevents Breaking Changes in Event Streams

**Without Registry:**
```
Producer changes event format:
- name: string (removed)
+ firstName: string
+ lastName: string

Consumer breaks (expects 'name' field)
```

**With Registry:**
```
Producer tries to register breaking change
→ Registry rejects (not backward compatible)
→ Producer must use new event type or major version
```

### 2. Self-Documenting Events

**Registry as Documentation:**
- What events exist?
- What fields do they have?
- What are the types?
- Who produces/consumes them?

### 3. Type Safety Across Producers/Consumers

**Generated Types:**
```typescript
// Auto-generated from schema
interface UserCreatedEvent {
  id: string;
  email: string;
  name: string;
  createdAt: string;
}

// Type-safe producer
producer.send<UserCreatedEvent>({
  id: '123',
  email: 'user@example.com',
  name: 'John Doe',
  createdAt: '2024-01-15T10:00:00Z'
});
```

### 4. Contract Between Services

**Agreement:**
- Producer promises to send events matching schema
- Consumer expects events matching schema
- Registry enforces contract

---

## Schema Formats

### JSON Schema (Flexible, Widely Supported)

**Pros:**
- Human-readable
- Widely supported
- Flexible

**Cons:**
- Verbose
- No built-in schema evolution

### Avro (Compact, Schema Evolution)

**Pros:**
- Compact binary format
- Built-in schema evolution
- Fast serialization

**Cons:**
- Not human-readable (binary)
- Requires schema to deserialize

### Protobuf (Efficient, Strongly Typed)

**Pros:**
- Very efficient
- Strongly typed
- Code generation

**Cons:**
- Requires compilation
- Less flexible than JSON

---

## Schema Evolution Rules

### Forward Compatibility (New Consumer, Old Producer)

**Definition:** New consumer can read old events

**Rule:** Can add optional fields

### Backward Compatibility (Old Consumer, New Producer)

**Definition:** Old consumer can read new events

**Rule:** Can add fields (old consumers ignore them)

### Full Compatibility (Both Directions)

**Definition:** New consumer reads old events AND old consumer reads new events

**Rule:** Only add optional fields

### Breaking Changes (Require Major Version)

**Examples:**
- Remove required field
- Change field type
- Rename field
- Change field semantics

---

## Compatible Changes

### Add Optional Field

**Before (v1):**
```json
{
  "type": "object",
  "required": ["id", "email"],
  "properties": {
    "id": {"type": "string"},
    "email": {"type": "string"}
  }
}
```

**After (v2):**
```json
{
  "type": "object",
  "required": ["id", "email"],
  "properties": {
    "id": {"type": "string"},
    "email": {"type": "string"},
    "name": {"type": "string"}  // Optional (not in required)
  }
}
```

**Compatible:** ✅ Backward compatible

### Add New Event Type

**New Event:**
```
user.account.deleted  (new event type)
```

**Compatible:** ✅ Doesn't affect existing events

### Add Enum Value (at End)

**Before:**
```json
{
  "status": {
    "type": "string",
    "enum": ["ACTIVE", "INACTIVE"]
  }
}
```

**After:**
```json
{
  "status": {
    "type": "string",
    "enum": ["ACTIVE", "INACTIVE", "PENDING"]
  }
}
```

**Compatible:** ✅ Backward compatible (old consumers may not handle new value, but schema is valid)

---

## Breaking Changes

### Remove Required Field

**Before:**
```json
{
  "required": ["id", "email", "name"],
  "properties": {
    "id": {"type": "string"},
    "email": {"type": "string"},
    "name": {"type": "string"}
  }
}
```

**After:**
```json
{
  "required": ["id", "email"],  // 'name' removed
  "properties": {
    "id": {"type": "string"},
    "email": {"type": "string"}
  }
}
```

**Breaking:** ❌ Old consumers expect 'name' field

### Change Field Type

**Before:**
```json
{
  "age": {"type": "integer"}
}
```

**After:**
```json
{
  "age": {"type": "string"}  // Changed type
}
```

**Breaking:** ❌ Old consumers expect integer

### Rename Field

**Before:**
```json
{
  "name": {"type": "string"}
}
```

**After:**
```json
{
  "fullName": {"type": "string"}  // Renamed
}
```

**Breaking:** ❌ Old consumers expect 'name' field

### Change Field Semantics

**Before:**
```json
{
  "amount": {"type": "integer"}  // Amount in dollars
}
```

**After:**
```json
{
  "amount": {"type": "integer"}  // Amount in cents (changed meaning!)
}
```

**Breaking:** ❌ Same field, different meaning

---

## Schema Versioning

### Semantic Versioning (MAJOR.MINOR.PATCH)

**Format:** `MAJOR.MINOR.PATCH`

**Rules:**
- **MAJOR:** Breaking changes (remove field, change type)
- **MINOR:** Backward-compatible additions (add optional field)
- **PATCH:** Bug fixes (no schema change, just documentation)

**Example:**
```
1.0.0: Initial schema
1.1.0: Add optional 'avatar' field (backward compatible)
1.1.1: Fix typo in description (no schema change)
2.0.0: Remove 'name' field, add 'firstName' and 'lastName' (breaking)
```

---

## Event Naming Conventions

### Format: domain.entity.action

**Structure:**
```
{domain}.{entity}.{action}

Examples:
user.account.created
order.payment.processed
inventory.item.updated
notification.email.sent
```

### Past Tense (Event Already Happened)

```
✅ Good:
user.created
order.placed
payment.processed

❌ Bad:
user.create (present tense)
order.place (imperative)
```

### Specific (Not Too Generic)

```
✅ Good:
user.account.created
user.profile.updated
user.password.reset

❌ Bad:
user.changed (too generic)
user.event (meaningless)
```

---

## Schema Validation

### Producer-Side Validation (Before Publish)

**Example (JavaScript):**
```javascript
const Ajv = require('ajv');
const ajv = new Ajv();

// Get schema from registry
const schema = await schemaRegistry.getSchema('user.created', 'latest');

// Validate event
const validate = ajv.compile(schema);
const event = {
  id: '123',
  email: 'user@example.com',
  name: 'John Doe',
  createdAt: '2024-01-15T10:00:00Z'
};

if (!validate(event)) {
  throw new Error(`Invalid event: ${JSON.stringify(validate.errors)}`);
}

// Publish event
await producer.send({
  topic: 'user-events',
  value: event
});
```

### Consumer-Side Validation (After Receive)

**Example:**
```javascript
consumer.on('message', async (message) => {
  const event = JSON.parse(message.value);
  
  // Get schema from registry
  const schema = await schemaRegistry.getSchema('user.created', event.version);
  
  // Validate event
  const validate = ajv.compile(schema);
  if (!validate(event)) {
    console.error('Invalid event:', validate.errors);
    // Send to Dead Letter Queue
    await dlq.send(message);
    return;
  }
  
  // Process event
  await handleUserCreated(event);
});
```

---

## Schema Discovery

### Searchable Registry UI

**Features:**
- Search schemas by name
- Browse by domain/entity
- View schema details
- See version history

---

## Multi-Environment Schemas

### Dev, Staging, Prod Registries

**Separate Registries:**
```
Dev:     http://schema-registry-dev:8081
Staging: http://schema-registry-staging:8081
Prod:    http://schema-registry-prod:8081
```

**Why Separate:**
- Test schema changes in dev/staging
- Prevent accidental prod changes
- Different schemas in different environments

---

## Schema Governance Workflow

### Step 1: Developer Proposes Schema (PR)

**Process:**
1. Create feature branch
2. Add/update schema file (schemas/user-created.json)
3. Commit and push
4. Create PR

### Step 2: Automated Compatibility Check (CI)

**GitHub Actions:**
```yaml
- name: Check schema compatibility
  run: |
    # Get previous version
    PREV_VERSION=$(curl http://schema-registry:8081/subjects/user.created/versions/latest | jq -r '.version')
    
    # Check compatibility
    curl -X POST http://schema-registry:8081/compatibility/subjects/user.created/versions/$PREV_VERSION \
      -H "Content-Type: application/json" \
      -d @schemas/user-created.json
    
    # Exit if not compatible
    if [ $? -ne 0 ]; then
      echo "Schema is not backward compatible"
      exit 1
    fi
```

### Step 3: Review by Data Team

**Review Checklist:**
- [ ] Follows naming conventions
- [ ] Has description and examples
- [ ] Backward compatible (or justified breaking change)
- [ ] No PII in event name
- [ ] Appropriate data types

### Step 4: Register Schema in Registry

**After Approval:**
```bash
curl -X POST http://schema-registry:8081/subjects/user.created/versions \
  -H "Content-Type: application/json" \
  -d @schemas/user-created.json
```

---

## Dead Letter Queue (DLQ)

### Invalid Events Go to DLQ

**Example:**
```javascript
consumer.on('message', async (message) => {
  try {
    const event = JSON.parse(message.value);
    
    // Validate against schema
    if (!validate(event)) {
      throw new Error('Invalid schema');
    }
    
    await handleEvent(event);
  } catch (err) {
    // Send to DLQ
    await dlq.send({
      topic: 'user-events-dlq',
      value: message.value,
      headers: {
        'error': err.message,
        'original-topic': 'user-events'
      }
    });
  }
});
```

---

## Schema Migration

### Dual Publishing (Old + New Schema)

**Process:**
1. Publish events in both old and new format
2. Consumers migrate to new format
3. Stop publishing old format
4. Remove old schema

---

## Tools and Libraries

### Confluent Schema Registry

**Features:**
- Avro, JSON Schema, Protobuf support
- Compatibility checking
- REST API
- Integration with Kafka

### JSON Schema Validators

**JavaScript:**
```bash
npm install ajv
```

**Python:**
```bash
pip install jsonschema
```

### Avro/Protobuf Libraries

**Avro (JavaScript):**
```bash
npm install avsc
```

**Protobuf (JavaScript):**
```bash
npm install protobufjs
```

---

## Real-World Event Schemas

### Kafka Event Schemas

See examples throughout this document

### Webhook Payloads

**GitHub Webhook:**
```json
{
  "action": "created",
  "issue": {
    "id": 1,
    "number": 1,
    "title": "Bug report",
    "body": "Description"
  },
  "repository": {
    "id": 123,
    "name": "my-repo"
  }
}
```

### CloudEvents Standard

**Format:**
```json
{
  "specversion": "1.0",
  "type": "com.example.user.created",
  "source": "https://example.com/users",
  "id": "A234-1234-1234",
  "time": "2024-01-15T10:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "userId": "123",
    "email": "user@example.com"
  }
}
```

---

## Best Practices

### Schema Design
- [ ] Use consistent naming conventions
- [ ] Use appropriate data types
- [ ] Use semantic versioning
- [ ] Document all fields
- [ ] Provide examples
- [ ] Use backward compatible changes
- [ ] Avoid breaking changes when possible
- [ ] Use optional fields for additions
- [ ] Document breaking changes clearly
- [ ]

### Validation
- [ ] Validate events before publishing
- [ ] Validate events after receiving
- [ ] Use schema registry for validation
- [ ] Send invalid events to DLQ
- [ ] Monitor DLQ for schema violations
- [ ] Fix and replay events
- [ ]

### Versioning
- [ ] Use semantic versioning
- [ ] Tag all releases with version numbers
- [ ] Document version compatibility matrix
- [ ] Maintain backward compatibility
- [ ] Use @deprecated directive for breaking changes
- [ ] Plan schema deprecation strategy
- [ ]

### Documentation
- [ ] Document all breaking changes with dates
- [ ] Document breaking changes clearly
- [ ] Provide migration guides for consumers
- [ ] Document version compatibility
- [ ] Document schema lifecycle
- [ ] Document schema evolution rules
- [ ] Document event naming conventions
- [ ]

### Monitoring
- [ ] Monitor breaking change impacts
- [ ] Track consumer adoption of new schema
- [ ] Set up dashboards for schema health
- [ ] Track migration success rates
- [ ] Monitor DLQ for schema violations
- [ ] Alert on high DLQ rate
- [ ]

### Prevention
- [ ] Use data contracts for all shared data
- [ ] Enforce schema validation at source
- [ ] Implement CI/CD schema checks
- [ ] Use schema registry for validation
- [ ] Use automated compatibility checking
- [ ]

### Testing
- [ ] Test backward compatibility
- [ ] Test with production-like data
- [ ] Test migration scripts thoroughly
- [ ] Test graceful degradation scenarios
- [ ] Monitor test coverage
- [ ] Test schema validation logic
- [ ]

### Governance
- [ ] Establish schema ownership
- [ ] Create schema review process
- [ ] Define schema lifecycle
- [ ] Plan schema deprecation strategy
- [ ] Set up incident response for violations
- [ ] Create data team review board
- [ ] Define schema evolution rules
- [ ]

### Tools
- [ ] Use Confluent Schema Registry for Kafka
- [ ] Use AWS Glue Schema Registry
- [ ] Use Azure Schema Registry
- [ ] Use JSON Schema validators (ajv, jsonschema)
- [ ] Use Avro/Protobuf libraries
- [ ] Use schema registry clients
- [ ]

### Multi-Environment
- [ ] Use separate registries for dev/staging/prod
- [ ] Test schema changes in dev/staging
- [ ] Promote schemas through environments
- [ ] Prevent accidental prod changes
- [ ]

### Checklist
- [ ] Use consistent event naming conventions
- [ ] Use semantic versioning
- [ ] Implement zero-downtime migrations
- [ ] Backfill data before removing old columns
- [ ] Test backward compatibility
- [ ] Have rollback procedures ready
- [ ] Monitor schema drift metrics
- [ ] Track migration success rates
- [ ] Document all breaking changes
- [ ] Set up change notifications
- [ ] Test with production-like data
- [ ] Monitor test coverage
- [ ] Optimize schema validation overhead
- [ ] Cache schema definitions
- [ ] Use efficient validation libraries
- [ ] Monitor schema performance impact
- [ ] Establish schema ownership
- [ ] Create schema review process
- [ ] Define schema lifecycle
- [ ] Plan schema deprecation strategy
- [ ] Set up incident response for violations
- [ ] Test schema validation logic
- [ ] Train team on schema governance
