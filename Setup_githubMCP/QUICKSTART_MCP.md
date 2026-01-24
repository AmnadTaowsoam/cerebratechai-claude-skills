# ⚡ Quick Start: GitHub MCP Server (5 นาที)

## 🎯 เป้าหมาย
ตั้งค่า Claude Desktop ให้อ่าน Skills จาก GitHub repository นี้ใน 5 นาที

---

## 📝 3 ขั้นตอนหลัก

### 1️⃣ สร้าง GitHub Token (2 นาที)

1. ไปที่: **https://github.com/settings/tokens**
2. คลิก: **Fine-grained tokens** → **Generate new token**
3. ตั้งค่า:
   - Name: `Claude MCP`
   - Expiration: `90 days`
   - Repository: เลือก `cerebraSkills`
   - Permissions: **Contents** = `Read-only`
4. คลิก **Generate token**
5. **คัดลอก token** (ขึ้นต้นด้วย `github_pat_...`)

---

### 2️⃣ ตั้งค่า Claude Desktop (2 นาที)

#### Windows:
```powershell
notepad "$env:APPDATA\Claude\claude_desktop_config.json"
```

#### macOS:
```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

#### Linux:
```bash
nano ~/.config/Claude/claude_desktop_config.json
```

**วางโค้ดนี้** (แก้ `YOUR_TOKEN_HERE`):

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

**บันทึกไฟล์**

---

### 3️⃣ Restart Claude (1 นาที)

#### Windows:
- คลิกขวา Claude icon → **Quit**
- เปิด Claude ใหม่

#### macOS:
```bash
killall Claude && open -a Claude
```

#### Linux:
```bash
pkill -f claude && claude &
```

---

## ✅ ทดสอบ

เปิด Claude Desktop แล้วพิมพ์:

```
List available MCP servers
```

ถ้าเห็น `cerebratechai-skills` แสดงว่า**สำเร็จ**! 🎉

---

## 🚀 ใช้งาน

```
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns
- prisma-guide

Create a Next.js API with Prisma and TypeScript
```

Claude จะใช้ best practices จาก skills เหล่านี้ในการสร้างโค้ด!

---

## 📚 เอกสารเพิ่มเติม

- **คู่มือภาษาไทยฉบับเต็ม**: [SETUP_TH.md](./SETUP_TH.md)
- **คู่มือภาษาอังกฤษฉบับเต็ม**: [GITHUB_MCP_SETUP.md](./GITHUB_MCP_SETUP.md)
- **รายการ Skills ทั้งหมด**: [README.md](./README.md)

---

## ❓ มีปัญหา?

### Claude ไม่เห็น MCP Server
- ตรวจสอบ JSON syntax (ใช้ https://jsonlint.com)
- Restart Claude อีกครั้ง
- ตรวจสอบว่า Node.js 18+ ติดตั้งแล้ว

### Invalid Token Error
- สร้าง token ใหม่
- ตรวจสอบว่าคัดลอกครบถ้วน (ไม่มีช่องว่าง)
- ตรวจสอบว่า token มีสิทธิ์ `Contents: Read-only`

---

**เวลาทั้งหมด**: ~5 นาที  
**ความยาก**: ⭐⭐☆☆☆ (ง่าย)
