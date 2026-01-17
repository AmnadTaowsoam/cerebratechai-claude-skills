---
name: Release Workflow
description: Standardized release processes including versioning, changelog generation, and deployment automation.
---

# Release Workflow

## Overview

Release Workflow defines how code moves from development to production, including versioning, changelog generation, tagging, and deployment automation.

**Core Principle**: "Releases should be boring, predictable, and automated."

---

## 1. Semantic Versioning (SemVer)

Format: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (1.0.0 → 2.0.0)
- **MINOR**: New features, backward compatible (1.0.0 → 1.1.0)
- **PATCH**: Bug fixes, backward compatible (1.0.0 → 1.0.1)

### Examples
```
1.0.0 → 1.0.1  (fix: resolve login bug)
1.0.1 → 1.1.0  (feat: add dark mode)
1.1.0 → 2.0.0  (BREAKING CHANGE: remove deprecated API)
```

---

## 2. Automated Versioning with standard-version

```bash
# Install
npm install --save-dev standard-version

# Add to package.json
{
  "scripts": {
    "release": "standard-version",
    "release:minor": "standard-version --release-as minor",
    "release:major": "standard-version --release-as major"
  }
}
```

### What standard-version does:
1. Bumps version in `package.json`
2. Generates `CHANGELOG.md`
3. Creates git commit
4. Creates git tag

```bash
# Run release
npm run release

# Output:
✔ bumping version in package.json from 1.0.0 to 1.1.0
✔ outputting changes to CHANGELOG.md
✔ committing package.json and CHANGELOG.md
✔ tagging release v1.1.0
```

---

## 3. Changelog Generation

### Automated CHANGELOG.md
```markdown
# Changelog

## [1.1.0] - 2024-01-15

### Features
- **auth**: add OAuth2 support (#123)
- **ui**: implement dark mode (#124)

### Bug Fixes
- **api**: resolve race condition in user creation (#125)
- **cart**: prevent negative quantities (#126)

### BREAKING CHANGES
- User API now requires authentication token
```

---

## 4. Git Tagging Strategy

```bash
# Lightweight tag (not recommended)
git tag v1.0.0

# Annotated tag (recommended)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tags
git push --follow-tags
```

---

## 5. Release Branches

### Git Flow
```
main (production)
  ↑
release/1.1.0
  ↑
develop
  ↑
feature/new-feature
```

### Trunk-Based Development
```
main (production)
  ↑
feature/new-feature (short-lived)
```

---

## 6. GitHub Release Automation

```yaml
# .github/workflows/release.yml
name: Release

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: Release ${{ github.ref }}
          body_path: CHANGELOG.md
          draft: false
          prerelease: false
      
      - name: Build and Deploy
        run: |
          npm ci
          npm run build
          npm run deploy
```

---

## 7. Pre-release Versions

```bash
# Alpha release
1.0.0-alpha.1

# Beta release
1.0.0-beta.1

# Release candidate
1.0.0-rc.1

# Creating pre-release
npm run release -- --prerelease alpha
```

---

## 8. Release Checklist Template

```markdown
## Release Checklist for v1.1.0

### Pre-Release
- [ ] All tests passing
- [ ] No critical bugs
- [ ] Documentation updated
- [ ] CHANGELOG reviewed
- [ ] Breaking changes communicated

### Release
- [ ] Run `npm run release`
- [ ] Push tags: `git push --follow-tags`
- [ ] Verify CI/CD pipeline
- [ ] Monitor deployment

### Post-Release
- [ ] Verify production deployment
- [ ] Monitor error rates
- [ ] Announce release to team
- [ ] Update documentation site
```

---

## 9. Hotfix Workflow

```bash
# Create hotfix branch from main
git checkout -b hotfix/1.0.1 main

# Make fix
git commit -m "fix: resolve critical security issue"

# Release hotfix
npm run release -- --release-as patch

# Merge to main and develop
git checkout main
git merge hotfix/1.0.1
git checkout develop
git merge hotfix/1.0.1
```

---

## 10. Release Workflow Checklist

- [ ] **Semantic Versioning**: Following SemVer?
- [ ] **Automated Versioning**: standard-version configured?
- [ ] **Changelog**: Auto-generated from commits?
- [ ] **Git Tags**: Annotated tags created?
- [ ] **CI/CD Integration**: Automated deployment on tag?
- [ ] **Release Notes**: Published to GitHub Releases?
- [ ] **Rollback Plan**: Can we rollback if needed?
- [ ] **Monitoring**: Post-release monitoring in place?

---

## Related Skills
- `45-developer-experience/commit-conventions`
- `45-developer-experience/repo-automation-scripts`
