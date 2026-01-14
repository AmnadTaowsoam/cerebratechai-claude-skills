#!/usr/bin/env python3
"""
Complete automation script to generate all Claude skills.
Handles batch generation with progress tracking and error handling.
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
import logging
import anthropic

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('skill_generation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

@dataclass
class SkillPrompt:
    """Represents a skill prompt."""
    batch: str
    category: str
    skill_name: str
    file_path: str
    prompt: str
    priority: str = "medium"  # low, medium, high


class SkillGenerator:
    """Main class for generating skills."""
    
    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir)
        self.prompts_file = self.base_dir / "tools" / "prompts.json"
        self.state_file = self.base_dir / "tools" / "generation_state.json"
        self.generated_skills = []
        self.failed_skills = []
        self.load_state()
    
    def load_state(self):
        """Load previous generation state."""
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                self.generated_skills = state.get('generated', [])
                self.failed_skills = state.get('failed', [])
            logger.info(f"Loaded state: {len(self.generated_skills)} generated, {len(self.failed_skills)} failed")
    
    def save_state(self):
        """Save generation state."""
        state = {
            'generated': self.generated_skills,
            'failed': self.failed_skills,
            'last_updated': datetime.now().isoformat()
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)
    
    def load_prompts(self) -> List[SkillPrompt]:
        """Load all prompts from JSON file."""
        if not self.prompts_file.exists():
            logger.error(f"Prompts file not found: {self.prompts_file}")
            sys.exit(1)
        
        with open(self.prompts_file, 'r') as f:
            data = json.load(f)
        
        prompts = []
        for batch_data in data['batches']:
            for skill in batch_data['skills']:
                prompts.append(SkillPrompt(
                    batch=batch_data['batch'],
                    category=batch_data['category'],
                    skill_name=skill['name'],
                    file_path=skill['path'],
                    prompt=skill['prompt'],
                    priority=skill.get('priority', 'medium')
                ))
        
        return prompts
    
    def ensure_directory(self, file_path: str):
        """Ensure directory exists for file path."""
        directory = Path(file_path).parent
        directory.mkdir(parents=True, exist_ok=True)
    


    def generate_skill_with_claude(self, skill: SkillPrompt) -> bool:
        """Generate using Claude API."""
        try:
            # Initialize Anthropic client
            client = anthropic.Anthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY")
            )
            
            logger.info(f"Generating: {skill.skill_name}")
            
            # Ensure directory exists
            self.ensure_directory(skill.file_path)
            
            # Call Claude API
            message = client.messages.create(
                model="claude-sonnet-4-20250514",  # หรือ model อื่นที่ต้องการ
                max_tokens=8000,
                messages=[
                    {"role": "user", "content": skill.prompt}
                ]
            )
            
            # Extract content
            content = message.content[0].text
            
            # Save to file
            with open(skill.file_path, 'w') as f:
                f.write(content)
            
            logger.info(f"✓ Successfully generated: {skill.skill_name}")
            self.generated_skills.append(skill.file_path)
            self.save_state()
            return True
        
        except Exception as e:
            logger.error(f"✗ Failed: {str(e)}")
            self.failed_skills.append(skill.file_path)
            self.save_state()
            return False
    
    def generate_batch(self, batch_number: str, prompts: List[SkillPrompt], delay: int = 5):
        """Generate all skills in a batch."""
        batch_prompts = [p for p in prompts if p.batch == batch_number]
        
        if not batch_prompts:
            logger.warning(f"No prompts found for batch {batch_number}")
            return
        
        logger.info(f"\n{'='*70}")
        logger.info(f"Starting Batch {batch_number}: {batch_prompts[0].category}")
        logger.info(f"Total skills: {len(batch_prompts)}")
        logger.info(f"{'='*70}\n")
        
        success_count = 0
        fail_count = 0
        
        for i, skill in enumerate(batch_prompts, 1):
            # Skip if already generated
            if skill.file_path in self.generated_skills:
                logger.info(f"[{i}/{len(batch_prompts)}] Skipping (already generated): {skill.skill_name}")
                success_count += 1
                continue
            
            logger.info(f"[{i}/{len(batch_prompts)}] Processing: {skill.skill_name}")
            
            if self.generate_skill_with_claude(skill):
                success_count += 1
            else:
                fail_count += 1
            
            # Delay between requests (except for last item)
            if i < len(batch_prompts):
                logger.info(f"Waiting {delay} seconds before next skill...")
                time.sleep(delay)
        
        logger.info(f"\n{'='*70}")
        logger.info(f"Batch {batch_number} Complete!")
        logger.info(f"Success: {success_count}/{len(batch_prompts)}")
        logger.info(f"Failed: {fail_count}/{len(batch_prompts)}")
        logger.info(f"{'='*70}\n")
    
    def generate_all(self, start_batch: Optional[str] = None, end_batch: Optional[str] = None, delay: int = 5):
        """Generate all skills from start_batch to end_batch."""
        prompts = self.load_prompts()
        
        # Get unique batch numbers
        batches = sorted(set(p.batch for p in prompts))
        
        # Filter batches if start/end specified
        if start_batch:
            batches = [b for b in batches if b >= start_batch]
        if end_batch:
            batches = [b for b in batches if b <= end_batch]
        
        logger.info(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        logger.info(f"{Colors.BOLD}{Colors.HEADER}Starting Skill Generation{Colors.ENDC}")
        logger.info(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
        logger.info(f"Batches to generate: {', '.join(batches)}")
        logger.info(f"Total skills: {len([p for p in prompts if p.batch in batches])}\n")
        
        start_time = time.time()
        
        for batch in batches:
            self.generate_batch(batch, prompts, delay)
        
        elapsed_time = time.time() - start_time
        
        # Final summary
        self.print_summary(elapsed_time)
    
    def generate_priority(self, priority: str = "high", delay: int = 5):
        """Generate only high priority skills."""
        prompts = self.load_prompts()
        priority_prompts = [p for p in prompts if p.priority == priority]
        
        logger.info(f"\n{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}")
        logger.info(f"{Colors.BOLD}{Colors.HEADER}Generating {priority.upper()} Priority Skills{Colors.ENDC}")
        logger.info(f"{Colors.BOLD}{Colors.HEADER}{'='*70}{Colors.ENDC}\n")
        logger.info(f"Total skills: {len(priority_prompts)}\n")
        
        start_time = time.time()
        
        success_count = 0
        fail_count = 0
        
        for i, skill in enumerate(priority_prompts, 1):
            if skill.file_path in self.generated_skills:
                logger.info(f"[{i}/{len(priority_prompts)}] Skipping: {skill.skill_name}")
                success_count += 1
                continue
            
            logger.info(f"[{i}/{len(priority_prompts)}] Processing: {skill.skill_name}")
            
            if self.generate_skill_with_claude(skill):
                success_count += 1
            else:
                fail_count += 1
            
            if i < len(priority_prompts):
                time.sleep(delay)
        
        elapsed_time = time.time() - start_time
        self.print_summary(elapsed_time)
    
    def retry_failed(self, delay: int = 5):
        """Retry generating failed skills."""
        if not self.failed_skills:
            logger.info("No failed skills to retry.")
            return
        
        logger.info(f"\n{Colors.BOLD}{Colors.WARNING}{'='*70}{Colors.ENDC}")
        logger.info(f"{Colors.BOLD}{Colors.WARNING}Retrying Failed Skills{Colors.ENDC}")
        logger.info(f"{Colors.BOLD}{Colors.WARNING}{'='*70}{Colors.ENDC}\n")
        logger.info(f"Total failed: {len(self.failed_skills)}\n")
        
        prompts = self.load_prompts()
        failed_prompts = [p for p in prompts if p.file_path in self.failed_skills]
        
        # Clear failed list for retry
        self.failed_skills = []
        self.save_state()
        
        success_count = 0
        fail_count = 0
        
        for i, skill in enumerate(failed_prompts, 1):
            logger.info(f"[{i}/{len(failed_prompts)}] Retrying: {skill.skill_name}")
            
            if self.generate_skill_with_claude(skill):
                success_count += 1
            else:
                fail_count += 1
            
            if i < len(failed_prompts):
                time.sleep(delay)
        
        logger.info(f"\nRetry complete: {success_count} succeeded, {fail_count} failed")
    
    def print_summary(self, elapsed_time: float):
        """Print generation summary."""
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        
        logger.info(f"\n{Colors.BOLD}{Colors.OKGREEN}{'='*70}{Colors.ENDC}")
        logger.info(f"{Colors.BOLD}{Colors.OKGREEN}Generation Complete!{Colors.ENDC}")
        logger.info(f"{Colors.BOLD}{Colors.OKGREEN}{'='*70}{Colors.ENDC}\n")
        logger.info(f"Total generated: {len(self.generated_skills)}")
        logger.info(f"Total failed: {len(self.failed_skills)}")
        logger.info(f"Time elapsed: {hours}h {minutes}m {seconds}s\n")
        
        if self.failed_skills:
            logger.warning(f"{Colors.WARNING}Failed skills:{Colors.ENDC}")
            for skill in self.failed_skills:
                logger.warning(f"  • {skill}")
            logger.warning(f"\nRun with --retry to retry failed skills.")
    
    def export_report(self, output_file: str = "generation_report.html"):
        """Export generation report as HTML."""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Skill Generation Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .success {{ color: green; }}
        .failed {{ color: red; }}
        table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
    </style>
</head>
<body>
    <h1>Skill Generation Report</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <h2>Summary</h2>
    <p class="success">✓ Successfully generated: {len(self.generated_skills)}</p>
    <p class="failed">✗ Failed: {len(self.failed_skills)}</p>
    
    <h2>Generated Skills</h2>
    <table>
        <tr><th>#</th><th>Skill Path</th></tr>
        {''.join([f'<tr><td>{i+1}</td><td>{skill}</td></tr>' for i, skill in enumerate(self.generated_skills)])}
    </table>
    
    <h2>Failed Skills</h2>
    <table>
        <tr><th>#</th><th>Skill Path</th></tr>
        {''.join([f'<tr><td>{i+1}</td><td>{skill}</td></tr>' for i, skill in enumerate(self.failed_skills)])}
    </table>
</body>
</html>
        """
        
        with open(output_file, 'w') as f:
            f.write(html)
        
        logger.info(f"Report exported to: {output_file}")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Claude skills automatically')
    parser.add_argument('--batch', help='Generate specific batch (e.g., "01" or "01-05")')
    parser.add_argument('--priority', choices=['low', 'medium', 'high'], help='Generate by priority')
    parser.add_argument('--retry', action='store_true', help='Retry failed skills')
    parser.add_argument('--delay', type=int, default=5, help='Delay between requests (seconds)')
    parser.add_argument('--report', action='store_true', help='Export generation report')
    
    args = parser.parse_args()
    
    generator = SkillGenerator()
    
    try:
        if args.retry:
            generator.retry_failed(delay=args.delay)
        elif args.priority:
            generator.generate_priority(priority=args.priority, delay=args.delay)
        elif args.batch:
            if '-' in args.batch:
                start, end = args.batch.split('-')
                generator.generate_all(start_batch=start, end_batch=end, delay=args.delay)
            else:
                generator.generate_batch(args.batch, generator.load_prompts(), delay=args.delay)
        else:
            # Generate all
            generator.generate_all(delay=args.delay)
        
        if args.report:
            generator.export_report()
    
    except KeyboardInterrupt:
        logger.warning("\n\nInterrupted by user. Progress has been saved.")
        generator.save_state()
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n\nFatal error: {str(e)}")
        generator.save_state()
        sys.exit(1)


if __name__ == "__main__":
    main()