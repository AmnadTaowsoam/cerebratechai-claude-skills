# API Request Validation Patterns

## 1. Validation Libraries

### Zod (TypeScript)
```typescript
// validators/user.validator.ts
import { z } from "zod"

export const createUserSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters").max(50),
  email: z.string().email("Invalid email address"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Password must contain uppercase letter")
    .regex(/[a-z]/, "Password must contain lowercase letter")
    .regex(/[0-9]/, "Password must contain number"),
  age: z.number().int().positive().min(18, "Must be at least 18"),
  role: z.enum(["user", "admin"], { message: "Invalid role" }),
})

export const updateUserSchema = createUserSchema.partial()

export type CreateUserDto = z.infer<typeof createUserSchema>
export type UpdateUserDto = z.infer<typeof updateUserSchema>
```

### Pydantic (Python)
```python
# validators/user.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    
    @validator("password")
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain uppercase letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain lowercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain number")
        return v


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDBBase(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Joi (Node.js)
```javascript
// validators/user.validator.js
const Joi = require("joi")

const createUserSchema = Joi.object({
  name: Joi.string().min(2).max(50).required(),
  email: Joi.string().email().required(),
  password: Joi.string()
    .min(8)
    .pattern(/[A-Z]/, "uppercase")
    .pattern(/[a-z]/, "lowercase")
    .pattern(/[0-9]/, "number")
    .required(),
  age: Joi.number().integer().positive().min(18).required(),
  role: Joi.string().valid("user", "admin").required(),
})

const updateUserSchema = createUserSchema.fork(["name", "email", "password", "age", "role"])

module.exports = { createUserSchema, updateUserSchema }
```

## 2. Schema Definitions

### Complex Object Schema
```typescript
// validators/order.validator.ts
import { z } from "zod"

export const createOrderSchema = z.object({
  customer: z.object({
    id: z.string().uuid(),
    name: z.string().min(2),
    email: z.string().email(),
    phone: z.string().regex(/^\+?[\d\s-]+$/),
  }),
  items: z.array(z.object({
    productId: z.string().uuid(),
    quantity: z.number().int().positive(),
    price: z.number().positive(),
  })).min(1, "At least one item is required"),
  
  shipping: z.object({
    address: z.string().min(10),
    city: z.string().min(2),
    state: z.string().length(2).regex(/^[A-Z]{2}$/),
    zipCode: z.string().regex(/^\d{5}(-\d{4})?$/),
    country: z.string().length(2).regex(/^[A-Z]{2}$/),
  }),
  
  payment: z.object({
    method: z.enum(["credit_card", "paypal", "bank_transfer"]),
    cardNumber: z.string().regex(/^\d{16}$/).optional(),
    cardExpiry: z.string().regex(/^(0[1-9]|1[0-2])\/\d{2}$/).optional(),
    cardCvv: z.string().regex(/^\d{3,4}$/).optional(),
  }).refine(
    (data) => {
      if (data.method === "credit_card") {
        return !!data.cardNumber && !!data.cardExpiry && !!data.cardCvv
      }
      return true
    },
    {
      message: "Card details required for credit card payment",
      path: ["payment"],
    }
  ),
  
  notes: z.string().max(500).optional(),
})
```

### Nested Schema with Refinement
```typescript
// validators/auth.validator.ts
import { z } from "zod"

export const registerSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  confirmPassword: z.string(),
}).refine(
  (data) => data.password === data.confirmPassword,
  {
    message: "Passwords don't match",
    path: ["confirmPassword"],
  }
)

export const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
})
```

### Array Validation
```typescript
// validators/batch.validator.ts
import { z } from "zod"

export const batchUpdateSchema = z.object({
  items: z.array(z.object({
    id: z.string().uuid(),
    name: z.string().min(2),
    email: z.string().email(),
  })).min(1).max(100),
  
  operation: z.enum(["update", "delete"]),
})

export const bulkImportSchema = z.object({
  data: z.array(z.object({
    code: z.string().min(3),
    name: z.string().min(2),
    quantity: z.number().int().positive(),
  })).max(1000),
  
  format: z.enum(["csv", "json"]),
})
```

## 3. Validation Middleware

### Express with Zod
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
        code: err.code,
      }))

      return res.status(422).json({
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
router.post(
  "/users",
  validate(createUserSchema),
  userController.create
)
```

### Express with Joi
```javascript
// middleware/joi-validation.middleware.js
const Joi = require("joi")

function validate(schema) {
  return (req, res, next) => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      stripUnknown: true,
    })

    if (error) {
      const errors = error.details.map((detail) => ({
        field: detail.path.join("."),
        message: detail.message,
        type: detail.type,
      }))

      return res.status(400).json({
        success: false,
        message: "Validation failed",
        errors,
      })
    }

    req.body = value
    next()
  }
}

module.exports = validate
```

### FastAPI with Pydantic
```python
# FastAPI automatically validates Pydantic models
# No explicit middleware needed

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class UserCreate(BaseModel):
    name: str
    email: str


@app.post("/users")
async def create_user(user: UserCreate):
    # Pydantic validation happens automatically
    # If validation fails, FastAPI returns 422 with error details
    return {"user": user}
```

## 4. Error Responses

### Standard Validation Error Response
```typescript
// utils/response.util.ts
import { Response } from "express"

export interface ValidationErrorResponse {
  success: false
  message: string
  errors: Array<{
    field: string
    message: string
    code?: string
  }>
}

export function sendValidationError(
  res: Response,
  errors: Array<{ field: string; message: string; code?: string }>
): Response {
  return res.status(422).json<ValidationErrorResponse>({
    success: false,
    message: "Validation failed",
    errors,
  })
}
```

### Detailed Error Response
```typescript
export interface DetailedErrorResponse {
  success: false
  message: string
  errors: {
    field: string
    message: string
    constraints: Record<string, string>
  }[]
}

export function sendDetailedValidationError(
  res: Response,
  errors: Array<{
    field: string
    message: string
    constraints?: Record<string, string>
  }>
): Response {
  return res.status(422).json<DetailedErrorResponse>({
    success: false,
    message: "Validation failed",
    errors: errors.map((err) => ({
      field: err.field,
      message: err.message,
      constraints: err.constraints || {},
    })),
  })
}
```

## 5. Custom Validators

### Email Domain Validator
```typescript
import { z } from "zod"

const allowedDomains = ["example.com", "company.org"]

export const emailWithDomain = z.string().email().refine(
  (email) => {
    const domain = email.split("@")[1]
    return allowedDomains.includes(domain)
  },
  {
    message: `Email domain must be one of: ${allowedDomains.join(", ")}`,
  }
)
```

### Password Strength Validator
```typescript
import { z } from "zod"

export const strongPassword = z.string().refine(
  (password) => {
    const checks = {
      length: password.length >= 8,
      uppercase: /[A-Z]/.test(password),
      lowercase: /[a-z]/.test(password),
      number: /[0-9]/.test(password),
      special: /[^A-Za-z0-9]/.test(password),
    }

    const passedChecks = Object.values(checks).filter(Boolean).length

    return passedChecks >= 4
  },
  {
    message: "Password must meet at least 4 of 5 strength requirements",
  }
)
```

### Unique Field Validator
```typescript
import { z } from "zod"

export function uniqueFieldValidator(
  checkFn: (value: string) => Promise<boolean>,
  fieldName: string
) {
  return z.string().refine(
    async (value) => {
      const isUnique = await checkFn(value)
      return isUnique
    },
    {
      message: `${fieldName} already exists`,
    }
  )
}

// Usage
export const createUserSchema = z.object({
  email: uniqueFieldValidator(
    async (email) => {
      const existing = await db.user.findUnique({ where: { email } })
      return !existing
    },
    "Email"
  ),
})
```

### Date Range Validator
```typescript
import { z } from "zod"

export const dateRangeSchema = z.object({
  startDate: z.string().datetime(),
  endDate: z.string().datetime(),
}).refine(
  (data) => {
    const start = new Date(data.startDate)
    const end = new Date(data.endDate)
    return start < end
  },
  {
    message: "End date must be after start date",
    path: ["endDate"],
  }
)
```

## 6. Async Validation

### Async Zod Validator
```typescript
import { z } from "zod"

export const emailExistsValidator = z.string().email().refine(
  async (email) => {
    const user = await db.user.findUnique({ where: { email } })
    return !user
  },
  {
    message: "Email already exists",
  }
)

export const registerSchema = z.object({
  email: emailExistsValidator,
  password: z.string().min(8),
})
```

### Async Validation with Express
```typescript
// middleware/async-validation.middleware.ts
import { Request, Response, NextFunction } from "express"
import { AnyZodObject } from "zod"

export async function validateAsync(
  schema: AnyZodObject
) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const result = await schema.safeParseAsync(req.body)

    if (!result.success) {
      const errors = result.error.errors.map((err) => ({
        field: err.path.join("."),
        message: err.message,
      }))

      return res.status(422).json({
        success: false,
        message: "Validation failed",
        errors,
      })
    }

    req.body = result.data
    next()
  }
}
```

### Async Validation with FastAPI
```python
# FastAPI handles async validation automatically
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional


class UserCreate(BaseModel):
    email: str
    username: str
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        # Async validation
        if not is_username_available(v):
            raise HTTPException(status_code=400, detail="Username already taken")
        return v


def is_username_available(username: str) -> bool:
    # Check database
    return True  # or False


@app.post("/users")
async def create_user(user: UserCreate):
    return {"user": user}
```

## 7. File Validation

### File Type Validation
```typescript
import { z } from "zod"

const ALLOWED_FILE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]

export const fileSchema = z.object({
  file: z.custom((file) => {
    if (!file) return true

    const fileObj = file as File
    if (!ALLOWED_FILE_TYPES.includes(fileObj.type)) {
      return false
    }

    return true
  }, {
    message: `File type must be one of: ${ALLOWED_FILE_TYPES.join(", ")}`,
  }),
})
```

### File Size Validation
```typescript
const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB

export const fileSizeSchema = z.object({
  file: z.custom((file) => {
    if (!file) return true

    const fileObj = file as File
    if (fileObj.size > MAX_FILE_SIZE) {
      return false
    }

    return true
  }, {
    message: `File size must be less than ${MAX_FILE_SIZE / 1024 / 1024}MB`,
  }),
})
```

### Image Dimensions Validation
```typescript
export const imageDimensionsSchema = z.object({
  file: z.custom(async (file) => {
    if (!file) return true

    const fileObj = file as File
    const dimensions = await getImageDimensions(fileObj)

    if (dimensions.width < 100 || dimensions.height < 100) {
      return false
    }

    if (dimensions.width > 4000 || dimensions.height > 4000) {
      return false
    }

    return true
  }, {
    message: "Image must be between 100x100 and 4000x4000 pixels",
  }),
})

async function getImageDimensions(file: File): Promise<{ width: number; height: number }> {
  return new Promise((resolve) => {
    const img = new Image()
    img.onload = () => {
      resolve({ width: img.width, height: img.height })
    }
    img.src = URL.createObjectURL(file)
  })
}
```

## 8. Query Parameter Validation

### Query Schema
```typescript
// validators/pagination.validator.ts
import { z } from "zod"

export const paginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  limit: z.coerce.number().int().positive().max(100).default(10),
  sort: z.enum(["name", "created_at", "updated_at"]).default("created_at"),
  order: z.enum(["asc", "desc"]).default("desc"),
})

export type PaginationQuery = z.infer<typeof paginationSchema>
```

### Query Validation Middleware
```typescript
// middleware/query-validation.middleware.ts
import { Request, Response, NextFunction } from "express"
import { AnyZodObject } from "zod"

export function validateQuery(schema: AnyZodObject) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.query)

    if (!result.success) {
      const errors = result.error.errors.map((err) => ({
        field: err.path.join("."),
        message: err.message,
      }))

      return res.status(400).json({
        success: false,
        message: "Invalid query parameters",
        errors,
      })
    }

    req.query = result.data
    next()
  }
}

// Usage
router.get(
  "/users",
  validateQuery(paginationSchema),
  userController.getAll
)
```

### Filter Query Validation
```typescript
export const filterSchema = z.object({
  status: z.enum(["active", "inactive", "all"]).default("all"),
  role: z.enum(["user", "admin"]).optional(),
  search: z.string().max(100).optional(),
  dateFrom: z.string().datetime().optional(),
  dateTo: z.string().datetime().optional(),
}).refine(
  (data) => {
    if (data.dateFrom && data.dateTo) {
      return new Date(data.dateFrom) < new Date(data.dateTo)
    }
    return true
  },
  {
    message: "dateFrom must be before dateTo",
    path: ["dateTo"],
  }
)
```

## 9. Path Parameter Validation

### UUID Validation
```typescript
export const uuidSchema = z.object({
  id: z.string().uuid("Invalid UUID format"),
})
```

### Integer ID Validation
```typescript
export const idSchema = z.object({
  id: z.coerce.number().int().positive("Invalid ID"),
})
```

### Slug Validation
```typescript
export const slugSchema = z.object({
  slug: z.string()
    .regex(/^[a-z0-9-]+$/, "Invalid slug format")
    .min(3, "Slug must be at least 3 characters")
    .max(100, "Slug must be at most 100 characters"),
})
```

### Path Parameter Middleware
```typescript
// middleware/param-validation.middleware.ts
import { Request, Response, NextFunction } from "express"
import { AnyZodObject } from "zod"

export function validateParams(schema: AnyZodObject) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.params)

    if (!result.success) {
      const errors = result.error.errors.map((err) => ({
        field: err.path.join("."),
        message: err.message,
      }))

      return res.status(400).json({
        success: false,
        message: "Invalid path parameters",
        errors,
      })
    }

    req.params = result.data
    next()
  }
}

// Usage
router.get(
  "/users/:id",
  validateParams(uuidSchema),
  userController.getById
)
```

## 10. Best Practices

### 1. Validate at the Edge
```typescript
// Good: Validate as early as possible
router.post(
  "/users",
  validate(createUserSchema),
  authMiddleware,
  userController.create
)

// Bad: Validate inside controller
router.post("/users", userController.create)
// Controller has to handle validation
```

### 2. Use Type Inference
```typescript
// Good: Infer types from schemas
export type CreateUserDto = z.infer<typeof createUserSchema>

// Bad: Duplicate type definitions
interface CreateUserDto {
  name: string
  email: string
  password: string
}
```

### 3. Provide Clear Error Messages
```typescript
// Good: Specific error messages
z.string().min(8, "Password must be at least 8 characters")

// Bad: Generic error messages
z.string().min(8, "Invalid password")
```

### 4. Validate on Both Client and Server
```typescript
// Client-side validation (for UX)
export const createUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
  password: z.string().min(8),
})

// Server-side validation (for security)
router.post(
  "/users",
  validate(createUserSchema),
  userController.create
)
```

### 5. Use Consistent Error Format
```typescript
// Standardized error response
{
  "success": false,
  "message": "Validation failed",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

### 6. Sanitize Input
```typescript
import { z } from "zod"

export const sanitizeString = z.string().transform((val) => {
  return val.trim().replace(/\s+/g, " ")
})

export const createUserSchema = z.object({
  name: sanitizeString.min(2),
  email: z.string().email().toLowerCase().trim(),
  password: z.string().min(8),
})
```

### 7. Validate All Input Sources
```typescript
// Validate body
router.post("/users", validateBody(createUserSchema), handler)

// Validate query
router.get("/users", validateQuery(paginationSchema), handler)

// Validate params
router.get("/users/:id", validateParams(uuidSchema), handler)

// Validate headers
router.get("/users", validateHeaders(authHeaderSchema), handler)
```

### 8. Use Schema Composition
```typescript
// Base schema
const baseUserSchema = z.object({
  name: z.string().min(2),
  email: z.string().email(),
})

// Extend for create
export const createUserSchema = baseUserSchema.extend({
  password: z.string().min(8),
})

// Extend for update
export const updateUserSchema = baseUserSchema.partial()
```
