---
name: Lead Management
description: Tracking potential customers from initial contact through conversion, including lead capture, scoring, qualification, assignment, nurturing, and conversion processes.
---

# Lead Management

> **Current Level:** Intermediate  
> **Domain:** CRM / Sales

---

## Overview

Lead management tracks potential customers from initial contact through conversion. This guide covers lead capture, scoring, qualification, and conversion processes for managing sales pipelines and converting leads into customers effectively.

---

## Lead Lifecycle

```
Capture → Score → Qualify → Assign → Nurture → Convert
```

**Stages:**
1. **New** - Just captured
2. **Contacted** - Initial outreach made
3. **Qualified** - Meets criteria
4. **Unqualified** - Doesn't meet criteria
5. **Converted** - Became customer

## Database Schema

```sql
-- leads table
CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  phone VARCHAR(50),
  company VARCHAR(255),
  
  title VARCHAR(100),
  industry VARCHAR(100),
  employee_count INTEGER,
  annual_revenue DECIMAL(15, 2),
  
  lead_source VARCHAR(50),
  lead_status VARCHAR(50) DEFAULT 'new',
  
  score INTEGER DEFAULT 0,
  grade VARCHAR(10),
  
  qualified BOOLEAN DEFAULT FALSE,
  qualified_at TIMESTAMP,
  
  assigned_to UUID REFERENCES users(id),
  assigned_at TIMESTAMP,
  
  converted BOOLEAN DEFAULT FALSE,
  converted_at TIMESTAMP,
  contact_id UUID REFERENCES contacts(id),
  
  custom_fields JSONB,
  
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_email (email),
  INDEX idx_status (lead_status),
  INDEX idx_assigned (assigned_to),
  INDEX idx_score (score),
  FULLTEXT idx_search (first_name, last_name, email, company)
);

-- lead_scoring_rules table
CREATE TABLE lead_scoring_rules (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  name VARCHAR(255) NOT NULL,
  field VARCHAR(100) NOT NULL,
  operator VARCHAR(50) NOT NULL,
  value VARCHAR(255),
  points INTEGER NOT NULL,
  
  active BOOLEAN DEFAULT TRUE,
  
  created_at TIMESTAMP DEFAULT NOW()
);

-- lead_activities table
CREATE TABLE lead_activities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
  
  type VARCHAR(50) NOT NULL,
  description TEXT,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  
  INDEX idx_lead (lead_id),
  INDEX idx_type (type)
);
```

## Lead Capture

### Form Capture

```typescript
// services/lead-capture.service.ts
export class LeadCaptureService {
  async captureFormLead(data: FormLeadData): Promise<Lead> {
    // Check for existing lead
    const existing = await db.lead.findUnique({
      where: { email: data.email }
    });

    if (existing) {
      // Update existing lead
      return this.updateLead(existing.id, data);
    }

    // Create new lead
    const lead = await db.lead.create({
      data: {
        ...data,
        leadSource: 'website_form',
        leadStatus: 'new'
      }
    });

    // Calculate initial score
    await leadScoringService.calculateScore(lead.id);

    // Auto-assign if rules exist
    await leadAssignmentService.autoAssign(lead.id);

    // Send notification
    await this.notifyNewLead(lead);

    return lead;
  }

  async captureChatLead(data: ChatLeadData): Promise<Lead> {
    const lead = await db.lead.create({
      data: {
        ...data,
        leadSource: 'live_chat',
        leadStatus: 'contacted'
      }
    });

    // Immediate assignment for chat leads
    await leadAssignmentService.assignToAvailable(lead.id);

    return lead;
  }

  async captureAPILead(data: APILeadData): Promise<Lead> {
    const lead = await db.lead.create({
      data: {
        ...data,
        leadSource: data.source || 'api',
        leadStatus: 'new'
      }
    });

    await leadScoringService.calculateScore(lead.id);
    await leadAssignmentService.autoAssign(lead.id);

    return lead;
  }

  private async notifyNewLead(lead: Lead): Promise<void> {
    // Send email notification
    await emailService.send({
      to: lead.assignedTo?.email,
      subject: 'New Lead Assigned',
      template: 'new_lead',
      data: { lead }
    });
  }
}

interface FormLeadData {
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  company?: string;
  message?: string;
}

interface ChatLeadData extends FormLeadData {
  chatTranscript?: string;
}

interface APILeadData extends FormLeadData {
  source?: string;
  customFields?: Record<string, any>;
}
```

## Lead Scoring

```typescript
// services/lead-scoring.service.ts
export class LeadScoringService {
  async calculateScore(leadId: string): Promise<number> {
    const lead = await db.lead.findUnique({ where: { id: leadId } });
    if (!lead) throw new Error('Lead not found');

    let score = 0;

    // Demographic scoring
    score += this.scoreDemographics(lead);

    // Behavioral scoring
    score += await this.scoreBehavior(leadId);

    // Firmographic scoring
    score += this.scoreFirmographics(lead);

    // Update lead score
    await db.lead.update({
      where: { id: leadId },
      data: {
        score,
        grade: this.calculateGrade(score)
      }
    });

    // Check if lead should be auto-qualified
    if (score >= 80) {
      await this.autoQualifyLead(leadId);
    }

    return score;
  }

  private scoreDemographics(lead: Lead): number {
    let score = 0;

    // Job title scoring
    if (lead.title?.includes('Director')) score += 10;
    if (lead.title?.includes('VP')) score += 15;
    if (lead.title?.includes('C-level')) score += 20;

    // Email domain scoring
    if (lead.email?.endsWith('.edu')) score += 5;
    if (lead.email?.endsWith('.gov')) score += 10;

    return score;
  }

  private async scoreBehavior(leadId: string): Promise<number> {
    const activities = await db.leadActivity.findMany({
      where: { leadId }
    });

    let score = 0;

    activities.forEach(activity => {
      switch (activity.type) {
        case 'email_opened':
          score += 2;
          break;
        case 'email_clicked':
          score += 5;
          break;
        case 'page_viewed':
          score += 1;
          break;
        case 'form_submitted':
          score += 10;
          break;
        case 'demo_requested':
          score += 20;
          break;
      }
    });

    return score;
  }

  private scoreFirmographics(lead: Lead): number {
    let score = 0;

    // Company size
    if (lead.employeeCount && lead.employeeCount > 1000) score += 15;
    else if (lead.employeeCount && lead.employeeCount > 100) score += 10;
    else if (lead.employeeCount && lead.employeeCount > 10) score += 5;

    // Revenue
    if (lead.annualRevenue && lead.annualRevenue > 10000000) score += 15;
    else if (lead.annualRevenue && lead.annualRevenue > 1000000) score += 10;

    // Industry
    const targetIndustries = ['Technology', 'Finance', 'Healthcare'];
    if (lead.industry && targetIndustries.includes(lead.industry)) {
      score += 10;
    }

    return score;
  }

  private calculateGrade(score: number): string {
    if (score >= 90) return 'A+';
    if (score >= 80) return 'A';
    if (score >= 70) return 'B';
    if (score >= 60) return 'C';
    if (score >= 50) return 'D';
    return 'F';
  }

  private async autoQualifyLead(leadId: string): Promise<void> {
    await db.lead.update({
      where: { id: leadId },
      data: {
        qualified: true,
        qualifiedAt: new Date(),
        leadStatus: 'qualified'
      }
    });
  }
}
```

## Lead Qualification (BANT)

```typescript
// services/lead-qualification.service.ts
export class LeadQualificationService {
  async qualifyLead(leadId: string, criteria: QualificationCriteria): Promise<boolean> {
    const lead = await db.lead.findUnique({ where: { id: leadId } });
    if (!lead) throw new Error('Lead not found');

    // BANT Framework
    const qualified = this.evaluateBANT(criteria);

    await db.lead.update({
      where: { id: leadId },
      data: {
        qualified,
        qualifiedAt: qualified ? new Date() : null,
        leadStatus: qualified ? 'qualified' : 'unqualified',
        customFields: {
          ...lead.customFields,
          bant: criteria
        }
      }
    });

    if (qualified) {
      await this.createQualifiedLeadTasks(leadId);
    }

    return qualified;
  }

  private evaluateBANT(criteria: QualificationCriteria): boolean {
    const {
      hasBudget,
      hasAuthority,
      hasNeed,
      hasTimeline
    } = criteria;

    // All BANT criteria must be met
    return hasBudget && hasAuthority && hasNeed && hasTimeline;
  }

  private async createQualifiedLeadTasks(leadId: string): Promise<void> {
    await db.task.create({
      data: {
        leadId,
        title: 'Schedule discovery call',
        priority: 'high',
        dueDate: new Date(Date.now() + 24 * 60 * 60 * 1000) // Tomorrow
      }
    });
  }
}

interface QualificationCriteria {
  hasBudget: boolean;
  hasAuthority: boolean;
  hasNeed: boolean;
  hasTimeline: boolean;
  notes?: string;
}
```

## Lead Assignment

```typescript
// services/lead-assignment.service.ts
export class LeadAssignmentService {
  async autoAssign(leadId: string): Promise<void> {
    const lead = await db.lead.findUnique({ where: { id: leadId } });
    if (!lead) throw new Error('Lead not found');

    // Get assignment rules
    const rules = await db.assignmentRule.findMany({
      where: { active: true },
      orderBy: { priority: 'asc' }
    });

    for (const rule of rules) {
      if (this.matchesRule(lead, rule)) {
        await this.assignLead(leadId, rule.assignToUserId);
        return;
      }
    }

    // Round-robin if no rules match
    await this.roundRobinAssign(leadId);
  }

  async assignLead(leadId: string, userId: string): Promise<void> {
    await db.lead.update({
      where: { id: leadId },
      data: {
        assignedTo: userId,
        assignedAt: new Date()
      }
    });

    // Create activity
    await db.leadActivity.create({
      data: {
        leadId,
        type: 'assigned',
        description: `Lead assigned to user ${userId}`
      }
    });
  }

  private async roundRobinAssign(leadId: string): Promise<void> {
    // Get user with least leads
    const users = await db.user.findMany({
      where: { role: 'sales' },
      include: {
        _count: {
          select: { leads: true }
        }
      },
      orderBy: {
        leads: {
          _count: 'asc'
        }
      }
    });

    if (users.length > 0) {
      await this.assignLead(leadId, users[0].id);
    }
  }

  private matchesRule(lead: Lead, rule: AssignmentRule): boolean {
    // Implementation
    return false;
  }
}
```

## Lead Conversion

```typescript
// services/lead-conversion.service.ts
export class LeadConversionService {
  async convertLead(leadId: string, createOpportunity: boolean = true): Promise<ConversionResult> {
    const lead = await db.lead.findUnique({ where: { id: leadId } });
    if (!lead) throw new Error('Lead not found');

    // Create contact
    const contact = await db.contact.create({
      data: {
        firstName: lead.firstName,
        lastName: lead.lastName,
        email: lead.email,
        phone: lead.phone,
        title: lead.title,
        ownerId: lead.assignedTo
      }
    });

    // Create company if needed
    let company = null;
    if (lead.company) {
      company = await db.company.create({
        data: {
          name: lead.company,
          industry: lead.industry,
          employeeCount: lead.employeeCount,
          annualRevenue: lead.annualRevenue,
          ownerId: lead.assignedTo
        }
      });

      // Associate contact with company
      await db.contact.update({
        where: { id: contact.id },
        data: { companyId: company.id }
      });
    }

    // Create opportunity
    let opportunity = null;
    if (createOpportunity) {
      opportunity = await db.deal.create({
        data: {
          name: `${lead.company || lead.lastName} - Opportunity`,
          contactId: contact.id,
          companyId: company?.id,
          ownerId: lead.assignedTo,
          stage: 'qualification'
        }
      });
    }

    // Mark lead as converted
    await db.lead.update({
      where: { id: leadId },
      data: {
        converted: true,
        convertedAt: new Date(),
        contactId: contact.id
      }
    });

    return {
      contactId: contact.id,
      companyId: company?.id,
      opportunityId: opportunity?.id
    };
  }
}

interface ConversionResult {
  contactId: string;
  companyId?: string;
  opportunityId?: string;
}
```

## Best Practices

1. **Lead Capture** - Capture from multiple sources
2. **Lead Scoring** - Implement automated scoring
3. **Qualification** - Use BANT or similar framework
4. **Assignment** - Auto-assign based on rules
5. **Nurturing** - Set up nurture campaigns
6. **Conversion** - Track conversion metrics
7. **Duplicate Detection** - Prevent duplicate leads
8. **Response Time** - Follow up quickly
9. **Analytics** - Track lead metrics
10. **Integration** - Integrate with marketing tools

---

## Quick Start

### Lead Capture

```typescript
async function captureLead(data: LeadData) {
  const lead = await db.leads.create({
    data: {
      email: data.email,
      name: data.name,
      source: data.source,
      status: 'new',
      score: calculateInitialScore(data)
    }
  })
  
  // Trigger automation
  await triggerWorkflow('new-lead', lead.id)
  
  return lead
}
```

### Lead Scoring

```typescript
function calculateLeadScore(lead: Lead): number {
  let score = 0
  
  // Company size
  if (lead.companySize === 'enterprise') score += 30
  else if (lead.companySize === 'mid-market') score += 20
  
  // Engagement
  if (lead.emailOpens > 5) score += 20
  if (lead.websiteVisits > 10) score += 15
  
  // Fit
  if (lead.industry === 'target-industry') score += 25
  
  return Math.min(score, 100)
}
```

---

## Production Checklist

- [ ] **Lead Capture**: Multiple lead capture points
- [ ] **Lead Scoring**: Automated lead scoring
- [ ] **Qualification**: Lead qualification process
- [ ] **Assignment**: Automatic lead assignment
- [ ] **Nurturing**: Lead nurturing workflows
- [ ] **Conversion Tracking**: Track conversions
- [ ] **CRM Integration**: Integrate with CRM
- [ ] **Analytics**: Track lead metrics
- [ ] **Follow-up**: Automated follow-up sequences
- [ ] **Documentation**: Document lead process
- [ ] **Testing**: Test lead workflows
- [ ] **Optimization**: Optimize conversion rates

---

## Anti-patterns

### ❌ Don't: No Lead Scoring

```typescript
// ❌ Bad - All leads treated equally
const leads = await getLeads()
leads.forEach(lead => {
  assignToSales(lead)  // Even unqualified leads!
})
```

```typescript
// ✅ Good - Score and qualify
const leads = await getLeads()
leads.forEach(lead => {
  lead.score = calculateLeadScore(lead)
  if (lead.score >= 70) {
    assignToSales(lead)
  } else {
    addToNurture(lead)
  }
})
```

### ❌ Don't: No Follow-up

```typescript
// ❌ Bad - No follow-up
await captureLead(data)
// Lead forgotten!
```

```typescript
// ✅ Good - Automated follow-up
await captureLead(data)
await scheduleFollowUp(leadId, '1 day')
await scheduleFollowUp(leadId, '1 week')
```

---

## Integration Points

- **Marketing Automation** (`28-marketing-integration/marketing-automation/`) - Lead nurturing
- **Salesforce Integration** (`32-crm-integration/salesforce-integration/`) - CRM sync
- **Email Marketing** (`28-marketing-integration/email-marketing/`) - Email campaigns

---

## Further Reading

- [Lead Management Best Practices](https://www.salesforce.com/resources/articles/lead-management/)
- [Lead Scoring](https://www.hubspot.com/lead-scoring)
- [BANT Framework](https://www.salesforce.com/resources/articles/bant-sales-qualification/)
