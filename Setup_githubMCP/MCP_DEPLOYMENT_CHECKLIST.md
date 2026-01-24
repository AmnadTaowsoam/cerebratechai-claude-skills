# ✅ GitHub MCP Server Deployment Checklist

## 📋 Pre-Deployment Checklist

### Repository Preparation
- [x] Repository exists on GitHub: `AmnadTaowsoam/cerebraSkills`
- [x] All skill files are committed and pushed
- [x] README.md updated with MCP setup instructions
- [x] Setup guides created (English & Thai)
- [ ] Repository is public (or private with proper token permissions)
- [ ] Default branch is `main` (or update config accordingly)

### Documentation
- [x] `GITHUB_MCP_SETUP.md` - Complete English guide
- [x] `SETUP_TH.md` - Complete Thai guide
- [x] `QUICKSTART_MCP.md` - Quick start guide
- [x] README.md updated with setup links
- [ ] CHANGELOG.md updated (if applicable)

---

## 🚀 Deployment Steps

### Step 1: Verify Repository
- [ ] Visit: https://github.com/AmnadTaowsoam/cerebraSkills
- [ ] Confirm all files are visible
- [ ] Check that skills are organized in folders (00-meta-skills, 01-foundations, etc.)
- [ ] Verify README.md displays correctly

### Step 2: Create GitHub Token
- [ ] Go to: https://github.com/settings/tokens
- [ ] Create Fine-grained token with:
  - [ ] Name: `Claude MCP - Skills`
  - [ ] Expiration: 90 days (or custom)
  - [ ] Repository: `cerebraSkills`
  - [ ] Permissions: `Contents: Read-only`
- [ ] Copy token (starts with `github_pat_`)
- [ ] Save token securely (password manager)

### Step 3: Configure Claude Desktop

#### Windows
- [ ] Create/edit: `%APPDATA%\Claude\claude_desktop_config.json`
- [ ] Add MCP configuration (see SETUP_TH.md)
- [ ] Replace `YOUR_TOKEN_HERE` with actual token
- [ ] Verify JSON syntax
- [ ] Save file

#### macOS
- [ ] Create/edit: `~/Library/Application Support/Claude/claude_desktop_config.json`
- [ ] Add MCP configuration
- [ ] Replace `YOUR_TOKEN_HERE` with actual token
- [ ] Verify JSON syntax
- [ ] Save file

#### Linux
- [ ] Create/edit: `~/.config/Claude/claude_desktop_config.json`
- [ ] Add MCP configuration
- [ ] Replace `YOUR_TOKEN_HERE` with actual token
- [ ] Verify JSON syntax
- [ ] Save file

### Step 4: Restart Claude
- [ ] Quit Claude Desktop completely
- [ ] Start Claude Desktop
- [ ] Wait for initialization (~10 seconds)

---

## ✅ Testing & Verification

### Basic Tests
- [ ] Test 1: List MCP servers
  ```
  List available MCP servers
  ```
  Expected: See `cerebratechai-skills`

- [ ] Test 2: List repository files
  ```
  What files are in the cerebratechai-skills repository?
  ```
  Expected: See folder structure

- [ ] Test 3: Read a skill
  ```
  Read the typescript-standards skill from cerebratechai-skills
  ```
  Expected: See skill content

### Advanced Tests
- [ ] Test 4: Use skill in task
  ```
  Using typescript-standards from cerebratechai-skills,
  create a TypeScript function for user authentication
  ```
  Expected: Code follows skill guidelines

- [ ] Test 5: Multiple skills
  ```
  Using skills from cerebratechai-skills:
  - nextjs-patterns
  - prisma-guide
  - jwt-authentication
  
  Create a Next.js API with authentication
  ```
  Expected: Implementation uses all three skills

### Claude Code (VS Code) Tests
- [ ] Install Claude Code extension
- [ ] Open Claude Code panel
- [ ] Verify `cerebratechai-skills` appears in tools
- [ ] Test skill usage in VS Code

---

## 🔧 Troubleshooting

### Issue: MCP Server Not Visible
- [ ] Check config file location is correct
- [ ] Validate JSON syntax (use https://jsonlint.com)
- [ ] Verify Node.js 18+ is installed: `node --version`
- [ ] Check token hasn't expired
- [ ] Restart Claude Desktop again

### Issue: "Invalid Token" Error
- [ ] Verify token copied correctly (no spaces)
- [ ] Check token permissions include `Contents: Read-only`
- [ ] Confirm token hasn't expired
- [ ] Try creating a new token

### Issue: "Repository Not Found"
- [ ] Verify `GITHUB_OWNER` is correct: `AmnadTaowsoam`
- [ ] Verify `GITHUB_REPO` is correct: `cerebraSkills`
- [ ] Check repository visibility (public/private)
- [ ] Confirm token has access to the repository

### Issue: Skills Not Loading
- [ ] Verify `GITHUB_BRANCH` is correct: `main`
- [ ] Check that skill files exist in repository
- [ ] Confirm skill files are named `SKILL.md`
- [ ] Try reading a specific skill by path

---

## 📊 Post-Deployment

### Documentation
- [ ] Share setup guides with team
- [ ] Update internal wiki/docs
- [ ] Create video tutorial (optional)

### Monitoring
- [ ] Monitor token expiration date
- [ ] Set reminder to renew token before expiry
- [ ] Track usage and feedback

### Maintenance
- [ ] Plan regular skill updates
- [ ] Review and improve skills based on usage
- [ ] Keep documentation up-to-date

---

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ Claude Desktop shows `cerebratechai-skills` in MCP servers
- ✅ Can list repository files
- ✅ Can read individual skills
- ✅ Can use skills in code generation tasks
- ✅ Skills are applied correctly in generated code
- ✅ Works across multiple devices (if configured)

---

## 📞 Support

### Resources
- 📖 Full Setup Guide: [GITHUB_MCP_SETUP.md](./GITHUB_MCP_SETUP.md)
- 🇹🇭 Thai Guide: [SETUP_TH.md](./SETUP_TH.md)
- ⚡ Quick Start: [QUICKSTART_MCP.md](./QUICKSTART_MCP.md)
- 🌐 MCP Documentation: https://modelcontextprotocol.io
- 🐙 GitHub MCP Server: https://github.com/modelcontextprotocol/servers

### Getting Help
- 🐛 Report Issues: https://github.com/AmnadTaowsoam/cerebraSkills/issues
- 💬 Discussions: https://github.com/AmnadTaowsoam/cerebraSkills/discussions

---

**Last Updated**: January 16, 2026  
**Version**: 1.0.0
