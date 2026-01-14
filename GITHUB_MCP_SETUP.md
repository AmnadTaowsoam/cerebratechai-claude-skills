# 🎯 GitHub + MCP Setup Guide

Complete guide for setting up Claude Skills with GitHub and Model Context Protocol (MCP)

**Last Updated**: January 15, 2024  
**Estimated Time**: 15-20 minutes  
**Difficulty**: Beginner-Friendly

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Part 1: GitHub Repository Setup](#part-1-github-repository-setup)
4. [Part 2: GitHub Token Creation](#part-2-github-token-creation)
5. [Part 3: Claude Desktop Configuration](#part-3-claude-desktop-configuration)
6. [Part 4: Claude Code (VS Code) Configuration](#part-4-claude-code-vs-code-configuration)
7. [Part 5: Testing & Verification](#part-5-testing--verification)
8. [Part 6: Multi-Device Setup](#part-6-multi-device-setup)
9. [Troubleshooting](#troubleshooting)
10. [Advanced Configuration](#advanced-configuration)
11. [Best Practices](#best-practices)

---

## Overview

### What You'll Achieve

By the end of this guide, you'll have:

- ✅ Skills repository hosted on GitHub
- ✅ MCP server connected to Claude Desktop
- ✅ MCP server connected to Claude Code (VS Code)
- ✅ Automatic sync across all your devices
- ✅ Ability to use skills in your development workflow

### Architecture

```
┌─────────────────────┐
│  GitHub Repository  │ ← Your skills stored here
└──────────┬──────────┘
           │
           │ (MCP Protocol)
           │
     ┌─────┴─────┐
     │           │
┌────▼────┐ ┌───▼─────┐
│ Claude  │ │ Claude  │
│ Desktop │ │  Code   │
└─────────┘ └─────────┘
  (Mac 1)    (Mac 2, PC, etc.)
```

---

## Prerequisites

### Required Software

| Software | Version | Download |
|----------|---------|----------|
| **Git** | 2.30+ | [git-scm.com](https://git-scm.com) |
| **Node.js** | 18+ | [nodejs.org](https://nodejs.org) |
| **Claude Desktop** | Latest | [claude.ai/download](https://claude.ai/download) |
| **VS Code** (optional) | Latest | [code.visualstudio.com](https://code.visualstudio.com) |

### Check Installation

```bash
# Verify Git
git --version
# Expected: git version 2.x.x

# Verify Node.js
node --version
# Expected: v18.x.x or higher

# Verify npm
npm --version
# Expected: 9.x.x or higher
```

### Required Accounts

- ✅ GitHub account (free tier is fine)
- ✅ Claude account (claude.ai)

---

## Part 1: GitHub Repository Setup

### Step 1.1: Create Repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Fill in repository details:
   - **Repository name**: `cerebratechai-claude-skills`
   - **Description**: `Production-ready skills for Claude AI development`
   - **Visibility**: 
     - ✅ **Public** (recommended for easy sharing)
     - or **Private** (if needed, works with MCP)
   - **Initialize**: 
     - ✅ Add README file
     - ✅ Add .gitignore (choose "Node" template)
     - ✅ Choose a license (MIT recommended)
3. Click **Create repository**

### Step 1.2: Clone Repository Locally

```bash
# Choose your preferred location
cd ~/projects

# Clone the repository
git clone https://github.com/YOUR_USERNAME/cerebratechai-claude-skills.git

# Enter the directory
cd cerebratechai-claude-skills
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 1.3: Create Directory Structure

```bash
# Create all skill category folders
mkdir -p {01-foundations,02-frontend,03-backend-api,04-database,05-ai-ml-core,06-ai-ml-production,07-document-processing,08-messaging-queue,09-microservices,10-authentication-authorization,11-billing-subscription,12-compliance-governance,13-file-storage,14-monitoring-observability,15-devops-infrastructure,16-testing,17-domain-specific,18-project-management,19-seo-optimization,20-ai-integration,21-documentation,22-ux-ui-design,28-marketing-integration,29-customer-support,30-ecommerce,31-mobile-development,32-crm-integration,33-content-management,34-real-time-features,35-blockchain-web3,36-iot-integration,37-video-streaming,38-gaming-features,39-data-science-ml}

# Create a sample skill to test
mkdir -p 01-foundations/typescript-standards

cat > 01-foundations/typescript-standards/SKILL.md << 'EOF'
# TypeScript Standards

## Overview
Comprehensive TypeScript coding standards for production applications.

## Naming Conventions

### Variables and Functions
- Use **camelCase** for variables and functions
- Use descriptive names that indicate purpose

```typescript
// ✅ Good
const userName = 'John';
const calculateTotalPrice = (items: Item[]) => {...}

// ❌ Bad
const un = 'John';
const calc = (items: Item[]) => {...}
```

### Classes and Interfaces
- Use **PascalCase** for classes and interfaces
- Prefix interfaces with 'I' only when necessary for clarity

```typescript
// ✅ Good
class UserService {...}
interface User {...}
interface IPaymentProvider {...}

// ❌ Bad
class userService {...}
interface user {...}
```

### Constants
- Use **UPPER_SNAKE_CASE** for constants

```typescript
// ✅ Good
const MAX_RETRY_ATTEMPTS = 3;
const API_BASE_URL = 'https://api.example.com';

// ❌ Bad
const maxRetryAttempts = 3;
const apiBaseUrl = 'https://api.example.com';
```

## Type Definitions

### Explicit Types
Always use explicit type annotations for function parameters and return types.

```typescript
// ✅ Good
function calculateTotal(price: number, tax: number): number {
  return price + (price * tax);
}

// ❌ Bad
function calculateTotal(price, tax) {
  return price + (price * tax);
}
```

### Avoid `any`
Avoid using `any` type. Use `unknown` if type is truly unknown.

```typescript
// ✅ Good
function processData(data: unknown): void {
  if (typeof data === 'string') {
    console.log(data.toUpperCase());
  }
}

// ❌ Bad
function processData(data: any): void {
  console.log(data.toUpperCase()); // No type safety
}
```

## Best Practices

- [ ] Enable `strict` mode in tsconfig.json
- [ ] Use `interface` for object shapes
- [ ] Use `type` for unions and intersections
- [ ] Prefer `const` over `let`, avoid `var`
- [ ] Use optional chaining (`?.`) and nullish coalescing (`??`)
- [ ] Document complex types with JSDoc comments

## tsconfig.json Template

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## ESLint Configuration

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "project": "./tsconfig.json"
  },
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

## Common Pitfalls

### ❌ Pitfall 1: Not using strict null checks
```typescript
// Bad: Can lead to runtime errors
function getUserName(user: User): string {
  return user.name; // What if user is undefined?
}

// Good: Explicit null handling
function getUserName(user: User | undefined): string {
  return user?.name ?? 'Guest';
}
```

### ❌ Pitfall 2: Type assertions without validation
```typescript
// Bad: Unsafe type assertion
const data = JSON.parse(response) as User;

// Good: Runtime validation
function isUser(obj: unknown): obj is User {
  return typeof obj === 'object' && obj !== null && 'id' in obj;
}

const data = JSON.parse(response);
if (isUser(data)) {
  // Safe to use as User
}
```

---

**When to use this skill**: For all TypeScript projects to maintain consistent code quality and type safety.
EOF

# Verify the file was created
cat 01-foundations/typescript-standards/SKILL.md
```

### Step 1.4: Update README

```bash
cat > README.md << 'EOF'
# 🧠 Cerebrate Chai - Claude Skills Repository

Production-ready skills for Claude AI development across multiple projects and teams.

## 📚 What Are Skills?

Skills are comprehensive markdown documents that teach Claude best practices, patterns, and standards for software development. Each skill contains:

- ✅ Detailed implementation guides
- ✅ Production-ready code examples
- ✅ Best practices and anti-patterns
- ✅ Common pitfalls to avoid
- ✅ Testing strategies
- ✅ Security considerations

## 🗂️ Repository Structure

```
cerebratechai-claude-skills/
├── 01-foundations/          # Core development standards
├── 02-frontend/             # Frontend frameworks & patterns
├── 03-backend-api/          # Backend API development
├── 04-database/             # Database design & optimization
├── 05-ai-ml-core/          # ML model training & deployment
├── 06-ai-ml-production/    # Production AI/ML systems
├── 07-document-processing/ # OCR & document parsing
├── 08-messaging-queue/     # Message queuing systems
├── 09-microservices/       # Microservices architecture
├── 10-authentication-authorization/  # Auth & security
├── 11-billing-subscription/         # Payment systems
├── 12-compliance-governance/        # Legal compliance
├── 13-file-storage/        # File management & CDN
├── 14-monitoring-observability/     # Monitoring & logging
├── 15-devops-infrastructure/        # DevOps & IaC
├── 16-testing/             # Testing strategies
├── 17-domain-specific/     # Cross-cutting concerns
└── [18-39]/                # Additional categories
```

## 🚀 Quick Start

### For Claude Desktop Users

See [GITHUB_MCP_SETUP.md](./docs/GITHUB_MCP_SETUP.md) for complete setup instructions.

### For Claude Code (VS Code) Users

See [GITHUB_MCP_SETUP.md](./docs/GITHUB_MCP_SETUP.md) for complete setup instructions.

## 📖 Usage

Once configured, reference skills in your conversations:

```
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns
- jwt-authentication

Create a complete authentication system for my Next.js app.
```

Claude will read these skills and implement following all best practices.

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](./LICENSE) for details.

## 🙏 Acknowledgments

Created for use with Claude AI by Anthropic.
EOF
```

### Step 1.5: Commit and Push

```bash
# Stage all files
git add .

# Commit
git commit -m "Initial repository structure with sample skill"

# Push to GitHub
git push origin main
```

**✅ Checkpoint**: Your skills repository is now on GitHub!

Visit `https://github.com/YOUR_USERNAME/cerebratechai-claude-skills` to verify.

---

## Part 2: GitHub Token Creation

### Why Do You Need a Token?

GitHub tokens allow Claude to read your skills repository securely without requiring your GitHub password.

### Step 2.1: Navigate to Token Settings

1. Go to [github.com/settings/tokens](https://github.com/settings/tokens)
2. Or: Click your profile → Settings → Developer settings → Personal access tokens

### Step 2.2: Choose Token Type

**Option A: Fine-grained Token (Recommended - More Secure)**

1. Click: **Personal access tokens** → **Fine-grained tokens**
2. Click: **Generate new token**
3. Fill in details:
   - **Token name**: `Claude MCP - Skills` (or any descriptive name)
   - **Expiration**: 
     - Recommended: `90 days` (you'll need to renew)
     - or `Custom` with specific date
     - ⚠️ Avoid: `No expiration` (security risk)
   - **Description**: `MCP access for Claude to read skills repository`

4. **Repository access**:
   - Select: **Only select repositories**
   - Choose: `cerebratechai-claude-skills`

5. **Permissions** → **Repository permissions**:
   - **Contents**: Select `Read-only` ✅
   - **Metadata**: Will be selected automatically ✅

6. Click: **Generate token**

7. **IMPORTANT**: Copy the token immediately
   ```
   github_pat_11XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
   - Token starts with `github_pat_`
   - You will **not** be able to see it again!

**Option B: Classic Token (Easier but Less Secure)**

1. Click: **Personal access tokens** → **Tokens (classic)**
2. Click: **Generate new token (classic)**
3. Fill in details:
   - **Note**: `Claude MCP Skills`
   - **Expiration**: `90 days`
   - **Select scopes**:
     - ✅ `repo` (Full control of private repositories)
     - This gives access to all your repos (less secure)

4. Click: **Generate token**

5. Copy the token:
   ```
   ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
   - Token starts with `ghp_`

### Step 2.3: Save Token Securely

**⚠️ CRITICAL: Save your token immediately!**

Create a secure note:

```bash
# Option 1: Use a password manager (recommende