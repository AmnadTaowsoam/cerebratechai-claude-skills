### **05: Safe Refactoring Patterns**

> 
> **Current Level:** Expert (Enterprise Scale) 
> 
> 
> **Domain:** Foundations / Code Quality 
> 

---

### **1. Executive Summary & Strategic Necessity**

* **Context:** ในโลกปี 2025-2026 การพัฒนาซอฟต์แวร์มีความซับซ้อนเพิ่มขึ้นอย่างมาก การ Refactoring ที่ปลอดภัยเป็นกระบวนการที่ช่วยให้ทีมพัฒนาสามารถปรับปรุงโค้ดที่มีอยู่โดยไม่ทำให้ระบบหยุดชะงัก การ Refactoring ที่ปลอดภัยช่วยลด Technical Debt และเพิ่มความสามารถในการบำรุงรักษา
* **Business Impact:** การใช้ Refactoring Patterns ที่มีประสิทธิภาพช่วย:
  - ลดความเสี่ยงในการปรับปรุงโค้ด
  - เพิ่มความเสถียรของระบบ
  - ลด Technical Debt ที่สะสมในระยะว
  - เพิ่มประสิทธิภาพในการพัฒนา
  - ลดเวลาในการแก้ไข Bug
  - เพิ่มความสามารถในการทำงานร่วมกัน
  - เพิ่มความโปร่งใสในการพัฒนา
* **Product Thinking:** ทักษะนี้ช่วยแก้ปัญหา (Pain Point) ให้กับ:
  - ทีมพัฒนาที่ต้องการ Refactor Legacy Code
  - ผู้ทำงานผิดพลาดที่ต้องการ Refactor ที่ปลอดภัย
  - ทีมพัฒนาที่ต้องการลด Technical Debt
  - ลูกค้าที่ต้องการความเสถียรของระบบ
  - ทีม Support ที่ต้องการ Debug ของ Code

### **2. Technical Deep Dive (The "How-to")**

* **Core Logic:** Refactoring Patterns ประกอบด้วย:
  - **Refactoring Safety Principles:** หลักการ Refactoring ที่ปลอดภัย (Never Break What Works, Change in Small Steps, Verify After Each Step, Maintain Backward Compatibility, Have a Rollback Plan, Document Change)
  - **The Strangler Fig Pattern:** รูปแบบการแทนที่ระบบเก่าด้วยระบบใหม่ (Create New Implementation, Add Facade/Routing Layer, Migrate Traffic Gradually, Monitor and Verify, Remove Old System)
  - **The Parallel Change Pattern:** รูปแบบการเปลี่ยนแปลงแบบขนาน (Phase 1: Expand, Phase 2: Migrate, Phase 3: Contract)
  - **Verification Between Changes:** การตรวจสอบระหว่างการเปลี่ยนแปลง (Unit Verification, Integration Verification, Regression Verification, Performance Verification)
  - **Refactoring Checklist:** รายการตรวจสอบการ Refactoring (Before Starting, During Refactoring, After Refactoring)
  - **Common Refactoring Scenarios:** สถานการณ์ทั่วไปของการ Refactoring (Extracting a Function, Renaming a Method, Changing Data Structure)

* **Architecture Diagram Requirements:** แผนผังสถาปัตยกรรมที่ต้องมี:
  - **Refactoring Safety Protocol Diagram:** แผนผังแสดงกระบวนการ Refactoring ที่ปลอดภัย
  - **Strangler Fig Pattern Diagram:** แผนผังแสดงรูปแบบ Strangler Fig
  - **Parallel Change Pattern Diagram:** แผนผังแสดงรูปแบบ Parallel Change
  - **Verification Protocol Diagram:** แผนผังแสดงกระบวนการ Verification
  - **Migration Flow Diagram:** แผนผังแสดงกระบวนการ Migration

* **Implementation Workflow:**
  1. **Identify Refactoring Need:** ระบุความต้องการ Refactoring
  2. **Understand Current Behavior:** ทำความเข้าใจพฤติกรรมปัจจุบัน
  3. **Write Tests for Current Behavior:** เขียน Tests สำหรับพฤติกรรมปัจจุบัน
  4. **Plan Refactoring Steps:** วางแผนขั้นตอนการ Refactoring
  5. **Execute Steps One by One:** ดำเนินการ Refactoring ทีละขั้น
  6. **Verify After Each Step:** ตรวจสอบหลังจากแต่ละขั้น
  7. **Complete Refactoring:** ทำการ Refactoring ให้เสร็จสิ้น

### **3. Tooling & Tech Stack**

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้:
  - **Version Control:** Git, GitHub, GitLab, Bitbucket
  - **Testing Frameworks:** Jest, Pytest, JUnit, NUnit
  - **Code Analysis Tools:** SonarQube, CodeQL, Coverity, Fortify
  - **CI/CD Platforms:** GitHub Actions, GitLab CI, Azure Pipelines, Jenkins
  - **Monitoring Tools:** Datadog, New Relic, Prometheus, Grafana
  - **Documentation Tools:** Confluence, Notion, GitHub Wiki

* **Configuration Essentials:** ส่วนประกอบสำคัญในการตั้งค่า:
  - **Git Configuration:** การตั้งค่า Git สำหรับ Refactoring (Branch Protection, Required Reviews, Status Checks)
  - **CI/CD Configuration:** การตั้งค่า CI/CD สำหรับ Automated Testing
  - **Monitoring Configuration:** การตั้งค่า Monitoring สำหรับ Tracking Changes
  - **Feature Flags:** การตั้งค่า Feature Flags สำหรับ Gradual Rollout
  - **Rollback Configuration:** การตั้งค่า Rollback สำหรับ Emergency Reversal

### **4. Standards, Compliance & Security**

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  - **ISO/IEC 25010:** Software Quality Model
  - **IEEE 730:** Standard for Software Quality Assurance
  - **Refactoring Best Practices:** แนวทางปฏิบัติที่ดีในการ Refactoring
  - **Code Quality Standards:** มาตรฐานคุณภาพของโค้ด

* **Security Protocol:** กลไกการป้องกัน:
  - **Access Control:** การควบคุมการเข้าถึง Code ที่กำลัง Refactor
  - **Audit Trail:** การบันทึกการเข้าถึงและการเปลี่ยนแปลง
  - **Security Scanning:** การสแกน Security Vulnerabilities ก่อน Deploy
  - **Code Review:** การทบทวน Code ก่อน Merge
  - **Rollback Plan:** แผนการ Rollback สำหรับ Emergency Reversal

* **Explainability:** ความสามารถในการอธิบาย:
  - **Refactoring Rationale Documentation:** การบันทึกเหตุผลของการ Refactoring
  - **Change Log:** การบันทึกการเปลี่ยนแปลง
  - **Before/After Comparison:** การเปรียบเทียบก่อนและหลัง Refactoring
  - **Migration Documentation:** การบันทึกกระบวนการ Migration

### **5. Unit Economics & Performance Metrics (KPIs)**

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย (COGS):
  ```
  Total Cost = (Refactoring Time × Hourly Rate) + 
               (Testing Time × Hourly Rate) + 
               (Rollback Time × Hourly Rate) + 
               (Tooling Cost)
  
  ROI = (Productivity Gain - Total Cost) / Total Cost × 100%
  
  Productivity Gain = (Time Saved on Bug Fixes) + 
                      (Time Saved on Maintenance) + 
                      (Time Saved on New Features)
  ```

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  - **Refactoring Success Rate:** % ของ Refactoring ที่สำเร็จ (Target: > 95%)
  - **Bug Reduction Rate:** % ของ Bugs ที่ลดลง (Target: > 20%)
  - **Code Quality Score:** คะแนนคุณภาพของโค้ด (Target: > B)
  - **Technical Debt Reduction:** % ของ Technical Debt ที่ลดลง (Target: > 15%)
  - **Development Velocity:** จำนวน Features ต่อสัปดาห์ (Target: > 5/week)
  - **Team Satisfaction:** ความพึงพอใจของทีม (Target: > 4/5)

### **6. Strategic Recommendations (CTO Insights)**

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน:
  1. **Phase 1 (Months 1-2):** สร้าง Refactoring Standards และ Guidelines, ฝึกอบรมทีม
  2. **Phase 2 (Months 3-4):** ตั้งค่า Testing Tools และ CI/CD Pipeline
  3. **Phase 3 (Months 5-6):** ฝึกอบรมทีมเกี่ยวกับ Refactoring Patterns และ Best Practices
  4. **Phase 4 (Year 2+):** ขยายไปยังทุกทีม, สร้าง Culture ของ Safe Refactoring

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาด:
  - **Skipping Verification:** หลีกเลี่ยงการไม่ตรวจสอบหลังจากแต่ละขั้น
  - **Making Too Many Changes at Once:** หลีกเลี่ยงการทำการเปลี่ยนแปลงมากเกินไปในครั้งเดียว
  - **Not Having Tests:** หลีกเลี่ยงการไม่มี Tests ก่อน Refactoring
  - **Breaking Backward Compatibility:** หลีกเลี่ยงการทำลา Backward Compatibility
  - **No Rollback Plan:** หลีกเลี่ยงการไม่มีแผนการ Rollback
  - **Refactoring Without Understanding:** หลีกเลี่ยงการ Refactoring โดยไม่ทำความเข้าใจ
  - **Forgetting to Update Documentation:** หลีกเลี่ยงการลืมอัปเดต Documentation

---

## Overview

Safe refactoring is the practice of modifying existing code without breaking functionality. This skill teaches patterns and protocols for making changes to production codebases safely, focusing on "brownfield" development where existing systems must remain operational while improvements are made.

**When to use this skill:** When modifying, improving, or restructuring existing code that is currently in use or production.

## Refactoring Safety Principles

### Core Principles

1. **Never Break What Works** - Existing functionality must remain intact
2. **Change in Small Steps** - Each change should be independently verifiable
3. **Verify After Each Step** - Run tests and checks before proceeding
4. **Maintain Backward Compatibility** - Don't break existing consumers
5. **Have a Rollback Plan** - Know how to revert if something goes wrong
6. **Document Change** - Explain why and what was changed

### The Safety Protocol

```mermaid
graph TD
    A[Identify Refactoring Need] --> B[Understand Current Behavior]
    B --> C[Write Tests for Current Behavior]
    C --> D[Plan Refactoring Steps]
    D --> E[Execute Step 1]
    E --> F[Verify: Tests Pass?]
    F -->|Yes| G[More Steps?]
    F -->|No| H[Rollback Step 1]
    H --> I[Diagnose Issue]
    I --> E
    G -->|Yes| J[Execute Next Step]
    G -->|No| K[Refactoring Complete]
    J --> F
```

### Pre-Refactoring Checklist

```markdown
## Pre-Refactoring Checklist

### Understanding
- [ ] I understand what current code does
- [ ] I understand why it was written this way
- [ ] I know who/what depends on this code
- [ ] I have identified all entry points and side effects

### Safety
- [ ] Tests exist for current behavior
- [ ] If no tests, I will add tests first
- [ ] I know how to rollback changes
- [ ] I have a backup/branch of working code

### Planning
- [ ] Refactoring is broken into small steps
- [ ] Each step can be verified independently
- [ ] Dependencies between steps are understood
- [ ] Time estimate includes testing and verification
```

## The Strangler Fig Pattern

### Concept

The Strangler Fig pattern involves gradually replacing an old system by building new functionality alongside it, then migrating usage incrementally. The old system is "strangled" piece by piece until it can be completely removed.

### When to Use

- Replacing legacy systems
- Major architectural changes
- Migrating between frameworks/libraries
- When a complete rewrite is too risky

### Implementation Steps

```mermaid
graph LR
    A[Old System] --> B[Create New Implementation]
    B --> C[Add Facade/Routing Layer]
    C --> D[Migrate Traffic Gradually]
    D --> E[Monitor and Verify]
    E --> F{Migration Complete?}
    F -->|No| D
    F -->|Yes| G[Remove Old System]
```

### Step-by-Step Process

#### Step 1: Create New Implementation

```javascript
// OLD: Legacy user service
class LegacyUserService {
  async getUser(id) {
    // Old implementation
    return database.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}

// NEW: Modern user service
class ModernUserService {
  async getUser(id) {
    // New implementation with better structure
    const user = await this.userRepository.findById(id);
    return this.userMapper.toDTO(user);
  }
}
```

#### Step 2: Add Facade/Routing Layer

```javascript
// Facade that routes between old and new
class UserServiceFacade {
  constructor(legacyService, modernService) {
    this.legacyService = legacyService;
    this.modernService = modernService;
    this.useModern = false; // Feature flag
  }

  async getUser(id) {
    if (this.useModern) {
      return this.modernService.getUser(id);
    }
    return this.legacyService.getUser(id);
  }

  setUseModern(useModern) {
    this.useModern = useModern;
  }
}
```

#### Step 3: Migrate Traffic Gradually

```javascript
// Gradual migration strategy
async function migrateUsers() {
  const facade = new UserServiceFacade(legacyService, modernService);
  const migratedUserIds = new Set();

  // Migrate users incrementally
  for (const userId of allUsers) {
    // Test with new implementation
    const legacyResult = await facade.legacyService.getUser(userId);
    const modernResult = await facade.modernService.getUser(userId);

    // Verify results match
    if (resultsMatch(legacyResult, modernResult)) {
      migratedUserIds.add(userId);
      facade.setUseModern(userId, true);
    } else {
      // Log discrepancy for investigation
      logMismatch(userId, legacyResult, modernResult);
    }
  }

  return migratedUserIds;
}
```

#### Step 4: Monitor and Verify

```javascript
// Monitoring during migration
class MigrationMonitor {
  constructor() {
    this.metrics = {
      totalRequests: 0,
      modernRequests: 0,
      legacyRequests: 0,
      errors: 0,
      mismatches: 0
    };
  }

  trackRequest(userId, usedModern, error, mismatch) {
    this.metrics.totalRequests++;
    if (usedModern) this.metrics.modernRequests++;
    else this.metrics.legacyRequests++;
    if (error) this.metrics.errors++;
    if (mismatch) this.metrics.mismatches++;
  }

  getMetrics() {
    return {
      ...this.metrics,
      modernPercentage: (this.metrics.modernRequests / this.metrics.totalRequests * 100).toFixed(2),
      errorRate: (this.metrics.errors / this.metrics.totalRequests * 100).toFixed(2)
    };
  }
}
```

#### Step 5: Remove Old System

```javascript
// Once migration is complete and verified
async function completeMigration() {
  const metrics = monitor.getMetrics();

  // Verify migration success
  if (metrics.modernPercentage >= 99.9 && metrics.errorRate < 0.01) {
    // Remove old implementation
    delete this.legacyService;
    // Remove facade, use modern directly
    this.userService = this.modernService;
    console.log('Migration complete: old system removed');
  } else {
    console.warn('Migration not complete:', metrics);
  }
}
```

### Strangler Fig Example: API Migration

```typescript
// OLD: Express API
app.get('/api/users/:id', async (req, res) => {
  const user = await legacyDb.query('SELECT * FROM users WHERE id = ?', [req.params.id]);
  res.json(user[0]);
});

// NEW: Fastify API
fastify.get('/api/users/:id', async (request, reply) => {
  const user = await userRepository.findById(request.params.id);
  return userMapper.toDTO(user);
});

// FACADE: Routing layer
app.use('/api/*', async (req, res, next) => {
  if (useFastify && isMigratedRoute(req.path)) {
    // Proxy to Fastify
    const response = await fastify.inject({
      method: req.method,
      url: req.url,
      headers: req.headers,
      body: req.body
    });
    res.status(response.statusCode).send(response.json());
  } else {
    next(); // Use Express
  }
});
```

## The Parallel Change Pattern

### Concept

The Parallel Change pattern involves making changes in three phases: expand, migrate, contract. This ensures backward compatibility while allowing safe evolution of APIs and data structures.

### Three Phases

```mermaid
graph LR
    A[Phase 1: Expand] --> B[Phase 2: Migrate]
    B --> C[Phase 3: Contract]

    subgraph Phase 1
        A1[Add New Field/Method]
        A2[Keep Old Field/Method]
        A3[Both Work]
    end

    subgraph Phase 2
        B1[Start Using New]
        B2[Gradual Migration]
        B3[Verify Compatibility]
    end

    subgraph Phase 3
        C1[All Consumers Migrated]
        C2[Remove Old Field/Method]
        C3[Cleanup Complete]
    end
```

### Phase 1: Expand

**Goal:** Add new functionality while keeping old functionality working.

```javascript
// BEFORE: Old API
class UserService {
  async getUser(id) {
    return database.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}

// AFTER PHASE 1: Both old and new
class UserService {
  // OLD: Still works
  async getUser(id) {
    return database.query('SELECT * FROM users WHERE id = ?', [id]);
  }

  // NEW: Added, but not used yet
  async getUserById(id) {
    const user = await this.userRepository.findById(id);
    return this.userMapper.toDTO(user);
  }
}
```

**Verification after Phase 1:**
```javascript
// Verify old functionality still works
describe('UserService - Phase 1', () => {
  it('old getUser method still works', async () => {
    const user = await userService.getUser(1);
    expect(user).toBeDefined();
    expect(user.id).toBe(1);
  });

  it('new getUserById method works', async () => {
    const user = await userService.getUserById(1);
    expect(user).toBeDefined();
    expect(user.id).toBe(1);
  });

  it('both methods return equivalent results', async () => {
    const oldUser = await userService.getUser(1);
    const newUser = await userService.getUserById(1);
    expect(oldUser).toEqual(newUser);
  });
});
```

### Phase 2: Migrate

**Goal:** Gradually switch consumers to use new implementation.

```javascript
// Migrate consumers one at a time
class UserController {
  // Consumer 1: Still using old
  async getOldWay(req, res) {
    const user = await userService.getUser(req.params.id);
    res.json(user);
  }

  // Consumer 2: Using new
  async getNewWay(req, res) {
    const user = await userService.getUserById(req.params.id);
    res.json(user);
  }
}

// Feature flag for gradual rollout
const useNewMethod = process.env.USE_NEW_USER_METHOD === 'true';

class UserController {
  async getUser(req, res) {
    const user = useNewMethod
      ? await userService.getUserById(req.params.id)
      : await userService.getUser(req.params.id);
    res.json(user);
  }
}
```

**Migration tracking:**
```javascript
class MigrationTracker {
  constructor() {
    this.migratedConsumers = new Set();
  }

  markMigrated(consumerId) {
    this.migratedConsumers.add(consumerId);
  }

  isMigrated(consumerId) {
    return this.migratedConsumers.has(consumerId);
  }

  getMigrationProgress(totalConsumers) {
    return {
      migrated: this.migratedConsumers.size,
      total: totalConsumers,
      percentage: (this.migratedConsumers.size / totalConsumers * 100).toFixed(2)
    };
  }
}
```

**Verification after Phase 2:**
```javascript
// Verify migration is working
describe('UserService - Phase 2', () => {
  it('migrated consumers use new method', async () => {
    const result = await userController.getNewWay({ params: { id: 1 } });
    expect(result).toBeDefined();
  });

  it('non-migrated consumers still work', async () => {
    const result = await userController.getOldWay({ params: { id: 1 } });
    expect(result).toBeDefined();
  });

  it('both methods produce same output', async () => {
    const oldResult = await userController.getOldWay({ params: { id: 1 } });
    const newResult = await userController.getNewWay({ params: { id: 1 } });
    expect(oldResult.body).toEqual(newResult.body);
  });
});
```

### Phase 3: Contract

**Goal:** Remove old functionality once all consumers are migrated.

```javascript
// BEFORE PHASE 3: Both methods exist
class UserService {
  async getUser(id) { /* old */ }
  async getUserById(id) { /* new */ }
}

// AFTER PHASE 3: Only new method
class UserService {
  async getUserById(id) {
    const user = await this.userRepository.findById(id);
    return this.userMapper.toDTO(user);
  }

  // Old method removed
  // async getUser(id) { ... }
}
```

**Pre-removal checklist:**
```markdown
## Phase 3: Pre-Removal Checklist

### Migration Status
- [ ] All consumers have been migrated
- [ ] No references to old method in codebase
- [ ] No external API dependencies on old method
- [ ] Documentation has been updated

### Testing
- [ ] All tests pass with new method only
- [ ] Integration tests verify new behavior
- [ ] Load tests perform as expected
- [ ] No performance regression

### Safety
- [ ] Rollback plan documented
- [ ] Monitoring in place
- [ ] Team notified of breaking change
- [ ] Version bumped (if API)
```

## Verification Between Changes

### The Verification Protocol

**CRITICAL:** Run verification tests AFTER EACH change, not just at the end.

### Verification Types

#### 1. Unit Verification

```javascript
// Test that individual components still work
describe('Post-refactoring unit tests', () => {
  it('calculates tax correctly', () => {
    const result = calculateTax(100, 0.1);
    expect(result).toBe(10);
  });

  it('validates email correctly', () => {
    const result = validateEmail('test@example.com');
    expect(result).toBe(true);
  });
});
```

#### 2. Integration Verification

```javascript
// Test that components work together
describe('Post-refactoring integration tests', () => {
  it('user can complete checkout flow', async () => {
    const user = await createUser();
    const cart = await addToCart(user.id, product);
    const order = await checkout(user.id, cart.id);
    expect(order.status).toBe('completed');
  });
});
```

#### 3. Regression Verification

```javascript
// Test that old functionality still works
describe('Post-refactoring regression tests', () => {
  it('legacy API endpoint still returns expected format', async () => {
    const response = await request(app).get('/api/v1/users/1');
    expect(response.status).toBe(200);
    expect(response.body).toHaveProperty('id');
    expect(response.body).toHaveProperty('name');
  });
});
```

#### 4. Performance Verification

```javascript
// Test that performance hasn't degraded
describe('Post-refactoring performance tests', () => {
  it('response time is within acceptable range', async () => {
    const start = Date.now();
    await userService.getUser(1);
    const duration = Date.now() - start;
    expect(duration).toBeLessThan(100); // 100ms threshold
  });
});
```

### Automated Verification Script

```bash
#!/bin/bash
# verify.sh - Run after each refactoring step

echo "=== Running Post-Refactoring Verification ==="

# Step 1: Unit tests
echo "1. Running unit tests..."
npm run test:unit
if [ $? -ne 0 ]; then
  echo "❌ Unit tests failed!"
  exit 1
fi
echo "✅ Unit tests passed"

# Step 2: Integration tests
echo "2. Running integration tests..."
npm run test:integration
if [ $? -ne 0 ]; then
  echo "❌ Integration tests failed!"
  exit 1
fi
echo "✅ Integration tests passed"

# Step 3: Linting
echo "3. Running linter..."
npm run lint
if [ $? -ne 0 ]; then
  echo "❌ Linting failed!"
  exit 1
fi
echo "✅ Linting passed"

# Step 4: Type checking (if TypeScript)
echo "4. Running type check..."
npm run type-check
if [ $? -ne 0 ]; then
  echo "❌ Type check failed!"
  exit 1
fi
echo "✅ Type check passed"

# Step 5: Build
echo "5. Running build..."
npm run build
if [ $? -ne 0 ]; then
  echo "❌ Build failed!"
  exit 1
fi
echo "✅ Build passed"

echo "=== All Verifications Passed! ==="
```

### Manual Verification Checklist

```markdown
## Manual Verification Checklist

After each refactoring step:

### Functionality
- [ ] Core features work as expected
- [ ] Edge cases handled correctly
- [ ] Error messages are appropriate
- [ ] User experience unchanged (unless intentional)

### Data Integrity
- [ ] No data corruption
- [ ] No data loss
- [ ] Data relationships maintained
- [ ] Database constraints satisfied

### Performance
- [ ] Response times acceptable
- [ ] No memory leaks
- [ ] CPU usage normal
- [ ] Database queries efficient

### Compatibility
- [ ] Backward compatibility maintained
- [ ] API contracts unchanged (unless in Phase 3)
- [ ] External integrations work
- [ ] Third-party dependencies compatible

### Security
- [ ] Authentication still works
- [ ] Authorization checks in place
- [ ] No new vulnerabilities introduced
- [ ] Sensitive data protected
```

## Refactoring Checklist

### Before Starting

```markdown
## Pre-Refactoring Checklist

### Preparation
- [ ] I understand current code
- [ ] I have identified all dependencies
- [ ] I have written tests for current behavior
- [ ] I have a clear refactoring plan
- [ ] I have estimated work

### Safety
- [ ] I have a backup/branch
- [ ] I know how to rollback
- [ ] I have notified stakeholders
- [ ] I have scheduled appropriate time

### Environment
- [ ] Development environment is ready
- [ ] Test environment is available
- [ ] CI/CD pipeline is configured
- [ ] Monitoring tools are set up
```

### During Refactoring

```markdown
## During Refactoring Checklist

### Process
- [ ] Changes are made in small steps
- [ ] Each step is verified before proceeding
- [ ] Tests are run after each change
- [ ] Changes are committed frequently

### Quality
- [ ] Code follows style guide
- [ ] Code is readable and maintainable
- [ ] Comments explain "why" not "what"
- [ ] No unnecessary complexity added

### Safety
- [ ] Backward compatibility maintained
- [ ] No breaking changes introduced
- [ ] Error handling preserved
- [ ] Security measures intact
```

### After Refactoring

```markdown
## Post-Refactoring Checklist

### Verification
- [ ] All tests pass
- [ ] Manual testing completed
- [ ] Integration verified
- [ ] Performance validated

### Documentation
- [ ] Code comments updated
- [ ] README updated
- [ ] API documentation updated
- [ ] Changelog updated

### Cleanup
- [ ] Dead code removed
- [ ] Unused dependencies removed
- [ ] Temporary files deleted
- [ ] Debug code removed

### Deployment
- [ ] Code reviewed
- [ ] Approved for merge
- [ ] Deployed to staging
- [ ] Monitored for issues
```

## Common Refactoring Scenarios

### Scenario 1: Extracting a Function

**Before:**
```javascript
function processOrder(order) {
  // Calculate tax
  const taxRate = order.state === 'CA' ? 0.08 : 0.05;
  const tax = order.subtotal * taxRate;

  // Calculate discount
  let discount = 0;
  if (order.couponCode) {
    discount = order.subtotal * 0.1;
  }

  // Calculate total
  const total = order.subtotal + tax - discount;

  return { subtotal: order.subtotal, tax, discount, total };
}
```

**Step 1: Extract tax calculation (verify still works)**
```javascript
function calculateTax(subtotal, state) {
  const taxRate = state === 'CA' ? 0.08 : 0.05;
  return subtotal * taxRate;
}

function processOrder(order) {
  const tax = calculateTax(order.subtotal, order.state);

  let discount = 0;
  if (order.couponCode) {
    discount = order.subtotal * 0.1;
  }

  const total = order.subtotal + tax - discount;

  return { subtotal: order.subtotal, tax, discount, total };
}
```

**Step 2: Extract discount calculation (verify still works)**
```javascript
function calculateTax(subtotal, state) {
  const taxRate = state === 'CA' ? 0.08 : 0.05;
  return subtotal * taxRate;
}

function calculateDiscount(subtotal, couponCode) {
  if (!couponCode) return 0;
  return subtotal * 0.1;
}

function processOrder(order) {
  const tax = calculateTax(order.subtotal, order.state);
  const discount = calculateDiscount(order.subtotal, order.couponCode);
  const total = order.subtotal + tax - discount;

  return { subtotal: order.subtotal, tax, discount, total };
}
```

**Step 3: Extract total calculation (verify still works)**
```javascript
function calculateTax(subtotal, state) {
  const taxRate = state === 'CA' ? 0.08 : 0.05;
  return subtotal * taxRate;
}

function calculateDiscount(subtotal, couponCode) {
  if (!couponCode) return 0;
  return subtotal * 0.1;
}

function calculateTotal(subtotal, tax, discount) {
  return subtotal + tax - discount;
}

function processOrder(order) {
  const tax = calculateTax(order.subtotal, order.state);
  const discount = calculateDiscount(order.subtotal, order.couponCode);
  const total = calculateTotal(order.subtotal, tax, discount);

  return { subtotal: order.subtotal, tax, discount, total };
}
```

### Scenario 2: Renaming a Method (Parallel Change)

**Phase 1: Expand**
```javascript
class UserService {
  // Old method (keep working)
  async getUser(id) {
    return database.query('SELECT * FROM users WHERE id = ?', [id]);
  }

  // New method (add, but don't use yet)
  async fetchUser(id) {
    return database.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}
```

**Phase 2: Migrate**
```javascript
// Migrate consumers one at a time
class OrderController {
  // Still using old
  async getOrdersForUser(userId) {
    const user = await userService.getUser(userId);
    // ...
  }
}

class ProfileController {
  // Now using new
  async getProfile(userId) {
    const user = await userService.fetchUser(userId);
    // ...
  }
}
```

**Phase 3: Contract**
```javascript
class UserService {
  // Remove old method
  // async getUser(id) { ... }

  // Only new method remains
  async fetchUser(id) {
    return database.query('SELECT * FROM users WHERE id = ?', [id]);
  }
}
```

### Scenario 3: Changing Data Structure (Strangler Fig)

**Before:**
```javascript
// Old data structure
const user = {
  id: 1,
  name: 'John Doe',
  email: 'john@example.com',
  address: '123 Main St, City, State'
};
```

**Step 1: Add new structure alongside old**
```javascript
// Both structures exist
const user = {
  // Old fields (keep)
  id: 1,
  name: 'John Doe',
  email: 'john@example.com',
  address: '123 Main St, City, State',

  // New fields (add)
  profile: {
    firstName: 'John',
    lastName: 'Doe',
    contact: {
      email: 'john@example.com',
      address: {
        street: '123 Main St',
        city: 'City',
        state: 'State'
      }
    }
  }
};
```

**Step 2: Create migration function**
```javascript
function migrateUserToNewStructure(oldUser) {
  const parts = oldUser.name.split(' ');
  const addressParts = oldUser.address.split(', ');

  return {
    ...oldUser,
    profile: {
      firstName: parts[0],
      lastName: parts[1],
      contact: {
        email: oldUser.email,
        address: {
          street: addressParts[0],
          city: addressParts[1],
          state: addressParts[2]
        }
      }
    }
  };
}
```

**Step 3: Gradually migrate consumers**
```javascript
// Consumer 1: Still using old
function renderUserCard(user) {
  return `<div>${user.name}</div>`;
}

// Consumer 2: Using new
function renderUserProfile(user) {
  return `<div>${user.profile.firstName} ${user.profile.lastName}</div>`;
}
```

**Step 4: Remove old structure**
```javascript
// Final structure
const user = {
  id: 1,
  profile: {
    firstName: 'John',
    lastName: 'Doe',
    contact: {
      email: 'john@example.com',
      address: {
        street: '123 Main St',
        city: 'City',
        state: 'State'
      }
    }
  }
};
```

## Quick Reference

### Pattern Selection

| Situation | Recommended Pattern |
|-----------|---------------------|
| Replacing entire system/module | Strangler Fig |
| Changing API method signature | Parallel Change |
| Migrating data structure | Parallel Change |
| Refactoring internal logic | Small steps + verification |
| Multiple consumers affected | Strangler Fig |
| Single consumer affected | Direct refactoring |

### Verification Commands

```bash
# Run all tests
npm test

# Run specific test suite
npm test -- --grep "UserService"

# Run linting
npm run lint

# Type check (TypeScript)
npm run type-check

# Build
npm run build

# Run verification script
./verify.sh
```

### Rollback Commands

```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert specific commit
git revert <commit-hash>

# Checkout previous version
git checkout HEAD~1 -- <file>

# Reset to specific commit
git reset --hard <commit-hash>
```

### Git Workflow for Refactoring

```bash
# Create feature branch
git checkout -b refactor/user-service

# Make small change
# ... edit code ...

# Verify change
npm test

# Commit if verification passes
git add .
git commit -m "refactor: extract tax calculation"

# Continue with next change
# ... repeat ...

# When complete, create PR
git push origin refactor/user-service
gh pr create --title "Refactor user service" --body "..."
```

## Common Pitfalls

1. **Skipping verification** - Always verify after each change
2. **Making too many changes at once** - Break into small steps
3. **Not having tests** - Write tests before refactoring
4. **Breaking backward compatibility** - Use Parallel Change pattern
5. **No rollback plan** - Always know how to revert
6. **Refactoring without understanding** - Understand before changing
7. **Forgetting to update documentation** - Keep docs in sync
8. **Premature optimization** - Focus on correctness first

## Additional Resources

- [Refactoring Guru](https://refactoring.guru/)
- [Working Effectively with Legacy Code](https://www.amazon.com/Working-Effectively-Legacy-Michael-Feathers/dp/0131177052)
- [Martin Fowler's Refactoring](https://refactoring.com/)
