# Constraints and Assumptions

## Overview

Constraints are fixed limitations that you must work within. Assumptions are things you believe to be true but need validation. Documenting both is critical for project success.

## Definitions

| Term | Definition |
|------|------------|
| **Constraints** | Fixed limitations that must be worked within (budget, timeline, resources, regulations) |
| **Assumptions** | Things believed to be true that need validation (technical, user, data, availability) |

## Why Documenting Them Matters

| Benefit | Description |
|---------|-------------|
| **Surface hidden risks** - Identify potential problems early |
| **Clarify expectations** - Align stakeholders on what's possible |
| **Guide decisions** - Make informed choices based on known limits |
| **Identify validation needs** - Know what needs to be verified |
| **Prevent surprises** - Avoid unexpected issues mid-project |
| **Support change management** - Baseline for managing changes |

---

## Types of Constraints

### 1. Budget Constraints

Financial limitations that affect the project.

```
Budget Constraints:

Total Budget: $50,000
- Development: $35,000 (70%)
- Infrastructure: $10,000 (20%)
- Third-party services: $3,000 (6%)
- Contingency: $2,000 (4%)

Breakdown by Phase:
- Phase 1 (MVP): $30,000
- Phase 2: $15,000
- Phase 3: $5,000

Infrastructure Costs:
- Cloud hosting: $500/month
- Database: $200/month
- CDN: $100/month
- Monitoring: $50/month

Third-Party Costs:
- Payment gateway: 2.9% + $0.30 per transaction
- Email service: $50/month
- Analytics: Free tier

Development Costs:
- 2 developers × $100/hour × 160 hours/month × 2 months = $64,000
- Wait, this exceeds budget! Need to adjust scope or timeline.
```

### 2. Time Constraints

Deadlines and timeline limitations.

```
Time Constraints:

Hard Deadline: June 30, 2024 (product launch event)
Soft Deadline: June 15, 2024 (for testing and buffer)

Milestones:
- Week 2: Design approval
- Week 4: MVP feature complete
- Week 6: Testing complete
- Week 8: Launch ready

Dependency Deadlines:
- Design assets: Week 2 (blocks development)
- Third-party API access: Week 3 (blocks integration)
- Stakeholder review: Week 5 (blocks finalization)

Working Days:
- Monday-Friday only
- No work on holidays
- Team availability: 80% (accounting for meetings, etc.)

Time Zone Considerations:
- Team: UTC+7 (Bangkok)
- Stakeholders: UTC-5 (New York)
- Overlap: 9 AM - 12 PM Bangkok time
```

### 3. Resource Constraints

Limitations on people, skills, and tools.

```
Resource Constraints:

Team Size: 3 people
- 2 developers (full-stack)
- 1 designer (part-time, 20 hours/week)
- 0 dedicated QA (developers will test)

Skills Available:
- Frontend: React, TypeScript, CSS
- Backend: Node.js, PostgreSQL
- DevOps: Basic AWS deployment
- Design: Figma, UI/UX
- Missing: Mobile development, advanced DevOps

Tools Available:
- IDE: VS Code
- Version control: GitHub
- Project management: Jira
- Communication: Slack
- Design: Figma
- Testing: Jest, Cypress (basic)

Third-Party Resources:
- Design agency: Available for 10 hours/week
- Security consultant: Available on-demand ($200/hour)
- Legal counsel: Available for compliance review
```

### 4. Technical Constraints

Technology and system limitations.

```
Technical Constraints:

Must Use:
- Frontend: React 18, TypeScript
- Backend: Node.js 18, Fastify
- Database: PostgreSQL 14
- Hosting: AWS (company standard)
- CI/CD: GitHub Actions

Must Integrate With:
- Existing authentication system (OAuth 2.0)
- Legacy user database (MySQL, read-only)
- Third-party payment gateway (Stripe)
- Email service (SendGrid)

Performance Requirements:
- API response time: P95 < 200ms
- Page load time: P95 < 2 seconds
- Database query time: P95 < 100ms
- Support 10,000 concurrent users

Browser/Device Support:
- Desktop: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- Mobile: iOS 14+, Android 10+
- No IE support

Scalability Requirements:
- Initial: 1,000 users
- Target: 10,000 users (Year 1)
- Peak: 50,000 users (marketing events)
```

### 5. Legal/Compliance Constraints

Regulatory and legal requirements.

```
Legal/Compliance Constraints:

Data Privacy:
- GDPR: Yes (EU users)
- CCPA: Yes (California users)
- PDPA: Yes (Thailand users)
- Data retention: 2 years, then delete
- Right to be forgotten: Must implement

Industry Regulations:
- HIPAA: No (not healthcare)
- PCI-DSS: Yes (payment processing)
- SOC2: No (not required yet)
- ISO 27001: No (not required yet)

Accessibility:
- WCAG 2.1 Level AA: Yes (required by law in some regions)
- Screen reader support: Yes
- Keyboard navigation: Yes
- Color contrast: 4.5:1 minimum

Security Standards:
- HTTPS only: Yes
- Data encryption at rest: Yes (AES-256)
- Data encryption in transit: Yes (TLS 1.3)
- Penetration testing: Required before launch

Legal Review:
- Terms of service: Must be reviewed by legal
- Privacy policy: Must be reviewed by legal
- Cookie consent: Required (GDPR)
```

### 6. Business Constraints

Organizational and operational limitations.

```
Business Constraints:

Brand Guidelines:
- Primary color: #3B82F6 (blue)
- Secondary color: #10B981 (green)
- Font: Inter (Google Fonts)
- Logo: Must be in top-left corner
- Tone: Professional, friendly, concise

Approval Processes:
- Design changes: Require product owner approval
- Feature changes: Require product owner + tech lead approval
- Budget changes: Require VP approval
- Launch decisions: Require CEO approval

Communication Channels:
- Daily standups: Slack
- Weekly updates: Email to stakeholders
- Sprint reviews: In-person/Zoom
- Critical issues: Slack @channel

Existing Commitments:
- Contract with payment provider (Stripe): 1 year
- Contract with email provider (SendGrid): 1 year
- Hosting commitment (AWS): 3 years (reserved instances)
- Team availability: Committed for 6 months

Pricing Constraints:
- Cannot exceed $10/month per user
- Must offer free tier (up to 5 users)
- Enterprise tier: Custom pricing
```

---

## Types of Assumptions

### 1. Technical Assumptions

Beliefs about technology and systems.

```
Technical Assumptions:

API Availability:
- Third-party API will be available 99.9% of the time
- API rate limits will not be exceeded
- API will not change without notice
- API documentation is accurate

Technology Capabilities:
- PostgreSQL can handle 10,000 concurrent connections
- Redis can cache all frequently accessed data
- CDN will cache 95% of static assets
- Load balancer will distribute traffic evenly

Integration Points:
- Legacy system can provide read-only access
- Authentication system supports OAuth 2.0
- Email service will deliver 99% of emails
- Payment gateway will process transactions in < 2 seconds

Performance:
- Current infrastructure can support 10x growth
- Database queries will remain fast with 10x data
- CDN will reduce latency by 80%
- Caching will reduce database load by 70%
```

### 2. User Assumptions

Beliefs about users and their behavior.

```
User Assumptions:

Technical Proficiency:
- Users are comfortable with web applications
- Users understand basic internet concepts
- Users can troubleshoot simple issues
- Users have reliable internet connection

Device/Browser:
- Users have modern browsers (Chrome, Firefox, Safari)
- Users have devices with at least 4GB RAM
- Users have screens with minimum 1024x768 resolution
- 80% of users access from desktop, 20% from mobile

Behavior:
- Users will read documentation before asking for help
- Users will provide feedback when prompted
- Users will complete onboarding flow
- Users will return to the application regularly

Location:
- 60% of users are in North America
- 30% of users are in Europe
- 10% of users are in Asia-Pacific
- Users are primarily in urban areas
```

### 3. Data Assumptions

Beliefs about data quality and availability.

```
Data Assumptions:

Data Quality:
- Product data is accurate and complete
- User data is clean and consistent
- Historical data is reliable
- No duplicate records exist

Data Volume:
- Initial data: 10,000 products
- Expected growth: 1,000 products/month
- User data: 1,000 users initially
- Expected growth: 100 users/month

Data Structure:
- Database schema is optimized
- Indexes are properly configured
- No data migration needed
- Data relationships are correct

Data Availability:
- Data will be available when needed
- Data exports can be generated on demand
- Real-time sync is possible
- No data loss will occur
```

### 4. Availability Assumptions

Beliefs about resource availability.

```
Availability Assumptions:

Team Availability:
- All team members will be available for full project duration
- No unexpected absences will occur
- Team will maintain current skill level
- Team will not be pulled to other projects

Stakeholder Availability:
- Product owner will provide timely feedback
- Stakeholders will attend required meetings
- Decisions will be made within 48 hours
- No scope changes will occur mid-project

Third-Party Availability:
- Vendors will deliver on time
- APIs will remain stable
- Services will not go down unexpectedly
- Support will be available when needed

Infrastructure Availability:
- Cloud provider will maintain 99.9% uptime
- Database will not have extended outages
- CDN will serve content reliably
- Load balancer will not fail
```

### 5. Third-Party Assumptions

Beliefs about external vendors and services.

```
Third-Party Assumptions:

Vendor Reliability:
- Stripe will process payments reliably
- SendGrid will deliver emails reliably
- Google Analytics will track accurately
- AWS will maintain uptime SLA

Vendor Support:
- Support will respond within 24 hours
- Critical issues will be resolved in 4 hours
- Documentation will be accurate and up-to-date
- APIs will be stable and well-documented

Vendor Pricing:
- Pricing will not increase unexpectedly
- Free tiers will remain available
- No hidden fees will be charged
- Billing will be accurate

Vendor Roadmap:
- No breaking changes will occur
- New features will be backward compatible
- Deprecation notices will be given 6 months in advance
- Migration paths will be provided
```

---

## Documenting Assumptions

For each assumption, document key information.

### Assumption Documentation Template

```
Assumption: [Statement of what we believe to be true]

Impact if Wrong:
- [What happens if this assumption is incorrect?]
- [How does it affect the project?]
- [What's the severity of the impact?]

Validation Method:
- [How will we validate this assumption?]
- [When will we validate it?]
- [Who is responsible for validation?]

Validation Status:
- [ ] Not validated
- [ ] In progress
- [ ] Validated (confirmed true)
- [ ] Invalidated (confirmed false)

Contingency Plan:
- [What will we do if the assumption is wrong?]
- [What's the backup plan?]

Owner: [Name of person responsible]
Due Date: [Date when validation should be complete]
```

### Example Assumption Documentation

```
Assumption: Users have modern browsers (Chrome 90+, Firefox 88+, Safari 14+)

Impact if Wrong:
- If users have older browsers, features may not work
- May need to implement polyfills
- May need to support older browsers (adds development time)
- Could affect user experience and adoption

Validation Method:
- Check Google Analytics for browser usage data
- Survey existing users about their browser versions
- Test on older browsers to identify issues

Validation Status:
[ ] Not validated
[x] In progress (analytics review)
[ ] Validated
[ ] Invalidated

Contingency Plan:
- If >10% of users have older browsers:
  - Implement polyfills for critical features
  - Add browser upgrade prompts
  - Consider supporting older browsers for core features

Owner: Product Manager
Due Date: Week 2
```

---

## Example Assumptions

### Common Assumptions by Category

#### Technical Assumptions

```
1. API will be available and reliable
   Impact: Payment processing, email delivery
   Validation: Test API endpoints, check SLA

2. Database can handle expected load
   Impact: Performance, user experience
   Validation: Load testing, query optimization

3. Third-party library will be maintained
   Impact: Security, bug fixes
   Validation: Check library activity, last update date

4. Infrastructure can scale to meet demand
   Impact: Performance, availability
   Validation: Load testing, capacity planning

5. Integration with legacy system is possible
   Impact: Data access, user migration
   Validation: Proof of concept, API testing
```

#### User Assumptions

```
1. Users have internet connection
   Impact: Application usability
   Validation: User survey, usage analytics

2. Users understand basic web concepts
   Impact: Onboarding, support
   Validation: User testing, feedback

3. Users will provide accurate data
   Impact: Data quality, analytics
   Validation: Data validation, user testing

4. Users will read documentation
   Impact: Support burden
   Validation: User testing, analytics

5. Users will complete onboarding
   Impact: Adoption, retention
   Validation: Funnel analytics, user testing
```

#### Data Assumptions

```
1. Product data is accurate and complete
   Impact: User experience, business operations
   Validation: Data audit, manual review

2. User data is clean and consistent
   Impact: Analytics, reporting
   Validation: Data quality checks

3. Historical data is reliable
   Impact: Trend analysis, forecasting
   Validation: Data validation, cross-reference

4. Data can be migrated from legacy system
   Impact: User migration, continuity
   Validation: Migration testing
```

#### Availability Assumptions

```
1. Team will be available for full project
   Impact: Timeline, delivery
   Validation: Team commitment, resource planning

2. Stakeholders will provide timely feedback
   Impact: Decision making, progress
   Validation: Communication plan, SLA

3. Third-party vendors will deliver on time
   Impact: Dependencies, timeline
   Validation: Vendor contracts, SLA

4. No major scope changes will occur
   Impact: Timeline, budget
   Validation: Change control process
```

---

## Validating Assumptions

Don't assume - validate early and often.

### Validation Timeline

```
Project Phase 1 (Planning):
- Validate critical assumptions
- Validate high-risk assumptions
- Validate assumptions that affect scope

Project Phase 2 (Development):
- Validate technical assumptions
- Validate integration assumptions
- Validate performance assumptions

Project Phase 3 (Testing):
- Validate user assumptions
- Validate data assumptions
- Validate availability assumptions
```

### Validation Methods

| Method | When to Use | Example |
|--------|-------------|---------|
| **Testing** | Technical assumptions | Test API endpoints, load test database |
| **Prototyping** | UX assumptions | Build prototype, test with users |
| **Research** | Market assumptions | Competitor analysis, market research |
| **Surveys** | User assumptions | Survey users about preferences |
| **Analytics** | Behavior assumptions | Analyze usage data, metrics |
| **Expert Review** | Technical assumptions | Consult experts, get opinions |
| **Proof of Concept** | Feasibility assumptions | Build small version to test |

### Validation Checklist

```
Assumption Validation Checklist

For each assumption:
[ ] Is this assumption critical to project success?
[ ] What is the impact if this assumption is wrong?
[ ] How will we validate this assumption?
[ ] When will we validate this assumption?
[ ] Who is responsible for validation?
[ ] What is the contingency plan if validation fails?
[ ] Is the validation complete?
[ ] Was the assumption validated or invalidated?
[ ] If invalidated, what actions were taken?
```

---

## Risk of Invalid Assumptions

Invalid assumptions can derail projects.

### Impact Assessment

```
Assumption: Third-party API will support feature X

If Validated True:
- Proceed with implementation
- Use API as planned
- Project on track

If Invalidated False:
- API doesn't support feature X
- Need alternative approach:
  - Build feature ourselves (adds time, cost)
  - Use different API (may not exist)
  - Drop feature from scope (affects value)
- Impact: Timeline delay, budget increase, scope reduction
```

### Common Invalid Assumption Impacts

| Invalid Assumption | Impact | Severity |
|-------------------|--------|----------|
| Users have modern browsers | Need polyfills, older browser support | Medium |
| API will be available | Need backup, alternative API | High |
| Team will be available | Need additional resources | High |
| Data is clean | Need data cleaning, ETL | Medium |
| No scope changes | Scope creep, timeline delay | High |
| Infrastructure can scale | Performance issues, downtime | Critical |

---

## Constraints and Assumptions Document

Create a comprehensive document for your project.

### Document Structure

```markdown
# Constraints and Assumptions: [Project Name]

**Version:** 1.0
**Date:** [Date]
**Author:** [Name]

## Constraints

### Budget Constraints
[Details]

### Time Constraints
[Details]

### Resource Constraints
[Details]

### Technical Constraints
[Details]

### Legal/Compliance Constraints
[Details]

### Business Constraints
[Details]

## Assumptions

### Technical Assumptions
[Details]

### User Assumptions
[Details]

### Data Assumptions
[Details]

### Availability Assumptions
[Details]

### Third-Party Assumptions
[Details]

## Validation Status

| Assumption | Status | Owner | Due Date |
|------------|--------|-------|----------|
| [Assumption 1] | Validated | [Name] | [Date] |
| [Assumption 2] | In Progress | [Name] | [Date] |
| [Assumption 3] | Not Validated | [Name] | [Date] |

## Contingency Plans
[Details for invalidated assumptions]

## Review Schedule
- [ ] Weekly review during planning
- [ ] Bi-weekly review during development
- [ ] Final review before launch
```

---

## Template Structure

### Complete Constraints and Assumptions Template

```markdown
# Constraints and Assumptions: [Project Name]

**Version:** 1.0
**Date:** [Date]
**Author:** [Name]

## Constraints

### Budget Constraints
- Total budget: $[amount]
- Development: $[amount]
- Infrastructure: $[amount]
- Third-party services: $[amount]
- Contingency: $[amount]

### Time Constraints
- Hard deadline: [date]
- Soft deadline: [date]
- Milestones:
  - [Milestone 1]: [date]
  - [Milestone 2]: [date]

### Resource Constraints
- Team size: [number] people
- Skills: [list]
- Tools: [list]
- Third-party resources: [list]

### Technical Constraints
- Must use: [technologies]
- Must integrate with: [systems]
- Performance requirements: [metrics]
- Browser/device support: [list]

### Legal/Compliance Constraints
- GDPR: Yes/No
- PCI-DSS: Yes/No
- WCAG 2.1: Yes/No
- Other: [list]

### Business Constraints
- Brand guidelines: [link]
- Approval processes: [description]
- Communication channels: [list]
- Existing commitments: [list]

## Assumptions

### Technical Assumptions

| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| [Assumption 1] | [Impact] | [Method] | [Name] | [Status] |
| [Assumption 2] | [Impact] | [Method] | [Name] | [Status] |

### User Assumptions

| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| [Assumption 1] | [Impact] | [Method] | [Name] | [Status] |
| [Assumption 2] | [Impact] | [Method] | [Name] | [Status] |

### Data Assumptions

| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| [Assumption 1] | [Impact] | [Method] | [Name] | [Status] |
| [Assumption 2] | [Impact] | [Method] | [Name] | [Status] |

### Availability Assumptions

| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| [Assumption 1] | [Impact] | [Method] | [Name] | [Status] |
| [Assumption 2] | [Impact] | [Method] | [Name] | [Status] |

### Third-Party Assumptions

| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| [Assumption 1] | [Impact] | [Method] | [Name] | [Status] |
| [Assumption 2] | [Impact] | [Method] | [Name] | [Status] |

## Contingency Plans

### [Invalidated Assumption 1]
- Issue: [Description]
- Impact: [Impact]
- Plan: [Contingency plan]
- Status: [In progress/Complete]

### [Invalidated Assumption 2]
- Issue: [Description]
- Impact: [Impact]
- Plan: [Contingency plan]
- Status: [In progress/Complete]

## Review Schedule
- [ ] Initial review: [Date]
- [ ] Planning review: [Date]
- [ ] Development review: [Date]
- [ ] Pre-launch review: [Date]
```

---

## Change Management

What happens when constraints change or assumptions are invalidated.

### Constraint Changes

```
Constraint Change Process:

1. Identify Change
   - Constraint has changed (e.g., more budget, more time)
   - Document what changed and why

2. Assess Impact
   - How does this affect the project?
   - What can we do differently?
   - What's the new baseline?

3. Update Plan
   - Adjust scope, timeline, or quality
   - Update project plan
   - Communicate to stakeholders

4. Document Change
   - Update constraints document
   - Note reason for change
   - Get approval if needed
```

### Assumption Invalidation

```
Assumption Invalidation Process:

1. Identify Invalidation
   - Assumption proven false
   - Document what was wrong

2. Assess Impact
   - How does this affect the project?
   - What's the severity?
   - What needs to change?

3. Execute Contingency
   - Implement contingency plan
   - Adjust project as needed
   - Communicate impact

4. Update Documentation
   - Mark assumption as invalidated
   - Document what was done
   - Learn for future projects
```

---

## Communication

Share constraints and assumptions with the right people.

### Communication Matrix

| Audience | What to Share | When | How |
|----------|---------------|------|-----|
| **Team** | All constraints, all assumptions | Project kickoff, updates | Project documentation, meetings |
| **Stakeholders** | Critical constraints, high-risk assumptions | Project kickoff, changes | Executive summary, meetings |
| **Management** | Budget, timeline, resource constraints | Project kickoff, changes | Reports, presentations |
| **Vendors** | Integration constraints, API assumptions | Onboarding, changes | Contracts, documentation |

### Regular Reviews

```
Review Schedule:

Weekly (during planning):
- Review constraint status
- Review assumption validation progress
- Identify new assumptions

Bi-weekly (during development):
- Review constraint changes
- Review invalidated assumptions
- Update contingency plans

Monthly (overall):
- Full review of all constraints and assumptions
- Assess overall risk
- Adjust plans as needed
```

---

## Real-World Examples

### Example 1: E-Commerce Project

```markdown
# Constraints and Assumptions: Online Store

## Constraints

### Budget Constraints
- Total: $50,000
- Development: $35,000
- Infrastructure: $10,000
- Third-party: $5,000

### Time Constraints
- Launch: June 30 (hard deadline)
- MVP ready: June 15

### Resource Constraints
- Team: 2 developers, 1 designer
- No dedicated QA

### Technical Constraints
- Must use React + Node.js
- Must integrate with Stripe
- Must support 10,000 concurrent users

### Legal/Compliance Constraints
- PCI-DSS: Yes (payment processing)
- GDPR: Yes (EU users)
- WCAG 2.1: Yes (accessibility)

## Assumptions

### Technical Assumptions
| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| Stripe API available 99.9% | Payment processing | SLA review | Dev | Validated |
| Database can handle 10K users | Performance | Load testing | Dev | In progress |
| CDN caches 95% of assets | Performance | Analytics review | Dev | Not validated |

### User Assumptions
| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| Users have modern browsers | Compatibility | Analytics check | PM | Validated |
| Users understand e-commerce | UX | User testing | Designer | In progress |
| Users will provide payment info | Conversion | Analytics | PM | Not validated |

### Data Assumptions
| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| Product data is accurate | User experience | Data audit | PM | Validated |
| Product images are available | UI | Manual check | PM | In progress |
```

### Example 2: Mobile App Development

```markdown
# Constraints and Assumptions: Mobile App

## Constraints

### Budget Constraints
- Total: $100,000
- Development: $70,000
- Design: $20,000
- Testing: $10,000

### Time Constraints
- iOS launch: September 1
- Android launch: September 15

### Resource Constraints
- Team: 3 developers (2 iOS, 1 Android)
- Designer: 1 (part-time)

### Technical Constraints
- iOS: iOS 14+ only
- Android: Android 10+ only
- Must use React Native (cross-platform)
- App Store review: 1-2 weeks

### Legal/Compliance Constraints
- App Store guidelines: Must follow
- Play Store guidelines: Must follow
- Privacy policy: Required

## Assumptions

### Technical Assumptions
| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| React Native performance adequate | UX | Prototype testing | Tech Lead | Validated |
| App Store approval in 1 week | Timeline | Past experience | PM | Not validated |
| Push notifications work reliably | Engagement | Testing | Dev | In progress |

### User Assumptions
| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| Users will grant permissions | Functionality | Beta testing | PM | In progress |
| Users have stable internet | App usability | Analytics | PM | Not validated |
| Users will rate the app | App Store ranking | Analytics | PM | Not validated |
```

### Example 3: API Integration Project

```markdown
# Constraints and Assumptions: Payment API Integration

## Constraints

### Budget Constraints
- Total: $25,000
- Development: $20,000
- Testing: $5,000

### Time Constraints
- Integration complete: 4 weeks
- Testing complete: 5 weeks
- Launch: 6 weeks

### Resource Constraints
- Team: 1 backend developer
- QA: Shared resource (10 hours/week)

### Technical Constraints
- Must use existing payment provider
- Must maintain PCI-DSS compliance
- Must support existing database schema
- Must not break existing functionality

### Legal/Compliance Constraints
- PCI-DSS: Yes (payment processing)
- Data retention: 7 years (transaction records)

## Assumptions

### Technical Assumptions
| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| API documentation is accurate | Integration success | API testing | Dev | In progress |
| API supports all needed features | Scope | API review | Dev | Not validated |
| API rate limits sufficient | Performance | Load testing | Dev | Not validated |

### Third-Party Assumptions
| Assumption | Impact | Validation | Owner | Status |
|------------|--------|------------|-------|--------|
| Vendor support available 24/7 | Issue resolution | Contract review | PM | Validated |
| API will not change without notice | Stability | Vendor communication | PM | In progress |
| SLA of 99.9% uptime | Reliability | SLA review | PM | Validated |
```

---

## Templates

### Constraints Template

```markdown
# Constraints: [Project Name]

**Version:** 1.0
**Date:** [Date]

## Budget Constraints
- Total: $[amount]
- Development: $[amount]
- Infrastructure: $[amount]
- Third-party: $[amount]

## Time Constraints
- Hard deadline: [date]
- Soft deadline: [date]
- Milestones:
  - [Milestone]: [date]

## Resource Constraints
- Team size: [number]
- Skills: [list]
- Tools: [list]

## Technical Constraints
- Must use: [technologies]
- Must integrate with: [systems]
- Performance: [requirements]

## Legal/Compliance Constraints
- [Regulation 1]: Yes/No
- [Regulation 2]: Yes/No
- [Regulation 3]: Yes/No

## Business Constraints
- Brand guidelines: [link]
- Approval processes: [description]
- Communication: [channels]
```

### Assumptions Template

```markdown
# Assumptions: [Project Name]

**Version:** 1.0
**Date:** [Date]

## Technical Assumptions

| Assumption | Impact | Validation Method | Owner | Status | Due Date |
|------------|--------|-------------------|-------|--------|----------|
| [Assumption] | [Impact] | [Method] | [Name] | [Status] | [Date] |

## User Assumptions

| Assumption | Impact | Validation Method | Owner | Status | Due Date |
|------------|--------|-------------------|-------|--------|----------|
| [Assumption] | [Impact] | [Method] | [Name] | [Status] | [Date] |

## Data Assumptions

| Assumption | Impact | Validation Method | Owner | Status | Due Date |
|------------|--------|-------------------|-------|--------|----------|
| [Assumption] | [Impact] | [Method] | [Name] | [Status] | [Date] |

## Availability Assumptions

| Assumption | Impact | Validation Method | Owner | Status | Due Date |
|------------|--------|-------------------|-------|--------|----------|
| [Assumption] | [Impact] | [Method] | [Name] | [Status] | [Date] |

## Third-Party Assumptions

| Assumption | Impact | Validation Method | Owner | Status | Due Date |
|------------|--------|-------------------|-------|--------|----------|
| [Assumption] | [Impact] | [Method] | [Name] | [Status] | [Date] |
```

### Validation Checklist Template

```markdown
# Assumption Validation Checklist

**Project:** [Project Name]
**Date:** [Date]

## Critical Assumptions

| Assumption | Validation Method | Owner | Status | Notes |
|------------|-------------------|-------|--------|-------|
| [Assumption 1] | [Method] | [Name] | [Status] | [Notes] |
| [Assumption 2] | [Method] | [Name] | [Status] | [Notes] |

## High-Risk Assumptions

| Assumption | Validation Method | Owner | Status | Notes |
|------------|-------------------|-------|--------|-------|
| [Assumption 1] | [Method] | [Name] | [Status] | [Notes] |
| [Assumption 2] | [Method] | [Name] | [Status] | [Notes] |

## Invalidated Assumptions

| Assumption | Impact | Contingency Plan | Status |
|------------|--------|------------------|--------|
| [Assumption 1] | [Impact] | [Plan] | [Status] |
| [Assumption 2] | [Impact] | [Plan] | [Status] |

## Next Steps
- [ ] Validate [Assumption 1] by [Date]
- [ ] Validate [Assumption 2] by [Date]
- [ ] Review invalidated assumptions
- [ ] Update contingency plans
```

### Impact Analysis Framework Template

```markdown
# Impact Analysis: [Assumption Name]

**Assumption:** [Statement]
**Date:** [Date]

## Impact if Invalidated

### Project Impact
- Timeline: [Delay in weeks/days]
- Budget: [Additional cost]
- Scope: [Features affected]
- Quality: [Quality impact]

### Business Impact
- Revenue: [Impact on revenue]
- Customer satisfaction: [Impact]
- Reputation: [Impact]
- Legal/Compliance: [Impact]

### Technical Impact
- Architecture: [Changes needed]
- Development: [Additional work]
- Testing: [Additional testing]
- Deployment: [Deployment impact]

## Contingency Plan

### Option 1: [Description]
- Effort: [Time/Cost]
- Feasibility: [High/Med/Low]
- Risk: [High/Med/Low]

### Option 2: [Description]
- Effort: [Time/Cost]
- Feasibility: [High/Med/Low]
- Risk: [High/Med/Low]

## Recommendation
[Recommended contingency plan and rationale]

## Owner
[Name of person responsible]

## Due Date
[Date for decision]
```

---

## Best Practices

1. **Document early** - Capture constraints and assumptions at project start
2. **Be specific** - Clear, unambiguous statements
3. **Validate assumptions** - Don't assume, verify
4. **Prioritize** - Focus on critical and high-risk items
5. **Review regularly** - Update as project progresses
6. **Communicate** - Share with relevant stakeholders
7. **Plan contingencies** - Have backup plans for invalid assumptions
8. **Learn from experience** - Track what was right/wrong for future projects
9. **Get sign-off** - Stakeholders should acknowledge constraints
10. **Be realistic** - Don't overcommit based on optimistic assumptions

---

## Related Skills

- [Discovery Questions](../discovery-questions/SKILL.md) - Identify constraints and assumptions during discovery
- [Requirement to Scope](../requirement-to-scope/SKILL.md) - Incorporate constraints into scope
- [Acceptance Criteria](../acceptance-criteria/SKILL.md) - Address constraints in acceptance criteria
- [Risk and Dependencies](../risk-and-dependencies/SKILL.md) - Manage risks from invalid assumptions
