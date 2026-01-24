---
name: Dashboard Design
description: Creating visual displays of key metrics and data points that provide at-a-glance insights for monitoring, analysis, and data-driven decision-making.
---

# Dashboard Design

> **Current Level:** Intermediate  
> **Domain:** Business Analytics / Data Visualization

---

## Overview

A dashboard is a visual display of key metrics and data points that provides at-a-glance insights for monitoring, analysis, and decision-making. Effective dashboards present the right information at the right time, using appropriate visualizations and clear hierarchy to help users understand and act on data.

### Dashboard Purpose

| Purpose | Description |
|---------|-------------|
| **Monitoring** | Track real-time performance |
| **Analysis** | Explore data and find insights |
| **Reporting** | Share status with stakeholders |
| **Decision-making** | Support data-driven decisions |

### Dashboard Value

- **Save time**: Quick access to key information
- **Improve decisions**: Data-driven insights
- **Increase alignment**: Shared understanding

---

## Core Concepts
- **Enable action**: Identify issues and opportunities

## Dashboard Types

### 1. Strategic (Executive)

**Audience**: Executives, C-suite

**Characteristics**:
- High-level KPIs only (5-7 metrics)
- Monthly/quarterly updates
- Focus on trends and targets
- Simple, clean design

**Example Metrics**: Revenue, profit, market share, customer satisfaction

### 2. Operational

**Audience**: Managers, operators

**Characteristics**:
- Real-time or hourly updates
- Process-specific metrics
- Alert thresholds
- Drill-down capability

**Example Metrics**: Orders per hour, server uptime, queue length

### 3. Analytical

**Audience**: Analysts, data scientists

**Characteristics**:
- Deep exploration tools
- Many filters and dimensions
- Ad-hoc analysis
- Complex visualizations

**Example**: Cohort analysis, funnel analysis, segmentation

### 4. Tactical

**Audience**: Team leads, department heads

**Characteristics**:
- Department-specific metrics
- Daily/weekly updates
- Team performance tracking
- Action-oriented

**Example**: Sales pipeline, marketing campaign performance

## Dashboard Design Principles

### 1. Most Important First

Top-left is prime real estate.

```
┌─────────────────────────────────────────────────────────────────┐
│  [KPI 1]  [KPI 2]  [KPI 3]  [KPI 4]  ← Primary metrics    │
│                                                                  │
│  [Chart 1]           [Chart 2]  ← Secondary metrics           │
│                                                                  │
│  [Table/Detail]  ← Deep dive                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 2. Visual Hierarchy

Use size, color, and position to guide attention.

| Element | Hierarchy |
|----------|-----------|
| Primary KPIs | Largest, top-left |
| Secondary charts | Medium, below |
| Detail tables | Smallest, bottom |

### 3. Consistent Layout

Grid-based design for consistency.

```
┌───────┬───────┬───────┬───────┐
│ KPI 1 │ KPI 2 │ KPI 3 │ KPI 4 │
├───────┼───────┼───────┼───────┤
│ Chart 1      │ Chart 2      │
├───────┼───────┼───────┼───────┤
│ Chart 3      │ Chart 4      │
├───────┴───────┴───────┴───────┤
│ Detail Table                   │
└────────────────────────────────┘
```

### 4. White Space

Don't clutter. Use whitespace effectively.

**Good**: Spacing between elements
**Bad**: Everything packed together

### 5. Actionable Insights

Not just numbers, but insights.

| Bad | Good |
|-----|------|
| "Revenue: $100K" | "Revenue: $100K ▲ 12% vs last month" |
| "Conversion: 2%" | "Conversion: 2% ▼ 0.5% (below target)" |

## Chart Selection

### Chart Type Guide

| Chart Type | Best For | Example |
|------------|----------|---------|
| **Line Chart** | Trends over time | Revenue over months |
| **Bar Chart** | Compare categories | Sales by region |
| **Pie Chart** | Parts of whole (max 5 slices) | Market share |
| **Table** | Detailed data, exact values | Transaction list |
| **KPI Card** | Single important number | Total revenue |
| **Heatmap** | Two dimensions | Sales by region × month |
| **Scatter Plot** | Correlation | Price vs. quantity |
| **Histogram** | Distribution | Order value distribution |

### When to Use Each Chart

#### Line Chart

**Use for**: Time series data

```
Revenue ($)
$100k ┤
 $80k ┤  ●───●───●───●───●
 $60k ┤
 $40k ┤
 $20k ┤
   $0 └────────────────────────────
        Jan  Feb  Mar  Apr  May
```

**Best practices**:
- Smooth curves for trends
- Don't connect unrelated points
- Use area charts for cumulative data

#### Bar Chart

**Use for**: Category comparison

```
Sales by Region
North America  ████████████████████████████████████████  $50M
Europe         ████████████████████████████              $35M
Asia           ████████████████████                      $25M
Other          ████████████                              $10M
               0    10M   20M   30M   40M   50M
```

**Best practices**:
- Horizontal bars for many categories
- Sort by value (not alphabetically)
- Start Y-axis at zero

#### Pie Chart

**Use for**: Parts of whole (max 5 slices)

```
Market Share
Product A  ████████████████████████████████████████  50%
Product B  ████████████████████                      25%
Product C  ████████████████████                      25%
```

**Best practices**:
- Max 5 slices
- Use donut chart for modern look
- Consider bar chart instead (easier to compare)

#### KPI Card

**Use for**: Single important metric

```
┌─────────────────────────────────────┐
│  Total Revenue                      │
│  $1,234,567                        │
│  ─────────────────────────────────  │
│  ▲ 12.3% vs last month              │
│  ─────────────────────────────────  │
│  ▂▃▅▇█▇▅▃▂ (sparkline)             │
└─────────────────────────────────────┘
```

**Best practices**:
- Big number
- Context (vs previous period)
- Sparkline for trend
- Color indicator (red/yellow/green)

#### Heatmap

**Use for**: Two-dimensional data

```
Sales by Region × Month
         Jan   Feb   Mar   Apr
US      ■■■■■ ■■■■■ ■■■■■ ■■■■■
EU      ■■■■  ■■■■  ■■■■  ■■■■
Asia    ■■■   ■■■   ■■■   ■■■
```

**Best practices**:
- Use color scale
- Include legend
- Label both axes

#### Scatter Plot

**Use for**: Correlation between variables

```
Quantity
100 ┤     ●
     │   ●   ●
 50 ┤ ●   ●   ●
     │ ●   ●   ●
  0 └────────────────────
     0   50  100  150
          Price
```

**Best practices**:
- Add trend line
- Color by category
- Identify outliers

## Color Usage

### Color Principles

| Principle | Description |
|-----------|-------------|
| **Limit palette** | 3-5 colors max |
| **Semantic colors** | Red=bad, green=good, yellow=warning |
| **Colorblind-friendly** | Avoid red-green only |
| **Consistent** | Same color = same meaning |
| **Use saturation** | Darker = more emphasis |

### Semantic Colors

| Color | Meaning | Use Case |
|-------|---------|----------|
| **Green** | Good, positive | Above target, growth |
| **Red** | Bad, negative | Below target, decline |
| **Yellow/Orange** | Warning | Near threshold |
| **Blue** | Neutral | Information |
| **Gray** | Inactive | Disabled, placeholder |

### Colorblind-Friendly Palettes

**Viridis** (colorblind-safe):
```
#440154 → #3b528b → #21918c → #5ec962 → #fde725
```

**ColorBrewer** (safe palettes):
- Set1: #e41a1c, #377eb8, #4daf4a, #984ea3, #ff7f00
- Set2: #66c2a5, #fc8d62, #8da0cb, #e78ac3, #a6d854

## KPI Design

### KPI Card Components

```
┌─────────────────────────────────────┐
│  [Label]                          │  ← Metric name
│  [Value]                          │  ← Big number
│  [Context]                        │  ← Comparison
│  [Sparkline]                      │  ← Mini trend
│  [Indicator]                      │  ← Color
└─────────────────────────────────────┘
```

### KPI Examples

#### Simple KPI

```
┌─────────────────────────────────────┐
│  Revenue                          │
│  $1,234,567                       │
│  ▲ 12.3% vs last month            │
└─────────────────────────────────────┘
```

#### KPI with Sparkline

```
┌─────────────────────────────────────┐
│  Active Users                      │
│  12,345                           │
│  ▲ 8.2% vs last week              │
│  ▂▃▅▇█▇▅▃▂                        │
└─────────────────────────────────────┘
```

#### KPI with Target

```
┌─────────────────────────────────────┐
│  Conversion Rate                  │
│  2.5%                            │
│  Target: 3.0%                     │
│  ████████████░░░░░░░░░░░░░░░░  83% │
└─────────────────────────────────────┘
```

### KPI Best Practices

| Practice | Why |
|----------|-----|
| Big number | Easy to read |
| Context | Comparison gives meaning |
| Sparkline | Shows trend |
| Color indicator | Quick status |
| Target line | Shows progress |

## Layout Principles

### F-Pattern (Western Reading)

```
┌─────────────────────────────────────┐
│  [Primary]  [Primary]  [Primary]  │  ← Eye starts here
│                                  │
│  [Secondary]    [Secondary]       │  ← Scan down
│                                  │
│  [Detail]                        │  ← Finish
└─────────────────────────────────────┘
```

### Z-Pattern

```
┌─────────────────────────────────────┐
│  [Primary] ─────────────────▶ [Primary] │
│                              │       │
│                              ▼       │
│                        [Secondary]     │
│                              │       │
│  [Detail] ◀──────────────────┘       │
└─────────────────────────────────────┘
```

### Responsive Layout

**Desktop**: Side-by-side charts
**Mobile**: Stacked charts

```
Desktop:          Mobile:
┌─────┬─────┐    ┌─────┐
│  A  │  B  │    │  A  │
├─────┼─────┤    ├─────┤
│  C  │  D  │    │  B  │
└─────┴─────┘    ├─────┤
                 │  C  │
                 ├─────┤
                 │  D  │
                 └─────┘
```

## Interactivity

### Interactive Features

| Feature | Description | Use Case |
|---------|-------------|----------|
| **Filters** | Date range, category | Narrow down data |
| **Drill-down** | Click for details | Explore deeper |
| **Tooltips** | Hover for context | Show details |
| **Cross-filtering** | Select in one, filter others | Related analysis |
| **Export** | PDF, CSV, image | Share data |

### Filter Design

```
┌─────────────────────────────────────┐
│  Filters                          │
│  ┌─────────────────────────────┐   │
│  │ Date Range: [Last 30 days ▼]│   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ Region: [All ▼]            │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ Product: [All ▼]           │   │
│  └─────────────────────────────┘   │
│  [Apply] [Reset]                 │
└─────────────────────────────────────┘
```

### Tooltip Example

```
Hover on data point:
┌─────────────────────────────────────┐
│  January 2024                     │
│  ───────────────────────────────  │
│  Revenue: $1,234,567             │
│  Orders: 1,234                   │
│  AOV: $1,000                     │
│  ▲ 12.3% vs previous month       │
└─────────────────────────────────────┘
```

## User Personas

### Executive

**Needs**:
- High-level overview
- Few metrics (5-7)
- Trends and targets
- Simple visualizations

**Don't show**:
- Detailed tables
- Complex charts
- Technical jargon

### Manager

**Needs**:
- Departmental metrics
- Moderate detail (10-15 metrics)
- Team performance
- Actionable insights

### Analyst

**Needs**:
- All data available
- Many filters
- Complex analysis
- Export capability

### Operator

**Needs**:
- Real-time data
- Alerts and thresholds
- Specific operational metrics
- Quick status checks

## Dashboard Types by Role

### Sales Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  Sales Dashboard                                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ Pipeline    │  │ Revenue     │  │ Conversion  │           │
│  │ $5,000,000  │  │ $1,234,567  │  │   25%       │           │
│  │ ▲ 10%       │  │ ▲ 12%       │  │ ▲ 2%        │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                  │
│  Pipeline by Stage                                               │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Qualified  ████████████████████████████████████████  $2M   │ │
│  │ Proposal   ████████████████████████████              $1.5M │ │
│  │ Negotiation███████████████████████                      $1M │ │
│  │ Closed Won ████████████████████████████████████████  $0.5M │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Top Deals                                                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Deal          │ Value    │ Stage    │ Owner    │ Close    │ │
│  ├───────────────┼──────────┼──────────┼──────────┼─────────┤ │
│  │ Enterprise Co │ $500K    │ Negot.   │ John D.  │ Mar 15  │ │
│  │ Tech Corp     │ $250K    │ Proposal │ Jane S.  │ Apr 01  │ │
│  │ Global Inc    │ $200K    │ Qual.    │ Mike R.  │ Apr 15  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Marketing Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  Marketing Dashboard                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ Traffic     │  │ Leads       │  │ CAC         │           │
│  │ 123,456     │  │   1,234     │  │    $45       │           │
│  │ ▲ 8%        │  │ ▲ 12%       │  │ ▼ 5%        │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                  │
│  Traffic by Channel                                              │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Organic    ████████████████████████████████████████  50K   │ │
│  │ Paid      ████████████████████████████              40K   │ │
│  │ Social    ████████████████████                         20K   │
│  │ Email    ████████████                                 10K   │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  Campaign Performance                                            │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Campaign   │ Spend   │ Impressions│ Clicks  │ CTR   │ Conv │ │
│  ├───────────┼─────────┼───────────┼─────────┼───────┼──────┤ │
│  │ Spring Sale│ $10,000 │ 100,000   │  5,000  │  5%   │ 250  │ │
│  │ Branding   │ $5,000  │  50,000   │  1,000  │  2%   │  50  │ │
│  │ Retargeting│ $2,000  │  10,000   │  2,000  │ 20%   │ 100  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Product Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  Product Dashboard                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ DAU         │  │ Retention   │  │ NPS         │           │
│  │ 12,345      │  │   45%       │  │   +42       │           │
│  │ ▲ 5%        │  │ ▲ 2%        │  │ ▲ 3         │           │
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
│  Feature Adoption                                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Feature A  ████████████████████████████████████████  80%   │ │
│  │ Feature B  ████████████████████████████              60%   │ │
│  │ Feature C  ████████████████████                         40%   │ │
│  │ Feature D  ████████████                                 20%   │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Storytelling with Data

### Narrative Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  [Headline: Key Insight]                                      │
│  ─────────────────────────────────────────────────────────────── │
│                                                                  │
│  [What happened]                                                │
│  Revenue increased by 12% to $1.2M in Q1, driven by            │
│  strong performance in North America.                             │
│                                                                  │
│  [Why it happened]                                              │
│  New product launch in January and successful marketing           │
│  campaign contributed to growth.                                 │
│                                                                  │
│  [What to do]                                                   │
│  Continue investment in North America and replicate               │
│  successful tactics in other regions.                            │
│                                                                  │
│  [Supporting Charts]                                            │
│  ┌─────────────┐  ┌─────────────┐                           │
│  │ Revenue     │  │ By Region   │                           │
│  │ Trend       │  │ Breakdown   │                           │
│  └─────────────┘  └─────────────┘                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Annotation Best Practices

| Practice | Example |
|----------|---------|
| Mark important events | "Product launch: Jan 15" |
| Explain anomalies | "Server outage: Feb 1-3" |
| Show targets | "Target: $1.5M" |
| Highlight changes | "New pricing: Mar 1" |

### Comparison Types

| Comparison | Example |
|------------|---------|
| **vs Previous Period** | "▲ 12% vs last month" |
| **vs Target** | "85% of target" |
| **vs Benchmark** | "Above industry avg" |
| **vs Competitor** | "Market leader" |

## Dashboard Performance

### Optimization Techniques

| Technique | Impact |
|------------|--------|
| **Pre-aggregation** | 10-100x faster |
| **Materialized views** | 5-50x faster |
| **Query optimization** | 2-10x faster |
| **Caching** | 10-1000x faster |
| **Incremental refresh** | 2-5x faster |

### Materialized View Example

```sql
CREATE MATERIALIZED VIEW mv_daily_revenue AS
SELECT
    DATE(order_date) AS date,
    SUM(revenue) AS total_revenue,
    COUNT(*) AS order_count
FROM orders
GROUP BY DATE(order_date);

-- Refresh
REFRESH MATERIALIZED VIEW mv_daily_revenue;

-- Query (fast)
SELECT * FROM mv_daily_revenue WHERE date >= '2024-01-01';
```

### Caching Strategy

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Dashboard  │────▶│   Cache     │────▶│  Database  │
│  Request    │     │  (Redis)    │     │  (Slow)    │
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │
       │                    │
       └────────────────────┘
              Fast response
```

## Mobile Dashboards

### Mobile Design Principles

| Principle | Implementation |
|-----------|----------------|
| **Vertical layout** | Stack charts vertically |
| **Touch-friendly** | Large buttons (44×44px min) |
| **Simplified** | Fewer metrics |
| **Fast loading** | Optimize images, lazy load |

### Mobile Layout Example

```
┌─────────────────────────────────────┐
│  ☰  Dashboard                    │
├─────────────────────────────────────┤
│  ┌─────────────────────────────┐   │
│  │ Revenue                    │   │
│  │ $1,234,567 ▲ 12%         │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ Active Users               │   │
│  │ 12,345 ▲ 5%              │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ Conversion Rate            │   │
│  │ 2.5% ▲ 0.5%             │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ Revenue Trend             │   │
│  │ [Line Chart]              │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │ [View Full Dashboard]      │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Dashboard Anti-Patterns

### Common Mistakes

| Anti-Pattern | Why Bad | Fix |
|--------------|----------|-----|
| **Too many metrics** | Information overload | Focus on 5-7 key metrics |
| **Misleading charts** | Truncated axis, 3D | Start Y at 0, use 2D |
| **No context** | Just numbers, no comparison | Add vs. previous period |
| **Vanity metrics** | Impressive but not actionable | Focus on actionable metrics |
| **Pie charts with 10+ slices** | Hard to compare | Use bar chart |
| **Rainbow colors** | No meaning | Use semantic colors |
| **Small fonts** | Hard to read | Use readable size (12px+) |

### Before/After Example

**Before** (Bad):
```
┌─────────────────────────────────────┐
│  Dashboard                        │
│  ┌───┬───┬───┬───┬───┬───┬───┐ │
│  │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ │  ← Too many metrics
│  ├───┼───┼───┼───┼───┼───┼───┤ │
│  │ 8 │ 9 │10 │11 │12 │13 │14 │ │
│  └───┴───┴───┴───┴───┴───┴───┘ │
│  [Pie chart with 10 slices]      │  ← Hard to read
└─────────────────────────────────────┘
```

**After** (Good):
```
┌─────────────────────────────────────┐
│  Dashboard                        │
│  ┌─────────────┐  ┌─────────────┐ │
│  │ Revenue    │  │ Users       │ │  ← Key metrics
│  │ $1.2M ▲12% │  │ 12K ▲5%     │ │
│  └─────────────┘  └─────────────┘ │
│  ┌─────────────────────────────┐   │
│  │ Revenue Trend             │   │
│  │ [Line chart]              │   │  ← Clear visualization
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

## Data Visualization Best Practices

### Direct Labeling

**Bad** (legend):
```
[Chart]
Legend: Blue = A, Red = B
```

**Good** (direct labels):
```
[Chart with labels on chart]
  Series A ●───●───●
  Series B ●───●───●
```

### Start Y-Axis at Zero

**Bad** (truncated):
```
$100k ┤  ●
 $98k ┤
 $96k ┤  ●
 $94k ┤
       └────────
```

**Good** (starts at zero):
```
$100k ┤  ●
 $50k ┤
   $0 ┤  ●
       └────────
```

### Sort by Value

**Bad** (alphabetical):
```
Zebra    ████████
Apple    ████████████████
Banana   ████████████
```

**Good** (by value):
```
Apple    ████████████████
Banana   ████████████
Zebra    ████████
```

### Show Uncertainty

**Good** (with confidence interval):
```
Revenue
$100k ┤
 $80k ┤  ●───●───●
 $60k ┤      └─┬─┘
 $40k ┤       CI
       └────────
```

### Remove Chart Junk

**Bad** (cluttered):
```
[Chart with grid, borders, 3D effects, shadows]
```

**Good** (clean):
```
[Clean chart with minimal decoration]
```

## Dashboard Development Process

### Step 1: Understand Audience and Goals

**Questions to ask**:
- Who is the dashboard for?
- What questions do they need to answer?
- What decisions will they make?
- How often will they use it?

### Step 2: Identify Key Metrics

**Criteria**:
- Actionable
- Measurable
- Relevant to goals
- Limited to 5-7 metrics

### Step 3: Sketch Layout

**Wireframe**:
```
┌─────────────────────────────────────┐
│  [KPI 1]  [KPI 2]  [KPI 3]    │
│                                  │
│  [Chart 1]      [Chart 2]        │
│                                  │
│  [Table/Detail]                  │
└─────────────────────────────────────┘
```

### Step 4: Build and Iterate

**Process**:
1. Build MVP dashboard
2. Get user feedback
3. Iterate based on feedback
4. Repeat

### Step 5: Test Usability

**Test questions**:
- Can users find what they need?
- Is the dashboard intuitive?
- Are there any confusion points?
- Is the performance acceptable?

### Step 6: Deploy and Monitor

**Post-launch**:
- Monitor usage analytics
- Track which charts are used
- Gather ongoing feedback
- Update regularly

## Tools

### BI Tools

| Tool | Strengths | Pricing |
|------|-----------|---------|
| **Tableau** | Powerful visualizations | $$$ |
| **Looker** | SQL-based, embedded | $$$ |
| **Power BI** | Microsoft ecosystem | $$ |
| **Metabase** | Open-source, simple | Free/$ |
| **Grafana** | Monitoring, time-series | Free |

### Custom (React + Recharts/Chart.js)

```javascript
import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const Dashboard = ({ data }) => (
  <div className="dashboard">
    <div className="kpi-cards">
      <KPICard title="Revenue" value="$1,234,567" change="+12%" />
      <KPICard title="Users" value="12,345" change="+5%" />
      <KPICard title="Conversion" value="2.5%" change="+0.5%" />
    </div>

    <div className="charts">
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="date" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="revenue" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  </div>
);
```

## Dashboard Maintenance

### Maintenance Tasks

| Task | Frequency |
|------|-----------|
| **Data quality check** | Daily |
| **Broken chart alerts** | Daily |
| **Usage analytics review** | Weekly |
| **User feedback review** | Weekly |
| **Update metrics** | Monthly |
| **Remove unused charts** | Quarterly |

### Usage Analytics

Track:
- Which dashboards are used most
- Which charts are viewed
- How long users spend
- What filters are applied

### User Feedback Loop

**Methods**:
- In-app feedback button
- Regular user interviews
- Quarterly surveys
- Office hours with users

## Real Dashboard Examples

### SaaS Metrics Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  SaaS Metrics Dashboard                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ MRR         │  │ ARR         │  │ Churn       │           │
│  │ $125,000    │  │ $1,500,000  │  │ 2.5%        │           │
│  │ ▲ 8.2%      │  │ ▲ 10.1%     │  │ ▼ 0.3%      │           │
│  └─────────────┘  └─────────────┘  └─────────────┘           │
│                                                                  │
│  MRR Trend                                                      │
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
│  Churn by Plan                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Enterprise  ████████████████████████████████████████  1.2%  │ │
│  │ Business   ████████████████████████████████████████  2.8%  │ │
│  │ Starter    ████████████████████████████████████████  4.5%  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### E-commerce Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  E-commerce Dashboard                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ Revenue     │  │ Orders      │  │ AOV         │           │
│  │ $45,234     │  │   1,234     │  │   $36.67    │           │
│  │ ▲ 12.3%     │  │ ▲ 8.5%      │  │ ▲ 3.2%      │           │
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
│  Top Products                                                    │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Product          │  Sales  │  Revenue  │  Growth           │ │
│  ├─────────────────┼─────────┼──────────┼───────────────────┤ │
│  │ Wireless Mouse   │   234   │  $4,680   │  ▲ 15.3%          │ │
│  │ USB-C Cable      │   189   │  $1,890   │  ▲ 8.7%           │ │
│  │ Laptop Stand     │   156   │  $3,120   │  ▲ 22.1%          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Summary Checklist

### Design Phase

- [ ] Understand audience and goals
- [ ] Identify key metrics (5-7)
- [ ] Choose appropriate charts
- [ ] Design layout (wireframe)
- [ ] Select color palette

### Build Phase

- [ ] Implement dashboard
- [ ] Add interactivity
- [ ] Test with users
- [ ] Iterate based on feedback
```

---

## Quick Start

### Basic Dashboard Layout

```typescript
// Dashboard component structure
const Dashboard = () => {
  return (
    <div className="dashboard">
      {/* Header */}
      <header>
        <h1>Dashboard</h1>
        <DateRangePicker />
      </header>
      
      {/* Key Metrics Row */}
      <div className="metrics-row">
        <MetricCard title="Revenue" value="$12,345" trend="+5%" />
        <MetricCard title="Users" value="1,234" trend="+12%" />
        <MetricCard title="Orders" value="567" trend="-3%" />
      </div>
      
      {/* Charts */}
      <div className="charts-grid">
        <Chart type="line" data={revenueData} />
        <Chart type="bar" data={userData} />
      </div>
    </div>
  )
}
```

### Key Metrics Selection

```markdown
# Dashboard Metrics Selection

## Process
1. Identify business goals
2. Map goals to metrics
3. Prioritize metrics (5-7 max)
4. Choose visualization type
5. Design layout
```

---

## Production Checklist

- [ ] **Audience**: Understand dashboard audience and their needs
- [ ] **Metrics**: Select 5-7 key metrics (not too many)
- [ ] **Visualization**: Choose appropriate chart types
- [ ] **Layout**: Design clear visual hierarchy
- [ ] **Interactivity**: Add filters, drill-downs, date ranges
- [ ] **Performance**: Optimize for fast loading
- [ ] **Responsive**: Works on mobile and desktop
- [ ] **Accessibility**: Accessible to all users
- [ ] **Real-time**: Update data appropriately
- [ ] **Documentation**: Document metric definitions
- [ ] **Testing**: Test with real users
- [ ] **Iteration**: Iterate based on usage data

---

## Anti-patterns

### ❌ Don't: Too Many Metrics

```typescript
// ❌ Bad - Information overload
<Dashboard>
  <MetricCard title="Metric 1" />
  <MetricCard title="Metric 2" />
  // ... 20 more metrics
</Dashboard>
```

```typescript
// ✅ Good - Focused metrics
<Dashboard>
  <MetricCard title="Revenue" />      // Top priority
  <MetricCard title="Users" />        // Top priority
  <MetricCard title="Orders" />       // Top priority
  // Only 5-7 key metrics
</Dashboard>
```

### ❌ Don't: Wrong Chart Type

```typescript
// ❌ Bad - Line chart for categories
<LineChart data={categories} />  // Categories don't have trends
```

```typescript
// ✅ Good - Bar chart for categories
<BarChart data={categories} />  // Better for comparing categories
```

### ❌ Don't: No Context

```typescript
// ❌ Bad - Just numbers
<MetricCard value="1234" />
```

```typescript
// ✅ Good - With context
<MetricCard 
  title="Active Users"
  value="1,234"
  trend="+12%"
  period="vs last month"
/>
```

---

## Integration Points

- **Data Visualization** (`23-business-analytics/data-visualization/`) - Chart types
- **KPI Metrics** (`23-business-analytics/kpi-metrics/`) - Metric selection
- **SQL for Analytics** (`23-business-analytics/sql-for-analytics/`) - Data queries

---

## Further Reading

- [Dashboard Design Best Practices](https://www.tableau.com/learn/articles/dashboards)
- [Information Dashboard Design](https://www.edwardtufte.com/)
- [Data Visualization Guide](https://www.d3js.org/)
- [ ] Optimize performance
- [ ] Test on multiple devices

### Launch Phase

- [ ] User acceptance testing
- [ ] Documentation
- [ ] Training
- [ ] Deploy to production

### Maintenance Phase

- [ ] Monitor data quality
- [ ] Track usage analytics
- [ ] Gather feedback
- [ ] Update regularly
- [ ] Remove unused elements
