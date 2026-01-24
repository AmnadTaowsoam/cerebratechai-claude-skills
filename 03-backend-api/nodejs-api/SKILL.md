# Node.js REST API Patterns

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

Node.js REST API คือ RESTful API ที่ build ด้วย Node.js และ Express.js framework โดยใช้ middleware pattern สำหรับ cross-cutting concerns อย่าง authentication, logging, error handling และ validation

Node.js REST API ประกอบด้วย:
- **Express.js** - Web framework สำหรับ building REST APIs
- **Middleware Pattern** - Chainable middleware สำหรับ request/response processing
- **TypeScript** - Type-safe development ด้วย TypeScript
- **RESTful Design** - REST API design principles และ best practices
- **Layered Architecture** - Controller-Service-Repository pattern สำหรับ separation of concerns

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **เพิ่ม Development Speed** - Node.js ช่วยเพิ่ม development speed ได้ถึง 2-3x
2. **ลด Time-to-Market** - Fast development ช่วยลด time-to-market
3. **ปรับปรุง Maintainability** - Layered architecture ช่วยปรับปรุง maintainability
4. **เพิ่ม Developer Experience** - TypeScript ช่วยเพิ่ม DX ด้วย type safety
5. **ลด Learning Curve** - JavaScript ecosystem มี community support และ resources

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **RESTful** - APIs ต้อง follow RESTful design principles
2. **Type-Safe** - APIs ต้อง type-safe ด้วย TypeScript
3. **Layered** - APIs ต้อง use layered architecture
4. **Middleware-First** - APIs ต้อง use middleware pattern สำหรับ cross-cutting concerns
5. **Async-Ready** - APIs ต้อง support async/await patterns

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

Node.js REST API ประกอบด้วย:

1. **Express.js** - Web framework สำหรับ building REST APIs
2. **Middleware Pattern** - Chainable middleware สำหรับ request/response processing
3. **Controller Layer** - Request handlers สำหรับ HTTP endpoints
4. **Service Layer** - Business logic และ orchestration
5. **Repository Layer** - Data access layer สำหรับ database operations
6. **Dependency Injection** - DI pattern สำหรับ loose coupling
7. **Error Handling** - Centralized error handling ด้วย custom error classes

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              Node.js REST API Architecture           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Client Layer                 │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │  Browser     │  │  Mobile     │  │  API Client│  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │         Middleware Chain                    │  │
│  │  ┌─────────┐  ┌─────────┐  ┌───────────┐  │  │
│  │  │Security  │  │   CORS   │  │  Logging  │  │  │
│  │  └─────────┘  └─────────┘  └───────────┘  │  │
│  │       │              │              │          │  │
│  │       ▼              ▼              ▼          │  │
│  │  ┌─────────┐  ┌─────────┐  ┌───────────┐  │  │
│  │  │ Body     │  │ Request  │  │  Rate     │  │  │
│  │  │ Parser   │  │   ID     │  │  Limit    │  │  │
│  │  └─────────┘  └─────────┘  └───────────┘  │  │
│  │       │              │              │          │  │
│  │       ▼              ▼              ▼          │  │
│  │  ┌─────────┐  ┌─────────┐  ┌───────────┐  │  │
│  │  │ Auth     │  │ Validate │  │  Error    │  │  │
│  │  │          │  │          │  │ Handler  │  │  │
│  │  └─────────┘  └─────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Controller Layer               │  │
│  │  ┌─────────┐  ┌─────────┐  ┌───────────┐  │  │
│  │  │  User     │  │  Auth     │  │  Order    │  │  │
│  │  │ Controller│  │ Controller│  │  Controller│  │  │
│  │  └─────────┘  └─────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Service Layer                  │  │
│  │  ┌─────────┐  ┌─────────┐  ┌───────────┐  │  │
│  │  │  User     │  │  Auth     │  │  Order    │  │  │
│  │  │ Service   │  │  Service   │  │  Service   │  │  │
│  │  └─────────┘  └─────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Repository Layer                │  │
│  │  ┌─────────┐  ┌─────────┐  ┌───────────┐  │  │
│  │  │  User     │  │  Auth     │  │  Order    │  │  │
│  │  │ Repository│  │ Repository│  │  Repository│  │  │
│  │  └─────────┘  └─────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Data Layer                      │  │
│  │  ┌─────────┐  ┌─────────┐  ┌───────────┐  │  │
│  │  │  Database │  │  Cache    │  │  External  │  │  │
│  │  │          │  │          │  │ Services  │  │  │
│  │  └─────────┘  └─────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

1. **Project Setup** - Initialize Node.js project with TypeScript
2. **Project Structure** - Set up layered architecture (controllers, services, repositories)
3. **Middleware Setup** - Configure middleware chain (security, logging, validation)
4. **Controller Implementation** - Implement request handlers for HTTP endpoints
5. **Service Implementation** - Implement business logic layer
6. **Repository Implementation** - Implement data access layer
7. **Dependency Injection** - Set up DI container for loose coupling
8. **Testing** - Write unit and integration tests
9. **Deployment** - Deploy to production with monitoring

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Enterprise Features |
|------|---------|---------------------|
| Express.js | Web framework | Mature ecosystem, middleware support |
| TypeScript | Type-safe development | Static typing, IDE support |
| Zod | Schema validation | Runtime validation, TypeScript integration |
| Prisma | ORM | Type-safe database client, migrations |
| Jest | Testing framework | Fast testing, mocking support |
| ESLint | Linting | Configurable rules, auto-fix |
| Prettier | Code formatting | Consistent code style |

### 3.2 Configuration Essentials

```typescript
// src/config/env.ts
import dotenv from "dotenv"
import { z } from "zod"

dotenv.config()

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
  PORT: z.string().transform(Number).default(3000),
  DATABASE_URL: z.string(),
  JWT_SECRET: z.string(),
  JWT_EXPIRES_IN: z.string().default("1d"),
  REDIS_URL: z.string().optional(),
})

export const config = envSchema.parse(process.env)
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **REST API Design** - Follow REST API design principles
- **HTTP Status Codes** - Use appropriate HTTP status codes
- **JSON API** - Use JSON for request/response format
- **OWASP Security** - Follow OWASP security guidelines
- **GDPR Compliance** - Handle personal data properly

### 4.2 Security Protocol

1. **Security Headers** - Implement security headers (Helmet)
2. **CORS Configuration** - Configure CORS properly for production
3. **Authentication** - Implement JWT-based authentication
4. **Authorization** - Implement role-based access control
5. **Input Validation** - Validate all inputs with Zod
6. **Rate Limiting** - Implement rate limiting to prevent abuse
7. **SQL Injection Prevention** - Use parameterized queries with Prisma

### 4.3 Explainability

- **Request Logging** - Log all incoming requests with metadata
- **Response Logging** - Log all responses with status codes
- **Error Logging** - Log all errors with context
- **Request ID** - Add request ID for tracing
- **Performance Metrics** - Track response times

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

```
Total Cost = (Server Cost) + (Development Cost) + (Maintenance Cost)

Server Cost = (Instance Hours × Hourly Rate)
Development Cost = (Development Hours × Hourly Rate)
Maintenance Cost = (Support Hours × Hourly Rate)

Node.js Optimization Savings:
- Development speed: 2-3x faster than traditional languages
- Time-to-market: 30-50% reduction
- Maintenance: 20-30% reduction due to modular architecture
```

### 5.2 Key Performance Indicators

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time | < 200ms | p95 latency |
| Request Throughput | > 1000 RPS | Requests per second |
| Error Rate | < 0.1% | Total errors / Total requests |
| Test Coverage | > 80% | Code coverage percentage |
| Build Time | < 5min | Average build time |
| Startup Time | < 5s | Server startup time |

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Weeks 1-2)**
- Set up Node.js project with TypeScript
- Configure Express.js with middleware
- Implement basic CRUD operations

**Phase 2: Architecture (Weeks 3-4)**
- Implement layered architecture
- Set up dependency injection
- Add error handling

**Phase 3: Security (Weeks 5-6)**
- Implement authentication
- Add authorization
- Configure CORS and security headers

**Phase 4: Production (Weeks 7-8)**
- Deploy to production
- Set up monitoring
- Documentation and training

### 6.2 Pitfalls to Avoid

1. **Blocking the Event Loop** - Use async/await properly
2. **Memory Leaks** - Properly manage connections and timers
3. **Uncaught Exceptions** - Implement global error handlers
4. **No Validation** - Always validate all inputs
5. **No Logging** - Log all requests and errors
6. **No Testing** - Write comprehensive tests
7. **No Documentation** - Document all APIs

### 6.3 Best Practices Checklist

- [ ] Use TypeScript for type safety
- [ ] Implement layered architecture
- [ ] Use middleware for cross-cutting concerns
- [ ] Implement proper error handling
- [ ] Add request validation
- [ ] Implement authentication and authorization
- [ ] Use environment variables for configuration
- [ ] Add logging and monitoring
- [ ] Write unit tests for all layers
- [ ] Write integration tests for API endpoints
- [ ] Use async/await for async operations
- [ ] Implement proper CORS configuration
- [ ] Add rate limiting
- [ ] Use security headers (Helmet)
- [ ] Document all APIs

---

## 7. Implementation Examples

### 7.1 Project Structure

```
src/
├── config/              # Configuration files
│   ├── database.ts
│   ├── env.ts
│   └── constants.ts
├── controllers/          # Request handlers
│   ├── user.controller.ts
│   └── auth.controller.ts
├── services/             # Business logic
│   ├── user.service.ts
│   └── auth.service.ts
├── repositories/          # Data access layer
│   ├── user.repository.ts
│   └── base.repository.ts
├── middleware/           # Express middleware
│   ├── auth.middleware.ts
│   ├── error.middleware.ts
│   └── validation.middleware.ts
├── routes/               # Route definitions
│   ├── index.ts
│   ├── user.routes.ts
│   └── auth.routes.ts
├── types/                # TypeScript types
│   ├── express.d.ts
│   └── index.ts
├── utils/                # Utility functions
│   ├── logger.ts
│   └── response.util.ts
├── validators/           # Request validation schemas
│   └── user.validator.ts
├── app.ts                # Express app setup
└── server.ts             # Server entry point
```

### 7.2 Express.js Setup

```typescript
// src/app.ts
import express, { Application } from "express"
import cors from "cors"
import helmet from "helmet"
import morgan from "morgan"
import { errorHandler } from "./middleware/error.middleware"
import { logger } from "./utils/logger"
import routes from "./routes"

export function createApp(): Application {
  const app = express()

  // Security
  app.use(helmet())

  // CORS
  app.use(cors())

  // Logging
  app.use(morgan("combined", { stream: { write: (msg) => logger.info(msg.trim()) } }))

  // Body parsing
  app.use(express.json())
  app.use(express.urlencoded({ extended: true }))

  // Routes
  app.use("/api", routes)

  // Error handling (must be last)
  app.use(errorHandler)

  return app
}
```

### 7.3 Authentication Middleware

```typescript
// src/middleware/auth.middleware.ts
import { Request, Response, NextFunction } from "express"
import jwt from "jsonwebtoken"
import { UnauthorizedError } from "../errors/unauthorized.error"

interface JwtPayload {
  userId: string
  email: string
}

declare global {
  namespace Express {
    interface Request {
      user?: JwtPayload
    }
  }
}

export function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization

  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    throw new UnauthorizedError("No token provided")
  }

  const token = authHeader.substring(7)

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload
    req.user = decoded
    next()
  } catch (error) {
    throw new UnauthorizedError("Invalid token")
  }
}

// Optional auth (doesn't throw if no token)
export function optionalAuthMiddleware(req: Request, res: Response, next: NextFunction) {
  const authHeader = req.headers.authorization

  if (authHeader && authHeader.startsWith("Bearer ")) {
    const token = authHeader.substring(7)

    try {
      const decoded = jwt.verify(token, process.env.JWT_SECRET!) as JwtPayload
      req.user = decoded
    } catch (error) {
      // Continue without user
    }
  }

  next()
}
```

### 7.4 Error Handling Middleware

```typescript
// src/middleware/error.middleware.ts
import { Request, Response, NextFunction } from "express"
import { ZodError } from "zod-validation-error"
import { AppError } from "../errors/app.error"
import { logger } from "../utils/logger"

export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  logger.error(error, { path: req.path, method: req.method })

  // Handle known application errors
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      status: "error",
      message: error.message,
      ...(error.details && { details: error.details }),
    })
  }

  // Handle Zod validation errors
  if (error instanceof ZodError) {
    return res.status(400).json({
      status: "error",
      message: "Validation error",
      details: error.details,
    })
  }

  // Handle JWT errors
  if (error.name === "JsonWebTokenError") {
    return res.status(401).json({
      status: "error",
      message: "Invalid token",
    })
  }

  // Default error
  res.status(500).json({
    status: "error",
    message: process.env.NODE_ENV === "production"
      ? "Internal server error"
      : error.message,
  })
}
```

### 7.5 Request Validation Middleware

```typescript
// src/middleware/validation.middleware.ts
import { Request, Response, NextFunction } from "express"
import { AnyZodObject, ZodError } from "zod"

export function validate(schema: AnyZodObject) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body)

    if (!result.success) {
      const errors = result.error.errors.map((err) => ({
        field: err.path.join("."),
        message: err.message,
      }))

      return res.status(400).json({
        status: "error",
        message: "Validation failed",
        errors,
      })
    }

    req.body = result.data
    next()
  }
}

// Usage in routes
import { createUserSchema } from "../validators/user.validator"

router.post(
  "/users",
  validate(createUserSchema),
  userController.create
)
```

### 7.6 Controller Pattern

```typescript
// src/controllers/user.controller.ts
import { Request, Response, NextFunction } from "express"
import { UserService } from "../services/user.service"

export class UserController {
  constructor(private userService: UserService) {}

  async getAll(req: Request, res: Response, next: NextFunction) {
    try {
      const users = await this.userService.findAll()
      res.json({ status: "success", data: users })
    } catch (error) {
      next(error)
    }
  }

  async getById(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await this.userService.findById(req.params.id)
      res.json({ status: "success", data: user })
    } catch (error) {
      next(error)
    }
  }

  async create(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await this.userService.create(req.body)
      res.status(201).json({ status: "success", data: user })
    } catch (error) {
      next(error)
    }
  }

  async update(req: Request, res: Response, next: NextFunction) {
    try {
      const user = await this.userService.update(req.params.id, req.body)
      res.json({ status: "success", data: user })
    } catch (error) {
      next(error)
    }
  }

  async delete(req: Request, res: Response, next: NextFunction) {
    try {
      await this.userService.delete(req.params.id)
      res.status(204).send()
    } catch (error) {
      next(error)
    }
  }
}
```

### 7.7 Service Layer Pattern

```typescript
// src/services/user.service.ts
import { UserRepository } from "../repositories/user.repository"
import { NotFoundError } from "../errors/not-found.error"
import { ConflictError } from "../errors/conflict.error"

export class UserService {
  constructor(private userRepository: UserRepository) {}

  async findAll() {
    return this.userRepository.findAll()
  }

  async findById(id: string) {
    const user = await this.userRepository.findById(id)
    if (!user) {
      throw new NotFoundError("User not found")
    }
    return user
  }

  async create(data: CreateUserDto) {
    const existing = await this.userRepository.findByEmail(data.email)
    if (existing) {
      throw new ConflictError("Email already exists")
    }

    return this.userRepository.create(data)
  }

  async update(id: string, data: UpdateUserDto) {
    await this.findById(id) // Check if exists
    return this.userRepository.update(id, data)
  }

  async delete(id: string) {
    await this.findById(id) // Check if exists
    await this.userRepository.delete(id)
  }
}
```

### 7.8 Repository Pattern

```typescript
// src/repositories/user.repository.ts
import { PrismaClient, User } from "@prisma/client"
import { BaseRepository } from "./base.repository"

export class UserRepository extends BaseRepository<User> {
  constructor(prisma: PrismaClient) {
    super(prisma)
  }

  async findAll() {
    return this.prisma.user.findMany()
  }

  async findById(id: string) {
    return this.prisma.user.findUnique({ where: { id } })
  }

  async findByEmail(email: string) {
    return this.prisma.user.findUnique({ where: { email } })
  }

  async create(data: CreateUserDto) {
    return this.prisma.user.create({
      data: {
        ...data,
        password: await hashPassword(data.password),
      },
    })
  }

  async update(id: string, data: UpdateUserDto) {
    return this.prisma.user.update({
      where: { id },
      data,
    })
  }

  async delete(id: string) {
    await this.prisma.user.delete({ where: { id } })
  }
}
```

### 7.9 Dependency Injection

```typescript
// src/di/container.ts
import { UserRepository } from "../repositories/user.repository"
import { UserService } from "../services/user.service"
import { UserController } from "../controllers/user.controller"
import { prisma } from "../config/database"

class DIContainer {
  private static instance: DIContainer
  private repositories: Map<string, any>
  private services: Map<string, any>
  private controllers: Map<string, any>

  private constructor() {
    this.repositories = new Map()
    this.services = new Map()
    this.controllers = new Map()
    this.initialize()
  }

  static getInstance(): DIContainer {
    if (!DIContainer.instance) {
      DIContainer.instance = new DIContainer()
    }
    return DIContainer.instance
  }

  private initialize() {
    // Initialize repositories
    this.repositories.set("user", new UserRepository(prisma))

    // Initialize services
    this.services.set(
      "user",
      new UserService(this.repositories.get("user"))
    )

    // Initialize controllers
    this.controllers.set(
      "user",
      new UserController(this.services.get("user"))
    )
  }

  getController(name: string) {
    return this.controllers.get(name)
  }

  getService(name: string) {
    return this.services.get(name)
  }
}

export const container = DIContainer.getInstance()
```

### 7.10 Request Validation (Zod)

```typescript
// src/validators/user.validator.ts
import { z } from "zod"

export const createUserSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
})

export const updateUserSchema = z.object({
  name: z.string().min(2).optional(),
  email: z.string().email().optional(),
}).partial()

export type CreateUserDto = z.infer<typeof createUserSchema>
export type UpdateUserDto = z.infer<typeof updateUserSchema>
```

---

## 8. Related Skills

- [`03-backend-api/express-rest`](03-backend-api/express-rest/SKILL.md)
- [`03-backend-api/middleware`](03-backend-api/middleware/SKILL.md)
- [`03-backend-api/error-handling`](03-backend-api/error-handling/SKILL.md)
- [`03-backend-api/validation`](03-backend-api/validation/SKILL.md)
- [`10-authentication-authorization`](10-authentication-authorization/SKILL.md)
- [`04-database/database-optimization`](04-database/database-optimization/SKILL.md)
