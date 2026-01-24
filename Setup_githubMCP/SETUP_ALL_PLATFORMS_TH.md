# 🤖 คู่มือตั้งค่าสำหรับ AI Coding Assistants ทุกตัว

คู่มือครบวงจรสำหรับการใช้ CerebraTechAI Skills กับ AI coding platforms ต่างๆ

**รองรับ:**
- 🟣 **Claude Desktop** (ผ่าน MCP)
- 🔵 **Claude Code** (VS Code extension)
- 🟢 **GitHub Codex** (ผ่าน GitHub Copilot)
- 🟠 **Roo Code** (Cursor IDE)
- 🔴 **Antigravity** (Google DeepMind)

---

## 📋 สารบัญ

1. [Claude Desktop (MCP)](#1-claude-desktop-mcp)
2. [Claude Code (VS Code)](#2-claude-code-vs-code)
3. [GitHub Codex (Copilot)](#3-github-codex-copilot)
4. [Roo Code (Cursor)](#4-roo-code-cursor)
5. [Antigravity (Google DeepMind)](#5-antigravity-google-deepmind)
6. [ตารางเปรียบเทียบ](#ตารางเปรียบเทียบ)

---

## 1. 🟣 Claude Desktop (MCP)

### ภาพรวม
ใช้ Model Context Protocol (MCP) เชื่อมต่อ Claude Desktop กับ GitHub repository นี้โดยตรง

### สิ่งที่ต้องเตรียม
- Claude Desktop ติดตั้งแล้ว
- Node.js 18+
- GitHub Personal Access Token

### ขั้นตอนการตั้งค่า

#### ขั้นที่ 1: สร้าง GitHub Token
1. ไปที่: https://github.com/settings/tokens
2. สร้าง **Fine-grained token**:
   - ชื่อ: `Claude MCP - Skills`
   - Repository: `cerebraSkills`
   - สิทธิ์: `Contents: Read-only`
3. คัดลอก token (ขึ้นต้นด้วย `github_pat_`)

#### ขั้นที่ 2: ตั้งค่า Claude Desktop

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

**โค้ดตั้งค่า:**
```json
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN_HERE",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

#### ขั้นที่ 3: Restart Claude Desktop

**Windows:** ปิดจาก System Tray → เปิดใหม่  
**macOS:** `killall Claude && open -a Claude`  
**Linux:** `pkill -f claude && claude &`

### วิธีใช้งาน
```
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns

Create a Next.js API endpoint
```

### เอกสารเพิ่มเติม
- 🇹🇭 [SETUP_TH.md](./SETUP_TH.md) - คู่มือภาษาไทยฉบับเต็ม
- ⚡ [QUICKSTART_MCP.md](./QUICKSTART_MCP.md) - ตั้งค่าใน 5 นาที

---

## 2. 🔵 Claude Code (VS Code)

### ภาพรวม
Claude Code extension สำหรับ VS Code ใช้การตั้งค่า MCP เดียวกับ Claude Desktop

### สิ่งที่ต้องเตรียม
- VS Code ติดตั้งแล้ว
- Claude Code extension
- ตั้งค่าเหมือน Claude Desktop

### ขั้นตอนการตั้งค่า

#### ขั้นที่ 1: ติดตั้ง Extension
1. เปิด VS Code
2. กด `Cmd+Shift+X` (macOS) หรือ `Ctrl+Shift+X` (Windows/Linux)
3. ค้นหา: **"Claude Code"**
4. คลิก **Install**

#### ขั้นที่ 2: การตั้งค่า
**ข่าวดี!** Claude Code ใช้**ไฟล์ config เดียวกัน**กับ Claude Desktop

ถ้าคุณตั้งค่า Claude Desktop แล้ว (ส่วนที่ 1) ก็เสร็จแล้ว! ✅

ถ้ายัง ให้ทำตามขั้นตอนเดียวกับส่วนที่ 1

#### ขั้นที่ 3: Reload VS Code
```
Cmd+Shift+P (หรือ Ctrl+Shift+P)
→ "Developer: Reload Window"
```

### วิธีใช้งาน

**เปิด Claude Code:**
- `Cmd+Shift+/` (macOS)
- `Ctrl+Shift+/` (Windows/Linux)

**ตัวอย่าง:**
```
Using cerebratechai-skills:
- prisma-guide
- typescript-standards

Create a Prisma schema for a blog
```

---

## 3. 🟢 GitHub Codex (Copilot)

### ภาพรวม
ใช้ repository นี้เป็น context สำหรับ GitHub Copilot ผ่าน workspace indexing

### สิ่งที่ต้องเตรียม
- GitHub Copilot subscription
- VS Code พร้อม Copilot extension
- Clone repository มาไว้ local

### ขั้นตอนการตั้งค่า

#### ขั้นที่ 1: Clone Repository
```bash
cd ~/projects
git clone https://github.com/AmnadTaowsoam/cerebraSkills.git
cd cerebraSkills
```

#### ขั้นที่ 2: เปิดใน VS Code
```bash
code .
```

#### ขั้นที่ 3: ตั้งค่า Copilot Workspace

สร้างไฟล์ `.vscode/settings.json`:
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

#### ขั้นที่ 4: Index Skills

สร้างไฟล์ `.copilot-instructions.md` ใน root:
```markdown
# Copilot Instructions

## Context
Repository นี้มี coding skills และ best practices สำหรับ production

## ตำแหน่ง Skills
Skills จัดเรียงในโฟลเดอร์:
- 00-meta-skills/ - แนวทางสถาปัตยกรรม
- 01-foundations/ - มาตรฐานพื้นฐาน
- 02-frontend/ - Frontend patterns
- 03-backend-api/ - Backend patterns
- [ฯลฯ...]

## การใช้งาน
เมื่อสร้างโค้ด ให้อ้างอิง skills จากโฟลเดอร์ที่เหมาะสม
ปฏิบัติตาม patterns และ best practices ที่กำหนดในไฟล์ SKILL.md

## ตัวอย่าง
สำหรับ TypeScript: 01-foundations/typescript-standards/SKILL.md
สำหรับ Next.js: 02-frontend/nextjs-patterns/SKILL.md
```

### วิธีใช้งาน

**วิธีที่ 1: ใช้ Comment**
```typescript
// ปฏิบัติตาม typescript-standards และ nextjs-patterns skills
// สร้าง Next.js API route สำหรับ user authentication

// Copilot จะแนะนำโค้ดตาม skills
```

**วิธีที่ 2: Copilot Chat**
```
@workspace ใช้ typescript-standards skill
สร้าง type-safe API client
```

### เคล็ดลับ
- เปิด repository ไว้ใน workspace
- อ้างอิงไฟล์ skill เฉพาะใน comments
- ใช้ `@workspace` ใน Copilot Chat

---

## 4. 🟠 Roo Code (Cursor)

### ภาพรวม
Cursor IDE (Roo Code) ตอนนี้รองรับ **MCP (Model Context Protocol)** สำหรับการเชื่อมต่อ GitHub แบบไร้รอยต่อ พร้อมทั้ง local repository indexing

### สิ่งที่ต้องเตรียม
- Cursor IDE ติดตั้งแล้ว
- Node.js 18+ (สำหรับวิธี MCP)
- GitHub Personal Access Token (สำหรับวิธี MCP)

---

### วิธีที่ 1: MCP (แนะนำ) ⭐

#### ขั้นที่ 1: สร้าง GitHub Token
เหมือนกับ Claude Desktop (ส่วนที่ 1, ขั้นที่ 1)

#### ขั้นที่ 2: ตั้งค่า Cursor MCP

1. **เปิด Cursor Settings**
   - กด `Cmd+,` (macOS) หรือ `Ctrl+,` (Windows/Linux)
   - หรือ: คลิกไอคอนเฟือง → Settings

2. **ไปที่ MCP Servers**
   - ใน sidebar ด้านซ้าย คลิก **"MCP Servers"**

3. **แก้ไข Global MCP**
   - คลิกปุ่ม **"Edit Global MCP"**
   - จะเปิดไฟล์ `.cursor/mcp.json`

4. **เพิ่มการตั้งค่า**
   ```json
   {
     "mcpServers": {
       "cerebratechai-skills": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-github"],
         "env": {
           "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN_HERE",
           "GITHUB_OWNER": "AmnadTaowsoam",
           "GITHUB_REPO": "cerebraSkills",
           "GITHUB_BRANCH": "main"
         }
       }
     }
   }
   ```

5. **แทนที่ Token**
   - แทนที่ `YOUR_TOKEN_HERE` ด้วย GitHub token จริงของคุณ

6. **บันทึกและ Refresh**
   - บันทึกไฟล์ (`Cmd+S` หรือ `Ctrl+S`)
   - คลิกปุ่ม **"Refresh MCP Servers"**

#### ขั้นที่ 3: ตรวจสอบการเชื่อมต่อ MCP

1. เริ่ม chat ใหม่ (`Cmd+L` หรือ `Ctrl+L`)
2. พิมพ์: `List available MCP servers`
3. ควรเห็น `cerebratechai-skills` ในรายการ

### วิธีใช้งาน (วิธี MCP)

**อ้างอิงโดยตรง:**
```
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns

Create a Next.js API endpoint
```

**ใช้กับ Cmd+L Chat:**
```
@cerebratechai-skills

แสดง typescript-standards skill
```

---

### วิธีที่ 2: Local Repository Indexing

ถ้าต้องการใช้ไฟล์ local หรือต้องการใช้งาน offline:

#### ขั้นที่ 1: Clone Repository
```bash
cd ~/projects
git clone https://github.com/AmnadTaowsoam/cerebraSkills.git
```

#### ขั้นที่ 2: เปิดใน Cursor
```bash
cursor cerebraSkills
```

หรือ: File → Open Folder → เลือก `cerebraSkills`

#### ขั้นที่ 3: ตั้งค่า Cursor Rules

สร้างไฟล์ `.cursorrules` ใน root:
```markdown
# CerebraTechAI Skills - Cursor Rules

## Context
Repository นี้มี 473+ production-ready coding skills ใน 73 หมวดหมู่

## โครงสร้าง Skill
แต่ละ skill อยู่ในโฟลเดอร์พร้อม SKILL.md ที่มี:
- Best practices
- ตัวอย่างโค้ด
- Anti-patterns
- กลยุทธ์การทดสอบ

## แนวทางการใช้งาน

### เมื่อเขียน TypeScript:
- อ้างอิง: 01-foundations/typescript-standards/SKILL.md
- ใช้ strict typing
- ปฏิบัติตาม naming conventions

### เมื่อเขียน Next.js:
- อ้างอิง: 02-frontend/nextjs-patterns/SKILL.md
- ใช้ App Router patterns
- ปฏิบัติตาม file structure conventions

### เมื่อเขียน APIs:
- อ้างอิง: 03-backend-api/nodejs-api/SKILL.md หรือ fastapi-patterns/SKILL.md
- ใช้ error handling ที่เหมาะสม
- ใช้ validation patterns

### เมื่อทำงานกับ databases:
- อ้างอิง: 04-database/prisma-guide/SKILL.md
- ปฏิบัติตาม schema best practices
- ใช้ migrations ที่เหมาะสม

## กฎทั่วไป
1. ตรวจสอบไฟล์ skill ที่เกี่ยวข้องก่อนสร้างโค้ด
2. ปฏิบัติตาม patterns ที่กำหนดใน skills
3. ใช้ security best practices จาก skills
4. ใช้ testing patterns จาก 16-testing/ skills

## หมวดหมู่ Skills
- 00-meta-skills: สถาปัตยกรรม & การตัดสินใจ
- 01-foundations: มาตรฐานพื้นฐาน (TypeScript, Python, Git)
- 02-frontend: React, Next.js, Tailwind
- 03-backend-api: Node.js, FastAPI, Express
- 04-database: Prisma, MongoDB, Redis
- 05-ai-ml-core: PyTorch, YOLO, training
- 06-ai-ml-production: LLM, RAG, embeddings
- [... ดูรายการเต็มใน README.md]
```

#### ขั้นที่ 4: Index Repository

1. เปิด Cursor Settings (`Cmd+,` หรือ `Ctrl+,`)
2. ไปที่ **Features** → **Codebase Indexing**
3. เปิด **"Index entire workspace"**
4. คลิก **"Reindex"**

### วิธีใช้งาน (วิธี Local)

**วิธีที่ 1: Cmd+K (Inline Edit)**
```typescript
// เลือกโค้ดหรือวางเคอร์เซอร์
// กด Cmd+K (หรือ Ctrl+K)
// พิมพ์: "Refactor ตาม typescript-standards skill"
```

**วิธีที่ 2: Cmd+L (Chat)**
```
ใช้ skills จาก repository นี้:
- typescript-standards
- nextjs-patterns
- jwt-authentication

สร้างระบบ auth สำหรับ Next.js
```

**วิธีที่ 3: @ Mentions**
```
@cerebraSkills/01-foundations/typescript-standards/SKILL.md

ใช้มาตรฐานเหล่านี้กับไฟล์ปัจจุบัน
```

### เคล็ดลับ
- **วิธี MCP**: Auto-sync, ทันสมัยเสมอ, ใช้ได้จากทุก project
- **วิธี Local**: ใช้งาน offline ได้, เร็วกว่าสำหรับ codebase ใหญ่
- ใช้ `@Docs` เพื่ออ้างอิงไฟล์ skill
- ใช้ Cmd+K สำหรับ refactoring เร็ว
- ใช้ Cmd+L สำหรับงานซับซ้อน

---

## 5. 🔴 Antigravity (Google DeepMind)

### ภาพรวม
Antigravity รองรับ **MCP (Model Context Protocol)** สำหรับการเชื่อมต่อกับ GitHub repositories และแหล่งข้อมูลอื่นๆ

### สิ่งที่ต้องเตรียม
- Antigravity IDE ติดตั้งแล้ว
- Node.js 18+
- GitHub Personal Access Token

---

### วิธีที่ 1: MCP กับ GitHub (แนะนำ) ⭐

#### ขั้นที่ 1: สร้าง GitHub Token

เหมือนกับ Claude Desktop (ส่วนที่ 1, ขั้นที่ 1)

#### ขั้นที่ 2: ตั้งค่า MCP

**ตำแหน่งไฟล์ config:**
- Windows: `%APPDATA%\Antigravity\mcp_config.json`
- macOS: `~/Library/Application Support/Antigravity/mcp_config.json`
- Linux: `~/.config/Antigravity/mcp_config.json`

**สร้าง/แก้ไข `mcp_config.json`:**

```json
{
  "mcpServers": {
    "cerebratechai-skills": {
      "command": "npx",
      "arguments": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN_HERE",
        "GITHUB_OWNER": "AmnadTaowsoam",
        "GITHUB_REPO": "cerebraSkills",
        "GITHUB_BRANCH": "main"
      }
    }
  }
}
```

**Windows PowerShell:**
```powershell
# สร้างโฟลเดอร์ถ้าจำเป็น
New-Item -ItemType Directory -Force -Path "$env:APPDATA\Antigravity"

# แก้ไข config
notepad "$env:APPDATA\Antigravity\mcp_config.json"
```

**macOS/Linux:**
```bash
# สร้างโฟลเดอร์ถ้าจำเป็น
mkdir -p ~/Library/Application\ Support/Antigravity

# แก้ไข config
nano ~/Library/Application\ Support/Antigravity/mcp_config.json
```

#### ขั้นที่ 3: Restart Antigravity

ปิดและเปิด Antigravity ใหม่เพื่อโหลด MCP server

#### ขั้นที่ 4: ตรวจสอบการเชื่อมต่อ

ใน Antigravity คุณควรสามารถเข้าถึง repository ผ่านคำสั่ง MCP ได้

### การใช้งานกับ MCP

```
Using skills from cerebratechai-skills repository:
- typescript-standards
- nextjs-patterns

Create a Next.js API endpoint
```

---

### วิธีที่ 2: Local Skills (Offline)

ถ้าต้องการใช้ไฟล์ local หรือต้องการใช้งาน offline:

#### ขั้นที่ 1: Clone Repository

```bash
# Windows (PowerShell)
cd $HOME\Documents
git clone https://github.com/AmnadTaowsoam/cerebraSkills.git

# macOS/Linux
cd ~/Documents
git clone https://github.com/AmnadTaowsoam/cerebraSkills.git
```

#### ขั้นที่ 2: เพิ่มเป็น Skill ใน Antigravity

1. **เปิด Antigravity**
2. **ไปที่ Settings** (ไอคอนเฟือง หรือ `Ctrl+,`)
3. **ไปที่ส่วน "Skills"**
4. **คลิก "Add Skill"** หรือ "Add Folder"
5. **เลือกโฟลเดอร์** ที่ clone มา:
   - Windows: `C:\Users\YOUR_USERNAME\Documents\cerebraSkills`
   - macOS/Linux: `/Users/YOUR_USERNAME/Documents/cerebraSkills`
6. **ตั้งชื่อ**: `cerebratechai-skills`
7. **เปิดใช้งาน** skill
8. **บันทึก** การตั้งค่า

#### ขั้นที่ 3: ตรวจสอบว่า Skill โหลดแล้ว

1. เริ่มการสนทนาใหม่
2. พิมพ์: `List available skills`
3. ควรเห็น `cerebratechai-skills` ในรายการ

### การใช้งาน (วิธี Local)

**วิธีที่ 1: อ้างอิงโดยตรง**
```
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns
- prisma-guide

Create a Next.js app with Prisma
```

**วิธีที่ 2: อ้างอิงไฟล์ Skill**
```
อ้างอิงไฟล์ skill:
cerebratechai-skills/01-foundations/typescript-standards/SKILL.md

ใช้มาตรฐาน TypeScript เหล่านี้กับโค้ดของฉัน
```

**วิธีที่ 3: โหลด Context**
```
Load context from cerebratechai-skills:
- 01-foundations/
- 02-frontend/
- 03-backend-api/

ช่วยสร้าง full-stack app
```

### อัปเดต Skills

**วิธี MCP:** Auto-sync จาก GitHub (ไม่ต้องทำอะไร)

**วิธี Local:**
```bash
# ไปที่ repository
cd ~/Documents/cerebraSkills

# Pull การเปลี่ยนแปลงล่าสุด
git pull origin main
```

Antigravity จะใช้ไฟล์ที่อัปเดตแล้วโดยอัตโนมัติ

---

## 📊 ตารางเปรียบเทียบ

| คุณสมบัติ | Claude Desktop | Claude Code | GitHub Codex | Roo Code | Antigravity |
|---------|---------------|-------------|--------------|----------|-------------|
| **ความยากในการตั้งค่า** | ⭐⭐ ง่าย | ⭐ ง่ายมาก | ⭐⭐⭐ ปานกลาง | ⭐⭐ ง่าย | ⭐⭐ ง่าย |
| **รองรับ MCP** | ✅ ใช่ | ✅ ใช่ | ❌ ไม่ | ✅ ใช่ | ✅ ใช่ |
| **Auto-sync** | ✅ ใช่ | ✅ ใช่ | ⚠️ Manual | ✅ ใช่ (MCP) | ✅ ใช่ (MCP) |
| **โหมด Offline** | ❌ ไม่ | ❌ ไม่ | ✅ ใช่ | ✅ ใช่ (Local) | ✅ ใช่ (Local) |
| **รวมกับ IDE** | ❌ ไม่ | ✅ VS Code | ✅ VS Code | ✅ Cursor | ✅ Antigravity IDE |
| **Skill Indexing** | ✅ อัตโนมัติ | ✅ อัตโนมัติ | ⚠️ Manual | ✅ อัตโนมัติ | ✅ อัตโนมัติ |
| **Context Window** | ใหญ่ | ใหญ่ | ปานกลาง | ใหญ่ | ใหญ่มาก |
| **เหมาะสำหรับ** | ใช้แยก | VS Code | ผู้ใช้ Copilot | ผู้ใช้ Cursor | พัฒนา AI agent |

### สัญลักษณ์
- ✅ รองรับเต็มรูปแบบ
- ⚠️ รองรับบางส่วน / ตั้งค่าเอง
- ❌ ไม่รองรับ
- ⭐ ความยาก (1-5 ดาว)

---

## 🎯 คำแนะนำ

### เลือก Claude Desktop/Code ถ้า:
- ✅ ต้องการ sync อัตโนมัติจาก GitHub
- ✅ ชอบใช้ MCP protocol
- ✅ ใช้ VS Code
- ✅ ต้องการตั้งค่าง่ายที่สุด

### เลือก GitHub Codex ถ้า:
- ✅ ใช้ GitHub Copilot อยู่แล้ว
- ✅ ทำงานใน VS Code เป็นหลัก
- ✅ ต้องการ inline suggestions
- ✅ คุ้นเคยกับ workspace indexing

### เลือก Roo Code (Cursor) ถ้า:
- ✅ ใช้ Cursor IDE
- ✅ ต้องการ MCP auto-sync หรือ local indexing (รองรับทั้งสอง!)
- ✅ ต้องการ AI editing ที่ทรงพลังด้วย Cmd+K
- ✅ ต้องการ AI ที่เข้าใจ codebase
- ✅ ต้องการทั้งสองวิธี (MCP + local files)

### เลือก Antigravity ถ้า:
- ✅ กำลังสร้าง AI agents
- ✅ ต้องการ MCP auto-sync หรือ local files (รองรับทั้งสอง!)
- ✅ ต้องการ context window ใหญ่มาก
- ✅ ต้องการความสามารถ AI agent ขั้นสูง
- ✅ ชอบเทคโนโลยี AI จาก Google DeepMind

---

## 🔄 ตั้งค่าหลาย Platform

คุณสามารถใช้**หลาย platforms พร้อมกัน**ได้!

### แนะนำให้ใช้ร่วมกัน:
1. **Claude Desktop** (MCP) - สำหรับถามคำถามทั่วไปและวางแผน
2. **Claude Code** (VS Code) - สำหรับเขียนโค้ดใน VS Code
3. **Roo Code** (Cursor) - สำหรับแก้ไขด้วย AI ใน Cursor

ทั้งสามตัวสามารถใช้ GitHub repository เดียวกันและ sync กันได้!

### ลำดับการตั้งค่า:
1. ตั้งค่า Claude Desktop (MCP) ก่อน
2. Claude Code ใช้งานได้ทันที (config เดียวกัน)
3. Clone repo มาไว้ local สำหรับ Roo Code/Codex
4. ตั้งค่า Antigravity ถ้าต้องการ

---

## 📚 แหล่งข้อมูลเพิ่มเติม

### เอกสาร
- 🇹🇭 [SETUP_TH.md](./SETUP_TH.md) - คู่มือภาษาไทยฉบับเต็ม
- 📖 [GITHUB_MCP_SETUP.md](./GITHUB_MCP_SETUP.md) - คู่มือ MCP ภาษาอังกฤษ
- ⚡ [QUICKSTART_MCP.md](./QUICKSTART_MCP.md) - ตั้งค่า 5 นาที
- ✅ [MCP_DEPLOYMENT_CHECKLIST.md](./MCP_DEPLOYMENT_CHECKLIST.md) - Checklist

### Skills
- 📋 [README.md](./README.md) - ภาพรวม 473+ skills
- 📑 [SKILL_INDEX.md](./SKILL_INDEX.md) - ดัชนี skill ทั้งหมด

### ชุมชน
- 🐛 [Issues](https://github.com/AmnadTaowsoam/cerebraSkills/issues)
- 💬 [Discussions](https://github.com/AmnadTaowsoam/cerebraSkills/discussions)
- 🤝 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

## 🆘 แก้ปัญหา

### ปัญหาที่พบบ่อย

#### MCP เชื่อมต่อไม่ได้ (Claude/Antigravity)
- ตรวจสอบ Node.js 18+: `node --version`
- ตรวจสอบ token ยังไม่หมดอายุ
- ตรวจสอบ JSON syntax
- Restart แอปพลิเคชัน

#### Skills ไม่ถูก Index (Codex/Roo Code)
- ตรวจสอบ repository อยู่ใน workspace
- Index ใหม่ด้วยตนเอง
- ตรวจสอบ `.vscode/settings.json` หรือ `.cursorrules`
- Restart IDE

#### Skills ไม่ทันสมัย
- **ผู้ใช้ MCP**: Sync อัตโนมัติ (ไม่ต้องทำอะไร)
- **ผู้ใช้ Local**: `git pull` เพื่ออัปเดต

---

**อัปเดตล่าสุด**: 16 มกราคม 2026  
**Repository**: https://github.com/AmnadTaowsoam/cerebraSkills  
**License**: MIT
