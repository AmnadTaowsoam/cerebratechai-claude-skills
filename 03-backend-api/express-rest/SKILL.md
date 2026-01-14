# Express.js REST API Patterns

## 1. App Initialization

### Basic Express Setup
```typescript
// src/app.ts
import express, { Application, Request, Response, NextFunction } from "express"
import cors from "cors"
import helmet from "helmet"
import morgan from "morgan"
import { errorHandler } from "./middleware/error.middleware"
import { logger } from "./utils/logger"
import routes from "./routes"

export function createApp(): Application {
  const app = express()

  // Security middleware
  app.use(helmet())
  app.use(cors())

  // Logging
  app.use(morgan("combined", { stream: { write: (msg) => logger.info(msg.trim()) } }))

  // Body parsing
  app.use(express.json())
  app.use(express.urlencoded({ extended: true }))

  // Request logging
  app.use((req: Request, res: Response, next: NextFunction) => {
    logger.info(`${req.method} ${req.path}`)
    next()
  })

  // Routes
  app.use("/api", routes)

  // 404 handler
  app.use((req: Request, res: Response) => {
    res.status(404).json({ error: "Not found" })
  })

  // Error handler (must be last)
  app.use(errorHandler)

  return app
}
```

### Server Entry Point
```typescript
// src/server.ts
import { createApp } from "./app"
import { config } from "./config/env"

const app = createApp()

const server = app.listen(config.PORT, () => {
  console.log(`Server running on port ${config.PORT}`)
})

// Graceful shutdown
process.on("SIGTERM", () => {
  console.log("SIGTERM signal received: closing HTTP server")
  server.close(() => {
    console.log("HTTP server closed")
  })
})

process.on("SIGINT", () => {
  console.log("SIGINT signal received: closing HTTP server")
  server.close(() => {
    console.log("HTTP server closed")
  })
})
```

## 2. Routing Patterns

### Basic Routes
```typescript
// src/routes/user.routes.ts
import { Router, Request, Response, NextFunction } from "express"
import { UserController } from "../controllers/user.controller"

const router = Router()
const userController = new UserController()

// CRUD routes
router.get("/users", userController.getAll)
router.get("/users/:id", userController.getById)
router.post("/users", userController.create)
router.put("/users/:id", userController.update)
router.delete("/users/:id", userController.delete)

export default router
```

### Route Modules
```typescript
// src/routes/index.ts
import { Router } from "express"
import userRoutes from "./user.routes"
import authRoutes from "./auth.routes"
import postRoutes from "./post.routes"

const router = Router()

router.use("/users", userRoutes)
router.use("/auth", authRoutes)
router.use("/posts", postRoutes)

export default router
```

### Nested Routes
```typescript
// src/routes/comment.routes.ts
import { Router } from "express"
import { CommentController } from "../controllers/comment.controller"

const router = Router()
const commentController = new CommentController()

router.get("/comments", commentController.getAll)
router.post("/comments", commentController.create)
router.get("/comments/:id", commentController.getById)
router.put("/comments/:id", commentController.update)
router.delete("/comments/:id", commentController.delete)

export default router

// src/routes/post.routes.ts
import { Router } from "express"
import { PostController } from "../controllers/post.controller"
import commentRoutes from "./comment.routes"

const router = Router()
const postController = new PostController()

// Post routes
router.get("/posts", postController.getAll)
router.get("/posts/:id", postController.getById)
router.post("/posts", postController.create)
router.put("/posts/:id", postController.update)
router.delete("/posts/:id", postController.delete)

// Nested comment routes
router.use("/posts/:postId", commentRoutes)

export default router
```

### Route Parameters
```typescript
// src/routes/product.routes.ts
import { Router, Request, Response } from "express"

const router = Router()

// Single parameter
router.get("/products/:id", (req: Request, res: Response) => {
  const productId = req.params.id
  res.json({ productId })
})

// Multiple parameters
router.get("/categories/:categoryId/products/:productId", (req: Request, res: Response) => {
  const { categoryId, productId } = req.params
  res.json({ categoryId, productId })
})

// Optional parameter
router.get("/products/:id?", (req: Request, res: Response) => {
  const productId = req.params.id
  res.json({ productId })
})

// Wildcard parameter
router.get("/files/*", (req: Request, res: Response) => {
  const filePath = req.params[0]
  res.json({ filePath })
})
```

## 3. Middleware Stack

### Middleware Order
```typescript
// src/app.ts
import express, { Application } from "express"

export function createApp(): Application {
  const app = express()

  // 1. Security headers (first)
  app.use(helmet())

  // 2. CORS
  app.use(cors())

  // 3. Request logging
  app.use(morgan("combined"))

  // 4. Body parsing
  app.use(express.json())
  app.use(express.urlencoded({ extended: true }))

  // 5. Custom middleware
  app.use(requestIdMiddleware)
  app.use(loggingMiddleware)

  // 6. Authentication (before routes)
  app.use(authMiddleware)

  // 7. Routes
  app.use("/api", routes)

  // 8. Error handling (last)
  app.use(errorHandler)

  return app
}
```

### Conditional Middleware
```typescript
// src/middleware/conditional.middleware.ts
import { Request, Response, NextFunction } from "express"

export function conditionalMiddleware(condition: boolean) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (condition) {
      // Apply middleware logic
      console.log("Conditional middleware applied")
    }
    next()
  }
}

// Usage
router.get(
  "/admin/users",
  conditionalMiddleware(process.env.NODE_ENV === "production"),
  userController.getAll
)
```

### Middleware for Specific Routes
```typescript
// Apply middleware to single route
router.get("/protected", authMiddleware, userController.getProtected)

// Apply multiple middleware
router.post(
  "/upload",
  authMiddleware,
  uploadMiddleware,
  userController.upload
)

// Apply middleware to route group
router.use("/admin", adminAuthMiddleware)
router.get("/admin/users", userController.getAll)
router.get("/admin/settings", settingsController.get)
```

## 4. Error Handling Middleware

### Error Handler
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

  // Handle known errors
  if (error instanceof AppError) {
    res.status(error.statusCode).json({
      status: "error",
      message: error.message,
      ...(error.details && { details: error.details }),
    })
    return
  }

  // Handle Zod validation errors
  if (error instanceof ZodError) {
    res.status(400).json({
      status: "error",
      message: "Validation error",
      details: error.details,
    })
    return
  }

  // Handle Multer errors
  if (error.name === "MulterError") {
    res.status(400).json({
      status: "error",
      message: "File upload error",
    })
    return
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

### 404 Handler
```typescript
// src/middleware/not-found.middleware.ts
import { Request, Response } from "express"

export function notFoundHandler(req: Request, res: Response): void {
  res.status(404).json({
    status: "error",
    message: `Route ${req.method} ${req.path} not found`,
  })
}
```

### Async Error Wrapper
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
router.post("/users", asyncHandler(userController.create))
```

## 5. Request Validation

### Express Validator
```typescript
// src/middleware/validation.middleware.ts
import { Request, Response, NextFunction } from "express"
import { body, param, query, validationResult } from "express-validator"

export const validateUser = [
  body("name")
    .trim()
    .notEmpty()
    .withMessage("Name is required")
    .isLength({ min: 2, max: 50 })
    .withMessage("Name must be between 2 and 50 characters"),
  body("email")
    .trim()
    .isEmail()
    .withMessage("Invalid email address")
    .normalizeEmail(),
  body("password")
    .isLength({ min: 8 })
    .withMessage("Password must be at least 8 characters")
    .matches(/[A-Z]/)
    .withMessage("Password must contain uppercase letter")
    .matches(/[a-z]/)
    .withMessage("Password must contain lowercase letter")
    .matches(/[0-9]/)
    .withMessage("Password must contain number"),
]

export const validateUserId = [
  param("id")
    .isMongoId()
    .withMessage("Invalid user ID"),
]

export const validatePagination = [
  query("page")
    .optional()
    .isInt({ min: 1 })
    .withMessage("Page must be a positive integer")
    .toInt(),
  query("limit")
    .optional()
    .isInt({ min: 1, max: 100 })
    .withMessage("Limit must be between 1 and 100")
    .toInt(),
]

export function handleValidationErrors(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  const errors = validationResult(req)
  if (!errors.isEmpty()) {
    res.status(400).json({
      status: "error",
      message: "Validation failed",
      errors: errors.array().map((err) => ({
        field: err.path.join("."),
        message: err.msg,
      })),
    })
    return
  }
  next()
}

// Usage
router.post(
  "/users",
  validateUser,
  handleValidationErrors,
  asyncHandler(userController.create)
)

router.get(
  "/users/:id",
  validateUserId,
  handleValidationErrors,
  asyncHandler(userController.getById)
)
```

### Zod Validation
```typescript
// src/middleware/zod-validation.middleware.ts
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

      res.status(400).json({
        status: "error",
        message: "Validation failed",
        errors,
      })
      return
    }

    req.body = result.data
    next()
  }
}

// Usage
import { createUserSchema } from "../validators/user.validator"

router.post(
  "/users",
  validate(createUserSchema),
  asyncHandler(userController.create)
)
```

## 6. Authentication Middleware

### JWT Authentication
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

export function authMiddleware(req: Request, res: Response, next: NextFunction): void {
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
export function optionalAuth(req: Request, res: Response, next: NextFunction): void {
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

### Role-based Authorization
```typescript
// src/middleware/role.middleware.ts
import { Request, Response, NextFunction } from "express"
import { ForbiddenError } from "../errors/forbidden.error"

type Role = "user" | "admin" | "moderator"

export function requireRole(...roles: Role[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      throw new ForbiddenError("Authentication required")
    }

    const userRole = req.user.role || "user"

    if (!roles.includes(userRole)) {
      throw new ForbiddenError("Insufficient permissions")
    }

    next()
  }
}

// Usage
router.get(
  "/admin/users",
  authMiddleware,
  requireRole("admin"),
  asyncHandler(userController.getAll)
)

router.get(
  "/moderator/posts",
  authMiddleware,
  requireRole("admin", "moderator"),
  asyncHandler(postController.getAll)
)
```

## 7. CORS Configuration

### Basic CORS
```typescript
import cors from "cors"

app.use(cors())
```

### Custom CORS
```typescript
import cors from "cors"

const corsOptions = {
  origin: (origin: string | undefined, callback: (err: Error | null, allow: boolean) => void) => {
    const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(",") || "*"

    if (!origin) {
      return callback(null, true)
    }

    if (allowedOrigins === "*") {
      return callback(null, true)
    }

    if (allowedOrigins.indexOf(origin) !== -1) {
      callback(null, true)
    } else {
      callback(new Error("Not allowed by CORS"))
    }
  },
  credentials: true,
  methods: ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
  allowedHeaders: ["Content-Type", "Authorization"],
  maxAge: 86400, // 24 hours
}

app.use(cors(corsOptions))
```

### Per-route CORS
```typescript
import cors from "cors"

const publicCors = cors({ origin: "*" })
const restrictedCors = cors({
  origin: "https://example.com",
  credentials: true,
})

app.get("/public/data", publicCors, (req, res) => {
  res.json({ data: "public" })
})

app.get("/private/data", restrictedCors, (req, res) => {
  res.json({ data: "private" })
})
```

## 8. Rate Limiting

### Basic Rate Limiting
```typescript
import rateLimit from "express-rate-limit"

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: "Too many requests from this IP, please try again later.",
  standardHeaders: true,
  legacyHeaders: false,
})

app.use("/api", limiter)
```

### Multiple Rate Limiters
```typescript
import rateLimit from "express-rate-limit"

// General API rate limiter
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 100,
  message: "Too many requests from this IP",
})

// Stricter rate limiter for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: "Too many login attempts, please try again later",
})

// Apply different limiters
app.use("/api", apiLimiter)
app.use("/api/auth", authLimiter)
```

### Rate Limiting with Redis
```typescript
import RedisStore from "rate-limit-redis"
import rateLimit from "express-rate-limit"

const redisClient = createClient({
  url: process.env.REDIS_URL,
})

const redisStore = new RedisStore({
  client: redisClient,
  prefix: "rate-limit:",
})

const limiter = rateLimit({
  store: redisStore,
  windowMs: 15 * 60 * 1000,
  max: 100,
})

app.use(limiter)
```

## 9. Security Headers

### Helmet Configuration
```typescript
import helmet from "helmet"

app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'"],
      fontSrc: ["'self'"],
      objectSrc: ["'none'"],
      mediaSrc: ["'self'"],
      frameSrc: ["'none'"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
  noSniff: true,
  xssFilter: true,
  referrerPolicy: { policy: "no-referrer" },
}))
```

### Custom Security Headers
```typescript
app.use((req, res, next) => {
  // X-Content-Type-Options
  res.setHeader("X-Content-Type-Options", "nosniff")

  // X-Frame-Options
  res.setHeader("X-Frame-Options", "DENY")

  // X-XSS-Protection
  res.setHeader("X-XSS-Protection", "1; mode=block")

  // Strict-Transport-Security
  if (process.env.NODE_ENV === "production") {
    res.setHeader(
      "Strict-Transport-Security",
      "max-age=31536000; includeSubDomains"
    )
  }

  // Content-Security-Policy
  res.setHeader(
    "Content-Security-Policy",
    "default-src 'self'; script-src 'self'; object-src 'none';"
  )

  next()
})
```

## 10. Logging

### Morgan Configuration
```typescript
import morgan from "morgan"
import { createStream } from "rotating-file-stream"
import path from "path"

const accessLogStream = createStream(path.join(__dirname, "../logs/access.log"), {
  size: "10M",
  interval: "1d",
})

// Development format
if (process.env.NODE_ENV === "development") {
  app.use(morgan("dev"))
}

// Production format
if (process.env.NODE_ENV === "production") {
  app.use(
    morgan("combined", {
      stream: accessLogStream,
      skip: (req) => req.path === "/health",
    })
  )
}
```

### Custom Logger
```typescript
// src/utils/logger.ts
import winston from "winston"

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || "info",
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({
      format: winston.format.simple(),
    }),
    new winston.transports.File({
      filename: "logs/error.log",
      level: "error",
    }),
    new winston.transports.File({
      filename: "logs/combined.log",
    }),
  ],
})

export default logger
```

### Request Logging Middleware
```typescript
// src/middleware/logging.middleware.ts
import { Request, Response, NextFunction } from "express"
import { v4 as uuidv4 } from "uuid"
import logger from "../utils/logger"

interface RequestWithId extends Request {
  id: string
}

export function loggingMiddleware(
  req: RequestWithId,
  res: Response,
  next: NextFunction
): void {
  req.id = uuidv4()

  const start = Date.now()

  res.on("finish", () => {
    const duration = Date.now() - start

    logger.info({
      requestId: req.id,
      method: req.method,
      url: req.url,
      status: res.statusCode,
      duration: `${duration}ms`,
      ip: req.ip,
      userAgent: req.get("user-agent"),
    })
  })

  next()
}
```

## 11. Testing

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

### Integration Tests
```typescript
// tests/integration/api.test.ts
import request from "supertest"
import { createApp } from "../../src/app"

describe("API Integration Tests", () => {
  const app = createApp()

  describe("Authentication Flow", () => {
    it("should register, login, and access protected route", async () => {
      // Register
      const registerResponse = await request(app)
        .post("/api/auth/register")
        .send({
          name: "Test User",
          email: "test@example.com",
          password: "password123",
        })

      expect(registerResponse.status).toBe(201)

      // Login
      const loginResponse = await request(app)
        .post("/api/auth/login")
        .send({
          email: "test@example.com",
          password: "password123",
        })

      expect(loginResponse.status).toBe(200)
      const { token } = loginResponse.body.data

      // Access protected route
      const protectedResponse = await request(app)
        .get("/api/users/me")
        .set("Authorization", `Bearer ${token}`)

      expect(protectedResponse.status).toBe(200)
    })
  })
})
```

## 12. Production Setup

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
  LOG_LEVEL: z.string().default("info"),
})

export const config = envSchema.parse(process.env)
```

### Cluster Mode
```typescript
// src/cluster.ts
import cluster from "cluster"
import os from "os"
import { createServer } from "./server"

const numCPUs = os.cpus().length

if (cluster.isPrimary) {
  console.log(`Primary ${process.pid} is running`)

  // Fork workers
  for (let i = 0; i < numCPUs; i++) {
    cluster.fork()
  }

  cluster.on("exit", (worker, code, signal) => {
    console.log(`Worker ${worker.process.pid} died`)
    cluster.fork()
  })
} else {
  // Worker process
  createServer()
}
```

### Graceful Shutdown
```typescript
// src/server.ts
import http from "http"
import { createApp } from "./app"
import { config } from "./config/env"

const app = createApp()
const server = http.createServer(app)

server.listen(config.PORT, () => {
  console.log(`Server running on port ${config.PORT}`)
})

const shutdown = (signal: string) => {
  console.log(`${signal} received: closing HTTP server`)
  server.close(() => {
    console.log("HTTP server closed")
    process.exit(0)
  })
}

process.on("SIGTERM", () => shutdown("SIGTERM"))
process.on("SIGINT", () => shutdown("SIGINT"))

process.on("uncaughtException", (error) => {
  console.error("Uncaught Exception:", error)
  shutdown("uncaughtException")
})

process.on("unhandledRejection", (reason, promise) => {
  console.error("Unhandled Rejection at:", promise, "reason:", reason)
  shutdown("unhandledRejection")
})
```

### Health Check Endpoint
```typescript
// src/routes/health.routes.ts
import { Router, Request, Response } from "express"
import { prisma } from "../config/database"

const router = Router()

router.get("/health", async (req: Request, res: Response) => {
  try {
    // Check database connection
    await prisma.$queryRaw`SELECT 1`

    res.status(200).json({
      status: "ok",
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      environment: process.env.NODE_ENV,
    })
  } catch (error) {
    res.status(503).json({
      status: "error",
      message: "Service unavailable",
      timestamp: new Date().toISOString(),
    })
  }
})

export default router
```
