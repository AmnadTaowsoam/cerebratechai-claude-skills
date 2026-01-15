# Feature Flags

A comprehensive guide to feature flag implementation.

## Table of Contents

1. [Feature Flag Concepts](#feature-flag-concepts)
2. [Implementation Approaches](#implementation-approaches)
3. [Libraries](#libraries)
4. [Flag Types](#flag-types)
5. [Targeting Rules](#targeting-rules)
6. [A/B Testing](#ab-testing)
7. [Flag Lifecycle](#flag-lifecycle)
8. [Technical Debt Management](#technical-debt-management)
9. [Best Practices](#best-practices)

---

## Feature Flag Concepts

### What are Feature Flags?

Feature flags (also known as feature toggles) allow you to enable or disable features without deploying new code.

```
┌─────────────────────────────────────────────────────┐
│              Feature Flag Workflow                    │
├─────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐      │
│  │   Deploy    │──>│   Enable    │──>│   Monitor   │      │
│  │  (No Flag) │  │  (With Flag)│  │  (Metrics)  │      │
│  └─────────────┘  └─────────────┘  └─────────────┘      │
│                                                             │
│  Benefits:                                                  │
│  - Deploy without releasing features                    │
│  - Rollback instantly                                   │
│  - Test in production with subset of users            │
│  - Gradual rollout                                     │
└─────────────────────────────────────────────────────┘
```

### Key Concepts

| Concept | Description |
|---------|-------------|
| **Feature Flag** | A toggle that enables/disables functionality |
| **Rollout** | The process of gradually enabling a feature |
| **Targeting** | Rules that determine which users see a feature |
| **A/B Testing** | Comparing two versions of a feature |
| **Canary Release** | Testing with a small subset of users |
| **Kill Switch** | Emergency disable of a problematic feature |

---

## Implementation Approaches

### Simple Configuration File

```typescript
// config/features.ts
export const features = {
  newDashboard: true,
  darkMode: true,
  betaAPI: false,
  experimentalFeature: false,
};
```

```typescript
// Usage
import { features } from '../config/features';

if (features.newDashboard) {
  // Show new dashboard
}
```

### Database-Backed Flags

```typescript
// models/FeatureFlag.ts
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class FeatureFlag {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  name: string;

  @Column()
  enabled: boolean;

  @Column()
  rolloutPercentage: number;

  @Column({ type: 'json', nullable: true })
  targetingRules: Record<string, any>;
}
```

```typescript
// services/featureFlag.service.ts
import { Repository } from 'typeorm';
import { FeatureFlag } from '../models/FeatureFlag';

export class FeatureFlagService {
  constructor(
    private repository: Repository<FeatureFlag>,
  ) {}

  async isFeatureEnabled(featureName: string, userId?: string): Promise<boolean> {
    const flag = await this.repository.findOne({ where: { name: featureName } });

    if (!flag) {
      return false;
    }

    if (!flag.enabled) {
      return false;
    }

    if (userId && flag.targetingRules) {
      const user = await this.getUser(userId);
      return this.matchesTargeting(user, flag.targetingRules);
    }

    return true;
  }

  private matchesTargeting(user: any, rules: Record<string, any>): boolean {
    // Implement targeting logic
    return true;
  }

  async getUser(userId: string): Promise<any> {
    // Fetch user data
    return { id: userId, tier: 'free' };
  }
}
```

### Redis-Backed Flags

```typescript
// services/featureFlag.service.ts
import { createClient } from 'redis';

const redis = createClient();

export class FeatureFlagService {
  async isFeatureEnabled(featureName: string, userId?: string): Promise<boolean> {
    const key = `feature:${featureName}`;
    const enabled = await redis.get(key);

    if (enabled === null) {
      return false; // Default to disabled
    }

    return enabled === 'true';
  }

  async setFeatureEnabled(featureName: string, enabled: boolean): Promise<void> {
    const key = `feature:${featureName}`;
    await redis.set(key, enabled ? 'true' : 'false');
    await redis.expire(key, 3600); // 1 hour TTL
  }

  async getRolloutPercentage(featureName: string): Promise<number> {
    const key = `feature:${featureName}:rollout`;
    const percentage = await redis.get(key);
    return percentage ? parseFloat(percentage) : 0;
  }

  async setRolloutPercentage(featureName: string, percentage: number): Promise<void> {
    const key = `feature:${featureName}:rollout`;
    await redis.set(key, percentage.toString());
    await redis.expire(key, 3600); // 1 hour TTL
  }
}
```

---

## Libraries

### LaunchDarkly

```typescript
// services/launchDarkly.service.ts
import * as LaunchDarkly from 'launchdarkly-node-server-sdk';

const client = new LaunchDarkly({
  sdkKey: process.env.LAUNCHDARKLY_SDK_KEY,
});

export class FeatureFlagService {
  async isFeatureEnabled(featureName: string, userId?: string): Promise<boolean> {
    const context = userId ? { key: userId } : {};

    const flag = await client.variation(featureName, context);

    return flag.value === true;
  }

  async getFeatureConfig(featureName: string): Promise<any> {
    const flag = await client.variation(featureName);

    return {
      enabled: flag.value,
      variation: flag.variationKey,
      config: flag.config,
    };
  }
}
```

```python
# services/launchdarkly_service.py
import ldclient

client = ldclient.Client(
    sdk_key=os.environ.get('LAUNCHDARKLY_SDK_KEY')
)

class FeatureFlagService:
    @staticmethod
    def is_feature_enabled(feature_name: str, user_id: str = None) -> bool:
        context = {'key': user_id} if user_id else {}
        flag = client.variation(feature_name, context)
        return flag.value is True

    @staticmethod
    def get_feature_config(feature_name: str) -> dict:
        flag = client.variation(feature_name)
        return {
            'enabled': flag.value,
            'variation': flag.variation_key,
            'config': flag.config,
        }
```

### Unleash

```typescript
// services/unleash.service.ts
import { unleash } from 'unleash-client-node';

const unleash = unleash({
  url: process.env.UNLEASH_URL,
  appName: 'myapp',
  instanceId: process.env.UNLEASH_INSTANCE_ID,
});

export class FeatureFlagService {
  async isFeatureEnabled(featureName: string): Promise<boolean> {
    const isEnabled = await unleash.isEnabled(featureName);
    return isEnabled;
  }

  async getFeatureConfig(featureName: string): Promise<any> {
    const variant = await unleash.getVariant(featureName);
    return variant;
  }
}
```

```python
# services/unleash_service.py
from unleash_client import UnleashClient

client = UnleashClient(
    url=os.environ.get('UNLEASH_URL'),
    app_name='myapp',
    instance_id=os.environ.get('UNLEASH_INSTANCE_ID')
)

class FeatureFlagService:
    @staticmethod
    def is_feature_enabled(feature_name: str) -> bool:
        return client.is_enabled(feature_name)

    @staticmethod
    def get_feature_config(feature_name: str) -> dict:
        variant = client.get_variant(feature_name)
        return {
            'enabled': variant.enabled,
            'name': variant.name,
            'payload': variant.payload,
        }
```

### Custom Solution

```typescript
// services/featureFlag.service.ts
export class FeatureFlagService {
  private flags: Map<string, FeatureFlagConfig>;

  constructor() {
    this.flags = new Map();
    this.loadFlags();
  }

  private loadFlags(): void {
    // Load from config or API
    this.flags.set('newDashboard', {
      enabled: true,
      rolloutPercentage: 100,
      targetingRules: {},
    });

    this.flags.set('betaAPI', {
      enabled: false,
      rolloutPercentage: 0,
      targetingRules: {},
    });
  }

  async isFeatureEnabled(featureName: string, userId?: string): Promise<boolean> {
    const flag = this.flags.get(featureName);

    if (!flag || !flag.enabled) {
      return false;
    }

    if (userId && flag.targetingRules) {
      const user = await this.getUser(userId);
      return this.matchesTargeting(user, flag.targetingRules);
    }

    if (flag.rolloutPercentage < 100) {
      const hash = this.hashUserId(userId);
      return (hash % 100) < flag.rolloutPercentage;
    }

    return true;
  }

  private hashUserId(userId: string): number {
    // Simple hash function
    let hash = 0;
    for (let i = 0; i < userId.length; i++) {
      hash = ((hash << 5) - hash) + userId.charCodeAt(i);
      hash = hash & hash;
    }
    return Math.abs(hash);
  }

  private async getUser(userId: string): Promise<any> {
    // Fetch user data
    return { id: userId, tier: 'free' };
  }

  private matchesTargeting(user: any, rules: Record<string, any>): boolean {
    // Implement targeting logic
    return true;
  }
}

interface FeatureFlagConfig {
  enabled: boolean;
  rolloutPercentage: number;
  targetingRules?: Record<string, any>;
}
```

---

## Flag Types

### Boolean Flags

```typescript
// Boolean flag - simple on/off
export const features = {
  newDashboard: {
    type: 'boolean',
    enabled: true,
    description: 'Enable new dashboard UI',
  },
};
```

### Multivariate Flags

```typescript
// Multivariate flag - multiple variations
export const features = {
  buttonColor: {
    type: 'multivariate',
    enabled: true,
    variations: [
      { value: 'blue', weight: 50 },
      { value: 'green', weight: 30 },
      { value: 'red', weight: 20 },
    ],
    description: 'Button color A/B test',
  },
};
```

### Percentage Rollout

```typescript
// Percentage rollout - gradual enablement
export const features = {
  betaAPI: {
    type: 'percentage',
    enabled: true,
    rolloutPercentage: 10, // Start at 10%
    description: 'Beta API rollout',
  },
};
```

---

## Targeting Rules

### User-Based Targeting

```typescript
// Target specific users
export const features = {
  betaFeature: {
    enabled: true,
    targetingRules: {
      userIds: ['user1', 'user2', 'user3'], // Specific users
    },
    description: 'Beta feature for specific users',
  },
};
```

### Tier-Based Targeting

```typescript
// Target by user tier
export const features = {
  premiumFeature: {
    enabled: true,
    targetingRules: {
      tiers: ['premium', 'enterprise'], // Premium and enterprise users
    },
    description: 'Premium feature for paid users',
  },
};
```

### Geography-Based Targeting

```typescript
// Target by location
export const features = features = {
  regionSpecificFeature: {
    enabled: true,
    targetingRules: {
      countries: ['US', 'CA', 'GB'], // Specific countries
    },
    description: 'Feature for specific regions',
  },
};
```

### Time-Based Targeting

```typescript
// Target by time
export const features = {
  scheduledFeature: {
    enabled: true,
    targetingRules: {
      startDate: '2024-01-01T00:00:00Z',
      endDate: '2024-12-31T23:59:59Z',
    },
    description: 'Feature available during specific time period',
  },
};
```

---

## A/B Testing

### Simple A/B Test

```typescript
// A/B test configuration
export const features = {
  checkoutFlow: {
    type: 'multivariate',
    enabled: true,
    variations: [
      { value: 'v1', weight: 50, description: 'Original checkout flow' },
      { value: 'v2', weight: 50, description: 'New checkout flow' },
    ],
    description: 'Checkout flow A/B test',
  },
};
```

```typescript
// Usage
import { FeatureFlagService } from '../services/featureFlag.service';

async function handleCheckout(userId: string) {
  const flag = await featureFlagService.getFeatureConfig('checkoutFlow');

  if (flag.variation === 'v1') {
    // Use v1 checkout flow
    return await processCheckoutV1();
  } else {
    // Use v2 checkout flow
    return await processCheckoutV2();
  }
}
```

### Multi-Variate Test

```typescript
// Multi-variate test configuration
export const features = {
  homepageLayout: {
    type: 'multivariate',
    enabled: true,
    variations: [
      { value: 'layout-a', weight: 40, config: { columns: 3 } },
      { value: 'layout-b', weight: 40, config: { columns: 2 } },
      { value: 'layout-c', weight: 20, config: { columns: 4 } },
    ],
    description: 'Homepage layout test',
  },
};
```

---

## Flag Lifecycle

### Creating a Flag

```typescript
// Create new feature flag
export const features = {
  newFeature: {
    type: 'boolean',
    enabled: false, // Start disabled
    description: 'New feature under development',
    createdAt: '2024-01-01',
  },
};
```

### Gradual Rollout

```typescript
// Gradually enable feature
async function rolloutFeature(featureName: string) {
  const percentages = [10, 25, 50, 75, 100];

  for (const percentage of percentages) {
    await setRolloutPercentage(featureName, percentage);
    await sleep(24 * 60 * 60 * 1000); // Wait 24 hours
  }
}

async function setRolloutPercentage(featureName: string, percentage: number): Promise<void> {
  // Update rollout percentage
  const flag = features[featureName];
  flag.rolloutPercentage = percentage;

  // Save to database/Redis
  await saveFlag(featureName, flag);
}
```

### Killing a Flag

```typescript
// Emergency disable of feature
async function killFeature(featureName: string): Promise<void> {
  const flag = features[featureName];
  flag.enabled = false;

  // Save to database/Redis
  await saveFlag(featureName, flag);

  // Notify team
  await notifyTeam(`Feature ${featureName} has been killed`);
}
```

### Sunsetting a Flag

```typescript
// Deprecate and remove flag
async function sunsetFeature(featureName: string): Promise<void> {
  const flag = features[featureName];
  flag.enabled = false;
  flag.sunsetDate = new Date();

  // Save to database/Redis
  await saveFlag(featureName, flag);

  // Remove code after sunset
  await removeFeatureCode(featureName);
}
```

---

## Technical Debt Management

### Tracking Feature Flags

```typescript
// Track feature flags for cleanup
interface FeatureFlag {
  name: string;
  createdAt: Date;
  enabled: boolean;
  sunsetDate?: Date;
}

const activeFlags: FeatureFlag[] = [
  {
    name: 'newDashboard',
    createdAt: new Date('2024-01-01'),
    enabled: true,
  },
  {
    name: 'oldDashboard',
    createdAt: new Date('2023-01-01'),
    enabled: false,
    sunsetDate: new Date('2024-01-01'),
  },
];

// Schedule cleanup
async function cleanupOldFlags(): Promise<void> {
  const now = new Date();
  const sixMonthsAgo = new Date(now.getTime() - 6 * 30 * 24 * 60 * 60 * 1000);

  for (const flag of activeFlags) {
    if (flag.sunsetDate && flag.sunsetDate < sixMonthsAgo) {
      // Remove flag code
      await removeFeatureCode(flag.name);
    }
  }
}
```

### Documentation

```markdown
# Feature Flags Documentation

## Active Flags

### newDashboard
- **Status**: Enabled
- **Rollout**: 100%
- **Description**: New dashboard UI
- **Created**: 2024-01-01

### betaAPI
- **Status**: Enabled
- **Rollout**: 25%
- **Description**: Beta API for testing
- **Created**: 2024-01-15

## Deprecated Flags

### oldDashboard
- **Status**: Disabled
- **Sunset**: 2024-01-01
- **Description**: Old dashboard UI
- **Migration Guide**: See /docs/dashboard-migration.md
```

---

## Best Practices

### 1. Use Feature Flags for Risky Changes

```typescript
// Use flags for risky changes
export const features = {
  riskyChange: {
    enabled: false,
    description: 'Risky change - start with 0% rollout',
  },
};
```

### 2. Keep Flags Temporary

```typescript
// Set sunset date for temporary flags
export const features = {
  temporaryFeature: {
    enabled: true,
  sunsetDate: new Date('2024-06-01'), // Sunset in 6 months
    description: 'Temporary feature for campaign',
  },
};
```

### 3. Monitor Flag Performance

```typescript
// Monitor flag performance
async function monitorFlagPerformance(featureName: string): Promise<void> {
  const enabledUsers = await getEnabledUserCount(featureName);
  const metrics = await getMetrics(featureName);

  console.log(`Feature ${featureName}:`, {
    enabledUsers,
    metrics,
  });
}
```

### 4. Document Flag Purpose

```typescript
// Document flag purpose and owner
export const features = {
  newFeature: {
    enabled: true,
    owner: 'team-name',
    description: 'New feature for improving user experience',
    jira: 'PROJ-123',
  },
};
```

### 5. Test Flags Before Rollout

```typescript
// Test flags before enabling
describe('Feature Flags', () => {
  it('should be disabled by default', async () => {
    const enabled = await featureFlagService.isFeatureEnabled('newFeature');
    expect(enabled).toBe(false);
  });

  it('should be enabled for test users', async () => {
    const enabled = await featureFlagService.isFeatureEnabled('newFeature', 'test-user-1');
    expect(enabled).toBe(true);
  });
});
```

### 6. Use Consistent Naming

```typescript
// Use consistent naming convention
export const features = {
  // Feature name: kebab-case
  newFeature: {
    enabled: true,
    description: 'New feature',
  },

  // Variation names: descriptive
  buttonColor: {
    variations: [
      { value: 'blue', description: 'Blue button' },
      { value: 'green', description: 'Green button' },
    ],
  },
};
```

### 7. Set Rollout Targets

```typescript
// Set clear rollout targets
export const rolloutSchedule = {
  betaAPI: {
    week1: 10,   // 10% of users
    week2: 25,   // 25% of users
    week3: 50,   // 50% of users
    week4: 75,   // 75% of users
    week5: 100,  // 100% of users
  },
};
```

### 8. Use Feature Flags for Experiments

```typescript
// Use flags for experiments
export const features = {
  experimentA: {
    type: 'multivariate',
    enabled: true,
    variations: [
      { value: 'control', weight: 50 },
      { value: 'variant1', weight: 25 },
      { value: 'variant2', weight: 25 },
    ],
    description: 'Experiment A',
  },
};
```

### 9. Monitor Flag Usage

```typescript
// Track flag usage
async function trackFlagUsage(featureName: string, userId: string): Promise<void> {
  await analytics.track('feature_flag_used', {
    feature: featureName,
    userId,
    timestamp: new Date(),
  });
}
```

### 10. Clean Up Old Flags

```typescript
// Clean up old flags
async function cleanupOldFlags(): Promise<void> {
  const flags = await getAllFlags();

  for (const flag of flags) {
    if (flag.createdAt < oneYearAgo && !flag.enabled) {
      await deleteFlag(flag.name);
    }
  }
}
```

---

## Resources

- [LaunchDarkly Documentation](https://docs.launchdarkly.com/)
- [Unleash Documentation](https://docs.unleash.io/)
- [Feature Flag Best Practices](https://martinfowler.com/articles/feature-flags/)
- [Progressive Delivery](https://martinfowler.com/articles/progressive-delivery/)
