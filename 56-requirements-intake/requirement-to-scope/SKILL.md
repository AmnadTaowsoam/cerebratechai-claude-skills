# Requirement to Scope (In-Scope vs Out-of-Scope)

## Overview

Scoping is the process of defining what will be delivered (in-scope) and explicitly stating what won't be delivered (out-of-scope). This sets clear boundaries and expectations for the project.

## What Is Scoping

Scoping involves:

- **Defining in-scope**: What will be delivered in this project
- **Defining out-of-scope**: What explicitly won't be delivered (deferred or excluded)
- **Setting clear boundaries**: Establishing the project's limits
- **Documenting assumptions**: What we assume to be true
- **Identifying dependencies**: What we rely on

## Why Scoping Matters

| Benefit | Description |
|---------|-------------|
| **Prevent scope creep** | Clear boundaries prevent uncontrolled expansion |
| **Set expectations** | Stakeholders know exactly what will be delivered |
| **Estimate effort accurately** | Clear scope enables better estimation |
| **Avoid misunderstandings** | Explicit out-of-scope prevents "I thought you were doing X" |
| **Enable prioritization** | Focus on what matters most |
| **Support change control** | Baseline scope for managing changes |

---

## Scope Definition Components

### 1. In-Scope
Features and functionality that will be delivered.

### 2. Out-of-Scope
Features and functionality explicitly excluded from this project.

### 3. Assumptions
Things we believe to be true (need validation).

### 4. Dependencies
External factors or systems we rely on.

### 5. Constraints
Limitations that affect the scope (budget, timeline, resources).

---

## From Requirements to Scope

The process of converting raw requirements into a well-defined scope.

```
Requirements → Prioritize → Define MVP → Document Scope
```

### Step 1: Gather All Requirements
- From discovery sessions
- From stakeholder interviews
- From existing documentation
- From competitive analysis

### Step 2: Prioritize Requirements
Use prioritization frameworks (see below) to categorize requirements.

### Step 3: Define MVP (Minimum Viable Scope)
- Core value proposition only
- Remove nice-to-haves
- Simplify where possible

### Step 4: Document Scope
- Write in-scope items clearly
- Explicitly document out-of-scope
- Note assumptions and dependencies

---

## Prioritization Frameworks

### MoSCoW Method

| Category | Definition | Example |
|----------|------------|---------|
| **Must Have** | Non-negotiable, project fails without | User authentication |
| **Should Have** | Important but not vital for launch | Email notifications |
| **Could Have** | Desirable, can be deferred | Social login |
| **Won't Have** | Out of scope for this project | Mobile app |

### RICE Scoring

```
Score = (Reach × Impact × Confidence) / Effort

- Reach: How many users will this affect? (1-10)
- Impact: How much will it benefit users? (0.25-3)
- Confidence: How confident are we? (50%-100%)
- Effort: How much work is required? (months/weeks)

Higher score = Higher priority
```

### Value vs Effort Matrix

```
         Low Effort    High Effort
High Value   Do First    Consider
Low Value    Maybe       Don't Do
```

### Kano Model

| Category | Description | Priority |
|----------|-------------|----------|
| **Basic** | Expected features, absence causes dissatisfaction | Must have |
| **Performance** | More is better, linear relationship | Should have |
| **Delighter** | Unexpected features, creates delight | Could have |

---

## In-Scope Examples

Clear, specific statements of what will be delivered.

```
In-Scope for User Management:

- Users can sign up with email and password
- Users can log in with email and password
- Users can reset password via email link
- Admin can view user list with pagination (20 per page)
- Admin can search users by email or name
- Admin can deactivate user accounts
- System validates email format on signup
- System enforces password requirements (8+ chars, mix of types)
- System sends welcome email after signup
- System logs all authentication events
```

### Writing Good In-Scope Items

- **Specific**: "User can sign up with email and password" (not "User signup")
- **Actionable**: Clear what needs to be built
- **Testable**: Can verify it's complete
- **User-focused**: Describe what users can do

---

## Out-of-Scope Examples

Explicitly stating what won't be delivered.

```
Out-of-Scope for User Management (Phase 1):

- Social login (Google, Facebook, etc.) - Defer to Phase 2
- Multi-factor authentication (2FA) - Defer to Phase 2
- User profile customization - Defer to Phase 2
- Bulk user import - Defer to Phase 2
- User roles and permissions - Defer to Phase 2
- SSO/SAML integration - Defer to Phase 2
- Mobile app - Web only for now
- Multi-language support - English only in MVP
```

### Why Out-of-Scope Matters

| Reason | Example |
|--------|---------|
| Prevents misunderstandings | "I thought you were doing social login" |
| Manages expectations | Stakeholders know what's coming later |
| Documents decisions | Shows what was considered but deferred |
| Enables future planning | Out-of-scope items become Phase 2 backlog |
| Supports change control | Adding out-of-scope items requires formal change |

---

## Assumptions

Things we believe to be true but need validation.

### Example Assumptions

```
Assumptions for E-Commerce Project:

- Users have modern browsers (Chrome, Firefox, Safari, Edge)
- Users have internet connection (no offline mode needed)
- Third-party payment gateway (Stripe) will be available
- Design team will provide mockups by Week 2
- Product data is accurate and complete
- Existing user database can be migrated
- Team members will be available for the full project duration
- No major regulatory changes during development
```

### Documenting Assumptions

For each assumption, note:
- **The assumption**: What we believe to be true
- **Impact**: What happens if it's wrong
- **Validation**: How to verify it
- **Owner**: Who will validate it

```
Assumption: Users have modern browsers
Impact: If false, need polyfills or older browser support (adds effort)
Validation: Check analytics for browser usage
Owner: Product Manager
```

---

## Dependencies

External factors or systems we rely on.

### Types of Dependencies

| Type | Example |
|------|---------|
| **Internal** | Depends on authentication service being ready |
| **External** | Depends on Stripe API for payments |
| **Data** | Depends on product data being available |
| **Resource** | Depends on design team providing assets |
| **Technical** | Depends on existing API endpoints |

### Example Dependencies

```
Dependencies for E-Commerce Project:

Internal:
- Authentication service must be deployed before checkout
- Product catalog API must be available before frontend development
- Design team must provide UI assets by Week 2

External:
- Stripe API for payment processing
- SendGrid API for email notifications
- Google Analytics for tracking

Data:
- Product database must be migrated and validated
- User data must be exported from legacy system

Critical Path:
1. Design assets (Week 2) → Frontend development can start
2. Authentication service (Week 3) → User features can be tested
3. Product data migration (Week 4) → Product catalog can be built
```

---

## Scope Document Structure

A comprehensive scope document includes all key components.

```markdown
# Scope Document: [Project Name]

**Version:** 1.0
**Date:** [Date]
**Author:** [Name]

## Project Overview
[Brief description of the project]

## Goals and Objectives
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

## In-Scope

### User Management
- [ ] User registration with email and password
- [ ] User login with email and password
- [ ] Password reset via email
- [ ] Admin user list with pagination

### Product Catalog
- [ ] Product listing page
- [ ] Product detail page
- [ ] Product search functionality
- [ ] Product filtering by category

### Shopping Cart
- [ ] Add to cart
- [ ] View cart
- [ ] Update quantity
- [ ] Remove item from cart

### Checkout
- [ ] Shipping address form
- [ ] Payment processing (Stripe)
- [ ] Order confirmation
- [ ] Order confirmation email

## Out-of-Scope

### Deferred to Phase 2
- Social login (Google, Facebook)
- User reviews and ratings
- Wishlist functionality
- Product recommendations
- Multi-language support

### Not in Scope
- Mobile app (web only)
- Multi-currency support
- Gift cards
- Loyalty program

## Assumptions

| Assumption | Impact | Validation | Owner |
|------------|--------|------------|-------|
| Users have modern browsers | Need polyfills if false | Check analytics | PM |
| Stripe API available | Need alternative if false | Test integration | Dev |
| Design assets by Week 2 | Delay if false | Confirm with design | PM |

## Dependencies

| Dependency | Critical | Owner | Status | Contingency |
|------------|----------|-------|--------|-------------|
| Design assets (Week 2) | Yes | Design Lead | On track | Use wireframes |
| Stripe integration | Yes | Backend Dev | On track | PayPal fallback |
| Product data migration | Yes | Data Eng | At risk | Manual entry |

## Constraints

### Budget
- Total: $50,000
- Development: $35,000
- Infrastructure: $10,000
- Contingency: $5,000

### Timeline
- Start: [Date]
- End: [Date] (hard deadline)
- Duration: 12 weeks

### Resources
- Team: 2 developers, 1 designer, 1 PM
- No dedicated QA (developers will test)

### Technical
- Must use React + Node.js
- Must integrate with existing authentication system
- Must support Chrome, Firefox, Safari, Edge

## Success Criteria
- [ ] Users can complete purchase flow end-to-end
- [ ] Page load time < 3 seconds (P95)
- [ ] Zero critical bugs in production
- [ ] Stakeholder sign-off received

## Change Control
Any changes to this scope require:
1. Impact assessment (time, cost, quality)
2. Stakeholder approval
3. Updated scope document

## Sign-Off
[ ] Product Owner: _________________ Date: _______
[ ] Tech Lead: _____________________ Date: _______
[ ] Project Manager: ________________ Date: _______
```

---

## Handling Scope Creep

Scope creep is the uncontrolled expansion of project scope. Manage it proactively.

### Scope Creep Detection

| Sign | Example |
|------|---------|
| "Just one more thing" | Adding features mid-project |
| "It's quick" | Underestimating effort |
| "We need it" | Emotional urgency without analysis |
| "While you're at it" | Adding related features |
| "It's related" | Expanding scope loosely |

### Scope Change Process

```
1. Document the change request
   - What is being requested?
   - Why is it needed?
   - Who is requesting it?

2. Assess impact
   - How much effort? (time estimate)
   - What's the cost? (budget impact)
   - What's the risk? (quality, timeline)

3. Re-prioritize
   - What gets deferred to accommodate this?
   - What's the trade-off?

4. Get approval
   - Stakeholder sign-off on change
   - Document the decision

5. Update scope document
   - Add to in-scope (if approved)
   - Move something to out-of-scope (if trade-off)
   - Update timeline and budget
```

### Change Request Template

```
Change Request # [Number]

Requested by: [Name]
Date: [Date]

Description:
[What is being requested?]

Rationale:
[Why is this needed?]

Impact Assessment:
- Effort: [hours/days]
- Cost: [$ amount]
- Timeline impact: [delay]
- Quality impact: [risk]

Trade-offs:
[What will be deferred or removed?]

Recommendation:
[ ] Approve - [Reason]
[ ] Reject - [Reason]
[ ] Defer to Phase [X] - [Reason]

Approval:
Product Owner: _________________ Date: _______
Tech Lead: _____________________ Date: _______
```

---

## Communicating Scope

Clear communication prevents misunderstandings.

### Written Scope Document

- Share with all stakeholders
- Use clear, specific language
- Include visuals (diagrams, mockups)
- Version control changes

### Kickoff Meeting

- Present scope document
- Walk through in-scope items
- Explain out-of-scope items
- Discuss assumptions and dependencies
- Get questions answered

### Regular Check-ins

- Weekly scope review
- Confirm alignment
- Flag potential scope creep early
- Update if changes approved

### Visual Scope

- User story map (see below)
- Feature matrix
- Roadmap visualization
- Kanban board with scope columns

---

## User Story Mapping

Visualize scope as a user journey.

### Structure

```
Horizontal (Left to Right): User flow / Narrative
Vertical (Top to Bottom): Priority

Top row = MVP (Must have)
Middle rows = Should have
Bottom rows = Could have
```

### Example: E-Commerce User Story Map

```
                    Browse Products    Add to Cart    Checkout    Order Complete
Must Have         [Product List]    [Add Item]    [Payment]    [Confirmation]
                  [Search]          [View Cart]   [Shipping]
                  [Filter]

Should Have       [Categories]      [Quantity]    [Saved Addresses]
                  [Compare]          [Remove]      [Order History]

Could Have        [Reviews]          [Wishlist]    [Gift Options]
                  [Recommendations]  [Quick Add]   [Multiple Addresses]
```

### Benefits of User Story Mapping

- Visual representation of scope
- Easy to see MVP (top row)
- Shows user journey flow
- Facilitates prioritization discussions
- Identifies gaps in the user experience

---

## Scope Negotiation

Stakeholders often want everything. Negotiate effectively.

### The Iron Triangle

```
       Quality
          /\
         /  \
        /    \
   Time  ----  Cost
```

You can't have all three. Trade-offs are necessary.

### Negotiation Framework

1. **Acknowledge the request**
   - "I understand you want feature X"

2. **Explain constraints**
   - "Given our timeline and budget, we can't do everything"

3. **Offer options**
   - "We can do X now and Y in Phase 2, or Y now and X in Phase 2"

4. **Prioritize together**
   - "Which is more important to you: X or Y?"

5. **Document the decision**
   - Update scope document

### Example Dialogue

```
Stakeholder: "We need social login, reviews, and recommendations."

You: "I understand. Those are all valuable features. However, given our
     12-week timeline and $50k budget, we need to prioritize. Let me show
     you what fits in MVP."

Stakeholder: "What do you suggest?"

You: "For MVP, I recommend core e-commerce functionality: browse, cart,
     checkout. Social login, reviews, and recommendations can be Phase 2.
     This way we get to market faster and gather user feedback before
     investing in those features."

Stakeholder: "That makes sense. Let's do that."
```

---

## MVP Scoping

MVP (Minimum Viable Product) is the smallest scope that delivers value.

### MVP Principles

1. **Core value proposition only**
   - What's the one thing users must be able to do?

2. **Remove nice-to-haves**
   - Defer everything that's not essential

3. **Simplify**
   - Basic version first, enhance later

4. **Test assumptions**
   - MVP is for learning, not perfection

### MVP Scoping Examples

| Project | MVP | Nice-to-Haves (Defer) |
|---------|-----|----------------------|
| **E-commerce** | Browse + checkout | Reviews, recommendations, wishlist |
| **Task app** | Create + complete tasks | Tags, reminders, collaboration |
| **Chat app** | 1-on-1 messaging | Groups, file sharing, reactions |
| **Blog** | Read + write posts | Comments, categories, search |

### MVP Checklist

```
MVP Scoping Checklist:

Core Value:
[ ] Does this solve the primary user problem?
[ ] Can users accomplish their main goal?

Essential Only:
[ ] Have we removed all nice-to-haves?
[ ] Is everything else deferred to future phases?

Simplified:
[ ] Can we simplify any features?
[ ] Are we using the simplest approach?

Testable:
[ ] Can we validate our assumptions with this scope?
[ ] Will we learn what we need to learn?

Timeboxed:
[ ] Can we build this in our timeline?
[ ] Is the effort realistic for our team?
```

---

## Phased Delivery

Break large projects into manageable phases.

### Phase Structure

```
Phase 1 (MVP): Core functionality
- Must-have features only
- Delivers primary value
- Time: [duration]

Phase 2: Enhanced features
- Should-have features
- Improves user experience
- Time: [duration]

Phase 3: Advanced features
- Could-have features
- Delighters and optimizations
- Time: [duration]
```

### Example: E-Commerce Phases

**Phase 1 (MVP - 8 weeks)**
- Product browsing
- Shopping cart
- Checkout with Stripe
- Order confirmation
- Basic user accounts

**Phase 2 (Enhancement - 6 weeks)**
- User reviews and ratings
- Wishlist functionality
- Order history
- Email notifications
- Product search

**Phase 3 (Advanced - 8 weeks)**
- Product recommendations
- Social login
- Gift cards
- Loyalty program
- Multi-language support

### Phase Documentation

```markdown
# Project Phases: [Project Name]

## Phase 1: MVP
**Timeline:** [Start] - [End]
**Goal:** [Primary goal]

In-Scope:
- [Feature 1]
- [Feature 2]

Out-of-Scope:
- [Feature A] → Phase 2
- [Feature B] → Phase 3

## Phase 2: Enhancement
**Timeline:** [Start] - [End]
**Goal:** [Goal]

In-Scope:
- [Feature A]
- [Feature C]

Out-of-Scope:
- [Feature B] → Phase 3

## Phase 3: Advanced
**Timeline:** [Start] - [End]
**Goal:** [Goal]

In-Scope:
- [Feature B]
- [Feature D]
```

---

## Red Flags in Scoping

Watch for these warning signs.

| Red Flag | Problem | Solution |
|----------|---------|----------|
| "Everything is must-have" | No prioritization | Use MoSCoW framework |
| "We'll figure it out later" | Deferred decisions | Push for clarity now |
| Scope keeps changing | No change control | Implement change process |
| No out-of-scope documented | Ambiguous boundaries | Explicitly document |
| Assumptions not validated | Hidden risks | Validate early |
| Dependencies not tracked | Surprise delays | Map and monitor |
| No success criteria | Can't measure completion | Define clear metrics |

---

## Scope Approval

Formal sign-off establishes the baseline.

### Approval Process

1. **Draft scope document**
   - Include all sections
   - Be specific and clear

2. **Review with stakeholders**
   - Walk through in-scope
   - Explain out-of-scope
   - Discuss assumptions

3. **Get feedback**
   - Address concerns
   - Make adjustments

4. **Final sign-off**
   - Document approval
   - Establish baseline

### Sign-Off Template

```
Scope Approval

Project: [Project Name]
Scope Version: [Version]
Date: [Date]

I have reviewed and approved the scope document as defined above.

Approved In-Scope:
[ ] I confirm the in-scope items are accurate
[ ] I understand the out-of-scope items
[ ] I agree to the assumptions and dependencies

Approvals:

Product Owner: ____________________ Date: _______
Signature: _________________________

Tech Lead: _________________________ Date: _______
Signature: _________________________

Project Manager: ____________________ Date: _______
Signature: _________________________

Stakeholder: _______________________ Date: _______
Signature: _________________________

This scope document serves as the baseline for the project.
Any changes require formal change control.
```

---

## Real Scoping Examples

### Example 1: E-Commerce Project Scope

```markdown
# Scope: Online Store MVP

## In-Scope

### User Features
- User registration (email/password)
- User login
- Password reset
- View product catalog
- Search products
- Filter by category
- View product details
- Add to cart
- View cart
- Update quantity
- Remove from cart
- Checkout (shipping + payment)
- Order confirmation
- View order history

### Admin Features
- Add/edit/delete products
- Manage product categories
- View orders
- Update order status

### Technical
- Stripe payment integration
- SendGrid email notifications
- PostgreSQL database
- React frontend
- Node.js backend

## Out-of-Scope

### Deferred to Phase 2
- User reviews and ratings
- Wishlist
- Product recommendations
- Social login
- Multi-currency
- Gift cards
- Loyalty program

### Not in Scope
- Mobile app
- Multi-language support
- Vendor marketplace
- Auction functionality

## Assumptions
- Users have modern browsers
- Stripe API available
- Product data provided by client
- No more than 10,000 products initially

## Dependencies
- Design assets by Week 2
- Stripe account setup
- Product data migration

## Constraints
- Budget: $50,000
- Timeline: 12 weeks
- Team: 2 developers, 1 designer
```

### Example 2: Internal Dashboard Scope

```markdown
# Scope: Analytics Dashboard

## In-Scope

### Data Sources
- Connect to Google Analytics
- Connect to database (sales data)
- Connect to CRM (customer data)

### Dashboard Views
- Overview dashboard (key metrics)
- Sales dashboard (revenue, orders)
- Customer dashboard (acquisition, retention)
- Traffic dashboard (visitors, sources)

### Features
- Date range selector
- Export to CSV
- Refresh data button
- Basic filters

### Technical
- React frontend
- Python backend (FastAPI)
- PostgreSQL
- Scheduled data refresh (daily)

## Out-of-Scope

### Deferred to Phase 2
- Custom report builder
- Alert notifications
- Data drill-down
- Multiple user roles
- SSO integration

### Not in Scope
- Real-time data
- Mobile app
- White-labeling
- API access

## Assumptions
- GA API access available
- Database access available
- Daily refresh acceptable (not real-time)

## Dependencies
- GA API credentials
- Database credentials
- CRM API access

## Constraints
- Budget: $30,000
- Timeline: 8 weeks
- Team: 1 developer, 1 designer
```

### Example 3: API Integration Scope

```markdown
# Scope: Payment Gateway Integration

## In-Scope

### Integration
- Connect to [Payment Provider] API
- Implement payment processing
- Handle payment success
- Handle payment failure
- Implement webhooks for payment status

### Features
- Create payment intent
- Process payment
- Refund payment
- Get payment status
- List transactions

### Error Handling
- API timeout handling
- Retry logic for transient failures
- Error logging
- User-friendly error messages

### Technical
- Node.js backend integration
- API client library
- Database for payment records
- Webhook endpoint

## Out-of-Scope

### Deferred to Phase 2
- Multiple payment methods
- Subscription billing
- Payment plans
- Dispute handling
- Advanced fraud detection

### Not in Scope
- Mobile SDK integration
- Alternative payment providers
- Custom payment forms

## Assumptions
- Payment provider API is stable
- Webhooks are reliable
- API rate limits sufficient

## Dependencies
- Payment provider account setup
- API keys and credentials
- Webhook endpoint configuration

## Constraints
- Budget: $15,000
- Timeline: 4 weeks
- Team: 1 backend developer
```

---

## Templates

### Scope Document Template

```markdown
# Scope Document: [Project Name]

**Version:** 1.0
**Date:** [Date]
**Author:** [Name]

## Project Overview
[Description]

## Goals
1. [Goal 1]
2. [Goal 2]

## In-Scope

### [Category 1]
- [ ] [Feature 1]
- [ ] [Feature 2]

### [Category 2]
- [ ] [Feature 3]
- [ ] [Feature 4]

## Out-of-Scope

### Deferred to Phase 2
- [Feature A]
- [Feature B]

### Not in Scope
- [Feature X]
- [Feature Y]

## Assumptions

| Assumption | Impact | Validation | Owner |
|------------|--------|------------|-------|
| [Assumption 1] | [Impact] | [How to validate] | [Owner] |
| [Assumption 2] | [Impact] | [How to validate] | [Owner] |

## Dependencies

| Dependency | Critical | Owner | Status | Contingency |
|------------|----------|-------|--------|-------------|
| [Dependency 1] | Yes/No | [Owner] | [Status] | [Plan B] |
| [Dependency 2] | Yes/No | [Owner] | [Status] | [Plan B] |

## Constraints

### Budget
- Total: $[amount]

### Timeline
- Start: [date]
- End: [date]
- Duration: [weeks]

### Resources
- Team: [composition]
- Tools: [list]

### Technical
- Must use: [technologies]
- Must integrate with: [systems]

## Success Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Change Control
Any changes require:
1. Impact assessment
2. Stakeholder approval
3. Updated scope document

## Sign-Off
[ ] Product Owner: _________________ Date: _______
[ ] Tech Lead: _____________________ Date: _______
[ ] Project Manager: ________________ Date: _______
```

### Prioritization Matrix Template

```
Value vs Effort Matrix

High Value, Low Effort (DO FIRST):
- [Feature 1] - [Value: 9, Effort: 3]
- [Feature 2] - [Value: 8, Effort: 2]

High Value, High Effort (CONSIDER):
- [Feature 3] - [Value: 9, Effort: 8]
- [Feature 4] - [Value: 7, Effort: 7]

Low Value, Low Effort (MAYBE):
- [Feature 5] - [Value: 3, Effort: 2]
- [Feature 6] - [Value: 4, Effort: 3]

Low Value, High Effort (DON'T DO):
- [Feature 7] - [Value: 2, Effort: 8]
- [Feature 8] - [Value: 1, Effort: 7]
```

### User Story Map Template

```
User Story Map: [Project Name]

                    [Step 1]    [Step 2]    [Step 3]    [Step 4]
Must Have         [Story A]    [Story B]    [Story C]    [Story D]
                  [Story E]

Should Have       [Story F]    [Story G]    [Story H]
                               [Story I]

Could Have        [Story J]                 [Story K]
                  [Story L]    [Story M]
```

### Change Request Template

```
Change Request

Requested by: [Name]
Date: [Date]
Project: [Project Name]

Description:
[What is being requested?]

Rationale:
[Why is this needed?]

Impact Assessment:
- Effort: [hours/days/weeks]
- Cost: [$ amount]
- Timeline impact: [delay]
- Quality impact: [risk]

Trade-offs:
[What will be deferred or removed?]

Recommendation:
[ ] Approve
[ ] Reject
[ ] Defer to Phase [X]

Approval:
Product Owner: _________________ Date: _______
Tech Lead: _____________________ Date: _______
```

---

## Best Practices

1. **Be specific** - Clear, unambiguous scope items
2. **Document out-of-scope** - Explicitly state what's excluded
3. **Validate assumptions** - Don't assume, verify
4. **Track dependencies** - Monitor external factors
5. **Get sign-off** - Formal approval establishes baseline
6. **Control changes** - Use change process for modifications
7. **Communicate clearly** - Share scope with all stakeholders
8. **Review regularly** - Confirm scope alignment throughout project
9. **Learn from experience** - Use lessons learned for future projects
10. **Be realistic** - Don't overpromise, underdeliver

---

## Related Skills

- [Discovery Questions](../discovery-questions/SKILL.md) - Gather requirements before scoping
- [Acceptance Criteria](../acceptance-criteria/SKILL.md) - Define done criteria
- [Constraints and Assumptions](../constraints-and-assumptions/SKILL.md) - Document constraints
- [Risk and Dependencies](../risk-and-dependencies/SKILL.md) - Manage dependencies
