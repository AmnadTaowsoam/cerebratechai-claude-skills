# Skill Improvement Loop

## Overview

กระบวนการปรับปรุง Skills จากการใช้งานจริง เมื่อพบปัญหา ข้อผิดพลาด หรือวิธีที่ดีกว่าระหว่างพัฒนา สามารถ feedback กลับมาอัปเดต Skill ได้ทันที ทำให้ Skills พัฒนาขึ้นอย่างต่อเนื่องจากประสบการณ์จริง

---

## Feedback Loop Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    SKILL IMPROVEMENT LOOP                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐                │
│   │  1. USE  │────▶│ 2. FIND  │────▶│ 3. FIX   │                │
│   │  SKILL   │     │  ISSUE   │     │  CODE    │                │
│   └──────────┘     └──────────┘     └──────────┘                │
│        ▲                                  │                      │
│        │                                  ▼                      │
│   ┌──────────┐     ┌──────────┐     ┌──────────┐                │
│   │ 6. DONE  │◀────│ 5. COMMIT│◀────│ 4. UPDATE│                │
│   │          │     │  & PUSH  │     │  SKILL   │                │
│   └──────────┘     └──────────┘     └──────────┘                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Issue Categories

### Category 1: Bug / Error in Skill
Skill แนะนำ code ที่ไม่ทำงาน หรือมี error

```markdown
## Bug Report Template

**Skill**: [skill-name]
**Section**: [section ที่มีปัญหา]

### Problem
[อธิบายปัญหาที่เจอ]

### Code ที่ Skill แนะนำ
```[language]
// code จาก skill ที่มีปัญหา
```

### Error Message
```
[error message ที่ได้]
```

### Fixed Code
```[language]
// code ที่แก้ไขแล้ว
```

### Root Cause
[สาเหตุของปัญหา]
```

### Category 2: Outdated Pattern
Pattern ที่แนะนำล้าสมัยหรือมีวิธีที่ดีกว่า

```markdown
## Outdated Pattern Report

**Skill**: [skill-name]
**Section**: [section ที่ต้องอัปเดต]

### Current Pattern (Outdated)
```[language]
// pattern เดิมใน skill
```

### Better Pattern
```[language]
// pattern ใหม่ที่ดีกว่า
```

### Why Better?
- [ ] Performance improvement
- [ ] Better maintainability
- [ ] New API/Feature available
- [ ] Security improvement
- [ ] Other: [specify]

### Source/Reference
[link หรือ documentation ที่อ้างอิง]
```

### Category 3: Missing Information
Skill ขาดข้อมูลสำคัญที่ควรมี

```markdown
## Missing Information Report

**Skill**: [skill-name]
**Section**: [section ที่ควรเพิ่ม หรือ "New Section"]

### What's Missing
[อธิบายสิ่งที่ขาดหายไป]

### Why Important
[ทำไมข้อมูลนี้จึงสำคัญ]

### Suggested Content
```[language]
// code หรือ content ที่ควรเพิ่ม
```

### Real-world Scenario
[อธิบาย use case จริงที่ต้องใช้ข้อมูลนี้]
```

### Category 4: Environment-Specific Issue
Skill ไม่ work กับ environment บางอย่าง

```markdown
## Environment-Specific Issue

**Skill**: [skill-name]
**Environment**: [e.g., Vercel Serverless, Docker, AWS Lambda]

### Issue
[อธิบายปัญหาที่เจอใน environment นี้]

### Current Skill Recommendation
```[language]
// code ที่ skill แนะนำ
```

### Environment-Specific Fix
```[language]
// code ที่ใช้ได้กับ environment นี้
```

### Suggested Skill Update
- [ ] Add environment note
- [ ] Add alternative pattern
- [ ] Create separate section for this environment
```

---

## Quick Feedback Commands

### Command 1: Report Issue While Working

```
ระหว่างใช้ skill [skill-name] พบปัญหา:
- ปัญหา: [อธิบายสั้นๆ]
- แก้ไขโดย: [วิธีที่แก้ไขแล้ว]

ช่วยอัปเดต skill นี้ด้วย
```

### Command 2: Suggest Improvement

```
skill [skill-name] section [section-name]
น่าจะเพิ่มเรื่อง [topic] เพราะ [reason]
ตัวอย่าง code: [code snippet]

ช่วยอัปเดต skill ด้วย
```

### Command 3: Report Outdated Pattern

```
skill [skill-name] ใช้ pattern เก่า:
- เดิม: [old pattern]
- ใหม่: [new pattern]
- เหตุผล: [why better]

ช่วยอัปเดตให้เป็นแบบใหม่ด้วย
```

### Command 4: Add Real-world Example

```
skill [skill-name] ควรเพิ่ม real-world example:
- Scenario: [use case]
- Solution: [code]

ช่วยเพิ่มเข้าไปใน skill ด้วย
```

---

## Skill Update Process

### Step 1: Validate the Issue

ก่อนอัปเดต skill ต้องตรวจสอบ:

```markdown
## Validation Checklist

- [ ] Issue เกิดจาก skill จริงๆ (ไม่ใช่ user error)
- [ ] Fix ที่เสนอทำงานได้จริง
- [ ] Fix ไม่ทำให้ use case อื่นพัง
- [ ] Fix เป็น best practice ไม่ใช่ workaround
- [ ] มี reference/documentation รองรับ (ถ้าเป็น pattern ใหม่)
```

### Step 2: Determine Update Scope

```markdown
## Update Scope Decision

### Minor Update (แก้ไขเล็กน้อย)
- Typo fix
- Code syntax error
- Missing import statement
- Small clarification

### Moderate Update (เพิ่มเติมข้อมูล)
- Add new example
- Add environment-specific note
- Add warning/pitfall
- Expand existing section

### Major Update (เปลี่ยนแปลงสำคัญ)
- Change recommended pattern
- Deprecate old approach
- Add new section
- Restructure content
```

### Step 3: Update the Skill

```markdown
## Update Guidelines

### For Code Changes
1. ใส่ comment อธิบายว่าทำไมถึงเปลี่ยน
2. Keep old code as "❌ Avoid" example ถ้ามีประโยชน์
3. Add version/date note ถ้าเป็น breaking change

### For New Content
1. ใส่ในตำแหน่งที่เหมาะสม (ไม่ใช่แค่ต่อท้าย)
2. Follow existing format/style
3. Add cross-reference ถ้าเกี่ยวข้องกับ section อื่น

### For Deprecation
1. Mark old pattern clearly with ❌
2. Provide migration path
3. Explain why deprecated
```

---

## Real-world Examples

### Example 1: Prisma Connection Pooling Fix

**Scenario**: ใช้ skill `prisma-guide` ใน Vercel serverless แล้วเจอ connection limit error

**Report**:
```
skill prisma-guide พบปัญหากับ Vercel serverless:
- ปัญหา: Connection pool exhausted error
- Environment: Vercel Edge Functions
- แก้ไขโดย: เพิ่ม pgbouncer และ connection_limit=1

ช่วยเพิ่มเรื่อง serverless connection handling ใน skill ด้วย
```

**Skill Update**:
```typescript
// ✅ Serverless-friendly connection (Added from real-world usage)
// Note: Standard pooling doesn't work well with serverless

const prisma = new PrismaClient({
  datasources: {
    db: {
      url: process.env.DATABASE_URL + '?pgbouncer=true&connection_limit=1'
    }
  }
})

// For Vercel/Netlify/AWS Lambda
export const prismaClientSingleton = () => {
  return new PrismaClient({
    log: process.env.NODE_ENV === 'development' ? ['query'] : [],
  })
}

declare global {
  var prisma: undefined | ReturnType<typeof prismaClientSingleton>
}

export const db = globalThis.prisma ?? prismaClientSingleton()

if (process.env.NODE_ENV !== 'production') globalThis.prisma = db
```

### Example 2: Next.js API Route Error Handling

**Scenario**: ใช้ skill `nextjs-patterns` แล้วพบว่า error handling ไม่ครอบคลุม edge cases

**Report**:
```
skill nextjs-patterns section API Routes:
- ขาด handling สำหรับ Zod validation errors
- ขาด proper error response format
- เพิ่ม code ที่ใช้จริงแล้ว work ดี

ช่วยอัปเดต skill ด้วย
```

**Skill Update**:
```typescript
// ✅ Complete error handling (Updated from production usage)

import { NextRequest, NextResponse } from 'next/server'
import { ZodError } from 'zod'

type ApiHandler = (req: NextRequest) => Promise<NextResponse>

export function withErrorHandling(handler: ApiHandler): ApiHandler {
  return async (req: NextRequest) => {
    try {
      return await handler(req)
    } catch (error) {
      // Zod validation errors
      if (error instanceof ZodError) {
        return NextResponse.json(
          {
            error: 'Validation Error',
            details: error.errors.map(e => ({
              field: e.path.join('.'),
              message: e.message
            }))
          },
          { status: 400 }
        )
      }

      // Known application errors
      if (error instanceof AppError) {
        return NextResponse.json(
          { error: error.message, code: error.code },
          { status: error.statusCode }
        )
      }

      // Unknown errors
      console.error('Unhandled error:', error)
      return NextResponse.json(
        { error: 'Internal Server Error' },
        { status: 500 }
      )
    }
  }
}
```

### Example 3: Adding Missing TypeScript Pattern

**Scenario**: skill `typescript-standards` ขาดเรื่อง discriminated unions ที่ใช้บ่อยมาก

**Report**:
```
skill typescript-standards ควรเพิ่ม discriminated unions:
- เป็น pattern ที่ใช้บ่อยมากใน production
- ช่วยให้ type-safe มากขึ้น
- ตัวอย่าง: API response handling, state management

ช่วยเพิ่มเข้าไปใน skill ด้วย
```

**Skill Update**:
```typescript
// ✅ Discriminated Unions (Added from common production patterns)

// API Response Pattern
type ApiResponse<T> =
  | { status: 'success'; data: T }
  | { status: 'error'; error: string; code: number }
  | { status: 'loading' }

function handleResponse<T>(response: ApiResponse<T>) {
  switch (response.status) {
    case 'success':
      return response.data // TypeScript knows data exists
    case 'error':
      throw new Error(response.error) // TypeScript knows error exists
    case 'loading':
      return null
  }
}

// Form State Pattern
type FormState =
  | { step: 'input'; data: Partial<FormData> }
  | { step: 'review'; data: FormData }
  | { step: 'submitted'; confirmationId: string }

function FormWizard({ state }: { state: FormState }) {
  switch (state.step) {
    case 'input':
      return <InputForm initialData={state.data} />
    case 'review':
      return <ReviewForm data={state.data} /> // data is complete here
    case 'submitted':
      return <Confirmation id={state.confirmationId} />
  }
}
```

---

## Tracking Skill Changes

### Change Log Format

เมื่ออัปเดต skill ให้เพิ่ม change log ที่ท้าย skill:

```markdown
---

## Changelog

### 2026-01-15
- Added serverless connection handling for Vercel/Netlify
- Source: Production issue with connection pooling

### 2026-01-10
- Updated error handling pattern with Zod support
- Source: Real-world API development feedback

### 2026-01-05
- Added discriminated unions section
- Source: Common pattern identified from multiple projects
```

### Git Commit Convention

```bash
# For bug fixes
git commit -m "fix(prisma-guide): add serverless connection handling

- Added pgbouncer configuration for serverless
- Added singleton pattern for edge functions
- Source: Production issue in Vercel deployment"

# For improvements
git commit -m "feat(typescript-standards): add discriminated unions

- Added API response pattern
- Added form state pattern
- Source: Common pattern from production projects"

# For deprecations
git commit -m "refactor(nextjs-patterns): deprecate pages router examples

- Marked Pages Router patterns as legacy
- Added migration guide to App Router
- Source: Next.js 14+ best practices"
```

---

## Automation Ideas

### GitHub Issue Template

สร้างไฟล์ `.github/ISSUE_TEMPLATE/skill-feedback.md`:

```markdown
---
name: Skill Feedback
about: Report issues or suggest improvements for skills
title: '[SKILL] '
labels: skill-improvement
---

## Skill Name
<!-- ชื่อ skill ที่ต้องการ feedback -->

## Feedback Type
- [ ] Bug/Error in code example
- [ ] Outdated pattern
- [ ] Missing information
- [ ] Environment-specific issue
- [ ] General improvement

## Description
<!-- อธิบายปัญหาหรือข้อเสนอแนะ -->

## Current Content
```
<!-- code หรือ content ปัจจุบันที่มีปัญหา -->
```

## Suggested Change
```
<!-- code หรือ content ที่แนะนำ -->
```

## Real-world Context
<!-- อธิบาย use case จริงที่ทำให้พบปัญหานี้ -->

## Additional Notes
<!-- ข้อมูลเพิ่มเติม -->
```

### CI Check for Skill Quality

```yaml
# .github/workflows/skill-quality.yml
name: Skill Quality Check

on:
  pull_request:
    paths:
      - '**/SKILL.md'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Check skill structure
        run: |
          for file in $(find . -name "SKILL.md"); do
            echo "Checking $file"

            # Must have Overview section
            grep -q "## Overview" "$file" || echo "Missing Overview in $file"

            # Must have code examples
            grep -q '```' "$file" || echo "No code examples in $file"

            # Check for changelog (recommended)
            grep -q "## Changelog" "$file" || echo "Consider adding Changelog to $file"
          done
```

---

## Best Practices

### Do's

- [ ] Report issues ทันทีที่พบ (อย่ารอ)
- [ ] ให้ context ครบ (environment, version, use case)
- [ ] Test fix ก่อน suggest
- [ ] ใช้ format ที่กำหนดให้ feedback ชัดเจน
- [ ] Add changelog เมื่ออัปเดต skill
- [ ] Cross-reference กับ skills อื่นที่เกี่ยวข้อง

### Don'ts

- [ ] อย่า report ปัญหาที่เกิดจาก user error
- [ ] อย่า suggest workaround แทน proper fix
- [ ] อย่าลบ content เดิมโดยไม่มีเหตุผล (mark as deprecated แทน)
- [ ] อย่าเพิ่ม content ที่ไม่ได้ test
- [ ] อย่าเปลี่ยน pattern โดยไม่อธิบายว่าทำไม

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────────┐
│              SKILL FEEDBACK QUICK REFERENCE                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  🐛 Bug:      "skill [name] มี bug: [desc] แก้โดย [fix]"    │
│                                                              │
│  📝 Missing:  "skill [name] ควรเพิ่ม [topic] เพราะ [why]"   │
│                                                              │
│  🔄 Outdated: "skill [name] pattern เก่า ใหม่คือ [new]"     │
│                                                              │
│  🌍 Env:      "skill [name] ไม่ work กับ [env] แก้โดย [fix]"│
│                                                              │
│  ✨ Example:  "skill [name] ควรเพิ่ม example: [scenario]"   │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  After reporting: Claude will update the skill and commit   │
└─────────────────────────────────────────────────────────────┘
```

---

## Checklist

เมื่อต้องการ feedback skill:

- [ ] ระบุชื่อ skill ที่ต้องการ feedback
- [ ] ระบุประเภท feedback (bug/missing/outdated/env)
- [ ] อธิบายปัญหาหรือข้อเสนอแนะ
- [ ] ให้ code ตัวอย่างที่ใช้ได้จริง
- [ ] อธิบาย context (environment, use case)
- [ ] Test ก่อน suggest (ถ้าเป็นไปได้)

---

Format: Markdown with templates and examples.

Create the file now.
