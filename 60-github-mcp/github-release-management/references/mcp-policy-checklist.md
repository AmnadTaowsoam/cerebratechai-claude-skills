# GitHub MCP policy checklist

Use this checklist before making write actions or sensitive reads.

## Access and scopes
- Confirm the GitHub MCP token has the minimum required scopes for the task.
- If the repo is private, verify access permissions explicitly.

## Approval gates
- Require explicit approval for actions that merge, deploy, or change permissions.
- Confirm approval before closing issues or dismissing security alerts.

## SLA and escalation
- Follow the repo's SLA for issue/alert response and remediation.
- Escalate immediately on critical severity or secret exposure.

## Logging and traceability
- Leave an auditable comment or summary for all write actions.
- Link to related issues/PRs when performing changes.
