---
name: GraphQL Best Practices
description: Comprehensive guide to GraphQL API design, schema design, resolvers, performance optimization, and security.
---

# GraphQL Best Practices

## Overview

GraphQL is a query language for APIs that gives clients the power to ask for exactly what they need and nothing more. This guide covers best practices for designing, implementing, and optimizing GraphQL APIs.

## GraphQL Fundamentals

### Queries, Mutations, and Subscriptions

**Queries** are used to fetch data:

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
    posts {
      id
      title
    }
  }
}
```

**Mutations** are used to modify data:

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    name
    email
  }
}
```

**Subscriptions** are used for real-time updates:

```graphql
subscription OnPostCreated {
  postCreated {
    id
    title
    author {
      name
    }
  }
}
```

### Core Concepts

- **Schema**: Defines the structure of your API with types, fields, and operations
- **Resolvers**: Functions that resolve field values
- **Type System**: Strong typing with scalars, objects, enums, unions, and interfaces
- **Introspection**: Self-documenting API capabilities

## Schema Design Best Practices

### Type Design Principles

1. **Use descriptive names** that reflect business domain
2. **Keep types focused** - single responsibility
3. **Use interfaces for shared fields** across types
4. **Use unions for disjoint types** that share no common fields

```graphql
interface Node {
  id: ID!
}

type User implements Node {
  id: ID!
  name: String!
  email: String!
}

type Post implements Node {
  id: ID!
  title: String!
  content: String!
}

union SearchResult = User | Post | Comment
```

### Input Types

Use input types for complex arguments to mutations:

```graphql
input CreateUserInput {
  name: String!
  email: String!
  password: String!
  profile: UserProfileInput
}

input UserProfileInput {
  bio: String
  avatar: String
}
```

### Pagination Design

Use cursor-based pagination for better performance:

```graphql
type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type Query {
  users(first: Int, after: String): UserConnection!
}
```

### Naming Conventions

- **Types**: PascalCase (`User`, `UserProfile`)
- **Fields**: camelCase (`firstName`, `lastName`)
- **Arguments**: camelCase (`userId`, `limit`)
- **Enums**: PascalCase with SCREAMING_SNAKE_CASE values (`UserRole`, `ADMIN`)
- **Input Types**: PascalCase with `Input` suffix (`CreateUserInput`)

## Resolver Patterns and Data Fetching

### Basic Resolver Structure

```javascript
const resolvers = {
  Query: {
    user: (parent, args, context, info) => {
      return context.dataSources.userAPI.getUserById(args.id);
    },
    users: (parent, args, context, info) => {
      return context.dataSources.userAPI.getUsers(args.first, args.after);
    },
  },
  User: {
    posts: (user, args, context, info) => {
      return context.dataSources.postAPI.getPostsByUserId(user.id);
    },
    email: (user, args, context) => {
      // Only return email if user is authorized
      if (context.user.id === user.id || context.user.isAdmin) {
        return user.email;
      }
      return null;
    },
  },
};
```

### Resolver Composition

Resolvers are composed in a hierarchical manner. Each field has its own resolver, and the parent resolver passes data to child resolvers.

### Context Pattern

Use context for shared resources like data sources, authentication info, and loaders:

```javascript
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => ({
    user: req.user,
    dataSources: {
      userAPI: new UserAPI(),
      postAPI: new PostAPI(),
    },
    loaders: {
      userLoader: createUserLoader(),
    },
  }),
});
```

## N+1 Problem and DataLoader

### The N+1 Problem

The N+1 problem occurs when fetching a list of items and then making N additional queries to fetch related data for each item:

```javascript
// BAD: N+1 problem
Query: {
  users: () => db.users.findMany(),
},
User: {
  posts: (user) => db.posts.findMany({ where: { userId: user.id } }),
},
```

### DataLoader Solution

DataLoader batches and caches requests to solve the N+1 problem:

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

const resolvers = {
  User: {
    posts: async (user, args, { loaders }) => {
      return await loaders.postLoader.load(user.id);
    },
  },
};
```

### Custom DataLoader Implementation

```javascript
class PostLoader {
  constructor(db) {
    this.db = db;
    this.batch = new Map();
    this.timer = null;
  }

  load(userId) {
    return new Promise((resolve, reject) => {
      this.batch.set(userId, { resolve, reject });
      
      if (!this.timer) {
        this.timer = setTimeout(() => this.executeBatch(), 10);
      }
    });
  }

  async executeBatch() {
    const userIds = Array.from(this.batch.keys());
    const posts = await this.db.posts.findMany({
      where: { userId: { in: userIds } },
    });

    const postsByUserId = new Map();
    posts.forEach(post => {
      if (!postsByUserId.has(post.userId)) {
        postsByUserId.set(post.userId, []);
      }
      postsByUserId.get(post.userId).push(post);
    });

    this.batch.forEach(({ resolve }, userId) => {
      resolve(postsByUserId.get(userId) || []);
    });

    this.batch.clear();
    this.timer = null;
  }
}
```

## Authentication & Authorization in GraphQL

### Authentication

Authentication should happen at the HTTP level before the GraphQL request is processed:

```javascript
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import express from 'express';

const app = express();

const authMiddleware = (req, res, next) => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (token) {
    try {
      req.user = verifyToken(token);
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

### Authorization Patterns

**Field-level authorization:**

```javascript
const resolvers = {
  User: {
    email: (user, args, { user: currentUser }) => {
      if (!currentUser || (currentUser.id !== user.id && !currentUser.isAdmin)) {
        throw new AuthenticationError('Not authorized');
      }
      return user.email;
    },
  },
};
```

**Custom directive for authorization:**

```graphql
directive @auth(requires: String) on FIELD_DEFINITION

type Query {
  adminPanel: String @auth(requires: "admin")
  userProfile: String @auth(requires: "user")
}
```

```javascript
const authDirective = (schema, directiveName) => {
  return mapSchema(schema, {
    [MapperKind.FIELD]: (fieldConfig) => {
      const authDirective = getDirective(schema, fieldConfig, directiveName)?.[0];
      if (authDirective) {
        const { requires } = authDirective;
        const originalResolver = fieldConfig.resolve;
        fieldConfig.resolve = (root, args, context, info) => {
          if (!context.user || !hasRole(context.user, requires)) {
            throw new AuthenticationError(`You must be ${requires}`);
          }
          return originalResolver?.(root, args, context, info);
        };
      }
      return fieldConfig;
    },
  });
};
```

## Error Handling

### Error Format

GraphQL uses a standardized error format:

```javascript
const resolvers = {
  Query: {
    user: (_, { id }, { dataSources }) => {
      const user = dataSources.userAPI.getUserById(id);
      if (!user) {
        throw new GraphQLError('User not found', {
          extensions: {
            code: 'USER_NOT_FOUND',
            http: { status: 404 },
          },
        });
      }
      return user;
    },
  },
};
```

### Error Types

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

class ValidationError extends GraphQLError {
  constructor(message, fields) {
    super(message, {
      extensions: { code: 'VALIDATION_ERROR', fields },
    });
  }
}
```

### Error Handling Middleware

```javascript
const formatError = (error) => {
  // Log the error for debugging
  console.error(error);

  // Don't expose internal errors to clients
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

## Pagination

### Cursor-Based Pagination

Cursor-based pagination is recommended for large datasets:

```graphql
type Query {
  users(first: Int, after: String, last: Int, before: String): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}
```

**Implementation:**

```javascript
const resolvers = {
  Query: {
    users: async (_, { first, after, last, before }, { dataSources }) => {
      const limit = first || last || 10;
      const cursor = after || before;
      
      const users = await dataSources.userAPI.getUsers(limit, cursor);
      const totalCount = await dataSources.userAPI.getUserCount();
      
      const edges = users.map(user => ({
        node: user,
        cursor: toCursor(user.id),
      }));
      
      return {
        edges,
        pageInfo: {
          hasNextPage: users.length === limit,
          hasPreviousPage: !!after || !!before,
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

### Offset-Based Pagination

Offset-based pagination is simpler but less efficient for large datasets:

```graphql
type Query {
  users(limit: Int, offset: Int): [User!]!
}
```

## File Uploads

### Using GraphQL Upload Scalar

```graphql
scalar Upload

type Mutation {
  uploadFile(file: Upload!): File!
}

type File {
  id: ID!
  filename: String!
  url: String!
}
```

**Implementation:**

```javascript
import { GraphQLUpload } from 'graphql-upload';
import { createWriteStream } from 'fs';
import { join } from 'path';

const resolvers = {
  Upload: GraphQLUpload,
  Mutation: {
    uploadFile: async (_, { file }, { user }) => {
      const { createReadStream, filename, mimetype } = await file;
      
      const stream = createReadStream();
      const path = join(__dirname, 'uploads', `${Date.now()}-${filename}`);
      const writeStream = createWriteStream(path);
      
      await new Promise((resolve, reject) => {
        stream.pipe(writeStream).on('finish', resolve).on('error', reject);
      });
      
      return {
        id: generateId(),
        filename,
        url: `/uploads/${path.split('/').pop()}`,
      };
    },
  },
};
```

## Real-time Subscriptions

### WebSocket Setup

```javascript
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { makeExecutableSchema } from '@graphql-tools/schema';
import { ApolloServer } from '@apollo/server';
import { ApolloServerPluginDrainHttpServer } from '@apollo/server/plugin/drainHttpServer';

const httpServer = createServer();
const wsServer = new WebSocketServer({
  server: httpServer,
  path: '/graphql',
});

const schema = makeExecutableSchema({ typeDefs, resolvers });

const serverCleanup = useServer({ schema }, wsServer);

const server = new ApolloServer({
  schema,
  plugins: [
    ApolloServerPluginDrainHttpServer({ httpServer }),
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await serverCleanup.dispose();
          },
        };
      },
    },
  ],
});
```

### Subscription Resolvers

```graphql
type Subscription {
  postCreated: Post!
  userUpdated(userId: ID!): User!
}

type Post {
  id: ID!
  title: String!
  author: User!
}
```

```javascript
import { PubSub } from 'graphql-subscriptions';

const pubsub = new PubSub();
const POST_CREATED = 'POST_CREATED';
const USER_UPDATED = 'USER_UPDATED';

const resolvers = {
  Subscription: {
    postCreated: {
      subscribe: () => pubsub.asyncIterator([POST_CREATED]),
    },
    userUpdated: {
      subscribe: (_, { userId }) => {
        return pubsub.asyncIterator([USER_UPDATED], {
          filter: (payload) => payload.userUpdated.id === userId,
        });
      },
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

## Performance Optimization

### Query Complexity Analysis

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

### Query Depth Limiting

```javascript
import { depthLimit } from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(7)],
});
```

### Persisted Queries

```javascript
import { createPersistedQueryLink } from '@apollo/client/link/persisted-queries';
import { sha256 } from 'crypto-hash';

const persistedQueryLink = createPersistedQueryLink({
  sha256,
  generateHash: async (query) => {
    return await sha256(query);
  },
});

const server = new ApolloServer({
  typeDefs,
  resolvers,
  persistedQueries: {
    ttl: 900, // 15 minutes
  },
});
```

### Response Caching

```javascript
import responseCachePlugin from '@apollo/server-plugin-response-cache';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  plugins: [
    responseCachePlugin({
      sessionId: (requestContext) => {
        return requestContext.request.http.headers.get('session-id');
      },
    }),
  ],
});
```

### Field-Level Caching

```javascript
const resolvers = {
  Query: {
    user: async (_, { id }, { dataSources, cache }) => {
      const cacheKey = `user:${id}`;
      const cached = await cache.get(cacheKey);
      
      if (cached) {
        return JSON.parse(cached);
      }
      
      const user = await dataSources.userAPI.getUserById(id);
      await cache.set(cacheKey, JSON.stringify(user), { ttl: 300 });
      
      return user;
    },
  },
};
```

## Security Considerations

### Query Depth Limiting

Prevent deeply nested queries that could cause performance issues:

```javascript
import { depthLimit } from 'graphql-depth-limit';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [depthLimit(7)],
});
```

### Rate Limiting

Implement rate limiting at the HTTP level:

```javascript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
});

app.use('/graphql', limiter);
```

### Query Whitelisting

Only allow predefined queries in production:

```javascript
import { createPersistedQueryLink } from '@apollo/client/link/persisted-queries';

const server = new ApolloServer({
  typeDefs,
  resolvers,
  persistedQueries: {
    onlyPersisted: process.env.NODE_ENV === 'production',
  },
});
```

### Input Validation

Validate all inputs before processing:

```javascript
import { yup } from '@as-integrations/yup';
import * as yup from 'yup';

const createUserSchema = yup.object({
  input: yup.object({
    name: yup.string().min(2).max(100).required(),
    email: yup.string().email().required(),
    password: yup.string().min(8).required(),
  }),
});

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [yup(createUserSchema)],
});
```

## Apollo Server Implementation

### Basic Setup

```javascript
import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { readFileSync } from 'fs';
import { resolve } from 'path';

const typeDefs = readFileSync(
  resolve(__dirname, 'schema.graphql'),
  { encoding: 'utf-8' }
);

const resolvers = {
  Query: {
    hello: () => 'Hello world!',
  },
};

const server = new ApolloServer({
  typeDefs,
  resolvers,
});

const { url } = await startStandaloneServer(server, {
  context: async ({ req }) => ({
    user: await getUser(req.headers.authorization),
  }),
});

console.log(`🚀 Server ready at ${url}`);
```

### Data Sources Pattern

```javascript
import { RESTDataSource } from '@apollo/datasource-rest';

class UserAPI extends RESTDataSource {
  constructor() {
    super();
    this.baseURL = 'https://api.example.com/';
  }

  async getUser(id) {
    return this.get(`users/${id}`);
  }

  async getUsers(limit, cursor) {
    const params = { limit };
    if (cursor) params.cursor = cursor;
    return this.get('users', { params });
  }
}

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: () => ({
    dataSources: {
      userAPI: new UserAPI(),
    },
  }),
});
```

### Apollo Federation

**Subgraph:**

```javascript
import { ApolloServer } from '@apollo/server';
import { buildSubgraphSchema } from '@apollo/subgraph';
import { readFileSync } from 'fs';
import gql from 'graphql-tag';

const typeDefs = gql(readFileSync('schema.graphql', 'utf-8'));

const server = new ApolloServer({
  schema: buildSubgraphSchema([{ typeDefs, resolvers }]),
});
```

**Gateway:**

```javascript
import { ApolloGateway } from '@apollo/gateway';
import { ApolloServer } from '@apollo/server';

const gateway = new ApolloGateway({
  supergraphSdl: new IntrospectAndCompose({
    subgraphs: [
      { name: 'users', url: 'http://localhost:4001/graphql' },
      { name: 'posts', url: 'http://localhost:4002/graphql' },
    ],
  }),
});

const server = new ApolloServer({ gateway });
```

## Testing GraphQL APIs

### Unit Testing Resolvers

```javascript
import { resolvers } from './resolvers';

describe('User resolvers', () => {
  it('should return user by id', async () => {
    const mockUser = { id: '1', name: 'John Doe' };
    const mockDataSource = {
      userAPI: {
        getUserById: jest.fn().mockResolvedValue(mockUser),
      },
    };

    const result = await resolvers.Query.user(null, { id: '1' }, { dataSources: mockDataSource });
    
    expect(result).toEqual(mockUser);
    expect(mockDataSource.userAPI.getUserById).toHaveBeenCalledWith('1');
  });
});
```

### Integration Testing

```javascript
import { ApolloServer } from '@apollo/server';
import { executeOperation } from '@apollo/server/testing';
import { gql } from 'graphql-tag';

describe('GraphQL API', () => {
  let server;

  beforeEach(() => {
    server = new ApolloServer({ typeDefs, resolvers });
  });

  it('should fetch user with posts', async () => {
    const query = gql`
      query GetUser($id: ID!) {
        user(id: $id) {
          id
          name
          posts {
            id
            title
          }
        }
      }
    `;

    const result = await executeOperation(server, {
      query,
      variables: { id: '1' },
    });

    expect(result.body.kind).toBe('single');
    expect(result.body.singleResult.data).toBeDefined();
  });
});
```

## Best Practices Summary

1. **Schema Design**
   - Use descriptive, domain-driven type names
   - Implement cursor-based pagination for large lists
   - Use interfaces for shared fields, unions for disjoint types
   - Keep mutations focused and return modified data

2. **Performance**
   - Always use DataLoader to prevent N+1 queries
   - Implement query complexity analysis
   - Use caching strategically (field-level, response-level)
   - Consider persisted queries for production

3. **Security**
   - Authenticate at the HTTP level, authorize at the resolver level
   - Implement rate limiting and query depth limits
   - Validate all inputs
   - Use query whitelisting in production

4. **Error Handling**
   - Use custom error types with appropriate extensions
   - Log errors server-side, expose minimal info to clients
   - Implement proper HTTP status codes

5. **Testing**
   - Unit test individual resolvers
   - Integration test complete queries
   - Test error scenarios and edge cases

6. **Monitoring**
   - Track query complexity and response times
   - Monitor resolver performance
   - Log errors and warnings
   - Set up alerts for anomalies

## Related Skills

- `03-backend-api/express-rest`
- `03-backend-api/nodejs-api`
