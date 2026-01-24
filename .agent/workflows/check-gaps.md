---
description: Workflow for autonomously detecting skill gaps in the current project.
---

1.  Identify the target project directory (default is current directory).
2.  Check for the existence of `package.json`, `requirements.txt`, or `pyproject.toml`.
// turbo
3.  Execute the skill watcher script:
    ```cmd
    python d:\Cerebra\cerebraSkills\scripts\skill_watcher.py --target .
    ```
4.  Read the generated `GAP_REPORT.md`.
5.  If any **🔴 Potential Skill Gaps** are found:
    - List the missing libraries to the user.
    - Offer to create new skills using the **Skill Architect** protocol.
6.  If no gaps are found, report: "✅ Documentation is healthy. No skill gaps detected."
