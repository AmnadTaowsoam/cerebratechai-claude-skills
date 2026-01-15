---
name: User Research and Discovery
description: Techniques for identifying user needs, validating assumptions, and ensuring we build the right product before building it right.
---

# User Research and Discovery

## Overview

User Research and Discovery is the process of understanding user behaviors, needs, and motivations through various qualitative and quantitative investigation methods. Modern product discovery is **Continuous**, meaning it happens in parallel with delivery to ensure the team is solving real problems.

**Core Principle**: "Fall in love with the problem, not the solution."

---

## 1. Problem Space vs. Solution Space

A common mistake is jumping straight to features (Solution) before defining the need (Problem).

*   **Problem Space**: Understanding the user's pain points, context, and goals (e.g., "It takes too long for researchers to find specific experiment data").
*   **Solution Space**: Designing features and technology to address the need (e.g., "Build an AI-powered semantic search engine for lab notes").

---

## 2. Research Methodologies

### Qualitative (The "Why")
*   **User Interviews**: One-on-one conversations to explore motivations.
*   **Contextual Inquiry**: Observing users in their natural environment as they work.
*   **Usability Testing**: Watching users attempt to complete tasks using a prototype.

### Quantitative (The "What")
*   **Product Analytics**: Tracking what users *actually* do in the app (Mixpanel, Amplitude).
*   **Surveys**: Gathering data from a large sample.
*   **A/B Testing**: Comparing two versions to see which performs better.

---

## 3. The Mom Test (Effective Interviewing)

Based on Rob Fitzpatrick's framework, you should ask questions that even your mom couldn't lie about.

| Bad Questions (Avoid) | Good Questions (Ask) |
| :--- | :--- |
| "Would you use this feature?" | "Tell me about the last time you tried to [Action]?" |
| "Is this a good idea?" | "What are you doing now to solve [Problem]?" |
| "How much would you pay?" | "How much does [Problem] currently cost you (time/money)?" |

---

## 4. Opportunity Solution Tree (Teresa Torres)

A visual framework for mapping the path from a desired outcome to specific technical experiments.

1.  **Outcome**: The high-level goal (e.g., "Increase user retention by 20%").
2.  **Opportunities**: User needs/pain points that drive the outcome (e.g., "App is too slow," "Don't know how to start").
3.  **Solutions**: Ideas to address opportunities (e.g., "Onboarding walkthrough," "Native mobile app").
4.  **Assumptions/Experiments**: Small tests to validate solutions (e.g., "Prototype a 3-step wizard").

---

## 5. Artifacts of Discovery

### Personas
Fictional characters created to represent the different user types within your targeted demographic.
*   *Example*: "Alice the Analyst" - Goal: Speed. Pain: Manual data entry. Tech: Advanced Excel.

### Customer Journey Maps
A visual representation of every touchpoint a customer has with your product, highlighting emotional highs and lows.

### Empathy Maps
What the user is **Saying**, **Thinking**, **Doing**, and **Feeling**.

---

## 6. Validating Assumptions

Before writing code, validate the three risks (Marty Cagan):
1.  **Value Risk**: Will customers buy/use it?
2.  **Usability Risk**: Can they figure out how to use it?
3.  **Feasibility Risk**: Can we build it with our current tech/time?
4.  **Viability Risk**: Should we build it? Does it fit the business?

---

## 7. Tools for Discovery

*   **Dovetail / EnjoyHQ**: For organizing and tagging interview notes.
*   **Maze / UserTesting**: For unmoderated remote usability tests.
*   **Hotjar / FullStory**: For session recordings and heatmaps.
*   **Miro / FigJam**: For mapping journeys and collaborative brainstorming.

---

## 8. Real-World Scenario: The "Social" Feature
*   **Assumption**: Adding a social feed to a fitness app will increase engagement.
*   **Discovery**: Conducted 10 interviews. Found that users felt "intimidated" by others' progress.
*   **Pivot**: Instead of a public feed, built a "Private Groups" feature for families.
*   **Result**: 30% higher engagement than the original feed proposal, and avoided a high-cost failure.

---

## 9. User Research and Discovery Checklist

- [ ] **Problem defined**: Can we state the user problem in one sentence without mentioning a feature?
- [ ] **Diverse users**: Have we interviewed both "Power Users" and "New/Struggling Users"?
- [ ] **Mom Test**: Are we asking about past behavior instead of future predictions?
- [ ] **Prototype**: Do we have a low-fidelity (Miro/Figma) version to test first?
- [ ] **Feasibility**: Have we included an engineer in the discovery calls to assess technical lift?
- [ ] **Metric**: Do we know exactly which metric this discovery work aims to improve?

---

## Related Skills
* `45-product-thinking/product-vision-strategy`
* `45-product-thinking/metrics-north-star`
* `00-meta-skills/empathetic-communication`
