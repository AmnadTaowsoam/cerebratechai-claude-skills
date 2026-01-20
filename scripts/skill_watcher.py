import os
import re
import json
import time
import argparse
from pathlib import Path

# Configuration
SKILL_INDEX_PATH = Path('..') / 'SKILL_INDEX.md'
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', '.env', 'dist', 'build', '.next'}
IGNORE_FILES = {'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml'}

# Heuristic Mapping (Library -> Skill Category/Name)
# In a real agent, this would be learned or queried from an LLM.
LIB_MAPPING = {
    'react': 'react-best-practices',
    'next': 'nextjs-patterns',
    'express': 'express-rest',
    'fastapi': 'fastapi-patterns',
    'prisma': 'prisma-guide',
    'mongoose': 'mongodb-patterns',
    'sequelize': 'database-migration',
    'redux': 'state-management',
    'zustand': 'state-management',
    'tailwindcss': 'tailwind-patterns',
    'jest': 'jest-patterns',
    'pytest': 'pytest-patterns',
    'docker': 'docker-patterns',
    'kubernetes': 'kubernetes-deployment',
    'terraform': 'terraform-infrastructure',
    'stripe': 'stripe-integration',
    'firebase': 'firebase-integration', # Hypothetical
    'socket.io': 'websocket-patterns',
    'kafka': 'kafka-streams',
    'rabbitmq': 'rabbitmq-patterns',
    'pydantic': 'python-standards',
    'pandas': 'data-preprocessing',
    'numpy': 'data-preprocessing',
    'pytorch': 'pytorch-deployment',
    'tensorflow': 'model-training',
    'openai': 'llm-integration',
    'langchain': 'ai-agents',
}

class SkillWatcher:
    def __init__(self, target_dir):
        self.target_dir = Path(target_dir).resolve()
        self.root_dir = Path(__file__).parent.parent.resolve()
        self.skill_index_file = self.root_dir / 'SKILL_INDEX.md'
        self.known_skills = set()
        self.load_known_skills()

    def load_known_skills(self):
        """Parse SKILL_INDEX.md to find all registered skills."""
        if not self.skill_index_file.exists():
            print(f"Warning: SKILL_INDEX.md not found at {self.skill_index_file}")
            return
        
        with open(self.skill_index_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # Extract links like [skill-name](...)
            skills = re.findall(r'\[([\w-]+)\]\(', content)
            self.known_skills = set(skills)
        print(f"Loaded {len(self.known_skills)} known skills.")

    def scan_dependencies(self):
        """Scan package files for dependencies."""
        dependencies = set()
        
        # Node.js
        pkg_json = self.target_dir / 'package.json'
        if pkg_json.exists():
            try:
                with open(pkg_json, 'r') as f:
                    data = json.load(f)
                    dependencies.update(data.get('dependencies', {}).keys())
                    dependencies.update(data.get('devDependencies', {}).keys())
            except Exception as e:
                print(f"Error reading package.json: {e}")

        # Python
        req_txt = self.target_dir / 'requirements.txt'
        if req_txt.exists():
            with open(req_txt, 'r') as f:
                for line in f:
                    line = line.strip().split('==')[0].split('>=')[0]
                    if line and not line.startswith('#'):
                        dependencies.add(line.lower())
        
        # Python (pyproject.toml) - simple regex scan
        pyproject = self.target_dir / 'pyproject.toml'
        if pyproject.exists():
             with open(pyproject, 'r') as f:
                content = f.read()
                # Very basic match for poetry/lists
                deps = re.findall(r'^\s*([\w-]+)\s*=', content, re.MULTILINE)
                dependencies.update(deps)

        return dependencies

    def analyze_gaps(self):
        print(f"Scanning {self.target_dir}...")
        dependencies = self.scan_dependencies()
        
        gaps = []
        covered = []

        for lib in dependencies:
            # Check if we have a mapping
            mapped_skill = LIB_MAPPING.get(lib)
            if mapped_skill:
                if mapped_skill in self.known_skills:
                    covered.append((lib, mapped_skill))
                else:
                    gaps.append((lib, f"Mapped to '{mapped_skill}' but skill not found in Index"))
            else:
                # No mapping, check if library name matches any skill significantly?
                # For now, flag as 'Unknown'
                # Filter out obvious ones to reduce noise?
                if lib not in ['react-dom', 'react-scripts']: # Noise filter
                     # Check if fuzzy match?
                     if lib in self.known_skills:
                         covered.append((lib, lib))
                     else:
                         gaps.append((lib, "No specific skill mapped"))

        return gaps, covered

    def generate_report(self, gaps, covered):
        report_path = self.target_dir / 'GAP_REPORT.md'
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Skill Gap Analysis Report\n\n")
            f.write(f"**Target:** `{self.target_dir}`\n")
            f.write(f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 🔴 Potential Skill Gaps\n")
            f.write("The following libraries/technologies were found but may lack comprehensive documentation/skills:\n\n")
            if gaps:
                f.write("| Library | Issue/Gap |\n")
                f.write("|---|---|\n")
                for lib, issue in sorted(gaps):
                    f.write(f"| `{lib}` | {issue} |\n")
            else:
                f.write("✅ No obvious gaps detected.\n")
            
            f.write("\n## 🟢 Covered Skills\n")
            f.write("The following technologies are supported by existing skills:\n\n")
            if covered:
                f.write("| Library | Matched Skill |\n")
                f.write("|---|---|\n")
                for lib, skill in sorted(covered):
                    f.write(f"| `{lib}` | `[{skill}]` |\n")
            else:
                f.write("No dependencies found matching known skills.\n")
            
            f.write("\n---\n*Run verify logic regularly to keep this up to date.*")
        
        print(f"Report generated at: {report_path}")

def main():
    parser = argparse.ArgumentParser(description='Analyze Codebase for Skill Gaps')
    parser.add_argument('--target', type=str, default='.', help='Directory to scan')
    parser.add_argument('--watch', action='store_true', help='Continuous watch mode')
    args = parser.parse_args()

    watcher = SkillWatcher(args.target)
    
    if args.watch:
        print(f"Watching {args.target} for changes... (Ctrl+C to stop)")
        last_mtime = 0
        while True:
            # Simple polling for file changes
            # (Just checking package.json/requirements.txt mod time for efficiency)
            changed = False
            for f in ['package.json', 'requirements.txt', 'pyproject.toml']:
                p = watcher.target_dir / f
                if p.exists():
                    mtime = p.stat().st_mtime
                    if mtime > last_mtime:
                        last_mtime = mtime
                        changed = True
            
            if changed or last_mtime == 0:
                gaps, covered = watcher.analyze_gaps()
                watcher.generate_report(gaps, covered)
                if last_mtime == 0:
                     last_mtime = time.time() # Set initial checks
            
            time.sleep(10)
    else:
        gaps, covered = watcher.analyze_gaps()
        watcher.generate_report(gaps, covered)

if __name__ == '__main__':
    main()
