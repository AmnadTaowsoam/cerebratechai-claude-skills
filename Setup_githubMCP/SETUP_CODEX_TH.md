# 🟢 คู่มือตั้งค่า OpenAI Codex & GitHub Copilot

คู่มือครบวงจรสำหรับการใช้ CerebraTechAI Skills กับ OpenAI Codex และ GitHub Copilot

---

## 📋 ภาพรวม

**สองวิธีในการใช้ skills:**
1. **OpenAI Codex** - ใช้ MCP (Model Context Protocol) เชื่อมต่อ GitHub โดยตรง ⭐ **แนะนำ**
2. **GitHub Copilot** - ใช้ workspace indexing และ custom instructions

### สิ่งที่คุณจะได้รับ
- ✅ Code suggestions ที่รู้จัก skills
- ✅ Context จาก 473+ production-ready skills
- ✅ Best practices ใน inline suggestions
- ✅ Auto-sync (Codex MCP) หรือ Manual sync (Copilot)

---

## 🎯 วิธีที่ 1: OpenAI Codex กับ MCP (แนะนำ)

### สิ่งที่ต้องเตรียม
- ✅ OpenAI Codex ติดตั้งแล้ว
- ✅ Node.js 18+
- ✅ GitHub Personal Access Token

### ขั้นตอนการตั้งค่า

#### ขั้นที่ 1: สร้าง GitHub Token

1. ไปที่: https://github.com/settings/tokens
2. สร้าง **Fine-grained token**:
   - ชื่อ: `Codex MCP - Skills`
   - Repository: `cerebraSkills`
   - สิทธิ์: `Contents: Read-only`
3. คัดลอก token (ขึ้นต้นด้วย `github_pat_`)

#### ขั้นที่ 2: ตั้งค่า Codex MCP

**ตัวเลือก A: ใช้ CLI (ง่ายที่สุด)**

```bash
codex mcp add cerebratechai-skills \
  --env GITHUB_PERSONAL_ACCESS_TOKEN=YOUR_TOKEN_HERE \
  --env GITHUB_OWNER=AmnadTaowsoam \
  --env GITHUB_REPO=cerebraSkills \
  --env GITHUB_BRANCH=main \
  -- npx -y @modelcontextprotocol/server-github
```

**ตัวเลือก B: แก้ไข config.toml**

ตำแหน่ง: `~/.codex/config.toml`

```toml
[mcp_servers.cerebratechai-skills]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]

[mcp_servers.cerebratechai-skills.env]
GITHUB_PERSONAL_ACCESS_TOKEN = "YOUR_TOKEN_HERE"
GITHUB_OWNER = "AmnadTaowsoam"
GITHUB_REPO = "cerebraSkills"
GITHUB_BRANCH = "main"
```

#### ขั้นที่ 3: ตรวจสอบการเชื่อมต่อ

```bash
# ใน Codex TUI
codex

# ตรวจสอบ MCP servers
/mcp
```

ควรเห็น `cerebratechai-skills` ในรายการ

### การใช้งาน Codex MCP

```
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns

Create a Next.js API endpoint
```

### ข้อดีของ Codex MCP
- ✅ **Auto-sync**: ทันสมัยเสมอจาก GitHub
- ✅ **ไม่ต้อง clone**: ทำงานได้โดยไม่ต้องมี local repository
- ✅ **ตั้งค่าง่าย**: ใช้คำสั่งเดียว
- ✅ **Config ร่วมกัน**: ใช้ได้ทั้ง CLI และ IDE extension

---

## 🔧 วิธีที่ 2: GitHub Copilot กับ Workspace Indexing

### ขั้นที่ 1: ติดตั้ง GitHub Copilot

1. **เปิด VS Code**
2. **กด** `Cmd+Shift+X` (macOS) หรือ `Ctrl+Shift+X` (Windows/Linux)
3. **ค้นหา**: "GitHub Copilot"
4. **ติดตั้ง** ทั้งสอง extensions:
   - GitHub Copilot
   - GitHub Copilot Chat

### ขั้นที่ 2: Clone Repository

```bash
# เลือกตำแหน่งที่ต้องการ
cd ~/projects

# Clone repository
git clone https://github.com/AmnadTaowsoam/cerebraSkills.git

# เข้าไปในโฟลเดอร์
cd cerebraSkills
```

### ขั้นที่ 3: เปิดใน VS Code

```bash
# เปิด repository ใน VS Code
code .
```

หรือ: File → Open Folder → เลือก `cerebraSkills`

### ขั้นที่ 4: ตั้งค่า Copilot Workspace

สร้างไฟล์ `.vscode/settings.json` ใน repository:

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

### ขั้นที่ 5: สร้าง Copilot Instructions

สร้างไฟล์ `.copilot-instructions.md` ใน root ของ repository:

```markdown
# GitHub Copilot Instructions สำหรับ CerebraTechAI Skills

## Context ของ Repository
Repository นี้มี 473+ production-ready coding skills ใน 73 หมวดหมู่
แต่ละ skill มี best practices, ตัวอย่างโค้ด, anti-patterns, และกลยุทธ์การทดสอบ

## การจัดระเบียบ Skills

### โครงสร้างโฟลเดอร์
- `00-meta-skills/` - แนวทางสถาปัตยกรรมและการตัดสินใจ
- `01-foundations/` - มาตรฐานพื้นฐาน (TypeScript, Python, Git)
- `02-frontend/` - Frontend patterns (React, Next.js, Tailwind)
- `03-backend-api/` - Backend patterns (Node.js, FastAPI, Express)
- `04-database/` - Database design (Prisma, MongoDB, Redis)
- `05-ai-ml-core/` - ML training และ deployment
- `06-ai-ml-production/` - Production AI/ML (LLM, RAG, embeddings)
- ... (ดูรายการเต็มใน README.md)

## แนวทางการใช้งาน

### เมื่อสร้างโค้ด TypeScript
- อ้างอิง: `01-foundations/typescript-standards/SKILL.md`
- ใช้ strict typing พร้อม type annotations ที่ชัดเจน
- ใช้ camelCase สำหรับตัวแปร, PascalCase สำหรับ classes
- ใช้ UPPER_SNAKE_CASE สำหรับ constants
- หลีกเลี่ยง `any` type, ใช้ `unknown` แทน

### เมื่อสร้างโค้ด Next.js
- อ้างอิง: `02-frontend/nextjs-patterns/SKILL.md`
- ใช้ App Router (app directory)
- ใช้ Server Components เป็นค่าเริ่มต้น
- ใช้ Client Components เฉพาะเมื่อจำเป็น

### เมื่อสร้าง API
- อ้างอิง: `03-backend-api/nodejs-api/SKILL.md`
- ใช้ error handling ที่เหมาะสม
- ใช้ validation (Zod สำหรับ TypeScript)
- ปฏิบัติตาม RESTful conventions

### เมื่อทำงานกับ Database
- อ้างอิง: `04-database/prisma-guide/SKILL.md`
- ใช้ Prisma schema best practices
- ใช้ migrations ที่เหมาะสม
- ใช้ transactions สำหรับ multi-step operations

## กฎการสร้างโค้ด

1. **ตรวจสอบไฟล์ skill ที่เกี่ยวข้อง** ก่อนสร้างโค้ด
2. **ปฏิบัติตาม patterns** ที่กำหนดใน skills
3. **ใช้ security best practices** จาก skills
4. **ใช้ testing patterns** จาก 16-testing/ skills
5. **รวม error handling** ตามแนวทางใน skills

## ตัวอย่าง Patterns

### TypeScript Function
```typescript
// ✅ ดี - ปฏิบัติตาม typescript-standards
function calculateTotal(price: number, tax: number): number {
  if (price < 0 || tax < 0) {
    throw new Error('Price and tax must be non-negative');
  }
  return price + (price * tax);
}

// ❌ ไม่ดี - ไม่ปฏิบัติตามมาตรฐาน
function calc(p, t) {
  return p + p * t;
}
```

## Anti-Patterns ที่ต้องหลีกเลี่ยง

1. ❌ ใช้ `any` type ใน TypeScript
2. ❌ ไม่ validate user input
3. ❌ เปิดเผยข้อมูลสำคัญใน error messages
4. ❌ ไม่จัดการ async errors
5. ❌ Hardcode credentials
6. ❌ ไม่ใช้ environment variables

---

**จำไว้**: Skills เหล่านี้เป็น production-ready best practices
จงให้ความสำคัญกับ code quality, security, และ maintainability เสมอ
```

### ขั้นที่ 6: ตั้งค่า Copilot Chat

1. **เปิด Copilot Chat** (`Cmd+Shift+I` หรือ `Ctrl+Shift+I`)
2. **คลิก** ไอคอน settings
3. **เปิด** "Use workspace context"

---

## 💡 ตัวอย่างการใช้งาน

### วิธีที่ 1: ใช้ Comment

```typescript
// ปฏิบัติตาม typescript-standards และ nextjs-patterns skills
// สร้าง Next.js API route สำหรับ user authentication ด้วย JWT

// Copilot จะแนะนำโค้ดตาม skills
```

### วิธีที่ 2: Copilot Chat กับ @workspace

```
@workspace ใช้ typescript-standards skill
สร้าง type-safe API client สำหรับ REST API
```

### วิธีที่ 3: Inline Suggestions

```typescript
// เริ่มพิมพ์และ Copilot จะแนะนำตาม skills context
const userService = // Copilot แนะนำ implementation
```

### วิธีที่ 4: อธิบายโค้ดด้วย Skills Context

```
@workspace อธิบายโค้ดนี้และแนะนำการปรับปรุง
ตาม nextjs-patterns skill
```

---

## 🎯 Best Practices

### 1. เปิด Repository ไว้เสมอ
เปิด skills repository ไว้ใน workspace เสมอเพื่อ context ที่ดีที่สุด

### 2. อ้างอิง Skills เฉพาะเจาะจง
```typescript
// Reference: 01-foundations/typescript-standards/SKILL.md
// ช่วยให้ Copilot เข้าใจว่าควรให้ความสำคัญกับ skill ไหน
```

### 3. ใช้ Comments ที่อธิบายชัดเจน
```typescript
// สร้าง user authentication ตาม jwt-authentication skill
// พร้อม error handling และ validation ที่เหมาะสม
```

### 4. ตรวจสอบ Suggestions
ตรวจสอบ suggestions ของ Copilot กับไฟล์ skill จริงเสมอ

### 5. อัปเดตเป็นประจำ
```bash
# Pull skills ล่าสุด
cd ~/projects/cerebraSkills
git pull origin main
```

---

## 🔄 อัปเดต Skills

เพื่อรับ skills ล่าสุด:

```bash
# ไปที่ repository
cd ~/projects/cerebraSkills

# Pull การเปลี่ยนแปลงล่าสุด
git pull origin main

# Reload VS Code window
# Cmd+Shift+P → "Developer: Reload Window"
```

---

## 🆚 เปรียบเทียบกับวิธีอื่น

| คุณสมบัติ | Copilot | MCP (Claude/Cursor) |
|---------|---------|---------------------|
| การตั้งค่า | ปานกลาง | ง่าย |
| Auto-sync | Manual (git pull) | อัตโนมัติ |
| Offline | ✅ ใช่ | ❌ ไม่ (MCP) |
| Inline suggestions | ✅ ใช่ | ⚠️ จำกัด |
| Chat integration | ✅ ใช่ | ✅ ใช่ |
| Context awareness | ⚠️ Workspace เท่านั้น | ✅ เสมอ |

---

## 🆘 แก้ปัญหา

### ปัญหา: Copilot ไม่ใช้ skills context

**วิธีแก้:**
1. ตรวจสอบว่ามี `.copilot-instructions.md` ใน root
2. ตรวจสอบ `.vscode/settings.json` ตั้งค่าแล้ว
3. Reload VS Code window
4. เปิด "Use workspace context" ใน Copilot Chat

### ปัญหา: Suggestions ไม่ปฏิบัติตาม skills

**วิธีแก้:**
1. เพิ่ม comments อ้างอิง skills อย่างชัดเจน
2. ใช้ `@workspace` ใน Copilot Chat
3. ตรวจสอบว่า repository เปิดอยู่ใน workspace
4. ตรวจสอบว่าไฟล์ skill ไม่อยู่ใน `.gitignore`

### ปัญหา: Suggestions ช้า

**วิธีแก้:**
1. ลด `contextFiles` ใน settings
2. จำกัด `length` parameter
3. ปิดไฟล์ที่ไม่จำเป็น
4. Restart VS Code

---

## 📚 แหล่งข้อมูลเพิ่มเติม

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [VS Code Copilot Guide](https://code.visualstudio.com/docs/editor/github-copilot)
- [ภาพรวม Skills ทั้งหมด](./README.md)
- [ดัชนี Skills](./SKILL_INDEX.md)

---

## 🎓 เส้นทางการเรียนรู้

### ระดับเริ่มต้น
1. เริ่มจาก `01-foundations/` skills
2. ใช้ Copilot Chat กับ `@workspace`
3. ตรวจสอบ suggestions กับไฟล์ skill

### ระดับกลาง
1. อ้างอิง skills เฉพาะเจาะจงใน comments
2. ใช้หลาย skills ร่วมกัน
3. ปรับแต่ง `.copilot-instructions.md`

### ระดับสูง
1. สร้าง instructions เฉพาะโปรเจกต์
2. รวมกับ `.cursorrules` แบบ local
3. สร้างชุด skill combinations เอง

---

**อัปเดตล่าสุด**: 17 มกราคม 2026  
**Repository**: https://github.com/AmnadTaowsoam/cerebraSkills  
**License**: MIT
