---
name: Mobile Push Notifications
description: Sending messages to users even when apps are not actively running using FCM, APNs, token management, and best practices for engagement and retention.
---

# Mobile Push Notifications

> **Current Level:** Intermediate  
> **Domain:** Mobile Development / Communication

---

## Overview

Push notifications enable apps to send messages to users even when the app is not actively running. This guide covers FCM, APNs, backend implementation, and best practices for building effective push notification systems that engage users without being intrusive.

---

---

## Core Concepts

### Table of Contents

1. [Push Notification Concepts](#push-notification-concepts)
2. [Firebase Cloud Messaging (FCM)](#firebase-cloud-messaging-fcm)
3. [Apple Push Notification Service (APNs)](#apple-push-notification-service-apns)
4. [Backend Implementation](#backend-implementation)
5. [Token Management](#token-management)
6. [Notification Handling](#notification-handling)
7. [Deep Linking from Notifications]((#deep-linking-from-notifications)
8. [Rich Notifications](#rich-notifications)
9. [Notification Channels (Android)](#notification-channels-android)
10. [Silent Notifications]((#silent-notifications)
11. [Testing](#testing)
12. [Analytics](#analytics)
13. [Best Practices](#best-practices)

---

## Push Notification Concepts

### Notification Types

```typescript
enum NotificationType {
  PUSH = 'push',           // Standard push notification
  DATA = 'data',           // Data-only message
  SILENT = 'silent',       // Silent notification
  RICH = 'rich',           // Rich notification with media
}

enum NotificationPriority {
  HIGH = 'high',
  NORMAL = 'normal',
}

enum NotificationCategory {
  PROMOTIONAL = 'promotional',
  TRANSACTIONAL = 'transactional',
  ALERT = 'alert',
  REMINDER = 'reminder',
}
```

---

## Firebase Cloud Messaging (FCM)

### FCM Setup

```typescript
// npm install firebase-admin
import admin from 'firebase-admin';

const serviceAccount = require('./firebase-service-account.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});

const fcm = admin.messaging();

class FCMService {
  /**
   * Send notification
   */
  async sendNotification(params: {
    token: string;
    title: string;
    body: string;
    data?: Record<string, string>;
    imageUrl?: string;
    priority?: NotificationPriority;
  }): Promise<string> {
    const message: admin.messaging.Message = {
      token: params.token,
      notification: {
        title: params.title,
        body: params.body,
        imageUrl: params.imageUrl,
      },
      data: params.data,
      android: {
        priority: params.priority === NotificationPriority.HIGH ? 'high' : 'normal',
        notification: {
          channel_id: 'default',
          sound: 'default',
        },
      },
      apns: {
        payload: {
          aps: {
            sound: 'default',
            badge: 1,
          },
        },
      },
    };

    const messageId = await fcm.send(message);
    return messageId;
  }

  /**
   * Send multicast notification
   */
  async sendMulticast(params: {
    tokens: string[];
    title: string;
    body: string;
    data?: Record<string, string>;
  }): Promise<{
    successCount: number;
    failureCount: number;
    responses: BatchResponse[];
  }> {
    const message: admin.messaging.Message = {
      notification: {
        title: params.title,
        body: params.body,
      },
      data: params.data,
    };

    const response = await fcm.sendMulticast(message, params.tokens);

    return {
      successCount: response.successCount,
      failureCount: response.failureCount,
      responses: response.responses,
    };
  }

  /**
   * Send topic message
   */
  async sendToTopic(params: {
    topic: string;
    title: string;
    body: string;
    data?: Record<string, string>;
  }): Promise<string> {
    const message: admin.messaging.Message = {
      topic: params.topic,
      notification: {
        title: params.title,
        body: params.body,
      },
      data: params.data,
    };

    const messageId = await fcm.send(message);
    return messageId;
  }

  /**
   * Subscribe to topic
   */
  async subscribeToTopic(params: {
    token: string;
    topic: string;
  }): Promise<void> {
    await fcm.subscribeToTopic(params.token, params.topic);
  }

  /**
   * Unsubscribe from topic
   */
  async unsubscribeFromTopic(params: {
    token: string;
    topic: string;
  }): Promise<void> {
    await fcm.unsubscribeFromTopic(params.token, params.topic);
  }

  /**
   * Send silent notification
   */
  async sendSilentNotification(params: {
    token: string;
    data: Record<string, string>;
  }): Promise<string> {
    const message: admin.messaging.Message = {
      token: params.token,
      data: params.data,
      android: {
        priority: 'high',
      ttl: 3600, // 1 hour
      },
      apns: {
        headers: {
          'apns-priority': '10',
        },
      },
    };

    const messageId = await fcm.send(message);
    return messageId;
  }
}

interface BatchResponse {
  success: boolean;
  messageId?: string;
  error?: admin.messaging.FirebaseError;
}
```

### React Native FCM

```typescript
// npm install @react-native-firebase/app @react-native-firebase/messaging
import messaging, { FirebaseMessagingTypes } from '@react-native-firebase/messaging';
import { Platform } from 'react-native';

class PushNotificationService {
  private unsubscribe: (() => void) | null = null;

  /**
   * Initialize
   */
  async initialize(): Promise<void> {
    if (!messaging().isDeviceRegisteredForRemoteMessages) {
      await messaging().registerDeviceForRemoteMessages();
    }

    // Request permission on iOS
    if (Platform.OS === 'ios') {
      const authStatus = await messaging().requestPermission();
      if (authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
          authStatus === messaging.AuthorizationStatus.PROVISIONAL) {
        await this.getToken();
      }
    } else {
      await this.getToken();
    }

    // Set up listeners
    this.setupListeners();
  }

  /**
   * Get token
   */
  private async getToken(): Promise<string | null> {
    try {
      const token = await messaging().getToken();
      console.log('FCM Token:', token);

      // Send token to backend
      await this.sendTokenToBackend(token);

      return token;
    } catch (error) {
      console.error('Error getting FCM token:', error);
      return null;
    }
  }

  /**
   * Send token to backend
   */
  private async sendTokenToBackend(token: string): Promise<void> {
    // Implement token registration
    await apiService.registerPushToken(token);
  }

  /**
   * Set up listeners
   */
  private setupListeners(): void {
    // Foreground messages
    this.unsubscribe = messaging().onMessage(async (remoteMessage: FirebaseMessagingTypes.RemoteMessage) => {
      console.log('Foreground message:', remoteMessage);

      // Handle foreground message
      this.handleForegroundMessage(remoteMessage);
    });

    // Background/quit state messages
    messaging().setBackgroundMessageHandler(async (remoteMessage) => {
      console.log('Background message:', remoteMessage);

      // Handle background message
      await this.handleBackgroundMessage(remoteMessage);
    });

    // Token refresh
    messaging().onTokenRefresh(async (token) => {
      console.log('Token refreshed:', token);
      await this.sendTokenToBackend(token);
    });
  }

  /**
   * Handle foreground message
   */
  private handleForegroundMessage(
    remoteMessage: FirebaseMessagingTypes.RemoteMessage
  ): void {
    // Show local notification
    this.showLocalNotification({
      title: remoteMessage.notification?.title || 'New Message',
      body: remoteMessage.notification?.body || '',
      data: remoteMessage.data,
    });
  }

  /**
   * Handle background message
   */
  private async handleBackgroundMessage(
    remoteMessage: FirebaseMessagingTypes.RemoteMessage
  ): Promise<void> {
    // Process data in background
    if (remoteMessage.data) {
      await this.processData(remoteMessage.data);
    }
  }

  /**
   * Show local notification
   */
  private showLocalNotification(params: {
    title: string;
    body: string;
    data?: Record<string, string>;
  }): void {
    // Implement local notification
    console.log('Show local notification:', params);
  }

  /**
   * Process data
   */
  private async processData(data: Record<string, string>): Promise<void> {
    // Implement data processing
    console.log('Process data:', data);
  }

  /**
   * Cleanup
   */
  cleanup(): void {
    if (this.unsubscribe) {
      this.unsubscribe();
      this.unsubscribe = null;
    }
  }
}

// Usage in App.tsx
import { useEffect } from 'react';
import { PushNotificationService } from './services/PushNotificationService';

function App() {
  const pushService = new PushNotificationService();

  useEffect(() => {
    pushService.initialize();

    return () => {
      pushService.cleanup();
    };
  }, []);

  return <YourApp />;
}
```

---

## Apple Push Notification Service (APNs)

### APNs Setup

```typescript
// npm install apn
import apn from 'apn';

class APNsService {
  private provider: apn.Provider;

  constructor() {
    this.provider = new apn.Provider({
      token: {
        key: process.env.APNS_KEY_PATH!,
        keyId: process.env.APNS_KEY_ID!,
        teamId: process.env.APNS_TEAM_ID!,
      },
      production: process.env.NODE_ENV === 'production',
    });
  }

  /**
   * Send notification
   */
  async sendNotification(params: {
    deviceToken: string;
    title: string;
    body: string;
    data?: Record<string, string>;
    badge?: number;
    sound?: string;
    category?: string;
    threadId?: string;
    mutableContent?: boolean;
  }): Promise<string> {
    const notification = new apn.Notification();

    notification.alert = {
      title: params.title,
      body: params.body,
    };

    notification.badge = params.badge || 1;
    notification.sound = params.sound || 'default';
    notification.category = params.category || 'default';
    notification.threadId = params.threadId;
    notification.mutableContent = params.mutableContent || false;

    notification.payload = params.data;

    const message = new apn.Message();
    message.addDevice(params.deviceToken);
    message.setNotification(notification);

    const response = await this.provider.send(message);
    return response.sent[0];
  }

  /**
   * Send silent notification
   */
  async sendSilentNotification(params: {
    deviceToken: string;
    data: Record<string, string>;
    contentAvailable?: number;
  }): Promise<string> {
    const notification = new apn.Notification();

    notification.payload = params.data;
    notification.contentAvailable = params.contentAvailable || 1;

    const message = new apn.Message();
    message.addDevice(params.deviceToken);
    message.setNotification(notification);

    const response = await this.provider.send(message);
    return response.sent[0];
  }

  /**
   * Send multicast notification
   */
  async sendMulticast(params: {
    deviceTokens: string[];
    title: string;
    body: string;
    data?: Record<string, string>;
  }): Promise<{
    successCount: number;
    failureCount: number;
  }> {
    const notification = new apn.Notification();

    notification.alert = {
      title: params.title,
      body: params.body,
    };

    notification.payload = params.data;

    const message = new apn.Message();
    message.addDevices(params.deviceTokens);
    message.setNotification(notification);

    const response = await this.provider.send(message);

    return {
      successCount: response.sent.length,
      failureCount: response.failed.length,
    };
  }
}
```

---

## Backend Implementation

### Notification Service

```typescript
class NotificationService {
  private fcmService: FCMService;
  private apnsService: APNsService;

  constructor() {
    this.fcmService = new FCMService();
    this.apnsService = new APNsService();
  }

  /**
   * Send notification
   */
  async sendNotification(params: {
    userId: string;
    platform: 'ios' | 'android';
    title: string;
    body: string;
    data?: Record<string, string>;
    imageUrl?: string;
  }): Promise<void> {
    const user = await this.getUserDeviceToken(params.userId);

    if (!user) {
      throw new Error('User not found');
    }

    if (params.platform === 'ios') {
      await this.apnsService.sendNotification({
        deviceToken: user.deviceToken,
        title: params.title,
        body: params.body,
        data: params.data,
      });
    } else {
      await this.fcmService.sendNotification({
        token: user.deviceToken,
        title: params.title,
        body: params.body,
        data: params.data,
        imageUrl: params.imageUrl,
      });
    }
  }

  /**
   * Send to multiple users
   */
  async sendToMultipleUsers(params: {
    userIds: string[];
    title: string;
    body: string;
    data?: Record<string, string>;
  }): Promise<void> {
    const users = await this.getUserDeviceTokens(params.userIds);

    const iosTokens = users.filter(u => u.platform === 'ios').map(u => u.deviceToken);
    const androidTokens = users.filter(u => u.platform === 'android').map(u => u.deviceToken);

    // Send to iOS
    if (iosTokens.length > 0) {
      await this.apnsService.sendMulticast({
        deviceTokens: iosTokens,
        title: params.title,
        body: params.body,
        data: params.data,
      });
    }

    // Send to Android
    if (androidTokens.length > 0) {
      await this.fcmService.sendMulticast({
        tokens: androidTokens,
        title: params.title,
        body: params.body,
        data: params.data,
      });
    }
  }

  /**
   * Send to topic
   */
  async sendToTopic(params: {
    topic: string;
    title: string;
    body: string;
    data?: Record<string, string>;
  }): Promise<void> {
    await this.fcmService.sendToTopic({
      topic: params.topic,
      title: params.title,
      body: params.body,
      data: params.data,
    });
  }

  /**
   * Get user device token
   */
  private async getUserDeviceToken(userId: string): Promise<{
    deviceToken: string;
    platform: 'ios' | 'android';
  } | null> {
    const user = await prisma.user.findUnique({
      where: { id: userId },
      select: {
        deviceToken: true,
        platform: true,
      },
    });

    return user;
  }

  /**
   * Get user device tokens
   */
  private async getUserDeviceTokens(userIds: string[]): Promise<Array<{
    deviceToken: string;
    platform: 'ios' | 'android';
  }>> {
    const users = await prisma.user.findMany({
      where: { id: { in: userIds } },
      select: {
        deviceToken: true,
        platform: true,
      },
    });

    return users.filter(u => u.deviceToken);
  }
}
```

---

## Token Management

### Token Registration

```typescript
class TokenManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Register token
   */
  async registerToken(params: {
    userId: string;
    deviceToken: string;
    platform: 'ios' | 'android';
    appVersion?: string;
    deviceInfo?: Record<string, string>;
  }): Promise<void> {
    // Check if token already exists
    const existing = await this.prisma.pushToken.findFirst({
      where: {
        deviceToken: params.deviceToken,
      },
    });

    if (existing) {
      // Update existing token
      await this.prisma.pushToken.update({
        where: { id: existing.id },
        data: {
          userId: params.userId,
          platform: params.platform,
          appVersion: params.appVersion,
          deviceInfo: params.deviceInfo,
          isActive: true,
        },
      });
    } else {
      // Create new token
      await this.prisma.pushToken.create({
        data: {
          userId: params.userId,
          deviceToken: params.deviceToken,
          platform: params.platform,
          appVersion: params.appVersion,
          deviceInfo: params.deviceInfo,
          isActive: true,
        },
      });
    }
  }

  /**
   * Unregister token
   */
  async unregisterToken(deviceToken: string): Promise<void> {
    await this.prisma.pushToken.updateMany({
      where: { deviceToken },
      data: { isActive: false },
    });
  }

  /**
   * Get active tokens for user
   */
  async getActiveTokens(userId: string): Promise<Array<{
    deviceToken: string;
    platform: 'ios' | 'android';
  }>> {
    const tokens = await this.prisma.pushToken.findMany({
      where: {
        userId,
        isActive: true,
      },
      select: {
        deviceToken: true,
        platform: true,
      },
    });

    return tokens;
  }

  /**
   * Clean up inactive tokens
   */
  async cleanupInactiveTokens(daysInactive: number = 90): Promise<number> {
    const cutoffDate = new Date(Date.now() - daysInactive * 24 * 60 * 60 * 1000);

    const result = await this.prisma.pushToken.updateMany({
      where: {
        updatedAt: { lt: cutoffDate },
        isActive: true,
      },
      data: { isActive: false },
    });

    return result.count;
  }
}
```

---

## Notification Handling

### React Native Notification Handler

```typescript
// npm install @react-native-firebase/app @react-native-firebase/messaging @react-native-firebase/notifications
import { useEffect } from 'react';
import messaging, { FirebaseMessagingTypes } from '@react-native-firebase/messaging';
import { Notifications } from '@react-native-firebase/notifications';
import { Platform } from 'react-native';

function NotificationHandler() {
  useEffect(() => {
    // Set up message handlers
    const unsubscribe = messaging().onMessage(async (remoteMessage) => {
      console.log('Foreground message:', remoteMessage);
      // Handle foreground message
    });

    messaging().setBackgroundMessageHandler(async (remoteMessage) => {
      console.log('Background message:', remoteMessage);
      // Handle background message
    });

    // Handle notification open
    const unsubscribeOpen = Notifications().onNotificationOpenedApp((notificationOpen) => {
      console.log('Notification opened:', notificationOpen);
      // Handle notification open
    });

    // Handle notification display
    const unsubscribeDisplay = Notifications().onNotificationDisplayed((notification) => {
      console.log('Notification displayed:', notification);
    });

    return () => {
      unsubscribe();
      unsubscribeOpen();
      unsubscribeDisplay();
    };
  }, []);

  return null;
}
```

---

## Deep Linking from Notifications

### Deep Link Handler

```typescript
class DeepLinkHandler {
  /**
   * Handle notification deep link
   */
  async handleDeepLink(params: {
    notification: any;
    navigation: any;
  }): Promise<void> {
    const deepLink = params.notification?.data?.deepLink;

    if (!deepLink) {
      return;
    }

    // Parse deep link
    const parsed = this.parseDeepLink(deepLink);

    // Navigate to destination
    switch (parsed.type) {
      case 'product':
        params.navigation.navigate('ProductDetails', { productId: parsed.id });
        break;
      case 'order':
        params.navigation.navigate('OrderDetails', { orderId: parsed.id });
        break;
      case 'profile':
        params.navigation.navigate('Profile');
        break;
      default:
        params.navigation.navigate('Home');
    }
  }

  /**
   * Parse deep link
   */
  private parseDeepLink(url: string): {
    type: string;
    id: string;
  } {
    // Parse URL
    const parsed = new URL(url);
    const path = parsed.pathname;

    // Extract type and ID
    const parts = path.split('/').filter(p => p);

    if (parts[0] === 'product') {
      return { type: 'product', id: parts[1] };
    }

    if (parts[0] === 'order') {
      return { type: 'order', id: parts[1] };
    }

    return { type: 'home', id: '' };
  }
}
```

---

## Rich Notifications

### Rich Notification

```typescript
// npm install @react-native-firebase/notifications
import { Notifications } from '@react-native-firebase/notifications';

class RichNotificationService {
  /**
   * Send rich notification
   */
  async sendRichNotification(params: {
    title: string;
    body: string;
    imageUrl?: string;
    largeIcon?: string;
    bigPicture?: string;
    actions?: Array<{
      id: string;
      title: string;
      icon?: string;
    }>;
    data?: Record<string, string>;
  }): Promise<void> {
    const channelId = await this.createChannel();

    const notification = new Notifications.Notification();
    notification.setNotificationId(Math.random().toString());
    notification.setTitle(params.title);
    notification.setBody(params.body);
    notification.setData(params.data);
    notification.android.setChannelId(channelId);
    notification.android.setSmallIcon('@mipmap/ic_launcher');
    notification.android.setAutoCancel(true);

    if (params.imageUrl) {
      notification.android.setBigPicture(params.imageUrl);
    }

    if (params.actions) {
      notification.android.addAction(
        params.actions[0].id,
        params.actions[0].title,
        params.actions[0].icon,
        'action',
      );

      if (params.actions[1]) {
        notification.android.addAction(
          params.actions[1].id,
          params.actions[1].title,
          params.actions[1].icon,
          'cancel',
        );
      }
    }

    await Notifications.displayNotification(notification);
  }

  /**
   * Create channel
   */
  private async createChannel(): Promise<string> {
    const channel = new Notifications.Android.Channel(
      'rich_notifications',
      'Rich Notifications',
      'Notifications with media and actions',
      4, // importance
    );

    channel.setSound('default');
    channel.enableVibration(true);
    channel.enableLights(true);

    await Notifications.createChannel(channel);

    return channel.id;
  }
}
```

---

## Notification Channels (Android)

### Channel Manager

```typescript
// npm install @react-native-firebase/notifications
import { Notifications } from '@react-native-firebase/notifications';

class ChannelManager {
  /**
   * Create default channel
   */
  async createDefaultChannel(): Promise<void> {
    const channel = new Notifications.Android.Channel(
      'default',
      'Default',
      'Default notification channel',
      3, // importance
    );

    channel.setSound('default');
    channel.enableVibration(true);
    channel.enableLights(true);

    await Notifications.createChannel(channel);
  }

  /**
   * Create high priority channel
   */
  async createHighPriorityChannel(): Promise<void> {
    const channel = new Notifications.Android.Channel(
      'high_priority',
      'High Priority',
      'High priority notifications',
      5, // importance
    );

    channel.setSound('default');
    channel.enableVibration(true);
    channel.enableLights(true);

    await Notifications.createChannel(channel);
  }

  /**
   * Create silent channel
   */
  async createSilentChannel(): Promise<void> {
    const channel = new Notifications.Android.Channel(
      'silent',
      'Silent',
      'Silent notifications',
      1, // min importance
    );

    await Notifications.createChannel(channel);
  }

  /**
   * Create all channels
   */
  async createAllChannels(): Promise<void> {
    await this.createDefaultChannel();
    await this.createHighPriorityChannel();
    await this.createSilentChannel();
  }
}
```

---

## Silent Notifications

### Silent Notification Service

```typescript
class SilentNotificationService {
  /**
   * Send silent notification for data sync
   */
  async sendDataSync(params: {
    deviceToken: string;
    syncType: string;
    data?: Record<string, string>;
  }): Promise<void> {
    const message: admin.messaging.Message = {
      token: params.deviceToken,
      data: {
        type: 'data_sync',
        syncType: params.syncType,
        ...params.data,
      },
      android: {
        priority: 'high',
        ttl: 3600, // 1 hour
      },
      apns: {
        headers: {
          'apns-priority': '10',
        },
        payload: {
          aps: {
            'content-available': 1,
          },
        },
      },
    };

    await fcm.send(message);
  }

  /**
   * Send silent notification for location update
   */
  async sendLocationUpdate(params: {
    deviceToken: string;
    location: {
      latitude: number;
      longitude: number;
    };
  }): Promise<void> {
    const message: admin.messaging.Message = {
      token: params.deviceToken,
      data: {
        type: 'location_update',
        latitude: params.location.latitude.toString(),
        longitude: params.location.longitude.toString(),
      },
      android: {
        priority: 'high',
      },
      apns: {
        headers: {
          'apns-priority': '10',
        },
        payload: {
          aps: {
            'content-available': 1,
          },
        },
      },
    };

    await fcm.send(message);
  }
}
```

---

## Testing

### Notification Testing

```typescript
class NotificationTester {
  /**
   * Test notification
   */
  async testNotification(params: {
    deviceToken: string;
    title: string;
    body: string;
  }): Promise<void> {
    const fcmService = new FCMService();

    try {
      const messageId = await fcmService.sendNotification(params);
      console.log('Test notification sent:', messageId);
    } catch (error) {
      console.error('Error sending test notification:', error);
    }
  }

  /**
   * Test silent notification
   */
  async testSilentNotification(deviceToken: string): Promise<void> {
    const silentService = new SilentNotificationService();

    try {
      await silentService.sendDataSync({
        deviceToken,
        syncType: 'test',
      });
      console.log('Test silent notification sent');
    } catch (error) {
      console.error('Error sending test silent notification:', error);
    }
  }

  /**
   * Test topic subscription
   */
  async testTopicSubscription(params: {
    deviceToken: string;
    topic: string;
  }): Promise<void> {
    const fcmService = new FCMService();

    try {
      await fcmService.subscribeToTopic(params);
      console.log('Subscribed to topic:', params.topic);
    } catch (error) {
      console.error('Error subscribing to topic:', error);
    }
  }
}
```

---

## Analytics

### Notification Analytics

```typescript
class NotificationAnalytics {
  constructor(private prisma: PrismaClient) {}

  /**
   * Track notification sent
   */
  async trackSent(params: {
    notificationId: string;
    userIds: string[];
    platform: 'ios' | 'android';
    category: NotificationCategory;
  }): Promise<void> {
    await this.prisma.notificationAnalytics.create({
      data: {
        notificationId: params.notificationId,
        sentAt: new Date(),
        recipientCount: params.userIds.length,
        platform: params.platform,
        category: params.category,
      },
    });
  }

  /**
   * Track notification opened
   */
  async trackOpened(params: {
    notificationId: string;
    userId: string;
  }): Promise<void> {
    await this.prisma.notificationAnalytics.updateMany({
      where: { notificationId },
      data: {
        opens: { increment: 1 },
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
    category?: NotificationCategory;
  }): Promise<{
    totalSent: number;
    totalOpens: number;
    openRate: number;
    byCategory: Record<string, { sent: number; opened: number }>;
  }> {
    const where: any = {
      sentAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    if (params.category) {
      where.category = params.category;
    }

    const analytics = await this.prisma.notificationAnalytics.findMany({
      where,
    });

    const totalSent = analytics.reduce((sum, a) => sum + a.recipientCount, 0);
    const totalOpens = analytics.reduce((sum, a) => sum + a.opens, 0);

    const byCategory: Record<string, { sent: number; opened: number }> = {};

    for (const a of analytics) {
      if (!byCategory[a.category]) {
        byCategory[a.category] = { sent: 0, opened: 0 };
      }
      byCategory[a.category].sent += a.recipientCount;
      byCategory[a.category].opened += a.opens;
    }

    return {
      totalSent,
      totalOpens,
      openRate: totalSent > 0 ? (totalOpens / totalSent) * 100 : 0,
      byCategory,
    };
  }
}
```

---

## Best Practices

### Notification Best Practices

```typescript
// 1. Always handle notification permissions
async function requestNotificationPermission(): Promise<boolean> {
  const authStatus = await messaging().requestPermission();

  return authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
         authStatus === messaging.AuthorizationStatus.PROVISIONAL;
}

// 2. Use silent notifications for data sync
async function syncDataInBackground(deviceToken: string): Promise<void> {
  const silentService = new SilentNotificationService();

  await silentService.sendDataSync({
    deviceToken,
    syncType: 'background_sync',
    data: {
      timestamp: Date.now().toString(),
    },
  });
}

// 3. Use channels for Android
async function createChannels(): Promise<void> {
  const channelManager = new ChannelManager();
  await channelManager.createAllChannels();
}

// 4. Handle foreground messages gracefully
function handleForegroundMessage(
  remoteMessage: FirebaseMessagingTypes.RemoteMessage
): void {
  // Show local notification for foreground messages
  Notifications.displayLocalNotification({
    title: remoteMessage.notification?.title || 'New Message',
    body: remoteMessage.notification?.body || '',
    data: remoteMessage.data,
  });
}

// 5. Clean up inactive tokens
async function cleanupInactiveTokens(): Promise<void> {
  const tokenManager = new TokenManager(prisma);
  const cleaned = await tokenManager.cleanupInactiveTokens(90);
}
```

---

## Quick Start

### FCM Setup (React Native)

```javascript
import messaging from '@react-native-firebase/messaging'

// Request permission
async function requestPermission() {
  const authStatus = await messaging().requestPermission()
  return authStatus === messaging.AuthorizationStatus.AUTHORIZED
}

// Get FCM token
async function getToken() {
  const token = await messaging().getToken()
  // Send token to backend
  await api.saveDeviceToken(token)
  return token
}

// Handle notifications
messaging().onMessage(async remoteMessage => {
  console.log('Notification received:', remoteMessage)
  // Show local notification
})
```

### Backend: Send Push Notification

```javascript
const admin = require('firebase-admin')

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
})

async function sendPushNotification(token, title, body, data) {
  const message = {
    notification: { title, body },
    data: data,
    token: token
  }
  
  try {
    const response = await admin.messaging().send(message)
    return { success: true, messageId: response }
  } catch (error) {
    if (error.code === 'messaging/invalid-registration-token') {
      // Remove invalid token
      await removeToken(token)
    }
    throw error
  }
}
```

---

## Production Checklist

- [ ] **Permission**: Request notification permission properly
- [ ] **Token Management**: Store and manage device tokens
- [ ] **Token Refresh**: Handle token refresh on app updates
- [ ] **Invalid Tokens**: Clean up invalid/expired tokens
- [ ] **Segmentation**: Segment users for targeted notifications
- [ ] **Scheduling**: Support scheduled notifications
- [ ] **Deep Linking**: Deep links from notifications
- [ ] **Rich Notifications**: Rich media and actions
- [ ] **Analytics**: Track notification open rates
- [ ] **Rate Limiting**: Prevent notification spam
- [ ] **Testing**: Test on real devices
- [ ] **Error Handling**: Handle delivery failures

---

## Anti-patterns

### ❌ Don't: Send Without Permission

```javascript
// ❌ Bad - Send without checking permission
await sendNotification(token, message)  // User might not have permission!
```

```javascript
// ✅ Good - Check permission first
const hasPermission = await messaging().hasPermission()
if (hasPermission) {
  await sendNotification(token, message)
} else {
  await requestPermission()
}
```

### ❌ Don't: No Token Cleanup

```javascript
// ❌ Bad - Never clean up tokens
// Tokens accumulate forever!
```

```javascript
// ✅ Good - Clean up invalid tokens
async function sendNotification(token, message) {
  try {
    await admin.messaging().send({ token, ...message })
  } catch (error) {
    if (error.code === 'messaging/invalid-registration-token') {
      await db.tokens.delete({ where: { token } })
    }
  }
}
```

### ❌ Don't: Notification Spam

```javascript
// ❌ Bad - Send too many notifications
user.actions.forEach(action => {
  sendNotification(token, `You ${action}`)  // Spam!
})
```

```javascript
// ✅ Good - Batch and rate limit
const notificationQueue = []
user.actions.forEach(action => {
  notificationQueue.push(action)
})

// Send one summary notification
if (notificationQueue.length > 0) {
  sendNotification(token, `You have ${notificationQueue.length} updates`)
}
```

---

## Integration Points

- **Deep Linking** (`31-mobile-development/deep-linking/`) - Links from notifications
- **Mobile CI/CD** (`31-mobile-development/mobile-ci-cd/`) - Notification testing
- **Analytics** (`23-business-analytics/`) - Notification analytics

---

## Further Reading

- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)
- [Apple Push Notification Service](https://developer.apple.com/documentation/usernotifications)
- [React Native Firebase](https://rnfirebase.io/)

  console.log(`Cleaned up ${cleaned} inactive tokens`);
}
```

---

## Resources

- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging)
- [Apple Push Notifications](https://developer.apple.com/documentation/usernotifications)
- [React Native Firebase](https://rnfirebase.io/)
- [OneSignal](https://onesignal.com/)
- [Airship](https://www.airship.com/)
