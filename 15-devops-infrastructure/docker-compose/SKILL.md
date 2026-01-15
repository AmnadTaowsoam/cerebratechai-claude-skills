# Docker Compose

A comprehensive guide to Docker Compose for multi-container applications.

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
version: '3.8'  # Compose file version

services:        # Define services
  service1:
    # service configuration
  service2:
    # service configuration

networks:        # Define networks
  network1:
    # network configuration

volumes:         # Define volumes
  volume1:
    # volume configuration
```

### Complete Example

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    networks:
      - frontend
      - backend
    depends_on:
      - api

  api:
    build: ./api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://db:5432/app
    networks:
      - backend
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  frontend:
  backend:

volumes:
  postgres_data:
```

---

## Services Definition

### Build Configuration

```yaml
services:
  # Build from Dockerfile in current directory
  app:
    build: .

  # Build from specific directory
  app:
    build: ./app

  # Build with Dockerfile path
  app:
    build:
      context: ./app
      dockerfile: Dockerfile.prod

  # Build with build args
  app:
    build:
      context: .
      args:
        NODE_ENV: production
        VERSION: 1.0.0

  # Build with cache_from
  app:
    build:
      context: .
      cache_from:
        - myapp:latest
        - myapp:build

  # Build with target stage
  app:
    build:
      context: .
      target: production
```

### Image Configuration

```yaml
services:
  # Use image from registry
  app:
    image: myapp:latest

  # Use image with tag
  app:
    image: myapp:1.0.0

  # Use image from private registry
  app:
    image: registry.example.com/myapp:latest

  # Pull always
  app:
    image: myapp:latest
    pull_policy: always

  # Pull if missing
  app:
    image: myapp:latest
    pull_policy: missing
```

### Ports Configuration

```yaml
services:
  # Map single port
  app:
    ports:
      - "3000:3000"

  # Map multiple ports
  app:
    ports:
      - "3000:3000"
      - "3001:3001"

  # Map to random host port
  app:
    ports:
      - "3000"  # Maps to random port on host

  # Map with IP
  app:
    ports:
      - "127.0.0.1:3000:3000"

  # Map with protocol
  app:
    ports:
      - "3000:3000/tcp"
      - "3001:3001/udp"

  # Map port range
  app:
    ports:
      - "3000-3010:3000-3010"
```

### Command Configuration

```yaml
services:
  # Override default command
  app:
    image: node:18
    command: node index.js

  # Override with array form
  app:
    image: node:18
    command: ["node", "index.js"]

  # Override entrypoint
  app:
    image: node:18
    entrypoint: ["npm"]
    command: ["start"]

  # Multiple commands
  app:
    image: node:18
    command: >
      sh -c "npm install && npm start"
```

### Restart Policy

```yaml
services:
  # No restart
  app:
    restart: "no"

  # Always restart
  app:
    restart: always

  # Restart on failure
  app:
    restart: on-failure

  # Restart on failure with max retries
  app:
    restart: on-failure
    deploy:
      restart_policy:
        max_attempts: 3

  # Restart unless stopped
  app:
    restart: unless-stopped
```

---

## Networks

### Default Network

```yaml
services:
  web:
    image: nginx
    # Automatically joins default network

  api:
    image: node
    # Can reach web by service name
```

### Custom Networks

```yaml
version: '3.8'

services:
  web:
    image: nginx
    networks:
      - frontend

  api:
    image: node
    networks:
      - frontend
      - backend

  db:
    image: postgres
    networks:
      - backend

networks:
  frontend:
  backend:
```

### Network Configuration

```yaml
networks:
  # Default bridge network
  frontend:
    driver: bridge

  # Host network
  host_network:
    driver: host

  # None network (no network)
  no_network:
    driver: none

  # Custom bridge with options
  custom_bridge:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.name: my_bridge
      com.docker.network.bridge.enable_icc: "true"

  # Overlay network (Swarm)
  overlay_network:
    driver: overlay
    attachable: true
```

### IPv6 Network

```yaml
networks:
  frontend:
    driver: bridge
    enable_ipv6: true
    ipam:
      driver: default
      config:
        - subnet: "2001:db8:1::/64"
```

### External Network

```yaml
networks:
  # Use existing network
  external_network:
    external: true

  # Use named external network
  external_network:
    name: my-existing-network
    external: true
```

---

## Volumes

### Named Volumes

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Bind Mounts

```yaml
services:
  app:
    image: node:18
    volumes:
      # Mount current directory
      - .:/app

      # Mount specific file
      - ./nginx.conf:/etc/nginx/nginx.conf:ro

      # Mount with options
      - ./data:/data:ro

      # Mount on Windows
      - //c/Users/data:/data
```

### Tmpfs

```yaml
services:
  app:
    image: node:18
    tmpfs:
      - /tmp
      - /run
      - /app/cache:size=1000000000
```

### Volume Configuration

```yaml
volumes:
  # Local driver
  data_volume:
    driver: local

  # Local driver with options
  data_volume:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /data

  # NFS driver
  nfs_volume:
    driver: local
    driver_opts:
      type: nfs
      o: addr=192.168.1.1,rw
      device: ":/path/to/nfs/share"

  # External volume
  external_volume:
    external: true

  # Named external volume
  external_volume:
    name: my-existing-volume
    external: true
```

### Read-Only Volumes

```yaml
services:
  app:
    image: node:18
    volumes:
      - ./src:/app/src:ro
      - ./config:/app/config:ro
```

---

## Environment Variables

### Inline Environment Variables

```yaml
services:
  app:
    image: node:18
    environment:
      - NODE_ENV=production
      - PORT=3000
      - DATABASE_URL=postgresql://db:5432/app
```

### Array Form

```yaml
services:
  app:
    image: node:18
    environment:
      NODE_ENV: production
      PORT: 3000
      DATABASE_URL: postgresql://db:5432/app
```

### From .env File

```yaml
services:
  app:
    image: node:18
    env_file:
      - .env
      - .env.production
```

### From Shell Environment

```yaml
services:
  app:
    image: node:18
    environment:
      - NODE_ENV=${NODE_ENV:-development}
      - PORT=${PORT:-3000}
      - DATABASE_URL=${DATABASE_URL}
```

### Environment File

```bash
# .env
NODE_ENV=production
PORT=3000
DATABASE_URL=postgresql://db:5432/app
SECRET_KEY=supersecret

# .env.production
NODE_ENV=production
PORT=3000
DATABASE_URL=postgresql://prod-db:5432/app
SECRET_KEY=productionsecret
```

---

## Dependencies (depends_on)

### Basic Dependencies

```yaml
services:
  web:
    image: nginx
    depends_on:
      - api

  api:
    image: node
    depends_on:
      - db

  db:
    image: postgres
```

### Conditional Dependencies

```yaml
services:
  api:
    image: node
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started

  db:
    image: postgres
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis
```

### Long Form

```yaml
services:
  web:
    image: nginx
    depends_on:
      api:
        condition: service_healthy
      redis:
        condition: service_started
```

---

## Health Checks

### Basic Health Check

```yaml
services:
  app:
    image: myapp:latest
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

### Shell Command

```yaml
services:
  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### TCP Check

```yaml
services:
  redis:
    image: redis:7
    healthcheck:
      test: ["CMD-SHELL", "redis-cli ping"]
      interval: 10s
      timeout: 3s
      retries: 3
```

### Disable Health Check

```yaml
services:
  app:
    image: myapp:latest
    healthcheck:
      disable: true
```

---

## Development Setup

### Development Compose File

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build:
      context: .
      target: development
    volumes:
      - .:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development
      - WATCH=true
    ports:
      - "3000:3000"
      - "9229:9229"  # Debug port

  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=dev_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_dev_data:/var/lib/postgresql/data

volumes:
  postgres_dev_data:
```

### Override File

```yaml
# docker-compose.override.yml
version: '3.8'

services:
  app:
    volumes:
      - .:/app
    environment:
      - NODE_ENV=development
    command: npm run dev
```

### Development Workflow

```bash
# Start development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Use override file
docker-compose up

# Rebuild on changes
docker-compose up --build

# Watch mode
docker-compose up --force-recreate
```

---

## Production Considerations

### Production Compose File

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    image: registry.example.com/myapp:latest
    restart: always
    environment:
      - NODE_ENV=production
    ports:
      - "3000:3000"
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
        max_attempts: 3

  db:
    image: postgres:15
    restart: always
    environment:
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_prod_data:/var/lib/postgresql/data
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G

volumes:
  postgres_prod_data:
```

### Secrets Management

```yaml
version: '3.8'

services:
  app:
    image: myapp:latest
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    external: true
```

### Resource Limits

```yaml
services:
  app:
    image: myapp:latest
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

---

## Common Stacks

### PERN Stack (Postgres, Express, React, Node)

```yaml
version: '3.8'

services:
  # React Frontend
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    depends_on:
      - backend
    networks:
      - frontend

  # Express/Node Backend
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/app
      - NODE_ENV=production
    depends_on:
      db:
        condition: service_healthy
    networks:
      - frontend
      - backend

  # PostgreSQL Database
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

networks:
  frontend:
  backend:

volumes:
  postgres_data:
```

### FastAPI + PostgreSQL + Redis

```yaml
version: '3.8'

services:
  # FastAPI Application
  api:
    build:
      context: ./app
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - backend

  # PostgreSQL Database
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3
    networks:
      - backend

networks:
  backend:

volumes:
  postgres_data:
  redis_data:
```

### WordPress Stack

```yaml
version: '3.8'

services:
  # WordPress
  wordpress:
    image: wordpress:latest
    ports:
      - "8080:80"
    environment:
      - WORDPRESS_DB_HOST=db
      - WORDPRESS_DB_USER=wordpress
      - WORDPRESS_DB_PASSWORD=wordpress
      - WORDPRESS_DB_NAME=wordpress
    volumes:
      - wordpress_data:/var/www/html
    depends_on:
      db:
        condition: service_healthy
    networks:
      - frontend
      - backend

  # MySQL Database
  db:
    image: mysql:8
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=wordpress
      - MYSQL_USER=wordpress
      - MYSQL_PASSWORD=wordpress
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - backend

  # phpMyAdmin
  phpmyadmin:
    image: phpmyadmin:latest
    ports:
      - "8081:80"
    environment:
      - PMA_HOST=db
      - PMA_USER=wordpress
      - PMA_PASSWORD=wordpress
    depends_on:
      - db
    networks:
      - backend

networks:
  frontend:
  backend:

volumes:
  wordpress_data:
  mysql_data:
```

---

## Best Practices

### 1. Use Multiple Compose Files

```bash
# Development
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up
```

### 2. Use Environment Files

```yaml
services:
  app:
    env_file:
      - .env
```

### 3. Use Health Checks

```yaml
services:
  db:
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### 4. Use Named Volumes

```yaml
volumes:
  postgres_data:
```

### 5. Use Custom Networks

```yaml
networks:
  frontend:
  backend:
```

### 6. Use Restart Policies

```yaml
services:
  app:
    restart: unless-stopped
```

### 7. Set Resource Limits

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### 8. Use Specific Image Tags

```yaml
services:
  db:
    image: postgres:15.3
```

### 9. Don't Expose Ports in Production

```yaml
services:
  app:
    # Development
    ports:
      - "3000:3000"

    # Production
    # No ports exposed, use reverse proxy
```

### 10. Use Secrets for Sensitive Data

```yaml
services:
  app:
    secrets:
      - db_password
```

---

## Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Compose File Reference](https://docs.docker.com/compose/compose-file/)
- [Compose Best Practices](https://docs.docker.com/compose/production/)
