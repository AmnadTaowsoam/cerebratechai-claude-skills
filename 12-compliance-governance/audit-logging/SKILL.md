# Audit Logging

## Overview

Comprehensive guide to audit logging patterns for compliance and security.

## Table of Contents

1. [Audit Log Requirements](#audit-log-requirements)
2. [What to Log](#what-to-log)
3. [Log Structure](#log-structure)
4. [Storage Strategies](#storage-strategies)
5. [Immutability](#immutability)
6. [Retention Policies](#retention-policies)
7. [Query and Reporting](#query-and-reporting)
8. [Performance Considerations](#performance-considerations)
9. [Compliance Requirements](#compliance-requirements)
10. [Implementation Patterns](#implementation-patterns)
11. [Best Practices](#best-practices)

---

## Audit Log Requirements

### Compliance Requirements

```typescript
// audit-requirements.ts

export enum ComplianceFramework {
  GDPR = 'gdpr',
  HIPAA = 'hipaa',
  PCI_DSS = 'pci_dss',
  SOX = 'sox',
  ISO_27001 = 'iso_27001'
}

export interface AuditRequirement {
  framework: ComplianceFramework;
  eventTypes: string[];
  retentionPeriod: number; // in days
  immutable: boolean;
  signed: boolean;
}

export class AuditRequirements {
  private static readonly REQUIREMENTS: Map<ComplianceFramework, AuditRequirement> = new Map([
    [ComplianceFramework.GDPR, {
      framework: ComplianceFramework.GDPR,
      eventTypes: ['data_access', 'data_modification', 'data_export', 'consent_changes'],
      retentionPeriod: 3650, // 10 years
      immutable: true,
      signed: true
    }],
    [ComplianceFramework.HIPAA, {
      framework: ComplianceFramework.HIPAA,
      eventTypes: ['phi_access', 'phi_modification', 'auth_events', 'system_changes'],
      retentionPeriod: 2190, // 6 years
      immutable: true,
      signed: true
    }],
    [ComplianceFramework.PCI_DSS, {
      framework: ComplianceFramework.PCI_DSS,
      eventTypes: ['card_data_access', 'auth_events', 'system_changes', 'user_actions'],
      retentionPeriod: 365, // 1 year
      immutable: true,
      signed: true
    }],
    [ComplianceFramework.SOX, {
      framework: ComplianceFramework.SOX,
      eventTypes: ['financial_transactions', 'system_changes', 'user_actions', 'data_access'],
      retentionPeriod: 2555, // 7 years
      immutable: true,
      signed: true
    }],
    [ComplianceFramework.ISO_27001, {
      framework: ComplianceFramework.ISO_27001,
      eventTypes: ['all_events'],
      retentionPeriod: 1825, // 5 years
      immutable: true,
      signed: false
    }]
  ]);
  
  static getRequirements(framework: ComplianceFramework): AuditRequirement {
    return this.REQUIREMENTS.get(framework)!;
  }
  
  static getRetentionPeriod(framework: ComplianceFramework): number {
    return this.REQUIREMENTS.get(framework)!.retentionPeriod;
  }
  
  static isImmutableRequired(framework: ComplianceFramework): boolean {
    return this.REQUIREMENTS.get(framework)!.immutable;
  }
  
  static isSigningRequired(framework: ComplianceFramework): boolean {
    return this.REQUIREMENTS.get(framework)!.signed;
  }
}
```

---

## What to Log

### Event Types

```typescript
// audit-events.ts

export enum AuditEventType {
  // Authentication Events
  USER_LOGIN = 'user_login',
  USER_LOGOUT = 'user_logout',
  LOGIN_FAILED = 'login_failed',
  PASSWORD_CHANGE = 'password_change',
  PASSWORD_RESET = 'password_reset',
  MFA_ENABLED = 'mfa_enabled',
  MFA_DISABLED = 'mfa_disabled',
  
  // Data Access Events
  DATA_READ = 'data_read',
  DATA_EXPORT = 'data_export',
  DATA_SEARCH = 'data_search',
  REPORT_GENERATED = 'report_generated',
  
  // Data Modification Events
  DATA_CREATED = 'data_created',
  DATA_UPDATED = 'data_updated',
  DATA_DELETED = 'data_deleted',
  BULK_IMPORT = 'bulk_import',
  BULK_EXPORT = 'bulk_export',
  
  // Permission Events
  PERMISSION_GRANTED = 'permission_granted',
  PERMISSION_REVOKED = 'permission_revoked',
  ROLE_ASSIGNED = 'role_assigned',
  ROLE_REMOVED = 'role_removed',
  
  // Configuration Events
  CONFIG_CHANGED = 'config_changed',
  SYSTEM_SETTING_CHANGED = 'system_setting_changed',
  API_KEY_CREATED = 'api_key_created',
  API_KEY_DELETED = 'api_key_deleted',
  
  // Security Events
  SUSPICIOUS_ACTIVITY = 'suspicious_activity',
  RATE_LIMIT_EXCEEDED = 'rate_limit_exceeded',
  UNAUTHORIZED_ACCESS_ATTEMPT = 'unauthorized_access_attempt',
  DATA_BREACH = 'data_breach',
  
  // Compliance Events
  CONSENT_GRANTED = 'consent_granted',
  CONSENT_REVOKED = 'consent_revoked',
  DATA_RETENTION_POLICY_APPLIED = 'data_retention_policy_applied',
  RIGHT_TO_ACCESS_REQUEST = 'right_to_access_request',
  RIGHT_TO_ERASURE_REQUEST = 'right_to_erasure_request'
}

export interface AuditEvent {
  id: string;
  eventType: AuditEventType;
  userId?: string;
  sessionId?: string;
  ipAddress?: string;
  userAgent?: string;
  resource?: string;
  resourceId?: string;
  action?: string;
  details?: Record<string, any>;
  timestamp: Date;
  severity: 'low' | 'medium' | 'high' | 'critical';
  success: boolean;
  errorMessage?: string;
}

export class AuditEventLogger {
  private events: AuditEvent[] = [];
  
  logEvent(event: Omit<AuditEvent, 'id' | 'timestamp'>): AuditEvent {
    const auditEvent: AuditEvent = {
      id: this.generateId(),
      ...event,
      timestamp: new Date()
    };
    
    this.events.push(auditEvent);
    
    return auditEvent;
  }
  
  logUserLogin(userId: string, sessionId: string, ipAddress: string, userAgent: string): AuditEvent {
    return this.logEvent({
      eventType: AuditEventType.USER_LOGIN,
      userId,
      sessionId,
      ipAddress,
      userAgent,
      severity: 'low',
      success: true
    });
  }
  
  logDataAccess(
    userId: string,
    resource: string,
    resourceId: string,
    action: string
  ): AuditEvent {
    return this.logEvent({
      eventType: AuditEventType.DATA_READ,
      userId,
      resource,
      resourceId,
      action,
      severity: 'low',
      success: true
    });
  }
  
  logDataModification(
    userId: string,
    resource: string,
    resourceId: string,
    action: string,
    changes?: Record<string, any>
  ): AuditEvent {
    return this.logEvent({
      eventType: AuditEventType.DATA_UPDATED,
      userId,
      resource,
      resourceId,
      action,
      details: { changes },
      severity: 'medium',
      success: true
    });
  }
  
  logPermissionChange(
    userId: string,
    targetUserId: string,
    permission: string,
    granted: boolean
  ): AuditEvent {
    return this.logEvent({
      eventType: granted ? AuditEventType.PERMISSION_GRANTED : AuditEventType.PERMISSION_REVOKED,
      userId,
      resource: 'user',
      resourceId: targetUserId,
      action: granted ? 'grant' : 'revoke',
      details: { permission },
      severity: 'medium',
      success: true
    });
  }
  
  logSecurityEvent(
    eventType: AuditEventType,
    userId?: string,
    ipAddress?: string,
    details?: Record<string, any>
  ): AuditEvent {
    return this.logEvent({
      eventType,
      userId,
      ipAddress,
      details,
      severity: 'high',
      success: false
    });
  }
  
  logComplianceEvent(
    eventType: AuditEventType,
    userId: string,
    details?: Record<string, any>
  ): AuditEvent {
    return this.logEvent({
      eventType,
      userId,
      details,
      severity: 'medium',
      success: true
    });
  }
  
  private generateId(): string {
    return `audit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

---

## Log Structure

### Standard Log Format

```typescript
// log-structure.ts

export interface StandardAuditLog {
  // Required fields
  timestamp: string; // ISO 8601
  event_id: string;
  event_type: string;
  actor: {
    id?: string;
    type: 'user' | 'system' | 'service';
    name?: string;
  };
  action: string;
  resource: {
    type: string;
    id?: string;
    name?: string;
  };
  outcome: {
    status: 'success' | 'failure';
    error_code?: string;
    error_message?: string;
  };
  
  // Optional fields
  session?: {
    id: string;
    start_time: string;
  };
  request?: {
    id: string;
    method: string;
    path: string;
    headers?: Record<string, string>;
  };
  changes?: {
    before?: Record<string, any>;
    after?: Record<string, any>;
  };
  metadata?: Record<string, any>;
  compliance?: {
    frameworks: string[];
    retention_days?: number;
  };
}

export class AuditLogFormatter {
  static formatEvent(event: any): StandardAuditLog {
    return {
      timestamp: event.timestamp.toISOString(),
      event_id: event.id,
      event_type: event.eventType,
      actor: {
        id: event.userId,
        type: event.userId ? 'user' : 'system',
        name: event.userName
      },
      action: event.action || 'unknown',
      resource: {
        type: event.resource || 'unknown',
        id: event.resourceId,
        name: event.resourceName
      },
      outcome: {
        status: event.success ? 'success' : 'failure',
        error_code: event.errorCode,
        error_message: event.errorMessage
      },
      session: event.sessionId ? {
        id: event.sessionId,
        start_time: event.sessionStartTime?.toISOString()
      } : undefined,
      request: event.requestId ? {
        id: event.requestId,
        method: event.requestMethod,
        path: event.requestPath,
        headers: event.requestHeaders
      } : undefined,
      changes: event.changes,
      metadata: event.metadata,
      compliance: event.compliance
    };
  }
  
  static toJSON(log: StandardAuditLog): string {
    return JSON.stringify(log, null, 2);
  }
  
  static toCSV(logs: StandardAuditLog[]): string {
    const headers = [
      'timestamp', 'event_id', 'event_type', 'actor_id', 'actor_type',
      'action', 'resource_type', 'resource_id', 'outcome_status',
      'session_id', 'request_id'
    ];
    
    const rows = logs.map(log => [
      log.timestamp,
      log.event_id,
      log.event_type,
      log.actor.id || '',
      log.actor.type,
      log.action,
      log.resource.type,
      log.resource.id || '',
      log.outcome.status,
      log.session?.id || '',
      log.request?.id || ''
    ].join(','));
    
    return [headers.join(','), ...rows].join('\n');
  }
}
```

---

## Storage Strategies

### Database Storage

```sql
-- audit-logs-schema.sql

-- Main audit logs table
CREATE TABLE audit_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id VARCHAR(255) UNIQUE NOT NULL,
  event_type VARCHAR(100) NOT NULL,
  actor_id UUID,
  actor_type VARCHAR(20) NOT NULL CHECK (actor_type IN ('user', 'system', 'service')),
  actor_name VARCHAR(255),
  action VARCHAR(255) NOT NULL,
  resource_type VARCHAR(100) NOT NULL,
  resource_id UUID,
  resource_name VARCHAR(255),
  outcome_status VARCHAR(20) NOT NULL CHECK (outcome_status IN ('success', 'failure')),
  error_code VARCHAR(50),
  error_message TEXT,
  session_id UUID,
  session_start_time TIMESTAMPTZ,
  request_id VARCHAR(255),
  request_method VARCHAR(10),
  request_path TEXT,
  request_headers JSONB,
  changes_before JSONB,
  changes_after JSONB,
  metadata JSONB,
  compliance_frameworks TEXT[],
  retention_days INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  INDEX idx_event_type (event_type),
  INDEX idx_actor_id (actor_id),
  INDEX idx_resource_type (resource_type),
  INDEX idx_resource_id (resource_id),
  INDEX idx_created_at (created_at DESC),
  INDEX idx_outcome_status (outcome_status)
);

-- Partitioned audit logs by month for better performance
CREATE TABLE audit_logs_partitioned (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_id VARCHAR(255) UNIQUE NOT NULL,
  event_type VARCHAR(100) NOT NULL,
  actor_id UUID,
  actor_type VARCHAR(20) NOT NULL,
  actor_name VARCHAR(255),
  action VARCHAR(255) NOT NULL,
  resource_type VARCHAR(100) NOT NULL,
  resource_id UUID,
  resource_name VARCHAR(255),
  outcome_status VARCHAR(20) NOT NULL,
  error_code VARCHAR(50),
  error_message TEXT,
  session_id UUID,
  session_start_time TIMESTAMPTZ,
  request_id VARCHAR(255),
  request_method VARCHAR(10),
  request_path TEXT,
  request_headers JSONB,
  changes_before JSONB,
  changes_after JSONB,
  metadata JSONB,
  compliance_frameworks TEXT[],
  retention_days INTEGER,
  created_at TIMESTAMPTZ DEFAULT NOW()
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE audit_logs_2024_01 PARTITION OF audit_logs_partitioned
  FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE audit_logs_2024_02 PARTITION OF audit_logs_partitioned
  FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- Create indexes on partitioned table
CREATE INDEX idx_audit_logs_event_type ON audit_logs_partitioned (event_type);
CREATE INDEX idx_audit_logs_actor_id ON audit_logs_partitioned (actor_id);
CREATE INDEX idx_audit_logs_resource_type ON audit_logs_partitioned (resource_type);
CREATE INDEX idx_audit_logs_created_at ON audit_logs_partitioned (created_at DESC);
```

### Log Aggregation (ELK)

```typescript
// elk-audit-logger.ts
import { Client } from '@elastic/elasticsearch';

export class ELKAuditLogger {
  private client: Client;
  private indexPrefix: string;
  
  constructor(
    node: string,
    indexPrefix: string = 'audit-logs'
  ) {
    this.client = new Client({ node });
    this.indexPrefix = indexPrefix;
  }
  
  async logEvent(event: any): Promise<void> {
    const indexName = this.getIndexName();
    
    await this.client.index({
      index: indexName,
      body: event
    });
  }
  
  async queryEvents(
    query: any,
    size: number = 100
  ): Promise<any[]> {
    const indexName = this.getIndexName();
    
    const result = await this.client.search({
      index: indexName,
      body: {
        query,
        size
      }
    });
    
    return result.hits.hits.map((hit: any) => hit._source);
  }
  
  async aggregateByEventType(
    startDate: Date,
    endDate: Date
  ): Promise<Record<string, number>> {
    const indexName = this.getIndexName();
    
    const result = await this.client.search({
      index: indexName,
      body: {
        query: {
          range: {
            timestamp: {
              gte: startDate.toISOString(),
              lte: endDate.toISOString()
            }
          }
        },
        aggs: {
          event_types: {
            terms: {
              field: 'event_type'
            }
          }
        }
      }
    });
    
    const aggregations: Record<string, number> = {};
    for (const bucket of result.aggregations.event_types.buckets) {
      aggregations[bucket.key] = bucket.doc_count;
    }
    
    return aggregations;
  }
  
  private getIndexName(): string {
    const now = new Date();
    const year = now.getFullYear();
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    return `${this.indexPrefix}-${year}-${month}`;
  }
}
```

---

## Immutability

### Immutable Storage

```typescript
// immutable-audit.ts
import crypto from 'crypto';

export interface ImmutableAuditLog {
  id: string;
  logData: string;
  hash: string;
  previousHash: string;
  timestamp: number;
  nonce: number;
}

export class ImmutableAuditLogger {
  private logs: ImmutableAuditLog[] = [];
  private difficulty: number = 4; // Number of leading zeros
  
  addLog(logData: string): ImmutableAuditLog {
    const previousHash = this.logs.length > 0
      ? this.logs[this.logs.length - 1].hash
      : '0'.repeat(64);
    
    const log = this.mineLog(logData, previousHash);
    this.logs.push(log);
    
    return log;
  }
  
  private mineLog(logData: string, previousHash: string): ImmutableAuditLog {
    let nonce = 0;
    let hash: string;
    
    do {
      const data = `${previousHash}${logData}${Date.now()}${nonce}`;
      hash = crypto.createHash('sha256').update(data).digest('hex');
      nonce++;
    } while (!this.isValidHash(hash));
    
    return {
      id: this.generateId(),
      logData,
      hash,
      previousHash,
      timestamp: Date.now(),
      nonce: nonce - 1
    };
  }
  
  private isValidHash(hash: string): boolean {
    return hash.substring(0, this.difficulty) === '0'.repeat(this.difficulty);
  }
  
  verifyIntegrity(): boolean {
    for (let i = 0; i < this.logs.length; i++) {
      const log = this.logs[i];
      
      // Verify hash
      const data = `${log.previousHash}${log.logData}${log.timestamp}${log.nonce}`;
      const computedHash = crypto.createHash('sha256').update(data).digest('hex');
      
      if (computedHash !== log.hash) {
        return false;
      }
      
      // Verify chain
      if (i > 0 && log.previousHash !== this.logs[i - 1].hash) {
        return false;
      }
    }
    
    return true;
  }
  
  getLogs(): ImmutableAuditLog[] {
    return [...this.logs];
  }
  
  private generateId(): string {
    return `audit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

---

## Retention Policies

### Retention Manager

```typescript
// retention-manager.ts
import { Pool } from 'pg';

export interface RetentionPolicy {
  eventType: string;
  retentionDays: number;
  framework?: string;
}

export class AuditLogRetentionManager {
  constructor(private pool: Pool) {}
  
  async setRetentionPolicy(policy: RetentionPolicy): Promise<void> {
    await this.pool.query(
      `INSERT INTO audit_retention_policies (event_type, retention_days, framework)
       VALUES ($1, $2, $3)
       ON CONFLICT (event_type) DO UPDATE
       SET retention_days = EXCLUDED.retention_days,
           framework = EXCLUDED.framework`,
      [policy.eventType, policy.retentionDays, policy.framework]
    );
  }
  
  async getRetentionPolicy(eventType: string): Promise<RetentionPolicy | null> {
    const result = await this.pool.query(
      'SELECT * FROM audit_retention_policies WHERE event_type = $1',
      [eventType]
    );
    
    if (result.rows.length === 0) return null;
    
    return {
      eventType: result.rows[0].event_type,
      retentionDays: result.rows[0].retention_days,
      framework: result.rows[0].framework
    };
  }
  
  async applyRetentionPolicies(): Promise<number> {
    const policies = await this.getAllPolicies();
    let deletedCount = 0;
    
    for (const policy of policies) {
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - policy.retentionDays);
      
      const result = await this.pool.query(
        `DELETE FROM audit_logs
         WHERE event_type = $1 AND created_at < $2`,
        [policy.eventType, cutoffDate]
      );
      
      deletedCount += result.rowCount || 0;
    }
    
    return deletedCount;
  }
  
  async getAllPolicies(): Promise<RetentionPolicy[]> {
    const result = await this.pool.query(
      'SELECT * FROM audit_retention_policies'
    );
    
    return result.rows.map(row => ({
      eventType: row.event_type,
      retentionDays: row.retention_days,
      framework: row.framework
    }));
  }
}

-- SQL table
/*
CREATE TABLE audit_retention_policies (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type VARCHAR(100) UNIQUE NOT NULL,
  retention_days INTEGER NOT NULL,
  framework VARCHAR(50),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
*/
```

---

## Query and Reporting

### Query Builder

```typescript
// audit-query-builder.ts
import { Pool } from 'pg';
import { AuditEventType } from './audit-events';

export interface AuditQuery {
  eventTypes?: AuditEventType[];
  userId?: string;
  resourceType?: string;
  resourceId?: string;
  startDate?: Date;
  endDate?: Date;
  outcomeStatus?: 'success' | 'failure';
  limit?: number;
  offset?: number;
}

export class AuditQueryService {
  constructor(private pool: Pool) {}
  
  async query(query: AuditQuery): Promise<any[]> {
    const { sql, params } = this.buildQuery(query);
    
    const result = await this.pool.query(sql, params);
    
    return result.rows;
  }
  
  async count(query: AuditQuery): Promise<number> {
    const countQuery: AuditQuery = { ...query };
    const { sql, params } = this.buildQuery(countQuery, true);
    
    const result = await this.pool.query(sql, params);
    
    return parseInt(result.rows[0].count, 10);
  }
  
  async getAuditTrail(
    userId: string,
    startDate: Date,
    endDate: Date
  ): Promise<any[]> {
    return this.query({
      userId,
      startDate,
      endDate,
      limit: 1000
    });
  }
  
  async getFailedLogins(
    startDate: Date,
    endDate: Date
  ): Promise<any[]> {
    return this.query({
      eventTypes: [AuditEventType.LOGIN_FAILED],
      startDate,
      endDate,
      limit: 100
    });
  }
  
  async getDataAccessEvents(
    resourceId: string,
    startDate: Date,
    endDate: Date
  ): Promise<any[]> {
    return this.query({
      resourceType: 'data',
      resourceId,
      startDate,
      endDate,
      limit: 100
    });
  }
  
  private buildQuery(query: AuditQuery, count: boolean = false): { sql: string; params: any[] } {
    const conditions: string[] = [];
    const params: any[] = [];
    let paramIndex = 1;
    
    if (query.eventTypes && query.eventTypes.length > 0) {
      conditions.push(`event_type = ANY($${paramIndex})`);
      params.push(query.eventTypes);
      paramIndex++;
    }
    
    if (query.userId) {
      conditions.push(`actor_id = $${paramIndex}`);
      params.push(query.userId);
      paramIndex++;
    }
    
    if (query.resourceType) {
      conditions.push(`resource_type = $${paramIndex}`);
      params.push(query.resourceType);
      paramIndex++;
    }
    
    if (query.resourceId) {
      conditions.push(`resource_id = $${paramIndex}`);
      params.push(query.resourceId);
      paramIndex++;
    }
    
    if (query.startDate) {
      conditions.push(`created_at >= $${paramIndex}`);
      params.push(query.startDate);
      paramIndex++;
    }
    
    if (query.endDate) {
      conditions.push(`created_at <= $${paramIndex}`);
      params.push(query.endDate);
      paramIndex++;
    }
    
    if (query.outcomeStatus) {
      conditions.push(`outcome_status = $${paramIndex}`);
      params.push(query.outcomeStatus);
      paramIndex++;
    }
    
    const whereClause = conditions.length > 0
      ? `WHERE ${conditions.join(' AND ')}`
      : '';
    
    const sql = count
      ? `SELECT COUNT(*) as count FROM audit_logs ${whereClause}`
      : `SELECT * FROM audit_logs ${whereClause}
         ORDER BY created_at DESC
         LIMIT $${paramIndex} OFFSET $${paramIndex + 1}`;
    
    if (!count) {
      params.push(query.limit || 100);
      params.push(query.offset || 0);
    }
    
    return { sql, params };
  }
}
```

---

## Performance Considerations

### Performance Optimization

```typescript
// audit-performance.ts
import { Pool } from 'pg';

export class AuditLogPerformanceOptimizer {
  constructor(private pool: Pool) {}
  
  async createIndexes(): Promise<void> {
    // Create composite indexes for common queries
    await this.pool.query(`
      CREATE INDEX IF NOT EXISTS idx_audit_logs_user_time
      ON audit_logs (actor_id, created_at DESC)
    `);
    
    await this.pool.query(`
      CREATE INDEX IF NOT EXISTS idx_audit_logs_resource_time
      ON audit_logs (resource_type, resource_id, created_at DESC)
    `);
    
    await this.pool.query(`
      CREATE INDEX IF NOT EXISTS idx_audit_logs_type_time
      ON audit_logs (event_type, created_at DESC)
    `);
    
    // Create partial index for failed events
    await this.pool.query(`
      CREATE INDEX IF NOT EXISTS idx_audit_logs_failed
      ON audit_logs (created_at DESC)
      WHERE outcome_status = 'failure'
    `);
  }
  
  async archiveOldLogs(days: number = 90): Promise<number> {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    // Move old logs to archive table
    const result = await this.pool.query(`
      INSERT INTO audit_logs_archive
      SELECT * FROM audit_logs
      WHERE created_at < $1
      ON CONFLICT (event_id) DO NOTHING
      RETURNING id
    `, [cutoffDate]);
    
    const archivedCount = result.rows.length;
    
    // Delete from main table
    await this.pool.query(`
      DELETE FROM audit_logs
      WHERE created_at < $1
    `, [cutoffDate]);
    
    return archivedCount;
  }
  
  async vacuumAnalyze(): Promise<void> {
    await this.pool.query('VACUUM ANALYZE audit_logs');
  }
  
  async getQueryStats(): Promise<any> {
    const result = await this.pool.query(`
      SELECT
        schemaname,
        tablename,
        seq_scan,
        seq_tup_read,
        idx_scan,
        idx_tup_fetch,
        n_tup_ins,
        n_tup_upd,
        n_tup_del
      FROM pg_stat_user_tables
      WHERE tablename = 'audit_logs'
    `);
    
    return result.rows[0];
  }
}

-- Archive table
/*
CREATE TABLE audit_logs_archive (
  LIKE audit_logs INCLUDING ALL
);

CREATE INDEX idx_audit_logs_archive_created_at
  ON audit_logs_archive (created_at DESC);
*/
```

---

## Compliance Requirements

### Compliance Checker

```typescript
// compliance-checker.ts
import { ComplianceFramework } from './audit-requirements';

export interface ComplianceCheck {
  framework: ComplianceFramework;
  passed: boolean;
  requirements: string[];
  findings: string[];
}

export class AuditComplianceChecker {
  async checkGDPRCompliance(): Promise<ComplianceCheck> {
    const requirements = [
      'All data access events logged',
      'Data modification events logged',
      'Consent changes logged',
      'Logs retained for 10 years',
      'Logs are immutable',
      'Logs are signed'
    ];
    
    const findings: string[] = [];
    let passed = true;
    
    // Check if required event types are being logged
    const requiredEvents = ['data_access', 'data_modification', 'consent_changes'];
    const loggedEvents = await this.getLoggedEventTypes();
    
    for (const event of requiredEvents) {
      if (!loggedEvents.includes(event)) {
        findings.push(`Event type ${event} not being logged`);
        passed = false;
      }
    }
    
    // Check retention period
    const retentionPeriod = await this.getRetentionPeriod();
    if (retentionPeriod < 3650) {
      findings.push(`Retention period ${retentionPeriod} days is less than required 3650 days`);
      passed = false;
    }
    
    // Check immutability
    const isImmutable = await this.checkImmutability();
    if (!isImmutable) {
      findings.push('Audit logs are not immutable');
      passed = false;
    }
    
    return {
      framework: ComplianceFramework.GDPR,
      passed,
      requirements,
      findings
    };
  }
  
  async checkHIPAACompliance(): Promise<ComplianceCheck> {
    const requirements = [
      'PHI access events logged',
      'PHI modification events logged',
      'Authentication events logged',
      'System changes logged',
      'Logs retained for 6 years',
      'Logs are immutable'
    ];
    
    const findings: string[] = [];
    let passed = true;
    
    // Check PHI event logging
    const phiEvents = await this.getPHIEventTypes();
    if (phiEvents.length === 0) {
      findings.push('No PHI events being logged');
      passed = false;
    }
    
    // Check retention period
    const retentionPeriod = await this.getRetentionPeriod();
    if (retentionPeriod < 2190) {
      findings.push(`Retention period ${retentionPeriod} days is less than required 2190 days`);
      passed = false;
    }
    
    return {
      framework: ComplianceFramework.HIPAA,
      passed,
      requirements,
      findings
    };
  }
  
  async checkPCIDSSCompliance(): Promise<ComplianceCheck> {
    const requirements = [
      'Card data access events logged',
      'Authentication events logged',
      'System changes logged',
      'User actions logged',
      'Logs retained for 1 year',
      'Logs are immutable'
    ];
    
    const findings: string[] = [];
    let passed = true;
    
    // Check card data logging
    const cardEvents = await this.getCardDataEventTypes();
    if (cardEvents.length === 0) {
      findings.push('No card data events being logged');
      passed = false;
    }
    
    // Check retention period
    const retentionPeriod = await this.getRetentionPeriod();
    if (retentionPeriod < 365) {
      findings.push(`Retention period ${retentionPeriod} days is less than required 365 days`);
      passed = false;
    }
    
    return {
      framework: ComplianceFramework.PCI_DSS,
      passed,
      requirements,
      findings
    };
  }
  
  private async getLoggedEventTypes(): Promise<string[]> {
    // Implementation to get logged event types
    return [];
  }
  
  private async getPHIEventTypes(): Promise<string[]> {
    // Implementation to get PHI event types
    return [];
  }
  
  private async getCardDataEventTypes(): Promise<string[]> {
    // Implementation to get card data event types
    return [];
  }
  
  private async getRetentionPeriod(): Promise<number> {
    // Implementation to get retention period
    return 365;
  }
  
  private async checkImmutability(): Promise<boolean> {
    // Implementation to check immutability
    return true;
  }
}
```

---

## Implementation Patterns

### Middleware Integration

```typescript
// audit-middleware.ts
import { Request, Response, NextFunction } from 'express';
import { AuditEventLogger, AuditEventType } from './audit-events';

export class AuditMiddleware {
  private logger: AuditEventLogger;
  
  constructor() {
    this.logger = new AuditEventLogger();
  }
  
  middleware = (eventType: AuditEventType) => {
    return (req: Request, res: Response, next: NextFunction) => {
      const startTime = Date.now();
      
      // Capture original methods
      const originalJson = res.json;
      
      // Override res.json to capture response
      res.json = function(this: Response, body: any) {
        const duration = Date.now() - startTime;
        
        // Log audit event
        this.logger.logEvent({
          eventType,
          userId: req.user?.id,
          sessionId: req.sessionID,
          ipAddress: req.ip,
          userAgent: req.get('user-agent'),
          resource: req.baseUrl + req.path,
          action: req.method,
          details: {
            statusCode: res.statusCode,
            duration
          },
          severity: res.statusCode >= 400 ? 'medium' : 'low',
          success: res.statusCode < 400
        });
        
        return originalJson.call(this, body);
      };
      
      next();
    };
  };
  
  auditMiddleware = (req: Request, res: Response, next: NextFunction) => {
    const startTime = Date.now();
    
    res.on('finish', () => {
      const duration = Date.now() - startTime;
      
      this.logger.logEvent({
        eventType: this.getEventType(req.method, res.statusCode),
        userId: req.user?.id,
        sessionId: req.sessionID,
        ipAddress: req.ip,
        userAgent: req.get('user-agent'),
        resource: req.baseUrl + req.path,
        action: req.method,
        details: {
          statusCode: res.statusCode,
          duration
        },
        severity: res.statusCode >= 400 ? 'medium' : 'low',
        success: res.statusCode < 400
      });
    });
    
    next();
  };
  
  private getEventType(method: string, statusCode: number): AuditEventType {
    if (statusCode >= 400) {
      return AuditEventType.UNAUTHORIZED_ACCESS_ATTEMPT;
    }
    
    switch (method.toLowerCase()) {
      case 'get':
        return AuditEventType.DATA_READ;
      case 'post':
        return AuditEventType.DATA_CREATED;
      case 'put':
      case 'patch':
        return AuditEventType.DATA_UPDATED;
      case 'delete':
        return AuditEventType.DATA_DELETED;
      default:
        return AuditEventType.DATA_READ;
    }
  }
}
```

---

## Best Practices

```markdown
## Audit Logging Best Practices

### What to Log
- [ ] Log all authentication events (login, logout, failed attempts)
- [ ] Log all authorization events (permission changes, role changes)
- [ ] Log all data access events (read, export, search)
- [ ] Log all data modification events (create, update, delete)
- [ ] Log all configuration changes
- [ ] Log all security events (suspicious activity, breaches)
- [ ] Log all compliance events (consent, data subject requests)

### Log Structure
- [ ] Use standardized log format (JSON recommended)
- [ ] Include timestamp (ISO 8601 format)
- [ ] Include unique event ID
- [ ] Include actor information (who performed the action)
- [ ] Include resource information (what was acted upon)
- [ ] Include action type (what was done)
- [ ] Include outcome (success/failure)
- [ ] Include relevant metadata

### Storage
- [ ] Use appropriate storage for compliance requirements
- [ ] Implement partitioning for large datasets
- [ ] Create appropriate indexes for query performance
- [ ] Archive old logs to separate storage
- [ ] Implement retention policies
- [ ] Ensure immutability for compliance

### Performance
- [ ] Use async logging to avoid performance impact
- [ ] Batch log writes when possible
- [ ] Monitor query performance
- [ ] Optimize indexes based on query patterns
- [ ] Use connection pooling
- [ ] Implement caching for frequent queries

### Security
- [ ] Encrypt logs at rest
- [ ] Encrypt logs in transit
- [ ] Implement access controls for log viewing
- [ ] Log all access to audit logs
- [ ] Implement tamper detection
- [ ] Use digital signatures for critical logs

### Compliance
- [ ] Understand compliance requirements for your industry
- [ ] Implement required retention periods
- [ ] Ensure logs are immutable where required
- [ ] Implement log signing where required
- [ ] Regularly test compliance
- [ ] Document audit logging procedures

### Monitoring
- [ ] Monitor log volume and growth
- [ ] Monitor query performance
- [ ] Set up alerts for suspicious activity
- [ ] Monitor storage capacity
- [ ] Track compliance metrics
- [ ] Regular audit of audit logs
```

---

## Additional Resources

- [NIST Audit Logging](https://csrc.nist.gov/publications/detail/sp/800-92/final)
- [PCI DSS Requirements](https://www.pcisecuritystandards.org/)
- [HIPAA Security Rule](https://www.hhs.gov/hipaa/for-professionals/security/laws-regulations/)
- [GDPR Article 30](https://gdpr.eu/article-30-records-of-processing-activities/)
