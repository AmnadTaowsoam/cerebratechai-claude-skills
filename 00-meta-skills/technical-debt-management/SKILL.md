### **05: Technical Debt Management**

> 
> **Current Level:** Expert (Enterprise Scale) 
> 
> 
> **Domain:** Meta Skills / Code Quality 
> 

---

### **1. Executive Summary & Strategic Necessity**

* **Context:** ในโลกปี 2025-2026 ระบบซอฟต์แวร์มีความซับซ้อนเพิ่มขึ้นอย่างมาก การจัดการ Technical Debt เป็นกระบวนการสำคัญที่ช่วยให้ทีมสามารถสร้างสมดุลในการพัฒนาซอฟต์แวร์และลดความเสี่ยงที่อาจเกิดจากการเก็บสะสมหนี้ไป Technical Debt ที่ไม่ได้รับการจัดการ
* **Business Impact:** การจัดการ Technical Debt ที่มีประสิทธิภาพช่วย:
  - เพิ่มความเร็วในการพัฒนา Feature ใหม่
  - ลดความเสี่ยงที่อาจเกิดจาก Technical Debt
  - เพิ่มความสามารถในการวางแผน Roadmap
  - ลดต้นทุนในการบำรุงรักษาและการแก้ไข
  - เพิ่มความพึงพอใจของทีมพัฒนา
  - เพิ่มประสิทธิภาพในการจัดการความคาดหวัง
* **Product Thinking:** ทักษะนี้ช่วยแก้ปัญหา (Pain Point) ให้กับ:
  - ทีมพัฒนาที่ต้องการความชัดเจนเกี่ยวกับ Technical Debt ที่มีอยู่
  - ผู้ตัดสินใจที่ต้องการความมั่นใจในการประเมินความเสี่ยง
  - ลูกค้าที่ต้องการ Feature ใหม่ที่เสถียร
  - ทีม DevOps ที่ต้องการระบบที่ Deploy ได้ง่าย
  - ผู้บริหารที่ต้องการความสามารถในการวางแผนงบริหาร

### **2. Technical Deep Dive (The "How-to")**

* **Core Logic:** Technical Debt Management เป็นกระบวนการที่ช่วยให้:
  - **Debt Identification:** การระบุ Technical Debt ที่มีอยู่ในระบบ
  - **Debt Classification:** การจัดประเภท Technical Debt ตามประเภท (Code, Design, Architecture, Test, Documentation, Infrastructure)
  - **Debt Quantification:** การประเมินมูลค่าของ Technical Debt (Effort, Interest, Risk)
  - **Debt Prioritization:** การจัดลำดับ Technical Debt ตามความสำคัญและความเร่งด่วน
  - **Debt Repayment Strategy:** การวางแผนการชำระหนี้ Technical Debt (Refactoring, Rewriting, Paying Down)
  - **Debt Prevention:** การป้องกันการสะสม Technical Debt ใหม่

* **Architecture Diagram Requirements:** แผนผังสถาปัตยกรรมที่ต้องมี:
  - **Debt Register Template:** Template สำหรับการบันทึก Technical Debt
  - **Debt Classification Matrix:** แผนผังแสดงการจัดประเภท Technical Debt
  - **Debt Impact Analysis:** แผนผังแสดงผลกระทบของ Technical Debt
  - **Repayment Workflow Diagram:** แผนผังแสดงกระบวนการชำระหนี้ Technical Debt
  - **Prevention Process Diagram:** แผนผังแสดงกระบวนการป้องกันการสะสม Technical Debt

* **Implementation Workflow:**
  1. **Identify Debt:** ระบุ Technical Debt ที่มีอยู่ในระบบ
  2. **Classify Debt:** จัดประเภท Technical Debt ตามประเภทและความรุนแรง
  3. **Quantify Debt:** ประเมินมูลค่าของ Technical Debt (Effort, Interest, Risk)
  4. **Prioritize Debt:** จัดลำดับ Technical Debt ตามความสำคัญและความเร่งด่วน
  5. **Create Repayment Plan:** สร้างแผนการชำระหนี้ Technical Debt
  6. **Execute Repayment:** ดำเนินการชำระหนี้ Technical Debt ตามแผน
  7. **Monitor Progress:** ติดตามความคืบหนี้
  8. **Prevent New Debt:** ป้องกันการสะสม Technical Debt ใหม่

### **3. Tooling & Tech Stack**

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้:
  - **Code Analysis Tools:** SonarQube, CodeQL, Coverity, Fortify
  - **Debt Tracking Tools:** Jira, Azure DevOps, Linear, Shortcut
  - **Documentation Platforms:** Confluence, Notion, GitHub Wiki
  - **CI/CD Integration:** GitHub Actions, GitLab CI, Azure Pipelines
  - **Metrics Collection:** Datadog, New Relic, Prometheus

* **Configuration Essentials:** ส่วนประกอบสำคัญในการตั้งค่า:
  - **Debt Thresholds:** การตั้งค่าเกณวันสำหรับ Technical Debt
  - **Classification Rules:** กฎการจัดประเภท Technical Debt
  - **Severity Levels:** การจัดระดับความรุนแรงของ Technical Debt
  - **Interest Rate Calculation:** สูตรการคำนวณดอกเบี้ของ Technical Debt
  - **Repayment Schedule:** การวางแผนการจัดตารางชำระหนี้

### **4. Standards, Compliance & Security**

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  - **ISO/IEC 25010:** Software Quality Model
  - **IEEE 730:** Standard for Software Quality Assurance
  - **CMMI:** Capability Maturity Model Integration

* **Security Protocol:** กลไกการป้องกัน:
  - **Access Control:** การควบคุมการเข้าถึงข้อมูล Debt Register
  - **Audit Trail:** การบันทึกการเข้าถึงและการแก้ไข
  - **Classification:** การจัดประเภท Technical Debt ตามความละเอียด
  - **Backup and Recovery:** การสำรองและการกู้คืนข้อมูล

* **Explainability:** ความสามารถในการอธิบาย:
  - **Debt Rationale Documentation:** การบันทึกเหตุผลของการสะสม Technical Debt
  - **Impact Analysis:** การวิเคราะห์ผลกระทบของ Technical Debt
  - **Repayment Justification:** การอธิบายเหตุผลของการชำระหนี้
  - **Stakeholder Communication:** การสื่อสารกับผู้มีส่วนได้ส่วนเสีย

### **5. Unit Economics & Performance Metrics (KPIs)**

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย (COGS):
  ```
  Total Cost = (Interest Cost) + (Repayment Cost) + (Opportunity Cost)
  
  ROI = (Productivity Gain - Total Cost) / Total Cost × 100%
  
  Interest Cost = (Debt Hours × Hourly Rate × Interest Rate × Time)
  Productivity Gain = (Velocity Improvement × Hourly Rate × Time)
  ```

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  - **Debt Identification Rate:** % ของ Technical Debt ที่ถูกระบุ (Target: > 90%)
  - **Debt Reduction Rate:** % ของ Technical Debt ที่ถูกชำระหนี้ต่อปี (Target: > 20%)
  - **Velocity Improvement:** % ของการเพิ่มความเร็วในการพัฒนา (Target: > 15%)
  - **Code Quality Score:** คะแนนคุณภาพของโค้ด (Target: > B)
  - **Team Satisfaction:** ความพึงพอใจของทีม (Target: > 4/5)

### **6. Strategic Recommendations (CTO Insights)**

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน:
  1. **Phase 1 (Months 1-2):** สร้าง Debt Register และ Guidelines, ฝึกอบรมทีม
  2. **Phase 2 (Months 3-4):** เริ่มระบุและจัดประเภท Technical Debt
  3. **Phase 3 (Months 5-6):** สร้างแผนการชำระหนี้และเริ่มดำเนินการ
  4. **Phase 4 (Year 2+):** ขยายไปยังทุกทีม, สร้าง Culture ของการจัดการ Technical Debt

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาด:
  - **Ignoring Debt:** ต้องระบุและจัดการ Technical Debt อย่างต่อเนื่อง
  - **Over-refactoring:** หลีกเลี่ยงการ Refactoring ที่ไม่ให้ผลลัพธ์ทางธุรกิจ
  - **Not Prioritizing:** ต้องจัดลำดับ Technical Debt ตามความสำคัญ
  - **No Prevention:** ต้องมีกระบวนการป้องกันการสะสม Technical Debt ใหม่
  - **Poor Communication:** ต้องสื่อสารกับผู้มีส่วนได้ส่วนเสียอย่างชัดเจน
  - **Not Measuring:** ต้องวัดผลและปรับปรุงกระบวนการอย่างต่อเนื่อง
  - **Short-term Focus:** ต้องพิจารณาผลกระทบระยะยาว

---

## Overview

Technical debt is the implied cost of additional rework caused by choosing an easy solution now instead of using a better approach that would take longer. This skill provides frameworks for identifying, classifying, quantifying, and managing technical debt to maintain code quality and development velocity.

**When to use this skill:** When managing code quality, planning refactoring efforts, making architectural decisions, or conducting periodic code reviews.

## Types of Technical Debt

### 1. Code Debt

**Definition:** Poorly written or structured code that needs cleanup

**Examples:**
- Duplicated code
- Long methods/functions
- Poor naming conventions
- Missing error handling
- Inconsistent code style

**Detection:**
```typescript
// Bad: Duplicated code
function calculateDiscount(price) {
  if (price > 1000) return price * 0.9;
  if (price > 500) return price * 0.95;
  return price;
}

function calculateDiscount2(price) {
  if (price > 1000) return price * 0.9;
  if (price > 500) return price * 0.95;
  return price;
}

// Good: Reusable function
function calculateDiscount(price: number, discountRules: DiscountRule[]): number {
  for (const rule of discountRules) {
    if (rule.condition(price)) {
      return price * rule.discount;
    }
  }
  return price;
}
```

### 2. Design Debt

**Definition:** Poor design choices that lead to complexity

**Examples:**
- Tight coupling between components
- Violation of SOLID principles
- God objects
- Circular dependencies
- Poor separation of concerns

**Detection:**
```typescript
// Bad: Tight coupling
class OrderService {
  private database: Database;
  private emailService: EmailService;
  private paymentService: PaymentService;
  private inventoryService: InventoryService;
  private shippingService: ShippingService;
  private notificationService: NotificationService;
  
  constructor() {
    this.database = new Database();
    this.emailService = new EmailService();
    this.paymentService = new PaymentService();
    this.inventoryService = new InventoryService();
    this.shippingService = new ShippingService();
    this.notificationService = new NotificationService();
  }
}

// Good: Dependency injection
class OrderService {
  constructor(
    private database: Database,
    private emailService: EmailService,
    private paymentService: PaymentService,
    private inventoryService: InventoryService,
    private shippingService: ShippingService,
    private notificationService: NotificationService
  ) {}
}
```

### 3. Architecture Debt

**Definition:** Poor architectural decisions that limit scalability or maintainability

**Examples:**
- Monolithic architecture when microservices would be better
- Missing abstraction layers
- Poor data modeling
- Inadequate caching strategy
- No separation of concerns

**Detection:**
```typescript
// Bad: Direct database access from API layer
app.get('/api/users/:id', async (req, res) => {
  const user = await db.query('SELECT * FROM users WHERE id = $1', [req.params.id]);
  res.json(user);
});

// Good: Repository pattern
app.get('/api/users/:id', async (req, res) => {
  const user = await userRepository.findById(req.params.id);
  res.json(user);
});
```

### 4. Test Debt

**Definition:** Insufficient or missing test coverage

**Examples:**
- No unit tests
- Brittle tests
- Missing edge case coverage
- Slow tests
- Tests that don't actually test the code

**Detection:**
```typescript
// Bad: No tests
function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// Good: With tests
describe('calculateTotal', () => {
  it('calculates total correctly', () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 3 }
    ];
    expect(calculateTotal(items)).toBe(35);
  });
  
  it('handles empty cart', () => {
    expect(calculateTotal([])).toBe(0);
  });
});
```

### 5. Documentation Debt

**Definition:** Missing or outdated documentation

**Examples:**
- No API documentation
- Missing README files
- Outdated comments
- No architecture diagrams
- No onboarding guides

**Detection:**
```typescript
// Bad: No documentation
function calculateTax(price: number, rate: number): number {
  return price * rate;
}

// Good: With documentation
/**
 * Calculates tax for a given price and rate
 * @param price - The base price before tax
 * @param rate - The tax rate as a decimal (e.g., 0.1 for 10%)
 * @returns The tax amount
 * @example calculateTax(100, 0.1) // returns 10
 */
function calculateTax(price: number, rate: number): number {
  return price * rate;
}
```

### 6. Infrastructure Debt

**Definition:** Outdated or poorly configured infrastructure

**Examples:**
- Outdated dependencies
- Security vulnerabilities
- Poor monitoring
- No backup strategy
- Inadequate scaling configuration

**Detection:**
```json
// Bad: Outdated dependencies
{
  "dependencies": {
    "express": "^4.16.0",
    "lodash": "^4.17.0"
  }
}

// Good: Up-to-date dependencies
{
  "dependencies": {
    "express": "^4.18.0",
    "lodash": "^4.17.21"
  }
}
```

## Debt Identification

### Code Analysis Tools

#### SonarQube

```bash
# Install
docker run -d --name sonarqube -p 9000:9000 sonarqube

# Scan project
sonar-scanner \
  -Dsonar.projectKey=my-project \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000
```

**Key Metrics:**
- Code smells
- Bugs
- Vulnerabilities
- Code coverage
- Duplication
- Technical debt ratio

#### CodeQL

```bash
# Install
npm install -g codeql

# Create database
codeql database create my-project-db --language=typescript

# Run queries
codeql query run --database=my-project-db codeql-queries
```

**Key Metrics:**
- Security vulnerabilities
- Code quality issues
- Complexity metrics

### Manual Review

**Checklist:**
```markdown
## Code Review Checklist

### Code Quality
- [ ] No code duplication
- [ ] Functions are short and focused
- [ ] Naming conventions followed
- [ ] Error handling present
- [ ] Comments are useful and accurate

### Design Quality
- [ ] SOLID principles followed
- [ ] Proper separation of concerns
- [ ] Appropriate use of design patterns
- [ ] No tight coupling
- [ ] Interfaces are well-defined

### Test Coverage
- [ ] Unit tests for critical paths
- [ ] Integration tests for workflows
- [ ] Edge cases covered
- [ ] Tests are fast and reliable
- [ ] Test documentation is clear

### Documentation
- [ ] README is up-to-date
- [ ] API documentation exists
- [ ] Architecture diagrams are current
- [ ] Code comments are helpful
- [ ] Onboarding guide exists
```

## Debt Quantification

### Effort Estimation

```typescript
interface DebtItem {
  id: string;
  type: 'code' | 'design' | 'architecture' | 'test' | 'documentation' | 'infrastructure';
  description: string;
  location: string;
  estimatedHours: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  interestRate: number; // Additional cost per month
  createdAt: Date;
}

const debtItems: DebtItem[] = [
  {
    id: 'DEBT-001',
    type: 'code',
    description: 'Duplicated discount calculation logic',
    location: 'src/services/order.ts',
    estimatedHours: 8,
    severity: 'medium',
    interestRate: 0.1, // 10% additional cost per month
    createdAt: new Date('2024-01-15')
  }
];

function calculateTotalDebt(debtItems: DebtItem[]): {
  totalHours: number;
  weightedHours: number;
} {
  const severityWeights = {
    low: 1,
    medium: 2,
    high: 3,
    critical: 5
  };

  const totalHours = debtItems.reduce((sum, item) => sum + item.estimatedHours, 0);
  const weightedHours = debtItems.reduce((sum, item) => 
    sum + (item.estimatedHours * severityWeights[item.severity]), 0
  );

  return { totalHours, weightedHours };
}
```

### Interest Calculation

```typescript
function calculateInterest(debtItem: DebtItem, monthsElapsed: number): number {
  return debtItem.estimatedHours * debtItem.interestRate * monthsElapsed;
}

// Example
const debtItem: DebtItem = {
  estimatedHours: 8,
  interestRate: 0.1 // 10% per month
};

const interestAfter6Months = calculateInterest(debtItem, 6);
// Result: 4.8 hours of additional cost
```

## Debt Prioritization

### Prioritization Matrix

```
                Impact
                │  Low  │ Medium │ High  │ Critical
────────────────┼────────┼────────┼────────┼──────────
Severity        │        │        │        │
────────────────┼────────┼────────┼────────┼──────────
Critical        │  Low   │ Medium │ High   │ Critical
────────────────┼────────┼────────┼────────┼──────────
High            │  Low   │ Medium │ High   │ Critical
────────────────┼────────┼────────┼────────┼──────────
Medium          │  Low   │ Low    │ Medium │ High
────────────────┼────────┼────────┼────────┼──────────
Low             │  Low   │ Low    │ Low    │ Medium
```

### Prioritization Algorithm

```typescript
interface PrioritizedDebt extends DebtItem {
  priorityScore: number;
}

function prioritizeDebt(debtItems: DebtItem[]): PrioritizedDebt[] {
  const severityWeights = {
    low: 1,
    medium: 2,
    high: 3,
    critical: 5
  };

  const ageWeights = {
    recent: 1,    // < 3 months
    moderate: 2,  // 3-6 months
    old: 3        // > 6 months
  };

  return debtItems.map(item => {
    const age = getDebtAge(item.createdAt);
    const ageWeight = age < 90 ? ageWeights.recent : 
                      age < 180 ? ageWeights.moderate : 
                      ageWeights.old;

    const priorityScore = 
      (item.estimatedHours * severityWeights[item.severity]) +
      (item.estimatedHours * ageWeight);

    return {
      ...item,
      priorityScore
    };
  }).sort((a, b) => b.priorityScore - a.priorityScore);
}
```

## Debt Repayment Strategy

### 1. Refactoring

**When to use:**
- Code is functional but poorly structured
- Design needs improvement
- No breaking changes required

**Example:**
```typescript
// Before: Duplicated code
function getUserData(userId: string) {
  const user = db.query('SELECT * FROM users WHERE id = ?', [userId]);
  const orders = db.query('SELECT * FROM orders WHERE user_id = ?', [userId]);
  const payments = db.query('SELECT * FROM payments WHERE user_id = ?', [userId]);
  return { user, orders, payments };
}

function getUserData2(userId: string) {
  const user = db.query('SELECT * FROM users WHERE id = ?', [userId]);
  const orders = db.query('SELECT * FROM orders WHERE user_id = ?', [userId]);
  const payments = db.query('SELECT * FROM payments WHERE user_id = ?', [userId]);
  return { user, orders, payments };
}

// After: Reusable function
function getUserData(userId: string): Promise<UserData> {
  const [user, orders, payments] = await Promise.all([
    db.query('SELECT * FROM users WHERE id = ?', [userId]),
    db.query('SELECT * FROM orders WHERE user_id = ?', [userId]),
    db.query('SELECT * FROM payments WHERE user_id = ?', [userId])
  ]);
  return { user, orders, payments };
}
```

### 2. Rewriting

**When to use:**
- Code is fundamentally flawed
- Better approach exists
- Breaking changes acceptable

**Example:**
```typescript
// Before: Poor design
class UserService {
  async getUser(id: string) {
    const user = await db.query('SELECT * FROM users WHERE id = ?', [id]);
    return user;
  }
  
  async updateUser(id: string, data: any) {
    await db.query('UPDATE users SET ? WHERE id = ?', [data, id]);
  }
  
  async deleteUser(id: string) {
    await db.query('DELETE FROM users WHERE id = ?', [id]);
  }
}

// After: Repository pattern
interface UserRepository {
  findById(id: string): Promise<User>;
  update(id: string, data: Partial<User>): Promise<void>;
  delete(id: string): Promise<void>;
}

class PostgresUserRepository implements UserRepository {
  async findById(id: string): Promise<User> {
    const result = await db.query('SELECT * FROM users WHERE id = ?', [id]);
    return result[0];
  }
  
  async update(id: string, data: Partial<User>): Promise<void> {
    await db.query('UPDATE users SET ? WHERE id = ?', [data, id]);
  }
  
  async delete(id: string): Promise<void> {
    await db.query('DELETE FROM users WHERE id = ?', [id]);
  }
}
```

### 3. Paying Down

**When to use:**
- Debt is acceptable for now
- Better to address later
- Resources not available now

**Strategy:**
```typescript
interface DebtPaymentPlan {
  debtItem: DebtItem;
  scheduledDate: Date;
  assignedTo: string;
  estimatedCompletion: Date;
}

function createPaymentPlan(debtItems: PrioritizedDebt[]): DebtPaymentPlan[] {
  return debtItems.map((item, index) => ({
    debtItem: item,
    scheduledDate: getNextSprintDate(index),
    assignedTo: assignDeveloper(item),
    estimatedCompletion: calculateCompletionDate(item)
  }));
}
```

## Debt Prevention

### 1. Code Review Standards

```typescript
// Pull Request Template
interface PRChecklist {
  codeQuality: boolean;
  tests: boolean;
  documentation: boolean;
  performance: boolean;
  security: boolean;
}

const prChecklist: PRChecklist = {
  codeQuality: [
    'No code duplication',
    'Follows style guide',
    'Proper error handling',
    'Meaningful variable names'
  ],
  tests: [
    'Unit tests for new code',
    'Integration tests for workflows',
    'Edge cases covered',
    'Tests are fast'
  ],
  documentation: [
    'README updated if needed',
    'API documentation updated',
    'Code comments added',
    'Architecture diagrams updated'
  ],
  performance: [
    'Performance impact considered',
    'No unnecessary re-renders',
    'Efficient algorithms',
    'Proper caching'
  ],
  security: [
    'Input validation',
    'Output encoding',
    'SQL injection prevention',
    'XSS prevention'
  ]
};
```

### 2. Automated Quality Gates

```yaml
# .github/workflows/quality-gate.yml
name: Quality Gate

on: [pull_request]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run SonarQube Scan
        uses: sonarsource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          
      - name: Check Coverage
        run: |
          npm test -- --coverage
          if [ $(cat coverage/coverage-summary.json | jq '.total.lines.pct') -lt 80 ]; then
            echo "Coverage below 80%"
            exit 1
          fi
```

### 3. Continuous Improvement

```typescript
// Debt Reduction Sprints
interface DebtReductionSprint {
  sprintNumber: number;
  targetDebtItems: string[];
  allocatedHours: number;
  actualHours: number;
  debtPaid: number;
}

function planDebtReductionSprint(
  debtItems: PrioritizedDebt[],
  availableHours: number
): DebtReductionSprint {
  const targetItems = debtItems
    .filter(item => item.priorityScore > threshold)
    .slice(0, 5); // Top 5 items

  const totalEstimatedHours = targetItems.reduce(
    (sum, item) => sum + item.estimatedHours,
    0
  );

  return {
    sprintNumber: getNextSprintNumber(),
    targetDebtItems: targetItems.map(item => item.id),
    allocatedHours: availableHours,
    actualHours: 0,
    debtPaid: 0
  };
}
```

## Best Practices

1. **Track Debt Explicitly** - Keep a debt register
2. **Prioritize Ruthlessly** - Focus on highest-impact debt first
3. **Pay Down Regularly** - Allocate time in every sprint
4. **Prevent New Debt** - Use code reviews and quality gates
5. **Measure Everything** - Track velocity, quality, and debt
6. **Communicate Clearly** - Keep stakeholders informed
7. **Learn from Mistakes** - Understand why debt was incurred
8. **Balance Speed and Quality** - Don't sacrifice everything for speed
9. **Automate Detection** - Use tools to find debt automatically
10. **Make It Cultural** - Everyone should care about code quality

## Common Pitfalls

1. **Ignoring Debt** - Debt doesn't go away on its own
2. **Over-optimizing** - Don't spend too much time on minor issues
3. **No Prioritization** - All debt is not equal
4. **No Tracking** - You can't manage what you don't measure
5. **Short-term Focus** - Consider long-term consequences
6. **Blaming Individuals** - Debt is usually systemic
7. **Not Learning** - Understand root causes
8. **Inconsistent Standards** - Everyone should follow same rules
9. **No Prevention** - Stop debt before it starts
10. **Poor Communication** - Keep everyone aligned

## Resources

- [SonarQube Documentation](https://docs.sonarqube.org/)
- [Technical Debt Quadrant](https://martinfowler.com/bliki/TechnicalDebtQuadrant)
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350872)
- [Refactoring by Martin Fowler](https://www.amazon.com/Refactoring-Improving-Existing-Code/dp/0201485672)
- [Working Effectively with Legacy Code by Michael Feathers](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131170842)
