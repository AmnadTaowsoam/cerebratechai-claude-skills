---
name: Payment Gateway Integration
description: Secure processing of online payments through various providers like Stripe, PayPal, 2C2P, and Omise with proper error handling, webhooks, and PCI compliance.
---

# Payment Gateway Integration

> **Current Level:** Intermediate  
> **Domain:** E-commerce / Payments

---

## Overview

Payment gateway integration enables secure processing of online payments through various providers like Stripe, PayPal, 2C2P, and Omise. Effective payment integration handles 3D Secure, webhooks, refunds, reconciliation, and PCI compliance while providing a smooth user experience.

---

## Core Concepts

### Table of Contents

1. [Payment Gateway Comparison](#payment-gateway-comparison)
2. [Stripe Integration](#stripe-integration)
3. [PayPal Integration](#paypal-integration)
4. [Thailand-Specific Gateways](#thailand-specific-gateways)
5. [Payment Flow](#payment-flow)
6. [3D Secure](#3d-secure)
7. [Webhook Handling](#webhook-handling)
8. [Refunds and Cancellations](#refunds-and-cancellations)
9. [Payment Reconciliation](#payment-reconciliation)
10. [PCI Compliance](#pci-compliance)
11. [Testing](#testing)
12. [Error Handling](#error-handling)
13. [Best Practices](#best-practices)

---

## Payment Gateway Comparison

| Feature | Stripe | PayPal | 2C2P | Omise |
|---------|--------|--------|------|-------|
| Transaction Fee | 2.9% + 30¢ | 2.9% + 30¢ | 3.5% + 5฿ | 3.65% + 10฿ |
| Monthly Fee | None | None | 500฿ | 1,000฿ |
| Setup Fee | None | None | 10,000฿ | 5,000฿ |
| Settlement | Daily | Daily | Weekly | Daily |
| Currencies | 135+ | 25+ | 15+ | 10+ |
| Recurring | Yes | Yes | Yes | Yes |
| 3D Secure | Yes | Yes | Yes | Yes |
| API | REST | REST | REST | REST |

---

## Stripe Integration

### Stripe Setup

```typescript
// npm install stripe @stripe/stripe-js
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2024-01-01',
  typescript: true,
});

class StripeService {
  /**
   * Create payment intent
   */
  async createPaymentIntent(params: {
    amount: number;
    currency: string;
    customerId?: string;
    metadata?: Record<string, string>;
  }): Promise<Stripe.PaymentIntent> {
    return await stripe.paymentIntents.create({
      amount: Math.round(params.amount * 100), // Convert to cents
      currency: params.currency,
      customer: params.customerId,
      metadata: params.metadata,
      automatic_payment_methods: {
        enabled: true,
      },
    });
  }

  /**
   * Create checkout session
   */
  async createCheckoutSession(params: {
    items: Array<{
      name: string;
      description?: string;
      amount: number;
      currency: string;
      quantity: number;
    }>;
    successUrl: string;
    cancelUrl: string;
    customerId?: string;
    metadata?: Record<string, string>;
  }): Promise<Stripe.Checkout.Session> {
    return await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: params.items.map(item => ({
        price_data: {
          currency: item.currency,
          product_data: {
            name: item.name,
            description: item.description,
          },
          unit_amount: Math.round(item.amount * 100),
        },
        quantity: item.quantity,
      })),
      mode: 'payment',
      success_url: params.successUrl,
      cancel_url: params.cancelUrl,
      customer: params.customerId,
      metadata: params.metadata,
    });
  }

  /**
   * Create subscription
   */
  async createSubscription(params: {
    customerId: string;
    priceId: string;
    trialPeriodDays?: number;
    metadata?: Record<string, string>;
  }): Promise<Stripe.Subscription> {
    return await stripe.subscriptions.create({
      customer: params.customerId,
      items: [{ price: params.priceId }],
      trial_period_days: params.trialPeriodDays,
      metadata: params.metadata,
    });
  }

  /**
   * Create customer
   */
  async createCustomer(params: {
    email: string;
    name?: string;
    phone?: string;
    metadata?: Record<string, string>;
  }): Promise<Stripe.Customer> {
    return await stripe.customers.create({
      email: params.email,
      name: params.name,
      phone: params.phone,
      metadata: params.metadata,
    });
  }

  /**
   * Attach payment method
   */
  async attachPaymentMethod(paymentMethodId: string, customerId: string): Promise<Stripe.PaymentMethod> {
    return await stripe.paymentMethods.attach(paymentMethodId, {
      customer: customerId,
    });
  }

  /**
   * Retrieve payment intent
   */
  async retrievePaymentIntent(paymentIntentId: string): Promise<Stripe.PaymentIntent> {
    return await stripe.paymentIntents.retrieve(paymentIntentId);
  }

  /**
   * Confirm payment intent
   */
  async confirmPaymentIntent(paymentIntentId: string, paymentMethodId: string): Promise<Stripe.PaymentIntent> {
    return await stripe.paymentIntents.confirm(paymentIntentId, {
      payment_method: paymentMethodId,
    });
  }
}
```

### Stripe Webhook Handler

```typescript
import express from 'express';
import Stripe from 'stripe';

const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET!;

async function handleStripeWebhook(req: express.Request, res: express.Response): Promise<void> {
  const sig = req.headers['stripe-signature'] as string;

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, webhookSecret);
  } catch (err) {
    console.error('Webhook signature verification failed:', err);
    res.status(400).send('Invalid signature');
    return;
  }

  switch (event.type) {
    case 'payment_intent.succeeded':
      await handlePaymentIntentSucceeded(event.data.object as Stripe.PaymentIntent);
      break;
    case 'payment_intent.payment_failed':
      await handlePaymentIntentFailed(event.data.object as Stripe.PaymentIntent);
      break;
    case 'checkout.session.completed':
      await handleCheckoutSessionCompleted(event.data.object as Stripe.Checkout.Session);
      break;
    case 'invoice.paid':
      await handleInvoicePaid(event.data.object as Stripe.Invoice);
      break;
    case 'invoice.payment_failed':
      await handleInvoicePaymentFailed(event.data.object as Stripe.Invoice);
      break;
    case 'customer.subscription.created':
      await handleSubscriptionCreated(event.data.object as Stripe.Subscription);
      break;
    case 'customer.subscription.updated':
      await handleSubscriptionUpdated(event.data.object as Stripe.Subscription);
      break;
    case 'customer.subscription.deleted':
      await handleSubscriptionDeleted(event.data.object as Stripe.Subscription);
      break;
    default:
      console.log(`Unhandled event type: ${event.type}`);
  }

  res.json({ received: true });
}

async function handlePaymentIntentSucceeded(paymentIntent: Stripe.PaymentIntent): Promise<void> {
  console.log('Payment succeeded:', paymentIntent.id);

  // Update order status
  await prisma.order.update({
    where: { paymentIntentId: paymentIntent.id },
    data: {
      status: 'paid',
      paidAt: new Date(),
    },
  });

  // Send confirmation email
  await sendPaymentConfirmationEmail(paymentIntent.metadata.orderId);
}

async function handlePaymentIntentFailed(paymentIntent: Stripe.PaymentIntent): Promise<void> {
  console.log('Payment failed:', paymentIntent.id);

  // Update order status
  await prisma.order.update({
    where: { paymentIntentId: paymentIntent.id },
    data: {
      status: 'payment_failed',
      errorMessage: paymentIntent.last_payment_error?.message,
    },
  });

  // Send failure notification
  await sendPaymentFailedEmail(paymentIntent.metadata.orderId);
}

async function handleCheckoutSessionCompleted(session: Stripe.Checkout.Session): Promise<void> {
  console.log('Checkout session completed:', session.id);

  // Process order
  if (session.metadata?.orderId) {
    await prisma.order.update({
      where: { id: session.metadata.orderId },
      data: {
        status: 'paid',
        paidAt: new Date(),
      },
    });
  }
}

async function handleInvoicePaid(invoice: Stripe.Invoice): Promise<void> {
  console.log('Invoice paid:', invoice.id);

  // Update subscription payment
  await prisma.subscriptionPayment.create({
    data: {
      subscriptionId: invoice.subscription as string,
      amount: invoice.amount_paid / 100,
      currency: invoice.currency,
      paidAt: new Date(invoice.status_transitions?.paid_at! * 1000),
      invoiceId: invoice.id,
    },
  });
}

async function handleInvoicePaymentFailed(invoice: Stripe.Invoice): Promise<void> {
  console.log('Invoice payment failed:', invoice.id);

  // Notify customer
  await sendInvoiceFailedEmail(invoice.customer as string);
}

async function handleSubscriptionCreated(subscription: Stripe.Subscription): Promise<void> {
  console.log('Subscription created:', subscription.id);

  await prisma.subscription.create({
    data: {
      stripeSubscriptionId: subscription.id,
      customerId: subscription.customer as string,
      status: subscription.status,
      currentPeriodStart: new Date(subscription.current_period_start * 1000),
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
    },
  });
}

async function handleSubscriptionUpdated(subscription: Stripe.Subscription): Promise<void> {
  console.log('Subscription updated:', subscription.id);

  await prisma.subscription.update({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      status: subscription.status,
      currentPeriodStart: new Date(subscription.current_period_start * 1000),
      currentPeriodEnd: new Date(subscription.current_period_end * 1000),
    },
  });
}

async function handleSubscriptionDeleted(subscription: Stripe.Subscription): Promise<void> {
  console.log('Subscription deleted:', subscription.id);

  await prisma.subscription.update({
    where: { stripeSubscriptionId: subscription.id },
    data: {
      status: 'canceled',
      canceledAt: new Date(),
    },
  });
}
```

---

## PayPal Integration

### PayPal Service

```typescript
// npm install @paypal/checkout-server-sdk
import paypal from '@paypal/checkout-server-sdk';

const environment = new paypal.core.SandboxEnvironment(
  process.env.PAYPAL_CLIENT_ID!,
  process.env.PAYPAL_CLIENT_SECRET!
);

const client = new paypal.core.PayPalHttpClient(environment);

class PayPalService {
  /**
   * Create order
   */
  async createOrder(params: {
    amount: number;
    currency: string;
    returnUrl: string;
    cancelUrl: string;
  }): Promise<string> {
    const request = new paypal.orders.OrdersCreateRequest();
    request.prefer('return=representation');
    request.requestBody({
      intent: 'CAPTURE',
      purchase_units: [{
        amount: {
          currency_code: params.currency,
          value: params.amount.toFixed(2),
        },
      }],
      application_context: {
        return_url: params.returnUrl,
        cancel_url: params.cancelUrl,
      },
    });

    const response = await client.execute(request);
    return response.result.id;
  }

  /**
   * Capture payment
   */
  async capturePayment(orderId: string): Promise<any> {
    const request = new paypal.orders.OrdersCaptureRequest(orderId);
    request.requestBody({});

    const response = await client.execute(request);
    return response.result;
  }

  /**
   * Create subscription
   */
  async createSubscription(params: {
    planId: string;
    returnUrl: string;
    cancelUrl: string;
  }): Promise<any> {
    const request = new paypal.subscriptions.SubscriptionsCreateRequest();
    request.requestBody({
      plan_id: params.planId,
      application_context: {
        return_url: params.returnUrl,
        cancel_url: params.cancelUrl,
      },
    });

    const response = await client.execute(request);
    return response.result;
  }

  /**
   * Cancel subscription
   */
  async cancelSubscription(subscriptionId: string): Promise<void> {
    const request = new paypal.subscriptions.SubscriptionsCancelRequest(subscriptionId);
    request.requestBody({
      reason: 'Not satisfied with the service',
    });

    await client.execute(request);
  }

  /**
   * Create billing plan
   */
  async createBillingPlan(params: {
    name: string;
    description: string;
    amount: number;
    currency: string;
    interval: 'MONTH' | 'YEAR';
  }): Promise<string> {
    const request = new paypal.plans.PlansCreateRequest();
    request.requestBody({
      product_id: await this.createProduct(params.name, params.description),
      name: params.name,
      description: params.description,
      status: 'ACTIVE',
      billing_cycles: [{
        frequency: {
          interval_unit: params.interval,
          interval_count: 1,
        },
        tenure_type: 'REGULAR',
        sequence: 1,
        total_cycles: 0,
        pricing_scheme: {
          fixed_price: {
            value: params.amount.toFixed(2),
            currency_code: params.currency,
          },
        },
      }],
      payment_preferences: {
        auto_bill_outstanding: true,
        setup_fee_failure_action: 'CONTINUE',
        payment_failure_threshold: 3,
      },
    });

    const response = await client.execute(request);
    return response.result.id;
  }

  /**
   * Create product
   */
  private async createProduct(name: string, description: string): Promise<string> {
    const request = new paypal.products.ProductsCreateRequest();
    request.requestBody({
      name,
      description,
      type: 'SERVICE',
      category: 'SOFTWARE',
    });

    const response = await client.execute(request);
    return response.result.id;
  }
}
```

---

## Thailand-Specific Gateways

### 2C2P Integration

```typescript
class C2PService {
  private merchantId: string;
  private secretKey: string;
  private apiUrl: string;

  constructor() {
    this.merchantId = process.env.C2P_MERCHANT_ID!;
    this.secretKey = process.env.C2P_SECRET_KEY!;
    this.apiUrl = process.env.C2P_API_URL!;
  }

  /**
   * Generate payment request
   */
  async createPaymentRequest(params: {
    amount: number;
    currency: string;
    orderId: string;
    description: string;
    returnUrl: string;
    backUrl: string;
  }): Promise<{ paymentUrl: string; paymentToken: string }> {
    const timestamp = Date.now();
    const paymentRequest = {
      merchantID: this.merchantId,
      invoiceNo: params.orderId,
      description: params.description,
      amount: params.amount.toFixed(2),
      currencyCode: params.currency,
      paymentChannel: ['C'],
      frontendReturnUrl: params.returnUrl,
      backendReturnUrl: params.backUrl,
      timeStamp: timestamp,
    };

    const signature = this.generateSignature(paymentRequest);

    const response = await fetch(`${this.apiUrl}/payment`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        ...paymentRequest,
        signature,
      }),
    });

    const data = await response.json();

    return {
      paymentUrl: data.paymentUrl,
      paymentToken: data.paymentToken,
    };
  }

  /**
   * Generate signature
   */
  private generateSignature(params: any): string {
    const crypto = require('crypto');
    const sortedKeys = Object.keys(params).sort();

    const signatureString = sortedKeys
      .map(key => `${key}=${params[key]}`)
      .join('&');

    return crypto
      .createHmac('sha256', this.secretKey)
      .update(signatureString)
      .digest('hex');
  }

  /**
   * Verify payment response
   */
  verifyPaymentResponse(response: any): boolean {
    const signature = response.signature;
    delete response.signature;

    const calculatedSignature = this.generateSignature(response);

    return signature === calculatedSignature;
  }
}
```

### Omise Integration

```typescript
// npm install omise
import Omise from 'omise';

const omise = Omise({
  publicKey: process.env.OMISE_PUBLIC_KEY!,
  secretKey: process.env.OMISE_SECRET_KEY!,
});

class OmiseService {
  /**
   * Create charge
   */
  async createCharge(params: {
    amount: number;
    currency: string;
    cardToken: string;
    description: string;
    metadata?: Record<string, string>;
  }): Promise<any> {
    return await omise.charges.create({
      amount: Math.round(params.amount * 100), // Convert to satang
      currency: params.currency,
      card: params.cardToken,
      description: params.description,
      metadata: params.metadata,
    });
  }

  /**
   * Create token
   */
  async createToken(params: {
    cardNumber: string;
    cardExpirationMonth: number;
    cardExpirationYear: number;
    cardSecurityCode: string;
    cardHolderName: string;
  }): Promise<any> {
    return await omise.tokens.create({
      card: {
        number: params.cardNumber,
        expiration_month: params.cardExpirationMonth,
        expiration_year: params.cardExpirationYear,
        security_code: params.cardSecurityCode,
        name: params.cardHolderName,
      },
    });
  }

  /**
   * Create schedule
   */
  async createSchedule(params: {
    amount: number;
    currency: string;
    cardToken: string;
    every: number;
    period: 'day' | 'week' | 'month';
    startDate: Date;
    endDate?: Date;
    description: string;
  }): Promise<any> {
    return await omise.schedules.create({
      charge: {
        amount: Math.round(params.amount * 100),
        currency: params.currency,
        card: params.cardToken,
        description: params.description,
      },
      every: params.every,
      period: params.period,
      start_on: params.startDate.toISOString().split('T')[0],
      end_on: params.endDate?.toISOString().split('T')[0],
    });
  }

  /**
   * Retrieve charge
   */
  async retrieveCharge(chargeId: string): Promise<any> {
    return await omise.charges.retrieve(chargeId);
  }

  /**
   * Refund charge
   */
  async refundCharge(chargeId: string, amount?: number): Promise<any> {
    if (amount) {
      return await omise.charges.createRefund(chargeId, {
        amount: Math.round(amount * 100),
      });
    }

    return await omise.charges.createRefund(chargeId);
  }
}
```

---

## Payment Flow

### Payment Flow Controller

```typescript
class PaymentController {
  private stripeService: StripeService;
  private paypalService: PayPalService;
  private c2pService: C2PService;
  private omiseService: OmiseService;

  constructor() {
    this.stripeService = new StripeService();
    this.paypalService = new PayPalService();
    this.c2pService = new C2PService();
    this.omiseService = new OmiseService();
  }

  /**
   * Create payment
   */
  async createPayment(params: {
    orderId: string;
    amount: number;
    currency: string;
    gateway: 'stripe' | 'paypal' | '2c2p' | 'omise';
    returnUrl: string;
    cancelUrl: string;
  }): Promise<{
    paymentId: string;
    paymentUrl?: string;
    clientSecret?: string;
  }> {
    switch (params.gateway) {
      case 'stripe':
        return this.createStripePayment(params);
      case 'paypal':
        return this.createPayPalPayment(params);
      case '2c2p':
        return this.createC2PPayment(params);
      case 'omise':
        return this.createOmisePayment(params);
      default:
        throw new Error('Unsupported payment gateway');
    }
  }

  private async createStripePayment(params: any): Promise<any> {
    const order = await prisma.order.findUnique({
      where: { id: params.orderId },
      include: { user: true },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    const paymentIntent = await this.stripeService.createPaymentIntent({
      amount: params.amount,
      currency: params.currency,
      customerId: order.user?.stripeCustomerId,
      metadata: { orderId: params.orderId },
    });

    // Save payment intent
    await prisma.payment.create({
      data: {
        orderId: params.orderId,
        gateway: 'stripe',
        paymentIntentId: paymentIntent.id,
        amount: params.amount,
        currency: params.currency,
        status: 'pending',
      },
    });

    return {
      paymentId: paymentIntent.id,
      clientSecret: paymentIntent.client_secret,
    };
  }

  private async createPayPalPayment(params: any): Promise<any> {
    const orderId = await this.paypalService.createOrder({
      amount: params.amount,
      currency: params.currency,
      returnUrl: params.returnUrl,
      cancelUrl: params.cancelUrl,
    });

    // Save payment
    await prisma.payment.create({
      data: {
        orderId: params.orderId,
        gateway: 'paypal',
        paymentIntentId: orderId,
        amount: params.amount,
        currency: params.currency,
        status: 'pending',
      },
    });

    return {
      paymentId: orderId,
      paymentUrl: `https://www.sandbox.paypal.com/checkoutnow?token=${orderId}`,
    };
  }

  private async createC2PPayment(params: any): Promise<any> {
    const order = await prisma.order.findUnique({
      where: { id: params.orderId },
    });

    if (!order) {
      throw new Error('Order not found');
    }

    const { paymentUrl, paymentToken } = await this.c2pService.createPaymentRequest({
      amount: params.amount,
      currency: params.currency,
      orderId: params.orderId,
      description: `Order ${params.orderId}`,
      returnUrl: params.returnUrl,
      backUrl: `${process.env.API_URL}/payments/c2p/callback`,
    });

    // Save payment
    await prisma.payment.create({
      data: {
        orderId: params.orderId,
        gateway: '2c2p',
        paymentIntentId: paymentToken,
        amount: params.amount,
        currency: params.currency,
        status: 'pending',
      },
    });

    return {
      paymentId: paymentToken,
      paymentUrl,
    };
  }

  private async createOmisePayment(params: any): Promise<any> {
    const token = await this.omiseService.createToken({
      cardNumber: params.cardNumber,
      cardExpirationMonth: params.cardExpirationMonth,
      cardExpirationYear: params.cardExpirationYear,
      cardSecurityCode: params.cardSecurityCode,
      cardHolderName: params.cardHolderName,
    });

    const charge = await this.omiseService.createCharge({
      amount: params.amount,
      currency: params.currency,
      cardToken: token.id,
      description: `Order ${params.orderId}`,
      metadata: { orderId: params.orderId },
    });

    // Save payment
    await prisma.payment.create({
      data: {
        orderId: params.orderId,
        gateway: 'omise',
        paymentIntentId: charge.id,
        amount: params.amount,
        currency: params.currency,
        status: charge.status === 'successful' ? 'paid' : 'pending',
      },
    });

    return {
      paymentId: charge.id,
    };
  }
}
```

---

## 3D Secure

### 3D Secure Handler

```typescript
class ThreeDSecureHandler {
  private stripeService: StripeService;

  constructor() {
    this.stripeService = new StripeService();
  }

  /**
   * Handle 3D Secure authentication
   */
  async handleAuthentication(params: {
    paymentIntentId: string;
    paymentMethodId: string;
    clientSecret: string;
  }): Promise<Stripe.PaymentIntent> {
    try {
      // Attempt to confirm payment
      const paymentIntent = await this.stripeService.confirmPaymentIntent(
        params.paymentIntentId,
        params.paymentMethodId
      );

      if (paymentIntent.status === 'succeeded') {
        return paymentIntent;
      }

      // Handle 3D Secure
      if (paymentIntent.status === 'requires_action' ||
          paymentIntent.next_action?.type === 'use_stripe_sdk') {
        return paymentIntent;
      }

      throw new Error('Payment failed');
    } catch (error) {
      console.error('3D Secure error:', error);
      throw error;
    }
  }

  /**
   * Verify 3D Secure result
   */
  async verifyAuthentication(params: {
    paymentIntentId: string;
    clientSecret: string;
  }): Promise<Stripe.PaymentIntent> {
    const paymentIntent = await this.stripeService.retrievePaymentIntent(
      params.paymentIntentId
    );

    if (paymentIntent.status === 'succeeded') {
      return paymentIntent;
    }

    throw new Error('Payment not successful');
  }
}
```

---

## Webhook Handling

### Webhook Handler

```typescript
class WebhookHandler {
  private stripeService: StripeService;
  private paypalService: PayPalService;

  constructor() {
    this.stripeService = new StripeService();
    this.paypalService = new PayPalService();
  }

  /**
   * Handle webhook
   */
  async handleWebhook(params: {
    gateway: 'stripe' | 'paypal' | '2c2p' | 'omise';
    headers: Record<string, string>;
    body: any;
  }): Promise<void> {
    switch (params.gateway) {
      case 'stripe':
        await this.handleStripeWebhook(params.headers, params.body);
        break;
      case 'paypal':
        await this.handlePayPalWebhook(params.headers, params.body);
        break;
      case '2c2p':
        await this.handleC2PWebhook(params.body);
        break;
      case 'omise':
        await this.handleOmiseWebhook(params.body);
        break;
    }
  }

  private async handleStripeWebhook(headers: Record<string, string>, body: any): Promise<void> {
    await handleStripeWebhook({ headers, body } as any, { json: () => {} } as any);
  }

  private async handlePayPalWebhook(headers: Record<string, string>, body: any): Promise<void> {
    // Verify webhook signature
    const isValid = await this.verifyPayPalWebhook(headers, body);

    if (!isValid) {
      throw new Error('Invalid webhook signature');
    }

    // Handle event
    const eventType = body.event_type;

    switch (eventType) {
      case 'PAYMENT.CAPTURE.COMPLETED':
        await this.handlePayPalPaymentCompleted(body.resource);
        break;
      case 'PAYMENT.CAPTURE.DENIED':
        await this.handlePayPalPaymentDenied(body.resource);
        break;
    }
  }

  private async verifyPayPalWebhook(headers: Record<string, string>, body: any): Promise<boolean> {
    // Implement PayPal webhook verification
    return true;
  }

  private async handlePayPalPaymentCompleted(resource: any): Promise<void> {
    const payment = await prisma.payment.findFirst({
      where: { paymentIntentId: resource.id },
    });

    if (payment) {
      await prisma.payment.update({
        where: { id: payment.id },
        data: {
          status: 'paid',
          paidAt: new Date(),
        },
      });

      await prisma.order.update({
        where: { id: payment.orderId },
        data: {
          status: 'paid',
          paidAt: new Date(),
        },
      });
    }
  }

  private async handlePayPalPaymentDenied(resource: any): Promise<void> {
    const payment = await prisma.payment.findFirst({
      where: { paymentIntentId: resource.id },
    });

    if (payment) {
      await prisma.payment.update({
        where: { id: payment.id },
        data: {
          status: 'failed',
          errorMessage: resource.status_details?.reason,
        },
      });

      await prisma.order.update({
        where: { id: payment.orderId },
        data: {
          status: 'payment_failed',
          errorMessage: resource.status_details?.reason,
        },
      });
    }
  }

  private async handleC2PWebhook(body: any): Promise<void> {
    // Verify signature
    const isValid = new C2PService().verifyPaymentResponse(body);

    if (!isValid) {
      throw new Error('Invalid webhook signature');
    }

    // Handle payment result
    const payment = await prisma.payment.findFirst({
      where: { paymentIntentId: body.invoiceNo },
    });

    if (payment) {
      await prisma.payment.update({
        where: { id: payment.id },
        data: {
          status: body.respCode === '00' ? 'paid' : 'failed',
          paidAt: body.respCode === '00' ? new Date() : null,
          errorMessage: body.respCode !== '00' ? body.respDesc : null,
        },
      });
    }
  }

  private async handleOmiseWebhook(body: any): Promise<void> {
    // Verify webhook key
    if (body.key !== process.env.OMISE_WEBHOOK_KEY) {
      throw new Error('Invalid webhook key');
    }

    // Handle event
    switch (body.data.status) {
      case 'successful':
        await this.handleOmisePaymentSuccessful(body.data);
        break;
      case 'failed':
        await this.handleOmisePaymentFailed(body.data);
        break;
    }
  }

  private async handleOmisePaymentSuccessful(data: any): Promise<void> {
    const payment = await prisma.payment.findFirst({
      where: { paymentIntentId: data.id },
    });

    if (payment) {
      await prisma.payment.update({
        where: { id: payment.id },
        data: {
          status: 'paid',
          paidAt: new Date(),
        },
      });

      await prisma.order.update({
        where: { id: payment.orderId },
        data: {
          status: 'paid',
          paidAt: new Date(),
        },
      });
    }
  }

  private async handleOmisePaymentFailed(data: any): Promise<void> {
    const payment = await prisma.payment.findFirst({
      where: { paymentIntentId: data.id },
    });

    if (payment) {
      await prisma.payment.update({
        where: { id: payment.id },
        data: {
          status: 'failed',
          errorMessage: data.failure_message,
        },
      });

      await prisma.order.update({
        where: { id: payment.orderId },
        data: {
          status: 'payment_failed',
          errorMessage: data.failure_message,
        },
      });
    }
  }
}
```

---

## Refunds and Cancellations

### Refund Manager

```typescript
class RefundManager {
  private stripeService: StripeService;
  private paypalService: PayPalService;
  private omiseService: OmiseService;

  constructor() {
    this.stripeService = new StripeService();
    this.paypalService = new PayPalService();
    this.omiseService = new OmiseService();
  }

  /**
   * Create refund
   */
  async createRefund(params: {
    paymentId: string;
    amount?: number;
    reason?: string;
  }): Promise<Refund> {
    const payment = await prisma.payment.findUnique({
      where: { id: params.paymentId },
    });

    if (!payment) {
      throw new Error('Payment not found');
    }

    if (payment.status !== 'paid') {
      throw new Error('Payment cannot be refunded');
    }

    let refundResult: any;

    switch (payment.gateway) {
      case 'stripe':
        refundResult = await this.refundStripePayment(payment.paymentIntentId, params.amount);
        break;
      case 'paypal':
        refundResult = await this.refundPayPalPayment(payment.paymentIntentId, params.amount);
        break;
      case 'omise':
        refundResult = await this.refundOmisePayment(payment.paymentIntentId, params.amount);
        break;
      default:
        throw new Error('Refund not supported for this gateway');
    }

    // Create refund record
    const refund = await prisma.refund.create({
      data: {
        paymentId: params.paymentId,
        amount: params.amount || payment.amount,
        reason: params.reason,
        status: refundResult.status === 'succeeded' ? 'completed' : 'pending',
        gatewayRefundId: refundResult.id,
      },
    });

    return refund;
  }

  private async refundStripePayment(paymentIntentId: string, amount?: number): Promise<any> {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

    const params: Stripe.RefundCreateParams = {
      payment_intent: paymentIntentId,
    };

    if (amount) {
      params.amount = Math.round(amount * 100);
    }

    return await stripe.refunds.create(params);
  }

  private async refundPayPalPayment(orderId: string, amount?: number): Promise<any> {
    const client = new paypal.core.PayPalHttpClient(environment);

    const request = new paypal.payments.CapturesRefundRequest(orderId);
    request.requestBody({
      amount: amount ? {
        value: amount.toFixed(2),
        currency_code: 'USD',
      } : undefined,
    });

    const response = await client.execute(request);
    return response.result;
  }

  private async refundOmisePayment(chargeId: string, amount?: number): Promise<any> {
    return await this.omiseService.refundCharge(chargeId, amount);
  }
}
```

---

## Payment Reconciliation

### Reconciliation Manager

```typescript
class ReconciliationManager {
  /**
   * Reconcile payments
   */
  async reconcilePayments(params: {
    startDate: Date;
    endDate: Date;
    gateway?: 'stripe' | 'paypal' | '2c2p' | 'omise';
  }): Promise<{
    total: number;
    matched: number;
    unmatched: number;
    discrepancies: Discrepancy[];
  }> {
    const where: any = {
      createdAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    if (params.gateway) {
      where.gateway = params.gateway;
    }

    const payments = await prisma.payment.findMany({
      where,
      include: { order: true },
    });

    const discrepancies: Discrepancy[] = [];
    let matched = 0;
    let unmatched = 0;

    for (const payment of payments) {
      const gatewayData = await this.fetchGatewayPayment(payment);

      if (!gatewayData) {
        discrepancies.push({
          paymentId: payment.id,
          type: 'not_found',
          message: 'Payment not found in gateway',
        });
        unmatched++;
        continue;
      }

      const discrepancy = this.comparePayment(payment, gatewayData);

      if (discrepancy) {
        discrepancies.push(discrepancy);
        unmatched++;
      } else {
        matched++;
      }
    }

    return {
      total: payments.length,
      matched,
      unmatched,
      discrepancies,
    };
  }

  /**
   * Fetch gateway payment
   */
  private async fetchGatewayPayment(payment: any): Promise<any> {
    switch (payment.gateway) {
      case 'stripe':
        return await this.fetchStripePayment(payment.paymentIntentId);
      case 'paypal':
        return await this.fetchPayPalPayment(payment.paymentIntentId);
      case 'omise':
        return await this.fetchOmisePayment(payment.paymentIntentId);
      default:
        return null;
    }
  }

  private async fetchStripePayment(paymentIntentId: string): Promise<any> {
    const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
    return await stripe.paymentIntents.retrieve(paymentIntentId);
  }

  private async fetchPayPalPayment(orderId: string): Promise<any> {
    const client = new paypal.core.PayPalHttpClient(environment);
    const request = new paypal.orders.OrdersGetRequest(orderId);
    const response = await client.execute(request);
    return response.result;
  }

  private async fetchOmisePayment(chargeId: string): Promise<any> {
    const omise = Omise({
      secretKey: process.env.OMISE_SECRET_KEY!,
    });
    return await omise.charges.retrieve(chargeId);
  }

  /**
   * Compare payment
   */
  private comparePayment(localPayment: any, gatewayPayment: any): Discrepancy | null {
    // Check amount
    const localAmount = localPayment.amount;
    const gatewayAmount = gatewayPayment.amount / 100;

    if (Math.abs(localAmount - gatewayAmount) > 0.01) {
      return {
        paymentId: localPayment.id,
        type: 'amount_mismatch',
        message: `Amount mismatch: local ${localAmount}, gateway ${gatewayAmount}`,
        localAmount,
        gatewayAmount,
      };
    }

    // Check currency
    if (localPayment.currency !== gatewayPayment.currency) {
      return {
        paymentId: localPayment.id,
        type: 'currency_mismatch',
        message: `Currency mismatch: local ${localPayment.currency}, gateway ${gatewayPayment.currency}`,
        localCurrency: localPayment.currency,
        gatewayCurrency: gatewayPayment.currency,
      };
    }

    // Check status
    const localStatus = localPayment.status;
    const gatewayStatus = this.mapGatewayStatus(gatewayPayment.status);

    if (localStatus !== gatewayStatus) {
      return {
        paymentId: localPayment.id,
        type: 'status_mismatch',
        message: `Status mismatch: local ${localStatus}, gateway ${gatewayStatus}`,
        localStatus,
        gatewayStatus,
      };
    }

    return null;
  }

  /**
   * Map gateway status
   */
  private mapGatewayStatus(status: string): string {
    const statusMap: Record<string, string> = {
      'succeeded': 'paid',
      'paid': 'paid',
      'successful': 'paid',
      'failed': 'failed',
      'canceled': 'canceled',
    };

    return statusMap[status] || status;
  }
}

interface Discrepancy {
  paymentId: string;
  type: string;
  message: string;
  localAmount?: number;
  gatewayAmount?: number;
  localCurrency?: string;
  gatewayCurrency?: string;
  localStatus?: string;
  gatewayStatus?: string;
}
```

---

## PCI Compliance

### PCI Compliance Guidelines

```typescript
// 1. Never store card data
function validateNoCardData(data: any): boolean {
  const cardFields = [
    'cardNumber',
    'cardNumber',
    'cvv',
    'cvc',
    'expiry',
    'expiration',
  ];

  for (const field of cardFields) {
    if (data[field]) {
      throw new Error(`Card data field ${field} should not be stored`);
    }
  }

  return true;
}

// 2. Use tokenization
async function tokenizeCard(cardData: {
  number: string;
  expiryMonth: number;
  expiryYear: number;
  cvc: string;
}): Promise<string> {
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

  const token = await stripe.tokens.create({
    card: {
      number: cardData.number,
      exp_month: cardData.expiryMonth,
      exp_year: cardData.expiryYear,
      cvc: cardData.cvc,
    },
  });

  return token.id;
}

// 3. Use HTTPS
function enforceHTTPS(req: express.Request, res: express.Response, next: express.NextFunction): void {
  if (!req.secure && process.env.NODE_ENV === 'production') {
    return res.redirect('https://' + req.headers.host + req.url);
  }
  next();
}

// 4. Implement logging
function logPaymentAttempt(data: {
  orderId: string;
  amount: number;
  currency: string;
  gateway: string;
  status: string;
}): void {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    ...data,
  }));
}
```

---

## Testing

### Test Payment Manager

```typescript
class TestPaymentManager {
  /**
   * Create test payment
   */
  async createTestPayment(params: {
    gateway: 'stripe' | 'paypal' | 'omise';
    amount: number;
    currency: string;
  }): Promise<{
    paymentId: string;
    testCardNumber: string;
  }> {
    switch (params.gateway) {
      case 'stripe':
        return this.createStripeTestPayment(params);
      case 'paypal':
        return this.createPayPalTestPayment(params);
      case 'omise':
        return this.createOmiseTestPayment(params);
      default:
        throw new Error('Unsupported gateway');
    }
  }

  private createStripeTestPayment(params: any): any {
    const testCards = {
      success: '4242424242424242',
      decline: '4000000000000002',
      insufficient_funds: '4000000000009995',
      expired: '4000000000000069',
      incorrect_cvc: '4000000000000127',
    };

    return {
      paymentId: 'pi_test_' + Date.now(),
      testCardNumber: testCards.success,
    };
  }

  private createPayPalTestPayment(params: any): any {
    return {
      paymentId: 'PAYPAL_TEST_' + Date.now(),
      testCardNumber: '4111111111111111',
    };
  }

  private createOmiseTestPayment(params: any): any {
    return {
      paymentId: 'chrg_test_' + Date.now(),
      testCardNumber: '4242424242424242',
    };
  }
}
```

---

## Error Handling

### Payment Error Handler

```typescript
class PaymentErrorHandler {
  /**
   * Handle payment error
   */
  handleError(error: any, context: {
    orderId: string;
    gateway: string;
    amount: number;
  }): void {
    console.error('Payment error:', {
      error: error.message,
      code: error.code,
      type: error.type,
      ...context,
    });

    // Update order with error
    prisma.order.update({
      where: { id: context.orderId },
      data: {
        status: 'payment_failed',
        errorMessage: error.message,
      },
    });

    // Send notification
    this.sendErrorNotification(error, context);
  }

  /**
   * Classify error
   */
  classifyError(error: any): {
    type: 'card_error' | 'network_error' | 'api_error' | 'validation_error';
    recoverable: boolean;
    userMessage: string;
  } {
    if (error.type === 'StripeCardError') {
      return {
        type: 'card_error',
        recoverable: false,
        userMessage: error.message,
      };
    }

    if (error.type === 'StripeConnectionError' || error.type === 'StripeAPIError') {
      return {
        type: 'network_error',
        recoverable: true,
        userMessage: 'Network error. Please try again.',
      };
    }

    if (error.type === 'StripeInvalidRequestError') {
      return {
        type: 'validation_error',
        recoverable: false,
        userMessage: 'Invalid request. Please contact support.',
      };
    }

    return {
      type: 'api_error',
      recoverable: true,
      userMessage: 'An error occurred. Please try again.',
    };
  }

  private sendErrorNotification(error: any, context: any): void {
    // Send to Slack, email, etc.
    console.log('Sending error notification:', error.message);
  }
}
```

---

## Best Practices

### Payment Best Practices

```typescript
// 1. Always validate payment intent before processing
async function validatePaymentIntent(paymentIntentId: string): Promise<boolean> {
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);
  const paymentIntent = await stripe.paymentIntents.retrieve(paymentIntentId);

  return paymentIntent.status === 'succeeded';
}

// 2. Use idempotency keys to prevent duplicate charges
function generateIdempotencyKey(): string {
  return `idemp_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

// 3. Implement payment retries with exponential backoff
async function retryPayment(
  paymentIntentId: string,
  maxRetries: number = 3
): Promise<Stripe.PaymentIntent> {
  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const paymentIntent = await stripe.paymentIntents.confirm(paymentIntentId);

      if (paymentIntent.status === 'succeeded') {
        return paymentIntent;
      }
    } catch (error) {
      if (attempt === maxRetries) {
        throw error;
      }

      const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }

  throw new Error('Payment failed after retries');
}

// 4. Store minimal payment data
interface PaymentRecord {
  id: string;
  orderId: string;
  gateway: string;
  paymentIntentId: string;
  amount: number;
  currency: string;
  status: string;
  createdAt: Date;
  paidAt?: Date;
}

// 5. Implement payment timeout
async function processPaymentWithTimeout(
  paymentFn: () => Promise<any>,
  timeoutMs: number = 30000
): Promise<any> {
  return Promise.race([
    paymentFn(),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Payment timeout')), timeoutMs)
    ),
  ]);
}
```

---

---

## Quick Start

### Stripe Payment

```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY)

// Create payment intent
const paymentIntent = await stripe.paymentIntents.create({
  amount: 2000,  // $20.00
  currency: 'usd',
  metadata: { orderId: '123' }
})

// Client-side confirmation
// (Use Stripe.js on frontend)
```

### Webhook Handling

```javascript
const express = require('express')
const app = express()

app.post('/webhook', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature']
  const event = stripe.webhooks.constructEvent(req.body, sig, process.env.WEBHOOK_SECRET)
  
  if (event.type === 'payment_intent.succeeded') {
    const paymentIntent = event.data.object
    // Update order status
    updateOrderStatus(paymentIntent.metadata.orderId, 'paid')
  }
  
  res.json({ received: true })
})
```

---

## Production Checklist

- [ ] **API Keys**: Store API keys securely (secrets manager)
- [ ] **Webhooks**: Set up webhook endpoints with signature verification
- [ ] **3D Secure**: Implement 3D Secure for high-value transactions
- [ ] **Error Handling**: Handle payment failures gracefully
- [ ] **Idempotency**: Use idempotency keys for retries
- [ ] **Testing**: Test with test cards and sandbox environments
- [ ] **PCI Compliance**: Never store card data, use tokenization
- [ ] **Reconciliation**: Implement payment reconciliation
- [ ] **Refunds**: Handle refunds and cancellations
- [ ] **Monitoring**: Monitor payment success rates and failures
- [ ] **Logging**: Log all payment attempts (without sensitive data)
- [ ] **Rate Limiting**: Implement rate limiting on payment endpoints

---

## Anti-patterns

### ❌ Don't: Store Card Data

```javascript
// ❌ Bad - Storing card data (PCI violation!)
const cardData = {
  number: '4242424242424242',
  cvv: '123',
  expiry: '12/25'
}
await db.save(cardData)  // NEVER!
```

```javascript
// ✅ Good - Use tokenization
const paymentMethod = await stripe.paymentMethods.create({
  type: 'card',
  card: { token: 'tok_visa' }  // Token from Stripe.js
})
// Store only payment method ID
await db.save({ paymentMethodId: paymentMethod.id })
```

### ❌ Don't: No Webhook Verification

```javascript
// ❌ Bad - No signature verification
app.post('/webhook', (req, res) => {
  const event = req.body  // Trusted without verification!
  processEvent(event)
})
```

```javascript
// ✅ Good - Verify webhook signature
app.post('/webhook', express.raw({ type: 'application/json' }), (req, res) => {
  const sig = req.headers['stripe-signature']
  try {
    const event = stripe.webhooks.constructEvent(
      req.body, 
      sig, 
      process.env.WEBHOOK_SECRET
    )
    processEvent(event)
  } catch (err) {
    return res.status(400).send(`Webhook Error: ${err.message}`)
  }
})
```

### ❌ Don't: No Idempotency

```javascript
// ❌ Bad - Can create duplicate charges
app.post('/charge', async (req, res) => {
  await stripe.charges.create({ amount: 1000 })  // Can be called twice!
})
```

```javascript
// ✅ Good - Use idempotency key
app.post('/charge', async (req, res) => {
  const idempotencyKey = req.headers['idempotency-key']
  await stripe.charges.create(
    { amount: 1000 },
    { idempotencyKey }  // Prevents duplicates
  )
})
```

### ❌ Don't: Ignore Payment Failures

```javascript
// ❌ Bad - No error handling
const charge = await stripe.charges.create({ amount: 1000 })
// What if it fails?
```

```javascript
// ✅ Good - Handle failures
try {
  const charge = await stripe.charges.create({ amount: 1000 })
  await updateOrderStatus(orderId, 'paid')
} catch (error) {
  if (error.type === 'StripeCardError') {
    await updateOrderStatus(orderId, 'payment_failed', error.message)
  }
  throw error
}
```

---

## Integration Points

- **Secrets Management** (`24-security-practices/secrets-management/`) - Secure API keys
- **Webhooks** (`03-backend-api/`) - Webhook handling patterns
- **Error Handling** (`03-backend-api/error-handling/`) - Payment error handling
- **Idempotency** (`40-system-resilience/idempotency-and-dedup/`) - Prevent duplicate charges

---

## Further Reading

- [Stripe Documentation](https://stripe.com/docs/)
- [PayPal Developer Docs](https://developer.paypal.com/docs/)
- [2C2P Documentation](https://developer.2c2p.com/)
- [Omise Documentation](https://www.omise.co/docs)
- [PCI Compliance Guide](https://www.pcisecuritystandards.org/)
- [PCI DSS Requirements](https://www.pcisecuritystandards.org/)
