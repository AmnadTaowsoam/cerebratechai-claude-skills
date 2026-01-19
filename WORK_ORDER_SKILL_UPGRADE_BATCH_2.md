# Work Order: Skill Upgrade Batch 2 (Execution & Tooling)

**Issue Date:** 2026-01-19
**Architect**: Skill Architect (Skill 72)
**Assignee**: Roo Code
**Status**: Pending

## Overview
This work order focuses on upgrading the "Execution" capabilities of the agent. The goal is to improve how the agent interacts with the environment, manages tools, and handles legacy systems. These skills are critical for reducing "Runtime Errors" and "Environment Friction".

## Tasks

### 1. [P1] New Skill: Environment Diagnosis & Repair
- **Target Path**: `45-developer-experience/env-diagnosis/SKILL.md`
- **Objective**: Detailed checklist and auto-fix scripts for dev environments.
- **Key Principles**:
  - "Check First": Verify Node, Python, Docker versions against `.nvmrc` or `requirements.txt`.
  - "Permission Awareness": Check write access to directories.
  - "Port Conflict Resolution": Identify and kill zombie processes on required ports.

### 2. [P2] New Skill: MCP Tool Creation Patterns
- **Target Path**: `54-agentops/tool-creation-patterns/SKILL.md`
- **Objective**: Teach the agent how to build *new* tools (scripts) for itself.
- **Key Principles**:
  - If a task requires >50 repetitive text edits, write a script.
  - If a task requires complex calculation, write a script.
  - Scripts should be ephemeral or stored in `scripts/` if reusable.

### 3. [P3] New Skill: Legacy Migration Playbook
- **Target Path**: `59-release-engineering/legacy-migration-playbook/SKILL.md`
- **Objective**: Safe path for upgrading libraries/frameworks.
- **Key Principles**:
  - "Snapshot Testing": Lock current behavior before changing.
  - "Dependency Tree Analysis": Identify breaking changes in deps.
  - "Rollback Plan": Exactly how to undo the migration if it fails in Prod.

### 4. [P4] Update Skill: Code Commentary Standards
- **Target Path**: `21-documentation/self-documenting-code/SKILL.md` (Note: Verify if this file exists, if not create `21-documentation/code-commentary-standards/SKILL.md`)
- **Objective**: Elevate comments from "What" to "Why".
- **Key Principles**:
  - Anti-Rule: Do NOT comment obvious code (e.g., `i++ // increment i`).
  - Pro-Rule: Comment the measure of decision (e.g., `// Using Buffer here for performance on large files`).
  - "Agent-Friendly": Comments that help future AI understand the intent.

## Verification
- [ ] All new skills must follow the `skill-architect` Gold Standard structure.
- [ ] Update `SKILL_INDEX.md` after completion. 
