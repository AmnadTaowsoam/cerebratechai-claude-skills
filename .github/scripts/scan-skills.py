#!/usr/bin/env python3
"""Scan repository for skill files and output JSON manifest."""

import json
import re
import sys
from pathlib import Path

TITLE_PATTERN = re.compile(r'^#\s+(.+)$', re.MULTILINE)
CATEGORY_PATTERN = re.compile(r'^(\d+)-([^/]+)')


def extract_title(content: str) -> str:
    """Extract the first H1 title from markdown content."""
    match = TITLE_PATTERN.search(content)
    return match.group(1).strip() if match else "Untitled"


def get_category_info(filepath: Path) -> dict:
    """Extract category information from file path."""
    parts = filepath.parts

    for part in parts:
        match = CATEGORY_PATTERN.match(part)
        if match:
            return {
                'number': int(match.group(1)),
                'slug': match.group(2),
                'name': match.group(2).replace('-', ' ').title()
            }

    return {'number': 0, 'slug': 'uncategorized', 'name': 'Uncategorized'}


def scan_skill_file(filepath: Path) -> dict:
    """Scan a single skill file and extract metadata."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return {'error': str(e), 'path': str(filepath)}

    category = get_category_info(filepath)
    skill_name = filepath.parent.name

    return {
        'path': str(filepath),
        'title': extract_title(content),
        'skill_name': skill_name,
        'category': category,
        'has_overview': '## Overview' in content or '# Overview' in content,
        'has_best_practices': '## Best Practices' in content or '# Best Practices' in content,
        'has_code_examples': '```' in content,
        'word_count': len(content.split()),
    }


def main():
    """Main function to scan all skill files."""
    skill_files = list(Path('.').rglob('SKILL.md'))

    if not skill_files:
        print(json.dumps({'skills': [], 'total': 0}))
        sys.exit(0)

    skills = []
    categories = {}

    for filepath in skill_files:
        skill_info = scan_skill_file(filepath)
        skills.append(skill_info)

        cat_slug = skill_info.get('category', {}).get('slug', 'uncategorized')
        if cat_slug not in categories:
            categories[cat_slug] = {
                'info': skill_info.get('category', {}),
                'count': 0
            }
        categories[cat_slug]['count'] += 1

    skills.sort(key=lambda x: (
        x.get('category', {}).get('number', 0),
        x.get('skill_name', '')
    ))

    output = {
        'skills': skills,
        'total': len(skills),
        'categories': [
            {**cat['info'], 'skill_count': cat['count']}
            for cat in sorted(categories.values(), key=lambda x: x['info'].get('number', 0))
        ],
        'statistics': {
            'total_skills': len(skills),
            'total_categories': len(categories),
            'with_overview': sum(1 for s in skills if s.get('has_overview')),
            'with_best_practices': sum(1 for s in skills if s.get('has_best_practices')),
            'with_code_examples': sum(1 for s in skills if s.get('has_code_examples')),
        }
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
