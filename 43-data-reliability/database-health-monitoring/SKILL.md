---
name: Database Health Monitoring
description: Continuous monitoring and diagnostics for ensuring high availability, performance, and stability of database systems.
---

# Database Health Monitoring

## Overview

Database Health Monitoring is the practice of tracking internal and infrastructure metrics to identify performance bottlenecks, hardware failures, or configuration issues before they cause service outages.

**Core Principle**: "The database is usually the performance bottleneck. Measure everything from disk latency to query locks."

---

## 1. Core Health Metrics (Gold Standard)

Regardless of the database engine, these four areas must be monitored:

| Category | Metric | Critical Threshold |
| :--- | :--- | :--- |
| **Utilization** | CPU Usage | > 80% sustained. |
| **Memory** | Freeable Memory | < 5% of total RAM. |
| **Saturation** | Disk I/O Queue Depth | > 5-10 operations. |
| **Errors** | Connection Failures | Any > 0 per minute. |

---

## 2. Engine-Specific Metrics

### PostgreSQL
*   **Transaction Lag**: Time between primary and replica syncing.
*   **Autovacuum Progress**: Ensuring dead tuples (deleted rows) are cleaned up.
*   **Transaction Wrapper Overrun**: High-risk scenario where the DB stops to prevent data corruption.

### Redis
*   **Memory Fragmentation Ratio**: High fragmentation (> 1.5) means Redis is wasting RAM.
*   **Evicted Keys**: Increasing evictions mean the cache is too small.

### MongoDB
*   **Page Faults**: High faults mean the "Working Set" doesn't fit in RAM.
*   **Write Ticket Availability**: Bottlenecks in the WiredTiger storage engine.

---

## 3. Performance Tuning: The "Explain" Workflow

A healthy database is nothing without efficient queries.

1.  **Detect**: Use "Slow Query Logs" to find queries taking > 500ms.
2.  **Analyze**: Run `EXPLAIN ANALYZE` on the query.
```sql
EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = '123';
```
3.  **Optimize**: 
    - *Missing Index*: Create an index.
    - *Full Table Scan*: Add filters or rewrite query.
    - *Large Join*: Denormalize or use a read replica.

---

## 4. Connection Pool Monitoring

Connection pool exhaustion is a common cause of SEV0 incidents.

*   **Active Connections**: How many threads are currently running a query?
*   **Idle Connections**: How many are "waiting"?
*   **Wait Time**: How long does an application wait to get a connection?

**Strategy**: If `Wait Time > 10ms`, you need to either increase the max connections or fix leaking connections in your code.

---

## 5. Monitoring Tools

| Tool | Focus | Best For |
| :--- | :--- | :--- |
| **Datadog DB Monitoring**| Full Stack | Deep "Explain" plan visibility and DPM (Database Performance Monitoring). |
| **Grafana + Prometheus** | Open Source | Custom dashboards via `postgres_exporter`. |
| **Percona PMM** | SQL Expert | Detailed InnoDB/Postgres internal metrics. |
| **AWS CloudWatch** | Infrastructure | EBS IOPS, RAM, and Burst Credits. |

---

## 6. Critical Alerting Thresholds

Set up your PagerDuty/Slack alerts based on these baselines:

- **Disk Space**: Alert at 85% full. (Critical: DBs usually crash or go read-only at 95%).
- **Replication Lag**: Alert if > 60 seconds. (Critical: Replica data is "stale").
- **Slow Queries**: Alert if `slow_query_count > 10` per minute.
- **CPU Saturation**: Alert if `Load Average > Number of Cores`.

---

## 7. Diagnostic SQL Script (PostgreSQL)

Run this to find currently "blocking" queries (locks):

```sql
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocking_locks.pid AS blocking_pid,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks AS blocked_locks
JOIN pg_catalog.pg_stat_activity AS blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks AS blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity AS blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

---

## 8. Real-World Scenario: The "Zombie" Transaction
*   **Scenario**: A dashboard suddenly stopped updating. CPU and RAM were 10%.
*   **Discovery**: Monitoring showed a **Row Lock** on the main `metrics` table.
*   **Investigation**: An internal script started a transaction to update a row but crashed *before* sending `COMMIT`.
*   **Remediation**: Used the "Blocking Query" script to find the PID (Process ID) of the zombie transaction and ran `SELECT pg_terminate_backend(pid)`.
*   **Outcome**: Lock released, dashboard resumed, 15-minute outage resolved.

---

## 9. Database Health Checklist

- [ ] **Backups**: Have we verified a successful backup restore in the last 30 days?
- [ ] **IOPS**: Are we consistently exceeding 80% of our provisioned IOPS?
- [ ] **Indexes**: Have we run an "Unused Index" report to remove performance overhead?
- [ ] **Alerts**: Do we have an alert for "Max Connections" reaching 90%?
- [ ] **Security**: Are we monitoring for "Failed Login" spikes (Brute force)?
- [ ] **Patches**: Is the DB engine running a supported, minor version update?

---

## Related Skills
* `42-cost-engineering/infra-sizing`
* `43-data-reliability/data-quality-monitoring`
* `41-incident-management/oncall-playbooks`
