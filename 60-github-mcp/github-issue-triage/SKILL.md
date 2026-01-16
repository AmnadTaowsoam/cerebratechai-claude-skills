---
name: github-issue-triage
description: "Triage GitHub issues via GitHub MCP: label, assign, detect duplicates, request repro info, prioritize severity, and close or route issues with clear rationale."
---

# GitHub Issue Triage

## Required inputs
- Identify `owner`, `repo`, and issue numbers or query filters.
- Clarify triage goals (bug vs feature, SLA, component ownership).

## Preflight
- Confirm GitHub MCP auth can read and update issues.
- Discover existing labels and priorities to avoid inventing new taxonomy.
- If duplicates are expected, align on duplicate handling policy.
- Review `references/mcp-policy-checklist.md` for approval and access rules.

## Workflow
1. List issues by the requested filters (label, state, author, milestone).
2. For each issue, read title, body, and recent comments.
3. Detect duplicates by comparing symptoms, stack traces, and versions.
4. Apply labels for type, severity, component, and status.
5. Assign owners or request information if repro steps are missing.
6. Close with rationale when confirmed duplicate or out of scope.

## MCP call patterns
- Use issue search for keywords and error messages.
- Use label operations to standardize triage taxonomy.
- Add comments with an explicit request checklist when info is missing.
- For endpoint hints and inputs, read `references/mcp-calls.md`.

## Output
- Provide a triage summary: issue -> action -> reason -> next step.

## Guardrails
- Do not close issues without a clear policy or explicit instruction.
- Prefer minimal label changes that align with existing repo taxonomy.
