---
name: A/B Testing Implementation
description: User experience research methodology where two versions of a variable are shown to different segments to determine which version drives better business metrics with proper statistical significance testing.
---

# A/B Testing Implementation

> **Current Level:** Intermediate  
> **Domain:** Marketing / Analytics

---

## Overview

A/B testing (split testing) is a user experience research methodology where two versions of a variable (webpage, app screen, email, etc.) are shown to different segments of visitors at the same time to determine which version leaves the maximum impact and drives business metrics.

---

## Core Concepts

### Table of Contents

1. [A/B Testing Concepts](#ab-testing-concepts)
2. [Experiment Design](#experiment-design)
3. [Statistical Significance](#statistical-significance)
4. [Sample Size Calculation](#sample-size-calculation)
5. [Implementation Approaches](#implementation-approaches)
6. [Libraries](#libraries)
7. [Tracking and Analytics](#tracking-and-analytics)
8. [Multi-variate Testing](#multi-variate-testing)
9. [Personalization](#personalization)
10. [Best Practices](#best-practices)
11. [Common Pitfalls](#common-pitfalls)

---

## A/B Testing Concepts

### Core Concepts

```typescript
// A/B test experiment structure
interface Experiment {
  id: string;
  name: string;
  description: string;
  status: 'draft' | 'running' | 'paused' | 'completed';
  hypothesis: string;
  successMetric: string;
  variants: Variant[];
  targeting?: TargetingRules;
  trafficAllocation: number; // 0-1, percentage of traffic to include
  startDate?: Date;
  endDate?: Date;
  winner?: string;
  createdAt: Date;
}

interface Variant {
  id: string;
  name: string;
  description: string;
  config: Record<string, any>;
  trafficWeight: number; // 0-1, relative weight
  isControl: boolean;
}

interface TargetingRules {
  audiences?: string[];
  deviceTypes?: ('desktop' | 'mobile' | 'tablet')[];
  countries?: string[];
  customRules?: Rule[];
}

interface Rule {
  type: 'user_attribute' | 'event' | 'cohort';
  operator: 'equals' | 'not_equals' | 'contains' | 'greater_than' | 'less_than' | 'in';
  value: any;
}

// Experiment result
interface ExperimentResult {
  experimentId: string;
  variantResults: VariantResult[];
  winner?: {
    variantId: string;
    confidence: number;
    improvement: number;
  };
  completedAt: Date;
}

interface VariantResult {
  variantId: string;
  sampleSize: number;
  conversions: number;
  conversionRate: number;
  confidenceInterval: {
    lower: number;
    upper: number;
  };
  pValue?: number;
  isSignificant?: boolean;
}
```

### Test Types

```typescript
enum ExperimentType {
  // UI/UX tests
  BUTTON_COLOR = 'button_color',
  HEADLINE_TEXT = 'headline_text',
  PAGE_LAYOUT = 'page_layout',
  FORM_FIELDS = 'form_fields',
  
  // Feature tests
  FEATURE_FLAG = 'feature_flag',
  PRICING_PAGE = 'pricing_page',
  ONBOARDING_FLOW = 'onboarding_flow',
  
  // Content tests
  EMAIL_SUBJECT = 'email_subject',
  EMAIL_CONTENT = 'email_content',
  LANDING_PAGE = 'landing_page',
  
  // Algorithm tests
  RECOMMENDATION_ENGINE = 'recommendation_engine',
  SEARCH_RANKING = 'search_ranking',
  SORT_ORDER = 'sort_order',
}
```

---

## Experiment Design

### Hypothesis Framework

```typescript
interface Hypothesis {
  if: string; // Condition
  then: string; // Expected outcome
  because: string; // Reasoning
  metric: string; // Success metric
  expectedChange: number; // Expected percentage change
}

// Example hypothesis
const exampleHypothesis: Hypothesis = {
  if: 'We change the CTA button color from blue to green',
  then: 'more users will click the button',
  because: 'green creates a sense of urgency and action',
  metric: 'button_click_rate',
  expectedChange: 15, // 15% increase
};

// Hypothesis validator
function validateHypothesis(hypothesis: Hypothesis): {
  valid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  if (!hypothesis.if || hypothesis.if.trim() === '') {
    errors.push('Hypothesis must specify the "if" condition');
  }

  if (!hypothesis.then || hypothesis.then.trim() === '') {
    errors.push('Hypothesis must specify the "then" outcome');
  }

  if (!hypothesis.because || hypothesis.because.trim() === '') {
    errors.push('Hypothesis must specify the reasoning');
  }

  if (!hypothesis.metric || hypothesis.metric.trim() === '') {
    errors.push('Hypothesis must specify the success metric');
  }

  if (hypothesis.expectedChange <= 0) {
    errors.push('Expected change must be positive');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
```

### Experiment Configuration

```typescript
interface ExperimentConfig {
  experimentId: string;
  variants: {
    [key: string]: {
      config: Record<string, any>;
      weight: number;
    };
  };
  targeting?: {
    include?: string[];
    exclude?: string[];
  };
  duration?: {
    minDays?: number;
    maxDays?: number;
  };
  stoppingRules?: StoppingRule[];
}

interface StoppingRule {
  type: 'statistical_significance' | 'time_based' | 'sample_size' | 'negative_impact';
  config: Record<string, any>;
}

// Example experiment config
const buttonColorExperiment: ExperimentConfig = {
  experimentId: 'button_color_test',
  variants: {
    control: {
      config: { buttonColor: '#007bff' },
      weight: 0.5,
    },
    variant_a: {
      config: { buttonColor: '#28a745' },
      weight: 0.5,
    },
  },
  duration: {
    minDays: 7,
    maxDays: 14,
  },
  stoppingRules: [
    {
      type: 'statistical_significance',
      config: { confidence: 0.95, minSampleSize: 1000 },
    },
    {
      type: 'negative_impact',
      config: { maxDrop: 0.1 }, // Stop if variant drops 10%
    },
  ],
};
```

---

## Statistical Significance

### Statistical Calculations

```typescript
// Z-score calculation
function calculateZScore(
  p1: number, // Conversion rate of control
  p2: number, // Conversion rate of variant
  n1: number, // Sample size of control
  n2: number  // Sample size of variant
): number {
  const pooledProportion = (p1 * n1 + p2 * n2) / (n1 + n2);
  const standardError = Math.sqrt(
    pooledProportion * (1 - pooledProportion) * (1 / n1 + 1 / n2)
  );

  return (p2 - p1) / standardError;
}

// P-value from Z-score
function calculatePValue(zScore: number): number {
  // Two-tailed test
  return 2 * (1 - normalCDF(Math.abs(zScore)));
}

// Normal cumulative distribution function
function normalCDF(x: number): number {
  const a1 = 0.254829592;
  const a2 = -0.284496736;
  const a3 = 1.421413741;
  const a4 = -1.453152027;
  const a5 = 1.061405429;
  const p = 0.3275911;

  const sign = x < 0 ? -1 : 1;
  x = Math.abs(x) / Math.sqrt(2);

  const t = 1.0 / (1.0 + p * x);
  const y =
    1.0 -
    (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * Math.exp(-x * x);

  return 0.5 * (1.0 + sign * y);
}

// Confidence interval
function calculateConfidenceInterval(
  p: number,
  n: number,
  confidence: number = 0.95
): { lower: number; upper: number } {
  const z = getZScoreForConfidence(confidence);
  const marginOfError = z * Math.sqrt((p * (1 - p)) / n);

  return {
    lower: p - marginOfError,
    upper: p + marginOfError,
  };
}

function getZScoreForConfidence(confidence: number): number {
  const confidenceLevels: Record<number, number> = {
    0.90: 1.645,
    0.95: 1.96,
    0.99: 2.576,
  };
  return confidenceLevels[confidence] || 1.96;
}

// Statistical significance test
function isStatisticallySignificant(
  controlConversions: number,
  controlSample: number,
  variantConversions: number,
  variantSample: number,
  confidence: number = 0.95
): {
  significant: boolean;
  pValue: number;
  zScore: number;
  improvement: number;
  confidenceInterval: { lower: number; upper: number };
} {
  const p1 = controlConversions / controlSample;
  const p2 = variantConversions / variantSample;

  const zScore = calculateZScore(p1, p2, controlSample, variantSample);
  const pValue = calculatePValue(zScore);
  const significant = pValue < (1 - confidence);
  const improvement = ((p2 - p1) / p1) * 100;
  const confidenceInterval = calculateConfidenceInterval(p2, variantSample, confidence);

  return {
    significant,
    pValue,
    zScore,
    improvement,
    confidenceInterval,
  };
}
```

### Bayesian Analysis

```typescript
// Bayesian A/B testing using Beta distribution
interface BayesianResult {
  probabilityToWin: number;
  expectedLoss: number;
  credibleInterval: { lower: number; upper: number };
}

function calculateBayesianResult(
  controlConversions: number,
  controlSample: number,
  variantConversions: number,
  variantSample: number,
  simulations: number = 100000
): BayesianResult {
  // Beta distribution parameters
  const controlAlpha = controlConversions + 1;
  const controlBeta = controlSample - controlConversions + 1;
  const variantAlpha = variantConversions + 1;
  const variantBeta = variantSample - variantConversions + 1;

  // Monte Carlo simulation
  let variantWins = 0;
  let totalLoss = 0;

  for (let i = 0; i < simulations; i++) {
    const controlRate = betaRandom(controlAlpha, controlBeta);
    const variantRate = betaRandom(variantAlpha, variantBeta);

    if (variantRate > controlRate) {
      variantWins++;
    }

    totalLoss += Math.max(0, controlRate - variantRate);
  }

  const probabilityToWin = variantWins / simulations;
  const expectedLoss = totalLoss / simulations;

  // Calculate credible interval
  const credibleInterval = calculateBetaCredibleInterval(
    variantAlpha,
    variantBeta,
    0.95
  );

  return {
    probabilityToWin,
    expectedLoss,
    credibleInterval,
  };
}

// Beta random number generator (approximation)
function betaRandom(alpha: number, beta: number): number {
  const u1 = Math.random();
  const u2 = Math.random();
  const gamma1 = Math.pow(u1, 1 / alpha);
  const gamma2 = Math.pow(u2, 1 / beta);
  return gamma1 / (gamma1 + gamma2);
}

// Beta distribution credible interval
function calculateBetaCredibleInterval(
  alpha: number,
  beta: number,
  confidence: number
): { lower: number; upper: number } {
  // Approximation using normal distribution for large samples
  const mean = alpha / (alpha + beta);
  const variance = (alpha * beta) / (Math.pow(alpha + beta, 2) * (alpha + beta + 1));
  const stdDev = Math.sqrt(variance);
  const z = getZScoreForConfidence(confidence);

  return {
    lower: Math.max(0, mean - z * stdDev),
    upper: Math.min(1, mean + z * stdDev),
  };
}
```

---

## Sample Size Calculation

### Sample Size Calculator

```typescript
interface SampleSizeParams {
  baselineRate: number; // Current conversion rate
  minimumDetectableEffect: number; // Minimum change to detect (as percentage)
  confidence: number; // Statistical confidence (0.95 for 95%)
  power: number; // Statistical power (0.8 for 80%)
}

interface SampleSizeResult {
  sampleSizePerVariant: number;
  totalSampleSize: number;
  estimatedDurationDays?: number;
}

function calculateSampleSize(params: SampleSizeParams): SampleSizeResult {
  const {
    baselineRate,
    minimumDetectableEffect,
    confidence = 0.95,
    power = 0.8,
  } = params;

  const p1 = baselineRate;
  const p2 = baselineRate * (1 + minimumDetectableEffect / 100);

  const alpha = 1 - confidence;
  const beta = 1 - power;

  const zAlpha = getZScoreForConfidence(confidence);
  const zBeta = getZScoreForConfidence(2 * power - 1);

  // Pooled proportion
  const pooledP = (p1 + p2) / 2;

  // Sample size formula
  const sampleSizePerVariant =
    (Math.pow(zAlpha + zBeta, 2) * 2 * pooledP * (1 - pooledP)) /
    Math.pow(p2 - p1, 2);

  const totalSampleSize = Math.ceil(sampleSizePerVariant * 2);

  return {
    sampleSizePerVariant: Math.ceil(sampleSizePerVariant),
    totalSampleSize,
  };
}

// Calculate estimated duration
function calculateEstimatedDuration(
  sampleSize: number,
  dailyVisitors: number,
  trafficAllocation: number = 1
): number {
  const dailyAllocatedVisitors = dailyVisitors * trafficAllocation;
  return Math.ceil(sampleSize / dailyAllocatedVisitors);
}

// Example usage
const sampleSizeResult = calculateSampleSize({
  baselineRate: 0.05, // 5% conversion rate
  minimumDetectableEffect: 20, // 20% improvement
  confidence: 0.95,
  power: 0.8,
});

console.log('Sample size per variant:', sampleSizeResult.sampleSizePerVariant);
console.log('Total sample size:', sampleSizeResult.totalSampleSize);
```

### Minimum Detectable Effect Calculator

```typescript
function calculateMinimumDetectableEffect(
  sampleSizePerVariant: number,
  baselineRate: number,
  confidence: number = 0.95,
  power: number = 0.8
): number {
  const alpha = 1 - confidence;
  const beta = 1 - power;

  const zAlpha = getZScoreForConfidence(confidence);
  const zBeta = getZScoreForConfidence(2 * power - 1);

  const pooledP = baselineRate;

  const minimumDifference =
    (zAlpha + zBeta) *
    Math.sqrt((2 * pooledP * (1 - pooledP)) / sampleSizePerVariant);

  return (minimumDifference / baselineRate) * 100;
}
```

---

## Implementation Approaches

### Client-Side Implementation

```typescript
// Client-side A/B testing SDK
class ClientSideABTesting {
  private experiments: Map<string, Experiment> = new Map();
  private userVariants: Map<string, string> = new Map();
  private userId: string;

  constructor(
    private apiBaseUrl: string,
    userId?: string
  ) {
    this.userId = userId || this.generateUserId();
    this.loadExperiments();
  }

  private generateUserId(): string {
    let userId = localStorage.getItem('ab_test_user_id');
    if (!userId) {
      userId = `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
      localStorage.setItem('ab_test_user_id', userId);
    }
    return userId;
  }

  async loadExperiments(): Promise<void> {
    const response = await fetch(`${this.apiBaseUrl}/experiments/active`);
    const experiments: Experiment[] = await response.json();

    for (const experiment of experiments) {
      this.experiments.set(experiment.id, experiment);
    }
  }

  getVariant(experimentId: string): string | null {
    // Check if already assigned
    if (this.userVariants.has(experimentId)) {
      return this.userVariants.get(experimentId)!;
    }

    const experiment = this.experiments.get(experimentId);
    if (!experiment || experiment.status !== 'running') {
      return null;
    }

    // Check targeting
    if (!this.isEligible(experiment)) {
      return null;
    }

    // Assign variant
    const variantId = this.assignVariant(experiment);
    this.userVariants.set(experimentId, variantId);

    // Track assignment
    this.trackAssignment(experimentId, variantId);

    return variantId;
  }

  private assignVariant(experiment: Experiment): string {
    const random = Math.random();
    let cumulative = 0;

    for (const variant of experiment.variants) {
      cumulative += variant.trafficWeight;
      if (random < cumulative) {
        return variant.id;
      }
    }

    return experiment.variants[0].id; // Fallback
  }

  private isEligible(experiment: Experiment): boolean {
    // Check traffic allocation
    if (Math.random() > experiment.trafficAllocation) {
      return false;
    }

    // Check targeting rules
    if (experiment.targeting) {
      return this.checkTargeting(experiment.targeting);
    }

    return true;
  }

  private checkTargeting(targeting: TargetingRules): boolean {
    // Implement targeting logic
    return true;
  }

  private async trackAssignment(
    experimentId: string,
    variantId: string
  ): Promise<void> {
    await fetch(`${this.apiBaseUrl}/events/assignment`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userId: this.userId,
        experimentId,
        variantId,
        timestamp: new Date().toISOString(),
        context: {
          url: window.location.href,
          userAgent: navigator.userAgent,
          device: this.detectDevice(),
        },
      }),
    });
  }

  trackConversion(experimentId: string, value?: number): void {
    const variantId = this.userVariants.get(experimentId);
    if (!variantId) return;

    fetch(`${this.apiBaseUrl}/events/conversion`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        userId: this.userId,
        experimentId,
        variantId,
        value,
        timestamp: new Date().toISOString(),
      }),
    });
  }

  private detectDevice(): 'desktop' | 'mobile' | 'tablet' {
    const width = window.innerWidth;
    if (width < 768) return 'mobile';
    if (width < 1024) return 'tablet';
    return 'desktop';
  }
}

// Usage
const abTesting = new ClientSideABTesting('/api/ab-testing', 'user_123');

// Get variant
const variant = abTesting.getVariant('button_color_test');

// Apply variant
if (variant === 'variant_a') {
  document.getElementById('cta-button').style.backgroundColor = '#28a745';
}

// Track conversion
document.getElementById('cta-button').addEventListener('click', () => {
  abTesting.trackConversion('button_color_test');
});
```

### Server-Side Implementation

```typescript
import express from 'express';

const app = express();

// A/B testing middleware
interface ABTestingConfig {
  experiments: Map<string, Experiment>;
  userAssignments: Map<string, Map<string, string>>;
}

const abConfig: ABTestingConfig = {
  experiments: new Map(),
  userAssignments: new Map(),
};

// Load experiments from database
async function loadExperiments(): Promise<void> {
  const experiments = await db.experiment.findMany({
    where: { status: 'running' },
    include: { variants: true },
  });

  for (const experiment of experiments) {
    abConfig.experiments.set(experiment.id, experiment);
  }
}

// Get or create user assignment
function getUserAssignment(userId: string, experimentId: string): string | null {
  if (!abConfig.userAssignments.has(userId)) {
    abConfig.userAssignments.set(userId, new Map());
  }

  const userExperiments = abConfig.userAssignments.get(userId)!;

  if (userExperiments.has(experimentId)) {
    return userExperiments.get(experimentId)!;
  }

  const experiment = abConfig.experiments.get(experimentId);
  if (!experiment) return null;

  const variantId = assignVariant(experiment);
  userExperiments.set(experimentId, variantId);

  return variantId;
}

function assignVariant(experiment: Experiment): string {
  const random = Math.random();
  let cumulative = 0;

  for (const variant of experiment.variants) {
    cumulative += variant.trafficWeight;
    if (random < cumulative) {
      return variant.id;
    }
  }

  return experiment.variants[0].id;
}

// A/B testing middleware
function abTestingMiddleware(experimentId: string) {
  return (req: express.Request, res: express.Response, next: express.NextFunction) => {
    const userId = req.session?.userId || req.ip;
    const variantId = getUserAssignment(userId, experimentId);

    if (variantId) {
      req.abVariant = variantId;
      req.abExperiment = experimentId;
    }

    next();
  };
}

// Usage in routes
app.get('/landing', abTestingMiddleware('landing_page_test'), (req, res) => {
  const variantId = req.abVariant;

  if (variantId === 'variant_a') {
    res.render('landing-variant-a');
  } else {
    res.render('landing-control');
  }
});

// Track conversion endpoint
app.post('/api/ab-testing/conversion', express.json(), async (req, res) => {
  const { userId, experimentId, variantId, value } = req.body;

  await db.conversion.create({
    data: {
      userId,
      experimentId,
      variantId,
      value,
      timestamp: new Date(),
    },
  });

  res.json({ success: true });
});
```

### Edge Implementation (Vercel Edge Config)

```typescript
// Vercel Edge Config for A/B testing
import { NextRequest, NextResponse } from 'next/server';

// Edge Config
const edgeConfig = {
  experiments: {
    'button_color_test': {
      variants: [
        { id: 'control', weight: 0.5, config: { color: '#007bff' } },
        { id: 'variant_a', weight: 0.5, config: { color: '#28a745' } },
      ],
    },
  },
};

function getVariantFromEdge(
  experimentId: string,
  userId: string
): { variantId: string; config: any } | null {
  const experiment = edgeConfig.experiments[experimentId];
  if (!experiment) return null;

  // Consistent hash for user
  const hash = simpleHash(userId + experimentId);
  const random = (hash % 100) / 100;

  let cumulative = 0;
  for (const variant of experiment.variants) {
    cumulative += variant.weight;
    if (random < cumulative) {
      return { variantId: variant.id, config: variant.config };
    }
  }

  return { variantId: experiment.variants[0].id, config: experiment.variants[0].config };
}

function simpleHash(str: string): number {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash; // Convert to 32-bit integer
  }
  return Math.abs(hash);
}

// Edge middleware
export function middleware(request: NextRequest) {
  const userId = request.cookies.get('user_id')?.value || request.ip;
  const variant = getVariantFromEdge('button_color_test', userId);

  if (variant) {
    const response = NextResponse.next();
    response.headers.set('x-ab-variant', variant.variantId);
    response.headers.set('x-ab-config', JSON.stringify(variant.config));
    return response;
  }

  return NextResponse.next();
}
```

---

## Libraries

### GrowthBook

```typescript
// npm install @growthbook/growthbook-react
import { GrowthBook, GrowthBookProvider } from '@growthbook/growthbook-react';

// Initialize GrowthBook
const growthbook = new GrowthBook({
  apiHost: 'https://cdn.growthbook.io',
  clientKey: process.env.GROWTHBOOK_CLIENT_KEY!,
  enableDevMode: process.env.NODE_ENV === 'development',
  subscribeToChanges: true,
  trackingCallback: (experiment, result) => {
    // Track experiment view
    analytics.track('Experiment Viewed', {
      experimentId: experiment.key,
      variationId: result.key,
    });
  },
});

// Set user attributes
growthbook.setAttributes({
  id: userId,
  email: userEmail,
  country: userCountry,
  customAttribute: customValue,
});

// Use in React component
function MyComponent() {
  const { value } = useFeature('new-feature-flag');

  if (value) {
    return <NewFeature />;
  }

  return <OldFeature />;
}

// Run experiment
const { value, variationId } = growthbook.runExperiment({
  key: 'button-color-test',
  variations: ['#007bff', '#28a745', '#dc3545'],
  weights: [0.5, 0.3, 0.2],
});

// Track conversion
growthbook.track('button-clicked', {
  experimentId: 'button-color-test',
  variationId,
});
```

### Statsig

```typescript
// npm install statsig-react
import { StatsigProvider, useGate, useExperiment, useLogEvent } from 'statsig-react';

// Initialize Statsig
<StatsigProvider
  sdkKey={process.env.STATSIG_SDK_KEY!}
  user={{ userID: userId, email: userEmail }}
  options={{
    environment: { tier: process.env.NODE_ENV },
  }}
>
  <App />
</StatsigProvider>;

// Use feature gate
function MyComponent() {
  const { value: isEnabled, isLoading } = useGate('new_feature_gate');

  if (isLoading) return <LoadingSpinner />;
  if (!isEnabled) return <OldFeature />;

  return <NewFeature />;
}

// Use experiment
function ExperimentComponent() {
  const { config, isLoading } = useExperiment('button_color_experiment');
  const logEvent = useLogEvent();

  if (isLoading) return <LoadingSpinner />;

  return (
    <button
      style={{ backgroundColor: config.buttonColor }}
      onClick={() => logEvent('button_clicked')}
    >
      Click Me
    </button>
  );
}
```

### LaunchDarkly

```typescript
// npm install launchdarkly-react-client-sdk
import { withLDProvider, useFlags, useLDClient } from 'launchdarkly-react-client-sdk';

// Initialize LaunchDarkly
const App = withLDProvider({
  clientSideID: process.env.LAUNCHDARKLY_CLIENT_ID!,
  user: {
    key: userId,
    email: userEmail,
    custom: {
      country: userCountry,
      plan: userPlan,
    },
  },
  options: {
    streaming: true,
  },
})(RootComponent);

// Use feature flags
function MyComponent() {
  const flags = useFlags();
  const ldClient = useLDClient();

  if (flags.newFeature) {
    return <NewFeature />;
  }

  return <OldFeature />;
}

// Track custom event
ldClient.track('button_clicked', {
  buttonColor: flags.buttonColor,
});
```

---

## Tracking and Analytics

### Event Tracking

```typescript
// A/B testing event tracker
class ABTestingEventTracker {
  constructor(private apiBaseUrl: string) {}

  async trackAssignment(event: {
    userId: string;
    experimentId: string;
    variantId: string;
    context?: Record<string, any>;
  }): Promise<void> {
    await this.sendEvent('assignment', event);
  }

  async trackConversion(event: {
    userId: string;
    experimentId: string;
    variantId: string;
    value?: number;
    context?: Record<string, any>;
  }): Promise<void> {
    await this.sendEvent('conversion', event);
  }

  async trackView(event: {
    userId: string;
    experimentId: string;
    variantId: string;
    context?: Record<string, any>;
  }): Promise<void> {
    await this.sendEvent('view', event);
  }

  private async sendEvent(
    type: string,
    event: Record<string, any>
  ): Promise<void> {
    await fetch(`${this.apiBaseUrl}/events/${type}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...event,
        timestamp: new Date().toISOString(),
      }),
    });
  }

  // Batch events for performance
  private eventQueue: Array<{ type: string; event: Record<string, any> }> = [];
  private flushInterval: number = 5000;

  queueEvent(type: string, event: Record<string, any>): void {
    this.eventQueue.push({ type, event });

    if (this.eventQueue.length >= 10) {
      this.flush();
    }
  }

  async flush(): Promise<void> {
    if (this.eventQueue.length === 0) return;

    const events = [...this.eventQueue];
    this.eventQueue = [];

    await fetch(`${this.apiBaseUrl}/events/batch`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ events }),
    });
  }
}
```

### Analytics Integration

```typescript
// Integrate with Google Analytics 4
function trackExperimentWithGA4(
  experimentId: string,
  variantId: string,
  userId: string
): void {
  gtag('event', 'experiment_viewed', {
    experiment_id: experimentId,
    variant_id: variantId,
    user_id: userId,
  });
}

function trackConversionWithGA4(
  experimentId: string,
  variantId: string,
  value?: number
): void {
  gtag('event', 'conversion', {
    experiment_id: experimentId,
    variant_id: variantId,
    value,
  });
}

// Integrate with Mixpanel
function trackExperimentWithMixpanel(
  experimentId: string,
  variantId: string,
  userId: string
): void {
  mixpanel.track('Experiment Viewed', {
    experiment_id: experimentId,
    variant_id: variantId,
  });
}

function trackConversionWithMixpanel(
  experimentId: string,
  variantId: string,
  value?: number
): void {
  mixpanel.track('Conversion', {
    experiment_id: experimentId,
    variant_id: variantId,
    value,
  });
}
```

---

## Multi-variate Testing

### MVT Implementation

```typescript
interface MultivariateExperiment {
  id: string;
  name: string;
  factors: Factor[];
  combinations?: Combination[];
}

interface Factor {
  id: string;
  name: string;
  levels: Level[];
}

interface Level {
  id: string;
  name: string;
  config: Record<string, any>;
}

interface Combination {
  id: string;
  levels: Record<string, string>; // factorId -> levelId
  config: Record<string, any>;
  weight: number;
}

// Generate all combinations
function generateCombinations(factors: Factor[]): Combination[] {
  const combinations: Combination[] = [];
  const levelIds = factors.map(f => f.levels.map(l => l.id));

  function generate(current: Record<string, string>, index: number): void {
    if (index >= factors.length) {
      combinations.push({
        id: Object.values(current).join('-'),
        levels: { ...current },
        config: mergeConfigs(current, factors),
        weight: 1,
      });
      return;
    }

    for (const levelId of levelIds[index]) {
      current[factors[index].id] = levelId;
      generate(current, index + 1);
    }
  }

  generate({}, 0);
  return combinations;
}

function mergeConfigs(
  levelSelection: Record<string, string>,
  factors: Factor[]
): Record<string, any> {
  const config: Record<string, any> = {};

  for (const [factorId, levelId] of Object.entries(levelSelection)) {
    const factor = factors.find(f => f.id === factorId);
    const level = factor?.levels.find(l => l.id === levelId);
    Object.assign(config, level?.config);
  }

  return config;
}

// Example MVT experiment
const mvtExperiment: MultivariateExperiment = {
  id: 'landing_page_mvt',
  name: 'Landing Page MVT',
  factors: [
    {
      id: 'headline',
      name: 'Headline',
      levels: [
        { id: 'h1', name: 'Headline 1', config: { headline: 'Welcome to Our App' } },
        { id: 'h2', name: 'Headline 2', config: { headline: 'Start Your Journey Today' } },
      ],
    },
    {
      id: 'button_color',
      name: 'Button Color',
      levels: [
        { id: 'b1', name: 'Blue', config: { buttonColor: '#007bff' } },
        { id: 'b2', name: 'Green', config: { buttonColor: '#28a745' } },
        { id: 'b3', name: 'Red', config: { buttonColor: '#dc3545' } },
      ],
    },
    {
      id: 'button_text',
      name: 'Button Text',
      levels: [
        { id: 't1', name: 'Sign Up', config: { buttonText: 'Sign Up' } },
        { id: 't2', name: 'Get Started', config: { buttonText: 'Get Started' } },
      ],
    },
  ],
};

// Generate combinations
const combinations = generateCombinations(mvtExperiment.factors);
console.log(`Generated ${combinations.length} combinations`);
```

---

## Personalization

### Personalization Engine

```typescript
interface PersonalizationRule {
  id: string;
  name: string;
  condition: Condition;
  variants: {
    [key: string]: Record<string, any>;
  };
}

interface Condition {
  type: 'user_attribute' | 'behavior' | 'cohort';
  field?: string;
  operator?: string;
  value?: any;
}

class PersonalizationEngine {
  private rules: Map<string, PersonalizationRule> = new Map();

  addRule(rule: PersonalizationRule): void {
    this.rules.set(rule.id, rule);
  }

  getPersonalizedContent(
    userId: string,
    defaultContent: Record<string, any>
  ): Record<string, any> {
    let personalizedContent = { ...defaultContent };

    for (const rule of this.rules.values()) {
      if (this.matchesRule(userId, rule)) {
        // Apply personalization
        const variant = this.selectVariant(rule);
        personalizedContent = { ...personalizedContent, ...variant };
      }
    }

    return personalizedContent;
  }

  private matchesRule(userId: string, rule: PersonalizationRule): boolean {
    // Implement rule matching logic
    return true;
  }

  private selectVariant(rule: PersonalizationRule): Record<string, any> {
    const variants = Object.values(rule.variants);
    return variants[Math.floor(Math.random() * variants.length)];
  }
}

// Example personalization rule
const locationBasedRule: PersonalizationRule = {
  id: 'location_personalization',
  name: 'Location-based Personalization',
  condition: {
    type: 'user_attribute',
    field: 'country',
    operator: 'equals',
    value: 'US',
  },
  variants: {
    default: { currency: 'USD', language: 'en' },
    eu: { currency: 'EUR', language: 'en' },
  };
};
```

---

## Best Practices

### Experiment Design Checklist

```typescript
interface ExperimentChecklist {
  hypothesis: boolean;
  metrics: boolean;
  sampleSize: boolean;
  duration: boolean;
  segmentation: boolean;
  tracking: boolean;
  documentation: boolean;
}

function validateExperiment(experiment: Experiment): ExperimentChecklist {
  return {
    hypothesis: !!experiment.hypothesis,
    metrics: !!experiment.successMetric,
    sampleSize: experiment.variants.every(v => v.trafficWeight > 0),
    duration: !!experiment.duration,
    segmentation: !!experiment.targeting,
    tracking: true, // Ensure tracking is set up
    documentation: !!experiment.description,
  };
}
```

### Common Best Practices

```typescript
// 1. Always have a control group
const hasControl = experiment.variants.some(v => v.isControl);

// 2. Don't stop tests too early
function shouldContinueTest(
  experiment: Experiment,
  results: ExperimentResult
): boolean {
  const minDuration = 7 * 24 * 60 * 60 * 1000; // 7 days
  const minSampleSize = 1000;

  const elapsed = Date.now() - (experiment.startDate?.getTime() || 0);
  const totalSampleSize = results.variantResults.reduce(
    (sum, r) => sum + r.sampleSize,
    0
  );

  return elapsed < minDuration || totalSampleSize < minSampleSize;
}

// 3. Account for multiple comparisons
function bonferroniCorrection(pValue: number, numComparisons: number): number {
  return Math.min(pValue * numComparisons, 1);
}

// 4. Segment analysis
function analyzeBySegment(
  results: ExperimentResult,
  segment: string
): ExperimentResult {
  // Filter results by segment
  return results;
}
```

---

## Common Pitfalls

### Pitfall Detection

```typescript
// Detect peeking (checking results too frequently)
class PeekingDetector {
  private checkHistory: Map<string, Date[]> = new Map();

  recordCheck(experimentId: string): void {
    if (!this.checkHistory.has(experimentId)) {
      this.checkHistory.set(experimentId, []);
    }
    this.checkHistory.get(experimentId)!.push(new Date());
  }

  isPeeking(experimentId: string, maxChecksPerDay: number = 3): boolean {
    const checks = this.checkHistory.get(experimentId) || [];
    const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);

    const recentChecks = checks.filter(c => c > oneDayAgo);
    return recentChecks.length > maxChecksPerDay;
  }
}

// Detect sample ratio mismatch
function detectSampleRatioMismatch(
  expectedWeights: number[],
  actualCounts: number[],
  threshold: number = 0.05
): boolean {
  const total = actualCounts.reduce((sum, c) => sum + c, 0);
  const chiSquare = actualCounts.reduce((sum, count, i) => {
    const expected = total * expectedWeights[i];
    return sum + Math.pow(count - expected, 2) / expected;
  }, 0);

  const degreesOfFreedom = expectedWeights.length - 1;
  const criticalValue = getChiSquareCriticalValue(degreesOfFreedom, 0.95);

  return chiSquare > criticalValue;
}

function getChiSquareCriticalValue(df: number, alpha: number): number {
  // Simplified chi-square critical values
  const values: Record<number, number> = {
    1: 3.841,
    2: 5.991,
    3: 7.815,
    4: 9.488,
    5: 11.07,
  };
  return values[df] || 11.07;
}
```

---

## Resources

- [GrowthBook Documentation](https://docs.growthbook.io/)
- [Statsig Documentation](https://docs.statsig.com/)
---

## Quick Start

### A/B Test Implementation

```typescript
// Assign variant
function assignVariant(userId: string): 'A' | 'B' {
  const hash = hashUserId(userId)
  return hash % 2 === 0 ? 'A' : 'B'
}

// Track conversion
function trackConversion(userId: string, variant: string, converted: boolean) {
  analytics.track('ab_test_conversion', {
    userId,
    variant,
    converted,
    testName: 'button-color-test'
  })
}
```

---

## Production Checklist

- [ ] **Hypothesis**: Clear hypothesis and success metric
- [ ] **Sample Size**: Calculate required sample size
- [ ] **Randomization**: Proper random assignment
- [ ] **Tracking**: Implement conversion tracking
- [ ] **Statistical Significance**: Use proper statistical tests
- [ ] **Duration**: Run test for sufficient duration
- [ ] **No Peeking**: Don't peek at results early
- [ ] **Documentation**: Document test setup and results
- [ ] **Implementation**: Implement winning variant
- [ ] **Monitoring**: Monitor test performance
- [ ] **Testing**: Test implementation
- [ ] **Learning**: Document learnings

---

## Anti-patterns

### ❌ Don't: Peek Early

```typescript
// ❌ Bad - Check results too early
if (day === 1) {
  checkResults()  // Too early!
}
```

```typescript
// ✅ Good - Wait for sample size
const requiredSampleSize = calculateSampleSize(alpha, power, effectSize)
if (totalVisitors >= requiredSampleSize) {
  checkResults()
}
```

### ❌ Don't: No Statistical Significance

```typescript
// ❌ Bad - No significance test
if (variantB.rate > variantA.rate) {
  return 'B wins'  // Could be random!
}
```

```typescript
// ✅ Good - Statistical significance
const pValue = calculatePValue(variantA, variantB)
if (pValue < 0.05 && variantB.rate > variantA.rate) {
  return 'B wins (statistically significant)'
}
```

---

## Integration Points

- **A/B Testing Analysis** (`23-business-analytics/ab-testing-analysis/`) - Analysis methodology
- **Conversion Optimization** (`23-business-analytics/conversion-optimization/`) - CRO
- **Analytics** (`23-business-analytics/`) - Tracking

---

## Further Reading

- [A/B Testing Guide](https://www.optimizely.com/optimization-glossary/ab-testing/)
- [Statistical Significance](https://www.investopedia.com/terms/s/statistical-significance.asp)

- [LaunchDarkly Documentation](https://docs.launchdarkly.com/)
- [Google Optimize](https://optimize.google.com/)
- [A/B Testing Calculator](https://www.optimizely.com/sample-size-calculator/)
