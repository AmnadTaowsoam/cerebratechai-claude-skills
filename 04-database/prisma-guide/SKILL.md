# Prisma ORM Guide

## 1. Schema Definition

### Basic Models
```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  password  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### Relations
```prisma
model User {
  id        String    @id @default(cuid())
  email     String    @unique
  name      String?
  posts     Post[]
  profile   Profile?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)
  authorId  String
  author    User     @relation(fields: [authorId], references: [id])
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Profile {
  id        String  @id @default(cuid())
  bio       String?
  userId    String  @unique
  user      User    @relation(fields: [userId], references: [id])
}
```

### Enums
```prisma
enum Role {
  USER
  ADMIN
  MODERATOR
}

enum Status {
  DRAFT
  PUBLISHED
  ARCHIVED
}

model User {
  id        String  @id @default(cuid())
  email     String  @unique
  role      Role    @default(USER)
  status    Status  @default(DRAFT)
}
```

### Indexes
```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([email, name])
  @@index([createdAt])
  @@index([updatedAt])
}

model Post {
  id        String   @id @default(cuid())
  title     String
  published Boolean  @default(false)
  authorId  String
  createdAt DateTime @default(now())

  @@index([authorId, published])
  @@index([createdAt])
}
```

### Constraints
```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  age       Int
  
  @@map("users")
  @@index([email], name: "user_email_name_idx")
}

model Product {
  id          String  @id @default(cuid())
  name        String
  price       Float
  quantity    Int
  
  @@check: "price >= 0"
  @@check: "quantity >= 0"
}
```

## 2. Migrations Workflow

### Creating a Migration
```bash
# Create a new migration
npx prisma migrate dev --name add_user_profile

# Create migration without name (auto-generated)
npx prisma migrate dev

# Reset database and recreate migrations
npx prisma migrate reset
```

### Applying Migrations to Production
```bash
# Generate migration SQL for review
npx prisma migrate dev --create-only --name add_user_profile

# Deploy migration to production
npx prisma migrate deploy

# Deploy specific migration
npx prisma migrate deploy --name add_user_profile
```

### Migration History
```bash
# View migration history
npx prisma migrate status

# Resolve migration conflicts
npx prisma migrate resolve --applied "add_user_profile"
```

### Seeding Data
```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  // Create users
  const user1 = await prisma.user.create({
    data: {
      email: 'john@example.com',
      name: 'John Doe',
      password: 'hashed_password',
    },
  })

  const user2 = await prisma.user.create({
    data: {
      email: 'jane@example.com',
      name: 'Jane Smith',
      password: 'hashed_password',
    },
  })

  // Create posts
  await prisma.post.create({
    data: {
      title: 'First Post',
      content: 'This is my first post',
      published: true,
      authorId: user1.id,
    },
  })

  console.log('Database seeded successfully')
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
```

```bash
# Run seed script
npx prisma db seed
```

## 3. Query Patterns

### CRUD Operations
```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

// Create
const user = await prisma.user.create({
  data: {
    email: 'john@example.com',
    name: 'John Doe',
    password: 'hashed_password',
  },
})

// Read - Find many
const users = await prisma.user.findMany({
  where: {
    email: {
      contains: 'example.com',
    },
  },
  orderBy: {
    createdAt: 'desc',
  },
  take: 10,
  skip: 0,
})

// Read - Find unique
const user = await prisma.user.findUnique({
  where: {
    email: 'john@example.com',
  },
})

// Read - Find first
const firstUser = await prisma.user.findFirst({
  where: {
    name: {
      startsWith: 'J',
    },
  },
  orderBy: {
    createdAt: 'asc',
  },
})

// Update
const updatedUser = await prisma.user.update({
  where: {
    id: 'user_id',
  },
  data: {
    name: 'John Smith',
    updatedAt: new Date(),
  },
})

// Update many
const updatedUsers = await prisma.user.updateMany({
  where: {
    status: 'DRAFT',
  },
  data: {
    status: 'PUBLISHED',
  },
})

// Delete
await prisma.user.delete({
  where: {
    id: 'user_id',
  },
})

// Delete many
await prisma.user.deleteMany({
  where: {
    status: 'INACTIVE',
  },
})
```

### Relations
```typescript
// Create with nested relation
const postWithAuthor = await prisma.post.create({
  data: {
    title: 'New Post',
    content: 'Post content',
    author: {
      create: {
        email: 'author@example.com',
        name: 'Author Name',
        password: 'hashed_password',
      },
    },
  },
})

// Include relations in queries
const postWithAuthor = await prisma.post.findUnique({
  where: {
    id: 'post_id',
  },
  include: {
    author: true,
    comments: true,
  },
})

// Nested includes
const postWithDeepRelations = await prisma.post.findUnique({
  where: {
    id: 'post_id',
  },
  include: {
    author: {
      include: {
        profile: true,
      },
    },
    comments: {
      include: {
        author: true,
      },
    },
  },
})

// Select specific fields with relations
const postWithAuthor = await prisma.post.findUnique({
  where: {
    id: 'post_id',
  },
  select: {
    id: true,
    title: true,
    author: {
      select: {
        id: true,
        name: true,
        email: true,
      },
    },
  },
})
```

### Filtering
```typescript
// String filters
const users = await prisma.user.findMany({
  where: {
    email: {
      equals: 'john@example.com',
    },
    name: {
      contains: 'John',
    },
  },
})

// Number filters
const products = await prisma.product.findMany({
  where: {
    price: {
      gt: 100,
      gte: 100,
      lt: 1000,
      lte: 1000,
    },
    quantity: {
      in: [1, 2, 3],
      notIn: [0],
    },
  },
})

// Date filters
const posts = await prisma.post.findMany({
  where: {
    createdAt: {
      gte: new Date('2024-01-01'),
      lt: new Date('2024-12-31'),
    },
  },
})

// Boolean filters
const publishedPosts = await prisma.post.findMany({
  where: {
    published: true,
  },
})

// Null filters
const usersWithProfile = await prisma.user.findMany({
  where: {
    profile: {
      isNot: null,
    },
  },
})

// Multiple conditions (AND)
const users = await prisma.user.findMany({
  where: {
    AND: [
      { email: { contains: 'example.com' } },
      { name: { startsWith: 'J' } },
    ],
  },
})

// Multiple conditions (OR)
const users = await prisma.user.findMany({
  where: {
    OR: [
      { email: 'john@example.com' },
      { email: 'jane@example.com' },
    ],
  },
})

// NOT condition
const users = await prisma.user.findMany({
  where: {
    NOT: {
      status: 'INACTIVE',
    },
  },
})
```

### Pagination
```typescript
// Basic pagination
const page = 1
const pageSize = 10

const users = await prisma.user.findMany({
  skip: (page - 1) * pageSize,
  take: pageSize,
  orderBy: {
    createdAt: 'desc',
  },
})

// Cursor-based pagination (for large datasets)
const users = await prisma.user.findMany({
  take: pageSize + 1, // Fetch one extra to check if there's a next page
  cursor: lastUserId ? { id: lastUserId } : undefined,
  orderBy: {
    id: 'asc',
  },
})

const hasNextPage = users.length > pageSize
const items = hasNextPage ? users.slice(0, -1) : users
```

## 4. Transactions

### Basic Transaction
```typescript
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function transferFunds(fromId: string, toId: string, amount: number) {
  await prisma.$transaction(async (tx) => {
    // Get sender
    const sender = await tx.user.findUnique({
      where: { id: fromId },
    })

    if (!sender || sender.balance < amount) {
      throw new Error('Insufficient funds')
    }

    // Get receiver
    const receiver = await tx.user.findUnique({
      where: { id: toId },
    })

    if (!receiver) {
      throw new Error('Receiver not found')
    }

    // Transfer funds
    await tx.user.update({
      where: { id: fromId },
      data: { balance: sender.balance - amount },
    })

    await tx.user.update({
      where: { id: toId },
      data: { balance: receiver.balance + amount },
    })

    // Create transaction record
    await tx.transaction.create({
      data: {
        fromId,
        toId,
        amount,
      },
    })
  })
}
```

### Interactive Transactions
```typescript
async function createUserWithProfile(userData: any, profileData: any) {
  return await prisma.$transaction(async (tx) => {
    const user = await tx.user.create({
      data: userData,
    })

    const profile = await tx.profile.create({
      data: {
        ...profileData,
        userId: user.id,
      },
    })

    return { user, profile }
  })
}
```

### Transaction with Isolation Level
```typescript
import { Prisma } from '@prisma/client'

const prisma = new PrismaClient()

await prisma.$transaction(
  async (tx) => {
    // Transaction logic
  },
  {
    maxWait: 5000, // Maximum time to wait for transaction
    timeout: 10000, // Maximum time for transaction
    isolationLevel: Prisma.TransactionIsolationLevel.ReadCommitted,
  }
)
```

### Batch Operations
```typescript
// Create many records
const users = await prisma.user.createMany({
  data: [
    { email: 'user1@example.com', name: 'User 1', password: 'hash1' },
    { email: 'user2@example.com', name: 'User 2', password: 'hash2' },
    { email: 'user3@example.com', name: 'User 3', password: 'hash3' },
  ],
})

// Update many records
await prisma.user.updateMany({
  where: {
    status: 'DRAFT',
  },
  data: {
    status: 'PUBLISHED',
  },
})

// Delete many records
await prisma.user.deleteMany({
  where: {
    lastLogin: {
      lt: new Date('2023-01-01'),
    },
  },
})
```

## 5. Raw Queries

### Raw SQL Queries
```typescript
// Raw select query
const users = await prisma.$queryRaw`
  SELECT * FROM users
  WHERE email LIKE ${'%' + searchTerm + '%'}
  ORDER BY created_at DESC
  LIMIT 10
`

// Raw insert query
await prisma.$executeRaw`
  INSERT INTO users (email, name, password)
  VALUES (${'john@example.com'}, ${'John Doe'}, ${'hashed_password'})
`

// Raw update query
await prisma.$executeRaw`
  UPDATE users
  SET name = ${'John Smith'}
  WHERE id = ${'user_id'}
`

// Raw delete query
await prisma.$executeRaw`
  DELETE FROM users
  WHERE last_login < ${'2023-01-01'}
`
```

### Raw Queries with Parameters
```typescript
// Using parameterized queries (safer)
const users = await prisma.$queryRaw`
  SELECT * FROM users
  WHERE email LIKE $1
  ORDER BY created_at DESC
  LIMIT $2
`, ['%' + searchTerm + '%', 10])

// Using Prisma's raw method with types
interface UserRaw {
  id: string
  email: string
  name: string | null
}

const users = await prisma.$queryRaw<UserRaw[]>`
  SELECT id, email, name FROM users
  WHERE email = $1
`, ['john@example.com'])
```

### Raw Query with Transactions
```typescript
await prisma.$transaction(async (tx) => {
  // Raw query within transaction
  await tx.$queryRaw`
    INSERT INTO users (email, name) VALUES ($1, $2)
  `, ['john@example.com', 'John Doe'])

  // Regular Prisma query
  const user = await tx.user.findUnique({
    where: { email: 'john@example.com' },
  })
})
```

## 6. Performance Optimization

### Query Optimization
```typescript
// Select only needed fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    name: true,
  },
})

// Use indexes in queries
const users = await prisma.user.findMany({
  where: {
    email: {
      startsWith: 'john',
    },
  },
})

// Limit results
const users = await prisma.user.findMany({
  take: 100,
})

// Use findFirst instead of findMany when possible
const user = await prisma.user.findFirst({
  where: {
    email: 'john@example.com',
  },
})
```

### Connection Pooling
```typescript
// prisma/schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
  // Connection pool settings
  connection_limit = 10
}
```

### Batch Operations
```typescript
// Use createMany instead of multiple create calls
const users = await prisma.user.createMany({
  data: userDataArray,
})

// Use updateMany instead of multiple update calls
await prisma.user.updateMany({
  where: {
    id: { in: userIds },
  },
  data: {
    status: 'ACTIVE',
  },
})
```

### Eager Loading vs Lazy Loading
```typescript
// Eager loading (include relations)
const postWithAuthor = await prisma.post.findUnique({
  where: { id: 'post_id' },
  include: {
    author: true,
  },
})

// Lazy loading (separate queries)
const post = await prisma.post.findUnique({
  where: { id: 'post_id' },
})

const author = post.authorId 
  ? await prisma.user.findUnique({
      where: { id: post.authorId },
    })
  : null
```

## 7. Error Handling

### Handling Known Errors
```typescript
import { Prisma } from '@prisma/client'

const prisma = new PrismaClient()

try {
  const user = await prisma.user.findUnique({
    where: { email: 'john@example.com' },
  })
} catch (error) {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    // Handle known request errors
    if (error.code === 'P2002') {
      // Unique constraint violation
      throw new Error('Email already exists')
    }
    if (error.code === 'P2025') {
      // Record not found
      throw new Error('User not found')
    }
    if (error.code === 'P2003') {
      // Foreign key constraint violation
      throw new Error('Invalid reference')
    }
  } else if (error instanceof Prisma.PrismaClientUnknownRequestError) {
    // Handle unknown request errors
    throw new Error('Database error occurred')
  } else if (error instanceof Prisma.PrismaClientRustPanicError) {
    // Handle database panic
    throw new Error('Database panic - contact support')
  } else if (error instanceof Prisma.PrismaClientInitializationError) {
    // Handle initialization errors
    throw new Error('Failed to initialize database')
  } else {
    // Handle other errors
    throw error
  }
}
```

### Error Class Wrapper
```typescript
import { Prisma } from '@prisma/client'

class DatabaseError extends Error {
  constructor(
    public code: string,
    message: string,
    public originalError?: any
  ) {
    super(message)
    this.name = this.constructor.name
  }
}

export function handlePrismaError(error: any): never {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    const errorMap: Record<string, string> = {
      P2002: 'Unique constraint violation',
      P2025: 'Record not found',
      P2003: 'Foreign key constraint violation',
      P2011: 'Null constraint violation',
    }

    throw new DatabaseError(
      error.code,
      errorMap[error.code] || 'Database error',
      error
    )
  }

  throw error
}
```

## 8. Testing with Prisma

### Unit Tests with Mocks
```typescript
// tests/user.service.test.ts
import { PrismaClient } from '@prisma/client'
import { UserService } from '../services/user.service'

jest.mock('@prisma/client')

describe('UserService', () => {
  let prisma: jest.Mocked<PrismaClient>
  let userService: UserService

  beforeEach(() => {
    prisma = new PrismaClient() as any
    prisma.user.findMany = jest.fn()
    prisma.user.findUnique = jest.fn()
    prisma.user.create = jest.fn()
    prisma.user.update = jest.fn()
    prisma.user.delete = jest.fn()
    
    userService = new UserService(prisma)
  })

  describe('findAll', () => {
    it('should return all users', async () => {
      const mockUsers = [
        { id: '1', email: 'user1@example.com', name: 'User 1' },
        { id: '2', email: 'user2@example.com', name: 'User 2' },
      ]
      prisma.user.findMany.mockResolvedValue(mockUsers)

      const users = await userService.findAll()

      expect(users).toEqual(mockUsers)
      expect(prisma.user.findMany).toHaveBeenCalledWith()
    })
  })

  describe('findById', () => {
    it('should return user when found', async () => {
      const mockUser = { id: '1', email: 'user@example.com', name: 'User' }
      prisma.user.findUnique.mockResolvedValue(mockUser)

      const user = await userService.findById('1')

      expect(user).toEqual(mockUser)
      expect(prisma.user.findUnique).toHaveBeenCalledWith({
        where: { id: '1' },
      })
    })

    it('should throw error when not found', async () => {
      prisma.user.findUnique.mockResolvedValue(null)

      await expect(userService.findById('1')).rejects.toThrow('User not found')
    })
  })
})
```

### Integration Tests with Test Database
```typescript
// tests/integration/user.test.ts
import { PrismaClient } from '@prisma/client'
import { UserService } from '../services/user.service'

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.TEST_DATABASE_URL,
    },
  },
})

describe('UserService Integration', () => {
  let userService: UserService

  beforeAll(async () => {
    // Setup test database
    await prisma.$connect()
  })

  afterAll(async () => {
    // Cleanup
    await prisma.$disconnect()
  })

  beforeEach(async () => {
    // Clean database before each test
    await prisma.user.deleteMany()
  })

  describe('create', () => {
    it('should create a new user', async () => {
      userService = new UserService(prisma)

      const userData = {
        email: 'test@example.com',
        name: 'Test User',
        password: 'hashed_password',
      }

      const user = await userService.create(userData)

      expect(user).toBeDefined()
      expect(user.email).toBe(userData.email)
      expect(user.id).toBeDefined()

      // Verify in database
      const dbUser = await prisma.user.findUnique({
        where: { id: user.id },
      })

      expect(dbUser).toEqual(user)
    })
  })
})
```

## 9. Seeding Data

### Seed Script
```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

async function main() {
  console.log('Start seeding...')

  // Seed users
  const users = await Promise.all([
    prisma.user.create({
      data: {
        email: 'admin@example.com',
        name: 'Admin User',
        password: 'hashed_password',
        role: 'ADMIN',
      },
    }),
    prisma.user.create({
      data: {
        email: 'user@example.com',
        name: 'Regular User',
        password: 'hashed_password',
        role: 'USER',
      },
    }),
  ])

  // Seed posts
  await prisma.post.createMany({
    data: users.map((user, index) => ({
      title: `Post ${index + 1}`,
      content: `Content for post ${index + 1}`,
      published: true,
      authorId: user.id,
    })),
  })

  // Seed categories
  await prisma.category.createMany({
    data: [
      { name: 'Technology' },
      { name: 'Science' },
      { name: 'Business' },
    ],
  })

  console.log('Seeding finished.')
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
```

### Seed with TypeScript Types
```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

type UserData = {
  email: string
  name: string
  password: string
}

type PostData = {
  title: string
  content: string | null
  published: boolean
  authorId: string
}

async function main() {
  const users: UserData[] = [
    {
      email: 'admin@example.com',
      name: 'Admin User',
      password: 'hashed_password',
    },
    {
      email: 'user@example.com',
      name: 'Regular User',
      password: 'hashed_password',
    },
  ]

  const createdUsers = await prisma.user.createMany({
    data: users,
  })

  const posts: PostData[] = createdUsers.map((user, index) => ({
    title: `Post ${index + 1}`,
    content: null,
    published: true,
    authorId: user.id,
  }))

  await prisma.post.createMany({
    data: posts,
  })

  console.log('Seeding completed.')
}

main()
  .catch((e) => {
    console.error(e)
    process.exit(1)
  })
  .finally(async () => {
    await prisma.$disconnect()
  })
```

## 10. Best Practices

### 1. Use Type-Safe Queries
```typescript
// Good: Use generated types
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    name: true,
  },
})

// Bad: Use any
const users: any = await prisma.user.findMany()
```

### 2. Handle Errors Properly
```typescript
// Good: Handle specific Prisma errors
try {
  await prisma.user.create({ data: userData })
} catch (error) {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    if (error.code === 'P2002') {
      throw new Error('Email already exists')
    }
  }
  throw error
}

// Bad: Generic error handling
try {
  await prisma.user.create({ data: userData })
} catch (error) {
  throw new Error('Failed to create user')
}
```

### 3. Use Transactions for Multi-Step Operations
```typescript
// Good: Use transactions for related operations
await prisma.$transaction(async (tx) => {
  const user = await tx.user.create({ data: userData })
  await tx.profile.create({ data: { ...profileData, userId: user.id } })
})

// Bad: Separate operations without transaction
const user = await prisma.user.create({ data: userData })
await prisma.profile.create({ data: { ...profileData, userId: user.id } })
// If profile creation fails, user is still created
```

### 4. Optimize Queries
```typescript
// Good: Select only needed fields
const users = await prisma.user.findMany({
  select: { id: true, email: true },
})

// Bad: Select all fields
const users = await prisma.user.findMany()
```

### 5. Use Environment Variables for Database URL
```typescript
// Good: Use environment variable
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL,
    },
  },
})

// Bad: Hardcode database URL
const prisma = new PrismaClient({
  datasources: {
    db: {
      url: 'postgresql://user:password@localhost:5432/mydb',
    },
  },
})
```

### 6. Use Indexes for Common Queries
```prisma
// Good: Add indexes for frequently queried fields
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())

  @@index([email])
  @@index([name])
  @@index([createdAt])
}

// Bad: No indexes on frequently queried fields
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String?
  createdAt DateTime @default(now())
}
```

### 7. Use Soft Deletes
```typescript
// Good: Add deletedAt field
model User {
  id        String   @id @default(cuid())
  email     String   @unique
  deletedAt DateTime?
}

// Filter out deleted records
const activeUsers = await prisma.user.findMany({
  where: {
    deletedAt: null,
  },
})

// Bad: Hard delete
await prisma.user.delete({ where: { id: userId } })
```

### 8. Use Prisma Client Singleton
```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client'

const globalForPrisma = global as unknown as {
  prisma: PrismaClient | undefined
}

export const prisma = globalForPrisma.prisma ?? new PrismaClient()

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma
}
```

### 9. Use TypeScript for Type Safety
```typescript
// Good: Use generated types
import { User, Post } from '@prisma/client'

const user: User = await prisma.user.findUnique({
  where: { id: userId },
})

// Bad: Use any
const user: any = await prisma.user.findUnique({
  where: { id: userId },
})
```

### 10. Use Select for Performance
```typescript
// Good: Select only needed fields
const users = await prisma.user.findMany({
  select: {
    id: true,
    email: true,
    name: true,
  },
})

// Bad: Get all fields
const users = await prisma.user.findMany()
```
