# Stripe Integration

## Overview

Comprehensive guide to Stripe payment integration for web applications.

## Table of Contents

1. [Stripe Setup](#stripe-setup)
2. [Payment Intents](#payment-intents)
3. [Checkout Session](#checkout-session)
4. [Payment Methods](#payment-methods)
5. [Customer Management](#customer-management)
6. [Webhook Handling](#webhook-handling)
7. [Error Handling](#error-handling)
8. [Testing (Test Mode)](#testing-test-mode)
9. [PCI Compliance](#pci-compliance)
10. [Subscription Payments](#subscription-payments)
11. [Refunds](#refunds)
12. [Production Checklist](#production-checklist)

---

## Stripe Setup

### Installation

```bash
# stripe-install.sh
# Using npm
npm install stripe

# Using yarn
yarn add stripe

# Using pip
pip install stripe
```

### Configuration

```typescript
// stripe-config.ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
  typescript: true,
});

export const stripeConfig = {
  webhookSecret: process.env.STRIPE_WEBHOOK_SECRET!,
  webhookEndpoint: process.env.STRIPE_WEBHOOK_ENDPOINT!,
  successUrl: process.env.STRIPE_SUCCESS_URL!,
  cancelUrl: process.env.STRIPE_CANCEL_URL!,
  currency: 'usd'
};
```

### Environment Variables

```bash
# .env.example
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
STRIPE_WEBHOOK_ENDPOINT=http://localhost:3000/api/webhooks/stripe
STRIPE_SUCCESS_URL=http://localhost:3000/payment/success
STRIPE_CANCEL_URL=http://localhost:3000/payment/cancel
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
NODE_ENV=development
```

---

## Payment Intents

### Create Payment Intent

```typescript
// payment-intent.ts
import { Stripe } from 'stripe';

export class PaymentIntentService {
  async createPaymentIntent(
    amount: number,
    currency: string = 'usd',
    customerId?: string,
    metadata?: Record<string, string>
  ): Promise<Stripe.PaymentIntent> {
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount * 100), // Convert to cents
      currency,
      customer: customerId,
      metadata,
      automatic_payment_methods: ['card'],
      description: 'Order payment',
      receipt_email: metadata?.email,
      shipping: metadata?.shippingAddress ? {
        name: metadata.shippingAddress.name,
        address: {
          line1: metadata.shippingAddress.line1,
          city: metadata.shippingAddress.city,
          state: metadata.shippingAddress.state,
          postal_code: metadata.shippingAddress.postalCode,
          country: metadata.shippingAddress.country
        }
      } : undefined,
    });
    
    console.log(`Payment intent created: ${paymentIntent.id}`);
    return paymentIntent;
  }
  
  async retrievePaymentIntent(paymentIntentId: string): Promise<Stripe.PaymentIntent> {
    const paymentIntent = await stripe.paymentIntents.retrieve(paymentIntentId);
    console.log(`Payment intent retrieved: ${paymentIntent.status}`);
    return paymentIntent;
  }
  
  async confirmPaymentIntent(paymentIntentId: string): Promise<Stripe.PaymentIntent> {
    const paymentIntent = await stripe.paymentIntents.confirm(paymentIntentId);
    console.log(`Payment intent confirmed: ${paymentIntent.status}`);
    return paymentIntent;
  }
  
  async cancelPaymentIntent(paymentIntentId: string): Promise<Stripe.PaymentIntent> {
    const paymentIntent = await stripe.paymentIntents.cancel(paymentIntentId);
    console.log(`Payment intent cancelled: ${paymentIntent.status}`);
    return paymentIntent;
  }
  
  async listPaymentIntents(limit: number = 10): Promise<Stripe.ApiList<Stripe.PaymentIntent>> {
    const paymentIntents = await stripe.paymentIntents.list({
      limit,
      expand: ['data.customer']
    });
    
    return paymentIntents;
  }
}
```

### Payment Intent with Setup Future Usage

```typescript
// payment-intent-with-setup.ts
export class PaymentIntentWithSetupService {
  async createPaymentIntentWithSetup(
    amount: number,
    currency: string = 'usd',
    customerId?: string,
    paymentMethodTypes: string[] = ['card']
  ): Promise<Stripe.PaymentIntent> {
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount * 100),
      currency,
      customer: customerId,
      payment_method_types: paymentMethodTypes,
      setup_future_usage: 'off_session', // or 'on_session'
      description: 'Order payment',
      metadata: {
        order_id: 'order_123'
      }
    });
    
    return paymentIntent;
  }
  
  async createSubscriptionPaymentIntent(
    customerId: string,
    priceId: string,
    quantity: number = 1
  ): Promise<Stripe.PaymentIntent> {
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(quantity * 100), // Price in cents
      currency: 'usd',
      customer: customerId,
      payment_method: 'card',
      setup_future_usage: 'off_session',
      description: 'Subscription payment',
      metadata: {
        price_id: priceId,
        quantity
      }
    });
    
    return paymentIntent;
  }
}
```

---

## Checkout Session

### Create Checkout Session

```typescript
// checkout-session.ts
import { Stripe } from 'stripe';

export class CheckoutSessionService {
  async createCheckoutSession(
    items: Array<{
      price: string;
      quantity: number
    }>,
    successUrl: string,
    cancelUrl: string,
    customerEmail?: string,
    mode: 'payment' | 'subscription' = 'payment'
  ): Promise<Stripe.Checkout.Session> {
    const lineItems = items.map(item => ({
      price: item.price,
      quantity: item.quantity
    }));
    
    const session = await stripe.checkout.sessions.create({
      mode,
      line_items: lineItems,
      success_url: successUrl,
      cancel_url: cancelUrl,
      customer_email: customerEmail,
      allow_promotion_codes: true,
      billing_address_collection: 'required',
      shipping_address_collection: 'required',
      metadata: {
        order_id: 'order_123'
      }
    });
    
    console.log(`Checkout session created: ${session.id}`);
    return session;
  }
  
  async createSubscriptionCheckoutSession(
    priceId: string,
    successUrl: string,
    cancelUrl: string,
    customerId: string
  ): Promise<Stripe.Checkout.Session> {
    const session = await stripe.checkout.sessions.create({
      mode: 'subscription',
      payment_method_types: ['card'],
      line_items: [{
        price: priceId,
        quantity: 1
      }],
      success_url: successUrl,
      cancel_url: cancel_url,
      customer: customerId,
      allow_promotion_codes: true,
      subscription_data: {
        metadata: {
          order_id: 'order_123'
        }
      }
    });
    
    return session;
  }
  
  async retrieveCheckoutSession(sessionId: string): Promise<Stripe.Checkout.Session> {
    const session = await stripe.checkout.sessions.retrieve(sessionId);
    return session;
  }
}
```

### Express Route

```typescript
// checkout-routes.ts
import express from 'express';
import { CheckoutSessionService, PaymentIntentService } from './checkout-session';

const router = express.Router();
const checkoutService = new CheckoutSessionService();
const paymentIntentService = new PaymentIntentService();

// Create checkout session
router.post('/checkout', async (req, res) => {
  try {
    const { items, customerEmail } = req.body;
    
    const session = await checkoutService.createCheckoutSession(
      items,
      stripeConfig.successUrl,
      stripeConfig.cancelUrl,
      customerEmail
    );
    
    res.json({
      sessionId: session.id,
      url: session.url
    });
  } catch (error) {
    console.error('Error creating checkout session:', error);
    res.status(500).json({ error: 'Failed to create checkout session' });
  }
});

// Create payment intent
router.post('/payment-intent', async (req, res) => {
  try {
    const { amount, currency, customerId, metadata } = req.body;
    
    const paymentIntent = await paymentIntentService.createPaymentIntent(
      amount,
      currency,
      customerId,
      metadata
    );
    
    res.json({
      clientSecret: paymentIntent.client_secret,
      publishableKey: paymentIntent.publishable_key
    });
  } catch (error) {
    console.error('Error creating payment intent:', error);
    res.status(500).json({ error: 'Failed to create payment intent' });
  }
});

export default router;
```

---

## Payment Methods

### List Available Payment Methods

```typescript
// payment-methods.ts
import { Stripe } from 'stripe';

export class PaymentMethodService {
  async listPaymentMethods(): Promise<Stripe.PaymentMethod[]> {
    const paymentMethods = await stripe.paymentMethods.list({
      limit: 100,
      expand: ['data.customer']
    });
    
    return paymentMethods.data;
  }
  
  async createPaymentMethod(
    customerId: string,
    paymentMethodType: Stripe.PaymentMethodCreateParams.Type
  ): Promise<Stripe.PaymentMethod> {
    const paymentMethod = await stripe.paymentMethods.create({
      customer: customerId,
      type: paymentMethodType,
      billing_details: {
        name: 'John Doe',
        email: 'john.doe@example.com',
        phone: '+15551234567',
        address: {
          line1: '123 Main St',
          city: 'San Francisco',
          state: 'CA',
          postal_code: '94107',
          country: 'US'
        }
      },
      metadata: {
        source: 'web'
      }
    });
    
    console.log(`Payment method created: ${paymentMethod.id}`);
    return paymentMethod;
  }
  
  async detachPaymentMethod(paymentMethodId: string): Promise<Stripe.PaymentMethod> {
    const paymentMethod = await stripe.paymentMethods.detach(paymentMethodId);
    console.log(`Payment method detached: ${paymentMethod.id}`);
    return paymentMethod;
  }
  
  async updatePaymentMethod(
    paymentMethodId: string,
    default: boolean
  ): Promise<Stripe.PaymentMethod> {
    const paymentMethod = await stripe.paymentMethods.update(paymentMethodId, {
      default
    });
    
    return paymentMethod;
  }
}
```

---

## Customer Management

### Customer Creation

```typescript
// customer-service.ts
import { Stripe } from 'stripe';

export class CustomerService {
  async createCustomer(
    email: string,
    name: string,
    phone?: string,
    metadata?: Record<string, string>
  ): Promise<Stripe.Customer> {
    const customer = await stripe.customers.create({
      email,
      name,
      phone,
      metadata,
      description: 'Customer created via web app',
      payment_method: 'default',
      address: {
        line1: '123 Main St',
        city: 'San Francisco',
        state: 'CA',
        postal_code: '94107',
        country: 'US'
      },
      invoice_settings: {
        default_payment_method: 'card'
      },
      preferences: {
        invoice_pdf: true
      }
    });
    
    console.log(`Customer created: ${customer.id}`);
    return customer;
  }
  
  async retrieveCustomer(customerId: string): Promise<Stripe.Customer> {
    const customer = await stripe.customers.retrieve(customerId);
    return customer;
  }
  
  async updateCustomer(
    customerId: string,
    updates: Stripe.CustomerUpdateParams
  ): Promise<Stripe.Customer> {
    const customer = await stripe.customers.update(customerId, updates);
    console.log(`Customer updated: ${customer.id}`);
    return customer;
  }
  
  async deleteCustomer(customerId: string): Promise<Stripe.Customer> {
    const customer = await stripe.customers.del(customerId);
    console.log(`Customer deleted: ${customer.id}`);
    return customer;
  }
  
  async listCustomers(limit: number = 10): Promise<Stripe.ApiList<Stripe.Customer>> {
    const customers = await stripe.customers.list({
      limit,
      expand: ['data.sources']
    });
    
    return customers;
  }
}
```

---

## Webhook Handling

### Webhook Signature Verification

```typescript
// webhook-handler.ts
import crypto from 'crypto';
import { Stripe } from 'stripe';
import express, { Request, Response, NextFunction } from 'express';

export class WebhookHandler {
  static verifySignature(
    payload: string,
    signature: string,
    secret: string
  ): boolean {
    const hmac = crypto
      .createHmac('sha256', secret)
      .update(payload, 'utf8')
      .digest('hex');
    
    const expectedSignature = signature.split(',')[1].trim();
    const computedSignature = hmac;
    
    return crypto.timingSafeEqual(
      Buffer.from(expectedSignature, 'utf8'),
      computedSignature
    );
  }
  
  static async handleWebhook(
    req: Request,
    res: Response,
    next: NextFunction
  ): Promise<void> {
    const signature = req.headers['stripe-signature'];
    const payload = req.body;
    
    // Verify signature
    const isValid = this.verifySignature(
      JSON.stringify(payload),
      signature,
      stripeConfig.webhookSecret
    );
    
    if (!isValid) {
      console.error('Invalid webhook signature');
      return res.status(400).json({ error: 'Invalid signature' });
    }
    
    const event = payload.type;
    console.log(`Webhook event: ${event}`);
    
    try {
      switch (event) {
        case 'checkout.session.completed':
          await this.handleCheckoutCompleted(payload);
          break;
        case 'payment_intent.succeeded':
          await this.handlePaymentSucceeded(payload);
          break;
        case 'payment_intent.payment_failed':
          await this.handlePaymentFailed(payload);
          break;
        case 'invoice.payment_succeeded':
          await this.handleInvoicePaymentSucceeded(payload);
          break;
        case 'customer.subscription.created':
          await this.handleSubscriptionCreated(payload);
          break;
        case 'customer.subscription.updated':
          await this.handleSubscriptionUpdated(payload);
          break;
        case 'customer.subscription.deleted':
          await this.handleSubscriptionDeleted(payload);
          break;
        default:
          console.log(`Unhandled event: ${event}`);
      }
      
      res.status(200).json({ received: true });
    } catch (error) {
      console.error('Error handling webhook:', error);
      res.status(500).json({ error: 'Webhook processing failed' });
    }
  }
  
  private static async handleCheckoutCompleted(payload: any): Promise<void> {
    const { data } = payload;
    console.log(`Checkout completed: ${data.id}`);
    // Update order status
  }
  
  private static async handlePaymentSucceeded(payload: any): Promise<void> {
    const { data } = payload;
    console.log(`Payment succeeded: ${data.id}`);
    // Update order status
  }
  
  private static async handlePaymentFailed(payload: any): Promise<void> {
    const { data } = payload;
    console.log(`Payment failed: ${data.id}`);
    // Update order status
  }
  
  private static async handleSubscriptionCreated(payload: any): Promise<void> {
    const { data } = payload;
    console.log(`Subscription created: ${data.id}`);
    // Create subscription record
  }
  
  private static async handleSubscriptionUpdated(payload: any): Promise<void> {
    const { data } = payload;
    console.log(`Subscription updated: ${data.id}`);
    // Update subscription record
  }
  
  private static async handleSubscriptionDeleted(payload: any): Promise<void> {
    const { data } = payload;
    console.log(`Subscription deleted: ${data.id}`);
    // Cancel subscription
  }
  
  private static async handleInvoicePaymentSucceeded(payload: any): Promise<void> {
    const { data } = payload;
    console.log(`Invoice payment succeeded: ${data.id}`);
    // Update invoice status
  }
}

// Express middleware
export const webhookMiddleware = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  WebhookHandler.handleWebhook(req, res, next);
};
```

### Idempotency

```typescript
// webhook-idempotency.ts
export class WebhookIdempotency {
  private processedEvents: Map<string, number> = new Map();
  
  static async isProcessed(eventId: string): Promise<boolean> {
    // Check if event has been processed
    return this.processedEvents.has(eventId);
  }
  
  static async markProcessed(eventId: string): Promise<void> {
    // Mark event as processed
    this.processedEvents.set(eventId, Date.now());
  }
  
  static async cleanupOldEvents(maxAge: number = 24 * 60 * 60 * 1000): Promise<void> {
    const now = Date.now();
    const cutoff = now - maxAge;
    
    for (const [eventId, timestamp] of this.processedEvents.entries()) {
      if (timestamp < cutoff) {
        this.processedEvents.delete(eventId);
      }
    }
  }
}

// Cron job for cleanup
import cron from 'node-cron';

cron.schedule('0 * * * *', async () => {
  await WebhookIdempotency.cleanupOldEvents();
});
```

---

## Error Handling

### Error Handler

```typescript
// stripe-error-handler.ts
export class StripeErrorHandler {
  static handleStripeError(error: any): {
    if (error.type === 'StripeCardError') {
      return {
        type: 'card_error',
        message: error.message,
        code: error.code,
        decline_code: error.decline_code
      };
    }
    
    if (error.type === 'StripeInvalidRequestError') {
      return {
        type: 'invalid_request',
        message: error.message,
        param: error.param
      };
    }
    
    if (error.type === 'StripeAPIError') {
      return {
        type: 'api_error',
        message: error.message,
        status: error.status,
        code: error.code
      };
    }
    
    if (error.type === 'StripeConnectionError') {
      return {
        type: 'connection_error',
        message: 'Failed to connect to Stripe',
        error: error.message
      };
    }
    
    return {
      type: 'unknown_error',
      message: error.message || 'Unknown Stripe error'
    };
  }
}

// Express error handler
export function stripeErrorHandler(
  err: Error,
  req: any,
  res: any,
  next: any
) {
  if (err.type.startsWith('Stripe')) {
    const errorInfo = StripeErrorHandler.handleStripeError(err);
    
    if (err.type === 'StripeCardError') {
      return res.status(400).json({
        error: errorInfo
      });
    }
    
    if (err.type === 'StripeAPIError' && err.status === 402) {
      return res.status(402).json({
        error: errorInfo
      });
    }
  }
  
  next(err);
}
```

---

## Testing (Test Mode)

### Test Mode Configuration

```typescript
// stripe-test-config.ts
import Stripe from 'stripe';

// Use test mode for development
export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
  typescript: true,
});

export const testModeConfig = {
  testMode: process.env.NODE_ENV === 'development',
  publishableKey: process.env.STRIPE_PUBLISHABLE_KEY,
  webhookUrl: process.env.STRIPE_WEBHOOK_ENDPOINT
};
```

### Test Data

```typescript
// stripe-test-data.ts
export const testPaymentIntent = {
  amount: 2000, // $20.00
  currency: 'usd',
  payment_method_types: ['card'],
  metadata: {
    order_id: 'test_order_123'
  }
};

export const testCheckoutSession = {
  mode: 'payment' as const,
  line_items: [{
    price: 'price_123',
    quantity: 1
  }],
  success_url: 'http://localhost:3000/payment/success',
  cancel_url: 'http://localhost:3000/payment/cancel'
};

export const testCustomer = {
  email: 'test@example.com',
  name: 'Test User',
  phone: '+15551234567'
};
```

---

## PCI Compliance

### PCI Compliance Checklist

```markdown
## PCI DSS Compliance Checklist

### Data Storage
- [ ] Never store full card numbers
- [ ] Never store CVV/CVC codes
- [ ] Never store PINs
- [ ] Store only last 4 digits of card number
- [ ] Use tokenization
- [ ] Encrypt cardholder data at rest
- [ ] Use TLS for all card data
- [ ] Implement proper access controls

### Transmission
- [ ] Use HTTPS for all API calls
- [ ] Implement TLS 1.2+
- [ ] Use strong cipher suites
- [ ] Validate SSL certificates
- [ ] Implement HSTS
- [ ] Implement certificate pinning

### Processing
- [ ] Don't log sensitive card data
- [ ] Mask card numbers in logs
- [ ] Never log CVV/CVC/PINs
- [ ] Implement secure logging practices
- [ ] Use secure log storage
- [ ] Implement log retention policies

### Storage
- [ ] Encrypt cardholder data at rest
- [ ] Use strong encryption (AES-256)
- [ ] Implement proper key management
- [ ] Rotate encryption keys regularly
- [ ] Use HSM for key storage
- [ ] Implement secure key backup

### Network Security
- [ ] Use firewall rules
- [ ] Restrict access to Stripe APIs
- [ ] Implement IP whitelisting
- [ ] Monitor for suspicious activity
- [ ] Implement intrusion detection

### Application Security
- [ ] Validate all inputs
- [ ] Implement rate limiting
- [ ] Implement request validation
- [ ] Sanitize all outputs
- [ ] Implement CSP headers
- [ ] Implement XSS protection

### Compliance Validation
- [ ] Regular security audits
- [ ] Penetration testing
- [ ] Vulnerability scanning
- [ ] Compliance documentation
- [ ] Employee training
```

---

## Subscription Payments

### Subscription Creation

```typescript
// subscription-payment.ts
import { Stripe } from 'stripe';

export class SubscriptionService {
  async createSubscription(
    customerId: string,
    priceId: string,
    paymentMethodId: string,
    trialPeriodDays?: number
  ): Promise<Stripe.Subscription> {
    const subscription = await stripe.subscriptions.create({
      customer: customerId,
      items: [{
        price: priceId,
        quantity: 1
      }],
      default_payment_method: paymentMethodId,
      payment_behavior: 'default_incomplete',
      billing_cycle_anchor: 28, // 28th of month
      proration_behavior: 'create_prorations',
      metadata: {
        order_id: 'order_123'
      },
      trial_period_days: trialPeriodDays
    });
    
    console.log(`Subscription created: ${subscription.id}`);
    return subscription;
  }
  
  async retrieveSubscription(subscriptionId: string): Promise<Stripe.Subscription> {
    const subscription = await stripe.subscriptions.retrieve(subscriptionId);
    return subscription;
  }
  
  async updateSubscription(
    subscriptionId: string,
    updates: Stripe.SubscriptionUpdateParams
  ): Promise<Stripe.Subscription> {
    const subscription = await stripe.subscriptions.update(subscriptionId, updates);
    console.log(`Subscription updated: ${subscription.id}`);
    return subscription;
  }
  
  async cancelSubscription(
    subscriptionId: string,
    cancelAtPeriodEnd: boolean = true
  ): Promise<Stripe.Subscription> {
    const subscription = await stripe.subscriptions.cancel(subscriptionId, {
      cancel_at_period_end: cancelAtPeriodEnd
    });
    
    console.log(`Subscription cancelled: ${subscription.id}`);
    return subscription;
  }
  
  async listSubscriptions(
    customerId: string,
    status: Stripe.Subscription.Status = 'all'
  ): Promise<Stripe.ApiList<Stripe.Subscription>> {
    const subscriptions = await stripe.subscriptions.list({
      customer: customerId,
      status,
      expand: ['data.default_payment_method', 'latest_invoice']
    });
    
    return subscriptions;
  }
}
```

---

## Refunds

### Create Refund

```typescript
// refund-service.ts
import { Stripe } from 'stripe';

export class RefundService {
  async createRefund(
    chargeId: string,
    amount?: number,
    reason?: string,
    metadata?: Record<string, string>
  ): Promise<Stripe.Refund> {
    const refund = await stripe.refunds.create({
      charge: chargeId,
      amount: amount ? Math.round(amount * 100) : undefined,
      reason: reason || 'Customer request',
      metadata
    });
    
    console.log(`Refund created: ${refund.id}`);
    return refund;
  }
  
  async retrieveRefund(refundId: string): Promise<Stripe.Refund> {
    const refund = await stripe.refunds.retrieve(refundId);
    return refund;
  }
  
  async createPartialRefund(
    chargeId: string,
    amount: number,
    reason?: string
  ): Promise<Stripe.Refund> {
    const refund = await stripe.refunds.create({
      charge: chargeId,
      amount: Math.round(amount * 100),
      reason: reason || 'Partial refund',
      metadata: {
        partial: true
      }
    });
    
    console.log(`Partial refund created: ${refund.id}`);
    return refund;
  }
  
  async listRefunds(limit: number = 100): Promise<Stripe.ApiList<Stripe.Refund>> {
    const refunds = await stripe.refunds.list({
      limit,
      expand: ['data.charge']
    });
    
    return refunds;
  }
}
```

---

## Production Checklist

```markdown
## Stripe Production Checklist

### Configuration
- [ ] API keys configured in environment variables
- [ ] Webhook endpoint configured
- [ ] Webhook secret configured
- ] Success/cancel URLs configured
- ] Default currency set
- ] Test mode disabled in production

### Webhooks
- [ ] Webhook endpoint accessible
- [ ] Webhook signature verification
- [ ] Idempotency handling
- [ ] Retry logic implemented
- [ ] Error logging
- [ ] Webhook event tracking
- [ ] Webhook timeout handling

### Security
- [ ] HTTPS only in production
- [ ] API keys stored securely
- [ ] Webhook secret stored securely
- [ ] Client-side tokens not exposed
- [ ] Card data not logged
- [ ] PCI compliance verified
- [ ] Rate limiting implemented
- [ ] Input validation

### Error Handling
- [ ] Stripe errors handled gracefully
- [ ] User-friendly error messages
- [ ] Proper HTTP status codes
- [ ] Error logging implemented
- [ ] Monitoring/alerting configured
- [ ] Retry logic for transient errors

### Monitoring
- [ ] Payment success rate tracked
- [ ] Payment failure rate tracked
- [ ] Webhook delivery monitored
- [ ] Refund rate tracked
- [ ] Dispute rate tracked
- [ ] Revenue metrics tracked

### Testing
- [ ] Test mode used in development
- [ ] Test cards available
- [ ] Webhook testing completed
- [ ] Payment flow tested
- [ ] Refund flow tested
- [ ] Subscription flow tested

### Documentation
- [ ] API documentation updated
- [ ] Webhook events documented
- [ ] Error codes documented
- [ ] Refund policy documented
- [ ] Support procedures documented
```

---

## Additional Resources

- [Stripe Documentation](https://stripe.com/docs/api)
- [Stripe Node.js Library](https://github.com/stripe/stripe-node)
- [Stripe Python Library](https://github.com/stripe/stripe-python)
- [PCI DSS Requirements](https://www.pcisecuritystandards.org/)
- [Stripe Best Practices](https://stripe.com/docs/security/best-practices)
