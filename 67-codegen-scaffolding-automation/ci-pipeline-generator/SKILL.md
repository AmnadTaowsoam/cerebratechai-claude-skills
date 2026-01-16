---
name: CI Pipeline Generator
description: Generator สำหรับสร้าง CI/CD pipeline configs (GitHub Actions, GitLab CI) พร้อม testing, linting, building และ deployment
---

# CI Pipeline Generator

## Overview

สร้าง CI/CD pipeline configuration อัตโนมัติสำหรับ GitHub Actions, GitLab CI, หรือ Jenkins

## Why This Matters

- **Speed**: Pipeline พร้อมใช้ใน 1 นาที
- **Best practices**: Testing, linting, security scans
- **Consistency**: Same pipeline ทุก project
- **Complete**: Build, test, deploy ครบ

---

## Quick Start

```bash
# Generate GitHub Actions pipeline
npx generate-ci --platform github

# Output:
.github/workflows/
├── ci.yml          # PR checks
├── deploy.yml      # Deployment
└── release.yml     # Release automation
```

---

## Generated Pipeline

### GitHub Actions
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Lint
        run: npm run lint
      
      - name: Test
        run: npm test
      
      - name: Build
        run: npm run build
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Deployment Pipeline
```yaml
# .github/workflows/deploy.yml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      
      - name: Push to registry
        run: docker push myapp:${{ github.sha }}
      
      - name: Deploy to production
        run: kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
```

---

## Features

### Auto-generated Stages
```
1. Lint (ESLint, Prettier)
2. Test (Jest, coverage)
3. Security scan (npm audit)
4. Build (Docker)
5. Deploy (Kubernetes)
```

### Environment-specific
```bash
# Generate for staging
npx generate-ci --env staging

# Generate for production
npx generate-ci --env production
```

---

## Summary

**CI Pipeline Generator:** สร้าง CI/CD configs อัตโนมัติ

**Platforms:**
- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI

**Includes:**
- Lint + Test
- Build + Push
- Deploy
- Security scans

**Usage:**
```bash
npx generate-ci --platform github
git add .github/workflows/
git commit -m "Add CI pipeline"
```
