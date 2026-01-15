# Multi-Tenancy Architecture

## Overview

Multi-tenancy allows multiple customers (tenants) to share the same application infrastructure while maintaining data isolation. This skill covers multi-tenancy models, tenant identification, data isolation, query filtering, Prisma multi-tenancy, connection pooling, migrations, performance considerations, security, cost optimization, and best practices.

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

### Database Per Tenant

Each tenant gets their own database instance.

```sql
-- Create database for tenant
CREATE DATABASE tenant_123;
```

```typescript
// src/multi-tenancy/database-per-tenant.ts
import { Pool } from 'pg';

interface TenantDatabaseConfig {
  tenantId: string;
  host: string;
  port: number;
  database: string;
  user: string;
  password: string;
}

class TenantDatabaseManager {
  private pools: Map<string, Pool> = new Map();

  async getPool(tenantId: string): Promise<Pool> {
    if (this.pools.has(tenantId)) {
      return this.pools.get(tenantId)!;
    }

    const config = await this.getTenantConfig(tenantId);
    const pool = new Pool(config);
    this.pools.set(tenantId, pool);
    return pool;
  }

  private async getTenantConfig(tenantId: string): Promise<TenantDatabaseConfig> {
    // Fetch tenant database config from config service
    return {
      tenantId,
      host: 'localhost',
      port: 5432,
      database: `tenant_${tenantId}`,
      user: 'postgres',
      password: 'password',
    };
  }

  async closePool(tenantId: string): Promise<void> {
    const pool = this.pools.get(tenantId);
    if (pool) {
      await pool.end();
      this.pools.delete(tenantId);
    }
  }
}

export const tenantDatabaseManager = new TenantDatabaseManager();
```

### Schema Per Tenant

Each tenant gets their own schema within a shared database.

```sql
-- Create schema for tenant
CREATE SCHEMA tenant_123;

-- Create tables in tenant schema
CREATE TABLE tenant_123.users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(255)
);
```

```typescript
// src/multi-tenancy/schema-per-tenant.ts
import { Pool } from 'pg';

class TenantSchemaManager {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: 'localhost',
      port: 5432,
      database: 'multi_tenant_db',
      user: 'postgres',
      password: 'password',
    });
  }

  async createTenantSchema(tenantId: string): Promise<void> {
    const client = await this.pool.connect();
    try {
      await client.query(`CREATE SCHEMA IF NOT EXISTS tenant_${tenantId}`);
      
      // Create tables in tenant schema
      await client.query(`
        CREATE TABLE IF NOT EXISTS tenant_${tenantId}.users (
          id SERIAL PRIMARY KEY,
          name VARCHAR(100),
          email VARCHAR(255) UNIQUE,
          created_at TIMESTAMP DEFAULT NOW()
        )
      `);
      
      await client.query(`
        CREATE TABLE IF NOT EXISTS tenant_${tenantId}.posts (
          id SERIAL PRIMARY KEY,
          title VARCHAR(255),
          content TEXT,
          user_id INTEGER REFERENCES tenant_${tenantId}.users(id),
          created_at TIMESTAMP DEFAULT NOW()
        )
      `);
    } finally {
      client.release();
    }
  }

  async dropTenantSchema(tenantId: string): Promise<void> {
    const client = await this.pool.connect();
    try {
      await client.query(`DROP SCHEMA IF EXISTS tenant_${tenantId} CASCADE`);
    } finally {
      client.release();
    }
  }
}

export const tenantSchemaManager = new TenantSchemaManager();
```

### Shared Database

All tenants share the same database and tables, with a tenant_id column for isolation.

```sql
-- Create shared tables with tenant_id
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  tenant_id INTEGER NOT NULL,
  name VARCHAR(100),
  email VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE (tenant_id, email)
);

CREATE INDEX idx_users_tenant_id ON users(tenant_id);
```

```typescript
// src/multi-tenancy/shared-database.ts
import { Pool } from 'pg';

class SharedDatabaseManager {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: 'localhost',
      port: 5432,
      database: 'multi_tenant_db',
      user: 'postgres',
      password: 'password',
    });
  }

  async createUser(tenantId: number, userData: UserData): Promise<User> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'INSERT INTO users (tenant_id, name, email) VALUES ($1, $2, $3) RETURNING *',
        [tenantId, userData.name, userData.email]
      );
      return result.rows[0];
    } finally {
      client.release();
    }
  }

  async getUsers(tenantId: number): Promise<User[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'SELECT * FROM users WHERE tenant_id = $1',
        [tenantId]
      );
      return result.rows;
    } finally {
      client.release();
    }
  }

  async deleteUser(tenantId: number, userId: number): Promise<void> {
    const client = await this.pool.connect();
    try {
      await client.query(
        'DELETE FROM users WHERE tenant_id = $1 AND id = $2',
        [tenantId, userId]
      );
    } finally {
      client.release();
    }
  }
}

export const sharedDatabaseManager = new SharedDatabaseManager();
```

---

## Tenant Identification

### Subdomain-Based

```typescript
// src/multi-tenancy/subdomain-tenant.ts
import { Request } from 'express';

class TenantResolver {
  resolveTenant(req: Request): string | null {
    const host = req.headers.host || '';
    const subdomain = host.split('.')[0];
    
    // Skip common subdomains
    const commonSubdomains = ['www', 'api', 'app', 'staging'];
    if (commonSubdomains.includes(subdomain)) {
      return null;
    }
    
    return subdomain;
  }
}

export const tenantResolver = new TenantResolver();
```

```typescript
// src/middleware/tenant.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { tenantResolver } from '../multi-tenancy/subdomain-tenant';

export function tenantMiddleware(req: Request, res: Response, next: NextFunction) {
  const tenantId = tenantResolver.resolveTenant(req);
  
  if (!tenantId) {
    return res.status(400).json({ error: 'Unable to identify tenant' });
  }
  
  req.tenantId = tenantId;
  next();
}
```

### Path-Based

```typescript
// src/multi-tenancy/path-tenant.ts
import { Request } from 'express';

class PathTenantResolver {
  resolveTenant(req: Request): string | null {
    const pathParts = req.path.split('/').filter(Boolean);
    
    if (pathParts.length === 0) {
      return null;
    }
    
    // First path segment is tenant ID
    return pathParts[0];
  }
}

export const pathTenantResolver = new PathTenantResolver();
```

### Header-Based

```typescript
// src/multi-tenancy/header-tenant.ts
import { Request } from 'express';

class HeaderTenantResolver {
  resolveTenant(req: Request): string | null {
    const tenantId = req.headers['x-tenant-id'] as string;
    return tenantId || null;
  }
}

export const headerTenantResolver = new HeaderTenantResolver();
```

### Token-Based

```typescript
// src/multi-tenancy/token-tenant.ts
import { Request } from 'express';
import jwt from 'jsonwebtoken';

class TokenTenantResolver {
  resolveTenant(req: Request): string | null {
    const token = req.headers.authorization?.replace('Bearer ', '');
    
    if (!token) {
      return null;
    }
    
    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET!) as any;
      return decoded.tenantId;
    } catch (error) {
      return null;
    }
  }
}

export const tokenTenantResolver = new TokenTenantResolver();
```

---

## Data Isolation

### Row-Level Security (PostgreSQL)

```sql
-- Enable row-level security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policy for tenant isolation
CREATE POLICY tenant_isolation_policy ON users
  FOR ALL
  USING (tenant_id = current_setting('app.current_tenant_id')::INTEGER);

-- Create function to set tenant context
CREATE OR REPLACE FUNCTION set_tenant_context(tenant_id INTEGER)
RETURNS VOID AS $$
BEGIN
  PERFORM set_config('app.current_tenant_id', tenant_id::TEXT, FALSE);
END;
$$ LANGUAGE plpgsql;
```

```typescript
// src/multi-tenancy/rls.ts
import { Pool } from 'pg';

class RLSManager {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: 'localhost',
      port: 5432,
      database: 'multi_tenant_db',
      user: 'postgres',
      password: 'password',
    });
  }

  async setTenantContext(tenantId: number): Promise<void> {
    const client = await this.pool.connect();
    try {
      await client.query('SELECT set_tenant_context($1)', [tenantId]);
    } finally {
      client.release();
    }
  }

  async queryWithTenant<T>(tenantId: number, query: string, params: any[] = []): Promise<T[]> {
    const client = await this.pool.connect();
    try {
      await this.setTenantContext(tenantId);
      const result = await client.query(query, params);
      return result.rows;
    } finally {
      client.release();
    }
  }
}

export const rlsManager = new RLSManager();
```

### Application-Level Filtering

```typescript
// src/multi-tenancy/app-filtering.ts
import { Pool } from 'pg';

class AppFilterManager {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: 'localhost',
      port: 5432,
      database: 'multi_tenant_db',
      user: 'postgres',
      password: 'password',
    });
  }

  async getUsers(tenantId: number): Promise<User[]> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'SELECT * FROM users WHERE tenant_id = $1',
        [tenantId]
      );
      return result.rows;
    } finally {
      client.release();
    }
  }

  async getUser(tenantId: number, userId: number): Promise<User | null> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'SELECT * FROM users WHERE tenant_id = $1 AND id = $2',
        [tenantId, userId]
      );
      return result.rows[0] || null;
    } finally {
      client.release();
    }
  }

  async updateUser(tenantId: number, userId: number, updates: Partial<User>): Promise<User | null> {
    const client = await this.pool.connect();
    try {
      const setClause = Object.keys(updates)
        .map((key, index) => `${key} = $${index + 3}`)
        .join(', ');
      
      const values = Object.values(updates);
      const query = `
        UPDATE users
        SET ${setClause}
        WHERE tenant_id = $1 AND id = $2
        RETURNING *
      `;
      
      const result = await client.query(query, [tenantId, userId, ...values]);
      return result.rows[0] || null;
    } finally {
      client.release();
    }
  }

  async deleteUser(tenantId: number, userId: number): Promise<boolean> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(
        'DELETE FROM users WHERE tenant_id = $1 AND id = $2',
        [tenantId, userId]
      );
      return result.rowCount! > 0;
    } finally {
      client.release();
    }
  }
}

export const appFilterManager = new AppFilterManager();
```

---

## Query Filtering

### Automatic Query Filtering

```typescript
// src/multi-tenancy/query-filter.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

class QueryFilterManager {
  private tenantId: number | null = null;

  setTenant(tenantId: number): void {
    this.tenantId = tenantId;
  }

  clearTenant(): void {
    this.tenantId = null;
  }

  async getUsers(): Promise<User[]> {
    if (!this.tenantId) {
      throw new Error('Tenant not set');
    }

    return prisma.user.findMany({
      where: {
        tenantId: this.tenantId,
      },
    });
  }

  async getUser(id: number): Promise<User | null> {
    if (!this.tenantId) {
      throw new Error('Tenant not set');
    }

    return prisma.user.findFirst({
      where: {
        id,
        tenantId: this.tenantId,
      },
    });
  }

  async createUser(data: Omit<User, 'id'>): Promise<User> {
    if (!this.tenantId) {
      throw new Error('Tenant not set');
    }

    return prisma.user.create({
      data: {
        ...data,
        tenantId: this.tenantId,
      },
    });
  }

  async updateUser(id: number, data: Partial<User>): Promise<User> {
    if (!this.tenantId) {
      throw new Error('Tenant not set');
    }

    return prisma.user.update({
      where: {
        id,
        tenantId: this.tenantId,
      },
      data,
    });
  }

  async deleteUser(id: number): Promise<User> {
    if (!this.tenantId) {
      throw new Error('Tenant not set');
    }

    return prisma.user.delete({
      where: {
        id,
        tenantId: this.tenantId,
      },
    });
  }
}

export const queryFilterManager = new QueryFilterManager();
```

### Middleware Integration

```typescript
// src/middleware/query-filter.middleware.ts
import { Request, Response, NextFunction } from 'express';
import { queryFilterManager } from '../multi-tenancy/query-filter';

export function queryFilterMiddleware(req: Request, res: Response, next: NextFunction) {
  const tenantId = req.tenantId;
  
  if (!tenantId) {
    return res.status(400).json({ error: 'Tenant not identified' });
  }
  
  queryFilterManager.setTenant(parseInt(tenantId));
  next();
}
```

---

## Prisma Multi-Tenancy

### Schema Definition

```prisma
// prisma/schema.prisma

model Tenant {
  id        Int     @id @default(autoincrement())
  name      String
  slug      String  @unique
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  users     User[]
  posts     Post[]
}

model User {
  id        Int     @id @default(autoincrement())
  tenantId  Int
  tenant    Tenant  @relation(fields: [tenantId], references: [id], onDelete: Cascade)
  name      String
  email     String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  posts     Post[]
  
  @@unique([tenantId, email])
  @@index([tenantId])
}

model Post {
  id        Int     @id @default(autoincrement())
  tenantId  Int
  tenant    Tenant  @relation(fields: [tenantId], references: [id], onDelete: Cascade)
  userId    Int
  user      User    @relation(fields: [userId], references: [id], onDelete: Cascade)
  title     String
  content   String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  
  @@index([tenantId])
  @@index([userId])
}
```

### Prisma Middleware

```typescript
// src/multi-tenancy/prisma-middleware.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

prisma.$use(async (params, next) => {
  // Get tenant ID from context
  const tenantId = params.args?.tenantId;
  
  if (tenantId) {
    // Add tenant filter to queries
    if (params.action === 'findMany' || params.action === 'findFirst') {
      params.args.where = {
        ...params.args.where,
        tenantId,
      };
    }
    
    if (params.action === 'create') {
      params.args.data = {
        ...params.args.data,
        tenantId,
      };
    }
    
    if (params.action === 'update' || params.action === 'delete') {
      params.args.where = {
        ...params.args.where,
        tenantId,
      };
    }
  }
  
  return next(params);
});

export { prisma };
```

### Tenant-Aware Repository

```typescript
// src/repositories/tenant-aware.repository.ts
import { prisma } from '../multi-tenancy/prisma-middleware';

class TenantAwareRepository<T> {
  async findMany(tenantId: number, args?: any): Promise<T[]> {
    return prisma[this.modelName].findMany({
      ...args,
      tenantId,
    });
  }

  async findFirst(tenantId: number, args?: any): Promise<T | null> {
    return prisma[this.modelName].findFirst({
      ...args,
      tenantId,
    });
  }

  async create(tenantId: number, data: any): Promise<T> {
    return prisma[this.modelName].create({
      data: {
        ...data,
        tenantId,
      },
    });
  }

  async update(tenantId: number, id: number, data: any): Promise<T> {
    return prisma[this.modelName].update({
      where: { id, tenantId },
      data,
    });
  }

  async delete(tenantId: number, id: number): Promise<T> {
    return prisma[this.modelName].delete({
      where: { id, tenantId },
    });
  }
}

class UserRepository extends TenantAwareRepository<User> {
  protected modelName = 'user';
}

class PostRepository extends TenantAwareRepository<Post> {
  protected modelName = 'post';
}

export { UserRepository, PostRepository };
```

---

## Connection Pooling

### Per-Tenant Connection Pool

```typescript
// src/multi-tenancy/connection-pool.ts
import { Pool, PoolConfig } from 'pg';

interface TenantPoolConfig {
  tenantId: string;
  config: PoolConfig;
}

class TenantConnectionPoolManager {
  private pools: Map<string, Pool> = new Map();
  private poolConfigs: Map<string, PoolConfig> = new Map();

  async getPool(tenantId: string): Promise<Pool> {
    if (this.pools.has(tenantId)) {
      return this.pools.get(tenantId)!;
    }

    const config = await this.getPoolConfig(tenantId);
    const pool = new Pool(config);
    
    this.pools.set(tenantId, pool);
    return pool;
  }

  private async getPoolConfig(tenantId: string): Promise<PoolConfig> {
    if (this.poolConfigs.has(tenantId)) {
      return this.poolConfigs.get(tenantId)!;
    }

    // Fetch pool config from config service
    const config: PoolConfig = {
      host: 'localhost',
      port: 5432,
      database: `tenant_${tenantId}`,
      user: 'postgres',
      password: 'password',
      max: 20, // Maximum pool size
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    };

    this.poolConfigs.set(tenantId, config);
    return config;
  }

  async closePool(tenantId: string): Promise<void> {
    const pool = this.pools.get(tenantId);
    if (pool) {
      await pool.end();
      this.pools.delete(tenantId);
      this.poolConfigs.delete(tenantId);
    }
  }

  async closeAllPools(): Promise<void> {
    const closePromises = Array.from(this.pools.values()).map(pool => pool.end());
    await Promise.all(closePromises);
    this.pools.clear();
    this.poolConfigs.clear();
  }
}

export const tenantConnectionPoolManager = new TenantConnectionPoolManager();
```

### Shared Connection Pool with Schema

```typescript
// src/multi-tenancy/shared-pool.ts
import { Pool, PoolClient } from 'pg';

class SharedConnectionPoolManager {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: 'localhost',
      port: 5432,
      database: 'multi_tenant_db',
      user: 'postgres',
      password: 'password',
      max: 100, // Larger pool for shared database
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });
  }

  async getClient(tenantId: string): Promise<PoolClient> {
    const client = await this.pool.connect();
    
    // Set search path to tenant schema
    await client.query(`SET search_path TO tenant_${tenantId}, public`);
    
    return client;
  }

  async close(): Promise<void> {
    await this.pool.end();
  }
}

export const sharedConnectionPoolManager = new SharedConnectionPoolManager();
```

---

## Migrations

### Tenant-Specific Migrations

```typescript
// src/migrations/tenant-migration.ts
import { Pool } from 'pg';

class TenantMigrationManager {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: 'localhost',
      port: 5432,
      database: 'multi_tenant_db',
      user: 'postgres',
      password: 'password',
    });
  }

  async createTenantSchema(tenantId: string): Promise<void> {
    const client = await this.pool.connect();
    try {
      await client.query(`CREATE SCHEMA IF NOT EXISTS tenant_${tenantId}`);
      
      // Run migrations for tenant
      await this.runMigrations(client, tenantId);
    } finally {
      client.release();
    }
  }

  private async runMigrations(client: PoolClient, tenantId: string): Promise<void> {
    const migrations = [
      `
        CREATE TABLE IF NOT EXISTS tenant_${tenantId}.users (
          id SERIAL PRIMARY KEY,
          name VARCHAR(100),
          email VARCHAR(255) UNIQUE,
          created_at TIMESTAMP DEFAULT NOW()
        )
      `,
      `
        CREATE TABLE IF NOT EXISTS tenant_${tenantId}.posts (
          id SERIAL PRIMARY KEY,
          title VARCHAR(255),
          content TEXT,
          user_id INTEGER REFERENCES tenant_${tenantId}.users(id),
          created_at TIMESTAMP DEFAULT NOW()
        )
      `,
    ];

    for (const migration of migrations) {
      await client.query(migration);
    }
  }

  async dropTenantSchema(tenantId: string): Promise<void> {
    const client = await this.pool.connect();
    try {
      await client.query(`DROP SCHEMA IF EXISTS tenant_${tenantId} CASCADE`);
    } finally {
      client.release();
    }
  }
}

export const tenantMigrationManager = new TenantMigrationManager();
```

### Migration for All Tenants

```typescript
// src/migrations/batch-migration.ts
import { Pool } from 'pg';

class BatchMigrationManager {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: 'localhost',
      port: 5432,
      database: 'multi_tenant_db',
      user: 'postgres',
      password: 'password',
    });
  }

  async migrateAllTenants(): Promise<void> {
    const client = await this.pool.connect();
    try {
      // Get all tenant schemas
      const result = await client.query(`
        SELECT schema_name
        FROM information_schema.schemata
        WHERE schema_name LIKE 'tenant_%'
      `);

      for (const row of result.rows) {
        const tenantId = row.schema_name.replace('tenant_', '');
        await this.migrateTenant(tenantId);
      }
    } finally {
      client.release();
    }
  }

  private async migrateTenant(tenantId: string): Promise<void> {
    const client = await this.pool.connect();
    try {
      // Add new column to all tenant tables
      await client.query(`
        ALTER TABLE tenant_${tenantId}.users
        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT NOW()
      `);
    } finally {
      client.release();
    }
  }
}

export const batchMigrationManager = new BatchMigrationManager();
```

---

## Performance Considerations

### Database Indexing

```sql
-- Index tenant_id columns for faster queries
CREATE INDEX idx_users_tenant_id ON users(tenant_id);
CREATE INDEX idx_posts_tenant_id ON posts(tenant_id);

-- Composite indexes for common queries
CREATE INDEX idx_users_tenant_email ON users(tenant_id, email);
CREATE INDEX idx_posts_tenant_user ON posts(tenant_id, user_id);
```

### Query Optimization

```typescript
// src/multi-tenancy/query-optimization.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

class OptimizedQueryManager {
  async getUsersWithPosts(tenantId: number): Promise<User[]> {
    // Use include to avoid N+1 queries
    return prisma.user.findMany({
      where: { tenantId },
      include: {
        posts: true,
      },
    });
  }

  async getUsersPaginated(tenantId: number, page: number, limit: number): Promise<{ users: User[], total: number }> {
    const [users, total] = await Promise.all([
      prisma.user.findMany({
        where: { tenantId },
        skip: (page - 1) * limit,
        take: limit,
        orderBy: { createdAt: 'desc' },
      }),
      prisma.user.count({ where: { tenantId } }),
    ]);

    return { users, total };
  }

  async searchUsers(tenantId: number, query: string): Promise<User[]> {
    // Use full-text search
    return prisma.user.findMany({
      where: {
        tenantId,
        OR: [
          { name: { contains: query, mode: 'insensitive' } },
          { email: { contains: query, mode: 'insensitive' } },
        ],
      },
    });
  }
}

export const optimizedQueryManager = new OptimizedQueryManager();
```

### Caching

```typescript
// src/multi-tenancy/cache.ts
import { Redis } from 'ioredis';

const redis = new Redis();

class TenantCacheManager {
  private getCacheKey(tenantId: number, key: string): string {
    return `tenant:${tenantId}:${key}`;
  }

  async get<T>(tenantId: number, key: string): Promise<T | null> {
    const cacheKey = this.getCacheKey(tenantId, key);
    const cached = await redis.get(cacheKey);
    return cached ? JSON.parse(cached) : null;
  }

  async set(tenantId: number, key: string, value: any, ttl: number = 3600): Promise<void> {
    const cacheKey = this.getCacheKey(tenantId, key);
    await redis.setex(cacheKey, ttl, JSON.stringify(value));
  }

  async delete(tenantId: number, key: string): Promise<void> {
    const cacheKey = this.getCacheKey(tenantId, key);
    await redis.del(cacheKey);
  }

  async deleteAll(tenantId: number): Promise<void> {
    const pattern = `tenant:${tenantId}:*`;
    const keys = await redis.keys(pattern);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
  }
}

export const tenantCacheManager = new TenantCacheManager();
```

---

## Security

### Tenant Isolation Validation

```typescript
// src/multi-tenancy/security.ts
import { Request, Response, NextFunction } from 'express';

export function validateTenantAccess(req: Request, res: Response, next: NextFunction) {
  const tenantId = req.tenantId;
  const resourceTenantId = req.params.tenantId || req.body.tenantId;
  
  if (resourceTenantId && resourceTenantId !== tenantId) {
    return res.status(403).json({ error: 'Access denied: Tenant mismatch' });
  }
  
  next();
}
```

### Data Encryption

```typescript
// src/multi-tenancy/encryption.ts
import crypto from 'crypto';

class TenantEncryptionManager {
  private encryptionKeys: Map<string, Buffer> = new Map();

  setEncryptionKey(tenantId: string, key: string): void {
    this.encryptionKeys.set(tenantId, Buffer.from(key, 'hex'));
  }

  encrypt(tenantId: string, data: string): string {
    const key = this.encryptionKeys.get(tenantId);
    if (!key) {
      throw new Error('Encryption key not found for tenant');
    }

    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
    
    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    return iv.toString('hex') + ':' + encrypted;
  }

  decrypt(tenantId: string, encryptedData: string): string {
    const key = this.encryptionKeys.get(tenantId);
    if (!key) {
      throw new Error('Encryption key not found for tenant');
    }

    const [ivHex, encrypted] = encryptedData.split(':');
    const iv = Buffer.from(ivHex, 'hex');
    const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
    
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  }
}

export const tenantEncryptionManager = new TenantEncryptionManager();
```

---

## Cost Optimization

### Resource Monitoring

```typescript
// src/multi-tenancy/monitoring.ts
import { Pool } from 'pg';

class TenantResourceMonitor {
  private pool: Pool;

  constructor() {
    this.pool = new Pool({
      host: 'localhost',
      port: 5432,
      database: 'multi_tenant_db',
      user: 'postgres',
      password: 'password',
    });
  }

  async getTenantStats(tenantId: string): Promise<TenantStats> {
    const client = await this.pool.connect();
    try {
      // Get table sizes
      const tablesResult = await client.query(`
        SELECT
          schemaname,
          tablename,
          pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
        FROM pg_tables
        WHERE schemaname = 'tenant_${tenantId}'
      `);

      // Get row counts
      const rowsResult = await client.query(`
        SELECT
          schemaname,
          tablename,
          n_live_tup AS row_count
        FROM pg_stat_user_tables
        WHERE schemaname = 'tenant_${tenantId}'
      `);

      return {
        tables: tablesResult.rows,
        rows: rowsResult.rows,
      };
    } finally {
      client.release();
    }
  }

  async getAllTenantStats(): Promise<Map<string, TenantStats>> {
    const client = await this.pool.connect();
    try {
      const result = await client.query(`
        SELECT DISTINCT schemaname
        FROM pg_tables
        WHERE schemaname LIKE 'tenant_%'
      `);

      const stats = new Map<string, TenantStats>();
      
      for (const row of result.rows) {
        const tenantId = row.schemaname.replace('tenant_', '');
        stats.set(tenantId, await this.getTenantStats(tenantId));
      }

      return stats;
    } finally {
      client.release();
    }
  }
}

export const tenantResourceMonitor = new TenantResourceMonitor();
```

### Automatic Scaling

```typescript
// src/multi-tenancy/auto-scaling.ts
import { tenantConnectionPoolManager } from './connection-pool';

class AutoScalingManager {
  private readonly MAX_POOL_SIZE = 50;
  private readonly MIN_POOL_SIZE = 5;

  async scalePool(tenantId: string, currentUsage: number): Promise<void> {
    const pool = await tenantConnectionPoolManager.getPool(tenantId);
    const currentSize = pool.totalCount;
    
    if (currentUsage > 0.8 && currentSize < this.MAX_POOL_SIZE) {
      // Scale up
      const newSize = Math.min(currentSize + 10, this.MAX_POOL_SIZE);
      console.log(`Scaling up pool for tenant ${tenantId} to ${newSize}`);
    } else if (currentUsage < 0.3 && currentSize > this.MIN_POOL_SIZE) {
      // Scale down
      const newSize = Math.max(currentSize - 5, this.MIN_POOL_SIZE);
      console.log(`Scaling down pool for tenant ${tenantId} to ${newSize}`);
    }
  }
}

export const autoScalingManager = new AutoScalingManager();
```

---

## Best Practices

### 1. Always Filter by Tenant ID

```typescript
// Good: Always filter by tenant ID
async getUsers(tenantId: number): Promise<User[]> {
  return prisma.user.findMany({
    where: { tenantId },
  });
}

// Bad: No tenant filtering
async getUsers(): Promise<User[]> {
  return prisma.user.findMany();
}
```

### 2. Use Middleware for Tenant Context

```typescript
// Good: Use middleware
app.use(tenantMiddleware);

// Bad: Manual tenant handling in each route
app.get('/users', (req, res) => {
  const tenantId = req.headers['x-tenant-id'];
  // ...
});
```

### 3. Validate Tenant Access

```typescript
// Good: Validate tenant access
app.get('/users/:id', validateTenantAccess, async (req, res) => {
  const user = await getUser(req.tenantId, req.params.id);
  res.json(user);
});

// Bad: No validation
app.get('/users/:id', async (req, res) => {
  const user = await getUser(req.params.id);
  res.json(user);
});
```

### 4. Use Database-Level Isolation

```sql
-- Good: Use RLS
CREATE POLICY tenant_isolation_policy ON users
  FOR ALL
  USING (tenant_id = current_setting('app.current_tenant_id')::INTEGER);

-- Bad: Application-level only
-- No RLS, rely on application filtering
```

### 5. Monitor Tenant Resource Usage

```typescript
// Good: Monitor resources
const stats = await tenantResourceMonitor.getTenantStats(tenantId);
console.log(`Tenant ${tenantId} stats:`, stats);

// Bad: No monitoring
// No resource tracking
```

---

## Summary

This skill covers comprehensive multi-tenancy architecture patterns including:

- **Multi-Tenancy Models**: Database per tenant, schema per tenant, shared database
- **Tenant Identification**: Subdomain-based, path-based, header-based, token-based
- **Data Isolation**: Row-level security, application-level filtering
- **Query Filtering**: Automatic query filtering, middleware integration
- **Prisma Multi-Tenancy**: Schema definition, Prisma middleware, tenant-aware repository
- **Connection Pooling**: Per-tenant pool, shared pool with schema
- **Migrations**: Tenant-specific migrations, batch migrations
- **Performance Considerations**: Database indexing, query optimization, caching
- **Security**: Tenant isolation validation, data encryption
- **Cost Optimization**: Resource monitoring, automatic scaling
- **Best Practices**: Filter by tenant ID, use middleware, validate access, database-level isolation, monitor resources
