---
name: github-release-management
description: Manage GitHub releases via GitHub MCP: create tags and releases, draft release notes, validate artifacts, and coordinate changelog updates.
---

# GitHub Release Management

## Required inputs
- Identify `owner`, `repo`, and target version/tag.
- Confirm release type (draft, prerelease, or stable) and changelog source.

## Preflight
- Confirm GitHub MCP auth can create tags and releases.
- Identify the previous release tag to compute changes.
- Verify required artifacts or assets expectations for the repo.
- Review `references/mcp-policy-checklist.md` for approval and access rules.

## Workflow
1. Gather merged PRs and commits since the last release.
2. Draft release notes grouped by feature, fix, and breaking change.
3. Create or update the tag and release entry.
4. Validate required artifacts or assets if the repo expects them.
5. Post release summary and next steps.

## MCP call patterns
- Use compare endpoints to collect commits between tags.
- Use release create/update endpoints with notes and assets.
- Use repository files for changelog updates when requested.
- For endpoint hints and inputs, read `references/mcp-calls.md`.

## Output
- Provide the release notes and a checklist of completed actions.

## Guardrails
- Do not publish a release without explicit confirmation.
- Highlight potential breaking changes prominently.
