### **03: Risk Assessment & Mitigation**

> 
> **Current Level:** Expert (Enterprise Scale) 
> 
> 
> **Domain:** Meta Skills / Project Management 
> 

---

### **1. Executive Summary & Strategic Necessity**

* **Context:** ในโลกปี 2025-2026 โครงการพัฒนาซอฟต์แวร์มีความซับซ้อนเพิ่มขึ้นอย่างมาก การประเมินความเสี่ยง (Risk Assessment) เป็นกระบวนการสำคัญที่ช่วยให้ทีมสามารถระบุ ประเมิน และจัดการกับความเสี่ยงที่อาจเกิดขึ้นก่อนที่จะส่งผลกระทบต่อระบบและธุรกิจ
* **Business Impact:** การประเมินความเสี่ยงที่มีประสิทธิภาพช่วย:
  - ลดโอกาสที่อาจเกิดจากการพัฒนาซอฟต์แวร์
  - ลดเวลาที่ใช้ในการแก้ไขปัญหาที่เกิดจากความเสี่ยงที่ไม่ได้ระบุ
  - เพิ่มความมั่นใจในการตัดสินใจลงทุน
  - ลดต้นทุนในการบำรุงรักษาและการฟื้นฟู้ระบบ
  - เพิ่มความเชื่อมั่นใจของลูกค้าและผู้มีส่วนได้ส่วนเสีย
* **Product Thinking:** ทักษะนี้ช่วยแก้ปัญหา (Pain Point) ให้กับ:
  - ทีมพัฒนาที่ต้องการเครื่องมือในการประเมินความเสี่ยง
  - ผู้บริหารที่ต้องการความมั่นใจในการลงทุน
  - ลูกค้าที่ต้องการระบบที่เสถียรและเชื่อถือได้
  - ทีม DevOps ที่ต้องการวางแผนการจัดการเหตุการณ์ฉุกเฉิน

### **2. Technical Deep Dive (The "How-to")**

* **Core Logic:** Risk Assessment เป็นกระบวนการที่ช่วยให้ทีมสามารถ:
  - **Risk Identification:** การระบุความเสี่ยงที่อาจเกิดขึ้น (Technical, Operational, Security, Compliance, Financial)
  - **Risk Analysis:** การวิเคราะห์ความน่าจะเกิด (Probability) และผลกระทบ (Impact)
  - **Risk Prioritization:** การจัดลำดับความเสี่ยงตามความสำคัญ (Risk Matrix)
  - **Risk Mitigation:** การวางแผนการลดความเสี่ยง (Mitigation Strategies)
  - **Risk Monitoring:** การติดตามและตรวจสอบความเสี่ยงอย่างต่อเนื่อง

* **Architecture Diagram Requirements:** แผนผังสถาปัตยกรรมที่ต้องมี:
  - **Risk Matrix Diagram:** แผนผังแสดงความสัมพันธ์ระหว่าง Probability และ Impact
  - **Risk Register Template:** Template สำหรับการบันทึกความเสี่ยง
  - **Mitigation Workflow Diagram:** แผนผังแสดงกระบวนการจัดการความเสี่ยง
  - **Escalation Matrix:** แผนผังแสดงการยกระดับความเสี่ยง
  - **Monitoring Dashboard:** Dashboard สำหรับการติดตามความเสี่ยง

* **Implementation Workflow:**
  1. **Identify Risks:** ระบุความเสี่ยงที่อาจเกิดขึ้น
  2. **Analyze Risks:** วิเคราะห์ Probability และ Impact ของแต่ละความเสี่ยง
  3. **Prioritize Risks:** จัดลำดับความเสี่ยงตามความสำคัญ
  4. **Develop Mitigation Plans:** สร้างแผนการลดความเสี่ยง
  5. **Implement Mitigations:** นำแผนการลดความเสี่ยงไปใช้
  6. **Monitor Risks:** ติดตามและตรวจสอบความเสี่ยงอย่างต่อเนื่อง
  7. **Review and Update:** ทบทวนและอัปเดตแผนการจัดการความเสี่ยง

### **3. Tooling & Tech Stack**

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้:
  - **Risk Management Tools:** Jira, Azure DevOps, Confluence, Risk Register
  - **Project Management Tools:** Asana, Monday.com, Trello, ClickUp
  - **Documentation Platforms:** Confluence, Notion, GitHub Wiki
  - **Collaboration Tools:** Slack, Microsoft Teams, Discord
  - **Monitoring Tools:** Datadog, New Relic, Prometheus, Grafana

* **Configuration Essentials:** ส่วนประกอบสำคัญในการตั้งค่า:
  - **Risk Register Template:** Template มาตรฐานสำหรับการบันทึกความเสี่ยง
  - **Risk Matrix Configuration:** การตั้งค่า Risk Matrix (Probability × Impact)
  - **Escalation Rules:** กฎการยกระดับความเสี่ยง
  - **Notification Settings:** การตั้งค่าการแจ้งเตือน
  - **Integration with CI/CD:** การผนวกเข้ากับ Pipeline

### **4. Standards, Compliance & Security**

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  - **ISO 31000:** Risk Management Principles and Guidelines
  - **ISO/IEC 27001:** Information Security Management
  - **NIST SP 800-30:** Risk Management Guide for Information Technology Systems
  - **COSO ERM:** Committee of Sponsoring Organizations of the Treadway Commission

* **Security Protocol:** กลไกการป้องกัน:
  - **Access Control:** การควบคุมการเข้าถึงข้อมูลความเสี่ยง
  - **Audit Trail:** การบันทึกการเข้าถึงและการแก้ไข
  - **Classification:** การจัดประเภทความเสี่ยงตามความละเอียด
  - **Backup and Recovery:** การสำรองและการกู้คืนข้อมูล

* **Explainability:** ความสามารถในการอธิบาย:
  - **Risk Rationale Documentation:** การบันทึกเหตุผลของการประเมินความเสี่ยง
  - **Impact Analysis:** การวิเคราะห์ผลกระทบอย่างละเอียด
  - **Mitigation Justification:** การอธิบายเหตุผลของแผนการลดความเสี่ยง
  - **Stakeholder Communication:** การสื่อสารกับผู้มีส่วนได้ส่วนเสีย

### **5. Unit Economics & Performance Metrics (KPIs)**

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย (COGS):
  ```
  Total Cost = (Risk Assessment Time × Hourly Rate) + (Mitigation Cost) + (Monitoring Cost)
  
  ROI = (Risk Avoided Cost - Total Cost) / Total Cost × 100%
  
  Risk Avoided Cost = (Incident Cost × Probability) + (Downtime Cost × Probability)
  ```

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  - **Risk Identification Rate:** % ของความเสี่ยงที่ถูกระบุก่อนเกิด (Target: > 90%)
  - **Mitigation Effectiveness:** % ของความเสี่ยงที่ถูกลดอย่างมีประสิทธิภาพ (Target: > 80%)
  - **Incident Reduction Rate:** % ของการลดจำนวนเหตุการณ์ (Target: > 50%)
  - **Risk Review Compliance:** % ของการทบทวนความเสี่ยงตามกำหนด (Target: 100%)
  - **Team Satisfaction:** ความพึงพอใจของทีม (Target: > 4/5)

### **6. Strategic Recommendations (CTO Insights)**

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน:
  1. **Phase 1 (Months 1-2):** สร้าง Template และ Guidelines, ฝึกอบรมทีม
  2. **Phase 2 (Months 3-4):** เริ่มประเมินความเสี่ยงสำหรับโปรเจกต์สำคัญ
  3. **Phase 3 (Months 5-6):** วางแผนและดำเนินการลดความเสี่ยง
  4. **Phase 4 (Year 2+):** ขยายไปยังทุกทีม, สร้าง Culture ของการจัดการความเสี่ยง

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาด:
  - **Over-conservatism:** หลีกเลี่ยงการประเมินความเสี่ยงเกินไป
  - **Ignoring Low-Probability Risks:** ต้องพิจารณาความเสี่ยงที่มี Probability ต่ำแต่ Impact สูง
  - **Not Updating Risk Register:** ต้องอัปเดต Risk Register อย่างต่อเนื่อง
  - **Poor Communication:** ต้องสื่อสารความเสี่ยงกับผู้มีส่วนได้ส่วนเสียอย่างชัดเจน
  - **No Monitoring:** ต้องติดตามความเสี่ยงอย่างต่อเนื่อง
  - **Ignoring Mitigation:** ต้องดำเนินการ Mitigation Plans อย่างจริงจัง

---

## Overview

Risk assessment is the systematic process of identifying, analyzing, and evaluating potential risks that could affect project success, system stability, or business operations. This skill provides frameworks and methodologies for effective risk management in software development and IT projects.

**When to use this skill:** When starting new projects, making architectural decisions, implementing significant changes, or conducting periodic reviews of existing systems.

## Risk Categories

### 1. Technical Risks

**Definition:** Risks related to technology choices, implementation challenges, and system capabilities

**Examples:**
- Technology not mature enough for requirements
- Performance limitations of chosen architecture
- Integration complexity with existing systems
- Scalability concerns
- Technical debt accumulation

**Assessment Factors:**
- Technology maturity and community support
- Team expertise with chosen technologies
- Proof of concept results
- Benchmark data and performance metrics

### 2. Operational Risks

**Definition:** Risks related to day-to-day operations, maintenance, and support

**Examples:**
- Insufficient monitoring and alerting
- Lack of disaster recovery plans
- Inadequate backup strategies
- Staffing and skill gaps
- Process and procedure gaps

**Assessment Factors:**
- Operational maturity of systems
- Team size and expertise
- Documentation quality
- Historical incident data

### 3. Security Risks

**Definition:** Risks related to data protection, access control, and compliance

**Examples:**
- Data breaches and unauthorized access
- Insufficient encryption
- Vulnerabilities in third-party dependencies
- Non-compliance with regulations (GDPR, HIPAA)
- Social engineering attacks

**Assessment Factors:**
- Security audit results
- Vulnerability scan findings
- Compliance requirements
- Industry security standards

### 4. Compliance Risks

**Definition:** Risks related to regulatory and legal requirements

**Examples:**
- GDPR non-compliance
- Industry-specific regulations (HIPAA, PCI DSS)
- Data residency requirements
- Licensing issues
- Intellectual property concerns

**Assessment Factors:**
- Regulatory requirements analysis
- Legal review findings
- Industry best practices
- Geographic considerations

### 5. Financial Risks

**Definition:** Risks related to budget, cost overruns, and financial impact

**Examples:**
- Budget overruns
- Unexpected infrastructure costs
- Vendor lock-in costs
- Currency fluctuations
- Revenue impact from downtime

**Assessment Factors:**
- Budget analysis
- Cost estimation accuracy
- Vendor contract terms
- Historical cost data

## Risk Assessment Framework

### Risk Matrix

```
                Impact
                │  Low  │ Medium │ High  │ Critical
────────────────┼────────┼────────┼────────┼──────────
Probability     │        │        │        │
────────────────┼────────┼────────┼────────┼──────────
High            │  Low   │ Medium │ High   │ Critical
────────────────┼────────┼────────┼────────┼──────────
Medium          │  Low   │ Medium │ High   │ Critical
────────────────┼────────┼────────┼────────┼──────────
Low             │  Low   │ Low    │ Medium │ High
────────────────┼────────┼────────┼────────┼──────────
Very Low        │  Low   │ Low    │ Low    │ Medium
```

### Risk Scoring

```
Risk Score = Probability × Impact

Where:
- Probability: 1 (Very Low) to 5 (Very High)
- Impact: 1 (Low) to 5 (Critical)

Risk Levels:
- 1-4: Low Risk
- 5-9: Medium Risk
- 10-15: High Risk
- 16-25: Critical Risk
```

## Risk Register Template

```markdown
# Risk Register: [Project Name]

| ID | Risk | Category | Probability | Impact | Risk Score | Mitigation Strategy | Owner | Status | Review Date |
|----|------|----------|-------------|---------|-------------|--------|--------|------------|
| R001 | Database scaling issues | Technical | 4 | 4 | 16 | Implement read replicas + caching | DB Team | In Progress | 2024-02-01 |
| R002 | Security vulnerability in auth | Security | 3 | 5 | 15 | Conduct security audit | Security Team | Open | 2024-02-01 |
| R003 | Budget overrun for cloud costs | Financial | 4 | 3 | 12 | Implement cost monitoring | Finance | Open | 2024-02-01 |
```

## Mitigation Strategies

### 1. Avoid

**Definition:** Change plans to eliminate the risk entirely

**When to use:**
- Risk is unacceptable
- Alternative approaches available
- Cost of avoidance is reasonable

**Example:**
```
Risk: Chosen database doesn't scale to required load
Mitigation: Choose a different database with proven scalability
```

### 2. Transfer

**Definition:** Shift risk to another party

**When to use:**
- Third party can handle risk better
- Insurance available
- Cost of transfer is reasonable

**Example:**
```
Risk: Data center outage
Mitigation: Use managed cloud provider with SLA guarantees
```

### 3. Mitigate

**Definition:** Reduce probability or impact of risk

**When to use:**
- Risk cannot be avoided or transferred
- Mitigation actions are feasible
- Cost is justified

**Example:**
```
Risk: Security breach
Mitigation: Implement multi-factor authentication, encryption, and monitoring
```

### 4. Accept

**Definition:** Acknowledge risk and prepare contingency plans

**When to use:**
- Risk is low impact
- Mitigation cost exceeds potential loss
- Risk is inherent to business

**Example:**
```
Risk: Minor performance degradation during peak load
Mitigation: Accept and have communication plan ready
```

## Risk Assessment Process

### Step 1: Risk Identification

**Methods:**
- Brainstorming sessions with team
- Historical data analysis
- Expert interviews
- Checklists and templates
- SWOT analysis

**Tools:**
- Risk identification workshops
- Historical incident review
- Technology assessment
- Compliance requirements analysis

### Step 2: Risk Analysis

**Assessment Criteria:**

| Criteria | Description |
|-----------|-------------|
| **Probability** | Likelihood of risk occurring (1-5 scale) |
| **Impact** | Severity of consequences (1-5 scale) |
| **Timeframe** | When risk might materialize |
| **Dependencies** | Related risks or dependencies |

### Step 3: Risk Prioritization

**Prioritization Matrix:**

```
Priority = Risk Score × Strategic Importance

Where:
- Risk Score = Probability × Impact
- Strategic Importance = 1 (Low) to 3 (High)
```

### Step 4: Mitigation Planning

**Mitigation Plan Template:**

```markdown
## Risk: [Risk Description]

### Risk Details
- **ID:** RXXX
- **Category:** [Technical/Operational/Security/Compliance/Financial]
- **Probability:** [1-5]
- **Impact:** [1-5]
- **Risk Score:** [1-25]

### Mitigation Strategy
- **Approach:** [Avoid/Transfer/Mitigate/Accept]
- **Actions:**
  - [ ] Action 1
  - [ ] Action 2
  - [ ] Action 3
- **Owner:** [Name]
- **Timeline:** [Start Date - End Date]
- **Cost:** [Estimated Cost]

### Contingency Plan
- **Trigger:** [What triggers contingency]
- **Actions:** [What to do if risk materializes]
- **Owner:** [Name]
- **Communication:** [Who to notify]

### Success Criteria
- [ ] [Criteria 1]
- [ ] [Criteria 2]
- [ ] [Criteria 3]
```

### Step 5: Risk Monitoring

**Monitoring Activities:**

```markdown
## Risk Monitoring Checklist

### Regular Reviews
- [ ] Weekly risk review meetings
- [ ] Monthly risk register updates
- [ ] Quarterly risk assessment refresh

### Trigger Events
- [ ] Project milestone reviews
- [ ] Architecture changes
- [ ] Team changes
- [ ] Incident post-mortems

### KPIs to Track
- [ ] Number of risks materialized
- [ ] Mitigation effectiveness
- [ ] Cost of risk events
- [ ] Time to respond to risks
```

## Risk Communication

### Stakeholder Communication Plan

```markdown
## Risk Communication Plan

### Communication Matrix

| Stakeholder | Frequency | Format | Content |
|-------------|-------------|---------|----------|
| Executive Team | Monthly | Executive Summary | High-level risks and mitigation status |
| Project Team | Weekly | Detailed Report | All risks, status, and action items |
| Customers | As Needed | Public Notice | Risks affecting service delivery |
| Regulators | Quarterly | Compliance Report | Compliance-related risks |

### Escalation Criteria

| Risk Level | Escalation Path | Response Time |
|------------|------------------|---------------|
| Low | Project Manager | 1 week |
| Medium | Project Manager + Tech Lead | 3 days |
| High | Project Manager + Tech Lead + Director | 24 hours |
| Critical | Executive Team + All Stakeholders | Immediate |
```

## Risk Assessment Examples

### Example 1: Database Scaling Risk

```markdown
## Risk: Database Performance Under Load

### Risk Details
- **ID:** R001
- **Category:** Technical
- **Probability:** 4 (High)
- **Impact:** 4 (High)
- **Risk Score:** 16 (Critical)

### Context
System expects 100K concurrent users during peak hours. Current PostgreSQL setup may not handle write load.

### Mitigation Strategy
- **Approach:** Mitigate
- **Actions:**
  - [ ] Implement read replicas (Week 1-2)
  - [ ] Add caching layer (Week 2-3)
  - [ ] Optimize database queries (Week 3-4)
  - [ ] Load test with 150K users (Week 4)
  - [ ] Plan sharding strategy for future (Week 4)
- **Owner:** Database Team
- **Timeline:** 2024-02-01 - 2024-02-28
- **Cost:** $50,000 (infrastructure + engineering)

### Contingency Plan
- **Trigger:** Database CPU > 80% during peak
- **Actions:** 
  - Scale up database instances immediately
  - Enable read-only mode for non-critical features
  - Notify users of degraded performance
- **Owner:** DevOps Team
- **Communication:** Notify Project Manager, CTO, and Customer Support

### Success Criteria
- [ ] Database handles 150K concurrent users in load test
- [ ] CPU usage remains below 70% at 100K users
- [ ] Query response time < 100ms P95
```

### Example 2: Security Vulnerability Risk

```markdown
## Risk: Authentication System Vulnerability

### Risk Details
- **ID:** R002
- **Category:** Security
- **Probability:** 3 (Medium)
- **Impact:** 5 (Critical)
- **Risk Score:** 15 (High)

### Context
Current authentication system uses outdated encryption and lacks MFA. Security audit identified potential vulnerabilities.

### Mitigation Strategy
- **Approach:** Mitigate
- **Actions:**
  - [ ] Conduct full security audit (Week 1)
  - [ ] Implement MFA (Week 2-3)
  - [ ] Upgrade encryption algorithms (Week 3-4)
  - [ ] Add rate limiting (Week 4)
  - [ ] Implement session timeout (Week 4)
  - [ ] Update security policies (Week 4)
- **Owner:** Security Team
- **Timeline:** 2024-02-01 - 2024-02-28
- **Cost:** $75,000 (engineering + tools)

### Contingency Plan
- **Trigger:** Security breach detected
- **Actions:**
  - Immediately disable affected systems
  - Notify security team and legal
  - Activate incident response plan
  - Communicate with affected users
- **Owner:** CISO + Legal Team
- **Communication:** Notify Executive Team, Legal, PR, and Customers

### Success Criteria
- [ ] Security audit passes with no critical findings
- [ ] MFA implemented for all users
- [ ] Encryption upgraded to industry standards
- [ ] Rate limiting prevents brute force attacks
```

## Best Practices

1. **Be Proactive** - Identify risks before they materialize
2. **Be Realistic** - Don't underestimate probability or impact
3. **Involve the Team** - Get input from all stakeholders
4. **Document Everything** - Keep detailed risk register
5. **Review Regularly** - Update risk assessments frequently
6. **Communicate Clearly** - Keep stakeholders informed
7. **Learn from Incidents** - Use post-mortems to improve risk assessment
8. **Balance Cost vs. Risk** - Don't overspend on low-impact risks
9. **Use Standard Frameworks** - Follow industry best practices
10. **Plan for Contingencies** - Always have backup plans

## Resources

- [ISO 31000 Risk Management](https://www.iso.org/standard/31000)
- [NIST Risk Management Guide](https://csrc.nist.gov/publications/detail/sp/800-30)
- [OWASP Risk Assessment](https://owasp.org/www-community/risk_assessment)
- [PMI Risk Management](https://www.pmi.org/about/learn-about-pmi/what-is-project-management/risk-management)
