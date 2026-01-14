# Data Retention

## Overview

Comprehensive guide to data retention policy implementation.

## Table of Contents

1. [Retention Policy Design](#retention-policy-design)
2. [Retention Periods by Data Type](#retention-periods-by-data-type)
3. [Automated Deletion](#automated-deletion)
4. [Soft Delete vs Hard Delete](#soft-delete-vs-hard-delete)
5. [Archival Strategies](#archival-strategies)
6. [Backup Retention](#backup-retention)
7. [Legal Hold](#legal-hold)
8. [Compliance Requirements](#compliance-requirements)
9. [Implementation Patterns](#implementation-patterns)
10. [Testing Retention Policies](#testing-retention-policies)
11. [Audit Trails](#audit-trails)

---

## Retention Policy Design

### Policy Definition

```typescript
// retention-policy.ts

export enum RetentionBasis {
  LEGAL_REQUIREMENT = 'legal_requirement',
  BUSINESS_NEED = 'business_need',
  USER_CONSENT = 'user_consent',
  CONTRACTUAL_OBLIGATION = 'contractual_obligation'
}

export interface RetentionPolicy {
  id: string;
  dataType: string;
  retentionPeriod: number; // in days
  retentionBasis: RetentionBasis;
  description: string;
  legalReference?: string;
  exceptions: string[];
  archival: boolean;
  archivalPeriod?: number; // in days
}

export class RetentionPolicyManager {
  private policies: Map<string, RetentionPolicy> = new Map();
  
  createPolicy(policy: Omit<RetentionPolicy, 'id'>): RetentionPolicy {
    const newPolicy: RetentionPolicy = {
      id: this.generateId(),
      ...policy
    };
    
    this.policies.set(newPolicy.dataType, newPolicy);
    
    return newPolicy;
  }
  
  getPolicy(dataType: string): RetentionPolicy | undefined {
    return this.policies.get(dataType);
  }
  
  getAllPolicies(): RetentionPolicy[] {
    return Array.from(this.policies.values());
  }
  
  updatePolicy(dataType: string, updates: Partial<RetentionPolicy>): RetentionPolicy | undefined {
    const policy = this.policies.get(dataType);
    if (!policy) return undefined;
    
    const updated = { ...policy, ...updates };
    this.policies.set(dataType, updated);
    
    return updated;
  }
  
  deletePolicy(dataType: string): boolean {
    return this.policies.delete(dataType);
  }
  
  getRetentionPeriod(dataType: string): number {
    const policy = this.policies.get(dataType);
    return policy ? policy.retentionPeriod : 365; // Default 1 year
  }
  
  shouldArchive(dataType: string): boolean {
    const policy = this.policies.get(dataType);
    return policy ? policy.archival : false;
  }
  
  private generateId(): string {
    return `policy_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

### Default Policies

```typescript
// default-policies.ts
import { RetentionPolicy, RetentionBasis } from './retention-policy';

export class DefaultRetentionPolicies {
  static getPolicies(): RetentionPolicy[] {
    return [
      {
        id: 'policy_1',
        dataType: 'user_profile',
        retentionPeriod: 2555, // 7 years
        retentionBasis: RetentionBasis.LEGAL_REQUIREMENT,
        description: 'User profile data retained for legal compliance',
        legalReference: 'GDPR Article 5(1)(e)',
        exceptions: ['active_users'],
        archival: true,
        archivalPeriod: 1825 // 5 years
      },
      {
        id: 'policy_2',
        dataType: 'authentication_logs',
        retentionPeriod: 365, // 1 year
        retentionBasis: RetentionBasis.BUSINESS_NEED,
        description: 'Authentication logs retained for security analysis',
        exceptions: [],
        archival: true,
        archivalPeriod: 90 // 3 months
      },
      {
        id: 'policy_3',
        dataType: 'transaction_records',
        retentionPeriod: 2555, // 7 years
        retentionBasis: RetentionBasis.LEGAL_REQUIREMENT,
        description: 'Transaction records retained for tax purposes',
        legalReference: 'Tax regulations',
        exceptions: [],
        archival: true,
        archivalPeriod: 1825 // 5 years
      },
      {
        id: 'policy_4',
        dataType: 'user_consent',
        retentionPeriod: 3650, // 10 years
        retentionBasis: RetentionBasis.LEGAL_REQUIREMENT,
        description: 'User consent records retained for GDPR compliance',
        legalReference: 'GDPR Article 30',
        exceptions: [],
        archival: false
      },
      {
        id: 'policy_5',
        dataType: 'analytics_data',
        retentionPeriod: 730, // 2 years
        retentionBasis: RetentionBasis.BUSINESS_NEED,
        description: 'Analytics data retained for business intelligence',
        exceptions: [],
        archival: true,
        archivalPeriod: 365 // 1 year
      },
      {
        id: 'policy_6',
        dataType: 'chat_messages',
        retentionPeriod: 365, // 1 year
        retentionBasis: RetentionBasis.USER_CONSENT,
        description: 'Chat messages retained per user consent',
        exceptions: [],
        archival: false
      },
      {
        id: 'policy_7',
        dataType: 'audit_logs',
        retentionPeriod: 3650, // 10 years
        retentionBasis: RetentionBasis.LEGAL_REQUIREMENT,
        description: 'Audit logs retained for compliance',
        legalReference: 'SOX, HIPAA',
        exceptions: [],
        archival: true,
        archivalPeriod: 1825 // 5 years
      },
      {
        id: 'policy_8',
        dataType: 'email_communications',
        retentionPeriod: 1825, // 5 years
        retentionBasis: RetentionBasis.LEGAL_REQUIREMENT,
        description: 'Email communications retained for legal purposes',
        legalReference: 'Email retention laws',
        exceptions: [],
        archival: true,
        archivalPeriod: 1095 // 3 years
      },
      {
        id: 'policy_9',
        dataType: 'payment_data',
        retentionPeriod: 365, // 1 year
        retentionBasis: RetentionBasis.LEGAL_REQUIREMENT,
        description: 'Payment data retained per PCI DSS',
        legalReference: 'PCI DSS Requirement 3',
        exceptions: [],
        archival: false
      },
      {
        id: 'policy_10',
        dataType: 'support_tickets',
        retentionPeriod: 1825, // 5 years
        retentionBasis: RetentionBasis.BUSINESS_NEED,
        description: 'Support tickets retained for quality assurance',
        exceptions: [],
        archival: true,
        archivalPeriod: 1095 // 3 years
      }
    ];
  }
}
```

---

## Retention Periods by Data Type

### Data Type Classification

```typescript
// data-type-retention.ts

export enum DataType {
  // User Data
  USER_PROFILE = 'user_profile',
  USER_PREFERENCES = 'user_preferences',
  USER_ACTIVITY = 'user_activity',
  
  // Authentication Data
  AUTHENTICATION_LOGS = 'authentication_logs',
  SESSION_DATA = 'session_data',
  
  // Transaction Data
  TRANSACTION_RECORDS = 'transaction_records',
  PAYMENT_DATA = 'payment_data',
  INVOICES = 'invoices',
  
  // Communication Data
  EMAIL_COMMUNICATIONS = 'email_communications',
  CHAT_MESSAGES = 'chat_messages',
  SUPPORT_TICKETS = 'support_tickets',
  
  // Analytics Data
  ANALYTICS_DATA = 'analytics_data',
  USAGE_METRICS = 'usage_metrics',
  BEHAVIORAL_DATA = 'behavioral_data',
  
  // Compliance Data
  USER_CONSENT = 'user_consent',
  AUDIT_LOGS = 'audit_logs',
  PRIVACY_REQUESTS = 'privacy_requests',
  
  // Content Data
  USER_GENERATED_CONTENT = 'user_generated_content',
  COMMENTS = 'comments',
  REVIEWS = 'reviews'
}

export interface DataTypeRetention {
  dataType: DataType;
  retentionPeriod: number; // days
  archival: boolean;
  archivalPeriod?: number;
  legalReference?: string;
}

export class DataTypeRetentionManager {
  private static readonly RETENTION_PERIODS: Map<DataType, DataTypeRetention> = new Map([
    [DataType.USER_PROFILE, {
      dataType: DataType.USER_PROFILE,
      retentionPeriod: 2555, // 7 years
      archival: true,
      archivalPeriod: 1825, // 5 years
      legalReference: 'GDPR Article 5(1)(e)'
    }],
    [DataType.USER_PREFERENCES, {
      dataType: DataType.USER_PREFERENCES,
      retentionPeriod: 3650, // 10 years
      archival: false,
      legalReference: 'User consent'
    }],
    [DataType.USER_ACTIVITY, {
      dataType: DataType.USER_ACTIVITY,
      retentionPeriod: 365, // 1 year
      archival: true,
      archivalPeriod: 90, // 3 months
      legalReference: 'Business need'
    }],
    [DataType.AUTHENTICATION_LOGS, {
      dataType: DataType.AUTHENTICATION_LOGS,
      retentionPeriod: 365, // 1 year
      archival: true,
      archivalPeriod: 90, // 3 months
      legalReference: 'Security best practices'
    }],
    [DataType.SESSION_DATA, {
      dataType: DataType.SESSION_DATA,
      retentionPeriod: 30, // 30 days
      archival: false,
      legalReference: 'Session timeout'
    }],
    [DataType.TRANSACTION_RECORDS, {
      dataType: DataType.TRANSACTION_RECORDS,
      retentionPeriod: 2555, // 7 years
      archival: true,
      archivalPeriod: 1825, // 5 years
      legalReference: 'Tax regulations'
    }],
    [DataType.PAYMENT_DATA, {
      dataType: DataType.PAYMENT_DATA,
      retentionPeriod: 365, // 1 year
      archival: false,
      legalReference: 'PCI DSS Requirement 3'
    }],
    [DataType.INVOICES, {
      dataType: DataType.INVOICES,
      retentionPeriod: 2555, // 7 years
      archival: true,
      archivalPeriod: 1825, // 5 years
      legalReference: 'Tax regulations'
    }],
    [DataType.EMAIL_COMMUNICATIONS, {
      dataType: DataType.EMAIL_COMMUNICATIONS,
      retentionPeriod: 1825, // 5 years
      archival: true,
      archivalPeriod: 1095, // 3 years
      legalReference: 'Email retention laws'
    }],
    [DataType.CHAT_MESSAGES, {
      dataType: DataType.CHAT_MESSAGES,
      retentionPeriod: 365, // 1 year
      archival: false,
      legalReference: 'User consent'
    }],
    [DataType.SUPPORT_TICKETS, {
      dataType: DataType.SUPPORT_TICKETS,
      retentionPeriod: 1825, // 5 years
      archival: true,
      archivalPeriod: 1095, // 3 years
      legalReference: 'Quality assurance'
    }],
    [DataType.ANALYTICS_DATA, {
      dataType: DataType.ANALYTICS_DATA,
      retentionPeriod: 730, // 2 years
      archival: true,
      archivalPeriod: 365, // 1 year
      legalReference: 'Business need'
    }],
    [DataType.USAGE_METRICS, {
      dataType: DataType.USAGE_METRICS,
      retentionPeriod: 365, // 1 year
      archival: true,
      archivalPeriod: 90, // 3 months
      legalReference: 'Business need'
    }],
    [DataType.BEHAVIORAL_DATA, {
      dataType: DataType.BEHAVIORAL_DATA,
      retentionPeriod: 180, // 6 months
      archival: false,
      legalReference: 'User consent'
    }],
    [DataType.USER_CONSENT, {
      dataType: DataType.USER_CONSENT,
      retentionPeriod: 3650, // 10 years
      archival: false,
      legalReference: 'GDPR Article 30'
    }],
    [DataType.AUDIT_LOGS, {
      dataType: DataType.AUDIT_LOGS,
      retentionPeriod: 3650, // 10 years
      archival: true,
      archivalPeriod: 1825, // 5 years
      legalReference: 'SOX, HIPAA'
    }],
    [DataType.PRIVACY_REQUESTS, {
      dataType: DataType.PRIVACY_REQUESTS,
      retentionPeriod: 3650, // 10 years
      archival: false,
      legalReference: 'GDPR Article 12'
    }],
    [DataType.USER_GENERATED_CONTENT, {
      dataType: DataType.USER_GENERATED_CONTENT,
      retentionPeriod: 3650, // 10 years
      archival: true,
      archivalPeriod: 1825, // 5 years
      legalReference: 'User agreement'
    }],
    [DataType.COMMENTS, {
      dataType: DataType.COMMENTS,
      retentionPeriod: 1825, // 5 years
      archival: true,
      archivalPeriod: 1095, // 3 years
      legalReference: 'User agreement'
    }],
    [DataType.REVIEWS, {
      dataType: DataType.REVIEWS,
      retentionPeriod: 1825, // 5 years
      archival: true,
      archivalPeriod: 1095, // 3 years
      legalReference: 'User agreement'
    }]
  ]);
  
  static getRetentionPeriod(dataType: DataType): DataTypeRetention {
    return this.RETENTION_PERIODS.get(dataType)!;
  }
  
  static getAllRetentionPeriods(): DataTypeRetention[] {
    return Array.from(this.RETENTION_PERIODS.values());
  }
}
```

---

## Automated Deletion

### Deletion Service

```typescript
// automated-deletion.ts
import { DataType, DataTypeRetentionManager } from './data-type-retention';
import { Pool } from 'pg';

export class AutomatedDeletionService {
  constructor(
    private pool: Pool
  ) {}
  
  async deleteExpiredData(dataType: DataType): Promise<number> {
    const retention = DataTypeRetentionManager.getRetentionPeriod(dataType);
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - retention.retentionPeriod);
    
    let deletedCount = 0;
    
    switch (dataType) {
      case DataType.USER_ACTIVITY:
        deletedCount = await this.deleteUserActivity(cutoffDate);
        break;
      case DataType.AUTHENTICATION_LOGS:
        deletedCount = await this.deleteAuthenticationLogs(cutoffDate);
        break;
      case DataType.SESSION_DATA:
        deletedCount = await this.deleteSessionData(cutoffDate);
        break;
      case DataType.ANALYTICS_DATA:
        deletedCount = await this.deleteAnalyticsData(cutoffDate);
        break;
      case DataType.USAGE_METRICS:
        deletedCount = await this.deleteUsageMetrics(cutoffDate);
        break;
      case DataType.BEHAVIORAL_DATA:
        deletedCount = await this.deleteBehavioralData(cutoffDate);
        break;
      // Add more cases as needed
    }
    
    return deletedCount;
  }
  
  async deleteAllExpiredData(): Promise<Map<DataType, number>> {
    const results = new Map<DataType, number>();
    
    for (const dataType of Object.values(DataType)) {
      const deletedCount = await this.deleteExpiredData(dataType);
      results.set(dataType, deletedCount);
    }
    
    return results;
  }
  
  private async deleteUserActivity(cutoffDate: Date): Promise<number> {
    const result = await this.pool.query(
      `DELETE FROM user_activity 
       WHERE created_at < $1 
       RETURNING id`,
      [cutoffDate]
    );
    
    return result.rowCount || 0;
  }
  
  private async deleteAuthenticationLogs(cutoffDate: Date): Promise<number> {
    const result = await this.pool.query(
      `DELETE FROM authentication_logs 
       WHERE created_at < $1 
       RETURNING id`,
      [cutoffDate]
    );
    
    return result.rowCount || 0;
  }
  
  private async deleteSessionData(cutoffDate: Date): Promise<number> {
    const result = await this.pool.query(
      `DELETE FROM sessions 
       WHERE created_at < $1 
       RETURNING id`,
      [cutoffDate]
    );
    
    return result.rowCount || 0;
  }
  
  private async deleteAnalyticsData(cutoffDate: Date): Promise<number> {
    const result = await this.pool.query(
      `DELETE FROM analytics_events 
       WHERE created_at < $1 
       RETURNING id`,
      [cutoffDate]
    );
    
    return result.rowCount || 0;
  }
  
  private async deleteUsageMetrics(cutoffDate: Date): Promise<number> {
    const result = await this.pool.query(
      `DELETE FROM usage_metrics 
       WHERE created_at < $1 
       RETURNING id`,
      [cutoffDate]
    );
    
    return result.rowCount || 0;
  }
  
  private async deleteBehavioralData(cutoffDate: Date): Promise<number> {
    const result = await this.pool.query(
      `DELETE FROM behavioral_data 
       WHERE created_at < $1 
       RETURNING id`,
      [cutoffDate]
    );
    
    return result.rowCount || 0;
  }
}
```

### Scheduled Deletion

```typescript
// scheduled-deletion.ts
import cron from 'node-cron';
import { AutomatedDeletionService } from './automated-deletion';
import { DataType } from './data-type-retention';

export class ScheduledDeletionService {
  private deletionService: AutomatedDeletionService;
  private jobs: cron.ScheduledTask[] = [];
  
  constructor(deletionService: AutomatedDeletionService) {
    this.deletionService = deletionService;
  }
  
  start(): void {
    // Run daily at 2 AM
    const dailyJob = cron.schedule('0 2 * * *', async () => {
      console.log('Starting daily data deletion job');
      
      const results = await this.deletionService.deleteAllExpiredData();
      
      for (const [dataType, count] of results.entries()) {
        console.log(`Deleted ${count} records of type ${dataType}`);
      }
      
      console.log('Daily data deletion job completed');
    });
    
    this.jobs.push(dailyJob);
    
    // Run weekly cleanup on Sundays at 3 AM
    const weeklyJob = cron.schedule('0 3 * * 0', async () => {
      console.log('Starting weekly data cleanup job');
      
      await this.cleanupOrphanedData();
      await this.optimizeTables();
      
      console.log('Weekly data cleanup job completed');
    });
    
    this.jobs.push(weeklyJob);
    
    console.log('Scheduled deletion jobs started');
  }
  
  stop(): void {
    for (const job of this.jobs) {
      job.stop();
    }
    
    this.jobs = [];
    
    console.log('Scheduled deletion jobs stopped');
  }
  
  private async cleanupOrphanedData(): Promise<void> {
    // Implementation to cleanup orphaned data
    console.log('Cleaning up orphaned data');
  }
  
  private async optimizeTables(): Promise<void> {
    // Implementation to optimize database tables
    console.log('Optimizing database tables');
  }
}
```

---

## Soft Delete vs Hard Delete

### Delete Strategy

```typescript
// delete-strategy.ts

export enum DeleteStrategy {
  SOFT = 'soft',
  HARD = 'hard',
  HYBRID = 'hybrid'
}

export interface DeleteOptions {
  strategy: DeleteStrategy;
  retainPeriod?: number; // days to retain before hard delete
  notifyUser?: boolean;
  reason?: string;
}

export class DeleteStrategyManager {
  async deleteData(
    dataType: string,
    recordId: string,
    options: DeleteOptions
  ): Promise<void> {
    switch (options.strategy) {
      case DeleteStrategy.SOFT:
        await this.softDelete(dataType, recordId, options);
        break;
      case DeleteStrategy.HARD:
        await this.hardDelete(dataType, recordId, options);
        break;
      case DeleteStrategy.HYBRID:
        await this.hybridDelete(dataType, recordId, options);
        break;
    }
  }
  
  private async softDelete(
    dataType: string,
    recordId: string,
    options: DeleteOptions
  ): Promise<void> {
    // Mark record as deleted but keep it
    console.log(`Soft deleting ${dataType} record ${recordId}`);
    
    if (options.notifyUser) {
      await this.notifyUserOfDeletion(recordId, options.reason);
    }
  }
  
  private async hardDelete(
    dataType: string,
    recordId: string,
    options: DeleteOptions
  ): Promise<void> {
    // Permanently delete record
    console.log(`Hard deleting ${dataType} record ${recordId}`);
    
    if (options.notifyUser) {
      await this.notifyUserOfDeletion(recordId, options.reason);
    }
  }
  
  private async hybridDelete(
    dataType: string,
    recordId: string,
    options: DeleteOptions
  ): Promise<void> {
    // Soft delete first, then hard delete after retain period
    await this.softDelete(dataType, recordId, options);
    
    if (options.retainPeriod) {
      const hardDeleteDate = new Date();
      hardDeleteDate.setDate(hardDeleteDate.getDate() + options.retainPeriod);
      
      await this.scheduleHardDelete(dataType, recordId, hardDeleteDate);
    }
  }
  
  private async notifyUserOfDeletion(recordId: string, reason?: string): Promise<void> {
    // Implementation to notify user
    console.log(`Notifying user about deletion of record ${recordId}`);
  }
  
  private async scheduleHardDelete(
    dataType: string,
    recordId: string,
    date: Date
  ): Promise<void> {
    // Implementation to schedule hard delete
    console.log(`Scheduling hard delete of ${dataType} ${recordId} at ${date.toISOString()}`);
  }
}
```

### Soft Delete Implementation

```sql
-- soft-delete-schema.sql

-- Add deleted_at column to tables
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;
ALTER TABLE user_activity ADD COLUMN deleted_at TIMESTAMPTZ;
ALTER TABLE analytics_events ADD COLUMN deleted_at TIMESTAMPTZ;

-- Create indexes for soft delete queries
CREATE INDEX idx_users_deleted_at ON users(deleted_at) WHERE deleted_at IS NOT NULL;
CREATE INDEX idx_user_activity_deleted_at ON user_activity(deleted_at) WHERE deleted_at IS NOT NULL;
CREATE INDEX idx_analytics_events_deleted_at ON analytics_events(deleted_at) WHERE deleted_at IS NOT NULL;

-- Create view for active records
CREATE VIEW active_users AS
SELECT * FROM users WHERE deleted_at IS NULL;

CREATE VIEW active_user_activity AS
SELECT * FROM user_activity WHERE deleted_at IS NULL;

CREATE VIEW active_analytics_events AS
SELECT * FROM analytics_events WHERE deleted_at IS NULL;
```

```typescript
// soft-delete-service.ts
import { Pool } from 'pg';

export class SoftDeleteService {
  constructor(private pool: Pool) {}
  
  async softDeleteUser(userId: string, reason?: string): Promise<void> {
    await this.pool.query(
      `UPDATE users 
       SET deleted_at = NOW(), deletion_reason = $1 
       WHERE id = $2`,
      [reason, userId]
    );
  }
  
  async restoreUser(userId: string): Promise<void> {
    await this.pool.query(
      `UPDATE users 
       SET deleted_at = NULL, deletion_reason = NULL 
       WHERE id = $1`,
      [userId]
    );
  }
  
  async isUserDeleted(userId: string): Promise<boolean> {
    const result = await this.pool.query(
      'SELECT deleted_at FROM users WHERE id = $1',
      [userId]
    );
    
    if (result.rows.length === 0) return false;
    
    return result.rows[0].deleted_at !== null;
  }
  
  async softDeleteRecord(tableName: string, recordId: string, reason?: string): Promise<void> {
    await this.pool.query(
      `UPDATE ${tableName} 
       SET deleted_at = NOW(), deletion_reason = $1 
       WHERE id = $2`,
      [reason, recordId]
    );
  }
  
  async restoreRecord(tableName: string, recordId: string): Promise<void> {
    await this.pool.query(
      `UPDATE ${tableName} 
       SET deleted_at = NULL, deletion_reason = NULL 
       WHERE id = $1`,
      [recordId]
    );
  }
  
  async getDeletedRecords(tableName: string, limit: number = 100): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM ${tableName} 
       WHERE deleted_at IS NOT NULL 
       ORDER BY deleted_at DESC 
       LIMIT $1`,
      [limit]
    );
    
    return result.rows;
  }
  
  async permanentlyDeleteOldSoftDeletes(tableName: string, days: number = 90): Promise<number> {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    const result = await this.pool.query(
      `DELETE FROM ${tableName} 
       WHERE deleted_at < $1 
       RETURNING id`,
      [cutoffDate]
    );
    
    return result.rowCount || 0;
  }
}
```

---

## Archival Strategies

### Archival Service

```typescript
// archival-service.ts
import { DataType, DataTypeRetentionManager } from './data-type-retention';
import { Pool } from 'pg';

export class ArchivalService {
  constructor(private pool: Pool) {}
  
  async archiveData(dataType: DataType): Promise<number> {
    const retention = DataTypeRetentionManager.getRetentionPeriod(dataType);
    
    if (!retention.archival) {
      console.log(`Archival not configured for ${dataType}`);
      return 0;
    }
    
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - retention.archivalPeriod!);
    
    let archivedCount = 0;
    
    switch (dataType) {
      case DataType.USER_ACTIVITY:
        archivedCount = await this.archiveUserActivity(cutoffDate);
        break;
      case DataType.AUTHENTICATION_LOGS:
        archivedCount = await this.archiveAuthenticationLogs(cutoffDate);
        break;
      case DataType.TRANSACTION_RECORDS:
        archivedCount = await this.archiveTransactionRecords(cutoffDate);
        break;
      case DataType.ANALYTICS_DATA:
        archivedCount = await this.archiveAnalyticsData(cutoffDate);
        break;
      // Add more cases as needed
    }
    
    return archivedCount;
  }
  
  async archiveAllData(): Promise<Map<DataType, number>> {
    const results = new Map<DataType, number>();
    
    for (const dataType of Object.values(DataType)) {
      const retention = DataTypeRetentionManager.getRetentionPeriod(dataType);
      
      if (retention.archival) {
        const archivedCount = await this.archiveData(dataType);
        results.set(dataType, archivedCount);
      }
    }
    
    return results;
  }
  
  private async archiveUserActivity(cutoffDate: Date): Promise<number> {
    const result = await this.pool.query(
      `INSERT INTO user_activity_archive
       SELECT * FROM user_activity 
       WHERE created_at < $1 
       RETURNING id`,
      [cutoffDate]
    );
    
    const archivedCount = result.rowCount || 0;
    
    // Delete from main table
    await this.pool.query(
      `DELETE FROM user_activity 
       WHERE created_at < $1`,
      [cutoffDate]
    );
    
    return archivedCount;
  }
  
  private async archiveAuthenticationLogs(cutoffDate: Date): Promise<number> {
    const result = await this.pool.query(
      `INSERT INTO authentication_logs_archive
       SELECT * FROM authentication_logs 
       WHERE created_at < $1 
       RETURNING id`,
      [cutoffDate]
    );
    
    const archivedCount = result.rowCount || 0;
    
    await this.pool.query(
      `DELETE FROM authentication_logs 
       WHERE created_at < $1`,
      [cutoffDate]
    );
    
    return archivedCount;
  }
  
  private async archiveTransactionRecords(cutoffDate: Date): Promise<number> {
    const result = await this.pool.query(
      `INSERT INTO transaction_records_archive
       SELECT * FROM transaction_records 
       WHERE created_at < $1 
       RETURNING id`,
      [cutoffDate]
    );
    
    const archivedCount = result.rowCount || 0;
    
    await this.pool.query(
      `DELETE FROM transaction_records 
       WHERE created_at < $1`,
      [cutoffDate]
    );
    
    return archivedCount;
  }
  
  private async archiveAnalyticsData(cutoffDate: Date): Promise<number> {
    const result = await this.pool.query(
      `INSERT INTO analytics_events_archive
       SELECT * FROM analytics_events 
       WHERE created_at < $1 
       RETURNING id`,
      [cutoffDate]
    );
    
    const archivedCount = result.rowCount || 0;
    
    await this.pool.query(
      `DELETE FROM analytics_events 
       WHERE created_at < $1`,
      [cutoffDate]
    );
    
    return archivedCount;
  }
}
```

### Archive Table Schema

```sql
-- archive-schema.sql

-- Archive tables (read-only, compressed)
CREATE TABLE user_activity_archive (
  LIKE user_activity INCLUDING ALL
) WITH (autovacuum_enabled = false);

CREATE TABLE authentication_logs_archive (
  LIKE authentication_logs INCLUDING ALL
) WITH (autovacuum_enabled = false);

CREATE TABLE transaction_records_archive (
  LIKE transaction_records INCLUDING ALL
) WITH (autovacuum_enabled = false);

CREATE TABLE analytics_events_archive (
  LIKE analytics_events INCLUDING ALL
) WITH (autovacuum_enabled = false);

-- Partition archive tables by year
CREATE TABLE user_activity_archive_2024 PARTITION OF user_activity_archive
  FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');

CREATE TABLE user_activity_archive_2025 PARTITION OF user_activity_archive
  FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

-- Create indexes on archive tables
CREATE INDEX idx_user_activity_archive_created_at 
  ON user_activity_archive(created_at DESC);

CREATE INDEX idx_authentication_logs_archive_created_at 
  ON authentication_logs_archive(created_at DESC);

CREATE INDEX idx_transaction_records_archive_created_at 
  ON transaction_records_archive(created_at DESC);

CREATE INDEX idx_analytics_events_archive_created_at 
  ON analytics_events_archive(created_at DESC);
```

---

## Backup Retention

### Backup Retention Policy

```typescript
// backup-retention.ts

export enum BackupType {
  FULL = 'full',
  INCREMENTAL = 'incremental',
  DIFFERENTIAL = 'differential'
}

export interface BackupRetentionPolicy {
  backupType: BackupType;
  frequency: string; // cron expression
  retentionPeriod: number; // days
  archival: boolean;
  archivalLocation?: string;
}

export class BackupRetentionPolicyManager {
  private policies: BackupRetentionPolicy[] = [
    {
      backupType: BackupType.FULL,
      frequency: '0 2 * * 0', // Weekly on Sunday at 2 AM
      retentionPeriod: 90, // 3 months
      archival: true,
      archivalLocation: 's3://backups/full'
    },
    {
      backupType: BackupType.INCREMENTAL,
      frequency: '0 2 * * *', // Daily at 2 AM
      retentionPeriod: 30, // 1 month
      archival: false
    },
    {
      backupType: BackupType.DIFFERENTIAL,
      frequency: '0 3 * * 1-6', // Mon-Sat at 3 AM
      retentionPeriod: 60, // 2 months
      archival: true,
      archivalLocation: 's3://backups/differential'
    }
  ];
  
  getPolicies(): BackupRetentionPolicy[] {
    return this.policies;
  }
  
  getPolicy(backupType: BackupType): BackupRetentionPolicy | undefined {
    return this.policies.find(p => p.backupType === backupType);
  }
  
  getRetentionPeriod(backupType: BackupType): number {
    const policy = this.getPolicy(backupType);
    return policy ? policy.retentionPeriod : 30;
  }
  
  shouldArchive(backupType: BackupType): boolean {
    const policy = this.getPolicy(backupType);
    return policy ? policy.archival : false;
  }
}
```

### Backup Cleanup

```typescript
// backup-cleanup.ts
import { BackupRetentionPolicyManager, BackupType } from './backup-retention';

export class BackupCleanupService {
  private policyManager: BackupRetentionPolicyManager;
  
  constructor() {
    this.policyManager = new BackupRetentionPolicyManager();
  }
  
  async cleanupOldBackups(backupType: BackupType): Promise<number> {
    const retentionPeriod = this.policyManager.getRetentionPeriod(backupType);
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - retentionPeriod);
    
    // Implementation to delete old backups
    console.log(`Cleaning up ${backupType} backups older than ${retentionPeriod} days`);
    
    // Return count of deleted backups
    return 0;
  }
  
  async cleanupAllBackups(): Promise<Map<BackupType, number>> {
    const results = new Map<BackupType, number>();
    
    for (const backupType of Object.values(BackupType)) {
      const deletedCount = await this.cleanupOldBackups(backupType);
      results.set(backupType, deletedCount);
    }
    
    return results;
  }
  
  async archiveOldBackups(backupType: BackupType): Promise<number> {
    if (!this.policyManager.shouldArchive(backupType)) {
      console.log(`Archival not configured for ${backupType} backups`);
      return 0;
    }
    
    const retentionPeriod = this.policyManager.getRetentionPeriod(backupType);
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - retentionPeriod);
    
    // Implementation to archive old backups
    console.log(`Archiving ${backupType} backups older than ${retentionPeriod} days`);
    
    // Return count of archived backups
    return 0;
  }
}
```

---

## Legal Hold

### Legal Hold Service

```typescript
// legal-hold.ts

export interface LegalHold {
  id: string;
  caseId: string;
  caseName: string;
  description: string;
  startDate: Date;
  endDate?: Date;
  status: 'active' | 'released';
  dataTypes: string[];
  affectedRecords: string[];
  createdBy: string;
  createdAt: Date;
}

export class LegalHoldService {
  private holds: Map<string, LegalHold> = new Map();
  
  createHold(
    caseId: string,
    caseName: string,
    description: string,
    dataTypes: string[],
    createdBy: string
  ): LegalHold {
    const hold: LegalHold = {
      id: this.generateId(),
      caseId,
      caseName,
      description,
      startDate: new Date(),
      status: 'active',
      dataTypes,
      affectedRecords: [],
      createdBy,
      createdAt: new Date()
    };
    
    this.holds.set(hold.id, hold);
    
    return hold;
  }
  
  releaseHold(holdId: string): LegalHold | undefined {
    const hold = this.holds.get(holdId);
    
    if (!hold) return undefined;
    
    hold.status = 'released';
    hold.endDate = new Date();
    
    return hold;
  }
  
  getHold(holdId: string): LegalHold | undefined {
    return this.holds.get(holdId);
  }
  
  getActiveHolds(): LegalHold[] {
    return Array.from(this.holds.values()).filter(h => h.status === 'active');
  }
  
  getHoldsByCase(caseId: string): LegalHold[] {
    return Array.from(this.holds.values()).filter(h => h.caseId === caseId);
  }
  
  isDataOnHold(dataType: string, recordId: string): boolean {
    for (const hold of this.getActiveHolds()) {
      if (hold.dataTypes.includes(dataType) && hold.affectedRecords.includes(recordId)) {
        return true;
      }
    }
    
    return false;
  }
  
  addRecordToHold(holdId: string, recordId: string): void {
    const hold = this.holds.get(holdId);
    
    if (hold) {
      hold.affectedRecords.push(recordId);
    }
  }
  
  private generateId(): string {
    return `hold_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

### Legal Hold Integration

```typescript
// legal-hold-integration.ts
import { LegalHoldService } from './legal-hold';
import { AutomatedDeletionService } from './automated-deletion';

export class LegalHoldIntegration {
  constructor(
    private holdService: LegalHoldService,
    private deletionService: AutomatedDeletionService
  ) {}
  
  async deleteExpiredDataExcludingHolds(): Promise<Map<string, number>> {
    const activeHolds = this.holdService.getActiveHolds();
    const results = new Map<string, number>();
    
    for (const hold of activeHolds) {
      for (const dataType of hold.dataTypes) {
        // Skip deletion for data types on hold
        console.log(`Skipping deletion of ${dataType} due to legal hold ${hold.id}`);
        results.set(dataType, 0);
      }
    }
    
    // Delete data not on hold
    // Implementation depends on data types
    
    return results;
  }
  
  async checkBeforeDeletion(dataType: string, recordId: string): Promise<boolean> {
    const isOnHold = this.holdService.isDataOnHold(dataType, recordId);
    
    if (isOnHold) {
      console.log(`Cannot delete ${dataType} record ${recordId} - on legal hold`);
      return false;
    }
    
    return true;
  }
}
```

---

## Compliance Requirements

### Compliance Checker

```typescript
// retention-compliance.ts

export interface ComplianceRequirement {
  framework: string;
  dataType: string;
  minRetentionPeriod: number; // days
  maxRetentionPeriod?: number; // days
  legalReference: string;
}

export class RetentionComplianceChecker {
  private static readonly REQUIREMENTS: ComplianceRequirement[] = [
    {
      framework: 'GDPR',
      dataType: 'user_consent',
      minRetentionPeriod: 3650, // 10 years
      maxRetentionPeriod: undefined,
      legalReference: 'GDPR Article 30'
    },
    {
      framework: 'GDPR',
      dataType: 'audit_logs',
      minRetentionPeriod: 3650, // 10 years
      maxRetentionPeriod: undefined,
      legalReference: 'GDPR Article 30'
    },
    {
      framework: 'SOX',
      dataType: 'transaction_records',
      minRetentionPeriod: 2555, // 7 years
      maxRetentionPeriod: undefined,
      legalReference: 'SOX Section 404'
    },
    {
      framework: 'HIPAA',
      dataType: 'audit_logs',
      minRetentionPeriod: 2190, // 6 years
      maxRetentionPeriod: undefined,
      legalReference: 'HIPAA Security Rule'
    },
    {
      framework: 'PCI DSS',
      dataType: 'payment_data',
      minRetentionPeriod: 365, // 1 year
      maxRetentionPeriod: 365, // 1 year
      legalReference: 'PCI DSS Requirement 3'
    }
  ];
  
  static checkCompliance(
    dataType: string,
    retentionPeriod: number
  ): { compliant: boolean; issues: string[] } {
    const requirements = this.REQUIREMENTS.filter(r => r.dataType === dataType);
    const issues: string[] = [];
    let compliant = true;
    
    for (const requirement of requirements) {
      if (retentionPeriod < requirement.minRetentionPeriod) {
        issues.push(
          `Retention period ${retentionPeriod} days is less than minimum ${requirement.minRetentionPeriod} days for ${requirement.framework}`
        );
        compliant = false;
      }
      
      if (requirement.maxRetentionPeriod && retentionPeriod > requirement.maxRetentionPeriod) {
        issues.push(
          `Retention period ${retentionPeriod} days exceeds maximum ${requirement.maxRetentionPeriod} days for ${requirement.framework}`
        );
        compliant = false;
      }
    }
    
    return { compliant, issues };
  }
  
  static getAllRequirements(): ComplianceRequirement[] {
    return this.REQUIREMENTS;
  }
  
  static getRequirementsByFramework(framework: string): ComplianceRequirement[] {
    return this.REQUIREMENTS.filter(r => r.framework === framework);
  }
}
```

---

## Implementation Patterns

### Retention Manager

```typescript
// retention-manager.ts
import { DataType, DataTypeRetentionManager } from './data-type-retention';
import { AutomatedDeletionService } from './automated-deletion';
import { ArchivalService } from './archival-service';
import { LegalHoldService } from './legal-hold';
import { RetentionComplianceChecker } from './retention-compliance';

export class RetentionManager {
  private deletionService: AutomatedDeletionService;
  private archivalService: ArchivalService;
  private holdService: LegalHoldService;
  
  constructor(
    pool: any
  ) {
    this.deletionService = new AutomatedDeletionService(pool);
    this.archivalService = new ArchivalService(pool);
    this.holdService = new LegalHoldService();
  }
  
  async processRetention(): Promise<void> {
    console.log('Starting retention processing');
    
    // Archive old data
    const archiveResults = await this.archivalService.archiveAllData();
    console.log('Archived data:', archiveResults);
    
    // Delete expired data (excluding legal holds)
    const deleteResults = await this.deletionService.deleteAllExpiredData();
    console.log('Deleted data:', deleteResults);
    
    console.log('Retention processing completed');
  }
  
  async checkCompliance(dataType: DataType, retentionPeriod: number): Promise<any> {
    return RetentionComplianceChecker.checkCompliance(dataType, retentionPeriod);
  }
  
  async getRetentionReport(): Promise<any> {
    const report: any = {
      timestamp: new Date().toISOString(),
      policies: DataTypeRetentionManager.getAllRetentionPeriods(),
      compliance: {},
      legalHolds: this.holdService.getActiveHolds()
    };
    
    for (const dataType of Object.values(DataType)) {
      const retention = DataTypeRetentionManager.getRetentionPeriod(dataType);
      const compliance = await this.checkCompliance(dataType, retention.retentionPeriod);
      
      report.compliance[dataType] = compliance;
    }
    
    return report;
  }
}
```

---

## Testing Retention Policies

### Test Suite

```typescript
// retention-testing.ts

export class RetentionPolicyTestSuite {
  static testRetentionPeriod(dataType: string, expectedDays: number): {
    passed: boolean;
    message: string;
  } {
    const { DataTypeRetentionManager } = require('./data-type-retention');
    const retention = DataTypeRetentionManager.getRetentionPeriod(dataType);
    
    const passed = retention.retentionPeriod === expectedDays;
    
    return {
      passed,
      message: passed
        ? `Retention period for ${dataType} is correct: ${expectedDays} days`
        : `Retention period for ${dataType} is incorrect: expected ${expectedDays}, got ${retention.retentionPeriod}`
    };
  }
  
  static testArchivalConfiguration(dataType: string, expectedArchival: boolean): {
    passed: boolean;
    message: string;
  } {
    const { DataTypeRetentionManager } = require('./data-type-retention');
    const retention = DataTypeRetentionManager.getRetentionPeriod(dataType);
    
    const passed = retention.archival === expectedArchival;
    
    return {
      passed,
      message: passed
        ? `Archival configuration for ${dataType} is correct`
        : `Archival configuration for ${dataType} is incorrect`
    };
  }
  
  static testCompliance(dataType: string, retentionPeriod: number): {
    passed: boolean;
    issues: string[];
  } {
    const { RetentionComplianceChecker } = require('./retention-compliance');
    const result = RetentionComplianceChecker.checkCompliance(dataType, retentionPeriod);
    
    return {
      passed: result.compliant,
      issues: result.issues
    };
  }
  
  static testLegalHoldExemption(recordId: string, expectedExempt: boolean): {
    passed: boolean;
    message: string;
  } {
    const { LegalHoldService } = require('./legal-hold');
    const holdService = new LegalHoldService();
    
    const isOnHold = holdService.isDataOnHold('test_type', recordId);
    const passed = isOnHold === expectedExempt;
    
    return {
      passed,
      message: passed
        ? `Legal hold exemption for ${recordId} is correct`
        : `Legal hold exemption for ${recordId} is incorrect`
    };
  }
  
  static runAllTests(): any[] {
    const results = [];
    
    // Test retention periods
    results.push(this.testRetentionPeriod('user_profile', 2555));
    results.push(this.testRetentionPeriod('authentication_logs', 365));
    results.push(this.testRetentionPeriod('transaction_records', 2555));
    
    // Test archival configuration
    results.push(this.testArchivalConfiguration('user_profile', true));
    results.push(this.testArchivalConfiguration('user_consent', false));
    
    // Test compliance
    results.push(this.testCompliance('user_consent', 3650));
    results.push(this.testCompliance('user_consent', 100));
    
    return results;
  }
}
```

---

## Audit Trails

### Deletion Audit

```sql
-- deletion-audit-schema.sql

CREATE TABLE deletion_audit (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  data_type VARCHAR(100) NOT NULL,
  record_id VARCHAR(255) NOT NULL,
  deletion_type VARCHAR(20) NOT NULL CHECK (deletion_type IN ('soft', 'hard', 'archival')),
  deletion_reason TEXT,
  deleted_at TIMESTAMPTZ DEFAULT NOW(),
  deleted_by VARCHAR(255),
  legal_hold_id UUID REFERENCES legal_holds(id),
  metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_deletion_audit_data_type ON deletion_audit(data_type);
CREATE INDEX idx_deletion_audit_deleted_at ON deletion_audit(deleted_at DESC);
CREATE INDEX idx_deletion_audit_legal_hold_id ON deletion_audit(legal_hold_id);
```

```typescript
// deletion-audit.ts
import { Pool } from 'pg';

export class DeletionAuditService {
  constructor(private pool: Pool) {}
  
  async logDeletion(
    dataType: string,
    recordId: string,
    deletionType: 'soft' | 'hard' | 'archival',
    deletedBy: string,
    reason?: string,
    legalHoldId?: string,
    metadata?: Record<string, any>
  ): Promise<void> {
    await this.pool.query(
      `INSERT INTO deletion_audit (data_type, record_id, deletion_type, deletion_reason, deleted_by, legal_hold_id, metadata)
       VALUES ($1, $2, $3, $4, $5, $6, $7)`,
      [dataType, recordId, deletionType, reason, deletedBy, legalHoldId, metadata ? JSON.stringify(metadata) : null]
    );
  }
  
  async getDeletionHistory(
    dataType: string,
    recordId: string
  ): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM deletion_audit 
       WHERE data_type = $1 AND record_id = $2 
       ORDER BY deleted_at DESC`,
      [dataType, recordId]
    );
    
    return result.rows;
  }
  
  async getDeletionsByDateRange(
    startDate: Date,
    endDate: Date
  ): Promise<any[]> {
    const result = await this.pool.query(
      `SELECT * FROM deletion_audit 
       WHERE deleted_at >= $1 AND deleted_at <= $2 
       ORDER BY deleted_at DESC`,
      [startDate, endDate]
    );
    
    return result.rows;
  }
  
  async getDeletionStats(): Promise<any> {
    const result = await this.pool.query(
      `SELECT 
         data_type,
         deletion_type,
         COUNT(*) as count,
         MIN(deleted_at) as first_deleted,
         MAX(deleted_at) as last_deleted
       FROM deletion_audit
       GROUP BY data_type, deletion_type
       ORDER BY data_type, deletion_type`
    );
    
    return result.rows;
  }
}
```

---

## Additional Resources

- [GDPR Data Retention](https://gdpr.eu/data-retention/)
- [Data Retention Best Practices](https://www.dataguidance.com/data-retention-best-practices/)
- [ISO 27001 Retention](https://www.iso.org/standard/27001)
- [NIST Data Retention](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5)
