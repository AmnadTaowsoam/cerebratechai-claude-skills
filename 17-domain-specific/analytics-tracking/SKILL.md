# Analytics and Event Tracking

## Overview

Analytics and event tracking help understand user behavior and measure product success. This skill covers analytics platforms (Google Analytics 4, Mixpanel, Segment), event tracking, user properties, custom dimensions, e-commerce tracking, privacy considerations, server-side tracking, data validation, testing analytics, and best practices.

## Table of Contents

1. [Analytics Platforms](#analytics-platforms)
   - [Google Analytics 4](#google-analytics-4)
   - [Mixpanel](#mixpanel)
   - [Segment](#segment)
2. [Event Tracking](#event-tracking)
3. [User Properties](#user-properties)
4. [Custom Dimensions](#custom-dimensions)
5. [E-commerce Tracking](#e-commerce-tracking)
6. [Privacy Considerations](#privacy-considerations)
7. [Server-Side Tracking](#server-side-tracking)
8. [Data Validation](#data-validation)
9. [Testing Analytics](#testing-analytics)
10. [Best Practices](#best-practices)

---

## Analytics Platforms

### Google Analytics 4

#### Setup

```typescript
// src/analytics/ga4.ts
// Install: npm install @gtag/js

export const GA4_MEASUREMENT_ID = process.env.NEXT_PUBLIC_GA4_MEASUREMENT_ID || '';

export function initGA4(): void {
  if (typeof window === 'undefined' || !GA4_MEASUREMENT_ID) {
    return;
  }

  // Load GA4 script
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA4_MEASUREMENT_ID}`;
  document.head.appendChild(script);

  // Initialize GA4
  (window as any).dataLayer = (window as any).dataLayer || [];
  (window as any).gtag('js', new Date());
  (window as any).gtag('config', GA4_MEASUREMENT_ID);
}

export function trackEvent(eventName: string, parameters?: Record<string, any>): void {
  if (typeof window === 'undefined') {
    return;
  }

  (window as any).gtag('event', eventName, parameters);
}

export function trackPageView(pagePath: string, pageTitle: string): void {
  if (typeof window === 'undefined') {
    return;
  }

  (window as any).gtag('event', 'page_view', {
    page_path: pagePath,
    page_title: pageTitle,
  });
}

export function setUser(userId: string): void {
  if (typeof window === 'undefined') {
    return;
  }

  (window as any).gtag('config', GA4_MEASUREMENT_ID, {
    user_id: userId,
  });
}

export function setUserProperties(properties: Record<string, any>): void {
  if (typeof window === 'undefined') {
    return;
  }

  (window as any).gtag('set', 'user_properties', properties);
}
```

#### Usage in React

```typescript
// src/components/App.tsx
import { useEffect } from 'react';
import { initGA4, trackPageView } from '../analytics/ga4';
import { useRouter } from 'next/router';

export function App() {
  const router = useRouter();

  useEffect(() => {
    // Initialize GA4
    initGA4();

    // Track page views
    const handleRouteChange = (url: string) => {
      trackPageView(url, document.title);
    };

    router.events.on('routeChangeComplete', handleRouteChange);

    // Track initial page view
    handleRouteChange(router.pathname);

    return () => {
      router.events.off('routeChangeComplete', handleRouteChange);
    };
  }, [router]);

  return <div>Your App</div>;
}
```

### Mixpanel

#### Setup

```typescript
// src/analytics/mixpanel.ts
// Install: npm install mixpanel-browser

import mixpanel from 'mixpanel-browser';

const MIXPANEL_TOKEN = process.env.NEXT_PUBLIC_MIXPANEL_TOKEN || '';

export function initMixpanel(): void {
  if (typeof window === 'undefined' || !MIXPANEL_TOKEN) {
    return;
  }

  mixpanel.init(MIXPANEL_TOKEN, {
    debug: process.env.NODE_ENV === 'development',
    track_pageview: true,
    persistence: 'localStorage',
  });
}

export function trackEvent(eventName: string, properties?: Record<string, any>): void {
  if (typeof window === 'undefined') {
    return;
  }

  mixpanel.track(eventName, properties);
}

export function identify(userId: string): void {
  if (typeof window === 'undefined') {
    return;
  }

  mixpanel.identify(userId);
}

export function setUserProperties(properties: Record<string, any>): void {
  if (typeof window === 'undefined') {
    return;
  }

  mixpanel.people.set(properties);
}

export function alias(distinctId: string, alias: string): void {
  if (typeof window === 'undefined') {
    return;
  }

  mixpanel.alias(alias, distinctId);
}

export function reset(): void {
  if (typeof window === 'undefined') {
    return;
  }

  mixpanel.reset();
}
```

#### Usage in React

```typescript
// src/components/Button.tsx
import { trackEvent } from '../analytics/mixpanel';

interface ButtonProps {
  onClick?: () => void;
  eventName?: string;
  eventProperties?: Record<string, any>;
}

export function Button({ onClick, eventName, eventProperties, children }: ButtonProps) {
  const handleClick = () => {
    if (eventName) {
      trackEvent(eventName, eventProperties);
    }
    onClick?.();
  };

  return <button onClick={handleClick}>{children}</button>;
}

// Usage
<Button
  eventName="button_clicked"
  eventProperties={{ button_name: 'submit', page: 'checkout' }}
>
  Submit
</Button>
```

### Segment

#### Setup

```typescript
// src/analytics/segment.ts
// Install: npm install @segment/analytics-next

import { AnalyticsBrowser } from '@segment/analytics-next';

const SEGMENT_WRITE_KEY = process.env.NEXT_PUBLIC_SEGMENT_WRITE_KEY || '';

export const analytics = new AnalyticsBrowser();

export async function initSegment(): Promise<void> {
  if (typeof window === 'undefined' || !SEGMENT_WRITE_KEY) {
    return;
  }

  await analytics.load({ writeKey: SEGMENT_WRITE_KEY });
}

export function trackEvent(eventName: string, properties?: Record<string, any>): void {
  if (typeof window === 'undefined') {
    return;
  }

  analytics.track(eventName, properties);
}

export function identify(userId: string, traits?: Record<string, any>): void {
  if (typeof window === 'undefined') {
    return;
  }

  analytics.identify(userId, traits);
}

export function page(category?: string, name?: string, properties?: Record<string, any>): void {
  if (typeof window === 'undefined') {
    return;
  }

  analytics.page(category, name, properties);
}

export function group(groupId: string, traits?: Record<string, any>): void {
  if (typeof window === 'undefined') {
    return;
  }

  analytics.group(groupId, traits);
}

export function alias(userId: string, previousId?: string): void {
  if (typeof window === 'undefined') {
    return;
  }

  analytics.alias(userId, previousId);
}
```

#### Usage in React

```typescript
// src/components/SignupForm.tsx
import { useState } from 'react';
import { identify, trackEvent } from '../analytics/segment';

export function SignupForm() {
  const [email, setEmail] = useState('');
  const [name, setName] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Identify user
    identify(email, {
      name,
      email,
      signupDate: new Date().toISOString(),
    });

    // Track signup event
    trackEvent('user_signed_up', {
      method: 'email',
      plan: 'free',
    });

    // Submit form...
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
      />
      <button type="submit">Sign Up</button>
    </form>
  );
}
```

---

## Event Tracking

### Event Naming Conventions

```typescript
// src/analytics/event-naming.ts
export const AnalyticsEvents = {
  // User actions
  USER_SIGNED_UP: 'user_signed_up',
  USER_LOGGED_IN: 'user_logged_in',
  USER_LOGGED_OUT: 'user_logged_out',
  
  // Page interactions
  PAGE_VIEWED: 'page_viewed',
  BUTTON_CLICKED: 'button_clicked',
  LINK_CLICKED: 'link_clicked',
  FORM_SUBMITTED: 'form_submitted',
  
  // E-commerce
  PRODUCT_VIEWED: 'product_viewed',
  PRODUCT_ADDED_TO_CART: 'product_added_to_cart',
  PRODUCT_REMOVED_FROM_CART: 'product_removed_from_cart',
  CHECKOUT_STARTED: 'checkout_started',
  CHECKOUT_COMPLETED: 'checkout_completed',
  ORDER_PLACED: 'order_placed',
  
  // Content
  ARTICLE_VIEWED: 'article_viewed',
  VIDEO_PLAYED: 'video_played',
  VIDEO_PAUSED: 'video_paused',
  VIDEO_COMPLETED: 'video_completed',
  
  // Search
  SEARCH_PERFORMED: 'search_performed',
  SEARCH_RESULT_CLICKED: 'search_result_clicked',
} as const;
```

### Event Tracking Hook

```typescript
// src/hooks/useAnalytics.ts
import { useCallback } from 'react';
import { trackEvent as gaTrackEvent } from '../analytics/ga4';
import { trackEvent as mixpanelTrackEvent } from '../analytics/mixpanel';
import { trackEvent as segmentTrackEvent } from '../analytics/segment';

export function useAnalytics() {
  const trackEvent = useCallback((
    eventName: string,
    properties?: Record<string, any>
  ) => {
    // Track in GA4
    gaTrackEvent(eventName, properties);
    
    // Track in Mixpanel
    mixpanelTrackEvent(eventName, properties);
    
    // Track in Segment
    segmentTrackEvent(eventName, properties);
  }, []);

  const trackPageView = useCallback((
    pagePath: string,
    pageTitle: string
  ) => {
    gaTrackEvent('page_view', {
      page_path: pagePath,
      page_title: pageTitle,
    });
  }, []);

  const identifyUser = useCallback((userId: string, traits?: Record<string, any>) => {
    // Identify in Mixpanel
    mixpanel.identify(userId);
    
    // Identify in Segment
    segmentTrackEvent('identify', { userId, ...traits });
  }, []);

  const setUserProperties = useCallback((properties: Record<string, any>) => {
    // Set user properties in Mixpanel
    mixpanel.setUserProperties(properties);
    
    // Set user properties in Segment
    segmentTrackEvent('set_user_properties', properties);
  }, []);

  return {
    trackEvent,
    trackPageView,
    identifyUser,
    setUserProperties,
  };
}
```

### Usage Example

```typescript
// src/components/ProductCard.tsx
import { useAnalytics } from '../hooks/useAnalytics';

interface ProductCardProps {
  product: {
    id: string;
    name: string;
    price: number;
    category: string;
  };
}

export function ProductCard({ product }: ProductCardProps) {
  const { trackEvent } = useAnalytics();

  const handleView = () => {
    trackEvent('product_viewed', {
      product_id: product.id,
      product_name: product.name,
      product_price: product.price,
      product_category: product.category,
    });
  };

  const handleAddToCart = () => {
    trackEvent('product_added_to_cart', {
      product_id: product.id,
      product_name: product.name,
      product_price: product.price,
      product_category: product.category,
    });
  };

  return (
    <div className="product-card">
      <h3>{product.name}</h3>
      <p>${product.price}</p>
      <button onClick={handleView}>View Details</button>
      <button onClick={handleAddToCart}>Add to Cart</button>
    </div>
  );
}
```

---

## User Properties

### User Property Tracking

```typescript
// src/analytics/user-properties.ts
export interface UserProperties {
  // Basic info
  userId?: string;
  email?: string;
  name?: string;
  
  // Demographics
  age?: number;
  gender?: string;
  country?: string;
  city?: string;
  
  // Account info
  plan?: 'free' | 'basic' | 'premium' | 'enterprise';
  signupDate?: string;
  lastLoginDate?: string;
  
  // Usage
  totalOrders?: number;
  totalSpent?: number;
  lastOrderDate?: string;
  
  // Preferences
  language?: string;
  currency?: string;
  timezone?: string;
}

export function setUserProperties(properties: UserProperties): void {
  // Set in GA4
  (window as any).gtag('set', 'user_properties', properties);
  
  // Set in Mixpanel
  mixpanel.people.set(properties);
  
  // Set in Segment
  analytics.identify(properties.userId, properties);
}

export function incrementUserProperty(property: string, value: number): void {
  // Increment in Mixpanel
  mixpanel.people.increment(property, value);
}

export function setUserPropertyOnce(property: string, value: any): void {
  // Set once in Mixpanel
  mixpanel.people.set_once(property, value);
}

export function appendUserProperty(property: string, value: any): void {
  // Append in Mixpanel
  mixpanel.people.union(property, value);
}
```

### Usage Example

```typescript
// src/components/Profile.tsx
import { useEffect } from 'react';
import { setUserProperties } from '../analytics/user-properties';

export function Profile({ user }: { user: User }) {
  useEffect(() => {
    setUserProperties({
      userId: user.id,
      email: user.email,
      name: user.name,
      plan: user.plan,
      signupDate: user.createdAt,
      lastLoginDate: user.lastLoginAt,
      totalOrders: user.orderCount,
      totalSpent: user.totalSpent,
      language: user.language,
      currency: user.currency,
    });
  }, [user]);

  return (
    <div>
      <h1>{user.name}</h1>
      <p>Email: {user.email}</p>
      <p>Plan: {user.plan}</p>
    </div>
  );
}
```

---

## Custom Dimensions

### GA4 Custom Dimensions

```typescript
// src/analytics/custom-dimensions.ts
export const CustomDimensions = {
  // User-scoped custom dimensions
  USER_PLAN: 'custom_dimension_1',
  USER_TIER: 'custom_dimension_2',
  USER_SIGNUP_SOURCE: 'custom_dimension_3',
  
  // Event-scoped custom dimensions
  EVENT_CATEGORY: 'custom_dimension_4',
  EVENT_LABEL: 'custom_dimension_5',
  PRODUCT_CATEGORY: 'custom_dimension_6',
  
  // Item-scoped custom dimensions
  ITEM_BRAND: 'custom_dimension_7',
  ITEM_VARIANT: 'custom_dimension_8',
} as const;

export function setCustomDimensions(dimensions: Record<string, any>): void {
  (window as any).gtag('set', 'custom_map', dimensions);
}

export function trackEventWithCustomDimensions(
  eventName: string,
  parameters: Record<string, any>,
  customDimensions?: Record<string, any>
): void {
  const allParameters = {
    ...parameters,
    ...customDimensions,
  };
  
  (window as any).gtag('event', eventName, allParameters);
}
```

### Usage Example

```typescript
// src/components/ProductCard.tsx
import { trackEventWithCustomDimensions, CustomDimensions } from '../analytics/custom-dimensions';

export function ProductCard({ product }: { product: Product }) {
  const handleView = () => {
    trackEventWithCustomDimensions(
      'product_viewed',
      {
        item_id: product.id,
        item_name: product.name,
        price: product.price,
      },
      {
        [CustomDimensions.PRODUCT_CATEGORY]: product.category,
        [CustomDimensions.ITEM_BRAND]: product.brand,
        [CustomDimensions.ITEM_VARIANT]: product.variant,
      }
    );
  };

  return <div onClick={handleView}>{product.name}</div>;
}
```

---

## E-commerce Tracking

### GA4 E-commerce Events

```typescript
// src/analytics/ecommerce.ts
export function trackViewItemList(
  items: EcommerceItem[],
  itemListName: string
): void {
  (window as any).gtag('event', 'view_item_list', {
    item_list_name: itemListName,
    items: items.map(item => ({
      item_id: item.id,
      item_name: item.name,
      item_category: item.category,
      price: item.price,
      quantity: item.quantity,
    })),
  });
}

export function trackSelectItem(item: EcommerceItem, itemListName: string): void {
  (window as any).gtag('event', 'select_item', {
    item_list_name: itemListName,
    items: [{
      item_id: item.id,
      item_name: item.name,
      item_category: item.category,
      price: item.price,
    }],
  });
}

export function trackViewItem(item: EcommerceItem): void {
  (window as any).gtag('event', 'view_item', {
    items: [{
      item_id: item.id,
      item_name: item.name,
      item_category: item.category,
      price: item.price,
    }],
    value: item.price,
    currency: 'USD',
  });
}

export function trackAddToCart(item: EcommerceItem): void {
  (window as any).gtag('event', 'add_to_cart', {
    items: [{
      item_id: item.id,
      item_name: item.name,
      item_category: item.category,
      price: item.price,
      quantity: item.quantity,
    }],
    value: item.price * item.quantity,
    currency: 'USD',
  });
}

export function trackRemoveFromCart(item: EcommerceItem): void {
  (window as any).gtag('event', 'remove_from_cart', {
    items: [{
      item_id: item.id,
      item_name: item.name,
      item_category: item.category,
      price: item.price,
      quantity: item.quantity,
    }],
    value: item.price * item.quantity,
    currency: 'USD',
  });
}

export function trackBeginCheckout(items: EcommerceItem[]): void {
  const totalValue = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  
  (window as any).gtag('event', 'begin_checkout', {
    items: items.map(item => ({
      item_id: item.id,
      item_name: item.name,
      item_category: item.category,
      price: item.price,
      quantity: item.quantity,
    })),
    value: totalValue,
    currency: 'USD',
  });
}

export function trackPurchase(order: Order): void {
  (window as any).gtag('event', 'purchase', {
    transaction_id: order.id,
    value: order.total,
    currency: 'USD',
    items: order.items.map(item => ({
      item_id: item.id,
      item_name: item.name,
      item_category: item.category,
      price: item.price,
      quantity: item.quantity,
    })),
  });
}

interface EcommerceItem {
  id: string;
  name: string;
  category: string;
  price: number;
  quantity: number;
  brand?: string;
  variant?: string;
}

interface Order {
  id: string;
  total: number;
  items: EcommerceItem[];
}
```

### Usage Example

```typescript
// src/components/ProductList.tsx
import { trackViewItemList, trackSelectItem } from '../analytics/ecommerce';

export function ProductList({ products }: { products: Product[] }) {
  useEffect(() => {
    const items = products.map(p => ({
      id: p.id,
      name: p.name,
      category: p.category,
      price: p.price,
      quantity: 1,
    }));
    
    trackViewItemList(items, 'product_list');
  }, [products]);

  const handleProductClick = (product: Product) => {
    trackSelectItem({
      id: product.id,
      name: product.name,
      category: product.category,
      price: product.price,
      quantity: 1,
    }, 'product_list');
  };

  return (
    <div>
      {products.map(product => (
        <div key={product.id} onClick={() => handleProductClick(product)}>
          {product.name} - ${product.price}
        </div>
      ))}
    </div>
  );
}
```

---

## Privacy Considerations

### Consent Management

```typescript
// src/analytics/consent.ts
export type ConsentCategory = 'analytics' | 'marketing' | 'personalization';

export interface ConsentState {
  analytics: boolean;
  marketing: boolean;
  personalization: boolean;
}

export function initConsent(): void {
  if (typeof window === 'undefined') {
    return;
  }

  // Load consent from localStorage
  const savedConsent = localStorage.getItem('analytics_consent');
  
  if (savedConsent) {
    const consent = JSON.parse(savedConsent) as ConsentState;
    applyConsent(consent);
  }
}

export function setConsent(consent: ConsentState): void {
  if (typeof window === 'undefined') {
    return;
  }

  // Save consent to localStorage
  localStorage.setItem('analytics_consent', JSON.stringify(consent));
  
  // Apply consent
  applyConsent(consent);
}

export function applyConsent(consent: ConsentState): void {
  if (typeof window === 'undefined') {
    return;
  }

  // Update GA4 consent
  (window as any).gtag('consent', 'update', {
    analytics_storage: consent.analytics ? 'granted' : 'denied',
    ad_storage: consent.marketing ? 'granted' : 'denied',
    ad_user_data: consent.marketing ? 'granted' : 'denied',
    ad_personalization: consent.personalization ? 'granted' : 'denied',
  });
}

export function hasConsent(category: ConsentCategory): boolean {
  if (typeof window === 'undefined') {
    return false;
  }

  const savedConsent = localStorage.getItem('analytics_consent');
  
  if (!savedConsent) {
    return false;
  }

  const consent = JSON.parse(savedConsent) as ConsentState;
  return consent[category];
}
```

### Data Anonymization

```typescript
// src/analytics/anonymization.ts
export function anonymizeEmail(email: string): string {
  const [username, domain] = email.split('@');
  const anonymizedUsername = username.substring(0, 2) + '***';
  return `${anonymizedUsername}@${domain}`;
}

export function anonymizePhone(phone: string): string {
  return phone.substring(0, 3) + '***' + phone.substring(phone.length - 2);
}

export function anonymizeName(name: string): string {
  const parts = name.split(' ');
  const anonymizedParts = parts.map(part => part.substring(0, 1) + '***');
  return anonymizedParts.join(' ');
}

export function anonymizeAddress(address: string): string {
  const parts = address.split(' ');
  return parts[0] + '*** ' + parts.slice(-2).join(' ');
}
```

### Usage Example

```typescript
// src/components/AnalyticsProvider.tsx
import { useEffect } from 'react';
import { initConsent, hasConsent } from '../analytics/consent';
import { trackEvent } from '../analytics/ga4';

export function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Initialize consent
    initConsent();
  }, []);

  const handleTrackEvent = (eventName: string, properties?: Record<string, any>) => {
    // Only track if consent is given
    if (hasConsent('analytics')) {
      trackEvent(eventName, properties);
    }
  };

  return (
    <AnalyticsContext.Provider value={{ trackEvent: handleTrackEvent }}>
      {children}
    </AnalyticsContext.Provider>
  );
}
```

---

## Server-Side Tracking

### GA4 Server-Side Tracking

```typescript
// src/analytics/ga4-server.ts
import { createTransport } from '@gtag/server';

const GA4_MEASUREMENT_ID = process.env.GA4_MEASUREMENT_ID || '';
const GA4_API_SECRET = process.env.GA4_API_SECRET || '';

export async function trackEventServer(
  eventName: string,
  parameters?: Record<string, any>,
  clientId?: string
): Promise<void> {
  if (!GA4_MEASUREMENT_ID || !GA4_API_SECRET) {
    return;
  }

  const transport = createTransport({
    measurementId: GA4_MEASUREMENT_ID,
    apiSecret: GA4_API_SECRET,
  });

  await transport.send({
    name: eventName,
    parameters: {
      ...parameters,
      engagement_time_msec: 100,
    },
    clientId,
  });
}

export async function trackPageViewServer(
  pagePath: string,
  pageTitle: string,
  clientId?: string
): Promise<void> {
  await trackEventServer('page_view', {
    page_path: pagePath,
    page_title: pageTitle,
  }, clientId);
}
```

### Mixpanel Server-Side Tracking

```typescript
// src/analytics/mixpanel-server.ts
import Mixpanel from 'mixpanel';

const MIXPANEL_TOKEN = process.env.MIXPANEL_TOKEN || '';

const mixpanel = Mixpanel.init(MIXPANEL_TOKEN, {
  geolocate: true,
});

export function trackEventServer(
  eventName: string,
  properties?: Record<string, any>,
  distinctId?: string
): void {
  mixpanel.track(eventName, {
    ...properties,
    distinct_id: distinctId,
    ip: '0.0.0.0', // Disable IP tracking
  });
}

export function identifyServer(
  distinctId: string,
  traits?: Record<string, any>
): void {
  mixpanel.people.set(distinctId, traits);
}

export function setUserPropertiesServer(
  distinctId: string,
  properties: Record<string, any>
): void {
  mixpanel.people.set(distinctId, properties);
}
```

---

## Data Validation

### Event Schema Validation

```typescript
// src/analytics/validation.ts
import { z } from 'zod';

export const EventSchema = z.object({
  eventName: z.string().min(1),
  properties: z.record(z.any()).optional(),
  userId: z.string().optional(),
  timestamp: z.date().optional(),
});

export const UserPropertiesSchema = z.object({
  userId: z.string().optional(),
  email: z.string().email().optional(),
  name: z.string().optional(),
  plan: z.enum(['free', 'basic', 'premium', 'enterprise']).optional(),
});

export function validateEvent(event: unknown): boolean {
  try {
    EventSchema.parse(event);
    return true;
  } catch {
    return false;
  }
}

export function validateUserProperties(properties: unknown): boolean {
  try {
    UserPropertiesSchema.parse(properties);
    return true;
  } catch {
    return false;
  }
}
```

### Usage Example

```typescript
// src/analytics/analytics.ts
export function trackEvent(
  eventName: string,
  properties?: Record<string, any>
): void {
  const event = {
    eventName,
    properties,
    timestamp: new Date(),
  };

  // Validate event before tracking
  if (!validateEvent(event)) {
    console.error('Invalid event:', event);
    return;
  }

  // Track event
  (window as any).gtag('event', eventName, properties);
}
```

---

## Testing Analytics

### Analytics Testing Utilities

```typescript
// test/analytics/analytics.test.ts
import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { trackEvent, setUserProperties } from '../../src/analytics/ga4';

describe('Analytics', () => {
  beforeEach(() => {
    // Setup mock
    (window as any).gtag = jest.fn();
  });

  afterEach(() => {
    // Cleanup
    delete (window as any).gtag;
  });

  it('should track event', () => {
    trackEvent('test_event', { test_param: 'test_value' });

    expect((window as any).gtag).toHaveBeenCalledWith('event', 'test_event', {
      test_param: 'test_value',
    });
  });

  it('should track page view', () => {
    trackEvent('page_view', {
      page_path: '/test',
      page_title: 'Test Page',
    });

    expect((window as any).gtag).toHaveBeenCalledWith('event', 'page_view', {
      page_path: '/test',
      page_title: 'Test Page',
    });
  });

  it('should set user properties', () => {
    setUserProperties({
      user_id: '123',
      plan: 'premium',
    });

    expect((window as any).gtag).toHaveBeenCalledWith('set', 'user_properties', {
      user_id: '123',
      plan: 'premium',
    });
  });
});
```

---

## Best Practices

### 1. Use Consistent Event Names

```typescript
// Good: Consistent event names
export const Events = {
  USER_SIGNED_UP: 'user_signed_up',
  USER_LOGGED_IN: 'user_logged_in',
  PRODUCT_VIEWED: 'product_viewed',
} as const;

// Bad: Inconsistent event names
export const Events = {
  signUp: 'sign_up',
  login: 'login',
  viewProduct: 'view_product',
} as const;
```

### 2. Validate Events

```typescript
// Good: Validate events
export function trackEvent(eventName: string, properties?: Record<string, any>): void {
  if (!validateEvent({ eventName, properties })) {
    console.error('Invalid event:', { eventName, properties });
    return;
  }

  (window as any).gtag('event', eventName, properties);
}

// Bad: No validation
export function trackEvent(eventName: string, properties?: Record<string, any>): void {
  (window as any).gtag('event', eventName, properties);
}
```

### 3. Respect User Consent

```typescript
// Good: Respect consent
export function trackEvent(eventName: string, properties?: Record<string, any>): void {
  if (!hasConsent('analytics')) {
    return;
  }

  (window as any).gtag('event', eventName, properties);
}

// Bad: Ignore consent
export function trackEvent(eventName: string, properties?: Record<string, any>): void {
  (window as any).gtag('event', eventName, properties);
}
```

### 4. Anonymize Sensitive Data

```typescript
// Good: Anonymize data
export function trackUserSignup(email: string, name: string): void {
  (window as any).gtag('event', 'user_signed_up', {
    email: anonymizeEmail(email),
    name: anonymizeName(name),
  });
}

// Bad: Send raw data
export function trackUserSignup(email: string, name: string): void {
  (window as any).gtag('event', 'user_signed_up', {
    email,
    name,
  });
}
```

### 5. Test Analytics

```typescript
// Good: Test analytics
describe('Analytics', () => {
  it('should track event', () => {
    trackEvent('test_event', { test_param: 'test_value' });

    expect((window as any).gtag).toHaveBeenCalledWith('event', 'test_event', {
      test_param: 'test_value',
    });
  });
});

// Bad: No tests
// No testing of analytics
```

---

## Summary

This skill covers comprehensive analytics and event tracking patterns including:

- **Analytics Platforms**: Google Analytics 4, Mixpanel, Segment setup and usage
- **Event Tracking**: Event naming conventions, tracking hooks, usage examples
- **User Properties**: User property tracking, usage examples
- **Custom Dimensions**: GA4 custom dimensions, usage examples
- **E-commerce Tracking**: GA4 e-commerce events, usage examples
- **Privacy Considerations**: Consent management, data anonymization
- **Server-Side Tracking**: GA4 and Mixpanel server-side tracking
- **Data Validation**: Event schema validation
- **Testing Analytics**: Analytics testing utilities
- **Best Practices**: Consistent names, validation, consent, anonymization, testing
