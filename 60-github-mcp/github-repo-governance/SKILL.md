---
name: github-repo-governance
description: "Configure and audit GitHub repository governance via GitHub MCP: branch protection, rulesets, CODEOWNERS, permissions, and repository settings to enforce engineering policy."
---

# GitHub Repo Governance

## Required inputs
- Identify `owner`, `repo`, and target branches or rulesets.
- Confirm governance policy (required checks, approvals, admin bypass).

## Preflight
- Confirm GitHub MCP auth can read repo settings and manage rulesets.
- Identify existing branch protections and rules to avoid conflicts.
- Align on approval rules and admin bypass policy before changes.
- Review `references/mcp-policy-checklist.md` for approval and access rules.

## Workflow
1. Read current repository settings and rulesets.
2. Review branch protection settings and required checks.
3. Validate CODEOWNERS and team permissions.
4. Propose changes with minimal diffs and clear rationale.
5. Apply updates only with explicit approval.

## MCP call patterns
- Use repo settings and rulesets APIs to read current policy.
- Use file read for CODEOWNERS and workflow definitions.
- Use permission endpoints to validate team access levels.
- For endpoint hints and inputs, read `references/mcp-calls.md`.

## Output
- Provide a governance report: current state -> gaps -> proposed changes.

## Guardrails
- Do not modify permissions or branch protections without approval.
- Prefer incremental changes to avoid blocking development.
