# GDPR Compliance

## Overview

Comprehensive guide to GDPR (General Data Protection Regulation) compliance patterns and implementation.

## Table of Contents

1. [GDPR Principles](#gdpr-principles)
2. [Legal Basis for Processing](#legal-basis-for-processing)
3. [Data Subject Rights](#data-subject-rights)
4. [Consent Requirements](#consent-requirements)
5. [Privacy by Design](#privacy-by-design)
6. [Data Protection Impact Assessment](#data-protection-impact-assessment)
7. [Cross-Border Transfers](#cross-border-transfers)
8. [DPO Requirements](#dpo-requirements)
9. [Implementation Patterns](#implementation-patterns)
10. [Documentation Requirements](#documentation-requirements)

---

## GDPR Principles

### Core Principles

```typescript
// gdpr-principles.ts

/**
 * GDPR Core Principles (Article 5)
 * 
 * 1. Lawfulness, Fairness, and Transparency
 * 2. Purpose Limitation
 * 3. Data Minimization
 * 4. Accuracy
 * 5. Storage Limitation
 * 6. Integrity and Confidentiality
 * 7. Accountability
 */

export interface GDPRComplianceCheck {
  principle: string;
  compliant: boolean;
  issues: string[];
  recommendations: string[];
}

export class GDPRPrinciplesChecker {
  static checkLawfulness(dataProcessing: any): GDPRComplianceCheck {
    const issues: string[] = [];
    const recommendations: string[] = [];
    
    // Check for legal basis
    if (!dataProcessing.legalBasis) {
      issues.push('No legal basis specified for data processing');
      recommendations.push('Document legal basis for all data processing activities');
    }
    
    // Check for consent
    if (dataProcessing.legalBasis === 'consent' && !dataProcessing.consentRecorded) {
      issues.push('Consent not properly recorded');
      recommendations.push('Implement proper consent tracking system');
    }
    
    return {
      principle: 'Lawfulness, Fairness, and Transparency',
      compliant: issues.length === 0,
      issues,
      recommendations
    };
  }
  
  static checkPurposeLimitation(dataProcessing: any): GDPRComplianceCheck {
    const issues: string[] = [];
    const recommendations: string[] = [];
    
    // Check if data is used beyond stated purposes
    if (dataProcessing.actualUses.length > dataProcessing.statedPurposes.length) {
      issues.push('Data used for purposes beyond stated purposes');
      recommendations.push('Review and update privacy policy to reflect all data uses');
    }
    
    return {
      principle: 'Purpose Limitation',
      compliant: issues.length === 0,
      issues,
      recommendations
    };
  }
  
  static checkDataMinimization(dataProcessing: any): GDPRComplianceCheck {
    const issues: string[] = [];
    const recommendations: string[] = [];
    
    // Check if unnecessary data is collected
    if (dataProcessing.collectedFields.length > dataProcessing.requiredFields.length) {
      const unnecessary = dataProcessing.collectedFields.filter(
        (field: string) => !dataProcessing.requiredFields.includes(field)
      );
      issues.push(`Unnecessary data collected: ${unnecessary.join(', ')}`);
      recommendations.push('Review and remove unnecessary data collection');
    }
    
    return {
      principle: 'Data Minimization',
      compliant: issues.length === 0,
      issues,
      recommendations
    };
  }
  
  static checkAccuracy(dataProcessing: any): GDPRComplianceCheck {
    const issues: string[] = [];
    const recommendations: string[] = [];
    
    // Check for data accuracy mechanisms
    if (!dataProcessing.hasDataValidation) {
      issues.push('No data validation mechanisms in place');
      recommendations.push('Implement data validation to ensure accuracy');
    }
    
    if (!dataProcessing.hasUpdateMechanism) {
      issues.push('No mechanism for users to update their data');
      recommendations.push('Implement user data update functionality');
    }
    
    return {
      principle: 'Accuracy',
      compliant: issues.length === 0,
      issues,
      recommendations
    };
  }
  
  static checkStorageLimitation(dataProcessing: any): GDPRComplianceCheck {
    const issues: string[] = [];
    const recommendations: string[] = [];
    
    // Check for retention policies
    if (!dataProcessing.hasRetentionPolicy) {
      issues.push('No data retention policy defined');
      recommendations.push('Define and implement data retention policies');
    }
    
    if (!dataProcessing.hasAutoDeletion) {
      issues.push('No automatic data deletion mechanism');
      recommendations.push('Implement automatic data deletion based on retention policies');
    }
    
    return {
      principle: 'Storage Limitation',
      compliant: issues.length === 0,
      issues,
      recommendations
    };
  }
  
  static checkIntegrityAndConfidentiality(dataProcessing: any): GDPRComplianceCheck {
    const issues: string[] = [];
    const recommendations: string[] = [];
    
    // Check for security measures
    if (!dataProcessing.encryptionAtRest) {
      issues.push('Data not encrypted at rest');
      recommendations.push('Implement encryption for data at rest');
    }
    
    if (!dataProcessing.encryptionInTransit) {
      issues.push('Data not encrypted in transit');
      recommendations.push('Use HTTPS/TLS for all data transmission');
    }
    
    if (!dataProcessing.accessControls) {
      issues.push('No access controls implemented');
      recommendations.push('Implement role-based access controls');
    }
    
    if (!dataProcessing.auditLogging) {
      issues.push('No audit logging in place');
      recommendations.push('Implement comprehensive audit logging');
    }
    
    return {
      principle: 'Integrity and Confidentiality',
      compliant: issues.length === 0,
      issues,
      recommendations
    };
  }
  
  static checkAccountability(dataProcessing: any): GDPRComplianceCheck {
    const issues: string[] = [];
    const recommendations: string[] = [];
    
    // Check for documentation
    if (!dataProcessing.hasDocumentation) {
      issues.push('No documentation of data processing activities');
      recommendations.push('Maintain records of all data processing activities');
    }
    
    if (!dataProcessing.hasDPIA && dataProcessing.highRisk) {
      issues.push('High-risk processing without Data Protection Impact Assessment');
      recommendations.push('Conduct Data Protection Impact Assessment for high-risk processing');
    }
    
    return {
      principle: 'Accountability',
      compliant: issues.length === 0,
      issues,
      recommendations
    };
  }
  
  static runFullComplianceCheck(dataProcessing: any): GDPRComplianceCheck[] {
    return [
      this.checkLawfulness(dataProcessing),
      this.checkPurposeLimitation(dataProcessing),
      this.checkDataMinimization(dataProcessing),
      this.checkAccuracy(dataProcessing),
      this.checkStorageLimitation(dataProcessing),
      this.checkIntegrityAndConfidentiality(dataProcessing),
      this.checkAccountability(dataProcessing)
    ];
  }
}
```

---

## Legal Basis for Processing

### Legal Basis Manager

```typescript
// legal-basis.ts

export enum LegalBasis {
  CONSENT = 'consent',
  CONTRACT = 'contract',
  LEGAL_OBLIGATION = 'legal_obligation',
  VITAL_INTERESTS = 'vital_interests',
  PUBLIC_TASK = 'public_task',
  LEGITIMATE_INTERESTS = 'legitimate_interests'
}

export interface LegalBasisRecord {
  id: string;
  dataType: string;
  basis: LegalBasis;
  justification: string;
  startDate: Date;
  endDate?: Date;
  documented: boolean;
}

export class LegalBasisManager {
  private records: Map<string, LegalBasisRecord[]> = new Map();
  
  recordLegalBasis(record: LegalBasisRecord): void {
    const key = record.dataType;
    if (!this.records.has(key)) {
      this.records.set(key, []);
    }
    this.records.get(key)!.push(record);
  }
  
  getLegalBasis(dataType: string): LegalBasisRecord[] {
    return this.records.get(dataType) || [];
  }
  
  isValidBasis(basis: LegalBasis, dataType: string): boolean {
    // Special handling for consent
    if (basis === LegalBasis.CONSENT) {
      return this.hasValidConsent(dataType);
    }
    
    // Special handling for legitimate interests
    if (basis === LegalBasis.LEGITIMATE_INTERESTS) {
      return this.hasLegitimateInterestAssessment(dataType);
    }
    
    return true;
  }
  
  hasValidConsent(dataType: string): boolean {
    const records = this.getLegalBasis(dataType);
    const consentRecords = records.filter(r => r.basis === LegalBasis.CONSENT);
    
    return consentRecords.some(r => 
      r.documented && 
      (!r.endDate || r.endDate > new Date())
    );
  }
  
  hasLegitimateInterestAssessment(dataType: string): boolean {
    const records = this.getLegalBasis(dataType);
    const liRecords = records.filter(r => r.basis === LegalBasis.LEGITIMATE_INTERESTS);
    
    return liRecords.some(r => r.documented && r.justification.length > 0);
  }
  
  generateLegalBasisDocumentation(): string {
    let doc = '# Legal Basis Documentation\n\n';
    
    for (const [dataType, records] of this.records.entries()) {
      doc += `## ${dataType}\n\n`;
      
      for (const record of records) {
        doc += `### ${record.basis}\n`;
        doc += `- Justification: ${record.justification}\n`;
        doc += `- Start Date: ${record.startDate.toISOString()}\n`;
        if (record.endDate) {
          doc += `- End Date: ${record.endDate.toISOString()}\n`;
        }
        doc += `- Documented: ${record.documented ? 'Yes' : 'No'}\n\n`;
      }
    }
    
    return doc;
  }
}
```

---

## Data Subject Rights

### Rights Implementation

```typescript
// data-subject-rights.ts

export enum DataSubjectRight {
  RIGHT_TO_ACCESS = 'right_to_access',
  RIGHT_TO_RECTIFICATION = 'right_to_rectification',
  RIGHT_TO_ERASURE = 'right_to_erasure',
  RIGHT_TO_RESTRICT_PROCESSING = 'right_to_restrict_processing',
  RIGHT_TO_DATA_PORTABILITY = 'right_to_data_portability',
  RIGHT_TO_OBJECT = 'right_to_object',
  RIGHT_TO_NOT_BE_SUBJECT_TO_AUTOMATED_DECISION_MAKING = 'right_to_not_be_subject_to_automated_decision_making'
}

export interface DataSubjectRequest {
  id: string;
  userId: string;
  right: DataSubjectRight;
  requestDate: Date;
  status: 'pending' | 'processing' | 'completed' | 'rejected';
  completedDate?: Date;
  rejectionReason?: string;
  metadata?: Record<string, any>;
}

export class DataSubjectRightsService {
  private requests: DataSubjectRequest[] = [];
  
  async submitAccessRequest(userId: string): Promise<DataSubjectRequest> {
    const request: DataSubjectRequest = {
      id: this.generateId(),
      userId,
      right: DataSubjectRight.RIGHT_TO_ACCESS,
      requestDate: new Date(),
      status: 'pending'
    };
    
    this.requests.push(request);
    
    // Process request
    await this.processAccessRequest(request);
    
    return request;
  }
  
  async submitErasureRequest(userId: string, reason?: string): Promise<DataSubjectRequest> {
    const request: DataSubjectRequest = {
      id: this.generateId(),
      userId,
      right: DataSubjectRight.RIGHT_TO_ERASURE,
      requestDate: new Date(),
      status: 'pending',
      metadata: { reason }
    };
    
    this.requests.push(request);
    
    // Process request
    await this.processErasureRequest(request);
    
    return request;
  }
  
  async submitRectificationRequest(
    userId: string,
    corrections: Record<string, any>
  ): Promise<DataSubjectRequest> {
    const request: DataSubjectRequest = {
      id: this.generateId(),
      userId,
      right: DataSubjectRight.RIGHT_TO_RECTIFICATION,
      requestDate: new Date(),
      status: 'pending',
      metadata: { corrections }
    };
    
    this.requests.push(request);
    
    // Process request
    await this.processRectificationRequest(request);
    
    return request;
  }
  
  async submitPortabilityRequest(userId: string): Promise<DataSubjectRequest> {
    const request: DataSubjectRequest = {
      id: this.generateId(),
      userId,
      right: DataSubjectRight.RIGHT_TO_DATA_PORTABILITY,
      requestDate: new Date(),
      status: 'pending'
    };
    
    this.requests.push(request);
    
    // Process request
    await this.processPortabilityRequest(request);
    
    return request;
  }
  
  async submitObjectionRequest(userId: string, reason: string): Promise<DataSubjectRequest> {
    const request: DataSubjectRequest = {
      id: this.generateId(),
      userId,
      right: DataSubjectRight.RIGHT_TO_OBJECT,
      requestDate: new Date(),
      status: 'pending',
      metadata: { reason }
    };
    
    this.requests.push(request);
    
    // Process request
    await this.processObjectionRequest(request);
    
    return request;
  }
  
  private async processAccessRequest(request: DataSubjectRequest): Promise<void> {
    request.status = 'processing';
    
    // Gather all user data
    const userData = await this.gatherUserData(request.userId);
    
    // Generate report
    const report = this.generateAccessReport(userData);
    
    // Send to user
    await this.sendReport(request.userId, report);
    
    request.status = 'completed';
    request.completedDate = new Date();
  }
  
  private async processErasureRequest(request: DataSubjectRequest): Promise<void> {
    request.status = 'processing';
    
    // Check if erasure is allowed
    const canErase = await this.canEraseData(request.userId);
    
    if (!canErase) {
      request.status = 'rejected';
      request.rejectionReason = 'Data cannot be erased due to legal obligations';
      return;
    }
    
    // Erase data
    await this.eraseUserData(request.userId);
    
    request.status = 'completed';
    request.completedDate = new Date();
  }
  
  private async processRectificationRequest(request: DataSubjectRequest): Promise<void> {
    request.status = 'processing';
    
    // Apply corrections
    const corrections = request.metadata?.corrections;
    await this.applyCorrections(request.userId, corrections);
    
    request.status = 'completed';
    request.completedDate = new Date();
  }
  
  private async processPortabilityRequest(request: DataSubjectRequest): Promise<void> {
    request.status = 'processing';
    
    // Gather data
    const userData = await this.gatherUserData(request.userId);
    
    // Export in machine-readable format
    const exportData = this.exportUserData(userData);
    
    // Send to user
    await this.sendExport(request.userId, exportData);
    
    request.status = 'completed';
    request.completedDate = new Date();
  }
  
  private async processObjectionRequest(request: DataSubjectRequest): Promise<void> {
    request.status = 'processing';
    
    // Process objection
    await this.handleObjection(request.userId, request.metadata?.reason);
    
    request.status = 'completed';
    request.completedDate = new Date();
  }
  
  private async gatherUserData(userId: string): Promise<any> {
    // Implementation to gather all user data
    return {
      userId,
      personalData: {},
      accountData: {},
      activityData: {}
    };
  }
  
  private generateAccessReport(userData: any): string {
    return JSON.stringify(userData, null, 2);
  }
  
  private async sendReport(userId: string, report: string): Promise<void> {
    // Implementation to send report to user
  }
  
  private async canEraseData(userId: string): Promise<boolean> {
    // Check if data can be erased (legal obligations, etc.)
    return true;
  }
  
  private async eraseUserData(userId: string): Promise<void> {
    // Implementation to erase user data
  }
  
  private async applyCorrections(userId: string, corrections: any): Promise<void> {
    // Implementation to apply corrections
  }
  
  private exportUserData(userData: any): any {
    // Export in machine-readable format (JSON, XML, etc.)
    return userData;
  }
  
  private async sendExport(userId: string, exportData: any): Promise<void> {
    // Implementation to send export to user
  }
  
  private async handleObjection(userId: string, reason: string): Promise<void> {
    // Implementation to handle objection
  }
  
  private generateId(): string {
    return `req_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

---

## Consent Requirements

### Consent Management

```typescript
// gdpr-consent.ts

export interface ConsentRecord {
  id: string;
  userId: string;
  purpose: string;
  consentGiven: boolean;
  consentDate: Date;
  withdrawnDate?: Date;
  version: number;
  ipAddress?: string;
  userAgent?: string;
}

export class GDPRConsentManager {
  private consents: Map<string, ConsentRecord[]> = new Map();
  
  recordConsent(
    userId: string,
    purpose: string,
    ipAddress?: string,
    userAgent?: string
  ): ConsentRecord {
    const record: ConsentRecord = {
      id: this.generateId(),
      userId,
      purpose,
      consentGiven: true,
      consentDate: new Date(),
      version: this.getNextVersion(userId, purpose),
      ipAddress,
      userAgent
    };
    
    const key = `${userId}:${purpose}`;
    if (!this.consents.has(key)) {
      this.consents.set(key, []);
    }
    this.consents.get(key)!.push(record);
    
    return record;
  }
  
  withdrawConsent(userId: string, purpose: string): ConsentRecord | null {
    const key = `${userId}:${purpose}`;
    const records = this.consents.get(key);
    
    if (!records || records.length === 0) return null;
    
    const latestRecord = records[records.length - 1];
    
    if (latestRecord.consentGiven) {
      latestRecord.withdrawnDate = new Date();
      latestRecord.consentGiven = false;
    }
    
    return latestRecord;
  }
  
  hasConsent(userId: string, purpose: string): boolean {
    const key = `${userId}:${purpose}`;
    const records = this.consents.get(key);
    
    if (!records || records.length === 0) return false;
    
    const latestRecord = records[records.length - 1];
    return latestRecord.consentGiven && !latestRecord.withdrawnDate;
  }
  
  getConsentHistory(userId: string, purpose: string): ConsentRecord[] {
    const key = `${userId}:${purpose}`;
    return this.consents.get(key) || [];
  }
  
  getAllConsents(userId: string): ConsentRecord[] {
    const allConsents: ConsentRecord[] = [];
    
    for (const [key, records] of this.consents.entries()) {
      if (key.startsWith(`${userId}:`)) {
        allConsents.push(...records);
      }
    }
    
    return allConsents;
  }
  
  private getNextVersion(userId: string, purpose: string): number {
    const key = `${userId}:${purpose}`;
    const records = this.consents.get(key);
    return records ? records.length + 1 : 1;
  }
  
  private generateId(): string {
    return `consent_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

---

## Privacy by Design

### Privacy by Design Implementation

```typescript
// privacy-by-design.ts

export interface PrivacyAssessment {
  component: string;
  privacyRisks: string[];
  mitigations: string[];
  compliant: boolean;
}

export class PrivacyByDesignChecker {
  static assessComponent(component: any): PrivacyAssessment {
    const risks: string[] = [];
    const mitigations: string[] = [];
    
    // Check for data minimization
    if (component.collectsUnnecessaryData) {
      risks.push('Collects unnecessary data');
      mitigations.push('Remove unnecessary data collection');
    }
    
    // Check for encryption
    if (!component.usesEncryption) {
      risks.push('Data not encrypted');
      mitigations.push('Implement encryption');
    }
    
    // Check for access controls
    if (!component.hasAccessControls) {
      risks.push('No access controls');
      mitigations.push('Implement role-based access controls');
    }
    
    // Check for anonymization
    if (!component.anonymizesData) {
      risks.push('Data not anonymized when possible');
      mitigations.push('Implement data anonymization');
    }
    
    return {
      component: component.name,
      privacyRisks: risks,
      mitigations,
      compliant: risks.length === 0
    };
  }
  
  static assessSystem(components: any[]): PrivacyAssessment[] {
    return components.map(component => this.assessComponent(component));
  }
  
  static generatePrivacyReport(assessments: PrivacyAssessment[]): string {
    let report = '# Privacy by Design Assessment Report\n\n';
    
    const compliantCount = assessments.filter(a => a.compliant).length;
    const totalCount = assessments.length;
    
    report += `## Summary\n`;
    report += `- Total Components: ${totalCount}\n`;
    report += `- Compliant: ${compliantCount}\n`;
    report += `- Non-Compliant: ${totalCount - compliantCount}\n\n`;
    
    report += `## Detailed Assessment\n\n`;
    
    for (const assessment of assessments) {
      report += `### ${assessment.component}\n`;
      report += `Status: ${assessment.compliant ? '✓ Compliant' : '✗ Non-Compliant'}\n\n`;
      
      if (assessment.privacyRisks.length > 0) {
        report += `**Risks:**\n`;
        for (const risk of assessment.privacyRisks) {
          report += `- ${risk}\n`;
        }
        report += '\n';
      }
      
      if (assessment.mitigations.length > 0) {
        report += `**Mitigations:**\n`;
        for (const mitigation of assessment.mitigations) {
          report += `- ${mitigation}\n`;
        }
        report += '\n';
      }
    }
    
    return report;
  }
}
```

---

## Data Protection Impact Assessment

### DPIA Implementation

```typescript
// dpia.ts

export interface DPIA {
  id: string;
  projectName: string;
  description: string;
  dataTypes: string[];
  dataSubjects: string[];
  purposes: string[];
  risks: Risk[];
  mitigations: Mitigation[];
  assessmentDate: Date;
  assessor: string;
  approved: boolean;
  approvalDate?: Date;
  approver?: string;
}

export interface Risk {
  id: string;
  description: string;
  likelihood: 'low' | 'medium' | 'high';
  impact: 'low' | 'medium' | 'high';
  severity: 'low' | 'medium' | 'high';
}

export interface Mitigation {
  riskId: string;
  description: string;
  effectiveness: 'low' | 'medium' | 'high';
  implemented: boolean;
}

export class DPIAService {
  private dpias: Map<string, DPIA> = new Map();
  
  createDPIA(dpia: Omit<DPIA, 'id' | 'assessmentDate'>): DPIA {
    const newDPIA: DPIA = {
      id: this.generateId(),
      ...dpia,
      assessmentDate: new Date()
    };
    
    this.dpias.set(newDPIA.id, newDPIA);
    
    return newDPIA;
  }
  
  getDPIA(id: string): DPIA | undefined {
    return this.dpias.get(id);
  }
  
  updateDPIA(id: string, updates: Partial<DPIA>): DPIA | undefined {
    const dpia = this.dpias.get(id);
    if (!dpia) return undefined;
    
    const updated = { ...dpia, ...updates };
    this.dpias.set(id, updated);
    
    return updated;
  }
  
  approveDPIA(id: string, approver: string): DPIA | undefined {
    const dpia = this.dpias.get(id);
    if (!dpia) return undefined;
    
    dpia.approved = true;
    dpia.approvalDate = new Date();
    dpia.approver = approver;
    
    return dpia;
  }
  
  calculateRiskScore(risk: Risk): number {
    const likelihoodScore = { low: 1, medium: 2, high: 3 };
    const impactScore = { low: 1, medium: 2, high: 3 };
    
    const score = likelihoodScore[risk.likelihood] * impactScore[risk.impact];
    
    if (score >= 6) return 3; // High
    if (score >= 3) return 2; // Medium
    return 1; // Low
  }
  
  assessOverallRisk(dpia: DPIA): 'low' | 'medium' | 'high' {
    const riskScores = dpia.risks.map(r => this.calculateRiskScore(r));
    const averageScore = riskScores.reduce((a, b) => a + b, 0) / riskScores.length;
    
    if (averageScore >= 2.5) return 'high';
    if (averageScore >= 1.5) return 'medium';
    return 'low';
  }
  
  generateDPIAReport(dpia: DPIA): string {
    let report = '# Data Protection Impact Assessment\n\n';
    
    report += `## Project Information\n`;
    report += `- Project Name: ${dpia.projectName}\n`;
    report += `- Description: ${dpia.description}\n`;
    report += `- Assessment Date: ${dpia.assessmentDate.toISOString()}\n`;
    report += `- Assessor: ${dpia.assessor}\n\n`;
    
    report += `## Data Types\n`;
    for (const dataType of dpia.dataTypes) {
      report += `- ${dataType}\n`;
    }
    report += '\n';
    
    report += `## Data Subjects\n`;
    for (const subject of dpia.dataSubjects) {
      report += `- ${subject}\n`;
    }
    report += '\n';
    
    report += `## Purposes\n`;
    for (const purpose of dpia.purposes) {
      report += `- ${purpose}\n`;
    }
    report += '\n';
    
    report += `## Risk Assessment\n\n`;
    for (const risk of dpia.risks) {
      report += `### ${risk.description}\n`;
      report += `- Likelihood: ${risk.likelihood}\n`;
      report += `- Impact: ${risk.impact}\n`;
      report += `- Severity: ${risk.severity}\n\n`;
    }
    
    report += `## Mitigations\n\n`;
    for (const mitigation of dpia.mitigations) {
      const risk = dpia.risks.find(r => r.id === mitigation.riskId);
      report += `### ${risk?.description}\n`;
      report += `- Mitigation: ${mitigation.description}\n`;
      report += `- Effectiveness: ${mitigation.effectiveness}\n`;
      report += `- Implemented: ${mitigation.implemented ? 'Yes' : 'No'}\n\n`;
    }
    
    const overallRisk = this.assessOverallRisk(dpia);
    report += `## Overall Risk Assessment\n`;
    report += `Overall Risk Level: ${overallRisk.toUpperCase()}\n\n`;
    
    report += `## Approval\n`;
    report += `- Approved: ${dpia.approved ? 'Yes' : 'No'}\n`;
    if (dpia.approved) {
      report += `- Approval Date: ${dpia.approvalDate?.toISOString()}\n`;
      report += `- Approver: ${dpia.approver}\n`;
    }
    
    return report;
  }
  
  private generateId(): string {
    return `dpia_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

---

## Cross-Border Transfers

### Transfer Mechanisms

```typescript
// cross-border-transfers.ts

export enum TransferMechanism {
  ADEQUACY_DECISION = 'adequacy_decision',
  STANDARD_CONTRACTUAL_CLAUSES = 'standard_contractual_clauses',
  BINDING_CORPORATE_RULES = 'binding_corporate_rules',
  CODE_OF_CONDUCT = 'code_of_conduct',
  CERTIFICATION = 'certification',
  DEROGATIONS = 'derogations'
}

export interface TransferRecord {
  id: string;
  dataType: string;
  fromCountry: string;
  toCountry: string;
  mechanism: TransferMechanism;
  date: Date;
  documented: boolean;
}

export class CrossBorderTransferService {
  private transfers: TransferRecord[] = [];
  
  isAdequateCountry(country: string): boolean {
    // List of countries with adequacy decisions
    const adequateCountries = [
      'Andorra', 'Argentina', 'Canada (commercial organizations)',
      'Faroe Islands', 'Guernsey', 'Israel', 'Isle of Man',
      'Japan', 'Jersey', 'New Zealand', 'Republic of Korea',
      'Switzerland', 'United Kingdom', 'Uruguay', 'United States (limited)'
    ];
    
    return adequateCountries.some(c => c.toLowerCase().includes(country.toLowerCase()));
  }
  
  recordTransfer(
    dataType: string,
    fromCountry: string,
    toCountry: string,
    mechanism: TransferMechanism
  ): TransferRecord {
    const record: TransferRecord = {
      id: this.generateId(),
      dataType,
      fromCountry,
      toCountry,
      mechanism,
      date: new Date(),
      documented: true
    };
    
    this.transfers.push(record);
    
    return record;
  }
  
  getTransferMechanism(toCountry: string): TransferMechanism {
    if (this.isAdequateCountry(toCountry)) {
      return TransferMechanism.ADEQUACY_DECISION;
    }
    
    // Default to SCCs
    return TransferMechanism.STANDARD_CONTRACTUAL_CLAUSES;
  }
  
  validateTransfer(
    dataType: string,
    toCountry: string,
    mechanism: TransferMechanism
  ): boolean {
    if (this.isAdequateCountry(toCountry)) {
      return true;
    }
    
    // Check if appropriate mechanism is used
    if (mechanism === TransferMechanism.ADEQUACY_DECISION) {
      return false;
    }
    
    return true;
  }
  
  generateTransferDocumentation(): string {
    let doc = '# Cross-Border Data Transfer Documentation\n\n';
    
    for (const transfer of this.transfers) {
      doc += `## Transfer ${transfer.id}\n`;
      doc += `- Data Type: ${transfer.dataType}\n`;
      doc += `- From: ${transfer.fromCountry}\n`;
      doc += `- To: ${transfer.toCountry}\n`;
      doc += `- Mechanism: ${transfer.mechanism}\n`;
      doc += `- Date: ${transfer.date.toISOString()}\n`;
      doc += `- Documented: ${transfer.documented ? 'Yes' : 'No'}\n\n`;
    }
    
    return doc;
  }
  
  private generateId(): string {
    return `transfer_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

---

## DPO Requirements

### DPO Service

```typescript
// dpo-service.ts

export interface DPOContact {
  name: string;
  email: string;
  phone?: string;
  address?: string;
}

export interface DPORecord {
  id: string;
  organizationId: string;
  contact: DPOContact;
  appointmentDate: Date;
  responsibilities: string[];
}

export class DPOService {
  private dpos: Map<string, DPORecord> = new Map();
  
  appointDPO(organizationId: string, contact: DPOContact): DPORecord {
    const record: DPORecord = {
      id: this.generateId(),
      organizationId,
      contact,
      appointmentDate: new Date(),
      responsibilities: [
        'Inform and advise the organization about data protection obligations',
        'Monitor compliance with GDPR',
        'Provide advice on data protection impact assessments',
        'Cooperate with supervisory authorities',
        'Act as contact point for supervisory authorities'
      ]
    };
    
    this.dpos.set(organizationId, record);
    
    return record;
  }
  
  getDPO(organizationId: string): DPORecord | undefined {
    return this.dpos.get(organizationId);
  }
  
  updateDPOContact(
    organizationId: string,
    contact: Partial<DPOContact>
  ): DPORecord | undefined {
    const record = this.dpos.get(organizationId);
    if (!record) return undefined;
    
    record.contact = { ...record.contact, ...contact };
    
    return record;
  }
  
  generateDPOContactInfo(organizationId: string): string {
    const dpo = this.getDPO(organizationId);
    if (!dpo) return 'No DPO appointed';
    
    return `
# Data Protection Officer Contact Information

**Name:** ${dpo.contact.name}
**Email:** ${dpo.contact.email}
${dpo.contact.phone ? `**Phone:** ${dpo.contact.phone}` : ''}
${dpo.contact.address ? `**Address:** ${dpo.contact.address}` : ''}

## Responsibilities
${dpo.responsibilities.map(r => `- ${r}`).join('\n')}
    `.trim();
  }
  
  private generateId(): string {
    return `dpo_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
```

---

## Implementation Patterns

### GDPR Implementation Checklist

```typescript
// gdpr-implementation.ts

export interface GDPRImplementationChecklist {
  category: string;
  items: Array<{
    description: string;
    implemented: boolean;
    notes?: string;
  }>;
}

export class GDPRImplementationChecker {
  static getChecklist(): GDPRImplementationChecklist[] {
    return [
      {
        category: 'Legal Basis',
        items: [
          { description: 'Document legal basis for all data processing', implemented: false },
          { description: 'Implement consent management system', implemented: false },
          { description: 'Create records of processing activities', implemented: false }
        ]
      },
      {
        category: 'Data Subject Rights',
        items: [
          { description: 'Implement right to access (SAR)', implemented: false },
          { description: 'Implement right to erasure', implemented: false },
          { description: 'Implement right to rectification', implemented: false },
          { description: 'Implement right to data portability', implemented: false },
          { description: 'Implement right to object', implemented: false }
        ]
      },
      {
        category: 'Data Security',
        items: [
          { description: 'Implement encryption at rest', implemented: false },
          { description: 'Implement encryption in transit', implemented: false },
          { description: 'Implement access controls', implemented: false },
          { description: 'Implement audit logging', implemented: false },
          { description: 'Conduct regular security assessments', implemented: false }
        ]
      },
      {
        category: 'Data Breach Management',
        items: [
          { description: 'Implement breach detection system', implemented: false },
          { description: 'Create breach notification procedures', implemented: false },
          { description: 'Document breach response plan', implemented: false }
        ]
      },
      {
        category: 'Documentation',
        items: [
          { description: 'Maintain records of processing activities', implemented: false },
          { description: 'Document privacy policies', implemented: false },
          { description: 'Document cookie policy', implemented: false },
          { description: 'Document data retention policies', implemented: false }
        ]
      },
      {
        category: 'Training',
        items: [
          { description: 'Provide GDPR training to employees', implemented: false },
          { description: 'Document training records', implemented: false }
        ]
      }
    ];
  }
  
  static calculateComplianceScore(checklist: GDPRImplementationChecklist[]): number {
    let total = 0;
    let implemented = 0;
    
    for (const category of checklist) {
      for (const item of category.items) {
        total++;
        if (item.implemented) implemented++;
      }
    }
    
    return total > 0 ? (implemented / total) * 100 : 0;
  }
}
```

---

## Documentation Requirements

### Documentation Generator

```typescript
// gdpr-documentation.ts

export class GDPRDocumentationGenerator {
  static generateRecordsOfProcessingActivities(processing: any[]): string {
    let doc = '# Records of Processing Activities (Article 30)\n\n';
    
    for (const activity of processing) {
      doc += `## Processing Activity\n`;
      doc += `- Data Controller: ${activity.controller}\n`;
      doc += `- Data Processor: ${activity.processor || 'N/A'}\n`;
      doc += `- Purposes: ${activity.purposes.join(', ')}\n`;
      doc += `- Categories of Data Subjects: ${activity.dataSubjects.join(', ')}\n`;
      doc += `- Categories of Personal Data: ${activity.dataTypes.join(', ')}\n`;
      doc += `- Recipients: ${activity.recipients.join(', ')}\n`;
      doc += `- Transfers to Third Countries: ${activity.transfers || 'None'}\n`;
      doc += `- Retention Period: ${activity.retentionPeriod}\n`;
      doc += `- Security Measures: ${activity.securityMeasures.join(', ')}\n\n`;
    }
    
    return doc;
  }
  
  static generatePrivacyPolicy(organization: any): string {
    let doc = '# Privacy Policy\n\n';
    
    doc += `## ${organization.name}\n\n`;
    doc += `### Introduction\n`;
    doc += `${organization.introduction}\n\n`;
    
    doc += `### Data Controller\n`;
    doc += `- Name: ${organization.name}\n`;
    doc += `- Address: ${organization.address}\n`;
    doc += `- Email: ${organization.email}\n`;
    doc += `- Phone: ${organization.phone}\n\n`;
    
    doc += `### Data We Collect\n`;
    for (const dataType of organization.dataTypes) {
      doc += `- ${dataType.description}: ${dataType.purpose}\n`;
    }
    doc += '\n';
    
    doc += `### Legal Basis for Processing\n`;
    for (const basis of organization.legalBases) {
      doc += `- ${basis.dataType}: ${basis.basis} - ${basis.justification}\n`;
    }
    doc += '\n';
    
    doc += `### Your Rights\n`;
    for (const right of organization.rights) {
      doc += `- ${right.name}: ${right.description}\n`;
    }
    doc += '\n';
    
    doc += `### Data Retention\n`;
    doc += `${organization.retentionPolicy}\n\n`;
    
    doc += `### Data Security\n`;
    doc += `${organization.securityPolicy}\n\n`;
    
    doc += `### International Transfers\n`;
    doc += `${organization.transferPolicy}\n\n`;
    
    doc += `### Changes to This Policy\n`;
    doc += `${organization.changePolicy}\n\n`;
    
    doc += `### Contact Us\n`;
    doc += `- Email: ${organization.email}\n`;
    doc += `- Phone: ${organization.phone}\n`;
    
    return doc;
  }
  
  static generateCookiePolicy(organization: any): string {
    let doc = '# Cookie Policy\n\n';
    
    doc += `## ${organization.name}\n\n`;
    doc += `### What Are Cookies\n`;
    doc += `${organization.cookieExplanation}\n\n`;
    
    doc += `### Types of Cookies We Use\n`;
    for (const cookie of organization.cookies) {
      doc += `- ${cookie.name}: ${cookie.description}\n`;
      doc += `  - Type: ${cookie.type}\n`;
      doc += `  - Duration: ${cookie.duration}\n`;
    }
    doc += '\n';
    
    doc += `### Managing Cookies\n`;
    doc += `${organization.cookieManagement}\n\n`;
    
    doc += `### Updates to This Policy\n`;
    doc += `${organization.cookiePolicyUpdates}\n`;
    
    return doc;
  }
}
```

---

## Additional Resources

- [GDPR Official Text](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32016R0679)
- [UK ICO GDPR Guide](https://ico.org.uk/for-organisations/guide-to-data-protection/guide-to-the-general-data-protection-regulation-gdpr/)
- [EDPB Guidelines](https://edpb.europa.eu/guidelines)
- [GDPR Compliance Checklist](https://gdpr.eu/checklist/)
