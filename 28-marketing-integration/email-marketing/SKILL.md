---
name: Email Marketing Integration
description: Connecting your application with email service providers for transactional emails, marketing campaigns, and customer communications using SendGrid, Mailchimp, AWS SES, and best practices.
---

# Email Marketing Integration

> **Current Level:** Intermediate  
> **Domain:** Marketing / Communication

---

## Overview

Email marketing integration covers connecting your application with email service providers for transactional emails, marketing campaigns, and customer communications. Effective email integration handles deliverability, templates, tracking, compliance, and automation.

## Table of Contents

1. [Email Marketing Platforms Comparison](#email-marketing-platforms-comparison)
2. [SendGrid Integration](#sendgrid-integration)
3. [Mailchimp Integration](#mailchimp-integration)
4. [AWS SES Setup](#aws-ses-setup)
5. [Email Templates](#email-templates)
6. [Email Validation](#email-validation)
7. [Unsubscribe Handling](#unsubscribe-handling)
8. [Deliverability Best Practices](#deliverability-best-practices)
9. [Analytics and Tracking](#analytics-and-tracking)
10. [Compliance](#compliance)
11. [Testing Emails](#testing-emails)
12. [Production Patterns](#production-patterns)

---

## Email Marketing Platforms Comparison

| Platform | Best For | Pricing | Features |
|----------|----------|---------|----------|
| **SendGrid** | Transactional + Marketing | Free tier, then pay-as-you-go | Excellent API, templates, analytics |
| **Mailchimp** | Marketing campaigns | Free tier, tiered pricing | Easy UI, automation, segmentation |
| **AWS SES** | High volume, cost-sensitive | Pay-per-use ($0.10/1000 emails) | Lowest cost, AWS integration |
| **Postmark** | Transactional emails | Monthly subscription | Great deliverability, simple API |
| **Mailgun** | Developers | Pay-as-you-go | Powerful API, webhooks |

---

## SendGrid Integration

### API Setup

```typescript
// npm install @sendgrid/mail
import sgMail from '@sendgrid/mail';

// Initialize with API key
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

// TypeScript interfaces
interface SendGridEmail {
  to: string | string[];
  from: string;
  subject: string;
  text?: string;
  html?: string;
  templateId?: string;
  dynamicTemplateData?: Record<string, any>;
  attachments?: Array<{
    content: string;
    filename: string;
    type?: string;
    disposition?: string;
  }>;
  categories?: string[];
  customArgs?: Record<string, any>;
}

// Basic send function
async function sendEmail(email: SendGridEmail): Promise<void> {
  try {
    await sgMail.send(email);
    console.log('Email sent successfully');
  } catch (error) {
    console.error('Error sending email:', error);
    throw error;
  }
}
```

### Transactional Emails

```typescript
// Welcome email
async function sendWelcomeEmail(userEmail: string, userName: string): Promise<void> {
  await sendEmail({
    to: userEmail,
    from: 'welcome@yourapp.com',
    subject: 'Welcome to YourApp!',
    templateId: 'd-xxxxxxxxxxxxx', // SendGrid template ID
    dynamicTemplateData: {
      userName,
      loginUrl: 'https://yourapp.com/login',
    },
    categories: ['welcome', 'transactional'],
  });
}

// Password reset
async function sendPasswordReset(
  userEmail: string,
  resetToken: string
): Promise<void> {
  const resetUrl = `https://yourapp.com/reset-password?token=${resetToken}`;
  
  await sendEmail({
    to: userEmail,
    from: 'noreply@yourapp.com',
    subject: 'Reset Your Password',
    templateId: 'd-xxxxxxxxxxxxx',
    dynamicTemplateData: {
      resetUrl,
      expiryHours: 24,
    },
    categories: ['password-reset', 'transactional'],
  });
}

// Order confirmation
async function sendOrderConfirmation(
  userEmail: string,
  orderId: string,
  orderDetails: any
): Promise<void> {
  await sendEmail({
    to: userEmail,
    from: 'orders@yourapp.com',
    subject: `Order Confirmation #${orderId}`,
    templateId: 'd-xxxxxxxxxxxxx',
    dynamicTemplateData: {
      orderId,
      orderDate: new Date().toLocaleDateString(),
      items: orderDetails.items,
      total: orderDetails.total,
      trackingUrl: `https://yourapp.com/orders/${orderId}`,
    },
    categories: ['order-confirmation', 'transactional'],
    customArgs: {
      orderId,
      userId: orderDetails.userId,
    },
  });
}
```

### Marketing Campaigns

```typescript
// Add contact to list
import sgClient from '@sendgrid/client';

sgClient.setApiKey(process.env.SENDGRID_API_KEY);

interface Contact {
  email: string;
  firstName?: string;
  lastName?: string;
  customFields?: Record<string, any>;
}

async function addContactToList(
  contact: Contact,
  listId: string
): Promise<void> {
  const data = {
    list_ids: [listId],
    contacts: [
      {
        email: contact.email,
        first_name: contact.firstName,
        last_name: contact.lastName,
        ...contact.customFields,
      },
    ],
  };

  await sgClient.request({
    method: 'PUT',
    url: '/v3/marketing/contacts',
    body: data,
  });
}

// Create campaign
async function createCampaign(params: {
  name: string;
  subject: string;
  senderId: string;
  listIds: string[];
  htmlContent: string;
  plainContent: string;
}): Promise<string> {
  const campaign = {
    name: params.name,
    subject: params.subject,
    sender_id: params.senderId,
    list_ids: params.listIds,
    html_content: params.htmlContent,
    plain_content: params.plainContent,
    custom_unsubscribe_url: 'https://yourapp.com/unsubscribe',
  };

  const response = await sgClient.request({
    method: 'POST',
    url: '/v3/marketing/campaigns',
    body: campaign,
  });

  return response.body.id;
}

// Schedule campaign
async function scheduleCampaign(
  campaignId: string,
  sendAt: Date
): Promise<void> {
  await sgClient.request({
    method: 'POST',
    url: `/v3/marketing/campaigns/${campaignId}/schedules`,
    body: {
      send_at: sendAt.toISOString(),
    },
  });
}

// Send campaign immediately
async function sendCampaign(campaignId: string): Promise<void> {
  await sgClient.request({
    method: 'POST',
    url: `/v3/marketing/campaigns/${campaignId}/actions/send`,
  });
}
```

### Template Management

```typescript
// Create template
async function createTemplate(name: string): Promise<string> {
  const response = await sgClient.request({
    method: 'POST',
    url: '/v3/templates',
    body: {
      name,
      generation: 'dynamic', // Use dynamic templates
    },
  });

  return response.body.id;
}

// Create template version
async function createTemplateVersion(params: {
  templateId: string;
  name: string;
  subject: string;
  htmlContent: string;
  plainContent?: string;
  active?: boolean;
}): Promise<void> {
  await sgClient.request({
    method: 'POST',
    url: `/v3/templates/${params.templateId}/versions`,
    body: {
      name: params.name,
      subject: params.subject,
      html_content: params.htmlContent,
      plain_content: params.plainContent,
      active: params.active ?? true,
    },
  });
}

// List templates
async function listTemplates(): Promise<any[]> {
  const response = await sgClient.request({
    method: 'GET',
    url: '/v3/templates?generations=dynamic',
  });

  return response.body.results;
}

// Update template
async function updateTemplate(
  templateId: string,
  name: string
): Promise<void> {
  await sgClient.request({
    method: 'PATCH',
    url: `/v3/templates/${templateId}`,
    body: { name },
  });
}
```

### Webhooks (Opens, Clicks, Bounces)

```typescript
import express from 'express';

const app = express();

// Verify SendGrid webhook signature
function verifyWebhookSignature(
  payload: string,
  signature: string,
  timestamp: string
): boolean {
  const crypto = require('crypto');
  const publicKey = process.env.SENDGRID_WEBHOOK_PUBLIC_KEY;
  const decodedSignature = Buffer.from(signature, 'base64').toString();
  const expectedSignature = crypto
    .createHmac('sha256', publicKey)
    .update(timestamp + payload)
    .digest('base64');

  return decodedSignature === expectedSignature;
}

// Webhook handler
app.post('/webhooks/sendgrid', express.raw({ type: 'application/json' }), (req, res) => {
  const signature = req.headers['x-twilio-email-event-webhook-signature'] as string;
  const timestamp = req.headers['x-twilio-email-event-webhook-timestamp'] as string;
  const payload = req.body.toString();

  // Verify signature
  if (!verifyWebhookSignature(payload, signature, timestamp)) {
    return res.status(403).json({ error: 'Invalid signature' });
  }

  const events = JSON.parse(payload);

  events.forEach(async (event: any) => {
    switch (event.event) {
      case 'open':
        await handleEmailOpen(event);
        break;
      case 'click':
        await handleEmailClick(event);
        break;
      case 'bounce':
        await handleEmailBounce(event);
        break;
      case 'delivered':
        await handleEmailDelivered(event);
        break;
      case 'spamreport':
        await handleSpamReport(event);
        break;
      case 'unsubscribe':
        await handleUnsubscribe(event);
        break;
    }
  });

  res.status(200).json({ received: true });
});

async function handleEmailOpen(event: any): Promise<void> {
  // Track email open
  console.log('Email opened:', {
    email: event.email,
    messageId: event.sg_message_id,
    timestamp: event.timestamp,
    customArgs: event.custom_args,
  });
}

async function handleEmailClick(event: any): Promise<void> {
  // Track link click
  console.log('Link clicked:', {
    email: event.email,
    url: event.url,
    messageId: event.sg_message_id,
    timestamp: event.timestamp,
  });
}

async function handleEmailBounce(event: any): Promise<void> {
  // Handle bounced email
  console.log('Email bounced:', {
    email: event.email,
    reason: event.reason,
    type: event.bounce_type,
    timestamp: event.timestamp,
  });

  // Mark email as invalid in database
  await markEmailAsInvalid(event.email, event.reason);
}

async function handleSpamReport(event: any): Promise<void> {
  // Handle spam report
  console.log('Spam reported:', {
    email: event.email,
    timestamp: event.timestamp,
  });

  // Unsubscribe user immediately
  await unsubscribeUser(event.email);
}
```

---

## Mailchimp Integration

### List Management

```typescript
// npm install @mailchimp/mailchimp_marketing
import mailchimp from '@mailchimp/mailchimp_marketing';

mailchimp.setConfig({
  apiKey: process.env.MAILCHIMP_API_KEY,
  server: process.env.MAILCHIMP_SERVER_PREFIX, // e.g., 'us1'
});

// Add subscriber to list
async function addSubscriber(params: {
  listId: string;
  email: string;
  firstName?: string;
  lastName?: string;
  tags?: string[];
  mergeFields?: Record<string, any>;
}): Promise<void> {
  await mailchimp.lists.addListMember(params.listId, {
    email_address: params.email,
    status: 'subscribed',
    merge_fields: {
      FNAME: params.firstName,
      LNAME: params.lastName,
      ...params.mergeFields,
    },
    tags: params.tags,
  });
}

// Update subscriber
async function updateSubscriber(
  listId: string,
  subscriberHash: string,
  data: any
): Promise<void> {
  await mailchimp.lists.updateListMember(listId, subscriberHash, data);
}

// Get subscriber
async function getSubscriber(
  listId: string,
  email: string
): Promise<any> {
  const subscriberHash = Buffer.from(email.toLowerCase()).toString('base64');
  return await mailchimp.lists.getListMember(listId, subscriberHash);
}

// Batch add subscribers
async function batchAddSubscribers(
  listId: string,
  subscribers: Array<{
    email: string;
    firstName?: string;
    lastName?: string;
  }>
): Promise<void> {
  const members = subscribers.map((sub) => ({
    email_address: sub.email,
    status: 'subscribed',
    merge_fields: {
      FNAME: sub.firstName,
      LNAME: sub.lastName,
    },
  }));

  await mailchimp.lists.batchListMembers(listId, { members, update_existing: true });
}

// Create list
async function createList(params: {
  name: string;
  fromName: string;
  replyTo: string;
  permissionReminder: string;
  campaignDefaults: {
    fromName: string;
    fromEmail: string;
    subject: string;
    language: string;
  };
}): Promise<string> {
  const response = await mailchimp.lists.createList({
    name: params.name,
    contact: {
      company: 'Your Company',
      address1: '123 Main St',
      city: 'City',
      state: 'State',
      zip: '12345',
      country: 'US',
    },
    permission_reminder: params.permissionReminder,
    campaign_defaults: params.campaignDefaults,
    email_type_option: true,
  });

  return response.id;
}
```

### Campaign Creation

```typescript
// Create campaign
async function createCampaign(params: {
  type: 'regular' | 'plaintext' | 'absplit' | 'rss' | 'variate';
  listId: string;
  subject: string;
  fromName: string;
  replyTo: string;
  htmlContent?: string;
}): Promise<string> {
  const campaign = await mailchimp.campaigns.create({
    type: params.type,
    recipients: { list_id: params.listId },
    settings: {
      subject_line: params.subject,
      from_name: params.fromName,
      reply_to: params.replyTo,
      title: `${params.subject} - ${new Date().toISOString()}`,
    },
  });

  // Set content if provided
  if (params.htmlContent) {
    await mailchimp.campaigns.setContent(campaign.id, {
      html: params.htmlContent,
    });
  }

  return campaign.id;
}

// Send campaign
async function sendCampaign(campaignId: string): Promise<void> {
  await mailchimp.campaigns.send(campaignId);
}

// Schedule campaign
async function scheduleCampaign(
  campaignId: string,
  scheduleTime: Date
): Promise<void> {
  await mailchimp.campaigns.schedule(campaignId, {
    schedule_time: scheduleTime.toISOString(),
  });
}

// Test campaign
async function testCampaign(
  campaignId: string,
  testEmails: string[],
  testType: 'html' | 'text' = 'html'
): Promise<void> {
  await mailchimp.campaigns.sendTest(campaignId, {
    test_emails: testEmails,
    send_type: testType,
  });
}
```

### Automation Workflows

```typescript
// Create automation workflow
async function createAutomation(params: {
  workflowId: string;
  fromEmail: string;
  fromName: string;
  replyTo: string;
  listId: string;
}): Promise<void> {
  await mailchimp.automations.addWorkflow(params.workflowId, {
    from_email: params.fromEmail,
    from_name: params.fromName,
    reply_to: params.replyTo,
    recipients: {
      list_id: params.listId,
    },
  });
}

// Add email to workflow
async function addWorkflowEmail(
  workflowId: string,
  stepId: string,
  email: {
    subject: string;
    htmlContent: string;
    plainContent?: string;
  }
): Promise<void> {
  await mailchimp.automations.addEmail(workflowId, stepId, {
    settings: {
      subject_line: email.subject,
      title: email.subject,
      from_name: 'Your Company',
      reply_to: 'noreply@yourapp.com',
    },
    content: {
      html: email.htmlContent,
      plain: email.plainContent,
    },
  });
}

// Start automation
async function startAutomation(workflowId: string): Promise<void> {
  await mailchimp.automations.start(workflowId);
}

// Pause automation
async function pauseAutomation(workflowId: string): Promise<void> {
  await mailchimp.automations.pause(workflowId);
}

// Remove subscriber from all automations
async function removeSubscriberFromAutomations(
  listId: string,
  email: string
): Promise<void> {
  const subscriberHash = Buffer.from(email.toLowerCase()).toString('base64');
  await mailchimp.automations.removeSubscriberFromWorkflow(listId, subscriberHash);
}
```

### Segmentation

```typescript
// Create segment
async function createSegment(params: {
  listId: string;
  name: string;
  conditions: Array<{
    field: string;
    op: string;
    value: string;
  }>;
}): Promise<string> {
  const segment = await mailchimp.lists.createSegment(params.listId, {
    name: params.name,
    static_segment: [],
    options: {
      match: 'all',
      conditions: params.conditions,
    },
  });

  return segment.id;
}

// Example: Active users segment
async function createActiveUsersSegment(listId: string): Promise<string> {
  return await createSegment({
    listId,
    name: 'Active Users (Last 30 Days)',
    conditions: [
      {
        field: 'last_active',
        op: 'after',
        value: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
      },
    ],
  });
}

// Example: Purchased users segment
async function createPurchasedUsersSegment(listId: string): Promise<string> {
  return await createSegment({
    listId,
    name: 'Purchased Users',
    conditions: [
      {
        field: 'purchase_count',
        op: 'gt',
        value: '0',
      },
    ],
  });
}

// Get segment members
async function getSegmentMembers(
  listId: string,
  segmentId: string
): Promise<any[]> {
  const response = await mailchimp.lists.segmentMembers(listId, segmentId);
  return response.members;
}
```

---

## AWS SES Setup

### Configuration

```typescript
// npm install @aws-sdk/client-ses
import { SESClient, SendEmailCommand } from '@aws-sdk/client-ses';

// Initialize SES client
const sesClient = new SESClient({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    accessSecretKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
});

// Send email with SES
async function sendSESEmail(params: {
  to: string | string[];
  from: string;
  subject: string;
  html?: string;
  text?: string;
  replyTo?: string;
}): Promise<string> {
  const command = new SendEmailCommand({
    Source: params.from,
    Destination: {
      ToAddresses: Array.isArray(params.to) ? params.to : [params.to],
    },
    ReplyToAddresses: params.replyTo ? [params.replyTo] : undefined,
    Message: {
      Subject: {
        Data: params.subject,
        Charset: 'UTF-8',
      },
      Body: {
        Text: params.text
          ? {
              Data: params.text,
              Charset: 'UTF-8',
            }
          : undefined,
        Html: params.html
          ? {
              Data: params.html,
              Charset: 'UTF-8',
            }
          : undefined,
      },
    },
  });

  const response = await sesClient.send(command);
  return response.MessageId;
}

// Send templated email with SES
import { SendTemplatedEmailCommand } from '@aws-sdk/client-ses';

async function sendSESTemplateEmail(params: {
  to: string | string[];
  from: string;
  templateName: string;
  templateData: Record<string, any>;
}): Promise<string> {
  const command = new SendTemplatedEmailCommand({
    Source: params.from,
    Destination: {
      ToAddresses: Array.isArray(params.to) ? params.to : [params.to],
    },
    Template: params.templateName,
    TemplateData: JSON.stringify(params.templateData),
  });

  const response = await sesClient.send(command);
  return response.MessageId;
}
```

### Sending Bulk Emails

```typescript
import { SendBulkEmailCommand } from '@aws-sdk/client-sesv2';
import { SESv2Client } from '@aws-sdk/client-sesv2';

const sesV2Client = new SESv2Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    accessSecretKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
});

interface BulkEmailParams {
  from: string;
  templateName: string;
  defaultTemplateData: Record<string, any>;
  recipients: Array<{
    to: string;
    templateData: Record<string, any>;
  }>;
}

async function sendBulkEmail(params: BulkEmailParams): Promise<void> {
  const command = new SendBulkEmailCommand({
    FromEmailAddress: params.from,
    DefaultContent: {
      Template: {
        TemplateName: params.templateName,
        TemplateData: JSON.stringify(params.defaultTemplateData),
      },
    },
    BulkEmailEntries: params.recipients.map((recipient) => ({
      Destination: {
        ToAddresses: [recipient.to],
      },
      ReplacementEmailContent: {
        ReplacementTemplate: {
          ReplacementTemplateData: JSON.stringify(recipient.templateData),
        },
      },
    })),
  });

  await sesV2Client.send(command);
}
```

### SES Configuration Sets

```typescript
// Create configuration set
import { CreateConfigurationSetCommand } from '@aws-sdk/client-ses';

async function createConfigurationSet(name: string): Promise<void> {
  const command = new CreateConfigurationSetCommand({
    ConfigurationSet: {
      Name: name,
      SendingEnabled: true,
      ReputationOptions: {
        ReputationMetricsEnabled: true,
        LastFreshStart: new Date(),
      },
      DeliveryOptions: {
        SendingPoolName: 'Transactional',
      },
      TrackingOptions: {
        CustomRedirectDomain: 'email.yourapp.com',
      },
    },
  });

  await sesClient.send(command);
}

// Send email with configuration set
async function sendWithConfigurationSet(params: {
  to: string;
  from: string;
  subject: string;
  html: string;
  configurationSetName: string;
}): Promise<string> {
  const command = new SendEmailCommand({
    Source: params.from,
    Destination: { ToAddresses: [params.to] },
    ConfigurationSetName: params.configurationSetName,
    Message: {
      Subject: { Data: params.subject, Charset: 'UTF-8' },
      Body: {
        Html: { Data: params.html, Charset: 'UTF-8' },
      },
    },
  });

  const response = await sesClient.send(command);
  return response.MessageId;
}
```

---

## Email Templates

### HTML Templates

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{subject}}</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      color: #333;
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
    }
    .header {
      background: #007bff;
      color: white;
      padding: 20px;
      text-align: center;
    }
    .content {
      padding: 20px;
      background: #f9f9f9;
    }
    .button {
      display: inline-block;
      padding: 12px 24px;
      background: #007bff;
      color: white;
      text-decoration: none;
      border-radius: 4px;
      margin: 20px 0;
    }
    .footer {
      text-align: center;
      padding: 20px;
      font-size: 12px;
      color: #666;
    }
  </style>
</head>
<body>
  <div class="header">
    <h1>{{companyName}}</h1>
  </div>
  <div class="content">
    <h2>{{greeting}}</h2>
    <p>{{message}}</p>
    <a href="{{ctaUrl}}" class="button">{{ctaText}}</a>
  </div>
  <div class="footer">
    <p>© {{year}} {{companyName}}. All rights reserved.</p>
    <p>
      <a href="{{unsubscribeUrl}}">Unsubscribe</a> |
      <a href="{{privacyUrl}}">Privacy Policy</a>
    </p>
  </div>
</body>
</html>
```

### Dynamic Content with Handlebars

```typescript
// npm install handlebars
import Handlebars from 'handlebars';

// Register custom helpers
Handlebars.registerHelper('eq', (a: any, b: any) => a === b);
Handlebars.registerHelper('formatDate', (date: Date) => 
  new Date(date).toLocaleDateString()
);
Handlebars.registerHelper('formatCurrency', (amount: number) => 
  `$${amount.toFixed(2)}`
);

// Compile template
const templateSource = `
<div class="order-summary">
  <h2>Order #{{orderId}}</h2>
  <p>Order Date: {{formatDate orderDate}}</p>
  
  <table>
    <thead>
      <tr>
        <th>Product</th>
        <th>Quantity</th>
        <th>Price</th>
      </tr>
    </thead>
    <tbody>
      {{#each items}}
      <tr>
        <td>{{name}}</td>
        <td>{{quantity}}</td>
        <td>{{formatCurrency price}}</td>
      </tr>
      {{/each}}
    </tbody>
  </table>
  
  <p class="total">Total: {{formatCurrency total}}</p>
  
  {{#if shippingAddress}}
  <div class="shipping">
    <h3>Shipping Address</h3>
    <p>{{shippingAddress.name}}</p>
    <p>{{shippingAddress.line1}}</p>
    <p>{{shippingAddress.city}}, {{shippingAddress.state}} {{shippingAddress.zip}}</p>
  </div>
  {{/if}}
</div>
`;

const template = Handlebars.compile(templateSource);

// Render with data
function renderOrderEmail(orderData: any): string {
  return template(orderData);
}

// Usage
const html = renderOrderEmail({
  orderId: 'ORD-12345',
  orderDate: new Date(),
  items: [
    { name: 'Product A', quantity: 2, price: 29.99 },
    { name: 'Product B', quantity: 1, price: 49.99 },
  ],
  total: 109.97,
  shippingAddress: {
    name: 'John Doe',
    line1: '123 Main St',
    city: 'New York',
    state: 'NY',
    zip: '10001',
  },
});
```

### MJML Templates

```bash
npm install mjml
```

```mjml
<mjml>
  <mj-head>
    <mj-title>{{subject}}</mj-title>
    <mj-preview>{{previewText}}</mj-preview>
    <mj-font name="Roboto" href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap" />
    <mj-attributes>
      <mj-all font-family="Roboto, Arial, sans-serif" />
      <mj-section background-color="#ffffff" />
      <mj-column padding="0" />
    </mj-attributes>
  </mj-head>
  <mj-body background-color="#f4f4f4">
    <mj-section background-color="#007bff" padding="20px">
      <mj-column>
        <mj-text align="center" color="#ffffff" font-size="24px" font-weight="bold">
          {{companyName}}
        </mj-text>
      </mj-column>
    </mj-section>
    
    <mj-section padding="40px 20px">
      <mj-column>
        <mj-text font-size="18px" color="#333333">
          {{greeting}},
        </mj-text>
        <mj-text font-size="16px" color="#555555" padding="10px 0">
          {{message}}
        </mj-text>
        
        <mj-button href="{{ctaUrl}}" background-color="#007bff" color="#ffffff" padding="15px 30px" border-radius="4px">
          {{ctaText}}
        </mj-button>
      </mj-column>
    </mj-section>
    
    <mj-section background-color="#f9f9f9" padding="20px">
      <mj-column>
        {{#each items}}
        <mj-text>{{this}}</mj-text>
        {{/each}}
      </mj-column>
    </mj-section>
    
    <mj-section background-color="#333333" padding="20px">
      <mj-column>
        <mj-text align="center" color="#ffffff" font-size="12px">
          © {{year}} {{companyName}}. All rights reserved.
        </mj-text>
        <mj-text align="center" color="#cccccc" font-size="12px" padding="10px 0">
          <a href="{{unsubscribeUrl}}" style="color: #cccccc; text-decoration: underline;">Unsubscribe</a>
        </mj-text>
      </mj-column>
    </mj-section>
  </mj-body>
</mjml>
```

```typescript
import mjml2html from 'mjml';

function renderMJML(mjmlTemplate: string, data: Record<string, any>): string {
  // First, replace Handlebars variables
  const compiledTemplate = Handlebars.compile(mjmlTemplate);
  const renderedMJML = compiledTemplate(data);
  
  // Convert MJML to HTML
  const { html } = mjml2html(renderedMJML);
  return html;
}
```

---

## Email Validation

### Basic Validation

```typescript
// Simple regex validation
function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// More comprehensive validation
function validateEmail(email: string): {
  valid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  if (!email) {
    errors.push('Email is required');
    return { valid: false, errors };
  }

  if (!isValidEmail(email)) {
    errors.push('Invalid email format');
  }

  if (email.length > 254) {
    errors.push('Email is too long');
  }

  const [localPart, domain] = email.split('@');
  if (localPart.length > 64) {
    errors.push('Local part is too long');
  }

  if (domain && domain.length > 255) {
    errors.push('Domain is too long');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
```

### Advanced Validation with Third-Party Services

```typescript
// Using ZeroBounce API
async function validateEmailWithZeroBounce(email: string): Promise<{
  valid: boolean;
  status: string;
  subStatus?: string;
  freeEmail?: boolean;
  didYouMean?: string;
}> {
  const response = await fetch(
    `https://api.zerobounce.net/v2/validate?api_key=${process.env.ZEROBOUNCE_API_KEY}&email=${encodeURIComponent(email)}`
  );

  const data = await response.json();

  return {
    valid: data.status === 'valid',
    status: data.status,
    subStatus: data.sub_status,
    freeEmail: data.free_email,
    didYouMean: data.did_you_mean,
  };
}

// Using NeverBounce API
async function validateEmailWithNeverBounce(email: string): Promise<{
  valid: boolean;
  result: string;
  flags: string[];
  didYouMean?: string;
}> {
  const response = await fetch('https://api.neverbounce.com/v4/single/check', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${process.env.NEVERBOUNCE_API_KEY}`,
    },
    body: JSON.stringify({ email }),
  });

  const data = await response.json();

  return {
    valid: data.result === 'valid',
    result: data.result,
    flags: data.flags,
    didYouMean: data.suggested_correction,
  };
}

// Using Hunter.io API
async function verifyEmailWithHunter(email: string): Promise<{
  valid: boolean;
  status: string;
  score: number;
  regex: boolean;
  disposable: boolean;
  webmail: boolean;
}> {
  const response = await fetch(
    `https://api.hunter.io/v2/email-verifier?email=${encodeURIComponent(email)}&api_key=${process.env.HUNTER_API_KEY}`
  );

  const data = await response.json();

  return {
    valid: data.data.status === 'valid',
    status: data.data.status,
    score: data.data.score,
    regex: data.data.regex,
    disposable: data.data.disposable,
    webmail: data.data.webmail,
  };
}
```

### Disposable Email Detection

```typescript
// List of disposable email domains (expand as needed)
const DISPOSABLE_DOMAINS = new Set([
  'tempmail.com',
  'guerrillamail.com',
  'mailinator.com',
  '10minutemail.com',
  'yopmail.com',
  'trashmail.com',
  // Add more...
]);

function isDisposableEmail(email: string): boolean {
  const domain = email.split('@')[1]?.toLowerCase();
  return DISPOSABLE_DOMAINS.has(domain);
}

// Check against online database
async function checkDisposableEmail(email: string): Promise<boolean> {
  const domain = email.split('@')[1]?.toLowerCase();
  
  const response = await fetch(
    `https://open.kickbox.com/v1/disposable/${domain}`
  );

  const data = await response.json();
  return data.disposable;
}
```

---

## Unsubscribe Handling

### One-Click Unsubscribe

```typescript
// Generate one-click unsubscribe URL
function generateUnsubscribeUrl(email: string, campaignId?: string): string {
  const token = Buffer.from(
    JSON.stringify({ email, campaignId, timestamp: Date.now() })
  ).toString('base64');

  const signature = crypto
    .createHmac('sha256', process.env.UNSUBSCRIBE_SECRET!)
    .update(token)
    .digest('hex');

  return `https://yourapp.com/unsubscribe?token=${token}&sig=${signature}`;
}

// Verify unsubscribe token
function verifyUnsubscribeToken(
  token: string,
  signature: string
): { email: string; campaignId?: string } | null {
  const expectedSignature = crypto
    .createHmac('sha256', process.env.UNSUBSCRIBE_SECRET!)
    .update(token)
    .digest('hex');

  if (signature !== expectedSignature) {
    return null;
  }

  try {
    const data = JSON.parse(Buffer.from(token, 'base64').toString());
    
    // Check token expiry (7 days)
    if (Date.now() - data.timestamp > 7 * 24 * 60 * 60 * 1000) {
      return null;
    }

    return { email: data.email, campaignId: data.campaignId };
  } catch {
    return null;
  }
}

// Unsubscribe handler
import express from 'express';

app.get('/unsubscribe', async (req, res) => {
  const { token, sig } = req.query;

  if (!token || !sig) {
    return res.status(400).send('Invalid unsubscribe link');
  }

  const data = verifyUnsubscribeToken(token as string, sig as string);
  if (!data) {
    return res.status(400).send('Invalid or expired unsubscribe link');
  }

  // Unsubscribe user
  await unsubscribeUser(data.email);

  // Render confirmation page
  res.send(`
    <h1>You have been unsubscribed</h1>
    <p>You will no longer receive emails from us.</p>
  `);
});
```

### List-Unsubscribe Header

```typescript
// Add List-Unsubscribe header to emails
function addUnsubscribeHeaders(email: SendGridEmail): SendGridEmail {
  const unsubscribeUrl = generateUnsubscribeUrl(
    Array.isArray(email.to) ? email.to[0] : email.to
  );

  return {
    ...email,
    customArgs: {
      ...email.customArgs,
      unsubscribe_url: unsubscribeUrl,
    },
    headers: {
      'List-Unsubscribe': `<${unsubscribeUrl}>`,
      'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click',
    },
  };
}
```

---

## Deliverability Best Practices

### SPF, DKIM, and DMARC

```typescript
// DNS configuration guide

/**
 * SPF (Sender Policy Framework)
 * Add TXT record to your domain:
 * 
 * v=spf1 include:sendgrid.net -all
 * 
 * For multiple providers:
 * v=spf1 include:sendgrid.net include:_spf.google.com ~all
 */

/**
 * DKIM (DomainKeys Identified Mail)
 * 
 * SendGrid will provide DKIM records to add:
 * 
 * Name: smtpapi._domainkey
 * Type: TXT
 * Value: k=rsa; p=<public-key>
 */

/**
 * DMARC (Domain-based Message Authentication, Reporting, and Conformance)
 * Add TXT record:
 * 
 * _dmarc.yourdomain.com
 * Type: TXT
 * Value: v=DMARC1; p=quarantine; rua=mailto:dmarc@yourdomain.com; ruf=mailto:dmarc@yourdomain.com
 * 
 * Options:
 * p=none    - Monitor only
 * p=quarantine - Move to spam
 * p=reject  - Reject emails
 */
```

### Warming Up IP Addresses

```typescript
// Gradual increase in email volume
const WARMUP_SCHEDULE = [
  { day: 1, emails: 50 },
  { day: 2, emails: 100 },
  { day: 3, emails: 200 },
  { day: 4, emails: 400 },
  { day: 5, emails: 800 },
  { day: 6, emails: 1500 },
  { day: 7, emails: 3000 },
  { day: 8, emails: 5000 },
  { day: 9, emails: 8000 },
  { day: 10, emails: 12000 },
  { day: 11, emails: 18000 },
  { day: 12, emails: 25000 },
  { day: 13, emails: 35000 },
  { day: 14, emails: 50000 },
];

async function warmupIP(dedicatedIP: string): Promise<void> {
  for (const schedule of WARMUP_SCHEDULE) {
    console.log(`Day ${schedule.day}: Sending ${schedule.emails} emails`);
    
    // Send to engaged subscribers first
    const recipients = await getEngagedRecipients(schedule.emails);
    
    await sendBatch({
      to: recipients,
      from: 'welcome@yourapp.com',
      subject: 'Welcome to our newsletter!',
      templateId: 'd-xxxxxxxxxxxxx',
      customArgs: {
        warmup: 'true',
        ip: dedicatedIP,
      },
    });

    // Wait until next day
    await new Promise((resolve) => setTimeout(resolve, 24 * 60 * 60 * 1000));
  }
}
```

### Content Best Practices

```typescript
// Email content validator
interface EmailContent {
  subject: string;
  html: string;
  text?: string;
}

function validateEmailContent(content: EmailContent): {
  valid: boolean;
  warnings: string[];
} {
  const warnings: string[] = [];

  // Subject line checks
  if (content.subject.length > 78) {
    warnings.push('Subject line is too long (max 78 characters recommended)');
  }

  if (/[A-Z]{5,}/.test(content.subject)) {
    warnings.push('Subject line contains excessive caps');
  }

  if (/[!]{3,}/.test(content.subject)) {
    warnings.push('Subject line contains excessive exclamation marks');
  }

  // Content checks
  if (!content.text && !content.html) {
    warnings.push('Email must have either text or HTML content');
  }

  if (content.html) {
    // Check for spam trigger words
    const spamWords = ['free', 'winner', 'congratulations', 'click here'];
    const htmlLower = content.html.toLowerCase();
    
    const spamCount = spamWords.filter(word => htmlLower.includes(word)).length;
    if (spamCount > 2) {
      warnings.push('Email contains multiple spam trigger words');
    }

    // Check image-to-text ratio
    const imageCount = (content.html.match(/<img/gi) || []).length;
    const textLength = content.html.replace(/<[^>]*>/g, '').length;
    
    if (imageCount > 0 && textLength / imageCount < 100) {
      warnings.push('Low text-to-image ratio may trigger spam filters');
    }
  }

  return {
    valid: warnings.length === 0,
    warnings,
  };
}
```

---

## Analytics and Tracking

### Open and Click Tracking

```typescript
// SendGrid automatically adds tracking when enabled
// Configure tracking settings
async function configureTracking(): Promise<void> {
  await sgClient.request({
    method: 'PATCH',
    url: '/v3/tracking_settings',
    body: {
      open: { enabled: true },
      click: { enabled: true },
    },
  });
}

// Custom tracking parameters
function addTrackingParams(url: string, params: Record<string, string>): string {
  const urlObj = new URL(url);
  Object.entries(params).forEach(([key, value]) => {
    urlObj.searchParams.set(key, value);
  });
  return urlObj.toString();
}

// Usage in email template
const trackedUrl = addTrackingParams('https://yourapp.com/product', {
  utm_source: 'newsletter',
  utm_medium: 'email',
  utm_campaign: 'summer-sale',
  email: userEmail,
});
```

### Analytics Dashboard

```typescript
// Get SendGrid statistics
async function getEmailStats(params: {
  startDate: Date;
  endDate: Date;
  aggregatedBy?: 'day' | 'week' | 'month';
}): Promise<any> {
  const response = await sgClient.request({
    method: 'GET',
    url: '/v3/stats',
    qs: {
      start_date: params.startDate.toISOString().split('T')[0],
      end_date: params.endDate.toISOString().split('T')[0],
      aggregated_by: params.aggregatedBy || 'day',
    },
  });

  return response.body;
}

// Get campaign-specific stats
async function getCampaignStats(campaignId: string): Promise<any> {
  const response = await sgClient.request({
    method: 'GET',
    url: `/v3/campaigns/${campaignId}/stats`,
  });

  return response.body;
}

// Calculate key metrics
interface EmailMetrics {
  sent: number;
  delivered: number;
  opened: number;
  clicked: number;
  bounced: number;
  spamReports: number;
}

function calculateDeliveryRate(metrics: EmailMetrics): number {
  return (metrics.delivered / metrics.sent) * 100;
}

function calculateOpenRate(metrics: EmailMetrics): number {
  return (metrics.opened / metrics.delivered) * 100;
}

function calculateClickRate(metrics: EmailMetrics): number {
  return (metrics.clicked / metrics.delivered) * 100;
}

function calculateBounceRate(metrics: EmailMetrics): number {
  return (metrics.bounced / metrics.sent) * 100;
}

function calculateSpamRate(metrics: EmailMetrics): number {
  return (metrics.spamReports / metrics.sent) * 100;
}
```

---

## Compliance

### CAN-SPAM Compliance

```typescript
// Ensure all emails have required elements
interface CompliantEmail {
  to: string;
  from: string;
  subject: string;
  html: string;
  text?: string;
  // Required for CAN-SPAM
  physicalAddress: {
    street: string;
    city: string;
    state: string;
    zip: string;
    country?: string;
  };
  unsubscribeUrl: string;
}

function validateCANSPAM(email: CompliantEmail): {
  compliant: boolean;
  issues: string[];
} {
  const issues: string[] = [];

  // Check physical address
  if (!email.physicalAddress) {
    issues.push('Physical address is required');
  } else {
    const { street, city, state, zip } = email.physicalAddress;
    if (!street || !city || !state || !zip) {
      issues.push('Complete physical address is required');
    }
  }

  // Check unsubscribe mechanism
  if (!email.unsubscribeUrl) {
    issues.push('Unsubscribe URL is required');
  }

  // Check subject line (must not be misleading)
  if (!email.subject || email.subject.trim() === '') {
    issues.push('Subject line is required');
  }

  // Check that unsubscribe is clearly visible
  if (email.html && !email.html.includes('unsubscribe')) {
    issues.push('Unsubscribe link must be visible in email');
  }

  return {
    compliant: issues.length === 0,
    issues,
  };
}
```

### GDPR Compliance

```typescript
// Consent management
interface UserConsent {
  email: string;
  marketingConsent: boolean;
  consentDate: Date;
  consentMethod: 'checkbox' | 'email' | 'phone';
  ipAddress?: string;
  userAgent?: string;
}

async function recordConsent(consent: UserConsent): Promise<void> {
  await db.userConsent.create({
    data: {
      email: consent.email,
      marketingConsent: consent.marketingConsent,
      consentDate: consent.consentDate,
      consentMethod: consent.consentMethod,
      ipAddress: consent.ipAddress,
      userAgent: consent.userAgent,
    },
  });
}

// Check consent before sending
async function hasMarketingConsent(email: string): Promise<boolean> {
  const consent = await db.userConsent.findUnique({
    where: { email },
  });

  return consent?.marketingConsent ?? false;
}

// Right to be forgotten
async function deleteUserData(email: string): Promise<void> {
  // Remove from all email lists
  await unsubscribeFromAllLists(email);

  // Delete consent records
  await db.userConsent.delete({
    where: { email },
  });

  // Anonymize email in other records
  await db.user.updateMany({
    where: { email },
    data: { email: 'deleted@anonymized.com' },
  });
}
```

---

## Testing Emails

### Local Testing with Mailtrap

```typescript
// Mailtrap configuration
const mailtrapConfig = {
  host: 'sandbox.smtp.mailtrap.io',
  port: 2525,
  auth: {
    user: process.env.MAILTRAP_USER,
    pass: process.env.MAILTRAP_PASSWORD,
  },
};

// Use nodemailer for testing
import nodemailer from 'nodemailer';

async function sendTestEmail(email: any): Promise<void> {
  const transporter = nodemailer.createTransport(mailtrapConfig);

  await transporter.sendMail({
    from: email.from,
    to: email.to,
    subject: email.subject,
    html: email.html,
    text: email.text,
  });
}
```

### Email Preview

```typescript
// Preview email in browser
import express from 'express';

app.get('/preview-email/:templateId', async (req, res) => {
  const { templateId } = req.params;
  
  const template = await getTemplate(templateId);
  const sampleData = getSampleDataForTemplate(templateId);
  
  const html = renderTemplate(template.content, sampleData);
  
  res.send(html);
});

// Send test email
app.post('/send-test-email', async (req, res) => {
  const { templateId, testEmail, customData } = req.body;
  
  const template = await getTemplate(templateId);
  const data = customData || getSampleDataForTemplate(templateId);
  
  const html = renderTemplate(template.content, data);
  
  await sendTestEmail({
    to: testEmail,
    from: 'test@yourapp.com',
    subject: `[TEST] ${template.name}`,
    html,
  });
  
  res.json({ success: true });
});
```

### A/B Testing Subject Lines

```typescript
interface SubjectLineTest {
  campaignId: string;
  subjectLines: string[];
  sampleSize: number;
}

async function runSubjectLineTest(test: SubjectLineTest): Promise<void> {
  const recipients = await getRandomRecipients(test.sampleSize);
  
  // Split recipients evenly
  const chunkSize = Math.ceil(recipients.length / test.subjectLines.length);
  const chunks: string[][] = [];
  
  for (let i = 0; i < recipients.length; i += chunkSize) {
    chunks.push(recipients.slice(i, i + chunkSize));
  }
  
  // Send with different subject lines
  for (let i = 0; i < test.subjectLines.length; i++) {
    const chunk = chunks[i] || [];
    
    await sendBatch({
      to: chunk,
      from: 'newsletter@yourapp.com',
      subject: test.subjectLines[i],
      templateId: 'd-xxxxxxxxxxxxx',
      customArgs: {
        abTest: 'subject-line',
        variant: i.toString(),
        campaignId: test.campaignId,
      },
    });
  }
}
```

---

## Production Patterns

### Email Queue with Bull

```typescript
import Queue from 'bull';

const emailQueue = new Queue('emails', {
  redis: {
    host: process.env.REDIS_HOST,
    port: parseInt(process.env.REDIS_PORT || '6379'),
  },
});

interface EmailJob {
  type: 'transactional' | 'marketing';
  provider: 'sendgrid' | 'ses' | 'mailchimp';
  data: any;
  priority?: number;
  attempts?: number;
}

// Add email to queue
async function queueEmail(job: EmailJob): Promise<void> {
  await emailQueue.add(job.type, job, {
    priority: job.priority || 5,
    attempts: job.attempts || 3,
    backoff: {
      type: 'exponential',
      delay: 2000,
    },
  });
}

// Process email queue
emailQueue.process('transactional', async (job) => {
  const { data } = job;
  
  switch (data.provider) {
    case 'sendgrid':
      await sendSESEmail(data);
      break;
    case 'ses':
      await sendSESEmail(data);
      break;
    default:
      throw new Error(`Unknown provider: ${data.provider}`);
  }
});

// Process marketing emails with rate limiting
emailQueue.process('marketing', async (job) => {
  const { data } = job;
  
  // Respect rate limits
  await rateLimiter.acquire();
  
  await sendSESEmail(data);
}, {
  concurrency: 10, // Process 10 emails at a time
});

// Error handling
emailQueue.on('failed', (job, err) => {
  console.error(`Email job ${job.id} failed:`, err);
  
  // Notify team of critical failures
  if (job.attemptsMade >= job.opts.attempts) {
    notifyTeam(`Email delivery failed after ${job.attemptsMade} attempts`, {
      emailData: job.data,
      error: err.message,
    });
  }
});
```

### Retry Strategy

```typescript
interface RetryConfig {
  maxAttempts: number;
  initialDelay: number;
  maxDelay: number;
  backoffMultiplier: number;
}

const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxAttempts: 3,
  initialDelay: 1000, // 1 second
  maxDelay: 60000, // 1 minute
  backoffMultiplier: 2,
};

async function sendWithRetry(
  sendFn: () => Promise<any>,
  config: Partial<RetryConfig> = {}
): Promise<any> {
  const finalConfig = { ...DEFAULT_RETRY_CONFIG, ...config };
  let lastError: Error | null = null;

  for (let attempt = 1; attempt <= finalConfig.maxAttempts; attempt++) {
    try {
      return await sendFn();
    } catch (error) {
      lastError = error as Error;
      
      if (attempt === finalConfig.maxAttempts) {
        throw lastError;
      }

      const delay = Math.min(
        finalConfig.initialDelay * Math.pow(finalConfig.backoffMultiplier, attempt - 1),
        finalConfig.maxDelay
      );

      console.log(`Attempt ${attempt} failed, retrying in ${delay}ms...`);
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw lastError;
}

// Usage
await sendWithRetry(() => sendEmail(emailData), {
  maxAttempts: 5,
  initialDelay: 2000,
});
```

### Bounce Management

```typescript
// Handle bounces
interface BounceRecord {
  email: string;
  bounceType: 'hard' | 'soft';
  bounceReason: string;
  bouncedAt: Date;
  provider: string;
}

async function recordBounce(bounce: BounceRecord): Promise<void> {
  await db.bounce.create({
    data: bounce,
  });

  // For hard bounces, immediately mark as invalid
  if (bounce.bounceType === 'hard') {
    await markEmailAsInvalid(bounce.email, bounce.bounceReason);
  }
}

// Check if email is safe to send
async function isEmailSafeToSend(email: string): Promise<boolean> {
  // Check bounce records
  const recentHardBounce = await db.bounce.findFirst({
    where: {
      email,
      bounceType: 'hard',
      bouncedAt: {
        gte: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000), // Last 30 days
      },
    },
  });

  if (recentHardBounce) {
    return false;
  }

  // Check for recent soft bounces (more than 3 in last 7 days)
  const recentSoftBounces = await db.bounce.count({
    where: {
      email,
      bounceType: 'soft',
      bouncedAt: {
        gte: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
      },
    },
  });

  if (recentSoftBounces >= 3) {
    return false;
  }

  return true;
}
```

---

## Python Examples

### SendGrid with Python

```python
# pip install sendgrid
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))

def send_email(to_email, from_email, subject, html_content):
    message = Mail(
        from_email=Email(from_email),
        to_emails=To(to_email),
        subject=subject,
        html_content=Content('text/html', html_content)
    )
    response = sg.send(message)
    return response.status_code

def send_template_email(to_email, template_id, template_data):
    message = Mail(
        from_email='noreply@yourapp.com',
        to_emails=to_email,
        subject='Hello',
    )
    message.template_id = template_id
    message.dynamic_template_data = template_data
    response = sg.send(message)
    return response.status_code
```

### AWS SES with Python

```python
# pip install boto3
import boto3
from botocore.exceptions import ClientError

ses = boto3.client('ses', region_name='us-east-1')

def send_email(to_email, from_email, subject, html_content, text_content=None):
    try:
        response = ses.send_email(
            Source=from_email,
            Destination={'ToAddresses': [to_email]},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {
                    'Html': {'Data': html_content, 'Charset': 'UTF-8'},
                    'Text': {'Data': text_content, 'Charset': 'UTF-8'} if text_content else None
                }
            }
        )
        return response['MessageId']
    except ClientError as e:
        print(f"Error sending email: {e}")
        raise

def send_templated_email(to_email, from_email, template_name, template_data):
    try:
        response = ses.send_templated_email(
            Source=from_email,
            Destination={'ToAddresses': [to_email]},
            Template=template_name,
            TemplateData=json.dumps(template_data)
        )
        return response['MessageId']
    except ClientError as e:
        print(f"Error sending templated email: {e}")
        raise
```

---

## Resources

- [SendGrid Documentation](https://docs.sendgrid.com/)
- [Mailchimp API Documentation](https://mailchimp.com/developer/marketing/api/)
- [AWS SES Documentation](https://docs.aws.amazon.com/ses/)
- [MJML Documentation](https://documentation.mjml.io/)
- [CAN-SPAM Act](https://www.ftc.gov/tips-advice/business-center/guidance/can-spam-act-compliance-guide-business)
- [GDPR Email Marketing Guide](https://gdpr.eu/email-marketing/)

## Best Practices

### Email Design

- **Use responsive templates**: Ensure emails render correctly on all devices
- **Keep subject lines concise**: Under 50 characters for optimal display
- **Use clear CTAs**: Make action buttons prominent and descriptive
- **Include alt text**: Ensure accessibility for images
- **Test across clients**: Verify rendering in Gmail, Outlook, Apple Mail

### Deliverability

- **Configure SPF, DKIM, DMARC**: Essential for email authentication
- **Warm up IP addresses**: Gradually increase sending volume
- **Monitor bounce rates**: Address issues promptly
- **Maintain low complaint rates**: Keep below 0.1%
- **Use dedicated IPs**: Separate transactional and marketing emails

### List Management

- **Use double opt-in**: Confirm email subscriptions
- **Clean lists regularly**: Remove invalid emails
- **Segment your audience**: Target relevant content to segments
- **Respect unsubscribe requests**: Process immediately
- **Validate emails before sending**: Check format and deliverability

### Content Strategy

- **Personalize content**: Use recipient names and relevant data
- **A/B test subject lines**: Optimize for higher open rates
- **Provide value**: Ensure content is useful to recipients
- **Include unsubscribe link**: Make it easy to opt out
- **Add physical address**: Required for CAN-SPAM compliance

### Compliance

- **Follow CAN-SPAM rules**: Include physical address and unsubscribe
- **Obtain consent**: Get explicit permission for marketing emails
- **Honor opt-out requests**: Process within 10 business days
- **GDPR compliance**: Allow data access and deletion
- **Document consent**: Keep records of opt-in consent

### Technical Implementation

- **Use webhooks for tracking**: Handle opens, clicks, bounces
- **Implement retry logic**: Handle transient failures
- **Queue emails for bulk sending**: Respect rate limits
- **Use templates**: Maintain consistent branding
- **Monitor API usage**: Track quotas and limits

### Analytics and Optimization

- **Track key metrics**: Monitor open rates, click rates, conversions
- **Set up alerts**: Notify on unusual activity
- **Analyze campaign performance**: Identify best practices
- **Test before sending**: Use preview and test emails
- **Iterate based on data**: Continuously improve campaigns

### Security

- **Secure API keys**: Use environment variables
- **Rotate credentials**: Update keys regularly
- **Use HTTPS**: Encrypt all API communications
- **Validate webhooks**: Verify sender signatures
- **Limit access**: Use least-privilege principle

## Checklist

### Setup and Configuration
- [ ] Choose email provider (SendGrid/Mailchimp/SES)
- [ ] Configure API credentials
- [ ] Set up SPF records
- [ ] Configure DKIM signing
- [ ] Set up DMARC policy

### Template Design
- [ ] Create responsive HTML templates
- [ ] Design subject lines
- [ ] Add personalization fields
- [ ] Include unsubscribe links
- [ ] Add physical address
- [ ] Test across email clients

### List Management
- [ ] Implement double opt-in
- [ ] Set up email validation
- [ ] Create audience segments
- [ ] Configure suppression lists
- [ ] Set up bounce handling

### Compliance
- [ ] Implement consent tracking
- [ ] Add unsubscribe mechanism
- [ ] Include required headers
- [ ] Document data processing
- [ ] Set up GDPR compliance

### Sending Strategy
- [ ] Configure rate limiting
- [ ] Set up email queue
- [ ] Implement retry logic
- [ ] Schedule optimal send times
- [ ] Configure warmup schedule

### Tracking and Analytics
- [ ] Enable open tracking
- [ ] Enable click tracking
- [ ] Set up webhooks
- [ ] Configure analytics dashboard
- [ ] Set up alerting

### Testing
- [ ] Set up test environment
- [ ] Test email rendering
- [ ] Test spam score
- [ ] Send test emails
- [ ] Verify link functionality

### Production
- [ ] Configure production credentials
- [ ] Set up SPF, DKIM, DMARC records
- [ ] Monitor deliverability rates
- [ ] Set up bounce handling
- [ ] Configure unsubscribe handling
```

---

## Quick Start

### SendGrid Integration

```javascript
const sgMail = require('@sendgrid/mail')
sgMail.setApiKey(process.env.SENDGRID_API_KEY)

const msg = {
  to: 'user@example.com',
  from: 'noreply@example.com',
  subject: 'Welcome!',
  text: 'Welcome to our service',
  html: '<strong>Welcome to our service</strong>'
}

await sgMail.send(msg)
```

### AWS SES Integration

```javascript
const AWS = require('aws-sdk')
const ses = new AWS.SES({ region: 'us-east-1' })

const params = {
  Source: 'noreply@example.com',
  Destination: {
    ToAddresses: ['user@example.com']
  },
  Message: {
    Subject: { Data: 'Welcome!' },
    Body: {
      Html: { Data: '<h1>Welcome!</h1>' },
      Text: { Data: 'Welcome!' }
    }
  }
}

await ses.sendEmail(params).promise()
```

### Email Template

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
    <h1>Welcome {{name}}!</h1>
    <p>Thank you for joining us.</p>
    <a href="{{actionUrl}}" style="background: #007bff; color: white; padding: 10px 20px; text-decoration: none;">
      Get Started
    </a>
  </div>
</body>
</html>
```

---

## Production Checklist

- [ ] **Email Service**: Choose and configure email service provider
- [ ] **SPF/DKIM/DMARC**: Set up email authentication records
- [ ] **Templates**: Create responsive email templates
- [ ] **Unsubscribe**: Implement unsubscribe handling (CAN-SPAM, GDPR)
- [ ] **Bounce Handling**: Handle bounces and invalid emails
- [ ] **Rate Limiting**: Respect rate limits to avoid throttling
- [ ] **Tracking**: Set up open/click tracking (if needed)
- [ ] **Testing**: Test emails across email clients
- [ ] **Deliverability**: Monitor spam scores and deliverability
- [ ] **Compliance**: Ensure GDPR/CAN-SPAM compliance
- [ ] **Error Handling**: Handle API errors gracefully
- [ ] **Monitoring**: Monitor email sending success rates

---

## Anti-patterns

### ❌ Don't: No Unsubscribe Link

```html
<!-- ❌ Bad - No unsubscribe (violates CAN-SPAM) -->
<div>Marketing email content</div>
```

```html
<!-- ✅ Good - Unsubscribe link included -->
<div>Marketing email content</div>
<p><a href="{{unsubscribeUrl}}">Unsubscribe</a></p>
```

### ❌ Don't: Ignore Bounces

```javascript
// ❌ Bad - No bounce handling
await sendEmail(user.email, content)
```

```javascript
// ✅ Good - Handle bounces
try {
  await sendEmail(user.email, content)
} catch (error) {
  if (error.isBounce) {
    markEmailAsInvalid(user.email)
  }
}
```

### ❌ Don't: No Rate Limiting

```javascript
// ❌ Bad - Send all at once
users.forEach(user => sendEmail(user.email))
```

```javascript
// ✅ Good - Rate limit
const delay = ms => new Promise(resolve => setTimeout(resolve, ms))

for (const user of users) {
  await sendEmail(user.email)
  await delay(100)  // 10 emails per second
}
```

### ❌ Don't: Hardcoded Email Addresses

```javascript
// ❌ Bad - Hardcoded
const fromEmail = 'noreply@example.com'
```

```javascript
// ✅ Good - Environment variable
const fromEmail = process.env.FROM_EMAIL || 'noreply@example.com'
```

---

## Integration Points

- **Error Handling** (`03-backend-api/error-handling/`) - Email sending errors
- **Queue Systems** (`08-messaging-queue/`) - Async email sending
- **Compliance** (`12-compliance-governance/`) - GDPR/CAN-SPAM compliance

---

## Further Reading

- [SendGrid Documentation](https://docs.sendgrid.com/)
- [AWS SES Guide](https://docs.aws.amazon.com/ses/)
- [Email Best Practices](https://www.campaignmonitor.com/resources/)
- [ ] Set up monitoring
- [ ] Configure error handling
- [ ] Set up logging
- [ ] Document procedures
