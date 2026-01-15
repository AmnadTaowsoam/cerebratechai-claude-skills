# Docker Patterns

## Overview

Docker containerization provides consistent environments across development, testing, and production. This skill covers Dockerfile best practices, multi-stage builds, and production-ready patterns.

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

### Use Official Base Images

```dockerfile
# Good: Use official images
FROM node:18-alpine
FROM python:3.11-slim
FROM golang:1.21-alpine

# Bad: Use unofficial images
FROM someuser/node:latest
FROM random/python:3.11
```

### Use Specific Versions

```dockerfile
# Good: Use specific versions
FROM node:18.17.0-alpine
FROM python:3.11.4-slim
FROM golang:1.21.6-alpine

# Bad: Use latest tag
FROM node:latest
FROM python:latest
FROM golang:latest
```

### Minimize Layers

```dockerfile
# Bad: Multiple RUN commands create multiple layers
FROM node:18-alpine
RUN apk add --no-cache git
RUN apk add --no-cache curl
RUN apk add --no-cache build-base

# Good: Combine RUN commands
FROM node:18-alpine
RUN apk add --no-cache git curl build-base
```

### Clean Up After Install

```dockerfile
# Good: Clean up after package installation
FROM node:18-alpine
RUN apk add --no-cache --virtual .build-deps \
    gcc \
    g++ \
    make \
    && npm install \
    && apk del .build-deps
```

### Use .dockerignore

```dockerfile
# .dockerignore
node_modules
npm-debug.log
.git
.gitignore
.env
Dockerfile
docker-compose.yml
README.md
*.md
.vscode
.idea
```

### Order Instructions by Frequency

```dockerfile
# Good: Order instructions by frequency of change
FROM node:18-alpine

# 1. Dependencies (change infrequently)
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# 2. Application code (changes frequently)
COPY . .

# 3. Start command (rarely changes)
CMD ["node", "index.js"]
```

---

## Multi-Stage Builds

### Node.js Multi-Stage Build

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine AS production
WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

ENV NODE_ENV=production

CMD ["node", "dist/index.js"]
```

### Python Multi-Stage Build

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install .

# Production stage
FROM python:3.11-slim AS production
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app .

CMD ["python", "app.py"]
```

### Go Multi-Stage Build

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o app .

# Production stage
FROM alpine:3.18
WORKDIR /app

COPY --from=builder /app/app .

CMD ["./app"]
```

### React Multi-Stage Build

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage (serve with nginx)
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Next.js Multi-Stage Build

```dockerfile
# Build stage
FROM node:18-alpine AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

FROM node:18-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
```

---

## Layer Caching Optimization

### Cache Dependencies

```dockerfile
# Good: Copy dependencies first
FROM node:18-alpine
WORKDIR /app

# Copy only package files
COPY package*.json ./

# Install dependencies (cached if package.json unchanged)
RUN npm ci

# Copy application code
COPY . .

# Build application
RUN npm run build
```

### Use BuildKit Cache

```dockerfile
# Good: Use BuildKit cache mounts
FROM node:18-alpine
WORKDIR /app

COPY package*.json ./

# Use cache mount for npm
RUN --mount=type=cache,target=/root/.npm \
    npm ci

COPY . .

RUN npm run build
```

### Cache Go Modules

```dockerfile
# Good: Cache Go modules
FROM golang:1.21-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./

# Use cache mount for Go modules
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o app .
```

### Cache Python Packages

```dockerfile
# Good: Cache Python packages
FROM python:3.11-slim AS builder
WORKDIR /app

COPY requirements.txt .

# Use cache mount for pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install .
```

---

## .dockerignore

### Common Patterns

```dockerfile
# .dockerignore
node_modules
npm-debug.log
yarn-error.log
yarn-debug.log
.pnpm-debug.log

# Git
.git
.gitignore
.gitattributes

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode
.idea
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Docker
Dockerfile
docker-compose.yml
.dockerignore

# Documentation
README.md
*.md
docs/

# Tests
__tests__
tests/
*.test.js
*.spec.js
coverage/
.nyc_output/

# Build artifacts
dist/
build/
.next/
out/

# Misc
*.log
.cache
```

### Language-Specific .dockerignore

```dockerfile
# Node.js
node_modules
npm-debug.log
yarn-error.log
package-lock.json
yarn.lock

# Python
__pycache__
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info
dist
build
.eggs
.pytest_cache
.coverage
htmlcov

# Go
*.exe
*.exe~
*.dll
*.so
*.dylib
*.test
*.out
vendor/
```

---

## Environment Variables

### Using ARG and ENV

```dockerfile
# ARG: Build-time variable
ARG NODE_VERSION=18
ARG APP_ENV=production

# ENV: Runtime variable
ENV NODE_ENV=${APP_ENV}
ENV NODE_OPTIONS=--max-old-space-size=4096

# Use ARG in FROM
FROM node:${NODE_VERSION}-alpine
```

### Environment Files

```dockerfile
# Copy environment file
FROM node:18-alpine
WORKDIR /app

COPY .env.production .env

# Or use docker-compose for environment
```

### Docker Compose Environment

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    build: .
    environment:
      - NODE_ENV=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
    env_file:
      - .env.production
```

---

## Health Checks

### HTTP Health Check

```dockerfile
# HTTP health check
FROM node:18-alpine
WORKDIR /app

COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

CMD ["node", "dist/index.js"]
```

### TCP Health Check

```dockerfile
# TCP health check
FROM node:18-alpine
WORKDIR /app

COPY package*.json ./
RUN npm ci
COPY . .

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD nc -z localhost 3000

CMD ["node", "index.js"]
```

### Script Health Check

```dockerfile
# Script health check
FROM node:18-alpine
WORKDIR /app

COPY package*.json ./
RUN npm ci
COPY . .

# Create health check script
RUN echo '#!/bin/sh\nnode -e "require(\"./health-check.js\")"' > /health-check.sh && \
    chmod +x /health-check.sh

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD /health-check.sh

CMD ["node", "index.js"]
```

---

## Security Scanning

### Trivy Scan

```bash
# Scan Docker image
trivy image myapp:latest

# Scan Dockerfile
trivy config Dockerfile

# Scan with severity threshold
trivy image --severity HIGH,CRITICAL myapp:latest
```

### Docker Scout

```bash
# Scan Docker image
docker scout quickstart

# Scan Dockerfile
docker scout quickstart Dockerfile

# Scan with CVE database
docker scout cves myapp:latest
```

### Snyk Scan

```bash
# Scan Docker image
snyk container test myapp:latest --file=Dockerfile

# Scan Dockerfile
snyk iac test Dockerfile
```

---

## Image Optimization

### Use Alpine Images

```dockerfile
# Good: Use Alpine (smaller size)
FROM node:18-alpine
FROM python:3.11-alpine
FROM golang:1.21-alpine

# Bad: Use standard images (larger size)
FROM node:18
FROM python:3.11
FROM golang:1.21
```

### Use Distroless Images

```dockerfile
# Good: Use distroless (minimal attack surface)
FROM gcr.io/distroless/nodejs18-debian11
FROM gcr.io/distroless/python3-debian11
FROM gcr.io/distroless/base-debian11
```

### Remove Unnecessary Files

```dockerfile
# Good: Remove unnecessary files
FROM node:18-alpine
WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production && \
    npm cache clean --force

COPY . .
RUN npm run build && \
    rm -rf /app/src /app/test

CMD ["node", "dist/index.js"]
```

### Use .dockerignore

```dockerfile
# .dockerignore
node_modules
npm-debug.log
.git
.env
Dockerfile
docker-compose.yml
README.md
```

---

## Common Patterns

### Node.js App

```dockerfile
FROM node:18-alpine
WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .

ENV NODE_ENV=production

CMD ["node", "index.js"]
```

### Python App

```dockerfile
FROM python:3.11-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
```

### Go App

```dockerfile
FROM golang:1.21-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o app .

FROM alpine:3.18
WORKDIR /app

COPY --from=builder /app/app .

CMD ["./app"]
```

### React App

```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### Next.js App

```dockerfile
FROM node:18-alpine AS deps
WORKDIR /app

COPY package*.json ./
RUN npm ci

FROM node:18-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000

CMD ["node", "server.js"]
```

---

## Production Dockerfile Examples

### Node.js API

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

# Production stage
FROM node:18-alpine AS production
WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/package.json ./

ENV NODE_ENV=production

USER node

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

CMD ["node", "dist/index.js"]
```

### Python API

```dockerfile
# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

COPY . .
RUN pip install --user .

# Production stage
FROM python:3.11-slim AS production
WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY --from=builder /app .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

USER nobody

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["python", "app.py"]
```

### Go API

```dockerfile
# Build stage
FROM golang:1.21-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o app .

# Production stage
FROM alpine:3.18
WORKDIR /app

COPY --from=builder /app/app .

RUN apk add --no-cache ca-certificates

USER nobody

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["./app"]
```

### React SPA

```dockerfile
# Build stage
FROM node:18-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
WORKDIR /usr/share/nginx/html

COPY --from=builder /app/build .

COPY nginx.conf /etc/nginx/conf.d/default.conf

RUN chown -R nginx:nginx /usr/share/nginx/html

USER nginx

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

---

## Best Practices

### 1. Use Specific Versions

```dockerfile
# Good
FROM node:18.17.0-alpine

# Bad
FROM node:latest
```

### 2. Minimize Layers

```dockerfile
# Good
RUN apk add --no-cache git curl make && \
    npm ci && \
    npm run build

# Bad
RUN apk add --no-cache git
RUN apk add --no-cache curl
RUN npm ci
RUN npm run build
```

### 3. Use Multi-Stage Builds

```dockerfile
# Good: Multi-stage build
FROM node:18-alpine AS builder
RUN npm run build

FROM node:18-alpine
COPY --from=builder /app/dist ./dist

# Bad: Single stage
FROM node:18-alpine
RUN npm install && npm run build
```

### 4. Use .dockerignore

```dockerfile
# .dockerignore
node_modules
npm-debug.log
.git
.env
```

### 5. Run as Non-Root User

```dockerfile
# Good
USER node
USER nobody

# Bad
# Runs as root by default
```

---

## Summary

This skill covers comprehensive Docker containerization patterns including:

- **Dockerfile Best Practices**: Official images, specific versions, minimize layers
- **Multi-Stage Builds**: Node.js, Python, Go, React, Next.js
- **Layer Caching Optimization**: Cache dependencies, BuildKit cache
- **.dockerignore**: Common patterns and language-specific files
- **Environment Variables**: ARG, ENV, environment files
- **Health Checks**: HTTP, TCP, script-based health checks
- **Security Scanning**: Trivy, Docker Scout, Snyk
- **Image Optimization**: Alpine, distroless, remove unnecessary files
- **Common Patterns**: Node.js, Python, Go, React, Next.js
- **Production Dockerfile Examples**: Node.js API, Python API, Go API, React SPA
- **Best Practices**: Specific versions, minimize layers, multi-stage builds, .dockerignore, non-root user
