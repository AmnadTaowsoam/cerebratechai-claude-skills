---
name: Database Transactions
description: Comprehensive guide to database transactions, ACID properties, isolation levels, locking, and distributed transactions.
---

# Database Transactions

## Overview

Database transactions are fundamental to maintaining data integrity and consistency in applications. They provide a way to group multiple operations into a single unit of work that either succeeds completely or fails completely, following the ACID principles.

## Prerequisites

- Understanding of SQL and database operations
- Knowledge of database systems (PostgreSQL, MySQL, etc.)
- Familiarity with concurrency concepts
- Basic understanding of distributed systems

## Key Concepts

### What are Database Transactions?

Database transactions are:
- **Atomic**: All operations succeed or none do
- **Consistent**: Database moves from valid state to valid state
- **Isolated**: Transactions don't interfere with each other
- **Durable**: Committed changes persist

### ACID Properties

#### Atomicity

Atomicity ensures that all operations within a transaction are treated as a single unit. Either all operations succeed, or none do.

```sql
-- Example: Transfer money between accounts
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- Both updates succeed or both fail
```

If the second UPDATE fails, the first UPDATE is rolled back automatically.

#### Consistency

Consistency ensures that a transaction brings the database from one valid state to another valid state, maintaining all database rules and constraints.

```sql
-- Example: Ensuring business rules
BEGIN TRANSACTION;

-- Check if sufficient balance
SELECT balance FROM accounts WHERE id = 1 FOR UPDATE;
-- If balance < 100, ROLLBACK

-- Perform transfer
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Verify no negative balances
SELECT COUNT(*) FROM accounts WHERE balance < 0;
-- If count > 0, ROLLBACK

COMMIT;
```

#### Isolation

Isolation ensures that concurrent transactions don't interfere with each other. Each transaction sees a consistent snapshot of the database.

```sql
-- Transaction 1
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT balance FROM accounts WHERE id = 1;  -- Reads $1000

-- Transaction 2 (concurrent)
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance + 500 WHERE id = 1;
COMMIT;  -- Updates to $1500

-- Transaction 1 continues
SELECT balance FROM accounts WHERE id = 1;  -- Still reads $1000
COMMIT;
```

#### Durability

Durability ensures that once a transaction is committed, it remains permanent even in the event of a system failure.

```sql
BEGIN TRANSACTION;
INSERT INTO orders (user_id, total) VALUES (1, 100.00);
COMMIT;  -- This data is permanently stored
-- Even if server crashes after this, the data is preserved
```

## Implementation Guide

### Transaction Lifecycle

#### BEGIN

Starts a new transaction.

```sql
BEGIN;
-- or
BEGIN TRANSACTION;
-- or
START TRANSACTION;
```

#### COMMIT

Permanently saves all changes made in the transaction.

```sql
BEGIN;
UPDATE users SET email = 'new@example.com' WHERE id = 1;
COMMIT;  -- Changes are now permanent
```

#### ROLLBACK

Undoes all changes made in the transaction.

```sql
BEGIN;
UPDATE users SET email = 'new@example.com' WHERE id = 1;
ROLLBACK;  -- Changes are discarded
```

#### Transaction Lifecycle Example

```sql
-- 1. Begin transaction
BEGIN;

-- 2. Execute operations
UPDATE inventory SET quantity = quantity - 1 WHERE product_id = 1;
INSERT INTO orders (product_id, quantity) VALUES (1, 1);

-- 3. Check conditions
IF (SELECT quantity FROM inventory WHERE product_id = 1) < 0 THEN
    ROLLBACK;  -- Insufficient inventory
ELSE
    COMMIT;    -- Success
END IF;
```

### Isolation Levels

#### READ UNCOMMITTED

The lowest isolation level. Transactions can read uncommitted changes from other transactions.

```sql
SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
BEGIN;
SELECT * FROM accounts WHERE id = 1;  -- Can read uncommitted data
COMMIT;
```

**Characteristics:**
- Allows dirty reads
- Allows non-repeatable reads
- Allows phantom reads
- Highest concurrency, lowest consistency

**When to use:**
- Rarely used in practice
- Only when performance is critical and dirty reads are acceptable

#### READ COMMITTED

Default isolation level in PostgreSQL and SQL Server. Transactions can only read committed changes.

```sql
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
BEGIN;
SELECT * FROM accounts WHERE id = 1;  -- Only reads committed data
COMMIT;
```

**Characteristics:**
- Prevents dirty reads
- Allows non-repeatable reads
- Allows phantom reads
- Good balance between consistency and performance

**When to use:**
- Most applications
- When you need to see committed changes from other transactions

#### REPEATABLE READ

Default isolation level in MySQL. Transactions see a consistent snapshot from the start of the transaction.

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
BEGIN;
SELECT * FROM accounts WHERE id = 1;  -- Consistent snapshot
-- Even if other transactions commit changes, you won't see them
COMMIT;
```

**Characteristics:**
- Prevents dirty reads
- Prevents non-repeatable reads
- Allows phantom reads (in MySQL, prevents phantoms)
- Good for reporting and analytics

**When to use:**
- When you need consistent reads throughout a transaction
- Reporting queries
- When non-repeatable reads would cause issues

#### SERIALIZABLE

The highest isolation level. Transactions are completely isolated from each other.

```sql
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
BEGIN;
SELECT * FROM accounts WHERE id = 1;  -- Complete isolation
COMMIT;
```

**Characteristics:**
- Prevents dirty reads
- Prevents non-repeatable reads
- Prevents phantom reads
- Lowest concurrency, highest consistency
- May cause serialization failures

**When to use:**
- Critical financial operations
- When absolute consistency is required
- When phantom reads would cause issues

### Locking Mechanisms

#### Pessimistic Locking

Locks resources before accessing them, assuming conflicts will occur.

```sql
-- SELECT FOR UPDATE - Locks rows for update
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
-- This row is now locked, other transactions must wait

-- Do some processing
-- ...

UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;  -- Lock is released
```

**SELECT FOR SHARE (PostgreSQL) / SELECT FOR SHARE (MySQL):**

```sql
BEGIN;
SELECT * FROM accounts WHERE id = 1 FOR SHARE;
-- Other transactions can also read with FOR SHARE
-- But cannot update until this transaction commits
COMMIT;
```

**Advantages:**
- Guarantees data consistency
- Easy to understand
- Good for high-contention scenarios

**Disadvantages:**
- Can cause deadlocks
- Reduces concurrency
- May cause performance issues

#### Optimistic Locking

Assumes conflicts are rare and checks for conflicts before committing.

```sql
-- Add version column
ALTER TABLE accounts ADD COLUMN version INT DEFAULT 0;

-- Update with version check
UPDATE accounts
SET balance = balance - 100, version = version + 1
WHERE id = 1 AND version = 5;

-- Check if update succeeded
IF ROW_COUNT() = 0 THEN
    -- Conflict occurred, handle it
    ROLLBACK;
END IF;
```

**Using Timestamps:**

```sql
-- Add updated_at column
ALTER TABLE accounts ADD COLUMN updated_at TIMESTAMP;

-- Update with timestamp check
UPDATE accounts
SET balance = balance - 100, updated_at = NOW()
WHERE id = 1 AND updated_at = '2024-01-01 10:00:00';

-- Check if update succeeded
IF ROW_COUNT() = 0 THEN
    -- Conflict occurred
    ROLLBACK;
END IF;
```

**Advantages:**
- No locks, higher concurrency
- Better performance in low-contention scenarios
- No deadlocks

**Disadvantages:**
- Need to handle conflicts
- Extra column required
- More complex error handling

### Row-Level vs Table-Level Locks

#### Row-Level Locks

Locks individual rows, allowing concurrent access to other rows in the same table.

```sql
BEGIN;
-- Lock specific row
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;

-- Other rows in table are still accessible
SELECT * FROM accounts WHERE id = 2;  -- This works fine
COMMIT;
```

**When to use:**
- Most application scenarios
- High concurrency requirements
- When conflicts are localized to specific rows

#### Table-Level Locks

Locks entire table, preventing any concurrent access.

```sql
BEGIN;
-- Lock entire table
LOCK TABLE accounts IN EXCLUSIVE MODE;

-- No other transaction can access this table
SELECT * FROM accounts WHERE id = 1;  -- Only this transaction
COMMIT;
```

**Lock Modes:**
- `ACCESS SHARE`: SELECT
- `ROW SHARE`: SELECT FOR UPDATE
- `ROW EXCLUSIVE`: INSERT, UPDATE, DELETE
- `SHARE UPDATE EXCLUSIVE`: VACUUM, ANALYZE
- `SHARE`: CREATE INDEX CONCURRENTLY
- `SHARE ROW EXCLUSIVE`: LOCK TABLE
- `EXCLUSIVE`: REFRESH MATERIALIZED VIEW CONCURRENTLY
- `ACCESS EXCLUSIVE`: DROP TABLE, TRUNCATE, ALTER TABLE

**When to use:**
- Bulk operations
- Schema changes
- When you need exclusive access to all data

### Savepoints

Savepoints allow you to rollback to a specific point within a transaction without rolling back the entire transaction.

```sql
BEGIN;

-- First operation
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
SAVEPOINT sp1;

-- Second operation
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- If second operation fails, rollback to savepoint
-- ROLLBACK TO sp1;

-- Continue with other operations
UPDATE accounts SET balance = balance + 50 WHERE id = 3;

COMMIT;
```

**Multiple Savepoints:**

```sql
BEGIN;

-- Operation 1
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
SAVEPOINT sp1;

-- Operation 2
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
SAVEPOINT sp2;

-- If operation 2 fails, rollback to sp1
-- ROLLBACK TO sp1;

-- Try alternative operation 2
UPDATE accounts SET balance = balance + 50 WHERE id = 2;

COMMIT;
```

**Releasing Savepoints:**

```sql
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
SAVEPOINT sp1;

UPDATE accounts SET balance = balance + 100 WHERE id = 2;
RELEASE SAVEPOINT sp1;  -- Savepoint is released

-- Can't rollback to sp1 anymore
-- ROLLBACK TO sp1;  -- Error!
COMMIT;
```

### Deadlock Detection and Prevention

#### What is Deadlock?

A deadlock occurs when two or more transactions are waiting for each other's locks.

```
Transaction 1: Locks row A, waiting for row B
Transaction 2: Locks row B, waiting for row A
```

#### Deadlock Example

```sql
-- Transaction 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Locks row 1
-- Waiting for row 2...
UPDATE accounts SET balance = balance + 100 WHERE id = 2;

-- Transaction 2 (concurrent)
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 2;  -- Locks row 2
-- Waiting for row 1...
UPDATE accounts SET balance = balance + 100 WHERE id = 1;

-- DEADLOCK! Both transactions are waiting for each other
```

#### Deadlock Prevention

**Consistent Lock Ordering:**

```sql
-- Always lock rows in the same order (e.g., by ID)
-- Transaction 1
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Lower ID first
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;

-- Transaction 2
BEGIN;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;  -- Same order
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

**Lock Timeout:**

```sql
-- Set lock timeout
SET lock_timeout = '5s';  -- PostgreSQL
-- or
SET innodb_lock_wait_timeout = 5;  -- MySQL

BEGIN;
-- If lock can't be acquired within 5 seconds, error is raised
SELECT * FROM accounts WHERE id = 1 FOR UPDATE;
COMMIT;
```

**Short Transactions:**

```sql
-- Keep transactions as short as possible
BEGIN;
-- Only necessary operations
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
COMMIT;

-- Do processing outside transaction
-- ...

BEGIN;
-- Final update
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

#### Handling Deadlocks

```javascript
// Application-level retry logic
async function transferMoney(fromId, toId, amount) {
  const maxRetries = 3;
  let attempt = 0;

  while (attempt < maxRetries) {
    try {
      await db.transaction(async (trx) => {
        await trx('accounts')
          .where('id', fromId)
          .update('balance', db.raw('balance - ?', [amount]));

        await trx('accounts')
          .where('id', toId)
          .update('balance', db.raw('balance + ?', [amount]));
      });
      return;  // Success
    } catch (error) {
      if (error.code === '40P01') {  // Deadlock error code
        attempt++;
        await sleep(100 * attempt);  // Exponential backoff
      } else {
        throw error;  // Other errors
      }
    }
  }

  throw new Error('Max retries exceeded');
}
```

### Transaction Timeout and Retry

#### Setting Timeouts

**PostgreSQL:**

```sql
-- Statement timeout
SET statement_timeout = '30s';

-- Lock timeout
SET lock_timeout = '5s';

-- Idle in transaction timeout
SET idle_in_transaction_session_timeout = '10min';
```

**MySQL:**

```sql
-- Lock wait timeout
SET innodb_lock_wait_timeout = 5;

-- Transaction read-only timeout
SET tx_read_only = 1;
```

#### Retry Logic

```javascript
class TransactionRetry {
  constructor(options = {}) {
    this.maxRetries = options.maxRetries || 3;
    this.retryDelay = options.retryDelay || 100;
    this.backoffMultiplier = options.backoffMultiplier || 2;
  }

  async execute(fn) {
    let attempt = 0;
    let lastError;

    while (attempt < this.maxRetries) {
      try {
        return await fn();
      } catch (error) {
        lastError = error;

        if (this.isRetryableError(error)) {
          attempt++;
          const delay = this.retryDelay * Math.pow(this.backoffMultiplier, attempt - 1);
          await this.sleep(delay);
        } else {
          throw error;
        }
      }
    }

    throw lastError;
  }

  isRetryableError(error) {
    const retryableCodes = [
      '40P01',  // Deadlock
      '40001',  // Serialization failure
      '08006',  // Connection failure
    ];
    return retryableCodes.includes(error.code);
  }

  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Usage
const retry = new TransactionRetry({ maxRetries: 3 });

await retry.execute(async () => {
  await db.transaction(async (trx) => {
    // Transaction operations
  });
});
```

### Transaction Patterns in ORMs

#### Prisma

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// Simple transaction
await prisma.$transaction(async (tx) => {
  await tx.account.update({
    where: { id: 1 },
    data: { balance: { decrement: 100 } },
  });

  await tx.account.update({
    where: { id: 2 },
    data: { balance: { increment: 100 } },
  });
});

// Interactive transaction with retries
await prisma.$transaction(
  async (tx) => {
    const account = await tx.account.findUnique({
      where: { id: 1 },
    });

    if (account.balance < 100) {
      throw new Error('Insufficient balance');
    }

    await tx.account.update({
      where: { id: 1 },
      data: { balance: { decrement: 100 } },
    });
  },
  {
    maxWait: 5000,    // Max time to wait for transaction
    timeout: 10000,   // Max time for transaction to run
    isolationLevel: Prisma.TransactionIsolationLevel.Serializable,
  }
);
```

#### TypeORM

```typescript
import { DataSource, IsolationLevel } from 'typeorm';

const dataSource = new DataSource({ /* ... */ });

// Simple transaction
await dataSource.transaction(async (manager) => {
  await manager.update(Account, 1, {
    balance: () => `balance - 100`,
  });

  await manager.update(Account, 2, {
    balance: () => `balance + 100`,
  });
});

// Transaction with options
await dataSource.transaction({
  isolationLevel: IsolationLevel.REPEATABLE_READ,
}, async (manager) => {
  // Transaction operations
});

// Manual transaction control
const queryRunner = dataSource.createQueryRunner();
await queryRunner.connect();
await queryRunner.startTransaction();

try {
  await queryRunner.manager.update(Account, 1, {
    balance: () => `balance - 100`,
  });

  await queryRunner.manager.update(Account, 2, {
    balance: () => `balance + 100`,
  });

  await queryRunner.commitTransaction();
} catch (error) {
  await queryRunner.rollbackTransaction();
  throw error;
} finally {
  await queryRunner.release();
}
```

#### SQLAlchemy (Python)

```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

engine = create_engine('postgresql://user:pass@localhost/db')
Session = sessionmaker(bind=engine)

# Simple transaction
with Session() as session:
    try:
        session.execute(
            text("UPDATE accounts SET balance = balance - 100 WHERE id = 1")
        )
        session.execute(
            text("UPDATE accounts SET balance = balance + 100 WHERE id = 2")
        )
        session.commit()
    except Exception as e:
        session.rollback()
        raise

# Transaction with isolation level
with Session() as session:
    session.execute(
        text("SET TRANSACTION ISOLATION LEVEL REPEATABLE READ")
    )
    session.begin()
    try:
        # Transaction operations
        session.commit()
    except Exception as e:
        session.rollback()
        raise

# Nested transactions (savepoints)
with Session() as session:
    session.begin_nested()
    try:
        # Nested operations
        session.commit()
    except Exception as e:
        session.rollback()
        raise
```

## Best Practices

1. **Transaction Design**
   - Keep transactions as short as possible
   - Only include necessary operations
   - Avoid user interaction within transactions
   - Use appropriate isolation levels

2. **Error Handling**
   - Always handle transaction errors
   - Implement retry logic for transient failures
   - Log transaction failures for debugging
   - Rollback on errors

3. **Performance**
   - Use row-level locks when possible
   - Avoid long-running transactions
   - Monitor lock contention
   - Use connection pooling

4. **Testing**
   - Test transaction rollback scenarios
   - Test concurrent access
   - Test deadlock handling
   - Test isolation levels

5. **Distributed Transactions**
   - Consider Saga pattern for microservices
   - Use 2PC only when necessary
   - Be aware of performance implications
   - Have compensation logic ready

## Related Skills

- [`04-database/database-optimization`](04-database/database-optimization/SKILL.md)
- [`04-database/database-locking`](04-database/database-locking/SKILL.md)
- [`09-microservices/saga-pattern`](09-microservices/saga-pattern/SKILL.md)
- [`04-database/connection-pooling`](04-database/connection-pooling/SKILL.md)
