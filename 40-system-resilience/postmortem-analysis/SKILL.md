---
name: Postmortem Analysis
description: Comprehensive guide to conducting blameless postmortems and learning from incidents to improve system reliability
---

# Postmortem Analysis (Incident Review)

## Overview

A postmortem (also called incident review or retrospective) is a structured process for analyzing incidents to understand what happened, why it happened, and how to prevent similar incidents in the future. The goal is learning, not blaming.

**Core Principle**: "Blame the system, not the person. Every incident is an opportunity to learn and improve."

## 1. Purpose of Blameless Postmortems

### Why Blameless?

```
Traditional (Blame Culture):
"Who caused the outage?" → Engineer feels blamed → Hides mistakes → No learning

Blameless Culture:
"What system failures allowed this?" → Team investigates → Shares learnings → System improves
```

### Benefits

```
✓ Psychological safety - Engineers feel safe reporting issues
✓ Honest analysis - Root causes are identified
✓ Organizational learning - Knowledge is shared
✓ System improvement - Actionable fixes are implemented
✓ Cultural shift - Failures become learning opportunities
✓ Reduced MTTR - Better incident response over time
```

### Blameless Principles

1. **Assume good intent** - People make the best decisions with the information they have
2. **Focus on systems** - How did the system allow this to happen?
3. **Celebrate learning** - Incidents reveal system weaknesses
4. **Share widely** - Learnings benefit the entire organization
5. **Take action** - Identify and implement improvements

## 2. When to Conduct Postmortems

### Severity Threshold

```typescript
enum Severity {
  SEV0 = 0, // Always postmortem
  SEV1 = 1, // Always postmortem
  SEV2 = 2, // Postmortem recommended
  SEV3 = 3, // Optional postmortem
  SEV4 = 4  // No postmortem needed
}

function requiresPostmortem(severity: Severity, impact: Impact): boolean {
  // Always for SEV0 and SEV1
  if (severity <= Severity.SEV1) return true;

  // SEV2 if significant impact
  if (severity === Severity.SEV2) {
    return impact.usersAffected > 1000 || impact.revenue > 10000;
  }

  return false;
}
```

### Trigger Criteria

```
Conduct postmortem if:
✓ Customer-facing outage > 5 minutes
✓ Data loss or corruption
✓ Security incident
✓ Revenue impact > $10,000
✓ Users affected > 1,000
✓ SLA breach
✓ Repeated incidents (same root cause)
✓ Near-miss with potential for major impact
✓ New failure mode discovered
```

## 3. Postmortem Structure

### Complete Template

```markdown
# Postmortem: [Incident Title]

**Date**: 2024-01-15  
**Authors**: Alice Smith, Bob Johnson  
**Status**: Draft | Review | Final  
**Severity**: SEV1  

## Executive Summary
One-paragraph summary of what happened, impact, and resolution.

Example:
On January 15, 2024, our API experienced a complete outage for 47 minutes due to database connection pool exhaustion. This affected 100% of users and resulted in ~$50,000 in lost revenue. The issue was resolved by restarting the application servers and increasing the connection pool size.

## Impact
- **Duration**: 47 minutes (10:13 AM - 11:00 AM UTC)
- **Users Affected**: ~50,000 (100% of active users)
- **Requests Failed**: ~2.3 million
- **Revenue Lost**: ~$50,000
- **SLA Impact**: Breached 99.9% uptime SLA
- **Customer Complaints**: 237 support tickets

## Timeline
All times in UTC.

| Time | Event |
|------|-------|
| 10:00 | Deploy v2.5.0 to production (50% of instances) |
| 10:13 | First alerts: High error rate on API |
| 10:15 | On-call engineer paged |
| 10:18 | Engineer investigates, sees database connection errors |
| 10:22 | Incident escalated to SEV1 |
| 10:25 | War room established |
| 10:30 | Identified root cause: Connection pool exhaustion |
| 10:35 | Decision made to restart application servers |
| 10:40 | Rolling restart initiated |
| 10:55 | Error rate returning to normal |
| 11:00 | Incident resolved, monitoring continues |
| 11:30 | Postmortem meeting scheduled |

## Root Cause Analysis

### The Five Whys
1. **Why did the API go down?**  
   → Database connection pool was exhausted

2. **Why was the connection pool exhausted?**  
   → New code in v2.5.0 was leaking database connections

3. **Why was the code leaking connections?**  
   → Error handling didn't properly release connections on failure

4. **Why didn't we catch this before production?**  
   → Load testing didn't simulate error conditions

5. **Why didn't load testing include error conditions?**  
   → No process for testing error paths under load

### Root Cause
The new feature in v2.5.0 introduced a code path that failed to release database connections when errors occurred. Under normal conditions, this wasn't noticeable, but when a downstream service started returning errors, connections accumulated until the pool was exhausted.

### Contributing Factors
1. Code review didn't catch the connection leak
2. Unit tests didn't cover error paths
3. Load testing didn't simulate failures
4. No connection pool monitoring/alerting
5. Gradual rollout (50%) meant issue affected all users
6. No circuit breaker on downstream service

## What Went Well
- Incident detected quickly (2 minutes)
- On-call engineer responded promptly
- War room established efficiently
- Root cause identified in 17 minutes
- Decision to restart was correct
- Communication with customers was clear
- No data loss occurred

## What Went Wrong
- Code review missed connection leak
- Testing didn't cover error scenarios
- No monitoring for connection pool usage
- Rollout strategy didn't limit blast radius
- No circuit breaker for downstream service
- Recovery took longer than expected (47 min vs 15 min RTO)

## Action Items

| ID | Action | Owner | Due Date | Priority | Status |
|----|--------|-------|----------|----------|--------|
| AI-1 | Add connection pool monitoring and alerting | @alice | 2024-01-20 | P0 | In Progress |
| AI-2 | Implement circuit breaker for downstream service | @bob | 2024-01-25 | P0 | Not Started |
| AI-3 | Add error path testing to load test suite | @charlie | 2024-01-22 | P1 | Not Started |
| AI-4 | Update code review checklist (resource cleanup) | @diana | 2024-01-18 | P1 | Done |
| AI-5 | Implement canary deployment (5% → 50% → 100%) | @eve | 2024-02-01 | P1 | Not Started |
| AI-6 | Add linter rule for unclosed resources | @frank | 2024-01-30 | P2 | Not Started |
| AI-7 | Document connection pool best practices | @grace | 2024-01-25 | P2 | Not Started |

## Lessons Learned
1. **Always test error paths** - Happy path testing isn't enough
2. **Monitor resource usage** - Connection pools, memory, file handles
3. **Implement circuit breakers** - Prevent cascading failures
4. **Gradual rollouts need limits** - 50% can still affect 100% of users
5. **Automate resource cleanup** - Use try-finally or context managers

## Related Incidents
- INC-2023-045: Similar connection leak in payment service
- INC-2024-003: Database connection timeout (different root cause)

## Appendix

### Relevant Logs
```
2024-01-15 10:13:42 ERROR [pool] Connection pool exhausted (50/50 connections in use)
2024-01-15 10:13:43 ERROR [api] Cannot acquire database connection
2024-01-15 10:13:44 ERROR [api] Request failed: timeout waiting for connection
```

### Metrics
![Error Rate Graph](./images/error-rate.png)
![Connection Pool Usage](./images/connection-pool.png)

### Code Changes
The problematic code:
```typescript
async function processOrder(orderId: string) {
  const conn = await pool.getConnection();
  try {
    const order = await conn.query('SELECT * FROM orders WHERE id = ?', [orderId]);
    await externalService.validate(order); // Can throw error
    await conn.query('UPDATE orders SET status = ? WHERE id = ?', ['processed', orderId]);
  } catch (error) {
    logger.error('Order processing failed', error);
    throw error; // Connection not released!
  }
  conn.release(); // Only reached if no error
}
```

The fix:
```typescript
async function processOrder(orderId: string) {
  const conn = await pool.getConnection();
  try {
    const order = await conn.query('SELECT * FROM orders WHERE id = ?', [orderId]);
    await externalService.validate(order);
    await conn.query('UPDATE orders SET status = ? WHERE id = ?', ['processed', orderId]);
  } catch (error) {
    logger.error('Order processing failed', error);
    throw error;
  } finally {
    conn.release(); // Always released
  }
}
```
```

## 4. Postmortem Meeting Facilitation

### Meeting Structure (90 minutes)

```
1. Introduction (5 min)
   - Set blameless tone
   - Review meeting goals
   - Assign note-taker

2. Timeline Review (15 min)
   - Walk through events chronologically
   - Identify key decision points
   - Note what information was available

3. Root Cause Analysis (30 min)
   - Five Whys exercise
   - Fishbone diagram
   - Identify contributing factors

4. What Went Well / Wrong (20 min)
   - Celebrate successes
   - Identify improvement areas
   - Avoid blame language

5. Action Items (15 min)
   - Brainstorm preventive measures
   - Assign owners and deadlines
   - Prioritize actions

6. Lessons Learned (5 min)
   - Summarize key takeaways
   - Identify patterns

7. Next Steps (5 min)
   - Schedule follow-up
   - Plan for sharing learnings
```

### Facilitation Tips

```typescript
// Blameless language guide
const blamefulLanguage = {
  "Who broke production?": "What system failures led to this?",
  "Why didn't you test this?": "What testing gaps did we discover?",
  "This was a stupid mistake": "This revealed a system weakness",
  "You should have known": "What information was missing?",
  "Why did you deploy on Friday?": "What deployment safeguards can we add?"
};

// Facilitation checklist
const facilitationChecklist = [
  "Set blameless tone at start",
  "Redirect blame to system issues",
  "Encourage participation from all",
  "Focus on facts, not opinions",
  "Ask 'why' not 'who'",
  "Document action items with owners",
  "End with positive learnings",
  "Thank participants for honesty"
];
```

## 5. Blameless Culture Principles

### Creating Psychological Safety

```
1. Leadership sets the tone
   - Leaders admit their own mistakes
   - Celebrate learning from failures
   - Reward honesty over perfection

2. Normalize failure
   - "Failure is expected in complex systems"
   - Share postmortems widely
   - Discuss near-misses openly

3. Focus on systems, not people
   - "The system allowed this to happen"
   - "What safeguards were missing?"
   - "How can we prevent this systemically?"

4. Reward transparency
   - Thank people for reporting issues
   - Celebrate quick detection
   - Recognize honest analysis

5. Make it safe to experiment
   - Encourage innovation
   - Accept that experiments may fail
   - Learn from failed experiments
```

### Anti-Patterns to Avoid

```
❌ "Who did this?"
✓ "What happened?"

❌ "This could have been prevented if you..."
✓ "What safeguards could prevent this?"

❌ "Why didn't you know about X?"
✓ "What information was missing?"

❌ "This is your fault"
✓ "Let's understand the system failure"

❌ Punishing mistakes
✓ Learning from mistakes
```

## 6. Contributing Factors vs Root Causes

### Understanding the Difference

```
Root Cause:
The fundamental reason that, if removed, would prevent the incident

Contributing Factors:
Conditions that made the incident more likely or severe

Example Incident: Database Outage

Root Cause:
- Disk filled up due to unbounded log growth

Contributing Factors:
- No disk space monitoring
- No log rotation configured
- No alerts for disk usage
- Logs set to DEBUG level in production
- No automatic cleanup process
```

### Fishbone Diagram

```
                    Database Outage
                          |
        __________________|__________________
       |          |          |          |
    People    Process    Technology  Environment
       |          |          |          |
   No training  No runbook  No monitoring  High load
   On-call      No testing  No alerts      Traffic spike
   fatigue      Manual      Old version    DDoS attack
```

## 7. Documentation Standards

### Writing Guidelines

```
1. Be specific
   ❌ "The database was slow"
   ✓ "Database query latency increased from 50ms to 5000ms"

2. Include timestamps
   ❌ "We restarted the server"
   ✓ "10:35 UTC: Restarted application server"

3. Explain decisions
   ❌ "We rolled back"
   ✓ "Decided to rollback because fix would take >1 hour"

4. Use data
   ❌ "Many users were affected"
   ✓ "~50,000 users (80% of active users) were affected"

5. Be honest
   ❌ "Everything went smoothly"
   ✓ "Communication was delayed, causing confusion"
```

### Document Structure

```markdown
## Required Sections
- Executive Summary
- Impact (quantified)
- Timeline (with timestamps)
- Root Cause Analysis
- Action Items (with owners)

## Recommended Sections
- What Went Well
- What Went Wrong
- Lessons Learned
- Related Incidents

## Optional Sections
- Detailed Technical Analysis
- Code Snippets
- Metrics/Graphs
- Customer Communication
```

## 8. Postmortem Templates

### Google SRE Template

```markdown
# Incident Postmortem

## Incident Summary
[One paragraph: what, when, impact, resolution]

## Leadup
[What led to the incident? Recent changes, traffic patterns, etc.]

## Fault
[What specifically failed?]

## Impact
[Who/what was affected? For how long?]

## Detection
[How was the incident detected? How long did it take?]

## Response
[What actions were taken? Timeline of response]

## Recovery
[How was service restored? What fixed it?]

## Timeline
[Detailed chronological timeline]

## Root Causes
[Five Whys, contributing factors]

## Lessons Learned
[What did we learn?]

## Action Items
[Preventive measures with owners and deadlines]
```

### Atlassian Template

```markdown
# Incident Report

## Overview
- **Incident ID**: INC-2024-001
- **Date**: 2024-01-15
- **Severity**: SEV1
- **Duration**: 47 minutes
- **Impact**: 50,000 users

## What Happened
[Narrative description]

## Why It Happened
[Root cause analysis]

## How We Responded
[Response timeline and actions]

## What We're Doing About It
[Action items]

## Questions & Answers
[FAQ for stakeholders]
```

## 9. Action Item Tracking and Follow-Up

### Action Item Template

```typescript
interface ActionItem {
  id: string;
  description: string;
  owner: string;
  dueDate: Date;
  priority: 'P0' | 'P1' | 'P2' | 'P3';
  status: 'Not Started' | 'In Progress' | 'Done' | 'Blocked';
  blockedReason?: string;
  completedDate?: Date;
}

const actionItems: ActionItem[] = [
  {
    id: 'AI-1',
    description: 'Add connection pool monitoring',
    owner: '@alice',
    dueDate: new Date('2024-01-20'),
    priority: 'P0',
    status: 'In Progress'
  }
];
```

### Tracking System

```typescript
class ActionItemTracker {
  async trackProgress() {
    const items = await this.getActionItems();
    const overdue = items.filter(i => 
      i.status !== 'Done' && i.dueDate < new Date()
    );

    if (overdue.length > 0) {
      await this.notifyOwners(overdue);
      await this.escalate(overdue);
    }
  }

  async generateReport() {
    const items = await this.getActionItems();
    const stats = {
      total: items.length,
      completed: items.filter(i => i.status === 'Done').length,
      inProgress: items.filter(i => i.status === 'In Progress').length,
      overdue: items.filter(i => i.status !== 'Done' && i.dueDate < new Date()).length
    };

    return {
      stats,
      completionRate: stats.completed / stats.total,
      items: items.sort((a, b) => a.dueDate.getTime() - b.dueDate.getTime())
    };
  }
}

// Weekly action item review
cron.schedule('0 9 * * 1', async () => {
  const tracker = new ActionItemTracker();
  const report = await tracker.generateReport();
  await slack.postMessage({
    channel: '#incidents',
    text: `Action Item Report:\n${report.stats.completed}/${report.stats.total} completed\n${report.stats.overdue} overdue`
  });
});
```

## 10. Learning from Near-Misses

### What is a Near-Miss?

```
Near-Miss: An incident that could have caused significant impact but didn't due to luck or quick intervention.

Examples:
- Deployment bug caught in canary phase
- Database running out of space, cleaned up just in time
- Security vulnerability discovered before exploitation
- Load spike handled, but would have failed at 2x traffic
```

### Why Near-Misses Matter

```
Benefits of analyzing near-misses:
✓ Learn without customer impact
✓ Identify system weaknesses proactively
✓ Build resilience before real incidents
✓ Lower stakes for honest discussion
✓ More frequent learning opportunities
```

### Near-Miss Postmortem

```markdown
# Near-Miss Report: Canary Deployment Caught Critical Bug

## What Almost Happened
Deployment to 5% of production would have caused database corruption if rolled out to 100%.

## How We Caught It
- Canary monitoring detected elevated error rate
- Automatic rollback triggered
- Investigation revealed SQL injection vulnerability

## Impact if Not Caught
- Potential data corruption for all users
- Estimated recovery time: 4-8 hours
- Potential data loss
- SEV0 incident

## What We Learned
- Canary deployment saved us
- Need better SQL injection testing
- Code review missed vulnerability

## Action Items
- Add SQL injection tests to CI/CD
- Update code review checklist
- Implement prepared statements everywhere
```

## 11. Postmortem Database/Knowledge Base

### Organizing Postmortems

```
Structure:
/postmortems
  /2024
    /01-january
      - 2024-01-15-database-outage.md
      - 2024-01-22-api-latency.md
    /02-february
      - 2024-02-03-deployment-failure.md
  /templates
    - postmortem-template.md
  /index.md (searchable index)
```

### Searchable Index

```typescript
interface PostmortemIndex {
  id: string;
  date: Date;
  title: string;
  severity: string;
  rootCause: string;
  tags: string[];
  actionItemsCompleted: boolean;
}

// Search postmortems
async function searchPostmortems(query: string): Promise<PostmortemIndex[]> {
  const allPostmortems = await loadAllPostmortems();
  
  return allPostmortems.filter(pm =>
    pm.title.toLowerCase().includes(query.toLowerCase()) ||
    pm.rootCause.toLowerCase().includes(query.toLowerCase()) ||
    pm.tags.some(tag => tag.toLowerCase().includes(query.toLowerCase()))
  );
}

// Find similar incidents
async function findSimilarIncidents(currentIncident: Incident): Promise<PostmortemIndex[]> {
  const allPostmortems = await loadAllPostmortems();
  
  return allPostmortems.filter(pm =>
    pm.tags.some(tag => currentIncident.tags.includes(tag)) ||
    pm.rootCause.includes(currentIncident.symptoms)
  );
}
```

## 12. Sharing Postmortems

### Internal Sharing

```
1. Incident Review Meeting
   - Present to engineering team
   - Discuss learnings
   - Q&A session

2. Monthly Incident Review
   - Review all incidents from month
   - Identify patterns
   - Track action item progress

3. Engineering All-Hands
   - Share major incidents
   - Celebrate learnings
   - Recognize good incident response

4. Wiki/Documentation
   - Publish postmortems
   - Make searchable
   - Link related incidents
```

### Public Sharing

```
Benefits of public postmortems:
✓ Builds customer trust
✓ Demonstrates transparency
✓ Helps other companies learn
✓ Attracts talent (shows maturity)

Examples:
- GitLab: Publishes all postmortems
- Cloudflare: Detailed technical postmortems
- GitHub: Status page with incident reports
- PagerDuty: Public postmortem blog
```

### Public Postmortem Template

```markdown
# Public Incident Report

## Summary
On [date], we experienced [brief description]. This affected [impact]. The issue was resolved at [time].

## What Happened
[Customer-friendly explanation]

## Impact
- Duration: X minutes
- Users affected: Y%
- Services impacted: [list]

## Root Cause
[Non-technical explanation]

## Resolution
[What we did to fix it]

## Prevention
[What we're doing to prevent recurrence]

## Timeline
[Key events only]

We sincerely apologize for the disruption and appreciate your patience.

[Link to detailed technical postmortem]
```

## 13. Common Postmortem Antipatterns

### Antipattern 1: Blame Assignment

```
❌ Bad:
"Bob deployed buggy code that caused the outage"

✓ Good:
"A bug in the new feature caused the outage. Our testing didn't catch this because..."
```

### Antipattern 2: Surface-Level Analysis

```
❌ Bad:
Root Cause: "Server ran out of memory"
Action: "Restart server"

✓ Good:
Root Cause: "Memory leak in caching layer due to unbounded cache growth"
Actions:
- Implement cache size limits
- Add memory monitoring
- Add cache eviction policy
- Test under sustained load
```

### Antipattern 3: No Action Items

```
❌ Bad:
"We learned that we need better monitoring"

✓ Good:
Action Items:
- Add database connection pool monitoring (@alice, 2024-01-20)
- Implement circuit breaker (@bob, 2024-01-25)
- Update runbook with recovery steps (@charlie, 2024-01-22)
```

### Antipattern 4: Lost Follow-Up

```
❌ Bad:
Create action items, never track progress

✓ Good:
- Weekly action item review
- Automated reminders for overdue items
- Escalation for blocked items
- Celebrate completed items
```

## 14. Real Postmortem Examples

### Example 1: GitLab Database Incident (2017)

```markdown
# Postmortem: GitLab.com Database Incident

## Summary
On January 31, 2017, we lost 6 hours of database data due to accidental deletion of the production database.

## What Happened
1. Production database under heavy load
2. Engineer attempted to remove directory on wrong server
3. Removed production database instead of staging
4. Backup systems had failed (silently)
5. Only 6-hour-old backup was available

## Impact
- 6 hours of data lost
- 18 hours to recover
- 5,000 projects affected

## Root Causes
1. No confirmation for destructive operations
2. Backup systems not monitored
3. Backups not tested
4. Similar server names (production/staging)
5. High-stress situation led to mistake

## What We're Doing
1. Implement backup monitoring
2. Test backups weekly
3. Require confirmation for rm commands
4. Rename servers clearly
5. Implement infrastructure as code
6. Add more granular backups

## Lessons Learned
- Test your backups!
- Monitor backup systems
- Make destructive operations hard
- Don't work on production when tired
```

### Example 2: AWS S3 Outage (2017)

```markdown
# Summary of the Amazon S3 Service Disruption

## Overview
On February 28, 2017, S3 experienced high error rates in US-EAST-1 for approximately 4 hours.

## What Happened
An authorized S3 team member executed a command to remove a small number of servers for debugging. Unfortunately, the input to the command was entered incorrectly and a larger set of servers was removed than intended.

## Impact
- S3 API error rates increased
- S3 console unavailable
- Services depending on S3 affected
- AWS status page couldn't update (it uses S3)

## Resolution
- Subsystems had to be restarted in specific order
- Process took longer than expected
- Full recovery after 4 hours

## Prevention
1. Modified removal process to prevent large-scale removals
2. Added safeguards to command-line tools
3. Improved subsystem restart process
4. Moved status page to different storage
```

### Example 3: Knight Capital Trading Error (2012)

```markdown
# Knight Capital $440M Loss Postmortem

## Summary
On August 1, 2012, Knight Capital lost $440 million in 45 minutes due to a software deployment error.

## What Happened
1. New code deployed to 7 of 8 servers
2. 8th server had old code with repurposed flag
3. Old code activated, started errant trading
4. Bought high, sold low repeatedly
5. Lost $10 million per minute

## Root Causes
1. Non-atomic deployment
2. Repurposed feature flag
3. No deployment verification
4. No kill switch
5. No position limits

## Lessons
1. Ensure atomic deployments
2. Never repurpose flags
3. Verify all servers updated
4. Implement kill switches
5. Add position limits
6. Monitor for anomalies
```

## 15. Psychological Safety in Postmortems

### Building Trust

```
1. Leaders go first
   - Share their own mistakes
   - Model vulnerability
   - Accept responsibility

2. Celebrate honesty
   - Thank people for transparency
   - Reward early problem reporting
   - Recognize good incident response

3. No punishment for mistakes
   - Focus on system improvements
   - Avoid performance reviews tied to incidents
   - Separate learning from accountability

4. Make it safe to say "I don't know"
   - Encourage questions
   - Value curiosity
   - Admit uncertainty

5. Follow through on actions
   - Complete action items
   - Show that learnings lead to improvements
   - Close the feedback loop
```

### Measuring Psychological Safety

```typescript
// Survey questions (1-5 scale)
const psychologicalSafetyQuestions = [
  "I feel comfortable reporting mistakes",
  "My team discusses failures openly",
  "I'm not punished for honest mistakes",
  "I can ask questions without fear",
  "My team learns from incidents",
  "Postmortems focus on systems, not people",
  "I trust my team to support me during incidents"
];

// Track over time
async function measurePsychologicalSafety() {
  const responses = await conductSurvey(psychologicalSafetyQuestions);
  const average = responses.reduce((sum, r) => sum + r, 0) / responses.length;
  
  await logMetric('psychological_safety_score', average);
  
  if (average < 3.5) {
    await alertLeadership('Low psychological safety detected');
  }
}
```

## Summary

Key takeaways for Postmortem Analysis:

1. **Make it blameless** - Focus on systems, not people
2. **Conduct for all major incidents** - SEV0, SEV1, and significant SEV2
3. **Follow a structured process** - Use templates and facilitation guides
4. **Do root cause analysis** - Five Whys, fishbone diagrams
5. **Create actionable items** - With owners and deadlines
6. **Track action items** - Ensure they get completed
7. **Learn from near-misses** - Don't wait for major incidents
8. **Share learnings widely** - Internal and potentially public
9. **Build psychological safety** - Make it safe to report issues
10. **Follow through** - Show that postmortems lead to improvements

## Related Skills

- `40-system-resilience/failure-modes` - Understanding what can fail
- `40-system-resilience/chaos-engineering` - Proactively finding weaknesses
- `40-system-resilience/disaster-recovery` - Recovering from major incidents
- `00-meta-skills/documentation-practices` - Writing effective postmortems
