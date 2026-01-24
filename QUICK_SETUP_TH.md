# ⚡ Quick Setup - ตั้งค่าด่วน

คู่มือฉบับย่อสำหรับตั้งค่า Multi-Agent ให้ใช้งาน Skills

---

## 📍 ระบบของคุณ (2 Directory)

```
D:\Cerebra\cerebraSkills     ← แก้ไข Skills
         ↓
    sync-to-production.bat                 ← Push ขึ้น GitHub
         ↓
    GitHub Repository
         ↓
    update-skills.bat                      ← Pull มา Production
         ↓
D:\AgentSkill\cerebraSkills  ← Multi-Agent ใช้งาน
```

---

## 🚀 ขั้นตอนแรก (ทำครั้งเดียว)

### 1. ตรวจสอบว่ามี D:\AgentSkill หรือยัง

```batch
dir D:\AgentSkill\cerebraSkills
```

**ถ้ามีแล้ว** → ข้ามไปขั้นตอนที่ 2  
**ถ้ายังไม่มี** → Clone จาก GitHub:

```batch
cd D:\AgentSkill
git clone https://github.com/AmnadTaowsoam/cerebraSkills.git
```

### 2. สร้าง Junction Links (สำคัญ!) 🔗

**ทำไมต้องสร้าง Junction Links?**
- ✅ เข้าถึง skills ได้จากทุก project
- ✅ ไม่ต้อง config ซ้ำตอนเปลี่ยน project
- ✅ Agent หา skills เจอทันที

**วิธีสร้าง:** (รันใน project directory ที่ต้องการใช้ skills)

```batch
# สร้างโฟลเดอร์ .agentskills
mkdir .agentskills

# สร้าง junction link ไปที่ skills
mklink /J .agentskills\skills D:\AgentSkill\cerebraSkills

# สร้าง junction link สำหรับ Codex
mklink /J .codex .agentskills
```

**ผลลัพธ์:**
```
your-project/
├── .agentskills/
│   └── skills/  → D:\AgentSkill\cerebraSkills
└── .codex/      → .agentskills/
```

**หมายเหตุ:** ต้องรันใน Command Prompt **as Administrator**

### 3. ทดสอบ Sync Scripts

```batch
# ทดสอบ pull จาก GitHub
update-skills.bat
```

ถ้าสำเร็จ → ระบบพร้อมใช้งาน! ✅

---

## 🤖 ตั้งค่า Agents

### Antigravity (ง่ายที่สุด) ⭐

```
1. เปิด Antigravity
2. Ctrl+, (Settings)
3. Skills → Add Folder
4. เลือก: D:\AgentSkill\cerebraSkills
5. ตั้งชื่อ: cerebratechai-skills
6. ✅ Enable
7. Save
```

**ทดสอบ:**
```
List available skills
```

---

### Roo Code (Cursor)

```
1. File → Open Folder
2. เลือก: D:\AgentSkill\cerebraSkills
3. สร้างไฟล์ .cursorrules (ดูตัวอย่างด้านล่าง)
4. Settings → Codebase Indexing → Reindex
```

**ไฟล์ .cursorrules:**
```markdown
# CerebraTechAI Skills

## Context
Repository นี้มี 473+ production-ready coding skills

## กฎการใช้งาน
1. ตรวจสอบไฟล์ skill ก่อนสร้างโค้ด
2. ปฏิบัติตาม patterns ใน skills
3. ใช้ security best practices
```

**ทดสอบ:**
```
@cerebratechai-skills
```

---

### GitHub Copilot

```
1. Clone repository มาไว้ที่ไหนก็ได้
2. เปิดใน VS Code
3. สร้าง .vscode/settings.json (ดูตัวอย่างด้านล่าง)
4. สร้าง .copilot-instructions.md
```

**ไฟล์ .vscode/settings.json:**
```json
{
  "github.copilot.advanced": {
    "contextFiles": ["**/*.md", "**/SKILL.md"]
  },
  "github.copilot.enable": {
    "*": true,
    "markdown": true
  }
}
```

**ทดสอบ:**
```
@workspace
```

---

## 📅 การใช้งานประจำวัน

### เช้าวันจันทร์ - เริ่มงาน

```batch
# อัพเดท skills ล่าสุด
update-skills.bat
```

### กลางวัน - แก้ไข Skills

```
1. แก้ไขใน D:\Cerebra\cerebraSkills
2. ทดสอบให้แน่ใจว่าถูกต้อง
```

### เย็น - Sync ขึ้น Production

```batch
# Push ขึ้น GitHub
cd D:\Cerebra\cerebraSkills
sync-to-production.bat
# (ใส่ commit message)

# Pull มา Production
update-skills.bat
```

**เสร็จ!** Multi-agent ใช้งาน skills ใหม่ได้แล้ว 🎉

---

## 💡 Tips

### อัพเดทเป็นประจำ
```batch
# รันทุกเช้า
update-skills.bat
```

### ตรวจสอบ Agent เชื่อมต่อ

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

### อ้างอิง Skill เฉพาะ

```typescript
// Reference: 01-foundations/typescript-standards/SKILL.md
// สร้าง type-safe function
```

---

## 🆘 แก้ปัญหาด่วน

### Agent ไม่เห็น Skills

```
1. ตรวจสอบ path: D:\AgentSkill\cerebraSkills
2. Restart agent
3. Reindex (ถ้ามี)
```

### Skills ไม่อัพเดท

```batch
update-skills.bat
# แล้ว restart agent
```

### Agent ช้า

```
1. Reindex repository
2. ปิดไฟล์ที่ไม่ใช้
3. Restart agent
```

---

## 📚 เอกสารเพิ่มเติม

- **คู่มือละเอียด**: [HOW_AGENTS_USE_SKILLS_TH.md](./HOW_AGENTS_USE_SKILLS_TH.md)
- **Workflow**: [SYNC_WORKFLOW_TH.md](./SYNC_WORKFLOW_TH.md)
- **ทุก Platform**: [SETUP_ALL_PLATFORMS_TH.md](./SETUP_ALL_PLATFORMS_TH.md)

---

## ✅ Checklist

- [ ] มี D:\AgentSkill\cerebraSkills แล้ว
- [ ] ทดสอบ update-skills.bat สำเร็จ
- [ ] ตั้งค่า Agent แล้ว (Antigravity/Cursor/Copilot)
- [ ] ทดสอบ Agent เห็น skills แล้ว
- [ ] รู้วิธีอัพเดท skills (update-skills.bat)

**ครบทุกข้อ?** พร้อมใช้งาน! 🚀

---

**อัปเดตล่าสุด**: 17 มกราคม 2026  
**Repository**: https://github.com/AmnadTaowsoam/cerebraSkills  
**License**: MIT
