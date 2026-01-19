---
name: Task Decomposition Strategy
description: Systematic approach for breaking down complex, high-level requests into atomic, executable steps to ensure precision and prevent overwhelm.
---

# Task Decomposition Strategy

[Context: Complex user requests often fail not because of lack of capability, but lack of planning. This skill provides the mental framework to "Think before you Code", turning vague requirements into a concrete roadmap.]

## 1. Core Principles
- **Atomic Units**: Every step should be a single, verifiable action (e.g., "Create file" not "Build backend").
- **Dependency Awareness**: Identify what must exist before step X can happen.
- **Logical Flow**: Group related tasks (Scaffold -> Logic -> UI -> Polish).
- **Verification Points**: Define *how* you will know a step is done before moving to the next.

## 2. Step-by-Step Implementation

### Phase 1: Intake & Deconstruction
1. **Analyze Request**: Identify the "Definition of Done". what does the user theoretically have at the end?
2. **Identify Pillars**: Break the request into major domains (e.g., Database, API, Frontend, Ops).
3. **Draft the List**: Write out a high-level list of tasks.

### Phase 2: Refinement (The Recursive Step)
For each item in the high-level list:
1. **Is it atomic?**
   - No? -> Break it down further.
   - Yes? -> Keep it.
2. **Check Dependencies**: Does Step 3 need Step 5? Reorder.
3. **Add "Verification"**: Add a sub-step to verify the work (e.g., "Check standard output").

### Phase 3: Execution Plan Creation
Create a `PLAN.md` or keep a mental scratchpad:
1. `[ ]` **Setup**: Init environment, install deps.
2. `[ ]` **Core**: Implement the MVP logic.
3. `[ ]` **Interface**: Connect IO/UI.
4. `[ ]` **Verify**: Run tests.

## 3. Templates & Examples

### Decomposition Template
```markdown
## Master Plan: [Project Name]

### Phase 1: Foundation (Infrastructure)
- [ ] Task 1.1: [Action]
- [ ] Task 1.2: [Action] -> *Verify with [Command]*

### Phase 2: Logic (Backend/Core)
- [ ] Task 2.1: [Action]
...
```

### Prompt for Self (Internal Monologue)
> "The user wants a 'blogging app'. That is too big.
> Breakdown:
> 1. Data Model (Post, User)
> 2. API (CRUD Posts)
> 3. UI (Home, Post, Editor)
> 4. Auth (Login)
> I will start with Data Model."

## 4. Verification & Quality Gates
- [ ] Does the plan cover ALL user requirements?
- [ ] Are steps strictly sequential (no circular dependencies)?
- [ ] Is there a explicit "Verification" step for critical milestones?

## 5. Common Pitfalls
- **Don't**: Start coding without a plan for a multi-file change.
- **Don't**: Lump "Fix bugs" as a generic step; be specific.
- **Do**: Update the plan dynamically if you discover new complexity.
