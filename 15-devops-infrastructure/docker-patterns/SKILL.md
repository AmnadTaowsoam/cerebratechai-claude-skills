# Docker Patterns

A comprehensive guide to Docker containerization patterns and best practices.

## Table of Contents

1. [Dockerfile Best Practices](#dockerfile-best-practices)
2. [Multi-Stage Builds](#multi-stage-builds)
3. [Layer Caching Optimization](#layer-caching-optimization)
4. [.dockerignore](#dockerignore)
5. [Environment Variables](#environment-variables)
6. [Health Checks](#health-checks)
7. [Security Scanning](#security-scanning)
8. [Image Optimization](#image-optimization)
9. [Common Patterns](#common-patterns)
10. [Production Dockerfile Examples](#production-dockerfile-examples)
11. [Best Practices](#best-practices)

---

## Dockerfile Best Practices

### General Guidelines

| Practice | Why | Example |
|----------|-----|---------|
| Use specific base image | Smaller, more predictable | `node:18-alpine` vs `node:18` |
| Minimize layers | Faster builds, smaller images | Combine RUN commands |
| Order instructions strategically | Better cache utilization | Copy package files before source |
| Use .dockerignore | Exclude unnecessary files | `node_modules`, `.git` |
| Don't run as root | Security best practice | Create non-root user |
| Use build args for versioning | Reproducible builds | `ARG VERSION=1.0.0` |

### Basic Dockerfile Structure

```dockerfile
# 1. Base image
FROM node:18-alpine AS base

# 2. Set working directory
WORKDIR /app

# 3. Install dependencies
COPY package*.json ./
RUN npm ci --only=production

# 4. Copy application code
COPY . .

# 5. Set environment variables
ENV NODE_ENV=production

# 6. Expose ports
EXPOSE 3000

# 7. Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

# 8. Define entrypoint
CMD ["node", "index.js"]
```

---

## Multi-Stage Builds

### Why Multi-Stage Builds?

```
Single Stage Build:
┌─────────────────────────────────────┐
│  Base Image (Node + npm + tools)   │  ~500MB
│  + Dependencies                     │  ~200MB
│  + Dev Dependencies                 │  ~100MB  ← Not needed in prod!
│  + Source Code                      │  ~50MB
│  + Build Artifacts                  │  ~100MB  ← Not needed in prod!
└─────────────────────────────────────┘
Total: ~950MB

Multi-Stage Build:
┌──────────────────────┐    ┌──────────────────────────┐
│  Build Stage         │    │  Runtime Stage           │
│  Base + Dev Deps     │    │  Base + Runtime Deps    │  ~700MB
│  + Source Code       │    │  + Compiled Assets       │  ~50MB
│  + Build             │    │                          │
└──────────────────────┘    └──────────────────────────┘
        ↓ Copy only artifacts
Total: ~750MB (21% smaller)
```

### Node.js Multi-Stage Build

```dockerfile
# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including dev)
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production

# Copy built assets from builder
COPY --from=builder /app/dist ./dist

# Set environment
ENV NODE_ENV=production

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

# Expose port
EXPOSE 3000

# Start application
CMD ["node", "dist/index.js"]
```

### Python Multi-Stage Build

```dockerfile
# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim AS production

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Expose port
EXPOSE 8000

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Next.js Multi-Stage Build

```dockerfile
# Dependencies stage
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Builder stage
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

---

## Layer Caching Optimization

### Docker Layer Caching

```
Docker builds images in layers. Each instruction creates a new layer.

Layer 1: FROM node:18-alpine          ← Cached if base image unchanged
Layer 2: WORKDIR /app                  ← Always cached
Layer 3: COPY package*.json ./         ← Cached if package files unchanged
Layer 4: RUN npm ci                     ← Cached if package.json unchanged
Layer 5: COPY . .                      ← Invalidated if any file changes
Layer 6: RUN npm run build             ← Rebuild every time source changes

Optimization:
- Copy package files BEFORE source code
- Separate dependency installation from app copy
```

### Optimized Dockerfile

```dockerfile
FROM node:18-alpine

WORKDIR /app

# ✅ GOOD: Copy package files first
COPY package*.json ./

# ✅ GOOD: Install dependencies (cached if package.json unchanged)
RUN npm ci --only=production

# ✅ GOOD: Copy source code after dependencies
COPY . .

# ✅ GOOD: Build after source copy
RUN npm run build

# ❌ BAD: This would invalidate cache on any source change
# COPY . .
# RUN npm install
```

### Advanced Caching with BuildKit

```dockerfile
# syntax=docker/dockerfile:1.4

FROM node:18-alpine

WORKDIR /app

# Use cache mount for node_modules
RUN --mount=type=cache,target=/app/node_modules \
    npm ci

COPY . .

RUN npm run build
```

---

## .dockerignore

### Why .dockerignore?

```
Without .dockerignore:
- Copies entire context to build daemon
- Includes node_modules (huge!)
- Includes .git (huge!)
- Includes .env (security risk!)
- Includes test files (not needed in prod!)

With .dockerignore:
- Only copies necessary files
- Smaller build context
- Faster builds
- Better security
```

### Example .dockerignore

```dockerignore
# Dependencies
node_modules
npm-debug.log
yarn-error.log

# Testing
coverage
.nyc_output
*.test.js
*.spec.js
__tests__

# Environment
.env
.env.local
.env.*.local

# Git
.git
.gitignore

# Docker
Dockerfile
.dockerignore
docker-compose.yml

# IDE
.vscode
.idea
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Build artifacts
dist
build
.next

# Documentation
README.md
docs
*.md

# Misc
*.log
```

### Python .dockerignore

```dockerignore
# Python
__pycache__
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/

# IDE
.vscode
.idea
*.swp

# Git
.git
.gitignore

# Environment
.env
.env.local
.venv

# Docker
Dockerfile
docker-compose.yml
.dockerignore

# Documentation
README.md
docs/
```

---

## Environment Variables

### Using ENV Instruction

```dockerfile
# Set environment variable
ENV NODE_ENV=production
ENV PORT=3000

# Multiple variables
ENV NODE_ENV=production \
    PORT=3000 \
    HOST=0.0.0.0

# Using environment variables in subsequent instructions
ENV PATH="/app/bin:${PATH}"
```

### Using ARG Instruction

```dockerfile
# Build-time variable (not available at runtime)
ARG NODE_VERSION=18
ARG APP_VERSION=1.0.0

FROM node:${NODE_VERSION}-alpine

# Use ARG in ENV
ENV APP_VERSION=${APP_VERSION}

# ARG is not available after FROM unless redeclared
ARG APP_VERSION
ENV VERSION=${APP_VERSION}
```

### Runtime Environment Variables

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

# Set default values (can be overridden at runtime)
ENV NODE_ENV=production
ENV PORT=3000
ENV DATABASE_URL=postgresql://localhost:5432/db

EXPOSE 3000

CMD ["node", "index.js"]
```

### Override at Runtime

```bash
# Override environment variables
docker run -e NODE_ENV=development -e PORT=8080 myapp

# Use .env file
docker run --env-file .env myapp

# Docker Compose
services:
  app:
    environment:
      - NODE_ENV=production
      - PORT=3000
    env_file:
      - .env
```

---

## Health Checks

### Basic Health Check

```dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

EXPOSE 3000

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js || exit 1

CMD ["node", "index.js"]
```

### Health Check Script

```javascript
// healthcheck.js
const http = require('http');

const options = {
  host: 'localhost',
  port: process.env.PORT || 3000,
  path: '/health',
  timeout: 2000,
};

const request = http.request(options, (res) => {
  console.log(`Health check: ${res.statusCode}`);
  if (res.statusCode === 200) {
    process.exit(0);
  } else {
    process.exit(1);
  }
});

request.on('error', () => {
  process.exit(1);
});

request.end();
```

### Python Health Check

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Health check using curl
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose Health Check

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    healthcheck:
      test: ["CMD", "node", "healthcheck.js"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

---

## Security Scanning

### Docker Scout

```bash
# Scan image for vulnerabilities
docker scout quickimage myapp:latest

# Scan with detailed output
docker scout cves myapp:latest

# Scan during build
docker build --security-opt=scan=true .
```

### Trivy

```bash
# Install Trivy
brew install trivy

# Scan image
trivy image myapp:latest

# Scan with severity threshold
trivy image --severity HIGH,CRITICAL myapp:latest

# Scan filesystem
trivy fs .
```

### Snyk

```bash
# Install Snyk
npm install -g snyk

# Scan image
snyk container test myapp:latest

# Scan Dockerfile
snyk container test --file=Dockerfile

# Scan and monitor
snyk monitor --docker myapp:latest
```

### Docker Bench Security

```bash
# Run Docker Bench Security
docker run --rm --net host --pid host --userns host --cap-add SYS_ADMIN \
  --volume /var/lib/docker:/var/lib/docker \
  --volume /var/run/docker.sock:/var/run/docker.sock \
  docker/docker-bench-security
```

---

## Image Optimization

### Use Alpine Linux

```dockerfile
# ❌ BAD: Standard image ~900MB
FROM node:18

# ✅ GOOD: Alpine image ~100MB
FROM node:18-alpine

# ✅ EVEN BETTER: Distroless ~80MB
FROM gcr.io/distroless/nodejs18-debian11
```

### Minimize Layers

```dockerfile
# ❌ BAD: Multiple layers
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN rm -rf /var/lib/apt/lists/*

# ✅ GOOD: Single layer
RUN apt-get update && \
    apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/*
```

### Clean Up After Install

```dockerfile
# ❌ BAD: Leaves cache files
RUN npm install

# ✅ GOOD: Cleans up cache
RUN npm ci --only=production && \
    npm cache clean --force

# ✅ GOOD: Cleans up apt cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*
```

### Use .dockerignore

```dockerfile
# .dockerignore
node_modules
.git
.env
*.log

# This prevents copying unnecessary files
COPY . .
```

### Multi-Stage Builds

```dockerfile
# Build stage includes dev dependencies
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage only includes runtime dependencies
FROM node:18-alpine AS production
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

---

## Common Patterns

### Node.js Application

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy application code
COPY . .

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "index.js"]
```

### Python Application

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Next.js Application

```dockerfile
# syntax=docker/dockerfile:1.4

FROM node:18-alpine AS base

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Rebuild the source code only when needed
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production image, copy all the files and run next
FROM base AS runner
WORKDIR /app

ENV NODE_ENV production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public

# Set the correct permission for prerender cache
RUN mkdir .next
RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

CMD ["node", "server.js"]
```

### Static Site

```dockerfile
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

---

## Production Dockerfile Examples

### Production Node.js Dockerfile

```dockerfile
# syntax=docker/dockerfile:1.4

# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies
RUN npm ci

# Copy source code
COPY . .

# Run tests
RUN npm test

# Build application
RUN npm run build

# Production stage
FROM node:18-alpine AS production

WORKDIR /app

# Set environment
ENV NODE_ENV=production

# Copy package files
COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Copy built assets from builder
COPY --from=builder /app/dist ./dist

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# Start application
CMD ["node", "dist/index.js"]
```

### Production Python Dockerfile

```dockerfile
# syntax=docker/dockerfile:1.4

# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run tests
RUN pytest

# Production stage
FROM python:3.11-slim AS production

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Copy application code
COPY . .

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## Best Practices

### 1. Use Specific Base Image Tags

```dockerfile
# ❌ BAD: Latest tag
FROM node:latest

# ✅ GOOD: Specific version
FROM node:18.17.0-alpine
```

### 2. Minimize Layers

```dockerfile
# ❌ BAD: Multiple RUN commands
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git

# ✅ GOOD: Combined RUN
RUN apt-get update && \
    apt-get install -y curl git && \
    rm -rf /var/lib/apt/lists/*
```

### 3. Leverage Build Cache

```dockerfile
# ✅ GOOD: Copy package files before source code
COPY package*.json ./
RUN npm ci
COPY . .
```

### 4. Use Multi-Stage Builds

```dockerfile
# ✅ GOOD: Separate build and runtime stages
FROM node:18-alpine AS builder
# ... build steps ...

FROM node:18-alpine AS production
COPY --from=builder /app/dist ./dist
```

### 5. Don't Run as Root

```dockerfile
# ✅ GOOD: Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
USER nodejs
```

### 6. Use .dockerignore

```dockerfile
# .dockerignore
node_modules
.git
.env
*.log
```

### 7. Add Health Checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1
```

### 8. Scan for Vulnerabilities

```bash
docker scout quickimage myapp:latest
trivy image myapp:latest
```

### 9. Use Build Arguments for Versioning

```dockerfile
ARG VERSION=1.0.0
ENV APP_VERSION=${VERSION}
```

### 10. Document Your Dockerfile

```dockerfile
# Multi-stage build for Node.js application
# Stage 1: Builder - Installs dependencies and builds
# Stage 2: Production - Copies only runtime dependencies and built assets

FROM node:18-alpine AS builder
# ...
```

---

## Resources

- [Docker Documentation](https://docs.docker.com/)
- [Dockerfile Best Practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Docker Scout](https://docs.docker.com/scout/)
- [Trivy](https://aquasecurity.github.io/trivy/)
