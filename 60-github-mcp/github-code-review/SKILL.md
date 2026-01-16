---
name: github-code-review
description: "Review GitHub pull requests via GitHub MCP: analyze diffs, identify risks and regressions, verify tests, and provide actionable review feedback with references to files and lines."
---

# GitHub Code Review

## Required inputs
- Identify `owner`, `repo`, and PR number.
- Confirm review depth (quick pass, full review, security-focused).

## Preflight
- Confirm GitHub MCP auth can read PRs, diffs, and post reviews.
- Identify required review standards (security, performance, compliance).
- If the diff is large, agree on a scope focus before reviewing.
- Review `references/mcp-policy-checklist.md` for approval and access rules.

## Workflow
1. Fetch PR metadata, files changed, and diff.
2. Identify high-risk areas (auth, data access, migrations, infra changes).
3. Validate correctness, edge cases, and backward compatibility.
4. Check tests: coverage, missing cases, flaky or failing tests.
5. Provide feedback with file and line references, ordered by severity.

## MCP call patterns
- Use diff APIs for file-level changes first, then drill down.
- Use file reads for context only where the diff is unclear.
- Use review comments for specific line feedback; use a summary for overall risk.
- For endpoint hints and inputs, read `references/mcp-calls.md`.

## Output
- Provide findings ordered by severity with precise references.
- Include explicit test gaps and suggested fixes.

## Guardrails
- Avoid stylistic nitpicks unless they affect correctness or maintainability.
- Do not approve if critical issues or missing tests remain.
