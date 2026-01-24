---
name: Rolling Deployment
description: Gradually replacing application instances with new versions one at a time or in small batches, ensuring zero downtime and enabling fast rollback if issues occur.
---

# Rolling Deployment

> **Current Level:** Intermediate  
> **Domain:** DevOps / Deployment

---

## Overview

Rolling deployment is a strategy where you gradually replace instances of your application with new versions, one at a time or in small batches, ensuring zero downtime. This approach minimizes risk by deploying incrementally and allows for fast rollback if issues are detected.

## What is Rolling Deployment

### Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│  Rolling Deployment Process                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Step 1: Replace 1 instance (v1.0 → v2.0)           │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  v2.0 │ v1.0 │ v1.0 │ v1.0 │               │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Step 2: Replace 2 instances (v1.0 → v2.0)           │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  v2.0 │ v2.0 │ v1.0 │ v1.0 │               │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Step 3: Replace 3 instances (v1.0 → v2.0)           │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  v2.0 │ v2.0 │ v2.0 │ v1.0 │               │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Step 4: Replace 4 instances (v1.0 → v2.0)           │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  v2.0 │ v2.0 │ v2.0 │ v2.0 │               │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why Rolling Deployment

| Benefit | Impact |
|---------|---------|
| **Zero Downtime** | No service interruption |
| **Gradual Rollout** | Replace instances incrementally |
| **Easy Rollback** | Stop and rollback if issues |
| **Resource Efficient** | No need for double infrastructure |
| **Simple to Implement** | Built into most platforms |

## Rolling Update Process

### Step-by-Step Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Rolling Update Steps                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Deploy New Version ──▶ 2. Terminate Old Pod ──▶ 3. Start New Pod ──▶ 4. Wait for Healthy ──▶ 5. Repeat for All Pods │
│                                                                  │
│  └───────────────────────────────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

### Step 1: Deploy New Version

```bash
# Deploy new version
kubectl set image deployment/web-app web-app=web-app:v2.0

# Or apply new deployment manifest
kubectl apply -f deployment-v2.0.yaml
```

### Step 2: Terminate Old Pod

```bash
# Kubernetes automatically terminates old pods
# This is handled by the rolling update strategy
```

### Step 3: Start New Pod

```bash
# Kubernetes automatically starts new pods
# This is handled by the rolling update strategy
```

### Step 4: Wait for Healthy

```bash
# Kubernetes waits for new pods to be healthy
# This is handled by readiness and liveness probes
```

### Step 5: Repeat for All Pods

```bash
# Kubernetes repeats for all pods
# This is handled by the rolling update strategy
```

## Zero-Downtime with Rolling Updates

### Health Checks

```yaml
# Readiness probe (pod is ready to serve traffic)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        image: web-app:v2.0
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            successThreshold: 3
            failureThreshold: 3
```

```yaml
# Liveness probe (pod is alive)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        image: web-app:v2.0
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            successThreshold: 3
            failureThreshold: 3
```

### Graceful Shutdown

```yaml
# Graceful shutdown (SIGTERM)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        image: web-app:v2.0
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 10"]
        terminationGracePeriodSeconds: 30
```

## Health Checks

### Readiness Probe

```yaml
# Readiness probe
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        image: web-app:v2.0
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            successThreshold: 3
            failureThreshold: 3
```

### Liveness Probe

```yaml
# Liveness probe
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        image: web-app:v2.0
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
            successThreshold: 3
            failureThreshold: 3
```

### Startup Probe

```yaml
# Startup probe (for slow-starting apps)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        image: web-app:v2.0
        startupProbe:
          httpGet:
            path: /health
            port: 8080
            initialDelaySeconds: 0
            periodSeconds: 5
            successThreshold: 1
            failureThreshold: 30
```

## Kubernetes Rolling Update

### Default Strategy

```yaml
# Kubernetes rolling update (default strategy)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 4
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Create 1 extra pod during update
      maxUnavailable: 1  # Allow 1 pod to be unavailable during update
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: web-app:v2.0
        ports:
        - containerPort: 8080
```

### Max Unavailable and Max Surge

| Parameter | Description | Default |
|------------|-------------|---------|
| **maxSurge** | Maximum number of pods that can be created above desired | 25% |
| **maxUnavailable** | Maximum number of pods that can be unavailable during update | 25% |

### Custom Rolling Update

```yaml
# Custom rolling update
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 10
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # Create 2 extra pods during update
      maxUnavailable: 2  # Allow 2 pods to be unavailable during update
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: web-app:v2.0
        ports:
        - containerPort: 8080
```

## Rollback During Rolling Update

### Kubernetes Rollback

```bash
# Rollback rolling update
kubectl rollout undo deployment/web-app

# Check rollback status
kubectl rollout status deployment/web-app

# View rollback history
kubectl rollout history deployment/web-app
```

### Rollback to Specific Revision

```bash
# Rollback to specific revision
kubectl rollout undo deployment/web-app --to-revision=3
```

### Rollback Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Rolling Update Rollback Process                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Detect Issues ──▶ 2. Trigger Rollback ──▶ 3. Replace Pods ──▶ 4. Monitor Health │
│                                                                  │
│  └───────────────────────────────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

## Database Schema Compatibility

### Backward-Compatible Schema Changes

```sql
-- Version N: Add new column (nullable)
ALTER TABLE users ADD COLUMN new_feature_enabled BOOLEAN;

-- Version N+1: Populate new column
UPDATE users SET new_feature_enabled = FALSE;

-- Version N+2: Enable feature for new version
UPDATE users SET new_feature_enabled = TRUE;

-- Version N+3: Make column non-nullable
ALTER TABLE users ALTER COLUMN new_feature_enabled SET NOT NULL;
```

### Both Versions Work with Same Schema

```sql
-- Both versions must work with same schema
-- Old version: Ignores new column
-- New version: Uses new column

-- Example:
-- Old version
SELECT * FROM users;

-- New version
SELECT *, new_feature_enabled FROM users;
```

## Session Handling During Rolling Update

### Sticky Sessions

```yaml
# Sticky sessions (session affinity)
apiVersion: v1
kind: Service
metadata:
  name: web-app
spec:
  selector:
    app: web-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
  sessionAffinity: ClientIP
  sessionAffinityConfig:
    clientIP:
      timeoutSeconds: 10800
```

### Shared Session Store

```yaml
# Shared session store (Redis)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  template:
    spec:
      containers:
      - name: web-app
        image: web-app:v2.0
        env:
        - name: REDIS_HOST
          value: redis-service
        - name: REDIS_PORT
          value: "6379"
```

### Stateless Apps

```python
# Stateless app: No session handling needed
def handle_request(request):
    """Handle request without session."""
    # Process request
    response = process_request(request)
    
    # Return response
    return response
```

## Monitoring Rolling Updates

### Watch Rollout Status

```bash
# Watch rollout status
kubectl rollout status deployment/web-app

# Or watch pods
watch -n 1 kubectl get pods -l app=web-app
```

### Check Logs

```bash
# Check logs for new pods
kubectl logs -f deployment/web-app-<pod-name>

# Check logs for old pods
kubectl logs -f deployment/web-app-<old-pod-name>
```

### Monitor Metrics

```python
# Monitor metrics during rolling update
def monitor_rolling_update():
    """Monitor metrics during rolling update."""
    while True:
        try:
            # Check error rate
            error_rate = get_error_rate()
            print(f"Error rate: {error_rate}%")
            
            # Check latency
            latency = get_latency()
            print(f"Latency: {latency}ms")
            
            # Check if metrics are healthy
            if error_rate > 5 or latency > 1000:
                print("Metrics unhealthy, rolling back")
                rollback_rolling_update()
                break
            
            print("Metrics healthy")
            
        except Exception as e:
            print(f"Error monitoring: {e}")
            
        time.sleep(60)  # Check every minute

monitor_rolling_update()
```

## Tools

### Kubernetes

```bash
# Kubernetes rolling update
kubectl set image deployment/web-app web-app=web-app:v2.0

# Check rollout status
kubectl rollout status deployment/web-app

# Rollback
kubectl rollout undo deployment/web-app
```

### AWS ECS

```bash
# AWS ECS rolling update
aws ecs update-service \
  --cluster my-cluster \
  --service web-app \
  --force-new-deployment

# Check deployment status
aws ecs describe-services \
  --cluster my-cluster \
  --services web-app
```

### Docker Swarm

```bash
# Docker Swarm rolling update
docker service update \
  --image web-app:v2.0 \
  --update-parallelism 1 \
  --update-delay 10s \
  web-app

# Check service status
docker service ps web-app
```

### Cloud Foundry

```bash
# Cloud Foundry rolling update
cf push web-app -v v2.0

# Check app status
cf app web-app
```

## Real Examples

### Example 1: Kubernetes Rolling Update

**Scenario**: Deploy new API version

**Timeline**:
- 09:00: Deploy v2.0
- 09:05: Pod 1 replaced (v1.0 → v2.0)
- 09:10: Pod 2 replaced (v1.0 → v2.0)
- 09:15: Pod 3 replaced (v1.0 → v2.0)
- 09:20: Pod 4 replaced (v1.0 → v2.0)
- 09:25: All pods running v2.0

**Outcome**: Successful deployment, zero downtime

### Example 2: AWS ECS Rolling Update

**Scenario**: Deploy web application

**Timeline**:
- 14:00: Deploy v2.0
- 14:05: Task 1 replaced (v1.0 → v2.0)
- 14:10: Task 2 replaced (v1.0 → v2.0)
- 14:15: Task 3 replaced (v1.0 → v2.0)
- 14:20: Task 4 replaced (v1.0 → v2.0)
- 14:25: All tasks running v2.0

**Outcome**: Successful deployment, zero downtime

### Example 3: Docker Swarm Rolling Update

**Scenario**: Deploy microservice

**Timeline**:
- 10:00: Deploy v2.0
- 10:05: Container 1 replaced (v1.0 → v2.0)
- 10:10: Container 2 replaced (v1.0 → v2.0)
- 10:15: Container 3 replaced (v1.0 → v2.0)
- 10:20: Container 4 replaced (v1.0 → v2.0)
- 10:25: All containers running v2.0

**Outcome**: Successful deployment, zero downtime

## Summary Checklist

### Preparation

- [ ] Health checks configured
- [ ] Graceful shutdown implemented
- [ ] Rolling update strategy defined
- [ ] Rollback plan documented
- [ ] Monitoring configured

### Deployment

- [ ] Deploy new version
- [ ] Monitor pod replacement
- [ ] Check health checks
- [ ] Monitor metrics
- [ ] Verify zero downtime
- [ ] Complete rollout
```

---

## Quick Start

### Kubernetes Rolling Update

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 5
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # Allow 1 extra pod during update
      maxUnavailable: 1  # Allow 1 pod unavailable
  template:
    spec:
      containers:
      - name: app
        image: myapp:v2
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Rolling Update Command

```bash
# Update deployment
kubectl set image deployment/myapp app=myapp:v2

# Watch rollout
kubectl rollout status deployment/myapp

# Rollback if needed
kubectl rollout undo deployment/myapp
```

---

## Production Checklist

- [ ] **Strategy**: Rolling update strategy configured
- [ ] **Health Checks**: Readiness and liveness probes configured
- [ ] **Max Surge**: Configure max surge (extra pods during update)
- [ ] **Max Unavailable**: Configure max unavailable pods
- [ ] **Monitoring**: Monitor deployment progress
- [ ] **Rollback**: Rollback procedure tested
- [ ] **Zero Downtime**: Verify zero downtime during rollout
- [ ] **Testing**: Test rolling update in staging
- [ ] **Documentation**: Document deployment process
- [ ] **Automation**: Automate rolling updates in CI/CD
- [ ] **Validation**: Validate new version before full rollout
- [ ] **Communication**: Notify team of deployment

---

## Anti-patterns

### ❌ Don't: No Health Checks

```yaml
# ❌ Bad - No health checks
containers:
- name: app
  image: myapp:v2
  # No readiness probe!
```

```yaml
# ✅ Good - Health checks
containers:
- name: app
  image: myapp:v2
  readinessProbe:
    httpGet:
      path: /health
      port: 8080
  livenessProbe:
    httpGet:
      path: /live
      port: 8080
```

### ❌ Don't: Too Fast Rollout

```yaml
# ❌ Bad - Replace all at once
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 5  # Replace all at once!
    maxUnavailable: 5
```

```yaml
# ✅ Good - Gradual replacement
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 1        # One at a time
    maxUnavailable: 1  # One unavailable
```

---

## Integration Points

- **Canary Deployment** (`26-deployment-strategies/canary-deployment/`) - Alternative strategy
- **Rollback Strategies** (`26-deployment-strategies/rollback-strategies/`) - Rollback procedures
- **CI/CD** (`15-devops-infrastructure/ci-cd-github-actions/`) - Automated deployments

---

## Further Reading

- [Kubernetes Rolling Updates](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-update-deployment)
- [Deployment Strategies](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [ ] Verify all pods healthy

### Rollback

- [ ] Detect issues
- [ ] Trigger rollback
- [ ] Monitor rollback
- [ ] Verify system health
- [ ] Document issues

### Post-Deployment

- [ ] Review metrics
- [ ] Document deployment
- [ ] Lessons learned
- [ ] Process improved
