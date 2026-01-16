---
name: Security Questionnaires
description: Comprehensive guide to handling enterprise security questionnaires, building standard response libraries, and streamlining the vendor assessment process
---

# Security Questionnaires

## What are Security Questionnaires?

**Definition:** Long surveys (100-500 questions) from enterprise customers to assess vendor security practices.

### Typical Questions

```
- Do you encrypt data at rest?
- Where is data stored?
- Do you support SSO?
- Have you had any security breaches?
- Do you have SOC2 certification?
- What's your incident response process?
- Who has access to production data?
- Do you perform penetration testing?
```

### Example Questionnaire Structure

```
Section 1: Company Information (10 questions)
Section 2: Data Security (50 questions)
Section 3: Infrastructure (40 questions)
Section 4: Compliance (30 questions)
Section 5: Incident Response (20 questions)
Section 6: Access Management (30 questions)
Section 7: Development Practices (20 questions)
Section 8: Third-Party Vendors (15 questions)
Section 9: Physical Security (10 questions)
Section 10: HR Practices (15 questions)

Total: 240 questions
```

---

## Why They Matter

### 1. Blocker for Enterprise Sales

**Sales Cycle:**
```
1. Demo (Week 1)
2. POC (Weeks 2-4)
3. Security review (Weeks 5-8) ← Questionnaire here
4. Legal review (Weeks 9-12)
5. Procurement (Weeks 13-16)
6. Close deal (Week 16)
```

**If questionnaire fails:** Deal dies

### 2. Repeated for Every Large Customer

**Problem:**
```
Customer A sends questionnaire (200 questions)
Customer B sends questionnaire (250 questions, 80% same)
Customer C sends questionnaire (180 questions, 75% same)

Total time: 60-120 hours
```

### 3. Time-Consuming

**First Time:**
- 20-40 hours (no standard responses)
- Involves multiple teams (engineering, security, legal)

**With Standard Library:**
- 5-10 hours (copy/paste from library)
- Minimal team involvement

---

## Common Questionnaire Types

### Standard Questionnaires

**CAIQ (Consensus Assessments Initiative Questionnaire):**
- Cloud Security Alliance (CSA)
- 295 questions
- Cloud security focused

**SIG (Standardized Information Gathering):**
- Shared Assessments
- 400+ questions
- Financial services focused

**VSAQ (Vendor Security Assessment Questionnaire):**
- Google
- Open source
- Customizable

### Custom Questionnaires

**Characteristics:**
- Each customer's own format
- Excel, Word, or online form
- 100-500 questions
- 70-80% overlap with standard questions

### Self-Assessments

**SOC2 Type II:**
- Audit report (not questionnaire)
- Answers many questions
- Required by most enterprises

**ISO 27001:**
- Certification
- Information security management
- International standard

---

## Topics Covered

### 1. Company Info (10-20 questions)

**Questions:**
- Company name, address, website
- Number of employees
- Year founded
- Ownership structure (public, private, VC-backed)
- Primary business location
- Annual revenue (optional)

**Example Answers:**
```
Company: Acme Inc.
Employees: 50
Founded: 2020
Ownership: Private (VC-backed)
Location: San Francisco, CA
```

### 2. Data Security (40-60 questions)

**Questions:**
- Do you encrypt data at rest? (Algorithm?)
- Do you encrypt data in transit? (TLS version?)
- Where is data stored? (Region, datacenter)
- Do you support data residency? (EU, US, etc.)
- How is data backed up?
- What's your data retention policy?
- Do you support data deletion?

**Example Answers:**
```
Encryption at rest: Yes, AES-256
Encryption in transit: Yes, TLS 1.2+
Data location: AWS us-east-1 and us-west-2
Data residency: Yes, EU customers can choose EU region
Backups: Daily, retained for 30 days
Retention: Deleted 90 days after account closure
Deletion: Yes, via API or UI
```

### 3. Infrastructure (30-50 questions)

**Questions:**
- Cloud provider? (AWS, Azure, GCP)
- Do you own datacenters?
- What's your disaster recovery plan?
- What's your RTO (Recovery Time Objective)?
- What's your RPO (Recovery Point Objective)?
- Do you have redundancy?
- Do you perform DR drills?

**Example Answers:**
```
Cloud provider: AWS
Own datacenters: No
DR plan: Yes, documented and tested quarterly
RTO: 4 hours
RPO: 1 hour
Redundancy: Multi-AZ deployment
DR drills: Quarterly
```

### 4. Compliance (20-40 questions)

**Questions:**
- Do you have SOC2 Type II?
- Do you have ISO 27001?
- Are you GDPR compliant?
- Are you HIPAA compliant?
- Do you have PCI DSS certification?
- Do you have a privacy policy?
- Do you have a DPA (Data Processing Agreement)?

**Example Answers:**
```
SOC2 Type II: Yes (report available)
ISO 27001: In progress (expected Q3 2024)
GDPR: Yes, compliant
HIPAA: Yes, BAA available
PCI DSS: N/A (we don't process payments)
Privacy policy: Yes (link)
DPA: Yes (standard template available)
```

### 5. Incident Response (15-25 questions)

**Questions:**
- Do you have an incident response plan?
- Who is responsible for incident response?
- How do you detect incidents?
- What's your incident notification process?
- Have you had any security breaches?
- How do you communicate incidents to customers?

**Example Answers:**
```
IR plan: Yes, documented and tested
Responsible: Security team + on-call engineer
Detection: SIEM, IDS, monitoring alerts
Notification: Within 72 hours (GDPR requirement)
Breaches: No breaches in last 3 years
Communication: Email + status page
```

### 6. Access Management (25-35 questions)

**Questions:**
- Do you support SSO?
- Do you support SAML?
- Do you support OIDC?
- Do you support SCIM?
- Do you enforce MFA?
- Do you have RBAC?
- Who has access to production data?
- Do you log access attempts?

**Example Answers:**
```
SSO: Yes
SAML: Yes (SAML 2.0)
OIDC: Yes
SCIM: Yes (SCIM 2.0)
MFA: Yes, enforced for all users
RBAC: Yes (Admin, Manager, Member, Viewer)
Production access: Limited to 5 senior engineers
Access logs: Yes, retained for 1 year
```

### 7. Development Practices (15-25 questions)

**Questions:**
- Do you perform code reviews?
- Do you have automated testing?
- What's your test coverage?
- Do you use CI/CD?
- Do you perform security scans?
- Do you use dependency scanning?
- Do you have a bug bounty program?

**Example Answers:**
```
Code reviews: Yes, required for all changes
Automated testing: Yes (unit, integration, e2e)
Test coverage: >80%
CI/CD: Yes (GitHub Actions)
Security scans: Yes (SonarQube, Snyk)
Dependency scanning: Yes (Dependabot)
Bug bounty: Yes (HackerOne)
```

### 8. Third-Party Vendors (10-20 questions)

**Questions:**
- Do you use third-party vendors?
- List of subprocessors
- Do you vet vendors?
- Do you have vendor contracts?
- Do you monitor vendor security?

**Example Answers:**
```
Third-party vendors: Yes
Subprocessors:
  - AWS (infrastructure)
  - Stripe (payments)
  - SendGrid (email)
  - Datadog (monitoring)
Vendor vetting: Yes, security review before onboarding
Contracts: Yes, DPAs with all vendors
Monitoring: Annual security reviews
```

### 9. Physical Security (5-15 questions)

**Questions:**
- Do you own datacenters?
- Physical access controls?
- Video surveillance?
- Visitor logs?

**Example Answers:**
```
Own datacenters: No (cloud-hosted on AWS)
Physical access: N/A (AWS responsibility)
Surveillance: N/A (AWS responsibility)
Visitor logs: N/A (AWS responsibility)

Note: See AWS SOC2 report for datacenter security
```

### 10. HR Practices (10-20 questions)

**Questions:**
- Do you perform background checks?
- Do you have security training?
- Do you have acceptable use policy?
- Do you have NDA with employees?
- What happens when employee leaves?

**Example Answers:**
```
Background checks: Yes, for all employees
Security training: Yes, annual training required
Acceptable use policy: Yes, signed by all employees
NDA: Yes, signed on day 1
Offboarding: Access revoked within 1 hour
```

---

## Preparing for Questionnaires

### 1. Security Documentation

**Essential Documents:**
```
- Security policy
- Privacy policy
- Incident response plan
- Disaster recovery plan
- Business continuity plan
- Acceptable use policy
- Data retention policy
- Vendor management policy
```

**Where to Store:** Shared drive (Google Drive, Confluence)

### 2. Compliance Certifications

**Must-Have (for enterprise):**
- SOC2 Type II (annual audit)
- GDPR compliance documentation

**Nice-to-Have:**
- ISO 27001 certification
- HIPAA compliance (if healthcare)
- PCI DSS (if processing payments)

**Cost:**
- SOC2: $15k-50k (first year)
- ISO 27001: $20k-100k

### 3. Standard Responses Library

**Format:** Google Doc or Notion page

**Structure:**
```
# Standard Security Questionnaire Responses

## Company Information
Q: Company name
A: Acme Inc.

Q: Number of employees
A: 50

## Data Security
Q: Do you encrypt data at rest?
A: Yes, we encrypt all data at rest using AES-256 encryption.

Q: Where is data stored?
A: Data is stored in AWS data centers in us-east-1 (Virginia) and us-west-2 (Oregon). EU customers can opt for eu-west-1 (Ireland).

## Infrastructure
Q: What's your disaster recovery plan?
A: We have a documented disaster recovery plan that is tested quarterly. Our RTO is 4 hours and RPO is 1 hour. We use multi-AZ deployment for redundancy.

[... 200+ more questions]
```

### 4. Evidence Files

**Collect:**
```
- SOC2 Type II report (PDF)
- ISO 27001 certificate (PDF)
- Penetration test results (PDF, redacted)
- Encryption certificates
- DR test results
- Incident response plan (PDF)
- Security training certificates
- Vendor list (Excel)
```

**Where to Store:** Secure shared drive (encrypted, access-controlled)

---

## Standard Responses Library

### Example Questions and Answers

**Data Encryption:**
```
Q: Do you encrypt data at rest?
A: Yes, all data at rest is encrypted using AES-256 encryption. Database encryption is managed by AWS RDS with encryption keys stored in AWS KMS.

Q: Do you encrypt data in transit?
A: Yes, all data in transit is encrypted using TLS 1.2 or higher. We enforce HTTPS for all web traffic and use TLS for all API communications.
```

**Data Location:**
```
Q: Where is customer data stored?
A: Customer data is stored in AWS data centers. By default, US customers' data is stored in us-east-1 (Virginia) and us-west-2 (Oregon). EU customers can opt for data residency in eu-west-1 (Ireland) to comply with GDPR requirements.

Q: Do you support data residency?
A: Yes, we support data residency for EU customers. Data can be stored exclusively in EU regions (eu-west-1) upon request.
```

**SSO:**
```
Q: Do you support Single Sign-On (SSO)?
A: Yes, we support SSO via SAML 2.0 and OpenID Connect (OIDC). We integrate with major identity providers including Okta, Azure AD, Google Workspace, and OneLogin.

Q: Do you support SCIM provisioning?
A: Yes, we support SCIM 2.0 for automated user provisioning and deprovisioning. This allows IT administrators to manage user accounts centrally from their identity provider.
```

**Security Breaches:**
```
Q: Have you experienced any security breaches in the last 3 years?
A: No, we have not experienced any security breaches in the last 3 years. We maintain a comprehensive security program including regular penetration testing, security monitoring, and incident response procedures.

Q: If you had a breach, how would you notify us?
A: In the event of a security incident affecting customer data, we would notify affected customers within 72 hours via email and through our status page. We would provide details of the incident, affected data, and remediation steps.
```

**Compliance:**
```
Q: Do you have SOC2 Type II certification?
A: Yes, we complete an annual SOC2 Type II audit. Our most recent report is dated [DATE] and is available upon request under NDA.

Q: Are you GDPR compliant?
A: Yes, we are GDPR compliant. We have implemented appropriate technical and organizational measures to protect personal data, including data encryption, access controls, and data processing agreements. We support data subject rights including access, deletion, and portability.
```

**Access Control:**
```
Q: Who has access to production data?
A: Access to production data is restricted to a limited number of senior engineers (currently 5) who require access for operational purposes. All access is logged and reviewed monthly. Access is granted based on the principle of least privilege.

Q: Do you enforce multi-factor authentication (MFA)?
A: Yes, MFA is enforced for all user accounts, including employees and customers. We support authenticator apps (TOTP) and hardware tokens (WebAuthn/U2F).
```

**Disaster Recovery:**
```
Q: What is your Recovery Time Objective (RTO)?
A: Our RTO is 4 hours. This means we can restore service within 4 hours of a disaster.

Q: What is your Recovery Point Objective (RPO)?
A: Our RPO is 1 hour. This means we can recover data to within 1 hour of a disaster. We perform continuous backups with point-in-time recovery.

Q: Do you test your disaster recovery plan?
A: Yes, we test our disaster recovery plan quarterly. Tests include failover to backup systems, data restoration, and communication procedures. Results are documented and reviewed.
```

---

## Evidence Collection

### SOC2 Report

**What:** Independent audit of security controls

**Frequency:** Annual

**Cost:** $15k-50k (first year), $10k-30k (renewal)

**How to Get:**
1. Hire SOC2 auditor (Deloitte, PwC, Vanta, Drata)
2. Implement required controls
3. Operate controls for 3-12 months
4. Auditor reviews and tests controls
5. Receive SOC2 Type II report

**Sharing:** Under NDA only

### ISO 27001 Certificate

**What:** International standard for information security

**Frequency:** 3-year certification, annual surveillance audits

**Cost:** $20k-100k

**How to Get:**
1. Implement ISO 27001 controls
2. Hire certification body
3. Pass certification audit
4. Receive certificate

**Sharing:** Public (can display logo)

### Penetration Test Results

**What:** External security testing

**Frequency:** Annual (minimum)

**Cost:** $10k-50k

**How to Get:**
1. Hire penetration testing firm
2. Define scope (web app, API, infrastructure)
3. Testers attempt to find vulnerabilities
4. Receive report with findings
5. Remediate vulnerabilities
6. Re-test to verify fixes

**Sharing:** Redacted version (hide specific vulnerabilities)

### Disaster Recovery Test Results

**What:** Proof that DR plan works

**Frequency:** Quarterly

**How to Document:**
```
Disaster Recovery Test Report

Date: 2024-01-15
Test Type: Full failover
Duration: 3 hours

Scenario: Primary datacenter failure

Steps:
1. Simulated primary datacenter outage (10:00 AM)
2. Triggered failover to backup datacenter (10:05 AM)
3. Verified all services running (10:30 AM)
4. Tested application functionality (10:30-11:00 AM)
5. Verified data integrity (11:00-11:30 AM)
6. Restored primary datacenter (11:30 AM-1:00 PM)

Results:
- RTO: 30 minutes (target: 4 hours) ✅
- RPO: 0 minutes (target: 1 hour) ✅
- All services restored successfully ✅
- No data loss ✅

Lessons Learned:
- Failover automation worked well
- Communication to team was clear
- Documentation was up-to-date
```

---

## Tools for Questionnaires

### Whistic (Questionnaire Automation)

**Features:**
- Pre-filled questionnaire responses
- Share with multiple customers
- Track questionnaire status
- Integrations (Salesforce, HubSpot)

**Pricing:** $10k-50k/year

### SafeBase (Security Portal)

**Features:**
- Public security documentation
- Self-service questionnaires
- Trust center (SOC2, ISO, policies)
- Analytics (who viewed what)

**Pricing:** $5k-20k/year

### Vanta (Compliance + Questionnaires)

**Features:**
- SOC2 automation
- Questionnaire automation
- Trust center
- Continuous monitoring

**Pricing:** $20k-50k/year

### Drata (Similar to Vanta)

**Features:**
- SOC2, ISO 27001 automation
- Questionnaire automation
- Trust center

**Pricing:** $20k-50k/year

### Manual (Google Docs/Sheets)

**When to Use:** Early stage, <10 questionnaires/year

**Process:**
1. Create Google Doc with standard responses
2. Copy/paste into customer's questionnaire
3. Customize as needed

**Cost:** Free

---

## Streamlining the Process

### 1. Trust Center (Public Security Documentation)

**What:** Public website with security information

**Contents:**
- Security overview
- Compliance certifications (SOC2, ISO)
- Privacy policy
- Data Processing Agreement (DPA)
- Subprocessor list
- Security whitepaper

**Example:** https://trust.example.com

**Benefits:**
- Customers can self-serve
- Reduces questionnaire volume
- Builds trust

### 2. Self-Service Security Portal

**What:** Portal where customers can access security docs

**Features:**
- Download SOC2 report (under NDA)
- Download ISO certificate
- Download penetration test results
- Submit security questions

**Tools:** SafeBase, Whistic, Vanta

### 3. Standard Questionnaire (Accept Yours Instead)

**Strategy:** "We've completed a comprehensive security questionnaire. Can you accept ours instead?"

**Your Questionnaire:**
- 200 questions covering all common topics
- Pre-filled with your answers
- Includes evidence (SOC2, ISO)

**Success Rate:** 30-50% (some customers will accept)

### 4. Pre-Filled Responses (Share Library)

**Strategy:** Share your standard response library

**Format:**
- Google Doc (view-only)
- PDF
- Excel

**Instructions:** "Here are our standard responses. Please copy relevant answers into your questionnaire."

---

## Common Challenging Questions

### "Have you had any security breaches?"

**Bad Answer:**
```
"No" (if you have)
"Yes" (with no context)
```

**Good Answer:**
```
"We have not experienced any security breaches in the last 3 years. We maintain a comprehensive security program including:
- Regular penetration testing (annual)
- Security monitoring and alerting (24/7)
- Incident response plan (tested quarterly)
- Bug bounty program (HackerOne)

In [YEAR], we had a minor incident where [BRIEF DESCRIPTION]. We immediately:
1. Contained the incident
2. Notified affected customers within 72 hours
3. Conducted a thorough investigation
4. Implemented additional controls to prevent recurrence
5. Published a postmortem

No customer data was compromised."
```

**Key:** Honesty + mitigation

### "Do you have cyber insurance?"

**Why They Ask:** Risk transfer (if you get breached, insurance pays)

**Answer:**
```
"Yes, we maintain cyber liability insurance with coverage of $[AMOUNT]M. Our policy covers:
- Data breach response costs
- Legal fees
- Regulatory fines
- Customer notification
- Credit monitoring services
- Business interruption

Policy provider: [INSURANCE COMPANY]
Policy number: Available upon request
```

**If No:**
```
"We are currently evaluating cyber insurance options and plan to obtain coverage by [DATE]."
```

**Recommendation:** Get cyber insurance ($1M-5M coverage, $5k-20k/year)

### "What's your RTO/RPO?"

**RTO (Recovery Time Objective):** How long to restore service
**RPO (Recovery Point Objective):** How much data loss is acceptable

**Bad Answer:**
```
"We don't know"
"N/A"
```

**Good Answer:**
```
"Our disaster recovery plan defines:
- RTO: 4 hours (service restored within 4 hours)
- RPO: 1 hour (data recovered to within 1 hour of incident)

We achieve this through:
- Multi-AZ deployment (automatic failover)
- Continuous backups (every 5 minutes)
- Point-in-time recovery
- Quarterly DR testing

Most recent DR test: [DATE]
Actual RTO achieved: 30 minutes
Actual RPO achieved: 0 minutes (no data loss)"
```

**Recommendation:** Have a DR plan with defined RTO/RPO

### "Who has access to production data?"

**Bad Answer:**
```
"All engineers" (too broad)
"We don't track this" (red flag)
```

**Good Answer:**
```
"Access to production data is restricted based on the principle of least privilege:

Production Database Access:
- 5 senior engineers (for operational support)
- Access is granted via time-limited tokens (4 hours)
- All access is logged and reviewed monthly

Production Server Access:
- 3 SRE team members (for deployments and troubleshooting)
- Access via bastion host with MFA
- All commands logged

Customer Data Access:
- Customer support can view customer data only with customer permission
- Access is logged and audited

Access Reviews:
- Quarterly review of all production access
- Access automatically revoked after 90 days of inactivity
- Immediate revocation upon employee departure"
```

---

## Red Flags to Avoid

### "We don't know"

**Problem:** Looks unprepared, raises concerns

**Better:**
```
"We don't currently track this metric, but we will implement tracking by [DATE] and provide an update."
```

### "N/A" without explanation

**Problem:** Unclear why it's not applicable

**Better:**
```
"N/A - We use AWS for infrastructure, so physical datacenter security is AWS's responsibility. See AWS SOC2 report for details."
```

### Inconsistent answers

**Problem:** Same question answered differently

**Example:**
```
Question 50: "Do you encrypt data at rest?" → "Yes, AES-256"
Question 120: "What encryption do you use?" → "We don't encrypt data"
```

**Solution:** Use standard response library (consistent answers)

### Missing evidence

**Problem:** Claim without proof

**Example:**
```
"We have SOC2" (but can't provide report)
```

**Solution:** Have evidence ready (SOC2 report, certificates, test results)

### Outdated documentation

**Problem:** Documentation is 2 years old

**Example:**
```
"See our security policy" (dated 2022, mentions old systems)
```

**Solution:** Review and update documentation annually

---

## Questionnaire Workflow

### 1. Customer Sends Questionnaire

**Formats:**
- Excel spreadsheet
- Word document
- Online form (Google Forms, Typeform)
- Vendor portal (Whistic, SafeBase)

### 2. Assign Sections to Team Members

**Assignments:**
```
Company Info → Sales team
Data Security → Security team
Infrastructure → Engineering team
Compliance → Legal team
HR Practices → HR team
```

### 3. Fill Out Answers with Evidence

**Process:**
1. Copy from standard response library
2. Customize for this customer
3. Attach evidence (SOC2, certificates)
4. Flag questions that need research

### 4. Internal Review

**Reviewers:**
- Security team (technical accuracy)
- Legal team (compliance, contracts)
- Sales team (customer context)

### 5. Submit to Customer

**Submission:**
- Return completed questionnaire
- Include evidence files
- Cover letter summarizing security posture

### 6. Follow-Up Calls/Clarifications

**Common Follow-Ups:**
- "Can you explain your encryption in more detail?"
- "Can you provide your SOC2 report?"
- "Can you provide references?"

### 7. Approval (Hopefully!)

**Timeline:**
- Customer reviews: 1-2 weeks
- Follow-up questions: 1-2 rounds
- Final approval: 1 week

**Total:** 3-5 weeks

---

## Maintaining Questionnaire Readiness

### Keep Security Documentation Updated

**Schedule:**
```
Quarterly:
- Review and update security policies
- Update vendor list
- Update employee count, company info

Annually:
- Renew SOC2 (audit)
- Penetration testing
- DR testing
- Security training
```

### Renew Certifications

**SOC2:**
- Annual audit
- Cost: $10k-30k (renewal)
- Timeline: 2-3 months

**ISO 27001:**
- Annual surveillance audit
- 3-year recertification
- Cost: $5k-20k (surveillance), $20k-50k (recertification)

### Regular Penetration Tests

**Frequency:** Annual (minimum)

**Process:**
1. Hire pen testing firm (Q1)
2. Conduct test (Q2)
3. Remediate findings (Q2-Q3)
4. Re-test (Q3)
5. Update questionnaire responses (Q4)

### Incident Response Drills

**Frequency:** Quarterly

**Process:**
1. Simulate incident (e.g., data breach)
2. Execute incident response plan
3. Document results
4. Update plan based on learnings

### Update Standard Responses Library

**Triggers:**
- New certification (SOC2, ISO)
- Infrastructure changes (new cloud provider)
- Policy changes (new data retention policy)
- Incident (update breach history)

**Process:**
1. Update response in library
2. Notify team
3. Update any pending questionnaires

---

## Delegating Questionnaire Completion

### Sales Team

**Sections:**
- Company information
- Business model
- Customer references

**Why:** They know the business best

### Engineering Team

**Sections:**
- Infrastructure
- Development practices
- Technical security controls

**Why:** They built the system

### Security Team

**Sections:**
- Security controls
- Incident response
- Access management
- Compliance

**Why:** They own security

### Legal Team

**Sections:**
- Contracts
- Privacy policy
- Data Processing Agreement
- Regulatory compliance

**Why:** They handle legal matters

### Finance Team

**Sections:**
- Insurance
- Certifications (cost/budget)
- Vendor contracts

**Why:** They manage budget and contracts

---

## Timeline Expectations

### First Questionnaire

**Time:** 20-40 hours

**Breakdown:**
- Reading questions: 2-4 hours
- Researching answers: 8-16 hours
- Writing answers: 6-12 hours
- Gathering evidence: 2-4 hours
- Internal review: 2-4 hours

**Team Involvement:** 5-10 people

### Subsequent Questionnaires (With Library)

**Time:** 5-10 hours

**Breakdown:**
- Reading questions: 1-2 hours
- Copy/paste from library: 2-4 hours
- Customization: 1-2 hours
- Evidence attachment: 1 hour
- Internal review: 1 hour

**Team Involvement:** 2-3 people

### Customer Review

**Time:** 1-2 weeks

**Activities:**
- Customer security team reviews
- Follow-up questions
- Internal approvals

### Follow-Up Rounds

**Rounds:** 1-2 typically

**Time:** 1-2 weeks per round

**Common Follow-Ups:**
- Clarifications
- Additional evidence
- References

---

## Real Questionnaire Examples (Sanitized)

### Example 1: Financial Services Customer

**Questionnaire:** 350 questions (SIG format)

**Key Focus Areas:**
- Data encryption (detailed)
- Access controls (very detailed)
- Audit logging
- Compliance (SOC2, ISO, GDPR)
- Third-party vendors (extensive)

**Challenging Questions:**
- "Provide network diagram"
- "List all subprocessors with data access"
- "Describe your change management process"

**Outcome:** Approved after 2 rounds of follow-up (6 weeks)

### Example 2: Healthcare Customer

**Questionnaire:** 200 questions (custom)

**Key Focus Areas:**
- HIPAA compliance
- PHI handling
- Business Associate Agreement (BAA)
- Encryption
- Access controls

**Challenging Questions:**
- "Are you HIPAA compliant?" (needed BAA)
- "Do you have HITRUST certification?" (no, explained alternative controls)

**Outcome:** Approved with BAA signing (4 weeks)

### Example 3: Enterprise SaaS Customer

**Questionnaire:** 180 questions (CAIQ format)

**Key Focus Areas:**
- SOC2 Type II
- SSO/SCIM
- Data residency
- Disaster recovery

**Challenging Questions:**
- "Provide SOC2 report" (under NDA)
- "What's your RTO/RPO?" (needed DR plan)

**Outcome:** Approved after SOC2 report shared (3 weeks)

---

## Templates

### Standard Response Library Template

```markdown
# Security Questionnaire Standard Responses

Last Updated: [DATE]
Owner: Security Team

## Instructions
1. Search for question in this document
2. Copy answer
3. Customize for specific customer if needed
4. Attach evidence if required

---

## Company Information

### Q: Company name
**A:** Acme Inc.

### Q: Number of employees
**A:** 50 employees as of [DATE]

### Q: Year founded
**A:** 2020

---

## Data Security

### Q: Do you encrypt data at rest?
**A:** Yes, all data at rest is encrypted using AES-256 encryption. Database encryption is managed by AWS RDS with encryption keys stored in AWS KMS. File storage uses AWS S3 with server-side encryption enabled.

**Evidence:** AWS encryption configuration screenshots

### Q: Do you encrypt data in transit?
**A:** Yes, all data in transit is encrypted using TLS 1.2 or higher. We enforce HTTPS for all web traffic and use TLS for all API communications. We have disabled older protocols (SSL, TLS 1.0, TLS 1.1).

**Evidence:** SSL Labs test results

[... continue for all common questions]
```

### Evidence Checklist Template

```markdown
# Security Questionnaire Evidence Checklist

## Certifications
- [ ] SOC2 Type II report (PDF, under NDA)
- [ ] ISO 27001 certificate (PDF, if applicable)
- [ ] HIPAA compliance documentation (if applicable)
- [ ] PCI DSS certification (if applicable)

## Security Testing
- [ ] Penetration test results (PDF, redacted)
- [ ] Vulnerability scan results (PDF)
- [ ] Security audit results (PDF)

## Policies and Plans
- [ ] Security policy (PDF)
- [ ] Privacy policy (PDF)
- [ ] Incident response plan (PDF)
- [ ] Disaster recovery plan (PDF)
- [ ] Business continuity plan (PDF)
- [ ] Acceptable use policy (PDF)
- [ ] Data retention policy (PDF)

## Contracts and Agreements
- [ ] Data Processing Agreement (DPA) template
- [ ] Business Associate Agreement (BAA) template (if HIPAA)
- [ ] Master Service Agreement (MSA) template
- [ ] Service Level Agreement (SLA)

## Technical Documentation
- [ ] Network diagram (PDF, sanitized)
- [ ] Architecture diagram (PDF)
- [ ] Encryption configuration (screenshots)
- [ ] Access control configuration (screenshots)

## Vendor Information
- [ ] Subprocessor list (Excel/PDF)
- [ ] Vendor contracts (PDFs)
- [ ] Vendor security assessments (PDFs)

## Other
- [ ] Insurance certificate (cyber liability)
- [ ] Employee training certificates
- [ ] Background check policy
- [ ] DR test results
```

---

## Summary

### Quick Reference

**What:** Long surveys (100-500 questions) to assess vendor security

**Why:** Required for enterprise sales, repeated for each customer

**Time:**
- First time: 20-40 hours
- With library: 5-10 hours

**Topics:**
- Company info, data security, infrastructure, compliance, incident response, access management, development, vendors, physical security, HR

**Preparation:**
- Security documentation
- Compliance certifications (SOC2, ISO)
- Standard response library
- Evidence files

**Tools:**
- Whistic (questionnaire automation)
- SafeBase (security portal)
- Vanta (compliance + questionnaires)
- Manual (Google Docs)

**Streamlining:**
- Trust center (public docs)
- Self-service portal
- Standard questionnaire
- Pre-filled responses

**Challenging Questions:**
- Security breaches (honesty + mitigation)
- Cyber insurance (get it!)
- RTO/RPO (need DR plan)
- Production access (track and audit)

**Workflow:**
1. Receive questionnaire
2. Assign to teams
3. Fill out with evidence
4. Internal review
5. Submit
6. Follow-up
7. Approval

**Timeline:**
- Completion: 1-2 weeks
- Customer review: 1-2 weeks
- Follow-up: 1-2 weeks
- Total: 3-6 weeks

## Best Practices

### Preparation Best Practices
- **Start Early**: Begin security questionnaire preparation before your first enterprise customer. Getting SOC2, ISO 27001, and other certifications takes 6-12 months.
- **Build Standard Response Library**: Create and maintain a comprehensive library of standard responses to common security questions. This reduces completion time from 20-40 hours to 5-10 hours.
- **Keep Evidence Updated**: Maintain current versions of all evidence files (SOC2 reports, penetration test results, policies). Expired or outdated evidence raises red flags.
- **Centralized Documentation**: Store all security documentation in a single, accessible location (Google Drive, Confluence, Notion) with clear version control.
- **Cross-Team Collaboration**: Involve security, legal, engineering, and HR teams in questionnaire preparation. Each team owns their section.

### Questionnaire Response Best Practices
- **Be Honest but Positive**: If you've had security incidents, acknowledge them but emphasize your response and remediation. Honesty builds trust.
- **Provide Specific Details**: Avoid vague answers like "we have security controls." Instead, provide specific details like "we encrypt data at rest using AES-256 with keys managed by AWS KMS."
- **Include Evidence**: Reference supporting evidence for each claim. For example, "See our SOC2 Type II report (available under NDA) for audit findings."
- **Consistent Answers**: Ensure consistent answers across all questionnaires. Use your standard response library to maintain consistency.
- **Avoid "N/A" Without Explanation**: If a question doesn't apply, explain why. For example, "N/A - We use AWS for infrastructure, so physical datacenter security is AWS's responsibility. See AWS SOC2 report for details."

### Evidence Management Best Practices
- **Organize by Category**: Group evidence files by category (certifications, policies, testing, contracts) for easy access.
- **Version Control**: Maintain version history for all evidence files. Track when documents were last updated and by whom.
- **Secure Storage**: Store sensitive evidence (SOC2 reports, penetration test results) in secure, access-controlled locations.
- **Redaction**: Redact sensitive information from evidence before sharing (specific vulnerabilities, internal IP addresses, employee names).
- **Document Evidence**: Maintain a spreadsheet or database tracking all evidence files, their locations, and what questions they address.

### Streamlining Best Practices
- **Trust Center**: Create a public trust center with security overview, compliance certifications, privacy policy, DPA, and subprocessor list. This reduces questionnaire volume by 30-50%.
- **Self-Service Portal**: Implement a portal where customers can access security documentation under NDA. This reduces manual work.
- **Standard Questionnaire**: Offer your own comprehensive security questionnaire for customers to accept instead of theirs. 30-50% will accept.
- **Pre-Filled Responses**: Share your standard response library with customers. Ask them to copy relevant answers into their questionnaire.
- **Questionnaire Automation**: Use tools like Whistic, SafeBase, or Vanta to automate questionnaire completion and management.

### Challenging Question Best Practices
- **Security Breaches**: Be honest about past incidents. Describe the incident, your response, remediation steps, and lessons learned. Emphasize that customer data was not compromised.
- **Cyber Insurance**: Obtain cyber liability insurance ($1M-5M coverage). This shows you take security seriously and can financially respond to incidents.
- **RTO/RPO**: Have a documented disaster recovery plan with defined Recovery Time Objective (RTO) and Recovery Point Objective (RPO). Provide actual test results showing you meet these targets.
- **Production Access**: Track and audit who has access to production data. Provide specific counts (e.g., "5 senior engineers have production access, all access is logged and reviewed monthly").

### Workflow Best Practices
- **Assign by Expertise**: Assign questionnaire sections to team members with relevant expertise (security team for data security questions, legal for compliance questions).
- **Internal Review**: Conduct internal review before submission. Security team reviews technical accuracy, legal reviews compliance, sales reviews customer context.
- **Track Progress**: Use CRM or project management tools to track questionnaire progress, due dates, and follow-up items.
- **Follow-Up Preparation**: Anticipate follow-up questions and have additional evidence ready. Common follow-ups include "Can you provide your SOC2 report?" and "Can you explain your encryption in more detail?"
- **Timeline Management**: Set realistic expectations with customers. Questionnaire completion typically takes 1-2 weeks, plus 1-2 weeks for customer review and follow-up.

### Maintenance Best Practices
- **Regular Updates**: Review and update standard responses quarterly or when significant changes occur (new certification, infrastructure change, policy update).
- **Annual Renewals**: Track certification renewal dates (SOC2, ISO 27001) and start renewal process 3-6 months in advance.
- **Penetration Testing**: Schedule annual penetration testing. Budget 4-8 weeks for testing, remediation, and re-testing.
- **Security Training**: Conduct annual security training for all employees. Document completion and maintain training records.
- **Incident Response Drills**: Perform quarterly incident response drills. Document results and update incident response plan based on learnings.

## Checklist

### Preparation Checklist
- [ ] Obtain SOC2 Type II certification
- [ ] Obtain ISO 27001 certification (if applicable)
- [ ] Create standard response library with 200+ questions
- [ ] Collect all evidence files (SOC2, ISO, pen test results)
- [ ] Create security policy document
- [ ] Create privacy policy
- [ ] Create incident response plan
- [ ] Create disaster recovery plan
- [ ] Create data retention policy
- [ ] Create vendor management policy
- [ ] Create subprocessor list
- [ ] Obtain cyber liability insurance
- [ ] Set up centralized documentation storage

### Questionnaire Response Checklist
- [ ] Assign sections to appropriate team members
- [ ] Copy answers from standard response library
- [ ] Customize answers for specific customer
- [ ] Attach evidence where required
- [ ] Flag questions requiring research
- [ ] Conduct internal review (security, legal, sales)
- [ ] Submit completed questionnaire to customer
- [ ] Track submission date and expected review timeline

### Evidence Checklist
- [ ] SOC2 Type II report (current, under NDA)
- [ ] ISO 27001 certificate (if applicable)
- [ ] Penetration test results (redacted, current)
- [ ] Vulnerability scan results
- [ ] Security policy (current)
- [ ] Privacy policy (current)
- [ ] Incident response plan (current)
- [ ] Disaster recovery plan (current)
- [ ] Business continuity plan (current)
- [ ] Acceptable use policy (current)
- [ ] Data retention policy (current)
- [ ] Vendor management policy (current)
- [ ] Data Processing Agreement (DPA) template
- [ ] Business Associate Agreement (BAA) template (if HIPAA)
- [ ] Master Service Agreement (MSA) template
- [ ] Service Level Agreement (SLA)
- [ ] Network diagram (sanitized)
- [ ] Architecture diagram (sanitized)
- [ ] Encryption configuration screenshots
- [ ] Access control configuration screenshots
- [ ] Subprocessor list (Excel/PDF)
- [ ] Vendor contracts (PDFs)
- [ ] Vendor security assessments (PDFs)
- [ ] Insurance certificate (cyber liability)
- [ ] Employee training certificates
- [ ] Background check policy
- [ ] DR test results

### Trust Center Checklist
- [ ] Create public trust center website
- [ ] Add security overview page
- [ ] Add compliance certifications page (SOC2, ISO)
- [ ] Add privacy policy
- [ ] Add Data Processing Agreement (DPA)
- [ ] Add subprocessor list
- [ ] Add security whitepaper
- [ ] Add contact information (security@yourcompany.com)
- [ ] Configure secure document sharing (under NDA)
- [ ] Set up analytics (who viewed what)

### Streamlining Checklist
- [ ] Evaluate questionnaire automation tools (Whistic, SafeBase, Vanta)
- [ ] Implement self-service security portal
- [ ] Create standard questionnaire (200+ questions)
- [ ] Share standard response library with customers
- [ ] Train team on using automation tools
- [ ] Measure time savings from automation

### Challenging Question Preparation Checklist
- [ ] Document any security incidents (last 3 years)
- [ ] Prepare incident response summary (what happened, response, remediation)
- [ ] Obtain cyber liability insurance ($1M-5M coverage)
- [ ] Document RTO and RPO with DR plan
- [ ] Perform and document DR test results
- [ ] Audit and document production access (who, what, when)
- [ ] Create access review process documentation
- [ ] Prepare explanation for any security gaps

### Workflow Checklist
- [ ] Create questionnaire assignment process
- [ ] Set up internal review process
- [ ] Configure CRM to track questionnaire progress
- [ ] Set up project management tool for task tracking
- [ ] Define timeline expectations (1-2 weeks completion, 1-2 weeks review)
- [ ] Create follow-up question preparation process
- [ ] Train team on questionnaire workflow

### Maintenance Checklist
- [ ] Schedule quarterly documentation reviews
- [ ] Track certification renewal dates
- [ ] Schedule annual penetration testing
- [ ] Schedule annual security training
- [ ] Schedule quarterly incident response drills
- [ ] Create update triggers (new cert, infrastructure change, policy update)
- [ ] Assign documentation owners for each section
- [ ] Set up reminders for renewal dates

### Team Training Checklist
- [ ] Train security team on questionnaire responses
- [ ] Train legal team on compliance questions
- [ ] Train engineering team on technical security questions
- [ ] Train HR team on HR-related questions
- [ ] Train sales team on customer communication
- [ ] Create onboarding guide for new team members
- [ ] Document common mistakes and how to avoid them

### Post-Submission Checklist
- [ ] Track submission date
- [ ] Set reminder for customer review follow-up
- [ ] Prepare for follow-up questions
- [ ] Schedule follow-up call if needed
- [ ] Document lessons learned from each questionnaire
- [ ] Update standard response library based on new questions
