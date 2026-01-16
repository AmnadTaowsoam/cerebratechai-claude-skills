---
name: github-security-triage
description: Triage GitHub security alerts via GitHub MCP: assess severity, validate exposure, coordinate fixes, and close Dependabot/CodeQL/secret scanning alerts with documented rationale.
---

# GitHub Security Triage

## Required inputs
- Identify `owner`, `repo`, alert type, and alert identifiers.
- Confirm severity policy and remediation SLA.

## Preflight
- Confirm GitHub MCP auth can read security alerts and create tracking issues.
- Identify which alert types are in scope (Dependabot, CodeQL, secret scanning).
- Align on escalation policy for critical or secret exposure.
- Review `references/mcp-policy-checklist.md` for approval and access rules.

## Workflow
1. List open alerts by type and severity.
2. Read each alert details, affected versions, and suggested fixes.
3. Determine exploitability and exposure in the repo.
4. Create or update issues/PRs for remediation.
5. Close alerts only with a clear documented reason.

## MCP call patterns
- Use alert list/detail endpoints to gather context.
- Use dependency graphs or manifest files to verify versions.
- Use issue/PR creation for fix tracking when needed.
- For endpoint hints and inputs, read `references/mcp-calls.md`.

## Output
- Provide a security summary: alert -> risk -> action -> owner.

## Guardrails
- Do not dismiss alerts without a clear policy or justification.
- Escalate when secrets or critical vulnerabilities are detected.
