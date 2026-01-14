# Billing Cycles

## Overview

Comprehensive guide to billing cycle management, proration logic, and payment processing.

## Table of Contents

1. [Billing Cycle Types](#billing-cycle-types)
2. [Cycle Calculation](#cycle-calculation)
3. [Proration Logic](#proration-logic)
4. [Billing Date Handling](#billing-date-handling)
5. [Grace Periods](#grace-periods)
6. [Dunning Management](#dunning-management)
7. [Failed Payment Handling](#failed-payment-handling)
8. [Automated Billing Jobs](#automated-billing-jobs)
9. [Billing Notifications](#billing-notifications)
10. [Testing Billing Cycles](#testing-billing-cycles)
11. [Edge Cases](#edge-cases)

---

## Billing Cycle Types

### Cycle Types

```typescript
// billing-cycle-types.ts

export enum BillingCycleType {
  MONTHLY = 'monthly',
  YEARLY = 'yearly',
  WEEKLY = 'weekly',
  CUSTOM = 'custom'
}

export interface BillingCycle {
  id: string;
  type: BillingCycleType;
  interval: number; // For custom cycles
  anchorDate: Date; // Billing anchor date
  nextBillingDate: Date;
  previousBillingDate?: Date;
}

export interface BillingPeriod {
  start: Date;
  end: Date;
  days: number;
  proratedDays?: number;
}
```

### Monthly Cycle

```typescript
// monthly-cycle.ts
export class MonthlyBillingCycle {
  static calculateNextBillingDate(
    anchorDate: Date,
    currentDate: Date
  ): Date {
    const next = new Date(anchorDate);
    next.setFullYear(currentDate.getFullYear());
    next.setMonth(currentDate.getMonth());
    
    // If anchor day is greater than current month's days, use last day
    const lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
    const anchorDay = Math.min(anchorDate.getDate(), lastDayOfMonth);
    next.setDate(anchorDay);
    
    // If next billing date has passed, move to next month
    if (next <= currentDate) {
      next.setMonth(next.getMonth() + 1);
    }
    
    return next;
  }
  
  static calculateBillingPeriod(
    anchorDate: Date,
    billingDate: Date
  ): BillingPeriod {
    const start = new Date(billingDate);
    start.setMonth(start.getMonth() - 1);
    
    const end = new Date(billingDate);
    end.setMilliseconds(end.getMilliseconds() - 1);
    
    const days = Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
    
    return { start, end, days };
  }
}
```

### Yearly Cycle

```typescript
// yearly-cycle.ts
export class YearlyBillingCycle {
  static calculateNextBillingDate(
    anchorDate: Date,
    currentDate: Date
  ): Date {
    const next = new Date(anchorDate);
    next.setFullYear(currentDate.getFullYear());
    
    // If anchor day is greater than current year's days, adjust
    const lastDayOfYear = new Date(currentDate.getFullYear(), 11, 31).getDate();
    const anchorDay = Math.min(anchorDate.getDate(), lastDayOfYear);
    next.setDate(anchorDay);
    
    // If next billing date has passed, move to next year
    if (next <= currentDate) {
      next.setFullYear(next.getFullYear() + 1);
    }
    
    return next;
  }
  
  static calculateBillingPeriod(
    anchorDate: Date,
    billingDate: Date
  ): BillingPeriod {
    const start = new Date(billingDate);
    start.setFullYear(start.getFullYear() - 1);
    
    const end = new Date(billingDate);
    end.setMilliseconds(end.getMilliseconds() - 1);
    
    const days = Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
    
    return { start, end, days };
  }
}
```

---

## Cycle Calculation

### Billing Cycle Calculator

```typescript
// cycle-calculator.ts
import { BillingCycleType, BillingCycle, BillingPeriod } from './billing-cycle-types';

export class BillingCycleCalculator {
  static calculateNextBillingDate(
    type: BillingCycleType,
    anchorDate: Date,
    currentDate: Date,
    interval: number = 1
  ): Date {
    switch (type) {
      case BillingCycleType.MONTHLY:
        return this.calculateMonthlyNextDate(anchorDate, currentDate, interval);
      case BillingCycleType.YEARLY:
        return this.calculateYearlyNextDate(anchorDate, currentDate, interval);
      case BillingCycleType.WEEKLY:
        return this.calculateWeeklyNextDate(anchorDate, currentDate, interval);
      case BillingCycleType.CUSTOM:
        return this.calculateCustomNextDate(anchorDate, currentDate, interval);
      default:
        throw new Error(`Unknown billing cycle type: ${type}`);
    }
  }
  
  private static calculateMonthlyNextDate(
    anchorDate: Date,
    currentDate: Date,
    interval: number
  ): Date {
    const next = new Date(anchorDate);
    next.setFullYear(currentDate.getFullYear());
    next.setMonth(currentDate.getMonth());
    
    // Adjust for months with fewer days
    const lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
    const anchorDay = Math.min(anchorDate.getDate(), lastDayOfMonth);
    next.setDate(anchorDay);
    
    // Add interval months if needed
    while (next <= currentDate) {
      next.setMonth(next.getMonth() + interval);
    }
    
    return next;
  }
  
  private static calculateYearlyNextDate(
    anchorDate: Date,
    currentDate: Date,
    interval: number
  ): Date {
    const next = new Date(anchorDate);
    next.setFullYear(currentDate.getFullYear());
    
    // Adjust for leap years
    const lastDayOfYear = new Date(currentDate.getFullYear(), 11, 31).getDate();
    const anchorDay = Math.min(anchorDate.getDate(), lastDayOfYear);
    next.setDate(anchorDay);
    
    // Add interval years if needed
    while (next <= currentDate) {
      next.setFullYear(next.getFullYear() + interval);
    }
    
    return next;
  }
  
  private static calculateWeeklyNextDate(
    anchorDate: Date,
    currentDate: Date,
    interval: number
  ): Date {
    const anchorDayOfWeek = anchorDate.getDay();
    const currentDayOfWeek = currentDate.getDay();
    
    let daysUntilNext = (anchorDayOfWeek - currentDayOfWeek + 7) % 7;
    if (daysUntilNext === 0) daysUntilNext = 7 * interval;
    
    const next = new Date(currentDate);
    next.setDate(next.getDate() + daysUntilNext);
    
    return next;
  }
  
  private static calculateCustomNextDate(
    anchorDate: Date,
    currentDate: Date,
    interval: number
  ): Date {
    const next = new Date(anchorDate);
    next.setFullYear(currentDate.getFullYear());
    
    while (next <= currentDate) {
      next.setDate(next.getDate() + interval);
    }
    
    return next;
  }
  
  static calculateBillingPeriod(
    type: BillingCycleType,
    anchorDate: Date,
    billingDate: Date
  ): BillingPeriod {
    switch (type) {
      case BillingCycleType.MONTHLY:
        return this.calculateMonthlyPeriod(anchorDate, billingDate);
      case BillingCycleType.YEARLY:
        return this.calculateYearlyPeriod(anchorDate, billingDate);
      case BillingCycleType.WEEKLY:
        return this.calculateWeeklyPeriod(anchorDate, billingDate);
      case BillingCycleType.CUSTOM:
        return this.calculateCustomPeriod(anchorDate, billingDate);
      default:
        throw new Error(`Unknown billing cycle type: ${type}`);
    }
  }
  
  private static calculateMonthlyPeriod(
    anchorDate: Date,
    billingDate: Date
  ): BillingPeriod {
    const start = new Date(billingDate);
    start.setMonth(start.getMonth() - 1);
    
    const end = new Date(billingDate);
    end.setMilliseconds(end.getMilliseconds() - 1);
    
    const days = Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
    
    return { start, end, days };
  }
  
  private static calculateYearlyPeriod(
    anchorDate: Date,
    billingDate: Date
  ): BillingPeriod {
    const start = new Date(billingDate);
    start.setFullYear(start.getFullYear() - 1);
    
    const end = new Date(billingDate);
    end.setMilliseconds(end.getMilliseconds() - 1);
    
    const days = Math.floor((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
    
    return { start, end, days };
  }
  
  private static calculateWeeklyPeriod(
    anchorDate: Date,
    billingDate: Date
  ): BillingPeriod {
    const start = new Date(billingDate);
    start.setDate(start.getDate() - 7);
    
    const end = new Date(billingDate);
    end.setMilliseconds(end.getMilliseconds() - 1);
    
    const days = 7;
    
    return { start, end, days };
  }
  
  private static calculateCustomPeriod(
    anchorDate: Date,
    billingDate: Date
  ): BillingPeriod {
    // Calculate based on interval
    const start = new Date(billingDate);
    start.setDate(start.getDate() - 30); // Default 30 days
    
    const end = new Date(billingDate);
    end.setMilliseconds(end.getMilliseconds() - 1);
    
    const days = 30;
    
    return { start, end, days };
  }
}
```

---

## Proration Logic

### Proration Calculator

```typescript
// proration-calculator.ts
import { BillingPeriod } from './billing-cycle-types';

export interface ProrationResult {
  proratedAmount: number;
  creditAmount: number;
  chargeAmount: number;
  daysRemaining: number;
  daysInPeriod: number;
  prorationFactor: number;
}

export class ProrationCalculator {
  static calculateProration(
    fullAmount: number,
    billingPeriod: BillingPeriod,
    currentDate: Date
  ): ProrationResult {
    const daysInPeriod = billingPeriod.days;
    const daysRemaining = Math.max(0, Math.floor(
      (billingPeriod.end.getTime() - currentDate.getTime()) / (1000 * 60 * 60 * 24)
    ));
    
    const prorationFactor = daysRemaining / daysInPeriod;
    const proratedAmount = fullAmount * prorationFactor;
    const creditAmount = fullAmount - proratedAmount;
    const chargeAmount = proratedAmount;
    
    return {
      proratedAmount,
      creditAmount,
      chargeAmount,
      daysRemaining,
      daysInPeriod,
      prorationFactor
    };
  }
  
  static calculateUpgradeProration(
    oldAmount: number,
    newAmount: number,
    billingPeriod: BillingPeriod,
    currentDate: Date
  ): ProrationResult {
    const daysInPeriod = billingPeriod.days;
    const daysRemaining = Math.max(0, Math.floor(
      (billingPeriod.end.getTime() - currentDate.getTime()) / (1000 * 60 * 60 * 24)
    ));
    
    const prorationFactor = daysRemaining / daysInPeriod;
    
    // Credit for unused portion of old plan
    const creditAmount = oldAmount * prorationFactor;
    
    // Charge for new plan for remaining period
    const chargeAmount = newAmount * prorationFactor;
    
    const proratedAmount = chargeAmount - creditAmount;
    
    return {
      proratedAmount,
      creditAmount,
      chargeAmount,
      daysRemaining,
      daysInPeriod,
      prorationFactor
    };
  }
  
  static calculateDowngradeProration(
    oldAmount: number,
    newAmount: number,
    billingPeriod: BillingPeriod,
    effectiveAt: 'immediate' | 'period_end'
  ): ProrationResult {
    if (effectiveAt === 'period_end') {
      // No proration for period-end downgrades
      return {
        proratedAmount: 0,
        creditAmount: 0,
        chargeAmount: 0,
        daysRemaining: 0,
        daysInPeriod: billingPeriod.days,
        prorationFactor: 0
      };
    }
    
    // For immediate downgrades, no credit is given
    return {
      proratedAmount: 0,
      creditAmount: 0,
      chargeAmount: 0,
      daysRemaining: 0,
      daysInPeriod: billingPeriod.days,
      prorationFactor: 0
    };
  }
  
  static calculateMidCycleProration(
    amount: number,
    startDate: Date,
    endDate: Date,
    billingPeriod: BillingPeriod
  ): ProrationResult {
    const daysInPeriod = billingPeriod.days;
    const daysInUsage = Math.floor(
      (endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24)
    );
    
    const prorationFactor = daysInUsage / daysInPeriod;
    const proratedAmount = amount * prorationFactor;
    
    return {
      proratedAmount,
      creditAmount: 0,
      chargeAmount: proratedAmount,
      daysRemaining: daysInUsage,
      daysInPeriod,
      prorationFactor
    };
  }
}
```

---

## Billing Date Handling

### Billing Date Service

```typescript
// billing-date-service.ts
import { BillingCycleType } from './billing-cycle-types';

export class BillingDateService {
  static adjustForWeekend(date: Date): Date {
    const dayOfWeek = date.getDay();
    
    if (dayOfWeek === 0) {
      // Sunday, move to Monday
      const adjusted = new Date(date);
      adjusted.setDate(adjusted.getDate() + 1);
      return adjusted;
    }
    
    if (dayOfWeek === 6) {
      // Saturday, move to Friday
      const adjusted = new Date(date);
      adjusted.setDate(adjusted.getDate() - 1);
      return adjusted;
    }
    
    return new Date(date);
  }
  
  static adjustForHoliday(date: Date, holidays: Date[]): Date {
    const isHoliday = holidays.some(holiday =>
      holiday.getDate() === date.getDate() &&
      holiday.getMonth() === date.getMonth() &&
      holiday.getFullYear() === date.getFullYear()
    );
    
    if (isHoliday) {
      const adjusted = new Date(date);
      adjusted.setDate(adjusted.getDate() + 1);
      return this.adjustForHoliday(adjusted, holidays);
    }
    
    return this.adjustForWeekend(date);
  }
  
  static getBillingDayOfMonth(anchorDate: Date, currentDate: Date): number {
    const lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
    return Math.min(anchorDate.getDate(), lastDayOfMonth);
  }
  
  static getNextBillingDate(
    type: BillingCycleType,
    anchorDate: Date,
    currentDate: Date,
    holidays?: Date[]
  ): Date {
    const nextDate = this.calculateNextBillingDate(type, anchorDate, currentDate);
    
    if (holidays) {
      return this.adjustForHoliday(nextDate, holidays);
    }
    
    return this.adjustForWeekend(nextDate);
  }
  
  private static calculateNextBillingDate(
    type: BillingCycleType,
    anchorDate: Date,
    currentDate: Date
  ): Date {
    switch (type) {
      case BillingCycleType.MONTHLY:
        return this.calculateMonthlyNextDate(anchorDate, currentDate);
      case BillingCycleType.YEARLY:
        return this.calculateYearlyNextDate(anchorDate, currentDate);
      case BillingCycleType.WEEKLY:
        return this.calculateWeeklyNextDate(anchorDate, currentDate);
      default:
        throw new Error(`Unknown billing cycle type: ${type}`);
    }
  }
  
  private static calculateMonthlyNextDate(anchorDate: Date, currentDate: Date): Date {
    const next = new Date(anchorDate);
    next.setFullYear(currentDate.getFullYear());
    next.setMonth(currentDate.getMonth());
    
    const lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
    const anchorDay = Math.min(anchorDate.getDate(), lastDayOfMonth);
    next.setDate(anchorDay);
    
    if (next <= currentDate) {
      next.setMonth(next.getMonth() + 1);
    }
    
    return next;
  }
  
  private static calculateYearlyNextDate(anchorDate: Date, currentDate: Date): Date {
    const next = new Date(anchorDate);
    next.setFullYear(currentDate.getFullYear());
    
    const lastDayOfYear = new Date(currentDate.getFullYear(), 11, 31).getDate();
    const anchorDay = Math.min(anchorDate.getDate(), lastDayOfYear);
    next.setDate(anchorDay);
    
    if (next <= currentDate) {
      next.setFullYear(next.getFullYear() + 1);
    }
    
    return next;
  }
  
  private static calculateWeeklyNextDate(anchorDate: Date, currentDate: Date): Date {
    const anchorDayOfWeek = anchorDate.getDay();
    const currentDayOfWeek = currentDate.getDay();
    
    let daysUntilNext = (anchorDayOfWeek - currentDayOfWeek + 7) % 7;
    if (daysUntilNext === 0) daysUntilNext = 7;
    
    const next = new Date(currentDate);
    next.setDate(next.getDate() + daysUntilNext);
    
    return next;
  }
}
```

---

## Grace Periods

### Grace Period Service

```typescript
// grace-period-service.ts
export enum GracePeriodType {
  PAYMENT_FAILED = 'payment_failed',
  TRIAL_EXPIRED = 'trial_expired',
  ACCOUNT_SUSPENDED = 'account_suspended'
}

export interface GracePeriod {
  type: GracePeriodType;
  startDate: Date;
  endDate: Date;
  daysRemaining: number;
  isActive: boolean;
}

export class GracePeriodService {
  static createGracePeriod(
    type: GracePeriodType,
    days: number = 7
  ): GracePeriod {
    const startDate = new Date();
    const endDate = new Date();
    endDate.setDate(endDate.getDate() + days);
    
    return {
      type,
      startDate,
      endDate,
      daysRemaining: days,
      isActive: true
    };
  }
  
  static checkGracePeriod(gracePeriod: GracePeriod): boolean {
    const now = new Date();
    return now <= gracePeriod.endDate && gracePeriod.isActive;
  }
  
  static updateGracePeriod(gracePeriod: GracePeriod): GracePeriod {
    const now = new Date();
    const daysRemaining = Math.max(0, Math.ceil(
      (gracePeriod.endDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24)
    ));
    
    return {
      ...gracePeriod,
      daysRemaining,
      isActive: now <= gracePeriod.endDate
    };
  }
  
  static extendGracePeriod(
    gracePeriod: GracePeriod,
    additionalDays: number
  ): GracePeriod {
    const endDate = new Date(gracePeriod.endDate);
    endDate.setDate(endDate.getDate() + additionalDays);
    
    return {
      ...gracePeriod,
      endDate,
      daysRemaining: gracePeriod.daysRemaining + additionalDays
    };
  }
  
  static cancelGracePeriod(gracePeriod: GracePeriod): GracePeriod {
    return {
      ...gracePeriod,
      isActive: false,
      daysRemaining: 0
    };
  }
}
```

---

## Dunning Management

### Dunning Service

```typescript
// dunning-service.ts
import { Pool } from 'pg';

export enum DunningStatus {
  ACTIVE = 'active',
  IN_DUNNING = 'in_dunning',
  CANCELLED = 'cancelled',
  RESOLVED = 'resolved'
}

export interface DunningAttempt {
  attemptNumber: number;
  date: Date;
  status: 'pending' | 'success' | 'failed';
  error?: string;
}

export class DunningService {
  private static readonly MAX_ATTEMPTS = 4;
  private static readonly RETRY_INTERVALS = [1, 3, 7]; // Days
  
  constructor(private pool: Pool) {}
  
  async startDunning(subscriptionId: string): Promise<void> {
    await this.pool.query(
      `UPDATE subscriptions 
       SET dunning_status = 'in_dunning', 
           dunning_started_at = NOW(),
           dunning_attempt_count = 0
       WHERE id = $1`,
      [subscriptionId]
    );
  }
  
  async recordDunningAttempt(
    subscriptionId: string,
    success: boolean,
    error?: string
  ): Promise<void> {
    const result = await this.pool.query(
      `SELECT dunning_attempt_count FROM subscriptions WHERE id = $1`,
      [subscriptionId]
    );
    
    const attemptCount = result.rows[0].dunning_attempt_count + 1;
    
    await this.pool.query(
      `UPDATE subscriptions 
       SET dunning_attempt_count = $1,
           last_dunning_attempt_at = NOW()
       WHERE id = $2`,
      [attemptCount, subscriptionId]
    );
    
    // Log attempt
    await this.pool.query(
      `INSERT INTO dunning_attempts (subscription_id, attempt_number, status, error, created_at)
       VALUES ($1, $2, $3, $4, NOW())`,
      [subscriptionId, attemptCount, success ? 'success' : 'failed', error]
    );
    
    if (success) {
      await this.resolveDunning(subscriptionId);
    } else if (attemptCount >= DunningService.MAX_ATTEMPTS) {
      await this.cancelSubscription(subscriptionId);
    }
  }
  
  async getNextRetryDate(subscriptionId: string): Promise<Date | null> {
    const result = await this.pool.query(
      `SELECT dunning_attempt_count, last_dunning_attempt_at 
       FROM subscriptions 
       WHERE id = $1 AND dunning_status = 'in_dunning'`,
      [subscriptionId]
    );
    
    if (result.rows.length === 0) return null;
    
    const attemptCount = result.rows[0].dunning_attempt_count;
    const lastAttempt = result.rows[0].last_dunning_attempt_at;
    
    if (attemptCount >= DunningService.RETRY_INTERVALS.length) return null;
    
    const retryDays = DunningService.RETRY_INTERVALS[attemptCount];
    const retryDate = new Date(lastAttempt);
    retryDate.setDate(retryDate.getDate() + retryDays);
    
    return retryDate;
  }
  
  async resolveDunning(subscriptionId: string): Promise<void> {
    await this.pool.query(
      `UPDATE subscriptions 
       SET dunning_status = 'resolved',
           dunning_ended_at = NOW()
       WHERE id = $1`,
      [subscriptionId]
    );
  }
  
  async cancelSubscription(subscriptionId: string): Promise<void> {
    await this.pool.query(
      `UPDATE subscriptions 
       SET dunning_status = 'cancelled',
           status = 'canceled',
           dunning_ended_at = NOW(),
           canceled_at = NOW()
       WHERE id = $1`,
      [subscriptionId]
    );
  }
  
  async getDunningAttempts(
    subscriptionId: string
  ): Promise<DunningAttempt[]> {
    const result = await this.pool.query(
      `SELECT attempt_number, created_at as date, status, error
       FROM dunning_attempts
       WHERE subscription_id = $1
       ORDER BY attempt_number`,
      [subscriptionId]
    );
    
    return result.rows;
  }
}

// SQL for dunning attempts table
/*
CREATE TABLE dunning_attempts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subscription_id UUID NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
  attempt_number INTEGER NOT NULL,
  status VARCHAR(20) NOT NULL CHECK (status IN ('pending', 'success', 'failed')),
  error TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
*/
```

---

## Failed Payment Handling

### Failed Payment Service

```typescript
// failed-payment-service.ts
import { Pool } from 'pg';

export class FailedPaymentService {
  constructor(private pool: Pool) {}
  
  async handleFailedPayment(
    subscriptionId: string,
    invoiceId: string,
    errorMessage: string
  ): Promise<void> {
    // Update subscription status
    await this.pool.query(
      `UPDATE subscriptions 
       SET status = 'past_due',
           last_payment_failed_at = NOW(),
           last_payment_error = $1
       WHERE id = $2`,
      [errorMessage, subscriptionId]
    );
    
    // Log failed payment
    await this.pool.query(
      `INSERT INTO failed_payments (subscription_id, invoice_id, error_message, created_at)
       VALUES ($1, $2, $3, NOW())`,
      [subscriptionId, invoiceId, errorMessage]
    );
    
    // Start dunning process
    await this.startDunning(subscriptionId);
  }
  
  async handleSuccessfulRetry(
    subscriptionId: string,
    invoiceId: string
  ): Promise<void> {
    // Update subscription status
    await this.pool.query(
      `UPDATE subscriptions 
       SET status = 'active',
           last_payment_succeeded_at = NOW()
       WHERE id = $1`,
      [subscriptionId]
    );
    
    // Log successful retry
    await this.pool.query(
      `INSERT INTO payment_retries (subscription_id, invoice_id, status, created_at)
       VALUES ($1, $2, 'success', NOW())`,
      [subscriptionId, invoiceId]
    );
    
    // Resolve dunning
    await this.resolveDunning(subscriptionId);
  }
  
  async getFailedPayments(
    subscriptionId: string
  ): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM failed_payments 
       WHERE subscription_id = $1 
       ORDER BY created_at DESC`,
      [subscriptionId]
    );
    
    return result.rows;
  }
  
  async getRetryHistory(
    subscriptionId: string
  ): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM payment_retries 
       WHERE subscription_id = $1 
       ORDER BY created_at DESC`,
      [subscriptionId]
    );
    
    return result.rows;
  }
  
  private async startDunning(subscriptionId: string): Promise<void> {
    await this.pool.query(
      `UPDATE subscriptions 
       SET dunning_status = 'in_dunning',
           dunning_started_at = NOW(),
           dunning_attempt_count = 0
       WHERE id = $1`,
      [subscriptionId]
    );
  }
  
  private async resolveDunning(subscriptionId: string): Promise<void> {
    await this.pool.query(
      `UPDATE subscriptions 
       SET dunning_status = 'resolved',
           dunning_ended_at = NOW()
       WHERE id = $1`,
      [subscriptionId]
    );
  }
}

// SQL tables
/*
CREATE TABLE failed_payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subscription_id UUID NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
  invoice_id VARCHAR(255),
  error_message TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE payment_retries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subscription_id UUID NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
  invoice_id VARCHAR(255),
  status VARCHAR(20) NOT NULL CHECK (status IN ('success', 'failed')),
  created_at TIMESTAMP DEFAULT NOW()
);
*/
```

---

## Automated Billing Jobs

### Billing Job Scheduler

```typescript
// billing-jobs.ts
import cron from 'node-cron';
import { Pool } from 'pg';

export class BillingJobScheduler {
  constructor(private pool: Pool) {}
  
  start(): void {
    // Run daily at midnight UTC
    cron.schedule('0 0 * * *', async () => {
      await this.processDailyBilling();
    });
    
    // Run hourly for payment retries
    cron.schedule('0 * * * *', async () => {
      await this.processPaymentRetries();
    });
    
    // Run daily for grace period checks
    cron.schedule('0 0 * * *', async () => {
      await this.checkGracePeriods();
    });
    
    // Run daily for subscription renewals
    cron.schedule('0 0 * * *', async () => {
      await this.processSubscriptionRenewals();
    });
    
    console.log('Billing jobs started');
  }
  
  private async processDailyBilling(): Promise<void> {
    console.log('Processing daily billing...');
    
    const subscriptions = await this.getSubscriptionsDueForBilling();
    
    for (const subscription of subscriptions) {
      try {
        await this.processSubscriptionBilling(subscription);
      } catch (error) {
        console.error(`Error processing billing for subscription ${subscription.id}:`, error);
      }
    }
    
    console.log(`Processed ${subscriptions.length} subscriptions`);
  }
  
  private async processPaymentRetries(): Promise<void> {
    console.log('Processing payment retries...');
    
    const retries = await this.getPendingRetries();
    
    for (const retry of retries) {
      try {
        await this.processRetry(retry);
      } catch (error) {
        console.error(`Error processing retry for subscription ${retry.subscription_id}:`, error);
      }
    }
    
    console.log(`Processed ${retries.length} retries`);
  }
  
  private async checkGracePeriods(): Promise<void> {
    console.log('Checking grace periods...');
    
    const expiring = await this.getExpiringGracePeriods();
    
    for (const subscription of expiring) {
      try {
        await this.handleExpiringGracePeriod(subscription);
      } catch (error) {
        console.error(`Error handling expiring grace period for ${subscription.id}:`, error);
      }
    }
    
    console.log(`Checked ${expiring.length} grace periods`);
  }
  
  private async processSubscriptionRenewals(): Promise<void> {
    console.log('Processing subscription renewals...');
    
    const renewals = await this.getSubscriptionsDueForRenewal();
    
    for (const subscription of renewals) {
      try {
        await this.processRenewal(subscription);
      } catch (error) {
        console.error(`Error processing renewal for subscription ${subscription.id}:`, error);
      }
    }
    
    console.log(`Processed ${renewals.length} renewals`);
  }
  
  private async getSubscriptionsDueForBilling(): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM subscriptions 
       WHERE status = 'active' 
       AND next_billing_date <= NOW()
       AND cancel_at_period_end = false`
    );
    return result.rows;
  }
  
  private async getPendingRetries(): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT s.*, d.next_retry_date 
       FROM subscriptions s
       JOIN dunning d ON s.id = d.subscription_id
       WHERE d.status = 'in_dunning'
       AND d.next_retry_date <= NOW()`
    );
    return result.rows;
  }
  
  private async getExpiringGracePeriods(): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM subscriptions 
       WHERE grace_period_end_date <= NOW() + INTERVAL '1 day'
       AND grace_period_end_date > NOW()`
    );
    return result.rows;
  }
  
  private async getSubscriptionsDueForRenewal(): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM subscriptions 
       WHERE status = 'active'
       AND current_period_end <= NOW() + INTERVAL '1 day'`
    );
    return result.rows;
  }
  
  private async processSubscriptionBilling(subscription: any): Promise<void> {
    // Implement billing logic
    console.log(`Processing billing for subscription ${subscription.id}`);
  }
  
  private async processRetry(retry: any): Promise<void> {
    // Implement retry logic
    console.log(`Processing retry for subscription ${retry.subscription_id}`);
  }
  
  private async handleExpiringGracePeriod(subscription: any): Promise<void> {
    // Implement grace period handling
    console.log(`Handling expiring grace period for subscription ${subscription.id}`);
  }
  
  private async processRenewal(subscription: any): Promise<void> {
    // Implement renewal logic
    console.log(`Processing renewal for subscription ${subscription.id}`);
  }
}
```

---

## Billing Notifications

### Notification Service

```typescript
// billing-notifications.ts
import { Pool } from 'pg';

export enum NotificationType {
  BILLING_UPCOMING = 'billing_upcoming',
  PAYMENT_FAILED = 'payment_failed',
  PAYMENT_SUCCESS = 'payment_success',
  SUBSCRIPTION_EXPIRING = 'subscription_expiring',
  GRACE_PERIOD_ENDING = 'grace_period_ending',
  INVOICE_READY = 'invoice_ready'
}

export class BillingNotificationService {
  constructor(private pool: Pool) {}
  
  async sendUpcomingBillingNotification(
    subscriptionId: string,
    billingDate: Date,
    amount: number
  ): Promise<void> {
    const subscription = await this.getSubscription(subscriptionId);
    const user = await this.getUser(subscription.user_id);
    
    const message = this.buildUpcomingBillingMessage(user, billingDate, amount);
    
    await this.sendNotification(user.email, 'Upcoming Billing', message);
    await this.logNotification(subscriptionId, NotificationType.BILLING_UPCOMING);
  }
  
  async sendPaymentFailedNotification(
    subscriptionId: string,
    errorMessage: string
  ): Promise<void> {
    const subscription = await this.getSubscription(subscriptionId);
    const user = await this.getUser(subscription.user_id);
    
    const message = this.buildPaymentFailedMessage(user, errorMessage);
    
    await this.sendNotification(user.email, 'Payment Failed', message);
    await this.logNotification(subscriptionId, NotificationType.PAYMENT_FAILED);
  }
  
  async sendPaymentSuccessNotification(
    subscriptionId: string,
    amount: number
  ): Promise<void> {
    const subscription = await this.getSubscription(subscriptionId);
    const user = await this.getUser(subscription.user_id);
    
    const message = this.buildPaymentSuccessMessage(user, amount);
    
    await this.sendNotification(user.email, 'Payment Successful', message);
    await this.logNotification(subscriptionId, NotificationType.PAYMENT_SUCCESS);
  }
  
  async sendSubscriptionExpiringNotification(
    subscriptionId: string,
    expiryDate: Date
  ): Promise<void> {
    const subscription = await this.getSubscription(subscriptionId);
    const user = await this.getUser(subscription.user_id);
    
    const message = this.buildSubscriptionExpiringMessage(user, expiryDate);
    
    await this.sendNotification(user.email, 'Subscription Expiring', message);
    await this.logNotification(subscriptionId, NotificationType.SUBSCRIPTION_EXPIRING);
  }
  
  async sendGracePeriodEndingNotification(
    subscriptionId: string,
    endDate: Date
  ): Promise<void> {
    const subscription = await this.getSubscription(subscriptionId);
    const user = await this.getUser(subscription.user_id);
    
    const message = this.buildGracePeriodEndingMessage(user, endDate);
    
    await this.sendNotification(user.email, 'Grace Period Ending', message);
    await this.logNotification(subscriptionId, NotificationType.GRACE_PERIOD_ENDING);
  }
  
  async sendInvoiceReadyNotification(
    subscriptionId: string,
    invoiceId: string
  ): Promise<void> {
    const subscription = await this.getSubscription(subscriptionId);
    const user = await this.getUser(subscription.user_id);
    
    const message = this.buildInvoiceReadyMessage(user, invoiceId);
    
    await this.sendNotification(user.email, 'Invoice Ready', message);
    await this.logNotification(subscriptionId, NotificationType.INVOICE_READY);
  }
  
  private buildUpcomingBillingMessage(
    user: any,
    billingDate: Date,
    amount: number
  ): string {
    return `Dear ${user.name},
    
Your subscription will be billed on ${billingDate.toLocaleDateString()}.
Amount: $${amount.toFixed(2)}

Please ensure your payment method is up to date.

Best regards,
The Team`;
  }
  
  private buildPaymentFailedMessage(
    user: any,
    errorMessage: string
  ): string {
    return `Dear ${user.name},
    
We were unable to process your payment.
Error: ${errorMessage}

Please update your payment method to avoid service interruption.

Best regards,
The Team`;
  }
  
  private buildPaymentSuccessMessage(
    user: any,
    amount: number
  ): string {
    return `Dear ${user.name},
    
Your payment of $${amount.toFixed(2)} was successful.
Thank you for your continued subscription!

Best regards,
The Team`;
  }
  
  private buildSubscriptionExpiringMessage(
    user: any,
    expiryDate: Date
  ): string {
    return `Dear ${user.name},
    
Your subscription will expire on ${expiryDate.toLocaleDateString()}.
Renew now to continue enjoying our services.

Best regards,
The Team`;
  }
  
  private buildGracePeriodEndingMessage(
    user: any,
    endDate: Date
  ): string {
    return `Dear ${user.name},
    
Your grace period will end on ${endDate.toLocaleDateString()}.
Please update your payment method to avoid service interruption.

Best regards,
The Team`;
  }
  
  private buildInvoiceReadyMessage(
    user: any,
    invoiceId: string
  ): string {
    return `Dear ${user.name},
    
Your invoice ${invoiceId} is now available.
You can view and download it from your account.

Best regards,
The Team`;
  }
  
  private async sendNotification(
    email: string,
    subject: string,
    message: string
  ): Promise<void> {
    // Implement email sending
    console.log(`Sending email to ${email}: ${subject}`);
  }
  
  private async logNotification(
    subscriptionId: string,
    type: NotificationType
  ): Promise<void> {
    await this.pool.query(
      `INSERT INTO billing_notifications (subscription_id, type, created_at)
       VALUES ($1, $2, NOW())`,
      [subscriptionId, type]
    );
  }
  
  private async getSubscription(subscriptionId: string): Promise<any> {
    const result = await this.pool.query(
      'SELECT * FROM subscriptions WHERE id = $1',
      [subscriptionId]
    );
    return result.rows[0];
  }
  
  private async getUser(userId: string): Promise<any> {
    const result = await this.pool.query(
      'SELECT * FROM users WHERE id = $1',
      [userId]
    );
    return result.rows[0];
  }
}

// SQL table
/*
CREATE TABLE billing_notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  subscription_id UUID NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,
  sent_at TIMESTAMP DEFAULT NOW()
);
*/
```

---

## Testing Billing Cycles

### Test Utilities

```typescript
// billing-cycle-tests.ts
import { BillingCycleType, BillingPeriod } from './billing-cycle-types';
import { BillingCycleCalculator } from './cycle-calculator';
import { ProrationCalculator } from './proration-calculator';

export class BillingCycleTestUtils {
  static testMonthlyCycle(anchorDate: Date, currentDate: Date): void {
    const nextDate = BillingCycleCalculator.calculateNextBillingDate(
      BillingCycleType.MONTHLY,
      anchorDate,
      currentDate
    );
    
    console.log(`Monthly cycle test:`);
    console.log(`  Anchor date: ${anchorDate.toISOString()}`);
    console.log(`  Current date: ${currentDate.toISOString()}`);
    console.log(`  Next billing date: ${nextDate.toISOString()}`);
  }
  
  static testYearlyCycle(anchorDate: Date, currentDate: Date): void {
    const nextDate = BillingCycleCalculator.calculateNextBillingDate(
      BillingCycleType.YEARLY,
      anchorDate,
      currentDate
    );
    
    console.log(`Yearly cycle test:`);
    console.log(`  Anchor date: ${anchorDate.toISOString()}`);
    console.log(`  Current date: ${currentDate.toISOString()}`);
    console.log(`  Next billing date: ${nextDate.toISOString()}`);
  }
  
  static testProration(
    amount: number,
    billingPeriod: BillingPeriod,
    currentDate: Date
  ): void {
    const proration = ProrationCalculator.calculateProration(
      amount,
      billingPeriod,
      currentDate
    );
    
    console.log(`Proration test:`);
    console.log(`  Amount: $${amount}`);
    console.log(`  Days in period: ${proration.daysInPeriod}`);
    console.log(`  Days remaining: ${proration.daysRemaining}`);
    console.log(`  Proration factor: ${proration.prorationFactor.toFixed(4)}`);
    console.log(`  Prorated amount: $${proration.proratedAmount.toFixed(2)}`);
    console.log(`  Credit amount: $${proration.creditAmount.toFixed(2)}`);
  }
  
  static testUpgradeProration(
    oldAmount: number,
    newAmount: number,
    billingPeriod: BillingPeriod,
    currentDate: Date
  ): void {
    const proration = ProrationCalculator.calculateUpgradeProration(
      oldAmount,
      newAmount,
      billingPeriod,
      currentDate
    );
    
    console.log(`Upgrade proration test:`);
    console.log(`  Old amount: $${oldAmount}`);
    console.log(`  New amount: $${newAmount}`);
    console.log(`  Days in period: ${proration.daysInPeriod}`);
    console.log(`  Days remaining: ${proration.daysRemaining}`);
    console.log(`  Credit amount: $${proration.creditAmount.toFixed(2)}`);
    console.log(`  Charge amount: $${proration.chargeAmount.toFixed(2)}`);
    console.log(`  Net prorated amount: $${proration.proratedAmount.toFixed(2)}`);
  }
}

// Run tests
const anchorDate = new Date('2024-01-15');
const currentDate = new Date('2024-06-10');
const billingPeriod = {
  start: new Date('2024-05-15'),
  end: new Date('2024-06-15'),
  days: 31
};

BillingCycleTestUtils.testMonthlyCycle(anchorDate, currentDate);
BillingCycleTestUtils.testYearlyCycle(anchorDate, currentDate);
BillingCycleTestUtils.testProration(100, billingPeriod, currentDate);
BillingCycleTestUtils.testUpgradeProration(50, 100, billingPeriod, currentDate);
```

---

## Edge Cases

### Edge Case Handling

```typescript
// edge-cases.ts
export class EdgeCaseHandler {
  static handleLeapYear(date: Date): Date {
    const year = date.getFullYear();
    const isLeapYear = (year % 4 === 0 && year % 100 !== 0) || (year % 400 === 0);
    
    if (!isLeapYear && date.getMonth() === 1 && date.getDate() === 29) {
      const adjusted = new Date(date);
      adjusted.setDate(28);
      return adjusted;
    }
    
    return new Date(date);
  }
  
  static handleMonthEnd(date: Date): Date {
    const lastDayOfMonth = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    
    if (date.getDate() > lastDayOfMonth) {
      const adjusted = new Date(date);
      adjusted.setDate(lastDayOfMonth);
      return adjusted;
    }
    
    return new Date(date);
  }
  
  static handleDaylightSaving(date: Date): Date {
    // Handle DST transitions by using UTC
    return new Date(date.toISOString());
  }
  
  static handleTimezone(date: Date, timezone: string): Date {
    // Convert to specific timezone
    return new Date(date.toLocaleString('en-US', { timeZone: timezone }));
  }
  
  static handleShortMonth(anchorDate: Date, currentDate: Date): Date {
    const lastDayOfMonth = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0).getDate();
    const anchorDay = Math.min(anchorDate.getDate(), lastDayOfMonth);
    
    const adjusted = new Date(currentDate);
    adjusted.setDate(anchorDay);
    
    return adjusted;
  }
}
```

---

## Additional Resources

- [Stripe Billing Cycles](https://stripe.com/docs/billing/subscriptions/billing-cycle)
- [Proration Best Practices](https://stripe.com/docs/billing/subscriptions/prorations)
- [Dunning Management](https://stripe.com/docs/billing/subscriptions/overview#dunning)
- [Payment Retry Logic](https://stripe.com/docs/billing/subscriptions/overview#payment-retry)
