---
name: Agile and Scrum Practices
description: Frameworks and methodologies for iterative software development, team collaboration, and rapid value delivery.
---

# Agile and Scrum Practices

## Overview

Agile is a philosophy centered around iterative development, customer feedback, and cross-functional teams. **Scrum** is the most widely used framework for implementing Agile, providing a structured set of roles, events, and artifacts.

**Core Principle**: "Deliver working software frequently, and welcome changing requirements, even late in development."

---

## 1. The Agile Manifesto (Core Values)

1.  **Individuals and Interactions** over processes and tools.
2.  **Working Software** over comprehensive documentation.
3.  **Customer Collaboration** over contract negotiation.
4.  **Responding to Change** over following a plan.

---

## 2. The Scrum Framework: Roles

| Role | Responsibility |
| :--- | :--- |
| **Product Owner** | Maximize product value; manages the Product Backlog. (The "What"). |
| **Scrum Master** | Facilitator; removes blockers and ensures Scrum values are followed. |
| **Developers** | Cross-functional team that creates the "Increment" each sprint. (The "How"). |

---

## 3. The Scrum Events

The Sprint is the heart of Scrum—a time-box of 1–4 weeks.

1.  **Sprint Planning**: Defining the Sprint Goal and selecting backlog items.
2.  **Daily Stand-up**: 15-minute alignment. "What did I do? What will I do? What is blocking me?"
3.  **Sprint Review**: Demonstrating the "Increment" to stakeholders and gathering feedback.
4.  **Sprint Retrospective**: The team reflects on *process* (How to work better next time).
5.  **Backlog Refinement**: Ongoing activity to detail and estimate future backlog items.

---

## 4. Scrum Artifacts

*   **Product Backlog**: Ordered list of everything needed in the product.
*   **Sprint Backlog**: Set of items selected for the current Sprint.
*   **Increment**: The concrete sum of all backlog items completed during the Sprint (must be "Done").

---

## 5. User Stories and THE INVEST Criteria

A User Story is a placeholder for a conversation.
*   *Format*: "As a [User], I want to [Action], so that [Benefit]."

**INVEST Quality Check**:
*   **I**ndependent: Can be developed/released on its own.
*   **N**egotiable: Not a rigid contract; open to discussion.
*   **V**aluable: Provides clear customer value.
*   **E**stimable: Known enough for the team to size it.
*   **S**mall: Fits within a single sprint.
*   **T**estable: Has clear acceptance criteria.

---

## 6. Estimation: Story Points

Scrum uses relative sizing (complexity/effort) rather than time.
*   **Fibonacci Sequence**: 1, 2, 3, 5, 8, 13 (A '13' is too big; break it down).
*   **Planning Poker**: Collaborative technique to avoid "anchoring" (everyone votes simultaneously).
*   **Velocity**: The average number of Story Points a team completes per sprint. Use it for forecasting, not as a performance target.

---

## 7. Definition of Done (DoD) vs. Definition of Ready (DoR)

### Definition of Ready (DoR)
The criteria an item must meet *before* it can enter a Sprint.
*   User story written and estimated.
*   Dependencies identified.
*   Design/UX mockups attached.

### Definition of Done (DoD)
The criteria an item must meet to be considered "Finished."
*   Code reviewed and merged.
*   Tests passed (Unit, Integration).
*   Documentation updated.
*   Product Owner approval.

---

## 8. Kanban vs. Scrum

*   **Scrum**: Defined roles, fixed-length sprints, regular ceremonies. Best for complex, feature-heavy products.
*   **Kanban**: Continuous flow, no fixed roles, focus on **WIP (Work in Progress) Limits**. Best for support, DevOps, or highly unpredictable environments.

---

## 9. Tools for Agile Teams

*   **Jira**: Enterprise standard; highly customizable but complex.
*   **Linear**: Modern, fast tool focused on developer experience (DX).
*   **Trello**: Simple card-based Kanban.
*   **Miro**: Digital whiteboard for retrospectives and planning.

---

## 10. Agile and Scrum Checklist

- [ ] **Sprint Goal**: Does the team have a one-sentence goal for the current sprint?
- [ ] **Cross-functional**: Do we have all the skills (Front-end, Back-end, Design) required to finish the work?
- [ ] **Blockers**: Does the Scrum Master actively remove blockers within 24 hours?
- [ ] **Feedback**: Are we showing working code to REAL users in the Sprint Review?
- [ ] **Retrospective**: Is the team completing at least one "Action Item" from every retrospective?
- [ ] **Estimation**: Are we estimating based on complexity, not hours?
- [ ] **Tech Debt**: Do we allocate ~20% of the sprint to bugs and infrastructure?

---

## Related Skills
* `45-product-thinking/product-roadmapping`
* `45-product-thinking/stakeholder-management`
* `41-incident-management/incident-retrospective`
