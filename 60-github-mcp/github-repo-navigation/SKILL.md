---
name: github-repo-navigation
description: "Navigate GitHub repositories via GitHub MCP: locate files, search code, read directory trees, summarize repo structure, map questions to paths or owners, and fetch file contents for analysis."
---

# GitHub Repo Navigation

## Required inputs
- Identify `owner`, `repo`, and target `ref` (default to the repo default branch if not provided).
- Ask for scope if the user request is ambiguous (single file, directory, or full repo overview).

## Preflight
- Confirm GitHub MCP auth has at least read access to the repo and code search.
- Resolve the default branch if `ref` is not provided.
- If the repo is a monorepo, ask for the product or service scope.
- Review `references/mcp-policy-checklist.md` for approval and access rules.

## Workflow
1. List top-level files and directories to orient the structure.
2. Search for key terms to locate likely files (config, entrypoints, feature keywords).
3. Read files that establish architecture and ownership first (README, CODEOWNERS, package manifests).
4. Traverse into relevant directories and read focused files.
5. Summarize findings with exact paths and short rationales.

## MCP call patterns
- Use repo tree listing to identify candidates before reading full files.
- Use code search with narrow patterns (file glob, path hint, symbol name).
- Use file read sparingly and summarize per file to keep context small.
- For endpoint hints and inputs, read `references/mcp-calls.md`.

## Output
- Provide a short map: `path` -> purpose -> why it is relevant.
- Call out missing context (unknown branch, monorepo root, or generated code).

## Guardrails
- Avoid bulk-reading entire repos unless explicitly requested.
- Prefer the smallest set of files that satisfy the request.
