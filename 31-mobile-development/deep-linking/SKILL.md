---
name: Deep Linking and Universal Links
description: Enabling apps to open specific content when users click links from websites, emails, or other apps using URL schemes, Universal Links (iOS), and App Links (Android).
---

# Deep Linking and Universal Links

> **Current Level:** Intermediate  
> **Domain:** Mobile Development / UX

---

## Overview

Deep linking enables apps to open specific content when users click links from websites, emails, or other apps. This guide covers URL schemes, Universal Links, App Links, and deep linking best practices for creating seamless user experiences across web and mobile.

---

---

## Core Concepts

### Table of Contents

1. [Deep Linking Concepts](#deep-linking-concepts)
2. [URL Schemes](#url-schemes)
3. [Universal Links (iOS)]((#universal-links-ios)
4. [App Links (Android)]((#app-links-android))
5. [Setup and Configuration]((#setup-and-configuration)
6. [Handling Deep Links]((#handling-deep-links))
7. [Deferred Deep Linking]((#deferred-deep-linking))
8. [Branch.io Integration]((#branchio-integration)
9. [Testing Deep Links]((#testing-deep-links))
10. [Analytics]((#analytics))
11. [Common Patterns]((#common-patterns))
12. [Best Practices]((#best-practices))

---

## Deep Linking Concepts

### Deep Link Types

```typescript
enum DeepLinkType {
  URL_SCHEME = 'url_scheme',     // Custom URL scheme (myapp://)
  UNIVERSAL_LINK = 'universal_link', // Universal Links (https://myapp.com)
  APP_LINK = 'app_link',         // App Links (https://myapp.com)
  BRANCH_IO = 'branch_io',         // Branch.io
}

enum DeepLinkRoute {
  HOME = 'home',
  PRODUCT = 'product',
  PROFILE = 'profile',
  ORDER = 'order',
  CHECKOUT = 'checkout',
}
```

---

## URL Schemes

### Custom URL Scheme

```typescript
// Android: android/app/src/main/AndroidManifest.xml
<manifest>
  <application>
    <activity
      android:name=".MainActivity"
      android:launchMode="singleTask"
      android:exported="true">
      <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data android:scheme="myapp" />
      </intent-filter>
    </activity>
  </application>
</manifest>

// iOS: ios/Runner/Info.plist
<key>CFBundleURLTypes</key>
<array>
  <string>myapp</string>
</array>
```

### React Native URL Scheme Handler

```typescript
// Linking API
import { Linking, EventSubscription } from 'react-native';

class DeepLinkHandler {
  private urlListener: EventSubscription | null = null;

  /**
   * Initialize deep link handler
   */
  initialize(callback: (url: URL) => void): void {
    // Handle initial URL if app was opened from a link
    Linking.getInitialURL().then(url => {
      if (url) {
        callback(new URL(url));
      }
    });

    // Listen for incoming links
    this.urlListener = Linking.addEventListener('url', ({ url }) => {
      callback(new URL(url));
    });
  }

  /**
   * Cleanup
   */
  cleanup(): void {
    if (this.urlListener) {
      this.urlListener.remove();
      this.urlListener = null;
    }
  }

  /**
   * Parse deep link
   */
  parseDeepLink(url: URL): {
    route: DeepLinkRoute;
    params: Record<string, string>;
  } {
    const hostname = url.hostname;
    const pathname = url.pathname;
    const searchParams = Object.fromEntries(url.searchParams.entries());

    // Parse route
    let route: DeepLinkRoute;

    switch (pathname) {
      case '/product':
        route = DeepLinkRoute.PRODUCT;
        break;
      case '/profile':
        route = DeepLinkRoute.PROFILE;
        break;
      case '/order':
        route = DeepLinkRoute.ORDER;
        break;
      case '/checkout':
        route = DeepLinkRoute.CHECKOUT;
        break;
      default:
        route = DeepLinkRoute.HOME;
    }

    return {
      route,
      params: searchParams,
    };
  }
}

// Usage
function App() {
  const navigation = useNavigation();

  const handleDeepLink = (url: URL) => {
    const { route, params } = deepLinkHandler.parseDeepLink(url);

    switch (route) {
      case DeepLinkRoute.PRODUCT:
        navigation.navigate('ProductDetails', { productId: params.id });
        break;
      case DeepLinkRoute.PROFILE:
        navigation.navigate('Profile', { userId: params.userId });
        break;
      case DeepLinkRoute.ORDER:
        navigation.navigate('OrderDetails', { orderId: params.orderId });
        break;
      case DeepLinkRoute.CHECKOUT:
        navigation.navigate('Checkout');
        break;
      default:
        navigation.navigate('Home');
    }
  };

  useEffect(() => {
    deepLinkHandler.initialize(handleDeepLink);

    return () => {
      deepLinkHandler.cleanup();
    };
  }, []);

  return <YourApp />;
}
```

---

## Universal Links (iOS)

### Apple App Site Association

```xml
<!-- apple-app-site-association -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>applinks</key>
    <array>
      <dict>
        <key>appIDs</key>
        <array>
          <string>TEAMID.com.example.myapp</string>
        </array>
        <key>components</key>
        <array>
          <dict>
            <key>/</key>
            <dict>
              <key>AppID</key>
              <string>TEAMID.com.example.myapp</string>
            </dict>
          </dict>
          <dict>
            <key>/product</key>
            <dict>
              <key>AppID</key>
              <string>TEAMID.com.example.myapp</string>
            </dict>
          </dict>
          <dict>
            <key>/profile</key>
            <dict>
              <key>AppID</key>
              <string>TEAMID.com.example.myapp</string>
            </dict>
          </dict>
        </array>
      </dict>
    </array>
  </dict>
</plist>
```

### React Native Universal Link Handler

```typescript
// npm install @react-native-community/linking
import { Linking } from '@react-native-community/linking';

class UniversalLinkHandler {
  /**
   * Handle universal link
   */
  async handleUniversalLink(url: string): Promise<{
    route: DeepLinkRoute;
    params: Record<string, string>;
  }> {
    const parsedUrl = new URL(url);
    const pathname = parsedUrl.pathname;

    // Parse route
    let route: DeepLinkRoute;

    switch (pathname) {
      case '/product':
        route = DeepLinkRoute.PRODUCT;
        break;
      case '/profile':
        route = DeepLinkRoute.PROFILE;
        break;
      case '/order':
        route = DeepLinkRoute.ORDER;
        break;
      case '/checkout':
        route = DeepLinkRoute.CHECKOUT;
        break;
      default:
        route = DeepLinkRoute.HOME;
    }

    return {
      route,
      params: Object.fromEntries(parsedUrl.searchParams.entries()),
    };
  }

  /**
   * Check if URL is universal link
   */
  isUniversalLink(url: string): boolean {
    try {
      const parsed = new URL(url);
      const hostname = parsed.hostname;

      // Check if hostname matches app domain
      return hostname === 'myapp.com' || hostname === 'www.myapp.com';
    } catch {
      return false;
    }
  }
}
```

---

## App Links (Android)

### Android App Links

```xml
<!-- assetlinks.json -->
[{
  "applinks": [
    {
      "package_name": "com.example.myapp",
      "sha256_cert_fingerprints": [
        "14:6D:EA:7F:9C:4F:2B:1B:2D:4E:6F:8:0:2:A:4:C:6:E:8:0:2:A:4:C:6",
        "1A:2B:3C:4D:5E:6F:7A:8B:9C:0D:1E:2F:3A:4B:5C:6D:7E:8F"
      ],
      "package_name": "com.example.myapp",
      "domains": [
        "myapp.com",
        "www.myapp.com"
      ]
    }
  ]
}
```

### React Native App Link Handler

```typescript
import { Linking } from 'react-native';

class AppLinkHandler {
  /**
   * Handle app link
   */
  async handleAppLink(url: string): Promise<{
    route: DeepLinkRoute;
    params: Record<string, string>;
  }> {
    const parsedUrl = new URL(url);
    const pathname = parsedUrl.pathname;

    // Parse route
    let route: DeepLinkRoute;

    switch (pathname) {
      case '/product':
        route = DeepLinkRoute.PRODUCT;
        break;
      case '/profile':
        route = DeepLinkRoute.PROFILE;
        break;
      case '/order':
        route = DeepLinkRoute.ORDER;
        break;
      case '/checkout':
        route = DeepLinkRoute.CHECKOUT;
        break;
      default:
        route = DeepLinkRoute.HOME;
    }

    return {
      route,
      params: Object.fromEntries(parsedUrl.searchParams.entries()),
    };
  }

  /**
   * Check if URL is app link
   */
  isAppLink(url: string): boolean {
    try {
      const parsed = new URL(url);
      const hostname = parsed.hostname;

      // Check if hostname matches app domain
      return hostname === 'myapp.com' || hostname === 'www.myapp.com';
    } catch {
      return false;
    }
  }
}
```

---

## Setup and Configuration

### Unified Deep Link Handler

```typescript
import { Platform } from 'react-native';

class DeepLinkService {
  private urlSchemeHandler: DeepLinkHandler;
  private universalLinkHandler: UniversalLinkHandler;
  private appLinkHandler: AppLinkHandler;

  constructor() {
    this.urlSchemeHandler = new DeepLinkHandler();
    this.universalLinkHandler = new UniversalLinkHandler();
    this.appLinkHandler = new AppLinkHandler();
  }

  /**
   * Initialize
   */
  async initialize(callback: (result: {
    route: DeepLinkRoute;
    params: Record<string, string>;
  }) => void): Promise<void> {
    // Get initial URL
    const initialUrl = await Linking.getInitialURL();

    if (!initialUrl) {
      return;
    }

    // Handle based on URL type
    let result: {
      route: DeepLinkRoute;
      params: Record<string, string>;
    };

    if (this.isURLScheme(initialUrl)) {
      result = this.urlSchemeHandler.parseDeepLink(new URL(initialUrl));
    } else if (Platform.OS === 'ios' && this.universalLinkHandler.isUniversalLink(initialUrl)) {
      result = await this.universalLinkHandler.handleUniversalLink(initialUrl);
    } else if (Platform.OS === 'android' && this.appLinkHandler.isAppLink(initialUrl)) {
      result = await this.appLinkHandler.handleAppLink(initialUrl);
    }

    if (result) {
      callback(result);
    }
  }

  /**
   * Set up listener
   */
  setupListener(callback: (result: {
    route: DeepLinkRoute;
    params: Record<string, string>;
  }) => void): void {
    Linking.addEventListener('url', async ({ url }) => {
      if (this.isURLScheme(url)) {
        const result = this.urlSchemeHandler.parseDeepLink(new URL(url));
        callback(result);
      } else if (Platform.OS === 'ios' && this.universalLinkHandler.isUniversalLink(url)) {
        const result = await this.universalLinkHandler.handleUniversalLink(url);
        callback(result);
      } else if (Platform.OS === 'android' && this.appLinkHandler.isAppLink(url)) {
        const result = await this.appLinkHandler.handleAppLink(url);
        callback(result);
      }
    });
  }

  /**
   * Check if URL scheme
   */
  private isURLScheme(url: string): boolean {
    try {
      return url.startsWith('myapp://');
    } catch {
      return false;
    }
  }
}

// Usage
function App() {
  const navigation = useNavigation();
  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    const deepLinkService = new DeepLinkService();

    const handleDeepLink = (result: {
      route: DeepLinkRoute;
      params: Record<string, string>;
    }) => {
      switch (result.route) {
        case DeepLinkRoute.PRODUCT:
          navigation.navigate('ProductDetails', { productId: result.params.id });
          break;
        case DeepLinkRoute.PROFILE:
          navigation.navigate('Profile', { userId: result.params.userId });
          break;
        case DeepLinkRoute.ORDER:
          navigation.navigate('OrderDetails', { orderId: result.params.orderId });
          break;
        case DeepLinkRoute.CHECKOUT:
          navigation.navigate('Checkout');
          break;
        default:
          navigation.navigate('Home');
      }
    };

    // Initialize and set up listener
    deepLinkService.initialize(handleDeepLink);
    deepLinkService.setupListener(handleDeepLink);

    setIsInitialized(true);

    return () => {
      // Cleanup
      // Linking listeners are automatically cleaned up
    };
  }, []);

  return <YourApp />;
}
```

---

## Handling Deep Links

### Navigation Integration

```typescript
// src/navigation/DeepLinkNavigator.tsx
import { useEffect } from 'react';
import { useNavigation } from '@react-navigation/native';

export function DeepLinkHandler({ deepLink }: {
  deepLink: {
    route: DeepLinkRoute;
    params: Record<string, string>;
  };
}) {
  const navigation = useNavigation();

  useEffect(() => {
    if (!deepLink) return;

    switch (deepLink.route) {
      case DeepLinkRoute.PRODUCT:
        navigation.navigate('ProductDetails' as never, {
          productId: deepLink.params.id,
        });
        break;
      case DeepLinkRoute.PROFILE:
        navigation.navigate('Profile' as never, {
          userId: deepLink.params.userId,
        });
        break;
      case DeepLinkRoute.ORDER:
        navigation.navigate('OrderDetails' as never, {
          orderId: deepLink.params.orderId,
        });
        break;
      case DeepLinkRoute.CHECKOUT:
        navigation.navigate('Checkout' as never);
        break;
      default:
        navigation.navigate('Home' as never);
    }
  }, [deepLink, navigation]);
  return null;
}

// Usage in App.tsx
function App() {
  const [deepLink, setDeepLink] = useState<{
    route: DeepLinkRoute;
    params: Record<string, string>;
  } | null>(null);

  useEffect(() => {
    const deepLinkService = new DeepLinkService();

    const handleDeepLink = (result: {
      route: DeepLinkRoute;
      params: Record<string, string>;
    }) => {
      setDeepLink(result);
    };

    deepLinkService.initialize(handleDeepLink);
    deepLinkService.setupListener(handleDeepLink);
  }, []);

  return (
    <>
      <DeepLinkHandler deepLink={deepLink} />
      <YourApp />
    </>
  );
}
```

---

## Deferred Deep Linking

### Branch.io Integration

```typescript
import { AppState, AppStateStatus } from 'react-native';
import branch, { subscribe } from 'react-native-branch';

class DeferredDeepLinkHandler {
  private appState: AppStateStatus = 'active';

  /**
   * Initialize
   */
  initialize(): void {
    this.appState = AppState.currentState;

    AppState.addEventListener('change', this.handleAppStateChange);

    // Handle initial deep link
    branch.subscribe(async ({ params, error }) => {
      if (error) {
        console.error('Branch error:', error);
        return;
      }

      if (params['+non_branch_link']) {
        // Handle deep link
        this.handleDeepLink(params['+non_branch_link']);
      }
    });
  }

  /**
   * Handle app state change
   */
  private handleAppStateChange = (nextAppState: AppStateStatus) => {
    if (this.appState.match(/inactive/) && nextAppState === 'active') {
      // App came to foreground
      branch.subscribe(async ({ params }) => {
        if (params['+clicked_branch_link']) {
          // Handle deferred deep link
          this.handleDeepLink(params['+clicked_branch_link']);
        }
      });
    }

    this.appState = nextAppState;
  };

  /**
   * Handle deep link
   */
  private handleDeepLink(link: string): void {
    const url = new URL(link);
    const pathname = url.pathname;
    const searchParams = Object.fromEntries(url.searchParams.entries());

    // Parse route
    let route: DeepLinkRoute;

    switch (pathname) {
      case '/product':
        route = DeepLinkRoute.PRODUCT;
        break;
      case '/profile':
        route = DeepLinkRoute.PROFILE;
        break;
      case '/order':
        route = DeepLinkRoute.ORDER;
        break;
      case '/checkout':
        route = DeepLinkRoute.CHECKOUT;
        break;
      default:
        route = DeepLinkRoute.HOME;
    }

    // Emit event for navigation
    this.emitDeepLinkEvent(route, searchParams);
  }

  /**
   * Emit deep link event
   */
  private emitDeepLinkEvent(
    route: DeepLinkRoute,
    params: Record<string, string>
  ): void {
    // Emit event for navigation
    const event = new CustomEvent('deepLink', { route, params });
    eventEmitter.emit(event);
  }
}
```

---

## Branch.io Integration

### Branch SDK Setup

```typescript
// npm install react-native-branch
import branch, { createBranchUniversalObject } from 'react-native-branch';

class BranchService {
  /**
   * Initialize
   */
  async initialize(): Promise<void> {
    await branch.initSession();

    // Set user identity
    const userId = await this.getUserId();
    if (userId) {
      branch.setIdentity(userId);
    }
  }

  /**
   * Create deep link
   */
  async createDeepLink(params: {
    route: string;
    params: Record<string, string>;
    feature?: string;
    campaign?: string;
    channel?: string;
  }): Promise<string> {
    const linkData = {
      ...params.params,
      feature: params.feature || 'default',
      campaign: params.campaign || 'default',
      channel: params.channel || 'default',
      $desktop_url: `https://myapp.com/${params.route}?${new URLSearchParams(params.params).toString()}`,
      $android_url: `myapp://${params.route}?${new URLSearchParams(params.params).toString()}`,
      $ios_url: `https://myapp.com/${params.route}?${new URLSearchParams(params.params).toString()}`,
      $fallback_url: `https://myapp.com`,
    };

    const { url } = await branch.createBranchUniversalObject(linkData);

    return url;
  }

  /**
   * Track event
   */
  async trackEvent(eventName: string, attributes?: Record<string, string>): Promise<void> {
    await branch.logEvent(eventName, attributes);
  }

  /**
   * Track commerce event
   */
  async trackCommerceEvent(params: {
    revenue: number;
    currency: string;
    transactionId: string;
    affiliation?: string;
  }): Promise<void> {
    await branch.logCommerceEvent(
      'purchase',
      revenue,
      params.currency,
      {
        transaction_id: params.transactionId,
        affiliation: params.affiliation,
      }
    );
  }

  /**
   * Get user ID
   */
  private async getUserId(): Promise<string | null> {
    const userId = await AsyncStorage.getItem('userId');
    return userId;
  }
}
```

---

## Testing Deep Links

### Deep Link Tester

```typescript
class DeepLinkTester {
  /**
   * Test deep link
   */
  testDeepLink(link: string): void {
    console.log('Testing deep link:', link);

    // Parse link
    const url = new URL(link);
    const pathname = url.pathname;
    const searchParams = Object.fromEntries(url.searchParams.entries());

    console.log('Route:', pathname);
    console.log('Params:', searchParams);
  }

  /**
   * Generate test links
   */
  generateTestLinks(): {
    productLinks: string[];
    profileLinks: string[];
    orderLinks: string[];
    checkoutLinks: string[];

    for (let i = 1; i <= 3; i++) {
      // Product links
      productLinks.push(`https://myapp.com/product?id=prod_${i}`);
      productLinks.push(`myapp://product?id=prod_${i}`);

      // Profile links
      profileLinks.push(`https://myapp.com/profile?userId=user_${i}`);
      profileLinks.push(`myapp://profile?userId=user_${i}`);

      // Order links
      orderLinks.push(`https://myapp.com/order?orderId=order_${i}`);
      orderLinks.push(`myapp://order?orderId=order_${i}`);

      // Checkout links
      checkoutLinks.push(`https://myapp.com/checkout`);
      checkoutLinks.push(`myapp://checkout`);
    }

    return {
      productLinks,
      profileLinks,
      orderLinks,
      checkoutLinks,
    };
  }

  /**
   * Test all links
   */
  async testAllLinks(): Promise<void> {
    const links = this.generateTestLinks();

    for (const link of [...links.productLinks, ...links.profileLinks, ...links.orderLinks, ...links.checkoutLinks]) {
      this.testDeepLink(link);
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
}
```

---

## Analytics

### Deep Link Analytics

```typescript
class DeepLinkAnalytics {
  constructor(private prisma: PrismaClient) {}

  /**
   * Track deep link click
   */
  async trackClick(params: {
    link: string;
    source: string;
    campaign?: string;
    medium?: string;
  }): Promise<void> {
    await this.prisma.deepLinkAnalytics.create({
      data: {
        link: params.link,
        source: params.source,
        campaign: params.campaign,
        medium: params.medium,
        clickedAt: new Date(),
      },
    });
  }

  /**
   * Track deep link open
   */
  async trackOpen(params: {
    link: string;
    userId?: string;
  }): Promise<void> {
    await this.prisma.deepLinkAnalytics.updateMany({
      where: {
        link: params.link,
        userId: params.userId || null,
      },
      data: {
        openedAt: new Date(),
      },
    });
  }

  /**
   * Get analytics
   */
  async getAnalytics(params: {
    startDate: Date;
    endDate: Date;
  }): Promise<{
    totalClicks: number;
    totalOpens: number;
    openRate: number;
    bySource: Record<string, { clicks: number; opens: number }>;
  }> {
    const analytics = await this.prisma.deepLinkAnalytics.findMany({
      where: {
        clickedAt: {
          gte: params.startDate,
          lte: params.endDate,
        },
      },
    });

    const totalClicks = analytics.length;
    const totalOpens = analytics.filter(a => a.openedAt).length;
    const openRate = totalClicks > 0 ? (totalOpens / totalClicks) * 100 : 0;

    const bySource: Record<string, { clicks: number; opens: number }> = {};

    for (const item of analytics) {
      const source = item.source || 'direct';
      if (!bySource[source]) {
        bySource[source] = { clicks: 0, opens: 0 };
      }

      bySource[source].clicks++;
      if (item.openedAt) {
        bySource[source].opens++;
      }
    }

    return {
      totalClicks,
      totalOpens,
      openRate,
      bySource,
    };
  }
}
```

---

## Common Patterns

### Deep Link Patterns

```typescript
// 1. Product deep link
const productDeepLink = (productId: string) => {
  return `https://myapp.com/product?id=${productId}`;
};

// 2. Profile deep link
const profileDeepLink = (userId: string) => {
  return `https://myapp.com/profile?userId=${userId}`;
};

// 3. Order deep link
const orderDeepLink = (orderId: string) => {
  return `https://myapp.com/order?orderId=${orderId}`;
};

// 4. Checkout deep link
const checkoutDeepLink = () => {
  return `https://myapp.com/checkout`;
};

// 5. Referral deep link
const referralDeepLink = (referralCode: string) => {
  return `https://myapp.com/referral?code=${referralCode}`;
};

// 6. Share deep link
const shareDeepLink = (contentId: string, type: 'product' | 'profile') => {
  return `https://myapp.com/share?type=${type}&id=${contentId}`;
};
```

---

## Best Practices

### Deep Link Best Practices

```typescript
// 1. Always validate deep links
function validateDeepLink(url: string): {
  valid: boolean;
  route: string;
  params: Record<string, string>;
} {
  try {
    const parsedUrl = new URL(url);
    const pathname = parsedUrl.pathname;

    // Validate route
    const validRoutes = ['/', '/product', '/profile', '/order', '/checkout'];
    const isValidRoute = validRoutes.includes(pathname);

    return {
      valid: isValidRoute,
      route: pathname,
      params: Object.fromEntries(parsedUrl.searchParams.entries()),
    };
  } catch {
    return {
      valid: false,
      route: '/',
      params: {},
    };
  }
}

// 2. Handle all deep link types
function handleDeepLink(url: string): {
  route: string;
  params: Record<string, string>;
} {
  const { valid, route, params } = validateDeepLink(url);

  if (!valid) {
    return { route: '/', params: {} };
  }

  return { route, params };
}

// 3. Use fallback routes
function getFallbackRoute(route: string): string {
  const routeMap: Record<string, string> = {
    '/product': '/product',
    '/products': '/products',
    '/p': '/product',
    '/u': '/profile',
    '/user': '/profile',
    '/o': '/order',
    '/orders': '/orders',
    '/c': '/checkout',
    '/cart': '/cart',
  };

  return routeMap[route] || '/';
}

// 4. Track deep link analytics
async function trackDeepLinkAnalytics(params: {
  link: string;
  source: string;
  campaign?: string;
}): Promise<void> {
  const analytics = new DeepLinkAnalytics(prisma);

  await analytics.trackClick({
    link: params.link,
    source: params.source,
    campaign: params.campaign,
  });
}

// 5. Test deep links thoroughly
async function testDeepLinkFlow(link: string): Promise<void> {
  // 1. Test link generation
  console.log('Testing link generation:', link);

  // 2. Test link parsing
  const parsed = validateDeepLink(link);
  console.log('Parsed link:', parsed);

  // 3. Test navigation
  console.log('Testing navigation to:', parsed.route, parsed.params);

  // 4. Test analytics
  await trackDeepLinkAnalytics({
    link,
    source: 'test',
  });

  console.log('Deep link test completed');
}
```

---

---

## Quick Start

### React Navigation Deep Linking

```typescript
import { Linking } from 'react-native'
import { NavigationContainer } from '@react-navigation/native'

const linking = {
  prefixes: ['myapp://', 'https://myapp.com'],
  config: {
    screens: {
      Home: '',
      Product: 'product/:id',
      Profile: 'profile/:userId'
    }
  }
}

function App() {
  return (
    <NavigationContainer linking={linking}>
      {/* Navigation */}
    </NavigationContainer>
  )
}
```

### Handle Deep Links

```typescript
useEffect(() => {
  // Handle initial URL
  Linking.getInitialURL().then(url => {
    if (url) {
      handleDeepLink(url)
    }
  })
  
  // Handle URL changes
  const subscription = Linking.addEventListener('url', ({ url }) => {
    handleDeepLink(url)
  })
  
  return () => subscription.remove()
}, [])
```

---

## Production Checklist

- [ ] **URL Scheme**: Configure URL scheme (iOS) and intent filters (Android)
- [ ] **Universal Links**: Set up Universal Links (iOS) and App Links (Android)
- [ ] **Deep Link Handling**: Handle deep links in app
- [ ] **Fallback**: Fallback to web if app not installed
- [ ] **Analytics**: Track deep link usage
- [ ] **Testing**: Test deep links on real devices
- [ ] **Error Handling**: Handle invalid or broken links
- [ ] **Security**: Validate deep link parameters
- [ ] **Documentation**: Document deep link format
- [ ] **Branch.io/Adjust**: Consider deep linking service
- [ ] **Deferred Deep Linking**: Support deferred deep linking
- [ ] **Attribution**: Track attribution from deep links

---

## Anti-patterns

### ❌ Don't: No Fallback

```typescript
// ❌ Bad - No fallback
const url = 'myapp://product/123'
Linking.openURL(url)  // Fails if app not installed
```

```typescript
// ✅ Good - Fallback to web
async function openDeepLink(url: string) {
  const canOpen = await Linking.canOpenURL(url)
  if (canOpen) {
    await Linking.openURL(url)
  } else {
    // Fallback to web
    await Linking.openURL(`https://myapp.com${url.replace('myapp://', '')}`)
  }
}
```

### ❌ Don't: No Validation

```typescript
// ❌ Bad - No validation
function handleDeepLink(url: string) {
  const productId = extractProductId(url)  // Could be malicious!
  navigateToProduct(productId)
}
```

```typescript
// ✅ Good - Validate parameters
function handleDeepLink(url: string) {
  const productId = extractProductId(url)
  if (isValidProductId(productId)) {
    navigateToProduct(productId)
  } else {
    showError('Invalid product ID')
  }
}
```

---

## Integration Points

- **Push Notifications** (`31-mobile-development/push-notifications/`) - Deep links from notifications
- **React Native Patterns** (`31-mobile-development/react-native-patterns/`) - Navigation patterns

---

## Further Reading

- [React Navigation Deep Linking](https://reactnavigation.org/docs/deep-linking)
- [Apple Universal Links](https://developer.apple.com/documentation/xcode/inter-app-links)
- [Android App Links](https://developer.android.com/training/app-links)
- [Android App Links](https://developer.android.com/training/app-links)
- [Branch.io Documentation](https://help.branch.io/)
- [Firebase Dynamic Links](https://firebase.google.com/docs/dynamic-links)
