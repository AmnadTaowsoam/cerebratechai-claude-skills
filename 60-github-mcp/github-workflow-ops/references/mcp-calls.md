# GitHub MCP call guide (workflow ops)

## Common calls
- List workflows in a repo
- List workflow runs by branch or event
- Get run jobs and steps
- Fetch logs or annotations
- Rerun jobs or workflows (when safe)

## Safety
- Avoid reruns that deploy or mutate production without approval
- Redact secrets from summaries
