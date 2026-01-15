#!/usr/bin/env python3
"""Update README.md with current skill inventory."""

import json
import re
import sys
from pathlib import Path

SKILLS_SECTION_START = "<!-- SKILLS-START -->"
SKILLS_SECTION_END = "<!-- SKILLS-END -->"


def load_skills_manifest() -> dict:
    """Load skills manifest from scan output."""
    manifest_path = Path('skills.json')
    if manifest_path.exists():
        return json.loads(manifest_path.read_text(encoding='utf-8'))

    from scan_skills import main as scan_main
    import io
    from contextlib import redirect_stdout

    f = io.StringIO()
    with redirect_stdout(f):
        try:
            scan_main()
        except SystemExit:
            pass
    return json.loads(f.getvalue())


def generate_skills_table(manifest: dict) -> str:
    """Generate markdown table of skills organized by category."""
    lines = []

    lines.append(f"## Skills Overview\n")
    lines.append(f"**Total Skills:** {manifest.get('total', 0)}\n")

    categories = {}
    for skill in manifest.get('skills', []):
        cat = skill.get('category', {})
        cat_key = f"{cat.get('number', 0):02d}-{cat.get('slug', 'other')}"
        if cat_key not in categories:
            categories[cat_key] = {
                'name': cat.get('name', 'Other'),
                'number': cat.get('number', 0),
                'skills': []
            }
        categories[cat_key]['skills'].append(skill)

    for cat_key in sorted(categories.keys()):
        cat = categories[cat_key]
        lines.append(f"\n### {cat['number']:02d}. {cat['name']}\n")
        lines.append("| Skill | Description |")
        lines.append("|-------|-------------|")

        for skill in sorted(cat['skills'], key=lambda x: x.get('skill_name', '')):
            skill_name = skill.get('skill_name', 'Unknown')
            title = skill.get('title', skill_name)
            path = skill.get('path', '')
            path_link = path.replace('\\', '/')

            lines.append(f"| [{skill_name}]({path_link}) | {title} |")

    return '\n'.join(lines)


def update_readme(skills_content: str):
    """Update README.md with new skills content."""
    readme_path = Path('README.md')

    if not readme_path.exists():
        print("README.md not found, creating new file")
        readme_path.write_text(f"""# Claude Skills Collection

{SKILLS_SECTION_START}
{skills_content}
{SKILLS_SECTION_END}
""", encoding='utf-8')
        return

    content = readme_path.read_text(encoding='utf-8')

    pattern = re.compile(
        f"{re.escape(SKILLS_SECTION_START)}.*?{re.escape(SKILLS_SECTION_END)}",
        re.DOTALL
    )

    new_section = f"{SKILLS_SECTION_START}\n{skills_content}\n{SKILLS_SECTION_END}"

    if pattern.search(content):
        new_content = pattern.sub(new_section, content)
    else:
        new_content = content + f"\n\n{new_section}\n"

    readme_path.write_text(new_content, encoding='utf-8')


def main():
    """Main function to update README."""
    try:
        manifest = load_skills_manifest()
    except Exception as e:
        print(f"Error loading skills manifest: {e}", file=sys.stderr)
        sys.exit(1)

    skills_content = generate_skills_table(manifest)
    update_readme(skills_content)

    total = manifest.get('total', 0)
    print(f"✅ Updated README.md with {total} skills")


if __name__ == "__main__":
    main()
