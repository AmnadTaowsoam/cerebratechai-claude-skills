---
name: Customer Support Analytics
description: Providing insights into support team performance, customer satisfaction, and operational efficiency through metrics, dashboards, real-time monitoring, and predictive analytics.
---

# Customer Support Analytics

> **Current Level:** Intermediate  
> **Domain:** Customer Support / Analytics

---

## Overview

Customer support analytics provides insights into support team performance, customer satisfaction, and operational efficiency to improve the support experience. Effective analytics includes key metrics, dashboards, trend analysis, and predictive insights.

---

## Core Concepts

### Table of Contents

1. [Key Support Metrics](#key-support-metrics)
2. [Data Collection](#data-collection)
3. [Dashboard Design](#dashboard-design)
4. [Real-Time Monitoring](#real-time-monitoring)
5. [Agent Performance Metrics](#agent-performance-metrics)
6. [Trend Analysis](#trend-analysis)
7. [Predictive Analytics](#predictive-analytics)
8. [Reporting Automation](#reporting-automation)
9. [Integration with BI Tools](#integration-with-bi-tools)
10. [Custom Metrics](#custom-metrics)
11. [Best Practices](#best-practices)

---

## Key Support Metrics

### Core Metrics

```typescript
interface SupportMetrics {
  // Volume metrics
  ticketVolume: number;
  newTickets: number;
  openTickets: number;
  backlog: number;

  // Time metrics
  averageFirstResponseTime: number; // in minutes
  averageResolutionTime: number; // in minutes
  averageHandleTime: number; // in minutes

  // Quality metrics
  csatScore: number; // 1-5
  npsScore: number; // -100 to 100
  cesScore: number; // 1-7

  // Efficiency metrics
  ticketsPerAgent: number;
  ticketsResolvedPerDay: number;
  oneTouchResolutionRate: number;

  // Customer metrics
  repeatContactRate: number;
  churnRate: number;
  customerRetentionRate: number;
}

interface SLAMetrics {
  slaComplianceRate: number;
  responseSlaMet: number;
  resolutionSlaMet: number;
  averageSlaBreach: number; // in hours
  criticalSlaBreaches: number;
}

interface ChannelMetrics {
  email: ChannelStats;
  chat: ChannelStats;
  phone: ChannelStats;
  social: ChannelStats;
  selfService: ChannelStats;
}

interface ChannelStats {
  volume: number;
  avgResponseTime: number;
  avgResolutionTime: number;
  csatScore: number;
  resolutionRate: number;
}
```

---

## Data Collection

### Data Collector

```typescript
class SupportDataCollector {
  constructor(private prisma: PrismaClient) {}

  /**
   * Collect ticket data
   */
  async collectTicketData(params: {
    startDate: Date;
    endDate: Date;
    agentId?: string;
    category?: string;
  }): Promise<any[]> {
    const where: any = {
      createdAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    if (params.agentId) {
      where.assigneeId = params.agentId;
    }

    if (params.category) {
      where.category = params.category;
    }

    return await this.prisma.ticket.findMany({
      where,
      include: {
        requester: true,
        assignee: true,
        comments: true,
        sla: true,
      },
    });
  }

  /**
   * Collect agent activity
   */
  async collectAgentActivity(params: {
    startDate: Date;
    endDate: Date;
    agentId?: string;
  }): Promise<any[]> {
    const where: any = {
      createdAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    if (params.agentId) {
      where.agentId = params.agentId;
    }

    return await this.prisma.agentActivity.findMany({
      where,
      orderBy: { createdAt: 'asc' },
    });
  }

  /**
   * Collect feedback data
   */
  async collectFeedbackData(params: {
    startDate: Date;
    endDate: Date;
  }): Promise<any[]> {
    return await this.prisma.feedback.findMany({
      where: {
        createdAt: {
          gte: params.startDate,
          lte: params.endDate,
        },
      },
      include: {
        ticket: true,
        user: true,
      },
    });
  }

  /**
   * Collect chat data
   */
  async collectChatData(params: {
    startDate: Date;
    endDate: Date;
  }): Promise<any[]> {
    return await this.prisma.chatSession.findMany({
      where: {
        startedAt: {
          gte: params.startDate,
          lte: params.endDate,
        },
      },
      include: {
        messages: true,
        agent: true,
        requester: true,
      },
    });
  }

  /**
   * Collect survey data
   */
  async collectSurveyData(params: {
    startDate: Date;
    endDate: Date;
    surveyType?: 'nps' | 'csat' | 'ces';
  }): Promise<any[]> {
    const where: any = {
      submittedAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    if (params.surveyType) {
      where.type = params.surveyType;
    }

    return await this.prisma.surveyResponse.findMany({
      where,
      include: {
        survey: true,
        user: true,
      },
    });
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Dashboard Design

### Dashboard Component

```tsx
import React, { useState, useEffect } from 'react';

const SupportDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<SupportMetrics | null>(null);
  [loading, setLoading] = useState(true);
  const [dateRange, setDateRange] = useState({
    startDate: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
    endDate: new Date(),
  });

  useEffect(() => {
    loadMetrics();
  }, [dateRange]);

  const loadMetrics = async () => {
    setLoading(true);
    try {
      const analytics = new SupportAnalytics(prisma);
      const calculatedMetrics = await analytics.calculateMetrics(dateRange.startDate, dateRange.endDate);
      setMetrics(calculatedMetrics);
    } catch (error) {
      console.error('Error loading metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading metrics...</div>;
  }

  return (
    <div className="support-dashboard">
      <div className="date-filter">
        <DatePicker
          selected={dateRange.startDate}
          onChange={(date) => setDateRange(prev => ({ ...prev, startDate: date }))}
          label="Start Date"
        />
        <DatePicker
          selected={dateRange.endDate}
          onChange={(date) => setDateRange(prev => ({ ...prev, endDate: date }))}
          label="End Date"
        />
      </div>

      {metrics && (
        <>
          <div className="metrics-grid">
            <MetricCard
              title="Total Tickets"
              value={metrics.ticketVolume}
              change={calculateChange('ticketVolume')}
            />
            <MetricCard
              title="New Tickets"
              value={metrics.newTickets}
              change={calculateChange('newTickets')}
            />
            <MetricCard
              title="Open Tickets"
              value={metrics.openTickets}
              change={calculateChange('openTickets')}
            />
            <MetricCard
              title="Backlog"
              value={metrics.backlog}
              change={calculateChange('backlog')}
            />
          </div>

          <div className="metrics-grid">
            <MetricCard
              title="Avg First Response Time"
              value={`${formatTime(metrics.averageFirstResponseTime)}`}
              unit="minutes"
              change={calculateChange('averageFirstResponseTime')}
            />
            <MetricCard
              title="Avg Resolution Time"
              value={`${formatTime(metrics.averageResolutionTime)}`}
              unit="minutes"
              change={calculateChange('averageResolutionTime')}
            />
            <MetricCard
              title="CSAT Score"
              value={metrics.csatScore.toFixed(1)}
              max={5}
              change={calculateChange('csatScore')}
            />
            <MetricCard
              title="NPS Score"
              value={metrics.npsScore.toFixed(0)}
              max={100}
              min={-100}
              change={calculateChange('npsScore')}
            />
          </div>

          <div className="metrics-grid">
            <MetricCard
              title="One-Touch Resolution"
              value={`${metrics.oneTouchResolutionRate.toFixed(1)}%`}
              unit="%"
              change={calculateChange('oneTouchResolutionRate')}
            />
            <MetricCard
              title="Tickets Per Agent"
              value={metrics.ticketsPerAgent.toFixed(1)}
              change={calculateChange('ticketsPerAgent')}
            />
            <MetricCard
              title="Repeat Contact Rate"
              value={`${metrics.repeatContactRate.toFixed(1)}%`}
              unit="%"
              change={calculateChange('repeatContactRate')}
            />
          </div>

          <div className="charts-section">
            <TicketVolumeChart dateRange={dateRange} />
            <ResponseTimeChart dateRange={dateRange} />
            <CSATTrendChart dateRange={dateRange} />
          </div>
        </>
      )}
    </div>
  );
};

interface MetricCardProps {
  title: string;
  value: number | string;
  unit?: string;
  max?: number;
  min?: number;
  change?: number;
}

const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  unit,
  max = 5,
  min = 0,
  change,
}) => {
  const changeColor = change && change > 0 ? 'text-green' : change && change < 0 ? 'text-red' : 'text-gray';
  const changeIcon = change && change > 0 ? '↑' : change && change < 0 ? '↓' : '';

  return (
    <div className="metric-card">
      <div className="metric-title">{title}</div>
      <div className="metric-value">
        {typeof value === 'number' && unit && (
          <>
            {value.toFixed(1)}
            <span className="unit">{unit}</span>
          </>
        ) || (
          value
        )}
      </div>
      {change !== undefined && (
        <div className={`metric-change ${changeColor}`}>
          {changeIcon} {Math.abs(change).toFixed(1)}%
        </div>
      )}
    </div>
  );
};

const formatTime = (minutes: number): string => {
  if (minutes < 60) return `${Math.floor(minutes)}m`;
  const hours = Math.floor(minutes / 60);
  const mins = Math.floor(minutes % 60);
  return `${hours}h ${mins}m`;
};

const calculateChange = (currentValue: number): number | undefined => {
  // Implement change calculation based on previous period
  return 0;
};

export default SupportDashboard;
```

---

## Real-Time Monitoring

### Real-Time Metrics

```typescript
class RealTimeMonitor {
  private metrics: Map<string, any> = new Map();
  private subscribers: Set<WebSocket> = new Set();

  /**
   * Subscribe to real-time updates
   */
  subscribe(ws: WebSocket): void {
    this.subscribers.add(ws);

    // Send current metrics
    ws.send(JSON.stringify({
      type: 'metrics_update',
      data: Object.fromEntries(this.metrics),
    }));
  }

  /**
   * Unsubscribe
   */
  unsubscribe(ws: WebSocket): void {
    this.subscribers.delete(ws);
  }

  /**
   * Update metric
   */
  updateMetric(key: string, value: any): void {
    this.metrics.set(key, {
      value,
      timestamp: Date.now(),
    });

    // Broadcast to subscribers
    this.broadcast({
      type: 'metric_update',
      key,
      value,
    });
  }

  /**
   * Broadcast to all subscribers
   */
  private broadcast(message: any): void {
    const data = JSON.stringify(message);

    for (const ws of this.subscribers) {
      if (ws.readyState === ws.OPEN) {
        ws.send(data);
      }
    }
  }

  /**
   * Get current metrics
   */
  getMetrics(): Record<string, any> {
    return Object.fromEntries(this.metrics);
  }
}

// WebSocket server
import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({ port: 8080 });

const monitor = new RealTimeMonitor();

wss.on('connection', (ws) => {
  monitor.subscribe(ws);
});

// Update metrics on events
ticketManager.on('ticket_created', (ticket) => {
  monitor.updateMetric('totalTickets', (monitor.getMetrics().totalTickets || 0) + 1);
});

ticketManager.on('ticket_resolved', (ticket) => {
  const metrics = monitor.getMetrics();
  monitor.updateMetric('resolvedTickets', (metrics.resolvedTickets || 0) + 1);
  monitor.updateMetric('totalResolutionTime', calculateResolutionTime(ticket));
});

chatManager.on('message_sent', (message) => {
  const metrics = monitor.getMetrics();
  monitor.updateMetric('messagesSent', (metrics.messagesSent || 0) + 1);
});
});

function calculateResolutionTime(ticket: any): number {
  // Calculate resolution time in minutes
  return 0;
}
```

---

## Agent Performance Metrics

### Agent Performance

```typescript
interface AgentPerformance {
  agentId: string;
  agentName: string;
  metrics: {
    totalTickets: number;
    resolvedTickets: number;
    inProgressTickets: number;
    averageResolutionTime: number;
    averageResponseTime: number;
    csatAverage: number;
    oneTouchResolutionRate: number;
    ticketsPerDay: number;
    utilizationRate: number;
  };
  period: {
    startDate: Date;
    endDate: Date;
  };
}

class AgentPerformanceAnalyzer {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get agent performance
   */
  async getAgentPerformance(params: {
    agentId?: string;
    startDate: Date;
    endDate: Date;
  }): Promise<AgentPerformance[]> {
    const where: any = {
      createdAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    if (params.agentId) {
      where.assigneeId = params.agentId;
    }

    const tickets = await this.prisma.ticket.findMany({
      where,
      include: {
        assignee: true,
        comments: true,
        sla: true,
      },
    });

    // Group by agent
    const agentMap = new Map<string, any[]>();

    for (const ticket of tickets) {
      if (!ticket.assigneeId) continue;

      if (!agentMap.has(ticket.assigneeId)) {
        agentMap.set(ticket.assigneeId, []);
      }

      agentMap.get(ticket.assigneeId)!.push(ticket);
    }

    const performances: AgentPerformance[] = [];

    for (const [agentId, agentTickets] of agentMap.entries()) {
      const performance = await this.calculateAgentPerformance(agentId, agentTickets, params);
      performances.push(performance);
    }

    return performances;
  }

  /**
   * Calculate agent performance
   */
  private async calculateAgentPerformance(
    agentId: string,
    tickets: any[],
    params: { startDate: Date; endDate: Date }
  ): Promise<AgentPerformance> {
    const agent = await this.prisma.agent.findUnique({
      where: { id: agentId },
    });

    const totalTickets = tickets.length;
    const resolvedTickets = tickets.filter(t => t.status === 'resolved');
    const inProgressTickets = tickets.filter(t => t.status === 'in_progress');

    // Calculate average resolution time
    const resolutionTimes = resolvedTickets
      .filter(t => t.resolvedAt && t.createdAt)
      .map(t => t.resolvedAt!.getTime() - t.createdAt.getTime());

    const averageResolutionTime = resolutionTimes.length > 0
      ? resolutionTimes.reduce((sum, t) => sum + t, 0) / resolutionTimes.length / 60000
      : 0;

    // Calculate average response time
    const responseTimes = tickets
      .map(t => {
        const firstAgentComment = t.comments?.find((c: any) => c.authorType === 'agent');
        return firstAgentComment?.createdAt
          ? firstAgentComment.createdAt.getTime() - t.createdAt.getTime()
          : null;
      })
      .filter(t => t !== null);

    const averageResponseTime = responseTimes.length > 0
      ? responseTimes.reduce((sum, t) => sum + t!, 0) / responseTimes.length / 60000
      : 0;

    // Get CSAT scores
    const csatScores = await this.getAgentCSATScores(agentId, params.startDate, params.endDate);
    const csatAverage = csatScores.length > 0
      ? csatScores.reduce((sum, s) => sum + s, 0) / csatScores.length
      : 0;

    // Calculate one-touch resolution rate
    const oneTouchResolutions = resolvedTickets.filter(t => t.comments?.length === 1);
    const oneTouchResolutionRate = resolvedTickets.length > 0
      ? (oneTouchResolutions.length / resolvedTickets.length) * 100
      : 0;

    // Calculate tickets per day
    const days = Math.ceil((params.endDate.getTime() - params.startDate.getTime()) / (24 * 60 * 60 * 1000));
    const ticketsPerDay = totalTickets / days;

    // Calculate utilization rate
    const utilizationRate = await this.calculateUtilizationRate(agentId, params.startDate, params.endDate);

    return {
      agentId,
      agentName: agent?.name || 'Unknown',
      metrics: {
        totalTickets,
        resolvedTickets,
        inProgressTickets,
        averageResolutionTime,
        averageResponseTime,
        csatAverage,
        oneTouchResolutionRate,
        ticketsPerDay,
        utilizationRate,
      },
      period: {
        startDate: params.startDate,
        endDate: params.endDate,
      },
    };
  }

  /**
   * Get agent CSAT scores
   */
  private async getAgentCSATScores(
    agentId: string,
    startDate: Date,
    endDate: Date
  ): Promise<number[]> {
    const feedback = await this.prisma.feedback.findMany({
      where: {
        agentId,
        createdAt: {
          gte: startDate,
          lte: endDate,
        },
        type: 'csat',
      },
    });

    return feedback.map(f => f.score);
  }

  /**
   * Calculate utilization rate
   */
  private async calculateUtilizationRate(
    agentId: string,
    startDate: Date,
    endDate: Date
  ): Promise<number> {
    const agent = await this.prisma.agent.findUnique({
      where: { id: agentId },
    include: {
        activity: true,
      },
    });

    if (!agent) return 0;

    const activity = agent.activity.filter(a => 
      a.createdAt >= startDate && a.createdAt <= endDate
    );

    const totalMinutes = (endDate.getTime() - startDate.getTime()) / 60000;
    const activeMinutes = activity.reduce((sum, a) => {
      const sessionDuration = a.endedAt
        ? (a.endedAt.getTime() - a.startedAt.getTime()) / 60000
        : 0;
      return sum + sessionDuration;
    }, 0);

    return totalMinutes > 0 ? (activeMinutes / totalMinutes) * 100 : 0;
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Trend Analysis

### Trend Analyzer

```typescript
interface TrendData {
  date: Date;
  metrics: Partial<SupportMetrics>;
}

class TrendAnalyzer {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get trend data
   */
  async getTrendData(params: {
    metric: keyof SupportMetrics;
    startDate: Date;
    endDate: Date;
    period: 'day' | 'week' | 'month';
  }): Promise<TrendData[]> {
    const data: TrendData[] = [];
    const currentDate = new Date(params.startDate);

    while (currentDate <= params.endDate) {
      let periodEndDate: Date;

      switch (params.period) {
        case 'day':
          periodEndDate = new Date(currentDate);
          periodEndDate.setDate(currentDate.getDate() + 1);
          break;
        case 'week':
          periodEndDate = new Date(currentDate);
          periodEndDate.setDate(currentDate.getDate() + 7);
          break;
        case 'month':
          periodEndDate = new Date(currentDate);
          periodEndDate.setMonth(currentDate.getMonth() + 1);
          break;
      }

      const metrics = await this.getMetricsForPeriod(
        new Date(currentDate),
        periodEndDate
      );

      data.push({
        date: new Date(currentDate),
        metrics: {
          [params.metric]: metrics[params.metric],
        },
      });

      currentDate = periodEndDate;
    }

    return data;
  }

  /**
   * Get metrics for period
   */
  private async getMetricsForPeriod(
    startDate: Date,
    endDate: Date
  ): Promise<Partial<SupportMetrics>> {
    const analytics = new SupportAnalytics(this.prisma);
    return await analytics.calculateMetrics(startDate, endDate);
  }

  /**
   * Calculate trend
   */
  calculateTrend(data: TrendData[]): {
    trend: 'increasing' | 'decreasing' | 'stable';
    changePercentage: number;
    average: number;
    lastValue: number;
  } | null {
    if (data.length < 2) {
      return null;
    }

    const values = data.map(d => d.metrics[Object.keys(d.metrics)[0]]);
    const lastValue = values[values.length - 1];
    const previousValue = values[values.length - 2];

    const average = values.reduce((sum, v) => sum + v, 0) / values.length;

    let trend: 'increasing' | 'decreasing' | 'stable' = 'stable';
    let changePercentage = 0;

    if (lastValue > average * 1.05) {
      trend = 'increasing';
      changePercentage = ((lastValue - average) / average) * 100;
    } else if (lastValue < average * 0.95) {
      trend = 'decreasing';
      changePercentage = ((lastValue - average) / average) * 100;
    }

    return { trend, changePercentage, average, lastValue };
  }

  /**
   * Get moving average
   */
  getMovingAverage(data: TrendData[], window: number = 7): TrendData[] {
    const result: TrendData[] = [];

    for (let i = 0; i < data.length; i++) {
      const start = Math.max(0, i - window + 1);
      const end = i + 1;
      const windowData = data.slice(start, end);

      const values = windowData.map(d => Object.values(d.metrics)[0]);
      const average = values.reduce((sum, v) => sum + v, 0) / values.length;

      result.push({
        date: data[i].date,
        metrics: {
          [Object.keys(data[i].metrics)[0]]: average,
        },
      });
    }

    return result;
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Predictive Analytics

### Volume Prediction

```typescript
class VolumePredictor {
  private historicalData: Array<{ date: Date; volume: number }> = [];

  /**
   * Load historical data
   */
  async loadHistoricalData(days: number = 90): Promise<void> {
    const endDate = new Date();
    const startDate = new Date(endDate.getTime() - days * 24 * 60 * 60 * 1000);

    const tickets = await prisma.ticket.findMany({
      where: {
        createdAt: {
          gte: startDate,
          lte: endDate,
        },
      },
      orderBy: { createdAt: 'asc' },
    });

    // Group by day
    const grouped = new Map<string, number>();

    for (const ticket of tickets) {
      const dateKey = ticket.createdAt.toISOString().split('T')[0];
      grouped.set(dateKey, (grouped.get(dateKey) || 0) + 1);
    }

    this.historicalData = Array.from(grouped.entries()).map(([date, count]) => ({
      date: new Date(date),
      volume: count,
    }));
  }

  /**
   * Predict volume for next N days
   */
  predictVolume(days: number): Array<{ date: Date; predictedVolume: number; confidence: number }> {
    if (this.historicalData.length < 7) {
      throw new Error('Insufficient historical data for prediction');
    }

    const predictions: Array<{ date: Date; predictedVolume: number; confidence: number }> = [];
    const lastDate = this.historicalData[this.historicalData.length - 1].date;

    for (let i = 1; i <= days; i++) {
      const predictedDate = new Date(lastDate.getTime() + i * 24 * 60 * 60 * 1000);
      const predicted = this.predictForDate(predictedDate);
      const confidence = this.calculateConfidence(i);

      predictions.push({
        date: predictedDate,
        predictedVolume: predicted,
        confidence,
      });
    }

    return predictions;
  }

  /**
   * Predict volume for specific date
   */
  private predictForDate(date: Date): number {
    // Simple moving average prediction
    const windowSize = Math.min(7, this.historicalData.length);
    const recentData = this.historicalData.slice(-windowSize);

    const average = recentData.reduce((sum, d) => sum + d.volume, 0) / recentData.length;

    // Add trend adjustment
    const trend = this.calculateTrend(recentData);
    const trendAdjustment = (trend.changePercentage / 100) * average;

    return Math.round(average + trendAdjustment);
  }

  /**
   * Calculate trend
   */
  private calculateTrend(data: typeof this.historicalData): {
    trend: 'increasing' | 'decreasing' | 'stable';
    changePercentage: number;
  } {
    const values = data.map(d => d.volume);
    const recent = values.slice(-7);
    const older = values.slice(-14, -7);

    const recentAvg = recent.reduce((sum, v) => sum + v, 0) / recent.length;
    const olderAvg = older.reduce((sum, v) => sum + v, 0) / older.length;

    let trend: 'increasing' | 'decreasing' | 'stable' = 'stable';
    let changePercentage = 0;

    if (recentAvg > olderAvg * 1.05) {
      trend = 'increasing';
      changePercentage = ((recentAvg - olderAvg) / olderAvg) * 100;
    } else if (recentAvg < olderAvg * 0.95) {
      trend = 'decreasing';
      changePercentage = ((recentAvg - olderAvg) / olderAvg) * 100);
    }

    return { trend, changePercentage };
  }

  /**
   * Calculate confidence
   */
  private calculateConfidence(daysAhead: number): number {
    // Confidence decreases as we predict further ahead
    return Math.max(0, 1 - (daysAhead / 30));
  }
}
```

---

## Reporting Automation

### Report Generator

```typescript
interface ReportConfig {
  type: 'daily' | 'weekly' | 'monthly' | 'quarterly';
  recipients: string[];
  includeCharts: boolean;
  metrics: string[];
}

class ReportGenerator {
  constructor(private prisma: PrismaClient) {}

  /**
   * Generate report
   */
  async generateReport(config: ReportConfig): Promise<{
    html: string;
    text: string;
  }> {
    const dateRange = this.getDateRangeForReport(config.type);

    const analytics = new SupportAnalytics(this.prisma);
    const metrics = await analytics.calculateMetrics(dateRange.startDate, dateRange.endDate);
    const agentMetrics = await analytics.getAgentPerformance({
      startDate: dateRange.startDate,
      endDate: dateRange.endDate,
    });

    const html = this.generateHTMLReport(metrics, agentMetrics, dateRange, config);
    const text = this.generateTextReport(metrics, agentMetrics, dateRange, config);

    return { html, text };
  }

  /**
   * Send report
   */
  async sendReport(config: ReportConfig): Promise<void> {
    const { html, text } = await this.generateReport(config);

    // Send email to recipients
    for (const recipient of config.recipients) {
      await emailService.send({
        to: recipient,
        subject: `Support Report - ${config.type}`,
        html,
        text,
      });
    }
  }

  /**
   * Schedule reports
   */
  async scheduleReport(config: ReportConfig): Promise<void> {
    const schedule = await this.prisma.scheduledReport.create({
      data: {
        ...config,
        nextRunAt: this.getNextRunDate(config.type),
        isActive: true,
      },
    });
  }

  /**
   * Get next run date
   */
  private getNextRunDate(type: ReportConfig['type']): Date {
    const now = new Date();

    switch (type) {
      case 'daily':
        return new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 9, 0, 0);
      case 'weekly':
        return new Date(now.getFullYear(), now.getMonth(), now.getDate() + (7 - now.getDay()), 9, 0, 0);
      case 'monthly':
        return new Date(now.getFullYear(), now.getMonth() + 1, 1, 0, 0, 0);
      case 'quarterly':
        return new Date(now.getFullYear(), now.getMonth() + 3, 1, 0, 0, 0);
    }
  }

  /**
   * Generate HTML report
   */
  private generateHTMLReport(
    metrics: SupportMetrics,
    agentMetrics: AgentPerformance[],
    dateRange: { startDate: Date; endDate: Date },
    config: ReportConfig
  ): string {
    const agentRows = agentMetrics.map(agent => `
      <tr>
        <td>${agent.agentName}</td>
        <td>${agent.metrics.totalTickets}</td>
        <td>${agent.metrics.resolvedTickets}</td>
        <td>${this.formatTime(agent.metrics.averageResolutionTime)}</td>
        <td>${agent.metrics.csatAverage.toFixed(2)}</td>
        <td>${agent.metrics.oneTouchResolutionRate.toFixed(1)}%</td>
      </tr>
    `).join('');

    return `
      <!DOCTYPE html>
      <html>
      <head>
        <title>Support Report - ${config.type}</title>
        <style>
          body { font-family: Arial, sans-serif; padding: 20px; }
          table { border-collapse: collapse; width: 100%; }
          th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
          th { background: #f5f5f5; }
          .metric { font-weight: bold; }
          .positive { color: green; }
          .negative { color: red; }
        </style>
      </head>
      <body>
        <h1>Support Report - ${config.type}</h1>
        <p>${dateRange.startDate.toDateString()} - ${dateRange.endDate.toDateString()}</p>

        <h2>Overview</h2>
        <table>
          <tr>
            <th>Metric</th>
            <th>Value</th>
            <th>Trend</th>
          </tr>
          <tr>
            <td class="metric">Total Tickets</td>
            <td>${metrics.ticketVolume}</td>
            <td>${this.getTrendIndicator('ticketVolume')}</td>
          </tr>
          <tr>
            <td class="metric">New Tickets</td>
            <td>${metrics.newTickets}</td>
            <td>${this.getTrendIndicator('newTickets')}</td>
          </tr>
          <tr>
            <td class="metric">Open Tickets</td>
            <td>${metrics.openTickets}</td>
            <td>${this.getTrendIndicator('openTickets')}</td>
          </tr>
          <tr>
            <td class="metric">Avg First Response Time</td>
            <td>${this.formatTime(metrics.averageFirstResponseTime)}</td>
            <td>${this.getTrendIndicator('averageFirstResponseTime')}</td>
          </tr>
          <tr>
            <td class="metric">Avg Resolution Time</td>
            <td>${this.formatTime(metrics.averageResolutionTime)}</td>
            <td>${this.getTrendIndicator('averageResolutionTime')}</td>
          </tr>
          <tr>
            <td class="metric">CSAT Score</td>
            <td>${metrics.csatScore.toFixed(2)}</td>
            <td>${this.getTrendIndicator('csatScore')}</td>
          </tr>
          <tr>
            <td class="metric">NPS Score</td>
            <td>${metrics.npsScore.toFixed(0)}</td>
            <td>${this.getTrendIndicator('npsScore')}</td>
          </tr>
        </table>

        <h2>Agent Performance</h2>
        <table>
          <tr>
            <th>Agent</th>
            <th>Total</th>
            <th>Resolved</th>
            <th>Resolution Time</th>
            <th>CSAT</th>
            <th>One-Touch %</th>
          </tr>
          ${agentRows}
        </table>
      </body>
    </html>
    `;
  }

  /**
   * Generate text report
   */
  private generateTextReport(
    metrics: SupportMetrics,
    agentMetrics: AgentPerformance[],
    dateRange: { startDate: Date; endDate: Date },
    config: ReportConfig
  ): string {
    const agentLines = agentMetrics.map(agent =>
      `${agent.agentName}: ${agent.metrics.totalTickets} tickets, ${agent.metrics.resolvedTickets} resolved, ${this.formatTime(agent.metrics.averageResolutionTime)} avg resolution time, ${agent.metrics.csatAverage.toFixed(2)} CSAT, ${agent.metrics.oneTouchResolutionRate.toFixed(1)}% one-touch`
    ).join('\n');

    return `
Support Report - ${config.type}
${dateRange.startDate.toDateString()} - ${dateRange.endDate.toDateString()}

Overview
--------
Total Tickets: ${metrics.ticketVolume}
New Tickets: ${metrics.newTickets}
Open Tickets: ${metrics.openTickets}
Backlog: ${metrics.backlog}
Avg First Response Time: ${this.formatTime(metrics.averageFirstResponseTime)}
Avg Resolution Time: ${this.formatTime(metrics.averageResolutionTime)}
CSAT Score: ${metrics.csatScore.toFixed(2)}
NPS Score: ${metrics.npsScore.toFixed(0)}

Agent Performance
------------------
${agentLines}
    `.trim();
  }

  /**
   * Format time
   */
  private formatTime(minutes: number): string {
    if (minutes < 60) {
      return `${Math.floor(minutes)}m`;
    }
    const hours = Math.floor(minutes / 60);
    const mins = Math.floor(minutes % 60);
    return `${hours}h ${mins}m`;
  }

  /**
   * Get trend indicator
   */
  private getTrendIndicator(metric: number): string {
    // Implement trend calculation
    return '→';
  }

  constructor(private prisma: PrismaClient) {}
}
```

---

## Integration with BI Tools

### Power BI Integration

```typescript
class PowerBIIntegration {
  /**
   * Export data for Power BI
   */
  async exportForPowerBI(params: {
    startDate: Date;
    endDate: Date;
    tables: string[];
  }): Promise<string> {
    const data: any = {};

    if (params.tables.includes('tickets')) {
      data.tickets = await this.exportTickets(params.startDate, params.endDate);
    }

    if (params.tables.includes('agents')) {
      data.agents = await this.exportAgents();
    }

    if (params.tables.includes('feedback')) {
      data.feedback = await this.exportFeedback(params.startDate, params.endDate);
    }

    return JSON.stringify(data, null, 2);
  }

  /**
   * Export tickets
   */
  private async exportTickets(startDate: Date, endDate: Date): Promise<any[]> {
    const tickets = await prisma.ticket.findMany({
      where: {
        createdAt: {
          gte: startDate,
          lte: endDate,
        },
      },
      include: {
        requester: true,
        assignee: true,
        comments: true,
        sla: true,
      },
    });

    return tickets.map(t => ({
      id: t.id,
      subject: t.subject,
      status: t.status,
      priority: t.priority,
      category: t.category,
      requesterEmail: t.requester?.email,
      assigneeEmail: t.assignee?.email,
      createdAt: t.createdAt,
      resolvedAt: t.resolvedAt,
      responseTime: t.sla?.responseAt,
      resolutionTime: t.sla?.resolutionAt,
      responseMet: t.sla?.responseMet,
      resolutionMet: t.sla?.resolutionMet,
    }));
  }

  /**
   * Export agents
   */
  private async exportAgents(): Promise<any[]> {
    const agents = await prisma.agent.findMany({
      include: {
        tickets: true,
      },
    });

    return agents.map(a => ({
      id: a.id,
      name: a.name,
      email: a.email,
      role: a.role,
      status: a.status,
      currentTickets: a.currentTickets,
      totalTickets: a.tickets.length,
    }));
  }

  /**
   * Export feedback
   */
  private async exportFeedback(startDate: Date, endDate: Date): Promise<any[]> {
    const feedback = await prisma.feedback.findMany({
      where: {
        createdAt: {
          gte: startDate,
          lte: endDate,
        },
      },
      include: {
        ticket: true,
        user: true,
      },
    });

    return feedback.map(f => ({
      id: f.id,
      type: f.type,
      score: f.score,
      ticketId: f.ticketId,
      userId: f.userId,
      comment: f.comment,
      createdAt: f.createdAt,
    }));
  }
}
```

### Tableau Integration

```typescript
class TableauIntegration {
  /**
   * Create data extract
   */
  async createDataExtract(params: {
    startDate: Date;
    endDate: Date;
  }): Promise<string> {
    const analytics = new SupportAnalytics(prisma);
    const metrics = await analytics.calculateMetrics(params.startDate, params.endDate);

    // Create CSV
    const csv = this.convertToCSV(metrics);

    return csv;
  }

  /**
   * Convert to CSV
   */
  private convertToCSV(metrics: any): string {
    const headers = [
      'Date',
      'Total Tickets',
      'New Tickets',
      'Open Tickets',
      'Avg First Response Time (min)',
      'Avg Resolution Time (min)',
      'CSAT Score',
      'NPS Score',
      'Repeat Contact Rate (%)',
      'Churn Rate (%)',
    ];

    const rows = [
      [
        metrics.startDate.toISOString().split('T')[0],
        metrics.ticketVolume,
        metrics.newTickets,
        metrics.openTickets,
        metrics.averageFirstResponseTime.toFixed(2),
        metrics.averageResolutionTime.toFixed(2),
        metrics.csatScore.toFixed(2),
        metrics.npsScore.toFixed(0),
        metrics.repeatContactRate.toFixed(2),
        metrics.churnRate.toFixed(2),
      ],
    ];

    return [headers.join(','), ...rows.map(r => r.join(','))].join('\n');
  }
}
```

---

## Custom Metrics

### Custom Metric Definition

```typescript
interface CustomMetric {
  id: string;
  name: string;
  description: string;
  formula: string;
  type: 'calculated' | 'aggregated';
  aggregation: 'sum' | 'average' | 'count' | 'max' | 'min';
  dataSource: 'tickets' | 'feedback' | 'chat' | 'surveys';
  query: string;
  isActive: boolean;
}

class CustomMetricManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create custom metric
   */
  async createMetric(metric: Omit<CustomMetric, 'id'>): Promise<string> {
    const created = await this.prisma.customMetric.create({
      data: {
        ...metric,
        isActive: true,
      },
    });

    return created.id;
  }

  /**
   * Calculate custom metric
   */
  async calculateMetric(
    metricId: string,
    params: {
      startDate: Date;
      endDate: Date;
    }
  ): Promise<{
    value: number;
    breakdown?: any;
  }> {
    const metric = await this.prisma.customMetric.findUnique({
      where: { id: metricId },
    });

    if (!metric || !metric.isActive) {
      throw new Error('Metric not found or inactive');
    }

    // Get data source
    const data = await this.getDataFromSource(
      metric.dataSource,
      params.startDate,
      params.endDate
    );

    // Execute query
    const values = this.executeQuery(data, metric.query);

    // Apply aggregation
    let value: number;

    switch (metric.aggregation) {
      case 'sum':
        value = values.reduce((sum, v) => sum + v, 0);
        break;
      case 'average':
        value = values.length > 0 ? values.reduce((sum, v) => sum + v, 0) / values.length : 0;
        break;
      case 'count':
        value = values.length;
        break;
      case 'max':
        value = Math.max(...values);
        break;
      case 'min':
        value = Math.min(...values);
        break;
    }

    return { value };
  }

  /**
   * Get data from source
   */
  private async getDataFromSource(
  source: CustomMetric['dataSource'],
  startDate: Date,
  endDate: Date
  ): Promise<any[]> {
    switch (source) {
      case 'tickets':
        return await this.getTicketData(startDate, endDate);
      case 'feedback':
        return await this.getFeedbackData(startDate, endDate);
      case 'chat':
        return await this.getChatData(startDate, endDate);
      case 'surveys':
        return await this.getSurveyData(startDate, endDate);
      default:
        return [];
    }
  }

  private async getTicketData(startDate: Date, endDate: Date): Promise<any[]> {
    return await prisma.ticket.findMany({
      where: {
        createdAt: {
          gte: startDate,
          lte: endDate,
        },
      },
    });
  }

  private async getFeedbackData(startDate: Date, endDate: Date): Promise<any[]> {
    return await prisma.feedback.findMany({
      where: {
        createdAt: {
          gte: startDate,
          lte: endDate,
        },
      },
    });
  }

  private async getChatData(startDate: Date, endDate: Date): Promise<any[]> {
    return await prisma.chatSession.findMany({
      where: {
        startedAt: {
          gte: startDate,
          lte: endDate,
        },
      },
    });
  }

  private async getSurveyData(startDate: Date, endDate: Date): Promise<any[]> {
    return await prisma.surveyResponse.findMany({
      where: {
        submittedAt: {
          gte: startDate,
          lte: endDate,
        },
      },
    });
  }

  /**
   * Execute query
   */
  private executeQuery(data: any[], query: string): number[] {
    // Simple query executor
    // In production, you'd use a proper query parser
    return data.map(d => d.value || 0);
  }
}
```

---

## Best Practices

### Analytics Best Practices

```typescript
// 1. Use consistent time zones
function ensureUTCTimezone(date: Date): Date {
  return new Date(date.toLocaleString('en-US', { timeZone: 'UTC' }));
}

// 2. Cache expensive calculations
const metricsCache = new Map<string, { data: any; timestamp: number }>();

async function getCachedMetrics(
  key: string,
  fetchFn: () => Promise<any>
): Promise<any> {
  const cached = metricsCache.get(key);

  if (cached && Date.now() - cached.timestamp < 5 * 60 * 1000) {
    return cached.data;
  }

  const data = await fetchFn();
  metricsCache.set(key, { data, timestamp: Date.now() });

  return data;
}

// 3. Implement data validation
function validateMetrics(metrics: SupportMetrics): {
  valid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  if (metrics.ticketVolume < 0) {
    errors.push('Ticket volume cannot be negative');
  }

  if (metrics.csatScore < 0 || metrics.csatScore > 5) {
    errors.push('CSAT score must be between 0 and 5');
  }

  if (metrics.npsScore < -100 || metrics.npsScore > 100) {
    errors.push('NPS score must be between -100 and 100');
  }

  if (metrics.averageFirstResponseTime < 0) {
    errors.push('Average first response time cannot be negative');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}

// 4. Use proper data types for metrics
interface MetricDefinition {
  name: string;
  type: 'count' | 'duration' | 'rating' | 'percentage';
  aggregation: 'sum' | 'average' | 'count' | 'max' | 'min';
  unit?: string;
  positiveDirection: 'higher' | 'lower';
}

const metricDefinitions: Record<string, MetricDefinition> = {
  ticketVolume: {
    name: 'Ticket Volume',
    type: 'count',
    aggregation: 'sum',
    positiveDirection: 'lower',
  },
  firstResponseTime: {
    name: 'First Response Time',
    type: 'duration',
    aggregation: 'average',
    positiveDirection: 'lower',
    unit: 'minutes',
  },
  resolutionTime: {
    name: 'Resolution Time',
    type: 'duration',
    aggregation: 'average',
    positiveDirection: 'lower',
    unit: 'minutes',
  },
  csatScore: {
    name: 'CSAT Score',
    type: 'rating',
    aggregation: 'average',
    positiveDirection: 'higher',
    min: 0,
    max: 5,
  },
  npsScore: {
    name: 'NPS Score',
    type: 'rating',
    aggregation: 'average',
    positiveDirection: 'higher',
    min: -100,
    max: 100,
  },
};

// 5. Implement alerting
async function checkAlerts(metrics: SupportMetrics): Promise<void> {
  const alerts: string[] = [];

  // Check response time SLA
  if (metrics.averageFirstResponseTime > 60) {
    alerts.push('Average first response time exceeds 60 minutes');
  }

  // Check resolution time SLA
  if (metrics.averageResolutionTime > 480) {
    alerts.push('Average resolution time exceeds 8 hours');
  }

  // Check CSAT
  if (metrics.csatScore < 3) {
    alerts.push('CSAT score is below 3');
  }

  // Check NPS
  if (metrics.npsScore < 0) {
    alerts.push('NPS score is negative');
  }

  // Check backlog
  if (metrics.backlog > 100) {
    alerts.push('Backlog exceeds 100 tickets');
  }

  if (alerts.length > 0) {
    await sendAlerts(alerts);
  }
}

async function sendAlerts(alerts: string[]): Promise<void> {
  for (const alert of alerts) {
    await slackService.sendMessage({
      channel: '#alerts',
      text: `Support Alert: ${alert}`,
    });
  }
}
```

---

---

## Quick Start

### Support Metrics

```typescript
interface SupportMetrics {
  ticketsCreated: number
  ticketsResolved: number
  avgResolutionTime: number  // hours
  firstResponseTime: number  // hours
  customerSatisfaction: number  // 1-5
  agentProductivity: number  // tickets per day
}

async function calculateSupportMetrics(
  startDate: Date,
  endDate: Date
): Promise<SupportMetrics> {
  const tickets = await db.tickets.findMany({
    where: {
      createdAt: { gte: startDate, lte: endDate }
    }
  })
  
  return {
    ticketsCreated: tickets.length,
    ticketsResolved: tickets.filter(t => t.status === 'resolved').length,
    avgResolutionTime: calculateAvgResolutionTime(tickets),
    firstResponseTime: calculateAvgFirstResponseTime(tickets),
    customerSatisfaction: await calculateAvgSatisfaction(tickets),
    agentProductivity: await calculateAgentProductivity(startDate, endDate)
  }
}
```

---

## Production Checklist

- [ ] **Key Metrics**: Define key support metrics
- [ ] **Data Collection**: Collect support data
- [ ] **Dashboard**: Support analytics dashboard
- [ ] **Real-time Monitoring**: Real-time metrics
- [ ] **Agent Performance**: Agent performance metrics
- [ ] **Trend Analysis**: Trend analysis
- [ ] **Predictive Analytics**: Predictive insights
- [ ] **Reporting**: Automated reporting
- [ ] **BI Integration**: Integrate with BI tools
- [ ] **Custom Metrics**: Custom metrics if needed
- [ ] **Documentation**: Document metrics
- [ ] **Action**: Act on insights

---

## Anti-patterns

### ❌ Don't: Too Many Metrics

```markdown
# ❌ Bad - Metric overload
Metric 1, Metric 2, Metric 3...
# ... 100 metrics
# Can't focus!
```

```markdown
# ✅ Good - Key metrics
- First Response Time
- Resolution Time
- Customer Satisfaction
- Agent Productivity
# 5-10 key metrics
```

### ❌ Don't: No Action

```markdown
# ❌ Bad - Track but don't act
Metrics tracked: 50
Actions taken: 0
```

```markdown
# ✅ Good - Act on insights
Metrics tracked: 50
Actions taken: 15
Improvements: 10
```

---

## Integration Points

- **Ticketing System** (`29-customer-support/ticketing-system/`) - Ticket data
- **Dashboard Design** (`23-business-analytics/dashboard-design/`) - Dashboard layouts
- **KPI Metrics** (`23-business-analytics/kpi-metrics/`) - Key metrics

---

## Further Reading

- [Support Analytics Best Practices](https://www.zendesk.com/blog/support-analytics/)
- [Customer Support Metrics](https://www.intercom.com/blog/customer-support-metrics/)

## Resources

- [Zendesk Explore API](https://developer.zendesk.com/api-reference/)
- [Intercom API](https://developers.intercom.com/)
- [Freshdesk API](https://developers.freshdesk.com/api/)
- [Power BI Documentation](https://docs.microsoft.com/en-us/power-bi/)
- [Tableau Documentation](https://help.tableau.com/)
