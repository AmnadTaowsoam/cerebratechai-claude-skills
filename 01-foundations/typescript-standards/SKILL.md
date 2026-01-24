### **06: TypeScript Coding Standards**

> 
> **Current Level:** Expert (Enterprise Scale) 
> 
> 
> **Domain:** Foundations / TypeScript Development 
> 

---

### **1. Executive Summary & Strategic Necessity**

* **Context:** ในโลกปี 2025-2026 การพัฒนาซอฟต์แวร์ด้วย TypeScript มีความซับซ้อนเพิ่มขึ้นอย่างมาก การใช้ TypeScript Standards ที่เป็นมาตรฐานช่วยให้ทีมพัฒนาสามารถเขียนโค้ดที่มี Type Safety สูง ลด Bug และเพิ่มประสิทธิภาพในการพัฒนา
* **Business Impact:** การใช้ TypeScript Standards ที่มีประสิทธิภาพช่วย:
  - เพิ่มความโค้ดที่สะอดความและเป็นมาตรฐาน
  - ลดความ Bug ที่เกิดขึ้นใน Production
  - เพิ่มประสิทธิภาพในการพัฒนา
  - ลดเวลาในการ Code Review
  - เพิ่มความสามารถในการทำงานร่วมกัน
  - ลด Technical Debt ที่สะสมในระยะว
  - เพิ่มความโปร่งใสในการพัฒนา
* **Product Thinking:** ทักษะนี้ช่วยแก้ปัญหา (Pain Point) ให้กับ:
  - ทีมพัฒนาที่ต้องการ TypeScript Standards ที่เป็นระบบ
  - ผู้ทำงานผิดพลาดที่ต้องการ Standards ที่เข้าใจ
  - ทีมพัฒนาที่ต้องการ Type Safety ที่สูง
  - ลูกค้าที่ต้องการความเสถียรของระบบ
  - ทีม Support ที่ต้องการ Debug ของ Code

### **2. Technical Deep Dive (The "How-to")**

* **Core Logic:** TypeScript Standards ประกอบด้วย:
  - **TypeScript Configuration:** การตั้งค่า TypeScript (tsconfig.json, Strict Mode, Key Options Explained)
  - **Naming Conventions:** การตั้งชื่อที่เป็นมาตรฐาน (Variables & Functions, Types & Interfaces & Classes, Constants, Boolean Variables, Event Handlers, File Naming)
  - **Type Definitions:** การกำหนด Types (Basic Types, Interface vs Type, Generics Best Practices, Discriminated Unions, Type Guards)
  - **Error Handling Patterns:** การจัดการ Error ที่เป็นระบบ (Custom Error Classes Hierarchy, Try-Catch Patterns, Result Type Pattern, Error Boundary Pattern)
  - **API Response Patterns:** รูปแบบการตอบกลับ API (Standard Response Types, Response Helper Functions, Express Integration)
  - **Async/Await Best Practices:** การใช้ Async/Await อย่างถูกต้อง (Proper Promise Handling, Promise.allSettled for Partial Failures, Controlled Concurrency, Timeout Handling, Retry Pattern)
  - **Utility Types:** Types สำหรับการใช้งาน (Deep Partial, Required Fields, Nullable and NonNullable, Extract and Filter Types, Function Types, Builder Pattern Types, Path Types)
  - **Dependency Injection Patterns:** รูปแบบ Dependency Injection (Constructor Injection, Factory Pattern with DI, Functional Dependency Injection, Testing with DI)
  - **Environment Variables Validation:** การตรวจสอบ Environment Variables (Zod Schema Validation, Environment-Specific Configs)
  - **Import Organization:** การจัดระเบบ Imports (Import Order Convention, Type-Only Imports, Barrel Files)

* **Architecture Diagram Requirements:** แผนผังสถาปัตยกรรมที่ต้องมี:
  - **Type System Architecture Diagram:** แผนผังแสดง Type System ของ TypeScript
  - **Error Handling Flow Diagram:** แผนผังแสดงกระบวนการ Error Handling
  - **API Response Flow Diagram:** แผนผังแสดงกระบวนการ API Response
  - **Async Execution Flow Diagram:** แผนผังแสดงกระบวนการ Async Execution
  - **Dependency Injection Diagram:** แผนผังแสดง Dependency Injection Pattern

* **Implementation Workflow:**
  1. **Setup TypeScript Configuration:** ตั้งค่า TypeScript Configuration สำหรับโปรเจกต์
  2. **Define Naming Conventions:** กำหนด Naming Conventions สำหรับโปรเจกต์
  3. **Create Type Definitions:** สร้าง Type Definitions สำหรับโปรเจกต์
  4. **Implement Error Handling:** จัดการ Error Handling ที่เป็นระบบ
  5. **Setup API Response Patterns:** ตั้งค่า API Response Patterns
  6. **Implement Async/Await Patterns:** จัดการ Async/Await Patterns
  7. **Configure Environment Variables:** ตั้งค่า Environment Variables Validation

### **3. Tooling & Tech Stack**

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้:
  - **TypeScript Compiler:** TypeScript Compiler, tsc
  - **Linting:** ESLint, TypeScript ESLint
  - **Formatting:** Prettier
  - **Type Checking:** TypeScript Compiler, tsc
  - **Testing:** Jest, Vit, Mocha, Chai
  - **Build Tools:** Vite, Webpack, esbuild
  - **CI/CD Platforms:** GitHub Actions, GitLab CI, Azure Pipelines, Jenkins
  - **Package Managers:** npm, pnpm, yarn

* **Configuration Essentials:** ส่วนประกอบสำคัญในการตั้งค่า:
  - **tsconfig.json:** การตั้งค่า TypeScript Compiler Options
  - **ESLint Configuration:** การตั้งค่า ESLint สำหรับ TypeScript
  - **Prettier Configuration:** การตั้งค่า Prettier สำหรับ Formatting
  - **Package.json Scripts:** การตั้งค่า Scripts สำหรับ Build, Test, Lint
  - **GitHub Actions Workflow:** การตั้งค่า CI/CD Pipeline

### **4. Standards, Compliance & Security**

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  - **TypeScript Specification:** TypeScript Language Specification
  - **ECMAScript Standards:** ECMAScript Standards
  - **Type System Standards:** Type System Standards
  - **Code Quality Standards:** Code Quality Standards

* **Security Protocol:** กลไกการป้องกัน:
  - **Input Validation:** การตรวจสอบ Input ด้วย TypeScript Types
  - **Environment Variables Validation:** การตรวจสอบ Environment Variables ด้วย Zod
  - **Type Safety:** การใช้ Type Safety สำหรับการป้องกัน
  - **Error Handling:** การจัดการ Error ที่ปลอดภัย
  - **API Security:** การใช้ API Security ที่เป็นมาตรฐาน

* **Explainability:** ความสามารถในการอธิบาย:
  - **Type Annotations Documentation:** การบันทึก Type Annotations ที่ชัดเจน
  - **Error Messages Documentation:** การบันทึก Error Messages ที่ชัดเจน
  - **API Documentation:** การบันทึก API Documentation ที่ชัดเจน
  - **Code Comments:** การบันทึก Code Comments ที่ชัดเจน

### **5. Unit Economics & Performance Metrics (KPIs)**

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย (COGS):
  ```
  Total Cost = (Development Time × Hourly Rate) + 
               (Code Review Time × Hourly Rate) + 
               (Bug Fix Time × Hourly Rate) + 
               (Tooling Cost)
  
  ROI = (Productivity Gain - Total Cost) / Total Cost × 100%
  
  Productivity Gain = (Time Saved on Bug Fixes) + 
                      (Time Saved on Code Reviews) + 
                      (Time Saved on Onboarding)
  ```

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  - **Type Coverage:** % ของ Code ที่มี Type Annotations (Target: > 95%)
  - **Code Quality Score:** คะแนนคุณภาพของโค้ด (Target: > A)
  - **Bug Detection Rate:** % ของ Bugs ที่ค้นพบก่อน Production (Target: > 85%)
  - **Code Review Time:** เวลาเฉลี่ยในการ Code Review (Target: < 30 min)
  - **Team Productivity:** จำนวน Commits ต่อวัน (Target: > 10/day)

### **6. Strategic Recommendations (CTO Insights)**

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน:
  1. **Phase 1 (Months 1-2):** สร้าง TypeScript Standards และ Guidelines, ฝึกอบรมทีม
  2. **Phase 2 (Months 3-4):** ตั้งค่า TypeScript Configuration และ ESLint
  3. **Phase 3 (Months 5-6):** ฝึกอบรมทีมเกี่ยวกับ TypeScript Standards และ Best Practices
  4. **Phase 4 (Year 2+):** ขยายไปยังทุกทีม, สร้าง Culture ของ TypeScript Best Practices

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาด:
  - **Using `any` Type:** หลีกเลี่ยงการใช้ `any` Type
  - **Implicit Any:** หลีกเลี่ยงการใช้ Implicit Any
  - **Skipping Type Annotations:** หลีกเลี่ยงการไม่ใช้ Type Annotations
  - **Not Using Strict Mode:** หลีกเลี่ยงการไม่ใช้ Strict Mode
  - **Poor Error Handling:** หลีกเลี่ยงการจัดการ Error ที่ไม่ดี
  - **Inconsistent Naming:** หลีกเลี่ยงการใช้ Naming ที่ไม่สม่ำเสมอ
  - **Not Testing Types:** หลีกเลี่ยงการไม่ทดสอบ Types

---

## Overview

TypeScript coding standards for Backend and Frontend projects supporting Node.js and Next.js.

## Core Principles

- **Type Safety First**: หลีกเลี่ยง `any` ทุกกรณี
- **Explicit over Implicit**: ระบุ type ชัดเจน
- **Functional Programming**: ใช้ immutable patterns
- **Error Handling**: ใช้ Result type หรือ throw Error ที่มีโครงสร้าง

## TypeScript Configuration

### tsconfig.json (Strict Mode - Recommended)

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["ES2022"],
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "outDir": "./dist",
    "rootDir": "./src",
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.test.ts"]
}
```

### tsconfig.json for Next.js

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "ES2022"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noUncheckedIndexedAccess": true,
    "plugins": [{ "name": "next" }],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

### Key Strict Options Explained

```typescript
// noUncheckedIndexedAccess - Arrays return T | undefined
const items = ["a", "b", "c"];
const item = items[0]; // Type: string | undefined

// ❌ Bad - assumes item exists
console.log(item.toUpperCase()); // Error!

// ✅ Good - handle undefined
if (item) {
  console.log(item.toUpperCase());
}

// exactOptionalPropertyTypes - Distinguishes undefined from missing
interface Config {
  timeout?: number;
}

// ❌ Bad
const config: Config = { timeout: undefined }; // Error with exactOptionalPropertyTypes

// ✅ Good
const config1: Config = {}; // OK - property is absent
const config2: Config = { timeout: 5000 }; // OK - property has value
```

## Naming Conventions

### Variables & Functions (camelCase)

```typescript
// ❌ Bad
const UserData = { name: "John" };
const user_name = "John";
function Get_user() {}
function fetchuserdata() {}

// ✅ Good
const userData = { name: "John" };
const userName = "John";
function getUser() {}
function fetchUserData() {}
```

### Types, Interfaces, Classes & Enums (PascalCase)

```typescript
// ❌ Bad
interface user {}
type requestData = {};
class userService {}
enum status {}

// ✅ Good
interface User {}
type RequestData = {};
class UserService {}
enum Status {}

// Avoid "I" prefix for interfaces (Hungarian notation)
// ❌ Bad
interface IUser {}
interface IUserService {}

// ✅ Good
interface User {}
interface UserService {}
```

### Constants (SCREAMING_SNAKE_CASE for true constants)

```typescript
// ❌ Bad
const apikey = "sk-xxx";
const MaxRetryAttempts = 3;

// ✅ Good - true constants (values known at compile time)
const API_KEY = "sk-xxx";
const MAX_RETRY_ATTEMPTS = 3;
const HTTP_STATUS_OK = 200;
const DEFAULT_TIMEOUT_MS = 30000;

// ✅ Good - runtime constants use camelCase
const config = loadConfig();
const startTime = Date.now();
```

### Boolean Variables (use is/has/can/should prefix)

```typescript
// ❌ Bad
const loading = true;
const admin = false;
const visible = true;

// ✅ Good
const isLoading = true;
const isAdmin = false;
const isVisible = true;
const hasPermission = true;
const canEdit = false;
const shouldRefresh = true;
```

### Event Handlers (use handle/on prefix)

```typescript
// ❌ Bad
const clickButton = () => {};
const submitForm = () => {};

// ✅ Good
const handleButtonClick = () => {};
const handleFormSubmit = () => {};
const onUserSelect = () => {};
```

### File Naming Conventions

```typescript
// Classes and Components - PascalCase
UserController.ts
UserService.ts
UserProfile.tsx

// Utilities, helpers, hooks - camelCase or kebab-case
userUtils.ts
dateHelpers.ts
useAuth.ts

// Types - .types.ts suffix
user.types.ts
api.types.ts

// Tests - .test.ts or .spec.ts suffix
UserService.test.ts
userUtils.spec.ts

// Constants/Config
constants.ts
config.ts
```

## Type Definitions

### Basic Types - Avoid `any`

```typescript
// ❌ Bad - any defeats TypeScript's purpose
function processData(data: any): any {
  return data.value;
}

// ❌ Bad - implicit any
function processData(data) {
  return data.value;
}

// ✅ Good - specific types
function processData(data: { value: string }): string {
  return data.value;
}

// ✅ Good - use unknown for truly dynamic data
function processUnknownData(data: unknown): string {
  if (typeof data === "object" && data !== null && "value" in data) {
    return String((data as { value: unknown }).value);
  }
  throw new Error("Invalid data format");
}

// ✅ Good - generic types
function processData<T extends { value: string }>(data: T): string {
  return data.value;
}
```

### Interface vs Type - When to Use Each

```typescript
// USE INTERFACE for:
// 1. Object shapes that may be extended
interface User {
  id: string;
  name: string;
  email: string;
}

interface AdminUser extends User {
  role: "admin";
  permissions: string[];
}

// 2. Class implementations
interface Repository<T> {
  findById(id: string): Promise<T | null>;
  findAll(): Promise<T[]>;
  create(data: Omit<T, "id">): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

class UserRepository implements Repository<User> {
  // Implementation
}

// 3. Declaration merging (module augmentation)
declare module "express" {
  interface Request {
    user?: User;
    requestId: string;
  }
}

// USE TYPE for:
// 1. Union types
type Status = "pending" | "approved" | "rejected";
type ID = string | number;

// 2. Intersection types
type CreateUserDto = Pick<User, "name" | "email"> & {
  password: string;
};

// 3. Mapped types
type Readonly<T> = { readonly [K in keyof T]: T[K] };

// 4. Conditional types
type NonNullable<T> = T extends null | undefined ? never : T;

// 5. Function types
type AsyncFunction<T, R> = (input: T) => Promise<R>;
type EventHandler<E> = (event: E) => void;

// 6. Tuple types
type Coordinate = [number, number];
type RGB = [red: number, green: number, blue: number];

// 7. Template literal types
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type Endpoint = `/${string}`;
type Route = `${HttpMethod} ${Endpoint}`;
```

### Generics Best Practices

```typescript
// ❌ Bad - single letter without constraint is unclear
function process<T>(data: T): T {
  return data;
}

// ✅ Good - descriptive names with constraints
function processEntity<TEntity extends { id: string }>(
  entity: TEntity
): TEntity {
  return entity;
}

// ✅ Good - multiple generics with clear purpose
function transformData<TInput, TOutput>(
  data: TInput,
  transformer: (input: TInput) => TOutput
): TOutput {
  return transformer(data);
}

// ✅ Good - default generic types
interface ApiResponse<TData = unknown, TError = Error> {
  success: boolean;
  data?: TData;
  error?: TError;
}

// ✅ Good - generic constraints with keyof
function getProperty<TObj, TKey extends keyof TObj>(
  obj: TObj,
  key: TKey
): TObj[TKey] {
  return obj[key];
}

// ✅ Good - generic factory pattern
function createRepository<T extends { id: string }>( ): Repository<T> {
  return {
    async findById(id: string): Promise<T | null> {
      // Implementation
    },
    // ...
  };
}
```

### Discriminated Unions (Tagged Unions)

```typescript
// ✅ Excellent for state management and event handling
type LoadingState = { status: "loading" };
type SuccessState<T> = { status: "success"; data: T };
type ErrorState = { status: "error"; error: Error };

type AsyncState<T> = LoadingState | SuccessState<T> | ErrorState;

function handleState<T>(state: AsyncState<T>): void {
  switch (state.status) {
    case "loading":
      console.log("Loading...");
      break;
    case "success":
      console.log("Data:", state.data); // TypeScript knows data exists
      break;
    case "error":
      console.log("Error:", state.error.message); // TypeScript knows error exists
      break;
  }
}

// ✅ API Actions
type UserAction =
  | { type: "CREATE"; payload: CreateUserDto }
  | { type: "UPDATE"; payload: { id: string; data: Partial<User> } }
  | { type: "DELETE"; payload: { id: string } };

function handleUserAction(action: UserAction): void {
  switch (action.type) {
    case "CREATE":
      // action.payload is CreateUserDto
      break;
    case "UPDATE":
      // action.payload is { id: string; data: Partial<User> }
      break;
    case "DELETE":
      // action.payload is { id: string }
      break;
  }
}
```

### Type Guards

```typescript
// Custom type guard functions
function isUser(value: unknown): value is User {
  return (
    typeof value === "object" &&
    value !== null &&
    "id" in value &&
    "name" in value &&
    "email" in value &&
    typeof (value as User).id === "string" &&
    typeof (value as User).name === "string" &&
    typeof (value as User).email === "string"
  );
}

// Usage
function processValue(value: unknown): void {
  if (isUser(value)) {
    console.log(value.email); // TypeScript knows this is a User
  }
}

// Type guard with discriminated union
function isSuccessResponse<T>(
  response: ApiResponse<T>
): response is ApiResponse<T> & { success: true; data: T } {
  return response.success === true && response.data !== undefined;
}

// Assertion function
function assertIsUser(value: unknown): asserts value is User {
  if (!isUser(value)) {
    throw new Error("Value is not a User");
  }
}

// Usage
function processUnknown(value: unknown): void {
  assertIsUser(value);
  // After assertion, TypeScript knows value is User
  console.log(value.email);
}
```

## Error Handling Patterns

### Custom Error Classes Hierarchy

```typescript
// Base application error
export abstract class AppError extends Error {
  abstract readonly statusCode: number;
  abstract readonly code: string;
  readonly isOperational: boolean = true;
  readonly timestamp: Date = new Date();

  constructor(
    message: string,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON(): Record<string, unknown> {
    return {
      name: this.name,
      message: this.message,
      code: this.code,
      statusCode: this.statusCode,
      timestamp: this.timestamp.toISOString(),
      context: this.context,
    };
  }
}

// Client Errors (4xx)
export class BadRequestError extends AppError {
  readonly statusCode = 400;
  readonly code = "BAD_REQUEST";
}

export class ValidationError extends AppError {
  readonly statusCode = 400;
  readonly code = "VALIDATION_ERROR";

  constructor(
    message: string,
    public readonly errors: Array<{ field: string; message: string }>
  ) {
    super(message, { errors });
  }
}

export class UnauthorizedError extends AppError {
  readonly statusCode = 401;
  readonly code = "UNAUTHORIZED";

  constructor(message: string = "Authentication required") {
    super(message);
  }
}

export class ForbiddenError extends AppError {
  readonly statusCode = 403;
  readonly code = "FORBIDDEN";

  constructor(message: string = "Access denied") {
    super(message);
  }
}

export class NotFoundError extends AppError {
  readonly statusCode = 404;
  readonly code = "NOT_FOUND";

  constructor(resource: string, identifier?: string) {
    super(
      identifier
        ? `${resource} with id '${identifier}' not found`
        : `${resource} not found`,
      { resource, identifier }
    );
  }
}

export class ConflictError extends AppError {
  readonly statusCode = 409;
  readonly code = "CONFLICT";

  constructor(
    message: string,
    resource?: string
  ) {
    super(message, { resource });
  }
}

// Server Errors (5xx)
export class InternalError extends AppError {
  readonly statusCode = 500;
  readonly code = "INTERNAL_ERROR";
  readonly isOperational = false;

  constructor(message: string = "An unexpected error occurred") {
    super(message);
  }
}

export class ServiceUnavailableError extends AppError {
  readonly statusCode = 503;
  readonly code = "SERVICE_UNAVAILABLE";

  constructor(service: string) {
    super(`${service} is currently unavailable`, { service });
  }
}
```

### Try-Catch Patterns

```typescript
// ❌ Bad - swallowing errors
async function getUser(id: string): Promise<User | null> {
  try {
    return await db.user.findUnique({ where: { id } });
  } catch (error) {
    console.log(error); // Swallowed!
    return null;
  }
}

// ❌ Bad - catching and re-throwing without context
async function getUser(id: string): Promise<User> {
  try {
    const user = await db.user.findUnique({ where: { id } });
    if (!user) throw new Error("User not found");
    return user;
  } catch (error) {
    throw error; // No additional context
  }
}

// ✅ Good - proper error handling with context
async function getUser(id: string): Promise<User> {
  try {
    const user = await db.user.findUnique({ where: { id } });

    if (!user) {
      throw new NotFoundError("User", id);
    }

    return user;
  } catch (error) {
    // Re-throw known operational errors
    if (error instanceof AppError) {
      throw error;
    }

    // Log and wrap unexpected errors
    logger.error("Unexpected error fetching user", {
      error,
      userId: id,
      stack: error instanceof Error ? error.stack : undefined,
    });

    throw new InternalError("Failed to fetch user");
  }
}

// ✅ Good - error handling with cleanup
async function processFile(filePath: string): Promise<void> {
  let fileHandle: FileHandle | null = null;

  try {
    fileHandle = await fs.open(filePath, "r");
    const content = await fileHandle.readFile("utf-8");
    await processContent(content);
  } catch (error) {
    if (error instanceof AppError) throw error;

    logger.error("File processing failed", { filePath, error });
    throw new InternalError(`Failed to process file: ${filePath}`);
  } finally {
    // Always cleanup
    await fileHandle?.close();
  }
}
```

### Result Type Pattern (Functional Error Handling)

```typescript
// Result type definition
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

// Helper functions
const Ok = <T>(value: T): Result<T, never> => ({ ok: true, value });
const Err = <E>(error: E): Result<never, E> => ({ ok: false, error });

// Type guard
function isOk<T, E>(result: Result<T, E>): result is { ok: true; value: T } {
  return result.ok;
}

function isErr<T, E>(result: Result<T, E>): result is { ok: false; error: E } {
  return !result.ok;
}

// Usage example
async function safeGetUser(id: string): Promise<Result<User, AppError>> {
  try {
    const user = await db.user.findUnique({ where: { id } });

    if (!user) {
      return Err(new NotFoundError("User", id));
    }

    return Ok(user);
  } catch (error) {
    logger.error("Database error", { error, userId: id });
    return Err(new InternalError("Database query failed"));
  }
}

// Consuming Result type
async function handleGetUser(id: string): Promise<void> {
  const result = await safeGetUser(id);

  if (isOk(result)) {
    console.log(`Found user: ${result.value.name}`);
  } else {
    console.error(`Error: ${result.error.message}`);
  }
}

// Chaining Results
function map<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => U
): Result<U, E> {
  return isOk(result) ? Ok(fn(result.value)) : result;
}

function flatMap<T, U, E>(
  result: Result<T, E>,
  fn: (value: T) => Result<U, E>
): Result<U, E> {
  return isOk(result) ? fn(result.value) : result;
}

// Usage
const userResult = await safeGetUser("123");
const emailResult = map(userResult, (user) => user.email);
```

### Error Boundary Pattern (for Services)

```typescript
type ErrorHandler = (error: unknown) => AppError;

function withErrorBoundary<TArgs extends unknown[], TReturn>(
  fn: (...args: TArgs) => Promise<TReturn>,
  errorHandler: ErrorHandler
): (...args: TArgs) => Promise<TReturn> {
  return async (...args: TArgs): Promise<TReturn> => {
    try {
      return await fn(...args);
    } catch (error) {
      if (error instanceof AppError) {
        throw error;
      }
      throw errorHandler(error);
    }
  };
}

// Usage
const safeCreateUser = withErrorBoundary(
  async (data: CreateUserDto): Promise<User> => {
    return await db.user.create({ data });
  },
  (error) => {
    if (isPrismaUniqueConstraintError(error)) {
      return new ConflictError("User with this email already exists");
    }
    return new InternalError("Failed to create user");
  }
);
```

## API Response Patterns

### Standard Response Types

```typescript
// Base response interface
interface BaseResponse {
  success: boolean;
  meta: {
    timestamp: string;
    requestId: string;
    version: string;
  };
}

// Success response
interface SuccessResponse<T> extends BaseResponse {
  success: true;
  data: T;
}

// Error response
interface ErrorResponse extends BaseResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: unknown;
    stack?: string; // Only in development
  };
}

// Paginated response
interface PaginatedData<T> {
  items: T[];
  pagination: {
    page: number;
    pageSize: number;
    totalItems: number;
    totalPages: number;
    hasNextPage: boolean;
    hasPreviousPage: boolean;
  };
}

type PaginatedResponse<T> = SuccessResponse<PaginatedData<T>>;

// Union type for all responses
type ApiResponse<T> = SuccessResponse<T> | ErrorResponse;
```

### Response Helper Functions

```typescript
import { randomUUID } from "crypto";

const API_VERSION = "1.0.0";

function createMeta(requestId?: string): BaseResponse["meta"] {
  return {
    timestamp: new Date().toISOString(),
    requestId: requestId ?? randomUUID(),
    version: API_VERSION,
  };
}

export function successResponse<T>(
  data: T,
  requestId?: string
): SuccessResponse<T> {
  return {
    success: true,
    data,
    meta: createMeta(requestId),
  };
}

export function errorResponse(
  error: AppError,
  requestId?: string,
  includeStack = false
): ErrorResponse {
  return {
    success: false,
    error: {
      code: error.code,
      message: error.message,
      details: error.context,
      ...(includeStack && { stack: error.stack }),
    },
    meta: createMeta(requestId),
  };
}

export function paginatedResponse<T>(
  items: T[],
  page: number,
  pageSize: number,
  totalItems: number,
  requestId?: string
): PaginatedResponse<T> {
  const totalPages = Math.ceil(totalItems / pageSize);

  return {
    success: true,
    data: {
      items,
      pagination: {
        page,
        pageSize,
        totalItems,
        totalPages,
        hasNextPage: page < totalPages,
        hasPreviousPage: page > 1,
      },
    },
    meta: createMeta(requestId),
  };
}
```

### Express Integration

```typescript
import { Request, Response, NextFunction } from "express";

// Type-safe request handler
type AsyncHandler<TParams = {}, TBody = {}, TQuery = {}> = (
  req: Request<TParams, unknown, TBody, TQuery>,
  res: Response,
  next: NextFunction
) => Promise<void>;

// Wrapper for async handlers
function asyncHandler<TParams = {}, TBody = {}, TQuery = {}>(
  handler: AsyncHandler<TParams, TBody, TQuery>
): AsyncHandler<TParams, TBody, TQuery> {
  return async (req, res, next) => {
    try {
      await handler(req, res, next);
    } catch (error) {
      next(error);
    }
  };
}

// Type-safe controller
interface GetUserParams {
  id: string;
}

export const getUser = asyncHandler<GetUserParams>(async (req, res) => {
  const { id } = req.params;
  const user = await userService.getById(id);

  res.json(successResponse(user, req.requestId));
});

// Global error handler
export function errorHandler(
  error: Error,
  req: Request,
  res: Response,
  _next: NextFunction
): void {
  const isDev = process.env.NODE_ENV === "development";

  if (error instanceof AppError) {
    res.status(error.statusCode).json(
      errorResponse(error, req.requestId, isDev)
    );
    return;
  }

  // Unknown error
  logger.error("Unhandled error", { error, requestId: req.requestId });

  const internalError = new InternalError();
  res.status(500).json(errorResponse(internalError, req.requestId, isDev));
}
```

## Async/Await Best Practices

### Proper Promise Handling

```typescript
// ❌ Bad - fire and forget (unhandled promise)
async function processUsers(users: User[]): Promise<void> {
  users.forEach(async (user) => {
    await sendEmail(user.email); // These promises are not awaited!
  });
  console.log("Done"); // This runs before emails are sent!
}

// ❌ Bad - sequential when parallel is possible
async function fetchAllData(): Promise<[User[], Product[], Order[]]> {
  const users = await fetchUsers();
  const products = await fetchProducts();
  const orders = await fetchOrders();
  return [users, products, orders];
}

// ✅ Good - parallel execution with Promise.all
async function processUsers(users: User[]): Promise<void> {
  await Promise.all(users.map((user) => sendEmail(user.email)));
  console.log("All emails sent");
}

// ✅ Good - parallel independent requests
async function fetchAllData(): Promise<[User[], Product[], Order[]]> {
  const [users, products, orders] = await Promise.all([
    fetchUsers(),
    fetchProducts(),
    fetchOrders(),
  ]);
  return [users, products, orders];
}

// ✅ Good - sequential processing when order matters
async function processUsersSequentially(users: User[]): Promise<void> {
  for (const user of users) {
    await sendEmail(user.email);
    await updateUserStatus(user.id, "notified");
  }
}
```

### Promise.allSettled for Partial Failures

```typescript
interface BatchResult<T> {
  succeeded: T[];
  failed: Array<{ item: unknown; error: Error }>;
}

async function processBatch<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>
): Promise<BatchResult<R>> {
  const results = await Promise.allSettled(items.map(processor));

  const succeeded: R[] = [];
  const failed: Array<{ item: unknown; error: Error }> = [];

  results.forEach((result, index) => {
    if (result.status === "fulfilled") {
      succeeded.push(result.value);
    } else {
      failed.push({
        item: items[index],
        error: result.reason instanceof Error
          ? result.reason
          : new Error(String(result.reason)),
      });
    }
  });

  return { succeeded, failed };
}

// Usage
const { succeeded, failed } = await processBatch(users, async (user) => {
  await sendEmail(user.email);
  return user.id;
});

console.log(`Sent ${succeeded.length} emails, ${failed.length} failed`);
```

### Controlled Concurrency

```typescript
async function processWithConcurrency<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  concurrency: number
): Promise<R[]> {
  const results: R[] = [];
  const executing: Promise<void>[] = [];

  for (const item of items) {
    const promise = processor(item).then((result) => {
      results.push(result);
    });

    executing.push(promise);

    if (executing.length >= concurrency) {
      await Promise.race(executing);
      // Remove completed promises
      const completed = executing.filter(
        (p) => p !== promise && !isPending(p)
      );
      executing.splice(0, executing.length, ...executing.filter(isPending));
    }
  }

  await Promise.all(executing);
  return results;
}

// Using p-limit library (recommended)
import pLimit from "p-limit";

async function processWithLimit<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  concurrency: number
): Promise<R[]> {
  const limit = pLimit(concurrency);
  return Promise.all(items.map((item) => limit(() => processor(item))));
}

// Usage
const results = await processWithLimit(
  users,
  async (user) => sendEmail(user.email),
  5 // Max 5 concurrent operations
);
```

### Timeout Handling

```typescript
function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number,
  timeoutMessage = "Operation timed out"
): Promise<T> {
  return Promise.race([
    promise,
    new Promise<never>((_, reject) =>
      setTimeout(() => reject(new Error(timeoutMessage)), timeoutMs)
    ),
  ]);
}

// Usage
try {
  const result = await withTimeout(
    fetchData(),
    5000,
    "Data fetch timed out after 5 seconds"
  );
} catch (error) {
  if (error.message.includes("timed out")) {
    // Handle timeout
  }
}

// AbortController for cancellable operations
async function fetchWithAbort(
  url: string,
  timeoutMs: number
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, { signal: controller.signal });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}
```

### Retry Pattern

```typescript
interface RetryOptions {
  maxAttempts: number;
  delayMs: number;
  backoffMultiplier?: number;
  maxDelayMs?: number;
  shouldRetry?: (error: Error, attempt: number) => boolean;
}

async function withRetry<T>(
  operation: () => Promise<T>,
  options: RetryOptions
): Promise<T> {
  const {
    maxAttempts,
    delayMs,
    backoffMultiplier = 2,
    maxDelayMs = 30000,
    shouldRetry = () => true,
  } = options;

  let lastError: Error;
  let currentDelay = delayMs;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await operation();
    } catch (error) {
      lastError = error instanceof Error ? error : new Error(String(error));

      if (attempt === maxAttempts || !shouldRetry(lastError, attempt)) {
        throw lastError;
      }

      logger.warn(`Attempt ${attempt} failed, retrying...`, {
        error: lastError.message,
        nextAttemptIn: currentDelay,
      });

      await sleep(currentDelay);
      currentDelay = Math.min(currentDelay * backoffMultiplier, maxDelayMs);
    }
  }

  throw lastError!;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Usage
const data = await withRetry(() => fetchExternalApi(), {
  maxAttempts: 3,
  delayMs: 1000,
  backoffMultiplier: 2,
  shouldRetry: (error) => {
    // Only retry on network errors or 5xx
    return error.message.includes("network") || error.message.includes("5");
  },
});
```

## Utility Types

### Deep Partial

```typescript
type DeepPartial<T> = T extends object
  ? { [P in keyof T]?: DeepPartial<T[P]> }
  : T;

// Usage
interface Config {
  database: {
    host: string;
    port: number;
    credentials: {
      username: string;
      password: string;
    };
  };
  cache: {
    enabled: boolean;
    ttl: number;
  };
}

type ConfigUpdate = DeepPartial<Config>;

// Can update nested properties partially
const update: ConfigUpdate = {
  database: {
    credentials: {
      password: "newPassword",
    },
  },
};
```

### Required Fields

```typescript
// Make specific fields required
type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>;

// Make all fields required except specific ones
type RequiredExcept<T, K extends keyof T> = Required<Omit<T, K>> & Pick<T, K>;

// Usage
interface User {
  id: string;
  name: string;
  email?: string;
  phone?: string;
  avatar?: string;
}

type UserWithEmail = RequiredFields<User, "email">;
// { id: string; name: string; email: string; phone?: string; avatar?: string }

type UserComplete = RequiredExcept<User, "avatar">;
// { id: string; name: string; email: string; phone: string; avatar?: string }
```

### Nullable and NonNullable Utilities

```typescript
// Make all fields nullable
type Nullable<T> = { [K in keyof T]: T[K] | null };

// Deep non-nullable
type DeepNonNullable<T> = T extends object
  ? { [K in keyof T]: DeepNonNullable<NonNullable<T[K]>> }
  : NonNullable<T>;

// Optional to nullable (for database operations)
type OptionalToNullable<T> = {
  [K in keyof T]-?: undefined extends T[K] ? T[K] | null : T[K];
};
```

### Extract and Filter Types

```typescript
// Extract keys by value type
type KeysOfType<T, V> = {
  [K in keyof T]: T[K] extends V ? K : never;
}[keyof T];

// Extract string keys
type StringKeys<T> = KeysOfType<T, string>;

// Usage
interface User {
  id: string;
  name: string;
  age: number;
  isActive: boolean;
}

type UserStringKeys = StringKeys<User>; // "id" | "name"

// Filter object to specific types
type PickByType<T, V> = Pick<T, KeysOfType<T, V>>;

type UserStrings = PickByType<User, string>;
// { id: string; name: string }
```

### Function Types

```typescript
// Extract async function return type
type AsyncReturnType<T extends (...args: any[]) => Promise<any>> =
  T extends (...args: any[]) => Promise<infer R> ? R : never;

// Function with specific return type
type FunctionWithReturn<TArgs extends any[], TReturn> = (
  ...args: TArgs
) => TReturn;

// Async version
type AsyncFunction<TArgs extends any[], TReturn> = (
  ...args: TArgs
) => Promise<TReturn>;

// Usage
async function fetchUser(id: string): Promise<User> {
  // ...
}

type FetchedUser = AsyncReturnType<typeof fetchUser>; // User
```

### Builder Pattern Types

```typescript
type Builder<T> = {
  [K in keyof T as `set${Capitalize<string & K>}`]: (
    value: T[K]
  ) => Builder<T>;
} & {
  build: () => T;
};

// Mutable type (remove readonly)
type Mutable<T> = {
  -readonly [K in keyof T]: T[K];
};

// Immutable type (add readonly)
type Immutable<T> = {
  readonly [K in keyof T]: T[K] extends object ? Immutable<T[K]> : T[K];
};
```

### Path Types (for nested object access)

```typescript
type PathImpl<T, K extends keyof T> = K extends string
  ? T[K] extends Record<string, any>
    ? T[K] extends ArrayLike<any>
      ? K | `${K}.${PathImpl<T[K], Exclude<keyof T[K], keyof any[]>>}`
      : K | `${K}.${PathImpl<T[K], keyof T[K]>}`
    : K
  : never;

type Path<T> = PathImpl<T, keyof T>;

type PathValue<T, P extends Path<T>> = P extends `${infer K}.${infer Rest}`
  ? K extends keyof T
    ? Rest extends Path<T[K]>
      ? PathValue<T[K], Rest>
      : never
    : never
  : P extends keyof T
    ? T[P]
    : never;

// Usage
interface Settings {
  user: {
    profile: {
      name: string;
      email: string;
    };
    preferences: {
      theme: "light" | "dark";
    };
  };
}

type SettingsPaths = Path<Settings>;
// "user" | "user.profile" | "user.profile.name" | "user.profile.email" | ...

function getSetting<P extends Path<Settings>>(
  settings: Settings,
  path: P
): PathValue<Settings, P> {
  // Implementation
}
```

## Dependency Injection Patterns

### Constructor Injection

```typescript
// ❌ Bad - tight coupling, hard to test
class UserService {
  private db = new Database();
  private mailer = new EmailService();
  private logger = new Logger();

  async createUser(data: CreateUserDto): Promise<User> {
    const user = await this.db.user.create({ data });
    await this.mailer.sendWelcomeEmail(user.email);
    this.logger.info("User created", { userId: user.id });
    return user;
  }
}

// ✅ Good - dependency injection
interface IUserRepository {
  create(data: CreateUserDto): Promise<User>;
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
}

interface IEmailService {
  sendWelcomeEmail(to: string): Promise<void>;
  sendPasswordReset(to: string, token: string): Promise<void>;
}

interface ILogger {
  info(message: string, meta?: Record<string, unknown>): void;
  error(message: string, meta?: Record<string, unknown>): void;
}

class UserService {
  constructor(
    private readonly userRepository: IUserRepository,
    private readonly emailService: IEmailService,
    private readonly logger: ILogger
  ) {}

  async createUser(data: CreateUserDto): Promise<User> {
    const user = await this.userRepository.create(data);
    await this.emailService.sendWelcomeEmail(user.email);
    this.logger.info("User created", { userId: user.id });
    return user;
  }
}
```

### Factory Pattern with DI

```typescript
// Service factory
interface ServiceContainer {
  userRepository: IUserRepository;
  emailService: IEmailService;
  logger: ILogger;
}

function createUserService(container: ServiceContainer): UserService {
  return new UserService(
    container.userRepository,
    container.emailService,
    container.logger
  );
}

// Container setup
function createContainer(): ServiceContainer {
  const logger = new ConsoleLogger();
  const db = new PrismaClient();

  return {
    userRepository: new PrismaUserRepository(db),
    emailService: new SendGridEmailService(process.env.SENDGRID_API_KEY!),
    logger,
  };
}

// Application bootstrap
const container = createContainer();
const userService = createUserService(container);
```

### Functional Dependency Injection

```typescript
// Dependencies as function parameters
type CreateUserFn = (
  deps: {
    userRepo: IUserRepository;
    emailService: IEmailService;
    logger: ILogger;
  },
  data: CreateUserDto
) => Promise<User>;

const createUser: CreateUserFn = async (deps, data) => {
  const { userRepo, emailService, logger } = deps;

  const user = await userRepo.create(data);
  await emailService.sendWelcomeEmail(user.email);
  logger.info("User created", { userId: user.id });

  return user;
};

// Partial application for convenience
const createUserWithDeps = (deps: Parameters<CreateUserFn>[0]) =>
  (data: CreateUserDto) => createUser(deps, data);

// Usage
const boundCreateUser = createUserWithDeps({
  userRepo: new PrismaUserRepository(db),
  emailService: new SendGridEmailService(apiKey),
  logger: new ConsoleLogger(),
});

const user = await boundCreateUser({ name: "John", email: "john@example.com" });
```

### Testing with DI

```typescript
// Mock implementations
class MockUserRepository implements IUserRepository {
  private users: User[] = [];

  async create(data: CreateUserDto): Promise<User> {
    const user: User = { id: randomUUID(), ...data, createdAt: new Date() };
    this.users.push(user);
    return user;
  }

  async findById(id: string): Promise<User | null> {
    return this.users.find((u) => u.id === id) ?? null;
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.users.find((u) => u.email === email) ?? null;
  }
}

class MockEmailService implements IEmailService {
  sentEmails: Array<{ to: string; type: string }> = [];

  async sendWelcomeEmail(to: string): Promise<void> {
    this.sentEmails.push({ to, type: "welcome" });
  }

  async sendPasswordReset(to: string, _token: string): Promise<void> {
    this.sentEmails.push({ to, type: "password-reset" });
  }
}

// Test
describe("UserService", () => {
  let userService: UserService;
  let mockUserRepo: MockUserRepository;
  let mockEmailService: MockEmailService;

  beforeEach(() => {
    mockUserRepo = new MockUserRepository();
    mockEmailService = new MockEmailService();
    userService = new UserService(
      mockUserRepo,
      mockEmailService,
      new NoopLogger()
    );
  });

  it("should create user and send welcome email", async () => {
    const user = await userService.createUser({
      name: "John",
      email: "john@example.com",
    });

    expect(user.name).toBe("John");
    expect(mockEmailService.sentEmails).toHaveLength(1);
    expect(mockEmailService.sentEmails[0]).toEqual({
      to: "john@example.com",
      type: "welcome",
    });
  });
});
```

## Environment Variables Validation

### Zod Schema Validation

```typescript
import { z } from "zod";

// Environment schema
const envSchema = z.object({
  // Node environment
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),

  // Server
  PORT: z.string().regex(/^\d+$/).transform(Number).default("3000"),
  HOST: z.string().default("0.0.0.0"),

  // Database
  DATABASE_URL: z.string().url(),
  DATABASE_POOL_SIZE: z
    .string()
    .regex(/^\d+$/)
    .transform(Number)
    .default("10"),

  // Redis
  REDIS_URL: z.string().url().optional(),
  REDIS_PASSWORD: z.string().optional(),

  // Authentication
  JWT_SECRET: z.string().min(32),
  JWT_EXPIRES_IN: z.string().default("7d"),
  REFRESH_TOKEN_EXPIRES_IN: z.string().default("30d"),

  // External APIs
  OPENAI_API_KEY: z.string().startsWith("sk-").optional(),
  STRIPE_SECRET_KEY: z.string().startsWith("sk_").optional(),
  STRIPE_WEBHOOK_SECRET: z.string().startsWith("whsec_").optional(),

  // Email
  SMTP_HOST: z.string().optional(),
  SMTP_PORT: z.string().regex(/^\d+$/).transform(Number).optional(),
  SMTP_USER: z.string().optional(),
  SMTP_PASSWORD: z.string().optional(),
  EMAIL_FROM: z.string().email().optional(),

  // Feature flags
  ENABLE_CACHE: z
    .string()
    .transform((v) => v === "true")
    .default("true"),
  ENABLE_RATE_LIMIT: z
    .string()
    .transform((v) => v === "true")
    .default("true"),

  // Logging
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
});

// Infer type from schema
type Env = z.infer<typeof envSchema>;

// Parse and validate
function validateEnv(): Env {
  const result = envSchema.safeParse(process.env);

  if (!result.success) {
    console.error("❌ Invalid environment variables:");
    console.error(result.error.format());
    process.exit(1);
  }

  return result.data;
}

// Export validated env
export const env = validateEnv();

// Type-safe usage
console.log(env.PORT); // number
console.log(env.NODE_ENV); // "development" | "production" | "test"
console.log(env.ENABLE_CACHE); // boolean
```

### Environment-Specific Configs

```typescript
import { z } from "zod";

// Base config
const baseConfigSchema = z.object({
  appName: z.string().default("MyApp"),
  port: z.number(),
  logLevel: z.enum(["debug", "info", "warn", "error"]),
});

// Development config
const developmentConfigSchema = baseConfigSchema.extend({
  debug: z.literal(true),
  database: z.object({
    url: z.string(),
    logging: z.literal(true),
  }),
});

// Production config
const productionConfigSchema = baseConfigSchema.extend({
  debug: z.literal(false),
  database: z.object({
    url: z.string().url(),
    logging: z.literal(false),
    ssl: z.literal(true),
  }),
});

// Combined config type
type Config =
  | z.infer<typeof developmentConfigSchema>
  | z.infer<typeof productionConfigSchema>;

function loadConfig(): Config {
  const nodeEnv = process.env.NODE_ENV ?? "development";

  if (nodeEnv === "production") {
    return productionConfigSchema.parse({
      appName: process.env.APP_NAME,
      port: Number(process.env.PORT),
      logLevel: process.env.LOG_LEVEL,
      debug: false,
      database: {
        url: process.env.DATABASE_URL,
        logging: false,
        ssl: true,
      },
    });
  }

  return developmentConfigSchema.parse({
    appName: process.env.APP_NAME ?? "MyApp-Dev",
    port: Number(process.env.PORT ?? 3000),
    logLevel: process.env.LOG_LEVEL ?? "debug",
    debug: true,
    database: {
      url: process.env.DATABASE_URL ?? "postgresql://localhost:5432/dev",
      logging: true,
    },
  });
}

export const config = loadConfig();
```

## Import Organization

### Import Order Convention

```typescript
// 1. Node.js built-in modules
import { readFile } from "fs/promises";
import { join } from "path";
import { randomUUID } from "crypto";

// 2. External dependencies (npm packages)
import express, { Request, Response } from "express";
import { z } from "zod";
import { PrismaClient } from "@prisma/client";

// 3. Internal aliases (@/ paths)
import { UserService } from "@/services/user.service";
import { validateRequest } from "@/middleware/validation";
import { logger } from "@/lib/logger";

// 4. Type-only imports (use 'import type')
import type { User, CreateUserDto } from "@/types";
import type { Config } from "@/config";

// 5. Relative imports (same module/feature)
import { formatDate } from "./utils";
import { USER_ROLES } from "./constants";
```

### Type-Only Imports

```typescript
// ❌ Bad - importing type as value (increases bundle size)
import { User } from "./types";

function processUser(user: User): void {}

// ✅ Good - explicit type import
import type { User } from "./types";

function processUser(user: User): void {}

// ✅ Good - mixed import
import { UserService, type User } from "./user";

// ✅ Good - re-export types
// types/index.ts
export type { User, CreateUserDto, UpdateUserDto } from "./user.types";
export type { ApiResponse, PaginatedResponse } from "./api.types";
```

### Barrel Files (Index Exports)

```typescript
// services/index.ts
export { UserService } from "./user.service";
export { AuthService } from "./auth.service";
export { EmailService } from "./email.service";

// types/index.ts
export type { User, CreateUserDto, UpdateUserDto } from "./user.types";
export type { ApiResponse, ErrorResponse } from "./api.types";

// Usage - clean imports
import { UserService, AuthService } from "@/services";
import type { User, ApiResponse } from "@/types";
```

## ESLint Configuration

### Recommended ESLint Config

```javascript
// eslint.config.js (ESLint 9+ flat config)
import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import prettier from "eslint-config-prettier";

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.strictTypeChecked,
  ...tseslint.configs.stylisticTypeChecked,
  prettier,
  {
    languageOptions: {
      parserOptions: {
        project: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      // Prevent any
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-unsafe-assignment": "error",
      "@typescript-eslint/no-unsafe-member-access": "error",
      "@typescript-eslint/no-unsafe-call": "error",
      "@typescript-eslint/no-unsafe-return": "error",

      // Require explicit return types
      "@typescript-eslint/explicit-function-return-type": [
        "warn",
        {
          allowExpressions: true,
          allowTypedFunctionExpressions: true,
        },
      ],

      // Unused variables
      "@typescript-eslint/no-unused-vars": [
        "error",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
        },
      ],

      // Naming conventions
      "@typescript-eslint/naming-convention": [
        "error",
        // Variables and functions - camelCase
        {
          selector: "variableLike",
          format: ["camelCase", "UPPER_CASE"],
          leadingUnderscore: "allow",
        },
        // Types, interfaces, classes - PascalCase
        {
          selector: "typeLike",
          format: ["PascalCase"],
        },
        // Enum members - UPPER_CASE or PascalCase
        {
          selector: "enumMember",
          format: ["UPPER_CASE", "PascalCase"],
        },
        // No I prefix for interfaces
        {
          selector: "interface",
          format: ["PascalCase"],
          custom: {
            regex: "^I[A-Z]",
            match: false,
          },
        },
      ],

      // Enforce consistent type imports
      "@typescript-eslint/consistent-type-imports": [
        "error",
        {
          prefer: "type-imports",
          fixStyle: "separate-type-imports",
        },
      ],

      // Async/Promise rules
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/no-misused-promises": "error",
      "@typescript-eslint/await-thenable": "error",

      // Other strict rules
      "@typescript-eslint/no-non-null-assertion": "warn",
      "@typescript-eslint/prefer-nullish-coalescing": "error",
      "@typescript-eslint/prefer-optional-chain": "error",
      "@typescript-eslint/strict-boolean-expressions": "warn",
    },
  },
  {
    // Relaxed rules for test files
    files: ["**/*.test.ts", "**/*.spec.ts"],
    rules: {
      "@typescript-eslint/no-explicit-any": "off",
      "@typescript-eslint/no-non-null-assertion": "off",
    },
  }
);
```

## Common Patterns Checklist

When writing TypeScript code, ensure:

### Type Safety
- [ ] No `any` types (use `unknown` for truly dynamic data)
- [ ] All functions have explicit return types
- [ ] Generic types have meaningful constraints
- [ ] Type guards used for runtime type narrowing
- [ ] Discriminated unions for state management

### Error Handling
- [ ] Custom error classes extend base AppError
- [ ] Errors include error codes and context
- [ ] Operational vs programmer errors distinguished
- [ ] try-catch blocks handle errors appropriately
- [ ] Async errors properly propagated

### Code Organization
- [ ] Types exported from dedicated .types.ts files
- [ ] Import order follows convention
- [ ] Type-only imports use `import type`
- [ ] Barrel files for clean imports
- [ ] No circular dependencies

### Configuration
- [ ] Environment variables validated with Zod
- [ ] tsconfig.json uses strict mode
- [ ] ESLint configured with TypeScript rules
- [ ] Path aliases configured (@/)

### Async Code
- [ ] No fire-and-forget promises
- [ ] Promise.all for parallel operations
- [ ] Proper error handling in async functions
- [ ] Timeout handling for external calls
- [ ] Retry logic for transient failures

### Dependencies
- [ ] Services use dependency injection
- [ ] Interfaces defined for external dependencies
- [ ] Mocks created for testing
- [ ] No hard-coded dependencies in classes

### Naming
- [ ] camelCase for variables and functions
- [ ] PascalCase for types, interfaces, classes
- [ ] SCREAMING_SNAKE_CASE for constants
- [ ] Boolean variables have is/has/can prefix
- [ ] No Hungarian notation (I prefix)

### API Design
- [ ] Standard response types used
- [ ] Error responses include codes
- [ ] Pagination follows standard pattern
- [ ] Request/response types defined
