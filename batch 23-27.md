# Batch 23: Business Analytics - Complete Prompts

Complete prompts for creating business analytics and data analysis skills.

---

## Batch 23: Business Analytics

### Skill 1: A/B Testing Analysis

```
Create a comprehensive SKILL.md for A/B Testing Analysis (statistical analysis of experiments).

Location: 23-business-analytics/ab-testing-analysis/SKILL.md

Cover:
1. What is A/B testing:
   - Controlled experiment with two variants (A and B)
   - Measure which performs better
   - Data-driven decision making
2. Why A/B testing matters:
   - Remove guesswork (test assumptions)
   - Measure real impact (not opinions)
   - Optimize continuously (incremental improvements)
   - Justify decisions with data
3. A/B test components:
   - Hypothesis (what you believe will happen)
   - Variants (A = control, B = treatment)
   - Metric (what you're measuring)
   - Sample size (how many users)
   - Duration (how long to run)
4. Hypothesis formulation:
   - Format: "If [change], then [expected outcome], because [reasoning]"
   - Example: "If we change button color to green, then conversion will increase by 10%, because green signals action"
   - Must be testable and measurable
5. Choosing metrics:
   - Primary metric (main success measure)
   - Secondary metrics (related measures)
   - Guardrail metrics (ensure no harm)
   - Example primary: Conversion rate
   - Example secondary: Average order value
   - Example guardrail: Page load time
6. Statistical concepts:
   - Null hypothesis (H0): No difference between A and B
   - Alternative hypothesis (H1): B is better than A
   - P-value: Probability result is due to chance
   - Statistical significance: p < 0.05 (95% confidence)
   - Type I error (false positive): Saying B is better when it's not
   - Type II error (false negative): Missing real improvement
7. Sample size calculation:
   - Baseline conversion rate (e.g., 10%)
   - Minimum detectable effect (MDE) (e.g., 1% absolute)
   - Significance level (α = 0.05)
   - Statistical power (β = 0.80, means 80% chance to detect effect)
   - Formula: n = 16 * (p * (1-p)) / (MDE²) per variant
   - Tools: Evan Miller calculator, Optimizely calculator
8. Test duration:
   - Run for at least 1 week (capture weekly patterns)
   - Achieve required sample size
   - Don't stop early (peeking problem)
   - Account for seasonality (avoid holidays)
9. Statistical tests:
   - Z-test for proportions (conversion rate)
   - T-test for continuous metrics (revenue)
   - Chi-square for categorical data
   - Mann-Whitney U for non-normal distributions
10. Analyzing results:
    - Calculate test statistic
    - Compute p-value
    - Determine statistical significance
    - Calculate confidence interval
    - Interpret practical significance
11. Confidence intervals:
    - Range of plausible values
    - Example: "Conversion increased by 2% (95% CI: 1.2% to 2.8%)"
    - Visualize with error bars
    - Overlapping CIs = not significant
12. Statistical significance vs practical significance:
    - Statistical: p < 0.05 (unlikely due to chance)
    - Practical: Meaningful business impact
    - Example: 0.1% conversion increase may be statistically significant but not worth implementing
13. Multiple testing problem:
    - Testing many metrics increases false positives
    - If you test 20 metrics at α=0.05, expect 1 false positive
    - Solutions:
      * Bonferroni correction (divide α by number of tests)
      * Focus on primary metric only
      * Pre-register hypothesis
14. Common pitfalls:
    - Peeking (checking results before test completes)
    - Sample ratio mismatch (50/50 split becomes 45/55)
    - Novelty effect (users try new thing temporarily)
    - Selection bias (test only on specific segment)
    - Carryover effects (previous exposure affects results)
15. Peeking problem:
    - Checking results early increases false positives
    - Solution: Sequential testing with adjusted thresholds
    - Or use Bayesian methods
    - Or commit to sample size upfront
16. Segmentation analysis:
    - Does effect vary by segment?
    - Example: Mobile vs desktop users
    - Example: New vs returning users
    - Interaction effects
    - Simpson's paradox (aggregate vs segment results differ)
17. Bayesian A/B testing:
    - Alternative to frequentist (p-value) approach
    - Outputs: Probability that B beats A
    - Can stop test early more safely
    - More intuitive interpretation
    - Tools: VWO, Google Optimize
18. A/A testing:
    - Test identical variants (sanity check)
    - Should show no difference
    - Validates instrumentation
    - Detects biases
19. Multi-variate testing (MVT):
    - Test multiple changes simultaneously
    - Example: Button color AND text
    - More complex analysis
    - Requires larger sample size
20. Tools for A/B testing:
    - Experimentation platforms: Optimizely, VWO, LaunchDarkly
    - Analytics: Google Analytics, Mixpanel, Amplitude
    - Statistical analysis: Python (scipy, statsmodels), R
    - Sample size calculators: Evan Miller, Optimizely
21. Implementation:
    - Randomization (assign users to A or B)
    - Consistent assignment (same user gets same variant)
    - Tracking (log exposures and conversions)
    - Analysis (compute statistics)
22. Reporting results:
    - Winner declaration (if significant)
    - Lift: Absolute (10% → 12% = +2%) and Relative (+20%)
    - Confidence interval
    - Recommendation (ship, iterate, or abandon)
    - Caveats and limitations
23. Post-experiment:
    - Long-term impact (holdout group)
    - Interaction with other changes
    - Cost-benefit analysis
    - Document learnings
24. Real examples:
    - Button color test (green vs blue)
    - Pricing page variants ($19/mo vs $21/mo)
    - Checkout flow (one-page vs multi-step)
    - Email subject lines
25. Python implementation:
    - scipy.stats for statistical tests
    - Plotting with matplotlib/seaborn
    - Sample size calculation
    - Confidence interval calculation

Format: Include statistical formulas, Python code examples, and result interpretation guides.

Create the file now.
```

### Skill 2: Business Intelligence

```
Create a comprehensive SKILL.md for Business Intelligence (BI) practices.

Location: 23-business-analytics/business-intelligence/SKILL.md

Cover:
1. What is Business Intelligence:
   - Transforming data into actionable insights
   - Reporting, analytics, and visualization
   - Support data-driven decision making
2. BI components:
   - Data sources (databases, APIs, files)
   - ETL/ELT (extract, transform, load data)
   - Data warehouse (centralized data storage)
   - BI tools (Tableau, Looker, Power BI)
   - Dashboards and reports
3. BI architecture:
   - Operational databases (OLTP)
   - Data warehouse (OLAP)
   - Data marts (department-specific)
   - BI layer (visualization)
4. Data warehouse concepts:
   - Star schema (fact table + dimension tables)
   - Snowflake schema (normalized dimensions)
   - Fact table (metrics, measures)
   - Dimension tables (context, attributes)
5. ETL process:
   - Extract: Pull data from sources
   - Transform: Clean, deduplicate, aggregate
   - Load: Insert into warehouse
   - Scheduling (nightly, hourly, real-time)
6. Modern data stack:
   - Data sources → Fivetran/Airbyte (ingestion)
   - → Snowflake/BigQuery (warehouse)
   - → dbt (transformation)
   - → Looker/Tableau (visualization)
7. BI tools:
   - Tableau (powerful, enterprise)
   - Looker (SQL-based, embedded)
   - Power BI (Microsoft ecosystem)
   - Metabase (open-source, simple)
   - Redash (SQL-focused)
8. Metrics and KPIs:
   - North Star metric (primary success measure)
   - Leading indicators (predict future)
   - Lagging indicators (historical performance)
   - Vanity metrics vs actionable metrics
9. Dashboard design:
   - Audience-specific (executive vs analyst)
   - Key metrics prominent
   - Visual hierarchy
   - Filters and interactivity
10. Self-service BI:
    - Empower non-technical users
    - Semantic layer (business-friendly names)
    - Pre-built reports and templates
    - Data catalog (find data)
11. Data governance:
    - Single source of truth
    - Data quality checks
    - Access controls
    - Data lineage (track data origin)
12. BI best practices:
    - Start with business questions
    - Iterate with stakeholders
    - Document metrics definitions
    - Monitor data quality
    - Version control (dbt)
13. Common BI use cases:
    - Sales dashboards (pipeline, conversion)
    - Marketing dashboards (CAC, ROAS)
    - Product analytics (DAU, retention)
    - Financial reporting (revenue, expenses)
14. Real-time vs batch BI:
    - Batch: Scheduled updates (nightly)
    - Real-time: Streaming data (Kafka, Kinesis)
    - Tradeoffs: Cost, complexity, latency
15. BI performance:
    - Pre-aggregate data (OLAP cubes)
    - Incremental updates
    - Query optimization
    - Caching
16. Embedded analytics:
    - White-label BI in your product
    - Customer-facing dashboards
    - Tools: Looker, Metabase, Cube.js
17. Implementation:
    - BI stack setup
    - Data modeling
    - Dashboard creation
18. Real examples:
    - SaaS metrics dashboard
    - E-commerce BI system

Format: Include architecture diagrams, data models, and dashboard examples.

Create the file now.
```

### Skill 3: Cohort Analysis

```
Create a comprehensive SKILL.md for Cohort Analysis.

Location: 23-business-analytics/cohort-analysis/SKILL.md

Cover:
1. What is cohort analysis:
   - Analyzing user behavior by cohorts (groups)
   - Track retention, engagement, revenue over time
   - Identify patterns and trends
2. What is a cohort:
   - Group of users with shared characteristic
   - Example: All users who signed up in January
   - Cohorts allow apples-to-apples comparison
3. Types of cohorts:
   - Time-based (signup date, first purchase date)
   - Behavior-based (completed onboarding, power users)
   - Acquisition-based (organic vs paid, channel)
4. Cohort retention:
   - Most common cohort analysis
   - % of users who return after initial action
   - Day 0, Day 1, Day 7, Day 30 retention
5. Retention metrics:
   - Classic retention (did user return on Day N?)
   - N-day retention (returned on or after Day N?)
   - Rolling retention (returned in window)
   - Unbounded retention (returned ever after Day N?)
6. Cohort table (retention matrix):
   - Rows: Cohorts (by signup month)
   - Columns: Time periods (months since signup)
   - Cells: Retention %
   - Diagonal: First-month retention
   - Horizontal: How cohort evolves
7. Reading cohort table:
   - Compare cohorts (are newer cohorts better?)
   - Long-term retention (do users stick around?)
   - Retention curve (decay pattern)
8. Cohort visualization:
   - Retention curves (line chart)
   - Retention heatmap (color-coded matrix)
   - Retention by channel (stacked area)
9. SQL for cohort analysis:
   - User table (user_id, signup_date)
   - Events table (user_id, event_date, event_type)
   - Cohort definition: GROUP BY DATE_TRUNC('month', signup_date)
   - Retention calculation: COUNT DISTINCT active users / total cohort size
10. Cohort SQL example:
    ```sql
    WITH cohorts AS (
      SELECT user_id,
             DATE_TRUNC('month', signup_date) AS cohort_month
      FROM users
    ),
    user_activities AS (
      SELECT user_id,
             DATE_TRUNC('month', event_date) AS activity_month
      FROM events
      WHERE event_type = 'active'
    )
    SELECT c.cohort_month,
           ua.activity_month,
           COUNT(DISTINCT ua.user_id) AS retained_users,
           COUNT(DISTINCT c.user_id) AS cohort_size,
           100.0 * COUNT(DISTINCT ua.user_id) / COUNT(DISTINCT c.user_id) AS retention_pct
    FROM cohorts c
    LEFT JOIN user_activities ua ON c.user_id = ua.user_id
    GROUP BY c.cohort_month, ua.activity_month
    ORDER BY c.cohort_month, ua.activity_month
    ```
11. Retention goals by product:
    - Social media: Day 1 > 40%, Day 30 > 20%
    - SaaS: Month 1 > 80%, Month 12 > 60%
    - E-commerce: 30-day repeat purchase > 30%
    - Mobile game: Day 1 > 40%, Day 7 > 20%
12. Improving retention:
    - Identify drop-off points (when users churn)
    - Onboarding improvements
    - Engagement features (notifications, emails)
    - Product value delivery
13. Revenue cohorts:
    - Track revenue per cohort over time
    - LTV (Lifetime Value) by cohort
    - Payback period
14. Engagement cohorts:
    - Weekly active users by signup cohort
    - Feature adoption by cohort
    - Power user % by cohort
15. Segmented cohorts:
    - Cohorts by acquisition channel
    - Cohorts by pricing plan
    - Cohorts by geography
16. Cohort analysis tools:
    - SQL (custom analysis)
    - Product analytics: Amplitude, Mixpanel, Heap
    - BI tools: Tableau, Looker (with data modeling)
    - Python: pandas for analysis
17. Common mistakes:
    - Not accounting for cohort size differences
    - Comparing incomplete cohorts (recent cohorts have less data)
    - Ignoring external factors (seasonality, marketing campaigns)
18. Advanced cohort analysis:
    - Predictive retention (ML model)
    - Cohort-based forecasting
    - Cohort attribution (which features drive retention?)
19. Real examples:
    - SaaS subscription retention
    - E-commerce repeat purchase cohorts
    - Mobile app retention
20. Implementation:
    - SQL queries
    - Python cohort analysis
    - Visualization in Matplotlib/Seaborn

Format: Include SQL queries, cohort table examples, and visualization code.

Create the file now.
```

### Skill 4: Conversion Optimization

```
Create a comprehensive SKILL.md for Conversion Optimization.

Location: 23-business-analytics/conversion-optimization/SKILL.md

Cover:
1. What is conversion optimization (CRO):
   - Increasing % of visitors who complete desired action
   - Data-driven experimentation
   - Continuous improvement process
2. Conversion funnel:
   - Stages: Awareness → Interest → Desire → Action
   - Example: Visit → Signup → Activate → Purchase
   - Drop-off at each stage
3. Funnel analysis:
   - Identify bottlenecks (biggest drop-offs)
   - Calculate conversion rate per stage
   - Overall conversion = multiply all stage rates
4. CRO process:
   - Research (understand users, find issues)
   - Hypothesize (what changes might help)
   - Prioritize (which tests to run first)
   - Test (A/B test hypothesis)
   - Learn (analyze results, iterate)
5. Research methods:
   - Analytics (where do users drop off?)
   - Heatmaps (where do users click?)
   - Session recordings (watch user behavior)
   - User surveys (ask users directly)
   - User interviews (deep qualitative insights)
6. Common conversion issues:
   - Slow page load (users bounce)
   - Unclear value proposition (users confused)
   - Too many form fields (friction)
   - Poor mobile experience
   - Lack of trust signals (no reviews, security badges)
7. Conversion rate formulas:
   - Conversion rate = Conversions / Visitors
   - Example: 100 purchases / 10,000 visitors = 1%
   - Micro-conversions (small steps)
   - Macro-conversions (final goal)
8. Optimization tactics:
   - Reduce friction (fewer form fields, autofill)
   - Add urgency (limited time offer, stock countdown)
   - Social proof (testimonials, user count)
   - Clear CTAs (action-oriented, contrasting color)
   - Trust signals (security badges, guarantees)
9. Landing page optimization:
   - Match ad message (message match)
   - Clear headline (value proposition)
   - Benefit-focused copy (not features)
   - Single CTA (don't overwhelm)
   - Remove navigation (reduce exits)
10. Form optimization:
    - Minimize fields (only ask essential)
    - Inline validation (instant feedback)
    - Progress indicators (multi-step forms)
    - Clear labels (above fields)
    - Smart defaults (pre-fill when possible)
11. Checkout optimization:
    - Guest checkout (don't force account)
    - Multiple payment options
    - Show total cost upfront (no surprises)
    - Trust badges (security, money-back)
    - Exit-intent popups (save abandoners)
12. Mobile optimization:
    - Mobile-first design
    - Large tap targets (44x44px minimum)
    - Reduce text entry (use dropdowns)
    - Thumb-friendly navigation
13. Pricing page optimization:
    - Clear plans (feature comparison)
    - Highlight recommended plan
    - Annual discount (encourage commitment)
    - FAQ section (address objections)
14. Prioritization frameworks:
    - ICE score: Impact × Confidence × Ease
    - PIE score: Potential × Importance × Ease
    - Focus on high-impact, low-effort tests first
15. Testing:
    - A/B testing (statistical rigor)
    - Multivariate testing (multiple elements)
    - User testing (qualitative feedback)
16. Tools:
    - A/B testing: Optimizely, VWO, Google Optimize
    - Analytics: Google Analytics, Mixpanel
    - Heatmaps: Hotjar, Crazy Egg
    - Session replay: FullStory, LogRocket
17. Metrics to track:
    - Overall conversion rate
    - Micro-conversion rates (per funnel step)
    - Time to convert
    - Bounce rate
    - Revenue per visitor (RPV)
18. Psychological principles:
    - Scarcity (limited availability)
    - Urgency (time pressure)
    - Social proof (others are doing it)
    - Authority (expert endorsement)
    - Reciprocity (free value first)
19. Real optimization examples:
    - E-commerce checkout flow
    - SaaS signup funnel
    - Lead generation form
20. Implementation:
    - Funnel analysis SQL
    - A/B test setup
    - Conversion tracking

Format: Include funnel analysis examples, optimization tactics, and A/B test case studies.

Create the file now.
```

### Skill 5: Dashboard Design

```
Create a comprehensive SKILL.md for Dashboard Design.

Location: 23-business-analytics/dashboard-design/SKILL.md

Cover:
1. What is a dashboard:
   - Visual display of key metrics
   - At-a-glance insights for decision making
   - Monitoring and exploration
2. Dashboard types:
   - Strategic (executive, high-level KPIs)
   - Operational (real-time monitoring)
   - Analytical (deep dive exploration)
   - Tactical (team-specific metrics)
3. Dashboard design principles:
   - Most important info first (top-left)
   - Visual hierarchy (size, color, position)
   - Consistent layout (grid-based)
   - White space (not cluttered)
   - Actionable insights (not just numbers)
4. Chart selection:
   - Line chart: Trends over time
   - Bar chart: Compare categories
   - Pie chart: Parts of whole (use sparingly, max 5 slices)
   - Table: Detailed data, exact values
   - KPI card: Single important number
   - Heatmap: Two dimensions (time + category)
   - Scatter plot: Correlation between variables
5. When to use each chart:
   - Time series → Line chart (or area chart)
   - Category comparison → Bar chart (horizontal for many categories)
   - Distribution → Histogram or box plot
   - Relationship → Scatter plot
   - Geographic → Map
   - Part-to-whole → Stacked bar or pie (if <5 slices)
6. Color usage:
   - Limit palette (3-5 colors)
   - Semantic colors (red=bad, green=good, yellow=warning)
   - Colorblind-friendly (avoid red-green only)
   - Consistent across dashboards
   - Use saturation for emphasis
7. KPI design:
   - Big number (main metric)
   - Context (vs previous period, vs target)
   - Sparkline (mini trend chart)
   - Color indicator (red/yellow/green)
   - Target line or marker
8. Layout principles:
   - F-pattern or Z-pattern reading
   - Group related metrics
   - Responsive (mobile-friendly)
   - Above the fold (important metrics visible)
   - Grid system (consistent spacing)
9. Interactivity:
   - Filters (date range, category, segment)
   - Drill-down (click for details)
   - Tooltips (hover for context)
   - Cross-filtering (select in one chart, filter others)
   - Export (PDF, CSV, image)
10. User personas:
    - Executive: High-level, few metrics, trends
    - Manager: Departmental, moderate detail
    - Analyst: All data, many filters, exploration
    - Operator: Real-time, alerts, specific metrics
11. Dashboard types by role:
    - Sales: Pipeline, conversion, revenue, forecast
    - Marketing: Traffic, leads, CAC, ROAS, conversion
    - Product: DAU, retention, feature adoption, NPS
    - Finance: Revenue, expenses, cash flow, runway
    - Operations: Uptime, errors, latency, throughput
    - Customer Success: Churn, health score, tickets
12. Storytelling with data:
    - Start with insight, not data
    - Clear narrative (what happened, why, what to do)
    - Annotations (mark important events)
    - Comparisons (vs last period, vs goal, vs benchmark)
    - Progressive disclosure (summary → detail)
13. Dashboard performance:
    - Pre-aggregate data (OLAP cubes, materialized views)
    - Limit data points (sample if needed)
    - Query optimization
    - Caching (Redis, CDN)
    - Incremental refresh (not full reload)
14. Mobile dashboards:
    - Vertical layout (stacked, not side-by-side)
    - Touch-friendly (large buttons, swipe)
    - Simplified (fewer metrics)
    - Fast loading (optimize images, lazy load)
15. Dashboard anti-patterns:
    - Too many metrics (information overload)
    - Misleading charts (truncated axis, 3D)
    - No context (just numbers, no comparison)
    - Vanity metrics (impressive but not actionable)
    - Pie charts with 10+ slices
    - Rainbow colors (no meaning)
16. Data visualization best practices:
    - Direct labeling (on chart, not legend)
    - Start Y-axis at zero (for bar/column charts)
    - Sort by value (not alphabetically)
    - Show uncertainty (confidence intervals, ranges)
    - Remove chart junk (unnecessary decorations)
17. Dashboard development process:
    - Understand audience and goals
    - Identify key metrics (3-7 KPIs)
    - Sketch layout (wireframe)
    - Build and iterate (user feedback)
    - Test usability
    - Deploy and monitor usage
18. Tools:
    - Tableau (powerful, enterprise)
    - Looker (SQL-based, embedded)
    - Power BI (Microsoft ecosystem)
    - Metabase (open-source, simple)
    - Grafana (monitoring, time-series)
    - Custom (React + Recharts/Chart.js)
19. Dashboard maintenance:
    - Data quality monitoring
    - Broken chart alerts
    - Usage analytics (which dashboards used?)
    - Regular updates (add new metrics, remove unused)
    - User feedback loop
20. Real dashboard examples:
    - SaaS metrics dashboard
    - E-commerce dashboard
    - DevOps monitoring
    - Marketing performance

Format: Include wireframe examples, chart selection guides, and dashboard templates.

Create the file now.
```

### Skill 6: Data Visualization

```
Create a comprehensive SKILL.md for Data Visualization best practices.

Location: 23-business-analytics/data-visualization/SKILL.md

Cover:
1. Data visualization principles (Edward Tufte, Stephen Few)
2. Chart types and use cases (comprehensive guide)
3. Color theory (palettes, accessibility, meaning)
4. Visual perception (preattentive attributes)
5. Chart design best practices
6. Interactive visualizations
7. Accessibility (WCAG, alt text, keyboard)
8. Tools: D3.js, Plotly, Chart.js, Matplotlib, ggplot2
9. Common mistakes (3D charts, truncated axes, etc.)
10. Mobile-responsive charts
11. Animation and transitions
12. Data-to-ink ratio
13. Real examples with code

Format: Include chart gallery, color palettes, and implementation code.

Create the file now.
```

### Skill 7: Funnel Analysis

```
Create a comprehensive SKILL.md for Funnel Analysis.

Location: 23-business-analytics/funnel-analysis/SKILL.md

Cover:
1. What is funnel analysis:
   - Tracking user journey through steps
   - Identify where users drop off
   - Optimize conversion at each stage
2. Types of funnels:
   - Linear (step 1 → 2 → 3)
   - Non-linear (users can skip steps)
   - Time-bound (must complete in X days)
   - Open (can enter at any step)
3. Common funnels:
   - Purchase: Visit → Product → Cart → Checkout → Complete
   - Signup: Landing → Register → Verify Email → Activate
   - SaaS: Trial → Use Feature → Upgrade → Payment
4. Funnel metrics:
   - Conversion rate per step
   - Overall conversion (end-to-end)
   - Drop-off rate (% who leave at each step)
   - Time to convert
5. Funnel SQL:
   - COUNT DISTINCT users at each step
   - Conversion rate = (users at step N+1) / (users at step N)
   - Filter by time window (7-day, 30-day)
6. Funnel visualization:
   - Traditional funnel chart (trapezoid)
   - Sankey diagram (flow between steps)
   - Bar chart (users per step)
7. Funnel optimization:
   - Focus on biggest drop-off
   - A/B test improvements
   - Remove friction
8. Segmented funnels:
   - By channel (organic vs paid)
   - By device (mobile vs desktop)
   - By cohort (new vs returning)
9. Time-to-convert analysis:
   - Median time between steps
   - Distribution (histogram)
   - Optimize slow steps
10. Micro vs macro funnels:
    - Macro: Overall user journey
    - Micro: Specific feature flow
11. Tools: Google Analytics, Mixpanel, Amplitude, SQL
12. Real funnel examples with SQL

Format: Include SQL queries, funnel visualizations, and optimization strategies.

Create the file now.
```

### Skill 8: KPI Metrics

```
Create a comprehensive SKILL.md for KPI (Key Performance Indicator) Metrics.

Location: 23-business-analytics/kpi-metrics/SKILL.md

Cover:
1. What are KPIs:
   - Measurable values showing performance
   - Aligned with business objectives
   - Actionable and trackable
2. Good KPI characteristics:
   - Specific (clear definition)
   - Measurable (quantifiable)
   - Achievable (realistic target)
   - Relevant (aligned with goals)
   - Time-bound (measured over period)
3. Types of KPIs:
   - Financial (revenue, profit, CAC, LTV)
   - Customer (NPS, churn, satisfaction)
   - Operational (uptime, response time)
   - Growth (MRR growth, user growth)
4. North Star Metric:
   - Single metric capturing core value
   - SaaS: Weekly Active Users
   - E-commerce: Orders per week
   - Marketplace: GMV (Gross Merchandise Value)
5. Leading vs lagging indicators:
   - Leading: Predict future (pipeline, trials)
   - Lagging: Historical (revenue, churn)
   - Balance both
6. Vanity vs actionable metrics:
   - Vanity: Looks good but not useful (total signups)
   - Actionable: Drives decisions (activation rate)
7. SaaS KPIs:
   - MRR/ARR (Monthly/Annual Recurring Revenue)
   - Churn rate (% customers leaving)
   - LTV (Lifetime Value)
   - CAC (Customer Acquisition Cost)
   - LTV:CAC ratio (should be >3:1)
   - Payback period (months to recover CAC)
   - NPS (Net Promoter Score)
8. E-commerce KPIs:
   - Conversion rate
   - Average Order Value (AOV)
   - Revenue per visitor
   - Cart abandonment rate
   - Customer retention rate
   - Repeat purchase rate
9. Product KPIs:
   - DAU/WAU/MAU (Daily/Weekly/Monthly Active Users)
   - Stickiness (DAU/MAU ratio)
   - Retention rate (D1, D7, D30)
   - Feature adoption
   - Time to value (TTV)
10. Marketing KPIs:
    - Traffic (visits, pageviews)
    - Leads generated
    - Lead-to-customer rate
    - CAC by channel
    - ROAS (Return on Ad Spend)
    - Content engagement
11. Financial KPIs:
    - Gross margin
    - Net profit margin
    - Burn rate (monthly cash spent)
    - Runway (months until cash runs out)
    - Rule of 40 (growth rate + profit margin >40%)
12. Customer Success KPIs:
    - Customer health score
    - Time to resolution (support tickets)
    - CSAT (Customer Satisfaction)
    - Expansion MRR (upsells)
13. KPI targets:
    - Set baseline (current performance)
    - Set stretch goal (ambitious)
    - Set timeline (quarterly, annually)
    - Review regularly
14. KPI dashboards:
    - Executive dashboard (5-7 KPIs)
    - Departmental dashboards (10-15 KPIs)
    - Update frequency (daily, weekly, monthly)
15. Metric definitions:
    - Document clearly (what counts? what doesn't?)
    - Example: "Active user = logged in + performed action in last 7 days"
    - Share with team (single source of truth)
16. OKRs (Objectives and Key Results):
    - Objective (qualitative goal)
    - Key Results (measurable KPIs)
    - Example: Objective: Improve retention
      * KR1: Increase D30 retention from 20% to 30%
      * KR2: Reduce churn from 5% to 3%
17. Pirate Metrics (AARRR):
    - Acquisition (how users find you)
    - Activation (first experience)
    - Retention (users come back)
    - Referral (users tell others)
    - Revenue (users pay)
18. Real KPI examples by company stage:
    - Startup: User growth, activation
    - Growth: Retention, LTV:CAC
    - Mature: Margin, efficiency

Format: Include KPI definitions, calculation formulas, and industry benchmarks.

Create the file now.
```

### Skill 9: SQL for Analytics

```
Create a comprehensive SKILL.md for SQL for Analytics.

Location: 23-business-analytics/sql-for-analytics/SKILL.md

Cover:
1. Analytics SQL vs transactional SQL:
   - Analytics: Aggregations, complex JOINs, window functions
   - Transactional: CRUD operations, normalization
2. Core analytics queries:
   - Aggregations: SUM, AVG, COUNT, MIN, MAX
   - GROUP BY with multiple dimensions
   - HAVING (filter aggregated results)
   - DISTINCT (unique counts)
3. Window functions:
   - ROW_NUMBER() for ranking
   - RANK() and DENSE_RANK() for ties
   - LAG() and LEAD() for row comparisons
   - Running totals: SUM() OVER (ORDER BY date)
   - Moving averages: AVG() OVER (ORDER BY date ROWS BETWEEN 6 PRECEDING AND CURRENT ROW)
   - PARTITION BY for grouped calculations
4. Date/time analysis:
   - DATE_TRUNC for grouping (day, week, month)
   - EXTRACT for parts (year, month, dow)
   - Date arithmetic (+ INTERVAL, date differences)
   - Fiscal calendar handling
   - Time zones (AT TIME ZONE)
5. Common analytics patterns:
   - Daily/weekly/monthly aggregations
   - Year-over-year comparisons
   - Cohort analysis (user retention)
   - Funnel analysis (conversion steps)
   - Retention curves
6. CTEs (Common Table Expressions):
   - WITH clause for readable queries
   - Break complex queries into steps
   - Recursive CTEs (hierarchies, graphs)
7. JOINs for analytics:
   - LEFT JOIN (keep all from left)
   - INNER JOIN (only matches)
   - SELF JOIN (compare rows in same table)
   - CROSS JOIN (cartesian product)
   - Multiple JOINs in one query
8. CASE statements:
   - Conditional logic in SELECT
   - Bucketing (age ranges, price tiers)
   - Pivot-like transformations
9. Subqueries:
   - Scalar subqueries (single value)
   - Correlated subqueries
   - Subqueries in SELECT, WHERE, FROM
10. Performance optimization:
    - EXPLAIN for query plans
    - Indexes on filter/join columns
    - Avoid SELECT * (specify columns)
    - Filter early (WHERE before JOIN)
    - Partition large tables
    - Materialized views
11. Advanced aggregations:
    - PERCENTILE_CONT() for median, quartiles
    - STRING_AGG() / ARRAY_AGG() for concatenation
    - FILTER clause (PostgreSQL): COUNT(*) FILTER (WHERE condition)
    - ROLLUP / CUBE for subtotals
12. Database-specific features:
    - PostgreSQL: JSON functions, LATERAL joins
    - MySQL: JSON_EXTRACT, GROUP_CONCAT
    - BigQuery: ARRAY, STRUCT, UNNEST
    - Snowflake: QUALIFY clause (filter window functions)
13. Analytics use cases:
    - Daily Active Users (DAU)
    - Monthly Recurring Revenue (MRR)
    - Cohort retention
    - Conversion funnel
    - Customer LTV
14. Testing queries:
    - Test with sample data first
    - Validate aggregations (spot check)
    - Check for NULLs
    - Verify date ranges
15. Query organization:
    - Formatting (consistent indentation)
    - Comments (explain complex logic)
    - Naming (descriptive CTEs)
    - Version control (Git)
16. Tools integration:
    - Jupyter notebooks (SQL magic)
    - dbt (analytics engineering)
    - BI tools (Looker, Metabase)
17. Common mistakes:
    - Cartesian products (missing JOIN condition)
    - NULL handling (use COALESCE)
    - GROUP BY without aggregation
    - Division by zero (use NULLIF)
18. Real SQL examples:
    - Monthly Active Users
    - Cohort retention query
    - Revenue by product category
    - Conversion funnel
    - Running total
    - Year-over-year growth

Format: Include SQL query examples (PostgreSQL syntax), optimization tips, and common patterns.

Create the file now.
```

# Batches 24-27: Security, i18n, Deployment & Team - Complete Prompts

Complete prompts for creating security, internationalization, deployment, and team collaboration skills.

---

## Batch 24: Security Practices

### Skill 1: Incident Response

```
Create a comprehensive SKILL.md for Incident Response (security incident handling).

Location: 24-security-practices/incident-response/SKILL.md

Cover:
1. What is incident response:
   - Systematic approach to handling security breaches
   - Minimize damage and recovery time
   - Prevent future incidents
2. Why incident response matters:
   - Faster containment (reduce blast radius)
   - Preserve evidence (for investigation)
   - Meet compliance requirements (SOC2, ISO 27001)
   - Maintain customer trust
3. Incident types:
   - Data breach (unauthorized access to data)
   - Malware infection (ransomware, trojans)
   - DDoS attack (service disruption)
   - Account compromise (stolen credentials)
   - Insider threat (malicious employee)
   - Supply chain attack (compromised dependency)
4. Incident response phases:
   - Preparation (before incident)
   - Detection and Analysis (incident identified)
   - Containment (stop the bleeding)
   - Eradication (remove threat)
   - Recovery (restore services)
   - Post-Incident Activity (lessons learned)
5. Preparation phase:
   - Incident response plan (documented procedures)
   - Incident response team (roles and responsibilities)
   - Tools and resources (forensics tools, backups)
   - Training and drills (tabletop exercises)
   - Contact lists (internal, external, vendors)
6. Detection and analysis:
   - Monitoring and alerting (SIEM, IDS/IPS)
   - Log analysis (correlate events)
   - Threat intelligence (known attack patterns)
   - Initial assessment (severity, scope, impact)
7. Incident severity levels:
   - SEV1/Critical: Massive impact (data breach, complete outage)
   - SEV2/High: Significant impact (partial outage, active attack)
   - SEV3/Medium: Moderate impact (suspicious activity)
   - SEV4/Low: Minor impact (failed login attempts)
8. Containment strategies:
   - Short-term containment (isolate affected systems)
   - Long-term containment (patch vulnerabilities)
   - Evidence preservation (forensic images, logs)
   - Decision: Rebuild or clean infected systems?
9. Eradication:
   - Remove malware, backdoors, unauthorized access
   - Patch vulnerabilities exploited
   - Reset compromised credentials
   - Verify threat is eliminated
10. Recovery:
    - Restore systems from clean backups
    - Verify system integrity
    - Monitor for reinfection
    - Gradual return to normal operations
11. Post-incident activity:
    - Incident report (timeline, impact, actions taken)
    - Root cause analysis (how did this happen?)
    - Lessons learned (what went well, what didn't)
    - Update response plan and controls
12. Communication:
    - Internal: Executive team, affected teams
    - External: Customers, partners, regulators, media
    - Timing: When to notify (legal requirements)
    - Message: Transparent but controlled
13. Legal and compliance:
    - Data breach notification laws (GDPR 72 hours, state laws)
    - Evidence preservation (chain of custody)
    - Law enforcement involvement (when required)
    - Legal counsel (consult before public statements)
14. Incident response team roles:
    - Incident Commander (overall coordination)
    - Technical Lead (investigation and remediation)
    - Communications Lead (internal and external comms)
    - Legal/Compliance (regulatory requirements)
15. Tools for incident response:
    - SIEM (Splunk, ELK, Datadog)
    - Forensics (EnCase, FTK, Autopsy)
    - Network analysis (Wireshark, tcpdump)
    - Malware analysis (sandbox, reverse engineering)
16. Runbooks for common incidents:
    - Data breach response
    - Ransomware response
    - DDoS mitigation
    - Account takeover response
17. Metrics to track:
    - Mean time to detect (MTTD)
    - Mean time to respond (MTTR)
    - Number of incidents per month
    - False positive rate
18. Tabletop exercises:
    - Simulate incident scenarios
    - Test response procedures
    - Identify gaps
    - Train team members
19. Third-party incident response:
    - When to engage external help (major breach)
    - Incident response retainers
    - Cyber insurance
20. Real incident examples:
    - SQL injection leading to data breach
    - Ransomware attack
    - Compromised credentials

Format: Include incident response templates, runbooks, and communication templates.

Create the file now.
```

### Skill 2: OWASP Top 10

```
Create a comprehensive SKILL.md for OWASP Top 10 (common web vulnerabilities).

Location: 24-security-practices/owasp-top-10/SKILL.md

Cover:
1. What is OWASP Top 10:
   - List of most critical web app security risks
   - Updated every 3-4 years (2021 is latest)
   - Industry standard for web security
2. A01: Broken Access Control:
   - Description: Users access resources they shouldn't
   - Examples: View other users' data, admin functions without auth
   - Prevention: Deny by default, check permissions server-side, log access
3. A02: Cryptographic Failures:
   - Description: Sensitive data exposed due to weak/missing encryption
   - Examples: Passwords in plaintext, weak hashing (MD5), unencrypted transmission
   - Prevention: Encrypt at rest (AES-256), encrypt in transit (TLS), use bcrypt/Argon2 for passwords
4. A03: Injection:
   - Description: Malicious data sent to interpreter (SQL, NoSQL, OS, LDAP)
   - SQL Injection: `' OR '1'='1` bypassing authentication
   - Prevention: Parameterized queries, ORM, input validation, least privilege DB user
5. A04: Insecure Design:
   - Description: Missing or ineffective security controls by design
   - Examples: No rate limiting, weak password policy, lack of MFA
   - Prevention: Threat modeling, secure design patterns, defense in depth
6. A05: Security Misconfiguration:
   - Description: Insecure default configs, incomplete setups, open cloud storage
   - Examples: Default admin/admin, unnecessary services enabled, verbose errors
   - Prevention: Hardening guides, automated config scanning, minimal installs
7. A06: Vulnerable and Outdated Components:
   - Description: Using libraries with known vulnerabilities
   - Examples: Old versions of React, Express, OpenSSL
   - Prevention: Dependency scanning (Dependabot, Snyk), regular updates, remove unused dependencies
8. A07: Identification and Authentication Failures:
   - Description: Broken auth mechanisms
   - Examples: Weak passwords allowed, no MFA, session fixation, credential stuffing
   - Prevention: Strong password policy, MFA, secure session management, rate limiting
9. A08: Software and Data Integrity Failures:
   - Description: Code/infrastructure without integrity verification
   - Examples: Supply chain attacks, unsigned updates, insecure CI/CD
   - Prevention: Code signing, verify dependencies (lockfiles), secure CI/CD pipeline
10. A09: Security Logging and Monitoring Failures:
    - Description: Insufficient logging, no alerting on suspicious activity
    - Examples: No login attempt logs, no audit trail, alerts not monitored
    - Prevention: Comprehensive logging, SIEM, real-time alerts, log retention
11. A10: Server-Side Request Forgery (SSRF):
    - Description: App fetches remote resource without validating URL
    - Examples: Attacker forces app to read internal network, cloud metadata endpoint
    - Prevention: Whitelist allowed hosts, network segmentation, validate and sanitize URLs
12. Testing for OWASP Top 10:
    - Manual testing (try common attacks)
    - Automated scanners (OWASP ZAP, Burp Suite)
    - Code review (spot vulnerabilities in code)
    - Penetration testing (hire ethical hackers)
13. Prevention checklist:
    - Input validation (whitelist, not blacklist)
    - Output encoding (prevent XSS)
    - Parameterized queries (prevent SQL injection)
    - Authentication and authorization on every request
    - HTTPS everywhere
    - Security headers (CSP, HSTS, X-Frame-Options)
14. Security headers:
    - Content-Security-Policy (prevent XSS)
    - Strict-Transport-Security (force HTTPS)
    - X-Content-Type-Options (prevent MIME sniffing)
    - X-Frame-Options (prevent clickjacking)
15. Secure coding practices:
    - Principle of least privilege
    - Defense in depth (multiple layers)
    - Fail securely (errors don't expose info)
    - Keep security simple (complexity = bugs)
16. Developer security training:
    - OWASP Top 10 awareness
    - Secure coding practices
    - Common vulnerability patterns
    - Regular security updates
17. Tools for OWASP Top 10:
    - SAST (Static Application Security Testing): SonarQube, Checkmarx
    - DAST (Dynamic Application Security Testing): OWASP ZAP, Burp Suite
    - Dependency scanning: Snyk, Dependabot
18. Real vulnerability examples:
    - SQL injection in login form
    - XSS in comment section
    - Broken access control in API

Format: Include vulnerability examples, attack scenarios, and prevention code snippets.

Create the file now.
```

### Skill 3: Penetration Testing

```
Create a comprehensive SKILL.md for Penetration Testing (ethical hacking).

Location: 24-security-practices/penetration-testing/SKILL.md

Cover:
1. What is penetration testing:
   - Simulated cyberattack on your systems
   - Identify vulnerabilities before attackers do
   - Ethical hacking with permission
2. Types of pen tests:
   - Black box (no prior knowledge)
   - White box (full knowledge of systems)
   - Gray box (partial knowledge)
3. Pen testing phases:
   - Reconnaissance (gather information)
   - Scanning (identify vulnerabilities)
   - Gaining access (exploit vulnerabilities)
   - Maintaining access (persistence)
   - Covering tracks (hide evidence)
   - Reporting (document findings)
4. Reconnaissance:
   - Passive (OSINT, public records, social media)
   - Active (port scanning, service enumeration)
   - Tools: Google dorking, Shodan, WHOIS
5. Scanning:
   - Port scanning (Nmap)
   - Vulnerability scanning (Nessus, OpenVAS)
   - Web app scanning (OWASP ZAP, Burp Suite)
6. Exploitation:
   - Exploit known vulnerabilities (Metasploit)
   - Custom exploits (for unique vulns)
   - Social engineering (phishing, pretexting)
   - Password attacks (brute force, dictionary)
7. Common targets:
   - Web applications (OWASP Top 10)
   - Network infrastructure (firewalls, routers)
   - APIs (authentication, authorization)
   - Mobile apps (reverse engineering)
   - Cloud infrastructure (misconfigurations)
8. Tools:
   - Kali Linux (pen testing distro)
   - Nmap (port scanning)
   - Metasploit (exploitation framework)
   - Burp Suite (web app testing)
   - Wireshark (network analysis)
   - John the Ripper (password cracking)
9. Web app testing:
   - SQL injection
   - XSS (stored, reflected, DOM-based)
   - CSRF (cross-site request forgery)
   - Authentication bypass
   - Authorization flaws
10. API testing:
    - Broken authentication
    - Excessive data exposure
    - Lack of rate limiting
    - Injection flaws
11. Network testing:
    - Firewall bypass
    - Man-in-the-middle attacks
    - ARP spoofing
    - DNS poisoning
12. Reporting:
    - Executive summary (high-level findings)
    - Technical details (step-by-step reproduction)
    - Risk ratings (critical, high, medium, low)
    - Remediation recommendations
    - Evidence (screenshots, logs)
13. Pen test frequency:
    - Annual comprehensive test
    - Quarterly targeted tests
    - After major changes
    - Before major launches
14. Compliance requirements:
    - PCI DSS (annual pen test required)
    - SOC2 (security testing required)
    - HIPAA (vulnerability scanning required)
15. In-house vs outsourced:
    - In-house: Continuous, cheaper, less expertise
    - Outsourced: Expert perspective, unbiased, certification
16. Bug bounty programs:
    - Crowdsourced security testing
    - Pay for valid vulnerabilities
    - Platforms: HackerOne, Bugcrowd
17. Legal and ethical:
    - Always get written permission
    - Define scope (what's in/out)
    - Non-disclosure agreements
    - Report findings responsibly
18. Real pen test scenarios:
    - Web app security assessment
    - Network infrastructure test
    - Cloud security review

Format: Include testing methodologies, tool usage examples, and report templates.

Create the file now.
```

### Skill 4: Secure Coding

```
Create a comprehensive SKILL.md for Secure Coding practices.

Location: 24-security-practices/secure-coding/SKILL.md

Cover:
1. Secure coding principles
2. Input validation and sanitization
3. Output encoding (prevent XSS)
4. SQL injection prevention
5. Authentication and session management
6. Authorization checks
7. Error handling (don't leak info)
8. Cryptography best practices
9. Secure file handling
10. API security
11. Code review for security
12. SAST tools integration
13. Security linting rules
14. Language-specific security (Node.js, Python, Java)
15. Real code examples (vulnerable vs secure)

Format: Include code examples, security patterns, and vulnerability demos.

Create the file now.
```

### Skill 5: Security Audit

```
Create a comprehensive SKILL.md for Security Audit (systematic security review).

Location: 24-security-practices/security-audit/SKILL.md

Cover:
1. What is security audit
2. Audit types (internal, external, compliance)
3. Audit scope and planning
4. Security controls review
5. Code review for security
6. Configuration review
7. Access control audit
8. Log review and analysis
9. Vulnerability assessment
10. Compliance verification (SOC2, ISO 27001)
11. Audit findings and risk rating
12. Remediation planning
13. Audit reporting
14. Follow-up and verification
15. Continuous audit (automated checks)

Format: Include audit checklists, finding templates, and remediation guides.

Create the file now.
```

### Skill 6: Vulnerability Management

```
Create a comprehensive SKILL.md for Vulnerability Management.

Location: 24-security-practices/vulnerability-management/SKILL.md

Cover:
1. Vulnerability lifecycle (discovery, assessment, remediation, verification)
2. Vulnerability sources (scanners, pen tests, bug bounty, CVE databases)
3. Vulnerability scanning (Nessus, OpenVAS, Qualys)
4. Dependency scanning (Snyk, Dependabot, npm audit)
5. Vulnerability prioritization (CVSS score, exploitability, business impact)
6. Patch management (testing, deployment, rollback)
7. Virtual patching (WAF rules as temporary fix)
8. Vulnerability tracking (Jira, GitHub Issues)
9. Metrics (time to patch, open vulnerabilities by severity)
10. Compliance requirements (PCI DSS, SOC2)
11. Tools integration with CI/CD
12. Real examples: Critical CVE response workflow

Format: Include vulnerability management workflows, prioritization frameworks, and tool configurations.

Create the file now.
```

---

## Batch 25: Internationalization (i18n)

### Skill 1: Currency & Timezone

```
Create a comprehensive SKILL.md for Currency and Timezone handling.

Location: 25-internationalization/currency-timezone/SKILL.md

Cover:
1. Why currency and timezone matter:
   - Global applications need localization
   - User expectations (local currency, local time)
   - Business requirements (multi-currency payments)
2. Timezone fundamentals:
   - UTC (Coordinated Universal Time) as baseline
   - Timezone offsets (UTC+7 for Bangkok)
   - Daylight Saving Time (DST) complications
   - IANA timezone database (America/New_York)
3. Storing dates and times:
   - Always store in UTC in database
   - Convert to user's timezone for display
   - Database types: TIMESTAMP WITH TIME ZONE (PostgreSQL)
4. JavaScript timezone handling:
   - Date object (uses browser timezone)
   - Intl.DateTimeFormat for formatting
   - Libraries: date-fns-tz, Luxon, Day.js
   - Moment.js (deprecated, use alternatives)
5. Server-side timezone handling:
   - Python: pytz, dateutil
   - Node.js: date-fns-tz, Luxon
   - Java: ZonedDateTime, Instant
6. User timezone detection:
   - Browser: Intl.DateTimeFormat().resolvedOptions().timeZone
   - Server: User profile setting (preferred)
   - IP geolocation (fallback, less accurate)
7. Common timezone patterns:
   - User sets timezone in profile
   - Display all dates in user's timezone
   - Store all dates in UTC
   - Convert UTC → user timezone on read
   - Convert user timezone → UTC on write
8. Timezone edge cases:
   - DST transitions (spring forward, fall back)
   - Ambiguous times (2:30 AM on DST change)
   - Non-existent times (2:30 AM doesn't exist in spring)
   - Timezone changes (countries change timezone)
9. Currency fundamentals:
   - Currency codes (ISO 4217): USD, EUR, THB
   - Currency symbols ($, €, ฿)
   - Decimal precision (2 for most, 0 for JPY)
10. Storing currency:
    - Store amount + currency code
    - Use DECIMAL type (not FLOAT - precision issues)
    - Example: amount: 99.99, currency: "USD"
11. Currency formatting:
    - Intl.NumberFormat (browser and Node.js)
    - Different formats by locale (1,000.00 vs 1.000,00)
    - Symbol position ($100 vs 100$)
12. Multi-currency support:
    - Display prices in user's currency
    - Store prices in base currency
    - Exchange rate API (openexchangerates.org)
    - Update rates periodically
    - Cache exchange rates
13. Currency conversion:
    - Base currency (e.g., USD)
    - Convert to display currency using exchange rate
    - Show original currency in tooltip
    - Let user switch currency
14. Payment processing:
    - Charge in customer's currency (better UX)
    - Stripe supports 135+ currencies
    - Currency conversion handled by payment processor
15. Accounting considerations:
    - Precision (use DECIMAL, not FLOAT)
    - Rounding (banker's rounding, half-even)
    - Tax calculation in specific currency
16. Libraries:
    - JavaScript: Intl API, dinero.js, currency.js
    - Python: Babel, forex-python
    - Java: Joda-Money, JSR 354
17. Common mistakes:
    - Using FLOAT for currency (precision loss)
    - Not storing timezone with dates
    - Assuming user is in server timezone
    - Hardcoding currency symbols
18. Implementation examples:
    - Timezone conversion function
    - Currency formatter component
    - Multi-currency price display

Format: Include code examples, conversion utilities, and edge case handling.

Create the file now.
```

### Skill 2: i18n Setup

```
Create a comprehensive SKILL.md for i18n (Internationalization) Setup.

Location: 25-internationalization/i18n-setup/SKILL.md

Cover:
1. What is i18n:
   - Designing app to support multiple languages
   - Separate content from code
   - Enable localization (l10n) for specific regions
2. i18n vs l10n:
   - i18n: Making app translatable (developer work)
   - l10n: Translating app to specific language (translator work)
3. i18n architecture:
   - Locale (language + region): en-US, th-TH, pt-BR
   - Translation files (JSON, YAML, gettext .po)
   - Translation function (t('key'))
   - Locale switching
4. Translation file structure:
   - JSON format (most common)
   - Nested keys for organization
   - Pluralization rules
   - Variable interpolation
5. i18n libraries:
   - React: react-i18next, react-intl
   - Vue: vue-i18n
   - Angular: @angular/localize
   - Node.js: i18next
   - Python: gettext, Babel
6. react-i18next setup:
   - Install: i18next, react-i18next
   - Configure i18n instance
   - Load translation files
   - Wrap app with I18nextProvider
   - Use useTranslation hook
7. Translation keys:
   - Descriptive keys (common.submit vs submit)
   - Namespace organization (auth.login, auth.signup)
   - Default values (fallback text)
8. Dynamic content:
   - Variable interpolation: t('greeting', { name: 'John' })
   - HTML content: Trans component
   - Pluralization: t('items', { count: 5 })
9. Pluralization rules:
   - English: 0/1 vs 2+
   - Arabic: 0, 1, 2, 3-10, 11-99, 100+
   - i18next handles automatically
10. Date and number formatting:
    - Intl.DateTimeFormat
    - Intl.NumberFormat
    - Library integration (react-intl)
11. Language detection:
    - Browser language (navigator.language)
    - User preference (stored in profile)
    - URL parameter (?lang=th)
    - Subdomain (th.example.com)
    - Cookie
12. Language switching:
    - i18n.changeLanguage('th')
    - Persist preference (localStorage, database)
    - Reload content
13. RTL (Right-to-Left) support:
    - Arabic, Hebrew
    - dir="rtl" attribute
    - CSS logical properties (start vs left)
    - Flip layouts and icons
14. Translation workflow:
    - Developer extracts keys
    - Export to translation management system
    - Translator translates
    - Import translations back
    - Deploy
15. Translation management:
    - Platforms: Lokalise, Crowdin, Phrase
    - CSV export/import (simple)
    - Git-based workflow (JSON files)
16. Missing translations:
    - Show key (for developers)
    - Show default language (for users)
    - Log missing keys
17. SEO considerations:
    - Separate URLs per language (/en/, /th/)
    - Hreflang tags
    - Language selector
    - Translated meta tags
18. Performance:
    - Lazy load translations (per page/route)
    - Bundle only needed languages
    - Cache translations
19. Testing:
    - Test all languages
    - Screenshot testing (visual regression)
    - Pseudo-localization (test string expansion)
20. Common mistakes:
    - Hardcoded strings
    - Concatenating translations
    - Not handling pluralization
    - Not supporting RTL
21. Implementation examples:
    - React i18next setup
    - Translation file structure
    - Language switcher component

Format: Include setup code, translation file examples, and component patterns.

Create the file now.
```

### Skill 3: Localization

```
Create a comprehensive SKILL.md for Localization (l10n) - adapting to specific locales.

Location: 25-internationalization/localization/SKILL.md

Cover:
1. What is localization (beyond translation)
2. Cultural considerations (colors, images, symbols)
3. Date and time formats (MM/DD/YYYY vs DD/MM/YYYY)
4. Number formats (1,000.00 vs 1.000,00)
5. Currency display
6. Address formats (different by country)
7. Phone number formats
8. Name formats (first/last vs last/first)
9. Measurement units (metric vs imperial)
10. Legal and compliance (local laws)
11. Payment methods (local preferences)
12. Holidays and business hours
13. Locale-specific content
14. Testing localization
15. Real examples: US vs Europe vs Asia localization

Format: Include locale-specific patterns, format examples, and cultural guidelines.

Create the file now.
```

### Skill 4: Multi-Language

```
Create a comprehensive SKILL.md for Multi-Language Content Management.

Location: 25-internationalization/multi-language/SKILL.md

Cover:
1. Content types needing translation
2. Database schema for multi-language (separate tables vs JSON column)
3. CMS for multi-language content
4. Translation workflow (draft, review, publish)
5. Version control for translations
6. Fallback strategies (missing translation)
7. User-generated content translation
8. Machine translation (Google Translate API)
9. Professional translation services
10. Quality assurance
11. Content synchronization (when source changes)
12. SEO for multi-language sites
13. Real examples: Blog, product catalog, docs

Format: Include database schemas, CMS patterns, and translation workflows.

Create the file now.
```

### Skill 5: RTL Support

```
Create a comprehensive SKILL.md for RTL (Right-to-Left) Support.

Location: 25-internationalization/rtl-support/SKILL.md

Cover:
1. What is RTL (Arabic, Hebrew, Persian)
2. HTML dir attribute (dir="rtl")
3. CSS for RTL (logical properties)
4. BiDi (bidirectional text)
5. Flipping layouts (flex-direction, text-align)
6. Flipping icons and images
7. Not flipping (numbers, latin text)
8. RTL testing
9. Tools: RTL plugins, browser extensions
10. Common issues and solutions
11. Implementation: CSS-in-JS with RTL, Tailwind RTL
12. Real examples: RTL e-commerce, RTL dashboard

Format: Include CSS patterns, layout examples, and testing strategies.

Create the file now.
```

---

## Batch 26: Deployment Strategies

### Skill 1: Blue-Green Deployment

```
Create a comprehensive SKILL.md for Blue-Green Deployment.

Location: 26-deployment-strategies/blue-green-deployment/SKILL.md

Cover:
1. What is blue-green deployment:
   - Two identical production environments (blue and green)
   - Blue is live, green is staging
   - Deploy to green, test, then switch traffic
   - Instant rollback (switch back to blue)
2. Why blue-green deployment:
   - Zero-downtime deployments
   - Easy rollback (just switch back)
   - Full testing in production environment
   - Reduce deployment risk
3. Architecture:
   - Load balancer (routes traffic)
   - Blue environment (current production)
   - Green environment (new version)
   - Shared database or separate databases
4. Deployment process:
   - Deploy new version to green environment
   - Run smoke tests on green
   - Switch load balancer to green
   - Monitor for issues
   - Keep blue running (for rollback)
   - If successful, blue becomes next staging
5. Traffic switching:
   - DNS switch (slow, DNS caching)
   - Load balancer switch (instant, recommended)
   - Router configuration
6. Database challenges:
   - Shared database: Schema migrations must be backward compatible
   - Separate databases: Data synchronization needed
   - Solution: Backward-compatible migrations
7. Rollback:
   - Switch load balancer back to blue
   - Instant rollback (seconds)
   - No code changes needed
8. Cost considerations:
   - Double infrastructure (expensive)
   - Optimization: Scale down inactive environment
   - Cloud auto-scaling helps
9. Implementation:
   - AWS: Elastic Load Balancer + Auto Scaling Groups
   - Kubernetes: Service with label selectors
   - Cloud providers: Built-in support (AWS Elastic Beanstalk)
10. Database migration strategy:
    - Version N: Add new column (nullable)
    - Deploy application using new column
    - Version N+1: Make column non-nullable
    - Version N+2: Remove old column
11. Session handling:
    - Stateless apps (no issue)
    - Sticky sessions (user stays on same version)
    - Shared session store (Redis)
12. Monitoring:
    - Monitor both environments
    - Compare error rates
    - Alert on anomalies
13. Testing in green:
    - Synthetic monitoring
    - Canary requests (small % of real traffic)
    - Internal testing
14. When to use blue-green:
    - Zero-downtime requirement
    - Need instant rollback
    - Can afford double infrastructure
    - Stateless or session-compatible apps
15. When NOT to use:
    - Database changes are complex
    - Cost-prohibitive (small team)
    - Stateful apps without shared state
16. Variations:
    - Red-black deployment (same concept)
    - A/B deployment (traffic split, not full switch)
17. Tools:
    - AWS: CodeDeploy, Elastic Beanstalk
    - Kubernetes: Built-in (change service selector)
    - Cloud Foundry: Blue-green deployment plugin
    - Terraform: Create/destroy environments
18. Real examples:
    - E-commerce site deployment
    - API service deployment
    - Kubernetes blue-green

Format: Include architecture diagrams, deployment scripts, and rollback procedures.

Create the file now.
```

### Skill 2: Canary Deployment

```
Create a comprehensive SKILL.md for Canary Deployment.

Location: 26-deployment-strategies/canary-deployment/SKILL.md

Cover:
1. What is canary deployment:
   - Gradual rollout to subset of users
   - Start with 5%, then 25%, 50%, 100%
   - Monitor metrics at each stage
   - Rollback if issues detected
2. Why canary deployment:
   - Reduce blast radius (only affects small %)
   - Real-world testing (actual users)
   - Early issue detection
   - Confidence building (gradual expansion)
3. Canary process:
   - Deploy new version to canary servers
   - Route 5% traffic to canary
   - Monitor key metrics (errors, latency, business KPIs)
   - If healthy, increase to 25%, 50%, 100%
   - If unhealthy, rollback
4. Traffic routing:
   - Load balancer with weights (95% old, 5% new)
   - Service mesh (Istio, Linkerd)
   - Feature flags with % rollout
   - DNS (less common, caching issues)
5. Canary metrics:
   - Error rate (should not increase)
   - Latency (P95, P99)
   - Business metrics (conversion, revenue)
   - Resource usage (CPU, memory)
6. Canary decision:
   - Automated: If metrics within threshold, proceed
   - Manual: Human reviews metrics and decides
   - Hybrid: Auto proceed unless anomaly
7. Canary duration:
   - Fast canary: 10 min per stage (for small changes)
   - Slow canary: Hours or days per stage (for risky changes)
   - Soak time: Let it run before next stage
8. User selection:
   - Random users (most common)
   - Internal users first (dogfooding)
   - Beta testers (opt-in users)
   - Specific segments (e.g., free tier first)
9. Automated canary with Flagger:
   - Kubernetes-native canary deployment
   - Integrates with Istio/Linkerd
   - Automated promotion based on metrics
10. Monitoring and alerting:
    - Dashboards showing old vs new metrics
    - Alerts for anomalies (error spike)
    - Real-time decision making
11. Rollback:
    - Automatic rollback on threshold breach
    - Manual rollback button
    - Fast rollback (shift traffic back)
12. Database challenges:
    - Backward-compatible schema changes
    - Both versions must work with same schema
13. Session handling:
    - Sticky sessions (user stays on same version)
    - Or stateless (no issue)
14. Progressive delivery:
    - Canary + feature flags
    - Fine-grained control
    - A/B testing + canary
15. Tools:
    - Kubernetes: Flagger, Argo Rollouts
    - AWS: CodeDeploy with traffic shifting
    - Service mesh: Istio, Linkerd
    - Feature flags: LaunchDarkly, Split.io
16. Canary vs blue-green:
    - Canary: Gradual, lower risk, slower
    - Blue-green: All-at-once, fast rollback, more expensive
17. Real examples:
    - API service canary
    - Frontend deployment with canary
    - Kubernetes canary with Flagger
18. Canary anti-patterns:
    - Not monitoring metrics (blind canary)
    - Increasing too fast (defeats purpose)
    - No rollback plan

Format: Include traffic routing configs, metric monitoring setups, and rollback scripts.

Create the file now.
```

### Skill 3: Feature Toggles

```
Create a comprehensive SKILL.md for Feature Toggles (Feature Flags).

Location: 26-deployment-strategies/feature-toggles/SKILL.md

Cover:
1. What are feature toggles:
   - Runtime switches to enable/disable features
   - Deploy code without activating
   - Decouple deployment from release
2. Types of feature toggles:
   - Release toggles (temporary, for gradual rollout)
   - Experiment toggles (A/B testing)
   - Ops toggles (circuit breakers, kill switches)
   - Permission toggles (enable for specific users/plans)
3. Why feature toggles:
   - Trunk-based development (no long-lived branches)
   - Dark launches (deploy but don't activate)
   - Gradual rollout (enable for 5%, 50%, 100%)
   - Kill switch (disable feature if issues)
   - A/B testing
4. Feature toggle implementation:
   - Simple: if (featureEnabled('new-checkout')) { ... }
   - Config file (JSON, YAML)
   - Database (dynamic, requires DB query)
   - Feature flag service (LaunchDarkly, Split.io, Unleash)
5. Toggle configuration:
   - Boolean (on/off)
   - Percentage rollout (20% of users)
   - User targeting (specific user IDs)
   - Segment targeting (beta users, paid users)
   - Environment-based (on in prod, off in staging)
6. Toggle evaluation:
   - Server-side (backend checks flag)
   - Client-side (frontend checks flag)
   - Hybrid (some server, some client)
7. Gradual rollout with toggles:
   - Start at 0% (dark launch, code deployed but off)
   - Enable for internal users (dogfooding)
   - Ramp to 5% of users
   - Ramp to 50%, then 100%
   - Remove toggle after fully rolled out
8. A/B testing with toggles:
   - Variant A (50% of users)
   - Variant B (50% of users)
   - Measure metrics for each
   - Winner becomes default
9. Kill switch:
   - Quickly disable feature if issues
   - No redeployment needed
   - Example: Disable payments if payment gateway down
10. Toggle lifecycle:
    - Create toggle (for new feature)
    - Use during development (off by default)
    - Enable gradually (rollout)
    - Feature fully released
    - **Remove toggle** (technical debt if left)
11. Toggle debt:
    - Old toggles = complexity
    - Regular cleanup (remove after full rollout)
    - Set expiration dates on toggles
12. Feature flag services:
    - LaunchDarkly: Enterprise, robust
    - Split.io: A/B testing focus
    - Unleash: Open-source
    - Flagsmith: Open-source
    - ConfigCat: Simple, affordable
13. DIY feature flags:
    - Config file (simple, requires redeploy)
    - Database table (dynamic, adds latency)
    - Redis (fast, requires Redis)
14. Performance considerations:
    - Cache flag values (don't query every request)
    - Evaluate flags once per request
    - Minimal overhead
15. Testing with toggles:
    - Test both paths (on and off)
    - Integration tests with toggles enabled/disabled
    - Feature branch testing (toggle on)
16. Multi-variate flags:
    - Not just on/off, but multiple variants
    - Example: new-ui-v1, new-ui-v2, new-ui-v3
17. Toggle best practices:
    - Short-lived release toggles (remove after rollout)
    - Long-lived permission toggles (for plans)
    - Descriptive names (new-checkout, not flag-123)
    - Default to off (safe default)
18. Toggle anti-patterns:
    - Toggle everywhere (overuse)
    - Not removing old toggles (debt)
    - Complex toggle logic (if A && B && !C...)
19. Real examples:
    - Feature rollout with LaunchDarkly
    - A/B test with feature flags
    - Kill switch for critical feature
20. Implementation:
    - Simple boolean flag
    - Percentage rollout
    - LaunchDarkly integration

Format: Include code examples, flag configurations, and rollout strategies.

Create the file now.
```

### Skill 4: Rollback Strategies

```
Create a comprehensive SKILL.md for Rollback Strategies.

Location: 26-deployment-strategies/rollback-strategies/SKILL.md

Cover:
1. What is rollback (reverting to previous version)
2. Why rollback is needed (deployment issues)
3. Types of rollback (full, partial, forward fix)
4. Rollback triggers (manual, automated)
5. Blue-green rollback (instant, switch traffic back)
6. Canary rollback (stop rollout, shift traffic)
7. Rolling update rollback (Kubernetes)
8. Database rollback (complex, often not feasible)
9. Forward fix (fix bug in new version, deploy again)
10. Rollback testing (test rollback in staging)
11. Automated rollback (metric-based)
12. Rollback vs rollforward
13. Post-rollback analysis
14. Tools: Kubernetes rollback, cloud provider rollback
15. Real examples: Rollback scenarios and procedures

Format: Include rollback procedures, decision trees, and automation scripts.

Create the file now.
```

### Skill 5: Rolling Deployment

```
Create a comprehensive SKILL.md for Rolling Deployment.

Location: 26-deployment-strategies/rolling-deployment/SKILL.md

Cover:
1. What is rolling deployment (gradual replacement of instances)
2. Rolling update process (1 at a time or N at a time)
3. Zero-downtime with rolling updates
4. Health checks (wait for healthy before next)
5. Kubernetes rolling update (default strategy)
6. Max unavailable and max surge
7. Rollback during rolling update
8. Database schema compatibility
9. Session handling during rolling update
10. Monitoring rolling updates
11. Tools: Kubernetes, ECS, Cloud Foundry
12. Real examples: Rolling update configurations

Format: Include deployment configs, health check setups, and rollback procedures.

Create the file now.
```

---

## Batch 27: Team Collaboration

### Skill 1: Code Review Culture

```
Create a comprehensive SKILL.md for Code Review Culture.

Location: 27-team-collaboration/code-review-culture/SKILL.md

Cover:
1. Why code review matters:
   - Catch bugs before production
   - Knowledge sharing (team learns from each other)
   - Maintain code quality and consistency
   - Onboard new team members
2. Code review objectives:
   - Correctness (does it work?)
   - Quality (is it well-written?)
   - Readability (can others understand?)
   - Design (is the approach sound?)
   - Tests (adequate coverage?)
   - Security (any vulnerabilities?)
3. What to review:
   - Logic correctness
   - Edge cases handled
   - Error handling
   - Test coverage
   - Code style (formatting, naming)
   - Performance implications
   - Security vulnerabilities
   - Documentation
4. Code review process:
   - Developer creates PR (pull request)
   - Automated checks run (CI, linting, tests)
   - Reviewers assigned (1-2 people)
   - Reviewers provide feedback
   - Developer addresses feedback
   - Approval and merge
5. Review size:
   - Small PRs (< 400 lines) - easier to review
   - Large PRs (> 1000 lines) - hard to review thoroughly
   - Break up large changes into smaller PRs
6. Review turnaround time:
   - Goal: Review within 24 hours
   - Fast feedback keeps momentum
   - Blocked PRs slow down team
7. Giving feedback:
   - Be kind and constructive
   - Explain the "why" (not just "change this")
   - Suggest alternatives
   - Ask questions instead of demanding
   - Praise good work
8. Review comment types:
   - Blocking: Must fix before merge (security issue)
   - Non-blocking: Nice-to-have (nitpick)
   - Question: Asking for clarification
   - Praise: Recognizing good work
9. Receiving feedback:
   - Don't take it personally (it's about the code)
   - Ask for clarification if unclear
   - Discuss disagreements respectfully
   - Learn from feedback
10. Review checklist:
    - [ ] Code works as intended
    - [ ] Tests added/updated
    - [ ] Edge cases handled
    - [ ] Error handling present
    - [ ] No obvious bugs
    - [ ] Readable and maintainable
    - [ ] Follows style guide
    - [ ] No security issues
    - [ ] Documentation updated
11. Automated checks:
    - Linting (ESLint, Pylint)
    - Formatting (Prettier, Black)
    - Tests (unit, integration)
    - Type checking (TypeScript, mypy)
    - Security scanning (Snyk, CodeQL)
12. Review tools:
    - GitHub Pull Requests
    - GitLab Merge Requests
    - Bitbucket Pull Requests
    - Gerrit
    - Phabricator
13. Review best practices:
    - Review promptly (don't block teammates)
    - Focus on important issues (not nitpicks)
    - Automate what can be automated
    - Set time limits (30 min per review)
    - Synchronous discussion for complex topics
14. Common review mistakes:
    - Rubber-stamping (approving without reading)
    - Nitpicking (focusing on trivial issues)
    - Not explaining feedback
    - Long delays
15. Self-review:
    - Review your own code before submitting
    - Catch obvious issues
    - Reduces reviewer burden
16. Pair programming as review:
    - Real-time review during coding
    - Faster feedback
    - Great for complex or risky changes
17. Review metrics:
    - Review turnaround time
    - Review thoroughness (comments per PR)
    - Defect escape rate (bugs found in production)
18. Building review culture:
    - Everyone reviews (not just seniors)
    - Code review guidelines document
    - Regular feedback on review quality
    - Celebrate good reviews
19. Remote team reviews:
    - Async-first (written feedback)
    - Video call for complex discussions
    - Timezone-aware (don't block overnight)
20. Real examples:
    - Good review comments
    - Bad review comments
    - Review discussion threads

Format: Include review checklists, comment templates, and culture-building strategies.

Create the file now.
```

### Skill 2: Knowledge Sharing

```
Create a comprehensive SKILL.md for Knowledge Sharing in teams.

Location: 27-team-collaboration/knowledge-sharing/SKILL.md

Cover:
1. Why knowledge sharing matters (reduce silos, onboard faster, team resilience)
2. Types of knowledge (domain, technical, process, tribal)
3. Documentation (READMEs, wikis, ADRs)
4. Tech talks (internal presentations)
5. Lunch and learns (informal sessions)
6. Pair programming (learn by doing)
7. Mob programming (group coding)
8. Show and tell (demo recent work)
9. Office hours (expert availability)
10. Mentorship programs
11. Code review as learning
12. Post-mortems (learn from incidents)
13. Architecture decision records (ADRs)
14. Knowledge base (Confluence, Notion)
15. Recording sessions (for async viewing)
16. Onboarding documentation
17. Measuring knowledge sharing (participation, satisfaction)
18. Building a learning culture
19. Real examples: Knowledge sharing formats

Format: Include documentation templates, session formats, and measurement frameworks.

Create the file now.
```

### Skill 3: Onboarding

```
Create a comprehensive SKILL.md for Developer Onboarding.

Location: 27-team-collaboration/onboarding/SKILL.md

Cover:
1. Why good onboarding matters (faster productivity, retention)
2. Pre-boarding (before day 1)
3. Day 1 (welcome, setup, meet team)
4. Week 1 (environment setup, first commits)
5. First month (complete first feature)
6. Onboarding checklist (tasks to complete)
7. Buddy system (assign mentor)
8. Documentation (setup guide, architecture overview)
9. Small first tasks (easy wins)
10. Regular check-ins (1-on-1s)
11. Access and tools setup
12. Team culture introduction
13. Measuring onboarding success (time to first commit, satisfaction)
14. Remote onboarding
15. Real examples: Onboarding plans

Format: Include onboarding checklists, timelines, and documentation templates.

Create the file now.
```

### Skill 4: Pair Programming

```
Create a comprehensive SKILL.md for Pair Programming.

Location: 27-team-collaboration/pair-programming/SKILL.md

Cover:
1. What is pair programming (two developers, one workstation)
2. Roles: Driver (typing) and Navigator (reviewing)
3. Benefits (code quality, knowledge sharing, focus)
4. When to pair (complex features, onboarding, debugging)
5. Pairing styles (driver-navigator, ping-pong)
6. Pairing best practices (switch roles, take breaks)
7. Remote pairing (VS Code Live Share, Tuple)
8. Pairing challenges (fatigue, personality conflicts)
9. Measuring pairing effectiveness
10. Tools for remote pairing
11. Real examples: Pairing scenarios

Format: Include pairing guidelines, tool setups, and effectiveness metrics.

Create the file now.
```

### Skill 5: Remote Work

```
Create a comprehensive SKILL.md for Remote Work best practices.

Location: 27-team-collaboration/remote-work/SKILL.md

Cover:
1. Remote work challenges (communication, collaboration, isolation)
2. Async-first communication (documentation, written decisions)
3. Synchronous communication (when needed)
4. Tools for remote teams (Slack, Zoom, Notion, GitHub)
5. Remote meetings (best practices, avoid meeting fatigue)
6. Time zone management (overlap hours, async handoffs)
7. Building team culture remotely (virtual events, casual chats)
8. Remote onboarding
9. Work-life balance (boundaries, flexible hours)
10. Measuring remote team health
11. Hybrid teams (some remote, some in-office)
12. Remote security (VPN, device management)
13. Real examples: Remote team workflows

Format: Include communication guidelines, tool recommendations, and team health metrics.

Create the file now.
```

---

## Summary

**Total new prompts created: 27 skills** across 4 batches

### Batch Breakdown:
- **24-security-practices**: 6 skills (incident response, OWASP, pen testing, secure coding, audit, vulnerability mgmt)
- **25-internationalization**: 5 skills (currency/timezone, i18n setup, localization, multi-language, RTL)
- **26-deployment-strategies**: 5 skills (blue-green, canary, feature toggles, rollback, rolling)
- **27-team-collaboration**: 5 skills (code review, knowledge sharing, onboarding, pair programming, remote work)

### Combined with Previous Batches:
- **Total skills across all batches**: 379 skills

### Priority for Generation:

**Tier 1: Security (Critical)**
1. OWASP Top 10 (24)
2. Secure Coding (24)
3. Incident Response (24)

**Tier 2: Deployment (DevOps)**
4. Feature Toggles (26)
5. Blue-Green Deployment (26)
6. Canary Deployment (26)

**Tier 3: Global Apps**
7. i18n Setup (25)
8. Currency & Timezone (25)

**Tier 4: Team Culture**
9. Code Review Culture (27)
10. Onboarding (27)

All prompts are ready to generate SKILL.md files! 🎯