# 🟢 GitHub Codex (Copilot) Setup Guide

Complete guide for using CerebraTechAI Skills with GitHub Copilot

---

## 📋 Overview

GitHub Copilot can use this skills repository as context through workspace indexing and custom instructions.

### What You'll Get
- ✅ Skills-aware code suggestions
- ✅ Context from 473+ production-ready skills
- ✅ Best practices in inline suggestions
- ✅ Works offline once indexed

---

## 🔧 Prerequisites

- ✅ GitHub Copilot subscription (Individual or Business)
- ✅ VS Code installed
- ✅ GitHub Copilot extension installed
- ✅ Repository cloned locally

---

## 🚀 Setup Steps

### Step 1: Install GitHub Copilot

1. **Open VS Code**
2. **Press** `Cmd+Shift+X` (macOS) or `Ctrl+Shift+X` (Windows/Linux)
3. **Search**: "GitHub Copilot"
4. **Install** both extensions:
   - GitHub Copilot
   - GitHub Copilot Chat

### Step 2: Clone Repository

```bash
# Choose your preferred location
cd ~/projects

# Clone the repository
git clone https://github.com/AmnadTaowsoam/cerebratechai-claude-skills.git

# Enter directory
cd cerebratechai-claude-skills
```

### Step 3: Open in VS Code

```bash
# Open repository in VS Code
code .
```

Or: File → Open Folder → Select `cerebratechai-claude-skills`

### Step 4: Configure Copilot Workspace

Create `.vscode/settings.json` in the repository:

```json
{
  "github.copilot.advanced": {
    "contextFiles": [
      "**/*.md",
      "**/SKILL.md",
      "**/*.json"
    ],
    "length": 4000
  },
  "github.copilot.enable": {
    "*": true,
    "markdown": true,
    "plaintext": true
  }
}
```

### Step 5: Create Copilot Instructions

Create `.copilot-instructions.md` in repository root:

```markdown
# GitHub Copilot Instructions for CerebraTechAI Skills

## Repository Context
This repository contains 473+ production-ready coding skills across 73 categories.
Each skill provides best practices, code examples, anti-patterns, and testing strategies.

## Skill Organization

### Directory Structure
- `00-meta-skills/` - Architectural practices and decision-making
- `01-foundations/` - Core standards (TypeScript, Python, Git)
- `02-frontend/` - Frontend patterns (React, Next.js, Tailwind)
- `03-backend-api/` - Backend patterns (Node.js, FastAPI, Express)
- `04-database/` - Database design (Prisma, MongoDB, Redis)
- `05-ai-ml-core/` - ML training and deployment
- `06-ai-ml-production/` - Production AI/ML (LLM, RAG, embeddings)
- `07-document-processing/` - OCR and document parsing
- `08-messaging-queue/` - Message queuing systems
- `09-microservices/` - Microservices architecture
- `10-authentication-authorization/` - Auth and security
- ... (see README.md for complete list)

## Usage Guidelines

### When Generating TypeScript Code
- Reference: `01-foundations/typescript-standards/SKILL.md`
- Use strict typing with explicit type annotations
- Follow camelCase for variables, PascalCase for classes
- Use UPPER_SNAKE_CASE for constants
- Avoid `any` type, use `unknown` instead
- Enable strict mode in tsconfig.json

### When Generating Next.js Code
- Reference: `02-frontend/nextjs-patterns/SKILL.md`
- Use App Router (app directory)
- Implement Server Components by default
- Use Client Components only when needed
- Follow file-based routing conventions
- Implement proper error boundaries

### When Generating API Code
- Reference: `03-backend-api/nodejs-api/SKILL.md` or `fastapi-patterns/SKILL.md`
- Implement proper error handling
- Use validation (Zod for TypeScript, Pydantic for Python)
- Follow RESTful conventions
- Include proper status codes
- Implement rate limiting

### When Working with Databases
- Reference: `04-database/prisma-guide/SKILL.md`
- Use Prisma schema best practices
- Implement proper migrations
- Use transactions for multi-step operations
- Implement connection pooling
- Add proper indexes

### When Implementing Authentication
- Reference: `10-authentication-authorization/jwt-authentication/SKILL.md`
- Use JWT with proper expiration
- Implement refresh tokens
- Hash passwords with bcrypt
- Use HTTPS only
- Implement CSRF protection

### When Writing Tests
- Reference: `16-testing/jest-patterns/SKILL.md` or `pytest-patterns/SKILL.md`
- Write unit tests for all functions
- Use descriptive test names
- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies
- Aim for 80%+ coverage

## Code Generation Rules

1. **Always check relevant skill file** before generating code
2. **Follow the patterns** defined in skills
3. **Apply security best practices** from skills
4. **Use testing patterns** from 16-testing/ skills
5. **Include error handling** as per skill guidelines
6. **Add comments** for complex logic
7. **Use TypeScript** for type safety when applicable

## Example Patterns

### TypeScript Function
```typescript
// ✅ Good - Following typescript-standards
function calculateTotal(price: number, tax: number): number {
  if (price < 0 || tax < 0) {
    throw new Error('Price and tax must be non-negative');
  }
  return price + (price * tax);
}

// ❌ Bad - Not following standards
function calc(p, t) {
  return p + p * t;
}
```

### Next.js API Route
```typescript
// ✅ Good - Following nextjs-patterns
import { NextResponse } from 'next/server';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const data = schema.parse(body);
    
    // Process data
    return NextResponse.json({ success: true });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      );
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## Anti-Patterns to Avoid

1. ❌ Using `any` type in TypeScript
2. ❌ Not validating user input
3. ❌ Exposing sensitive data in error messages
4. ❌ Not handling async errors
5. ❌ Hardcoding credentials
6. ❌ Not using environment variables
7. ❌ Skipping error boundaries in React
8. ❌ Not implementing proper logging

## When in Doubt

If you're unsure about a pattern:
1. Check the relevant SKILL.md file
2. Look for code examples in the skill
3. Review the "Common Pitfalls" section
4. Follow the "Best Practices" checklist

## Skill Categories Quick Reference

- **Meta & Architecture**: 00-meta-skills, 59-architecture-decision
- **Core Development**: 01-foundations, 45-developer-experience
- **Frontend**: 02-frontend, 22-ux-ui-design
- **Backend**: 03-backend-api, 09-microservices
- **Data**: 04-database, 43-data-reliability, 53-data-engineering
- **AI/ML**: 05-ai-ml-core, 06-ai-ml-production, 52-ai-evaluation
- **Security**: 10-authentication-authorization, 24-security-practices
- **Testing**: 16-testing
- **DevOps**: 15-devops-infrastructure, 26-deployment-strategies
- **Monitoring**: 14-monitoring-observability, 41-incident-management

---

**Remember**: These skills represent production-ready best practices.
Always prioritize code quality, security, and maintainability.
```

### Step 6: Configure Copilot Chat

1. **Open Copilot Chat** (`Cmd+Shift+I` or `Ctrl+Shift+I`)
2. **Click** the settings icon
3. **Enable** "Use workspace context"

---

## 💡 Usage Examples

### Method 1: Comment-Based Suggestions

```typescript
// Following typescript-standards and nextjs-patterns skills
// Create a Next.js API route for user authentication with JWT

// Copilot will suggest code based on skills
```

### Method 2: Copilot Chat with @workspace

```
@workspace Using the typescript-standards skill,
create a type-safe API client for a REST API
```

### Method 3: Inline Suggestions

```typescript
// Start typing and Copilot will suggest based on skills context
const userService = // Copilot suggests implementation
```

### Method 4: Explain Code with Skills Context

```
@workspace Explain this code and suggest improvements
based on the nextjs-patterns skill
```

---

## 🎯 Best Practices

### 1. Keep Repository Open
Always have the skills repository open in your workspace for best context.

### 2. Reference Specific Skills
```typescript
// Reference: 01-foundations/typescript-standards/SKILL.md
// This helps Copilot understand which skill to prioritize
```

### 3. Use Descriptive Comments
```typescript
// Create user authentication following jwt-authentication skill
// with proper error handling and validation
```

### 4. Review Suggestions
Always review Copilot's suggestions against the actual skill files.

### 5. Update Regularly
```bash
# Pull latest skills
cd ~/projects/cerebratechai-claude-skills
git pull origin main
```

---

## 🔄 Updating Skills

To get the latest skills:

```bash
# Navigate to repository
cd ~/projects/cerebratechai-claude-skills

# Pull latest changes
git pull origin main

# Reload VS Code window
# Cmd+Shift+P → "Developer: Reload Window"
```

---

## 🆚 Comparison with Other Methods

| Feature | Copilot | MCP (Claude/Cursor) |
|---------|---------|---------------------|
| Setup | Medium | Easy |
| Auto-sync | Manual (git pull) | Automatic |
| Offline | ✅ Yes | ❌ No (MCP) |
| Inline suggestions | ✅ Yes | ⚠️ Limited |
| Chat integration | ✅ Yes | ✅ Yes |
| Context awareness | ⚠️ Workspace only | ✅ Always |

---

## 🆘 Troubleshooting

### Issue: Copilot not using skills context

**Solution:**
1. Ensure `.copilot-instructions.md` exists in root
2. Check `.vscode/settings.json` is configured
3. Reload VS Code window
4. Enable "Use workspace context" in Copilot Chat

### Issue: Suggestions not following skills

**Solution:**
1. Add explicit comments referencing skills
2. Use `@workspace` in Copilot Chat
3. Ensure repository is open in workspace
4. Check that skill files are not in `.gitignore`

### Issue: Slow suggestions

**Solution:**
1. Reduce `contextFiles` in settings
2. Limit `length` parameter
3. Close unnecessary files
4. Restart VS Code

---

## 📚 Additional Resources

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [VS Code Copilot Guide](https://code.visualstudio.com/docs/editor/github-copilot)
- [All Skills Overview](./README.md)
- [Skill Index](./SKILL_INDEX.md)

---

## 🎓 Learning Path

### Beginner
1. Start with `01-foundations/` skills
2. Use Copilot Chat with `@workspace`
3. Review suggestions against skill files

### Intermediate
1. Reference specific skills in comments
2. Use multiple skills together
3. Customize `.copilot-instructions.md`

### Advanced
1. Create project-specific instructions
2. Combine with local `.cursorrules`
3. Build custom skill combinations

---

**Last Updated**: January 17, 2026  
**Repository**: https://github.com/AmnadTaowsoam/cerebratechai-claude-skills  
**License**: MIT
