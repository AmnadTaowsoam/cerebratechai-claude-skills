---
name: Shopping Cart Implementation
description: Building shopping cart systems that allow users to collect items for purchase, with proper state management, validation, price calculations, and cart persistence.
---

# Shopping Cart Implementation

> **Current Level:** Intermediate  
> **Domain:** E-commerce / Frontend

---

## Overview

A shopping cart is a critical component of any e-commerce system, allowing users to collect items for purchase. This guide covers various cart architectures and implementations, including guest carts, logged-in user carts, cart persistence, and cart abandonment tracking.

---

---

## Core Concepts

### Table of Contents

1. [Cart Architecture](#cart-architecture)
2. [Cart Operations](#cart-operations)
3. [Cart State Management](#cart-state-management)
4. [Guest vs Logged-in Users](#guest-vs-logged-in-users)
5. [Cart Abandonment Tracking](#cart-abandonment-tracking)
6. [Cart Recovery](#cart-recovery)
7. [Cart Validation](#cart-validation)
8. [Price Calculations](#price-calculations)
9. [Database Schema](#database-schema)
10. [API Design](#api-design)
11. [Frontend Patterns](#frontend-patterns)
12. [Performance Optimization](#performance-optimization)
13. [Best Practices](#best-practices)

---

## Cart Architecture

### Session-Based Cart

```typescript
// npm install express-session
import session from 'express-session';

class SessionCartManager {
  /**
   * Get cart from session
   */
  getCart(req: Express.Request): Cart {
    if (!req.session.cart) {
      req.session.cart = {
        items: [],
        total: 0,
        subtotal: 0,
        tax: 0,
        shipping: 0,
      };
    }

    return req.session.cart;
  }

  /**
   * Save cart to session
   */
  saveCart(req: Express.Request, cart: Cart): void {
    req.session.cart = cart;
  }

  /**
   * Clear cart
   */
  clearCart(req: Express.Request): void {
    req.session.cart = {
      items: [],
      total: 0,
      subtotal: 0,
      tax: 0,
      shipping: 0,
    };
  }
}
```

### Persistent Cart

```typescript
interface Cart {
  id: string;
  userId?: string;
  sessionId?: string;
  items: CartItem[];
  subtotal: number;
  tax: number;
  shipping: number;
  total: number;
  currency: string;
  createdAt: Date;
  updatedAt: Date;
}

interface CartItem {
  id: string;
  cartId: string;
  productId: string;
  variantId?: string;
  quantity: number;
  price: number;
  salePrice?: number;
  addedAt: Date;
}

class PersistentCartManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get or create cart
   */
  async getOrCreateCart(params: {
    userId?: string;
    sessionId?: string;
  }): Promise<Cart> {
    const where: any = {};

    if (params.userId) {
      where.userId = params.userId;
    } else if (params.sessionId) {
      where.sessionId = params.sessionId;
    } else {
      throw new Error('Either userId or sessionId is required');
    }

    let cart = await this.prisma.cart.findFirst({
      where,
      include: { items: true },
    });

    if (!cart) {
      cart = await this.prisma.cart.create({
        data: {
          ...where,
          currency: 'USD',
        },
        include: { items: true },
      });
    }

    return this.calculateCartTotals(cart);
  }

  /**
   * Merge carts (guest to logged-in)
   */
  async mergeCarts(sessionCartId: string, userId: string): Promise<Cart> {
    const sessionCart = await this.prisma.cart.findUnique({
      where: { id: sessionCartId },
      include: { items: true },
    });

    if (!sessionCart) {
      return this.getOrCreateCart({ userId });
    }

    const userCart = await this.getOrCreateCart({ userId });

    // Merge items
    for (const sessionItem of sessionCart.items) {
      const existingItem = userCart.items.find(
        item => item.productId === sessionItem.productId &&
                item.variantId === sessionItem.variantId
      );

      if (existingItem) {
        await this.prisma.cartItem.update({
          where: { id: existingItem.id },
          data: { quantity: existingItem.quantity + sessionItem.quantity },
        });
      } else {
        await this.prisma.cartItem.create({
          data: {
            cartId: userCart.id,
            productId: sessionItem.productId,
            variantId: sessionItem.variantId,
            quantity: sessionItem.quantity,
            price: sessionItem.price,
            salePrice: sessionItem.salePrice,
          },
        });
      }
    }

    // Delete session cart
    await this.prisma.cart.delete({
      where: { id: sessionCartId },
    });

    return this.getOrCreateCart({ userId });
  }

  /**
   * Calculate cart totals
   */
  private async calculateCartTotals(cart: any): Promise<Cart> {
    let subtotal = 0;

    for (const item of cart.items) {
      const price = item.salePrice || item.price;
      subtotal += price * item.quantity;
    }

    const tax = await this.calculateTax(subtotal, cart.userId);
    const shipping = await this.calculateShipping(cart);
    const total = subtotal + tax + shipping;

    return {
      ...cart,
      subtotal,
      tax,
      shipping,
      total,
    };
  }

  /**
   * Calculate tax
   */
  private async calculateTax(subtotal: number, userId?: string): Promise<number> {
    // Implement tax calculation based on user location
    return subtotal * 0.1; // 10% tax
  }

  /**
   * Calculate shipping
   */
  private async calculateShipping(cart: any): Promise<number> {
    // Implement shipping calculation
    return 0; // Free shipping
  }

  constructor(private prisma: PrismaClient) {}
}
```

### Hybrid Cart

```typescript
class HybridCartManager {
  private sessionManager: SessionCartManager;
  private persistentManager: PersistentCartManager;

  constructor(
    private prisma: PrismaClient,
    private session: session.Session
  ) {
    this.sessionManager = new SessionCartManager();
    this.persistentManager = new PersistentCartManager(prisma);
  }

  /**
   * Get cart
   */
  async getCart(userId?: string): Promise<Cart> {
    if (userId) {
      return this.persistentManager.getOrCreateCart({ userId });
    }

    return this.sessionManager.getCart(this.session);
  }

  /**
   * Merge on login
   */
  async mergeOnLogin(userId: string): Promise<Cart> {
    const sessionCart = this.sessionManager.getCart(this.session);

    if (sessionCart.items.length === 0) {
      return this.persistentManager.getOrCreateCart({ userId });
    }

    // Create temporary cart for merging
    const tempCart = await this.prisma.cart.create({
      data: {
        sessionId: this.session.id,
        currency: 'USD',
      },
    });

    // Add session items to temp cart
    for (const item of sessionCart.items) {
      await this.prisma.cartItem.create({
        data: {
          cartId: tempCart.id,
          productId: item.productId,
          variantId: item.variantId,
          quantity: item.quantity,
          price: item.price,
          salePrice: item.salePrice,
        },
      });
    }

    // Merge with user cart
    const merged = await this.persistentManager.mergeCarts(tempCart.id, userId);

    // Clear session cart
    this.sessionManager.clearCart(this.session);

    return merged;
  }
}
```

---

## Cart Operations

### Cart Operations

```typescript
class CartOperations {
  constructor(private prisma: PrismaClient) {}

  /**
   * Add item to cart
   */
  async addItem(params: {
    cartId: string;
    productId: string;
    variantId?: string;
    quantity: number;
  }): Promise<Cart> {
    // Validate product
    const product = await this.prisma.product.findUnique({
      where: { id: params.productId },
      include: { variants: true },
    });

    if (!product) {
      throw new Error('Product not found');
    }

    if (!product.active) {
      throw new Error('Product is not available');
    }

    // Get price
    let price = product.price;
    let salePrice = product.salePrice;

    if (params.variantId) {
      const variant = product.variants.find(v => v.id === params.variantId);
      if (!variant) {
        throw new Error('Variant not found');
      }
      price = variant.price;
      salePrice = variant.salePrice;
    }

    // Check if item already exists
    const existingItem = await this.prisma.cartItem.findFirst({
      where: {
        cartId: params.cartId,
        productId: params.productId,
        variantId: params.variantId,
      },
    });

    if (existingItem) {
      await this.prisma.cartItem.update({
        where: { id: existingItem.id },
        data: { quantity: existingItem.quantity + params.quantity },
      });
    } else {
      await this.prisma.cartItem.create({
        data: {
          cartId: params.cartId,
          productId: params.productId,
          variantId: params.variantId,
          quantity: params.quantity,
          price,
          salePrice,
        },
      });
    }

    return this.getCart(params.cartId);
  }

  /**
   * Update item quantity
   */
  async updateQuantity(params: {
    cartId: string;
    itemId: string;
    quantity: number;
  }): Promise<Cart> {
    if (params.quantity <= 0) {
      return this.removeItem(params.cartId, params.itemId);
    }

    await this.prisma.cartItem.update({
      where: { id: params.itemId },
      data: { quantity: params.quantity },
    });

    return this.getCart(params.cartId);
  }

  /**
   * Remove item
   */
  async removeItem(cartId: string, itemId: string): Promise<Cart> {
    await this.prisma.cartItem.delete({
      where: { id: itemId },
    });

    return this.getCart(cartId);
  }

  /**
   * Clear cart
   */
  async clearCart(cartId: string): Promise<Cart> {
    await this.prisma.cartItem.deleteMany({
      where: { cartId },
    });

    return this.getCart(cartId);
  }

  /**
   * Get cart
   */
  async getCart(cartId: string): Promise<Cart> {
    const cart = await this.prisma.cart.findUnique({
      where: { id: cartId },
      include: {
        items: {
          include: {
            product: true,
            variant: true,
          },
        },
      },
    });

    if (!cart) {
      throw new Error('Cart not found');
    }

    return this.calculateTotals(cart);
  }

  /**
   * Calculate totals
   */
  private async calculateTotals(cart: any): Promise<Cart> {
    let subtotal = 0;

    for (const item of cart.items) {
      const price = item.salePrice || item.price;
      subtotal += price * item.quantity;
    }

    const tax = await this.calculateTax(subtotal, cart.userId);
    const shipping = await this.calculateShipping(cart);
    const total = subtotal + tax + shipping;

    return {
      ...cart,
      subtotal,
      tax,
      shipping,
      total,
    };
  }

  /**
   * Calculate tax
   */
  private async calculateTax(subtotal: number, userId?: string): Promise<number> {
    // Implement tax calculation
    return subtotal * 0.1;
  }

  /**
   * Calculate shipping
   */
  private async calculateShipping(cart: any): Promise<number> {
    // Implement shipping calculation
    return 0;
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Cart State Management

### Redux Cart Store

```typescript
// cartSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CartState {
  items: CartItem[];
  total: number;
  subtotal: number;
  tax: number;
  shipping: number;
  loading: boolean;
  error: string | null;
}

const initialState: CartState = {
  items: [],
  total: 0,
  subtotal: 0,
  tax: 0,
  shipping: 0,
  loading: false,
  error: null,
};

const cartSlice = createSlice({
  name: 'cart',
  initialState,
  reducers: {
    setCart: (state, action: PayloadAction<Cart>) => {
      state.items = action.payload.items;
      state.subtotal = action.payload.subtotal;
      state.tax = action.payload.tax;
      state.shipping = action.payload.shipping;
      state.total = action.payload.total;
    },
    addItem: (state, action: PayloadAction<CartItem>) => {
      const existingItem = state.items.find(
        item => item.productId === action.payload.productId &&
                item.variantId === action.payload.variantId
      );

      if (existingItem) {
        existingItem.quantity += action.payload.quantity;
      } else {
        state.items.push(action.payload);
      }
    },
    updateQuantity: (state, action: PayloadAction<{
      itemId: string;
      quantity: number;
    }>) => {
      const item = state.items.find(i => i.id === action.payload.itemId);
      if (item) {
        item.quantity = action.payload.quantity;
      }
    },
    removeItem: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter(i => i.id !== action.payload);
    },
    clearCart: (state) => {
      state.items = [];
    },
    setLoading: (state, action: PayloadAction<boolean>) => {
      state.loading = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
  },
});

export const {
  setCart,
  addItem,
  updateQuantity,
  removeItem,
  clearCart,
  setLoading,
  setError,
} = cartSlice.actions;

export default cartSlice.reducer;
```

### Cart Hook

```typescript
// useCart.ts
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../store';
import {
  setCart,
  addItem as addItemAction,
  updateQuantity as updateQuantityAction,
  removeItem as removeItemAction,
  clearCart as clearCartAction,
  setLoading,
  setError,
} from '../store/cartSlice';
import { cartApi } from '../api/cartApi';

export function useCart() {
  const dispatch = useDispatch();
  const { items, total, subtotal, tax, shipping, loading, error } = useSelector(
    (state: RootState) => state.cart
  );

  const loadCart = async () => {
    dispatch(setLoading(true));
    try {
      const cart = await cartApi.getCart();
      dispatch(setCart(cart));
    } catch (err) {
      dispatch(setError(err.message));
    } finally {
      dispatch(setLoading(false));
    }
  };

  const addItem = async (productId: string, variantId?: string, quantity: number = 1) => {
    dispatch(setLoading(true));
    try {
      const cart = await cartApi.addItem({ productId, variantId, quantity });
      dispatch(setCart(cart));
    } catch (err) {
      dispatch(setError(err.message));
    } finally {
      dispatch(setLoading(false));
    }
  };

  const updateQuantity = async (itemId: string, quantity: number) => {
    dispatch(setLoading(true));
    try {
      const cart = await cartApi.updateQuantity({ itemId, quantity });
      dispatch(setCart(cart));
    } catch (err) {
      dispatch(setError(err.message));
    } finally {
      dispatch(setLoading(false));
    }
  };

  const removeItem = async (itemId: string) => {
    dispatch(setLoading(true));
    try {
      const cart = await cartApi.removeItem(itemId);
      dispatch(setCart(cart));
    } catch (err) {
      dispatch(setError(err.message));
    } finally {
      dispatch(setLoading(false));
    }
  };

  const clearCart = async () => {
    dispatch(setLoading(true));
    try {
      const cart = await cartApi.clearCart();
      dispatch(setCart(cart));
    } catch (err) {
      dispatch(setError(err.message));
    } finally {
      dispatch(setLoading(false));
    }
  };

  return {
    items,
    total,
    subtotal,
    tax,
    shipping,
    loading,
    error,
    loadCart,
    addItem,
    updateQuantity,
    removeItem,
    clearCart,
  };
}
```

---

## Guest vs Logged-in Users

### Guest Cart Handler

```typescript
class GuestCartHandler {
  /**
   * Generate session ID
   */
  generateSessionId(): string {
    return crypto.randomUUID();
  }

  /**
   * Get cart for guest
   */
  async getGuestCart(sessionId: string): Promise<Cart> {
    return this.getOrCreateCart({ sessionId });
  }

  /**
   * Convert guest cart to user cart
   */
  async convertToUserCart(sessionId: string, userId: string): Promise<Cart> {
    return this.mergeCarts(sessionId, userId);
  }
}
```

---

## Cart Abandonment Tracking

### Abandonment Tracker

```typescript
class CartAbandonmentTracker {
  constructor(private prisma: PrismaClient) {}

  /**
   * Track cart activity
   */
  async trackActivity(cartId: string, activity: {
    type: 'view' | 'add' | 'update' | 'remove' | 'checkout';
    itemId?: string;
  }): Promise<void> {
    await this.prisma.cartActivity.create({
      data: {
        cartId,
        ...activity,
        timestamp: new Date(),
      },
    });
  }

  /**
   * Get abandoned carts
   */
  async getAbandonedCarts(params: {
    hoursSinceActivity: number;
    minItems?: number;
    minValue?: number;
  }): Promise<Cart[]> {
    const cutoffTime = new Date(Date.now() - params.hoursSinceActivity * 60 * 60 * 1000);

    const carts = await this.prisma.cart.findMany({
      where: {
        updatedAt: {
          lt: cutoffTime,
        },
        items: {
          some: {},
        },
      },
      include: {
        items: {
          include: {
            product: true,
          },
        },
        user: true,
      },
    });

    return carts.filter(cart => {
      if (params.minItems && cart.items.length < params.minItems) {
        return false;
      }

      if (params.minValue && cart.subtotal < params.minValue) {
        return false;
      }

      return true;
    });
  }

  /**
   * Send recovery email
   */
  async sendRecoveryEmail(cartId: string): Promise<void> {
    const cart = await this.prisma.cart.findUnique({
      where: { id: cartId },
      include: {
        items: {
          include: {
            product: true,
          },
        },
        user: true,
      },
    });

    if (!cart || !cart.user?.email) {
      return;
    }

    await emailService.send({
      to: cart.user.email,
      subject: 'Complete your purchase',
      templateId: 'cart-recovery',
      dynamicTemplateData: {
        cartUrl: `${process.env.APP_URL}/cart?id=${cart.id}`,
        items: cart.items,
        total: cart.total,
      },
    });

    // Track recovery email sent
    await this.prisma.cartRecovery.create({
      data: {
        cartId,
        type: 'email',
        sentAt: new Date(),
      },
    });
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Cart Recovery

### Recovery Manager

```typescript
class CartRecoveryManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Process abandoned carts
   */
  async processAbandonedCarts(): Promise<void> {
    const tracker = new CartAbandonmentTracker(this.prisma);

    // Get carts abandoned 1 hour ago
    const carts = await tracker.getAbandonedCarts({
      hoursSinceActivity: 1,
      minItems: 1,
    });

    for (const cart of carts) {
      // Check if recovery already sent
      const existingRecovery = await this.prisma.cartRecovery.findFirst({
        where: {
          cartId: cart.id,
          type: 'email',
          sentAt: {
            gte: new Date(Date.now() - 24 * 60 * 60 * 1000), // 24 hours
          },
        },
      });

      if (existingRecovery) {
        continue;
      }

      // Send recovery email
      await tracker.sendRecoveryEmail(cart.id);
    }
  }

  /**
   * Track recovery conversion
   */
  async trackRecoveryConversion(cartId: string): Promise<void> {
    await this.prisma.cartRecovery.updateMany({
      where: { cartId },
      data: {
        convertedAt: new Date(),
      },
    });
  }
}
```

---

## Cart Validation

### Cart Validator

```typescript
class CartValidator {
  /**
   * Validate cart
   */
  async validateCart(cart: Cart): Promise<{
    valid: boolean;
    errors: ValidationError[];
    warnings: ValidationWarning[];
  }> {
    const errors: ValidationError[] = [];
    const warnings: ValidationWarning[] = [];

    // Validate items
    for (const item of cart.items) {
      const itemValidation = await this.validateItem(item);
      errors.push(...itemValidation.errors);
      warnings.push(...itemValidation.warnings);
    }

    // Validate totals
    const totalValidation = this.validateTotals(cart);
    errors.push(...totalValidation.errors);
    warnings.push(...totalValidation.warnings);

    return {
      valid: errors.length === 0,
      errors,
      warnings,
    };
  }

  /**
   * Validate item
   */
  private async validateItem(item: CartItem): Promise<{
    errors: ValidationError[];
    warnings: ValidationWarning[];
  }> {
    const errors: ValidationError[] = [];
    const warnings: ValidationWarning[] = [];

    // Check product exists and is active
    const product = await this.prisma.product.findUnique({
      where: { id: item.productId },
      include: { variants: true },
    });

    if (!product) {
      errors.push({
        type: 'error',
        code: 'PRODUCT_NOT_FOUND',
        message: `Product ${item.productId} not found`,
        itemId: item.id,
      });
      return { errors, warnings };
    }

    if (!product.active) {
      errors.push({
        type: 'error',
        code: 'PRODUCT_INACTIVE',
        message: `Product ${product.name} is not available`,
        itemId: item.id,
      });
    }

    // Check variant
    if (item.variantId) {
      const variant = product.variants.find(v => v.id === item.variantId);
      if (!variant) {
        errors.push({
          type: 'error',
          code: 'VARIANT_NOT_FOUND',
          message: `Variant ${item.variantId} not found`,
          itemId: item.id,
        });
      }
    }

    // Check inventory
    const availableStock = await this.getAvailableStock(item.productId, item.variantId);
    if (item.quantity > availableStock) {
      errors.push({
        type: 'error',
        code: 'INSUFFICIENT_STOCK',
        message: `Only ${availableStock} items available`,
        itemId: item.id,
      });
    } else if (item.quantity > availableStock * 0.8) {
      warnings.push({
        type: 'warning',
        code: 'LOW_STOCK',
        message: `Only ${availableStock} items available`,
        itemId: item.id,
      });
    }

    // Check price
    const currentPrice = item.variantId
      ? product.variants.find(v => v.id === item.variantId)?.price
      : product.price;

    const currentSalePrice = item.variantId
      ? product.variants.find(v => v.id === item.variantId)?.salePrice
      : product.salePrice;

    if (item.price !== currentPrice) {
      warnings.push({
        type: 'warning',
        code: 'PRICE_CHANGED',
        message: `Price has changed from ${item.price} to ${currentPrice}`,
        itemId: item.id,
      });
    }

    return { errors, warnings };
  }

  /**
   * Validate totals
   */
  private validateTotals(cart: Cart): {
    errors: ValidationError[];
    warnings: ValidationWarning[];
  } {
    const errors: ValidationError[] = [];
    const warnings: ValidationWarning[] = [];

    // Recalculate subtotal
    let calculatedSubtotal = 0;
    for (const item of cart.items) {
      const price = item.salePrice || item.price;
      calculatedSubtotal += price * item.quantity;
    }

    if (Math.abs(cart.subtotal - calculatedSubtotal) > 0.01) {
      errors.push({
        type: 'error',
        code: 'SUBTOTAL_MISMATCH',
        message: `Subtotal mismatch: expected ${calculatedSubtotal}, got ${cart.subtotal}`,
      });
    }

    return { errors, warnings };
  }

  /**
   * Get available stock
   */
  private async getAvailableStock(productId: string, variantId?: string): Promise<number> {
    // Implement stock checking
    return 100;
  }

  constructor(private prisma: PrismaClient) {}
}

interface ValidationError {
  type: 'error' | 'warning';
  code: string;
  message: string;
  itemId?: string;
}

interface ValidationWarning {
  type: 'error' | 'warning';
  code: string;
  message: string;
  itemId?: string;
}
```

---

## Price Calculations

### Price Calculator

```typescript
class PriceCalculator {
  /**
   * Calculate item price
   */
  calculateItemPrice(item: CartItem): number {
    const price = item.salePrice || item.price;
    return price * item.quantity;
  }

  /**
   * Calculate subtotal
   */
  calculateSubtotal(items: CartItem[]): number {
    return items.reduce((sum, item) => sum + this.calculateItemPrice(item), 0);
  }

  /**
   * Calculate tax
   */
  async calculateTax(
    items: CartItem[],
    taxRate: number,
    userId?: string
  ): Promise<number> {
    const subtotal = this.calculateSubtotal(items);

    // Get user's tax jurisdiction
    const jurisdiction = userId
      ? await this.getUserTaxJurisdiction(userId)
      : { rate: taxRate };

    return subtotal * jurisdiction.rate;
  }

  /**
   * Calculate shipping
   */
  async calculateShipping(
    items: CartItem[],
    userId?: string,
    shippingMethod?: string
  ): Promise<number> {
    // Get user's address
    const address = userId
      ? await this.getUserShippingAddress(userId)
      : null;

    // Calculate based on weight, dimensions, and destination
    const weight = this.calculateTotalWeight(items);
    const distance = address ? await this.calculateDistance(address) : 0;

    // Apply shipping method rates
    const rates = await this.getShippingRates(weight, distance, address?.country);
    const method = shippingMethod || rates[0].id;

    const selectedRate = rates.find(r => r.id === method);
    return selectedRate?.price || 0;
  }

  /**
   * Calculate discounts
   */
  async calculateDiscounts(
    items: CartItem[],
    couponCode?: string
  ): Promise<{
    discountAmount: number;
    appliedCoupons: string[];
  }> {
    let discountAmount = 0;
    const appliedCoupons: string[] = [];

    if (couponCode) {
      const coupon = await this.validateCoupon(couponCode);
      if (coupon) {
        appliedCoupons.push(couponCode);
        discountAmount += this.applyCoupon(items, coupon);
      }
    }

    // Apply automatic discounts
    const autoDiscounts = await this.getAutomaticDiscounts(items);
    for (const discount of autoDiscounts) {
      discountAmount += this.applyDiscount(items, discount);
    }

    return { discountAmount, appliedCoupons };
  }

  /**
   * Calculate total
   */
  async calculateTotal(params: {
    items: CartItem[];
    taxRate: number;
    userId?: string;
    couponCode?: string;
    shippingMethod?: string;
  }): Promise<{
    subtotal: number;
    tax: number;
    shipping: number;
    discount: number;
    total: number;
  }> {
    const subtotal = this.calculateSubtotal(params.items);
    const tax = await this.calculateTax(params.items, params.taxRate, params.userId);
    const shipping = await this.calculateShipping(
      params.items,
      params.userId,
      params.shippingMethod
    );
    const { discountAmount } = await this.calculateDiscounts(
      params.items,
      params.couponCode
    );

    const total = subtotal + tax + shipping - discountAmount;

    return {
      subtotal,
      tax,
      shipping,
      discount: discountAmount,
      total,
    };
  }

  private async getUserTaxJurisdiction(userId: string): Promise<{ rate: number }> {
    // Implement jurisdiction lookup
    return { rate: 0.1 };
  }

  private async getUserShippingAddress(userId: string): Promise<any> {
    // Implement address lookup
    return null;
  }

  private calculateTotalWeight(items: CartItem[]): number {
    // Implement weight calculation
    return 0;
  }

  private async calculateDistance(address: any): Promise<number> {
    // Implement distance calculation
    return 0;
  }

  private async getShippingRates(weight: number, distance: number, country?: string): Promise<any[]> {
    // Implement rate lookup
    return [];
  }

  private async validateCoupon(code: string): Promise<any> {
    // Implement coupon validation
    return null;
  }

  private applyCoupon(items: CartItem[], coupon: any): number {
    // Implement coupon application
    return 0;
  }

  private async getAutomaticDiscounts(items: CartItem[]): Promise<any[]> {
    // Implement automatic discount lookup
    return [];
  }

  private applyDiscount(items: CartItem[], discount: any): number {
    // Implement discount application
    return 0;
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Database Schema

### Prisma Schema

```prisma
model Cart {
  id          String    @id @default(uuid())
  userId      String?   @unique
  user        User?     @relation(fields: [userId], references: [id])
  sessionId   String?   @unique
  currency    String    @default("USD")
  subtotal    Decimal   @default(0)
  tax         Decimal   @default(0)
  shipping    Decimal   @default(0)
  total       Decimal   @default(0)
  items       CartItem[]
  activities  CartActivity[]
  recoveries  CartRecovery[]
  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt

  @@index([userId])
  @@index([sessionId])
}

model CartItem {
  id        String   @id @default(uuid())
  cartId    String
  cart      Cart     @relation(fields: [cartId], references: [id], onDelete: Cascade)
  productId String
  product   Product  @relation(fields: [productId], references: [id])
  variantId String?
  variant   Variant? @relation(fields: [variantId], references: [id])
  quantity  Int      @default(1)
  price     Decimal
  salePrice Decimal?
  addedAt   DateTime @default(now())

  @@unique([cartId, productId, variantId])
  @@index([cartId])
  @@index([productId])
}

model CartActivity {
  id        String   @id @default(uuid())
  cartId    String
  cart      Cart     @relation(fields: [cartId], references: [id], onDelete: Cascade)
  type      String   // view, add, update, remove, checkout
  itemId    String?
  timestamp DateTime @default(now())

  @@index([cartId])
  @@index([timestamp])
}

model CartRecovery {
  id         String   @id @default(uuid())
  cartId     String
  cart       Cart     @relation(fields: [cartId], references: [id], onDelete: Cascade)
  type       String   // email, push, sms
  sentAt     DateTime
  convertedAt DateTime?

  @@index([cartId])
  @@index([sentAt])
}
```

---

## API Design

### REST API

```typescript
import express from 'express';

const router = express.Router();

/**
 * GET /api/cart
 * Get current user's cart
 */
router.get('/', async (req, res) => {
  try {
    const userId = req.user?.id;
    const sessionId = req.sessionID;

    const cart = await cartManager.getOrCreateCart({ userId, sessionId });
    res.json(cart);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * POST /api/cart/items
 * Add item to cart
 */
router.post('/items', async (req, res) => {
  try {
    const userId = req.user?.id;
    const sessionId = req.sessionID;

    const cart = await cartManager.getOrCreateCart({ userId, sessionId });
    const updatedCart = await cartOperations.addItem({
      cartId: cart.id,
      ...req.body,
    });

    res.json(updatedCart);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * PUT /api/cart/items/:itemId
 * Update item quantity
 */
router.put('/items/:itemId', async (req, res) => {
  try {
    const userId = req.user?.id;
    const sessionId = req.sessionID;

    const cart = await cartManager.getOrCreateCart({ userId, sessionId });
    const updatedCart = await cartOperations.updateQuantity({
      cartId: cart.id,
      itemId: req.params.itemId,
      quantity: req.body.quantity,
    });

    res.json(updatedCart);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * DELETE /api/cart/items/:itemId
 * Remove item from cart
 */
router.delete('/items/:itemId', async (req, res) => {
  try {
    const userId = req.user?.id;
    const sessionId = req.sessionID;

    const cart = await cartManager.getOrCreateCart({ userId, sessionId });
    const updatedCart = await cartOperations.removeItem(cart.id, req.params.itemId);

    res.json(updatedCart);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

/**
 * DELETE /api/cart
 * Clear cart
 */
router.delete('/', async (req, res) => {
  try {
    const userId = req.user?.id;
    const sessionId = req.sessionID;

    const cart = await cartManager.getOrCreateCart({ userId, sessionId });
    const updatedCart = await cartOperations.clearCart(cart.id);

    res.json(updatedCart);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * POST /api/cart/merge
 * Merge guest cart with user cart
 */
router.post('/merge', async (req, res) => {
  try {
    const userId = req.user?.id;
    const sessionId = req.body.sessionId;

    if (!userId || !sessionId) {
      return res.status(400).json({ error: 'userId and sessionId required' });
    }

    const cart = await cartManager.mergeCarts(sessionId, userId);
    res.json(cart);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

export default router;
```

---

## Frontend Patterns

### React Cart Component

```tsx
import React from 'react';
import { useCart } from '../hooks/useCart';

const Cart: React.FC = () => {
  const {
    items,
    total,
    subtotal,
    tax,
    shipping,
    loading,
    error,
    updateQuantity,
    removeItem,
  } = useCart();

  if (loading) {
    return <div className="cart-loading">Loading cart...</div>;
  }

  if (error) {
    return <div className="cart-error">{error}</div>;
  }

  if (items.length === 0) {
    return (
      <div className="cart-empty">
        <h2>Your cart is empty</h2>
        <button onClick={() => window.location.href = '/products'}>
          Continue Shopping
        </button>
      </div>
    );
  }

  return (
    <div className="cart">
      <h1>Shopping Cart</h1>

      <div className="cart-items">
        {items.map(item => (
          <div key={item.id} className="cart-item">
            <img src={item.product.imageUrl} alt={item.product.name} />
            <div className="item-details">
              <h3>{item.product.name}</h3>
              {item.variant && (
                <p className="item-variant">{item.variant.name}</p>
              )}
              <p className="item-price">
                ${(item.salePrice || item.price).toFixed(2)}
              </p>
            </div>

            <div className="item-quantity">
              <button
                onClick={() => updateQuantity(item.id, item.quantity - 1)}
                disabled={item.quantity <= 1}
              >
                -
              </button>
              <span>{item.quantity}</span>
              <button onClick={() => updateQuantity(item.id, item.quantity + 1)}>
                +
              </button>
            </div>

            <div className="item-total">
              ${((item.salePrice || item.price) * item.quantity).toFixed(2)}
            </div>

            <button
              className="item-remove"
              onClick={() => removeItem(item.id)}
            >
              Remove
            </button>
          </div>
        ))}
      </div>

      <div className="cart-summary">
        <div className="summary-row">
          <span>Subtotal</span>
          <span>${subtotal.toFixed(2)}</span>
        </div>
        <div className="summary-row">
          <span>Tax</span>
          <span>${tax.toFixed(2)}</span>
        </div>
        <div className="summary-row">
          <span>Shipping</span>
          <span>${shipping.toFixed(2)}</span>
        </div>
        <div className="summary-row total">
          <span>Total</span>
          <span>${total.toFixed(2)}</span>
        </div>

        <button className="checkout-button" onClick={() => window.location.href = '/checkout'}>
          Proceed to Checkout
        </button>
      </div>
    </div>
  );
};

export default Cart;
```

---

## Performance Optimization

### Caching Strategy

```typescript
class CartCacheManager {
  private cache: Map<string, { cart: Cart; timestamp: number }> = new Map();
  private readonly TTL = 5 * 60 * 1000; // 5 minutes

  /**
   * Get cart from cache
   */
  get(cartId: string): Cart | null {
    const cached = this.cache.get(cartId);

    if (!cached) {
      return null;
    }

    if (Date.now() - cached.timestamp > this.TTL) {
      this.cache.delete(cartId);
      return null;
    }

    return cached.cart;
  }

  /**
   * Set cart in cache
   */
  set(cartId: string, cart: Cart): void {
    this.cache.set(cartId, {
      cart,
      timestamp: Date.now(),
    });
  }

  /**
   * Invalidate cart cache
   */
  invalidate(cartId: string): void {
    this.cache.delete(cartId);
  }

  /**
   * Clear all cache
   */
  clear(): void {
    this.cache.clear();
  }
}
```

---

## Best Practices

### Cart Best Practices

```typescript
// 1. Always validate cart before checkout
async function validateBeforeCheckout(cartId: string): Promise<boolean> {
  const cart = await cartManager.getCart(cartId);
  const validator = new CartValidator(prisma);
  const validation = await validator.validateCart(cart);

  if (!validation.valid) {
    console.error('Cart validation failed:', validation.errors);
    return false;
  }

  if (validation.warnings.length > 0) {
    console.warn('Cart validation warnings:', validation.warnings);
  }

  return true;
}

// 2. Use optimistic updates for better UX
function optimisticUpdate(itemId: string, quantity: number) {
  // Update UI immediately
  dispatch(updateQuantityAction({ itemId, quantity }));

  // Then call API
  cartApi.updateQuantity({ itemId, quantity })
    .then(cart => dispatch(setCart(cart)))
    .catch(err => {
      // Revert on error
      dispatch(loadCart());
    });
}

// 3. Implement cart persistence
function persistCart(cart: Cart) {
  localStorage.setItem('cart', JSON.stringify(cart));
}

function loadPersistedCart(): Cart | null {
  const stored = localStorage.getItem('cart');
  return stored ? JSON.parse(stored) : null;
}

// 4. Handle price changes gracefully
async function handlePriceChanges(cart: Cart): Promise<Cart> {
  const updatedItems = [];

  for (const item of cart.items) {
    const product = await prisma.product.findUnique({
      where: { id: item.productId },
      include: { variants: true },
    });

    if (product) {
      const currentPrice = item.variantId
        ? product.variants.find(v => v.id === item.variantId)?.price
        : product.price;

      const currentSalePrice = item.variantId
        ? product.variants.find(v => v.id === item.variantId)?.salePrice
        : product.salePrice;

      updatedItems.push({
        ...item,
        price: currentPrice || item.price,
        salePrice: currentSalePrice,
      });
    }
  }

  return {
    ...cart,
    items: updatedItems,
  };
}

// 5. Implement cart limits
function validateCartLimits(cart: Cart): {
  valid: boolean;
  error?: string;
} {
  const MAX_ITEMS = 50;
  const MAX_QUANTITY = 10;

  if (cart.items.length > MAX_ITEMS) {
    return {
      valid: false,
      error: `Cart cannot contain more than ${MAX_ITEMS} items`,
    };
  }

  for (const item of cart.items) {
    if (item.quantity > MAX_QUANTITY) {
      return {
        valid: false,
        error: `Maximum quantity per item is ${MAX_QUANTITY}`,
      };
    }
  }

  return { valid: true };
}
```

---

---

## Quick Start

### Basic Shopping Cart

```typescript
interface CartItem {
  productId: string
  quantity: number
  price: number
}

class ShoppingCart {
  private items: CartItem[] = []
  
  addItem(productId: string, quantity: number, price: number) {
    const existing = this.items.find(item => item.productId === productId)
    if (existing) {
      existing.quantity += quantity
    } else {
      this.items.push({ productId, quantity, price })
    }
  }
  
  removeItem(productId: string) {
    this.items = this.items.filter(item => item.productId !== productId)
  }
  
  getTotal(): number {
    return this.items.reduce((sum, item) => sum + (item.price * item.quantity), 0)
  }
  
  getItemCount(): number {
    return this.items.reduce((sum, item) => sum + item.quantity, 0)
  }
}
```

### Cart Persistence

```typescript
// Save cart to localStorage (guest) or database (logged-in)
function saveCart(cart: ShoppingCart) {
  if (user.isLoggedIn()) {
    await api.saveCart(cart.items)
  } else {
    localStorage.setItem('cart', JSON.stringify(cart.items))
  }
}

// Load cart
function loadCart(): ShoppingCart {
  const cart = new ShoppingCart()
  if (user.isLoggedIn()) {
    const items = await api.getCart()
    cart.items = items
  } else {
    const items = JSON.parse(localStorage.getItem('cart') || '[]')
    cart.items = items
  }
  return cart
}
```

---

## Production Checklist

- [ ] **Cart State**: Manage cart state (localStorage or database)
- [ ] **Guest Cart**: Support guest cart with localStorage
- [ ] **Cart Merge**: Merge guest cart with user cart on login
- [ ] **Validation**: Validate cart items (stock, price, availability)
- [ ] **Price Calculation**: Accurate price calculations (tax, shipping, discounts)
- [ ] **Cart Persistence**: Persist cart across sessions
- [ ] **Cart Abandonment**: Track cart abandonment
- [ ] **Cart Recovery**: Email reminders for abandoned carts
- [ ] **Performance**: Optimize cart operations
- [ ] **Error Handling**: Handle cart errors gracefully
- [ ] **Testing**: Test cart operations thoroughly
- [ ] **Security**: Validate cart data server-side

---

## Anti-patterns

### ❌ Don't: Client-Side Only Validation

```typescript
// ❌ Bad - Only client validation
function addToCart(productId: string, quantity: number) {
  if (quantity > 0) {  // Client-side only!
    cart.addItem(productId, quantity)
  }
}
```

```typescript
// ✅ Good - Server-side validation
async function addToCart(productId: string, quantity: number) {
  // Validate on server
  const validation = await api.validateCartItem(productId, quantity)
  if (validation.valid) {
    cart.addItem(productId, quantity)
  } else {
    showError(validation.error)
  }
}
```

### ❌ Don't: No Cart Persistence

```typescript
// ❌ Bad - Cart lost on refresh
const cart = new ShoppingCart()  // Lost on page reload!
```

```typescript
// ✅ Good - Persist cart
const cart = loadCart()  // Load from storage

// Save on changes
cart.on('change', () => {
  saveCart(cart)
})
```

### ❌ Don't: Trust Client Prices

```typescript
// ❌ Bad - Use client price
cart.addItem(productId, quantity, clientPrice)  // Can be manipulated!
```

```typescript
// ✅ Good - Get price from server
const product = await api.getProduct(productId)
cart.addItem(productId, quantity, product.price)  // Server price
```

---

## Integration Points

- **Payment Gateways** (`30-ecommerce/payment-gateways/`) - Checkout integration
- **Order Management** (`30-ecommerce/order-management/`) - Order creation
- **Inventory Management** (`30-ecommerce/inventory-management/`) - Stock validation

---

## Further Reading

- [Stripe Checkout](https://stripe.com/docs/payments/checkout)
- [PayPal Checkout](https://developer.paypal.com/docs/checkout/)
- [Shopify Cart API](https://shopify.dev/api/admin-graphql/latest/objects/Cart)
- [WooCommerce Cart](https://woocommerce.github.io/woocommerce-rest-api-docs/)
