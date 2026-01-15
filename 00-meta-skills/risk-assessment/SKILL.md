# Risk Assessment

## Overview

Risk assessment identifies, evaluates, and mitigates potential technical risks in software projects. This guide covers identification techniques, assessment frameworks, and mitigation strategies.

## Risk Management Fundamentals for Engineers

### Risk Definition

```
Risk = Likelihood × Impact

Where:
- Likelihood: Probability of occurrence (Low, Medium, High)
- Impact: Severity of consequences (Minor, Major, Critical)
```

### Risk Management Process

```
1. Identify → 2. Assess → 3. Mitigate → 4. Monitor → 5. Review
     ↑                                                      │
     └──────────────────────────────────────────────────────┘
                    (Continuous Loop)
```

## Risk Identification Techniques

### 1. Pre-mortem Analysis

**Process:** Imagine the project has failed. Work backwards to identify what went wrong.

```
Exercise: "It's 6 months from now. The project failed catastrophically."

Team brainstorms:
- "We underestimated the database migration complexity"
- "Third-party API we depend on shut down"
- "Key developer left the team"
- "Security breach exposed user data"
- "Performance issues made the app unusable"

Result: List of potential failure modes to address proactively
```

**Template:**
```markdown
# Pre-mortem: [Project Name]

## Scenario
It's [date]. The project has failed.

## Failure Modes

### Technical Failures
1. Database migration failed, lost data
2. Third-party API deprecated
3. Performance issues under load
4. Security vulnerability exploited

### Process Failures
1. Scope creep delayed launch by 6 months
2. Key dependencies not identified early
3. Testing was inadequate

### People Failures
1. Lead developer left mid-project
2. Team lacked expertise in new technology
3. Communication breakdown between teams

## Preventive Actions
[For each failure mode, list preventive measures]
```

### 2. FMEA (Failure Mode and Effects Analysis)

```
Component → Failure Mode → Effect → Severity → Likelihood → Detection → RPN
```

**Example:**

| Component | Failure Mode | Effect | Severity (1-10) | Likelihood (1-10) | Detection (1-10) | RPN |
|-----------|-------------|--------|-----------------|-------------------|------------------|-----|
| Database | Connection pool exhausted | API requests fail | 9 | 6 | 3 | 162 |
| Cache | Redis unavailable | Slow responses | 6 | 4 | 2 | 48 |
| Payment API | Third-party downtime | Can't process orders | 10 | 3 | 1 | 30 |

**RPN (Risk Priority Number) = Severity × Likelihood × Detection**

Higher RPN = Higher priority to address

### 3. Threat Modeling

**STRIDE Framework:**

```
S - Spoofing (authentication)
T - Tampering (integrity)
R - Repudiation (non-repudiation)
I - Information Disclosure (confidentiality)
D - Denial of Service (availability)
E - Elevation of Privilege (authorization)
```

**Example:**
```markdown
# Threat Model: User Authentication System

## Assets
- User credentials
- Session tokens
- Personal data

## Threats

### Spoofing
- Attacker impersonates legitimate user
- Mitigation: MFA, strong password policy

### Tampering
- Attacker modifies authentication token
- Mitigation: Sign tokens with secret key

### Information Disclosure
- Credentials leaked in logs
- Mitigation: Never log passwords, encrypt sensitive data

### Denial of Service
- Brute force attacks overwhelm system
- Mitigation: Rate limiting, account lockout

### Elevation of Privilege
- User gains admin access
- Mitigation: Principle of least privilege, RBAC
```

### 4. Dependency Analysis

```python
# Identify dependency risks
def analyze_dependencies(project):
    risks = []
    
    for dependency in project.dependencies:
        # Check for outdated versions
        if dependency.is_outdated():
            risks.append({
                'type': 'Outdated Dependency',
                'name': dependency.name,
                'current': dependency.version,
                'latest': dependency.latest_version,
                'severity': 'Medium'
            })
        
        # Check for known vulnerabilities
        if dependency.has_vulnerabilities():
            risks.append({
                'type': 'Security Vulnerability',
                'name': dependency.name,
                'cve': dependency.vulnerabilities,
                'severity': 'High'
            })
        
        # Check for unmaintained packages
        if dependency.last_update > 365:  # days
            risks.append({
                'type': 'Unmaintained Package',
                'name': dependency.name,
                'last_update': dependency.last_update,
                'severity': 'Medium'
            })
        
        # Check for single point of failure
        if dependency.is_critical() and not dependency.has_alternative():
            risks.append({
                'type': 'Single Point of Failure',
                'name': dependency.name,
                'severity': 'High'
            })
    
    return risks
```

## Risk Assessment Dimensions

### Risk Matrix

```
                    IMPACT
                    
        │ Minor │ Major │ Critical │
────────┼───────┼───────┼──────────┤
High    │   M   │   H   │    C     │
────────┼───────┼───────┼──────────┤
Medium  │   L   │   M   │    H     │
────────┼───────┼───────┼──────────┤
Low     │   L   │   L   │    M     │
────────┴───────┴───────┴──────────┘
        
L = Low Risk (Monitor)
M = Medium Risk (Mitigate)
H = High Risk (Urgent Action)
C = Critical Risk (Immediate Action)
```

### Likelihood Scale

```
Low (1-3):
- Rare occurrence
- < 10% probability
- Example: Meteor destroys data center

Medium (4-6):
- Occasional occurrence
- 10-50% probability
- Example: Third-party API has outage

High (7-10):
- Frequent occurrence
- > 50% probability
- Example: Database connection pool exhausted under peak load
```

### Impact Scale

```
Minor (1-3):
- Minimal business impact
- Quick recovery
- Example: Non-critical feature unavailable for 5 minutes

Major (4-7):
- Significant business impact
- Hours to recover
- Example: Payment processing down for 1 hour

Critical (8-10):
- Severe business impact
- Days to recover or permanent damage
- Example: Data breach exposing customer PII
```

## Common Technical Risks

### 1. Scalability Risks

```markdown
Risk: System can't handle expected load

Indicators:
- No load testing performed
- Single server architecture
- Synchronous processing of heavy tasks
- No caching layer
- Database not optimized

Likelihood: High (if not addressed)
Impact: Critical (system unusable)

Mitigation:
- Perform load testing
- Implement horizontal scaling
- Add caching (Redis)
- Optimize database queries
- Use async processing for heavy tasks
```

### 2. Security Vulnerabilities

```markdown
Risk: Security breach exposing sensitive data

Indicators:
- No security audit performed
- Outdated dependencies with known CVEs
- No input validation
- Passwords stored in plain text
- No rate limiting

Likelihood: Medium
Impact: Critical

Mitigation:
- Regular security audits
- Dependency scanning (Snyk, Dependabot)
- Input validation and sanitization
- Encrypt sensitive data
- Implement rate limiting
- Use security headers
```

### 3. Dependency Risks

```markdown
Risk: Critical dependency becomes unavailable

Indicators:
- Reliance on single third-party API
- No fallback mechanism
- Unmaintained open-source library
- Vendor lock-in

Likelihood: Medium
Impact: Major

Mitigation:
- Identify critical dependencies
- Implement circuit breakers
- Have fallback options
- Monitor dependency health
- Consider alternatives
```

### 4. Data Loss Risks

```markdown
Risk: Data loss due to failure or error

Indicators:
- No backup strategy
- No disaster recovery plan
- Single database instance
- No replication
- Untested restore procedures

Likelihood: Low
Impact: Critical

Mitigation:
- Automated daily backups
- Test restore procedures monthly
- Database replication
- Point-in-time recovery
- Offsite backup storage
```

### 5. Performance Degradation

```markdown
Risk: System becomes slow over time

Indicators:
- No performance monitoring
- Unbounded data growth
- No query optimization
- Memory leaks
- No caching strategy

Likelihood: High
Impact: Major

Mitigation:
- Implement APM (Application Performance Monitoring)
- Database query optimization
- Data archival strategy
- Memory profiling
- Caching layer
```

## Risk Mitigation Strategies

### 1. Avoid

```
Eliminate the risk entirely

Example:
Risk: Third-party payment API might go down
Avoidance: Don't use third-party API, build in-house

When to use: Risk too high, alternative exists
```

### 2. Transfer

```
Shift risk to another party

Example:
Risk: Infrastructure failure
Transfer: Use cloud provider (AWS, Azure)
- They handle hardware failures
- SLA guarantees uptime

When to use: Others can manage risk better
```

### 3. Mitigate

```
Reduce likelihood or impact

Example:
Risk: Database failure causes downtime
Mitigation:
- Database replication (reduces likelihood of total failure)
- Automated failover (reduces impact)
- Regular backups (reduces impact)

When to use: Can't avoid, but can reduce
```

### 4. Accept

```
Acknowledge risk, do nothing

Example:
Risk: Rare edge case causes minor bug
Acceptance: Impact is minimal, fix if it occurs

When to use: Low likelihood × low impact
```

### Mitigation Patterns

#### Circuit Breaker

```python
# Prevent cascading failures
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
def call_external_api():
    """
    If 5 failures occur, circuit opens
    Requests fail fast for 60 seconds
    Then tries again
    """
    response = requests.get('https://api.example.com/data')
    return response.json()
```

#### Fallback

```python
# Graceful degradation
def get_user_recommendations(user_id):
    try:
        # Try ML-based recommendations
        return ml_service.get_recommendations(user_id)
    except Exception:
        # Fallback to simple recommendations
        return get_popular_items()
```

#### Retry with Exponential Backoff

```python
# Handle transient failures
import time

def retry_with_backoff(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            
            wait_time = 2 ** attempt  # 1s, 2s, 4s
            time.sleep(wait_time)
```

## Risk Register Creation and Maintenance

### Risk Register Template

```markdown
# Risk Register: [Project Name]

## Risk Summary
- Total Risks: 15
- Critical: 2
- High: 5
- Medium: 6
- Low: 2

---

## RISK-001: Database Migration Failure

**Category:** Technical
**Identified:** 2024-01-15
**Owner:** Database Team

### Description
Migration from MySQL to PostgreSQL might fail or cause data loss

### Likelihood:** Medium (5/10)
**Impact:** Critical (9/10)
**Risk Score:** 45 (High)

### Indicators
- Complex schema with 200+ tables
- 500GB of data to migrate
- Limited testing environment
- Tight deadline

### Consequences
- Data loss or corruption
- Extended downtime (days)
- Customer impact
- Regulatory issues

### Mitigation Plan
1. Create full backup before migration
2. Test migration on staging environment
3. Perform migration in stages
4. Have rollback plan ready
5. Schedule during low-traffic period

### Contingency Plan
If migration fails:
1. Rollback to MySQL
2. Investigate issues
3. Fix and retry

### Status:** Active
**Review Date:** 2024-02-01

---

## RISK-002: Third-Party API Dependency

**Category:** External Dependency
**Identified:** 2024-01-10
**Owner:** Backend Team

### Description
Payment processing API (Stripe) might experience outages

**Likelihood:** Medium (4/10)
**Impact:** Critical (10/10)
**Risk Score:** 40 (High)

### Mitigation Plan
1. Implement circuit breaker
2. Queue failed payments for retry
3. Monitor API health
4. Have backup payment provider ready

### Status:** Mitigated
**Review Date:** Monthly

---

[Continue for all risks...]
```

### Risk Tracking Spreadsheet

```
| ID | Risk | Likelihood | Impact | Score | Status | Owner | Due Date |
|----|------|------------|--------|-------|--------|-------|----------|
| 1  | DB Migration | 5 | 9 | 45 | Active | DB Team | 2024-02-01 |
| 2  | API Dependency | 4 | 10 | 40 | Mitigated | Backend | Ongoing |
| 3  | Scalability | 7 | 8 | 56 | Active | DevOps | 2024-01-30 |
```

## Continuous Risk Monitoring

```python
# Automated risk monitoring
class RiskMonitor:
    def __init__(self):
        self.risks = []
        self.alerts = []
    
    def monitor_dependencies(self):
        """Check for vulnerable dependencies"""
        vulnerabilities = scan_dependencies()
        
        for vuln in vulnerabilities:
            if vuln.severity == 'critical':
                self.alert(f"Critical vulnerability: {vuln.package}")
    
    def monitor_performance(self):
        """Check for performance degradation"""
        response_time = get_avg_response_time()
        
        if response_time > 1000:  # ms
            self.alert(f"Response time degraded: {response_time}ms")
    
    def monitor_error_rates(self):
        """Check for increased errors"""
        error_rate = get_error_rate()
        
        if error_rate > 0.01:  # 1%
            self.alert(f"Error rate elevated: {error_rate:.2%}")
    
    def monitor_capacity(self):
        """Check for capacity issues"""
        cpu_usage = get_cpu_usage()
        memory_usage = get_memory_usage()
        
        if cpu_usage > 80:
            self.alert(f"High CPU usage: {cpu_usage}%")
        
        if memory_usage > 85:
            self.alert(f"High memory usage: {memory_usage}%")
    
    def alert(self, message):
        """Send alert to team"""
        send_slack_message(f"⚠️ Risk Alert: {message}")
        self.alerts.append({
            'message': message,
            'timestamp': datetime.now()
        })
```

## Communicating Risks to Stakeholders

### Risk Report Template

```markdown
# Risk Report: Q1 2024

## Executive Summary
- 15 risks identified
- 2 critical risks require immediate attention
- 5 high risks being actively mitigated
- Overall risk level: MEDIUM

## Top 3 Risks

### 1. Database Migration (CRITICAL)
**What:** Migrating to new database might fail
**Impact:** Days of downtime, potential data loss
**Mitigation:** Extensive testing, staged rollout, rollback plan
**Status:** 60% complete, on track

### 2. Third-Party API Dependency (HIGH)
**What:** Payment API might go down
**Impact:** Can't process payments
**Mitigation:** Circuit breaker, fallback provider
**Status:** Mitigated

### 3. Scalability (HIGH)
**What:** System might not handle Black Friday traffic
**Impact:** Site slowdown or crash
**Mitigation:** Load testing, auto-scaling, caching
**Status:** In progress

## Risk Trend
- Q4 2023: 12 risks (3 critical)
- Q1 2024: 15 risks (2 critical)
- Trend: Improving (fewer critical risks)

## Recommendations
1. Allocate additional resources to database migration
2. Complete load testing by end of month
3. Schedule disaster recovery drill
```

## Risk-based Testing Strategies

### Test Prioritization by Risk

```
High Risk Areas → More Testing

Example:
- Payment processing: 95% code coverage, extensive integration tests
- User profile: 80% code coverage, standard tests
- Admin dashboard: 60% code coverage, basic tests
```

### Risk-based Test Plan

```markdown
# Test Plan: E-commerce Platform

## High Risk Features (Extensive Testing)

### Payment Processing
- Unit tests: 95% coverage
- Integration tests: All payment flows
- End-to-end tests: Complete checkout
- Security tests: PCI compliance
- Load tests: 10K concurrent transactions
- Chaos tests: Simulate API failures

### Inventory Management
- Unit tests: 90% coverage
- Integration tests: Stock updates
- Concurrency tests: Race conditions
- Data integrity tests: No overselling

## Medium Risk Features (Standard Testing)

### User Authentication
- Unit tests: 85% coverage
- Integration tests: Login/logout flows
- Security tests: Common vulnerabilities

## Low Risk Features (Basic Testing)

### Static Content Pages
- Unit tests: 60% coverage
- Smoke tests: Pages load correctly
```

## "Fear-Driven Development"

### What to Worry About

```
✅ Worry about:
- Data loss
- Security breaches
- Scalability limits
- Single points of failure
- Dependency failures
- Performance degradation

❌ Don't worry about:
- Perfect code
- Theoretical edge cases
- Premature optimization
- Technology hype
```

### Healthy Paranoia

```python
# Good paranoia: Defensive programming
def process_payment(amount, user_id):
    # Validate inputs
    if amount <= 0:
        raise ValueError("Amount must be positive")
    
    if not user_exists(user_id):
        raise ValueError("Invalid user")
    
    # Check for duplicate transactions
    if is_duplicate_transaction(amount, user_id):
        raise DuplicateTransactionError()
    
    # Use transaction for atomicity
    with db.transaction():
        deduct_balance(user_id, amount)
        record_transaction(user_id, amount)
        send_confirmation(user_id)
```

## Risk vs Uncertainty

```
Risk: Known unknowns
- We know what might go wrong
- We can estimate probability
- We can plan mitigation

Uncertainty: Unknown unknowns
- We don't know what we don't know
- Can't estimate probability
- Can't plan specific mitigation

Strategy for Uncertainty:
- Build flexibility
- Maintain options
- Iterate quickly
- Learn fast
```

## Tools and Templates

### Risk Assessment Template

```markdown
# Risk Assessment: [Feature/Project Name]

## Risk Identification

### Technical Risks
1. [Risk description]
2. [Risk description]

### External Risks
1. [Risk description]

### People Risks
1. [Risk description]

## Risk Analysis

| Risk | Likelihood | Impact | Score | Priority |
|------|------------|--------|-------|----------|
| [Risk 1] | H | C | 90 | Critical |
| [Risk 2] | M | M | 25 | Medium |

## Mitigation Plans

### Risk 1: [Name]
- **Mitigation:** [Actions]
- **Contingency:** [Backup plan]
- **Owner:** [Person]
- **Due:** [Date]

## Monitoring Plan
- [What to monitor]
- [How often]
- [Alert thresholds]
```

## Real-world Case Studies

### Case Study 1: AWS S3 Outage (2017)

**Risk:** Human error in operations
**What happened:** Engineer typo removed too many servers
**Impact:** S3 unavailable for hours, many sites down
**Lesson:** Add safeguards to destructive operations

**Mitigation:**
- Require confirmation for destructive commands
- Implement blast radius limits
- Test disaster recovery regularly

### Case Study 2: GitLab Database Incident (2017)

**Risk:** Data loss during operations
**What happened:** Accidentally deleted production database
**Impact:** 6 hours of data lost
**Lesson:** Backups must be tested

**Mitigation:**
- Test restore procedures regularly
- Multiple backup methods
- Delayed replication for protection against mistakes

### Case Study 3: Equifax Breach (2017)

**Risk:** Unpatched vulnerabilities
**What happened:** Known vulnerability not patched
**Impact:** 147 million records exposed
**Lesson:** Dependency management is critical

**Mitigation:**
- Automated vulnerability scanning
- Patch management process
- Regular security audits

## Best Practices

1. **Identify Early** - Start risk assessment at project kickoff
2. **Be Specific** - Vague risks are useless
3. **Quantify** - Use likelihood × impact
4. **Prioritize** - Focus on high-impact risks
5. **Mitigate Proactively** - Don't wait for risks to materialize
6. **Monitor Continuously** - Risks change over time
7. **Communicate Clearly** - Use stakeholder language
8. **Document** - Maintain risk register
9. **Review Regularly** - Monthly or quarterly
10. **Learn** - Post-mortems when risks materialize

## Resources

- [OWASP Risk Rating Methodology](https://owasp.org/www-community/OWASP_Risk_Rating_Methodology)
- [NIST Risk Management Framework](https://csrc.nist.gov/projects/risk-management)
- [Threat Modeling: Designing for Security](https://www.wiley.com/en-us/Threat+Modeling%3A+Designing+for+Security-p-9781118809990)
- [Risk Management in Software Engineering](https://www.sei.cmu.edu/our-work/risk-management/)
