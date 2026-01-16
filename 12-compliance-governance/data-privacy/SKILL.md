# Data Privacy

## Overview

Comprehensive guide to data privacy implementation patterns and best practices.

## Table of Contents

1. [Privacy Principles](#privacy-principles)
2. [PII Identification and Classification](#pii-identification-and-classification)
3. [Data Encryption](#data-encryption)
4. [Data Anonymization](#data-anonymization)
5. [Data Pseudonymization](#data-pseudonymization)
6. [Access Controls](#access-controls)
7. [Data Masking](#data-masking)
8. [Privacy-Preserving Techniques](#privacy-preserving-techniques)
9. [Privacy Policy Implementation](#privacy-policy-implementation)
10. [Cookie Consent](#cookie-consent)
11. [Testing Privacy Controls](#testing-privacy-controls)

---

## Privacy Principles

### Core Privacy Principles

```typescript
// privacy-principles.ts

export enum PrivacyPrinciple {
  LAWFULNESS = 'lawfulness',
  FAIRNESS = 'fairness',
  TRANSPARENCY = 'transparency',
  PURPOSE_LIMITATION = 'purpose_limitation',
  DATA_MINIMIZATION = 'data_minimization',
  ACCURACY = 'accuracy',
  STORAGE_LIMITATION = 'storage_limitation',
  INTEGRITY_CONFIDENTIALITY = 'integrity_confidentiality',
  ACCOUNTABILITY = 'accountability'
}

export interface PrivacyAssessment {
  principle: PrivacyPrinciple;
  status: 'compliant' | 'non_compliant' | 'partial';
  findings: string[];
  recommendations: string[];
}

export class PrivacyPrinciplesAssessor {
  static assessLawfulness(dataProcessing: any): PrivacyAssessment {
    const findings: string[] = [];
    const recommendations: string[] = [];
    let status: 'compliant' | 'non_compliant' | 'partial' = 'compliant';
    
    if (!dataProcessing.legalBasis) {
      findings.push('No legal basis documented');
      recommendations.push('Document legal basis for all data processing');
      status = 'non_compliant';
    }
    
    if (dataProcessing.legalBasis === 'consent' && !dataProcessing.consentObtained) {
      findings.push('Consent not obtained');
      recommendations.push('Obtain explicit consent');
      status = 'non_compliant';
    }
    
    return {
      principle: PrivacyPrinciple.LAWFULNESS,
      status,
      findings,
      recommendations
    };
  }
  
  static assessTransparency(dataProcessing: any): PrivacyAssessment {
    const findings: string[] = [];
    const recommendations: string[] = [];
    let status: 'compliant' | 'non_compliant' | 'partial' = 'compliant';
    
    if (!dataProcessing.privacyPolicy) {
      findings.push('No privacy policy');
      recommendations.push('Create and publish privacy policy');
      status = 'non_compliant';
    }
    
    if (!dataProcessing.cookiePolicy) {
      findings.push('No cookie policy');
      recommendations.push('Create and publish cookie policy');
      status = 'partial';
    }
    
    return {
      principle: PrivacyPrinciple.TRANSPARENCY,
      status,
      findings,
      recommendations
    };
  }
  
  static assessDataMinimization(dataProcessing: any): PrivacyAssessment {
    const findings: string[] = [];
    const recommendations: string[] = [];
    let status: 'compliant' | 'non_compliant' | 'partial' = 'compliant';
    
    const unnecessaryFields = dataProcessing.collectedFields.filter(
      (field: string) => !dataProcessing.requiredFields.includes(field)
    );
    
    if (unnecessaryFields.length > 0) {
      findings.push(`Unnecessary fields collected: ${unnecessaryFields.join(', ')}`);
      recommendations.push('Remove unnecessary data collection');
      status = 'partial';
    }
    
    return {
      principle: PrivacyPrinciple.DATA_MINIMIZATION,
      status,
      findings,
      recommendations
    };
  }
  
  static assessStorageLimitation(dataProcessing: any): PrivacyAssessment {
    const findings: string[] = [];
    const recommendations: string[] = [];
    let status: 'compliant' | 'non_compliant' | 'partial' = 'compliant';
    
    if (!dataProcessing.retentionPolicy) {
      findings.push('No retention policy');
      recommendations.push('Define data retention policy');
      status = 'non_compliant';
    }
    
    if (!dataProcessing.autoDeletion) {
      findings.push('No automatic deletion mechanism');
      recommendations.push('Implement automatic data deletion');
      status = 'partial';
    }
    
    return {
      principle: PrivacyPrinciple.STORAGE_LIMITATION,
      status,
      findings,
      recommendations
    };
  }
  
  static assessIntegrityConfidentiality(dataProcessing: any): PrivacyAssessment {
    const findings: string[] = [];
    const recommendations: string[] = [];
    let status: 'compliant' | 'non_compliant' | 'partial' = 'compliant';
    
    if (!dataProcessing.encryptionAtRest) {
      findings.push('Data not encrypted at rest');
      recommendations.push('Implement encryption at rest');
      status = 'non_compliant';
    }
    
    if (!dataProcessing.encryptionInTransit) {
      findings.push('Data not encrypted in transit');
      recommendations.push('Use HTTPS/TLS');
      status = 'non_compliant';
    }
    
    if (!dataProcessing.accessControls) {
      findings.push('No access controls');
      recommendations.push('Implement access controls');
      status = 'non_compliant';
    }
    
    return {
      principle: PrivacyPrinciple.INTEGRITY_CONFIDENTIALITY,
      status,
      findings,
      recommendations
    };
  }
}
```

---

## PII Identification and Classification

### PII Classifier

```typescript
// pii-classifier.ts

export enum PIIClassification {
  DIRECT = 'direct',           // Directly identifies individual (name, email, phone)
  INDIRECT = 'indirect',       // Can identify with other data (location, IP)
  SENSITIVE = 'sensitive',     // Requires special protection (SSN, health data)
  PUBLIC = 'public'            // Publicly available information
}

export interface PIIField {
  name: string;
  type: PIIClassification;
  description: string;
  examples: string[];
}

export class PIIClassifier {
  private static readonly PII_PATTERNS: Record<string, RegExp> = {
    email: /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/,
    phone: /^\+?[\d\s-()]{10,}$/,
    ssn: /^\d{3}-\d{2}-\d{4}$/,
    creditCard: /^\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}$/,
    ipAddress: /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/,
    dateOfBirth: /^\d{4}-\d{2}-\d{2}$/
  };
  
  private static readonly PII_FIELDS: PIIField[] = [
    {
      name: 'fullName',
      type: PIIClassification.DIRECT,
      description: 'Full name of individual',
      examples: ['John Doe', 'Jane Smith']
    },
    {
      name: 'email',
      type: PIIClassification.DIRECT,
      description: 'Email address',
      examples: ['john.doe@example.com']
    },
    {
      name: 'phoneNumber',
      type: PIIClassification.DIRECT,
      description: 'Phone number',
      examples: ['+1-555-123-4567']
    },
    {
      name: 'address',
      type: PIIClassification.INDIRECT,
      description: 'Physical address',
      examples: ['123 Main St, City, State 12345']
    },
    {
      name: 'ssn',
      type: PIIClassification.SENSITIVE,
      description: 'Social Security Number',
      examples: ['123-45-6789']
    },
    {
      name: 'creditCard',
      type: PIIClassification.SENSITIVE,
      description: 'Credit card number',
      examples: ['1234-5678-9012-3456']
    },
    {
      name: 'dateOfBirth',
      type: PIIClassification.DIRECT,
      description: 'Date of birth',
      examples: ['1990-01-15']
    },
    {
      name: 'ipAddress',
      type: PIIClassification.INDIRECT,
      description: 'IP address',
      examples: ['192.168.1.1']
    },
    {
      name: 'healthData',
      type: PIIClassification.SENSITIVE,
      description: 'Health information',
      examples: ['Medical records, test results']
    }
  ];
  
  static classifyField(fieldName: string, value: string): PIIClassification {
    const field = this.PII_FIELDS.find(f => f.name === fieldName);
    if (field) return field.type;
    
    // Check patterns
    for (const [patternName, pattern] of Object.entries(this.PII_PATTERNS)) {
      if (pattern.test(value)) {
        return this.getClassificationForPattern(patternName);
      }
    }
    
    return PIIClassification.PUBLIC;
  }
  
  static detectPII(data: Record<string, any>): Array<{ field: string; classification: PIIClassification }> {
    const detected: Array<{ field: string; classification: PIIClassification }> = [];
    
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'string') {
        const classification = this.classifyField(key, value);
        if (classification !== PIIClassification.PUBLIC) {
          detected.push({ field: key, classification });
        }
      }
    }
    
    return detected;
  }
  
  static getClassificationForPattern(patternName: string): PIIClassification {
    const sensitivePatterns = ['ssn', 'creditCard', 'healthData'];
    const directPatterns = ['email', 'phone', 'dateOfBirth'];
    
    if (sensitivePatterns.includes(patternName)) return PIIClassification.SENSITIVE;
    if (directPatterns.includes(patternName)) return PIIClassification.DIRECT;
    
    return PIIClassification.INDIRECT;
  }
  
  static getPIIFields(): PIIField[] {
    return this.PII_FIELDS;
  }
}
```

---

## Data Encryption

### Encryption Service

```typescript
// encryption-service.ts
import crypto from 'crypto';

export class DataEncryptionService {
  private readonly algorithm = 'aes-256-gcm';
  private readonly keyLength = 32;
  private readonly ivLength = 16;
  private readonly saltLength = 64;
  private readonly tagLength = 16;
  private readonly iterations = 100000;
  
  constructor(private encryptionKey: string) {}
  
  encrypt(data: string): { encrypted: string; iv: string; tag: string } {
    const iv = crypto.randomBytes(this.ivLength);
    const cipher = crypto.createCipheriv(
      this.algorithm,
      Buffer.from(this.encryptionKey, 'hex'),
      iv
    );
    
    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const tag = cipher.getAuthTag();
    
    return {
      encrypted,
      iv: iv.toString('hex'),
      tag: tag.toString('hex')
    };
  }
  
  decrypt(encrypted: string, iv: string, tag: string): string {
    const decipher = crypto.createDecipheriv(
      this.algorithm,
      Buffer.from(this.encryptionKey, 'hex'),
      Buffer.from(iv, 'hex')
    );
    
    decipher.setAuthTag(Buffer.from(tag, 'hex'));
    
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  }
  
  encryptWithPassword(data: string, password: string): {
    encrypted: string;
    salt: string;
    iv: string;
    tag: string;
  } {
    const salt = crypto.randomBytes(this.saltLength);
    const key = this.deriveKey(password, salt);
    const iv = crypto.randomBytes(this.ivLength);
    
    const cipher = crypto.createCipheriv(this.algorithm, key, iv);
    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const tag = cipher.getAuthTag();
    
    return {
      encrypted,
      salt: salt.toString('hex'),
      iv: iv.toString('hex'),
      tag: tag.toString('hex')
    };
  }
  
  decryptWithPassword(
    encrypted: string,
    password: string,
    salt: string,
    iv: string,
    tag: string
  ): string {
    const key = this.deriveKey(password, Buffer.from(salt, 'hex'));
    
    const decipher = crypto.createDecipheriv(this.algorithm, key, Buffer.from(iv, 'hex'));
    decipher.setAuthTag(Buffer.from(tag, 'hex'));
    
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  }
  
  hash(data: string): string {
    return crypto.createHash('sha256').update(data).digest('hex');
  }
  
  private deriveKey(password: string, salt: Buffer): Buffer {
    return crypto.pbkdf2Sync(
      password,
      salt,
      this.iterations,
      this.keyLength,
      'sha256'
    );
  }
}
```

### Field-Level Encryption

```typescript
// field-encryption.ts
import { DataEncryptionService } from './encryption-service';
import { PIIClassifier, PIIClassification } from './pii-classifier';

export class FieldLevelEncryption {
  constructor(private encryptionService: DataEncryptionService) {}
  
  encryptSensitiveFields(data: Record<string, any>): Record<string, any> {
    const result: Record<string, any> = { ...data };
    
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'string') {
        const classification = PIIClassifier.classifyField(key, value);
        
        if (classification === PIIClassification.SENSITIVE) {
          const encrypted = this.encryptionService.encrypt(value);
          result[key] = {
            encrypted: true,
            data: encrypted.encrypted,
            iv: encrypted.iv,
            tag: encrypted.tag
          };
        }
      }
    }
    
    return result;
  }
  
  decryptSensitiveFields(data: Record<string, any>): Record<string, any> {
    const result: Record<string, any> = { ...data };
    
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'object' && value !== null && value.encrypted) {
        const decrypted = this.encryptionService.decrypt(
          value.data,
          value.iv,
          value.tag
        );
        result[key] = decrypted;
      }
    }
    
    return result;
  }
  
  encryptField(fieldName: string, value: string): any {
    const classification = PIIClassifier.classifyField(fieldName, value);
    
    if (classification === PIIClassification.SENSITIVE) {
      const encrypted = this.encryptionService.encrypt(value);
      return {
        encrypted: true,
        data: encrypted.encrypted,
        iv: encrypted.iv,
        tag: encrypted.tag
      };
    }
    
    return value;
  }
  
  decryptField(fieldName: string, value: any): string {
    if (typeof value === 'object' && value !== null && value.encrypted) {
      return this.encryptionService.decrypt(value.data, value.iv, value.tag);
    }
    
    return value;
  }
}
```

---

## Data Anonymization

### Anonymization Service

```typescript
// anonymization-service.ts

export class DataAnonymizationService {
  anonymizeEmail(email: string): string {
    const [username, domain] = email.split('@');
    const maskedUsername = username.substring(0, 2) + '***';
    return `${maskedUsername}@${domain}`;
  }
  
  anonymizePhone(phone: string): string {
    // Keep last 4 digits
    const digits = phone.replace(/\D/g, '');
    const visible = digits.substring(digits.length - 4);
    const masked = '*'.repeat(digits.length - 4);
    return `${masked}${visible}`;
  }
  
  anonymizeSSN(ssn: string): string {
    return '***-**-' + ssn.substring(ssn.length - 4);
  }
  
  anonymizeCreditCard(card: string): string {
    const digits = card.replace(/\D/g, '');
    return '****-****-****-' + digits.substring(digits.length - 4);
  }
  
  anonymizeName(name: string): string {
    const parts = name.split(' ');
    return parts.map(part => part.substring(0, 1) + '***').join(' ');
  }
  
  anonymizeAddress(address: string): string {
    // Keep city and state, mask street address
    const parts = address.split(',');
    if (parts.length >= 2) {
      return `*** ${parts.slice(1).join(',')}`;
    }
    return '***';
  }
  
  anonymizeIP(ip: string): string {
    const parts = ip.split('.');
    return `${parts[0]}.${parts[1]}.***.***`;
  }
  
  anonymizeDate(date: string): string {
    // Keep only year
    return date.substring(0, 4);
  }
  
  anonymizeData(data: Record<string, any>): Record<string, any> {
    const result: Record<string, any> = { ...data };
    
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'string') {
        if (key.toLowerCase().includes('email')) {
          result[key] = this.anonymizeEmail(value);
        } else if (key.toLowerCase().includes('phone')) {
          result[key] = this.anonymizePhone(value);
        } else if (key.toLowerCase().includes('ssn')) {
          result[key] = this.anonymizeSSN(value);
        } else if (key.toLowerCase().includes('creditcard') || key.toLowerCase().includes('card')) {
          result[key] = this.anonymizeCreditCard(value);
        } else if (key.toLowerCase().includes('name')) {
          result[key] = this.anonymizeName(value);
        } else if (key.toLowerCase().includes('address')) {
          result[key] = this.anonymizeAddress(value);
        } else if (key.toLowerCase().includes('ip') || key.toLowerCase().includes('ipaddress')) {
          result[key] = this.anonymizeIP(value);
        } else if (key.toLowerCase().includes('date') || key.toLowerCase().includes('dob')) {
          result[key] = this.anonymizeDate(value);
        }
      }
    }
    
    return result;
  }
}
```

---

## Data Pseudonymization

### Pseudonymization Service

```typescript
// pseudonymization-service.ts
import crypto from 'crypto';

export class DataPseudonymizationService {
  private readonly salt: string;
  
  constructor(salt?: string) {
    this.salt = salt || crypto.randomBytes(16).toString('hex');
  }
  
  pseudonymize(value: string): string {
    const hash = crypto
      .createHmac('sha256', this.salt)
      .update(value)
      .digest('hex');
    
    return hash.substring(0, 16);
  }
  
  pseudonymizeEmail(email: string): string {
    const [username, domain] = email.split('@');
    const pseudonym = this.pseudonymize(username);
    return `${pseudonym}@${domain}`;
  }
  
  pseudonymizePhone(phone: string): string {
    const digits = phone.replace(/\D/g, '');
    const pseudonym = this.pseudonymize(digits);
    return pseudonym;
  }
  
  pseudonymizeID(id: string): string {
    return this.pseudonymize(id);
  }
  
  pseudonymizeData(data: Record<string, any>): Record<string, any> {
    const result: Record<string, any> = { ...data };
    
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'string') {
        if (key.toLowerCase().includes('email')) {
          result[key] = this.pseudonymizeEmail(value);
        } else if (key.toLowerCase().includes('phone')) {
          result[key] = this.pseudonymizePhone(value);
        } else if (key.toLowerCase().includes('id')) {
          result[key] = this.pseudonymizeID(value);
        }
      }
    }
    
    return result;
  }
}
```

---

## Access Controls

### RBAC for Privacy

```typescript
// privacy-access-control.ts

export enum PrivacyPermission {
  VIEW_PII = 'view_pii',
  EDIT_PII = 'edit_pii',
  DELETE_PII = 'delete_pii',
  EXPORT_PII = 'export_pii',
  VIEW_SENSITIVE = 'view_sensitive',
  EDIT_SENSITIVE = 'edit_sensitive',
  AUDIT_ACCESS = 'audit_access'
}

export interface PrivacyRole {
  name: string;
  permissions: PrivacyPermission[];
  description: string;
}

export class PrivacyAccessControl {
  private static readonly ROLES: PrivacyRole[] = [
    {
      name: 'admin',
      permissions: Object.values(PrivacyPermission),
      description: 'Full access to all data'
    },
    {
      name: 'support',
      permissions: [
        PrivacyPermission.VIEW_PII,
        PrivacyPermission.AUDIT_ACCESS
      ],
      description: 'Can view PII for support purposes'
    },
    {
      name: 'analyst',
      permissions: [
        PrivacyPermission.VIEW_PII,
        PrivacyPermission.EXPORT_PII,
        PrivacyPermission.AUDIT_ACCESS
      ],
      description: 'Can view and export PII for analysis'
    },
    {
      name: 'user',
      permissions: [],
      description: 'No access to other users PII'
    }
  ];
  
  static hasPermission(
    userRole: string,
    permission: PrivacyPermission
  ): boolean {
    const role = this.ROLES.find(r => r.name === userRole);
    return role ? role.permissions.includes(permission) : false;
  }
  
  static canViewPII(userRole: string): boolean {
    return this.hasPermission(userRole, PrivacyPermission.VIEW_PII);
  }
  
  static canEditPII(userRole: string): boolean {
    return this.hasPermission(userRole, PrivacyPermission.EDIT_PII);
  }
  
  static canDeletePII(userRole: string): boolean {
    return this.hasPermission(userRole, PrivacyPermission.DELETE_PII);
  }
  
  static canExportPII(userRole: string): boolean {
    return this.hasPermission(userRole, PrivacyPermission.EXPORT_PII);
  }
  
  static canViewSensitive(userRole: string): boolean {
    return this.hasPermission(userRole, PrivacyPermission.VIEW_SENSITIVE);
  }
  
  static filterSensitiveData(
    data: Record<string, any>,
    userRole: string
  ): Record<string, any> {
    const result: Record<string, any> = {};
    
    for (const [key, value] of Object.entries(data)) {
      const isSensitive = this.isSensitiveField(key);
      
      if (!isSensitive || this.canViewSensitive(userRole)) {
        result[key] = value;
      } else {
        result[key] = '***';
      }
    }
    
    return result;
  }
  
  private static isSensitiveField(fieldName: string): boolean {
    const sensitivePatterns = [
      'ssn', 'creditcard', 'health', 'medical', 'financial'
    ];
    
    return sensitivePatterns.some(pattern =>
      fieldName.toLowerCase().includes(pattern)
    );
  }
}
```

---

## Data Masking

### Masking Service

```typescript
// data-masking.ts

export enum MaskingStrategy {
  FULL = 'full',
  PARTIAL = 'partial',
  HASH = 'hash',
  NULL = 'null'
}

export class DataMaskingService {
  mask(value: string, strategy: MaskingStrategy): string {
    switch (strategy) {
      case MaskingStrategy.FULL:
        return '*'.repeat(value.length);
      case MaskingStrategy.PARTIAL:
        return this.partialMask(value);
      case MaskingStrategy.HASH:
        return this.hashMask(value);
      case MaskingStrategy.NULL:
        return '';
      default:
        return value;
    }
  }
  
  private partialMask(value: string): string {
    if (value.length <= 4) return '***';
    const visible = value.substring(value.length - 4);
    return '*'.repeat(value.length - 4) + visible;
  }
  
  private hashMask(value: string): string {
    const crypto = require('crypto');
    return crypto.createHash('sha256').update(value).digest('hex').substring(0, 8);
  }
  
  maskEmail(value: string, strategy: MaskingStrategy = MaskingStrategy.PARTIAL): string {
    if (strategy === MaskingStrategy.PARTIAL) {
      const [username, domain] = value.split('@');
      const maskedUsername = username.substring(0, 2) + '***';
      return `${maskedUsername}@${domain}`;
    }
    return this.mask(value, strategy);
  }
  
  maskPhone(value: string, strategy: MaskingStrategy = MaskingStrategy.PARTIAL): string {
    if (strategy === MaskingStrategy.PARTIAL) {
      const digits = value.replace(/\D/g, '');
      const visible = digits.substring(digits.length - 4);
      return '*'.repeat(digits.length - 4) + visible;
    }
    return this.mask(value, strategy);
  }
  
  maskCreditCard(value: string, strategy: MaskingStrategy = MaskingStrategy.PARTIAL): string {
    if (strategy === MaskingStrategy.PARTIAL) {
      const digits = value.replace(/\D/g, '');
      return '****-****-****-' + digits.substring(digits.length - 4);
    }
    return this.mask(value, strategy);
  }
  
  maskData(
    data: Record<string, any>,
    maskingRules: Record<string, MaskingStrategy>
  ): Record<string, any> {
    const result: Record<string, any> = { ...data };
    
    for (const [key, value] of Object.entries(data)) {
      if (typeof value === 'string' && maskingRules[key]) {
        if (key.toLowerCase().includes('email')) {
          result[key] = this.maskEmail(value, maskingRules[key]);
        } else if (key.toLowerCase().includes('phone')) {
          result[key] = this.maskPhone(value, maskingRules[key]);
        } else if (key.toLowerCase().includes('creditcard') || key.toLowerCase().includes('card')) {
          result[key] = this.maskCreditCard(value, maskingRules[key]);
        } else {
          result[key] = this.mask(value, maskingRules[key]);
        }
      }
    }
    
    return result;
  }
}
```

---

## Privacy-Preserving Techniques

### Differential Privacy

```typescript
// differential-privacy.ts

export class DifferentialPrivacyService {
  private readonly epsilon: number;
  
  constructor(epsilon: number = 1.0) {
    this.epsilon = epsilon;
  }
  
  addLaplaceNoise(value: number, sensitivity: number = 1): number {
    const scale = sensitivity / this.epsilon;
    const noise = this.laplaceNoise(scale);
    return value + noise;
  }
  
  private laplaceNoise(scale: number): number {
    const u = Math.random() - 0.5;
    return -scale * Math.sign(u) * Math.log(1 - 2 * Math.abs(u));
  }
  
  addGaussianNoise(value: number, sensitivity: number = 1): number {
    const sigma = Math.sqrt(2 * Math.log(1.25)) * sensitivity / this.epsilon;
    const noise = this.gaussianNoise(sigma);
    return value + noise;
  }
  
  private gaussianNoise(sigma: number): number {
    const u1 = Math.random();
    const u2 = Math.random();
    const z = Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2);
    return sigma * z;
  }
  
  privatizeCount(count: number): number {
    return Math.max(0, Math.round(this.addLaplaceNoise(count, 1)));
  }
  
  privatizeSum(values: number[]): number {
    const sum = values.reduce((a, b) => a + b, 0);
    return this.addLaplaceNoise(sum, values.length);
  }
  
  privatizeAverage(values: number[]): number {
    const sum = values.reduce((a, b) => a + b, 0);
    const avg = sum / values.length;
    return this.addLaplaceNoise(avg, 1);
  }
}
```

### K-Anonymity

```typescript
// k-anonymity.ts

export class KAnonymityService {
  checkKAnonymity(data: any[], k: number, quasiIdentifiers: string[]): boolean {
    const groups = this.groupByQuasiIdentifiers(data, quasiIdentifiers);
    
    for (const group of groups) {
      if (group.length < k) {
        return false;
      }
    }
    
    return true;
  }
  
  private groupByQuasiIdentifiers(data: any[], quasiIdentifiers: string[]): any[][] {
    const groups: Map<string, any[]> = new Map();
    
    for (const record of data) {
      const key = this.getQuasiIdentifierKey(record, quasiIdentifiers);
      
      if (!groups.has(key)) {
        groups.set(key, []);
      }
      
      groups.get(key)!.push(record);
    }
    
    return Array.from(groups.values());
  }
  
  private getQuasiIdentifierKey(record: any, quasiIdentifiers: string[]): string {
    return quasiIdentifiers
      .map(id => record[id])
      .join('|');
  }
  
  generalizeAge(age: number): string {
    if (age < 20) return '<20';
    if (age < 30) return '20-29';
    if (age < 40) return '30-39';
    if (age < 50) return '40-49';
    if (age < 60) return '50-59';
    return '60+';
  }
  
  generalizeZipCode(zipCode: string): string {
    return zipCode.substring(0, 3) + '***';
  }
  
  generalizeDate(date: string): string {
    return date.substring(0, 4); // Keep only year
  }
}
```

---

## Privacy Policy Implementation

### Policy Manager

```typescript
// privacy-policy.ts

export interface PrivacyPolicy {
  version: string;
  effectiveDate: Date;
  dataCollected: DataCollection[];
  dataUsage: DataUsage[];
  dataSharing: DataSharing[];
  userRights: UserRight[];
  contactInfo: ContactInfo;
}

export interface DataCollection {
  dataType: string;
  purpose: string;
  legalBasis: string;
  retention: string;
}

export interface DataUsage {
  dataType: string;
  usage: string[];
}

export interface DataSharing {
  dataType: string;
  recipient: string;
  purpose: string;
}

export interface UserRight {
  right: string;
  description: string;
  howToExercise: string;
}

export interface ContactInfo {
  name: string;
  email: string;
  address?: string;
  phone?: string;
}

export class PrivacyPolicyManager {
  private policy: PrivacyPolicy;
  
  constructor(policy: PrivacyPolicy) {
    this.policy = policy;
  }
  
  generatePolicy(): string {
    let policyText = `# Privacy Policy\n\n`;
    policyText += `**Version:** ${this.policy.version}\n`;
    policyText += `**Effective Date:** ${this.policy.effectiveDate.toISOString()}\n\n`;
    
    policyText += `## Data We Collect\n\n`;
    for (const collection of this.policy.dataCollected) {
      policyText += `### ${collection.dataType}\n`;
      policyText += `- **Purpose:** ${collection.purpose}\n`;
      policyText += `- **Legal Basis:** ${collection.legalBasis}\n`;
      policyText += `- **Retention Period:** ${collection.retention}\n\n`;
    }
    
    policyText += `## How We Use Your Data\n\n`;
    for (const usage of this.policy.dataUsage) {
      policyText += `### ${usage.dataType}\n`;
      policyText += `- Uses: ${usage.usage.join(', ')}\n\n`;
    }
    
    policyText += `## Data Sharing\n\n`;
    for (const sharing of this.policy.dataSharing) {
      policyText += `- **Data:** ${sharing.dataType}\n`;
      policyText += `- **Recipient:** ${sharing.recipient}\n`;
      policyText += `- **Purpose:** ${sharing.purpose}\n\n`;
    }
    
    policyText += `## Your Rights\n\n`;
    for (const right of this.policy.userRights) {
      policyText += `### ${right.right}\n`;
      policyText += `${right.description}\n\n`;
      policyText += `**How to Exercise:** ${right.howToExercise}\n\n`;
    }
    
    policyText += `## Contact Us\n\n`;
    policyText += `- **Name:** ${this.policy.contactInfo.name}\n`;
    policyText += `- **Email:** ${this.policy.contactInfo.email}\n`;
    if (this.policy.contactInfo.address) {
      policyText += `- **Address:** ${this.policy.contactInfo.address}\n`;
    }
    if (this.policy.contactInfo.phone) {
      policyText += `- **Phone:** ${this.policy.contactInfo.phone}\n`;
    }
    
    return policyText;
  }
  
  updatePolicy(updates: Partial<PrivacyPolicy>): PrivacyPolicy {
    this.policy = { ...this.policy, ...updates };
    return this.policy;
  }
}
```

---

## Cookie Consent

### Cookie Consent Manager

```typescript
// cookie-consent.ts

export enum CookieCategory {
  NECESSARY = 'necessary',
  FUNCTIONAL = 'functional',
  ANALYTICS = 'analytics',
  MARKETING = 'marketing'
}

export interface CookieConsent {
  userId?: string;
  consentId: string;
  timestamp: Date;
  categories: Record<CookieCategory, boolean>;
  version: string;
}

export class CookieConsentManager {
  private consents: Map<string, CookieConsent> = new Map();
  
  recordConsent(
    userId: string | undefined,
    categories: Record<CookieCategory, boolean>,
    version: string
  ): CookieConsent {
    const consent: CookieConsent = {
      userId,
      consentId: this.generateId(),
      timestamp: new Date(),
      categories,
      version
    };
    
    if (userId) {
      this.consents.set(userId, consent);
    }
    
    return consent;
  }
  
  getConsent(userId: string): CookieConsent | undefined {
    return this.consents.get(userId);
  }
  
  hasConsent(userId: string, category: CookieCategory): boolean {
    const consent = this.getConsent(userId);
    return consent ? consent.categories[category] : false;
  }
  
  updateConsent(
    userId: string,
    categories: Partial<Record<CookieCategory, boolean>>
  ): CookieConsent | undefined {
    const consent = this.getConsent(userId);
    if (!consent) return undefined;
    
    consent.categories = { ...consent.categories, ...categories };
    consent.timestamp = new Date();
    
    return consent;
  }
  
  generateConsentScript(consent: CookieConsent): string {
    const categories = Object.entries(consent.categories)
      .filter(([_, allowed]) => allowed)
      .map(([category]) => category);
    
    return `
// Cookie Consent
window.consentConfig = {
  userId: ${consent.userId ? `'${consent.userId}'` : 'null'},
  consentId: '${consent.consentId}',
  timestamp: '${consent.timestamp.toISOString()}',
  allowedCategories: ${JSON.stringify(categories)},
  version: '${consent.version}'
};

// Load allowed scripts
${this.generateScriptLoader(consent.categories)}
    `.trim();
  }
  
  private generateScriptLoader(categories: Record<CookieCategory, boolean>): string {
    let loader = '';
    
    if (categories[CookieCategory.ANALYTICS]) {
      loader += `
// Load Analytics
(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXX');
`;
    }
    
    if (categories[CookieCategory.MARKETING]) {
      loader += `
// Load Marketing
// Add marketing scripts here
`;
    }
    
    return loader;
  }
  
  private generateId(): string {
    return `consent_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

---

## Testing Privacy Controls

### Privacy Test Suite

```typescript
// privacy-testing.ts

export class PrivacyTestSuite {
  static testPIIDetection(data: Record<string, any>): {
    passed: boolean;
    detectedPII: string[];
  } {
    const { PIIClassifier } = require('./pii-classifier');
    const detected = PIIClassifier.detectPII(data);
    
    return {
      passed: detected.length > 0,
      detectedPII: detected.map(d => d.field)
    };
  }
  
  static testEncryption(plaintext: string, encrypted: string): {
    passed: boolean;
    message: string;
  } {
    const { DataEncryptionService } = require('./encryption-service');
    
    try {
      const service = new DataEncryptionService(process.env.ENCRYPTION_KEY || 'test-key');
      const decrypted = service.decrypt(encrypted.data, encrypted.iv, encrypted.tag);
      
      return {
        passed: decrypted === plaintext,
        message: decrypted === plaintext ? 'Encryption working correctly' : 'Decryption failed'
      };
    } catch (error) {
      return {
        passed: false,
        message: `Encryption error: ${error.message}`
      };
    }
  }
  
  static testAccessControl(
    userRole: string,
    permission: string
  ): { passed: boolean; message: string } {
    const { PrivacyAccessControl } = require('./privacy-access-control');
    
    const hasPermission = PrivacyAccessControl.hasPermission(userRole, permission);
    
    return {
      passed: true,
      message: hasPermission
        ? `User with role ${userRole} has permission ${permission}`
        : `User with role ${userRole} does not have permission ${permission}`
    };
  }
  
  static testDataMasking(
    data: Record<string, any>,
    maskingRules: Record<string, string>
  ): { passed: boolean; maskedData: Record<string, any> } {
    const { DataMaskingService } = require('./data-masking');
    const service = new DataMaskingService();
    
    const maskedData = service.maskData(data, maskingRules);
    
    return {
      passed: true,
      maskedData
    };
  }
  
  static testKAnonymity(
    data: any[],
    k: number,
    quasiIdentifiers: string[]
  ): { passed: boolean; message: string } {
    const { KAnonymityService } = require('./k-anonymity');
    const service = new KAnonymityService();
    
    const isKAnonymous = service.checkKAnonymity(data, k, quasiIdentifiers);
    
    return {
      passed: isKAnonymous,
      message: isKAnonymous
        ? `Dataset satisfies ${k}-anonymity`
        : `Dataset does not satisfy ${k}-anonymity`
    };
  }
}
```

---

## Additional Resources

- [NIST Privacy Framework](https://www.nist.gov/privacy-framework)
- [ISO 27001](https://www.iso.org/standard/27001)
- [Privacy by Design](https://www.ipc.on.ca/wp-content/uploads/Resources/7foundationalprinciples.pdf)
- [Differential Privacy](https://www.microsoft.com/en-us/research/project/differential-privacy/)

## Best Practices

### Data Minimization

- **Collect only necessary data**: Only collect data that is essential for your stated purpose
- **Use data minimization by design**: Build systems that collect minimal data by default
- **Implement data expiration**: Automatically delete data when no longer needed
- **Review data collection regularly**: Audit what data is being collected and why
- **Document data purpose**: Maintain clear records of why each data element is collected

### Consent Management

- **Obtain explicit consent**: Use clear, affirmative consent mechanisms
- **Provide granular consent options**: Allow users to choose what data to share
- **Make consent easily revocable**: Provide simple ways to withdraw consent
- **Maintain consent records**: Keep audit trail of consent grants and withdrawals
- **Use consent management platforms**: Implement proper consent lifecycle management

### Data Protection

- **Encrypt data at rest**: Use strong encryption for stored data
- **Encrypt data in transit**: Use TLS/SSL for all network communications
- **Use field-level encryption**: Encrypt sensitive fields separately
- **Implement key management**: Securely manage encryption keys
- **Regularly rotate keys**: Update encryption keys on a schedule

### Access Control

- **Implement least privilege**: Grant minimum necessary access
- **Use role-based access control**: Define roles with appropriate permissions
- **Require MFA for sensitive access**: Multi-factor authentication for high-risk operations
- **Audit access logs**: Monitor who accesses what data and when
- **Regularly review permissions**: Periodically audit and update access rights

### Data Retention

- **Define retention policies**: Specify how long different data types should be kept
- **Implement automatic deletion**: Delete data when retention period expires
- **Archive historical data**: Move old data to cheaper, slower storage
- **Document retention schedules**: Maintain clear records of retention policies
- **Comply with legal requirements**: Follow applicable laws and regulations

### Data Subject Rights

- **Provide access requests**: Allow users to request their data
- **Enable data deletion**: Implement right to be forgotten
- **Support data portability**: Allow users to export their data
- **Handle correction requests**: Allow users to correct inaccurate data
- **Respond within time limits**: Meet legal response time requirements

### Privacy by Design

- **Build privacy into products**: Consider privacy from the start of development
- **Conduct privacy impact assessments**: Evaluate privacy risks before deployment
- **Use privacy-enhancing technologies**: Implement techniques like differential privacy
- **Minimize data sharing**: Share data only when necessary
- **Provide transparency**: Be clear about data practices

### Vendor Management

- **Assess vendor privacy practices**: Evaluate third-party privacy compliance
- **Include privacy clauses in contracts**: Specify data handling requirements
- **Limit vendor access**: Share minimum necessary data with vendors
- **Monitor vendor compliance**: Audit vendor data handling
- **Have contingency plans**: Plan for vendor data breaches

### Incident Response

- **Have a breach response plan**: Document procedures for data breaches
- **Train staff on response**: Ensure team knows what to do
- **Notify affected parties**: Inform users of breaches promptly
- **Document incidents**: Keep records of all privacy incidents
- **Learn from incidents**: Update practices based on lessons learned

### Compliance

- **Understand applicable laws**: Know which regulations apply (GDPR, CCPA, etc.)
- **Conduct regular audits**: Assess compliance with privacy requirements
- **Maintain documentation**: Keep records of compliance activities
- **Stay updated on changes**: Monitor regulatory changes
- **Seek legal counsel**: Consult with privacy lawyers when needed

## Checklist

### Data Collection
- [ ] Define data collection purposes
- [ ] Implement data minimization practices
- [ ] Obtain explicit consent for collection
- [ ] Provide privacy notices
- [ ] Document data collection practices

### Data Storage
- [ ] Encrypt data at rest
- [ ] Implement secure key management
- [ ] Configure data retention policies
- [ ] Set up automatic data deletion
- [ ] Archive historical data appropriately

### Data Access
- [ ] Implement role-based access control
- [ ] Require authentication for access
- [ ] Enable MFA for sensitive operations
- [ ] Audit access logs
- [ ] Regularly review permissions

### Data Sharing
- [ ] Assess third-party privacy practices
- [ ] Include privacy clauses in contracts
- [ ] Limit data shared with vendors
- [ ] Monitor vendor compliance
- [ ] Document data sharing agreements

### Data Subject Rights
- [ ] Implement data access request process
- [ ] Enable data deletion requests
- [ ] Support data portability
- [ ] Allow data correction
- [ ] Respond within legal time limits

### Privacy by Design
- [ ] Conduct privacy impact assessments
- [ ] Implement privacy-enhancing technologies
- [ ] Build privacy into products
- [ ] Minimize data sharing
- [ ] Provide transparency to users

### Incident Response
- [ ] Create breach response plan
- [ ] Train staff on procedures
- [ ] Set up breach notification process
- [ ] Document all incidents
- [ ] Review and update procedures

### Compliance
- [ ] Identify applicable regulations
- [ ] Conduct regular compliance audits
- [ ] Maintain compliance documentation
- [ ] Monitor regulatory changes
- [ ] Consult with legal counsel

### Monitoring and Audit
- [ ] Set up data access monitoring
- [ ] Configure alerts for suspicious activity
- [ ] Conduct regular privacy audits
- [ ] Review privacy controls
- [ ] Track compliance metrics

### Documentation
- [ ] Document privacy policies
- [ ] Create data processing records
- [ ] Maintain consent records
- [ ] Document vendor agreements
- [ ] Keep incident response plans updated
