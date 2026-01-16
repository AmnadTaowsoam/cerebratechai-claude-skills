# Scoring and Prioritization

## Overview

Skill scoring ranks skills by relevance to a task. Prioritization determines the order in which skills should be read or applied. This ensures focus on the most important skills first, optimizing for time, cost, and quality.

## What Is Skill Scoring

Skill scoring is:

- **Ranking skills** by relevance to task
- **Must-have vs nice-to-have** categorization
- **Priority order** for reading/applying skills
- **Context-aware** - scores adjust based on project context

## Why Scoring Matters

| Benefit | Description |
|---------|-------------|
| **Focus on most important** - Read critical skills first |
| **Avoid information overload** - Don't read everything |
| **Optimize for time/cost** - Balance thoroughness with efficiency |
| **Better results** - Right skills applied at right time |
| **Adaptability** - Adjust to constraints (time, budget) |

---

## Scoring Dimensions

Multiple factors contribute to skill score.

### 1. Relevance

How applicable is the skill to the task?

| Score | Level | Description |
|-------|--------|-------------|
| **3** | High | Critical, directly addresses task |
| **2** | Medium | Important, indirectly related |
| **1** | Low | Helpful, general guidance |

### 2. Impact

How much difference will the skill make?

| Score | Level | Description |
|-------|--------|-------------|
| **2** | High | Makes significant difference to quality |
| **1** | Medium | Noticeable improvement |
| **0** | Low | Minor improvement |

### 3. Phase

When is the skill needed?

| Phase | Priority | Description |
|--------|-----------|-------------|
| **Planning** | High | Needed now to define approach |
| **Development** | High | Needed for implementation |
| **Deployment** | Medium | Needed before launch |
| **Maintenance** | Low | Needed after launch |

### 4. Complexity

How hard is it to apply the skill?

| Score | Level | Description |
|-------|--------|-------------|
| **3** | High | Complex, requires significant effort |
| **2** | Medium | Moderate effort |
| **1** | Low | Simple, straightforward |

---

## Relevance Scoring

Evaluate how directly a skill addresses the task.

### High Relevance (3)

Skill is critical to task completion.

```
Examples:
Task: "Create user authentication API"
- api-design: High (directly relevant)
- authentication-jwt: High (directly relevant)
- database-design: High (directly relevant)

Task: "Build React dashboard"
- react-patterns: High (directly relevant)
- css-patterns: High (directly relevant)
- data-visualization: High (directly relevant)
```

### Medium Relevance (2)

Skill is important but not critical.

```
Examples:
Task: "Create user authentication API"
- error-handling: Medium (important but not core)
- testing: Medium (important but not core)
- security: Medium (important but not core)

Task: "Build React dashboard"
- accessibility: Medium (important but not core)
- performance-engineering: Medium (important but not core)
```

### Low Relevance (1)

Skill is helpful but general guidance.

```
Examples:
Task: "Create user authentication API"
- git-workflow: Low (general practice)
- documentation: Low (general practice)
- code-review-standards: Low (general practice)

Task: "Build React dashboard"
- lint-format-typecheck: Low (general practice)
- monitoring: Low (general practice)
```

---

## Impact Scoring

Evaluate how much difference the skill makes.

### High Impact (2)

Skill makes significant difference to quality.

```
Examples:
- api-design: High impact on API quality
- authentication-jwt: High impact on security
- performance-engineering: High impact on performance
- accessibility: High impact on user experience
- error-handling: High impact on reliability
```

### Medium Impact (1)

Skill provides noticeable improvement.

```
Examples:
- testing: Medium impact on quality
- caching-strategies: Medium impact on performance
- documentation: Medium impact on maintainability
- monitoring: Medium impact on observability
```

### Low Impact (0)

Skill provides minor improvement.

```
Examples:
- git-workflow: Low impact on code quality
- code-review-standards: Low impact on code quality
- lint-format-typecheck: Low impact on code quality
```

---

## Phase-Based Prioritization

Prioritize skills based on project phase.

### Planning Phase

```
Priority Skills:
1. Discovery questions
2. Requirement to scope
3. Acceptance criteria
4. Constraints and assumptions
5. Risk and dependencies

Secondary Skills:
6. System thinking
7. Trade-off analysis
8. Estimation
9. Architecture decision
```

### Development Phase

```
Priority Skills:
1. Code quality
2. Testing
3. Git workflow
4. Error handling
5. Security

Secondary Skills:
6. Performance engineering
7. Documentation
8. Code review standards
9. Monitoring
```

### Deployment Phase

```
Priority Skills:
1. CI/CD
2. Deployment strategies
3. Monitoring
4. Incident management
5. Rollback strategies

Secondary Skills:
6. Health checks
7. Performance engineering
8. Security audit
9. Documentation
```

### Maintenance Phase

```
Priority Skills:
1. Debugging
2. Performance engineering
3. Refactoring
4. Testing
5. Error handling

Secondary Skills:
6. Monitoring
7. Documentation
8. Code review standards
9. Security practices
```

---

## Skill Categories

Categorize skills by priority level.

### Must-Read

Always read for this task type.

```
Example: Create API
Must-Read:
- api-design
- error-handling
- security
- database-design
```

### Should-Read

Usually helpful for this task type.

```
Example: Create API
Should-Read:
- testing
- authentication
- rate-limiting
- openapi-governance
```

### Could-Read

Sometimes helpful for this task type.

```
Example: Create API
Could-Read:
- caching-strategies
- webhooks
- graphql
- versioning
```

### Won't-Read

Not relevant for this task type.

```
Example: Create API
Won't-Read:
- mobile-development
- ux-ui-design
- marketing-integration
- customer-support
```

---

## Scoring Formula

Calculate overall skill score.

### Basic Formula

```
Score = (Relevance × 3) + (Impact × 2) + (Urgency × 1)

Higher score = Higher priority
```

### Example Calculation

```
Skill: api-design
Task: Create user authentication API

Relevance: 3 (High)
Impact: 2 (High)
Urgency: 1 (Planning phase)

Score = (3 × 3) + (2 × 2) + (1 × 1)
Score = 9 + 4 + 1
Score = 14

Priority: Must-Read
```

### Weighted Formula

Adjust weights based on context.

```
Score = (Relevance × W1) + (Impact × W2) + (Urgency × W3)

Weights:
- Time-constrained: Relevance (3), Impact (1), Urgency (2)
- Quality-focused: Relevance (2), Impact (3), Urgency (1)
- Balanced: Relevance (3), Impact (2), Urgency (1)
```

---

## Context-Aware Scoring

Adjust scores based on project context.

### Production System

Security and monitoring score higher.

```
Task: Deploy to production

Skills with boosted scores:
- security: +2
- monitoring: +2
- incident-management: +2
- rollback-strategies: +2
- health-checks: +1
```

### MVP

Core functionality scores higher, nice-to-haves lower.

```
Task: Build MVP

Skills with boosted scores:
- api-design: +2
- error-handling: +2
- testing: +1

Skills with reduced scores:
- caching-strategies: -1
- monitoring: -1
- documentation: -1
```

### Enterprise

Compliance and SSO score higher.

```
Task: Build enterprise app

Skills with boosted scores:
- sso-saml-oidc: +3
- enterprise-rbac-models: +2
- scim-provisioning: +2
- security-questionnaires: +2
- compliance: +2
```

### Time-Constrained

Essential skills only, skip nice-to-haves.

```
Task: Quick fix under tight deadline

Skills with boosted scores:
- debugging: +3
- error-handling: +2
- testing: +1

Skills with reduced scores:
- documentation: -2
- monitoring: -2
- performance-engineering: -1
```

---

## Skill Dependencies

Some skills depend on others.

### Dependency Rules

```
1. Read foundational skills first
2. Read in logical order
3. Don't skip dependencies

Example:
- Read "api-design" before "api-versioning"
- Read "authentication-jwt" before "oauth"
- Read "database-design" before "db-query-optimization"
```

### Dependency Graph

```
api-design
  ├── authentication-jwt
  ├── rate-limiting
  ├── openapi-governance
  └── api-versioning (depends on api-design)

database-design
  ├── db-query-optimization (depends on database-design)
  ├── data-quality (depends on database-design)
  └── data-migration (depends on database-design)

react-patterns
  ├── hooks-patterns (depends on react-patterns)
  ├── state-management (depends on react-patterns)
  └── testing (depends on react-patterns)
```

---

## Scoring Matrix Example

Complete example of scoring for a task.

### Task: Create User Authentication API

```
Skills                  | Relevance | Impact | Urgency | Score | Priority
----------------------|-----------|--------|---------|-------|----------
API Design            | 3 (High)  | 2 (High)| 1 (Plan)| 14    | Must
Authentication (JWT)  | 3 (High)  | 2 (High)| 1 (Plan)| 14    | Must
Database Design       | 3 (High)  | 2 (High)| 1 (Plan)| 14    | Must
Error Handling        | 3 (High)  | 2 (High)| 1 (Plan)| 14    | Must
Security              | 2 (Med)   | 2 (High)| 1 (Plan)| 11    | Must
Testing               | 2 (Med)   | 1 (Med) | 1 (Plan)| 9     | Should
Rate Limiting         | 2 (Med)   | 1 (Med) | 0 (Later)| 8     | Should
OpenAPI Docs          | 2 (Med)   | 1 (Med) | 0 (Later)| 8     | Should
Caching               | 1 (Low)   | 1 (Med) | 0 (Later)| 5     | Could
Monitoring            | 1 (Low)   | 1 (Med) | 0 (Later)| 5     | Could
Documentation          | 1 (Low)   | 0 (Low) | 0 (Later)| 3     | Could
```

### Task: Build AI Chatbot

```
Skills                  | Relevance | Impact | Urgency | Score | Priority
----------------------|-----------|--------|---------|-------|----------
RAG Evaluation         | 3 (High)  | 2 (High)| 1 (Plan)| 14    | Must
LLM Patterns           | 3 (High)  | 2 (High)| 1 (Plan)| 14    | Must
Prompt Engineering    | 3 (High)  | 2 (High)| 1 (Plan)| 14    | Must
API Design             | 3 (High)  | 2 (High)| 1 (Plan)| 14    | Must
Safety Guardrails     | 2 (Med)   | 2 (High)| 1 (Plan)| 11    | Must
Cost Optimization      | 2 (Med)   | 1 (Med) | 1 (Plan)| 9     | Should
Monitoring            | 2 (Med)   | 1 (Med) | 0 (Later)| 8     | Should
Error Handling        | 2 (Med)   | 2 (High)| 1 (Plan)| 11    | Must
React Patterns         | 2 (Med)   | 1 (Med) | 1 (Plan)| 9     | Should
Multi-Agent            | 1 (Low)   | 1 (Med) | 0 (Later)| 5     | Could
Function Calling      | 1 (Low)   | 1 (Med) | 0 (Later)| 5     | Could
```

---

## Dynamic Re-Scoring

Adjust scores as task progresses.

### Progression-Based Re-Scoring

```
Planning Phase:
- Requirements skills: High score
- Design skills: High score
- Implementation skills: Low score

Development Phase:
- Requirements skills: Low score
- Design skills: Low score
- Implementation skills: High score
- Testing skills: Medium score

Deployment Phase:
- Implementation skills: Low score
- Testing skills: Low score
- Deployment skills: High score
- Monitoring skills: High score
```

### Example: Dynamic Re-Scoring

```
Task: Create User Authentication API

Planning Phase (Week 1):
- api-design: Score 14 (Must)
- authentication-jwt: Score 14 (Must)
- database-design: Score 14 (Must)
- testing: Score 9 (Should)

Development Phase (Week 2-3):
- api-design: Score 5 (Could) - Already read
- authentication-jwt: Score 5 (Could) - Already read
- database-design: Score 5 (Could) - Already read
- testing: Score 14 (Must) - Now critical
- error-handling: Score 14 (Must) - Now critical

Deployment Phase (Week 4):
- testing: Score 5 (Could) - Already done
- error-handling: Score 5 (Could) - Already done
- ci-cd: Score 14 (Must) - Now critical
- monitoring: Score 14 (Must) - Now critical
- deployment-strategies: Score 14 (Must) - Now critical
```

---

## User-Driven Prioritization

Allow users to influence scoring.

### User Boosts

User marks skills as "critical" → boost score.

```
Example:
User marks "security" as critical for authentication API

Original Score:
- security: 11 (Must)

Boosted Score:
- security: 16 (Must) - +5 boost
```

### User Exclusions

User marks skills as "not needed" → lower score.

```
Example:
User marks "monitoring" as not needed for MVP

Original Score:
- monitoring: 8 (Should)

Reduced Score:
- monitoring: 3 (Could) - -5 reduction
```

### User Custom Weights

User adjusts scoring weights.

```
Example:
User wants to prioritize impact over relevance

Original Weights:
- Relevance: 3
- Impact: 2
- Urgency: 1

Custom Weights:
- Relevance: 2
- Impact: 3
- Urgency: 1
```

---

## Team Prioritization

Different team members value different skills.

### Frontend Developer

```
Prioritized Skills:
- react-patterns
- css-patterns
- accessibility
- performance-engineering
- testing

Less Prioritized:
- api-design
- database-design
- devops-infrastructure
```

### Backend Developer

```
Prioritized Skills:
- api-design
- database-design
- error-handling
- security
- testing

Less Prioritized:
- react-patterns
- css-patterns
- accessibility
```

### DevOps Engineer

```
Prioritized Skills:
- ci-cd
- deployment-strategies
- monitoring
- kubernetes-patterns
- terraform

Less Prioritized:
- react-patterns
- api-design
- database-design
```

---

## Scoring Automation

Use ML/heuristics to predict scores.

### Heuristic-Based Scoring

```
Rules:
1. If task contains "API" → Boost api-design by +3
2. If task contains "React" → Boost react-patterns by +3
3. If task contains "database" → Boost database-design by +3
4. If task contains "security" → Boost security by +3
5. If task contains "performance" → Boost performance-engineering by +3
```

### ML-Based Scoring

```
Training Data:
- Historical task-skill pairs
- User feedback on skill relevance
- Task completion success rates

Model:
- Learn patterns from training data
- Predict skill scores for new tasks
- Improve over time with feedback

Feedback Loop:
- User adjusts scores
- Model learns from adjustments
- Future predictions improve
```

---

## Presenting Scored Skills

Display skills in prioritized order.

### Sort by Score

```
Skills sorted by score (highest first):

1. api-design (Score: 14) ★★★ Must-Read
2. authentication-jwt (Score: 14) ★★★ Must-Read
3. database-design (Score: 14) ★★★ Must-Read
4. error-handling (Score: 14) ★★★ Must-Read
5. security (Score: 11) ★★★ Must-Read
6. testing (Score: 9) ★★ Should-Read
7. rate-limiting (Score: 8) ★★ Should-Read
8. openapi-governance (Score: 8) ★★ Should-Read
9. caching (Score: 5) ★ Could-Read
10. monitoring (Score: 5) ★ Could-Read
```

### Group by Category

```
Must-Read (Score 10+):
- api-design (14) ★★★
- authentication-jwt (14) ★★★
- database-design (14) ★★★
- error-handling (14) ★★★
- security (11) ★★★

Should-Read (Score 5-9):
- testing (9) ★★
- rate-limiting (8) ★★
- openapi-governance (8) ★★

Could-Read (Score <5):
- caching (5) ★
- monitoring (5) ★
- documentation (3) ★
```

### Visual Indicators

```
★★★ = Must-Read (Score 10+)
★★ = Should-Read (Score 5-9)
★ = Could-Read (Score <5)
```

---

## Budget-Based Prioritization

Adjust based on time/cost constraints.

### Limited Time/Cost

```
Constraint: Read only top 3-5 skills

Strategy:
- Read only Must-Read skills
- Skip Should-Read and Could-Read
- Focus on core functionality

Example:
Task: Create API (1 day deadline)
Read:
1. api-design
2. error-handling
3. security

Skip:
- testing (defer)
- rate-limiting (defer)
- openapi-governance (defer)
```

### Moderate Time/Cost

```
Constraint: Read top 5-10 skills

Strategy:
- Read Must-Read and top Should-Read
- Skip Could-Read

Example:
Task: Create API (3 days deadline)
Read:
1. api-design
2. error-handling
3. security
4. testing
5. rate-limiting
6. openapi-governance

Skip:
- caching (defer)
- monitoring (defer)
```

### Generous Time/Cost

```
Constraint: Read top 10-15 skills

Strategy:
- Read Must-Read, Should-Read, and top Could-Read
- Comprehensive coverage

Example:
Task: Create API (1 week timeline)
Read:
1. api-design
2. error-handling
3. security
4. testing
5. rate-limiting
6. openapi-governance
7. caching
8. monitoring
9. documentation
```

---

## Quality vs Speed Trade-Off

Balance thoroughness with efficiency.

### Fast (Speed-Focused)

```
Goal: Get started quickly

Strategy:
- Read top 3-5 skills
- Focus on core concepts
- Learn as you go

When to Use:
- Tight deadline
- Familiar domain
- Prototype/MVP

Trade-offs:
- Less comprehensive
- May miss edge cases
- More rework possible
```

### Balanced

```
Goal: Good balance

Strategy:
- Read top 5-10 skills
- Cover core and important secondary skills
- Reasonable coverage

When to Use:
- Standard project
- Moderate timeline
- Production system

Trade-offs:
- Good coverage
- Manageable effort
- Quality results
```

### Thorough (Quality-Focused)

```
Goal: Comprehensive coverage

Strategy:
- Read top 10-15+ skills
- Cover all relevant skills
- Deep understanding

When to Use:
- Critical system
- Long timeline
- Complex domain

Trade-offs:
- High quality
- Low risk
- More time/cost
```

---

## Real-World Scoring Examples

### Example 1: RAG Implementation

```
Task: Implement RAG system

Skills                  | Relevance | Impact | Score | Priority
----------------------|-----------|--------|-------|----------
RAG Evaluation         | 3 (High)  | 2 (High)| 14    | Must
Vector Database        | 3 (High)  | 2 (High)| 14    | Must
Prompt Engineering    | 3 (High)  | 2 (High)| 14    | Must
API Design             | 3 (High)  | 2 (High)| 14    | Must
LLM Patterns           | 2 (Med)   | 2 (High)| 11    | Must
Safety Guardrails     | 2 (Med)   | 2 (High)| 11    | Must
Cost Optimization      | 2 (Med)   | 1 (Med) | 9     | Should
Monitoring            | 2 (Med)   | 1 (Med) | 8     | Should
Error Handling        | 2 (Med)   | 2 (High)| 11    | Must
Data Quality          | 2 (Med)   | 1 (Med) | 8     | Should
```

### Example 2: Bug Fix Task

```
Task: Fix login bug

Skills                  | Relevance | Impact | Score | Priority
----------------------|-----------|--------|-------|----------
Debugging             | 3 (High)  | 2 (High)| 14    | Must
Error Handling        | 3 (High)  | 2 (High)| 14    | Must
Testing               | 2 (Med)   | 2 (High)| 11    | Must
Authentication-JWT    | 2 (Med)   | 1 (Med) | 9     | Should
Git Workflow          | 1 (Low)   | 0 (Low) | 3     | Could
Code Review Standards  | 1 (Low)   | 0 (Low) | 3     | Could
```

### Example 3: Performance Optimization

```
Task: Optimize API response time

Skills                  | Relevance | Impact | Score | Priority
----------------------|-----------|--------|-------|----------
Performance Engineering| 3 (High)  | 2 (High)| 14    | Must
Profiling             | 3 (High)  | 2 (High)| 14    | Must
DB Query Optimization | 3 (High)  | 2 (High)| 14    | Must
Caching Strategies    | 2 (Med)   | 2 (High)| 11    | Must
Monitoring            | 2 (Med)   | 1 (Med) | 8     | Should
API Design            | 2 (Med)   | 1 (Med) | 8     | Should
Database Design       | 1 (Low)   | 1 (Med) | 5     | Could
```

---

## Templates

### Scoring Matrix Template

```markdown
# Skill Scoring Matrix

**Task:** [Task Name]
**Date:** [Date]
**Scorer:** [Name]

## Scoring Formula
Score = (Relevance × 3) + (Impact × 2) + (Urgency × 1)

## Scoring Criteria

### Relevance
- 3 (High): Critical, directly addresses task
- 2 (Medium): Important, indirectly related
- 1 (Low): Helpful, general guidance

### Impact
- 2 (High): Makes significant difference to quality
- 1 (Medium): Noticeable improvement
- 0 (Low): Minor improvement

### Urgency
- 1 (Planning): Needed now
- 0 (Later): Needed later

## Skill Scores

| Skill | Relevance | Impact | Urgency | Score | Priority |
|-------|-----------|--------|---------|-------|----------|
| [Skill 1] | [L/M/H] | [H/M/L] | [Plan/Later] | [Score] | [Must/Should/Could] |
| [Skill 2] | [L/M/H] | [H/M/L] | [Plan/Later] | [Score] | [Must/Should/Could] |

## Prioritized List

### Must-Read (Score 10+)
1. [Skill 1] (Score: [Score])
2. [Skill 2] (Score: [Score])

### Should-Read (Score 5-9)
1. [Skill 3] (Score: [Score])
2. [Skill 4] (Score: [Score])

### Could-Read (Score <5)
1. [Skill 5] (Score: [Score])
2. [Skill 6] (Score: [Score])

## Context Adjustments
[Any context-specific adjustments]

## User Adjustments
[Any user-requested adjustments]
```

### Prioritization Algorithm Template

```python
# Skill Prioritization Algorithm

def score_skill(skill, task, context):
    """
    Calculate skill score based on relevance, impact, and urgency
    """
    # Base scores
    relevance = calculate_relevance(skill, task)
    impact = calculate_impact(skill, task)
    urgency = calculate_urgency(skill, task, context)

    # Context adjustments
    context_multiplier = get_context_multiplier(context)

    # User adjustments
    user_adjustment = get_user_adjustment(skill)

    # Calculate final score
    score = (relevance * 3) + (impact * 2) + (urgency * 1)
    score = score * context_multiplier + user_adjustment

    return score

def prioritize_skills(skills, task, context, budget):
    """
    Prioritize skills based on scores and budget
    """
    # Score all skills
    scored_skills = []
    for skill in skills:
        score = score_skill(skill, task, context)
        scored_skills.append((skill, score))

    # Sort by score (descending)
    scored_skills.sort(key=lambda x: x[1], reverse=True)

    # Filter by budget
    if budget == "limited":
        return scored_skills[:5]
    elif budget == "moderate":
        return scored_skills[:10]
    else:
        return scored_skills

# Example usage
task = "Create user authentication API"
context = "production"
budget = "moderate"

prioritized = prioritize_skills(all_skills, task, context, budget)
```

### Decision Framework Template

```markdown
# Skill Prioritization Decision Framework

**Task:** [Task Name]
**Constraints:** [Time, Budget, Quality]

## Decision Matrix

| Factor | Weight | Description |
|--------|--------|-------------|
| Relevance | 3 | How applicable to task |
| Impact | 2 | How much difference it makes |
| Urgency | 1 | When it's needed |
| Context | Variable | Project-specific adjustments |
| User | Variable | User preferences |

## Budget Levels

| Budget | Skills to Read | Description |
|--------|----------------|-------------|
| Limited | Top 3-5 | Speed-focused |
| Moderate | Top 5-10 | Balanced |
| Generous | Top 10-15+ | Quality-focused |

## Decision Process

1. Score all skills using formula
2. Apply context adjustments
3. Apply user adjustments
4. Sort by score
5. Filter by budget
6. Present prioritized list

## Output Format

```
Must-Read (★★★):
- [Skill 1] (Score: [Score])
- [Skill 2] (Score: [Score])

Should-Read (★★):
- [Skill 3] (Score: [Score])
- [Skill 4] (Score: [Score])

Could-Read (★):
- [Skill 5] (Score: [Score])
- [Skill 6] (Score: [Score])
```
```

---

## Best Practices

1. **Start with baseline** - Use universal baseline as foundation
2. **Score consistently** - Apply same scoring criteria to all skills
3. **Consider context** - Adjust scores based on project context
4. **Respect dependencies** - Read foundational skills first
5. **Be flexible** - Allow user adjustments to scores
6. **Present clearly** - Show scores and priorities visually
7. **Learn from feedback** - Improve scoring over time
8. **Balance quality vs speed** - Adjust based on constraints
9. **Document decisions** - Explain why skills are prioritized
10. **Review regularly** - Update scoring criteria as needed

---

## Related Skills

- [Baseline Policy](../baseline-policy/SKILL.md) - Universal baseline skills
- [Routing Rules](../routing-rules/SKILL.md) - Select skills before scoring
- [Output Templates](../output-templates/SKILL.md) - Document selected skills
