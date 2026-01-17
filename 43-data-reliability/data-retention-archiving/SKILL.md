---
name: Data Retention and Archiving
description: Strategies for managing the lifecycle of data to balance storage costs, system performance, and legal compliance.
---

# Data Retention and Archiving

## Overview

Data is an asset, but after a certain point, it becomes a liability. **Retention** defines how long you keep data available in primary systems. **Archiving** is the process of moving infrequently accessed data to secondary, low-cost storage.

**Core Principle**: "Delete data you don't need; archive data you might need; protect data you must keep."

---

## 1. Retention vs. Archiving

| Feature | Data Retention | Data Archiving |
| :--- | :--- | :--- |
| **Purpose** | Compliance and daily operations. | Cost reduction and performance. |
| **Location** | Primary Database (SSD, Hot). | Cold Storage (Glacier, Deep Archive). |
| **Access Time** | Milliseconds/Seconds. | Minutes to 12+ Hours. |
| **Integrity** | High (Primary system). | Extremely High (Immutable storage). |

---

## 2. Compliance and Legal Requirements

Different jurisdictions and industries have mandatory minimum retention periods:

*   **GDPR (Right to be Forgotten)**: Must delete personal data when no longer needed or on request.
*   **HIPAA (Healthcare)**: Typically 6-7 years.
*   **SOX (Financial)**: 7 years.
*   **Employment Records**: 3-7 years.

### The "Legal Hold"
In the event of litigation, you must be able to suspend automated deletion policies for specific records immediately.

---

## 3. Storage Tiering and Cost Optimization

Move data to cheaper storage as it ages.

| Tier | AWS Service | GCP Service | Typical Use Case | Cost per GB (approx) |
| :--- | :--- | :--- | :--- | :--- |
| **Hot** | S3 Standard | Standard | Active app data. | $0.023 |
| **Cool** | S3 IA | Nearline | Monthly reports. | $0.0125 |
| **Cold** | Glacier | Coldline | Annual audits. | $0.004 |
| **Frozen** | Deep Archive | Archive | Legal requirements (7-10 yrs) | $0.00099 |

---

## 4. Implementation Strategies

### A. TTL (Time To Live)
Automatically delete records after a set duration.
*   **DynamoDB/Redis**: Direct support for TTL fields.
*   **MongoDB**: TTL indexes.

### B. Partition Dropping (Databases)
For large tables (logs, transactions), partition by date (e.g., `orders_2023_01`).
*   **Action**: Dropping a partition is `O(1)` and much faster/safer than running a massive `DELETE` statement which locks the table.

```sql
-- PostgreSQL example: Drop old data
DROP TABLE IF EXISTS events_p2022_12;
```

### C. Archiving to Apache Parquet
Primary DB (SQL) is expensive for historical reads. 
1. Export 2-year-old data to **Parquet** files on S3.
2. Parquet is compressed and columnar (80-90% smaller than SQL storage).
3. Query via **AWS Athena** or **BigQuery Omni** if needed.

---

## 5. Deletion Strategies: Hard vs. Soft

*   **Soft Delete**: `is_deleted = true`. Data stays in the DB.
    - *Pros*: Easy to undo.
    - *Cons*: Doesn't save cost; DB continues to grow. Doesn't meet GDPR deletion requirements.
*   **Hard Delete**: `DELETE FROM table`. Permanently removed.
    - *Pros*: Real cost savings; compliance met.
    - *Cons*: Irreversible; can be slow on large tables.

---

## 6. Automated Lifecycle Policies

Don't rely on human memory. Use provider policies.

### AWS S3 Lifecycle Configuration
```json
{
  "Rules": [
    {
      "ID": "MoveOldLogs",
      "Status": "Enabled",
      "Prefix": "logs/",
      "Transitions": [
        { "Days": 90, "StorageClass": "GLACIER" }
      ],
      "Expiration": { "Days": 2555 } // Delete after 7 years
    }
  ]
}
```

---

## 7. Data Anonymization before Archiving

If you must keep data for analytics but don't need the identity:
1.  **Masking**: Replace `john@example.com` with `j***@example.com`.
2.  **Hashing**: `SHA256(user_id)`.
3.  **Aggregation**: Store "Total Sales per Zip Code" instead of individual transactions.

---

## 8. Data Re-hydration Strategy

If a regulator asks for data from 5 years ago:
1.  **Request**: Initiate retrieval from S3 Glacier.
2.  **Wait**: 3–5 hours for "Bulk" or "Standard" retrieval.
3.  **Validate**: Verify checksums.
4.  **Export**: Provide data in requested format (CSV/JSON).

---

## 9. Data Retention Checklist

- [ ] **Inventory**: Do we have a list of all data types and their retention periods?
- [ ] **Automation**: Are lifecycle policies enabled for all S3/GCS buckets?
- [ ] **Backup vs. Archive**: Are we clear that backups are for recovery, not long-term storage?
- [ ] **Legal Hold**: Do we have a manual override for the deletion script?
- [ ] **Privacy**: Are we hard-deleting PII within 30 days of a user deletion request?
- [ ] **Cost**: Have we calculated the savings of moving "Cold" data out of RDS/SQL?

---

## Related Skills
- `42-cost-engineering/cloud-cost-models`
- `43-data-reliability/data-quality-monitoring`
- `40-system-resilience/disaster-recovery`
