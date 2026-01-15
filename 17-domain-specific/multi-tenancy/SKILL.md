# Multi-Tenancy

A comprehensive guide to multi-tenancy architecture patterns.

## Table of Contents

1. [Multi-Tenancy Models](#multi-tenancy-models)
2. [Tenant Identification](#tenant-identification)
3. [Data Isolation](#data-isolation)
4. [Query Filtering](#query-filtering)
5. [Prisma Multi-Tenancy](#prisma-multi-tenancy)
6. [Connection Pooling](#connection-pooling)
7. [Migrations](#migrations)
8. [Performance Considerations](#performance-considerations)
9. [Security](#security)
10. [Cost Optimization](#cost-optimization)
11. [Best Practices](#best-practices)

---

## Multi-Tenancy Models

### Database per Tenant

```
┌─────────────────────────────────────────────────────┐
│            Database per Tenant Model              │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────┐ │
│  │  Tenant A   │  │  Tenant B   │  │ ... │ │
│  │ Database    │  │ Database    │  │     │ │
│  └─────────────┘  └─────────────┘  └─────┘ │
│                                                     │
│  Pros:                                             │
│  - Complete data isolation                        │
│  - Custom schema per tenant                        │
│  - Easy to scale individual tenants              │
│                                                     │
│  Cons:                                             │
│  - High cost (many databases)                     │
│  - Complex management                            │
│  - Connection overhead                           │
└─────────────────────────────────────────────────────┘
```

### Schema per Tenant

```
┌─────────────────────────────────────────────────────┐
│            Schema per Tenant Model                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────┐        │
│  │         Database                   │        │
│  │  ┌─────────┐ ┌─────────┐ ┌───┐   │        │
│  │  │Schema A │ │Schema B │ │...│   │        │
│  │  └─────────┘ └─────────┘ └───┘   │        │
│  └─────────────────────────────────────┘        │
│                                                     │
│  Pros:                                             │
│  - Data isolation at schema level                │
│  - Shared database (lower cost)                │
│  - Custom schema per tenant                    │
│                                                     │
│  Cons:                                             │
│  - Schema management complexity                │
│  - Migration challenges                         │
│  - Tenant-specific schema drift                │
└─────────────────────────────────────────────────────┘
```

### Shared Database

```
┌─────────────────────────────────────────────────────┐
│            Shared Database Model                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────┐        │
│  │         Database                   │        │
│  │  ┌─────────────────────────────┐   │        │
│  │  │      Shared Tables      │   │        │
│  │  │  ┌─────────┐ ┌──────┐ │   │        │
│  │  │  │Users    │ │Posts │ │   │        │
│  │  │  │Tenant A │ │Tenant│ │   │        │
│  │  │  │Tenant B │ │Tenant│ │   │        │
│  │  │  │...      │ │...   │ │   │        │
│  │  │  └─────────┘ └──────┘ │   │        │
│  │  └─────────────────────────────┘   │        │
│  └─────────────────────────────────────┘        │
│                                                     │
│  Pros:                                             │
│  - Lowest cost                                  │
│  - Simple management                           │
│  - Easy to scale                                │
│                                                     │
│  Cons:                                             │
│  - Risk of data leakage                        │
│  - Query filtering required                    │
│  - Performance concerns                        │
└─────────────────────────────────────────────────────┘
```

---

## Tenant Identification

### Subdomain-Based

```typescript
// Extract tenant from subdomain
function getTenantFromSubdomain(host: string): string {
  const parts = host.split('.');
  return parts[0]; // tenant.example.com -> tenant
}

// Express middleware
import express from 'express';

const app = express();

app.use((req, res, next) => {
  const tenant = getTenantFromSubdomain(req.hostname);
  req.tenant = tenant;
  next();
});
```

```python
# Extract tenant from subdomain
def get_tenant_from_subdomain(host: str) -> str:
    parts = host.split('.')
    return parts[0]  # tenant.example.com -> tenant

# Django middleware
class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant = get_tenant_from_subdomain(request.get_host())
        request.tenant = tenant
        return self.get_response(request)
```

### Path-Based

```typescript
// Extract tenant from path
function getTenantFromPath(path: string): string {
  const parts = path.split('/').filter(Boolean);
  return parts[0]; // /tenant/path -> tenant
}

// Express middleware
app.use((req, res, next) => {
  const tenant = getTenantFromPath(req.path);
  req.tenant = tenant;
  next();
});
```

```python
# Extract tenant from path
def get_tenant_from_path(path: str) -> str:
    parts = [p for p in path.split('/') if p]
    return parts[0]  # /tenant/path -> tenant

# Django middleware
class TenantMiddleware:
    def __call__(self, request):
        tenant = get_tenant_from_path(request.path)
        request.tenant = tenant
        return self.get_response(request)
```

### Header-Based

```typescript
// Extract tenant from header
function getTenantFromHeader(headers: any): string {
  return headers['x-tenant-id'] || 'default';
}

// Express middleware
app.use((req, res, next) => {
  const tenant = getTenantFromHeader(req.headers);
  req.tenant = tenant;
  next();
});
```

```python
# Extract tenant from header
def get_tenant_from_header(headers: dict) -> str:
    return headers.get('x-tenant-id', 'default')

# Django middleware
class TenantMiddleware:
    def __call__(self, request):
        tenant = get_tenant_from_header(request.META)
        request.tenant = tenant
        return self.get_response(request)
```

---

## Data Isolation

### Row-Level Isolation (Shared Database)

```typescript
// Add tenant_id to all tables
interface User {
  id: string;
  tenantId: string;
  name: string;
  email: string;
}

// Query with tenant filter
async function getUsers(tenantId: string): Promise<User[]> {
  return prisma.user.findMany({
    where: { tenantId },
  });
}
```

```python
# Add tenant_id to all tables
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    tenant_id = Column(String, nullable=False)
    name = Column(String)
    email = Column(String)

# Query with tenant filter
def get_users(tenant_id: str):
    return session.query(User).filter(User.tenant_id == tenant_id).all()
```

### Schema-Level Isolation

```sql
-- Create schema for tenant
CREATE SCHEMA tenant_1;

-- Create tables in schema
CREATE TABLE tenant_1.users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255),
  email VARCHAR(255)
);

-- Query in schema
SELECT * FROM tenant_1.users;
```

```typescript
// Use schema per tenant
async function getUsers(tenantId: string): Promise<User[]> {
  return prisma.$queryRaw`SELECT * FROM ${tenantId}.users`;
}
```

---

## Query Filtering

### Automatic Query Filtering (TypeScript)

```typescript
// Prisma middleware for automatic tenant filtering
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

prisma.$use(async (params, next) => {
  const tenant = params.args?.tenantId;

  if (tenant && params.model) {
    // Add tenant filter to queries
    params.args.where = {
      ...params.args.where,
      tenantId: tenant,
    };
  }

  return next(params);
});

// Usage
const users = await prisma.user.findMany({
  where: { tenantId: 'tenant-1' },
});
```

### Automatic Query Filtering (Python)

```python
# SQLAlchemy event listener for automatic tenant filtering
from sqlalchemy import event
from sqlalchemy.orm import Query

@event.listens_for(Query, "before_compile", retval=True)
def add_tenant_filter(query, compiler, **kwargs):
    tenant_id = kwargs.get('tenant_id')

    if tenant_id and query.column_descriptions:
        for column in query.column_descriptions:
            if hasattr(column, 'tenant_id'):
                query = query.filter(column.tenant_id == tenant_id)

    return query

# Usage
users = session.query(User).options(tenant_id='tenant-1').all()
```

### Global Scope Filtering

```typescript
// Prisma global scope
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function withTenant(tenantId: string, callback: () => Promise<void>) {
  // Create scoped client
  const scopedClient = prisma.$extends({
    query: {
      $allOperations({ args }) {
        return {
          ...args,
          where: {
            ...args.where,
            tenantId,
          },
        };
      },
    },
  });

  await callback();
}
```

---

## Prisma Multi-Tenancy

### Row-Level Multi-Tenancy

```typescript
// schema.prisma
model User {
  id        String   @id @default(cuid())
  tenantId  String
  name      String
  email     String   @unique

  @@index([tenantId, email])
}

// Middleware for tenant filtering
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

prisma.$use(async (params, next) => {
  const tenant = params.args?.tenantId;

  if (tenant && params.model) {
    params.args.where = {
      ...params.args.where,
      tenantId: tenant,
    };
  }

  return next(params);
});

// Usage
const users = await prisma.user.findMany({
  where: { tenantId: 'tenant-1' },
});
```

### Schema-Level Multi-Tenancy

```typescript
// schema.prisma
model User {
  id        String   @id @default(cuid())
  name      String
  email     String   @unique
}

// Multi-tenant client
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
});

// Create schema for tenant
async function createTenantSchema(tenantId: string) {
  await prisma.$executeRawUnsafe(`CREATE SCHEMA IF NOT EXISTS ${tenantId}`);
  await prisma.$executeRawUnsafe(`CREATE TABLE IF NOT EXISTS ${tenantId}.users (id TEXT PRIMARY KEY, name TEXT, email TEXT)`);
}

// Query tenant schema
async function getTenantUsers(tenantId: string) {
  return prisma.$queryRawUnsafe(`SELECT * FROM ${tenantId}.users`);
}
```

---

## Connection Pooling

### Tenant-Specific Connection Pools

```typescript
// Connection pool per tenant
import { Pool } from 'pg';

const tenantPools = new Map<string, Pool>();

function getTenantPool(tenantId: string): Pool {
  if (!tenantPools.has(tenantId)) {
    const pool = new Pool({
      host: process.env.DB_HOST,
      port: parseInt(process.env.DB_PORT || '5432'),
      database: `tenant_${tenantId}`,
      user: process.env.DB_USER,
      password: process.env.DB_PASSWORD,
      max: 20,
    });
    tenantPools.set(tenantId, pool);
  }
  return tenantPools.get(tenantId)!;
}

// Usage
const pool = getTenantPool('tenant-1');
const result = await pool.query('SELECT * FROM users');
```

```python
# Connection pool per tenant
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

tenant_pools = {}

def get_tenant_pool(tenant_id: str):
    if tenant_id not in tenant_pools:
        engine = create_engine(
            f"postgresql://user:pass@localhost/tenant_{tenant_id}",
            poolclass=QueuePool,
            pool_size=20,
            max_overflow=10
        )
        tenant_pools[tenant_id] = engine
    return tenant_pools[tenant_id]

# Usage
engine = get_tenant_pool('tenant-1')
result = engine.execute("SELECT * FROM users").fetchall()
```

---

## Migrations

### Schema-Level Migrations

```typescript
// Migration script for new tenant
async function migrateTenant(tenantId: string) {
  // Create schema
  await prisma.$executeRawUnsafe(`CREATE SCHEMA IF NOT EXISTS ${tenantId}`);

  // Run migrations in tenant schema
  const migrations = await prisma.$queryRaw`
    SELECT migration_name
    FROM schema_migrations
    WHERE applied = false
  `;

  for (const migration of migrations) {
    await prisma.$executeRawUnsafe(`
      SET search_path TO ${tenantId};
      ${migration.sql}
    `);
  }
}
```

### Row-Level Migrations

```typescript
// Migration with tenant_id
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function migrateTenant(tenantId: string) {
  // Add tenant_id to existing tables
  await prisma.$executeRaw`
    ALTER TABLE users ADD COLUMN IF NOT EXISTS tenant_id VARCHAR(255)
  `;

  // Migrate data
  await prisma.$executeRaw`
    UPDATE users
    SET tenant_id = '${tenantId}'
    WHERE tenant_id IS NULL
  `;
}
```

---

## Performance Considerations

### Indexing

```sql
-- Index tenant_id for faster filtering
CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_users_tenant_id_email ON users(tenant_id, email);

-- Composite index
CREATE INDEX idx_users_tenant_id_name ON users(tenant_id, name);
```

### Partitioning

```sql
-- Partition by tenant_id
CREATE TABLE users (
  id SERIAL,
  tenant_id VARCHAR(255),
  name VARCHAR(255),
  email VARCHAR(255)
) PARTITION BY LIST (tenant_id);

-- Create partitions for tenants
CREATE TABLE users_tenant1 PARTITION OF users FOR VALUES IN ('tenant1');
CREATE TABLE users_tenant2 PARTITION OF users FOR VALUES IN ('tenant2');
```

### Query Optimization

```typescript
// Use indexed columns in queries
async function getUserByEmail(tenantId: string, email: string) {
  return prisma.user.findUnique({
    where: {
      tenantId_email: {  // Composite index
        tenantId,
        email,
      },
    },
  });
}
```

---

## Security

### Tenant Isolation

```typescript
// Ensure tenant isolation in queries
async function getUser(tenantId: string, userId: string) {
  const user = await prisma.user.findUnique({
    where: {
      id: userId,
      tenantId,  // Ensure user belongs to tenant
    },
  });

  if (!user || user.tenantId !== tenantId) {
    throw new Error('User not found');
  }

  return user;
}
```

### Row-Level Security (PostgreSQL)

```sql
-- Enable row-level security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policy for tenant isolation
CREATE POLICY tenant_isolation ON users
  FOR ALL
  USING (tenant_id = current_setting('app.current_tenant')::TEXT);

-- Set tenant for session
SET app.current_tenant = 'tenant-1';
```

---

## Cost Optimization

### Database per Tenant - Cost Considerations

| Factor | Cost Impact |
|--------|-------------|
| **Storage** | High (many databases) |
| **Connections** | High (connection per database) |
| **Backups** | High (backup per database) |
| **Monitoring** | Medium (monitoring per database) |

### Schema per Tenant - Cost Considerations

| Factor | Cost Impact |
|--------|-------------|
| **Storage** | Medium (shared database) |
| **Connections** | Medium (shared connection pool) |
| **Backups** | Medium (backup per schema) |
| **Monitoring** | Medium (monitoring per schema) |

### Shared Database - Cost Considerations

| Factor | Cost Impact |
|--------|-------------|
| **Storage** | Low (single database) |
| **Connections** | Low (shared connection pool) |
| **Backups** | Low (single backup) |
| **Monitoring** | Low (single monitoring) |

---

## Best Practices

### 1. Use Consistent Tenant Identification

```typescript
// Use consistent tenant identification
const tenant = req.tenant || 'default';
```

### 2. Enforce Tenant Isolation

```typescript
// Always filter by tenant_id
const users = await prisma.user.findMany({
  where: { tenantId: req.tenantId },
});
```

### 3. Index Tenant Columns

```sql
-- Index tenant_id
CREATE INDEX idx_tenant_id ON users(tenant_id);
```

### 4. Use Connection Pooling

```typescript
// Use connection pools
const pool = new Pool({ max: 20 });
```

### 5. Monitor Tenant Performance

```typescript
// Monitor per-tenant metrics
metrics.record('query_duration', duration, {
  tenantId: req.tenantId,
  operation: 'getUsers',
});
```

### 6. Implement Tenant-Specific Caching

```typescript
// Cache with tenant key
const cacheKey = `users:${tenantId}:${userId}`;
```

### 7. Use Database Migrations

```typescript
// Version control migrations
const migrations = [
  { version: 1, name: 'add_tenant_id' },
  { version: 2, name: 'add_index' },
];
```

### 8. Test Tenant Isolation

```typescript
// Test that tenant isolation works
test('should not access other tenant data', async () => {
  const user1 = await prisma.user.findFirst({
    where: { tenantId: 'tenant-1' },
  });

  const user2 = await prisma.user.findFirst({
    where: { tenantId: 'tenant-2' },
  });

  expect(user1).not.toEqual(user2);
});
```

### 9. Document Tenant Architecture

```markdown
# Multi-Tenancy Architecture

## Model
- Shared database with row-level isolation

## Tenant Identification
- Subdomain-based: tenant.example.com

## Data Isolation
- tenant_id column on all tables
- Automatic query filtering
```

### 10. Plan for Tenant Migration

```typescript
// Plan tenant migration path
async function migrateTenant(tenantId: string) {
  // 1. Create new schema
  // 2. Migrate data
  // 3. Update application
  // 4. Test
  // 5. Switch traffic
}
```

---

## Resources

- [Prisma Multi-Tenancy](https://www.prisma.io/docs/guides/database/multi-tenancy)
- [PostgreSQL Row-Level Security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- [SQLAlchemy Multi-Tenancy](https://docs.sqlalchemy.org/en/14/core/pooling.html)
