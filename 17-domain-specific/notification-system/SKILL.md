# Notification System

A comprehensive guide to notification system implementation.

## Table of Contents

1. [Notification Types](#notification-types)
2. [Service Integration](#service-integration)
3. [Template Management](#template-management)
4. [Notification Preferences](#notification-preferences)
5. [Queue-Based Delivery](#queue-based-delivery)
6. [Retry Logic](#retry-logic)
7. [Delivery Tracking](#delivery-tracking)
8. [Rate Limiting](#rate-limiting)
9. [Testing](#testing)
10. [Best Practices](#best-practices)

---

## Notification Types

### Email Notifications

```typescript
// Send email notification
import { SendGrid } from '@sendgrid/mail';
import { EmailData } from './types';

export async function sendEmail(to: string, subject: string, html: string): Promise<void> {
  const msg = {
    to,
    from: process.env.SENDGRID_FROM_EMAIL,
    subject,
    html,
  };

  await sg.send(msg);
}
```

```python
# Send email notification
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content
from python.core import serializers

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

def send_email(to: str, subject: str, html: str) -> None:
    message = Mail(
        from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
        to_emails=[to],
        subject=subject,
        html_content=Content(html)
    )

    response = sg.send(message)
    print(f"Email sent: {response.status_code}")
```

### SMS Notifications

```typescript
// Send SMS notification
import twilio from 'twilio';

const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

export async function sendSMS(to: string, message: string): Promise<void> {
  const message = await client.messages.create({
    body: message,
    to,
    from: process.env.TWILIO_PHONE_NUMBER,
  });

  console.log(`SMS sent: ${message.sid}`);
}
```

```python
# Send SMS notification
from twilio.rest import Client

client = Client(
    os.environ.get('TWILIO_ACCOUNT_SID'),
    os.environ.get('TILIO_AUTH_TOKEN')
)

def send_sms(to: str, message: str) -> None:
    message = client.messages.create(
        body=message,
        to=to,
        from_=os.environ.get('TWILIO_PHONE_NUMBER')
    )

    print(f"SMS sent: {message.sid}")
```

### Push Notifications

```typescript
// Send push notification
import admin from 'firebase-admin';

const messaging = admin.messaging();

export async function sendPushNotification(userId: string, title: string, body: string): Promise<void> {
  const message = {
    notification: {
      title,
      body,
    },
    token: await getDeviceToken(userId),
  };

  await messaging.send(message);
}
```

```python
# Send push notification
from firebase_admin import messaging

messaging = messaging.Client(api_key=os.environ.get('FIREBASE_API_KEY'))

def send_push_notification(user_id: str, title: str, body: str) -> None:
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        token=get_device_token(user_id)
    )

    response = messaging.send(message)
    print(f"Push notification sent: {response}")
```

### In-App Notifications

```typescript
// In-app notification
import { toast } from 'react-hot-toast';

export function showNotification(title: string, message: string): void {
  toast.success(title, {
    description: message,
    position: 'top-right',
    autoClose: 5000,
  });
}
```

```python
# In-app notification (Django)
from django.contrib import messages

def show_in_app_notification(request, title: str, message: str) -> None:
    messages.success(request, title, message)
```

---

## Service Integration

### SendGrid Integration

```typescript
// services/emailService.ts
import { SendGrid } from '@sendgrid/mail';

const sg = new SendGrid(process.env.SENDGRID_API_KEY);

export class EmailService {
  async sendWelcomeEmail(to: string, name: string): Promise<void> {
    const html = `
      <h1>Welcome, ${name}!</h1>
      <p>Thank you for signing up for our service.</p>
      <p>We're excited to have you on board!</p>
    `;

    const msg = {
      to,
      from: process.env.SENDGRID_FROM_EMAIL,
      subject: 'Welcome to Our Service',
      html,
    };

    await sg.send(msg);
  }

  async sendPasswordResetEmail(to: string, resetToken: string): Promise<void> {
    const html = `
      <h1>Password Reset</h1>
      <p>Click the link below to reset your password:</p>
      <p><a href="${process.env.APP_URL}/reset?token=${resetToken}">Reset Password</a></p>
      `;

    const msg = {
      to,
      from: process.env.SENDGRID_FROM_EMAIL,
      subject: 'Password Reset',
      html,
    };

    await sg.send(msg);
  }
}
```

```python
# services/email_service.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Content
from python.core import serializers

sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))

class EmailService:
    @staticmethod
    def send_welcome_email(to: str, name: str):
        html = f"""
        <h1>Welcome, {name}!</h1>
        <p>Thank you for signing up for our service.</p>
        <p>We're excited to have you on board!</p>
        """
        message = Mail(
            from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
            to_emails=[to],
            subject='Welcome to Our Service',
            html_content=Content(html)
        )

        response = sg.send(message)
        return response.status_code

    @staticmethod
    def send_password_reset_email(to: str, reset_token: str):
        html = f"""
        <h1>Password Reset</h1>
        <p>Click the link below to reset your password:</p>
        <p><a href="{os.environ.get('APP_URL')}/reset?token={reset_token}">Reset Password</a></p>
        """
        message = Mail(
            from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
            to_emails=[to],
            subject='Password Reset',
            html_content=Content(html)
        )

        response = sg.send(message)
        return response.status_code
```

### Twilio Integration

```typescript
// services/smsService.ts
import twilio from 'twilio';

const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);

export class SMSService {
  async sendVerificationCode(to: string, code: string): Promise<void> {
    const message = await client.messages.create({
      body: `Your verification code is: ${code}`,
      to,
      from: process.env.TWILIO_PHONE_NUMBER,
    });

    console.log(`SMS sent: ${message.sid}`);
  }

  async sendAlert(to: string, message: string): Promise<void> {
    const msg = await client.messages.create({
      body: message,
      to,
      from: process.env.TWILIO_PHONE_NUMBER,
    });

    console.log(`Alert SMS sent: ${msg.sid}`);
  }
}
```

```python
# services/sms_service.py
from twilio.rest import Client

client = Client(
    os.environ.get('TWILIO_ACCOUNT_SID'),
    os.environ.get('TILIO_AUTH_TOKEN')
)

class SMSService:
    @staticmethod
    def send_verification_code(to: str, code: str):
        message = client.messages.create(
            body=f"Your verification code is: {code}",
            to=to,
            from_=os.environ.get('TILIO_PHONE_NUMBER')
        )
        print(f"SMS sent: {message.sid}")

    @staticmethod
    def send_alert(to: str, message: str):
        message = client.messages.create(
            body=message,
            to=to,
            from_=os.environ.get('TILIO_PHONE_NUMBER')
        )
        print(f"Alert SMS sent: {message.sid}")
```

### Firebase Integration

```typescript
// services/pushService.ts
import admin from 'firebase-admin';
import { getMessaging } from 'firebase-admin/messaging';

const messaging = getMessaging();

export class PushService {
  async sendPushNotification(userId: string, title: string, body: string): Promise<void> {
    const token = await this.getDeviceToken(userId);

    const message = {
      notification: {
        title,
        body,
      },
      token,
    };

    await messaging.send(message);
  }

  private async getDeviceToken(userId: string): Promise<string> {
    // Fetch device token from database
    const user = await prisma.user.findUnique({
      where: { id: userId },
      select: { deviceToken: true },
    });

    if (!user?.deviceToken) {
      throw new Error('No device token found');
    }

    return user.deviceToken;
  }
}
```

```python
# services/push_service.py
from firebase_admin import messaging

messaging = messaging.Client(api_key=os.environ.get('FIREBASE_API_KEY'))

class PushService:
    @staticmethod
    def send_push_notification(user_id: str, title: str, body: str):
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            token=get_device_token(user_id)
        )

        response = messaging.send(message)
        print(f"Push notification sent: {response}")

    @staticmethod
    def get_device_token(user_id: str) -> str:
        # Fetch device token from database
        user = get_user_from_db(user_id)
        return user.device_token or ""
```

---

## Template Management

### Email Templates

```typescript
// templates/emailTemplates.ts
export const emailTemplates = {
  welcome: (name: string) => `
    <h1>Welcome, ${name}!</h1>
    <p>Thank you for signing up for our service.</p>
    <p>We're excited to have you on board!</p>
    <p>Here are some tips to get started:</p>
    <ul>
      <li>Complete your profile</li>
      <li>Explore our features</li>
      <li>Contact support if you need help</li>
    </ul>
  </p>
    <p>Best regards,<br>The Team</p>
  `,

  passwordReset: (resetLink: string) => `
    <h1>Password Reset</h1>
    <p>Click the link below to reset your password:</p>
    <p><a href="${resetLink}">Reset Password</a></p>
    <p>If you didn't request this, please ignore this email.</p>
    </p>
    <p>Best regards,<br>The Team</p>
  `,

  orderConfirmation: (orderId: string, items: any[]) => `
    <h1>Order Confirmed #${orderId}</h1>
    <p>Thank you for your order!</p>
    <p>Order Details:</p>
    <ul>
      ${items.map(item => `<li>${item.name} - $${item.price}</li>`).join('')}
    </ul>
    <p>Total: $${items.reduce((sum, item) => sum + item.price, 0)}</p>
    </p>
    <p>Best regards,<br>The Team</p>
  `,
};
```

```python
# templates/email_templates.py
from string import Template

class EmailTemplates:
    welcome = Template("""
        <h1>Welcome, {{ name }}!</h1>
        <p>Thank you for signing up for our service.</p>
        <p>We're excited to have you on board!</p>
        <p>Here are some tips to get started:</p>
        <ul>
          <li>Complete your profile</li>
          <li>Explore our features</li>
          <li>Contact support if you need help</li>
        </ul>
        </p>
        <p>Best regards,<br>The Team</p>
    """)

    password_reset = Template("""
        <h1>Password Reset</h1>
        <p>Click the link below to reset your password:</p>
        <p><a href="{{ reset_link }}">Reset Password</a></p>
        <p>If you didn't request this, please ignore this email.</p>
        </p>
        <p>Best regards,<br>The Team</p>
    """)

    @staticmethod
    def render(template_name: str, **context) -> str:
        template = getattr(EmailTemplates, template_name)
        return template.render(**context)

    @staticmethod
    def welcome_email(name: str) -> str:
        return EmailTemplates.render('welcome', name=name)

    @staticmethod
    def password_reset_email(reset_link: str) -> str:
        return EmailTemplates.render('password_reset', reset_link=reset_link)
```

### SMS Templates

```typescript
// templates/smsTemplates.ts
export const smsTemplates = {
  verificationCode: (code: string) => `Your verification code is: ${code}`,
  alert: (message: string) => message,
  orderUpdate: (orderId: string, status: string) => `Order #${orderId} status: ${status}`,
};
```

```python
# templates/sms_templates.py
class SMSTemplates:
    verification_code = "Your verification code is: {code}"
    alert = "{message}"
    order_update = "Order #{order_id} status: {status}"
```

---

## Notification Preferences

### User Preferences Model

```typescript
// models/NotificationPreference.ts
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class NotificationPreference {
  @PrimaryGeneratedColumn()
  id: string;

  @Column()
  userId: string;

  @Column()
  emailEnabled: boolean;

  @Column()
  smsEnabled: boolean;

  @Column()
  pushEnabled: boolean;

  @Column({ type: 'json' })
  emailTypes: string[];

  @Column({ type: 'json' })
  smsTypes: string[];

  @Column({ type: 'json' })
  pushTypes: string[];
}
```

```python
# models/notification_preference.py
from sqlalchemy import Column, String, Boolean, JSON, Integer
from sqlalchemy.dialects.postgresql import UUID

class NotificationPreference(Base):
    __tablename__ = 'notification_preferences'

    id = Column(UUID(as_uuid=True, primary_key=True)
    user_id = Column(UUID, nullable=False)
    email_enabled = Column(Boolean, default=True)
    sms_enabled = Column(Boolean, default=False)
    push_enabled = Column(Boolean, default=True)
    email_types = Column(JSON, default=[])
    sms_types = Column(JSON, default=[])
    push_types = JSON, default=[])
```

### Managing Preferences

```typescript
// services/notificationPreference.service.ts
import { NotificationPreference } from '../models/NotificationPreference';

export class NotificationPreferenceService {
  async getPreferences(userId: string): Promise<NotificationPreference> {
    return await prisma.notificationPreference.findUnique({
      where: { userId },
    });
  }

  async updatePreferences(userId: string, updates: Partial<NotificationPreference>): Promise<NotificationPreference> {
    return prisma.notificationPreference.update({
      where: { userId },
      data: updates,
    });
  }

  async sendNotificationBasedOnPreferences(userId: string, notification: any): Promise<void> {
    const preferences = await this.getPreferences(userId);

    if (preferences.emailEnabled && notification.email) {
      await this.sendEmail(notification.email);
    }

    if (preferences.smsEnabled && notification.sms) {
      await this.sendSMS(notification.sms);
    }

    if (preferences.pushEnabled && notification.push) {
      await this.sendPush(userId, notification.push);
    }
  }

  private async sendEmail(email: EmailNotification): Promise<void> {
    // Send email using email service
  }

  private async sendSMS(sms: SMSNotification): Promise<void> {
    // Send SMS using SMS service
  }

  private async sendPush(userId: string, push: PushNotification): Promise<void> {
    // Send push notification using push service
  }
}
```

---

## Queue-Based Delivery

### Redis Queue

```typescript
// services/notificationQueue.service.ts
import { createClient } from 'redis';

const redis = createClient({ url: process.env.REDIS_URL });

export class NotificationQueue {
  async enqueue(notification: any): Promise<void> {
  const queueName = 'notifications';
  const payload = JSON.stringify(notification);

  await redis.lPush(queueName, payload);
  }

  async dequeue(): Promise<any> {
    const queueName = 'notifications';
    const payload = await redis.rPop(queueName);

    if (!payload) {
      return null;
    }

    return JSON.parse(payload);
  }

  async getQueueLength(): Promise<number> {
    return await redis.lLen('notifications');
  }
}
```

```python
# services/notification_queue.py
import redis
import json

redis = redis.Redis(host=os.environ.get('REDIS_HOST', port=6379)

class NotificationQueue:
    @staticmethod
    def enqueue(notification: dict) -> None:
        queue_name = "notifications"
        payload = json.dumps(notification)
        redis.rpush(queue_name, payload)

    @staticmethod
    def dequeue() -> dict:
        queue_name = "notifications"
        payload = redis.rpop(queue_name)

        if not payload:
            return None

        return json.loads(payload)

    @staticmethod
    def get_queue_length() -> int:
        queue_name = "notifications"
        return redis.llen(queue_name)
```

### Worker Process

```typescript
// workers/notificationWorker.ts
import { NotificationQueue } from '../services/notificationQueue.service';
import { EmailService } from '../services/emailService';
import { SMSService } from '../services/smsService';
import { PushService } from '../services/pushService';

export async function processNotifications(): Promise<void> {
  while (true) {
    const notification = await NotificationQueue.dequeue();

    if (!notification) {
      await sleep(1000); // Wait 1 second if queue is empty
      continue;
    }

    try {
      switch (notification.type) {
        case 'email':
          await EmailService.sendEmail(notification.to, notification.subject, notification.html);
          break;

        case 'sms':
          await SMSService.sendSMS(notification.to, notification.message);
          break;

        case 'push':
          await PushService.sendPushNotification(notification.userId, notification);
          break;

        default:
          console.log(`Unknown notification type: ${notification.type}`);
      }
    } catch (error) {
      console.error(`Error processing notification:`, error);

      // Requeue for retry
      await NotificationQueue.enqueue(notification);
    }
  }
}
```

```python
# workers/notification_worker.py
from services.notification_queue import NotificationQueue
from services.email_service import EmailService
from services.sms_service import SMSService
from services.push_service import PushService

async def process_notifications():
    while True:
        notification = await NotificationQueue.dequeue()

        if notification is None:
            await asyncio.sleep(1)  # Wait 1 second if queue is empty
            continue

        try:
            if notification['type'] == 'email':
                await EmailService.send_email(
                    notification['to'],
                    notification['subject'],
                    notification['html']
                )
            elif notification['type'] == 'sms':
                await SMSService.send_alert(
                    notification['to'],
                    notification['message']
                )
            elif notification['type'] == 'push':
                await PushService.send_push_notification(
                    notification['user_id'],
                    notification['title'],
                    notification['body']
                )
            else:
                print(f"Unknown notification type: {notification['type']}")
        except Exception as error:
            print(f"Error processing notification: {error}")
            # Requeue for retry
            await NotificationQueue.enqueue(notification)
```

# Run worker
if __name__ == '__main__':
    asyncio.run(process_notifications())
```

---

## Retry Logic

### Exponential Backoff

```typescript
// services/retry.service.ts
export async function withRetry<T>(
  fn: () => Promise,
  maxRetries: number = 3,
  baseDelay: number = 1000,
): Promise {
  let lastError: Error | null;
  let attempt = 0;

  while (attempt < maxRetries) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      const delay = baseDelay * Math.pow(2, attempt);
      await new Promise(resolve => setTimeout(resolve, delay));
      attempt++;
    }
  }

  throw lastError;
}
```

```python
# services/retry_service.py
import asyncio
import time

async def with_retry(func, max_retries=3, base_delay=1.0):
    last_error = None
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as error:
            last_error = error
            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)
    raise last_error
```

### Retry with Jitter

```typescript
// Add jitter to prevent thundering herd
export async function withJitteredRetry<T>(
  fn: () => Promise,
  maxRetries: number = 3,
  baseDelay: number = 1000,
): Promise {
  let lastError: Error | null;
  let attempt = 0;

  while (attempt < maxRetries) {
    try {
      return await fn();
    } catch (error) {
      lastError = error;
      const jitter = Math.random() * 0.5 * baseDelay; // 50% jitter
      const delay = baseDelay * Math.pow(2, attempt) + jitter;
      await new Promise(resolve => setTimeout(resolve, delay));
      attempt++;
    }
  }

  throw lastError;
}
```

---

## Delivery Tracking

### Delivery Status Model

```typescript
// models/DeliveryStatus.ts
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class DeliveryStatus {
  @PrimaryGeneratedColumn()
  id: string;

  @Column()
  notificationId: string;

  @Column()
  type: string;

  @Column()
  status: string;

  @Column()
  attempts: number;

  @Column({ type: 'json' })
  metadata: Record<string, any>;

  @Column()
  deliveredAt: Date;

  @Column()
  failedAt: Date;

  @Column()
  errorMessage: string;
}
```

```python
# models/delivery_status.py
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime

class DeliveryStatus(Base):
    __tablename__ = 'delivery_statuses'

    id = Column(UUID(as_uuid=True, primary_key=True)
    notification_id = Column(UUID, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    attempts = Column(Integer, default=0)
    metadata = Column(JSON, default={})
    delivered_at = Column(DateTime)
    failed_at = Column(DateTime)
    error_message = Column(String)
```

### Tracking Delivery

```typescript
// services/deliveryTracking.service.ts
import { DeliveryStatus } from '../models/DeliveryStatus';
import { prisma } from '../lib/prisma';

export class DeliveryTrackingService {
  async createDeliveryRecord(notificationId: string, type: string): Promise<DeliveryStatus> {
    return prisma.deliveryStatus.create({
      data: {
        notificationId,
        type,
        status: 'pending',
        attempts: 0,
      },
    });
  }

  async markDelivered(deliveryId: string): Promise<DeliveryStatus> {
    return prisma.deliveryStatus.update({
      where: { id: deliveryId },
      data: {
        status: 'delivered',
        deliveredAt: new Date(),
      },
    });
  }

  async markFailed(deliveryId: string, errorMessage: string): Promise<DeliveryStatus> {
  return prisma.deliveryStatus.update({
      where: { id: deliveryId },
      data: {
        status: 'failed',
        failedAt: new Date(),
        errorMessage,
      },
    });
  }

  async incrementAttempts(deliveryId: string): Promise<DeliveryStatus> {
  const delivery = await prisma.deliveryStatus.findUnique({
      where: { id: deliveryId },
    });

  return prisma.deliveryStatus.update({
      where: { id: deliveryId },
      data: {
        attempts: delivery.attempts + 1,
      },
    });
  }
}
```

```python
# services/delivery_tracking.py
from sqlalchemy import update
from models.delivery_status import DeliveryStatus

class DeliveryTrackingService:
    @staticmethod
    async def create_delivery_record(notification_id: str, type: str) -> DeliveryStatus:
        return await DeliveryStatus.create(
            notification_id=notification_id,
            type=type,
            status='pending',
            attempts=0
        )

    @staticmethod
    async def mark_delivered(delivery_id: str) -> DeliveryStatus:
        return await update(
            DeliveryStatus,
            id=delivery_id,
            updates={
                'status': 'delivered',
                'delivered_at': datetime.now()
            }
        )

    @staticmethod
    async def mark_failed(delivery_id: str, error_message: str) -> DeliveryStatus:
        return await update(
            DeliveryStatus,
            id=delivery_id,
            updates={
                'status': 'failed',
                'failed_at': datetime.now(),
                'error_message': error_message
            }
        )

    @staticmethod
    async def increment_attempts(delivery_id: str) -> DeliveryStatus:
        delivery = await DeliveryStatus.get(delivery_id)
        return await update(
            DeliveryStatus,
            id=delivery_id,
            updates={
                'attempts': delivery.attempts + 1
            }
        )
```

---

## Rate Limiting

### Per-User Rate Limiting

```typescript
// services/rateLimit.service.ts
import { createClient } from 'redis';

const redis = createClient({ url: process.env.REDIS_URL });

export class NotificationRateLimiter {
  async checkRateLimit(userId: string): Promise<boolean> {
    const key = `notification_rate:${userId}`;
    const count = await redis.incr(key);

    // Reset every hour
    await redis.expire(key, 3600); // 1 hour TTL

  // Check if rate limit exceeded
  const limit = 100; // 100 notifications per hour
  if (count > limit) {
      return false;
    }

  return true;
  }

  async decrementCount(userId: string): Promise<void> {
    const key = `notification_rate:${userId}`;
    await redis.decr(key);
  }
}
```

```python
# services/rate_limit_service.py
import redis

redis = redis.Redis(host=os.environ.get('REDIS_HOST', port=6379)

class NotificationRateLimiter:
    @staticmethod
    async def check_rate_limit(user_id: str) -> bool:
        key = f"notification_rate:{user_id}"
        count = redis.incr(key)

        # Reset every hour
        redis.expire(key, 3600)  # 1 hour TTL

        # Check if rate limit exceeded
        limit = 100  # 100 notifications per hour
        if count > limit:
            return False

        return True

    @staticmethod
    async def decrement_count(user_id: str):
        key = f"notification_rate:{user_id}"
        redis.decr(key)
```

### Per-Type Rate Limiting

```typescript
// services/rateLimit.service.ts
export class NotificationRateLimiter {
  async checkRateLimit(userId: string, type: string): Promise<boolean> {
  const key = `notification_rate:${userId}:${type}`;
  const count = await redis.incr(key);

  // Reset every hour
  await redis.expire(key, 3600);

  // Different limits per type
  const limits: Record<string, number> = {
    email: 1000,    // 1000 emails per hour
    sms: 100,       // 100 SMS per hour
    push: 500,       // 500 pushes per hour
  };

  const limit = limits[type] || 100;

  if (count > limit) {
    return false;
  }

  return true;
  }
}
```

---

## Testing

### Unit Tests

```typescript
// tests/notificationQueue.test.ts
import { NotificationQueue } from '../services/notificationQueue.service';

describe('NotificationQueue', () => {
  it('should enqueue and dequeue notification', async () => {
    const notification = { type: 'email', to: 'test@example.com', subject: 'Test', html: '<p>Test</p>' };

    await NotificationQueue.enqueue(notification);
    const dequeued = await NotificationQueue.dequeue();

    expect(dequeued).toEqual(notification);
  });

  it('should return null when queue is empty', async () => {
    const dequeued = await NotificationQueue.dequeue();

    expect(dequeued).toBeNull();
  });
});
```

### Integration Tests

```typescript
// tests/emailService.test.ts
import { EmailService } from '../services/emailService';
import { EmailService as MockedEmailService } from '../__mocks__/EmailService';

describe('EmailService', () => {
  let emailService: MockedEmailService;

  beforeEach(() => {
    emailService = new MockedEmailService();
  });

  it('should send welcome email', async () => {
    await emailService.sendWelcomeEmail('test@example.com', 'Test User');
    expect(emailService.sendWelcomeEmail).toHaveBeenCalled();
  });

  it('should send password reset email', async () => {
    await emailService.sendPasswordResetEmail('test@example.com', 'reset-token-123');

    expect(emailService.sendPasswordResetEmail).toHaveBeenCalledWith(
      'test@example.com',
      'reset-token-123'
    );
  });
});
```

---

## Best Practices

### 1. Use Templates

```typescript
// Use email templates for consistent formatting
const email = emailTemplates.welcome('John Doe');
```

### 2. Use Queues for Delivery

```typescript
// Use queues for async delivery
await NotificationQueue.enqueue(notification);
```

### 3. Track Delivery Status

```typescript
// Track delivery status for monitoring
await DeliveryTrackingService.markDelivered(deliveryId);
```

### 4. Implement Retry Logic

```typescript
// Implement retry with exponential backoff
await withRetry(() => sendEmail(...), 3);
```

### 5. Respect User Preferences

```typescript
// Check user preferences before sending
const preferences = await getPreferences(userId);
if (preferences.emailEnabled) {
  await sendEmail(...);
}
```

### 6. Use Idempotent Operations

```typescript
// Ensure notifications are idempotent
await sendEmail(email); // Should handle duplicate sends
```

### 7. Monitor Queue Length

```typescript
// Monitor queue for backlog
const queueLength = await NotificationQueue.getQueueLength();
if (queueLength > 10000) {
  alert('Notification queue backlog is high');
}
```

### 8. Handle Errors Gracefully

```typescript
// Handle errors and retry
try {
  await sendNotification(notification);
} catch (error) {
  console.error('Failed to send notification:', error);
  await NotificationQueue.enqueue(notification); // Requeue for retry
}
```

### 9. Use Structured Logging

```typescript
// Use structured logging for debugging
logger.info('Sending notification', { notificationId, type, userId });
```

### 10. Test Notifications

```typescript
// Test notification delivery
describe('Notification Delivery', () => {
  it('should deliver email successfully', async () => {
    const notification = { type: 'email', to: 'test@example.com', subject: 'Test', html: '<p>Test</p>' };

    const deliveryId = await DeliveryTrackingService.createDeliveryRecord('1', 'email');
    await EmailService.sendEmail('test@example.com', 'Test', '<p>Test</p>');
    await DeliveryTrackingService.markDelivered(deliveryId);

    const delivery = await DeliveryTrackingService.getDeliveryStatus(deliveryId);
    expect(delivery.status).toBe('delivered');
  });
});
```

---

## Resources

- [SendGrid Documentation](https://docs.sendgrid.com/)
- [Twilio Documentation](https://www.twilio.com/docs/)
- [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging/)
- [Redis Queues](https://redis.io/docs/manual/patterns/)
- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)
