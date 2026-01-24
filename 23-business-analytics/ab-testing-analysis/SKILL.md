---
name: A/B Testing Analysis
description: Running controlled experiments comparing two variants to determine which performs better for specific metrics, with statistical significance testing and data-driven decision making.
---

# A/B Testing Analysis

> **Current Level:** Intermediate  
> **Domain:** Business Analytics / Experimentation

---

## Overview

A/B testing (also known as split testing) is a controlled experiment where two variants (A and B) are compared to determine which performs better for a specific metric. Effective A/B testing uses proper randomization, statistical significance, and clear success metrics to make data-driven decisions.

## What is A/B Testing

- **Variant A (Control)**: The existing version
- **Variant B (Treatment)**: The modified version being tested
- **Random assignment**: Users are randomly assigned to either variant
- **Measurement**: Track which variant achieves better results

A/B testing enables **data-driven decision making** by removing guesswork and validating assumptions with statistical evidence.

## Why A/B Testing Matters

| Benefit | Description |
|---------|-------------|
| **Remove Guesswork** | Test assumptions instead of relying on opinions |
| **Measure Real Impact** | Quantify the effect of changes on user behavior |
| **Optimize Continuously** | Make incremental improvements over time |
| **Justify Decisions** | Support decisions with statistical evidence |
| **Reduce Risk** | Test changes before full rollout |
| **Learn About Users** | Gain insights into user preferences |

## A/B Test Components

### 1. Hypothesis
A clear statement of what you believe will happen and why.

### 2. Variants
- **Control (A)**: Current version
- **Treatment (B)**: New version to test

### 3. Metric
The key performance indicator you're measuring (e.g., conversion rate, click-through rate).

### 4. Sample Size
Number of users needed per variant to achieve statistical power.

### 5. Duration
How long to run the test to achieve required sample size.

## Hypothesis Formulation

### Format
```
If [change], then [expected outcome], because [reasoning]
```

### Examples

| Hypothesis | Change | Expected Outcome | Reasoning |
|------------|--------|------------------|-----------|
| "If we change button color to green, then conversion will increase by 10%, because green signals action" | Button color | +10% conversion | Green is psychologically associated with "go" and action |
| "If we add customer testimonials to checkout page, then cart abandonment will decrease by 5%, because social proof builds trust" | Testimonials | -5% abandonment | Social proof reduces purchase anxiety |
| "If we simplify signup form from 5 fields to 3 fields, then signup rate will increase by 15%, because reduced friction increases completion" | Form fields | +15% signup | Less effort required from users |

### Hypothesis Requirements
- **Testable**: Can be measured and validated
- **Measurable**: Quantifiable outcome
- **Specific**: Clear change and expected result
- **Time-bound**: Define test duration

## Choosing Metrics

### Metric Types

| Type | Purpose | Example |
|------|---------|---------|
| **Primary Metric** | Main success measure | Conversion rate |
| **Secondary Metrics** | Related measures | Average order value, time on page |
| **Guardrail Metrics** | Ensure no harm | Page load time, bounce rate |

### Metric Examples

| Domain | Primary | Secondary | Guardrail |
|--------|---------|-----------|-----------|
| E-commerce | Conversion rate | AOV, revenue per visitor | Page load time |
| SaaS | Free-to-paid conversion | Activation rate, retention | Churn rate |
| Content | Click-through rate | Time on page, scroll depth | Bounce rate |
| Mobile App | App install rate | Daily active users, retention | App crash rate |

### Metric Selection Criteria
1. **Actionable**: Can be influenced by your change
2. **Sensitive**: Will detect meaningful differences
3. **Reliable**: Consistent measurement
4. **Business-relevant**: Aligns with organizational goals

## Statistical Concepts

### Hypothesis Testing Framework

| Hypothesis | Definition |
|------------|-------------|
| **Null Hypothesis (H₀)** | No difference between A and B |
| **Alternative Hypothesis (H₁)** | B is different from A (typically B > A) |

### Key Statistical Terms

| Term | Definition | Typical Value |
|------|-------------|---------------|
| **P-value** | Probability result is due to chance | < 0.05 |
| **Statistical Significance** | Result unlikely due to chance | p < 0.05 (95% confidence) |
| **Confidence Level** | Probability result is correct | 95% |
| **Type I Error (α)** | False positive: Saying B is better when it's not | 5% (α = 0.05) |
| **Type II Error (β)** | False negative: Missing real improvement | 20% (β = 0.20) |
| **Statistical Power** | Probability to detect real effect | 80% (1 - β = 0.80) |

### Error Trade-offs

```
                    Reality
              B is better    B is same
          ┌─────────────┬─────────────┐
Decision  │             │             │
B is      │   Correct   │  Type I     │
better    │   (Power)   │  (α)        │
          ├─────────────┼─────────────┤
B is      │   Type II   │   Correct   │
same      │    (β)      │             │
          └─────────────┴─────────────┘
```

## Sample Size Calculation

### Parameters

| Parameter | Symbol | Example |
|-----------|--------|---------|
| Baseline conversion rate | p | 10% (0.10) |
| Minimum detectable effect | MDE | 1% absolute (0.01) |
| Significance level | α | 0.05 |
| Statistical power | 1-β | 0.80 |

### Formula (Two-sided test)

For proportions (conversion rate):

```
n = 16 * (p * (1-p)) / (MDE²)
```

Where:
- n = sample size per variant
- p = baseline conversion rate
- MDE = minimum detectable effect (absolute)

### Calculation Examples

| Baseline | MDE | Sample Size (per variant) | Total Sample |
|----------|-----|---------------------------|--------------|
| 10% | 1% absolute | 16 × 0.1 × 0.9 / 0.01² = 14,400 | 28,800 |
| 5% | 0.5% absolute | 16 × 0.05 × 0.95 / 0.005² = 30,400 | 60,800 |
| 20% | 2% absolute | 16 × 0.2 × 0.8 / 0.02² = 6,400 | 12,800 |

### Online Calculators

- **Evan Miller**: https://www.evanmiller.org/ab-testing/sample-size.html
- **Optimizely**: https://www.optimizely.com/sample-size-calculator/
- **ABTestGuide**: https://abtestguide.com/calc/

## Test Duration

### Duration Guidelines

| Factor | Recommendation |
|--------|----------------|
| **Minimum** | At least 1 week (capture weekly patterns) |
| **Business cycle** | 2-4 weeks for most tests |
| **Seasonality** | Avoid holidays, major events |
| **Sample size** | Must achieve required sample size |

### Weekly Patterns

```
Day        Traffic Pattern
─────────────────────────────
Monday     High (catching up)
Tuesday    Normal
Wednesday  Normal
Thursday   Normal
Friday     Lower (weekend prep)
Saturday   Low
Sunday     Low
```

### The Peeking Problem

**Problem**: Checking results early and stopping when you see significance increases false positive rate.

**Solutions**:
1. **Sequential testing**: Adjust significance thresholds for each peek
2. **Bayesian methods**: Can stop early more safely
3. **Commit to sample size**: Don't check until test completes

### Duration Calculation

```
Duration (weeks) = Required Sample / (Daily Visitors × 7 × Traffic %)
```

Example:
- Required sample: 28,800 users
- Daily visitors: 10,000
- Test traffic: 50% (50/50 split)
- Duration = 28,800 / (10,000 × 0.5 × 7) = 0.82 weeks ≈ 6 days

## Statistical Tests

### Test Selection Guide

| Metric Type | Distribution | Recommended Test |
|-------------|--------------|------------------|
| Proportions (conversion rate) | Binomial | Z-test for proportions |
| Continuous (revenue, time) | Normal | T-test |
| Categorical data | Chi-square | Chi-square test |
| Non-normal distributions | Any | Mann-Whitney U test |

### Z-Test for Proportions

Use for comparing conversion rates.

**Formula**:

```
z = (p̂₁ - p̂₂) / √(p̂(1-p̂)(1/n₁ + 1/n₂))
```

Where:
- p̂₁ = conversion rate for variant A
- p̂₂ = conversion rate for variant B
- p̂ = pooled proportion = (x₁ + x₂) / (n₁ + n₂)
- n₁, n₂ = sample sizes

### T-Test for Continuous Metrics

Use for comparing means (revenue, time on page).

**Formula**:

```
t = (x̄₁ - x̄₂) / √(s₁²/n₁ + s₂²/n₂)
```

Where:
- x̄₁, x̄₂ = sample means
- s₁², s₂² = sample variances
- n₁, n₂ = sample sizes

### Chi-Square Test

Use for categorical data (click patterns, device types).

**Formula**:

```
χ² = Σ (O - E)² / E
```

Where:
- O = observed frequency
- E = expected frequency

## Analyzing Results

### Analysis Steps

1. **Calculate test statistic** (z-score, t-score, etc.)
2. **Compute p-value** from test statistic
3. **Determine statistical significance** (p < 0.05?)
4. **Calculate confidence interval**
5. **Interpret practical significance**

### Result Interpretation

| Scenario | Interpretation | Action |
|----------|----------------|--------|
| p < 0.05, positive lift | Statistically significant improvement | Implement B |
| p < 0.05, negative lift | Statistically significant decline | Keep A |
| p ≥ 0.05 | No statistically significant difference | Keep A (or iterate) |

### Lift Calculation

```
Absolute Lift = Conversion_B - Conversion_A
Relative Lift = (Conversion_B - Conversion_A) / Conversion_A × 100%
```

Example:
- Conversion A: 10%
- Conversion B: 12%
- Absolute Lift: 2%
- Relative Lift: 20%

## Confidence Intervals

### What is a Confidence Interval?

A range of plausible values for the true effect size.

### Interpretation

"Conversion increased by 2% (95% CI: 1.2% to 2.8%)"

This means: We are 95% confident the true increase is between 1.2% and 2.8%.

### CI Formula (for proportions)

```
CI = p̂ ± z × √(p̂(1-p̂)/n)
```

Where:
- p̂ = observed proportion
- z = z-score for confidence level (1.96 for 95%)
- n = sample size

### Visualizing Confidence Intervals

```
Variant A: 10% ────────────────────────
Variant B: 12% ────────────────────────
           └────┬────┘
           95% CI: 11.2% to 12.8%
```

### CI Overlap Rule

- **Non-overlapping CIs**: Significant difference
- **Overlapping CIs**: Not significant (rough rule)

## Statistical Significance vs Practical Significance

### Comparison

| Aspect | Statistical Significance | Practical Significance |
|--------|------------------------|------------------------|
| Definition | p < 0.05 (unlikely due to chance) | Meaningful business impact |
| Example | 0.1% conversion increase, p = 0.01 | 10% conversion increase |
| Focus | Probability of chance | Business value |
| Decision | Is it real? | Is it worth it? |

### Decision Framework

```
                    Practical Impact
              Low              High
          ┌─────────────┬─────────────┐
Statistical│             │             │
Significance│  Ignore    │  Implement  │
Yes        │             │             │
           ├─────────────┼─────────────┤
Statistical│  Ignore    │  Consider   │
No         │             │  (more data)│
           └─────────────┴─────────────┘
```

### Example

| Scenario | Statistical | Practical | Decision |
|----------|------------|-----------|----------|
| 0.1% lift, p = 0.01 | ✓ | ✗ | Ignore (not worth implementation) |
| 10% lift, p = 0.01 | ✓ | ✓ | Implement |
| 10% lift, p = 0.15 | ✗ | ✓ | Collect more data |

## Multiple Testing Problem

### The Problem

Testing multiple metrics increases the chance of false positives.

**Example**: If you test 20 metrics at α = 0.05, expect 1 false positive by chance.

```
False positives = Number of tests × α
                 = 20 × 0.05
                 = 1
```

### Solutions

| Solution | How it Works | Trade-off |
|----------|--------------|-----------|
| **Bonferroni Correction** | Divide α by number of tests | More conservative, harder to find significance |
| **Focus on Primary Metric** | Only test primary metric | Misses insights from secondary metrics |
| **Pre-register Hypothesis** | Declare metrics before test | Reduces p-hacking |
| **False Discovery Rate** | Control proportion of false positives | More complex |

### Bonferroni Correction

```
Adjusted α = α / Number of tests
```

Example:
- Original α = 0.05
- Testing 5 metrics
- Adjusted α = 0.05 / 5 = 0.01

## Common Pitfalls

### 1. Peeking

**Problem**: Checking results early and stopping when you see significance.

**Solution**: Commit to sample size upfront or use sequential testing.

### 2. Sample Ratio Mismatch (SRM)

**Problem**: 50/50 split becomes 45/55 due to technical issues.

**Detection**: Chi-square test on sample sizes.

**Solution**: Fix randomization before proceeding.

### 3. Novelty Effect

**Problem**: Users try new thing temporarily because it's new.

**Solution**: Run test long enough for novelty to wear off.

### 4. Selection Bias

**Problem**: Test only on specific segment (e.g., only US users).

**Solution**: Ensure random assignment across all users.

### 5. Carryover Effects

**Problem**: Previous exposure affects results (users see both variants).

**Solution**: Ensure consistent user assignment (same user always sees same variant).

### 6. Insufficient Sample Size

**Problem**: Test too small to detect meaningful differences.

**Solution**: Calculate required sample size before starting.

### 7. Testing Too Many Variants

**Problem**: Multiple variants dilute sample size.

**Solution**: Limit to 2-3 variants per test.

### 8. Ignoring Seasonality

**Problem**: Test during unusual period (holidays, events).

**Solution**: Run tests during normal periods.

## Peeking Problem (Deep Dive)

### Why Peeking is Bad

Each peek increases the false positive rate:

```
Peeks    False Positive Rate
─────────────────────────────
1        5%
5        14%
10       23%
20       37%
```

### Solutions

#### 1. Sequential Testing

Adjust significance thresholds for each peek:

```
Peek    Adjusted α
─────────────────────
1        0.017
2        0.022
3        0.027
4        0.032
5        0.036
```

#### 2. Bayesian Methods

- Outputs probability that B beats A
- Can stop early more safely
- More intuitive interpretation

#### 3. Pre-committed Sample Size

- Calculate required sample size
- Don't check until complete
- Simplest approach

## Segmentation Analysis

### Why Segment?

The overall result might hide segment-specific effects.

### Common Segments

| Segment | Example |
|---------|---------|
| Device | Mobile vs Desktop |
| Geography | US vs EU vs Asia |
| User type | New vs Returning |
| Acquisition channel | Organic vs Paid |
| Browser | Chrome vs Safari |
| OS | iOS vs Android |

### Simpson's Paradox

Aggregated results differ from segment results.

**Example**:

| Segment | Variant A | Variant B | Winner |
|---------|-----------|-----------|--------|
| Mobile | 5% | 6% | B |
| Desktop | 15% | 16% | B |
| **Overall** | **10%** | **11%** | B |

But if sample sizes differ:

| Segment | A Sample | B Sample | A Conv | B Conv |
|---------|----------|----------|--------|--------|
| Mobile | 1000 | 100 | 5% | 6% |
| Desktop | 100 | 1000 | 15% | 16% |
| **Overall** | **1100** | **1100** | **5.9%** | **15.5%** | B wins big |

Always check segment results!

### Interaction Effects

Does the effect vary by segment?

Example: New checkout works better for mobile users but worse for desktop users.

**Solution**: Segment-specific analysis or interaction test.

## Bayesian A/B Testing

### Frequentist vs Bayesian

| Aspect | Frequentist (p-value) | Bayesian |
|--------|----------------------|----------|
| Output | p-value, confidence interval | Probability B beats A |
| Interpretation | "Probability of data given H₀" | "Probability of H₁ given data" |
| Early stopping | Not recommended | Allowed |
| Intuition | Less intuitive | More intuitive |

### Bayesian Output Example

```
Probability B beats A: 98.5%
Expected lift: +2.1% (95% credible interval: 1.2% to 3.0%)
```

### Advantages

1. **Intuitive**: "98% chance B is better"
2. **Early stopping**: Can stop when confident
3. **Small samples**: Works with smaller samples
4. **No sample size commitment**: Stop when ready

### Tools

- **VWO**: Built-in Bayesian testing
- **Google Optimize**: Bayesian by default
- **Statsig**: Bayesian A/B testing
- **Custom**: Python with PyMC, R with rstanarm

## A/A Testing

### What is A/A Testing?

Testing identical variants as a sanity check.

### Purpose

| Purpose | Description |
|---------|-------------|
| **Validate instrumentation** | Ensure tracking works correctly |
| **Detect biases** | Check for systematic differences |
| **Baseline variance** | Understand natural variation |
| **Sanity check** | Verify randomization |

### Expected Results

A/A test should show:
- No significant difference (p > 0.05)
- Conversion rates within expected variance
- 50/50 sample split (within margin of error)

### When to Run A/A Test

- Before launching new experimentation platform
- After major tracking changes
- When suspicious results appear

## Multi-Variate Testing (MVT)

### What is MVT?

Testing multiple changes simultaneously.

### Example

Test button color AND button text:

| Variant | Color | Text |
|---------|-------|------|
| Control | Blue | "Buy Now" |
| 1 | Green | "Buy Now" |
| 2 | Blue | "Add to Cart" |
| 3 | Green | "Add to Cart" |

### MVT vs Sequential A/B Tests

| Approach | Time | Sample Size | Insights |
|----------|------|-------------|----------|
| MVT | 1 test | Larger | Interaction effects |
| Sequential | 2 tests | Smaller | No interaction effects |

### Sample Size for MVT

```
Sample per variant = Base sample × Number of variants
```

Example:
- Base sample: 10,000 per variant
- 4 variants (MVT)
- Required: 40,000 per variant

### When to Use MVT

- Testing independent elements
- Want to find optimal combination
- Have sufficient traffic

## Tools for A/B Testing

### Experimentation Platforms

| Tool | Features | Pricing |
|------|----------|---------|
| **Optimizely** | Enterprise features, audience targeting | $$$ |
| **VWO** | Visual editor, heatmaps | $$ |
| **LaunchDarkly** | Feature flags, gradual rollout | $$ |
| **Statsig** | Free tier, warehouse native | $-$$ |
| **Google Optimize** | Free, integrates with GA | Free (discontinued) |

### Analytics

| Tool | Use Case |
|------|----------|
| **Google Analytics 4** | Web analytics, free |
| **Mixpanel** | Product analytics |
| **Amplitude** | Product analytics |
| **Heap** | Auto-capture events |

### Statistical Analysis

| Tool | Language | Use Case |
|------|----------|----------|
| **scipy.stats** | Python | Statistical tests |
| **statsmodels** | Python | Advanced statistics |
| **R** | R | Statistical analysis |
| **Excel** | - | Basic analysis |

### Sample Size Calculators

- Evan Miller: https://www.evanmiller.org/ab-testing/sample-size.html
- Optimizely: https://www.optimizely.com/sample-size-calculator/
- ABTestGuide: https://abtestguide.com/calc/

## Implementation

### Randomization

```python
import random
import hashlib

def assign_variant(user_id, variants=['A', 'B']):
    """Consistent user assignment using hash."""
    hash_value = int(hashlib.md5(user_id.encode()).hexdigest(), 16)
    variant_index = hash_value % len(variants)
    return variants[variant_index]

# Example
user_id = "user_12345"
variant = assign_variant(user_id)
print(f"User {user_id} assigned to variant {variant}")
```

### Tracking

```javascript
// Track exposure
function trackExposure(userId, variant) {
  analytics.track('ab_test_exposure', {
    userId: userId,
    testName: 'checkout_button_color',
    variant: variant,
    timestamp: new Date().toISOString()
  });
}

// Track conversion
function trackConversion(userId, variant) {
  analytics.track('ab_test_conversion', {
    userId: userId,
    testName: 'checkout_button_color',
    variant: variant,
    timestamp: new Date().toISOString()
  });
}
```

### Analysis (Python)

```python
import numpy as np
from scipy import stats

def analyze_ab_test(conversions_a, total_a, conversions_b, total_b):
    """Analyze A/B test results."""
    # Conversion rates
    rate_a = conversions_a / total_a
    rate_b = conversions_b / total_b

    # Z-test for proportions
    p_pooled = (conversions_a + conversions_b) / (total_a + total_b)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/total_a + 1/total_b))
    z_score = (rate_b - rate_a) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))  # Two-tailed

    # Confidence interval
    z_critical = stats.norm.ppf(0.975)  # 95% CI
    ci_lower = (rate_b - rate_a) - z_critical * se
    ci_upper = (rate_b - rate_a) + z_critical * se

    # Lift
    absolute_lift = rate_b - rate_a
    relative_lift = (rate_b - rate_a) / rate_a * 100

    return {
        'rate_a': rate_a,
        'rate_b': rate_b,
        'absolute_lift': absolute_lift,
        'relative_lift': relative_lift,
        'z_score': z_score,
        'p_value': p_value,
        'significant': p_value < 0.05,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper
    }

# Example
results = analyze_ab_test(
    conversions_a=1000, total_a=10000,
    conversions_b=1200, total_b=10000
)

print(f"Variant A: {results['rate_a']:.2%}")
print(f"Variant B: {results['rate_b']:.2%}")
print(f"Relative lift: {results['relative_lift']:.1f}%")
print(f"P-value: {results['p_value']:.4f}")
print(f"Significant: {results['significant']}")
print(f"95% CI: [{results['ci_lower']:.2%}, {results['ci_upper']:.2%}]")
```

### Sample Size Calculation (Python)

```python
import math

def calculate_sample_size(baseline_rate, mde, alpha=0.05, power=0.8):
    """Calculate sample size per variant for A/B test."""
    z_alpha = 1.96  # For alpha = 0.05
    z_beta = 0.84   # For power = 0.8

    p1 = baseline_rate
    p2 = baseline_rate + mde

    # Pooled proportion
    p_pooled = (p1 + p2) / 2

    # Sample size formula
    n = (z_alpha + z_beta) ** 2 * 2 * p_pooled * (1 - p_pooled) / (mde ** 2)

    return math.ceil(n)

# Example
sample_size = calculate_sample_size(
    baseline_rate=0.10,
    mde=0.01
)

print(f"Sample size per variant: {sample_size:,}")
print(f"Total sample size: {sample_size * 2:,}")
```

## Reporting Results

### Report Template

```
A/B Test Report: Checkout Button Color
─────────────────────────────────────────────────────────────

Test Details
  Test Name: checkout_button_color_v1
  Start Date: 2024-01-01
  End Date: 2024-01-14
  Duration: 14 days

Hypothesis
  If we change button color to green, then conversion will increase
  by 10%, because green signals action.

Variants
  A (Control): Blue button
  B (Treatment): Green button

Results
  Variant A: 10.0% (1,000/10,000)
  Variant B: 12.0% (1,200/10,000)

Lift
  Absolute: +2.0%
  Relative: +20.0%

Statistical Analysis
  Z-score: 4.47
  P-value: 0.0001
  95% CI: [1.2%, 2.8%]
  Significant: Yes ✓

Recommendation
  Ship variant B (green button)

Caveats
  - Test ran during normal business cycle
  - No seasonality effects observed
  - Consistent across mobile and desktop

Learnings
  - Color change had significant impact
  - Consider testing other CTA colors
  - No negative impact on guardrail metrics
```

### Recommendation Categories

| Recommendation | Criteria |
|----------------|----------|
| **Ship** | Statistically significant, positive lift, practical impact |
| **Iterate** | Not significant or small lift, promising direction |
| **Abandon** | Negative or no impact, not worth pursuing |

## Post-Experiment

### Long-Term Impact

| Activity | Purpose |
|----------|---------|
| **Holdout group** | Keep small % on control to measure long-term effects |
| **Monitor metrics** | Track if lift sustains over time |
| **Interaction analysis** | Check if change affects other features |

### Cost-Benefit Analysis

```
Benefit = Lift × Revenue per conversion × Traffic
Cost = Implementation cost + Maintenance cost

ROI = (Benefit - Cost) / Cost
```

### Document Learnings

1. **What worked**: Changes that had positive impact
2. **What didn't**: Changes that had no/negative impact
3. **User insights**: What users preferred
4. **Technical notes**: Implementation details
5. **Future tests**: Ideas for follow-up experiments

## Real Examples

### Example 1: Button Color Test

| Metric | Variant A (Blue) | Variant B (Green) | Result |
|--------|-----------------|-------------------|--------|
| Conversions | 1,000 | 1,200 | +20% lift |
| Sample Size | 10,000 | 10,000 | p < 0.001 |
| Decision | | | Ship B |

### Example 2: Pricing Page Test

| Metric | Variant A ($19/mo) | Variant B ($21/mo) | Result |
|--------|-------------------|-------------------|--------|
| Conversions | 500 | 450 | -10% lift |
| Revenue | $9,500 | $9,450 | -0.5% lift |
| Sample Size | 10,000 | 10,000 | p = 0.08 |
| Decision | | | Keep A |

### Example 3: Checkout Flow Test

| Metric | Variant A (Multi-step) | Variant B (One-page) | Result |
|--------|------------------------|----------------------|--------|
| Conversions | 800 | 1,000 | +25% lift |
| Sample Size | 10,000 | 10,000 | p < 0.001 |
| Decision | | | Ship B |

### Example 4: Email Subject Line Test

| Metric | Variant A | Variant B | Result |
|--------|-----------|-----------|--------|
| Open Rate | 20% | 22% | +10% lift |
| Click Rate | 5% | 5.5% | +10% lift |
| Sample Size | 10,000 | 10,000 | p = 0.03 |
| Decision | | | Ship B |

## Python Implementation

### Complete A/B Test Analysis Script

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class ABTestAnalyzer:
    """Complete A/B test analysis toolkit."""

    def __init__(self, conversions_a, total_a, conversions_b, total_b,
                 alpha=0.05, test_name="AB Test"):
        self.conversions_a = conversions_a
        self.total_a = total_a
        self.conversions_b = conversions_b
        self.total_b = total_b
        self.alpha = alpha
        self.test_name = test_name
        self.results = self._analyze()

    def _analyze(self):
        """Perform complete analysis."""
        rate_a = self.conversions_a / self.total_a
        rate_b = self.conversions_b / self.total_b

        # Z-test
        p_pooled = (self.conversions_a + self.conversions_b) / \
                   (self.total_a + self.total_b)
        se = np.sqrt(p_pooled * (1 - p_pooled) *
                     (1/self.total_a + 1/self.total_b))
        z_score = (rate_b - rate_a) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))

        # Confidence interval
        z_critical = stats.norm.ppf(1 - self.alpha/2)
        ci_lower = (rate_b - rate_a) - z_critical * se
        ci_upper = (rate_b - rate_a) + z_critical * se

        # Power
        effect_size = (rate_b - rate_a) / np.sqrt(p_pooled * (1 - p_pooled))
        power = stats.norm.cdf(
            (abs(rate_b - rate_a) - z_critical * se) / se
        )

        return {
            'rate_a': rate_a,
            'rate_b': rate_b,
            'absolute_lift': rate_b - rate_a,
            'relative_lift': (rate_b - rate_a) / rate_a * 100,
            'z_score': z_score,
            'p_value': p_value,
            'significant': p_value < self.alpha,
            'ci_lower': ci_lower,
            'ci_upper': ci_upper,
            'power': power,
            'conversions_a': self.conversions_a,
            'conversions_b': self.conversions_b,
            'total_a': self.total_a,
            'total_b': self.total_b
        }

    def print_report(self):
        """Print formatted report."""
        r = self.results

        print(f"\n{'='*60}")
        print(f"A/B Test Report: {self.test_name}")
        print(f"{'='*60}\n")

        print("Results:")
        print(f"  Variant A: {r['rate_a']:.2%} ({r['conversions_a']}/{r['total_a']})")
        print(f"  Variant B: {r['rate_b']:.2%} ({r['conversions_b']}/{r['total_a']})")
        print()

        print("Lift:")
        print(f"  Absolute: {r['absolute_lift']:+.2%}")
        print(f"  Relative: {r['relative_lift']:+.1f}%")
        print()

        print("Statistical Analysis:")
        print(f"  Z-score: {r['z_score']:.4f}")
        print(f"  P-value: {r['p_value']:.4f}")
        print(f"  95% CI: [{r['ci_lower']:.2%}, {r['ci_upper']:.2%}]")
        print(f"  Power: {r['power']:.2%}")
        print(f"  Significant: {'Yes ✓' if r['significant'] else 'No ✗'}")
        print()

        print("Recommendation:")
        if r['significant'] and r['relative_lift'] > 0:
            print("  Ship variant B")
        elif r['significant'] and r['relative_lift'] < 0:
            print("  Keep variant A (negative impact)")
        else:
            print("  Inconclusive (not significant)")

    def plot_results(self):
        """Plot comparison chart."""
        r = self.results

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

        # Bar chart
        variants = ['Variant A', 'Variant B']
        rates = [r['rate_a'], r['rate_b']]
        colors = ['#3498db', '#2ecc71']

        bars = ax1.bar(variants, rates, color=colors, alpha=0.7)
        ax1.set_ylabel('Conversion Rate')
        ax1.set_title('Conversion Rate Comparison')
        ax1.set_ylim(0, max(rates) * 1.2)

        # Add value labels
        for bar, rate in zip(bars, rates):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{rate:.2%}',
                    ha='center', va='bottom')

        # Error bars for CI
        ax2.errorbar(['Lift'], [r['absolute_lift']],
                    yerr=[[r['absolute_lift'] - r['ci_lower']],
                          [r['ci_upper'] - r['absolute_lift']]],
                    fmt='o', capsize=10, capthick=2, markersize=10)
        ax2.axhline(y=0, color='red', linestyle='--', alpha=0.5)
        ax2.set_ylabel('Absolute Lift')
        ax2.set_title(f'95% Confidence Interval\n(P-value: {r["p_value"]:.4f})')

        plt.tight_layout()
        return fig

# Example usage
if __name__ == "__main__":
    analyzer = ABTestAnalyzer(
        conversions_a=1000, total_a=10000,
        conversions_b=1200, total_b=10000,
        test_name="Checkout Button Color"
    )

    analyzer.print_report()
    fig = analyzer.plot_results()
    plt.show()
```

### Sample Size Calculator

```python
import numpy as np
from scipy import stats

def sample_size_calculator(baseline_rate, mde, alpha=0.05, power=0.8):
    """
    Calculate required sample size for A/B test.

    Parameters:
    -----------
    baseline_rate : float
        Current conversion rate (e.g., 0.10 for 10%)
    mde : float
        Minimum detectable effect (absolute, e.g., 0.01 for 1%)
    alpha : float
        Significance level (default 0.05)
    power : float
        Statistical power (default 0.8)

    Returns:
    --------
    dict : Sample size information
    """
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)

    p1 = baseline_rate
    p2 = baseline_rate + mde
    p_pooled = (p1 + p2) / 2

    n = (z_alpha + z_beta) ** 2 * 2 * p_pooled * (1 - p_pooled) / (mde ** 2)
    n_per_variant = math.ceil(n)

    return {
        'sample_per_variant': n_per_variant,
        'total_sample': n_per_variant * 2,
        'baseline_rate': baseline_rate,
        'mde': mde,
        'alpha': alpha,
        'power': power
    }

# Example
result = sample_size_calculator(baseline_rate=0.10, mde=0.01)
print(f"Sample per variant: {result['sample_per_variant']:,}")
print(f"Total sample: {result['total_sample']:,}")
```

## Summary Checklist

### Before Running A/B Test

- [ ] Clear hypothesis statement
- [ ] Primary metric defined
- [ ] Secondary and guardrail metrics identified
- [ ] Sample size calculated
- [ ] Test duration determined
- [ ] Randomization implemented
- [ ] Tracking verified
- [ ] A/A test run (if new setup)

### During A/B Test

- [ ] Monitor sample ratio (check for SRM)
- [ ] Don't peek early (or use sequential testing)
- [ ] Monitor guardrail metrics
- [ ] Watch for technical issues

### After A/B Test

- [ ] Verify sample size achieved
- [ ] Calculate statistical significance
- [ ] Analyze results
- [ ] Make decision
- [ ] Document findings
```

---

## Quick Start

### Basic A/B Test Setup

```javascript
// A/B test assignment
function assignVariant(userId) {
  const hash = hashUserId(userId)
  return hash % 2 === 0 ? 'A' : 'B'
}

// Track conversion
function trackConversion(userId, variant, converted) {
  analytics.track('ab_test_conversion', {
    userId,
    variant,
    converted,
    testName: 'button-color-test'
  })
}

// Calculate results
function calculateResults(variantA, variantB) {
  const rateA = variantA.conversions / variantA.visitors
  const rateB = variantB.conversions / variantB.visitors
  const lift = ((rateB - rateA) / rateA) * 100
  
  return {
    rateA,
    rateB,
    lift,
    significant: isStatisticallySignificant(variantA, variantB)
  }
}
```

---

## Production Checklist

- [ ] **Hypothesis**: Clear hypothesis and success metric
- [ ] **Sample Size**: Calculate required sample size
- [ ] **Randomization**: Proper random assignment
- [ ] **Tracking**: Set up conversion tracking
- [ ] **Guardrail Metrics**: Monitor guardrail metrics
- [ ] **Statistical Significance**: Use proper statistical tests
- [ ] **Duration**: Run test for sufficient duration
- [ ] **No Peeking**: Don't peek at results early
- [ ] **Documentation**: Document test setup and results
- [ ] **Decision**: Make data-driven decision
- [ ] **Implementation**: Implement winning variant
- [ ] **Learning**: Document learnings for future tests

---

## Anti-patterns

### ❌ Don't: Peek Early

```javascript
// ❌ Bad - Check results too early
if (day === 1) {
  checkResults()  // Too early!
}
```

```javascript
// ✅ Good - Wait for sample size
const requiredSampleSize = calculateSampleSize(alpha, power, effectSize)
if (totalVisitors >= requiredSampleSize) {
  checkResults()
}
```

### ❌ Don't: No Statistical Significance

```javascript
// ❌ Bad - No significance test
if (variantB.rate > variantA.rate) {
  return 'B wins'  // Could be random!
}
```

```javascript
// ✅ Good - Statistical significance
const pValue = calculatePValue(variantA, variantB)
if (pValue < 0.05 && variantB.rate > variantA.rate) {
  return 'B wins (statistically significant)'
}
```

### ❌ Don't: Ignore Guardrail Metrics

```javascript
// ❌ Bad - Only check conversion
if (conversionRateB > conversionRateA) {
  return 'B wins'  // But what about revenue?
}
```

```javascript
// ✅ Good - Check guardrail metrics
if (conversionRateB > conversionRateA && 
    revenueB >= revenueA && 
    bounceRateB <= bounceRateA) {
  return 'B wins'
}
```

---

## Integration Points

- **Dashboard Design** (`23-business-analytics/dashboard-design/`) - Test results visualization
- **KPI Metrics** (`23-business-analytics/kpi-metrics/`) - Success metrics
- **SQL for Analytics** (`23-business-analytics/sql-for-analytics/`) - Results analysis

---

## Further Reading

- [A/B Testing Guide](https://www.optimizely.com/optimization-glossary/ab-testing/)
- [Statistical Significance](https://www.investopedia.com/terms/s/statistical-significance.asp)
- [Sequential Testing](https://www.evanmiller.org/sequential-ab-testing.html)
- [ ] Calculate statistical significance
- [ ] Check confidence intervals
- [ ] Analyze segments
- [ ] Assess practical significance
- [ ] Document results
- [ ] Make recommendation
- [ ] Implement or iterate
