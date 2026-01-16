---
name: Summarization Rules (Evidence First)
description: กฎการสรุปแบบ evidence-first - เริ่มจาก evidence/data ก่อน แล้วค่อยสรุป ลด token และเพิ่มความน่าเชื่อถือ
---

# Summarization Rules (Evidence First)

## Overview

กฎการสรุปที่เน้น evidence ก่อน conclusion - แสดงข้อมูลสำคัญก่อน แล้วค่อยสรุป ทำให้ใช้ token น้อยลงและน่าเชื่อถือมากขึ้น

## Why This Matters

- **Credibility**: Evidence ก่อน = น่าเชื่อถือ
- **Efficiency**: ตัดคำอธิบายยาวๆ
- **Actionable**: เห็น data ชัดเจน
- **Verifiable**: ตรวจสอบได้

---

## Traditional vs Evidence-First

### ❌ Traditional (Conclusion First)
```
"The system is experiencing performance issues due to several factors 
including high database load, inefficient queries, and memory leaks. 
Based on our analysis, we recommend the following improvements..."

(150 tokens, vague)
```

### ✅ Evidence-First
```
Performance Issues:
- DB CPU: 95% (normal: <70%)
- Slow queries: 15 (>1s each)
- Memory: 8GB → 12GB in 2 hours

Fix: Add indexes, optimize queries, fix leak in auth.ts:45

(40 tokens, specific)
```

**Savings: 73%**

---

## Core Rules

### Rule 1: Data Before Interpretation
```
❌ "The API is slow"
✅ "API response time: 2.5s (SLA: <500ms)"

❌ "Many users affected"
✅ "1,247 users (12% of active users)"

❌ "Database is overloaded"
✅ "DB connections: 95/100, CPU: 87%"
```

### Rule 2: Numbers Over Adjectives
```
❌ "Very slow"
✅ "2.5s (5x slower than baseline)"

❌ "High error rate"
✅ "Error rate: 5.2% (normal: 0.1%)"

❌ "Significant improvement"
✅ "Response time: 2s → 500ms (75% faster)"
```

### Rule 3: Specific Over General
```
❌ "Several files changed"
✅ "3 files: auth.ts, db.ts, config.ts"

❌ "Recent issues"
✅ "Issues in last 24h: 12 (P0: 2, P1: 10)"

❌ "Multiple errors"
✅ "Errors: 'Invalid token' (80%), 'Timeout' (20%)"
```

---

## Templates

### Bug Report
```
## Bug: [Title]

Evidence:
- Error: [exact message]
- Frequency: [X times in Y period]
- Affected: [N users/requests]
- Location: [file:line]

Impact:
- [Metric]: [before] → [after]

Fix:
- [Specific action]
```

### Performance Issue
```
## Performance: [Area]

Metrics:
- [Metric 1]: [value] (baseline: [value])
- [Metric 2]: [value] (SLA: [value])
- [Metric 3]: [value]

Root cause:
- [Specific issue in file:line]

Solution:
- [Action with expected improvement]
```

### Code Review
```
## Review: [PR Title]

Changes:
- Added: [list]
- Modified: [list]
- Removed: [list]

Issues:
1. [File:line]: [Specific issue]
2. [File:line]: [Specific issue]

Recommendation:
- [Action]
```

---

## Examples

### Incident Report

#### ❌ Traditional (200 tokens)
```
We experienced a significant outage today that affected many of our users. 
The root cause appears to be related to database performance issues that 
cascaded into application timeouts. Our team investigated and found that 
the problem started around 2pm and was resolved by 4pm. We recommend 
implementing better monitoring and adding database indexes to prevent 
this from happening again.
```

#### ✅ Evidence-First (60 tokens)
```
Outage: 2:00pm - 4:00pm (2 hours)

Impact:
- Users affected: 15,234 (45% of active)
- Failed requests: 89,456
- Revenue loss: ~$12,000

Root cause:
- DB query timeout (auth.ts:156)
- Missing index on users.email

Fix applied:
- Added index (query: 2.5s → 50ms)
- Deployed 3:45pm

Prevention:
- Add query monitoring
- Index audit weekly
```

**Savings: 70%**

---

### Status Update

#### ❌ Traditional (120 tokens)
```
Good progress this week. The team has been working hard on several features 
and we've made significant headway. There are still some challenges we're 
working through, but overall things are moving in the right direction. 
We expect to complete most of the planned work by the end of the sprint.
```

#### ✅ Evidence-First (35 tokens)
```
Sprint Progress (Week 2/2):

Completed: 8/10 stories (80%)
- Feature A: ✓ deployed
- Feature B: ✓ in review
- Feature C: 🔄 in progress (80%)

Blocked: 2 stories
- Story D: waiting for API access
- Story E: design feedback needed

On track for Friday delivery
```

**Savings: 71%**

---

## Formatting Rules

### Use Tables for Comparisons
```
❌ Prose:
"Before the optimization, the API took 2 seconds. After optimization, 
it now takes 500ms. This is a 75% improvement."

✅ Table:
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Response time | 2s | 500ms | -75% |
```

### Use Lists for Multiple Items
```
❌ Prose:
"The changes include adding authentication, updating the database schema, 
and fixing the email service."

✅ List:
Changes:
- Added authentication
- Updated DB schema
- Fixed email service
```

### Use Code Blocks for Specifics
```
❌ Prose:
"The error occurs in the authentication file at line 45"

✅ Code reference:
Error location:
```typescript
// auth.ts:45
const user = await findUser(email);  // ← Throws if email null
```
```

---

## Measurement

### Before Evidence-First
```
Average summary: 150 tokens
Clarity score: 6/10
Action items: vague
```

### After Evidence-First
```
Average summary: 45 tokens
Clarity score: 9/10
Action items: specific
Savings: 70%
```

---

## Quick Checklist

```
Before writing summary:
☐ Do I have specific numbers?
☐ Can I show data instead of describing it?
☐ Are my action items specific?
☐ Can I use a table/list instead of prose?
☐ Did I remove adjectives and use metrics?

If any answer is "no", revise.
```

---

## Anti-Patterns

### ❌ Burying the Lede
```
"After careful analysis and consideration of various factors, 
we have determined that..."

✅ Start with the finding:
"Root cause: Missing index on users.email"
```

### ❌ Vague Quantifiers
```
"Many users", "Several issues", "Significant impact"

✅ Specific numbers:
"1,247 users", "3 issues", "45% slower"
```

### ❌ Opinion Without Evidence
```
"The code is poorly written"

✅ Specific issues:
"Issues:
- No error handling (auth.ts:45)
- N+1 query (users.service.ts:120)
- Memory leak (cache.ts:78)"
```

---

## Summary

**Evidence-First:** แสดง data ก่อน สรุปทีหลัง

**Rules:**
1. Data before interpretation
2. Numbers over adjectives
3. Specific over general

**Format:**
- Tables for comparisons
- Lists for multiple items
- Code blocks for specifics

**Template:**
```
Evidence:
- [Metric]: [value]
- [Metric]: [value]

Impact:
- [Specific impact]

Action:
- [Specific action]
```

**Savings: 70-75% tokens**

**Benefits:**
- More credible
- More actionable
- More verifiable
- Less tokens
