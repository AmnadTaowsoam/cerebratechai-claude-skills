---
name: Cohort Analysis
description: Grouping users into cohorts based on shared characteristics and analyzing their behavior over time to track retention, identify patterns, measure LTV, and optimize acquisition channels.
---

# Cohort Analysis

> **Current Level:** Intermediate  
> **Domain:** Business Analytics / Data Science

---

## Overview

Cohort analysis is the process of grouping users into cohorts based on shared characteristics and analyzing their behavior over time. This enables apples-to-apples comparison of different user groups to identify patterns and trends, track retention, measure lifetime value, and optimize acquisition channels.

## What is Cohort Analysis

### Key Benefits

| Benefit | Description |
|---------|-------------|
| **Track retention** | See how long users stay engaged |
| **Identify patterns** | Discover trends in user behavior |
| **Measure LTV** | Calculate lifetime value by cohort |
| **Optimize acquisition** | Find best acquisition channels |
| **Improve onboarding** | Identify drop-off points |

## What is a Cohort

A cohort is a group of users who share a common characteristic or experience within a defined time period.

### Cohort Examples

| Cohort Type | Example |
|-------------|---------|
| **Time-based** | All users who signed up in January 2024 |
| **Behavior-based** | Users who completed onboarding |
| **Acquisition-based** | Users acquired via organic search |
| **Geographic** | Users from Thailand |
| **Pricing plan** | Users on the Pro plan |

### Why Cohorts Matter

Without cohorts, you can't distinguish between:
- New user behavior vs. long-term user behavior
- Seasonal effects vs. product changes
- Acquisition channel differences vs. product quality

## Types of Cohorts

### 1. Time-Based Cohorts

Users grouped by when they took an action.

| Cohort Definition | Example |
|-------------------|---------|
| Signup month | January 2024 users |
| First purchase month | Q1 2024 purchasers |
| Activation date | Users who activated on a specific day |

### 2. Behavior-Based Cohorts

Users grouped by actions they've taken.

| Cohort Definition | Example |
|-------------------|---------|
| Power users | Users who used feature 10+ times |
| Free trial users | Users who started trial |
| Upgraded users | Users who upgraded from free to paid |

### 3. Acquisition-Based Cohorts

Users grouped by how they were acquired.

| Cohort Definition | Example |
|-------------------|---------|
| Organic search | Users from Google search |
| Paid ads | Users from Facebook ads |
| Referral | Users referred by other users |

## Cohort Retention

### What is Retention

The percentage of users who return after their initial action.

### Retention Metrics

| Metric | Definition | Use Case |
|--------|------------|----------|
| **Classic retention** | Did user return on Day N? | Daily active products |
| **N-day retention** | Returned on or after Day N? | Subscription products |
| **Rolling retention** | Returned in a window (e.g., past 7 days) | Mobile apps |
| **Unbounded retention** | Returned ever after Day N? | Lifetime value analysis |

### Retention Calculation

```
Retention Rate = (Users who returned / Total cohort size) × 100%
```

### Retention Goals by Product Type

| Product Type | Day 1 | Day 7 | Day 30 |
|--------------|-------|-------|--------|
| **Social Media** | >40% | >20% | >10% |
| **SaaS** | >60% | >40% | >30% |
| **E-commerce** | >30% | >15% | >10% |
| **Mobile Game** | >40% | >20% | >10% |

## Cohort Table (Retention Matrix)

### Structure

```
┌─────────────┬────────┬────────┬────────┬────────┬────────┐
│  Cohort     │  Size  │  Day 0 │  Day 1 │  Day 7 │ Day 30 │
├─────────────┼────────┼────────┼────────┼────────┼────────┤
│  Jan 2024   │  1000  │  100%  │  45%   │  25%   │  15%   │
│  Feb 2024   │  1200  │  100%  │  50%   │  30%   │  18%   │
│  Mar 2024   │  1500  │  100%  │  55%   │  35%   │  22%   │
│  Apr 2024   │  1800  │  100%  │  60%   │  40%   │  25%   │
└─────────────┴────────┴────────┴────────┴────────┴────────┘
```

### Reading the Cohort Table

| Direction | What It Shows |
|-----------|---------------|
| **Horizontal** | How a specific cohort decays over time |
| **Vertical** | How different cohorts compare at the same time point |
| **Diagonal** | First-month retention across cohorts |

### Interpretation Example

```
Jan 2024 cohort: 100% → 45% → 25% → 15%
- 55% churned after Day 1
- 20% more churned by Day 7
- 10% more churned by Day 30
- 15% retained after 30 days
```

## Cohort Visualization

### 1. Retention Curves (Line Chart)

```
Retention %
100% ┤
 90% ┤
 80% ┤
 70% ┤
 60% ┤
 50% ┤  ●─────── Jan 2024
 40% ┤      ●─── Feb 2024
 30% ┤          ●── Mar 2024
 20% ┤              ●─ Apr 2024
 10% ┤
  0% └─────────────────────────────
      0   7   14  21  30  60  90
               Days
```

### 2. Retention Heatmap

```
Cohort    Day 0  Day 7  Day 14  Day 30
─────────────────────────────────────────
Jan 2024  ■■■■■■■■■■  ■■■■■■■   ■■■■■    ■■■
Feb 2024  ■■■■■■■■■■  ■■■■■■■■  ■■■■■■   ■■■■
Mar 2024  ■■■■■■■■■■  ■■■■■■■■  ■■■■■■■  ■■■■■
Apr 2024  ■■■■■■■■■■  ■■■■■■■■  ■■■■■■■■ ■■■■■

Key: ■ = 10% retention
```

### 3. Stacked Area Chart (by Channel)

```
Active Users
1000 ┤
 900 ┤  ╱─────────────── Organic
 800 ┤ ╱
 700 ┤╱
 600 ┤
 500 ┤      ╱─────────── Paid
 400 ┤     ╱
 300 ┤    ╱
 200 ┤   ╱
 100 ┤  ╱
   0 └─────────────────────────────
      Jan  Feb  Mar  Apr  May
```

## SQL for Cohort Analysis

### Data Schema

```sql
-- Users table
CREATE TABLE users (
    user_id BIGINT PRIMARY KEY,
    signup_date DATE NOT NULL,
    country VARCHAR(50),
    acquisition_channel VARCHAR(50)
);

-- Events table
CREATE TABLE events (
    event_id BIGINT PRIMARY KEY,
    user_id BIGINT NOT NULL,
    event_date DATE NOT NULL,
    event_type VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Indexes for performance
CREATE INDEX idx_events_user_id ON events(user_id);
CREATE INDEX idx_events_date ON events(event_date);
CREATE INDEX idx_events_type ON events(event_type);
```

### Basic Cohort Retention Query

```sql
WITH cohorts AS (
    -- Define cohorts by signup month
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date) AS cohort_month
    FROM users
    WHERE signup_date >= '2024-01-01'
),

user_activities AS (
    -- Get user activity by month
    SELECT
        user_id,
        DATE_TRUNC('month', event_date) AS activity_month
    FROM events
    WHERE event_type = 'page_view'
),

cohort_activities AS (
    -- Join cohorts with activities
    SELECT
        c.cohort_month,
        c.user_id,
        ua.activity_month,
        EXTRACT(MONTH FROM AGE(ua.activity_month, c.cohort_month)) AS month_number
    FROM cohorts c
    LEFT JOIN user_activities ua ON c.user_id = ua.user_id
)

-- Calculate retention
SELECT
    cohort_month,
    month_number,
    COUNT(DISTINCT user_id) AS active_users,
    FIRST_VALUE(COUNT(DISTINCT user_id)) OVER (
        PARTITION BY cohort_month
        ORDER BY month_number
    ) AS cohort_size,
    ROUND(
        100.0 * COUNT(DISTINCT user_id) / FIRST_VALUE(COUNT(DISTINCT user_id)) OVER (
            PARTITION BY cohort_month
            ORDER BY month_number
        ),
        2
    ) AS retention_pct
FROM cohort_activities
WHERE month_number >= 0
GROUP BY cohort_month, month_number
ORDER BY cohort_month, month_number;
```

### Day-based Retention Query

```sql
WITH cohorts AS (
    SELECT
        user_id,
        signup_date
    FROM users
    WHERE signup_date >= '2024-01-01'
),

retention_data AS (
    SELECT
        c.user_id,
        c.signup_date,
        e.event_date,
        EXTRACT(DAY FROM (e.event_date - c.signup_date)) AS day_number
    FROM cohorts c
    LEFT JOIN events e ON c.user_id = e.user_id
    WHERE e.event_date >= c.signup_date
),

cohort_sizes AS (
    SELECT
        signup_date,
        COUNT(*) AS cohort_size
    FROM cohorts
    GROUP BY signup_date
)

SELECT
    r.signup_date,
    r.day_number,
    COUNT(DISTINCT r.user_id) AS retained_users,
    cs.cohort_size,
    ROUND(100.0 * COUNT(DISTINCT r.user_id) / cs.cohort_size, 2) AS retention_pct
FROM retention_data r
JOIN cohort_sizes cs ON r.signup_date = cs.signup_date
GROUP BY r.signup_date, r.day_number, cs.cohort_size
ORDER BY r.signup_date, r.day_number;
```

### Rolling Retention Query

```sql
WITH cohorts AS (
    SELECT
        user_id,
        signup_date
    FROM users
    WHERE signup_date >= '2024-01-01'
),

retention_data AS (
    SELECT
        c.user_id,
        c.signup_date,
        e.event_date,
        EXTRACT(DAY FROM (e.event_date - c.signup_date)) AS day_number
    FROM cohorts c
    JOIN events e ON c.user_id = e.user_id
    WHERE e.event_date >= c.signup_date
),

cohort_sizes AS (
    SELECT
        signup_date,
        COUNT(*) AS cohort_size
    FROM cohorts
    GROUP BY signup_date
),

rolling_retention AS (
    SELECT
        signup_date,
        day_number,
        COUNT(DISTINCT user_id) AS retained_users
    FROM retention_data
    GROUP BY signup_date, day_number
)

SELECT
    rr.signup_date,
    rr.day_number,
    rr.retained_users,
    cs.cohort_size,
    ROUND(100.0 * rr.retained_users / cs.cohort_size, 2) AS rolling_retention_pct
FROM rolling_retention rr
JOIN cohort_sizes cs ON rr.signup_date = cs.signup_date
WHERE rr.day_number IN (7, 14, 30)
ORDER BY rr.signup_date, rr.day_number;
```

### Cohort by Acquisition Channel

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date) AS cohort_month,
        acquisition_channel
    FROM users
    WHERE signup_date >= '2024-01-01'
),

user_activities AS (
    SELECT
        user_id,
        DATE_TRUNC('month', event_date) AS activity_month
    FROM events
    WHERE event_type = 'page_view'
),

cohort_activities AS (
    SELECT
        c.cohort_month,
        c.acquisition_channel,
        c.user_id,
        ua.activity_month,
        EXTRACT(MONTH FROM AGE(ua.activity_month, c.cohort_month)) AS month_number
    FROM cohorts c
    LEFT JOIN user_activities ua ON c.user_id = ua.user_id
),

cohort_sizes AS (
    SELECT
        cohort_month,
        acquisition_channel,
        COUNT(*) AS cohort_size
    FROM cohorts
    GROUP BY cohort_month, acquisition_channel
)

SELECT
    ca.cohort_month,
    ca.acquisition_channel,
    ca.month_number,
    cs.cohort_size,
    COUNT(DISTINCT ca.user_id) AS active_users,
    ROUND(100.0 * COUNT(DISTINCT ca.user_id) / cs.cohort_size, 2) AS retention_pct
FROM cohort_activities ca
JOIN cohort_sizes cs ON ca.cohort_month = cs.cohort_month
    AND ca.acquisition_channel = cs.acquisition_channel
WHERE ca.month_number >= 0
GROUP BY ca.cohort_month, ca.acquisition_channel, ca.month_number, cs.cohort_size
ORDER BY ca.cohort_month, ca.acquisition_channel, ca.month_number;
```

## Cohort Analysis Tools

### 1. SQL (Custom Analysis)

**Pros**:
- Full control
- Works with any database
- Flexible

**Cons**:
- Requires SQL knowledge
- No built-in visualization

### 2. Product Analytics Platforms

| Tool | Strengths | Pricing |
|------|-----------|---------|
| **Amplitude** | Excellent cohort analysis | $$$ |
| **Mixpanel** | Powerful segmentation | $$$ |
| **Heap** | Auto-capture events | $$ |
| **PostHog** | Open-source | Free/$ |

### 3. BI Tools

| Tool | Cohort Support |
|------|----------------|
| **Tableau** | Requires custom SQL |
| **Looker** | LookML for cohorts |
| **Metabase** | Basic cohort visualization |
| **Redash** | SQL-based cohorts |

### 4. Python (Custom Analysis)

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_cohort_retention(df, user_col='user_id', date_col='date'):
    """
    Calculate cohort retention from event data.

    Parameters:
    -----------
    df : DataFrame
        Event data with user_id and date columns
    user_col : str
        Name of user_id column
    date_col : str
        Name of date column

    Returns:
    --------
    DataFrame : Cohort retention table
    """
    # Convert to datetime
    df[date_col] = pd.to_datetime(df[date_col])

    # Get cohort (first activity date)
    df['cohort'] = df.groupby(user_col)[date_col].transform('min')

    # Calculate period number
    df['period_number'] = (
        (df[date_col].dt.year - df['cohort'].dt.year) * 12 +
        (df[date_col].dt.month - df['cohort'].dt.month)
    )

    # Group by cohort and period
    cohort_data = df.groupby(['cohort', 'period_number'])[user_col].nunique().reset_index()
    cohort_sizes = df.groupby('cohort')[user_col].nunique().reset_index()
    cohort_sizes.columns = ['cohort', 'cohort_size']

    # Merge and calculate retention
    cohort_data = cohort_data.merge(cohort_sizes, on='cohort')
    cohort_data['retention'] = cohort_data[user_col] / cohort_data['cohort_size']

    # Pivot for display
    cohort_pivot = cohort_data.pivot(
        index='cohort',
        columns='period_number',
        values='retention'
    )

    return cohort_pivot

def plot_cohort_heatmap(cohort_data, figsize=(12, 8)):
    """
    Plot cohort retention as heatmap.

    Parameters:
    -----------
    cohort_data : DataFrame
        Cohort retention data from calculate_cohort_retention
    figsize : tuple
        Figure size
    """
    plt.figure(figsize=figsize)

    # Create heatmap
    sns.heatmap(
        cohort_data,
        annot=True,
        fmt='.0%',
        cmap='YlGnBu',
        cbar_kws={'label': 'Retention Rate'}
    )

    plt.title('Cohort Retention Heatmap')
    plt.ylabel('Cohort')
    plt.xlabel('Period Number')
    plt.tight_layout()
    plt.show()

def plot_cohort_curves(cohort_data, figsize=(12, 6)):
    """
    Plot cohort retention curves.

    Parameters:
    -----------
    cohort_data : DataFrame
        Cohort retention data from calculate_cohort_retention
    figsize : tuple
        Figure size
    """
    plt.figure(figsize=figsize)

    # Plot each cohort
    for cohort in cohort_data.index:
        plt.plot(
            cohort_data.columns,
            cohort_data.loc[cohort],
            marker='o',
            label=cohort.strftime('%Y-%m')
        )

    plt.title('Cohort Retention Curves')
    plt.xlabel('Period Number')
    plt.ylabel('Retention Rate')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

# Example usage
if __name__ == "__main__":
    # Create sample data
    np.random.seed(42)
    dates = pd.date_range('2024-01-01', '2024-06-30', freq='D')

    data = []
    for i in range(1000):
        user_id = f'user_{i}'
        signup_date = np.random.choice(dates)
        # Generate activity events with decay
        for days in range(0, 60):
            if np.random.random() < 0.8 * (1 - days/60):  # Decay over time
                event_date = signup_date + pd.Timedelta(days=days)
                if event_date <= dates[-1]:
                    data.append({'user_id': user_id, 'date': event_date})

    df = pd.DataFrame(data)

    # Calculate cohort retention
    cohort_retention = calculate_cohort_retention(df)

    # Visualize
    plot_cohort_heatmap(cohort_retention)
    plot_cohort_curves(cohort_retention)
```

## Improving Retention

### 1. Identify Drop-off Points

Analyze where users churn:

| Drop-off Point | Analysis | Action |
|----------------|-----------|--------|
| **Day 1** | Users don't return | Improve onboarding |
| **Day 7** | Users don't find value | Add engagement features |
| **Day 30** | Users lose interest | Add new features, notifications |

### 2. Onboarding Improvements

| Strategy | Description |
|----------|-------------|
| **Simplified signup** | Reduce friction |
| **Guided tour** | Show key features |
| **Quick wins** | Enable early success |
| **Progressive disclosure** | Don't overwhelm |

### 3. Engagement Features

| Feature | Purpose |
|---------|---------|
| **Push notifications** | Remind users to return |
| **Email campaigns** | Re-engagement emails |
| **In-app messages** | Contextual prompts |
| **Gamification** | Rewards for engagement |

### 4. Product Value Delivery

| Approach | Description |
|----------|-------------|
| **Time to value** | Reduce time to first value |
| **Feature adoption** | Encourage feature usage |
| **Personalization** | Tailor experience |
| **Feedback loops** | Listen to users |

## Revenue Cohorts

### Revenue by Cohort

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date) AS cohort_month
    FROM users
),

revenue_data AS (
    SELECT
        c.user_id,
        c.cohort_month,
        DATE_TRUNC('month', o.order_date) AS revenue_month,
        SUM(o.revenue) AS revenue
    FROM cohorts c
    JOIN orders o ON c.user_id = o.user_id
    GROUP BY c.user_id, c.cohort_month, DATE_TRUNC('month', o.order_date)
),

cumulative_revenue AS (
    SELECT
        cohort_month,
        revenue_month,
        EXTRACT(MONTH FROM AGE(revenue_month, cohort_month)) AS month_number,
        SUM(revenue) OVER (
            PARTITION BY cohort_month
            ORDER BY revenue_month
        ) AS cumulative_revenue
    FROM revenue_data
)

SELECT
    cohort_month,
    month_number,
    ROUND(cumulative_revenue, 2) AS cumulative_revenue
FROM cumulative_revenue
ORDER BY cohort_month, month_number;
```

### Lifetime Value (LTV) by Cohort

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date) AS cohort_month
    FROM users
),

user_ltv AS (
    SELECT
        c.user_id,
        c.cohort_month,
        COALESCE(SUM(o.revenue), 0) AS lifetime_revenue
    FROM cohorts c
    LEFT JOIN orders o ON c.user_id = o.user_id
    GROUP BY c.user_id, c.cohort_month
)

SELECT
    cohort_month,
    COUNT(*) AS cohort_size,
    ROUND(AVG(lifetime_revenue), 2) AS avg_ltv,
    ROUND(SUM(lifetime_revenue), 2) AS total_revenue,
    ROUND(SUM(lifetime_revenue) / COUNT(*), 2) AS ltv_per_user
FROM user_ltv
GROUP BY cohort_month
ORDER BY cohort_month;
```

## Engagement Cohorts

### Weekly Active Users by Signup Cohort

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date) AS cohort_month
    FROM users
),

weekly_activity AS (
    SELECT
        c.user_id,
        c.cohort_month,
        DATE_TRUNC('week', e.event_date) AS week_start
    FROM cohorts c
    JOIN events e ON c.user_id = e.user_id
    WHERE e.event_type = 'page_view'
),

week_number AS (
    SELECT
        cohort_month,
        week_start,
        EXTRACT(WEEK FROM (week_start - MIN(week_start) OVER (PARTITION BY cohort_month))) AS week_number,
        COUNT(DISTINCT user_id) AS active_users
    FROM weekly_activity
    GROUP BY cohort_month, week_start
)

SELECT
    cohort_month,
    week_number,
    active_users
FROM week_number
ORDER BY cohort_month, week_number;
```

### Power User Percentage by Cohort

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date) AS cohort_month
    FROM users
),

user_activity AS (
    SELECT
        c.user_id,
        c.cohort_month,
        COUNT(*) AS event_count
    FROM cohorts c
    JOIN events e ON c.user_id = e.user_id
    WHERE e.event_date >= c.cohort_month
        AND e.event_date < c.cohort_month + INTERVAL '1 month'
    GROUP BY c.user_id, c.cohort_month
),

cohort_stats AS (
    SELECT
        cohort_month,
        COUNT(*) AS total_users,
        SUM(CASE WHEN event_count >= 10 THEN 1 ELSE 0 END) AS power_users
    FROM user_activity
    GROUP BY cohort_month
)

SELECT
    cohort_month,
    total_users,
    power_users,
    ROUND(100.0 * power_users / total_users, 2) AS power_user_pct
FROM cohort_stats
ORDER BY cohort_month;
```

## Segmented Cohorts

### Cohorts by Pricing Plan

```sql
WITH cohorts AS (
    SELECT
        user_id,
        DATE_TRUNC('month', signup_date) AS cohort_month,
        initial_plan
    FROM users
    WHERE signup_date >= '2024-01-01'
),

retention_data AS (
    SELECT
        c.cohort_month,
        c.initial_plan,
        c.user_id,
        DATE_TRUNC('month', e.event_date) AS activity_month,
        EXTRACT(MONTH FROM AGE(activity_month, cohort_month)) AS month_number
    FROM cohorts c
    JOIN events e ON c.user_id = e.user_id
    WHERE e.event_date >= c.cohort_month
),

cohort_sizes AS (
    SELECT
        cohort_month,
        initial_plan,
        COUNT(*) AS cohort_size
    FROM cohorts
    GROUP BY cohort_month, initial_plan
)

SELECT
    r.cohort_month,
    r.initial_plan,
    r.month_number,
    cs.cohort_size,
    COUNT(DISTINCT r.user_id) AS active_users,
    ROUND(100.0 * COUNT(DISTINCT r.user_id) / cs.cohort_size, 2) AS retention_pct
FROM retention_data r
JOIN cohort_sizes cs ON r.cohort_month = cs.cohort_month
    AND r.initial_plan = cs.initial_plan
GROUP BY r.cohort_month, r.initial_plan, r.month_number, cs.cohort_size
ORDER BY r.cohort_month, r.initial_plan, r.month_number;
```

## Common Mistakes

### 1. Not Accounting for Cohort Size Differences

**Problem**: Comparing retention percentages without considering cohort sizes.

**Solution**: Always show cohort size alongside retention rates.

### 2. Comparing Incomplete Cohorts

**Problem**: Recent cohorts have less data (e.g., only 2 months of data vs 12 months).

**Solution**: Mark incomplete cohorts or only compare same time periods.

### 3. Ignoring External Factors

**Problem**: Seasonality, marketing campaigns, or product changes affect results.

**Solution**: Document external events and analyze their impact.

### 4. Wrong Cohort Definition

**Problem**: Using wrong time period or action for cohort definition.

**Solution**: Align cohort definition with business goals (e.g., signup vs. activation).

### 5. Data Quality Issues

**Problem**: Missing events, duplicate users, or incorrect timestamps.

**Solution**: Validate data quality before analysis.

## Advanced Cohort Analysis

### 1. Predictive Retention

Use machine learning to predict which users will churn.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def predict_churn(df, features, target='churned'):
    """
    Predict user churn using Random Forest.

    Parameters:
    -----------
    df : DataFrame
        User feature data
    features : list
        List of feature column names
    target : str
        Target column name

    Returns:
    --------
    model : Trained model
    """
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    return model
```

### 2. Cohort-Based Forecasting

Project future retention based on historical patterns.

```python
def forecast_retention(cohort_data, periods_to_forecast=6):
    """
    Forecast future retention based on historical cohorts.

    Parameters:
    -----------
    cohort_data : DataFrame
        Historical cohort retention data
    periods_to_forecast : int
        Number of periods to forecast

    Returns:
    --------
    DataFrame : Forecasted retention
    """
    # Calculate average retention curve
    avg_retention = cohort_data.mean()

    # Forecast using decay pattern
    forecast = {}
    for i in range(periods_to_forecast):
        period = cohort_data.columns.max() + i + 1
        # Simple decay model
        forecast[period] = avg_retention.iloc[-1] * (0.95 ** (i + 1))

    return pd.Series(forecast)
```

### 3. Simpson's Paradox Detection

Check if aggregate results differ from segment results.

```python
def check_simpsons_paradox(cohort_data, segment_col):
    """
    Check for Simpson's paradox in cohort data.

    Parameters:
    -----------
    cohort_data : DataFrame
        Cohort retention data
    segment_col : str
        Column name for segmentation

    Returns:
    --------
    bool : True if Simpson's paradox detected
    """
    # Aggregate retention
    aggregate_trend = cohort_data.mean().diff().mean()

    # Segment trends
    segment_trends = cohort_data.groupby(segment_col).mean().diff().mean()

    # Check if trends differ
    paradox = False
    for segment, trend in segment_trends.items():
        if (aggregate_trend > 0 and trend < 0) or (aggregate_trend < 0 and trend > 0):
            paradox = True
            print(f"Simpson's paradox detected for segment: {segment}")

    return paradox
```

## Real Examples

### Example 1: SaaS Subscription Retention

```
Cohort    Size   M0    M1    M2    M3    M6    M12
──────────────────────────────────────────────────────
Jan 2024   500  100%  85%   75%   70%   60%   50%
Feb 2024   600  100%  88%   78%   72%   62%   -
Mar 2024   700  100%  90%   80%   74%   -    -
Apr 2024   800  100%  92%   82%   -    -    -

Insights:
- Retention improving over time (better onboarding)
- 12-month retention stable at 50%
- Recent cohorts showing better early retention
```

### Example 2: E-commerce Repeat Purchase

```
Cohort    Size   Day 0  Day 7  Day 30  Day 90
─────────────────────────────────────────────────
Jan 2024  1000   100%    25%     15%      8%
Feb 2024  1200   100%    28%     17%      9%
Mar 2024  1500   100%    30%     18%      -

Insights:
- Repeat purchase rate improving
- Email campaigns likely helping
- Focus on Day 7 to Day 30 conversion
```

### Example 3: Mobile App Retention

```
Cohort    Size   D1    D7    D30   D90
────────────────────────────────────────
Jan 2024  5000   40%   20%   10%    5%
Feb 2024  6000   42%   22%   11%    -
Mar 2024  7000   45%   24%   -     -

Insights:
- Day 1 retention improving (better onboarding)
- Push notifications helping Day 7 retention
- Long-term retention stable
```

## Summary Checklist

### Analysis Preparation

- [ ] Define cohort type (time, behavior, acquisition)
- [ ] Identify key metrics (retention, revenue, engagement)
- [ ] Prepare data schema
- [ ] Validate data quality

### Analysis Execution

- [ ] Calculate cohort sizes
- [ ] Compute retention rates
- [ ] Create cohort table
- [ ] Visualize results

### Interpretation

- [ ] Compare cohorts over time
- [ ] Identify trends
- [ ] Find drop-off points
- [ ] Segment by key dimensions
```

---

## Quick Start

### Cohort Retention Query

```sql
-- Monthly cohort retention
WITH first_purchase AS (
  SELECT 
    user_id,
    DATE_TRUNC('month', MIN(created_at)) as cohort_month
  FROM orders
  GROUP BY user_id
),
cohort_data AS (
  SELECT 
    fp.cohort_month,
    DATE_TRUNC('month', o.created_at) as order_month,
    COUNT(DISTINCT o.user_id) as users
  FROM first_purchase fp
  JOIN orders o ON fp.user_id = o.user_id
  GROUP BY fp.cohort_month, DATE_TRUNC('month', o.created_at)
)
SELECT 
  cohort_month,
  order_month,
  EXTRACT(MONTH FROM AGE(order_month, cohort_month)) as period,
  users
FROM cohort_data
ORDER BY cohort_month, period
```

---

## Production Checklist

- [ ] **Cohort Definition**: Define cohort criteria (signup date, acquisition channel)
- [ ] **Data Collection**: Collect user behavior data
- [ ] **Retention Calculation**: Calculate retention rates
- [ ] **Visualization**: Create cohort retention tables
- [ ] **Segmentation**: Segment cohorts by key dimensions
- [ ] **Trend Analysis**: Identify trends over time
- [ ] **LTV Calculation**: Calculate lifetime value by cohort
- [ ] **Documentation**: Document cohort definitions
- [ ] **Automation**: Automate cohort analysis
- [ ] **Reporting**: Regular cohort reports
- [ ] **Action Items**: Act on insights from analysis
- [ ] **Testing**: Validate cohort calculations

---

## Anti-patterns

### ❌ Don't: Too Many Cohorts

```sql
-- ❌ Bad - Too many cohort dimensions
SELECT 
  DATE_TRUNC('day', signup_date) as cohort,
  acquisition_channel,
  device_type,
  country,
  -- Too many dimensions!
```

```sql
-- ✅ Good - Focused cohorts
SELECT 
  DATE_TRUNC('month', signup_date) as cohort_month,
  acquisition_channel
-- Key dimensions only
```

### ❌ Don't: No Baseline

```markdown
# ❌ Bad - No baseline comparison
Cohort A: 50% retention
Cohort B: 45% retention
# Is this good or bad?
```

```markdown
# ✅ Good - With baseline
Cohort A: 50% retention (baseline: 40%) - +25% improvement
Cohort B: 45% retention (baseline: 40%) - +12.5% improvement
```

---

## Integration Points

- **KPI Metrics** (`23-business-analytics/kpi-metrics/`) - Retention KPIs
- **SQL for Analytics** (`23-business-analytics/sql-for-analytics/`) - Query patterns
- **Dashboard Design** (`23-business-analytics/dashboard-design/`) - Cohort visualization

---

## Further Reading

- [Cohort Analysis Guide](https://www.shopify.com/blog/cohort-analysis)
- [Retention Metrics](https://www.intercom.com/blog/cohort-analysis-retention/)

### Action

- [ ] Identify improvement opportunities
- [ ] Prioritize initiatives
- [ ] Implement changes
- [ ] Monitor impact
