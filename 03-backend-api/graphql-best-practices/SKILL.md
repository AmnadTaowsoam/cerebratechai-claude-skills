# GraphQL Best Practices

---

## 1. Executive Summary & Strategic Necessity

### 1.1 Context (ภาษาไทย)

GraphQL เป็น query language สำหรับ APIs ที่ให้ clients มี power ที่ ask for exactly what they need และ nothing more โดยใช้ strong typing system และ self-documenting capabilities

GraphQL ประกอบด้วย:
- **Query Language** - Query language สำหรับ fetching data
- **Schema-First** - Schema-driven development approach
- **Strong Typing** - Built-in type system และ validation
- **Introspection** - Self-documenting API capabilities
- **Real-Time** - Built-in subscription support สำหรับ real-time updates
- **Flexible** - Client can request exactly what they need

### 1.2 Business Impact (ภาษาไทย)

**ผลกระทบทางธุรกิจ:**

1. **ลด Over-Fetching** - GraphQL ช่วยลด over-fetching ได้ถึง 30-50%
2. **เพิ่ม Performance** - ลด round-trips และ data transfer
3. **เพิ่ม Developer Experience** - Self-documenting ช่วยเพิ่ม DX
4. **ลด Bandwidth** - ลด data transfer ด้วย precise queries
5. **ปรับปรุง Type Safety** - Built-in validation ช่วยเพิ่ม type safety

### 1.3 Product Thinking (ภาษาไทย)

**มุมมองด้านผลิตภัณฑ์:**

1. **Query-First** - GraphQL ต้อง query-first design
2. **Schema-Driven** - Schema ต้อง drive development
3. **Type-Safe** - APIs ต้อง type-safe ด้วย GraphQL types
4. **Introspectable** - APIs ต้อง self-documenting
5. **Real-Time** - APIs ต้อง support real-time updates

---

## 2. Technical Deep Dive (The "How-to")

### 2.1 Core Logic

GraphQL ประกอบด้วย:

1. **Schema** - Defines structure of API with types, fields, and operations
2. **Resolvers** - Functions that resolve field values
3. **Type System** - Strong typing with scalars, objects, enums, unions, and interfaces
4. **Introspection** - Self-documenting API capabilities
5. **Query Language** - Query language สำหรับ fetching data
6. **Mutations** - Operations สำหรับ modifying data
7. **Subscriptions** - Real-time updates via WebSocket

### 2.2 Architecture Diagram Requirements

```
┌─────────────────────────────────────────────────────────┐
│              GraphQL Architecture                        │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Client Layer                         │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │  Browser    │  │  Mobile     │  │  API Client│  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              GraphQL Server Layer                  │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │   Query     │  │  Mutation   │  │Subscription│  │  │
│  │  │  Executor   │  │  Executor   │  │  Executor  │  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  │                           │                              │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │         Resolver Layer                      │  │  │
│  │  │  ┌─────────┐  ┌─────────┐  ┌─────────────┐  │  │  │
│  │  │  │Schema   │  │Context  │  │DataLoaders  │  │  │  │
│  │  │  └─────────┘  └─────────┘  └─────────────┘  │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
│                           │                              │
│                           ▼                              │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Data Sources Layer                    │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌───────────┐  │  │
│  │  │  Database   │  │  REST API   │  │  External  │  │  │
│  │  │             │  │             │  │  Services  │  │  │
│  │  └─────────────┘  └─────────────┘  └───────────┘  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### 2.3 Implementation Workflow

1. **Schema Design** - Define types, queries, mutations, and subscriptions
2. **Resolver Implementation** - Implement resolver functions for each field
3. **Context Setup** - Configure context with data sources and loaders
4. **Middleware Integration** - Add authentication, authorization, and logging
5. **Performance Optimization** - Implement DataLoader, caching, and query analysis
6. **Testing** - Write unit and integration tests
7. **Documentation** - Generate API documentation from schema

---

## 3. Tooling & Tech Stack

### 3.1 Enterprise Tools

| Tool | Purpose | Enterprise Features |
|------|---------|---------------------|
| Apollo Server | Production-ready GraphQL server | Federation, caching, metrics |
| GraphQL Yoga | Lightweight GraphQL server | Fast startup, plugins |
| GraphQL Code Generator | Type-safe client code | TypeScript generation |
| Apollo Studio | GraphQL observability | Tracing, schema checks |
| GraphQL Inspector | Schema validation | Breaking change detection |

### 3.2 Configuration Essentials

```javascript
// apollo-server.config.js
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { readFileSync } from 'fs';

const typeDefs = readFileSync('./schema.graphql', 'utf-8');

const resolvers = {
  Query: {
    hello: () => 'Hello world!',
  },
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  introspection: true,
  csrfPrevention: true,
});

const { url } = await startStandaloneServer(server, {
  context: async ({ req }) => ({
    user: await authenticateUser(req),
  }),
});

console.log(`🚀 Server ready at ${url}`);
```

---

## 4. Standards, Compliance & Security

### 4.1 International Standards

- **GraphQL Specification** - Follow official GraphQL spec
- **OpenAPI Integration** - Map GraphQL to REST for legacy systems
- **ISO 27001** - Security management for GraphQL APIs
- **GDPR Compliance** - Data privacy in GraphQL queries

### 4.2 Security Protocol

1. **Query Depth Limiting** - Prevent deep nested queries
2. **Query Complexity Analysis** - Limit query complexity
3. **Rate Limiting** - Implement per-IP rate limits
4. **Input Validation** - Validate all inputs
5. **Authentication** - JWT-based authentication
6. **Authorization** - Field-level authorization
7. **Query Whitelisting** - Only allow predefined queries in production

### 4.3 Explainability

- **Schema Documentation** - Document all types and fields
- **Error Messages** - Provide clear, actionable error messages
- **Query Tracing** - Track query execution for debugging
- **Logging** - Log all queries and mutations

---

## 5. Unit Economics & Performance Metrics (KPIs)

### 5.1 Cost Calculation

```
Total Cost = (Server Cost) + (Database Cost) + (Bandwidth Cost)

Server Cost = (Instance Hours × Hourly Rate)
Database Cost = (Query Count × Cost Per Query)
Bandwidth Cost = (Data Transfer × Cost Per GB)

GraphQL Optimization Savings:
- Over-fetching reduction: 30-50%
- Under-fetching elimination: 100%
- Round-trip reduction: 50-70%
```

### 5.2 Key Performance Indicators

| Metric | Target | Measurement |
|--------|--------|-------------|
| Query Response Time | < 200ms | p95 latency |
| Mutation Response Time | < 500ms | p95 latency |
| Error Rate | < 0.1% | Total errors / Total requests |
| Cache Hit Rate | > 80% | Cache hits / Total queries |
| Query Complexity | < 1000 | Complexity score |
| Concurrent Connections | > 1000 | Active connections |

---

## 6. Strategic Recommendations (CTO Insights)

### 6.1 Phase Rollout

**Phase 1: Foundation (Weeks 1-2)**
- Set up basic GraphQL server
- Define initial schema
- Implement core resolvers

**Phase 2: Integration (Weeks 3-4)**
- Integrate with data sources
- Implement DataLoader
- Add authentication

**Phase 3: Optimization (Weeks 5-6)**
- Implement caching
- Add query analysis
- Performance tuning

**Phase 4: Production (Weeks 7-8)**
- Deploy to production
- Set up monitoring
- Documentation

### 6.2 Pitfalls to Avoid

1. **N+1 Query Problem** - Always use DataLoader for nested queries
2. **Over-Exposing Data** - Limit exposed fields and types
3. **Ignoring Caching** - Implement caching at multiple levels
4. **Poor Error Handling** - Provide meaningful error messages
5. **No Rate Limiting** - Implement rate limiting to prevent abuse
6. **Complex Mutations** - Keep mutations simple and focused
7. **No Monitoring** - Monitor query performance and errors

### 6.3 Best Practices Checklist

- [ ] Use cursor-based pagination for large lists
- [ ] Implement DataLoader for nested queries
- [ ] Add query depth limiting
- [ ] Implement query complexity analysis
- [ ] Use field-level caching
- [ ] Add authentication and authorization
- [ ] Implement error handling middleware
- [ ] Set up monitoring and logging
- [ ] Document schema with descriptions
- [ ] Use persisted queries in production
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Use TypeScript for type safety
- [ ] Test resolvers with unit tests
- [ ] Monitor query performance

---

## 7. Implementation Examples

### 7.1 Basic Query and Mutation

```graphql
# Query to fetch user with posts
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
    posts {
      id
      title
      content
    }
  }
}

# Mutation to create a user
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}
```

### 7.2 Schema Definition

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
}

input CreateUserInput {
  name: String!
  email: String!
  password: String!
}

type Query {
  user(id: ID!): User
  users: [User!]!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}
```

### 7.3 Resolver Implementation

```javascript
import DataLoader from 'dataloader';

const userLoader = new DataLoader(async (ids) => {
  const users = await db.users.findMany({
    where: { id: { in: ids } },
  });
  const userMap = new Map(users.map(u => [u.id, u]));
  return ids.map(id => userMap.get(id));
});

const resolvers = {
  Query: {
    user: async (_, { id }, { dataSources }) => {
      return await dataSources.userAPI.getUserById(id);
    },
    users: async (_, __, { dataSources }) => {
      return await dataSources.userAPI.getUsers();
    },
  },
  Mutation: {
    createUser: async (_, { input }, { dataSources }) => {
      return await dataSources.userAPI.createUser(input);
    },
  },
  User: {
    posts: async (user, _, { dataSources }) => {
      return await dataSources.postAPI.getPostsByUserId(user.id);
    },
  },
  Post: {
    author: async (post, _, { loaders }) => {
      return await loaders.userLoader.load(post.authorId);
    },
  },
};
```

### 7.4 DataLoader for N+1 Problem

```javascript
import DataLoader from 'dataloader';

const createUserLoader = () => {
  return new DataLoader(async (userIds) => {
    const users = await db.users.findMany({
      where: { id: { in: userIds } },
    });
    const userMap = new Map(users.map(u => [u.id, u]));
    return userIds.map(id => userMap.get(id));
  });
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: () => ({
    loaders: {
      user: createUserLoader(),
      post: createPostLoader(),
    },
  }),
});
```

### 7.5 Authentication Middleware

```javascript
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import express from 'express';
import jwt from 'jsonwebtoken';

const app = express();

const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (token) {
    try {
      req.user = jwt.verify(token, process.env.JWT_SECRET);
    } catch (error) {
      req.user = null;
    }
  }
  next();
};

app.use(authMiddleware);

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => ({
    user: req.user,
  }),
});

await server.start();
app.use('/graphql', expressMiddleware(server));
```

### 7.6 Field-Level Authorization

```javascript
const resolvers = {
  User: {
    email: (user, _, { user: currentUser }) => {
      if (!currentUser || (currentUser.id !== user.id && !currentUser.isAdmin)) {
        throw new AuthenticationError('Not authorized');
      }
      return user.email;
    },
  },
  Query: {
    adminPanel: (_, __, { user }) => {
      if (!user || !user.isAdmin) {
        throw new ForbiddenError('Admin access required');
      }
      return 'Admin panel data';
    },
  },
};
```

### 7.7 Query Complexity Analysis

```javascript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const complexityLimitRule = createComplexityLimitRule(1000, {
  onCost: (cost) => console.log(`Query complexity: ${cost}`),
});

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [complexityLimitRule],
});
```

### 7.8 Cursor-Based Pagination

```graphql
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type UserEdge {
  node: User!
  cursor: String!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type Query {
  users(first: Int, after: String): UserConnection!
}
```

```javascript
const resolvers = {
  Query: {
    users: async (_, { first, after }, { dataSources }) => {
      const limit = first || 10;
      const users = await dataSources.userAPI.getUsers(limit, after);
      const totalCount = await dataSources.userAPI.getUserCount();
      
      const edges = users.map(user => ({
        node: user,
        cursor: toCursor(user.id),
      }));
      
      return {
        edges,
        pageInfo: {
          hasNextPage: users.length === limit,
          hasPreviousPage: !!after,
          startCursor: edges[0]?.cursor,
          endCursor: edges[edges.length - 1]?.cursor,
        },
        totalCount,
      };
    },
  },
};

function toCursor(id) {
  return Buffer.from(id.toString()).toString('base64');
}
```

### 7.9 Subscriptions for Real-Time Updates

```javascript
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();
const POST_CREATED = 'POST_CREATED';

const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

useServer({ schema }, wsServer);

const resolvers = {
  Subscription: {
    postCreated: {
      subscribe: () => pubsub.asyncIterator([POST_CREATED]),
    },
  },
  Mutation: {
    createPost: async (_, { input }, { dataSources }) => {
      const post = await dataSources.postAPI.createPost(input);
      pubsub.publish(POST_CREATED, { postCreated: post });
      return post;
    },
  },
};
```

### 7.10 Error Handling

```javascript
import { GraphQLError } from 'graphql';

class AuthenticationError extends GraphQLError {
  constructor(message) {
    super(message, {
      extensions: { code: 'AUTHENTICATION_ERROR' },
    });
  }
}

class ForbiddenError extends GraphQLError {
  constructor(message) {
    super(message, {
      extensions: { code: 'FORBIDDEN' },
    });
  }
}

const formatError = (error) => {
  console.error(error);
  
  if (error.extensions?.code === 'INTERNAL_SERVER_ERROR') {
    return new GraphQLError('An unexpected error occurred');
  }
  
  return error;
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
  formatError,
});
```

---

## 8. Related Skills

- [`03-backend-api/express-rest`](03-backend-api/express-rest/SKILL.md)
- [`03-backend-api/nodejs-api`](03-backend-api/nodejs-api/SKILL.md)
- [`03-backend-api/error-handling`](03-backend-api/error-handling/SKILL.md)
- [`03-backend-api/middleware`](03-backend-api/middleware/SKILL.md)
- [`03-backend-api/validation`](03-backend-api/validation/SKILL.md)
- [`04-database/database-optimization`](04-database/database-optimization/SKILL.md)
- [`04-database/connection-pooling`](04-database/connection-pooling/SKILL.md)
