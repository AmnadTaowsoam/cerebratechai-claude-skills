# Integration Testing

A comprehensive guide to integration testing patterns for applications.

## Table of Contents

1. [Integration Testing Concepts](#integration-testing-concepts)
2. [Test Containers](#test-containers)
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

### What is Integration Testing?

Integration testing verifies that different modules or services work together correctly.

```
┌─────────────────────────────────────────────────────────────┐
│                   Integration Test Flow                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐              │
│  │   API    │──>│ Database │──>│  Redis   │              │
│  │ Service │  │          │  │         │              │
│  └─────────┘  └─────────┘  └─────────┘              │
│                                                             │
│  Tests verify:                                              │
│  - API can connect to database                              │
│  - API can read/write from Redis                             │
│  - Database transactions work correctly                         │
│  - Caching works as expected                                 │
└─────────────────────────────────────────────────────────────┘
```

### Integration vs Unit Testing

| Aspect | Unit Testing | Integration Testing |
|---------|---------------|----------------------|
| Scope | Single function/class | Multiple components/services |
| Dependencies | Mocked | Real or test containers |
| Speed | Fast | Slower |
| Isolation | High | Lower |
| Purpose | Verify logic | Verify integration |

---

## Test Containers

### Setup with Testcontainers (Node.js)

```typescript
import { GenericContainer, StartedTestContainer } from 'testcontainers';

describe('Integration Tests', () => {
  let postgresContainer: StartedTestContainer;
  let redisContainer: StartedTestContainer;

  beforeAll(async () => {
    // Start PostgreSQL container
    postgresContainer = await new GenericContainer('postgres:15')
      .withExposedPorts(5432)
      .withEnvironment({
        POSTGRES_USER: 'test',
        POSTGRES_PASSWORD: 'test',
        POSTGRES_DB: 'testdb',
      })
      .start();

    // Start Redis container
    redisContainer = await new GenericContainer('redis:7-alpine')
      .withExposedPorts(6379)
      .start();
  });

  afterAll(async () => {
    await postgresContainer.stop();
    await redisContainer.stop();
  });

  it('should connect to PostgreSQL', async () => {
    const port = postgresContainer.getMappedPort(5432);
    const client = new Client({
      host: 'localhost',
      port,
      user: 'test',
      password: 'test',
      database: 'testdb',
    });

    await client.connect();
    const result = await client.query('SELECT NOW()');
    expect(result.rows.length).toBe(1);
    await client.end();
  });
});
```

### Setup with Testcontainers (Python)

```python
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer

@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        postgres.with_exposed_ports(5432)
        postgres.with_env("POSTGRES_USER", "test")
        postgres.with_env("POSTGRES_PASSWORD", "test")
        postgres.with_env("POSTGRES_DB", "testdb")
        postgres.start()
        yield postgres

@pytest.fixture(scope="session")
def redis_container():
    with RedisContainer("redis:7-alpine") as redis:
        redis.with_exposed_ports(6379)
        redis.start()
        yield redis

def test_postgres_connection(postgres_container):
    port = postgres_container.get_exposed_port(5432)
    conn = psycopg2.connect(
        host="localhost",
        port=port,
        user="test",
        password="test",
        dbname="testdb"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT NOW()")
    result = cursor.fetchone()
    assert result is not None
    conn.close()
```

### Docker Compose for Tests

```yaml
# docker-compose.test.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: testdb
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
```

```bash
# Start test containers
docker-compose -f docker-compose.test.yml up -d

# Run tests
npm test

# Stop test containers
docker-compose -f docker-compose.test.yml down
```

---

## Database Testing

### PostgreSQL Testing (Node.js)

```typescript
import { Pool } from 'pg';
import { GenericContainer, StartedTestContainer } from 'testcontainers';

describe('Database Integration', () => {
  let container: StartedTestContainer;
  let pool: Pool;

  beforeAll(async () => {
    container = await new GenericContainer('postgres:15')
      .withExposedPorts(5432)
      .withEnvironment({
        POSTGRES_USER: 'test',
        POSTGRES_PASSWORD: 'test',
        POSTGRES_DB: 'testdb',
      })
      .start();

    const port = container.getMappedPort(5432);
    pool = new Pool({
      host: 'localhost',
      port,
      user: 'test',
      password: 'test',
      database: 'testdb',
    });
  });

  afterAll(async () => {
    await pool.end();
    await container.stop();
  });

  beforeEach(async () => {
    // Clean database before each test
    await pool.query('TRUNCATE TABLE users CASCADE');
  });

  it('should create user', async () => {
    await pool.query(
      'INSERT INTO users (name, email) VALUES ($1, $2)',
      ['John Doe', 'john@example.com']
    );

    const result = await pool.query('SELECT * FROM users');
    expect(result.rows.length).toBe(1);
    expect(result.rows[0].name).toBe('John Doe');
  });

  it('should update user', async () => {
    await pool.query(
      'INSERT INTO users (name, email) VALUES ($1, $2)',
      ['John Doe', 'john@example.com']
    );

    await pool.query(
      'UPDATE users SET name = $1 WHERE email = $2',
      ['Jane Doe', 'john@example.com']
    );

    const result = await pool.query('SELECT * FROM users WHERE email = $1', ['john@example.com']);
    expect(result.rows[0].name).toBe('Jane Doe');
  });

  it('should delete user', async () => {
    await pool.query(
      'INSERT INTO users (name, email) VALUES ($1, $2)',
      ['John Doe', 'john@example.com']
    );

    await pool.query('DELETE FROM users WHERE email = $1', ['john@example.com']);

    const result = await pool.query('SELECT * FROM users');
    expect(result.rows.length).toBe(0);
  });
});
```

### PostgreSQL Testing (Python)

```python
import pytest
import psycopg2
from testcontainers.postgres import PostgresContainer

@pytest.fixture(scope="session")
def db_connection():
    with PostgresContainer("postgres:15") as postgres:
        postgres.with_exposed_ports(5432)
        postgres.with_env("POSTGRES_USER", "test")
        postgres.with_env("POSTGRES_PASSWORD", "test")
        postgres.with_env("POSTGRES_DB", "testdb")
        postgres.start()

        port = postgres.get_exposed_port(5432)
        conn = psycopg2.connect(
            host="localhost",
            port=port,
            user="test",
            password="test",
            dbname="testdb"
        )
        yield conn
        conn.close()

@pytest.fixture(autouse=True)
def clean_database(db_connection):
    yield
    cursor = db_connection.cursor()
    cursor.execute("TRUNCATE TABLE users CASCADE")
    db_connection.commit()

def test_create_user(db_connection):
    cursor = db_connection.cursor()
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        ("John Doe", "john@example.com")
    )
    db_connection.commit()

    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    assert len(result) == 1
    assert result[0][1] == "John Doe"

def test_update_user(db_connection):
    cursor = db_connection.cursor()
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s)",
        ("John Doe", "john@example.com")
    )
    db_connection.commit()

    cursor.execute(
        "UPDATE users SET name = %s WHERE email = %s",
        ("Jane Doe", "john@example.com")
    )
    db_connection.commit()

    cursor.execute("SELECT * FROM users WHERE email = %s", ("john@example.com",))
    result = cursor.fetchone()
    assert result[1] == "Jane Doe"
```

### MongoDB Testing

```typescript
import { MongoClient, Db } from 'mongodb';
import { GenericContainer, StartedTestContainer } from 'testcontainers';

describe('MongoDB Integration', () => {
  let container: StartedTestContainer;
  let client: MongoClient;
  let db: Db;

  beforeAll(async () => {
    container = await new GenericContainer('mongo:6')
      .withExposedPorts(27017)
      .start();

    const port = container.getMappedPort(27017);
    client = new MongoClient(`mongodb://localhost:${port}`);
    await client.connect();
    db = client.db('testdb');
  });

  afterAll(async () => {
    await client.close();
    await container.stop();
  });

  beforeEach(async () => {
    await db.collection('users').deleteMany({});
  });

  it('should create user', async () => {
    await db.collection('users').insertOne({
      name: 'John Doe',
      email: 'john@example.com',
    });

    const count = await db.collection('users').countDocuments();
    expect(count).toBe(1);
  });

  it('should find user', async () => {
    await db.collection('users').insertOne({
      name: 'John Doe',
      email: 'john@example.com',
    });

    const user = await db.collection('users').findOne({ email: 'john@example.com' });
    expect(user?.name).toBe('John Doe');
  });
});
```

---

## API Testing

### Supertest (Node.js)

```typescript
import request from 'supertest';
import { app } from '../app';

describe('API Integration', () => {
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
    const createResponse = await request(app)
      .post('/api/users')
      .send({
        name: 'John Doe',
        email: 'john@example.com',
      })
      .expect(201);

    const response = await request(app)
      .get(`/api/users/${createResponse.body.id}`)
      .expect(200)
      .expect('Content-Type', /json/);

    expect(response.body.name).toBe('John Doe');
  });

  it('should return 404 for non-existent user', async () => {
    const response = await request(app)
      .get('/api/users/999')
      .expect(404);

    expect(response.body).toHaveProperty('error');
  });
});
```

### HTTPX (Python)

```python
import pytest
from httpx import AsyncClient
from myapp.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        "/api/users",
        json={
            "name": "John Doe",
            "email": "john@example.com"
        }
    )

    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["name"] == "John Doe"

@pytest.mark.asyncio
async def test_get_user(client):
    create_response = await client.post(
        "/api/users",
        json={
            "name": "John Doe",
            "email": "john@example.com"
        }
    )

    response = await client.get(f"/api/users/{create_response.json()['id']}")

    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"

@pytest.mark.asyncio
async def test_not_found(client):
    response = await client.get("/api/users/999")
    assert response.status_code == 404
```

### Authentication Testing

```typescript
import request from 'supertest';
import { app } from '../app';

describe('Authentication Integration', () => {
  let authToken: string;

  it('should login', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({
        email: 'user@example.com',
        password: 'password',
      })
      .expect(200);

    expect(response.body).toHaveProperty('token');
    authToken = response.body.token;
  });

  it('should access protected endpoint', async () => {
    const response = await request(app)
      .get('/api/protected')
      .set('Authorization', `Bearer ${authToken}`)
      .expect(200);

    expect(response.body).toHaveProperty('data');
  });

  it('should reject without token', async () => {
    const response = await request(app)
      .get('/api/protected')
      .expect(401);
  });
});
```

---

## Message Queue Testing

### Redis Queue Testing

```typescript
import { createClient } from 'redis';
import { GenericContainer, StartedTestContainer } from 'testcontainers';

describe('Redis Queue Integration', () => {
  let container: StartedTestContainer;
  let client: ReturnType<typeof createClient>;

  beforeAll(async () => {
    container = await new GenericContainer('redis:7-alpine')
      .withExposedPorts(6379)
      .start();

    const port = container.getMappedPort(6379);
    client = createClient({ url: `redis://localhost:${port}` });
    await client.connect();
  });

  afterAll(async () => {
    await client.quit();
    await container.stop();
  });

  it('should enqueue and dequeue', async () => {
    await client.lPush('queue', JSON.stringify({ id: 1, task: 'process' }));

    const item = await client.rPop('queue');
    const data = JSON.parse(item!);

    expect(data.id).toBe(1);
    expect(data.task).toBe('process');
  });
});
```

### RabbitMQ Testing

```typescript
import { connect, Channel, Connection } from 'amqplib';
import { GenericContainer, StartedTestContainer } from 'testcontainers';

describe('RabbitMQ Integration', () => {
  let container: StartedTestContainer;
  let connection: Connection;
  let channel: Channel;

  beforeAll(async () => {
    container = await new GenericContainer('rabbitmq:3-management')
      .withExposedPorts(5672, 15672)
      .start();

    const port = container.getMappedPort(5672);
    connection = await connect(`amqp://localhost:${port}`);
    channel = await connection.createChannel();
    await channel.assertQueue('test-queue');
  });

  afterAll(async () => {
    await channel.close();
    await connection.close();
    await container.stop();
  });

  it('should publish and consume message', async () => {
    const message = { id: 1, data: 'test' };

    await channel.sendToQueue('test-queue', Buffer.from(JSON.stringify(message)));

    await new Promise((resolve) => {
      channel.consume('test-queue', (msg) => {
        const data = JSON.parse(msg.content.toString());
        expect(data.id).toBe(1);
        expect(data.data).toBe('test');
        resolve(null);
      });
    });
  });
});
```

---

## External Service Mocking

### Mocking External API (Node.js)

```typescript
import { setupServer } from 'msw/node';
import { rest } from 'msw';
import request from 'supertest';
import { app } from '../app';

const server = setupServer();

describe('External API Integration', () => {
  beforeAll(() => {
    server.use(
      rest.get('https://api.example.com/users/:id', (req, res, ctx) => {
        return res(
          ctx.json({
            id: req.params.id,
            name: 'John Doe',
            email: 'john@example.com',
          })
        );
      })
    );
  });

  afterAll(() => server.close());

  it('should fetch user from external API', async () => {
    const response = await request(app)
      .get('/api/users/1')
      .expect(200);

    expect(response.body).toHaveProperty('name', 'John Doe');
  });
});
```

### Mocking External API (Python)

```python
import pytest
from unittest.mock import patch
from myapp.services import external_api_service

@pytest.mark.asyncio
async def test_fetch_user_from_external_api():
    mock_response = {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com"
    }

    with patch("myapp.services.external_api_service.requests.get") as mock_get:
        mock_get.return_value.json.return_value = mock_response

        user = await external_api_service.fetch_user(1)

        assert user["name"] == "John Doe"
        assert user["email"] == "john@example.com"
```

---

## Test Data Management

### Seeding Test Data

```typescript
import { Pool } from 'pg';

describe('Test Data Management', () => {
  let pool: Pool;

  beforeAll(async () => {
    pool = new Pool({ /* config */ });
  });

  beforeEach(async () => {
    // Clean database
    await pool.query('TRUNCATE TABLE users CASCADE');

    // Seed test data
    await pool.query(`
      INSERT INTO users (name, email) VALUES
        ('John Doe', 'john@example.com'),
        ('Jane Doe', 'jane@example.com')
    `);
  });

  it('should find all users', async () => {
    const result = await pool.query('SELECT * FROM users');
    expect(result.rows.length).toBe(2);
  });
});
```

### Factory Pattern

```typescript
// factories/userFactory.ts
export class UserFactory {
  static create(overrides = {}) {
    return {
      name: 'John Doe',
      email: 'john@example.com',
      ...overrides,
    };
  }
}

// Usage in tests
import { UserFactory } from '../factories/userFactory';

describe('User Factory', () => {
  it('should use default values', () => {
    const user = UserFactory.create();
    expect(user.name).toBe('John Doe');
    expect(user.email).toBe('john@example.com');
  });

  it('should override values', () => {
    const user = UserFactory.create({ name: 'Jane Doe' });
    expect(user.name).toBe('Jane Doe');
    expect(user.email).toBe('john@example.com');
  });
});
```

---

## Setup and Teardown

### Setup and Teardown (Node.js)

```typescript
describe('Setup and Teardown', () => {
  let pool: Pool;
  let client: RedisClient;

  beforeAll(async () => {
    // Setup once before all tests
    pool = new Pool({ /* config */ });
    client = createClient();
    await client.connect();
  });

  afterAll(async () => {
    // Cleanup once after all tests
    await pool.end();
    await client.quit();
  });

  beforeEach(async () => {
    // Setup before each test
    await pool.query('TRUNCATE TABLE users CASCADE');
    await client.flushDb();
  });

  afterEach(async () => {
    // Cleanup after each test
    // Additional cleanup if needed
  });
});
```

### Setup and Teardown (Python)

```python
import pytest

@pytest.fixture(scope="session")
def session_resources():
    # Setup once before all tests
    db = Database()
    db.connect()
    yield db
    # Cleanup once after all tests
    db.disconnect()

@pytest.fixture(autouse=True)
def clean_database(session_resources):
    # Setup before each test
    session_resources.execute("TRUNCATE TABLE users CASCADE")
    yield
    # Cleanup after each test
    pass
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Integration Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 18

      - name: Install dependencies
        run: npm ci

      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/testdb
          REDIS_URL: redis://localhost:6379
```

### GitLab CI

```yaml
integration-test:
  stage: test
  services:
    - postgres:15
    - redis:7-alpine

  variables:
    POSTGRES_USER: test
    POSTGRES_PASSWORD: test
    POSTGRES_DB: testdb
    DATABASE_URL: postgresql://test:test@postgres:5432/testdb
    REDIS_URL: redis://redis:6379

  script:
    - npm ci
    - npm run test:integration
```

---

## Best Practices

### 1. Use Test Containers

```typescript
// Use test containers for real dependencies
const container = await new GenericContainer('postgres:15')
  .withExposedPorts(5432)
  .start();
```

### 2. Clean Database Between Tests

```typescript
beforeEach(async () => {
  await pool.query('TRUNCATE TABLE users CASCADE');
});
```

### 3. Use Factories for Test Data

```typescript
const user = UserFactory.create({ name: 'Jane Doe' });
```

### 4. Test Real Integrations

```typescript
// Test real API endpoints
await request(app).post('/api/users').send({ name: 'John Doe' });
```

### 5. Mock External Services

```typescript
// Mock external APIs
server.use(
  rest.get('https://api.example.com/users/:id', (req, res, ctx) => {
    return res(ctx.json({ id: req.params.id, name: 'John Doe' }));
  })
);
```

### 6. Use Proper Setup/Teardown

```typescript
beforeAll(async () => {
  // Setup
});

afterAll(async () => {
  // Teardown
});
```

### 7. Test Error Cases

```typescript
it('should return 404 for non-existent user', async () => {
  await request(app).get('/api/users/999').expect(404);
});
```

### 8. Use Descriptive Test Names

```typescript
it('should create user with valid data', async () => {
  // ...
});
```

### 9. Keep Tests Independent

```typescript
// Each test should be able to run independently
it('test 1', async () => {
  // ...
});

it('test 2', async () => {
  // ...
});
```

### 10. Run in CI

```yaml
# Run integration tests in CI
- name: Run integration tests
  run: npm run test:integration
```

---

## Resources

- [Testcontainers Documentation](https://www.testcontainers.org/)
- [Supertest Documentation](https://github.com/visionmedia/supertest)
- [HTTPX Documentation](https://www.python-httpx.org/)
- [MSW Documentation](https://mswjs.io/)
