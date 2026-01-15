#!/usr/bin/env python3
"""Validate code examples in skill files for syntax correctness."""

import re
import sys
import subprocess
import tempfile
from pathlib import Path

SUPPORTED_LANGUAGES = {
    'python': {'extension': '.py', 'validator': 'python -m py_compile'},
    'typescript': {'extension': '.ts', 'validator': None},
    'javascript': {'extension': '.js', 'validator': None},
    'json': {'extension': '.json', 'validator': 'python -m json.tool'},
    'yaml': {'extension': '.yaml', 'validator': None},
    'yml': {'extension': '.yml', 'validator': None},
    'bash': {'extension': '.sh', 'validator': 'bash -n'},
    'sh': {'extension': '.sh', 'validator': 'bash -n'},
    'sql': {'extension': '.sql', 'validator': None},
}

CODE_BLOCK_PATTERN = re.compile(r'```(\w+)?\n(.*?)```', re.DOTALL)


def extract_code_blocks(content: str) -> list[tuple[str, str]]:
    """Extract code blocks with their language from markdown content."""
    blocks = []
    for match in CODE_BLOCK_PATTERN.finditer(content):
        language = match.group(1) or 'unknown'
        code = match.group(2)
        blocks.append((language.lower(), code))
    return blocks


def validate_code_block(language: str, code: str) -> tuple[bool, str]:
    """Validate a single code block."""
    if language not in SUPPORTED_LANGUAGES:
        return True, ""

    config = SUPPORTED_LANGUAGES[language]
    validator = config.get('validator')

    if not validator:
        return True, ""

    extension = config['extension']

    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix=extension,
        delete=False,
        encoding='utf-8'
    ) as f:
        f.write(code)
        temp_path = f.name

    try:
        cmd = f"{validator} {temp_path}"
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return False, result.stderr or result.stdout
        return True, ""
    except subprocess.TimeoutExpired:
        return False, "Validation timed out"
    except Exception as e:
        return False, str(e)
    finally:
        Path(temp_path).unlink(missing_ok=True)


def validate_skill_file(filepath: Path) -> list[str]:
    """Validate all code examples in a skill file."""
    errors = []

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return [f"Could not read file: {e}"]

    code_blocks = extract_code_blocks(content)

    for i, (language, code) in enumerate(code_blocks, 1):
        if language in SUPPORTED_LANGUAGES and SUPPORTED_LANGUAGES[language].get('validator'):
            valid, error = validate_code_block(language, code)
            if not valid:
                errors.append(f"Code block #{i} ({language}): {error[:100]}")

    return errors


def main():
    """Main function to validate all skill files."""
    skill_files = list(Path('.').rglob('SKILL.md'))

    if not skill_files:
        print("No SKILL.md files found")
        sys.exit(0)

    all_errors = {}
    total_blocks = 0

    for filepath in skill_files:
        try:
            content = filepath.read_text(encoding='utf-8')
            blocks = extract_code_blocks(content)
            total_blocks += len(blocks)
        except Exception:
            pass

        errors = validate_skill_file(filepath)
        if errors:
            all_errors[str(filepath)] = errors

    if all_errors:
        print("❌ Code example validation failed:\n")
        for filepath, errors in all_errors.items():
            print(f"  {filepath}:")
            for error in errors:
                print(f"    • {error}")
        sys.exit(1)
    else:
        print(f"✅ Validated {total_blocks} code blocks in {len(skill_files)} skill files!")
        sys.exit(0)


if __name__ == "__main__":
    main()
