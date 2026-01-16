---
name: Lineage and Provenance
description: Track data lineage และ provenance เพื่อเข้าใจ data flow, dependencies และ impact analysis
---

# Lineage and Provenance

## Overview

Track data lineage (ข้อมูลมาจากไหน ไปไหน) และ provenance (ประวัติการเปลี่ยนแปลง) เพื่อเข้าใจ data flow

## Why This Matters

- **Impact analysis**: รู้ว่าการเปลี่ยน table หนึ่งกระทบอะไรบ้าง
- **Debugging**: Trace ย้อนกลับหา root cause
- **Compliance**: Audit trail สำหรับ regulations
- **Trust**: เข้าใจว่า data มาจากไหน

---

## Data Lineage

### Column-Level Lineage
```
users.email
  ↓ (SELECT)
staging.user_profiles.email_address
  ↓ (TRANSFORM: lowercase)
analytics.dim_users.email
  ↓ (JOIN)
analytics.fct_orders.customer_email
```

### Table-Level Lineage
```
Source Tables:
- raw.users
- raw.orders

Transformations:
- staging.user_profiles (dbt model)
- staging.order_details (dbt model)

Analytics Tables:
- analytics.dim_users
- analytics.fct_orders

Dashboards:
- "Sales Dashboard" (uses fct_orders)
- "User Analytics" (uses dim_users)
```

---

## Lineage Tracking

### dbt (Automatic)
```yaml
# models/staging/stg_users.sql
{{ config(
    materialized='view',
    tags=['pii', 'staging']
) }}

SELECT
  id,
  LOWER(email) as email,  -- Lineage: raw.users.email → stg_users.email
  created_at
FROM {{ source('raw', 'users') }}
WHERE deleted_at IS NULL

-- dbt automatically tracks:
-- - Source: raw.users
-- - Target: staging.stg_users
-- - Columns: id, email, created_at
-- - Transformations: LOWER(email)
```

### Manual Tracking
```python
from datahub.emitter.mce_builder import make_lineage_mce

# Track lineage
lineage = make_lineage_mce(
    upstream_urns=[
        "urn:li:dataset:(urn:li:dataPlatform:postgres,raw.users,PROD)"
    ],
    downstream_urn="urn:li:dataset:(urn:li:dataPlatform:postgres,staging.users,PROD)"
)

emitter.emit_mce(lineage)
```

---

## Impact Analysis

```python
def get_downstream_impact(table_name: str) -> list:
    """Get all tables/dashboards affected by changes to this table"""
    
    lineage_graph = build_lineage_graph()
    
    # Find all downstream dependencies
    downstream = []
    queue = [table_name]
    visited = set()
    
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        
        # Get direct downstream
        for dep in lineage_graph.get_downstream(current):
            downstream.append(dep)
            queue.append(dep)
    
    return downstream

# Example
impact = get_downstream_impact('raw.users')
print(f"Changing raw.users will affect:")
for table in impact:
    print(f"- {table}")

# Output:
# - staging.stg_users
# - analytics.dim_users
# - analytics.fct_orders
# - dashboard: "Sales Report"
# - dashboard: "User Analytics"
```

---

## Provenance Tracking

### Change History
```sql
-- Track all changes to data
CREATE TABLE data_provenance (
  id UUID PRIMARY KEY,
  table_name VARCHAR,
  record_id VARCHAR,
  operation VARCHAR,  -- INSERT, UPDATE, DELETE
  changed_by VARCHAR,
  changed_at TIMESTAMP,
  old_values JSONB,
  new_values JSONB
);

-- Example record
{
  "table_name": "users",
  "record_id": "user_123",
  "operation": "UPDATE",
  "changed_by": "etl_job_456",
  "changed_at": "2024-01-16T12:00:00Z",
  "old_values": {"email": "old@example.com"},
  "new_values": {"email": "new@example.com"}
}
```

---

## Tools

```
Lineage Tracking:
- dbt (automatic for dbt models)
- DataHub (LinkedIn)
- Amundsen (Lyft)
- Apache Atlas

Visualization:
- dbt docs (lineage graph)
- DataHub UI
- Custom dashboards
```

---

## Summary

**Lineage:** ข้อมูลมาจากไหน ไปไหน

**Provenance:** ประวัติการเปลี่ยนแปลง

**Use Cases:**
- Impact analysis (ถ้าเปลี่ยน X จะกระทบ Y)
- Root cause analysis (bug มาจากไหน)
- Compliance (audit trail)
- Trust (data quality)

**Tools:**
- dbt (automatic)
- DataHub (metadata)
- Custom tracking
