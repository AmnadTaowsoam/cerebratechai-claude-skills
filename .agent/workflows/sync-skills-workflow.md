---
description: Workflow for syncing skills between development and production
---

# Skills Sync Workflow

This workflow describes how to sync skills between your development environment and production environment for multi-agent consumption.

## Directory Structure

- **Development**: `D:\Cerebra\cerebraSkills`
  - Where you edit and develop skills
  - Connected to GitHub for version control
  
- **Production**: `D:\AgentSkill\cerebraSkills`
  - Where multi-agent systems read skills from
  - Always pulls from GitHub (read-only workflow)

## Workflow Steps

### 1. Edit Skills (Local Development)

Work on your skills in the development directory:
```
D:\Cerebra\cerebraSkills
```

Make your changes to any skill files, add new skills, update documentation, etc.

### 2. Sync to GitHub (Push)

When you're ready to publish your changes:

```batch
cd D:\Cerebra\cerebraSkills
sync-to-production.bat
```

This script will:
- Show git status
- Add all changes
- Prompt for commit message
- Commit changes
- Push to GitHub (origin/main)

**Alternative manual method:**
```batch
cd D:\Cerebra\cerebraSkills
git add .
git commit -m "Your commit message"
git push origin main
```

### 3. Verify on GitHub

Visit your GitHub repository to confirm changes are pushed:
```
https://github.com/AmnadTaowsoam/cerebraSkills
```

### 4. Update Production (Pull)

Pull the latest changes to your production directory:

```batch
update-skills.bat
```

This script will:
- Fetch latest changes from GitHub
- Checkout main branch
- Pull changes with fast-forward only
- Confirm success

**Alternative manual method:**
```batch
cd D:\AgentSkill\cerebraSkills
git fetch origin
git checkout main
git pull --ff-only origin main
```

### 5. Multi-Agent Access

Your multi-agent systems can now access the updated skills from:
```
D:\AgentSkill\cerebraSkills
```

## Quick Reference

### Full Workflow (One-liner summary)
```
Edit (D:\Cerebra) → Push (sync-to-production.bat) → GitHub → Pull (update-skills.bat) → Use (D:\AgentSkill)
```

### Batch Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `sync-to-production.bat` | `D:\Cerebra\cerebraSkills\` | Push changes to GitHub |
| `update-skills.bat` | `D:\Cerebra\cerebraSkills\` | Pull changes from GitHub to production |

## Best Practices

1. **Always commit meaningful changes**: Use descriptive commit messages
2. **Test before pushing**: Ensure your skills work correctly before syncing to production
3. **Pull before editing**: Run `update-skills.bat` before starting new edits to avoid conflicts
4. **Keep production clean**: Never edit files directly in `D:\AgentSkill\cerebraSkills`

## Troubleshooting

### Merge Conflicts
If you get merge conflicts:
```batch
cd D:\Cerebra\cerebraSkills
git status
# Resolve conflicts manually
git add .
git commit -m "Resolved merge conflicts"
git push origin main
```

### Production Directory Out of Sync
If production directory has local changes:
```batch
cd D:\AgentSkill\cerebraSkills
git reset --hard origin/main
git pull origin main
```

### Push Rejected
If push is rejected (remote has changes you don't have):
```batch
cd D:\Cerebra\cerebraSkills
git pull --rebase origin main
git push origin main
```

## Automation Ideas

### Auto-sync on file change (optional)
You could set up a file watcher to automatically run `sync-to-production.bat` when files change, but this is not recommended for production use.

### Scheduled sync (optional)
Set up a Windows Task Scheduler to run `update-skills.bat` periodically to keep production up to date.

## Notes

- The development directory (`D:\Cerebra`) is your source of truth for edits
- The production directory (`D:\AgentSkill`) should always mirror GitHub
- GitHub acts as the central repository and version control system
- Multi-agent systems read from production directory only
