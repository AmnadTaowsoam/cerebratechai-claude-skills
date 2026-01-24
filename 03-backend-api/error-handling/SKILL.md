# Backend Error Handling Patterns

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

Error Handling เป็นส่วนสำคัญของ backend development ที่ช่วยให้ applications ทำงานได้อย่าง reliable, maintainable, และ debuggable โดยมี patterns และ best practices สำหรับ handling, logging, และ monitoring errors

Error Handling ประกอบด้วย:
- **Error Classification** - แยกแยะ error types (operational vs programmer errors)
- **Custom Error Classes** - สร้าง error classes ที่ domain-specific
- **Error Middleware** - Global error handlers สำหรับ consistent responses
- **Error Logging** - Logging errors สำหรับ debugging และ monitoring
- **Error Monitoring** - External monitoring services (Sentry, etc.)
- **Error Recovery** - Retry, fallback, และ circuit breaker patterns

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **ลด Downtime** - Proper error handling ช่วยลด downtime ได้ถึง 40-60%
2. **เพิ่ม User Experience** - Graceful error handling ช่วยเพิ่ม UX
3. **ลด Debugging Time** - Structured error logging ช่วยลดเวลา debug
4. **เพิ่ม Maintainability** - Consistent error handling ช่วยเพิ่ม maintainability
5. **ปรับปรุง Reliability** - Error recovery patterns ช่วยเพิ่ม reliability

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **User-Friendly** - Error messages ต้อง user-friendly และ actionable
2. **Secure** - ไม่ expose sensitive information ใน error responses
3. **Observable** - Errors ต้อง observable ด้วย logging และ monitoring
4. **Recoverable** - Errors ต้อง recoverable ด้วย retry และ fallback
5. **Testable** - Error handling ต้อง testable ง่าย

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

Backend Error Handling ประกอบด้วย:

1. **Error Classification** - Operational vs Programmer errors
2. **Custom Error Classes** - Domain-specific error types
3. **Error Middleware** - Global error handlers
4. **Error Responses** - Consistent response formats
5. **Error Logging** - Structured logging
6. **Error Monitoring** - External monitoring services
7. **Error Recovery** - Retry, fallback, circuit breaker

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              Error Handling Architecture               │
├─────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Request Layer                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  HTTP       │  │  WebSocket  │  │  gRPC       │  │   │
│  │  │  Requests   │  │  Requests   │  │  Requests   │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Application Layer                    │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Business   │  │  Validation │  │  Services  │  │   │
│  │  │  Logic      │  │  Layer      │  │            │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Error Handling Layer                │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Error      │  │  Error      │  │  Error     │  │   │
│  │  │  Classes    │  │  Middleware │  │  Factory   │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Monitoring Layer                      │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │   │
│  │  │  Logging    │  │  Monitoring │  │  Alerts    │  │   │
│  │  │  System     │  │  Services   │  │            │  │   │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │   │
│  └───────────────────────────────────────────────────┘   │
│                           │                                     │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

**Step 1: Create Error Classes**

```typescript
// types/errors.ts
export class OperationalError extends Error {
  constructor(
    public statusCode: number = 500,
    public message: string = "An error occurred",
    public isOperational: boolean = true
  ) {
    super(message)
    this.name = this.constructor.name
    Error.captureStackTrace(this, this.constructor)
  }
}
```

**Step 2: Create Error Middleware**

```typescript
// middleware/error.middleware.ts
export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  // Handle errors
}
```

**Step 3: Setup Logging**

```typescript
// utils/logger.ts
const logger = winston.createLogger({
  // Configure logger
})
```

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Version | License |
|------|---------|---------|---------|
| Winston | Logging Library | ^3.11.0 | MIT |
| Sentry | Error Monitoring | ^7.0.0 | BSD-3-Clause |
| Express Validator | Validation Middleware | ^7.0.0 | MIT |
| Zod | Schema Validation | ^3.22.0 | MIT |
| Axios | HTTP Client | ^1.6.0 | MIT |
| p-retry | Retry Utility | ^6.2.0 | MIT |
| opossum | Circuit Breaker | ^8.1.0 | Apache-2.0 |

### 3.2 Configuration Essentials

**Winston Configuration:**
```typescript
// utils/logger.ts
import winston from "winston"

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || "info",
  format: winston.format.combine(
    winston.format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      ),
    }),
    new winston.transports.File({
      filename: "logs/combined.log",
      level: "info",
    }),
    new winston.transports.File({
      filename: "logs/error.log",
      level: "error",
    }),
  ],
  exceptionHandlers: [
    new winston.transports.File({
      filename: "logs/exceptions.log",
    }),
  ],
})

export default logger
```

**Sentry Configuration:**
```typescript
// monitoring/sentry.ts
import * as Sentry from "@sentry/node"

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV || "development",
  tracesSampleRate: 1.0,
  beforeSend(event) {
    // Filter out operational errors
    if (event.exception?.values?.[0]?.mechanism?.type === "express") {
      const error = event.request?.error as any
      if (error?.isOperational) {
        return null
      }
    }
    return event
  },
})

export { Sentry }
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **RFC 7807** - Problem Details for HTTP APIs
- **OWASP** - Security Best Practices
- **GDPR** - Data Protection สำหรับ Error Logs
- **HIPAA** - Healthcare Data Protection
- **PCI DSS** - Payment Card Industry Standards

### 4.2 Security Protocol

Error Handling ต้องปฏิบัติตามหลักความปลอดภัย:

1. **No Sensitive Data** - ไม่ expose sensitive information ใน error responses
2. **Secure Logging** - ไม่ log passwords, tokens, หรือ sensitive data
3. **Error Sanitization** - Sanitize error messages ก่อนส่งให้ client
4. **Rate Limiting** - จำกัดจำนวน error reports
5. **Secure Monitoring** - ใช้ secure connections สำหรับ monitoring

### 4.3 Explainability

Error Handling ต้องสามารถอธิบายได้ว่า:

1. **Error Classification** - ทำไม error ถูก classify อย่างไร
2. **Error Logging** - ทำไม errors ถูก log อย่างไร
3. **Error Monitoring** - ทำไม errors ถูก monitor อย่างไร
4. **Error Recovery** - ทำไม errors ถูก recover อย่างไร

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

| Metric | Calculation | Target |
|--------|-------------|--------|
| Error Rate | Errors / Total Requests | < 1% |
| Recovery Rate | Recovered Errors / Total Errors | > 90% |
| MTTR (Mean Time to Recovery) | Average recovery time | < 5 min |
| Error Response Time | Error handling latency | < 100ms |
| Logging Overhead | Logging performance impact | < 5% |

### 5.2 Key Performance Indicators

**Technical Metrics:**

1. **Error Rate** - Error rate ต่อ requests
2. **Recovery Rate** - Error recovery rate
3. **MTTR** - Mean Time to Recovery
4. **Error Response Time** - Error handling latency

**Business Metrics:**

1. **User Impact** - Users affected by errors
2. **Downtime** - System downtime
3. **Support Tickets** - Support tickets จาก errors
4. **Customer Satisfaction** - CSAT score

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Week 1-2)**
- Create error classes
- Setup error middleware
- Implement basic logging
- Create error response formats

**Phase 2: Advanced Features (Week 3-4)**
- Add error classification
- Implement error monitoring
- Add error recovery patterns
- Create error factory

**Phase 3: Integration (Week 5-6)**
- Integrate with monitoring services
- Add alerting
- Implement circuit breakers
- Setup error dashboards

**Phase 4: Production (Week 7-8)**
- Performance optimization
- Documentation and training
- Error reporting workflows
- Best practices documentation

### 6.2 Pitfalls to Avoid

1. **Swallowing Errors** - ไม่ catch และ ignore errors
2. **Exposing Stack Traces** - ไม่ expose stack traces ใน production
3. **Poor Error Messages** - ไม่ใช้ error messages ที่ user-friendly
4. **Missing Logging** - ไม่ log errors อย่างเหมาะสม
5. **No Monitoring** - ไม่ monitor errors
6. **Poor Recovery** - ไม่ implement error recovery

### 6.3 Best Practices Checklist

- [ ] ใช้ custom error classes สำหรับ domain-specific errors
- [ ] Classify errors เป็น operational vs programmer errors
- [ ] Implement global error middleware
- [ ] Use consistent error response formats
- [ ] Log errors ด้วย structured logging
- [ ] Monitor errors ด้วย external services
- [ ] Implement error recovery patterns
- [ ] Use circuit breakers สำหรับ external services
- [ ] Test error scenarios
- [ ] Sanitize error messages สำหรับ production
- [ ] Implement retry logic สำหรับ transient errors
- [ ] Use fallback strategies สำหรับ critical failures
- [ ] Document error codes และ messages
- [ ] Setup alerting สำหรับ critical errors
- [ ] Review error logs regularly

---

## 7. Implementation Examples

### 7.1 Error Types and Classification

**Error Categories:**
```typescript
// types/errors.ts

// Operational Errors (expected, user errors)
export class OperationalError extends Error {
  constructor(
    public statusCode: number = 500,
    public message: string = "An error occurred",
    public isOperational: boolean = true
  ) {
    super(message)
    this.name = this.constructor.name
    Error.captureStackTrace(this, this.constructor)
  }
}

// Programmer Errors (bugs, unexpected)
export class ProgrammerError extends Error {
  constructor(message: string) {
    super(message)
    this.name = this.constructor.name
    this.isOperational = false
    Error.captureStackTrace(this, this.constructor)
  }
}

// HTTP Error Types
export class BadRequestError extends OperationalError {
  constructor(message: string = "Bad request") {
    super(400, message)
  }
}

export class UnauthorizedError extends OperationalError {
  constructor(message: string = "Unauthorized") {
    super(401, message)
  }
}

export class ForbiddenError extends OperationalError {
  constructor(message: string = "Forbidden") {
    super(403, message)
  }
}

export class NotFoundError extends OperationalError {
  constructor(message: string = "Not found") {
    super(404, message)
  }
}

export class ConflictError extends OperationalError {
  constructor(message: string = "Conflict") {
    super(409, message)
  }
}

export class UnprocessableEntityError extends OperationalError {
  constructor(message: string = "Unprocessable entity") {
    super(422, message)
  }
}

export class InternalServerError extends OperationalError {
  constructor(message: string = "Internal server error") {
    super(500, message)
  }
}

export class ServiceUnavailableError extends OperationalError {
  constructor(message: string = "Service unavailable") {
    super(503, message)
  }
}
```

**Error Classification:**
```typescript
// utils/error-classifier.ts
import { OperationalError, ProgrammerError } from "../types/errors"

export function isOperationalError(error: Error): boolean {
  if (error instanceof OperationalError) {
    return error.isOperational
  }
  return false
}

export function isProgrammerError(error: Error): boolean {
  return error instanceof ProgrammerError || !error.isOperational
}

export function isTrustedError(error: Error): boolean {
  if (error instanceof Error) {
    return isOperationalError(error)
  }
  return false
}
```

### 7.2 Custom Error Classes

**Base Error Class:**
```typescript
// errors/app.error.ts
export class AppError extends Error {
  constructor(
    public statusCode: number,
    public message: string,
    public details?: any,
    public isOperational: boolean = true
  ) {
    super(message)
    this.name = this.constructor.name
    Error.captureStackTrace(this, this.constructor)
  }
}
```

**Validation Error:**
```typescript
// errors/validation.error.ts
import { AppError } from "./app.error"

interface ValidationErrorDetail {
  field: string
  message: string
  value?: any
}

export class ValidationError extends AppError {
  constructor(
    message: string = "Validation failed",
    public details: ValidationErrorDetail[] = []
  ) {
    super(422, message, details)
  }
}
```

**Database Error:**
```typescript
// errors/database.error.ts
import { AppError } from "./app.error"

export class DatabaseError extends AppError {
  constructor(message: string = "Database error occurred") {
    super(500, message)
  }
}

export class RecordNotFoundError extends AppError {
  constructor(resource: string = "Record") {
    super(404, `${resource} not found`)
  }
}

export class DuplicateRecordError extends AppError {
  constructor(resource: string = "Record") {
    super(409, `${resource} already exists`)
  }
}
```

**Authentication Error:**
```typescript
// errors/auth.error.ts
import { AppError } from "./app.error"

export class AuthenticationError extends AppError {
  constructor(message: string = "Authentication failed") {
    super(401, message)
  }
}

export class TokenExpiredError extends AppError {
  constructor() {
    super(401, "Token has expired")
  }
}

export class InvalidTokenError extends AppError {
  constructor() {
    super(401, "Invalid token")
  }
}
```

**Authorization Error:**
```typescript
// errors/authorization.error.ts
import { AppError } from "./app.error"

export class AuthorizationError extends AppError {
  constructor(message: string = "Insufficient permissions") {
    super(403, message)
  }
}

export class RoleRequiredError extends AppError {
  constructor(requiredRole: string) {
    super(403, `This action requires ${requiredRole} role`)
  }
}
```

### 7.3 Error Middleware (Express)

**Global Error Handler:**
```typescript
// middleware/error.middleware.ts
import { Request, Response, NextFunction } from "express"
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
    ip: req.ip,
    userAgent: req.get("user-agent"),
  })

  // Handle known application errors
  if (error instanceof AppError) {
    return res.status(error.statusCode).json({
      success: false,
      message: error.message,
      ...(error.details && { details: error.details }),
    })
  }

  // Handle validation errors
  if (error.name === "ValidationError") {
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

  if (error.name === "TokenExpiredError") {
    return res.status(401).json({
      success: false,
      message: "Token expired",
    })
  }

  // Handle Multer errors
  if (error.name === "MulterError") {
    return res.status(400).json({
      success: false,
      message: "File upload error",
    })
  }

  // Handle Mongoose validation errors
  if (error.name === "ValidationError") {
    return res.status(400).json({
      success: false,
      message: "Validation error",
      details: Object.values((error as any).errors).map((e: any) => ({
        field: e.path,
        message: e.message,
      })),
    })
  }

  // Handle Mongoose duplicate key errors
  if (error.name === "MongoServerError" && (error as any).code === 11000) {
    const field = Object.keys((error as any).keyPattern)[0]
    return res.status(409).json({
      success: false,
      message: `Duplicate value for field: ${field}`,
    })
  }

  // Default error response
  res.status(500).json({
    success: false,
    message: process.env.NODE_ENV === "production"
      ? "Internal server error"
      : error.message,
  })
}
```

**404 Handler:**
```typescript
// middleware/not-found.middleware.ts
import { Request, Response } from "express"

export function notFoundHandler(req: Request, res: Response): void {
  res.status(404).json({
    success: false,
    message: `Route ${req.method} ${req.path} not found`,
  })
}
```

**Async Error Wrapper:**
```typescript
// middleware/async-handler.middleware.ts
import { Request, Response, NextFunction } from "express"

export function asyncHandler(
  fn: (req: Request, res: Response, next: NextFunction) => Promise<any>
) {
  return (req: Request, res: Response, next: NextFunction) => {
    Promise.resolve(fn(req, res, next)).catch(next)
  }
}
```

### 7.4 Error Responses Format

**Standard Response Format:**
```typescript
// utils/response.util.ts
import { Response } from "express"

export interface ErrorResponse {
  success: false
  message: string
  details?: any
  timestamp: string
  path?: string
}

export function sendErrorResponse(
  res: Response,
  statusCode: number,
  message: string,
  details?: any,
  path?: string
): void {
  const response: ErrorResponse = {
    success: false,
    message,
    timestamp: new Date().toISOString(),
    ...(details && { details }),
    ...(path && { path }),
  }

  res.status(statusCode).json(response)
}
```

**Validation Error Response:**
```typescript
export interface ValidationErrorResponse extends ErrorResponse {
  errors: Array<{
    field: string
    message: string
    value?: any
  }>
}

export function sendValidationError(
  res: Response,
  errors: Array<{ field: string; message: string; value?: any }>
): void {
  const response: ValidationErrorResponse = {
    success: false,
    message: "Validation failed",
    errors,
    timestamp: new Date().toISOString(),
  }

  res.status(422).json(response)
}
```

### 7.5 Logging Errors

**Logger Configuration:**
```typescript
// utils/logger.ts
import winston from "winston"

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || "info",
  format: winston.format.combine(
    winston.format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  transports: [
    // Console transport for development
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      ),
    }),
    // File transport for all logs
    new winston.transports.File({
      filename: "logs/combined.log",
      level: "info",
    }),
    // File transport for errors only
    new winston.transports.File({
      filename: "logs/error.log",
      level: "error",
    }),
  ],
  exceptionHandlers: [
    new winston.transports.File({
      filename: "logs/exceptions.log",
    }),
  ],
})

export default logger
```

**Error Logging Middleware:**
```typescript
// middleware/error-logging.middleware.ts
import { Request, Response, NextFunction } from "express"
import logger from "../utils/logger"

export function errorLoggingMiddleware(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  // Log error details
  logger.error({
    message: error.message,
    stack: error.stack,
    path: req.path,
    method: req.method,
    query: req.query,
    body: req.body,
    ip: req.ip,
    userAgent: req.get("user-agent"),
    timestamp: new Date().toISOString(),
  })

  // Pass to error handler
  next(error)
}
```

### 7.6 Error Monitoring

**Sentry Integration:**
```typescript
// monitoring/sentry.ts
import * as Sentry from "@sentry/node"

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV || "development",
  tracesSampleRate: 1.0,
  beforeSend(event) {
    // Filter out operational errors
    if (event.exception?.values?.[0]?.mechanism?.type === "express") {
      const error = event.request?.error as any
      if (error?.isOperational) {
        return null // Don't send operational errors
      }
    }
    return event
  },
})

export { Sentry }
```

**Error Tracking Middleware:**
```typescript
// middleware/error-tracking.middleware.ts
import { Request, Response, NextFunction } from "express"
import { Sentry } from "../monitoring/sentry"
import { logger } from "../utils/logger"
import { isProgrammerError } from "../utils/error-classifier"

export function errorTrackingMiddleware(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  // Log all errors
  logger.error(error, {
    path: req.path,
    method: req.method,
    userId: (req as any).user?.id,
  })

  // Send programmer errors to Sentry
  if (isProgrammerError(error)) {
    Sentry.captureException(error)
  }

  // Pass to error handler
  next(error)
}
```

### 7.7 Validation Errors

**Express Validator Errors:**
```typescript
// middleware/validation.middleware.ts
import { Request, Response, NextFunction } from "express"
import { validationResult } from "express-validator"

export function handleValidationErrors(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  const errors = validationResult(req)

  if (!errors.isEmpty()) {
    const formattedErrors = errors.array().map((error) => ({
      field: error.param,
      message: error.msg,
      value: error.value,
    }))

    return res.status(400).json({
      success: false,
      message: "Validation failed",
      errors: formattedErrors,
    })
  }

  next()
}
```

**Zod Validation Errors:**
```typescript
// middleware/zod-validation.middleware.ts
import { Request, Response, NextFunction } from "express"
import { ZodError } from "zod"

export function handleZodErrors(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  if (error instanceof ZodError) {
    const formattedErrors = error.errors.map((err) => ({
      field: err.path.join("."),
      message: err.message,
      code: err.code,
    }))

    return res.status(400).json({
      success: false,
      message: "Validation failed",
      errors: formattedErrors,
    })
  }

  next(error)
}
```

### 7.8 Database Errors

**Prisma Error Handling:**
```typescript
// errors/prisma.error.ts
import { Prisma } from "@prisma/client"

export function handlePrismaError(error: any): Error {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    // Unique constraint violation
    if (error.code === "P2002") {
      return new Error("A unique constraint would be violated")
    }

    // Record not found
    if (error.code === "P2025") {
      return new Error("Record not found")
    }

    // Foreign key constraint violation
    if (error.code === "P2003") {
      return new Error("Foreign key constraint failed")
    }
  }

  if (error instanceof Prisma.PrismaClientUnknownRequestError) {
    return new Error("Unknown database error")
  }

  if (error instanceof Prisma.PrismaClientRustPanicError) {
    return new Error("Database panic")
  }

  if (error instanceof Prisma.PrismaClientInitializationError) {
    return new Error("Database initialization error")
  }

  return error
}
```

**Mongoose Error Handling:**
```typescript
// errors/mongoose.error.ts
import mongoose from "mongoose"

export function handleMongooseError(error: any): Error {
  if (error instanceof mongoose.Error.ValidationError) {
    return new Error("Validation error")
  }

  if (error instanceof mongoose.Error.CastError) {
    return new Error("Invalid data type")
  }

  if (error.name === "MongoServerError" && error.code === 11000) {
    const field = Object.keys(error.keyPattern)[0]
    return new Error(`Duplicate value for field: ${field}`)
  }

  return error
}
```

### 7.9 External API Errors

**External API Error Handler:**
```typescript
// errors/external-api.error.ts
import { AppError } from "./app.error"

export class ExternalAPIError extends AppError {
  constructor(
    public service: string,
    public originalError: any,
    message?: string
  ) {
    super(
      502,
      message || `Error communicating with ${service}`,
      {
        service,
        originalError: originalError.message,
      }
    )
  }
}

export class ExternalAPIValidationError extends AppError {
  constructor(
    public service: string,
    public validationErrors: any[]
  ) {
    super(
      422,
      `Validation error from ${service}`,
      { service, validationErrors }
    )
  }
}

export class ExternalAPITimeoutError extends AppError {
  constructor(
    public service: string,
    public timeout: number
  ) {
    super(
      504,
      `Timeout waiting for ${service}`,
      { service, timeout }
    )
  }
}
```

**External API Wrapper:**
```typescript
// utils/external-api.util.ts
import { ExternalAPIError, ExternalAPITimeoutError } from "../errors/external-api.error"

export async function fetchFromExternalAPI<T>(
  serviceName: string,
  url: string,
  options: RequestInit = {},
  timeout: number = 5000
): Promise<T> {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), timeout)

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    })

    clearTimeout(timeoutId)

    if (!response.ok) {
      if (response.status === 422) {
        const data = await response.json()
        throw new ExternalAPIValidationError(serviceName, data.errors)
      }

      throw new ExternalAPIError(serviceName, {
        status: response.status,
        statusText: response.statusText,
      })
    }

    return response.json()
  } catch (error) {
    clearTimeout(timeoutId)

    if (error.name === "AbortError") {
      throw new ExternalAPITimeoutError(serviceName, timeout)
    }

    throw new ExternalAPIError(serviceName, error)
  }
}
```

### 7.10 Operational vs Programmer Errors

**Error Handler with Classification:**
```typescript
// middleware/classified-error.middleware.ts
import { Request, Response, NextFunction } from "express"
import { isOperationalError, isProgrammerError } from "../utils/error-classifier"
import { logger } from "../utils/logger"
import { Sentry } from "../monitoring/sentry"

export function classifiedErrorHandler(
  error: Error,
  req: Request,
  res: Response,
  next: NextFunction
): void {
  // Log all errors
  logger.error(error, {
    path: req.path,
    method: req.method,
    isOperational: isOperationalError(error),
  })

  // Operational errors - expected, handle gracefully
  if (isOperationalError(error)) {
    return res.status((error as any).statusCode || 500).json({
      success: false,
      message: error.message,
    })
  }

  // Programmer errors - unexpected, report to monitoring
  if (isProgrammerError(error)) {
    Sentry.captureException(error)

    return res.status(500).json({
      success: false,
      message: process.env.NODE_ENV === "production"
        ? "Internal server error"
        : error.message,
    })
  }

  // Unknown errors
  Sentry.captureException(error)
  res.status(500).json({
    success: false,
    message: "Internal server error",
  })
}
```

**Error Factory:**
```typescript
// utils/error-factory.util.ts
import { AppError } from "../errors/app.error"
import { ValidationError, DatabaseError, AuthenticationError } from "../errors"

export const ErrorFactory = {
  badRequest: (message: string) => new AppError(400, message),

  unauthorized: (message?: string) => new AuthenticationError(message),

  forbidden: (message?: string) => new AppError(403, message || "Forbidden"),

  notFound: (resource: string = "Resource") => new AppError(404, `${resource} not found`),

  conflict: (message: string) => new AppError(409, message),

  validation: (details: any[]) => new ValidationError("Validation failed", details),

  database: (message: string) => new DatabaseError(message),

  internal: (message?: string) => new AppError(500, message || "Internal server error"),
}

// Usage
throw ErrorFactory.badRequest("Invalid input")
throw ErrorFactory.unauthorized("Invalid credentials")
throw ErrorFactory.notFound("User")
```

### 7.11 Error Recovery Strategies

**Retry Strategy:**
```typescript
// utils/retry.util.ts
export async function retry<T>(
  fn: () => Promise<T>,
  options: {
    maxAttempts?: number
    delay?: number
    backoff?: boolean
  } = {}
): Promise<T> {
  const {
    maxAttempts = 3,
    delay = 1000,
    backoff = true,
  } = options

  let lastError: Error

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn()
    } catch (error) {
      lastError = error as Error

      if (attempt === maxAttempts) {
        throw lastError
      }

      const waitTime = backoff ? delay * attempt : delay
      await new Promise(resolve => setTimeout(resolve, waitTime))
    }
  }

  throw lastError!
}

// Usage
const result = await retry(
  () => fetchFromExternalAPI("service", url),
  { maxAttempts: 3, delay: 1000 }
)
```

**Fallback Strategy:**
```typescript
// utils/fallback.util.ts
export async function withFallback<T>(
  primaryFn: () => Promise<T>,
  fallbackFn: () => Promise<T>,
  shouldFallback?: (error: Error) => boolean
): Promise<T> {
  try {
    return await primaryFn()
  } catch (error) {
    if (shouldFallback && !shouldFallback(error)) {
      throw error
    }
    return await fallbackFn()
  }
}

// Usage
const data = await withFallback(
  () => fetchFromPrimaryDB(id),
  () => fetchFromCache(id),
  (error) => error instanceof DatabaseError
)
```

**Circuit Breaker Pattern:**
```typescript
// utils/circuit-breaker.util.ts
export class CircuitBreaker {
  private failures = 0
  private lastFailureTime: number | null = null
  private state: "closed" | "open" | "half-open" = "closed"

  constructor(
    private threshold: number = 5,
    private timeout: number = 60000 // 1 minute
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === "open") {
      if (this.shouldAttemptReset()) {
        this.state = "half-open"
      } else {
        throw new Error("Circuit breaker is open")
      }
    }

    try {
      const result = await fn()
      this.onSuccess()
      return result
    } catch (error) {
      this.onFailure()
      throw error
    }
  }

  private onSuccess(): void {
    this.failures = 0
    this.state = "closed"
  }

  private onFailure(): void {
    this.failures++
    this.lastFailureTime = Date.now()

    if (this.failures >= this.threshold) {
      this.state = "open"
    }
  }

  private shouldAttemptReset(): boolean {
    return (
      this.lastFailureTime !== null &&
      Date.now() - this.lastFailureTime > this.timeout
    )
  }
}

// Usage
const circuitBreaker = new CircuitBreaker(5, 60000)

try {
  const result = await circuitBreaker.execute(() => fetchFromExternalAPI("service", url))
} catch (error) {
  // Handle circuit breaker open
}
```

### 7.12 Testing Error Scenarios

**Error Handler Tests:**
```typescript
// tests/middleware/error.middleware.test.ts
import request from "supertest"
import { createApp } from "../../src/app"
import { AppError } from "../../src/errors/app.error"
import { ValidationError } from "../../src/errors/validation.error"

describe("Error Handler", () => {
  let app: Express

  beforeAll(() => {
    app = createApp()
  })

  describe("AppError handling", () => {
    it("should return 400 for BadRequestError", async () => {
      const response = await request(app).get("/test/bad-request")

      expect(response.status).toBe(400)
      expect(response.body.success).toBe(false)
      expect(response.body.message).toBeDefined()
    })

    it("should return 404 for NotFoundError", async () => {
      const response = await request(app).get("/test/not-found")

      expect(response.status).toBe(404)
      expect(response.body.message).toContain("not found")
    })

    it("should return 401 for UnauthorizedError", async () => {
      const response = await request(app).get("/test/unauthorized")

      expect(response.status).toBe(401)
      expect(response.body.message).toContain("Unauthorized")
    })

    it("should return 403 for ForbiddenError", async () => {
      const response = await request(app).get("/test/forbidden")

      expect(response.status).toBe(403)
      expect(response.body.message).toContain("Forbidden")
    })
  })

  describe("ValidationError handling", () => {
    it("should return 422 with validation details", async () => {
      const response = await request(app)
        .post("/test/validation")
        .send({ invalid: "data" })

      expect(response.status).toBe(422)
      expect(response.body.success).toBe(false)
      expect(response.body.message).toBe("Validation failed")
      expect(response.body.errors).toBeInstanceOf(Array)
    })
  })

  describe("Programmer error handling", () => {
    it("should log programmer errors", async () => {
      const loggerSpy = jest.spyOn(logger, "error")

      await request(app).get("/test/programmer-error")

      expect(loggerSpy).toHaveBeenCalled()
    })

    it("should not expose error details in production", async () => {
      const originalEnv = process.env.NODE_ENV
      process.env.NODE_ENV = "production"

      const response = await request(app).get("/test/programmer-error")

      expect(response.status).toBe(500)
      expect(response.body.message).toBe("Internal server error")
      expect(response.body).not.toHaveProperty("stack")

      process.env.NODE_ENV = originalEnv
    })
  })
})
```

**Service Error Tests:**
```typescript
// tests/services/user.service.test.ts
import { UserService } from "../../src/services/user.service"
import { NotFoundError, ConflictError } from "../../src/errors"

describe("UserService Error Handling", () => {
  let userService: UserService
  let mockUserRepository: jest.Mocked<UserRepository>

  beforeEach(() => {
    mockUserRepository = {
      findById: jest.fn(),
      findByEmail: jest.fn(),
      create: jest.fn(),
      update: jest.fn(),
      delete: jest.fn(),
    } as any

    userService = new UserService(mockUserRepository)
  })

  describe("findById", () => {
    it("should throw NotFoundError when user not found", async () => {
      mockUserRepository.findById.mockResolvedValue(null)

      await expect(userService.findById("1")).rejects.toThrow(NotFoundError)
      await expect(userService.findById("1")).rejects.toThrow("User not found")
    })

    it("should return user when found", async () => {
      const user = { id: "1", name: "John" }
      mockUserRepository.findById.mockResolvedValue(user)

      const result = await userService.findById("1")

      expect(result).toEqual(user)
    })
  })

  describe("create", () => {
    it("should throw ConflictError when email exists", async () => {
      const existingUser = { id: "1", email: "john@example.com" }
      mockUserRepository.findByEmail.mockResolvedValue(existingUser)

      await expect(
        userService.create({ name: "John", email: "john@example.com" })
      ).rejects.toThrow(ConflictError)
    })

    it("should create user when email is unique", async () => {
      mockUserRepository.findByEmail.mockResolvedValue(null)
      const newUser = { id: "2", name: "John", email: "john@example.com" }
      mockUserRepository.create.mockResolvedValue(newUser)

      const result = await userService.create({
        name: "John",
        email: "john@example.com",
      })

      expect(result).toEqual(newUser)
    })
  })
})
```

**Python Error Handler Tests:**
```python
# tests/test_error_handlers.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.exceptions import NotFoundException, BadRequestException

client = TestClient(app)


def test_not_found_error():
    response = client.get("/api/v1/users/999")

    assert response.status_code == 404
    assert response.json()["success"] == False
    assert "not found" in response.json()["message"].lower()


def test_bad_request_error():
    response = client.post("/api/v1/users", json={"name": "J"})  # Too short

    assert response.status_code == 400
    assert response.json()["success"] == False
    assert "validation" in response.json()["message"].lower()


def test_validation_error_details():
    response = client.post("/api/v1/users", json={
        "email": "invalid-email",
        "password": "short"
    })

    assert response.status_code == 422
    data = response.json()
    assert data["success"] == False
    assert "errors" in data
    assert isinstance(data["errors"], list)
```

---

## 8. Related Skills

- `03-backend-api/api-design`
- `03-backend-api/validation`
- `03-backend-api/middleware`
- `04-database/database-transactions`
- `14-monitoring-observability`
