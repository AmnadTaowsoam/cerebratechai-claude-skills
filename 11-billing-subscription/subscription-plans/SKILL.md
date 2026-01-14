# Subscription Plans

## Overview

Comprehensive guide to subscription plan management and design patterns.

## Table of Contents

1. [Plan Design Patterns](#plan-design-patterns)
2. [Database Schema](#database-schema)
3. [Plan Features Management](#plan-features-management)
4. [Plan Upgrades/Downgrades](#plan-upgradesdowngrades)
5. [Prorations](#prorations)
6. [Trial Periods](#trial-periods)
7. [Cancellation Handling](#cancellation-handling)
8. [Plan Comparison UI](#plan-comparison-ui)
9. [Feature Flags per Plan](#feature-flags-per-plan)
10. [Migration Strategies](#migration-strategies)
11. [Best Practices](#best-practices)

---

## Plan Design Patterns

### Tiered Pricing

```typescript
// tiered-pricing.ts
export interface TieredPricing {
  name: string;
  price: number;
  currency: string;
  interval: 'monthly' | 'yearly';
  features: string[];
  limits: {
    users: number;
    storage: number; // in GB
    apiCalls: number;
  };
  popular?: boolean;
}

export const tieredPlans: TieredPricing[] = [
  {
    name: 'Starter',
    price: 9.99,
    currency: 'USD',
    interval: 'monthly',
    features: [
      '5 users',
      '10 GB storage',
      '10,000 API calls/month',
      'Email support'
    ],
    limits: {
      users: 5,
      storage: 10,
      apiCalls: 10000
    }
  },
  {
    name: 'Professional',
    price: 29.99,
    currency: 'USD',
    interval: 'monthly',
    features: [
      '25 users',
      '100 GB storage',
      '100,000 API calls/month',
      'Priority email support',
      'Advanced analytics'
    ],
    limits: {
      users: 25,
      storage: 100,
      apiCalls: 100000
    },
    popular: true
  },
  {
    name: 'Enterprise',
    price: 99.99,
    currency: 'USD',
    interval: 'monthly',
    features: [
      'Unlimited users',
      'Unlimited storage',
      'Unlimited API calls',
      '24/7 phone support',
      'Custom integrations',
      'Dedicated account manager'
    ],
    limits: {
      users: Infinity,
      storage: Infinity,
      apiCalls: Infinity
    }
  }
];
```

### Per-Seat Pricing

```typescript
// per-seat-pricing.ts
export interface PerSeatPricing {
  name: string;
  basePrice: number;
  seatPrice: number;
  currency: string;
  interval: 'monthly' | 'yearly';
  includedSeats: number;
  features: string[];
  limits: {
    storage: number;
    apiCalls: number;
  };
}

export const perSeatPlans: PerSeatPricing[] = [
  {
    name: 'Team',
    basePrice: 19.99,
    seatPrice: 9.99,
    currency: 'USD',
    interval: 'monthly',
    includedSeats: 5,
    features: [
      '5 included seats',
      '50 GB storage',
      '50,000 API calls/month',
      'Email support'
    ],
    limits: {
      storage: 50,
      apiCalls: 50000
    }
  },
  {
    name: 'Business',
    basePrice: 49.99,
    seatPrice: 7.99,
    currency: 'USD',
    interval: 'monthly',
    includedSeats: 10,
    features: [
      '10 included seats',
      '500 GB storage',
      '500,000 API calls/month',
      'Priority support',
      'Advanced analytics'
    ],
    limits: {
      storage: 500,
      apiCalls: 500000
    }
  }
];

export function calculatePerSeatPrice(
  plan: PerSeatPricing,
  seats: number
): number {
  if (seats <= plan.includedSeats) {
    return plan.basePrice;
  }
  
  const additionalSeats = seats - plan.includedSeats;
  return plan.basePrice + (additionalSeats * plan.seatPrice);
}
```

### Usage-Based Pricing

```typescript
// usage-based-pricing.ts
export interface UsageTier {
  from: number;
  to?: number;
  price: number;
}

export interface UsageBasedPricing {
  name: string;
  currency: string;
  interval: 'monthly' | 'yearly';
  metric: string;
  tiers: UsageTier[];
  basePrice?: number;
}

export const usageBasedPlans: UsageBasedPricing[] = [
  {
    name: 'API Usage',
    currency: 'USD',
    interval: 'monthly',
    metric: 'api_calls',
    basePrice: 0,
    tiers: [
      { from: 0, to: 10000, price: 0 }, // Free tier
      { from: 10001, to: 100000, price: 0.001 }, // $0.001 per call
      { from: 100001, to: 1000000, price: 0.0005 }, // $0.0005 per call
      { from: 1000001, price: 0.0002 } // $0.0002 per call
    ]
  },
  {
    name: 'Storage',
    currency: 'USD',
    interval: 'monthly',
    metric: 'storage_gb',
    basePrice: 0,
    tiers: [
      { from: 0, to: 10, price: 0 }, // Free 10 GB
      { from: 11, to: 100, price: 0.10 }, // $0.10 per GB
      { from: 101, to: 1000, price: 0.05 }, // $0.05 per GB
      { from: 1001, price: 0.02 } // $0.02 per GB
    ]
  }
];

export function calculateUsagePrice(
  plan: UsageBasedPricing,
  usage: number
): number {
  let total = plan.basePrice || 0;
  let remainingUsage = usage;
  
  for (const tier of plan.tiers) {
    if (remainingUsage <= 0) break;
    
    const tierStart = tier.from;
    const tierEnd = tier.to || Infinity;
    const tierSize = tierEnd - tierStart + 1;
    const usageInTier = Math.min(remainingUsage, tierSize);
    
    total += usageInTier * tier.price;
    remainingUsage -= usageInTier;
  }
  
  return total;
}
```

### Hybrid Pricing

```typescript
// hybrid-pricing.ts
export interface HybridPricing {
  name: string;
  basePrice: number;
  currency: string;
  interval: 'monthly' | 'yearly';
  included: {
    users: number;
    storage: number;
    apiCalls: number;
  };
  overage: {
    users: number;
    storage: number;
    apiCalls: number;
  };
  features: string[];
}

export const hybridPlans: HybridPricing[] = [
  {
    name: 'Standard',
    basePrice: 49.99,
    currency: 'USD',
    interval: 'monthly',
    included: {
      users: 10,
      storage: 100,
      apiCalls: 100000
    },
    overage: {
      users: 5,
      storage: 0.50,
      apiCalls: 0.0005
    },
    features: [
      '10 included users',
      '100 GB storage',
      '100,000 API calls/month',
      'Email support'
    ]
  }
];

export function calculateHybridPrice(
  plan: HybridPricing,
  usage: {
    users: number;
    storage: number;
    apiCalls: number;
  }
): number {
  let total = plan.basePrice;
  
  // Calculate user overage
  const userOverage = Math.max(0, usage.users - plan.included.users);
  total += userOverage * plan.overage.users;
  
  // Calculate storage overage
  const storageOverage = Math.max(0, usage.storage - plan.included.storage);
  total += storageOverage * plan.overage.storage;
  
  // Calculate API call overage
  const apiOverage = Math.max(0, usage.apiCalls - plan.included.apiCalls);
  total += apiOverage * plan.overage.apiCalls;
  
  return total;
}
```

---

## Database Schema

### PostgreSQL Schema

```sql
-- subscription-plans-schema.sql

-- Plans table
CREATE TABLE plans (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  description TEXT,
  price DECIMAL(10, 2) NOT NULL,
  currency VARCHAR(3) DEFAULT 'USD',
  interval VARCHAR(20) NOT NULL CHECK (interval IN ('monthly', 'yearly', 'weekly')),
  stripe_price_id VARCHAR(255),
  features JSONB DEFAULT '[]',
  limits JSONB NOT NULL,
  is_active BOOLEAN DEFAULT true,
  is_public BOOLEAN DEFAULT true,
  sort_order INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Plan features table
CREATE TABLE plan_features (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  plan_id UUID NOT NULL REFERENCES plans(id) ON DELETE CASCADE,
  feature_key VARCHAR(255) NOT NULL,
  feature_name VARCHAR(255) NOT NULL,
  feature_value TEXT,
  is_included BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(plan_id, feature_key)
);

-- Subscriptions table
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  plan_id UUID NOT NULL REFERENCES plans(id) ON DELETE RESTRICT,
  stripe_subscription_id VARCHAR(255) UNIQUE,
  stripe_customer_id VARCHAR(255),
  status VARCHAR(50) NOT NULL CHECK (status IN ('active', 'past_due', 'canceled', 'unpaid', 'trialing')),
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  trial_start TIMESTAMP,
  trial_end TIMESTAMP,
  cancel_at_period_end BOOLEAN DEFAULT false,
  canceled_at TIMESTAMP,
  quantity INTEGER DEFAULT 1,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Subscription items table
CREATE TABLE subscription_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subscription_id UUID NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
  plan_id UUID NOT NULL REFERENCES plans(id) ON DELETE RESTRICT,
  stripe_item_id VARCHAR(255),
  quantity INTEGER DEFAULT 1,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Subscription history table
CREATE TABLE subscription_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subscription_id UUID NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
  event_type VARCHAR(50) NOT NULL,
  old_plan_id UUID REFERENCES plans(id),
  new_plan_id UUID REFERENCES plans(id),
  old_status VARCHAR(50),
  new_status VARCHAR(50),
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Usage tracking table
CREATE TABLE usage_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subscription_id UUID NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
  metric VARCHAR(255) NOT NULL,
  quantity INTEGER NOT NULL,
  period_start TIMESTAMP NOT NULL,
  period_end TIMESTAMP NOT NULL,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_plan_id ON subscriptions(plan_id);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_subscriptions_current_period_end ON subscriptions(current_period_end);
CREATE INDEX idx_subscription_items_subscription_id ON subscription_items(subscription_id);
CREATE INDEX idx_usage_records_subscription_id ON usage_records(subscription_id);
CREATE INDEX idx_usage_records_metric ON usage_records(metric);
CREATE INDEX idx_usage_records_period ON usage_records(period_start, period_end);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_plans_updated_at BEFORE UPDATE ON plans
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscriptions_updated_at BEFORE UPDATE ON subscriptions
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_subscription_items_updated_at BEFORE UPDATE ON subscription_items
FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

---

## Plan Features Management

### Feature Management Service

```typescript
// plan-features.ts
import { Pool } from 'pg';

export interface PlanFeature {
  featureKey: string;
  featureName: string;
  featureValue?: string;
  isIncluded: boolean;
}

export class PlanFeaturesService {
  constructor(private pool: Pool) {}
  
  async addFeatureToPlan(
    planId: string,
    feature: PlanFeature
  ): Promise<void> {
    await this.pool.query(
      `INSERT INTO plan_features (plan_id, feature_key, feature_name, feature_value, is_included)
       VALUES ($1, $2, $3, $4, $5)
       ON CONFLICT (plan_id, feature_key)
       DO UPDATE SET feature_name = EXCLUDED.feature_name,
                  feature_value = EXCLUDED.feature_value,
                  is_included = EXCLUDED.is_included`,
      [planId, feature.featureKey, feature.featureName, feature.featureValue, feature.isIncluded]
    );
  }
  
  async removeFeatureFromPlan(planId: string, featureKey: string): Promise<void> {
    await this.pool.query(
      'DELETE FROM plan_features WHERE plan_id = $1 AND feature_key = $2',
      [planId, featureKey]
    );
  }
  
  async getPlanFeatures(planId: string): Promise<PlanFeature[]> {
    const result = await this.pool.query(
      'SELECT * FROM plan_features WHERE plan_id = $1',
      [planId]
    );
    
    return result.rows.map(row => ({
      featureKey: row.feature_key,
      featureName: row.feature_name,
      featureValue: row.feature_value,
      isIncluded: row.is_included
    }));
  }
  
  async checkFeatureAccess(
    userId: string,
    featureKey: string
  ): Promise<boolean> {
    const result = await this.pool.query(
      `SELECT pf.is_included
       FROM subscriptions s
       JOIN plan_features pf ON s.plan_id = pf.plan_id
       WHERE s.user_id = $1 AND pf.feature_key = $2 AND s.status = 'active'
       LIMIT 1`,
      [userId, featureKey]
    );
    
    return result.rows.length > 0 && result.rows[0].is_included;
  }
  
  async getFeatureValue(
    userId: string,
    featureKey: string
  ): Promise<string | null> {
    const result = await this.pool.query(
      `SELECT pf.feature_value
       FROM subscriptions s
       JOIN plan_features pf ON s.plan_id = pf.plan_id
       WHERE s.user_id = $1 AND pf.feature_key = $2 AND s.status = 'active'
       LIMIT 1`,
      [userId, featureKey]
    );
    
    return result.rows.length > 0 ? result.rows[0].feature_value : null;
  }
}
```

---

## Plan Upgrades/Downgrades

### Subscription Change Service

```typescript
// subscription-change.ts
import Stripe from 'stripe';
import { Pool } from 'pg';

export class SubscriptionChangeService {
  constructor(
    private stripe: Stripe,
    private pool: Pool
  ) {}
  
  async upgradeSubscription(
    subscriptionId: string,
    newPlanId: string
  ): Promise<Stripe.Subscription> {
    // Get current subscription
    const subscription = await this.stripe.subscriptions.retrieve(subscriptionId);
    
    // Get new plan
    const newPlanResult = await this.pool.query(
      'SELECT stripe_price_id FROM plans WHERE id = $1',
      [newPlanId]
    );
    const newPriceId = newPlanResult.rows[0].stripe_price_id;
    
    // Update subscription
    const updatedSubscription = await this.stripe.subscriptions.update(subscriptionId, {
      items: [{
        id: subscription.items.data[0].id,
        price: newPriceId
      }],
      proration_behavior: 'create_prorations'
    });
    
    // Log history
    await this.logSubscriptionHistory(subscriptionId, 'upgrade', {
      old_plan_id: subscription.items.data[0].price.id,
      new_plan_id: newPriceId
    });
    
    return updatedSubscription;
  }
  
  async downgradeSubscription(
    subscriptionId: string,
    newPlanId: string,
    effectiveAt: 'immediate' | 'period_end' = 'period_end'
  ): Promise<Stripe.Subscription> {
    const subscription = await this.stripe.subscriptions.retrieve(subscriptionId);
    
    const newPlanResult = await this.pool.query(
      'SELECT stripe_price_id FROM plans WHERE id = $1',
      [newPlanId]
    );
    const newPriceId = newPlanResult.rows[0].stripe_price_id;
    
    const updateParams: Stripe.SubscriptionUpdateParams = {
      items: [{
        id: subscription.items.data[0].id,
        price: newPriceId
      }],
      proration_behavior: 'none' // No proration for downgrades
    };
    
    if (effectiveAt === 'period_end') {
      updateParams.cancel_at_period_end = false;
    }
    
    const updatedSubscription = await this.stripe.subscriptions.update(subscriptionId, updateParams);
    
    await this.logSubscriptionHistory(subscriptionId, 'downgrade', {
      old_plan_id: subscription.items.data[0].price.id,
      new_plan_id: newPriceId,
      effective_at: effectiveAt
    });
    
    return updatedSubscription;
  }
  
  async changeQuantity(
    subscriptionId: string,
    quantity: number
  ): Promise<Stripe.Subscription> {
    const subscription = await this.stripe.subscriptions.retrieve(subscriptionId);
    
    const updatedSubscription = await this.stripe.subscriptions.update(subscriptionId, {
      items: [{
        id: subscription.items.data[0].id,
        quantity
      }],
      proration_behavior: 'create_prorations'
    });
    
    await this.logSubscriptionHistory(subscriptionId, 'quantity_change', {
      old_quantity: subscription.items.data[0].quantity,
      new_quantity: quantity
    });
    
    return updatedSubscription;
  }
  
  private async logSubscriptionHistory(
    subscriptionId: string,
    eventType: string,
    metadata: Record<string, any>
  ): Promise<void> {
    await this.pool.query(
      `INSERT INTO subscription_history (subscription_id, event_type, metadata)
       VALUES ($1, $2, $3)`,
      [subscriptionId, eventType, metadata]
    );
  }
}
```

---

## Prorations

### Proration Calculation

```typescript
// proration.ts
import Stripe from 'stripe';

export interface ProrationCalculation {
  proratedAmount: number;
  creditAmount: number;
  chargeAmount: number;
  daysRemaining: number;
  daysInPeriod: number;
}

export class ProrationService {
  constructor(private stripe: Stripe) {}
  
  async calculateProration(
    subscriptionId: string,
    newPriceId: string
  ): Promise<ProrationCalculation> {
    const subscription = await this.stripe.subscriptions.retrieve(subscriptionId);
    const currentItem = subscription.items.data[0];
    const currentPrice = currentItem.price;
    const newPrice = await this.stripe.prices.retrieve(newPriceId);
    
    const currentPeriodEnd = new Date(subscription.current_period_end * 1000);
    const currentPeriodStart = new Date(subscription.current_period_start * 1000);
    const now = new Date();
    
    const daysInPeriod = Math.floor(
      (currentPeriodEnd.getTime() - currentPeriodStart.getTime()) / (1000 * 60 * 60 * 24)
    );
    const daysRemaining = Math.floor(
      (currentPeriodEnd.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)
    );
    
    const currentDailyRate = currentPrice.unit_amount / daysInPeriod;
    const newDailyRate = newPrice.unit_amount / daysInPeriod;
    
    const creditAmount = currentDailyRate * daysRemaining;
    const chargeAmount = newDailyRate * daysRemaining;
    const proratedAmount = chargeAmount - creditAmount;
    
    return {
      proratedAmount,
      creditAmount,
      chargeAmount,
      daysRemaining,
      daysInPeriod
    };
  }
  
  async previewProration(
    subscriptionId: string,
    newPriceId: string
  ): Promise<Stripe.UpcomingInvoice> {
    const subscription = await this.stripe.subscriptions.retrieve(subscriptionId);
    
    const invoice = await this.stripe.invoices.retrieveUpcoming({
      customer: subscription.customer as string,
      subscription: subscriptionId,
      subscription_items: [{
        id: subscription.items.data[0].id,
        price: newPriceId
      }]
    });
    
    return invoice;
  }
}
```

---

## Trial Periods

### Trial Management

```typescript
// trial-management.ts
import Stripe from 'stripe';
import { Pool } from 'pg';

export class TrialService {
  constructor(
    private stripe: Stripe,
    private pool: Pool
  ) {}
  
  async startTrial(
    customerId: string,
    priceId: string,
    trialDays: number = 14
  ): Promise<Stripe.Subscription> {
    const subscription = await this.stripe.subscriptions.create({
      customer: customerId,
      items: [{
        price: priceId
      }],
      trial_period_days: trialDays,
      payment_behavior: 'default_incomplete',
      metadata: {
        trial: true
      }
    });
    
    // Update local database
    await this.pool.query(
      `INSERT INTO subscriptions (user_id, plan_id, stripe_subscription_id, stripe_customer_id, status, trial_start, trial_end)
       VALUES ($1, $2, $3, $4, 'trialing', NOW(), NOW() + INTERVAL '${trialDays} days')`,
      [customerId, priceId, subscription.id, customerId]
    );
    
    return subscription;
  }
  
  async extendTrial(
    subscriptionId: string,
    additionalDays: number
  ): Promise<Stripe.Subscription> {
    const subscription = await this.stripe.subscriptions.retrieve(subscriptionId);
    const currentTrialEnd = subscription.trial_end || 0;
    const newTrialEnd = currentTrialEnd + (additionalDays * 24 * 60 * 60);
    
    const updatedSubscription = await this.stripe.subscriptions.update(subscriptionId, {
      trial_end: newTrialEnd
    });
    
    // Update local database
    await this.pool.query(
      `UPDATE subscriptions SET trial_end = NOW() + INTERVAL '${additionalDays} days' WHERE stripe_subscription_id = $1`,
      [subscriptionId]
    );
    
    return updatedSubscription;
  }
  
  async endTrial(
    subscriptionId: string
  ): Promise<Stripe.Subscription> {
    const subscription = await this.stripe.subscriptions.update(subscriptionId, {
      trial_end: 'now'
    });
    
    await this.pool.query(
      `UPDATE subscriptions SET trial_end = NOW() WHERE stripe_subscription_id = $1`,
      [subscriptionId]
    );
    
    return subscription;
  }
  
  async getTrialSubscriptions(): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM subscriptions WHERE status = 'trialing' AND trial_end > NOW()`
    );
    
    return result.rows;
  }
  
  async getExpiringTrials(days: number = 3): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM subscriptions 
       WHERE status = 'trialing' 
       AND trial_end <= NOW() + INTERVAL '${days} days' 
       AND trial_end > NOW()`
    );
    
    return result.rows;
  }
}
```

---

## Cancellation Handling

### Cancellation Service

```typescript
// cancellation-service.ts
import Stripe from 'stripe';
import { Pool } from 'pg';

export class CancellationService {
  constructor(
    private stripe: Stripe,
    private pool: Pool
  ) {}
  
  async cancelAtPeriodEnd(subscriptionId: string): Promise<Stripe.Subscription> {
    const subscription = await this.stripe.subscriptions.update(subscriptionId, {
      cancel_at_period_end: true
    });
    
    await this.pool.query(
      `UPDATE subscriptions SET cancel_at_period_end = true WHERE stripe_subscription_id = $1`,
      [subscriptionId]
    );
    
    await this.logCancellation(subscriptionId, 'cancel_at_period_end');
    
    return subscription;
  }
  
  async cancelImmediately(subscriptionId: string): Promise<Stripe.Subscription> {
    const subscription = await this.stripe.subscriptions.cancel(subscriptionId);
    
    await this.pool.query(
      `UPDATE subscriptions 
       SET status = 'canceled', canceled_at = NOW() 
       WHERE stripe_subscription_id = $1`,
      [subscriptionId]
    );
    
    await this.logCancellation(subscriptionId, 'cancel_immediately');
    
    return subscription;
  }
  
  async reinstateSubscription(subscriptionId: string): Promise<Stripe.Subscription> {
    const subscription = await this.stripe.subscriptions.update(subscriptionId, {
      cancel_at_period_end: false
    });
    
    await this.pool.query(
      `UPDATE subscriptions SET cancel_at_period_end = false WHERE stripe_subscription_id = $1`,
      [subscriptionId]
    );
    
    await this.logCancellation(subscriptionId, 'reinstate');
    
    return subscription;
  }
  
  async getCancellationSurvey(subscriptionId: string): Promise<any> {
    const result = await this.pool.query(
      `SELECT * FROM cancellation_surveys WHERE subscription_id = $1`,
      [subscriptionId]
    );
    
    return result.rows[0] || null;
  }
  
  async recordCancellationReason(
    subscriptionId: string,
    reason: string,
    feedback?: string
  ): Promise<void> {
    await this.pool.query(
      `INSERT INTO cancellation_surveys (subscription_id, reason, feedback, created_at)
       VALUES ($1, $2, $3, NOW())`,
      [subscriptionId, reason, feedback]
    );
  }
  
  private async logCancellation(
    subscriptionId: string,
    action: string
  ): Promise<void> {
    await this.pool.query(
      `INSERT INTO subscription_history (subscription_id, event_type, metadata)
       VALUES ($1, 'cancellation', $2)`,
      [subscriptionId, { action }]
    );
  }
}
```

---

## Plan Comparison UI

### React Component

```typescript
// plan-comparison.tsx
import React from 'react';

interface Plan {
  id: string;
  name: string;
  price: number;
  currency: string;
  interval: string;
  features: string[];
  popular?: boolean;
}

interface PlanComparisonProps {
  plans: Plan[];
  onSubscribe: (planId: string) => void;
  currentPlanId?: string;
}

export const PlanComparison: React.FC<PlanComparisonProps> = ({
  plans,
  onSubscribe,
  currentPlanId
}) => {
  const allFeatures = Array.from(
    new Set(plans.flatMap(plan => plan.features))
  );
  
  return (
    <div className="plan-comparison">
      <div className="plans-grid">
        {plans.map(plan => (
          <div
            key={plan.id}
            className={`plan-card ${plan.popular ? 'popular' : ''} ${currentPlanId === plan.id ? 'current' : ''}`}
          >
            {plan.popular && <div className="popular-badge">Most Popular</div>}
            {currentPlanId === plan.id && <div className="current-badge">Current Plan</div>}
            
            <h3>{plan.name}</h3>
            <div className="price">
              <span className="amount">${plan.price}</span>
              <span className="interval">/{plan.interval}</span>
            </div>
            
            <ul className="features">
              {plan.features.map((feature, index) => (
                <li key={index}>{feature}</li>
              ))}
            </ul>
            
            <button
              className={`subscribe-btn ${currentPlanId === plan.id ? 'disabled' : ''}`}
              onClick={() => onSubscribe(plan.id)}
              disabled={currentPlanId === plan.id}
            >
              {currentPlanId === plan.id ? 'Current Plan' : 'Subscribe'}
            </button>
          </div>
        ))}
      </div>
      
      <div className="feature-table">
        <table>
          <thead>
            <tr>
              <th>Feature</th>
              {plans.map(plan => (
                <th key={plan.id}>{plan.name}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {allFeatures.map(feature => (
              <tr key={feature}>
                <td>{feature}</td>
                {plans.map(plan => (
                  <td key={plan.id}>
                    {plan.features.includes(feature) ? '✓' : '✗'}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
```

---

## Feature Flags per Plan

### Feature Flag Integration

```typescript
// plan-feature-flags.ts
import { FeatureFlagService } from './feature-flags';

export class PlanFeatureFlagService {
  constructor(
    private featureFlagService: FeatureFlagService
  ) {}
  
  async getFeatureFlagsForUser(userId: string): Promise<Record<string, boolean>> {
    const flags = await this.featureFlagService.getUserFlags(userId);
    
    // Override with plan-based flags
    const planFlags = await this.getPlanFeatureFlags(userId);
    
    return { ...flags, ...planFlags };
  }
  
  async checkFeatureAccess(
    userId: string,
    featureKey: string
  ): Promise<boolean> {
    const flags = await this.getFeatureFlagsForUser(userId);
    return flags[featureKey] || false;
  }
  
  private async getPlanFeatureFlags(userId: string): Promise<Record<string, boolean>> {
    // Implementation to get plan-based feature flags
    return {};
  }
}
```

---

## Migration Strategies

### Plan Migration

```typescript
// plan-migration.ts
import { Pool } from 'pg';

export class PlanMigrationService {
  constructor(private pool: Pool) {}
  
  async migrateUsersToNewPlan(
    oldPlanId: string,
    newPlanId: string,
    batchSize: number = 100
  ): Promise<void> {
    let offset = 0;
    let migrated = 0;
    
    while (true) {
      const subscriptions = await this.pool.query(
        `SELECT id, user_id FROM subscriptions 
         WHERE plan_id = $1 AND status = 'active'
         LIMIT $2 OFFSET $3`,
        [oldPlanId, batchSize, offset]
      );
      
      if (subscriptions.rows.length === 0) break;
      
      for (const sub of subscriptions.rows) {
        await this.migrateSubscription(sub.id, newPlanId);
        migrated++;
      }
      
      offset += batchSize;
      console.log(`Migrated ${migrated} subscriptions...`);
    }
    
    console.log(`Migration complete. Total migrated: ${migrated}`);
  }
  
  async migrateSubscription(
    subscriptionId: string,
    newPlanId: string
  ): Promise<void> {
    await this.pool.query(
      `UPDATE subscriptions SET plan_id = $1 WHERE id = $2`,
      [newPlanId, subscriptionId]
    );
    
    await this.pool.query(
      `INSERT INTO subscription_history (subscription_id, event_type, new_plan_id, metadata)
       VALUES ($1, 'migration', $2, $3)`,
      [subscriptionId, newPlanId, { migrated_at: new Date() }]
    );
  }
  
  async rollbackMigration(
    oldPlanId: string,
    newPlanId: string
  ): Promise<void> {
    await this.pool.query(
      `UPDATE subscriptions SET plan_id = $1 WHERE plan_id = $2`,
      [oldPlanId, newPlanId]
    );
    
    await this.pool.query(
      `INSERT INTO subscription_history (subscription_id, event_type, old_plan_id, new_plan_id, metadata)
       SELECT id, 'rollback', $1, $2, $3 FROM subscriptions WHERE plan_id = $2`,
      [oldPlanId, newPlanId, { rolled_back_at: new Date() }]
    );
  }
}
```

---

## Best Practices

```markdown
## Subscription Plans Best Practices

### Plan Design
- [ ] Keep plans simple and easy to understand
- [ ] Limit to 3-4 plans maximum
- [ ] Use clear, descriptive names
- [ ] Highlight the recommended plan
- [ ] Show clear value differentiation
- [ ] Include feature comparison table

### Pricing Strategy
- [ ] Use psychological pricing ($9.99 instead of $10)
- [ ] Offer annual discounts (10-20%)
- [ ] Provide free tier for user acquisition
- [ ] Consider usage-based pricing for variable costs
- [ ] Implement clear upgrade paths

### Trial Management
- [ ] Offer 14-30 day trials
- [ ] Collect payment method before trial
- [ ] Send trial expiration reminders
- [ ] Offer trial extensions for qualified leads
- [ ] Track trial conversion rates

### Change Management
- [ ] Prorate charges for upgrades
- [ ] No proration for downgrades
- [ ] Allow immediate or period-end changes
- [ ] Send confirmation emails
- [ ] Maintain change history

### Cancellation
- [ ] Offer cancel at period end option
- [ ] Collect cancellation feedback
- [ ] Provide pause option instead of cancel
- [ ] Offer win-back incentives
- [ ] Keep cancellation process simple

### Communication
- [ ] Send billing reminders
- [ ] Notify of plan changes
- [ ] Provide invoice access
- [ ] Send payment failure notifications
- [ ] Offer multiple support channels

### Analytics
- [ ] Track MRR (Monthly Recurring Revenue)
- [ ] Monitor churn rate
- [ ] Track conversion rates
- [ ] Analyze upgrade/downgrade patterns
- [ ] Monitor trial conversion

### Compliance
- [ ] Clear terms of service
- [ ] Transparent pricing
- [ ] Easy cancellation process
- [ ] Data retention policies
- [ ] GDPR compliance
```

---

## Additional Resources

- [Stripe Subscriptions](https://stripe.com/docs/billing/subscriptions/overview)
- [SaaS Pricing Strategies](https://www.chargebee.com/blog/saas-pricing-strategies/)
- [Subscription Business Models](https://www.recurly.com/blog/subscription-business-models)
- [Pricing Psychology](https://hbr.org/2019/03/the-psychology-of-pricing)
