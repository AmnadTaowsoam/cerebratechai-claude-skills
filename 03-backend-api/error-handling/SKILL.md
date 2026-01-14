# Backend Error Handling Patterns

## 1. Error Types and Classification

### Error Categories
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

### Error Classification
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

## 2. Custom Error Classes

### Base Error Class
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

### Validation Error
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

### Database Error
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

### Authentication Error
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

### Authorization Error
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

## 3. Error Middleware (Express)

### Global Error Handler
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

### 404 Handler
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

### Async Error Wrapper
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

## 4. Error Responses Format

### Standard Response Format
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

### Validation Error Response
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

## 5. Logging Errors

### Logger Configuration
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

### Error Logging Middleware
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

## 6. Error Monitoring

### Sentry Integration
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

### Error Tracking Middleware
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

## 7. Validation Errors

### Express Validator Errors
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

### Zod Validation Errors
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

## 8. Database Errors

### Prisma Error Handling
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

### Mongoose Error Handling
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

## 9. External API Errors

### External API Error Handler
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

### External API Wrapper
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

## 10. Operational vs Programmer Errors

### Error Handler with Classification
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

### Error Factory
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

## 11. Error Recovery Strategies

### Retry Strategy
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

### Fallback Strategy
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

### Circuit Breaker Pattern
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

## 12. Testing Error Scenarios

### Error Handler Tests
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

### Service Error Tests
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

### Python Error Handler Tests
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
