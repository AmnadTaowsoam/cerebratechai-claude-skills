---
name: Lint, Test, Typecheck Policy
description: Policy สำหรับ enforce code quality ผ่าน linting, testing, และ type checking ใน CI pipeline
---

# Lint, Test, Typecheck Policy

## Overview

Policy สำหรับ enforce code quality standards ผ่าน automated checks: linting, testing, type checking - ต้องผ่านทุกอย่างก่อน merge

## Why This Matters

- **Quality**: จับ bugs ก่อนถึง production
- **Consistency**: Code style เหมือนกันทั้ง team
- **Safety**: Type errors จับได้ตั้งแต่ compile time
- **Automated**: ไม่ต้องพึ่ง manual review

---

## Three Pillars

### 1. Lint (Code Style)
```bash
# Must pass
npm run lint

# Zero errors, zero warnings
✓ 0 errors
✓ 0 warnings
```

### 2. Test (Correctness)
```bash
# Must pass
npm test

# All tests pass, coverage ≥80%
✓ 150 tests passing
✓ Coverage: 85%
```

### 3. Typecheck (Type Safety)
```bash
# Must pass
npm run typecheck

# Zero type errors
✓ 0 errors
```

---

## CI Pipeline

```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates
on: [pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      
      - name: Install
        run: npm ci
      
      - name: Lint
        run: npm run lint
        # Fails on any error/warning
      
      - name: Type Check
        run: npm run typecheck
        # Fails on any type error
      
      - name: Test
        run: npm test -- --coverage
        # Fails if coverage < 80%
      
      - name: Upload Coverage
        uses: codecov/codecov-action@v3
```

---

## Lint Configuration

### ESLint
```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:@typescript-eslint/recommended-requiring-type-checking',
  ],
  rules: {
    // Errors (must fix)
    'no-console': 'error',
    'no-debugger': 'error',
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-unused-vars': 'error',
    
    // Warnings (should fix)
    'complexity': ['warn', 10],
    'max-lines': ['warn', 300],
  }
};
```

### Prettier
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

---

## Test Policy

### Coverage Requirements
```json
{
  "jest": {
    "coverageThreshold": {
      "global": {
        "branches": 80,
        "functions": 80,
        "lines": 80,
        "statements": 80
      }
    }
  }
}
```

### Test Types Required
```
✓ Unit tests (all functions)
✓ Integration tests (critical paths)
✓ E2E tests (user flows)
```

---

## TypeScript Configuration

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true
  }
}
```

---

## Pre-commit Hooks

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.ts": [
      "eslint --fix",
      "prettier --write",
      "npm run typecheck"
    ],
    "*.test.ts": [
      "npm test -- --findRelatedTests"
    ]
  }
}
```

---

## Summary

**Quality Gates:** Lint + Test + Typecheck ต้องผ่านทั้งหมด

**Requirements:**
- Lint: 0 errors, 0 warnings
- Test: All pass, ≥80% coverage
- Typecheck: 0 type errors

**Enforcement:**
- CI pipeline (blocks merge)
- Pre-commit hooks (local)
- Code review (manual check)

**No exceptions:** ต้องผ่านทุกอย่าง
