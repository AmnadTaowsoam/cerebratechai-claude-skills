---
name: autonomous-gap-detector
description: Protocol for agents to autonomously detect skill gaps and maintain documentation health.
---

# Autonomous Gap Detector Protocol

This protocol defines how an AI agent should autonomously manage skill gaps within a repository.

## 🤖 Agent Instructions (CRITICAL)

As an AI Agent, you are responsible for maintaining the "Documentation Health" of the project. You MUST trigger the Gap Detection process in the following scenarios:

1.  **Task Initialization:** When starting a new feature, scan for existing skills to see if you have the necessary knowledge.
2.  **Dependency Changes:** Immediately after adding or updating any library (e.g., in `package.json`, `requirements.txt`).
3.  **Task Completion (DoD Check):** Before marking any task as "Done", you must verify that no new skill gaps were introduced.

### Execution Protocol

When triggered, you must perform these steps:

1.  **Run Scanner:** Execute the diagnostic script:
    ```cmd
    python d:\Cerebra\cerebraSkills\scripts\skill_watcher.py --target .
    ```
2.  **Analyze `GAP_REPORT.md`:** 
    *   If **RED GAPS** are found: 
        *   Analyze if the library is critical for the project's long-term maintenance.
        *   If it represents a new logic pattern, use the **Skill Architect** (`72-metacognitive-skill-architect`) to draft a new skill.
        *   Ask the user if they want you to finalize the new skill now or later.
    *   If **ALL GREEN**: Proceed with the task.

3.  **Cross-Reference:** Check if the library is already in `LIB_MAPPING` in `scripts/skill_watcher.py`. If not, update the mapping to ensure future scans are accurate.

## Reporting Logic

Any gaps identified should be reported to the user in this format:
> "🚨 **Skill Gap Detected**: You are using `{library}`, but we don't have a standardized Skill for it yet. This may lead to maintenance issues. Should I draft a Skill for this now?"

---

## Technical Details

### Scanner Script
*   Location: `d:\Cerebra\cerebraSkills\scripts\skill_watcher.py`
*   Config: Edit `LIB_MAPPING` to add new technology associations.

### Logic Flow
1. Parsing project dependency files.
2. Filtering against `IGNORE_FILES` and `IGNORE_DIRS`.
3. Matching against `SKILL_INDEX.md` entries.
4. Outputting markdown report to `GAP_REPORT.md`.
