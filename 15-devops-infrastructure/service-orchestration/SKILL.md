# Service Orchestration

## Overview

Patterns for orchestrating multiple microservices in Docker Compose and Kubernetes environments. This skill covers service dependency management, health checks, service discovery, load balancing, and deployment strategies.

---

## 1. Service Orchestration Architecture

### Microservices Architecture

```markdown
# Service Orchestration

## Components
1. **API Gateway**: Entry point for all requests
2. **Service Registry**: Service discovery
3. **Load Balancer**: Distribute traffic
4. **Health Checker**: Monitor service health
5. **Configuration Server**: Centralized config
6. **Message Queue**: Async communication

## Service Communication
```
Client → API Gateway → Service A → Message Queue → Service B
                ↓                        ↓
         Service Registry         Service Discovery
                ↓                        ↓
         Health Checks            Load Balancing
```

## Orchestration Platforms
- Docker Compose (Development)
- Kubernetes (Production)
- Docker Swarm (Alternative)
```

---

## 2. Docker Compose Orchestration

### Multi-Service Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  # API Gateway
  api-gateway:
    build: ./services/api-gateway
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - SERVICES_URL=http://service-registry:8500
    depends_on:
      - service-registry
      - auth-service
      - event-service
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - malai-network
    restart: unless-stopped

  # Service Registry (Consul)
  service-registry:
    image: consul:latest
    ports:
      - "8500:8500"
    command: agent -server -ui -bootstrap-expect=1 -client=0.0.0.0
    networks:
      - malai-network
    volumes:
      - consul-data:/consul/data
    restart: unless-stopped

  # Authentication Service
  auth-service:
    build: ./services/auth
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/auth
      - REDIS_URL=redis://redis:6379
      - JWT_SECRET=${JWT_SECRET}
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - malai-network
    restart: unless-stopped

  # Event Service
  event-service:
    build: ./services/events
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/events
      - RABBITMQ_URL=amqp://rabbitmq:5672
    depends_on:
      postgres:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - malai-network
    deploy:
      replicas: 2
    restart: unless-stopped

  # Payment Service
  payment-service:
    build: ./services/payment
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/payment
      - OMISE_SECRET_KEY=${OMISE_SECRET_KEY}
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4002/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - malai-network
    restart: unless-stopped

  # Notification Service
  notification-service:
    build: ./services/notification
    environment:
      - RABBITMQ_URL=amqp://rabbitmq:5672
      - LINE_CHANNEL_ACCESS_TOKEN=${LINE_CHANNEL_ACCESS_TOKEN}
      - SMTP_HOST=${SMTP_HOST}
    depends_on:
      rabbitmq:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4003/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - malai-network
    restart: unless-stopped

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_MULTIPLE_DATABASES=auth,events,payment
    ports:
      - "5432:5432"
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./scripts/init-databases.sh:/docker-entrypoint-initdb.d/init-databases.sh
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - malai-network
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - malai-network
    restart: unless-stopped

  # RabbitMQ Message Queue
  rabbitmq:
    image: rabbitmq:3-management-alpine
    ports:
      - "5672:5672"
      - "15672:15672"
    environment:
      - RABBITMQ_DEFAULT_USER=admin
      - RABBITMQ_DEFAULT_PASS=admin
    volumes:
      - rabbitmq-data:/var/lib/rabbitmq
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    networks:
      - malai-network
    restart: unless-stopped

  # Nginx Load Balancer
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - api-gateway
    networks:
      - malai-network
    restart: unless-stopped

networks:
  malai-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
  rabbitmq-data:
  consul-data:
```

### Service Health Checks

```typescript
// Health Check Implementation
import express from 'express'

interface HealthCheckResult {
  status: 'healthy' | 'unhealthy'
  timestamp: string
  uptime: number
  dependencies: {
    [key: string]: {
      status: 'up' | 'down'
      responseTime?: number
    }
  }
}

class HealthChecker {
  private app: express.Application

  constructor(app: express.Application) {
    this.app = app
  }

  setupHealthEndpoints(): void {
    // Liveness probe - is the service running?
    this.app.get('/health/live', (req, res) => {
      res.status(200).json({ status: 'alive' })
    })

    // Readiness probe - is the service ready to accept traffic?
    this.app.get('/health/ready', async (req, res) => {
      const isReady = await this.checkReadiness()

      if (isReady) {
        res.status(200).json({ status: 'ready' })
      } else {
        res.status(503).json({ status: 'not ready' })
      }
    })

    // Detailed health check
    this.app.get('/health', async (req, res) => {
      const health = await this.getDetailedHealth()

      const statusCode = health.status === 'healthy' ? 200 : 503
      res.status(statusCode).json(health)
    })
  }

  private async checkReadiness(): Promise<boolean> {
    try {
      // Check database connection
      await this.checkDatabase()

      // Check cache connection
      await this.checkCache()

      // Check message queue
      await this.checkMessageQueue()

      return true
    } catch (error) {
      return false
    }
  }

  private async getDetailedHealth(): Promise<HealthCheckResult> {
    const dependencies: HealthCheckResult['dependencies'] = {}

    // Check database
    try {
      const start = Date.now()
      await this.checkDatabase()
      dependencies.database = {
        status: 'up',
        responseTime: Date.now() - start,
      }
    } catch (error) {
      dependencies.database = { status: 'down' }
    }

    // Check cache
    try {
      const start = Date.now()
      await this.checkCache()
      dependencies.cache = {
        status: 'up',
        responseTime: Date.now() - start,
      }
    } catch (error) {
      dependencies.cache = { status: 'down' }
    }

    // Check message queue
    try {
      const start = Date.now()
      await this.checkMessageQueue()
      dependencies.messageQueue = {
        status: 'up',
        responseTime: Date.now() - start,
      }
    } catch (error) {
      dependencies.messageQueue = { status: 'down' }
    }

    const allHealthy = Object.values(dependencies).every(
      (dep) => dep.status === 'up'
    )

    return {
      status: allHealthy ? 'healthy' : 'unhealthy',
      timestamp: new Date().toISOString(),
      uptime: process.uptime(),
      dependencies,
    }
  }

  private async checkDatabase(): Promise<void> {
    // Implementation depends on database client
    // Example with Prisma:
    // await prisma.$queryRaw`SELECT 1`
  }

  private async checkCache(): Promise<void> {
    // Implementation depends on cache client
    // Example with Redis:
    // await redis.ping()
  }

  private async checkMessageQueue(): Promise<void> {
    // Implementation depends on message queue client
    // Example with RabbitMQ:
    // await channel.checkQueue('test')
  }
}

// Usage
const app = express()
const healthChecker = new HealthChecker(app)
healthChecker.setupHealthEndpoints()
```

---

## 3. Kubernetes Orchestration

### Kubernetes Deployment

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: event-service
  namespace: malai
  labels:
    app: event-service
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: event-service
  template:
    metadata:
      labels:
        app: event-service
        version: v1
    spec:
      containers:
      - name: event-service
        image: malai/event-service:latest
        ports:
        - containerPort: 4001
          name: http
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secrets
              key: url
        - name: NODE_ENV
          value: "production"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 4001
          initialDelaySeconds: 30
          periodSeconds: 10
          timeoutSeconds: 5
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 4001
          initialDelaySeconds: 10
          periodSeconds: 5
          timeoutSeconds: 3
          failureThreshold: 3
      initContainers:
      - name: wait-for-db
        image: busybox:latest
        command: ['sh', '-c', 'until nc -z postgres 5432; do sleep 2; done']

---
apiVersion: v1
kind: Service
metadata:
  name: event-service
  namespace: malai
spec:
  selector:
    app: event-service
  ports:
  - port: 80
    targetPort: 4001
    protocol: TCP
  type: ClusterIP

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: event-service-hpa
  namespace: malai
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: event-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## 4. Service Discovery

### Consul Service Registration

```typescript
// Service Registration with Consul
import Consul from 'consul'

interface ServiceConfig {
  name: string
  id: string
  port: number
  address: string
  tags?: string[]
  healthCheckPath?: string
}

class ServiceRegistry {
  private consul: Consul.Consul

  constructor(consulHost: string = 'localhost', consulPort: number = 8500) {
    this.consul = new Consul({
      host: consulHost,
      port: consulPort,
      promisify: true,
    })
  }

  async registerService(config: ServiceConfig): Promise<void> {
    const registration = {
      name: config.name,
      id: config.id,
      address: config.address,
      port: config.port,
      tags: config.tags || [],
      check: {
        http: `http://${config.address}:${config.port}${config.healthCheckPath || '/health'}`,
        interval: '10s',
        timeout: '5s',
      },
    }

    try {
      await this.consul.agent.service.register(registration)
      console.log(`Service ${config.name} registered successfully`)
    } catch (error) {
      console.error('Service registration failed:', error)
      throw error
    }
  }

  async deregisterService(serviceId: string): Promise<void> {
    try {
      await this.consul.agent.service.deregister(serviceId)
      console.log(`Service ${serviceId} deregistered successfully`)
    } catch (error) {
      console.error('Service deregistration failed:', error)
      throw error
    }
  }

  async discoverService(serviceName: string): Promise<string[]> {
    try {
      const result = await this.consul.health.service({
        service: serviceName,
        passing: true,
      })

      return result.map((service: any) => {
        const address = service.Service.Address
        const port = service.Service.Port
        return `http://${address}:${port}`
      })
    } catch (error) {
      console.error('Service discovery failed:', error)
      return []
    }
  }
}

// Usage
const registry = new ServiceRegistry()

// Register service on startup
await registry.registerService({
  name: 'event-service',
  id: `event-service-${process.env.HOSTNAME}`,
  port: 4001,
  address: process.env.SERVICE_ADDRESS || 'localhost',
  tags: ['api', 'events'],
  healthCheckPath: '/health',
})

// Discover other services
const authServiceUrls = await registry.discoverService('auth-service')
console.log('Auth service instances:', authServiceUrls)

// Deregister on shutdown
process.on('SIGTERM', async () => {
  await registry.deregisterService(`event-service-${process.env.HOSTNAME}`)
  process.exit(0)
})
```

---

## 5. Load Balancing

### Nginx Load Balancer Configuration

```nginx
# nginx/nginx.conf
upstream api_gateway {
    least_conn;
    server api-gateway-1:3000 weight=1 max_fails=3 fail_timeout=30s;
    server api-gateway-2:3000 weight=1 max_fails=3 fail_timeout=30s;
    server api-gateway-3:3000 weight=1 max_fails=3 fail_timeout=30s;
}

upstream event_service {
    ip_hash;
    server event-service-1:4001;
    server event-service-2:4001;
    server event-service-3:4001;
}

server {
    listen 80;
    server_name malai.app;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name malai.app;

    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;

    # API Gateway
    location /api/ {
        proxy_pass http://api_gateway;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;

        # Health check
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503;
    }

    # WebSocket support
    location /ws/ {
        proxy_pass http://api_gateway;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }

    # Health check endpoint
    location /health {
        access_log off;
        return 200 "healthy\n";
        add_header Content-Type text/plain;
    }
}
```

---

## 6. Deployment Strategies

### Blue-Green Deployment

```yaml
# Blue-Green Deployment Script
#!/bin/bash

# Deploy new version (green)
kubectl apply -f k8s/deployment-green.yaml

# Wait for green deployment to be ready
kubectl wait --for=condition=available --timeout=300s deployment/event-service-green

# Run smoke tests
./scripts/smoke-test.sh event-service-green

if [ $? -eq 0 ]; then
    echo "Smoke tests passed. Switching traffic to green..."
    
    # Switch service to green
    kubectl patch service event-service -p '{"spec":{"selector":{"version":"green"}}}'
    
    echo "Traffic switched to green. Monitoring..."
    sleep 60
    
    # Check metrics
    ./scripts/check-metrics.sh
    
    if [ $? -eq 0 ]; then
        echo "Deployment successful. Removing blue..."
        kubectl delete deployment event-service-blue
    else
        echo "Metrics check failed. Rolling back..."
        kubectl patch service event-service -p '{"spec":{"selector":{"version":"blue"}}}'
        kubectl delete deployment event-service-green
    fi
else
    echo "Smoke tests failed. Rolling back..."
    kubectl delete deployment event-service-green
fi
```

### Canary Deployment

```yaml
# Canary Deployment with Istio
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: event-service
spec:
  hosts:
  - event-service
  http:
  - match:
    - headers:
        canary:
          exact: "true"
    route:
    - destination:
        host: event-service
        subset: v2
  - route:
    - destination:
        host: event-service
        subset: v1
      weight: 90
    - destination:
        host: event-service
        subset: v2
      weight: 10

---
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: event-service
spec:
  host: event-service
  subsets:
  - name: v1
    labels:
      version: v1
  - name: v2
    labels:
      version: v2
```

---

## Best Practices

1. **Service Design**
   - Single responsibility per service
   - Stateless services
   - API versioning
   - Graceful degradation

2. **Health Checks**
   - Liveness and readiness probes
   - Dependency health checks
   - Timeout configuration
   - Retry mechanisms

3. **Resource Management**
   - CPU and memory limits
   - Auto-scaling policies
   - Resource quotas
   - Cost optimization

4. **Monitoring**
   - Centralized logging
   - Distributed tracing
   - Metrics collection
   - Alerting

5. **Security**
   - Service-to-service authentication
   - Network policies
   - Secrets management
   - TLS encryption

---

## Common Pitfalls

1. **Circular Dependencies**: Services depending on each other
2. **Missing Health Checks**: No proper health monitoring
3. **Resource Limits**: Not setting resource constraints
4. **Hardcoded Configuration**: Not using environment variables
5. **No Graceful Shutdown**: Services not handling SIGTERM

---

## Production Checklist

- [ ] Health checks configured
- [ ] Resource limits set
- [ ] Auto-scaling enabled
- [ ] Monitoring configured
- [ ] Logging centralized
- [ ] Secrets secured
- [ ] Network policies defined
- [ ] Backup strategy implemented
- [ ] Disaster recovery plan
- [ ] Documentation complete

---

## Tools & Libraries

| Tool | Purpose |
|------|---------|
| Docker Compose | Local orchestration |
| Kubernetes | Production orchestration |
| Consul | Service discovery |
| Nginx | Load balancing |
| Istio | Service mesh |

---

## Further Reading

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Service Mesh Patterns](https://www.nginx.com/blog/what-is-a-service-mesh/)
- [Microservices Patterns](https://microservices.io/patterns/)
