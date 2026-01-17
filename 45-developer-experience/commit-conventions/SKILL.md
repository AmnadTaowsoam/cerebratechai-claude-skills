---
name: Commit Conventions
description: Standardized commit message formats and conventions for clear, searchable, and automated-friendly version control history.
---

# Commit Conventions

## Overview

Commit conventions establish a standard format for commit messages, enabling automated changelog generation, semantic versioning, and clear project history.

**Core Principle**: "Commits are documentation. Make them readable, searchable, and meaningful."

---

## 1. Conventional Commits Standard

Format: `<type>(<scope>): <subject>`

```
feat(auth): add OAuth2 login support
fix(api): resolve race condition in user creation
docs(readme): update installation instructions
```

### Commit Types
| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(payments): add Stripe integration` |
| `fix` | Bug fix | `fix(cart): prevent negative quantities` |
| `docs` | Documentation only | `docs(api): add endpoint examples` |
| `style` | Code style (formatting, no logic change) | `style: fix indentation` |
| `refactor` | Code restructuring | `refactor(db): extract query builder` |
| `perf` | Performance improvement | `perf(search): add index to user table` |
| `test` | Add/update tests | `test(auth): add login flow tests` |
| `chore` | Build/tooling changes | `chore: update dependencies` |
| `ci` | CI/CD changes | `ci: add deployment workflow` |

---

## 2. Commit Message Structure

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Example
```
feat(user-profile): add avatar upload functionality

Users can now upload profile pictures up to 5MB.
Images are automatically resized and optimized.

Closes #123
BREAKING CHANGE: User API now requires multipart/form-data for profile updates
```

---

## 3. Commitlint Configuration

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'chore', 'ci']
    ],
    'subject-case': [2, 'never', ['upper-case']],
    'subject-max-length': [2, 'always', 72],
    'body-max-line-length': [2, 'always', 100]
  }
};
```

---

## 4. Husky Integration

```json
// package.json
{
  "scripts": {
    "prepare": "husky install"
  },
  "devDependencies": {
    "@commitlint/cli": "^17.0.0",
    "@commitlint/config-conventional": "^17.0.0",
    "husky": "^8.0.0"
  }
}
```

```bash
# .husky/commit-msg
#!/bin/sh
npx --no -- commitlint --edit $1
```

---

## 5. Semantic Versioning Integration

Commits drive version bumps:
- `feat:` → Minor version (1.0.0 → 1.1.0)
- `fix:` → Patch version (1.0.0 → 1.0.1)
- `BREAKING CHANGE:` → Major version (1.0.0 → 2.0.0)

---

## 6. Automated Changelog Generation

```bash
# Using standard-version
npx standard-version

# Generates CHANGELOG.md
## [1.2.0] - 2024-01-15
### Features
- **auth**: add OAuth2 login support (#123)
- **payments**: integrate Stripe (#124)

### Bug Fixes
- **cart**: prevent negative quantities (#125)
```

---

## 7. Commit Message Best Practices

### Good Commits
```
✅ feat(api): add user search endpoint
✅ fix(auth): resolve token expiration bug
✅ docs: update API documentation
```

### Bad Commits
```
❌ update stuff
❌ fix bug
❌ WIP
❌ asdfasdf
```

---

## 8. Commit Conventions Checklist

- [ ] **Format Enforced**: Commitlint configured and running?
- [ ] **Types Defined**: Team agrees on commit types?
- [ ] **Scope Guidelines**: Scopes documented?
- [ ] **Automated Checks**: Pre-commit hook validates messages?
- [ ] **Changelog**: Automated changelog generation set up?
- [ ] **Documentation**: Convention documented for team?

---

## Related Skills
- `45-developer-experience/release-workflow`
- `45-developer-experience/lint-format-typecheck`
