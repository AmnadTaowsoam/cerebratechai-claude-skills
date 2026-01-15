#!/usr/bin/env python3
"""Generate changelog from git history."""

import re
import subprocess
import sys
from datetime import datetime


def get_git_tags() -> list[str]:
    """Get list of git tags sorted by date."""
    result = subprocess.run(
        ['git', 'tag', '--sort=-creatordate'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return []
    return [tag.strip() for tag in result.stdout.strip().split('\n') if tag.strip()]


def get_commits_between(from_ref: str, to_ref: str) -> list[dict]:
    """Get commits between two refs."""
    range_spec = f"{from_ref}..{to_ref}" if from_ref else to_ref

    result = subprocess.run(
        ['git', 'log', range_spec, '--pretty=format:%H|%s|%an|%ad', '--date=short'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return []

    commits = []
    for line in result.stdout.strip().split('\n'):
        if not line:
            continue
        parts = line.split('|', 3)
        if len(parts) >= 4:
            commits.append({
                'hash': parts[0][:7],
                'message': parts[1],
                'author': parts[2],
                'date': parts[3]
            })
    return commits


def categorize_commit(message: str) -> str:
    """Categorize commit by conventional commit type."""
    message_lower = message.lower()

    if message_lower.startswith('feat') or 'add' in message_lower:
        return 'Features'
    elif message_lower.startswith('fix'):
        return 'Bug Fixes'
    elif message_lower.startswith('docs'):
        return 'Documentation'
    elif message_lower.startswith('refactor'):
        return 'Refactoring'
    elif message_lower.startswith('test'):
        return 'Tests'
    elif message_lower.startswith('chore') or message_lower.startswith('ci'):
        return 'Maintenance'
    else:
        return 'Other Changes'


def generate_changelog() -> str:
    """Generate changelog markdown."""
    tags = get_git_tags()
    lines = []

    lines.append("# Changelog\n")
    lines.append("All notable changes to this project will be documented in this file.\n")

    if not tags:
        commits = get_commits_between('', 'HEAD')
        if commits:
            lines.append(f"\n## Unreleased\n")
            categorized = {}
            for commit in commits[:50]:
                category = categorize_commit(commit['message'])
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append(commit)

            for category in ['Features', 'Bug Fixes', 'Documentation', 'Refactoring', 'Tests', 'Maintenance', 'Other Changes']:
                if category in categorized:
                    lines.append(f"\n### {category}\n")
                    for commit in categorized[category]:
                        lines.append(f"- {commit['message']} ({commit['hash']})")
    else:
        for i, tag in enumerate(tags[:5]):
            from_tag = tags[i + 1] if i + 1 < len(tags) else ''
            commits = get_commits_between(from_tag, tag)

            if commits:
                lines.append(f"\n## [{tag}] - {commits[0]['date']}\n")

                categorized = {}
                for commit in commits:
                    category = categorize_commit(commit['message'])
                    if category not in categorized:
                        categorized[category] = []
                    categorized[category].append(commit)

                for category in ['Features', 'Bug Fixes', 'Documentation', 'Refactoring', 'Tests', 'Maintenance', 'Other Changes']:
                    if category in categorized:
                        lines.append(f"\n### {category}\n")
                        for commit in categorized[category]:
                            lines.append(f"- {commit['message']} ({commit['hash']})")

    return '\n'.join(lines)


def main():
    """Main function to generate changelog."""
    changelog = generate_changelog()
    print(changelog)

    with open('CHANGELOG.md', 'w', encoding='utf-8') as f:
        f.write(changelog)


if __name__ == "__main__":
    main()
