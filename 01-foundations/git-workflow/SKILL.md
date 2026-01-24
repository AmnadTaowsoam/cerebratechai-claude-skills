### **03: Git Workflow and Best Practices**

> 
> **Current Level:** Expert (Enterprise Scale) 
> 
> 
> **Domain:** Foundations / Version Control 
> 

---

### **1. Executive Summary & Strategic Necessity**

* **Context:** ในโลกปี 2025-2026 การพัฒนาซอฟต์แวร์ทีมงานต้องมีระบบควบคุมเวอร์ชันที่มีประสิทธิภาพ Git Workflow คือกระบวนการที่ช่วยให้ทีมพัฒนาสามารถจัดการการเปลี่ยนแปลงโค้ดอย่างเป็นระบบ ลดความขัดแย้ง และเพิ่มประสิทธิภาพในการทำงานร่วมกัน
* **Business Impact:** การใช้ Git Workflow ที่มีประสิทธิภาพช่วย:
  - ลดความขัดแย้งในการพัฒนาโค้ด (Merge Conflicts)
  - เพิ่มความเสถียรของระบบ
  - เพิ่มประสิทธิภาพในการทำงานร่วมกัน
  - ลดเวลาในการแก้ไขปัญหา
  - เพิ่มความสามารถในการติดตามการเปลี่ยนแปลง
  - ลดความเสี่ยงในการ Deploy
  - เพิ่มความโปร่งใสในการพัฒนา
* **Product Thinking:** ทักษะนี้ช่วยแก้ปัญหา (Pain Point) ให้กับ:
  - ทีมพัฒนาที่ต้องการ Workflow ที่เป็นระบบ
  - ผู้ทำงานที่ต้องการความโปร่งใสในการพัฒนา
  - ทีมพัฒนาที่ต้องการลด Merge Conflicts
  - ผู้จัดการที่ต้องการติดตามความคืบหน้า
  - ทีม DevOps ที่ต้องการ CI/CD ที่เป็นระบบ

### **2. Technical Deep Dive (The "How-to")**

* **Core Logic:** Git Workflow ประกอบด้วย:
  - **Branching Strategies:** กลยุทธ์การแยก Branch (Git Flow, GitHub Flow, Trunk-Based Development)
  - **Commit Conventions:** การตั้งชื่อ Commit ที่เป็นมาตรฐาน (Conventional Commits)
  - **Pull Request Process:** กระบวนการทบทวนและรวมโค้ด (Code Review, Approval, Merge)
  - **Merge Strategies:** กลยุทธ์การรวม Branch (Merge, Squash, Rebase)
  - **Release Management:** การจัดการการเผยแพร่ (Semantic Versioning, Tagging, Release Notes)
  - **Hotfix Process:** กระบวนการแก้ไขปัญหาเร่งด่วน (Hotfix Workflow, Rollback)

* **Architecture Diagram Requirements:** แผนผังสถาปัตยกรรมที่ต้องมี:
  - **Git Flow Diagram:** แผนผังแสดง Branch Structure ของ Git Flow
  - **GitHub Flow Diagram:** แผนผังแสดง Branch Structure ของ GitHub Flow
  - **Pull Request Workflow Diagram:** แผนผังแสดงกระบวนการ Pull Request
  - **Release Process Diagram:** แผนผังแสดงกระบวนการ Release
  - **Hotfix Workflow Diagram:** แผนผังแสดงกระบวนการ Hotfix

* **Implementation Workflow:**
  1. **Choose Branching Strategy:** เลือกกลยุทธ์ Branching ที่เหมาะสม
  2. **Setup Git Hooks:** ตั้งค่า Git Hooks สำหรับ Validation
  3. **Configure CI/CD:** ตั้งค่า CI/CD Pipeline
  4. **Define Commit Conventions:** กำหนด Commit Message Standards
  5. **Train Team on Workflow:** ฝึกอบรมทีมเกี่ยวกับ Workflow
  6. **Implement Pull Request Process:** ดำเนินการ Pull Request Process
  7. **Monitor and Improve:** ติดตามและปรับปรุง Workflow

### **3. Tooling & Tech Stack**

* **Enterprise Tools:** เครื่องมือระดับอุตสาหกรรมที่เลือกใช้:
  - **Git Platforms:** GitHub, GitLab, Bitbucket, Azure DevOps
  - **Git Clients:** GitKraken, SourceTree, VS Code Git Integration
  - **Git Hooks:** Husky, pre-commit, commitlint
  - **Linting Tools:** ESLint, Prettier, Black, isort
  - **CI/CD Platforms:** GitHub Actions, GitLab CI, Azure Pipelines, Jenkins
  - **Release Tools:** semantic-release, standard-version, conventional-changelog

* **Configuration Essentials:** ส่วนประกอบสำคัญในการตั้งค่า:
  - **Git Configuration:** การตั้งค่า Git User, Email, Aliases
  - **Branch Protection Rules:** กฎการป้องกัน Branch (Require Review, Require Status Checks)
  - **Commitlint Configuration:** การตั้งค่า Commitlint สำหรับ Validation
  - **Husky Configuration:** การตั้งค่า Husky สำหรับ Git Hooks
  - **lint-staged Configuration:** การตั้งค่า lint-staged สำหรับ Linting ก่อน Commit
  - **Release Configuration:** การตั้งค่า Release Automation

### **4. Standards, Compliance & Security**

* **International Standards:** มาตรฐานที่เกี่ยวข้อง:
  - **Conventional Commits:** มาตรฐานสำหรับ Commit Messages
  - **Semantic Versioning:** มาตรฐานสำหรับ Versioning (MAJOR.MINOR.PATCH)
  - **Git Best Practices:** แนวทางปฏิบัติที่ดีในการใช้ Git
  - **Git Security:** แนวทางปฏิบัติด้านความปลอดใจในการใช้ Git

* **Security Protocol:** กลไกการป้องกัน:
  - **Branch Protection Rules:** กฎการป้องกัน Branch (Require Review, Require Status Checks)
  - **Pre-commit Hooks:** การตรวจสอบก่อน Commit (Linting, Security Scanning)
  - **Pre-push Hooks:** การตรวจสอบก่อน Push (Test Suite, Security Scanning)
  - **Signed Commits:** การลงนาม Commits สำหรับความเปลอดใจ
  - **Access Control:** การควบคุมการเข้าถึง Repository
  - **Audit Trail:** การบันทึกการเข้าถึงและการเปลี่ยนแปลง

* **Explainability:** ความสามารถในการอธิบาย:
  - **Commit Message Documentation:** การบันทึก Commit Messages ที่ชัดเจน
  - **Branch Naming Documentation:** การบันทึก Branch Naming Conventions
  - **Workflow Documentation:** การบันทึก Workflow และ Processes
  - **Release Notes:** การบันทึก Release Notes ที่ชัดเจน

### **5. Unit Economics & Performance Metrics (KPIs)**

* **Cost Calculation:** สูตรการคำนวณต้นทุนต่อหน่วย (COGS):
  ```
  Total Cost = (Merge Conflict Resolution Time × Hourly Rate) + 
               (Hotfix Time × Hourly Rate) + 
               (Tooling Cost)
  
  ROI = (Productivity Gain - Total Cost) / Total Cost × 100%
  
  Productivity Gain = (Time Saved on Conflicts) + 
                      (Time Saved on Reviews) + 
                      (Time Saved on Deployments)
  ```

* **Key Performance Indicators:** ตัวชี้วัดความสำเร็จทางเทคนิค:
  - **Merge Conflict Rate:** % ของ Pull Requests ที่มี Merge Conflicts (Target: < 10%)
  - **Review Turnaround Time:** เวลาเฉลี่ยในการ Review (Target: < 24 hours)
  - **Deployment Frequency:** จำนวน Deployments ต่อสัปดาห์ (Target: > 5/week)
  - **Lead Time:** เวลาเฉลี่ยจาก Commit ไป Deploy (Target: < 24 hours)
  - **Change Failure Rate:** % ของ Deployments ที่ล้มเหลว (Target: < 5%)
  - **Team Productivity:** จำนวน Commits ต่อวัน (Target: > 10/day)

### **6. Strategic Recommendations (CTO Insights)**

* **Phase Rollout:** คำแนะนำในการทยอยเริ่มใช้งาน:
  1. **Phase 1 (Months 1-2):** สร้าง Git Workflow Standards และ Guidelines, ฝึกอบรมทีม
  2. **Phase 2 (Months 3-4):** ตั้งค่า Git Hooks และ CI/CD Pipeline
  3. **Phase 3 (Months 5-6):** ฝึกอบรมทีมเกี่ยวกับ Workflow และ Processes
  4. **Phase 4 (Year 2+):** ขยายไปยังทุกทีม, สร้าง Culture ของ Git Best Practices

* **Pitfalls to Avoid:** ข้อควรระวังที่มักจะผิดพลาด:
  - **Over-Engineering:** หลีกเลี่ยงการสร้าง Workflow ที่ซับซ้อนเกินไป
  - **Not Following Standards:** ต้องทบทวนตามหลักการ Git Standards
  - **Skipping Reviews:** หลีกเลี่ยงการข้าม Review สำหรับ PR ที่สำคัญ
  - **Not Protecting Branches:** ต้องป้องกัน Branch ที่สำคัญ (main, develop)
  - **Not Using Hooks:** หลีกเลี่ยงการไม่ใช้ Git Hooks สำหรับ Validation
  - **Not Documenting:** ต้องบันทึก Workflow และ Processes อย่างชัดเจน
  - **Not Training Team:** ต้องฝึกอบรมทีมเกี่ยวกับ Workflow และ Best Practices

---

## Overview

Git workflow patterns, branching strategies, and best practices for maintaining clean, collaborative repositories. Consistent Git practices improve code quality, simplify debugging, and streamline team collaboration.

## Branch Naming Conventions

### Standard Branch Prefixes

| Prefix | Purpose | Example |
|--------|---------|---------|
| `feature/` | New features or enhancements | `feature/user-authentication` |
| `bugfix/` | Non-urgent bug fixes | `bugfix/login-validation-error` |
| `hotfix/` | Urgent production fixes | `hotfix/payment-crash` |
| `release/` | Release preparation | `release/v2.1.0` |
| `docs/` | Documentation updates | `docs/api-reference` |
| `refactor/` | Code refactoring | `refactor/user-service` |
| `test/` | Test additions or fixes | `test/payment-integration` |
| `chore/` | Maintenance tasks | `chore/update-dependencies` |

### Naming Rules

```bash
# GOOD: Descriptive, lowercase, hyphen-separated
feature/add-user-profile-page
bugfix/fix-cart-total-calculation
hotfix/resolve-payment-timeout

# BAD: Vague, inconsistent formatting
feature/newStuff
Feature/UserAuth
fix_bug
my-branch
```

### Including Ticket Numbers

```bash
# With ticket reference
feature/PROJ-123-user-authentication
bugfix/PROJ-456-fix-login-redirect

# Short descriptive names (when no ticket system)
feature/oauth2-google-login
bugfix/null-pointer-user-service
```

### Branch Naming Template

```
<type>/<ticket-id>-<short-description>

# Examples:
feature/JIRA-100-add-payment-gateway
bugfix/GH-42-fix-memory-leak
hotfix/PROD-001-database-connection
```

## Commit Message Format

### Conventional Commits Specification

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(cart): correct total calculation` |
| `docs` | Documentation only | `docs(readme): update installation steps` |
| `style` | Formatting, no code change | `style(api): fix indentation` |
| `refactor` | Code change, no new feature or fix | `refactor(user): extract validation logic` |
| `test` | Adding or updating tests | `test(payment): add integration tests` |
| `chore` | Maintenance, dependencies | `chore(deps): update lodash to 4.17.21` |
| `perf` | Performance improvement | `perf(query): add database index` |
| `ci` | CI/CD changes | `ci(github): add caching to workflow` |
| `build` | Build system changes | `build(docker): optimize image size` |
| `revert` | Revert previous commit | `revert: feat(auth): add OAuth2 login` |

### Commit Message Examples

#### Simple Commit
```
feat(auth): add password reset functionality
```

#### Commit with Body
```
fix(payment): resolve race condition in checkout

The checkout process was allowing multiple simultaneous
submissions, causing duplicate charges. Added a mutex
lock to prevent concurrent checkout operations.

Closes #234
```

#### Breaking Change
```
feat(api)!: change user endpoint response format

BREAKING CHANGE: The /api/users endpoint now returns
a paginated response instead of an array. Clients must
update to handle the new { data: [], meta: {} } format.

Migration guide: docs/migration/v2-users-endpoint.md
```

#### Multi-line with Co-authors
```
feat(dashboard): add real-time analytics widget

- Add WebSocket connection for live data
- Create Chart.js visualization component
- Implement data aggregation service

Co-authored-by: Jane Doe <jane@example.com>
Co-authored-by: John Smith <john@example.com>
```

### Commit Message Rules

```bash
# GOOD: Clear, imperative mood, specific
feat(user): add email verification on signup
fix(api): handle null response from payment gateway
refactor(auth): extract JWT validation to middleware

# BAD: Vague, past tense, no type
updated stuff
fixed bug
WIP
asdfasdf
changed the code to fix the thing
```

### Subject Line Guidelines

1. **Use imperative mood**: "add feature" not "added feature"
2. **Capitalize first letter**: "Add feature" not "add feature"
3. **No period at end**: "Add feature" not "Add feature."
4. **Max 50 characters**: Keep it concise
5. **Reference issues**: Include ticket numbers when applicable

## Git Flow vs GitHub Flow

### Git Flow

Best for: Projects with scheduled releases, multiple versions in production

```
main (production)
  │
  ├── develop (integration)
  │     │
  │     ├── feature/user-auth
  │     ├── feature/payment
  │     └── feature/dashboard
  │
  ├── release/v1.2.0
  │
  └── hotfix/critical-bug
```

#### Git Flow Branches

| Branch | Purpose | Merges To |
|--------|---------|-----------|
| `main` | Production code | - |
| `develop` | Integration branch | `main` (via release) |
| `feature/*` | New features | `develop` |
| `release/*` | Release preparation | `main` and `develop` |
| `hotfix/*` | Production fixes | `main` and `develop` |

#### Git Flow Commands

```bash
# Start a new feature
git checkout develop
git checkout -b feature/new-feature

# Finish feature (merge to develop)
git checkout develop
git merge --no-ff feature/new-feature
git branch -d feature/new-feature

# Start a release
git checkout develop
git checkout -b release/v1.2.0

# Finish release
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"
git checkout develop
git merge --no-ff release/v1.2.0
git branch -d release/v1.2.0

# Hotfix
git checkout main
git checkout -b hotfix/critical-fix
# ... make fixes ...
git checkout main
git merge --no-ff hotfix/critical-fix
git tag -a v1.2.1 -m "Hotfix v1.2.1"
git checkout develop
git merge --no-ff hotfix/critical-fix
git branch -d hotfix/critical-fix
```

### GitHub Flow

Best for: Continuous deployment, web applications, smaller teams

```
main (always deployable)
  │
  ├── feature/user-auth ──── PR ──── main
  ├── feature/payment ────── PR ──── main
  └── bugfix/login-error ─── PR ──── main
```

#### GitHub Flow Process

1. Create branch from `main`
2. Make commits
3. Open Pull Request
4. Review and discuss
5. Deploy and test (optional)
6. Merge to `main`

```bash
# GitHub Flow workflow
git checkout main
git pull origin main
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat: add new feature"

# Push and create PR
git push -u origin feature/new-feature
# Create PR via GitHub UI or CLI

# After PR approval and merge
git checkout main
git pull origin main
git branch -d feature/new-feature
```

### Comparison Table

| Aspect | Git Flow | GitHub Flow |
|--------|----------|-------------|
| Complexity | High | Low |
| Release cycle | Scheduled | Continuous |
| Branches | Multiple long-lived | Single (`main`) |
| Best for | Mobile apps, versioned software | Web apps, SaaS |
| Learning curve | Steep | Gentle |
| Hotfixes | Dedicated process | Same as features |

## Pull Request Process

### PR Checklist (Author)

- [ ] Branch is up to date with target branch
- [ ] All tests pass locally
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated if needed
- [ ] Commit history is clean
- [ ] PR description is complete

### PR Description Template

```markdown
## Summary
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Changes Made
- Added X component
- Fixed Y bug in Z module
- Updated API endpoint for W

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots (if applicable)
| Before | After |
|--------|-------|
| img    | img   |

## Related Issues
Closes #123
Related to #456

## Checklist
- [ ] My code follows the project style guidelines
- [ ] I have performed a self-review
- [ ] I have commented hard-to-understand areas
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests proving my fix/feature works
- [ ] All tests pass locally
```

### PR Review Checklist (Reviewer)

- [ ] Code logic is correct
- [ ] No security vulnerabilities
- [ ] Performance is acceptable
- [ ] Tests are adequate
- [ ] Documentation is updated
- [ ] Code style is consistent

### PR Size Guidelines

| Lines Changed | Classification | Review Time |
|---------------|----------------|-------------|
| < 50 | Tiny | Minutes |
| 50-200 | Small | < 30 min |
| 200-400 | Medium | 30-60 min |
| 400-800 | Large | 1-2 hours |
| > 800 | Too Large | Split it! |

## Merge Strategies

### Merge Commit (--no-ff)

Preserves complete history with merge commit.

```bash
git checkout main
git merge --no-ff feature/user-auth
```

```
*   Merge branch 'feature/user-auth'
|\
| * feat: add password validation
| * feat: add login form
| * feat: add user model
|/
* Previous commit on main
```

**Pros:**
- Complete history preserved
- Clear feature boundaries
- Easy to revert entire feature

**Cons:**
- Cluttered history
- Many merge commits

**Best for:** Git Flow, features that should be grouped

### Squash and Merge

Combines all commits into single commit.

```bash
git checkout main
git merge --squash feature/user-auth
git commit -m "feat(auth): add user authentication"
```

```
* feat(auth): add user authentication
* Previous commit on main
```

**Pros:**
- Clean, linear history
- One commit per feature
- Easy to understand

**Cons:**
- Loses detailed commit history
- Harder to debug individual changes

**Best for:** GitHub Flow, small features, messy commit histories

### Rebase and Merge

Replays commits on top of target branch.

```bash
git checkout feature/user-auth
git rebase main
git checkout main
git merge feature/user-auth  # Fast-forward
```

```
* feat: add password validation
* feat: add login form
* feat: add user model
* Previous commit on main
```

**Pros:**
- Linear history
- Individual commits preserved
- No merge commits

**Cons:**
- Rewrites history
- Can cause issues with shared branches
- Conflicts resolved per-commit

**Best for:** Clean commit histories, personal branches

### Strategy Comparison

| Strategy | History | Complexity | Revert | Best For |
|----------|---------|------------|--------|----------|
| Merge | Non-linear | Low | Easy (whole feature) | Git Flow |
| Squash | Linear | Low | Easy (single commit) | GitHub Flow |
| Rebase | Linear | High | Hard | Clean histories |

### Recommended Approach by Scenario

```bash
# Feature branch with clean commits → Rebase and merge
git checkout feature/clean-history
git rebase main
git checkout main
git merge --ff-only feature/clean-history

# Feature branch with messy commits → Squash and merge
git checkout main
git merge --squash feature/messy-history
git commit -m "feat: add complete feature"

# Long-running feature branch → Merge commit
git checkout main
git merge --no-ff feature/long-running
```

## Common Git Commands and Scenarios

### Daily Workflow

```bash
# Start your day - update local main
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/new-feature

# Stage and commit changes
git add .
git commit -m "feat: add new component"

# Push to remote
git push -u origin feature/new-feature

# Keep branch updated with main
git fetch origin
git rebase origin/main
# or
git merge origin/main
```

### Undoing Changes

```bash
# Discard unstaged changes in a file
git checkout -- <file>
# or (Git 2.23+)
git restore <file>

# Unstage a file (keep changes)
git reset HEAD <file>
# or (Git 2.23+)
git restore --staged <file>

# Undo last commit (keep changes staged)
git reset --soft HEAD~1

# Undo last commit (keep changes unstaged)
git reset HEAD~1

# Undo last commit (discard changes) - DANGEROUS
git reset --hard HEAD~1

# Revert a specific commit (creates new commit)
git revert <commit-hash>

# Revert merge commit
git revert -m 1 <merge-commit-hash>
```

### Working with Stash

```bash
# Stash current changes
git stash

# Stash with message
git stash push -m "WIP: user authentication"

# List stashes
git stash list

# Apply most recent stash (keep in stash list)
git stash apply

# Apply and remove from stash list
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Drop a stash
git stash drop stash@{0}

# Clear all stashes
git stash clear

# Create branch from stash
git stash branch new-branch stash@{0}
```

### Branch Management

```bash
# List all branches
git branch -a

# List branches with last commit
git branch -v

# Delete local branch
git branch -d feature/completed
git branch -D feature/force-delete  # Force delete

# Delete remote branch
git push origin --delete feature/old-branch

# Rename current branch
git branch -m new-name

# Rename specific branch
git branch -m old-name new-name

# Track remote branch
git branch -u origin/feature/branch

# See which branches are merged
git branch --merged main
git branch --no-merged main
```

### Viewing History

```bash
# View commit history
git log

# One line per commit
git log --oneline

# With graph
git log --oneline --graph --all

# Show files changed in each commit
git log --stat

# Show changes in each commit
git log -p

# Filter by author
git log --author="John"

# Filter by date
git log --since="2024-01-01" --until="2024-12-31"

# Filter by message
git log --grep="fix"

# Show commits affecting a file
git log -- <file>

# Show who changed each line
git blame <file>

# Show specific line range
git blame -L 10,20 <file>
```

### Cherry-picking

```bash
# Apply specific commit to current branch
git cherry-pick <commit-hash>

# Cherry-pick without committing
git cherry-pick --no-commit <commit-hash>

# Cherry-pick range of commits
git cherry-pick <start-hash>^..<end-hash>

# Continue after resolving conflicts
git cherry-pick --continue

# Abort cherry-pick
git cherry-pick --abort
```

### Interactive Rebase

```bash
# Rebase last N commits
git rebase -i HEAD~5

# Rebase onto main
git rebase -i main

# Commands in interactive rebase:
# pick   - use commit
# reword - use commit, edit message
# edit   - use commit, stop for amending
# squash - meld into previous commit
# fixup  - like squash, discard message
# drop   - remove commit
```

### Working with Remotes

```bash
# List remotes
git remote -v

# Add remote
git remote add upstream https://github.com/original/repo.git

# Remove remote
git remote remove upstream

# Rename remote
git remote rename origin upstream

# Fetch from all remotes
git fetch --all

# Prune deleted remote branches
git fetch --prune
git remote prune origin
```

## .gitignore Best Practices

### Basic Patterns

```gitignore
# Ignore specific file
secret.txt

# Ignore all files with extension
*.log
*.tmp

# Ignore directory
node_modules/
dist/
build/

# Ignore files in any directory
**/*.pyc

# Negate pattern (don't ignore)
!important.log

# Ignore in root only
/config.local.js

# Ignore files starting with
temp*
```

### Comprehensive .gitignore Template

```gitignore
# ===== Dependencies =====
node_modules/
vendor/
.pnp.*
.yarn/*
!.yarn/patches
!.yarn/plugins
!.yarn/releases
!.yarn/sdks
!.yarn/versions

# ===== Build Outputs =====
dist/
build/
out/
.next/
.nuxt/
.output/
*.tsbuildinfo

# ===== Environment & Secrets =====
.env
.env.local
.env.*.local
*.pem
*.key
secrets/
credentials.json

# ===== IDE & Editor =====
.idea/
.vscode/*
!.vscode/settings.json
!.vscode/extensions.json
*.swp
*.swo
*~
.project
.classpath

# ===== OS Files =====
.DS_Store
.DS_Store?
Thumbs.db
ehthumbs.db
Desktop.ini

# ===== Logs =====
logs/
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# ===== Testing =====
coverage/
.nyc_output/
*.lcov
.jest/

# ===== Cache =====
.cache/
.parcel-cache/
.eslintcache
.stylelintcache
*.tscache

# ===== Python =====
__pycache__/
*.py[cod]
*$py.class
.Python
*.egg-info/
.eggs/
venv/
.venv/
ENV/

# ===== Java =====
*.class
*.jar
*.war
target/

# ===== Database =====
*.sqlite
*.sqlite3
*.db

# ===== Misc =====
*.bak
*.backup
*.orig
temp/
tmp/
```

### Per-Language Templates

```bash
# Download gitignore templates
curl -o .gitignore https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore

# Combine multiple templates
curl -s https://raw.githubusercontent.com/github/gitignore/main/Node.gitignore >> .gitignore
curl -s https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore >> .gitignore
```

### Global .gitignore

```bash
# Create global gitignore
touch ~/.gitignore_global

# Configure Git to use it
git config --global core.excludesfile ~/.gitignore_global
```

```gitignore
# ~/.gitignore_global - OS and editor files
.DS_Store
Thumbs.db
.idea/
*.swp
*~
```

## Handling Merge Conflicts

### Understanding Conflict Markers

```
<<<<<<< HEAD
Your current branch changes
=======
Incoming changes from merged branch
>>>>>>> feature/branch-name
```

### Step-by-Step Resolution

```bash
# 1. Start merge that causes conflict
git merge feature/other-branch

# 2. See which files have conflicts
git status

# 3. Open conflicted file and resolve manually
# Edit the file, remove conflict markers, keep desired code

# 4. Stage resolved files
git add <resolved-file>

# 5. Complete the merge
git commit -m "Merge feature/other-branch, resolve conflicts"

# Or abort if needed
git merge --abort
```

### Visual Merge Tools

```bash
# Configure merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Use merge tool
git mergetool
```

### Common Conflict Scenarios

#### Both Modified Same Lines

```bash
# File: src/config.js
<<<<<<< HEAD
const API_URL = 'https://api.production.com';
=======
const API_URL = 'https://api.staging.com';
>>>>>>> feature/update-config

# Resolution: Choose appropriate value or combine
const API_URL = process.env.API_URL || 'https://api.production.com';
```

#### File Deleted in One Branch

```bash
# One branch deleted the file, other modified it
git status
# both deleted:    old-file.js
# or
# deleted by them: old-file.js

# Keep the file
git add old-file.js

# Or accept deletion
git rm old-file.js
```

#### Rebase Conflicts

```bash
# During rebase
git rebase main

# Conflicts occur - resolve them, then:
git add <resolved-files>
git rebase --continue

# Or abort
git rebase --abort

# Skip problematic commit
git rebase --skip
```

### Prevention Strategies

1. **Keep branches short-lived** - Less time for divergence
2. **Regularly sync with main** - `git merge main` or `git rebase main`
3. **Communicate with team** - Know who's working on what
4. **Small, focused commits** - Easier to resolve conflicts
5. **Use feature flags** - Multiple features can coexist

## Git Hooks

### Available Hooks

| Hook | Trigger | Common Use |
|------|---------|------------|
| `pre-commit` | Before commit created | Linting, formatting |
| `prepare-commit-msg` | Before editor opens | Add ticket numbers |
| `commit-msg` | After message entered | Validate format |
| `post-commit` | After commit created | Notifications |
| `pre-push` | Before push to remote | Run tests |
| `pre-rebase` | Before rebase starts | Prevent on shared branches |
| `post-merge` | After merge completes | Install dependencies |
| `post-checkout` | After checkout/switch | Environment setup |

### Pre-commit Hook Examples

```bash
#!/bin/sh
# .git/hooks/pre-commit

# Run linter
npm run lint
if [ $? -ne 0 ]; then
  echo "Linting failed. Please fix errors before committing."
  exit 1
fi

# Run type check
npm run type-check
if [ $? -ne 0 ]; then
  echo "Type checking failed. Please fix errors before committing."
  exit 1
fi

# Check for console.log
if git diff --cached --name-only | xargs grep -l 'console.log' 2>/dev/null; then
  echo "Warning: console.log found in staged files"
  exit 1
fi

# Run tests on changed files
npm run test:changed
if [ $? -ne 0 ]; then
  echo "Tests failed. Please fix before committing."
  exit 1
fi

exit 0
```

### Commit-msg Hook (Conventional Commits)

```bash
#!/bin/sh
# .git/hooks/commit-msg

commit_msg=$(cat "$1")

# Regex for conventional commits
pattern="^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert)(\(.+\))?(!)?: .{1,50}"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
  echo "ERROR: Invalid commit message format."
  echo ""
  echo "Expected format: <type>(<scope>): <subject>"
  echo "Example: feat(auth): add password reset"
  echo ""
  echo "Types: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert"
  exit 1
fi

exit 0
```

### Pre-push Hook

```bash
#!/bin/sh
# .git/hooks/pre-push

# Run full test suite before pushing
npm test
if [ $? -ne 0 ]; then
  echo "Tests failed. Push aborted."
  exit 1
fi

# Prevent push to main/master directly
protected_branch='main'
current_branch=$(git symbolic-ref HEAD | sed -e 's,.*/\(.*\),\1,')

if [ "$current_branch" = "$protected_branch" ]; then
  echo "Direct push to $protected_branch is not allowed."
  echo "Please create a pull request instead."
  exit 1
fi

exit 0
```

### Using Husky (Recommended)

```bash
# Install Husky
npm install husky --save-dev

# Initialize Husky
npx husky init

# Add pre-commit hook
echo "npm run lint && npm run test" > .husky/pre-commit

# Add commit-msg hook with commitlint
npm install @commitlint/cli @commitlint/config-conventional --save-dev
echo "npx --no -- commitlint --edit \$1" > .husky/commit-msg
```

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore', 'perf', 'ci', 'build', 'revert']
    ],
    'subject-max-length': [2, 'always', 72],
    'body-max-line-length': [2, 'always', 100]
  }
};
```

### Using lint-staged

```bash
npm install lint-staged --save-dev
```

```json
// package.json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write"
    ],
    "*.{css,scss}": [
      "stylelint --fix",
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
npx lint-staged
```

## Tagging and Releases

### Semantic Versioning

```
MAJOR.MINOR.PATCH

v1.0.0 - Initial release
v1.1.0 - New feature (backward compatible)
v1.1.1 - Bug fix
v2.0.0 - Breaking change
```

### Creating Tags

```bash
# Lightweight tag (just a pointer)
git tag v1.0.0

# Annotated tag (recommended - includes metadata)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Tag specific commit
git tag -a v1.0.0 <commit-hash> -m "Release version 1.0.0"

# Push single tag
git push origin v1.0.0

# Push all tags
git push origin --tags

# List tags
git tag
git tag -l "v1.*"

# Show tag details
git show v1.0.0

# Delete local tag
git tag -d v1.0.0

# Delete remote tag
git push origin --delete v1.0.0
```

### Release Branch Workflow

```bash
# Create release branch
git checkout develop
git checkout -b release/v1.2.0

# Update version numbers
npm version 1.2.0 --no-git-tag-version

# Commit version bump
git commit -am "chore: bump version to 1.2.0"

# Final testing and fixes...

# Merge to main and tag
git checkout main
git merge --no-ff release/v1.2.0
git tag -a v1.2.0 -m "Release v1.2.0"

# Merge back to develop
git checkout develop
git merge --no-ff release/v1.2.0

# Delete release branch
git branch -d release/v1.2.0

# Push everything
git push origin main develop --tags
```

### GitHub Release with CLI

```bash
# Create release from tag
gh release create v1.2.0 --title "v1.2.0" --notes "Release notes here"

# Create release with auto-generated notes
gh release create v1.2.0 --generate-notes

# Create release with notes from file
gh release create v1.2.0 --notes-file CHANGELOG.md

# Upload assets with release
gh release create v1.2.0 ./dist/app.zip ./dist/app.tar.gz

# Create draft release
gh release create v1.2.0 --draft

# Create pre-release
gh release create v1.2.0-beta.1 --prerelease
```

### Automated Changelog

```bash
# Install conventional-changelog
npm install -g conventional-changelog-cli

# Generate changelog
conventional-changelog -p angular -i CHANGELOG.md -s

# Generate from scratch
conventional-changelog -p angular -i CHANGELOG.md -s -r 0
```

## Emergency Hotfix Process

### When to Use Hotfix

- Production is broken
- Security vulnerability discovered
- Critical data loss occurring
- Revenue-impacting bug

### Hotfix Workflow

```bash
# 1. Create hotfix branch from main/production
git checkout main
git pull origin main
git checkout -b hotfix/critical-payment-bug

# 2. Make minimal fix
# Edit files...
git add .
git commit -m "fix(payment): resolve transaction timeout"

# 3. Test thoroughly (even under pressure!)
npm test
npm run e2e

# 4. Merge to main
git checkout main
git merge --no-ff hotfix/critical-payment-bug

# 5. Tag the release
git tag -a v1.2.1 -m "Hotfix: payment timeout"

# 6. Deploy to production
git push origin main --tags

# 7. Merge back to develop (if using Git Flow)
git checkout develop
git merge --no-ff hotfix/critical-payment-bug

# 8. Clean up
git branch -d hotfix/critical-payment-bug
git push origin --delete hotfix/critical-payment-bug
```

### Hotfix Checklist

- [ ] Identify root cause
- [ ] Create hotfix branch from production
- [ ] Make minimal, focused fix
- [ ] Write test for the bug
- [ ] Run existing tests
- [ ] Get quick code review (pair if urgent)
- [ ] Merge and tag
- [ ] Deploy to production
- [ ] Verify fix in production
- [ ] Merge to develop/other branches
- [ ] Document incident
- [ ] Schedule post-mortem

### Hotfix vs Regular Fix

| Aspect | Hotfix | Regular Bugfix |
|--------|--------|----------------|
| Branch from | `main` | `develop` |
| Merge to | `main` + `develop` | `develop` |
| Testing | Minimal required | Full suite |
| Review | Expedited | Standard |
| Deployment | Immediate | Next release |

### Rollback if Hotfix Fails

```bash
# Option 1: Revert the merge commit
git checkout main
git revert -m 1 <merge-commit-hash>
git push origin main

# Option 2: Reset to previous tag (if not pushed widely)
git checkout main
git reset --hard v1.2.0
git push --force origin main  # DANGEROUS - coordinate with team

# Option 3: Deploy previous version
git checkout v1.2.0
# Deploy this version
```

## Quick Reference

### Daily Commands

```bash
git status                    # Check status
git pull                      # Update from remote
git add .                     # Stage all changes
git commit -m "message"       # Commit
git push                      # Push to remote
git log --oneline -10         # Recent history
```

### Branch Commands

```bash
git branch                    # List branches
git checkout -b name          # Create and switch
git checkout name             # Switch branch
git branch -d name            # Delete branch
git merge branch              # Merge branch
```

### Undo Commands

```bash
git checkout -- file          # Discard changes
git reset HEAD file           # Unstage file
git reset --soft HEAD~1       # Undo commit (keep staged)
git reset HEAD~1              # Undo commit (keep unstaged)
git revert <hash>             # Revert commit
```

### Remote Commands

```bash
git remote -v                 # List remotes
git fetch                     # Download changes
git pull                      # Fetch + merge
git push                      # Upload changes
git push -u origin branch     # Push new branch
```

### Commit Message Prefixes

```
feat:     New feature
fix:      Bug fix
docs:     Documentation
style:    Formatting
refactor: Code restructure
test:     Tests
chore:    Maintenance
perf:     Performance
ci:       CI/CD
build:    Build system
```

## Best Practices

1. **Choose the right workflow** - Git Flow for scheduled releases, GitHub Flow for continuous deployment
2. **Keep branches short-lived** - Less time for merge conflicts
3. **Follow commit conventions** - Use Conventional Commits for consistency
4. **Write meaningful commit messages** - Clear, imperative mood, specific
5. **Use descriptive branch names** - Include type and description
6. **Keep PRs small** - Ideal size: 200-400 lines
7. **Review thoroughly** - Check logic, security, performance, tests
8. **Use appropriate merge strategy** - Merge, squash, or rebase based on context
9. **Tag releases** - Use semantic versioning and annotated tags
10. **Automate with hooks** - Use Husky and lint-staged for automation

## Common Pitfalls

1. **Over-engineering workflows** - Keep it simple for your team's needs
2. **Not syncing branches** - Regularly merge or rebase with main
3. **Skipping reviews** - Always review code before merging
4. **Large PRs** - Split large PRs into smaller, focused ones
5. **Poor commit messages** - Follow Conventional Commits specification
6. **Not using hooks** - Automate validation with Git hooks
7. **Force pushing shared branches** - Never force push to main/develop
8. **Ignoring conflicts** - Resolve conflicts promptly and communicate
9. **Not protecting branches** - Use branch protection rules
10. **Hotfixing without testing** - Always test hotfixes thoroughly

## Resources

- [Pro Git Book](https://git-scm.com/book/en/v2) - Comprehensive Git documentation
- [GitHub Flow](https://guides.github.com/introduction/flow/) - GitHub's workflow guide
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/) - Git Flow branching model
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit message specification
- [Semantic Versioning](https://semver.org/) - Versioning specification
- [Husky](https://typicode.github.io/husky/) - Git hooks made easy
- [lint-staged](https://github.com/okonet/lint-staged) - Run linters on staged files
- [commitlint](https://commitlint.js.org/) - Lint commit messages
