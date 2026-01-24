---
name: MongoDB Patterns and Best Practices
description: Schema design, querying, indexing, and optimization patterns for MongoDB applications.
---

# MongoDB Patterns and Best Practices

## Overview

MongoDB is a document-oriented NoSQL database that provides high performance, high availability, and easy scalability. This skill covers schema design patterns, query optimization, indexing strategies, and best practices for building MongoDB applications.

## Prerequisites

- Understanding of NoSQL database concepts
- Knowledge of JavaScript/TypeScript
- Familiarity with document data structures
- Basic understanding of database indexing

## Key Concepts

### MongoDB Architecture

- **Document Model**: Data stored as BSON documents (JSON-like)
- **Collections**: Groups of documents (similar to tables in SQL)
- **Indexes**: B-tree indexes for efficient queries
- **Replica Sets**: High availability through replication
- **Sharding**: Horizontal scaling across multiple servers

### Schema Design Philosophy

MongoDB's flexible schema allows:
- **Embedded Documents**: Related data in a single document
- **References**: Links between documents
- **Hybrid Approach**: Combination of both
- **Schema Validation**: Enforce data structure at database level

## Implementation Guide

### Schema Design Principles

#### Denormalization for Read Performance

```typescript
// Good: Denormalize for read-heavy workloads
interface PostWithAuthor {
  _id: string
  title: string
  content: string
  authorName: string    // Denormalized for faster reads
  authorEmail: string
  createdAt: Date
}

// Bad: Always requiring joins
interface Post {
  _id: string
  title: string
  content: string
  authorId: ObjectId  // Requires join to get author info
  createdAt: Date
}
```

#### Embed vs Reference

```typescript
// Good: Embed for 1-to-few relationships
interface User {
  _id: string
  name: string
  preferences: {
    theme: 'light' | 'dark'
    notifications: boolean
  }  // Embedded - small, rarely changes
  createdAt: Date
}

// Good: Reference for 1-to-many or many-to-many
interface User {
  _id: string
  name: string
  posts: ObjectId[]  // Reference - many posts, can grow
  createdAt: Date
}

interface Post {
  _id: string
  title: string
  authorId: ObjectId  // Reference back to user
  createdAt: Date
}
```

#### Schema Versioning

```typescript
interface User {
  _id: string
  name: string
  email: string
  version: number  // Schema version
  createdAt: Date
}

// Migration strategy
async function migrateUserSchema() {
  const users = await User.find({ version: { $lt: 2 } })

  for (const user of users) {
    await User.updateOne(
      { _id: user._id },
      {
        $set: {
          'newField': 'default value',
          version: 2
        }
      }
    )
  }
}
```

### Mongoose Setup

#### Connection Configuration

```typescript
// config/database.ts
import mongoose from 'mongoose'

const MONGODB_URI = process.env.MONGODB_URI || 'mongodb://localhost:27017/myapp'

export async function connectDatabase() {
  try {
    await mongoose.connect(MONGODB_URI)
    console.log('Connected to MongoDB')
  } catch (error) {
    console.error('MongoDB connection error:', error)
    process.exit(1)
  }
}

export async function disconnectDatabase() {
  await mongoose.disconnect()
  console.log('Disconnected from MongoDB')
}
```

#### Connection Pooling

```typescript
// config/database.ts
import mongoose from 'mongoose'

const options = {
  serverSelectionTimeoutMS: 5000,
  socketTimeoutMS: 45000,
  maxPoolSize: 50,
  minPoolSize: 5,
}

export async function connectDatabase() {
  await mongoose.connect(process.env.MONGODB_URI, options)
}
```

#### Multiple Connections

```typescript
// config/database.ts
import mongoose from 'mongoose'

const connections: Record<string, mongoose.Connection> = {}

export function getConnection(name: string = 'default'): mongoose.Connection {
  if (!connections[name]) {
    connections[name] = mongoose.createConnection(name)
  }
  return connections[name]
}

export async function connectAll() {
  await Promise.all(Object.values(connections).map(conn => conn.asPromise()))
}

export async function disconnectAll() {
  await Promise.all(Object.values(connections).map(conn => conn.close()))
}
```

### Model Definitions

#### Basic Model

```typescript
// models/User.ts
import mongoose, { Document, Schema } from 'mongoose'

interface IUser {
  name: string
  email: string
  password: string
  createdAt: Date
  updatedAt: Date
}

const userSchema = new Schema<IUser>({
  name: {
    type: String,
    required: true,
    trim: true,
    minlength: 2,
    maxlength: 50
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true
  },
  password: {
    type: String,
    required: true,
    minlength: 8
  },
}, {
  timestamps: true,
})

export const User = mongoose.model<IUser>('User', userSchema)
```

#### Model with Methods

```typescript
// models/User.ts
import mongoose, { Document, Schema } from 'mongoose'

interface IUser {
  name: string
  email: string
  password: string
  comparePassword(candidatePassword: string): Promise<boolean>
}

const userSchema = new Schema<IUser>({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
})

userSchema.methods.comparePassword = async function(candidatePassword: string) {
  const bcrypt = require('bcrypt')
  return bcrypt.compare(candidatePassword, this.password)
}

export const User = mongoose.model<IUser>('User', userSchema)
```

#### Model with Virtuals

```typescript
// models/User.ts
import mongoose, { Document, Schema } from 'mongoose'

interface IUser {
  firstName: string
  lastName: string
}

const userSchema = new Schema<IUser>({
  firstName: { type: String, required: true },
  lastName: { type: String, required: true },
})

userSchema.virtual('fullName').get(function() {
  return `${this.firstName} ${this.lastName}`
})

userSchema.virtual('fullName').set(function(v) {
  const parts = v.split(' ')
  this.firstName = parts[0] || ''
  this.lastName = parts[1] || ''
})

// Include virtuals in JSON
userSchema.set('toJSON', { virtuals: true })

export const User = mongoose.model<IUser>('User', userSchema)
```

#### Model with Hooks

```typescript
// models/User.ts
import mongoose, { Schema } from 'mongoose'

const userSchema = new Schema({
  name: { type: String, required: true },
  email: { type: String, required: true },
})

// Pre-save hook
userSchema.pre('save', async function(next) {
  console.log('Saving user:', this.name)
  next()
})

// Post-save hook
userSchema.post('save', async function(doc, next) {
  console.log('User saved:', doc.name)
  next()
})

// Pre-remove hook
userSchema.pre('remove', async function(next) {
  console.log('Removing user:', this.name)
  // Cleanup related data
  await Post.deleteMany({ authorId: this._id })
  next()
})

// Post-remove hook
userSchema.post('remove', async function(doc, next) {
  console.log('User removed:', doc.name)
  next()
})

export const User = mongoose.model('User', userSchema)
```

### Query Patterns

#### Basic CRUD Operations

```typescript
// Create
const user = await User.create({
  name: 'John Doe',
  email: 'john@example.com',
  password: 'hashed_password'
})

// Read - Find all
const users = await User.find().sort({ createdAt: -1 })

// Read - Find one
const user = await User.findById(userId)

// Read - Find with conditions
const user = await User.findOne({ email: 'john@example.com' })

// Update
const updatedUser = await User.findByIdAndUpdate(
  userId,
  { name: 'John Smith' },
  { new: true }
)

// Delete
await User.findByIdAndDelete(userId)

// Delete many
await User.deleteMany({ status: 'inactive' })
```

#### Advanced Filtering

```typescript
// String queries
const users = await User.find({
  name: { $regex: /^John/i },  // Case-insensitive
  email: { $in: ['test@example.com', 'admin@example.com'] },
})

// Number queries
const products = await Product.find({
  price: { $gte: 10, $lte: 100 },
  quantity: { $gt: 0 }
})

// Date queries
const posts = await Post.find({
  createdAt: {
    $gte: new Date('2024-01-01'),
    $lte: new Date('2024-12-31')
  }
})

// Array queries
const users = await User.find({
  tags: { $all: ['admin', 'moderator'] },  // Must have all tags
  tags: { $in: ['admin'] },  // Must have at least one tag
  tags: { $size: 2 },  // Must have exactly 2 tags
})

// Logical operators
const users = await User.find({
  $or: [
    { email: 'john@example.com' },
    { name: 'John Doe' }
  ],
  $and: [
    { status: 'active' },
    { age: { $gte: 18 } }
  ]
})

// Negation
const users = await User.find({
  email: { $ne: 'admin@example.com' },  // Not equal
  status: { $ne: 'inactive' }
})
```

#### Projection

```typescript
// Select specific fields
const users = await User.find({})
  .select('name email createdAt')

// Exclude fields
const users = await User.find({})
  .select('-password -__v')

// Nested projection
const posts = await Post.find({})
  .select('title author.name author.email')
```

#### Pagination

```typescript
// Skip and limit
const page = 1
const limit = 10
const users = await User.find({})
  .skip((page - 1) * limit)
  .limit(limit)
  .sort({ createdAt: -1 })

// Get total count for pagination
const total = await User.countDocuments()
const totalPages = Math.ceil(total / limit)
```

#### Sorting

```typescript
// Single field sort
const users = await User.find({}).sort({ name: 1 })

// Multiple field sort
const users = await User.find({}).sort({ name: 1, createdAt: -1 })

// Complex sort
const users = await User.find({}).sort({
  name: 1,
  createdAt: -1,
  score: -1
})
```

### Aggregation Pipelines

#### Basic Aggregation

```typescript
// Group by and count
const result = await User.aggregate([
  {
    $group: {
      _id: '$status',
      count: { $sum: 1 }
    }
  }
])

// Average calculation
const result = await Product.aggregate([
  {
    $group: {
      _id: '$category',
      avgPrice: { $avg: '$price' }
    }
  }
])
```

#### Lookup and Unwind

```typescript
// Join users with their posts
const result = await User.aggregate([
  {
    $lookup: {
      from: 'posts',
      localField: '_id',
      foreignField: 'authorId',
      as: 'userPosts'
    }
  },
  {
    $unwind: '$userPosts'
  }
])
```

#### Faceted Search

```typescript
// Multi-faceted search with counts
const result = await Product.aggregate([
  {
    $match: {
      category: category,
      price: { $gte: minPrice, $lte: maxPrice },
      tags: { $in: selectedTags }
    }
  },
  {
    $facet: {
      categories: [
        { $group: { _id: '$category' } },
        { $group: { _id: '$brand' } }
      ],
      priceRanges: [
        {
          $bucketAuto: {
            buckets: [
              { to: 50, label: 'Under $50' },
              { from: 50, to: 100, label: '$50 - $100' },
              { from: 100, to: 200, label: '$100 - $200' },
              { from: 200, label: 'Over $200' }
            ],
            outputPath: 'price'
          }
        }
      ]
    }
  }
])
```

#### Time Series Aggregation

```typescript
// Daily aggregation
const result = await Order.aggregate([
  {
    $match: {
      createdAt: {
        $gte: new Date('2024-01-01'),
        $lte: new Date('2024-01-31')
      }
    }
  },
  {
    $group: {
      _id: {
        year: { $year: '$createdAt' },
        month: { $month: '$createdAt' },
        day: { $dayOfMonth: '$createdAt' }
      },
      totalSales: { $sum: '$total' },
      avgOrderValue: { $avg: '$total' }
    }
  },
  {
    $sort: {
      '_id.year': 1,
      '_id.month': 1,
      '_id.day': 1
    }
  }
])
```

#### Pipeline with Multiple Stages

```typescript
const result = await Order.aggregate([
  // Stage 1: Match documents
  {
    $match: {
      status: 'completed'
    }
  },
  // Stage 2: Group by user
  {
    $group: {
      _id: '$userId',
      totalSpent: { $sum: '$total' },
      orderCount: { $sum: 1 }
    }
  },
  // Stage 3: Sort by total spent
  {
    $sort: { totalSpent: -1 }
  },
  // Stage 4: Limit results
  {
    $limit: 10
  }
])
```

### Indexing Strategies

#### Single Field Indexes

```typescript
// models/User.ts
import mongoose, { Schema } from 'mongoose'

const userSchema = new Schema({
  email: { type: String, unique: true, index: true },
  name: { type: String, index: true },
  createdAt: { type: Date, index: true }
})
```

#### Compound Indexes

```typescript
// models/Product.ts
import mongoose, { Schema } from 'mongoose'

const productSchema = new Schema({
  name: { type: String },
  category: { type: String },
  price: { type: Number },
  stock: { type: Number },
})

// Compound index for category + price
productSchema.index({ category: 1, price: -1 })

// Compound index for stock + category
productSchema.index({ stock: 1, category: 1 })
```

#### Text Indexes

```typescript
// models/Article.ts
import mongoose, { Schema } from 'mongoose'

const articleSchema = new Schema({
  title: { type: String },
  content: { type: String },
  tags: [String],
})

// Text index for full-text search
articleSchema.index({ title: 'text', content: 'text' })

// Text index for tags
articleSchema.index({ tags: 1 })
```

#### Geospatial Indexes

```typescript
// models/Location.ts
import mongoose, { Schema } from 'mongoose'

const locationSchema = new Schema({
  name: { type: String },
  location: {
    type: {
      type: 'Point',
      coordinates: [Number]
    },
    index: '2dsphere'
  }
})
```

#### TTL Indexes

```typescript
// models/Session.ts
import mongoose, { Schema } from 'mongoose'

const sessionSchema = new Schema({
  userId: { type: String },
  token: { type: String },
  expiresAt: { type: Date, index: { expiresAt: 1 } }
})

// TTL index for automatic expiration
sessionSchema.index({ expiresAt: 1 }, { expireAfterSeconds: 3600 })
```

### Transactions

#### Basic Transaction

```typescript
import mongoose from 'mongoose'

const session = await mongoose.startSession()

try {
  const user = await User.create([{ name: 'John' }], { session })
  const order = await Order.create([
    { userId: user[0]._id, total: 100 }
  ], { session })

  await session.commitTransaction()
  console.log('Transaction committed')
} catch (error) {
  await session.abortTransaction()
  console.error('Transaction aborted:', error)
}
```

#### Transaction with Multiple Operations

```typescript
const session = await mongoose.startSession()

try {
  // Create user
  const user = await User.create([{ name: 'John' }], { session })

  // Create posts
  await Order.create([
    { title: 'Post 1', authorId: user[0]._id },
    { title: 'Post 2', authorId: user[0]._id }
  ], { session })

  // Update user stats
  await User.findByIdAndUpdate(
    user[0]._id,
    { postCount: 2 },
    { session }
  )

  await session.commitTransaction()
} catch (error) {
  await session.abortTransaction()
  throw error
}
```

#### Transaction with Error Handling

```typescript
async function transferFunds(fromId: string, toId: string, amount: number) {
  const session = await mongoose.startSession()

  try {
    // Get both users
    const [fromUser, toUser] = await User.find({
      _id: { $in: [fromId, toId] }
    }).session(session)

    if (!fromUser || !toUser) {
      throw new Error('User not found')
    }

    if (fromUser.balance < amount) {
      throw new Error('Insufficient funds')
    }

    // Transfer funds
    await User.findByIdAndUpdate(
      fromId,
      { $inc: { balance: -amount } },
      { session }
    )

    await User.findByIdAndUpdate(
      toId,
      { $inc: { balance: amount } },
      { session }
    )

    // Create transaction record
    await Transaction.create([
      { fromId, toId, amount, type: 'transfer' }
    ], { session })

    await session.commitTransaction()
    return { success: true }
  } catch (error) {
    await session.abortTransaction()
    throw error
  }
}
```

### Change Streams

#### Watching for Changes

```typescript
// models/User.ts
import mongoose, { Schema } from 'mongoose'

const userSchema = new Schema({
  name: { type: String },
  email: { type: String },
  status: { type: String, enum: ['active', 'inactive'] }
})

// Watch for changes
const changeStream = User.watch()

changeStream.on('change', (change) => {
  console.log('Change detected:', change)

  switch (change.operationType) {
    case 'insert':
      console.log('New user:', change.fullDocument)
      break
    case 'update':
      console.log('User updated:', change.fullDocument)
      break
    case 'delete':
      console.log('User deleted:', change.documentKey)
      break
  }
})
```

#### Change Stream with Pipeline

```typescript
const userChangeStream = User.watch()

userChangeStream.on('change', async (change) => {
  if (change.operationType === 'update') {
    // Get related data
    const posts = await Post.find({ authorId: change.documentKey })

    // Update denormalized data in posts
    await Post.updateMany(
      { authorId: change.documentKey },
      { $set: { authorName: change.fullDocument.name } }
    )
  }
})
```

#### Aggregation Change Stream

```typescript
const changeStream = User.watch()

changeStream.on('change', async (change) => {
  // Aggregate statistics on change
  const stats = await User.aggregate([
    { $group: { _id: '$status', count: { $sum: 1 } }
  ])

  console.log('Updated stats:', stats)
})
```

### Performance Optimization

#### Query Optimization

```typescript
// Good: Use lean() for read-only operations
const users = await User.find({}).lean()

// Bad: Get full documents when not needed
const users = await User.find({})

// Good: Select only needed fields
const users = await User.find({})
  .select('name email')

// Bad: Get all fields
const users = await User.find({})
```

#### Projection for Large Documents

```typescript
// Good: Use projection for large documents
const posts = await Post.find({})
  .select('title createdAt author.name')

// Bad: Fetch entire document
const posts = await Post.find({})
```

#### Cursor-based Pagination

```typescript
// Good: Use cursor for large datasets
const users = await User.find({})
  .sort({ _id: 1 })
  .cursor()

// Bad: Skip/limit for large datasets
const users = await User.find({})
  .skip(1000)
  .limit(100)
```

#### Bulk Operations

```typescript
// Good: Use bulk operations for inserts
const users = await User.insertMany([
  { name: 'User 1', email: 'user1@example.com' },
  { name: 'User 2', email: 'user2@example.com' },
  { name: 'User 3', email: 'user3@example.com' },
])

// Bad: Multiple individual inserts
for (const userData of userDataArray) {
  await User.create(userData)
}
```

#### Index Usage

```typescript
// Good: Ensure indexes exist for query fields
const users = await User.find({ email: 'john@example.com' })
// Email has unique index

const products = await Product.find({
  category: 'electronics',
  price: { $gte: 100, $lte: 500 }
})
// Category and price have compound index
```

### Data Validation

#### Schema Validation

```typescript
// models/User.ts
import mongoose, { Schema } from 'mongoose'

const userSchema = new Schema({
  name: {
    type: String,
    required: [true, 'Name is required'],
    minlength: 2,
    maxlength: 50
  },
  email: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    lowercase: true,
    validate: {
      validator: (v: string) => /^[^\w-\.]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,}$/.test(v),
      message: 'Invalid email format'
    }
  },
  age: {
    type: Number,
    min: 18,
    max: 120,
    validate: {
      validator: (v: number) => Number.isInteger(v) && v >= 18,
      message: 'Age must be an integer >= 18'
    }
  }
})
```

#### Custom Validators

```typescript
// validators/password.validator.ts
import { Schema } from 'mongoose'

export const passwordValidator = {
  validator: (v: string) => {
    if (v.length < 8) {
      return false
    }
    if (!/[A-Z]/.test(v)) {
      return false
    }
    if (!/[a-z]/.test(v)) {
      return false
    }
    if (!/[0-9]/.test(v)) {
      return false
    }
    return true
  },
  message: 'Password must contain uppercase, lowercase, and numbers'
}

// Usage in schema
const userSchema = new Schema({
  password: {
    type: String,
    required: true,
    validate: passwordValidator
  }
})
```

#### Async Validation

```typescript
// validators/unique.validator.ts
import { Schema } from 'mongoose'

export const uniqueEmailValidator = {
  validator: async (v: string) => {
    const user = await User.findOne({ email: v })
    return !user
  },
  message: 'Email already exists'
}

// Usage in schema
const userSchema = new Schema({
  email: {
    type: String,
    required: true,
    unique: true,
    validate: uniqueEmailValidator
  }
})
```

## Best Practices

1. **Schema Design**
   - Use embedding for 1-to-few relationships
   - Use references for 1-to-many or many-to-many
   - Implement schema versioning
   - Denormalize for read-heavy workloads

2. **Query Optimization**
   - Use lean() for read-only operations
   - Select only needed fields
   - Use appropriate indexes
   - Avoid large result sets

3. **Indexing Strategy**
   - Create indexes on frequently queried fields
   - Use compound indexes for multi-field queries
   - Monitor and remove unused indexes
   - Consider TTL indexes for time-based data

4. **Performance**
   - Use connection pooling
   - Implement pagination for large datasets
   - Use bulk operations when appropriate
   - Monitor query performance

5. **Data Integrity**
   - Implement schema validation
   - Use transactions for multi-document operations
   - Handle write conflicts gracefully
   - Implement proper error handling

6. **Change Streams**
   - Use change streams for real-time updates
   - Implement proper error handling
   - Consider aggregation for statistics
   - Handle reconnection scenarios

## Related Skills

- [`04-database/database-optimization`](04-database/database-optimization/SKILL.md)
- [`04-database/redis-caching`](04-database/redis-caching/SKILL.md)
- [`04-database/vector-database`](04-database/vector-database/SKILL.md)
