#!/usr/bin/env python3
"""Generate repository statistics."""

import os
import re
from pathlib import Path
from collections import defaultdict
from datetime import datetime

def count_skills():
    """Count total skills."""
    skill_files = list(Path('.').rglob('SKILL.md'))
    return len(skill_files)

def count_by_category():
    """Count skills by category."""
    categories = defaultdict(int)
    for skill_file in Path('.').rglob('SKILL.md'):
        parts = skill_file.parts
        if len(parts) >= 2:
            category = parts[0]
            categories[category] += 1
    return dict(sorted(categories.items()))

def count_lines_of_code():
    """Count lines in all SKILL.md files."""
    total_lines = 0
    for skill_file in Path('.').rglob('SKILL.md'):
        with open(skill_file, 'r', encoding='utf-8') as f:
            total_lines += len(f.readlines())
    return total_lines

def count_code_examples():
    """Count code examples."""
    total_examples = 0
    for skill_file in Path('.').rglob('SKILL.md'):
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
            total_examples += content.count('```')
    return total_examples // 2  # Divide by 2 (opening and closing)

def main():
    """Generate and print statistics."""
    total_skills = count_skills()
    categories = count_by_category()
    total_lines = count_lines_of_code()
    total_examples = count_code_examples()
    
    print(f"# 📊 Cerebrate Chai Skills Repository Statistics")
    print(f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n## Overall Statistics")
    print(f"\n- **Total Skills**: {total_skills}")
    print(f"- **Total Lines**: {total_lines:,}")
    print(f"- **Code Examples**: {total_examples:,}")
    print(f"- **Categories**: {len(categories)}")
    print(f"\n## Skills by Category")
    print("\n| Category | Count |")
    print("|----------|-------|")
    for category, count in categories.items():
        category_name = category.split('-', 1)[1] if '-' in category else category
        print(f"| {category_name.replace('-', ' ').title()} | {count} |")
    print(f"\n---")
    print(f"\n*This report is generated automatically every week.*")

if __name__ == "__main__":
    main()