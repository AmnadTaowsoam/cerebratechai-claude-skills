# API Key Management

## Overview

Comprehensive guide to API key management patterns for web applications.

## Table of Contents

1. [API Key Generation](#api-key-generation)
2. [Secure Storage (Hashing)](#secure-storage-hashing)
3. [Key Rotation](#key-rotation)
4. [Multiple Keys Per User](#multiple-keys-per-user)
5. [Key Scopes/Permissions](#key-scopespermissions)
6. [Rate Limiting Per Key](#rate-limiting-per-key)
7. [Key Revocation](#key-revocation)
8. [Usage Tracking](#usage-tracking)
9. [Middleware Implementation](#middleware-implementation)
10. [Best Practices](#best-practices)
11. [Security Considerations](#security-considerations)

---

## API Key Generation

### Key Generation

```typescript
// api-key-generator.ts
import crypto from 'crypto';

export class APIKeyGenerator {
  private static readonly KEY_PREFIX = 'sk_';
  private static readonly KEY_LENGTH = 32;
  
  static generateKey(): string {
    // Generate random bytes
    const randomBytes = crypto.randomBytes(this.KEY_LENGTH);
    
    // Convert to hex
    const hexKey = randomBytes.toString('hex');
    
    // Add prefix
    return `${this.KEY_PREFIX}${hexKey}`;
  }
  
  static generateKeyWithVersion(version: number): string {
    const randomBytes = crypto.randomBytes(this.KEY_LENGTH);
    const hexKey = randomBytes.toString('hex');
    
    return `${this.KEY_PREFIX}v${version}_${hexKey}`;
  }
  
  static generateKeyWithPrefix(customPrefix: string): string {
    const randomBytes = crypto.randomBytes(this.KEY_LENGTH);
    const hexKey = randomBytes.toString('hex');
    
    return `${customPrefix}${hexKey}`;
  }
}

// Usage
const apiKey = APIKeyGenerator.generateKey();
console.log(apiKey); // sk_abc123def456...
```

### Python Implementation

```python
# api_key_generator.py
import secrets
import string
from typing import Optional

class APIKeyGenerator:
    KEY_PREFIX = 'sk_'
    KEY_LENGTH = 32
    CHARACTERS = string.ascii_letters + string.digits + string.hexdigits.lower()
    
    @classmethod
    def generate_key(cls) -> str:
        """Generate API key"""
        random_bytes = secrets.token_bytes(cls.KEY_LENGTH)
        hex_key = random_bytes.hex()
        return f"{cls.KEY_PREFIX}{hex_key}"
    
    @classmethod
    def generate_key_with_version(cls, version: int) -> str:
        """Generate API key with version"""
        random_bytes = secrets.token_bytes(cls.KEY_LENGTH)
        hex_key = random_bytes.hex()
        return f"{cls.KEY_PREFIX}v{version}_{hex_key}"
    
    @classmethod
    def generate_key_with_prefix(cls, custom_prefix: str) -> str:
        """Generate API key with custom prefix"""
        random_bytes = secrets.token_bytes(cls.KEY_LENGTH)
        hex_key = random_bytes.hex()
        return f"{custom_prefix}{hex_key}"

# Usage
api_key = APIKeyGenerator.generate_key()
print(api_key)  # sk_abc123def456...
```

---

## Secure Storage (Hashing)

### Key Hashing

```typescript
// api-key-storage.ts
import bcrypt from 'bcryptjs';
import crypto from 'crypto';

export class APIKeyStorage {
  private static readonly SALT_ROUNDS = 10;
  
  static async hashKey(apiKey: string): Promise<string> {
    // Extract key without prefix
    const keyWithoutPrefix = this.extractKey(apiKey);
    
    // Hash with bcrypt
    const salt = await bcrypt.genSalt(this.SALT_ROUNDS);
    const hash = await bcrypt.hash(keyWithoutPrefix, salt);
    
    return hash;
  }
  
  static async verifyKey(apiKey: string, hash: string): Promise<boolean> {
    const keyWithoutPrefix = this.extractKey(apiKey);
    return await bcrypt.compare(keyWithoutPrefix, hash);
  }
  
  static hashKeyWithSHA256(apiKey: string): string {
    const keyWithoutPrefix = this.extractKey(apiKey);
    return crypto
      .createHash('sha256')
      .update(keyWithoutPrefix)
      .digest('hex');
  }
  
  static verifyKeyWithSHA256(apiKey: string, hash: string): boolean {
    const keyWithoutPrefix = this.extractKey(apiKey);
    const computedHash = crypto
      .createHash('sha256')
      .update(keyWithoutPrefix)
      .digest('hex');
    
    return computedHash === hash;
  }
  
  private static extractKey(apiKey: string): string {
    // Remove prefix (e.g., sk_)
    const parts = apiKey.split('_');
    return parts.length > 1 ? parts.slice(1).join('_') : apiKey;
  }
}

// Usage
const apiKey = APIKeyGenerator.generateKey();
const hash = await APIKeyStorage.hashKey(apiKey);
const isValid = await APIKeyStorage.verifyKey(apiKey, hash);
```

---

## Key Rotation

### Key Rotation Strategy

```typescript
// key-rotation.ts
export class KeyRotationService {
  constructor(
    private apiKeyRepository: APIKeyRepository,
    private keyGenerator: APIKeyGenerator
  ) {}
  
  async rotateKey(userId: string, oldKeyId: string): Promise<string> {
    // Generate new key
    const newApiKey = this.keyGenerator.generateKey();
    const newHash = await APIKeyStorage.hashKey(newApiKey);
    
    // Update database
    await this.apiKeyRepository.update(oldKeyId, {
      keyHash: newHash,
      lastRotatedAt: new Date(),
      isActive: true
    });
    
    // Deactivate old key after grace period
    setTimeout(async () => {
      await this.apiKeyRepository.deactivate(oldKeyId);
    }, 5 * 60 * 1000); // 5 minutes
    
    return newApiKey;
  }
  
  async rotateAllKeysForUser(userId: string): Promise<void> {
    const keys = await this.apiKeyRepository.findByUserId(userId);
    
    for (const key of keys) {
      await this.rotateKey(userId, key.id);
    }
  }
  
  async scheduleRotation(userId: string, keyId: string): Promise<void> {
    // Schedule rotation (e.g., every 90 days)
    const rotationDate = new Date();
    rotationDate.setDate(rotationDate.getDate() + 90);
    
    await this.apiKeyRepository.update(keyId, {
      scheduledRotationAt: rotationDate
    });
  }
}

// Cron job for automatic rotation
// rotation-cron.ts
import cron from 'node-cron';

export class KeyRotationScheduler {
  constructor(private rotationService: KeyRotationService) {}
  
  start(): void {
    // Check for keys that need rotation daily
    cron.schedule('0 2 * * *', async () => {
      await this.checkAndRotateKeys();
    });
  }
  
  private async checkAndRotateKeys(): Promise<void> {
    const keysNeedingRotation = await this.apiKeyRepository.findKeysNeedingRotation();
    
    for (const key of keysNeedingRotation) {
      await this.rotationService.rotateKey(key.userId, key.id);
    }
  }
}
```

---

## Multiple Keys Per User

### Multi-Key Management

```typescript
// multi-key-manager.ts
export interface APIKey {
  id: string;
  userId: string;
  name: string;
  keyHash: string;
  keyPrefix: string;
  scopes: string[];
  isActive: boolean;
  expiresAt?: Date;
  lastUsedAt?: Date;
  createdAt: Date;
}

export class MultiKeyManager {
  constructor(private apiKeyRepository: APIKeyRepository) {}
  
  async createKey(
    userId: string,
    name: string,
    scopes: string[],
    expiresAt?: Date
  ): Promise<{ apiKey: string; keyId: string }> {
    // Generate key
    const apiKey = APIKeyGenerator.generateKey();
    const keyHash = await APIKeyStorage.hashKey(apiKey);
    const keyPrefix = apiKey.substring(0, 3); // sk_
    
    // Store in database
    const keyRecord = await this.apiKeyRepository.create({
      userId,
      name,
      keyHash,
      keyPrefix,
      scopes,
      isActive: true,
      expiresAt,
      createdAt: new Date()
    });
    
    return {
      apiKey,
      keyId: keyRecord.id
    };
  }
  
  async listKeysForUser(userId: string): Promise<APIKey[]> {
    return await this.apiKeyRepository.findByUserId(userId);
  }
  
  async revokeKey(userId: string, keyId: string): Promise<void> {
    const key = await this.apiKeyRepository.findById(keyId);
    
    if (!key || key.userId !== userId) {
      throw new Error('Key not found or access denied');
    }
    
    await this.apiKeyRepository.update(keyId, {
      isActive: false,
      revokedAt: new Date()
    });
  }
  
  async deleteKey(userId: string, keyId: string): Promise<void> {
    const key = await this.apiKeyRepository.findById(keyId);
    
    if (!key || key.userId !== userId) {
      throw new Error('Key not found or access denied');
    }
    
    await this.apiKeyRepository.delete(keyId);
  }
}
```

---

## Key Scopes/Permissions

### Scope Management

```typescript
// scope-manager.ts
export interface Scope {
  name: string;
  description: string;
  permissions: string[];
}

export const API_SCOPES: Record<string, Scope> = {
  read: {
    name: 'read',
    description: 'Read access',
    permissions: ['users:read', 'posts:read']
  },
  write: {
    name: 'write',
    description: 'Write access',
    permissions: ['users:write', 'posts:write']
  },
  admin: {
    name: 'admin',
    description: 'Admin access',
    permissions: ['*'] // All permissions
  },
  billing: {
    name: 'billing',
    description: 'Billing access',
    permissions: ['billing:read', 'billing:write']
  }
};

export class ScopeManager {
  static validateScopes(requestedScopes: string[]): string[] {
    const validScopes: string[] = [];
    
    for (const scope of requestedScopes) {
      if (API_SCOPES[scope]) {
        validScopes.push(scope);
      }
    }
    
    return validScopes;
  }
  
  static checkPermission(keyScopes: string[], requiredPermission: string): boolean {
    // Check if key has admin scope (all permissions)
    if (keyScopes.includes('admin')) {
      return true;
    }
    
    // Check specific permissions
    for (const scope of keyScopes) {
      const scopeConfig = API_SCOPES[scope];
      if (scopeConfig && scopeConfig.permissions.includes(requiredPermission)) {
        return true;
      }
    }
    
    return false;
  }
  
  static getPermissionsFromScopes(scopes: string[]): string[] {
    const permissions: string[] = [];
    
    for (const scope of scopes) {
      const scopeConfig = API_SCOPES[scope];
      if (scopeConfig) {
        if (scopeConfig.permissions.includes('*')) {
          return ['*'];
        }
        permissions.push(...scopeConfig.permissions);
      }
    }
    
    return [...new Set(permissions)];
  }
}
```

---

## Rate Limiting Per Key

### Rate Limiting

```typescript
// api-key-rate-limit.ts
import { RateLimiter } from 'rate-limiter-flexible';

export class APIKeyRateLimiter {
  private limiters: Map<string, RateLimiter> = new Map();
  
  constructor() {}
  
  getLimiter(apiKeyId: string, scopes: string[]): RateLimiter {
    const limiterKey = `${apiKeyId}:${scopes.join(',')}`;
    
    if (!this.limiters.has(limiterKey)) {
      // Determine rate limit based on scopes
      const rateLimit = this.getRateLimitForScopes(scopes);
      
      const limiter = new RateLimiter({
        points: rateLimit.points,
        duration: rateLimit.duration, // seconds
      });
      
      this.limiters.set(limiterKey, limiter);
    }
    
    return this.limiters.get(limiterKey)!;
  }
  
  private getRateLimitForScopes(scopes: string[]): { points: number; duration: number } {
    // Admin keys have higher limits
    if (scopes.includes('admin')) {
      return { points: 10000, duration: 60 }; // 10000 requests per minute
    }
    
    // Billing keys have higher limits
    if (scopes.includes('billing')) {
      return { points: 5000, duration: 60 }; // 5000 requests per minute
    }
    
    // Default limits
    return { points: 1000, duration: 60 }; // 1000 requests per minute
  }
  
  async checkRateLimit(apiKeyId: string, scopes: string[]): Promise<boolean> {
    const limiter = this.getLimiter(apiKeyId, scopes);
    
    try {
      await limiter.consume(1);
      return true;
    } catch (error) {
      return false;
    }
  }
}

// Express middleware
import { Request, Response, NextFunction } from 'express';

export function apiKeyRateLimitMiddleware(rateLimiter: APIKeyRateLimiter) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const apiKey = req.headers['x-api-key'];
    const apiKeyId = req['apiKey']?.id;
    const scopes = req['apiKey']?.scopes || [];
    
    if (!apiKey || !apiKeyId) {
      return next();
    }
    
    const allowed = await rateLimiter.checkRateLimit(apiKeyId, scopes);
    
    if (!allowed) {
      res.set('X-RateLimit-Limit', '1000');
      res.set('X-RateLimit-Remaining', '0');
      res.set('Retry-After', '60');
      return res.status(429).json({ error: 'Rate limit exceeded' });
    }
    
    next();
  };
}
```

---

## Key Revocation

### Revocation System

```typescript
// key-revocation.ts
export class KeyRevocationService {
  constructor(private apiKeyRepository: APIKeyRepository) {}
  
  async revokeKey(keyId: string, reason?: string): Promise<void> {
    await this.apiKeyRepository.update(keyId, {
      isActive: false,
      revokedAt: new Date(),
      revocationReason: reason
    });
  }
  
  async revokeAllKeysForUser(userId: string, reason?: string): Promise<void> {
    await this.apiKeyRepository.updateMany(
      { userId, isActive: true },
      {
        isActive: false,
        revokedAt: new Date(),
        revocationReason: reason
      }
    );
  }
  
  async revokeExpiredKeys(): Promise<void> {
    const expiredKeys = await this.apiKeyRepository.findExpired();
    
    for (const key of expiredKeys) {
      await this.revokeKey(key.id, 'Key expired');
    }
  }
  
  async revokeCompromisedKeys(apiKeyPrefixes: string[]): Promise<void> {
    // Revoke all keys with specific prefixes (security measure)
    await this.apiKeyRepository.updateMany(
      { keyPrefix: { $in: apiKeyPrefixes }, isActive: true },
      {
        isActive: false,
        revokedAt: new Date(),
        revocationReason: 'Security incident'
      }
    );
  }
  
  async isKeyRevoked(keyId: string): Promise<boolean> {
    const key = await this.apiKeyRepository.findById(keyId);
    return !key || !key.isActive || key.revokedAt !== null;
  }
}

// Cron job for cleanup
import cron from 'node-cron';

export class KeyCleanupScheduler {
  constructor(private revocationService: KeyRevocationService) {}
  
  start(): void {
    // Revoke expired keys hourly
    cron.schedule('0 * * * *', async () => {
      await this.revocationService.revokeExpiredKeys();
    });
  }
}
```

---

## Usage Tracking

### Usage Analytics

```typescript
// usage-tracker.ts
export class APIKeyUsageTracker {
  constructor(private usageRepository: UsageRepository) {}
  
  async trackUsage(
    apiKeyId: string,
    endpoint: string,
    method: string,
    statusCode: number,
    responseTime: number
  ): Promise<void> {
    await this.usageRepository.create({
      apiKeyId,
      endpoint,
      method,
      statusCode,
      responseTime,
      timestamp: new Date()
    });
  }
  
  async getUsageStats(apiKeyId: string, days: number = 30): Promise<any> {
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);
    
    const usage = await this.usageRepository.findByApiKeyAndDateRange(
      apiKeyId,
      startDate,
      new Date()
    );
    
    return {
      totalRequests: usage.length,
      successRate: usage.filter(u => u.statusCode < 400).length / usage.length,
      avgResponseTime: usage.reduce((sum, u) => sum + u.responseTime, 0) / usage.length,
      endpoints: this.groupByEndpoint(usage)
    };
  }
  
  private groupByEndpoint(usage: any[]): Record<string, any> {
    const grouped: Record<string, any> = {};
    
    for (const record of usage) {
      const key = `${record.method} ${record.endpoint}`;
      if (!grouped[key]) {
        grouped[key] = {
          count: 0,
          avgResponseTime: 0,
          errors: 0
        };
      }
      
      grouped[key].count++;
      grouped[key].avgResponseTime += record.responseTime;
      if (record.statusCode >= 400) {
        grouped[key].errors++;
      }
    }
    
    // Calculate averages
    for (const key in grouped) {
      grouped[key].avgResponseTime /= grouped[key].count;
    }
    
    return grouped;
  }
}
```

---

## Middleware Implementation

### API Key Middleware

```typescript
// api-key-middleware.ts
import { Request, Response, NextFunction } from 'express';
import { APIKeyStorage } from './api-key-storage';
import { ScopeManager } from './scope-manager';
import { APIKeyRateLimiter } from './api-key-rate-limit';
import { APIKeyUsageTracker } from './usage-tracker';

export interface APIKeyRequest extends Request {
  apiKey?: {
    id: string;
    userId: string;
    name: string;
    scopes: string[];
  };
}

export class APIKeyMiddleware {
  constructor(
    private apiKeyRepository: APIKeyRepository,
    private rateLimiter: APIKeyRateLimiter,
    private usageTracker: APIKeyUsageTracker
  ) {}
  
  middleware() {
    return async (req: APIKeyRequest, res: Response, next: NextFunction) => {
      const apiKey = req.headers['x-api-key'];
      
      if (!apiKey) {
        return res.status(401).json({ error: 'API key required' });
      }
      
      // Find key in database
      const keyRecord = await this.apiKeyRepository.findByKeyHash(apiKey);
      
      if (!keyRecord) {
        return res.status(401).json({ error: 'Invalid API key' });
      }
      
      // Check if key is active
      if (!keyRecord.isActive) {
        return res.status(401).json({ 
          error: 'API key has been revoked',
          revokedAt: keyRecord.revokedAt
        });
      }
      
      // Check if key has expired
      if (keyRecord.expiresAt && keyRecord.expiresAt < new Date()) {
        return res.status(401).json({ error: 'API key has expired' });
      }
      
      // Check rate limit
      const allowed = await this.rateLimiter.checkRateLimit(
        keyRecord.id,
        keyRecord.scopes
      );
      
      if (!allowed) {
        return res.status(429).json({ error: 'Rate limit exceeded' });
      }
      
      // Attach key info to request
      req.apiKey = {
        id: keyRecord.id,
        userId: keyRecord.userId,
        name: keyRecord.name,
        scopes: keyRecord.scopes
      };
      
      // Update last used timestamp
      await this.apiKeyRepository.update(keyRecord.id, {
        lastUsedAt: new Date()
      });
      
      next();
    };
  }
  
  requireScope(requiredScope: string) {
    return (req: APIKeyRequest, res: Response, next: NextFunction) => {
      if (!req.apiKey) {
        return res.status(401).json({ error: 'API key required' });
      }
      
      const hasPermission = ScopeManager.checkPermission(
        req.apiKey.scopes,
        requiredScope
      );
      
      if (!hasPermission) {
        return res.status(403).json({ 
          error: 'Insufficient permissions',
          required: requiredScope
        });
      }
      
      next();
    };
  }
}

// Usage
const apiKeyMiddleware = new APIKeyMiddleware(
  apiKeyRepository,
  new APIKeyRateLimiter(),
  new APIKeyUsageTracker(usageRepository)
);

app.use(apiKeyMiddleware.middleware());

app.get('/api/users', apiKeyMiddleware.requireScope('read'), async (req, res) => {
  const users = await User.find();
  res.json(users);
});
```

---

## Best Practices

### API Key Management Checklist

```markdown
## API Key Management Best Practices

### Generation
- [ ] Use cryptographically secure random generation
- [ ] Include meaningful prefixes (sk_, pk_, etc.)
- [ ] Use sufficient key length (32+ characters)
- [ ] Never expose full keys in logs
- [ ] Only show full key once during creation

### Storage
- [ ] Always hash keys before storage
- [ ] Use bcrypt or SHA-256 for hashing
- [ ] Store hash, not raw key
- [ ] Store key metadata (prefix, scopes, etc.)
- [ ] Implement proper indexing

### Rotation
- [ ] Implement key rotation
- [ ] Schedule automatic rotation
- [ ] Support manual rotation
- [ ] Implement grace period for old keys
- [ ] Notify users before rotation

### Scopes
- [ ] Define clear scope names
- [ ] Document scope permissions
- [ ] Use hierarchical scopes
- [ ] Implement wildcard scopes carefully
- [ ] Validate scopes on each request

### Rate Limiting
- [ ] Implement per-key rate limiting
- [ ] Use different limits for different scopes
- [ ] Return rate limit headers
- [ ] Implement proper backoff
- [ ] Monitor rate limit violations

### Revocation
- [ ] Support immediate revocation
- [ ] Track revocation reasons
- [ ] Implement key expiration
- [ ] Clean up expired keys
- [ ] Audit revocation events

### Monitoring
- [ ] Track API key usage
- [ ] Monitor for suspicious activity
- [ ] Alert on unusual patterns
- [ ] Track success/error rates
- [ ] Implement usage analytics

### Security
- [ ] Never log full API keys
- [ ] Use HTTPS for all API calls
- [ ] Implement proper authentication
- [ ] Validate all requests
- [ ] Implement IP-based restrictions
```

---

## Security Considerations

### Security Checklist

```markdown
## API Key Security Considerations

### Key Generation
- [ ] Use CSPRNG for random generation
- [ ] Minimum 32 bytes of entropy
- [ ] Mix alphanumeric characters
- [ ] Avoid predictable patterns
- [ ] Include version in key

### Storage
- [ ] Hash keys with bcrypt (cost factor >= 10)
- [ ] Use separate salt for each key
- [ ] Store in encrypted database
- [ ] Never store plain text keys
- [ ] Implement proper access controls

### Transport
- [ ] Always use HTTPS
- [ ] Implement TLS 1.2+
- [ ] Use secure cipher suites
- [ ] Implement HSTS
- [ ] Validate certificates

### Validation
- [ ] Validate key format
- [ ] Check key prefix
- [ ] Verify key length
- [ ] Validate key characters
- [ ] Implement rate limiting
- [ ] Check for replay attacks

### Logging
- [ ] Never log full keys
- [ ] Log key prefix only
- [ ] Log authentication attempts
- [ ] Log revocation events
- [ ] Implement audit trail

### Rate Limiting
- [ ] Per-key rate limits
- [ ] Different limits per scope
- [ ] Implement exponential backoff
- [ ] Return proper headers
- [ ] Monitor for abuse
- [ ] Block suspicious keys

### Monitoring
- [ ] Track usage patterns
- [ ] Monitor for anomalies
- [ ] Alert on suspicious activity
- [ ] Implement analytics
- [ ] Review regularly
```

---

## Additional Resources

- [OWASP API Security](https://owasp.org/www-project-api-security)
- [NIST Guidelines](https://csrc.nist.gov/publications/detail/sp800-63)
- [API Key Best Practices](https://api-keys.bestpractices/)
- [Rate Limiting Best Practices](https://cloud.google.com/architecture/rate-limiting)
