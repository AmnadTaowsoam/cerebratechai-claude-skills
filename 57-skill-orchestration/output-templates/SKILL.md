# Output Templates

## Overview

Output templates are structured formats for project deliverables. They ensure consistency, completeness, and clear communication across all projects.

## What Are Output Templates

Output templates are:

- **Structured formats** for deliverables
- **Consistent presentation** - same format across projects
- **Reusable** - use templates for similar work
- **Complete** - don't forget important sections

## Why Templates Matter

| Benefit | Description |
|---------|-------------|
| **Consistency** - Same format across all projects |
| **Completeness** - Don't forget important sections |
| **Communication clarity** - Clear, organized information |
| **Time-saving** - Start with template, fill in details |
| **Quality** - Ensures all required information is included |

---

## Key Output Templates

### 1. skill-stack.md

Documents skills used for a project.

### 2. backlog.md

Lists user stories and tasks.

### 3. requirements.md

Full requirements documentation.

### 4. architecture.md

Technical design documentation.

### 5. deployment.md

Deployment plan documentation.

---

## skill-stack.md Template

Documents which skills were used for a project.

```markdown
# Skill Stack for [Project Name]

**Version:** 1.0
**Date:** [Date]
**Author:** [Name]

## Must-Have Skills

### Core Skills
- [ ] [skill-1] - [Brief description]
- [ ] [skill-2] - [Brief description]
- [ ] [skill-3] - [Brief description]

### Domain Skills
- [ ] [skill-4] - [Brief description]
- [ ] [skill-5] - [Brief description]

## Recommended Skills

- [ ] [skill-6] - [Brief description]
- [ ] [skill-7] - [Brief description]
- [ ] [skill-8] - [Brief description]

## Optional Skills

- [ ] [skill-9] - [Brief description]
- [ ] [skill-10] - [Brief description]

## Skill Application Notes

### [Skill 1]
- How applied: [Description]
- Key decisions: [List]
- Lessons learned: [List]

### [Skill 2]
- How applied: [Description]
- Key decisions: [List]
- Lessons learned: [List]

## Skill Gaps

Skills that would have been helpful but weren't used:
- [skill-11] - [Reason not used]
- [skill-12] - [Reason not used]

## References

- [Link to skill 1]
- [Link to skill 2]
- [Link to skill 3]
```

### Example skill-stack.md

```markdown
# Skill Stack for E-Commerce Platform

**Version:** 1.0
**Date:** 2024-01-15
**Author:** John Doe

## Must-Have Skills

### Core Skills
- [x] api-design - REST API patterns and conventions
- [x] authentication-jwt - JWT-based user authentication
- [x] database-design - PostgreSQL schema design
- [x] error-handling - Consistent error handling patterns

### Domain Skills
- [x] payment-security - PCI-DSS compliance for payments
- [x] shopping-cart - Cart state management
- [x] product-catalog - Product data modeling

## Recommended Skills

- [x] caching-strategies - Redis caching for performance
- [x] rate-limiting - API rate limiting
- [x] monitoring - Application monitoring and alerting

## Optional Skills

- [ ] webhooks - Event notifications (deferred to Phase 2)
- [ ] graphql - GraphQL API (not needed for MVP)

## Skill Application Notes

### api-design
- How applied: Used REST conventions, resource-based URLs
- Key decisions:
  - Used URL versioning (/v1/)
  - Implemented cursor-based pagination
  - Standardized error response format
- Lessons learned:
  - OpenAPI documentation saved time
  - Early API design prevented rework

### authentication-jwt
- How applied: JWT with 15-minute access tokens
- Key decisions:
  - Used refresh tokens for better UX
  - Implemented token rotation
  - Stored only token hashes in database
- Lessons learned:
  - Short access tokens improve security
  - Refresh token rotation is complex but worth it

### database-design
- How applied: Normalized schema with proper indexes
- Key decisions:
  - Used UUIDs for primary keys
  - Implemented soft deletes
  - Added created_at/updated_at timestamps
- Lessons learned:
  - Proper indexing critical for performance
  - Soft deletes simplify data recovery

## Skill Gaps

Skills that would have been helpful but weren't used:
- testing - Limited time, focused on manual testing
- accessibility - Not prioritized for MVP, will add later

## References

- [api-design](../../03-backend-api/api-design/SKILL.md)
- [authentication-jwt](../../10-authentication-authorization/authentication-jwt/SKILL.md)
- [database-design](../../04-database/database-design/SKILL.md)
```

---

## backlog.md Template

Lists user stories and tasks for a project.

```markdown
# Project Backlog: [Project Name]

**Version:** 1.0
**Date:** [Date]
**Author:** [Name]

## Epic: [Epic Name]

### User Story 1: [Story Name]

**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Tasks:**
- [ ] [Task 1]
- [ ] [Task 2]
- [ ] [Task 3]

**Skills Used:** [skill-1], [skill-2]
**Estimate:** [story points or days]
**Priority:** Must-have/Should-have/Could-have
**Status:** [Todo/In Progress/Done]

### User Story 2: [Story Name]

**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Tasks:**
- [ ] [Task 1]
- [ ] [Task 2]

**Skills Used:** [skill-1], [skill-3]
**Estimate:** [story points or days]
**Priority:** Must-have/Should-have/Could-have
**Status:** [Todo/In Progress/Done]

## Epic: [Epic Name]

### User Story 3: [Story Name]

**As a** [user type]
**I want to** [action]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Tasks:**
- [ ] [Task 1]
- [ ] [Task 2]

**Skills Used:** [skill-2], [skill-4]
**Estimate:** [story points or days]
**Priority:** Must-have/Should-have/Could-have
**Status:** [Todo/In Progress/Done]

## Backlog Summary

| Epic | Stories | Total Estimate | Completed | Remaining |
|------|---------|---------------|-----------|-----------|
| [Epic 1] | [number] | [estimate] | [estimate] | [estimate] |
| [Epic 2] | [number] | [estimate] | [estimate] | [estimate] |

## Sprint Planning

### Current Sprint
**Sprint:** [Sprint number]
**Dates:** [Start date] - [End date]

**Stories:**
- [Story 1] - [Estimate]
- [Story 2] - [Estimate]

**Total Estimate:** [Total]

### Upcoming Sprints
**Sprint [N+1]:**
- [Story 3] - [Estimate]
- [Story 4] - [Estimate]
```

### Example backlog.md

```markdown
# Project Backlog: E-Commerce Platform

**Version:** 1.0
**Date:** 2024-01-15
**Author:** John Doe

## Epic: User Management

### User Story 1: User Registration

**As a** new user
**I want to** register with email and password
**So that** I can create an account

**Acceptance Criteria:**
- [ ] User can enter email and password
- [ ] Email is validated (format check)
- [ ] Password meets requirements (8+ chars, mix)
- [ ] Confirmation email sent
- [ ] User redirected to dashboard

**Tasks:**
- [ ] Design registration form
- [ ] Implement email validation
- [ ] Implement password validation
- [ ] Implement user creation API
- [ ] Implement email sending
- [ ] Write tests

**Skills Used:** authentication-jwt, email-sending, testing
**Estimate:** 5 story points
**Priority:** Must-have
**Status:** Done

### User Story 2: User Login

**As a** registered user
**I want to** log in with email and password
**So that** I can access my account

**Acceptance Criteria:**
- [ ] User can enter email and password
- [ ] Invalid credentials show error
- [ ] Successful login redirects to dashboard
- [ ] Session is maintained

**Tasks:**
- [ ] Design login form
- [ ] Implement authentication API
- [ ] Implement session management
- [ ] Write tests

**Skills Used:** authentication-jwt, error-handling, testing
**Estimate:** 3 story points
**Priority:** Must-have
**Status:** Done

### User Story 3: Password Reset

**As a** user
**I want to** reset my password
**So that** I can regain access to my account

**Acceptance Criteria:**
- [ ] User can request password reset
- [ ] Reset link sent to email
- [ ] Link expires after 24 hours
- [ ] User can set new password

**Tasks:**
- [ ] Design forgot password flow
- [ ] Implement password reset API
- [ ] Implement email sending
- [ ] Write tests

**Skills Used:** authentication-jwt, email-sending, security
**Estimate:** 5 story points
**Priority:** Should-have
**Status:** In Progress

## Epic: Product Catalog

### User Story 4: Product Listing

**As a** customer
**I want to** browse products
**So that** I can find what I want to buy

**Acceptance Criteria:**
- [ ] Products displayed in grid/list
- [ ] Pagination (20 products per page)
- [ ] Filter by category
- [ ] Search by name

**Tasks:**
- [ ] Design product listing page
- [ ] Implement product API
- [ ] Implement pagination
- [ ] Implement filtering
- [ ] Implement search
- [ ] Write tests

**Skills Used:** api-design, database-design, caching-strategies
**Estimate:** 8 story points
**Priority:** Must-have
**Status:** Todo

## Backlog Summary

| Epic | Stories | Total Estimate | Completed | Remaining |
|------|---------|---------------|-----------|-----------|
| User Management | 3 | 13 | 8 | 5 |
| Product Catalog | 1 | 8 | 0 | 8 |

## Sprint Planning

### Current Sprint
**Sprint:** 1
**Dates:** 2024-01-15 - 2024-01-29

**Stories:**
- User Story 3: Password Reset - 5 story points
- User Story 4: Product Listing - 8 story points

**Total Estimate:** 13 story points

### Upcoming Sprints
**Sprint 2:**
- User Story 5: Product Details - 5 story points
- User Story 6: Shopping Cart - 8 story points
```

---

## requirements.md Template

Full requirements documentation for a project.

```markdown
# Requirements: [Project Name]

**Version:** 1.0
**Date:** [Date]
**Author:** [Name]

## Overview
[Brief description of the project]

## Goals and Objectives

### Primary Goals
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

### Success Criteria
- [ ] [Success criterion 1]
- [ ] [Success criterion 2]
- [ ] [Success criterion 3]

## Functional Requirements

### FR-1: [Requirement Name]
**Description:** [Description]
**Priority:** Must-have/Should-have/Could-have
**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### FR-2: [Requirement Name]
**Description:** [Description]
**Priority:** Must-have/Should-have/Could-have
**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Non-Functional Requirements

### NFR-1: [Requirement Name]
**Description:** [Description]
**Priority:** Must-have/Should-have/Could-have
**Metric:** [Specific metric]

### NFR-2: [Requirement Name]
**Description:** [Description]
**Priority:** Must-have/Should-have/Could-have
**Metric:** [Specific metric]

## Constraints

### Budget
- Total: $[amount]
- Breakdown: [details]

### Timeline
- Start: [date]
- End: [date]
- Milestones: [list]

### Resources
- Team: [composition]
- Tools: [list]

### Technical
- Must use: [technologies]
- Must integrate with: [systems]
- Must support: [platforms]

### Legal/Compliance
- [Regulation 1]: [requirements]
- [Regulation 2]: [requirements]

## Assumptions

- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

## Dependencies

| Dependency | Owner | Status | Critical | Due Date |
|------------|-------|--------|----------|----------|
| [Dep 1] | [Name] | [Status] | Yes/No | [Date] |
| [Dep 2] | [Name] | [Status] | Yes/No | [Date] |

## Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| [Risk 1] | [L/M/H] | [L/M/H/C] | [Mitigation] | [Name] |
| [Risk 2] | [L/M/H] | [L/M/H/C] | [Mitigation] | [Name] |

## Out of Scope

- [Item 1] - [Reason]
- [Item 2] - [Reason]

## Appendices

### User Personas
[Description of user personas]

### Use Cases
[Description of use cases]

### Glossary
[Definition of terms]
```

### Example requirements.md

```markdown
# Requirements: E-Commerce Platform

**Version:** 1.0
**Date:** 2024-01-15
**Author:** John Doe

## Overview
An online e-commerce platform for selling products to customers. The platform will support product browsing, shopping cart, checkout, and user account management.

## Goals and Objectives

### Primary Goals
1. Enable customers to browse and purchase products online
2. Provide a secure and seamless checkout experience
3. Support user account management
4. Enable order tracking and management

### Success Criteria
- [ ] 100+ products available for purchase
- [ ] 50+ successful transactions in first month
- [ ] Page load time < 3 seconds (P95)
- [ ] Zero critical security vulnerabilities

## Functional Requirements

### FR-1: User Registration
**Description:** Users must be able to register for an account using email and password
**Priority:** Must-have
**Acceptance Criteria:**
- [ ] User can enter email and password
- [ ] Email format is validated
- [ ] Password meets requirements (8+ chars, mixed types)
- [ ] Confirmation email is sent
- [ ] User is redirected to dashboard

### FR-2: User Login
**Description:** Registered users must be able to log in with email and password
**Priority:** Must-have
**Acceptance Criteria:**
- [ ] User can enter email and password
- [ ] Invalid credentials show error message
- [ ] Successful login redirects to dashboard
- [ ] Session is maintained

### FR-3: Product Browsing
**Description:** Customers must be able to browse products
**Priority:** Must-have
**Acceptance Criteria:**
- [ ] Products displayed in grid/list view
- [ ] Pagination (20 products per page)
- [ ] Filter by category
- [ ] Search by product name

### FR-4: Shopping Cart
**Description:** Customers must be able to add products to cart
**Priority:** Must-have
**Acceptance Criteria:**
- [ ] User can add product to cart
- [ ] User can view cart
- [ ] User can update quantity
- [ ] User can remove item from cart

### FR-5: Checkout
**Description:** Customers must be able to complete purchase
**Priority:** Must-have
**Acceptance Criteria:**
- [ ] User enters shipping information
- [ ] User enters payment information
- [ ] Payment is processed securely
- [ ] Order confirmation is displayed
- [ ] Confirmation email is sent

## Non-Functional Requirements

### NFR-1: Performance
**Description:** System must perform well under expected load
**Priority:** Must-have
**Metric:**
- Page load time: P95 < 3 seconds
- API response time: P95 < 200ms
- Support 10,000 concurrent users

### NFR-2: Security
**Description:** System must be secure and protect user data
**Priority:** Must-have
**Metric:**
- HTTPS only
- PCI-DSS compliant
- No critical vulnerabilities
- Regular security audits

### NFR-3: Availability
**Description:** System must be highly available
**Priority:** Must-have
**Metric:**
- 99.9% uptime
- Automated failover
- Disaster recovery plan

### NFR-4: Scalability
**Description:** System must scale to meet demand
**Priority:** Should-have
**Metric:**
- Horizontal scaling capability
- Auto-scaling based on load
- Handle 10x growth

## Constraints

### Budget
- Total: $50,000
- Development: $35,000
- Infrastructure: $10,000
- Third-party: $5,000

### Timeline
- Start: 2024-01-15
- End: 2024-04-15 (3 months)
- Milestones:
  - Week 4: Design complete
  - Week 8: MVP complete
  - Week 10: Testing complete
  - Week 12: Launch

### Resources
- Team: 2 developers, 1 designer, 1 PM
- Tools: React, Node.js, PostgreSQL, AWS

### Technical
- Must use: React 18, Node.js 18, PostgreSQL 14
- Must integrate with: Stripe (payments), SendGrid (email)
- Must support: Chrome, Firefox, Safari, Edge

### Legal/Compliance
- PCI-DSS: Yes (payment processing)
- GDPR: Yes (EU users)
- WCAG 2.1: Yes (accessibility)

## Assumptions

- Users have modern browsers (Chrome 90+, Firefox 88+, Safari 14+)
- Users have internet connection
- Stripe API will be available and reliable
- Product data is accurate and complete
- Design team will provide assets by Week 2

## Dependencies

| Dependency | Owner | Status | Critical | Due Date |
|------------|-------|--------|----------|----------|
| UI Mockups | Design Agency | On Track | Yes | Week 2 |
| Stripe Account | PM | Complete | Yes | Week 1 |
| Product Data | Client | Delayed | Yes | Week 4 |
| SendGrid Account | PM | Complete | Yes | Week 1 |

## Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| Stripe API changes | Medium | High | Abstraction layer | Dev |
| Design delayed | Medium | High | Wireframes as backup | PM |
| Performance issues | Medium | Critical | Load testing early | Dev |
| Scope creep | High | High | Strict change control | PM |

## Out of Scope

- Social login (Google, Facebook) - Defer to Phase 2
- User reviews and ratings - Defer to Phase 2
- Wishlist functionality - Defer to Phase 2
- Product recommendations - Defer to Phase 2
- Multi-language support - Defer to Phase 2
- Mobile app - Web only for MVP

## Appendices

### User Personas

**Primary User: Sarah (Customer)**
- Age: 28
- Tech-savvy: Yes
- Goals: Browse products, make purchases, track orders
- Pain points: Slow checkout, confusing navigation

**Secondary User: Admin (Store Manager)**
- Age: 35
- Tech-savvy: Yes
- Goals: Manage products, view orders, update inventory
- Pain points: Complex admin interface

### Use Cases

**UC-1: Browse Products**
1. User navigates to home page
2. User views product listings
3. User filters by category
4. User searches for product
5. User views product details

**UC-2: Complete Purchase**
1. User adds product to cart
2. User views cart
3. User proceeds to checkout
4. User enters shipping info
5. User enters payment info
6. User completes purchase
7. User receives confirmation

### Glossary

- **SKU:** Stock Keeping Unit - unique identifier for products
- **PCI-DSS:** Payment Card Industry Data Security Standard
- **P95:** 95th percentile - 95% of requests complete within this time
```

---

## architecture.md Template

Technical design documentation for a project.

```markdown
# Architecture: [Project Name]

**Version:** 1.0
**Date:** [Date]
**Author:** [Name]

## System Overview
[High-level description of the system]

## Architecture Diagram
[Diagram or ASCII art]

## Components

### Frontend
- **Tech:** [Technology stack]
- **Hosting:** [Hosting provider]
- **Responsibilities:** [List]

### Backend
- **Tech:** [Technology stack]
- **Hosting:** [Hosting provider]
- **Responsibilities:** [List]

### Database
- **Tech:** [Technology]
- **Hosting:** [Hosting provider]
- **Schema:** [Description]

### [Other Components]
- **Tech:** [Technology]
- **Hosting:** [Hosting provider]
- **Responsibilities:** [List]

## API Design

### API Style
- [REST/GraphQL/gRPC]

### Authentication
- [Method: JWT, OAuth, etc.]

### Endpoints
| Method | Endpoint | Description | Auth |
|--------|-----------|-------------|-------|
| [GET] | [/path] | [Description] | [Yes/No] |
| [POST] | [/path] | [Description] | [Yes/No] |

### Error Responses
```json
{
  "error": {
    "code": "[code]",
    "message": "[message]"
  }
}
```

## Data Flow

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Security Considerations

- [Security consideration 1]
- [Security consideration 2]
- [Security consideration 3]

## Performance Considerations

- [Performance consideration 1]
- [Performance consideration 2]
- [Performance consideration 3]

## Scalability Considerations

- [Scalability consideration 1]
- [Scalability consideration 2]

## Deployment Architecture

### Environments
- **Development:** [Description]
- **Staging:** [Description]
- **Production:** [Description]

### Infrastructure
- [Infrastructure component 1]
- [Infrastructure component 2]

## Technology Decisions

### [Decision 1]
**Decision:** [What was decided]
**Alternatives Considered:** [List]
**Rationale:** [Why this decision]
**Trade-offs:** [What was traded]

### [Decision 2]
**Decision:** [What was decided]
**Alternatives Considered:** [List]
**Rationale:** [Why this decision]
**Trade-offs:** [What was traded]
```

### Example architecture.md

```markdown
# Architecture: E-Commerce Platform

**Version:** 1.0
**Date:** 2024-01-15
**Author:** John Doe

## System Overview
A web-based e-commerce platform consisting of a React frontend, Node.js backend, and PostgreSQL database. The platform supports product browsing, shopping cart, checkout, and user account management.

## Architecture Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │────▶│  Database   │
│   (React)   │     │  (Node.js)  │     │(PostgreSQL) │
└─────────────┘     └─────────────┘     └─────────────┘
       │                   │
       │                   ▼
       │            ┌─────────────┐
       │            │    Redis    │
       │            │   (Cache)   │
       │            └─────────────┘
       │
       ▼
┌─────────────┐
│   CDN       │
│  (CloudFlare)│
└─────────────┘
```

## Components

### Frontend
- **Tech:** React 18, TypeScript, Tailwind CSS
- **Hosting:** Vercel
- **Responsibilities:**
  - User interface
  - Client-side routing
  - State management
  - API communication

### Backend
- **Tech:** Node.js 18, Fastify, TypeScript
- **Hosting:** AWS ECS
- **Responsibilities:**
  - API endpoints
  - Business logic
  - Authentication
  - Data validation

### Database
- **Tech:** PostgreSQL 14
- **Hosting:** AWS RDS
- **Schema:** Normalized with proper indexes
- **Responsibilities:**
  - Data persistence
  - Data integrity
  - Query optimization

### Cache
- **Tech:** Redis 7
- **Hosting:** AWS ElastiCache
- **Responsibilities:**
  - Session storage
  - Product data caching
  - Query result caching

### CDN
- **Tech:** CloudFlare
- **Responsibilities:**
  - Static asset delivery
  - DDoS protection
  - SSL termination

## API Design

### API Style
- RESTful API with JSON responses

### Authentication
- JWT tokens (15-minute access, 7-day refresh)
- Bearer token in Authorization header

### Endpoints
| Method | Endpoint | Description | Auth |
|--------|-----------|-------------|-------|
| POST | /api/v1/auth/register | Register new user | No |
| POST | /api/v1/auth/login | Login user | No |
| POST | /api/v1/auth/logout | Logout user | Yes |
| POST | /api/v1/auth/refresh | Refresh access token | No |
| GET | /api/v1/products | List products | No |
| GET | /api/v1/products/:id | Get product details | No |
| POST | /api/v1/cart/items | Add to cart | Yes |
| GET | /api/v1/cart | Get cart | Yes |
| PUT | /api/v1/cart/items/:id | Update cart item | Yes |
| DELETE | /api/v1/cart/items/:id | Remove from cart | Yes |
| POST | /api/v1/checkout | Create order | Yes |
| GET | /api/v1/orders/:id | Get order details | Yes |

### Error Responses
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "value": "invalid-email"
    }
  }
}
```

## Data Flow

1. User requests page from frontend
2. Frontend fetches data from backend API
3. Backend checks cache (Redis)
4. If cache miss, query database
5. Database returns data
6. Backend caches result in Redis
7. Backend returns data to frontend
8. Frontend renders page

## Security Considerations

- HTTPS only (TLS 1.3)
- JWT tokens with short expiration
- Password hashing with bcrypt (12 rounds)
- Input validation on all endpoints
- SQL injection prevention (parameterized queries)
- XSS prevention (output encoding)
- CORS configuration
- Rate limiting (100 req/min per IP)

## Performance Considerations

- Redis caching for frequently accessed data
- Database connection pooling (max 20)
- CDN for static assets
- Lazy loading for images
- Pagination for large datasets
- Database indexes on frequently queried columns

## Scalability Considerations

- Horizontal scaling for backend (ECS auto-scaling)
- Read replicas for database (RDS read replicas)
- Redis cluster for cache (ElastiCache cluster)
- CDN for global content delivery

## Deployment Architecture

### Environments
- **Development:** Local development with Docker Compose
- **Staging:** AWS ECS with limited resources
- **Production:** AWS ECS with auto-scaling

### Infrastructure
- **VPC:** AWS VPC with public/private subnets
- **Load Balancer:** AWS ALB
- **Container Registry:** AWS ECR
- **CI/CD:** GitHub Actions
- **Monitoring:** CloudWatch, Sentry

## Technology Decisions

### Decision 1: React vs Vue
**Decision:** React
**Alternatives Considered:** Vue, Svelte
**Rationale:**
- Larger ecosystem and community
- More job opportunities
- Team familiarity
- Better TypeScript support

**Trade-offs:**
- Vue has simpler learning curve
- Svelte has better performance
- React has larger bundle size

### Decision 2: PostgreSQL vs MongoDB
**Decision:** PostgreSQL
**Alternatives Considered:** MongoDB, MySQL
**Rationale:**
- Strong data integrity (ACID)
- Better for relational data
- Advanced features (JSON, full-text search)
- Team experience

**Trade-offs:**
- MongoDB has better schema flexibility
- MongoDB scales horizontally more easily
- PostgreSQL has more complex setup

### Decision 3: Fastify vs Express
**Decision:** Fastify
**Alternatives Considered:** Express, Koa
**Rationale:**
- Better performance
- Built-in TypeScript support
- Plugin ecosystem
- Lower overhead

**Trade-offs:**
- Express has larger community
- Express has more middleware
- Koa has more modern async/await
```

---

## deployment.md Template

Deployment plan documentation for a project.

```markdown
# Deployment Plan: [Project Name]

**Version:** 1.0
**Date:** [Date]
**Author:** [Name]

## Deployment Strategy
- [Blue-green deployment]
- [Canary deployment]
- [Rolling deployment]
- [Recreate deployment]

## Environments

### Development
- **URL:** [URL]
- **Purpose:** [Description]
- **Deployment:** [How deployed]

### Staging
- **URL:** [URL]
- **Purpose:** [Description]
- **Deployment:** [How deployed]

### Production
- **URL:** [URL]
- **Purpose:** [Description]
- **Deployment:** [How deployed]

## Pre-Deployment Checklist

### Code Quality
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] No TODO comments without tickets

### Security
- [ ] Security scan clean
- [ ] No hardcoded secrets
- [ ] Dependencies updated (no vulnerabilities)

### Performance
- [ ] Performance tests passed
- [ ] Load tests passed
- [ ] Bundle size optimized

### Testing
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] E2E tests passing
- [ ] Staging environment tested

### Documentation
- [ ] README updated
- [ ] API documentation updated
- [ ] Deployment documentation updated

## Deployment Steps

### Step 1: [Step Name]
**Description:** [What to do]
**Commands:**
```bash
[commands]
```
**Verification:**
- [ ] [Verification step]

### Step 2: [Step Name]
**Description:** [What to do]
**Commands:**
```bash
[commands]
```
**Verification:**
- [ ] [Verification step]

## Rollback Plan

### Rollback Trigger
- [Trigger condition 1]
- [Trigger condition 2]

### Rollback Steps

### Step 1: [Step Name]
**Description:** [What to do]
**Commands:**
```bash
[commands]
```

### Step 2: [Step Name]
**Description:** [What to do]
**Commands:**
```bash
[commands]
```

## Post-Deployment

### Verification
- [ ] Health checks passing
- [ ] Error rates normal
- [ ] Key metrics normal
- [ ] Smoke tests passing

### Monitoring
- [ ] Dashboard configured
- [ ] Alerts configured
- [ ] Logs streaming

### Communication
- [ ] Stakeholders notified
- [ ] Team notified
- [ ] Users notified (if applicable)

## Deployment Schedule

| Environment | Date | Time | Status |
|-------------|------|------|--------|
| Development | [date] | [time] | [status] |
| Staging | [date] | [time] | [status] |
| Production | [date] | [time] | [status] |

## Incident Response

### Contact Information
- **On-call:** [Name] - [Contact]
- **Tech Lead:** [Name] - [Contact]
- **Product Owner:** [Name] - [Contact]

### Runbook
[Link to runbook]

## Appendix

### Environment Variables
[List of required environment variables]

### External Services
[List of external services and their status]

### Dependencies
[List of dependencies and their versions]
```

### Example deployment.md

```markdown
# Deployment Plan: E-Commerce Platform

**Version:** 1.0
**Date:** 2024-01-15
**Author:** John Doe

## Deployment Strategy
- Blue-green deployment with 10% canary

## Environments

### Development
- **URL:** dev.example.com
- **Purpose:** Development and testing
- **Deployment:** Manual deploy to local environment

### Staging
- **URL:** staging.example.com
- **Purpose:** Pre-production testing
- **Deployment:** GitHub Actions to AWS ECS

### Production
- **URL:** www.example.com
- **Purpose:** Production environment
- **Deployment:** GitHub Actions to AWS ECS with canary

## Pre-Deployment Checklist

### Code Quality
- [x] All tests passing
- [x] Code reviewed and approved
- [x] No TODO comments without tickets

### Security
- [x] Security scan clean (Snyk)
- [x] No hardcoded secrets
- [x] Dependencies updated (npm audit)

### Performance
- [x] Performance tests passed (Lighthouse)
- [x] Load tests passed (k6)
- [x] Bundle size optimized (< 200KB)

### Testing
- [x] Unit tests passing (Jest)
- [x] Integration tests passing (Supertest)
- [x] E2E tests passing (Cypress)
- [x] Staging environment tested

### Documentation
- [x] README updated
- [x] API documentation updated (OpenAPI)
- [x] Deployment documentation updated

## Deployment Steps

### Step 1: Build and Push Docker Image
**Description:** Build Docker image and push to ECR
**Commands:**
```bash
docker build -t e-commerce:latest .
docker tag e-commerce:latest [ECR-REPO]/e-commerce:latest
docker push [ECR-REPO]/e-commerce:latest
```
**Verification:**
- [ ] Image pushed successfully

### Step 2: Deploy to Staging
**Description:** Deploy to staging environment
**Commands:**
```bash
# Update ECS task definition
aws ecs update-task-definition --family e-commerce-staging --container-definitions file://task-def-staging.json

# Update ECS service
aws ecs update-service --cluster e-commerce-staging --service e-commerce --task-definition e-commerce-staging
```
**Verification:**
- [ ] Service updated successfully
- [ ] Health checks passing
- [ ] Smoke tests passing

### Step 3: Run Staging Tests
**Description:** Run full test suite on staging
**Commands:**
```bash
npm run test:e2e:staging
```
**Verification:**
- [ ] All tests passing

### Step 4: Deploy to Production (Canary 10%)
**Description:** Deploy to production with 10% canary
**Commands:**
```bash
# Update ECS task definition
aws ecs update-task-definition --family e-commerce-prod --container-definitions file://task-def-prod.json

# Update ECS service with canary
aws ecs update-service --cluster e-commerce-prod --service e-commerce --task-definition e-commerce-prod --deployment-configuration "maximumPercent=110,minimumHealthyPercent=50"
```
**Verification:**
- [ ] Service updated successfully
- [ ] Health checks passing
- [ ] Error rates normal
- [ ] Key metrics normal

### Step 5: Monitor Canary (1 hour)
**Description:** Monitor canary deployment for 1 hour
**Verification:**
- [ ] Error rates < 0.1%
- [ ] Response time P95 < 200ms
- [ ] No critical alerts
- [ ] User feedback positive

### Step 6: Scale to 100%
**Description:** Scale canary to full production
**Commands:**
```bash
aws ecs update-service --cluster e-commerce-prod --service e-commerce --deployment-configuration "maximumPercent=200,minimumHealthyPercent=100"
```
**Verification:**
- [ ] Service updated successfully
- [ ] All instances healthy

## Rollback Plan

### Rollback Trigger
- Error rate > 1% for 5 minutes
- Response time P95 > 1 second for 5 minutes
- Critical security issue discovered
- Major bug affecting core functionality

### Rollback Steps

### Step 1: Rollback ECS Service
**Description:** Rollback to previous task definition
**Commands:**
```bash
# Get previous task definition
aws ecs describe-task-definition --task-definition e-commerce-prod --query 'sort_by(taskDefinitions, &revision)[0]'

# Update service with previous task definition
aws ecs update-service --cluster e-commerce-prod --service e-commerce --task-definition e-commerce-prod:[PREVIOUS-REVISION]
```

### Step 2: Verify Rollback
**Description:** Verify rollback was successful
**Verification:**
- [ ] Service updated successfully
- [ ] Health checks passing
- [ ] Error rates normal

## Post-Deployment

### Verification
- [x] Health checks passing (/health endpoint)
- [x] Error rates normal (< 0.1%)
- [x] Key metrics normal (response time, throughput)
- [x] Smoke tests passing

### Monitoring
- [x] Dashboard configured (CloudWatch)
- [x] Alerts configured (Sentry, PagerDuty)
- [x] Logs streaming (CloudWatch Logs)

### Communication
- [x] Stakeholders notified (email)
- [x] Team notified (Slack)
- [x] Users notified (status page)

## Deployment Schedule

| Environment | Date | Time | Status |
|-------------|------|------|--------|
| Development | 2024-01-15 | 10:00 UTC | Complete |
| Staging | 2024-01-15 | 14:00 UTC | Complete |
| Production | 2024-01-16 | 10:00 UTC | Scheduled |

## Incident Response

### Contact Information
- **On-call:** John Doe - +1-555-123-4567
- **Tech Lead:** Jane Smith - +1-555-987-6543
- **Product Owner:** Bob Johnson - +1-555-246-8135

### Runbook
https://docs.example.com/runbooks/e-commerce

## Appendix

### Environment Variables

**Required:**
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET` - JWT signing secret
- `STRIPE_SECRET_KEY` - Stripe API secret
- `SENDGRID_API_KEY` - SendGrid API key
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key

**Optional:**
- `LOG_LEVEL` - Log level (default: info)
- `NODE_ENV` - Environment (default: production)

### External Services

| Service | Status | SLA |
|---------|--------|-----|
| PostgreSQL | Operational | 99.9% |
| Redis | Operational | 99.9% |
| Stripe | Operational | 99.9% |
| SendGrid | Operational | 99.9% |
| CloudFlare | Operational | 99.99% |

### Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| React | 18.2.0 | Frontend framework |
| Node.js | 18.17.0 | Runtime |
| Fastify | 4.24.3 | Backend framework |
| PostgreSQL | 14.9 | Database |
| Redis | 7.0.11 | Cache |
```

---

## Template Customization

Adapt templates to your needs.

### Customization Process

```
1. Start with base template
2. Add project-specific sections
3. Remove irrelevant sections
4. Adapt to team style
5. Version and share
```

### Template Variables

Standardize variables for easy replacement.

```
[Project Name]
[Team Name]
[Date]
[Author]
[URL]
[Contact]
```

### Auto-Fill Variables

Use tools to auto-fill variables.

```bash
# Example: Auto-fill project metadata
PROJECT_NAME=$(git config --get remote.origin.url | sed 's/.*\///' | sed 's/.git$//')
AUTHOR=$(git config user.name)
DATE=$(date +%Y-%m-%d)
```

---

## Template Enforcement

Ensure templates are used correctly.

### Required Sections

```markdown
# Required Sections for [Template Name]

## Section 1 (Required)
[Description of what must be included]

## Section 2 (Required)
[Description of what must be included]

## Section 3 (Optional)
[Description of what's optional]
```

### Validation

```yaml
# Template Validation Rules

required_sections:
  - overview
  - goals
  - requirements
  - constraints

validation:
  - check_required_sections: true
  - check_format: true
  - check_links: true
```

---

## Template Versioning

Track template changes over time.

### Version History

```markdown
# Template Version History

## Version 1.1 (2024-01-15)
- Added security section
- Updated deployment steps
- Fixed typos

## Version 1.0 (2024-01-01)
- Initial version
```

### Changelog

```markdown
# Changelog

## [Date] - Version [X.Y.Z]

### Added
- [New feature 1]
- [New feature 2]

### Changed
- [Modified feature 1]
- [Modified feature 2]

### Fixed
- [Bug fix 1]
- [Bug fix 2]

### Removed
- [Removed feature 1]
```

---

## Template Library

Central repository of templates.

### Library Structure

```
/templates
  /project
    skill-stack.md
    backlog.md
    requirements.md
    architecture.md
    deployment.md
  /domain
    /ecommerce
      requirements.md
      architecture.md
    /healthcare
      requirements.md
      architecture.md
  /organization
    /company-a
      /custom-templates
```

### Template Index

```markdown
# Template Library

## Project Templates
- [skill-stack.md](project/skill-stack.md) - Skills used for project
- [backlog.md](project/backlog.md) - User stories and tasks
- [requirements.md](project/requirements.md) - Full requirements
- [architecture.md](project/architecture.md) - Technical design
- [deployment.md](project/deployment.md) - Deployment plan

## Domain Templates
- [E-commerce Requirements](domain/ecommerce/requirements.md)
- [Healthcare Requirements](domain/healthcare/requirements.md)

## Organization Templates
- [Company A Custom](organization/company-a/)
```

---

## Tools for Templating

### Markdown Files

Simple, version-controlled templates.

**Pros:**
- Simple to use
- Version control friendly
- No special tools needed

**Cons:**
- Manual filling
- No validation
- Limited formatting

### Notion/Confluence Templates

Rich templates with collaboration features.

**Pros:**
- Rich formatting
- Collaboration features
- Database views

**Cons:**
- Not version controlled
- Requires account
- Limited export options

### Jira Templates

Templates integrated with project management.

**Pros:**
- Integrated with Jira
- Issue tracking
- Workflow integration

**Cons:**
- Jira-specific
- Limited customization
- Requires Jira account

### Cookiecutter

Project structure templating.

**Pros:**
- Automates project creation
- Variable substitution
- Hooks for customization

**Cons:**
- Python-based
- Learning curve
- Overkill for simple templates

---

## Real-World Template Usage

### Example 1: New Feature Kickoff

```
Templates Used:
1. requirements.md - Document feature requirements
2. backlog.md - Create user stories
3. skill-stack.md - Document skills used

Process:
1. Copy requirements.md template
2. Fill in feature-specific details
3. Create backlog from requirements
4. Identify skills needed
5. Document in skill-stack.md
```

### Example 2: Bug Investigation

```
Templates Used:
1. architecture.md - Understand system context
2. deployment.md - Check deployment status

Process:
1. Review architecture.md for context
2. Check deployment.md for current state
3. Identify affected components
4. Plan investigation approach
```

### Example 3: Performance Optimization Project

```
Templates Used:
1. requirements.md - Document performance goals
2. architecture.md - Document current architecture
3. deployment.md - Plan deployment of optimizations

Process:
1. Document performance requirements
2. Analyze current architecture
3. Plan optimization changes
4. Document deployment approach
```

---

## Best Practices

1. **Start with templates** - Don't create from scratch
2. **Customize appropriately** - Adapt to project needs
3. **Keep templates updated** - Reflect best practices
4. **Version control templates** - Track changes
5. **Share templates** - Make them accessible to team
6. **Validate templates** - Ensure completeness
7. **Document templates** - Explain how to use
8. **Gather feedback** - Improve templates based on usage
9. **Standardize variables** - Use consistent naming
10. **Automate where possible** - Use tools for efficiency

---

## Related Skills

- [Baseline Policy](../baseline-policy/SKILL.md) - Templates should reflect baseline
- [Routing Rules](../routing-rules/SKILL.md) - Select templates based on task
- [Scoring and Prioritization](../scoring-and-prioritization/SKILL.md) - Prioritize template sections
