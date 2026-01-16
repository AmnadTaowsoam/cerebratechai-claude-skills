---
name: github-workflow-ops
description: "Operate GitHub Actions via GitHub MCP: inspect workflow runs, diagnose failures, fetch logs and annotations, re-run jobs, and summarize root causes."
---

# GitHub Workflow Ops

## Required inputs
- Identify `owner`, `repo`, workflow name or ID, and branch or run ID.
- Clarify time window and the failing job names if known.

## Preflight
- Confirm GitHub MCP auth can read workflows and rerun jobs if needed.
- Identify whether the workflow mutates production or deploys artifacts.
- If multiple failing runs exist, select the most recent relevant one.
- Review `references/mcp-policy-checklist.md` for approval and access rules.

## Workflow
1. List recent workflow runs and locate the failing run.
2. Inspect jobs and steps to identify the failing step.
3. Fetch logs or annotations for the failing step.
4. Determine root cause and propose a fix or rerun.
5. Rerun jobs only when safe and requested.

## MCP call patterns
- Use workflow list and run list to narrow scope.
- Use job/step logs to extract error messages.
- Post a comment or issue summary when changes are required.
- For endpoint hints and inputs, read `references/mcp-calls.md`.

## Output
- Provide a failure summary: run -> job -> step -> error -> fix.

## Guardrails
- Do not rerun workflows that mutate production without explicit approval.
- Avoid exposing secrets in summaries; redact tokens or credentials.
