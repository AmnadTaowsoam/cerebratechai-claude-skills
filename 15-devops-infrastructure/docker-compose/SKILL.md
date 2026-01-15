# Docker Compose

## Overview

Docker Compose is a tool for defining and running multi-container Docker applications. This skill covers Compose file structure, services definition, and common stacks.

## Table of Contents

1. [Compose File Structure](#compose-file-structure)
2. [Services Definition](#services-definition)
3. [Networks](#networks)
4. [Volumes](#volumes)
5. [Environment Variables](#environment-variables)
6. [Dependencies (depends_on)](#dependencies-dependson)
7. [Health Checks](#health-checks)
8. [Development Setup](#development-setup)
9. [Production Considerations](#production-considerations)
10. [Common Stacks](#common-stacks)
11. [Best Practices](#best-practices)

---

## Compose File Structure

### Basic Structure

```yaml
version: '3.8'

services:
  service1:
    image: nginx:latest
    ports:
      - "80:80"

  service2:
    build: .
    ports:
      - "3000:3000"

networks:
  default:
    name: my-network

volumes:
  data:
    driver: local
```

### File Versioning

| Version | Features | Docker Engine |
|---------|----------|---------------|
| 3.8 | Long syntax for secrets, configs | 19.03+ |
| 3.7 | External secrets | 19.03+ |
| 3.6 | Runtime on Linux | 18.02+ |
| 3.5 | Long syntax for mounts | 17.12+ |

---

## Services Definition

### Basic Service

```yaml
services:
  app:
    image: node:18-alpine
    container_name: myapp
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - PORT=3000
    volumes:
      - ./app:/app
      - node_modules:/app/node_modules
    working_dir: /app
    command: npm start
```

### Build Service

```yaml
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        NODE_VERSION: 18
    image: myapp:latest
    ports:
      - "3000:3000"
```

### Multiple Services

```yaml
services:
  app:
    image: node:18-alpine
    ports:
      - "3000:3000"
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - db_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  db_data:
  redis_data:
```

---

## Networks

### Default Network

```yaml
services:
  app:
    image: nginx:alpine
    ports:
      - "80:80"
    # Uses default network automatically
```

### Custom Network

```yaml
services:
  app:
    image: nginx:alpine
    networks:
      - frontend

networks:
  frontend:
    driver: bridge
```

### Multiple Networks

```yaml
services:
  app:
    image: nginx:alpine
    networks:
      - frontend
      - backend

  db:
    image: postgres:15-alpine
    networks:
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
```

### External Network

```yaml
services:
  app:
    image: nginx:alpine
    networks:
      - external_network

networks:
  external_network:
    external: true
```

---

## Volumes

### Named Volume

```yaml
services:
  db:
    image: postgres:15-alpine
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
    driver: local
```

### Bind Mount

```yaml
services:
  app:
    image: node:18-alpine
    volumes:
      - ./app:/app
      - ./config:/app/config:ro
```

### Anonymous Volume

```yaml
services:
  app:
    image: node:18-alpine
    volumes:
      - /app/node_modules
```

### Volume Options

```yaml
services:
  app:
    image: node:18-alpine
    volumes:
      - type: volume
        source: data
        target: /app/data
        volume:
          nocopy: true
      - type: bind
        source: ./config
        target: /app/config
        read_only: true

volumes:
  data:
    driver: local
```

---

## Environment Variables

### Inline Environment

```yaml
services:
  app:
    image: node:18-alpine
    environment:
      - NODE_ENV=production
      - PORT=3000
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
```

### Environment File

```yaml
services:
  app:
    image: node:18-alpine
    env_file:
      - .env
      - .env.production
```

### Multiple Environment Files

```yaml
services:
  app:
    image: node:18-alpine
    env_file:
      - path: .env
        required: true
      - path: .env.production
        required: false
```

### Environment with Default Values

```yaml
services:
  app:
    image: node:18-alpine
    environment:
      - NODE_ENV=${NODE_ENV:-development}
      - PORT=${PORT:-3000}
```

---

## Dependencies (depends_on)

### Simple Dependency

```yaml
services:
  app:
    image: node:18-alpine
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine

  redis:
    image: redis:7-alpine
```

### Conditional Dependency

```yaml
services:
  app:
    image: node:18-alpine
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
```

### Long Syntax

```yaml
services:
  app:
    image: node:18-alpine
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
```

---

## Health Checks

### HTTP Health Check

```yaml
services:
  app:
    image: node:18-alpine
    ports:
      - "3000:3000"
    healthcheck:
      test: ["CMD", "wget", "--no-verbose", "--tries=1", "--spider", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### TCP Health Check

```yaml
services:
  app:
    image: node:18-alpine
    ports:
      - "3000:3000"
    healthcheck:
      test: ["CMD-SHELL", "nc -z localhost 3000 || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Command Health Check

```yaml
services:
  db:
    image: postgres:15-alpine
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Disable Health Check

```yaml
services:
  app:
    image: node:18-alpine
    healthcheck:
      disable: true
```

---

## Development Setup

### Hot Reload

```yaml
version: '3.8'

services:
  app:
    build: .
    volumes:
      - ./app:/app
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    command: npm run dev
```

### Debug Mode

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
      - "9229:9229"  # Node.js debugger
    environment:
      - NODE_ENV=development
      - DEBUG=app:*
    command: node --inspect=0.0.0.0:9229 index.js
```

### Development Override

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
```

```yaml
# docker-compose.override.yml
version: '3.8'

services:
  app:
    volumes:
      - ./app:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
    command: npm run dev
```

---

## Production Considerations

### Resource Limits

```yaml
services:
  app:
    image: node:18-alpine
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
```

### Restart Policies

```yaml
services:
  app:
    image: node:18-alpine
    restart: always  # no, always, on-failure, unless-stopped

  db:
    image: postgres:15-alpine
    restart: unless-stopped
```

### Logging

```yaml
services:
  app:
    image: node:18-alpine
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
```

### Security Options

```yaml
services:
  app:
    image: node:18-alpine
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    read_only: true
    tmpfs:
      - /tmp:noexec,size=100m
```

---

## Common Stacks

### PERN Stack (Postgres, Express, React, Node)

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: postgres
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: ./api
    container_name: api
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/myapp
      - JWT_SECRET=your-secret-key
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./api:/app
      - /app/node_modules
    command: npm start

  frontend:
    build: ./frontend
    container_name: frontend
    ports:
      - "80:80"
    depends_on:
      - api
    volumes:
      - ./frontend/nginx.conf:/etc/nginx/conf.d/default.conf:ro

volumes:
  postgres_data:
```

### FastAPI + PostgreSQL + Redis

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: postgres
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: ./api
    container_name: api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/myapp
      - REDIS_URL=redis://redis:6379/0
      - SECRET_KEY=your-secret-key
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./api:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000

volumes:
  postgres_data:
  redis_data:
```

### Microservices Stack

```yaml
version: '3.8'

services:
  api-gateway:
    build: ./api-gateway
    ports:
      - "8080:8080"
    depends_on:
      - users-service
      - products-service
      - orders-service

  users-service:
    build: ./users-service
    ports:
      - "3001:3000"
    depends_on:
      - postgres
      - redis

  products-service:
    build: ./products-service
    ports:
      - "3002:3000"
    depends_on:
      - postgres
      - redis

  orders-service:
    build: ./orders-service
    ports:
      - "3003:3000"
    depends_on:
      - postgres
      - redis
      - rabbitmq

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      - RABBITMQ_DEFAULT_USER=admin
      - RABBITMQ_DEFAULT_PASS=admin

volumes:
  postgres_data:
  redis_data:
```

---

## Best Practices

### 1. Use Specific Versions

```yaml
# Good
services:
  app:
    image: node:18.17.0-alpine

# Bad
services:
  app:
    image: node:latest
```

### 2. Use Environment Files

```yaml
# Good
services:
  app:
    env_file:
      - .env

# Bad
services:
  app:
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
```

### 3. Use Named Volumes

```yaml
# Good
services:
  db:
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:

# Bad
services:
  db:
    volumes:
      - ./data:/var/lib/postgresql/data
```

### 4. Set Resource Limits

```yaml
# Good
services:
  app:
    deploy:
      resources:
        limits:
          memory: 512M
        reservations:
          memory: 256M

# Bad
services:
  app:
    # No resource limits
```

### 5. Use Health Checks

```yaml
# Good
services:
  app:
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:3000/health"]
      interval: 30s
      retries: 3

# Bad
services:
  app:
    # No health check
```

---

## Summary

This skill covers comprehensive Docker Compose implementation including:

- **Compose File Structure**: Basic structure and file versioning
- **Services Definition**: Basic, build, and multiple services
- **Networks**: Default, custom, multiple, and external networks
- **Volumes**: Named, bind mount, anonymous, and volume options
- **Environment Variables**: Inline, file, multiple files, and default values
- **Dependencies (depends_on)**: Simple, conditional, and long syntax
- **Health Checks**: HTTP, TCP, command, and disable options
- **Development Setup**: Hot reload, debug mode, and override
- **Production Considerations**: Resource limits, restart policies, logging, security
- **Common Stacks**: PERN, FastAPI + PostgreSQL + Redis, microservices
- **Best Practices**: Specific versions, environment files, named volumes, resource limits, health checks
