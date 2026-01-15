# CI/CD GitHub Actions

## Overview

GitHub Actions is a CI/CD platform that automates your build, test, and deployment workflows. This skill covers workflow syntax, common patterns, and production configurations.

## Table of Contents

1. [GitHub Actions Basics](#github-actions-basics)
2. [Workflow Syntax](#workflow-syntax)
3. [Common Workflows](#common-workflows)
4. [Matrix Builds](#matrix-builds)
5. [Caching](#caching)
6. [Secrets Management](#secrets-management)
7. [Environments](#environments)
8. [Deployment Strategies](#deployment-strategies)
9. [Monorepo Support](#monorepo-support)
10. [Reusable Workflows](#reusable-workflows)
11. [Security Best Practices](#security-best-practices)
12. [Production Examples](#production-examples)

---

## GitHub Actions Basics

### Workflow File Location

```
.github/
└── workflows/
    ├── ci.yml
    ├── deploy.yml
    └── release.yml
```

### Trigger Events

```yaml
name: CI

# Trigger on push
on:
  push:
    branches: [main, develop]

# Trigger on pull request
on:
  pull_request:
    branches: [main]

# Trigger on schedule
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

# Trigger on manual dispatch
on:
  workflow_dispatch:

# Multiple triggers
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
```

### Jobs and Steps

```yaml
name: CI

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test
```

---

## Workflow Syntax

### Basic Structure

```yaml
name: My Workflow

on: push

permissions:
  contents: read

env:
  NODE_ENV: production

jobs:
  job1:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: echo "Hello World"
```

### Job Dependencies

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm run build

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm test
```

### Job Outputs

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - id: version
        run: echo "version=$(node -p 'require(\"./package.json\").version')" >> $GITHUB_OUTPUT

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying version ${{ needs.build.outputs.version }}"
```

### Conditional Steps

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build
        run: npm run build

      - name: Deploy
        if: github.ref == 'refs/heads/main'
        run: npm run deploy
```

---

## Common Workflows

### Test on PR

```yaml
name: Test

on:
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Build and Deploy

```yaml
name: Build and Deploy

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: dist
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v3
        with:
          name: dist

      - name: Deploy to S3
        uses: jakejarvis/s3-deploy-action@v0.0.5
        with:
          args: --acl public-read --delete
          source: dist
          region: ${{ secrets.AWS_REGION }}
          bucket: ${{ secrets.AWS_S3_BUCKET }}
          aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

### Docker Build and Push

```yaml
name: Docker Build and Push

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: myorg/myapp
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha,prefix={{branch}}-

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

---

## Matrix Builds

### Node.js Matrix

```yaml
name: Test Matrix

on: push

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
        os: [ubuntu-latest, windows-latest, macos-latest]
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test
```

### Python Matrix

```yaml
name: Test Matrix

on: push

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

### Exclude Matrix Values

```yaml
name: Test Matrix

on: push

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
        os: [ubuntu-latest, windows-latest]
        exclude:
          - os: windows-latest
            node-version: 16
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

---

## Caching

### Node.js Dependencies Cache

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

### Python Dependencies Cache

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Cache pip
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: pip install -r requirements.txt
```

### Docker Layer Cache

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Cache Docker layers
        uses: actions/cache@v3
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      - name: Build and push
        uses: docker/build-push-action@v4
        with:
          context: .
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache-new
```

---

## Secrets Management

### Using Secrets

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
        run: npm run deploy
```

### Encrypted Secrets

```bash
# Encrypt secret
gpg --symmetric --cipher-algo AES256 secret.txt > secret.txt.gpg

# Add to repository
git add secret.txt.gpg
git commit -m "Add encrypted secret"
git push
```

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Decrypt secret
        run: |
          gpg --quiet --batch --yes --decrypt --passphrase="${{ secrets.GPG_PASSPHRASE }}" \
            secret.txt.gpg > secret.txt

      - name: Use secret
        run: cat secret.txt
```

---

## Environments

### Environment Protection Rules

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v3
      - run: npm run deploy
```

### Environment Secrets

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v3
      - name: Deploy
        env:
          PRODUCTION_API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
        run: npm run deploy
```

---

## Deployment Strategies

### Blue-Green Deployment

```yaml
name: Blue-Green Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production
    steps:
      - uses: actions/checkout@v3

      - name: Deploy to green
        run: |
          kubectl apply -f k8s-green.yaml
          kubectl wait --for=condition=available --timeout=60s deployment/myapp-green

      - name: Switch traffic
        run: kubectl patch service myapp -p '{"spec":{"selector":{"version":"green"}}}'
```

### Canary Deployment

```yaml
name: Canary Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: production-canary
    steps:
      - uses: actions/checkout@v3

      - name: Deploy canary
        run: |
          kubectl apply -f k8s-canary.yaml
          kubectl wait --for=condition=available --timeout=60s deployment/myapp-canary
```

---

## Monorepo Support

### Path Filtering

```yaml
name: Monorepo CI

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Detect changed packages
        id: changes
        run: |
          git diff --name-only ${{ github.event.before }} ${{ github.sha }} > changed.txt
          echo "packages=$(cat changed.txt | grep '^packages/' | cut -d'/' -f2 | sort -u | tr '\n' ',')" >> $GITHUB_OUTPUT

      - name: Test changed packages
        run: |
          for pkg in ${{ steps.changes.outputs.packages }}; do
            cd packages/$pkg
            npm test
          done
```

### Turborepo

```yaml
name: Turborepo CI

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npx turbo run build --filter=...^main
```

---

## Reusable Workflows

### Create Reusable Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image:
        required: true
        type: string

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy
        run: |
          echo "Deploying ${{ inputs.image }} to ${{ inputs.environment }}"
```

### Call Reusable Workflow

```yaml
# .github/workflows/ci.yml
name: CI

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build
        run: npm run build

      - name: Deploy to staging
        uses: ./.github/workflows/deploy.yml
        with:
          environment: staging
          image: myapp:latest

      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        uses: ./.github/workflows/deploy.yml
        with:
          environment: production
          image: myapp:latest
```

---

## Security Best Practices

### Pin Action Versions

```yaml
# Good: Pin specific versions
- uses: actions/checkout@v3
- uses: actions/setup-node@v3

# Bad: Use @latest
- uses: actions/checkout@latest
- uses: actions/setup-node@latest
```

### Use OIDC for AWS

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Deploy to S3
        run: aws s3 sync dist/ s3://my-bucket/
```

### Scan for Vulnerabilities

```yaml
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

---

## Production Examples

### Production Deployment

```yaml
name: Production Deploy

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Run linter
        run: npm run lint

      - name: Build
        run: npm run build

  deploy:
    needs: test
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://example.com
    steps:
      - uses: actions/checkout@v3

      - name: Download artifacts
        uses: actions/download-artifact@v3
        with:
          name: dist

      - name: Deploy to AWS
        uses: aws-actions/configure-aws-credentials@v1
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Deploy to S3
        run: aws s3 sync dist/ s3://my-bucket/ --delete

      - name: Invalidate CloudFront
        run: |
          DISTRIBUTION_ID=${{ secrets.CLOUDFRONT_DISTRIBUTION_ID }}
          aws cloudfront create-invalidation \
            --distribution-id $DISTRIBUTION_ID \
            --paths "/*"

      - name: Notify Slack
        uses: slackapi/slack-github-action@v1.24.0
        with:
          payload: |
            {
              "text": "Production deployment successful!"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

---

## Summary

This skill covers comprehensive CI/CD with GitHub Actions including:

- **GitHub Actions Basics**: Workflow file location, trigger events, jobs and steps
- **Workflow Syntax**: Basic structure, job dependencies, job outputs, conditional steps
- **Common Workflows**: Test on PR, build and deploy, Docker build and push
- **Matrix Builds**: Node.js matrix, Python matrix, exclude matrix values
- **Caching**: Node.js dependencies, Python dependencies, Docker layer cache
- **Secrets Management**: Using secrets, encrypted secrets
- **Environments**: Environment protection rules, environment secrets
- **Deployment Strategies**: Blue-green deployment, canary deployment
- **Monorepo Support**: Path filtering, Turborepo
- **Reusable Workflows**: Create and call reusable workflows
- **Security Best Practices**: Pin action versions, OIDC for AWS, vulnerability scanning
- **Production Examples**: Production deployment with testing, AWS S3, CloudFront, Slack notifications
