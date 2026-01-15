# Contact Management

## Overview

Contact management organizes and tracks interactions with customers and prospects. This guide covers data models, segmentation, enrichment, and GDPR compliance.

## Contact Data Model

```sql
-- contacts table (extended)
CREATE TABLE contacts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  -- Basic info
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  phone VARCHAR(50),
  mobile VARCHAR(50),
  
  -- Professional info
  title VARCHAR(100),
  department VARCHAR(100),
  company_id UUID REFERENCES companies(id),
  
  -- Address
  address_line1 VARCHAR(255),
  address_line2 VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(100),
  postal_code VARCHAR(20),
  country VARCHAR(100),
  
  -- CRM fields
  lifecycle_stage VARCHAR(50),
  lead_status VARCHAR(50),
  lead_source VARCHAR(50),
  owner_id UUID REFERENCES users(id),
  
  -- Social
  linkedin_url VARCHAR(255),
  twitter_handle VARCHAR(100),
  
  -- Engagement
  last_contacted_at TIMESTAMP,
  last_activity_at TIMESTAMP,
  email_opt_in BOOLEAN DEFAULT TRUE,
  
  -- GDPR
  consent_given BOOLEAN DEFAULT FALSE,
  consent_date TIMESTAMP,
  data_processing_consent BOOLEAN DEFAULT FALSE,
  
  -- Custom fields
  custom_fields JSONB,
  
  -- Metadata
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  deleted_at TIMESTAMP,
  
  INDEX idx_email (email),
  INDEX idx_company (company_id),
  INDEX idx_owner (owner_id),
  INDEX idx_lifecycle (lifecycle_stage),
  FULLTEXT idx_search (first_name, last_name, email)
);

-- contact_tags table
CREATE TABLE contact_tags (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(100) UNIQUE NOT NULL,
  color VARCHAR(7),
  
  created_at TIMESTAMP DEFAULT NOW()
);

-- contact_tag_relations table
CREATE TABLE contact_tag_relations (
  contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES contact_tags(id) ON DELETE CASCADE,
  
  created_at TIMESTAMP DEFAULT NOW(),
  
  PRIMARY KEY (contact_id, tag_id)
);

-- contact_lists table
CREATE TABLE contact_lists (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  
  name VARCHAR(255) NOT NULL,
  description TEXT,
  type VARCHAR(50) DEFAULT 'static',
  
  filters JSONB,
  
  created_by UUID REFERENCES users(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- contact_list_members table
CREATE TABLE contact_list_members (
  list_id UUID REFERENCES contact_lists(id) ON DELETE CASCADE,
  contact_id UUID REFERENCES contacts(id) ON DELETE CASCADE,
  
  added_at TIMESTAMP DEFAULT NOW(),
  
  PRIMARY KEY (list_id, contact_id)
);
```

## Contact Segmentation

```typescript
// services/contact-segmentation.service.ts
export class ContactSegmentationService {
  async createStaticList(name: string, contactIds: string[]): Promise<ContactList> {
    const list = await db.contactList.create({
      data: {
        name,
        type: 'static'
      }
    });

    // Add contacts to list
    await db.contactListMember.createMany({
      data: contactIds.map(contactId => ({
        listId: list.id,
        contactId
      }))
    });

    return list;
  }

  async createDynamicList(name: string, filters: ListFilter[]): Promise<ContactList> {
    const list = await db.contactList.create({
      data: {
        name,
        type: 'dynamic',
        filters: JSON.stringify(filters)
      }
    });

    // Populate list based on filters
    await this.refreshDynamicList(list.id);

    return list;
  }

  async refreshDynamicList(listId: string): Promise<void> {
    const list = await db.contactList.findUnique({
      where: { id: listId }
    });

    if (!list || list.type !== 'dynamic') {
      throw new Error('Not a dynamic list');
    }

    const filters = JSON.parse(list.filters as string) as ListFilter[];
    const contacts = await this.getContactsByFilters(filters);

    // Clear existing members
    await db.contactListMember.deleteMany({
      where: { listId }
    });

    // Add new members
    await db.contactListMember.createMany({
      data: contacts.map(contact => ({
        listId,
        contactId: contact.id
      }))
    });
  }

  private async getContactsByFilters(filters: ListFilter[]): Promise<Contact[]> {
    const where: any = {};

    filters.forEach(filter => {
      switch (filter.operator) {
        case 'equals':
          where[filter.field] = filter.value;
          break;
        case 'contains':
          where[filter.field] = { contains: filter.value };
          break;
        case 'greater_than':
          where[filter.field] = { gt: filter.value };
          break;
        case 'less_than':
          where[filter.field] = { lt: filter.value };
          break;
      }
    });

    return db.contact.findMany({ where });
  }
}

interface ListFilter {
  field: string;
  operator: 'equals' | 'contains' | 'greater_than' | 'less_than';
  value: any;
}
```

## Contact Enrichment

```typescript
// services/contact-enrichment.service.ts
import axios from 'axios';

export class ContactEnrichmentService {
  async enrichContact(contactId: string): Promise<Contact> {
    const contact = await db.contact.findUnique({
      where: { id: contactId }
    });

    if (!contact) throw new Error('Contact not found');

    // Enrich with Clearbit
    const enrichedData = await this.enrichWithClearbit(contact.email);

    // Update contact
    return db.contact.update({
      where: { id: contactId },
      data: {
        title: enrichedData.title || contact.title,
        linkedinUrl: enrichedData.linkedin || contact.linkedinUrl,
        twitterHandle: enrichedData.twitter || contact.twitterHandle,
        customFields: {
          ...contact.customFields,
          ...enrichedData.customFields
        }
      }
    });
  }

  private async enrichWithClearbit(email: string): Promise<EnrichedData> {
    try {
      const response = await axios.get(
        `https://person.clearbit.com/v2/combined/find?email=${email}`,
        {
          headers: {
            'Authorization': `Bearer ${process.env.CLEARBIT_API_KEY}`
          }
        }
      );

      const person = response.data.person;
      const company = response.data.company;

      return {
        title: person.employment?.title,
        linkedin: person.linkedin?.handle,
        twitter: person.twitter?.handle,
        customFields: {
          clearbit_id: person.id,
          company_name: company?.name,
          company_domain: company?.domain,
          company_industry: company?.category?.industry
        }
      };
    } catch (error) {
      console.error('Clearbit enrichment failed:', error);
      return {};
    }
  }
}

interface EnrichedData {
  title?: string;
  linkedin?: string;
  twitter?: string;
  customFields?: Record<string, any>;
}
```

## Duplicate Management

```typescript
// services/contact-duplicate.service.ts
export class ContactDuplicateService {
  async findDuplicates(contactId: string): Promise<Contact[]> {
    const contact = await db.contact.findUnique({
      where: { id: contactId }
    });

    if (!contact) return [];

    // Find by email
    const emailDuplicates = await db.contact.findMany({
      where: {
        email: contact.email,
        id: { not: contactId }
      }
    });

    // Find by name + company
    const nameDuplicates = await db.contact.findMany({
      where: {
        firstName: contact.firstName,
        lastName: contact.lastName,
        companyId: contact.companyId,
        id: { not: contactId }
      }
    });

    // Combine and deduplicate
    const allDuplicates = [...emailDuplicates, ...nameDuplicates];
    return Array.from(new Map(allDuplicates.map(c => [c.id, c])).values());
  }

  async mergeContacts(primaryId: string, duplicateIds: string[]): Promise<Contact> {
    const primary = await db.contact.findUnique({
      where: { id: primaryId }
    });

    if (!primary) throw new Error('Primary contact not found');

    const duplicates = await db.contact.findMany({
      where: { id: { in: duplicateIds } }
    });

    // Merge data (prefer non-null values)
    const merged: any = { ...primary };

    duplicates.forEach(duplicate => {
      Object.keys(duplicate).forEach(key => {
        if (duplicate[key] && !merged[key]) {
          merged[key] = duplicate[key];
        }
      });
    });

    // Update primary contact
    const updated = await db.contact.update({
      where: { id: primaryId },
      data: merged
    });

    // Transfer relationships
    await this.transferRelationships(duplicateIds, primaryId);

    // Soft delete duplicates
    await db.contact.updateMany({
      where: { id: { in: duplicateIds } },
      data: { deletedAt: new Date() }
    });

    return updated;
  }

  private async transferRelationships(fromIds: string[], toId: string): Promise<void> {
    await Promise.all([
      // Transfer activities
      db.activity.updateMany({
        where: { contactId: { in: fromIds } },
        data: { contactId: toId }
      }),
      // Transfer tasks
      db.task.updateMany({
        where: { contactId: { in: fromIds } },
        data: { contactId: toId }
      }),
      // Transfer deals
      db.deal.updateMany({
        where: { contactId: { in: fromIds } },
        data: { contactId: toId }
      })
    ]);
  }
}
```

## Bulk Operations

```typescript
// services/contact-bulk.service.ts
export class ContactBulkService {
  async bulkImport(contacts: ImportContactDto[]): Promise<BulkImportResult> {
    const results: BulkImportResult = {
      success: 0,
      failed: 0,
      errors: []
    };

    for (const contactData of contacts) {
      try {
        // Validate
        this.validateContact(contactData);

        // Check for duplicates
        const existing = await db.contact.findUnique({
          where: { email: contactData.email }
        });

        if (existing) {
          // Update existing
          await db.contact.update({
            where: { id: existing.id },
            data: contactData
          });
        } else {
          // Create new
          await db.contact.create({
            data: contactData
          });
        }

        results.success++;
      } catch (error) {
        results.failed++;
        results.errors.push({
          email: contactData.email,
          error: error.message
        });
      }
    }

    return results;
  }

  async bulkExport(filters?: any): Promise<Contact[]> {
    return db.contact.findMany({
      where: filters,
      include: {
        company: true,
        tags: true
      }
    });
  }

  async bulkUpdate(contactIds: string[], updates: Partial<Contact>): Promise<number> {
    const result = await db.contact.updateMany({
      where: { id: { in: contactIds } },
      data: updates
    });

    return result.count;
  }

  async bulkDelete(contactIds: string[]): Promise<number> {
    const result = await db.contact.updateMany({
      where: { id: { in: contactIds } },
      data: { deletedAt: new Date() }
    });

    return result.count;
  }

  private validateContact(contact: ImportContactDto): void {
    if (!contact.email) {
      throw new Error('Email is required');
    }

    if (!this.isValidEmail(contact.email)) {
      throw new Error('Invalid email format');
    }
  }

  private isValidEmail(email: string): boolean {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  }
}

interface ImportContactDto {
  firstName: string;
  lastName: string;
  email: string;
  phone?: string;
  company?: string;
}

interface BulkImportResult {
  success: number;
  failed: number;
  errors: Array<{ email: string; error: string }>;
}
```

## GDPR Compliance

```typescript
// services/contact-gdpr.service.ts
export class ContactGDPRService {
  async recordConsent(contactId: string, consentType: string): Promise<void> {
    await db.contact.update({
      where: { id: contactId },
      data: {
        consentGiven: true,
        consentDate: new Date(),
        dataProcessingConsent: consentType === 'full'
      }
    });

    // Log consent
    await db.consentLog.create({
      data: {
        contactId,
        consentType,
        timestamp: new Date()
      }
    });
  }

  async exportContactData(contactId: string): Promise<ContactDataExport> {
    const contact = await db.contact.findUnique({
      where: { id: contactId },
      include: {
        activities: true,
        tasks: true,
        deals: true
      }
    });

    if (!contact) throw new Error('Contact not found');

    return {
      personalData: contact,
      activities: contact.activities,
      tasks: contact.tasks,
      deals: contact.deals
    };
  }

  async deleteContactData(contactId: string): Promise<void> {
    // Anonymize instead of delete for audit trail
    await db.contact.update({
      where: { id: contactId },
      data: {
        firstName: 'DELETED',
        lastName: 'DELETED',
        email: `deleted_${contactId}@deleted.com`,
        phone: null,
        mobile: null,
        deletedAt: new Date()
      }
    });
  }
}

interface ContactDataExport {
  personalData: Contact;
  activities: Activity[];
  tasks: Task[];
  deals: Deal[];
}
```

## Best Practices

1. **Data Quality** - Validate and clean data
2. **Deduplication** - Prevent and merge duplicates
3. **Enrichment** - Enrich contacts automatically
4. **Segmentation** - Create targeted segments
5. **GDPR** - Comply with data regulations
6. **Bulk Operations** - Support import/export
7. **Search** - Implement full-text search
8. **Tags** - Use tags for organization
9. **Lists** - Support static and dynamic lists
10. **Audit Trail** - Track all changes

## Resources

- [GDPR Compliance](https://gdpr.eu/)
- [Contact Management Best Practices](https://www.salesforce.com/resources/articles/contact-management/)
- [Clearbit API](https://clearbit.com/docs)
