---
name: Funnel Analysis
description: Tracking user journeys through sequential steps to identify where users drop off and optimize conversion at each stage using funnel visualization and drop-off analysis.
---

# Funnel Analysis

> **Current Level:** Intermediate  
> **Domain:** Business Analytics / User Experience

---

## Overview

Funnel analysis is the process of tracking user journeys through sequential steps to identify where users drop off and optimize conversion at each stage. Effective funnel analysis helps identify bottlenecks, optimize user flows, and improve overall conversion rates.

## What is Funnel Analysis

### Core Concept

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Step 1   │───▶│   Step 2   │───▶│   Step 3   │───▶│   Step 4   │
│  (Entry)   │    │ (Progress)  │    │ (Progress)  │    │ (Complete)  │
│  10,000     │    │   5,000     │    │   2,500     │    │    500      │
│  (100%)     │    │   (50%)     │    │   (25%)     │    │   (5%)     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Why Funnel Analysis Matters

| Benefit | Description |
|---------|-------------|
| **Identify bottlenecks** | Find biggest drop-offs |
| **Measure conversion** | Track overall performance |
| **Optimize stages** | Improve each step |
| **Compare segments** | Find high-performing groups |
| **A/B test impact** | Measure test effectiveness |

## Types of Funnels

### 1. Linear Funnel

Users must complete steps in order.

```
Visit → Product View → Add to Cart → Checkout → Purchase
```

**Use case**: Standard e-commerce flow

### 2. Non-Linear Funnel

Users can skip or revisit steps.

```
Visit → Browse → Product View → Reviews → Add to Cart → Checkout → Purchase
         ↑_____________|←__________________|
```

**Use case**: Complex user journeys

### 3. Time-Bound Funnel

Users must complete within time window.

```
Visit → Add to Cart → Purchase (within 24 hours)
```

**Use case**: Flash sales, limited offers

### 4. Open Funnel

Users can enter at any step.

```
Product View → Add to Cart → Checkout → Purchase
     ↑______________|←_____________________|
```

**Use case**: Users arriving via product links

## Common Funnels

### E-commerce Purchase Funnel

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Visit    │───▶│Product View│───▶│ Add to Cart│───▶│  Checkout  │───▶│  Purchase   │
│  100,000    │    │   50,000    │    │   10,000    │    │   5,000     │    │    500      │
│  (100%)     │    │   (50%)     │    │   (10%)     │    │   (5%)      │    │   (0.5%)    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Overall conversion**: 0.5% (500/100,000)

### SaaS Signup Funnel

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Landing   │───▶│   Signup    │───▶│ Verify Email│───▶│  Activate   │───▶│  Upgrade    │
│   Page     │    │    Form     │    │             │    │             │    │             │
│  10,000     │    │   5,000     │    │   4,000     │    │   2,000     │    │    200      │
│  (100%)     │    │   (50%)     │    │   (40%)     │    │   (20%)     │    │   (2%)      │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Overall conversion**: 2% (200/10,000)

### App Install Funnel

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   App Store │───▶│   Install   │───▶│   Open     │───▶│   Sign Up   │───▶│  First Use  │
│   Page     │    │             │    │             │    │             │    │             │
│  50,000     │    │   25,000    │    │   15,000    │    │   10,000    │    │   5,000     │
│  (100%)     │    │   (50%)     │    │   (30%)     │    │   (20%)     │    │   (10%)     │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Overall conversion**: 10% (5,000/50,000)

## Funnel Metrics

### Conversion Rate

```
Conversion Rate = (Users at Step N+1 / Users at Step N) × 100%
```

**Example**:
- Step 1: 10,000 users
- Step 2: 5,000 users
- Conversion: 50%

### Overall Conversion

```
Overall Conversion = (Users at Final Step / Users at First Step) × 100%
```

**Example**:
- First step: 10,000 users
- Final step: 500 users
- Overall conversion: 5%

### Drop-off Rate

```
Drop-off Rate = ((Users at Step N - Users at Step N+1) / Users at Step N) × 100%
```

**Example**:
- Step 1: 10,000 users
- Step 2: 5,000 users
- Drop-off: 50%

### Time to Convert

```
Median Time = Median(Time from Step 1 to Final Step)
```

**Example**:
- Users take median 3 days to complete funnel

## Funnel SQL

### Basic Funnel Query

```sql
WITH funnel_steps AS (
    -- Step 1: Visit
    SELECT
        session_id,
        'visit' AS step,
        1 AS step_number,
        MIN(timestamp) AS step_time
    FROM page_views
    WHERE page_url = '/'
    GROUP BY session_id

    UNION ALL

    -- Step 2: Product View
    SELECT
        session_id,
        'product_view' AS step,
        2 AS step_number,
        MIN(timestamp) AS step_time
    FROM page_views
    WHERE page_url LIKE '/product/%'
    GROUP BY session_id

    UNION ALL

    -- Step 3: Add to Cart
    SELECT
        session_id,
        'add_to_cart' AS step,
        3 AS step_number,
        MIN(timestamp) AS step_time
    FROM events
    WHERE event_type = 'add_to_cart'
    GROUP BY session_id

    UNION ALL

    -- Step 4: Purchase
    SELECT
        session_id,
        'purchase' AS step,
        4 AS step_number,
        MIN(timestamp) AS step_time
    FROM events
    WHERE event_type = 'purchase'
    GROUP BY session_id
),

funnel_counts AS (
    SELECT
        step_number,
        step,
        COUNT(DISTINCT session_id) AS users
    FROM funnel_steps
    GROUP BY step_number, step
)

SELECT
    step_number,
    step,
    users,
    LAG(users) OVER (ORDER BY step_number) AS previous_users,
    ROUND(100.0 * users / LAG(users) OVER (ORDER BY step_number), 2) AS conversion_rate,
    ROUND(100.0 * (LAG(users) OVER (ORDER BY step_number) - users) /
          LAG(users) OVER (ORDER BY step_number), 2) AS drop_off_rate
FROM funnel_counts
ORDER BY step_number;
```

### Time-Bound Funnel Query

```sql
WITH funnel_steps AS (
    SELECT
        session_id,
        'visit' AS step,
        1 AS step_number,
        MIN(timestamp) AS step_time
    FROM page_views
    WHERE page_url = '/'
    GROUP BY session_id

    UNION ALL

    SELECT
        session_id,
        'purchase' AS step,
        2 AS step_number,
        MIN(timestamp) AS step_time
    FROM events
    WHERE event_type = 'purchase'
    GROUP BY session_id
),

user_funnels AS (
    SELECT
        session_id,
        MAX(CASE WHEN step_number = 1 THEN step_time END) AS visit_time,
        MAX(CASE WHEN step_number = 2 THEN step_time END) AS purchase_time
    FROM funnel_steps
    GROUP BY session_id
)

SELECT
    COUNT(*) AS total_visits,
    COUNT(CASE WHEN purchase_time IS NOT NULL THEN 1 END) AS purchases,
    ROUND(100.0 * COUNT(CASE WHEN purchase_time IS NOT NULL THEN 1 END) /
          COUNT(*), 2) AS conversion_rate
FROM user_funnels
WHERE purchase_time IS NULL
   OR (purchase_time - visit_time) <= INTERVAL '24 hours';
```

### Segmented Funnel Query

```sql
WITH funnel_steps AS (
    SELECT
        session_id,
        'visit' AS step,
        1 AS step_number,
        device_type
    FROM page_views
    WHERE page_url = '/'
    GROUP BY session_id, device_type

    UNION ALL

    SELECT
        session_id,
        'purchase' AS step,
        2 AS step_number,
        device_type
    FROM events e
    JOIN page_views pv ON e.session_id = pv.session_id
    WHERE e.event_type = 'purchase'
    GROUP BY session_id, device_type
),

funnel_counts AS (
    SELECT
        step_number,
        step,
        device_type,
        COUNT(DISTINCT session_id) AS users
    FROM funnel_steps
    GROUP BY step_number, step, device_type
)

SELECT
    device_type,
    step_number,
    step,
    users,
    LAG(users) OVER (PARTITION BY device_type ORDER BY step_number) AS previous_users,
    ROUND(100.0 * users / LAG(users) OVER (PARTITION BY device_type ORDER BY step_number), 2) AS conversion_rate
FROM funnel_counts
ORDER BY device_type, step_number;
```

## Funnel Visualization

### Traditional Funnel Chart

```
                    ┌─────────────┐
                    │   Visit     │
                    │  10,000    │
                    │  (100%)     │
                    └──────┬──────┘
                           │
                    ┌────────┴────────┐
                    │   Product     │
                    │    View       │
                    │   5,000      │
                    │   (50%)      │
                    └──────┬───────┘
                           │
                    ┌────────┴────────┐
                    │  Add to Cart  │
                    │   10,000      │
                    │   (10%)      │
                    └──────┬───────┘
                           │
                    ┌────────┴────────┐
                    │   Purchase    │
                    │    500       │
                    │   (0.5%)     │
                    └───────────────┘
```

### Sankey Diagram

```
Visit (10,000) ───────────────────────────────────────┐
                                                  │
                                                  ▼
                                         Product View (5,000) ─────┐
                                                  │              │
                                                  ▼              │
                                         Add to Cart (1,000) ───┤
                                                  │              │
                                                  ▼              ▼
                                         Purchase (500)  Abandon (500)
```

### Bar Chart (Users per Step)

```
Users
10,000 ┤  ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
 8,000 ┤
 6,000 ┤
 4,000 ┤
 2,000 ┤
    0 └──────────────────────────────────────────────────────
        Visit    Product  Add to   Checkout  Purchase
                  View     Cart
```

## Funnel Optimization

### 1. Identify Bottlenecks

Find biggest drop-offs.

```
Step        Users    Drop-off   Priority
─────────────────────────────────────────
Visit       10,000    -          -
Product      5,000     50%        High
Add to Cart 1,000     80%        Critical
Checkout    500       50%        High
Purchase    500       -          -
```

**Priority**: Fix Add to Cart → Checkout (80% drop-off)

### 2. A/B Test Improvements

Test changes to improve conversion.

| Stage | Hypothesis | Test |
|-------|------------|------|
| Product View | Better images increase conversion | A: Current vs B: High-quality images |
| Add to Cart | Clearer CTA increases clicks | A: "Add" vs B: "Add to Cart Now" |
| Checkout | Fewer fields reduce abandonment | A: 5 fields vs B: 3 fields |

### 3. Remove Friction

Reduce steps and effort.

| Friction Point | Solution |
|----------------|-----------|
| Too many form fields | Reduce to essential |
| Slow page load | Optimize performance |
| Unclear CTAs | Make action obvious |
| No trust signals | Add reviews, badges |

## Segmented Funnels

### By Device

```
Device    Visit    Product  Cart    Checkout  Purchase
─────────────────────────────────────────────────────
Mobile    6,000    2,500    400     200       100
Desktop   4,000    2,500    600     300       400
```

**Insight**: Desktop converts better (10% vs 1.7%)

### By Acquisition Channel

```
Channel   Visit    Product  Cart    Checkout  Purchase
─────────────────────────────────────────────────────
Organic   5,000    3,000    600     300       150
Paid      3,000    1,500    300     150       300
Social    2,000    500      100     50        50
```

**Insight**: Paid has higher conversion but lower traffic

### By User Type

```
Type      Visit    Product  Cart    Checkout  Purchase
─────────────────────────────────────────────────────
New       7,000    2,500    400     200       100
Returning 3,000    2,500    600     300       400
```

**Insight**: Returning users convert better (13% vs 1.4%)

## Time-to-Convert Analysis

### Median Time Between Steps

```sql
WITH step_times AS (
    SELECT
        session_id,
        MIN(CASE WHEN step = 'visit' THEN timestamp END) AS visit_time,
        MIN(CASE WHEN step = 'product_view' THEN timestamp END) AS product_time,
        MIN(CASE WHEN step = 'add_to_cart' THEN timestamp END) AS cart_time,
        MIN(CASE WHEN step = 'purchase' THEN timestamp END) AS purchase_time
    FROM funnel_steps
    GROUP BY session_id
),

time_diffs AS (
    SELECT
        session_id,
        EXTRACT(EPOCH FROM (product_time - visit_time)) / 60 AS visit_to_product_min,
        EXTRACT(EPOCH FROM (cart_time - product_time)) / 60 AS product_to_cart_min,
        EXTRACT(EPOCH FROM (purchase_time - cart_time)) / 60 AS cart_to_purchase_min
    FROM step_times
    WHERE purchase_time IS NOT NULL
)

SELECT
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY visit_to_product_min) AS median_visit_to_product,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY product_to_cart_min) AS median_product_to_cart,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY cart_to_purchase_min) AS median_cart_to_purchase
FROM time_diffs;
```

### Time Distribution

```
Time to Complete Funnel
0-1 hour    ████████████████████████████████████████  20%
1-24 hours   ████████████████████████████████          40%
1-7 days     ████████████████████████                 25%
7-30 days    ████████████████                          10%
30+ days     ██████                                    5%
```

**Insight**: Most users complete within 24 hours

## Micro vs Macro Funnels

### Macro Funnel

Overall user journey from acquisition to conversion.

```
Acquisition → Activation → Engagement → Revenue → Retention
```

### Micro Funnel

Specific feature or process flow.

```
Search → Results → Click → Product View → Add to Cart
```

**Use case**: Optimize specific feature

## Tools

### Analytics Platforms

| Tool | Funnel Features | Pricing |
|------|----------------|----------|
| **Google Analytics 4** | Basic funnels | Free |
| **Mixpanel** | Advanced funnels | $$$ |
| **Amplitude** | Complex funnels | $$$ |
| **Heap** | Auto-capture funnels | $$ |
| **PostHog** | Open-source funnels | Free/$ |

### SQL (Custom)

**Pros**:
- Full control
- Works with any database
- Custom segmentation

**Cons**:
- Requires SQL knowledge
- No built-in visualization

### Python (Custom)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_funnel(df, steps):
    """
    Analyze funnel from event data.

    Parameters:
    -----------
    df : DataFrame
        Event data with session_id, event_type, timestamp
    steps : list
        Ordered list of funnel steps

    Returns:
    --------
    DataFrame : Funnel analysis
    """
    funnel_data = []

    for i, step in enumerate(steps):
        step_users = df[df['event_type'] == step]['session_id'].nunique()

        if i == 0:
            conversion_rate = 100.0
            drop_off_rate = 0.0
        else:
            previous_users = funnel_data[i-1]['users']
            conversion_rate = 100.0 * step_users / previous_users
            drop_off_rate = 100.0 - conversion_rate

        funnel_data.append({
            'step': step,
            'step_number': i + 1,
            'users': step_users,
            'conversion_rate': conversion_rate,
            'drop_off_rate': drop_off_rate
        })

    return pd.DataFrame(funnel_data)

def plot_funnel(funnel_df):
    """
    Plot funnel as bar chart.

    Parameters:
    -----------
    funnel_df : DataFrame
        Funnel analysis from analyze_funnel
    """
    plt.figure(figsize=(10, 6))

    bars = plt.barh(
        funnel_df['step'],
        funnel_df['users'],
        color='steelblue'
    )

    # Add value labels
    for bar, users in zip(bars, funnel_df['users']):
        plt.text(
            bar.get_width() + 100,
            bar.get_y() + bar.get_height()/2,
            f'{users:,} ({funnel_df.loc[funnel_df["users"] == users, "conversion_rate"].values[0]:.1f}%)',
            va='center'
        )

    plt.xlabel('Users')
    plt.title('Funnel Analysis')
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Create sample data
    np.random.seed(42)
    events = []

    for session_id in range(10000):
        # Visit
        events.append({
            'session_id': session_id,
            'event_type': 'visit',
            'timestamp': pd.Timestamp('2024-01-01')
        })

        # Product view (50%)
        if np.random.random() < 0.5:
            events.append({
                'session_id': session_id,
                'event_type': 'product_view',
                'timestamp': pd.Timestamp('2024-01-01') + pd.Timedelta(minutes=np.random.randint(1, 10))
            })

            # Add to cart (20% of product views)
            if np.random.random() < 0.2:
                events.append({
                    'session_id': session_id,
                    'event_type': 'add_to_cart',
                    'timestamp': pd.Timestamp('2024-01-01') + pd.Timedelta(minutes=np.random.randint(10, 20))
                })

                # Purchase (50% of carts)
                if np.random.random() < 0.5:
                    events.append({
                        'session_id': session_id,
                        'event_type': 'purchase',
                        'timestamp': pd.Timestamp('2024-01-01') + pd.Timedelta(minutes=np.random.randint(20, 30))
                    })

    df = pd.DataFrame(events)

    # Analyze funnel
    steps = ['visit', 'product_view', 'add_to_cart', 'purchase']
    funnel_df = analyze_funnel(df, steps)

    print(funnel_df)
    plot_funnel(funnel_df)
```

## Real Funnel Examples

### Example 1: E-commerce Checkout Funnel

```
Step          Users    Conversion    Drop-off
─────────────────────────────────────────────
Visit         10,000    100%          -
Product View  5,000     50%           50%
Add to Cart   1,000     20%           80%
Checkout      500       50%           50%
Purchase      500       100%          -
```

**Insights**:
- Biggest drop-off: Add to Cart (80%)
- Overall conversion: 5%
- Focus on improving Add to Cart → Checkout

### Example 2: SaaS Signup Funnel

```
Step          Users    Conversion    Drop-off
─────────────────────────────────────────────
Landing       10,000    100%          -
Signup Form   5,000     50%           50%
Verify Email  4,000     80%           20%
Activate      2,000     50%           50%
Upgrade       200       10%           90%
```

**Insights**:
- Biggest drop-off: Upgrade (90%)
- Overall conversion: 2%
- Focus on improving activation and upgrade

### Example 3: Mobile App Funnel

```
Step          Users    Conversion    Drop-off
─────────────────────────────────────────────
App Store     50,000    100%          -
Install       25,000    50%           50%
Open          15,000    60%           40%
Sign Up       10,000    67%           33%
First Use     5,000     50%           50%
```

**Insights**:
- Biggest drop-off: Install (50%)
- Overall conversion: 10%
- Focus on improving app store conversion

## Summary Checklist

### Analysis Phase

- [ ] Define funnel steps
- [ ] Identify key metrics
- [ ] Gather event data
- [ ] Calculate conversion rates
- [ ] Identify bottlenecks

### Optimization Phase

- [ ] Prioritize biggest drop-offs
- [ ] Formulate hypotheses
- [ ] Run A/B tests
- [ ] Measure impact
```

---

## Quick Start

### Funnel Query

```sql
-- Calculate funnel conversion rates
WITH funnel_steps AS (
  SELECT 
    COUNT(DISTINCT CASE WHEN event = 'page_view' THEN user_id END) as step1,
    COUNT(DISTINCT CASE WHEN event = 'add_to_cart' THEN user_id END) as step2,
    COUNT(DISTINCT CASE WHEN event = 'checkout_start' THEN user_id END) as step3,
    COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) as step4
  FROM events
  WHERE date >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT 
  step1 as visitors,
  step2 as add_to_cart,
  step3 as checkout_start,
  step4 as purchases,
  (step2::float / step1 * 100) as step1_to_step2,
  (step3::float / step2 * 100) as step2_to_step3,
  (step4::float / step3 * 100) as step3_to_step4,
  (step4::float / step1 * 100) as overall_conversion
FROM funnel_steps
```

---

## Production Checklist

- [ ] **Funnel Definition**: Define funnel steps clearly
- [ ] **Event Tracking**: Track all funnel events
- [ ] **Data Collection**: Collect user journey data
- [ ] **Visualization**: Create funnel visualization
- [ ] **Drop-off Analysis**: Identify drop-off points
- [ ] **Hypothesis**: Formulate optimization hypotheses
- [ ] **A/B Testing**: Test improvements
- [ ] **Monitoring**: Monitor funnel metrics
- [ ] **Documentation**: Document funnel definitions
- [ ] **Segmentation**: Segment funnels by user type
- [ ] **Reporting**: Regular funnel reports
- [ ] **Action Items**: Act on insights

---

## Anti-patterns

### ❌ Don't: Too Many Steps

```markdown
# ❌ Bad - Too many steps
Step 1: Visit
Step 2: View product
Step 3: Add to cart
Step 4: View cart
Step 5: Start checkout
Step 6: Enter email
Step 7: Enter address
Step 8: Enter payment
Step 9: Complete
# Too granular!
```

```markdown
# ✅ Good - Key steps only
Step 1: Visit
Step 2: Add to cart
Step 3: Start checkout
Step 4: Complete purchase
# Focus on major actions
```

### ❌ Don't: No Context

```markdown
# ❌ Bad - No context
Step 2: 50% drop-off
# Why?
```

```markdown
# ✅ Good - With context
Step 2: 50% drop-off
- Users see shipping cost
- Many abandon here
- Hypothesis: Free shipping would help
```

---

## Integration Points

- **Conversion Optimization** (`23-business-analytics/conversion-optimization/`) - CRO
- **A/B Testing** (`23-business-analytics/ab-testing-analysis/`) - Testing improvements
- **Dashboard Design** (`23-business-analytics/dashboard-design/`) - Funnel visualization

---

## Further Reading

- [Funnel Analysis Guide](https://www.optimizely.com/optimization-glossary/funnel-analysis/)
- [Conversion Funnel Optimization](https://www.shopify.com/blog/conversion-funnel)
- [ ] Iterate

### Monitoring Phase

- [ ] Track funnel performance
- [ ] Monitor for anomalies
- [ ] Segment by key dimensions
- [ ] Update regularly
- [ ] Share insights with team
