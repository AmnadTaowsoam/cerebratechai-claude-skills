---
name: Security Scan Policy
description: Policy สำหรับ automated security scanning ใน CI/CD pipeline รวม dependency audit, SAST, และ secret detection
---

# Security Scan Policy

## Overview

Policy สำหรับ automated security scanning - dependency vulnerabilities, code vulnerabilities, secrets - ต้องผ่านก่อน deploy

## Why This Matters

- **Prevent breaches**: จับ vulnerabilities ก่อน production
- **Compliance**: Meet security requirements
- **Automated**: ไม่พลาด human error
- **Fast feedback**: รู้ทันทีถ้ามี issue

---

## Security Checks

### 1. Dependency Audit
```bash
# Check for vulnerable dependencies
npm audit --audit-level=high

# Must have 0 high/critical vulnerabilities
✓ 0 vulnerabilities found
```

### 2. SAST (Static Analysis)
```bash
# Scan code for security issues
npm run security:scan

# Check for:
- SQL injection
- XSS vulnerabilities
- Insecure crypto
- Hardcoded secrets
```

### 3. Secret Detection
```bash
# Scan for leaked secrets
git-secrets --scan

# Check for:
- API keys
- Passwords
- Private keys
- Tokens
```

---

## CI Pipeline

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [pull_request, push]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Dependency Audit
        run: npm audit --audit-level=high
      
      - name: SAST Scan
        uses: github/codeql-action/analyze@v2
      
      - name: Secret Scan
        uses: trufflesecurity/trufflehog@main
      
      - name: Container Scan
        run: trivy image myapp:latest
```

---

## Severity Levels

| Level | Action | Example |
|-------|--------|---------|
| Critical | Block merge | RCE vulnerability |
| High | Block merge | SQL injection |
| Medium | Warning | Weak crypto |
| Low | Info only | Outdated dependency |

---

## Tools

```
Dependency: npm audit, Snyk
SAST: CodeQL, SonarQube
Secrets: TruffleHog, git-secrets
Container: Trivy, Grype
```

---

## Summary

**Security Scan:** Automated security checks

**Checks:**
- Dependency audit (npm audit)
- SAST (CodeQL)
- Secret detection (TruffleHog)
- Container scan (Trivy)

**Policy:**
- Critical/High: Block merge
- Medium: Warning
- Low: Info only

**No exceptions for Critical/High**
