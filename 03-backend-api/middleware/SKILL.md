# Backend Middleware Patterns

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

Middleware functions คือ functions ที่มี access ถึง request object (req), response object (res), และ next middleware function ใน application's request-response cycle โดย middleware ช่วยจัดการ cross-cutting concerns อย่าง authentication, logging, error handling และ validation

Middleware ประกอบด้วย:
- **Request Processing** - Process incoming requests before route handlers
- **Response Processing** - Modify responses before sending to clients
- **Error Handling** - Centralized error handling across all routes
- **Cross-Cutting Concerns** - Authentication, logging, validation, compression
- **Modular Design** - Composable middleware chain for flexible configuration

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **เพิ่ม Maintainability** - Centralized logic ช่วยลด code duplication
2. **เพิ่ม Security** - Consistent security policies across all endpoints
3. **เพิ่ม Observability** - Centralized logging และ monitoring
4. **ลด Development Time** - Reusable middleware ช่วยลด boilerplate
5. **ปรับปรุง Consistency** - Consistent error handling และ validation

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Composable** - Middleware ต้อง composable และ chainable
2. **Reusable** - Middleware ต้อง reusable across routes
3. **Testable** - Middleware ต้อง testable ใน isolation
4. **Configurable** - Middleware ต้อง configurable ด้วย options
5. **Type-Safe** - Middleware ต้อง type-safe ด้วย TypeScript

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

Middleware ประกอบด้วย:

1. **Request Processing** - Access and modify request object
2. **Response Processing** - Access and modify response object
3. **Next Function** - Pass control to next middleware or route handler
4. **Error Handling** - Catch and handle errors in middleware chain
5. **Async Support** - Support async middleware functions
6. **Termination** - Terminate request-response cycle early if needed

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              Middleware Architecture                 │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Client Request                     │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │         Middleware Chain (Execution Order)     │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │  │
│  │  │Security  │  │   CORS   │  │  Logging │  │  │
│  │  │Headers   │  │          │  │          │  │  │
│  │  └─────────┘  └─────────┘  └─────────┘  │  │
│  │       │              │              │          │  │
│  │       ▼              ▼              ▼          │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │  │
│  │  │ Body     │  │ Request  │  │ Rate     │  │  │
│  │  │ Parser   │  │   ID     │  │ Limit    │  │  │
│  │  └─────────┘  └─────────┘  └─────────┘  │  │
│  │       │              │              │          │  │
│  │       ▼              ▼              ▼          │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │  │
│  │  │ Auth     │  │ Validate │  │  Error    │  │  │
│  │  │          │  │          │  │ Handler  │  │  │
│  │  └─────────┘  └─────────┘  └─────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Route Handler                    │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │  │
│  │  │  GET     │  │  POST    │  │  PUT     │  │  │
│  │  │ /users   │  │ /users   │  │ /users   │  │  │
│  │  └─────────┘  └─────────┘  └─────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Response Processing               │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  │  │
│  │  │ Format   │  │ Compress │  │  Cache    │  │  │
│  │  │          │  │          │  │ Control  │  │  │
│  │  └─────────┘  └─────────┘  └─────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Client Response                    │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

1. **Middleware Definition** - Define middleware function with req, res, next
2. **Logic Implementation** - Implement middleware logic (auth, logging, etc.)
3. **Error Handling** - Handle errors appropriately
4. **Next Function Call** - Call next() or send response
5. **Middleware Registration** - Register middleware with app or router
6. **Order Configuration** - Configure correct execution order
7. **Testing** - Write unit tests for middleware

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Enterprise Features |
|------|---------|---------------------|
| Express Middleware | Express.js middleware ecosystem | Built-in middleware, community packages |
| FastAPI Middleware | FastAPI middleware support | Starlette-based, async support |
| Helmet | Security headers | Comprehensive security defaults |
| CORS | Cross-Origin Resource Sharing | Configurable CORS policies |
| Morgan | HTTP request logger | Custom formats, stream support |
| Multer | Multipart form data | File upload handling |

### 3.2 Configuration Essentials

```typescript
// middleware.config.ts
import express, { Application } from "express"
import helmet from "helmet"
import cors from "cors"
import morgan from "morgan"
import { securityMiddleware } from "./middleware/security.middleware"
import { loggingMiddleware } from "./middleware/logging.middleware"
import { authMiddleware } from "./middleware/auth.middleware"
import { errorHandler } from "./middleware/error.middleware"

export function createApp(): Application {
  const app = express()

  // Security headers (first)
  app.use(helmet())

  // CORS
  app.use(cors())

  // Logging
  app.use(morgan("combined"))
  app.use(loggingMiddleware)

  // Body parsing
  app.use(express.json())
  app.use(express.urlencoded({ extended: true }))

  // Request ID
  app.use(requestIdMiddleware)

  // Rate limiting (before auth)
  app.use(rateLimiter)

  // Authentication (before routes)
  app.use(authMiddleware)

  // Routes
  app.use("/api", routes)

  // 404 handler
  app.use(notFoundHandler)

  // Error handler (must be last)
  app.use(errorHandler)

  return app
}
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **OWASP Security** - Follow OWASP security guidelines
- **HTTP Security Headers** - Implement security headers per RFC
- **CORS Specification** - Follow CORS specification
- **Rate Limiting** - Implement rate limiting per API best practices
- **GDPR Compliance** - Handle personal data in middleware

### 4.2 Security Protocol

1. **Security Headers** - Implement security headers (Helmet)
2. **CORS Configuration** - Configure CORS properly for production
3. **Authentication** - Implement JWT-based authentication
4. **Authorization** - Implement role-based access control
5. **Input Validation** - Validate all inputs
6. **Rate Limiting** - Implement rate limiting to prevent abuse
7. **Error Handling** - Don't expose internal errors

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
Total Cost = (Server Cost) + (Middleware Overhead Cost)

Server Cost = (Instance Hours × Hourly Rate)
Middleware Overhead Cost = (Processing Time × CPU Cost)

Middleware Optimization Savings:
- Centralized logic: 20-30% code reduction
- Reusable middleware: 40-50% development time reduction
- Consistent error handling: 15-20% support cost reduction
```

### 5.2 Key Performance Indicators

| Metric | Target | Measurement |
|--------|--------|-------------|
| Middleware Latency | < 5ms | Average middleware processing time |
| Request ID Coverage | 100% | Requests with request IDs |
| Error Logging Coverage | 100% | Errors logged with context |
| Rate Limit Effectiveness | > 95% | Blocked requests / Total abuse attempts |
| Validation Accuracy | 100% | Valid requests / Total requests |
| Cache Hit Rate | > 80% | Cache hits / Total requests |

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Weeks 1-2)**
- Set up basic middleware (logging, error handling)
- Implement request ID generation
- Add security headers

**Phase 2: Security (Weeks 3-4)**
- Implement authentication middleware
- Add authorization middleware
- Configure CORS properly

**Phase 3: Performance (Weeks 5-6)**
- Implement rate limiting
- Add compression middleware
- Implement caching middleware

**Phase 4: Production (Weeks 7-8)**
- Deploy with monitoring
- Set up alerts for middleware failures
- Documentation and training

### 6.2 Pitfalls to Avoid

1. **Wrong Order** - Middleware order is critical (security first, error handler last)
2. **Skipping next()** - Always call next() or send response
3. **Blocking Async** - Don't block async operations
4. **No Error Handling** - Handle errors in middleware properly
5. **Exposing Errors** - Don't expose internal errors to clients
6. **Ignoring Performance** - Monitor middleware performance impact
7. **No Testing** - Write unit tests for all middleware

### 6.3 Best Practices Checklist

- [ ] Configure middleware in correct order
- [ ] Use security headers (Helmet)
- [ ] Implement proper CORS configuration
- [ ] Add request ID for tracing
- [ ] Implement authentication middleware
- [ ] Implement authorization middleware
- [ ] Add rate limiting
- [ ] Implement input validation
- [ ] Add error handling middleware (last)
- [ ] Log all requests and responses
- [ ] Monitor middleware performance
- [ ] Test middleware in isolation
- [ ] Use TypeScript for type safety
- [ ] Document middleware options
- [ ] Implement graceful shutdown

---

## 7. Implementation Examples

### 7.1 Request Logging Middleware

```typescript
// middleware/logging.middleware.ts
import { Request, Response, NextFunction } from "express"
import { v4 as uuidv4 } from "uuid"

interface RequestWithId extends Request {
  id: string
}

export function loggingMiddleware(
  req: RequestWithId,
  res: Response,
  next: NextFunction
): void {
  req.id = uuidv4()

  const { method, url, ip } = req
  const userAgent = req.get("user-agent")

  console.log({
    requestId: req.id,
    method,
    url,
    ip,
    userAgent,
    timestamp: new Date().toISOString(),
  })

  next()
}

// Enhanced logging with response time
export function detailedLoggingMiddleware(
  req: RequestWithId,
  res: Response,
  next: NextFunction
): void {
  const startTime = Date.now()

  req.id = uuidv4()

  // Log incoming request
  console.log(`[${req.id}] ${req.method} ${req.url}`)

  // Capture response
  const originalSend = res.send
  res.send = function (data) {
    const duration = Date.now() - startTime
    console.log(`[${req.id}] Response in ${duration}ms`)
    originalSend.call(this, data)
  }

  next()
}
```

### 7.2 Authentication Middleware

```typescript
// middleware/auth.middleware.ts
import { Request, Response, NextFunction } from "express"
import jwt from "jsonwebtoken"
import { UnauthorizedError } from "../errors/unauthorized.error"

interface JwtPayload {
  userId: string
  email: string
  role: string
}

declare global {
  namespace Express {
    interface Request {
      user?: JwtPayload
    }
  }
}

export function authMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
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

// Optional authentication (doesn't throw if no token)
export function optionalAuthMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
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

### 7.3 Authorization Middleware

```typescript
// middleware/authorization.middleware.ts
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
      throw new ForbiddenError(`Requires one of: ${roles.join(", ")}`)
    }

    next()
  }
}

// Usage
router.get("/admin/users", authMiddleware, requireRole("admin"), userController.getAll)
```

### 7.4 Error Handling Middleware

```typescript
// middleware/error.middleware.ts
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
  logger.error(error, {
    path: req.path,
    method: req.method,
    userId: (req as any).user?.id,
  })

  // Handle known application errors
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      success: false,
      message: error.message,
      ...(error.details && { details: error.details }),
    })
  }

  // Handle Zod validation errors
  if (error instanceof ZodError) {
    return res.status(400).json({
      success: false,
      message: "Validation error",
      details: error.details,
    })
  }

  // Handle JWT errors
  if (error.name === "JsonWebTokenError") {
    return res.status(401).json({
      success: false,
      message: "Invalid token",
    })
  }

  // Default error
  res.status(500).json({
    success: false,
    message: process.env.NODE_ENV === "production"
      ? "Internal server error"
      : error.message,
  })
}
```

### 7.5 Rate Limiting Middleware

```typescript
// middleware/rate-limit.middleware.ts
import { Request, Response, NextFunction } from "express"
import rateLimit from "express-rate-limit"

// General API rate limiter
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: "Too many requests from this IP, please try again later.",
  standardHeaders: true,
  legacyHeaders: false,
})

// Stricter rate limiter for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5,
  message: "Too many login attempts, please try again later.",
})

// Rate limiter for API key based
const apiKeyLimiter = rateLimit({
  keyGenerator: (req) => {
    return req.headers["x-api-key"] || req.ip
  },
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 1000,
})
```

### 7.6 CORS Middleware

```typescript
// middleware/cors.middleware.ts
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

export default cors(corsOptions)
```

### 7.7 Security Headers Middleware

```typescript
// middleware/security.middleware.ts
import { Request, Response, NextFunction } from "express"
import helmet from "helmet"

export function securityMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  // Add custom security headers
  res.setHeader("X-Content-Type-Options", "nosniff")
  res.setHeader("X-Frame-Options", "DENY")
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
}

// Using helmet
export function helmetMiddleware() {
  return helmet({
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
  })
}
```

### 7.8 Request Validation Middleware

```typescript
// middleware/validation.middleware.ts
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
        success: false,
        message: "Validation failed",
        errors,
      })
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
  userController.create
)
```

### 7.9 Middleware Composition

```typescript
// middleware/compose.middleware.ts
import { Request, Response, NextFunction } from "express"

export function compose(...middlewares: Array<(req: Request, res: Response, next: NextFunction) => void>) {
  return (req: Request, res: Response, next: NextFunction) => {
    const dispatch = (i: number) => {
      if (i <= middlewares.length) {
        return middlewares[i - 1](req, res, (err?: Error) => {
          if (err) {
            return next(err)
          }
          return dispatch(i + 1)
        })
      }
      return next()
    }
    return dispatch(1)
  }
}

// Usage
const authChain = compose(
  loggingMiddleware,
  requestIdMiddleware,
  authMiddleware
)

router.use(authChain)
```

### 7.10 Middleware Order Configuration

```typescript
// app.ts
import express, { Application } from "express"
import helmet from "helmet"
import cors from "cors"
import morgan from "morgan"
import { securityMiddleware } from "./middleware/security.middleware"
import { loggingMiddleware } from "./middleware/logging.middleware"
import { authMiddleware } from "./middleware/auth.middleware"
import { errorHandler } from "./middleware/error.middleware"

export function createApp(): Application {
  const app = express()

  // 1. Security headers (first)
  app.use(helmet())

  // 2. CORS
  app.use(cors())

  // 3. Logging
  app.use(morgan("combined"))
  app.use(loggingMiddleware)

  // 4. Body parsing
  app.use(express.json())
  app.use(express.urlencoded({ extended: true }))

  // 5. Request ID
  app.use(requestIdMiddleware)

  // 6. Rate limiting (before auth)
  app.use(rateLimiter)

  // 7. Authentication (before routes)
  app.use(authMiddleware)

  // 8. Routes
  app.use("/api", routes)

  // 9. 404 handler
  app.use(notFoundHandler)

  // 10. Error handler (must be last)
  app.use(errorHandler)

  return app
}
```

---

## 8. Related Skills

- [`03-backend-api/express-rest`](03-backend-api/express-rest/SKILL.md)
- [`03-backend-api/nodejs-api`](03-backend-api/nodejs-api/SKILL.md)
- [`03-backend-api/error-handling`](03-backend-api/error-handling/SKILL.md)
- [`03-backend-api/validation`](03-backend-api/validation/SKILL.md)
- [`10-authentication-authorization`](10-authentication-authorization/SKILL.md)
- [`14-monitoring-observability`](14-monitoring-observability/SKILL.md)
