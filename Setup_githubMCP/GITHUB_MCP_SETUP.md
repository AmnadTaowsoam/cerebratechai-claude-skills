# 🎯 GitHub + MCP Setup Guide

Complete guide for setting up Claude Skills with GitHub and Model Context Protocol (MCP)

**Last Updated**: January 16, 2026  
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
   - **Repository name**: `cerebraSkills`
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
git clone https://github.com/YOUR_USERNAME/cerebraSkills.git

# Enter the directory
cd cerebraSkills
```

Replace `YOUR_USERNAME` with your actual GitHub username.

### Step 1.3: Create Directory Structure

```bash
# Create all skill category folders
mkdir -p {00-meta-skills,01-foundations,02-frontend,03-backend-api,04-database,05-ai-ml-core,06-ai-ml-production,07-document-processing,08-messaging-queue,09-microservices,10-authentication-authorization,11-billing-subscription,12-compliance-governance,13-file-storage,14-monitoring-observability,15-devops-infrastructure,16-testing,17-domain-specific,18-project-management,19-seo-optimization,20-ai-integration,21-documentation,22-ux-ui-design,23-business-analytics,24-security-practices,25-internationalization,26-deployment-strategies,27-team-collaboration,28-marketing-integration,29-customer-support,30-ecommerce,31-mobile-development,32-crm-integration,33-content-management,34-real-time-features,35-blockchain-web3,36-iot-integration,37-video-streaming,38-gaming-features,39-data-science-ml,40-system-resilience,41-incident-management,42-cost-engineering,43-data-reliability,44-ai-governance,45-developer-experience,46-data-classification,47-performance-engineering,48-product-discovery,49-portfolio-management,50-enterprise-integrations,51-contracts-governance,52-ai-evaluation,53-data-engineering,54-agentops,55-ux-writing,56-requirements-intake,57-skill-orchestration,58-investment-estimation,59-architecture-decision,59-release-engineering,60-github-mcp,60-infrastructure-patterns,61-ai-production,62-scale-operations,63-professional-services,64-meta-standards,65-context-token-optimization,66-repo-navigation-knowledge-map,67-codegen-scaffolding-automation,68-quality-gates-ci-policies,69-platform-engineering-lite,70-data-platform-governance}

# Create a sample skill to test
mkdir -p 01-foundations/typescript-standards

cat > 01-foundations/typescript-standards/SKILL.md << 'EOF'
---
name: TypeScript Standards
description: Comprehensive TypeScript coding standards for production applications
---

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

````
cerebraSkills/
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
````

## 🚀 Quick Start

### For Claude Desktop Users

See [GITHUB_MCP_SETUP.md](./docs/GITHUB_MCP_SETUP.md) for complete setup instructions.

### For Claude Code (VS Code) Users

See [GITHUB_MCP_SETUP.md](./docs/GITHUB_MCP_SETUP.md) for complete setup instructions.

## 📖 Usage

Once configured, reference skills in your conversations:

````
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns
- jwt-authentication

Create a complete authentication system for my Next.js app.
````

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

Visit `https://github.com/YOUR_USERNAME/cerebraSkills` to verify.

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
   - Choose: `cerebraSkills`

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
# Option 1: Use a password manager (recommended)
# - 1Password
# - LastPass
# - Bitwarden

# Option 2: Save to encrypted file
echo "GITHUB_TOKEN=github_pat_YOUR_TOKEN_HERE" > ~/.github-tokens
chmod 600 ~/.github-tokens

# Option 3: Add to environment variables (temporary)
export GITHUB_TOKEN="github_pat_YOUR_TOKEN_HERE"
```

**Never commit tokens to Git!**

Add to `.gitignore` if storing locally:
```bash
echo ".github-tokens" >> .gitignore
echo ".env" >> .gitignore
```

**✅ Checkpoint**: You now have a GitHub Personal Access Token saved securely!

---

## Part 3: Claude Desktop Configuration

### Step 3.1: Locate Configuration File

The configuration file location depends on your operating system:

| OS | Configuration Path |
|----|-------------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

### Step 3.2: Create or Edit Configuration

#### macOS:

```bash
# Create directory if it doesn't exist
mkdir -p ~/Library/Application\ Support/Claude

# Edit configuration file
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### Windows (PowerShell):

```powershell
# Create directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude"

# Edit configuration file
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

#### Linux:

```bash
# Create directory if it doesn't exist
mkdir -p ~/.config/Claude

# Edit configuration file
nano ~/.config/Claude/claude_desktop_config.json
```

### Step 3.3: Add MCP Configuration

Copy and paste this configuration, replacing the placeholders:

```json
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_GITHUB_TOKEN_HERE",
        "GITHUB_OWNER": "YOUR_GITHUB_USERNAME",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

**Replace these values:**

- `YOUR_GITHUB_TOKEN_HERE` → Your actual token (starts with `github_pat_` or `ghp_`)
- `YOUR_GITHUB_USERNAME` → Your GitHub username (e.g., `AmnadTaowsoam`)

**Example:**

```json
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "github_pat_11ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

### Step 3.4: Verify JSON Syntax

Before saving, verify your JSON is valid:

```bash
# macOS/Linux - Validate JSON
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool

# Windows PowerShell
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json

# If no errors, JSON is valid ✅
```

### Step 3.5: Save and Close

- **nano**: Press `Ctrl+X`, then `Y`, then `Enter`
- **Notepad**: File → Save → Close

### Step 3.6: Restart Claude Desktop

#### macOS:

```bash
# Quit Claude
killall Claude

# Start Claude
open -a Claude
```

#### Windows:

1. Right-click Claude in System Tray
2. Select **Quit**
3. Start Claude from Start Menu

#### Linux:

```bash
# Quit Claude
pkill -f claude

# Start Claude
claude &
```

**✅ Checkpoint**: Claude Desktop is now configured with MCP!

---

## Part 4: Claude Code (VS Code) Configuration

### Step 4.1: Install Claude Code Extension

1. Open VS Code
2. Press `Cmd+Shift+X` (macOS) or `Ctrl+Shift+X` (Windows/Linux)
3. Search for: **"Claude Code"**
4. Click: **Install**

### Step 4.2: Configuration is Shared!

**Good news**: Claude Code uses the **same configuration file** as Claude Desktop!

The config you created in Part 3 automatically works for Claude Code.

**No additional setup needed!** ✅

### Step 4.3: Reload VS Code

```bash
# Press Cmd+Shift+P (macOS) or Ctrl+Shift+P (Windows/Linux)
# Type: "Developer: Reload Window"
# Press Enter
```

Or simply restart VS Code:

```bash
# Close and reopen VS Code
```

### Step 4.4: Open Claude Code

**Method 1: Command Palette**
```bash
Cmd+Shift+P (or Ctrl+Shift+P)
→ Type: "Claude Code: Chat"
→ Press Enter
```

**Method 2: Activity Bar**
- Look for Claude icon in left sidebar
- Click to open chat panel

**Method 3: Keyboard Shortcut**
- `Cmd+Shift+/` (macOS)
- `Ctrl+Shift+/` (Windows/Linux)

**✅ Checkpoint**: Claude Code is ready to use!

---

## Part 5: Testing & Verification

### Test 1: Check MCP Connection (Claude Desktop)

Open Claude Desktop and type:

```
List available MCP servers
```

**Expected Output:**
```
I can see the following MCP servers:
- cerebratechai-skills
```

### Test 2: List Repository Contents

```
What files are in the cerebratechai-skills repository?
```

**Expected Output:**
```
The cerebratechai-skills repository contains:
- README.md
- 01-foundations/
  - typescript-standards/
    - SKILL.md
- 02-frontend/
- 03-backend-api/
[... and other folders]
```

### Test 3: Read a Skill

```
Read the typescript-standards skill from cerebratechai-skills
```

**Expected Output:**
```
# TypeScript Standards

## Overview
Comprehensive TypeScript coding standards for production applications.

[... rest of the skill content ...]
```

### Test 4: Use Skill in Task

```
Using the typescript-standards skill from cerebratechai-skills,
create a function that calculates the total price with tax.
```

**Expected Output:**
Claude will create a TypeScript function following the naming conventions and best practices from the skill.

### Test 5: Claude Code (VS Code) Test

Open Claude Code in VS Code and type:

```
/model
```

You should see `cerebratechai-skills` in the list of available tools.

Then try:

```
List all skills in cerebratechai-skills
```

**✅ All Tests Passed**: Your setup is complete and working!

---

## Part 6: Multi-Device Setup

### Device 1 (Primary - Already Done)

✅ Repository created on GitHub  
✅ Token created  
✅ Claude Desktop configured  
✅ Claude Code configured

### Device 2, 3, etc. (Additional Devices)

On each new device, you only need to:

#### Step 1: Install Prerequisites

```bash
# Verify installations
git --version
node --version
npm --version
```

#### Step 2: Configure Claude Desktop

Use the **same configuration** from Part 3:

**macOS:**
```bash
mkdir -p ~/Library/Application\ Support/Claude
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```powershell
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude"
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

**Linux:**
```bash
mkdir -p ~/.config/Claude
nano ~/.config/Claude/claude_desktop_config.json
```

**Paste the same config:**

```json
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_SAME_TOKEN",
        "GITHUB_OWNER": "YOUR_USERNAME",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

#### Step 3: Restart Claude

```bash
# macOS
killall Claude && open -a Claude

# Windows
# Quit from system tray, then restart

# Linux
pkill -f claude && claude &
```

#### Step 4: Test

```
List skills in cerebratechai-skills
```

**✅ That's it!** Same token works on all devices.

### Updating Skills

**On any device:**

```bash
# 1. Clone repo (if not already)
cd ~/projects
git clone https://github.com/YOUR_USERNAME/cerebraSkills.git

# 2. Make changes
cd cerebraSkills
# ... edit skills ...

# 3. Commit and push
git add .
git commit -m "Update skills"
git push
```

**On all other devices:**

No action needed! Claude automatically fetches latest from GitHub.

---

## Troubleshooting

### Problem 1: "Authentication failed" Error

**Symptom:**
```
Error: Failed to connect to GitHub: Authentication failed
```

**Solutions:**

1. **Check token is correct:**
   ```bash
   # Test token manually
   curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user
   
   # Should return your GitHub user info
   # If error → token is invalid
   ```

2. **Token may have expired:**
   - Go to [github.com/settings/tokens](https://github.com/settings/tokens)
   - Check if token is expired
   - Generate new token if needed

3. **Verify token in config file:**
   ```bash
   # macOS
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Check that token matches what you saved
   ```

4. **Wrong token scope:**
   - Fine-grained token must have "Contents: Read" permission
   - Classic token must have "repo" scope

### Problem 2: "Repository not found" Error

**Symptom:**
```
Error: Repository cerebraSkills not found
```

**Solutions:**

1. **Check repository exists:**
   - Visit `https://github.com/YOUR_USERNAME/cerebraSkills`
   - If 404 → repository name is wrong or doesn't exist

2. **Verify GITHUB_OWNER is correct:**
   ```json
   "GITHUB_OWNER": "YOUR_ACTUAL_USERNAME"
   ```
   - Must match your GitHub username exactly
   - Case-sensitive!

3. **Check if repo is private:**
   - Private repos require token with `repo` scope
   - Fine-grained tokens need repository access granted

### Problem 3: Claude Doesn't See MCP Server

**Symptom:**
```
User: List MCP servers
Claude: I don't see any MCP servers configured.
```

**Solutions:**

1. **Verify config file location:**
   ```bash
   # macOS - Check file exists
   ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Windows
   dir "%APPDATA%\Claude\claude_desktop_config.json"
   
   # Linux
   ls -la ~/.config/Claude/claude_desktop_config.json
   ```

2. **Validate JSON syntax:**
   ```bash
   # macOS/Linux
   cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool
   
   # Windows PowerShell
   Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json
   
   # If error → fix JSON syntax
   ```

3. **Check for typos:**
   - `mcpServers` (case-sensitive)
   - `command`, `args`, `env` (must be exact)

4. **Restart Claude properly:**
   ```bash
   # macOS - Force quit
   killall -9 Claude
   open -a Claude
   
   # Windows - Task Manager
   # End task, then restart
   ```

### Problem 4: npx Command Not Found

**Symptom:**
```
Error: command not found: npx
```

**Solutions:**

1. **Install Node.js:**
   - Download from [nodejs.org](https://nodejs.org)
   - Restart terminal after installation

2. **Verify PATH:**
   ```bash
   which npx
   # Should show: /usr/local/bin/npx or similar
   
   echo $PATH
   # Should include Node.js bin directory
   ```

3. **Restart terminal/VS Code:**
   - Close all terminals
   - Restart VS Code completely

### Problem 5: Skills Not Updating

**Symptom:**
After pushing changes to GitHub, Claude still shows old content.

**Solutions:**

1. **Verify push succeeded:**
   ```bash
   # Check latest commit on GitHub
   git log -1
   # Visit GitHub repo to confirm
   ```

2. **MCP servers cache content:**
   ```bash
   # Clear Claude cache (macOS)
   rm -rf ~/Library/Caches/Claude
   
   # Windows
   del /f /s /q "%LOCALAPPDATA%\Claude\Cache"
   
   # Linux
   rm -rf ~/.cache/Claude
   
   # Then restart Claude
   ```

3. **Force re-read:**
   ```
   Re-read the typescript-standards skill from cerebratechai-skills
   ```

### Problem 6: Slow Performance

**Symptom:**
Claude takes a long time to read skills.

**Solutions:**

1. **Check internet connection:**
   - MCP fetches from GitHub each time
   - Slow connection = slow reads

2. **Repository too large:**
   - If repo > 100MB, consider splitting
   - Remove large binary files

3. **Consider local MCP:**
   - For faster access, use filesystem MCP
   - See Advanced Configuration section

### Problem 7: VS Code Extension Not Working

**Symptom:**
Claude Code extension installed but not working.

**Solutions:**

1. **Check Claude Desktop works first:**
   - MCP must work in Desktop before Code
   - Follow Parts 1-3 first

2. **Reload VS Code window:**
   ```
   Cmd+Shift+P → Developer: Reload Window
   ```

3. **Check extension is enabled:**
   - Extensions view (Cmd+Shift+X)
   - Search "Claude Code"
   - Should show "Enabled"

4. **View extension logs:**
   ```
   View → Output → Select "Claude Code" from dropdown
   ```

### Problem 8: Token Security Concerns

**Symptom:**
Worried about token in plain text config file.

**Solutions:**

1. **Use environment variables:**
   ```bash
   # Add to .zshrc or .bashrc
   export GITHUB_CLAUDE_TOKEN="your_token_here"
   ```

   ```json
   {
     "mcpServers": {
       "cerebratechai-skills": {
         "env": {
           "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_CLAUDE_TOKEN}"
         }
       }
     }
   }
   ```

2. **Use system keychain:**
   ```bash
   # macOS Keychain
   security add-generic-password -s "Claude MCP" -a "github-token" -w "your_token"
   
   # Retrieve in config using script
   ```

3. **Use fine-grained token:**
   - Limit to specific repository only
   - Read-only access
   - Set expiration date

4. **Regular token rotation:**
   - Revoke old tokens monthly
   - Generate new tokens
   - Update config files

---

## Advanced Configuration

### Multiple Repositories

You can connect multiple skills repositories:

```json
{
  "mcpServers": {
    "global-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token",
        "GITHUB_OWNER": "YourUsername",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    },
    "project-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token",
        "GITHUB_OWNER": "YourUsername",
        "GITHUB_REPO": "my-project-skills",
        "GITHUB_BRANCH": "main"
      }
    },
    "team-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token",
        "GITHUB_OWNER": "CompanyName",
        "GITHUB_REPO": "company-skills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

Usage:
```
Read typescript-standards from global-skills
Read api-conventions from project-skills
Read security-policy from team-skills
```

### Different Branches

Use different branches for development and production:

```json
{
  "mcpServers": {
    "skills-prod": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token",
        "GITHUB_OWNER": "YourUsername",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    },
    "skills-dev": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token",
        "GITHUB_OWNER": "YourUsername",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "develop"
      }
    }
  }
}
```

### Combining GitHub + Local Skills

Mix cloud and local skills:

```json
{
  "mcpServers": {
    "github-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token",
        "GITHUB_OWNER": "YourUsername",
        "GITHUB_REPO": "cerebraSkills"
      }
    },
    "local-skills": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/yourname/my-project/.claude/skills"
      ]
    }
  }
}
```

### Custom MCP Server (Advanced)

For advanced users, create a custom MCP server with additional features:

```bash
# Create custom server directory
mkdir ~/cerebratechai-mcp
cd ~/cerebratechai-mcp

# Initialize npm project
npm init -y

# Install dependencies
npm install @modelcontextprotocol/sdk

# Create server.js
# (See custom server code in main documentation)

# Link globally
npm link

# Update config
{
  "mcpServers": {
    "custom-skills": {
      "command": "cerebratechai-mcp",
      "env": {
        "GITHUB_TOKEN": "your_token",
        "SKILLS_REPO": "YourUsername/cerebraSkills"
      }
    }
  }
}
```

---

## Best Practices

### Security

1. **Token Management**
   - ✅ Use fine-grained tokens when possible
   - ✅ Set expiration dates (90 days recommended)
   - ✅ Rotate tokens regularly
   - ✅ Revoke unused tokens immediately
   - ❌ Never commit tokens to Git
   - ❌ Never share tokens in screenshots/videos
   - ❌ Never use tokens with more permissions than needed

2. **Repository Access**
   - ✅ Use private repos for proprietary skills
   - ✅ Use public repos for open-source skills
   - ✅ Review token permissions quarterly
   - ✅ Use different tokens for different purposes

### Skills Organization

1. **Naming Conventions**
   ```
   ✅ Good:
   - typescript-standards/SKILL.md
   - react-best-practices/SKILL.md
   - api-error-handling/SKILL.md
   
   ❌ Bad:
   - ts.md
   - react_patterns.md
   - errors/README.md
   ```

2. **Skill Structure**
   ```markdown
   # Skill Name
   
   ## Overview
   Brief description (2-3 sentences)
   
   ## [Main Sections]
   Detailed content with examples
   
   ## Best Practices
   - Checklist format
   
   ## Common Pitfalls
   - What to avoid
   
   ## Examples
   - Code examples
   ```

3. **Category Placement**
   ```
   - GitHub MCP skills: 60-github-mcp/<skill-name>/SKILL.md
   ```

4. **Using GitHub MCP Skills**
   ```
   Use the skill name directly in prompts:
   - "Use github-repo-navigation to find the auth module in owner/repo"
   - "Use github-issue-triage to label new bugs in owner/repo"
   - "Use github-pr-lifecycle to prepare a PR summary for #123"
   ```

5. **Version Control**
   ```bash
   # Always use meaningful commit messages
   git commit -m "Add error handling patterns to nodejs-api skill"
   
   # Use branches for major changes
   git checkout -b feature/add-graphql-skill
   
   # Tag releases
   git tag -a v1.0 -m "Initial skill collection"
   git push --tags
   ```

### Workflow

1. **Update Workflow**
   ```bash
   # On any device
   cd ~/cerebraSkills
   git pull                          # Get latest
   # ... make changes ...
   git add .
   git commit -m "Update XYZ skill"
   git push
   
   # On all other devices: automatic! ✅
   ```

2. **Testing New Skills**
   ```bash
   # Create in branch
   git checkout -b test/new-skill
   
   # Test with Claude
   # If good, merge
   git checkout main
   git merge test/new-skill
   git push
   ```

3. **Team Collaboration**
   ```bash
   # Team member creates PR
   # Review on GitHub
   # Merge when approved
   # Everyone gets updates automatically
   ```

### Maintenance

1. **Regular Updates**
   - Review skills monthly
   - Update examples with new framework versions
   - Add new patterns as you learn them
   - Remove deprecated practices

2. **Documentation**
   - Keep README.md updated
   - Document major changes in CHANGELOG.md
   - Add comments to complex examples

3. **Monitoring**
   - Check GitHub Insights for repository health
   - Review which skills are most accessed
   - Update based on actual usage

---

## Quick Reference

### Configuration File Locations

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

### Essential Commands

```bash
# Validate config JSON
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool

# Test GitHub token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# Update skills
cd ~/cerebraSkills
git pull && git add . && git commit -m "Update" && git push

# Restart Claude (macOS)
killall Claude && open -a Claude

# Clear Claude cache (macOS)
rm -rf ~/Library/Caches/Claude
```

### Common Claude Queries

```
# Test connection
List MCP servers

# List contents
What files are in cerebratechai-skills?

# Read skill
Read [skill-name] from cerebratechai-skills

# Use skill
Using [skill-name] from cerebratechai-skills, [task description]

# Multiple skills
Using skills from cerebratechai-skills:
- skill-1
- skill-2
- skill-3

[Task description]
```

---

## Checklist

### Initial Setup

```
[ ] Git installed and configured
[ ] Node.js 18+ installed
[ ] Claude Desktop installed
[ ] VS Code installed (optional)
[ ] Claude Code extension installed (optional)
[ ] GitHub account created
[ ] Repository created on GitHub
[ ] Local repository cloned
[ ] Sample skill created
[ ] Changes pushed to GitHub
[ ] GitHub token created
[ ] Token saved securely
[ ] Configuration file created
[ ] Configuration validated
[ ] Claude Desktop restarted
[ ] VS Code reloaded (if using Claude Code)
[ ] MCP connection tested
[ ] Skills readable from Claude
[ ] Sample task completed successfully
```

### Multi-Device Setup

```
For each new device:
[ ] Prerequisites installed
[ ] Configuration file created
[ ] Same token used
[ ] Claude restarted
[ ] Connection tested
```

### Maintenance (Monthly)

```
[ ] Review and update skills
[ ] Check token expiration
[ ] Rotate tokens if needed
[ ] Update documentation
[ ] Review GitHub insights
[ ] Clean up old branches
[ ] Update dependencies
```

---

## Additional Resources

### Official Documentation

- [Claude.ai](https://claude.ai)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

### Community

- [Claude Discord](https://discord.gg/claude) (check claude.ai for invite)
- [GitHub Discussions](https://github.com/YOUR_USERNAME/cerebraSkills/discussions)

### Related Guides

- `CONTRIBUTING.md` - How to add new skills
- `SKILL_TEMPLATE.md` - Template for creating skills
- `FAQ.md` - Frequently asked questions

---

## Support

### Getting Help

1. **Check Troubleshooting section** above
2. **Search GitHub Issues** in your repository
3. **Create New Issue** with:
   - Operating system
   - Claude version
   - Config file (remove token!)
   - Error messages
   - Steps to reproduce

### Reporting Bugs

```markdown
**Environment:**
- OS: macOS 14.0
- Claude Desktop: 0.7.0
- Node.js: 18.17.0

**Config:**
(paste config with token removed)

**Error:**
(paste error message)

**Steps to Reproduce:**
1. Step 1
2. Step 2
3. Error occurs
```

---

## Changelog

### Version 1.1 - January 16, 2026

- Updated skill counts (368+ skills, 59 categories)
- Added 22 new skills including GraphQL, gRPC, Saga Pattern, CQRS, and more
- Improved documentation structure

### Version 1.0 - January 15, 2024

- Initial release
- Complete setup guide for GitHub + MCP
- Support for macOS, Windows, Linux
- Support for Claude Desktop and Claude Code
- Troubleshooting section
- Advanced configuration examples

---

## License

MIT License - You are free to use, modify, and distribute this guide.

---

<div align="center">

**Made with ❤️ for the Claude community**

[⬆ Back to Top](#-github--mcp-setup-guide)

</div>d)
# Save to 1Password, LastPass, Bitwarden, etc.

# Option 2: Save to encrypted file
echo "GITHUB_TOKEN=ghp_your_token_here" > ~/.github_token
chmod 600 ~/.github_token

# Option 3: Save to environment variable
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.zshrc
source ~/.zshrc
```

**Test your token:**

```bash
# Replace with your actual token
curl -H "Authorization: token ghp_YOUR_TOKEN_HERE" \
  https://api.github.com/user

# Expected output: Your GitHub user info (JSON)
# If error: Token is invalid or expired
```

**✅ Checkpoint**: You have a working GitHub token saved securely.

---

## Part 3: Claude Desktop Configuration

### Step 3.1: Locate Configuration File

**macOS:**
```bash
# Configuration file location
~/Library/Application Support/Claude/claude_desktop_config.json

# Create directory if it doesn't exist
mkdir -p ~/Library/Application\ Support/Claude

# Open in editor
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```powershell
# Configuration file location
%APPDATA%\Claude\claude_desktop_config.json

# Create directory if it doesn't exist
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude"

# Open in notepad
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

**Linux:**
```bash
# Configuration file location
~/.config/Claude/claude_desktop_config.json

# Create directory if it doesn't exist
mkdir -p ~/.config/Claude

# Open in editor
nano ~/.config/Claude/claude_desktop_config.json
```

### Step 3.2: Create Configuration

Copy and paste this configuration:

```json
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN_HERE",
        "GITHUB_OWNER": "YOUR_USERNAME",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

**Replace the following:**
- `YOUR_TOKEN_HERE` → Your actual GitHub token (starts with `ghp_` or `github_pat_`)
- `YOUR_USERNAME` → Your GitHub username

**Example:**
```json
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_AbCdEfGhIjKlMnOpQrStUvWxYz1234567890",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

### Step 3.3: Validate JSON Syntax

```bash
# macOS/Linux - validate JSON
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq .

# If jq not installed:
brew install jq  # macOS
sudo apt install jq  # Linux

# Windows PowerShell - validate JSON
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json
```

**Expected output**: Your config printed with proper formatting  
**If error**: Fix JSON syntax (missing comma, bracket, etc.)

### Step 3.4: Restart Claude Desktop

**macOS:**
```bash
# Quit Claude completely
osascript -e 'quit app "Claude"'

# Or use Activity Monitor
# Cmd+Q on Claude

# Reopen Claude
open -a Claude
```

**Windows:**
```powershell
# Close from system tray (right-click → Exit)
# Or use Task Manager

# Reopen Claude from Start Menu
```

**Linux:**
```bash
# Kill Claude process
pkill -f claude

# Restart
claude &
```

### Step 3.5: Verify MCP Connection

Open Claude Desktop and type:

```
List available MCP servers
```

**Expected response:**
```
I can see the following MCP servers:
- cerebratechai-skills
```

If you see this, **configuration successful!** 🎉

---

## Part 4: Claude Code (VS Code) Configuration

### Step 4.1: Install Claude Code Extension

1. Open VS Code
2. Press `Cmd+Shift+X` (macOS) or `Ctrl+Shift+X` (Windows/Linux)
3. Search for: `Claude Code`
4. Click: **Install**
5. Wait for installation to complete

### Step 4.2: Configure MCP (Same as Desktop)

**Good News**: Claude Code uses the **same configuration file** as Claude Desktop!

If you completed Part 3, you're already done. ✅

If not, follow Step 3.1 and 3.2 above.

### Step 4.3: Reload VS Code

```
Cmd+Shift+P (or Ctrl+Shift+P)
→ Type: "Developer: Reload Window"
→ Press Enter
```

### Step 4.4: Verify in VS Code

1. Open Claude Code panel:
   - `Cmd+Shift+P` → "Claude Code: Open Chat"
   - Or click Claude icon in sidebar

2. Type: `/model`

3. You should see: `cerebratechai-skills` listed as available server

**✅ Checkpoint**: Claude Code can access your skills!

---

## Part 5: Testing & Verification

### Test 1: List Skills

**In Claude Desktop or Claude Code:**

```
What skills are available in the cerebratechai-skills MCP server?
```

**Expected response:**
```
I can see the following structure:
- 01-foundations/
  - typescript-standards/
    - SKILL.md
```

### Test 2: Read a Skill

```
Read the typescript-standards skill from cerebratechai-skills
and explain the naming conventions.
```

**Expected**: Claude reads and explains the skill content.

### Test 3: Use Skill to Generate Code

```
Using the typescript-standards skill from cerebratechai-skills,
create a TypeScript function that calculates compound interest.

Follow all naming conventions and best practices from the skill.
```

**Expected**: Claude generates code following the patterns in the skill.

### Test 4: Multiple Skills (if you have more)

```
Using skills from cerebratechai-skills:
- typescript-standards
- nodejs-api (if created)

Create a simple Express API endpoint.
```

**✅ All tests pass**: Setup complete and working perfectly!

---

## Part 6: Multi-Device Setup

### Setup on Second Device

**The beauty of GitHub + MCP**: Only need to repeat config, not repository!

#### On Your Second Device:

**Step 1: Install Prerequisites**
```bash
# Verify Git, Node.js, npm (same as Prerequisites section)
git --version
node --version
npm --version
```

**Step 2: Install Claude Desktop/Code**
- Download and install Claude Desktop
- Install VS Code + Claude Code extension (if needed)

**Step 3: Copy Configuration**

**Option A: Manual Copy**
```bash
# On first device - export config
# macOS
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Copy the output, then on second device:
# macOS
mkdir -p ~/Library/Application\ Support/Claude
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
# Paste and save
```

**Option B: Use Git to Share Config (Recommended)**

On first device:
```bash
# Create a private config repo (do NOT commit tokens!)
cd ~/.claude-config
git init

# Create config template
cat > config.template.json << 'EOF'
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN_HERE",
        "GITHUB_OWNER": "YOUR_USERNAME",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
EOF

# Create README with instructions
cat > README.md << 'EOF'
# Claude Configuration Template

1. Copy config.template.json to appropriate location:
   - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
   - Windows: %APPDATA%\Claude\claude_desktop_config.json
   - Linux: ~/.config/Claude/claude_desktop_config.json

2. Replace YOUR_TOKEN_HERE with your GitHub token
3. Replace YOUR_USERNAME with your GitHub username
4. Restart Claude Desktop
EOF

git add .
git commit -m "Claude config template"

# Push to private repo
git remote add origin https://github.com/YOUR_USERNAME/claude-config.git
git push -u origin main
```

On second device:
```bash
# Clone config repo
git clone https://github.com/YOUR_USERNAME/claude-config.git
cd claude-config

# Copy template and configure
# macOS
cp config.template.json ~/Library/Application\ Support/Claude/claude_desktop_config.json
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
# Update token and username
```

**Step 4: Restart Claude**

**Step 5: Verify**
```
List available MCP servers
```

**✅ Done**: Same skills accessible on all devices!

### Updating Skills (Any Device)

```bash
# On any device where you have the repo
cd ~/projects/cerebraSkills

# Make changes
nano 01-foundations/typescript-standards/SKILL.md

# Commit and push
git add .
git commit -m "Update typescript standards"
git push

# Other devices: Skills update automatically!
# Claude fetches latest from GitHub every time
```

---

## Troubleshooting

### Problem 1: "MCP server not found"

**Symptoms:**
- Claude says "I don't see any MCP servers"
- Skills are not accessible

**Solution:**
```bash
# 1. Check config file exists
ls -la ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 2. Validate JSON syntax
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | jq .

# 3. Check for typos in server name
# Must match exactly in config and when referencing

# 4. Restart Claude Desktop completely
killall Claude
open -a Claude
```

### Problem 2: "Authentication failed"

**Symptoms:**
- Error about GitHub authentication
- Cannot access repository

**Solution:**
```bash
# 1. Test token manually
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/YOUR_USERNAME/cerebraSkills

# If 401 error: Token expired or invalid
# → Create new token (Part 2)

# If 404 error: Repo name or username wrong
# → Check spelling in config

# 2. Verify token has correct permissions
# → Go to github.com/settings/tokens
# → Check token has "repo" or "Contents: Read" permission

# 3. Update config with new token
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 4. Restart Claude
```

### Problem 3: "Cannot find repository"

**Symptoms:**
- Error: Repository not found
- 404 errors in logs

**Solution:**
```bash
# 1. Verify repository exists
# Open: https://github.com/YOUR_USERNAME/cerebraSkills

# 2. Check repository visibility
# Private repo? Token must have "repo" access
# Public repo? Token needs "public_repo" or "Contents: Read"

# 3. Verify exact name in config
# Repository name is case-sensitive!

# 4. Check branch name
# Default is "main" but might be "master"
git ls-remote --heads https://github.com/YOUR_USERNAME/cerebraSkills
```

### Problem 4: Skills not updating

**Symptoms:**
- Made changes in GitHub but Claude shows old version
- New skills not visible

**Solution:**
```bash
# MCP fetches from GitHub each time, but may cache

# 1. Make sure changes are pushed
cd ~/projects/cerebraSkills
git status
git push

# 2. Verify on GitHub
# Open repo in browser, check file content

# 3. Clear Claude cache (if needed)
# macOS
rm -rf ~/Library/Caches/Claude/*

# 4. Restart Claude
killall Claude
open -a Claude

# 5. Test again
# In Claude: "Read typescript-standards skill from cerebratechai-skills"
```

### Problem 5: "npx command not found"

**Symptoms:**
- Error about npx not found
- MCP server won't start

**Solution:**
```bash
# 1. Verify Node.js and npm installed
node --version
npm --version

# If not installed:
# macOS: brew install node
# Windows: Download from nodejs.org
# Linux: sudo apt install nodejs npm

# 2. Verify npx available
npx --version

# 3. Update npm
npm install -g npm@latest

# 4. Try alternative: install MCP server globally
npm install -g @modelcontextprotocol/server-github

# Update config to use global install:
{
  "command": "mcp-server-github",
  "args": []
}
```

### Problem 6: Token expired

**Symptoms:**
- Was working, now getting auth errors
- Token expiration date reached

**Solution:**
```bash
# 1. Check token expiration
# Go to: github.com/settings/tokens
# Look for your token's expiration date

# 2. Generate new token (follow Part 2)

# 3. Update config with new token
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# 4. Restart Claude
```

### Problem 7: Slow performance

**Symptoms:**
- Claude takes long time to read skills
- Timeout errors

**Solution:**
```bash
# 1. Check repository size
du -sh ~/projects/cerebraSkills
# If > 100MB, might be slow

# 2. Check internet connection
ping github.com

# 3. Consider local cache option
# Switch to filesystem MCP for faster access:
{
  "command": "npx",
  "args": [
    "-y",
    "@modelcontextprotocol/server-filesystem",
    "/path/to/cerebraSkills"
  ]
}

# Sync periodically:
cd ~/projects/cerebraSkills
git pull
```

### Check Logs for Detailed Errors

**macOS:**
```bash
# Claude Desktop logs
tail -f ~/Library/Logs/Claude/mcp*.log

# System logs
log show --predicate 'process == "Claude"' --last 5m
```

**Windows:**
```powershell
# Claude logs location
Get-Content "$env:LOCALAPPDATA\Claude\logs\mcp*.log" -Tail 50
```

**Linux:**
```bash
# Claude logs
tail -f ~/.local/share/Claude/logs/mcp*.log
```

---

## Advanced Configuration

### Configuration 1: Multiple Skill Repositories

```json
{
  "mcpServers": {
    "global-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    },
    "company-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx",
        "GITHUB_OWNER": "YourCompany",
        "GITHUB_REPO": "company-internal-skills",
        "GITHUB_BRANCH": "main"
      }
    },
    "project-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "project-x-skills",
        "GITHUB_BRANCH": "develop"
      }
    }
  }
}
```

**Usage:**
```
Using global-skills:
- typescript-standards

And company-skills:
- api-conventions

Create an API endpoint.
```

### Configuration 2: Development vs Production

```json
{
  "mcpServers": {
    "skills-prod": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    },
    "skills-dev": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "develop"
      }
    }
  }
}
```

### Configuration 3: Using Environment Variables

```bash
# Set environment variable
export GITHUB_TOKEN="ghp_your_token_here"
export GITHUB_OWNER="AmnadTaowsoam"

# Config file
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}",
        "GITHUB_OWNER": "${GITHUB_OWNER}",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

### Configuration 4: Combining GitHub + Local

```json
{
  "mcpServers": {
    "github-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxx",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "cerebraSkills"
      }
    },
    "local-skills": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/username/projects/my-project/.claude/skills"
      ]
    }
  }
}
```

**Usage:**
```
Use github-skills for global patterns
and local-skills for project-specific conventions

Create a new feature.
```

---

## Best Practices

### 1. Security

#### ✅ Do:
- Use fine-grained tokens with minimal permissions
- Set token expiration (90 days recommended)
- Store tokens in password manager
- Use environment variables for sensitive data
- Rotate tokens regularly
- Revoke unused tokens

#### ❌ Don't:
- Commit tokens to Git repositories
- Share tokens via email or chat
- Use tokens with "no expiration"
- Give tokens more permissions than needed
- Reuse tokens across different purposes

### 2. Repository Management

#### ✅ Do:
- Use descriptive commit messages
- Create branches for major skill updates
- Use Pull Requests for team review
- Tag stable versions
- Keep skills organized by category
- Document each skill thoroughly

#### ❌ Don't:
- Commit directly to main without review
- Mix different skill categories in one file
- Include sensitive information in skills
- Create overly large skills (split them up)

### 3. Skill Organization

```
Good structure:
📁 01-foundations/
  📁 typescript-standards/
    📄 SKILL.md           ← Main skill content
    📄 examples/          ← Optional: code examples
    📄 templates/         ← Optional: templates

Bad structure:
📄 typescript.md          ← Not organized
📄 all-skills.md          ← Too large, hard to maintain
```

### 4. Naming Conventions

#### ✅ Good Names:
- `typescript-standards` (clear, specific)
- `nextjs-patterns` (technology + concept)
- `jwt-authentication` (clear purpose)

#### ❌ Bad Names:
- `ts` (too short, unclear)
- `stuff` (not descriptive)
- `best-practices` (too vague)

### 5. Version Control Workflow

```bash
# Create feature branch
git checkout -b add-react-patterns

# Make changes
nano 02-frontend/react-patterns/SKILL.md

# Commit with descriptive message
git add .
git commit -m "feat(frontend): add React hooks best practices

- Add useState patterns
- Add useEffect patterns  
- Add custom hooks guidelines"

# Push and create PR
git push origin add-react-patterns

# After review, merge to main
```

### 6. Team Collaboration

#### Share Configuration Template:
```bash
# In your skills repo, create:
docs/TEAM_SETUP.md

# Include:
- Link to this setup guide
- Your organization's GitHub username
- Repository name
- Any team-specific conventions
```

#### Example Team Setup Doc:
```markdown
# Team Skills Setup

1. Follow the main setup guide: [GITHUB_MCP_SETUP.md](./GITHUB_MCP_SETUP.md)

2. Use our organization repo:
   - Owner: `YourCompany`
   - Repo: `engineering-skills`
   - Branch: `main`

3. Request GitHub token from IT:
   - Email: it@company.com
   - Include: Your GitHub username

4. After setup, test with:
   ```
   Read the company-api-standards skill
   ```

5. Questions? Ask in #engineering-tools Slack channel
```

### 7. Maintenance Schedule

#### Weekly:
- Review and update active skills
- Check for outdated patterns
- Add new examples based on recent work

#### Monthly:
- Review token expiration dates
- Update dependencies in code examples
- Archive deprecated skills

#### Quarterly:
- Major skill reorganization (if needed)
- Team review session
- Update setup documentation

---

## Complete Checklist

### Initial Setup
```
[ ] Install prerequisites (Git, Node.js, Claude)
[ ] Create GitHub repository
[ ] Clone repository locally
[ ] Create directory structure
[ ] Add first skill
[ ] Commit and push to GitHub
[ ] Generate GitHub token
[ ] Save token securely
[ ] Configure Claude Desktop
[ ] Restart Claude Desktop
[ ] Test MCP connection
[ ] Configure Claude Code (if using VS Code)
[ ] Test skill reading
[ ] Test skill usage
```

### Multi-Device Setup
```
[ ] Install Claude on second device
[ ] Copy configuration file
[ ] Update token in config
[ ] Restart Claude
[ ] Verify MCP connection
[ ] Test skill access
```

### Ongoing Maintenance
```
[ ] Add new skills as needed
[ ] Update existing skills
[ ] Review token expiration monthly
[ ] Rotate tokens quarterly
[ ] Update documentation
[ ] Share with team members
```

---

## Quick Reference

### File Locations

| OS | Config Path |
|----|------------|
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

### Common Commands

```bash
# View config
cat ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Edit config (macOS/Linux)
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Validate JSON
cat config.json | jq .

# Test GitHub token
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# View Claude logs
tail -f ~/Library/Logs/Claude/mcp*.log

# Restart Claude (macOS)
killall Claude && open -a Claude

# Update skills repo
cd ~/projects/cerebraSkills && git pull

# Push skill changes
git add . && git commit -m "Update skills" && git push
```

### Config Template

```json
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN",
        "GITHUB_OWNER": "YOUR_USERNAME",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

### Usage Examples

```
# List servers
List available MCP servers

# List skills
What skills are in cerebratechai-skills?

# Read specific skill
Read the typescript-standards skill from cerebratechai-skills

# Use skills to generate code
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns

Create a Next.js API route for user authentication
```

---

## Getting Help

### Documentation
- **MCP Protocol**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Claude Help**: [support.claude.ai](https://support.claude.ai)
- **GitHub Tokens**: [docs.github.com/authentication](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)

### Common Issues
1. Check troubleshooting section above
2. Review Claude logs
3. Verify GitHub token permissions
4. Test with minimal configuration

### Community
- GitHub Issues: Create issue in your skills repo
- Claude Community: [Anthropic Discord](https://discord.gg/anthropic)

---

## Next Steps

After completing this setup:

1. **Add More Skills**
   - Create skills for your tech stack
   - Document your team's best practices
   - Share patterns you've learned

2. **Integrate into Workflow**
   - Reference skills in every project
   - Review code against skills
   - Update skills based on learnings

3. **Share with Team**
   - Send setup guide to colleagues
   - Create team-specific skills
   - Establish skill review process

4. **Automate**
   - Setup GitHub Actions for validation
   - Create templates for new skills
   - Add automated testing

---

## Appendix

### A. Token Permissions Reference

| Permission | Needed For | Access Level |
|-----------|------------|--------------|
| **repo** (classic) | Private repositories | Full access |
| **public_repo** (classic) | Public repositories only | Read/Write |
| **Contents: Read** (fine-grained) | Read files | Read-only |
| **Contents: Write** (fine-grained) | Modify files | Read/Write |
| **Metadata: Read** (fine-grained) | Repository info | Read-only (auto) |

### B. Supported File Types

MCP server-github supports:
- ✅ Markdown (`.md`)
- ✅ Text files (`.txt`)
- ✅ Code files (`.js`, `.ts`, `.py`, etc.)
- ✅ JSON (`.json`)
- ✅ YAML (`.yaml`, `.yml`)
- ✅ Configuration files

### C. Performance Considerations

| Repository Size | Performance | Recommendation |
|----------------|-------------|----------------|
| < 10 MB | ⚡⚡⚡ Excellent | Use as-is |
| 10-50 MB | ⚡⚡ Good | Consider organization |
| 50-100 MB | ⚡ Acceptable | Split into multiple repos |
| > 100 MB | 🐢 Slow | Definitely split or use local |

### D. Comparison: GitHub vs Local MCP

| Feature | GitHub MCP | Local Filesystem MCP |
|---------|-----------|---------------------|
| **Sync across devices** | ✅ Automatic | ❌ Manual |
| **Speed** | ⚡⚡ Good | ⚡⚡⚡ Excellent |
| **Offline access** | ❌ No | ✅ Yes |
| **Setup complexity** | Medium | Easy |
| **Team sharing** | ✅ Built-in | ❌ Manual |
| **Version control** | ✅ Git | Manual Git |
| **Cost** | Free | Free |

---

**Congratulations!** 🎉

You now have a complete, production-ready skills system that syncs across all your devices.

**Questions or issues?**
- Review the Troubleshooting section
- Check Claude logs
- Create an issue in your skills repository

**Happy coding with Claude!** 🚀

---

*Last updated: January 16, 2026*
*Version: 1.1.0*
