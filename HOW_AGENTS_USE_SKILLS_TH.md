# 🤖 แต่ละ Agent เรียกใช้ Skills อย่างไร?

คู่มือสำหรับการตั้งค่า AI Agents ให้ใช้งาน Skills จาก Local Repository

---

## 📍 ที่ตั้ง Skills (2 Directory System)

### Development (สำหรับแก้ไข)
```
D:\Cerebra\cerebraSkills
```
- ✏️ แก้ไขและพัฒนา skills ที่นี่
- 📤 Push ขึ้น GitHub ด้วย `sync-to-production.bat`

### Production (สำหรับ Multi-Agent)
```
D:\AgentSkill\cerebraSkills
```
- 🤖 Multi-agent อ่าน skills จากที่นี่
- 📥 Pull จาก GitHub ด้วย `update-skills.bat`

---

## 🔄 Workflow ที่สมบูรณ์

```
1. แก้ไข Skills
   ↓
   D:\Cerebra\cerebraSkills
   
2. Push ขึ้น GitHub
   ↓
   sync-to-production.bat
   
3. GitHub Repository
   ↓
   https://github.com/AmnadTaowsoam/cerebraSkills
   
4. Pull มา Production
   ↓
   update-skills.bat
   
5. Multi-Agent ใช้งาน
   ↓
   D:\AgentSkill\cerebraSkills
```

---

## 🔗 ตั้งค่า Junction Links (แนะนำ)

### ทำไมต้องใช้ Junction Links?

**ปัญหาของการใช้ MCP:**
- ❌ ต้อง config ใหม่ทุกครั้งที่เปลี่ยน project
- ❌ ต้องมี GitHub token
- ❌ ต้องมี internet

**วิธีแก้ด้วย Junction Links:**
- ✅ ตั้งค่าครั้งเดียวต่อ project
- ✅ เข้าถึง skills ได้จากทุก project
- ✅ ไม่ต้อง config ซ้ำ
- ✅ ใช้งาน offline ได้

### วิธีสร้าง Junction Links

**ตัวเลือก 1: ใช้ Batch Script (แนะนำ)** ⭐

```batch
# รันใน project directory ที่ต้องการใช้ skills
# ต้องรันด้วย Administrator
setup-project-links.bat
```

**ตัวเลือก 2: สร้างเอง**

```batch
# เปิด Command Prompt as Administrator
# cd ไปที่ project directory

# สร้างโฟลเดอร์ .agentskills
mkdir .agentskills

# สร้าง junction link ไปที่ skills
mklink /J .agentskills\skills D:\AgentSkill\cerebraSkills

```

### ผลลัพธ์

```
your-project/
├── .agentskills/
    └── skills/  → D:\AgentSkill\cerebraSkills

```

### ตรวจสอบว่าสำเร็จ

```batch
# ดู junction links
dir /AL

# ทดสอบเข้าถึง skills
dir .agentskills\skills
```

### เพิ่มใน .gitignore

```gitignore
# Agent Skills Junction Links
.agentskills/
```

**หมายเหตุ:** Junction links จะไม่ถูก commit ขึ้น git (เป็น symbolic link)

---

## 🤖 วิธีตั้งค่าแต่ละ Agent

### 1. 🔴 **Antigravity** (แนะนำ)

#### ขั้นตอนการตั้งค่า

**1. เปิด Antigravity Settings**
```
Ctrl+, (หรือคลิกไอคอนเฟือง)
```

**2. เพิ่ม Skills Folder**
```
Settings → Skills → Add Folder
```

**3. เลือก Production Directory**
```
D:\AgentSkill\cerebraSkills
```

**4. ตั้งชื่อ**
```
cerebratechai-skills
```

**5. เปิดใช้งาน**
```
✅ Enable skill
```

**6. บันทึก**
```
Save settings
```

#### วิธีใช้งาน

```
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns
- prisma-guide

Create a Next.js app with Prisma and TypeScript
```

#### อัพเดท Skills

```batch
# รัน batch file
update-skills.bat

# Antigravity จะใช้ไฟล์ที่อัพเดทแล้วอัตโนมัติ
```

---

### 2. 🟠 **Roo Code (Cursor IDE)**

#### ขั้นตอนการตั้งค่า

**1. เปิด Production Repository**
```bash
cursor D:\AgentSkill\cerebraSkills
```

หรือ: `File → Open Folder → เลือก D:\AgentSkill\cerebraSkills`

**2. สร้างไฟล์ .cursorrules** (ใน root ของ repository)

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
- อ้างอิง: 03-backend-api/nodejs-api/SKILL.md
- ใช้ error handling ที่เหมาะสม
- ใช้ validation patterns

## กฎทั่วไป
1. ตรวจสอบไฟล์ skill ที่เกี่ยวข้องก่อนสร้างโค้ด
2. ปฏิบัติตาม patterns ที่กำหนดใน skills
3. ใช้ security best practices จาก skills
```

**3. Index Repository**
```
Settings (Cmd+,) → Features → Codebase Indexing → Reindex
```

#### วิธีใช้งาน

**Cmd+K (Inline Edit):**
```typescript
// เลือกโค้ด → กด Cmd+K
// พิมพ์: "Refactor ตาม typescript-standards skill"
```

**Cmd+L (Chat):**
```
ใช้ skills จาก repository นี้:
- typescript-standards
- nextjs-patterns

สร้างระบบ auth สำหรับ Next.js
```

**@ Mentions:**
```
@01-foundations/typescript-standards/SKILL.md

ใช้มาตรฐานเหล่านี้กับไฟล์ปัจจุบัน
```

#### อัพเดท Skills

```batch
# รัน batch file
update-skills.bat

# Reload Cursor window
Cmd+Shift+P → "Developer: Reload Window"
```

---

### 3. 🟢 **GitHub Codex / Copilot**

#### ขั้นตอนการตั้งค่า

**1. Clone Repository**
```bash
cd ~/projects
git clone https://github.com/AmnadTaowsoam/cerebraSkills.git
cd cerebraSkills
```

**2. เปิดใน VS Code**
```bash
code .
```

**3. สร้างไฟล์ .vscode/settings.json**

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

**4. สร้างไฟล์ .copilot-instructions.md** (ใน root)

```markdown
# GitHub Copilot Instructions

## Context
Repository นี้มี 473+ production-ready coding skills

## การจัดระเบียบ Skills
- 00-meta-skills/ - แนวทางสถาปัตยกรรม
- 01-foundations/ - มาตรฐานพื้นฐาน
- 02-frontend/ - Frontend patterns
- 03-backend-api/ - Backend patterns
- [ฯลฯ...]

## กฎการสร้างโค้ด
1. ตรวจสอบไฟล์ skill ที่เกี่ยวข้องก่อนสร้างโค้ด
2. ปฏิบัติตาม patterns ที่กำหนดใน skills
3. ใช้ security best practices จาก skills
```

#### วิธีใช้งาน

**Comment:**
```typescript
// ปฏิบัติตาม typescript-standards และ nextjs-patterns skills
// สร้าง Next.js API route สำหรับ user authentication

// Copilot จะแนะนำโค้ดตาม skills
```

**Copilot Chat:**
```
@workspace ใช้ typescript-standards skill
สร้าง type-safe API client
```

#### อัพเดท Skills

```bash
cd ~/projects/cerebraSkills
git pull origin main

# Reload VS Code
Cmd+Shift+P → "Developer: Reload Window"
```

---

## 📊 ตารางเปรียบเทียบ

| Agent | วิธีตั้งค่า | ความยาก | Offline | แนะนำ |
|-------|------------|---------|---------|-------|
| **Antigravity** | Add Folder | ⭐ ง่าย | ✅ | ⭐⭐⭐⭐⭐ |
| **Roo Code** | Open Folder + .cursorrules | ⭐⭐ ปานกลาง | ✅ | ⭐⭐⭐⭐ |
| **Codex/Copilot** | Clone + settings.json | ⭐⭐⭐ ปานกลาง | ✅ | ⭐⭐⭐ |

---

## 💡 Best Practices

### 1. อัพเดท Skills เป็นประจำ

```batch
# รันทุกวันก่อนเริ่มงาน
update-skills.bat
```

### 2. ตรวจสอบว่า Agent เชื่อมต่อแล้ว

**Antigravity:**
```
List available skills
```

**Cursor:**
```
@cerebratechai-skills
```

**Copilot:**
```
@workspace
```

### 3. อ้างอิง Skills เฉพาะเจาะจง

```typescript
// Reference: 01-foundations/typescript-standards/SKILL.md
// ช่วยให้ Agent เข้าใจว่าควรให้ความสำคัญกับ skill ไหน
```

---

## 🆘 แก้ปัญหา

### Agent ไม่เห็น Skills

**ตรวจสอบ:**
1. ✅ Path ถูกต้อง: `D:\AgentSkill\cerebraSkills`
2. ✅ มีไฟล์ SKILL.md ในโฟลเดอร์
3. ✅ Restart agent / Reload window

### Skills ไม่อัพเดท

**วิธีแก้:**
```batch
# รัน update script
update-skills.bat

# Restart agent
```

### Agent ช้า

**วิธีแก้:**
1. Reindex repository
2. ปิดไฟล์ที่ไม่จำเป็น
3. Restart agent

---

## 📚 เอกสารเพิ่มเติม

- **คู่มือทุก Platform**: [SETUP_ALL_PLATFORMS_TH.md](./SETUP_ALL_PLATFORMS_TH.md)
- **คู่มือ Codex**: [SETUP_CODEX_TH.md](./SETUP_CODEX_TH.md)
- **คู่มือ Sync**: [SYNC_WORKFLOW_TH.md](./SYNC_WORKFLOW_TH.md)
- **Workflow**: [.agent/workflows/sync-skills-workflow.md](./.agent/workflows/sync-skills-workflow.md)

---

## 🎓 สรุป

### Agent ใช้ Skills ได้ 2 วิธี:

1. **MCP (Model Context Protocol)**
   - เชื่อมต่อ GitHub โดยตรง
   - Auto-sync
   - ต้องมี internet

2. **Local Repository**
   - อ่านจากไฟล์ local
   - Manual sync (git pull)
   - ใช้งาน offline ได้

### สำหรับระบบของคุณ:

```
Development (D:\Cerebra)
→ ใช้ MCP หรือ Local ก็ได้

Production (D:\AgentSkill)
→ ใช้ Local Repository
→ อัพเดทด้วย update-skills.bat
```

---

**อัปเดตล่าสุด**: 17 มกราคม 2026  
**Repository**: https://github.com/AmnadTaowsoam/cerebraSkills  
**License**: MIT
