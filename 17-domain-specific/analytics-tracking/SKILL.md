# Analytics Tracking

A comprehensive guide to analytics and event tracking.

## Table of Contents

1. [Analytics Platforms](#analytics-platforms)
2. [Event Tracking](#event-tracking)
3. [User Properties](#user-properties)
4. [Custom Dimensions](#custom-dimensions)
5. [E-Commerce Tracking](#e-commerce-tracking)
6. [Privacy Considerations](#privacy-considerations)
7. [Server-Side Tracking](#server-side-tracking)
8. [Data Validation](#data-validation)
9. [Testing Analytics](#testing-analytics)
10. [Best Practices](#best-practices)

---

## Analytics Platforms

### Google Analytics 4 (GA4)

```typescript
// Install GA4
npm install gtag

// Initialize GA4
import { gtag, install } from 'ga-gtag';

install('G-XXXXXXXXXX', {
  send_page_view: true,
  debug_mode: process.env.NODE_ENV !== 'production',
});

// Track page view
gtag('event', 'page_view', {
  page_title: document.title,
  page_location: window.location.href,
});

// Track custom event
gtag('event', 'button_click', {
  event_category: 'engagement',
  event_label: 'signup_button',
});
```

```python
# Install GA4
pip install google-analytics-data-api

# Initialize GA4
from google.analytics.data_api import BetaAnalyticsDataApiV4

client = BetaAnalyticsDataApiV4()
client.initialize(
    property_id='GA_MEASUREMENT_ID',
    transport='http',
    debug_mode=False
)

# Track page view
client.events().create(
    event_name='page_view',
    params={
        'page_title': 'Home Page',
        'page_location': 'https://example.com/home'
    }
).execute()

# Track custom event
client.events().create(
    event_name='button_click',
    params={
        'event_category': 'engagement',
        'event_label': 'signup_button'
    }
).execute()
```

### Mixpanel

```typescript
// Install Mixpanel
npm install mixpanel-browser

// Initialize Mixpanel
import mixpanel from 'mixpanel-browser';

mixpanel.init('YOUR_PROJECT_TOKEN', {
  debug: process.env.NODE_ENV !== 'production',
});

// Track page view
mixpanel.track('Page View', {
  page: window.location.pathname,
});

// Track custom event
mixpanel.track('Button Click', {
  button_name: 'Sign Up',
  location: 'Homepage',
});
```

```python
# Install Mixpanel
pip install mixpanel

# Initialize Mixpanel
import mixpanel

mixpanel.init(
    token='YOUR_PROJECT_TOKEN',
    debug=False
)

# Track page view
mixpanel.track('Page View', {
    'page': '/home'
})

# Track custom event
mixpanel.track('Button Click', {
    'button_name': 'Sign Up',
    'location': 'Homepage'
})
```

### Segment

```typescript
// Install Segment
npm install @segment/analytics-node

// Initialize Segment
import Analytics from '@segment/analytics-node';

const analytics = new Analytics('YOUR_WRITE_KEY', {
  flushAt: 20,
});

// Track page view
analytics.track('Page View', {
  path: window.location.pathname,
});

// Track custom event
analytics.track('Button Click', {
  button_name: 'Sign Up',
  location: 'Homepage',
});
```

```python
# Install Segment
pip install segment-analytics-python

# Initialize Segment
from segment import Analytics

analytics = Analytics('YOUR_WRITE_KEY')

# Track page view
analytics.track(
    'Page View',
    {'path': '/home'}
)

# Track custom event
analytics.track(
    'Button Click',
    {
        'button_name': 'Sign Up',
        'location': 'Homepage'
    }
)
```

---

## Event Tracking

### Page View Tracking

```typescript
// Track page views
import { gtag } from 'ga-gtag';

export function trackPageView(title: string, location: string) {
  gtag('event', 'page_view', {
    page_title: title,
    page_location: location,
  });
}

// Usage
trackPageView('Home Page', 'https://example.com/home');
```

```python
# Track page views
from google.analytics.data_api import BetaAnalyticsDataApiV4

client = BetaAnalyticsDataApiV4()
client.initialize(property_id='GA_MEASUREMENT_ID')

def track_page_view(title: str, location: str):
    client.events().create(
        event_name='page_view',
        params={
            'page_title': title,
            'page_location': location
        }
    ).execute()
```

### Custom Event Tracking

```typescript
// Track custom events
import { gtag } from 'ga-gtag';

export function trackEvent(category: string, action: string, label?: string, value?: any) {
  gtag('event', action, {
    event_category: category,
    event_label: label,
    value,
  });
}

// Usage
trackEvent('engagement', 'click', 'signup_button');
trackEvent('ecommerce', 'purchase', 'product_123', 99.99);
```

```python
# Track custom events
from google.analytics.data_api import BetaAnalyticsDataApiV4

client = BetaAnalyticsDataApiV4()
client.initialize(property_id='GA_MEASUREMENT_ID')

def track_event(category: str, action: str, label: str = None, value: any = None):
    client.events().create(
        event_name=action,
        params={
            'event_category': category,
            'event_label': label,
            'value': value
        }
    ).execute()

# Usage
track_event('engagement', 'click', 'signup_button')
track_event('ecommerce', 'purchase', value=99.99)
```

### Form Submission Tracking

```typescript
// Track form submissions
import { gtag } from 'ga-gtag';

export function trackFormSubmission(formName: string, formData: Record<string, any>) {
  gtag('event', 'form_submit', {
    event_category: 'forms',
    event_label: formName,
    form_name: formName,
    ...formData,
  });
}

// Usage
trackFormSubmission('Contact', {
  name: 'John Doe',
  email: 'john@example.com',
  message: 'Hello',
});
```

---

## User Properties

### Setting User Properties

```typescript
// Set user properties
import { gtag } from 'ga-gtag';

export function setUserProperties(userId: string, properties: Record<string, any>) {
  gtag('set', 'user_properties', properties);
}

// Usage
setUserProperties('user_123', {
  user_id: 'user_123',
  plan: 'premium',
  signup_date: '2024-01-01',
});
```

```python
# Set user properties
from google.analytics.data_api import BetaAnalyticsDataApiV4

client = BetaAnalyticsDataApiV4()
client.initialize(property_id='GA_MEASUREMENT_ID')

def set_user_properties(user_id: str, properties: dict):
    client.events().create(
        event_name='set_user_properties',
        params={
            'user_id': user_id,
            **properties
        }
    ).execute()

# Usage
set_user_properties('user_123', {
    'plan': 'premium',
    'signup_date': '2024-01-01'
})
```

### Updating User Properties

```typescript
// Update user properties
import { gtag } from 'ga-gtag';

export function updateUserProperties(userId: string, properties: Record<string, any>) {
  gtag('set', 'user_properties', properties);
}

// Usage
updateUserProperties('user_123', {
  plan: 'enterprise',
  upgraded_at: new Date().toISOString(),
});
```

---

## Custom Dimensions

### Defining Custom Dimensions

```typescript
// Define custom dimensions
import { gtag } from 'gtag';

// Configure custom dimensions
gtag('config', {
  custom_map: {
    dimension1: 'user_tier',
    dimension2: 'content_type',
    dimension3: 'page_section',
  },
});
```

### Using Custom Dimensions

```typescript
// Use custom dimensions in events
import { gtag } from 'ga-gtag';

export function trackPageView(title: string, section: string, tier: string) {
  gtag('event', 'page_view', {
    page_title: title,
    page_section: section,
    user_tier: tier,
  });
}

// Usage
trackPageView('Product Page', 'products', 'premium');
```

---

## E-Commerce Tracking

### Product View Tracking

```typescript
// Track product views
import { gtag } from 'ga-gtag';

export function trackProductView(productId: string, productName: string, price: number, category: string) {
  gtag('event', 'view_item', {
    event_category: 'ecommerce',
    event_label: productId,
    items: [
      {
        item_id: productId,
        item_name: productName,
        price: price,
        item_category: category,
      },
    ],
  });
}

// Usage
trackProductView('prod_123', 'Premium Widget', 99.99, 'widgets');
```

### Purchase Tracking

```typescript
// Track purchases
import { gtag } from 'gtag';

export function trackPurchase(orderId: string, items: Array<any>, total: number) {
  gtag('event', 'purchase', {
    transaction_id: orderId,
    value: total,
    items: items,
  });
}

// Usage
trackPurchase('order_456', [
  {
    item_id: 'prod_123',
    item_name: 'Premium Widget',
    price: 99.99,
    quantity: 2,
  },
], 199.98);
```

### Checkout Tracking

```typescript
// Track checkout steps
import { gtag } from 'ga-gtag';

export function trackCheckoutStep(step: string, stepNumber: number) {
  gtag('event', 'begin_checkout', {
    event_category: 'ecommerce',
    event_label: step,
    checkout_step: stepNumber,
  });
}

// Usage
trackCheckoutStep('shipping_info', 1);
trackCheckoutStep('payment_info', 2);
trackCheckoutStep('review', 3);
trackCheckoutStep('complete', 4);
```

---

## Privacy Considerations

### Anonymizing IP Addresses

```typescript
// Anonymize IP addresses
export function anonymizeIP(ip: string): string {
  const parts = ip.split('.');
  return `${parts[0]}.${parts[1]}.${parts[2]}.xxx`;
}

// Usage
const anonymizedIP = anonymizeIP('192.168.1.100');
// Returns: 192.168.1.xxx
```

### Hashing User Data

```typescript
// Hash user identifiers
import { createHash } from 'crypto';

export function hashUserId(userId: string): string {
  return createHash('sha256').update(userId).digest('hex');
}

// Usage
const hashedUserId = hashUserId('user_123');
```

### Removing PII

```typescript
// Remove PII from events
export function sanitizeEvent(event: any): any {
  const sanitized = { ...event };

  // Remove PII fields
  delete sanitized.email;
  delete sanitized.phone;
  delete sanitized.ssn;
  delete sanitized.creditCard;

  return sanitized;
}

// Usage
const event = {
  user_id: 'user_123',
  email: 'john@example.com', // Will be removed
  phone: '555-1234', // Will be removed
  action: 'purchase',
};

const sanitized = sanitizeEvent(event);
```

### Consent Management

```typescript
// Check user consent
export function hasConsent(consentType: string): boolean {
  const consent = localStorage.getItem(`consent_${consentType}`);
  return consent === 'true';
}

export function setConsent(consentType: string, granted: boolean): void {
  localStorage.setItem(`consent_${consentType}`, granted.toString());
}

// Usage
if (hasConsent('analytics')) {
  // Track analytics
}
```

---

## Server-Side Tracking

### Node.js Server-Side Tracking

```typescript
// Install GA4
npm install @google-analytics/data

// Initialize GA4
import { MeasurementProtocol } from '@google-analytics/data';

const measurement = new MeasurementProtocol('GA_MEASUREMENT_ID', {
  debug: process.env.NODE_ENV !== 'production',
});

// Track event from server
export function trackServerEvent(eventName: string, parameters: Record<string, any>) {
  measurement.event(eventName, parameters);
}

// Usage
trackServerEvent('api_request', {
  endpoint: '/api/users',
  method: 'GET',
  status_code: 200,
  response_time_ms: 150,
});
```

### Python Server-Side Tracking

```python
# Install GA4
pip install google-analytics-data-api

from google.analytics.data_api import BetaAnalyticsDataApiV4

client = BetaAnalyticsDataApiV4()
client.initialize(property_id='GA_MEASUREMENT_ID')

# Track event from server
def track_server_event(event_name: str, parameters: dict):
    client.events().create(
        event_name=event_name,
        params=parameters
    ).execute()

# Usage
track_server_event('api_request', {
    'endpoint': '/api/users',
    'method': 'GET',
    'status_code': 200,
    "response_time_ms": 150
})
```

---

## Data Validation

### Event Schema Validation

```typescript
// Validate event data
interface AnalyticsEvent {
  event_name: string;
  event_category?: string;
  event_label?: string;
  value?: number;
  [key: string]: any;
}

export function validateEvent(event: any): AnalyticsEvent | null {
  if (!event || typeof event !== 'object') {
    return null;
  }

  if (!event.event_name || typeof event.event_name !== 'string') {
    return null;
  }

  return event as AnalyticsEvent;
}

// Usage
const event = validateEvent({
  event_name: 'button_click',
  event_category: 'engagement',
  event_label: 'signup_button',
});

if (event) {
  // Track event
}
```

### Required Fields Validation

```typescript
// Validate required fields
export function validateRequiredFields(event: any, requiredFields: string[]): boolean {
  for (const field of requiredFields) {
    if (!event[field]) {
      console.warn(`Missing required field: ${field}`);
      return false;
    }
  }
  return true;
}

// Usage
const event = {
  event_name: 'purchase',
  transaction_id: 'order_123',
  value: 99.99,
};

if (validateRequiredFields(event, ['event_name', 'transaction_id', 'value'])) {
  // Track event
}
```

---

## Testing Analytics

### Debug Mode

```typescript
// Enable debug mode for development
import { gtag } from 'ga-gtag';

const isDevelopment = process.env.NODE_ENV !== 'production';

gtag('config', {
  debug_mode: isDevelopment,
  send_page_view: !isDevelopment, // Don't send page views in dev
});

// Log events in development
export function trackEvent(category: string, action: string, label?: string) {
  const eventData = {
    event_category: category,
    event_label: label,
  };

  if (isDevelopment) {
    console.log('Analytics Event:', eventData);
  } else {
    gtag('event', action, eventData);
  }
}
```

### Test Events

```typescript
// Test analytics tracking
export function testAnalytics() {
  console.log('Testing analytics...');

  // Test page view
  gtag('event', 'page_view', {
    page_title: 'Test Page',
  });

  // Test custom event
  gtag('event', 'test_event', {
    event_category: 'test',
    event_label: 'test_label',
  });

  console.log('Analytics test complete');
}
```

---

## Best Practices

### 1. Use Consistent Event Names

```typescript
// Use consistent naming convention
export const EVENT_NAMES = {
  PAGE_VIEW: 'page_view',
  BUTTON_CLICK: 'button_click',
  FORM_SUBMIT: 'form_submit',
  PURCHASE: 'purchase',
  SEARCH: 'search',
};

// Usage
gtag('event', EVENT_NAMES.BUTTON_CLICK, {
  event_category: 'engagement',
  event_label: 'signup_button',
});
```

### 2. Set User Context

```typescript
// Set user context early
export function setUserContext(userId: string, properties: Record<string, any>) {
  gtag('set', 'user_id', userId);
  gtag('set', 'user_properties', properties);
}

// Usage
setUserContext('user_123', {
  plan: 'premium',
  signup_date: '2024-01-01',
});
```

### 3. Track Key Metrics

```typescript
// Track key business metrics
export function trackKeyMetrics() {
  gtag('event', 'page_view', {
    page_title: document.title,
    page_location: window.location.href,
  });
}

export function trackConversion() {
  gtag('event', 'conversion', {
    value: 1,
  });
}
```

### 4. Use Custom Dimensions

```typescript
// Use custom dimensions for better analysis
export function trackWithDimensions(event: string, dimensions: Record<string, string>) {
  gtag('event', event, dimensions);
}

// Usage
trackWithDimensions('page_view', {
  user_tier: 'premium',
  content_type: 'article',
  page_section: 'blog',
});
```

### 5. Validate Data Before Sending

```typescript
// Validate event data
export function trackValidatedEvent(event: any) {
  const validated = validateEvent(event);

  if (validated) {
    gtag('event', validated.event_name, validated);
  }
}
```

### 6. Handle Errors Gracefully

```typescript
// Handle tracking errors
export function safeTrack(event: string, parameters?: Record<string, any>) {
  try {
    gtag('event', event, parameters);
  } catch (error) {
    console.error('Analytics error:', error);
  }
}

// Usage
safeTrack('button_click', {
  button_name: 'signup_button',
});
```

### 7. Use Server-Side Tracking for Sensitive Data

```typescript
// Track sensitive data server-side
export function trackServerEvent(eventName: string, parameters: Record<string, any>) {
  fetch('/api/analytics', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      event_name: eventName,
      parameters,
      timestamp: new Date().toISOString(),
    }),
  }).catch(error => {
    console.error('Analytics error:', error);
  });
}
```

### 8. Respect User Consent

```typescript
// Check consent before tracking
export function trackWithConsent(event: string, parameters?: Record<string, any>) {
  if (hasConsent('analytics')) {
    gtag('event', event, parameters);
  } else {
    console.log('Analytics consent not granted');
  }
}
```

### 9. Use Event Batching

```typescript
// Batch events for performance
const eventQueue: any[] = [];

export function queueEvent(event: any) {
  eventQueue.push(event);

  if (eventQueue.length >= 10) {
    flushEvents();
  }
}

function flushEvents() {
  if (eventQueue.length === 0) return;

  eventQueue.forEach(event => {
    gtag('event', event.event_name, event);
  });

  eventQueue.length = 0;
}
```

### 10. Document Your Events

```typescript
// Document analytics events
/**
 * Analytics Events
 *
 * PAGE_VIEW: Tracked when a user views a page
 * BUTTON_CLICK: Tracked when a user clicks a button
 * FORM_SUBMIT: Tracked when a user submits a form
 * PURCHASE: Tracked when a user makes a purchase
 *
 * Event Naming Convention: category_action
 */
export const EVENTS = {
  PAGE_VIEW: 'page_view',
  BUTTON_CLICK: 'button_click',
  FORM_SUBMIT: 'form_submit',
  PURCHASE: 'purchase',
};
```

---

## Resources

- [Google Analytics 4 Documentation](https://developers.google.com/analytics/devguides/collection/gtagjs/)
- [Mixpanel Documentation](https://mixpanel.com/help/reference/)
- [Segment Documentation](https://segment.com/docs/connections/sources/)
- [Analytics Best Practices](https://www.optimizesmartly.com/blog/google-analytics/)
