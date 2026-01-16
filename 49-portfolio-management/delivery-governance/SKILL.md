---
name: Delivery Governance
description: Comprehensive guide to delivery governance including quality gates, standards, compliance, and balancing governance with agility
---

# Delivery Governance

## What is Delivery Governance?

**Definition:** Standards and processes for shipping software with consistent quality, reduced risk, and compliance.

### Key Components

1. **Standards:** What quality looks like
2. **Processes:** How to achieve quality
3. **Quality Gates:** Checkpoints before shipping
4. **Risk Management:** Identifying and mitigating risks
5. **Compliance:** Meeting regulatory requirements

### Example
```
Before deployment:
✅ Code reviewed (2 approvals)
✅ Tests passing (>80% coverage)
✅ Security scan clean (no high/critical vulnerabilities)
✅ Performance acceptable (<200ms p95 latency)
✅ Documentation updated
→ Approved to deploy
```

---

## Why Governance Matters

### 1. Consistent Quality

**Without Governance:**
```
Team A: 90% test coverage, thorough code reviews
Team B: 20% test coverage, no code reviews
→ Inconsistent quality, Team B ships bugs
```

**With Governance:**
```
All teams: >80% test coverage, 2 code review approvals
→ Consistent quality across teams
```

### 2. Reduce Incidents

**Without Governance:**
```
Deploy without testing → Production outage → Customer impact
```

**With Governance:**
```
Quality gates catch issues before production → Fewer incidents
```

### 3. Meet Compliance Requirements

**Examples:**
- **GDPR:** Data privacy requirements
- **SOC2:** Security controls
- **HIPAA:** Healthcare data protection
- **PCI DSS:** Payment card security

### 4. Stakeholder Confidence

**With Governance:**
- Predictable quality
- Transparent processes
- Audit trail
- Risk mitigation

---

## Types of Governance

### 1. Technical Governance (Architecture, Code Quality)

**What:**
- Architecture standards
- Code quality standards
- Technology choices
- Design patterns

**Example:**
```
Technical Standards:
• Language: TypeScript (not JavaScript)
• Framework: React (not Vue)
• Database: PostgreSQL (not MySQL)
• Code coverage: >80%
• Linting: ESLint (enforced in CI)
```

### 2. Process Governance (Agile Practices, Ceremonies)

**What:**
- Development process
- Agile ceremonies
- Code review process
- Deployment process

**Example:**
```
Process Standards:
• Sprint length: 2 weeks
• Daily standup: 15 minutes
• Code review: 2 approvals required
• Deployment: Staged rollout (canary → full)
```

### 3. Risk Governance (Security, Compliance)

**What:**
- Security standards
- Compliance requirements
- Risk assessment
- Incident management

**Example:**
```
Risk Standards:
• Security scan: Before every deployment
• Penetration testing: Annually
• Data encryption: All PII encrypted at rest
• Incident response: <15 min for SEV0
```

### 4. Portfolio Governance (Prioritization, Budget)

**What:**
- Prioritization framework
- Budget allocation
- Resource planning
- Progress tracking

**Example:**
```
Portfolio Standards:
• Prioritization: RICE framework
• Budget: Quarterly review
• Capacity: 70% feature work, 30% tech debt
• OKRs: Quarterly goals, monthly review
```

---

## Quality Gates

### 1. Code Review (Required Approvals)

**Standard:**
```
• 2 approvals required
• At least 1 from senior engineer
• No self-approval
• All comments resolved
```

**GitHub Branch Protection:**
```yaml
branch_protection:
  required_pull_request_reviews:
    required_approving_review_count: 2
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
  required_status_checks:
    strict: true
    contexts:
      - ci/tests
      - ci/lint
      - ci/security-scan
```

### 2. Automated Tests (% Coverage, Passing)

**Standard:**
```
• Unit tests: >80% coverage
• Integration tests: Critical paths covered
• E2E tests: Happy path + error cases
• All tests passing (0 failures)
```

**CI Check:**
```yaml
# .github/workflows/ci.yml
name: CI

on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: npm test
      - name: Check coverage
        run: |
          coverage=$(npm run coverage:report | grep 'All files' | awk '{print $10}' | sed 's/%//')
          if [ $coverage -lt 80 ]; then
            echo "Coverage $coverage% is below 80%"
            exit 1
          fi
```

### 3. Security Scans (Vulnerabilities)

**Standard:**
```
• No high or critical vulnerabilities
• Medium vulnerabilities: Documented exceptions only
• Dependency scanning: Daily
• Secret scanning: No secrets in code
```

**Tools:**
- **Snyk:** Dependency scanning
- **Dependabot:** Automated dependency updates
- **SonarQube:** SAST (Static Application Security Testing)
- **OWASP ZAP:** DAST (Dynamic Application Security Testing)

**Example (Snyk):**
```yaml
# .github/workflows/security.yml
name: Security Scan

on: [pull_request]

jobs:
  snyk:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Snyk
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
```

### 4. Performance Tests (Load Testing)

**Standard:**
```
• p95 latency: <200ms
• p99 latency: <500ms
• Throughput: >1000 req/s
• Error rate: <0.1%
```

**Load Testing (k6):**
```javascript
// load-test.js
import http from 'k6/http';
import { check } from 'k6';

export let options = {
  stages: [
    { duration: '2m', target: 100 },  // Ramp up to 100 users
    { duration: '5m', target: 100 },  // Stay at 100 users
    { duration: '2m', target: 0 },    // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  let res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
}
```

### 5. Accessibility Checks (WCAG Compliance)

**Standard:**
```
• WCAG 2.1 Level AA compliance
• Keyboard navigation: All features accessible
• Screen reader: All content readable
• Color contrast: 4.5:1 minimum
```

**Tools:**
- **axe DevTools:** Browser extension
- **Lighthouse:** Automated audits
- **Pa11y:** CI integration

**Example (Pa11y):**
```yaml
# .github/workflows/accessibility.yml
name: Accessibility

on: [pull_request]

jobs:
  pa11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Pa11y
        run: |
          npm install -g pa11y-ci
          pa11y-ci --threshold 0
```

---

## Pre-Deployment Checklist

### Comprehensive Checklist

```markdown
# Pre-Deployment Checklist

## Code Quality
- [ ] Code reviewed and approved (2+ approvals)
- [ ] All tests passing (unit, integration, e2e)
- [ ] Test coverage >80%
- [ ] Linting passing (no errors)
- [ ] No code smells (SonarQube)

## Security
- [ ] Security scan clean (no high/critical vulnerabilities)
- [ ] Dependency scan clean (Snyk)
- [ ] No secrets in code (git-secrets)
- [ ] Authentication/authorization tested
- [ ] Input validation implemented

## Performance
- [ ] Load testing completed (p95 <200ms)
- [ ] Database queries optimized (no N+1)
- [ ] Caching implemented (where applicable)
- [ ] Bundle size acceptable (<500KB)

## Accessibility
- [ ] WCAG 2.1 AA compliance (Pa11y)
- [ ] Keyboard navigation tested
- [ ] Screen reader tested
- [ ] Color contrast verified

## Documentation
- [ ] README updated
- [ ] API documentation updated (OpenAPI)
- [ ] Changelog updated
- [ ] Runbook created (for ops)

## Deployment
- [ ] Rollback plan defined
- [ ] Feature flags configured
- [ ] Monitoring configured (metrics, logs, alerts)
- [ ] Stakeholders notified (email, Slack)

## Post-Deployment
- [ ] Smoke tests passing
- [ ] Monitoring dashboard reviewed
- [ ] No alerts firing
- [ ] User feedback monitored
```

---

## Architecture Governance

### 1. Architecture Decision Records (ADRs)

**What:** Document significant architecture decisions

**Template:**
```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted

## Context
We need a relational database for our application. Options considered:
- PostgreSQL
- MySQL
- MongoDB

## Decision
We will use PostgreSQL as our primary database.

## Consequences
**Positive:**
- Strong ACID compliance
- Advanced features (JSONB, full-text search)
- Excellent performance
- Active community

**Negative:**
- Steeper learning curve than MySQL
- Fewer managed hosting options than MySQL

## Alternatives Considered
- **MySQL:** Simpler but fewer features
- **MongoDB:** NoSQL, but we need relational data
```

### 2. Design Review Process

**When Required:**
- New services
- Major refactoring
- Technology changes
- Architecture changes

**Process:**
```
1. Create design doc (RFC)
2. Share with team (Slack, email)
3. Review meeting (1 hour)
4. Incorporate feedback
5. Get approval from tech lead
6. Implement
```

**Design Doc Template:**
```markdown
# Design Doc: [Feature Name]

## Overview
[Brief description]

## Goals
- [Goal 1]
- [Goal 2]

## Non-Goals
- [What we're NOT doing]

## Design
### Architecture Diagram
[Diagram]

### Components
[Description of components]

### Data Model
[Database schema]

### API
[API endpoints]

## Alternatives Considered
[Other approaches and why not chosen]

## Risks
[Potential risks and mitigations]

## Timeline
[Estimated timeline]

## Open Questions
[Unresolved questions]
```

### 3. Technology Standards (Approved Languages, Frameworks)

**Approved Technologies:**
```markdown
# Technology Standards

## Languages
- **Backend:** TypeScript, Python, Go
- **Frontend:** TypeScript (React)
- **Mobile:** Swift (iOS), Kotlin (Android)
- **Infrastructure:** Terraform, Bash

## Frameworks
- **Backend:** Express.js, FastAPI, Gin
- **Frontend:** React, Next.js
- **Testing:** Jest, Pytest, Cypress

## Databases
- **Primary:** PostgreSQL
- **Cache:** Redis
- **Search:** Elasticsearch

## Infrastructure
- **Cloud:** AWS
- **Container:** Docker, Kubernetes
- **CI/CD:** GitHub Actions

## Exceptions
New technologies require approval from Architecture Review Board.
Submit RFC with justification.
```

### 4. Architecture Review Board (For Major Decisions)

**When to Escalate:**
- New technology adoption
- Major architecture changes
- Cross-team impact
- High risk decisions

**Board Members:**
- CTO
- VP Engineering
- Principal Engineers
- Tech Leads

**Meeting:**
- Frequency: Monthly
- Duration: 2 hours
- Agenda: Review RFCs

---

## Code Quality Standards

### 1. Linting (ESLint, Pylint)

**ESLint Config:**
```javascript
// .eslintrc.js
module.exports = {
  extends: ['eslint:recommended', 'plugin:@typescript-eslint/recommended'],
  rules: {
    'no-console': 'error',
    'no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'error',
    'max-lines-per-function': ['error', 50],
    'complexity': ['error', 10],
  },
};
```

**CI Enforcement:**
```yaml
# .github/workflows/lint.yml
name: Lint

on: [pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run ESLint
        run: npm run lint
```

### 2. Formatting (Prettier, Black)

**Prettier Config:**
```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

**Pre-commit Hook:**
```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{js,ts,tsx}": ["prettier --write", "eslint --fix"]
  }
}
```

### 3. Test Coverage (>80%)

**Jest Config:**
```javascript
// jest.config.js
module.exports = {
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};
```

### 4. Code Complexity (Cyclomatic Complexity <10)

**What:** Number of independent paths through code

**Example (Bad - Complexity 11):**
```javascript
function processOrder(order) {
  if (order.status === 'pending') {
    if (order.paymentMethod === 'card') {
      if (order.amount > 100) {
        if (order.customer.verified) {
          if (order.items.length > 0) {
            if (order.shippingAddress) {
              if (order.billingAddress) {
                if (order.discount) {
                  if (order.coupon) {
                    if (order.giftWrap) {
                      if (order.express) {
                        // Process order
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
// Complexity: 11 (too high!)
```

**Example (Good - Complexity 3):**
```javascript
function processOrder(order) {
  validateOrder(order);
  processPayment(order);
  shipOrder(order);
}

function validateOrder(order) {
  if (order.status !== 'pending') throw new Error('Invalid status');
  if (!order.customer.verified) throw new Error('Customer not verified');
  if (order.items.length === 0) throw new Error('No items');
}
// Complexity: 3 (good!)
```

### 5. SonarQube/CodeClimate Checks

**SonarQube Quality Gate:**
```yaml
# sonar-project.properties
sonar.projectKey=my-project
sonar.sources=src
sonar.tests=tests

# Quality gate
sonar.qualitygate.wait=true
sonar.coverage.exclusions=**/*.test.ts
sonar.cpd.exclusions=**/*.test.ts

# Thresholds
sonar.coverage.minimum=80
sonar.duplicated_lines_density.maximum=3
sonar.cognitive_complexity.maximum=15
```

---

## Security Governance

### 1. Dependency Scanning (Snyk, Dependabot)

**Dependabot Config:**
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
    open-pull-requests-limit: 10
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "security"
```

### 2. SAST (Static Application Security Testing)

**Tools:**
- **SonarQube:** Code quality + security
- **Semgrep:** Pattern-based scanning
- **CodeQL:** Semantic code analysis

**Example (CodeQL):**
```yaml
# .github/workflows/codeql.yml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: github/codeql-action/init@v2
        with:
          languages: javascript, typescript
      - uses: github/codeql-action/analyze@v2
```

### 3. DAST (Dynamic Application Security Testing)

**Tools:**
- **OWASP ZAP:** Web app scanner
- **Burp Suite:** Security testing
- **Nessus:** Vulnerability scanner

**Example (OWASP ZAP):**
```yaml
# .github/workflows/dast.yml
name: DAST

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2am

jobs:
  zap_scan:
    runs-on: ubuntu-latest
    steps:
      - name: ZAP Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a'
```

### 4. Secret Scanning (No API Keys in Code)

**Tools:**
- **git-secrets:** Pre-commit hook
- **TruffleHog:** Scan git history
- **GitHub Secret Scanning:** Built-in

**Example (git-secrets):**
```bash
# Install git-secrets
git secrets --install

# Add patterns
git secrets --add 'API_KEY.*=.*'
git secrets --add 'SECRET.*=.*'
git secrets --add 'PASSWORD.*=.*'

# Scan
git secrets --scan
```

### 5. Penetration Testing (Annually)

**Process:**
```
1. Hire external security firm
2. Define scope (what to test)
3. Conduct test (1-2 weeks)
4. Review findings
5. Prioritize fixes (by severity)
6. Fix vulnerabilities
7. Re-test (verify fixes)
8. Document results
```

---

## Compliance Governance

### 1. GDPR/CCPA Requirements

**Requirements:**
- **Right to access:** Users can request their data
- **Right to deletion:** Users can delete their data
- **Right to portability:** Users can export their data
- **Consent:** Explicit consent for data collection
- **Data minimization:** Only collect necessary data

**Implementation:**
```javascript
// User data export
app.get('/api/users/:id/export', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  const data = {
    profile: user,
    orders: await db.orders.findByUserId(user.id),
    activity: await db.activity.findByUserId(user.id),
  };
  res.json(data);
});

// User data deletion
app.delete('/api/users/:id', async (req, res) => {
  await db.users.delete(req.params.id);
  await db.orders.deleteByUserId(req.params.id);
  await db.activity.deleteByUserId(req.params.id);
  res.status(204).send();
});
```

### 2. SOC2 Controls

**Control Categories:**
- **Security:** Access controls, encryption
- **Availability:** Uptime, disaster recovery
- **Processing Integrity:** Data accuracy
- **Confidentiality:** Data protection
- **Privacy:** PII handling

**Example Controls:**
```markdown
# SOC2 Controls

## CC6.1: Logical Access Controls
- Multi-factor authentication required
- Role-based access control (RBAC)
- Access reviews quarterly

## CC7.2: System Monitoring
- Centralized logging (ELK)
- Real-time alerting (PagerDuty)
- Security event monitoring (SIEM)

## CC8.1: Change Management
- Code review required (2 approvals)
- Automated testing (CI/CD)
- Staged rollouts (canary)
```

### 3. HIPAA (If Healthcare)

**Requirements:**
- **Encryption:** All PHI encrypted at rest and in transit
- **Access controls:** Role-based access to PHI
- **Audit logs:** All PHI access logged
- **Business Associate Agreements:** With vendors

### 4. Industry-Specific Regulations

**Examples:**
- **PCI DSS:** Payment card data
- **FERPA:** Student data
- **GLBA:** Financial data
- **COPPA:** Children's data

---

## Release Governance

### 1. Change Management Process

**Process:**
```
1. Create change request (Jira ticket)
2. Fill out change details:
   - What's changing?
   - Why?
   - Risk level (low, medium, high)
   - Rollback plan
3. Get approvals:
   - Tech lead (all changes)
   - Product manager (feature changes)
   - Security team (security-related)
4. Schedule deployment
5. Deploy
6. Verify deployment
7. Close change request
```

**Change Request Template:**
```markdown
# Change Request: [Title]

## Summary
[Brief description of change]

## Risk Level
- [ ] Low (bug fix, minor change)
- [ ] Medium (new feature, refactoring)
- [ ] High (breaking change, infrastructure)

## Details
**What:** [What's changing?]
**Why:** [Why is this needed?]
**Impact:** [Who/what is affected?]

## Rollback Plan
[How to rollback if something goes wrong]

## Testing
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Manual testing completed

## Approvals
- [ ] Tech Lead
- [ ] Product Manager (if feature change)
- [ ] Security Team (if security-related)

## Deployment
**Date:** [YYYY-MM-DD]
**Time:** [HH:MM timezone]
**Window:** [Duration]
```

### 2. Deployment Windows (Avoid Friday Deploys)

**Deployment Schedule:**
```
✅ Monday-Thursday: 9am-5pm (business hours)
⚠️ Friday: Emergency only
❌ Weekend: No deployments
❌ Holidays: No deployments
```

**Why:**
- Avoid Friday deploys (no one wants to debug on weekend)
- Deploy during business hours (team available if issues)
- Avoid holidays (reduced staff)

### 3. Staged Rollouts (Canary, Blue-Green)

**Canary Deployment:**
```
1. Deploy to 5% of traffic
2. Monitor for 30 minutes
3. If healthy, deploy to 25%
4. Monitor for 30 minutes
5. If healthy, deploy to 50%
6. Monitor for 30 minutes
7. If healthy, deploy to 100%

If any stage fails: Rollback immediately
```

**Blue-Green Deployment:**
```
Blue (current): 100% traffic
Green (new): 0% traffic

1. Deploy to Green
2. Test Green (smoke tests)
3. Switch traffic: Blue 0%, Green 100%
4. Monitor Green
5. If healthy: Keep Green, decommission Blue
6. If issues: Switch back to Blue
```

### 4. Post-Deployment Monitoring

**Monitoring Checklist:**
```markdown
# Post-Deployment Monitoring (First 24 Hours)

## Immediate (0-15 min)
- [ ] Smoke tests passing
- [ ] No alerts firing
- [ ] Error rate normal (<0.1%)
- [ ] Latency normal (p95 <200ms)

## Short-term (15 min - 1 hour)
- [ ] Traffic patterns normal
- [ ] Database performance normal
- [ ] Cache hit rate normal
- [ ] No user complaints

## Medium-term (1-4 hours)
- [ ] Business metrics normal (signups, conversions)
- [ ] No increase in support tickets
- [ ] Monitoring dashboards reviewed

## Long-term (4-24 hours)
- [ ] Daily metrics reviewed
- [ ] Stakeholders notified (success)
- [ ] Post-deployment review scheduled
```

---

## Incident Management Governance

### 1. Severity Definitions

**Severity Levels:**
```markdown
# Incident Severity

## SEV0 (Critical)
**Impact:** Complete outage, all users affected
**Examples:** Site down, database unavailable, data breach
**Response:** Immediate (page on-call)
**Communication:** Every 30 min (status page, Slack, email)
**Postmortem:** Required

## SEV1 (High)
**Impact:** Major functionality broken, many users affected
**Examples:** Payment processing down, login broken
**Response:** <15 minutes
**Communication:** Every hour
**Postmortem:** Required

## SEV2 (Medium)
**Impact:** Minor functionality broken, some users affected
**Examples:** Feature not working, performance degradation
**Response:** <1 hour
**Communication:** Daily
**Postmortem:** Optional

## SEV3 (Low)
**Impact:** Cosmetic issue, few users affected
**Examples:** UI bug, typo
**Response:** <1 day
**Communication:** As needed
**Postmortem:** Not required
```

### 2. Escalation Procedures

**Escalation Path:**
```
Level 1: On-call engineer (respond <15 min)
    ↓ (if not resolved in 30 min)
Level 2: Engineering manager (respond <30 min)
    ↓ (if not resolved in 1 hour)
Level 3: VP Engineering (respond <1 hour)
    ↓ (if not resolved in 2 hours)
Level 4: CTO (respond <2 hours)
```

### 3. Postmortem Requirements (SEV0/1)

**Postmortem Template:**
```markdown
# Postmortem: [Incident Title]

## Summary
[Brief description of incident]

## Impact
- **Duration:** [Start time] - [End time] ([Duration])
- **Users affected:** [Number or percentage]
- **Revenue impact:** [$Amount]
- **Severity:** SEV0/SEV1

## Timeline
- **[Time]:** [Event]
- **[Time]:** [Event]
- **[Time]:** [Event]

## Root Cause
[What caused the incident?]

## Resolution
[How was it resolved?]

## What Went Well
- [Thing 1]
- [Thing 2]

## What Went Wrong
- [Thing 1]
- [Thing 2]

## Action Items
- [ ] [Action 1] (Owner: [Name], Due: [Date])
- [ ] [Action 2] (Owner: [Name], Due: [Date])

## Lessons Learned
[What did we learn?]
```

### 4. Communication Protocols

**Communication Channels:**
```
Internal:
• Slack: #incidents (real-time updates)
• Email: engineering@example.com (summary)
• PagerDuty: On-call rotation

External:
• Status page: status.example.com
• Twitter: @examplestatus
• Email: customers (for SEV0/1)
```

**Communication Template:**
```markdown
# Incident Update

**Status:** Investigating / Identified / Monitoring / Resolved
**Severity:** SEV0 / SEV1 / SEV2
**Impact:** [Description]
**Started:** [Time]
**Last Update:** [Time]

## Current Status
[What's happening now?]

## Next Steps
[What are we doing?]

## Next Update
[When will we update again?]
```

---

## Portfolio Governance

### 1. Prioritization Framework (RICE, Value/Effort)

**See Roadmap Planning skill for details**

### 2. Budget Allocation

**Budget Categories:**
```
Total Engineering Budget: $10M/year

Allocation:
• Feature development: 50% ($5M)
• Technical debt: 20% ($2M)
• Platform/infrastructure: 15% ($1.5M)
• Security/compliance: 10% ($1M)
• Innovation/R&D: 5% ($0.5M)
```

### 3. Resource Planning

**Capacity Allocation:**
```
Total Capacity: 100 engineers

Allocation:
• Product teams: 70 engineers (feature development)
• Platform team: 15 engineers (shared services)
• SRE team: 10 engineers (operations)
• Security team: 5 engineers (security)
```

### 4. Progress Tracking (OKRs, KPIs)

**OKRs (Quarterly):**
```
Objective: Improve product reliability

Key Results:
• KR1: Reduce MTTR from 2h to 30min
• KR2: Increase uptime from 99.5% to 99.9%
• KR3: Reduce SEV0/1 incidents from 10 to 2 per quarter
```

**KPIs (Monthly):**
```
Delivery KPIs:
• Deployment frequency: 50 deploys/week
• Lead time: 2 days (commit to production)
• Change failure rate: <5%
• MTTR: <30 minutes

Quality KPIs:
• Test coverage: >80%
• Code review time: <4 hours
• Bug escape rate: <2%
• Customer satisfaction: NPS >50
```

---

## Governance Tools

### 1. Jira (Workflow Enforcement)

**Workflow:**
```
To Do → In Progress → Code Review → Testing → Done

Transitions:
• To Do → In Progress: Assign to self
• In Progress → Code Review: Create PR, link PR
• Code Review → Testing: 2 approvals, all checks passing
• Testing → Done: QA approval, deployed to production
```

**Required Fields:**
```
• Title
• Description
• Acceptance criteria
• Story points
• Priority
• Labels (feature, bug, tech-debt)
```

### 2. GitHub (Branch Protection, Required Reviews)

**Branch Protection Rules:**
```yaml
main:
  required_pull_request_reviews:
    required_approving_review_count: 2
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
  required_status_checks:
    strict: true
    contexts:
      - ci/tests
      - ci/lint
      - ci/security-scan
      - ci/coverage
  enforce_admins: true
  restrictions:
    users: []
    teams: ["engineering"]
```

### 3. SonarQube (Code Quality Gates)

**Quality Gate:**
```yaml
# Quality Gate: Default

Conditions:
• Coverage: >80%
• Duplicated Lines: <3%
• Maintainability Rating: A
• Reliability Rating: A
• Security Rating: A
• Security Hotspots Reviewed: 100%
• New Code Coverage: >80%
```

### 4. ServiceNow (Change Management)

**Change Request Workflow:**
```
1. Create change request
2. Fill out details (risk, impact, rollback)
3. Get approvals (tech lead, manager)
4. Schedule deployment
5. Deploy
6. Verify
7. Close change request
```

---

## Balancing Governance and Agility

### 1. Lightweight Processes

**Principle:** Governance should enable, not block

**Example:**
```
❌ Heavy: 10-page change request form
✅ Light: 1-page template with key info

❌ Heavy: 5 approval layers
✅ Light: 2 approvals (tech lead + peer)

❌ Heavy: Manual quality checks
✅ Light: Automated quality gates (CI/CD)
```

### 2. Automate Checks (CI/CD)

**Automate Everything:**
```
Manual (slow):
• Code review → Manual
• Testing → Manual
• Security scan → Manual
• Deployment → Manual

Automated (fast):
• Code review → Required (enforced by GitHub)
• Testing → Automated (CI)
• Security scan → Automated (CI)
• Deployment → Automated (CD)
```

### 3. Risk-Based (Higher Governance for Critical Systems)

**Governance Levels:**
```
Low Risk (Internal tools):
• 1 code review approval
• Basic tests
• Deploy anytime

Medium Risk (Customer-facing features):
• 2 code review approvals
• Comprehensive tests
• Staged rollout

High Risk (Payment, auth, data):
• 2+ code review approvals (including security)
• Extensive tests + security scan
• Staged rollout + manual verification
```

### 4. Continuous Improvement (Retrospectives)

**Retrospective Questions:**
```
1. What governance helped us?
2. What governance slowed us down?
3. What governance is missing?
4. What can we automate?
5. What can we simplify?
```

**Example Improvements:**
```
Problem: Code reviews taking 2 days
Solution: Set SLA (4 hours), add review rotation

Problem: Security scans blocking PRs
Solution: Run scans async, only block on high/critical

Problem: Too many manual deployment steps
Solution: Automate deployment, add rollback button
```

---

## Governance Anti-Patterns

### 1. Too Much Bureaucracy (Slows Down Delivery)

**Problem:**
```
10-page change request form
5 approval layers
Manual quality checks
Deployment takes 2 weeks
```

**Solution:** Lightweight processes, automation

### 2. Too Little Governance (Quality Issues, Incidents)

**Problem:**
```
No code reviews
No tests
No security scans
Frequent production incidents
```

**Solution:** Implement quality gates, automate checks

### 3. Manual Gates (Automate Instead)

**Problem:**
```
Manual code review checklist
Manual security review
Manual deployment approval
```

**Solution:** Automate with CI/CD, branch protection, quality gates

### 4. Governance as Blocker (Should Be Enabler)

**Problem:**
```
Governance team says "no" to everything
Slows down innovation
Teams work around governance
```

**Solution:** Governance team helps teams meet standards, provides tools and automation

---

## Metrics to Track

### DORA Metrics

**1. Deployment Frequency**
```
Target: >1 deploy/day
Measure: Number of deploys per day/week
```

**2. Lead Time for Changes**
```
Target: <1 day (commit to production)
Measure: Time from commit to production
```

**3. Change Failure Rate**
```
Target: <5%
Measure: % of deploys that cause incidents
```

**4. Time to Restore Service (MTTR)**
```
Target: <1 hour
Measure: Time from incident start to resolution
```

### Quality Metrics

**5. Test Coverage**
```
Target: >80%
Measure: % of code covered by tests
```

**6. Code Review Time**
```
Target: <4 hours
Measure: Time from PR creation to approval
```

**7. Bug Escape Rate**
```
Target: <2%
Measure: % of bugs found in production (not caught in testing)
```

**8. Security Vulnerabilities**
```
Target: 0 high/critical
Measure: Number of high/critical vulnerabilities
```

---

## Real Governance Frameworks

### 1. COBIT (Control Objectives for Information and Related Technologies)

**Focus:** IT governance and management

**Domains:**
- Align, Plan, and Organize
- Build, Acquire, and Implement
- Deliver, Service, and Support
- Monitor, Evaluate, and Assess

### 2. ITIL (Information Technology Infrastructure Library)

**Focus:** IT service management

**Processes:**
- Service Strategy
- Service Design
- Service Transition
- Service Operation
- Continual Service Improvement

### 3. SAFe (Scaled Agile Framework)

**Focus:** Scaling agile to large organizations

**Levels:**
- Team (Scrum/Kanban)
- Program (Agile Release Train)
- Large Solution
- Portfolio

### 4. Custom Lightweight Governance

**Example:**
```
Our Governance Framework:

1. Quality Gates (automated)
   • Code review (2 approvals)
   • Tests (>80% coverage)
   • Security scan (no high/critical)

2. Risk-Based Approvals
   • Low risk: Tech lead approval
   • Medium risk: Tech lead + manager
   • High risk: Tech lead + manager + security

3. Continuous Improvement
   • Monthly retrospectives
   • Quarterly governance review
   • Automate manual processes
```

---

## Templates

### Template 1: Pre-Deployment Checklist

See "Pre-Deployment Checklist" section above

### Template 2: ADR Template

See "Architecture Decision Records" section above

### Template 3: Change Request Form

See "Change Management Process" section above

---

## Summary

### Quick Reference

**Governance Types:**
- Technical: Architecture, code quality
- Process: Agile practices, ceremonies
- Risk: Security, compliance
- Portfolio: Prioritization, budget

**Quality Gates:**
- Code review (2 approvals)
- Tests (>80% coverage, all passing)
- Security scan (no high/critical)
- Performance (p95 <200ms)
- Accessibility (WCAG 2.1 AA)

**Security:**
- Dependency scanning (Snyk, Dependabot)
- SAST (SonarQube, CodeQL)
- DAST (OWASP ZAP)
- Secret scanning (git-secrets)
- Penetration testing (annually)

**Compliance:**
- GDPR/CCPA (data privacy)
- SOC2 (security controls)
- HIPAA (healthcare)
- Industry-specific

**Release:**
- Change management (approval process)
- Deployment windows (Mon-Thu, 9am-5pm)
- Staged rollouts (canary, blue-green)
- Post-deployment monitoring

**Incident Management:**
- Severity definitions (SEV0-3)
- Escalation procedures
- Postmortems (SEV0/1)
- Communication protocols

**Balancing:**
- Lightweight processes
- Automate checks (CI/CD)
- Risk-based (higher governance for critical)
- Continuous improvement (retrospectives)

**Metrics (DORA):**
- Deployment frequency (>1/day)
- Lead time (<1 day)
- Change failure rate (<5%)
- MTTR (<1 hour)

**Tools:**
- Jira (workflow enforcement)
- GitHub (branch protection)
- SonarQube (quality gates)
- ServiceNow (change management)
