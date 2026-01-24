# Fastify REST API Patterns

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

Fastify เป็น high-performance Node.js web framework ที่ focused บน speed และ low overhead โดยมี built-in schema validation และ serialization ซึ่งช่วยให้ developers สร้าง APIs ที่ production-ready อย่างรวดเร็ว

Fastify ประกอบด้วย:
- **High Performance** - 2x faster กว่า Express
- **JSON Schema Validation** - Built-in validation ด้วย JSON Schema
- **Fast Serialization** - Optimized JSON serialization
- **TypeScript Support** - First-class TypeScript support
- **Plugin System** - Extensible plugin architecture
- **Low Overhead** - Minimal request overhead

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **เพิ่ม Performance** - Fastify ช่วยเพิ่ม API performance ได้ถึง 2-3x
2. **ลด Infrastructure Cost** - Higher throughput ช่วยลด infrastructure cost
3. **เพิ่ม Developer Experience** - Built-in validation และ serialization ช่วยเพิ่ม DX
4. **ลด Bugs** - Type-safe validation ช่วยลด bugs
5. **ปรับปรุง Scalability** - High-performance framework ช่วยเพิ่ม scalability

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Performance-First** - Fastify ต้องเป็น performance-first framework
2. **Type-Safe** - APIs ต้อง type-safe ด้วย TypeScript
3. **Validated** - APIs ต้อง validated ด้วย JSON Schema
4. **Fast** - APIs ต้อง fast และ low-latency
5. **Production-Ready** - APIs ต้อง production-ready ด้วย monitoring

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

Fastify ประกอบด้วย:

1. **Application** - Fastify application instance
2. **Router** - Routing system สำหรับ mapping URLs ไปยัง handlers
3. **JSON Schema** - JSON Schema validation
4. **Serialization** - Fast JSON serialization
5. **Hooks** - Request/response lifecycle hooks
6. **Plugins** - Extensible plugin system
7. **Error Handling** - Built-in error handling

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              Fastify Architecture                   │
├─────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Client Layer                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Browser    │  │  Mobile     │  │  API Client │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Plugin Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  CORS       │  │  Helmet     │  │  Swagger    │  │   │
│  │  │  Plugin     │  │  Plugin     │  │  Plugin     │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Hook Layer                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  onRequest   │  │  preHandler │  │  onResponse │  │   │
│  │  │  Hook        │  │  Hook       │  │  Hook       │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Routing Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Routes     │  │  Handlers    │  │  Services   │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Data Layer                           │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  JSON Schema │  │  Models     │  │  Repositories│  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Initialize Fastify App**

```typescript
// src/app.ts
import Fastify from 'fastify'

export async function buildApp(): Promise<FastifyInstance> {
  const app = Fastify({
    logger: {
      level: 'info',
    },
  })

  return app
}
```

**Step 2: Add Routes**

```typescript
// src/routes/users/index.ts
import { FastifyPluginAsync } from 'fastify'

const userRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.get('/users', async (request, reply) => {
    return { users: [] }
  })
}

export default userRoutes
```

**Step 3: Include Routes**

```typescript
// src/app.ts
import { buildApp } from './app'

const app = await buildApp()

await app.register(userRoutes, { prefix: '/api/v1' })
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| Fastify | Web Framework | ^4.25.0 | MIT |
| TypeScript | Type Safety | ^5.3.0 | Apache-2.0 |
| @fastify/cors | CORS Plugin | ^8.4.0 | MIT |
| @fastify/helmet | Security Plugin | ^11.1.0 | MIT |
| @fastify/swagger | API Documentation | ^8.12.0 | MIT |
| @fastify/jwt | JWT Authentication | ^7.2.0 | MIT |
| @fastify/rate-limit | Rate Limiting | ^9.1.0 | MIT |
| @fastify/swagger-ui | Swagger UI | ^2.1.0 | MIT |
| pino | Logging Library | ^8.16.0 | MIT |

### 3.2 Configuration Essentials

**TypeScript Configuration:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

**Fastify Configuration:**
```typescript
// src/config/fastify.ts
import { FastifyInstance } from 'fastify'

export async function buildApp(): Promise<FastifyInstance> {
  const app = Fastify({
    logger: {
      level: 'info',
      transport: {
        target: 'pino-pretty',
        options: {
          translateTime: 'HH:MM:ss Z',
          ignore: 'pid,hostname',
        },
      },
    },
    // Request ID tracking
    requestIdHeader: 'x-request-id',
    requestIdLogLabel: 'reqId',
    // Trust proxy (for production behind reverse proxy)
    trustProxy: process.env.NODE_ENV === 'production',
    // Body size limits
    bodyLimit: 1048576, // 1MB
    // Timeout
    connectionTimeout: 10000,
    keepAliveTimeout: 5000,
  })

  return app
}
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **OpenAPI 3.0** - OpenAPI Specification
- **REST API Standards** - RESTful API Design Standards
- **OWASP** - Security Best Practices
- **GDPR** - Data Protection สำหรับ API Data
- **HIPAA** - Healthcare Data Protection

### 4.2 Security Protocol

Fastify ต้องปฏิบัติตามหลักความปลอดภัย:

1. **Input Validation** - Validate ข้อมูลทั้ง client และ server
2. **Authentication** - ใช้ JWT หรือ OAuth2
3. **Authorization** - Implement role-based access control
4. **CORS** - Configure CORS อย่างเหมาะสม
5. **HTTPS** - ใช้ HTTPS สำหรับ production
6. **Rate Limiting** - จำกัดจำนวน requests
7. **Security Headers** - ใช้ Helmet สำหรับ security headers

### 4.3 Explainability

Fastify ต้องสามารถอธิบายได้ว่า:

1. **Request Flow** - ทำไม request ถูก process อย่างไร
2. **Validation** - ทำไม data ถูก validate อย่างไร
3. **Error Handling** - ทำไม errors ถูก handle อย่างไร
4. **Response Format** - ทำไม responses ถูก serialize อย่างไร

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Response Time | Average response time | < 20ms |
| Throughput | Requests per second | > 3000 req/s |
| Error Rate | Errors / Total Requests | < 1% |
| Memory Usage | Memory per request | < 2 MB |
| CPU Usage | CPU utilization | < 50% |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **Response Time** - Average response time
2. **Throughput** - Requests per second
3. **Error Rate** - Error rate
4. **Memory Usage** - Memory usage

**Business Metrics:**

1. **API Availability** - API uptime
2. **User Satisfaction** - CSAT score
3. **Support Tickets** - Support tickets จาก API issues
4. **Time to Resolution** - Average time to resolve issues

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Initialize Fastify app
- Setup project structure
- Add basic routes
- Implement JSON Schema validation

**Phase 2: Advanced Features (Week 3-4)**
- Add hooks
- Implement authentication
- Add plugins
- Setup database integration

**Phase 3: Integration (Week 5-6)**
- Add Swagger documentation
- Implement rate limiting
- Add caching
- Setup monitoring

**Phase 4: Production (Week 7-8)**
- Optimize performance
- Setup load testing
- Documentation and training
- Best practices documentation

### 6.2 Pitfalls to Avoid

1. **Poor JSON Schema Design** - ไม่ design JSON schemas อย่างถูกต้อง
2. **Missing Error Handling** - ไม่ handle errors อย่างเหมาะสม
3. **No Request ID** - ไม่ track request IDs
4. **Poor Performance** - ไม่ optimize performance
5. **No Monitoring** - ไม่ monitor performance
6. **Poor TypeScript** - ไม่ใช้ TypeScript อย่างถูกต้อง

### 6.3 Best Practices Checklist

- [ ] ใช้ TypeScript สำหรับ type safety
- [ ] Implement JSON Schema validation
- [ ] Use Fastify hooks สำหรับ cross-cutting concerns
- [ ] Implement proper error handling
- [ ] Add authentication แล authorization
- [ ] Use plugins สำหรับ reusable functionality
- [ ] Implement request ID tracking
- [ ] Use async/await สำหรับ async operations
- [ ] Test endpoints ด้วย Jest
- [ ] Use Swagger documentation
- [ ] Add CORS configuration
- [ ] Implement rate limiting
- [ ] Use caching สำหรับ performance
- [ ] Monitor performance แล errors
- [ ] Optimize serialization
- [ ] Use connection pooling

---

## 7. Implementation Examples

### 7.1 Project Setup

**Installation:**
```bash
# Create new project
mkdir my-fastify-api
cd my-fastify-api
npm init -y

# Install Fastify and TypeScript
npm install fastify
npm install -D typescript @types/node tsx

# Install common dependencies
npm install @fastify/cors @fastify/helmet @fastify/rate-limit
npm install @fastify/swagger @fastify/swagger-ui
npm install @fastify/jwt @fastify/cookie
npm install dotenv
```

**TypeScript Configuration:**
```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "moduleResolution": "node",
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

**Project Structure:**
```
src/
├── config/
│   ├── env.ts              # Environment variables
│   └── fastify.ts          # Fastify configuration
├── plugins/
│   ├── cors.ts             # CORS plugin
│   ├── helmet.ts           # Security plugin
│   ├── swagger.ts          # API documentation
│   └── sensible.ts         # Utility decorators
├── routes/
│   ├── index.ts            # Route registration
│   ├── users/
│   │   ├── index.ts        # User routes
│   │   ├── schemas.ts      # Validation schemas
│   │   └── handlers.ts     # Route handlers
│   └── auth/
│       ├── index.ts
│       ├── schemas.ts
│       └── handlers.ts
├── services/
│   ├── user.service.ts     # Business logic
│   └── auth.service.ts
├── repositories/
│   └── user.repository.ts  # Data access
├── models/
│   └── user.model.ts       # Type definitions
├── utils/
│   ├── errors.ts           # Custom errors
│   └── logger.ts           # Logging utility
├── hooks/
│   ├── auth.hook.ts        # Authentication hook
│   └── logging.hook.ts     # Request logging
├── app.ts                  # Fastify app setup
└── server.ts               # Server entry point
```

### 7.2 Basic Server Configuration

**Environment Variables:**
```typescript
// src/config/env.ts
import { config } from 'dotenv';

config();

interface EnvConfig {
  NODE_ENV: string;
  PORT: number;
  HOST: string;
  LOG_LEVEL: string;
  DATABASE_URL: string;
  JWT_SECRET: string;
  CORS_ORIGIN: string;
}

function validateEnv(): EnvConfig {
  const requiredVars = [
    'NODE_ENV',
    'PORT',
    'HOST',
    'DATABASE_URL',
    'JWT_SECRET',
  ];

  for (const varName of requiredVars) {
    if (!process.env[varName]) {
      throw new Error(`Missing required environment variable: ${varName}`);
    }
  }

  return {
    NODE_ENV: process.env.NODE_ENV!,
    PORT: parseInt(process.env.PORT!, 10),
    HOST: process.env.HOST!,
    LOG_LEVEL: process.env.LOG_LEVEL || 'info',
    DATABASE_URL: process.env.DATABASE_URL!,
    JWT_SECRET: process.env.JWT_SECRET!,
    CORS_ORIGIN: process.env.CORS_ORIGIN || '*',
  };
}

export const env = validateEnv();
```

**App Configuration:**
```typescript
// src/app.ts
import Fastify, { FastifyInstance } from 'fastify';
import { env } from './config/env';

export async function buildApp(): Promise<FastifyInstance> {
  const app = Fastify({
    logger: {
      level: env.LOG_LEVEL,
      transport: {
        target: 'pino-pretty',
        options: {
          translateTime: 'HH:MM:ss Z',
          ignore: 'pid,hostname',
        },
      },
    },
    // Request ID tracking
    requestIdHeader: 'x-request-id',
    requestIdLogLabel: 'reqId',
    // Trust proxy (for production behind reverse proxy)
    trustProxy: env.NODE_ENV === 'production',
    // Body size limits
    bodyLimit: 1048576, // 1MB
    // Timeout
    connectionTimeout: 10000,
    keepAliveTimeout: 5000,
  });

  // Register plugins
  await app.register(import('./plugins/cors'));
  await app.register(import('./plugins/helmet'));
  await app.register(import('./plugins/sensible'));
  await app.register(import('./plugins/swagger'));

  // Register routes
  await app.register(import('./routes'), { prefix: '/api/v1' });

  // Global error handler
  app.setErrorHandler((error, request, reply) => {
    request.log.error(error);

    const statusCode = error.statusCode || 500;
    const message = error.message || 'Internal Server Error';

    reply.status(statusCode).send({
      success: false,
      error: {
        message,
        statusCode,
        ...(env.NODE_ENV === 'development' && { stack: error.stack }),
      },
    });
  });

  return app;
}
```

**Server Entry Point:**
```typescript
// src/server.ts
import { buildApp } from './app';
import { env } from './config/env';

async function start() {
  try {
    const app = await buildApp();

    await app.listen({
      port: env.PORT,
      host: env.HOST,
    });

    // Graceful shutdown
    const signals = ['SIGINT', 'SIGTERM'];
    signals.forEach((signal) => {
      process.on(signal, async () => {
        app.log.info(`Received ${signal}, closing server...`);
        await app.close();
        process.exit(0);
      });
    });
  } catch (error) {
    console.error('Error starting server:', error);
    process.exit(1);
  }
}

start();
```

### 7.3 Routing Patterns

**Basic Routes:**
```typescript
// src/routes/users/index.ts
import { FastifyPluginAsync } from 'fastify';
import { createUser, getUsers, getUser, updateUser, deleteUser } from './handlers';
import { createUserSchema, getUserSchema, updateUserSchema } from './schemas';

const userRoutes: FastifyPluginAsync = async (fastify) => {
  // GET /users - List all users
  fastify.get('/', {
    schema: {
      description: 'Get all users',
      tags: ['users'],
      response: {
        200: {
          type: 'object',
          properties: {
            success: { type: 'boolean' },
            data: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  id: { type: 'string' },
                  email: { type: 'string' },
                  name: { type: 'string' },
                },
              },
            },
          },
        },
      },
    },
  }, getUsers);

  // POST /users - Create user
  fastify.post('/', {
    schema: createUserSchema,
  }, createUser);

  // GET /users/:id - Get user by ID
  fastify.get('/:id', {
    schema: getUserSchema,
  }, getUser);

  // PUT /users/:id - Update user
  fastify.put('/:id', {
    schema: updateUserSchema,
  }, updateUser);

  // DELETE /users/:id - Delete user
  fastify.delete('/:id', {
    schema: {
      description: 'Delete a user',
      tags: ['users'],
      params: {
        type: 'object',
        properties: {
          id: { type: 'string', format: 'uuid' },
        },
        required: ['id'],
      },
    },
  }, deleteUser);
};

export default userRoutes;
```

**Route Handlers:**
```typescript
// src/routes/users/handlers.ts
import { FastifyRequest, FastifyReply } from 'fastify';
import { UserService } from '../../services/user.service';

interface CreateUserBody {
  email: string;
  password: string;
  name: string;
}

interface GetUserParams {
  id: string;
}

interface UpdateUserBody {
  name?: string;
  email?: string;
}

const userService = new UserService();

export async function createUser(
  request: FastifyRequest<{ Body: CreateUserBody }>,
  reply: FastifyReply
) {
  try {
    const user = await userService.create(request.body);

    return reply.status(201).send({
      success: true,
      data: user,
    });
  } catch (error) {
    request.log.error(error);
    throw error;
  }
}

export async function getUsers(
  request: FastifyRequest,
  reply: FastifyReply
) {
  try {
    const users = await userService.findAll();

    return reply.send({
      success: true,
      data: users,
    });
  } catch (error) {
    request.log.error(error);
    throw error;
  }
}

export async function getUser(
  request: FastifyRequest<{ Params: GetUserParams }>,
  reply: FastifyReply
) {
  try {
    const user = await userService.findById(request.params.id);

    if (!user) {
      return reply.notFound('User not found');
    }

    return reply.send({
      success: true,
      data: user,
    });
  } catch (error) {
    request.log.error(error);
    throw error;
  }
}

export async function updateUser(
  request: FastifyRequest<{
    Params: GetUserParams;
    Body: UpdateUserBody;
  }>,
  reply: FastifyReply
) {
  try {
    const user = await userService.update(
      request.params.id,
      request.body
    );

    if (!user) {
      return reply.notFound('User not found');
    }

    return reply.send({
      success: true,
      data: user,
    });
  } catch (error) {
    request.log.error(error);
    throw error;
  }
}

export async function deleteUser(
  request: FastifyRequest<{ Params: GetUserParams }>,
  reply: FastifyReply
) {
  try {
    await userService.delete(request.params.id);

    return reply.status(204).send();
  } catch (error) {
    request.log.error(error);
    throw error;
  }
}
```

**Route Registration:**
```typescript
// src/routes/index.ts
import { FastifyPluginAsync } from 'fastify';

const routes: FastifyPluginAsync = async (fastify) => {
  // Health check
  fastify.get('/health', async () => {
    return {
      status: 'ok',
      timestamp: new Date().toISOString(),
    };
  });

  // Register resource routes
  await fastify.register(import('./users'), { prefix: '/users' });
  await fastify.register(import('./auth'), { prefix: '/auth' });
};

export default routes;
```

### 7.4 Request Validation

**JSON Schema Validation:**
```typescript
// src/routes/users/schemas.ts
import { FastifySchema } from 'fastify';

// User properties schema (reusable)
const userProperties = {
  id: { type: 'string', format: 'uuid' },
  email: { type: 'string', format: 'email' },
  name: { type: 'string', minLength: 2, maxLength: 100 },
  createdAt: { type: 'string', format: 'date-time' },
  updatedAt: { type: 'string', format: 'date-time' },
};

// Create user schema
export const createUserSchema: FastifySchema = {
  description: 'Create a new user',
  tags: ['users'],
  body: {
    type: 'object',
    required: ['email', 'password', 'name'],
    properties: {
      email: { type: 'string', format: 'email' },
      password: {
        type: 'string',
        minLength: 8,
        pattern: '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]',
      },
      name: { type: 'string', minLength: 2, maxLength: 100 },
    },
    additionalProperties: false,
  },
  response: {
    201: {
      type: 'object',
      properties: {
        success: { type: 'boolean' },
        data: {
          type: 'object',
          properties: userProperties,
        },
      },
    },
    400: {
      type: 'object',
      properties: {
        success: { type: 'boolean' },
        error: {
          type: 'object',
          properties: {
            message: { type: 'string' },
            statusCode: { type: 'number' },
          },
        },
      },
    },
  },
};

// Get user schema
export const getUserSchema: FastifySchema = {
  description: 'Get user by ID',
  tags: ['users'],
  params: {
    type: 'object',
    required: ['id'],
    properties: {
      id: { type: 'string', format: 'uuid' },
    },
  },
  response: {
    200: {
      type: 'object',
      properties: {
        success: { type: 'boolean' },
        data: {
          type: 'object',
          properties: userProperties,
        },
      },
    },
    404: {
      type: 'object',
      properties: {
        success: { type: 'boolean' },
        error: {
          type: 'object',
          properties: {
            message: { type: 'string' },
            statusCode: { type: 'number' },
          },
        },
      },
    },
  },
};

// Update user schema
export const updateUserSchema: FastifySchema = {
  description: 'Update a user',
  tags: ['users'],
  params: {
    type: 'object',
    required: ['id'],
    properties: {
      id: { type: 'string', format: 'uuid' },
    },
  },
  body: {
    type: 'object',
    properties: {
      name: { type: 'string', minLength: 2, maxLength: 100 },
      email: { type: 'string', format: 'email' },
    },
    additionalProperties: false,
    minProperties: 1, // At least one field required
  },
  response: {
    200: {
      type: 'object',
      properties: {
        success: { type: 'boolean' },
        data: {
          type: 'object',
          properties: userProperties,
        },
      },
    },
  },
};

// Query parameters schema
export const listUsersSchema: FastifySchema = {
  description: 'List users with pagination',
  tags: ['users'],
  querystring: {
    type: 'object',
    properties: {
      page: { type: 'integer', minimum: 1, default: 1 },
      limit: { type: 'integer', minimum: 1, maximum: 100, default: 10 },
      sort: { type: 'string', enum: ['name', 'email', 'createdAt'], default: 'createdAt' },
      order: { type: 'string', enum: ['asc', 'desc'], default: 'desc' },
      search: { type: 'string', minLength: 2 },
    },
  },
  response: {
    200: {
      type: 'object',
      properties: {
        success: { type: 'boolean' },
        data: {
          type: 'array',
          items: {
            type: 'object',
            properties: userProperties,
          },
        },
        meta: {
          type: 'object',
          properties: {
            page: { type: 'integer' },
            limit: { type: 'integer' },
            total: { type: 'integer' },
            totalPages: { type: 'integer' },
          },
        },
      },
    },
  },
};
```

**Custom Validation:**
```typescript
// Custom validator function
fastify.addHook('preValidation', async (request, reply) => {
  if (request.body && typeof request.body === 'object') {
    const body = request.body as Record<string, unknown>;

    // Custom validation logic
    if (body.email && !isValidEmail(body.email as string)) {
      return reply.badRequest('Invalid email format');
    }
  }
});

function isValidEmail(email: string): boolean {
  // Custom email validation
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

### 7.5 Response Serialization

**Fast JSON Serialization:**
```typescript
// Fastify uses JSON schemas for serialization optimization
const getUserResponse = {
  200: {
    type: 'object',
    properties: {
      success: { type: 'boolean' },
      data: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          email: { type: 'string' },
          name: { type: 'string' },
          // Password is NOT included in schema
          // Fastify will automatically exclude it from response
        },
      },
    },
  },
};

// This is MUCH faster than manually deleting properties
// ✅ Good: Fastify serialization (fast)
fastify.get('/users/:id', {
  schema: { response: getUserResponse },
}, async (request, reply) => {
  const user = await userService.findById(request.params.id);
  return { success: true, data: user };
  // Password field automatically removed by serialization
});

// ❌ Bad: Manual property deletion (slow)
fastify.get('/users/:id', async (request, reply) => {
  const user = await userService.findById(request.params.id);
  delete user.password; // Slow!
  return { success: true, data: user };
});
```

**Custom Serializers:**
```typescript
// src/utils/serializers.ts
import { FastifyReply } from 'fastify';

export function serializeUser(user: any) {
  return {
    id: user.id,
    email: user.email,
    name: user.name,
    createdAt: user.createdAt,
    // Explicitly exclude password and sensitive fields
  };
}

// Use in route handler
export async function getUser(request: FastifyRequest, reply: FastifyReply) {
  const user = await userService.findById(request.params.id);

  return reply.send({
    success: true,
    data: serializeUser(user),
  });
}
```

### 7.6 Error Handling

**Custom Error Classes:**
```typescript
// src/utils/errors.ts
export class AppError extends Error {
  constructor(
    public message: string,
    public statusCode: number = 500,
    public code?: string
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(message: string = 'Validation failed', public details?: any) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

export class NotFoundError extends AppError {
  constructor(message: string = 'Resource not found') {
    super(message, 404, 'NOT_FOUND');
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = 'Unauthorized') {
    super(message, 401, 'UNAUTHORIZED');
  }
}

export class ForbiddenError extends AppError {
  constructor(message: string = 'Forbidden') {
    super(message, 403, 'FORBIDDEN');
  }
}

export class ConflictError extends AppError {
  constructor(message: string) {
    super(message, 409, 'CONFLICT');
  }
}
```

**Global Error Handler:**
```typescript
// src/app.ts
import { FastifyError } from 'fastify';
import { AppError } from './utils/errors';

app.setErrorHandler((error: FastifyError, request, reply) => {
  request.log.error({
    err: error,
    reqId: request.id,
    url: request.url,
    method: request.method,
  });

  // Handle Fastify validation errors
  if (error.validation) {
    return reply.status(400).send({
      success: false,
      error: {
        message: 'Validation error',
        statusCode: 400,
        code: 'VALIDATION_ERROR',
        details: error.validation,
      },
    });
  }

  // Handle custom AppError
  if (error instanceof AppError) {
    return reply.status(error.statusCode).send({
      success: false,
      error: {
        message: error.message,
        statusCode: error.statusCode,
        code: error.code,
        ...(error instanceof ValidationError && { details: error.details }),
      },
    });
  }

  // Handle unknown errors
  const statusCode = error.statusCode || 500;
  const message = error.message || 'Internal Server Error';

  return reply.status(statusCode).send({
    success: false,
    error: {
      message,
      statusCode,
      ...(env.NODE_ENV === 'development' && { stack: error.stack }),
    },
  });
});
```

**Async Error Handling:**
```typescript
// Fastify automatically catches async errors
// No need for try-catch in every handler!

// ✅ Good: Let Fastify handle errors
export async function getUser(request: FastifyRequest, reply: FastifyReply) {
  const user = await userService.findById(request.params.id);

  if (!user) {
    throw new NotFoundError('User not found');
  }

  return reply.send({ success: true, data: user });
}

// ❌ Bad: Unnecessary try-catch
export async function getUser(request: FastifyRequest, reply: FastifyReply) {
  try {
    const user = await userService.findById(request.params.id);

    if (!user) {
      throw new NotFoundError('User not found');
    }

    return reply.send({ success: true, data: user });
  } catch (error) {
    // This is unnecessary! Fastify catches it automatically
    throw error;
  }
}
```

### 7.7 Plugins

**Creating Custom Plugin:**
```typescript
// src/plugins/database.ts
import fp from 'fastify-plugin';
import { FastifyInstance } from 'fastify';
import { PrismaClient } from '@prisma/client';

declare module 'fastify' {
  interface FastifyInstance {
    prisma: PrismaClient;
  }
}

async function databasePlugin(fastify: FastifyInstance) {
  const prisma = new PrismaClient({
    log: ['error', 'warn'],
  });

  // Connect
  await prisma.$connect();
  fastify.log.info('Database connected');

  // Decorate Fastify instance
  fastify.decorate('prisma', prisma);

  // Cleanup on close
  fastify.addHook('onClose', async (instance) => {
    await instance.prisma.$disconnect();
    instance.log.info('Database disconnected');
  });
}

export default fp(databasePlugin, {
  name: 'database',
});
```

**Using Plugins:**
```typescript
// src/app.ts
import database from './plugins/database';

const app = await buildApp();

// Register database plugin
await app.register(database);

// Now you can use app.prisma in all routes
app.get('/users', async (request, reply) => {
  const users = await app.prisma.user.findMany();
  return { success: true, data: users };
});
```

**Common Plugins:**
```typescript
// src/plugins/cors.ts
import fp from 'fastify-plugin';
import cors from '@fastify/cors';
import { env } from '../config/env';

export default fp(async (fastify) => {
  await fastify.register(cors, {
    origin: env.CORS_ORIGIN,
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
    allowedHeaders: ['Content-Type', 'Authorization'],
  });
});

// src/plugins/helmet.ts
import fp from 'fastify-plugin';
import helmet from '@fastify/helmet';

export default fp(async (fastify) => {
  await fastify.register(helmet, {
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        scriptSrc: ["'self'"],
        imgSrc: ["'self'", 'data:', 'https:'],
      },
    },
  });
});

// src/plugins/rate-limit.ts
import fp from 'fastify-plugin';
import rateLimit from '@fastify/rate-limit';

export default fp(async (fastify) => {
  await fastify.register(rateLimit, {
    max: 100,
    timeWindow: '15 minutes',
    cache: 10000,
    allowList: ['127.0.0.1'],
    redis: process.env.REDIS_URL, // Optional: use Redis for distributed rate limiting
  });
});

// src/plugins/swagger.ts
import fp from 'fastify-plugin';
import swagger from '@fastify/swagger';
import swaggerUi from '@fastify/swagger-ui';

export default fp(async (fastify) => {
  await fastify.register(swagger, {
    openapi: {
      info: {
        title: 'My API',
        description: 'API documentation',
        version: '1.0.0',
      },
      servers: [
        {
          url: 'http://localhost:3000',
          description: 'Development server',
        },
      ],
      tags: [
        { name: 'users', description: 'User related endpoints' },
        { name: 'auth', description: 'Authentication endpoints' },
      ],
    },
  });

  await fastify.register(swaggerUi, {
    routePrefix: '/documentation',
    uiConfig: {
      docExpansion: 'list',
      deepLinking: false,
    },
  });
});
```

### 7.8 Middleware (Hooks)

**Hook Types:**
```
Fastify uses hooks instead of traditional middleware:

Request lifecycle hooks (in order):
- onRequest
- preParsing
- preValidation
- preHandler
- preSerialization
- onSend
- onResponse

Application hooks:
- onReady
- onClose
- onRoute
- onRegister
```

**Authentication Hook:**
```typescript
// src/hooks/auth.hook.ts
import { FastifyRequest, FastifyReply } from 'fastify';
import { verifyToken } from '../utils/jwt';
import { UnauthorizedError } from '../utils/errors';

declare module 'fastify' {
  interface FastifyRequest {
    user?: {
      id: string;
      email: string;
      role: string;
    };
  }
}

export async function authHook(
  request: FastifyRequest,
  reply: FastifyReply
) {
  const authHeader = request.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    throw new UnauthorizedError('No token provided');
  }

  const token = authHeader.substring(7);

  try {
    const payload = await verifyToken(token);
    request.user = payload;
  } catch (error) {
    throw new UnauthorizedError('Invalid token');
  }
}

// Usage in routes
fastify.get('/protected', {
  onRequest: authHook, // Add auth hook to this route
}, async (request, reply) => {
  return {
    success: true,
    data: {
      message: 'You are authenticated!',
      user: request.user,
    },
  };
});
```

**Logging Hook:**
```typescript
// src/hooks/logging.hook.ts
import { FastifyRequest, FastifyReply } from 'fastify';

export async function logRequestHook(
  request: FastifyRequest,
  reply: FastifyReply
) {
  request.log.info({
    reqId: request.id,
    method: request.method,
    url: request.url,
    ip: request.ip,
    userAgent: request.headers['user-agent'],
  }, 'Incoming request');
}

export async function logResponseHook(
  request: FastifyRequest,
  reply: FastifyReply
) {
  request.log.info({
    reqId: request.id,
    statusCode: reply.statusCode,
    responseTime: reply.getResponseTime(),
  }, 'Request completed');
}

// Register globally
app.addHook('onRequest', logRequestHook);
app.addHook('onResponse', logResponseHook);
```

**Global Hooks:**
```typescript
// src/app.ts
export async function buildApp() {
  const app = Fastify({...});

  // Global hooks for all routes
  app.addHook('onRequest', async (request, reply) => {
    request.log.info(`${request.method} ${request.url}`);
  });

  app.addHook('preHandler', async (request, reply) => {
    // Add custom headers
    reply.header('X-API-Version', '1.0.0');
  });

  app.addHook('onResponse', async (request, reply) => {
    request.log.info({
      url: request.url,
      statusCode: reply.statusCode,
      responseTime: reply.getResponseTime(),
    });
  });

  return app;
}
```

### 7.9 Authentication & Authorization

**JWT Authentication:**
```typescript
// src/plugins/jwt.ts
import fp from 'fastify-plugin';
import jwt from '@fastify/jwt';
import { env } from '../config/env';

export default fp(async (fastify) => {
  await fastify.register(jwt, {
    secret: env.JWT_SECRET,
    sign: {
      expiresIn: '15m', // Access token expires in 15 minutes
    },
  });
});

// src/routes/auth/handlers.ts
import { FastifyRequest, FastifyReply } from 'fastify';
import bcrypt from 'bcrypt';
import { UnauthorizedError } from '../../utils/errors';

interface LoginBody {
  email: string;
  password: string;
}

export async function login(
  request: FastifyRequest<{ Body: LoginBody }>,
  reply: FastifyReply
) {
  const { email, password } = request.body;

  // Find user
  const user = await request.server.prisma.user.findUnique({
    where: { email },
  });

  if (!user) {
    throw new UnauthorizedError('Invalid credentials');
  }

  // Verify password
  const isValid = await bcrypt.compare(password, user.password);

  if (!isValid) {
    throw new UnauthorizedError('Invalid credentials');
  }

  // Generate tokens
  const accessToken = request.server.jwt.sign({
    id: user.id,
    email: user.email,
    role: user.role,
  });

  const refreshToken = request.server.jwt.sign(
    { id: user.id },
    { expiresIn: '7d' }
  );

  return reply.send({
    success: true,
    data: {
      accessToken,
      refreshToken,
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
      },
    },
  });
}

export async function refreshToken(
  request: FastifyRequest<{ Body: { refreshToken: string } }>,
  reply: FastifyReply
) {
  try {
    const decoded = request.server.jwt.verify(request.body.refreshToken);

    const newAccessToken = request.server.jwt.sign({
      id: decoded.id,
    });

    return reply.send({
      success: true,
      data: { accessToken: newAccessToken },
    });
  } catch (error) {
    throw new UnauthorizedError('Invalid refresh token');
  }
}
```

**Role-Based Authorization:**
```typescript
// src/hooks/authorize.hook.ts
import { FastifyRequest, FastifyReply } from 'fastify';
import { ForbiddenError } from '../utils/errors';

export function authorize(...allowedRoles: string[]) {
  return async (request: FastifyRequest, reply: FastifyReply) => {
    if (!request.user) {
      throw new ForbiddenError('Authentication required');
    }

    if (!allowedRoles.includes(request.user.role)) {
      throw new ForbiddenError('Insufficient permissions');
    }
  };
}

// Usage
fastify.delete('/users/:id', {
  onRequest: [authHook, authorize('admin')],
}, deleteUser);

fastify.post('/posts', {
  onRequest: [authHook, authorize('admin', 'editor')],
}, createPost);
```

### 7.10 Database Integration

**Prisma Integration:**
```typescript
// src/plugins/database.ts
import fp from 'fastify-plugin';
import { FastifyInstance } from 'fastify';
import { PrismaClient } from '@prisma/client';

declare module 'fastify' {
  interface FastifyInstance {
    prisma: PrismaClient;
  }
}

async function databasePlugin(fastify: FastifyInstance) {
  const prisma = new PrismaClient({
    log: env.NODE_ENV === 'development'
      ? ['query', 'error', 'warn']
      : ['error'],
  });

  await prisma.$connect();

  fastify.decorate('prisma', prisma);

  fastify.addHook('onClose', async (instance) => {
    await instance.prisma.$disconnect();
  });
}

export default fp(databasePlugin, {
  name: 'database',
});
```

**Repository Pattern:**
```typescript
// src/repositories/user.repository.ts
import { PrismaClient, User } from '@prisma/client';

export class UserRepository {
  constructor(private prisma: PrismaClient) {}

  async create(data: {
    email: string;
    password: string;
    name: string;
  }): Promise<User> {
    return this.prisma.user.create({ data });
  }

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { id },
    });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { email },
    });
  }

  async findMany(options: {
    skip?: number;
    take?: number;
    orderBy?: any;
    where?: any;
  }): Promise<User[]> {
    return this.prisma.user.findMany(options);
  }

  async update(id: string, data: Partial<User>): Promise<User> {
    return this.prisma.user.update({
      where: { id },
      data,
    });
  }

  async delete(id: string): Promise<User> {
    return this.prisma.user.delete({
      where: { id },
    });
  }

  async count(where?: any): Promise<number> {
    return this.prisma.user.count({ where });
  }
}

// src/services/user.service.ts
import { UserRepository } from '../repositories/user.repository';
import bcrypt from 'bcrypt';

export class UserService {
  constructor(private userRepository: UserRepository) {}

  async create(data: {
    email: string;
    password: string;
    name: string;
  }) {
    // Hash password
    const hashedPassword = await bcrypt.hash(data.password, 10);

    return this.userRepository.create({
      ...data,
      password: hashedPassword,
    });
  }

  async findById(id: string) {
    return this.userRepository.findById(id);
  }

  async findAll(options: {
    page: number;
    limit: number;
    sort?: string;
    order?: 'asc' | 'desc';
  }) {
    const { page, limit, sort = 'createdAt', order = 'desc' } = options;

    const skip = (page - 1) * limit;

    const [users, total] = await Promise.all([
      this.userRepository.findMany({
        skip,
        take: limit,
        orderBy: { [sort]: order },
      }),
      this.userRepository.count(),
    ]);

    return {
      users,
      meta: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    };
  }

  async update(id: string, data: Partial<User>) {
    return this.userRepository.update(id, data);
  }

  async delete(id: string) {
    return this.userRepository.delete(id);
  }
}
```

### 7.11 Testing

**Test Setup:**
```typescript
// test/helper.ts
import { FastifyInstance } from 'fastify';
import { buildApp } from '../src/app';

export async function buildTestApp(): Promise<FastifyInstance> {
  const app = await buildApp();
  await app.ready();
  return app;
}

export async function cleanupTestApp(app: FastifyInstance) {
  await app.close();
}
```

**Unit Tests:**
```typescript
// test/routes/users.test.ts
import { describe, it, beforeAll, afterAll, expect } from '@jest/globals';
import { FastifyInstance } from 'fastify';
import { buildTestApp, cleanupTestApp } from '../helper';

describe('User Routes', () => {
  let app: FastifyInstance;

  beforeAll(async () => {
    app = await buildTestApp();
  });

  afterAll(async () => {
    await cleanupTestApp(app);
  });

  describe('POST /api/v1/users', () => {
    it('should create a new user', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/v1/users',
        payload: {
          email: 'test@example.com',
          password: 'Password123!',
          name: 'Test User',
        },
      });

      expect(response.statusCode).toBe(201);
      expect(response.json()).toMatchObject({
        success: true,
        data: {
          email: 'test@example.com',
          name: 'Test User',
        },
      });
      expect(response.json().data).not.toHaveProperty('password');
    });

    it('should return 400 for invalid email', async () => {
      const response = await app.inject({
        method: 'POST',
        url: '/api/v1/users',
        payload: {
          email: 'invalid-email',
          password: 'Password123!',
          name: 'Test User',
        },
      });

      expect(response.statusCode).toBe(400);
      expect(response.json()).toMatchObject({
        success: false,
        error: {
          code: 'VALIDATION_ERROR',
        },
      });
    });
  });

  describe('GET /api/v1/users/:id', () => {
    it('should get user by id', async () => {
      // Create user first
      const createResponse = await app.inject({
        method: 'POST',
        url: '/api/v1/users',
        payload: {
          email: 'gettest@example.com',
          password: 'Password123!',
          name: 'Get Test User',
        },
      });

      const userId = createResponse.json().data.id;

      // Get user
      const response = await app.inject({
        method: 'GET',
        url: `/api/v1/users/${userId}`,
      });

      expect(response.statusCode).toBe(200);
      expect(response.json()).toMatchObject({
        success: true,
        data: {
          id: userId,
          email: 'gettest@example.com',
        },
      });
    });

    it('should return 404 for non-existent user', async () => {
      const response = await app.inject({
        method: 'GET',
        url: '/api/v1/users/00000000-0000-0000-0000-000000000000',
      });

      expect(response.statusCode).toBe(404);
    });
  });
});
```

**Integration Tests:**
```typescript
// test/integration/auth.test.ts
describe('Authentication Flow', () => {
  let app: FastifyInstance;
  let accessToken: string;

  beforeAll(async () => {
    app = await buildTestApp();
  });

  afterAll(async () => {
    await cleanupTestApp(app);
  });

  it('should complete full auth flow', async () => {
    // 1. Register
    const registerResponse = await app.inject({
      method: 'POST',
      url: '/api/v1/auth/register',
      payload: {
        email: 'authtest@example.com',
        password: 'Password123!',
        name: 'Auth Test User',
      },
    });

    expect(registerResponse.statusCode).toBe(201);

    // 2. Login
    const loginResponse = await app.inject({
      method: 'POST',
      url: '/api/v1/auth/login',
      payload: {
        email: 'authtest@example.com',
        password: 'Password123!',
      },
    });

    expect(loginResponse.statusCode).toBe(200);
    accessToken = loginResponse.json().data.accessToken;
    expect(accessToken).toBeDefined();

    // 3. Access protected route
    const protectedResponse = await app.inject({
      method: 'GET',
      url: '/api/v1/users/me',
      headers: {
        authorization: `Bearer ${accessToken}`,
      },
    });

    expect(protectedResponse.statusCode).toBe(200);
    expect(protectedResponse.json().data.email).toBe('authtest@example.com');
  });
});
```

### 7.12 Performance Optimization

**Caching:**
```typescript
// src/plugins/cache.ts
import fp from 'fastify-plugin';
import cache from '@fastify/caching';

export default fp(async (fastify) => {
  await fastify.register(cache, {
    privacy: 'private',
    expiresIn: 300, // 5 minutes
  });
});

// Usage in routes
fastify.get('/users/:id', {
  config: {
    cache: {
      expiresIn: 60, // Cache for 1 minute
    },
  },
}, async (request, reply) => {
  const user = await userService.findById(request.params.id);
  return { success: true, data: user };
});
```

**Connection Pooling:**
```typescript
// src/plugins/database.ts
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: env.DATABASE_URL,
    },
  },
  log: ['error', 'warn'],
});

// Connection pool settings
log: ['error', 'warn'],
});

// In prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  // Connection pool
  shadowDatabaseUrl = env("SHADOW_DATABASE_URL")
  // Pool size
  pool = {
    timeout = 30
    max_size = 10
    min_size = 2
  }
}
```

**Load Testing:**
```bash
# Install autocannon
npm install -g autocannon

# Run load test
autocannon -c 100 -d 30 http://localhost:3000/api/v1/users

# With payload
autocannon -c 100 -d 30 -m POST \
  -H "Content-Type: application/json" \
  -b '{"email":"test@example.com","password":"Password123!","name":"Test"}' \
  http://localhost:3000/api/v1/users
```

### 7.13 Production Deployment

**Production Configuration:**
```typescript
// src/config/production.ts
export const productionConfig = {
  logger: {
    level: 'warn',
    // Use JSON logging for production
    serializers: {
      req(request) {
        return {
          method: request.method,
          url: request.url,
          headers: request.headers,
          hostname: request.hostname,
          remoteAddress: request.ip,
          remotePort: request.socket.remotePort,
        };
      },
      res(reply) {
        return {
          statusCode: reply.statusCode,
        };
      },
    },
  },
  // Disable request logging in production
  disableRequestLogging: true,
  // Trust proxy headers
  trustProxy: true,
  // Production timeouts
  connectionTimeout: 5000,
  keepAliveTimeout: 5000,
  // Larger body limit
  bodyLimit: 5242880, // 5MB
};
```

**Dockerfile:**
```dockerfile
# Dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package*.json ./

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

CMD ["node", "dist/server.js"]
```

**Docker Compose:**
```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
      - HOST=0.0.0.0
      - DATABASE_URL=postgresql://user:password@db:5432/mydb
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=mydb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

volumes:
  postgres_data:
```

**PM2 Configuration:**
```javascript
// ecosystem.config.js
module.exports = {
  apps: [{
    name: 'api',
    script: './dist/server.js',
    instances: 'max',
    exec_mode: 'cluster',
    env: {
      NODE_ENV: 'production',
    },
    error_file: './logs/error.log',
    out_file: './logs/out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    max_memory_restart: '1G',
  }],
};
```

### 7.14 Best Practices

**✅ DO:**
- **Use JSON Schema for validation and serialization**
  ```typescript
  // Fast and type-safe
  fastify.post('/users', { schema: createUserSchema }, handler);
  ```

- **Leverage Fastify's built-in features**
  ```typescript
  // Use decorators for shared functionality
  fastify.decorate('prisma', prismaClient);
  ```

- **Use async/await consistently**
  ```typescript
  // Fastify handles async errors automatically
  async function handler(request, reply) {
    const user = await userService.findById(id);
    return { success: true, data: user };
  }
  ```

- **Enable request ID tracking**
  ```typescript
  const app = Fastify({
    requestIdHeader: 'x-request-id',
    requestIdLogLabel: 'reqId',
  });
  ```

- **Use plugins for reusable functionality**
  ```typescript
  await app.register(databasePlugin);
  await app.register(authPlugin);
  ```

- **Implement proper error handling**
  ```typescript
  if (!user) {
    throw new NotFoundError('User not found');
  }
  ```

**❌ DON'T:**
- **Don't use Express middleware directly**
  ```typescript
  // ❌ Bad: Express middleware
  app.use(expressMiddleware);

  // ✅ Good: Use Fastify hooks
  app.addHook('onRequest', fastifyHook);
  ```

- **Don't manually delete sensitive fields**
  ```typescript
  // ❌ Bad: Slow
  delete user.password;

  // ✅ Good: Use schema serialization
  schema: { response: { 200: userSchema } }
  ```

- **Don't use synchronous operations**
  ```typescript
  // ❌ Bad
  const file = fs.readFileSync('file.txt');

  // ✅ Good
  const file = await fs.promises.readFile('file.txt');
  ```

- **Don't forget to register plugins before routes**
  ```typescript
  // ❌ Bad: Routes registered before plugins
  await app.register(routes);
  await app.register(database);

  // ✅ Good: Plugins first
  await app.register(database);
  await app.register(routes);
  ```

### 7.15 Checklist

- [ ] JSON schemas for all routes
- [ ] Error handling middleware configured
- [ ] Authentication implemented
- [ ] Request validation on all endpoints
- [ ] Response serialization schemas
- [ ] Database connection pooling
- [ ] Logging configured
- [ ] CORS configured properly
- [ ] Rate limiting enabled
- [ ] Security headers (Helmet)
- [ ] API documentation (Swagger)
- [ ] Tests written (unit + integration)
- [ ] Environment variables validated
- [ ] Production build tested
- [ ] Performance tested (load testing)
- [ ] Request ID tracking enabled
- [ ] Async/await used consistently
- [ ] Fastify hooks used for cross-cutting concerns

---

## 8. Related Skills

- `03-backend-api/error-handling`
- `03-backend-api/validation`
- `03-backend-api/middleware`
- `01-foundations/api-design`
- `14-monitoring-observability`
