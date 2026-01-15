# CI/CD with GitHub Actions

A comprehensive guide to CI/CD pipelines using GitHub Actions.

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

### Key Concepts

```
┌─────────────────────────────────────────────────────────────┐
│                   GitHub Actions Workflow                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Trigger   │──>│   Jobs     │──>│   Actions   │      │
│  │  (push/PR)  │  │  (steps)   │  │  (deploy)  │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│                                                             │
│  Workflow = YAML file in .github/workflows/              │
│  Job = Collection of steps                                │
│  Step = Individual command or action                       │
│  Runner = Server that executes the workflow               │
└─────────────────────────────────────────────────────────────┘
```

### Workflow File Location

```
myapp/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       └── deploy.yml
├── src/
└── package.json
```

### Basic Workflow Structure

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run tests
        run: npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build application
        run: npm run build
```

---

## Workflow Syntax

### Triggers

```yaml
# Push to specific branches
on:
  push:
    branches:
      - main
      - develop
      - 'feature/**'

# Pull request to main
on:
  pull_request:
    branches:
      - main

# Manual trigger
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Environment to deploy'
        required: true
        type: choice
        options:
          - staging
          - production

# Schedule (cron)
on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight

# Multiple triggers
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

# Tag push
on:
  push:
    tags:
      - 'v*'

# Release
on:
  release:
    types: [published]
```

### Jobs

```yaml
jobs:
  # Single job
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm test

  # Job with dependencies
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: npm run build

  # Job with conditions
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - run: npm run deploy

  # Job with matrix
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
        os: [ubuntu-latest, windows-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
      - run: npm test
```

### Steps

```yaml
jobs:
  example:
    runs-on: ubuntu-latest
    steps:
      # Checkout code
      - name: Checkout
        uses: actions/checkout@v4

      # Set up Node.js
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      # Install dependencies
      - name: Install dependencies
        run: npm ci

      # Run tests
      - name: Run tests
        run: npm test

      # Run custom script
      - name: Run custom script
        run: |
          echo "Running custom script"
          npm run custom:script

      # Use environment variables
      - name: Use environment
        env:
          MY_VAR: ${{ secrets.MY_SECRET }}
        run: echo $MY_VAR

      # Conditional step
      - name: Conditional step
        if: github.event_name == 'pull_request'
        run: echo "This is a PR"

      # Continue on error
      - name: Continue on error
        continue-on-error: true
        run: npm run lint
```

---

## Common Workflows

### Test on PR

```yaml
name: Test

on:
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info
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
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build application
        run: npm run build

      - name: Upload build artifacts
        uses: actions/upload-artifact@v3
        with:
          name: build
          path: dist/

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment: production

    steps:
      - name: Download build artifacts
        uses: actions/download-artifact@v3
        with:
          name: build

      - name: Deploy to production
        run: |
          # Your deployment commands
          echo "Deploying to production"
```

### Docker Build and Push

```yaml
name: Docker Build and Push

on:
  push:
    branches: [main]
    tags:
      - 'v*'

jobs:
  docker:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: myapp/myapp
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

---

## Matrix Builds

### Node.js Version Matrix

```yaml
name: Test Matrix

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16, 18, 20]
        os: [ubuntu-latest, windows-latest, macos-latest]
        exclude:
          - os: macos-latest
            node-version: 16

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test
```

### Python Version Matrix

```yaml
name: Test Matrix

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']
        django-version: ['4.1', '4.2']

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install django==${{ matrix.django-version }}
          pip install -r requirements.txt

      - name: Run tests
        run: pytest
```

### Fail-Fast Strategy

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false  # Continue even if one job fails
      matrix:
        node-version: [16, 18, 20]

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}

      - name: Run tests
        run: npm test
```

---

## Caching

### NPM Cache

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'  # Automatic caching

      - name: Install dependencies
        run: npm ci
```

### Custom Cache

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

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

### Docker Layer Cache

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build with cache
        uses: docker/build-push-action@v5
        with:
          context: .
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Python Cache

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'  # Automatic caching

      - name: Install dependencies
        run: pip install -r requirements.txt
```

---

## Secrets Management

### Using Secrets

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Use secret
        env:
          MY_SECRET: ${{ secrets.MY_SECRET }}
        run: echo "Secret is $MY_SECRET"

      - name: Deploy with secret
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          # Deployment commands
```

### Encrypted Secrets

```bash
# Encrypt secret
echo "my-secret-value" | gpg --symmetric --cipher-algo AES256

# Decrypt in workflow
- name: Decrypt secret
  run: |
    echo "${{ secrets.GPG_PRIVATE_KEY }}" | gpg --batch --passphrase-fd 0 --import
    gpg --decrypt secret.txt.gpg > secret.txt
```

### Environment Secrets

```yaml
jobs:
  deploy:
    environment: production
    runs-on: ubuntu-latest
    steps:
      - name: Use environment secret
        env:
          API_KEY: ${{ secrets.API_KEY }}
        run: echo "Deploying with API key"
```

---

## Environments

### Define Environments

```yaml
jobs:
  deploy-staging:
    environment:
      name: staging
      url: https://staging.example.com
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: echo "Deploying to staging"

  deploy-production:
    environment:
      name: production
      url: https://example.com
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: echo "Deploying to production"
```

### Environment Protection Rules

```
Settings > Environments > Production > Protection rules:
- Required reviewers: @team-leads
- Wait timer: 30 minutes
- Restrict who can deploy: @deploy-team
```

### Environment Secrets

```yaml
jobs:
  deploy:
    environment: production
    runs-on: ubuntu-latest
    steps:
      - name: Use environment-specific secret
        env:
          PRODUCTION_API_KEY: ${{ secrets.PRODUCTION_API_KEY }}
        run: echo "Deploying to production"
```

---

## Deployment Strategies

### Rolling Deployment

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Deploy to Kubernetes
        uses: azure/k8s-deploy@v4
        with:
          manifests: |
            k8s/deployment.yaml
            k8s/service.yaml
          images: |
            myapp:${{ github.sha }}
          kubectl-version: 'latest'
```

### Blue/Green Deployment

```yaml
jobs:
  deploy-blue:
    runs-on: ubuntu-latest
    environment:
      name: production-blue
      url: https://blue.example.com
    steps:
      - name: Deploy blue
        run: |
          kubectl apply -f k8s/blue-deployment.yaml

  deploy-green:
    needs: deploy-blue
    runs-on: ubuntu-latest
    environment:
      name: production-green
      url: https://green.example.com
    steps:
      - name: Deploy green
        run: |
          kubectl apply -f k8s/green-deployment.yaml

  switch-traffic:
    needs: deploy-green
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Switch traffic to green
        run: |
          kubectl patch service myapp -p '{"spec":{"selector":{"version":"green"}}}'
```

### Canary Deployment

```yaml
jobs:
  deploy-main:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Deploy main version
        run: |
          kubectl set image deployment/myapp myapp=myapp:1.0.0

  deploy-canary:
    needs: deploy-main
    runs-on: ubuntu-latest
    environment: production-canary
    steps:
      - name: Deploy canary version
        run: |
          kubectl apply -f k8s/canary-deployment.yaml
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
  frontend:
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.modified, 'frontend/')
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build frontend
        run: |
          cd frontend
          npm run build

  backend:
    runs-on: ubuntu-latest
    if: contains(github.event.head_commit.modified, 'backend/')
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Build backend
        run: |
          cd backend
          npm run build
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
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install Turborepo
        run: npm install -g turbo

      - name: Run Turborepo
        run: turbo run build --filter=[HEAD~1]
```

### Nx

```yaml
name: Nx CI

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Install Nx
        run: npm install -g nx

      - name: Run affected
        run: nx affected --target=build --base=HEAD~1
```

---

## Reusable Workflows

### Create Reusable Workflow

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

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
name: Deploy to Staging

on:
  push:
    branches: [main]

jobs:
  deploy-staging:
    uses: ./.github/workflows/reusable-deploy.yml
    with:
      environment: staging
      image: myapp:${{ github.sha }}
    secrets: inherit
```

### Reusable Workflow with Secrets

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      AWS_ACCESS_KEY_ID:
        required: true
      AWS_SECRET_ACCESS_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Deploy
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        run: |
          echo "Deploying to ${{ inputs.environment }}"
```

---

## Security Best Practices

### Pin Action Versions

```yaml
# ❌ BAD: Using @latest
- uses: actions/checkout@latest

# ✅ GOOD: Using specific version
- uses: actions/checkout@v4
```

### Use OIDC for Authentication

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Deploy
        run: |
          # Deployment commands
```

### Scan for Vulnerabilities

```yaml
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

### CodeQL Analysis

```yaml
name: CodeQL

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: ['javascript']

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: ${{ matrix.language }}

      - name: Autobuild
        uses: github/codeql-action/autobuild@v2

      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2
```

---

## Production Examples

### Complete CI/CD Pipeline

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  release:
    types: [published]

env:
  NODE_VERSION: '18'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Run tests
        run: npm test -- --coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  build:
    name: Build Docker Image
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    name: Deploy to Staging
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG }}

      - name: Deploy to staging
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:develop \
            -n staging

  deploy-production:
    name: Deploy to Production
    needs: build
    if: github.event_name == 'release'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          method: kubeconfig
          kubeconfig: ${{ secrets.KUBE_CONFIG }}

      - name: Deploy to production
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.event.release.tag_name }} \
            -n production

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/myapp -n production
```

---

## Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Marketplace](https://github.com/marketplace?type=actions)
- [Starter Workflows](https://github.com/actions/starter-workflows)
