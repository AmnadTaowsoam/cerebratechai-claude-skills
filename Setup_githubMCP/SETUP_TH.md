# 🚀 คู่มือตั้งค่า GitHub MCP Server (ภาษาไทย)

## 📋 ภาพรวม

คู่มือนี้จะแนะนำวิธีการตั้งค่าให้ Claude Desktop สามารถอ่าน Skills จาก GitHub repository นี้ผ่าน Model Context Protocol (MCP)

## ⏱️ เวลาที่ใช้: 10-15 นาที

---

## ✅ สิ่งที่ต้องเตรียม

- [x] บัญชี GitHub (มีอยู่แล้ว)
- [x] Repository นี้อยู่บน GitHub แล้ว
- [ ] Claude Desktop ติดตั้งแล้ว
- [ ] Node.js 18+ ติดตั้งแล้ว

---

## 📝 ขั้นตอนการตั้งค่า

### ขั้นตอนที่ 1: สร้าง GitHub Personal Access Token

1. **เปิดหน้าสร้าง Token**
   - ไปที่: https://github.com/settings/tokens
   - หรือ: Profile → Settings → Developer settings → Personal access tokens

2. **เลือกประเภท Token**
   - คลิก: **Fine-grained tokens** (แนะนำ)
   - คลิก: **Generate new token**

3. **กรอกข้อมูล**
   - **Token name**: `Claude MCP - Skills`
   - **Expiration**: `90 days` (หรือตามต้องการ)
   - **Repository access**: เลือก **Only select repositories**
   - เลือก repository: `cerebraSkills`

4. **ตั้งค่าสิทธิ์**
   - **Repository permissions**:
     - **Contents**: `Read-only` ✅
     - **Metadata**: จะถูกเลือกอัตโนมัติ ✅

5. **สร้าง Token**
   - คลิก: **Generate token**
   - **⚠️ สำคัญมาก**: คัดลอก token ทันที!
   ```
   github_pat_11XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
   - คุณจะ**ไม่สามารถดู token นี้ได้อีก**!

6. **บันทึก Token อย่างปลอดภัย**
   - ใช้ Password Manager (1Password, Bitwarden, LastPass)
   - หรือบันทึกในไฟล์เข้ารหัส
   - **ห้ามแชร์หรือ commit token ลง Git!**

---

### ขั้นตอนที่ 2: ตั้งค่า Claude Desktop

#### สำหรับ Windows:

1. **เปิดไฟล์ Config**
   ```powershell
   # สร้างโฟลเดอร์ถ้ายังไม่มี
   New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude"
   
   # เปิดไฟล์ด้วย Notepad
   notepad "$env:APPDATA\Claude\claude_desktop_config.json"
   ```

2. **วางโค้ดนี้ลงในไฟล์** (แก้ไข `YOUR_TOKEN_HERE`):
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
           "GITHUB_OWNER": "AmnadTaowsoam",
           "GITHUB_REPO": "cerebraSkills",
           "GITHUB_BRANCH": "main"
         }
       }
     }
   }
   ```

3. **แทนที่ค่าเหล่านี้**:
   - `YOUR_TOKEN_HERE` → Token ที่คุณคัดลอกไว้ (ขึ้นต้นด้วย `github_pat_`)

4. **บันทึกไฟล์**: File → Save → ปิด Notepad

#### สำหรับ macOS:

```bash
# สร้างโฟลเดอร์ถ้ายังไม่มี
mkdir -p ~/Library/Application\ Support/Claude

# เปิดไฟล์ด้วย nano
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

วางโค้ดเดียวกัน แล้วกด `Ctrl+X`, `Y`, `Enter` เพื่อบันทึก

#### สำหรับ Linux:

```bash
# สร้างโฟลเดอร์ถ้ายังไม่มี
mkdir -p ~/.config/Claude

# เปิดไฟล์ด้วย nano
nano ~/.config/Claude/claude_desktop_config.json
```

วางโค้ดเดียวกัน แล้วกด `Ctrl+X`, `Y`, `Enter` เพื่อบันทึก

---

### ขั้นตอนที่ 3: Restart Claude Desktop

#### Windows:
1. คลิกขวาที่ไอคอน Claude ใน System Tray
2. เลือก **Quit**
3. เปิด Claude ใหม่จาก Start Menu

#### macOS:
```bash
# ปิด Claude
killall Claude

# เปิด Claude
open -a Claude
```

#### Linux:
```bash
# ปิด Claude
pkill -f claude

# เปิด Claude
claude &
```

---

## ✅ ทดสอบการทำงาน

### ทดสอบที่ 1: ตรวจสอบ MCP Server

เปิด Claude Desktop แล้วพิมพ์:
```
List available MCP servers
```

**ผลลัพธ์ที่คาดหวัง:**
```
I can see the following MCP servers:
- cerebratechai-skills
```

### ทดสอบที่ 2: ดูไฟล์ใน Repository

```
What files are in the cerebratechai-skills repository?
```

**ผลลัพธ์ที่คาดหวัง:**
```
The cerebratechai-skills repository contains:
- README.md
- 00-meta-skills/
- 01-foundations/
- 02-frontend/
[... และโฟลเดอร์อื่นๆ]
```

### ทดสอบที่ 3: อ่าน Skill

```
Read the typescript-standards skill from cerebratechai-skills
```

Claude จะแสดงเนื้อหาของ skill ที่คุณเลือก

### ทดสอบที่ 4: ใช้ Skill ในการทำงาน

```
Using skills from cerebratechai-skills:
- typescript-standards
- nextjs-patterns

Create a Next.js API endpoint for user authentication
```

Claude จะสร้างโค้ดตาม best practices ที่กำหนดใน skills

---

## 🎉 เสร็จสิ้น!

ตอนนี้คุณสามารถใช้ Skills จาก GitHub repository นี้กับ Claude Desktop ได้แล้ว!

---

## 🔧 การแก้ปัญหา

### ปัญหา: Claude ไม่เห็น MCP Server

**วิธีแก้:**
1. ตรวจสอบว่าไฟล์ `claude_desktop_config.json` อยู่ในตำแหน่งที่ถูกต้อง
2. ตรวจสอบว่า JSON syntax ถูกต้อง (ใช้ JSON validator)
3. ตรวจสอบว่า Token ยังไม่หมดอายุ
4. Restart Claude Desktop อีกครั้ง

### ปัญหา: Error "Invalid token"

**วิธีแก้:**
1. สร้าง Token ใหม่
2. ตรวจสอบว่าคัดลอก Token ครบถ้วน (ไม่มีช่องว่างหรืออักขระพิเศษ)
3. ตรวจสอบว่า Token มีสิทธิ์ `Contents: Read-only`

### ปัญหา: Error "Repository not found"

**วิธีแก้:**
1. ตรวจสอบว่า `GITHUB_OWNER` และ `GITHUB_REPO` ถูกต้อง
2. ตรวจสอบว่า Token มีสิทธิ์เข้าถึง repository นี้
3. ถ้า repository เป็น private ให้ใช้ Fine-grained token

---

## 📚 เอกสารเพิ่มเติม

- [GITHUB_MCP_SETUP.md](./GITHUB_MCP_SETUP.md) - คู่มือฉบับเต็ม (ภาษาอังกฤษ)
- [README.md](./README.md) - ภาพรวม Skills ทั้งหมด
- [CONTRIBUTING.md](./CONTRIBUTING.md) - วิธีการมีส่วนร่วม

---

## 🆘 ต้องการความช่วยเหลือ?

- เปิด Issue: https://github.com/AmnadTaowsoam/cerebraSkills/issues
- ดูเอกสาร MCP: https://modelcontextprotocol.io
- ดูเอกสาร GitHub MCP Server: https://github.com/modelcontextprotocol/servers/tree/main/src/github

---

**สร้างโดย**: CerebraTechAI  
**License**: MIT  
**Last Updated**: January 16, 2026
