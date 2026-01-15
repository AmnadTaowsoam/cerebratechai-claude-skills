#!/usr/bin/env python3
"""Check that skill files contain required sections."""

import sys
from pathlib import Path

REQUIRED_SECTIONS = {
    "Overview": ["## Overview", "# Overview"],
    "Best Practices": ["## Best Practices", "# Best Practices"],
}

OPTIONAL_SECTIONS = [
    "Code Examples",
    "Common Patterns",
    "Troubleshooting",
    "References",
]


def check_sections(filepath: Path) -> list[str]:
    """Check a single skill file for required sections."""
    errors = []

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return [f"Could not read file: {e}"]

    for section_name, patterns in REQUIRED_SECTIONS.items():
        found = any(pattern in content for pattern in patterns)
        if not found:
            errors.append(f"Missing required section: '{section_name}'")

    return errors


def main():
    """Main function to check all skill files."""
    skill_files = list(Path('.').rglob('SKILL.md'))

    if not skill_files:
        print("No SKILL.md files found")
        sys.exit(0)

    all_errors = {}

    for filepath in skill_files:
        errors = check_sections(filepath)
        if errors:
            all_errors[str(filepath)] = errors

    if all_errors:
        print("❌ Required sections check failed:\n")
        for filepath, errors in all_errors.items():
            print(f"  {filepath}:")
            for error in errors:
                print(f"    • {error}")
        sys.exit(1)
    else:
        print(f"✅ All {len(skill_files)} skill files have required sections!")
        sys.exit(0)


if __name__ == "__main__":
    main()
