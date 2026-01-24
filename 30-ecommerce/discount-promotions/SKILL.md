---
name: Discount and Promotion Engine
description: Managing coupon codes, promotional rules, discount calculations, validation, stacking rules, usage limits, and analytics for e-commerce platforms with flexible promotion system.
---

# Discount and Promotion Engine

> **Current Level:** Intermediate  
> **Domain:** E-commerce / Backend

---

## Overview

Discount and promotion engine manages coupon codes, promotional rules, discount calculations, validation, and analytics for e-commerce platforms. Effective promotion systems support multiple discount types, stacking rules, eligibility checks, and usage limits.

---

## Core Concepts

### Table of Contents

1. [Discount Types](#discount-types)
2. [Coupon Codes](#coupon-codes)
3. [Promotion Rules](#promotion-rules)
4. [Stacking Rules](#stacking-rules)
5. [Date/Time Restrictions](#datetime-restrictions)
6. [User Eligibility](#user-eligibility)
7. [Usage Limits](#usage-limits)
8. [Database Schema](#database-schema)
9. [Calculation Engine](#calculation-engine)
10. [Validation](#validation)
11. [Analytics](#analytics)
12. [A/B Testing Promotions](#ab-testing-promotions)
13. [Best Practices](#best-practices)

---

## Discount Types

### Discount Types

```typescript
enum DiscountType {
  PERCENTAGE = 'percentage',
  FIXED_AMOUNT = 'fixed_amount',
  BUY_X_GET_Y = 'buy_x_get_y',
  FREE_SHIPPING = 'free_shipping',
}

enum DiscountScope {
  CART = 'cart',
  PRODUCT = 'product',
  CATEGORY = 'category',
  BRAND = 'brand',
  USER = 'user',
}

enum DiscountApplication {
  AUTOMATIC = 'automatic',  // Applied automatically
  CODE = 'code',          // Requires coupon code
}

enum DiscountStatus {
  ACTIVE = 'active',
  SCHEDULED = 'scheduled',
  EXPIRED = 'expired',
  PAUSED = 'paused',
}
```

---

## Coupon Codes

### Coupon Manager

```typescript
class CouponManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create coupon
   */
  async createCoupon(params: {
    code: string;
    type: DiscountType;
    value: number;
    scope: DiscountScope;
    scopeIds?: string[];
    minOrderAmount?: number;
    maxOrderAmount?: number;
    maxDiscountAmount?: number;
    startDate?: Date;
    endDate?: Date;
    usageLimit?: number;
    usageLimitPerUser?: number;
    userSegmentIds?: string[];
    autoApply?: boolean;
    stackable?: boolean;
  }): Promise<Coupon> {
    // Validate code uniqueness
    const existing = await this.prisma.coupon.findUnique({
      where: { code: params.code },
    });

    if (existing) {
      throw new Error('Coupon code already exists');
    }

    return await this.prisma.coupon.create({
      data: {
        code: params.code,
        type: params.type,
        value: params.value,
        scope: params.scope,
        scopeIds: params.scopeIds,
        minOrderAmount: params.minOrderAmount,
        maxOrderAmount: params.maxOrderAmount,
        maxDiscountAmount: params.maxDiscountAmount,
        startDate: params.startDate,
        endDate: params.endDate,
        usageLimit: params.usageLimit,
        usageLimitPerUser: params.usageLimitPerUser,
        userSegmentIds: params.userSegmentIds,
        autoApply: params.autoApply || false,
        stackable: params.stackable || false,
        status: params.startDate && params.startDate > new Date()
          ? DiscountStatus.SCHEDULED
          : DiscountStatus.ACTIVE,
      },
    });
  }

  /**
   * Generate coupon codes
   */
  async generateCoupons(params: {
    prefix?: string;
    suffix?: string;
    length: number;
    count: number;
    type: DiscountType;
    value: number;
    scope: DiscountScope;
    usageLimit?: number;
    startDate?: Date;
    endDate?: Date;
  }): Promise<Coupon[]> {
    const coupons: Coupon[] = [];

    for (let i = 0; i < params.count; i++) {
      const code = this.generateCode({
        prefix: params.prefix,
        suffix: params.suffix,
        length: params.length,
      });

      const coupon = await this.createCoupon({
        code,
        type: params.type,
        value: params.value,
        scope: params.scope,
        usageLimit: params.usageLimit,
        startDate: params.startDate,
        endDate: params.endDate,
      });

      coupons.push(coupon);
    }

    return coupons;
  }

  /**
   * Generate code
   */
  private generateCode(params: {
    prefix?: string;
    suffix?: string;
    length: number;
  }): string {
    const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    let code = '';

    for (let i = 0; i < params.length; i++) {
      code += chars.charAt(Math.floor(Math.random() * chars.length));
    }

    return `${params.prefix || ''}${code}${params.suffix || ''}`;
  }

  /**
   * Validate coupon
   */
  async validateCoupon(params: {
    code: string;
    userId?: string;
    cartTotal: number;
    cartItems: Array<{
      productId: string;
      categoryId?: string;
      brandId?: string;
      quantity: number;
      price: number;
    }>;
  }): Promise<{
    valid: boolean;
    coupon?: Coupon;
    error?: string;
  }> {
    const coupon = await this.prisma.coupon.findUnique({
      where: { code: params.code },
    });

    if (!coupon) {
      return { valid: false, error: 'Invalid coupon code' };
    }

    // Check status
    if (coupon.status !== DiscountStatus.ACTIVE) {
      return { valid: false, error: 'Coupon is not active' };
    }

    // Check dates
    const now = new Date();
    if (coupon.startDate && now < coupon.startDate) {
      return { valid: false, error: 'Coupon is not yet active' };
    }

    if (coupon.endDate && now > coupon.endDate) {
      return { valid: false, error: 'Coupon has expired' };
    }

    // Check usage limit
    if (coupon.usageLimit && coupon.usedCount >= coupon.usageLimit) {
      return { valid: false, error: 'Coupon usage limit reached' };
    }

    // Check usage limit per user
    if (params.userId && coupon.usageLimitPerUser) {
      const userUsage = await this.prisma.couponUsage.count({
        where: {
          couponId: coupon.id,
          userId: params.userId,
        },
      });

      if (userUsage >= coupon.usageLimitPerUser) {
        return { valid: false, error: 'You have used this coupon the maximum number of times' };
      }
    }

    // Check user segments
    if (coupon.userSegmentIds && coupon.userSegmentIds.length > 0) {
      if (!params.userId) {
        return { valid: false, error: 'You must be logged in to use this coupon' };
      }

      const userSegments = await this.getUserSegments(params.userId);
      const hasRequiredSegment = coupon.userSegmentIds.some(segment =>
        userSegments.includes(segment)
      );

      if (!hasRequiredSegment) {
        return { valid: false, error: 'You are not eligible for this coupon' };
      }
    }

    // Check minimum order amount
    if (coupon.minOrderAmount && params.cartTotal < coupon.minOrderAmount) {
      return {
        valid: false,
        error: `Minimum order amount of ${coupon.minOrderAmount} required`,
      };
    }

    // Check maximum order amount
    if (coupon.maxOrderAmount && params.cartTotal > coupon.maxOrderAmount) {
      return {
        valid: false,
        error: `Maximum order amount of ${coupon.maxOrderAmount} exceeded`,
      };
    }

    // Check scope
    if (coupon.scope !== DiscountScope.CART) {
      const hasEligibleItem = params.cartItems.some(item => {
        switch (coupon.scope) {
          case DiscountScope.PRODUCT:
            return coupon.scopeIds?.includes(item.productId);
          case DiscountScope.CATEGORY:
            return item.categoryId && coupon.scopeIds?.includes(item.categoryId);
          case DiscountScope.BRAND:
            return item.brandId && coupon.scopeIds?.includes(item.brandId);
          default:
            return false;
        }
      });

      if (!hasEligibleItem) {
        return { valid: false, error: 'Coupon does not apply to any items in your cart' };
      }
    }

    return { valid: true, coupon };
  }

  /**
   * Get user segments
   */
  private async getUserSegments(userId: string): Promise<string[]> {
    // Implement user segmentation
    return [];
  }

  /**
   * Apply coupon
   */
  async applyCoupon(params: {
    code: string;
    userId?: string;
    orderId: string;
  }): Promise<void> {
    const validation = await this.validateCoupon({
      code: params.code,
      userId: params.userId,
      cartTotal: 0, // Will be calculated from order
      cartItems: [],
    });

    if (!validation.valid || !validation.coupon) {
      throw new Error(validation.error);
    }

    // Record usage
    await this.prisma.couponUsage.create({
      data: {
        couponId: validation.coupon.id,
        userId: params.userId,
        orderId: params.orderId,
        usedAt: new Date(),
      },
    });

    // Update coupon usage count
    await this.prisma.coupon.update({
      where: { id: validation.coupon.id },
      data: { usedCount: { increment: 1 } },
    });
  }

  /**
   * Get coupons
   */
  async getCoupons(params?: {
    status?: DiscountStatus;
    userId?: string;
  }): Promise<Coupon[]> {
    const where: any = {};

    if (params?.status) {
      where.status = params.status;
    }

    if (params?.userId) {
      where.userSegmentIds = {
        has: await this.getUserSegments(params.userId),
      };
    }

    return await this.prisma.coupon.findMany({
      where,
      orderBy: { createdAt: 'desc' },
    });
  }
}
```

---

## Promotion Rules

### Promotion Manager

```typescript
class PromotionManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create promotion
   */
  async createPromotion(params: {
    name: string;
    description?: string;
    type: DiscountType;
    value: number;
    scope: DiscountScope;
    scopeIds?: string[];
    conditions: PromotionCondition[];
    minOrderAmount?: number;
    maxOrderAmount?: number;
    maxDiscountAmount?: number;
    startDate: Date;
    endDate: Date;
    userSegmentIds?: string[];
    priority?: number;
    stackable?: boolean;
  }): Promise<Promotion> {
    return await this.prisma.$transaction(async (tx) => {
      // Create promotion
      const promotion = await tx.promotion.create({
        data: {
          name: params.name,
          description: params.description,
          type: params.type,
          value: params.value,
          scope: params.scope,
          scopeIds: params.scopeIds,
          minOrderAmount: params.minOrderAmount,
          maxOrderAmount: params.maxOrderAmount,
          maxDiscountAmount: params.maxDiscountAmount,
          startDate: params.startDate,
          endDate: params.endDate,
          userSegmentIds: params.userSegmentIds,
          priority: params.priority || 0,
          stackable: params.stackable || false,
          status: params.startDate > new Date()
            ? DiscountStatus.SCHEDULED
            : DiscountStatus.ACTIVE,
        },
      });

      // Create conditions
      for (const condition of params.conditions) {
        await tx.promotionCondition.create({
          data: {
            promotionId: promotion.id,
            type: condition.type,
            operator: condition.operator,
            value: condition.value,
            scopeId: condition.scopeId,
          },
        });
      }

      return promotion;
    });
  }

  /**
   * Get applicable promotions
   */
  async getApplicablePromotions(params: {
    userId?: string;
    cartTotal: number;
    cartItems: Array<{
      productId: string;
      categoryId?: string;
      brandId?: string;
      quantity: number;
      price: number;
    }>;
  }): Promise<Promotion[]> {
    const where: any = {
      status: DiscountStatus.ACTIVE,
      startDate: { lte: new Date() },
      endDate: { gte: new Date() },
    };

    // Check user segments
    if (params.userId) {
      const userSegments = await this.getUserSegments(params.userId);
      where.OR = [
        { userSegmentIds: { isEmpty: true } },
        { userSegmentIds: { hasSome: userSegments } },
      ];
    }

    const promotions = await this.prisma.promotion.findMany({
      where,
      include: { conditions: true },
      orderBy: { priority: 'desc' },
    });

    // Filter by conditions
    return promotions.filter(promotion =>
      this.matchesConditions(promotion, params)
    );
  }

  /**
   * Check if promotion matches conditions
   */
  private matchesConditions(
    promotion: Promotion,
    params: {
      cartTotal: number;
      cartItems: Array<{
        productId: string;
        categoryId?: string;
        brandId?: string;
        quantity: number;
        price: number;
      }>;
    }
  ): boolean {
    // Check min/max order amount
    if (promotion.minOrderAmount && params.cartTotal < promotion.minOrderAmount) {
      return false;
    }

    if (promotion.maxOrderAmount && params.cartTotal > promotion.maxOrderAmount) {
      return false;
    }

    // Check conditions
    for (const condition of promotion.conditions) {
      if (!this.matchesCondition(condition, params)) {
        return false;
      }
    }

    return true;
  }

  /**
   * Check if condition matches
   */
  private matchesCondition(
    condition: PromotionCondition,
    params: {
      cartTotal: number;
      cartItems: Array<{
        productId: string;
        categoryId?: string;
        brandId?: string;
        quantity: number;
        price: number;
      }>;
    }
  ): boolean {
    switch (condition.type) {
      case 'cart_total':
        return this.compareValue(params.cartTotal, condition.operator, condition.value);

      case 'product_quantity':
        const item = params.cartItems.find(i => i.productId === condition.scopeId);
        return item ? this.compareValue(item.quantity, condition.operator, condition.value) : false;

      case 'category_quantity':
        const categoryItems = params.cartItems.filter(i =>
          i.categoryId === condition.scopeId
        );
        const categoryQuantity = categoryItems.reduce((sum, i) => sum + i.quantity, 0);
        return this.compareValue(categoryQuantity, condition.operator, condition.value);

      case 'product_in_cart':
        return params.cartItems.some(i => i.productId === condition.scopeId);

      case 'category_in_cart':
        return params.cartItems.some(i => i.categoryId === condition.scopeId);

      default:
        return true;
    }
  }

  /**
   * Compare values
   */
  private compareValue(
    actual: number,
    operator: string,
    expected: number
  ): boolean {
    switch (operator) {
      case 'eq':
        return actual === expected;
      case 'gt':
        return actual > expected;
      case 'gte':
        return actual >= expected;
      case 'lt':
        return actual < expected;
      case 'lte':
        return actual <= expected;
      default:
        return false;
    }
  }

  /**
   * Get user segments
   */
  private async getUserSegments(userId: string): Promise<string[]> {
    // Implement user segmentation
    return [];
  }
}
```

---

## Stacking Rules

### Stacking Manager

```typescript
class StackingManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get applicable discounts
   */
  async getApplicableDiscounts(params: {
    userId?: string;
    cartTotal: number;
    cartItems: Array<{
      productId: string;
      categoryId?: string;
      brandId?: string;
      quantity: number;
      price: number;
    }>;
    couponCodes?: string[];
  }): Promise<Discount[]> {
    const discounts: Discount[] = [];

    // Get applicable coupons
    if (params.couponCodes && params.couponCodes.length > 0) {
      const couponManager = new CouponManager(this.prisma);

      for (const code of params.couponCodes) {
        const validation = await couponManager.validateCoupon({
          code,
          userId: params.userId,
          cartTotal: params.cartTotal,
          cartItems: params.cartItems,
        });

        if (validation.valid && validation.coupon) {
          discounts.push({
            id: validation.coupon.id,
            type: validation.coupon.type,
            value: validation.coupon.value,
            scope: validation.coupon.scope,
            scopeIds: validation.coupon.scopeIds,
            maxDiscountAmount: validation.coupon.maxDiscountAmount,
            stackable: validation.coupon.stackable,
            source: 'coupon',
            name: validation.coupon.code,
          });
        }
      }
    }

    // Get applicable promotions
    const promotionManager = new PromotionManager(this.prisma);
    const promotions = await promotionManager.getApplicablePromotions(params);

    for (const promotion of promotions) {
      discounts.push({
        id: promotion.id,
        type: promotion.type,
        value: promotion.value,
        scope: promotion.scope,
        scopeIds: promotion.scopeIds,
        maxDiscountAmount: promotion.maxDiscountAmount,
        stackable: promotion.stackable,
        source: 'promotion',
        name: promotion.name,
      });
    }

    // Apply stacking rules
    return this.applyStackingRules(discounts);
  }

  /**
   * Apply stacking rules
   */
  private applyStackingRules(discounts: Discount[]): Discount[] {
    const stackingConfig = this.getStackingConfig();
    const result: Discount[] = [];

    // Separate by type
    const percentageDiscounts = discounts.filter(d => d.type === DiscountType.PERCENTAGE);
    const fixedDiscounts = discounts.filter(d => d.type === DiscountType.FIXED_AMOUNT);
    const freeShipping = discounts.find(d => d.type === DiscountType.FREE_SHIPPING);

    // Apply percentage discounts (only best one if not stackable)
    if (percentageDiscounts.length > 0) {
      if (stackingConfig.allowPercentageStacking) {
        result.push(...percentageDiscounts.filter(d => d.stackable));
      } else {
        const best = percentageDiscounts.reduce((best, current) =>
          current.value > best.value ? current : best
        );
        result.push(best);
      }
    }

    // Apply fixed discounts (only best one if not stackable)
    if (fixedDiscounts.length > 0) {
      if (stackingConfig.allowFixedStacking) {
        result.push(...fixedDiscounts.filter(d => d.stackable));
      } else {
        const best = fixedDiscounts.reduce((best, current) =>
          current.value > best.value ? current : best
        );
        result.push(best);
      }
    }

    // Apply free shipping
    if (freeShipping) {
      result.push(freeShipping);
    }

    return result;
  }

  /**
   * Get stacking config
   */
  private getStackingConfig(): {
    allowPercentageStacking: boolean;
    allowFixedStacking: boolean;
    allowMixedStacking: boolean;
    maxStackedDiscounts: number;
  } {
    return {
      allowPercentageStacking: false,
      allowFixedStacking: false,
      allowMixedStacking: true,
      maxStackedDiscounts: 2,
    };
  }
}
```

---

## Date/Time Restrictions

### Date Restriction Manager

```typescript
class DateRestrictionManager {
  /**
   * Check if discount is active
   */
  isDiscountActive(discount: {
    startDate?: Date;
    endDate?: Date;
    activeDays?: number[]; // 0-6 (Sunday-Saturday)
    activeHours?: { start: number; end: number };
  }): boolean {
    const now = new Date();

    // Check date range
    if (discount.startDate && now < discount.startDate) {
      return false;
    }

    if (discount.endDate && now > discount.endDate) {
      return false;
    }

    // Check active days
    if (discount.activeDays && discount.activeDays.length > 0) {
      const dayOfWeek = now.getDay();
      if (!discount.activeDays.includes(dayOfWeek)) {
        return false;
      }
    }

    // Check active hours
    if (discount.activeHours) {
      const hour = now.getHours();
      if (hour < discount.activeHours.start || hour >= discount.activeHours.end) {
        return false;
      }
    }

    return true;
  }

  /**
   * Check if discount is scheduled
   */
  isDiscountScheduled(discount: {
    startDate?: Date;
  }): boolean {
    if (!discount.startDate) {
      return false;
    }

    return new Date() < discount.startDate;
  }

  /**
   * Check if discount is expired
   */
  isDiscountExpired(discount: {
    endDate?: Date;
  }): boolean {
    if (!discount.endDate) {
      return false;
    }

    return new Date() > discount.endDate;
  }

  /**
   * Get active discounts
   */
  async getActiveDiscounts<T extends { startDate?: Date; endDate?: Date }>(
    discounts: T[]
  ): Promise<T[]> {
    return discounts.filter(discount =>
      this.isDiscountActive(discount)
    );
  }
}
```

---

## User Eligibility

### Eligibility Manager

```typescript
class EligibilityManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Check user eligibility
   */
  async checkEligibility(params: {
    userId?: string;
    discount: {
      userSegmentIds?: string[];
      minOrders?: number;
      minTotalSpent?: number;
      firstOrderOnly?: boolean;
      newCustomersOnly?: boolean;
    };
  }): Promise<{
    eligible: boolean;
    reason?: string;
  }> {
    // If no user ID, check if guest eligible
    if (!params.userId) {
      if (params.discount.newCustomersOnly) {
        return { eligible: true };
      }

      if (params.discount.userSegmentIds && params.discount.userSegmentIds.length > 0) {
        return { eligible: false, reason: 'You must be logged in to use this discount' };
      }

      return { eligible: true };
    }

    // Get user data
    const user = await this.prisma.user.findUnique({
      where: { id: params.userId },
      include: {
        orders: {
          where: { status: OrderStatus.DELIVERED },
        },
      },
    });

    if (!user) {
      return { eligible: false, reason: 'User not found' };
    }

    // Check first order only
    if (params.discount.firstOrderOnly && user.orders.length > 0) {
      return { eligible: false, reason: 'This discount is only for first orders' };
    }

    // Check new customers only
    if (params.discount.newCustomersOnly) {
      const accountAge = Date.now() - user.createdAt.getTime();
      const thirtyDays = 30 * 24 * 60 * 60 * 1000;

      if (accountAge > thirtyDays) {
        return { eligible: false, reason: 'This discount is for new customers only' };
      }
    }

    // Check minimum orders
    if (params.discount.minOrders && user.orders.length < params.discount.minOrders) {
      return {
        eligible: false,
        reason: `You need at least ${params.discount.minOrders} orders to use this discount`,
      };
    }

    // Check minimum total spent
    if (params.discount.minTotalSpent) {
      const totalSpent = user.orders.reduce((sum, order) => sum + Number(order.total), 0);

      if (totalSpent < params.discount.minTotalSpent) {
        return {
          eligible: false,
          reason: `You need to spend at least ${params.discount.minTotalSpent} to use this discount`,
        };
      }
    }

    // Check user segments
    if (params.discount.userSegmentIds && params.discount.userSegmentIds.length > 0) {
      const userSegments = await this.getUserSegments(params.userId);
      const hasRequiredSegment = params.discount.userSegmentIds.some(segment =>
        userSegments.includes(segment)
      );

      if (!hasRequiredSegment) {
        return { eligible: false, reason: 'You are not eligible for this discount' };
      }
    }

    return { eligible: true };
  }

  /**
   * Get user segments
   */
  private async getUserSegments(userId: string): Promise<string[]> {
    // Implement user segmentation
    return [];
  }
}
```

---

## Usage Limits

### Usage Limit Manager

```typescript
class UsageLimitManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Check usage limit
   */
  async checkUsageLimit(params: {
    discountId: string;
    userId?: string;
  }): Promise<{
    canUse: boolean;
    remainingUses?: number;
    reason?: string;
  }> {
    const discount = await this.prisma.coupon.findUnique({
      where: { id: params.discountId },
    });

    if (!discount) {
      return { canUse: false, reason: 'Discount not found' };
    }

    // Check global usage limit
    if (discount.usageLimit && discount.usedCount >= discount.usageLimit) {
      return { canUse: false, reason: 'Discount usage limit reached' };
    }

    // Check per-user usage limit
    if (params.userId && discount.usageLimitPerUser) {
      const userUsage = await this.prisma.couponUsage.count({
        where: {
          couponId: params.discountId,
          userId: params.userId,
        },
      });

      if (userUsage >= discount.usageLimitPerUser) {
        return {
          canUse: false,
          reason: 'You have used this discount the maximum number of times',
        };
      }
    }

    return {
      canUse: true,
      remainingUses: discount.usageLimit
        ? discount.usageLimit - discount.usedCount
        : undefined,
    };
  }

  /**
   * Record usage
   */
  async recordUsage(params: {
    discountId: string;
    userId?: string;
    orderId: string;
  }): Promise<void> {
    await this.prisma.$transaction(async (tx) => {
      // Create usage record
      await tx.couponUsage.create({
        data: {
          couponId: params.discountId,
          userId: params.userId,
          orderId: params.orderId,
          usedAt: new Date(),
        },
      });

      // Update usage count
      await tx.coupon.update({
        where: { id: params.discountId },
        data: { usedCount: { increment: 1 } },
      });
    });
  }
}
```

---

## Database Schema

### Prisma Schema

```prisma
model Coupon {
  id                String                @id @default(uuid())
  code              String                @unique
  type              DiscountType
  value             Decimal
  scope             DiscountScope
  scopeIds          String[]
  minOrderAmount    Decimal?
  maxOrderAmount    Decimal?
  maxDiscountAmount Decimal?
  startDate         DateTime?
  endDate           DateTime?
  usageLimit        Int?
  usageLimitPerUser Int?
  usedCount         Int                   @default(0)
  userSegmentIds    String[]
  autoApply         Boolean               @default(false)
  stackable         Boolean               @default(false)
  status            DiscountStatus         @default(ACTIVE)
  createdAt         DateTime              @default(now())
  updatedAt         DateTime              @updatedAt
  usages            CouponUsage[]

  @@index([code])
  @@index([status])
  @@index([startDate, endDate])
}

model CouponUsage {
  id        String   @id @default(uuid())
  couponId  String
  coupon    Coupon   @relation(fields: [couponId], references: [id], onDelete: Cascade)
  userId    String?
  orderId   String
  usedAt    DateTime @default(now())

  @@index([couponId])
  @@index([userId])
  @@index([orderId])
}

model Promotion {
  id               String                @id @default(uuid())
  name             String
  description      String?
  type             DiscountType
  value            Decimal
  scope            DiscountScope
  scopeIds         String[]
  conditions       PromotionCondition[]
  minOrderAmount   Decimal?
  maxOrderAmount   Decimal?
  maxDiscountAmount Decimal?
  startDate        DateTime
  endDate          DateTime
  userSegmentIds   String[]
  priority         Int                   @default(0)
  stackable        Boolean               @default(false)
  status           DiscountStatus         @default(ACTIVE)
  createdAt        DateTime              @default(now())
  updatedAt        DateTime              @updatedAt

  @@index([status])
  @@index([startDate, endDate])
  @@index([priority])
}

model PromotionCondition {
  id          String   @id @default(uuid())
  promotionId String
  promotion   Promotion @relation(fields: [promotionId], references: [id], onDelete: Cascade)
  type        String   // cart_total, product_quantity, category_quantity, product_in_cart, category_in_cart
  operator    String   // eq, gt, gte, lt, lte
  value       Decimal
  scopeId     String?

  @@index([promotionId])
}

model DiscountApplication {
  id          String   @id @default(uuid())
  orderId     String
  discountId  String
  discountType String   // coupon, promotion
  amount      Decimal
  createdAt   DateTime @default(now())

  @@index([orderId])
  @@index([discountId])
}
```

---

## Calculation Engine

### Discount Calculator

```typescript
class DiscountCalculator {
  /**
   * Calculate discounts
   */
  async calculateDiscounts(params: {
    userId?: string;
    cartTotal: number;
    cartItems: Array<{
      productId: string;
      categoryId?: string;
      brandId?: string;
      quantity: number;
      price: number;
    }>;
    couponCodes?: string[];
  }): Promise<{
    discounts: Array<{
      id: string;
      name: string;
      type: DiscountType;
      amount: number;
    }>;
    totalDiscount: number;
    finalTotal: number;
  }> {
    const stackingManager = new StackingManager(prisma);
    const applicableDiscounts = await stackingManager.getApplicableDiscounts(params);

    const discounts: Array<{
      id: string;
      name: string;
      type: DiscountType;
      amount: number;
    }> = [];

    let totalDiscount = 0;

    for (const discount of applicableDiscounts) {
      const discountAmount = await this.calculateDiscountAmount(discount, params);

      if (discountAmount > 0) {
        discounts.push({
          id: discount.id,
          name: discount.name,
          type: discount.type,
          amount: discountAmount,
        });

        totalDiscount += discountAmount;
      }
    }

    // Apply max discount cap
    for (const discount of applicableDiscounts) {
      if (discount.maxDiscountAmount) {
        const discountIndex = discounts.findIndex(d => d.id === discount.id);
        if (discountIndex >= 0) {
          discounts[discountIndex].amount = Math.min(
            discounts[discountIndex].amount,
            Number(discount.maxDiscountAmount)
          );
        }
      }
    }

    // Recalculate total
    totalDiscount = discounts.reduce((sum, d) => sum + d.amount, 0);

    return {
      discounts,
      totalDiscount,
      finalTotal: params.cartTotal - totalDiscount,
    };
  }

  /**
   * Calculate discount amount
   */
  private async calculateDiscountAmount(
    discount: Discount,
    params: {
      cartTotal: number;
      cartItems: Array<{
        productId: string;
        categoryId?: string;
        brandId?: string;
        quantity: number;
        price: number;
      }>;
    }
  ): Promise<number> {
    switch (discount.type) {
      case DiscountType.PERCENTAGE:
        return this.calculatePercentageDiscount(discount, params);

      case DiscountType.FIXED_AMOUNT:
        return this.calculateFixedDiscount(discount, params);

      case DiscountType.BUY_X_GET_Y:
        return this.calculateBuyXGetYDiscount(discount, params);

      case DiscountType.FREE_SHIPPING:
        return 0; // Handled separately

      default:
        return 0;
    }
  }

  /**
   * Calculate percentage discount
   */
  private calculatePercentageDiscount(
    discount: Discount,
    params: { cartTotal: number; cartItems: any[] }
  ): number {
    if (discount.scope === DiscountScope.CART) {
      return params.cartTotal * (Number(discount.value) / 100);
    }

    // Calculate for specific items
    let discountAmount = 0;

    for (const item of params.cartItems) {
      if (this.isItemEligible(item, discount)) {
        discountAmount += item.price * item.quantity * (Number(discount.value) / 100);
      }
    }

    return discountAmount;
  }

  /**
   * Calculate fixed discount
   */
  private calculateFixedDiscount(
    discount: Discount,
    params: { cartTotal: number; cartItems: any[] }
  ): number {
    if (discount.scope === DiscountScope.CART) {
      return Number(discount.value);
    }

    // Calculate for specific items
    let discountAmount = 0;

    for (const item of params.cartItems) {
      if (this.isItemEligible(item, discount)) {
        discountAmount += Number(discount.value) * item.quantity;
      }
    }

    return discountAmount;
  }

  /**
   * Calculate buy X get Y discount
   */
  private calculateBuyXGetYDiscount(
    discount: Discount,
    params: { cartItems: any[] }
  ): number {
    // Implement buy X get Y logic
    return 0;
  }

  /**
   * Check if item is eligible
   */
  private isItemEligible(
    item: any,
    discount: Discount
  ): boolean {
    if (!discount.scopeIds || discount.scopeIds.length === 0) {
      return true;
    }

    switch (discount.scope) {
      case DiscountScope.PRODUCT:
        return discount.scopeIds.includes(item.productId);
      case DiscountScope.CATEGORY:
        return item.categoryId && discount.scopeIds.includes(item.categoryId);
      case DiscountScope.BRAND:
        return item.brandId && discount.scopeIds.includes(item.brandId);
      default:
        return false;
    }
  }
}
```

---

## Validation

### Discount Validator

```typescript
class DiscountValidator {
  constructor(private prisma: PrismaClient) {}

  /**
   * Validate discount
   */
  async validateDiscount(params: {
    discountId: string;
    userId?: string;
    cartTotal: number;
    cartItems: Array<{
      productId: string;
      categoryId?: string;
      brandId?: string;
      quantity: number;
      price: number;
    }>;
  }): Promise<{
    valid: boolean;
    errors: string[];
  }> {
    const errors: string[] = [];

    const discount = await this.prisma.coupon.findUnique({
      where: { id: params.discountId },
    });

    if (!discount) {
      errors.push('Discount not found');
      return { valid: false, errors };
    }

    // Check status
    if (discount.status !== DiscountStatus.ACTIVE) {
      errors.push('Discount is not active');
    }

    // Check dates
    const dateManager = new DateRestrictionManager();

    if (!dateManager.isDiscountActive(discount)) {
      if (dateManager.isDiscountScheduled(discount)) {
        errors.push('Discount is not yet active');
      } else if (dateManager.isDiscountExpired(discount)) {
        errors.push('Discount has expired');
      } else {
        errors.push('Discount is not currently active');
      }
    }

    // Check usage limits
    const usageManager = new UsageLimitManager(this.prisma);
    const usageCheck = await usageManager.checkUsageLimit({
      discountId: params.discountId,
      userId: params.userId,
    });

    if (!usageCheck.canUse) {
      errors.push(usageCheck.reason || 'Usage limit reached');
    }

    // Check eligibility
    const eligibilityManager = new EligibilityManager(this.prisma);
    const eligibilityCheck = await eligibilityManager.checkEligibility({
      userId: params.userId,
      discount: {
        userSegmentIds: discount.userSegmentIds,
        firstOrderOnly: discount.firstOrderOnly,
        newCustomersOnly: discount.newCustomersOnly,
      },
    });

    if (!eligibilityCheck.eligible) {
      errors.push(eligibilityCheck.reason || 'Not eligible for this discount');
    }

    // Check min/max order amount
    if (discount.minOrderAmount && params.cartTotal < Number(discount.minOrderAmount)) {
      errors.push(`Minimum order amount of ${discount.minOrderAmount} required`);
    }

    if (discount.maxOrderAmount && params.cartTotal > Number(discount.maxOrderAmount)) {
      errors.push(`Maximum order amount of ${discount.maxOrderAmount} exceeded`);
    }

    // Check scope
    if (discount.scope !== DiscountScope.CART) {
      const hasEligibleItem = params.cartItems.some(item => {
        switch (discount.scope) {
          case DiscountScope.PRODUCT:
            return discount.scopeIds?.includes(item.productId);
          case DiscountScope.CATEGORY:
            return item.categoryId && discount.scopeIds?.includes(item.categoryId);
          case DiscountScope.BRAND:
            return item.brandId && discount.scopeIds?.includes(item.brandId);
          default:
            return false;
        }
      });

      if (!hasEligibleItem) {
        errors.push('Discount does not apply to any items in your cart');
      }
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }
}
```

---

## Analytics

### Discount Analytics

```typescript
class DiscountAnalytics {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get discount usage stats
   */
  async getUsageStats(params: {
    discountId: string;
    startDate?: Date;
    endDate?: Date;
  }): Promise<{
    totalUses: number;
    uniqueUsers: number;
    totalDiscountAmount: number;
    averageOrderValue: number;
  }> {
    const where: any = {
      discountId: params.discountId,
    };

    if (params.startDate || params.endDate) {
      where.usedAt = {};
      if (params.startDate) {
        where.usedAt.gte = params.startDate;
      }
      if (params.endDate) {
        where.usedAt.lte = params.endDate;
      }
    }

    const usages = await this.prisma.couponUsage.findMany({
      where,
      include: {
        order: true,
      },
    });

    const totalUses = usages.length;
    const uniqueUsers = new Set(usages.map(u => u.userId)).size;
    const totalDiscountAmount = usages.reduce((sum, u) => {
      const discount = u.order?.discountAmount || 0;
      return sum + Number(discount);
    }, 0);
    const averageOrderValue = totalUses > 0
      ? usages.reduce((sum, u) => sum + Number(u.order?.total || 0), 0) / totalUses
      : 0;

    return {
      totalUses,
      uniqueUsers,
      totalDiscountAmount,
      averageOrderValue,
    };
  }

  /**
   * Get discount performance
   */
  async getPerformance(params: {
    startDate: Date;
    endDate: Date;
  }): Promise<Array<{
    discountId: string;
    discountName: string;
    type: DiscountType;
    totalUses: number;
    totalDiscountAmount: number;
    conversionRate: number;
  }>> {
    const coupons = await this.prisma.coupon.findMany({
      where: {
        status: DiscountStatus.ACTIVE,
        startDate: { lte: params.endDate },
        endDate: { gte: params.startDate },
      },
    });

    const performance = [];

    for (const coupon of coupons) {
      const stats = await this.getUsageStats({
        discountId: coupon.id,
        startDate: params.startDate,
        endDate: params.endDate,
      });

      performance.push({
        discountId: coupon.id,
        discountName: coupon.code,
        type: coupon.type,
        totalUses: stats.totalUses,
        totalDiscountAmount: stats.totalDiscountAmount,
        conversionRate: stats.totalUses > 0 ? stats.uniqueUsers / stats.totalUses : 0,
      });
    }

    return performance.sort((a, b) => b.totalUses - a.totalUses);
  }
}
```

---

## A/B Testing Promotions

### A/B Test Manager

```typescript
class DiscountABTestManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create A/B test
   */
  async createTest(params: {
    name: string;
    description?: string;
    variants: Array<{
      name: string;
      type: DiscountType;
      value: number;
      trafficPercentage: number;
    }>;
    startDate: Date;
    endDate: Date;
    targetSegmentIds?: string[];
  }): Promise<DiscountABTest> {
    // Validate traffic percentages
    const totalTraffic = params.variants.reduce((sum, v) => sum + v.trafficPercentage, 0);

    if (totalTraffic !== 100) {
      throw new Error('Traffic percentages must sum to 100');
    }

    return await this.prisma.$transaction(async (tx) => {
      const test = await tx.discountABTest.create({
        data: {
          name: params.name,
          description: params.description,
          startDate: params.startDate,
          endDate: params.endDate,
          targetSegmentIds: params.targetSegmentIds,
          status: 'active',
        },
      });

      // Create variants
      for (const variant of params.variants) {
        await tx.discountABTestVariant.create({
          data: {
            testId: test.id,
            name: variant.name,
            type: variant.type,
            value: variant.value,
            trafficPercentage: variant.trafficPercentage,
          },
        });
      }

      return test;
    });
  }

  /**
   * Get variant for user
   */
  async getVariantForUser(
    testId: string,
    userId: string
  ): Promise<DiscountABTestVariant | null> {
    // Check if user already assigned
    const assignment = await this.prisma.discountABTestAssignment.findUnique({
      where: { testId_userId: { testId, userId } },
    });

    if (assignment) {
      return this.prisma.discountABTestVariant.findUnique({
        where: { id: assignment.variantId },
      });
    }

    // Assign user to variant
    const test = await this.prisma.discountABTest.findUnique({
      where: { id: testId },
      include: { variants: true },
    });

    if (!test) {
      return null;
    }

    // Determine variant based on traffic percentage
    const hash = this.hashUserId(userId);
    const variant = this.selectVariant(hash, test.variants);

    // Save assignment
    await this.prisma.discountABTestAssignment.create({
      data: {
        testId,
        userId,
        variantId: variant.id,
      },
    });

    return variant;
  }

  /**
   * Hash user ID
   */
  private hashUserId(userId: string): number {
    let hash = 0;

    for (let i = 0; i < userId.length; i++) {
      const char = userId.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash;
    }

    return Math.abs(hash);
  }

  /**
   * Select variant
   */
  private selectVariant(
    hash: number,
    variants: DiscountABTestVariant[]
  ): DiscountABTestVariant {
    const percentage = hash % 100;
    let cumulative = 0;

    for (const variant of variants) {
      cumulative += variant.trafficPercentage;

      if (percentage < cumulative) {
        return variant;
      }
    }

    return variants[variants.length - 1];
  }

  /**
   * Get test results
   */
  async getTestResults(testId: string): Promise<{
    test: DiscountABTest;
    variants: Array<{
      variant: DiscountABTestVariant;
      impressions: number;
      conversions: number;
      conversionRate: number;
    }>;
    winner?: DiscountABTestVariant;
  }> {
    const test = await this.prisma.discountABTest.findUnique({
      where: { id: testId },
      include: { variants: true },
    });

    if (!test) {
      throw new Error('Test not found');
    }

    const variantResults = [];

    for (const variant of test.variants) {
      const impressions = await this.prisma.discountABTestAssignment.count({
        where: { variantId: variant.id },
      });

      const conversions = await this.prisma.discountABTestAssignment.count({
        where: {
          variantId: variant.id,
          converted: true,
        },
      });

      variantResults.push({
        variant,
        impressions,
        conversions,
        conversionRate: impressions > 0 ? conversions / impressions : 0,
      });
    }

    // Determine winner
    const winner = variantResults
      .sort((a, b) => b.conversionRate - a.conversionRate)[0]?.variant;

    return {
      test,
      variants: variantResults,
      winner,
    };
  }
}
```

---

## Best Practices

### Discount Best Practices

```typescript
// 1. Always validate before applying
async function validateAndApplyDiscount(
  code: string,
  userId?: string
): Promise<void> {
  const couponManager = new CouponManager(prisma);
  const validation = await couponManager.validateCoupon({
    code,
    userId,
    cartTotal: 0,
    cartItems: [],
  });

  if (!validation.valid) {
    throw new Error(validation.error);
  }

  // Apply discount
  await couponManager.applyCoupon({ code, userId, orderId: '' });
}

// 2. Use clear expiration dates
function createCouponWithExpiration(
  code: string,
  daysUntilExpiration: number
): Coupon {
  const endDate = new Date();
  endDate.setDate(endDate.getDate() + daysUntilExpiration);

  return {
    code,
    endDate,
    // ... other fields
  };
}

// 3. Set reasonable usage limits
async function createCouponWithLimits(
  code: string,
  totalLimit: number,
  perUserLimit: number
): Promise<Coupon> {
  const couponManager = new CouponManager(prisma);

  return await couponManager.createCoupon({
    code,
    usageLimit: totalLimit,
    usageLimitPerUser: perUserLimit,
    // ... other fields
  });
}

// 4. Test discounts thoroughly
async function testDiscount(
  discountId: string,
  testCases: Array<{
    cartTotal: number;
    cartItems: any[];
    expectedDiscount: number;
  }>
): Promise<void> {
  const calculator = new DiscountCalculator();

  for (const testCase of testCases) {
    const result = await calculator.calculateDiscounts({
      cartTotal: testCase.cartTotal,
      cartItems: testCase.cartItems,
    });

    if (result.totalDiscount !== testCase.expectedDiscount) {
      throw new Error(`Test failed: expected ${testCase.expectedDiscount}, got ${result.totalDiscount}`);
    }
  }
}

// 5. Monitor discount performance
async function monitorDiscountPerformance(discountId: string): Promise<void> {
  const analytics = new DiscountAnalytics(prisma);
  const stats = await analytics.getUsageStats({
    discountId,
    startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
  });

  console.log(`Discount stats:`, stats);

  // Alert if performance is poor
  if (stats.totalUses < 10) {
    console.warn('Discount has low usage');
  }
}
```

---

---

## Quick Start

### Discount Calculation

```typescript
interface Discount {
  id: string
  type: 'percentage' | 'fixed' | 'free_shipping'
  value: number
  minPurchase?: number
  maxDiscount?: number
  applicableTo: 'all' | 'category' | 'product'
}

function calculateDiscount(
  cart: Cart,
  discount: Discount
): number {
  let discountAmount = 0
  
  if (discount.type === 'percentage') {
    const subtotal = cart.subtotal
    discountAmount = (subtotal * discount.value) / 100
    
    if (discount.maxDiscount) {
      discountAmount = Math.min(discountAmount, discount.maxDiscount)
    }
  } else if (discount.type === 'fixed') {
    discountAmount = discount.value
  } else if (discount.type === 'free_shipping') {
    discountAmount = cart.shippingCost
  }
  
  return discountAmount
}
```

### Coupon Validation

```typescript
async function validateCoupon(
  code: string,
  userId: string,
  cart: Cart
): Promise<{ valid: boolean; discount?: Discount; error?: string }> {
  const coupon = await db.coupons.findUnique({
    where: { code }
  })
  
  if (!coupon || !coupon.active) {
    return { valid: false, error: 'Invalid coupon' }
  }
  
  if (coupon.usageLimit && coupon.usedCount >= coupon.usageLimit) {
    return { valid: false, error: 'Coupon limit reached' }
  }
  
  if (coupon.userLimit) {
    const userUsage = await getUserCouponUsage(userId, coupon.id)
    if (userUsage >= coupon.userLimit) {
      return { valid: false, error: 'You have used this coupon already' }
    }
  }
  
  if (coupon.minPurchase && cart.subtotal < coupon.minPurchase) {
    return { valid: false, error: `Minimum purchase of ${coupon.minPurchase} required` }
  }
  
  return { valid: true, discount: coupon }
}
```

---

## Production Checklist

- [ ] **Discount Types**: Support multiple discount types
- [ ] **Coupon Codes**: Coupon code generation and validation
- [ ] **Promotion Rules**: Flexible promotion rules
- [ ] **Stacking Rules**: Define stacking rules
- [ ] **Eligibility**: User and product eligibility
- [ ] **Usage Limits**: Usage limits per user/coupon
- [ ] **Date Restrictions**: Start/end dates
- [ ] **Calculation**: Accurate discount calculation
- [ ] **Validation**: Validate discounts before application
- [ ] **Analytics**: Track promotion performance
- [ ] **Testing**: A/B test promotions
- [ ] **Documentation**: Document promotion rules

---

## Anti-patterns

### ❌ Don't: No Validation

```typescript
// ❌ Bad - No validation
const discount = calculateDiscount(cart, coupon)
cart.total -= discount  // Could be negative!
```

```typescript
// ✅ Good - Validate first
const validation = await validateCoupon(coupon.code, userId, cart)
if (validation.valid) {
  const discount = calculateDiscount(cart, validation.discount)
  cart.total = Math.max(0, cart.total - discount)
}
```

### ❌ Don't: Unlimited Stacking

```typescript
// ❌ Bad - Stack all discounts
const totalDiscount = discounts.reduce((sum, d) => sum + d.value, 0)
// Could be > 100%!
```

```typescript
// ✅ Good - Stacking rules
const totalDiscount = applyStackingRules(discounts, cart)
// Max 50% total discount
```

---

## Integration Points

- **Shopping Cart** (`30-ecommerce/shopping-cart/`) - Apply discounts
- **Order Management** (`30-ecommerce/order-management/`) - Order processing
- **Analytics** (`23-business-analytics/`) - Promotion analytics

---

## Further Reading

- [E-commerce Discount Strategies](https://www.shopify.com/blog/discount-strategies)
- [Promotion Engine Design](https://www.optimizely.com/optimization-glossary/promotion-engine/)

## Resources

- [Shopify Discount API](https://shopify.dev/api/admin-graphql/latest/objects/DiscountCode)
- [WooCommerce Coupons](https://woocommerce.github.io/woocommerce-rest-api-docs/#coupons)
- [Magento 2 Promotions](https://devdocs.magento.com/guides/v2.4/rest/bk-rest-api.html)
- [BigCommerce Discounts](https://developer.bigcommerce.com/api-reference/catalog/catalog-api/discounts)
