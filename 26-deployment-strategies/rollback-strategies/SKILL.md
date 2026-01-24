---
name: Rollback Strategies
description: Reverting to a previous version of application or infrastructure after a deployment causes issues, including automated rollback, database rollback, and blue-green rollback strategies.
---

# Rollback Strategies

> **Current Level:** Intermediate  
> **Domain:** DevOps / Deployment

---

## Overview

Rollback is the process of reverting to a previous version of your application or infrastructure after a deployment causes issues. Effective rollback strategies include automated rollback triggers, database migration rollbacks, and blue-green deployment rollbacks to minimize downtime and data loss.

## What is Rollback

### Core Concept

```
┌─────────────────────────────────────────────────────────────────┐
│  Rollback Concept                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Deploy v2.0 ──▶ Issues Detected ──▶ Rollback to v1.0 │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Rollback Types:                                        │     │
│  │  - Full Rollback (revert entire deployment)             │     │
│  │  - Partial Rollback (revert specific component)          │     │
│  │  - Forward Fix (fix bug in new version)                  │     │
│  └─────────────────────────────────────────────────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why Rollback is Needed

| Scenario | Impact |
|----------|---------|
| **Deployment Issues** | Bugs in new version |
| **Performance Degradation** | Slower response times |
| **Data Corruption** | Incorrect data processing |
| **Security Vulnerabilities** | New security issues |
| **Configuration Errors** | Misconfigured settings |

## Types of Rollback

### Full Rollback

```bash
# Full rollback (revert entire deployment)
kubectl rollout undo deployment/web-app

# Or specify revision
kubectl rollout undo deployment/web-app --to-revision=3
```

### Partial Rollback

```bash
# Partial rollback (revert specific component)
kubectl rollout undo deployment/web-app-frontend

# Keep other components at new version
```

### Forward Fix

```python
# Forward fix (fix bug in new version)
def forward_fix():
    # Fix bug in new version
    fix_bug_in_v2()
    
    # Deploy fixed version
    deploy_v2_1()
    
    # No rollback needed
    print("Forward fix deployed")

forward_fix()
```

## Rollback Triggers

### Manual Triggers

```javascript
// Manual rollback trigger
function manualRollbackTrigger() {
    // User manually triggers rollback
    if (userClickedRollbackButton()) {
        rollbackToPreviousVersion();
    }
}
```

### Automated Triggers

```python
# Automated rollback trigger
def automatedRollbackTrigger():
    """Automatically rollback if metrics are unhealthy."""
    error_rate = get_error_rate()
    latency = get_latency()
    
    if error_rate > 5 or latency > 1000:
        print("Metrics unhealthy, rolling back")
        rollbackToPreviousVersion()
```

### Alert-Based Triggers

```javascript
// Alert-based rollback trigger
function alertBasedRollbackTrigger() {
    // Rollback if alert fires
    if (alertFired('high_error_rate')) {
        rollbackToPreviousVersion();
    }
}
```

## Blue-Green Rollback

### Instant Rollback

```bash
# Blue-green rollback (instant, switch traffic back)
kubectl patch service web-app -p '{"spec":{"template":{"spec":{"containers":[{"name":"web-app","image":"web-app:v1.0"}]}}}}'

# Or update DNS
aws route53 change-resource-record \
  --hosted-zone-id Z1234567890 \
  --change-batch-file rollback.json
```

### Rollback Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Blue-Green Rollback Process                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Detect Issues ──▶ 2. Switch Traffic to Blue ──▶ 3. Monitor Blue ──▶ 4. Green Becomes Staging │
│                                                                  │
│  └───────────────────────────────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

### Rollback Script

```python
# Blue-green rollback script
def blue_green_rollback():
    """Rollback from green to blue."""
    print("Rolling back to blue...")
    
    try:
        # Update load balancer to route to blue
        response = requests.post(
            'http://load-balancer/api/switch',
            json={'target': 'blue'}
        )
        response.raise_for_status()
        print(f"✓ Rolled back to blue")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Rollback failed: {e}")
        # Manual intervention required
        send_alert('Rollback failed, manual intervention required')

blue_green_rollback()
```

## Canary Rollback

### Stop Rollout

```yaml
# Stop canary rollout
apiVersion: flagger.app/v1beta1
kind: Canary
metadata:
  name: web-app
spec:
  analysis:
    rollbackEnabled: true
    threshold: 5
```

### Shift Traffic Back

```bash
# Shift traffic back to old version
kubectl patch virtualservice web-app -p '{"spec":{"http":[{"route":[{"destination":{"host":"web-app","subset":"v1"},"weight":100}]}]}}'
```

### Rollback Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Canary Rollback Process                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Detect Issues ──▶ 2. Stop Rollout ──▶ 3. Shift Traffic Back ──▶ 4. Delete Canary │
│                                                                  │
│  └───────────────────────────────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

### Rollback Script

```python
# Canary rollback script
def canary_rollback():
    """Rollback canary deployment."""
    print("Rolling back canary...")
    
    try:
        # Stop canary rollout
        stop_canary_rollout()
        
        # Shift traffic back to old version
        shift_traffic_back()
        
        # Delete canary deployment
        delete_canary_deployment()
        
        print("✓ Canary rolled back")
        
    except Exception as e:
        print(f"✗ Rollback failed: {e}")
        send_alert('Canary rollback failed')

canary_rollback()
```

## Rolling Update Rollback

### Kubernetes Rollback

```bash
# Kubernetes rolling update rollback
kubectl rollout undo deployment/web-app

# Check rollback status
kubectl rollout status deployment/web-app
```

### Rollback Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Rolling Update Rollback Process                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Detect Issues ──▶ 2. Trigger Rollback ──▶ 3. Replace Pods ──▶ 4. Monitor Health │
│                                                                  │
│  └───────────────────────────────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

### Rollback Script

```python
# Rolling update rollback script
def rolling_update_rollback():
    """Rollback rolling update."""
    print("Rolling back rolling update...")
    
    try:
        # Trigger rollback
        subprocess.run(['kubectl', 'rollout', 'undo', 'deployment/web-app'], check=True)
        
        # Wait for rollback to complete
        subprocess.run(['kubectl', 'rollout', 'status', 'deployment/web-app'], check=True)
        
        print("✓ Rolling update rolled back")
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Rollback failed: {e}")
        send_alert('Rolling update rollback failed')

rolling_update_rollback()
```

## Database Rollback

### Schema Migration Rollback

```sql
-- Rollback schema migration
-- Version N+2: Make column nullable (revert from non-nullable)
ALTER TABLE users ALTER COLUMN new_feature_enabled DROP NOT NULL;

-- Version N+1: Remove data (revert from populate)
-- DELETE FROM users WHERE new_feature_enabled = TRUE;

-- Version N: Drop column (revert from add)
ALTER TABLE users DROP COLUMN new_feature_enabled;
```

### Data Migration Rollback

```sql
-- Rollback data migration
-- Restore from backup
-- Example: Restore users table from backup
-- DROP TABLE users;
-- CREATE TABLE users AS SELECT * FROM users_backup;
```

### Rollback Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Database Rollback Process                                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Detect Issues ──▶ 2. Stop Application ──▶ 3. Rollback Schema ──▶ 4. Restore Data ──▶ 5. Restart Application │
│                                                                  │
│  └───────────────────────────────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

### Rollback Script

```python
# Database rollback script
def database_rollback():
    """Rollback database changes."""
    print("Rolling back database...")
    
    try:
        # Stop application
        stop_application()
        
        # Rollback schema
        rollback_schema()
        
        # Restore data
        restore_data()
        
        # Restart application
        start_application()
        
        print("✓ Database rolled back")
        
    except Exception as e:
        print(f"✗ Rollback failed: {e}")
        send_alert('Database rollback failed')

database_rollback()
```

## Forward Fix

### Fix Bug in New Version

```python
# Forward fix (fix bug in new version)
def forward_fix():
    """Fix bug in new version and deploy."""
    print("Forward fix: fixing bug in v2.0...")
    
    try:
        # Fix bug
        fix_bug_in_v2()
        
        # Deploy fixed version
        deploy_v2_1()
        
        # No rollback needed
        print("✓ Forward fix deployed")
        
    except Exception as e:
        print(f"✗ Forward fix failed: {e}")
        # Fallback to rollback
        rollback_to_previous_version()

forward_fix()
```

### When to Use Forward Fix

| Scenario | Use Forward Fix? |
|----------|------------------|
| **Minor Bug** | Yes |
| **Critical Bug** | No (rollback) |
| **Quick Fix** | Yes |
| **Complex Fix** | No (rollback) |
| **Rollback Impossible** | Yes |

## Rollback Testing

### Test Rollback in Staging

```python
# Test rollback in staging
def test_rollback_in_staging():
    """Test rollback procedure in staging."""
    print("Testing rollback in staging...")
    
    try:
        # Deploy to staging
        deploy_to_staging()
        
        # Trigger rollback
        rollback_staging()
        
        # Verify rollback
        verify_rollback()
        
        print("✓ Rollback test passed")
        
    except Exception as e:
        print(f"✗ Rollback test failed: {e}")
        send_alert('Rollback test failed')

test_rollback_in_staging()
```

### Rollback Test Checklist

| Test | Description |
|------|-------------|
| **Full Rollback** | Test complete rollback |
| **Partial Rollback** | Test component rollback |
| **Database Rollback** | Test schema/data rollback |
| **Rollback Time** | Measure rollback duration |
| **Rollback Verification** | Verify system health |

## Automated Rollback

### Metric-Based Rollback

```python
# Automated rollback based on metrics
def automated_metric_based_rollback():
    """Automatically rollback if metrics are unhealthy."""
    while True:
        try:
            # Check error rate
            error_rate = get_error_rate()
            
            # Check latency
            latency = get_latency()
            
            # Check if metrics are unhealthy
            if error_rate > 5 or latency > 1000:
                print("Metrics unhealthy, rolling back")
                rollback_to_previous_version()
                break
            
            print("Metrics healthy")
            
        except Exception as e:
            print(f"Error monitoring: {e}")
            
        time.sleep(60)  # Check every minute

automated_metric_based_rollback()
```

### Alert-Based Rollback

```javascript
// Alert-based rollback
function alertBasedRollback() {
    // Rollback if alert fires
    if (alertFired('high_error_rate') || alertFired('high_latency')) {
        rollbackToPreviousVersion();
    }
}
```

### Rollback Automation Script

```python
# Rollback automation script
def rollback_automation():
    """Automate rollback process."""
    print("Starting rollback automation...")
    
    # Monitor metrics
    while True:
        try:
            # Check metrics
            metrics = get_metrics()
            
            # Check if rollback needed
            if should_rollback(metrics):
                # Rollback
                rollback_to_previous_version()
                
                # Send alert
                send_alert('Automated rollback triggered')
                
                break
            
            # Wait before next check
            time.sleep(60)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)

rollback_automation()
```

## Rollback vs Rollforward

### Rollback

```python
# Rollback (revert to previous version)
def rollback():
    """Revert to previous version."""
    print("Rolling back to previous version...")
    
    # Revert to previous version
    revert_to_previous_version()
    
    print("✓ Rolled back")
```

### Rollforward

```python
# Rollforward (fix bug in new version)
def rollforward():
    """Fix bug in new version and deploy."""
    print("Rolling forward: fixing bug in new version...")
    
    # Fix bug in new version
    fix_bug_in_new_version()
    
    # Deploy fixed version
    deploy_fixed_version()
    
    print("✓ Rolled forward")
```

### Decision Tree

```
┌─────────────────────────────────────────────────────────────────┐
│  Rollback vs Rollforward Decision Tree                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Issue Detected?                                              │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐   │
│  │           │             │             │             │   │
│  │  YES       │    NO          │    NO         │   │
│  │           │             │             │             │   │
│  ▼           │     ▼         │     ▼         │   ▼ │
│  │           │             │             │             │   │
│  └───────────┴─────────────┴─────────────┴─────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐                      │
│  │  Quick Fix Available?                                   │
│  └─────────────────────────────────────────────────────┘                      │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐                      │
│  │  YES: Rollforward                                      │
│  │  NO: Rollback                                          │
│  └─────────────────────────────────────────────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
```

## Post-Rollback Analysis

### Root Cause Analysis

```python
# Root cause analysis after rollback
def post_rollback_analysis():
    """Analyze why rollback was needed."""
    print("Starting post-rollback analysis...")
    
    # Collect data
    logs = collect_logs()
    metrics = collect_metrics()
    
    # Analyze
    root_cause = analyze_root_cause(logs, metrics)
    
    # Document findings
    document_findings(root_cause)
    
    # Create action items
    create_action_items(root_cause)
    
    print("✓ Post-rollback analysis complete")

post_rollback_analysis()
```

### Incident Report

```markdown
# Incident Report

## Summary
- **Date**: 2024-01-15
- **Time**: 14:30 UTC
- **Duration**: 30 minutes
- **Impact**: 50% of users affected

## Timeline
- 14:00: Deploy v2.0
- 14:15: High error rate detected
- 14:20: Rollback triggered
- 14:25: Rollback completed
- 14:30: System stable

## Root Cause
- Bug in payment processing logic
- Insufficient testing

## Actions Taken
- Rolled back to v1.0
- Fixed bug in v2.1
- Added more tests

## Lessons Learned
- Improve testing
- Add more monitoring
```

## Tools

### Kubernetes Rollback

```bash
# Kubernetes rollback
kubectl rollout undo deployment/web-app

# Check rollback status
kubectl rollout status deployment/web-app

# View rollback history
kubectl rollout history deployment/web-app
```

### AWS Rollback

```bash
# AWS CodeDeploy rollback
aws deploy create-deployment \
  --application-name web-app \
  --deployment-group-name production \
  --deployment-config-name CodeDeployDefault.OneAtATime \
  --deployment-id d-1234567890 \
  --rollback-to-last-deployment
```

### Docker Rollback

```bash
# Docker rollback
docker stop web-app
docker run -d web-app:v1.0
```

### Terraform Rollback

```bash
# Terraform rollback
terraform plan -out=rollback.tfplan
terraform apply rollback.tfplan
```

## Real Examples

### Example 1: Blue-Green Rollback

**Scenario**: Payment gateway integration issue

**Timeline**:
- 10:00: Deploy v2.0 to green
- 10:15: Switch traffic to green
- 10:20: Payment errors detected
- 10:22: Rollback to blue
- 10:23: System stable

**Outcome**: Successful rollback, 3 minutes downtime

### Example 2: Canary Rollback

**Scenario**: API performance degradation

**Timeline**:
- 14:00: Deploy v2.0 to canary
- 14:05: Route 5% traffic
- 14:15: Monitor metrics (latency high)
- 14:17: Rollback canary
- 14:18: System stable

**Outcome**: Successful rollback, 5% of users affected

### Example 3: Rolling Update Rollback

**Scenario**: Database migration issue

**Timeline**:
- 09:00: Deploy v2.0
- 09:15: Database errors detected
- 09:17: Trigger rollback
- 09:20: Rollback complete
- 09:25: System stable

**Outcome**: Successful rollback, 10 minutes downtime

## Summary Checklist

### Preparation

- [ ] Rollback procedure documented
- [ ] Rollback tested in staging
- [ ] Rollback triggers defined
- [ ] Rollback automation configured
- [ ] Rollback monitoring set up

### During Rollback

- [ ] Detect issue
- [ ] Trigger rollback
- [ ] Monitor rollback
- [ ] Verify system health
- [ ] Communicate to team

### Post-Rollback

- [ ] Root cause analysis
- [ ] Incident report created
- [ ] Lessons learned documented
- [ ] Action items created
- [ ] Process improved

### Prevention

- [ ] Improve testing
- [ ] Add more monitoring
- [ ] Better code review
- [ ] More gradual rollouts
- [ ] Feature flags for risky changes
```

---

## Quick Start

### Kubernetes Rollback

```bash
# Rollback deployment
kubectl rollout undo deployment/myapp

# Rollback to specific revision
kubectl rollout undo deployment/myapp --to-revision=3

# Check rollout history
kubectl rollout history deployment/myapp
```

### Database Migration Rollback

```typescript
// Prisma migration rollback
npx prisma migrate resolve --rolled-back 20240115123456_add_column

// Or create down migration
npx prisma migrate dev --create-only --name rollback_add_column
```

---

## Production Checklist

- [ ] **Rollback Plan**: Document rollback procedures
- [ ] **Automated Rollback**: Set up automated rollback triggers
- [ ] **Database Rollback**: Plan database migration rollbacks
- [ ] **Monitoring**: Monitor for rollback triggers
- [ ] **Testing**: Test rollback procedures
- [ ] **Communication**: Notify team of rollbacks
- [ ] **Documentation**: Document rollback steps
- [ ] **Version Control**: Keep previous versions available
- [ ] **Backup**: Backup before deployment
- [ ] **Recovery**: Test recovery procedures
- [ ] **Post-mortem**: Analyze rollback causes
- [ ] **Prevention**: Improve to prevent future rollbacks

---

## Anti-patterns

### ❌ Don't: No Rollback Plan

```yaml
# ❌ Bad - Deploy without rollback plan
apiVersion: apps/v1
kind: Deployment
# No rollback strategy!
```

```yaml
# ✅ Good - With rollback strategy
apiVersion: apps/v1
kind: Deployment
spec:
  revisionHistoryLimit: 10  # Keep revisions for rollback
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
```

### ❌ Don't: Destructive Migrations

```sql
-- ❌ Bad - Destructive migration
ALTER TABLE users DROP COLUMN email  -- Can't rollback!
```

```sql
-- ✅ Good - Reversible migration
-- Up migration
ALTER TABLE users ADD COLUMN email_new VARCHAR(255);
UPDATE users SET email_new = email;
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN email_new TO email;

-- Down migration (rollback)
ALTER TABLE users ADD COLUMN email_old VARCHAR(255);
UPDATE users SET email_old = email;
ALTER TABLE users DROP COLUMN email;
ALTER TABLE users RENAME COLUMN email_old TO email;
```

---

## Integration Points

- **Canary Deployment** (`26-deployment-strategies/canary-deployment/`) - Gradual rollout
- **Blue-Green Deployment** (`26-deployment-strategies/blue-green-deployment/`) - Zero-downtime
- **Monitoring** (`14-monitoring-observability/`) - Rollback triggers

---

## Further Reading

- [Kubernetes Rollback](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment)
- [Database Migration Rollback](https://www.prisma.io/docs/concepts/components/prisma-migrate)
