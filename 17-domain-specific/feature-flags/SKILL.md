# Feature Flags

## Overview

Feature flags allow you to enable or disable features without deploying code. This skill covers feature flag concepts, implementation approaches, libraries (LaunchDarkly, Unleash, custom), flag types (boolean, multivariate, gradual rollout), targeting rules, A/B testing, flag lifecycle, technical debt management, and best practices.

## Table of Contents

1. [Feature Flag Concepts](#feature-flag-concepts)
2. [Implementation Approaches](#implementation-approaches)
3. [Libraries](#libraries)
   - [LaunchDarkly](#launchdarkly)
   - [Unleash](#unleash)
   - [Custom Solution](#custom-solution)
4. [Flag Types](#flag-types)
   - [Boolean](#boolean)
   - [Multivariate](#multivariate)
   - [Gradual Rollout](#gradual-rollout)
5. [Targeting Rules](#targeting-rules)
6. [A/B Testing](#ab-testing)
7. [Flag Lifecycle](#flag-lifecycle)
8. [Technical Debt Management](#technical-debt-management)
9. [Best Practices](#best-practices)

---

## Feature Flag Concepts

### Why Feature Flags?

1. **Deploy without releasing**: Deploy code without exposing features
2. **Gradual rollout**: Roll out features to subsets of users
3. **A/B testing**: Test different variations
4. **Kill switches**: Quickly disable problematic features
5. **Personalization**: Customize features per user

### Feature Flag Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Boolean** | On/Off | Simple feature toggles |
| **Multivariate** | Multiple values | Testing different variations |
| **Gradual Rollout** | Percentage-based | Phased releases |

---

## Implementation Approaches

### Simple Boolean Flag

```typescript
// src/flags/feature-flags.ts
export const FeatureFlags = {
  NEW_DASHBOARD: process.env.FEATURE_NEW_DASHBOARD === 'true',
  DARK_MODE: process.env.FEATURE_DARK_MODE === 'true',
  BETA_FEATURE: process.env.FEATURE_BETA === 'true',
};

export function isFeatureEnabled(flag: keyof typeof FeatureFlags): boolean {
  return FeatureFlags[flag];
}
```

```typescript
// src/components/Dashboard.tsx
import { isFeatureEnabled } from '../flags/feature-flags';

export function Dashboard() {
  if (isFeatureEnabled('NEW_DASHBOARD')) {
    return <NewDashboard />;
  }
  return <OldDashboard />;
}
```

### Database-Backed Flags

```typescript
// src/models/feature-flag.model.ts
import { Model, DataTypes } from 'sequelize';

class FeatureFlag extends Model {
  public id!: number;
  public key!: string;
  public value!: string;
  public enabled!: boolean;
  public rolloutPercentage!: number;
  public createdAt!: Date;
  public updatedAt!: Date;
}

FeatureFlag.init({
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
  },
  key: {
    type: DataTypes.STRING,
    allowNull: false,
    unique: true,
  },
  value: {
    type: DataTypes.TEXT,
    allowNull: true,
  },
  enabled: {
    type: DataTypes.BOOLEAN,
    defaultValue: false,
  },
  rolloutPercentage: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
  },
  createdAt: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW,
  },
  updatedAt: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW,
  },
}, {
  sequelize,
  modelName: 'FeatureFlag',
});

export default FeatureFlag;
```

```typescript
// src/services/feature-flag.service.ts
import FeatureFlag from '../models/feature-flag.model';

export class FeatureFlagService {
  private cache: Map<string, FeatureFlag> = new Map();

  async isEnabled(key: string, userId?: string): Promise<boolean> {
    // Check cache first
    if (this.cache.has(key)) {
      const flag = this.cache.get(key)!;
      return this.evaluateFlag(flag, userId);
    }

    // Load from database
    const flag = await FeatureFlag.findOne({ where: { key } });
    
    if (!flag) {
      return false;
    }

    // Cache the flag
    this.cache.set(key, flag);

    return this.evaluateFlag(flag, userId);
  }

  async getValue<T>(key: string, userId?: string): Promise<T | null> {
    const flag = await FeatureFlag.findOne({ where: { key } });
    
    if (!flag || !flag.enabled) {
      return null;
    }

    if (flag.value) {
      try {
        return JSON.parse(flag.value) as T;
      } catch {
        return flag.value as T;
      }
    }

    return null;
  }

  private evaluateFlag(flag: FeatureFlag, userId?: string): boolean {
    if (!flag.enabled) {
      return false;
    }

    // If no rollout percentage, return enabled status
    if (flag.rolloutPercentage === 0 || flag.rolloutPercentage === 100) {
      return flag.enabled;
    }

    // Gradual rollout based on user ID
    if (userId) {
      const hash = this.hashUserId(userId);
      const percentage = hash % 100;
      return percentage < flag.rolloutPercentage;
    }

    // Random rollout for anonymous users
    return Math.random() * 100 < flag.rolloutPercentage;
  }

  private hashUserId(userId: string): number {
    let hash = 0;
    for (let i = 0; i < userId.length; i++) {
      const char = userId.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash);
  }

  async clearCache(): Promise<void> {
    this.cache.clear();
  }
}

export const featureFlagService = new FeatureFlagService();
```

---

## Libraries

### LaunchDarkly

#### Installation

```bash
npm install launchdarkly-node-server-sdk
```

#### Setup

```typescript
// src/flags/launchdarkly.ts
import * as ld from 'launchdarkly-node-server-sdk';

const client = ld.init(process.env.LAUNCHDARKLY_SDK_KEY!, {
  streamUri: 'https://stream.launchdarkly.us',
  eventsUri: 'https://events.launchdarkly.us',
});

export const launchDarklyClient = client;

export async function isFeatureEnabled(
  key: string,
  user: LDUser,
  defaultValue: boolean = false
): Promise<boolean> {
  return await client.variation(key, user, defaultValue);
}

export async function getFeatureValue<T>(
  key: string,
  user: LDUser,
  defaultValue: T
): Promise<T> {
  return await client.variation(key, user, defaultValue);
}
```

#### Usage

```typescript
// src/services/user.service.ts
import { isFeatureEnabled } from '../flags/launchdarkly';

export class UserService {
  async getUser(userId: string) {
    const user: LDUser = {
      key: userId,
      email: 'user@example.com',
      custom: {
        plan: 'premium',
      },
    };

    const newProfileEnabled = await isFeatureEnabled(
      'new-user-profile',
      user,
      false
    );

    if (newProfileEnabled) {
      return this.getNewUserProfile(userId);
    }
    return this.getOldUserProfile(userId);
  }
}
```

### Unleash

#### Installation

```bash
npm install unleash-client
```

#### Setup

```typescript
// src/flags/unleash.ts
import { UnleashClient } from 'unleash-client';

const unleash = new UnleashClient({
  url: process.env.UNLEASH_URL!,
  appName: 'my-app',
  instanceId: process.env.UNLEASH_INSTANCE_ID!,
  refreshInterval: 15000,
  metricsInterval: 60000,
});

unleash.on('error', console.error);
unleash.on('warn', console.warn);

export const unleashClient = unleash;

export function isFeatureEnabled(
  key: string,
  context?: UnleashContext
): boolean {
  return unleash.isEnabled(key, context);
}

export function getFeatureVariant(
  key: string,
  context?: UnleashContext
): Variant {
  return unleash.getVariant(key, context);
}
```

#### Usage

```typescript
// src/components/FeatureToggle.tsx
import { isFeatureEnabled } from '../flags/unleash';

interface FeatureToggleProps {
  featureKey: string;
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function FeatureToggle({ featureKey, children, fallback = null }: FeatureToggleProps) {
  const enabled = isFeatureEnabled(featureKey);

  if (enabled) {
    return <>{children}</>;
  }
  return <>{fallback}</>;
}
```

### Custom Solution

#### Redis-Backed Feature Flags

```typescript
// src/flags/redis-feature-flags.ts
import Redis from 'ioredis';

interface FeatureFlagConfig {
  key: string;
  enabled: boolean;
  value?: any;
  rolloutPercentage?: number;
  targetingRules?: TargetingRule[];
}

interface TargetingRule {
  attribute: string;
  operator: 'equals' | 'contains' | 'in' | 'notIn';
  values: any[];
}

class RedisFeatureFlagService {
  private cache: Map<string, FeatureFlagConfig> = new Map();
  private readonly CACHE_TTL = 60; // seconds

  constructor(private redis: Redis) {}

  async isEnabled(key: string, context?: Record<string, any>): Promise<boolean> {
    const config = await this.getFlagConfig(key);
    
    if (!config || !config.enabled) {
      return false;
    }

    // Check targeting rules
    if (config.targetingRules && context) {
      const matchesRules = this.evaluateTargetingRules(config.targetingRules, context);
      if (!matchesRules) {
        return false;
      }
    }

    // Check rollout percentage
    if (config.rolloutPercentage && config.rolloutPercentage < 100) {
      const userId = context?.userId || context?.sessionId;
      if (userId) {
        const hash = this.hashUserId(userId);
        const percentage = hash % 100;
        return percentage < config.rolloutPercentage;
      }
      return Math.random() * 100 < config.rolloutPercentage;
    }

    return true;
  }

  async getValue<T>(key: string, context?: Record<string, any>): Promise<T | null> {
    const enabled = await this.isEnabled(key, context);
    
    if (!enabled) {
      return null;
    }

    const config = await this.getFlagConfig(key);
    return config.value || null;
  }

  async setFlag(config: FeatureFlagConfig): Promise<void> {
    const key = `feature-flag:${config.key}`;
    await this.redis.set(key, JSON.stringify(config));
    await this.redis.expire(key, this.CACHE_TTL);
    this.cache.set(config.key, config);
  }

  async deleteFlag(key: string): Promise<void> {
    const redisKey = `feature-flag:${key}`;
    await this.redis.del(redisKey);
    this.cache.delete(key);
  }

  private async getFlagConfig(key: string): Promise<FeatureFlagConfig | null> {
    // Check cache
    if (this.cache.has(key)) {
      return this.cache.get(key)!;
    }

    // Load from Redis
    const redisKey = `feature-flag:${key}`;
    const data = await this.redis.get(redisKey);
    
    if (!data) {
      return null;
    }

    const config = JSON.parse(data) as FeatureFlagConfig;
    this.cache.set(key, config);
    return config;
  }

  private evaluateTargetingRules(
    rules: TargetingRule[],
    context: Record<string, any>
  ): boolean {
    for (const rule of rules) {
      const value = context[rule.attribute];
      
      switch (rule.operator) {
        case 'equals':
          if (value !== rule.values[0]) {
            return false;
          }
          break;
        case 'contains':
          if (!value || !value.includes(rule.values[0])) {
            return false;
          }
          break;
        case 'in':
          if (!rule.values.includes(value)) {
            return false;
          }
          break;
        case 'notIn':
          if (rule.values.includes(value)) {
            return false;
          }
          break;
      }
    }
    return true;
  }

  private hashUserId(userId: string): number {
    let hash = 0;
    for (let i = 0; i < userId.length; i++) {
      const char = userId.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash);
  }
}

export const redisFeatureFlagService = new RedisFeatureFlagService(new Redis());
```

---

## Flag Types

### Boolean

```typescript
// src/flags/boolean-flag.ts
export async function useBooleanFlag(
  key: string,
  context?: Record<string, any>
): Promise<boolean> {
  return await featureFlagService.isEnabled(key, context);
}

// Usage
const newDashboardEnabled = await useBooleanFlag('new-dashboard', { userId: '123' });

if (newDashboardEnabled) {
  // Show new dashboard
} else {
  // Show old dashboard
}
```

### Multivariate

```typescript
// src/flags/multivariate-flag.ts
interface MultivariateOption {
  value: string;
  weight: number;
}

export async function useMultivariateFlag(
  key: string,
  context?: Record<string, any>
): Promise<string | null> {
  const config = await featureFlagService.getFlagConfig(key);
  
  if (!config || !config.enabled) {
    return null;
  }

  const options = config.value as MultivariateOption[];
  const totalWeight = options.reduce((sum, opt) => sum + opt.weight, 0);
  const random = Math.random() * totalWeight;
  
  let cumulativeWeight = 0;
  for (const option of options) {
    cumulativeWeight += option.weight;
    if (random < cumulativeWeight) {
      return option.value;
    }
  }

  return options[0].value;
}

// Usage
const buttonColor = await useMultivariateFlag('button-color', { userId: '123' });

// buttonColor could be 'blue', 'green', or 'red'
```

### Gradual Rollout

```typescript
// src/flags/gradual-rollout.ts
export async function useGradualRollout(
  key: string,
  userId: string
): Promise<boolean> {
  const config = await featureFlagService.getFlagConfig(key);
  
  if (!config || !config.enabled || !config.rolloutPercentage) {
    return false;
  }

  const hash = hashUserId(userId);
  const percentage = hash % 100;
  
  return percentage < config.rolloutPercentage;
}

function hashUserId(userId: string): number {
  let hash = 0;
  for (let i = 0; i < userId.length; i++) {
    const char = userId.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  return Math.abs(hash);
}

// Usage
const featureEnabled = await useGradualRollout('new-feature', 'user123');
```

---

## Targeting Rules

```typescript
// src/flags/targeting-rules.ts
interface TargetingRule {
  id: string;
  name: string;
  conditions: Condition[];
  rolloutPercentage?: number;
}

interface Condition {
  attribute: string;
  operator: 'equals' | 'notEquals' | 'contains' | 'notContains' | 'in' | 'notIn' | 'greaterThan' | 'lessThan';
  value: any;
}

export class TargetingRuleEngine {
  evaluate(rules: TargetingRule[], context: Record<string, any>): boolean {
    for (const rule of rules) {
      if (this.evaluateRule(rule, context)) {
        return true;
      }
    }
    return false;
  }

  private evaluateRule(rule: TargetingRule, context: Record<string, any>): boolean {
    for (const condition of rule.conditions) {
      if (!this.evaluateCondition(condition, context)) {
        return false;
      }
    }
    return true;
  }

  private evaluateCondition(condition: Condition, context: Record<string, any>): boolean {
    const value = context[condition.attribute];

    switch (condition.operator) {
      case 'equals':
        return value === condition.value;
      case 'notEquals':
        return value !== condition.value;
      case 'contains':
        return typeof value === 'string' && value.includes(condition.value);
      case 'notContains':
        return typeof value === 'string' && !value.includes(condition.value);
      case 'in':
        return Array.isArray(condition.value) && condition.value.includes(value);
      case 'notIn':
        return Array.isArray(condition.value) && !condition.value.includes(value);
      case 'greaterThan':
        return typeof value === 'number' && value > condition.value;
      case 'lessThan':
        return typeof value === 'number' && value < condition.value;
      default:
        return false;
    }
  }
}

// Usage
const rules: TargetingRule[] = [
  {
    id: '1',
    name: 'Premium Users',
    conditions: [
      { attribute: 'plan', operator: 'equals', value: 'premium' },
    ],
    rolloutPercentage: 100,
  },
  {
    id: '2',
    name: 'US Users',
    conditions: [
      { attribute: 'country', operator: 'equals', value: 'US' },
    ],
    rolloutPercentage: 50,
  },
];

const engine = new TargetingRuleEngine();
const enabled = engine.evaluate(rules, { plan: 'premium', country: 'US', userId: '123' });
```

---

## A/B Testing

```typescript
// src/flags/ab-testing.ts
interface ABTestVariant {
  name: string;
  weight: number;
  config: Record<string, any>;
}

interface ABTest {
  key: string;
  variants: ABTestVariant[];
  startDate: Date;
  endDate?: Date;
}

export class ABTestService {
  private tests: Map<string, ABTest> = new Map();

  registerTest(test: ABTest): void {
    this.tests.set(test.key, test);
  }

  async getVariant(key: string, userId: string): Promise<ABTestVariant | null> {
    const test = this.tests.get(key);
    
    if (!test) {
      return null;
    }

    // Check if test is active
    const now = new Date();
    if (now < test.startDate || (test.endDate && now > test.endDate)) {
      return null;
    }

    // Assign variant based on user ID
    const hash = this.hashUserId(userId);
    const totalWeight = test.variants.reduce((sum, v) => sum + v.weight, 0);
    const random = (hash % totalWeight) / totalWeight;
    
    let cumulativeWeight = 0;
    for (const variant of test.variants) {
      cumulativeWeight += variant.weight;
      if (random < cumulativeWeight / totalWeight) {
        return variant;
      }
    }

    return test.variants[0];
  }

  private hashUserId(userId: string): number {
    let hash = 0;
    for (let i = 0; i < userId.length; i++) {
      const char = userId.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }
    return Math.abs(hash);
  }
}

export const abTestService = new ABTestService();

// Register A/B test
abTestService.registerTest({
  key: 'checkout-flow',
  variants: [
    {
      name: 'control',
      weight: 50,
      config: { showNewCheckout: false },
    },
    {
      name: 'variant-a',
      weight: 25,
      config: { showNewCheckout: true, step1: 'address' },
    },
    {
      name: 'variant-b',
      weight: 25,
      config: { showNewCheckout: true, step1: 'payment' },
    },
  ],
  startDate: new Date('2024-01-01'),
  endDate: new Date('2024-03-01'),
});

// Usage
const variant = await abTestService.getVariant('checkout-flow', 'user123');
if (variant) {
  console.log(`User ${userId} is in variant: ${variant.name}`);
  console.log('Config:', variant.config);
}
```

---

## Flag Lifecycle

```typescript
// src/flags/flag-lifecycle.ts
export enum FlagStatus {
  DRAFT = 'draft',
  ACTIVE = 'active',
  DEPRECATED = 'deprecated',
  REMOVED = 'removed',
}

interface FlagLifecycleConfig {
  key: string;
  status: FlagStatus;
  createdAt: Date;
  activatedAt?: Date;
  deprecatedAt?: Date;
  removedAt?: Date;
  owner: string;
  description: string;
}

export class FlagLifecycleManager {
  private flags: Map<string, FlagLifecycleConfig> = new Map();

  createFlag(key: string, owner: string, description: string): FlagLifecycleConfig {
    const config: FlagLifecycleConfig = {
      key,
      status: FlagStatus.DRAFT,
      createdAt: new Date(),
      owner,
      description,
    };
    
    this.flags.set(key, config);
    return config;
  }

  activateFlag(key: string): FlagLifecycleConfig {
    const config = this.flags.get(key);
    
    if (!config) {
      throw new Error(`Flag ${key} not found`);
    }

    if (config.status !== FlagStatus.DRAFT) {
      throw new Error(`Flag ${key} is not in draft status`);
    }

    config.status = FlagStatus.ACTIVE;
    config.activatedAt = new Date();
    
    return config;
  }

  deprecateFlag(key: string): FlagLifecycleConfig {
    const config = this.flags.get(key);
    
    if (!config) {
      throw new Error(`Flag ${key} not found`);
    }

    if (config.status !== FlagStatus.ACTIVE) {
      throw new Error(`Flag ${key} is not active`);
    }

    config.status = FlagStatus.DEPRECATED;
    config.deprecatedAt = new Date();
    
    return config;
  }

  removeFlag(key: string): FlagLifecycleConfig {
    const config = this.flags.get(key);
    
    if (!config) {
      throw new Error(`Flag ${key} not found`);
    }

    if (config.status !== FlagStatus.DEPRECATED) {
      throw new Error(`Flag ${key} must be deprecated before removal`);
    }

    config.status = FlagStatus.REMOVED;
    config.removedAt = new Date();
    
    // Remove flag after a grace period
    setTimeout(() => {
      this.flags.delete(key);
    }, 30 * 24 * 60 * 60 * 1000); // 30 days
    
    return config;
  }

  getFlag(key: string): FlagLifecycleConfig | undefined {
    return this.flags.get(key);
  }

  getAllFlags(): FlagLifecycleConfig[] {
    return Array.from(this.flags.values());
  }
}

export const flagLifecycleManager = new FlagLifecycleManager();
```

---

## Technical Debt Management

```typescript
// src/flags/technical-debt.ts
interface FlagTechnicalDebt {
  key: string;
  age: number; // days
  usage: number; // number of evaluations
  complexity: number; // 1-10 scale
  lastUpdated: Date;
  owner: string;
}

export class TechnicalDebtTracker {
  private flags: Map<string, FlagTechnicalDebt> = new Map();

  trackFlagEvaluation(key: string): void {
    const flag = this.flags.get(key);
    
    if (flag) {
      flag.usage++;
    }
  }

  calculateDebtScore(key: string): number {
    const flag = this.flags.get(key);
    
    if (!flag) {
      return 0;
    }

    // Higher score = more technical debt
    const ageScore = Math.min(flag.age / 365, 1) * 30; // Max 30 points
    const usageScore = Math.min(flag.usage / 1000000, 1) * 20; // Max 20 points
    const complexityScore = flag.complexity * 5; // Max 50 points
    
    return ageScore + usageScore + complexityScore;
  }

  getFlagsNeedingCleanup(threshold: number = 50): FlagTechnicalDebt[] {
    return Array.from(this.flags.values())
      .filter(flag => this.calculateDebtScore(flag.key) >= threshold)
      .sort((a, b) => this.calculateDebtScore(b.key) - this.calculateDebtScore(a.key));
  }

  generateReport(): string {
    const flags = Array.from(this.flags.values());
    const totalDebt = flags.reduce((sum, flag) => sum + this.calculateDebtScore(flag.key), 0);
    const highDebtFlags = this.getFlagsNeedingCleanup(70);

    return `
Feature Flag Technical Debt Report
================================

Total Flags: ${flags.length}
Total Debt Score: ${totalDebt}
Average Debt Score: ${totalDebt / flags.length}

High Debt Flags (Score >= 70):
${highDebtFlags.map(flag => `- ${flag.key}: ${this.calculateDebtScore(flag.key)} (Owner: ${flag.owner})`).join('\n')}

Recommendations:
${this.generateRecommendations()}
    `;
  }

  private generateRecommendations(): string {
    const highDebtFlags = this.getFlagsNeedingCleanup(70);
    
    if (highDebtFlags.length === 0) {
      return 'No immediate action required.';
    }

    return highDebtFlags.map(flag => {
      const score = this.calculateDebtScore(flag.key);
      if (score >= 90) {
        return `- ${flag.key}: Remove immediately (Score: ${score})`;
      } else if (score >= 70) {
        return `- ${flag.key}: Plan removal within 30 days (Score: ${score})`;
      }
      return '';
    }).filter(Boolean).join('\n');
  }
}

export const technicalDebtTracker = new TechnicalDebtTracker();
```

---

## Best Practices

### 1. Use Descriptive Flag Names

```typescript
// Good: Descriptive flag names
const FEATURE_NEW_DASHBOARD = 'new-dashboard';
const FEATURE_DARK_MODE = 'dark-mode';
const FEATURE_BETA_API = 'beta-api';

// Bad: Vague flag names
const FEATURE_FLAG_1 = 'flag1';
const FEATURE_FLAG_2 = 'flag2';
```

### 2. Set Default Values

```typescript
// Good: Set default values
const enabled = await featureFlagService.isEnabled('new-feature', { userId: '123' }, false);

// Bad: No default value
const enabled = await featureFlagService.isEnabled('new-feature', { userId: '123' });
```

### 3. Clean Up Old Flags

```typescript
// Good: Clean up old flags
const flagsNeedingCleanup = technicalDebtTracker.getFlagsNeedingCleanup(70);
flagsNeedingCleanup.forEach(flag => {
  console.log(`Flag ${flag.key} needs cleanup`);
  // Plan removal
});

// Bad: Never clean up
// Flags accumulate indefinitely
```

### 4. Use Gradual Rollout

```typescript
// Good: Gradual rollout
await featureFlagService.setFlag({
  key: 'new-feature',
  enabled: true,
  rolloutPercentage: 10, // Start with 10%
});

// Later increase to 50%
await featureFlagService.setFlag({
  key: 'new-feature',
  enabled: true,
  rolloutPercentage: 50,
});

// Bad: Immediate 100% rollout
await featureFlagService.setFlag({
  key: 'new-feature',
  enabled: true,
  rolloutPercentage: 100,
});
```

### 5. Monitor Flag Usage

```typescript
// Good: Monitor flag usage
technicalDebtTracker.trackFlagEvaluation('new-feature');

// Generate report
console.log(technicalDebtTracker.generateReport());

// Bad: No monitoring
// No tracking of flag usage
```

---

## Summary

This skill covers comprehensive feature flag implementation patterns including:

- **Feature Flag Concepts**: Why feature flags, flag types
- **Implementation Approaches**: Simple boolean flags, database-backed flags
- **Libraries**: LaunchDarkly, Unleash, custom Redis solution
- **Flag Types**: Boolean, multivariate, gradual rollout
- **Targeting Rules**: Rule engine, condition evaluation
- **A/B Testing**: Variant assignment, test management
- **Flag Lifecycle**: Draft, active, deprecated, removed states
- **Technical Debt Management**: Debt tracking, cleanup recommendations
- **Best Practices**: Descriptive names, default values, cleanup, gradual rollout, monitoring
