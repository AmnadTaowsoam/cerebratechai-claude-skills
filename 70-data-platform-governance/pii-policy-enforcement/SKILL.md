---
name: PII Policy Enforcement
description: Policy และ mechanisms สำหรับ detect, classify และ protect PII data ใน data platform
---

# PII Policy Enforcement

## Overview

Policy และ mechanisms สำหรับ detect, classify และ protect PII (Personally Identifiable Information) ใน data platform

## Why This Matters

- **Compliance**: GDPR, CCPA requirements
- **Privacy**: Protect user data
- **Security**: Prevent data leaks
- **Trust**: Build customer confidence

---

## PII Classification

### Levels
```
Level 1 - Public: Name, job title
Level 2 - Internal: Employee ID, department
Level 3 - Confidential: Email, phone, address
Level 4 - Restricted: SSN, credit card, health data
```

### Auto-Detection
```python
from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()

# Detect PII
text = "John's email is john@example.com and SSN is 123-45-6789"
results = analyzer.analyze(text, language='en')

for result in results:
    print(f"{result.entity_type}: {result.score}")
# Output:
# EMAIL_ADDRESS: 0.95
# US_SSN: 0.85
```

---

## Enforcement Mechanisms

### 1. Column-Level Encryption
```sql
-- Encrypt PII columns
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR ENCRYPTED,  -- Auto-encrypt
  ssn VARCHAR ENCRYPTED,
  name VARCHAR  -- Not encrypted
);
```

### 2. Row-Level Security
```sql
-- Only show PII to authorized users
CREATE POLICY pii_access ON users
  USING (
    current_user IN (SELECT user_id FROM pii_authorized_users)
    OR is_admin(current_user)
  );
```

### 3. Data Masking
```python
def mask_pii(data: dict) -> dict:
    """Mask PII fields"""
    masked = data.copy()
    
    if 'email' in masked:
        masked['email'] = mask_email(masked['email'])
        # john@example.com → j***@example.com
    
    if 'ssn' in masked:
        masked['ssn'] = mask_ssn(masked['ssn'])
        # 123-45-6789 → ***-**-6789
    
    return masked
```

---

## Access Control

```yaml
# pii-policy.yaml
policies:
  - name: email_access
    resource: users.email
    allowed_roles:
      - admin
      - customer_support
    audit: true
  
  - name: ssn_access
    resource: users.ssn
    allowed_roles:
      - admin
    require_mfa: true
    audit: true
    alert: true
```

---

## Audit Logging

```python
# Log all PII access
def log_pii_access(user_id: str, resource: str, action: str):
    audit_log.write({
        'timestamp': datetime.now(),
        'user_id': user_id,
        'resource': resource,
        'action': action,
        'ip_address': request.ip,
        'success': True
    })

# Example
@require_pii_access('users.email')
def get_user_email(user_id: str):
    log_pii_access(current_user.id, f'users.{user_id}.email', 'read')
    return db.query('SELECT email FROM users WHERE id = ?', user_id)
```

---

## Summary

**PII Policy:** Protect sensitive personal data

**Classification:**
- Level 1-4 (Public → Restricted)
- Auto-detection (Presidio)

**Enforcement:**
- Column encryption
- Row-level security
- Data masking
- Access control

**Compliance:**
- Audit logging
- Access reviews
- Data retention
- Right to deletion
