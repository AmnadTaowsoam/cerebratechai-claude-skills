#!/usr/bin/env python3
"""Validate that skill files follow the required structure."""

import os
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "Overview",
    "Best Practices",
]

ERRORS = []

def validate_skill_file(filepath):
    """Validate a single skill file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for required sections
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in content and f"# {section}" not in content:
            ERRORS.append(f"{filepath}: Missing required section '{section}'")
    
    # Check for code examples
    if "```" not in content:
        ERRORS.append(f"{filepath}: No code examples found")
    
    # Check for checklist
    if "- [ ]" not in content and "- [x]" not in content:
        ERRORS.append(f"{filepath}: No checklist found")

def main():
    """Main validation function."""
    skill_files = Path('.').rglob('SKILL.md')
    
    for filepath in skill_files:
        validate_skill_file(filepath)
    
    if ERRORS:
        print("❌ Validation failed with the following errors:\n")
        for error in ERRORS:
            print(f"  • {error}")
        sys.exit(1)
    else:
        print("✅ All skill files validated successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()