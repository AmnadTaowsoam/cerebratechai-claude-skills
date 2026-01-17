---
name: Lint, Format, and Type Check
description: Automated code quality enforcement through linting, formatting, and type checking to maintain consistent, error-free codebases.
---

# Lint, Format, and Type Check

## Overview

Linting, formatting, and type checking are automated code quality tools that catch errors, enforce style consistency, and improve code maintainability before code reaches production.

**Core Principle**: "Automate code quality checks so humans can focus on logic, not syntax."

---

## 1. The Three Pillars of Code Quality Automation

| Tool Type | Purpose | Example Tools |
|-----------|---------|---------------|
| **Linter** | Find bugs, code smells, and enforce best practices | ESLint, Pylint, RuboCop |
| **Formatter** | Enforce consistent code style automatically | Prettier, Black, gofmt |
| **Type Checker** | Catch type errors before runtime | TypeScript, mypy, Flow |

---

## 2. Linting

### ESLint (JavaScript/TypeScript)
```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended"
  ],
  "rules": {
    "no-console": "warn",
    "no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "error",
    "react/prop-types": "off"
  }
}
```

### Pylint (Python)
```ini
# .pylintrc
[MESSAGES CONTROL]
disable=missing-docstring,too-few-public-methods

[FORMAT]
max-line-length=100

[BASIC]
good-names=i,j,k,x,y,z,df,db
```

### Running Linters
```bash
# JavaScript/TypeScript
npx eslint . --ext .ts,.tsx

# Python
pylint src/

# Auto-fix where possible
npx eslint . --fix
```

---

## 3. Formatting

### Prettier (JavaScript/TypeScript)
```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5",
  "printWidth": 100
}
```

### Black (Python)
```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py39']
include = '\.pyi?$'
```

### Running Formatters
```bash
# Prettier
npx prettier --write .

# Black
black .

# Check without modifying
npx prettier --check .
black --check .
```

---

## 4. Type Checking

### TypeScript
```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

### mypy (Python)
```ini
# mypy.ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

### Running Type Checkers
```bash
# TypeScript
tsc --noEmit

# Python mypy
mypy src/
```

---

## 5. Pre-commit Hooks

Enforce checks before code is committed using **Husky** (JS) or **pre-commit** (Python).

### Husky (JavaScript/TypeScript)
```json
// package.json
{
  "scripts": {
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
#!/bin/sh
npx lint-staged
npm run type-check
```

### pre-commit (Python)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/pylint
    rev: v3.0.0
    hooks:
      - id: pylint
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.0.0
    hooks:
      - id: mypy
```

---

## 6. CI/CD Integration

```yaml
# .github/workflows/code-quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  lint-format-typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Format check
        run: npm run format:check
      
      - name: Type check
        run: npm run type-check
```

---

## 7. IDE Integration

### VS Code Settings
```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "eslint.validate": [
    "javascript",
    "typescript",
    "typescriptreact"
  ],
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

---

## 8. Common Linting Rules

### Security Rules
```javascript
// Prevent security issues
{
  "no-eval": "error",
  "no-implied-eval": "error",
  "no-new-func": "error",
  "no-script-url": "error"
}
```

### Performance Rules
```javascript
{
  "no-await-in-loop": "warn",
  "require-atomic-updates": "error"
}
```

### Best Practices
```javascript
{
  "eqeqeq": ["error", "always"],
  "no-var": "error",
  "prefer-const": "error",
  "prefer-arrow-callback": "warn"
}
```

---

## 9. Progressive Adoption

### Start Permissive, Tighten Over Time
```json
// Week 1: Warnings only
{
  "rules": {
    "no-console": "warn",
    "@typescript-eslint/no-explicit-any": "warn"
  }
}

// Week 4: Errors
{
  "rules": {
    "no-console": "error",
    "@typescript-eslint/no-explicit-any": "error"
  }
}
```

---

## 10. Lint, Format, Type Check Checklist

- [ ] **Linter Configured**: ESLint/Pylint with team-agreed rules?
- [ ] **Formatter Configured**: Prettier/Black with consistent settings?
- [ ] **Type Checker**: TypeScript/mypy enabled with strict mode?
- [ ] **Pre-commit Hooks**: Automated checks before commit?
- [ ] **CI Integration**: Checks run on every PR?
- [ ] **IDE Integration**: Auto-format on save enabled?
- [ ] **Documentation**: Rules documented for team?
- [ ] **Gradual Adoption**: New rules introduced incrementally?

---

## Related Skills
- `45-developer-experience/commit-conventions`
- `45-developer-experience/code-review-standards`
- `45-developer-experience/local-dev-standard`
