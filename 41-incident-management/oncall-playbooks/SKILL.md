---
name: On-Call Playbooks
description: Comprehensive runbooks and playbooks for on-call incident response
---

# On-Call Playbooks and Runbooks

## Overview

Playbooks and runbooks are essential tools for on-call engineers, providing step-by-step guidance for responding to common incidents. Well-written runbooks reduce Mean Time To Recovery (MTTR), enable consistent responses, and help less experienced engineers handle complex situations.

**Core Principle**: "Document once, execute many times. Make incident response repeatable and reliable."

## 1. Purpose of Playbooks and Runbooks

### Why They Matter

```
Benefits:
✓ Faster incident response (no need to figure out from scratch)
✓ Consistent response (same steps every time)
✓ Knowledge sharing (junior engineers can handle incidents)
✓ Reduced stress (clear guidance during high-pressure situations)
✓ Continuous improvement (update based on learnings)
✓ Onboarding tool (new engineers learn system architecture)

Without Runbooks:
❌ Every incident is a new adventure
❌ Tribal knowledge (only seniors know what to do)
❌ Inconsistent responses
❌ Longer MTTR
❌ Higher stress
```

### When to Use

```
Use runbooks for:
✓ Common incidents (happens monthly or more)
✓ Complex procedures (multiple steps)
✓ High-risk operations (database failover)
✓ Time-sensitive incidents (every minute counts)
✓ Knowledge preservation (expert leaving team)

Don't need runbooks for:
✗ One-time incidents (not repeatable)
✗ Trivial issues (restart service)
✗ Well-documented in product docs
```

## 2. Playbook vs Runbook Distinction

### Playbook

```
Definition: High-level strategy and decision-making guide

Characteristics:
- Strategic approach
- Decision trees
- When to escalate
- Communication templates
- Multiple possible paths

Example: "Incident Response Playbook"
- How to assess severity
- When to create war room
- Communication cadence
- Escalation criteria
```

### Runbook

```
Definition: Step-by-step tactical procedures

Characteristics:
- Specific commands
- Exact steps to follow
- Copy-pasteable code
- Expected outcomes
- Troubleshooting steps

Example: "Database Failover Runbook"
1. Check primary database health
2. Verify replica is in sync
3. Promote replica to primary
4. Update application config
5. Verify traffic routing
```

### Relationship

```
Playbook (Strategy)
  ├─ Runbook 1 (Tactics)
  ├─ Runbook 2 (Tactics)
  └─ Runbook 3 (Tactics)

Example:
"High Error Rate Playbook"
  ├─ Check Recent Deployments Runbook
  ├─ Database Performance Runbook
  └─ Rollback Deployment Runbook
```

## 3. Essential Playbooks

### Playbook 1: Service is Down

```markdown
# Playbook: Service is Down

## Symptoms
- Health check failing
- 100% error rate
- No traffic reaching service
- Users reporting "site is down"

## Initial Triage (2 minutes)
1. Verify service is actually down
   ```bash
   curl -i https://api.example.com/health
   ```

2. Check if pods/instances are running
   ```bash
   kubectl get pods -l app=api-service
   ```

3. Check recent changes
   ```bash
   kubectl rollout history deployment/api-service
   ```

## Decision Tree

```
Is service responding to health checks?
├─ NO → Are pods running?
│   ├─ NO → Pods crashed
│   │   └─ Go to: Pod Crash Runbook
│   └─ YES → Network/routing issue
│       └─ Go to: Network Troubleshooting Runbook
└─ YES → Partial outage
    └─ Go to: High Error Rate Playbook
```

## Common Causes
1. Recent deployment broke service
2. Database connection failed
3. Out of memory/CPU
4. Configuration error
5. Network partition

## Runbooks to Execute
- [Pod Crash Loop Runbook](#runbook-pod-crashloop)
- [Database Connection Runbook](#runbook-database-connection)
- [Rollback Deployment Runbook](#runbook-rollback)

## Communication
- Severity: SEV0 or SEV1
- Status page: "Major outage"
- Update frequency: Every 15 minutes
```

### Playbook 2: Database is Slow

```markdown
# Playbook: Database is Slow

## Symptoms
- Query latency > 2x baseline
- Connection pool exhaustion
- Timeouts on database operations
- Application slow/timing out

## Initial Triage (3 minutes)
1. Check database metrics
   ```sql
   SELECT * FROM pg_stat_activity WHERE state = 'active';
   ```

2. Identify slow queries
   ```sql
   SELECT pid, now() - query_start AS duration, query
   FROM pg_stat_activity
   WHERE state = 'active'
   ORDER BY duration DESC
   LIMIT 10;
   ```

3. Check resource usage
   ```bash
   # CPU, memory, disk I/O
   kubectl top pods -l app=postgres
   ```

## Decision Tree

```
Are there long-running queries?
├─ YES → Are they legitimate?
│   ├─ YES → Optimize or kill
│   └─ NO → Kill immediately
└─ NO → Check resource usage
    ├─ High CPU → Scale up or optimize
    ├─ High I/O → Check disk, add read replicas
    └─ Normal → Check connection pool
```

## Runbooks to Execute
- [Kill Long-Running Queries](#runbook-kill-queries)
- [Database Failover](#runbook-db-failover)
- [Add Read Replica](#runbook-add-replica)
```

### Playbook 3: High Error Rate

```markdown
# Playbook: High Error Rate

## Symptoms
- Error rate > 5% (baseline: <0.1%)
- Alerts firing for 5xx errors
- Users reporting errors

## Initial Triage (3 minutes)
1. Check error rate trend
   - Is it increasing, stable, or decreasing?

2. Identify affected endpoints
   ```bash
   kubectl logs -l app=api --since=5m | grep "HTTP/1.1 5" | awk '{print $7}' | sort | uniq -c | sort -rn
   ```

3. Check recent deployments
   ```bash
   git log --since="1 hour ago" --oneline
   ```

## Decision Tree

```
Error rate > 50%?
├─ YES → Recent deployment?
│   ├─ YES → ROLLBACK immediately
│   └─ NO → Check dependencies
└─ NO → Specific endpoint?
    ├─ YES → Disable endpoint, investigate
    └─ NO → Monitor, investigate root cause
```

## Quick Actions
- Rollback if recent deployment
- Disable failing endpoint
- Scale up if resource constrained
- Failover if database issue
```

### Playbook 4: Disk Full

```markdown
# Playbook: Disk Full

## Symptoms
- Disk usage > 95%
- Write operations failing
- Application crashes
- "No space left on device" errors

## Initial Triage (2 minutes)
1. Check disk usage
   ```bash
   df -h
   du -sh /* | sort -rh | head -10
   ```

2. Identify large files/directories
   ```bash
   find / -type f -size +1G -exec ls -lh {} \;
   ```

## Immediate Actions
1. Clear logs
   ```bash
   find /var/log -name "*.log" -mtime +7 -delete
   journalctl --vacuum-time=7d
   ```

2. Clear temp files
   ```bash
   rm -rf /tmp/*
   ```

3. Clear old Docker images
   ```bash
   docker system prune -af --volumes
   ```

## Long-term Fix
- Implement log rotation
- Set up disk monitoring
- Increase disk size
- Archive old data
```

### Playbook 5: Memory Leak

```markdown
# Playbook: Memory Leak

## Symptoms
- Memory usage gradually increasing
- OOM (Out of Memory) kills
- Slow performance
- Frequent restarts

## Initial Triage (5 minutes)
1. Check memory trend
   ```bash
   kubectl top pods -l app=api --sort-by=memory
   ```

2. Check for OOM kills
   ```bash
   kubectl get pods -l app=api | grep OOMKilled
   kubectl describe pod <pod-name>
   ```

3. Review recent code changes
   ```bash
   git log --since="1 week ago" --grep="cache\|memory"
   ```

## Immediate Actions
1. Restart affected pods
   ```bash
   kubectl rollout restart deployment/api
   ```

2. Increase memory limits (temporary)
   ```bash
   kubectl set resources deployment/api --limits=memory=4Gi
   ```

## Investigation
- Profile memory usage
- Review cache implementation
- Check for connection leaks
- Analyze heap dumps
```

### Playbook 6: Certificate Expiration

```markdown
# Playbook: Certificate Expiration

## Symptoms
- SSL/TLS errors
- "Certificate expired" warnings
- HTTPS connections failing

## Prevention (Before Expiration)
1. Check certificate expiration
   ```bash
   echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -dates
   ```

2. Set up monitoring
   ```bash
   # Alert if cert expires in < 30 days
   ```

## Immediate Actions (After Expiration)
1. Renew certificate
   ```bash
   certbot renew --force-renewal
   ```

2. Update Kubernetes secret
   ```bash
   kubectl create secret tls example-tls --cert=cert.pem --key=key.pem --dry-run=client -o yaml | kubectl apply -f -
   ```

3. Restart ingress controller
   ```bash
   kubectl rollout restart deployment/nginx-ingress-controller
   ```

## Long-term Fix
- Automate certificate renewal (cert-manager)
- Set up expiration alerts (30, 14, 7 days)
```

### Playbook 7: DDoS Attack

```markdown
# Playbook: DDoS Attack

## Symptoms
- Sudden traffic spike (10x-100x normal)
- Legitimate users can't access service
- High bandwidth usage
- Resource exhaustion

## Initial Triage (3 minutes)
1. Confirm DDoS vs legitimate traffic
   ```bash
   # Check traffic sources
   tail -f /var/log/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -rn
   ```

2. Identify attack pattern
   - Single IP or distributed?
   - Specific endpoint targeted?
   - Request pattern (same User-Agent, etc.)

## Immediate Actions
1. Enable rate limiting
   ```nginx
   limit_req_zone $binary_remote_addr zone=ddos:10m rate=10r/s;
   limit_req zone=ddos burst=20 nodelay;
   ```

2. Block attacking IPs
   ```bash
   iptables -A INPUT -s <attacker-ip> -j DROP
   ```

3. Enable CloudFlare "Under Attack" mode
   ```bash
   # Or equivalent CDN protection
   ```

4. Scale up infrastructure (if needed)
   ```bash
   kubectl scale deployment/api --replicas=50
   ```

## Escalation
- Contact CDN provider (CloudFlare, Akamai)
- Contact ISP for upstream filtering
- Consider AWS Shield / GCP Cloud Armor
```

### Playbook 8: Data Loss Incident

```markdown
# Playbook: Data Loss Incident

## Symptoms
- Data missing from database
- User reports data disappeared
- Accidental DELETE/DROP executed

## STOP THE BLEEDING (Immediate)
1. **DO NOT** make any more changes
2. Stop all write operations
   ```bash
   # Put database in read-only mode
   ALTER DATABASE mydb SET default_transaction_read_only = on;
   ```

3. Identify scope of data loss
   ```sql
   SELECT COUNT(*) FROM users WHERE deleted_at > NOW() - INTERVAL '1 hour';
   ```

## Assessment (5 minutes)
1. What data was lost?
2. When did it happen?
3. How much data?
4. Is backup available?

## Recovery Options

### Option 1: Point-in-Time Recovery
```bash
# Restore from backup to specific time
pg_restore --dbname=mydb_recovery backup.dump
```

### Option 2: Replay from WAL
```bash
# PostgreSQL WAL replay
recovery_target_time = '2024-01-15 10:00:00'
```

### Option 3: Restore from Replica
```bash
# If replica has data, promote it
```

## Communication
- Severity: SEV0 (data loss)
- Notify: All stakeholders immediately
- Transparency: Explain what happened, what we're doing
```

## 4. Runbook Structure

### Complete Runbook Template

```markdown
# Runbook: [Title]

## Metadata
- **ID**: RB-001
- **Owner**: @team-platform
- **Last Updated**: 2024-01-15
- **Tested**: 2024-01-10
- **Severity**: SEV1
- **Estimated Time**: 15 minutes

## Symptoms
Clear description of what the on-call engineer will observe:
- Specific error messages
- Metric thresholds
- User-reported issues
- Alert names

## Triage Steps
Quick diagnostic steps to confirm this is the right runbook:

1. **Check [specific metric]**
   ```bash
   # Command to run
   ```
   Expected: [what you should see]
   Actual: [what you're seeing if this runbook applies]

2. **Verify [condition]**
   ```bash
   # Command to run
   ```

## Common Causes
Ranked by likelihood:
1. Recent deployment (70%)
2. Database issue (20%)
3. External dependency (10%)

## Resolution Steps

### Step 1: [Action]
**Time estimate**: 2 minutes

**Commands**:
```bash
# Exact commands to run
kubectl get pods -l app=api-service
```

**Expected outcome**:
```
NAME                          READY   STATUS    RESTARTS   AGE
api-service-7d9f8b6c4-abc12   1/1     Running   0          5m
```

**If this fails**:
- Try: [alternative approach]
- Or: Escalate to [team/person]

### Step 2: [Action]
**Time estimate**: 3 minutes

[Continue with detailed steps...]

## Rollback Procedures
If resolution fails, how to undo changes:

```bash
# Rollback commands
kubectl rollout undo deployment/api-service
```

## Escalation Path
When to escalate and to whom:
- If not resolved in 15 minutes → Escalate to @senior-engineer
- If database-related → Escalate to @database-team
- If affects payments → Escalate to @payments-team

## Related Runbooks
- [Database Failover Runbook](#)
- [Rollback Deployment Runbook](#)

## Verification
How to confirm the issue is resolved:

1. Check error rate
   ```bash
   # Command to verify
   ```
   Expected: < 0.1%

2. Check user reports
   - Support tickets should stop coming in

3. Monitor for 10 minutes
   - Ensure issue doesn't recur

## Post-Incident
- [ ] Update incident timeline
- [ ] Document any deviations from runbook
- [ ] Create postmortem ticket (if SEV0/1)
- [ ] Update runbook if needed

## Notes
Additional context, gotchas, or tips:
- Note: This issue often recurs after 24 hours
- Tip: Check CloudFlare cache if API seems fine but users report issues
- Warning: Don't run this command in production without backup
```

## 5. Runbook Best Practices

### 1. Step-by-Step Instructions

```markdown
❌ Bad:
"Fix the database connection issue"

✓ Good:
"1. Check database connectivity:
   ```bash
   psql -h db.example.com -U app -c 'SELECT 1'
   ```
   Expected output: `1`
   
2. If connection fails, check credentials:
   ```bash
   kubectl get secret db-credentials -o jsonpath='{.data.password}' | base64 -d
   ```
   
3. Verify database is running:
   ```bash
   kubectl get pods -l app=postgres
   ```"
```

### 2. Command Examples (Copy-Pasteable)

```markdown
✓ Include full commands with all flags:
```bash
kubectl logs deployment/api-service \
  --tail=100 \
  --since=15m \
  --all-containers=true
```

✓ Include expected output:
```
Expected:
2024-01-15 10:00:00 INFO Server started on port 8080
```

✓ Include error output:
```
If you see:
Error: connection refused
Then: Database is down, proceed to Step 5
```
```

### 3. Decision Points

```markdown
## Step 3: Check Error Rate

```bash
curl "https://grafana.example.com/api/metrics/error-rate"
```

**Decision**:
- If error rate > 50% → Go to Step 4 (Rollback)
- If error rate 10-50% → Go to Step 5 (Investigate)
- If error rate < 10% → Go to Step 6 (Monitor)
```

### 4. Expected Outcomes

```markdown
## Step 2: Restart Service

```bash
kubectl rollout restart deployment/api-service
```

**Expected outcome** (within 2 minutes):
- All pods show `Running` status
- Error rate drops below 1%
- Latency returns to < 200ms

**If outcome not achieved**:
- Wait additional 3 minutes
- If still failing, proceed to Step 3 (Rollback)
- If pods crash, check logs: `kubectl logs <pod-name> --previous`
```

### 5. Time Estimates

```markdown
## Resolution Steps

### Step 1: Identify Issue (2 minutes)
[Commands...]

### Step 2: Apply Fix (5 minutes)
[Commands...]

### Step 3: Verify (3 minutes)
[Commands...]

**Total estimated time**: 10 minutes
**If exceeds 15 minutes**: Escalate to senior engineer
```

## 6. Runbook Organization and Discoverability

### Directory Structure

```
runbooks/
├── README.md (index of all runbooks)
├── infrastructure/
│   ├── kubernetes-pod-crashloop.md
│   ├── disk-full.md
│   └── network-partition.md
├── database/
│   ├── postgres-connection-pool.md
│   ├── postgres-slow-queries.md
│   └── postgres-failover.md
├── application/
│   ├── api-high-error-rate.md
│   ├── memory-leak.md
│   └── deployment-rollback.md
└── security/
    ├── ddos-attack.md
    ├── certificate-expiration.md
    └── security-breach.md
```

### Runbook Index

```markdown
# Runbook Index

## By Symptom
- **Service is down** → [Pod Crashloop](infrastructure/kubernetes-pod-crashloop.md)
- **High error rate** → [API Errors](application/api-high-error-rate.md)
- **Slow database** → [Slow Queries](database/postgres-slow-queries.md)
- **Disk full** → [Disk Full](infrastructure/disk-full.md)

## By Alert Name
- `HighErrorRate` → [API Errors](application/api-high-error-rate.md)
- `PodCrashLooping` → [Pod Crashloop](infrastructure/kubernetes-pod-crashloop.md)
- `DatabaseSlow` → [Slow Queries](database/postgres-slow-queries.md)

## By Severity
- **SEV0**: [Data Loss](database/data-loss.md), [Security Breach](security/security-breach.md)
- **SEV1**: [Service Down](infrastructure/service-down.md), [Database Failover](database/postgres-failover.md)
- **SEV2**: [High Latency](application/high-latency.md), [Disk Full](infrastructure/disk-full.md)

## Recently Updated
- 2024-01-15: [Pod Crashloop](infrastructure/kubernetes-pod-crashloop.md)
- 2024-01-14: [API Errors](application/api-high-error-rate.md)
```

### Search Tags

```markdown
# Runbook: PostgreSQL Connection Pool Exhausted

**Tags**: #database #postgresql #connection-pool #sev1
**Alerts**: `DatabaseConnectionPoolExhausted`, `HighDatabaseLatency`
**Symptoms**: timeout, connection refused, pool exhausted
```

## 7. Runbook Versioning

### Version Control

```markdown
# Runbook: Database Failover

**Version**: 2.1.0
**Last Updated**: 2024-01-15
**Author**: @alice
**Changelog**:
- 2.1.0 (2024-01-15): Added automated failover steps
- 2.0.0 (2024-01-01): Complete rewrite for Kubernetes
- 1.5.0 (2023-12-01): Added rollback procedure
- 1.0.0 (2023-10-01): Initial version

**Breaking Changes in 2.0.0**:
- Commands changed from Docker to Kubernetes
- Failover now automated (manual override available)
```

### Git-Based Versioning

```bash
# Track runbooks in Git
runbooks/
├── .git/
├── database/
│   └── failover.md
└── CHANGELOG.md

# View runbook history
git log --follow runbooks/database/failover.md

# Compare versions
git diff v1.0.0 v2.0.0 runbooks/database/failover.md
```

## 8. Runbook Testing (DR Drills)

### Test Schedule

```
Monthly: Test critical runbooks (SEV0/1)
Quarterly: Test all runbooks
Annually: Full disaster recovery drill

Example Schedule:
- Week 1: Database failover
- Week 2: Service rollback
- Week 3: DDoS response
- Week 4: Data recovery
```

### Test Procedure

```markdown
# Runbook Test: Database Failover

**Date**: 2024-01-15
**Tester**: @bob
**Environment**: Staging

## Test Steps
1. ✅ Follow runbook exactly as written
2. ✅ Time each step
3. ✅ Note any deviations
4. ✅ Verify expected outcomes

## Results
- **Total Time**: 12 minutes (target: 15 minutes) ✅
- **Success**: Yes ✅
- **Deviations**: Step 3 command had typo (fixed)

## Issues Found
1. Step 3 command missing `--namespace` flag
2. Expected output in Step 5 was outdated
3. Escalation path unclear

## Actions
- [ ] Fix command in Step 3
- [ ] Update expected output in Step 5
- [ ] Clarify escalation path
- [ ] Retest next month
```

## 9. Auto-Remediation vs Manual Runbooks

### When to Automate

```
Automate if:
✓ Happens frequently (weekly or more)
✓ Clear root cause and fix
✓ Low risk of making things worse
✓ Can be fully automated
✓ Saves significant time

Examples:
- Restart crashed pod
- Clear disk space (delete old logs)
- Scale up on high CPU
- Renew expiring certificates
```

### When to Keep Manual

```
Keep manual if:
✓ Requires judgment/decision-making
✓ High risk (data loss, security)
✓ Rare occurrence
✓ Complex troubleshooting needed
✓ Regulatory/compliance requires human approval

Examples:
- Database failover
- Data recovery
- Security incident response
- Major architecture changes
```

### Hybrid Approach

```typescript
// Auto-remediation with human oversight
async function autoRemediate(alert: Alert) {
  // Attempt automatic fix
  const result = await attemptAutoFix(alert);

  if (result.success) {
    // Fixed automatically
    await notifySlack(`✅ Auto-remediated: ${alert.name}`);
    await createTicket(alert, 'auto-resolved');
  } else {
    // Failed, escalate to human
    await pageOnCall(alert);
    await notifySlack(`⚠️ Auto-remediation failed: ${alert.name}. Paging on-call.`);
  }
}
```

## 10. Runbook Tools

### PagerDuty Runbooks

```yaml
# PagerDuty runbook integration
service:
  name: api-service
  escalation_policy: engineering
  incident_urgency_rule:
    type: constant
    urgency: high
  auto_resolve_timeout: 14400
  acknowledgement_timeout: 600
  runbook_url: https://wiki.example.com/runbooks/api-service
```

### Confluence / Notion

```
Advantages:
✓ Rich formatting
✓ Easy collaboration
✓ Version history
✓ Search functionality
✓ Comments and discussions

Disadvantages:
✗ Not in version control
✗ Requires login
✗ Can become outdated
```

### GitHub Wikis

```
Advantages:
✓ Version controlled
✓ Markdown format
✓ Easy to update (PR workflow)
✓ Free and accessible

Disadvantages:
✗ Less rich formatting
✗ Requires Git knowledge
```

### Internal Tools

```typescript
// Custom runbook platform
interface Runbook {
  id: string;
  title: string;
  severity: string;
  steps: RunbookStep[];
  lastTested: Date;
  owner: string;
}

interface RunbookStep {
  number: number;
  title: string;
  description: string;
  commands: string[];
  expectedOutcome: string;
  timeEstimate: number; // minutes
}

// Runbook execution tracking
async function executeRunbook(runbookId: string, incidentId: string) {
  const runbook = await getRunbook(runbookId);
  const execution = await createExecution(runbookId, incidentId);

  for (const step of runbook.steps) {
    const startTime = Date.now();
    
    // Show step to engineer
    await displayStep(step);
    
    // Wait for confirmation
    await waitForConfirmation();
    
    // Record execution time
    const duration = Date.now() - startTime;
    await recordStepExecution(execution.id, step.number, duration);
  }

  await completeExecution(execution.id);
}
```

## 11. Runbook Maintenance (Keep Updated)

### Maintenance Schedule

```
After each incident:
- Update runbook if steps changed
- Add new troubleshooting tips
- Document what worked/didn't work

Monthly:
- Review runbook usage stats
- Update outdated screenshots
- Test critical runbooks

Quarterly:
- Full runbook audit
- Archive unused runbooks
- Create runbooks for new common issues
```

### Runbook Health Metrics

```typescript
interface RunbookMetrics {
  id: string;
  title: string;
  lastUsed: Date;
  usageCount: number;
  lastTested: Date;
  lastUpdated: Date;
  averageExecutionTime: number;
  successRate: number;
  feedbackScore: number; // 1-5
}

// Identify stale runbooks
function findStaleRunbooks(runbooks: RunbookMetrics[]): RunbookMetrics[] {
  const sixMonthsAgo = new Date();
  sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 6);

  return runbooks.filter(rb =>
    rb.lastUpdated < sixMonthsAgo ||
    rb.lastTested < sixMonthsAgo
  );
}
```

## 12. Integration with Monitoring (Links from Alerts)

### Alert to Runbook Linking

```yaml
# Prometheus alert with runbook link
groups:
  - name: api-service
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        annotations:
          summary: "High error rate on {{ $labels.service }}"
          description: "Error rate is {{ $value | humanizePercentage }}"
          runbook_url: "https://runbooks.example.com/api-high-error-rate"
```

### PagerDuty Integration

```json
{
  "incident": {
    "title": "High Error Rate on API Service",
    "service": {
      "id": "PSERVICE1"
    },
    "body": {
      "type": "incident_body",
      "details": "Error rate: 15%"
    },
    "incident_key": "api-high-error-rate",
    "custom_details": {
      "runbook": "https://runbooks.example.com/api-high-error-rate",
      "dashboard": "https://grafana.example.com/d/api-service"
    }
  }
}
```

## 13. Example Runbooks

### Runbook 1: Kubernetes Pod CrashLoop

```markdown
# Runbook: Kubernetes Pod CrashLoopBackOff

## Metadata
- **ID**: RB-K8S-001
- **Severity**: SEV1
- **Estimated Time**: 10 minutes
- **Owner**: @platform-team

## Symptoms
- Alert: `PodCrashLooping`
- Pod status: `CrashLoopBackOff`
- Application unavailable or degraded

## Triage (2 minutes)

### Step 1: Identify crashing pods
```bash
kubectl get pods -l app=api-service | grep CrashLoopBackOff
```

### Step 2: Check pod logs
```bash
# Current logs
kubectl logs <pod-name>

# Previous container logs (if restarted)
kubectl logs <pod-name> --previous
```

### Step 3: Check pod events
```bash
kubectl describe pod <pod-name>
```

## Common Causes

### 1. Application Error (60%)
**Symptoms in logs**:
```
Error: Cannot connect to database
Fatal: Configuration file not found
```

**Resolution**: Fix application code or configuration

### 2. Resource Limits (20%)
**Symptoms in events**:
```
OOMKilled
Liveness probe failed
```

**Resolution**: Increase resource limits

### 3. Missing Dependencies (15%)
**Symptoms in logs**:
```
Error: Secret "db-credentials" not found
Error: ConfigMap "app-config" not found
```

**Resolution**: Create missing resources

### 4. Image Pull Error (5%)
**Symptoms in events**:
```
Failed to pull image "api-service:v2.0.0"
ImagePullBackOff
```

**Resolution**: Fix image name or registry credentials

## Resolution Steps

### For Application Errors

**Step 1**: Identify error from logs
```bash
kubectl logs <pod-name> --previous | tail -50
```

**Step 2**: Rollback to previous version
```bash
kubectl rollout undo deployment/api-service
```

**Step 3**: Verify rollback
```bash
kubectl rollout status deployment/api-service
```

Expected: `deployment "api-service" successfully rolled out`

### For Resource Limits

**Step 1**: Check current limits
```bash
kubectl get deployment api-service -o jsonpath='{.spec.template.spec.containers[0].resources}'
```

**Step 2**: Increase limits
```bash
kubectl set resources deployment/api-service \
  --limits=cpu=2,memory=4Gi \
  --requests=cpu=1,memory=2Gi
```

**Step 3**: Verify pods running
```bash
kubectl get pods -l app=api-service
```

### For Missing Dependencies

**Step 1**: Identify missing resource
```bash
kubectl describe pod <pod-name> | grep -A 5 "Error"
```

**Step 2**: Create missing secret/configmap
```bash
# Example: Create database credentials
kubectl create secret generic db-credentials \
  --from-literal=username=app \
  --from-literal=password=secret123
```

**Step 3**: Restart deployment
```bash
kubectl rollout restart deployment/api-service
```

## Verification (2 minutes)

1. Check pod status
   ```bash
   kubectl get pods -l app=api-service
   ```
   Expected: All pods `Running` with `READY 1/1`

2. Check application logs
   ```bash
   kubectl logs -l app=api-service --tail=20
   ```
   Expected: No error messages

3. Test endpoint
   ```bash
   curl -i https://api.example.com/health
   ```
   Expected: `200 OK`

## Escalation
- If not resolved in 10 minutes → Escalate to @platform-team
- If application-specific → Escalate to @app-team
- If database-related → Escalate to @database-team
```

### Runbook 2: PostgreSQL Connection Pool Exhausted

```markdown
# Runbook: PostgreSQL Connection Pool Exhausted

## Metadata
- **ID**: RB-DB-001
- **Severity**: SEV1
- **Estimated Time**: 15 minutes
- **Owner**: @database-team

## Symptoms
- Alert: `DatabaseConnectionPoolExhausted`
- Error logs: "Connection pool exhausted"
- Application timeouts
- High error rate

## Triage (3 minutes)

### Step 1: Check connection pool usage
```sql
SELECT count(*) FROM pg_stat_activity;
```

Compare to max connections:
```sql
SHOW max_connections;
```

### Step 2: Identify connection sources
```sql
SELECT application_name, count(*) 
FROM pg_stat_activity 
GROUP BY application_name 
ORDER BY count DESC;
```

### Step 3: Check for long-running queries
```sql
SELECT pid, now() - query_start AS duration, query, state
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC
LIMIT 10;
```

## Common Causes

### 1. Connection Leak (50%)
Application not closing connections properly

### 2. Traffic Spike (30%)
Sudden increase in requests

### 3. Slow Queries (15%)
Queries holding connections for too long

### 4. Misconfigured Pool (5%)
Pool size too small for workload

## Resolution Steps

### Immediate Mitigation (5 minutes)

**Step 1**: Kill idle connections
```sql
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle'
AND now() - state_change > interval '5 minutes';
```

**Step 2**: Restart application (releases connections)
```bash
kubectl rollout restart deployment/api-service
```

**Step 3**: Monitor connection count
```sql
SELECT count(*) FROM pg_stat_activity;
```

Expected: Connections drop below 80% of max

### Long-term Fix

**Step 1**: Increase connection pool size (if needed)
```yaml
# application config
database:
  pool:
    min: 5
    max: 50  # Increased from 20
```

**Step 2**: Fix connection leak (if found)
```typescript
// Bad: Connection leak
async function badQuery() {
  const conn = await pool.getConnection();
  const result = await conn.query('SELECT * FROM users');
  return result; // Connection not released!
}

// Good: Always release
async function goodQuery() {
  const conn = await pool.getConnection();
  try {
    const result = await conn.query('SELECT * FROM users');
    return result;
  } finally {
    conn.release(); // Always released
  }
}
```

**Step 3**: Add connection pool monitoring
```typescript
// Monitor pool usage
setInterval(() => {
  const poolStats = pool.getStats();
  metrics.gauge('db.pool.active', poolStats.active);
  metrics.gauge('db.pool.idle', poolStats.idle);
  metrics.gauge('db.pool.waiting', poolStats.waiting);
}, 10000);
```

## Verification (2 minutes)

1. Check connection count
   ```sql
   SELECT count(*) FROM pg_stat_activity;
   ```
   Expected: < 80% of max_connections

2. Check error rate
   ```bash
   # Should drop to < 1%
   ```

3. Monitor for 10 minutes
   - Ensure connections don't grow again

## Escalation
- If connections don't drop → Escalate to @database-team
- If application-specific leak → Escalate to @app-team
- If traffic spike → Escalate to @infrastructure-team (scale up)
```

### Runbook 3: Redis Memory Maxed

```markdown
# Runbook: Redis Memory Maxed Out

## Metadata
- **ID**: RB-CACHE-001
- **Severity**: SEV2
- **Estimated Time**: 10 minutes

## Symptoms
- Alert: `RedisMemoryHigh`
- Redis evicting keys
- Cache misses increasing
- Application slow (cache not working)

## Triage (2 minutes)

### Step 1: Check memory usage
```bash
redis-cli INFO memory | grep used_memory_human
```

### Step 2: Check eviction stats
```bash
redis-cli INFO stats | grep evicted_keys
```

### Step 3: Check key count
```bash
redis-cli DBSIZE
```

## Resolution Steps

### Immediate Mitigation (5 minutes)

**Step 1**: Clear expired keys
```bash
redis-cli --scan --pattern "*" | xargs redis-cli DEL
```

**Step 2**: Flush least important data
```bash
# If using multiple databases
redis-cli -n 2 FLUSHDB  # Flush non-critical cache
```

**Step 3**: Increase memory limit (temporary)
```bash
kubectl set resources deployment/redis --limits=memory=4Gi
```

### Long-term Fix

**Step 1**: Implement eviction policy
```bash
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

**Step 2**: Set TTL on keys
```typescript
// Always set expiration
await redis.set('user:123', userData, 'EX', 3600); // 1 hour TTL
```

**Step 3**: Add memory monitoring
```typescript
setInterval(async () => {
  const info = await redis.info('memory');
  const memoryUsage = parseFloat(info.match(/used_memory:(\d+)/)[1]);
  metrics.gauge('redis.memory.used', memoryUsage);
}, 30000);
```

## Verification

1. Check memory usage
   ```bash
   redis-cli INFO memory | grep used_memory_human
   ```
   Expected: < 80% of maxmemory

2. Check cache hit rate
   ```bash
   redis-cli INFO stats | grep keyspace_hits
   ```
   Expected: Hit rate > 80%
```

### Runbook 4: API 5xx Spike

```markdown
# Runbook: API 5xx Error Spike

## Metadata
- **ID**: RB-API-001
- **Severity**: SEV1
- **Estimated Time**: 15 minutes

## Symptoms
- Alert: `HighErrorRate`
- Error rate > 5%
- Users reporting errors
- 500/503 responses

## Triage (3 minutes)

### Step 1: Check error rate
```bash
# Prometheus query
rate(http_requests_total{status=~"5.."}[5m])
```

### Step 2: Identify affected endpoints
```bash
kubectl logs -l app=api --since=5m | \
  grep "HTTP/1.1 5" | \
  awk '{print $7}' | \
  sort | uniq -c | sort -rn
```

### Step 3: Check recent deployments
```bash
kubectl rollout history deployment/api-service
```

## Decision Tree

```
Error rate > 50%?
├─ YES → Recent deployment (< 1 hour)?
│   ├─ YES → ROLLBACK immediately
│   └─ NO → Check dependencies
│       ├─ Database down? → Escalate to DB team
│       └─ External API down? → Enable fallback
└─ NO (5-50% errors) → Investigate specific endpoint
    ├─ Single endpoint failing? → Disable endpoint
    └─ All endpoints affected? → Check resources
```

## Resolution Steps

### If Recent Deployment (Most Common)

**Step 1**: Rollback deployment
```bash
kubectl rollout undo deployment/api-service
```

**Step 2**: Monitor error rate
```bash
# Should drop within 2 minutes
```

**Step 3**: Verify rollback
```bash
kubectl rollout status deployment/api-service
```

### If Database Issue

**Step 1**: Check database connectivity
```bash
kubectl run -it --rm debug --image=postgres:14 --restart=Never -- \
  psql -h db.example.com -U app -c "SELECT 1"
```

**Step 2**: If database down, escalate
```bash
# Page database team
# Check: database/postgres-failover.md runbook
```

### If External API Issue

**Step 1**: Check vendor status
```bash
curl https://status.stripe.com/api/v2/status.json
```

**Step 2**: Enable fallback
```typescript
// Feature flag to disable external API
await launchdarkly.variation('use-backup-payment-processor', user, false);
```

## Verification

1. Error rate < 1%
2. Latency back to normal
3. No user complaints
4. Monitor for 10 minutes
```

## 14. Runbook Templates

### Quick Runbook Template

```markdown
# Runbook: [Title]

## Symptoms
- [What you'll see]

## Quick Fix
```bash
# Commands to run
```

## If That Doesn't Work
1. [Step 1]
2. [Step 2]
3. Escalate to [team]

## Verification
- [How to confirm it's fixed]
```

### Detailed Runbook Template

See [Section 4: Runbook Structure](#4-runbook-structure)

## 15. Common Runbook Antipatterns

### Antipattern 1: Too Vague

```
❌ Bad:
"Fix the database issue"

✓ Good:
"1. Check database connectivity:
   ```bash
   psql -h db.example.com -U app -c 'SELECT 1'
   ```
2. If connection fails, check credentials:
   [specific steps...]"
```

### Antipattern 2: Outdated Commands

```
❌ Bad:
```bash
docker ps  # We migrated to Kubernetes 6 months ago
```

✓ Good:
```bash
kubectl get pods -l app=api-service
```

**Prevention**: Test runbooks quarterly
```

### Antipattern 3: No Expected Outcomes

```
❌ Bad:
"Run this command:
```bash
kubectl get pods
```"

✓ Good:
"Run this command:
```bash
kubectl get pods -l app=api-service
```

Expected output:
```
NAME                          READY   STATUS    RESTARTS   AGE
api-service-7d9f8b6c4-abc12   1/1     Running   0          5m
```

If you see `CrashLoopBackOff`, proceed to Step 5."
```

### Antipattern 4: No Escalation Path

```
❌ Bad:
"If this doesn't work, good luck!"

✓ Good:
"If not resolved in 15 minutes:
- Escalate to @senior-engineer
- Join war room: [Zoom link]
- Related runbooks: [links]"
```

### Antipattern 5: Copy-Paste Errors

```
❌ Bad:
```bash
kubectl delete pod api-service-abc123  # Specific pod name
```

✓ Good:
```bash
kubectl delete pod <pod-name>  # Replace with actual pod name
# Or use label selector:
kubectl delete pods -l app=api-service --field-selector=status.phase=Failed
```
```

## Summary

Key takeaways for On-Call Playbooks and Runbooks:

1. **Document common incidents** - Don't reinvent the wheel each time
2. **Be specific** - Exact commands, expected outcomes, time estimates
3. **Test regularly** - Runbooks get stale quickly
4. **Keep updated** - Update after each incident
5. **Make discoverable** - Good organization and search
6. **Link from alerts** - Runbook URL in alert annotations
7. **Include escalation paths** - Know when to ask for help
8. **Version control** - Track changes over time
9. **Automate when possible** - But keep manual for complex/risky operations
10. **Continuous improvement** - Runbooks should evolve with system

## Related Skills

- `41-incident-management/incident-triage` - Initial incident assessment
- `41-incident-management/escalation-paths` - When and how to escalate
- `40-system-resilience/disaster-recovery` - DR runbooks and procedures
- `40-system-resilience/postmortem-analysis` - Learning from incidents to improve runbooks
