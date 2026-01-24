### **02: Code Review Best Practices**

> 
> **Current Level:** Expert (Enterprise Scale) 
> 
> 
> **Domain:** Foundations / Code Quality 
> 

---

### **1. Executive Summary & Strategic Necessity**

* **Context:** ในโลกปี 2025-2026 การพัฒนาซอฟต์แวร์มีความซับซ้อนเพิ่มขึ้นอย่างมาก การทบทวนโค้ด (Code Review) เป็นกระบวนการสำคัญที่ช่วยให้ทีมสามารถตรวจสอบความโค้ด และปรับปรุงกระบวนการแก้ไข ความที่ไม่ดีและการสร้าง Technical Debt ใหม่
* **Business Impact:** การทบทวนโค้ดที่มีประสิทธิภาพช่วย:
  - ลดความ Bug ที่เกิดขึ้นใน Production
  - เพิ่มความโค้ดที่สะอดความของทีมพัฒนา
  - เพิ่มความเสถียรของระบบ
  - ลด Technical Debt ที่สะสมในระยะว
  - เพิ่มความความพึงพอใจของทีมพัฒนา
  - ลดต้นทุนในการบำรุงและการแก้ไข
  - เพิ่มประสิทธิภาพในการวางแผน Roadmap
* **Product Thinking:** ทักษะนี้ช่วยแก้ปัญหา (Pain Point) ให้กับ:
  - ทีมพัฒนาที่ต้องการ Code Review ที่เป็นระบบอัตโนมัก
  - ผู้ทำงานผิดพลาดที่ต้องการ Review ที่เข้าใจ
  - ทีมพัฒนาที่ต้องการ Feedback ที่มีประสิทธิภาพ
  - ลูกค้าที่ต้องการความโค้ดที่สะอดความและเป็นมาตรฐาน
  - ทีม Support ที่ต้องการ Review และ Debug ของ Code

### **2. Technical Deep Dive (The "How-to")**

* **Core Logic:** Code Review เป็นกระบวนการที่ช่วยให้:
  - **Review Principles:** การทบทวนโค้ดตามหลักการ Review (Review Code, Not Author, Be Timely, Be Thorough but Practical, Share Knowledge, Keep Reviews Small)
  - **Review Process:** กระบวนการทบทวน (Before Submitting, During Review, After Review, Review Process Workflow)
  - **Review Checklists:** รายการตรวจสอบความโค้ด (Code Quality, Security, Performance, Testing, Documentation, API Design)
  - **Feedback Guidelines:** การให้ Feedback ที่มีประสิทธิภาพ (Be Constructive, Be Specific, Use Questions Over Statements, Explain Why, Acknowledge Good Work, Categorize Comments, Respond to All Comments)
  - **Review Categories:** ประเภทของ Code Review (General Code Quality, Security Vulnerabilities, Performance Issues, Testing Coverage, Documentation, API Design)

* **Architecture Diagram Requirements:** แผนผังสถาปัตยกรรมที่ต้องมี:
  - **Review Process Flow Diagram:** แผนผังแสดงกระบวนการทบทวน
  - **Review Workflow Diagram:** แผนผังแสดงการไหลของ Pull Request
  - **Feedback Flow Diagram:** แผนผังแสดงการให้ Feedback และการแก้ไข
  - **Integration with CI/CD Diagram:** แผนผังแสดงการผนวกกับ CI/CD Pipeline

* **Implementation Workflow:**
  1. **Define Review Standards:** กำหนด Review Standards สำหรับโปรเจกต์
  2. **Setup Review Checklists:** สร้าง Review Checklists สำหรับแต่ละประเภท
  3. **Configure CI/CD Integration:** ตั้งค่า CI/CD เพื่อทบทวนโค้ดอัตโนมัก
  4. **Train Team on Review Process:** ฝึกอบรมทีมเกี่ยวกับ Review Process
  5. **Implement Review Workflow:** ดำเนินการ Review ตาม Workflow
  6. **Monitor Review Metrics:** ติดตามและวัดผล Review Metrics
  7. **Continuous Improvement:** ปรับปรุง Review Process อย่างต่อเนื่อง

### **3. Tooling & Tech Stack**

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้:
  - **Code Review Platforms:** GitHub PRs, GitLab MRs, Bitbucket PRs, Azure DevOps
  - **Code Analysis Tools:** SonarQube, CodeQL, Coverity, Fortify
  - **Documentation Platforms:** Confluence, Notion, GitHub Wiki
  - **CI/CD Integration:** GitHub Actions, GitLab CI, Azure Pipelines, Jenkins
  - **Communication Tools:** Slack, Microsoft Teams, Discord
  - **Project Management:** Jira, Azure DevOps, Linear, Shortcut

* **Configuration Essentials:** ส่วนประกอบสำคัญในการตั้งค่า:
  - **Review Thresholds:** การตั้งค่าเกณวันสำหรับ PR Size (Lines of Code, Files Changed)
  - **Approval Rules:** กฎการอนุมัติ PR (Minimum Reviewers, Approval Process)
  - **CI/CD Gates:** การตั้งค่า CI/CD Gates (Lint, Type Check, Test Coverage, Security Scan)
  - **Notification Settings:** การตั้งค่าการแจ้งเตือนอัตโนมัก
  - **Integration with Issue Tracker:** การผนวกกับ Issue Tracker เพื่อ Track Review Comments

### **4. Standards, Compliance & Security**

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  - **ISO/IEC 25010:** Software Quality Model
  - **IEEE 730:** Standard for Software Quality Assurance
  - **OWASP Top 10:** Web Application Security Risks
  - **CWE/SANS Top 25:** Most Dangerous Software Errors

* **Security Protocol:** กลไกการป้องกัน:
  - **Access Control:** การควบคุมการเข้าถึง Pull Request และการแก้ไข
  - **Audit Trail:** การบันทึกการเข้าถึงและการแก้ไข
  - **Secret Scanning:** การสแกน Secrets ใน Code ก่อนเกิด
  - **Dependency Scanning:** การสแกน Dependencies ที่มีช่อง Security Vulnerabilities
  - **Code Signing:** การลงนาม Code สำหรับความเปลอดใจ

* **Explainability:** ความสามารถในการอธิบาย:
  - **Review Rationale Documentation:** การบันทึกเหตุผลของการ Review
  - **Comment Templates:** Template สำหรับการให้ Comment ที่มีประสิทธิภาพ
  - **Decision Records:** การบันทึก ADRs สำหรับการตัดสินใจที่สำคัญใน Review

### **5. Unit Economics & Performance Metrics (KPIs)**

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย (COGS):
  ```
  Total Cost = (Review Time × Hourly Rate) + (Fix Time × Hourly Rate) + (Tooling Cost)
  
  ROI = (Bug Prevention Value - Total Cost) / Total Cost × 100%
  
  Bug Prevention Value = (Bug Cost in Production × Probability of Detection) + (Reputation Impact)
  ```

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  - **Review Coverage:** % ของ Pull Requests ที่ถูทบทวน (Target: > 90%)
  - **Review Turnaround Time:** เวลาเฉลี่ยในการทบทวน (Target: < 24 hours)
  - **Bug Detection Rate:** % ของ Bugs ที่ค้นพบก่อน Production (Target: > 80%)
  - **Code Quality Score:** คะแนนคุณภาพของโค้ด (Target: > B)
  - **Team Satisfaction:** ความพึงพอใจของทีม (Target: > 4/5)
  - **Review Participation Rate:** % ของทีมที่มีส่วนการ Review (Target: > 80%)

### **6. Strategic Recommendations (CTO Insights)**

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน:
  1. **Phase 1 (Months 1-2):** สร้าง Review Standards และ Guidelines, ฝึกอบรมทีม
  2. **Phase 2 (Months 3-4):** ตั้งค่า CI/CD Integration และ Gates
  3. **Phase 3 (Months 5-6):** ฝึกอบรมทีมเกี่ยวกับ Review Process
  4. **Phase 4 (Year 2+):** ขยายไปยังทุกทีม, สร้าง Culture ของ Code Review

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาด:
  - **Over-reviewing:** หลีกเลี่ยงการ Review ที่เกินไป
  - **Personal Comments:** หลีกเลี่ยงการให้ Comment ส่วนตัวบุคน
  - **Nitpicking:** หลีกเลี่ยงการวิจารณ์รายเล็กเล็ก
  - **Not Following Standards:** ต้องทบทวนตามหลักการ Review Standards
  - **Skipping Reviews:** หลีกเลี่ยงการข้าม Review สำหรับ PR ที่สำคัญ
  - **Not Providing Context:** ต้องให้ความและเหตุผลใน Comment
  - **Not Responding to Comments:** ต้องตอบสนทุก Comment
  - **Blocking PRs:** หลีกเลี่ยงการ Block PR โดยไม่ให้เหตุผล

---

## Overview

Code review is a systematic examination of source code intended to find bugs, improve code quality, and share knowledge across the team. Effective code reviews catch defects early, enforce coding standards, and foster collaborative learning.

## Code Review Principles

### 1. Review Code, Not Author

- Focus on code's behavior and quality, not personal preferences
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
- Explain "why" behind suggestions
- Learn from code you're reviewing
- Share insights with the wider team

### 5. Keep Reviews Small

- Ideal PR size: 200-400 lines of code
- Large PRs should be split into logical chunks
- Smaller PRs get better reviews and faster feedback

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
- Appropriate abstraction level
- DRY (Don't Repeat Yourself)

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

**Check for:**
- Database query efficiency (N+1, missing indexes)
- Unnecessary computations or re-renders
- Memory leaks
- Appropriate caching
- Algorithmic complexity (O(n²) vs O(n log n))
- Resource cleanup (connections, file handles)

### Testing Coverage

```typescript
// BAD: No tests for new functionality
function calculateTotalTax(transactions: number[]): number {
  return transactions.reduce((totalTax, amount) => {
    const taxRate = amount > HIGH_VALUE_THRESHOLD
      ? HIGH_VALUE_TAX_RATE
      : STANDARD_TAX_RATE;
    return totalTax + (amount * taxRate);
  }, 0);
}

// GOOD: With tests
describe('calculateTotalTax', () => {
  it('calculates total tax correctly', () => {
    const transactions = [
      { amount: 150, type: 'high' },
      { amount: 50, type: 'standard' }
    ];
    expect(calculateTotalTax(transactions)).toBe(15.5);
  });
  
  it('handles empty array', () => {
    expect(calculateTotalTax([])).toBe(0);
  });
});
```

**Check for:**
- Unit tests for new functionality
- Edge cases and error conditions tested
- Integration tests for API endpoints
- Mocked dependencies where appropriate
- Test readability and maintainability
- No tests that always pass or are flaky

### Documentation

```typescript
// BAD: No documentation
function calculateTotalTax(transactions: number[]): number {
  return transactions.reduce((totalTax, amount) => {
    const taxRate = amount > HIGH_VALUE_THRESHOLD
      ? HIGH_VALUE_TAX_RATE
      : STANDARD_TAX_RATE;
    return totalTax + (amount * taxRate);
  }, 0);
}

// GOOD: With documentation
/**
 * Calculates total tax for a list of transactions
 * @param transactions - Array of transaction objects
 * @returns The total tax amount
 * @example calculateTotalTax([{ amount: 150, type: 'high' }]) // returns 15.5
 */
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
- Updated README if needed
- API documentation for new endpoints
- JSDoc/docstrings for public functions
- Architecture decision records for significant changes
- Updated CHANGELOG if applicable
- Onboarding guides for new team members

## Review Process Workflow

### Step 1: Before Submitting a PR

**Author responsibilities:**
```markdown
## PR Preparation Checklist

### Code Quality
- [ ] Code is readable and self-documenting
- [ ] Variable and function names are descriptive
- [ ] No dead code or commented-out code
- [ ] No duplicated code (DRY principle)
- [ ] Functions are small and focused
- [ ] Error handling is appropriate
- [ ] No hardcoded values (use constants/config)
- [ ] Code follows project style guide
- [ ] No unnecessary complexity
- [ ] Imports are organized and minimal

### Testing
- [ ] Unit tests for new functionality
- [ ] Edge cases and error conditions tested
- [ ] Integration tests for API endpoints
- [ ] Tests are readable and maintainable
- [ ] No tests that always pass or are flaky
- [ ] Mocked dependencies where appropriate

### Documentation
- [ ] Updated README if needed
- [ ] API documentation for new endpoints
- [ ] JSDoc/docstrings for public functions
- [ ] Architecture decision records for significant changes
- [ ] Updated CHANGELOG if applicable

### Security
- [ ] Input is validated and sanitized
- [ ] No SQL/NoSQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Authentication/authorization checks in place
- [ ] Sensitive data is not logged
- [ ] Secrets are not hardcoded
- [ ] Dependencies don't have known vulnerabilities

### Performance
- [ ] No N+1 query problems
- [ ] Database queries are optimized
- [ ] Appropriate indexes exist
- [ ] Caching is used where beneficial
- [ ] No memory leaks
- [ ] Large datasets are paginated
- [ ] Async operations are properly handled

### Commit Message
- [ ] Follows commit message conventions
- [ ] Clearly describes what and why
- [ ] References related issues
- [ ] Includes breaking change notice if applicable
```

**Reviewer preparation:**
```markdown
## Review Preparation Checklist

- [ ] Read PR description and linked issues
- [ ] Review code changes locally first
- [ ] Check related files for context
- [ ] Prepare questions and feedback
- [ ] Set aside adequate time for thorough review
```

### Step 2: During Review

**Review structure:**
```markdown
## Review Summary

**Status:** ✅ Approved / 🟡 Needs Changes / ❌ Rejected

**Overall Assessment:**
[Brief summary of the review]

## Code Quality

### Strengths
- [ ] Clear and readable code
- [ ] Good naming conventions
- [ ] Appropriate error handling
- [ ] Well-structured code

### Concerns
- [ ] [Specific concern 1]
- [ ] [Specific concern 2]

## Security

### Findings
- [ ] [Security finding 1]
- [ ] [Security finding 2]

## Performance

### Findings
- [ ] [Performance concern 1]
- [ ] [Performance concern 2]

## Testing

### Findings
- [ ] [Test coverage concern]
- [ ] [Test quality concern]

## Documentation

### Findings
- [ ] [Documentation concern]
```

**Comment organization:**
```markdown
## Comments by Category

### Code Quality
- [ ] [Code quality comments]
- [ ] [Refactoring suggestions]
- [ ] [Style improvements]

### Security
- [ ] [Security-related comments]
- [ ] [Vulnerability findings]

### Performance
- [ ] [Performance-related comments]
- [ ] [Optimization suggestions]

### Testing
- [ ] [Test-related comments]
- [ ] [Coverage gaps]

### Documentation
- [ ] [Documentation suggestions]
```

### Step 3: After Review

**Author actions:**
```markdown
## Post-Review Actions

### Address Feedback
- [ ] Respond to all review comments
- [ ] Make requested changes
- [ ] Ask clarifying questions if needed
- [ ] Update documentation if requested
- [ ] Fix critical issues immediately

### Update PR
- [ ] Push changes to branch
- [ ] Mark conversations as resolved
- [ ] Request re-review if changes are significant

### Learn from Feedback
- [ ] Note patterns in feedback received
- [ ] Update personal coding standards
- [ ] Share learnings with team
```

**Reviewer follow-up:**
```markdown
## Follow-up Actions

### Track Implementation
- [ ] Verify changes were implemented correctly
- [ ] Check if related code was affected
- [ ] Run tests to ensure nothing broke
- [ ] Monitor for regressions

### Close Review
- [ ] Mark PR as merged when appropriate
- [ ] Update any related documentation
- [ ] Celebrate successful completion
```

## Review Checklists

### General Code Quality Checklist

```markdown
## Code Quality Checklist

### Readability
- [ ] Code is readable and self-documenting
- [ ] Variable and function names are descriptive
- [ ] No magic numbers or unclear values
- [ ] Consistent formatting and style
- [ ] Appropriate comments (explain "why", not "what")
- [ ] Functions are small and focused (single responsibility)
- [ ] Appropriate abstraction level
- [ ] No dead code or commented-out code
- [ ] No duplicated code (DRY principle)
- [ ] No unnecessary complexity

### Maintainability
- [ ] Code follows project style guide
- [ ] Imports are organized and minimal
- [ ] Dependencies are appropriate and minimal
- [ ] Configuration is externalized
- [ ] No hardcoded values
- [ ] Error handling is consistent
- [ ] Logging is appropriate and not excessive

### Extensibility
- [ ] Code is modular and loosely coupled
- [ ] Interfaces are well-defined
- [ ] Plugin points are clear
- [ ] Design patterns are used appropriately
- [ ] No tight coupling between components

### Testability
- [ ] Code is structured to support testing
- [ ] Dependencies are injectable
- [ ] Side effects are minimal
- [ ] State is managed properly
- [ ] Async operations are handled correctly
```

### Security Checklist

```markdown
## Security Checklist

### Input Validation
- [ ] All inputs are validated
- [ ] User input is sanitized
- [ ] File uploads are validated
- [ ] Query parameters are validated
- [ ] Request size limits are enforced

### Authentication & Authorization
- [ ] Authentication is properly implemented
- [ ] Authorization checks are in place
- [ ] Session management is secure
- [ ] Token-based auth is properly secured
- [ ] API keys are validated and rotated

### Data Protection
- [ ] Sensitive data is not logged
- [ ] Secrets are not hardcoded
- [ ] PII is encrypted at rest
- [ ] Secrets are stored securely
- [ ] Database connections use TLS
- [ ] File permissions are correct

### Output Encoding
- [ ] HTML is properly encoded
- [ ] JSON is properly encoded
- [ ] XSS prevention is in place
- [ ] Content-Type headers are set correctly
- [ ] CSP headers are implemented

### Dependency Security
- [ ] Dependencies are scanned for vulnerabilities
- [ ] Dependencies are up-to-date
- [ ] No dependencies with known CVEs
- [ ] Package locks are used
- [ ] Supply chain attacks are prevented

### Error Handling
- [ ] Errors don't expose sensitive information
- [ ] Stack traces are not shown in production
- [ ] Error messages are user-friendly
- [ ] Errors are logged for debugging
- [ ] Appropriate HTTP status codes are used
- [ ] Error responses follow standard format
```

### Performance Checklist

```markdown
## Performance Checklist

### Database
- [ ] No N+1 query problems
- [ ] Queries use indexes appropriately
- [ ] Large datasets are paginated
- [ ] Connection pooling is used
- [ ] Query results are cached when appropriate
- [ ] Transactions are properly managed
- [ ] Database schema is optimized

### API Performance
- [ ] Response times are monitored
- [ ] Rate limiting is implemented
- [ ] Compression is enabled
- [ ] CDN is used for static assets
- [ ] Caching headers are set correctly
- [ ] GraphQL queries are optimized

### Code Performance
- [ ] No unnecessary computations
- [ ] Loops are optimized
- [ ] Memory usage is monitored
- [ ] No memory leaks
- [ ] Algorithms have appropriate complexity
- [ ] Async operations are handled efficiently

### Frontend Performance
- [ ] Bundle size is optimized
- [ ] Code splitting is used
- [ ] Lazy loading is implemented
- [ ] Images are optimized
- [ ] CSS animations are performant
- [ ] Virtual scrolling is efficient
```

### Testing Checklist

```markdown
## Testing Checklist

### Unit Tests
- [ ] Unit tests for new functionality
- [ ] Edge cases are tested
- [ ] Error conditions are covered
- [ ] Tests are fast and reliable
- [ ] Tests are readable and maintainable
- [ ] Mocks are used appropriately
- [ ] Test coverage meets targets (>80%)

### Integration Tests
- [ ] API endpoints are tested
- [ ] Database interactions are tested
- [ ] External service integrations are tested
- [ ] Error scenarios are covered
- [ ] Authentication flows are tested
- [ ] Rate limiting is tested

### End-to-End Tests
- [ ] Critical user journeys are tested
- [ ] Cross-browser compatibility is verified
- [ ] Mobile responsiveness is tested
- [ ] Performance tests are run
- [ ] Accessibility tests are conducted

### Test Quality
- [ ] Tests are not flaky
- [ ] Tests are independent
- [ ] Tests are deterministic
- [ ] Test data is cleaned up after runs
- [ ] Tests use appropriate assertions
- [ ] Test names describe expected behavior
```

### Documentation Checklist

```markdown
## Documentation Checklist

### Code Documentation
- [ ] README is up-to-date
- [ ] API documentation exists
- [ ] Architecture diagrams are current
- [ ] Database schema is documented
- [ ] Environment variables are documented
- [ ] Deployment instructions are clear

### API Documentation
- [ ] OpenAPI/Swagger specification exists
- [ ] Authentication documentation is provided
- [ ] Rate limiting is documented
- [ ] Error codes are documented
- [ ] Webhook documentation is provided (if applicable)
- [ ] SDK/client library examples are provided

### Developer Documentation
- [ ] Onboarding guide exists
- [ ] Development setup instructions are clear
- [ ] Contribution guidelines are linked
- [ ] Code style guide is referenced
- [ ] Architecture decision records are accessible

### Release Documentation
- [ ] CHANGELOG is maintained
- [ ] Migration guides are provided
- [ ] Breaking changes are documented
- [ ] Rollback procedures are documented
```

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

### Explain Why

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
"Nice use of the builder pattern here! It makes configuration
much more readable than a large constructor."
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

**[Praise]** Great test coverage on edge cases!
```

### Comment Templates

#### For Bugs

```markdown
## Bug Report

**Issue:** [Description of the problem]
**Impact:** [What could go wrong]
**Suggestion:** [How to fix it]
**Benefit:** [Why this is better]
```

#### For Improvements

```markdown
## Improvement Suggestion

**Current:** [What the code does now]
**Proposed:** [What it could do better]
**Benefit:** [Why this is better]
```

## How to Receive Feedback

### Stay Open-Minded

- Remember: reviewers want to help improve the code
- Don't take feedback personally
- Consider each comment thoughtfully before responding
- Ask clarifying questions if feedback is unclear

### Respond to All Comments

- Acknowledge every comment, even if just with a thumbs up
- If you disagree, provide technical reasoning
- Reference documentation or best practices
- Offer alternatives if rejecting a suggestion
- Ask clarifying questions if feedback is unclear

### Learn from Feedback

- Look for patterns in feedback you receive
- Thank reviewers for catching issues
- Use reviews as learning opportunities
- Update personal coding standards based on feedback
- Share insights with the wider team

### Know When to Push Back

- If you disagree, provide technical reasoning
- Reference documentation or best practices
- Offer alternatives if rejecting a suggestion
- Ask clarifying questions if feedback is unclear

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
async function getUserOrderPayments(userId: string) {
  const user = await getUser(userId);
  const orders = await getOrders(user.id);
  const payments = await getPayments(orders[0].id);
  // ... more nesting
}

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

## Automated Checks vs Manual Review

### What to Automate

| Check Type | Why Automate | Tools |
|------------|--------------|--------|
| Code formatting | Prettier, Black | Eliminates style debates |
| Linting | ESLint, Pylint | Catches common issues instantly |
| Type checking | TypeScript, mypy | Finds type errors before review |
| Security scanning | Snyk, npm audit | Finds known vulnerabilities |
| Test execution | Jest, pytest | Ensures tests pass |
| Dependency updates | Dependabot, Renovate | Keeps dependencies current |
| Commit message | commitlint | Enforces consistent messages |

### What Requires Human Review

| Aspect | Why Human Review |
|---------|------------------|
| Architecture decisions | Requires domain knowledge and judgment |
| Business logic correctness | Automated tools can't verify requirements |
| Code readability | Subjective assessment of clarity |
| Appropriate abstraction | Judgment call on when to abstract |
| Security context | Understanding of threat model |
| Performance trade-offs | Requires understanding of use cases |
| API design consistency | Review of overall API contract |
| Test coverage quality | Understanding of edge cases |

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
      
      - name: Type check
        run: npm run type-check
      
      - name: Lint
        run: npm run lint
      
      - name: Format check
        run: npm run format:check
      
      - name: Test coverage
        run: npm test -- --coverage
          if [ $(cat coverage/coverage-summary.json | jq '.total.lines.pct') -lt 80 ]; then
            echo "Coverage below 80%"
            exit 1
          fi
      
      - name: Security audit
        run: npm audit --audit-level=high

  manual-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Manual review
        run: echo "Manual review required for this PR"
```

## Best Practices

1. **Review Code, Not People** - Focus on code's behavior and quality
2. **Be Timely** - Review PRs within 24 hours when possible
3. **Be Thorough but Practical** - Balance thoroughness with velocity
4. **Share Knowledge** - Use reviews as teaching opportunities
5. **Keep Reviews Small** - Ideal PR size: 200-400 lines
6. **Follow Standards** - Use established coding conventions
7. **Provide Context** - Include PR description and linked issues
8. **Be Constructive** - Give specific, actionable feedback
9. **Learn from Feedback** - Look for patterns in feedback you receive
10. **Respond to All Comments** - Acknowledge every comment

## Common Pitfalls

1. **Over-reviewing** - Don't review more than necessary
2. **Personal Comments** - Keep feedback professional and focused on code
3. **Nitpicking** - Focus on issues that matter, not style preferences
4. **Not Following Standards** - Adhere to established conventions
5. **Skipping Reviews** - Don't skip reviews for small PRs
6. **Blocking PRs** - Don't block PRs without clear justification
7. **Not Providing Context** - Include rationale in comments
8. **Not Responding to Comments** - Address all review feedback
9. **Short-term Focus** - Consider long-term consequences
10. **Ignoring Security** - Always prioritize security findings

## Resources

- [Google Engineering Practices](https://google.github.io/eng-practices/review/) - Google's code review guidelines
- [Uber Engineering Practices](https://eng.uber.com/review-guide/) - Uber's code review guide
- [Facebook Code Review Guide](https://github.com/facebook/fbcode/) - Facebook's code review guide
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) - JavaScript style guide
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350872) - Clean code principles
- [Refactoring by Martin Fowler](https://www.amazon.com/Refactoring-Improving-Existing-Code/dp/0201485672) - Refactoring techniques
