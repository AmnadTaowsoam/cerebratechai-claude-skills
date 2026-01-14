#!/bin/bash
# Validate all skills

set -e

echo "🔍 Validating all skills..."

# Run markdown linting
echo "Checking markdown syntax..."
markdownlint '**/*.md' --ignore node_modules --ignore .github

# Check for broken links
echo "Checking for broken links..."
find . -name "*.md" -not -path "./node_modules/*" | \
  xargs markdown-link-check --config .github/markdown-link-check.json

# Validate skill structure
echo "Validating skill structure..."
python .github/scripts/validate-skill-structure.py

# Check code examples
echo "Validating code examples..."
python .github/scripts/validate-code-examples.py

echo "✅ All validations passed!"