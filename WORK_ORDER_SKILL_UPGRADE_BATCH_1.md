# Work Order: Skill Upgrade Batch 1 (Cognitive & Process)

**Issue Date:** 2026-01-19
**Architect**: Skill Architect (Skill 72)
**Assignee**: Roo Code
**Status**: Pending

## Overview
This work order focuses on upgrading the "Cognitive" capabilities of the agent. The goal is to improve how the agent thinks, plans, and learns before it executes. These skills are critical for reducing "Hallucinations" and improving "First-Shot Success Rate".

## Tasks

### 1. [P1] New Skill: Problem Framing & Ambiguity Resolution
- **Target Path**: `00-meta-skills/problem-framing/SKILL.md`
- **Objective**: Teach the agent to "Stop and Ask" when requirements are vague.
- **Key Principles**:
  - Detect "Lazy Prompts" (e.g., "Fix it").
  - Formulate clarifying questions (A/B testing the user's intent).
  - Restate the problem in technical terms before solving.
- **Implementation Guide**: Use the `skill-architect` template.

### 2. [P2] New Skill: Safe Refactoring Patterns
- **Target Path**: `01-foundations/refactoring-strategies/SKILL.md`
- **Objective**: Teach the agent how to modify *existing* code without breaking it.
- **Key Principles**:
  - "Strangler Fig Pattern" (create new, migrate, delete old).
  - "Parallel Change" (expand, migrate, contract).
  - Verification steps MUST be run *between* changes.
- **Implementation Guide**: Focus on "Brownfield" development safety.

### 3. [P3] New Skill: Codebase Absorption Strategy
- **Target Path**: `66-repo-navigation-knowledge-map/codebase-learning/SKILL.md`
- **Objective**: Protocol for "Reading Code" to build a mental map.
- **Key Principles**:
  - The "Outside-In" read (Entry point -> Routes -> Models).
  - Identifying "God Objects" and "Utility Bags".
  - Creating a scratchpad `CONTEXT.md` (if allowed) to store findings.

### 4. [P4] New Skill: TDD for Agents
- **Target Path**: `16-testing/test-driven-development-agentic/SKILL.md`
- **Objective**: Standardize the "Red-Green-Refactor" loop for AI.
- **Key Principles**:
  - Write the test *before* the implementation.
  - The test acts as the "Spec" for the AI itself.
  - If the test fails, do NOT change the test (unless the test is wrong); change the code.

## Verification
- [ ] All new skills must follow the `skill-architect` Gold Standard structure.
- [ ] Update `SKILL_INDEX.md` after completion. 
