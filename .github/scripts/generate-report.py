#!/usr/bin/env python3
"""Generate HTML validation report for skill files."""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

REQUIRED_SECTIONS = ["Overview", "Best Practices"]
CODE_BLOCK_PATTERN = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)


def analyze_skill_file(filepath: Path) -> dict:
    """Analyze a single skill file and return metrics."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return {'error': str(e)}

    sections_found = []
    for section in REQUIRED_SECTIONS:
        if f"## {section}" in content or f"# {section}" in content:
            sections_found.append(section)

    code_blocks = CODE_BLOCK_PATTERN.findall(content)
    languages = [lang for lang, _ in code_blocks if lang]

    has_checklist = "- [ ]" in content or "- [x]" in content
    word_count = len(content.split())
    line_count = len(content.splitlines())

    return {
        'path': str(filepath),
        'sections_found': sections_found,
        'sections_missing': [s for s in REQUIRED_SECTIONS if s not in sections_found],
        'code_blocks': len(code_blocks),
        'languages': list(set(languages)),
        'has_checklist': has_checklist,
        'word_count': word_count,
        'line_count': line_count,
        'valid': len(sections_found) == len(REQUIRED_SECTIONS) and len(code_blocks) > 0,
    }


def generate_html_report(results: list[dict]) -> str:
    """Generate HTML report from analysis results."""
    valid_count = sum(1 for r in results if r.get('valid', False))
    total_count = len(results)
    total_code_blocks = sum(r.get('code_blocks', 0) for r in results)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Skill Validation Report</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #007bff; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #007bff; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .valid {{ color: #28a745; }}
        .invalid {{ color: #dc3545; }}
        .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; margin: 2px; }}
        .badge-lang {{ background: #e9ecef; color: #495057; }}
        .badge-missing {{ background: #f8d7da; color: #721c24; }}
        .timestamp {{ color: #666; font-size: 0.9em; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Skill Validation Report</h1>

        <div class="summary">
            <div class="stat">
                <div class="stat-value">{total_count}</div>
                <div class="stat-label">Total Skills</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color: #28a745;">{valid_count}</div>
                <div class="stat-label">Valid Skills</div>
            </div>
            <div class="stat">
                <div class="stat-value" style="color: #dc3545;">{total_count - valid_count}</div>
                <div class="stat-label">Invalid Skills</div>
            </div>
            <div class="stat">
                <div class="stat-value">{total_code_blocks}</div>
                <div class="stat-label">Code Blocks</div>
            </div>
        </div>

        <h2>Skill Details</h2>
        <table>
            <thead>
                <tr>
                    <th>Skill Path</th>
                    <th>Status</th>
                    <th>Code Blocks</th>
                    <th>Languages</th>
                    <th>Issues</th>
                </tr>
            </thead>
            <tbody>
"""

    for result in sorted(results, key=lambda x: x.get('valid', False)):
        status_class = 'valid' if result.get('valid') else 'invalid'
        status_text = '✅ Valid' if result.get('valid') else '❌ Invalid'

        languages_html = ''.join(
            f'<span class="badge badge-lang">{lang}</span>'
            for lang in result.get('languages', [])
        ) or '<span style="color:#999">None</span>'

        issues_html = ''.join(
            f'<span class="badge badge-missing">Missing: {section}</span>'
            for section in result.get('sections_missing', [])
        )
        if not result.get('has_checklist'):
            issues_html += '<span class="badge badge-missing">No checklist</span>'
        if result.get('code_blocks', 0) == 0:
            issues_html += '<span class="badge badge-missing">No code examples</span>'

        html += f"""
                <tr>
                    <td>{result.get('path', 'Unknown')}</td>
                    <td class="{status_class}">{status_text}</td>
                    <td>{result.get('code_blocks', 0)}</td>
                    <td>{languages_html}</td>
                    <td>{issues_html or '<span class="valid">None</span>'}</td>
                </tr>
"""

    html += f"""
            </tbody>
        </table>

        <p class="timestamp">Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}</p>
    </div>
</body>
</html>
"""
    return html


def main():
    """Main function to generate validation report."""
    skill_files = list(Path('.').rglob('SKILL.md'))

    if not skill_files:
        print("No SKILL.md files found")
        sys.exit(0)

    results = []
    for filepath in skill_files:
        result = analyze_skill_file(filepath)
        results.append(result)

    html_report = generate_html_report(results)

    with open('validation-report.html', 'w', encoding='utf-8') as f:
        f.write(html_report)

    print(f"✅ Generated validation report for {len(results)} skill files")
    print("   Output: validation-report.html")


if __name__ == "__main__":
    main()
