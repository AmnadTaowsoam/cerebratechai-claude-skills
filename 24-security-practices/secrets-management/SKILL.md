---
name: Secrets Management
description: Secure storage, rotation, and access control for secrets, credentials, and sensitive configuration.
---

# Secrets Management

## Overview

Secrets management is the practice of securely storing, accessing, and managing sensitive information such as API keys, passwords, certificates, and encryption keys. Proper secrets management prevents credential leakage, enables rotation and auditing, and ensures compliance with security standards.

## Why Secrets Management Matters

### Security Risks of Poor Secrets Management

**Common Vulnerabilities:**
- Hardcoded credentials in source code
- Secrets committed to version control
- Credentials in log files
- Unencrypted secrets in configuration files
- Shared secrets across environments
- Long-lived credentials without rotation

**Real-World Consequences:**
- Data breaches and unauthorized access
- Compliance violations (GDPR, PCI-DSS, SOC 2)
- Financial losses
- Reputational damage
- Legal liabilities

### Benefits of Proper Secrets Management

- **Centralized Control**: Single source of truth for all secrets
- **Access Control**: Fine-grained permissions and role-based access
- **Audit Trail**: Complete visibility into who accessed what and when
- **Rotation**: Automated credential rotation reduces exposure
- **Encryption**: Secrets encrypted at rest and in transit
- **Compliance**: Meets regulatory requirements

## Types of Secrets

### API Keys and Tokens

```javascript
// BAD: Hardcoded API key
const apiKey = 'sk-1234567890abcdef';

// GOOD: Retrieved from secrets manager
const apiKey = await secretsManager.getSecret('api-key');
```

**Examples:**
- Third-party API keys (Stripe, SendGrid, Twilio)
- Internal service API keys
- OAuth tokens
- JWT signing keys

### Database Credentials

```javascript
// BAD: Credentials in code
const dbConfig = {
  host: 'db.example.com',
  user: 'admin',
  password: 'P@ssw0rd123',
  database: 'production'
};

// GOOD: Retrieved from secrets manager
const dbConfig = {
  host: process.env.DB_HOST,
  user: await secretsManager.getSecret('db-user'),
  password: await secretsManager.getSecret('db-password'),
  database: process.env.DB_NAME
};
```

### Encryption Keys

```javascript
// Encryption keys for:
// - Data encryption at rest
// - JWT signing
// - Cookie encryption
// - File encryption

const encryptionKey = await secretsManager.getSecret('encryption-key');
```

### Certificates and Private Keys

```bash
# TLS/SSL certificates
# SSH private keys
# Code signing certificates
# Client certificates
```

### OAuth and SAML Credentials

```javascript
// OAuth client secrets
// SAML signing certificates
// Identity provider credentials
```

## Secrets Management Tools

### HashiCorp Vault

**Setup:**

```bash
# Start Vault server
vault server -dev

# Set Vault address
export VAULT_ADDR='http://127.0.0.1:8200'

# Login
vault login <token>
```

**Storing Secrets:**

```bash
# Write secret
vault kv put secret/myapp/config \
  db_password="supersecret" \
  api_key="sk-1234567890"

# Read secret
vault kv get secret/myapp/config

# Read specific field
vault kv get -field=db_password secret/myapp/config
```

**Using Vault in Node.js:**

```javascript
const vault = require('node-vault')({
  apiVersion: 'v1',
  endpoint: 'http://127.0.0.1:8200',
  token: process.env.VAULT_TOKEN
});

async function getSecret(path) {
  try {
    const result = await vault.read(`secret/data/${path}`);
    return result.data.data;
  } catch (error) {
    console.error('Error reading secret:', error);
    throw error;
  }
}

// Usage
const secrets = await getSecret('myapp/config');
const dbPassword = secrets.db_password;
```

**Dynamic Secrets:**

```bash
# Enable database secrets engine
vault secrets enable database

# Configure database connection
vault write database/config/postgresql \
  plugin_name=postgresql-database-plugin \
  allowed_roles="readonly" \
  connection_url="postgresql://{{username}}:{{password}}@localhost:5432/mydb" \
  username="vault" \
  password="vaultpass"

# Create role
vault write database/roles/readonly \
  db_name=postgresql \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
    GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Generate dynamic credentials
vault read database/creds/readonly
```

### AWS Secrets Manager

**Setup:**

```bash
# Install AWS CLI
aws configure

# Create secret
aws secretsmanager create-secret \
  --name myapp/database \
  --secret-string '{"username":"admin","password":"supersecret"}'
```

**Retrieving Secrets:**

```javascript
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function getSecret(secretName) {
  try {
    const response = await client.send(
      new GetSecretValueCommand({ SecretId: secretName })
    );
    
    if (response.SecretString) {
      return JSON.parse(response.SecretString);
    }
    
    // Binary secret
    const buff = Buffer.from(response.SecretBinary, 'base64');
    return buff.toString('ascii');
  } catch (error) {
    console.error('Error retrieving secret:', error);
    throw error;
  }
}

// Usage
const dbCredentials = await getSecret('myapp/database');
console.log(dbCredentials.username);
console.log(dbCredentials.password);
```

**Automatic Rotation:**

```javascript
// Lambda function for rotation
exports.handler = async (event) => {
  const { Step, Token, SecretId } = event;
  
  switch (Step) {
    case 'createSecret':
      // Generate new password
      const newPassword = generateRandomPassword();
      // Store pending secret
      await secretsManager.putSecretValue({
        SecretId,
        ClientRequestToken: Token,
        SecretString: JSON.stringify({ password: newPassword }),
        VersionStages: ['AWSPENDING']
      });
      break;
      
    case 'setSecret':
      // Update database with new password
      await updateDatabasePassword(newPassword);
      break;
      
    case 'testSecret':
      // Verify new password works
      await testDatabaseConnection(newPassword);
      break;
      
    case 'finishSecret':
      // Mark new version as current
      await secretsManager.updateSecretVersionStage({
        SecretId,
        VersionStage: 'AWSCURRENT',
        MoveToVersionId: Token
      });
      break;
  }
};
```

### AWS Systems Manager Parameter Store

**Setup:**

```bash
# Store parameter
aws ssm put-parameter \
  --name "/myapp/database/password" \
  --value "supersecret" \
  --type "SecureString" \
  --key-id "alias/aws/ssm"

# Retrieve parameter
aws ssm get-parameter \
  --name "/myapp/database/password" \
  --with-decryption
```

**Using in Node.js:**

```javascript
const { SSMClient, GetParameterCommand } = require('@aws-sdk/client-ssm');

const client = new SSMClient({ region: 'us-east-1' });

async function getParameter(name) {
  try {
    const response = await client.send(
      new GetParameterCommand({
        Name: name,
        WithDecryption: true
      })
    );
    return response.Parameter.Value;
  } catch (error) {
    console.error('Error retrieving parameter:', error);
    throw error;
  }
}

// Usage
const dbPassword = await getParameter('/myapp/database/password');
```

### Google Cloud Secret Manager

**Setup:**

```bash
# Create secret
gcloud secrets create myapp-database-password \
  --replication-policy="automatic"

# Add secret version
echo -n "supersecret" | gcloud secrets versions add myapp-database-password --data-file=-

# Access secret
gcloud secrets versions access latest --secret="myapp-database-password"
```

**Using in Node.js:**

```javascript
const { SecretManagerServiceClient } = require('@google-cloud/secret-manager');

const client = new SecretManagerServiceClient();

async function getSecret(secretName) {
  const name = `projects/${projectId}/secrets/${secretName}/versions/latest`;
  
  try {
    const [version] = await client.accessSecretVersion({ name });
    const payload = version.payload.data.toString('utf8');
    return payload;
  } catch (error) {
    console.error('Error accessing secret:', error);
    throw error;
  }
}

// Usage
const dbPassword = await getSecret('myapp-database-password');
```

### Azure Key Vault

**Setup:**

```bash
# Create Key Vault
az keyvault create \
  --name myapp-keyvault \
  --resource-group myResourceGroup \
  --location eastus

# Store secret
az keyvault secret set \
  --vault-name myapp-keyvault \
  --name database-password \
  --value "supersecret"

# Retrieve secret
az keyvault secret show \
  --vault-name myapp-keyvault \
  --name database-password
```

**Using in Node.js:**

```javascript
const { SecretClient } = require('@azure/keyvault-secrets');
const { DefaultAzureCredential } = require('@azure/identity');

const credential = new DefaultAzureCredential();
const vaultUrl = 'https://myapp-keyvault.vault.azure.net';
const client = new SecretClient(vaultUrl, credential);

async function getSecret(secretName) {
  try {
    const secret = await client.getSecret(secretName);
    return secret.value;
  } catch (error) {
    console.error('Error retrieving secret:', error);
    throw error;
  }
}

// Usage
const dbPassword = await getSecret('database-password');
```

### Doppler

**Setup:**

```bash
# Install Doppler CLI
brew install dopplerhq/cli/doppler

# Login
doppler login

# Setup project
doppler setup

# Set secrets
doppler secrets set DB_PASSWORD="supersecret"

# Run app with secrets
doppler run -- node app.js
```

**Using Doppler SDK:**

```javascript
const { Doppler } = require('@dopplerhq/node-sdk');

const doppler = new Doppler({
  token: process.env.DOPPLER_TOKEN
});

async function getSecrets() {
  try {
    const secrets = await doppler.secrets.list({
      project: 'myapp',
      config: 'production'
    });
    return secrets;
  } catch (error) {
    console.error('Error retrieving secrets:', error);
    throw error;
  }
}

// Usage
const secrets = await getSecrets();
const dbPassword = secrets.DB_PASSWORD;
```

## Rotation Strategies

### Manual Rotation

```bash
# 1. Generate new secret
NEW_PASSWORD=$(openssl rand -base64 32)

# 2. Update secrets manager
aws secretsmanager update-secret \
  --secret-id myapp/database \
  --secret-string "{\"password\":\"$NEW_PASSWORD\"}"

# 3. Update database
psql -c "ALTER USER myuser WITH PASSWORD '$NEW_PASSWORD';"

# 4. Restart applications to pick up new secret
kubectl rollout restart deployment/myapp
```

### Scheduled Rotation

```javascript
// Automated rotation using cron
const cron = require('node-cron');

// Rotate every 30 days
cron.schedule('0 0 1 * *', async () => {
  console.log('Starting secret rotation...');
  
  try {
    // Generate new password
    const newPassword = generateSecurePassword();
    
    // Update secrets manager
    await secretsManager.updateSecret('db-password', newPassword);
    
    // Update database
    await updateDatabasePassword(newPassword);
    
    // Notify team
    await notifyTeam('Database password rotated successfully');
    
    console.log('Secret rotation completed');
  } catch (error) {
    console.error('Secret rotation failed:', error);
    await notifyTeam('Secret rotation failed: ' + error.message);
  }
});
```

### Automatic Rotation with AWS

```javascript
// Enable automatic rotation
const { SecretsManagerClient, RotateSecretCommand } = require('@aws-sdk/client-secrets-manager');

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function enableRotation(secretId, lambdaArn) {
  try {
    await client.send(
      new RotateSecretCommand({
        SecretId: secretId,
        RotationLambdaARN: lambdaArn,
        RotationRules: {
          AutomaticallyAfterDays: 30
        }
      })
    );
    console.log('Automatic rotation enabled');
  } catch (error) {
    console.error('Error enabling rotation:', error);
    throw error;
  }
}
```

### Zero-Downtime Rotation

```javascript
// Dual-credential rotation pattern
class DualCredentialRotation {
  constructor(secretsManager) {
    this.secretsManager = secretsManager;
  }
  
  async rotate(secretName) {
    // 1. Create new credential (PENDING)
    const newCredential = await this.generateNewCredential();
    await this.secretsManager.storeSecret(`${secretName}-pending`, newCredential);
    
    // 2. Update service to accept both old and new credentials
    await this.updateServiceToAcceptBoth(secretName);
    
    // 3. Wait for all instances to update
    await this.waitForDeployment();
    
    // 4. Promote new credential to CURRENT
    await this.secretsManager.promoteSecret(`${secretName}-pending`, secretName);
    
    // 5. Revoke old credential
    await this.revokeOldCredential();
    
    // 6. Clean up
    await this.secretsManager.deleteSecret(`${secretName}-pending`);
  }
  
  async generateNewCredential() {
    return crypto.randomBytes(32).toString('hex');
  }
}
```

## Dynamic Secrets

### Database Dynamic Credentials

```javascript
// Vault dynamic database credentials
const vault = require('node-vault')({
  endpoint: 'http://127.0.0.1:8200',
  token: process.env.VAULT_TOKEN
});

async function getDatabaseCredentials() {
  try {
    // Request new credentials (valid for 1 hour)
    const result = await vault.read('database/creds/readonly');
    
    return {
      username: result.data.username,
      password: result.data.password,
      leaseId: result.lease_id,
      leaseDuration: result.lease_duration
    };
  } catch (error) {
    console.error('Error getting dynamic credentials:', error);
    throw error;
  }
}

// Usage with connection pooling
class DynamicDatabasePool {
  constructor() {
    this.pool = null;
    this.leaseId = null;
    this.renewalTimer = null;
  }
  
  async initialize() {
    const creds = await getDatabaseCredentials();
    
    this.pool = new Pool({
      host: process.env.DB_HOST,
      user: creds.username,
      password: creds.password,
      database: process.env.DB_NAME
    });
    
    this.leaseId = creds.leaseId;
    
    // Renew lease before expiration
    this.scheduleRenewal(creds.leaseDuration);
  }
  
  async scheduleRenewal(duration) {
    // Renew at 80% of lease duration
    const renewalTime = duration * 0.8 * 1000;
    
    this.renewalTimer = setTimeout(async () => {
      try {
        await vault.write(`sys/leases/renew`, {
          lease_id: this.leaseId
        });
        console.log('Lease renewed');
        this.scheduleRenewal(duration);
      } catch (error) {
        console.error('Lease renewal failed, rotating credentials');
        await this.rotateCredentials();
      }
    }, renewalTime);
  }
  
  async rotateCredentials() {
    // Get new credentials
    const creds = await getDatabaseCredentials();
    
    // Create new pool
    const newPool = new Pool({
      host: process.env.DB_HOST,
      user: creds.username,
      password: creds.password,
      database: process.env.DB_NAME
    });
    
    // Gracefully close old pool
    await this.pool.end();
    
    // Switch to new pool
    this.pool = newPool;
    this.leaseId = creds.leaseId;
    
    // Schedule next renewal
    this.scheduleRenewal(creds.leaseDuration);
  }
  
  getPool() {
    return this.pool;
  }
}
```

### Temporary Cloud Credentials

```javascript
// AWS STS temporary credentials
const { STSClient, AssumeRoleCommand } = require('@aws-sdk/client-sts');

async function getTemporaryCredentials(roleArn, sessionName) {
  const client = new STSClient({ region: 'us-east-1' });
  
  try {
    const response = await client.send(
      new AssumeRoleCommand({
        RoleArn: roleArn,
        RoleSessionName: sessionName,
        DurationSeconds: 3600 // 1 hour
      })
    );
    
    return {
      accessKeyId: response.Credentials.AccessKeyId,
      secretAccessKey: response.Credentials.SecretAccessKey,
      sessionToken: response.Credentials.SessionToken,
      expiration: response.Credentials.Expiration
    };
  } catch (error) {
    console.error('Error assuming role:', error);
    throw error;
  }
}

// Usage
const tempCreds = await getTemporaryCredentials(
  'arn:aws:iam::123456789012:role/MyRole',
  'my-session'
);

const s3Client = new S3Client({
  region: 'us-east-1',
  credentials: {
    accessKeyId: tempCreds.accessKeyId,
    secretAccessKey: tempCreds.secretAccessKey,
    sessionToken: tempCreds.sessionToken
  }
});
```

## Encryption

### Encryption at Rest

```javascript
// Using AWS KMS for encryption
const { KMSClient, EncryptCommand, DecryptCommand } = require('@aws-sdk/client-kms');

const client = new KMSClient({ region: 'us-east-1' });

async function encryptSecret(plaintext, keyId) {
  try {
    const response = await client.send(
      new EncryptCommand({
        KeyId: keyId,
        Plaintext: Buffer.from(plaintext)
      })
    );
    
    return response.CiphertextBlob.toString('base64');
  } catch (error) {
    console.error('Encryption error:', error);
    throw error;
  }
}

async function decryptSecret(ciphertext) {
  try {
    const response = await client.send(
      new DecryptCommand({
        CiphertextBlob: Buffer.from(ciphertext, 'base64')
      })
    );
    
    return response.Plaintext.toString('utf8');
  } catch (error) {
    console.error('Decryption error:', error);
    throw error;
  }
}

// Usage
const encrypted = await encryptSecret('my-secret-password', 'alias/my-key');
const decrypted = await decryptSecret(encrypted);
```

### Encryption in Transit

```javascript
// TLS configuration for secrets transmission
const https = require('https');
const fs = require('fs');

const options = {
  key: fs.readFileSync('private-key.pem'),
  cert: fs.readFileSync('certificate.pem'),
  ca: fs.readFileSync('ca-cert.pem'),
  requestCert: true,
  rejectUnauthorized: true
};

https.createServer(options, (req, res) => {
  // Handle secure requests
}).listen(443);
```

### Envelope Encryption

```javascript
// Envelope encryption pattern
const crypto = require('crypto');

class EnvelopeEncryption {
  constructor(kmsClient, masterKeyId) {
    this.kmsClient = kmsClient;
    this.masterKeyId = masterKeyId;
  }
  
  async encrypt(plaintext) {
    // 1. Generate data encryption key (DEK)
    const dek = crypto.randomBytes(32);
    
    // 2. Encrypt plaintext with DEK
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipheriv('aes-256-gcm', dek, iv);
    const encrypted = Buffer.concat([
      cipher.update(plaintext, 'utf8'),
      cipher.final()
    ]);
    const authTag = cipher.getAuthTag();
    
    // 3. Encrypt DEK with KMS master key
    const encryptedDek = await this.kmsClient.send(
      new EncryptCommand({
        KeyId: this.masterKeyId,
        Plaintext: dek
      })
    );
    
    // 4. Return encrypted data + encrypted DEK
    return {
      ciphertext: encrypted.toString('base64'),
      encryptedKey: encryptedDek.CiphertextBlob.toString('base64'),
      iv: iv.toString('base64'),
      authTag: authTag.toString('base64')
    };
  }
  
  async decrypt(envelope) {
    // 1. Decrypt DEK with KMS
    const dekResponse = await this.kmsClient.send(
      new DecryptCommand({
        CiphertextBlob: Buffer.from(envelope.encryptedKey, 'base64')
      })
    );
    const dek = dekResponse.Plaintext;
    
    // 2. Decrypt ciphertext with DEK
    const decipher = crypto.createDecipheriv(
      'aes-256-gcm',
      dek,
      Buffer.from(envelope.iv, 'base64')
    );
    decipher.setAuthTag(Buffer.from(envelope.authTag, 'base64'));
    
    const decrypted = Buffer.concat([
      decipher.update(Buffer.from(envelope.ciphertext, 'base64')),
      decipher.final()
    ]);
    
    return decrypted.toString('utf8');
  }
}
```

## Access Control and Auditing

### Role-Based Access Control (RBAC)

```javascript
// Vault policy for RBAC
const policy = `
# Read-only access to application secrets
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}

# Full access to database secrets
path "secret/data/database/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Deny access to production secrets
path "secret/data/production/*" {
  capabilities = ["deny"]
}
`;

// Create policy
await vault.write('sys/policy/myapp-policy', {
  policy: policy
});

// Assign policy to role
await vault.write('auth/approle/role/myapp', {
  policies: ['myapp-policy'],
  secret_id_ttl: '10m',
  token_ttl: '20m',
  token_max_ttl: '30m'
});
```

### Audit Logging

```javascript
// Enable audit logging in Vault
await vault.write('sys/audit/file', {
  type: 'file',
  options: {
    file_path: '/var/log/vault/audit.log'
  }
});

// Parse audit logs
const fs = require('fs');
const readline = require('readline');

async function parseAuditLogs(filePath) {
  const fileStream = fs.createReadStream(filePath);
  const rl = readline.createInterface({
    input: fileStream,
    crlfDelay: Infinity
  });
  
  for await (const line of rl) {
    const entry = JSON.parse(line);
    
    if (entry.type === 'response') {
      console.log(`User: ${entry.auth.display_name}`);
      console.log(`Action: ${entry.request.operation}`);
      console.log(`Path: ${entry.request.path}`);
      console.log(`Time: ${new Date(entry.time)}`);
      console.log('---');
    }
  }
}
```

### AWS CloudTrail for Secrets Access

```javascript
// Query CloudTrail for secrets access
const { CloudTrailClient, LookupEventsCommand } = require('@aws-sdk/client-cloudtrail');

const client = new CloudTrailClient({ region: 'us-east-1' });

async function getSecretsAccessLogs(startTime, endTime) {
  try {
    const response = await client.send(
      new LookupEventsCommand({
        LookupAttributes: [
          {
            AttributeKey: 'EventName',
            AttributeValue: 'GetSecretValue'
          }
        ],
        StartTime: startTime,
        EndTime: endTime
      })
    );
    
    return response.Events.map(event => ({
      time: event.EventTime,
      user: event.Username,
      secretName: JSON.parse(event.CloudTrailEvent).requestParameters.secretId,
      sourceIP: JSON.parse(event.CloudTrailEvent).sourceIPAddress
    }));
  } catch (error) {
    console.error('Error querying CloudTrail:', error);
    throw error;
  }
}

// Usage
const logs = await getSecretsAccessLogs(
  new Date(Date.now() - 24 * 60 * 60 * 1000), // Last 24 hours
  new Date()
);

console.log('Secrets access logs:', logs);
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Retrieve secrets from AWS Secrets Manager
        run: |
          SECRET=$(aws secretsmanager get-secret-value --secret-id myapp/database --query SecretString --output text)
          echo "DB_PASSWORD=$(echo $SECRET | jq -r .password)" >> $GITHUB_ENV
      
      - name: Deploy application
        run: |
          # Use $DB_PASSWORD in deployment
          echo "Deploying with database password"
```

### GitLab CI

```yaml
# .gitlab-ci.yml
deploy:
  stage: deploy
  image: alpine:latest
  
  before_script:
    - apk add --no-cache curl jq
  
  script:
    # Retrieve secrets from Vault
    - export VAULT_TOKEN=$(vault write -field=token auth/approle/login role_id=$ROLE_ID secret_id=$SECRET_ID)
    - export DB_PASSWORD=$(vault kv get -field=password secret/myapp/database)
    
    # Deploy application
    - ./deploy.sh
  
  only:
    - main
```

### Jenkins

```groovy
// Jenkinsfile
pipeline {
  agent any
  
  environment {
    VAULT_ADDR = 'https://vault.example.com'
  }
  
  stages {
    stage('Retrieve Secrets') {
      steps {
        script {
          withCredentials([string(credentialsId: 'vault-token', variable: 'VAULT_TOKEN')]) {
            def secrets = sh(
              script: "vault kv get -format=json secret/myapp/database",
              returnStdout: true
            ).trim()
            
            def secretsJson = readJSON text: secrets
            env.DB_PASSWORD = secretsJson.data.data.password
          }
        }
      }
    }
    
    stage('Deploy') {
      steps {
        sh './deploy.sh'
      }
    }
  }
}
```

## Kubernetes Integration

### External Secrets Operator

```yaml
# Install External Secrets Operator
apiVersion: v1
kind: Namespace
metadata:
  name: external-secrets

---
# SecretStore for AWS Secrets Manager
apiVersion: external-secrets.io/v1beta1
kind: SecretStore
metadata:
  name: aws-secrets-manager
  namespace: myapp
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
# ExternalSecret resource
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: myapp
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  
  target:
    name: database-secret
    creationPolicy: Owner
  
  data:
    - secretKey: username
      remoteRef:
        key: myapp/database
        property: username
    
    - secretKey: password
      remoteRef:
        key: myapp/database
        property: password
```

### Sealed Secrets

```bash
# Install Sealed Secrets controller
kubectl apply -f https://github.com/bitnami-labs/sealed-secrets/releases/download/v0.18.0/controller.yaml

# Install kubeseal CLI
brew install kubeseal

# Create secret
kubectl create secret generic mysecret \
  --from-literal=password=supersecret \
  --dry-run=client -o yaml > mysecret.yaml

# Seal the secret
kubeseal --format=yaml < mysecret.yaml > mysealedsecret.yaml

# Apply sealed secret
kubectl apply -f mysealedsecret.yaml
```

**Sealed Secret Example:**

```yaml
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  name: mysecret
  namespace: myapp
spec:
  encryptedData:
    password: AgBvXYZ...encrypted...data
  template:
    metadata:
      name: mysecret
      namespace: myapp
```

### Vault Agent Sidecar

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
  annotations:
    vault.hashicorp.com/agent-inject: "true"
    vault.hashicorp.com/role: "myapp"
    vault.hashicorp.com/agent-inject-secret-database: "secret/data/myapp/database"
    vault.hashicorp.com/agent-inject-template-database: |
      {{- with secret "secret/data/myapp/database" -}}
      export DB_USERNAME="{{ .Data.data.username }}"
      export DB_PASSWORD="{{ .Data.data.password }}"
      {{- end }}
spec:
  serviceAccountName: myapp
  containers:
    - name: myapp
      image: myapp:latest
      command: ["/bin/sh"]
      args:
        - -c
        - source /vault/secrets/database && ./app
```

## Environment Variables vs Secret Managers

### Environment Variables

**Pros:**
- Simple to use
- Native support in all platforms
- No external dependencies

**Cons:**
- Easy to leak (logs, error messages, process listings)
- No rotation capabilities
- No audit trail
- Visible in container inspect
- Shared across all processes

**Example:**

```javascript
// Using environment variables
const dbPassword = process.env.DB_PASSWORD;

// Risk: Can be leaked in logs
console.log(process.env); // Exposes all secrets!

// Risk: Visible in error stack traces
throw new Error(`Connection failed with password: ${dbPassword}`);
```

### Secret Managers

**Pros:**
- Centralized management
- Automatic rotation
- Audit logging
- Fine-grained access control
- Encryption at rest and in transit
- Version history

**Cons:**
- Additional complexity
- External dependency
- Network latency
- Cost

**Example:**

```javascript
// Using secret manager
const secretsManager = new SecretsManager();
const dbPassword = await secretsManager.getSecret('db-password');

// Secrets are not in environment
console.log(process.env); // No secrets exposed

// Audit trail
// Every access is logged with who, when, and from where
```

### Hybrid Approach

```javascript
// Use secret manager for sensitive secrets
const dbPassword = await secretsManager.getSecret('db-password');
const apiKey = await secretsManager.getSecret('api-key');

// Use environment variables for non-sensitive config
const dbHost = process.env.DB_HOST;
const dbPort = process.env.DB_PORT;
const environment = process.env.NODE_ENV;

const config = {
  database: {
    host: dbHost,
    port: dbPort,
    password: dbPassword // From secret manager
  },
  api: {
    key: apiKey // From secret manager
  },
  environment // From env var
};
```

## Secret Injection Patterns

### Sidecar Injection

```yaml
# Vault sidecar pattern
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  containers:
    # Main application container
    - name: app
      image: myapp:latest
      volumeMounts:
        - name: secrets
          mountPath: /secrets
          readOnly: true
    
    # Vault agent sidecar
    - name: vault-agent
      image: vault:latest
      command:
        - vault
        - agent
        - -config=/vault/config/agent.hcl
      volumeMounts:
        - name: vault-config
          mountPath: /vault/config
        - name: secrets
          mountPath: /secrets
  
  volumes:
    - name: vault-config
      configMap:
        name: vault-agent-config
    - name: secrets
      emptyDir:
        medium: Memory
```

### Init Container

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp
spec:
  initContainers:
    # Fetch secrets before app starts
    - name: secret-fetcher
      image: vault:latest
      command:
        - sh
        - -c
        - |
          vault kv get -field=password secret/myapp/database > /secrets/db-password
          vault kv get -field=api-key secret/myapp/api > /secrets/api-key
      volumeMounts:
        - name: secrets
          mountPath: /secrets
  
  containers:
    - name: app
      image: myapp:latest
      volumeMounts:
        - name: secrets
          mountPath: /secrets
          readOnly: true
  
  volumes:
    - name: secrets
      emptyDir:
        medium: Memory
```

### Runtime Fetch with Caching

```javascript
class SecretsCache {
  constructor(secretsManager, ttl = 300000) { // 5 minutes default
    this.secretsManager = secretsManager;
    this.ttl = ttl;
    this.cache = new Map();
  }
  
  async getSecret(key) {
    const cached = this.cache.get(key);
    
    if (cached && Date.now() - cached.timestamp < this.ttl) {
      return cached.value;
    }
    
    // Fetch from secrets manager
    const value = await this.secretsManager.getSecret(key);
    
    // Cache the value
    this.cache.set(key, {
      value,
      timestamp: Date.now()
    });
    
    return value;
  }
  
  invalidate(key) {
    this.cache.delete(key);
  }
  
  clear() {
    this.cache.clear();
  }
}

// Usage
const cache = new SecretsCache(secretsManager, 300000);
const dbPassword = await cache.getSecret('db-password');
```

## Container Security

### Avoid Baking Secrets into Images

```dockerfile
# BAD: Secret in Dockerfile
FROM node:18
WORKDIR /app
COPY . .
ENV API_KEY=sk-1234567890  # NEVER DO THIS!
RUN npm install
CMD ["node", "app.js"]

# GOOD: Secrets injected at runtime
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "app.js"]
```

### Multi-Stage Builds

```dockerfile
# Build stage
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage
FROM node:18-slim
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
# No secrets in image
CMD ["node", "dist/app.js"]
```

### Docker Secrets

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    image: myapp:latest
    secrets:
      - db_password
      - api_key
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password
      API_KEY_FILE: /run/secrets/api_key

secrets:
  db_password:
    external: true
  api_key:
    external: true
```

```javascript
// Read Docker secrets from files
const fs = require('fs');

function readSecret(secretName) {
  const secretPath = `/run/secrets/${secretName}`;
  try {
    return fs.readFileSync(secretPath, 'utf8').trim();
  } catch (error) {
    console.error(`Error reading secret ${secretName}:`, error);
    throw error;
  }
}

const dbPassword = readSecret('db_password');
const apiKey = readSecret('api_key');
```

## Local Development

### .env Files

```bash
# .env (NOT committed to git)
DB_HOST=localhost
DB_PORT=5432
DB_USER=dev_user
DB_PASSWORD=dev_password
API_KEY=dev_api_key
```

```javascript
// Load .env file
require('dotenv').config();

const config = {
  database: {
    host: process.env.DB_HOST,
    port: process.env.DB_PORT,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD
  },
  api: {
    key: process.env.API_KEY
  }
};
```

**.gitignore:**

```
.env
.env.local
.env.*.local
```

### Mock Secrets for Development

```javascript
// config/secrets.js
class SecretsManager {
  constructor() {
    this.isDevelopment = process.env.NODE_ENV === 'development';
  }
  
  async getSecret(key) {
    if (this.isDevelopment) {
      // Use mock secrets in development
      return this.getMockSecret(key);
    }
    
    // Use real secrets manager in production
    return this.getRealSecret(key);
  }
  
  getMockSecret(key) {
    const mockSecrets = {
      'db-password': 'dev_password',
      'api-key': 'dev_api_key',
      'jwt-secret': 'dev_jwt_secret'
    };
    
    return mockSecrets[key] || 'mock_secret';
  }
  
  async getRealSecret(key) {
    // Fetch from AWS Secrets Manager, Vault, etc.
    const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');
    const client = new SecretsManagerClient({ region: 'us-east-1' });
    
    const response = await client.send(
      new GetSecretValueCommand({ SecretId: key })
    );
    
    return JSON.parse(response.SecretString);
  }
}

module.exports = new SecretsManager();
```

### Local Vault Development

```bash
# Start Vault in dev mode
vault server -dev

# Set environment variables
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'

# Store development secrets
vault kv put secret/myapp/database password=dev_password
vault kv put secret/myapp/api key=dev_api_key
```

## Scanning and Detection

### git-secrets

```bash
# Install git-secrets
brew install git-secrets

# Initialize in repository
cd my-repo
git secrets --install

# Add patterns to detect
git secrets --register-aws

# Scan repository
git secrets --scan

# Scan history
git secrets --scan-history
```

### TruffleHog

```bash
# Install TruffleHog
pip install truffleHog

# Scan repository
trufflehog --regex --entropy=True https://github.com/user/repo

# Scan local directory
trufflehog --regex --entropy=True file:///path/to/repo
```

### Gitleaks

```bash
# Install Gitleaks
brew install gitleaks

# Scan repository
gitleaks detect --source . --verbose

# Scan with custom config
gitleaks detect --config .gitleaks.toml

# Pre-commit hook
gitleaks protect --staged
```

**.gitleaks.toml:**

```toml
title = "Gitleaks Config"

[[rules]]
id = "aws-access-key"
description = "AWS Access Key"
regex = '''(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}'''

[[rules]]
id = "generic-api-key"
description = "Generic API Key"
regex = '''(?i)(api_key|apikey|api-key)['"\s]*[:=]\s*['"]([0-9a-zA-Z\-_]{20,})['"]'''

[[rules]]
id = "private-key"
description = "Private Key"
regex = '''-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----'''
```

### Pre-commit Hooks

```bash
# .git/hooks/pre-commit
#!/bin/sh

# Run Gitleaks
gitleaks protect --staged --verbose

if [ $? -ne 0 ]; then
  echo "⚠️  Gitleaks detected secrets in your changes!"
  echo "Please remove them before committing."
  exit 1
fi

# Run git-secrets
git secrets --pre_commit_hook -- "$@"
```

## Incident Response

### Detection

```javascript
// Automated secret leak detection
const { Octokit } = require('@octokit/rest');

async function scanForLeakedSecrets(owner, repo) {
  const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
  
  // Get recent commits
  const { data: commits } = await octokit.repos.listCommits({
    owner,
    repo,
    per_page: 100
  });
  
  const leaks = [];
  
  for (const commit of commits) {
    const { data: commitData } = await octokit.repos.getCommit({
      owner,
      repo,
      ref: commit.sha
    });
    
    // Check for potential secrets
    for (const file of commitData.files) {
      if (file.patch) {
        const potentialSecrets = detectSecrets(file.patch);
        if (potentialSecrets.length > 0) {
          leaks.push({
            commit: commit.sha,
            file: file.filename,
            secrets: potentialSecrets
          });
        }
      }
    }
  }
  
  return leaks;
}

function detectSecrets(content) {
  const patterns = [
    /(?i)(api_key|apikey|api-key)['"\s]*[:=]\s*['"]([0-9a-zA-Z\-_]{20,})['"]/g,
    /(?i)(password|passwd|pwd)['"\s]*[:=]\s*['"]([^\s'"]{8,})['"]/g,
    /(sk|pk)_live_[0-9a-zA-Z]{24,}/g, // Stripe keys
    /AIza[0-9A-Za-z\-_]{35}/g, // Google API keys
  ];
  
  const found = [];
  for (const pattern of patterns) {
    const matches = content.matchAll(pattern);
    for (const match of matches) {
      found.push({
        type: match[1] || 'unknown',
        value: match[0]
      });
    }
  }
  
  return found;
}
```

### Immediate Response

```javascript
// Automated secret rotation on leak detection
async function respondToSecretLeak(secretType, secretValue) {
  console.log(`🚨 Secret leak detected: ${secretType}`);
  
  // 1. Revoke the leaked secret immediately
  await revokeSecret(secretType, secretValue);
  console.log('✅ Secret revoked');
  
  // 2. Generate new secret
  const newSecret = await generateNewSecret(secretType);
  console.log('✅ New secret generated');
  
  // 3. Update secrets manager
  await updateSecretsManager(secretType, newSecret);
  console.log('✅ Secrets manager updated');
  
  // 4. Notify team
  await notifyTeam({
    type: 'SECRET_LEAK',
    secretType,
    timestamp: new Date(),
    action: 'Secret revoked and rotated'
  });
  console.log('✅ Team notified');
  
  // 5. Create incident ticket
  await createIncidentTicket({
    title: `Secret Leak: ${secretType}`,
    description: `A ${secretType} was detected in a commit and has been automatically revoked and rotated.`,
    severity: 'HIGH'
  });
  console.log('✅ Incident ticket created');
  
  // 6. Audit access logs
  const accessLogs = await getAccessLogs(secretType, Date.now() - 24 * 60 * 60 * 1000);
  console.log(`📊 Access logs retrieved: ${accessLogs.length} entries`);
  
  return {
    revoked: true,
    newSecretGenerated: true,
    teamNotified: true,
    incidentCreated: true
  };
}
```

### Post-Incident Review

```javascript
// Generate incident report
async function generateIncidentReport(incidentId) {
  const incident = await getIncident(incidentId);
  
  const report = {
    incidentId,
    timestamp: incident.timestamp,
    secretType: incident.secretType,
    detectionMethod: incident.detectionMethod,
    
    timeline: [
      {
        time: incident.leakTime,
        event: 'Secret leaked in commit'
      },
      {
        time: incident.detectionTime,
        event: 'Leak detected by automated scan'
      },
      {
        time: incident.revocationTime,
        event: 'Secret revoked'
      },
      {
        time: incident.rotationTime,
        event: 'New secret generated and deployed'
      }
    ],
    
    exposureWindow: {
      start: incident.leakTime,
      end: incident.revocationTime,
      duration: incident.revocationTime - incident.leakTime
    },
    
    accessLogs: await getAccessLogs(
      incident.secretType,
      incident.leakTime,
      incident.revocationTime
    ),
    
    recommendations: [
      'Enable pre-commit hooks to prevent future leaks',
      'Conduct security training for developers',
      'Review and update secret scanning patterns',
      'Implement automated secret rotation'
    ]
  };
  
  return report;
}
```

## Best Practices

### 1. Never Hardcode Secrets

```javascript
// ❌ BAD
const apiKey = 'sk-1234567890abcdef';
const dbPassword = 'P@ssw0rd123';

// ✅ GOOD
const apiKey = await secretsManager.getSecret('api-key');
const dbPassword = await secretsManager.getSecret('db-password');
```

### 2. Use Short-Lived Credentials

```javascript
// ✅ GOOD: Request temporary credentials
const tempCreds = await getTemporaryCredentials({
  role: 'data-processor',
  duration: 3600 // 1 hour
});

// Use credentials
const client = new S3Client({ credentials: tempCreds });

// Credentials automatically expire after 1 hour
```

### 3. Implement Least Privilege

```javascript
// ✅ GOOD: Service-specific secrets with minimal permissions
const readOnlyDbCreds = await secretsManager.getSecret('db-readonly');
const writeDbCreds = await secretsManager.getSecret('db-write');

// Use read-only credentials for queries
const queryClient = new DatabaseClient(readOnlyDbCreds);

// Use write credentials only when needed
const writeClient = new DatabaseClient(writeDbCreds);
```

### 4. Rotate Regularly

```javascript
// ✅ GOOD: Automated rotation schedule
const rotationSchedule = {
  'api-keys': 30, // days
  'database-passwords': 90,
  'encryption-keys': 365
};

async function scheduleRotations() {
  for (const [secretType, days] of Object.entries(rotationSchedule)) {
    cron.schedule(`0 0 */${days} * *`, async () => {
      await rotateSecret(secretType);
    });
  }
}
```

### 5. Monitor and Audit

```javascript
// ✅ GOOD: Comprehensive audit logging
class AuditedSecretsManager {
  async getSecret(key) {
    const startTime = Date.now();
    
    try {
      const secret = await this.secretsManager.getSecret(key);
      
      await this.logAccess({
        action: 'GET_SECRET',
        key,
        user: this.getCurrentUser(),
        timestamp: new Date(),
        duration: Date.now() - startTime,
        success: true
      });
      
      return secret;
    } catch (error) {
      await this.logAccess({
        action: 'GET_SECRET',
        key,
        user: this.getCurrentUser(),
        timestamp: new Date(),
        duration: Date.now() - startTime,
        success: false,
        error: error.message
      });
      
      throw error;
    }
  }
}
```

## Anti-Patterns

### 1. Secrets in Version Control

```bash
# ❌ BAD: Committing secrets
git add .env
git commit -m "Add configuration"

# ✅ GOOD: Exclude secrets from version control
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
```

### 2. Sharing Secrets Across Services

```javascript
// ❌ BAD: One secret for all services
const sharedApiKey = await secretsManager.getSecret('shared-api-key');

// ✅ GOOD: Service-specific secrets
const userServiceKey = await secretsManager.getSecret('user-service-api-key');
const orderServiceKey = await secretsManager.getSecret('order-service-api-key');
```

### 3. Long-Lived Tokens

```javascript
// ❌ BAD: Token that never expires
const permanentToken = 'token-that-lasts-forever';

// ✅ GOOD: Short-lived tokens with refresh
const accessToken = await getAccessToken({ expiresIn: '15m' });
const refreshToken = await getRefreshToken({ expiresIn: '7d' });
```

### 4. Secrets in Logs

```javascript
// ❌ BAD: Logging secrets
console.log(`Connecting with password: ${password}`);
logger.info({ apiKey, userId });

// ✅ GOOD: Redact secrets from logs
console.log('Connecting to database');
logger.info({ userId }); // No sensitive data
```

### 5. Unencrypted Secrets

```javascript
// ❌ BAD: Storing secrets in plain text
fs.writeFileSync('secrets.txt', apiKey);
```

---

## Quick Start

### Using Environment Variables

```bash
# .env file (never commit!)
DATABASE_URL=postgresql://user:pass@localhost/db
API_KEY=sk-1234567890
SECRET_KEY=your-secret-key
```

```javascript
// Load from environment
require('dotenv').config()

const dbUrl = process.env.DATABASE_URL
const apiKey = process.env.API_KEY
```

### Using AWS Secrets Manager

```javascript
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager')

const client = new SecretsManagerClient({ region: 'us-east-1' })

async function getSecret(secretName) {
  const command = new GetSecretValueCommand({ SecretId: secretName })
  const response = await client.send(command)
  return JSON.parse(response.SecretString)
}

// Usage
const secrets = await getSecret('my-app/secrets')
const dbPassword = secrets.DATABASE_PASSWORD
```

### Using HashiCorp Vault

```bash
# Install Vault CLI
vault auth -method=aws
vault read secret/my-app/database
```

```javascript
const vault = require('node-vault')({ apiVersion: 'v1' })

const secrets = await vault.read('secret/my-app/database')
const dbPassword = secrets.data.password
```

---

## Production Checklist

- [ ] **No Hardcoded Secrets**: Never commit secrets to version control
- [ ] **Environment Variables**: Use .env files (gitignored) for local development
- [ ] **Secrets Manager**: Use cloud secrets manager (AWS, Azure, GCP) in production
- [ ] **Rotation**: Implement secret rotation policies
- [ ] **Access Control**: Limit access to secrets (principle of least privilege)
- [ ] **Encryption**: Encrypt secrets at rest and in transit
- [ ] **Audit Logging**: Log all secret access
- [ ] **Backup**: Backup secrets securely
- [ ] **Testing**: Use separate test secrets, never production secrets in tests
- [ ] **Documentation**: Document where secrets are stored and how to access
- [ ] **Monitoring**: Monitor for secret leaks or unauthorized access
- [ ] **Incident Response**: Have plan for secret compromise

---

## Anti-patterns

### ❌ Don't: Commit Secrets to Git

```javascript
// ❌ Bad - Committed to repo
const config = {
  apiKey: 'sk-1234567890',  // Exposed!
  dbPassword: 'mypassword'
}
```

```javascript
// ✅ Good - Use environment variables
const config = {
  apiKey: process.env.API_KEY,
  dbPassword: process.env.DB_PASSWORD
}
```

### ❌ Don't: Log Secrets

```javascript
// ❌ Bad - Secrets in logs
console.log('API Key:', apiKey)  // Exposed in logs!
logger.info({ apiKey })  // Exposed!
```

```javascript
// ✅ Good - Never log secrets
console.log('API Key configured')  // Generic message
logger.info({ hasApiKey: !!apiKey })  // Boolean only
```

### ❌ Don't: Share Secrets via Email/Chat

```javascript
// ❌ Bad - Sent via insecure channel
// Email: "Here's the API key: sk-1234567890"
```

```javascript
// ✅ Good - Use secure secrets manager
// Share access to secrets manager, not the secret itself
```

### ❌ Don't: No Secret Rotation

```javascript
// ❌ Bad - Same secret forever
const API_KEY = 'sk-1234567890'  // Never rotated
```

```javascript
// ✅ Good - Rotate regularly
// Implement rotation policy (e.g., every 90 days)
// Use secrets manager with automatic rotation
```

---

## Integration Points

- **Error Handling** (`03-backend-api/error-handling/`) - Don't expose secrets in errors
- **Logging** (`14-monitoring-observability/logging/`) - Secure logging practices
- **CI/CD** (`15-devops-infrastructure/ci-cd-github-actions/`) - Secure secret injection

---

## Further Reading

- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/)
- [HashiCorp Vault](https://www.vaultproject.io/)

// ✅ GOOD: Encrypt before storing
const encrypted = await encrypt(apiKey, encryptionKey);
fs.writeFileSync('secrets.enc', encrypted);
```

## Related Skills

- `10-authentication-authorization/jwt-auth`
- `15-devops-infrastructure/kubernetes-helm`
- `24-security-practices/secure-coding`
- `03-backend-api/middleware`
- `09-microservices/service-mesh`
