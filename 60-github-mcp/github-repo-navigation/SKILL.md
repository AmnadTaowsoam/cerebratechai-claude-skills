# GitHub Repository Navigation

## Overview

Repository navigation covers techniques and tools for efficiently finding, understanding, and working with code in GitHub repositories. This skill includes code search, file exploration, understanding repository structure, and using GitHub's navigation features effectively.

**When to use this skill:** When exploring new repositories, finding specific code, or understanding project structure.

## Table of Contents

1. [Repository Structure](#repository-structure)
2. [Code Search Techniques](#code-search-techniques)
3. [File Navigation](#file-navigation)
4. [Understanding History](#understanding-history)
5. [Navigation Tools](#navigation-tools)
6. [Navigation Checklist](#navigation-checklist)
7. [Quick Reference](#quick-reference)

---

## Repository Structure

### Standard Directory Layout

```
repository/
├── .github/              # GitHub-specific files
│   ├── workflows/        # CI/CD workflows
│   ├── actions/          # Custom actions
│   ├── ISSUE_TEMPLATE/   # Issue templates
│   └── PULL_REQUEST_TEMPLATE/
├── src/                  # Source code
│   ├── api/            # API layer
│   ├── components/      # UI components
│   └── utils/           # Utilities
├── tests/                # Test files
├── docs/                 # Documentation
├── scripts/              # Build/utility scripts
├── config/               # Configuration files
├── public/               # Static assets
├── package.json          # Dependencies
├── README.md             # Project documentation
├── CONTRIBUTING.md       # Contribution guide
└── LICENSE               # License file
```

### Common File Patterns

| Pattern | Location | Purpose |
|---------|-----------|---------|
| `*.config.js` | Root | Configuration |
| `*.test.js` | tests/ | Unit tests |
| `*.spec.js` | tests/ | Spec tests |
| `*.md` | docs/ | Documentation |
| `Dockerfile` | Root | Container config |
| `.env.example` | Root | Environment template |

### Monorepo Structure

```
monorepo/
├── packages/
│   ├── package-a/
│   ├── package-b/
│   └── package-c/
├── apps/
│   ├── web/
│   └── mobile/
├── services/
│   ├── api/
│   └── worker/
├── shared/
│   ├── utils/
│   └── types/
└── package.json
```

---

## Code Search Techniques

### GitHub Search Syntax

| Operator | Description | Example |
|----------|-------------|----------|
| `repo:` | Search in specific repo | `repo:owner/repo query` |
| `org:` | Search in organization | `org:orgname query` |
| `language:` | Filter by language | `language:javascript query` |
| `filename:` | Search by filename | `filename:package.json` |
| `path:` | Search in path | `path:src/api query` |
| `extension:` | Filter by extension | `extension:js query` |
| `in:` | Search location | `in:file`, `in:path`, `in:comment` |
| `user:` | Filter by user | `user:username query` |

### Advanced Search Queries

```bash
# Find function definition
repo:owner/repo language:javascript "function authenticate"

# Find TODO comments
repo:owner/repo "TODO" in:file

# Find specific file
repo:owner/repo filename:dockerfile

# Find in specific directory
repo:owner/repo path:src/api "endpoint"

# Find by author
repo:owner/repo user:username "feature"

# Find recent changes
repo:owner/repo "bug" updated:>2024-01-01

# Find in issues
repo:owner/repo "error" in:issue

# Find in PRs
repo:owner/repo "refactor" in:pr
```

### Code Search Best Practices

| Practice | Description |
|----------|-------------|
| **Use specific terms** | Search for exact function names |
| **Filter by language** | Narrow down results |
| **Use file patterns** | Search specific file types |
| **Combine operators** | Use multiple filters |
| **Search paths** | Limit to directories |
| **Check dates** | Find recent changes |
| **Review context** | Look at surrounding code |

---

## File Navigation

### GitHub Web Navigation

```
1. Repository root
   ↓
2. Click on folder
   ↓
3. Browse files
   ↓
4. Click file to view
   ↓
5. Use blame to see history
   ↓
6. Use raw for copy
```

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `t` | Activate file finder |
| `s` | Focus search bar |
| `w` | Switch branch/tag |
| `y` | Copy file path |
| `b` | Find file |
| `.` | Go to repository root |
| `l` | Go to issues |
| `p` | Go to pull requests |
| `g p` | Go to pulse |
| `g a` | Go to actions |

### File Operations

```bash
# View file raw content
gh api repos/:owner/:repo/contents/:path?ref=main

# Download file
gh api repos/:owner/:repo/contents/:path?ref=main \
  --method GET \
  -H "Accept: application/vnd.github.v3.raw"

# Get file history
gh api repos/:owner/:repo/commits?path=:path

# Get blame information
gh api repos/:owner/:repo/commits?path=:path
```

---

## Understanding History

### Commit History

```bash
# View commit history
gh repo view

# View file history
gh api repos/:owner/:repo/commits?path=:path

# View commit details
gh api repos/:owner/:repo/commits/:sha

# Compare commits
gh api repos/:owner/:repo/compare/:base...:head

# View diff
gh pr diff 123
```

### Blame View

```bash
# View blame for file
gh blame :path

# View blame for specific line
gh blame :path -L 10

# View blame with date
gh blame :path --date
```

### Branch Navigation

```bash
# List all branches
gh repo view --json defaultBranchRef

# List remote branches
gh api repos/:owner/:repo/branches

# Switch branch
gh repo checkout main

# View branch comparison
gh repo compare main...feature-branch
```

---

## Navigation Tools

### GitHub CLI

```bash
# Repository overview
gh repo view

# List repositories
gh repo list

# Clone repository
gh repo clone owner/repo

# Fork repository
gh repo fork owner/repo

# Create repository
gh repo create my-repo --public

# View issues
gh issue list

# View pull requests
gh pr list

# View releases
gh release list
```

### VS Code Integration

```bash
# Open repository in VS Code
gh repo clone owner/repo && code repo

# Open specific file
gh repo clone owner/repo && code repo --file src/index.js

# Open PR in VS Code
gh pr checkout 123 && code .
```

### Git Navigation

```bash
# Navigate to repository
cd path/to/repo

# View git status
git status

# View current branch
git branch

# Switch branch
git checkout branch-name

# View commit log
git log

# View file changes
git diff

# Search commits
git log --grep="search term"

# Search file content
git grep "search term"
```

---

## Navigation Checklist

### Exploring New Repository

```markdown
## Repository Exploration Checklist

### Initial Assessment
- [ ] README.md reviewed
- [ ] Project structure understood
- [ ] Main branch identified
- [ ] Contribution guidelines read
- [ ] License reviewed
- [ ] Documentation checked

### Code Navigation
- [ ] Entry point identified
- [ ] Key directories located
- [ ] Configuration files found
- [ ] Test structure understood
- [ ] Dependencies reviewed

### Search Strategy
- [ ] Search terms identified
- [ ] File patterns determined
- [ ] Language filters applied
- [ ] Path filters used
- [ ] Results reviewed
```

### Finding Specific Code

```markdown
## Code Search Checklist

### Search Preparation
- [ ] Search terms defined
- [ ] File patterns identified
- [ ] Language specified
- [ ] Repository scoped
- [ ] Date filters applied

### Search Execution
- [ ] Query constructed
- [ ] Filters applied
- [ ] Results reviewed
- [ ] Context examined
- [ ] Multiple sources checked

### Results Analysis
- [ ] Relevant files identified
- [ ] Code patterns understood
- [ ] Related code found
- [ ] Dependencies traced
- [ ] Usage documented
```

---

## Quick Reference

### Search Query Examples

| Goal | Query |
|-------|--------|
| Find function | `repo:owner/repo "function name"` |
| Find TODO | `repo:owner/repo "TODO" in:file` |
| Find config | `repo:owner/repo filename:config.js` |
| Find API routes | `repo:owner/repo path:src/api "router"` |
| Find tests | `repo:owner/repo extension:test.js` |
| Find recent bug fix | `repo:owner/repo "bug" updated:>2024-01-01` |

### File Path Patterns

| Pattern | Matches |
|---------|----------|
| `src/**/*` | All files in src |
| `**/*.test.js` | All test files |
| `config/*.json` | All JSON configs |
| `docs/**/*.md` | All markdown docs |
| `*.spec.js` | All spec files |

### Navigation Commands

```bash
# GitHub CLI
gh repo view                    # Repository overview
gh repo list                    # List repositories
gh issue list                   # List issues
gh pr list                      # List PRs
gh blame :path                   # View blame
gh repo checkout main              # Switch branch

# Git
git log --oneline             # Compact history
git log --graph               # Branch graph
git show :sha                 # Show commit
git diff HEAD~1 HEAD         # Show changes
git grep "pattern"            # Search content
```

### Navigation Metrics

| Metric | Target | How to Track |
|--------|--------|----------------|
| **Search success rate** | > 80% | Found what looking for |
| **Time to locate code** | < 5 min | Average search time |
| **Files reviewed per session** | 10-20 | Productivity metric |
| **Documentation usage** | > 50% | Use docs for navigation |
| **Blame usage** | Regularly | Understand changes |

---

## Common Pitfalls

1. **Not reading README** - Always start with documentation
2. **Poor search terms** - Use specific, relevant keywords
3. **Ignoring filters** - Use filters to narrow results
4. **Not exploring structure** - Understand project layout first
5. **Relying only on search** - Browse directories too
6. **Not using blame** - Understand code history
7. **Ignoring docs** - Documentation guides navigation
8. **Not using CLI** - CLI is faster than web UI

## Additional Resources

- [GitHub Search Documentation](https://docs.github.com/en/search-github/searching-on-github)
- [GitHub CLI Documentation](https://cli.github.com/)
- [Repository Structure Best Practices](https://github.com/goldberghoni/folder-structure-convention)
