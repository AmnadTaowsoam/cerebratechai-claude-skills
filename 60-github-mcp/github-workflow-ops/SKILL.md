# GitHub Workflow Operations

## Overview

GitHub workflow operations cover the management, optimization, and troubleshooting of GitHub Actions workflows. This skill includes workflow design, CI/CD pipelines, automation patterns, and best practices for reliable and efficient workflows.

**When to use this skill:** When creating, maintaining, or troubleshooting GitHub Actions workflows.

## Table of Contents

1. [Workflow Fundamentals](#workflow-fundamentals)
2. [Workflow Design Patterns](#workflow-design-patterns)
3. [CI/CD Pipelines](#cicd-pipelines)
4. [Workflow Optimization](#workflow-optimization)
5. [Troubleshooting](#troubleshooting)
6. [Workflow Checklist](#workflow-checklist)
7. [Quick Reference](#quick-reference)

---

## Workflow Fundamentals

### Workflow Structure

```yaml
# .github/workflows/workflow-name.yml
name: Workflow Name

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * *'

jobs:
  job-name:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run script
        run: echo "Hello World"
```

### Workflow Triggers

| Trigger | Description | Example |
|---------|-------------|----------|
| `push` | Code pushed | `on: push: branches: [main]` |
| `pull_request` | PR created/updated | `on: pull_request` |
| `schedule` | Cron schedule | `on: schedule: - cron: '0 0 * * *'` |
| `workflow_dispatch` | Manual trigger | `on: workflow_dispatch` |
| `release` | Release published | `on: release: types: [created]` |
| `issue_comment` | Comment on issue | `on: issue_comment` |

### Workflow Events

```yaml
on:
  # Multiple triggers
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        default: 'production'

  # Conditional triggers
  push:
    branches:
      - main
      - 'releases/**'
    paths:
      - 'src/**'
      - '.github/workflows/**'
```

---

## Workflow Design Patterns

### Matrix Strategy

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [14, 16, 18]
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

### Conditional Jobs

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Building..."

  deploy:
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    steps:
      - run: echo "Deploying..."
```

### Reusable Workflows

```yaml
# .github/workflows/reusable.yml
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      api-key:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to ${{ inputs.environment }}"
```

### Calling Reusable Workflow

```yaml
# .github/workflows/main.yml
jobs:
  deploy-prod:
    uses: ./.github/workflows/reusable.yml
    with:
      environment: production
    secrets:
      api-key: ${{ secrets.PROD_API_KEY }}

  deploy-staging:
    uses: ./.github/workflows/reusable.yml
    with:
      environment: staging
    secrets:
      api-key: ${{ secrets.STAGING_API_KEY }}
```

---

## CI/CD Pipelines

### CI Pipeline

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm ci
      - name: Run linter
        run: npm run lint

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm ci
      - name: Run tests
        run: npm test
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    runs-on: ubuntu-latest
    needs: [lint, test]
    steps:
      - uses: actions/checkout@v3
      - name: Build
        run: npm run build
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/
```

### CD Pipeline

```yaml
name: CD Pipeline

on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: build

      - name: Deploy to production
        run: |
          echo "Deploying to production..."
          # Deployment commands here
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
```

### Environment-Specific Deployment

```yaml
jobs:
  deploy-staging:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment:
      name: staging
      url: https://staging.example.com
    steps:
      - run: echo "Deploy to staging"

  deploy-production:
    runs-on: ubuntu-latest
    if: startsWith(github.ref, 'refs/tags/v')
    environment:
      name: production
      url: https://example.com
    steps:
      - run: echo "Deploy to production"
```

---

## Workflow Optimization

### Caching Strategy

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Cache node modules
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-node-

      - name: Install dependencies
        run: npm ci
```

### Parallel Execution

```yaml
jobs:
  test-unit:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:unit

  test-integration:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:integration

  test-e2e:
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:e2e

  report:
    runs-on: ubuntu-latest
    needs: [test-unit, test-integration, test-e2e]
    steps:
      - run: echo "All tests passed"
```

### Artifact Management

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Build
        run: npm run build

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: application
          path: dist/
          retention-days: 30

  deploy:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: application
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|--------|--------|----------|
| **Workflow not triggering** | Wrong path or event | Check `.github/workflows/` path |
| **Permissions error** | Missing token | Add `GITHUB_TOKEN` |
| **Cache miss** | Wrong cache key | Verify cache key format |
| **Secret not found** | Not added to repo | Add in Settings > Secrets |
| **Timeout** | Job too long | Optimize or increase timeout |
| **Flaky tests** | Race condition | Add retries or isolation |

### Debugging Workflows

```yaml
jobs:
  debug:
    runs-on: ubuntu-latest
    steps:
      - name: Enable debug logging
        run: |
          echo "Runner OS: ${{ runner.os }}"
          echo "Event name: ${{ github.event_name }}"
          echo "Ref: ${{ github.ref }}"
          echo "Actor: ${{ github.actor }}"

      - name: List files
        run: ls -la

      - name: Environment variables
        run: env | sort
```

### Workflow Logs

```bash
# View workflow runs
gh run list

# View specific run
gh run view 123

# View workflow logs
gh run view 123 --log

# Download logs
gh run download 123

# Rerun workflow
gh run rerun 123
```

---

## Workflow Checklist

### Workflow Creation

```markdown
## Workflow Creation Checklist

### Design
- [ ] Purpose defined
- [ ] Triggers identified
- [ ] Jobs planned
- [ ] Dependencies mapped
- [ ] Artifacts defined

### Implementation
- [ ] Workflow file created
- [ ] Syntax validated
- [ ] Secrets configured
- [ ] Permissions set
- [ ] Caching configured

### Testing
- [ ] Workflow tested manually
- [ ] All jobs pass
- [ ] Artifacts uploaded
- [ ] Logs reviewed
- [ ] Performance acceptable
```

### Workflow Maintenance

```markdown
## Workflow Maintenance Checklist

### Regular Review
- [ ] Workflow usage reviewed
- [ ] Failed runs analyzed
- [ ] Performance monitored
- [ ] Dependencies updated
- [ ] Secrets rotated

### Optimization
- [ ] Caching effective
- [ ] Parallel jobs optimized
- [ ] Artifacts managed
- [ ] Timeout settings reviewed
- [ ] Resource usage monitored

### Documentation
- [ ] Workflow documented
- [ ] Triggers explained
- [ ] Secrets documented
- [ ] Troubleshooting guide updated
- [ ] Runbook created
```

---

## Quick Reference

### GitHub CLI Commands

```bash
# List workflows
gh workflow list

# View workflow
gh workflow view workflow-name.yml

# Run workflow manually
gh workflow run workflow-name.yml

# List workflow runs
gh run list --workflow=workflow-name.yml

# View run details
gh run view 123

# Rerun failed jobs
gh run rerun 123

# Cancel workflow
gh run cancel 123

# View logs
gh run view 123 --log
```

### Workflow Syntax

```yaml
# Common patterns
on: push: branches: [main]           # Push to main
on: schedule: - cron: '0 0 * * *'   # Daily at midnight
on: workflow_dispatch                    # Manual trigger
if: github.ref == 'refs/heads/main'  # Conditional
needs: [build, test]                 # Job dependency
runs-on: ubuntu-latest                   # Runner OS
timeout-minutes: 30                     # Job timeout
```

### Workflow Metrics

| Metric | Target | How to Track |
|--------|--------|----------------|
| **Success rate** | > 95% | Successful runs / total runs |
| **Average duration** | < 10 min | Workflow run time |
| **Cache hit rate** | > 80% | Cache effectiveness |
| **Artifact usage** | Managed | Storage usage |
| **Cost** | Within budget | Minutes used × cost |

---

## Common Pitfalls

1. **Hardcoded values** - Use environment variables and secrets
2. **No caching** - Cache dependencies to speed up builds
3. **Long-running jobs** - Optimize or split into smaller jobs
4. **Ignoring failures** - Monitor and fix failed workflows
5. **No logging** - Add debug logging for troubleshooting
6. **Secret exposure** - Never log secrets or use in PRs
7. **Not using matrix** - Use matrix for parallel testing
8. **Missing cleanup** - Clean up old artifacts and cache

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Workflow Examples](https://github.com/actions/starter-workflows)
