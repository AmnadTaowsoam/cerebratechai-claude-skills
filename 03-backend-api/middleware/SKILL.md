# Backend Middleware Patterns

## 1. Middleware Concept

### What is Middleware?
Middleware functions have access to the request object (req), the response object (res), and the next middleware function in the application's request-response cycle.

### Middleware Flow
```
Request → Middleware 1 → Middleware 2 → ... → Route Handler → Response
              ↓ (next)         ↓ (next)                ↓
            Middleware 2 → ... → Response
```

### Middleware Types
1. **Application-level middleware**: Applied to all routes
2. **Router-level middleware**: Applied to specific router
3. **Route-level middleware**: Applied to specific routes
4. **Error-handling middleware**: Handles errors

## 2. Express Middleware

### Request Logging
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

### Authentication
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

### Authorization (Role-based)
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

### Error Handling
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

### Request Validation
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

### Rate Limiting
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

// Custom rate limiter with Redis
import RedisStore from "rate-limit-redis"
import { createClient } from "redis"

const redisClient = createClient({
  url: process.env.REDIS_URL,
})

const redisStore = new RedisStore({
  client: redisClient,
  prefix: "rate-limit:",
})

const redisLimiter = rateLimit({
  store: redisStore,
  windowMs: 60 * 60 * 1000,
  max: 100,
})
```

### CORS Configuration
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

### Security Headers
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

### Body Parser
```typescript
// middleware/body-parser.middleware.ts
import { Request, Response, NextFunction } from "express"
import { z } from "zod"

// JSON body parser with validation
export const jsonBodyParser = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  // Express.json() is usually applied globally
  // This is for additional processing
  if (req.is("application/json")) {
    try {
      // Validate JSON structure
      JSON.parse(req.body)
    } catch (error) {
      return res.status(400).json({
        success: false,
        message: "Invalid JSON",
      })
    }
  }
  next()
}

// URL-encoded body parser
export const urlEncodedParser = (
  req: Request,
  res: Response,
  next: NextFunction
): void => {
  if (req.is("application/x-www-form-urlencoded")) {
    // Additional processing for form data
    console.log("Processing form data")
  }
  next()
}

// Multipart form data
import multer from "multer"

const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 5 * 1024 * 1024, // 5MB
    files: 10,
  },
})

export const multipartParser = upload.single("file")
```

## 3. FastAPI Middleware

### CORS
```python
# middleware/cors.py
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://example.com",
]

cors_middleware = CORSMiddleware(
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Trusted Hosts
```python
# middleware/trusted_hosts.py
from fastapi.middleware.trustedhost import TrustedHostMiddleware

trusted_hosts = [
    "example.com",
    "*.example.com",
    "localhost",
]

trusted_host_middleware = TrustedHostMiddleware(
    allowed_hosts=trusted_hosts,
)
```

### GZip Compression
```python
# middleware/compression.py
from fastapi.middleware.gzip import GZipMiddleware

gzip_middleware = GZipMiddleware(minimum_size=1000)
```

### Custom Middleware
```python
# middleware/logging.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
import logging

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # Log request
        logger.info({
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "client": request.client.host if request.client else None,
        })
        
        # Process request
        response = await call_next(request)
        
        # Calculate duration
        process_time = (time.time() - start_time) * 1000
        
        # Log response
        logger.info({
            "request_id": request_id,
            "status_code": response.status_code,
            "process_time_ms": round(process_time, 2),
        })
        
        # Add custom header
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
```

### Request ID Middleware
```python
# middleware/request_id.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.request_id = str(uuid.uuid4())
        response = await call_next(request)
        response.headers["X-Request-ID"] = request.state.request_id
        return response
```

### Timing Middleware
```python
# middleware/timing.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import time


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        process_time = time.time() - start_time
        response.headers["X-Response-Time"] = str(process_time)
        
        return response
```

### Authentication Middleware
```python
# middleware/auth.py
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from app.core.config import settings

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: dict = Depends(get_current_user)
):
    if not current_user.get("is_active"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user
```

## 4. Middleware Order

### Correct Order
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

### Wrong Order Examples
```typescript
// ❌ Wrong: Error handler before routes
app.use(errorHandler)  // Will catch errors too early
app.use("/api", routes)

// ❌ Wrong: Body parser after routes
app.use("/api", routes)
app.use(express.json())  // Won't parse route bodies

// ❌ Wrong: CORS after routes
app.use("/api", routes)
app.use(cors())  // CORS headers won't be set
```

## 5. Testing Middleware

### Express Middleware Tests
```typescript
// tests/middleware/auth.middleware.test.ts
import { Request, Response, NextFunction } from "express"
import { authMiddleware } from "../../middleware/auth.middleware"
import jwt from "jsonwebtoken"

describe("Auth Middleware", () => {
  let mockReq: Partial<Request>
  let mockRes: Partial<Response>
  let mockNext: NextFunction

  beforeEach(() => {
    mockReq = {
      headers: {},
    }
    mockRes = {
      status: jest.fn().mockReturnThis(),
      json: jest.fn().mockReturnThis(),
    }
    mockNext = jest.fn()
  })

  it("should pass with valid token", () => {
    const token = jwt.sign({ userId: "123" }, "secret")
    mockReq.headers!.authorization = `Bearer ${token}`

    authMiddleware(mockReq as Request, mockRes as Response, mockNext)

    expect(mockNext).toHaveBeenCalled()
    expect((mockReq as any).user).toBeDefined()
    expect((mockReq as any).user.userId).toBe("123")
  })

  it("should fail without token", () => {
    authMiddleware(mockReq as Request, mockRes as Response, mockNext)

    expect(mockNext).toHaveBeenCalledWith(expect.any(Error))
    expect(mockRes.status).toHaveBeenCalledWith(401)
    expect(mockRes.json).toHaveBeenCalledWith({
      success: false,
      message: expect.stringContaining("token"),
    })
  })

  it("should fail with invalid token", () => {
    mockReq.headers!.authorization = "Bearer invalid-token"

    authMiddleware(mockReq as Request, mockRes as Response, mockNext)

    expect(mockNext).toHaveBeenCalledWith(expect.any(Error))
    expect(mockRes.status).toHaveBeenCalledWith(401)
  })
})
```

### FastAPI Middleware Tests
```python
# tests/middleware/test_logging.py
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch, MagicMock

client = TestClient(app)


def test_logging_middleware_adds_request_id():
    response = client.get("/api/v1/users")
    
    assert "X-Request-ID" in response.headers
    assert len(response.headers["X-Request-ID"]) == 36  # UUID length


def test_logging_middleware_logs_request(caplog):
    with patch("app.middleware.logging.logger") as mock_logger:
        client.get("/api/v1/users")
        
        # Check that logger.info was called
        assert mock_logger.info.called
        
        # Check log content
        call_args = mock_logger.info.call_args
        assert "request_id" in call_args[0]
        assert "method" in call_args[0]
        assert "url" in call_args[0]


def test_logging_middleware_adds_process_time():
    response = client.get("/api/v1/users")
    
    assert "X-Process-Time" in response.headers
    process_time = float(response.headers["X-Process-Time"])
    assert process_time >= 0
```

## 6. Common Middleware Patterns

### Conditional Middleware
```typescript
// middleware/conditional.middleware.ts
import { Request, Response, NextFunction } from "express"

export function conditionalMiddleware(
  condition: boolean,
  middleware: (req: Request, res: Response, next: NextFunction) => void
) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (condition) {
      return middleware(req, res, next)
    }
    next()
  }
}

// Usage
router.get(
  "/admin/users",
  conditionalMiddleware(process.env.NODE_ENV === "production", authMiddleware),
  userController.getAll
)
```

### Middleware Composition
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

### Async Middleware Wrapper
```typescript
// middleware/async.middleware.ts
import { Request, Response, NextFunction } from "express"

export function asyncMiddleware(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>
) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next)
  }
}

// Usage in controllers
router.get("/users", asyncMiddleware(async (req, res) => {
  const users = await userService.findAll()
  res.json(users)
}))
```

### Error Boundary Middleware
```typescript
// middleware/error-boundary.middleware.ts
import { Request, Response, NextFunction } from "express"

export function errorBoundaryMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  const originalJson = res.json.bind(res)

  res.json = function (data: any) {
    // Check if this is an error response
    if (data && data.success === false) {
      // Log error
      console.error("API Error:", data)
    }

    return originalJson(data)
  }

  next()
}
```

### Request Context Middleware
```typescript
// middleware/context.middleware.ts
import { Request, Response, NextFunction } from "express"

interface RequestContext {
  requestId: string
  startTime: number
  userId?: string
}

declare global {
  namespace Express {
    interface Request {
      context: RequestContext
    }
  }
}

export function contextMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  req.context = {
    requestId: req.id || "unknown",
    startTime: Date.now(),
  }

  next()
}
```

### Cache Control Middleware
```typescript
// middleware/cache.middleware.ts
import { Request, Response, NextFunction } from "express"

export function cacheControl(maxAge: number) {
  return (req: Request, res: Response, next: NextFunction) => {
    res.setHeader("Cache-Control", `public, max-age=${maxAge}`)
    next()
  }
}

// Usage
router.get(
  "/static/data",
  cacheControl(3600), // 1 hour
  staticDataController.get
)
```

### Request Sanitization Middleware
```typescript
// middleware/sanitize.middleware.ts
import { Request, Response, NextFunction } from "express"
import xss from "xss"

export function sanitizeBody(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  if (req.body) {
    if (typeof req.body === "object") {
      for (const key in req.body) {
        if (typeof req.body[key] === "string") {
          req.body[key] = xss(req.body[key])
        }
      }
    } else if (typeof req.body === "string") {
      req.body = xss(req.body)
    }
  }

  next()
}

// Usage
router.post(
  "/comments",
  sanitizeBody,
  commentController.create
)
```

### Request Size Limit Middleware
```typescript
// middleware/size-limit.middleware.ts
import { Request, Response, NextFunction } from "express"

export function sizeLimit(maxSize: number) {
  return (req: Request, res: Response, next: NextFunction) => {
    const contentLength = parseInt(req.get("content-length") || "0", 10)

    if (contentLength > maxSize) {
      return res.status(413).json({
        success: false,
        message: `Request entity too large. Max size is ${maxSize} bytes`,
      })
    }

    next()
  }
}

// Usage
router.post(
  "/upload",
  sizeLimit(10 * 1024 * 1024), // 10MB
  uploadController.upload
)
```
