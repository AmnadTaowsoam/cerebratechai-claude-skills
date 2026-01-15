# Integration Testing

## Overview

Integration testing verifies that different parts of your application work together correctly. This skill covers integration testing patterns, test containers, database testing, API testing, and best practices.

## Table of Contents

1. [Integration Testing Concepts](#integration-testing-concepts)
2. [Test Containers (Testcontainers)](#test-containers)
3. [Database Testing](#database-testing)
4. [API Testing](#api-testing)
5. [Message Queue Testing](#message-queue-testing)
6. [External Service Mocking](#external-service-mocking)
7. [Test Data Management](#test-data-management)
8. [Setup and Teardown](#setup-and-teardown)
9. [CI/CD Integration](#cicd-integration)
10. [Best Practices](#best-practices)

---

## Integration Testing Concepts

### Why Integration Testing?

1. **Verify component interactions**
2. **Test data flow between services**
3. **Validate external integrations**
4. **Catch integration bugs early**
5. **Ensure system reliability**

### Integration vs Unit Tests

| Aspect | Unit Tests | Integration Tests |
|--------|-----------|------------------|
| Scope | Single component | Multiple components |
| Speed | Fast | Slower |
| Isolation | Isolated | Real dependencies |
| Environment | Mocked | Real infrastructure |
| Cost | Low | Higher |

---

## Test Containers (Testcontainers)

### Node.js with Testcontainers

```bash
npm install -D testcontainers
```

```typescript
// test/integration/database.test.ts
import { describe, it, beforeEach, afterEach } from '@jest/globals';
import { PostgreSqlContainer, StartedPostgreSqlContainer } from 'testcontainers';

describe('Database Integration', () => {
  let container: StartedPostgreSqlContainer;
  let connection: any;

  beforeEach(async () => {
    // Start PostgreSQL container
    container = await new PostgreSqlContainer('postgres:15-alpine').start();
    
    // Get connection string
    connection = await container.getConnectionString();
  });

  afterEach(async () => {
    // Stop container
    await container.stop();
  });

  it('should connect to database', async () => {
    const { Client } = require('pg');
    const client = new Client({ connectionString: connection });
    await client.connect();
    
    const result = await client.query('SELECT NOW()');
    expect(result.rows.length).toBeGreaterThan(0);
    
    await client.end();
  });
});
```

### Python with Testcontainers

```bash
pip install testcontainers
```

```python
# test/integration/database_test.py
import pytest
from testcontainers.postgres import PostgresContainer

def test_database_connection():
    """Test database connection with testcontainers."""
    with PostgresContainer('postgres:15-alpine') as postgres:
        connection_string = postgres.get_connection_url()
        
        import psycopg2
        conn = psycopg2.connect(connection_string)
        
        cursor = conn.cursor()
        cursor.execute('SELECT NOW()')
        result = cursor.fetchone()
        
        assert result is not None
        assert result[0] is not None
        
        cursor.close()
        conn.close()
```

### Redis Container

```typescript
// test/integration/redis.test.ts
import { describe, it, beforeEach, afterEach } from '@jest/globals';
import { GenericContainer } from 'testcontainers';

describe('Redis Integration', () => {
  let container: GenericContainer;

  beforeEach(async () => {
    container = await new GenericContainer('redis:7-alpine').start();
  });

  afterEach(async () => {
    await container.stop();
  });

  it('should connect to Redis', async () => {    const { createClient } = require('redis');
    const client = createClient({ url: `redis://localhost:${container.getMappedPort(6379)}` });
    
    await client.connect();
    await client.set('test', 'value');
    const result = await client.get('test');
    
    expect(result).toBe('value');
    
    await client.quit();
  });
});
```

### MongoDB Container

```typescript
// test/integration/mongodb.test.ts
import { describe, it, beforeEach, afterEach } from '@jest/globals';
import { MongoContainer } from 'testcontainers';

describe('MongoDB Integration', () => {
  let container: MongoContainer;

  beforeEach(async () => {
    container = await new MongoContainer('mongo:6').start();
  });

  afterEach(async () => {
    await container.stop();
  });

  it('should connect to MongoDB', async () => {
    const { MongoClient } = require('mongodb');
    const url = `mongodb://localhost:${container.getMappedPort(27017)}`;
    
    const client = new MongoClient(url);
    await client.connect();
    
    const db = client.db('testdb');
    const result = await db.collection('users').insertOne({ name: 'Test User' });
    
    expect(result.insertedId).toBeDefined();
    
    await client.close();
  });
});
```

---

## Database Testing

### PostgreSQL Integration

```typescript
// test/integration/postgres.test.ts
import { describe, it, beforeEach, afterEach } from '@jest/globals';
import { PostgreSqlContainer, StartedPostgreSqlContainer } from 'testcontainers';
import { Client } from 'pg';

describe('PostgreSQL Integration', () => {
  let container: StartedPostgreSqlContainer;
  let client: Client;

  beforeEach(async () => {
    container = await new PostgreSqlContainer('postgres:15-alpine').start();
    const connectionString = await container.getConnectionString();
    client = new Client({ connectionString });
    await client.connect();
  });

  afterEach(async () => {
    await client.end();
    await container.stop();
  });

  it('should create and retrieve user', async () => {
    const result = await client.query(
      'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email',
      ['John Doe', 'john@example.com']
    );
    
    expect(result.rows.length).toBe(1);
    expect(result.rows[0].id).toBeDefined();
    expect(result.rows[0].name).toBe('John Doe');
    expect(result.rows[0].email).toBe('john@example.com');
  });

  it('should update user', async () => {
    await client.query(
      'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id, name, email',
      ['Jane Doe', 'jane@example.com']
    );
    
    const { rows } = await client.query('UPDATE users SET name = $1 WHERE id = $2', ['Updated Name', 1]);
    
    expect(rows[0].name).toBe('Updated Name');
  });

  it('should delete user', async () => {
    await client.query('INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id', ['John Doe', 'john@example.com']);
    const { rows } = await client.query('SELECT id FROM users WHERE email = $1', ['john@example.com']);
    const userId = rows[0].id;
    
    await client.query('DELETE FROM users WHERE id = $1', [userId]);
    
    const result = await client.query('SELECT COUNT(*) FROM users WHERE email = $1', ['john@example.com']);
    expect(result.rows[0].count).toBe(0);
  });
});
```

### MongoDB Integration

```typescript
// test/integration/mongodb.test.ts
import { describe, it, beforeEach, afterEach } from '@jest/globals';
import { MongoContainer } from 'testcontainers';
import { MongoClient } from 'mongodb';

describe('MongoDB Integration', () => {
  let container: MongoContainer;
  let client: MongoClient;

  beforeEach(async () => {
    container = await new MongoContainer('mongo:6').start();
    const url = `mongodb://localhost:${container.getMappedPort(27017)}`;
    client = new MongoClient(url);
    await client.connect();
  });

  afterEach(async () => {
    await client.close();
    await container.stop();
  });

  it('should create and retrieve document', async () => {
    const db = client.db('testdb');
    
    const result = await db.collection('users').insertOne({
      name: 'Test User',
      email: 'test@example.com',
    age: 30,
    });
    
    expect(result.insertedId).toBeDefined();
    
    const user = await db.collection('users').findOne({ email: 'test@example.com' });
    expect(user).not.toBeNull();
    expect(user.name).toBe('Test User');
  });

  it('should update document', async () => {
    const db = client.db('testdb');
    
    await db.collection('users').insertOne({
      name: 'Test User',
      email: 'test@example.com',
      age: 30,
    });
    
    await db.collection('users').updateOne(
      { email: 'test@example.com' },
      { $set: { age: 31 } }
    );
    
    const user = await db.collection('users').findOne({ email: 'test@example.com' });
    expect(user.age).toBe(31);
  });

  it('should delete document', async () => {
    const db = client.db('testdb');
    
    await db.collection('users').insertOne({
      name: 'Test User',
      email: 'test@example.com',
      age: 30,
    });
    
    await db.collection('users').deleteOne({ email: 'test@example.com' });
    
    const user = await db.collection('users').findOne({ email: 'test@example.com' });
    expect(user).toBeNull();
  });
});
```

---

## API Testing

### Supertest (Node.js)

```bash
npm install --save-dev supertest
```

```typescript
// test/integration/api.test.ts
import request from 'supertest';
import { describe, it, beforeAll, afterAll } from '@jest/globals';
import app from '../src/app';

describe('API Integration', () => {
  let server: any;

  beforeAll(async () => {
    server = app.listen(3000);
  });

  afterAll(async () => {
    server.close();
  });

  it('should create user', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({
        name: 'John Doe',
        email: 'john@example.com',
      })
      .expect(201)
      .expect('Content-Type', /json/);
    
    expect(response.body).toHaveProperty('id');
    expect(response.body.name).toBe('John Doe');
  });

  it('should get user', async () => {
    // First create a user
    const createResponse = await request(app)
      .post('/api/users')
      .send({
        name: 'Jane Doe',
        email: 'jane@example.com',
      })
      .expect(201);
    
    const userId = createResponse.body.id;

    const response = await request(app)
      .get(`/api/users/${userId}`)
      .expect(200)
      .expect('Content-Type', /json/);
    
    expect(response.body.id).toBe(userId);
    expect(response.body.name).toBe('Jane Doe');
  });

  it('should update user', async () => {
    // First create a user
    const createResponse = await request(app)
      .post('/api/users')
      .send({
        name: 'Test User',
        email: 'test@example.com',
      })
      .expect(201);
    
    const userId = createResponse.body.id;

    const response = await request(app)
      .put(`/api/users/${userId}`)
      .send({
        name: 'Updated User',
      })
      .expect(200)
      .expect('Content-Type', /json/);
    
    expect(response.body.name).toBe('Updated User');
  });

  it('should delete user', async () => {
    // First create a user
    const createResponse = await request(app)
      .post('/api/users')
      .send({
        name: 'Test User',
        email: 'test@example.com',
      })
      .expect(201);
    
    const userId = createResponse.body.id;

    const response = await request(app)
      .delete(`/api/users/${userId}`)
      .expect(200);
    
    expect(response.body.message).toBe('User deleted');
  });
});
```

### httpx (Python)

```bash
pip install httpx pytest
```

```python
# test/integration/api_test.py
import pytest
from httpx import AsyncClient
import asyncio

from src.main import app

@pytest.fixture
async def client():
    """Async HTTP client for testing."""
    async with AsyncClient(app=app, base_url='http://localhost:8000') as ac:
        yield ac

async def test_create_user(client):
    """Test user creation endpoint."""
    response = await client.post(
        '/api/users',
        json={
            'name': 'John Doe',
            'email': 'john@example.com'
        }
    )
    assert response.status_code == 201
    assert 'id' in response.json()
    assert response.json()['name'] == 'John Doe'

async def test_get_user(client):
    """Test getting a user."""
    # First create a user
    create_response = await client.post(
        '/api/users',
        json={
            'name': 'Jane Doe',
            'email': 'jane@example.com'
        }
    )
    user_id = create_response.json()['id']
    
    response = await client.get(f'/api/users/{user_id}')
    assert response.status_code == 200
    assert response.json()['id'] == user_id
    assert response.json()['name'] == 'Jane Doe'

async def test_update_user(client):
    """Test updating a user."""
    # First create a user
    create_response = await client.post(
        '/api/users',
        json={
            'name': 'Test User',
            'email': 'test@example.com'
        }
    )
    user_id = create_response.json()['id']
    
    response = await client.put(
        f'/api/users/{user_id}',
        json={'name': 'Updated User'}
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Updated User'

async def test_delete_user(client):
    """Test deleting a user."""
    # First create a user
    create_response = await client.post(
        '/api/users',
        json={
            'name': 'Test User',
            'email': 'test@example.com'
        }
    )
    user_id = create_response.json()['id']
    
    response = await client.delete(f'/api/users/{user_id}')
    assert response.status_code == 200
    assert 'message' in response.json()
```
```

---

## Message Queue Testing

### Redis Pub/Sub

```typescript
// test/integration/redis-pubsub.test.ts
import { describe, it, beforeEach, afterEach } from '@jest/globals';
import { GenericContainer } from 'testcontainers';

describe('Redis Pub/Sub Integration', () => {
  let container: GenericContainer;
  let client: any;

  beforeEach(async () => {
    container = await new GenericContainer('redis:7-alpine').start();
    const { createClient } = require('redis');
    client = createClient({ url: `redis://localhost:${container.getMappedPort(6379)}` });
    await client.connect();
  });

  afterEach(async () => {
    await client.quit();
    await container.stop();
  });

  it('should publish and subscribe to channel', async () => {
    const subscriber = client.duplicate();
    
    const messages: string[] = [];
    
    subscriber.subscribe('test-channel', (message) => {
      messages.push(message);
    });
    
    await new Promise(resolve => setTimeout(resolve, 100));
    await client.publish('test-channel', 'message 1');
    await new Promise(resolve => setTimeout(resolve, 100));
    await client.publish('test-channel', 'message 2');
    await new Promise(resolve => setTimeout(resolve, 100));
    
    await new Promise(resolve => setTimeout(resolve, 200));
    
    expect(messages).toEqual(['message 1', 'message 2']);
    
    subscriber.quit();
  });

  it('should handle large messages', async () => {
    const subscriber = client.duplicate();
    
    const largeMessage = 'x'.repeat(10000); // 10KB message
    
    subscriber.subscribe('large-channel', (message) => {
      expect(message).toBe(largeMessage);
    });
    
    await client.publish('large-channel', largeMessage);
    
    await new Promise(resolve => setTimeout(resolve, 200));
    
    subscriber.quit();
  });
});
```

### RabbitMQ Integration

```typescript
// test/integration/rabbitmq.test.ts
import { describe, it, beforeEach, afterEach } from '@jest/globals';
import { RabbitMQContainer } from 'testcontainers';

describe('RabbitMQ Integration', () => {
  let container: RabbitMQContainer;
  let channel: any;

  beforeEach(async () => {
    container = await new RabbitMQContainer('rabbitmq:3-management-alpine').start();
    const amqplib = require('amqplib');
    
    const connection = await amqplib.connect(`amqp://guest:guest@localhost:${container.getMappedPort(5672)}`);
    channel = await connection.createChannel();
    await channel.assertQueue('test-queue');
  });

  afterEach(async () => {
    await channel.close();
    await container.stop();
  });

  it('should publish and consume message', async () => {
    const messages: string[] = [];
    
    await channel.consume('test-queue', (msg) => {
      messages.push(msg.content.toString());
  });
    
    await channel.sendToQueue('test-queue', 'message 1');
    await new Promise(resolve => setTimeout(resolve, 100));
    await channel.sendToQueue('test-queue', 'message 2');
    await new Promise(resolve => setTimeout(resolve, 100));
    
    await new Promise(resolve => setTimeout(resolve, 200));
    
    expect(messages).toEqual(['message 1', 'message 2']);
  });
});
```

---

## External Service Mocking

### Mocking External API

```typescript
// test/integration/external-api-mock.test.ts
import { describe, it, beforeEach, afterEach } from '@jest/globals';
import nock from 'nock';

describe('External API Mock', () => {
  beforeEach(() => {
    nock.cleanAll();
  });

  afterEach(() => {
    nock.cleanAll();
  });

  it('should mock external API call', async () => {
    nock('https://api.example.com/users')
      .get('/1')
      .reply(200, {
        id: 1,
        name: 'Test User',
        email: 'test@example.com',
      })
      .times(1);

    const response = await fetch('https://api.example.com/users/1');
    const data = await response.json();

    expect(data.id).toBe(1);
    expect(data.name).toBe('Test User');
  });

  it('should handle API errors', async () => {
    nock('https://api.example.com/users')
      .get('/999')
      .reply(404, {
        error: 'User not found',
      })
      .times(1);

    try {
      await fetch('https://api.example.com/users/999');
      expect(true).toBe(false);
    } catch (error) {
      expect(error.message).toContain('404');
    }
  });
});
```

### Mocking Database

```typescript
// test/integration/database-mock.test.ts
import { describe, it, beforeEach, afterEach } from '@jest/globals';

describe('Database Mock', () => {
  const mockDb = {
    users: [],
    
    create: async (userData: any) => {
      const user = { id: mockDb.users.length + 1, ...userData };
      mockDb.users.push(user);
      return user;
    },
    
    getById: async (id: number) => {
      return mockDb.users.find(u => u.id === id);
    },
    
    getAll: async () => {
      return [...mockDb.users];
    },
    
    update: async (id: number, updates: any) => {
      const user = mockDb.users.find(u => u.id === id);
      if (!user) throw new Error('User not found');
      Object.assign(user, updates);
      return user;
    },
    
    delete: async (id: number) => {
      const index = mockDb.users.findIndex(u => u.id === id);
      if (index === -1) throw new Error('User not found');
      mockDb.users.splice(index, 1);
    },
  };

  beforeEach(() => {
    mockDb.users = [];
  });

  afterEach(() => {
    mockDb.users = [];
  });

  it('should create and retrieve user', async () => {
    const user = await mockDb.create({
      name: 'John Doe',
      email: 'john@example.com',
    });
    
    expect(user.id).toBe(1);
    
    const retrieved = await mockDb.getById(user.id);
    expect(retrieved).toEqual(user);
  });

  it('should update user', async () => {
    const user = await mockDb.create({
      name: 'Jane Doe',
      email: 'jane@example.com',
    });
    
    const updated = await mockDb.update(user.id, { name: 'Updated Name' });
    expect(updated.name).toBe('Updated Name');
    
    const retrieved = await mockDb.getById(user.id);
    expect(retrieved.name).toBe('Updated Name');
  });

  it('should delete user', async () => {
    const user = await mockDb.create({
      name: 'Test User',
      email: 'test@example.com',
    });
    
    await mockDb.delete(user.id);
    
    const retrieved = await mockDb.getById(user.id);
    expect(retrieved).toBeNull();
  });
});
```

---

## Test Data Management

### Factory Pattern

```typescript
// test/factories/user.factory.ts
export class UserFactory {
  static create(overrides: Partial<User> = {}): User {
    return {
      id: Math.floor(Math.random() * 1000),
      name: 'Test User',
      email: `test${Math.floor(Math.random() * 1000)}@example.com`,
      createdAt: new Date(),
      ...overrides,
    };
}

static createMany(count: number, overrides: Partial<User> = {}): User[] {
  return Array.from({ length: count }, () => this.create(overrides));
}
}

interface User {
  id: number;
  name: string;
  email: string;
  createdAt: Date;
}
```

```typescript
// test/integration/user.test.ts
import { UserFactory } from '../factories/user.factory';

describe('User Factory', () => {
  it('should create user with defaults', () => {
    const user = UserFactory.create();
    
    expect(user.id).toBeDefined();
    expect(user.name).toBe('Test User');
    expect(user.email).toContain('@example.com');
  });

  it('should create user with overrides', () => {
    const user = UserFactory.create({
      name: 'Custom Name',
      email: 'custom@example.com',
    });
    
    expect(user.name).toBe('Custom Name');
    expect(user.email).toBe('custom@example.com');
  });

  it('should create multiple users', () => {
    const users = UserFactory.createMany(5);
    
    expect(users).toHaveLength(5);
    expect(users.every(u => u.email.includes('@example.com'));
  });
});
```

### Faker Integration

```typescript
// test/factories/faker.factory.ts
import { faker } from '@faker-js/faker';

export class DataFactory {
  static user() {
    return {
      id: faker.number.int(),
      name: faker.person.fullName(),
      email: faker.internet.email(),
      phone: faker.phone.number(),
      address: {
        street: faker.location.streetAddress(),
        city: faker.location.city(),
        state: faker.location.state({ abbreviated: true }),
        zipCode: faker.location.zipCode('#####'),
      },
    };
  }

  static product() {
    return {
      id: faker.number.int(),
      name: faker.commerce.productName(),
      price: parseFloat(faker.commerce.price()),
      description: faker.commerce.productDescription(),
      stock: faker.number.int({ min: 0, max: 100 }),
    };
  }

  static order() {
    const user = this.user();
    const products = this.products(faker.number.int({ min: 1, max: 5 }));
    
    return {
      id: faker.number.int(),
      userId: user.id,
      total: products.reduce((sum, p) => sum + p.price, 0),
      status: faker.helpers.arrayElement(['pending', 'processing', 'shipped', 'delivered', 'cancelled']),
      createdAt: faker.date.past(),
    items: products.map(p => ({
      productId: p.id,
      quantity: faker.number.int({ min: 1, max: 10 }),
      price: p.price,
    })),
    };
  }

  static products(count: number) {
    return Array.from({ length: count }, () => this.product());
  }
}
```

---

## Setup and Teardown

### Database Setup and Teardown

```typescript
// test/integration/database-setup.test.ts
import { describe, beforeAll, afterAll } from '@jest/globals';
import { Client } from 'pg';

describe('Database Integration', () => {
  let client: Client;

  beforeAll(async () => {
    client = new Client({
      host: 'localhost',
      port: 5432,
      database: 'testdb',
      user: 'postgres',
      password: 'postgres',
    });
    await client.connect();
    
    // Setup test data
    await client.query(`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
      )
    `);
  });

  afterAll(async () => {
    // Cleanup test data
    await client.query('DROP TABLE IF EXISTS users CASCADE');
    await client.end();
  });
});
```

### API Setup and Teardown

```typescript
// test/integration/api-setup.test.ts
import { describe, beforeAll, afterAll } from '@jest/globals';
import request from 'supertest';
import app from '../src/app';

describe('API Integration', () => {
  let server: any;

  beforeAll(async () => {
    server = app.listen(3000);
  });

  afterAll(async () => {
    server.close();
  });
});
```

### Container Setup and Teardown

```typescript
// test/integration/container-setup.test.ts
import { describe, beforeEach, afterEach } from '@jest/globals';
import { PostgreSqlContainer } from 'testcontainers';

describe('Container Integration', () => {
  let container: StartedPostgreSqlContainer;
  let connection: any;

  beforeEach(async () => {
    container = await new PostgreSqlContainer('postgres:15-alpine').start();
    connection = await container.getConnectionString();
  });

  afterEach(async () => {
    await container.stop();
  });
});
```

---

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/integration-tests.yml
name: Integration Tests

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      - postgres
      - redis
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run integration tests
        run: npm test -- testPathPattern='integration/**/*.test.ts'

      - name: Upload coverage
        if: always()
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
```

### GitLab CI

```yaml
# .gitlab-ci.yml
stages:
  test:
  stage: test
    services:
      - postgres
      - redis
    script:
      - npm ci
      - npm test -- testPathPattern='integration/**/*.test.ts'
    coverage: '/coverage/'
```

---

## Best Practices

### 1. Use Test Containers

```typescript
// Good: Use testcontainers for real infrastructure
import { PostgreSqlContainer } from 'testcontainers';

test('database integration', async () => {
  const container = await new PostgreSqlContainer('postgres:15-alpine').start();
  const connection = await container.getConnectionString();
  // Use real database
});

// Bad: Use mocks for infrastructure
test('database integration', async () => {
  const mockDb = { users: [] };
  // Use mocked database
});
```

### 2. Isolate Tests

```typescript
// Good: Each test is independent
test('test 1', async () => {
  const user = await createTestUser();
  expect(user.id).toBeDefined();
});

test('test 2', async () => {
  const user = await createTestUser();
  expect(user.id).toBeDefined();
});

// Bad: Tests depend on each other
let userId: number;

test('setup user', async () => {
  userId = await createTestUser();
});

test('get user', async () => {
  const user = await getUser(userId);
  expect(user.id).toBe(userId);
});

test('delete user', async () => {
  await deleteUser(userId);
});
```

### 3. Clean Up After Tests

```typescript
// Good: Clean up after each test
test('user lifecycle', async () => {
  const user = await createTestUser();
  
  try {
    const retrieved = await getUser(user.id);
    expect(retrieved).toEqual(user);
  } finally {
    await deleteUser(user.id);
  }
});

// Bad: No cleanup
test('user lifecycle', async () => {
  const user = await createTestUser();
  const retrieved = await getUser(user.id);
  expect(retrieved).toEqual(user);
});
});
```

### 4. Use Descriptive Test Names

```typescript
// Good: Descriptive test names
test('should create user with valid email', async () => {
  const user = await createTestUser('john@example.com');
  expect(user.id).toBeDefined();
});

// Bad: Non-descriptive test names
test('user creation', async () => {
  const user = await createTestUser();
  expect(user.id).toBeDefined();
});
```

### 5. Use Factories for Test Data

```typescript
// Good: Use factories for test data
import { UserFactory } from '../factories/user.factory';

test('should create user', async () => {
  const user = UserFactory.create();
  expect(user.email).toContain('@example.com');
});

// Bad: Hardcode test data
test('should create user', async () => {
  const user = await createTestUser('test@example.com');
  expect(user.email).toContain('@example.com');
});
```

---

## Summary

This skill covers comprehensive integration testing patterns including:

- **Integration Testing Concepts**: Why integration testing, comparison with unit tests
- **Test Containers**: PostgreSQL, Redis, MongoDB with Testcontainers
- **Database Testing**: PostgreSQL and MongoDB integration tests
- **API Testing**: Supertest (Node.js) and httpx (Python)
- **Message Queue Testing**: Redis pub/sub and RabbitMQ integration
- **External Service Mocking**: Mocking external APIs and databases
- **Test Data Management**: Factory pattern and Faker integration
- **Setup and Teardown**: Database, API, and container setup
- **CI/CD Integration**: GitHub Actions and GitLab CI configurations
- **Best Practices**: Test containers, isolate tests, clean up, descriptive names, factories
