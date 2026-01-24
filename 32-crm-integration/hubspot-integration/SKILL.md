---
name: HubSpot Integration
description: Integrating with HubSpot inbound marketing and sales platform using comprehensive APIs for CRM objects, workflows, webhooks, contacts, deals, and marketing automation.
---

# HubSpot Integration

> **Current Level:** Intermediate  
> **Domain:** CRM / Marketing Integration

---

## Overview

HubSpot is an inbound marketing and sales platform with comprehensive APIs. This guide covers CRM objects, workflows, webhooks, and integration patterns for syncing data and automating marketing and sales processes.

## Authentication

### API Key

```typescript
// services/hubspot-auth.service.ts
import axios, { AxiosInstance } from 'axios';

export class HubSpotClient {
  private client: AxiosInstance;

  constructor(apiKey: string) {
    this.client = axios.create({
      baseURL: 'https://api.hubapi.com',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      }
    });
  }
}
```

### OAuth 2.0

```typescript
// services/hubspot-oauth.service.ts
export class HubSpotOAuthService {
  private clientId = process.env.HUBSPOT_CLIENT_ID!;
  private clientSecret = process.env.HUBSPOT_CLIENT_SECRET!;
  private redirectUri = process.env.HUBSPOT_REDIRECT_URI!;

  getAuthorizationUrl(scopes: string[]): string {
    const params = new URLSearchParams({
      client_id: this.clientId,
      redirect_uri: this.redirectUri,
      scope: scopes.join(' ')
    });

    return `https://app.hubspot.com/oauth/authorize?${params}`;
  }

  async getAccessToken(code: string): Promise<TokenResponse> {
    const response = await axios.post(
      'https://api.hubapi.com/oauth/v1/token',
      new URLSearchParams({
        grant_type: 'authorization_code',
        client_id: this.clientId,
        client_secret: this.clientSecret,
        redirect_uri: this.redirectUri,
        code
      })
    );

    return response.data;
  }

  async refreshAccessToken(refreshToken: string): Promise<TokenResponse> {
    const response = await axios.post(
      'https://api.hubapi.com/oauth/v1/token',
      new URLSearchParams({
        grant_type: 'refresh_token',
        client_id: this.clientId,
        client_secret: this.clientSecret,
        refresh_token: refreshToken
      })
    );

    return response.data;
  }
}

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}
```

## CRM Objects

### Contacts

```typescript
// services/hubspot-contacts.service.ts
export class HubSpotContactsService {
  constructor(private client: HubSpotClient) {}

  async createContact(contact: CreateContactDto): Promise<Contact> {
    const response = await this.client.post('/crm/v3/objects/contacts', {
      properties: contact
    });

    return response.data;
  }

  async getContact(contactId: string): Promise<Contact> {
    const response = await this.client.get(`/crm/v3/objects/contacts/${contactId}`);
    return response.data;
  }

  async updateContact(contactId: string, updates: Partial<ContactProperties>): Promise<Contact> {
    const response = await this.client.patch(
      `/crm/v3/objects/contacts/${contactId}`,
      { properties: updates }
    );

    return response.data;
  }

  async deleteContact(contactId: string): Promise<void> {
    await this.client.delete(`/crm/v3/objects/contacts/${contactId}`);
  }

  async searchContacts(filters: SearchFilter[]): Promise<Contact[]> {
    const response = await this.client.post('/crm/v3/objects/contacts/search', {
      filterGroups: [{
        filters
      }],
      sorts: [{ propertyName: 'createdate', direction: 'DESCENDING' }],
      limit: 100
    });

    return response.data.results;
  }

  async getContactByEmail(email: string): Promise<Contact | null> {
    const contacts = await this.searchContacts([{
      propertyName: 'email',
      operator: 'EQ',
      value: email
    }]);

    return contacts.length > 0 ? contacts[0] : null;
  }
}

interface CreateContactDto {
  email: string;
  firstname?: string;
  lastname?: string;
  phone?: string;
  company?: string;
  website?: string;
  lifecyclestage?: string;
}

interface ContactProperties extends CreateContactDto {
  [key: string]: any;
}

interface Contact {
  id: string;
  properties: ContactProperties;
  createdAt: string;
  updatedAt: string;
}

interface SearchFilter {
  propertyName: string;
  operator: 'EQ' | 'NEQ' | 'LT' | 'LTE' | 'GT' | 'GTE' | 'CONTAINS';
  value: string;
}
```

### Companies

```typescript
// services/hubspot-companies.service.ts
export class HubSpotCompaniesService {
  constructor(private client: HubSpotClient) {}

  async createCompany(company: CreateCompanyDto): Promise<Company> {
    const response = await this.client.post('/crm/v3/objects/companies', {
      properties: company
    });

    return response.data;
  }

  async getCompany(companyId: string): Promise<Company> {
    const response = await this.client.get(`/crm/v3/objects/companies/${companyId}`);
    return response.data;
  }

  async associateContactWithCompany(contactId: string, companyId: string): Promise<void> {
    await this.client.put(
      `/crm/v3/objects/contacts/${contactId}/associations/companies/${companyId}/280`
    );
  }
}

interface CreateCompanyDto {
  name: string;
  domain?: string;
  industry?: string;
  phone?: string;
  city?: string;
  state?: string;
}

interface Company {
  id: string;
  properties: CreateCompanyDto & { [key: string]: any };
  createdAt: string;
  updatedAt: string;
}
```

### Deals

```typescript
// services/hubspot-deals.service.ts
export class HubSpotDealsService {
  constructor(private client: HubSpotClient) {}

  async createDeal(deal: CreateDealDto): Promise<Deal> {
    const response = await this.client.post('/crm/v3/objects/deals', {
      properties: deal
    });

    return response.data;
  }

  async getDeal(dealId: string): Promise<Deal> {
    const response = await this.client.get(`/crm/v3/objects/deals/${dealId}`);
    return response.data;
  }

  async updateDealStage(dealId: string, stage: string): Promise<Deal> {
    const response = await this.client.patch(
      `/crm/v3/objects/deals/${dealId}`,
      {
        properties: {
          dealstage: stage
        }
      }
    );

    return response.data;
  }

  async getDealsByStage(stage: string): Promise<Deal[]> {
    const response = await this.client.post('/crm/v3/objects/deals/search', {
      filterGroups: [{
        filters: [{
          propertyName: 'dealstage',
          operator: 'EQ',
          value: stage
        }]
      }]
    });

    return response.data.results;
  }

  async associateDealWithContact(dealId: string, contactId: string): Promise<void> {
    await this.client.put(
      `/crm/v3/objects/deals/${dealId}/associations/contacts/${contactId}/3`
    );
  }
}

interface CreateDealDto {
  dealname: string;
  dealstage: string;
  amount?: number;
  closedate?: string;
  pipeline?: string;
}

interface Deal {
  id: string;
  properties: CreateDealDto & { [key: string]: any };
  createdAt: string;
  updatedAt: string;
}
```

## Pipelines and Stages

```typescript
// services/hubspot-pipelines.service.ts
export class HubSpotPipelinesService {
  async getPipelines(): Promise<Pipeline[]> {
    const response = await this.client.get('/crm/v3/pipelines/deals');
    return response.data.results;
  }

  async createPipeline(pipeline: CreatePipelineDto): Promise<Pipeline> {
    const response = await this.client.post('/crm/v3/pipelines/deals', pipeline);
    return response.data;
  }

  async getStages(pipelineId: string): Promise<Stage[]> {
    const pipeline = await this.client.get(`/crm/v3/pipelines/deals/${pipelineId}`);
    return pipeline.data.stages;
  }

  async createStage(pipelineId: string, stage: CreateStageDto): Promise<Stage> {
    const response = await this.client.post(
      `/crm/v3/pipelines/deals/${pipelineId}/stages`,
      stage
    );

    return response.data;
  }
}

interface Pipeline {
  id: string;
  label: string;
  displayOrder: number;
  stages: Stage[];
}

interface Stage {
  id: string;
  label: string;
  displayOrder: number;
  metadata: {
    probability?: number;
  };
}

interface CreatePipelineDto {
  label: string;
  displayOrder: number;
  stages: CreateStageDto[];
}

interface CreateStageDto {
  label: string;
  displayOrder: number;
  metadata?: {
    probability?: number;
  };
}
```

## Webhooks

```typescript
// services/hubspot-webhooks.service.ts
import crypto from 'crypto';
import express from 'express';

export class HubSpotWebhooksService {
  private webhookSecret = process.env.HUBSPOT_WEBHOOK_SECRET!;

  setupWebhookEndpoint(app: express.Application): void {
    app.post('/webhooks/hubspot', express.json(), async (req, res) => {
      // Verify signature
      if (!this.verifySignature(req)) {
        return res.status(401).send('Invalid signature');
      }

      const events = req.body;

      for (const event of events) {
        await this.handleWebhookEvent(event);
      }

      res.json({ success: true });
    });
  }

  private verifySignature(req: express.Request): boolean {
    const signature = req.headers['x-hubspot-signature'] as string;
    const timestamp = req.headers['x-hubspot-request-timestamp'] as string;

    const sourceString = this.webhookSecret + req.body;
    const hash = crypto
      .createHash('sha256')
      .update(sourceString)
      .digest('hex');

    return hash === signature;
  }

  private async handleWebhookEvent(event: WebhookEvent): Promise<void> {
    console.log('Webhook event:', event);

    switch (event.subscriptionType) {
      case 'contact.creation':
        await this.handleContactCreated(event);
        break;

      case 'contact.propertyChange':
        await this.handleContactUpdated(event);
        break;

      case 'deal.creation':
        await this.handleDealCreated(event);
        break;

      case 'deal.propertyChange':
        await this.handleDealUpdated(event);
        break;
    }
  }

  private async handleContactCreated(event: WebhookEvent): Promise<void> {
    // Implementation
  }

  private async handleContactUpdated(event: WebhookEvent): Promise<void> {
    // Implementation
  }

  private async handleDealCreated(event: WebhookEvent): Promise<void> {
    // Implementation
  }

  private async handleDealUpdated(event: WebhookEvent): Promise<void> {
    // Implementation
  }
}

interface WebhookEvent {
  subscriptionType: string;
  objectId: number;
  propertyName?: string;
  propertyValue?: string;
  changeSource?: string;
  eventId: number;
  occurredAt: number;
}
```

## Integration Patterns

### Lead Scoring

```typescript
// services/lead-scoring.service.ts
export class LeadScoringService {
  async calculateLeadScore(contactId: string): Promise<number> {
    const contact = await hubspot.getContact(contactId);
    let score = 0;

    // Demographic scoring
    if (contact.properties.jobtitle?.includes('Director')) score += 10;
    if (contact.properties.jobtitle?.includes('VP')) score += 15;
    if (contact.properties.jobtitle?.includes('C-level')) score += 20;

    // Engagement scoring
    const engagements = await this.getContactEngagements(contactId);
    score += engagements.emails_opened * 2;
    score += engagements.emails_clicked * 5;
    score += engagements.pages_viewed * 1;

    // Update contact score
    await hubspot.updateContact(contactId, {
      hs_lead_score: score.toString()
    });

    return score;
  }

  private async getContactEngagements(contactId: string): Promise<any> {
    // Implementation
    return {
      emails_opened: 0,
      emails_clicked: 0,
      pages_viewed: 0
    };
  }
}
```

## Best Practices

1. **Rate Limiting** - Respect API limits (100 requests/10 seconds)
2. **Batch Operations** - Use batch APIs for bulk operations
3. **Webhooks** - Use webhooks for real-time updates
4. **Error Handling** - Handle all API errors gracefully
5. **OAuth** - Use OAuth for user-specific access
6. **Custom Properties** - Create custom properties as needed
7. **Associations** - Properly associate related objects
8. **Testing** - Test with sandbox account
9. **Monitoring** - Monitor API usage
10. **Security** - Secure API keys and tokens

---

## Quick Start

### HubSpot Client

```typescript
const hubspot = require('@hubspot/api-client')

const client = new hubspot.Client({
  accessToken: process.env.HUBSPOT_API_TOKEN
})

// Create contact
async function createContact(contact: Contact) {
  const response = await client.crm.contacts.basicApi.create({
    properties: {
      firstname: contact.firstName,
      lastname: contact.lastName,
      email: contact.email
    }
  })
  return response
}

// Create deal
async function createDeal(deal: Deal) {
  const response = await client.crm.deals.basicApi.create({
    properties: {
      dealname: deal.name,
      amount: deal.value,
      dealstage: deal.stage,
      pipeline: deal.pipeline
    },
    associations: [{
      to: { id: deal.contactId },
      types: [{
        associationCategory: 'HUBSPOT_DEFINED',
        associationTypeId: 3  // Contact to Deal
      }]
    }]
  })
  return response
}
```

---

## Production Checklist

- [ ] **API Access**: HubSpot API access configured
- [ ] **Authentication**: OAuth or API key setup
- [ ] **Rate Limiting**: Respect API limits
- [ ] **Batch Operations**: Use batch APIs
- [ ] **Webhooks**: Set up webhooks
- [ ] **Error Handling**: Handle API errors
- [ ] **Data Sync**: Sync data bidirectionally
- [ ] **Workflows**: HubSpot workflows
- [ ] **Testing**: Test with HubSpot
- [ ] **Documentation**: Document integration
- [ ] **Monitoring**: Monitor API usage
- [ ] **Support**: HubSpot support access

---

## Anti-patterns

### ❌ Don't: Ignore Rate Limits

```typescript
// ❌ Bad - No rate limiting
for (const contact of contacts) {
  await createContact(contact)  // May hit limits!
}
```

```typescript
// ✅ Good - Rate limiting
const rateLimiter = require('rate-limiter-flexible')
const limiter = new rateLimiter.RateLimiter({
  points: 100,  // 100 requests
  duration: 10  // per 10 seconds
})

for (const contact of contacts) {
  await limiter.consume('hubspot')
  await createContact(contact)
}
```

### ❌ Don't: No Error Handling

```typescript
// ❌ Bad - No error handling
await client.crm.contacts.basicApi.create(contact)
// What if it fails?
```

```typescript
// ✅ Good - Error handling
try {
  await client.crm.contacts.basicApi.create(contact)
} catch (error) {
  if (error.statusCode === 409) {
    // Duplicate contact
    await updateContact(contact)
  } else {
    throw error
  }
}
```

---

## Integration Points

- **Salesforce Integration** (`32-crm-integration/salesforce-integration/`) - Alternative CRM
- **Lead Management** (`32-crm-integration/lead-management/`) - Lead sync
- **Marketing Automation** (`28-marketing-integration/marketing-automation/`) - Marketing sync

---

## Further Reading

- [HubSpot API Documentation](https://developers.hubspot.com/docs/api/overview)
- [CRM API](https://developers.hubspot.com/docs/api/crm/understanding-the-crm)

## Resources
- [Webhooks](https://developers.hubspot.com/docs/api/webhooks)
- [OAuth](https://developers.hubspot.com/docs/api/oauth-quickstart-guide)
