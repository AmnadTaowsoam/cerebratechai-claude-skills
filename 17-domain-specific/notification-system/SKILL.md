# Notification System

## Overview

A notification system delivers messages to users through various channels. This skill covers notification types (email, SMS, push, in-app), service integration (SendGrid/AWS SES, Twilio, Firebase), template management, notification preferences, queue-based delivery, retry logic, delivery tracking, rate limiting, testing, and best practices.

## Table of Contents

1. [Notification Types](#notification-types)
2. [Service Integration](#service-integration)
   - [Email (SendGrid/AWS SES)](#email-sendgridaws-ses)
   - [SMS (Twilio)](#sms-twilio)
   - [Push Notifications (Firebase)](#push-notifications-firebase)
   - [In-App Notifications](#in-app-notifications)
3. [Template Management](#template-management)
4. [Notification Preferences](#notification-preferences)
5. [Queue-Based Delivery](#queue-based-delivery)
6. [Retry Logic](#retry-logic)
7. [Delivery Tracking](#delivery-tracking)
8. [Testing](#testing)
9. [Best Practices](#best-practices)

---

## Notification Types

### Email Notifications

```typescript
// src/notifications/email-notification.ts
export interface EmailNotification {
  to: string | string[];
  subject: string;
  html?: string;
  text?: string;
  templateId?: string;
  templateData?: Record<string, any>;
  attachments?: EmailAttachment[];
  from?: string;
  replyTo?: string;
}

export interface EmailAttachment {
  filename: string;
  content: string | Buffer;
  contentType?: string;
}
```

### SMS Notifications

```typescript
// src/notifications/sms-notification.ts
export interface SMSNotification {
  to: string;
  body: string;
  from?: string;
  mediaUrls?: string[];
}
```

### Push Notifications

```typescript
// src/notifications/push-notification.ts
export interface PushNotification {
  to: string | string[];
  title: string;
  body: string;
  data?: Record<string, any>;
  badge?: number;
  sound?: string;
  image?: string;
  priority?: 'high' | 'normal';
  ttl?: number;
}
```

### In-App Notifications

```typescript
// src/notifications/inapp-notification.ts
export interface InAppNotification {
  userId: string;
  title: string;
  body: string;
  type: NotificationType;
  data?: Record<string, any>;
  actionUrl?: string;
  expiresAt?: Date;
}

export enum NotificationType {
  INFO = 'info',
  SUCCESS = 'success',
  WARNING = 'warning',
  ERROR = 'error',
}
```

---

## Service Integration

### Email (SendGrid/AWS SES)

#### SendGrid Integration

```typescript
// src/notifications/sendgrid.service.ts
import sgMail from '@sendgrid/mail';

const SENDGRID_API_KEY = process.env.SENDGRID_API_KEY || '';

sgMail.setApiKey(SENDGRID_API_KEY);

export class SendGridService {
  async sendEmail(notification: EmailNotification): Promise<void> {
    const msg: sgMail.MailDataRequired = {
      to: notification.to,
      from: notification.from || 'noreply@example.com',
      subject: notification.subject,
      text: notification.text,
      html: notification.html,
      templateId: notification.templateId,
      dynamicTemplateData: notification.templateData,
      attachments: notification.attachments?.map(att => ({
        filename: att.filename,
        content: att.content.toString('base64'),
        type: att.contentType,
        disposition: 'attachment',
      })),
    };

    try {
      await sgMail.send(msg);
      console.log('Email sent successfully:', notification.to);
    } catch (error) {
      console.error('Failed to send email:', error);
      throw error;
    }
  }

  async sendTemplateEmail(
    to: string | string[],
    templateId: string,
    templateData: Record<string, any>
  ): Promise<void> {
    const msg: sgMail.MailDataRequired = {
      to,
      from: 'noreply@example.com',
      templateId,
      dynamicTemplateData: templateData,
    };

    try {
      await sgMail.send(msg);
      console.log('Template email sent successfully:', to);
    } catch (error) {
      console.error('Failed to send template email:', error);
      throw error;
    }
  }
}

export const sendGridService = new SendGridService();
```

#### AWS SES Integration

```typescript
// src/notifications/aws-ses.service.ts
import { SESClient, SendEmailCommand } from '@aws-sdk/client-ses';

const sesClient = new SESClient({
  region: process.env.AWS_REGION || 'us-east-1',
});

export class AWSSESService {
  async sendEmail(notification: EmailNotification): Promise<void> {
    const command = new SendEmailCommand({
      Source: notification.from || 'noreply@example.com',
      Destination: {
        ToAddresses: Array.isArray(notification.to) ? notification.to : [notification.to],
      },
      Message: {
        Subject: { Data: notification.subject },
        Body: {
          Text: { Data: notification.text || '' },
          Html: { Data: notification.html || '' },
        },
      },
    });

    try {
      await sesClient.send(command);
      console.log('Email sent successfully:', notification.to);
    } catch (error) {
      console.error('Failed to send email:', error);
      throw error;
    }
  }
}

export const awsSESService = new AWSSESService();
```

### SMS (Twilio)

```typescript
// src/notifications/twilio.service.ts
import twilio from 'twilio';

const TWILIO_ACCOUNT_SID = process.env.TWILIO_ACCOUNT_SID || '';
const TWILIO_AUTH_TOKEN = process.env.TWILIO_AUTH_TOKEN || '';
const TWILIO_PHONE_NUMBER = process.env.TWILIO_PHONE_NUMBER || '';

const client = twilio(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN);

export class TwilioService {
  async sendSMS(notification: SMSNotification): Promise<void> {
    try {
      const message = await client.messages.create({
        body: notification.body,
        from: notification.from || TWILIO_PHONE_NUMBER,
        to: notification.to,
        mediaUrl: notification.mediaUrls,
      });

      console.log('SMS sent successfully:', message.sid);
    } catch (error) {
      console.error('Failed to send SMS:', error);
      throw error;
    }
  }

  async sendBulkSMS(notifications: SMSNotification[]): Promise<void> {
    const promises = notifications.map(notification => this.sendSMS(notification));
    await Promise.all(promises);
  }
}

export const twilioService = new TwilioService();
```

### Push Notifications (Firebase)

```typescript
// src/notifications/firebase.service.ts
import admin from 'firebase-admin';

const firebaseConfig = {
  credential: admin.credential.cert({
    projectId: process.env.FIREBASE_PROJECT_ID,
    privateKey: process.env.FIREBASE_PRIVATE_KEY?.replace(/\\n/g, '\n'),
    clientEmail: process.env.FIREBASE_CLIENT_EMAIL,
  }),
};

admin.initializeApp(firebaseConfig);

export class FirebasePushService {
  async sendPushNotification(notification: PushNotification): Promise<void> {
    const message: admin.messaging.Message = {
      notification: {
        title: notification.title,
        body: notification.body,
        badge: notification.badge,
        sound: notification.sound,
        imageUrl: notification.image,
      },
      data: notification.data,
      android: {
        priority: notification.priority || 'normal',
        ttl: notification.ttl,
      },
      apns: {
        payload: {
          aps: {
            badge: notification.badge,
            sound: notification.sound,
          },
        },
      },
      token: Array.isArray(notification.to) ? undefined : notification.to,
      topic: Array.isArray(notification.to) ? undefined : notification.to,
      tokens: Array.isArray(notification.to) ? notification.to : undefined,
    };

    try {
      const response = await admin.messaging().send(message);
      console.log('Push notification sent successfully:', response);
    } catch (error) {
      console.error('Failed to send push notification:', error);
      throw error;
    }
  }

  async sendMulticastNotification(notification: PushNotification): Promise<void> {
    if (!Array.isArray(notification.to)) {
      throw new Error('Multicast requires array of tokens');
    }

    const message: admin.messaging.MulticastMessage = {
      notification: {
        title: notification.title,
        body: notification.body,
      },
      data: notification.data,
      tokens: notification.to,
    };

    try {
      const response = await admin.messaging().sendMulticast(message);
      console.log('Multicast notification sent:', response.successCount, 'successful');
      
      if (response.failureCount > 0) {
        console.error('Failed tokens:', response.responses
          .filter(r => !r.success)
          .map(r => r.error));
      }
    } catch (error) {
      console.error('Failed to send multicast notification:', error);
      throw error;
    }
  }
}

export const firebasePushService = new FirebasePushService();
```

### In-App Notifications

```typescript
// src/notifications/inapp.service.ts
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export class InAppNotificationService {
  async createNotification(notification: InAppNotification): Promise<void> {
    try {
      await prisma.notification.create({
        data: {
          userId: notification.userId,
          title: notification.title,
          body: notification.body,
          type: notification.type,
          data: notification.data,
          actionUrl: notification.actionUrl,
          expiresAt: notification.expiresAt,
          read: false,
        },
      });
      
      console.log('In-app notification created:', notification.userId);
    } catch (error) {
      console.error('Failed to create in-app notification:', error);
      throw error;
    }
  }

  async getUserNotifications(
    userId: string,
    unreadOnly: boolean = false
  ): Promise<Notification[]> {
    const where: any = { userId };
    
    if (unreadOnly) {
      where.read = false;
    }

    return prisma.notification.findMany({
      where,
      orderBy: { createdAt: 'desc' },
    });
  }

  async markAsRead(notificationId: string): Promise<void> {
    await prisma.notification.update({
      where: { id: notificationId },
      data: { read: true },
    });
  }

  async markAllAsRead(userId: string): Promise<void> {
    await prisma.notification.updateMany({
      where: { userId },
      data: { read: true },
    });
  }

  async deleteNotification(notificationId: string): Promise<void> {
    await prisma.notification.delete({
      where: { id: notificationId },
    });
  }
}

export const inAppNotificationService = new InAppNotificationService();
```

---

## Template Management

### Email Templates

```typescript
// src/notifications/email-templates.ts
export interface EmailTemplate {
  id: string;
  name: string;
  subject: string;
  html: string;
  text?: string;
}

export const EmailTemplates: Record<string, EmailTemplate> = {
  WELCOME_EMAIL: {
    id: 'd-1234567890',
    name: 'Welcome Email',
    subject: 'Welcome to {{company_name}}!',
    html: `
      <h1>Welcome, {{user_name}}!</h1>
      <p>Thank you for joining {{company_name}}.</p>
      <p>We're excited to have you on board.</p>
      <a href="{{verify_email_url}}">Verify your email</a>
    `,
    text: `
      Welcome, {{user_name}}!
      
      Thank you for joining {{company_name}}.
      We're excited to have you on board.
      
      Verify your email: {{verify_email_url}}
    `,
  },

  PASSWORD_RESET: {
    id: 'd-0987654321',
    name: 'Password Reset',
    subject: 'Reset your password',
    html: `
      <h1>Password Reset Request</h1>
      <p>Hi {{user_name}},</p>
      <p>We received a request to reset your password.</p>
      <a href="{{reset_url}}">Reset your password</a>
      <p>If you didn't request this, please ignore this email.</p>
    `,
    text: `
      Password Reset Request
      
      Hi {{user_name}},
      
      We received a request to reset your password.
      
      Reset your password: {{reset_url}}
      
      If you didn't request this, please ignore this email.
    `,
  },

  ORDER_CONFIRMATION: {
    id: 'd-1122334455',
    name: 'Order Confirmation',
    subject: 'Order #{{order_id}} Confirmed',
    html: `
      <h1>Order Confirmed!</h1>
      <p>Thank you for your order, {{user_name}}.</p>
      <p>Order #{{order_id}}</p>
      <p>Total: ${{order_total}}</p>
      <a href="{{order_url}}">View your order</a>
    `,
    text: `
      Order Confirmed!
      
      Thank you for your order, {{user_name}}.
      Order #{{order_id}}
      Total: ${{order_total}}
      
      View your order: {{order_url}}
    `,
  },
};
```

### Template Rendering

```typescript
// src/notifications/template-renderer.ts
export class TemplateRenderer {
  render(template: string, data: Record<string, any>): string {
    return template.replace(/\{\{(\w+)\}\}/g, (match, key) => {
      return data[key] !== undefined ? data[key] : match;
    });
  }

  renderEmailTemplate(
    template: EmailTemplate,
    data: Record<string, any>
  ): EmailNotification {
    return {
      to: data.to,
      subject: this.render(template.subject, data),
      html: this.render(template.html, data),
      text: template.text ? this.render(template.text, data) : undefined,
      templateId: template.id,
      templateData: data,
    };
  }
}

export const templateRenderer = new TemplateRenderer();
```

### Usage Example

```typescript
// src/notifications/notification-sender.ts
import { EmailTemplates } from './email-templates';
import { templateRenderer } from './template-renderer';
import { sendGridService } from './sendgrid.service';

export async function sendWelcomeEmail(
  userEmail: string,
  userName: string,
  verifyUrl: string
): Promise<void> {
  const template = EmailTemplates.WELCOME_EMAIL;
  
  const notification = templateRenderer.renderEmailTemplate(template, {
    to: userEmail,
    user_name: userName,
    company_name: 'Example Company',
    verify_email_url: verifyUrl,
  });

  await sendGridService.sendEmail(notification);
}
```

---

## Notification Preferences

### User Preferences Model

```typescript
// src/models/notification-preference.model.ts
import { Model, DataTypes } from 'sequelize';

class NotificationPreference extends Model {
  public id!: number;
  public userId!: string;
  public channel!: NotificationChannel;
  public enabled!: boolean;
  public types!: NotificationType[];
}

export enum NotificationChannel {
  EMAIL = 'email',
  SMS = 'sms',
  PUSH = 'push',
  IN_APP = 'in_app',
}

export enum NotificationType {
  MARKETING = 'marketing',
  TRANSACTIONAL = 'transactional',
  SECURITY = 'security',
  UPDATES = 'updates',
}

NotificationPreference.init({
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
  },
  userId: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  channel: {
    type: DataTypes.ENUM(...Object.values(NotificationChannel)),
    allowNull: false,
  },
  enabled: {
    type: DataTypes.BOOLEAN,
    defaultValue: true,
  },
  types: {
    type: DataTypes.ARRAY(DataTypes.ENUM(...Object.values(NotificationType))),
    defaultValue: [NotificationType.TRANSACTIONAL, NotificationType.SECURITY],
  },
}, {
  sequelize,
  modelName: 'NotificationPreference',
});

export default NotificationPreference;
```

### Preference Service

```typescript
// src/services/notification-preference.service.ts
import NotificationPreference, { NotificationChannel, NotificationType } from '../models/notification-preference.model';

export class NotificationPreferenceService {
  async getUserPreferences(userId: string): Promise<Map<NotificationChannel, NotificationPreference>> {
    const preferences = await NotificationPreference.findAll({
      where: { userId },
    });

    const map = new Map<NotificationChannel, NotificationPreference>();
    preferences.forEach(pref => map.set(pref.channel, pref));
    
    return map;
  }

  async isChannelEnabled(
    userId: string,
    channel: NotificationChannel,
    type: NotificationType
  ): Promise<boolean> {
    const preference = await NotificationPreference.findOne({
      where: { userId, channel },
    });

    if (!preference) {
      // Default: enable transactional and security notifications
      return [NotificationType.TRANSACTIONAL, NotificationType.SECURITY].includes(type);
    }

    return preference.enabled && preference.types.includes(type);
  }

  async updatePreferences(
    userId: string,
    channel: NotificationChannel,
    enabled: boolean,
    types: NotificationType[]
  ): Promise<NotificationPreference> {
    const [preference] = await NotificationPreference.findOrCreate({
      where: { userId, channel },
      defaults: { enabled, types },
    });

    preference.enabled = enabled;
    preference.types = types;
    await preference.save();

    return preference;
  }

  async disableAllChannels(userId: string): Promise<void> {
    await NotificationPreference.update(
      { enabled: false },
      { where: { userId } }
    );
  }
}

export const notificationPreferenceService = new NotificationPreferenceService();
```

---

## Queue-Based Delivery

### Bull Queue Integration

```typescript
// src/queues/notification.queue.ts
import Queue from 'bull';
import { sendGridService } from '../notifications/sendgrid.service';
import { twilioService } from '../notifications/twilio.service';
import { firebasePushService } from '../notifications/firebase.service';
import { inAppNotificationService } from '../notifications/inapp.service';

const notificationQueue = new Queue('notifications', {
  redis: {
    host: process.env.REDIS_HOST || 'localhost',
    port: parseInt(process.env.REDIS_PORT || '6379'),
  },
});

interface NotificationJob {
  type: 'email' | 'sms' | 'push' | 'in_app';
  data: any;
  userId: string;
  retryCount?: number;
}

notificationQueue.process(async (job) => {
  const { type, data, userId } = job.data as NotificationJob;
  
  console.log(`Processing ${type} notification for user ${userId}`);

  try {
    switch (type) {
      case 'email':
        await sendGridService.sendEmail(data);
        break;
      case 'sms':
        await twilioService.sendSMS(data);
        break;
      case 'push':
        await firebasePushService.sendPushNotification(data);
        break;
      case 'in_app':
        await inAppNotificationService.createNotification(data);
        break;
    }
    
    console.log(`Successfully processed ${type} notification`);
  } catch (error) {
    console.error(`Failed to process ${type} notification:`, error);
    throw error;
  }
});

export async function enqueueNotification(job: NotificationJob): Promise<void> {
  await notificationQueue.add(job, {
    attempts: 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
    removeOnComplete: 100,
    removeOnFail: 50,
  });
}

export { notificationQueue };
```

### Usage Example

```typescript
// src/services/notification.service.ts
import { enqueueNotification } from '../queues/notification.queue';
import { notificationPreferenceService } from './notification-preference.service';
import { NotificationChannel, NotificationType } from '../models/notification-preference.model';

export class NotificationService {
  async sendNotification(
    userId: string,
    type: NotificationType,
    channels: NotificationChannel[],
    data: any
  ): Promise<void> {
    for (const channel of channels) {
      const enabled = await notificationPreferenceService.isChannelEnabled(
        userId,
        channel,
        type
      );

      if (!enabled) {
        console.log(`Channel ${channel} is disabled for user ${userId}`);
        continue;
      }

      await enqueueNotification({
        type: channel,
        data,
        userId,
      });
    }
  }

  async sendWelcomeNotification(
    userId: string,
    email: string,
    name: string,
    verifyUrl: string
  ): Promise<void> {
    await this.sendNotification(
      userId,
      NotificationType.TRANSACTIONAL,
      [NotificationChannel.EMAIL],
      {
        to: email,
        subject: 'Welcome!',
        html: `<h1>Welcome ${name}!</h1>`,
      }
    );
  }

  async sendOrderConfirmation(
    userId: string,
    email: string,
    orderId: string,
    total: number
  ): Promise<void> {
    await this.sendNotification(
      userId,
      NotificationType.TRANSACTIONAL,
      [NotificationChannel.EMAIL, NotificationChannel.IN_APP],
      {
        to: email,
        subject: `Order #${orderId} Confirmed`,
        html: `<h1>Order Confirmed!</h1><p>Total: $${total}</p>`,
        userId,
        title: 'Order Confirmed',
        body: `Your order #${orderId} has been confirmed.`,
        type: 'success',
      }
    );
  }
}

export const notificationService = new NotificationService();
```

---

## Retry Logic

```typescript
// src/notifications/retry.service.ts
import { notificationQueue } from '../queues/notification.queue';

interface RetryConfig {
  maxAttempts: number;
  initialDelay: number;
  maxDelay: number;
  backoffMultiplier: number;
}

export class RetryService {
  private config: RetryConfig = {
    maxAttempts: 3,
    initialDelay: 2000, // 2 seconds
    maxDelay: 60000, // 1 minute
    backoffMultiplier: 2,
  };

  async executeWithRetry<T>(
    fn: () => Promise<T>,
    context: string
  ): Promise<T> {
    let lastError: Error | undefined;
    let delay = this.config.initialDelay;

    for (let attempt = 1; attempt <= this.config.maxAttempts; attempt++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error as Error;
        
        console.error(
          `Attempt ${attempt} failed for ${context}:`,
          error
        );

        if (attempt < this.config.maxAttempts) {
          await this.sleep(delay);
          delay = Math.min(
            delay * this.config.backoffMultiplier,
            this.config.maxDelay
          );
        }
      }
    }

    throw new Error(
      `Max retry attempts (${this.config.maxAttempts}) reached for ${context}`,
      { cause: lastError }
    );
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  async retryFailedJob(jobId: string): Promise<void> {
    const job = await notificationQueue.getJob(jobId);
    
    if (!job) {
      throw new Error(`Job ${jobId} not found`);
    }

    const retryCount = (job.data.retryCount || 0) + 1;
    
    if (retryCount > this.config.maxAttempts) {
      console.log(`Max retries reached for job ${jobId}`);
      await job.moveToFailed(new Error('Max retries reached'));
      return;
    }

    job.data.retryCount = retryCount;
    await job.update(job.data);
    await job.retry();
    
    console.log(`Retrying job ${jobId}, attempt ${retryCount}`);
  }
}

export const retryService = new RetryService();
```

---

## Delivery Tracking

### Delivery Tracking Model

```typescript
// src/models/delivery-tracker.model.ts
import { Model, DataTypes } from 'sequelize';

class DeliveryTracker extends Model {
  public id!: number;
  public notificationId!: string;
  public channel!: NotificationChannel;
  public status!: DeliveryStatus;
  public attempts!: number;
  public lastAttemptAt?: Date;
  public deliveredAt?: Date;
  public error?: string;
  public metadata?: Record<string, any>;
}

export enum DeliveryStatus {
  PENDING = 'pending',
  SENDING = 'sending',
  DELIVERED = 'delivered',
  FAILED = 'failed',
  BOUNCED = 'bounced',
  OPENED = 'opened',
  CLICKED = 'clicked',
}

DeliveryTracker.init({
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true,
  },
  notificationId: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  channel: {
    type: DataTypes.ENUM(...Object.values(NotificationChannel)),
    allowNull: false,
  },
  status: {
    type: DataTypes.ENUM(...Object.values(DeliveryStatus)),
    allowNull: false,
    defaultValue: DeliveryStatus.PENDING,
  },
  attempts: {
    type: DataTypes.INTEGER,
    defaultValue: 0,
  },
  lastAttemptAt: {
    type: DataTypes.DATE,
  },
  deliveredAt: {
    type: DataTypes.DATE,
  },
  error: {
    type: DataTypes.TEXT,
  },
  metadata: {
    type: DataTypes.JSONB,
  },
}, {
  sequelize,
  modelName: 'DeliveryTracker',
});

export default DeliveryTracker;
```

### Delivery Tracking Service

```typescript
// src/services/delivery-tracker.service.ts
import DeliveryTracker, { DeliveryStatus } from '../models/delivery-tracker.model';
import { NotificationChannel } from '../models/notification-preference.model';

export class DeliveryTrackerService {
  async createTracker(
    notificationId: string,
    channel: NotificationChannel
  ): Promise<DeliveryTracker> {
    return DeliveryTracker.create({
      notificationId,
      channel,
      status: DeliveryStatus.PENDING,
      attempts: 0,
    });
  }

  async updateStatus(
    trackerId: number,
    status: DeliveryStatus,
    error?: string
  ): Promise<void> {
    const updateData: any = { status };
    
    if (status === DeliveryStatus.DELIVERED) {
      updateData.deliveredAt = new Date();
    }
    
    if (error) {
      updateData.error = error;
    }
    
    await DeliveryTracker.update(updateData, {
      where: { id: trackerId },
    });
  }

  async incrementAttempts(trackerId: number): Promise<void> {
    await DeliveryTracker.update(
      {
        attempts: DeliveryTracker.sequelize!.literal('attempts + 1'),
        lastAttemptAt: new Date(),
      },
      { where: { id: trackerId } }
    );
  }

  async getDeliveryStats(
    notificationId: string
  ): Promise<DeliveryStats> {
    const trackers = await DeliveryTracker.findAll({
      where: { notificationId },
    });

    const stats: DeliveryStats = {
      total: trackers.length,
      pending: 0,
      sending: 0,
      delivered: 0,
      failed: 0,
      bounced: 0,
    };

    trackers.forEach(tracker => {
      stats[tracker.status]++;
    });

    return stats;
  }
}

interface DeliveryStats {
  total: number;
  pending: number;
  sending: number;
  delivered: number;
  failed: number;
  bounced: number;
}

export const deliveryTrackerService = new DeliveryTrackerService();
```

---

## Testing

### Notification Service Tests

```typescript
// test/notifications/notification.service.test.ts
import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { notificationService } from '../../src/services/notification.service';
import { enqueueNotification } from '../../src/queues/notification.queue';

jest.mock('../../src/queues/notification.queue');

describe('Notification Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('should send notification to enabled channels', async () => {
    await notificationService.sendNotification(
      'user123',
      'transactional',
      ['email', 'sms'],
      { to: 'test@example.com', subject: 'Test' }
    );

    expect(enqueueNotification).toHaveBeenCalledTimes(2);
  });

  it('should skip disabled channels', async () => {
    await notificationService.sendNotification(
      'user123',
      'marketing',
      ['email', 'sms'],
      { to: 'test@example.com', subject: 'Test' }
    );

    expect(enqueueNotification).not.toHaveBeenCalled();
  });
});
```

---

## Best Practices

### 1. Use Templates

```typescript
// Good: Use templates
const template = EmailTemplates.WELCOME_EMAIL;
const notification = templateRenderer.renderEmailTemplate(template, {
  user_name: userName,
  company_name: 'Example Company',
});

// Bad: Hardcode content
const notification = {
  to: userEmail,
  subject: 'Welcome to Example Company!',
  html: `<h1>Welcome, ${userName}!</h1>`,
};
```

### 2. Respect User Preferences

```typescript
// Good: Check preferences
const enabled = await notificationPreferenceService.isChannelEnabled(
  userId,
  channel,
  type
);

if (enabled) {
  await sendNotification(channel, data);
}

// Bad: Ignore preferences
await sendNotification(channel, data);
```

### 3. Use Queues for Delivery

```typescript
// Good: Use queue
await enqueueNotification({
  type: 'email',
  data: emailData,
  userId,
});

// Bad: Send synchronously
await sendEmail(emailData);
```

### 4. Implement Retry Logic

```typescript
// Good: Retry with exponential backoff
await retryService.executeWithRetry(
  () => sendEmail(data),
  'email delivery'
);

// Bad: No retry
try {
  await sendEmail(data);
} catch (error) {
  console.error('Failed to send email:', error);
}
```

### 5. Track Delivery

```typescript
// Good: Track delivery
const tracker = await deliveryTrackerService.createTracker(notificationId, channel);
await sendEmail(data);
await deliveryTrackerService.updateStatus(tracker.id, DeliveryStatus.DELIVERED);

// Bad: No tracking
await sendEmail(data);
```

---

## Summary

This skill covers comprehensive notification system implementation patterns including:

- **Notification Types**: Email, SMS, push, in-app notifications
- **Service Integration**: SendGrid/AWS SES (email), Twilio (SMS), Firebase (push), in-app
- **Template Management**: Email templates, template rendering
- **Notification Preferences**: User preferences model, preference service
- **Queue-Based Delivery**: Bull queue integration, notification service
- **Retry Logic**: Retry service with exponential backoff
- **Delivery Tracking**: Delivery tracker model, tracking service
- **Testing**: Notification service tests
- **Best Practices**: Use templates, respect preferences, use queues, implement retry, track delivery
