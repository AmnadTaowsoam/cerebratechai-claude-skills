---
name: Data Contracts
description: Implementing formal agreements between data producers and consumers to ensure data reliability and stability.
---

# Data Contracts

## Overview

A Data Contract is a formal agreement between a data producer (e.g., a microservice) and a data consumer (e.g., a data platform) that defines the structure, semantics, and quality of the data being shared. It acts as a "service-level agreement" (SLA) for data.

**Core Principle**: "Data should be treated as a product, and products need specifications."

---

## 1. Why Data Contracts Matter

In traditional systems, downstream data pipelines often break when an upstream software engineer changes a database field name or format. Data contracts shift the responsibility to the producer.

| Benefit | Description |
| :--- | :--- |
| **Stability** | Upstream changes don't break downstream dashboards/ML models. |
| **Accountability** | Producers are responsible for the data quality of their events. |
| **Efficiency** | Data engineers spend less time "fixing" broken pipelines. |
| **Security** | Fine-grained control over PII and sensitive data. |

---

## 2. Components of a Data Contract

A comprehensive contract covers four main areas:

1.  **Schema**: The structure (fields, types, nested objects).
2.  **Semantics**: The meaning of the data (e.g., "Price" must be in USD).
3.  **Quality**: Expected values (e.g., "user_id" cannot be null, "age" > 18).
4.  **SLA**: Performance expectations (e.g., "Data will arrive within 5 minutes of the event").

---

## 3. Data Contract Implementation (YAML Standard)

Data contracts are typically defined in a machine-readable format like YAML or JSON.

```yaml
# customer_onboarded_contract.yaml
contract_id: "order-service.customer-v1"
owner: "order-processing-team"
version: "1.0.2"

schema:
  type: record
  fields:
    - name: customer_id
      type: string
      description: "Unique UUID for the customer"
    - name: email
      type: string
      pattern: "^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$"
    - name: tier
      type: enum
      symbols: ["FREE", "PRO", "ENTERPRISE"]

quality:
  - assertion: "all_values_unique(customer_id)"
  - assertion: "no_nulls(tier)"
  - assertion: "column_value_ranges(age, 18, 120)"

sla:
  freshness: "15 minutes"
  availability: "99.9%"
```

---

## 4. Enforcement Strategy

### A. Producer-Side Validation (The "Gatekeeper")
Validation happens *before* the data is published to a message bus (Kafka/Kinesis).

```typescript
// Example: Validating a message against a contract in Node.js
import { validate } from 'data-contract-validator';

async function publishEvent(event: any) {
  const result = await validate('order-service.customer-v1', event);
  
  if (!result.isValid) {
    // Block the deployment or alert the producer
    throw new Error(`Data Contract Violation: ${result.errors}`);
  }
  
  await kafka.send(event);
}
```

### B. CI/CD Integration
Run contract checks during Pull Requests. If a PR changes a field specified in a contract, the build fails until the contract is versioned.

---

## 5. Schema Evolution and Versioning

Contracts must follow **Semantic Versioning (SemVer)**:
*   **PATCH**: Adding an optional field.
*   **MINOR**: Adding a mandatory field with a default value.
*   **MAJOR**: Deleting a field, renaming a field, or changing a data type.

### Backwards Compatibility
A data platform should always be able to process `v1.0.0` data even if `v1.5.0` is released.

---

## 6. Tools for Data Contracts

1.  **Aclaro**: Lightweight data contract management.
2.  **Gable**: Data contract platform for monitoring and enforcement.
3.  **Confluent Schema Registry**: For Kafka-based schema enforcement.
4.  **Great Expectations**: For defining data quality assertions within a contract.
5.  **Deequ**: Unit testing for data (Amazon).

---

## 7. The Lifecycle of a Data Contract

1.  **Discovery**: Consumer requests a specific data set.
2.  **Definition**: Producer and Consumer co-create the YAML contract.
3.  **Validation**: Producer implements automated checks.
4.  **Monitoring**: Ongoing observability of contract compliance.
5.  **Evolution**: Negotiated changes to the contract for new features.

---

## 8. Real-World Case Study: Fintech Startup
*   **Problem**: Monthly financial reports were inaccurate because the `transaction_service` changed "currency" from a 3-letter code (`USD`) to a numeric code (`840`).
*   **Solution**: Implemented YAML-based contracts for all transaction events.
*   **Outcome**: The `transaction_service` team was alerted *during local testing* that their change would break the data contract. The code was corrected before reaching production.

---

## 9. Data Contract Checklist

* [ ] **Owner**: Is there a specific team responsible for this contract?
* [ ] **PII Identification**: Are sensitive fields (SSN, Email) tagged for encryption?
* [ ] **Validation**: Is the data validated *at the source*?
* [ ] **Alerting**: Does the consumer get alerted if an SLA (Freshness) is breached?
* [ ] **Documentation**: Is the `description` field filled out for every column?

---

## Related Skills
* `43-data-reliability/schema-management`
* `43-data-reliability/data-quality-monitoring`
* `41-incident-management/incident-triage` (contract violations are incidents)
