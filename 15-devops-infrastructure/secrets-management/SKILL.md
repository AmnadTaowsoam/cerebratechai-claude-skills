# Secrets Management

## Overview

Secrets management is critical for securing sensitive data like passwords, API keys, and certificates. This skill covers tools, patterns, and best practices.

## Table of Contents

1. [Secrets Management Principles](#secrets-management-principles)
2. [Tools](#tools)
3. [.env Files (Development)](#env-files-development)
4. [Secrets Rotation](#secrets-rotation)
5. [Access Control](#access-control)
6. [Encryption at Rest](#encryption-at-rest)
7. [Application Integration](#application-integration)
8. [CI/CD Integration](#cicd-integration)
9. [Audit Logging](#audit-logging)
10. [Best Practices](#best-practices)

---

## Secrets Management Principles

### Core Principles

1. **Never commit secrets to version control**
2. **Use environment-specific secrets**
3. **Rotate secrets regularly**
4. **Use least privilege access**
5. **Audit secret access**
6. **Encrypt secrets at rest**
7. **Use secure secret storage**
8. **Implement secret rotation**

### Security Hierarchy

```
┌─────────────────────────────────────┐
│   Application Secrets             │
│   (Database URLs, API Keys)       │
└──────────┬──────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│   Secret Management Service       │
│   (Vault, Secrets Manager, etc.)   │
└──────────┬──────────────────────┘
           │
           ↓
┌─────────────────────────────────────┐
│   Encryption & Access Control    │
└─────────────────────────────────────┘
```

---

## Tools

### HashiCorp Vault

#### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  vault:
    image: hashicorp/vault:latest
    container_name: vault
    ports:
      - "8200:8200"
    environment:
      - VAULT_DEV_ROOT_TOKEN_ID=my-root-token
      - VAULT_DEV_LISTEN_ADDRESS=0.0.0.0:8200
    cap_add:
      - IPC_LOCK
    volumes:
      - vault_data:/vault/data
    command: server -dev
    networks:
      - vault

networks:
  vault:
    driver: bridge

volumes:
  vault_data:
```

#### Terraform

```hcl
# vault.tf
resource "aws_kms_key" "vault" {
  description = "KMS key for Vault encryption"
  enable_key_rotation = true
}

resource "aws_iam_role" "vault" {
  name = "vault-server"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "kms:Decrypt",
          "kms:Encrypt",
          "kms:GenerateDataKey"
        ]
        Effect = "Allow"
        Resource = aws_kms_key.vault.arn
      }
    ]
  })
}

resource "aws_instance" "vault" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t3.medium"
  key_name      = aws_key_pair.vault.key_name
  subnet_id     = module.vpc.private_subnet_ids[0]
  vpc_security_group_ids = [module.vpc.security_group_id]

  user_data = filebase64("${path.module}/vault-init.sh")

  tags = {
    Name = "vault-server"
  }
}
```

### AWS Secrets Manager

#### Terraform

```hcl
# secrets-manager.tf
resource "aws_secretsmanager_secret" "database" {
  name = "prod/database/url"

  secret_string = jsonencode({
    host     = "db.example.com"
    port     = 5432
    username = "admin"
    password = "secretpassword"
    database = "myapp"
  })

  tags = {
    Environment = "production"
    Application = "myapp"
  }
}

resource "aws_secretsmanager_secret" "api" {
  name = "prod/api/key"

  secret_string = "my-api-key-12345"

  tags = {
    Environment = "production"
    Application = "myapp"
  }
}
```

#### AWS CLI

```bash
# Create secret
aws secretsmanager create-secret \
  --name prod/database/url \
  --secret-string '{"host":"db.example.com","port":5432,"username":"admin","password":"secretpassword","database":"myapp"}'

# Get secret
aws secretsmanager get-secret-value \
  --secret-id prod/database/url \
  --query SecretString \
  --output text

# Update secret
aws secretsmanager put-secret-value \
  --secret-id prod/database/url \
  --secret-string '{"host":"db.example.com","port":5432,"username":"admin","password":"newpassword","database":"myapp"}'

# Delete secret
aws secretsmanager delete-secret \
  --secret-id prod/database/url
```

### Kubernetes Secrets

#### Create Secret

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: myapp-secret
  namespace: production
type: Opaque
stringData:
  database-url: postgresql://user:password@db:5432/mydb
  api-key: my-api-key-12345
```

```bash
# Create from file
kubectl create secret generic myapp-secret \
  --from-env-file=.env.production \
  --namespace=production

# Create from literal
kubectl create secret generic myapp-secret \
  --from-literal=database-url=postgresql://user:password@db:5432/mydb \
  --namespace=production
```

#### Use Secret in Pod

```yaml
# pod.yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  namespace: production
spec:
  containers:
    - name: myapp
      image: myapp:latest
      env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: myapp-secret
              key: database-url
        - name: API_KEY
          valueFrom:
            secretKeyRef:
              name: myapp-secret
              key: api-key
```

### Docker Secrets

#### Create Secret

```bash
# Create secret
echo "my-secret-password" | docker secret create myapp-secret -

# Create from file
docker secret create myapp-secret ./secret.txt

# Create from environment
docker secret create myapp-secret --env-file=.env
```

#### Use Secret in Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    image: myapp:latest
    secrets:
      - database_url
      - api_key

secrets:
  database_url:
    file: ./database_url.txt
  api_key:
    external: true
```

---

## .env Files (Development)

### Node.js

```javascript
// config.js
require('dotenv').config();

module.exports = {
  database: {
    url: process.env.DATABASE_URL,
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT || '5432'),
    username: process.env.DB_USERNAME,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
  },
  api: {
    key: process.env.API_KEY,
    secret: process.env.API_SECRET,
  },
};
```

```bash
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=user
DB_PASSWORD=password
DB_NAME=mydb

API_KEY=my-api-key-12345
API_SECRET=my-api-secret-67890
```

```javascript
// .env.example
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=user
DB_PASSWORD=password
DB_NAME=mydb

API_KEY=your-api-key-here
API_SECRET=your-api-secret-here
```

### Python

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', '5432'))
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    
    API_KEY = os.getenv('API_KEY')
    API_SECRET = os.getenv('API_SECRET')

config = Config()
```

```bash
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=user
DB_PASSWORD=password
DB_NAME=mydb

API_KEY=my-api-key-12345
API_SECRET=my-api-secret-67890
```

```bash
# .env.example
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=user
DB_PASSWORD=password
DB_NAME=mydb

API_KEY=your-api-key-here
API_SECRET=your-api-secret-here
```

---

## Secrets Rotation

### Vault Rotation

```bash
# Enable rotation
vault secrets enable -path=database database

vault write database/config/myapp \
  plugin_name=postgresql-database-plugin \
  allowed_roles="myapp-role" \
  connection_url="postgresql://user:pass@db:5432/mydb"

vault write database/roles/myapp-role \
  db_name=myapp \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}';" \
  default_ttl="1h" \
  max_ttl="24h" \
  rotation_statements="ALTER ROLE \"{{name}}\" WITH PASSWORD '{{password}}';"

# Rotate credentials
vault write -f database/rotate-credentials/myapp-role
```

### AWS Secrets Manager Rotation

```hcl
# rotation.tf
resource "aws_secretsmanager_secret" "database" {
  name = "prod/database/credentials"

  secret_string = jsonencode({
    host     = "db.example.com"
    port     = 5432
    username = "admin"
    password = "secretpassword"
    database = "myapp"
  })

  tags = {
    Environment = "production"
    Application = "myapp"
  }
}

resource "aws_secretsmanager_secret_rotation" "database" {
  secret_id           = aws_secretsmanager_secret.database.id
  rotation_lambda_arn = aws_lambda_function.rotation.arn

  rotation_rules {
    automatically_after_days = 90
  }
}

resource "aws_lambda_function" "rotation" {
  function_name = "secrets-rotation"
  runtime       = "python3.9"
  handler       = "lambda_function.lambda_handler"
  role          = aws_iam_role.lambda.arn

  environment {
    SECRET_ID = aws_secretsmanager_secret.database.id
  }

  s3_bucket = aws_s3_bucket.lambda_bucket.id
  s3_key    = "secrets-rotation.zip"

  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
}
```

---

## Access Control

### Vault Policies

```hcl
# vault-policy.hcl
path "database/creds/myapp" {
  capabilities = ["read"]
}

path "database/rotate/myapp" {
  capabilities = ["update"]
}

path "sys/leases/renew/database/creds/myapp" {
  capabilities = ["update"]
}
```

```bash
# Create policy
vault policy write myapp-policy vault-policy.hcl

# Create role with policy
vault write auth/approle/role/myapp \
  policies=myapp-policy \
  token_ttl=1h \
  token_max_ttl=24h
```

### AWS IAM Policies

```hcl
# iam.tf
resource "aws_iam_role" "secrets_reader" {
  name = "secrets-reader"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue",
          "secretsmanager:DescribeSecret"
        ]
        Resource = "arn:aws:secretsmanager:us-east-1:123456789012:secret:prod/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "secrets_reader" {
  role       = aws_iam_role.secrets_reader.name
  policy_arn = "arn:aws:iam::aws:policy/SecretsReader"
}
```

### Kubernetes RBAC

```yaml
# rbac.yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: secret-reader
  namespace: production
rules:
  - apiGroups: [""]
    resources: ["secrets"]
    verbs: ["get", "list"]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: secret-reader-binding
  namespace: production
subjects:
  - kind: ServiceAccount
    name: myapp-sa
roleRef:
  kind: Role
  name: secret-reader
  apiGroup: rbac.authorization.k8s.io
```

---

## Encryption at Rest

### Vault Encryption

```bash
# Enable transit engine
vault secrets enable transit

# Create encryption key
vault write -f transit/keys/myapp-key \
  type=aes256-gcm96 \
  convergent_encryption=true

# Encrypt data
vault write transit/encrypt/myapp-key \
  plaintext=$(echo -n "my-secret-data" | base64)

# Decrypt data
vault write transit/decrypt/myapp-key \
  ciphertext=<encrypted-text>
```

### AWS KMS Encryption

```bash
# Create KMS key
aws kms create-key \
  --description "Encryption key for myapp" \
  --key-usage ENCRYPT_DECRYPT \
  --origin AWS_KMS

# Encrypt data
aws kms encrypt \
  --key-id <key-id> \
  --plaintext fileb://<(echo -n "my-secret-data") \
  --output text \
  --query CiphertextBlob

# Decrypt data
aws kms decrypt \
  --ciphertext-fileb://<(echo -n "<encrypted-data>") \
  --output text \
  --query Plaintext
```

---

## Application Integration

### Node.js with Vault

```typescript
// vault-client.ts
import { Vault } from 'node-vault';

const vault = new Vault({
  endpoint: process.env.VAULT_ADDR || 'http://localhost:8200',
  token: process.env.VAULT_TOKEN,
});

async function getSecret(path: string): Promise<any> {
  const result = await vault.read(path);
  return result.data;
}

async function getDatabaseCredentials(): Promise<{
  host: string;
  port: number;
  username: string;
  password: string;
  database: string;
}> {
  const creds = await getSecret('database/creds/myapp');
  return creds;
}

// Usage
const dbCreds = await getDatabaseCredentials();
console.log('Database credentials:', dbCreds);
```

### Python with Vault

```python
# vault_client.py
import hvac
import os

class VaultClient:
    def __init__(self):
        self.client = hvac.Client(
            url=os.getenv('VAULT_ADDR', 'http://localhost:8200'),
            token=os.getenv('VAULT_TOKEN')
        )
    
    def get_secret(self, path: str) -> dict:
        """Get secret from Vault."""
        response = self.client.secrets.kv.v1.read_secret_version(
            path=path,
            raise_exception_on_deleted_version=False
        )
        return response['data']['data']
    
    def get_database_credentials(self) -> dict:
        """Get database credentials from Vault."""
        return self.get_secret('database/creds/myapp')

# Usage
vault = VaultClient()
creds = vault.get_database_credentials()
print(f"Database credentials: {creds}")
```

### Node.js with AWS Secrets Manager

```typescript
// secrets-manager.ts
import {
  SecretsManagerClient,
  GetSecretValueCommand,
} from '@aws-sdk/client-secrets-manager';

const client = new SecretsManagerClient({ region: 'us-east-1' });

async function getSecret(secretId: string): Promise<string> {
  const command = new GetSecretValueCommand({
    SecretId: secretId,
  });

  const response = await client.send(command);
  return response.SecretString || '';
}

async function getDatabaseUrl(): Promise<string> {
  const secret = await getSecret('prod/database/url');
  const dbConfig = JSON.parse(secret);
  return dbConfig.url;
}

// Usage
const dbUrl = await getDatabaseUrl();
console.log('Database URL:', dbUrl);
```

### Python with AWS Secrets Manager

```python
# secrets_manager.py
import boto3
import os
import json

class SecretsManagerClient:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region)
    
    def get_secret(self, secret_id: str) -> str:
        """Get secret from AWS Secrets Manager."""
        response = self.client.get_secret_value(
            SecretId=secret_id
        )
        return response['SecretString']
    
    def get_database_url(self) -> str:
        """Get database URL from AWS Secrets Manager."""
        secret = self.get_secret('prod/database/url')
        db_config = json.loads(secret)
        return db_config['url']

# Usage
client = SecretsManagerClient()
db_url = client.get_database_url()
print(f"Database URL: {db_url}")
```

---

## CI/CD Integration

### GitHub Actions with Vault

```yaml
# .github/workflows/ci.yml
name: CI

on: push

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Vault CLI
        run: |
          wget -O- https://releases.hashicorp.com/vault/${{ vault_version }}/vault_${{ vault_version }}_linux_amd64.zip
          unzip vault_${{ vault_version }}_linux_amd64.zip
          sudo mv vault /usr/local/bin/

      - name: Get Vault token
        id: vault-token
        run: |
          echo "VAULT_TOKEN=$(vault token create -role=github-actions -ttl=1h)" >> $GITHUB_OUTPUT

      - name: Get secrets
        env:
          VAULT_ADDR: ${{ secrets.VAULT_ADDR }}
          VAULT_TOKEN: ${{ steps.vault-token.outputs.VAULT_TOKEN }}
        run: |
          vault kv get -field=database_url database/creds/myapp
```

### GitHub Actions with AWS Secrets

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
        uses: aws-actions/configure-aws-credentials@v1
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: us-east-1

      - name: Get secrets
        id: secrets
        run: |
          echo "DATABASE_URL=$(aws secretsmanager get-secret-value --secret-id prod/database/url --query SecretString --output text)" >> $GITHUB_OUTPUT

      - name: Deploy
        env:
          DATABASE_URL: ${{ steps.secrets.outputs.DATABASE_URL }}
        run: npm run deploy
```

### Terraform with Vault

```hcl
# terraform.tf
terraform {
  backend "s3" {
    bucket = "my-terraform-state"
    key    = "vault/terraform.tfstate"
    region = "us-east-1"
    encrypt = true
  }
}

provider "vault" {
  address = var.vault_addr
  token   = var.vault_token
}

variable "vault_addr" {
  description = "Vault address"
  type        = string
  default     = "http://localhost:8200"
}

variable "vault_token" {
  description = "Vault token"
  type        = string
  sensitive   = true
}

data "vault_generic_secret" "database" {
  path = "database/creds/myapp"
}

output "database_url" {
  value     = data.vault_generic_secret.database.data["url"]
  sensitive = true
}
```

---

## Audit Logging

### Vault Audit

```bash
# Enable audit logging
vault audit enable file file_path=/var/log/vault_audit.log

# View audit logs
tail -f /var/log/vault_audit.log
```

### AWS CloudTrail

```hcl
# cloudtrail.tf
resource "aws_cloudtrail" "vault" {
  name                          = "vault-audit-trail"
  s3_bucket_name               = aws_s3_bucket.cloudtrail.id
  include_global_service_events = true

  event_selector {
    read_write_type           = "All"
    include_management_events = false
    data_resource {
      type = "AWS::SecretsManager::Secret"
    }
  }

  tags = {
    Name = "vault-audit-trail"
  }
}

resource "aws_s3_bucket" "cloudtrail" {
  bucket = "my-vault-cloudtrail-bucket"
  acl    = "private"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    id      = "expire"
    enabled = true
    noncurrent_version_expiration {
      days = 90
    }
  }

  tags = {
    Name = "vault-cloudtrail-bucket"
  }
}
```

---

## Best Practices

### 1. Never Commit Secrets

```bash
# .gitignore
.env
.env.local
.env.*.local
*.key
*.pem
secrets/
```

### 2. Use Environment-Specific Secrets

```bash
# Development
.env.development

# Staging
.env.staging

# Production
.env.production
```

### 3. Rotate Secrets Regularly

```bash
# Rotate database credentials every 90 days
# Rotate API keys every 30 days
# Rotate certificates before expiration
```

### 4. Use Least Privilege

```hcl
# Grant only necessary permissions
resource "aws_iam_role" "database_reader" {
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "arn:aws:secretsmanager:us-east-1:123456789012:secret:prod/database/*"
      }
    ]
  })
}
```

### 5. Audit Secret Access

```bash
# Enable audit logging
# Review audit logs regularly
# Alert on suspicious activity
```

---

## Summary

This skill covers comprehensive secrets management implementation including:

- **Secrets Management Principles**: Core principles and security hierarchy
- **Tools**: HashiCorp Vault, AWS Secrets Manager, Kubernetes Secrets, Docker Secrets
- **.env Files**: Node.js and Python configuration
- **Secrets Rotation**: Vault and AWS Secrets Manager rotation
- **Access Control**: Vault policies, AWS IAM policies, Kubernetes RBAC
- **Encryption at Rest**: Vault transit, AWS KMS encryption
- **Application Integration**: Node.js and Python with Vault and AWS Secrets Manager
- **CI/CD Integration**: GitHub Actions with Vault and AWS Secrets, Terraform with Vault
- **Audit Logging**: Vault audit, AWS CloudTrail
- **Best Practices**: Never commit secrets, environment-specific secrets, rotation, least privilege, audit access
