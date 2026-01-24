---
name: Secrets & Key Management
description: Secure secrets management: secret managers (AWS Secrets Manager, HashiCorp Vault), key rotation, encryption at rest/in transit, and secret injection patterns
---

# Secrets & Key Management

## Overview

Secure secrets management ใช้ secret managers เช่น AWS Secrets Manager, HashiCorp Vault, Azure Key Vault เพื่อจัดการ secrets, API keys, certificates และ credentials อย่างปลอดภัย รวมถึง key rotation, encryption, และ secret injection

## Why This Matters

- **Security**: Secrets ไม่ถูก hardcode หรือ leak
- **Compliance**: Meet security standards (PCI DSS, SOC 2, GDPR)
- **Auditability**: Track ใครเข้าถึง secrets เมื่อไหร่
- **Rotation**: Auto-rotate keys ลด risk จาก compromised keys

---

## Core Concepts

### 1. Secret Managers

**AWS Secrets Manager:**
```typescript
import { SecretsManagerClient, GetSecretValueCommand } from '@aws-sdk/client-secrets-manager'

const client = new SecretsManagerClient({ region: 'us-east-1' })

export async function getSecret(secretName: string): Promise<string> {
  const command = new GetSecretValueCommand({
    SecretId: secretName,
  })

  const response = await client.send(command)

  if (response.SecretString) {
    return response.SecretString
  }

  throw new Error('Secret not found')
}

// Usage
const dbPassword = await getSecret('prod/db/password')
```

**HashiCorp Vault:**
```typescript
import { Vault } from 'node-vault'

const vault = Vault({
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN,
})

export async function getSecret(path: string): Promise<any> {
  try {
    const result = await vault.read(path)
    return result.data.data
  } catch (error) {
    throw new Error(`Failed to get secret: ${error}`)
  }
}

// Usage
const apiKey = await getSecret('secret/data/api-keys/payment')
```

**Azure Key Vault:**
```typescript
import { SecretClient } from '@azure/keyvault-secrets'
import { DefaultAzureCredential } from '@azure/identity'

const credential = new DefaultAzureCredential()
const client = new SecretClient(
  `https://${process.env.KEY_VAULT_NAME}.vault.azure.net`,
  credential
)

export async function getSecret(secretName: string): Promise<string> {
  const secret = await client.getSecret(secretName)
  return secret.value || ''
}

// Usage
const connectionString = await getSecret('storage-connection-string')
```

### 2. Environment Variable Injection

```typescript
// Load secrets at startup
import { config } from 'dotenv'

config()

interface AppConfig {
  database: {
    host: string
    port: number
    username: string
    password: string
  }
  api: {
    key: string
    endpoint: string
  }
}

export async function loadConfig(): Promise<AppConfig> {
  return {
    database: {
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432'),
      username: process.env.DB_USERNAME!,
      password: process.env.DB_PASSWORD!,
    },
    api: {
      key: process.env.API_KEY!,
      endpoint: process.env.API_ENDPOINT!,
    },
  }
}

// Validate required secrets
function validateConfig(config: AppConfig): void {
  const required = [
    config.database.username,
    config.database.password,
    config.api.key,
  ]

  if (required.some(v => !v)) {
    throw new Error('Missing required secrets')
  }
}
```

### 3. Secret Rotation

```typescript
// AWS Secrets Manager rotation
import {
  SecretsManagerClient,
  RotateSecretCommand,
} from '@aws-sdk/client-secrets-manager'

async function rotateSecret(secretId: string): Promise<void> {
  const client = new SecretsManagerClient()

  const command = new RotateSecretCommand({
    SecretId: secretId,
  })

  await client.send(command)
  console.log(`Secret ${secretId} rotated successfully`)
}

// Schedule rotation
import { CronJob } from 'cron'

const rotationJob = new CronJob('0 0 * * 0', async () => {
  // Rotate every Sunday at midnight
  await rotateSecret('prod/db/password')
  await rotateSecret('prod/api/key')
})

rotationJob.start()

// Custom rotation logic
async function rotateDatabaseCredentials(secretId: string): Promise<void> {
  const client = new SecretsManagerClient()

  // 1. Get current secret
  const current = await getSecret(secretId)
  const { username, password } = JSON.parse(current)

  // 2. Generate new password
  const newPassword = generateSecurePassword()

  // 3. Update database
  await updateDatabasePassword(username, newPassword)

  // 4. Update secret
  await client.send(new PutSecretValueCommand({
    SecretId: secretId,
    SecretString: JSON.stringify({
      username,
      password: newPassword,
    }),
  }))
}

function generateSecurePassword(): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*'
  const password = []
  const randomValues = crypto.randomBytes(32)

  for (let i = 0; i < 32; i++) {
    password.push(chars[randomValues[i] % chars.length])
  }

  return password.join('')
}
```

### 4. Encryption at Rest

```typescript
import crypto from 'crypto'

// AES-256-GCM encryption
const ALGORITHM = 'aes-256-gcm'
const KEY_LENGTH = 32
const IV_LENGTH = 16
const SALT_LENGTH = 64
const TAG_LENGTH = 16

export class EncryptionService {
  private key: Buffer

  constructor(masterKey: string) {
    // Derive encryption key from master key
    this.key = crypto.scryptSync(masterKey, 'salt', KEY_LENGTH)
  }

  encrypt(plaintext: string): string {
    // Generate random IV
    const iv = crypto.randomBytes(IV_LENGTH)

    // Create cipher
    const cipher = crypto.createCipheriv(ALGORITHM, this.key, iv)

    // Encrypt
    let ciphertext = cipher.update(plaintext, 'utf8', 'hex')
    ciphertext += cipher.final('hex')

    // Get auth tag
    const authTag = cipher.getAuthTag()

    // Combine: iv + authTag + ciphertext
    const combined = Buffer.concat([
      iv,
      authTag,
      Buffer.from(ciphertext, 'hex'),
    ])

    return combined.toString('base64')
  }

  decrypt(encrypted: string): string {
    // Decode base64
    const combined = Buffer.from(encrypted, 'base64')

    // Extract components
    const iv = combined.subarray(0, IV_LENGTH)
    const authTag = combined.subarray(IV_LENGTH, IV_LENGTH + TAG_LENGTH)
    const ciphertext = combined.subarray(IV_LENGTH + TAG_LENGTH)

    // Create decipher
    const decipher = crypto.createDecipheriv(ALGORITHM, this.key, iv)
    decipher.setAuthTag(authTag)

    // Decrypt
    let plaintext = decipher.update(ciphertext)
    plaintext = Buffer.concat([plaintext, decipher.final()])

    return plaintext.toString('utf8')
  }
}

// Usage
const encryption = new EncryptionService(process.env.MASTER_KEY!)
const encrypted = encryption.encrypt('sensitive data')
const decrypted = encryption.decrypt(encrypted)
```

### 5. Encryption in Transit

```typescript
import https from 'https'
import fs from 'fs'

// HTTPS server with TLS
const options = {
  key: fs.readFileSync(process.env.TLS_KEY_PATH!),
  cert: fs.readFileSync(process.env.TLS_CERT_PATH!),
  ca: fs.readFileSync(process.env.TLS_CA_PATH!), // Optional: for mutual TLS
  minVersion: 'TLSv1.2', // Require TLS 1.2 or higher
  ciphers: [
    'ECDHE-ECDSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES256-GCM-SHA384',
    'ECDHE-ECDSA-CHACHA20-POLY1305',
    'ECDHE-RSA-CHACHA20-POLY1305',
  ].join(':'),
}

const server = https.createServer(options, (req, res) => {
  res.writeHead(200)
  res.end('Secure connection')
})

server.listen(443)

// HTTPS client with certificate validation
import axios from 'axios'

const httpsAgent = new https.Agent({
  rejectUnauthorized: true, // Validate certificates
  minVersion: 'TLSv1.2',
  ca: fs.readFileSync(process.env.CA_CERT_PATH!), // Custom CA
})

const client = axios.create({
  httpsAgent,
  baseURL: 'https://api.example.com',
})

// Mutual TLS (mTLS)
const mTLSOptions = {
  key: fs.readFileSync(process.env.CLIENT_KEY_PATH!),
  cert: fs.readFileSync(process.env.CLIENT_CERT_PATH!),
  ca: fs.readFileSync(process.env.CA_CERT_PATH!),
  rejectUnauthorized: true,
}

const mTLSAgent = new https.Agent(mTLSOptions)
```

### 6. Secret Injection in Kubernetes

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  db-password: <base64-encoded-password>
  api-key: <base64-encoded-api-key>

---
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        env:
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: db-password
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: api-key

---
# External Secrets Operator (sync from AWS Secrets Manager)
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: external-secrets-sa

---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: db-credentials
    creationPolicy: Owner
  data:
  - secretKey: password
    remoteRef:
      key: prod/db/password
```

### 7. Secret Auditing

```typescript
// Audit log for secret access
interface SecretAccessLog {
  timestamp: Date
  secretName: string
  userId: string
  action: 'read' | 'write' | 'delete'
  success: boolean
  ipAddress: string
}

class SecretAuditor {
  private logs: SecretAccessLog[] = []

  logAccess(
    secretName: string,
    userId: string,
    action: SecretAccessLog['action'],
    success: boolean,
    ipAddress: string
  ): void {
    const log: SecretAccessLog = {
      timestamp: new Date(),
      secretName,
      userId,
      action,
      success,
      ipAddress,
    }

    this.logs.push(log)

    // Send to monitoring/alerting
    this.sendAlert(log)
  }

  private sendAlert(log: SecretAccessLog): void {
    // Alert on suspicious activity
    if (!log.success || log.action === 'delete') {
      console.error('Suspicious secret access:', log)
      // Send to Slack/PagerDuty
    }
  }

  async exportLogs(startDate: Date, endDate: Date): Promise<SecretAccessLog[]> {
    return this.logs.filter(
      log => log.timestamp >= startDate && log.timestamp <= endDate
    )
  }
}

// Wrap secret manager with auditing
class AuditedSecretManager {
  private secretManager: any
  private auditor: SecretAuditor

  constructor(secretManager: any, auditor: SecretAuditor) {
    this.secretManager = secretManager
    this.auditor = auditor
  }

  async getSecret(
    secretName: string,
    userId: string,
    ipAddress: string
  ): Promise<string> {
    try {
      const value = await this.secretManager.getSecret(secretName)
      this.auditor.logAccess(secretName, userId, 'read', true, ipAddress)
      return value
    } catch (error) {
      this.auditor.logAccess(secretName, userId, 'read', false, ipAddress)
      throw error
    }
  }
}
```

### 8. Secret Validation

```typescript
// Validate secrets before use
interface SecretValidation {
  secretName: string
  required: boolean
  pattern?: RegExp
  minLength?: number
  maxLength?: number
}

class SecretValidator {
  private validations: SecretValidation[] = []

  addValidation(validation: SecretValidation): void {
    this.validations.push(validation)
  }

  validate(secrets: Record<string, string>): void {
    const errors: string[] = []

    for (const validation of this.validations) {
      const value = secrets[validation.secretName]

      if (validation.required && !value) {
        errors.push(`Secret ${validation.secretName} is required`)
        continue
      }

      if (value && validation.pattern && !validation.pattern.test(value)) {
        errors.push(`Secret ${validation.secretName} does not match pattern`)
      }

      if (value && validation.minLength && value.length < validation.minLength) {
        errors.push(
          `Secret ${validation.secretName} is too short (min ${validation.minLength})`
        )
      }

      if (value && validation.maxLength && value.length > validation.maxLength) {
        errors.push(
          `Secret ${validation.secretName} is too long (max ${validation.maxLength})`
        )
      }
    }

    if (errors.length > 0) {
      throw new Error(`Secret validation failed:\n${errors.join('\n')}`)
    }
  }
}

// Usage
const validator = new SecretValidator()
validator.addValidation({
  secretName: 'DB_PASSWORD',
  required: true,
  minLength: 16,
})
validator.addValidation({
  secretName: 'API_KEY',
  required: true,
  pattern: /^sk_[a-zA-Z0-9]{32}$/,
})

const secrets = {
  DB_PASSWORD: process.env.DB_PASSWORD,
  API_KEY: process.env.API_KEY,
}

validator.validate(secrets)
```

## Quick Start

```typescript
// 1. Set up secret manager
import { SecretsManagerClient } from '@aws-sdk/client-secrets-manager'

const client = new SecretsManagerClient({ region: 'us-east-1' })

// 2. Load secrets at startup
const dbPassword = await getSecret('prod/db/password')

// 3. Use in config
const config = {
  database: {
    host: process.env.DB_HOST,
    password: dbPassword,
  },
}

// 4. Set up rotation
await rotateSecret('prod/db/password')
```

## Production Checklist

- [ ] Secret manager configured
- [ ] Secrets not hardcoded
- [ ] Secrets not in version control
- [ ] Key rotation enabled
- [ ] Encryption at rest enabled
- [ ] Encryption in transit (TLS 1.2+)
- [ ] Secret auditing enabled
- [ ] Secret validation in place
- [ ] Least privilege access
- [ ] Secret access logging

## Anti-patterns

1. **Hardcoded secrets**: Secrets ใน code หรือ config files
2. **Secrets in version control**: Commit secrets ไป Git
3. **No rotation**: Keys ไม่ถูก rotate
4. **Weak encryption**: ใช้ encryption algorithms เก่า/อ่อนแอ
5. **No audit**: ไม่ track ใครเข้าถึง secrets

## Integration Points

- CI/CD pipelines
- Kubernetes secrets
- Environment variables
- Monitoring/alerting
- Compliance tools

## Further Reading

- [AWS Secrets Manager](https://docs.aws.amazon.com/secretsmanager/)
- [HashiCorp Vault](https://www.vaultproject.io/docs)
- [Azure Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/)
- [OWASP Secret Scanning](https://owasp.org/www-community/Secrets_Detection_Cheat_Sheet)
