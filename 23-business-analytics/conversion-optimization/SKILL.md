---
name: Conversion Optimization (CRO)
description: Systematically increasing the percentage of website or app visitors who complete desired actions through data-driven experimentation, A/B testing, and continuous improvement.
---

# Conversion Optimization (CRO)

> **Current Level:** Intermediate  
> **Domain:** Business Analytics / Marketing

---

## Overview

Conversion Rate Optimization (CRO) is the systematic process of increasing the percentage of website or app visitors who complete a desired action (conversion) through data-driven experimentation and continuous improvement. Effective CRO uses A/B testing, user research, analytics, and iterative improvements to maximize conversions.

## What is Conversion Optimization

### Core Definition

```
Conversion Rate = (Conversions / Total Visitors) × 100%
```

### CRO Value Proposition

| Benefit | Impact |
|---------|--------|
| **Increase Revenue** | More conversions = more revenue |
| **Reduce Acquisition Cost** | Better conversion = lower CAC |
| **Improve User Experience** | Smoother journey = happier users |
| **Data-Driven Decisions** | Test assumptions, not guess |
| **Competitive Advantage** | Continuous improvement |

## Conversion Funnel

### AIDA Model

```
┌─────────────────────────────────────────────────────────────────┐
│                        Conversion Funnel                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │ Awareness   │───▶│  Interest   │───▶│   Desire    │       │
│  │  100,000    │    │   50,000    │    │   25,000    │       │
│  │  (100%)     │    │   (50%)     │    │   (25%)     │       │
│  └─────────────┘    └─────────────┘    └─────────────┘       │
│                                              │                  │
│                                              ▼                  │
│                                    ┌─────────────┐             │
│                                    │   Action    │             │
│                                    │    5,000    │             │
│                                    │    (5%)     │             │
│                                    └─────────────┘             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Example Funnel: E-commerce

| Stage | Users | Conversion Rate | Drop-off |
|-------|-------|-----------------|----------|
| Visit | 10,000 | 100% | - |
| Product View | 5,000 | 50% | 50% |
| Add to Cart | 2,500 | 25% | 50% |
| Checkout | 1,500 | 15% | 40% |
| Purchase | 500 | 5% | 67% |

**Overall Conversion**: 5% (500/10,000)

### Funnel Analysis

Identify bottlenecks (biggest drop-offs):

```
Drop-off Rate = (Users at Stage N - Users at Stage N+1) / Users at Stage N × 100%
```

**Example**:
- Visit → Product View: 50% drop-off (5,000 users lost)
- Add to Cart → Checkout: 40% drop-off (1,000 users lost)
- Checkout → Purchase: 67% drop-off (1,000 users lost)

**Priority**: Fix Checkout → Purchase (highest drop-off)

## CRO Process

### The CRO Framework

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Research   │───▶│ Hypothesize │───▶│  Prioritize  │
│             │    │             │    │             │
│ Understand  │    │ Formulate   │    │ ICE/PIE     │
│ users       │    │ hypotheses  │    │ scoring     │
└─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │
      └──────────────────┴──────────────────┘
                         │
                         ▼
                   ┌─────────────┐
                   │    Test     │
                   │             │
                   │ A/B test    │
                   └─────────────┘
                         │
                         ▼
                   ┌─────────────┐
                   │   Learn     │
                   │             │
                   │ Analyze &   │
                   │ iterate     │
                   └─────────────┘
```

### Step 1: Research

Understand users and identify issues.

| Method | What It Reveals | Tools |
|--------|----------------|-------|
| **Analytics** | Where users drop off | Google Analytics, Mixpanel |
| **Heatmaps** | Where users click | Hotjar, Crazy Egg |
| **Session Recordings** | User behavior | FullStory, LogRocket |
| **User Surveys** | User opinions | Typeform, SurveyMonkey |
| **User Interviews** | Deep insights | Calendly, Zoom |

### Step 2: Hypothesize

Formulate testable hypotheses.

**Format**:
```
If [change], then [expected outcome], because [reasoning]
```

**Examples**:
- "If we add trust badges to checkout, then conversion will increase by 10%, because users feel more secure."
- "If we reduce form fields from 5 to 3, then signup rate will increase by 15%, because less friction."

### Step 3: Prioritize

Decide which tests to run first.

**ICE Score**:
```
ICE = Impact × Confidence × Ease
```

| Score | Range |
|-------|-------|
| Impact | 1-10 (10 = huge impact) |
| Confidence | 1-10 (10 = very confident) |
| Ease | 1-10 (10 = very easy) |

**PIE Score**:
```
PIE = Potential × Importance × Ease
```

### Step 4: Test

Run A/B tests to validate hypotheses.

### Step 5: Learn

Analyze results and iterate.

## Research Methods

### 1. Analytics Analysis

Identify where users drop off.

```sql
-- Funnel analysis SQL
WITH funnel_stages AS (
    SELECT
        'visit' AS stage,
        COUNT(DISTINCT session_id) AS users
    FROM page_views
    WHERE page_url = '/home'

    UNION ALL

    SELECT
        'product_view' AS stage,
        COUNT(DISTINCT session_id) AS users
    FROM page_views
    WHERE page_url LIKE '/product/%'

    UNION ALL

    SELECT
        'add_to_cart' AS stage,
        COUNT(DISTINCT session_id) AS users
    FROM events
    WHERE event_type = 'add_to_cart'

    UNION ALL

    SELECT
        'purchase' AS stage,
        COUNT(DISTINCT session_id) AS users
    FROM events
    WHERE event_type = 'purchase'
)

SELECT
    stage,
    users,
    LAG(users) OVER (ORDER BY users DESC) AS previous_users,
    ROUND(100.0 * users / LAG(users) OVER (ORDER BY users DESC), 2) AS conversion_rate,
    ROUND(100.0 * (LAG(users) OVER (ORDER BY users DESC) - users) / LAG(users) OVER (ORDER BY users DESC), 2) AS drop_off_rate
FROM funnel_stages
ORDER BY users DESC;
```

### 2. Heatmaps

Visualize where users click.

| Type | What It Shows |
|------|---------------|
| **Click heatmap** | Where users click |
| **Scroll heatmap** | How far users scroll |
| **Move heatmap** | Where users hover |
| **Attention heatmap** | Where users spend time |

**Tools**: Hotjar, Crazy Egg, Lucky Orange

### 3. Session Recordings

Watch real user sessions.

**What to Look For**:
- Frustration (rage clicks)
- Confusion (back-and-forth navigation)
- Abandonment (leaving mid-process)
- Success patterns (what works)

**Tools**: FullStory, LogRocket, Hotjar

### 4. User Surveys

Ask users directly.

**Survey Questions**:
- "What almost stopped you from completing your purchase?"
- "What would make this process easier?"
- "What's your biggest frustration with our site?"

**Tools**: Typeform, SurveyMonkey, Google Forms

### 5. User Interviews

Deep qualitative insights.

**Interview Tips**:
- Ask open-ended questions
- Listen more than talk
- Probe for "why"
- Record sessions (with permission)

## Common Conversion Issues

### 1. Slow Page Load

**Problem**: Users bounce before page loads.

**Solution**:
- Optimize images
- Minify CSS/JS
- Use CDN
- Enable caching

**Impact**: 1-second delay = 7% conversion drop

### 2. Unclear Value Proposition

**Problem**: Users don't understand what you offer.

**Solution**:
- Clear headline
- Benefit-focused copy
- Social proof
- Simple language

### 3. Too Many Form Fields

**Problem**: Users abandon due to friction.

**Solution**:
- Minimize fields
- Use smart defaults
- Inline validation
- Progress indicators

**Impact**: Each extra field = 10% drop-off

### 4. Poor Mobile Experience

**Problem**: Mobile users can't convert.

**Solution**:
- Mobile-first design
- Large tap targets
- Simplified forms
- Test on real devices

### 5. Lack of Trust Signals

**Problem**: Users don't trust your site.

**Solution**:
- Security badges
- Customer reviews
- Money-back guarantee
- Contact information

## Conversion Rate Formulas

### Basic Conversion Rate

```
Conversion Rate = (Conversions / Visitors) × 100%
```

**Example**:
- Visitors: 10,000
- Conversions: 500
- Conversion Rate: 5%

### Micro vs Macro Conversions

| Type | Definition | Example |
|------|-------------|---------|
| **Micro** | Small step toward goal | Email signup, add to cart |
| **Macro** | Final goal | Purchase, subscription |

### Funnel Conversion

```
Overall Conversion = Product(Stage Rates)
```

**Example**:
- Visit → Product View: 50%
- Product View → Add to Cart: 50%
- Add to Cart → Purchase: 20%
- Overall: 0.5 × 0.5 × 0.2 = 5%

### Revenue Per Visitor (RPV)

```
RPV = Total Revenue / Total Visitors
```

**Example**:
- Revenue: $50,000
- Visitors: 10,000
- RPV: $5

## Optimization Tactics

### 1. Reduce Friction

| Tactic | Impact |
|--------|--------|
| Fewer form fields | +10-20% |
| Autofill | +5-10% |
| One-page checkout | +10-30% |
| Guest checkout | +15-25% |

### 2. Add Urgency

| Tactic | Example |
|--------|---------|
| Limited time | "Offer ends in 2 hours" |
| Limited quantity | "Only 3 left in stock" |
| Countdown timer | ⏱️ 23:59:59 |

### 3. Social Proof

| Tactic | Example |
|--------|---------|
| Testimonials | "Great product!" - John D. |
| User count | "10,000+ happy customers" |
| Ratings | ⭐⭐⭐⭐⭐ 4.8/5 |
| Logos | "Trusted by 500+ companies" |

### 4. Clear CTAs

| Bad | Good |
|-----|------|
| "Submit" | "Get Started Free" |
| "Click here" | "Download Now" |
| "Continue" | "Complete Your Purchase" |

**CTA Best Practices**:
- Action-oriented verb
- Specific benefit
- Contrasting color
- Above the fold

### 5. Trust Signals

| Signal | Placement |
|--------|-----------|
| Security badges | Checkout, forms |
| Money-back guarantee | Pricing, checkout |
| Contact info | Footer, about page |
| Reviews | Product pages |

## Landing Page Optimization

### Key Elements

```
┌─────────────────────────────────────────────────────────────────┐
│                      Landing Page Layout                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  [Headline: Clear Value Proposition]                       │ │
│  │  [Subheadline: Supporting benefit]                         │ │
│  │  [Hero Image/Video]                                       │ │
│  │  [Primary CTA: Get Started Free]                          │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  [Social Proof: Testimonials, Reviews, Logos]             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  [Benefits: What user gets]                                │ │
│  │  [Features: How it works]                                  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  [FAQ: Address objections]                                 │ │
│  │  [Secondary CTA: Not ready? Learn more]                    │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Best Practices

| Practice | Why |
|----------|-----|
| **Message match** | Align with ad copy |
| **Single CTA** | Don't overwhelm |
| **Above the fold** | Key info visible without scroll |
| **Remove navigation** | Reduce exits |
| **Benefit-focused** | Focus on value, not features |

## Form Optimization

### Field Reduction

| Fields | Impact |
|--------|--------|
| 5+ fields | Baseline |
| 4 fields | +5% |
| 3 fields | +10% |
| 2 fields | +15% |

### Form Best Practices

| Practice | Impact |
|----------|--------|
| Inline validation | +5% |
| Progress indicators | +10% |
| Clear labels | +5% |
| Smart defaults | +8% |
| Multi-step forms | +15% |

### Example: Optimized Signup Form

```
┌─────────────────────────────────────────────────────────────────┐
│  Sign Up for Free                                              │
│  ─────────────────────────────────────────────────────────────── │
│                                                                  │
│  Step 1 of 2: Account Info                                      │
│  ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  │
│                                                                  │
│  Email: [john@example.com] ✓ Valid                              │
│                                                                  │
│  Password: [••••••••] Strong                                    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  [Continue]                                                │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  By signing up, you agree to our Terms and Privacy Policy.      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Checkout Optimization

### Best Practices

| Practice | Impact |
|----------|--------|
| Guest checkout | +15-25% |
| Multiple payment options | +10% |
| Show total upfront | +8% |
| Trust badges | +5% |
| Exit-intent popup | +5-10% |

### Checkout Flow

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Cart      │───▶│  Shipping   │───▶│  Payment   │───▶│  Confirm   │
│             │    │             │    │             │    │             │
│ Review      │    │ Address     │    │ Method      │    │ Complete    │
│ Items       │    │ Options     │    │ Details     │    │ Order       │
│ ───────────  │    │ ─────────── │    │ ─────────── │    │ ─────────── │
│ [Guest]     │    │ [Saved]     │    │ [Cards]     │    │ [Place]     │
│ [Login]     │    │ [New]       │    │ [PayPal]    │    │ [Order]     │
│             │    │             │    │             │    │             │
│ Total: $99  │    │ Total: $99  │    │ Total: $99  │    │ Total: $99  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### Exit-Intent Popup

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
│  Wait! Don't leave empty-handed                                  │
│                                                                  │
│  Get 10% off your first order with code: SAVE10                 │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  [Apply Code & Continue Shopping]                           │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [No thanks, I'll pay full price]                               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Mobile Optimization

### Mobile-First Design

| Practice | Specification |
|----------|----------------|
| Tap targets | Minimum 44×44px |
| Font size | Minimum 16px |
| Form fields | Full width |
| Navigation | Bottom thumb zone |
| Load time | < 3 seconds |

### Mobile UX Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                      Mobile Layout                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  [Logo]              [Search]              [Cart (3)]     │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  [Product Image]                                          │ │
│  │  Product Name                                              │ │
│  │  $99.99                                                    │ │
│  │  ⭐⭐⭐⭐⭐ 4.8 (234 reviews)                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  [Add to Cart]                                             │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  Description                                               │ │
│  │  Features                                                 │ │
│  │  Reviews                                                  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  [Home]  [Search]  [Cart]  [Profile]                     │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Pricing Page Optimization

### Best Practices

| Practice | Impact |
|----------|--------|
| Clear plans | +10% |
| Highlight recommended | +15% |
| Annual discount | +20% |
| FAQ section | +8% |
| Feature comparison | +12% |

### Pricing Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                      Pricing Plans                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐  ┌─────────────────────────┐  ┌─────────────┐ │
│  │   Starter   │  │      RECOMMENDED        │  │   Pro       │ │
│  │             │  │                         │  │             │ │
│  │   $9/mo     │  │       $29/mo           │  │   $99/mo    │ │
│  │             │  │                         │  │             │
│  │ ✓ 1 user    │  │ ✓ 5 users              │  │ ✓ Unlimited │ │
│  │ ✓ 10GB      │  │ ✓ 100GB               │  │ ✓ 1TB       │
│  │ ✓ Email     │  │ ✓ Priority Support     │  │ ✓ 24/7      │
│  │ ✗ Analytics │  │ ✓ Analytics            │  │ ✓ API       │
│  │             │  │                         │  │             │
│  │ [Get       │  │ [Get Started]           │  │ [Contact    │ │
│  │  Started]  │  │                         │  │  Sales]     │ │
│  └─────────────┘  └─────────────────────────┘  └─────────────┘ │
│                                                                  │
│  💰 Save 20% with annual billing                                │
│                                                                  │
│  FAQ                                                             │
│  • Can I change plans later? Yes, anytime.                       │
│  • What's your refund policy? 30-day money-back guarantee.        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Prioritization Frameworks

### ICE Scoring

```
ICE = Impact × Confidence × Ease
```

| Test | Impact | Confidence | Ease | ICE | Priority |
|------|--------|------------|------|-----|----------|
| Add trust badges | 8 | 9 | 8 | 576 | 1 |
| Reduce form fields | 7 | 8 | 6 | 336 | 2 |
| New hero image | 5 | 5 | 7 | 175 | 3 |

### PIE Scoring

```
PIE = Potential × Importance × Ease
```

| Test | Potential | Importance | Ease | PIE | Priority |
|------|-----------|------------|------|-----|----------|
| Fix checkout bugs | 10 | 10 | 3 | 300 | 1 |
| Improve mobile UX | 8 | 8 | 5 | 320 | 2 |
| A/B test headline | 5 | 6 | 9 | 270 | 3 |

## Testing Methods

### A/B Testing

Split traffic between variants.

| Variant | Traffic |
|---------|---------|
| Control | 50% |
| Treatment | 50% |

### Multivariate Testing

Test multiple elements simultaneously.

| Button Color | Button Text | Traffic |
|--------------|-------------|---------|
| Blue | Buy Now | 25% |
| Blue | Add to Cart | 25% |
| Green | Buy Now | 25% |
| Green | Add to Cart | 25% |

### User Testing

Qualitative feedback before testing.

| Method | When to Use |
|--------|-------------|
| Usability testing | Before launch |
| A/B testing | After launch |
| Session analysis | Ongoing |

## Tools

### A/B Testing

| Tool | Features | Pricing |
|------|----------|---------|
| **Optimizely** | Enterprise features | $$$ |
| **VWO** | Visual editor | $$ |
| **Google Optimize** | Free, GA integration | Free (discontinued) |
| **Statsig** | Free tier | Free/$ |

### Analytics

| Tool | Use Case |
|------|----------|
| **Google Analytics 4** | Web analytics |
| **Mixpanel** | Product analytics |
| **Amplitude** | User behavior |
| **Hotjar** | Heatmaps, recordings |

### Heatmaps & Recordings

| Tool | Features |
|------|----------|
| **Hotjar** | Heatmaps, recordings, surveys |
| **Crazy Egg** | Heatmaps, scroll maps |
| **FullStory** | Session replay |
| **LogRocket** | Frontend monitoring |

## Metrics to Track

### Key CRO Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| **Conversion Rate** | Conversions / Visitors | 2-5% (varies) |
| **Bounce Rate** | Single-page sessions / Sessions | < 50% |
| **Time on Page** | Avg time on page | 2-3 min |
| **Pages per Session** | Pageviews / Sessions | 2-4 |
| **Cart Abandonment** | Abandoned / Started | 70-80% |

### Micro-Conversion Metrics

| Metric | Description |
|--------|-------------|
| **Click-through Rate** | CTR on CTAs |
| **Form Start Rate** | Users who start form |
| **Form Completion Rate** | Users who complete form |
| **Scroll Depth** | How far users scroll |

## Psychological Principles

### 1. Scarcity

Limited availability increases desire.

**Examples**:
- "Only 3 left in stock"
- "Offer ends in 2 hours"
- "Limited edition"

### 2. Urgency

Time pressure drives action.

**Examples**:
- Countdown timer
- "Last chance"
- "Today only"

### 3. Social Proof

Others are doing it, so should you.

**Examples**:
- Testimonials
- User count
- Ratings
- Logos

### 4. Authority

Expert endorsement builds trust.

**Examples**:
- "As seen in"
- Expert quotes
- Certifications

### 5. Reciprocity

Give value first, get value back.

**Examples**:
- Free trial
- Free content
- Samples

## Real Optimization Examples

### Example 1: E-commerce Checkout Flow

**Problem**: 70% cart abandonment

**Hypothesis**: Guest checkout will reduce abandonment

**Test**: Require login vs. Guest checkout

**Results**:
- Control (Login): 65% completion
- Treatment (Guest): 85% completion
- Lift: +31%

**Action**: Ship guest checkout

### Example 2: SaaS Signup Funnel

**Problem**: 15% signup completion

**Hypothesis**: Reduce form fields from 5 to 3

**Test**: 5 fields vs. 3 fields

**Results**:
- Control (5 fields): 15% completion
- Treatment (3 fields): 22% completion
- Lift: +47%

**Action**: Ship 3-field form

### Example 3: Lead Generation Form

**Problem**: 8% form completion

**Hypothesis**: Add social proof to increase trust

**Test**: Without testimonials vs. With testimonials

**Results**:
- Control: 8% completion
- Treatment: 12% completion
- Lift: +50%

**Action**: Ship with testimonials

## Implementation

### Funnel Analysis SQL

```sql
WITH funnel AS (
    SELECT
        'visit' AS stage,
        COUNT(DISTINCT session_id) AS users
    FROM page_views
    WHERE page_url = '/'

    UNION ALL

    SELECT
        'product' AS stage,
        COUNT(DISTINCT session_id) AS users
    FROM page_views
    WHERE page_url LIKE '/product/%'

    UNION ALL

    SELECT
        'cart' AS stage,
        COUNT(DISTINCT session_id) AS users
    FROM events
    WHERE event_type = 'add_to_cart'

    UNION ALL

    SELECT
        'checkout' AS stage,
        COUNT(DISTINCT session_id) AS users
    FROM page_views
    WHERE page_url = '/checkout'

    UNION ALL

    SELECT
        'purchase' AS stage,
        COUNT(DISTINCT session_id) AS users
    FROM events
    WHERE event_type = 'purchase'
)

SELECT
    stage,
    users,
    LAG(users) OVER (ORDER BY users DESC) AS previous_users,
    ROUND(100.0 * users / LAG(users) OVER (ORDER BY users DESC), 2) AS conversion_rate,
    ROUND(100.0 * (LAG(users) OVER (ORDER BY users DESC) - users) /
          LAG(users) OVER (ORDER BY users DESC), 2) AS drop_off
FROM funnel
ORDER BY users DESC;
```

### A/B Test Setup (JavaScript)

```javascript
// Simple A/B test implementation
const ABTest = {
  variants: ['A', 'B'],
  weights: [0.5, 0.5], // 50/50 split

  assignVariant(userId) {
    // Consistent assignment using hash
    const hash = this.hashCode(userId);
    const index = Math.abs(hash) % this.variants.length;
    return this.variants[index];
  },

  hashCode(str) {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      hash = ((hash << 5) - hash) + str.charCodeAt(i);
      hash = hash & hash;
    }
    return hash;
  },

  trackExposure(userId, variant, testName) {
    analytics.track('ab_test_exposure', {
      userId,
      testName,
      variant,
      timestamp: new Date().toISOString()
    });
  },

  trackConversion(userId, variant, testName) {
    analytics.track('ab_test_conversion', {
      userId,
      testName,
      variant,
      timestamp: new Date().toISOString()
    });
  }
};

// Usage
const userId = getUserId(); // Get user ID somehow
const variant = ABTest.assignVariant(userId);
ABTest.trackExposure(userId, variant, 'checkout_test');

// Apply variant
if (variant === 'A') {
  // Show control
} else {
  // Show treatment
}
```

## Summary Checklist

### Research Phase

- [ ] Analyze funnel drop-offs
- [ ] Review heatmaps and recordings
- [ ] Survey users
- [ ] Interview users
- [ ] Identify optimization opportunities

### Hypothesis Phase

- [ ] Formulate clear hypotheses
- [ ] Prioritize using ICE/PIE
- [ ] Document expected impact

### Testing Phase

- [ ] Set up A/B test
- [ ] Ensure proper tracking
- [ ] Run for required duration
- [ ] Monitor for issues

### Analysis Phase

- [ ] Calculate statistical significance
- [ ] Analyze results
- [ ] Document findings
- [ ] Implement winning variant
```

---

## Quick Start

### A/B Test Setup

```javascript
// Track conversion
function trackConversion(goal, variant) {
  analytics.track('conversion', {
    goal: goal,  // 'signup', 'purchase', etc.
    variant: variant,  // 'A' or 'B'
    timestamp: Date.now()
  })
}

// Calculate conversion rate
function calculateConversionRate(variant, goal) {
  const visitors = getVisitors(variant)
  const conversions = getConversions(variant, goal)
  return (conversions / visitors) * 100
}
```

---

## Production Checklist

- [ ] **Hypothesis**: Clear hypothesis and success metric
- [ ] **A/B Testing**: Set up A/B testing framework
- [ ] **Tracking**: Implement conversion tracking
- [ ] **Sample Size**: Calculate required sample size
- [ ] **Statistical Significance**: Use proper statistical tests
- [ ] **User Research**: Conduct user research
- [ ] **Heatmaps**: Use heatmaps to identify issues
- [ ] **Analytics**: Set up analytics tracking
- [ ] **Documentation**: Document test results
- [ ] **Implementation**: Implement winning variants
- [ ] **Monitoring**: Monitor conversion rates
- [ ] **Iteration**: Continuous improvement

---

## Anti-patterns

### ❌ Don't: Test Everything at Once

```javascript
// ❌ Bad - Too many changes
const variant = {
  newHeader: true,
  newButton: true,
  newLayout: true,
  newColors: true
  // Which change caused the improvement?
}
```

```javascript
// ✅ Good - One change at a time
const variant = {
  newHeader: true  // Test one change
}
// Then test next change
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

---

## Integration Points

- **A/B Testing Analysis** (`23-business-analytics/ab-testing-analysis/`) - Testing methodology
- **Dashboard Design** (`23-business-analytics/dashboard-design/`) - Results visualization
- **Analytics** (`23-business-analytics/`) - Conversion tracking

---

## Further Reading

- [CRO Best Practices](https://www.optimizely.com/optimization-glossary/conversion-rate-optimization/)
- [A/B Testing Guide](https://www.optimizely.com/optimization-glossary/ab-testing/)
- [ ] Document learnings
- [ ] Make recommendation

### Implementation Phase

- [ ] Ship winning variant
- [ ] Monitor post-implementation
- [ ] Document results
- [ ] Plan next tests
