# Quick Start Guide

เริ่มใช้ Claude Skills ใน 5 นาที

---

## 1. Setup (ครั้งเดียว)

### Option A: GitHub MCP (แนะนำ)

```json
// เพิ่มใน claude_desktop_config.json
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "cerebratechai-claude-skills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

### Option B: Local Clone

```bash
git clone https://github.com/AmnadTaowsoam/cerebratechai-claude-skills.git
```

---

## 2. วิธีใช้งาน

### Basic Usage

```
ใช้ skill [ชื่อ skill] สร้าง [สิ่งที่ต้องการ]
```

**ตัวอย่าง:**
```
ใช้ skill typescript-standards สร้าง function คำนวณราคา
```

### Multiple Skills

```
ใช้ skills:
- typescript-standards
- prisma-guide
- jwt-authentication

สร้าง user authentication API
```

---

## 3. หา Skill ที่ต้องการ

### ตาม Technology

| ต้องการ | ใช้ Skill |
|---------|-----------|
| TypeScript | `typescript-standards` |
| React/Next.js | `nextjs-patterns`, `react-best-practices` |
| Python API | `fastapi-patterns`, `python-standards` |
| Database | `prisma-guide`, `mongodb-patterns` |
| Auth | `jwt-authentication`, `oauth2-implementation` |
| AI/LLM | `llm-integration`, `rag-implementation` |

### ตาม Project Type

| Project | Skills แนะนำ |
|---------|-------------|
| **SaaS Web App** | `nextjs-patterns`, `prisma-guide`, `stripe-integration` |
| **REST API** | `fastapi-patterns`, `error-handling`, `validation` |
| **AI App** | `llm-integration`, `rag-implementation`, `prompt-engineering` |
| **E-commerce** | `shopping-cart`, `payment-gateways`, `inventory-management` |

---

## 4. Feedback Loop

พบปัญหาหรือมีวิธีที่ดีกว่า? บอก Claude ได้เลย:

```
skill [ชื่อ skill] พบปัญหา:
- ปัญหา: [อธิบาย]
- แก้ไขโดย: [วิธีแก้]

ช่วยอัปเดต skill ด้วย
```

---

## 5. Quick Reference

### Skill Categories

```
00 - Meta Skills (การคิดเชิงระบบ)
01 - Foundations (พื้นฐาน)
02 - Frontend
03 - Backend API
04 - Database
05 - AI/ML Core
06 - AI/ML Production
07 - Document Processing
08 - Messaging Queue
09 - Microservices
10 - Authentication
11 - Billing
12 - Compliance
13 - File Storage
14 - Monitoring
15 - DevOps
16 - Testing
17 - Domain-Specific
18 - Project Management
19 - SEO
20 - AI Integration
21 - Documentation
22 - UX/UI Design
23 - Business Analytics
24 - Security
25 - i18n
26 - Deployment
27 - Team Collaboration
28-39 - Specialized (E-commerce, Mobile, CRM, etc.)
40-58 - Enterprise (Resilience, Cost, Data, etc.)
```

### Popular Skills

| Skill | ใช้สำหรับ |
|-------|----------|
| `typescript-standards` | TypeScript coding standards |
| `nextjs-patterns` | Next.js 14+ App Router |
| `fastapi-patterns` | Python FastAPI |
| `prisma-guide` | Prisma ORM |
| `jwt-authentication` | JWT auth |
| `llm-integration` | LLM (OpenAI, Claude) |
| `docker-patterns` | Docker containerization |
| `ci-cd-github-actions` | GitHub Actions CI/CD |

---

## Next Steps

- [README.md](README.md) - รายละเอียดทั้งหมด
- [SKILL_INDEX.md](SKILL_INDEX.md) - ดัชนี Skills ทั้งหมด
- [USE_CASES.md](USE_CASES.md) - ตัวอย่างการใช้งานจริง
- [GITHUB_MCP_SETUP.md](GITHUB_MCP_SETUP.md) - คู่มือ setup แบบละเอียด
