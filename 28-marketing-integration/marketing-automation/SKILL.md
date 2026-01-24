---
name: Marketing Automation
description: Streamlining, automating, and measuring marketing tasks and workflows to enable personalized customer engagement at scale through segmentation, behavioral triggers, and automated campaigns.
---

# Marketing Automation

> **Current Level:** Intermediate  
> **Domain:** Marketing / Automation

---

## Overview

Marketing automation enables businesses to streamline, automate, and measure marketing tasks and workflows, allowing for personalized customer engagement at scale. Effective marketing automation uses segmentation, behavioral triggers, lead scoring, and automated workflows to engage customers at the right time with the right message.

---

## Core Concepts

### Table of Contents

1. [Marketing Automation Concepts](#marketing-automation-concepts)
2. [User Segmentation](#user-segmentation)
3. [Behavioral Triggers](#behavioral-triggers)
4. [Email Sequences/Drip Campaigns](#email-sequencesdrip-campaigns)
5. [Lead Scoring](#lead-scoring)
6. [Workflow Automation](#workflow-automation)
7. [Event Tracking](#event-tracking)
8. [Integration with CRM](#integration-with-crm)
9. [Platforms](#platforms)
10. [Custom Automation Engine](#custom-automation-engine)
11. [Testing Automation Flows](#testing-automation-flows)
12. [Analytics and Optimization](#analytics-and-optimization)

---

## Marketing Automation Concepts

### Core Components

```typescript
// Core automation entities
interface AutomationWorkflow {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'paused' | 'draft';
  triggers: Trigger[];
  actions: Action[];
  conditions?: Condition[];
  createdAt: Date;
  updatedAt: Date;
}

interface Trigger {
  id: string;
  type: 'event' | 'schedule' | 'segment_entry' | 'segment_exit';
  config: Record<string, any>;
}

interface Action {
  id: string;
  type: 'send_email' | 'add_tag' | 'remove_tag' | 'update_field' | 'webhook' | 'wait';
  config: Record<string, any>;
  delay?: number; // in seconds
}

interface Condition {
  id: string;
  type: 'if_else' | 'branch';
  config: Record<string, any>;
  trueActions: Action[];
  falseActions?: Action[];
}

// Automation execution context
interface ExecutionContext {
  workflowId: string;
  userId: string;
  triggerEvent: Event;
  variables: Record<string, any>;
  executionHistory: ExecutionStep[];
}

interface ExecutionStep {
  actionId: string;
  status: 'pending' | 'running' | 'completed' | 'failed' | 'skipped';
  startedAt?: Date;
  completedAt?: Date;
  error?: string;
  result?: any;
}
```

### Automation Types

```typescript
enum AutomationType {
  // Welcome series
  WELCOME = 'welcome',
  
  // Onboarding flows
  ONBOARDING = 'onboarding',
  
  // Re-engagement campaigns
  RE_ENGAGEMENT = 're_engagement',
  
  // Abandoned cart
  ABANDONED_CART = 'abandoned_cart',
  
  // Post-purchase
  POST_PURCHASE = 'post_purchase',
  
  // Birthday campaigns
  BIRTHDAY = 'birthday',
  
  // Lead nurturing
  LEAD_NURTURING = 'lead_nurturing',
  
  // Product recommendations
  RECOMMENDATIONS = 'recommendations',
  
  // Cross-sell/upsell
  CROSS_SELL = 'cross_sell',
  UPSELL = 'upsell',
}
```

---

## User Segmentation

### Segment Definition

```typescript
interface Segment {
  id: string;
  name: string;
  description: string;
  type: 'static' | 'dynamic';
  rules: SegmentRule[];
  userCount: number;
  createdAt: Date;
  updatedAt: Date;
}

interface SegmentRule {
  field: string;
  operator: 'equals' | 'not_equals' | 'contains' | 'not_contains' | 'greater_than' | 'less_than' | 'in' | 'not_in' | 'is_set' | 'is_not_set';
  value: any;
  logicalOperator?: 'AND' | 'OR';
}

// Segment engine
class SegmentEngine {
  async evaluateUser(userId: string, segment: Segment): Promise<boolean> {
    const user = await this.getUserData(userId);
    
    if (segment.type === 'static') {
      return await this.isInStaticSegment(userId, segment.id);
    }
    
    return this.evaluateRules(user, segment.rules);
  }
  
  private evaluateRules(user: any, rules: SegmentRule[]): boolean {
    let result = true;
    let currentOperator: 'AND' | 'OR' = 'AND';
    
    for (const rule of rules) {
      const ruleResult = this.evaluateRule(user, rule);
      
      if (currentOperator === 'AND') {
        result = result && ruleResult;
      } else {
        result = result || ruleResult;
      }
      
      currentOperator = rule.logicalOperator || 'AND';
    }
    
    return result;
  }
  
  private evaluateRule(user: any, rule: SegmentRule): boolean {
    const fieldValue = this.getFieldValue(user, rule.field);
    
    switch (rule.operator) {
      case 'equals':
        return fieldValue === rule.value;
      case 'not_equals':
        return fieldValue !== rule.value;
      case 'contains':
        return String(fieldValue).includes(rule.value);
      case 'not_contains':
        return !String(fieldValue).includes(rule.value);
      case 'greater_than':
        return Number(fieldValue) > Number(rule.value);
      case 'less_than':
        return Number(fieldValue) < Number(rule.value);
      case 'in':
        return Array.isArray(rule.value) && rule.value.includes(fieldValue);
      case 'not_in':
        return Array.isArray(rule.value) && !rule.value.includes(fieldValue);
      case 'is_set':
        return fieldValue !== null && fieldValue !== undefined;
      case 'is_not_set':
        return fieldValue === null || fieldValue === undefined;
      default:
        return false;
    }
  }
  
  private getFieldValue(user: any, field: string): any {
    return field.split('.').reduce((obj, key) => obj?.[key], user);
  }
  
  async getUserData(userId: string): Promise<any> {
    // Fetch user data from database
    return await db.user.findUnique({
      where: { id: userId },
      include: {
        profile: true,
        subscription: true,
        orders: true,
      },
    });
  }
  
  async isInStaticSegment(userId: string, segmentId: string): Promise<boolean> {
    const membership = await db.segmentMembership.findUnique({
      where: {
        userId_segmentId: { userId, segmentId },
      },
    });
    return !!membership;
  }
}
```

### Common Segments

```typescript
// Pre-defined segment templates
const segmentTemplates = {
  // Active users (last 30 days)
  activeUsers: {
    name: 'Active Users',
    type: 'dynamic',
    rules: [
      {
        field: 'lastLoginAt',
        operator: 'greater_than',
        value: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
      },
    ],
  },
  
  // Churned users (no activity in 90 days)
  churnedUsers: {
    name: 'Churned Users',
    type: 'dynamic',
    rules: [
      {
        field: 'lastLoginAt',
        operator: 'less_than',
        value: new Date(Date.now() - 90 * 24 * 60 * 60 * 1000).toISOString(),
      },
    ],
  },
  
  // High-value customers (spent > $500)
  highValueCustomers: {
    name: 'High-Value Customers',
    type: 'dynamic',
    rules: [
      {
        field: 'totalSpent',
        operator: 'greater_than',
        value: 500,
      },
    ],
  },
  
  // New users (signed up in last 7 days)
  newUsers: {
    name: 'New Users',
    type: 'dynamic',
    rules: [
      {
        field: 'createdAt',
        operator: 'greater_than',
        value: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString(),
      },
    ],
  },
  
  // Trial users
  trialUsers: {
    name: 'Trial Users',
    type: 'dynamic',
    rules: [
      {
        field: 'subscription.plan',
        operator: 'equals',
        value: 'trial',
      },
    ],
  },
  
  // Paid subscribers
  paidSubscribers: {
    name: 'Paid Subscribers',
    type: 'dynamic',
    rules: [
      {
        field: 'subscription.status',
        operator: 'equals',
        value: 'active',
        logicalOperator: 'AND',
      },
      {
        field: 'subscription.plan',
        operator: 'not_equals',
        value: 'trial',
      },
    ],
  },
  
  // Cart abandoners
  cartAbandoners: {
    name: 'Cart Abandoners',
    type: 'dynamic',
    rules: [
      {
        field: 'cart.items',
        operator: 'is_set',
        value: null,
      },
      {
        field: 'cart.updatedAt',
        operator: 'greater_than',
        value: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
        logicalOperator: 'AND',
      },
    ],
  },
};
```

---

## Behavioral Triggers

### Event Types

```typescript
interface Event {
  id: string;
  type: string;
  userId: string;
  properties: Record<string, any>;
  timestamp: Date;
  context?: {
    ip?: string;
    userAgent?: string;
    url?: string;
  };
}

// Common event types
enum EventType {
  // User lifecycle
  USER_SIGNED_UP = 'user.signed_up',
  USER_LOGGED_IN = 'user.logged_in',
  USER_PROFILE_UPDATED = 'user.profile_updated',
  
  // Engagement
  PAGE_VIEWED = 'page.viewed',
  ARTICLE_VIEWED = 'article.viewed',
  VIDEO_WATCHED = 'video.watched',
  BUTTON_CLICKED = 'button.clicked',
  FORM_SUBMITTED = 'form.submitted',
  
  // E-commerce
  PRODUCT_VIEWED = 'product.viewed',
  PRODUCT_ADDED_TO_CART = 'product.added_to_cart',
  CART_ABANDONED = 'cart.abandoned',
  ORDER_COMPLETED = 'order.completed',
  ORDER_REFUNDED = 'order.refunded',
  
  // Subscription
  SUBSCRIPTION_STARTED = 'subscription.started',
  SUBSCRIPTION_CANCELLED = 'subscription.cancelled',
  SUBSCRIPTION_UPGRADED = 'subscription.upgraded',
  
  // Content
  EMAIL_OPENED = 'email.opened',
  EMAIL_CLICKED = 'email.clicked',
  PUSH_OPENED = 'push.opened',
}

// Event tracking
class EventTracker {
  async track(event: Event): Promise<void> {
    // Store event
    await db.event.create({
      data: {
        id: event.id,
        type: event.type,
        userId: event.userId,
        properties: event.properties,
        timestamp: event.timestamp,
        context: event.context,
      },
    });
    
    // Check for matching triggers
    await this.checkTriggers(event);
  }
  
  async checkTriggers(event: Event): Promise<void> {
    const triggers = await db.trigger.findMany({
      where: {
        eventType: event.type,
        workflow: {
          status: 'active',
        },
      },
    });
    
    for (const trigger of triggers) {
      if (this.matchesTrigger(event, trigger)) {
        await this.executeWorkflow(trigger.workflowId, event);
      }
    }
  }
  
  private matchesTrigger(event: Event, trigger: any): boolean {
    // Check trigger conditions
    if (trigger.conditions) {
      return this.evaluateConditions(event.properties, trigger.conditions);
    }
    return true;
  }
  
  private evaluateConditions(properties: any, conditions: any): boolean {
    // Implement condition evaluation logic
    return true;
  }
}
```

### Trigger Configuration

```typescript
// Trigger examples
const triggerExamples = {
  // User signs up
  userSignUp: {
    type: 'event',
    eventType: EventType.USER_SIGNED_UP,
    conditions: {
      // Optional: only trigger for certain user types
      'user.type': { equals: 'customer' },
    },
  },
  
  // Cart abandoned
  cartAbandoned: {
    type: 'event',
    eventType: EventType.CART_ABANDONED,
    conditions: {
      'cart.total': { greater_than: 50 },
    },
  },
  
  // Purchase completed
  purchaseCompleted: {
    type: 'event',
    eventType: EventType.ORDER_COMPLETED,
    conditions: {
      'order.total': { greater_than: 100 },
    },
  },
  
  // Scheduled trigger
  scheduledEmail: {
    type: 'schedule',
    schedule: '0 9 * * *', // Cron expression: 9 AM daily
    timezone: 'America/New_York',
  },
  
  // Segment entry trigger
  segmentEntry: {
    type: 'segment_entry',
    segmentId: 'high_value_customers',
  },
  
  // Email opened
  emailOpened: {
    type: 'event',
    eventType: EventType.EMAIL_OPENED,
    conditions: {
      'email.campaignId': { equals: 'welcome_series' },
    },
  },
};
```

---

## Email Sequences/Drip Campaigns

### Drip Campaign Structure

```typescript
interface DripCampaign {
  id: string;
  name: string;
  type: AutomationType;
  status: 'active' | 'paused' | 'draft';
  emails: DripEmail[];
  trigger: Trigger;
  createdAt: Date;
}

interface DripEmail {
  id: string;
  templateId: string;
  subject: string;
  delay: number; // in seconds from previous email
  conditions?: Condition[];
}

// Drip campaign manager
class DripCampaignManager {
  async startCampaign(userId: string, campaign: DripCampaign): Promise<void> {
    // Create campaign enrollment
    const enrollment = await db.campaignEnrollment.create({
      data: {
        userId,
        campaignId: campaign.id,
        currentEmailIndex: 0,
        status: 'active',
        startedAt: new Date(),
      },
    });
    
    // Schedule first email
    await this.scheduleEmail(enrollment.id, campaign.emails[0], 0);
  }
  
  async scheduleEmail(
    enrollmentId: string,
    email: DripEmail,
    delaySeconds: number
  ): Promise<void> {
    const scheduledFor = new Date(Date.now() + delaySeconds * 1000);
    
    await db.scheduledEmail.create({
      data: {
        enrollmentId,
        emailId: email.id,
        templateId: email.templateId,
        subject: email.subject,
        scheduledFor,
        status: 'scheduled',
      },
    });
  }
  
  async processScheduledEmails(): Promise<void> {
    const dueEmails = await db.scheduledEmail.findMany({
      where: {
        scheduledFor: { lte: new Date() },
        status: 'scheduled',
      },
      include: {
        enrollment: {
          include: {
            user: true,
            campaign: true,
          },
        },
      },
    });
    
    for (const scheduledEmail of dueEmails) {
      await this.sendEmail(scheduledEmail);
    }
  }
  
  async sendEmail(scheduledEmail: any): Promise<void> {
    const { enrollment, templateId, subject } = scheduledEmail;
    
    // Check conditions
    const campaign = await db.dripCampaign.findUnique({
      where: { id: enrollment.campaignId },
      include: { emails: true },
    });
    
    const emailConfig = campaign!.emails[enrollment.currentEmailIndex];
    if (emailConfig.conditions) {
      const conditionsMet = await this.evaluateConditions(
        enrollment.user,
        emailConfig.conditions
      );
      
      if (!conditionsMet) {
        // Skip this email, move to next
        await this.moveToNextEmail(enrollment.id);
        return;
      }
    }
    
    // Send email
    await emailService.send({
      to: enrollment.user.email,
      subject,
      templateId,
      dynamicTemplateData: {
        userName: enrollment.user.name,
        // Add more personalization
      },
    });
    
    // Update status
    await db.scheduledEmail.update({
      where: { id: scheduledEmail.id },
      data: {
        status: 'sent',
        sentAt: new Date(),
      },
    });
    
    // Schedule next email
    await this.moveToNextEmail(enrollment.id);
  }
  
  async moveToNextEmail(enrollmentId: string): Promise<void> {
    const enrollment = await db.campaignEnrollment.findUnique({
      where: { id: enrollmentId },
      include: { campaign: { include: { emails: true } } },
    });
    
    const nextIndex = enrollment!.currentEmailIndex + 1;
    
    if (nextIndex >= enrollment!.campaign.emails.length) {
      // Campaign completed
      await db.campaignEnrollment.update({
        where: { id: enrollmentId },
        data: {
          status: 'completed',
          completedAt: new Date(),
        },
      });
      return;
    }
    
    const nextEmail = enrollment!.campaign.emails[nextIndex];
    await db.campaignEnrollment.update({
      where: { id: enrollmentId },
      data: { currentEmailIndex: nextIndex },
    });
    
    await this.scheduleEmail(
      enrollmentId,
      nextEmail,
      nextEmail.delay
    );
  }
}
```

### Welcome Series Example

```typescript
const welcomeSeries: DripCampaign = {
  id: 'welcome_series',
  name: 'Welcome Series',
  type: AutomationType.WELCOME,
  status: 'active',
  trigger: {
    type: 'event',
    eventType: EventType.USER_SIGNED_UP,
  },
  emails: [
    {
      id: 'welcome_1',
      templateId: 'welcome_email_1',
      subject: 'Welcome to Our App! 🎉',
      delay: 0, // Send immediately
    },
    {
      id: 'welcome_2',
      templateId: 'welcome_email_2',
      subject: 'Getting Started Guide',
      delay: 24 * 60 * 60, // 1 day later
    },
    {
      id: 'welcome_3',
      templateId: 'welcome_email_3',
      subject: 'Tips and Tricks',
      delay: 48 * 60 * 60, // 2 days after email 2
    },
    {
      id: 'welcome_4',
      templateId: 'welcome_email_4',
      subject: 'How are you doing?',
      delay: 72 * 60 * 60, // 3 days after email 3
    },
  ],
};
```

---

## Lead Scoring

### Lead Scoring Model

```typescript
interface LeadScoringRule {
  id: string;
  name: string;
  type: 'behavioral' | 'demographic' | 'firmographic';
  condition: any;
  points: number;
  maxOccurrences?: number;
}

interface LeadScore {
  userId: string;
  totalScore: number;
  behavioralScore: number;
  demographicScore: number;
  firmographicScore: number;
  lastUpdated: Date;
}

// Lead scoring engine
class LeadScoringEngine {
  private rules: LeadScoringRule[] = [];
  
  constructor(rules: LeadScoringRule[]) {
    this.rules = rules;
  }
  
  async calculateScore(userId: string): Promise<LeadScore> {
    const user = await this.getUserData(userId);
    const events = await this.getUserEvents(userId);
    
    let behavioralScore = 0;
    let demographicScore = 0;
    let firmographicScore = 0;
    
    for (const rule of this.rules) {
      let score = 0;
      
      switch (rule.type) {
        case 'behavioral':
          score = this.calculateBehavioralScore(user, events, rule);
          behavioralScore += score;
          break;
        case 'demographic':
          score = this.calculateDemographicScore(user, rule);
          demographicScore += score;
          break;
        case 'firmographic':
          score = this.calculateFirmographicScore(user, rule);
          firmographicScore += score;
          break;
      }
    }
    
    const totalScore = behavioralScore + demographicScore + firmographicScore;
    
    return {
      userId,
      totalScore,
      behavioralScore,
      demographicScore,
      firmographicScore,
      lastUpdated: new Date(),
    };
  }
  
  private calculateBehavioralScore(user: any, events: Event[], rule: LeadScoringRule): number {
    let occurrences = 0;
    
    for (const event of events) {
      if (this.matchesCondition(event, rule.condition)) {
        occurrences++;
        
        if (rule.maxOccurrences && occurrences >= rule.maxOccurrences) {
          break;
        }
      }
    }
    
    return occurrences * rule.points;
  }
  
  private calculateDemographicScore(user: any, rule: LeadScoringRule): number {
    if (this.matchesCondition(user, rule.condition)) {
      return rule.points;
    }
    return 0;
  }
  
  private calculateFirmographicScore(user: any, rule: LeadScoringRule): number {
    if (this.matchesCondition(user.company, rule.condition)) {
      return rule.points;
    }
    return 0;
  }
  
  private matchesCondition(data: any, condition: any): boolean {
    // Implement condition matching logic
    return true;
  }
  
  async getUserData(userId: string): Promise<any> {
    return await db.user.findUnique({
      where: { id: userId },
      include: {
        profile: true,
        company: true,
      },
    });
  }
  
  async getUserEvents(userId: string): Promise<Event[]> {
    return await db.event.findMany({
      where: { userId },
      orderBy: { timestamp: 'desc' },
      take: 1000,
    });
  }
}
```

### Lead Scoring Rules

```typescript
const leadScoringRules: LeadScoringRule[] = [
  // Behavioral scoring
  {
    id: 'page_visit',
    name: 'Page Visit',
    type: 'behavioral',
    condition: { type: EventType.PAGE_VIEWED },
    points: 1,
    maxOccurrences: 50,
  },
  {
    id: 'product_view',
    name: 'Product View',
    type: 'behavioral',
    condition: { type: EventType.PRODUCT_VIEWED },
    points: 5,
    maxOccurrences: 20,
  },
  {
    id: 'add_to_cart',
    name: 'Add to Cart',
    type: 'behavioral',
    condition: { type: EventType.PRODUCT_ADDED_TO_CART },
    points: 10,
    maxOccurrences: 10,
  },
  {
    id: 'email_open',
    name: 'Email Open',
    type: 'behavioral',
    condition: { type: EventType.EMAIL_OPENED },
    points: 2,
    maxOccurrences: 30,
  },
  {
    id: 'email_click',
    name: 'Email Click',
    type: 'behavioral',
    condition: { type: EventType.EMAIL_CLICKED },
    points: 5,
    maxOccurrences: 20,
  },
  {
    id: 'form_submit',
    name: 'Form Submit',
    type: 'behavioral',
    condition: { type: EventType.FORM_SUBMITTED },
    points: 15,
    maxOccurrences: 5,
  },
  
  // Demographic scoring
  {
    id: 'job_title',
    name: 'Decision Maker',
    type: 'demographic',
    condition: { 'profile.jobTitle': { in: ['CEO', 'CTO', 'VP', 'Director'] } },
    points: 20,
  },
  {
    id: 'company_size',
    name: 'Large Company',
    type: 'demographic',
    condition: { 'company.size': { greater_than: 100 } },
    points: 15,
  },
  {
    id: 'industry',
    name: 'Target Industry',
    type: 'demographic',
    condition: { 'company.industry': { in: ['Technology', 'Finance', 'Healthcare'] } },
    points: 10,
  },
  
  // Firmographic scoring
  {
    id: 'revenue',
    name: 'High Revenue',
    type: 'firmographic',
    condition: { 'company.revenue': { greater_than: 10000000 } },
    points: 25,
  },
  {
    id: 'location',
    name: 'Target Location',
    type: 'firmographic',
    condition: { 'company.country': { in: ['US', 'UK', 'CA'] } },
    points: 10,
  },
];

// Lead qualification thresholds
const leadThresholds = {
  hot: 80,
  warm: 50,
  cold: 0,
};

function qualifyLead(score: number): 'hot' | 'warm' | 'cold' {
  if (score >= leadThresholds.hot) return 'hot';
  if (score >= leadThresholds.warm) return 'warm';
  return 'cold';
}
```

---

## Workflow Automation

### Workflow Engine

```typescript
class WorkflowEngine {
  async executeWorkflow(workflowId: string, triggerEvent: Event): Promise<void> {
    const workflow = await db.automationWorkflow.findUnique({
      where: { id: workflowId },
      include: { triggers: true, actions: true },
    });
    
    if (!workflow || workflow.status !== 'active') {
      return;
    }
    
    // Create execution context
    const context: ExecutionContext = {
      workflowId,
      userId: triggerEvent.userId,
      triggerEvent,
      variables: this.extractVariables(triggerEvent),
      executionHistory: [],
    };
    
    // Execute actions sequentially
    for (const action of workflow.actions) {
      await this.executeAction(context, action);
    }
  }
  
  private async executeAction(
    context: ExecutionContext,
    action: Action
  ): Promise<void> {
    const step: ExecutionStep = {
      actionId: action.id,
      status: 'pending',
    };
    
    context.executionHistory.push(step);
    
    // Apply delay if specified
    if (action.delay) {
      await this.delay(action.delay * 1000);
    }
    
    step.status = 'running';
    step.startedAt = new Date();
    
    try {
      const result = await this.performAction(context, action);
      
      step.status = 'completed';
      step.completedAt = new Date();
      step.result = result;
      
      // Update context variables
      if (result) {
        context.variables = { ...context.variables, ...result };
      }
    } catch (error) {
      step.status = 'failed';
      step.completedAt = new Date();
      step.error = (error as Error).message;
      
      // Log error
      console.error(`Action ${action.id} failed:`, error);
    }
  }
  
  private async performAction(
    context: ExecutionContext,
    action: Action
  ): Promise<any> {
    switch (action.type) {
      case 'send_email':
        return await this.sendEmailAction(context, action);
      case 'add_tag':
        return await this.addTagAction(context, action);
      case 'remove_tag':
        return await this.removeTagAction(context, action);
      case 'update_field':
        return await this.updateFieldAction(context, action);
      case 'webhook':
        return await this.webhookAction(context, action);
      case 'wait':
        return await this.waitAction(context, action);
      default:
        throw new Error(`Unknown action type: ${action.type}`);
    }
  }
  
  private async sendEmailAction(
    context: ExecutionContext,
    action: Action
  ): Promise<any> {
    const { to, templateId, subject } = action.config;
    
    await emailService.send({
      to: this.resolveValue(to, context),
      templateId,
      subject: this.resolveValue(subject, context),
      dynamicTemplateData: context.variables,
    });
  }
  
  private async addTagAction(
    context: ExecutionContext,
    action: Action
  ): Promise<any> {
    const { tag } = action.config;
    
    await db.userTag.create({
      data: {
        userId: context.userId,
        tag: this.resolveValue(tag, context),
      },
    });
  }
  
  private async removeTagAction(
    context: ExecutionContext,
    action: Action
  ): Promise<any> {
    const { tag } = action.config;
    
    await db.userTag.deleteMany({
      where: {
        userId: context.userId,
        tag: this.resolveValue(tag, context),
      },
    });
  }
  
  private async updateFieldAction(
    context: ExecutionContext,
    action: Action
  ): Promise<any> {
    const { field, value } = action.config;
    
    await db.user.update({
      where: { id: context.userId },
      data: {
        [field]: this.resolveValue(value, context),
      },
    });
  }
  
  private async webhookAction(
    context: ExecutionContext,
    action: Action
  ): Promise<any> {
    const { url, method, headers, body } = action.config;
    
    const response = await fetch(this.resolveValue(url, context), {
      method: method || 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...headers,
      },
      body: JSON.stringify(this.resolveValue(body, context)),
    });
    
    return await response.json();
  }
  
  private async waitAction(
    context: ExecutionContext,
    action: Action
  ): Promise<any> {
    const { duration } = action.config;
    await this.delay(duration * 1000);
  }
  
  private resolveValue(value: any, context: ExecutionContext): any {
    if (typeof value === 'string' && value.startsWith('{{') && value.endsWith('}}')) {
      const key = value.slice(2, -2).trim();
      return context.variables[key];
    }
    return value;
  }
  
  private extractVariables(event: Event): Record<string, any> {
    return {
      userId: event.userId,
      eventType: event.type,
      ...event.properties,
    };
  }
  
  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

---

## Event Tracking

### Event Tracking Implementation

```typescript
// Frontend event tracking
class EventTracker {
  private queue: Event[] = [];
  private flushInterval: number = 5000; // 5 seconds
  private batchSize: number = 10;
  
  constructor(private apiUrl: string) {
    this.startFlushInterval();
  }
  
  track(eventName: string, properties: Record<string, any> = {}): void {
    const event: Event = {
      id: this.generateId(),
      type: eventName,
      userId: this.getUserId(),
      properties,
      timestamp: new Date(),
      context: {
        url: window.location.href,
        userAgent: navigator.userAgent,
      },
    };
    
    this.queue.push(event);
    
    if (this.queue.length >= this.batchSize) {
      this.flush();
    }
  }
  
  private async flush(): Promise<void> {
    if (this.queue.length === 0) return;
    
    const events = [...this.queue];
    this.queue = [];
    
    try {
      await fetch(`${this.apiUrl}/events/batch`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ events }),
      });
    } catch (error) {
      // Re-queue failed events
      this.queue.unshift(...events);
    }
  }
  
  private startFlushInterval(): void {
    setInterval(() => this.flush(), this.flushInterval);
  }
  
  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }
  
  private getUserId(): string {
    // Get user ID from cookie, localStorage, or session
    return localStorage.getItem('userId') || 'anonymous';
  }
}

// Usage
const tracker = new EventTracker('/api/analytics');

tracker.track('button_clicked', {
  buttonId: 'signup-button',
  page: '/landing',
});

tracker.track('product_viewed', {
  productId: '12345',
  productName: 'Product Name',
  category: 'Electronics',
});
```

### Backend Event Handler

```typescript
import express from 'express';

const app = express();

app.post('/events/batch', express.json(), async (req, res) => {
  const { events } = req.body;
  
  // Store events
  await db.event.createMany({
    data: events,
  });
  
  // Process events for automation
  for (const event of events) {
    await eventTracker.track(event);
  }
  
  res.status(200).json({ received: events.length });
});

// Get user events
app.get('/events/:userId', async (req, res) => {
  const { userId } = req.params;
  const { limit = 100, type } = req.query;
  
  const events = await db.event.findMany({
    where: {
      userId,
      ...(type && { type: type as string }),
    },
    orderBy: { timestamp: 'desc' },
    take: Number(limit),
  });
  
  res.json({ events });
});
```

---

## Integration with CRM

### CRM Integration

```typescript
interface CRMConfig {
  provider: 'hubspot' | 'salesforce' | 'pipedrive';
  apiKey: string;
  baseUrl: string;
}

class CRMIntegration {
  constructor(private config: CRMConfig) {}
  
  async syncUser(userId: string): Promise<void> {
    const user = await db.user.findUnique({
      where: { id: userId },
      include: {
        profile: true,
        company: true,
        subscription: true,
      },
    });
    
    const crmContact = this.mapUserToContact(user!);
    
    switch (this.config.provider) {
      case 'hubspot':
        await this.syncToHubSpot(crmContact);
        break;
      case 'salesforce':
        await this.syncToSalesforce(crmContact);
        break;
      case 'pipedrive':
        await this.syncToPipedrive(crmContact);
        break;
    }
  }
  
  private mapUserToContact(user: any): any {
    return {
      email: user.email,
      firstName: user.profile?.firstName,
      lastName: user.profile?.lastName,
      company: user.company?.name,
      phone: user.profile?.phone,
      website: user.company?.website,
      customFields: {
        userId: user.id,
        subscriptionPlan: user.subscription?.plan,
        subscriptionStatus: user.subscription?.status,
        totalSpent: user.totalSpent,
      },
    };
  }
  
  private async syncToHubSpot(contact: any): Promise<void> {
    const response = await fetch(`${this.config.baseUrl}/crm/v3/objects/contacts`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        properties: {
          email: contact.email,
          firstname: contact.firstName,
          lastname: contact.lastName,
          company: contact.company,
          phone: contact.phone,
          website: contact.website,
          ...contact.customFields,
        },
      }),
    });
    
    const data = await response.json();
    
    // Store CRM contact ID
    await db.user.update({
      where: { id: contact.customFields.userId },
      data: { hubspotContactId: data.id },
    });
  }
  
  private async syncToSalesforce(contact: any): Promise<void> {
    // Salesforce integration
  }
  
  private async syncToPipedrive(contact: any): Promise<void> {
    // Pipedrive integration
  }
  
  async trackActivity(userId: string, activity: {
    type: string;
    description: string;
    metadata?: Record<string, any>;
  }): Promise<void> {
    const user = await db.user.findUnique({
      where: { id: userId },
    });
    
    switch (this.config.provider) {
      case 'hubspot':
        await this.createHubSpotActivity(user!.hubspotContactId, activity);
        break;
      case 'salesforce':
        await this.createSalesforceActivity(user!.salesforceContactId, activity);
        break;
      case 'pipedrive':
        await this.createPipedriveActivity(user!.pipedriveContactId, activity);
        break;
    }
  }
  
  private async createHubSpotActivity(contactId: string, activity: any): Promise<void> {
    await fetch(`${this.config.baseUrl}/crm/v3/objects/engagements`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.config.apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        engagement: {
          type: activity.type,
        },
        associations: [
          {
            to: { id: contactId },
            types: [{ associationCategory: 'HUBSPOT_DEFINED', associationTypeId: 1 }],
          },
        ],
        metadata: {
          body: activity.description,
          ...activity.metadata,
        },
      }),
    });
  }
}
```

---

## Platforms

### HubSpot Integration

```typescript
// npm install @hubspot/api-client
import { Client } from '@hubspot/api-client';

const hubspotClient = new Client({
  apiKey: process.env.HUBSPOT_API_KEY,
});

// Create contact
async function createHubSpotContact(contact: {
  email: string;
  firstName?: string;
  lastName?: string;
  company?: string;
}): Promise<string> {
  const response = await hubspotClient.crm.contacts.basicApi.create({
    properties: {
      email: contact.email,
      firstname: contact.firstName || '',
      lastname: contact.lastName || '',
      company: contact.company || '',
    },
  });
  
  return response.id;
}

// Update contact
async function updateHubSpotContact(
  contactId: string,
  properties: Record<string, string>
): Promise<void> {
  await hubspotClient.crm.contacts.basicApi.update(contactId, {
    properties,
  });
}

// Add to list
async function addContactToList(
  contactId: string,
  listId: string
): Promise<void> {
  await hubspotClient.crm.lists.listsApi.addContactsToList(listId, [contactId]);
}

// Get contact
async function getHubSpotContact(contactId: string): Promise<any> {
  const response = await hubspotClient.crm.contacts.basicApi.getById(contactId);
  return response.properties;
}

// Create deal
async function createHubSpotDeal(deal: {
  dealname: string;
  amount?: number;
  dealstage?: string;
  closedate?: string;
}): Promise<string> {
  const response = await hubspotClient.crm.deals.basicApi.create({
    properties: {
      dealname: deal.dealname,
      amount: deal.amount?.toString(),
      dealstage: deal.dealstage || 'appointmentscheduled',
      closedate: deal.closedate,
    },
  });
  
  return response.id;
}

// Associate contact with deal
async function associateContactWithDeal(
  contactId: string,
  dealId: string
): Promise<void> {
  await hubspotClient.crm.deals.associationsApi.create(
    dealId,
    'contact',
    contactId
  );
}
```

### ActiveCampaign Integration

```typescript
// npm install activecampaign
import ActiveCampaign from 'activecampaign';

const ac = new ActiveCampaign(
  process.env.ACTIVECAMPAIGN_API_URL!,
  process.env.ACTIVECAMPAIGN_API_KEY!
);

// Sync contact
async function syncContact(contact: {
  email: string;
  firstName?: string;
  lastName?: string;
  phone?: string;
}): Promise<string> {
  const response = await ac.contacts.create({
    contact: {
      email: contact.email,
      firstName: contact.firstName,
      lastName: contact.lastName,
      phone: contact.phone,
    },
  });
  
  return response.contact.id;
}

// Add tag
async function addTag(contactId: string, tag: string): Promise<void> {
  const tags = await ac.tags.list();
  const existingTag = tags.tags.find((t: any) => t.tag === tag);
  
  if (!existingTag) {
    await ac.tags.create({ tag });
  }
  
  await ac.contacts.tagContact({
    contact: contactId,
    tag: tag,
  });
}

// Add to automation
async function addToAutomation(
  contactId: string,
  automationId: string
): Promise<void> {
  await ac.contacts.addContactAutomation({
    contact: contactId,
    automation: automationId,
  });
}

// Track event
async function trackEvent(
  contactId: string,
  eventName: string,
  eventData?: Record<string, any>
): Promise<void> {
  await ac.tracking.log({
    event: eventName,
    eventdata: eventData,
    contactid: contactId,
  });
}
```

### Customer.io Integration

```typescript
// npm install customerio
import { TrackAPI, Region } from 'customerio-node';

const cio = new TrackAPI(
  process.env.CUSTOMERIO_SITE_ID!,
  process.env.CUSTOMERIO_API_KEY!,
  { region: Region.US }
);

// Identify user
async function identifyUser(user: {
  id: string;
  email: string;
  name?: string;
  [key: string]: any;
}): Promise<void> {
  await cio.identify(user.id, {
    email: user.email,
    name: user.name,
    ...user,
  });
}

// Track event
async function trackCustomerIOEvent(
  userId: string,
  eventName: string,
  attributes?: Record<string, any>
): Promise<void> {
  await cio.track(userId, {
    name: eventName,
    data: attributes,
  });
}

// Trigger campaign
async function triggerCampaign(
  campaignId: string,
  userId: string,
  data?: Record<string, any>
): Promise<void> {
  await cio.triggerCampaign(campaignId, {
    recipients: [{ id: userId }],
    data,
  });
}
```

---

## Custom Automation Engine

### Database Schema

```sql
-- Automation workflows
CREATE TABLE automation_workflows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) NOT NULL DEFAULT 'draft',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Triggers
CREATE TABLE triggers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id UUID REFERENCES automation_workflows(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,
  event_type VARCHAR(255),
  schedule VARCHAR(100),
  segment_id UUID,
  conditions JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Actions
CREATE TABLE actions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id UUID REFERENCES automation_workflows(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL,
  config JSONB NOT NULL,
  delay_seconds INTEGER DEFAULT 0,
  order_index INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Workflow executions
CREATE TABLE workflow_executions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  workflow_id UUID REFERENCES automation_workflows(id) ON DELETE CASCADE,
  user_id UUID NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'running',
  started_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  error_message TEXT
);

-- Execution steps
CREATE TABLE execution_steps (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  execution_id UUID REFERENCES workflow_executions(id) ON DELETE CASCADE,
  action_id UUID REFERENCES actions(id),
  status VARCHAR(50) NOT NULL DEFAULT 'pending',
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  error_message TEXT,
  result JSONB
);

-- Segments
CREATE TABLE segments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  type VARCHAR(50) NOT NULL DEFAULT 'dynamic',
  rules JSONB NOT NULL,
  user_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Segment memberships
CREATE TABLE segment_memberships (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  segment_id UUID REFERENCES segments(id) ON DELETE CASCADE,
  user_id UUID NOT NULL,
  added_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(segment_id, user_id)
);

-- Drip campaigns
CREATE TABLE drip_campaigns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50) NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'draft',
  trigger_id UUID REFERENCES triggers(id),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Drip campaign emails
CREATE TABLE drip_emails (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES drip_campaigns(id) ON DELETE CASCADE,
  template_id VARCHAR(255) NOT NULL,
  subject VARCHAR(500) NOT NULL,
  delay_seconds INTEGER NOT NULL,
  conditions JSONB,
  order_index INTEGER NOT NULL
);

-- Campaign enrollments
CREATE TABLE campaign_enrollments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES drip_campaigns(id) ON DELETE CASCADE,
  user_id UUID NOT NULL,
  current_email_index INTEGER DEFAULT 0,
  status VARCHAR(50) NOT NULL DEFAULT 'active',
  started_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP
);

-- Scheduled emails
CREATE TABLE scheduled_emails (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  enrollment_id UUID REFERENCES campaign_enrollments(id) ON DELETE CASCADE,
  email_id UUID REFERENCES drip_emails(id),
  template_id VARCHAR(255) NOT NULL,
  subject VARCHAR(500) NOT NULL,
  scheduled_for TIMESTAMP NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'scheduled',
  sent_at TIMESTAMP
);
```

---

## Testing Automation Flows

### Test Framework

```typescript
class AutomationTester {
  async testWorkflow(workflowId: string, testUserId: string): Promise<TestResult> {
    const workflow = await db.automationWorkflow.findUnique({
      where: { id: workflowId },
      include: { triggers: true, actions: true },
    });
    
    const result: TestResult = {
      workflowId,
      testUserId,
      passed: true,
      steps: [],
      errors: [],
    };
    
    // Create test event
    const testEvent: Event = {
      id: 'test-event',
      type: workflow!.triggers[0].eventType || 'test.event',
      userId: testUserId,
      properties: { test: true },
      timestamp: new Date(),
    };
    
    // Execute workflow
    try {
      await workflowEngine.executeWorkflow(workflowId, testEvent);
    } catch (error) {
      result.passed = false;
      result.errors.push((error as Error).message);
    }
    
    // Check execution
    const execution = await db.workflowExecution.findFirst({
      where: {
        workflowId,
        userId: testUserId,
      },
      include: { steps: true },
    });
    
    if (execution) {
      for (const step of execution.steps) {
        result.steps.push({
          actionId: step.actionId,
          status: step.status,
          error: step.error_message,
        });
        
        if (step.status === 'failed') {
          result.passed = false;
          result.errors.push(step.error_message || 'Unknown error');
        }
      }
    }
    
    return result;
  }
  
  async testSegment(segmentId: string, testUserId: string): Promise<boolean> {
    const segment = await db.segment.findUnique({
      where: { id: segmentId },
    });
    
    const engine = new SegmentEngine();
    return await engine.evaluateUser(testUserId, segment!);
  }
}

interface TestResult {
  workflowId: string;
  testUserId: string;
  passed: boolean;
  steps: Array<{
    actionId: string;
    status: string;
    error?: string;
  }>;
  errors: string[];
}
```

---

## Analytics and Optimization

### Campaign Analytics

```typescript
interface CampaignAnalytics {
  workflowId: string;
  totalEnrollments: number;
  completions: number;
  dropoffs: number;
  conversionRate: number;
  averageTimeToComplete: number;
  stepMetrics: StepMetric[];
}

interface StepMetric {
  actionId: string;
  executed: number;
  completed: number;
  failed: number;
  skipped: number;
  averageExecutionTime: number;
}

async function getWorkflowAnalytics(workflowId: string): Promise<CampaignAnalytics> {
  const executions = await db.workflowExecution.findMany({
    where: { workflowId },
    include: { steps: true },
  });
  
  const totalEnrollments = executions.length;
  const completions = executions.filter(e => e.status === 'completed').length;
  const dropoffs = totalEnrollments - completions;
  const conversionRate = totalEnrollments > 0 ? (completions / totalEnrollments) * 100 : 0;
  
  const totalTime = executions.reduce((sum, e) => {
    if (e.completed_at && e.started_at) {
      return sum + (e.completed_at.getTime() - e.started_at.getTime());
    }
    return sum;
  }, 0);
  
  const averageTimeToComplete = completions > 0 ? totalTime / completions : 0;
  
  // Calculate step metrics
  const stepMetricsMap = new Map<string, StepMetric>();
  
  for (const execution of executions) {
    for (const step of execution.steps) {
      if (!stepMetricsMap.has(step.actionId)) {
        stepMetricsMap.set(step.actionId, {
          actionId: step.actionId,
          executed: 0,
          completed: 0,
          failed: 0,
          skipped: 0,
          averageExecutionTime: 0,
        });
      }
      
      const metric = stepMetricsMap.get(step.actionId)!;
      metric.executed++;
      
      switch (step.status) {
        case 'completed':
          metric.completed++;
          if (step.started_at && step.completed_at) {
            metric.averageExecutionTime += step.completed_at.getTime() - step.started_at.getTime();
          }
          break;
        case 'failed':
          metric.failed++;
          break;
        case 'skipped':
          metric.skipped++;
          break;
      }
    }
  }
  
  // Calculate averages
  const stepMetrics = Array.from(stepMetricsMap.values()).map(metric => ({
    ...metric,
    averageExecutionTime: metric.completed > 0 ? metric.averageExecutionTime / metric.completed : 0,
  }));
  
  return {
    workflowId,
    totalEnrollments,
    completions,
    dropoffs,
    conversionRate,
    averageTimeToComplete,
    stepMetrics,
  };
}
```

---

## Resources

- [HubSpot API Documentation](https://developers.hubspot.com/)
- [ActiveCampaign API Documentation](https://developers.activecampaign.com/)
- [Customer.io Documentation](https://customer.io/docs/)
- [Marketing Automation Best Practices](https://blog.hubspot.com/marketing/marketing-automation)

## Best Practices

### Workflow Design

- **Keep workflows simple**: Complex workflows are harder to maintain
- **Use clear naming**: Descriptive names for workflows and actions
- **Document triggers**: Make it clear what starts each workflow
- **Test before activating**: Verify workflows work in staging
- **Monitor execution**: Track workflow performance and failures

### Segmentation

- **Use dynamic segments**: Auto-update based on user behavior
- **Keep segment rules simple**: Avoid overly complex logic
- **Limit segment size**: Large segments impact performance
- **Regularly review segments**: Remove outdated segments
- **Use meaningful names**: Make segments easy to understand

### Trigger Configuration

- **Use specific event types**: Avoid overly broad triggers
- **Add conditions**: Filter triggers to reduce false positives
- **Set appropriate delays**: Time actions for optimal engagement
- **Test trigger logic**: Verify triggers fire correctly
- **Document trigger requirements**: Clear documentation for users

### Email Sequences

- **Space emails appropriately**: Don't overwhelm recipients
- **Personalize content**: Use recipient data effectively
- **Include value in each email**: Each email should be useful
- **Test sequence flow**: Verify emails arrive in order
- **Monitor engagement**: Track opens, clicks, and conversions

### Lead Scoring

- **Balance scoring rules**: Don't overweight any single factor
- **Update scores regularly**: Keep scores current with recent activity
- **Use multiple criteria**: Behavioral, demographic, and firmographic
- **Set appropriate thresholds**: Define hot/warm/cold lead stages
- **Review scoring effectiveness**: Adjust rules based on conversion rates

### CRM Integration

- **Keep data synchronized**: Ensure CRM reflects latest user data
- **Handle sync failures**: Implement retry and error handling
- **Map fields correctly**: Ensure data maps to CRM fields properly
- **Respect rate limits**: Don't overwhelm CRM APIs
- **Use webhooks for updates**: Real-time CRM updates

### Event Tracking

- **Track meaningful events**: Focus on business-critical events
- **Use consistent naming**: Standardize event names
- **Include context**: Add metadata for better analysis
- **Batch event sending**: Reduce API calls
- **Handle tracking failures**: Don't lose events on errors

### Testing and Validation

- **Test workflows end-to-end**: Verify complete user journeys
- **Use test users**: Dedicated test accounts for validation
- **Test edge cases**: Verify unusual scenarios
- **Monitor test results**: Track test execution and outcomes
- **Document test procedures**: Clear testing guidelines

### Analytics and Optimization

- **Track key metrics**: Monitor engagement, conversion, and retention
- **Set up dashboards**: Visualize automation performance
- **Analyze drop-off points**: Identify where users disengage
- **A/B test content**: Optimize subject lines and content
- **Iterate continuously**: Improve based on data

### Compliance and Privacy

- **Obtain consent**: Get permission for marketing communications
- **Provide opt-out**: Easy unsubscribe mechanisms
- **Honor preferences**: Respect user communication preferences
- **Secure user data**: Protect PII and sensitive information
- **Comply with regulations**: GDPR, CAN-SPAM, and other laws

## Checklist

### Workflow Design
- [ ] Define workflow objectives
- [ ] Identify trigger events
- [ ] Design workflow steps
- [ ] Configure actions and delays
- [ ] Test workflow logic

### Segmentation
- [ ] Define segment criteria
- [ ] Create segment rules
- [ ] Test segment logic
- [ ] Monitor segment sizes
- [ ] Review segment performance

### Trigger Setup
- [ ] Choose trigger types
- [ ] Configure event filters
- [ ] Set up conditions
- [ ] Test trigger firing
- [ ] Document trigger requirements

### Email Sequences
- [ ] Design email flow
- [ ] Create email templates
- [ ] Set up delays
- [ ] Personalize content
- [ ] Test sequence timing

### Lead Scoring
- [ ] Define scoring criteria
- [ ] Create scoring rules
- [ ] Set point values
- [ ] Configure thresholds
- [ ] Monitor scoring accuracy

### CRM Integration
- [ ] Choose CRM platform
- [ ] Configure API credentials
- [ ] Map data fields
- [ ] Set up sync schedules
- [ ] Test data synchronization

### Event Tracking
- [ ] Define event schema
- [ ] Implement tracking SDK
- [ ] Configure event batching
- [ ] Set up event endpoints
- [ ] Test event delivery

### Testing
- [ ] Create test accounts
- [ ] Write test scenarios
- [ ] Test workflow execution
- [ ] Validate segment logic
- [ ] Test email rendering

### Analytics
- [ ] Define KPIs
- [ ] Set up tracking
- [ ] Create dashboards
- [ ] Configure alerts
- [ ] Schedule performance reviews

### Compliance
- [ ] Implement consent tracking
- [ ] Add unsubscribe mechanisms
- [ ] Configure data retention
- [ ] Document privacy policy
- [ ] Set up GDPR compliance

### Production
- [ ] Configure production environment
- [ ] Set up monitoring
- [ ] Configure error handling
- [ ] Document runbooks
- [ ] Train team on procedures
```

---

## Quick Start

### Basic Automation Workflow

```javascript
// User segmentation
const segment = await segmentUser(userId)
if (segment === 'high-value') {
  await triggerWorkflow('welcome-premium', userId)
} else {
  await triggerWorkflow('welcome-standard', userId)
}

// Behavioral trigger
eventEmitter.on('user:abandoned-cart', async (userId) => {
  await delay(24 * 60 * 60 * 1000)  // 24 hours
  const cart = await getCart(userId)
  if (cart.items.length > 0) {
    await sendEmail('cart-reminder', userId, { cart })
  }
})
```

---

## Production Checklist

- [ ] **Segmentation**: User segmentation configured
- [ ] **Triggers**: Behavioral triggers set up
- [ ] **Workflows**: Automation workflows created
- [ ] **Email Templates**: Email templates designed
- [ ] **Lead Scoring**: Lead scoring rules configured
- [ ] **CRM Integration**: CRM integration working
- [ ] **Testing**: Test automation flows
- [ ] **Monitoring**: Monitor automation performance
- [ ] **Analytics**: Track automation metrics
- [ ] **Compliance**: GDPR and consent tracking
- [ ] **Documentation**: Document automation rules
- [ ] **Optimization**: A/B test automation flows

---

## Anti-patterns

### ❌ Don't: Spam Users

```javascript
// ❌ Bad - Too many emails
user.actions.forEach(action => {
  sendEmail(`action-${action}`, userId)  // Spam!
})
```

```javascript
// ✅ Good - Rate limiting
const lastEmail = await getLastEmailSent(userId)
if (Date.now() - lastEmail > 24 * 60 * 60 * 1000) {
  sendEmail('summary', userId, { actions })
}
```

### ❌ Don't: No Personalization

```javascript
// ❌ Bad - Generic emails
sendEmail('welcome', userId, {})  // No personalization
```

```javascript
// ✅ Good - Personalized
const user = await getUser(userId)
sendEmail('welcome', userId, {
  name: user.name,
  preferences: user.preferences
})
```

---

## Integration Points

- **Email Marketing** (`28-marketing-integration/email-marketing/`) - Email campaigns
- **CRM Integration** (`32-crm-integration/`) - Lead management
- **Analytics** (`23-business-analytics/`) - Campaign analytics

---

## Further Reading

- [Marketing Automation Best Practices](https://www.hubspot.com/marketing-automation)
- [Customer Journey Mapping](https://www.salesforce.com/resources/articles/customer-journey-mapping/)
