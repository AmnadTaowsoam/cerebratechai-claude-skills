# Risk and Dependencies

## Overview

Risks are potential problems that may occur. Dependencies are external factors or systems we rely on. Identifying and managing both early is critical for project success.

## Definitions

| Term | Definition |
|------|------------|
| **Risk** | A potential problem that may occur, with associated probability and impact |
| **Dependency** | Reliance on an external factor (person, system, vendor, data) that must be available for project success |

## Why Identify Early

| Benefit | Description |
|---------|-------------|
| **Plan mitigation strategies** - Have plans ready before problems occur |
| **Avoid surprises** - No unexpected issues mid-project |
| **Set realistic timelines** - Account for potential delays |
| **Communicate to stakeholders** - Set proper expectations |
| **Allocate resources** - Prepare contingency budgets and time |
| **Reduce project failure** - Proactive risk management improves success rates |

---

## Types of Risks

### 1. Technical Risk

Can we build it? Will the technology work?

```
Technical Risks:

- New technology unfamiliar to team
  - Probability: Medium
  - Impact: High
  - Example: Using GraphQL for the first time

- Complex integration with multiple systems
  - Probability: High
  - Impact: High
  - Example: Integrating with 5 legacy systems

- Performance at scale
  - Probability: Medium
  - Impact: Critical
  - Example: Can system handle 100K concurrent users?

- Data migration complexity
  - Probability: High
  - Impact: High
  - Example: Migrating 10M records from legacy system

- Third-party API limitations
  - Probability: Medium
  - Impact: Medium
  - Example: API doesn't support required feature

- Security vulnerabilities
  - Probability: Medium
  - Impact: Critical
  - Example: Uncovered security flaw in implementation
```

### 2. Schedule Risk

Will we finish on time?

```
Schedule Risks:

- Underestimated effort
  - Probability: High
  - Impact: High
  - Example: Task takes 2x longer than estimated

- Scope creep
  - Probability: High
  - Impact: High
  - Example: Stakeholders keep adding features

- Dependencies delayed
  - Probability: Medium
  - Impact: High
  - Example: Design team delivers late

- Team availability issues
  - Probability: Medium
  - Impact: Medium
  - Example: Team member gets sick or leaves

- Unexpected technical challenges
  - Probability: Medium
  - Impact: High
  - Example: Unforeseen technical roadblocks

- Testing takes longer than expected
  - Probability: Medium
  - Impact: Medium
  - Example: More bugs found than anticipated
```

### 3. Resource Risk

Do we have the people and skills?

```
Resource Risks:

- Insufficient team size
  - Probability: Medium
  - Impact: High
  - Example: Need 3 developers, only have 2

- Missing skills
  - Probability: Medium
  - Impact: High
  - Example: No one knows Kubernetes

- Team turnover
  - Probability: Low
  - Impact: High
  - Example: Key developer leaves mid-project

- Overcommitted team
  - Probability: High
  - Impact: Medium
  - Example: Team working on multiple projects

- Budget cuts
  - Probability: Low
  - Impact: Critical
  - Example: Budget reduced mid-project

- Tool/license limitations
  - Probability: Low
  - Impact: Medium
  - Example: License expires or limits reached
```

### 4. Integration Risk

Will systems connect properly?

```
Integration Risks:

- API incompatibility
  - Probability: Medium
  - Impact: High
  - Example: Third-party API doesn't match documentation

- Data format mismatches
  - Probability: High
  - Impact: Medium
  - Example: Date formats differ between systems

- Authentication/authorization issues
  - Probability: Medium
  - Impact: High
  - Example: OAuth tokens not accepted

- Performance degradation
  - Probability: Medium
  - Impact: Medium
  - Example: Integration slows down system

- Version conflicts
  - Probability: Low
  - Impact: Medium
  - Example: Dependency version incompatible

- Network/firewall issues
  - Probability: Medium
  - Impact: Medium
  - Example: Ports blocked, connection refused
```

### 5. Third-Party Risk

Will vendors deliver?

```
Third-Party Risks:

- Vendor delays
  - Probability: Medium
  - Impact: High
  - Example: Design agency delivers late

- Vendor quality issues
  - Probability: Medium
  - Impact: High
  - Example: Deliverables don't meet requirements

- Vendor goes out of business
  - Probability: Low
  - Impact: Critical
  - Example: Critical vendor shuts down

- API changes without notice
  - Probability: Medium
  - Impact: High
  - Example: Third-party API breaks

- Pricing changes
  - Probability: Low
  - Impact: Medium
  - Example: Vendor increases prices

- Support unavailability
  - Probability: Medium
  - Impact: Medium
  - Example: Can't get help when needed
```

### 6. Compliance Risk

Will we meet regulations?

```
Compliance Risks:

- Regulatory changes
  - Probability: Low
  - Impact: Critical
  - Example: New GDPR requirements

- Non-compliance discovered
  - Probability: Low
  - Impact: Critical
  - Example: Audit finds violations

- Data breach
  - Probability: Low
  - Impact: Critical
  - Example: User data exposed

- Certification delays
  - Probability: Medium
  - Impact: High
  - Example: Security audit takes longer

- Legal challenges
  - Probability: Low
  - Impact: Critical
  - Example: Lawsuit over IP or compliance
```

---

## Risk Identification Techniques

### 1. Brainstorming

Team discussion to identify potential risks.

```
Brainstorming Session:

Participants: All team members, stakeholders
Duration: 1-2 hours
Format: Free-form idea generation

Process:
1. Set the stage: "Let's think about what could go wrong"
2. Generate ideas: No judgment, all ideas welcome
3. Cluster similar ideas: Group related risks
4. Prioritize: Vote on most important risks
5. Document: Create initial risk register

Example Output:
- "What if the API changes?"
- "What if a developer leaves?"
- "What if we can't scale?"
- "What if the design is delayed?"
```

### 2. Pre-Mortem

Imagine the project has failed and work backwards.

```
Pre-Mortem Exercise:

Question: "It's 6 months from now and the project has failed. Why?"

Process:
1. Imagine failure scenario
2. List reasons for failure
3. Convert to risks
4. Develop mitigations

Example Reasons for Failure:
- "We couldn't integrate with the legacy system"
- "The team didn't have the right skills"
- "We ran out of budget"
- "The stakeholders kept changing requirements"
- "The technology didn't perform at scale"

Converted to Risks:
- Risk: Integration with legacy system fails
- Risk: Team lacks necessary skills
- Risk: Budget overrun
- Risk: Scope creep
- Risk: Performance issues at scale
```

### 3. Checklist

Use a standard checklist of common risks.

```
Risk Checklist:

Technical:
[ ] New technology
[ ] Complex integration
[ ] Performance at scale
[ ] Data migration
[ ] Third-party API limitations
[ ] Security vulnerabilities

Schedule:
[ ] Underestimated effort
[ ] Scope creep
[ ] Dependencies delayed
[ ] Team availability
[ ] Unexpected challenges
[ ] Testing delays

Resource:
[ ] Insufficient team size
[ ] Missing skills
[ ] Team turnover
[ ] Overcommitted team
[ ] Budget cuts
[ ] Tool limitations

Integration:
[ ] API incompatibility
[ ] Data format mismatches
[ ] Authentication issues
[ ] Performance degradation
[ ] Version conflicts
[ ] Network/firewall issues

Third-Party:
[ ] Vendor delays
[ ] Vendor quality issues
[ ] Vendor bankruptcy
[ ] API changes
[ ] Pricing changes
[ ] Support issues

Compliance:
[ ] Regulatory changes
[ ] Non-compliance
[ ] Data breach
[ ] Certification delays
[ ] Legal challenges
```

### 4. Past Projects

Learn from what went wrong before.

```
Past Project Analysis:

Review previous projects and identify:
1. What risks occurred?
2. What was the impact?
3. How were they handled?
4. What could have been done better?

Example:
Previous Project: E-commerce Platform
Risks that occurred:
- Integration with payment gateway took 3x longer
- Design team delivered 2 weeks late
- Performance issues at launch
- Scope creep added 20% more work

Lessons learned:
- Always test integrations early
- Build buffer for design delivery
- Load test before launch
- Implement strict change control

Apply to current project:
- Risk: Payment integration may take longer than expected
- Risk: Design delivery may be delayed
- Risk: Performance issues at scale
- Risk: Scope creep
```

---

## Risk Assessment

Evaluate risks based on probability and impact.

### Probability Levels

| Level | Description | Percentage |
|-------|-------------|------------|
| **Low** | Unlikely to occur | < 30% |
| **Medium** | May occur | 30-70% |
| **High** | Likely to occur | > 70% |

### Impact Levels

| Level | Description | Example |
|-------|-------------|---------|
| **Low** | Minor impact, easy to recover | Small delay, minor cost increase |
| **Medium** | Significant impact, recoverable | 2-week delay, 20% budget increase |
| **High** | Major impact, difficult to recover | 1-month delay, 50% budget increase |
| **Critical** | Project failure possible | Project cancelled, major cost overrun |

### Risk Level Calculation

```
Risk Level = Probability × Impact

Risk Matrix:
             Low Impact | Medium Impact | High Impact | Critical Impact
Low Prob:    Low Risk   |    Low Risk   |  Medium Risk |   High Risk
Med Prob:    Low Risk   |  Medium Risk  |   High Risk  | Critical Risk
High Prob:  Medium Risk |   High Risk   | Critical Risk| Critical Risk
```

### Risk Matrix Visualization

```
                    Impact
                  Low  Med  High  Crit
           Low    G     G     Y      R
Prob:      Med    G     Y     R      R
           High   Y     R     R      R

Legend:
G = Green (Low Risk) - Monitor
Y = Yellow (Medium Risk) - Plan mitigation
R = Red (High/Critical Risk) - Immediate action
```

---

## Risk Register

Maintain a comprehensive list of all identified risks.

### Risk Register Template

```
Risk Register: [Project Name]

| ID | Risk | Category | Probability | Impact | Risk Level | Mitigation | Owner | Status | Last Updated |
|----|------|----------|-------------|--------|------------|------------|-------|--------|--------------|
| R1 | [Risk description] | [Type] | [L/M/H] | [L/M/H/C] | [Level] | [Mitigation] | [Name] | [Status] | [Date] |
| R2 | [Risk description] | [Type] | [L/M/H] | [L/M/H/C] | [Level] | [Mitigation] | [Name] | [Status] | [Date] |
```

### Example Risk Register

```
Risk Register: E-Commerce Platform

| ID | Risk | Category | Prob | Impact | Level | Mitigation | Owner | Status |
|----|------|----------|------|--------|-------|------------|-------|--------|
| R1 | Integration with Stripe API fails | Technical | M | H | High | Build abstraction layer, test early | Dev | Open |
| R2 | Design team delivers late | Schedule | M | H | High | Build buffer, use wireframes if needed | PM | Open |
| R3 | Performance issues at scale | Technical | M | C | Critical | Load testing early, optimize queries | Dev | Open |
| R4 | Scope creep | Schedule | H | H | Critical | Strict change control, document scope | PM | Open |
| R5 | Team member leaves | Resource | L | H | Medium | Knowledge sharing, documentation | Tech Lead | Open |
```

---

## Common Technical Risks

### Risk 1: New Technology

```
Risk: Team unfamiliar with new technology

Probability: Medium
Impact: High

Symptoms:
- Learning curve delays development
- Unexpected technical challenges
- Poor implementation due to inexperience

Mitigation:
- Allocate time for training and learning
- Build proof of concept before full implementation
- Consider bringing in expert consultant
- Have fallback technology option

Owner: Tech Lead
Status: Open
```

### Risk 2: Complex Integration

```
Risk: Integration with multiple systems is complex

Probability: High
Impact: High

Symptoms:
- API incompatibilities
- Data format mismatches
- Authentication/authorization issues

Mitigation:
- Test integrations early
- Build abstraction layers
- Document integration points thoroughly
- Have contingency for each integration

Owner: Backend Lead
Status: Open
```

### Risk 3: Performance at Scale

```
Risk: System doesn't perform at expected scale

Probability: Medium
Impact: Critical

Symptoms:
- Slow response times
- Database timeouts
- System crashes under load

Mitigation:
- Load test early and often
- Optimize database queries
- Implement caching strategies
- Design for horizontal scalability

Owner: DevOps Engineer
Status: Open
```

### Risk 4: Data Migration

```
Risk: Data migration from legacy system fails

Probability: High
Impact: High

Symptoms:
- Data loss or corruption
- Incomplete migration
- Data format issues

Mitigation:
- Backup all data before migration
- Test migration with sample data
- Have rollback plan
- Validate migrated data thoroughly

Owner: Data Engineer
Status: Open
```

### Risk 5: Third-Party API Limitations

```
Risk: Third-party API doesn't support required features

Probability: Medium
Impact: Medium

Symptoms:
- Feature cannot be implemented
- Workarounds required
- Additional development time

Mitigation:
- Verify API capabilities before committing
- Build abstraction layer for flexibility
- Have alternative vendors ready
- Consider building feature in-house

Owner: Backend Lead
Status: Open
```

---

## Mitigation Strategies

Four main approaches to managing risks.

### 1. Avoid

Eliminate the risk by changing the plan.

```
Example:
Risk: Integration with legacy system is too complex

Avoidance:
- Don't integrate with legacy system
- Build new system from scratch
- Or use different approach that doesn't require integration

When to use:
- Risk is high probability and high impact
- Alternative approaches exist
- Cost of avoidance is acceptable
```

### 2. Reduce

Take actions to lower probability or impact.

```
Example:
Risk: Team unfamiliar with new technology

Reduction:
- Allocate 2 weeks for training
- Build proof of concept
- Hire consultant for critical parts
- Pair programming with experienced developer

When to use:
- Risk cannot be avoided
- Can take actions to reduce likelihood or impact
- Cost of reduction is acceptable
```

### 3. Transfer

Shift risk to another party.

```
Example:
Risk: Security vulnerabilities in implementation

Transfer:
- Use managed service (e.g., AWS Cognito for auth)
- Purchase cyber insurance
- Hire security firm for audit
- Use vendor with SLA guarantees

When to use:
- Third party can handle risk better
- Cost of transfer is acceptable
- Risk is significant but specialized
```

### 4. Accept

Acknowledge risk and monitor.

```
Example:
Risk: Minor performance degradation at peak load

Acceptance:
- Document risk
- Monitor performance metrics
- Have plan if degradation exceeds threshold
- Accept minor impact as acceptable trade-off

When to use:
- Risk probability is low
- Impact is manageable
- Cost of mitigation exceeds impact
- Risk is inherent to project
```

---

## Example Risk Mitigations

### Example 1: Technical Risk

```
Risk: Team unfamiliar with GraphQL

Probability: Medium
Impact: High

Mitigation Strategy: Reduce

Actions:
1. Allocate 1 week for GraphQL training
2. Build proof of concept before full implementation
3. Use GraphQL playground for testing
4. Consider bringing in GraphQL consultant for review

Timeline: Week 1-2
Owner: Tech Lead
Cost: $2,000 (training + consultant)
```

### Example 2: Third-Party Risk

```
Risk: Third-party API may change without notice

Probability: Medium
Impact: High

Mitigation Strategy: Reduce

Actions:
1. Build abstraction layer around API
2. Version the integration
3. Subscribe to API changelog
4. Implement integration tests
5. Have fallback plan (alternative vendor)

Timeline: Week 3-4
Owner: Backend Lead
Cost: $0 (development effort)
```

### Example 3: Schedule Risk

```
Risk: Design team may deliver assets late

Probability: Medium
Impact: High

Mitigation Strategy: Reduce + Accept

Actions:
1. Build 2-week buffer into timeline
2. Use wireframes if design delayed
3. Regular check-ins with design team
4. Have backup designer available

Timeline: Throughout project
Owner: Project Manager
Cost: $0 (buffer time)
```

### Example 4: Resource Risk

```
Risk: Key developer may leave mid-project

Probability: Low
Impact: High

Mitigation Strategy: Reduce + Transfer

Actions:
1. Knowledge sharing sessions
2. Comprehensive documentation
3. Code reviews by multiple developers
4. Pair programming
5. Have backup developer familiar with code

Timeline: Throughout project
Owner: Tech Lead
Cost: $0 (process overhead)
```

---

## Types of Dependencies

### 1. Internal Dependencies

Other teams or internal systems.

```
Internal Dependencies:

- Other Teams:
  - Design team: Must provide UI assets by Week 2
  - QA team: Must allocate time for testing
  - DevOps team: Must set up infrastructure

- Internal Systems:
  - Authentication service: Must be deployed
  - User database: Must be accessible
  - Analytics platform: Must be configured
```

### 2. External Dependencies

Vendors, partners, clients.

```
External Dependencies:

- Vendors:
  - Design agency: Must deliver mockups
  - Security consultant: Must complete audit
  - Hosting provider: Must provision servers

- Partners:
  - Payment gateway: Must provide API access
  - Email service: Must configure account
  - Analytics provider: Must set up tracking

- Clients:
  - Must provide requirements
  - Must approve designs
  - Must provide test data
```

### 3. Technical Dependencies

Libraries, frameworks, platforms.

```
Technical Dependencies:

- Libraries:
  - React 18: Must be available
  - Node.js 18: Must be installed
  - PostgreSQL 14: Must be running

- Frameworks:
  - Next.js: Must be compatible
  - Fastify: Must support required features
  - Jest: Must work with codebase

- Platforms:
  - AWS: Must have account configured
  - GitHub: Must have repository set up
  - Vercel: Must have deployment configured
```

### 4. Data Dependencies

Existing databases, data sources.

```
Data Dependencies:

- Databases:
  - User database: Must be migrated
  - Product database: Must be accessible
  - Analytics database: Must be configured

- Data Sources:
  - Legacy system: Must export data
  - Third-party API: Must provide data
  - CSV files: Must be provided by client

- Data Quality:
  - Data must be clean and accurate
  - Data must be complete
  - Data must be in correct format
```

---

## Dependency Mapping

Visualize and track all dependencies.

### Dependency Map Template

```
Dependency Map: [Project Name]

Critical Path:
[Dependency 1] → [Dependency 2] → [Dependency 3] → [Dependency 4]

All Dependencies:

| Dependency | Type | Owner | Status | Critical | Due Date | Contingency |
|------------|------|-------|--------|----------|----------|-------------|
| [Dep 1] | Internal | [Name] | On Track | Yes | [Date] | [Plan] |
| [Dep 2] | External | [Name] | At Risk | Yes | [Date] | [Plan] |
| [Dep 3] | Technical | [Name] | Complete | No | [Date] | N/A |
```

### Example Dependency Map

```
Dependency Map: E-Commerce Platform

Critical Path:
Design Assets → Frontend Development → Backend API → Integration Testing → Launch

All Dependencies:

| Dependency | Type | Owner | Status | Critical | Due Date | Contingency |
|------------|------|-------|--------|----------|----------|-------------|
| UI Mockups | External | Design Agency | On Track | Yes | Week 2 | Use wireframes |
| Auth Service | Internal | Auth Team | At Risk | Yes | Week 3 | Build basic auth |
| Stripe API | External | Stripe | Complete | Yes | Week 1 | PayPal fallback |
| Product Data | Data | Client | Delayed | Yes | Week 4 | Manual entry |
| Hosting Setup | Technical | DevOps | On Track | No | Week 2 | Manual setup |
```

---

## Dependency Risks

What happens when dependencies fail?

### Risk 1: Dependency Delayed

```
Risk: Dependency is delayed

Impact:
- Our project is delayed
- Timeline must be adjusted
- Resources may be idle

Mitigation:
- Build buffer into timeline
- Have contingency plan
- Communicate early about delays
- Adjust critical path if possible

Example:
Design assets delayed by 1 week
→ Frontend development delayed by 1 week
→ Launch delayed by 1 week
→ OR: Use wireframes, start development with placeholders
```

### Risk 2: Dependency Changes

```
Risk: Dependency changes unexpectedly

Impact:
- Integration breaks
- Additional work required
- Timeline affected

Mitigation:
- Build abstraction layers
- Version dependencies
- Subscribe to changelogs
- Have alternative options

Example:
Stripe API changes authentication method
→ Integration breaks
→ Need to update code
→ Timeline delayed by 3 days
→ OR: Used abstraction layer, only change one file
```

### Risk 3: Dependency Fails

```
Risk: Dependency fails completely

Impact:
- Feature cannot be delivered
- Project may fail
- Significant rework required

Mitigation:
- Have backup options
- Build in-house if needed
- Use multiple providers
- Plan for failure scenarios

Example:
Payment gateway goes out of business
→ Cannot process payments
→ Project cannot launch
→ OR: Have backup payment provider ready
```

---

## Managing Dependencies

Proactive management reduces dependency risks.

### Clear Agreements

```
Dependency Agreement Template:

Dependency: [Description]
Owner: [Name/Team]
Deliverable: [What is being delivered]
Due Date: [Date]
Quality Criteria: [What defines "done"]
Communication Plan: [How and when to communicate]

Example:
Dependency: UI Mockups
Owner: Design Agency
Deliverable: Figma files for all pages
Due Date: Week 2 (Friday)
Quality Criteria: All screens designed, responsive, approved by PO
Communication Plan: Weekly check-ins, daily Slack updates
```

### Regular Check-ins

```
Check-in Schedule:

Daily:
- Quick status update
- Any blockers?
- On track for due date?

Weekly:
- Detailed progress review
- Risk assessment
- Timeline adjustment if needed

Milestone:
- Formal review of deliverable
- Sign-off if complete
- Plan for next milestone
```

### Contingency Plans

```
Contingency Planning:

For each dependency:
1. What if it's delayed?
2. What if it's not delivered?
3. What if quality is poor?
4. What's the backup plan?

Example:
Dependency: Design Assets
Contingency:
- If delayed by 1 week: Use wireframes, start development
- If delayed by 2 weeks: Hire backup designer
- If not delivered: Use internal designer, adjust timeline
- If quality is poor: Request revisions, allocate time for fixes
```

### Reduce Dependencies

```
Dependency Reduction Strategies:

1. Decouple where possible
   - Use APIs instead of direct database access
   - Build abstraction layers
   - Use message queues for async communication

2. Own critical components
   - Build in-house instead of relying on vendor
   - Control your own destiny for critical path

3. Multiple options
   - Have backup vendors
   - Use multiple providers for redundancy

4. Simplify
   - Reduce number of integrations
   - Use standard protocols
   - Minimize custom work
```

---

## Red Flags

Watch for these warning signs.

### Risk Red Flags

| Red Flag | Why It's a Problem | Action |
|----------|-------------------|--------|
| Many high-probability, high-impact risks | Project likely to fail | Reassess project feasibility |
| No mitigation plans | Unprepared for problems | Develop mitigation strategies |
| Risks not being monitored | Problems will surprise you | Implement regular risk reviews |
| Stakeholders unaware of risks | Expectations misaligned | Communicate risks clearly |
| Risk register outdated | Not managing risks actively | Update regularly |

### Dependency Red Flags

| Red Flag | Why It's a Problem | Action |
|----------|-------------------|--------|
| Critical dependencies on unreliable sources | High risk of delay | Find alternatives |
| No contingency plans | No backup if dependency fails | Develop contingencies |
| Dependencies not tracked | Surprises when they fail | Create dependency map |
| Single point of failure | Project stops if dependency fails | Add redundancy |
| No communication with dependency owners | Don't know status | Regular check-ins |

---

## Communicating Risks

Tailor communication to audience.

### To Stakeholders (High-Level)

```
Top 5 Risks:

1. Integration with legacy system (High)
   - May delay project by 2 weeks
   - Mitigation: Testing early, buffer in timeline

2. Performance at scale (Critical)
   - System may not handle expected load
   - Mitigation: Load testing, optimization

3. Scope creep (High)
   - Requirements keep changing
   - Mitigation: Strict change control

4. Design team delivery (Medium)
   - May be delayed by 1 week
   - Mitigation: Wireframes as backup

5. Team availability (Medium)
   - Resource constraints
   - Mitigation: Prioritize work, consider additional resources
```

### To Team (Detailed)

```
Full Risk Register:

[Complete risk register with all risks, mitigations, owners, status]

Focus:
- All risks documented
- Mitigation plans clear
- Owners assigned
- Status tracked
```

### Regular Updates

```
Risk Status Updates:

Weekly:
- New risks identified
- Existing risks updated
- Mitigation progress
- Risk status changes

Monthly:
- Full risk review
- Risk level reassessment
- Mitigation effectiveness
- Lessons learned
```

---

## Risk and Dependency Document Structure

```markdown
# Risk and Dependencies: [Project Name]

**Version:** 1.0
**Date:** [Date]
**Author:** [Name]

## Risks

### Risk Register

| ID | Risk | Category | Prob | Impact | Level | Mitigation | Owner | Status |
|----|------|----------|------|--------|-------|------------|-------|--------|
| R1 | [Risk] | [Type] | [L/M/H] | [L/M/H/C] | [Level] | [Mitigation] | [Name] | [Status] |
| R2 | [Risk] | [Type] | [L/M/H] | [L/M/H/C] | [Level] | [Mitigation] | [Name] | [Status] |

### High Priority Risks

**Risk 1: [Risk Name]**
- Description: [Details]
- Probability: [L/M/H]
- Impact: [L/M/H/C]
- Level: [Level]
- Mitigation: [Plan]
- Owner: [Name]
- Status: [Status]

**Risk 2: [Risk Name]**
- Description: [Details]
- Probability: [L/M/H]
- Impact: [L/M/H/C]
- Level: [Level]
- Mitigation: [Plan]
- Owner: [Name]
- Status: [Status]

## Dependencies

### Dependency Map

Critical Path:
[Dep 1] → [Dep 2] → [Dep 3] → [Dep 4]

### Dependency Register

| Dependency | Type | Owner | Status | Critical | Due Date | Contingency |
|------------|------|-------|--------|----------|----------|-------------|
| [Dep 1] | [Type] | [Name] | [Status] | Yes/No | [Date] | [Plan] |
| [Dep 2] | [Type] | [Name] | [Status] | Yes/No | [Date] | [Plan] |

### Critical Dependencies

**Dependency 1: [Name]**
- Description: [Details]
- Type: [Internal/External/Technical/Data]
- Owner: [Name]
- Status: [On Track/At Risk/Delayed/Complete]
- Critical: Yes
- Due Date: [Date]
- Contingency: [Plan]

**Dependency 2: [Name]**
- Description: [Details]
- Type: [Internal/External/Technical/Data]
- Owner: [Name]
- Status: [On Track/At Risk/Delayed/Complete]
- Critical: Yes
- Due Date: [Date]
- Contingency: [Plan]

## Review Schedule
- [ ] Weekly risk review
- [ ] Weekly dependency check-in
- [ ] Monthly full review
```

---

## Real-World Examples

### Example 1: Integration Project

```markdown
# Risk and Dependencies: Payment Integration

## Risks

### Risk Register

| ID | Risk | Category | Prob | Impact | Level | Mitigation | Owner | Status |
|----|------|----------|------|--------|-------|------------|-------|--------|
| R1 | Stripe API changes | Technical | M | H | High | Abstraction layer | Dev | Open |
| R2 | Integration delayed | Schedule | M | H | High | Early testing | Dev | Open |
| R3 | Security issues | Technical | L | C | High | Security audit | Security | Open |
| R4 | Documentation inaccurate | Technical | M | M | Medium | Verify with testing | Dev | Open |

### High Priority Risks

**Risk 1: Stripe API changes**
- Description: API may change without notice
- Probability: Medium
- Impact: High
- Level: High
- Mitigation: Build abstraction layer, subscribe to changelog
- Owner: Backend Lead
- Status: Open

## Dependencies

### Dependency Map

Critical Path:
Stripe Account → API Keys → Integration → Testing → Launch

### Dependency Register

| Dependency | Type | Owner | Status | Critical | Due Date | Contingency |
|------------|------|-------|--------|----------|----------|-------------|
| Stripe Account | External | PM | Complete | Yes | Week 1 | PayPal |
| API Keys | External | PM | Complete | Yes | Week 1 | N/A |
| Design Assets | External | Design | On Track | No | Week 2 | Wireframes |

### Critical Dependencies

**Dependency 1: Stripe API Access**
- Description: Need API keys and account configured
- Type: External
- Owner: Project Manager
- Status: Complete
- Critical: Yes
- Due Date: Week 1
- Contingency: Use PayPal as backup
```

### Example 2: New Product Development

```markdown
# Risk and Dependencies: New Product Launch

## Risks

### Risk Register

| ID | Risk | Category | Prob | Impact | Level | Mitigation | Owner | Status |
|----|------|----------|------|--------|-------|------------|-------|--------|
| R1 | Scope creep | Schedule | H | H | Critical | Change control | PM | Open |
| R2 | Performance issues | Technical | M | C | Critical | Load testing | Dev | Open |
| R3 | Team turnover | Resource | L | H | Medium | Documentation | Tech Lead | Open |
| R4 | Design delayed | Schedule | M | H | High | Buffer, wireframes | PM | Open |

### High Priority Risks

**Risk 1: Scope creep**
- Description: Stakeholders keep adding features
- Probability: High
- Impact: High
- Level: Critical
- Mitigation: Strict change control, document scope
- Owner: Project Manager
- Status: Open

**Risk 2: Performance at scale**
- Description: System may not handle expected load
- Probability: Medium
- Impact: Critical
- Level: Critical
- Mitigation: Load testing early, optimize queries
- Owner: DevOps Engineer
- Status: Open

## Dependencies

### Dependency Map

Critical Path:
Requirements → Design → Development → Testing → Launch

### Dependency Register

| Dependency | Type | Owner | Status | Critical | Due Date | Contingency |
|------------|------|-------|--------|----------|----------|-------------|
| Requirements | Internal | PO | Complete | Yes | Week 1 | N/A |
| Design | External | Agency | At Risk | Yes | Week 3 | Internal team |
| Infrastructure | Technical | DevOps | On Track | Yes | Week 2 | Manual setup |
```

### Example 3: System Migration

```markdown
# Risk and Dependencies: Legacy System Migration

## Risks

### Risk Register

| ID | Risk | Category | Prob | Impact | Level | Mitigation | Owner | Status |
|----|------|----------|------|--------|-------|------------|-------|--------|
| R1 | Data loss | Technical | L | C | Critical | Backup, test migration | Data Eng | Open |
| R2 | Migration delayed | Schedule | H | H | Critical | Buffer, parallel run | PM | Open |
| R3 | User adoption | Resource | M | H | High | Training, support | PM | Open |
| R4 | Integration fails | Technical | M | H | High | Test early, fallback | Dev | Open |

### High Priority Risks

**Risk 1: Data loss during migration**
- Description: Critical data may be lost or corrupted
- Probability: Low
- Impact: Critical
- Level: Critical
- Mitigation: Full backup before migration, test with sample data
- Owner: Data Engineer
- Status: Open

## Dependencies

### Dependency Map

Critical Path:
Legacy System Export → Data Validation → Import → Testing → Cutover

### Dependency Register

| Dependency | Type | Owner | Status | Critical | Due Date | Contingency |
|------------|------|-------|--------|----------|----------|-------------|
| Legacy Access | Internal | Legacy Team | On Track | Yes | Week 1 | Manual export |
| Data Mapping | Technical | Data Eng | In Progress | Yes | Week 2 | Manual mapping |
| User Training | Internal | PM | Not Started | No | Week 6 | Online tutorials |
```

---

## Templates

### Risk Register Template

```markdown
# Risk Register: [Project Name]

**Version:** 1.0
**Date:** [Date]

| ID | Risk | Category | Probability | Impact | Risk Level | Mitigation | Owner | Status | Last Updated |
|----|------|----------|-------------|--------|------------|------------|-------|--------|--------------|
| R1 | [Risk description] | [Type] | [L/M/H] | [L/M/H/C] | [Level] | [Mitigation plan] | [Name] | [Status] | [Date] |
| R2 | [Risk description] | [Type] | [L/M/H] | [L/M/H/C] | [Level] | [Mitigation plan] | [Name] | [Status] | [Date] |

## Risk Summary
- Total Risks: [number]
- Critical: [number]
- High: [number]
- Medium: [number]
- Low: [number]

## High Priority Risks
[Details of top 3-5 risks]

## Review Schedule
- [ ] Weekly review
- [ ] Monthly full review
```

### Dependency Tracking Template

```markdown
# Dependency Tracking: [Project Name]

**Version:** 1.0
**Date:** [Date]

## Critical Path
[Dependency 1] → [Dependency 2] → [Dependency 3] → [Dependency 4]

## Dependency Register

| Dependency | Type | Owner | Status | Critical | Due Date | Contingency | Last Updated |
|------------|------|-------|--------|----------|----------|-------------|--------------|
| [Dep 1] | [Internal/External/Technical/Data] | [Name] | [Status] | Yes/No | [Date] | [Plan] | [Date] |
| [Dep 2] | [Internal/External/Technical/Data] | [Name] | [Status] | Yes/No | [Date] | [Plan] | [Date] |

## Status Summary
- On Track: [number]
- At Risk: [number]
- Delayed: [number]
- Complete: [number]

## Critical Dependencies
[Details of critical dependencies]

## Review Schedule
- [ ] Weekly check-in
- [ ] Milestone review
```

### Risk Assessment Template

```markdown
# Risk Assessment: [Risk Name]

**Date:** [Date]
**Assessed by:** [Name]

## Risk Description
[Detailed description of the risk]

## Risk Assessment

### Probability
- [ ] Low (< 30%)
- [ ] Medium (30-70%)
- [ ] High (> 70%)

### Impact
- [ ] Low (minor, easy to recover)
- [ ] Medium (significant, recoverable)
- [ ] High (major, difficult to recover)
- [ ] Critical (project failure possible)

### Risk Level
[Calculated level based on probability × impact]

## Mitigation Strategy

### Strategy
- [ ] Avoid
- [ ] Reduce
- [ ] Transfer
- [ ] Accept

### Mitigation Plan
[Detailed mitigation actions]

### Implementation
- Timeline: [When]
- Owner: [Who]
- Cost: [How much]
- Resources: [What]

### Contingency Plan
[What if mitigation fails?]

## Monitoring
- How will we monitor this risk?
- What triggers action?
- How often will we review?

## Approval
Risk Owner: _________________ Date: _______
Project Manager: ____________ Date: _______
```

### Dependency Agreement Template

```markdown
# Dependency Agreement: [Dependency Name]

**Project:** [Project Name]
**Date:** [Date]

## Dependency Details
- **Name:** [Dependency name]
- **Description:** [What is being delivered]
- **Type:** [Internal/External/Technical/Data]
- **Owner:** [Name/Team]

## Deliverables
[Detailed description of what will be delivered]

## Due Date
- **Planned:** [Date]
- **Latest Acceptable:** [Date]

## Quality Criteria
[What defines "done"?]

## Communication Plan
- **Frequency:** [Daily/Weekly/Milestone]
- **Method:** [Slack/Email/Meeting]
- **Reporting:** [What to report]

## Contingency Plan
[What if dependency is delayed or not delivered?]

## Sign-Off

Dependency Owner: _________________ Date: _______
Project Manager: ________________ Date: _______
```

---

## Best Practices

1. **Identify early** - Start risk identification at project kickoff
2. **Be realistic** - Don't underestimate risks
3. **Prioritize** - Focus on high-probability, high-impact risks
4. **Document thoroughly** - Maintain comprehensive risk register
5. **Assign owners** - Every risk needs someone responsible
6. **Monitor regularly** - Review risks weekly
7. **Mitigate proactively** - Don't wait for risks to materialize
8. **Communicate clearly** - Keep stakeholders informed
9. **Learn from experience** - Track what worked and what didn't
10. **Be agile** - Adjust plans as risks change

---

## Related Skills

- [Discovery Questions](../discovery-questions/SKILL.md) - Identify risks during discovery
- [Requirement to Scope](../requirement-to-scope/SKILL.md) - Account for risks in scope
- [Acceptance Criteria](../acceptance-criteria/SKILL.md) - Address risks in acceptance criteria
- [Constraints and Assumptions](../constraints-and-assumptions/SKILL.md) - Risks from invalid assumptions
