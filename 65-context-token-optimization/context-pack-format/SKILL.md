---
name: Context Pack Format
description: รูปแบบการจัดเตรียม context ให้กระชับ มีโครงสร้าง และใช้ token อย่างมีประสิทธิภาพ
---

# Context Pack Format

## Overview

รูปแบบมาตรฐานสำหรับจัดเตรียม context ให้ AI - กระชับ มีโครงสร้าง ใช้ token คุ้มค่า

## Why This Matters

- **Token efficiency**: ลด context size 50-70%
- **Better focus**: AI เข้าใจ context เร็วขึ้น
- **Consistency**: รูปแบบเดียวกันทุกครั้ง
- **Reusability**: Pack ซ้ำได้ง่าย

---

## Standard Format

### Basic Structure
```markdown
# Context Pack: [Topic]

## Summary (50 words max)
[One-paragraph overview]

## Key Files
- `auth.ts` (lines 45-60): Token validation
- `db.ts` (lines 120-135): User queries

## Relevant Code
[Code snippets only - no full files]

## Current State
- What works: [list]
- What's broken: [list]
- Goal: [one sentence]
```

### Example
```markdown
# Context Pack: User Authentication Bug

## Summary
Login fails for users with special characters in email. 
Error occurs in token validation. Need to fix email sanitization.

## Key Files
- `auth.ts` (lines 45-60): validateToken function
- `utils.ts` (lines 12-20): sanitizeEmail helper

## Relevant Code
```typescript
// auth.ts:45-60
export function validateToken(token: string) {
  const decoded = jwt.verify(token, SECRET);
  const email = decoded.email; // ← Bug: no sanitization
  return findUserByEmail(email);
}
```

## Current State
- Works: Normal emails (test@example.com)
- Broken: Emails with + or . (test+1@example.com)
- Goal: Support all valid email characters
```

---

## File Reference Format

### Snippet with Context
```markdown
## From: `path/to/file.ts`
Lines: 45-60
Purpose: Token validation logic

```typescript
export function validateToken(token: string): User | null {
  try {
    const decoded = jwt.verify(token, SECRET);
    return findUserByEmail(decoded.email);
  } catch (error) {
    return null;
  }
}
```

Why included: Shows current implementation with bug
```

### Multiple Snippets
```markdown
## Authentication Flow

### Step 1: Login (`auth.ts:10-25`)
```typescript
export async function login(email: string, password: string) {
  const user = await findUserByEmail(email);
  if (!user || !await bcrypt.compare(password, user.passwordHash)) {
    throw new Error('Invalid credentials');
  }
  return generateToken(user);
}
```

### Step 2: Token Generation (`auth.ts:30-40`)
```typescript
function generateToken(user: User): string {
  return jwt.sign({ userId: user.id, email: user.email }, SECRET);
}
```
```

---

## Compression Techniques

### 1. Remove Boilerplate
```typescript
❌ Bloat (150 tokens):
import { Request, Response, NextFunction } from 'express';
import { validateToken } from './auth';
import { logger } from './logger';
import { config } from './config';

export async function authMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    if (!token) {
      return res.status(401).json({ error: 'No token' });
    }
    const user = await validateToken(token);
    if (!user) {
      return res.status(401).json({ error: 'Invalid token' });
    }
    req.user = user;
    next();
  } catch (error) {
    logger.error(error);
    res.status(500).json({ error: 'Server error' });
  }
}

✅ Compressed (40 tokens):
```typescript
// authMiddleware: Extract token → validate → attach user to req
// Returns 401 if invalid, 500 on error
const token = req.headers.authorization?.split(' ')[1];
const user = await validateToken(token);
req.user = user;
```

Savings: 73%
```

### 2. Use Pseudocode
```
❌ Full implementation (200 tokens)

✅ Pseudocode (30 tokens):
```
function processPayment(order):
  1. Validate order amount
  2. Call Stripe API
  3. Update order status
  4. Send confirmation email
  return success/failure
```

Savings: 85%
```

### 3. Reference by Description
```
❌ Include entire config file (500 tokens)

✅ Reference (20 tokens):
"Database config: PostgreSQL on localhost:5432, pool size 20"

Savings: 96%
```

---

## Context Hierarchy

### Level 1: Critical (Always Include)
```
- Bug location (file + line)
- Error message
- Expected vs actual behavior
- Minimal reproduction code
```

### Level 2: Important (Include if space)
```
- Related functions
- Recent changes
- Test cases
- Dependencies
```

### Level 3: Nice-to-Have (Exclude if tight)
```
- Full file contents
- Documentation
- Comments
- Configuration
```

---

## Template Library

### Bug Fix Pack
```markdown
# Bug: [Title]

## Error
```
[Error message]
```

## Location
`file.ts:45` - [function name]

## Code
```typescript
[10-20 lines showing bug]
```

## Expected
[What should happen]

## Actual
[What happens now]
```

### Feature Request Pack
```markdown
# Feature: [Title]

## Goal
[One sentence]

## Current
[How it works now - 2-3 bullets]

## Proposed
[How it should work - 2-3 bullets]

## Files to Change
- `file1.ts`: [what to add]
- `file2.ts`: [what to modify]
```

### Code Review Pack
```markdown
# Review: [PR Title]

## Changes
- Added: [list]
- Modified: [list]
- Removed: [list]

## Key Code
[Show only changed functions]

## Questions
1. [Specific question about code]
2. [Another question]
```

---

## Best Practices

### 1. Start with Summary
```
First 50 words should answer:
- What is this about?
- What's the goal?
- What's the current state?
```

### 2. Show, Don't Tell
```
❌ "The authentication system uses JWT tokens"
✅ [Show the code that uses JWT]
```

### 3. Inline Context
```
✓ Add context in code comments
✓ Explain WHY, not WHAT
✓ Keep under 10 words per comment

Example:
```typescript
const token = jwt.sign(payload, SECRET, { 
  expiresIn: '1h'  // Short expiry for security
});
```
```

### 4. Use Line Numbers
```
✓ "See auth.ts:45-60"
✗ "See the validateToken function in the auth file"

Saves tokens, more precise
```

---

## Summary

**Context Pack:** Structured, compressed context format

**Format:**
- Summary (50 words)
- Key files (with line numbers)
- Code snippets (not full files)
- Current state (works/broken/goal)

**Compression:**
- Remove boilerplate (70%+ savings)
- Use pseudocode (85%+ savings)
- Reference by description (90%+ savings)

**Hierarchy:**
- Level 1: Critical (always)
- Level 2: Important (if space)
- Level 3: Nice-to-have (exclude)

**Target:**
- 50-70% size reduction
- Same or better clarity
- Faster AI comprehension
