---
name: Incident Triage
description: Rapid assessment and initial response processes for production incidents
---

# Incident Triage

## Overview

Incident triage is the critical first phase of incident response where you rapidly assess the situation, classify severity, gather initial information, and determine the appropriate response. Effective triage can mean the difference between a 5-minute incident and a 5-hour outage.

**Core Principle**: "Fast assessment, clear communication, decisive action."

## 1. What is Incident Triage

### Definition

```
Triage: The process of rapidly assessing an incident to:
1. Understand what's broken
2. Determine severity and impact
3. Gather critical information
4. Decide on response strategy
5. Initiate appropriate escalation
```

### Triage vs Full Response

```
Triage (First 5-15 minutes):
- Quick assessment
- Severity classification
- Initial information gathering
- Communication initiation
- Resource mobilization

Full Response (After triage):
- Deep investigation
- Root cause analysis
- Detailed remediation
- Comprehensive communication
- Postmortem preparation
```

## 2. Triage Objectives

### 2.1 Rapid Assessment

```
Goal: Understand the situation in < 5 minutes

Key Questions:
- What is the primary symptom?
- When did it start?
- Is it getting worse?
- What's the blast radius?
```

### 2.2 Severity Classification

```
Determine severity level (SEV0-SEV4) based on:
- User impact (how many affected?)
- Business impact (revenue loss?)
- Functionality impact (what's broken?)
- Duration (how long has it been happening?)

Example:
- 100% of users can't login → SEV0
- 10% of users seeing slow search → SEV2
- UI button misaligned → SEV4
```

### 2.3 Resource Allocation

```
Based on severity, mobilize:
- SEV0: All hands, war room, executive notification
- SEV1: On-call team + subject matter experts
- SEV2: On-call engineer + team lead
- SEV3: On-call engineer only
```

### 2.4 Communication Initiation

```
Start communication immediately:
- Internal: Slack incident channel
- External: Status page update (for SEV0/1)
- Stakeholders: Executive notification (for SEV0)

First message template:
"🚨 Incident detected: [Brief description]
Severity: [SEV level]
Impact: [User/business impact]
Status: Investigating
Updates: Every 30 minutes"
```

## 3. Initial Assessment Questions

### The Critical Five

```typescript
interface InitialAssessment {
  whatIsBroken: string;
  howManyAffected: number | string; // "All users" or specific count
  isStillHappening: boolean;
  whenDidItStart: Date;
  whatChangedRecently: string[];
}

// Example
const assessment: InitialAssessment = {
  whatIsBroken: "API returning 500 errors on /api/users endpoint",
  howManyAffected: "~50,000 users (100% of active users)",
  isStillHappening: true,
  whenDidItStart: new Date("2024-01-15T10:13:00Z"),
  whatChangedRecently: [
    "Deployed v2.5.0 at 10:00 UTC",
    "Database migration ran at 09:30 UTC"
  ]
};
```

### What is Broken?

```
Be specific:
❌ "The site is down"
✓ "API Gateway returning 503 errors"

❌ "Database issues"
✓ "PostgreSQL primary database connection pool exhausted"

❌ "Users complaining"
✓ "Login page timing out after 30 seconds"
```

### How Many Users Affected?

```
Quantify impact:
- All users (100%)
- Majority of users (>50%)
- Significant portion (~10-50%)
- Small subset (<10%)
- Single user/tenant

Sources:
- Error rate metrics
- Active user count
- Support ticket volume
- Social media mentions
```

### Is It Still Happening?

```
Determine current state:
- Active: Still occurring right now
- Intermittent: Coming and going
- Resolved: No longer occurring (but investigate why)

Check:
- Real-time error rates
- Recent logs (last 5 minutes)
- Synthetic monitoring
- User reports
```

### What Changed Recently?

```
Look for changes in last 24 hours:
- Code deployments
- Configuration changes
- Database migrations
- Infrastructure changes
- Dependency updates
- Traffic patterns (marketing campaign?)
- External events (AWS outage?)

Command to check:
git log --since="24 hours ago" --oneline
kubectl rollout history deployment/api-service
```

## 4. Triage Checklist

### Quick Triage Checklist (5 minutes)

```markdown
## Incident Triage Checklist

### 1. Initial Detection (1 min)
- [ ] Alert received or incident reported
- [ ] Acknowledge alert in PagerDuty/Opsgenie
- [ ] Note detection time

### 2. Quick Assessment (2 min)
- [ ] Check monitoring dashboards
- [ ] Review error rates (last 15 minutes)
- [ ] Check recent deployments
- [ ] Verify scope (how many users?)
- [ ] Determine if still active

### 3. Severity Classification (1 min)
- [ ] Classify as SEV0/1/2/3/4
- [ ] Document reasoning

### 4. Communication (1 min)
- [ ] Create incident Slack channel
- [ ] Post initial status
- [ ] Update status page (if SEV0/1)
- [ ] Page additional responders (if needed)

### 5. Initial Actions (varies)
- [ ] Decide: investigate or rollback?
- [ ] Assign incident commander (if SEV0/1)
- [ ] Start war room (if SEV0)
- [ ] Begin investigation or mitigation
```

## 5. Information Gathering

### 5.1 Logs

```bash
# Recent errors
kubectl logs -l app=api-service --since=15m | grep ERROR

# Specific pod logs
kubectl logs api-service-7d9f8b6c4-xk2lm --tail=100

# Application logs
tail -f /var/log/app/error.log | grep -i "exception\|error\|fatal"

# Database logs
tail -f /var/log/postgresql/postgresql.log
```

```typescript
// Structured log query (e.g., CloudWatch Logs Insights)
const query = `
  fields @timestamp, @message, level, error
  | filter level = "ERROR"
  | filter @timestamp > ago(15m)
  | sort @timestamp desc
  | limit 100
`;
```

### 5.2 Metrics

```typescript
// Key metrics to check
interface TriageMetrics {
  errorRate: number;        // Errors per second
  requestRate: number;      // Requests per second
  p99Latency: number;       // 99th percentile latency
  cpuUsage: number;         // CPU utilization %
  memoryUsage: number;      // Memory utilization %
  activeConnections: number; // Database connections
  queueDepth: number;       // Message queue depth
}

// Quick dashboard check
const metrics = await getMetrics({
  timeRange: 'last_15_minutes',
  services: ['api-gateway', 'user-service', 'database']
});

console.log(`Error rate: ${metrics.errorRate}/s`);
console.log(`P99 latency: ${metrics.p99Latency}ms`);
```

### 5.3 Traces

```typescript
// Distributed tracing query
// Find slow or failing requests
const traces = await tracing.query({
  service: 'api-gateway',
  operation: 'GET /api/users',
  minDuration: '5s',
  status: 'error',
  limit: 10
});

// Analyze trace
traces.forEach(trace => {
  console.log(`Trace ID: ${trace.id}`);
  console.log(`Duration: ${trace.duration}ms`);
  console.log(`Error: ${trace.error}`);
  console.log(`Spans: ${trace.spans.length}`);
});
```

### 5.4 Error Rates

```typescript
// Calculate error rate
async function getErrorRate(service: string, minutes: number = 15) {
  const now = Date.now();
  const start = now - (minutes * 60 * 1000);

  const total = await metrics.query({
    metric: 'http_requests_total',
    service,
    start,
    end: now
  });

  const errors = await metrics.query({
    metric: 'http_requests_total',
    service,
    status: '5xx',
    start,
    end: now
  });

  return {
    total,
    errors,
    errorRate: errors / total,
    errorPercentage: (errors / total) * 100
  };
}

// Usage
const rate = await getErrorRate('api-service', 15);
console.log(`Error rate: ${rate.errorPercentage.toFixed(2)}%`);
```

### 5.5 User Reports

```typescript
// Check support tickets
const recentTickets = await zendesk.search({
  query: 'status:open created>15m',
  sort: 'created_at desc'
});

// Check social media
const tweets = await twitter.search({
  query: '@yourcompany down OR broken',
  since: '15m'
});

// Aggregate user reports
const userReports = {
  supportTickets: recentTickets.length,
  socialMentions: tweets.length,
  commonIssues: extractCommonIssues(recentTickets, tweets)
};
```

### 5.6 Deployment History

```bash
# Recent deployments
kubectl rollout history deployment/api-service

# Git commits in last 24 hours
git log --since="24 hours ago" --pretty=format:"%h - %an, %ar : %s"

# Terraform changes
terraform show | grep "last_modified"

# Database migrations
SELECT * FROM schema_migrations 
ORDER BY applied_at DESC 
LIMIT 10;
```

## 6. Quick Diagnosis Techniques

### 6.1 Check Recent Changes

```typescript
// Automated change detection
async function checkRecentChanges() {
  const changes = {
    deployments: await getRecentDeployments(24), // last 24 hours
    configChanges: await getConfigChanges(24),
    dbMigrations: await getDatabaseMigrations(24),
    infraChanges: await getTerraformChanges(24)
  };

  // Correlate with incident start time
  const incidentStart = new Date('2024-01-15T10:13:00Z');
  const suspiciousChanges = [];

  for (const [type, items] of Object.entries(changes)) {
    for (const item of items) {
      if (item.timestamp < incidentStart && 
          item.timestamp > new Date(incidentStart.getTime() - 60*60*1000)) {
        suspiciousChanges.push({ type, ...item });
      }
    }
  }

  return suspiciousChanges;
}
```

### 6.2 Review Monitoring Dashboards

```
Essential dashboards to check:
1. Service health overview
2. Error rates by endpoint
3. Latency percentiles (p50, p95, p99)
4. Infrastructure metrics (CPU, memory, disk)
5. Database performance
6. External dependencies status

Quick wins:
- Look for sudden spikes or drops
- Compare to baseline (same time yesterday)
- Check all services, not just suspected one
```

### 6.3 Query Logs

```bash
# Find errors in last 15 minutes
grep -i "error\|exception\|fatal" /var/log/app/*.log | \
  awk '{print $1, $2}' | \
  sort | uniq -c | sort -rn | head -20

# Find specific error pattern
grep "Connection refused" /var/log/app/*.log | tail -50

# Count errors by type
awk '/ERROR/ {print $5}' /var/log/app/app.log | \
  sort | uniq -c | sort -rn
```

```typescript
// Structured log analysis
async function analyzeRecentErrors() {
  const logs = await cloudwatch.query({
    logGroup: '/aws/lambda/api-service',
    query: `
      fields @timestamp, @message, level, error
      | filter level = "ERROR"
      | filter @timestamp > ago(15m)
      | stats count() by error
      | sort count desc
    `
  });

  return logs;
}
```

### 6.4 Test Critical Paths

```bash
# Quick health check
curl -i https://api.example.com/health

# Test authentication
curl -X POST https://api.example.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Test critical endpoint
curl -i https://api.example.com/api/users/123

# Check database connectivity
psql -h db.example.com -U app -c "SELECT 1;"

# Check Redis
redis-cli -h cache.example.com ping
```

```typescript
// Automated critical path testing
async function testCriticalPaths() {
  const results = {
    health: await testEndpoint('GET', '/health'),
    auth: await testEndpoint('POST', '/auth/login', { email: 'test@example.com', password: 'test' }),
    userAPI: await testEndpoint('GET', '/api/users/123'),
    database: await testDatabase(),
    cache: await testCache()
  };

  const failures = Object.entries(results)
    .filter(([_, result]) => !result.success)
    .map(([name, result]) => ({ name, error: result.error }));

  return { results, failures };
}
```

## 7. Decision: Escalate or Resolve

### Decision Tree

```
START
  |
  ├─ Can I fix this in < 5 minutes?
  │   ├─ YES → Fix it, monitor, document
  │   └─ NO → Continue
  |
  ├─ Is it SEV0 or SEV1?
  │   ├─ YES → Escalate immediately
  │   └─ NO → Continue
  |
  ├─ Do I know the root cause?
  │   ├─ YES → Implement fix or escalate if complex
  │   └─ NO → Continue
  |
  ├─ Is there an obvious recent change?
  │   ├─ YES → Rollback and monitor
  │   └─ NO → Continue
  |
  ├─ Do I need subject matter expert?
  │   ├─ YES → Escalate to SME
  │   └─ NO → Continue investigating
  |
  └─ Escalate to next level
```

### Quick Win Scenarios (Resolve Immediately)

```
1. Recent deployment causing issues
   → Rollback deployment
   → Monitor for 5 minutes
   → Document and create postmortem

2. Known issue with known fix
   → Apply fix from runbook
   → Verify resolution
   → Document

3. Resource exhaustion (disk, memory)
   → Clear logs/cache
   → Scale up resources
   → Monitor

4. Configuration error
   → Revert to last known good config
   → Verify
   → Document
```

### Escalation Scenarios

```
1. Unknown root cause after 15 minutes
   → Escalate to senior engineer

2. Requires database expertise
   → Escalate to DBA

3. Affects multiple services
   → Escalate to architect

4. SEV0 incident
   → Escalate to all hands

5. Requires vendor support
   → Open support ticket, escalate internally
```

## 8. Documenting Triage Findings

### Triage Notes Template

```markdown
# Incident Triage Notes

**Incident ID**: INC-2024-001
**Detected**: 2024-01-15 10:13 UTC
**Triaged By**: @alice
**Severity**: SEV1

## Initial Assessment

**What's Broken**: API Gateway returning 503 errors on all endpoints

**Impact**:
- Users affected: ~50,000 (100% of active users)
- Services affected: Web app, mobile app, public API
- Business impact: Unable to process orders, ~$10k/hour revenue loss

**Timeline**:
- 10:00 UTC: Deployed v2.5.0 to production
- 10:13 UTC: First alerts received
- 10:15 UTC: Triage started

**Still Happening**: Yes, ongoing

## Information Gathered

**Metrics**:
- Error rate: 95% (baseline: 0.1%)
- Request rate: 1000/s (normal)
- P99 latency: 30s (baseline: 200ms)
- CPU: 45% (normal)
- Memory: 78% (normal)

**Logs**:
```
[ERROR] Database connection pool exhausted (50/50 connections in use)
[ERROR] Timeout waiting for database connection
```

**Recent Changes**:
- v2.5.0 deployed at 10:00 UTC (new feature: order recommendations)
- No infrastructure changes
- No database migrations

## Initial Diagnosis

**Suspected Root Cause**: Connection leak in new code (v2.5.0)

**Evidence**:
- Timing correlates with deployment
- Connection pool exhaustion errors
- No infrastructure issues

## Actions Taken

1. ✅ Created incident channel #inc-2024-001
2. ✅ Updated status page
3. ✅ Paged senior engineer @bob
4. ✅ Started war room
5. 🔄 Investigating connection leak in v2.5.0

## Next Steps

1. Review v2.5.0 code for connection leaks
2. If found: Rollback to v2.4.9
3. If not found: Escalate to database team
4. Monitor connection pool usage

## Communication

- Status page: Updated at 10:15 UTC
- Internal: #inc-2024-001 channel
- Next update: 10:30 UTC (15 minutes)
```

## 9. Triage Tools

### 9.1 PagerDuty

```typescript
// Acknowledge incident
await pagerduty.incidents.acknowledge({
  incident_id: 'PT4KHLK',
  from: 'alice@example.com'
});

// Add note
await pagerduty.incidents.addNote({
  incident_id: 'PT4KHLK',
  note: 'Triage complete. SEV1. Database connection pool exhausted.'
});

// Escalate
await pagerduty.incidents.escalate({
  incident_id: 'PT4KHLK',
  escalation_policy_id: 'P123ABC'
});
```

### 9.2 Opsgenie

```typescript
// Acknowledge alert
await opsgenie.alerts.acknowledge({
  identifier: 'alert-123',
  user: 'alice@example.com',
  note: 'Triaging incident'
});

// Add details
await opsgenie.alerts.addDetails({
  identifier: 'alert-123',
  details: {
    severity: 'SEV1',
    affectedUsers: '50000',
    rootCause: 'Connection pool exhausted'
  }
});
```

### 9.3 Incident.io

```typescript
// Create incident
const incident = await incidentio.incidents.create({
  title: 'API Gateway 503 errors',
  severity: 'sev1',
  status: 'investigating',
  summary: 'All API endpoints returning 503 due to database connection pool exhaustion'
});

// Update incident
await incidentio.incidents.update(incident.id, {
  status: 'identified',
  summary: 'Connection leak in v2.5.0 deployment identified. Rolling back.'
});
```

### 9.4 Jira Service Management

```typescript
// Create incident ticket
const issue = await jira.issues.create({
  fields: {
    project: { key: 'INC' },
    issuetype: { name: 'Incident' },
    summary: 'API Gateway 503 errors - SEV1',
    description: 'Database connection pool exhausted after v2.5.0 deployment',
    priority: { name: 'Critical' },
    customfield_10001: 'SEV1' // Severity field
  }
});
```

## 10. Triage SLAs (Time Limits)

### Response SLAs

```
Severity | Acknowledge | Initial Triage | First Update
---------|-------------|----------------|-------------
SEV0     | 5 minutes   | 10 minutes     | 15 minutes
SEV1     | 15 minutes  | 30 minutes     | 30 minutes
SEV2     | 1 hour      | 2 hours        | 2 hours
SEV3     | 4 hours     | Next day       | Next day
SEV4     | Next day    | Next week      | Next week
```

### Triage Time Limits

```typescript
interface TriageSLA {
  severity: string;
  maxTriageTime: number; // minutes
  escalateAfter: number;  // minutes
}

const triageSLAs: TriageSLA[] = [
  { severity: 'SEV0', maxTriageTime: 10, escalateAfter: 15 },
  { severity: 'SEV1', maxTriageTime: 30, escalateAfter: 45 },
  { severity: 'SEV2', maxTriageTime: 120, escalateAfter: 180 },
  { severity: 'SEV3', maxTriageTime: 480, escalateAfter: 1440 }
];

// Auto-escalate if triage takes too long
function checkTriageSLA(incident: Incident) {
  const sla = triageSLAs.find(s => s.severity === incident.severity);
  const triageTime = Date.now() - incident.detectedAt.getTime();
  const triageMinutes = triageTime / (60 * 1000);

  if (triageMinutes > sla.escalateAfter) {
    escalateIncident(incident, 'Triage SLA exceeded');
  }
}
```

## 11. Handoff Procedures

### Handoff Checklist

```markdown
## Incident Handoff Checklist

### Context Transfer
- [ ] Incident ID and severity
- [ ] What's broken (specific symptoms)
- [ ] Impact (users, revenue, services)
- [ ] Timeline (when started, key events)
- [ ] What's been tried so far
- [ ] Current hypothesis
- [ ] Relevant links (dashboards, logs, runbooks)

### Communication Handoff
- [ ] Incident channel ownership
- [ ] Status page update responsibility
- [ ] Stakeholder notification
- [ ] Next update timing

### Access Transfer
- [ ] Necessary permissions granted
- [ ] VPN/SSH access confirmed
- [ ] Tool access verified

### Action Items
- [ ] Current action in progress
- [ ] Next steps documented
- [ ] Blockers identified
```

### Handoff Message Template

```
🔄 **Incident Handoff**

**From**: @alice
**To**: @bob
**Time**: 10:45 UTC

**Incident**: INC-2024-001 (SEV1)
**Summary**: API Gateway 503 errors due to database connection pool exhaustion

**What We Know**:
- Started at 10:13 UTC after v2.5.0 deployment
- 100% of users affected
- Connection pool exhausted (50/50 connections)
- Suspected connection leak in new code

**What We've Tried**:
- ✅ Reviewed logs (found connection errors)
- ✅ Checked metrics (confirmed pool exhaustion)
- ✅ Reviewed v2.5.0 code (found potential leak in order recommendations)
- 🔄 Preparing rollback to v2.4.9

**Current Action**:
Rolling back to v2.4.9 (ETA: 5 minutes)

**Next Steps**:
1. Complete rollback
2. Monitor for 10 minutes
3. If resolved, investigate v2.5.0 code offline
4. If not resolved, escalate to database team

**Links**:
- Incident channel: #inc-2024-001
- Dashboard: https://grafana.example.com/d/incident
- Runbook: https://wiki.example.com/runbooks/rollback

**Questions?** Ask in #inc-2024-001
```

## 12. Common Triage Mistakes

### Mistake 1: Analysis Paralysis

```
❌ Problem:
Spending 30 minutes investigating before taking action

✓ Solution:
- Set 5-minute timer for initial triage
- Make decision: rollback, escalate, or investigate
- Don't let perfect be enemy of good
```

### Mistake 2: Premature Root Cause Claims

```
❌ Problem:
"It's definitely the database" (without evidence)

✓ Solution:
- Use "suspected" or "likely" language
- Gather evidence before claiming root cause
- Be willing to pivot when evidence contradicts hypothesis
```

### Mistake 3: Solo Hero Mode

```
❌ Problem:
Trying to fix everything alone without escalating

✓ Solution:
- Escalate early for SEV0/1
- Ask for help after 15 minutes if stuck
- Incident response is a team sport
```

### Mistake 4: Poor Communication

```
❌ Problem:
No updates for 45 minutes during SEV1

✓ Solution:
- Set update cadence (every 15-30 minutes)
- Even if no progress: "Still investigating, next update in 15 min"
- Silence creates anxiety
```

### Mistake 5: Ignoring Recent Changes

```
❌ Problem:
Deep-diving into code without checking recent deployments

✓ Solution:
- Always check: What changed recently?
- Correlation doesn't prove causation, but it's a strong hint
- Rollback is often faster than debug
```

## 13. Triage Runbooks for Common Scenarios

### Runbook 1: High Error Rate

```markdown
# Runbook: High Error Rate

## Symptoms
- Error rate > 5%
- Alerts firing for HTTP 5xx errors

## Triage Steps (5 minutes)

1. **Check error rate trend**
   ```bash
   # Is it increasing, stable, or decreasing?
   curl "https://grafana.example.com/api/datasources/proxy/1/api/v1/query?query=rate(http_requests_total{status=~'5..'}[5m])"
   ```

2. **Identify affected endpoints**
   ```bash
   # Which endpoints are failing?
   kubectl logs -l app=api-service --since=5m | grep "HTTP/1.1 5" | awk '{print $7}' | sort | uniq -c | sort -rn
   ```

3. **Check recent deployments**
   ```bash
   kubectl rollout history deployment/api-service
   ```

4. **Review error logs**
   ```bash
   kubectl logs -l app=api-service --since=5m | grep ERROR | tail -20
   ```

## Decision Tree

- If error rate > 50% AND recent deployment → **Rollback**
- If specific endpoint failing → **Disable endpoint, investigate**
- If database errors → **Escalate to database team**
- If external API errors → **Check vendor status, implement fallback**

## Quick Fixes

- Rollback deployment: `kubectl rollout undo deployment/api-service`
- Restart pods: `kubectl rollout restart deployment/api-service`
- Scale up: `kubectl scale deployment/api-service --replicas=10`
```

### Runbook 2: Service Completely Down

```markdown
# Runbook: Service Completely Down

## Symptoms
- Health check failing
- 100% error rate or no traffic

## Triage Steps (5 minutes)

1. **Verify service is actually down**
   ```bash
   curl -i https://api.example.com/health
   # Expected: 200 OK
   # Actual: Connection refused / timeout
   ```

2. **Check if pods are running**
   ```bash
   kubectl get pods -l app=api-service
   # Look for: Running, CrashLoopBackOff, ImagePullBackOff
   ```

3. **Check pod logs**
   ```bash
   kubectl logs -l app=api-service --tail=50
   ```

4. **Check recent changes**
   ```bash
   kubectl rollout history deployment/api-service
   ```

## Common Causes & Fixes

### Pods CrashLooping
```bash
# Check why pods are crashing
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous

# If bad deployment → Rollback
kubectl rollout undo deployment/api-service
```

### No Pods Running
```bash
# Check deployment
kubectl get deployment api-service

# Check if scaled to 0
kubectl scale deployment/api-service --replicas=3
```

### Database Connection Failed
```bash
# Test database connectivity
kubectl run -it --rm debug --image=postgres:14 --restart=Never -- psql -h db.example.com -U app -c "SELECT 1"

# If database down → Escalate to database team
```
```

### Runbook 3: Slow Response Times

```markdown
# Runbook: Slow Response Times

## Symptoms
- P99 latency > 2x baseline
- Timeout errors
- User complaints about slowness

## Triage Steps (5 minutes)

1. **Check latency metrics**
   ```bash
   # Current P99 latency
   curl "https://grafana.example.com/api/datasources/proxy/1/api/v1/query?query=histogram_quantile(0.99, http_request_duration_seconds_bucket)"
   ```

2. **Identify slow endpoints**
   ```bash
   # Which endpoints are slow?
   kubectl logs -l app=api-service --since=5m | grep "duration" | awk '{print $5, $8}' | sort -rn | head -10
   ```

3. **Check resource usage**
   ```bash
   # CPU and memory
   kubectl top pods -l app=api-service
   ```

4. **Check database performance**
   ```sql
   -- Long-running queries
   SELECT pid, now() - query_start AS duration, query
   FROM pg_stat_activity
   WHERE state = 'active'
   ORDER BY duration DESC
   LIMIT 10;
   ```

## Common Causes & Fixes

### High CPU
```bash
# Scale up
kubectl scale deployment/api-service --replicas=10
```

### Slow Database Queries
```sql
-- Kill long-running query
SELECT pg_terminate_backend(pid);

-- Escalate to database team for query optimization
```

### External API Slow
```bash
# Check vendor status page
# Implement timeout and fallback
```
```

## 14. War Room Setup

### When to Establish War Room

```
Criteria for war room:
- SEV0 incident (always)
- SEV1 lasting > 30 minutes
- Multiple teams needed
- Executive visibility required
- Complex coordination needed
```

### War Room Roles

```
Incident Commander (IC):
- Leads response
- Makes decisions
- Coordinates teams
- Owns communication

Technical Lead:
- Deep technical investigation
- Implements fixes
- Coordinates with IC

Communications Lead:
- Status page updates
- Stakeholder communication
- Customer support liaison

Scribe:
- Documents timeline
- Takes notes
- Tracks action items
```

### War Room Setup Checklist

```markdown
## War Room Setup

### Virtual War Room (Zoom/Meet)
- [ ] Create video call
- [ ] Share link in incident channel
- [ ] Pin link to channel topic
- [ ] Mute all by default
- [ ] Enable screen sharing

### Incident Channel (Slack)
- [ ] Create #inc-YYYY-NNN channel
- [ ] Set channel topic with incident summary
- [ ] Pin important links (dashboard, runbook, war room)
- [ ] Invite relevant people
- [ ] Set up bot for status updates

### Shared Documents
- [ ] Create incident timeline doc
- [ ] Create action items tracker
- [ ] Share edit access with responders

### Monitoring
- [ ] Open relevant dashboards
- [ ] Set up alerts for key metrics
- [ ] Share screen in war room

### Communication
- [ ] Post initial status update
- [ ] Update status page
- [ ] Notify stakeholders
- [ ] Set update cadence (every 15-30 min)
```

## 15. Real Triage Scenarios and Walkthroughs

### Scenario 1: Database Connection Pool Exhausted

```
10:13 UTC - Alert: High error rate on API

Triage (10:13-10:18):
1. Check error rate: 95% (baseline: 0.1%) ✓
2. Check logs: "Connection pool exhausted" ✓
3. Check recent changes: v2.5.0 deployed at 10:00 ✓
4. Classify: SEV1 (100% users affected) ✓
5. Create incident channel ✓
6. Update status page ✓

Decision (10:18):
- Suspected: Connection leak in v2.5.0
- Action: Rollback to v2.4.9
- Reason: Fast mitigation, investigate offline

Actions (10:18-10:25):
1. Rollback deployment ✓
2. Monitor error rate ✓
3. Error rate drops to 0.2% ✓
4. Incident resolved ✓

Total time: 12 minutes
```

### Scenario 2: Third-Party API Down

```
14:22 UTC - Alert: Payment processing failing

Triage (14:22-14:27):
1. Check error rate: 100% on /api/checkout ✓
2. Check logs: "Stripe API timeout" ✓
3. Check Stripe status: Major outage ✓
4. Classify: SEV1 (can't process payments) ✓
5. Create incident channel ✓

Decision (14:27):
- Root cause: Stripe outage (external)
- Action: Enable fallback payment processor
- Reason: Can't fix Stripe, need alternative

Actions (14:27-14:35):
1. Enable feature flag for backup processor ✓
2. Test checkout flow ✓
3. Update status page (degraded, using backup) ✓
4. Monitor payment success rate ✓

Total time: 13 minutes
```

### Scenario 3: Gradual Performance Degradation

```
09:00 UTC - Alert: P99 latency increasing

Triage (09:00-09:10):
1. Check latency: P99 = 2s (baseline: 200ms) ✓
2. Check trend: Gradually increasing over 2 hours ✓
3. Check recent changes: None in last 24 hours ✓
4. Check resource usage: Memory at 95% ✓
5. Classify: SEV2 (degraded, not down) ✓

Decision (09:10):
- Suspected: Memory leak
- Action: Restart pods, investigate leak
- Reason: Quick mitigation, then root cause

Actions (09:10-09:20):
1. Rolling restart of pods ✓
2. Memory usage drops to 40% ✓
3. Latency returns to normal ✓
4. Create ticket to investigate memory leak ✓

Total time: 20 minutes
```

## Summary

Key takeaways for Incident Triage:

1. **Speed matters** - Triage in < 5 minutes
2. **Ask the right questions** - What, who, when, still happening, what changed
3. **Classify severity quickly** - Determines response urgency
4. **Communicate early and often** - Don't go silent
5. **Gather evidence** - Logs, metrics, traces, user reports
6. **Check recent changes first** - Often the culprit
7. **Decide quickly** - Rollback, escalate, or investigate
8. **Document everything** - Timeline, actions, decisions
9. **Know when to escalate** - Don't be a hero
10. **Use runbooks** - Don't reinvent the wheel

## Related Skills

- `41-incident-management/severity-levels` - Classifying incident severity
- `41-incident-management/oncall-playbooks` - Detailed response procedures
- `41-incident-management/escalation-paths` - When and how to escalate
- `40-system-resilience/postmortem-analysis` - Learning from incidents
