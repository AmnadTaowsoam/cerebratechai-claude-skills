---
name: Security Audit
description: Systematic examination of an organization's security controls, policies, and procedures to identify vulnerabilities, assess compliance, validate controls, and ensure security standards are met.
---

# Security Audit

> **Current Level:** Intermediate  
> **Domain:** Security / Compliance

---

## Overview

A security audit is a systematic examination of an organization's security controls, policies, and procedures to identify vulnerabilities and ensure compliance with security standards. Effective security audits include comprehensive reviews, risk assessment, compliance checking, and actionable recommendations.

## What is Security Audit

### Security Audit Goals

| Goal | Description |
|-------|-------------|
| **Identify Vulnerabilities** | Find security weaknesses |
| **Assess Compliance** | Verify regulatory requirements |
| **Validate Controls** | Ensure security measures work |
| **Prioritize Remediation** | Guide security improvements |
| **Reduce Risk** | Minimize security exposure |

### Why Security Audit Matters

| Benefit | Impact |
|---------|---------|
| **Proactive Security** | Find issues before attackers |
| **Compliance** | Meet regulatory requirements |
| **Risk Management** | Understand and reduce risk |
| **Trust Building** | Demonstrate security commitment |
| **Cost Savings** | Fix issues before breach |

## Audit Types

### Internal Audit

**Conducted by**: Internal security team

| Pros | Cons |
|-------|-------|
| Less expensive | May lack objectivity |
| Faster turnaround | May miss external perspective |
| Better system knowledge | Limited expertise |

### External Audit

**Conducted by**: Third-party security firm

| Pros | Cons |
|-------|-------|
| Objective assessment | More expensive |
| Specialized expertise | Longer timeline |
| Industry benchmarking | Less system knowledge |

### Compliance Audit

**Focus**: Regulatory requirements

| Regulation | Requirements |
|------------|-------------|
| **SOC2** | Security controls, availability |
| **ISO 27001** | ISMS requirements |
| **PCI DSS** | Payment card security |
| **HIPAA** | Healthcare data security |
| **GDPR** | Data protection (EU) |

## Audit Scope and Planning

### Define Scope

| Component | Examples |
|-----------|----------|
| **Systems** | Web servers, databases, APIs |
| **Applications** | Web apps, mobile apps, internal tools |
| **Network** | Firewall, VPN, wireless |
| **Processes** | Access control, change management |
| **People** | Security awareness, training |

### Audit Planning Checklist

| Item | Description |
|------|-------------|
| [ ] Audit objectives defined |
| [ ] Scope documented |
| [ ] Team assigned |
| [ ] Timeline established |
| [ ] Tools selected |
| [ ] Stakeholders notified |
| [ ] Legal review completed |

### Risk Assessment

| Risk Level | Description |
|------------|-------------|
| **Critical** | Immediate action required |
| **High** | Action required within 30 days |
| **Medium** | Action required within 90 days |
| **Low** | Action recommended within 180 days |

## Security Controls Review

### Technical Controls

| Control Type | Examples |
|--------------|----------|
| **Access Control** | MFA, least privilege, RBAC |
| **Network Security** | Firewall, IDS/IPS, VPN |
| **Application Security** | WAF, input validation, encryption |
| **Endpoint Security** | Antivirus, EDR, disk encryption |
| **Data Security** | Encryption at rest, DLP |

### Administrative Controls

| Control Type | Examples |
|--------------|----------|
| **Policies** | Security policy, acceptable use policy |
| **Procedures** | Incident response, change management |
| **Training** | Security awareness, secure coding |
| **Monitoring** | Log review, security metrics |

### Physical Controls

| Control Type | Examples |
|--------------|----------|
| **Access** | Badge readers, biometrics |
| **Surveillance** | Cameras, security guards |
| **Environmental** | Fire suppression, climate control |
| **Visitor Management** | Sign-in/out procedures |

## Code Review for Security

### Review Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Secure Code Review Process                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Self-Review ──▶ 2. Peer Review ──▶ 3. Security Review │
│                                                                  │
│  └───────────────────────────────────────────────────────────────┘
│                                  │
│                                  ▼
│                           ┌─────────────┐
│                           │  SAST Scan  │
│                           └─────────────┘
│                                  │
│                                  ▼
│                           ┌─────────────┐
│                           │  Fix Issues  │
│                           └─────────────┘
```

### Review Checklist

| Category | Items |
|----------|--------|
| **Input Validation** | All user input validated? |
| **Output Encoding** | All output properly encoded? |
| **SQL Injection** | Parameterized queries used? |
| **Authentication** | Strong password hashing? MFA? |
| **Authorization** | Proper access controls? |
| **Error Handling** | No information leakage? |
| **Cryptography** | Strong algorithms used? |
| **Session Management** | Secure configuration? |
| **Dependencies** | Known vulnerabilities? |

## Configuration Review

### Web Server Configuration

| Check | Apache | Nginx |
|-------|---------|--------|
| **Version** | Latest stable | Latest stable |
| **SSL/TLS** | Strong ciphers | Strong ciphers |
| **HTTP Headers** | Security headers | Security headers |
| **Directory Listing** | Disabled | Disabled |
| **Default Files** | Removed | Removed |
| **Server Tokens** | Hidden | Hidden |

### Database Configuration

| Check | MySQL | PostgreSQL |
|-------|-------|-----------|
| **Version** | Latest stable | Latest stable |
| **Authentication** | Strong passwords | Strong passwords |
| **Network** | Bind to localhost | Bind to localhost |
| **Logging** | Enabled | Enabled |
| **Backup** | Regular backups | Regular backups |
| **Encryption** | At rest | At rest |

### Cloud Configuration

| Check | AWS | Azure | GCP |
|-------|-----|-------|-----|
| **IAM** | Least privilege | Least privilege | Least privilege |
| **S3 Buckets** | Private | Private | Private |
| **Security Groups** | Minimal ports | Minimal ports | Minimal ports |
| **Encryption** | Enabled | Enabled | Enabled |
| **Logging** | CloudTrail | Monitor | Cloud Audit |

## Access Control Audit

### User Access Review

```sql
-- Identify users with excessive access
SELECT
    u.username,
    COUNT(DISTINCT r.role_id) AS role_count
FROM users u
JOIN user_roles ur ON u.id = ur.user_id
JOIN roles r ON ur.role_id = r.id
GROUP BY u.username
HAVING COUNT(DISTINCT r.role_id) > 3;
```

### Permission Audit

```sql
-- Identify users with admin access
SELECT
    u.username,
    r.name AS role
FROM users u
JOIN user_roles ur ON u.id = ur.user_id
JOIN roles r ON ur.role_id = r.id
WHERE r.name = 'admin';
```

### Inactive Account Review

```sql
-- Identify inactive accounts
SELECT
    username,
    last_login,
    EXTRACT(DAY FROM (CURRENT_DATE - last_login)) AS days_inactive
FROM users
WHERE EXTRACT(DAY FROM (CURRENT_DATE - last_login)) > 90;
```

## Log Review and Analysis

### Log Sources

| Source | Type | What It Shows |
|---------|-------|----------------|
| **Web Server** | Access, Error | Requests, errors |
| **Application** | Application | App events, errors |
| **Database** | Query, Error | Queries, errors |
| **Firewall** | Network | Allowed/blocked traffic |
| **IDS/IPS** | Security | Security events |

### Log Analysis Queries

```bash
# Find failed login attempts
grep "Failed password" /var/log/auth.log | tail -100

# Find suspicious IP addresses
awk '$9 > 1000 {print}' /var/log/nginx/access.log

# Find error spikes
grep "ERROR" /var/log/app.log | awk '{print $1,$2}' | sort | uniq -c | sort -rn
```

### SIEM Queries

```sql
-- Find brute force attempts
SELECT
    source_ip,
    COUNT(*) AS attempt_count
FROM auth_logs
WHERE event_type = 'failed_login'
    AND timestamp > NOW() - INTERVAL '1 hour'
GROUP BY source_ip
HAVING COUNT(*) > 10;
```

## Vulnerability Assessment

### Automated Scanning

| Tool | Type | What It Finds |
|-------|-------|----------------|
| **Nessus** | Vulnerability scanner | Known vulnerabilities |
| **OpenVAS** | Vulnerability scanner | Known vulnerabilities |
| **Qualys** | Vulnerability scanner | Known vulnerabilities |
| **Nikto** | Web scanner | Web server vulnerabilities |

### Manual Testing

| Test Type | What It Checks |
|-----------|----------------|
| **Penetration Test** | Exploitable vulnerabilities |
| **Code Review** | Security issues in code |
| **Configuration Review** | Security misconfigurations |
| **Social Engineering** | Human vulnerabilities |

### Vulnerability Prioritization

| Factor | Weight |
|---------|--------|
| **CVSS Score** | 40% |
| **Exploitability** | 30% |
| **Business Impact** | 20% |
| **Asset Criticality** | 10% |

## Compliance Verification

### SOC2 Compliance

| Requirement | Evidence |
|-------------|-----------|
| **Access Control** | Access logs, MFA implementation |
| **Change Management** | Change tickets, approvals |
| **Incident Response** | Incident reports, procedures |
| **Monitoring** | SIEM logs, alerts |
| **Data Encryption** | Encryption policies, implementation |

### ISO 27001 Compliance

| Requirement | Evidence |
|-------------|-----------|
| **Security Policy** | Documented security policy |
| **Risk Assessment** | Risk register, treatment plans |
| **Asset Management** | Asset inventory |
| **Access Control** | Access control procedures |
| **Training** | Training records |

### PCI DSS Compliance

| Requirement | Evidence |
|-------------|-----------|
| **Network Security** | Firewall rules, IDS/IPS |
| **Data Protection** | Encryption at rest and in transit |
| **Vulnerability Management** | Scan reports, patch management |
| **Access Control** | MFA, least privilege |
| **Monitoring** | Log monitoring, alerting |

## Audit Findings and Risk Rating

### Finding Template

```
Finding: [Title]

Severity: [Critical/High/Medium/Low]

Description:
[Detailed description of the vulnerability]

Evidence:
[Screenshots, logs, code snippets]

Impact:
[Potential business impact]

CVSS Score:
[CVSS score if applicable]

Recommendation:
[Specific remediation steps]

Priority:
[Immediate/30 days/90 days/180 days]

Owner:
[Person or team responsible]
```

### Risk Matrix

```
                    Impact
              Low    Medium    High
              ┌───────┬─────────┬─────────┐
        Low   │   L    │    M    │    H    │
              ├───────┼─────────┼─────────┤
Likelihood Medium │   M    │    H    │   C    │
              ├───────┼─────────┼─────────┤
        High  │   H    │    C    │   C    │
              └───────┴─────────┴─────────┘

L = Low Risk, M = Medium Risk, H = High Risk, C = Critical Risk
```

## Remediation Planning

### Remediation Process

```
┌─────────────────────────────────────────────────────────────────┐
│  Remediation Process                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Prioritize ──▶ 2. Assign ──▶ 3. Implement ──▶ 4. Verify │
│                                                                  │
│  └───────────────────────────────────────────────────────────────┘
│                                  │
│                                  ▼
│                           ┌─────────────┐
│                           │  Document    │
│                           └─────────────┘
```

### Remediation Tracking

| Finding | Priority | Assigned To | Status | Target Date |
|---------|----------|-------------|--------|-------------|
| SQL injection in login | Critical | John Smith | In Progress | 2024-02-01 |
| Missing security headers | High | Jane Doe | Not Started | 2024-02-15 |
| Outdated OpenSSL | Medium | Dev Team | Not Started | 2024-03-01 |

### Verification

```bash
# Verify SQL injection fix
sqlmap -u "https://example.com/login" --batch

# Verify security headers
curl -I https://example.com | grep -E "X-Frame-Options|X-XSS-Protection"

# Verify OpenSSL version
openssl version
```

## Audit Reporting

### Report Structure

1. **Executive Summary**
   - High-level findings
   - Risk assessment
   - Recommendations

2. **Methodology**
   - Audit scope
   - Tools used
   - Timeline

3. **Findings**
   - Detailed findings
   - Risk ratings
   - Evidence

4. **Recommendations**
   - Prioritized actions
   - Remediation timeline
   - Resource requirements

5. **Appendices**
   - Technical details
   - Evidence
   - Checklists

### Report Template

```markdown
# Security Audit Report

**Company**: [Company Name]
**Date**: [Audit Date]
**Auditor**: [Auditor Name]

## Executive Summary

[Brief summary of audit findings and overall risk assessment]

## Methodology

### Scope
[Description of audit scope]

### Tools Used
- [Tool 1]
- [Tool 2]
- [Tool 3]

### Timeline
- Planning: [Date]
- Testing: [Date]
- Analysis: [Date]
- Reporting: [Date]

## Findings

### Critical Findings
[Detailed findings]

### High Findings
[Detailed findings]

### Medium Findings
[Detailed findings]

### Low Findings
[Detailed findings]

## Recommendations

[Priority recommendations with timelines]

## Appendices

[Technical details, evidence, checklists]
```

## Follow-up and Verification

### Remediation Verification

| Step | Description |
|------|-------------|
| [ ] Implement fixes |
| [ ] Test fixes |
| [ ] Document changes |
| [ ] Update procedures |
| [ ] Train staff |

### Re-audit

| Trigger | Action |
|---------|--------|
| Major changes | Schedule re-audit |
| Time-based | Annual re-audit |
| Incident | Post-incident audit |

### Continuous Monitoring

| Metric | Target |
|---------|--------|
| Vulnerability count | Trending down |
| Patch compliance | > 95% |
| Security incidents | < 1 per quarter |
| Audit findings closed | > 90% within SLA |

## Continuous Audit

### Automated Auditing

| Tool | What It Monitors |
|------|------------------|
| **SAST** | Code vulnerabilities |
| **DAST** | Web vulnerabilities |
| **Dependency Scanning** | Known vulnerabilities |
| **Configuration Scanning** | Misconfigurations |

### Continuous Monitoring

```bash
# Daily vulnerability scan
0 0 * * * /usr/bin/nessus -q localhost >> /var/log/nessus.log 2>&1

# Weekly configuration check
0 0 * * 0 /usr/bin/nmap -sV localhost >> /var/log/nmap.log 2>&1

# Daily log review
0 0 * * * /usr/bin/grep "ERROR" /var/log/app.log | tail -100
```

## Summary Checklist

### Audit Preparation

- [ ] Scope defined
- [ ] Team assembled
- [ ] Tools selected
- [ ] Timeline established
- [ ] Stakeholders notified

### Audit Execution

- [ ] Technical controls reviewed
- [ ] Administrative controls reviewed
- [ ] Physical controls reviewed
- [ ] Code reviewed
- [ ] Configuration reviewed
- [ ] Logs analyzed
- [ ] Vulnerabilities assessed

### Reporting

- [ ] Findings documented
- [ ] Risks assessed
- [ ] Recommendations made
```

---

## Quick Start

### Security Audit Checklist

```markdown
# Security Audit Checklist

## Authentication & Authorization
- [ ] Strong password policies
- [ ] Multi-factor authentication
- [ ] Role-based access control
- [ ] Session management

## Data Protection
- [ ] Encryption at rest
- [ ] Encryption in transit
- [ ] Data backup
- [ ] Data retention policies

## Network Security
- [ ] Firewall rules
- [ ] Network segmentation
- [ ] Intrusion detection
- [ ] VPN access

## Application Security
- [ ] Input validation
- [ ] Output encoding
- [ ] Error handling
- [ ] Security headers
```

---

## Production Checklist

- [ ] **Audit Plan**: Security audit plan documented
- [ ] **Team**: Audit team assembled
- [ ] **Scope**: Audit scope defined
- [ ] **Tools**: Audit tools selected
- [ ] **Review**: Review security controls
- [ ] **Compliance**: Check compliance requirements
- [ ] **Documentation**: Document all findings
- [ ] **Risk Assessment**: Assess security risks
- [ ] **Recommendations**: Provide recommendations
- [ ] **Remediation**: Track remediation
- [ ] **Follow-up**: Follow-up audits
- [ ] **Reporting**: Regular audit reports

---

## Anti-patterns

### ❌ Don't: No Follow-up

```markdown
# ❌ Bad - Audit but no action
Security audit completed
Findings: 50 vulnerabilities
Actions taken: 0
```

```markdown
# ✅ Good - Act on findings
Security audit completed
Findings: 50 vulnerabilities
Actions taken: 45 fixed, 5 in progress
```

### ❌ Don't: Surface-Level Audit

```markdown
# ❌ Bad - Surface-level only
Checked: Password policy
# No deep review!
```

```markdown
# ✅ Good - Comprehensive audit
Checked:
- Password policy
- Implementation
- Enforcement
- Monitoring
# Deep review
```

---

## Integration Points

- **Penetration Testing** (`24-security-practices/penetration-testing/`) - Security testing
- **Vulnerability Management** (`24-security-practices/vulnerability-management/`) - Vulnerability handling
- **OWASP Top 10** (`24-security-practices/owasp-top-10/`) - Security standards

---

## Further Reading

- [Security Audit Guide](https://www.isaca.org/resources/security-audit)
- [NIST Security Framework](https://www.nist.gov/cyberframework)
- [ ] Report delivered

### Follow-up

- [ ] Remediation tracked
- [ ] Fixes verified
- [ ] Procedures updated
- [ ] Re-audit scheduled
