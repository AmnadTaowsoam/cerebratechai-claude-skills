---
name: Definition of Done
description: เกณฑ์ที่ชัดเจนว่า "งานเสร็จ" หมายความว่าอย่างไร ครอบคลุมทุก task type พร้อม checklist และ verification
---

# Definition of Done

## Overview

เกณฑ์ที่ชัดเจนว่า "งานเสร็จ" หมายความว่าอย่างไร ครอบคลุมทุก task type: feature, bug fix, refactor เพื่อให้ทุกคนมีมาตรฐานเดียวกัน

## Why This Matters

- **Clarity**: ทุกคนรู้ว่า "done" คืออะไร
- **Quality**: ไม่ปล่อย half-baked work
- **Consistency**: ทุก task มีมาตรฐานเดียวกัน
- **Accountability**: ตรวจสอบได้ว่าครบหรือไม่

---

## Universal DoD (ทุก Task)

```markdown
### Code Quality (ทุก task ต้องผ่าน)
☐ Lint passes (no errors)
☐ Type check passes (no errors)
☐ Tests pass (all existing + new)
☐ No security vulnerabilities (high/critical)

### Review
☐ Self-review completed
☐ Code review approved (≥1 reviewer)
☐ No unresolved comments

### CI/CD
☐ All CI checks pass
☐ Build succeeds
☐ No breaking changes (or documented)

### Skill Stewardship (ใหม่!)
☐ Skill Gap Analysis performed (Check `GAP_REPORT.md`)
☐ New skills drafted/updated if required
```

---

## DoD by Task Type

### Feature Development

```markdown
## DoD: New Feature

### Code
☐ Implementation complete (all acceptance criteria met)
☐ Unit tests written (≥80% coverage for new code)
☐ Integration tests for critical paths
☐ Type safety (no `any`, proper types)
☐ Error handling included
☐ Logging added for key operations

### Review
☐ Self-review completed
☐ Code review approved (≥1 reviewer)
☐ Design review (if architectural change)
☐ Security review (if handling sensitive data)

### Documentation
☐ API documentation updated (if applicable)
☐ README updated (if applicable)
☐ Changelog entry added
☐ Migration guide (if breaking change)

### Deployment
☐ Works in local environment
☐ Works in staging environment
☐ Feature flag configured (if applicable)
☐ Monitoring/alerts in place
☐ Rollback plan documented

### Communication
☐ Stakeholders notified
☐ Release notes drafted
☐ Demo prepared (if customer-facing)

### Verification
How to verify:
1. Run feature in staging
2. Test all acceptance criteria
3. Check monitoring dashboard
4. Verify no errors in logs
```

---

### Bug Fix

```markdown
## DoD: Bug Fix

### Code
☐ Bug reproduced with test (failing test first)
☐ Fix implemented
☐ Test now passes
☐ No regression introduced (all tests pass)
☐ Root cause documented (in PR or ticket)

### Review
☐ Code review approved
☐ QA verified (if applicable)
☐ Tested in staging

### Documentation
☐ Changelog entry added
☐ Known issues updated (if applicable)
☐ Incident report (if production bug)

### Deployment
☐ Fix verified in staging
☐ Production deployment planned
☐ Hotfix process followed (if critical)

### Verification
How to verify:
1. Reproduce original bug (should fail)
2. Apply fix
3. Bug no longer occurs
4. Related functionality still works
```

---

### Refactoring

```markdown
## DoD: Refactor

### Code
☐ Behavior unchanged (all tests pass)
☐ Code quality improved (measurable)
☐ No new dependencies (unless justified)
☐ Performance not degraded (benchmarks)
☐ Test coverage maintained or improved

### Review
☐ Code review approved
☐ Architecture review (if significant)
☐ Performance review (if optimization)

### Documentation
☐ Technical docs updated
☐ ADR written (if significant decision)
☐ Comments updated (if logic changed)

### Verification
How to verify:
1. All tests pass
2. No new bugs introduced
3. Performance benchmarks stable
4. Code metrics improved
```

---

### Documentation

```markdown
## DoD: Documentation

### Content
☐ Accurate and up-to-date
☐ Spell-checked
☐ Code examples tested (actually run)
☐ Links verified (no 404s)
☐ Screenshots current (if applicable)

### Review
☐ Technical review (content accuracy)
☐ Editorial review (clarity, grammar)
☐ Peer review (by target audience)

### Publishing
☐ Merged to main
☐ Visible on docs site
☐ Search indexed
☐ Old docs archived/redirected

### Verification
How to verify:
1. Read through as new user
2. Follow all examples
3. Click all links
4. Check on live docs site
```

---

## Quality Criteria Details

| Criterion | Requirement | How to Verify | Tool |
|-----------|-------------|---------------|------|
| Test Coverage | ≥80% new code | `npm run test:coverage` | Jest |
| Lint | No errors | `npm run lint` | ESLint |
| Type Check | No errors | `npm run typecheck` | TypeScript |
| Security | No high/critical | `npm audit` | npm |
| Performance | No regression | Benchmark tests | Custom |
| Bundle Size | No >10% increase | `npm run analyze` | webpack-bundle-analyzer |

---

## PR Template with DoD

```markdown
## Description
[Brief description of changes]

## Type
- [ ] Feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation
- [ ] Other: ___

## Definition of Done

### Code Quality
- [ ] Tests written and passing (≥80% coverage)
- [ ] Lint passes (no errors)
- [ ] Type check passes (no errors)
- [ ] No security issues (npm audit)
- [ ] Performance benchmarks stable

### Review
- [ ] Self-review completed
- [ ] Ready for code review
- [ ] All comments addressed

### Documentation
- [ ] Docs updated (if applicable)
- [ ] Changelog entry added
- [ ] API docs updated (if applicable)

### Deployment
- [ ] Works in local
- [ ] Works in staging
- [ ] Rollback plan exists
- [ ] Monitoring in place

### Verification
- [ ] Acceptance criteria met
- [ ] No regressions
- [ ] Skill Gap Analysis completed (No red gaps in `GAP_REPORT.md` related to this task)
- [ ] Stakeholders notified

## Testing
- [ ] Unit tests
- [ ] Integration tests
- [ ] E2E tests (if applicable)
- [ ] Manual testing completed

## Screenshots/Videos
[If UI changes]

## Additional Notes
[Any additional context]
```

---

## Automated DoD Checks

### GitHub Actions
```yaml
# .github/workflows/dod-check.yml
name: DoD Check
on: [pull_request]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Lint
        run: npm run lint
      
      - name: Type Check
        run: npm run typecheck
      
      - name: Tests
        run: npm test
      
      - name: Coverage
        run: npm run test:coverage
        # Fail if coverage < 80%
      
      - name: Security Audit
        run: npm audit --audit-level=high
      
      - name: Bundle Size
        run: npm run analyze
        # Fail if size increased >10%
```

---

## Exception Process

### When to Deviate from DoD

**Acceptable reasons:**
- Hotfix for production incident (P0)
- Experimental/spike work (clearly marked)
- External deadline with documented trade-offs
- Technical debt with approved plan

**Process:**
```markdown
1. Document why deviation needed
   - What criteria skipped?
   - Why is it necessary?
   - What's the risk?

2. Get approval
   - Tech lead approval required
   - Product owner (if affects features)
   - Security team (if security criteria skipped)

3. Create follow-up ticket
   - Link to original PR
   - List skipped criteria
   - Set deadline to complete

4. Review in retrospective
   - Was deviation justified?
   - How to prevent in future?
   - Update DoD if needed
```

**Example:**
```markdown
## DoD Exception Request

**PR:** #123
**Criteria Skipped:** Integration tests
**Reason:** Production incident, need hotfix immediately
**Risk:** May have edge cases not covered
**Mitigation:** Manual testing in staging, monitoring alerts
**Follow-up:** Ticket #456 to add integration tests
**Approved by:** @tech-lead
**Deadline:** Within 2 days
```

---

## DoD Enforcement

### Code Review Checklist
```markdown
Reviewer checklist:
☐ All DoD criteria met (or exception approved)
☐ Tests actually test the feature
☐ Documentation is clear
☐ No obvious bugs
☐ Follows team conventions
☐ No security issues
☐ Performance acceptable
```

### Automated Enforcement
```typescript
// PR validation bot
async function validatePR(pr: PullRequest) {
  const checks = {
    lint: await runLint(),
    typecheck: await runTypeCheck(),
    tests: await runTests(),
    coverage: await checkCoverage(80),
    security: await runSecurityAudit(),
  };
  
  const failed = Object.entries(checks)
    .filter(([_, passed]) => !passed)
    .map(([name]) => name);
  
  if (failed.length > 0) {
    await pr.comment(`
      ❌ DoD checks failed:
      ${failed.map(f => `- ${f}`).join('\n')}
      
      Please fix before merging.
    `);
    await pr.setStatus('failure');
  } else {
    await pr.comment('✅ All DoD checks passed!');
    await pr.setStatus('success');
  }
}
```

---

## Metrics to Track

```typescript
interface DoDMetrics {
  // Compliance
  prsWithAllCriteria: number;
  prsWithExceptions: number;
  exceptionRate: number;
  
  // Quality
  avgTestCoverage: number;
  bugEscapeRate: number;  // Bugs found in production
  reworkRate: number;     // PRs needing rework
  
  // Speed
  avgTimeToMerge: number;
  avgReviewCycles: number;
}

// Track over time
const metrics = {
  week1: { exceptionRate: 0.15, bugEscapeRate: 0.05 },
  week2: { exceptionRate: 0.10, bugEscapeRate: 0.03 },
  // Goal: exception rate < 10%, bug escape < 2%
};
```

---

## Best Practices

### 1. Make DoD Visible
```
✓ In PR template
✓ In team wiki
✓ In onboarding docs
✓ In code review guide
```

### 2. Keep It Updated
```
✓ Review quarterly
✓ Update based on incidents
✓ Team input on changes
✓ Version control DoD
```

### 3. Automate What You Can
```
✓ Lint (automated)
✓ Type check (automated)
✓ Tests (automated)
✓ Security scan (automated)
✗ Code quality (manual review)
✗ Architecture (manual review)
```

### 4. Be Pragmatic
```
✓ Allow exceptions with process
✓ Different DoD for different task types
✓ Adjust based on context
✗ Rigid, one-size-fits-all
```

---

## Summary

**Definition of Done:** เกณฑ์ชัดเจนว่า "งานเสร็จ" คืออะไร

**Universal DoD:**
- Lint + Type check pass
- Tests pass
- Code review approved
- CI checks pass

**By Task Type:**
- Feature: Tests + Docs + Staging
- Bug: Reproduce + Fix + Verify
- Refactor: Tests pass + Quality improved
- Docs: Accurate + Reviewed + Published

**Enforcement:**
- PR template
- Automated checks
- Code review
- Metrics tracking

**Exceptions:**
- Document reason
- Get approval
- Create follow-up
- Review in retro

**Goal:** 100% compliance or approved exceptions
