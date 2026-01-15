---
name: Stakeholder Communication
description: Effective communication strategies for incidents across all stakeholder groups
---

# Stakeholder Communication During Incidents

## Overview

Effective communication during incidents is critical for maintaining trust, managing expectations, and coordinating response efforts. Poor communication can turn a technical incident into a PR crisis.

**Core Principle**: "Communicate early, often, and clearly. Silence creates anxiety."

## 1. Who Are Stakeholders During Incidents

### Stakeholder Categories

```
External Stakeholders:
✓ End users (customers)
✓ Enterprise clients
✓ Business partners / integrations
✓ Media / public (for major incidents)
✓ Regulators (for compliance incidents)

Internal Stakeholders:
✓ Engineering teams
✓ Customer support
✓ Sales team
✓ Product management
✓ Executive leadership (C-suite)
✓ Legal / compliance
✓ PR / communications team
```

### Stakeholder Needs by Type

```typescript
interface StakeholderNeeds {
  group: string;
  primaryConcern: string;
  updateFrequency: string;
  detailLevel: string;
  channel: string[];
}

const stakeholderNeeds: StakeholderNeeds[] = [
  {
    group: 'End Users',
    primaryConcern: 'When will service be restored?',
    updateFrequency: 'Every 30-60 minutes',
    detailLevel: 'High-level, non-technical',
    channel: ['Status page', 'Email', 'In-app banner']
  },
  {
    group: 'Enterprise Clients',
    primaryConcern: 'Business impact, SLA credits',
    updateFrequency: 'Every 15-30 minutes',
    detailLevel: 'Detailed, with business impact',
    channel: ['Direct email', 'Phone call', 'Dedicated Slack']
  },
  {
    group: 'Engineering Teams',
    primaryConcern: 'Technical details, how to help',
    updateFrequency: 'Real-time',
    detailLevel: 'Highly technical',
    channel: ['Slack incident channel', 'War room']
  },
  {
    group: 'Executives',
    primaryConcern: 'Business impact, PR risk, resolution ETA',
    updateFrequency: 'Every 30 minutes',
    detailLevel: 'Executive summary + key details',
    channel: ['Slack DM', 'Email', 'Phone (SEV0)']
  },
  {
    group: 'Customer Support',
    primaryConcern: 'What to tell customers, workarounds',
    updateFrequency: 'Every 15 minutes',
    detailLevel: 'Customer-facing talking points',
    channel: ['Slack support channel', 'Email']
  }
];
```

## 2. Communication Channels

### 2.1 Status Page

```
Purpose: Public-facing incident updates

Tools:
- Statuspage.io (Atlassian)
- Status.io
- Instatus
- Custom status page

Best Practices:
✓ Update within 15 minutes of SEV0/1
✓ Use clear, non-technical language
✓ Provide ETA when known (or "investigating")
✓ Update every 30-60 minutes
✓ Mark as resolved only when fully stable
```

**Status Page Example**:
```markdown
## Major Outage - API Service
**Status**: Investigating
**Started**: Jan 15, 2024 10:13 UTC
**Last Update**: Jan 15, 2024 10:45 UTC

We are currently experiencing a major outage affecting our API service. Users are unable to access the application. Our team is actively investigating the issue and working on a resolution.

**Impact**: All users
**Affected Services**: Web App, Mobile App, Public API

**Next Update**: 11:15 UTC (30 minutes)
```

### 2.2 Email Notifications

```
Purpose: Direct communication to affected users

When to Use:
- SEV0/1 incidents affecting all users
- Extended outages (> 1 hour)
- Post-incident summary
- Enterprise customer notifications

Segments:
- All users
- Affected users only
- Enterprise customers
- Free tier users
```

**Email Template**:
```html
Subject: [Resolved] Service Disruption - January 15, 2024

Dear Customer,

We experienced a service disruption today from 10:13 UTC to 11:00 UTC (47 minutes) that prevented access to our application.

What Happened:
A database connection issue caused our API service to become unavailable.

Impact:
- Duration: 47 minutes
- Affected: All users
- Services: Web app, mobile app, API

Resolution:
Our team identified and resolved the issue by rolling back a recent deployment. Service has been fully restored and is operating normally.

What We're Doing:
We're conducting a thorough investigation to prevent this from happening again. We'll publish a detailed postmortem within 48 hours.

We sincerely apologize for the disruption and appreciate your patience.

If you have any questions, please contact support@example.com.

Best regards,
The Example Team
```

### 2.3 In-App Messages

```typescript
// In-app banner for active incidents
interface IncidentBanner {
  severity: string;
  message: string;
  link: string;
  dismissible: boolean;
}

const banner: IncidentBanner = {
  severity: 'error',
  message: 'We are experiencing technical difficulties. Some features may be unavailable.',
  link: 'https://status.example.com',
  dismissible: false
};

// Display banner
function showIncidentBanner(banner: IncidentBanner) {
  const bannerEl = document.createElement('div');
  bannerEl.className = `banner banner-${banner.severity}`;
  bannerEl.innerHTML = `
    <span>${banner.message}</span>
    <a href="${banner.link}" target="_blank">View Status</a>
    ${banner.dismissible ? '<button class="close">×</button>' : ''}
  `;
  document.body.prepend(bannerEl);
}
```

### 2.4 Social Media

```
Platforms:
- Twitter/X
- LinkedIn
- Facebook
- Reddit (if community exists)

When to Use:
- SEV0 incidents
- High user visibility
- Proactive communication
- Respond to user complaints

Best Practices:
✓ Acknowledge issue quickly
✓ Link to status page
✓ Update as situation evolves
✓ Thank users for patience
```

**Twitter Example**:
```
🔴 We're aware of an issue preventing access to our service. Our team is investigating and working on a fix. We'll provide updates here and on our status page: https://status.example.com

Updates:
10:45 UTC - Issue identified, implementing fix
11:00 UTC - Service restored, monitoring for stability
11:30 UTC - All systems operational

Thank you for your patience. We're sorry for the disruption.
```

### 2.5 Internal Slack/Teams

```
Channels:
- #incidents (all incidents)
- #inc-YYYY-NNN (specific incident channel)
- #customer-support (support team updates)
- #executive-alerts (SEV0 only)

Purpose:
- Real-time coordination
- Technical discussion
- Status updates
- Action item tracking
```

### 2.6 Direct Outreach (Enterprise Customers)

```
When to Use:
- Enterprise customers affected
- SLA breach
- Revenue-critical customers
- Contractual obligations

Method:
- Dedicated Slack channel
- Direct phone call
- Account manager email
- Executive-to-executive (for major incidents)

Frequency:
- SEV0: Every 15 minutes
- SEV1: Every 30 minutes
- Proactive (don't wait for them to ask)
```

## 3. Communication Timing

### 3.1 Initial Notification

```
Timing by Severity:

SEV0:
- Status page: Within 5 minutes
- Internal Slack: Immediate
- Executive notification: Within 5 minutes
- Enterprise customers: Within 15 minutes

SEV1:
- Status page: Within 15 minutes
- Internal Slack: Within 5 minutes
- Executive notification: Within 30 minutes
- Enterprise customers: Within 30 minutes

SEV2:
- Status page: Optional (if customer-facing)
- Internal Slack: Within 15 minutes
- Executive notification: If prolonged
- Enterprise customers: If affected

SEV3/4:
- No external communication
- Internal ticket only
```

### 3.2 Regular Updates

```
Update Frequency:

SEV0:
- Every 15-30 minutes
- Even if no progress: "Still investigating, next update in 15 min"

SEV1:
- Every 30-60 minutes
- Include progress updates

SEV2:
- Every 1-2 hours
- Or when significant progress

Update Content:
- Current status
- What we've learned
- What we're doing
- Next update time
- ETA (if known)
```

### 3.3 Resolution Notification

```
When to Declare Resolved:

✓ Issue completely fixed
✓ Monitoring shows stable state (15-30 minutes)
✓ Error rates back to normal
✓ No user reports

Don't declare resolved if:
✗ Still monitoring
✗ Intermittent issues
✗ Partial mitigation only
```

**Resolution Message**:
```markdown
## Resolved - API Service Outage

**Status**: Resolved
**Duration**: 47 minutes (10:13 UTC - 11:00 UTC)

The issue has been fully resolved. All services are operating normally.

**Root Cause**: Database connection pool exhaustion due to a bug in recent deployment.

**Resolution**: Rolled back to previous version. Service fully restored at 11:00 UTC.

**Next Steps**: We're conducting a full investigation and will publish a detailed postmortem within 48 hours.

Thank you for your patience.
```

### 3.4 Postmortem Sharing

```
Timeline:
- Internal postmortem: Within 24-48 hours
- Public postmortem: Within 1 week (for major incidents)

Share With:
- Internal: All engineering, product, support
- External: Public blog post (optional)
- Enterprise customers: Direct email with detailed postmortem

Content:
- What happened
- Root cause
- Impact
- Timeline
- What we're doing to prevent recurrence
```

## 4. Message Structure

### The 5 W's Framework

```
What: What is broken?
- Specific, clear description
- Avoid jargon

Who: Who is affected?
- All users, specific region, enterprise customers
- Percentage or number

When: When did it start?
- Timestamp in UTC
- Duration so far

Where: Where is the impact?
- Services affected
- Geographic regions

Why: What are we doing?
- Current actions
- Next steps
- ETA (if known)
```

### Message Template

```markdown
## Incident Update

**What**: API service returning errors
**Who**: All users (~50,000 active users)
**When**: Started 10:13 UTC (32 minutes ago)
**Where**: All regions, all services (web, mobile, API)
**Why**: Database connection issue, team is investigating

**Current Status**: Investigating root cause
**Next Steps**: 
1. Checking database health
2. Reviewing recent deployments
3. Preparing rollback if needed

**ETA**: Unknown at this time
**Next Update**: 11:15 UTC (30 minutes)
```

## 5. Communication Templates by Severity

### SEV0 Template: Complete Outage

```markdown
## INCIDENT: Complete Service Outage

**Status**: Investigating
**Severity**: SEV0
**Started**: 2024-01-15 10:13 UTC
**Impact**: All users unable to access service

We are experiencing a complete service outage. Our entire team is engaged and working on a resolution.

**Affected Services**:
- Web application
- Mobile apps
- Public API

**What We're Doing**:
- Investigating root cause
- All hands on deck
- War room established

**Next Update**: 10:30 UTC (15 minutes)

We sincerely apologize for this disruption and will provide frequent updates.
```

### SEV1 Template: Major Functionality Broken

```markdown
## INCIDENT: Login System Unavailable

**Status**: Investigating
**Severity**: SEV1
**Started**: 2024-01-15 14:00 UTC
**Impact**: Users unable to login (existing sessions unaffected)

We are experiencing issues with our login system. Users who are already logged in can continue using the service, but new logins are currently unavailable.

**Affected**: ~30% of users (those not currently logged in)

**What We're Doing**:
- Investigating authentication service
- Checking recent deployments
- Preparing rollback if needed

**Workaround**: If you're already logged in, you can continue using the service.

**Next Update**: 14:30 UTC (30 minutes)
```

### SEV2 Template: Degraded Performance

```markdown
## INCIDENT: Slow Search Performance

**Status**: Investigating
**Severity**: SEV2
**Started**: 2024-01-15 09:00 UTC
**Impact**: Search feature responding slowly

We are experiencing degraded performance with our search feature. Search results may take 5-10 seconds to load instead of the usual 1 second.

**Affected**: All users (degraded, not broken)

**What We're Doing**:
- Investigating search infrastructure
- Scaling up resources
- Optimizing queries

**Workaround**: Search is still functional, just slower than normal.

**Next Update**: 11:00 UTC (2 hours)
```

## 6. Tone and Language

### Clear and Honest

```
❌ Vague:
"We're experiencing some technical difficulties."

✓ Clear:
"Our API service is returning errors, preventing users from logging in."

❌ Dishonest:
"Everything is fine, just a minor hiccup."

✓ Honest:
"We're experiencing a major outage affecting all users. We're working urgently on a fix."
```

### Avoid Jargon

```
❌ Technical Jargon:
"The PostgreSQL primary instance experienced connection pool exhaustion due to a resource leak in the ORM layer."

✓ Plain Language:
"Our database ran out of available connections, preventing the application from accessing user data."

❌ Acronyms:
"The K8s pod in the us-east-1 AZ is experiencing OOM errors."

✓ Clear:
"Our application servers in the US East region are running out of memory."
```

### Empathy for Affected Users

```
❌ Dismissive:
"We had a small issue. It's fixed now."

✓ Empathetic:
"We know how disruptive this outage was, and we sincerely apologize for the inconvenience."

❌ Blame Users:
"If you had used the workaround we posted, you wouldn't have had issues."

✓ Take Responsibility:
"We should have communicated the workaround more clearly. We're sorry for the confusion."
```

### No Premature Root Cause Claims

```
❌ Premature:
"The issue was caused by AWS."
(Later: Actually it was our code)

✓ Cautious:
"We're investigating the root cause and will share details once confirmed."

❌ Speculative:
"We think it might be a database issue, or maybe network, or possibly..."

✓ Factual:
"We've identified the issue is related to our database layer. Investigation ongoing."
```

## 7. Internal vs External Communication

### Internal Communication (Engineering)

```
Audience: Engineers, technical teams

Style:
✓ Highly technical
✓ Real-time updates
✓ Detailed logs, metrics, traces
✓ Hypotheses and debugging steps
✓ Raw, unfiltered

Channel: Slack incident channel

Example:
"Error rate spiked to 95% at 10:13 UTC. Logs show:
```
[ERROR] Connection pool exhausted (50/50 connections in use)
[ERROR] Timeout waiting for connection
```
Hypothesis: Connection leak in v2.5.0 (deployed at 10:00 UTC)
Action: Rolling back to v2.4.9
ETA: 5 minutes"
```

### External Communication (Customers)

```
Audience: End users, non-technical

Style:
✓ Non-technical language
✓ Clear and concise
✓ Empathetic tone
✓ Focus on impact and resolution
✓ Polished and professional

Channel: Status page, email

Example:
"We're experiencing an issue preventing access to our service. Our team is working on a fix and we expect to have service restored within 15 minutes. We apologize for the disruption."
```

### Translation Example

```
Internal (Technical):
"PostgreSQL connection pool exhausted. Max connections: 50. Current: 50. Long-running queries holding connections. Killing idle connections and restarting app servers."

External (Customer-Facing):
"We're experiencing database connection issues that are preventing access to the service. Our team is actively working on a fix."
```

## 8. Executive Communication (C-Suite Updates)

### Executive Summary Format

```markdown
## Executive Incident Summary

**Incident**: API Service Outage
**Severity**: SEV0
**Status**: Resolved
**Duration**: 47 minutes

### Business Impact
- Users affected: 50,000 (100%)
- Revenue loss: ~$50,000
- SLA breach: Yes (99.9% uptime)
- Customer complaints: 237 support tickets
- Enterprise customers affected: 12

### Root Cause
Database connection pool exhausted due to bug in v2.5.0 deployment.

### Resolution
Rolled back to v2.4.9. Service fully restored at 11:00 UTC.

### Customer Communication
- Status page: Updated every 15 minutes
- Email: Sent to all users
- Enterprise customers: Notified directly
- Social media: Posted updates on Twitter

### Next Steps
1. Postmortem scheduled for tomorrow 10:00 AM
2. Investigating connection leak in v2.5.0
3. Reviewing deployment process
4. Considering SLA credits for enterprise customers

### Recommendations
- Approve SLA credits for affected enterprise customers (~$10k)
- Public postmortem blog post (builds trust)
- Additional investment in testing infrastructure
```

### Executive Update Frequency

```
SEV0:
- Initial: Immediate (within 5 minutes)
- Updates: Every 30 minutes
- Resolution: Immediate
- Postmortem: Within 24 hours

SEV1:
- Initial: Within 30 minutes
- Updates: Every 60 minutes (if prolonged)
- Resolution: When resolved
- Postmortem: Within 48 hours

SEV2:
- Initial: If prolonged (> 4 hours)
- Updates: Daily
- Resolution: When resolved
- Postmortem: Optional
```

## 9. Communication Ownership (IC vs Comms Team)

### Incident Commander (IC) Responsibilities

```
IC Owns:
✓ Technical incident response
✓ Internal technical communication
✓ Initial status page update
✓ Engineering team coordination

IC Does NOT Own:
✗ Customer emails (unless small company)
✗ Social media posts
✗ PR statements
✗ Executive communication (beyond updates)
```

### Communications Team Responsibilities

```
Comms Team Owns:
✓ Customer-facing messaging
✓ Social media posts
✓ Email campaigns
✓ PR statements
✓ Media inquiries
✓ Executive communication drafts

Comms Team Does NOT Own:
✗ Technical details
✗ Root cause analysis
✗ Resolution timeline
```

### Collaboration Model

```
1. IC provides technical updates
   ↓
2. Comms team translates to customer-facing language
   ↓
3. IC reviews for accuracy
   ↓
4. Comms team publishes

Example:
IC: "Connection pool exhausted, rolling back deployment"
Comms: "We're experiencing database issues and are implementing a fix"
IC: ✓ Approved
Comms: Publishes to status page
```

## 10. Status Page Best Practices

### Status Page Structure

```
Components:
- API
- Web Application
- Mobile App
- Database
- Authentication
- Payments

Status Levels:
- Operational (green)
- Degraded Performance (yellow)
- Partial Outage (orange)
- Major Outage (red)
- Under Maintenance (blue)
```

### Update Cadence

```
Initial Update:
- Within 5-15 minutes of incident
- Acknowledge the issue
- State you're investigating

Progress Updates:
- Every 15-30 minutes (SEV0/1)
- Every 1-2 hours (SEV2)
- Include what you've learned
- Provide ETA if known

Resolution Update:
- Mark as resolved
- Explain what happened
- Apologize
- Link to postmortem (when available)
```

### Status Page Examples

**Good Example**:
```markdown
## Investigating - API Service

**Jan 15, 10:15 UTC**
We are investigating reports of errors when accessing our API service. Users may experience failed requests or timeouts. Our team is actively investigating.

**Jan 15, 10:45 UTC**
We have identified the issue as a database connection problem and are implementing a fix. We expect to have service restored within 15 minutes.

**Jan 15, 11:00 UTC**
The issue has been resolved. All services are operating normally. We apologize for the disruption and will publish a detailed postmortem within 48 hours.
```

**Bad Example**:
```markdown
## Issue

**Jan 15, 10:15 UTC**
We're having some problems.

**Jan 15, 11:30 UTC**
It's fixed.
```

## 11. Post-Incident Communication

### Resolution Announcement

```markdown
## Service Restored - API Outage Resolved

**Duration**: 47 minutes (10:13 UTC - 11:00 UTC)
**Impact**: All users

The issue affecting our API service has been fully resolved. All services are now operating normally.

**What Happened**:
A bug in our recent deployment caused our database connection pool to become exhausted, preventing the application from accessing data.

**How We Fixed It**:
We rolled back to the previous version of our application, which immediately resolved the issue.

**What We're Doing Next**:
- Conducting a thorough investigation
- Implementing additional testing to prevent similar issues
- Publishing a detailed postmortem within 48 hours

We sincerely apologize for this disruption and appreciate your patience.
```

### Postmortem Summary (Customer-Facing)

```markdown
## Postmortem: API Service Outage - January 15, 2024

**Summary**:
On January 15, 2024, our API service experienced a complete outage for 47 minutes due to a database connection leak in a recent deployment.

**Impact**:
- Duration: 47 minutes
- Users affected: 50,000 (100%)
- Services affected: Web app, mobile app, API

**What Happened**:
We deployed version 2.5.0 at 10:00 UTC, which included a new feature for order recommendations. This feature had a bug that caused database connections to not be properly released when errors occurred. Over 13 minutes, all 50 available connections were exhausted, causing the service to become unavailable.

**How We Responded**:
- 10:13 UTC: Issue detected via monitoring
- 10:15 UTC: Team began investigation
- 10:30 UTC: Root cause identified
- 10:35 UTC: Decision made to rollback
- 10:40 UTC: Rollback initiated
- 11:00 UTC: Service fully restored

**Root Cause**:
The new code failed to release database connections in error scenarios, leading to connection pool exhaustion.

**What We're Doing to Prevent This**:
1. Added connection pool monitoring and alerting
2. Implemented circuit breakers for downstream services
3. Enhanced load testing to include error scenarios
4. Updated code review checklist to catch resource leaks
5. Implementing canary deployments (5% → 50% → 100%)

**Lessons Learned**:
- Always test error paths, not just happy paths
- Monitor resource usage (connection pools, memory, file handles)
- Gradual rollouts need proper limits to prevent widespread impact

We're committed to learning from this incident and improving our systems. Thank you for your patience and continued trust.

Full technical postmortem: [link]
```

## 12. Communication Antipatterns

### Antipattern 1: Radio Silence

```
❌ Bad:
- Incident starts at 10:00
- No communication until 12:00
- Users panicking on social media

✓ Good:
- Incident starts at 10:00
- Status page updated at 10:05
- Updates every 30 minutes
- Users informed and patient
```

### Antipattern 2: Over-Promising Resolution Time

```
❌ Bad:
"We'll have this fixed in 10 minutes."
(2 hours later, still broken)

✓ Good:
"We're working on a fix. We'll provide an update in 30 minutes."
(Under-promise, over-deliver)
```

### Antipattern 3: Blaming Users

```
❌ Bad:
"The issue only affects users who didn't follow our documentation."

✓ Good:
"We should have made this clearer in our documentation. We're updating it now."
```

### Antipattern 4: Technical Jargon Overload

```
❌ Bad:
"The Kubernetes pod in the us-east-1 AZ experienced OOM errors due to a memory leak in the JVM heap, causing the pod to enter CrashLoopBackOff state."

✓ Good:
"Our application servers ran out of memory and restarted. We're investigating the cause and scaling up resources."
```

### Antipattern 5: Declaring Victory Too Early

```
❌ Bad:
10:30 UTC: "Issue resolved!"
10:45 UTC: "Issue has returned..."

✓ Good:
10:30 UTC: "Fix implemented, monitoring for stability"
11:00 UTC: "Confirmed stable for 30 minutes, marking as resolved"
```

## 13. Real Communication Examples (Good and Bad)

### Good Example: GitLab (2017)

```
GitLab's response to database deletion incident:

✓ Immediate acknowledgement on Twitter
✓ Live-streamed recovery process on YouTube
✓ Transparent about what went wrong
✓ Detailed postmortem published
✓ Honest about backup failures
✓ Community appreciated transparency

Result: Increased trust despite major incident
```

### Bad Example: Equifax (2017)

```
Equifax's response to data breach:

❌ Delayed disclosure (6 weeks)
❌ Vague initial statement
❌ Confusing communication
❌ Executives sold stock before disclosure
❌ Poor customer support

Result: Congressional hearings, massive fines, CEO resigned
```

### Good Example: AWS S3 (2017)

```
AWS's response to S3 outage:

✓ Status page updated quickly
✓ Regular updates every 30 minutes
✓ Detailed postmortem published
✓ Explained root cause clearly
✓ Outlined prevention measures

Result: Industry-standard postmortem, trust maintained
```

## 14. Tools: Statuspage, Incident.io, Slack Workflows

### Statuspage.io

```typescript
// Statuspage API integration
import { StatuspageAPI } from 'statuspage-api';

const statuspage = new StatuspageAPI(process.env.STATUSPAGE_API_KEY);

// Create incident
async function createIncident(incident: Incident) {
  await statuspage.incidents.create({
    name: incident.title,
    status: 'investigating', // investigating, identified, monitoring, resolved
    impact: 'major', // none, minor, major, critical
    body: incident.description,
    components: incident.affectedComponents,
    component_ids: ['api', 'web-app']
  });
}

// Update incident
async function updateIncident(incidentId: string, update: string) {
  await statuspage.incidents.update(incidentId, {
    status: 'identified',
    body: update
  });
}

// Resolve incident
async function resolveIncident(incidentId: string, resolution: string) {
  await statuspage.incidents.update(incidentId, {
    status: 'resolved',
    body: resolution
  });
}
```

### Incident.io

```typescript
// Incident.io API integration
import { IncidentIO } from 'incident-io';

const incidentio = new IncidentIO(process.env.INCIDENT_IO_API_KEY);

// Create incident
const incident = await incidentio.incidents.create({
  title: 'API Service Outage',
  severity: 'sev1',
  status: 'investigating',
  summary: 'API returning 503 errors for all requests'
});

// Post update
await incidentio.incidents.postUpdate(incident.id, {
  message: 'Identified root cause: database connection pool exhausted. Rolling back deployment.',
  status: 'identified'
});

// Resolve
await incidentio.incidents.resolve(incident.id, {
  message: 'Service restored. Monitoring for stability.',
  resolution: 'Rolled back to v2.4.9'
});
```

### Slack Workflows

```typescript
// Automated Slack notifications
async function notifyStakeholders(incident: Incident) {
  // Engineering team
  await slack.postMessage({
    channel: '#incidents',
    text: `🚨 ${incident.severity}: ${incident.title}`,
    blocks: [
      {
        type: 'header',
        text: { type: 'plain_text', text: `${incident.severity}: ${incident.title}` }
      },
      {
        type: 'section',
        fields: [
          { type: 'mrkdwn', text: `*Impact:* ${incident.impact}` },
          { type: 'mrkdwn', text: `*Status:* ${incident.status}` }
        ]
      },
      {
        type: 'actions',
        elements: [
          { type: 'button', text: { type: 'plain_text', text: 'Join War Room' }, url: incident.warRoomUrl },
          { type: 'button', text: { type: 'plain_text', text: 'View Dashboard' }, url: incident.dashboardUrl }
        ]
      }
    ]
  });

  // Executive team (SEV0 only)
  if (incident.severity === 'SEV0') {
    await slack.postMessage({
      channel: '#executive-alerts',
      text: `🚨 SEV0 Incident: ${incident.title}\nImpact: ${incident.impact}\nWar Room: ${incident.warRoomUrl}`
    });
  }

  // Customer support
  await slack.postMessage({
    channel: '#customer-support',
    text: `📢 Customer Impact Alert\n\n*Issue:* ${incident.title}\n*Impact:* ${incident.impact}\n*Status:* ${incident.status}\n\n*What to tell customers:* ${incident.customerMessage}`
  });
}
```

## Summary

Key takeaways for Stakeholder Communication:

1. **Communicate early** - Within 5-15 minutes for SEV0/1
2. **Update frequently** - Every 15-30 minutes, even if no progress
3. **Use appropriate channels** - Status page, email, Slack, social media
4. **Tailor messaging** - Technical for engineers, plain language for customers
5. **Be honest and transparent** - Don't hide or minimize issues
6. **Avoid jargon** - Use clear, simple language
7. **Show empathy** - Acknowledge impact on users
8. **Don't over-promise** - Under-promise, over-deliver on ETAs
9. **Declare resolved carefully** - Only when truly stable
10. **Follow up with postmortem** - Share learnings and prevention measures

## Related Skills

- `41-incident-management/incident-triage` - Initial assessment before communication
- `41-incident-management/severity-levels` - Severity determines communication urgency
- `41-incident-management/escalation-paths` - Who to notify and when
- `40-system-resilience/postmortem-analysis` - Post-incident communication and learning
