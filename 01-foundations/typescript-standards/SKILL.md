# TypeScript Coding Standards

## Overview
มาตรฐานการเขียน TypeScript สำหรับทุกโปรเจค รองรับ Node.js และ Next.js

## Core Principles
- Type Safety First: หลีกเลี่ยง `any` ทุกกรณี
- Explicit over Implicit: ระบุ type ชัดเจน
- Functional Programming: ใช้ immutable patterns
- Error Handling: ใช้ Result type หรือ throw Error ที่มีโครงสร้าง

## TypeScript Configuration

### tsconfig.json (Strict Mode)
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "commonjs",
    "moduleResolution": "node",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "outDir": "./dist",
    "rootDir": "./src"
  }
}
```

## Naming Conventions

### Variables & Functions
```typescript
// ❌ Bad
const UserData = {...};
function Get_user() {}

// ✅ Good
const userData = {...};
function getUser() {}
```

### Types & Interfaces
```typescript
// ❌ Bad
interface user {}
type requestData = {};

// ✅ Good
interface User {}
type RequestData = {};
```

### Constants
```typescript
// ❌ Bad
const apikey = "...";

// ✅ Good
const API_KEY = "...";
const MAX_RETRY_ATTEMPTS = 3;
```

### File Names
```typescript
// ❌ Bad
UserController.ts
user-service.ts

// ✅ Good (choose one style and be consistent)
// For classes/components:
UserController.ts
UserService.ts

// For utilities:
user.utils.ts
date.helpers.ts
```

## Type Definitions

### Basic Types
```typescript
// ❌ Avoid any
function processData(data: any) { }

// ✅ Use specific types
function processData(data: string | number) { }

// ✅ Or generic types
function processData<T>(data: T): T { }
```

### Interface vs Type
```typescript
// Use Interface for objects that can be extended
interface User {
  id: string;
  name: string;
  email: string;
}

interface AdminUser extends User {
  role: "admin";
  permissions: string[];
}

// Use Type for unions, intersections, and primitives
type Status = "pending" | "approved" | "rejected";
type ID = string | number;
type ApiResponse<T> = {
  success: boolean;
  data?: T;
  error?: string;
};
```

### Function Types
```typescript
// ❌ Bad
const handleClick = (e: any) => { };

// ✅ Good
type ClickHandler = (event: MouseEvent) => void;
const handleClick: ClickHandler = (event) => { };

// ✅ For async functions
type AsyncProcessor<T, R> = (input: T) => Promise<R>;
```

## Error Handling

### Custom Error Classes
```typescript
// Base error class
export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public isOperational: boolean = true
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

// Specific error types
export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, "VALIDATION_ERROR", 400);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, "NOT_FOUND", 404);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message: string = "Unauthorized") {
    super(message, "UNAUTHORIZED", 401);
  }
}
```

### Try-Catch Patterns
```typescript
// ❌ Bad
try {
  const user = await getUser(id);
  return user;
} catch (error) {
  console.log(error);
}

// ✅ Good
try {
  const user = await getUser(id);
  return user;
} catch (error) {
  if (error instanceof NotFoundError) {
    throw error; // Re-throw operational errors
  }
  // Log and wrap unexpected errors
  logger.error("Unexpected error in getUser", { error, userId: id });
  throw new AppError("Failed to fetch user", "INTERNAL_ERROR");
}
```

### Result Type Pattern (Optional)
```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

async function safeGetUser(id: string): Promise<Result<User>> {
  try {
    const user = await db.user.findUnique({ where: { id } });
    if (!user) {
      return { success: false, error: new NotFoundError("User") };
    }
    return { success: true, data: user };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}

// Usage
const result = await safeGetUser("123");
if (result.success) {
  console.log(result.data.name);
} else {
  console.error(result.error.message);
}
```

## API Response Patterns

### Standard Response Type
```typescript
interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
  meta?: {
    timestamp: string;
    requestId?: string;
  };
}

// Helper function
function createSuccessResponse<T>(data: T): ApiResponse<T> {
  return {
    success: true,
    data,
    meta: {
      timestamp: new Date().toISOString(),
    },
  };
}

function createErrorResponse(
  code: string,
  message: string,
  details?: unknown
): ApiResponse {
  return {
    success: false,
    error: { code, message, details },
    meta: {
      timestamp: new Date().toISOString(),
    },
  };
}
```

## Async/Await Best Practices
```typescript
// ❌ Bad - unhandled promise
async function processUsers() {
  users.forEach(async (user) => {
    await processUser(user);
  });
}

// ✅ Good - proper promise handling
async function processUsers() {
  await Promise.all(users.map((user) => processUser(user)));
}

// ✅ Good - sequential processing with for...of
async function processUsers() {
  for (const user of users) {
    await processUser(user);
  }
}
```

## Utility Types
```typescript
// Deep Partial
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

// Pick Required Fields
type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Exclude null and undefined
type NonNullableFields<T> = {
  [P in keyof T]: NonNullable<T[P]>;
};

// Usage
interface User {
  id: string;
  name: string;
  email?: string;
  profile?: {
    avatar?: string;
    bio?: string;
  };
}

type UserUpdate = DeepPartial<User>;
type UserWithEmail = RequiredFields<User, "email">;
```

## Dependency Injection Pattern
```typescript
// ❌ Bad - tight coupling
class UserService {
  private db = new Database();
  
  async getUser(id: string) {
    return this.db.users.findOne(id);
  }
}

// ✅ Good - dependency injection
interface IDatabase {
  users: {
    findOne(id: string): Promise<User | null>;
  };
}

class UserService {
  constructor(private db: IDatabase) {}
  
  async getUser(id: string): Promise<User | null> {
    return this.db.users.findOne(id);
  }
}

// Usage
const db = new Database();
const userService = new UserService(db);
```

## Testing Types
```typescript
// Mock types for testing
type MockFunction<T extends (...args: any[]) => any> = jest.Mock
  ReturnType<T>,
  Parameters<T>
>;

// Type-safe test data
type TestUser = Required<User>;

const createTestUser = (overrides?: Partial<User>): TestUser => ({
  id: "test-id",
  name: "Test User",
  email: "test@example.com",
  profile: {
    avatar: "https://example.com/avatar.jpg",
    bio: "Test bio",
  },
  ...overrides,
});
```

## Environment Variables
```typescript
// ❌ Bad
const apiKey = process.env.API_KEY;

// ✅ Good - with validation
import { z } from "zod";

const envSchema = z.object({
  NODE_ENV: z.enum(["development", "production", "test"]),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
  PORT: z.string().regex(/^\d+$/).transform(Number).default("3000"),
});

export const env = envSchema.parse(process.env);

// Usage with full type safety
console.log(env.PORT); // number
console.log(env.NODE_ENV); // "development" | "production" | "test"
```

## Code Organization

### File Structure
```
src/
├── types/
│   ├── index.ts          # Export all types
│   ├── user.types.ts
│   └── api.types.ts
├── utils/
│   ├── errors.ts
│   ├── validators.ts
│   └── helpers.ts
├── services/
│   └── user.service.ts
└── controllers/
    └── user.controller.ts
```

### Import Order
```typescript
// 1. External dependencies
import express from "express";
import { z } from "zod";

// 2. Internal modules
import { UserService } from "@/services/user.service";
import { validateRequest } from "@/middleware/validation";

// 3. Types
import type { User, CreateUserDto } from "@/types";

// 4. Relative imports
import { logger } from "./logger";
```

## ESLint Configuration
```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": ["error", { 
      "argsIgnorePattern": "^_" 
    }],
    "@typescript-eslint/naming-convention": [
      "error",
      {
        "selector": "interface",
        "format": ["PascalCase"],
        "custom": {
          "regex": "^I[A-Z]",
          "match": false
        }
      }
    ]
  }
}
```

## Common Patterns Checklist

When writing TypeScript code, ensure:
- [ ] No `any` types (use `unknown` if truly dynamic)
- [ ] All functions have explicit return types
- [ ] Error handling is consistent and type-safe
- [ ] Environment variables are validated
- [ ] API responses follow standard structure
- [ ] Async operations are properly awaited
- [ ] Types are exported from dedicated type files
- [ ] Naming conventions are followed
- [ ] Dependencies are injected, not hard-coded
- [ ] Unit tests cover type assertions