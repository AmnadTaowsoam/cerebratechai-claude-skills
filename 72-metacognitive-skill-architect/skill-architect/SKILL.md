---
name: Skill Architect
description: The master skill for analyzing, designing, and standardizing the creation of new AI skills (Skill 72).
---

# Skill Architect

This skill empowers the agent to act as a **Skill Architect**, responsible for identifying skill gaps, defining the "Gold Standard" for skill documentation, and guiding the creation of high-performance agentic skills.

## 1. The Prime Object: The Perfect Skill

A perfect Skill is not just a document; it is a **programmable instruction set** for an AI agent. It must be:
- **Atomic**: Focused on a single, clear capability (e.g., "Designing an API" vs "Building Software").
- **Actionable**: Contains concrete steps, not just theory.
- **Context-Aware**: Explains *when* to use it and *why*.
- **Machine-Readable**: Formatted with clear headers and code blocks that an LLM can parse easily.

### The Gold Standard Structure

Every `SKILL.md` MUST follow this exact structure:

```markdown
---
name: [Skill Name]
description: [Brief 1-sentence description of what this skill allows the agent to do]
---

# [Skill Name]

[Context: A high-level overview of the skill. What is it? Why does it matter?]

## 1. Core Principles
- [Principle 1]: [Explanation]
- [Principle 2]: [Explanation]

## 2. Step-by-Step Implementation
[The "Meat" of the skill. Detailed, numbered steps on how to execute the task.]

### Phase 1: Preparation
1. Step 1...
2. Step 2...

### Phase 2: Execution
1. Step 1...
   - **Checklist**: [Critical item to check]

## 3. Templates & Examples
[Provide copy-pasteable templates, code snippets, or prompt patterns.]

\`\`\`language
# Example Code or Content
\`\`\`

## 4. Verification & Quality Gates
- [ ] Checklist item 1
- [ ] Checklist item 2

## 5. Common Pitfalls
- **Don't**: [Bad practice]
- **Do**: [Good practice]
```

## 2. Skill Analysis Workflow

When asked to "create a skill" or "analyze what skills are needed":

1.  **Gap Analysis**:
    - Read `SKILL_INDEX.md` to see what exists.
    - Identify the user's friction points (e.g., "I keep repeating X").
    - Propose a skill that turns that friction into a workflow.

2.  **Definition**:
    - **Name**: kebab-case (e.g., `skill-architect`).
    - **Batch**: Choose the appropriate category ID.
    - **Description**: Define the input (context) and output (result).

3.  **Drafting**:
    - Use the **Gold Standard Structure** above.
    - Focus on *Agent Instructions*: "You MUST do X", "Always check Y".

4.  **Verification**:
    - Does this skill reduce ambiguity?
    - Can a fresh agent execute this without asking clarifying questions?

## 3. Skill Creation Prompt

When generating a skill, use this internal monologue/prompt strategy:

> "I am the Skill Architect. My goal is to encode expert knowledge into a Markdown file. I must be precise. I must provide examples. I must assume the agent reading this has High Intelligence but Low Context. I will bridge that gap."

## 4. Maintenance

- **Update Index**: Always update `SKILL_INDEX.md` immediately after creating a skill.
- **Cross-Linking**: If a skill relies on another (e.g., `api-design` relies on `security-baseline`), link to it relatively.
