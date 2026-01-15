#!/usr/bin/env python3
"""Extract code examples from skill files for testing."""

import argparse
import json
import os
import re
import sys
from pathlib import Path

CODE_BLOCK_PATTERN = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)

LANGUAGE_MAP = {
    'typescript': ['typescript', 'ts', 'tsx'],
    'python': ['python', 'py'],
    'javascript': ['javascript', 'js', 'jsx'],
}


def extract_code_blocks(filepath: Path, target_language: str) -> list[dict]:
    """Extract code blocks of a specific language from a file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Warning: Could not read {filepath}: {e}", file=sys.stderr)
        return []

    blocks = []
    target_aliases = LANGUAGE_MAP.get(target_language, [target_language])

    for match in CODE_BLOCK_PATTERN.finditer(content):
        language = (match.group(1) or '').lower()
        code = match.group(2)

        if language in target_aliases:
            blocks.append({
                'source': str(filepath),
                'language': language,
                'code': code,
                'line': content[:match.start()].count('\n') + 1,
            })

    return blocks


def setup_typescript_project(output_dir: Path, examples: list[dict]):
    """Set up a TypeScript project with extracted examples."""
    output_dir.mkdir(parents=True, exist_ok=True)

    package_json = {
        "name": "skill-code-examples",
        "version": "1.0.0",
        "scripts": {
            "test": "tsc --noEmit",
            "build": "tsc"
        },
        "devDependencies": {
            "typescript": "^5.0.0",
            "@types/node": "^20.0.0"
        }
    }

    tsconfig = {
        "compilerOptions": {
            "target": "ES2022",
            "module": "commonjs",
            "strict": False,
            "esModuleInterop": True,
            "skipLibCheck": True,
            "noEmit": True,
            "allowJs": True
        },
        "include": ["**/*.ts", "**/*.tsx"]
    }

    (output_dir / 'package.json').write_text(json.dumps(package_json, indent=2))
    (output_dir / 'tsconfig.json').write_text(json.dumps(tsconfig, indent=2))

    for i, example in enumerate(examples):
        filename = f"example_{i+1}.ts"
        (output_dir / filename).write_text(example['code'])

    (output_dir / 'test-results').mkdir(exist_ok=True)


def setup_python_project(output_dir: Path, examples: list[dict]):
    """Set up a Python project with extracted examples."""
    output_dir.mkdir(parents=True, exist_ok=True)

    requirements = """pytest>=7.0.0
mypy>=1.0.0
"""
    (output_dir / 'requirements.txt').write_text(requirements)

    for i, example in enumerate(examples):
        filename = f"example_{i+1}.py"
        (output_dir / filename).write_text(example['code'])

    test_file = """import subprocess
import sys
from pathlib import Path

def test_syntax():
    \"\"\"Test that all Python examples have valid syntax.\"\"\"
    examples_dir = Path(__file__).parent
    errors = []

    for py_file in examples_dir.glob('example_*.py'):
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', str(py_file)],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            errors.append(f"{py_file.name}: {result.stderr}")

    assert not errors, f"Syntax errors found:\\n" + "\\n".join(errors)
"""
    (output_dir / 'test_examples.py').write_text(test_file)
    (output_dir / 'test-results').mkdir(exist_ok=True)


def main():
    """Main function to extract and set up code examples."""
    parser = argparse.ArgumentParser(description='Extract code examples from skill files')
    parser.add_argument('--language', required=True, choices=['typescript', 'python', 'javascript'],
                        help='Language to extract')
    parser.add_argument('--output', default='extracted-examples',
                        help='Output directory')
    args = parser.parse_args()

    skill_files = list(Path('.').rglob('SKILL.md'))

    if not skill_files:
        print("No SKILL.md files found")
        sys.exit(0)

    all_examples = []
    for filepath in skill_files:
        examples = extract_code_blocks(filepath, args.language)
        all_examples.extend(examples)

    print(f"Found {len(all_examples)} {args.language} code examples in {len(skill_files)} files")

    output_dir = Path(args.output) / args.language

    if args.language == 'typescript':
        setup_typescript_project(output_dir, all_examples)
    elif args.language == 'python':
        setup_python_project(output_dir, all_examples)

    manifest = {
        'language': args.language,
        'total_examples': len(all_examples),
        'source_files': len(skill_files),
        'examples': [
            {'source': e['source'], 'line': e['line']}
            for e in all_examples
        ]
    }
    (output_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2))

    print(f"✅ Extracted {len(all_examples)} examples to {output_dir}")


if __name__ == "__main__":
    main()
