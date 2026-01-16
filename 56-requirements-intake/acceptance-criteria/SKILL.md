# Acceptance Criteria

## Overview

Acceptance criteria are specific, testable conditions that must be met for work to be considered complete. They provide a shared understanding of "done" and enable verification that requirements have been met.

## What Are Acceptance Criteria

Acceptance criteria are:

- **Specific conditions** that must be met for work to be complete
- **Testable and measurable** - can be verified through testing
- **Shared understanding** of what "done" means
- **Clear boundaries** between complete and incomplete

## Why Acceptance Criteria Matter

| Benefit | Description |
|---------|-------------|
| **Prevent misunderstandings** | Clear expectations for all parties |
| **Enable testing** - QA can verify against criteria |
| **Clarify requirements** - Makes vague requirements specific |
| **Enable sign-off** - Objective basis for approval |
| **Guide development** - Developers know what to build |
| **Reduce rework** - Build it right the first time |

---

## Good Acceptance Criteria Characteristics

Use the **SMART** framework:

| Characteristic | Description | Example |
|----------------|-------------|---------|
| **Specific** | Clear and unambiguous | "User can sign up with email and password" |
| **Measurable** | Can be verified objectively | "Email validation checks for @ and .domain" |
| **Achievable** | Realistic and possible | "Password must be 8+ characters" |
| **Relevant** | Directly related to requirement | "Confirmation email sent after signup" |
| **Testable** | Can be validated through testing | "Error message shown for invalid email format" |

### Good vs Bad Examples

| Bad | Why Bad | Good |
|-----|---------|------|
| "Works well" | Vague, not measurable | "Page loads in under 2 seconds" |
| "User-friendly" | Subjective | "Form has clear labels and help text" |
| "Looks good" | Subjective | "Matches design mockup exactly" |
| "Secure" | Vague | "Password hashed with bcrypt, salt rounds 12" |
| "Fast" | Vague | "API response time P95 < 200ms" |

---

## Format Options

### 1. Given-When-Then (BDD Style)

Behavior-Driven Development format, great for user stories.

```
Given [context/precondition]
When [action/event]
Then [expected outcome]
```

**Example:**
```
Given user is logged in
When user clicks "Add to Cart" on a product
Then product is added to cart
And cart count increases by 1
And success message is displayed
```

### 2. Checklist Format

Simple list of requirements that must be met.

```
[ ] User can sign up with email and password
[ ] System validates email format
[ ] System sends verification email
[ ] Error message shown for invalid inputs
[ ] Password must be 8+ characters with mixed types
[ ] User is redirected to dashboard after signup
```

### 3. Scenario Format

Descriptive format with steps and expected outcomes.

```
Scenario: User signs up successfully
1. User enters valid email and password
2. User clicks "Sign Up" button
3. Account is created in database
4. Confirmation email is sent
5. User is redirected to dashboard
6. Success message is displayed

Scenario: User signs up with invalid email
1. User enters invalid email format
2. User clicks "Sign Up" button
3. Error message: "Invalid email format" is shown
4. Account is not created
5. User remains on signup page
```

### 4. Rule-Based Format

Format with explicit rules and conditions.

```
Rule 1: Email Validation
- Must contain @ symbol
- Must have domain after @
- Must not contain spaces
- Max length: 255 characters

Rule 2: Password Requirements
- Minimum 8 characters
- Must contain uppercase letter
- Must contain lowercase letter
- Must contain number
- Must contain special character

Rule 3: Account Creation
- Email must be unique
- Account is created as "unverified"
- Verification email sent immediately
- Account expires after 7 days if unverified
```

---

## Given-When-Then Format in Detail

The Gherkin syntax is widely used for BDD and acceptance criteria.

### Structure

```
SCENARIO: [Scenario name]

GIVEN [context or precondition]
  AND [additional context]
WHEN [action or event]
  AND [additional action]
THEN [expected outcome]
  AND [additional outcome]
```

### Complete Example

```
SCENARIO: Successful user registration

GIVEN the user is on the registration page
  AND the user has not registered before
WHEN the user enters a valid email address
  AND the user enters a valid password
  AND the user clicks the "Sign Up" button
THEN a new user account is created
  AND the account status is "unverified"
  AND a verification email is sent
  AND the user is redirected to the dashboard
  AND a success message is displayed

SCENARIO: Registration with invalid email

GIVEN the user is on the registration page
WHEN the user enters an invalid email address
  AND the user enters a valid password
  AND the user clicks the "Sign Up" button
THEN no account is created
  AND an error message "Invalid email format" is displayed
  AND the user remains on the registration page

SCENARIO: Registration with duplicate email

GIVEN the user is on the registration page
  AND an account with this email already exists
WHEN the user enters an existing email address
  AND the user enters a valid password
  AND the user clicks the "Sign Up" button
THEN no account is created
  AND an error message "Email already registered" is displayed
  AND the user remains on the registration page
```

### Best Practices for Gherkin

1. **One scenario per test case** - Keep scenarios focused
2. **Use business language** - Not technical implementation details
3. **Focus on behavior** - What the system does, not how
4. **Include happy path and error cases** - Cover all scenarios
5. **Be specific** - Use concrete values where appropriate

---

## Writing Good Acceptance Criteria

### Focus on "What" Not "How"

| Bad (How) | Good (What) |
|-----------|-------------|
| "Use React useState for form" | "Form maintains state between user inputs" |
| "Store password in bcrypt" | "Password is securely hashed" |
| "Use axios for API calls" | "API requests are made and responses handled" |

### Include Happy Path and Error Cases

```
Happy Path:
- User enters valid credentials → Login successful
- User submits valid form → Data saved

Error Cases:
- User enters invalid email → Error message shown
- User enters wrong password → Error message shown
- Network error → Retry option displayed
- Server error → Friendly error message shown
```

### Be Specific About Data Formats

```
Vague: "Valid email format"
Specific: "Email must match regex: ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

Vague: "Valid phone number"
Specific: "Phone number: 10 digits, optional country code (+1)"

Vague: "Valid date"
Specific: "Date format: YYYY-MM-DD, must be future date"
```

### Define Validation Rules

```
Password Validation:
- Minimum length: 8 characters
- Maximum length: 128 characters
- Must contain: uppercase, lowercase, number, special character
- Cannot contain: username, email, common passwords

Email Validation:
- Format: standard email format
- Max length: 255 characters
- Must be unique in system
- Disposable email domains not allowed

Username Validation:
- Length: 3-20 characters
- Characters: alphanumeric, underscore, hyphen
- Must start with letter
- Cannot be: "admin", "root", "system" (reserved)
```

### Specify User Feedback

```
Success Messages:
- "Account created successfully"
- "Your changes have been saved"
- "Password reset email sent"

Error Messages:
- "Invalid email format"
- "Password must be at least 8 characters"
- "Email already registered"
- "Incorrect username or password"

Loading States:
- Show spinner during API calls
- Disable submit button while processing
- Show "Processing..." text

Empty States:
- "No items found"
- "Your cart is empty"
- "No results for your search"
```

---

## Common Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Too vague | "Works well" | "Page loads in under 2 seconds" |
| Implementation details | "Uses React hooks" | "Form maintains state correctly" |
| No error cases | Only happy path | Add error scenarios |
| Not measurable | "Fast", "intuitive" | Use specific metrics |
| Too broad | "User management" | Break into specific criteria |
| Missing edge cases | Normal flow only | Add boundary conditions |
| Ambiguous language | "Should", "might" | Use "must", "will" |
| Multiple criteria in one | "User can login and logout" | Split into separate criteria |

---

## Acceptance Criteria for Different Work Types

### Features

Focus on user actions, system responses, and validation.

```
Feature: User Registration

Acceptance Criteria:

Given-When-Then:
1. Given user is on registration page
   When user enters valid email and password
   Then account is created and verification email sent

2. Given user enters invalid email format
   When user submits form
   Then error message "Invalid email format" is displayed

3. Given user enters password less than 8 characters
   When user submits form
   Then error message "Password must be at least 8 characters" is displayed

4. Given user enters email that already exists
   When user submits form
   Then error message "Email already registered" is displayed

Checklist:
[ ] User can enter email and password
[ ] Email format is validated
[ ] Password requirements are enforced
[ ] Duplicate email is detected
[ ] Verification email is sent
[ ] Success message is displayed
[ ] User is redirected to dashboard
```

### Bug Fixes

Focus on reproduction steps no longer failing and root cause addressed.

```
Bug: Login fails when password contains special characters

Acceptance Criteria:

1. Given user has valid credentials
   When password contains special characters (!@#$%^&*)
   Then login is successful
   And user is redirected to dashboard

2. Given user enters invalid password with special characters
   When user submits login form
   Then error message "Invalid credentials" is displayed
   And account is not locked

3. Verify:
   [ ] Special characters in password work correctly
   [ ] No SQL injection vulnerability
   [ ] Password is still hashed correctly
   [ ] All existing passwords continue to work
```

### Performance

Focus on specific metrics and benchmarks.

```
Feature: Page Load Performance

Acceptance Criteria:

1. Homepage Performance:
   - Initial load time: < 2 seconds (P95)
   - Time to interactive: < 3 seconds (P95)
   - First contentful paint: < 1 second (P95)

2. API Performance:
   - Average response time: < 200ms
   - P95 response time: < 500ms
   - P99 response time: < 1 second

3. Database Performance:
   - Query execution time: < 100ms (P95)
   - Connection pool utilization: < 80%

4. Under Load:
   - 100 concurrent users: < 3 second response time (P95)
   - 500 concurrent users: < 5 second response time (P95)
   - 1000 concurrent users: < 10 second response time (P95)

5. Verify:
   [ ] Meets all performance targets
   [ ] No memory leaks under load
   [ ] Graceful degradation under high load
```

### Refactoring

Focus on no behavior change and tests still passing.

```
Refactoring: Extract user authentication service

Acceptance Criteria:

1. Behavior Preservation:
   - All existing authentication flows work identically
   - No changes to API contracts
   - No changes to database schema

2. Code Quality:
   - Authentication logic is in separate service
   - Code is more maintainable and testable
   - No code duplication

3. Testing:
   [ ] All existing tests pass
   [ ] New unit tests for authentication service
   [ ] Integration tests verify behavior unchanged
   [ ] Manual testing confirms no regressions

4. Documentation:
   [ ] Code comments updated
   [ ] API documentation unchanged
   [ ] Architecture diagram updated
```

---

## Definition of Done (DoD)

Definition of Done is broader than acceptance criteria - it's the checklist for completing any work item.

### Typical DoD Checklist

```
Definition of Done

Code Quality:
[ ] Code follows style guidelines
[ ] Code is self-documenting (clear names, comments)
[ ] No TODO comments without tickets
[ ] No console.log or debug code

Testing:
[ ] Unit tests written (coverage > 80%)
[ ] Integration tests written
[ ] All tests passing
[ ] Manual testing completed

Review:
[ ] Code reviewed by at least one peer
[ ] Review comments addressed
[ ] Approval received

Documentation:
[ ] README updated (if needed)
[ ] API documentation updated (if API change)
[ ] User-facing documentation updated (if needed)

Security:
[ ] No hardcoded secrets or credentials
[ ] Input validation implemented
[ ] Output encoding implemented (XSS prevention)
[ ] SQL injection prevention verified

Performance:
[ ] No N+1 query problems
[ ] No unnecessary database calls
[ ] Caching implemented where appropriate

Deployment:
[ ] Deployed to staging environment
[ ] Smoke tests passed on staging
[ ] Rollback plan documented

Stakeholder:
[ ] Demoed to product owner
[ ] Acceptance criteria verified
[ ] Sign-off received

Monitoring:
[ ] Logging implemented
[ ] Error tracking configured
[ ] Metrics defined and tracked
```

### DoD vs Acceptance Criteria

| Aspect | Acceptance Criteria | Definition of Done |
|--------|-------------------|-------------------|
| Scope | Specific to work item | Applies to all work |
| Focus | What was built | How it was built |
| Owner | Product owner defines | Team defines |
| Content | Business value | Quality standards |
| Example | "User can login" | "Code reviewed, tests pass" |

---

## Verification Methods

### Manual Testing

QA follows the acceptance criteria step by step.

```
Manual Test Plan for User Registration

Test Case 1: Successful Registration
Steps:
1. Navigate to /register
2. Enter valid email: test@example.com
3. Enter valid password: Passw0rd!
4. Click "Sign Up"

Expected Results:
- Account created in database
- Verification email sent
- Redirected to /dashboard
- Success message displayed

Actual Results: _________________
Status: Pass / Fail
```

### Automated Tests

E2E tests verify each criterion automatically.

```javascript
// Example: Cypress E2E test
describe('User Registration', () => {
  it('should register with valid credentials', () => {
    cy.visit('/register')
    cy.get('[data-testid="email"]').type('test@example.com')
    cy.get('[data-testid="password"]').type('Passw0rd!')
    cy.get('[data-testid="submit"]').click()

    // Verify acceptance criteria
    cy.url().should('include', '/dashboard')
    cy.get('[data-testid="success-message"]').should('contain', 'Account created')
  })

  it('should show error for invalid email', () => {
    cy.visit('/register')
    cy.get('[data-testid="email"]').type('invalid-email')
    cy.get('[data-testid="password"]').type('Passw0rd!')
    cy.get('[data-testid="submit"]').click()

    // Verify acceptance criteria
    cy.get('[data-testid="error-message"]').should('contain', 'Invalid email format')
    cy.url().should('include', '/register')
  })
})
```

### Demo to Stakeholder

Show the feature working in a live demo.

```
Demo Script for User Registration

1. Introduction (1 min)
   - "Today I'll demo the user registration feature"

2. Happy Path (2 min)
   - "I'll register a new user with valid credentials"
   - Show each step
   - Highlight success message and redirect

3. Error Cases (2 min)
   - "Now let's try with invalid email"
   - Show error message
   - "Now with duplicate email"
   - Show error message

4. Edge Cases (1 min)
   - "Let's test password requirements"
   - Show various password scenarios

5. Q&A (remaining time)
   - Answer stakeholder questions
```

---

## Handling Ambiguity

When acceptance criteria are unclear, take action.

### Strategies

1. **Write multiple scenarios**
   - Cover different interpretations
   - Ask which is correct

2. **Add "Questions" section**
   - List unclear points
   - Get clarification before starting

3. **Get stakeholder clarification**
   - Schedule meeting
   - Walk through scenarios
   - Document decisions

4. **Update criteria with answers**
   - Remove ambiguity
   - Be specific

### Example: Ambiguous Criteria

```
Ambiguous: "User can upload files"

Questions:
- What file types are allowed?
- What is the maximum file size?
- Is there a limit on number of files?
- What happens if upload fails?
- Are virus scans required?

Clarified:
- User can upload files (PDF, JPG, PNG, DOCX)
- Maximum file size: 10MB
- Maximum files per upload: 5
- On failure: Show error message with reason
- All files scanned for viruses before processing
```

---

## Example Acceptance Criteria

### Example 1: User Registration Feature

```
Feature: User Registration

User Story:
As a new user
I want to register with email and password
So that I can create an account

Acceptance Criteria:

Given-When-Then Scenarios:

1. Successful Registration
   Given the user is on the registration page
   And the user has not registered before
   When the user enters a valid email address
   And the user enters a valid password (8+ chars, mixed types)
   And the user clicks "Sign Up"
   Then a new user account is created with status "unverified"
   And a verification email is sent to the user's email
   And the user is redirected to the dashboard
   And a success message "Account created! Check your email to verify" is displayed

2. Invalid Email Format
   Given the user is on the registration page
   When the user enters an invalid email format (no @ symbol)
   And the user enters a valid password
   And the user clicks "Sign Up"
   Then no account is created
   And an error message "Invalid email format" is displayed
   And the user remains on the registration page

3. Password Too Short
   Given the user is on the registration page
   When the user enters a valid email address
   And the user enters a password with less than 8 characters
   And the user clicks "Sign Up"
   Then no account is created
   And an error message "Password must be at least 8 characters" is displayed

4. Duplicate Email
   Given the user is on the registration page
   And an account with email "test@example.com" already exists
   When the user enters "test@example.com"
   And the user enters a valid password
   And the user clicks "Sign Up"
   Then no account is created
   And an error message "Email already registered" is displayed

Checklist:
[ ] User can enter email and password
[ ] Email format is validated (regex: standard email pattern)
[ ] Password is validated (8+ chars, uppercase, lowercase, number, special char)
[ ] Duplicate email is detected
[ ] Account is created with "unverified" status
[ ] Verification email is sent
[ ] Success message is displayed
[ ] User is redirected to dashboard
[ ] Error messages are clear and helpful
[ ] Form fields are cleared on successful submission
[ ] Submit button is disabled during processing
[ ] Loading indicator is shown during processing
```

### Example 2: Payment Processing

```
Feature: Payment Processing

User Story:
As a customer
I want to pay for my order with a credit card
So that I can complete my purchase

Acceptance Criteria:

Given-When-Then Scenarios:

1. Successful Payment
   Given the user has items in their cart
   And the user is on the checkout page
   When the user enters valid card details
   And the user clicks "Pay Now"
   Then the payment is processed successfully
   And the order is confirmed
   And a confirmation email is sent
   And the user is redirected to the order confirmation page
   And the order status is set to "paid"

2. Payment Declined
   Given the user is on the checkout page
   When the user enters card details that will be declined
   And the user clicks "Pay Now"
   Then the payment is declined
   And an error message "Payment declined. Please try another card" is displayed
   And the order is not created
   And the user remains on the checkout page

3. Insufficient Funds
   Given the user is on the checkout page
   When the user enters card details with insufficient funds
   And the user clicks "Pay Now"
   Then the payment is declined
   And an error message "Insufficient funds" is displayed

4. Network Error
   Given the user is on the checkout page
   When the payment gateway is unreachable
   And the user clicks "Pay Now"
   Then an error message "Payment service unavailable. Please try again" is displayed
   And the user can retry the payment

Checklist:
[ ] User can enter card number (16 digits, Luhn validated)
[ ] User can enter expiry date (MM/YY format, future date only)
[ ] User can enter CVV (3-4 digits)
[ ] Card details are validated before submission
[ ] Payment is processed via Stripe API
[ ] Order is created only on successful payment
[ ] Confirmation email is sent
[ ] Error messages are user-friendly
[ ] Card details are never stored (PCI compliance)
[ ] Payment processing is secure (HTTPS)
[ ] Loading state shown during processing
[ ] Retry option available on failure
```

### Example 3: Search Functionality

```
Feature: Product Search

User Story:
As a customer
I want to search for products
So that I can find what I'm looking for

Acceptance Criteria:

Given-When-Then Scenarios:

1. Successful Search
   Given the user is on the products page
   When the user enters a search term
   And the user clicks "Search" or presses Enter
   Then products matching the search term are displayed
   And the search term is shown in the results header
   And the number of results is displayed

2. No Results Found
   Given the user is on the products page
   When the user enters a search term with no matches
   And the user clicks "Search"
   Then a "No results found" message is displayed
   And suggestions for similar products are shown

3. Empty Search
   Given the user is on the products page
   When the user clicks "Search" without entering a term
   Then an error message "Please enter a search term" is displayed
   And no search is performed

4. Search with Filters
   Given the user is on the products page
   When the user enters a search term
   And the user applies category and price filters
   And the user clicks "Search"
   Then results match both search term and filters

Checklist:
[ ] Search input field is available
[ ] Search works on product name
[ ] Search works on product description
[ ] Search is case-insensitive
[ ] Search handles partial matches
[ ] Results are sorted by relevance
[ ] Pagination is shown for >20 results
[ ] Loading indicator shown during search
[ ] Search term is highlighted in results
[ ] Recent searches are saved
[ ] Clear search button is available
[ ] Keyboard navigation supported (Enter to search)
```

### Example 4: Admin Dashboard

```
Feature: Admin User Management

User Story:
As an admin
I want to view and manage users
So that I can maintain the user base

Acceptance Criteria:

Given-When-Then Scenarios:

1. View User List
   Given the admin is logged in
   And the admin is on the admin dashboard
   When the admin navigates to "Users"
   Then a list of users is displayed
   And each user shows: name, email, status, registration date
   And the list is paginated (20 users per page)

2. Search Users
   Given the admin is on the users page
   When the admin enters a search term
   Then users matching the search are displayed
   And the search works on name and email

3. Deactivate User
   Given the admin is on the users page
   When the admin clicks "Deactivate" on a user
   And confirms the action
   Then the user status is set to "inactive"
   And the user cannot log in
   And a success message is displayed

4. View User Details
   Given the admin is on the users page
   When the admin clicks on a user
   Then the user details page is displayed
   And all user information is shown
   And user activity history is displayed

Checklist:
[ ] Admin can view all users
[ ] User list is paginated
[ ] Admin can search users by name or email
[ ] Admin can filter users by status (active/inactive)
[ ] Admin can deactivate users
[ ] Admin can activate users
[ ] Admin can view user details
[ ] Admin can view user activity history
[ ] Admin can export user list (CSV)
[ ] Actions require confirmation
[ ] Audit log tracks all admin actions
```

---

## Acceptance Criteria in User Stories

Complete user story with acceptance criteria.

```
User Story: Password Reset

As a user
I want to reset my password
So that I can regain access to my account

Acceptance Criteria:

1. User can click "Forgot Password" link on login page
2. User is redirected to password reset request page
3. User enters email address
4. System validates email format
5. System checks if email exists in database
6. If email exists:
   - Password reset link is generated
   - Reset link expires after 24 hours
   - Reset email is sent to user
   - Success message: "Password reset link sent to your email"
7. If email doesn't exist:
   - Same success message is shown (security: don't reveal email existence)
8. User clicks reset link from email
9. User is redirected to password reset page
10. User enters new password
11. Password must meet requirements (8+ chars, mixed types)
12. User confirms new password
13. Both passwords must match
14. On success:
    - Password is updated
    - User is redirected to login page
    - Success message: "Password reset successfully"
    - All existing sessions are invalidated
15. On expired link:
    - Error message: "Reset link has expired"
    - User can request new reset link
16. On already used link:
    - Error message: "Reset link has already been used"
    - User can request new reset link

Checklist:
[ ] Forgot password link visible on login page
[ ] Email format validation
[ ] Reset link expires after 24 hours
[ ] Reset link can only be used once
[ ] Password requirements enforced
[ ] Password confirmation required
[ ] All sessions invalidated after reset
[ ] Error messages are user-friendly
[ ] Security: don't reveal email existence
[ ] Rate limiting on reset requests (max 5 per hour)
```

---

## Sign-Off Process

Formal process for accepting completed work.

### Sign-Off Workflow

```
1. Development Complete
   Developer marks work as "Ready for Review"

2. QA Verification
   QA tests against acceptance criteria
   All criteria must pass

3. Product Owner Review
   Product owner reviews the feature
   Confirms it meets requirements

4. Sign-Off
   All criteria met → Approved
   Any issues → Back to development

5. Deployment
   Approved work can be deployed
```

### Sign-Off Checklist

```
Sign-Off Checklist

Developer:
[ ] All acceptance criteria implemented
[ ] Code reviewed and approved
[ ] All tests passing
[ ] Documentation updated
[ ] Ready for QA review

QA:
[ ] All acceptance criteria verified
[ ] Manual testing completed
[ ] Edge cases tested
[ ] No critical bugs found
[ ] Ready for product owner review

Product Owner:
[ ] Feature meets requirements
[ ] User experience is acceptable
[ ] Ready for deployment

Final Approval:
[ ] Approved for deployment
[ ] Deployment date scheduled
```

---

## Traceability

Link acceptance criteria to requirements and tests.

### Traceability Matrix

| Requirement | Acceptance Criteria | Test Case | Status |
|-------------|-------------------|-----------|--------|
| FR-1: User Registration | AC-1.1: Valid email signup | TC-REG-001 | Pass |
| FR-1: User Registration | AC-1.2: Invalid email error | TC-REG-002 | Pass |
| FR-1: User Registration | AC-1.3: Duplicate email error | TC-REG-003 | Pass |
| FR-2: User Login | AC-2.1: Valid credentials | TC-LOG-001 | Pass |
| FR-2: User Login | AC-2.2: Invalid credentials | TC-LOG-002 | Pass |

### Benefits of Traceability

- **Coverage verification** - All requirements have criteria
- **Test coverage** - All criteria have tests
- **Impact analysis** - Know what's affected by changes
- **Audit trail** - Track what was tested and approved

---

## Templates

### Acceptance Criteria Template

```markdown
# Acceptance Criteria: [Feature Name]

**User Story:**
As a [user type]
I want to [action]
So that [benefit]

## Given-When-Then Scenarios

### Scenario 1: [Scenario Name]
**Given** [context]
**When** [action]
**Then** [outcome]

### Scenario 2: [Scenario Name]
**Given** [context]
**When** [action]
**Then** [outcome]

## Checklist

Functional:
[ ] [Criterion 1]
[ ] [Criterion 2]
[ ] [Criterion 3]

Validation:
[ ] [Validation rule 1]
[ ] [Validation rule 2]

Error Handling:
[ ] [Error case 1]
[ ] [Error case 2]

Edge Cases:
[ ] [Edge case 1]
[ ] [Edge case 2]

## Questions
- [Question 1]
- [Question 2]
```

### Verification Checklist Template

```markdown
# Verification Checklist: [Feature Name]

**Date:** [Date]
**Tester:** [Name]

## Acceptance Criteria Verification

| Criteria | Test Method | Result | Notes |
|----------|-------------|--------|-------|
| [AC 1] | Manual/Auto | Pass/Fail | [Notes] |
| [AC 2] | Manual/Auto | Pass/Fail | [Notes] |
| [AC 3] | Manual/Auto | Pass/Fail | [Notes] |

## Test Cases

### TC-001: [Test Case Name]
Steps:
1. [Step 1]
2. [Step 2]

Expected: [Expected result]
Actual: [Actual result]
Status: Pass/Fail

## Bugs Found
- [Bug 1]: [Description]
- [Bug 2]: [Description]

## Sign-Off
[ ] All acceptance criteria met
[ ] Ready for deployment

Tester: _____________________ Date: _______
Product Owner: ________________ Date: _______
```

### User Story with AC Template

```markdown
# User Story: [Story Name]

**Priority:** [Must/Should/Could]
**Story Points:** [Number]
**Sprint:** [Sprint number]

## User Story
As a [user type]
I want to [action]
So that [benefit]

## Acceptance Criteria

### Scenario: [Happy Path]
Given [context]
When [action]
Then [outcome]

### Scenario: [Error Case 1]
Given [context]
When [action]
Then [outcome]

### Scenario: [Error Case 2]
Given [context]
When [action]
Then [outcome]

## Checklist
[ ] [Criterion 1]
[ ] [Criterion 2]
[ ] [Criterion 3]

## Definition of Done
[ ] Code reviewed
[ ] Tests written and passing
[ ] Documentation updated
[ ] QA verified
[ ] Product owner approved

## Notes
[Any additional notes]
```

---

## Best Practices

1. **Write criteria before development** - Not after
2. **Involve stakeholders** - Product owner should review
3. **Be specific** - No vague language
4. **Include all scenarios** - Happy path + error cases
5. **Make them testable** - Each criterion can be verified
6. **Keep them focused** - One feature per set of criteria
7. **Review regularly** - Update as requirements change
8. **Link to tests** - Ensure test coverage
9. **Get sign-off** - Formal approval before deployment
10. **Learn from experience** - Improve criteria writing over time

---

## Related Skills

- [Discovery Questions](../discovery-questions/SKILL.md) - Gather requirements before writing AC
- [Requirement to Scope](../requirement-to-scope/SKILL.md) - Define scope before writing AC
- [Constraints and Assumptions](../constraints-and-assumptions/SKILL.md) - Consider constraints in AC
- [Risk and Dependencies](../risk-and-dependencies/SKILL.md) - Address risks in AC
