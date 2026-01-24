### **01: Technical Decision Records (ADRs)**

> 
> **Current Level:** Expert (Enterprise Scale) 
> 
> 
> **Domain:** Meta Skills / Architecture 
> 

---

### **1. Executive Summary & Strategic Necessity**

* **Context:** ในโลกปี 2025-2026 ระบบซอฟต์แวร์มีความซับซ้อนเพิ่มขึ้นอย่างมาก การตัดสินใจทางเทคนิคที่สำคัญจำเป็นต้องมีการบันทึกและติดตามอย่างเป็นระบบ Architecture Decision Records (ADRs) เป็นกระบวนการที่ช่วยให้ทีมสามารถทำความเข้าใจเหตุผลของการตัดสินใจในอดีต และหลีกเลี่ยงการทำซ้ำการอภิปรายหรือการตัดสินใจที่ผิดพลาดเดิม
* **Business Impact:** การใช้ ADRs ช่วย:
  - ลดเวลาในการอภิปรายและการตัดสินใจซ้ำ
  - เพิ่มความโปร่งใสในการตัดสินใจ
  - ลดความเสี่ยงของการสูญเสียความรู้เมื่อทีมเปลี่ยน
  - เพิ่มประสิทธิภาพในการ Onboard ทีมใหม่
  - ลดต้นทุนในการ Refactoring และการแก้ไขปัญหาที่เกิดจากการตัดสินใจที่ผิด
* **Product Thinking:** ทักษะนี้ช่วยแก้ปัญหา (Pain Point) ให้กับ:
  - ทีมพัฒนาที่ต้องการความเข้าใจในการตัดสินใจในอดีต
  - ผู้บริหารที่ต้องการความมั่นใจในการตัดสินใจทางเทคนิค
  - ลูกค้าที่ต้องการความสอดคล้องในการพัฒนา
  - ทีม DevOps ที่ต้องการความเข้าใจในการ Deploy และ Monitor

### **2. Technical Deep Dive (The "How-to")**

* **Core Logic:** ADRs เป็นเอกสารที่บันทึกการตัดสินใจทางสถาปัตยกรรมที่สำคัญ โดยใช้กลไกต่อไปนี้:
  - **Decision Significance Threshold:** การตัดสินใจว่าเมื่อไรควรเขียน ADR (เช่น การเปลี่ยนฐานข้อมูล, การเลือก Framework ใหม่, การเปลี่ยน Architecture)
  - **ADR Structure:** โครงสร้างมาตรฐานของ ADR (Status, Context, Decision, Consequences, Alternatives Considered, References)
  - **Versioning and Linking:** การใช้เลขลำดับและการเชื่อมโยงระหว่าง ADRs
  - **Storage and Organization:** การจัดเก็บและการจัดระเบียบ ADRs

* **Architecture Diagram Requirements:** แผนผังสถาปัตยกรรมที่ต้องมี:
  - **Decision Flow Diagram:** แผนผังแสดงการไหลของการตัดสินใจ
  - **ADR Relationship Map:** แผนผังแสดงความสัมพันธ์ระหว่าง ADRs
  - **Timeline View:** มุมมองเวลาของการตัดสินใจ
  - **Impact Analysis Diagram:** แผนผังแสดงผลกระทบของการตัดสินใจ

* **Implementation Workflow:**
  1. **Identify Decision:** ระบุการตัดสินใจที่ต้องบันทึก
  2. **Create ADR:** สร้าง ADR ใหม่โดยใช้ Template
  3. **Review:** ทีมทบทวน ADR
  4. **Approve:** อนุมัติ ADR
  5. **Implement:** นำการตัดสินใจไปใช้
  6. **Track:** ติดตามผลลัพธ์
  7. **Update:** อัปเดตหรือ Deprecate ADR ตามความเหมาะสม

### **3. Tooling & Tech Stack**

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้:
  - **ADR Tools:** adr-tools, MADR (Markdown ADR), log4brains
  - **Documentation Platforms:** Confluence, Notion, GitHub Wiki, GitBook
  - **Diagram Tools:** Mermaid.js, PlantUML, Draw.io, Lucidchart
  - **Version Control:** Git, GitHub, GitLab, Bitbucket
  - **Review Tools:** GitHub PRs, GitLab MRs, Code Review Tools

* **Configuration Essentials:** ส่วนประกอบสำคัญในการตั้งค่า:
  - **ADR Template:** Template มาตรฐานสำหรับการสร้าง ADR
  - **Numbering Scheme:** รูปแบบการใช้เลขลำดับ (Sequential, Date-based, Hierarchical)
  - **Directory Structure:** โครงสร้างไดเรกทอรี่สำหรับจัดเก็บ ADRs
  - **Automation Scripts:** Script สำหรับสร้างและจัดการ ADRs
  - **Integration with CI/CD:** การผนวก ADRs เข้ากับ Pipeline

### **4. Standards, Compliance & Security**

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  - **ISO/IEC 27001:** Information Security Management
  - **ISO/IEC 9001:** Quality Management System
  - **IEEE 1471:** Recommended Practice for Architectural Description

* **Security Protocol:** กลไกการป้องกัน:
  - **Access Control:** การควบคุมการเข้าถึง ADRs
  - **Audit Trail:** การบันทึกการเข้าถึงและการแก้ไข
  - **Classification:** การจัดประเภท ADRs ตามความละเอียด
  - **Backup and Recovery:** การสำรองและการกู้คืนข้อมูล

* **Explainability:** ความสามารถในการอธิบาย:
  - **Rationale Documentation:** การบันทึกเหตุผลอย่างละเอียด
  - **Trade-off Analysis:** การวิเคราะห์ข้อดีและข้อเสีย
  - **Context Preservation:** การรักษาบริบทของการตัดสินใจ
  - **Stakeholder Perspectives:** การรวมมุมมองของผู้มีส่วนได้ส่วนเสีย

### **5. Unit Economics & Performance Metrics (KPIs)**

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย (COGS):
  ```
  Total Cost = (Time to Create ADR × Hourly Rate) + (Review Time × Hourly Rate) + (Maintenance Cost)
  
  ROI = (Time Saved - ADR Cost) / ADR Cost × 100%
  
  Time Saved = (Discussion Time Avoided) + (Re-decision Prevention) + (Onboarding Time Saved)
  ```

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  - **ADR Coverage:** % ของการตัดสินใจที่สำคัญที่มี ADR (Target: > 90%)
  - **ADR Quality Score:** คะแนนคุณภาพของ ADR (Target: > 4/5)
  - **Decision Reversal Rate:** % ของการตัดสินใจที่ถูกยกเลิก (Target: < 10%)
  - **ADR Reference Rate:** % ของ ADRs ที่ถูกอ้างอิง (Target: > 50%)
  - **Team Satisfaction:** ความพึงพอใจของทีม (Target: > 4/5)

### **6. Strategic Recommendations (CTO Insights)**

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน:
  1. **Phase 1 (Months 1-2):** สร้าง Template และ Guidelines, ฝึกอบรมทีม
  2. **Phase 2 (Months 3-4):** เริ่มเขียน ADRs สำหรับการตัดสินใจที่สำคัญ
  3. **Phase 3 (Months 5-6):** ผนวกเข้ากับ CI/CD, วัดผลและปรับปรุง
  4. **Phase 4 (Year 2+):** ขยายไปยังทุกทีม, สร้าง Culture ของการบันทึกการตัดสินใจ

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาด:
  - **Over-documentation:** หลีกเลี่ยงการเขียน ADR สำหรับการตัดสินใจที่ไม่สำคัญ
  - **Vague Rationale:** ต้องอธิบายเหตุผลอย่างชัดเจนและเฉพาะเจาะจง
  - **Missing Alternatives:** ต้องระบุทางเลือกอื่นที่พิจารณา
  - **Not Updating:** ต้องอัปเดต ADR เมื่อมีการเปลี่ยนแปลง
  - **No Review Process:** ต้องมีกระบวนการทบทวน ADR
  - **Poor Organization:** ต้องจัดระเบียบ ADRs อย่างเป็นระบบ

---

## What are ADRs and Why They Matter

**ADRs are:**
- Lightweight documents capturing important decisions
- Historical record of architectural choices
- Communication tool for current and future team members
- Learning resource for understanding system evolution

**Why they matter:**
- **Knowledge preservation** - Decisions outlive team members
- **Context sharing** - New team members understand "why"
- **Decision quality** - Writing forces thorough thinking
- **Accountability** - Clear ownership of decisions
- **Avoiding repetition** - Don't revisit settled decisions

## When to Write an ADR

### Decision Significance Threshold

Write an ADR when the decision:

✅ **Write ADR:**
- Affects system structure or architecture
- Has long-term consequences
- Is difficult or expensive to reverse
- Impacts multiple teams or components
- Involves significant trade-offs
- Sets a precedent for future decisions

❌ **Don't write ADR:**
- Trivial implementation details
- Easily reversible decisions
- Team conventions (use style guide instead)
- Temporary workarounds

### Examples

| Decision | ADR Needed? | Why |
|----------|-------------|-----|
| Choose PostgreSQL vs MongoDB | ✅ Yes | Hard to change, affects entire system |
| Use JWT for authentication | ✅ Yes | Security-critical, affects all services |
| Name a variable `userId` vs `user_id` | ❌ No | Trivial, use linter/style guide |
| Add logging to a function | ❌ No | Easily reversible |
| Adopt microservices architecture | ✅ Yes | Major architectural decision |

## ADR Structure and Format

### Standard Template

```markdown
# ADR-001: [Short Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
What is the issue we're facing? What factors are driving this decision?
Include relevant background, constraints, and requirements.

## Decision
What decision have we made? Be specific and concrete.

## Consequences
What are the positive and negative outcomes of this decision?

### Positive
- Benefit 1
- Benefit 2

### Negative
- Drawback 1
- Drawback 2

### Risks
- Risk 1
- Risk 2

## Alternatives Considered
What other options did we evaluate? Why were they rejected?

### Alternative 1: [Name]
- Pros: ...
- Cons: ...
- Why rejected: ...

### Alternative 2: [Name]
- Pros: ...
- Cons: ...
- Why rejected: ...

## References
- Link to related documents
- Link to discussions
- Link to prototypes

## Notes
- Date: YYYY-MM-DD
- Author: Name
- Reviewers: Names
```

## ADR Examples

### Example 1: Database Selection

```markdown
# ADR-001: Use PostgreSQL for Primary Database

## Status
Accepted (2024-01-15)

## Context
We need to select a database for our e-commerce platform. Requirements:
- ACID transactions for order processing
- Complex queries for reporting
- Scalability to 100K+ users
- Strong consistency for inventory management
- Team has SQL experience
- Budget constraints (prefer open-source)

## Decision
We will use PostgreSQL as our primary database.

## Consequences

### Positive
- ACID compliance ensures data integrity for financial transactions
- Rich query capabilities support complex reporting needs
- Mature ecosystem with extensive tooling and extensions
- Strong community support and documentation
- Team already familiar with SQL
- Free and open-source (no licensing costs)
- Excellent performance for our expected scale

### Negative
- Vertical scaling limitations (though sufficient for our needs)
- More complex to set up high availability compared to managed services
- Requires careful schema design upfront

### Risks
- May need to add read replicas as traffic grows
- Schema migrations need careful planning
- Potential performance issues if queries aren't optimized

## Alternatives Considered

### Alternative 1: MongoDB
- Pros: Flexible schema, horizontal scaling, JSON-native
- Cons: Weaker consistency guarantees, team unfamiliar with NoSQL, overkill for our structured data
- Why rejected: Our data is highly structured and relational; ACID guarantees are critical

### Alternative 2: Amazon DynamoDB
- Pros: Fully managed, excellent scalability, predictable performance
- Cons: Expensive at scale, vendor lock-in, limited query capabilities, learning curve
- Why rejected: Cost concerns and query limitations outweigh scalability benefits

### Alternative 3: MySQL
- Pros: Similar to PostgreSQL, widely used, good performance
- Cons: Less feature-rich than PostgreSQL, weaker JSON support
- Why rejected: PostgreSQL offers better features for same complexity

## References
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Database comparison spreadsheet](link-to-internal-doc)
- [Team discussion thread](link-to-slack/email)

## Notes
- Date: 2024-01-15
- Author: Jane Smith
- Reviewers: John Doe, Alice Johnson
- Next review: 2025-01-15 (or when scaling beyond 100K users)
```

### Example 2: Authentication Strategy

```markdown
# ADR-002: Use JWT with Refresh Tokens for Authentication

## Status
Accepted (2024-01-20)

## Context
We need an authentication mechanism for our API that:
- Works with our React frontend and mobile apps
- Supports stateless API servers for horizontal scaling
- Provides reasonable security
- Allows token revocation when needed
- Balances security with user experience

Current situation:
- Multiple client types (web, iOS, Android)
- Microservices architecture
- Need to scale horizontally
- Security is important but not ultra-high-security (not banking/healthcare)

## Decision
We will implement JWT-based authentication with refresh tokens:
- Short-lived access tokens (15 minutes)
- Long-lived refresh tokens (7 days)
- Refresh tokens stored in database for revocation
- Access tokens are stateless (not stored)

## Consequences

### Positive
- Stateless access tokens enable horizontal scaling
- Works seamlessly across web and mobile
- Industry-standard approach with good library support
- Can revoke access via refresh token invalidation
- Reduced database load (only hit DB on refresh)
- Clear separation between authentication and authorization

### Negative
- Cannot immediately revoke access tokens (must wait for expiry)
- Need to manage refresh token storage and rotation
- Slightly more complex than session-based auth
- Tokens can be stolen if not handled carefully
- Need to implement token refresh logic in clients

### Risks
- XSS attacks could steal tokens (mitigated by httpOnly cookies for web)
- Token replay attacks (mitigated by short expiry)
- Refresh token theft (mitigated by rotation and secure storage)

## Alternatives Considered

### Alternative 1: Session-based Authentication
- Pros: Easy to implement, immediate revocation, familiar pattern
- Cons: Requires sticky sessions or shared session store, doesn't scale horizontally well, complex with multiple clients
- Why rejected: Doesn't fit our microservices architecture and scaling needs

### Alternative 2: OAuth 2.0 with External Provider (Auth0, Cognito)
- Pros: Fully managed, battle-tested, includes MFA and social login
- Cons: Vendor lock-in, ongoing costs, less control, overkill for our needs
- Why rejected: Want to maintain control and avoid ongoing costs at this stage

### Alternative 3: API Keys
- Pros: Simple, stateless
- Cons: No user context, difficult to rotate, no expiration, security concerns
- Why rejected: Doesn't support user-specific permissions and lacks security features

### Alternative 4: JWT without Refresh Tokens
- Pros: Simpler implementation
- Cons: Either long-lived tokens (security risk) or frequent re-authentication (bad UX)
- Why rejected: Refresh tokens provide better security/UX balance

## Implementation Notes
- Use RS256 (asymmetric) for signing to allow verification without shared secret
- Store refresh tokens hashed in database
- Implement token rotation on refresh
- Set appropriate CORS and security headers
- Use httpOnly cookies for web clients
- Implement rate limiting on auth endpoints

## References
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Auth0 Blog on Refresh Tokens](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)

## Notes
- Date: 2024-01-20
- Author: John Doe
- Reviewers: Jane Smith, Security Team
- Implementation target: Sprint 5
- Review trigger: Security audit or scaling beyond 50K users
```

## ADR Storage and Versioning

### Storage Options

1. **In Repository** (Recommended)
   ```
   docs/adr/
   ├── 0001-use-postgresql.md
   ├── 0002-jwt-authentication.md
   ├── 0003-graphql-api.md
   └── README.md
   ```

2. **Wiki/Confluence**
   - Good for discoverability
   - May get out of sync with code

3. **Dedicated Tool**
   - log4brains
   - ADR Manager

### Versioning

- Use sequential numbering: `0001`, `0002`, etc.
- Never delete ADRs (mark as deprecated/superseded)
- Link related ADRs
- Keep in version control with code

## Linking ADRs

### Superseding

```markdown
# ADR-015: Use REST API Instead of GraphQL

## Status
Accepted (2024-06-01)
Supersedes: ADR-003

## Context
After 4 months with GraphQL (ADR-003), we've encountered issues:
- Query complexity causing performance problems
- Team struggling with GraphQL concepts
- Third-party developers requesting REST
- Caching complexity outweighs benefits

## Decision
Revert to REST API with careful endpoint design...
```

### Deprecating

```markdown
# ADR-003: Use GraphQL for Public API

## Status
Deprecated (2024-06-01)
Superseded by: ADR-015

## Deprecation Reason
GraphQL complexity outweighed benefits for our use case.
See ADR-015 for new approach.

[Original content remains below for historical reference]
```

## ADR Review Process

1. **Draft** - Author creates ADR
2. **Review** - Team reviews and comments
3. **Discussion** - Address feedback
4. **Decision** - Accept, reject, or request changes
5. **Implementation** - Execute decision
6. **Retrospective** - Review outcomes after 3-6 months

## Tools

### adr-tools

```bash
# Install
npm install -g adr-tools

# Initialize
adr init docs/adr

# Create new ADR
adr new "Use PostgreSQL for primary database"

# List ADRs
adr list

# Generate graph
adr generate graph
```

### MADR (Markdown ADR)

```bash
# Install
npm install -g madr

# Create ADR
madr new "Database selection"
```

### log4brains

```bash
# Install
npm install -g log4brains

# Initialize
log4brains init

# Preview
log4brains preview

# Build static site
log4brains build
```

## Writing Style

### Do ✅

- Be concise and specific
- Use active voice
- Include dates and authors
- List alternatives considered
- Explain trade-offs
- Use diagrams when helpful
- Link to references

### Don't ❌

- Write novels (keep it under 2 pages)
- Use jargon without explanation
- Skip the "why"
- Ignore alternatives
- Make it a specification (ADR ≠ spec)
- Update old ADRs (create new ones instead)

## Common Pitfalls

1. **Too Verbose** - Keep it concise
2. **Missing Context** - Always explain why
3. **No Alternatives** - Show you considered options
4. **No Consequences** - List both pros and cons
5. **Too Late** - Write during decision, not after
6. **Too Early** - Wait until decision is clear
7. **Wrong Scope** - Not every decision needs an ADR

## Integration with Documentation

```
docs/
├── adr/              # Architecture decisions
├── api/              # API documentation
├── guides/           # How-to guides
├── architecture/     # Architecture diagrams
└── runbooks/         # Operational procedures
```

**Cross-reference:**
- Link ADRs from architecture docs
- Reference ADRs in code comments
- Include ADR links in PR descriptions

## Team Adoption Strategies

1. **Start Small** - Begin with major decisions only
2. **Lead by Example** - Architects write first ADRs
3. **Make it Easy** - Provide templates and tools
4. **Review Together** - Discuss ADRs in team meetings
5. **Celebrate** - Recognize good ADRs
6. **Iterate** - Improve process based on feedback

## Best Practices

1. **Write During Decision** - Not after implementation
2. **Keep it Short** - 1-2 pages maximum
3. **Be Honest** - Include negatives and risks
4. **Show Alternatives** - Prove you considered options
5. **Use Templates** - Consistency helps readability
6. **Version Control** - Keep with code
7. **Review Regularly** - Revisit decisions periodically
8. **Link Related ADRs** - Show decision evolution
9. **Include Dates** - Context changes over time
10. **Make it Searchable** - Use clear titles and tags

## Resources

- [ADR GitHub Organization](https://adr.github.io/)
- [Documenting Architecture Decisions by Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR Tools](https://github.com/npryce/adr-tools)
- [MADR](https://adr.github.io/madr/)
- [log4brains](https://github.com/thomvaill/log4brains)
