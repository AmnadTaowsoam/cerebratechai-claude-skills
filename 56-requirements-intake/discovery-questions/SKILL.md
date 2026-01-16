# Discovery Questions in Requirements Gathering

## Overview

Discovery questions are structured inquiries used to uncover hidden needs, clarify vague requirements, identify risks and dependencies, and understand the true problem space before building solutions.

## What Are Discovery Questions

Discovery questions are:

- **Structured questions** to understand requirements systematically
- **Uncover hidden needs** and constraints not explicitly stated
- **Clarify vague requirements** like "make it faster" or "improve UX"
- **Identify risks and dependencies** early in the project
- **Surface assumptions** that need validation

## Why Discovery Matters

| Benefit | Description |
|---------|-------------|
| **Avoid building the wrong thing** | Understand the real problem, not just the stated solution |
| **Understand true needs** | Distinguish between wants and underlying needs |
| **Surface constraints early** | Budget, timeline, technical, and regulatory limitations |
| **Set clear expectations** | Align stakeholders on what will be delivered |

## Discovery Question Categories

### 1. Problem Space Questions
Understand what problem we're solving and why it matters.

### 2. User Questions
Understand who will use the solution and their characteristics.

### 3. Success Criteria Questions
Define what success looks like and how we'll measure it.

### 4. Constraint Questions
Identify limitations that affect the solution.

### 5. Context Questions
Understand the broader business and project context.

### 6. Technical Discovery Questions
Explore technical requirements and constraints.

### 7. Risk Discovery Questions
Identify potential problems and uncertainties.

---

## Problem Space Questions

These questions help you understand the core problem and its context.

| Question | Purpose |
|----------|---------|
| What problem are you trying to solve? | Establish the primary issue |
| Why is this a problem? | Understand the impact and urgency |
| Who experiences this problem? | Identify affected users/stakeholders |
| How often does it occur? | Assess frequency and scope |
| What is the impact of not solving it? | Understand urgency and priority |
| What have you tried already? | Learn from past attempts |
| Why didn't previous solutions work? | Identify root causes and pitfalls |

### The 5 Whys Technique

When someone states a problem, ask "why" five times to reach the root cause:

```
Problem: "We need a new CRM system"

Why? "The current system is slow"
Why? "It takes too long to find customer data"
Why? "Data is spread across multiple systems"
Why? "We acquired 3 companies with different systems"
Why? "We grew through acquisitions without integration strategy"

Root Cause: Lack of unified data strategy, not just a slow system
```

---

## User Questions

Understanding the users is critical to building the right solution.

| Question | Purpose |
|----------|---------|
| Who are the primary users? | Main audience for the solution |
| Who are secondary users? | Indirect users or stakeholders |
| What is their technical skill level? | Design appropriate complexity |
| How many users (current and expected)? | Scale requirements |
| Where are they located (regions, timezones)? | Localization and availability needs |
| What devices/browsers do they use? | Compatibility requirements |
| What are their pain points with current solutions? | Opportunities for improvement |
| What are their goals when using this? | Design for user intent |

### User Persona Template

```
User Persona: [Name]
- Role: [Job title]
- Technical proficiency: [Beginner/Intermediate/Advanced]
- Primary goals: [What they want to achieve]
- Pain points: [What frustrates them]
- Typical environment: [Device, location, context]
- Frequency of use: [Daily/Weekly/Monthly]
```

---

## Success Criteria Questions

Define measurable outcomes to determine project success.

| Question | Purpose |
|----------|---------|
| How will we know this is successful? | Define success metrics |
| What metrics will we track? | Establish KPIs |
| What is the desired outcome? | Clarify end state |
| What would make this a failure? | Define failure conditions |
| When do you need this by? | Timeline (hard deadline or flexible?) |
| What's the minimum acceptable outcome? | MVP definition |

### Success Criteria Framework

```
Success Criteria for [Project Name]

Quantitative Metrics:
- [Metric 1]: [Target value] (e.g., Page load time < 2s)
- [Metric 2]: [Target value] (e.g., Conversion rate increase by 15%)

Qualitative Outcomes:
- [Outcome 1]: [Description]
- [Outcome 2]: [Description]

Failure Conditions:
- [Failure condition 1]: [Description]
- [Failure condition 2]: [Description]
```

---

## Constraint Questions

Identify limitations that affect what you can build.

| Question | Purpose |
|----------|---------|
| What is the budget? | Financial constraints |
| What is the timeline? | Time constraints (hard vs soft deadlines) |
| Who is available to work on this? | Resource constraints |
| Are there technical constraints? | Existing systems, tech stack requirements |
| Are there legal/compliance requirements? | Regulatory constraints |
| Are there performance requirements? | SLA, latency, throughput |
| What are the brand guidelines? | Design and tone constraints |

### Constraint Categories

```
Budget Constraints:
- Total budget: $[amount]
- Infrastructure budget: $[amount]
- Development budget: $[amount]

Time Constraints:
- Hard deadline: [date] (if applicable)
- Preferred completion: [date]
- Milestone dates: [list]

Resource Constraints:
- Team size: [number] people
- Available skills: [list]
- Tools available: [list]

Technical Constraints:
- Must use: [technologies]
- Must integrate with: [systems]
- Must support: [platforms/browsers]

Compliance Constraints:
- GDPR: Yes/No
- HIPAA: Yes/No
- SOC2: Yes/No
- WCAG 2.1: Yes/No
```

---

## Context Questions

Understand the broader business and project context.

| Question | Purpose |
|----------|---------|
| What is the broader business goal? | Align with company strategy |
| How does this fit into the roadmap? | Understand dependencies and sequencing |
| Who are the stakeholders? | Identify decision-makers and influencers |
| Are there dependencies on other projects? | Identify external factors |
| What is the competitive landscape? | Understand market position |
| What's the history of this project? | Learn from past attempts |

---

## Technical Discovery Questions

Explore technical requirements and constraints.

| Question | Purpose |
|----------|---------|
| What systems need to integrate? | Integration requirements |
| What data needs to be accessed? | Data access patterns |
| What is the expected traffic/load? | Scalability requirements |
| What are the availability requirements? | Uptime and reliability |
| What are the security requirements? | Data protection, authentication |
| What is the data retention policy? | Data lifecycle management |
| Are there existing APIs we must use? | Integration constraints |
| What's the expected data volume? | Storage and performance needs |

---

## Risk Discovery Questions

Identify potential problems and uncertainties.

| Question | Purpose |
|----------|---------|
| What could go wrong? | Surface potential issues |
| What keeps you up at night about this project? | Identify biggest concerns |
| What is the biggest uncertainty? | Highlight unknowns |
| What external dependencies exist? | Identify external risks |
| What happens if [X] fails? | Test assumptions |
| What's our backup plan if [Y] happens? | Contingency planning |

---

## Question Techniques

### Open-Ended Questions
Encourage detailed responses and exploration.

- "Tell me about how users currently..."
- "Describe the process when..."
- "Walk me through a typical scenario..."

### Probing Questions
Dig deeper into specific areas.

- "Why is that important?"
- "Can you elaborate on..."
- "What do you mean by..."
- "How does that work in practice?"

### Hypothetical Questions
Explore edge cases and alternatives.

- "What if the user doesn't have..."
- "What would happen if..."
- "How would you handle..."

### Reflective Questions
Confirm understanding and encourage elaboration.

- "So what you're saying is..."
- "Let me make sure I understand..."
- "If I'm hearing you correctly..."

---

## Avoiding Bad Questions

| Bad Question Type | Example | Better Alternative |
|-------------------|---------|-------------------|
| Leading question | "Don't you think we should use React?" | "What are your thoughts on using React?" |
| Multiple questions | "What's the timeline and budget and team?" | "What's the timeline? What's the budget?" |
| Yes/no when details needed | "Do users like the current system?" | "What do users like/dislike about the current system?" |
| Jargon with non-technical | "Do you need RESTful API endpoints?" | "How do other systems need to connect to this?" |

---

## Active Listening

Active listening is as important as asking good questions.

### Techniques

1. **Paraphrase back** - Confirm understanding
   - "So what you're saying is..."
   - "Let me make sure I understand..."

2. **Note what's not said** - Unspoken concerns
   - Notice hesitation
   - Note topics avoided

3. **Ask follow-ups** - Dig deeper
   - "Tell me more about..."
   - "Can you give an example..."

4. **Silence is okay** - Let them think
   - Don't rush to fill silence
   - Give space for reflection

---

## Documenting Discovery

Take structured notes during discovery conversations.

### Discovery Notes Template

```
Discovery Session Notes
Project: [Project Name]
Date: [Date]
Attendees: [List]

Key Points:
- [Point 1]
- [Point 2]

Requirements Identified:
- [Requirement 1]
- [Requirement 2]

Constraints:
- [Constraint 1]
- [Constraint 2]

Ambiguities (need clarification):
- [Ambiguity 1] - [Follow-up needed]
- [Ambiguity 2] - [Follow-up needed]

Action Items:
- [ ] [Action item] - [Owner] - [Due date]
- [ ] [Action item] - [Owner] - [Due date]

Open Questions:
- [Question 1]
- [Question 2]
```

---

## Discovery Meeting Structure

A well-structured discovery meeting ensures comprehensive coverage.

```
Discovery Meeting Agenda (60 minutes)

1. Intro (5 min)
   - Set context and goals
   - Review agenda
   - Introduce participants

2. Problem Space (15 min)
   - What problem are we solving?
   - Why is this a problem?
   - Who is affected?
   - Impact of not solving

3. Solution Space (15 min)
   - What have you tried?
   - What worked/didn't work?
   - What's the ideal outcome?

4. Constraints & Context (10 min)
   - Budget, timeline, resources
   - Technical constraints
   - Stakeholders and dependencies

5. Next Steps (5 min)
   - Summary of key points
   - Follow-up items
   - Next meeting (if needed)
```

---

## Domain-Specific Question Templates

### New Feature Discovery

```
Problem:
- What problem does this feature solve?
- Which users requested it?
- How often will it be used?

Functionality:
- What should the feature do?
- What are the edge cases?
- How does it integrate with existing features?

Success:
- How will we know it's successful?
- What metrics will we track?
```

### Bug Fix Discovery

```
Issue:
- What is the bug?
- When does it occur?
- How often does it happen?
- What is the impact?

Context:
- When was it introduced?
- What changed recently?
- Who is affected?

Resolution:
- What is the expected behavior?
- Are there workarounds?
- What's the priority?
```

### Performance Improvement

```
Current State:
- What are the current metrics?
- What is the target performance?
- When is the performance issue observed?

Analysis:
- What have you measured?
- Where are the bottlenecks?
- What have you tried?

Goals:
- What's the acceptable performance?
- What's the target improvement?
```

### Integration Project

```
Systems:
- What systems need to integrate?
- What data needs to flow between them?
- What are the integration points?

Technical:
- What APIs exist?
- What are the data formats?
- What are the authentication requirements?

Reliability:
- What happens if a system is down?
- What's the acceptable latency?
- Are there transaction requirements?
```

### Compliance Project

```
Regulations:
- What regulations apply?
- What are the specific requirements?
- What's the compliance deadline?

Current State:
- What's the current compliance status?
- What gaps exist?
- What's already in place?

Implementation:
- What needs to change?
- What's the timeline?
- Who needs to be involved?
```

---

## Red Flags in Discovery

Watch for these warning signs during discovery.

| Red Flag | Why It's a Problem | How to Address |
|----------|-------------------|----------------|
| Vague requirements ("make it better") | Hard to define success | Ask for specific examples and metrics |
| Solution masquerading as problem | May not address root cause | Ask "why" multiple times (5 Whys) |
| Unrealistic timelines | Risk of failure or quality issues | Break down work, provide realistic estimates |
| Unclear success criteria | Can't measure success | Define specific, measurable outcomes |
| Too many stakeholders with conflicting needs | Scope creep and delays | Identify decision-maker, prioritize needs |
| "We'll figure it out later" | Deferred decisions cause problems | Push for decisions or document as risk |
| No budget defined | Can't scope appropriately | Ask for budget range or constraints |
| No clear owner | Decision paralysis | Identify who has authority to decide |

---

## Post-Discovery

After discovery sessions, synthesize and share findings.

### Discovery Summary Template

```
Discovery Summary
Project: [Project Name]
Date: [Date]

Executive Summary:
[Brief overview of findings]

Problem Statement:
[Clear statement of the problem being solved]

Key Requirements:
1. [Requirement 1] - [Priority]
2. [Requirement 2] - [Priority]

Constraints:
- Budget: [amount]
- Timeline: [date]
- Team: [size/composition]
- Technical: [constraints]

Assumptions:
- [Assumption 1]
- [Assumption 2]

Risks:
- [Risk 1] - [Mitigation]
- [Risk 2] - [Mitigation]

Success Criteria:
- [Metric 1]: [Target]
- [Metric 2]: [Target]

Open Questions:
- [Question 1]
- [Question 2]

Next Steps:
1. [Step 1] - [Owner] - [Due date]
2. [Step 2] - [Owner] - [Due date]
```

---

## Real Discovery Scenarios

### Scenario 1: E-commerce Feature Request

**Stakeholder Request:** "We need a better checkout experience"

**Discovery Questions:**
- What's wrong with the current checkout?
- Where do users drop off?
- What are the specific pain points?
- What does "better" mean to you?
- What metrics are you tracking now?
- What's the desired improvement?

**Discovery Outcome:**
- Problem: 40% cart abandonment at payment step
- Root cause: Payment form is too complex
- Success metric: Reduce abandonment to 20%
- Constraint: Must use existing payment provider

### Scenario 2: Internal Tool Improvement

**Stakeholder Request:** "The dashboard is slow"

**Discovery Questions:**
- How slow is it? (specific numbers)
- When is it slow? (all the time, certain times, certain users?)
- What data is being displayed?
- How many users access it?
- What's the acceptable load time?
- Have there been recent changes?

**Discovery Outcome:**
- Problem: Dashboard takes 15+ seconds to load
- Root cause: N+1 query problem
- Success metric: Load time < 3 seconds
- Constraint: Cannot change database schema

### Scenario 3: API Integration Project

**Stakeholder Request:** "We need to integrate with [Third-Party API]"

**Discovery Questions:**
- What data needs to flow?
- How often does it need to sync?
- What's the acceptable latency?
- What happens if the API is down?
- What's the fallback strategy?
- Are there rate limits?
- What authentication is required?

**Discovery Outcome:**
- Requirement: Real-time sync of customer data
- Constraint: API has 1000 req/min rate limit
- Risk: API downtime could block operations
- Mitigation: Implement queue with retry logic

---

## Templates

### Discovery Question Checklist

```
Discovery Question Checklist

Problem Space:
[ ] What problem are you trying to solve?
[ ] Why is this a problem?
[ ] Who experiences this problem?
[ ] How often does it occur?
[ ] What is the impact of not solving it?
[ ] What have you tried already?
[ ] Why didn't previous solutions work?

Users:
[ ] Who are the primary users?
[ ] Who are secondary users?
[ ] What is their technical skill level?
[ ] How many users (current and expected)?
[ ] Where are they located?
[ ] What devices/browsers do they use?

Success Criteria:
[ ] How will we know this is successful?
[ ] What metrics will we track?
[ ] What is the desired outcome?
[ ] What would make this a failure?
[ ] When do you need this by?

Constraints:
[ ] What is the budget?
[ ] What is the timeline?
[ ] Who is available to work on this?
[ ] Are there technical constraints?
[ ] Are there legal/compliance requirements?
[ ] Are there performance requirements?

Context:
[ ] What is the broader business goal?
[ ] How does this fit into the roadmap?
[ ] Who are the stakeholders?
[ ] Are there dependencies on other projects?
[ ] What is the competitive landscape?

Technical:
[ ] What systems need to integrate?
[ ] What data needs to be accessed?
[ ] What is the expected traffic/load?
[ ] What are the availability requirements?
[ ] What are the security requirements?
[ ] What is the data retention policy?

Risks:
[ ] What could go wrong?
[ ] What keeps you up at night?
[ ] What is the biggest uncertainty?
[ ] What external dependencies exist?
```

### Discovery Meeting Notes Template

```
Discovery Meeting Notes

Project: _______________________________
Date: _________________________________
Time: _________________________________
Location: ______________________________
Attendees: ____________________________

Agenda:
1. _________________________________
2. _________________________________
3. _________________________________

Problem Space:
_______________________________________________
_______________________________________________
_______________________________________________

Users:
_______________________________________________
_______________________________________________
_______________________________________________

Success Criteria:
_______________________________________________
_______________________________________________
_______________________________________________

Constraints:
Budget: _______________________________
Timeline: _____________________________
Resources: ____________________________
Technical: ____________________________

Risks:
_______________________________________________
_______________________________________________
_______________________________________________

Open Questions:
1. _________________________________
2. _________________________________
3. _________________________________

Action Items:
[ ] _________________________________ - Owner: ________ Due: _______
[ ] _________________________________ - Owner: ________ Due: _______
[ ] _________________________________ - Owner: ________ Due: _______

Next Meeting: _________________________
```

### Discovery Summary Document Template

```markdown
# Discovery Summary: [Project Name]

**Date:** [Date]
**Prepared by:** [Name]

## Executive Summary
[2-3 sentence summary of key findings]

## Problem Statement
[Clear, concise statement of the problem]

## Key Requirements

### Must-Have
- [Requirement 1]
- [Requirement 2]

### Should-Have
- [Requirement 1]
- [Requirement 2]

### Could-Have
- [Requirement 1]
- [Requirement 2]

## Constraints

### Budget
- Total: $[amount]
- Breakdown: [details]

### Timeline
- Start date: [date]
- End date: [date]
- Milestones: [list]

### Resources
- Team size: [number]
- Skills available: [list]

### Technical
- Must use: [technologies]
- Must integrate with: [systems]
- Must support: [platforms]

### Compliance
- [Regulation 1]: [requirements]
- [Regulation 2]: [requirements]

## Assumptions
- [Assumption 1]
- [Assumption 2]
- [Assumption 3]

## Risks

| Risk | Probability | Impact | Mitigation | Owner |
|------|-------------|--------|------------|-------|
| [Risk 1] | High/Med/Low | High/Med/Low | [Mitigation] | [Name] |
| [Risk 2] | High/Med/Low | High/Med/Low | [Mitigation] | [Name] |

## Success Criteria

### Quantitative
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]

### Qualitative
- [Outcome 1]
- [Outcome 2]

## Open Questions
1. [Question 1]
2. [Question 2]

## Next Steps
1. [Step 1] - [Owner] - [Due date]
2. [Step 2] - [Owner] - [Due date]
3. [Step 3] - [Owner] - [Due date]

## Appendix
- [Additional notes, diagrams, etc.]
```

---

## Best Practices

1. **Prepare before the meeting** - Review existing materials, prepare questions
2. **Start with the problem, not the solution** - Understand the "why" before the "what"
3. **Listen more than you speak** - Ratio of 80% listening, 20% asking
4. **Document in real-time** - Take notes during the conversation
5. **Follow up promptly** - Send summary within 24-48 hours
6. **Validate assumptions** - Don't assume, verify
7. **Be curious** - Ask "why" to get to root causes
8. **Stay neutral** - Don't push your own solutions
9. **Use visual aids** - Diagrams, whiteboards help clarify
10. **Build rapport** - Discovery is a collaborative process

---

## Related Skills

- [Requirement to Scope](../requirement-to-scope/SKILL.md) - Convert discovery findings to scope
- [Acceptance Criteria](../acceptance-criteria/SKILL.md) - Define done criteria
- [Constraints and Assumptions](../constraints-and-assumptions/SKILL.md) - Document constraints
- [Risk and Dependencies](../risk-and-dependencies/SKILL.md) - Identify and manage risks
