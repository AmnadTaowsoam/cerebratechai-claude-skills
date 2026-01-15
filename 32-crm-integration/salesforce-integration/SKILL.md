# Salesforce Integration

## Overview

Salesforce is a leading CRM platform with comprehensive APIs for integration. This guide covers REST API, SOAP API, Bulk API, authentication, and common integration patterns.

## Salesforce API Overview

### API Types

| API | Use Case | Limits |
|-----|----------|--------|
| **REST API** | CRUD operations, queries | 15,000 calls/24hrs |
| **SOAP API** | Enterprise integrations | 15,000 calls/24hrs |
| **Bulk API** | Large data operations | 10,000 batches/24hrs |
| **Streaming API** | Real-time events | 40 events/sec |
| **Metadata API** | Deploy customizations | N/A |

## Authentication

### OAuth 2.0 Web Server Flow

```typescript
// services/salesforce-auth.service.ts
import axios from 'axios';

export class SalesforceAuthService {
  private clientId = process.env.SALESFORCE_CLIENT_ID!;
  private clientSecret = process.env.SALESFORCE_CLIENT_SECRET!;
  private redirectUri = process.env.SALESFORCE_REDIRECT_URI!;
  private loginUrl = 'https://login.salesforce.com';

  getAuthorizationUrl(): string {
    const params = new URLSearchParams({
      response_type: 'code',
      client_id: this.clientId,
      redirect_uri: this.redirectUri,
      scope: 'api refresh_token'
    });

    return `${this.loginUrl}/services/oauth2/authorize?${params}`;
  }

  async getAccessToken(code: string): Promise<TokenResponse> {
    const response = await axios.post(
      `${this.loginUrl}/services/oauth2/token`,
      new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        client_id: this.clientId,
        client_secret: this.clientSecret,
        redirect_uri: this.redirectUri
      })
    );

    return response.data;
  }

  async refreshAccessToken(refreshToken: string): Promise<TokenResponse> {
    const response = await axios.post(
      `${this.loginUrl}/services/oauth2/token`,
      new URLSearchParams({
        grant_type: 'refresh_token',
        refresh_token: refreshToken,
        client_id: this.clientId,
        client_secret: this.clientSecret
      })
    );

    return response.data;
  }
}

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  instance_url: string;
  id: string;
  token_type: string;
  issued_at: string;
  signature: string;
}
```

### JWT Bearer Flow

```typescript
// services/salesforce-jwt-auth.service.ts
import jwt from 'jsonwebtoken';
import axios from 'axios';
import fs from 'fs';

export class SalesforceJWTAuthService {
  private clientId = process.env.SALESFORCE_CLIENT_ID!;
  private username = process.env.SALESFORCE_USERNAME!;
  private privateKey = fs.readFileSync(process.env.SALESFORCE_PRIVATE_KEY_PATH!, 'utf8');
  private loginUrl = 'https://login.salesforce.com';

  async getAccessToken(): Promise<string> {
    const token = jwt.sign(
      {
        iss: this.clientId,
        sub: this.username,
        aud: this.loginUrl,
        exp: Math.floor(Date.now() / 1000) + 300 // 5 minutes
      },
      this.privateKey,
      { algorithm: 'RS256' }
    );

    const response = await axios.post(
      `${this.loginUrl}/services/oauth2/token`,
      new URLSearchParams({
        grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer',
        assertion: token
      })
    );

    return response.data.access_token;
  }
}
```

## REST API

### SOQL Queries

```typescript
// services/salesforce-api.service.ts
import axios, { AxiosInstance } from 'axios';

export class SalesforceAPIService {
  private client: AxiosInstance;
  private instanceUrl: string;

  constructor(accessToken: string, instanceUrl: string) {
    this.instanceUrl = instanceUrl;
    this.client = axios.create({
      baseURL: `${instanceUrl}/services/data/v58.0`,
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      }
    });
  }

  async query<T>(soql: string): Promise<QueryResult<T>> {
    const response = await this.client.get('/query', {
      params: { q: soql }
    });

    return response.data;
  }

  async queryAll<T>(soql: string): Promise<T[]> {
    let records: T[] = [];
    let nextRecordsUrl: string | null = null;

    do {
      const response = nextRecordsUrl
        ? await this.client.get(nextRecordsUrl)
        : await this.client.get('/query', { params: { q: soql } });

      records = records.concat(response.data.records);
      nextRecordsUrl = response.data.nextRecordsUrl || null;
    } while (nextRecordsUrl);

    return records;
  }

  // Example queries
  async getAccounts(): Promise<Account[]> {
    const soql = `
      SELECT Id, Name, Industry, AnnualRevenue, Phone, Website
      FROM Account
      WHERE IsDeleted = false
      ORDER BY CreatedDate DESC
      LIMIT 100
    `;

    const result = await this.query<Account>(soql);
    return result.records;
  }

  async getContactsByAccount(accountId: string): Promise<Contact[]> {
    const soql = `
      SELECT Id, FirstName, LastName, Email, Phone, Title
      FROM Contact
      WHERE AccountId = '${accountId}'
      AND IsDeleted = false
    `;

    const result = await this.query<Contact>(soql);
    return result.records;
  }

  async getOpportunities(stage?: string): Promise<Opportunity[]> {
    let soql = `
      SELECT Id, Name, StageName, Amount, CloseDate, AccountId, Account.Name
      FROM Opportunity
      WHERE IsDeleted = false
    `;

    if (stage) {
      soql += ` AND StageName = '${stage}'`;
    }

    soql += ' ORDER BY CloseDate DESC';

    const result = await this.query<Opportunity>(soql);
    return result.records;
  }
}

interface QueryResult<T> {
  totalSize: number;
  done: boolean;
  records: T[];
  nextRecordsUrl?: string;
}

interface Account {
  Id: string;
  Name: string;
  Industry?: string;
  AnnualRevenue?: number;
  Phone?: string;
  Website?: string;
}

interface Contact {
  Id: string;
  FirstName: string;
  LastName: string;
  Email?: string;
  Phone?: string;
  Title?: string;
}

interface Opportunity {
  Id: string;
  Name: string;
  StageName: string;
  Amount?: number;
  CloseDate: string;
  AccountId: string;
}
```

### CRUD Operations

```typescript
// CRUD operations
export class SalesforceCRUDService {
  constructor(private api: SalesforceAPIService) {}

  // Create
  async createAccount(account: Partial<Account>): Promise<string> {
    const response = await this.api.client.post('/sobjects/Account', account);
    return response.data.id;
  }

  async createContact(contact: Partial<Contact>): Promise<string> {
    const response = await this.api.client.post('/sobjects/Contact', contact);
    return response.data.id;
  }

  async createOpportunity(opportunity: Partial<Opportunity>): Promise<string> {
    const response = await this.api.client.post('/sobjects/Opportunity', opportunity);
    return response.data.id;
  }

  // Read
  async getAccount(id: string): Promise<Account> {
    const response = await this.api.client.get(`/sobjects/Account/${id}`);
    return response.data;
  }

  // Update
  async updateAccount(id: string, updates: Partial<Account>): Promise<void> {
    await this.api.client.patch(`/sobjects/Account/${id}`, updates);
  }

  async updateOpportunityStage(id: string, stage: string): Promise<void> {
    await this.api.client.patch(`/sobjects/Opportunity/${id}`, {
      StageName: stage
    });
  }

  // Delete
  async deleteAccount(id: string): Promise<void> {
    await this.api.client.delete(`/sobjects/Account/${id}`);
  }

  // Upsert (using external ID)
  async upsertAccount(externalId: string, account: Partial<Account>): Promise<void> {
    await this.api.client.patch(
      `/sobjects/Account/ExternalId__c/${externalId}`,
      account
    );
  }
}
```

## Bulk API

```typescript
// services/salesforce-bulk.service.ts
export class SalesforceBulkService {
  constructor(private api: SalesforceAPIService) {}

  async bulkInsert(objectType: string, records: any[]): Promise<string> {
    // Create job
    const job = await this.api.client.post('/jobs/ingest', {
      object: objectType,
      operation: 'insert',
      contentType: 'CSV'
    });

    const jobId = job.data.id;

    // Upload data
    const csv = this.convertToCSV(records);
    await this.api.client.put(`/jobs/ingest/${jobId}/batches`, csv, {
      headers: { 'Content-Type': 'text/csv' }
    });

    // Close job
    await this.api.client.patch(`/jobs/ingest/${jobId}`, {
      state: 'UploadComplete'
    });

    return jobId;
  }

  async getBulkJobStatus(jobId: string): Promise<BulkJobStatus> {
    const response = await this.api.client.get(`/jobs/ingest/${jobId}`);
    return response.data;
  }

  async getBulkJobResults(jobId: string): Promise<any[]> {
    const response = await this.api.client.get(
      `/jobs/ingest/${jobId}/successfulResults`
    );
    return this.parseCSV(response.data);
  }

  private convertToCSV(records: any[]): string {
    if (records.length === 0) return '';

    const headers = Object.keys(records[0]);
    const rows = records.map(record =>
      headers.map(header => record[header]).join(',')
    );

    return [headers.join(','), ...rows].join('\n');
  }

  private parseCSV(csv: string): any[] {
    // Implementation
    return [];
  }
}

interface BulkJobStatus {
  id: string;
  state: string;
  object: string;
  operation: string;
  numberRecordsProcessed: number;
  numberRecordsFailed: number;
}
```

## Common Integration Patterns

### Lead Capture

```typescript
// services/lead-capture.service.ts
export class LeadCaptureService {
  constructor(private salesforce: SalesforceCRUDService) {}

  async captureWebLead(data: WebLeadData): Promise<string> {
    const lead = {
      FirstName: data.firstName,
      LastName: data.lastName,
      Email: data.email,
      Company: data.company,
      Phone: data.phone,
      LeadSource: 'Website',
      Status: 'New',
      Description: data.message
    };

    const leadId = await this.salesforce.createLead(lead);

    // Create task for follow-up
    await this.salesforce.createTask({
      WhoId: leadId,
      Subject: 'Follow up on web inquiry',
      Status: 'Not Started',
      Priority: 'Normal',
      ActivityDate: new Date(Date.now() + 24 * 60 * 60 * 1000) // Tomorrow
    });

    return leadId;
  }

  async convertLead(leadId: string, accountId?: string): Promise<ConvertResult> {
    const response = await this.salesforce.api.client.post(
      '/actions/standard/convertLead',
      {
        leadId,
        accountId,
        convertedStatus: 'Qualified',
        doNotCreateOpportunity: false
      }
    );

    return response.data;
  }
}

interface WebLeadData {
  firstName: string;
  lastName: string;
  email: string;
  company: string;
  phone?: string;
  message?: string;
}

interface ConvertResult {
  accountId: string;
  contactId: string;
  opportunityId: string;
}
```

## Best Practices

1. **Authentication** - Use OAuth 2.0 for user context
2. **Bulk Operations** - Use Bulk API for large datasets
3. **Rate Limiting** - Implement rate limiting
4. **Error Handling** - Handle all Salesforce errors
5. **Field Mapping** - Map external fields to Salesforce
6. **Testing** - Use Sandbox for testing
7. **Monitoring** - Monitor API usage
8. **Security** - Secure credentials
9. **Pagination** - Handle large query results
10. **Idempotency** - Use external IDs for upserts

## Resources

- [Salesforce REST API](https://developer.salesforce.com/docs/atlas.en-us.api_rest.meta/api_rest/)
- [Salesforce SOQL](https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/)
- [Bulk API 2.0](https://developer.salesforce.com/docs/atlas.en-us.api_asynch.meta/api_asynch/)
- [Platform Events](https://developer.salesforce.com/docs/atlas.en-us.platform_events.meta/platform_events/)
