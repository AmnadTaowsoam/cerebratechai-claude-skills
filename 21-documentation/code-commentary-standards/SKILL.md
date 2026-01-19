# Code Commentary Standards

## Overview

Code commentary (comments) should explain "why" code exists, not "what" it does. This skill provides standards for writing effective comments that help future developers and AI agents understand the intent, context, and reasoning behind code decisions.

**When to use this skill:** When writing code, reviewing code, or when comments would help explain complex logic, design decisions, or potential pitfalls.

## Table of Contents

1. [Commentary Principles](#commentary-principles)
2. [Anti-Patterns](#anti-patterns)
3. [Pro-Patterns](#pro-patterns)
4. [Comment Types](#comment-types)
5. [Agent-Friendly Comments](#agent-friendly-comments)
6. [Quick Reference](#quick-reference)

---

## Commentary Principles

### The "Why" Rule

**Core Principle:** Comments should explain the reasoning, not the mechanics.

**Bad Example:**
```javascript
// Increment counter
i++;
```

**Good Example:**
```javascript
// Increment counter to track retry attempts
// We limit to 3 retries to avoid infinite loops
i++;
```

### The "When to Comment" Rule

**Core Principle:** Comment when code doesn't explain itself.

**When to comment:**
- Complex algorithms
- Non-obvious business logic
- Workarounds or hacks
- Performance optimizations
- Security-sensitive operations
- API integrations with quirks

**When NOT to comment:**
- Obvious code (`i++` increments counter)
- Function names that are self-documenting
- Standard patterns (`if (err) return err`)
- Type definitions (use TypeScript instead)

### The "Audience" Rule

**Core Principle:** Write comments for the next developer who will maintain this code.

**Audience considerations:**
- New team members (explain context)
- Future you (explain reasoning)
- AI agents (explain intent clearly)
- External contributors (explain domain knowledge)

---

## Anti-Patterns

### Anti-Pattern 1: Commenting Obvious Code

**Don't comment what the code already says.**

**Bad:**
```javascript
// Check if user is authenticated
if (user.isAuthenticated) {
    // Return true
    return true;
}
```

**Good:**
```javascript
if (user.isAuthenticated) {
    return true;
}
```

### Anti-Pattern 2: Outdated Comments

**Don't let comments diverge from code.**

**Bad:**
```javascript
// Check if user is admin (TODO: update to use role-based check)
if (user.role === 'admin') {
    // Grant admin access
}
```

**Good:**
```javascript
// Check if user has admin role
// Note: We use role-based access control, not user.isAdmin flag
if (user.role === 'admin') {
    grantAdminAccess(user);
}
```

### Anti-Pattern 3: Commented-Out Code

**Don't leave commented-out code in production.**

**Bad:**
```javascript
// function oldProcess() {
//     // Old implementation
//     // return processOld(data);
// }
```

**Good:**
```javascript
// Old implementation removed in v2.0
// See git history for reference if needed
function newProcess(data) {
    return processNew(data);
}
```

### Anti-Pattern 4: Noise Comments

**Don't add comments that add no value.**

**Bad:**
```javascript
// Start of function
function processUser(user) {
    // Get user
    const userData = getUser(user.id);
    // Process user
    const processed = process(userData);
    // Return result
    return processed;
    // End of function
}
```

**Good:**
```javascript
function processUser(user) {
    const userData = getUser(user.id);
    const processed = process(userData);
    return processed;
}
```

### Anti-Pattern 5: Misleading Comments

**Don't write comments that contradict the code.**

**Bad:**
```javascript
// Always return user data
function getUserData(userId) {
    const user = database.find(userId);
    if (!user) {
        return null;  // Comment says always return, but we return null
    }
    return user;
}
```

**Good:**
```javascript
// Return user data or null if not found
function getUserData(userId) {
    const user = database.find(userId);
    return user || null;
}
```

---

## Pro-Patterns

### Pro-Pattern 1: Explain Design Decisions

**Document why you chose a specific approach.**

**Example:**
```javascript
/**
 * Using a Map instead of an object for user cache.
 * 
 * Rationale: Maps maintain insertion order and have O(1) lookup,
 * which is important for cache hit analysis. Objects have O(n) lookup
 * and don't guarantee order.
 */
const userCache = new Map();
```

### Pro-Pattern 2: Document Complex Algorithms

**Explain non-obvious logic.**

**Example:**
```javascript
/**
 * Implements the Boyer-Moore majority vote algorithm.
 * 
 * This algorithm finds the majority element in linear time O(n)
 * by maintaining a candidate and counter. When the counter drops to zero,
 * we switch candidates. The final candidate is the majority.
 * 
 * @param {Array} votes - Array of vote values
 * @returns {*} The majority value or null if no majority
 */
function findMajority(votes) {
    // Implementation...
}
```

### Pro-Pattern 3: Document Workarounds

**Explain why non-standard solutions were used.**

**Example:**
```javascript
/**
 * Using setTimeout to break the call stack.
 * 
 * Rationale: This is a workaround for a bug in the external API
 * where large payloads cause stack overflow. The API team is aware
 * (ticket #1234) and plans to fix in v3.0.
 * 
 * TODO: Remove this workaround when API v3.0 is deployed.
 */
async function processLargePayload(data) {
    await new Promise(resolve => setTimeout(resolve, 0));
    return externalApi.process(data);
}
```

### Pro-Pattern 4: Document Performance Trade-offs

**Explain performance-related decisions.**

**Example:**
```javascript
/**
 * Using a simple object instead of a Proxy for configuration.
 * 
 * Rationale: Proxies add ~15% overhead per property access.
 * For our read-heavy configuration (1000+ reads per request),
 * the overhead is significant. We accept the lack of dynamic updates
 * in exchange for better performance.
 * 
 * Trade-off: Performance vs. Flexibility - we chose performance.
 */
const config = {
    // Static configuration
};
```

### Pro-Pattern 5: Document Security Considerations

**Explain security-sensitive code.**

**Example:**
```javascript
/**
 * Validates user input using a whitelist approach.
 * 
 * Security: We use a whitelist of allowed characters instead of
 * blacklist filtering. This is more secure because:
 * 1. Whitelist explicitly defines what's allowed (fail-safe)
 * 2. Blacklist filtering can be bypassed with unexpected characters
 * 3. New attack vectors won't bypass whitelist
 * 
 * Performance: Regex whitelist is O(n) vs O(n*m) for blacklist
 */
function validateUsername(username) {
    const allowedChars = /^[a-zA-Z0-9_-]+$/;
    return allowedChars.test(username);
}
```

---

## Comment Types

### 1. Function/Method Comments

**Purpose:** Explain what the function does and why.

**Template:**
```javascript
/**
 * Brief description of what the function does.
 * 
 * @param {Type} paramName - Description of parameter
 * @returns {Type} Description of return value
 * 
 * Rationale/Context: Why this function exists or uses this approach
 */
function functionName(paramName) {
    // Implementation
}
```

**Example:**
```javascript
/**
 * Calculates the discounted price based on user tier and quantity.
 * 
 * We use tier-based discounting instead of percentage-based to
 * align with business rules. Tier-based is also more performant
 * (O(1) lookup vs O(n) calculation).
 * 
 * @param {number} basePrice - The original price
 * @param {string} userTier - The user's tier (bronze/silver/gold)
 * @param {number} quantity - The quantity being purchased
 * @returns {number} The discounted price
 */
function calculateDiscountedPrice(basePrice, userTier, quantity) {
    const tierDiscount = TIER_DISCOUNTS[userTier] || 0;
    const quantityDiscount = quantity > 10 ? 0.1 : 0;
    return basePrice * (1 - tierDiscount - quantityDiscount);
}
```

### 2. Inline Comments

**Purpose:** Explain non-obvious logic within a function.

**Template:**
```javascript
// Rationale: Why this code exists or uses this approach
const result = complexLogic();
```

**Example:**
```javascript
// Use Set for O(1) lookup instead of Array.includes() which is O(n)
// This is called in a hot path (user authentication) so performance matters
const allowedRoles = new Set(['admin', 'moderator', 'user']);

if (allowedRoles.has(user.role)) {
    // Grant access
}
```

### 3. TODO Comments

**Purpose:** Mark work that needs to be done.

**Template:**
```javascript
// TODO: [Action] - [Context] - [Optional: ticket/issue]
// Example: TODO: Refactor to use async/await - Ticket #123
```

**Example:**
```javascript
// TODO: Implement caching for this function - Performance issue #456
// Current latency: 200ms, Target: <50ms
function fetchUserData(userId) {
    return database.query(`SELECT * FROM users WHERE id = ${userId}`);
}
```

### 4. FIXME Comments

**Purpose:** Mark code that works but needs improvement.

**Template:**
```javascript
// FIXME: [Issue] - [Suggested fix]
// Example: FIXME: This has a race condition - Use mutex lock
```

**Example:**
```javascript
// FIXME: Race condition possible here if two requests process same user simultaneously
// Suggested fix: Implement distributed lock using Redis
async function updateUser(userId, data) {
    const user = await database.find(userId);
    user.update(data);
    await user.save();
}
```

### 5. HACK Comments

**Purpose:** Mark temporary or non-standard solutions.

**Template:**
```javascript
// HACK: [Reason] - [Cleanup plan]
// Example: HACK: Working around API bug #123 - Remove when v2.0 deployed
```

**Example:**
```javascript
// HACK: Temporary workaround for API rate limiting
// The API returns 429 errors during peak hours. We're adding
// exponential backoff to handle this gracefully.
// Cleanup plan: Remove when API team implements proper rate limiting (Q2 2026)
async function callApiWithRetry(url, data) {
    // Implementation with retry logic
}
```

### 6. NOTE Comments

**Purpose:** Provide additional context or warnings.

**Template:**
```javascript
// NOTE: [Important information]
// Example: NOTE: This function is deprecated - Use newFunction instead
```

**Example:**
```javascript
// NOTE: This function is deprecated and will be removed in v3.0
// Use processUserDataV2() instead which handles edge cases better
function processUserData(data) {
    // Old implementation
}
```

---

## Agent-Friendly Comments

### Writing Comments for AI Agents

AI agents benefit from comments that clearly explain intent, context, and reasoning.

### Principle 1: Explicit Intent

**State what you're trying to achieve.**

**Example:**
```javascript
// Intent: We want to ensure the user has at least one active subscription
// before allowing access to premium features.
if (user.subscriptions.some(s => s.isActive)) {
    grantPremiumAccess(user);
}
```

### Principle 2: Explain Constraints

**Document business or technical constraints.**

**Example:**
```javascript
// Constraint: Payment gateway requires amounts in cents (not dollars)
// to avoid floating-point precision issues.
const amountInCents = Math.round(amount * 100);

// Constraint: Maximum amount is $10,000 (1,000,000 cents)
if (amountInCents > 1000000) {
    throw new Error('Amount exceeds maximum');
}
```

### Principle 3: Explain Edge Cases

**Document how edge cases are handled.**

**Example:**
```javascript
// Edge case: User may have no email (social login only)
// We handle this by generating a placeholder email for notifications
const email = user.email || `${user.id}@placeholder.internal`;

// Edge case: Email may be invalid format
// We validate and fall back to in-app notifications if invalid
if (isValidEmail(email)) {
    sendEmailNotification(user, email);
} else {
    sendInAppNotification(user);
}
```

### Principle 4: Link to Documentation

**Reference external docs for complex topics.**

**Example:**
```javascript
// See: https://docs.company.com/algorithm/boyer-moore
// for detailed explanation of this majority vote algorithm
function findMajority(votes) {
    // Implementation
}
```

### Principle 5: Explain Alternatives Considered

**Document why other approaches weren't chosen.**

**Example:**
```javascript
// Alternative considered: Use a third-party validation library
// Rejected: Adds 50KB to bundle size for simple validation
// Chosen: Custom regex validation (2KB)
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}
```

---

## Quick Reference

### Comment Decision Matrix

| Situation | Comment Type | Example |
|-----------|--------------|---------|
| **Complex algorithm** | Function comment with rationale | `/** Implements Boyer-Moore algorithm... */` |
| **Design decision** | Inline comment explaining why | `// Using Map for O(1) lookup...` |
| **Workaround** | HACK comment with cleanup plan | `// HACK: Working around API bug #123...` |
| **Future work** | TODO with context | `// TODO: Add caching - Ticket #456` |
| **Known issue** | FIXME with suggested fix | `// FIXME: Race condition - Use mutex lock` |
| **Deprecation** | NOTE with replacement | `// NOTE: Deprecated - Use newFunction()` |

### Comment Quality Checklist

```markdown
## Comment Quality Checklist

### Content
- [ ] Explains "why" not "what"
- [ ] Provides context or reasoning
- [ ] Accurate and up-to-date
- [ ] Doesn't contradict code

### Clarity
- [ ] Uses clear, concise language
- [ ] Avoids jargon unless necessary
- [ ] Follows consistent style

### Relevance
- [ ] Adds value to understanding
- [ ] Not redundant with code
- [ ] Not stating the obvious

### Agent-Friendly
- [ ] Explains intent clearly
- [ ] Documents constraints
- [ ] Mentions edge cases
- [ ] Links to external docs when needed
```

### Common Comment Patterns

| Pattern | When to Use | Example |
|---------|--------------|---------|
| **Algorithm explanation** | Non-obvious logic | `// Using two-pointer technique for O(n) search` |
| **Performance note** | Optimization | `// Caching here to avoid N+1 database queries` |
| **Security note** | Sensitive operations | `// Input sanitized to prevent SQL injection` |
| **Workaround** | Non-standard solution | `// HACK: Bypassing API rate limit with backoff` |
| **Business rule** | Domain logic | `// Business rule: Free tier limited to 5 projects` |
| **External reference** | Complex topic | `// See RFC 3921 for protocol details` |

---

## Common Pitfalls

1. **Over-commenting** - Don't comment obvious code
2. **Under-commenting** - Comment complex logic that isn't obvious
3. **Outdated comments** - Keep comments in sync with code
4. **Misleading comments** - Ensure comments match code behavior
5. **Commented-out code** - Remove old code, don't comment it out
6. **Noise comments** - Every line doesn't need a comment
7. **Vague comments** - Be specific about what and why
8. **No rationale** - Explain design decisions and trade-offs

## Additional Resources

- [Google JavaScript Style Guide - Comments](https://google.github.io/styleguide/jsguide.html#comments)
- [Clean Code Comments](https://github.com/ryanmcdermott/clean-code-javascript#comments)
- [Writing Comments](https://stackoverflow.blog/2021/12/15/writing-comments)
