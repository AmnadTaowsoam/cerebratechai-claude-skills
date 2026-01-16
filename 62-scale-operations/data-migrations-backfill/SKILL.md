---
name: Data Migrations & Backfill
description: Zero-downtime patterns for production schema changes and large backfills, including expand/contract, batching, verification, and rollback strategies
---

# Data Migrations & Backfill

## Overview

Production migrations are operational changes, not just SQL. The goal is to ship schema + code changes safely, keep latency stable, and prove correctness with observability and verification.

## Why This Matters

- **Zero downtime**: avoid breaking reads/writes during deploys
- **Integrity**: prevent silent corruption and partial backfills
- **Reversibility**: fast rollback path when reality differs from plan
- **Scale**: millions of rows without timeouts or lock storms

---

## Core Concepts

### 1. Schema Migration Patterns

- Prefer additive changes first: `ADD COLUMN NULL`, `ADD INDEX CONCURRENTLY` (Postgres), `ADD CONSTRAINT NOT VALID` + `VALIDATE CONSTRAINT` (Postgres).
- Treat renames/splits as “add new → dual write → switch reads → remove old” (never “rename in place” if clients may be on mixed versions).
- Every new constraint has an “enforcement time”: validate in a controlled window, not during peak.

### 2. Zero-Downtime Strategies

- **Expand/Contract**: keep old + new schemas compatible across multiple deployments.
- **Dual writes**: write to both representations, but read from one until verified.
- **Feature flags**: gate read-path cutovers and new write behaviors.
- **Compatibility window**: assume old app versions can run for at least one deploy cycle.

### 3. Backfill Patterns

- **Batch + checkpoint**: small batches with persisted cursor (e.g., last `id`, `(created_at,id)` tuple).
- **Idempotent writes**: safe to retry; use deterministic transforms and `WHERE new_col IS NULL` guards.
- **Throttle + pause**: dynamic rate limits, backpressure on DB load/replication lag.
- **Sharded backfills**: split by tenant, hash ranges, or time partitions for parallelism.

### 4. Data Transformation & Verification

- Define invariants upfront (counts, sums, uniqueness, “old == new” mapping).
- Verify with **sampling** + **full aggregate checks** (cheap aggregates + targeted deep checks).
- Consider dual-read compare (shadow reads) before switching primary reads.

### 5. Rollback Strategies

- Rollback is usually **application-first**, not schema-first: revert read-path flag, stop dual write, stop backfill.
- Avoid irreversible DDL in the critical path (drops, destructive type changes).
- Track migration state explicitly (table/row storing phase + cursor + last success timestamp).

### 6. Large Table & Online DDL

- Postgres: avoid long `ALTER TABLE` rewrites; use `CREATE INDEX CONCURRENTLY`; prefer `NOT VALID` constraints + validate later.
- MySQL: use online schema change tools (`gh-ost`, `pt-online-schema-change`) for heavy ops.
- Plan for replication lag, statement timeouts, lock timeouts, and maintenance windows.

### 7. Cross-Database / Storage Migrations

- Use **dual write** + **backfill** + **cutover** (reads switch) + **decommission**.
- Decide on cutover mode: **stop-the-world** (short maintenance) vs **eventual consistency** (reconciliation loop).
- Build reconciliation: periodic diffs, checksums, and replay of missed writes.

### 8. Migration Testing

- Run on a production-like snapshot (size + distribution matters more than schema).
- Load test the backfill job (DB CPU, locks, buffer cache, replica lag).
- Validate rollback playbook in staging: “flip flag → stop job → revert deploy”.

## Quick Start (Expand/Contract + Backfill)

1. **Expand**: add new nullable column/index (safe DDL) and deploy code that can read/write both.
2. **Backfill**: run a batched idempotent job with a checkpoint.
3. **Verify**: aggregates + sampling + dashboards; optionally shadow reads.
4. **Switch reads**: flip feature flag to read from new column/table.
5. **Contract**: enforce constraints, remove dual write, then drop old column/table later.

```typescript
type Cursor = { lastId: number };

export async function backfillUsers(db: any, cursor: Cursor, batchSize = 1000) {
  for (;;) {
    const rows: Array<{ id: number }> = await db.query(
      `SELECT id FROM users WHERE id > $1 AND new_col IS NULL ORDER BY id LIMIT $2`,
      [cursor.lastId, batchSize],
    );
    if (rows.length === 0) break;

    const ids = rows.map((r) => r.id);
    await db.query(`UPDATE users SET new_col = compute_new_col(old_col) WHERE id = ANY($1)`, [ids]);

    cursor.lastId = rows[rows.length - 1].id;
    await db.query(`UPDATE migration_state SET cursor = $1, updated_at = NOW() WHERE name = 'users_new_col'`, [
      JSON.stringify(cursor),
    ]);
  }
}
```

## Production Checklist

- [ ] DDL reviewed for locks/rewrites (and has `lock_timeout` / safe settings)
- [ ] Compatibility window planned (old/new app versions can run together)
- [ ] Backfill is batched, resumable, and idempotent (safe to retry)
- [ ] Metrics + logs + alerting exist (rate, errors, lag, ETA, DB load)
- [ ] Verification plan exists (aggregates + sampling + invariants)
- [ ] Rollback plan is executable (flags, deploy steps, job stop)

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| Prisma Migrate / Flyway / Liquibase | Schema migrations with history |
| Alembic | Python migrations |
| `gh-ost` / `pt-online-schema-change` | MySQL online schema changes |
| `pg_repack` | Postgres table maintenance/rewrites |
| Feature flag system | Read-path cutovers + kill switches |

## Anti-patterns

1. **Big bang migration**: change schema + code in one deploy with no compatibility window
2. **One huge transaction**: backfilling millions of rows in a single write
3. **Destructive DDL early**: dropping columns/tables before traffic is fully cut over
4. **No verification**: “job finished” ≠ “data is correct”

## Real-World Examples

### Example: Column Rename (Zero-Downtime)

1. Add `new_name` nullable.
2. Deploy dual write (`old_name` + `new_name`).
3. Backfill `new_name` for existing rows.
4. Switch reads to `new_name` (flag).
5. Remove `old_name` later (contract phase).

### Example: Large Table Backfill (Throttled)

- Batch by monotonic key; cap runtime per batch; sleep/backoff on DB pressure.
- Add “pause” control and alert on replica lag and deadlocks.

### Example: Database Switch (Dual Write)

- Writes go to DB-A + DB-B; reconciliation job compares diffs; reads switch to DB-B after SLO + correctness validation; DB-A becomes read-only before decomission.

## Common Mistakes

1. Adding `NOT NULL` (or validating constraints) during peak traffic without a plan
2. Dropping columns that are still referenced by older app versions or background jobs
3. Backfilling without a durable checkpoint (cannot resume safely)
4. Running migrations without dashboards/alerts for lock waits, replication lag, and error rates

## Integration Points

- CI/CD (migration ordering, gated deploys, maintenance windows)
- Background job system (batch workers, retries, idempotency keys)
- Observability stack (metrics, dashboards, alerts)
- Feature flags / config management (phased cutovers)

## Further Reading

- [Zero-Downtime Migrations (Stripe)](https://stripe.com/blog/online-migrations)
- [Evolutionary Database Design](https://martinfowler.com/articles/evodb.html)
- [gh-ost](https://github.com/github/gh-ost)
