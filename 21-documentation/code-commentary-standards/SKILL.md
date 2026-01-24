---
name: Code Commentary Standards
description: Standards for writing effective code comments that explain "why" code exists, helping future developers and AI agents understand intent, context, and reasoning behind code decisions.
---

# Code Commentary Standards

> **Current Level:** Expert (Enterprise Scale)
> **Domain:** Documentation / Code Quality

---

## Overview

Code commentary (comments) should explain "why" code exists, not "what" it does. This skill provides standards for writing effective comments that help future developers and AI agents understand the intent, context, and reasoning behind code decisions.

---

## 1. Executive Summary & Strategic Necessity

* **Context:** ในปี 2025-2026 Code Commentary Standards ด้วย Best Practices ช่วย Code Quality ที่มีอัตโนมาติการทำงานอัตโนมาติ (Code Commentary) ใน Enterprise Scale

* **Business Impact:** Code Commentary Standards ช่วยลด Downtime ของระบบ Customer Support ผ่านการตอบคำถามอัตโนมาติการเขียนเอกสาร (Reduce onboarding time), ลดต้นทุนการจัดการทีม (Increase code maintainability), เพิ่มอัตรากำไร Gross Margin ผ่านการทำงานอัตโนมาติ (Faster debugging), และปรับประสบทการทำงาน (Consistent code quality)

* **Product Thinking:** Code Commentary Standards ช่วยแก้ปัญหา (Pain Point) ความต้องการมีการเขียนเอกสารที่ชัดเจน (Developers need clear comments) ผ่านการทำงานอัตโนมาติ (Standardized comments)

---

## 2. Technical Deep Dive (The "How-to")

* **Core Logic:** Code Commentary Standards ใช้ Best Practices ช่วย Code Quality ทำงานอัตโนมาติ:
  1. **Commentary Principles**: กำหนด Commentary Principles (The "Why" Rule, The "When to Comment" Rule, The "Audience" Rule)
  2. **Comment Types**: จัดหมวด Comment Types (Function comments, Inline comments, Block comments, TODO comments)
  3. **Comment Templates**: สร้าง Comment Templates สำหรับการเขียน comments (Function template, Inline template)
  4. **Comment Quality**: จัดการ Comment Quality (Accuracy, Completeness, Clarity)
  5. **Agent-Friendly Comments**: สร้าง Agent-Friendly Comments สำหรับ AI Agents (Intent, Constraints, Edge Cases)

* **Architecture Diagram Requirements:** แผนผังระบบ Code Commentary Standards ต้องมีองค์ประกอบ:
  1. **Commentary Guidelines**: Commentary Guidelines สำหรับการเขียน comments (Comment Principles, Comment Types)
  2. **Comment Templates**: Comment Templates สำหรับการเขียน comments (Function template, Inline template)
  3. **Comment Quality Check**: Comment Quality Check สำหรับการตรวจสอบ comments (Accuracy, Completeness, Clarity)
  4. **Agent-Friendly Comment Generator**: Agent-Friendly Comment Generator สำหรับการสร้าง comments สำหรับ AI Agents
  5. **Comment Linter**: Comment Linter สำหรับการตรวจสอบ comment quality (ESLint, TSLint)
  6. **CI/CD Integration**: CI/CD Integration สำหรับการตรวจสอบ comment quality (Pre-commit hooks, CI checks)
  7. **Observability**: Logging, Monitoring, Tracing สำหรับการ debug และปรับสิทท

* **Implementation Workflow:** ขั้นตอนการนำ Code Commentary Standards ไปใช้งานจริง:
  1. **Planning Phase**: กำหนด Requirement และเลือก Comment Standards ที่เหมาะสม
  2. **Commentary Guidelines Setup**: ตั้งค่า Commentary Guidelines สำหรับการเขียน comments
  3. **Comment Templates Creation**: สร้าง Comment Templates สำหรับการเขียน comments
  4. **Comment Linter Setup**: ตั้งค่า Comment Linter สำหรับการตรวจสอบ comment quality
  5. **CI/CD Integration**: ผสาน Comment Linter เข้ากับ CI/CD pipeline
  6. **Testing Phase**: Unit test, Integration test, E2E test ด้วยจริง Scenario
  7. **Deployment**: Deploy ด้วย CI/CD pipeline, Set up Monitoring
  8. **Optimization**: Optimize comment quality, Add comment templates, Improve UX
  9. **Maintenance**: Monitor comment quality, Update Comment Standards, Handle edge cases

---

## 3. Tooling & Tech Stack

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้สำหรับ Code Commentary Standards ใน Enterprise Scale:
  1. **ESLint**: JavaScript/TypeScript Linter สำหรับ enforcing comment quality
  2. **TSLint**: TypeScript Linter สำหรับ enforcing comment quality
  3. **JSDoc**: JavaScript documentation generator สำหรับ API documentation
  4. **TSDoc**: TypeScript documentation generator สำหรับ API documentation
  5. **Comment Linter Plugins**: Comment Linter plugins สำหรับ enforcing comment standards (eslint-plugin-jsdoc, eslint-plugin-tsdoc)
  6. **Husky**: Git hooks สำหรับ enforcing comment quality before commit
  7. **Commitlint**: Commit message linter สำหรับ enforcing conventional commits
  8. **GitHub Actions**: CI/CD platform สำหรับ automated comment quality checks
  9. **GitLab CI**: CI/CD platform สำหรับ automated comment quality checks
  10. **SonarQube**: Code quality platform สำหรับ tracking comment coverage

* **Configuration Essentials:** การตั้งค่าสำคัญสำหรับให้ระบบเสถียร Code Commentary Standards:
  1. **Comment Standards**: ตั้งค่า Comment Standards (Comment Principles, Comment Types)
  2. **Comment Templates**: ตั้งค่า Comment Templates (Function template, Inline template)
  3. **Comment Linter Rules**: ตั้งค่า Comment Linter Rules (Comment format, Comment completeness)
  4. **CI/CD Configuration**: ตั้งค่า CI/CD Configuration สำหรับ comment quality checks
  5. **Monitoring**: ตั้งค่า Monitoring สำหรับ tracking comment quality (Comment coverage, Comment accuracy)
  6. **Secret Management**: Use Environment variables หรือ Secret Manager (AWS Secrets Manager, HashiCorp Vault)
  7. **Rate Limiting**: Per-user และ Per-IP rate limits สำหรับป้องกัน Abuse (100-1000 requests/hour)
  8. **Logging Level**: INFO สำหรับ Production, DEBUG สำหรับ Development
  9. **Observability**: Track success rate, comment coverage, comment quality ต่อเป้าหลาย
  10. **Documentation**: Maintain Comment Standards documentation สำหรับ team reference

---

## 4. Standards, Compliance & Security

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  1. **ISO/IEC 27001**: Information Security Management - สำหรับการจัดการ Secrets และ Access Control
  2. **ISO/IEC 27017**: Code of Practice for Information Security Controls - สำหรับ Secure Development
  3. **GDPR**: General Data Protection Regulation - สำหรับการจัดการ Personal Data และ User Consent
  4. **SOC 2 Type II**: Security Controls - สำหรับการ Audit และ Compliance
  5. **JSDoc/TSDoc Standards**: Documentation standards สำหรับ JavaScript/TypeScript

* **Security Protocol:** กลไกการป้องกัน Code Commentary Standards:
  1. **Input Validation**: Validate และ Sanitize ทุก Input ก่อน processing (Prevent XSS, SQL injection)
  2. **Output Sanitization**: Filter sensitive information จาก comments (API keys, Secrets)
  3. **Access Control**: RBAC (Role-Based Access Control) สำหรับ comment access - บาง comments internal only
  4. **Audit Trail**: Log ทุก comment access ด้วย Timestamp, User ID, และ Page accessed (สำหรับ Forensics และ Compliance)
  5. **Rate Limiting**: Per-user และ Per-IP rate limits สำหรับป้องกัน Abuse (100-1000 requests/hour)
  6. **Secure Communication**: TLS 1.3 สำหรับ HTTPS access
  7. **Secret Management**: Use Environment variables หรือ Secret Manager (AWS Secrets Manager, HashiCorp Vault)
  8. **Content Security**: CSP headers สำหรับ preventing XSS attacks
  9. **Authentication**: Implement authentication สำหรับ internal comments (SSO, OAuth)
  10. **Data Encryption**: Encrypt sensitive data ที่ rest ใน Database (AES-256 หรือ Customer-managed keys)

* **Explainability:** (สำหรับ Comments) ความสามารถในการอธิบายผลลัพธ์ผ่านเทคนิค:
  1. **Clear Structure**: เก็บ comment structure สำหรับ easy understanding
  2. **Detailed Explanations**: Provide detailed explanations สำหรับ complex logic
  3. **Context Information**: Include context information สำหรับ understanding code decisions
  4. **Reference Links**: Link to external documentation สำหรับ complex topics
  5. **Examples**: Provide examples สำหรับ comment patterns

---

## 5. Unit Economics & Performance Metrics (KPIs)

* **Cost Calculation:** สูตรการคำนวณต้นทุกต่อหน่วย Code Commentary Standards:
  1. **CI/CD Cost** = CI/CD minutes × Cost per minute
     - GitHub Actions: Free tier + $0.008/minute
     - GitLab CI: Free tier + $0.014/minute
  2. **Storage Cost** = Comment documentation storage × Cost per GB/month
     - GitHub Pages: Free
     - GitLab Pages: Free
     - S3: $0.023/GB/month
  3. **Domain Cost** = Domain registration ($10-15/year)
  4. **SSL Certificate Cost** = $0 (Let's Encrypt) or $50-100/year (paid)
  5. **Total Monthly Cost** = CI/CD Cost + Storage Cost + Domain Cost + SSL Cost
  6. **Infrastructure Costs** = Compute ($0/month for static sites) + Storage ($0/month for static sites) + Monitoring ($0/month for static sites)

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  1. **Comment Coverage**: เปอร์เซ็นต์ของ functions ที่มี comments (Target: >80%)
  2. **Comment Quality Score**: คะแนน comment quality จาก automated checks (Target: >4.0)
  3. **Comment Accuracy**: เปอร์เซ็นต์ของ comments ที่ตรงกับ code (Target: >95%)
  4. **Comment Completeness**: เปอร์เซ็นต์ของ comments ที่มี context (Target: >90%)
  5. **Developer Satisfaction Score**: 1-5 rating จาก Developer feedback (Target: >4.0)
  6. **Error Rate**: อัตราการ Error (Target: <1%)
  7. **Onboarding Time**: เวลาการ onboarding developers (Target: <1 week)
  8. **Code Review Time**: เวลาการ code review (Target: <30 minutes per PR)
  9. **Bug Fix Time**: เวลาการ bug fix ด้วย good comments (Target: <1 day)
  10. **Knowledge Transfer**: เปอร์เซ็นต์ของ knowledge transfer (Target: >80%)

---

## 6. Strategic Recommendations (CTO Insights)

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน Code Commentary Standards เพื่อลดความเสี่ยง:
  1. **Phase 1: MVP (1-2 เดือน)**: Deploy Simple Code Commentary Standards ด้วย Comment Guidelines และ Manual review สำหรับ Internal team ก่อนเปิดให้ Public
     - **Goal**: Validate Code Commentary Standards architecture และ gather feedback
     - **Success Criteria**: >80% comment coverage, <30s review time
     - **Risk Mitigation**: Internal-only access, Manual review ก่อน Public
  2. **Phase 2: Beta (2-3 เดือน)**: Expand ด้วย Comment Linter และ CI/CD Integration สำหรับ Selected customers
     - **Goal**: Test scalability และ Comment reliability
     - **Success Criteria**: >90% comment coverage, <15s review time
     - **Risk Mitigation**: Canary deployment, Feature flags, Gradual rollout
  3. **Phase 3: GA (3-6 เดือน)**: Full rollout ด้วย Advanced features (Comment Templates, Agent-Friendly Comments, Automated Documentation)
     - **Goal**: Enterprise-grade comment quality และ Performance
     - **Success Criteria**: >95% comment coverage, <10s review time, 99.9% uptime
     - **Risk Mitigation**: Load testing, Disaster recovery, Blue-green deployment

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาดในระดับ Enterprise Scale:
  1. **Over-engineering**: สร้าง Code Commentary Standards ที่ซ้อนเกินไป (Too many rules, Complex templates) → เริ่มจาก Simple และ iterate
  2. **No Comment Linter**: ไม่มี Comment Linter ทำให้ Comment quality ลด → Implement Comment Linter ด้วย ESLint/TSLint
  3. **Outdated Comments**: Comments ไม่ sync กับ code → Implement automated comment quality checks
  4. **Missing Comment Types**: ไม่มี Comment Types ทำให้ developers สับสนใจ → Implement clear comment type guidelines
  5. **No Comment Templates**: ไม่มี Comment Templates ทำให้ consistency → Implement comment templates สำหรับ common patterns
  6. **No Agent-Friendly Comments**: ไม่มี Agent-Friendly Comments ทำให้ AI Agents สับสนใจ → Implement Agent-Friendly comment guidelines
  7. **No CI/CD Integration**: ไม่มี CI/CD Integration ทำให้ manual review → Implement automated comment quality checks
  8. **Poor Comment Quality**: Comments ไม่มี quality ทำให้ code understanding → Implement comment quality metrics
  9. **No Comment Documentation**: ไม่มี Comment Documentation ทำให้ team reference → Maintain Comment Standards documentation
  10. **Single Point of Failure**: ไม่มี Redundancy หรือ Fallback → Deploy multiple instances ด้วย CDN

---

## Core Concepts

### 1. Commentary Principles

### The "Why" Rule

**Core Principle:** Comments should explain "why" code exists, not "what" it does.

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

## 2. Anti-Patterns

### Anti-Pattern 1: Commenting Obvious Code

**Don't comment what code already says.**

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
    grantAdminAccess(user);
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

**Don't write comments that contradict code.**

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

## 3. Pro-Patterns

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

## 4. Comment Types

### 1. Function/Method Comments

**Purpose:** Explain what a function does and why.

**Template:**
```javascript
/**
 * Brief description of what the function does.
 * 
 * Rationale/Context: Why this function exists or uses this approach
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
 * (O(1) lookup vs O(n*m) calculation).
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

## 5. Agent-Friendly Comments

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

---

## 6. Quick Start

### Good Comment Examples

```python
# ✅ Good - Explains WHY
# Using binary search because list is sorted and we need O(log n) performance
def find_user(user_id: int, users: List[User]) -> Optional[User]:
    # Implementation...
```

```python
# ✅ Good - Explains business context
# Business rule: Free tier users limited to 5 projects to prevent abuse
if user.tier == 'free' and len(user.projects) >= 5:
    raise LimitExceeded()
```

```python
# ✅ Good - Explains non-obvious behavior
# Cache expires after 1 hour, but we check every 5 minutes to avoid
# serving stale data during high traffic periods.
CACHE_TTL = 3600
CACHE_CHECK_INTERVAL = 300
```

### Bad Comment Examples

```python
# ❌ Bad - States the obvious
# Add 1 to counter
counter += 1
```

```python
# ❌ Bad - Outdated comment
# TODO: Fix this bug (from 2020, bug already fixed)
def process_data(data):
    # Fixed implementation
```

---

## Production Checklist

- [ ] **Purpose**: Comments explain "why", not "what"
- [ ] **Complex Logic**: Complex algorithms and business rules documented
- [ ] **Non-Obvious**: Non-obvious behavior explained
- [ ] **Context**: Historical context and decisions documented
- [ ] **Accuracy**: Comments match actual code behavior
- [ ] **Updates**: Comments updated when code changes
- [ ] **No Noise**: Obvious code not commented
- [ ] **Format**: Consistent comment style and format
- [ ] **Language**: Comments in same language as codebase
- [ ] **Links**: Complex topics link to external documentation

---

## Anti-patterns

### ❌ Don't: Comment Obvious Code

```javascript
// ❌ Bad - Obvious
// Check if user is authenticated
if (user.isAuthenticated) {
    // Return true
    return true;
}
```

```javascript
// ✅ Good - No comment needed
if (user.isAuthenticated) {
    return true;
}
```

### ❌ Don't: Outdated Comments

```javascript
// ❌ Bad - Comment doesn't match code
// Always return user data
function getUserData(userId) {
    const user = database.find(userId);
    if (!user) {
        return null;  // Comment says always return, but we return null
    }
    return user;
}
```

```javascript
// ✅ Good - Comment matches code
// Return user data or null if not found
function getUserData(userId) {
    const user = database.find(userId);
    return user || null;
}
```

---

## Integration Points

- **Code Review** (`01-foundations/code-review/`) - Review comment quality
- **Technical Writing** (`21-documentation/technical-writing/`) - Clear documentation
- **API Documentation** (`21-documentation/api-documentation/`) - Code examples

---

## Further Reading

- [Clean Code: Comments](https://www.amazon.com/Clean-Code-Handbook/Software-Craftsmanship/dp/013235082)
- [Google Style Guides](https://google.github.io/styleguide/)
- [No rationale](https://stackoverflow.blog/2021/12/15/writing-comments)
- [Clean Code JavaScript Comments](https://github.com/ryanmcdermott/clean-code-javascript#comments)
- [Writing Comments](https://stackoverflow.blog/2021/12/15/writing-comments)
