---
name: KPI (Key Performance Indicator) Metrics
description: Defining, tracking, and measuring key performance indicators that demonstrate how effectively an organization is achieving key business objectives.
---

# KPI (Key Performance Indicator) Metrics

> **Current Level:** Intermediate  
> **Domain:** Business Analytics / Strategy

---

## Overview

KPIs are measurable values that demonstrate how effectively an organization is achieving key business objectives. Effective KPIs are aligned with business goals, actionable, trackable over time, and drive decision-making.

## What are KPIs

KPIs are measurable values that demonstrate how effectively an organization is achieving key business objectives.

### KPI Definition

| Component | Description |
|-----------|-------------|
| **Measurable** | Can be quantified |
| **Aligned** | Linked to business goals |
| **Actionable** | Drives decisions |
| **Trackable** | Can be monitored over time |

### Why KPIs Matter

| Benefit | Description |
|---------|-------------|
| **Focus** | Align team on priorities |
| **Accountability** | Clear ownership |
| **Decision-making** | Data-driven choices |
| **Performance** | Track progress |
| **Improvement** | Identify areas to optimize |

## Good KPI Characteristics

### SMART Framework

| Letter | Meaning | Example |
|--------|----------|---------|
| **S** | Specific | "Increase revenue by 10%" not "Improve revenue" |
| **M** | Measurable | "100 new signups" not "More signups" |
| **A** | Achievable | "10% growth" not "1000% growth" |
| **R** | Relevant | "Improve retention" aligns with business goal |
| **T** | Time-bound | "By Q4 2024" not "Eventually" |

### KPI Quality Checklist

- [ ] Is it specific?
- [ ] Is it measurable?
- [ ] Is it achievable?
- [ ] Is it relevant to goals?
- [ ] Does it have a deadline?

## Types of KPIs

### Financial KPIs

| KPI | Formula | Benchmark |
|------|---------|-----------|
| **Revenue** | Sum of all sales | Varies by industry |
| **Gross Margin** | (Revenue - COGS) / Revenue | 30-50% |
| **Net Profit Margin** | Net Income / Revenue | 10-20% |
| **Burn Rate** | Monthly cash spent | Depends on stage |
| **Runway** | Cash / Burn Rate | 12+ months (startup) |
| **Cash Flow** | Cash In - Cash Out | Positive |

### Customer KPIs

| KPI | Formula | Benchmark |
|------|---------|-----------|
| **NPS** | % Promoters - % Detractors | > 50 (excellent) |
| **Churn Rate** | Customers Lost / Total Customers | < 5% (SaaS) |
| **Customer Satisfaction (CSAT)** | Average satisfaction score | 4-5/5 |
| **Customer Lifetime Value (LTV)** | Avg Revenue × Avg Lifetime | 3-5× CAC |
| **Customer Acquisition Cost (CAC)** | Marketing Spend / New Customers | Varies |
| **LTV:CAC Ratio** | LTV / CAC | > 3:1 |

### Operational KPIs

| KPI | Formula | Benchmark |
|------|---------|-----------|
| **Uptime** | (Total Time - Downtime) / Total Time | > 99.9% |
| **Response Time** | Avg time to respond | < 24 hours |
| **Resolution Time** | Avg time to resolve | < 48 hours |
| **Throughput** | Units processed per hour | Varies |
| **Error Rate** | Errors / Total Requests | < 1% |

### Growth KPIs

| KPI | Formula | Benchmark |
|------|---------|-----------|
| **MRR Growth** | (Current MRR - Previous MRR) / Previous MRR | 10-20% MoM |
| **User Growth** | (Current Users - Previous Users) / Previous Users | 5-15% MoM |
| **Viral Coefficient** | Invites per user × Conversion | > 1 (viral) |
| **Activation Rate** | Activated Users / Signups | > 40% |

## North Star Metric

### What is North Star Metric

The single metric that best captures the core value your product delivers to customers.

### North Star Examples

| Product Type | North Star Metric |
|--------------|-------------------|
| **SaaS** | Weekly Active Users (WAU) |
| **E-commerce** | Orders per week |
| **Marketplace** | Gross Merchandise Value (GMV) |
| **Social Media** | Daily Active Users (DAU) |
| **Streaming** | Hours watched per week |
| **Messaging** | Messages sent per week |

### North Star Criteria

- **Customer-centric**: Measures value delivered
- **Leading indicator**: Predicts future success
- **Actionable**: Team can influence it
- **Measurable**: Can be tracked accurately

## Leading vs Lagging Indicators

### Comparison

| Aspect | Leading Indicators | Lagging Indicators |
|---------|-------------------|-------------------|
| **Definition** | Predict future | Measure past |
| **Example** | Pipeline, trials | Revenue, churn |
| **Use Case** | Forecasting | Reporting |
| **Timing** | Early warning | Post-fact |

### Balance Both

```
Leading Indicators          Lagging Indicators
─────────────────         ┌─────────────────┐
Pipeline ($5M)     ─────▶│  Revenue       │
                          │  ($1M)         │
Trials (500)        ─────▶│  Signups       │
                          │  (100)         │
NPS Score (+50)      ─────▶│  Churn Rate   │
                          │  (2%)          │
                          └─────────────────┘
```

## Vanity vs Actionable Metrics

### Comparison

| Metric Type | Description | Example |
|--------------|-------------|---------|
| **Vanity** | Looks good but not useful | Total signups |
| **Actionable** | Drives decisions | Activation rate |

### Examples

| Vanity Metric | Actionable Metric |
|---------------|------------------|
| Total signups | Activation rate |
| Page views | Time on page |
| App downloads | Daily active users |
| Email opens | Click-through rate |
| Social media followers | Engagement rate |

### Test for Actionability

**Question**: If this metric goes up/down, would you take different action?

- **Yes** → Actionable
- **No** → Vanity

## SaaS KPIs

### Key Metrics

| KPI | Formula | Benchmark |
|------|---------|-----------|
| **MRR** | Sum of monthly recurring revenue | Varies |
| **ARR** | MRR × 12 | Varies |
| **Churn Rate** | Customers Lost / Total Customers | < 5% |
| **Net Churn** | (Churned MRR - Expansion MRR) / Starting MRR | < 2% |
| **LTV** | ARPU × Customer Lifetime | 3-5× CAC |
| **CAC** | Marketing Spend / New Customers | Varies |
| **LTV:CAC Ratio** | LTV / CAC | > 3:1 |
| **Payback Period** | CAC / (ARPU × Gross Margin) | < 12 months |
| **NPS** | % Promoters - % Detractors | > 50 |
| **Activation Rate** | Activated Users / Signups | > 40% |

### SaaS KPI Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  SaaS Metrics Dashboard                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ MRR         │  │ Churn       │  │ LTV:CAC     │           │
│  │ $125,000    │  │ 2.5%        │  │ 4.2:1      │           │
│  │ ▲ 8.2%      │  │ ▼ 0.3%      │  │ ▲ 0.2      │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                  │
│  MRR Growth                                                     │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ $150k ┤                                                    │ │
│  │ $125k ┤  ●───●───●───●───●                                  │ │
│  │ $100k ┤                                                    │ │
│  │  $75k ┤                                                    │ │
│  │  $50k ┤                                                    │ │
│  │  $25k ┤                                                    │ │
│  │   $0 └──────────────────────────────────────────────────────│ │
│  │        Jan  Feb  Mar  Apr  May  Jun                      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## E-commerce KPIs

### Key Metrics

| KPI | Formula | Benchmark |
|------|---------|-----------|
| **Conversion Rate** | Conversions / Visitors | 2-5% |
| **Average Order Value (AOV)** | Revenue / Orders | $50-100 |
| **Revenue Per Visitor (RPV)** | Revenue / Visitors | $2-5 |
| **Cart Abandonment Rate** | Abandoned Carts / Started Carts | 70-80% |
| **Customer Retention Rate** | Returning Customers / Total Customers | 30-50% |
| **Repeat Purchase Rate** | Repeat Purchases / Total Purchases | 20-30% |
| **Return Rate** | Returned Orders / Total Orders | < 10% |

### E-commerce KPI Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  E-commerce Dashboard                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ Revenue     │  │ Conversion  │  │ AOV         │           │
│  │ $45,234     │  │ 2.5%        │  │ $36.67      │           │
│  │ ▲ 12.3%     │  │ ▲ 0.5%      │  │ ▲ 3.2%      │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                  │
│  Revenue by Category                                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Electronics  ████████████████████████████████████████  $15K  │ │
│  │ Clothing     ██████████████████████                  $10K  │ │
│  │ Home         ████████████████                         $8K   │ │
│  │ Books        ██████████                                 $4K   │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Product KPIs

### Key Metrics

| KPI | Formula | Benchmark |
|------|---------|-----------|
| **DAU** | Daily Active Users | Varies |
| **WAU** | Weekly Active Users | Varies |
| **MAU** | Monthly Active Users | Varies |
| **Stickiness** | DAU / MAU | > 20% |
| **Retention (D1)** | % users return Day 1 | > 40% |
| **Retention (D7)** | % users return Day 7 | > 20% |
| **Retention (D30)** | % users return Day 30 | > 10% |
| **Feature Adoption** | % users using feature | Varies |
| **Time to Value (TTV)** | Time to first value | < 5 minutes |

### Product KPI Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  Product Dashboard                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ DAU         │  │ Stickiness  │  │ Retention   │           │
│  │ 12,345      │  │ 25%         │  │ 45%        │           │
│  │ ▲ 5%        │  │ ▲ 2%        │  │ ▲ 3%        │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                  │
│  Active Users Trend                                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 15k ┤                                                    │ │
│  │ 12k ┤  ●───●───●───●───●                                  │ │
│  │  9k ┤                                                    │ │
│  │  6k ┤                                                    │ │
│  │  3k ┤                                                    │ │
│  │   0 └──────────────────────────────────────────────────────│ │
│  │        Jan  Feb  Mar  Apr  May  Jun                      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Marketing KPIs

### Key Metrics

| KPI | Formula | Benchmark |
|------|---------|-----------|
| **Traffic** | Website visits | Varies |
| **Leads** | Form submissions, signups | Varies |
| **Lead-to-Customer Rate** | Customers / Leads | 10-20% |
| **CAC by Channel** | Channel Spend / New Customers | Varies |
| **ROAS** | Revenue / Ad Spend | > 4:1 |
| **CTR** | Clicks / Impressions | 1-3% |
| **Conversion Rate** | Conversions / Clicks | 2-5% |
| **Content Engagement** | Avg time on page | 2-3 min |

### Marketing KPI Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  Marketing Dashboard                                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ Traffic     │  │ Leads       │  │ CAC         │           │
│  │ 123,456     │  │   1,234     │  │    $45       │           │
│  │ ▲ 8%        │  │ ▲ 12%       │  │ ▼ 5%        │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                  │
│  Traffic by Channel                                             │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Organic    ████████████████████████████████████████  50K   │ │
│  │ Paid      ████████████████████████████              40K   │ │
│  │ Social    ████████████████████                         20K   │ │
│  │ Email    ████████████                                 10K   │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Financial KPIs

### Key Metrics

| KPI | Formula | Benchmark |
|------|---------|-----------|
| **Gross Margin** | (Revenue - COGS) / Revenue | 30-50% |
| **Net Profit Margin** | Net Income / Revenue | 10-20% |
| **Burn Rate** | Monthly cash spent | Depends on stage |
| **Runway** | Cash / Burn Rate | 12+ months (startup) |
| **Rule of 40** | Growth Rate + Profit Margin | > 40% |
| **EBITDA** | Earnings Before Interest, Taxes, Depreciation, Amortization | Positive |

### Financial KPI Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  Financial Dashboard                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ Revenue     │  │ Gross Margin│  │ Burn Rate   │           │
│  │ $1,234,567  │  │ 45%         │  │ $50,000     │           │
│  │ ▲ 12.3%     │  │ ▲ 2%        │  │ ▼ 5%        │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                  │
│  Revenue Trend                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ $1.5M ┤                                                    │ │
│  │ $1.2M ┤  ●───●───●───●───●                                  │ │
│  │ $0.9M ┤                                                    │ │
│  │ $0.6M ┤                                                    │ │
│  │ $0.3M ┤                                                    │ │
│  │   $0 └──────────────────────────────────────────────────────│ │
│  │        Q1    Q2    Q3    Q4                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Customer Success KPIs

### Key Metrics

| KPI | Formula | Benchmark |
|------|---------|-----------|
| **Customer Health Score** | Weighted score of engagement | Varies |
| **Time to Resolution** | Avg time to resolve ticket | < 24 hours |
| **First Response Time** | Avg time to first response | < 1 hour |
| **CSAT** | Average satisfaction score | 4-5/5 |
| **Expansion MRR** | Additional revenue from existing customers | > 10% |
| **Renewal Rate** | Renewed subscriptions / Total | > 90% |

## KPI Targets

### Setting Targets

| Component | Description | Example |
|------------|-------------|---------|
| **Baseline** | Current performance | 2% conversion |
| **Target** | Goal to achieve | 3% conversion |
| **Stretch Goal** | Ambitious target | 4% conversion |
| **Timeline** | When to achieve | By Q4 2024 |

### Target Setting Process

1. **Measure baseline**: Current performance
2. **Set realistic target**: 10-20% improvement
3. **Set stretch goal**: 50%+ improvement
4. **Define timeline**: Quarterly, annually
5. **Track progress**: Regular reviews

### Example: Revenue Target

```
Baseline: $1M ARR
Target: $1.2M ARR (+20%)
Stretch Goal: $1.5M ARR (+50%)
Timeline: By Q4 2024
```

## KPI Dashboards

### Executive Dashboard

**Audience**: C-suite, executives

**Metrics**: 5-7 high-level KPIs

**Update**: Monthly/quarterly

```
┌─────────────────────────────────────────────────────────────────┐
│  Executive Dashboard                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ Revenue     │  │ Profit      │  │ Growth      │           │
│  │ $1.2M ARR   │  │ 15% margin  │  │ 20% YoY     │           │
│  │ ▲ 12% YoY   │  │ ▲ 2%       │  │ ▲ 3%       │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐                           │
│  │ Customers   │  │ Churn       │                           │
│  │ 10,000      │  │ 2.5%        │                           │
│  │ ▲ 15% YoY   │  │ ▼ 0.5%      │                           │
│  └─────────────┘  └─────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Departmental Dashboard

**Audience**: Managers, team leads

**Metrics**: 10-15 KPIs

**Update**: Weekly/daily

```
┌─────────────────────────────────────────────────────────────────┐
│  Sales Dashboard                                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ Pipeline    │  │ Revenue     │  │ Conversion  │           │
│  │ $5M         │  │ $1.2M       │  │ 25%         │           │
│  │ ▲ 10%       │  │ ▲ 12%       │  │ ▲ 2%        │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                  │
│  Pipeline by Stage                                               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Qualified  ████████████████████████████████████████  $2M   │ │
│  │ Proposal   ████████████████████████████              $1.5M │ │
│  │ Negotiation███████████████████████                      $1M   │ │
│  │ Closed Won ████████████████████████████████████████  $0.5M │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Metric Definitions

### Definition Template

```markdown
# Metric: Monthly Recurring Revenue (MRR)

**Definition**: Sum of all monthly subscription revenue.

**Calculation**: SUM(monthly_subscription_amount) for active subscriptions

**Includes**:
- Monthly subscriptions
- Prorated annual subscriptions

**Excludes**:
- One-time fees
- Annual subscriptions (not prorated)

**Owner**: Finance Team

**Update Frequency**: Daily

**Data Source**: Billing system (Stripe)
```

### Example Definitions

#### Active User

```markdown
**Definition**: User who logged in AND performed an action in the last 7 days.

**Includes**:
- Page views
- Feature usage
- API calls

**Excludes**:
- Passive page loads
- Background sync

**Owner**: Product Team
```

#### Conversion Rate

```markdown
**Definition**: Percentage of visitors who complete a purchase.

**Calculation**: (Purchases / Unique Visitors) × 100%

**Time Window**: Session-based (30 min)

**Owner**: Marketing Team
```

## OKRs (Objectives and Key Results)

### Structure

```
Objective (Qualitative Goal)
  ├─ Key Result 1 (Measurable KPI)
  ├─ Key Result 2 (Measurable KPI)
  └─ Key Result 3 (Measurable KPI)
```

### Example: Improve Retention

```
Objective: Improve user retention and reduce churn

Key Results:
  KR1: Increase D30 retention from 20% to 30%
  KR2: Reduce churn rate from 5% to 3%
  KR3: Improve NPS from 40 to 50
```

### Example: Grow Revenue

```
Objective: Achieve $2M ARR by end of year

Key Results:
  KR1: Increase MRR from $125K to $167K
  KR2: Close 50 enterprise deals
  KR3: Reduce CAC from $50 to $40
```

## Pirate Metrics (AARRR)

### Framework

```
Acquisition ──▶ Activation ──▶ Retention ──▶ Referral ──▶ Revenue
```

### AARRR Metrics

| Stage | Metric | Description |
|-------|---------|-------------|
| **Acquisition** | Traffic, signups | How users find you |
| **Activation** | Activation rate | First experience |
| **Retention** | D1, D7, D30 | Users come back |
| **Referral** | Viral coefficient | Users tell others |
| **Revenue** | LTV, ARPU | Users pay |

### AARRR Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  AARRR Framework                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Acquisition                                                   │
│  ┌─────────────┐  ┌─────────────┐                           │
│  │ Traffic     │  │ Signups     │                           │
│  │ 100K        │  │ 10K         │                           │
│  │ ▲ 8%        │  │ ▲ 12%       │                           │
│  └─────────────┘  └─────────────┘                           │
│                                                                  │
│  Activation                                                   │
│  ┌─────────────┐                                           │
│  │ Activated   │                                           │
│  │ 4K (40%)   │                                           │
│  │ ▲ 5%        │                                           │
│  └─────────────┘                                           │
│                                                                  │
│  Retention                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ D1          │  │ D7          │  │ D30         │           │
│  │ 60%         │  │ 40%         │  │ 20%         │           │
│  │ ▲ 5%        │  │ ▲ 3%        │  │ ▲ 2%        │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                  │
│  Referral                                                    │
│  ┌─────────────┐                                           │
│  │ Viral Coef  │                                           │
│  │ 0.8         │                                           │
│  │ ▲ 0.1       │                                           │
│  └─────────────┘                                           │
│                                                                  │
│  Revenue                                                     │
│  ┌─────────────┐  ┌─────────────┐                           │
│  │ LTV         │  │ ARPU        │                           │
│  │ $300        │  │ $25         │                           │
│  │ ▲ $20        │  │ ▲ $2        │                           │
│  └─────────────┘  └─────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Real KPI Examples by Company Stage

### Startup (Pre-PMF)

**Focus**: User growth, activation

| KPI | Target |
|------|--------|
| User Growth | 20% MoM |
| Activation Rate | > 40% |
| NPS | > 40 |
| Time to Value | < 5 min |

### Growth Stage

**Focus**: Retention, LTV:CAC

| KPI | Target |
|------|--------|
| D30 Retention | > 30% |
| Churn Rate | < 5% |
| LTV:CAC | > 3:1 |
| MRR Growth | > 15% MoM |

### Mature Stage

**Focus**: Margin, efficiency

| KPI | Target |
|------|--------|
| Gross Margin | > 50% |
| Net Profit Margin | > 20% |
| Rule of 40 | > 40 |
| Customer Satisfaction | > 4.5/5 |

---

## Quick Start

### Define KPI

```markdown
# KPI: Monthly Recurring Revenue (MRR)

## Definition
Total predictable revenue generated from subscriptions per month

## Formula
MRR = Sum of all monthly subscription fees

## Target
$100,000 by end of Q2

## Measurement
- Tracked: Daily
- Reported: Weekly
- Reviewed: Monthly

## Owner
VP of Sales
```

### Track KPI

```javascript
// KPI tracking service
class KPITracker {
  async trackKPI(kpiId, value, timestamp) {
    await db.kpiMetrics.create({
      data: {
        kpiId,
        value,
        timestamp,
        period: 'monthly'
      }
    })
  }
  
  async getKPI(kpiId, period) {
    return await db.kpiMetrics.findMany({
      where: { kpiId, period },
      orderBy: { timestamp: 'desc' }
    })
  }
}
```

---

## Production Checklist

- [ ] **KPI Definition**: Clear definition and formula
- [ ] **Alignment**: Aligned with business goals
- [ ] **Measurability**: Can be measured accurately
- [ ] **Targets**: Realistic targets set
- [ ] **Tracking**: Automated tracking system
- [ ] **Reporting**: Regular reporting schedule
- [ ] **Dashboard**: KPI dashboard for visibility
- [ ] **Ownership**: Clear KPI ownership
- [ ] **Review**: Regular review and adjustment
- [ ] **Action**: Actionable insights from KPIs
- [ ] **Documentation**: Document KPI definitions
- [ ] **Updates**: Update KPIs as business evolves

---

## Anti-patterns

### ❌ Don't: Too Many KPIs

```markdown
# ❌ Bad - Too many KPIs
- KPI 1
- KPI 2
- KPI 3
# ... 50 more KPIs
```

```markdown
# ✅ Good - Focused KPIs
- Revenue (Primary)
- Customer Acquisition Cost (Primary)
- Customer Lifetime Value (Primary)
# 5-7 key KPIs maximum
```

### ❌ Don't: Vague Definitions

```markdown
# ❌ Bad - Vague
KPI: User Engagement
```

```markdown
# ✅ Good - Specific
KPI: Daily Active Users (DAU)
Definition: Number of unique users who open the app in a day
Formula: COUNT(DISTINCT user_id) WHERE date = today
```

### ❌ Don't: No Targets

```markdown
# ❌ Bad - No target
KPI: Revenue
Current: $50,000
```

```markdown
# ✅ Good - With target
KPI: Monthly Recurring Revenue
Current: $50,000
Target: $100,000 by Q2
Progress: 50%
```

---

## Integration Points

- **Dashboard Design** (`23-business-analytics/dashboard-design/`) - KPI visualization
- **Business Intelligence** (`23-business-analytics/business-intelligence/`) - BI tools
- **SQL for Analytics** (`23-business-analytics/sql-for-analytics/`) - KPI queries

---

## Further Reading

- [KPI Best Practices](https://www.klipfolio.com/resources/articles/what-is-a-key-performance-indicator-kpi)
- [OKR vs KPI](https://www.whatmatters.com/resources/okr-vs-kpi)
- [ ] Define clearly

### KPI Tracking

- [ ] Set up data collection
- [ ] Create dashboards
- [ ] Define update frequency
- [ ] Assign ownership
- [ ] Document definitions

### KPI Review

- [ ] Review regularly (weekly/monthly)
- [ ] Analyze trends
- [ ] Identify issues
- [ ] Take action
- [ ] Adjust targets as needed
