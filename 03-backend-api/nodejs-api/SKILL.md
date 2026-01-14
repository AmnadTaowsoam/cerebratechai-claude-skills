# Node.js REST API Patterns

## 1. Project Structure

### Recommended Structure
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

### Example File Structure
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

## 2. Express.js Setup

### Basic Setup
```typescript
// src/server.ts
import { createApp } from "./app"
import { config } from "./config/env"

const app = createApp()

app.listen(config.PORT, () => {
  console.log(`Server running on port ${config.PORT}`)
})
```

### Environment Configuration
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

## 3. Middleware Patterns

### Authentication Middleware
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
export function optionalAuth(req: Request, res: Response, next: NextFunction) {
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

### Error Handling Middleware
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
) {
  logger.error(error, { path: req.path, method: req.method })

  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      status: "error",
      message: error.message,
      ...(error.details && { details: error.details }),
    })
  }

  if (error instanceof ZodError) {
    return res.status(400).json({
      status: "error",
      message: "Validation error",
      details: error.details,
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

### Request Validation Middleware
```typescript
// src/middleware/validation.middleware.ts
import { Request, Response, NextFunction } from "express"
import { AnyZodObject } from "zod"
import { ZodError } from "zod-validation-error"

export function validate(schema: AnyZodObject) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body)

    if (!result.success) {
      throw new ZodError("Validation failed", result.error.issues)
    }

    req.body = result.data
    next()
  }
}

// Usage in routes
router.post(
  "/users",
  validate(createUserSchema),
  userController.create
)
```

### Logging Middleware
```typescript
// src/middleware/logging.middleware.ts
import { Request, Response, NextFunction } from "express"
import { logger } from "../utils/logger"

export function loggingMiddleware(req: Request, res: Response, next: NextFunction) {
  const start = Date.now()

  res.on("finish", () => {
    const duration = Date.now() - start
    logger.info({
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: `${duration}ms`,
      ip: req.ip,
    })
  })

  next()
}
```

## 4. Controller Patterns

### Basic Controller
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

### Async Handler Wrapper
```typescript
// src/utils/async-handler.util.ts
import { Request, Response, NextFunction } from "express"

export function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>
) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next)
  }
}

// Usage
router.get("/users", asyncHandler(userController.getAll))
```

## 5. Service Layer Patterns

### Basic Service
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

### Service with Transactions
```typescript
// src/services/order.service.ts
import { OrderRepository } from "../repositories/order.repository"
import { ProductRepository } from "../repositories/product.repository"
import { Database } from "../config/database"

export class OrderService {
  constructor(
    private orderRepository: OrderRepository,
    private productRepository: ProductRepository,
    private db: Database
  ) {}

  async createOrder(data: CreateOrderDto) {
    return this.db.transaction(async (tx) => {
      // Check product availability
      const product = await this.productRepository.findById(tx, data.productId)
      if (!product || product.stock < data.quantity) {
        throw new Error("Product not available")
      }

      // Create order
      const order = await this.orderRepository.create(tx, {
        ...data,
        total: product.price * data.quantity,
      })

      // Update product stock
      await this.productRepository.updateStock(tx, data.productId, -data.quantity)

      return order
    })
  }
}
```

## 6. Repository Pattern

### Base Repository
```typescript
// src/repositories/base.repository.ts
import { PrismaClient } from "@prisma/client"

export abstract class BaseRepository<T> {
  constructor(protected prisma: PrismaClient) {}

  async findAll(): Promise<T[]> {
    throw new Error("Method not implemented")
  }

  async findById(id: string): Promise<T | null> {
    throw new Error("Method not implemented")
  }

  async create(data: any): Promise<T> {
    throw new Error("Method not implemented")
  }

  async update(id: string, data: any): Promise<T> {
    throw new Error("Method not implemented")
  }

  async delete(id: string): Promise<void> {
    throw new Error("Method not implemented")
  }
}
```

### User Repository
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

## 7. Dependency Injection

### Simple DI Container
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

### Using DI
```typescript
// src/routes/user.routes.ts
import { Router } from "express"
import { container } from "../di/container"
import { authMiddleware } from "../middleware/auth.middleware"

const router = Router()
const userController = container.getController("user")

router.get("/users", authMiddleware, userController.getAll.bind(userController))
router.get("/users/:id", authMiddleware, userController.getById.bind(userController))
router.post("/users", userController.create.bind(userController))
router.put("/users/:id", authMiddleware, userController.update.bind(userController))
router.delete("/users/:id", authMiddleware, userController.delete.bind(userController))

export default router
```

## 8. Error Handling

### Custom Error Classes
```typescript
// src/errors/app.error.ts
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public details?: any
  ) {
    super(message)
    this.name = this.constructor.name
    Error.captureStackTrace(this, this.constructor)
  }
}

// src/errors/bad-request.error.ts
export class BadRequestError extends AppError {
  constructor(message: string = "Bad request", details?: any) {
    super(400, message, details)
  }
}

// src/errors/unauthorized.error.ts
export class UnauthorizedError extends AppError {
  constructor(message: string = "Unauthorized") {
    super(401, message)
  }
}

// src/errors/forbidden.error.ts
export class ForbiddenError extends AppError {
  constructor(message: string = "Forbidden") {
    super(403, message)
  }
}

// src/errors/not-found.error.ts
export class NotFoundError extends AppError {
  constructor(message: string = "Not found") {
    super(404, message)
  }
}

// src/errors/conflict.error.ts
export class ConflictError extends AppError {
  constructor(message: string = "Conflict") {
    super(409, message)
  }
}
```

### Using Custom Errors
```typescript
// src/services/user.service.ts
import { NotFoundError, ConflictError } from "../errors"

export class UserService {
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
}
```

## 9. Request Validation (Zod)

### Validation Schemas
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

### Validation Middleware
```typescript
// src/middleware/validation.middleware.ts
import { Request, Response, NextFunction } from "express"
import { AnyZodObject, ZodError } from "zod"

export function validate(schema: AnyZodObject) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body)

    if (!result.success) {
      const errors = result.error.errors.map((e) => ({
        field: e.path.join("."),
        message: e.message,
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
```

## 10. Response Formatting

### Response Utility
```typescript
// src/utils/response.util.ts
import { Response } from "express"

export interface SuccessResponse<T> {
  status: "success"
  data: T
}

export interface PaginatedResponse<T> {
  status: "success"
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

export function success<T>(res: Response, data: T, statusCode: number = 200) {
  return res.status(statusCode).json<SuccessResponse<T>>({
    status: "success",
    data,
  })
}

export function paginated<T>(
  res: Response,
  data: T[],
  page: number,
  limit: number,
  total: number
) {
  return res.json<PaginatedResponse<T>>({
    status: "success",
    data,
    pagination: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  })
}

export function created<T>(res: Response, data: T) {
  return success(res, data, 201)
}

export function noContent(res: Response) {
  return res.status(204).send()
}
```

### Using Response Utility
```typescript
// src/controllers/user.controller.ts
import { success, paginated, created, noContent } from "../utils/response.util"

export class UserController {
  async getAll(req: Request, res: Response) {
    const { page = 1, limit = 10 } = req.query
    const { users, total } = await this.userService.findAllPaginated(
      Number(page),
      Number(limit)
    )
    return paginated(res, users, Number(page), Number(limit), total)
  }

  async getById(req: Request, res: Response) {
    const user = await this.userService.findById(req.params.id)
    return success(res, user)
  }

  async create(req: Request, res: Response) {
    const user = await this.userService.create(req.body)
    return created(res, user)
  }

  async delete(req: Request, res: Response) {
    await this.userService.delete(req.params.id)
    return noContent(res)
  }
}
```

## 11. Testing Patterns

### Controller Tests
```typescript
// tests/controllers/user.controller.test.ts
import request from "supertest"
import { createApp } from "../../src/app"
import { prisma } from "../../src/config/database"

describe("UserController", () => {
  let app: Express

  beforeAll(async () => {
    app = createApp()
    await prisma.$connect()
  })

  afterAll(async () => {
    await prisma.$disconnect()
  })

  beforeEach(async () => {
    await prisma.user.deleteMany()
  })

  describe("GET /api/users", () => {
    it("should return all users", async () => {
      await prisma.user.createMany({
        data: [
          { name: "John", email: "john@example.com", password: "hashed" },
          { name: "Jane", email: "jane@example.com", password: "hashed" },
        ],
      })

      const response = await request(app).get("/api/users")

      expect(response.status).toBe(200)
      expect(response.body.status).toBe("success")
      expect(response.body.data).toHaveLength(2)
    })

    it("should return paginated users", async () => {
      await prisma.user.createMany({
        data: Array.from({ length: 25 }, (_, i) => ({
          name: `User ${i}`,
          email: `user${i}@example.com`,
          password: "hashed",
        })),
      })

      const response = await request(app).get("/api/users?page=1&limit=10")

      expect(response.status).toBe(200)
      expect(response.body.data).toHaveLength(10)
      expect(response.body.pagination.total).toBe(25)
      expect(response.body.pagination.totalPages).toBe(3)
    })
  })

  describe("POST /api/users", () => {
    it("should create a new user", async () => {
      const userData = {
        name: "John Doe",
        email: "john@example.com",
        password: "password123",
      }

      const response = await request(app)
        .post("/api/users")
        .send(userData)

      expect(response.status).toBe(201)
      expect(response.body.data.name).toBe(userData.name)
      expect(response.body.data.email).toBe(userData.email)
      expect(response.body.data).not.toHaveProperty("password")
    })

    it("should return validation error for invalid data", async () => {
      const response = await request(app)
        .post("/api/users")
        .send({ name: "J" }) // Too short

      expect(response.status).toBe(400)
      expect(response.body.status).toBe("error")
      expect(response.body.errors).toBeDefined()
    })
  })
})
```

### Service Tests
```typescript
// tests/services/user.service.test.ts
import { UserService } from "../../src/services/user.service"
import { UserRepository } from "../../src/repositories/user.repository"
import { NotFoundError, ConflictError } from "../../src/errors"

describe("UserService", () => {
  let userService: UserService
  let mockUserRepository: jest.Mocked<UserRepository>

  beforeEach(() => {
    mockUserRepository = {
      findById: jest.fn(),
      findByEmail: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
      findAll: jest.fn(),
    } as any

    userService = new UserService(mockUserRepository)
  })

  describe("findById", () => {
    it("should return user when found", async () => {
      const user = { id: "1", name: "John", email: "john@example.com" }
      mockUserRepository.findById.mockResolvedValue(user)

      const result = await userService.findById("1")

      expect(result).toEqual(user)
      expect(mockUserRepository.findById).toHaveBeenCalledWith("1")
    })

    it("should throw NotFoundError when user not found", async () => {
      mockUserRepository.findById.mockResolvedValue(null)

      await expect(userService.findById("1")).rejects.toThrow(NotFoundError)
    })
  })

  describe("create", () => {
    it("should create user when email is unique", async () => {
      const userData = { name: "John", email: "john@example.com", password: "pass" }
      mockUserRepository.findByEmail.mockResolvedValue(null)
      mockUserRepository.create.mockResolvedValue({ id: "1", ...userData })

      const result = await userService.create(userData)

      expect(result).toHaveProperty("id")
      expect(mockUserRepository.create).toHaveBeenCalled()
    })

    it("should throw ConflictError when email exists", async () => {
      const userData = { name: "John", email: "john@example.com", password: "pass" }
      mockUserRepository.findByEmail.mockResolvedValue({ id: "1", ...userData })

      await expect(userService.create(userData)).rejects.toThrow(ConflictError)
    })
  })
})
```

## 12. Security Best Practices

### Helmet for Security Headers
```typescript
import helmet from "helmet"

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
}))
```

### Rate Limiting
```typescript
import rateLimit from "express-rate-limit"

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: "Too many requests from this IP, please try again later.",
})

app.use("/api", limiter)

// Stricter rate limiting for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: "Too many login attempts, please try again later.",
})

app.use("/api/auth/login", authLimiter)
```

### Input Sanitization
```typescript
import { body, param, query, validationResult } from "express-validator"

app.post(
  "/users",
  [
    body("name").trim().escape(),
    body("email").trim().normalizeEmail(),
    body("password").isLength({ min: 8 }),
  ],
  (req, res) => {
    const errors = validationResult(req)
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() })
    }
    // Process request
  }
)
```

### CORS Configuration
```typescript
import cors from "cors"

app.use(cors({
  origin: process.env.ALLOWED_ORIGINS?.split(",") || "*",
  methods: ["GET", "POST", "PUT", "DELETE", "PATCH"],
  allowedHeaders: ["Content-Type", "Authorization"],
  credentials: true,
}))
```

### SQL Injection Prevention
```typescript
// Always use parameterized queries with Prisma
// Bad: Direct string concatenation
const user = await prisma.$queryRaw`SELECT * FROM User WHERE id = '${userId}'`

// Good: Parameterized query
const user = await prisma.$queryRaw`SELECT * FROM User WHERE id = ${userId}`

// Better: Use Prisma's built-in methods
const user = await prisma.user.findUnique({ where: { id: userId } })
```

### XSS Prevention
```typescript
import xss from "xss"

// Sanitize user input
const sanitized = xss(req.body.content)

// Use DOMPurify for HTML content
import DOMPurify from "dompurify"

const clean = DOMPurify.sanitize(dirtyHtml)
```
