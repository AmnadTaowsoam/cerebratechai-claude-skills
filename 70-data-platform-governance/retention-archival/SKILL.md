---
name: Retention and Archival
description: Policy และ automation สำหรับ data retention, archival และ deletion ตาม compliance requirements
---

# Retention and Archival

## Overview

Policy และ automation สำหรับ data retention (เก็บนานแค่ไหน), archival (ย้ายไป cold storage) และ deletion (ลบทิ้ง)

## Why This Matters

- **Compliance**: GDPR, CCPA retention limits
- **Cost**: Cold storage ถูกกว่า hot storage
- **Performance**: น้อย data = query เร็วขึ้น
- **Legal**: Right to deletion

---

## Retention Policy

```yaml
# retention-policy.yaml
policies:
  - table: users
    retention: 7 years
    reason: Legal requirement
    archive_after: 2 years
    delete_after: 7 years
  
  - table: logs
    retention: 90 days
    reason: Operational needs
    archive_after: 30 days
    delete_after: 90 days
  
  - table: analytics_events
    retention: 2 years
    reason: Business analytics
    archive_after: 6 months
    delete_after: 2 years
```

---

## Automated Archival

```python
# Archive old data to S3
def archive_old_data(table_name: str, cutoff_days: int):
    cutoff_date = datetime.now() - timedelta(days=cutoff_days)
    
    # Export to S3
    query = f"""
        COPY (
            SELECT * FROM {table_name}
            WHERE created_at < '{cutoff_date}'
        )
        TO 's3://archive-bucket/{table_name}/{cutoff_date.year}/'
        WITH (FORMAT PARQUET, COMPRESSION GZIP)
    """
    db.execute(query)
    
    # Delete from hot storage
    db.execute(f"""
        DELETE FROM {table_name}
        WHERE created_at < '{cutoff_date}'
    """)
    
    print(f"Archived {table_name} data older than {cutoff_days} days")

# Schedule daily
schedule.every().day.at("02:00").do(archive_old_data, 'logs', 30)
```

---

## Deletion Policy

```python
# Right to deletion (GDPR)
def delete_user_data(user_id: str):
    """Delete all user data across all tables"""
    
    tables_with_user_data = [
        'users',
        'orders',
        'analytics_events',
        'audit_logs'
    ]
    
    for table in tables_with_user_data:
        db.execute(f"""
            DELETE FROM {table}
            WHERE user_id = '{user_id}'
        """)
    
    # Log deletion
    audit_log.write({
        'action': 'user_data_deletion',
        'user_id': user_id,
        'timestamp': datetime.now(),
        'tables_affected': tables_with_user_data
    })
    
    print(f"Deleted all data for user {user_id}")
```

---

## Lifecycle Management

```sql
-- Partition by date for easy archival
CREATE TABLE logs (
  id UUID,
  message TEXT,
  created_at TIMESTAMP
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE logs_2024_01 PARTITION OF logs
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Drop old partitions (fast deletion)
DROP TABLE logs_2023_01;  -- Deletes entire month instantly
```

---

## Summary

**Retention:** เก็บ data นานแค่ไหน

**Archival:** ย้ายไป cold storage (S3, Glacier)

**Deletion:** ลบตาม policy หรือ user request

**Automation:**
- Scheduled archival jobs
- Partition-based deletion
- Audit logging

**Compliance:**
- GDPR (right to deletion)
- Data retention limits
- Audit trails
