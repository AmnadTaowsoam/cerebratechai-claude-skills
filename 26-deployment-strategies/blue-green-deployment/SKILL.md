---
name: Blue-Green Deployment
description: Deploying new version alongside existing version, switching traffic to new version after validation, enabling instant rollback by switching back to old version for zero-downtime deployments.
---

# Blue-Green Deployment

> **Current Level:** Intermediate  
> **Domain:** DevOps / Deployment

---

## Overview

Blue-Green deployment maintains two identical production environments (blue and green). One environment serves live traffic while the other hosts the new version. After validation, traffic switches to the new environment, enabling instant rollback by switching back.

## What is Blue-Green Deployment

Blue-Green deployment is a deployment strategy where you maintain two identical production environments. One environment (blue) serves live traffic while the other (green) hosts the new version. After validation, traffic switches to the green environment, enabling instant rollback by switching back to blue.

### Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│  Blue-Green Deployment Process                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Step 1: Deploy to Green (idle)                        │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Blue (Live) │ Green (New, Idle) │             │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Step 2: Validate Green                                  │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Blue (Live) │ Green (Validated) │             │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Step 3: Switch Traffic to Green                       │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Blue (Idle) │ Green (Live) │                   │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Rollback: Switch back to Blue                        │     │
│  │  ┌─────────────────────────────────────────────────┐   │     │
│  │  │  Blue (Live) │ Green (Idle) │                   │   │     │
│  │  └─────────────────────────────────────────────────┘   │     │
│  └─────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
```

### Benefits

| Benefit | Description |
|---------|-------------|
| **Zero Downtime** | No downtime during deployment |
| **Instant Rollback** | Switch back immediately if issues |
| **Safe Testing** | Test new version before switching |
| **No Impact** | Old version continues serving traffic |

---

## Core Concepts

### Blue-Green Architecture

```yaml
# Kubernetes example
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  selector:
    version: blue  # Current live version
  ports:
  - port: 80
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-blue
spec:
  replicas: 3
  template:
    metadata:
      labels:
        version: blue
    spec:
      containers:
      - name: app
        image: app:v1.0
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-green
spec:
  replicas: 3
  template:
    metadata:
      labels:
        version: green
    spec:
      containers:
      - name: app
        image: app:v2.0
```

### Traffic Switching

```typescript
// Switch traffic from blue to green
async function switchToGreen() {
  // Update service selector
  await k8s.patchService('app-service', {
    spec: {
      selector: { version: 'green' }
    }
  })
  
  // Monitor green
  await monitorGreen()
  
  // If issues, switch back
  if (hasIssues()) {
    await switchToBlue()
  }
}
```

---

## Quick Start

### Kubernetes Blue-Green

```yaml
# Deploy green version
kubectl apply -f app-green.yaml

# Validate green
kubectl get pods -l version=green
kubectl port-forward pod/green-pod 8080:80
# Test locally

# Switch traffic
kubectl patch service app-service -p '{"spec":{"selector":{"version":"green"}}}'

# Rollback if needed
kubectl patch service app-service -p '{"spec":{"selector":{"version":"blue"}}}'
```

### Load Balancer Switching

```typescript
// AWS ALB example
async function switchToGreen() {
  const targetGroup = await getTargetGroup('green')
  
  // Update listener to point to green
  await elb.modifyListener({
    ListenerArn: listenerArn,
    DefaultActions: [{
      Type: 'forward',
      TargetGroupArn: targetGroup.Arn
    }]
  })
}
```

---

## Production Checklist

- [ ] **Environment Setup**: Two identical environments
- [ ] **Database**: Database migration strategy
- [ ] **Traffic Switching**: Load balancer or service switching
- [ ] **Validation**: Validate green before switching
- [ ] **Monitoring**: Monitor both environments
- [ ] **Rollback Plan**: Instant rollback procedure
- [ ] **Testing**: Test switching process
- [ ] **Documentation**: Document deployment process
- [ ] **Automation**: Automate switching
- [ ] **Communication**: Notify team of deployment
- [ ] **Cost**: Consider infrastructure costs
- [ ] **Cleanup**: Clean up old environment after validation

---

## Anti-patterns

### ❌ Don't: Database Mismatch

```yaml
# ❌ Bad - Different database versions
Blue: Database v1
Green: Database v2
# Schema mismatch!
```

```yaml
# ✅ Good - Compatible databases
Blue: Database v1
Green: Database v1 (compatible with v2 code)
# Or migrate database before switching
```

### ❌ Don't: No Validation

```typescript
// ❌ Bad - Switch without validation
await switchToGreen()
// What if green is broken?
```

```typescript
// ✅ Good - Validate first
await deployToGreen()
await validateGreen()  // Health checks, smoke tests
if (greenHealthy) {
  await switchToGreen()
}
```

---

## Integration Points

- **Canary Deployment** (`26-deployment-strategies/canary-deployment/`) - Alternative strategy
- **Rollback Strategies** (`26-deployment-strategies/rollback-strategies/`) - Rollback procedures
- **Monitoring** (`14-monitoring-observability/`) - Deployment monitoring

---

## Further Reading

- [Blue-Green Deployment](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Kubernetes Blue-Green](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#blue-green-deployment)
