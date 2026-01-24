---
name: Marketing Campaign Management
description: Planning, executing, tracking, and analyzing marketing campaigns across multiple channels to achieve business objectives and maximize return on investment with proper budget management and performance metrics.
---

# Marketing Campaign Management

> **Current Level:** Intermediate  
> **Domain:** Marketing / Analytics

---

## Overview

Campaign management involves planning, executing, tracking, and analyzing marketing campaigns across multiple channels to achieve business objectives and maximize return on investment. Effective campaign management includes budget allocation, performance tracking, ROI calculation, and multi-channel coordination.

---

## Core Concepts

### Table of Contents

1. [Campaign Lifecycle](#campaign-lifecycle)
2. [Campaign Planning](#campaign-planning)
3. [Multi-Channel Campaigns](#multi-channel-campaigns)
4. [Campaign Tracking System](#campaign-tracking-system)
5. [Budget Management](#budget-management)
6. [Performance Metrics](#performance-metrics)
7. [ROI Calculation](#roi-calculation)
8. [Database Schema for Campaigns](#database-schema-for-campaigns)
9. [Reporting Dashboards](#reporting-dashboards)
10. [Integration with Analytics](#integration-with-analytics)
11. [Automation](#automation)
12. [Best Practices](#best-practices)

---

## Campaign Lifecycle

### Campaign States

```typescript
enum CampaignStatus {
  DRAFT = 'draft',
  SCHEDULED = 'scheduled',
  ACTIVE = 'active',
  PAUSED = 'paused',
  COMPLETED = 'completed',
  CANCELLED = 'cancelled',
}

enum CampaignType {
  EMAIL = 'email',
  SOCIAL = 'social',
  PAID_SEARCH = 'paid_search',
  DISPLAY = 'display',
  INFLUENCER = 'influencer',
  AFFILIATE = 'affiliate',
  CONTENT = 'content',
  EVENT = 'event',
  MULTICHANNEL = 'multichannel',
}

interface Campaign {
  id: string;
  name: string;
  description: string;
  type: CampaignType;
  status: CampaignStatus;
  startDate: Date;
  endDate: Date;
  budget: number;
  actualSpend: number;
  targetAudience: string[];
  channels: string[];
  objectives: string[];
  kpis: KPIMetric[];
  createdAt: Date;
  updatedAt: Date;
}

interface KPIMetric {
  name: string;
  target: number;
  current: number;
  unit: string;
}
```

### Lifecycle Management

```typescript
class CampaignLifecycle {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create new campaign
   */
  async createCampaign(campaign: Omit<Campaign, 'id' | 'actualSpend' | 'createdAt' | 'updatedAt'>): Promise<string> {
    const created = await this.prisma.campaign.create({
      data: {
        ...campaign,
        actualSpend: 0,
        createdAt: new Date(),
        updatedAt: new Date(),
      },
    });

    return created.id;
  }

  /**
   * Launch campaign
   */
  async launchCampaign(campaignId: string): Promise<void> {
    const campaign = await this.prisma.campaign.findUnique({
      where: { id: campaignId },
    });

    if (!campaign) {
      throw new Error('Campaign not found');
    }

    if (campaign.status !== CampaignStatus.DRAFT && campaign.status !== CampaignStatus.SCHEDULED) {
      throw new Error('Campaign must be in draft or scheduled status');
    }

    if (campaign.startDate > new Date()) {
      // Schedule for future launch
      await this.prisma.campaign.update({
        where: { id: campaignId },
        data: { status: CampaignStatus.SCHEDULED },
      });

      // Schedule launch job
      await this.scheduleCampaignLaunch(campaignId, campaign.startDate);
    } else {
      // Launch immediately
      await this.prisma.campaign.update({
        where: { id: campaignId },
        data: { status: CampaignStatus.ACTIVE },
      });

      // Execute campaign
      await this.executeCampaign(campaignId);
    }
  }

  /**
   * Pause campaign
   */
  async pauseCampaign(campaignId: string, reason?: string): Promise<void> {
    await this.prisma.campaign.update({
      where: { id: campaignId },
      data: {
        status: CampaignStatus.PAUSED,
        pauseReason: reason,
        pausedAt: new Date(),
      },
    });

    // Stop campaign execution
    await this.stopCampaignExecution(campaignId);
  }

  /**
   * Resume campaign
   */
  async resumeCampaign(campaignId: string): Promise<void> {
    const campaign = await this.prisma.campaign.findUnique({
      where: { id: campaignId },
    });

    if (!campaign || campaign.status !== CampaignStatus.PAUSED) {
      throw new Error('Campaign must be paused to resume');
    }

    await this.prisma.campaign.update({
      where: { id: campaignId },
      data: {
        status: CampaignStatus.ACTIVE,
        pauseReason: null,
        pausedAt: null,
      },
    });

    // Resume campaign execution
    await this.resumeCampaignExecution(campaignId);
  }

  /**
   * Complete campaign
   */
  async completeCampaign(campaignId: string): Promise<void> {
    await this.prisma.campaign.update({
      where: { id: campaignId },
      data: {
        status: CampaignStatus.COMPLETED,
        completedAt: new Date(),
      },
    });

    // Generate final report
    await this.generateCampaignReport(campaignId);
  }

  /**
   * Cancel campaign
   */
  async cancelCampaign(campaignId: string, reason: string): Promise<void> {
    await this.prisma.campaign.update({
      where: { id: campaignId },
      data: {
        status: CampaignStatus.CANCELLED,
        cancelReason: reason,
        cancelledAt: new Date(),
      },
    });

    // Stop all campaign activities
    await this.stopCampaignExecution(campaignId);
  }

  private async scheduleCampaignLaunch(campaignId: string, launchDate: Date): Promise<void> {
    // Implement scheduling logic
  }

  private async executeCampaign(campaignId: string): Promise<void> {
    // Implement campaign execution logic
  }

  private async stopCampaignExecution(campaignId: string): Promise<void> {
    // Implement stop logic
  }

  private async resumeCampaignExecution(campaignId: string): Promise<void> {
    // Implement resume logic
  }

  private async generateCampaignReport(campaignId: string): Promise<void> {
    // Implement report generation
  }
}
```

---

## Campaign Planning

### Campaign Planner

```typescript
interface CampaignPlan {
  name: string;
  objectives: string[];
  targetAudience: {
    demographics: Record<string, any>;
    psychographics: Record<string, any>;
    behaviors: Record<string, any>;
  };
  channels: ChannelPlan[];
  timeline: {
    startDate: Date;
    endDate: Date;
    milestones: Milestone[];
  };
  budget: BudgetAllocation;
  kpis: KPIMetric[];
  content: ContentPlan[];
  risks: Risk[];
}

interface ChannelPlan {
  channel: string;
  budget: number;
  tactics: Tactic[];
  targetMetrics: Record<string, number>;
}

interface Tactic {
  name: string;
  description: string;
  startDate: Date;
  endDate: Date;
  budget: number;
  expectedResults: Record<string, number>;
}

interface Milestone {
  name: string;
  date: Date;
  deliverables: string[];
}

interface BudgetAllocation {
  total: number;
  allocations: Record<string, number>;
  contingency: number;
}

interface ContentPlan {
  type: string;
  title: string;
  description: string;
  channel: string;
  publishDate: Date;
  status: 'planned' | 'in_progress' | 'completed' | 'published';
}

interface Risk {
  description: string;
  probability: 'low' | 'medium' | 'high';
  impact: 'low' | 'medium' | 'high';
  mitigation: string;
}

class CampaignPlanner {
  /**
   * Validate campaign plan
   */
  validatePlan(plan: CampaignPlan): {
    valid: boolean;
    errors: string[];
    warnings: string[];
  } {
    const errors: string[] = [];
    const warnings: string[] = [];

    // Check objectives
    if (!plan.objectives || plan.objectives.length === 0) {
      errors.push('Campaign must have at least one objective');
    }

    // Check timeline
    if (plan.timeline.endDate <= plan.timeline.startDate) {
      errors.push('End date must be after start date');
    }

    // Check budget
    const allocatedBudget = Object.values(plan.budget.allocations).reduce((sum, v) => sum + v, 0);
    if (allocatedBudget + plan.budget.contingency > plan.budget.total) {
      errors.push('Budget allocation exceeds total budget');
    }

    // Check channels
    if (!plan.channels || plan.channels.length === 0) {
      warnings.push('Campaign has no channels defined');
    }

    // Check KPIs
    if (!plan.kpis || plan.kpis.length === 0) {
      warnings.push('Campaign has no KPIs defined');
    }

    return {
      valid: errors.length === 0,
      errors,
      warnings,
    };
  }

  /**
   * Estimate campaign performance
   */
  estimatePerformance(plan: CampaignPlan): {
    expectedReach: number;
    expectedImpressions: number;
    expectedClicks: number;
    expectedConversions: number;
    expectedCPM: number;
    expectedCPC: number;
    expectedCPA: number;
  } {
    const totalBudget = plan.budget.total;

    // Channel-specific estimates
    let totalReach = 0;
    let totalImpressions = 0;
    let totalClicks = 0;

    for (const channel of plan.channels) {
      const channelEstimates = this.getChannelEstimates(channel);
      totalReach += channelEstimates.reach;
      totalImpressions += channelEstimates.impressions;
      totalClicks += channelEstimates.clicks;
    }

    // Calculate metrics
    const expectedCPM = (totalBudget / totalImpressions) * 1000;
    const expectedCPC = totalBudget / totalClicks;
    const expectedConversions = totalClicks * 0.02; // 2% conversion rate assumption
    const expectedCPA = totalBudget / expectedConversions;

    return {
      expectedReach,
      expectedImpressions,
      expectedClicks,
      expectedConversions,
      expectedCPM,
      expectedCPC,
      expectedCPA,
    };
  }

  private getChannelEstimates(channel: ChannelPlan): {
    reach: number;
    impressions: number;
    clicks: number;
  } {
    // Simplified channel estimates
    const estimates: Record<string, { cpm: number; ctr: number }> = {
      facebook: { cpm: 10, ctr: 0.02 },
      google_search: { cpm: 20, ctr: 0.05 },
      instagram: { cpm: 8, ctr: 0.015 },
      linkedin: { cpm: 25, ctr: 0.03 },
      email: { cpm: 0, ctr: 0.03 },
    };

    const estimate = estimates[channel.channel] || { cpm: 10, ctr: 0.02 };
    const impressions = (channel.budget / estimate.cpm) * 1000;
    const clicks = impressions * estimate.ctr;
    const reach = impressions * 0.3; // 30% unique reach assumption

    return { reach, impressions, clicks };
  }
}
```

---

## Multi-Channel Campaigns

### Multi-Channel Coordinator

```typescript
interface MultiChannelCampaign {
  campaignId: string;
  channels: ChannelCampaign[];
  syncRules: SyncRule[];
  crossChannelAttribution: AttributionModel;
}

interface ChannelCampaign {
  channelId: string;
  platform: 'facebook' | 'google' | 'email' | 'instagram' | 'linkedin';
  config: Record<string, any>;
  status: 'pending' | 'active' | 'paused' | 'completed';
  metrics: ChannelMetrics;
}

interface ChannelMetrics {
  impressions: number;
  clicks: number;
  conversions: number;
  spend: number;
  revenue: number;
}

interface SyncRule {
  trigger: string;
  actions: SyncAction[];
}

interface SyncAction {
  targetChannel: string;
  action: string;
  config: Record<string, any>;
}

class MultiChannelCoordinator {
  constructor(private prisma: PrismaClient) {}

  /**
   * Launch multi-channel campaign
   */
  async launchCampaign(campaign: MultiChannelCampaign): Promise<void> {
    // Validate all channels are ready
    await this.validateChannels(campaign.channels);

    // Launch channels in sequence or parallel
    for (const channel of campaign.channels) {
      await this.launchChannel(channel);
    }

    // Set up sync rules
    await this.setupSyncRules(campaign.syncRules);

    // Start monitoring
    await this.startMonitoring(campaign.campaignId);
  }

  /**
   * Sync campaign data across channels
   */
  async syncCampaignData(campaignId: string, eventType: string, data: any): Promise<void> {
    const campaign = await this.getCampaign(campaignId);

    for (const rule of campaign.syncRules) {
      if (rule.trigger === eventType) {
        for (const action of rule.actions) {
          await this.executeSyncAction(action, data);
        }
      }
    }
  }

  /**
   * Aggregate cross-channel metrics
   */
  async getAggregatedMetrics(campaignId: string): Promise<{
    totalImpressions: number;
    totalClicks: number;
    totalConversions: number;
    totalSpend: number;
    totalRevenue: number;
    averageCTR: number;
    averageCVR: number;
    averageROAS: number;
    byChannel: Record<string, ChannelMetrics>;
  }> {
    const campaign = await this.getCampaign(campaignId);

    let totalImpressions = 0;
    let totalClicks = 0;
    let totalConversions = 0;
    let totalSpend = 0;
    let totalRevenue = 0;

    const byChannel: Record<string, ChannelMetrics> = {};

    for (const channel of campaign.channels) {
      totalImpressions += channel.metrics.impressions;
      totalClicks += channel.metrics.clicks;
      totalConversions += channel.metrics.conversions;
      totalSpend += channel.metrics.spend;
      totalRevenue += channel.metrics.revenue;

      byChannel[channel.channelId] = channel.metrics;
    }

    const averageCTR = totalImpressions > 0 ? (totalClicks / totalImpressions) * 100 : 0;
    const averageCVR = totalClicks > 0 ? (totalConversions / totalClicks) * 100 : 0;
    const averageROAS = totalSpend > 0 ? totalRevenue / totalSpend : 0;

    return {
      totalImpressions,
      totalClicks,
      totalConversions,
      totalSpend,
      totalRevenue,
      averageCTR,
      averageCVR,
      averageROAS,
      byChannel,
    };
  }

  private async validateChannels(channels: ChannelCampaign[]): Promise<void> {
    for (const channel of channels) {
      // Validate channel configuration
      if (!channel.config || Object.keys(channel.config).length === 0) {
        throw new Error(`Channel ${channel.channelId} has no configuration`);
      }
    }
  }

  private async launchChannel(channel: ChannelCampaign): Promise<void> {
    switch (channel.platform) {
      case 'facebook':
        await this.launchFacebookCampaign(channel);
        break;
      case 'google':
        await this.launchGoogleCampaign(channel);
        break;
      case 'email':
        await this.launchEmailCampaign(channel);
        break;
      default:
        throw new Error(`Unsupported platform: ${channel.platform}`);
    }
  }

  private async launchFacebookCampaign(channel: ChannelCampaign): Promise<void> {
    // Implement Facebook campaign launch
  }

  private async launchGoogleCampaign(channel: ChannelCampaign): Promise<void> {
    // Implement Google Ads campaign launch
  }

  private async launchEmailCampaign(channel: ChannelCampaign): Promise<void> {
    // Implement email campaign launch
  }

  private async setupSyncRules(rules: SyncRule[]): Promise<void> {
    // Implement sync rule setup
  }

  private async executeSyncAction(action: SyncAction, data: any): Promise<void> {
    // Implement sync action execution
  }

  private async startMonitoring(campaignId: string): Promise<void> {
    // Implement monitoring setup
  }

  private async getCampaign(campaignId: string): Promise<MultiChannelCampaign> {
    // Implement campaign retrieval
    return {} as MultiChannelCampaign;
  }
}
```

---

## Campaign Tracking System

### Tracking Implementation

```typescript
interface CampaignEvent {
  id: string;
  campaignId: string;
  channelId?: string;
  userId?: string;
  sessionId: string;
  eventType: 'impression' | 'click' | 'conversion' | 'view';
  properties: Record<string, any>;
  value?: number;
  timestamp: Date;
}

class CampaignTracker {
  constructor(private prisma: PrismaClient) {}

  /**
   * Track impression
   */
  async trackImpression(params: {
    campaignId: string;
    channelId?: string;
    userId?: string;
    sessionId: string;
    properties?: Record<string, any>;
  }): Promise<void> {
    await this.trackEvent({
      eventType: 'impression',
      ...params,
    });
  }

  /**
   * Track click
   */
  async trackClick(params: {
    campaignId: string;
    channelId?: string;
    userId?: string;
    sessionId: string;
    properties?: Record<string, any>;
  }): Promise<void> {
    await this.trackEvent({
      eventType: 'click',
      ...params,
    });
  }

  /**
   * Track conversion
   */
  async trackConversion(params: {
    campaignId: string;
    channelId?: string;
    userId?: string;
    sessionId: string;
    conversionType: string;
    value?: number;
    properties?: Record<string, any>;
  }): Promise<void> {
    await this.trackEvent({
      eventType: 'conversion',
      value: params.value,
      properties: {
        ...params.properties,
        conversionType: params.conversionType,
      },
      campaignId: params.campaignId,
      channelId: params.channelId,
      userId: params.userId,
      sessionId: params.sessionId,
    });
  }

  /**
   * Get campaign events
   */
  async getEvents(params: {
    campaignId: string;
    eventType?: CampaignEvent['eventType'];
    startDate?: Date;
    endDate?: Date;
    limit?: number;
  }): Promise<CampaignEvent[]> {
    const where: any = { campaignId: params.campaignId };

    if (params.eventType) {
      where.eventType = params.eventType;
    }

    if (params.startDate || params.endDate) {
      where.timestamp = {};
      if (params.startDate) where.timestamp.gte = params.startDate;
      if (params.endDate) where.timestamp.lte = params.endDate;
    }

    return await this.prisma.campaignEvent.findMany({
      where,
      orderBy: { timestamp: 'desc' },
      take: params.limit,
    });
  }

  /**
   * Get funnel data
   */
  async getFunnelData(campaignId: string): Promise<{
    impressions: number;
    clicks: number;
    conversions: number;
    clickThroughRate: number;
    conversionRate: number;
  }> {
    const [impressions, clicks, conversions] = await Promise.all([
      this.prisma.campaignEvent.count({
        where: { campaignId, eventType: 'impression' },
      }),
      this.prisma.campaignEvent.count({
        where: { campaignId, eventType: 'click' },
      }),
      this.prisma.campaignEvent.count({
        where: { campaignId, eventType: 'conversion' },
      }),
    ]);

    const clickThroughRate = impressions > 0 ? (clicks / impressions) * 100 : 0;
    const conversionRate = clicks > 0 ? (conversions / clicks) * 100 : 0;

    return {
      impressions,
      clicks,
      conversions,
      clickThroughRate,
      conversionRate,
    };
  }

  private async trackEvent(event: Omit<CampaignEvent, 'id' | 'timestamp'>): Promise<void> {
    await this.prisma.campaignEvent.create({
      data: {
        ...event,
        timestamp: new Date(),
      },
    });
  }
}
```

---

## Budget Management

### Budget Manager

```typescript
interface BudgetAllocation {
  campaignId: string;
  totalBudget: number;
  allocated: number;
  spent: number;
  remaining: number;
  allocations: ChannelAllocation[];
}

interface ChannelAllocation {
  channelId: string;
  allocated: number;
  spent: number;
  remaining: number;
  percentage: number;
}

class BudgetManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Allocate budget to campaign
   */
  async allocateBudget(params: {
    campaignId: string;
    totalBudget: number;
    allocations: Record<string, number>; // channelId -> amount
  }): Promise<void> {
    const totalAllocated = Object.values(params.allocations).reduce((sum, v) => sum + v, 0);

    if (totalAllocated > params.totalBudget) {
      throw new Error('Allocations exceed total budget');
    }

    // Create budget allocation
    await this.prisma.budgetAllocation.create({
      data: {
        campaignId: params.campaignId,
        totalBudget: params.totalBudget,
        allocated: totalAllocated,
        spent: 0,
        remaining: params.totalBudget - totalAllocated,
      },
    });

    // Create channel allocations
    for (const [channelId, amount] of Object.entries(params.allocations)) {
      await this.prisma.channelAllocation.create({
        data: {
          campaignId: params.campaignId,
          channelId,
          allocated: amount,
          spent: 0,
          remaining: amount,
          percentage: (amount / totalAllocated) * 100,
        },
      });
    }
  }

  /**
   * Record spend
   */
  async recordSpend(params: {
    campaignId: string;
    channelId?: string;
    amount: number;
    description?: string;
  }): Promise<void> {
    // Update campaign budget
    await this.prisma.budgetAllocation.update({
      where: { campaignId: params.campaignId },
      data: {
        spent: { increment: params.amount },
        remaining: { decrement: params.amount },
      },
    });

    // Update channel budget if specified
    if (params.channelId) {
      await this.prisma.channelAllocation.update({
        where: {
          campaignId_channelId: {
            campaignId: params.campaignId,
            channelId: params.channelId,
          },
        },
        data: {
          spent: { increment: params.amount },
          remaining: { decrement: params.amount },
        },
      });
    }

    // Record spend transaction
    await this.prisma.budgetTransaction.create({
      data: {
        campaignId: params.campaignId,
        channelId: params.channelId,
        amount: params.amount,
        description: params.description,
        timestamp: new Date(),
      },
    });
  }

  /**
   * Get budget status
   */
  async getBudgetStatus(campaignId: string): Promise<BudgetAllocation> {
    const budget = await this.prisma.budgetAllocation.findUnique({
      where: { campaignId },
      include: { allocations: true },
    });

    if (!budget) {
      throw new Error('Budget allocation not found');
    }

    return {
      campaignId: budget.campaignId,
      totalBudget: budget.totalBudget,
      allocated: budget.allocated,
      spent: budget.spent,
      remaining: budget.remaining,
      allocations: budget.allocations.map(allocation => ({
        channelId: allocation.channelId,
        allocated: allocation.allocated,
        spent: allocation.spent,
        remaining: allocation.remaining,
        percentage: allocation.percentage,
      })),
    };
  }

  /**
   * Check budget alerts
   */
  async checkBudgetAlerts(campaignId: string): Promise<{
    hasAlerts: boolean;
    alerts: string[];
  }> {
    const budget = await this.getBudgetStatus(campaignId);
    const alerts: string[] = [];

    const spendPercentage = (budget.spent / budget.totalBudget) * 100;

    if (spendPercentage >= 100) {
      alerts.push('Budget exhausted');
    } else if (spendPercentage >= 90) {
      alerts.push('Budget at 90% capacity');
    } else if (spendPercentage >= 75) {
      alerts.push('Budget at 75% capacity');
    }

    for (const allocation of budget.allocations) {
      const channelSpendPercentage = (allocation.spent / allocation.allocated) * 100;
      if (channelSpendPercentage >= 100) {
        alerts.push(`Channel ${allocation.channelId} budget exhausted`);
      }
    }

    return {
      hasAlerts: alerts.length > 0,
      alerts,
    };
  }

  /**
   * Reallocate budget
   */
  async reallocateBudget(params: {
    campaignId: string;
    fromChannel: string;
    toChannel: string;
    amount: number;
  }): Promise<void> {
    // Check source channel has enough budget
    const fromAllocation = await this.prisma.channelAllocation.findUnique({
      where: {
        campaignId_channelId: {
          campaignId: params.campaignId,
          channelId: params.fromChannel,
        },
      },
    });

    if (!fromAllocation || fromAllocation.remaining < params.amount) {
      throw new Error('Insufficient budget in source channel');
    }

    // Transfer budget
    await this.prisma.$transaction([
      this.prisma.channelAllocation.update({
        where: {
          campaignId_channelId: {
            campaignId: params.campaignId,
            channelId: params.fromChannel,
          },
        },
        data: {
          allocated: { decrement: params.amount },
          remaining: { decrement: params.amount },
        },
      }),
      this.prisma.channelAllocation.update({
        where: {
          campaignId_channelId: {
            campaignId: params.campaignId,
            channelId: params.toChannel,
          },
        },
        data: {
          allocated: { increment: params.amount },
          remaining: { increment: params.amount },
        },
      }),
    ]);
  }
}
```

---

## Performance Metrics

### Metrics Calculator

```typescript
interface CampaignPerformance {
  campaignId: string;
  impressions: number;
  clicks: number;
  conversions: number;
  revenue: number;
  cost: number;
  ctr: number; // Click-through rate
  cpr: number; // Cost per result
  cpa: number; // Cost per acquisition
  roas: number; // Return on ad spend
  roi: number; // Return on investment
  conversionRate: number;
  averageOrderValue: number;
  customerLifetimeValue?: number;
}

class MetricsCalculator {
  /**
   * Calculate campaign performance
   */
  async calculatePerformance(campaignId: string): Promise<CampaignPerformance> {
    const [events, budget] = await Promise.all([
      this.getCampaignEvents(campaignId),
      this.getBudget(campaignId),
    ]);

    const impressions = events.filter(e => e.eventType === 'impression').length;
    const clicks = events.filter(e => e.eventType === 'click').length;
    const conversions = events.filter(e => e.eventType === 'conversion');
    const revenue = conversions.reduce((sum, c) => sum + (c.value || 0), 0);
    const cost = budget?.spent || 0;

    const ctr = impressions > 0 ? (clicks / impressions) * 100 : 0;
    const cpr = clicks > 0 ? cost / clicks : 0;
    const cpa = conversions.length > 0 ? cost / conversions.length : 0;
    const roas = cost > 0 ? revenue / cost : 0;
    const roi = cost > 0 ? ((revenue - cost) / cost) * 100 : 0;
    const conversionRate = clicks > 0 ? (conversions.length / clicks) * 100 : 0;
    const averageOrderValue = conversions.length > 0 ? revenue / conversions.length : 0;

    return {
      campaignId,
      impressions,
      clicks,
      conversions: conversions.length,
      revenue,
      cost,
      ctr,
      cpr,
      cpa,
      roas,
      roi,
      conversionRate,
      averageOrderValue,
    };
  }

  /**
   * Compare campaigns
   */
  async compareCampaigns(campaignIds: string[]): Promise<{
    best: CampaignPerformance;
    worst: CampaignPerformance;
    byMetric: Record<string, CampaignPerformance>;
  }> {
    const performances = await Promise.all(
      campaignIds.map(id => this.calculatePerformance(id))
    );

    const best = performances.reduce((a, b) => (b.roas > a.roas ? b : a));
    const worst = performances.reduce((a, b) => (b.roas < a.roas ? b : a));

    const byMetric: Record<string, CampaignPerformance> = {
      highestCTR: performances.reduce((a, b) => (b.ctr > a.ctr ? b : a)),
      lowestCPA: performances.reduce((a, b) => (b.cpa < a.cpa ? b : a)),
      highestROAS: performances.reduce((a, b) => (b.roas > a.roas ? b : a)),
      highestConversionRate: performances.reduce((a, b) => (b.conversionRate > a.conversionRate ? b : a)),
    };

    return { best, worst, byMetric };
  }

  /**
   * Calculate trend metrics
   */
  async calculateTrends(
    campaignId: string,
    period: 'day' | 'week' | 'month',
    startDate: Date,
    endDate: Date
  ): Promise<Array<{
    date: Date;
    impressions: number;
    clicks: number;
    conversions: number;
    revenue: number;
    cost: number;
    roas: number;
  }>> {
    const events = await this.getCampaignEvents(campaignId, startDate, endDate);

    // Group by period
    const grouped = new Map<string, {
      impressions: number;
      clicks: number;
      conversions: number;
      revenue: number;
      cost: number;
    }>();

    for (const event of events) {
      const key = this.getPeriodKey(event.timestamp, period);
      const existing = grouped.get(key) || {
        impressions: 0,
        clicks: 0,
        conversions: 0,
        revenue: 0,
        cost: 0,
      };

      switch (event.eventType) {
        case 'impression':
          existing.impressions++;
          break;
        case 'click':
          existing.clicks++;
          break;
        case 'conversion':
          existing.conversions++;
          existing.revenue += event.value || 0;
          break;
      }

      grouped.set(key, existing);
    }

    // Convert to array with ROAS
    return Array.from(grouped.entries()).map(([date, data]) => ({
      date: this.parsePeriodKey(date),
      ...data,
      roas: data.cost > 0 ? data.revenue / data.cost : 0,
    }));
  }

  private async getCampaignEvents(campaignId: string, startDate?: Date, endDate?: Date): Promise<CampaignEvent[]> {
    const where: any = { campaignId };

    if (startDate || endDate) {
      where.timestamp = {};
      if (startDate) where.timestamp.gte = startDate;
      if (endDate) where.timestamp.lte = endDate;
    }

    return await this.prisma.campaignEvent.findMany({ where });
  }

  private async getBudget(campaignId: string): Promise<{ spent: number } | null> {
    const budget = await this.prisma.budgetAllocation.findUnique({
      where: { campaignId },
    });
    return budget ? { spent: budget.spent } : null;
  }

  private getPeriodKey(date: Date, period: string): string {
    const d = new Date(date);
    switch (period) {
      case 'day':
        return d.toISOString().split('T')[0];
      case 'week':
        const weekStart = new Date(d);
        weekStart.setDate(d.getDate() - d.getDay());
        return weekStart.toISOString().split('T')[0];
      case 'month':
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
      default:
        return d.toISOString().split('T')[0];
    }
  }

  private parsePeriodKey(key: string): Date {
    return new Date(key);
  }
}
```

---

## ROI Calculation

### ROI Calculator

```typescript
interface ROICalculation {
  campaignId: string;
  revenue: number;
  cost: number;
  profit: number;
  roi: number; // Return on investment
  roas: number; // Return on ad spend
  paybackPeriod: number; // in days
  breakEvenPoint: number; // conversions needed
}

class ROICalculator {
  constructor(private prisma: PrismaClient) {}

  /**
   * Calculate ROI for campaign
   */
  async calculateROI(campaignId: string): Promise<ROICalculation> {
    const [revenue, cost, conversions, startDate] = await Promise.all([
      this.getTotalRevenue(campaignId),
      this.getTotalCost(campaignId),
      this.getTotalConversions(campaignId),
      this.getCampaignStartDate(campaignId),
    ]);

    const profit = revenue - cost;
    const roi = cost > 0 ? (profit / cost) * 100 : 0;
    const roas = cost > 0 ? revenue / cost : 0;

    const daysRunning = startDate
      ? Math.max(1, Math.floor((Date.now() - startDate.getTime()) / (1000 * 60 * 60 * 24)))
      : 1;
    const paybackPeriod = profit > 0 ? daysRunning : Infinity;

    const averageOrderValue = conversions > 0 ? revenue / conversions : 0;
    const breakEvenPoint = averageOrderValue > 0 ? Math.ceil(cost / averageOrderValue) : 0;

    return {
      campaignId,
      revenue,
      cost,
      profit,
      roi,
      roas,
      paybackPeriod,
      breakEvenPoint,
    };
  }

  /**
   * Calculate ROI across multiple campaigns
   */
  async calculateAggregateROI(campaignIds: string[]): Promise<{
    totalRevenue: number;
    totalCost: number;
    totalProfit: number;
    aggregateROI: number;
    aggregateROAS: number;
    byCampaign: ROICalculation[];
  }> {
    const calculations = await Promise.all(
      campaignIds.map(id => this.calculateROI(id))
    );

    const totalRevenue = calculations.reduce((sum, c) => sum + c.revenue, 0);
    const totalCost = calculations.reduce((sum, c) => sum + c.cost, 0);
    const totalProfit = totalRevenue - totalCost;
    const aggregateROI = totalCost > 0 ? (totalProfit / totalCost) * 100 : 0;
    const aggregateROAS = totalCost > 0 ? totalRevenue / totalCost : 0;

    return {
      totalRevenue,
      totalCost,
      totalProfit,
      aggregateROI,
      aggregateROAS,
      byCampaign: calculations,
    };
  }

  /**
   * Project ROI based on current performance
   */
  async projectROI(
    campaignId: string,
    remainingDays: number
  ): Promise<{
    projectedRevenue: number;
    projectedCost: number;
    projectedROI: number;
    projectedROAS: number;
  }> {
    const [currentROI, dailyMetrics] = await Promise.all([
      this.calculateROI(campaignId),
      this.getDailyMetrics(campaignId),
    ]);

    const daysRunning = currentROI.paybackPeriod === Infinity ? 1 : currentROI.paybackPeriod;
    const dailyRevenue = dailyMetrics.revenue;
    const dailyCost = dailyMetrics.cost;

    const projectedRevenue = currentROI.revenue + (dailyRevenue * remainingDays);
    const projectedCost = currentROI.cost + (dailyCost * remainingDays);
    const projectedProfit = projectedRevenue - projectedCost;
    const projectedROI = projectedCost > 0 ? (projectedProfit / projectedCost) * 100 : 0;
    const projectedROAS = projectedCost > 0 ? projectedRevenue / projectedCost : 0;

    return {
      projectedRevenue,
      projectedCost,
      projectedROI,
      projectedROAS,
    };
  }

  private async getTotalRevenue(campaignId: string): Promise<number> {
    const conversions = await this.prisma.campaignEvent.findMany({
      where: {
        campaignId,
        eventType: 'conversion',
      },
    });

    return conversions.reduce((sum, c) => sum + (c.value || 0), 0);
  }

  private async getTotalCost(campaignId: string): Promise<number> {
    const budget = await this.prisma.budgetAllocation.findUnique({
      where: { campaignId },
    });

    return budget?.spent || 0;
  }

  private async getTotalConversions(campaignId: string): Promise<number> {
    return await this.prisma.campaignEvent.count({
      where: {
        campaignId,
        eventType: 'conversion',
      },
    });
  }

  private async getCampaignStartDate(campaignId: string): Promise<Date | null> {
    const campaign = await this.prisma.campaign.findUnique({
      where: { id: campaignId },
    });

    return campaign?.startDate || null;
  }

  private async getDailyMetrics(campaignId: string): Promise<{
    revenue: number;
    cost: number;
  }> {
    const [roi, startDate] = await Promise.all([
      this.calculateROI(campaignId),
      this.getCampaignStartDate(campaignId),
    ]);

    if (!startDate) {
      return { revenue: 0, cost: 0 };
    }

    const daysRunning = Math.max(1, Math.floor((Date.now() - startDate.getTime()) / (1000 * 60 * 60 * 24)));

    return {
      revenue: roi.revenue / daysRunning,
      cost: roi.cost / daysRunning,
    };
  }
}
```

---

## Database Schema for Campaigns

```sql
-- Campaigns table
CREATE TABLE campaigns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  type VARCHAR(50) NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'draft',
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP NOT NULL,
  budget DECIMAL(12, 2) NOT NULL,
  actual_spend DECIMAL(12, 2) DEFAULT 0,
  target_audience JSONB,
  channels TEXT[],
  objectives TEXT[],
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  completed_at TIMESTAMP,
  paused_at TIMESTAMP,
  cancelled_at TIMESTAMP,
  pause_reason TEXT,
  cancel_reason TEXT
);

-- Campaign channels
CREATE TABLE campaign_channels (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
  channel_id VARCHAR(255) NOT NULL,
  platform VARCHAR(50) NOT NULL,
  config JSONB NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(campaign_id, channel_id)
);

-- Budget allocations
CREATE TABLE budget_allocations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
  total_budget DECIMAL(12, 2) NOT NULL,
  allocated DECIMAL(12, 2) NOT NULL,
  spent DECIMAL(12, 2) DEFAULT 0,
  remaining DECIMAL(12, 2) GENERATED ALWAYS AS (total_budget - spent) STORED,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Channel allocations
CREATE TABLE channel_allocations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
  channel_id VARCHAR(255) NOT NULL,
  allocated DECIMAL(12, 2) NOT NULL,
  spent DECIMAL(12, 2) DEFAULT 0,
  remaining DECIMAL(12, 2) GENERATED ALWAYS AS (allocated - spent) STORED,
  percentage DECIMAL(5, 2) GENERATED ALWAYS AS ((allocated / (SELECT total_budget FROM budget_allocations WHERE campaign_id = channel_allocations.campaign_id)) * 100) STORED,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(campaign_id, channel_id)
);

-- Budget transactions
CREATE TABLE budget_transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
  channel_id VARCHAR(255),
  amount DECIMAL(12, 2) NOT NULL,
  description TEXT,
  timestamp TIMESTAMP DEFAULT NOW()
);

-- Campaign events
CREATE TABLE campaign_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
  channel_id VARCHAR(255),
  user_id UUID,
  session_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(50) NOT NULL,
  properties JSONB,
  value DECIMAL(12, 2),
  timestamp TIMESTAMP DEFAULT NOW()
);

-- KPIs
CREATE TABLE campaign_kpis (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,
  target DECIMAL(12, 2) NOT NULL,
  current DECIMAL(12, 2) DEFAULT 0,
  unit VARCHAR(50),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Campaign content
CREATE TABLE campaign_content (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES campaigns(id) ON DELETE CASCADE,
  channel_id VARCHAR(255),
  content_type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  content_url VARCHAR(500),
  publish_date TIMESTAMP,
  status VARCHAR(50) NOT NULL DEFAULT 'planned',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_campaigns_status ON campaigns(status);
CREATE INDEX idx_campaigns_dates ON campaigns(start_date, end_date);
CREATE INDEX idx_campaign_events_campaign_id ON campaign_events(campaign_id);
CREATE INDEX idx_campaign_events_timestamp ON campaign_events(timestamp);
CREATE INDEX idx_campaign_events_type ON campaign_events(event_type);
CREATE INDEX idx_budget_transactions_campaign_id ON budget_transactions(campaign_id);
CREATE INDEX idx_budget_transactions_timestamp ON budget_transactions(timestamp);
```

---

## Reporting Dashboards

### Dashboard Data Provider

```typescript
interface DashboardData {
  summary: CampaignSummary;
  topCampaigns: CampaignPerformance[];
  trends: TrendData[];
  byChannel: ChannelPerformance[];
  kpis: KPIData[];
}

interface CampaignSummary {
  totalCampaigns: number;
  activeCampaigns: number;
  totalBudget: number;
  totalSpend: number;
  totalRevenue: number;
  averageROI: number;
  averageROAS: number;
}

interface TrendData {
  date: Date;
  impressions: number;
  clicks: number;
  conversions: number;
  revenue: number;
  spend: number;
}

interface ChannelPerformance {
  channel: string;
  campaigns: number;
  impressions: number;
  clicks: number;
  conversions: number;
  revenue: number;
  spend: number;
  roas: number;
}

interface KPIData {
  name: string;
  target: number;
  current: number;
  percentage: number;
  status: 'on_track' | 'at_risk' | 'behind';
}

class DashboardDataProvider {
  constructor(
    private prisma: PrismaClient,
    private metricsCalculator: MetricsCalculator,
    private roiCalculator: ROICalculator
  ) {}

  /**
   * Get dashboard data
   */
  async getDashboardData(params: {
    startDate?: Date;
    endDate?: Date;
    campaignIds?: string[];
  }): Promise<DashboardData> {
    const [summary, topCampaigns, trends, byChannel, kpis] = await Promise.all([
      this.getSummary(params),
      this.getTopCampaigns(params),
      this.getTrends(params),
      this.getChannelPerformance(params),
      this.getKPIs(params),
    ]);

    return { summary, topCampaigns, trends, byChannel, kpis };
  }

  /**
   * Get campaign summary
   */
  private async getSummary(params: any): Promise<CampaignSummary> {
    const where = this.buildWhereClause(params);

    const [campaigns, budgetSum, spendSum] = await Promise.all([
      this.prisma.campaign.findMany({ where }),
      this.prisma.budgetAllocation.aggregate({
        where: { campaign: where },
        _sum: { totalBudget: true },
      }),
      this.prisma.budgetAllocation.aggregate({
        where: { campaign: where },
        _sum: { spent: true },
      }),
    ]);

    const totalBudget = budgetSum._sum.totalBudget || 0;
    const totalSpend = spendSum._sum.spent || 0;

    const campaignIds = campaigns.map(c => c.id);
    const [totalRevenue, roisArray] = await Promise.all([
      this.getTotalRevenue(campaignIds),
      this.getROASArray(campaignIds),
    ]);

    const averageROAS = roisArray.length > 0
      ? roisArray.reduce((sum, r) => sum + r, 0) / roisArray.length
      : 0;
    const averageROI = (averageROAS - 1) * 100;

    return {
      totalCampaigns: campaigns.length,
      activeCampaigns: campaigns.filter(c => c.status === CampaignStatus.ACTIVE).length,
      totalBudget,
      totalSpend,
      totalRevenue,
      averageROI,
      averageROAS,
    };
  }

  /**
   * Get top performing campaigns
   */
  private async getTopCampaigns(params: any): Promise<CampaignPerformance[]> {
    const where = this.buildWhereClause(params);
    const campaigns = await this.prisma.campaign.findMany({ where });
    const campaignIds = campaigns.map(c => c.id);

    const performances = await Promise.all(
      campaignIds.map(id => this.metricsCalculator.calculatePerformance(id))
    );

    return performances
      .sort((a, b) => b.roas - a.roas)
      .slice(0, 10);
  }

  /**
   * Get trend data
   */
  private async getTrends(params: any): Promise<TrendData[]> {
    const campaignIds = params.campaignIds || await this.getActiveCampaignIds();
    const startDate = params.startDate || new Date(Date.now() - 30 * 24 * 60 * 60 * 1000);
    const endDate = params.endDate || new Date();

    const trends = await this.metricsCalculator.calculateTrends(
      campaignIds[0], // Simplified - in reality, aggregate across all campaigns
      'day',
      startDate,
      endDate
    );

    return trends;
  }

  /**
   * Get channel performance
   */
  private async getChannelPerformance(params: any): Promise<ChannelPerformance[]> {
    const where = this.buildWhereClause(params);
    const channels = await this.prisma.campaignChannel.findMany({
      where: { campaign: where },
    });

    const channelIds = [...new Set(channels.map(c => c.channelId))];
    const performances = await Promise.all(
      channelIds.map(channelId => this.calculateChannelPerformance(channelId, params))
    );

    return performances;
  }

  /**
   * Get KPIs
   */
  private async getKPIs(params: any): Promise<KPIData[]> {
    const where = this.buildWhereClause(params);
    const campaigns = await this.prisma.campaign.findMany({ where });
    const campaignIds = campaigns.map(c => c.id);

    const kpis = await this.prisma.campaignKPI.findMany({
      where: { campaignId: { in: campaignIds } },
    });

    return kpis.map(kpi => {
      const percentage = kpi.target > 0 ? (kpi.current / kpi.target) * 100 : 0;
      let status: 'on_track' | 'at_risk' | 'behind' = 'on_track';

      if (percentage < 50) {
        status = 'behind';
      } else if (percentage < 80) {
        status = 'at_risk';
      }

      return {
        name: kpi.name,
        target: kpi.target,
        current: kpi.current,
        percentage,
        status,
      };
    });
  }

  private buildWhereClause(params: any): any {
    const where: any = {};

    if (params.startDate || params.endDate) {
      where.startDate = {};
      if (params.startDate) where.startDate.gte = params.startDate;
      if (params.endDate) where.startDate.lte = params.endDate;
    }

    if (params.campaignIds) {
      where.id = { in: params.campaignIds };
    }

    return where;
  }

  private async getTotalRevenue(campaignIds: string[]): Promise<number> {
    const conversions = await this.prisma.campaignEvent.findMany({
      where: {
        campaignId: { in: campaignIds },
        eventType: 'conversion',
      },
    });

    return conversions.reduce((sum, c) => sum + (c.value || 0), 0);
  }

  private async getROASArray(campaignIds: string[]): Promise<number[]> {
    const calculations = await Promise.all(
      campaignIds.map(id => this.roiCalculator.calculateROI(id))
    );

    return calculations.map(c => c.roas);
  }

  private async getActiveCampaignIds(): Promise<string[]> {
    const campaigns = await this.prisma.campaign.findMany({
      where: { status: CampaignStatus.ACTIVE },
    });

    return campaigns.map(c => c.id);
  }

  private async calculateChannelPerformance(channelId: string, params: any): Promise<ChannelPerformance> {
    // Implement channel performance calculation
    return {} as ChannelPerformance;
  }
}
```

---

## Integration with Analytics

### Analytics Integration

```typescript
interface AnalyticsIntegration {
  platform: 'google_analytics' | 'mixpanel' | 'amplitude' | 'segment';
  config: Record<string, any>;
}

class AnalyticsIntegrator {
  private integrations: Map<string, AnalyticsIntegration> = new Map();

  /**
   * Add analytics integration
   */
  addIntegration(platform: string, config: Record<string, any>): void {
    this.integrations.set(platform, {
      platform: platform as any,
      config,
    });
  }

  /**
   * Track campaign event across all integrations
   */
  async trackEvent(event: {
    campaignId: string;
    eventType: string;
    properties: Record<string, any>;
    value?: number;
  }): Promise<void> {
    const promises = [];

    for (const [platform, integration] of this.integrations) {
      switch (integration.platform) {
        case 'google_analytics':
          promises.push(this.trackWithGA(event, integration.config));
          break;
        case 'mixpanel':
          promises.push(this.trackWithMixpanel(event, integration.config));
          break;
        case 'amplitude':
          promises.push(this.trackWithAmplitude(event, integration.config));
          break;
        case 'segment':
          promises.push(this.trackWithSegment(event, integration.config));
          break;
      }
    }

    await Promise.all(promises);
  }

  /**
   * Track with Google Analytics
   */
  private async trackWithGA(event: any, config: any): Promise<void> {
    gtag('event', event.eventType, {
      campaign_id: event.campaignId,
      ...event.properties,
      value: event.value,
    });
  }

  /**
   * Track with Mixpanel
   */
  private async trackWithMixpanel(event: any, config: any): Promise<void> {
    mixpanel.track(event.eventType, {
      campaign_id: event.campaignId,
      ...event.properties,
      value: event.value,
    });
  }

  /**
   * Track with Amplitude
   */
  private async trackWithAmplitude(event: any, config: any): Promise<void> {
    amplitude.getInstance().logEvent(event.eventType, {
      campaign_id: event.campaignId,
      ...event.properties,
      value: event.value,
    });
  }

  /**
   * Track with Segment
   */
  private async trackWithSegment(event: any, config: any): Promise<void> {
    analytics.track(event.eventType, {
      campaign_id: event.campaignId,
      ...event.properties,
      value: event.value,
    });
  }

  /**
   * Import analytics data
   */
  async importAnalyticsData(
    campaignId: string,
    platform: string,
    startDate: Date,
    endDate: Date
  ): Promise<void> {
    const integration = this.integrations.get(platform);
    if (!integration) {
      throw new Error(`Integration not found: ${platform}`);
    }

    const data = await this.fetchAnalyticsData(
      integration,
      campaignId,
      startDate,
      endDate
    );

    // Import data into database
    await this.importData(campaignId, data);
  }

  private async fetchAnalyticsData(
    integration: AnalyticsIntegration,
    campaignId: string,
    startDate: Date,
    endDate: Date
  ): Promise<any[]> {
    // Implement platform-specific data fetching
    return [];
  }

  private async importData(campaignId: string, data: any[]): Promise<void> {
    // Implement data import logic
  }
}
```

---

## Automation

### Campaign Automation

```typescript
interface AutomationRule {
  id: string;
  name: string;
  trigger: AutomationTrigger;
  actions: AutomationAction[];
  enabled: boolean;
}

interface AutomationTrigger {
  type: 'budget_threshold' | 'performance_threshold' | 'time_based' | 'event_based';
  config: Record<string, any>;
}

interface AutomationAction {
  type: 'pause_campaign' | 'adjust_budget' | 'send_alert' | 'optimize' | 'scale';
  config: Record<string, any>;
}

class CampaignAutomation {
  private rules: Map<string, AutomationRule> = new Map();

  /**
   * Add automation rule
   */
  addRule(rule: AutomationRule): void {
    this.rules.set(rule.id, rule);
  }

  /**
   * Remove automation rule
   */
  removeRule(ruleId: string): void {
    this.rules.delete(ruleId);
  }

  /**
   * Check and execute rules
   */
  async checkRules(campaignId: string): Promise<void> {
    for (const [ruleId, rule] of this.rules) {
      if (!rule.enabled) continue;

      const shouldTrigger = await this.evaluateTrigger(rule.trigger, campaignId);

      if (shouldTrigger) {
        await this.executeActions(rule.actions, campaignId);
      }
    }
  }

  /**
   * Evaluate trigger
   */
  private async evaluateTrigger(trigger: AutomationTrigger, campaignId: string): Promise<boolean> {
    switch (trigger.type) {
      case 'budget_threshold':
        return await this.evaluateBudgetTrigger(trigger.config, campaignId);
      case 'performance_threshold':
        return await this.evaluatePerformanceTrigger(trigger.config, campaignId);
      case 'time_based':
        return await this.evaluateTimeTrigger(trigger.config, campaignId);
      case 'event_based':
        return await this.evaluateEventTrigger(trigger.config, campaignId);
      default:
        return false;
    }
  }

  /**
   * Execute actions
   */
  private async executeActions(actions: AutomationAction[], campaignId: string): Promise<void> {
    for (const action of actions) {
      switch (action.type) {
        case 'pause_campaign':
          await this.pauseCampaign(campaignId, action.config.reason);
          break;
        case 'adjust_budget':
          await this.adjustBudget(campaignId, action.config);
          break;
        case 'send_alert':
          await this.sendAlert(campaignId, action.config);
          break;
        case 'optimize':
          await this.optimizeCampaign(campaignId, action.config);
          break;
        case 'scale':
          await this.scaleCampaign(campaignId, action.config);
          break;
      }
    }
  }

  private async evaluateBudgetTrigger(config: any, campaignId: string): Promise<boolean> {
    const budget = await this.getBudget(campaignId);
    const spendPercentage = (budget.spent / budget.totalBudget) * 100;

    return spendPercentage >= config.percentage;
  }

  private async evaluatePerformanceTrigger(config: any, campaignId: string): Promise<boolean> {
    const performance = await this.getPerformance(campaignId);

    switch (config.metric) {
      case 'roas':
        return performance.roas < config.threshold;
      case 'cpa':
        return performance.cpa > config.threshold;
      case 'ctr':
        return performance.ctr < config.threshold;
      default:
        return false;
    }
  }

  private async evaluateTimeTrigger(config: any, campaignId: string): Promise<boolean> {
    const campaign = await this.getCampaign(campaignId);
    const now = new Date();

    switch (config.condition) {
      case 'before_end':
        return campaign.endDate.getTime() - now.getTime() <= config.hours * 60 * 60 * 1000;
      case 'after_start':
        return now.getTime() - campaign.startDate.getTime() >= config.hours * 60 * 60 * 1000;
      default:
        return false;
    }
  }

  private async evaluateEventTrigger(config: any, campaignId: string): Promise<boolean> {
    // Implement event-based trigger evaluation
    return false;
  }

  private async pauseCampaign(campaignId: string, reason: string): Promise<void> {
    // Implement pause logic
  }

  private async adjustBudget(campaignId: string, config: any): Promise<void> {
    // Implement budget adjustment logic
  }

  private async sendAlert(campaignId: string, config: any): Promise<void> {
    // Implement alert sending logic
  }

  private async optimizeCampaign(campaignId: string, config: any): Promise<void> {
    // Implement optimization logic
  }

  private async scaleCampaign(campaignId: string, config: any): Promise<void> {
    // Implement scaling logic
  }

  private async getBudget(campaignId: string): Promise<any> {
    // Implement budget retrieval
    return {};
  }

  private async getPerformance(campaignId: string): Promise<any> {
    // Implement performance retrieval
    return {};
  }

  private async getCampaign(campaignId: string): Promise<any> {
    // Implement campaign retrieval
    return {};
  }
}
```

---

## Best Practices

### Campaign Management Checklist

```typescript
interface CampaignChecklist {
  planning: ChecklistItem[];
  execution: ChecklistItem[];
  monitoring: ChecklistItem[];
  optimization: ChecklistItem[];
  reporting: ChecklistItem[];
}

interface ChecklistItem {
  item: string;
  completed: boolean;
  notes?: string;
}

const campaignChecklist: CampaignChecklist = {
  planning: [
    { item: 'Define clear objectives', completed: false },
    { item: 'Identify target audience', completed: false },
    { item: 'Set budget allocation', completed: false },
    { item: 'Define KPIs and targets', completed: false },
    { item: 'Create content plan', completed: false },
    { item: 'Set up tracking', completed: false },
  ],
  execution: [
    { item: 'Test all channels', completed: false },
    { item: 'Verify tracking setup', completed: false },
    { item: 'Set up automation rules', completed: false },
    { item: 'Configure alerts', completed: false },
    { item: 'Launch campaign', completed: false },
  ],
  monitoring: [
    { item: 'Monitor daily performance', completed: false },
    { item: 'Check budget utilization', completed: false },
    { item: 'Review channel performance', completed: false },
    { item: 'Analyze conversion data', completed: false },
  ],
  optimization: [
    { item: 'Identify underperforming channels', completed: false },
    { item: 'Reallocate budget to top performers', completed: false },
    { item: 'A/B test creatives', completed: false },
    { item: 'Optimize targeting', completed: false },
  ],
  reporting: [
    { item: 'Generate weekly reports', completed: false },
    { item: 'Calculate ROI', completed: false },
    { item: 'Document learnings', completed: false },
    { item: 'Share insights with team', completed: false },
  ],
};
```

---

## Quick Start

### Campaign Creation

```typescript
interface Campaign {
  id: string
  name: string
  type: 'email' | 'social' | 'paid' | 'content'
  status: 'draft' | 'scheduled' | 'active' | 'paused' | 'completed'
  budget: number
  startDate: Date
  endDate: Date
  channels: string[]
}

async function createCampaign(campaign: Campaign) {
  return await db.campaigns.create({
    data: campaign
  })
}
```

### Campaign Tracking

```typescript
async function trackCampaignEvent(
  campaignId: string,
  event: 'impression' | 'click' | 'conversion',
  userId?: string
) {
  await db.campaignEvents.create({
    data: {
      campaignId,
      event,
      userId,
      timestamp: new Date()
    }
  })
}
```

---

## Production Checklist

- [ ] **Campaign Planning**: Plan campaigns with clear objectives
- [ ] **Budget Management**: Allocate and track budgets
- [ ] **Multi-Channel**: Coordinate across multiple channels
- [ ] **Tracking**: Implement campaign tracking (UTM, pixels)
- [ ] **Performance Metrics**: Track KPIs (CTR, conversion, ROI)
- [ ] **ROI Calculation**: Calculate return on investment
- [ ] **Reporting**: Regular campaign reports
- [ ] **Optimization**: Optimize based on performance
- [ ] **A/B Testing**: Test campaign variations
- [ ] **Documentation**: Document campaign learnings
- [ ] **Automation**: Automate campaign workflows
- [ ] **Integration**: Integrate with analytics tools

---

## Anti-patterns

### ❌ Don't: No Tracking

```markdown
# ❌ Bad - No tracking
Campaign: "Summer Sale"
# How did it perform?
```

```markdown
# ✅ Good - Complete tracking
Campaign: "Summer Sale"
UTM: ?utm_source=email&utm_campaign=summer_sale
Impressions: 10,000
Clicks: 500
Conversions: 50
ROI: 300%
```

### ❌ Don't: No Budget Control

```typescript
// ❌ Bad - No budget control
async function runCampaign(campaignId: string) {
  // Spend unlimited!
}
```

```typescript
// ✅ Good - Budget control
async function runCampaign(campaignId: string) {
  const campaign = await getCampaign(campaignId)
  const spent = await getSpent(campaignId)
  
  if (spent >= campaign.budget) {
    await pauseCampaign(campaignId)
    return
  }
  
  // Continue campaign
}
```

---

## Integration Points

- **Marketing Automation** (`28-marketing-integration/marketing-automation/`) - Automated campaigns
- **Email Marketing** (`28-marketing-integration/email-marketing/`) - Email campaigns
- **Analytics** (`23-business-analytics/`) - Campaign analytics

---

## Further Reading

- [Campaign Management Best Practices](https://www.hubspot.com/marketing/campaign-management)
- [UTM Tracking](https://support.google.com/analytics/answer/1033863)

## Resources

- [Google Analytics 4](https://analytics.google.com/)
- [Google Ads API](https://developers.google.com/google-ads/api/docs/)
- [Facebook Marketing API](https://developers.facebook.com/docs/marketing-apis/)
- [Mixpanel](https://mixpanel.com/)
- [Segment](https://segment.com/)
