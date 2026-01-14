# Service Design

## Overview

Comprehensive guide to microservice design principles and best practices for building scalable distributed systems.

## Table of Contents

1. [Microservice Principles](#microservice-principles)
2. [Service Boundaries](#service-boundaries)
3. [Domain-Driven Design](#domain-driven-design)
4. [API Design](#api-design)
5. [Data Management](#data-management)
6. [Communication Patterns](#communication-patterns)
7. [Service Discovery](#service-discovery)
8. [Configuration Management](#configuration-management)
9. [Logging and Tracing](#logging-and-tracing)
10. [Testing Strategies](#testing-strategies)
11. [Common Anti-Patterns](#common-anti-patterns)
12. [Best Practices](#best-practices)

---

## Microservice Principles

### Core Principles

```markdown
## Microservice Principles

### Single Responsibility
- Each service should have one business capability
- Focused on a specific domain
- Easy to understand and maintain

### Decentralized Governance
- Services own their data and logic
- Independent technology choices
- Autonomous deployment

### Failure Isolation
- Services fail independently
- Circuit breakers prevent cascading failures
- Graceful degradation

### Scalability
- Services scale independently
- Horizontal scaling preferred
- Resource optimization per service

### Observability
- Services are observable
- Metrics, logs, and traces
- Health checks and monitoring
```

### Service Definition

```typescript
// service-interface.ts
export interface Microservice {
  name: string;
  version: string;
  description: string;
  capabilities: string[];
  dependencies: string[];
  endpoints: ServiceEndpoint[];
  healthCheck: HealthCheck;
}

export interface ServiceEndpoint {
  path: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';
  description: string;
  authRequired: boolean;
  rateLimit?: number;
}

export interface HealthCheck {
  path: string;
  interval: number; // seconds
  timeout: number; // seconds
}

// Example service definition
export const UserService: Microservice = {
  name: 'user-service',
  version: '1.0.0',
  description: 'Manages user accounts and profiles',
  capabilities: [
    'user-registration',
    'user-authentication',
    'profile-management',
    'password-reset'
  ],
  dependencies: [
    'database',
    'cache',
    'notification-service'
  ],
  endpoints: [
    {
      path: '/api/users',
      method: 'GET',
      description: 'List users',
      authRequired: true,
      rateLimit: 100
    },
    {
      path: '/api/users/:id',
      method: 'GET',
      description: 'Get user by ID',
      authRequired: true,
      rateLimit: 1000
    }
  ],
  healthCheck: {
    path: '/health',
    interval: 30,
    timeout: 5
  }
};
```

---

## Service Boundaries

### Bounded Contexts

```typescript
// bounded-contexts.ts
export interface BoundedContext {
  name: string;
  domain: string;
  entities: string[];
  valueObjects: string[];
  aggregates: string[];
  services: string[];
}

// Example bounded contexts
export const UserContext: BoundedContext = {
  name: 'User Management',
  domain: 'Identity',
  entities: ['User', 'Profile', 'Credential'],
  valueObjects: ['Email', 'PhoneNumber', 'Address'],
  aggregates: ['UserAggregate'],
  services: ['UserService', 'AuthService', 'ProfileService']
};

export const OrderContext: BoundedContext = {
  name: 'Order Management',
  domain: 'Commerce',
  entities: ['Order', 'OrderItem', 'Payment'],
  valueObjects: ['Money', 'Quantity', 'OrderStatus'],
  aggregates: ['OrderAggregate'],
  services: ['OrderService', 'PaymentService', 'InventoryService']
};

export const ProductContext: BoundedContext = {
  name: 'Product Catalog',
  domain: 'Commerce',
  entities: ['Product', 'Category', 'Review'],
  valueObjects: ['Price', 'Rating', 'ProductInfo'],
  aggregates: ['ProductAggregate'],
  services: ['ProductService', 'CategoryService', 'ReviewService']
};
```

### Service Boundary Identification

```typescript
// service-boundary-analyzer.ts
export interface ServiceBoundary {
  name: string;
  reason: string;
  businessCapability: string;
  dataOwnership: string[];
  apiContracts: string[];
}

export class ServiceBoundaryAnalyzer {
  static analyzeDomain(domain: string): ServiceBoundary[] {
    const boundaries: ServiceBoundary[] = [];
    
    // Identify business capabilities
    const capabilities = this.identifyCapabilities(domain);
    
    // Group related capabilities
    const groups = this.groupCapabilities(capabilities);
    
    // Create service boundaries
    for (const group of groups) {
      boundaries.push({
        name: this.generateServiceName(group),
        reason: this.justifyBoundary(group),
        businessCapability: group.capability,
        dataOwnership: group.entities,
        apiContracts: group.contracts
      });
    }
    
    return boundaries;
  }
  
  private static identifyCapabilities(domain: string): any[] {
    // Implementation
    return [];
  }
  
  private static groupCapabilities(capabilities: any[]): any[] {
    // Implementation
    return [];
  }
  
  private static generateServiceName(group: any): string {
    // Implementation
    return '';
  }
  
  private static justifyBoundary(group: any): string {
    // Implementation
    return '';
  }
}
```

---

## Domain-Driven Design

### Aggregates

```typescript
// aggregates.ts
export interface AggregateRoot {
  id: string;
  version: number;
  createdAt: Date;
  updatedAt: Date;
}

export class UserAggregate implements AggregateRoot {
  id: string;
  version: number;
  createdAt: Date;
  updatedAt: Date;
  
  private email: string;
  private passwordHash: string;
  private profile: Profile;
  
  constructor(data: any) {
    this.id = data.id;
    this.version = data.version || 0;
    this.createdAt = data.createdAt || new Date();
    this.updatedAt = data.updatedAt || new Date();
    this.email = data.email;
    this.passwordHash = data.passwordHash;
    this.profile = data.profile;
  }
  
  changeEmail(newEmail: string): void {
    if (!this.isValidEmail(newEmail)) {
      throw new Error('Invalid email format');
    }
    this.email = newEmail;
    this.updatedAt = new Date();
    this.version++;
  }
  
  updateProfile(profile: Partial<Profile>): void {
    this.profile = { ...this.profile, ...profile };
    this.updatedAt = new Date();
    this.version++;
  }
  
  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}

export interface Profile {
  firstName: string;
  lastName: string;
  dateOfBirth?: Date;
  address?: Address;
}

export interface Address {
  street: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
}
```

### Domain Events

```typescript
// domain-events.ts
export interface DomainEvent {
  eventType: string;
  aggregateId: string;
  aggregateType: string;
  occurredAt: Date;
  data: any;
}

export class UserCreatedEvent implements DomainEvent {
  eventType = 'UserCreated';
  aggregateId: string;
  aggregateType = 'User';
  occurredAt: Date;
  data: any;
  
  constructor(userId: string, email: string) {
    this.aggregateId = userId;
    this.occurredAt = new Date();
    this.data = { userId, email };
  }
}

export class EmailChangedEvent implements DomainEvent {
  eventType = 'EmailChanged';
  aggregateId: string;
  aggregateType = 'User';
  occurredAt: Date;
  data: any;
  
  constructor(userId: string, oldEmail: string, newEmail: string) {
    this.aggregateId = userId;
    this.occurredAt = new Date();
    this.data = { userId, oldEmail, newEmail };
  }
}

export class EventPublisher {
  private eventHandlers: Map<string, Function[]> = new Map();
  
  subscribe(eventType: string, handler: Function): void {
    if (!this.eventHandlers.has(eventType)) {
      this.eventHandlers.set(eventType, []);
    }
    this.eventHandlers.get(eventType)!.push(handler);
  }
  
  publish(event: DomainEvent): void {
    const handlers = this.eventHandlers.get(event.eventType) || [];
    for (const handler of handlers) {
      handler(event);
    }
  }
}
```

---

## API Design

### REST API Design

```typescript
// rest-api.ts
import express from 'express';
import { UserService } from './user-service';

export class UserAPI {
  private app: express.Application;
  private userService: UserService;
  
  constructor() {
    this.app = express();
    this.userService = new UserService();
    this.setupRoutes();
  }
  
  private setupRoutes(): void {
    // List users with pagination
    this.app.get('/api/users', async (req, res) => {
      const page = parseInt(req.query.page as string) || 1;
      const limit = parseInt(req.query.limit as string) || 10;
      
      const result = await this.userService.listUsers(page, limit);
      
      res.json({
        data: result.users,
        pagination: {
          page,
          limit,
          total: result.total,
          totalPages: Math.ceil(result.total / limit)
        }
      });
    });
    
    // Get user by ID
    this.app.get('/api/users/:id', async (req, res) => {
      const user = await this.userService.getUserById(req.params.id);
      
      if (!user) {
        return res.status(404).json({ error: 'User not found' });
      }
      
      res.json(user);
    });
    
    // Create user
    this.app.post('/api/users', async (req, res) => {
      try {
        const user = await this.userService.createUser(req.body);
        res.status(201).json(user);
      } catch (error) {
        res.status(400).json({ error: (error as Error).message });
      }
    });
    
    // Update user
    this.app.put('/api/users/:id', async (req, res) => {
      try {
        const user = await this.userService.updateUser(req.params.id, req.body);
        res.json(user);
      } catch (error) {
        res.status(400).json({ error: (error as Error).message });
      }
    });
    
    // Delete user
    this.app.delete('/api/users/:id', async (req, res) => {
      await this.userService.deleteUser(req.params.id);
      res.status(204).send();
    });
  }
  
  getApp(): express.Application {
    return this.app;
  }
}
```

### gRPC API Design

```typescript
// grpc-api.ts
import * as grpc from '@grpc/grpc-js';
import * as protoLoader from '@grpc/proto-loader';

export class UserGRPCService {
  private server: grpc.Server;
  
  constructor() {
    this.server = new grpc.Server();
    this.setupServices();
  }
  
  private setupServices(): void {
    const packageDefinition = protoLoader.loadSync('user.proto', {
      keepCase: true,
      longs: String,
      enums: String,
      defaults: true,
      oneofs: true
    });
    
    const userProto = grpc.loadPackageDefinition(packageDefinition).user;
    
    this.server.addService(userProto.UserService.service, {
      GetUser: this.getUser.bind(this),
      ListUsers: this.listUsers.bind(this),
      CreateUser: this.createUser.bind(this),
      UpdateUser: this.updateUser.bind(this),
      DeleteUser: this.deleteUser.bind(this)
    });
  }
  
  private async getUser(
    call: grpc.ServerUnaryCall<any, any>,
    callback: grpc.sendUnaryData<any>
  ): Promise<void> {
    try {
      const user = await new UserService().getUserById(call.request.id);
      callback(null, user);
    } catch (error) {
      callback(error as Error, null);
    }
  }
  
  private async listUsers(
    call: grpc.ServerUnaryCall<any, any>,
    callback: grpc.sendUnaryData<any>
  ): Promise<void> {
    try {
      const result = await new UserService().listUsers(
        call.request.page,
        call.request.limit
      );
      callback(null, {
        users: result.users,
        total: result.total
      });
    } catch (error) {
      callback(error as Error, null);
    }
  }
  
  start(port: number): void {
    this.server.bindAsync(
      `0.0.0.0:${port}`,
      grpc.ServerCredentials.createInsecure(),
      () => {
        console.log(`gRPC server running on port ${port}`);
        this.server.start();
      }
    );
  }
}
```

---

## Data Management

### Database Per Service

```typescript
// database-per-service.ts
import { Pool } from 'pg';

export class UserDatabase {
  private pool: Pool;
  
  constructor(connectionString: string) {
    this.pool = new Pool({ connectionString });
  }
  
  async createUser(user: any): Promise<any> {
    const query = `
      INSERT INTO users (id, email, password_hash, created_at)
      VALUES ($1, $2, $3, NOW())
      RETURNING *
    `;
    
    const result = await this.pool.query(query, [
      user.id,
      user.email,
      user.passwordHash
    ]);
    
    return result.rows[0];
  }
  
  async getUserById(id: string): Promise<any> {
    const query = 'SELECT * FROM users WHERE id = $1';
    const result = await this.pool.query(query, [id]);
    return result.rows[0];
  }
  
  async updateUser(id: string, updates: any): Promise<any> {
    const setClause = Object.keys(updates)
      .map((key, index) => `${key} = $${index + 2}`)
      .join(', ');
    
    const query = `
      UPDATE users
      SET ${setClause}, updated_at = NOW()
      WHERE id = $1
      RETURNING *
    `;
    
    const values = [id, ...Object.values(updates)];
    const result = await this.pool.query(query, values);
    return result.rows[0];
  }
  
  async close(): Promise<void> {
    await this.pool.end();
  }
}
```

### Shared Database

```typescript
// shared-database.ts
import { Pool } from 'pg';

export class SharedDatabase {
  private pool: Pool;
  
  constructor(connectionString: string) {
    this.pool = new Pool({ connectionString });
  }
  
  async query(sql: string, params: any[] = []): Promise<any> {
    const result = await this.pool.query(sql, params);
    return result.rows;
  }
  
  async transaction<T>(callback: (client: any) => Promise<T>): Promise<T> {
    const client = await this.pool.connect();
    
    try {
      await client.query('BEGIN');
      const result = await callback(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }
  
  async close(): Promise<void> {
    await this.pool.end();
  }
}
```

---

## Communication Patterns

### Synchronous Communication

```typescript
// sync-communication.ts
import axios from 'axios';

export class OrderServiceClient {
  private baseURL: string;
  
  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }
  
  async createOrder(orderData: any): Promise<any> {
    const response = await axios.post(
      `${this.baseURL}/api/orders`,
      orderData,
      { timeout: 5000 }
    );
    return response.data;
  }
  
  async getOrder(orderId: string): Promise<any> {
    const response = await axios.get(
      `${this.baseURL}/api/orders/${orderId}`,
      { timeout: 5000 }
    );
    return response.data;
  }
  
  async updateOrder(orderId: string, updates: any): Promise<any> {
    const response = await axios.put(
      `${this.baseURL}/api/orders/${orderId}`,
      updates,
      { timeout: 5000 }
    );
    return response.data;
  }
}
```

### Asynchronous Communication

```typescript
// async-communication.ts
import { Queue } from 'bullmq';
import { createRedisConnection } from '../messaging-queue/redis-queue/redis-connection';

export class OrderEventPublisher {
  private queue: Queue;
  
  constructor() {
    this.queue = new Queue('order-events', {
      connection: createRedisConnection()
    });
  }
  
  async publishOrderCreated(order: any): Promise<void> {
    await this.queue.add('order-created', {
      eventType: 'OrderCreated',
      orderId: order.id,
      userId: order.userId,
      total: order.total,
      items: order.items,
      timestamp: new Date()
    });
  }
  
  async publishOrderUpdated(order: any): Promise<void> {
    await this.queue.add('order-updated', {
      eventType: 'OrderUpdated',
      orderId: order.id,
      changes: order.changes,
      timestamp: new Date()
    });
  }
  
  async publishOrderCancelled(orderId: string, reason: string): Promise<void> {
    await this.queue.add('order-cancelled', {
      eventType: 'OrderCancelled',
      orderId,
      reason,
      timestamp: new Date()
    });
  }
}
```

---

## Service Discovery

### Service Registry

```typescript
// service-registry.ts
export interface ServiceInstance {
  id: string;
  name: string;
  address: string;
  port: number;
  health: 'healthy' | 'unhealthy';
  lastSeen: Date;
}

export class ServiceRegistry {
  private services: Map<string, ServiceInstance[]> = new Map();
  
  register(instance: ServiceInstance): void {
    const serviceName = instance.name;
    
    if (!this.services.has(serviceName)) {
      this.services.set(serviceName, []);
    }
    
    const instances = this.services.get(serviceName)!;
    const existingIndex = instances.findIndex(i => i.id === instance.id);
    
    if (existingIndex >= 0) {
      instances[existingIndex] = { ...instance, lastSeen: new Date() };
    } else {
      instances.push({ ...instance, lastSeen: new Date() });
    }
  }
  
  deregister(serviceName: string, instanceId: string): void {
    const instances = this.services.get(serviceName);
    if (instances) {
      const index = instances.findIndex(i => i.id === instanceId);
      if (index >= 0) {
        instances.splice(index, 1);
      }
    }
  }
  
  discover(serviceName: string): ServiceInstance | null {
    const instances = this.services.get(serviceName);
    if (!instances || instances.length === 0) {
      return null;
    }
    
    // Return first healthy instance
    const healthyInstances = instances.filter(i => i.health === 'healthy');
    if (healthyInstances.length === 0) {
      return null;
    }
    
    // Simple round-robin (can be enhanced with load balancing)
    return healthyInstances[Math.floor(Math.random() * healthyInstances.length)];
  }
  
  heartbeat(serviceName: string, instanceId: string): void {
    const instances = this.services.get(serviceName);
    if (instances) {
      const instance = instances.find(i => i.id === instanceId);
      if (instance) {
        instance.lastSeen = new Date();
        instance.health = 'healthy';
      }
    }
  }
  
  cleanupStaleServices(timeoutMs: number = 60000): void {
    const now = new Date();
    
    for (const [serviceName, instances] of this.services.entries()) {
      for (let i = instances.length - 1; i >= 0; i--) {
        const instance = instances[i];
        const age = now.getTime() - instance.lastSeen.getTime();
        
        if (age > timeoutMs) {
          instances.splice(i, 1);
        }
      }
      
      if (instances.length === 0) {
        this.services.delete(serviceName);
      }
    }
  }
}
```

---

## Configuration Management

### Configuration Service

```typescript
// config-service.ts
export interface ServiceConfig {
  serviceName: string;
  version: string;
  environment: 'development' | 'staging' | 'production';
  settings: Record<string, any>;
}

export class ConfigService {
  private configs: Map<string, ServiceConfig> = new Map();
  
  async loadConfig(serviceName: string, environment: string): Promise<ServiceConfig> {
    const cacheKey = `${serviceName}:${environment}`;
    
    if (this.configs.has(cacheKey)) {
      return this.configs.get(cacheKey)!;
    }
    
    // Load from database or config server
    const config = await this.fetchConfig(serviceName, environment);
    this.configs.set(cacheKey, config);
    
    return config;
  }
  
  async updateConfig(serviceName: string, environment: string, updates: any): Promise<void> {
    const cacheKey = `${serviceName}:${environment}`;
    const existing = this.configs.get(cacheKey);
    
    const updated: ServiceConfig = {
      serviceName,
      version: existing?.version || '1.0.0',
      environment,
      settings: { ...existing?.settings, ...updates }
    };
    
    await this.saveConfig(serviceName, environment, updated);
    this.configs.set(cacheKey, updated);
  }
  
  private async fetchConfig(serviceName: string, environment: string): Promise<ServiceConfig> {
    // Implementation - fetch from database or config server
    return {
      serviceName,
      version: '1.0.0',
      environment: environment as any,
      settings: {}
    };
  }
  
  private async saveConfig(serviceName: string, environment: string, config: ServiceConfig): Promise<void> {
    // Implementation - save to database or config server
  }
}
```

---

## Logging and Tracing

### Structured Logging

```typescript
// logger.ts
export enum LogLevel {
  DEBUG = 'DEBUG',
  INFO = 'INFO',
  WARN = 'WARN',
  ERROR = 'ERROR'
}

export interface LogEntry {
  timestamp: Date;
  level: LogLevel;
  service: string;
  message: string;
  context?: Record<string, any>;
  traceId?: string;
  spanId?: string;
}

export class Logger {
  constructor(private serviceName: string) {}
  
  private log(level: LogLevel, message: string, context?: Record<string, any>): void {
    const entry: LogEntry = {
      timestamp: new Date(),
      level,
      service: this.serviceName,
      message,
      context
    };
    
    console.log(JSON.stringify(entry));
  }
  
  debug(message: string, context?: Record<string, any>): void {
    this.log(LogLevel.DEBUG, message, context);
  }
  
  info(message: string, context?: Record<string, any>): void {
    this.log(LogLevel.INFO, message, context);
  }
  
  warn(message: string, context?: Record<string, any>): void {
    this.log(LogLevel.WARN, message, context);
  }
  
  error(message: string, error?: Error, context?: Record<string, any>): void {
    this.log(LogLevel.ERROR, message, {
      ...context,
      error: error ? {
        message: error.message,
        stack: error.stack
      } : undefined
    });
  }
}
```

---

## Testing Strategies

### Service Testing

```typescript
// service-testing.ts
import { describe, it, expect, beforeEach } from '@jest/globals';
import { UserService } from './user-service';
import { UserDatabase } from './database-per-service';

describe('UserService', () => {
  let userService: UserService;
  let mockDatabase: jest.Mocked<UserDatabase>;
  
  beforeEach(() => {
    mockDatabase = {
      createUser: jest.fn(),
      getUserById: jest.fn(),
      updateUser: jest.fn(),
      deleteUser: jest.fn()
    } as any;
    
    userService = new UserService(mockDatabase);
  });
  
  describe('createUser', () => {
    it('should create a new user', async () => {
      const userData = {
        email: 'test@example.com',
        password: 'password123'
      };
      
      const expectedUser = {
        id: '123',
        email: userData.email,
        passwordHash: 'hashed_password'
      };
      
      mockDatabase.createUser.mockResolvedValue(expectedUser);
      
      const result = await userService.createUser(userData);
      
      expect(result).toEqual(expectedUser);
      expect(mockDatabase.createUser).toHaveBeenCalledWith(
        expect.objectContaining({
          email: userData.email
        })
      );
    });
    
    it('should throw error for invalid email', async () => {
      const userData = {
        email: 'invalid-email',
        password: 'password123'
      };
      
      await expect(userService.createUser(userData)).rejects.toThrow('Invalid email');
    });
  });
  
  describe('getUserById', () => {
    it('should return user when found', async () => {
      const userId = '123';
      const expectedUser = { id: userId, email: 'test@example.com' };
      
      mockDatabase.getUserById.mockResolvedValue(expectedUser);
      
      const result = await userService.getUserById(userId);
      
      expect(result).toEqual(expectedUser);
      expect(mockDatabase.getUserById).toHaveBeenCalledWith(userId);
    });
    
    it('should return null when user not found', async () => {
      mockDatabase.getUserById.mockResolvedValue(null);
      
      const result = await userService.getUserById('nonexistent');
      
      expect(result).toBeNull();
    });
  });
});
```

---

## Common Anti-Patterns

### Anti-Patterns to Avoid

```markdown
## Common Microservice Anti-Patterns

### Distributed Monolith
- Services are too tightly coupled
- Shared databases between services
- Synchronous calls between all services

### Chatty Services
- Too many small services
- Excessive network calls
- Performance degradation

### Shared Nothing
- No communication between services
- Data duplication
- Inconsistent state

### Database per Service (Misapplied)
- Sharing database but calling through APIs
- Data integrity issues
- Performance problems

### Versioning Nightmares
- Multiple versions running simultaneously
- Breaking changes
- Complex routing logic
```

---

## Best Practices

### Service Design Checklist

```markdown
## Service Design Checklist

### Service Boundaries
- [ ] Clear business capability
- [ ] Well-defined API contract
- [ ] Independent data ownership
- [ ] Minimal dependencies

### API Design
- [ ] RESTful or gRPC
- [ ] Versioned endpoints
- [ ] Consistent error handling
- [ ] Rate limiting

### Data Management
- [ ] Database per service
- [ ] Data migration strategy
- [ ] Backup and recovery
- [ ] Data consistency model

### Communication
- [ ] Synchronous for queries
- [ ] Asynchronous for events
- [ ] Circuit breakers
- [ ] Retry logic

### Observability
- [ ] Structured logging
- [ ] Metrics collection
- [ ] Distributed tracing
- [ ] Health checks

### Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] Contract tests
- [ ] Load tests
```

---

## Additional Resources

- [Microservices Patterns](https://microservices.io/patterns/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Building Microservices](https://www.oreilly.com/library/view/building-microservices/9781491950340/)
- [Microservices Best Practices](https://aws.amazon.com/microservices/best-practices/)
