# 1. Clone repo ของคุณ
git clone https://github.com/AmnadTaowsoam/cerebratechai-claude-skills.git
cd cerebratechai-claude-skills

# 2. สร้างโครงสร้างหลัก
mkdir -p {01-foundations,02-frontend,03-backend-api,04-database,05-ai-ml-core,06-ai-ml-production,07-document-processing,08-messaging-queue,09-microservices,10-authentication-authorization,11-billing-subscription,12-compliance-governance,13-file-storage,14-monitoring-observability,15-devops-infrastructure,16-testing,17-domain-specific}

# 3. เปิด Claude CLI
# ใช้ --dangerously-skip-permissions เพื่อให้ Claude สามารถสร้างไฟล์ได้
```

---

## 🎯 Batch 1: Foundations (01) - 5 Skills

### Prompt 1.1: TypeScript Standards
```
I need you to create a comprehensive SKILL.md file for TypeScript coding standards.

Location: 01-foundations/typescript-standards/SKILL.md

Create a detailed guide covering:
1. TypeScript configuration (tsconfig.json with strict mode)
2. Naming conventions (variables, functions, classes, constants, files)
3. Type definitions (basic types, interfaces vs types, generics)
4. Error handling patterns (custom error classes, try-catch patterns, Result type)
5. API response patterns (standard response types, helper functions)
6. Async/await best practices
7. Utility types (DeepPartial, RequiredFields, etc.)
8. Dependency injection patterns
9. Environment variables validation (with Zod)
10. Import organization
11. ESLint configuration
12. Testing types
13. Common patterns checklist

Format: Use markdown with clear code examples in TypeScript. Include ❌ Bad and ✅ Good examples throughout.

Please create the file with complete, production-ready content.
```

### Prompt 1.2: Python Standards
```
Create a comprehensive SKILL.md file for Python coding standards.

Location: 01-foundations/python-standards/SKILL.md

Cover these topics:
1. Python version and setup (pyproject.toml, Python 3.11+)
2. Naming conventions (PEP 8 compliance)
3. Type hints (modern Python 3.10+ syntax)
4. Pydantic models for validation
5. Error handling (custom exceptions, try-except patterns, context managers)
6. Async/await patterns
7. Logging best practices
8. Function patterns (dependency injection with Protocol)
9. Dataclasses vs Pydantic
10. File organization and imports
11. Environment variables (Pydantic Settings)
12. Testing patterns (pytest, fixtures, parametrize, mocking)
13. Code quality tools (Black, Ruff, Mypy)
14. Pre-commit configuration

Format: Markdown with clear Python code examples showing ❌ Bad and ✅ Good patterns.

Create the complete file now.
```

### Prompt 1.3: Code Review Guidelines
```
Create a SKILL.md for code review best practices.

Location: 01-foundations/code-review/SKILL.md

Include:
1. Code review principles
2. What to look for:
   - Code quality and readability
   - Security vulnerabilities
   - Performance issues
   - Testing coverage
   - Documentation
3. Review checklist by category:
   - General code quality
   - Security
   - Performance
   - Testing
   - API design
4. How to give feedback (constructive comments)
5. How to receive feedback
6. Common anti-patterns to catch
7. Automated checks vs manual review
8. Review process workflow
9. Examples of good/bad review comments

Format: Markdown with examples and checklists.

Create the file now.
```

### Prompt 1.4: Git Workflow
```
Create a SKILL.md for Git workflow and best practices.

Location: 01-foundations/git-workflow/SKILL.md

Cover:
1. Branch naming conventions
   - feature/*, bugfix/*, hotfix/*, release/*
2. Commit message format
   - Conventional Commits
   - feat, fix, docs, style, refactor, test, chore
3. Git flow vs GitHub flow
4. Pull request process
5. Merge strategies (merge, squash, rebase)
6. Common Git commands and scenarios
7. .gitignore best practices
8. Handling merge conflicts
9. Git hooks (pre-commit, pre-push)
10. Tagging and releases
11. Emergency hotfix process

Format: Markdown with command examples and templates.

Create the file now.
```

### Prompt 1.5: API Design Principles
```
Create a SKILL.md for RESTful API design principles.

Location: 01-foundations/api-design/SKILL.md

Include:
1. REST principles
2. HTTP methods usage (GET, POST, PUT, PATCH, DELETE)
3. URL structure and naming
   - Resource naming
   - Nested resources
   - Query parameters
4. Status codes (2xx, 4xx, 5xx)
5. Request/Response format
   - JSON structure
   - Error responses
   - Pagination
   - Filtering and sorting
6. Versioning strategies
7. Authentication patterns
8. Rate limiting headers
9. CORS configuration
10. API documentation requirements
11. Common API patterns checklist

Format: Markdown with examples of good API design.

Create the complete file now.
```

---

## 🎯 Batch 2: Frontend (02) - 7 Skills

### Prompt 2.1: Next.js Patterns
```
Create a comprehensive SKILL.md for Next.js 14+ App Router patterns.

Location: 02-frontend/nextjs-patterns/SKILL.md

Cover:
1. App Router structure and conventions
2. Server Components vs Client Components
   - When to use each
   - "use client" directive
3. Data fetching patterns
   - Server components
   - Client components
   - Streaming and Suspense
4. Caching strategies
   - force-cache, no-store
   - revalidate options
   - Route handlers
5. API Routes patterns (Route Handlers)
6. Metadata API
7. Loading and Error states
8. Route groups and layouts
9. Parallel and Intercepting routes
10. Server Actions
11. Middleware
12. Performance optimization

Format: Markdown with TypeScript code examples.

Create the file now.
```

### Prompt 2.2: React Best Practices
```
Create a SKILL.md for React best practices and patterns.

Location: 02-frontend/react-best-practices/SKILL.md

Include:
1. Component patterns
   - Functional components
   - Custom hooks
   - Composition patterns
2. State management
   - useState, useReducer
   - When to lift state up
   - Context API usage
3. Performance optimization
   - useMemo, useCallback
   - React.memo
   - Code splitting
4. Side effects (useEffect)
   - Dependencies
   - Cleanup
   - Common pitfalls
5. Forms handling
6. Error boundaries
7. Accessibility (a11y)
8. Testing components
9. Common anti-patterns to avoid
10. TypeScript with React

Format: Markdown with React/TypeScript examples.

Create the file now.
```

### Prompt 2.3: Tailwind CSS Patterns
```
Create a SKILL.md for Tailwind CSS patterns and best practices.

Location: 02-frontend/tailwind-patterns/SKILL.md

Cover:
1. Configuration (tailwind.config.js)
   - Theme customization
   - Custom colors
   - Extending utilities
2. Common utility patterns
   - Layout (flex, grid)
   - Spacing
   - Typography
   - Colors and backgrounds
3. Responsive design
   - Breakpoints
   - Mobile-first approach
4. Component patterns
   - Buttons
   - Cards
   - Forms
   - Navigation
5. Dark mode implementation
6. Custom utilities with @apply
7. Performance optimization
8. With CSS-in-JS (styled-components, emotion)
9. Common layouts
10. Best practices

Format: Markdown with HTML/Tailwind examples.

Create the file now.
```

### Prompt 2.4: Material-UI (MUI)
```
Create a SKILL.md for Material-UI (MUI) best practices.

Location: 02-frontend/mui-material/SKILL.md

Include:
1. Theme setup and customization
2. Component styling approaches
   - sx prop
   - styled() API
   - makeStyles (legacy)
3. Common components
   - Layout (Grid, Stack, Container, Box)
   - Navigation (AppBar, Drawer, Tabs)
   - Forms (TextField, Select, Checkbox)
   - Feedback (Snackbar, Dialog, Alert)
   - Data Display (Table, Card, List)
4. Responsive design with MUI
5. Dark mode implementation
6. Custom theme tokens
7. Performance optimization
8. TypeScript integration
9. Common patterns and recipes

Format: Markdown with React/TypeScript/MUI examples.

Create the file now.
```

### Prompt 2.5: shadcn/ui Patterns
```
Create a SKILL.md for shadcn/ui component patterns.

Location: 02-frontend/shadcn-ui/SKILL.md

Cover:
1. Installation and setup
2. Component categories
   - Form components
   - Overlay components
   - Data display
   - Navigation
   - Feedback
3. Composition patterns
   - Form with validation (React Hook Form + Zod)
   - Data tables with sorting
   - Command palette
   - Dialog patterns
4. Customization
   - Tailwind configuration
   - Component modification
   - Custom variants
5. Accessibility features
6. Integration with React Hook Form
7. Common recipes
8. Best practices

Format: Markdown with TypeScript/React examples.

Create the file now.
```

### Prompt 2.6: Form Handling
```
Create a SKILL.md for form handling with React Hook Form and Zod.

Location: 02-frontend/form-handling/SKILL.md

Include:
1. Setup (React Hook Form + Zod)
2. Validation schemas
   - Basic schema
   - Advanced validation
   - Nested objects
   - Arrays
   - Custom validators
3. Form implementation
   - Basic form
   - Multi-step form
   - Dynamic fields (useFieldArray)
   - File uploads
4. Error handling
   - Field-level errors
   - Form-level errors
   - Server-side errors
   - Async validation
5. Performance optimization
6. Integration with UI libraries
7. Common patterns
8. Testing forms

Format: Markdown with TypeScript examples.

Create the file now.
```

### Prompt 2.7: State Management
```
Create a SKILL.md for state management patterns in React.

Location: 02-frontend/state-management/SKILL.md

Cover:
1. When to use each solution
2. React Context
   - Setup
   - Usage patterns
   - Performance considerations
3. Zustand
   - Store creation
   - Usage
   - Middleware
4. Redux Toolkit
   - Slices
   - Async thunks
   - RTK Query
5. TanStack Query (React Query)
   - Queries
   - Mutations
   - Cache management
   - Optimistic updates
6. Jotai (atoms)
7. Decision matrix
8. Best practices per solution

Format: Markdown with TypeScript examples.

Create the file now.
```

---

## 🎯 Batch 3: Backend API (03) - 6 Skills

### Prompt 3.1: Node.js REST API
```
Create a comprehensive SKILL.md for Node.js REST API patterns.

Location: 03-backend-api/nodejs-api/SKILL.md

Cover:
1. Project structure
2. Express.js setup
3. Middleware patterns
   - Authentication
   - Error handling
   - Request validation
   - Logging
4. Controller patterns
5. Service layer patterns
6. Repository pattern
7. Dependency injection
8. Error handling
9. Request validation (Zod)
10. Response formatting
11. Testing patterns
12. Security best practices

Format: Markdown with TypeScript examples.

Create the file now.
```

### Prompt 3.2: FastAPI Patterns
```
Create a SKILL.md for FastAPI patterns and best practices.

Location: 03-backend-api/fastapi-patterns/SKILL.md

Include:
1. Project structure
2. Application setup
3. Pydantic models
   - Request models
   - Response models
   - Validation
4. Dependency injection
5. Async patterns
6. Error handling
7. Middleware
8. Background tasks
9. WebSocket support
10. File uploads
11. Testing with pytest
12. Auto-documentation

Format: Markdown with Python examples.

Create the file now.
```

### Prompt 3.3: Express REST API
```
Create a SKILL.md for Express.js REST API patterns.

Location: 03-backend-api/express-rest/SKILL.md

Cover:
1. App initialization
2. Routing patterns
3. Middleware stack
4. Error handling middleware
5. Request validation
6. Authentication middleware
7. CORS configuration
8. Rate limiting
9. Security headers
10. Logging
11. Testing
12. Production setup

Format: Markdown with TypeScript examples.

Create the file now.
```

### Prompt 3.4: Error Handling
```
Create a SKILL.md for backend error handling patterns.

Location: 03-backend-api/error-handling/SKILL.md

Include:
1. Error types and classification
2. Custom error classes
3. Error middleware (Express)
4. Error responses format
5. Logging errors
6. Error monitoring
7. Validation errors
8. Database errors
9. External API errors
10. Operational vs programmer errors
11. Error recovery strategies
12. Testing error scenarios

Format: Markdown with TypeScript and Python examples.

Create the file now.
```

### Prompt 3.5: Request Validation
```
Create a SKILL.md for API request validation patterns.

Location: 03-backend-api/validation/SKILL.md

Cover:
1. Validation libraries
   - Zod (TypeScript)
   - Pydantic (Python)
   - Joi (Node.js)
2. Schema definitions
3. Validation middleware
4. Error responses
5. Custom validators
6. Async validation
7. File validation
8. Query parameter validation
9. Path parameter validation
10. Best practices

Format: Markdown with code examples.

Create the file now.
```

### Prompt 3.6: Middleware Patterns
```
Create a SKILL.md for backend middleware patterns.

Location: 03-backend-api/middleware/SKILL.md

Include:
1. Middleware concept
2. Express middleware
   - Request logging
   - Authentication
   - Authorization
   - Error handling
   - Request validation
   - Rate limiting
3. FastAPI middleware
   - CORS
   - Trusted hosts
   - GZip compression
   - Custom middleware
4. Middleware order
5. Testing middleware
6. Common middleware patterns

Format: Markdown with TypeScript and Python examples.

Create the file now.
```

---

## 🎯 Batch 4: Database (04) - 6 Skills

### Prompt 4.1: Prisma Guide
```
Create a comprehensive SKILL.md for Prisma ORM.

Location: 04-database/prisma-guide/SKILL.md

Cover:
1. Schema definition
   - Models
   - Relations
   - Enums
   - Indexes
2. Migrations workflow
3. Query patterns
   - CRUD operations
   - Relations
   - Filtering
   - Pagination
4. Transactions
5. Raw queries
6. Performance optimization
7. Error handling
8. Testing with Prisma
9. Seeding data
10. Best practices

Format: Markdown with TypeScript examples.

Create the file now.
```

### Prompt 4.2: MongoDB Patterns
```
Create a SKILL.md for MongoDB patterns and best practices.

Location: 04-database/mongodb-patterns/SKILL.md

Include:
1. Schema design principles
2. Mongoose setup
3. Model definitions
4. Query patterns
5. Aggregation pipelines
6. Indexing strategies
7. Transactions
8. Change streams
9. Performance optimization
10. Data validation
11. Testing
12. Migration patterns

Format: Markdown with TypeScript examples.

Create the file now.
```

### Prompt 4.3: Redis Caching
```
Create a SKILL.md for Redis caching patterns.

Location: 04-database/redis-caching/SKILL.md

Cover:
1. Redis setup
2. Data structures
   - Strings
   - Hashes
   - Lists
   - Sets
   - Sorted Sets
3. Caching strategies
   - Cache-aside
   - Write-through
   - Write-behind
4. Key naming conventions
5. TTL management
6. Cache invalidation
7. Distributed caching
8. Pub/Sub patterns
9. Session storage
10. Rate limiting with Redis
11. Best practices

Format: Markdown with TypeScript and Python examples.

Create the file now.
```

### Prompt 4.4: TimescaleDB
```
Create a SKILL.md for TimescaleDB (time-series database) patterns.

Location: 04-database/timescaledb/SKILL.md

Include:
1. TimescaleDB setup
2. Hypertable creation
3. Time-based partitioning
4. Continuous aggregates
5. Data retention policies
6. Query optimization for time-series
7. Compression
8. Common time-series queries
9. Downsampling strategies
10. Monitoring and alerting
11. Integration with Grafana
12. Best practices

Format: Markdown with SQL and TypeScript examples.

Create the file now.
```

### Prompt 4.5: Vector Database
```
Create a SKILL.md for Vector Database patterns (Pinecone, Qdrant, Weaviate).

Location: 04-database/vector-database/SKILL.md

Cover:
1. Vector database concepts
2. When to use vector databases
3. Pinecone
   - Setup and indexing
   - Queries
   - Metadata filtering
4. Qdrant
   - Collections
   - Points and vectors
   - Filtering
5. Weaviate
   - Schema
   - Queries
   - Hybrid search
6. Embedding strategies
7. Similarity search
8. Performance optimization
9. Production considerations
10. Cost optimization

Format: Markdown with Python and TypeScript examples.

Create the file now.
```

### Prompt 4.6: Database Optimization
```
Create a SKILL.md for database optimization techniques.

Location: 04-database/database-optimization/SKILL.md

Include:
1. Query optimization
   - EXPLAIN analysis
   - Query planning
   - Join optimization
2. Indexing strategies
   - B-tree indexes
   - Composite indexes
   - Partial indexes
   - Index maintenance
3. Connection pooling
4. N+1 query problem
5. Caching strategies
6. Denormalization when needed
7. Partitioning
8. Monitoring queries
9. Database maintenance
10. Common anti-patterns

Format: Markdown with SQL and code examples.

Create the file now.

