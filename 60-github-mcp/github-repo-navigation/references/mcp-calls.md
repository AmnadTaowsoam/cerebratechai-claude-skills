# GitHub MCP call guide (repo navigation)

Use these as generic call patterns; adapt to the MCP schema in use.

## Common calls
- Get repository metadata (default branch, visibility)
- List repository tree at a ref
- Search code with a narrow query and path/file filters
- Read a file at a ref
- Read CODEOWNERS or ownership metadata if present

## Safety
- Prefer smallest possible tree or path scopes
- Avoid bulk file reads unless explicitly requested
