---
name: Skill Discovery & Chaining
description: Protocols for efficiently identifying, retrieving, and combining relevant skills from the index to solve complex problems without context overload.
---

# Skill Discovery & Chaining

[Context: With a library of 70+ skills, finding the "right tool for the job" is harder than using it. This skill provides the search and integration logic to turn a static library into a dynamic toolkit.]

## 1. Core Principles
- **Just-in-Time Loading**: Never load skills "just in case". Load them only when the plan requires them.
- **Semantic Mapping**: Match user intent (e.g., "Make it safe") to skill categories (e.g., `24-security-practices`).
- **Chain of Responsibility**: Output of Skill A (e.g., `problem-framing`) becomes Input of Skill B (e.g., `task-decomposition`).
- **Index First**: Always query `SKILL_INDEX.md` before assuming a skill doesn't exist.

## 2. Step-by-Step Implementation

### Phase 1: Discovery (The Librarian Protocol)
1. **Analyze Intent**: Extract keywords from the user request (e.g., "slow query" -> `performance`, `database`).
2. **Scan Index**: Use `grep_search` or `view_file` on `SKILL_INDEX.md`.
   - query: "performance"
   - query: "database"
3. **Select Candidates**: Identify the top 1-3 most relevant skills.
   - Example matches: `47-performance-engineering/db-query-optimization`, `04-database/database-optimization`.
4. **Verify Fit**: Read the *Description* in the index table. If promising, read the `SKILL.md`.

### Phase 2: Chaining (The Integration Protocol)
1. **Define the Pipeline**:
   - Step 1: `prompt-engineering` (Refine input)
   - Step 2: `api-design` (Create spec)
   - Step 3: `secure-coding` (Review spec)
2. **Execute Sequentially**:
   - Run Step 1.
   - *Pass the output* to Step 2 context.
   - Run Step 2.
3. **Cross-Pollinate**: If Skill A says "Check X", and Skill B says "Check Y", the final output must satisfy X+Y.

## 3. Templates & Examples

### Internal Monologue for Discovery
```text
intent: "User wants to fix a slow API."
keywords: [api, slow, performance, debug]
scan_results: [profiling-node-python, db-query-optimization, caching-strategies]
selection: "I will start with 'profiling-node-python' to diagnose, then use 'caching-strategies' to fix."
```

## 4. Verification & Quality Gates
- [ ] Did I check the global index before writing custom code?
- [ ] Am I using more than 3 skills at once? (If yes, decompose the task).
- [ ] Did I verify that the chosen skill is compatible with the project stack?

## 5. Common Pitfalls
- **Don't**: Guess the skill path (e.g., `skills/coding/best-practices.md`). Always look it up.
- **Don't**: Load 10 skills into context effectively "DOS-ing" your own token limit.
- **Do**: Unload (stop strict adherence to) a skill once that phase of the task is done.
