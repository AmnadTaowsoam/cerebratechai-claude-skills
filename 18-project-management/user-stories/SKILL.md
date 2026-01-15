# User Stories

## Overview

User stories are short, simple descriptions of a feature told from the perspective of the user. They help teams focus on delivering value to users rather than just building functionality.

---

## 1. User Story Format

### The Standard Format

```
As a [type of user],
I want [some goal],
So that [some reason].
```

### Example

```
As a registered user,
I want to reset my password,
So that I can regain access to my account if I forget it.
```

### Breaking Down the Format

| Component | Purpose | Example |
|-----------|---------|---------|
| **As a** | Defines the persona/user type | "As a registered user" |
| **I want** | Describes the feature/action | "I want to reset my password" |
| **So that** | Explains the value/benefit | "So that I can regain access to my account" |

### Why This Format Works

1. **User-Centric**: Forces thinking from user perspective
2. **Value-Focused**: The "so that" ensures we understand the value
3. **Simple**: Easy to understand and communicate
4. **Concise**: Keeps stories short and focused

---

## 2. INVEST Criteria

The INVEST acronym describes the characteristics of a good user story.

### I - Independent

A story should be self-contained and not dependent on other stories.

```markdown
# Bad Example - Dependent Stories

## Story 1: User Registration
As a new user, I want to create an account.

## Story 2: User Login
As a registered user, I want to login to my account.

# Problem: Story 2 depends on Story 1

# Good Example - Independent Story

## Story: User Authentication
As a user, I want to authenticate with email and password, so that I can access my account securely.

# Includes both registration and login in one cohesive story
```

### N - Negotiable

A story should be a starting point for discussion, not a fixed specification.

```markdown
# Negotiable Story

## US-001: Password Reset

As a user, I want to reset my password, so that I can regain access to my account.

### Discussion Points
- Should we send reset link via email or SMS?
- How long should the reset link be valid?
- Should we require the old password?
- Should we notify the user of the password change?

### Implementation Options
1. Email link with token
2. SMS verification code
3. Security questions
4. Multi-factor reset
```

### V - Valuable

A story must deliver value to the user or business.

```markdown
# Valuable Story

## US-001: Order Tracking

As a customer, I want to track my order status, so that I know when to expect delivery.

### Value Delivered
- Reduces customer anxiety
- Decreases support inquiries
- Improves customer satisfaction
- Builds trust in the service

# Non-Valuable Story (Avoid)

## US-XXX: Database Migration

As a developer, I want to migrate to a new database, so that we can use new features.

# Problem: This is a technical task, not a user story
# Solution: Break into technical tasks, not user stories
```

### E - Estimable

A story should be small enough to estimate with reasonable accuracy.

```markdown
# Too Large - Not Estimable

## US-XXX: E-commerce Platform

As a business owner, I want a complete e-commerce platform, so that I can sell products online.

# Problem: Too large, includes many features
# Solution: Break into multiple stories

# Good - Estimable

## US-001: Product Listing

As a customer, I want to browse products, so that I can find what I want to buy.

## US-002: Product Details

As a customer, I want to view product details, so that I can make informed purchase decisions.

## US-003: Shopping Cart

As a customer, I want to add products to my cart, so that I can purchase multiple items.
```

### S - Small

A story should be small enough to complete in one sprint (typically 1-3 days).

```markdown
# Too Large

## US-XXX: User Profile Management

As a user, I want to manage my profile, so that I can keep my information up to date.

# Includes: View profile, edit profile, upload photo, change password, delete account

# Break Down

## US-001: View Profile
As a user, I want to view my profile, so that I can see my current information.

## US-002: Edit Profile
As a user, I want to edit my profile, so that I can update my information.

## US-003: Upload Profile Photo
As a user, I want to upload a profile photo, so that others can recognize me.

## US-004: Change Password
As a user, I want to change my password, so that I can maintain account security.
```

### T - Testable

A story should have clear acceptance criteria that can be verified.

```markdown
# Testable Story

## US-001: User Registration

As a new user, I want to create an account, so that I can access the platform.

### Acceptance Criteria
- [ ] User can enter email, password, and confirm password
- [ ] Email format is validated
- [ ] Password must be at least 8 characters
- [ ] Password must contain uppercase, lowercase, and number
- [ ] Password and confirmation must match
- [ ] Email must be unique
- [ ] User receives confirmation email
- [ ] User is logged in after registration

# Each criterion can be tested and verified

# Not Testable (Avoid)

## US-XXX: Improve Performance

As a user, I want the app to be faster, so that I can use it more efficiently.

# Problem: "Faster" is not measurable
# Solution: Add specific, measurable criteria

## US-XXX: Improve Page Load Time

As a user, I want pages to load within 2 seconds, so that I can use the app without waiting.

### Acceptance Criteria
- [ ] Homepage loads within 2 seconds on 4G
- [ ] Product page loads within 2 seconds on 4G
- [ ] Checkout page loads within 2 seconds on 4G
```

---

## 3. Acceptance Criteria

### Acceptance Criteria Template

```markdown
# User Story: [Story Name]

## Story
As a [user type], I want [action], so that [benefit].

## Acceptance Criteria

### Happy Path
- [ ] [User action] results in [expected outcome]
- [ ] [User action] results in [expected outcome]

### Validation
- [ ] [Validation rule] is enforced
- [ ] [Validation rule] is enforced

### Error Handling
- [ ] [Error condition] shows [error message]
- [ ] [Error condition] shows [error message]

### Edge Cases
- [ ] [Edge case] is handled by [behavior]
- [ ] [Edge case] is handled by [behavior]

### Performance
- [ ] [Operation] completes within [time]
- [ ] [Operation] completes within [time]

### Security
- [ ] [Security requirement] is implemented
- [ ] [Security requirement] is implemented

## Definition of Done
- [ ] Code implemented
- [ ] Unit tests written
- [ ] Integration tests written
- [ ] Code reviewed
- [ ] QA approved
- [ ] Documentation updated
```

### Example: Password Reset

```markdown
# US-001: Password Reset

As a registered user, I want to reset my password, so that I can regain access to my account if I forget it.

## Acceptance Criteria

### User Flow
- [ ] User can request password reset from login page
- [ ] User enters their email address
- [ ] System validates email format
- [ ] System checks if email exists in database
- [ ] System sends reset link to email
- [ ] Reset link expires after 1 hour
- [ ] User clicks reset link
- [ ] User enters new password
- [ ] User confirms new password
- [ ] System validates password strength
- [ ] System updates password
- [ ] User is redirected to login page

### Validation
- [ ] Email must be in valid format
- [ ] Email must exist in system
- [ ] Password must be at least 8 characters
- [ ] Password must contain uppercase, lowercase, and number
- [ ] Password and confirmation must match

### Error Handling
- [ ] Invalid email shows "Please enter a valid email address"
- [ ] Email not found shows "No account found with this email"
- [ ] Expired link shows "This link has expired. Please request a new password reset"
- [ ] Used link shows "This link has already been used. Please request a new password reset"
- [ ] Weak password shows "Password must contain at least 8 characters, including uppercase, lowercase, and numbers"

### Security
- [ ] Reset token is cryptographically secure
- [ ] Reset token is single-use
- [ ] Reset token expires after 1 hour
- [ ] Rate limiting: max 5 reset requests per hour per email
- [ ] Old password is invalidated
- [ ] User is logged out of all sessions
- [ ] Email notification sent for password change

### Performance
- [ ] Reset email sent within 5 seconds
- [ ] Password update completes within 2 seconds

## Definition of Done
- [ ] Frontend implementation complete
- [ ] Backend API implementation complete
- [ ] Email service integration complete
- [ ] Unit tests written (coverage > 80%)
- [ ] Integration tests written
- [ ] Security review completed
- [ ] Code reviewed by at least one peer
- [ ] QA tested in staging environment
- [ ] Product owner accepted
- [ ] Documentation updated
```

---

## 4. Story Points Estimation

### What Are Story Points?

Story points are a relative measure of the effort required to implement a user story, considering:
- Complexity
- Effort
- Risk
- Uncertainty

### Fibonacci Sequence

Most teams use the Fibonacci sequence for story points:
1, 2, 3, 5, 8, 13, 21, 40

| Points | Description |
|--------|-------------|
| 1 | Very small, trivial task |
| 2 | Small task, minimal complexity |
| 3 | Small to medium, some complexity |
| 5 | Medium, typical story |
| 8 | Medium to large, significant complexity |
| 13 | Large, high complexity or uncertainty |
| 21 | Very large, should be broken down |
| 40 | Epic, must be broken down |

### Estimation Guidelines

```markdown
# Story Point Reference

## 1 Point Story
- Simple UI change
- Fix a minor bug
- Add a simple validation
- Update text or labels

Example:
- Change button color
- Fix typo in error message
- Add email format validation

## 2 Point Story
- Simple CRUD operation
- Small feature with minimal complexity
- Integration with existing service

Example:
- Add "delete" button to list
- Update user profile field
- Add simple filter to list

## 3 Point Story
- Typical feature with some complexity
- Multiple components involved
- Some new code, some existing code

Example:
- Implement search functionality
- Add pagination to list
- Create simple dashboard widget

## 5 Point Story
- Medium complexity feature
- Multiple components and interactions
- Some uncertainty or research needed

Example:
- Implement file upload
- Add notification system
- Create multi-step form

## 8 Point Story
- Complex feature
- Multiple integrations
- Significant uncertainty

Example:
- Implement shopping cart
- Add real-time chat
- Create reporting dashboard

## 13 Point Story
- Very complex feature
- High uncertainty
- Should consider breaking down

Example:
- Implement payment processing
- Add advanced search with filters
- Create user management system

## 21+ Points
- Too large
- Must be broken down into smaller stories
```

### Planning Poker

Planning poker is a consensus-based estimation technique.

```markdown
# Planning Poker Process

## Preparation
1. Prepare a list of user stories to estimate
2. Each team member gets a deck of cards (1, 2, 3, 5, 8, 13, 21, 40, ?)
3. Appoint a moderator (usually Scrum Master)

## Estimation Process

### Step 1: Story Overview
- Product Owner presents the user story
- Team asks clarifying questions
- Acceptance criteria are reviewed

### Step 2: Initial Estimates
- Each team member selects a card privately
- All cards are revealed simultaneously

### Step 3: Discussion
- If estimates are close, use the average
- If estimates differ significantly, discuss:
  - Why did you choose that number?
  - What complexity did you see?
  - What risks did you identify?

### Step 4: Re-estimate
- Team discusses and clarifies
- Team re-estimates
- Repeat until consensus is reached

### Step 5: Record
- Record the agreed story point
- Move to next story

## Tips
- The person with the highest estimate explains first
- The person with the lowest estimate explains second
- Don't average - aim for consensus
- Use "?" if you need more information
- Timebox discussions (2-3 minutes per story)
```

---

## 5. Epic vs Story vs Task

### Hierarchy

```
Epic (Large initiative)
  └── Feature (Major capability)
      └── User Story (User-centric requirement)
          └── Task (Implementation step)
```

### Epic

An epic is a large body of work that can be broken down into smaller user stories.

```markdown
# Epic: User Management

## Description
Comprehensive user management system including registration, authentication, profiles, and permissions.

## Business Value
- Secure user access
- Personalized user experience
- Admin control over users
- Compliance with security standards

## Stories Included
- US-001: User Registration
- US-002: User Login
- US-003: Password Reset
- US-004: User Profile
- US-005: User Permissions
- US-006: User Administration

## Estimated Duration
- 4-6 sprints

## Dependencies
- Authentication service
- Database schema
- Email service
```

### Feature

A feature is a cohesive set of functionality that delivers value to users.

```markdown
# Feature: Social Login

## Description
Allow users to register and login using social media accounts.

## User Stories
- US-001: Google Login
- US-002: Facebook Login
- US-003: Apple Login
- US-004: Link Social Account

## Acceptance Criteria
- Users can login with social accounts
- Existing users can link social accounts
- Profile data is imported from social providers
- Users can unlink social accounts

## Dependencies
- OAuth 2.0 integration
- Social provider APIs
- User account linking logic
```

### User Story

A user story is a small, user-centric requirement.

```markdown
# US-001: Google Login

As a new user, I want to login with my Google account, so that I can quickly access the platform.

## Acceptance Criteria
- [ ] User can click "Login with Google" button
- [ ] Google OAuth flow is initiated
- [ ] User is redirected to Google authentication page
- [ ] User grants permissions
- [ ] User is redirected back to app
- [ ] User account is created or logged in
- [ ] User profile is populated with Google data
```

### Task

A task is a specific implementation step.

```markdown
# Tasks for US-001: Google Login

## Frontend Tasks
- [ ] Add "Login with Google" button to login page
- [ ] Install and configure Google OAuth library
- [ ] Implement OAuth redirect handling
- [ ] Add loading states
- [ ] Add error handling

## Backend Tasks
- [ ] Set up Google OAuth credentials
- [ ] Implement OAuth callback endpoint
- [ ] Implement token validation
- [ ] Implement user account creation logic
- [ ] Implement user account linking logic
- [ ] Add error handling

## Testing Tasks
- [ ] Write unit tests for OAuth flow
- [ ] Write integration tests
- [ ] Manual testing in staging
- [ ] Test error scenarios

## Documentation Tasks
- [ ] Update API documentation
- [ ] Create user guide for social login
- [ ] Document OAuth configuration
```

---

## 6. Story Mapping

Story mapping is a visual technique for organizing user stories to understand the complete user journey.

### Story Map Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    User Activities                           │
├─────────────────────────────────────────────────────────────┤
│  Browse Products  →  Add to Cart  →  Checkout  →  Receive   │
├─────────────────────────────────────────────────────────────┤
│  User Stories (organized by priority)                       │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ View    │  │ Add     │  │ View    │  │ Track   │        │
│  │ Product │  │ Item    │  │ Cart    │  │ Order   │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Search  │  │ Remove  │  │ Apply   │  │ Receive │        │
│  │ Products│  │ Item    │  │ Coupon  │  │ Order   │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Filter  │  │ Update  │  │ Payment │  │ Return  │        │
│  │ Products│  │ Quantity│  │         │  │ Order   │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│                                                              │
│  Release 1 (MVP)  │  Release 2  │  Release 3               │
└─────────────────────────────────────────────────────────────┘
```

### Story Mapping Process

```markdown
# Story Mapping Workshop

## Preparation
- [ ] Identify user personas
- [ ] Define user activities
- [ ] Gather all user stories
- [ ] Prepare story mapping board (physical or digital)

## Steps

### Step 1: Frame the Problem
- What problem are we solving?
- Who are we solving it for?
- What are our goals?

### Step 2: Map User Activities
- Identify major activities users perform
- Arrange activities in chronological order
- Example: Browse → Select → Purchase → Use

### Step 3: Brainstorm User Stories
- For each activity, brainstorm user stories
- Write each story on a sticky note or card
- Don't worry about order or priority yet

### Step 4: Organize Stories
- Group stories under activities
- Arrange stories in priority order (top to bottom)
- Most important stories at the top

### Step 5: Identify Releases
- Draw horizontal lines to separate releases
- Release 1 (MVP): Must-have stories
- Release 2: Should-have stories
- Release 3: Nice-to-have stories

### Step 6: Validate and Refine
- Review the map with stakeholders
- Ensure the user journey makes sense
- Adjust priorities as needed

## Outputs
- Visual story map
- Prioritized backlog
- Release plan
- User journey understanding
```

---

## 7. Personas

User personas are fictional characters that represent different user types.

### Persona Template

```markdown
# User Persona: [Persona Name]

## Basic Information
- **Name**: [Name]
- **Age**: [Age]
- **Occupation**: [Job Title]
- **Location**: [City, Country]
- **Photo**: [Image]

## Background
[Description of their background, experience, and context]

## Goals
- [Primary goal 1]
- [Primary goal 2]
- [Secondary goal 1]

## Pain Points
- [Pain point 1]
- [Pain point 2]
- [Pain point 3]

## Behaviors
- [Behavior 1]
- [Behavior 2]
- [Behavior 3]

## Technical Proficiency
- **Level**: [Beginner/Intermediate/Advanced]
- **Devices Used**: [List devices]
- **Software Used**: [List software]

## Motivations
- [Motivation 1]
- [Motivation 2]

## Frustrations
- [Frustration 1]
- [Frustration 2]

## Quote
"[Representative quote from this persona]"

## Scenarios
[Typical scenarios where this persona uses the product]
```

### Example Personas

```markdown
# Persona: Busy Professional

## Basic Information
- **Name**: Sarah Johnson
- **Age**: 32
- **Occupation**: Marketing Manager
- **Location**: San Francisco, CA
- **Photo**: [Professional headshot]

## Background
Sarah is a marketing manager at a mid-sized tech company. She manages a team of 5 people and is responsible for multiple marketing campaigns. She's tech-savvy but always pressed for time.

## Goals
- Complete tasks quickly and efficiently
- Stay organized and on top of deadlines
- Collaborate effectively with her team
- Access information from anywhere

## Pain Points
- Too many tools and platforms to manage
- Difficulty finding information quickly
- Email overload
- Limited time for learning new features

## Behaviors
- Checks email first thing in the morning
- Uses mobile apps while commuting
- Prefers keyboard shortcuts
- Multitasks frequently

## Technical Proficiency
- **Level**: Advanced
- **Devices Used**: iPhone, MacBook Pro, iPad
- **Software Used**: Slack, Google Workspace, Asana, Salesforce

## Motivations
- Wants to be seen as efficient and reliable
- Values productivity tools that save time
- Appreciates clean, intuitive interfaces

## Frustrations
- Cluttered, confusing interfaces
- Slow performance
- Having to click multiple times for simple actions
- Features that are hard to discover

## Quote
"I don't have time to figure out how things work. It should just work."

## Scenarios
- Checking campaign status on her phone during commute
- Quick review of team tasks before a meeting
- Responding to urgent client emails from home
```

```markdown
# Persona: First-Time User

## Basic Information
- **Name**: Alex Chen
- **Age**: 24
- **Occupation**: Recent Graduate
- **Location**: New York, NY
- **Photo**: [Casual photo]

## Background
Alex recently graduated college and is looking for their first job. They're comfortable with technology but may not be familiar with industry-specific tools.

## Goals
- Learn how to use the platform quickly
- Complete tasks without asking for help
- Understand the value of the platform
- Feel confident using the features

## Pain Points
- Unclear instructions
- Confusing terminology
- Fear of making mistakes
- Not knowing where to start

## Behaviors
- Relies on tooltips and help text
- Watches video tutorials
- Asks peers for help
- Prefers step-by-step guidance

## Technical Proficiency
- **Level**: Intermediate
- **Devices Used**: Smartphone, Laptop
- **Software Used**: Social media apps, Google Docs

## Motivations
- Wants to impress in their new role
- Values clear, simple instructions
- Appreciates onboarding and guidance

## Frustrations
- Jargon and technical terms
- Hidden features
- No clear next steps
- Feeling overwhelmed

## Quote
"I just want to know what to do next."

## Scenarios
- First time logging into the platform
- Setting up their profile
- Completing their first task
```

---

## 8. Edge Cases

Edge cases are scenarios that occur at the extreme ends of normal operation.

### Common Edge Cases to Consider

```markdown
# Edge Case Checklist

## Data-Related Edge Cases
- [ ] Empty data (null, empty string, zero)
- [ ] Maximum length data
- [ ] Minimum length data
- [ ] Special characters
- [ ] Unicode characters
- [ ] Duplicate data
- [ ] Corrupted data

## User Behavior Edge Cases
- [ ] Rapid clicking (double-submit)
- [ ] Back button navigation
- [ ] Refresh during operation
- [ ] Closing browser during operation
- [ ] Multiple tabs open
- [ ] Browser offline
- [ ] Slow network connection

## System Edge Cases
- [ ] Server timeout
- [ ] Database connection failure
- [ ] API rate limits exceeded
- [ ] Concurrent operations
- [ ] Large dataset processing
- [ ] Memory limits exceeded

## Business Logic Edge Cases
- [ ] Boundary values (0, 1, max, max+1)
- [ ] Time zone differences
- [ ] Leap years
- [ ] Daylight saving time
- [ ] Currency conversion edge cases
- [ ] Permission conflicts

## Security Edge Cases
- [ ] SQL injection attempts
- [ ] XSS attempts
- [ ] CSRF attempts
- [ ] Brute force attacks
- [ ] Session hijacking
- [ ] Token expiration
```

### Edge Case Examples

```markdown
# US-001: User Registration - Edge Cases

## Acceptance Criteria (Standard)
- [ ] User can register with valid email and password

## Edge Cases

### Empty Fields
- [ ] Submitting with empty email shows error
- [ ] Submitting with empty password shows error
- [ ] Submitting with all fields empty shows error

### Invalid Email
- [ ] Email without @ symbol shows error
- [ ] Email without domain shows error
- [ ] Email with invalid characters shows error
- [ ] Email with spaces shows error

### Password Edge Cases
- [ ] Password shorter than 8 characters shows error
- [ ] Password without uppercase shows error
- [ ] Password without lowercase shows error
- [ ] Password without number shows error
- [ ] Password with only numbers shows error
- [ ] Password with only letters shows error

### Existing Email
- [ ] Registering with existing email shows error
- [ ] Error message doesn't reveal if email exists (security)

### Special Characters
- [ ] Email with + sign is accepted (e.g., user+tag@gmail.com)
- [ ] Password with special characters is accepted
- [ ] Name with accents is accepted

### Network Issues
- [ ] Slow network shows loading state
- [ ] Network error shows appropriate message
- [ ] Retry mechanism works after network failure

### Concurrent Operations
- [ ] Double-clicking submit doesn't create duplicate accounts
- [ ] Multiple registration attempts from same IP are rate-limited

### Time-Based Edge Cases
- [ ] Account expires if not verified within 24 hours
- [ ] Verification link expires after 1 hour
```

---

## 9. Non-Functional Requirements in Stories

Non-functional requirements (NFRs) describe how the system performs rather than what it does.

### Including NFRs in User Stories

```markdown
# US-001: User Registration with NFRs

As a new user, I want to create an account, so that I can access the platform.

## Functional Acceptance Criteria
- [ ] User can enter email and password
- [ ] User receives confirmation email
- [ ] User is logged in after registration

## Non-Functional Acceptance Criteria

### Performance
- [ ] Registration completes within 2 seconds
- [ ] Confirmation email is sent within 5 seconds
- [ ] Page loads within 1 second

### Security
- [ ] Password is hashed using bcrypt
- [ ] HTTPS is enforced
- [ ] Rate limiting: max 5 registrations per IP per hour
- [ ] SQL injection protection implemented

### Usability
- [ ] Form is accessible (WCAG 2.1 AA)
- [ ] Error messages are clear and helpful
- [ ] Form works on mobile devices
- [ ] Keyboard navigation is supported

### Reliability
- [ ] Registration succeeds 99.9% of the time
- [ ] System handles 1000 concurrent registrations
- [ ] Graceful degradation if email service is down

### Maintainability
- [ ] Code is documented
- [ ] Unit tests have 80% coverage
- [ ] Logging is implemented for debugging
```

### NFR Story Template

```markdown
# NFR Story Template

## Story
As a [user], I want [functional requirement], so that [benefit].

## NFR Categories

### Performance
- [ ] [Response time requirement]
- [ ] [Throughput requirement]
- [ ] [Resource usage requirement]

### Security
- [ ] [Authentication requirement]
- [ ] [Authorization requirement]
- [ ] [Data protection requirement]

### Scalability
- [ ] [Concurrent user requirement]
- [ ] [Data volume requirement]
- [ ] [Growth requirement]

### Reliability
- [ ] [Uptime requirement]
- [ ] [Error rate requirement]
- [ ] [Recovery requirement]

### Usability
- [ ] [Accessibility requirement]
- [ ] [Mobile requirement]
- [ ] [Learnability requirement]

### Maintainability
- [ ] [Code quality requirement]
- [ ] [Documentation requirement]
- [ ] [Testing requirement]
```

---

## 10. Examples for Common Features

### Authentication

```markdown
# US-001: User Registration

As a new user, I want to create an account with my email and password, so that I can access the platform.

## Acceptance Criteria
- [ ] User can enter email, password, and confirm password
- [ ] Email format is validated
- [ ] Password must be at least 8 characters
- [ ] Password must contain uppercase, lowercase, and number
- [ ] Password and confirmation must match
- [ ] Email must be unique
- [ ] User receives confirmation email
- [ ] User is logged in after registration
- [ ] User profile is created with default settings

---

# US-002: User Login

As a registered user, I want to login with my email and password, so that I can access my account.

## Acceptance Criteria
- [ ] User can enter email and password
- [ ] Invalid credentials show appropriate error
- [ ] Successful login redirects to dashboard
- [ ] Session is created and maintained
- [ ] "Remember me" option keeps user logged in
- [ ] Account locked after 5 failed attempts

---

# US-003: Password Reset

As a registered user, I want to reset my password, so that I can regain access to my account.

## Acceptance Criteria
- [ ] User can request reset from login page
- [ ] Reset link sent to email
- [ ] Link expires after 1 hour
- [ ] User can set new password
- [ ] New password must meet requirements
- [ ] User is logged out of all sessions
- [ ] Notification sent for password change

---

# US-004: Social Login

As a new user, I want to login with my Google account, so that I can quickly access the platform.

## Acceptance Criteria
- [ ] User can click "Login with Google" button
- [ ] OAuth flow is initiated
- [ ] User is redirected to Google
- [ ] User grants permissions
- [ ] User account is created or logged in
- [ ] Profile data is imported from Google
- [ ] Existing users can link Google account
```

### Payment

```markdown
# US-001: Add Payment Method

As a customer, I want to add a credit card to my account, so that I can make purchases.

## Acceptance Criteria
- [ ] User can enter card number, expiry, and CVV
- [ ] Card number is validated (Luhn algorithm)
- [ ] Expiry date is validated
- [ ] CVV is validated
- [ ] Card type is detected (Visa, Mastercard, etc.)
- [ ] Card is tokenized (not stored directly)
- [ ] Default payment method can be set
- [ ] Payment methods can be deleted

---

# US-002: Checkout with Payment

As a customer, I want to pay for my order, so that I can complete my purchase.

## Acceptance Criteria
- [ ] User can select payment method
- [ ] Order total is displayed
- [ ] Tax and shipping are calculated
- [ ] User can enter billing address
- [ ] Payment is processed securely
- [ ] Success page shows order confirmation
- [ ] Email confirmation is sent
- [ ] Order is created in system

---

# US-003: Refund Request

As a customer, I want to request a refund, so that I can get my money back if I'm not satisfied.

## Acceptance Criteria
- [ ] User can select order for refund
- [ ] User can select items to refund
- [ ] User can provide reason for refund
- [ ] Refund request is submitted
- [ ] Admin is notified of refund request
- [ ] User receives confirmation email
- [ ] Refund status can be tracked
```

### Search

```markdown
# US-001: Basic Search

As a user, I want to search for products, so that I can find what I'm looking for.

## Acceptance Criteria
- [ ] User can enter search query
- [ ] Results display within 2 seconds
- [ ] Results are sorted by relevance
- [ ] Pagination shows 20 results per page
- [ ] Search is case-insensitive
- [ ] Partial matches are supported
- [ ] No results message is helpful

---

# US-002: Advanced Search

As a user, I want to filter search results, so that I can find exactly what I need.

## Acceptance Criteria
- [ ] User can filter by category
- [ ] User can filter by price range
- [ ] User can filter by brand
- [ ] User can filter by rating
- [ ] Multiple filters can be combined
- [ ] Active filters are displayed
- [ ] Filters can be cleared

---

# US-003: Search Suggestions

As a user, I want to see search suggestions, so that I can find results faster.

## Acceptance Criteria
- [ ] Suggestions appear as user types
- [ ] Suggestions appear within 300ms
- [ ] Top 5 suggestions are shown
- [ ] User can select suggestion
- [ ] Keyboard navigation is supported
- [ ] No suggestions message if no matches
```

### Notifications

```markdown
# US-001: In-App Notifications

As a user, I want to see notifications in the app, so that I don't miss important updates.

## Acceptance Criteria
- [ ] Notification bell shows unread count
- [ ] Clicking bell opens notification panel
- [ ] Notifications are sorted by date (newest first)
- [ ] Mark as read functionality
- [ ] Mark all as read functionality
- [ ] Delete notification functionality
- [ ] Notification links to relevant content

---

# US-002: Email Notifications

As a user, I want to receive email notifications, so that I can stay informed when not in the app.

## Acceptance Criteria
- [ ] User can enable/disable email notifications
- [ ] User can choose notification types
- [ ] Emails are sent for selected events
- [ ] Email format is consistent
- [ ] Unsubscribe link is included
- [ ] Notification preferences are saved

---

# US-003: Push Notifications

As a user, I want to receive push notifications, so that I can be alerted to important events.

## Acceptance Criteria
- [ ] User can grant push notification permission
- [ ] User can enable/disable push notifications
- [ ] Push notifications are sent for important events
- [ ] Notification badge shows on app icon
- [ ] Tapping notification opens relevant screen
- [ ] Quiet hours can be set
```

---

## 11. Templates

### Quick Reference Card

```markdown
# User Story Quick Reference

## Format
```
As a [user type],
I want [action],
So that [benefit].
```

## INVEST Criteria
- **I**ndependent
- **N**egotiable
- **V**aluable
- **E**stimable
- **S**mall
- **T**estable

## Story Points
- 1: Trivial
- 2: Small
- 3: Small/Medium
- 5: Medium
- 8: Medium/Large
- 13: Large
- 21+: Break down

## Acceptance Criteria Template
- [ ] Happy path
- [ ] Validation
- [ ] Error handling
- [ ] Edge cases
- [ ] Performance
- [ ] Security

## Definition of Done
- [ ] Code implemented
- [ ] Tests written
- [ ] Code reviewed
- [ ] QA approved
- [ ] Documentation updated
```

### Story Card Template

```markdown
# [US-ID]: [Story Title]

## Story
As a [user type], I want [action], so that [benefit].

## Priority
- [ ] P0 (Critical)
- [ ] P1 (High)
- [ ] P2 (Medium)
- [ ] P3 (Low)

## Story Points
[Points]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Edge Cases
- [ ] [Edge case 1]
- [ ] [Edge case 2]

## Dependencies
- [Dependency 1]
- [Dependency 2]

## Notes
[Any additional context]

## Tasks
- [ ] [Task 1]
- [ ] [Task 2]
```

---

## Best Practices

### Writing Good User Stories

1. **Start with the User**
   - Always write from the user's perspective
   - Focus on user needs and goals
   - Understand the user's context

2. **Keep It Simple**
   - Use clear, simple language
   - Avoid technical jargon
   - Be concise but complete

3. **Focus on Value**
   - The "so that" clause is crucial
   - Explain why the feature matters
   - Connect to business goals

4. **Make It Testable**
   - Write clear acceptance criteria
   - Include measurable criteria
   - Define edge cases

5. **Break Down Large Stories**
   - If it's too big, split it
   - Aim for 1-3 days of work
   - Keep stories independent

6. **Collaborate**
   - Involve the whole team
   - Discuss stories before estimating
   - Get product owner input

7. **Iterate**
   - Stories can change
   - Refine as you learn more
   - Don't be afraid to rewrite

### Common Mistakes to Avoid

- ❌ Writing stories from developer perspective
- ❌ Forgetting the "so that" clause
- ❌ Making stories too large
- ❌ Vague acceptance criteria
- ❌ Including implementation details
- ❌ Writing stories without user value
- ❌ Not considering edge cases
- ❌ Ignoring non-functional requirements
- ❌ Not collaborating with stakeholders
- ❌ Treating stories as fixed requirements

### Quick Tips

- ✅ Use "As a" to define the persona
- ✅ Use "I want" to describe the action
- ✅ Use "So that" to explain the value
- ✅ Write acceptance criteria as testable statements
- ✅ Include edge cases
- ✅ Consider NFRs
- ✅ Keep stories small
- ✅ Collaborate with the team
- ✅ Be willing to adapt
- ✅ Focus on delivering value
