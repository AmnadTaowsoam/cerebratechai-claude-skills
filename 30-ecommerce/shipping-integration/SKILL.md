---
name: Shipping Carrier Integration
description: Integrating with shipping carriers for real-time rate calculation, label generation, tracking, and pickup scheduling with various shipping providers like FedEx, UPS, DHL, and USPS.
---

# Shipping Carrier Integration

> **Current Level:** Intermediate  
> **Domain:** E-commerce / Logistics

---

## Overview

Shipping carrier integration enables real-time shipping rate calculation, label generation, tracking, and pickup scheduling with various shipping providers. Effective integration includes address validation, rate comparison, label generation, and tracking updates.

---

## Core Concepts

### Table of Contents

1. [Shipping Concepts](#shipping-concepts)
2. [Carrier APIs](#carrier-apis)
3. [Rate Calculation](#rate-calculation)
4. [Address Validation](#address-validation)
5. [Label Generation](#label-generation)
6. [Tracking Integration](#tracking-integration)
7. [Pickup Scheduling](#pickup-scheduling)
8. [Shipping Zones](#shipping-zones)
9. [Shipping Methods](#shipping-methods)
10. [Free Shipping Rules](#free-shipping-rules)
11. [Multi-Carrier Support](#multi-carrier-support)
12. [Webhook Handling](#webhook-handling)
13. [Best Practices](#best-practices)

---

## Shipping Concepts

### Shipping Types

```typescript
enum ShippingMethodType {
  FLAT_RATE = 'flat_rate',
  FREE_SHIPPING = 'free_shipping',
  WEIGHT_BASED = 'weight_based',
  PRICE_BASED = 'price_based',
  CARRIER_RATE = 'carrier_rate',
  LOCAL_PICKUP = 'local_pickup',
}

enum CarrierType {
  THAILAND_POST = 'thailand_post',
  KERRY_EXPRESS = 'kerry_express',
  FLASH_EXPRESS = 'flash_express',
  J_T_EXPRESS = 'j_t_express',
  DHL = 'dhl',
  FEDEX = 'fedex',
  UPS = 'ups',
}

enum ShippingStatus {
  PENDING = 'pending',
  LABEL_CREATED = 'label_created',
  PICKED_UP = 'picked_up',
  IN_TRANSIT = 'in_transit',
  OUT_FOR_DELIVERY = 'out_for_delivery',
  DELIVERED = 'delivered',
  FAILED = 'failed',
  RETURNED = 'returned',
}
```

---

## Carrier APIs

### Carrier Service Interface

```typescript
interface CarrierService {
  calculateRate(params: RateRequest): Promise<RateResponse>;
  createShipment(params: ShipmentRequest): Promise<ShipmentResponse>;
  trackShipment(trackingNumber: string): Promise<TrackingResponse>;
  cancelShipment(trackingNumber: string): Promise<void>;
  schedulePickup(params: PickupRequest): Promise<PickupResponse>;
}

interface RateRequest {
  from: Address;
  to: Address;
  weight: number;
  dimensions: {
    length: number;
    width: number;
    height: number;
  };
  serviceType?: string;
}

interface RateResponse {
  carrier: string;
  serviceType: string;
  serviceName: string;
  rate: number;
  currency: string;
  estimatedDays: number;
}

interface ShipmentRequest {
  from: Address;
  to: Address;
  weight: number;
  dimensions: {
    length: number;
    width: number;
    height: number;
  };
  serviceType: string;
  referenceNumber?: string;
}

interface ShipmentResponse {
  trackingNumber: string;
  labelUrl: string;
  cost: number;
  currency: string;
}

interface TrackingResponse {
  trackingNumber: string;
  status: ShippingStatus;
  events: TrackingEvent[];
}

interface TrackingEvent {
  date: Date;
  status: string;
  location: string;
  description: string;
}
```

---

## Rate Calculation

### Rate Calculator

```typescript
class ShippingRateCalculator {
  private carriers: Map<string, CarrierService> = new Map();

  constructor() {
    this.registerCarriers();
  }

  /**
   * Register carriers
   */
  private registerCarriers(): void {
    this.carriers.set(CarrierType.THAILAND_POST, new ThailandPostService());
    this.carriers.set(CarrierType.KERRY_EXPRESS, new KerryExpressService());
    this.carriers.set(CarrierType.FLASH_EXPRESS, new FlashExpressService());
    this.carriers.set(CarrierType.J_T_EXPRESS, new JTExpressService());
    this.carriers.set(CarrierType.DHL, new DHLService());
    this.carriers.set(CarrierType.FEDEX, new FedExService());
  }

  /**
   * Calculate rates
   */
  async calculateRates(params: {
    from: Address;
    to: Address;
    weight: number;
    dimensions: {
      length: number;
      width: number;
      height: number;
    };
    carriers?: CarrierType[];
    serviceTypes?: string[];
  }): Promise<RateResponse[]> {
    const carrierTypes = params.carriers || Array.from(this.carriers.keys());
    const rates: RateResponse[] = [];

    for (const carrierType of carrierTypes) {
      const carrier = this.carriers.get(carrierType);

      if (!carrier) continue;

      try {
        const rate = await carrier.calculateRate({
          from: params.from,
          to: params.to,
          weight: params.weight,
          dimensions: params.dimensions,
        });

        // Filter by service type
        if (params.serviceTypes && !params.serviceTypes.includes(rate.serviceType)) {
          continue;
        }

        rates.push(rate);
      } catch (error) {
        console.error(`Error calculating rate for ${carrierType}:`, error);
      }
    }

    // Sort by rate
    return rates.sort((a, b) => a.rate - b.rate);
  }

  /**
   * Get cheapest rate
   */
  async getCheapestRate(params: {
    from: Address;
    to: Address;
    weight: number;
    dimensions: {
      length: number;
      width: number;
      height: number;
    };
  }): Promise<RateResponse | null> {
    const rates = await this.calculateRates(params);

    return rates.length > 0 ? rates[0] : null;
  }

  /**
   * Get fastest rate
   */
  async getFastestRate(params: {
    from: Address;
    to: Address;
    weight: number;
    dimensions: {
      length: number;
      width: number;
      height: number;
    };
  }): Promise<RateResponse | null> {
    const rates = await this.calculateRates(params);

    const sorted = rates.sort((a, b) => a.estimatedDays - b.estimatedDays);

    return sorted.length > 0 ? sorted[0] : null;
  }
}
```

---

## Address Validation

### Address Validator

```typescript
class AddressValidator {
  /**
   * Validate address
   */
  async validateAddress(address: Address): Promise<{
    valid: boolean;
    normalizedAddress?: Address;
    errors: string[];
  }> {
    const errors: string[] = [];

    // Check required fields
    if (!address.firstName) {
      errors.push('First name is required');
    }

    if (!address.lastName) {
      errors.push('Last name is required');
    }

    if (!address.address1) {
      errors.push('Address line 1 is required');
    }

    if (!address.city) {
      errors.push('City is required');
    }

    if (!address.country) {
      errors.push('Country is required');
    }

    if (!address.postalCode) {
      errors.push('Postal code is required');
    }

    if (!address.phone) {
      errors.push('Phone number is required');
    }

    // Validate phone format
    if (address.phone && !this.isValidPhone(address.phone)) {
      errors.push('Invalid phone number format');
    }

    // Validate postal code format
    if (address.postalCode && !this.isValidPostalCode(address.postalCode, address.country)) {
      errors.push('Invalid postal code format');
    }

    // Normalize address
    const normalizedAddress = errors.length === 0
      ? await this.normalizeAddress(address)
      : undefined;

    return {
      valid: errors.length === 0,
      normalizedAddress,
      errors,
    };
  }

  /**
   * Normalize address
   */
  private async normalizeAddress(address: Address): Promise<Address> {
    // Implement address normalization using carrier APIs
    return {
      ...address,
      firstName: address.firstName.trim(),
      lastName: address.lastName.trim(),
      address1: address.address1.trim(),
      address2: address.address2?.trim(),
      city: address.city.trim(),
      state: address.state?.trim(),
      country: address.country.trim().toUpperCase(),
      postalCode: address.postalCode.trim().toUpperCase(),
      phone: this.normalizePhone(address.phone),
    };
  }

  /**
   * Validate phone
   */
  private isValidPhone(phone: string): boolean {
    const phoneRegex = /^[\d\s\-\+\(\)]+$/;
    return phoneRegex.test(phone) && phone.replace(/\D/g, '').length >= 10;
  }

  /**
   * Validate postal code
   */
  private isValidPostalCode(postalCode: string, country: string): boolean {
    const patterns: Record<string, RegExp> = {
      TH: /^\d{5}$/,
      US: /^\d{5}(-\d{4})?$/,
      GB: /^[A-Z]{1,2}\d[A-Z\d]? \d[A-Z]{2}$/,
    };

    const pattern = patterns[country.toUpperCase()];

    return pattern ? pattern.test(postalCode) : true;
  }

  /**
   * Normalize phone
   */
  private normalizePhone(phone: string): string {
    return phone.replace(/\D/g, '');
  }
}
```

---

## Label Generation

### Label Generator

```typescript
class LabelGenerator {
  private carriers: Map<string, CarrierService> = new Map();

  constructor() {
    this.registerCarriers();
  }

  /**
   * Register carriers
   */
  private registerCarriers(): void {
    this.carriers.set(CarrierType.THAILAND_POST, new ThailandPostService());
    this.carriers.set(CarrierType.KERRY_EXPRESS, new KerryExpressService());
    this.carriers.set(CarrierType.FLASH_EXPRESS, new FlashExpressService());
    this.carriers.set(CarrierType.J_T_EXPRESS, new JTExpressService());
    this.carriers.set(CarrierType.DHL, new DHLService());
    this.carriers.set(CarrierType.FEDEX, new FedExService());
  }

  /**
   * Generate label
   */
  async generateLabel(params: {
    carrier: CarrierType;
    from: Address;
    to: Address;
    weight: number;
    dimensions: {
      length: number;
      width: number;
      height: number;
    };
    serviceType: string;
    referenceNumber?: string;
  }): Promise<{
    trackingNumber: string;
    labelUrl: string;
    cost: number;
  }> {
    const carrier = this.carriers.get(params.carrier);

    if (!carrier) {
      throw new Error(`Carrier ${params.carrier} not found`);
    }

    const shipment = await carrier.createShipment({
      from: params.from,
      to: params.to,
      weight: params.weight,
      dimensions: params.dimensions,
      serviceType: params.serviceType,
      referenceNumber: params.referenceNumber,
    });

    return {
      trackingNumber: shipment.trackingNumber,
      labelUrl: shipment.labelUrl,
      cost: shipment.cost,
    };
  }

  /**
   * Generate labels for fulfillment
   */
  async generateLabelsForFulfillment(params: {
    fulfillmentId: string;
  }): Promise<Array<{
    trackingNumber: string;
    labelUrl: string;
    cost: number;
  }>> {
    const fulfillment = await prisma.fulfillment.findUnique({
      where: { id: params.fulfillmentId },
      include: {
        order: {
          include: {
            shippingAddress: true,
          },
        },
        items: {
          include: {
            orderItem: {
              include: {
                product: true,
                variant: true,
              },
            },
          },
        },
      },
    });

    if (!fulfillment) {
      throw new Error('Fulfillment not found');
    }

    // Get warehouse address
    const warehouse = await prisma.warehouse.findFirst({
      where: { isDefault: true },
    });

    if (!warehouse) {
      throw new Error('No default warehouse found');
    }

    // Calculate total weight and dimensions
    const { weight, dimensions } = this.calculatePackageDetails(fulfillment.items);

    // Generate label
    const label = await this.generateLabel({
      carrier: fulfillment.carrier as CarrierType,
      from: warehouse.address,
      to: fulfillment.order.shippingAddress,
      weight,
      dimensions,
      serviceType: fulfillment.serviceType,
      referenceNumber: fulfillment.order.orderNumber,
    });

    // Update fulfillment
    await prisma.fulfillment.update({
      where: { id: params.fulfillmentId },
      data: {
        trackingNumber: label.trackingNumber,
        labelUrl: label.labelUrl,
        status: 'label_created',
      },
    });

    return [label];
  }

  /**
   * Calculate package details
   */
  private calculatePackageDetails(items: any[]): {
    weight: number;
    dimensions: {
      length: number;
      width: number;
      height: number;
    };
  } {
    let totalWeight = 0;
    let totalLength = 0;
    let totalWidth = 0;
    let totalHeight = 0;

    for (const item of items) {
      const product = item.orderItem.product;
      const variant = item.orderItem.variant;

      const weight = (variant?.weight || product?.weight || 0) * item.quantity;
      const length = variant?.length || product?.length || 0;
      const width = variant?.width || product?.width || 0;
      const height = variant?.height || product?.height || 0;

      totalWeight += weight;
      totalLength = Math.max(totalLength, length);
      totalWidth = Math.max(totalWidth, width);
      totalHeight = Math.max(totalHeight, height);
    }

    return {
      weight: totalWeight,
      dimensions: {
        length: totalLength,
        width: totalWidth,
        height: totalHeight,
      },
    };
  }
}
```

---

## Tracking Integration

### Tracking Manager

```typescript
class TrackingManager {
  private carriers: Map<string, CarrierService> = new Map();

  constructor() {
    this.registerCarriers();
  }

  /**
   * Register carriers
   */
  private registerCarriers(): void {
    this.carriers.set(CarrierType.THAILAND_POST, new ThailandPostService());
    this.carriers.set(CarrierType.KERRY_EXPRESS, new KerryExpressService());
    this.carriers.set(CarrierType.FLASH_EXPRESS, new FlashExpressService());
    this.carriers.set(CarrierType.J_T_EXPRESS, new JTExpressService());
    this.carriers.set(CarrierType.DHL, new DHLService());
    this.carriers.set(CarrierType.FEDEX, new FedExService());
  }

  /**
   * Track shipment
   */
  async trackShipment(trackingNumber: string): Promise<TrackingResponse> {
    const fulfillment = await prisma.fulfillment.findFirst({
      where: { trackingNumber },
    });

    if (!fulfillment) {
      throw new Error('Fulfillment not found');
    }

    const carrier = this.carriers.get(fulfillment.carrier as CarrierType);

    if (!carrier) {
      throw new Error(`Carrier ${fulfillment.carrier} not found`);
    }

    const tracking = await carrier.trackShipment(trackingNumber);

    // Update fulfillment status
    await this.updateFulfillmentStatus(trackingNumber, tracking.status);

    return tracking;
  }

  /**
   * Track multiple shipments
   */
  async trackShipments(trackingNumbers: string[]): Promise<TrackingResponse[]> {
    const trackings: TrackingResponse[] = [];

    for (const trackingNumber of trackingNumbers) {
      try {
        const tracking = await this.trackShipment(trackingNumber);
        trackings.push(tracking);
      } catch (error) {
        console.error(`Error tracking ${trackingNumber}:`, error);
      }
    }

    return trackings;
  }

  /**
   * Update fulfillment status
   */
  private async updateFulfillmentStatus(
    trackingNumber: string,
    status: ShippingStatus
  ): Promise<void> {
    await prisma.fulfillment.updateMany({
      where: { trackingNumber },
      data: { status },
    });
  }
}
```

---

## Pickup Scheduling

### Pickup Scheduler

```typescript
class PickupScheduler {
  private carriers: Map<string, CarrierService> = new Map();

  constructor() {
    this.registerCarriers();
  }

  /**
   * Register carriers
   */
  private registerCarriers(): void {
    this.carriers.set(CarrierType.THAILAND_POST, new ThailandPostService());
    this.carriers.set(CarrierType.KERRY_EXPRESS, new KerryExpressService());
    this.carriers.set(CarrierType.FLASH_EXPRESS, new FlashExpressService());
    this.carriers.set(CarrierType.J_T_EXPRESS, new JTExpressService());
    this.carriers.set(CarrierType.DHL, new DHLService());
    this.carriers.set(CarrierType.FEDEX, new FedExService());
  }

  /**
   * Schedule pickup
   */
  async schedulePickup(params: {
    carrier: CarrierType;
    from: Address;
    trackingNumbers: string[];
    scheduledDate: Date;
    instructions?: string;
  }): Promise<PickupResponse> {
    const carrier = this.carriers.get(params.carrier);

    if (!carrier) {
      throw new Error(`Carrier ${params.carrier} not found`);
    }

    const pickup = await carrier.schedulePickup({
      from: params.from,
      trackingNumbers: params.trackingNumbers,
      scheduledDate: params.scheduledDate,
      instructions: params.instructions,
    });

    return pickup;
  }

  /**
   * Schedule pickup for fulfillment
   */
  async schedulePickupForFulfillment(params: {
    fulfillmentId: string;
    scheduledDate: Date;
    instructions?: string;
  }): Promise<PickupResponse> {
    const fulfillment = await prisma.fulfillment.findUnique({
      where: { id: params.fulfillmentId },
      include: {
        order: {
          include: {
            shippingAddress: true,
          },
        },
      },
    });

    if (!fulfillment) {
      throw new Error('Fulfillment not found');
    }

    const warehouse = await prisma.warehouse.findFirst({
      where: { isDefault: true },
    });

    if (!warehouse) {
      throw new Error('No default warehouse found');
    }

    const pickup = await this.schedulePickup({
      carrier: fulfillment.carrier as CarrierType,
      from: warehouse.address,
      trackingNumbers: [fulfillment.trackingNumber],
      scheduledDate: params.scheduledDate,
      instructions: params.instructions,
    });

    // Update fulfillment
    await prisma.fulfillment.update({
      where: { id: params.fulfillmentId },
      data: {
        pickupScheduledAt: new Date(),
        pickupDate: params.scheduledDate,
      },
    });

    return pickup;
  }
}
```

---

## Shipping Zones

### Zone Manager

```typescript
class ShippingZoneManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create zone
   */
  async createZone(params: {
    name: string;
    countries: string[];
    regions?: Array<{
      country: string;
      states?: string[];
      postalCodes?: string[];
    }>;
  }): Promise<ShippingZone> {
    return await this.prisma.shippingZone.create({
      data: {
        name: params.name,
        countries: params.countries,
        regions: params.regions || [],
      },
    });
  }

  /**
   * Get zone for address
   */
  async getZoneForAddress(address: Address): Promise<ShippingZone | null> {
    const zones = await this.prisma.shippingZone.findMany({
      include: { methods: true },
    });

    for (const zone of zones) {
      if (this.addressInZone(address, zone)) {
        return zone;
      }
    }

    return null;
  }

  /**
   * Check if address is in zone
   */
  private addressInZone(address: Address, zone: ShippingZone): boolean {
    // Check country
    if (!zone.countries.includes(address.country)) {
      return false;
    }

    // Check regions
    if (zone.regions && zone.regions.length > 0) {
      for (const region of zone.regions) {
        if (region.country === address.country) {
          // Check states
          if (region.states && region.states.length > 0) {
            if (!address.state || !region.states.includes(address.state)) {
              continue;
            }
          }

          // Check postal codes
          if (region.postalCodes && region.postalCodes.length > 0) {
            if (!this.postalCodeInList(address.postalCode, region.postalCodes)) {
              continue;
            }
          }

          return true;
        }
      }

      return false;
    }

    return true;
  }

  /**
   * Check if postal code is in list
   */
  private postalCodeInList(postalCode: string, postalCodes: string[]): boolean {
    for (const pc of postalCodes) {
      if (pc.includes('*')) {
        const pattern = pc.replace(/\*/g, '.*');
        const regex = new RegExp(`^${pattern}$`);
        if (regex.test(postalCode)) {
          return true;
        }
      } else if (pc === postalCode) {
        return true;
      }
    }

    return false;
  }

  /**
   * Get zones
   */
  async getZones(): Promise<ShippingZone[]> {
    return await this.prisma.shippingZone.findMany({
      include: { methods: true },
      orderBy: { name: 'asc' },
    });
  }
}
```

---

## Shipping Methods

### Method Manager

```typescript
class ShippingMethodManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create method
   */
  async createMethod(params: {
    zoneId: string;
    name: string;
    type: ShippingMethodType;
    cost?: number;
    freeThreshold?: number;
    carrier?: CarrierType;
    serviceType?: string;
    enabled?: boolean;
  }): Promise<ShippingMethod> {
    return await this.prisma.shippingMethod.create({
      data: {
        zoneId: params.zoneId,
        name: params.name,
        type: params.type,
        cost: params.cost,
        freeThreshold: params.freeThreshold,
        carrier: params.carrier,
        serviceType: params.serviceType,
        enabled: params.enabled !== false,
      },
    });
  }

  /**
   * Get available methods for address
   */
  async getAvailableMethods(params: {
    address: Address;
    cartTotal?: number;
    cartWeight?: number;
  }): Promise<ShippingMethod[]> {
    const zoneManager = new ShippingZoneManager(this.prisma);
    const zone = await zoneManager.getZoneForAddress(params.address);

    if (!zone) {
      return [];
    }

    const methods = await this.prisma.shippingMethod.findMany({
      where: {
        zoneId: zone.id,
        enabled: true,
      },
    });

    // Filter by conditions
    return methods.filter(method => {
      // Check free shipping threshold
      if (method.freeThreshold && params.cartTotal) {
        return params.cartTotal >= method.freeThreshold;
      }

      return true;
    });
  }

  /**
   * Calculate method cost
   */
  async calculateMethodCost(
    methodId: string,
    params: {
      cartTotal?: number;
      cartWeight?: number;
    }
  ): Promise<number> {
    const method = await this.prisma.shippingMethod.findUnique({
      where: { id: methodId },
    });

    if (!method) {
      throw new Error('Method not found');
    }

    // Check free shipping
    if (method.freeThreshold && params.cartTotal >= method.freeThreshold) {
      return 0;
    }

    switch (method.type) {
      case ShippingMethodType.FLAT_RATE:
        return method.cost || 0;

      case ShippingMethodType.FREE_SHIPPING:
        return 0;

      case ShippingMethodType.WEIGHT_BASED:
        return this.calculateWeightBasedCost(method, params.cartWeight || 0);

      case ShippingMethodType.PRICE_BASED:
        return this.calculatePriceBasedCost(method, params.cartTotal || 0);

      case ShippingMethodType.CARRIER_RATE:
        return await this.calculateCarrierRate(method, params);

      default:
        return method.cost || 0;
    }
  }

  /**
   * Calculate weight-based cost
   */
  private calculateWeightBasedCost(method: any, weight: number): number {
    if (!method.weightBasedRates) {
      return method.cost || 0;
    }

    const rates = method.weightBasedRates.sort((a: any, b: any) => b.weight - a.weight);

    for (const rate of rates) {
      if (weight >= rate.weight) {
        return rate.cost;
      }
    }

    return rates[rates.length - 1]?.cost || 0;
  }

  /**
   * Calculate price-based cost
   */
  private calculatePriceBasedCost(method: any, price: number): number {
    if (!method.priceBasedRates) {
      return method.cost || 0;
    }

    const rates = method.priceBasedRates.sort((a: any, b: any) => b.price - a.price);

    for (const rate of rates) {
      if (price >= rate.price) {
        return rate.cost;
      }
    }

    return rates[rates.length - 1]?.cost || 0;
  }

  /**
   * Calculate carrier rate
   */
  private async calculateCarrierRate(
    method: any,
    params: { cartTotal?: number; cartWeight?: number }
  ): Promise<number> {
    const rateCalculator = new ShippingRateCalculator();

    // Get warehouse address
    const warehouse = await this.prisma.warehouse.findFirst({
      where: { isDefault: true },
    });

    if (!warehouse) {
      throw new Error('No default warehouse found');
    }

    // Calculate rate
    const rate = await rateCalculator.calculateRate({
      from: warehouse.address,
      to: params.address,
      weight: params.cartWeight || 0,
      dimensions: { length: 0, width: 0, height: 0 },
      carriers: [method.carrier],
      serviceTypes: method.serviceType ? [method.serviceType] : undefined,
    });

    return rate[0]?.rate || method.cost || 0;
  }
}
```

---

## Free Shipping Rules

### Free Shipping Manager

```typescript
class FreeShippingManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Check if eligible for free shipping
   */
  async isEligibleForFreeShipping(params: {
    cartTotal: number;
    address: Address;
    userId?: string;
  }): Promise<{
    eligible: boolean;
    rule?: FreeShippingRule;
    remainingAmount?: number;
  }> {
    const rules = await this.getActiveRules();

    for (const rule of rules) {
      if (this.matchesRule(rule, params)) {
        const remainingAmount = Math.max(0, rule.minAmount - params.cartTotal);

        return {
          eligible: remainingAmount === 0,
          rule,
          remainingAmount,
        };
      }
    }

    return {
      eligible: false,
    };
  }

  /**
   * Get active rules
   */
  private async getActiveRules(): Promise<FreeShippingRule[]> {
    return await this.prisma.freeShippingRule.findMany({
      where: {
        active: true,
        OR: [
          { startDate: null },
          { startDate: { lte: new Date() } },
        ],
        AND: [
          { endDate: null },
          { endDate: { gte: new Date() } },
        ],
      },
    });
  }

  /**
   * Check if rule matches
   */
  private matchesRule(rule: FreeShippingRule, params: {
    cartTotal: number;
    address: Address;
    userId?: string;
  }): boolean {
    // Check minimum amount
    if (params.cartTotal < rule.minAmount) {
      return false;
    }

    // Check countries
    if (rule.countries && rule.countries.length > 0) {
      if (!rule.countries.includes(params.address.country)) {
        return false;
      }
    }

    // Check user segments
    if (rule.userSegments && rule.userSegments.length > 0) {
      if (!params.userId) {
        return false;
      }

      const userSegments = await this.getUserSegments(params.userId);
      const hasRequiredSegment = rule.userSegments.some(segment =>
        userSegments.includes(segment)
      );

      if (!hasRequiredSegment) {
        return false;
      }
    }

    return true;
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

## Multi-Carrier Support

### Carrier Manager

```typescript
class CarrierManager {
  private carriers: Map<string, CarrierService> = new Map();

  constructor() {
    this.registerCarriers();
  }

  /**
   * Register carriers
   */
  private registerCarriers(): void {
    this.carriers.set(CarrierType.THAILAND_POST, new ThailandPostService());
    this.carriers.set(CarrierType.KERRY_EXPRESS, new KerryExpressService());
    this.carriers.set(CarrierType.FLASH_EXPRESS, new FlashExpressService());
    this.carriers.set(CarrierType.J_T_EXPRESS, new JTExpressService());
    this.carriers.set(CarrierType.DHL, new DHLService());
    this.carriers.set(CarrierType.FEDEX, new FedExService());
  }

  /**
   * Get available carriers
   */
  getAvailableCarriers(): CarrierType[] {
    return Array.from(this.carriers.keys());
  }

  /**
   * Get carrier
   */
  getCarrier(carrierType: CarrierType): CarrierService | undefined {
    return this.carriers.get(carrierType);
  }

  /**
   * Get best carrier for shipment
   */
  async getBestCarrier(params: {
    from: Address;
    to: Address;
    weight: number;
    dimensions: {
      length: number;
      width: number;
      height: number;
    };
    priority?: 'cost' | 'speed';
  }): Promise<{
    carrier: CarrierType;
    rate: RateResponse;
  } | null> {
    const rateCalculator = new ShippingRateCalculator();
    const rates = await rateCalculator.calculateRates(params);

    if (rates.length === 0) {
      return null;
    }

    let selectedRate: RateResponse;

    if (params.priority === 'speed') {
      const sorted = rates.sort((a, b) => a.estimatedDays - b.estimatedDays);
      selectedRate = sorted[0];
    } else {
      selectedRate = rates[0]; // Already sorted by cost
    }

    return {
      carrier: selectedRate.carrier as CarrierType,
      rate: selectedRate,
    };
  }
}
```

---

## Webhook Handling

### Webhook Handler

```typescript
class ShippingWebhookHandler {
  /**
   * Handle carrier webhook
   */
  async handleWebhook(params: {
    carrier: CarrierType;
    payload: any;
  }): Promise<void> {
    switch (params.carrier) {
      case CarrierType.THAILAND_POST:
        await this.handleThailandPostWebhook(params.payload);
        break;
      case CarrierType.KERRY_EXPRESS:
        await this.handleKerryExpressWebhook(params.payload);
        break;
      case CarrierType.FLASH_EXPRESS:
        await this.handleFlashExpressWebhook(params.payload);
        break;
      case CarrierType.J_T_EXPRESS:
        await this.handleJTExpressWebhook(params.payload);
        break;
      case CarrierType.DHL:
        await this.handleDHLWebhook(params.payload);
        break;
      case CarrierType.FEDEX:
        await this.handleFedExWebhook(params.payload);
        break;
    }
  }

  /**
   * Handle tracking update
   */
  private async handleTrackingUpdate(params: {
    trackingNumber: string;
    status: ShippingStatus;
    event: TrackingEvent;
  }): Promise<void> {
    // Update fulfillment
    const fulfillment = await prisma.fulfillment.findFirst({
      where: { trackingNumber: params.trackingNumber },
    });

    if (fulfillment) {
      await prisma.fulfillment.update({
        where: { id: fulfillment.id },
        data: { status: params.status },
      });

      // Create tracking event
      await prisma.trackingEvent.create({
        data: {
          fulfillmentId: fulfillment.id,
          status: params.status,
          location: params.event.location,
          description: params.event.description,
          eventDate: params.event.date,
        },
      });
    }
  }

  private async handleThailandPostWebhook(payload: any): Promise<void> {
    // Implement Thailand Post webhook handling
  }

  private async handleKerryExpressWebhook(payload: any): Promise<void> {
    // Implement Kerry Express webhook handling
  }

  private async handleFlashExpressWebhook(payload: any): Promise<void> {
    // Implement Flash Express webhook handling
  }

  private async handleJTExpressWebhook(payload: any): Promise<void> {
    // Implement J&T Express webhook handling
  }

  private async handleDHLWebhook(payload: any): Promise<void> {
    // Implement DHL webhook handling
  }

  private async handleFedExWebhook(payload: any): Promise<void> {
    // Implement FedEx webhook handling
  }
}
```

---

## Best Practices

### Shipping Best Practices

```typescript
// 1. Always validate addresses before shipping
async function validateBeforeShipping(address: Address): Promise<boolean> {
  const validator = new AddressValidator();
  const result = await validator.validateAddress(address);

  return result.valid;
}

// 2. Use proper packaging dimensions
async function calculatePackageDimensions(items: OrderItem[]): {
  length: number;
  width: number;
  height: number;
  weight: number;
} {
  let totalWeight = 0;
  let maxLength = 0;
  let maxWidth = 0;
  let maxHeight = 0;

  for (const item of items) {
    const product = item.product;
    const variant = item.variant;

    totalWeight += (variant?.weight || product?.weight || 0) * item.quantity;
    maxLength = Math.max(maxLength, variant?.length || product?.length || 0);
    maxWidth = Math.max(maxWidth, variant?.width || product?.width || 0);
    maxHeight = Math.max(maxHeight, variant?.height || product?.height || 0);
  }

  return {
    length: maxLength,
    width: maxWidth,
    height: maxHeight,
    weight: totalWeight,
  };
}

// 3. Implement proper tracking updates
async function updateTracking(trackingNumber: string): Promise<void> {
  const trackingManager = new TrackingManager();
  const tracking = await trackingManager.trackShipment(trackingNumber);

  // Update fulfillment status
  await prisma.fulfillment.updateMany({
    where: { trackingNumber },
    data: { status: tracking.status },
  });
}

// 4. Use proper error handling for carrier APIs
async function callCarrierAPI<T>(
  carrierFn: () => Promise<T>
): Promise<T | null> {
  try {
    return await carrierFn();
  } catch (error) {
    console.error('Carrier API error:', error);
    return null;
  }
}

// 5. Implement proper fallback carriers
async function getShippingRateWithFallback(params: RateRequest): Promise<RateResponse | null> {
  const carriers = [CarrierType.THAILAND_POST, CarrierType.KERRY_EXPRESS, CarrierType.FLASH_EXPRESS];

  for (const carrier of carriers) {
    try {
      const carrierService = new CarrierManager().getCarrier(carrier);
      if (carrierService) {
        const rate = await carrierService.calculateRate(params);
        return rate;
      }
    } catch (error) {
      console.error(`Error with ${carrier}:`, error);
      continue;
    }
  }

  return null;
}
```

---

---

## Quick Start

### Shipping Rate Calculation

```typescript
interface ShippingRate {
  carrier: string
  service: string
  rate: number
  estimatedDays: number
}

async function calculateShippingRates(
  origin: Address,
  destination: Address,
  weight: number,
  dimensions: Dimensions
): Promise<ShippingRate[]> {
  const carriers = ['fedex', 'ups', 'usps']
  const rates: ShippingRate[] = []
  
  for (const carrier of carriers) {
    const rate = await getCarrierRate(carrier, {
      origin,
      destination,
      weight,
      dimensions
    })
    rates.push(rate)
  }
  
  return rates.sort((a, b) => a.rate - b.rate)
}
```

### Label Generation

```typescript
async function generateShippingLabel(
  orderId: string,
  carrier: string,
  service: string
): Promise<string> {
  const order = await getOrder(orderId)
  
  const label = await carrierAPI.createLabel({
    carrier,
    service,
    from: order.originAddress,
    to: order.shippingAddress,
    weight: order.totalWeight,
    dimensions: order.dimensions
  })
  
  await saveTrackingNumber(orderId, label.trackingNumber)
  return label.labelUrl
}
```

---

## Production Checklist

- [ ] **Carrier APIs**: Integrate with shipping carriers
- [ ] **Rate Calculation**: Real-time rate calculation
- [ ] **Address Validation**: Validate shipping addresses
- [ ] **Label Generation**: Generate shipping labels
- [ ] **Tracking**: Track shipments
- [ ] **Multi-Carrier**: Support multiple carriers
- [ ] **Rate Comparison**: Compare rates across carriers
- [ ] **Webhooks**: Handle carrier webhooks
- [ ] **Error Handling**: Handle carrier errors
- [ ] **Testing**: Test with real carriers
- [ ] **Documentation**: Document integration
- [ ] **Monitoring**: Monitor carrier API health

---

## Anti-patterns

### ❌ Don't: No Address Validation

```typescript
// ❌ Bad - No validation
const rate = await calculateRate({
  address: userInput  // Could be invalid!
})
```

```typescript
// ✅ Good - Validate first
const validated = await validateAddress(userInput)
if (!validated.valid) {
  throw new Error('Invalid address')
}
const rate = await calculateRate({ address: validated.address })
```

### ❌ Don't: No Fallback

```typescript
// ❌ Bad - Single carrier
const rate = await fedex.calculateRate(params)
// What if FedEx fails?
```

```typescript
// ✅ Good - Multiple carriers
const carriers = ['fedex', 'ups', 'usps']
for (const carrier of carriers) {
  try {
    const rate = await getCarrierRate(carrier, params)
    return rate
  } catch (error) {
    continue  // Try next carrier
  }
}
```

---

## Integration Points

- **Order Fulfillment** (`30-ecommerce/order-fulfillment/`) - Fulfillment workflow
- **Order Management** (`30-ecommerce/order-management/`) - Order tracking
- **Payment Gateways** (`30-ecommerce/payment-gateways/`) - Payment processing

---

## Further Reading

- [FedEx API](https://developer.fedex.com/)
- [UPS API](https://developer.ups.com/)
- [USPS API](https://www.usps.com/business/web-tools-apis/)

## Resources

- [Thailand Post API](https://track.thailandpost.co.th/)
- [Kerry Express API](https://www.kerryexpress.com/)
- [Flash Express API](https://www.flashexpress.com/)
- [J&T Express API](https://www.jtexpress.co.th/)
- [DHL API](https://developer.dhl.com/)
- [FedEx API](https://developer.fedex.com/)
