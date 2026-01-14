# Code Review Best Practices

## Overview

Code review is a systematic examination of source code intended to find bugs, improve code quality, and share knowledge across the team. Effective code reviews catch defects early, enforce coding standards, and foster collaborative learning.

## Code Review Principles

### 1. Review the Code, Not the Author
- Focus on the code's behavior and quality, not personal preferences
- Assume positive intent from the author
- Separate the code from the person who wrote it

### 2. Be Timely
- Review PRs within 24 hours when possible
- Smaller, frequent reviews are better than large, delayed ones
- Don't let PRs sit unreviewed for days

### 3. Be Thorough but Practical
- Balance thoroughness with velocity
- Focus on what matters most: correctness, security, maintainability
- Not every line needs a comment

### 4. Share Knowledge
- Use reviews as teaching opportunities
- Explain the "why" behind suggestions
- Learn from code you're reviewing

### 5. Keep Reviews Small
- Ideal PR size: 200-400 lines of code
- Large PRs should be split into logical chunks
- Smaller PRs get better reviews and faster feedback

---

## What to Look For

### Code Quality and Readability

```typescript
// BAD: Unclear naming and magic numbers
function calc(d: number[]): number {
  let t = 0;
  for (let i = 0; i < d.length; i++) {
    if (d[i] > 100) t += d[i] * 0.1;
    else t += d[i] * 0.05;
  }
  return t;
}

// GOOD: Clear naming and constants
const HIGH_VALUE_THRESHOLD = 100;
const HIGH_VALUE_TAX_RATE = 0.1;
const STANDARD_TAX_RATE = 0.05;

function calculateTotalTax(transactions: number[]): number {
  return transactions.reduce((totalTax, amount) => {
    const taxRate = amount > HIGH_VALUE_THRESHOLD
      ? HIGH_VALUE_TAX_RATE
      : STANDARD_TAX_RATE;
    return totalTax + (amount * taxRate);
  }, 0);
}
```

**Check for:**
- Meaningful variable and function names
- Consistent formatting and style
- Appropriate comments (explain "why", not "what")
- Single responsibility principle
- DRY (Don't Repeat Yourself)
- Appropriate abstraction level

### Security Vulnerabilities

```typescript
// BAD: SQL Injection vulnerability
async function getUser(userId: string) {
  const query = `SELECT * FROM users WHERE id = '${userId}'`;
  return await db.query(query);
}

// GOOD: Parameterized query
async function getUser(userId: string) {
  const query = 'SELECT * FROM users WHERE id = $1';
  return await db.query(query, [userId]);
}
```

```typescript
// BAD: XSS vulnerability
function renderComment(comment: string) {
  document.innerHTML = `<div>${comment}</div>`;
}

// GOOD: Sanitized output
import DOMPurify from 'dompurify';

function renderComment(comment: string) {
  const sanitized = DOMPurify.sanitize(comment);
  document.innerHTML = `<div>${sanitized}</div>`;
}
```

**Check for:**
- Input validation and sanitization
- Authentication and authorization checks
- Sensitive data exposure (logs, error messages)
- Injection vulnerabilities (SQL, XSS, command injection)
- Secure defaults
- Proper error handling that doesn't leak information

### Performance Issues

```typescript
// BAD: N+1 query problem
async function getUsersWithOrders() {
  const users = await User.findAll();
  for (const user of users) {
    user.orders = await Order.findAll({ where: { userId: user.id } });
  }
  return users;
}

// GOOD: Eager loading
async function getUsersWithOrders() {
  return await User.findAll({
    include: [{ model: Order }]
  });
}
```

```typescript
// BAD: Unnecessary re-renders in React
function UserList({ users }) {
  const sortedUsers = users.sort((a, b) => a.name.localeCompare(b.name));
  return <ul>{sortedUsers.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}

// GOOD: Memoized computation
function UserList({ users }) {
  const sortedUsers = useMemo(
    () => [...users].sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  );
  return <ul>{sortedUsers.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

**Check for:**
- Database query efficiency (N+1, missing indexes)
- Unnecessary computations or re-renders
- Memory leaks
- Appropriate caching
- Algorithmic complexity (O(n²) vs O(n log n))
- Resource cleanup (connections, file handles)

### Testing Coverage

**Check for:**
- Unit tests for new functionality
- Edge cases and error conditions tested
- Integration tests for API endpoints
- Mocked dependencies where appropriate
- Test readability and maintainability
- No tests that always pass or are flaky

### Documentation

**Check for:**
- Updated README if needed
- API documentation for new endpoints
- JSDoc/docstrings for public functions
- Architecture decision records for significant changes
- Updated CHANGELOG if applicable

---

## Review Checklists

### General Code Quality Checklist

- [ ] Code is readable and self-documenting
- [ ] Variable and function names are descriptive
- [ ] No dead code or commented-out code
- [ ] No duplicated code (DRY principle)
- [ ] Functions are small and focused (single responsibility)
- [ ] Error handling is appropriate
- [ ] No hardcoded values (use constants/config)
- [ ] Code follows project style guide
- [ ] No unnecessary complexity
- [ ] Imports are organized and minimal

### Security Checklist

- [ ] Input is validated and sanitized
- [ ] No SQL/NoSQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Authentication/authorization checks in place
- [ ] Sensitive data is not logged
- [ ] Secrets are not hardcoded
- [ ] HTTPS is enforced where needed
- [ ] Rate limiting considered for public endpoints
- [ ] Error messages don't expose internal details
- [ ] Dependencies don't have known vulnerabilities

### Performance Checklist

- [ ] No N+1 query problems
- [ ] Database queries are optimized
- [ ] Appropriate indexes exist
- [ ] Caching is used where beneficial
- [ ] No memory leaks
- [ ] Large datasets are paginated
- [ ] Async operations are properly handled
- [ ] No blocking operations on main thread
- [ ] Resources are properly cleaned up
- [ ] Bundle size impact considered (frontend)

### Testing Checklist

- [ ] New code has appropriate test coverage
- [ ] Tests cover happy path and edge cases
- [ ] Tests cover error conditions
- [ ] Tests are readable and maintainable
- [ ] No flaky tests introduced
- [ ] Mocks are used appropriately
- [ ] Integration tests for critical paths
- [ ] Test names describe expected behavior

### API Design Checklist

- [ ] RESTful conventions followed
- [ ] HTTP methods used correctly
- [ ] Status codes are appropriate
- [ ] Response format is consistent
- [ ] Error responses are informative
- [ ] Pagination implemented for list endpoints
- [ ] API versioning considered
- [ ] Rate limiting implemented
- [ ] Request/response validation in place
- [ ] API documentation updated

---

## How to Give Feedback

### Be Constructive and Specific

```markdown
# BAD: Vague and unhelpful
"This code is confusing."

# GOOD: Specific and actionable
"The `processData` function handles both validation and transformation.
Consider splitting into `validateInput()` and `transformData()` for
better testability and clearer responsibilities."
```

### Use Questions Over Statements

```markdown
# BAD: Demanding
"Change this to use a Map instead of an object."

# GOOD: Collaborative
"Have you considered using a Map here? It would give us O(1)
lookups and preserve insertion order. What do you think?"
```

### Explain the Why

```markdown
# BAD: No context
"Add error handling here."

# GOOD: Educational
"If the API call fails, this will throw an unhandled exception and
crash the server. Consider wrapping in try/catch and returning a
meaningful error response to the client."
```

### Acknowledge Good Work

```markdown
# GOOD: Positive reinforcement
"Nice use of the builder pattern here - it makes the
configuration much more readable than a large constructor."
```

### Categorize Your Comments

Use prefixes to indicate severity:

```markdown
**[Blocking]** This SQL query is vulnerable to injection attacks.
Must use parameterized queries.

**[Suggestion]** Consider extracting this logic into a separate
function for better reusability.

**[Nitpick]** Minor: extra blank line at the end of the file.

**[Question]** Why did you choose to use recursion here instead
of iteration?

**[Praise]** Great test coverage on the edge cases!
```

### Comment Templates

```markdown
# For bugs
**Issue:** [Description of the problem]
**Impact:** [What could go wrong]
**Suggestion:** [How to fix it]

# For improvements
**Current:** [What the code does now]
**Suggested:** [What it could do better]
**Benefit:** [Why this is better]
```

---

## How to Receive Feedback

### Stay Open-Minded
- Remember: reviewers want to help improve the code
- Don't take feedback personally
- Consider each comment thoughtfully before responding

### Respond to All Comments
- Acknowledge every comment, even if just with a thumbs up
- If you disagree, explain your reasoning respectfully
- Ask clarifying questions if feedback is unclear

### Learn from Feedback
- Look for patterns in feedback you receive
- Use reviews as learning opportunities
- Thank reviewers for catching issues

### Know When to Push Back
- If you disagree, provide technical reasoning
- Reference documentation or best practices
- Offer alternatives if rejecting a suggestion

```markdown
# Example professional pushback
"Thanks for the suggestion! I considered using a Map, but in this
case we need JSON serialization for caching, and objects serialize
directly while Maps require additional handling. The dataset is
also small (<100 items) so the performance difference is negligible."
```

---

## Common Anti-Patterns to Catch

### 1. God Objects/Functions

```typescript
// ANTI-PATTERN: Function doing too much
async function handleUserRegistration(userData: UserInput) {
  // Validates input
  // Creates user in database
  // Sends welcome email
  // Creates default settings
  // Logs analytics event
  // Updates referral system
  // ... 200+ lines
}

// BETTER: Single responsibility
async function handleUserRegistration(userData: UserInput) {
  const validatedData = validateUserInput(userData);
  const user = await createUser(validatedData);
  await Promise.all([
    sendWelcomeEmail(user),
    createDefaultSettings(user.id),
    trackRegistrationEvent(user.id),
    processReferral(user.id, userData.referralCode),
  ]);
  return user;
}
```

### 2. Premature Optimization

```typescript
// ANTI-PATTERN: Over-optimized for no reason
const userCache = new LRUCache({ max: 10000 });
const userCacheIndex = new Map();
const userCacheStats = { hits: 0, misses: 0 };

function getUser(id: string) {
  // Complex caching logic for a function called 10 times/day
}

// BETTER: Simple solution until proven necessary
async function getUser(id: string) {
  return await db.users.findUnique({ where: { id } });
}
```

### 3. Stringly Typed Code

```typescript
// ANTI-PATTERN: Using strings for everything
function processOrder(status: string) {
  if (status === 'pending') { /* ... */ }
  else if (status === 'processing') { /* ... */ }
  else if (status === 'shipped') { /* ... */ }
}

// BETTER: Use enums or union types
type OrderStatus = 'pending' | 'processing' | 'shipped' | 'delivered';

function processOrder(status: OrderStatus) {
  // TypeScript catches typos at compile time
}
```

### 4. Boolean Blindness

```typescript
// ANTI-PATTERN: Multiple boolean parameters
createUser(name, email, true, false, true, false);

// BETTER: Use options object
createUser({
  name,
  email,
  isAdmin: true,
  isVerified: false,
  sendWelcomeEmail: true,
  requireMFA: false,
});
```

### 5. Copy-Paste Programming

```typescript
// ANTI-PATTERN: Duplicated validation logic
function validateCreateUser(data) {
  if (!data.email || !data.email.includes('@')) throw new Error('Invalid email');
  if (!data.name || data.name.length < 2) throw new Error('Invalid name');
}

function validateUpdateUser(data) {
  if (!data.email || !data.email.includes('@')) throw new Error('Invalid email');
  if (!data.name || data.name.length < 2) throw new Error('Invalid name');
}

// BETTER: Shared validation
const userSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
});

function validateCreateUser(data) {
  return userSchema.parse(data);
}

function validateUpdateUser(data) {
  return userSchema.partial().parse(data);
}
```

### 6. Callback Hell

```typescript
// ANTI-PATTERN: Nested callbacks
getUser(userId, (err, user) => {
  if (err) return handleError(err);
  getOrders(user.id, (err, orders) => {
    if (err) return handleError(err);
    getPayments(orders[0].id, (err, payments) => {
      if (err) return handleError(err);
      // ... more nesting
    });
  });
});

// BETTER: Async/await
async function getUserOrderPayments(userId: string) {
  const user = await getUser(userId);
  const orders = await getOrders(user.id);
  const payments = await getPayments(orders[0].id);
  return { user, orders, payments };
}
```

### 7. Swallowed Exceptions

```typescript
// ANTI-PATTERN: Silently swallowing errors
try {
  await saveToDatabase(data);
} catch (error) {
  // Nothing here - bug hides forever
}

// BETTER: Handle or rethrow
try {
  await saveToDatabase(data);
} catch (error) {
  logger.error('Database save failed', { error, data });
  throw new DatabaseError('Failed to save data', { cause: error });
}
```

---

## Automated Checks vs Manual Review

### What to Automate

| Check Type | Tools | Why Automate |
|------------|-------|--------------|
| Code formatting | Prettier, Black | Eliminates style debates |
| Linting | ESLint, Pylint | Catches common issues instantly |
| Type checking | TypeScript, mypy | Finds type errors before review |
| Security scanning | Snyk, npm audit | Finds known vulnerabilities |
| Test execution | Jest, pytest | Ensures tests pass |
| Code coverage | Istanbul, coverage.py | Tracks test coverage |
| Dependency updates | Dependabot, Renovate | Keeps dependencies current |
| Commit message format | commitlint | Enforces consistent messages |

### What Requires Human Review

| Aspect | Why Human Review |
|--------|------------------|
| Architecture decisions | Requires domain knowledge and judgment |
| Business logic correctness | Automated tools can't verify requirements |
| Code readability | Subjective assessment of clarity |
| Appropriate abstraction | Judgment call on when to abstract |
| Security logic | Business context needed for auth decisions |
| Performance trade-offs | Requires understanding of use cases |
| API design | UX and consistency considerations |
| Test quality | Are the right things being tested? |

### Recommended CI Pipeline

```yaml
# .github/workflows/pr-checks.yml
name: PR Checks

on: [pull_request]

jobs:
  automated-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: npm ci

      - name: Type check
        run: npm run type-check

      - name: Lint
        run: npm run lint

      - name: Format check
        run: npm run format:check

      - name: Run tests
        run: npm test -- --coverage

      - name: Security audit
        run: npm audit --audit-level=high

      - name: Check coverage threshold
        run: npm run coverage:check
```

---

## Review Process Workflow

### 1. Before Submitting a PR

**Author responsibilities:**
- [ ] Self-review your changes first
- [ ] Run all tests locally
- [ ] Update documentation if needed
- [ ] Write clear PR description
- [ ] Keep PR focused and appropriately sized
- [ ] Link related issues

### 2. PR Description Template

```markdown
## Summary
Brief description of what this PR does.

## Changes
- Added X feature
- Fixed Y bug
- Refactored Z component

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing performed

## Screenshots (if UI changes)
Before | After
--- | ---
img | img

## Related Issues
Closes #123
Related to #456

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests pass locally
```

### 3. During Review

**Reviewer responsibilities:**
- Review within 24 hours
- Start with understanding the goal
- Check the most critical areas first
- Leave actionable, constructive feedback
- Approve when satisfied, not when perfect

**Review order:**
1. Read the PR description and linked issues
2. Understand the high-level approach
3. Review the test changes first
4. Review the implementation
5. Check for edge cases and error handling
6. Verify documentation updates

### 4. After Review

**If changes requested:**
- Address all comments
- Mark conversations as resolved
- Request re-review when ready

**If approved:**
- Squash and merge (for clean history)
- Delete the feature branch
- Verify deployment if applicable

### 5. Review Metrics to Track

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Time to first review | < 24 hours | Keeps momentum |
| Review iterations | < 3 | Indicates clear requirements |
| PR size (lines changed) | < 400 | Smaller = better reviews |
| Review comments addressed | 100% | Ensures follow-through |
| Time to merge | < 3 days | Prevents stale PRs |

---

## Examples of Good vs Bad Review Comments

### Example 1: Bug Found

```markdown
# BAD
"This is wrong."

# GOOD
"**[Blocking]** This will throw a null reference error if `user.address`
is undefined. Consider using optional chaining:
```typescript
const city = user.address?.city ?? 'Unknown';
```"
```

### Example 2: Suggesting Improvement

```markdown
# BAD
"Use reduce."

# GOOD
"**[Suggestion]** This loop could be simplified with `reduce`:
```typescript
const total = items.reduce((sum, item) => sum + item.price, 0);
```
This is more idiomatic and handles the empty array case automatically."
```

### Example 3: Questioning Design

```markdown
# BAD
"Why did you do it this way?"

# GOOD
"**[Question]** I see you chose to fetch all users and filter in memory.
Was there a specific reason to avoid doing the filtering in the database
query? With large datasets, the database filter would be more efficient."
```

### Example 4: Security Concern

```markdown
# BAD
"Security issue here."

# GOOD
"**[Blocking - Security]** This endpoint accepts a `userId` from the
request body without verifying the authenticated user has permission
to access that user's data. This could allow users to access other
users' information.

Suggested fix:
```typescript
if (req.user.id !== userId && !req.user.isAdmin) {
  throw new ForbiddenError('Cannot access other user data');
}
```"
```

### Example 5: Positive Feedback

```markdown
# BAD
"LGTM"

# GOOD
"LGTM! Nice work on the error handling - the custom error classes
make debugging much easier. The test coverage is thorough too."
```

### Example 6: Nitpick

```markdown
# BAD
"Rename this."

# GOOD
"**[Nitpick]** Consider renaming `data` to `userProfile` for clarity,
since it specifically holds profile information. Not a blocker."
```

---

## Quick Reference Card

### Comment Prefixes
- `[Blocking]` - Must fix before merge
- `[Suggestion]` - Nice to have improvement
- `[Question]` - Need clarification
- `[Nitpick]` - Minor style preference
- `[Praise]` - Positive feedback

### Review Priorities (High to Low)
1. Security vulnerabilities
2. Correctness bugs
3. Performance issues
4. Test coverage
5. Code maintainability
6. Style consistency

### Golden Rules
1. Review code, not people
2. Be specific and actionable
3. Explain the "why"
4. Keep PRs small
5. Respond within 24 hours
6. Assume good intent
