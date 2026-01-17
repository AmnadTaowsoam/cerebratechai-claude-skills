---
name: Usage-Based Pricing
description: Architecture and implementation strategies for consumption-based billing models in SaaS products.
---

# Usage-Based Pricing (Consumption Billing)

## Overview

Usage-based pricing (UBP) is a billing model where customers pay based on their consumption of a product or service. Unlike fixed subscription models, UBP aligns cost with value for the customer and revenue with infrastructure expense for the provider.

**Core Principle**: "Charge for the value metric most correlated with the user's success (e.g., messages sent, minutes watched, GB stored)."

---

## 1. Usage-Based Pricing Models

| Model | Description | Example |
| :--- | :--- | :--- |
| **Pure Pay-per-use**| Linear cost per unit (e.g., $0.01 per query). | AWS Lambda, Twilio |
| **Tiered (Graduated)**| Cost per unit decreases as volume increases. | Stripe, S3 |
| **Volume-based** | Price for all units changes based on total volume. | Bulk SMS providers |
| **Hybrid** | Fixed base fee + Overage/Usage. | Snowflake, Datadog |

---

## 2. Metering Fundamentals

Metering is the technical process of capturing, aggregating, and reporting usage events.

### What to Meter?
Select a **Value Metric** that is:
1.  **Understandable**: The user knows what they are being charged for.
2.  **Scalable**: It grows as the user's business grows.
3.  **Measurable**: You can track it with 99.999% accuracy.

### Aggregation Methods
*   **Sum**: Total units in a period (e.g., total API calls).
*   **Unique (Count Distinct)**: Total unique items (e.g., monthly active users).
*   **Max (High Water Mark)**: The highest point of usage (e.g., peak concurrent users).
*   **Last**: The value at the end of the period (e.g., current storage size).

---

## 3. Usage Tracking Architecture

Implementation requires an "Event-to-Invoice" pipeline.

### Architecture Diagram (Simplified)
```text
[App Service] --> [Event Bus (Kafka/Kinesis)] --> [Meter Aggregator] --> [Billing DB]
                                                     |
                                                     V
                                             [Stripe/Billing API]
```

### The Reliability Challenge
A billing system must be **Idempotent**. If you process the same usage event twice, you shouldn't charge the customer twice.

---

## 4. Implementation with Stripe Billing

Stripe is the industry standard for metered billing.

### Step 1: Define a Price in Stripe
Use `recurring.usage_type = 'metered'` and `aggregate_usage = 'sum'`.

### Step 2: Reporting Usage (Node.js)
```typescript
import Stripe from 'stripe';
const stripe = new Stripe('sk_test_...');

async function reportUsage(subscriptionItemId: string, usageQuantity: number) {
  const timestamp = Math.floor(Date.now() / 1000);
  
  try {
    await stripe.subscriptionItems.createUsageRecord(
      subscriptionItemId,
      {
        quantity: usageQuantity,
        timestamp: timestamp,
        action: 'increment', // Adds to current period total
      },
      {
        idempotencyKey: `usage-${subscriptionItemId}-${timestamp}`
      }
    );
  } catch (err) {
    console.error('Failed to report usage:', err);
  }
}
```

---

## 5. Predictable Billing (Avoiding "Bill Shock")

Usage-based pricing can be scary for customers. You must provide transparency.

### Guardrails
1.  **Usage Quotas (Hard Limits)**: Stop service when a budget is hit.
2.  **Spending Alerts (Soft Limits)**: Email the user when they hit 50%, 80%, and 100% of their "target" budget.
3.  **Real-Time Dashboard**: Show users their currently accrued bill *before* the invoice is generated.

### Python Example: Checking Quota
```python
def check_quota(user_id, metric, limit):
    current_usage = cache.get(f"usage:{user_id}:{metric}")
    if current_usage >= limit:
        return False, "Quota Exceeded"
    return True, "OK"
```

---

## 6. Unit Economics: Margin Calculation

When implementing UBP, you must track your **Cost of Goods Sold (COGS)** relative to your pricing.

| Metric | Revenue per Unit | COGS per Unit | Contribution Margin |
| :--- | :--- | :--- | :--- |
| **API Call** | $0.05 | $0.002 (Compute) | 96% |
| **LLM Inference**| $0.15 | $0.10 (GPU/Token) | 33% |
| **Storage** | $0.08 | $0.02 (S3) | 75% |

*If your LLM margin is too low, you need to either raise prices or optimize inference (see `llm-cost-optimization`).*

---

## 7. Metering Infrastructure Tools

1.  **Lago**: Open-source metering and billing engine.
2.  **Metronome**: Enterprise usage-based billing platform.
3.  **Orb**: Flexible pricing and usage management.
4.  **Apache Flink**: For high-volume streaming aggregation.

---

## 8. Real-world Examples

### Twilio (Pure Pay-per-use)
- **Metric**: Number of SMS segments or voice minutes.
- **Why it works**: Cost is almost entirely external (carrier fees), so the price must scale exactly with usage.

### Datadog (Hybrid)
- **Metric**: Number of hosts (fixed) + GB of logs (metered).
- **Why it works**: Captures value from both infra scale and data scale.

### Snowflake (Credit-based)
- **Metric**: "Credits" based on virtual warehouse size and uptime.
- **Why it works**: Simplifies complex compute cost into a single abstract currency.

---

## 9. Implementation Checklist

- [ ] **Idempotency**: Do usage events have a unique ID to prevent double-billing?
- [ ] **Precision**: Does the aggregator handle floating point math correctly (no rounding errors)?
- [ ] **Delay/Latency**: How long does it take for usage in the app to appear on the dashboard? (Target: < 5 mins).
- [ ] **Backfill**: Can you re-process events if the billing pipeline fails?
- [ ] **Limits**: Are there spending caps to protect customers from accidental "infinite loops"?
- [ ] **Margin**: Have you calculated the infrastructure cost of 1 million units of the metric?

---

## Related Skills
- `42-cost-engineering/cloud-cost-models`
- `42-cost-engineering/cost-observability`
- `45-product-thinking/pricing-strategies`
