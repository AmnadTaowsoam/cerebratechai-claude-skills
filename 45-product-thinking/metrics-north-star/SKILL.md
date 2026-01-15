---
name: Metrics and North Star
description: Defining the key performance indicators that measure product success and align team efforts toward a common goal.
---

# Metrics and North Star

## Overview

Metrics and North Star is the discipline of using data to measure product-market fit, user engagement, and business growth. A **North Star Metric** is the single key metric that best captures the core value your product delivers to customers.

**Core Principle**: "If you can’t measure it, you can’t improve it. But if you measure the wrong thing, you will destroy the product."

---

## 1. The North Star Metric (NSM)

The NSM should be a **Leading Indicator** of future business success and a **Reflector** of customer value.

| Industry | Example North Star Metric | Why? |
| :--- | :--- | :--- |
| **SaaS (Slack)** | Messages sent within the team. | Reflects communication value. |
| **E-commerce (Amazon)** | Number of items delivered. | Reflects fulfillment value. |
| **Social (Facebook)** | Daily Active Users (DAU). | Reflects attention/ad value. |
| **Fintech (Stripe)** | Total Payment Volume (TPV). | Reflects transactional value. |

---

## 2. Leading vs. Lagging Indicators

*   **Lagging Indicators**: Outcomes that have already happened (e.g., Monthly Revenue, Total Churn). They are easy to measure but hard to influence directly.
*   **Leading Indicators**: Predictive signals of future success (e.g., Number of new projects created per user). They are harder to measure but easier to influence.

---

## 3. Metric Frameworks

### A. AARRR (Pirate Metrics)
Focuses on the customer lifecycle for growth-stage products.
1.  **A**cquisition: Where are users coming from?
2.  **A**ctivation: Do they have a "Great First Experience"?
3.  **R**etention: Do they come back?
4.  **R**eferral: Do they tell others?
5.  **R**evenue: Do we make money?

### B. HEART Framework (Google)
Focuses on the User Experience (UX).
1.  **H**appiness: Satisfaction, ease of use.
2.  **E**ngagement: Frequency, intensity of use.
3.  **A**doption: New user signups.
4.  **R**etention: Return rate.
5.  **T**ask Success: Efficiency, error rate.

### C. DORA Metrics (Engineering Quality)
Focuses on the software delivery speed and stability.
1.  Deployment Frequency.
2.  Lead Time for Changes.
3.  Change Failure Rate.
4.  Time to Restore Service (MTTR).

---

## 4. The Metric Hierarchy

A North Star metric is supported by **Input Metrics**.

*   **Level 0 (North Star)**: Total Active Subscriptions.
*   **Level 1 (Direct Inputs)**: New signups, Renewal rate, Average contract value.
*   **Level 2 (Indirect Inputs)**: Page load speed, Support ticket volume, Marketing spend.

---

## 5. Setting OKRs (Objectives and Key Results)

OKRs align the company's vision with actionable goals.

*   **Objective**: Qualitative, inspirational goal (e.g., "The fastest search experience on the web").
*   **Key Results**: Quantitative, measurable outcomes (e.g., "Reduce P99 search latency from 500ms to 100ms").

### OKR Template:
*"We will [Objective] as measured by [Key Result 1], [Key Result 2], and [Key Result 3]."*

---

## 6. Avoiding Vanity Metrics

A **Vanity Metric** makes you look good but doesn't correlate with success.
*   *Example*: "Total Registered Users" (meaningless if no one uses the app).
*   *Actionable Metric*: "Weekly Active Users who completed 2+ tasks."

---

## 7. Data-Informed vs. Data-Driven

*   **Data-Driven**: Follow the data blindly. (Risk: Missing the "Why," local maxima).
*   **Data-Informed**: Use data as one input among many (User research, intuition, market trends).

---

## 8. Retention and Churn Analysis

Retention is the lifeblood of SaaS.
*   **Cohort Analysis**: Tracking groups of users who signed up at the same time.
*   **Churn Rate**: (Users lost during period / Users at start of period) * 100.
*   **Critical Retention Metric**: "User completes core action 3 times in 7 days."

---

## 9. Tools for Metrics

*   **Instrumentation**: Segment, Google Tag Manager.
*   **Behavioral Analytics**: Amplitude, Mixpanel, PostHog.
*   **Business Intelligence**: Tableau, Looker, Metabase.
*   **Site Reliability**: Datadog, Grafana.

---

## 10. Metrics and North Star Checklist

- [ ] **Value-Linked**: Does our North Star metric actually track value for the customer?
- [ ] **Actionable**: If an input metric drops, does the team know exactly what to fix?
- [ ] **Leading**: Are we tracking leading indicators, not just revenue?
- [ ] **Non-Vanity**: Have we removed metrics that just make us look good?
- [ ] **Common Language**: Does every department (Sales, Eng, Product) understand the North Star?
- [ ] **Retention**: Are we tracking retention by cohort?
- [ ] **Data Quality**: Have we verified the accuracy of our instrumentation (no double-counting)?

---

## Related Skills
* `45-product-thinking/product-vision-strategy`
* `45-product-thinking/user-research-discovery`
* `42-cost-engineering/cost-observability`
