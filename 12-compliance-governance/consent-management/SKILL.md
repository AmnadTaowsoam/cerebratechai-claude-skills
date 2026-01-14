# Consent Management

## Overview

Comprehensive guide to user consent management implementation.

## Table of Contents

1. [Consent Types](#consent-types)
2. [Granular Consent](#granular-consent)
3. [Consent UI Patterns](#consent-ui-patterns)
4. [Consent Storage](#consent-storage)
5. [Consent Versioning](#consent-versioning)
6. [Withdrawal Mechanism](#withdrawal-mechanism)
7. [Consent Logs](#consent-logs)
8. [Cookie Consent](#cookie-consent)
9. [Third-Party Consent](#third-party-consent)
10. [Compliance Verification](#compliance-verification)
11. [Best Practices](#best-practices)

---

## Consent Types

### Consent Categories

```typescript
// consent-types.ts

export enum ConsentType {
  // Essential Consent
  ESSENTIAL = 'essential', // Required for core functionality
  
  // Functional Consent
  FUNCTIONAL = 'functional', // Enables additional features
  
  // Analytics Consent
  ANALYTICS = 'analytics', // Enables analytics and tracking
  
  // Marketing Consent
  MARKETING = 'marketing', // Enables marketing communications
  
  // Advertising Consent
  ADVERTISING = 'advertising', // Enables personalized advertising
  
  // Social Media Consent
  SOCIAL_MEDIA = 'social_media', // Enables social media integration
  
  // Location Consent
  LOCATION = 'location', // Enables location tracking
  
  // Biometric Consent
  BIOMETRIC = 'biometric', // Enables biometric data collection
  
  // Health Data Consent
  HEALTH_DATA = 'health_data', // Enables health data collection
  
  // Financial Data Consent
  FINANCIAL_DATA = 'financial_data' // Enables financial data access
}

export interface ConsentDefinition {
  type: ConsentType;
  name: string;
  description: string;
  required: boolean;
  dataCollected: string[];
  dataUsedFor: string[];
  thirdPartySharing: boolean;
  retentionPeriod: string;
}

export class ConsentDefinitions {
  private static readonly DEFINITIONS: Map<ConsentType, ConsentDefinition> = new Map([
    [ConsentType.ESSENTIAL, {
      type: ConsentType.ESSENTIAL,
      name: 'Essential Cookies',
      description: 'Required for the website to function properly',
      required: true,
      dataCollected: ['session_id', 'csrf_token'],
      dataUsedFor: ['authentication', 'security'],
      thirdPartySharing: false,
      retentionPeriod: 'session'
    }],
    [ConsentType.FUNCTIONAL, {
      type: ConsentType.FUNCTIONAL,
      name: 'Functional Cookies',
      description: 'Enable enhanced functionality and personalization',
      required: false,
      dataCollected: ['preferences', 'language', 'theme'],
      dataUsedFor: ['personalization', 'user_experience'],
      thirdPartySharing: false,
      retentionPeriod: '1 year'
    }],
    [ConsentType.ANALYTICS, {
      type: ConsentType.ANALYTICS,
      name: 'Analytics Cookies',
      description: 'Help us understand how visitors use our website',
      required: false,
      dataCollected: ['page_views', 'click_events', 'session_duration'],
      dataUsedFor: ['analytics', 'improvement'],
      thirdPartySharing: false,
      retentionPeriod: '2 years'
    }],
    [ConsentType.MARKETING, {
      type: ConsentType.MARKETING,
      name: 'Marketing Communications',
      description: 'Receive marketing emails and newsletters',
      required: false,
      dataCollected: ['email', 'name', 'preferences'],
      dataUsedFor: ['marketing', 'promotions'],
      thirdPartySharing: false,
      retentionPeriod: 'until withdrawal'
    }],
    [ConsentType.ADVERTISING, {
      type: ConsentType.ADVERTISING,
      name: 'Advertising Cookies',
      description: 'Enable personalized advertising',
      required: false,
      dataCollected: ['browsing_history', 'interests', 'demographics'],
      dataUsedFor: ['personalized_ads', 'targeting'],
      thirdPartySharing: true,
      retentionPeriod: '2 years'
    }],
    [ConsentType.LOCATION, {
      type: ConsentType.LOCATION,
      name: 'Location Data',
      description: 'Allow access to your location',
      required: false,
      dataCollected: ['gps_coordinates', 'ip_location'],
      dataUsedFor: ['location_services', 'personalization'],
      thirdPartySharing: false,
      retentionPeriod: '6 months'
    }]
  ]);
  
  static getDefinition(type: ConsentType): ConsentDefinition {
    return this.DEFINITIONS.get(type)!;
  }
  
  static getAllDefinitions(): ConsentDefinition[] {
    return Array.from(this.DEFINITIONS.values());
  }
  
  static getRequiredConsents(): ConsentType[] {
    return Array.from(this.DEFINITIONS.values())
      .filter(d => d.required)
      .map(d => d.type);
  }
  
  static getOptionalConsents(): ConsentType[] {
    return Array.from(this.DEFINITIONS.values())
      .filter(d => !d.required)
      .map(d => d.type);
  }
}
```

---

## Granular Consent

### Granular Consent Manager

```typescript
// granular-consent.ts
import { ConsentType, ConsentDefinitions } from './consent-types';

export interface GranularConsent {
  userId: string;
  consents: Map<ConsentType, ConsentRecord>;
  version: string;
  timestamp: Date;
}

export interface ConsentRecord {
  granted: boolean;
  grantedAt: Date;
  withdrawnAt?: Date;
  ipAddress?: string;
  userAgent?: string;
}

export class GranularConsentManager {
  private consents: Map<string, GranularConsent> = new Map();
  
  grantConsent(
    userId: string,
    consentType: ConsentType,
    ipAddress?: string,
    userAgent?: string
  ): void {
    let userConsent = this.consents.get(userId);
    
    if (!userConsent) {
      userConsent = {
        userId,
        consents: new Map(),
        version: this.getCurrentVersion(),
        timestamp: new Date()
      };
      this.consents.set(userId, userConsent);
    }
    
    userConsent.consents.set(consentType, {
      granted: true,
      grantedAt: new Date(),
      ipAddress,
      userAgent
    });
    
    userConsent.timestamp = new Date();
  }
  
  revokeConsent(
    userId: string,
    consentType: ConsentType
  ): void {
    const userConsent = this.consents.get(userId);
    
    if (!userConsent) return;
    
    const consent = userConsent.consents.get(consentType);
    
    if (consent && consent.granted) {
      consent.granted = false;
      consent.withdrawnAt = new Date();
      userConsent.timestamp = new Date();
    }
  }
  
  hasConsent(userId: string, consentType: ConsentType): boolean {
    const userConsent = this.consents.get(userId);
    
    if (!userConsent) return false;
    
    const consent = userConsent.consents.get(consentType);
    
    return consent ? consent.granted && !consent.withdrawnAt : false;
  }
  
  getAllConsents(userId: string): Map<ConsentType, ConsentRecord> {
    const userConsent = this.consents.get(userId);
    return userConsent ? new Map(userConsent.consents) : new Map();
  }
  
  getRequiredConsents(userId: string): Map<ConsentType, ConsentRecord> {
    const requiredTypes = ConsentDefinitions.getRequiredConsents();
    const allConsents = this.getAllConsents(userId);
    
    const requiredConsents = new Map<ConsentType, ConsentRecord>();
    
    for (const type of requiredTypes) {
      const consent = allConsents.get(type);
      if (consent) {
        requiredConsents.set(type, consent);
      }
    }
    
    return requiredConsents;
  }
  
  getOptionalConsents(userId: string): Map<ConsentType, ConsentRecord> {
    const optionalTypes = ConsentDefinitions.getOptionalConsents();
    const allConsents = this.getAllConsents(userId);
    
    const optionalConsents = new Map<ConsentType, ConsentRecord>();
    
    for (const type of optionalTypes) {
      const consent = allConsents.get(type);
      if (consent) {
        optionalConsents.set(type, consent);
      }
    }
    
    return optionalConsents;
  }
  
  updateConsents(
    userId: string,
    newConsents: Map<ConsentType, boolean>,
    ipAddress?: string,
    userAgent?: string
  ): void {
    for (const [type, granted] of newConsents.entries()) {
      if (granted) {
        this.grantConsent(userId, type, ipAddress, userAgent);
      } else {
        this.revokeConsent(userId, type);
      }
    }
  }
  
  private getCurrentVersion(): string {
    return '1.0.0';
  }
}
```

---

## Consent UI Patterns

### React Components

```typescript
// consent-ui.tsx
import React, { useState, useEffect } from 'react';
import { ConsentType, ConsentDefinitions } from './consent-types';
import { GranularConsentManager } from './granular-consent';

interface ConsentBannerProps {
  onAccept: (consents: Map<ConsentType, boolean>) => void;
  onReject: () => void;
  onCustomize: () => void;
}

export const ConsentBanner: React.FC<ConsentBannerProps> = ({
  onAccept,
  onReject,
  onCustomize
}) => {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    // Check if user has already consented
    const hasConsented = localStorage.getItem('consent_given');
    if (!hasConsented) {
      setIsVisible(true);
    }
  }, []);
  
  const handleAcceptAll = () => {
    const allConsents = new Map<ConsentType, boolean>();
    
    for (const definition of ConsentDefinitions.getAllDefinitions()) {
      allConsents.set(definition.type, true);
    }
    
    onAccept(allConsents);
    setIsVisible(false);
    localStorage.setItem('consent_given', 'true');
  };
  
  const handleRejectAll = () => {
    onReject();
    setIsVisible(false);
    localStorage.setItem('consent_given', 'true');
  };
  
  if (!isVisible) return null;
  
  return (
    <div className="consent-banner">
      <div className="consent-content">
        <h3>We use cookies</h3>
        <p>
          We use cookies to enhance your experience. By continuing to visit this site
          you agree to our use of cookies.
        </p>
      </div>
      <div className="consent-actions">
        <button onClick={handleRejectAll} className="btn btn-secondary">
          Reject All
        </button>
        <button onClick={onCustomize} className="btn btn-secondary">
          Customize
        </button>
        <button onClick={handleAcceptAll} className="btn btn-primary">
          Accept All
        </button>
      </div>
    </div>
  );
};

interface ConsentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (consents: Map<ConsentType, boolean>) => void;
}

export const ConsentModal: React.FC<ConsentModalProps> = ({
  isOpen,
  onClose,
  onSave
}) => {
  const [consents, setConsents] = useState<Map<ConsentType, boolean>>(new Map());
  
  useEffect(() => {
    if (isOpen) {
      const newConsents = new Map<ConsentType, boolean>();
      
      for (const definition of ConsentDefinitions.getAllDefinitions()) {
        newConsents.set(definition.type, definition.required);
      }
      
      setConsents(newConsents);
    }
  }, [isOpen]);
  
  const handleToggle = (type: ConsentType) => {
    const definition = ConsentDefinitions.getDefinition(type);
    
    if (definition.required) return;
    
    const newConsents = new Map(consents);
    newConsents.set(type, !newConsents.get(type));
    setConsents(newConsents);
  };
  
  const handleSave = () => {
    onSave(consents);
    onClose();
  };
  
  if (!isOpen) return null;
  
  return (
    <div className="consent-modal-overlay">
      <div className="consent-modal">
        <div className="consent-modal-header">
          <h2>Cookie Preferences</h2>
          <button onClick={onClose} className="close-button">×</button>
        </div>
        
        <div className="consent-modal-body">
          {ConsentDefinitions.getAllDefinitions().map(definition => (
            <div key={definition.type} className="consent-item">
              <div className="consent-item-header">
                <input
                  type="checkbox"
                  id={definition.type}
                  checked={consents.get(definition.type) || false}
                  onChange={() => handleToggle(definition.type)}
                  disabled={definition.required}
                />
                <label htmlFor={definition.type}>
                  {definition.name}
                  {definition.required && <span className="required-badge">Required</span>}
                </label>
              </div>
              
              <p className="consent-description">{definition.description}</p>
              
              <details className="consent-details">
                <summary>More details</summary>
                <div className="consent-details-content">
                  <p><strong>Data Collected:</strong></p>
                  <ul>
                    {definition.dataCollected.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                  
                  <p><strong>Data Used For:</strong></p>
                  <ul>
                    {definition.dataUsedFor.map((item, index) => (
                      <li key={index}>{item}</li>
                    ))}
                  </ul>
                  
                  <p><strong>Third Party Sharing:</strong></p>
                  <p>{definition.thirdPartySharing ? 'Yes' : 'No'}</p>
                  
                  <p><strong>Retention Period:</strong></p>
                  <p>{definition.retentionPeriod}</p>
                </div>
              </details>
            </div>
          ))}
        </div>
        
        <div className="consent-modal-footer">
          <button onClick={onClose} className="btn btn-secondary">
            Cancel
          </button>
          <button onClick={handleSave} className="btn btn-primary">
            Save Preferences
          </button>
        </div>
      </div>
    </div>
  );
};
```

### CSS Styles

```css
/* consent-ui.css */

.consent-banner {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #1a1a1a;
  color: #ffffff;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 9999;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}

.consent-content h3 {
  margin: 0 0 10px 0;
  font-size: 18px;
}

.consent-content p {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
}

.consent-actions {
  display: flex;
  gap: 10px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s;
}

.btn-primary {
  background-color: #007bff;
  color: #ffffff;
}

.btn-primary:hover {
  background-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  color: #ffffff;
}

.btn-secondary:hover {
  background-color: #545b62;
}

.consent-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
}

.consent-modal {
  background-color: #ffffff;
  border-radius: 8px;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.consent-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e0e0e0;
}

.consent-modal-header h2 {
  margin: 0;
  font-size: 20px;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
}

.consent-modal-body {
  padding: 20px;
  overflow-y: auto;
}

.consent-item {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.consent-item-header {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.consent-item-header input[type="checkbox"] {
  margin-right: 10px;
}

.consent-item-header label {
  font-weight: 600;
  cursor: pointer;
}

.required-badge {
  margin-left: 10px;
  padding: 2px 8px;
  background-color: #dc3545;
  color: #ffffff;
  border-radius: 10px;
  font-size: 12px;
}

.consent-description {
  margin: 10px 0;
  color: #6c757d;
  font-size: 14px;
}

.consent-details {
  margin-top: 10px;
}

.consent-details summary {
  cursor: pointer;
  color: #007bff;
  font-weight: 500;
}

.consent-details-content {
  margin-top: 10px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.consent-details-content p {
  margin: 5px 0;
}

.consent-details-content ul {
  margin: 5px 0;
  padding-left: 20px;
}

.consent-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 20px;
  border-top: 1px solid #e0e0e0;
}
```

---

## Consent Storage

### Database Schema

```sql
-- consent-storage.sql

CREATE TABLE consents (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  consent_type VARCHAR(50) NOT NULL,
  granted BOOLEAN NOT NULL,
  granted_at TIMESTAMPTZ NOT NULL,
  withdrawn_at TIMESTAMPTZ,
  ip_address INET,
  user_agent TEXT,
  version VARCHAR(20) NOT NULL,
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, consent_type, version)
);

CREATE INDEX idx_consents_user_id ON consents(user_id);
CREATE INDEX idx_consents_consent_type ON consents(consent_type);
CREATE INDEX idx_consents_granted_at ON consents(granted_at DESC);
CREATE INDEX idx_consents_version ON consents(version);

CREATE TABLE consent_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  consent_id UUID REFERENCES consents(id) ON DELETE SET NULL,
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  consent_type VARCHAR(50) NOT NULL,
  action VARCHAR(20) NOT NULL CHECK (action IN ('granted', 'revoked', 'updated')),
  previous_value BOOLEAN,
  new_value BOOLEAN,
  ip_address INET,
  user_agent TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_consent_logs_user_id ON consent_logs(user_id);
CREATE INDEX idx_consent_logs_consent_type ON consent_logs(consent_type);
CREATE INDEX idx_consent_logs_created_at ON consent_logs(created_at DESC);

CREATE TABLE consent_templates (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL UNIQUE,
  consent_type VARCHAR(50) NOT NULL,
  description TEXT NOT NULL,
  required BOOLEAN DEFAULT false,
  data_collected JSONB NOT NULL,
  data_used_for JSONB NOT NULL,
  third_party_sharing BOOLEAN DEFAULT false,
  retention_period VARCHAR(100),
  version VARCHAR(20) NOT NULL,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_consent_templates_consent_type ON consent_templates(consent_type);
CREATE INDEX idx_consent_templates_version ON consent_templates(version);
```

### Storage Service

```typescript
// consent-storage.ts
import { Pool } from 'pg';
import { ConsentType } from './consent-types';

export interface ConsentRecord {
  id: string;
  userId: string;
  consentType: ConsentType;
  granted: boolean;
  grantedAt: Date;
  withdrawnAt?: Date;
  ipAddress?: string;
  userAgent?: string;
  version: string;
  metadata?: Record<string, any>;
}

export class ConsentStorageService {
  constructor(private pool: Pool) {}
  
  async grantConsent(
    userId: string,
    consentType: ConsentType,
    ipAddress?: string,
    userAgent?: string
  ): Promise<ConsentRecord> {
    const version = await this.getCurrentVersion();
    
    const result = await this.pool.query(
      `INSERT INTO consents (user_id, consent_type, granted, granted_at, ip_address, user_agent, version)
       VALUES ($1, $2, true, NOW(), $3, $4, $5)
       RETURNING *`,
      [userId, consentType, ipAddress, userAgent, version]
    );
    
    const consent = this.mapRowToConsent(result.rows[0]);
    
    // Log the action
    await this.logConsentAction(userId, consentType, 'granted', null, true, ipAddress, userAgent);
    
    return consent;
  }
  
  async revokeConsent(
    userId: string,
    consentType: ConsentType,
    ipAddress?: string,
    userAgent?: string
  ): Promise<ConsentRecord | null> {
    const result = await this.pool.query(
      `UPDATE consents 
       SET granted = false, withdrawn_at = NOW(), updated_at = NOW()
       WHERE user_id = $1 AND consent_type = $2 AND granted = true
       RETURNING *`,
      [userId, consentType]
    );
    
    if (result.rows.length === 0) return null;
    
    const consent = this.mapRowToConsent(result.rows[0]);
    
    // Log the action
    await this.logConsentAction(userId, consentType, 'revoked', true, false, ipAddress, userAgent);
    
    return consent;
  }
  
  async hasConsent(userId: string, consentType: ConsentType): Promise<boolean> {
    const result = await this.pool.query(
      `SELECT granted FROM consents 
       WHERE user_id = $1 AND consent_type = $2 
       ORDER BY created_at DESC 
       LIMIT 1`,
      [userId, consentType]
    );
    
    if (result.rows.length === 0) return false;
    
    return result.rows[0].granted;
  }
  
  async getAllConsents(userId: string): Promise<ConsentRecord[]> {
    const result = await this.pool.query(
      `SELECT DISTINCT ON (consent_type) * FROM consents 
       WHERE user_id = $1 
       ORDER BY consent_type, created_at DESC`,
      [userId]
    );
    
    return result.rows.map(row => this.mapRowToConsent(row));
  }
  
  async getConsentHistory(
    userId: string,
    consentType: ConsentType
  ): Promise<ConsentRecord[]> {
    const result = await this.pool.query(
      `SELECT * FROM consents 
       WHERE user_id = $1 AND consent_type = $2 
       ORDER BY created_at DESC`,
      [userId, consentType]
    );
    
    return result.rows.map(row => this.mapRowToConsent(row));
  }
  
  async getConsentLogs(
    userId: string,
    consentType?: ConsentType
  ): Promise<any[]> {
    let query = 'SELECT * FROM consent_logs WHERE user_id = $1';
    const params: any[] = [userId];
    
    if (consentType) {
      query += ' AND consent_type = $2';
      params.push(consentType);
    }
    
    query += ' ORDER BY created_at DESC';
    
    const result = await this.pool.query(query, params);
    
    return result.rows;
  }
  
  private async logConsentAction(
    userId: string,
    consentType: ConsentType,
    action: 'granted' | 'revoked' | 'updated',
    previousValue: boolean | null,
    newValue: boolean,
    ipAddress?: string,
    userAgent?: string
  ): Promise<void> {
    await this.pool.query(
      `INSERT INTO consent_logs (user_id, consent_type, action, previous_value, new_value, ip_address, user_agent)
       VALUES ($1, $2, $3, $4, $5, $6, $7)`,
      [userId, consentType, action, previousValue, newValue, ipAddress, userAgent]
    );
  }
  
  private async getCurrentVersion(): Promise<string> {
    const result = await this.pool.query(
      'SELECT version FROM consent_templates WHERE is_active = true ORDER BY version DESC LIMIT 1'
    );
    
    return result.rows[0]?.version || '1.0.0';
  }
  
  private mapRowToConsent(row: any): ConsentRecord {
    return {
      id: row.id,
      userId: row.user_id,
      consentType: row.consent_type,
      granted: row.granted,
      grantedAt: row.granted_at,
      withdrawnAt: row.withdrawn_at,
      ipAddress: row.ip_address,
      userAgent: row.user_agent,
      version: row.version,
      metadata: row.metadata
    };
  }
}
```

---

## Consent Versioning

### Version Manager

```typescript
// consent-versioning.ts
import { Pool } from 'pg';

export interface ConsentTemplate {
  id: string;
  name: string;
  consentType: string;
  description: string;
  required: boolean;
  dataCollected: string[];
  dataUsedFor: string[];
  thirdPartySharing: boolean;
  retentionPeriod: string;
  version: string;
  isActive: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export class ConsentVersionManager {
  constructor(private pool: Pool) {}
  
  async createTemplate(template: Omit<ConsentTemplate, 'id' | 'createdAt' | 'updatedAt'>): Promise<ConsentTemplate> {
    // Deactivate previous versions
    await this.pool.query(
      `UPDATE consent_templates 
       SET is_active = false 
       WHERE consent_type = $1`,
      [template.consentType]
    );
    
    const result = await this.pool.query(
      `INSERT INTO consent_templates (name, consent_type, description, required, data_collected, data_used_for, third_party_sharing, retention_period, version, is_active)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, true)
       RETURNING *`,
      [
        template.name,
        template.consentType,
        template.description,
        template.required,
        JSON.stringify(template.dataCollected),
        JSON.stringify(template.dataUsedFor),
        template.thirdPartySharing,
        template.retentionPeriod,
        template.version
      ]
    );
    
    return this.mapRowToTemplate(result.rows[0]);
  }
  
  async getActiveTemplate(consentType: string): Promise<ConsentTemplate | null> {
    const result = await this.pool.query(
      `SELECT * FROM consent_templates 
       WHERE consent_type = $1 AND is_active = true 
       LIMIT 1`,
      [consentType]
    );
    
    if (result.rows.length === 0) return null;
    
    return this.mapRowToTemplate(result.rows[0]);
  }
  
  async getTemplateVersion(consentType: string, version: string): Promise<ConsentTemplate | null> {
    const result = await this.pool.query(
      `SELECT * FROM consent_templates 
       WHERE consent_type = $1 AND version = $2 
       LIMIT 1`,
      [consentType, version]
    );
    
    if (result.rows.length === 0) return null;
    
    return this.mapRowToTemplate(result.rows[0]);
  }
  
  async getAllVersions(consentType: string): Promise<ConsentTemplate[]> {
    const result = await this.pool.query(
      `SELECT * FROM consent_templates 
       WHERE consent_type = $1 
       ORDER BY version DESC`,
      [consentType]
    );
    
    return result.rows.map(row => this.mapRowToTemplate(row));
  }
  
  async activateTemplate(id: string): Promise<void> {
    const template = await this.getTemplateById(id);
    
    if (!template) return;
    
    // Deactivate all versions of this consent type
    await this.pool.query(
      `UPDATE consent_templates 
       SET is_active = false 
       WHERE consent_type = $1`,
      [template.consentType]
    );
    
    // Activate the specified version
    await this.pool.query(
      `UPDATE consent_templates 
       SET is_active = true 
       WHERE id = $1`,
      [id]
    );
  }
  
  async getTemplateById(id: string): Promise<ConsentTemplate | null> {
    const result = await this.pool.query(
      'SELECT * FROM consent_templates WHERE id = $1',
      [id]
    );
    
    if (result.rows.length === 0) return null;
    
    return this.mapRowToTemplate(result.rows[0]);
  }
  
  private mapRowToTemplate(row: any): ConsentTemplate {
    return {
      id: row.id,
      name: row.name,
      consentType: row.consent_type,
      description: row.description,
      required: row.required,
      dataCollected: JSON.parse(row.data_collected),
      dataUsedFor: JSON.parse(row.data_used_for),
      thirdPartySharing: row.third_party_sharing,
      retentionPeriod: row.retention_period,
      version: row.version,
      isActive: row.is_active,
      createdAt: row.created_at,
      updatedAt: row.updated_at
    };
  }
}
```

---

## Withdrawal Mechanism

### Withdrawal Service

```typescript
// consent-withdrawal.ts
import { ConsentType } from './consent-types';

export interface WithdrawalRequest {
  id: string;
  userId: string;
  consentType: ConsentType;
  reason?: string;
  requestedAt: Date;
  processedAt?: Date;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  errorMessage?: string;
}

export class ConsentWithdrawalService {
  private withdrawals: Map<string, WithdrawalRequest> = new Map();
  
  requestWithdrawal(
    userId: string,
    consentType: ConsentType,
    reason?: string
  ): WithdrawalRequest {
    const request: WithdrawalRequest = {
      id: this.generateId(),
      userId,
      consentType,
      reason,
      requestedAt: new Date(),
      status: 'pending'
    };
    
    this.withdrawals.set(request.id, request);
    
    // Process withdrawal asynchronously
    this.processWithdrawal(request);
    
    return request;
  }
  
  async processWithdrawal(request: WithdrawalRequest): Promise<void> {
    request.status = 'processing';
    
    try {
      // Revoke consent
      await this.revokeConsent(request.userId, request.consentType);
      
      // Delete associated data if required
      await this.deleteAssociatedData(request.userId, request.consentType);
      
      // Notify user
      await this.notifyUser(request.userId, request.consentType);
      
      request.status = 'completed';
      request.processedAt = new Date();
    } catch (error) {
      request.status = 'failed';
      request.errorMessage = error.message;
      request.processedAt = new Date();
    }
  }
  
  getWithdrawalStatus(requestId: string): WithdrawalRequest | undefined {
    return this.withdrawals.get(requestId);
  }
  
  getUserWithdrawals(userId: string): WithdrawalRequest[] {
    return Array.from(this.withdrawals.values()).filter(
      w => w.userId === userId
    );
  }
  
  private async revokeConsent(userId: string, consentType: ConsentType): Promise<void> {
    // Implementation to revoke consent
    console.log(`Revoking consent ${consentType} for user ${userId}`);
  }
  
  private async deleteAssociatedData(
    userId: string,
    consentType: ConsentType
  ): Promise<void> {
    // Implementation to delete associated data
    console.log(`Deleting data for consent ${consentType} for user ${userId}`);
  }
  
  private async notifyUser(userId: string, consentType: ConsentType): Promise<void> {
    // Implementation to notify user
    console.log(`Notifying user ${userId} about withdrawal of ${consentType}`);
  }
  
  private generateId(): string {
    return `withdrawal_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

---

## Consent Logs

### Logging Service

```typescript
// consent-logging.ts

export enum ConsentAction {
  GRANTED = 'granted',
  REVOKED = 'revoked',
  UPDATED = 'updated',
  VIEWED = 'viewed',
  WITHDRAWN = 'withdrawn'
}

export interface ConsentLogEntry {
  id: string;
  userId: string;
  consentType: string;
  action: ConsentAction;
  previousValue?: boolean;
  newValue?: boolean;
  ipAddress?: string;
  userAgent?: string;
  timestamp: Date;
  metadata?: Record<string, any>;
}

export class ConsentLoggingService {
  private logs: ConsentLogEntry[] = [];
  
  logAction(
    userId: string,
    consentType: string,
    action: ConsentAction,
    previousValue?: boolean,
    newValue?: boolean,
    ipAddress?: string,
    userAgent?: string,
    metadata?: Record<string, any>
  ): ConsentLogEntry {
    const entry: ConsentLogEntry = {
      id: this.generateId(),
      userId,
      consentType,
      action,
      previousValue,
      newValue,
      ipAddress,
      userAgent,
      timestamp: new Date(),
      metadata
    };
    
    this.logs.push(entry);
    
    return entry;
  }
  
  getLogs(userId: string): ConsentLogEntry[] {
    return this.logs.filter(log => log.userId === userId);
  }
  
  getLogsByConsentType(userId: string, consentType: string): ConsentLogEntry[] {
    return this.logs.filter(
      log => log.userId === userId && log.consentType === consentType
    );
  }
  
  getLogsByAction(userId: string, action: ConsentAction): ConsentLogEntry[] {
    return this.logs.filter(
      log => log.userId === userId && log.action === action
    );
  }
  
  getLogsByDateRange(
    userId: string,
    startDate: Date,
    endDate: Date
  ): ConsentLogEntry[] {
    return this.logs.filter(
      log =>
        log.userId === userId &&
        log.timestamp >= startDate &&
        log.timestamp <= endDate
    );
  }
  
  exportLogs(userId: string): string {
    const logs = this.getLogs(userId);
    return JSON.stringify(logs, null, 2);
  }
  
  private generateId(): string {
    return `log_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

---

## Cookie Consent

### Cookie Consent Manager

```typescript
// cookie-consent-manager.ts

export interface CookieConsentConfig {
  domain: string;
  path: string;
  secure: boolean;
  sameSite: 'strict' | 'lax' | 'none';
  expirationDays: number;
}

export class CookieConsentManager {
  private config: CookieConsentConfig;
  
  constructor(config: Partial<CookieConsentConfig> = {}) {
    this.config = {
      domain: config.domain || window.location.hostname,
      path: config.path || '/',
      secure: config.secure || window.location.protocol === 'https:',
      sameSite: config.sameSite || 'lax',
      expirationDays: config.expirationDays || 365
    };
  }
  
  setConsentCookie(consents: Record<string, boolean>): void {
    const cookieValue = JSON.stringify(consents);
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + this.config.expirationDays);
    
    document.cookie = this.buildCookieString(
      'consent',
      cookieValue,
      expirationDate
    );
  }
  
  getConsentCookie(): Record<string, boolean> | null {
    const cookies = document.cookie.split('; ');
    
    for (const cookie of cookies) {
      const [name, value] = cookie.split('=');
      
      if (name === 'consent') {
        try {
          return JSON.parse(decodeURIComponent(value));
        } catch {
          return null;
        }
      }
    }
    
    return null;
  }
  
  hasConsentCookie(): boolean {
    return this.getConsentCookie() !== null;
  }
  
  clearConsentCookie(): void {
    const expirationDate = new Date(0);
    
    document.cookie = this.buildCookieString(
      'consent',
      '',
      expirationDate
    );
  }
  
  setConsentVersion(version: string): void {
    const expirationDate = new Date();
    expirationDate.setDate(expirationDate.getDate() + this.config.expirationDays);
    
    document.cookie = this.buildCookieString(
      'consent_version',
      version,
      expirationDate
    );
  }
  
  getConsentVersion(): string | null {
    const cookies = document.cookie.split('; ');
    
    for (const cookie of cookies) {
      const [name, value] = cookie.split('=');
      
      if (name === 'consent_version') {
        return decodeURIComponent(value);
      }
    }
    
    return null;
  }
  
  private buildCookieString(name: string, value: string, expirationDate: Date): string {
    return [
      `${name}=${encodeURIComponent(value)}`,
      `expires=${expirationDate.toUTCString()}`,
      `path=${this.config.path}`,
      `domain=${this.config.domain}`,
      this.config.secure ? 'secure' : '',
      `samesite=${this.config.sameSite}`
    ].filter(Boolean).join('; ');
  }
}
```

---

## Third-Party Consent

### Third-Party Manager

```typescript
// third-party-consent.ts

export interface ThirdPartyService {
  name: string;
  category: string;
  consentRequired: boolean;
  scriptUrl?: string;
  initialize?: () => void;
  cleanup?: () => void;
}

export class ThirdPartyConsentManager {
  private services: Map<string, ThirdPartyService> = new Map();
  private loadedServices: Set<string> = new Set();
  
  registerService(service: ThirdPartyService): void {
    this.services.set(service.name, service);
  }
  
  async loadService(serviceName: string, granted: boolean): Promise<void> {
    const service = this.services.get(serviceName);
    
    if (!service) return;
    
    if (!granted) {
      this.unloadService(serviceName);
      return;
    }
    
    if (this.loadedServices.has(serviceName)) return;
    
    if (service.scriptUrl) {
      await this.loadScript(service.scriptUrl);
    }
    
    if (service.initialize) {
      service.initialize();
    }
    
    this.loadedServices.add(serviceName);
  }
  
  unloadService(serviceName: string): void {
    const service = this.services.get(serviceName);
    
    if (!service) return;
    
    if (!this.loadedServices.has(serviceName)) return;
    
    if (service.cleanup) {
      service.cleanup();
    }
    
    this.loadedServices.delete(serviceName);
  }
  
  loadServicesBasedOnConsent(consents: Record<string, boolean>): void {
    for (const [serviceName, service] of this.services.entries()) {
      const consentGranted = consents[serviceName] || false;
      
      if (service.consentRequired && !consentGranted) {
        this.unloadService(serviceName);
      } else {
        this.loadService(serviceName, consentGranted);
      }
    }
  }
  
  private loadScript(url: string): Promise<void> {
    return new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = url;
      script.async = true;
      
      script.onload = () => resolve();
      script.onerror = () => reject(new Error(`Failed to load script: ${url}`));
      
      document.head.appendChild(script);
    });
  }
}
```

---

## Compliance Verification

### Compliance Checker

```typescript
// consent-compliance.ts

export interface ComplianceCheck {
  framework: string;
  passed: boolean;
  requirements: string[];
  findings: string[];
  recommendations: string[];
}

export class ConsentComplianceChecker {
  static checkGDPRCompliance(consentData: any): ComplianceCheck {
    const requirements = [
      'Consent must be freely given',
      'Consent must be specific and informed',
      'Consent must be unambiguous',
      'Consent must be given by a clear affirmative action',
      'User must be able to withdraw consent as easily as giving it',
      'Consent records must be maintained',
      'Consent must be verifiable'
    ];
    
    const findings: string[] = [];
    const recommendations: string[] = [];
    let passed = true;
    
    // Check for affirmative action
    if (!consentData.affirmativeAction) {
      findings.push('Consent not given by affirmative action');
      recommendations.push('Implement explicit opt-in mechanism');
      passed = false;
    }
    
    // Check for specificity
    if (!consentData.specificConsent) {
      findings.push('Consent not specific enough');
      recommendations.push('Implement granular consent');
      passed = false;
    }
    
    // Check for informed consent
    if (!consentData.informedConsent) {
      findings.push('User not properly informed');
      recommendations.push('Provide clear information about data use');
      passed = false;
    }
    
    // Check for withdrawal mechanism
    if (!consentData.withdrawalMechanism) {
      findings.push('No easy withdrawal mechanism');
      recommendations.push('Implement easy consent withdrawal');
      passed = false;
    }
    
    // Check for consent records
    if (!consentData.consentRecords) {
      findings.push('No consent records maintained');
      recommendations.push('Implement consent logging');
      passed = false;
    }
    
    return {
      framework: 'GDPR',
      passed,
      requirements,
      findings,
      recommendations
    };
  }
  
  static checkCCPACompliance(consentData: any): ComplianceCheck {
    const requirements = [
      'Users must be informed about data collection',
      'Users must be able to opt-out of data sale',
      'Users must be able to opt-out of data sharing',
      'Do Not Sell link must be prominent',
      'Opt-out must be easy to use'
    ];
    
    const findings: string[] = [];
    const recommendations: string[] = [];
    let passed = true;
    
    // Check for Do Not Sell link
    if (!consentData.doNotSellLink) {
      findings.push('Do Not Sell link not present');
      recommendations.push('Add prominent Do Not Sell link');
      passed = false;
    }
    
    // Check for opt-out mechanism
    if (!consentData.optOutMechanism) {
      findings.push('No opt-out mechanism');
      recommendations.push('Implement opt-out mechanism');
      passed = false;
    }
    
    return {
      framework: 'CCPA',
      passed,
      requirements,
      findings,
      recommendations
    };
  }
}
```

---

## Best Practices

```markdown
## Consent Management Best Practices

### Consent Collection
- [ ] Use clear, plain language
- [ ] Separate consent from terms and conditions
- [ ] Use affirmative opt-in (no pre-checked boxes)
- [ ] Implement granular consent
- [ ] Provide detailed information about data use
- [ ] Make consent easy to give and withdraw
- [ ] Use cookie banners appropriately
- [ ] Implement consent for all data collection

### Consent Storage
- [ ] Store consent records securely
- [ ] Maintain consent history
- [ ] Track consent version changes
- [ ] Log all consent actions
- [ ] Implement data retention for consent records
- [ ] Ensure consent records are tamper-evident

### Consent Management
- [ ] Implement easy withdrawal mechanism
- [ ] Provide consent management UI
- [ ] Allow users to view their consent history
- [ ] Notify users of consent changes
- [ ] Implement consent versioning
- [ ] Handle consent expiry properly

### Third-Party Integration
- [ ] Only load third-party scripts with consent
- [ ] Implement lazy loading for non-essential services
- [ ] Provide clear information about third parties
- [ ] Allow users to opt-out of specific third parties
- [ ] Monitor third-party script behavior

### Compliance
- [ ] Understand applicable regulations (GDPR, CCPA, etc.)
- [ ] Implement required consent types
- [ ] Maintain proper documentation
- [ ] Regularly audit consent practices
- [ ] Keep consent policies up to date
- [ ] Implement proper data handling based on consent

### User Experience
- [ ] Design intuitive consent UI
- [ ] Provide clear explanations
- [ ] Make consent management easily accessible
- [ ] Use appropriate timing for consent requests
- [ ] Provide feedback on consent actions
- [ ] Consider mobile experience

### Technical Implementation
- [ ] Use secure cookie settings
- [ ] Implement proper consent storage
- [ ] Handle consent across subdomains
- [ ] Implement consent synchronization
- [ ] Handle consent expiry gracefully
- [ ] Monitor consent-related errors
```

---

## Additional Resources

- [GDPR Consent Guidelines](https://gdpr.eu/consent/)
- [IAB Europe Transparency & Consent Framework](https://iabeurope.eu/tcf/)
- [CCPA Compliance Guide](https://oag.ca.gov/privacy/ccpa)
- [Cookie Consent Best Practices](https://www.cookiebot.com/en/cookie-consent/)
