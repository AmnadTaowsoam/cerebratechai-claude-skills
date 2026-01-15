---
name: Product Roadmapping
description: Creating a high-level visual plan and communication tool for aligning the organization on product priorities and goals over time.
---

# Product Roadmapping

## Overview

A Product Roadmap is a strategic communication tool that outlines the vision, direction, and progress of a product over time. It aligns internal stakeholders and informs external customers about what features and outcomes to expect and when.

**Core Principle**: "A roadmap is a statement of intent, not a fixed contract."

---

## 1. Outcome-Based vs. Output-Based Roadmaps

| Type | Focus | Example |
| :--- | :--- | :--- |
| **Output-Based (Legacy)**| Specific features and dates. | "Integrate Stripe by Q3." |
| **Outcome-Based (Modern)**| Problems to solve or goals. | "Reduce payment failure rate by 50%." |

Modern product teams prefer **Outcome-Based** roadmaps because they allow for flexibility in *how* the problem is solved as technology and user needs evolve.

---

## 2. Roadmap Formats: Now, Next, Later

The most effective roadmap format for Agile teams replaces "Quarterly Dates" with "Tiers of Certainty."

*   **Now** (0-3 months): Committed work; well-defined problems and solutions. High confidence.
*   **Next** (3-6 months): Validated opportunities; discovery is underway. Medium confidence.
*   **Later** (6+ months): Strategic areas of interest; needs validation. Low confidence.

---

## 3. Prioritization Frameworks

Choosing what to build next requires a structured, objective methodology.

### A. RICE Scoring (The "Go-To" for SaaS)
*   **R**each: How many users will this impact per period? (e.g., 500/mo).
*   **I**mpact: How much will it help? (3: Massive, 2: High, 1: Medium, 0.5: Low).
*   **C**onfidence: How sure are we about the data? (100%: High, 80%: Medium, 50%: Low).
*   **E**ffort: How many person-months will it take?
*   **Formula**: `(Reach * Impact * Confidence) / Effort = RICE Score`

### B. MoSCoW
*   **M**ust have: Vital for launch/success.
*   **S**hould have: Important but not vital.
*   **C**ould have: Nice to have (will do if time permits).
*   **W**on't have: Not this time.

### C. The Kano Model
*   **Basic Needs**: Features users assume are there (must be perfect).
*   **Performance Needs**: "More is better" (e.g., speed).
*   **Delighters**: Unexpected features that drive high satisfaction (User wows).

---

## 4. Connecting Strategy to Roadmap

A roadmap item should always link back to a **Strategic Pillar** (see `product-vision-strategy`).

```text
Vision: Be the safest bank in the world.
  -> Pillar: Security First.
    -> Roadmap Item: "Implement 2FA biometric login" (NOW).
```

---

## 5. Handling Change: The "In-N-Out" Rule

When a stakeholder requests an urgent new feature:
1.  **Acknowledge**: "That's an interesting opportunity."
2.  **Trade-off**: "If we move this into 'Now', which currently planned item should we move to 'Later'?"
3.  **Data-check**: Run a quick RICE score on the new request.

---

## 6. Communicating the Roadmap

*   **Internal Roadmap**: Detailed, including tech debt, infrastructure, and internal tools.
*   **External Roadmap**: Public-facing, higher-level, focuses on value and benefits (usually avoids specific dates).

---

## 7. Roadmap Tools

*   **Productboard**: Comprehensive platform for discovery, prioritization, and roadmapping.
*   **Aha!**: Enterprise roadmap software with deep strategic alignment tools.
*   **Roadmunk**: Visual roadmapping for presentation and stakeholder alignment.
*   **Notion**: Highly flexible for "Now/Next/Later" boards using database views.

---

## 8. Real-World Scenario: The "Competitor Panic"
*   **Scenario**: A competitor launches a new "AI Chat" feature. The CEO wants it on our roadmap immediately.
*   **Roadmap Response**: Instead of adding "AI Chat" to the roadmap, the product manager performed Discovery. Found that users actually just wanted "Faster Support Replies."
*   **Result**: The roadmap item became "Automated Support Macros," which was 10x cheaper to build than a full LLM chat and solved the actual user problem.

---

## 9. Product Roadmapping Checklist

- [ ] **Outcome-focused**: Does every item have a clearly defined "Desired Outcome"?
- [ ] **Prioritized**: Is the roadmap ordered by RICE score or an equivalent framework?
- [ ] **Tiers**: Are we using "Now/Next/Later" instead of rigid dates?
- [ ] **Alignment**: Have the engineering leads reviewed the "Effort" estimates?
- [ ] **Strategy-linked**: Does every item map to a high-level strategic pillar?
- [ ] **Buffer**: Is there room in the "Now" tier for maintenance and unplanned bugs?
- [ ] **Access**: Is the latest roadmap accessible to all stakeholders?

---

## Related Skills
* `45-product-thinking/product-vision-strategy`
* `45-product-thinking/agile-scrum-practices`
* `45-product-thinking/metrics-north-star`
