---
name: Ticketing System
description: Managing customer support requests, tracking their lifecycle, assigning them to agents, and ensuring timely resolution with SLA tracking, priority management, and automated routing.
---

# Ticketing System

> **Current Level:** Intermediate  
> **Domain:** Customer Support / Backend

---

## Overview

A ticketing system manages customer support requests, tracks their lifecycle, assigns them to agents, and ensures timely resolution. Effective ticketing systems include automated routing, SLA tracking, priority management, and integration with email and chat systems.

---

## Core Concepts

### Table of Contents

1. [Ticketing System Architecture](#ticketing-system-architecture)
2. [Database Schema](#database-schema)
3. [Ticket Creation and Routing](#ticket-creation-and-routing)
4. [Assignment Logic](#assignment-logic)
5. [Priority Management](#priority-management)
6. [SLA Tracking](#sla-tracking)
7. [Email Integration](#email-integration)
8. [Automated Responses](#automated-responses)
9. [Ticket Search and Filters](#ticket-search-and-filters)
10. [Reporting](#reporting)
11. [API Design](#api-design)
12. [UI Patterns](#ui-patterns)
13. [Best Practices](#best-practices)

---

## Ticketing System Architecture

### System Components

```typescript
interface TicketingSystem {
  ticketManager: TicketManager;
  assignmentEngine: AssignmentEngine;
  slaManager: SLAManager;
  notificationService: NotificationService;
  integrationService: IntegrationService;
  analyticsService: AnalyticsService;
}

// Ticket entity
interface Ticket {
  id: string;
  externalId?: string; // External system ID (e.g., Zendesk)
  subject: string;
  description: string;
  status: TicketStatus;
  priority: TicketPriority;
  category: string;
  subcategory?: string;
  requester: Requester;
  assignee?: Agent;
  assigneeGroup?: string;
  tags: string[];
  customFields: Record<string, any>;
  source: 'email' | 'web' | 'chat' | 'api' | 'phone';
  channel?: string;
  createdAt: Date;
  updatedAt: Date;
  dueDate?: Date;
  resolvedAt?: Date;
  closedAt?: Date;
  sla?: SLA;
}

interface Requester {
  id: string;
  name: string;
  email: string;
  phone?: string;
  userId?: string; // Internal user ID
  organization?: string;
  tier?: 'free' | 'standard' | 'premium' | 'enterprise';
}

interface Agent {
  id: string;
  name: string;
  email: string;
  role: 'agent' | 'supervisor' | 'admin';
  groups: string[];
  skills: string[];
  maxConcurrentTickets: number;
  currentTickets: number;
  status: 'online' | 'away' | 'busy' | 'offline';
}

enum TicketStatus {
  NEW = 'new',
  OPEN = 'open',
  IN_PROGRESS = 'in_progress',
  PENDING = 'pending',
  RESOLVED = 'resolved',
  CLOSED = 'closed',
  CANCELLED = 'cancelled',
}

enum TicketPriority {
  CRITICAL = 'critical',
  HIGH = 'high',
  NORMAL = 'normal',
  LOW = 'low',
}

interface SLA {
  id: string;
  policyId: string;
  responseDue: Date;
  resolutionDue: Date;
  responseMet?: boolean;
  resolutionMet?: boolean;
}
```

---

## Database Schema

```sql
-- Tickets table
CREATE TABLE tickets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  external_id VARCHAR(255),
  subject VARCHAR(500) NOT NULL,
  description TEXT NOT NULL,
  status VARCHAR(50) NOT NULL DEFAULT 'new',
  priority VARCHAR(50) NOT NULL DEFAULT 'normal',
  category VARCHAR(100) NOT NULL,
  subcategory VARCHAR(100),
  requester_id UUID NOT NULL,
  assignee_id UUID REFERENCES agents(id) ON DELETE SET NULL,
  assignee_group VARCHAR(100),
  source VARCHAR(50) NOT NULL,
  channel VARCHAR(100),
  tags TEXT[],
  custom_fields JSONB,
  due_date TIMESTAMP,
  resolved_at TIMESTAMP,
  closed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Requesters table
CREATE TABLE requesters (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  phone VARCHAR(50),
  user_id UUID,
  organization VARCHAR(255),
  tier VARCHAR(50) DEFAULT 'standard',
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Agents table
CREATE TABLE agents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  role VARCHAR(50) NOT NULL DEFAULT 'agent',
  groups TEXT[],
  skills TEXT[],
  max_concurrent_tickets INTEGER DEFAULT 5,
  current_tickets INTEGER DEFAULT 0,
  status VARCHAR(50) NOT NULL DEFAULT 'offline',
  last_active_at TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Ticket comments
CREATE TABLE ticket_comments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ticket_id UUID REFERENCES tickets(id) ON DELETE CASCADE,
  author_id UUID NOT NULL,
  author_type VARCHAR(50) NOT NULL, -- 'requester' or 'agent'
  content TEXT NOT NULL,
  is_internal BOOLEAN DEFAULT FALSE,
  is_public BOOLEAN DEFAULT TRUE,
  attachments JSONB,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Attachments
CREATE TABLE attachments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ticket_id UUID REFERENCES tickets(id) ON DELETE CASCADE,
  comment_id UUID REFERENCES ticket_comments(id) ON DELETE CASCADE,
  file_name VARCHAR(255) NOT NULL,
  file_url VARCHAR(500) NOT NULL,
  file_size INTEGER NOT NULL,
  mime_type VARCHAR(100) NOT NULL,
  uploaded_by UUID NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- SLA policies
CREATE TABLE sla_policies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  conditions JSONB NOT NULL, -- priority, category, tier, etc.
  response_time_hours INTEGER NOT NULL,
  resolution_time_hours INTEGER NOT NULL,
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Ticket SLA
CREATE TABLE ticket_sla (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ticket_id UUID REFERENCES tickets(id) ON DELETE CASCADE,
  policy_id UUID REFERENCES sla_policies(id) ON DELETE SET NULL,
  response_due TIMESTAMP NOT NULL,
  resolution_due TIMESTAMP NOT NULL,
  response_met BOOLEAN,
  resolution_met BOOLEAN,
  response_at TIMESTAMP,
  resolution_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Ticket history
CREATE TABLE ticket_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  ticket_id UUID REFERENCES tickets(id) ON DELETE CASCADE,
  changed_by UUID NOT NULL,
  changed_from JSONB,
  changed_to JSONB,
  change_type VARCHAR(100) NOT NULL, -- 'status', 'priority', 'assignee', etc.
  comment TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_tickets_status ON tickets(status);
CREATE INDEX idx_tickets_priority ON tickets(priority);
CREATE INDEX idx_tickets_assignee ON tickets(assignee_id);
CREATE INDEX idx_tickets_requester ON tickets(requester_id);
CREATE INDEX idx_tickets_created_at ON tickets(created_at);
CREATE INDEX idx_tickets_due_date ON tickets(due_date);
CREATE INDEX idx_ticket_comments_ticket_id ON ticket_comments(ticket_id);
CREATE INDEX idx_ticket_comments_created_at ON ticket_comments(created_at);
CREATE INDEX idx_attachments_ticket_id ON attachments(ticket_id);
CREATE INDEX idx_ticket_history_ticket_id ON ticket_history(ticket_id);
CREATE INDEX idx_ticket_history_created_at ON ticket_history(created_at);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_groups ON agents USING GIN(groups);
```

---

## Ticket Creation and Routing

### Ticket Manager

```typescript
class TicketManager {
  constructor(
    private prisma: PrismaClient,
    private assignmentEngine: AssignmentEngine,
    private slaManager: SLAManager
  ) {}

  /**
   * Create ticket
   */
  async createTicket(params: {
    subject: string;
    description: string;
    requester: {
      name: string;
      email: string;
      phone?: string;
      userId?: string;
      organization?: string;
    };
    category: string;
    subcategory?: string;
    priority?: TicketPriority;
    source: Ticket['source'];
    channel?: string;
    tags?: string[];
    customFields?: Record<string, any>;
  }): Promise<Ticket> {
    // Create or get requester
    const requester = await this.getOrCreateRequester(params.requester);

    // Create ticket
    const ticket = await this.prisma.ticket.create({
      data: {
        subject: params.subject,
        description: params.description,
        status: TicketStatus.NEW,
        priority: params.priority || TicketPriority.NORMAL,
        category: params.category,
        subcategory: params.subcategory,
        requesterId: requester.id,
        source: params.source,
        channel: params.channel,
        tags: params.tags || [],
        customFields: params.customFields || {},
      },
    });

    // Calculate SLA
    const sla = await this.slaManager.calculateSLA(ticket);
    if (sla) {
      await this.prisma.ticketSLA.create({
        data: {
          ticketId: ticket.id,
          policyId: sla.policyId,
          responseDue: sla.responseDue,
          resolutionDue: sla.resolutionDue,
        },
      });
    }

    // Route ticket
    await this.routeTicket(ticket.id);

    // Create history entry
    await this.createHistoryEntry(ticket.id, 'created', null, ticket);

    return ticket;
  }

  /**
   * Route ticket to appropriate agent/group
   */
  private async routeTicket(ticketId: string): Promise<void> {
    const ticket = await this.prisma.ticket.findUnique({
      where: { id: ticketId },
    });

    if (!ticket) throw new Error('Ticket not found');

    // Get assignment
    const assignment = await this.assignmentEngine.assignTicket({
      ticketId: ticket.id,
      category: ticket.category,
      subcategory: ticket.subcategory,
      priority: ticket.priority,
      requesterId: ticket.requesterId,
    });

    if (assignment) {
      // Update ticket with assignment
      await this.prisma.ticket.update({
        where: { id: ticketId },
        data: {
          assigneeId: assignment.agentId,
          assigneeGroup: assignment.groupId,
          status: TicketStatus.OPEN,
        },
      });

      // Update agent's current tickets
      if (assignment.agentId) {
        await this.prisma.agent.update({
          where: { id: assignment.agentId },
          data: { currentTickets: { increment: 1 } },
        });
      }

      // Create history entry
      await this.createHistoryEntry(
        ticketId,
        'assigned',
        { assignee: null },
        { assignee: assignment.agentId || assignment.groupId }
      );

      // Notify agent
      await this.notifyAgent(assignment.agentId, ticketId);
    }
  }

  /**
   * Get or create requester
   */
  private async getOrCreateRequester(requesterData: any): Promise<any> {
    let requester = await this.prisma.requester.findUnique({
      where: { email: requesterData.email },
    });

    if (!requester) {
      requester = await this.prisma.requester.create({
        data: {
          name: requesterData.name,
          email: requesterData.email,
          phone: requesterData.phone,
          userId: requesterData.userId,
          organization: requesterData.organization,
        },
      });
    }

    return requester;
  }

  /**
   * Create history entry
   */
  private async createHistoryEntry(
    ticketId: string,
    changeType: string,
    changedFrom: any,
    changedTo: any,
    comment?: string
  ): Promise<void> {
    await this.prisma.ticketHistory.create({
      data: {
        ticketId,
        changedBy: changedTo?.assigneeId || changedFrom?.assigneeId || 'system',
        changedFrom,
        changedTo,
        changeType,
        comment,
      },
    });
  }

  /**
   * Notify agent
   */
  private async notifyAgent(agentId: string, ticketId: string): Promise<void> {
    // Implement notification logic
    console.log(`Notifying agent ${agentId} about ticket ${ticketId}`);
  }
}
```

---

## Assignment Logic

### Assignment Engine

```typescript
interface AssignmentResult {
  agentId?: string;
  groupId?: string;
  method: 'auto' | 'manual' | 'round_robin' | 'skill_based';
}

class AssignmentEngine {
  constructor(private prisma: PrismaClient) {}

  /**
   * Assign ticket
   */
  async assignTicket(params: {
    ticketId: string;
    category: string;
    subcategory?: string;
    priority: TicketPriority;
    requesterId: string;
  }): Promise<AssignmentResult | null> {
    // Get assignment rules
    const rules = await this.getAssignmentRules(params.category, params.subcategory);

    // Apply rules
    for (const rule of rules) {
      const result = await this.applyRule(rule, params);
      if (result) return result;
    }

    // Fallback to round robin
    return await this.assignByRoundRobin(params);
  }

  /**
   * Get assignment rules for category
   */
  private async getAssignmentRules(
    category: string,
    subcategory?: string
  ): Promise<AssignmentRule[]> {
    const rules = await this.prisma.assignmentRule.findMany({
      where: {
        category,
        subcategory: subcategory || null,
        isActive: true,
      },
      orderBy: { priority: 'desc' },
    });

    return rules;
  }

  /**
   * Apply assignment rule
   */
  private async applyRule(
    rule: AssignmentRule,
    params: any
  ): Promise<AssignmentResult | null> {
    switch (rule.type) {
      case 'specific_agent':
        return this.assignToSpecificAgent(rule.agentId!);
      case 'group':
        return this.assignToGroup(rule.groupId!);
      case 'skill_based':
        return await this.assignBySkill(params);
      case 'least_busy':
        return await this.assignToLeastBusy(rule.groupId);
      default:
        return null;
    }
  }

  /**
   * Assign to specific agent
   */
  private assignToSpecificAgent(agentId: string): AssignmentResult {
    return {
      agentId,
      method: 'auto',
    };
  }

  /**
   * Assign to group
   */
  private assignToGroup(groupId: string): AssignmentResult {
    return {
      groupId,
      method: 'auto',
    };
  }

  /**
   * Assign by skill
   */
  private async assignBySkill(params: any): Promise<AssignmentResult | null> {
    const requiredSkills = await this.getRequiredSkills(params.category, params.subcategory);

    // Find agents with required skills
    const agents = await this.prisma.agent.findMany({
      where: {
        status: 'online',
        currentTickets: { lt: this.prisma.agent.fields.maxConcurrentTickets },
        skills: {
          hasSome: requiredSkills,
        },
      },
    });

    if (agents.length === 0) return null;

    // Sort by least busy
    agents.sort((a, b) => a.currentTickets - b.currentTickets);

    return {
      agentId: agents[0].id,
      method: 'skill_based',
    };
  }

  /**
   * Assign to least busy agent in group
   */
  private async assignToLeastBusy(groupId: string): Promise<AssignmentResult | null> {
    const agents = await this.prisma.agent.findMany({
      where: {
        status: 'online',
        groups: { has: groupId },
        currentTickets: { lt: this.prisma.agent.fields.maxConcurrentTickets },
      },
    });

    if (agents.length === 0) return null;

    agents.sort((a, b) => a.currentTickets - b.currentTickets);

    return {
      agentId: agents[0].id,
      groupId,
      method: 'least_busy',
    };
  }

  /**
   * Assign by round robin
   */
  private async assignByRoundRobin(params: any): Promise<AssignmentResult | null> {
    const agents = await this.prisma.agent.findMany({
      where: {
        status: 'online',
        currentTickets: { lt: this.prisma.agent.fields.maxConcurrentTickets },
      },
    });

    if (agents.length === 0) return null;

    // Get round robin index
    const index = await this.getRoundRobinIndex();
    const agent = agents[index % agents.length];

    return {
      agentId: agent.id,
      method: 'round_robin',
    };
  }

  /**
   * Get required skills for category
   */
  private async getRequiredSkills(
    category: string,
    subcategory?: string
  ): Promise<string[]> {
    const categorySkills = await this.prisma.categorySkill.findMany({
      where: { category, subcategory: subcategory || null },
    });

    return categorySkills.map(cs => cs.skill);
  }

  /**
   * Get round robin index
   */
  private async getRoundRobinIndex(): Promise<number> {
    const counter = await this.prisma.roundRobinCounter.findUnique({
      where: { id: 'default' },
    });

    if (!counter) {
      await this.prisma.roundRobinCounter.create({
        data: { id: 'default', index: 0 },
      });
      return 0;
    }

    const newIndex = (counter.index + 1) % 1000;
    await this.prisma.roundRobinCounter.update({
      where: { id: 'default' },
      data: { index: newIndex },
    });

    return newIndex;
  }
}

interface AssignmentRule {
  id: string;
  type: 'specific_agent' | 'group' | 'skill_based' | 'least_busy';
  category: string;
  subcategory?: string;
  priority: number;
  agentId?: string;
  groupId?: string;
  isActive: boolean;
}
```

---

## Priority Management

### Priority Calculator

```typescript
class PriorityCalculator {
  /**
   * Calculate ticket priority
   */
  calculatePriority(params: {
    userTier?: string;
    category: string;
    subcategory?: string;
    keywords?: string[];
    attachmentsCount?: number;
    previousTickets?: number;
    timeSinceLastTicket?: number;
  }): TicketPriority {
    let score = 0;

    // User tier
    if (params.userTier === 'enterprise') {
      score += 30;
    } else if (params.userTier === 'premium') {
      score += 20;
    } else if (params.userTier === 'standard') {
      score += 10;
    }

    // Category priority
    const categoryPriority = this.getCategoryPriority(params.category, params.subcategory);
    score += categoryPriority;

    // Keywords
    if (params.keywords) {
      const keywordScore = this.getKeywordScore(params.keywords);
      score += keywordScore;
    }

    // Attachments
    if (params.attachmentsCount && params.attachmentsCount > 0) {
      score += 5;
    }

    // Previous tickets
    if (params.previousTickets && params.previousTickets > 5) {
      score += 10;
    }

    // Time since last ticket
    if (params.timeSinceLastTicket && params.timeSinceLastTicket < 24 * 60 * 60 * 1000) {
      score += 5;
    }

    // Convert score to priority
    if (score >= 80) return TicketPriority.CRITICAL;
    if (score >= 60) return TicketPriority.HIGH;
    if (score >= 40) return TicketPriority.NORMAL;
    return TicketPriority.LOW;
  }

  /**
   * Get category priority
   */
  private getCategoryPriority(category: string, subcategory?: string): number {
    const priorities: Record<string, number> = {
      'billing': 50,
      'technical': 40,
      'account': 30,
      'feature_request': 20,
      'general': 10,
    };

    return priorities[category] || 10;
  }

  /**
   * Get keyword score
   */
  private getKeywordScore(keywords: string[]): number {
    const urgentKeywords = [
      'urgent',
      'emergency',
      'critical',
      'asap',
      'immediate',
      'broken',
      'down',
      'error',
      'cannot access',
      'not working',
    ];

    let score = 0;
    for (const keyword of keywords) {
      if (urgentKeywords.some(uk => keyword.toLowerCase().includes(uk))) {
        score += 15;
      }
    }

    return score;
  }
}
```

---

## SLA Tracking

### SLA Manager

```typescript
class SLAManager {
  constructor(private prisma: PrismaClient) {}

  /**
   * Calculate SLA for ticket
   */
  async calculateSLA(ticket: Ticket): Promise<SLA | null> {
    // Get applicable policy
    const policy = await this.getApplicablePolicy(ticket);
    if (!policy) return null;

    // Calculate due dates
    const now = new Date();
    const responseDue = new Date(now.getTime() + policy.responseTimeHours * 60 * 60 * 1000);
    const resolutionDue = new Date(now.getTime() + policy.resolutionTimeHours * 60 * 60 * 1000);

    return {
      id: '',
      policyId: policy.id,
      responseDue,
      resolutionDue,
    };
  }

  /**
   * Get applicable SLA policy
   */
  private async getApplicablePolicy(ticket: Ticket): Promise<SLAPolicy | null> {
    const policies = await this.prisma.slaPolicy.findMany({
      where: { isActive: true },
    });

    for (const policy of policies) {
      if (this.matchesPolicy(policy, ticket)) {
        return policy;
      }
    }

    return null;
  }

  /**
   * Check if policy matches ticket
   */
  private matchesPolicy(policy: SLAPolicy, ticket: Ticket): boolean {
    const conditions = policy.conditions;

    // Check priority
    if (conditions.priorities && !conditions.priorities.includes(ticket.priority)) {
      return false;
    }

    // Check category
    if (conditions.categories && !conditions.categories.includes(ticket.category)) {
      return false;
    }

    // Check user tier
    if (conditions.tiers && !conditions.tiers.includes(ticket.requester.tier)) {
      return false;
    }

    return true;
  }

  /**
   * Check SLA compliance
   */
  async checkSLACompliance(ticketId: string): Promise<{
    responseMet: boolean;
    resolutionMet: boolean;
    responseOverdue?: number;
    resolutionOverdue?: number;
  }> {
    const ticketSLA = await this.prisma.ticketSLA.findUnique({
      where: { ticketId },
    });

    if (!ticketSLA) {
      return { responseMet: true, resolutionMet: true };
    }

    const now = new Date();
    const responseOverdue = Math.max(
      0,
      (now.getTime() - ticketSLA.responseDue.getTime()) / (1000 * 60 * 60)
    );
    const resolutionOverdue = Math.max(
      0,
      (now.getTime() - ticketSLA.resolutionDue.getTime()) / (1000 * 60 * 60)
    );

    const responseMet = responseOverdue === 0 || ticketSLA.responseMet;
    const resolutionMet = resolutionOverdue === 0 || ticketSLA.resolutionMet;

    return {
      responseMet,
      resolutionMet,
      responseOverdue: responseOverdue > 0 ? responseOverdue : undefined,
      resolutionOverdue: resolutionOverdue > 0 ? resolutionOverdue : undefined,
    };
  }

  /**
   * Update SLA on ticket update
   */
  async updateSLA(ticketId: string, updateType: 'response' | 'resolution'): Promise<void> {
    const ticketSLA = await this.prisma.ticketSLA.findUnique({
      where: { ticketId },
    });

    if (!ticketSLA) return;

    const now = new Date();

    if (updateType === 'response' && !ticketSLA.responseAt) {
      await this.prisma.ticketSLA.update({
        where: { ticketId },
        data: {
          responseAt: now,
          responseMet: now <= ticketSLA.responseDue,
        },
      });
    } else if (updateType === 'resolution' && !ticketSLA.resolutionAt) {
      await this.prisma.ticketSLA.update({
        where: { ticketId },
        data: {
          resolutionAt: now,
          resolutionMet: now <= ticketSLA.resolutionDue,
        },
      });
    }
  }
}
```

---

## Email Integration

### Email Ticket Handler

```typescript
import { simpleParser } from 'mailparser';
import { ImapFlow } from 'imapflow';

class EmailTicketHandler {
  private imap: ImapFlow;

  constructor() {
    this.imap = new ImapFlow({
      host: process.env.IMAP_HOST!,
      port: 993,
      secure: true,
      auth: {
        user: process.env.EMAIL_USER!,
        pass: process.env.EMAIL_PASSWORD!,
      },
    });
  }

  /**
   * Start listening for emails
   */
  async start(): Promise<void> {
    await this.imap.connect();

    this.imap.on('mail', async (mail) => {
      await this.processEmail(mail);
    });

    console.log('Email ticket handler started');
  }

  /**
   * Process incoming email
   */
  private async processEmail(mail: any): Promise<void> {
    const parsed = await simpleParser(mail.source);

    // Check if this is a reply to existing ticket
    const existingTicket = await this.findTicketByMessageId(parsed.messageId);

    if (existingTicket) {
      await this.addCommentToTicket(existingTicket.id, parsed);
    } else {
      await this.createTicketFromEmail(parsed);
    }
  }

  /**
   * Find ticket by message ID
   */
  private async findTicketByMessageId(messageId: string): Promise<Ticket | null> {
    const ticket = await this.prisma.ticket.findFirst({
      where: {
        customFields: {
          path: ['emailMessageId'],
          equals: messageId,
        },
      },
    });

    return ticket || null;
  }

  /**
   * Add comment to existing ticket
   */
  private async addCommentToTicket(ticketId: string, email: any): Promise<void> {
    await this.prisma.ticketComment.create({
      data: {
        ticketId,
        authorId: email.from.value.address,
        authorType: 'requester',
        content: email.text || email.html,
        isInternal: false,
        isPublic: true,
      },
    });

    // Update ticket status
    await this.prisma.ticket.update({
      where: { id: ticketId },
      data: {
        status: TicketStatus.OPEN,
        updatedAt: new Date(),
      },
    });
  }

  /**
   * Create ticket from email
   */
  private async createTicketFromEmail(email: any): Promise<void> {
    const ticketManager = new TicketManager(this.prisma, this.assignmentEngine, this.slaManager);

    // Parse priority from subject
    const priority = this.parsePriorityFromSubject(email.subject);

    // Parse category from subject
    const category = this.parseCategoryFromSubject(email.subject);

    await ticketManager.createTicket({
      subject: email.subject,
      description: email.text || email.html,
      requester: {
        name: email.from.value.name || email.from.value.address,
        email: email.from.value.address,
      },
      category,
      priority,
      source: 'email',
      customFields: {
        emailMessageId: email.messageId,
        emailInReplyTo: email.inReplyTo,
        emailReferences: email.references,
      },
    });
  }

  /**
   * Parse priority from subject
   */
  private parsePriorityFromSubject(subject: string): TicketPriority {
    const lowerSubject = subject.toLowerCase();

    if (lowerSubject.includes('[urgent]') || lowerSubject.includes('[critical]')) {
      return TicketPriority.CRITICAL;
    }
    if (lowerSubject.includes('[high]')) {
      return TicketPriority.HIGH;
    }
    if (lowerSubject.includes('[low]')) {
      return TicketPriority.LOW;
    }

    return TicketPriority.NORMAL;
  }

  /**
   * Parse category from subject
   */
  private parseCategoryFromSubject(subject: string): string {
    const lowerSubject = subject.toLowerCase();
    const categoryMatch = lowerSubject.match(/\[([^\]]+)\]/);

    if (categoryMatch) {
      const category = categoryMatch[1];
      const validCategories = ['billing', 'technical', 'account', 'general'];
      if (validCategories.includes(category)) {
        return category;
      }
    }

    return 'general';
  }
}
```

---

## Automated Responses

### Auto-Response Handler

```typescript
class AutoResponseHandler {
  constructor(private prisma: PrismaClient) {}

  /**
   * Send auto-response
   */
  async sendAutoResponse(ticketId: string): Promise<void> {
    const ticket = await this.prisma.ticket.findUnique({
      where: { id: ticketId },
      include: { requester: true },
    });

    if (!ticket) return;

    // Get auto-response template
    const template = await this.getAutoResponseTemplate(ticket);

    if (!template) return;

    // Render template
    const content = this.renderTemplate(template, ticket);

    // Add as comment
    await this.prisma.ticketComment.create({
      data: {
        ticketId,
        authorId: 'system',
        authorType: 'agent',
        content,
        isInternal: false,
        isPublic: true,
      },
    });

    // Send email
    await this.sendEmail(ticket.requester.email, template.subject, content);
  }

  /**
   * Get auto-response template
   */
  private async getAutoResponseTemplate(ticket: Ticket): Promise<AutoResponseTemplate | null> {
    return await this.prisma.autoResponseTemplate.findFirst({
      where: {
        category: ticket.category,
        isActive: true,
      },
    });
  }

  /**
   * Render template
   */
  private renderTemplate(template: AutoResponseTemplate, ticket: Ticket): string {
    let content = template.content;

    // Replace placeholders
    content = content.replace(/\{\{ticket_id\}\}/g, ticket.id);
    content = content.replace(/\{\{ticket_subject\}\}/g, ticket.subject);
    content = content.replace(/\{\{requester_name\}\}/g, ticket.requester.name);

    return content;
  }

  /**
   * Send email
   */
  private async sendEmail(to: string, subject: string, content: string): Promise<void> {
    // Implement email sending
    console.log(`Sending email to ${to}: ${subject}`);
  }
}

interface AutoResponseTemplate {
  id: string;
  category: string;
  subject: string;
  content: string;
  isActive: boolean;
}
```

---

## Ticket Search and Filters

### Search Implementation

```typescript
interface SearchFilters {
  status?: TicketStatus[];
  priority?: TicketPriority[];
  category?: string[];
  assigneeId?: string[];
  requesterId?: string[];
  tags?: string[];
  createdAfter?: Date;
  createdBefore?: Date;
  dueAfter?: Date;
  dueBefore?: Date;
  searchQuery?: string;
  page?: number;
  limit?: number;
  sortBy?: 'createdAt' | 'priority' | 'dueDate';
  sortOrder?: 'asc' | 'desc';
}

class TicketSearch {
  constructor(private prisma: PrismaClient) {}

  /**
   * Search tickets
   */
  async search(filters: SearchFilters): Promise<{
    tickets: Ticket[];
    total: number;
    page: number;
    totalPages: number;
  }> {
    const where = this.buildWhereClause(filters);
    const orderBy = this.buildOrderBy(filters);

    const [tickets, total] = await Promise.all([
      this.prisma.ticket.findMany({
        where,
        orderBy,
        skip: ((filters.page || 1) - 1) * (filters.limit || 20),
        take: filters.limit || 20,
        include: {
          requester: true,
          assignee: true,
        },
      }),
      this.prisma.ticket.count({ where }),
    ]);

    const totalPages = Math.ceil(total / (filters.limit || 20));

    return {
      tickets,
      total,
      page: filters.page || 1,
      totalPages,
    };
  }

  /**
   * Build where clause
   */
  private buildWhereClause(filters: SearchFilters): any {
    const where: any = {};

    if (filters.status && filters.status.length > 0) {
      where.status = { in: filters.status };
    }

    if (filters.priority && filters.priority.length > 0) {
      where.priority = { in: filters.priority };
    }

    if (filters.category && filters.category.length > 0) {
      where.category = { in: filters.category };
    }

    if (filters.assigneeId && filters.assigneeId.length > 0) {
      where.assigneeId = { in: filters.assigneeId };
    }

    if (filters.requesterId && filters.requesterId.length > 0) {
      where.requesterId = { in: filters.requesterId };
    }

    if (filters.tags && filters.tags.length > 0) {
      where.tags = { hasSome: filters.tags };
    }

    if (filters.createdAfter || filters.createdBefore) {
      where.createdAt = {};
      if (filters.createdAfter) where.createdAt.gte = filters.createdAfter;
      if (filters.createdBefore) where.createdAt.lte = filters.createdBefore;
    }

    if (filters.dueAfter || filters.dueBefore) {
      where.dueDate = {};
      if (filters.dueAfter) where.dueDate.gte = filters.dueAfter;
      if (filters.dueBefore) where.dueDate.lte = filters.dueBefore;
    }

    if (filters.searchQuery) {
      where.OR = [
        { subject: { contains: filters.searchQuery, mode: 'insensitive' } },
        { description: { contains: filters.searchQuery, mode: 'insensitive' } },
      ];
    }

    return where;
  }

  /**
   * Build order by
   */
  private buildOrderBy(filters: SearchFilters): any {
    const sortBy = filters.sortBy || 'createdAt';
    const sortOrder = filters.sortOrder || 'desc';

    return {
      [sortBy]: sortOrder,
    };
  }

  /**
   * Get ticket statistics
   */
  async getStatistics(filters: Partial<SearchFilters>): Promise<{
    total: number;
    byStatus: Record<string, number>;
    byPriority: Record<string, number>;
    byCategory: Record<string, number>;
    byAssignee: Record<string, number>;
  }> {
    const where = this.buildWhereClause(filters);

    const [tickets, byStatus, byPriority, byCategory, byAssignee] = await Promise.all([
      this.prisma.ticket.count({ where }),
      this.prisma.ticket.groupBy({
        by: ['status'],
        where,
        _count: true,
      }),
      this.prisma.ticket.groupBy({
        by: ['priority'],
        where,
        _count: true,
      }),
      this.prisma.ticket.groupBy({
        by: ['category'],
        where,
        _count: true,
      }),
      this.prisma.ticket.groupBy({
        by: ['assigneeId'],
        where,
        _count: true,
      }),
    ]);

    return {
      total: tickets,
      byStatus: this.groupByResult(byStatus),
      byPriority: this.groupByResult(byPriority),
      byCategory: this.groupByResult(byCategory),
      byAssignee: this.groupByResult(byAssignee),
    };
  }

  private groupByResult(results: any[]): Record<string, number> {
    return results.reduce((acc, r) => {
      acc[r[Object.keys(r)[0]]] = r._count;
      return acc;
    }, {});
  }
}
```

---

## Reporting

### Ticket Reports

```typescript
interface TicketReport {
  period: {
    start: Date;
    end: Date;
  };
  metrics: {
    totalTickets: number;
    newTickets: number;
    openTickets: number;
    resolvedTickets: number;
    closedTickets: number;
    averageResolutionTime: number;
    averageResponseTime: number;
    slaComplianceRate: number;
  };
  byPriority: Record<string, TicketMetrics>;
  byCategory: Record<string, TicketMetrics>;
  byAgent: Record<string, TicketMetrics>;
}

interface TicketMetrics {
  total: number;
  resolved: number;
  averageResolutionTime: number;
  slaComplianceRate: number;
}

class TicketReporter {
  constructor(private prisma: PrismaClient) {}

  /**
   * Generate ticket report
   */
  async generateReport(params: {
    startDate: Date;
    endDate: Date;
    agentId?: string;
  }): Promise<TicketReport> {
    const where: any = {
      createdAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    if (params.agentId) {
      where.assigneeId = params.agentId;
    }

    const [tickets, byPriority, byCategory, byAgent] = await Promise.all([
      this.prisma.ticket.findMany({
        where,
        include: { sla: true },
      }),
      this.prisma.ticket.groupBy({
        by: ['priority'],
        where,
        _count: true,
      }),
      this.prisma.ticket.groupBy({
        by: ['category'],
        where,
        _count: true,
      }),
      this.prisma.ticket.groupBy({
        by: ['assigneeId'],
        where,
        _count: true,
      }),
    ]);

    const metrics = this.calculateMetrics(tickets);

    return {
      period: {
        start: params.startDate,
        end: params.endDate,
      },
      metrics,
      byPriority: this.calculateByPriority(byPriority, tickets),
      byCategory: this.calculateByCategory(byCategory, tickets),
      byAgent: this.calculateByAgent(byAgent, tickets),
    };
  }

  /**
   * Calculate metrics
   */
  private calculateMetrics(tickets: Ticket[]): any {
    const total = tickets.length;
    const newTickets = tickets.filter(t => t.status === TicketStatus.NEW).length;
    const openTickets = tickets.filter(t => t.status === TicketStatus.OPEN || t.status === TicketStatus.IN_PROGRESS).length;
    const resolvedTickets = tickets.filter(t => t.status === TicketStatus.RESOLVED).length;
    const closedTickets = tickets.filter(t => t.status === TicketStatus.CLOSED).length;

    const resolvedTicketsWithSLA = tickets.filter(t => t.status === TicketStatus.RESOLVED && t.sla?.resolutionMet);
    const averageResolutionTime = this.calculateAverageResolutionTime(resolvedTicketsWithSLA);
    const averageResponseTime = this.calculateAverageResponseTime(tickets);
    const slaComplianceRate = resolvedTicketsWithSLA.length > 0
      ? (resolvedTicketsWithSLA.filter(t => t.sla!.resolutionMet).length / resolvedTicketsWithSLA.length) * 100
      : 0;

    return {
      totalTickets: total,
      newTickets,
      openTickets,
      resolvedTickets,
      closedTickets,
      averageResolutionTime,
      averageResponseTime,
      slaComplianceRate,
    };
  }

  /**
   * Calculate average resolution time
   */
  private calculateAverageResolutionTime(tickets: Ticket[]): number {
    const resolved = tickets.filter(t => t.resolvedAt);

    if (resolved.length === 0) return 0;

    const totalTime = resolved.reduce((sum, t) => {
      return sum + (t.resolvedAt!.getTime() - t.createdAt.getTime());
    }, 0);

    return totalTime / resolved.length;
  }

  /**
   * Calculate average response time
   */
  private calculateAverageResponseTime(tickets: Ticket[]): number {
    const withResponse = tickets.filter(t => {
      // Find first agent comment
      return t.comments?.some((c: any) => c.authorType === 'agent');
    });

    if (withResponse.length === 0) return 0;

    const responseTimes = withResponse.map(t => {
      const firstAgentComment = t.comments?.find((c: any) => c.authorType === 'agent');
      return firstAgentComment.createdAt.getTime() - t.createdAt.getTime();
    });

    return responseTimes.reduce((sum, t) => sum + t, 0) / responseTimes.length;
  }

  private calculateByPriority(groupBy: any[], tickets: Ticket[]): Record<string, TicketMetrics> {
    const result: Record<string, TicketMetrics> = {};

    for (const group of groupBy) {
      const priority = group.priority;
      const priorityTickets = tickets.filter(t => t.priority === priority);
      const resolved = priorityTickets.filter(t => t.status === TicketStatus.RESOLVED);

      result[priority] = {
        total: group._count,
        resolved: resolved.length,
        averageResolutionTime: this.calculateAverageResolutionTime(resolved),
        slaComplianceRate: this.calculateSLAComplianceRate(resolved),
      };
    }

    return result;
  }

  private calculateByCategory(groupBy: any[], tickets: Ticket[]): Record<string, TicketMetrics> {
    const result: Record<string, TicketMetrics> = {};

    for (const group of groupBy) {
      const category = group.category;
      const categoryTickets = tickets.filter(t => t.category === category);
      const resolved = categoryTickets.filter(t => t.status === TicketStatus.RESOLVED);

      result[category] = {
        total: group._count,
        resolved: resolved.length,
        averageResolutionTime: this.calculateAverageResolutionTime(resolved),
        slaComplianceRate: this.calculateSLAComplianceRate(resolved),
      };
    }

    return result;
  }

  private calculateByAgent(groupBy: any[], tickets: Ticket[]): Record<string, TicketMetrics> {
    const result: Record<string, TicketMetrics> = {};

    for (const group of groupBy) {
      const agentId = group.assigneeId;
      if (!agentId) continue;

      const agentTickets = tickets.filter(t => t.assigneeId === agentId);
      const resolved = agentTickets.filter(t => t.status === TicketStatus.RESOLVED);

      result[agentId] = {
        total: group._count,
        resolved: resolved.length,
        averageResolutionTime: this.calculateAverageResolutionTime(resolved),
        slaComplianceRate: this.calculateSLAComplianceRate(resolved),
      };
    }

    return result;
  }

  private calculateSLAComplianceRate(tickets: Ticket[]): number {
    const withSLA = tickets.filter(t => t.sla);
    if (withSLA.length === 0) return 0;

    const met = withSLA.filter(t => t.sla!.resolutionMet).length;
    return (met / withSLA.length) * 100;
  }
}
```

---

## API Design

### REST API Endpoints

```typescript
import express from 'express';
import { body, param, query } from 'express-validator';

const router = express.Router();

// Create ticket
router.post(
  '/tickets',
  [
    body('subject').notEmpty(),
    body('description').notEmpty(),
    body('requester.email').isEmail(),
    body('category').notEmpty(),
  ],
  async (req, res) => {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }

    try {
      const ticketManager = new TicketManager(prisma, assignmentEngine, slaManager);
      const ticket = await ticketManager.createTicket(req.body);
      res.status(201).json(ticket);
    } catch (error) {
      res.status(500).json({ error: 'Failed to create ticket' });
    }
  }
);

// Get tickets
router.get('/tickets', async (req, res) => {
  try {
    const search = new TicketSearch(prisma);
    const result = await search.search(req.query);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch tickets' });
  }
});

// Get ticket by ID
router.get('/tickets/:id', async (req, res) => {
  try {
    const ticket = await prisma.ticket.findUnique({
      where: { id: req.params.id },
      include: {
        requester: true,
        assignee: true,
        comments: {
          include: { author: true },
          orderBy: { createdAt: 'asc' },
        },
        sla: true,
      },
    });

    if (!ticket) {
      return res.status(404).json({ error: 'Ticket not found' });
    }

    res.json(ticket);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch ticket' });
  }
});

// Update ticket
router.patch('/tickets/:id', async (req, res) => {
  try {
    const ticket = await prisma.ticket.update({
      where: { id: req.params.id },
      data: req.body,
    });

    // Create history entry
    await createHistoryEntry(req.params.id, 'updated', null, req.body);

    res.json(ticket);
  } catch (error) {
    res.status(500).json({ error: 'Failed to update ticket' });
  }
});

// Add comment
router.post('/tickets/:id/comments', async (req, res) => {
  try {
    const comment = await prisma.ticketComment.create({
      data: {
        ticketId: req.params.id,
        authorId: req.user.id,
        authorType: 'agent',
        content: req.body.content,
        isInternal: req.body.isInternal || false,
        isPublic: req.body.isPublic !== false,
      },
    });

    // Update ticket status
    await prisma.ticket.update({
      where: { id: req.params.id },
      data: { updatedAt: new Date() },
    });

    res.status(201).json(comment);
  } catch (error) {
    res.status(500).json({ error: 'Failed to add comment' });
  }
});

// Assign ticket
router.post('/tickets/:id/assign', async (req, res) => {
  try {
    const ticket = await prisma.ticket.update({
      where: { id: req.params.id },
      data: {
        assigneeId: req.body.agentId,
        status: TicketStatus.OPEN,
      },
    });

    // Create history entry
    await createHistoryEntry(req.params.id, 'assigned', null, req.body);

    res.json(ticket);
  } catch (error) {
    res.status(500).json({ error: 'Failed to assign ticket' });
  }
});

// Resolve ticket
router.post('/tickets/:id/resolve', async (req, res) => {
  try {
    const ticket = await prisma.ticket.update({
      where: { id: req.params.id },
      data: {
        status: TicketStatus.RESOLVED,
        resolvedAt: new Date(),
      },
    });

    // Update SLA
    await slaManager.updateSLA(req.params.id, 'resolution');

    // Create history entry
    await createHistoryEntry(req.params.id, 'resolved', null, null);

    res.json(ticket);
  } catch (error) {
    res.status(500).json({ error: 'Failed to resolve ticket' });
  }
});

// Close ticket
router.post('/tickets/:id/close', async (req, res) => {
  try {
    const ticket = await prisma.ticket.update({
      where: { id: req.params.id },
      data: {
        status: TicketStatus.CLOSED,
        closedAt: new Date(),
      },
    });

    // Create history entry
    await createHistoryEntry(req.params.id, 'closed', null, null);

    res.json(ticket);
  } catch (error) {
    res.status(500).json({ error: 'Failed to close ticket' });
  }
});

// Get reports
router.get('/reports', async (req, res) => {
  try {
    const reporter = new TicketReporter(prisma);
    const report = await reporter.generateReport({
      startDate: new Date(req.query.startDate as string),
      endDate: new Date(req.query.endDate as string),
      agentId: req.query.agentId as string,
    });
    res.json(report);
  } catch (error) {
    res.status(500).json({ error: 'Failed to generate report' });
  }
});

async function createHistoryEntry(
  ticketId: string,
  changeType: string,
  changedFrom: any,
  changedTo: any
): Promise<void> {
  await prisma.ticketHistory.create({
    data: {
      ticketId,
      changedBy: 'system',
      changedFrom,
      changedTo,
      changeType,
    },
  });
}

export default router;
```

---

## UI Patterns

### React Ticket List Component

```tsx
import React, { useState, useEffect } from 'react';

const TicketList: React.FC = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<SearchFilters>({});
  const [page, setPage] = useState(1);

  useEffect(() => {
    fetchTickets();
  }, [filters, page]);

  const fetchTickets = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/tickets?${new URLSearchParams({
        ...filters,
        page: page.toString(),
      })}`);
      const data = await response.json();
      setTickets(data.tickets);
    } catch (error) {
      console.error('Error fetching tickets:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (key: string, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
    setPage(1);
  };

  const getStatusColor = (status: TicketStatus): string => {
    const colors: Record<TicketStatus, string> = {
      [TicketStatus.NEW]: 'bg-blue-100 text-blue-800',
      [TicketStatus.OPEN]: 'bg-yellow-100 text-yellow-800',
      [TicketStatus.IN_PROGRESS]: 'bg-purple-100 text-purple-800',
      [TicketStatus.PENDING]: 'bg-orange-100 text-orange-800',
      [TicketStatus.RESOLVED]: 'bg-green-100 text-green-800',
      [TicketStatus.CLOSED]: 'bg-gray-100 text-gray-800',
    };
    return colors[status];
  };

  const getPriorityColor = (priority: TicketPriority): string => {
    const colors: Record<TicketPriority, string> = {
      [TicketPriority.CRITICAL]: 'bg-red-100 text-red-800',
      [TicketPriority.HIGH]: 'bg-orange-100 text-orange-800',
      [TicketPriority.NORMAL]: 'bg-blue-100 text-blue-800',
      [TicketPriority.LOW]: 'bg-gray-100 text-gray-800',
    };
    return colors[priority];
  };

  return (
    <div className="ticket-list">
      <div className="filters">
        <select
          value={filters.status}
          onChange={e => handleFilterChange('status', e.target.value)}
        >
          <option value="">All Status</option>
          <option value="new">New</option>
          <option value="open">Open</option>
          <option value="in_progress">In Progress</option>
          <option value="resolved">Resolved</option>
          <option value="closed">Closed</option>
        </select>

        <select
          value={filters.priority}
          onChange={e => handleFilterChange('priority', e.target.value)}
        >
          <option value="">All Priorities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="normal">Normal</option>
          <option value="low">Low</option>
        </select>

        <input
          type="text"
          placeholder="Search tickets..."
          value={filters.searchQuery}
          onChange={e => handleFilterChange('searchQuery', e.target.value)}
        />
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <table className="tickets-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Subject</th>
              <th>Requester</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Assignee</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {tickets.map(ticket => (
              <tr key={ticket.id}>
                <td>{ticket.id.slice(0, 8)}</td>
                <td>
                  <a href={`/tickets/${ticket.id}`}>{ticket.subject}</a>
                </td>
                <td>{ticket.requester.email}</td>
                <td>
                  <span className={`badge ${getStatusColor(ticket.status)}`}>
                    {ticket.status}
                  </span>
                </td>
                <td>
                  <span className={`badge ${getPriorityColor(ticket.priority)}`}>
                    {ticket.priority}
                  </span>
                </td>
                <td>{ticket.assignee?.name || 'Unassigned'}</td>
                <td>{new Date(ticket.createdAt).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      <div className="pagination">
        <button
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
        >
          Previous
        </button>
        <span>Page {page}</span>
        <button
          onClick={() => setPage(p => p + 1)}
        >
          Next
        </button>
      </div>
    </div>
  );
};

export default TicketList;
```

---

## Best Practices

### Ticket Management Best Practices

```typescript
// 1. Always maintain ticket history
async function maintainHistory(
  ticketId: string,
  changeType: string,
  oldValue: any,
  newValue: any
): Promise<void> {
  await prisma.ticketHistory.create({
    data: {
      ticketId,
      changedBy: getCurrentUserId(),
      changedFrom: oldValue,
      changedTo: newValue,
      changeType,
      comment: getChangeComment(changeType, oldValue, newValue),
    },
  });
}

// 2. Use transactions for complex operations
async function assignTicketWithTransaction(
  ticketId: string,
  agentId: string
): Promise<void> {
  await prisma.$transaction(async (tx) => {
    // Update ticket
    await tx.ticket.update({
      where: { id: ticketId },
      data: { assigneeId: agentId },
    });

    // Update agent
    await tx.agent.update({
      where: { id: agentId },
      data: { currentTickets: { increment: 1 } },
    });

    // Create history
    await tx.ticketHistory.create({
      data: {
        ticketId,
        changedBy: agentId,
        changedFrom: { assigneeId: null },
        changedTo: { assigneeId: agentId },
        changeType: 'assigned',
      },
    });
  });
}

// 3. Implement soft deletes
async function softDeleteTicket(ticketId: string): Promise<void> {
  await prisma.ticket.update({
    where: { id: ticketId },
    data: {
      status: TicketStatus.CANCELLED,
      deletedAt: new Date(),
    },
  });
}

// 4. Use caching for frequently accessed data
const ticketCache = new Map<string, Ticket>();

async function getCachedTicket(ticketId: string): Promise<Ticket> {
  if (ticketCache.has(ticketId)) {
    return ticketCache.get(ticketId)!;
  }

  const ticket = await prisma.ticket.findUnique({
    where: { id: ticketId },
  });

  if (ticket) {
    ticketCache.set(ticketId, ticket);
  }

  return ticket!;
}

// 5. Implement audit logging
async function logAuditEvent(
  action: string,
  entityType: string,
  entityId: string,
  userId: string,
  changes?: any
): Promise<void> {
  await prisma.auditLog.create({
    data: {
      action,
      entityType,
      entityId,
      userId,
      changes,
      timestamp: new Date(),
      ipAddress: getClientIp(),
      userAgent: getUserAgent(),
    },
  });
}
```

---

---

## Quick Start

### Ticket Creation

```typescript
interface Ticket {
  id: string
  subject: string
  description: string
  priority: 'low' | 'medium' | 'high' | 'urgent'
  status: 'open' | 'in-progress' | 'resolved' | 'closed'
  customerId: string
  assignedTo?: string
  createdAt: Date
  slaDeadline?: Date
}

async function createTicket(ticket: Ticket) {
  const created = await db.tickets.create({
    data: {
      ...ticket,
      slaDeadline: calculateSLADeadline(ticket.priority)
    }
  })
  
  // Auto-assign if rules match
  await autoAssignTicket(created.id)
  
  return created
}
```

### SLA Tracking

```typescript
function calculateSLADeadline(priority: string): Date {
  const slaHours = {
    urgent: 1,
    high: 4,
    medium: 24,
    low: 72
  }
  
  const deadline = new Date()
  deadline.setHours(deadline.getHours() + slaHours[priority])
  return deadline
}
```

---

## Production Checklist

- [ ] **Ticket Creation**: Multiple channels (email, chat, web)
- [ ] **Auto-Routing**: Automatic ticket routing
- [ ] **Assignment Logic**: Smart assignment to agents
- [ ] **Priority Management**: Priority levels and escalation
- [ ] **SLA Tracking**: Track SLA compliance
- [ ] **Email Integration**: Email to ticket conversion
- [ ] **Automated Responses**: Automated acknowledgment
- [ ] **Search**: Full-text search for tickets
- [ ] **Reporting**: Ticket metrics and reports
- [ ] **Integration**: Integrate with CRM and other tools
- [ ] **Documentation**: Document ticket processes
- [ ] **Training**: Train agents on system

---

## Anti-patterns

### ❌ Don't: No SLA Tracking

```typescript
// ❌ Bad - No SLA
const ticket = await createTicket(data)
// No deadline tracking!
```

```typescript
// ✅ Good - SLA tracking
const ticket = await createTicket({
  ...data,
  slaDeadline: calculateSLADeadline(data.priority)
})

// Monitor SLA
setInterval(() => {
  checkSLABreaches()
}, 60000)  // Every minute
```

### ❌ Don't: Manual Assignment Only

```typescript
// ❌ Bad - Manual assignment
// Tickets sit unassigned!
```

```typescript
// ✅ Good - Auto-assignment
async function autoAssignTicket(ticketId: string) {
  const ticket = await getTicket(ticketId)
  const agent = await findBestAgent(ticket)
  
  if (agent) {
    await assignTicket(ticketId, agent.id)
  }
}
```

---

## Integration Points

- **Live Chat** (`29-customer-support/live-chat/`) - Chat to ticket
- **Knowledge Base** (`29-customer-support/knowledge-base/`) - Self-service
- **CRM Integration** (`32-crm-integration/`) - Customer data

---

## Further Reading

- [Zendesk API Documentation](https://developer.zendesk.com/api-reference/)
- [Ticketing System Best Practices](https://www.zendesk.com/blog/ticketing-system-best-practices/)

## Resources
- [Freshdesk API Documentation](https://developers.freshdesk.com/api/)
- [Help Scout API Documentation](https://developer.helpscout.com/)
- [Prisma Documentation](https://www.prisma.io/docs/)
