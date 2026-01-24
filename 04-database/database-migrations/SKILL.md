---
name: Database Migrations
description: Database migration strategies and tools for schema evolution and data transformation.
---

# Database Migrations

## Overview

Database migrations are versioned scripts that modify database schema and data over time. They enable teams to evolve their database structure in a controlled, reproducible manner while maintaining data integrity and minimizing downtime.

## Prerequisites

- Understanding of SQL and database schema design
- Knowledge of database systems (PostgreSQL, MySQL, etc.)
- Familiarity with version control systems
- Basic understanding of data transformation concepts

## Key Concepts

### What are Database Migrations?

Database migrations are:
- **Versioned**: Each migration has a unique version number or timestamp
- **Ordered**: Migrations are applied in a specific sequence
- **Reversible**: Most migrations can be rolled back
- **Idempotent**: Can be run multiple times safely
- **Team-compatible**: Allow multiple developers to work on schema changes

### Migration Types

1. **Schema Migrations**
   - Create/drop tables
   - Add/remove columns
   - Modify constraints
   - Create/drop indexes

2. **Data Migrations**
   - Transform existing data
   - Populate reference tables
   - Clean up inconsistent data
   - Backfill new columns

3. **Rollback Migrations**
   - Reverse schema changes
   - Restore previous data state
   - Handle edge cases

### Migration Lifecycle

```
Development → Testing → Staging → Production
     ↓            ↓          ↓          ↓
   Create      Verify    Validate    Deploy
   Test         Test       Test      Monitor
```

## Implementation Guide

### Basic Migration Structure

```javascript
// migrations/20240124000001_create_users_table.js
module.exports = {
  up: async (db) => {
    await db.schema.createTable('users', (table) => {
      table.increments('id').primary();
      table.string('email', 255).notNullable().unique();
      table.string('password_hash', 255).notNullable();
      table.timestamp('created_at').defaultTo(db.fn.now());
      table.timestamp('updated_at').defaultTo(db.fn.now());
    });
  },

  down: async (db) => {
    await db.schema.dropTable('users');
  }
};
```

### Using Knex.js

```javascript
const knex = require('knex');

// Initialize knex
const db = knex({
  client: 'pg',
  connection: {
    host: 'localhost',
    user: 'user',
    password: 'password',
    database: 'mydb'
  },
  migrations: {
    directory: './migrations',
    tableName: 'knex_migrations'
  }
});

// Create a new migration
// npx knex migrate:make create_users_table

// Run migrations
await db.migrate.latest();

// Rollback last migration
await db.migrate.rollback();

// Get current version
const current = await db.migrate.currentVersion();
console.log('Current migration version:', current);
```

### Using Sequelize

```javascript
const { Sequelize } = require('sequelize');

const sequelize = new Sequelize('mydb', 'user', 'password', {
  dialect: 'postgres',
  host: 'localhost',
  logging: false
});

// Define migration
module.exports = {
  up: async (queryInterface, Sequelize) => {
    await queryInterface.createTable('users', {
      id: {
        type: Sequelize.INTEGER,
        primaryKey: true,
        autoIncrement: true
      },
      email: {
        type: Sequelize.STRING(255),
        allowNull: false,
        unique: true
      },
      password_hash: {
        type: Sequelize.STRING(255),
        allowNull: false
      },
      created_at: {
        type: Sequelize.DATE,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      },
      updated_at: {
        type: Sequelize.DATE,
        defaultValue: Sequelize.literal('CURRENT_TIMESTAMP')
      }
    });
  },

  down: async (queryInterface) => {
    await queryInterface.dropTable('users');
  }
};

// Run migrations
await sequelize.sync({ alter: true });
```

### Using TypeORM

```typescript
import { MigrationInterface, QueryRunner } from 'typeorm';

export class CreateUsersTable1234567890 implements MigrationInterface {
  public async up(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.createTable(new Table({
      name: 'users',
      columns: [
        {
          name: 'id',
          type: 'int',
          isPrimary: true,
          isGenerated: true,
          generationStrategy: 'increment'
        },
        {
          name: 'email',
          type: 'varchar',
          length: '255',
          isNullable: false,
          isUnique: true
        },
        {
          name: 'password_hash',
          type: 'varchar',
          length: '255',
          isNullable: false
        },
        {
          name: 'created_at',
          type: 'timestamp',
          default: 'CURRENT_TIMESTAMP'
        },
        {
          name: 'updated_at',
          type: 'timestamp',
          default: 'CURRENT_TIMESTAMP'
        }
      ]
    }));
  }

  public async down(queryRunner: QueryRunner): Promise<void> {
    await queryRunner.dropTable('users');
  }
}
```

### Using Prisma

```typescript
// prisma/migrations/20240124000001_init/migration.sql
-- CreateUsersTable
CREATE TABLE "users" (
    "id" SERIAL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CreateUsersTableRollback
DROP TABLE "users";
```

```bash
# Generate migration
npx prisma migrate dev --name init

# Apply migrations
npx prisma migrate deploy

# Rollback
npx prisma migrate resolve --rolled-back 20240124000001_init
```

## Migration Patterns

### Adding a Column

```javascript
module.exports = {
  up: async (db) => {
    await db.schema.table('users')
      .addColumn('phone', 'varchar', { length: 20 });
  },

  down: async (db) => {
    await db.schema.table('users')
      .dropColumn('phone');
  }
};
```

### Adding a Column with Default Value

```javascript
module.exports = {
  up: async (db) => {
    await db.schema.table('users')
      .addColumn('status', 'varchar', {
        length: 50,
        defaultTo: 'active',
        notNullable: true
      });
  },

  down: async (db) => {
    await db.schema.table('users')
      .dropColumn('status');
  }
};
```

### Renaming a Column

```javascript
module.exports = {
  up: async (db) => {
    await db.schema.table('users')
      .renameColumn('email_address', 'email');
  },

  down: async (db) => {
    await db.schema.table('users')
      .renameColumn('email', 'email_address');
  }
};
```

### Adding an Index

```javascript
module.exports = {
  up: async (db) => {
    await db.schema.table('users')
      .index('email', 'idx_users_email');
  },

  down: async (db) => {
    await db.schema.table('users')
      .dropIndex('email', 'idx_users_email');
  }
};
```

### Adding a Foreign Key

```javascript
module.exports = {
  up: async (db) => {
    await db.schema.table('posts')
      .foreign('user_id')
      .references('id')
      .inTable('users')
      .onDelete('CASCADE');
  },

  down: async (db) => {
    await db.schema.table('posts')
      .dropForeign('user_id');
  }
};
```

### Data Migration

```javascript
module.exports = {
  up: async (db) => {
    // Add new column
    await db.schema.table('users')
      .addColumn('full_name', 'varchar', { length: 255 });

    // Migrate data
    await db('users')
      .update({
        full_name: db.raw('CONCAT(first_name, " ", last_name)')
      });

    // Drop old columns
    await db.schema.table('users')
      .dropColumn('first_name');
    await db.schema.table('users')
      .dropColumn('last_name');
  },

  down: async (db) => {
    // Add back old columns
    await db.schema.table('users')
      .addColumn('first_name', 'varchar', { length: 100 });
    await db.schema.table('users')
      .addColumn('last_name', 'varchar', { length: 100 });

    // Migrate data back
    await db.raw(`
      UPDATE users
      SET first_name = SPLIT_PART(full_name, ' ', 1),
          last_name = SPLIT_PART(full_name, ' ', 2)
    `);

    // Drop new column
    await db.schema.table('users')
      .dropColumn('full_name');
  }
};
```

## Zero-Downtime Migrations

### Expanding Columns (PostgreSQL)

```javascript
module.exports = {
  up: async (db) => {
    // Step 1: Add new column as nullable
    await db.schema.table('users')
      .addColumn('email_new', 'varchar', { length: 255 });

    // Step 2: Backfill data
    await db.raw(`
      UPDATE users
      SET email_new = email
      WHERE email_new IS NULL
    `);

    // Step 3: Add constraint
    await db.raw(`
      ALTER TABLE users
      ADD CONSTRAINT users_email_new_key
      UNIQUE (email_new)
    `);

    // Step 4: Swap columns
    await db.raw(`
      ALTER TABLE users
      RENAME COLUMN email TO email_old
    `);

    await db.raw(`
      ALTER TABLE users
      RENAME COLUMN email_new TO email
    `);

    // Step 5: Drop old column
    await db.schema.table('users')
      .dropColumn('email_old');
  },

  down: async (db) => {
    // Reverse the process
    await db.schema.table('users')
      .addColumn('email_old', 'varchar', { length: 255 });

    await db.raw(`
      UPDATE users
      SET email_old = email
      WHERE email_old IS NULL
    `);

    await db.raw(`
      ALTER TABLE users
      DROP CONSTRAINT IF EXISTS users_email_key
    `);

    await db.raw(`
      ALTER TABLE users
      RENAME COLUMN email TO email_new
    `);

    await db.raw(`
      ALTER TABLE users
      RENAME COLUMN email_old TO email
    `);

    await db.schema.table('users')
      .dropColumn('email_new');
  }
};
```

### Expanding Columns (MySQL)

```javascript
module.exports = {
  up: async (db) => {
    // Step 1: Add new column
    await db.schema.table('users')
      .addColumn('email_new', 'varchar', { length: 255 });

    // Step 2: Backfill data in batches
    const batchSize = 1000;
    let offset = 0;

    while (true) {
      const result = await db('users')
        .whereNull('email_new')
        .limit(batchSize)
        .offset(offset)
        .update({
          email_new: db.raw('email')
        });

      if (result === 0) break;
      offset += batchSize;
    }

    // Step 3: Rename columns
    await db.raw(`
      ALTER TABLE users
      CHANGE COLUMN email email_old VARCHAR(255)
    `);

    await db.raw(`
      ALTER TABLE users
      CHANGE COLUMN email_new email VARCHAR(255) NOT NULL UNIQUE
    `);

    // Step 4: Drop old column
    await db.schema.table('users')
      .dropColumn('email_old');
  },

  down: async (db) => {
    // Reverse the process
    await db.schema.table('users')
      .addColumn('email_old', 'varchar', { length: 255 });

    const batchSize = 1000;
    let offset = 0;

    while (true) {
      const result = await db('users')
        .whereNull('email_old')
        .limit(batchSize)
        .offset(offset)
        .update({
          email_old: db.raw('email')
        });

      if (result === 0) break;
      offset += batchSize;
    }

    await db.raw(`
      ALTER TABLE users
      CHANGE COLUMN email email_new VARCHAR(255)
    `);

    await db.raw(`
      ALTER TABLE users
      CHANGE COLUMN email_old email VARCHAR(255) NOT NULL UNIQUE
    `);

    await db.schema.table('users')
      .dropColumn('email_new');
  }
};
```

### Adding Indexes Without Locking

```javascript
module.exports = {
  up: async (db) => {
    // PostgreSQL: CREATE INDEX CONCURRENTLY
    await db.raw(`
      CREATE INDEX CONCURRENTLY idx_users_email
      ON users(email)
    `);
  },

  down: async (db) => {
    await db.raw(`
      DROP INDEX CONCURRENTLY IF EXISTS idx_users_email
    `);
  }
};
```

## Rollback Strategies

### Simple Rollback

```javascript
module.exports = {
  up: async (db) => {
    await db.schema.createTable('users', (table) => {
      table.increments('id').primary();
      table.string('email', 255).notNullable().unique();
    });
  },

  down: async (db) => {
    await db.schema.dropTable('users');
  }
};
```

### Data-Preserving Rollback

```javascript
module.exports = {
  up: async (db) => {
    // Create backup table
    await db.raw(`
      CREATE TABLE users_backup AS
      SELECT * FROM users
    `);

    // Make changes
    await db('users')
      .where('status', 'inactive')
      .update({ status: 'deleted' });
  },

  down: async (db) => {
    // Restore from backup
    await db.raw(`
      UPDATE users u
      SET status = ub.status
      FROM users_backup ub
      WHERE u.id = ub.id
    `);

    // Drop backup table
    await db.schema.dropTableIfExists('users_backup');
  }
};
```

### Conditional Rollback

```javascript
module.exports = {
  up: async (db) => {
    // Check if column exists
    const hasColumn = await db.schema.hasColumn('users', 'phone');

    if (!hasColumn) {
      await db.schema.table('users')
        .addColumn('phone', 'varchar', { length: 20 });
    }
  },

  down: async (db) => {
    await db.schema.table('users')
      .dropColumnIfExists('phone');
  }
};
```

## Version Control

### Naming Conventions

```bash
# Timestamp-based
20240124000001_create_users_table.js
20240124000002_add_phone_to_users.js

# Description-based
20240124_120000_create_users_table.js
20240124_130000_add_phone_to_users.js

# Sequential
001_create_users_table.js
002_add_phone_to_users.js
```

### Migration Tracking Table

```sql
CREATE TABLE schema_migrations (
  id SERIAL PRIMARY KEY,
  version VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255),
  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Branch Migrations

```javascript
// Handle branch-specific migrations
const isProduction = process.env.NODE_ENV === 'production';

module.exports = {
  up: async (db) => {
    await db.schema.createTable('users', (table) => {
      table.increments('id').primary();
      table.string('email', 255).notNullable().unique();
    });

    // Production-specific migrations
    if (isProduction) {
      await db.raw(`
        CREATE INDEX CONCURRENTLY idx_users_email
        ON users(email)
      `);
    }
  },

  down: async (db) => {
    if (isProduction) {
      await db.raw(`
        DROP INDEX CONCURRENTLY IF EXISTS idx_users_email
      `);
    }

    await db.schema.dropTable('users');
  }
};
```

## Testing Migrations

### Unit Testing

```javascript
const { expect } = require('chai');
const db = require('./db');

describe('Migration: create_users_table', () => {
  let migration;

  before(async () => {
    migration = require('./migrations/20240124000001_create_users_table');
  });

  it('should create users table', async () => {
    await migration.up(db);

    const hasTable = await db.schema.hasTable('users');
    expect(hasTable).to.be.true;
  });

  it('should create all columns', async () => {
    await migration.up(db);

    const hasId = await db.schema.hasColumn('users', 'id');
    const hasEmail = await db.schema.hasColumn('users', 'email');
    const hasPasswordHash = await db.schema.hasColumn('users', 'password_hash');

    expect(hasId).to.be.true;
    expect(hasEmail).to.be.true;
    expect(hasPasswordHash).to.be.true;
  });

  it('should create unique constraint on email', async () => {
    await migration.up(db);

    const indexes = await db('users').columnInfo();
    const emailIndex = indexes.find(i => i.column_name === 'email');

    expect(emailIndex).to.exist;
  });

  afterEach(async () => {
    await migration.down(db);
  });
});
```

### Integration Testing

```javascript
describe('Migration Integration', () => {
  let testDb;

  before(async () => {
    // Create test database
    testDb = knex({
      client: 'pg',
      connection: {
        host: 'localhost',
        user: 'user',
        password: 'password',
        database: 'mydb_test'
      }
    });

    // Run all migrations
    await testDb.migrate.latest();
  });

  it('should allow inserting users', async () => {
    await testDb('users').insert({
      email: 'test@example.com',
      password_hash: 'hashed_password'
    });

    const users = await testDb('users').select();
    expect(users).to.have.lengthOf(1);
  });

  it('should enforce unique email constraint', async () => {
    await testDb('users').insert({
      email: 'test@example.com',
      password_hash: 'hashed_password'
    });

    try {
      await testDb('users').insert({
        email: 'test@example.com',
        password_hash: 'different_hash'
      });
      throw new Error('Should have thrown unique constraint error');
    } catch (error) {
      expect(error.code).to.equal('23505'); // Unique violation
    }
  });

  after(async () => {
    await testDb.destroy();
  });
});
```

## Best Practices

1. **Make Migrations Reversible**
   - Always implement the `down` function
   - Test rollback in development
   - Document irreversible migrations

2. **Keep Migrations Small**
   - One logical change per migration
   - Avoid combining unrelated changes
   - Split large migrations into smaller ones

3. **Use Transactions**
   - Wrap migrations in transactions
   - Rollback on failure
   - Ensure atomicity

4. **Test Thoroughly**
   - Test migrations on sample data
   - Verify rollback works
   - Test in staging before production

5. **Document Changes**
   - Add comments explaining the change
   - Note breaking changes
   - Document data transformations

6. **Handle Large Datasets**
   - Use batch processing for data migrations
   - Add indexes before data migrations
   - Monitor performance during migration

7. **Version Control**
   - Commit migrations with code changes
   - Never modify committed migrations
   - Create new migrations for corrections

## Common Pitfalls

1. **Irreversible Migrations**
   ```javascript
   // Bad: Dropping table without backup
   down: async (db) => {
     await db.schema.dropTable('users'); // Data lost!
   }

   // Good: Create backup before dropping
   up: async (db) => {
     await db.raw('CREATE TABLE users_backup AS SELECT * FROM users');
     await db.schema.dropTable('users');
   }

   down: async (db) => {
     await db.raw('CREATE TABLE users AS SELECT * FROM users_backup');
     await db.schema.dropTable('users_backup');
   }
   ```

2. **Blocking Production**
   ```javascript
   // Bad: Long-running migration blocks production
   up: async (db) => {
     await db.raw('CREATE INDEX idx_users_email ON users(email)');
   }

   // Good: Use CONCURRENTLY for PostgreSQL
   up: async (db) => {
     await db.raw('CREATE INDEX CONCURRENTLY idx_users_email ON users(email)');
   }
   ```

3. **Data Loss**
   ```javascript
   // Bad: Overwriting data without backup
   up: async (db) => {
     await db('users').update({ status: 'active' });
   }

   // Good: Create backup first
   up: async (db) => {
     await db.raw('CREATE TABLE users_backup AS SELECT * FROM users');
     await db('users').update({ status: 'active' });
   }
   ```

## Related Skills

- [`04-database/database-optimization`](04-database/database-optimization/SKILL.md)
- [`04-database/database-transactions`](04-database/database-transactions/SKILL.md)
- [`15-devops-infrastructure/ci-cd-pipelines`](15-devops-infrastructure/ci-cd-pipelines/SKILL.md)
