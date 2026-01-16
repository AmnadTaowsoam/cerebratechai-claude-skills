# 🤖 Setup Guide for All AI Coding Assistants

Complete guide for using CerebraTechAI Skills with multiple AI coding platforms

**Supported Platforms:**
- 🟣 **Claude Desktop** (via MCP)
- 🔵 **Claude Code** (VS Code extension)
- 🟢 **GitHub Codex** (via GitHub Copilot)
- 🟠 **Roo Code** (Cursor IDE)
- 🔴 **Antigravity** (Google DeepMind)

---

## 📋 Table of Contents

1. [Claude Desktop (MCP)](#1-claude-desktop-mcp)
2. [Claude Code (VS Code)](#2-claude-code-vs-code)
3. [GitHub Codex (Copilot)](#3-github-codex-copilot)
4. [Roo Code (Cursor)](#4-roo-code-cursor)
5. [Antigravity (Google DeepMind)](#5-antigravity-google-deepmind)
6. [Comparison Table](#comparison-table)

---

## 1. 🟣 Claude Desktop (MCP)

### Overview
Use Model Context Protocol (MCP) to connect Claude Desktop directly to this GitHub repository.

### Prerequisites
- Claude Desktop installed
- Node.js 18+
- GitHub Personal Access Token

### Setup Steps

#### Step 1: Create GitHub Token
1. Go to: https://github.com/settings/tokens
2. Create **Fine-grained token**:
   - Name: `Claude MCP - Skills`
   - Repository: `cerebratechai-claude-skills`
   - Permissions: `Contents: Read-only`
3. Copy token (starts with `github_pat_`)

#### Step 2: Configure Claude Desktop

**Windows:**
```powershell
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

**macOS:**
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Linux:**
```bash
nano ~/.config/Claude/claude_desktop_config.json
```

**Configuration:**
```json
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN_HERE",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "cerebratechai-claude-skills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

#### Step 3: Restart Claude Desktop

**Windows:** Quit from System Tray → Restart  
**macOS:** `killall Claude && open -a Claude`  
**Linux:** `pkill -f claude && claude &`

### Usage
```
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns

Create a Next.js API endpoint
```

### Documentation
- 🇬🇧 [GITHUB_MCP_SETUP.md](./GITHUB_MCP_SETUP.md)
- 🇹🇭 [SETUP_TH.md](./SETUP_TH.md)
- ⚡ [QUICKSTART_MCP.md](./QUICKSTART_MCP.md)

---

## 2. 🔵 Claude Code (VS Code)

### Overview
Claude Code extension for VS Code uses the same MCP configuration as Claude Desktop.

### Prerequisites
- VS Code installed
- Claude Code extension
- Same config as Claude Desktop

### Setup Steps

#### Step 1: Install Extension
1. Open VS Code
2. Press `Cmd+Shift+X` (macOS) or `Ctrl+Shift+X` (Windows/Linux)
3. Search: **"Claude Code"**
4. Click **Install**

#### Step 2: Configuration
**Good news!** Claude Code uses the **same config file** as Claude Desktop.

If you've already set up Claude Desktop (Section 1), you're done! ✅

If not, follow the same configuration steps from Section 1.

#### Step 3: Reload VS Code
```
Cmd+Shift+P (or Ctrl+Shift+P)
→ "Developer: Reload Window"
```

### Usage

**Open Claude Code:**
- `Cmd+Shift+/` (macOS)
- `Ctrl+Shift+/` (Windows/Linux)

**Example:**
```
Using cerebratechai-skills:
- prisma-guide
- typescript-standards

Create a Prisma schema for a blog
```

---

## 3. 🟢 GitHub Codex (Copilot)

### Overview
Use this repository as context for GitHub Copilot through workspace indexing.

### Prerequisites
- GitHub Copilot subscription
- VS Code with Copilot extension
- Repository cloned locally

### Setup Steps

#### Step 1: Clone Repository
```bash
cd ~/projects
git clone https://github.com/AmnadTaowsoam/cerebratechai-claude-skills.git
cd cerebratechai-claude-skills
```

#### Step 2: Open in VS Code
```bash
code .
```

#### Step 3: Configure Copilot Workspace

Create `.vscode/settings.json`:
```json
{
  "github.copilot.advanced": {
    "contextFiles": [
      "**/*.md",
      "**/SKILL.md"
    ]
  },
  "github.copilot.enable": {
    "*": true,
    "markdown": true
  }
}
```

#### Step 4: Index Skills

Create `.copilot-instructions.md` in project root:
```markdown
# Copilot Instructions

## Context
This repository contains production-ready coding skills and best practices.

## Skills Location
Skills are organized in folders:
- 00-meta-skills/ - Architectural practices
- 01-foundations/ - Core standards
- 02-frontend/ - Frontend patterns
- 03-backend-api/ - Backend patterns
- [etc...]

## Usage
When generating code, reference skills from the appropriate folder.
Follow the patterns and best practices defined in SKILL.md files.

## Example
For TypeScript code, reference: 01-foundations/typescript-standards/SKILL.md
For Next.js code, reference: 02-frontend/nextjs-patterns/SKILL.md
```

### Usage

**Method 1: Comment-based**
```typescript
// Following typescript-standards and nextjs-patterns skills
// Create a Next.js API route for user authentication

// Copilot will suggest code based on skills
```

**Method 2: Copilot Chat**
```
@workspace Using the typescript-standards skill,
create a type-safe API client
```

### Tips
- Keep repository open in workspace
- Reference specific skill files in comments
- Use `@workspace` in Copilot Chat

---

## 4. 🟠 Roo Code (Cursor)

### Overview
Cursor IDE (Roo Code) can index this repository for AI-assisted coding.

### Prerequisites
- Cursor IDE installed
- Repository cloned locally

### Setup Steps

#### Step 1: Clone Repository
```bash
cd ~/projects
git clone https://github.com/AmnadTaowsoam/cerebratechai-claude-skills.git
```

#### Step 2: Open in Cursor
```bash
cursor cerebratechai-claude-skills
```

Or: File → Open Folder → Select `cerebratechai-claude-skills`

#### Step 3: Configure Cursor Rules

Create `.cursorrules` in project root:
```markdown
# CerebraTechAI Skills - Cursor Rules

## Context
This repository contains 473+ production-ready coding skills across 73 categories.

## Skill Structure
Each skill is in a folder with SKILL.md containing:
- Best practices
- Code examples
- Anti-patterns
- Testing strategies

## Usage Guidelines

### When writing TypeScript:
- Reference: 01-foundations/typescript-standards/SKILL.md
- Use strict typing
- Follow naming conventions

### When writing Next.js:
- Reference: 02-frontend/nextjs-patterns/SKILL.md
- Use App Router patterns
- Follow file structure conventions

### When writing APIs:
- Reference: 03-backend-api/nodejs-api/SKILL.md or fastapi-patterns/SKILL.md
- Implement proper error handling
- Use validation patterns

### When working with databases:
- Reference: 04-database/prisma-guide/SKILL.md
- Follow schema best practices
- Implement proper migrations

## General Rules
1. Always check relevant skill file before generating code
2. Follow the patterns defined in skills
3. Apply security best practices from skills
4. Use testing patterns from 16-testing/ skills

## Skill Categories
- 00-meta-skills: Architecture & decisions
- 01-foundations: Core standards (TypeScript, Python, Git)
- 02-frontend: React, Next.js, Tailwind
- 03-backend-api: Node.js, FastAPI, Express
- 04-database: Prisma, MongoDB, Redis
- 05-ai-ml-core: PyTorch, YOLO, training
- 06-ai-ml-production: LLM, RAG, embeddings
- [... see README.md for full list]
```

#### Step 4: Index Repository

1. Open Cursor Settings (`Cmd+,` or `Ctrl+,`)
2. Go to **Features** → **Codebase Indexing**
3. Enable **"Index entire workspace"**
4. Click **"Reindex"**

### Usage

**Method 1: Cmd+K (Inline Edit)**
```typescript
// Select code or place cursor
// Press Cmd+K (or Ctrl+K)
// Type: "Refactor following typescript-standards skill"
```

**Method 2: Cmd+L (Chat)**
```
Using skills from this repository:
- typescript-standards
- nextjs-patterns
- jwt-authentication

Create a complete auth system for Next.js
```

**Method 3: @ Mentions**
```
@cerebratechai-claude-skills/01-foundations/typescript-standards/SKILL.md

Apply these standards to my current file
```

### Tips
- Use `@Docs` to reference skill files
- Keep skills repo in workspace
- Use Cmd+K for quick refactoring
- Use Cmd+L for complex tasks

---

## 5. 🔴 Antigravity (Google DeepMind)

### Overview
Antigravity can access this repository through MCP or direct file access.

### Prerequisites
- Antigravity installed
- Node.js 18+ (for MCP)
- Repository access

### Setup Method 1: MCP (Recommended)

#### Step 1: Create GitHub Token
Same as Claude Desktop (Section 1, Step 1)

#### Step 2: Configure Antigravity

**Windows:**
```powershell
notepad "$env:APPDATA\Antigravity\config.json"
```

**macOS:**
```bash
nano ~/Library/Application\ Support/Antigravity/config.json
```

**Linux:**
```bash
nano ~/.config/Antigravity/config.json
```

**Configuration:**
```json
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN_HERE",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "cerebratechai-claude-skills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

#### Step 3: Restart Antigravity

### Setup Method 2: Local Files

#### Step 1: Clone Repository
```bash
cd ~/projects
git clone https://github.com/AmnadTaowsoam/cerebratechai-claude-skills.git
```

#### Step 2: Configure Skills Path

Create `~/.antigravity/skills.json`:
```json
{
  "skillsRepositories": [
    {
      "name": "cerebratechai-skills",
      "path": "/Users/YOUR_USERNAME/projects/cerebratechai-claude-skills",
      "enabled": true
    }
  ]
}
```

Replace `/Users/YOUR_USERNAME/projects/` with your actual path.

### Usage

**Method 1: Direct Reference**
```
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns
- prisma-guide

Create a Next.js app with Prisma
```

**Method 2: Skill Invocation**
```
@skill typescript-standards
@skill nextjs-patterns

Generate a type-safe API client
```

**Method 3: Context Loading**
```
Load context from cerebratechai-skills:
- 01-foundations/
- 02-frontend/
- 03-backend-api/

Now help me build a full-stack app
```

---

## 📊 Comparison Table

| Feature | Claude Desktop | Claude Code | GitHub Codex | Roo Code | Antigravity |
|---------|---------------|-------------|--------------|----------|-------------|
| **Setup Difficulty** | ⭐⭐ Easy | ⭐ Very Easy | ⭐⭐⭐ Medium | ⭐⭐ Easy | ⭐⭐ Easy |
| **MCP Support** | ✅ Yes | ✅ Yes | ❌ No | ❌ No | ✅ Yes |
| **Auto-sync** | ✅ Yes | ✅ Yes | ⚠️ Manual | ⚠️ Manual | ✅ Yes |
| **Offline Mode** | ❌ No | ❌ No | ✅ Yes | ✅ Yes | ⚠️ Partial |
| **IDE Integration** | ❌ No | ✅ VS Code | ✅ VS Code | ✅ Cursor | ✅ Multiple |
| **Skill Indexing** | ✅ Automatic | ✅ Automatic | ⚠️ Manual | ✅ Automatic | ✅ Automatic |
| **Context Window** | Large | Large | Medium | Large | Very Large |
| **Best For** | Standalone | VS Code | GitHub users | Cursor users | Multi-IDE |

### Legend
- ✅ Full support
- ⚠️ Partial support / Manual setup
- ❌ Not supported
- ⭐ Difficulty (1-5 stars)

---

## 🎯 Recommendations

### Choose Claude Desktop/Code if:
- ✅ You want automatic sync from GitHub
- ✅ You prefer MCP protocol
- ✅ You use VS Code
- ✅ You want the easiest setup

### Choose GitHub Codex if:
- ✅ You already use GitHub Copilot
- ✅ You work primarily in VS Code
- ✅ You want inline suggestions
- ✅ You're comfortable with workspace indexing

### Choose Roo Code (Cursor) if:
- ✅ You use Cursor IDE
- ✅ You want powerful AI editing
- ✅ You prefer Cmd+K inline edits
- ✅ You want codebase-aware AI

### Choose Antigravity if:
- ✅ You use multiple IDEs
- ✅ You want maximum flexibility
- ✅ You need very large context windows
- ✅ You want advanced AI capabilities

---

## 🔄 Multi-Platform Setup

You can use **multiple platforms simultaneously**!

### Recommended Combination:
1. **Claude Desktop** (MCP) - For general queries and planning
2. **Claude Code** (VS Code) - For coding in VS Code
3. **Roo Code** (Cursor) - For AI-assisted editing in Cursor

All three can share the same GitHub repository and stay in sync!

### Setup Order:
1. Set up Claude Desktop (MCP) first
2. Claude Code automatically works (same config)
3. Clone repo locally for Roo Code/Codex
4. Configure Antigravity if needed

---

## 📚 Additional Resources

### Documentation
- 📖 [GITHUB_MCP_SETUP.md](./GITHUB_MCP_SETUP.md) - Complete MCP guide
- 🇹🇭 [SETUP_TH.md](./SETUP_TH.md) - Thai language guide
- ⚡ [QUICKSTART_MCP.md](./QUICKSTART_MCP.md) - 5-minute setup
- ✅ [MCP_DEPLOYMENT_CHECKLIST.md](./MCP_DEPLOYMENT_CHECKLIST.md) - Deployment checklist

### Skills
- 📋 [README.md](./README.md) - All 473+ skills overview
- 📑 [SKILL_INDEX.md](./SKILL_INDEX.md) - Detailed skill index

### Community
- 🐛 [Issues](https://github.com/AmnadTaowsoam/cerebratechai-claude-skills/issues)
- 💬 [Discussions](https://github.com/AmnadTaowsoam/cerebratechai-claude-skills/discussions)
- 🤝 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 🆘 Troubleshooting

### Common Issues

#### MCP Connection Failed (Claude/Antigravity)
- Verify Node.js 18+ installed: `node --version`
- Check token hasn't expired
- Validate JSON syntax
- Restart application

#### Skills Not Indexed (Codex/Roo Code)
- Ensure repository is in workspace
- Trigger manual reindex
- Check `.vscode/settings.json` or `.cursorrules`
- Restart IDE

#### Outdated Skills
- **MCP users**: Automatic sync (no action needed)
- **Local users**: `git pull` to update

---

**Last Updated**: January 16, 2026  
**Repository**: https://github.com/AmnadTaowsoam/cerebratechai-claude-skills  
**License**: MIT
