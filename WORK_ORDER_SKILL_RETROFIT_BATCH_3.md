# Work Order: Skill Retrofit & Audit Batch 3 (Legacy Update)

**Issue Date:** 2026-01-19
**Architect**: Skill Architect (Skill 72)
**Assignee**: Roo Code
**Status**: Pending

## Overview
This work order focuses on **retrofitting** existing skills (Categories 00-71) to align with the new "Gold Standard" defined in Skill 72 (`skill-architect`). Currently, legacy skills may lack structure, consistency, or cognitive cues required for high-performance agent execution.

## Audit Strategy: The "Traffic Light" System
Roo Code is tasked to audit skills and classify them:
- 🟢 **Green**: Meets Gold Standard (Structure, Clarity, Actionability).
- 🟡 **Yellow**: Usable but needs structural update (e.g., missing "Common Pitfalls").
- 🔴 **Red**: Critical issues (Outdated tech, confusing instructions, huge blobs of text).

## Tasks

### 1. [P1] Audit & Upgrade "Core Foundations" (Categories 00-04)
- **Target**: `00-meta-skills`, `01-foundations`, `02-frontend`, `03-backend-api`, `04-database`
- **Objective**: Ensure the most frequently used skills are perfect.
- **Action**:
  - Check `api-design`: Does it have clear "Core Principles"?
  - Check `react-best-practices`: Is it updated for React 18/19 patterns?
  - **Execute**: Rewrite any 🔴 Red or 🟡 Yellow skills using the Skill 72 template.

### 2. [P2] Audit & Upgrade "Ops & Security" (Categories 14, 15, 24)
- **Target**: `14-monitoring`, `15-devops`, `24-security`
- **Action**:
  - Focus on *Safety*. Do these skills have strong "Verification Gates"?
  - Ensure `secrets-management` is 100% unambiguous.

### 3. [P3] Standardization Sweep
- **Target**: All Categories
- **Action**: Ensure EVERY `SKILL.md` has:
  1. YAML Frontmatter (`name`, `description`).
  2. `# [Title]` H1 Header.
  3. `## Core Principles`.
  4. `## Step-by-Step Implementation`.
  5. `## Common Pitfalls`.

## Deliverable
- A report listing which skills were upgraded.
- Standardized `SKILL.md` files for all modified skills.

## Verification
- [ ] Randomly sample 3 upgraded skills.
- [ ] Verify they follow the `skill-architect` template EXACTLY.
